"""T-059 (D-031): firm-voice treatment paragraph from ACCEPTED entries only; every sentence code-checked and judged; seeded hallucinations are removed."""
import pytest
from app.backend import export as X, narrative as N, pipeline as PL, review as RV, store
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script


@pytest.fixture(autouse=True)
def _narrative_on(monkeypatch):
    monkeypatch.setenv("NARRATIVE_IN_LETTER", "1")      # D-067: off by default; these tests exercise the flagged-on path (test_d067_narrative_cut.py covers the default)


def accepted_sample(tmp_path, accept=lambda n: True):
    conn = DB.connect(str(tmp_path / "n.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["state"] != "rejected" and accept(int(e["id"][1:])):
            RV.apply_review(conn, cid, e["id"], {"action": "accept"}, call=FakeCall(sample_script()))
    return conn, cid


GOOD = [{"entry_id": "e1", "text": "On January 9, 2026, Austin EMS documented a restrained driver rear-ended at approx. 35 mph who complained of neck pain 7/10 and headache."},
        {"entry_id": "e5", "text": "On February 20, 2026, Capital PT recorded pain 4/10, improving."}]


def narr(sentences, judge="supported"):
    return FakeCall({"narrative": {"sentences": sentences}, "j1": {"verdict": judge, "reason_code": "NONE"}})


def test_good_sentences_kept_with_citations(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    n = N.draft(conn, cid, call=narr(GOOD), now=2.0)
    assert [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"] and not n["removed"] and n["status"] == "pending"
    assert all(s["cite"].startswith("record ") and s["judge"]["verdict"] == "supported" for s in n["sentences"])


def test_only_accepted_entries_are_sent_to_the_model(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: n in (1, 5))
    call = narr(GOOD)
    N.draft(conn, cid, call=call, now=2.0)
    user = call.prompts("narrative")[0]
    assert "ENTRY e1" in user and "ENTRY e5" in user and "ENTRY e2 " not in user and "ENTRY e7" not in user
    for flagword in ("73 days", "gap", "Conflict", "FLAGS"):
        assert flagword.lower() not in user.lower().replace("approx", "")


def test_no_accepted_entries_means_no_call(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: False)
    call = narr(GOOD)
    n = N.draft(conn, cid, call=call, now=2.0)
    assert n["error"] == "NO_ACCEPTED_ENTRIES" and call.steps() == []


E5 = "On February 20, 2026, Capital PT recorded pain 4/10, improving"     # e5 quote: 'Pain 4/10, improving.' (no hedge, no self-report marker)
TOK, QUAL, CAUSE, FLAG, SEV = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "FLAG_CONTENT", "SEVERITY_NOT_QUOTED")


@pytest.mark.parametrize("entry,text,reasons", [
    # D-006: each of number, side, negation and date, on a quote with no hedge so ONLY the token check can fire
    ("e5", E5.replace("4/10", "9/10") + ".", [TOK]),
    ("e5", E5.replace("pain", "left pain") + ".", [TOK]),
    ("e5", E5.replace("pain", "no pain") + ".", [TOK]),
    ("e5", E5.replace("February 20", "March 5") + ".", [TOK]),
    ("e1", "On January 9, 2026, Austin EMS found a herniated disc at C6-C7 and neck pain 9/10.", [TOK, QUAL]),            # invented numbers; also drops C/O
    # each other code check on its own
    ("e5", E5.replace("recorded", "recorded that the collision caused her") + ".", [CAUSE]),
    ("e5", E5 + ", after a gap in care.", [FLAG]),
    ("e8", "On May 29, 2026, Austin Imaging documented a C5-C6 disc protrusion with mild right foraminal narrowing.", [QUAL]),   # drops 'may represent'
    # optional backstop: severity / outcome wording that is not in the quote
    ("e5", E5.replace("recorded", "recorded significant") + ".", [SEV]),
    ("e5", E5.replace("recorded", "recorded severe") + ".", [SEV]),
    ("e5", E5 + ", and recommended surgery.", [SEV]),
    ("e5", E5.replace("pain 4/10, improving", "worsening pain 4/10") + ".", [SEV]),
])
def test_each_code_check_removes_a_seeded_sentence_with_its_own_reason(tmp_path, entry, text, reasons):
    conn, cid = accepted_sample(tmp_path)
    call = narr([{"entry_id": entry, "text": text}])
    n = N.draft(conn, cid, call=call, now=2.0)
    assert not n["sentences"], "judge 1 says supported, so only a code check can have removed it"
    r, = n["removed"]
    assert r["text"] == text and r["reasons"] == reasons and r["reason"] == reasons[0] and r["message"] == N.REASONS[reasons[0]]
    assert "j1" not in call.steps()                                  # rejected before the judge: rung (a) is what caught it


def test_sentence_citing_an_entry_that_is_not_accepted_is_removed(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: n != 8)
    call = narr([{"entry_id": "e8", "text": "On May 29, 2026, Austin Imaging documented a C5-C6 disc protrusion."}, {"entry_id": "e404", "text": "Invented entry."}])
    n = N.draft(conn, cid, call=call, now=2.0)
    assert not n["sentences"] and [(r["entry_id"], r["reason"]) for r in n["removed"]] == [("e8", "NOT_AN_ACCEPTED_ENTRY"), ("e404", "NOT_AN_ACCEPTED_ENTRY")]
    assert "j1" not in call.steps()


def test_quoted_severity_and_recommendation_words_are_allowed(tmp_path):
    conn, cid = accepted_sample(tmp_path)           # e9 quote: 'Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.'
    s = {"entry_id": "e9", "text": "On June 12, 2026, Hill Country Pain Management recommended cervical epidural steroid injection; the patient states symptoms began after the January collision."}
    n = N.draft(conn, cid, call=narr([s]), now=2.0)
    assert len(n["sentences"]) == 1 and not n["removed"]


@pytest.mark.parametrize("verdict,reason", [("partially", "JUDGE_PARTIAL"), ("unsupported", "JUDGE_UNSUPPORTED"), ("unavailable", "JUDGE_UNAVAILABLE")])
def test_judge_one_removes_unsupported_sentences(tmp_path, verdict, reason):
    conn, cid = accepted_sample(tmp_path)
    call = narr(GOOD, judge="agrees" if verdict == "unavailable" else verdict)        # an invalid verdict = judge did not answer
    n = N.draft(conn, cid, call=call, now=2.0)
    assert not n["sentences"] and {r["reason"] for r in n["removed"]} == {reason}


def test_quoted_causation_is_allowed(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    s = {"entry_id": "e9", "text": "On June 12, 2026, Hill Country Pain Management recorded that the patient states symptoms began after the January collision."}
    n = N.draft(conn, cid, call=narr([s]), now=2.0)
    assert len(n["sentences"]) == 1 and not n["removed"]


# ---- export wiring: internal until accepted
def test_internal_notes_until_accepted_then_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert "DRAFT TREATMENT PARAGRAPH" in ex["internal_notes_text"] and "Not in the letter until you accept it" in ex["internal_notes_text"]
    assert "TREATMENT SUMMARY" not in ex["letter_text"] and GOOD[0]["text"] not in ex["letter_text"]
    N.review(conn, cid, "accept", now=3.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert "TREATMENT SUMMARY" in ex["letter_text"] and f"{GOOD[1]['text']} (Capital PT, visit 8, February 20, 2026)" in ex["letter_text"]


def test_dismissed_and_stale_sentences_stay_out_of_the_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "dismiss", now=3.0)
    assert "TREATMENT SUMMARY" not in X.build_export(store.export_case(conn, cid))["letter_text"]
    N.review(conn, cid, "accept", now=4.0)
    RV.apply_review(conn, cid, "e5", {"action": "dismiss"})                      # the cited entry leaves the letter
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[1]["text"] not in ex["letter_text"] and GOOD[0]["text"] in ex["letter_text"]


def test_export_without_a_narrative_is_unchanged():
    from tests.unit.test_export import build_case
    out = X.build_export(build_case())
    assert "DRAFT TREATMENT" not in out["internal_notes_text"] and "TREATMENT SUMMARY" not in out["letter_text"]


# ---- recorded fixtures (claude-cli, sample case): replay through audited; python /private/tmp/.../rec_narr.py --record regenerates them
def test_recorded_sample_paragraph_replays_with_every_sentence_supported(tmp_path, monkeypatch):
    import pathlib
    from app.llm import audited as AU
    root = pathlib.Path(__file__).resolve().parents[2]
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    conn = DB.connect(str(tmp_path / "r.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=AU.make_call(conn, cid), now=lambda: 1.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["state"] != "rejected":
            RV.apply_review(conn, cid, e["id"], {"action": "accept"})      # T-139: e2/e4 are narrowed (their charge sentence is dropped by code), so all nine can be accepted; the paragraph is recorded over them
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(root / "tests" / "fixtures" / "llm" / "narrative"))
    n = N.draft(conn, cid, call=AU.make_call(conn, cid), now=2.0)
    assert not n.get("error") and len(n["sentences"]) >= 6 and not n["removed"]
    assert all(s["judge"]["verdict"] == "supported" and s["cite"] for s in n["sentences"])
    text = " ".join(s["text"] for s in n["sentences"]).lower()
    assert "73 days" not in text and " gap" not in text and "conflict" not in text
    steps = [c["step"] for c in DB.list_llm_calls(conn, cid) if c["step"] in ("narrative", "j1")]
    assert steps.count("narrative") == 1 and steps.count("j1") >= len(n["sentences"])      # the ladder record has every call


# ---- T-059 review F2: an entry edited after the draft drops its sentence (basis hash), the others stay
def test_entry_edited_after_the_draft_drops_its_sentence_from_the_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[0]["text"] in ex["letter_text"] and GOOD[1]["text"] in ex["letter_text"]           # control: both in before the edit
    RV.apply_review(conn, cid, "e5", {"action": "edit", "edits": {"summary": "Pain rated 4/10, improving."}}, call=FakeCall(sample_script()))
    assert [e for e in DB.list_items(conn, cid, "entry") if e["id"] == "e5"][0]["review_status"] == "edited"      # still in the letter as an entry
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[1]["text"] not in ex["letter_text"] and GOOD[0]["text"] in ex["letter_text"]
    tag = "[NOT in the letter: the cited entry changed or is no longer accepted]"
    notes = ex["internal_notes_text"]
    assert f'- {GOOD[1]["text"]} (' in notes and tag in notes.split(GOOD[1]["text"])[1].split("\n")[0]
    assert tag not in notes.split(GOOD[0]["text"])[1].split("\n")[0]                                   # the unchanged sentence carries no tag


# ---- T-059 review F4: a failed re-draft must not overwrite the paragraph the paralegal already has
class Boom(Exception):
    pass


def failing_calls():
    from app.llm import audited as AU, provider as P
    return [("llm_failed", FakeCall({"narrative": AU.LLMFailed("down")})), ("fixture_miss", FakeCall({"narrative": P.FixtureMiss("none")})),
            ("schema", FakeCall({"narrative": {"sentences": "not a list"}})), ("type", FakeCall({"narrative": None}))]


@pytest.mark.parametrize("which", range(4))
def test_failed_redraft_keeps_the_accepted_paragraph(tmp_path, which):
    name, bad = failing_calls()[which]
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    before = N.get(conn, cid)
    out = N.draft(conn, cid, call=bad, now=4.0)
    assert out["error"] == "LLM_FAILED_AFTER_RETRIES", name                       # the failure is reported alongside ...
    assert out["status"] == "accepted" and [s["entry_id"] for s in out["sentences"]] == ["e1", "e5"]
    assert N.get(conn, cid) == before and "error" not in N.get(conn, cid)         # ... and nothing stored changed
    assert GOOD[1]["text"] in X.build_export(store.export_case(conn, cid))["letter_text"]


def test_failed_first_draft_stores_the_error_and_a_later_draft_replaces_it(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    assert N.draft(conn, cid, call=failing_calls()[0][1], now=2.0)["error"] == "LLM_FAILED_AFTER_RETRIES"
    assert N.get(conn, cid)["error"] == "LLM_FAILED_AFTER_RETRIES" and N.get(conn, cid)["sentences"] == []
    ok = N.draft(conn, cid, call=narr(GOOD), now=3.0)
    assert "error" not in ok and len(ok["sentences"]) == 2


def test_no_accepted_entries_does_not_wipe_an_existing_paragraph(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["review_status"] == "accepted":
            RV.apply_review(conn, cid, e["id"], {"action": "dismiss"})
    out = N.draft(conn, cid, call=narr(GOOD), now=4.0)
    assert out["error"] == "NO_ACCEPTED_ENTRIES" and out["status"] == "accepted" and len(out["sentences"]) == 2
    assert "error" not in N.get(conn, cid)


def test_successful_redraft_replaces_the_paragraph_as_pending(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    n = N.draft(conn, cid, call=narr(GOOD[:1]), now=4.0)
    assert n["status"] == "pending" and [s["entry_id"] for s in n["sentences"]] == ["e1"]


# ---- T-059 review F4: review() and the routes
def test_review_before_a_draft_and_bad_actions(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    with pytest.raises(KeyError):
        N.review(conn, cid, "accept")
    N.draft(conn, cid, call=narr([{"entry_id": "e1", "text": "Invented sentence with 99/99."}]), now=2.0)     # every sentence removed
    with pytest.raises(ValueError):
        N.review(conn, cid, "accept")                                           # nothing to accept
    with pytest.raises(ValueError):
        N.review(conn, cid, "publish")


@pytest.fixture
def client(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    return TestClient(create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path)))


def test_narrative_routes_before_any_draft(client):
    tok = client.post("/api/cases", json={"sample": True}).json()["token"]
    base = f"/api/cases/{tok}/narrative"
    assert client.get(base).status_code == 200 and client.get(base).json() == {"narrative": None}
    assert client.get("/api/cases/nope/narrative").status_code == 404
    r = client.post(base, json={})                                              # nothing accepted yet: no model call
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_request"
    r = client.post(base + "/review", json={"action": "accept"})
    assert r.status_code == 404 and r.json()["error"]["code"] == "not_found"
    assert client.get(base).json() == {"narrative": None}                       # the refused POST stored nothing


def test_narrative_review_route_refuses_a_bad_action_and_an_empty_accept(client, tmp_path):
    tok = client.post("/api/cases", json={"sample": True}).json()["token"]
    conn = DB.connect(str(tmp_path / "x.sqlite"))
    DB.update_case(conn, tok, config_json={"narrative": {"status": "pending", "sentences": [], "removed": []}})
    conn.commit(); conn.close()
    for body in ({"action": "publish"}, {"action": "accept"}, {}):
        r = client.post(f"/api/cases/{tok}/narrative/review", json=body)
        assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_edit", body
    assert client.post(f"/api/cases/{tok}/narrative/review", json={"action": "dismiss"}).json()["narrative"]["status"] == "dismissed"


# ---- T-106 (T-098 r3 F1): a sentence that cites an entry that is not accepted was never code-checked; the notes do not print its wording
def test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    bad = {"entry_id": "e99", "text": "Pain was 9/10 on the left side."}
    n = N.draft(conn, cid, call=narr(GOOD + [bad]), now=2.0)
    assert [r["reason"] for r in n["removed"]] == ["NOT_AN_ACCEPTED_ENTRY"] and [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"]
    for accept in (False, True):
        if accept:
            N.review(conn, cid, "accept", now=3.0)
        ex = X.build_export(store.export_case(conn, cid))
        notes = ex["internal_notes_text"]
        assert "9/10 on the left" not in notes and "left side" not in notes and "9/10 on the left" not in ex["letter_text"]
        assert "Sentence removed (cites an entry that is not accepted) (e99)." in notes and "NOT_AN_ACCEPTED_ENTRY" not in notes      # T-167: no code in the notes
        assert GOOD[0]["text"] in notes                                                  # control: the checked sentences still print
