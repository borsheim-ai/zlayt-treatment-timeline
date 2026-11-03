"""T-146 round 3: ONE rule for every stage. A re-run never lowers or replaces a decided item (accepted, dismissed, edited), whatever fails or whatever the new run's
checks say. When the new output for a decided item differs from it or fails a check, the decided item is kept whole, carries a visible note, and the case reads
run_partial with an honest message (the exact text is pinned here). Paths: flag step down, summary-in-quote fails on the new extract, extract down, judge down,
the deadline, and a re-run with nothing to keep."""
import json

import pytest
from app.backend import pipeline as PL, present
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

TAIL = " Run it again to retry."
DECIDED = ("e1", "e2", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7")


def down(step):
    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")


def model_flag(user):
    """A model flag for record 3 with the same quote as the lexicon flag f_r3_1: the two corroborate (origin lexicon+llm, verified)."""
    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")] if which_record(user)[0] == 3 else []}


def _no_calls(v):
    return {a: _no_calls(b) for a, b in v.items() if a not in ("call_id", "rerun_note")} if isinstance(v, dict) else v


def full(conn, cid):
    """Every stored column of every item, but not `ladder.rerun_note` (checked on its own) and not call ids (every re-run numbers its calls afresh; they are compared on
    the kept e1 in test_kept_rows_keep_their_original_call_ids)."""
    return {k: {i["id"]: {c: _no_calls(v) for c, v in i.items() if c != "updated_at"} for i in DB.list_items(conn, cid, k)} for k in ("entry", "amount", "flag")}


def completed(tmp_path, decide=True):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    assert PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 1.0)["status"] == "done"
    assert DB.get_item(conn, "f_r3_1")["origin"] == "lexicon+llm" and DB.get_item(conn, "f_r3_1")["state"] == "verified"
    if decide:
        for i in ("e1", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7"):      # a corroborated flag, a lexicon-only flag, a code flag, an entry, an amount
            DB.apply_review(conn, i, "accept", now=2.0, case=cid)
        DB.apply_review(conn, "e2", "dismiss", now=2.0, case=cid)
    return conn, cid


def rerun(conn, cid, **script):
    script.setdefault("flags", model_flag)
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)


def case_error(conn, cid):
    c = DB.get_case(conn, cid)
    return c["status"], (json.loads(c["error"]) if c["error"] else None)


def note(conn, cid, i):
    return (DB.get_item(conn, i, cid)["ladder"] or {}).get("rerun_note")


def assert_notes(conn, cid, ids, kind, step):
    for i in ids:
        n = note(conn, cid, i)
        assert n and n["kind"] == kind and n["step"] == step, (i, n)
        assert present.item_view(conn, cid, i)["rerun_note"] == n["message"]      # shown on the item, not only stored
    for i in set(DECIDED) - set(ids):
        assert note(conn, cid, i) is None, i


# ---- the flag step is down
def test_flag_step_down_keeps_every_decided_flag_whole_and_notes_it(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid, flags=down("flags"))
    assert out["status"] == "done"
    assert full(conn, cid) == before                      # 10 flags: origin, state, reasons and judge answer all as stored
    f = DB.get_item(conn, "f_r3_1", cid)
    assert (f["state"], f["origin"], f["state_reasons"], f["review_status"]) == ("verified", "lexicon+llm", [], "accepted")
    assert f["ladder"]["judge"]["verdict"] == "agree"
    assert DB.get_item(conn, "f_r6_1", cid)["state_reasons"] == ["LEXICON_ONLY"]            # an accepted lexicon-only flag is not rewritten to LLM_FAILED either
    status, err = case_error(conn, cid)
    assert status == "failed" and err == out["error"]
    assert err == {"code": "run_partial", "message": "The AI step failed for 7 items (finding the flags) on this run. Their earlier results and every decision of yours "
                                                      "were kept unchanged." + TAIL}
    assert_notes(conn, cid, ("f_r3_1", "f_r6_1"), "failed", "finding the flags")      # only the decided ones carry a note
    assert "could not redo" in note(conn, cid, "f_r3_1")["message"] and "kept" in note(conn, cid, "f_r3_1")["message"]


# ---- the summary-in-quote check fails on the new extract
def _bad_summary(user):
    good = sample_script()["extract"](user)
    return dict(summary="Patient had a skull fracture of 99 cm.", excerpt=good["excerpt"]) if which_record(user)[0] == 1 else good


