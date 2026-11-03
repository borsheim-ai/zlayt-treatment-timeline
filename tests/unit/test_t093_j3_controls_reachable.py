"""T-093 r4 (staff-engineer r3 major 1): every J3 control input is a pair the shipped candidate generator proposes.
Deterministic: runs app.backend.conflict_candidates over the control records and the golden and library packets. No model, no network."""
import json
import re

from app.backend import conflict_candidates as CC
from evals import j3_controls as J
from evals import run as R

CONTROLS = R.load_controls()
J3 = [c for c in CONTROLS if c["judge"] == "j3"]


def proposed(records, rule, category, qa, qb, nos=None):
    """The candidates(records) entries equal to the control's pair (rule, category and both quotes, optionally the record numbers)."""
    return [c for c in CC.candidates(records) if c["rule"] == rule and c["category"] == category and c["a"].text == qa and c["b"].text == qb
            and (nos is None or (c["a"].record_no, c["b"].record_no) == tuple(nos))]


def unreachable(rows, candidates_fn=CC.candidates):
    """ids of J3 controls whose pair candidates_fn does not propose from the control's own records."""
    out = []
    for r in rows:
        got = [c for c in candidates_fn(r["records"]) if (c["rule"], c["category"], c["a"].text, c["b"].text) == (r["rule"], r["category"], r["excerpt_a"], r["excerpt_b"])]
        if not got:
            out.append(r["id"])
    return out


def test_every_j3_control_input_is_producible_by_the_candidate_generator():
    assert J3 and unreachable(J3) == []
    for r in J3:
        texts = {rec["excerpt"] for rec in r["records"]}
        assert any(r["excerpt_a"] in t for t in texts) and any(r["excerpt_b"] in t for t in texts), f"{r['id']}: quotes are not cut from its records"
        assert len(proposed(r["records"], r["rule"], r["category"], r["excerpt_a"], r["excerpt_b"])) == 1, f"{r['id']}: proposed exactly once"


def test_the_reachability_check_goes_red_when_a_candidate_rule_is_removed():
    """Mutation: with the denial rule removed (or the plan rule), the controls that rest on it are named unreachable."""
    no_denial = lambda recs: CC.plan_vs_outcome(recs)
    no_plan = lambda recs: CC.history_denials(recs)
    lost_d, lost_p = unreachable(J3, no_denial), unreachable(J3, no_plan)
    assert lost_d and all(next(r for r in J3 if r["id"] == i)["rule"] == "history_denial" for i in lost_d)
    assert lost_p and all(next(r for r in J3 if r["id"] == i)["rule"] == "plan_vs_outcome" for i in lost_p)
    assert set(lost_d) | set(lost_p) == {r["id"] for r in J3}


def test_real_candidates_are_the_ones_the_generator_proposes_on_the_golden_and_library_packets_and_all_of_them_are_controls():
    real = [r for r in J3 if r["origin"] == "packet"]
    from_gen = {(p, c["a"].record_no, c["b"].record_no, c["a"].text, c["b"].text) for p, c in J.packet_candidates()}
    from_rows = {(r["packet"], *r["packet_record_nos"], r["excerpt_a"], r["excerpt_b"]) for r in real}
    assert from_gen == from_rows, "a new or removed candidate on a golden/library packet must be added to (or dropped from) the controls with a locked label"
    for r in real:
        recs = {x["n"]: x for x in J.packet_records(J.ROOT / r["packet"])}
        for rec in r["records"]:
            assert (rec["excerpt"], rec["date_iso"]) == (recs[rec["n"]]["excerpt"], recs[rec["n"]].get("date_iso")), f"{r['id']}: stored record {rec['n']} drifted from the packet"
        assert proposed(list(recs.values()), r["rule"], r["category"], r["excerpt_a"], r["excerpt_b"], r["packet_record_nos"])


def test_every_variant_derives_from_a_real_candidate_of_the_same_rule_and_changes_a_quote():
    by = {r["id"]: r for r in J3}
    for r in (r for r in J3 if r["origin"] == "variant"):
        src = by[r["derived_from"]]
        assert src["origin"] == "packet" and src["rule"] == r["rule"] and src["category"] == r["category"]
        assert (r["excerpt_a"], r["excerpt_b"]) != (src["excerpt_a"], src["excerpt_b"])


def test_the_j3_set_has_real_candidates_and_variants_of_both_rules_and_both_kinds_in_both_splits():
    assert sum(r["origin"] == "packet" for r in J3) >= 4 and sum(r["origin"] == "variant" for r in J3) >= 20
    for split in ("in_sample", "held_out"):
        for rule in ("plan_vs_outcome", "history_denial"):
            kinds = {r["kind"] for r in J3 if r["split"] == split and r["rule"] == rule}
            assert kinds == {"wrong", "correct"}, f"{split}/{rule} needs wrong and correct items"
    assert sum(r["kind"] == "wrong" for r in J3) >= 15


