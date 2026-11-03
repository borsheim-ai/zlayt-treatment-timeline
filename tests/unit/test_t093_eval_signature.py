"""T-093 (R-CO-7): the determinism signature covers every field R-CO-7 names, the live runs leave per-run artifacts a failure can be diagnosed from,
and J3 / J4 (judge_conflict_v2 / judge_flag_v2) are measured on seeded wrong and correct items. Fake pipeline only; no model, no network."""
import inspect, json
import pytest
from evals import run as R
from tests.unit.test_eval_runner import Perfect, SAMPLE, report, perfect_control


def first(out, pred):
    return next(f for f in out["flags"] if pred(f))


def on_run2(fn):
    """Mutation applied to the sample's second run only."""
    def mutate(name, out, p):
        if name == "sample" and p.sample_runs == 2:
            fn(out)
    return mutate


def set_(d, k, v):
    d[k] = v


# field -> a mutation of ONE thing in run 2. Each must make determinism < 1.0 and be named in the differences.
MUTATIONS = {
    "record_split:drop_record": ("record_split", lambda o: o["records"].pop()),
    "record_split:source_changed": ("record_split", lambda o: set_(o["records"][0], "source", "Some Other Clinic")),
    "record_split:excerpt_changed": ("record_split", lambda o: set_(o["records"][0], "excerpt", "different text altogether")),
    "parsed_dates:record_date": ("parsed_dates", lambda o: set_(o["records"][0], "date_iso", "2030-01-01")),
    "parsed_dates:record_date_status": ("parsed_dates", lambda o: set_(o["records"][0], "date_status", "ambiguous")),
    "parsed_dates:entry_date": ("entries", lambda o: set_(o["entries"][0], "date", "2030-01-01")),
    "entry_ids:rename": ("entry_ids", lambda o: set_(o["entries"][0], "id", "e_renamed")),
    "entry_ids:extra": ("entry_ids", lambda o: o["entries"].append(dict(o["entries"][0], id="e_extra"))),
    "entries:state": ("entries", lambda o: set_(o["entries"][0], "state", "needs_review")),
    "entries:reasons": ("entries", lambda o: set_(o["entries"][0], "reasons", ["JUDGE_DISAGREES"])),
    "entries:provider": ("entries", lambda o: set_(o["entries"][0], "provider", "Elsewhere")),
    "tray:rejected_entry": ("tray", lambda o: o["tray"].append(dict(record_ids=["r3"], state="rejected", reasons=["UNSUPPORTED"]))),
    "gap_flags:days": ("gap_flags", lambda o: set_(first(o, lambda f: f["type"] == "gap")["computed"], "days", 74)),
    "gap_flags:dropped": ("gap_flags", lambda o: o["flags"].remove(first(o, lambda f: f["type"] == "gap"))),
    "gap_flags:from": ("gap_flags", lambda o: set_(first(o, lambda f: f["type"] == "gap")["computed"], "from", "2030-01-01")),
    "gap_flags:to": ("gap_flags", lambda o: set_(first(o, lambda f: f["type"] == "gap")["computed"], "to", "2030-01-01")),
    "entries:date_status": ("entries", lambda o: set_(o["entries"][0], "date_status", "ambiguous")),
    "entry_ids:removed": ("entry_ids", lambda o: o["entries"].pop(0)),
    "amounts:record_ids": ("amounts", lambda o: set_(o["amounts"][0], "record_ids", ["r98"])),
    "gap_flags:state": ("gap_flags", lambda o: set_(first(o, lambda f: f["type"] == "gap"), "state", "needs_review")),
    "amounts:dropped": ("amounts", lambda o: o["amounts"].pop()),
    "amounts:class": ("amounts", lambda o: set_(o["amounts"][0], "kind", "unclear")),
    "amounts:value": ("amounts", lambda o: set_(o["amounts"][0], "value_cents", 1)),
    "amounts:state": ("amounts", lambda o: set_(o["amounts"][0], "state", "needs_review")),
    "totals:existing_key": ("totals", lambda o: o["totals"]["detected_not_a_total"].update(cents=1)),
    "totals:new_key": ("totals", lambda o: set_(o["totals"], "detected_pending_cents", 1)),
    "flags:type": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation"), "type", "pre_existing")),
    "flags:evidence_record_id": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation")["evidence"][0], "record_id", "r99")),
    "flags:record_ids": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation"), "record_ids", ["r98"])),
    "flags:excerpt": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation")["evidence"][0], "excerpt", "another quote")),
    "flags:category": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation"), "category", "other")),
    "flags:state": ("flags", lambda o: set_(first(o, lambda f: f["type"] == "causation"), "state", "needs_review")),
    "flags:dropped": ("flags", lambda o: o["flags"].remove(first(o, lambda f: f["type"] == "causation"))),
    "flags:extra": ("flags", lambda o: o["flags"].append(dict(id="x", type="conflict", evidence=[dict(record_id="r2", excerpt="x")]))),
}


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_a_mutation_of_each_r_co_7_field_in_one_run_makes_determinism_less_than_one(name):
    field, fn = MUTATIONS[name]
    m = R.live_metrics(Perfect(mutate=on_run2(fn)), "claude-cli", SAMPLE, 3)["determinism_3run"]
    assert m["value"] < 1.0, f"{name} went undetected"
    diffs = m["differences"]
    assert list(diffs) == ["run1_vs_run2"], "only the mutated run differs from run 1"
    assert field in diffs["run1_vs_run2"], f"the report names the field that differs ({field}); got {list(diffs['run1_vs_run2'])}"


