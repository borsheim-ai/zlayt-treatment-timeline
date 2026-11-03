"""T-139 follow-up (orchestrator note 13:28): code narrows an excerpt whose currency-bearing sentence(s) sit at the START or END of a multi-sentence quote.
The narrowed quote is a contiguous run of whole, verbatim sentences; every rung-1 check re-runs on it (generator.verify); judge 1 runs on the narrowed pair
(D-044/D-058) and, with no answer for that pair, the item is JUDGE_NOT_RUN and held. Held out only when narrowing is impossible or the summary needs the amount."""
import pytest

from app.backend import charge_text as CT
from app.backend import generator, grounding

REC = ("Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week. "
       "ED charge: $3,915.")


# ---------------------------------------------------------------- the pure step
def test_trailing_amount_sentence_is_dropped():
    n = CT.narrow_excerpt(REC)
    assert n == {"excerpt": "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week.",
                 "dropped": ["ED charge: $3,915."]}


def test_leading_amount_sentence_is_dropped():
    n = CT.narrow_excerpt("Charge per visit $140. Plan of care: 8 visits, 2x/week for 6 weeks.")
    assert n["excerpt"] == "Plan of care: 8 visits, 2x/week for 6 weeks." and n["dropped"] == ["Charge per visit $140."]


def test_leading_and_trailing_both_dropped():
    n = CT.narrow_excerpt("Charge per visit $140. Plan of care: 8 visits. Balance due $280.")
    assert n["excerpt"] == "Plan of care: 8 visits." and n["dropped"] == ["Charge per visit $140.", "Balance due $280."]


def test_several_trailing_amount_sentences_are_all_dropped():
    n = CT.narrow_excerpt("Dx: cervical strain. Follow up in 1 week. ED charge: $3,915. Balance $200.")
    assert n["excerpt"] == "Dx: cervical strain. Follow up in 1 week." and len(n["dropped"]) == 2


@pytest.mark.parametrize("excerpt", [
    "ED charge: $3,915.",                                               # one sentence: nothing to keep
    "Charge $140. Balance $280.",                                       # every sentence states an amount
    "Dx: cervical strain. Charge $140. Follow up in 1 week.",           # the amount sits in the MIDDLE: a contiguous run cannot skip it
    "Dx: cervical strain. Follow up in 1 week.",                        # no amount: nothing to narrow
    "",
])
def test_narrowing_is_impossible(excerpt):
    assert CT.narrow_excerpt(excerpt) is None


def test_narrowed_text_is_a_verbatim_substring_of_the_quote():
    q = "Charge per visit $140.\nPlan of care: 8 visits,\n2x/week for 6 weeks."
    n = CT.narrow_excerpt(q)
    assert n["excerpt"] in q and not CT.has_currency(n["excerpt"])


def test_abbreviation_period_is_not_a_sentence_end():
    n = CT.narrow_excerpt("Cervical range of motion reduced approx. 30%. Charge per visit $140.")
    assert n["excerpt"] == "Cervical range of motion reduced approx. 30%."


def test_a_stub_is_not_a_quote():
    assert CT.narrow_excerpt("Billing. Charge per visit $140.") is None          # fewer than 2 content words are left


# ---------------------------------------------------------------- through the generator: rung-1 re-runs on the narrowed quote
def _record(excerpt=REC):
    return {"n": 1, "id": "r1", "source": "Marrowgate General ED", "date_iso": "2026-02-14", "date_status": "parsed", "excerpt": excerpt, "text": excerpt, "char_start": 0}


def _extract(summary, excerpt, record=None):
    rec = record or _record()
    out = {"summary": summary, "excerpt": excerpt}
    def call(step, system, user, schema, *, item_id=None):
        return out, "c1"
    return generator.extract_one(rec, [1], call=call, case_text=rec["excerpt"])


def test_extract_narrows_a_trailing_charge_sentence_and_records_what_was_dropped():
    e = _extract("Diagnosis of cervical strain; X-ray negative for fracture; ibuprofen 600 mg; follow up with primary care in 1 week.", REC)
    assert e["excerpt"].endswith("in 1 week.") and "$" not in e["excerpt"]
    assert "CHARGE_TEXT_IN_ENTRY" not in e["reasons"]
    nar = e["ladder"]["excerpt_narrowed"]
    assert nar["rule"] == "T-139" and nar["dropped"] == ["ED charge: $3,915."] and nar["original_excerpt"] == REC
    assert e["ladder"]["generator"]["output"]["excerpt"] == REC                 # the model's own output is kept for audit
    assert e["ladder"]["code_checks"]["excerpt_verbatim"] and e["ladder"]["code_checks"]["highlight_found"]
    assert REC[e["excerpt_start"]:e["excerpt_end"]] == e["excerpt"]             # offsets belong to the narrowed quote


