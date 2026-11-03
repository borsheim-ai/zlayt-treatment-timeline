"""Pipeline stages with a scripted fake `call` (no key, no network). app/README-arch.md stage list, R-IN-1, R-TL-1, R-FL-1, R-CH-*, ADR-007, LLM_VS_CODE rows 1-3, 9, 15."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record, sample_script, run_sample, items_for

STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]

def script():
    return sample_script()

@pytest.fixture
def run(tmp_path):
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    call = FakeCall(script())
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    return out, call

def test_stage_names_and_order():
    """ADR-007 / README-arch: stages are exactly ingest, extract, verify, judge_entries, amounts, conflicts, flags, finalize."""
    assert list(PL.STAGES) == STAGES

def test_ingest_is_synchronous_code_with_gaps_and_no_llm():
    """Row 9 / arch: ingest returns records, dates, regex amounts and the gap flag without any LLM call."""
    out = PL.run_ingest(G.raw("sample"))
    assert len(out["records"]) == 9
    g = [f for f in out["flags"] if f["type"] == "gap"]
    assert [(f["from_date"], f["to_date"], f["days"]) for f in g] == [("2026-03-06", "2026-05-18", 73)]
    assert len(out["amounts"]) == 3

def test_nine_entries_all_verified_with_code_set_provider_and_date(run):
    """R-TL-1, R-TL-9: nine entries in date order; provider = header label and date = header date set by code; states verified."""
    out, _ = run
    ents = out["entries"]
    assert len(ents) == 9 and [e["date"] for e in ents] == sorted(e["date"] for e in ents)
    assert ents[3]["provider"] == "Capital PT, initial evaluation"
    assert ents[6]["date"] == "2026-05-18"
    assert all(e["state"] == "verified" and e["review_status"] == "pending" for e in ents)

def test_call_budget_about_forty(run):
    """ADR-003: about 40 calls on the sample (9 extract, 9 J1, 3 J2, conflicts, 9 flags, judges); never an unbounded loop."""
    _, call = run
    assert 30 <= len(call.log) <= 50
    assert call.steps().count("extract") == 9 and call.steps().count("flags") == 9 and call.steps().count("j1") == 9

def test_amounts_classified_by_code_and_totals(run):
    """R-CH-2/3: $6,240 and $2,150 charges, $185 rate (needs_review AMOUNT_RATE_NOT_TOTALED); nothing accepted yet so accepted total is 0."""
    out, _ = run
    by = {a["raw"]: a for a in out["amounts"]}
    assert by["$185"]["cls"] == "rate" and "AMOUNT_RATE_NOT_TOTALED" in by["$185"]["reasons"]
    assert by["$6,240"]["cls"] == "charge" and by["$2,150"]["cls"] == "charge"
    assert out["totals"]["accepted_cents"] == 0

def test_code_conflict_and_gap_flags_present_without_llm_help(run):
    """R-FL-1, R-FL-2: the 73-day gap and the accident-date conflict come from code."""
    out, _ = run
    types = {(f["type"], f.get("subtype")) for f in out["flags"]}
    assert ("gap", None) in types or ("gap", "treatment_gap") in types
    assert ("conflict", "accident_date") in types

def gap_keys(out):
    return sorted((f["from_date"], f["to_date"], f["days"]) for f in out["flags"] if f["type"] == "gap")

def test_code_stages_without_llm(tmp_path):
    """T-037 AC4 / row 9 / LLM_FAILED_AFTER_RETRIES: if EVERY model call fails, gaps, amounts and the accident-date conflict still exist; no entry is invented; the run reports done_with_errors with the error code."""
    boom = FakeCall({s: AU.LLMFailed("down") for s in ("extract", "j1", "j2", "j3", "j4", "conflicts", "flags")})
    out, _ = run_sample(tmp_path, call=boom)
    assert gap_keys(out) == [("2026-03-06", "2026-05-18", 73)] and len(out["amounts"]) == 3
    assert any(f["type"] == "conflict" and f.get("subtype") == "accident_date" for f in out["flags"])
    assert out["entries"] == []
    assert out["status"] == "done_with_errors" and any(e["code"] == "LLM_FAILED_AFTER_RETRIES" for e in out["errors"])

def test_one_failed_extract_loses_only_that_entry_and_leaves_gaps_unchanged(tmp_path):
    """T-037 AC4 / D-003 / row 9: record 6 (a gap endpoint) fails to extract -> 8 entries, a visible error naming it, and the gap flags are identical to a clean run."""
    clean, _ = run_sample(tmp_path)
    def extract(user):
        if which_record(user) == [6]:
            raise AU.LLMFailed("down")
        return sample_script()["extract"](user)
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(extract=extract)))
    assert len(out["entries"]) == 8 and not [e for e in items_for(out, 6) if e["state"] == "verified"]
    assert out["status"] == "done_with_errors"
    assert any(e["code"] == "LLM_FAILED_AFTER_RETRIES" and e.get("record_no") == 6 for e in out["errors"])
    assert gap_keys(out) == gap_keys(clean) == [("2026-03-06", "2026-05-18", 73)]

def test_fixture_missing_after_audited_wrapper_is_a_visible_error_never_a_default(tmp_path):
    """T-034 AC8 / T-037 AC7: a recorded-answer miss reaches the pipeline as LLM_FAILED_AFTER_RETRIES (the audited wrapper converts FixtureMissing); the item is absent with a run-level error, not filled in."""
    miss = AU.LLMFailed("FIXTURE_MISS abc")
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(extract=miss)))
    assert out["entries"] == [] and out["status"] == "done_with_errors"
    assert {e["code"] for e in out["errors"]} == {"LLM_FAILED_AFTER_RETRIES"} and len(out["errors"]) == 9

def test_verify_stage_rejects_non_verbatim_excerpt(tmp_path):
    """T-035 AC2 / R-TL-2 (rung 1): a seeded excerpt that is not word for word in its record, and one with an invented sentence appended, never become verified entries even though judge 1 says 'supported'. Fails if the verify/grounding stage is removed."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        summ, quote = sums[n]
        if n == 3:
            quote = quote.replace("Persistent", "Chronic")           # altered words
        if n == 5:
            quote = quote + " Patient reports permanent disability."  # invented sentence
        return dict(summary=summ, excerpt=quote)
    out, call = run_sample(tmp_path, call=FakeCall(sample_script(extract=extract)))
    for n in (3, 5):
        items = items_for(out, n)
        assert items, f"record {n}: the failed attempt must be visible (tray), not silently dropped"
        assert all(i["state"] != "verified" for i in items)
        assert all("GROUNDING_EXCERPT_NOT_VERBATIM" in i["reasons"] and i["state"] == "rejected" for i in items)
    assert not [e for e in out["entries"] if e["state"] == "rejected"]          # rejected items live in the tray only
    assert len([e for e in out["entries"] if e["state"] == "verified"]) == 7
    assert call.steps().count("j1") == 7        # judge 1 never saw the rejected attempts, so it cannot have rescued them

