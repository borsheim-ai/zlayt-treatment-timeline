"""T-045 AC2: the R-EX-1 matrix. The letter ('Treatment section') holds accepted entries and accepted charges only; no flag, note, count, day-count or AI-assistance text ever reaches it.

test_letter_isolation.py proves the rule on the sample case with one note. This matrix proves it across the whole recorded set (sample + case_01..09 = 10 cases) and three decision profiles:
  A  accept everything the server lets you accept, and put a reviewer note on EVERY flag (the flags are accepted by that edit);
  B  accept exactly the same entries and amounts, dismiss every flag, no note;
  C  accept every other entry only, leave the rest and all flags pending.
Properties (each derived from the case's own API data, never from a copy kept here):
  1. letter(A) == letter(B): flag decisions and notes cannot change a single character of the letter.
  2. Take the letter and remove the text of the accepted entries (summary, quote, heading) and accepted charges (line, quote): what is left holds none of this case's flag titles, explanations,
     type labels, '<N> days' for a gap, the reviewer-note text, 'AI assistance', 'Pending', 'Reviewer note', or an 'N of M records' count line.
  3. export.items names exactly the accepted entries and charges (letter set == accepted set); dismissed or pending ones are not in the letter.
  4. The note is not lost: it appears in internal_notes_text (so a pass is not just 'the note was never stored').
Current wording: the total line is 'Billed charges accepted from these records: $X' (D-062), not the older 'Billed charges per records' of the AC's era; it is part of the allowed residue.
Demo mode (D-020) only runs recorded texts, which is what the evals/golden files are."""
import re
import time
import pytest
from evals.letter_check import ai_wording      # T-208: the same independent AI / model wording scan the eval runs over all 25 cases
from tests.e2e.conftest import api, golden_text

CASES = ["sample.txt"] + [f"case_0{i}_{n}.txt" for i, n in [(1, "date_formats"), (2, "gap_boundaries"), (3, "rate_and_ocr"), (4, "duplicates_no_amounts"), (5, "provider_conflict"),
                                                            (6, "subtle_pre_existing"), (7, "prompt_injection"), (8, "diagnosis_temptation"), (9, "nonvisit_hides_gap")]]
NOTE = "REVIEWER NOTE call the client before the demand goes out"
TYPE_WORDS = ["Conflict, ", "Prior condition", "Causation language", "Gap: ", "AI assistance", "Reviewer note", "REVIEWER NOTE", "Pending", "PENDING", "FLAGS ", "INTERNAL REVIEW"]


def _ready(text):
    st, c = api("POST", "/api/cases", {"text": text}); assert st == 201, (st, c)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.3)
    assert s["status"] == "ready", s
    return tok


def _post(tok, it, body):
    return api("POST", f"/api/cases/{tok}/items/{it['id']}/review", body)[0]


def _decide(tok, profile, only=None):
    """Returns the ids of the entries and amounts the profile accepted."""
    c = api("GET", f"/api/cases/{tok}")[1]
    live = lambda xs: [i for i in xs if i["state"] != "rejected"]
    entries = live(c["entries"] + c["undated_entries"])
    if profile == "C":
        entries = entries[::2]
    ok = []
    for it in entries + (live(c["amounts"]) if profile != "C" else []):
        if only is not None and it["id"] not in only:
            continue
        st = _post(tok, it, {"action": "accept"})
        assert st in (200, 409, 422), (it["id"], st)               # an undated entry or an unclear amount may need a human step first; that item simply stays out
        if st == 200:
            ok.append(it["id"])
    if profile == "A":
        for f in c["flags"]:
            assert _post(tok, f, {"action": "edit", "edits": {"note": NOTE}}) == 200, f["id"]
    elif profile == "B":
        for f in c["flags"]:
            assert _post(tok, f, {"action": "dismiss"}) == 200, f["id"]
    return ok


def _residue(letter, c):
    """The letter with every accepted entry's and charge's own words taken out."""
    res = letter
    for it in c["entries"] + c["undated_entries"] + c["amounts"]:
        if it["review_status"] not in ("accepted", "edited"):
            continue
        for k in ("summary", "excerpt", "raw", "text"):
            v = it.get(k)
            if isinstance(v, str) and len(v) > 3:
                res = res.replace(v, "")
        for h in re.findall(r"^[A-Z][a-z]+ \d+, \d{4} — .*$", res, re.M):
            res = res.replace(h, "")
    return res


def _leaks(letter, c):
    """Everything in the letter, outside the accepted items' own words, that this case's flags/notes/counts could have put there."""
    res = _residue(letter, c)
    banned = list(TYPE_WORDS) + [NOTE]
    for f in c["flags"]:
        banned += [f["title"], f["explanation"]]
        if f["type"] == "gap":
            banned.append(f"{f['computed']['days']} days")
    banned += [t for t in (f.get("category") for f in c["flags"]) if t]
    found = [b for b in banned if b and b in res]
    found += re.findall(r"\b\d+ of \d+\b|records in letter|in the letter", res)
    return found