def test_unmutated_runs_are_deterministic_and_summary_wording_does_not_count():
    """Summary wording may differ between runs (it is gated by unsupported_count_3run), so a rewrite must not fail determinism."""
    m = R.live_metrics(Perfect(), "claude-cli", SAMPLE, 3)["determinism_3run"]
    assert m["value"] == 1.0 and "differences" not in m
    rewrite = lambda o: [e.update(summary=e["summary"] + " (reworded)") for e in o["entries"]]
    assert R.live_metrics(Perfect(mutate=on_run2(rewrite)), "claude-cli", SAMPLE, 3)["determinism_3run"]["value"] == 1.0


def test_every_mutation_names_a_field_the_signature_has_and_no_key_is_invented():
    fields = set(R.signature_parts(Perfect().run_case(SAMPLE, "claude-cli")))
    assert {f for f, _ in MUTATIONS.values()} <= fields
    assert fields >= {"record_split", "parsed_dates", "entry_ids", "gap_flags", "amounts", "totals", "flags", "entries"}
    src = inspect.getsource(R.signature_parts)
    assert "detected_not_a_total" not in src, "the old signature read a key that run_case never produces"


def test_the_signature_compares_the_whole_totals_dict_of_the_real_shape():
    """The real run_case totals has accepted_cents / detected_pending_cents / status ..., not detected_not_a_total."""
    a = Perfect().run_case(SAMPLE, "claude-cli")
    b = json.loads(json.dumps(a))
    a["totals"], b["totals"] = ({"accepted_cents": 0, "detected_pending_cents": 215000, "amounts_found": 4, "status": "complete", "unclear_items": []} for _ in "ab")
    assert R.signature(a) == R.signature(b)
    b["totals"]["detected_pending_cents"] = 215001
    assert R.signature(a) != R.signature(b)


# ---------------------------------------------------------------- per-run artifacts
def with_ladder(name, out, p):
    for e in out["entries"]:
        e["ladder"] = {"generator": {"prompt_version": "extract_v1", "system": "SECRET SYSTEM PROMPT"},
                       "judge": {"verdict": "supported", "reason_code": "NONE", "prompt_version": "judge_faithfulness_v1", "model": "claude-haiku-5-5", "raw": "SECRET RAW"}}
    for f in out["flags"]:
        f["ladder"] = {"judge": {"verdict": "agree", "reason_code": "NONE", "prompt_version": "judge_flag_v2", "model": "claude-haiku-5-5"}}
    out["errors"] = [{"code": "LLM_FAILED_AFTER_RETRIES", "stage": "judge", "record_no": 3, "message": "secret prompt text"}]