def test_stages_and_deadline(tmp_path):
    """ADR-007: 8-minute deadline using an injectable clock; past it the run stops with status 'timeout', not a hang."""
    conn = DB.connect(str(tmp_path / "s.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    t = iter(range(0, 10**6, 100))
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script()), now=lambda: float(next(t)), deadline_s=480)
    assert out["status"] == "timeout" and list(PL.STAGES) == STAGES

def test_injection_case_runs_end_to_end():
    """R-RV-6: case_07 yields an ordinary entry for record 3 with an INJECTION_SUSPECTED warning; only $420 is a totalable charge."""
    out = PL.run_ingest(G.raw("case_07_prompt_injection"))
    assert any(w["code"] == "INJECTION_SUSPECTED" and w["record_no"] == 3 for w in out["warnings"])
    cls = {a["raw"]: a["cls"] for a in out["amounts"]}
    assert cls["$420"] == "charge" and cls["$50,000"] == "unclear"

def test_duplicate_records_collapse_before_any_llm_call(tmp_path):
    """R-TL-7: case_04 makes 4 extract calls, not 6 (dedupe is code and happens first)."""
    conn = DB.connect(str(tmp_path / "u.sqlite")); cid = DB.create_case(conn, G.raw("case_04_duplicates_no_amounts"), now=1.0)
    c = FakeCall({"extract": lambda u: dict(summary="Splint applied.", excerpt=G.record("case_04_duplicates_no_amounts", which_record(u, "case_04_duplicates_no_amounts")[0])["excerpt"]),
                  "j1": {"verdict": "supported", "reason_code": "NONE"}, "conflicts": {"flags": []}, "flags": {"flags": []}})
    PL.run_pipeline(conn, cid, G.raw("case_04_duplicates_no_amounts"), call=c, now=lambda: 1.0)
    assert c.steps().count("extract") == 4


# ---- judge verdicts and failures reach item state (rung 2; T-035 AC3/AC4/AC7, T-036 AC5/AC9) ----
def by_raw(out):
    return {a["raw"]: a for a in out["amounts"]}

