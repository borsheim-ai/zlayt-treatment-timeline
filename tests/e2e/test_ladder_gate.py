"""Validation ladder gate. R-CO-2, R-TL-4, R-RV-6, CONTRACT 5.2 (nothing LLM-made reaches the export without all three rungs)."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_unreviewed_items_absent_from_export(sample_case):
    """R-CO-2 + D-045: with nothing accepted the export is refused (422 export_blocked, NOTHING_ACCEPTED); once one item is accepted, only that item is in the letter
    and the pending ones stay out (they are a warning, not a blocker)."""
    st, body = api("GET", f"/api/cases/{sample_case}/export")
    assert st == 422 and body["error"]["code"] == "export_blocked"
    assert [b["reason_code"] for b in body["error"]["detail"]["blockers"]] == ["NOTHING_ACCEPTED"]
    c = api("GET", f"/api/cases/{sample_case}")[1]
    live = [e for e in c["entries"] if e["state"] != "rejected"]
    assert api("POST", f"/api/cases/{sample_case}/items/{live[0]['id']}/review", {"action": "accept"})[0] == 200
    e = api("GET", f"/api/cases/{sample_case}/export")
    assert e[0] == 200
    assert live[0]["summary"] in e[1]["letter_text"]
    assert all(x["summary"] not in e[1]["letter_text"] for x in live[1:] if x["summary"] != live[0]["summary"])
    assert e[1]["counts"]["pending"] > 0


def test_audit_has_call_per_llm_item(sample_case):
    """R-CO-2 / ADR-006: GET /audit lists the model calls (generator + judge) with prompt hash, and no human events yet."""
    a = api("GET", f"/api/cases/{sample_case}/audit")[1]
    assert len(a["calls"]) >= 30 and not a["events"]

def test_ladder_present_on_every_entry(sample_case):
    """R-CO-2: each entry carries its ladder (generator call_id, judge verdict, code checks)."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    assert all(e["ladder"] and e["ladder"].get("judge") for e in c["entries"])

def test_rejected_attempt_visible_but_not_exportable(sample_case, pw):
    """ADR-005 / T-045 r2: an item the ladder rejected (could not verify) cannot be accepted or edited (409 item_rejected, nothing changes), is shown in the Could-not-verify tray without
    an Accept button, and never reaches the letter. The fixture run has none, so one entry is put into the rejected state through the server's own SQLite file (needs_db, like test_edit_to_check;
    with E2E_REQUIRE_DB=1 a missing file fails, it does not skip). Dismiss and reset still work on it."""
    from tests.e2e.conftest import needs_db
    from app.db import db as DB
    c = api("GET", f"/api/cases/{sample_case}")[1]
    rej, ok = c["entries"][0], c["entries"][1]
    conn = DB.connect(needs_db())
    try:
        DB.update_item(conn, rej["id"], now=9e9, case=sample_case, state="rejected")
    finally:
        conn.close()
    url = f"/api/cases/{sample_case}/items/{rej['id']}/review"
    for body in ({"action": "accept"}, {"action": "edit", "edits": {"summary": "Visit completed."}}):
        st, err = api("POST", url, body)
        assert st == 409 and err["error"]["code"] == "item_rejected", (body, st, err)
    after = api("GET", f"/api/cases/{sample_case}")[1]
    assert any(i["id"] == rej["id"] for i in after["tray"]) and not any(i["review_status"] != "pending" for i in after["entries"] + after["undated_entries"] + after["amounts"] + after["flags"])
    assert api("POST", f"/api/cases/{sample_case}/items/{ok['id']}/review", {"action": "accept"})[0] == 200
    letter = api("GET", f"/api/cases/{sample_case}/export")[1]["letter_text"]
    assert ok["summary"] in letter and rej["summary"] not in letter
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
        from tests.e2e.conftest import open_case
        open_case(pg, sample_case)
        item = pg.locator(f'[data-testid=tray-item][data-item-id="{rej["id"]}"]'); item.wait_for(timeout=15000)
        assert item.get_by_test_id("btn-accept").count() == 0
    finally:
        b.close()
    assert api("POST", url, {"action": "dismiss"})[0] == 200 and api("POST", url, {"action": "reset"})[0] == 200

def test_all_judge_verdicts_recorded_with_backend(sample_case):
    """R-TL-4 / ADR-004: the ladder names the backend ('fixture') and recorded_from for replays."""
    e = api("GET", f"/api/cases/{sample_case}")[1]["entries"][0]
    assert e["ladder"]["backend"] == "fixture" and e["ladder"]["generator"]["call_id"]


# ---- T-045 AC5 (R-CO-2): an LLM item nobody has acted on is in neither block
PENDING = "PENDING ITEMS NOT INCLUDED"


def _sections(notes):
    """internal_notes_text -> {HEADING: body}. A heading is an all-capitals line (it may carry a bracket of guidance after it)."""
    out, cur = {}, None
    for ln in notes.split("\n"):
        m = re.match(r"^([A-Z][A-Z ,/'-]{5,})(?: \(.*\))?$", ln)
        if m and not ln.startswith("- "):
            cur = m.group(1).strip(); out[cur] = []
        elif cur:
            out[cur].append(ln)
    return {k: "\n".join(v) for k, v in out.items()}