def test_live_metrics_writes_one_artifact_per_run_with_items_states_codes_and_prompt_versions(tmp_path):
    R.live_metrics(Perfect(mutate=with_ladder), "claude-cli", SAMPLE, 3, runs_dir=tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["run1.json", "run2.json", "run3.json"]
    a = json.loads((tmp_path / "run2.json").read_text())
    assert a["run"] == 2 and a["case"] == "sample" and a["backend"] == "claude-cli"
    kinds = {i["kind"] for i in a["items"]}
    assert {"entry", "amount", "flag"} <= kinds
    ent = next(i for i in a["items"] if i["kind"] == "entry")
    assert ent["state"] == "verified" and ent["judge"] == {"verdict": "supported", "reason_code": "NONE", "prompt_version": "judge_faithfulness_v1", "model": "claude-haiku-5-5"}
    assert ent["generator_prompt_version"] == "extract_v1"
    assert any(i["kind"] == "flag" and i["judge"]["prompt_version"] == "judge_flag_v2" for i in a["items"])
    assert a["errors"] == [{"code": "LLM_FAILED_AFTER_RETRIES", "stage": "judge", "record_no": 3}]
    assert a["signature_parts"] == json.loads(json.dumps(R.signature_parts(Perfect(mutate=with_ladder).run_case(SAMPLE, "claude-cli"))))


def test_run_artifacts_hold_no_prompts_no_model_text_and_no_summaries(tmp_path):
    R.live_metrics(Perfect(mutate=with_ladder), "claude-cli", SAMPLE, 3, runs_dir=tmp_path)
    body = "".join(p.read_text() for p in tmp_path.iterdir())
    for needle in ("SECRET SYSTEM PROMPT", "SECRET RAW", "secret prompt text", "ANTHROPIC_API_KEY", "sk-"):
        assert needle not in body
    summary = Perfect().run_case(SAMPLE, "claude-cli")["entries"][0]["summary"]
    assert summary not in body, "summary text is stored as a hash only"


def test_a_secret_looking_value_makes_the_artifact_write_refuse(tmp_path):
    out = Perfect().run_case(SAMPLE, "claude-cli")
    out["flags"][0]["evidence"][0]["excerpt"] = "key " + "sk" + "-" + "x" * 30  # assembled so the repo secret scan does not see a literal
    with pytest.raises(ValueError):
        R.write_run_artifact(tmp_path, "run1", out)
    assert not list(tmp_path.iterdir())


def test_a_determinism_failure_is_diagnosable_from_the_report_and_the_artifacts(tmp_path):
    fn = on_run2(lambda o: o["flags"].remove(first(o, lambda f: f["type"] == "gap")))
    m = R.live_metrics(Perfect(mutate=fn), "claude-cli", SAMPLE, 3, runs_dir=tmp_path)["determinism_3run"]
    d = m["differences"]["run1_vs_run2"]["gap_flags"]
    assert d["only_in_first"] and not d["only_in_other"]
    a1, a2 = (json.loads((tmp_path / f"run{i}.json").read_text()) for i in (1, 2))
    assert len([i for i in a1["items"] if i["kind"] == "flag"]) == len([i for i in a2["items"] if i["kind"] == "flag"]) + 1


def test_build_report_writes_every_case_artifact_and_names_the_directory(tmp_path):
    rd = tmp_path / "runs" / "20261102T000000Z"
    r = report(runs_dir=rd)
    names = {p.stem for p in rd.iterdir()}
    assert {"run1", "run2", "run3", "sample", "case_02_gap_boundaries"} <= names
    assert r["run_artifacts"] == str(rd)
    assert f"per-run artifacts: `{rd}`" in R.render_md(r)


def test_main_writes_artifacts_next_to_the_report_for_a_live_backend(tmp_path):
    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) in (0, 1)
    dirs = list((tmp_path / "runs").iterdir())
    assert len(dirs) == 1 and (dirs[0] / "run3.json").exists() and (dirs[0] / "case_02_gap_boundaries.json").exists()
    assert json.loads((tmp_path / "latest.json").read_text())["run_artifacts"].endswith(dirs[0].name)