def test_summary_check_failing_on_the_new_extract_keeps_the_decided_entry(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid, extract=_bad_summary)
    assert out["status"] == "done"
    assert full(conn, cid) == before                       # e1 keeps its summary, quote, offsets, ladder, state and accepted status
    e1 = DB.get_item(conn, "e1", cid)
    assert e1["summary"] and e1["excerpt"] and e1["state"] == "verified" and e1["review_status"] == "accepted"
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_partial", "message": "The re-run gave a different result for 1 item you had already decided; your decision and the earlier result were kept, "
                                                      "and each item carries a note." + TAIL}
    assert_notes(conn, cid, ("e1",), "disagreed", "a different result")
    assert "different result" in note(conn, cid, "e1")["message"] and "not applied" in note(conn, cid, "e1")["message"]
    assert present.review_view(conn, cid)["counts"]["accepted"] >= 1


def test_the_same_failure_on_an_undecided_entry_stands_as_the_new_check_result(tmp_path):
    """Scope of the rule: a pending entry is not a decision. The new run's failed check puts it in the tray (D-054), as before."""
    conn, cid = completed(tmp_path, decide=False)
    rerun(conn, cid, extract=_bad_summary)
    e1 = DB.get_item(conn, "e1", cid)
    assert e1["state"] == "rejected" and e1["state_reasons"] == ["SUMMARY_NOT_IN_QUOTE"] and e1["review_status"] == "pending"
    assert case_error(conn, cid)[1] is None


# ---- the extract step is down
def test_extract_down_keeps_decided_entries_and_notes_them(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid, extract=down("extract"))
    assert out["status"] == "done_with_errors"
    assert full(conn, cid) == before
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours "
                                                      "were kept unchanged." + TAIL}
    assert_notes(conn, cid, ("e1", "e2", "e3"), "failed", "writing the entries")


@pytest.mark.parametrize("cause", ["llm_failed", "fixture_miss", "schema_invalid"])
def test_each_kind_of_extract_failure_for_one_record_keeps_that_row(tmp_path, cause):
    """All three stub reasons (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, SCHEMA_INVALID), for a decided and for an undecided entry."""
    for decide in (True, False):
        sub = tmp_path / str(decide)
        sub.mkdir()
        conn, cid = completed(sub, decide)
        before = full(conn, cid)
        good = sample_script()["extract"]

        def extract(user, good=good):
            if which_record(user)[0] != 1:
                return good(user)
            if cause == "llm_failed":
                raise down("extract")
            if cause == "fixture_miss":
                raise PL.P.FixtureMiss("no recorded answer")
            return {"nonsense": True}
        rerun(conn, cid, extract=extract)
        assert full(conn, cid) == before, (cause, decide)
        status, err = case_error(conn, cid)
        assert status == "failed" and err["message"] == ("The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours "
                                                         "were kept unchanged." + TAIL)
        assert (note(conn, cid, "e1") is not None) is decide


# ---- the judge is down
def test_judge_down_keeps_decided_items_and_notes_them(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid, j1=down("j1"), j2=down("j2"), j3=down("j3"), j4=down("j4"))
    assert out["status"] == "done"
    assert full(conn, cid) == before
    assert {DB.get_item(conn, i, cid)["ladder"]["judge"]["verdict"] for i in ("e1", "e2", "e3")} == {"supported"}      # the stored answers, not 'unavailable'
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err["code"] == "run_partial" and err["message"] == ("The AI step failed for 14 items (the second check) on this run. Their earlier results and every decision of "
                                                              "yours were kept unchanged." + TAIL)
    assert_notes(conn, cid, ("e1", "e2", "e3", "a1", "f_r3_1"), "failed", "the second check")
    assert "second check" in note(conn, cid, "e1")["message"]


def test_one_judge_down_names_only_its_items(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    rerun(conn, cid, j1=down("j1"))
    assert full(conn, cid) == before
    assert case_error(conn, cid)[1]["message"] == ("The AI step failed for 9 items (the second check) on this run. Their earlier results and every decision of yours "
                                                    "were kept unchanged." + TAIL)
    assert_notes(conn, cid, ("e1", "e2", "e3"), "failed", "the second check")


# ---- the deadline is hit
@pytest.mark.parametrize("jump_at", ["extract", "judge_entries", "flags"])
def test_deadline_keeps_decided_items_without_a_disagreement_note(tmp_path, jump_at):
    """A stopped run did not redo anything, so it has nothing to disagree with: rows are byte-identical (no note) and the case says so with run_deadline."""
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == jump_at:
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    assert full(conn, cid) == before
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    assert_notes(conn, cid, (), "failed", "")


# ---- a re-run with nothing to keep
def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 1.0)
    assert first["status"] == "done_with_errors" and case_error(conn, cid)[0] == "failed"      # T-161 r2: a first run with no entries at all is failed too (steps named)
    again = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 2.0)
    assert again["status"] == "done_with_errors"
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_partial", "records": list(range(1, 10)), "extract_only": True,      # T-165: the records are named
                   "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL}


