"""T-146 r4 (§7.4 fix-up). (1) The keep-and-note compare reads the whole ladder, not only the state: a decided item whose checks get worse INSIDE the same state (a new
reason, a second-check answer that moves from positive to negative, a code check that turns false) is kept whole with a note, and the case reads run_partial.
(2) A failure in the conflicts step (judge 3) makes the case failed and the export gate RUN_FAILED, like every other step."""
import pytest
from app.backend import pipeline as PL, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script
from tests.unit.test_t146_r3_decided_items_never_lowered import (OLD_AMOUNT, OLD_ENTRY, OLD_FLAG, NEW_FLAG, TAIL, assert_notes, case_error, completed, down, full,
                                                                  model_flag, note, rerun)


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


# ---- the compare, equal-rank rows (state needs_review on both sides)
NR_AMOUNT = {**OLD_AMOUNT, "state": "needs_review", "state_reasons": ["AMOUNT_RATE_NOT_TOTALED"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"amount_in_text": True}}}
NEW_AMT = {"text": "$10", "cents": 1000, "cls": "charge", "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
           "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"amount_in_text": True}}}
NR_ENTRY = {**OLD_ENTRY, "state": "needs_review", "state_reasons": ["QUALIFIER_DROPPED"],
            "ladder": {"judge": {"verdict": "partially"}, "code_checks": {"excerpt_verbatim": True, "summary_tokens_not_in_excerpt": []}}}
NEW_ENT = {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "needs_review", "reasons": ["QUALIFIER_DROPPED"],
           "ladder": {"judge": {"verdict": "partially"}, "code_checks": {"excerpt_verbatim": True, "summary_tokens_not_in_excerpt": []}}}
NR_FLAG = {**OLD_FLAG, "state": "needs_review", "state_reasons": ["LEXICON_ONLY"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"excerpt_verbatim": True}}}
NEW_FL = {**NEW_FLAG, "state": "needs_review", "reasons": ["LEXICON_ONLY"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"excerpt_verbatim": True}}}


def lad(judge=None, **checks):
    return {"judge": {"verdict": judge} if judge else None, "code_checks": checks}


@pytest.mark.parametrize("kind,old,new,expected", [
    ("amount", NR_AMOUNT, NEW_AMT, False),                                                                                    # identical: nothing changed
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": ["JUDGE_DISAGREES", "AMOUNT_RATE_NOT_TOTALED"], "ladder": lad("disagree", amount_in_text=True)}, True),     # the F1 repro
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": ["AMOUNT_RATE_NOT_TOTALED", "OCR_DERIVED"]}, True),                          # a new reason alone
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": []}, False),                                                                 # a reason gone is not worse
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("disagree", amount_in_text=True)}, True),                                 # answer agree -> disagree, same reasons
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("unsure", amount_in_text=True)}, True),
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("agree", amount_in_text=False)}, True),                                   # a code check true -> false
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": {"judge": None, "code_checks": {"amount_in_text": True}}}, False),            # no new answer is not a negative answer
    ("amount", {**NR_AMOUNT, "ladder": lad("disagree", amount_in_text=True)}, {**NEW_AMT, "ladder": lad("agree", amount_in_text=True)}, False),    # better
    ("amount", {**NR_AMOUNT, "ladder": lad("unsure", amount_in_text=True)}, {**NEW_AMT, "ladder": lad("disagree", amount_in_text=True)}, False),   # was not positive: no answer was taken back
    ("entry", NR_ENTRY, NEW_ENT, False),
    ("entry", {**NR_ENTRY, "ladder": lad("supported", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])},
     {**NEW_ENT, "ladder": lad("unsupported", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])}, True),
    ("entry", NR_ENTRY, {**NEW_ENT, "ladder": lad("partially", excerpt_verbatim=True, summary_tokens_not_in_excerpt=["fracture"])}, True),    # unsupported tokens appear
    ("entry", NR_ENTRY, {**NEW_ENT, "reasons": ["QUALIFIER_DROPPED", "DATE_UNCONFIRMED"]}, True),
    ("flag", NR_FLAG, NEW_FL, False),
    ("flag", NR_FLAG, {**NEW_FL, "reasons": ["LEXICON_ONLY", "JUDGE_DISAGREES"], "ladder": lad("disagree", excerpt_verbatim=True)}, True),
    ("flag", NR_FLAG, {**NEW_FL, "ladder": lad("conflict", excerpt_verbatim=True)}, False),                                   # agree and conflict are both positive
    ("flag", {**NR_FLAG, "ladder": lad("conflict", excerpt_verbatim=True)}, {**NEW_FL, "ladder": lad("benign", excerpt_verbatim=True)}, True),
    ("flag", NR_FLAG, {**NEW_FL, "days": 40, "reasons": ["LEXICON_ONLY", "JUDGE_DISAGREES"]}, False),                         # numbers moved: the reset path decides
])
def test_disagrees_reads_the_whole_ladder(kind, old, new, expected):
    assert PL._disagrees(kind, old, new) is expected