def test_fixture_runs_write_no_artifacts(tmp_path):
    R.main(["--backend", "fixture", "--out", str(tmp_path)], pipeline=Perfect("fixture"))
    # T-101: a plain run puts a scratch calibration.json under runs/<ts>/ (so the committed file is untouched); that is the only file allowed there.
    files = [p.relative_to(tmp_path / "runs").as_posix() for p in (tmp_path / "runs").rglob("*") if p.is_file()] if (tmp_path / "runs").exists() else []
    assert [f for f in files if not f.endswith("/calibration.json")] == [], "a fixture run writes no run*.json or per-case artifacts"
    assert json.loads((tmp_path / "latest.json").read_text()).get("run_artifacts") in (None, "")


# ---------------------------------------------------------------- J3 / J4 seeded controls
CONTROLS = R.load_controls()
IN_SAMPLE = [c for c in CONTROLS if c["split"] == "in_sample"]
HELD_OUT = [c for c in CONTROLS if c["split"] == "held_out"]


def test_the_control_file_has_wrong_and_correct_items_for_both_judges():
    assert len({c["id"] for c in CONTROLS}) == len(CONTROLS)
    for j, pos, neg in (("j3", "conflict", "benign"), ("j4", "agree", "disagree")):
        mine = [c for c in CONTROLS if c["judge"] == j]
        assert sum(c["kind"] == "wrong" for c in mine) >= 5 and sum(c["kind"] == "correct" for c in mine) >= 5
        assert all(c.get("why") for c in mine), "every control item, wrong or correct, says why it is labelled as it is"
        assert all(c["synthetic"] is True and c["expected"] == (neg if c["kind"] == "wrong" else pos) for c in mine)


def test_perfect_judges_catch_every_wrong_item_and_accept_every_correct_one():
    m = R.judge_controls_metrics(CONTROLS, perfect_control)
    assert m["status"] == "measured" and m["value"] == 1.0
    for j in ("j3", "j4"):
        assert m[j]["catch_rate"] == 1.0 and m[j]["false_agree"] == [] and m[j]["correct_accepted"] == m[j]["correct_total"] > 0
    assert R.controls_ok(m)


def test_a_judge_that_agrees_with_everything_fails_the_bar_and_names_the_false_agrees():
    r = report(judge_control=lambda i: (R.POSITIVE[i["judge"]], "NONE"))
    jc = r["metrics"]["judge_controls"]
    assert jc["j3"]["catch_rate"] == 0.0 and jc["j4"]["catch_rate"] == 0.0 and jc["j4"]["false_agree"]
    assert r["ship_bar_met"] is False and r["bars"]["4_no_invented_facts"] is False
    assert any(b.startswith("judge_controls") for b in r["blockers"])
    assert "J4 judge_flag_v3 seeded catch rate | 0.000" in R.render_md(r)


def test_one_false_agree_in_one_judge_fails_the_bar():
    leak = next(c["id"] for c in CONTROLS if c["judge"] == "j4" and c["kind"] == "wrong")
    r = report(judge_control=lambda i: ("agree", "NONE") if i["id"] == leak else (i["expected"], "NONE"))
    assert r["metrics"]["judge_controls"]["j4"]["false_agree"] == [leak]
    assert r["ship_bar_met"] is False