def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
    conn, cid = completed(tmp_path)
    good = sample_script()["extract"]
    DB.update_item(conn, "e4", now=2.0, case=cid, summary=None, excerpt=None, state="rejected", state_reasons_json=["LLM_FAILED_AFTER_RETRIES"])      # a stub left by an earlier failure

    def extract(user):
        if which_record(user)[0] in (1, 4):
            raise down("extract")
        return good(user)
    rerun(conn, cid, extract=extract)
    _, err = case_error(conn, cid)
    assert err["message"] == ("The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
                              "The AI step also failed for 1 item (writing the entries) with no earlier result to keep. No entry was made for record 4." + TAIL)      # T-165: the record is named


# ---- a later good run clears the notes and the error
def test_a_later_good_rerun_clears_the_note_and_keeps_the_decision(tmp_path):
    conn, cid = completed(tmp_path)
    rerun(conn, cid, extract=down("extract"))
    assert note(conn, cid, "e1")
    out = rerun(conn, cid)
    assert out["status"] == "done"
    assert case_error(conn, cid) == ("ready", None)
    assert note(conn, cid, "e1") is None and DB.get_item(conn, "e1", cid)["review_status"] == "accepted"
    assert present.item_view(conn, cid, "e1")["rerun_note"] is None


def test_a_clean_rerun_of_a_decided_item_is_not_a_disagreement(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid)
    assert out["status"] == "done" and case_error(conn, cid) == ("ready", None)
    assert full(conn, cid) == before
    assert DB.get_item(conn, "e1", cid)["summary"] == before["entry"]["e1"]["summary"] and DB.get_item(conn, "e1", cid)["review_status"] == "accepted"
    assert_notes(conn, cid, (), "failed", "")


# ---- the rule's edges, one per branch of the compare
def test_a_decided_flag_the_model_no_longer_proposes_is_kept_with_its_higher_state(tmp_path):
    """f_r3_1 was verified because the model agreed. If the model's re-run does not propose it, the new row is lexicon-only (needs_review): lower, so the stored row stays."""
    conn, cid = completed(tmp_path)
    rerun(conn, cid, flags={"flags": []})
    f = DB.get_item(conn, "f_r3_1", cid)
    assert f["state"] == "verified" and f["origin"] == "lexicon+llm" and f["review_status"] == "accepted"
    assert_notes(conn, cid, ("f_r3_1",), "disagreed", "a different result")


def test_a_better_state_with_the_same_content_is_not_a_disagreement(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(j1=down("j1"))), now=lambda: 1.0)      # e1 needs_review: second check failed
    assert DB.get_item(conn, "e1", cid)["state"] == "needs_review"
    DB.apply_review(conn, "e1", "accept", now=2.0, case=cid)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 3.0)
    e1 = DB.get_item(conn, "e1", cid)
    assert e1["state"] == "verified" and e1["review_status"] == "accepted" and note(conn, cid, "e1") is None
    assert case_error(conn, cid) == ("ready", None)


def test_kept_rows_keep_their_original_call_ids(tmp_path):
    """The audit trail of a kept row points at the calls that made what is shown, not at the failed re-run's calls."""
    conn, cid = completed(tmp_path)
    before = DB.get_item(conn, "e1", cid)["ladder"]
    rerun(conn, cid, extract=down("extract"))
    after = DB.get_item(conn, "e1", cid)["ladder"]
    assert after["generator"]["call_id"] == before["generator"]["call_id"] and after["judge"]["call_id"] == before["judge"]["call_id"]


# ---- flag step failing by a missing recorded answer is the same as it failing
def test_flag_step_fixture_miss_is_a_failure_too(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    rerun(conn, cid, flags=PL.P.FixtureMiss("no recorded answer"))
    assert full(conn, cid) == before
    assert case_error(conn, cid)[1]["message"].startswith("The AI step failed for 7 items (finding the flags) on this run.")
    assert_notes(conn, cid, ("f_r3_1", "f_r6_1"), "failed", "finding the flags")


@pytest.mark.parametrize("miss", [False, True])
def test_a_pending_model_only_flag_survives_a_down_flag_step(tmp_path, miss):
    """The flag step cannot tell which stored flags are stale when it is down: nothing pending is deleted (a model-only flag has no new row to compare)."""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)

    def only_model(user):
        return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="CT head negative.")] if which_record(user)[0] == 2 else []}
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=only_model)), now=lambda: 1.0)
    assert DB.get_item(conn, "f_r2_1", cid)["origin"] == "llm"
    before = full(conn, cid)["flag"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=PL.P.FixtureMiss("x") if miss else down("flags"))), now=lambda: 3.0)
    assert full(conn, cid)["flag"]["f_r2_1"] == before["f_r2_1"]
    assert "finding the flags" in case_error(conn, cid)[1]["message"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 4.0)      # a good run that no longer finds it removes the pending stale flag
    assert "f_r2_1" not in {f["id"] for f in DB.list_items(conn, cid, "flag")}