def test_extract_trims_the_summary_amount_clause_when_the_quote_is_narrowed():
    e = _extract("Diagnosis of cervical strain; X-ray negative for fracture; follow up with primary care in 1 week; ED charge $3,915.", REC)
    assert "$" not in e["summary"] and "CHARGE_TEXT_IN_ENTRY" not in e["reasons"]
    assert e["ladder"]["excerpt_narrowed"]["summary_removed"] == ["ED charge $3,915"]       # shown in the trace data, like D-054


def test_extract_holds_the_entry_when_the_summary_itself_needs_the_amount():
    e = _extract("ED charge $3,915; diagnosis of cervical strain.", REC)          # the amount is in the FIRST clause: code never removes it
    assert "CHARGE_TEXT_IN_ENTRY" in e["reasons"] and e["state"] == "needs_review"
    assert e["excerpt"] == REC and "excerpt_narrowed" not in e["ladder"]          # nothing was changed


def test_extract_holds_the_entry_when_the_amount_is_in_the_middle():
    q = "Dx: cervical strain. ED charge: $3,915. Follow up with primary care in 1 week."
    e = _extract("Diagnosis of cervical strain; follow up with primary care in 1 week.", q, _record(q))
    assert "CHARGE_TEXT_IN_ENTRY" in e["reasons"] and e["excerpt"] == q


def test_narrowing_that_leaves_no_supported_summary_is_not_applied():
    q = "Dx: cervical strain. Return in 3 weeks, fee $140."
    e = _extract("Return in 3 weeks.", q, _record(q))                          # the only clause is supported by the sentence that would be dropped
    assert "CHARGE_TEXT_IN_ENTRY" in e["reasons"] and e["excerpt"] == q and "excerpt_narrowed" not in e["ladder"]
    assert e["state"] == "needs_review"                                        # held, not sent to the could-not-verify tray


def test_narrowing_that_would_fail_a_rung_one_check_is_not_applied():
    q = "Fee $140, no fracture on x-ray. Neck strain."
    e = _extract("No fracture; neck strain.", q, _record(q))                   # 'No fracture' lives in the sentence that would be dropped
    assert "CHARGE_TEXT_IN_ENTRY" in e["reasons"] and e["excerpt"] == q and "excerpt_narrowed" not in e["ladder"]


def test_a_clean_entry_is_untouched():
    q = "Dx: cervical strain. Follow up in 1 week."
    e = _extract("Diagnosis of cervical strain; follow up in 1 week.", q, _record(q))
    assert e["excerpt"] == q and "excerpt_narrowed" not in e["ladder"] and e["state"] != "rejected"


# ---------------------------------------------------------------- judge validity (D-044, D-058)
def _judged(call):
    rec = _record()
    e = _extract("Diagnosis of cervical strain; X-ray negative for fracture; ibuprofen 600 mg; follow up with primary care in 1 week.", REC, rec)
    generator.judge_entries([e], {1: dict(rec, n=1)}, call=call, case_text=rec["excerpt"])
    return e


def test_judge_one_runs_on_the_narrowed_pair_only():
    seen = []

    def call(step, system, user, schema, *, item_id=None):
        seen.append((step, user))
        return {"verdict": "supported", "reason_code": "NONE"}, "j1"
    e = _judged(call)
    assert len(seen) == 1 and seen[0][0] == "j1"
    assert "$3,915" not in seen[0][1] and "ED charge" not in seen[0][1]            # the judge never saw the sentence code dropped
    assert e["ladder"]["judge"]["verdict"] == "supported" and e["state"] == "verified"


def test_a_narrowed_pair_with_no_judge_answer_is_judge_not_run_and_not_verified():
    from app.llm import provider as P

    def call(step, system, user, schema, *, item_id=None):
        raise P.FixtureMiss("k")                                                  # an answer recorded for the OLD pair does not exist for this one
    e = _judged(call)
    assert e["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in e["reasons"] and e["ladder"]["judge"]["verdict"] == "unavailable"