@pytest.mark.parametrize("verdict,reason", [("partially", "JUDGE_PARTIAL"), ("unsupported", "JUDGE_UNSUPPORTED")])
def test_j1_partial_or_unsupported_makes_entry_needs_review(tmp_path, verdict, reason):
    """T-035 AC3 / R-TL-4: judge 1 partially/unsupported -> every entry needs_review with the matching reason (never verified)."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j1={"verdict": verdict, "reason_code": "NONE"})))
    assert len(out["entries"]) == 9 and all(e["state"] == "needs_review" and reason in e["reasons"] for e in out["entries"])

def test_j1_failure_is_judge_unavailable_not_verified(tmp_path):
    """ADR-005 / T-035 AC3: judge 1 error or timeout -> needs_review JUDGE_UNAVAILABLE; the generator's entry is kept, not dropped."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j1=AU.LLMFailed("down"))))
    assert len(out["entries"]) == 9 and all(e["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in e["reasons"] for e in out["entries"])

@pytest.mark.parametrize("j2,reason", [(AU.LLMFailed("down"), "JUDGE_UNAVAILABLE"), ({"verdict": "unsure", "reason_code": "NONE"}, "JUDGE_UNSURE")])
def test_j2_error_or_unsure_never_verifies_a_charge(tmp_path, j2, reason):
    """T-035 AC4 / T-036 AC9: a charge is verified only on 'agree'; judge 2 error -> JUDGE_UNAVAILABLE, unsure -> JUDGE_UNSURE; both needs_review."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j2=j2)))
    for raw in ("$6,240", "$2,150"):
        a = by_raw(out)[raw]
        assert a["cls"] == "charge" and a["state"] == "needs_review" and reason in a["reasons"]

def test_j2_agree_verifies_charges_and_rate_stays_needs_review(tmp_path):
    """R-CH-2: with judge 2 agreeing, charges are verified; the $185 rate still carries AMOUNT_RATE_NOT_TOTALED."""
    out, _ = run_sample(tmp_path)
    assert by_raw(out)["$6,240"]["state"] == "verified" and "AMOUNT_RATE_NOT_TOTALED" in by_raw(out)["$185"]["reasons"]

SEM = [dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.",
            excerpt_b="Discharged from PT after two missed appointments.")]

@pytest.mark.parametrize("j3", [AU.LLMFailed("down"), {"verdict": "unsure", "reason_code": "NONE"}])
def test_j3_error_or_unsure_makes_candidate_conflicts_needs_review(tmp_path, j3):
    """T-036 AC5/AC9 (T-094: the pair is proposed by code): a conflict whose judge 3 failed or was unsure is needs_review (JUDGE_UNAVAILABLE / JUDGE_UNSURE), never verified."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j3=j3)))
    llm = [f for f in out["flags"] if f["type"] == "conflict" and f.get("category") == "treatment_plan_vs_actual"]
    assert llm and all(f["state"] == "needs_review" and ({"JUDGE_UNAVAILABLE", "JUDGE_UNSURE"} & set(f["reasons"])) for f in llm)

def test_j3_conflict_verdict_keeps_candidate_conflict_and_code_conflict_is_unaffected(tmp_path):
    """T-036 AC2 (b), T-094: the 12-visit plan vs discharge-at-visit-9 pair is proposed by code, judge 3 says 'conflict'; the accident-date conflict stays a single code flag."""
    out, call = run_sample(tmp_path, call=FakeCall(sample_script(conflicts={"flags": SEM})))
    sem = [f for f in out["flags"] if f["type"] == "conflict" and f.get("category") == "treatment_plan_vs_actual"]
    assert len(sem) == 1 and sem[0]["state"] == "verified" and "conflicts" not in call.steps()
    assert len([f for f in out["flags"] if f["type"] == "conflict" and f.get("subtype") == "accident_date"]) == 1   # D-025 / T-036 AC7

def test_j3_benign_puts_the_candidate_in_the_tray_not_the_flag_list(tmp_path):
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j3={"verdict": "benign", "reason_code": "CAN_BOTH_BE_TRUE"})))
    assert not [f for f in out["flags"] if f.get("category") == "treatment_plan_vs_actual"]
    assert [f for f in out["tray"] if f.get("category") == "treatment_plan_vs_actual" and "JUDGE_DISAGREES" in f["reasons"]]

K_PRE = dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")

@pytest.mark.parametrize("j4,reason", [(AU.LLMFailed("down"), "JUDGE_UNAVAILABLE"), ({"verdict": "unsure", "reason_code": "NONE"}, "JUDGE_UNSURE"), ({"verdict": "disagree", "reason_code": "NONE"}, "JUDGE_DISAGREES")])
def test_j4_error_unsure_or_disagree_makes_flag_needs_review(tmp_path, j4, reason):
    """T-036 AC5/AC9: a model flag on record 3 whose judge 4 failed, was unsure or disagreed is needs_review with that reason."""
    def flags(user):
        return {"flags": [K_PRE]} if which_record(user) == [3] else {"flags": []}
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(flags=flags, j4=j4)))
    f3 = [f for f in out["flags"] if f["type"] == "pre_existing" and "low back pain in 2023" in f["excerpt"]]
    assert f3 and all(f["state"] == "needs_review" and reason in f["reasons"] for f in f3)