# ---- the compare itself, branch by branch
OLD_ENTRY = {"summary": "S", "excerpt": "Q", "date_iso": "2026-01-01", "state": "verified"}
OLD_AMOUNT = {"text": "$10", "value_cents": 1000, "kind": "charge", "state": "verified"}
OLD_FLAG = {"type": "pre_existing", "category": "pre_existing", "evidence": [{"text": "Q"}], "computed": {"from_date": None, "to_date": None, "days": None}, "state": "verified"}
NEW_FLAG = {"type": "pre_existing", "category": "pre_existing", "evidence": [{"text": "Q"}], "from_date": None, "to_date": None, "days": None, "state": "verified"}


@pytest.mark.parametrize("kind,old,new,expected", [
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "needs_review"}, True),            # lower state
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "rejected"}, True),
    ("entry", {**OLD_ENTRY, "state": "needs_review"}, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),      # a better state is not a disagreement
    ("entry", OLD_ENTRY, {"summary": "S2", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, True),               # each content field alone
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q2", "date": "2026-01-01", "state": "verified"}, True),
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-02", "state": "verified"}, True),
    ("entry", {**OLD_ENTRY, "state": "rejected", "summary": None}, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),   # a stub has nothing to lower
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "charge", "state": "verified"}, False),
    ("amount", OLD_AMOUNT, {"text": "$11", "cents": 1000, "cls": "charge", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1100, "cls": "charge", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "estimate", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "charge", "state": "needs_review"}, True),
    ("flag", OLD_FLAG, NEW_FLAG, False),
    ("flag", OLD_FLAG, {**NEW_FLAG, "type": "causation"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "category": "x"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "evidence": [{"text": "Q2"}]}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "state": "needs_review"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "days": 40, "type": "causation"}, False),       # computed numbers moved: the existing reset path decides, not this compare
])
def test_disagrees_table(kind, old, new, expected):
    assert PL._disagrees(kind, old, new) is expected


@pytest.mark.parametrize("kind,old,new,expected", [
    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, "writing the entries"),
    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["FIXTURE_MISS"]}, "writing the entries"),
    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["SCHEMA_INVALID"]}, "writing the entries"),
    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["SUMMARY_NOT_IN_QUOTE"]}, None),            # the model answered; undecided entries take the new check result
    ("entry", {"summary": None, "excerpt": None}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),      # nothing stored to keep
    ("entry", {"summary": "S", "excerpt": None}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),
    ("flag", {"state_reasons": ["LEXICON_ONLY"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, "finding the flags"),
    ("flag", {"state_reasons": ["LEXICON_ONLY"]}, {"reasons": ["FIXTURE_MISS"]}, "finding the flags"),
    ("flag", {"state_reasons": ["LLM_FAILED_AFTER_RETRIES"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),               # already a failure: nothing better stored
    ("flag", {"state_reasons": ["FIXTURE_MISS"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),
    ("amount", {"ladder": {"judge": {"verdict": "agree"}}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, "the second check"),
    ("amount", {"ladder": {"judge": {"verdict": "unavailable"}}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, None),
    ("amount", {"ladder": {"judge": None}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, None),
    ("amount", {"ladder": {"judge": {"verdict": "agree"}}}, {"ladder": {"judge": {"verdict": "agree"}}}, None),
])
def test_degrades_table(kind, old, new, expected):
    assert PL._degrades(kind, old, new) == expected


def test_failed_and_different_are_counted_apart(tmp_path):
    """Extract down (9 entries kept) and the model no longer proposing the corroborating flag (1 decided flag differs): two sentences, each with its own count."""
    conn, cid = completed(tmp_path)
    rerun(conn, cid, extract=down("extract"), flags={"flags": []})
    assert case_error(conn, cid)[1]["message"] == (
        "The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
        "The re-run gave a different result for 1 item you had already decided; your decision and the earlier result were kept, and each item carries a note." + TAIL)