def test_a_judge_that_rejects_everything_catches_all_but_the_correct_accept_rate_shows_it():
    r = report(judge_control=lambda i: ({"j3": "benign", "j4": "disagree"}[i["judge"]], "NOT_SUPPORTED_BY_QUOTE"))
    jc = r["metrics"]["judge_controls"]
    assert jc["j4"]["catch_rate"] == 1.0 and jc["j4"]["correct_accepted"] == 0
    assert "correct accepted 0/" in R.render_md(r)


def test_unavailable_judges_make_the_controls_not_measured_and_fail_the_bar():
    r = report(judge_control=lambda i: ("unavailable", "NONE"))
    jc = r["metrics"]["judge_controls"]
    assert jc["status"] == "not_measured" and jc["value"] is None and jc["j4"]["wrong_caught"] == 0
    assert r["ship_bar_met"] is False


def test_no_judge_control_supplied_is_not_measured_and_fails_the_bar():
    r = R.build_report(Perfect(), "claude-cli", lexicon_flags=__import__("tests.unit.test_eval_runner", fromlist=["gold_floor"]).gold_floor)
    assert r["metrics"]["judge_controls"]["status"] == "not_measured" and r["ship_bar_met"] is False


def test_default_judge_control_returns_unavailable_when_the_fixture_is_missing(monkeypatch):
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    v, code = R.default_judge_control("fixture")(next(c for c in CONTROLS if c["judge"] == "j4"))
    assert v == "unavailable"


# ---------------------------------------------------------------- T-093 round 2: matched pairs, fixed labels, repeats, in-sample vs held-out
STOP = {"the", "and", "for", "with", "was", "were", "has", "had", "not", "any", "all", "per", "after", "from", "this", "that", "patient", "visit", "plan", "care"}


def words(t):
    import re
    return {w for w in re.findall(r"[a-z]{3,}", t.lower())} - STOP


def test_a_held_out_set_exists_for_both_judges_and_never_duplicates_an_in_sample_quote():
    assert {c["judge"] for c in HELD_OUT} == {"j3", "j4"} and all(c["id"][0] == "H" for c in HELD_OUT)
    seen = {(c.get("excerpt_a") or c["excerpt"], c.get("excerpt_b")) for c in IN_SAMPLE}
    assert not [c["id"] for c in HELD_OUT if (c.get("excerpt_a") or c["excerpt"], c.get("excerpt_b")) in seen]


def test_the_report_labels_in_sample_and_held_out_controls_and_lists_every_item_per_run():
    r = report(judge_control=perfect_control)
    jc = r["metrics"]["judge_controls"]
    assert set(jc["j3"]["by_split"]) == {"in_sample", "held_out"} and jc["j3"]["by_split"]["held_out"]["wrong_total"] >= 2
    md = R.render_md(r)
    assert "In-sample controls were written with the prompts they test" in md and "held-out" in md and "| J3R1 | j3 |" in md
    assert all(len(row["verdicts"]) == jc["repeats"] for row in jc["rows"])


def test_a_judge_that_flips_one_item_on_run_two_fails_the_gate_and_is_named_unstable():
    calls = {}
    flip = next(c["id"] for c in CONTROLS if c["judge"] == "j3" and c["kind"] == "wrong")

    def judge(i):
        calls[i["id"]] = calls.get(i["id"], 0) + 1
        if i["id"] == flip and calls[i["id"]] == 2:
            return "conflict", "FACT_MISMATCH"
        return perfect_control(i)
    jc = R.judge_controls_metrics(CONTROLS, judge, repeats=3)
    assert jc["j3"]["false_agree"] == [flip] and jc["j3"]["unstable"] == [flip] and not R.controls_ok(jc)
    row = next(r for r in jc["rows"] if r["id"] == flip)
    assert row["verdicts"] == ["benign", "conflict", "benign"] or row["verdicts"][1] == "conflict"