def test_llm_item_with_no_human_action_is_absent_from_the_letter_and_from_every_accepted_part_of_the_notes(sample_case):
    """R-CO-2 / spec s.6: accept entry 1 and the gap flag only. Every other entry (LLM draft) and every flag whose origin includes the LLM stays pending: its words are not in the letter
    and not in any notes section that reports what the paralegal accepted or quoted (FLAGS ACCEPTED/DISMISSED, FLAGGED LANGUAGE QUOTED IN THE LETTER, EDITED ITEMS).
    Where the AC says 'absent from both blocks': the notes block has ONE place that names undecided items, 'PENDING ITEMS NOT INCLUDED' (spec s.6, D-045: pending is a warning, not
    a blocker), which says in its title that they are not included. That is the current rule and what is tested; the pending items must be there, so the reader is told.
    Then a human action moves each: accept -> letter, dismiss -> out of the letter and listed as dismissed in the notes."""
    tok = sample_case
    c = api("GET", f"/api/cases/{tok}")[1]
    e1 = c["entries"][0]; gap = next(f for f in c["flags"] if f["type"] == "gap")
    assert api("POST", f"/api/cases/{tok}/items/{e1['id']}/review", {"action": "accept"})[0] == 200
    assert api("POST", f"/api/cases/{tok}/items/{gap['id']}/review", {"action": "accept"})[0] == 200
    ex = api("GET", f"/api/cases/{tok}/export")[1]
    letter, sec = ex["letter_text"], _sections(ex["internal_notes_text"])
    assert PENDING in sec and "FLAGS ACCEPTED" in sec
    llm_entries = [e for e in c["entries"][1:] if e["state"] != "rejected"]
    llm_flags = [f for f in c["flags"] if "llm" in (f.get("origin") or "") and f["id"] != gap["id"]]
    assert len(llm_entries) == 8 and len(llm_flags) >= 5
    accepted_parts = {k: v for k, v in sec.items() if k != PENDING}
    for e in llm_entries:
        assert e["summary"] not in letter, e["id"]
        assert not [k for k, v in accepted_parts.items() if e["summary"] in v], e["id"]
        assert e["summary"] in sec[PENDING], f"{e['id']} is pending and must be named under {PENDING}"
    for f in llm_flags:
        label = {"pre_existing": "Prior condition", "causation": "Causation language", "conflict": "Conflict"}[f["type"]]
        line = next(ln for ln in sec[PENDING].split("\n") if ln.startswith("- Flag, " + label) and any(ev["excerpt"][:30] in ln for ev in f["evidence"]))
        assert line and not [k for k in ("FLAGS ACCEPTED", "FLAGS DISMISSED", "EDITED ITEMS") if label in sec.get(k, "") and line[2:] in sec.get(k, "")], f["id"]
    assert "Gap: 73 days" in sec["FLAGS ACCEPTED"] and "Gap: 73 days" not in sec[PENDING]                    # the one flag a human accepted is where it belongs
    assert [i["id"] for i in ex["items"]["entries"]] == [e1["id"]] and not ex["items"]["amounts"]            # export.items is the accepted set, nothing else
    # a human action moves the item
    a, d = llm_entries[0], llm_entries[1]
    assert api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"})[0] == 200
    assert api("POST", f"/api/cases/{tok}/items/{d['id']}/review", {"action": "dismiss"})[0] == 200
    ex2 = api("GET", f"/api/cases/{tok}/export")[1]; s2 = _sections(ex2["internal_notes_text"])
    assert a["summary"] in ex2["letter_text"] and a["summary"] not in s2[PENDING]
    assert d["summary"] not in ex2["letter_text"] and d["summary"] not in s2[PENDING] and "dismissed" in s2["RECORDS NOT IN THE TREATMENT SECTION"]


def test_edited_llm_item_keeps_the_humans_words_and_is_labeled_in_the_notes(sample_case):
    """R-CO-2 + 'edits labeled' (ship bar 5): the paralegal edits an LLM draft (the new wording still passes the code check) and then accepts it; the letter carries her words, not the draft's, and the
    notes list the item under EDITED ITEMS with both texts."""
    tok = sample_case
    e = api("GET", f"/api/cases/{tok}")[1]["entries"][2]
    new = "Persistent neck pain 6/10 with daily headaches noted."
    st, body = api("POST", f"/api/cases/{tok}/items/{e['id']}/review", {"action": "edit", "edits": {"summary": new}})
    assert st == 200, body
    assert api("GET", f"/api/cases/{tok}/export")[0] == 422                     # an edit alone is not a decision to send it (D-045: 'nothing is accepted or edited yet' until she confirms)
    st, body = api("POST", f"/api/cases/{tok}/items/{e['id']}/review", {"action": "accept"})
    assert st == 200, body
    ex = api("GET", f"/api/cases/{tok}/export")
    assert ex[0] == 200, ex[1]
    assert new in ex[1]["letter_text"] and e["summary"] not in ex[1]["letter_text"]
    sec = _sections(ex[1]["internal_notes_text"])
    assert new in sec["EDITED ITEMS"] and e["summary"] in sec["EDITED ITEMS"]