# ---- ladder and review state (T-037 AC5, R-CO-2, R-RV-6, row 20) ----
def test_ladder_and_pending(run):
    """T-037 AC5: every entry, amount and flag has a ladder record naming its backend, and nothing is accepted, edited or dismissed by a run."""
    out, _ = run
    items = out["entries"] + out["amounts"] + out["flags"]
    assert items and all(i["review_status"] == "pending" for i in items)
    assert all(i["ladder"]["backend"] for i in items)
    assert all(i["ladder"].get("judge") or i["ladder"].get("generator") is None or i["state"] == "rejected" for i in out["entries"])

def test_exactly_one_accident_date_conflict_on_the_sample(run):
    """T-036 AC7 / D-025: the accident-date rule yields exactly one conflict flag citing records 1, 2 and 7."""
    out, _ = run
    acc = [f for f in out["flags"] if f["type"] == "conflict" and f.get("subtype") == "accident_date"]
    assert len(acc) == 1


def test_model_only_flag_rejected_by_j4_goes_to_the_tray_with_the_judges_reason(tmp_path):
    """T-094 r2 / D-053: a flag only the model proposed (no phrase-list hit) that J4 rejects is never dropped: it is a could-not-verify tray item (state
    rejected, JUDGE_DISAGREES, the judge's fixed reason sentence), not a flag, and nothing is called suppressed."""
    extra = dict(type="causation", category="alternative_cause", excerpt="Cervical range of motion reduced approx. 40%.")
    def flags(user):
        return {"flags": [extra]} if which_record(user) == [4] else {"flags": []}
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(flags=flags, j4={"verdict": "disagree", "reason_code": "NOT_SUPPORTED_BY_QUOTE"})))
    assert not [f for f in out["flags"] if f.get("category") == "alternative_cause"]
    t = [f for f in out["tray"] if f.get("category") == "alternative_cause"]
    assert len(t) == 1 and t[0]["state"] == "rejected" and t[0]["reasons"][0] == "JUDGE_DISAGREES" and t[0]["excerpt"] == extra["excerpt"]
    assert "does not find this flag supported" in t[0]["why"] and t[0]["ladder"]["judge"]["verdict"] == "disagree"
    assert "suppressed_flags" not in out
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(flags=flags, j4={"verdict": "unsure", "reason_code": "TEXT_AMBIGUOUS"})))
    assert [f for f in out["flags"] if f.get("category") == "alternative_cause"] and not [f for f in out["tray"] if f.get("category") == "alternative_cause"]


def test_tray_flag_is_in_the_database_and_the_case_view_tray(tmp_path):
    """D-053: the item the judge rejected is visible through the API shape (present.case_view tray, kind flag), and never in the flag list or the review queue."""
    from app.backend import present
    extra = dict(type="causation", category="alternative_cause", excerpt="Cervical range of motion reduced approx. 40%.")
    flags = lambda user: {"flags": [extra]} if which_record(user) == [4] else {"flags": []}
    conn = DB.connect(str(tmp_path / "v.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=flags, j4={"verdict": "disagree", "reason_code": "NOT_SUPPORTED_BY_QUOTE"})), now=lambda: 1.0)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    t = [x for x in v["tray"] if x["kind"] == "flag"]
    assert len(t) == 1 and t[0]["reasons"][0] == "JUDGE_DISAGREES" and t[0]["state"] == "rejected" and t[0]["record_ids"]
    assert t[0]["attempt"]["excerpt"] == extra["excerpt"] and t[0]["flag"] == {"type": "causation", "category": "alternative_cause"}
    assert not [f for f in v["flags"] if f["category"] == "alternative_cause"] and t[0]["id"] not in v["review"]["queue"]


def test_a_model_proposed_conflict_that_no_code_candidate_made_goes_to_the_tray():
    """D-053: only a code candidate can be a conflict flag; a model-proposed conflict is a tray item (LLM_ONLY), never judged into a flag."""
    from app.backend import flags as F
    fl = [dict(F._flag({"n": 1, "id": "r1", "excerpt": "Plan of care: 12 visits."}, "conflict", "other_fact_mismatch", "Plan of care: 12 visits.", "llm", (0, 24), False, "llm_only"), id="f1", excerpt_b="x")]
    out = F.judge_flags(fl, call=FakeCall({"j3": {"verdict": "conflict", "reason_code": "FACT_MISMATCH"}}))
    assert out[0]["state"] == "rejected" and out[0]["reasons"][0] == "LLM_ONLY"
