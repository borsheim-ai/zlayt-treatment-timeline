"""T-075 (R-CO-7): the order, wording or duplication of what a model returns must not change the flag set, the flag ids or the judge prompts.
Fake model only; the live 3-run check is evals/run.py."""
import itertools
from app.backend import flags as F, judges as J
from app.llm import audited as AU, promptlib, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall

EX = G.expected("sample")
HEDGE = "Findings may represent degenerative change; correlate clinically."
PLAN, OUT = "Plan of care: 12 visits.", "Discharged from PT after two missed appointments."


def rec(n):
    r = G.record("sample", n)
    return dict(n=n, source=r["source"], excerpt=r["excerpt"], date_iso=EX["records"][n - 1]["date"])


def _ident(fl):
    return [(f["type"], f["category"], f["excerpt"], f["origin"], f["state"], tuple(f["reasons"])) for f in fl]


def test_model_flag_order_does_not_change_the_flag_list():
    """Three model-only flags (no lexicon flag shares their type and span) returned in every order, with a duplicate, give the same flags in
    the same order (ids f_r{n}_{k} follow this order). Removing the model-flag sort in flags.merge makes this fail."""
    m1 = dict(type="causation", category="missed_care", excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")
    m2 = dict(type="causation", category="new_onset", excerpt="mild right foraminal narrowing")
    m3 = dict(type="causation", category="patient_report", excerpt="Charge: $2,150.")
    r8 = rec(8)
    base = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [m1, m2, m3]}}))
    model_only = [f for f in base if f["origin"] != "lexicon"]
    assert len(model_only) == 3                      # the setup really has three model-only flags
    for order in itertools.permutations([m1, m2, m3]):
        got = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [*order, dict(order[0])]}}))
        assert _ident(got) == _ident(base), [x["category"] for x in order]


def test_model_cannot_change_the_conflict_list_and_ids_follow_the_code_order():
    """T-094: whatever a model returns on a (now unused) conflicts step, the conflict flags and their ids f_cx1.. come from code candidates only."""
    recs = [rec(n) for n in range(1, 10)]
    junk = dict(type="conflict", category="other_fact_mismatch", excerpt="Pain 4/10, improving.", excerpt_b="Pain 3/10.")
    one = F.run_conflict_pass(recs, call=FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}, "conflicts": {"flags": [junk]}}))
    two = F.run_conflict_pass(recs, call=FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}, "conflicts": {"flags": [junk, dict(junk)]}}))
    assert [(f["id"], f["category"], f["record_nos"], f["state"]) for f in one] == [(f["id"], f["category"], f["record_nos"], f["state"]) for f in two] == [("f_cx1", "treatment_plan_vs_actual", [4, 6], "verified")]


def test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v4_and_v2():
    c = FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}})
    fl = F.run_conflict_pass([rec(n) for n in range(1, 10)], call=c)
    assert "FLAG CATEGORY: treatment_plan_vs_actual" in c.prompts("j3")[0]
    assert fl[0]["ladder"]["judge"]["prompt_version"] == "judge_conflict_v6"
    assert AU.PROMPT_OF_STEP["j3"] == "judge_conflict_v6" and AU.PROMPT_OF_STEP["j4"] == "judge_flag_v3" and "conflicts" not in AU.PROMPT_OF_STEP
    assert "decision rules" in promptlib.load("judge_conflict_v6").text.lower() and "unsure" in promptlib.load("judge_flag_v3").text
    assert "denies prior" in promptlib.load("judge_conflict_v6").text.lower()


def test_live_backend_retries_pause_but_fixture_does_not(monkeypatch):
    """T-075: a live backend that just failed is retried after a pause, not at once; the fixture backend never sleeps."""
    seen = []
    monkeypatch.setattr(AU, "audited_call", lambda *a, **k: seen.append(k.get("sleep")) or ({}, "c1"))
    call = AU.make_call(None, "case")
    monkeypatch.setattr(P, "backend_name", lambda: "fixture")
    call("j4", "s", "u", {})
    monkeypatch.setattr(P, "backend_name", lambda: "claude-cli")
    call("j4", "s", "u", {})
    assert seen[0] is None and callable(seen[1])


def test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names():
    """The prompt text a judge call carries must be the prompt the ladder's audit record says (J3 and J4). Reverting either judge in
    judges.py to v1 while flags.py still records v2 makes this fail."""
    c = FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
                  "conflicts": {"flags": [dict(type="conflict", category="treatment_plan_vs_actual", excerpt=PLAN, excerpt_b=OUT)]},
                  "flags": {"flags": [dict(type="causation", category="missed_care", excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")]}})
    fl = F.run_conflict_pass([rec(n) for n in range(1, 10)], call=c) + F.run_flag_pass(rec(8), call=c)
    F.judge_flags(fl, call=c)
    seen = {}
    for f in fl:
        j = f["ladder"]["judge"]
        if j and j["verdict"] != "unavailable":
            seen[f["type"] == "conflict" and "j3" or "j4"] = j["prompt_version"]
    assert set(seen) == {"j3", "j4"}
    for step, pv in seen.items():
        sent = [l["system"] for l in c.log if l["step"] == step]
        assert sent and all(s == promptlib.load(pv).text for s in sent), (step, pv)