def test_a_correct_item_the_judge_confirms_on_only_some_runs_is_not_counted_as_accepted():
    calls = {}
    item = next(c["id"] for c in CONTROLS if c["judge"] == "j4" and c["kind"] == "correct")

    def judge(i):
        calls[i["id"]] = calls.get(i["id"], 0) + 1
        return ("disagree", "NONE") if i["id"] == item and calls[i["id"]] == 3 else perfect_control(i)
    jc = R.judge_controls_metrics(CONTROLS, judge, repeats=3)
    assert jc["j4"]["correct_accepted"] == jc["j4"]["correct_total"] - 1 and jc["j4"]["unstable"] == [item]
    assert R.controls_ok(jc), "over-rejection is reported, not gated (D-046 gates catches and false agrees only)"


def test_live_backends_judge_every_control_three_times_and_other_backends_once():
    seen = []

    def count(i):
        seen.append(i["id"])
        return perfect_control(i)
    report(judge_control=count)                                                       # helper default backend is claude-cli (live)
    assert len(seen) == 3 * len(CONTROLS)
    seen.clear()
    R.build_report(Perfect("fixture"), "fixture", lexicon_flags=__import__("tests.unit.test_eval_runner", fromlist=["gold_floor"]).gold_floor, judge_control=count)
    assert len(seen) == len(CONTROLS), "fixture backend: one repeat"


# ---------------------------------------------------------------- T-093 round 3: the gate is "every" (D-046), arithmetic is code's, J3C10 reason
def jc_with(j3_caught, j3_total, j4_caught=12, j4_total=12, false3=(), status="measured"):
    one = lambda c, t, fa=(): {"wrong_total": t, "wrong_caught": c, "catch_rate": c / t, "false_agree": list(fa)}
    return {"status": status, "j3": one(j3_caught, j3_total, false3), "j4": one(j4_caught, j4_total)}


def test_the_controls_gate_is_every_wrong_item_not_a_rate():
    """D-046 / spec section 7 row 4: one missed wrong item fails the gate however large the set (19 x 0.95 = 18.05 only failed 18/19 by rounding)."""
    assert R.controls_ok(jc_with(19, 19)) and R.controls_ok(jc_with(20, 20))
    assert not R.controls_ok(jc_with(18, 19, false3=["J3W11"]))
    assert not R.controls_ok(jc_with(19, 20)), "19/20 is 0.95, which the old hallucination bar passed"
    assert not R.controls_ok(jc_with(99, 100)), "a larger set may not hide a miss"
    assert not R.controls_ok(jc_with(19, 19, j4_caught=11)) and not R.controls_ok(jc_with(19, 19, status="not_measured"))
    assert not R.controls_ok(jc_with(0, 1) | {"j3": {"wrong_total": 0, "wrong_caught": 0, "catch_rate": None, "false_agree": []}}), "an empty wrong set measures nothing"


def test_the_gate_does_not_read_the_catch_rate_threshold():
    """Mutation guard: the threshold constant is not what gates controls (a rate of 0.99 with a miss is still a fail)."""
    jc = jc_with(99, 100)
    jc["j3"]["catch_rate"] = 1.0
    assert not R.controls_ok(jc), "the gate counts items, not the reported rate"


def test_the_report_states_the_gate_as_every_wrong_item():
    md = R.render_md(report(judge_control=perfect_control))
    assert "all wrong caught, 0 false agree" in md


def test_code_resolves_frequency_times_duration_against_a_visit_count():
    """The pairs removed from the J3 controls (J3W10/J3C6, H3W1/H3C1), now tested against T-094's candidate code: the sums are code's."""
    from app.backend import conflict_candidates as CC

    def total(text):
        return CC.plans([dict(n=1, source="s", excerpt=text, date_iso="2026-01-10")])[0]["visits"]
    two_x_six = total("Physical therapy 2x/week for 6 weeks.")
    assert two_x_six == 12 == total("Physical therapy plan of care: 12 visits.")          # was J3W10: the two plans agree
    assert two_x_six != total("Physical therapy plan of care: 10 visits.")                  # was J3C6: 12 against 10 is a difference
    assert total("Chiropractic 2x/week for 4 weeks.") == 8 == total("Plan: 8 visits authorized.")   # was H3W1
    assert total("Chiropractic 3x/week for 4 weeks.") == 12 != 8                            # was H3C1


