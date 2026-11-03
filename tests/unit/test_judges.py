"""Judges J1-J4 (independent LLM check, rung 2). LLM_VS_CODE rows 4, 7, 11, 12; ADR-008.5; R-TL-4. Fake `call` only (no key, no network)."""
import pytest
from app.backend import judges as J
from app.llm import audited as AU
from tests.unit._fakes import FakeCall
from tests.unit import _golden as G

def call_returning(verdict):
    return FakeCall({"j1": {"verdict": verdict, "reason_code": "NONE"}, "j2": {"verdict": verdict, "reason_code": "NONE"},
                     "j3": {"verdict": verdict, "reason_code": "NONE"}, "j4": {"verdict": verdict, "reason_code": "NONE"}})

@pytest.mark.parametrize("v", ["supported", "partially", "unsupported"])
def test_j1_states(v):
    """Row 4: J1 maps the model enum to a verdict."""
    assert J.run_j1("Pain 4/10.", "Pain 4/10, improving.", "Capital PT, visit 8", call=call_returning(v)) == v

def test_j1_prompt_has_record_and_candidate_only():
    """Row 4 / ADR-003: judge sees the excerpt and the candidate summary - never the generator's reasoning or other records."""
    c = call_returning("supported")
    J.run_j1("Visit 8: pain 4/10.", "Pain 4/10, improving.", "Capital PT, visit 8", call=c, nonce="abc123")
    u = c.prompts("j1")[0]
    assert "Pain 4/10, improving." in u and "Visit 8: pain 4/10." in u
    assert "reasoning" not in u.lower() and "Dx: cervical strain" not in u

def test_j1_wraps_record_text_in_nonce_delimiters():
    """ADR-008.5: record text is wrapped in nonce delimiters."""
    c = call_returning("supported")
    J.run_j1("s", "excerpt text", "label", call=c, nonce="n0nce")
    assert "<record-n0nce>" in c.prompts("j1")[0]

J_CASES = [("run_j1", ("s", "e", "l")), ("run_j2", ("e", "$185", "rate")), ("run_j3", ("a", "b")), ("run_j4", ("e", "pre_existing", "pre_existing"))]
J_STEP = {"run_j1": "j1", "run_j2": "j2", "run_j3": "j3", "run_j4": "j4"}

@pytest.mark.parametrize("fn,args", J_CASES)
def test_judge_unavailable_when_call_fails(fn, args):
    """ADR-005 JUDGE_UNAVAILABLE: a failed call of ANY judge (J1-J4) yields 'unavailable', never an exception and never a passing verdict."""
    c = FakeCall({J_STEP[fn]: AU.LLMFailed("x")})
    assert getattr(J, fn)(*args, call=c) == "unavailable"

@pytest.mark.parametrize("fn,args", J_CASES)
def test_judge_unparseable_verdict_is_never_a_pass(fn, args):
    """ADR-005: an out-of-enum verdict from any judge can never become supported/agree/benign."""
    c = FakeCall({J_STEP[fn]: {"verdict": "yes", "reason_code": "NONE"}})
    assert getattr(J, fn)(*args, call=c) in ("unavailable", "unsure")

def test_j2_every_amount(tmp_path):
    """T-035 AC4 / row 7: judge 2 re-reads EVERY amount incl. rule-made ones (sample: 3 amounts -> 3 j2 calls); the rate never becomes a charge when J2 disagrees."""
    from tests.unit._fakes import run_sample, sample_script
    out, call = run_sample(tmp_path, call=FakeCall(sample_script(j2={"verdict": "disagree", "reason_code": "NONE"})))
    assert call.steps().count("j2") == 3 == len(out["amounts"])
    by = {a["raw"]: a for a in out["amounts"]}
    assert by["$185"]["cls"] == "rate" and all(a["state"] == "needs_review" and "JUDGE_DISAGREES" in a["reasons"] for a in out["amounts"])

@pytest.mark.parametrize("v,exp", [("agree", "agree"), ("disagree", "disagree"), ("unsure", "unsure")])
def test_j2_rereads_amount_class(v, exp):
    """Row 7: J2 re-reads the excerpt and confirms or disputes the code's class."""
    assert J.run_j2("Charge per visit $185.", "$185", "rate", call=call_returning(v)) == exp

@pytest.mark.parametrize("v", ["conflict", "benign", "unsure"])
def test_j3_conflict_verdicts(v):
    """Row 11: J3 decides whether two excerpts really conflict."""
    assert J.run_j3("Plan of care: 12 visits.", "Discharged from PT after two missed appointments.", call=call_returning(v)) == v

@pytest.mark.parametrize("v", ["agree", "disagree", "unsure"])
def test_j4_flag_category(v):
    """Row 12: J4 confirms or disputes a flag category."""
    assert J.run_j4("Findings may represent degenerative change", "pre_existing", "degenerative_language", call=call_returning(v)) == v

def test_judge_model_differs_from_generator_by_default(monkeypatch):
    """Row 4: independent judge - different model by default (GENERATOR_MODEL vs JUDGE_MODEL)."""
    for k in ("GENERATOR_MODEL", "JUDGE_MODEL"):
        monkeypatch.delenv(k, raising=False)
    assert J.judge_model() != J.generator_model()

def test_seeded_hallucinations_are_all_presented_to_judge_with_their_record():
    """R-TL-4 / ship bar 4: every seeded item can be run through J1 (record_text + candidate); a judge that says 'unsupported' catches 100% (harness check, judge recall itself is an eval)."""
    import json
    items = [json.loads(l) for l in (G.G / "hallucinations.jsonl").read_text().splitlines()]
    c = call_returning("unsupported")
    caught = sum(J.run_j1(i["candidate_summary"], i["record_text"], "label", call=c) != "supported" for i in items)
    assert caught == len(items) >= 40