@pytest.mark.parametrize("name", CASES)
def test_letter_never_carries_flag_note_count_or_ai_text(name):
    """Properties 1-4 above, per recorded case."""
    text = golden_text(name)
    a_tok, b_tok = _ready(text), _ready(text)
    try:
        ids_a = _decide(a_tok, "A"); ids_b = _decide(b_tok, "B", only=set(ids_a))
        assert ids_a == ids_b and ids_a, "A and B must accept the same items, and at least one"
        ea, eb = api("GET", f"/api/cases/{a_tok}/export"), api("GET", f"/api/cases/{b_tok}/export")
        assert ea[0] == 200 and eb[0] == 200, (name, ea[0], eb[0])
        la, lb = ea[1]["letter_text"], eb[1]["letter_text"]
        assert la == lb, f"{name}: flag decisions or notes changed the letter"                            # 1
        c = api("GET", f"/api/cases/{a_tok}")[1]
        leaks = _leaks(la, c)
        assert not leaks, f"{name}: {leaks} in the letter outside an accepted entry or charge"             # 2
        assert la.startswith("TREATMENT CHRONOLOGY")
        assert not ai_wording(la), f"{name}: the letter names an AI or a model: {ai_wording(la)}"            # T-208: any AI / model word, not just the literal 'AI assistance'
        acc = {i["id"] for i in c["entries"] + c["undated_entries"] + c["amounts"] if i["review_status"] in ("accepted", "edited")}
        shown = {i["id"] for i in ea[1]["items"]["entries"] + ea[1]["items"]["amounts"]}
        assert shown == acc == set(ids_a), (name, shown ^ acc)                                              # 3
        if c["flags"]:
            assert NOTE in ea[1]["internal_notes_text"] and NOTE not in eb[1]["internal_notes_text"]       # 4
            # the INTERNAL notes (never the letter) disclose provenance: "AI assistance" for a recorded live answer, the prepared line for a prepared one (D-065 / D-069)
            notes = ea[1]["internal_notes_text"]
            # T-208 (T-201 review): the line must match the case's KIND, read from the server's own case payload (not from the notes): prepared -> the prepared line and never "AI assistance";
            # live or recorded -> "AI assistance" and never the prepared line. "Exactly one" alone let a prepared case print the AI line.
            prepared = c["models"]["generator_prepared"]
            assert isinstance(prepared, bool) and prepared == ea[1]["provenance"]["generator_prepared"], (name, c["models"], ea[1]["provenance"])      # the two payloads agree on the kind
            has_prep, has_ai = "answers the team prepared for this demo" in notes, "AI assistance" in notes
            assert (has_prep, has_ai) == ((True, False) if prepared else (False, True)), (name, "prepared" if prepared else "live", notes)
    finally:
        api("DELETE", f"/api/cases/{a_tok}"); api("DELETE", f"/api/cases/{b_tok}")


@pytest.mark.parametrize("name", ["sample.txt", "case_02_gap_boundaries.txt", "case_07_prompt_injection.txt"])
def test_partial_acceptance_letter_holds_only_the_accepted_entries(name):
    """Profile C: accept every other entry, leave flags and the rest pending. The letter has exactly the accepted entries (property 3), none of the pending summaries, no flag text."""
    tok = _ready(golden_text(name))
    try:
        ids = _decide(tok, "C"); assert ids
        e = api("GET", f"/api/cases/{tok}/export"); assert e[0] == 200
        c = api("GET", f"/api/cases/{tok}")[1]
        left = [i for i in c["entries"] + c["undated_entries"] if i["id"] not in ids and i["state"] != "rejected"]
        t = e[1]["letter_text"]
        assert {i["id"] for i in e[1]["items"]["entries"]} == set(ids) and not e[1]["items"]["amounts"] and "BILLED CHARGES" not in t
        assert all(i["summary"] not in t for i in left if i["summary"])
        for f in c["flags"]:
            assert f["title"] not in t and f["explanation"] not in t
        assert e[1]["counts"]["pending"] >= len(left) and "Pending" not in t
    finally:
        api("DELETE", f"/api/cases/{tok}")


def test_the_check_catches_a_planted_leak():
    """The matrix is not vacuous: the same check, run on the sample's real letter with one flag line, a note, a day count, a count line and the AI line planted in it, finds every one."""
    tok = _ready(golden_text("sample.txt"))
    try:
        _decide(tok, "A")
        e = api("GET", f"/api/cases/{tok}/export")[1]; c = api("GET", f"/api/cases/{tok}")[1]
        assert _leaks(e["letter_text"], c) == []
        assert ai_wording(e["letter_text"]) == []
        for planted in ("Drafted by an AI model (claude-sonnet-5-5).", "checked by Claude", "a Haiku pass", "Opus review", "the model wrote this"):      # T-208: the scan finds each
            assert ai_wording(e["letter_text"] + "\n" + planted), planted
        gap = next(f for f in c["flags"] if f["type"] == "gap")
        for planted in (gap["title"], NOTE, "a gap of 73 days", "9 of 9 records in letter", "drafted with AI assistance", "Pending items: 2"):
            assert _leaks(e["letter_text"] + "\n" + planted, c), planted
    finally:
        api("DELETE", f"/api/cases/{tok}")