def test_agreeing_totals_make_no_candidate_and_differing_totals_are_both_stated_to_the_judge_as_arithmetic_notes():
    from app.backend import conflict_candidates as CC
    R_ = lambda n, t, d: dict(n=n, source="s", excerpt=t, date_iso=d)
    end = R_(3, "Discharged from PT after two missed appointments.", "2026-03-01")
    agree = CC.candidates([R_(1, "Physical therapy 2x/week for 6 weeks.", "2026-01-10"), R_(2, "Physical therapy plan of care: 12 visits.", "2026-01-12"), end])
    assert [(c["a"].record_no, c["b"].record_no) for c in agree] == [(2, 3)], "the explicit count is the one plan quoted; 2x6 and 12 are not paired with each other"
    assert "2 per week x 6 weeks = 12 visits" in agree[0]["arithmetic"] and "12 visits" in agree[0]["arithmetic"]
    differ = CC.candidates([R_(1, "Physical therapy 2x/week for 6 weeks.", "2026-01-10"), R_(2, "Physical therapy plan of care: 10 visits.", "2026-01-12"), end])
    assert "2 per week x 6 weeks = 12 visits" in differ[0]["arithmetic"] and "10 visits" in differ[0]["arithmetic"], "both totals are stated, by code, next to the pair"


def test_audit_prompt_ids_equal_the_ids_judges_py_sends():
    """T-093 r2 F-1: the audit row names the prompt id judges.py loads (one source), and the prompt file exists."""
    import re
    from app.llm import audited
    src = (R.ROOT / "app" / "backend" / "judges.py").read_text()
    sent = dict(re.findall(r'_run\("(j\d)", "([a-z_0-9]+)"', src))
    assert sent and all(audited.PROMPT_OF_STEP[k] == v for k, v in sent.items()), (sent, audited.PROMPT_OF_STEP)
    assert all((R.ROOT / "app" / "llm" / "prompts" / f"{v}.md").exists() for v in sent.values())
    assert R.control_prompt("j3") == sent["j3"] and R.control_prompt("j4") == sent["j4"]


def test_controls_report_header_names_the_source_commit_and_whether_the_tree_was_clean(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "git_source", lambda root=R.ROOT: {"commit": "abc123", "clean": True, "tree": "def456", "dirty": []})
    monkeypatch.setattr(R, "default_judge_control", lambda backend: perfect_control)
    assert R.run_controls_only("fixture", tmp_path, "20260101T000000Z") == 0
    md = (tmp_path / "controls-20260101T000000Z.md").read_text()
    js = json.loads((tmp_path / "controls-20260101T000000Z.json").read_text())
    assert "Source commit `abc123`, tree clean" in md and js["source_commit"] == "abc123" and js["source_tree_clean"] is True
    monkeypatch.setattr(R, "git_source", lambda root=R.ROOT: {"commit": "abc123", "clean": False, "tree": "x", "dirty": [" M app/x.py"]})
    R.run_controls_only("fixture", tmp_path, "20260101T000001Z")
    assert "DIRTY, not reproducible" in (tmp_path / "controls-20260101T000001Z.md").read_text()


def test_the_changelog_records_the_round_4_rebuild_from_candidates_and_the_history_of_the_old_ids():
    cl = (R.ROOT / "evals" / "golden" / "judge_controls.CHANGELOG.md").read_text()
    for needle in ("round 4", "conflict_candidates", "J3C10", "J3W1", "J3W11", "035750Z", "FACT_MISMATCH", "undated", "not proposed", "evals/j3_controls.py", "J4W7", "locked"):
        assert needle in cl, f"the changelog must mention {needle}"