def test_every_wrong_item_has_a_correct_twin_that_shares_its_first_quote():
    """The twin may sit in the other split: J3V17..J3V19 moved from held_out to in_sample (T-113 r2) and keep their held-out twins, which is enough to stop a topic-only pass."""
    for r in (r for r in J3 if r["kind"] == "wrong"):
        twins = [t for t in J3 if t["kind"] == "correct" and t["excerpt_a"] == r["excerpt_a"]]
        assert twins, f"{r['id']} has no contradictory twin on the same first quote: a judge could pass it by topic alone"


# labels, locked before the first live run of this set (D-046). Editing a label means editing this table in the same diff, where a reviewer sees it.
LOCKED = {
    "J3R1": "correct", "J3R2": "correct", "J3R3": "correct", "J3R4": "wrong", "J3R5": "correct", "J3R6": "correct", "J3R7": "correct", "J3V20": "wrong",       # T-141: new, labels fixed before any run
    "J3V1": "wrong", "J3V2": "wrong", "J3V3": "wrong", "J3V4": "correct", "J3V5": "wrong", "J3V6": "correct",
    "J3V7": "wrong", "J3V10": "wrong", "J3V11": "correct", "J3V12": "correct", "J3V14": "wrong", "J3V15": "wrong", "J3V16": "wrong",
    "J3V17": "wrong", "J3V18": "wrong", "J3V19": "wrong",                    # T-113 r2: were H3V16, H3V1, H3V3 (held_out) -> in_sample, labels unchanged
    "H3V2": "correct", "H3V4": "correct", "H3V5": "correct", "H3V6": "correct",
    "H3V17": "wrong", "H3V18": "correct", "H3V19": "wrong", "H3V20": "correct", "H3V21": "wrong",       # T-113 r2: new held-out, committed before any run
    "H3V8": "correct", "H3V9": "wrong", "H3V10": "correct", "H3V11": "wrong", "H3V12": "correct", "H3V13": "wrong", "H3V14": "correct", "H3V15": "correct",
}


def test_j3_labels_are_the_locked_ones_and_every_item_gives_its_reason():
    assert {r["id"]: r["kind"] for r in J3} == LOCKED
    assert all(r["expected"] == ("benign" if r["kind"] == "wrong" else "conflict") and len(r["why"]) > 25 for r in J3)


def test_the_committed_control_files_equal_the_build_and_the_j4_rows_are_untouched():
    assert J.main(["--check"]) == 0
    j4 = {c["id"]: c for c in CONTROLS if c["judge"] == "j4"}
    assert sum(c["kind"] == "wrong" for c in j4.values()) == 12 and len(j4) == 27, "J4 rows are kept as they were (T-093 r3: 12 wrong, 15 correct)"
    w7 = j4["J4W7"]
    assert (w7["category"], w7["expected"], w7["kind"], w7["excerpt"]) == ("missed_care", "disagree", "wrong", "Patient walked at the scene and declined ambulance transport.")


def test_no_frequency_plan_control_asks_the_judge_to_count_visits():
    """LLM_VS_CODE row 1 (r3 M-3): where the first quote is a frequency x duration plan, the second states no visit count, so no label needs a multiplication.
    (Arithmetic itself is tested against CC.plans in test_t093_eval_signature.)"""
    for r in J3:
        if r["rule"] != "plan_vs_outcome":
            continue
        plan = CC.plans([{"n": 1, "excerpt": r["excerpt_a"], "date_iso": "2026-01-01"}])
        if plan and plan[0]["kind"] == "freq":
            assert not CC._VISITS.search(r["excerpt_b"]), f"{r['id']}: the outcome states a visit count against a frequency plan"


def test_controls_json_keeps_the_gate_every_wrong_item_with_the_new_set():
    m = R.judge_controls_metrics(CONTROLS, lambda i: (i["expected"], "NONE"))
    assert R.controls_ok(m) and m["j3"]["wrong_total"] == sum(r["kind"] == "wrong" for r in J3)
    leak = next(r["id"] for r in J3 if r["kind"] == "wrong")
    bad = R.judge_controls_metrics(CONTROLS, lambda i: ("conflict", "FACT_MISMATCH") if i["id"] == leak else (i["expected"], "NONE"))
    assert not R.controls_ok(bad) and bad["j3"]["false_agree"] == [leak]
    assert all(json.dumps(r["origin"]) for r in m["rows"] if r["judge"] == "j3") and {r["origin"] for r in m["rows"] if r["judge"] == "j3"} == {"packet", "variant"}


def test_the_rendered_report_says_where_the_j3_inputs_come_from():
    md = "\n".join(R.render_control_items(R.judge_controls_metrics(CONTROLS, lambda i: (i["expected"], "NONE"))))
    assert "conflict_candidates.py" in md and "| origin |" in md and re.search(r"\| J3R1 \| j3 \| in-sample \| correct \| .* \| packet \|", md)