# ---- end to end: the F1 repro (accepted or dismissed rate in needs_review, the second check flips)
@pytest.mark.parametrize("action", ["accept", "dismiss"])
def test_decided_needs_review_amount_survives_a_judge_that_now_disagrees(tmp_path, action):
    conn, cid = completed(tmp_path)
    a2 = DB.get_item(conn, "a2", cid)
    assert (a2["state"], a2["state_reasons"], a2["ladder"]["judge"]["verdict"]) == ("needs_review", ["AMOUNT_RATE_NOT_TOTALED"], "agree")
    DB.apply_review(conn, "a2", action, now=2.5, case=cid)
    before = full(conn, cid)
    out = rerun(conn, cid, j2={"verdict": "disagree", "reason_code": "NONE"})
    assert out["status"] == "done"
    after = DB.get_item(conn, "a2", cid)
    assert (after["state"], after["state_reasons"], after["ladder"]["judge"]["verdict"], after["review_status"]) == \
        ("needs_review", ["AMOUNT_RATE_NOT_TOTALED"], "agree", "accepted" if action == "accept" else "dismissed")
    assert full(conn, cid)["amount"]["a2"] == before["amount"]["a2"]                  # the whole stored row, call id aside
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert "The re-run gave a different result for" in err["message"] and err["message"].endswith(TAIL)
    n = note(conn, cid, "a2")
    assert n and n["kind"] == "disagreed" and n["step"] == "a different result"
    assert "RUN_FAILED" in blockers(conn, cid)


def test_an_undecided_needs_review_amount_takes_the_new_answer_and_the_case_stays_ready(tmp_path):
    """Control: nothing was decided, so there is nothing to protect; the new check result stands."""
    conn, cid = completed(tmp_path, decide=False)
    rerun(conn, cid, j2={"verdict": "disagree", "reason_code": "NONE"})
    a2 = DB.get_item(conn, "a2", cid)
    assert a2["ladder"]["judge"]["verdict"] == "disagree" and "JUDGE_DISAGREES" in a2["state_reasons"]
    assert note(conn, cid, "a2") is None
    assert "RUN_FAILED" not in blockers(conn, cid)


def test_a_clean_rerun_of_a_decided_case_has_no_run_failed_blocker(tmp_path):
    conn, cid = completed(tmp_path)
    rerun(conn, cid)
    assert case_error(conn, cid) == ("ready", None)
    assert "RUN_FAILED" not in blockers(conn, cid)


# ---- the conflicts step (judge 3)
def j3_cases(tmp_path, decide_cx):
    conn, cid = completed(tmp_path)
    cx = DB.get_item(conn, "f_cx1", cid)
    assert (cx["state"], cx["ladder"]["judge"]["verdict"], cx["review_status"]) == ("verified", "conflict", "pending")
    if decide_cx:
        DB.apply_review(conn, "f_cx1", "accept", now=2.5, case=cid)
    return conn, cid


@pytest.mark.parametrize("decide_cx", [False, True])
@pytest.mark.parametrize("miss", [False, True])
def test_conflicts_step_down_keeps_the_conflict_flag_fails_the_case_and_blocks_the_gate(tmp_path, decide_cx, miss):
    conn, cid = j3_cases(tmp_path, decide_cx)
    before = full(conn, cid)
    out = rerun(conn, cid, j3=PL.AU.LLMFailedFixtureMiss("x") if miss else down("j3"))
    assert out["status"] == "done" and out["error"]["code"] == "run_partial"
    assert full(conn, cid) == before
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err["message"] == ("The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged." + TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)
    assert bool(note(conn, cid, "f_cx1")) is decide_cx          # a decided item carries the note; an undecided one is kept silently
    rerun(conn, cid)                                             # a good run clears the failure and the gate
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert DB.get_item(conn, "f_cx1", cid)["ladder"]["judge"]["verdict"] == "conflict"


def test_conflicts_step_down_twice_with_nothing_to_keep_still_fails_the_case(tmp_path):
    """The first run had judge 3 down (the conflict flag is needs_review with no answer); a second run with it down again has no earlier answer to keep."""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag, j3=down("j3"))), now=lambda: 1.0)
    assert DB.get_item(conn, "f_cx1", cid)["ladder"]["judge"]["verdict"] == "unavailable"
    rerun(conn, cid, j3=down("j3"))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert err["message"] == "The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep." + TAIL
    assert "RUN_FAILED" in blockers(conn, cid)


def test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):
    """The deadline passes during the amounts stage, so the conflicts stage is skipped (and GET case checks say so)."""
    conn, cid = j3_cases(tmp_path, True)
    before = full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == "amounts":
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_deadline"
    assert full(conn, cid) == before and "RUN_FAILED" in blockers(conn, cid)
    assert DB.get_case(conn, cid)["config"]["run_checks"]["conflicts_stage"] == "skipped"


# ---- review minor: the gate agrees with the case on every r3 failure path
@pytest.mark.parametrize("script", [
    {"flags": down("flags")},
    {"extract": down("extract")},
    {"j1": down("j1")},
    {"j2": down("j2")},
    {"j4": down("j4")},
    {"j3": down("j3")},
    {"extract": lambda user: {"summary": "Patient had surgery on Mars.", "excerpt": "Patient reports low back pain in 2023, resolved."}},      # summary-in-quote check fails
], ids=["flags", "extract", "j1", "j2", "j4", "j3", "summary_not_in_quote"])
def test_gate_lists_run_failed_whenever_the_case_is_failed(tmp_path, script):
    conn, cid = completed(tmp_path)
    rerun(conn, cid, **script)
    assert case_error(conn, cid)[0] == "failed"
    assert "RUN_FAILED" in blockers(conn, cid)
