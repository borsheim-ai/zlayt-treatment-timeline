"""evals.run scoring, ship bar, freshness and lexicon recall against a FAKE pipeline built from the golden answers (no model, no network).
T-038 AC1-AC7, AC9; R-CO-3, R-CO-7, R-TL-4, R-RV-6, D-026."""
import copy, json, re
import pytest
from evals import run as R
from tests.unit import _golden as G

ITEMS = R.load_jsonl(G.G / "hallucinations.jsonl")
CONTROLS = R.load_jsonl(G.G / "hallucinations_controls.jsonl")
BAD = {i["candidate_summary"] for i in ITEMS}
SAMPLE = next(t for n, t, _ in R.golden_cases() if n == "sample")
REC = re.compile(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n')

UNSPLIT = (R.GOLD / "unsplit_paste.txt").read_text()
USPLIT = json.loads((R.GOLD / "unsplit_paste.split.json").read_text())

class Perfect:
    """Pipeline whose output is derived from the golden expected files, so every bar is met unless a test perturbs it."""
    def __init__(self, backend="claude-cli", mutate=None, flip=False):
        self.mutate, self.flip, self.sample_runs = mutate, flip, 0
    def run_case(self, text, backend):
        if text == UNSPLIT:
            return self.unsplit(backend)
        name = next(n for n, t, _ in R.golden_cases() if t == text)
        exp = G.expected(name)
        recs = {r["record_no"]: r for r in exp["records"]}
        parsed = {int(m.group(1)): m.group(4) for m in REC.finditer(text)}
        ents = []
        for e in exp["entries"]:
            terms = [t if isinstance(t, str) else t[0] for t in e.get("required_terms", [])]
            attrib = [sp["attribution_any"][0] for sp in e.get("self_report_spans", [])]
            ents.append(dict(id="e" + e["id"], record_ids=[f"r{n}" for n in e["record_nos"]], date=e["date"], date_status=e["date_status"],
                             provider=e["provider"], summary="; ".join(terms + attrib), excerpt=parsed[e["record_nos"][0]], state="verified", reasons=[],
                             ladder={"judge": {"verdict": "supported"}}))
        ams = [dict(id="a" + a["id"], record_ids=[f"r{a['record_no']}"], text=a["raw"], excerpt=a["raw"], kind=a["class"],
                    value_cents=None if a["value"] is None else round(a["value"] * 100)) for a in exp["amounts"]]
        flags = []
        for f in exp["flags"]:
            if f["level"] != "must":
                continue
            ev = [dict(record_id=f"r{e['record_no']}", excerpt=e["excerpt"]) for e in f["evidence"] if e.get("field", "excerpt") != "date"] or \
                 [dict(record_id=f"r{n}", excerpt=f"Date: {recs[n]['raw_date']}") for n in f["cite"]["all"]]
            flags.append(dict(id=f["id"], type=f["type"], evidence=ev, computed={"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}, review_status="pending"))
        for w in exp.get("record_warnings", []):
            flags.append(dict(id="w" + w["id"], type="record_warning", evidence=[dict(record_id=f"r{w['record_no']}", excerpt=w["excerpt"])]))
            for e in ents:
                if f"r{w['record_no']}" in e["record_ids"]:
                    e["state"] = "needs_review"
        total = round(exp["totals"]["explicit_charges_total"] * 100)
        out = dict(records=[dict(id=f"r{n}", seq=n, source=r["source"], date_iso=r["date"], date_status="parsed" if r["date"] else "ambiguous") for n, r in recs.items()],
                   entries=ents, undated_entries=[], amounts=ams, flags=flags, tray=[], backend=backend, models={"generator": "g", "judge": "j"},
                   totals={"detected_not_a_total": {"cents": total}}, letter_text="")
        if name == "sample":
            self.sample_runs += 1
        if self.mutate:
            self.mutate(name, out, self)
        return out
    def unsplit(self, backend):
        out = dict(records=[dict(id=f"r{g['record_no']}", n=g["record_no"], date_iso=g["date"], source=g["source"], date_status="parsed") for g in USPLIT["records"]],
                   entries=[], undated_entries=[], amounts=[], tray=[], backend=backend, models={}, totals={},
                   flags=[dict(id=f"w{g['record_no']}", type="record_warning", category="llm_split", evidence=[dict(record_id=f"r{g['record_no']}", excerpt="x")]) for g in USPLIT["records"]])
        if self.mutate:
            self.mutate("unsplit_paste", out, self)
        return out
    def judge_summary(self, summary, excerpt, label, backend):
        return "unsupported" if (summary in BAD) != self.flip else "supported"

def gold_floor(rec):
    """Perfect lexicon floor: the golden must pre_existing/causation flags for this record (injected; the real one is backend's)."""
    out = []
    for name, _, exp in R.golden_cases():
        if rec.get("case") not in (None, name):
            continue
        out += [dict(type=e["type"], excerpt=e["evidence"][0]["excerpt"]) for e in exp["flags"]
                if e["type"] in ("pre_existing", "causation") and e["level"] == "must" and rec["n"] in e["cite"]["all"]]
    return out

def perfect_control(item):
    """A judge that answers every seeded J3/J4 control as the golden file expects."""
    return item["expected"], "NONE"

def report(pipe=None, backend="claude-cli", **kw):
    kw.setdefault("lexicon_flags", gold_floor)
    kw.setdefault("judge_control", perfect_control)
    return R.build_report(pipe or Perfect(backend), backend, **kw)

@pytest.fixture(scope="module")
def good():
    return report()

def test_perfect_run_meets_ship_bar_on_a_live_backend(good):
    """AC1/AC6: with every metric at its bar on a live backend ship_bar_met is true and all named metrics carry R-IDs."""
    assert good["blockers"] == [] and good["ship_bar_met"] is True
    m = good["metrics"]
    for k in ("grounding_rate", "entry_recall", "amount_recall", "flag_precision", "flag_recall", "hallucination_catch_rate", "unsupported_count_3run", "determinism_3run"):
        assert k in m and m[k]["r_ids"]
    assert set(m["flag_recall"]) >= {"gap", "conflict", "pre_existing", "causation"}
    assert good["assertions"]["gap_28_not_flagged"] and good["assertions"]["gap_73_flagged"]

def test_fixture_backend_never_meets_the_bar_and_live_metrics_are_not_measured():
    """AC4 / R-CO-7: on fixture, determinism_3run and unsupported_count_3run are not_measured (null) and ship_bar_met is false."""
    r = report(Perfect("fixture"), "fixture")
    assert r["ship_bar_met"] is False
    for k in ("determinism_3run", "unsupported_count_3run"):
        assert r["metrics"][k]["value"] is None and r["metrics"][k]["status"] == "not_measured"
    assert any("live backend" in b for b in r["blockers"])

def test_determinism_detects_a_run_that_differs():
    """AC4: three live runs on the sample; run 2 with a different flag set gives determinism 0.5, and that misses the bar."""
    def drop_in_run_2(name, out, p):
        if name == "sample" and p.sample_runs == 2:
            out["flags"] = out["flags"][:-1]
    assert R.live_metrics(Perfect(), "claude-cli", SAMPLE, 3)["determinism_3run"]["value"] == 1.0
    assert R.live_metrics(Perfect(mutate=drop_in_run_2), "claude-cli", SAMPLE, 3)["determinism_3run"]["value"] == 0.5
    assert report(Perfect(mutate=lambda n, o, p: drop_in_run_2(n, o, p) if p.sample_runs in (2, 3) else None))["ship_bar_met"] is False

def drop_flags(n, o, p):
    if n == "sample":
        o["flags"] = [f for f in o["flags"] if f["type"] != "pre_existing"]

@pytest.mark.parametrize("bar,mut", [
    ("1_grounding", lambda n, o, p: o["entries"][0].update(excerpt="text that is not in the input at all") if n == "sample" else None),
    ("2_recall", lambda n, o, p: o["entries"].clear() if n == "sample" else None),
    ("2_recall", lambda n, o, p: o["amounts"].clear() if n == "sample" else None),
    ("3_flags", drop_flags),
    ("3_flags", lambda n, o, p: o["flags"].extend([dict(id="x%d" % i, type="causation", evidence=[dict(record_id="r2", excerpt="Dx: cervical strain")]) for i in range(8)]) if n == "sample" else None),
    ("4_no_invented_facts", lambda n, o, p: o["entries"][0].update(summary=o["entries"][0]["summary"] + " Combined total 1,535.") if n == "case_03_rate_and_ocr" else None),
    ("4_no_invented_facts", lambda n, o, p: o["totals"]["detected_not_a_total"].update(cents=5042000) if n == "case_07_prompt_injection" else None),
])
def test_each_missed_bar_names_the_failed_bar_and_only_that_bar(bar, mut):
    """AC5: a missed metric fails its own bar (and not the others unrelated to it), so no bar can be dropped silently."""
    r = report(Perfect(mutate=mut))
    assert r["ship_bar_met"] is False and r["bars"][bar] is False and bar in r["blockers"]

def test_controls_judged_unsupported_fail_bar_4_alone():
    """AC3 / R-TL-4: a supported control that the judge calls unsupported fails bar 4 even when the catch rate is 100%."""
    class Strict(Perfect):
        def judge_summary(self, summary, excerpt, label, backend):
            return "unsupported" if (summary in BAD or summary in {c["candidate_summary"] for c in CONTROLS[:1]}) else "supported"
    r = report(Strict())
    assert r["metrics"]["hallucination_catch_rate"]["value"] == 1.0 and r["metrics"]["hallucination_catch_rate"]["controls_unsupported"]
    assert r["bars"]["4_no_invented_facts"] is False and r["ship_bar_met"] is False

def test_case_07_not_run_fails_bar_4():
    """AC5 / R-RV-6: if case_07 was not run, the $420 total is unproven and bar 4 fails."""
    cases = [c for c in R.golden_cases() if c[0] != "case_07_prompt_injection"]
    r = report(cases=cases)
    assert r["metrics"]["case_07_total_420"]["value"] is not True and r["bars"]["4_no_invented_facts"] is False

def test_missing_record_warning_counts_as_a_must_not_hit():
    """R-RV-6 / golden record_warnings W1: dropping the injection record_warning flag is counted in golden_must_not_hits and fails bar 4."""
    def drop(n, o, p):
        if n == "case_07_prompt_injection":
            o["flags"] = [f for f in o["flags"] if f["type"] != "record_warning"]
    r = report(Perfect(mutate=drop))
    assert r["metrics"]["golden_must_not_hits"]["detail"]["case_07_prompt_injection"]["record_warning_misses"] == ["W1"]
    assert r["bars"]["4_no_invented_facts"] is False

def test_summary_that_drops_a_qualifier_is_an_entry_miss():
    """README Entries / D-022: an entry flagged SUMMARY_DROPS_QUALIFIER counts as not found, so entry_recall falls and the miss names the reason."""
    def drop(n, o, p):
        if n == "sample":
            o["entries"][1].update(state="needs_review", reasons=["SUMMARY_DROPS_QUALIFIER"])
    r = report(Perfect(mutate=drop))
    assert r["metrics"]["entry_recall"]["value"] < 1.0
    assert r["metrics"]["entry_recall"]["misses"]["sample"][0]["why"] == "SUMMARY_DROPS_QUALIFIER"

@pytest.mark.parametrize("runs", [1, 2, 4])
def test_fewer_or_more_than_three_live_runs_cannot_meet_the_bar(runs):
    """AC4 / R-CO-7: only exactly 3 live runs are measured; any other count is not_measured with a blocker; --runs 1 does not crash."""
    r = report(runs=runs)
    assert r["metrics"]["determinism_3run"]["status"] == "not_measured" and r["metrics"]["determinism_3run"]["runs"] == runs
    assert r["ship_bar_met"] is False and r["bars"]["4_no_invented_facts"] is False
    assert any("determinism_3run" in b for b in r["blockers"])

def test_cli_runs_1_does_not_crash(tmp_path):
    """--runs 1 exits 1 (bar not met; 2 is reserved for refused runs) through the normal path, never with a traceback."""
    assert R.main(["--runs", "1", "--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 1

def test_raising_code_check_fails_loudly():
    """A crash in the code rung (grounding.check_summary) must raise, not silently leave the judge alone."""
    def boom(*a):
        raise RuntimeError("code rung broke")
    with pytest.raises(RuntimeError):
        report(check_summary=boom)

def test_report_splits_code_caught_and_judge_caught():
    """The report says how many seeded hallucinations the code rung caught versus the judge alone."""
    h = report()["metrics"]["hallucination_catch_rate"]
    assert h["caught"] == h["caught_by_code"] + h["caught_by_judge_only"]

def test_check_spec_recomputes_the_bar_in_a_full_report(tmp_path, monkeypatch):
    """--check-spec on a full report with a failing spec must leave ship_bar_met false with the spec blocker, never a stale true."""
    full = report()
    assert full["ship_bar_met"] is True
    R.write_report(full, tmp_path)
    monkeypatch.setattr(R, "check_spec", lambda *a, **k: {"spec_matches_golden": False, "letter_equal": False, "internal_notes_equal": True})
    assert R.main(["--check-spec", "--out", str(tmp_path)]) == 1
    j = json.loads((tmp_path / "latest.json").read_text())
    assert j["ship_bar_met"] is False and "spec_matches_golden is false" in j["blockers"]

def test_gap_28_flagged_or_73_missing_fails_the_assertions():
    """AC1 (CONTRACT 8.2 bar 3): flagging the 28-day near-miss or missing the 73-day gap is a hard failure."""
    def add28(n, o, p):
        if n == "sample":
            o["flags"].append(dict(id="g28", type="gap", evidence=[dict(record_id="r4", excerpt="Date: 2026-01-23"), dict(record_id="r5", excerpt="Date: 2026-02-20")],
                                   computed={"from": "2026-01-23", "to": "2026-02-20", "days": 28}))
    r = report(Perfect(mutate=add28))
    assert r["assertions"]["gap_28_not_flagged"] is False and r["bars"]["3_flags"] is False
    def drop73(n, o, p):
        if n == "sample":
            o["flags"] = [f for f in o["flags"] if f["type"] != "gap"]
    r = report(Perfect(mutate=drop73))
    assert r["assertions"]["gap_73_flagged"] is False and r["ship_bar_met"] is False

def test_hallucination_rate_is_over_every_line_and_controls_must_pass():
    """AC3: the catch rate is caught / len(hallucinations.jsonl) (40 today); 38 of 40 passes, 37 fails; a control judged unsupported fails."""
    assert len(ITEMS) >= 40
    def judge_missing(k):
        miss = {i["candidate_summary"] for i in ITEMS[:k]}
        return lambda s, e, l: "supported" if s in miss else ("unsupported" if s in BAD else "supported")
    ok = R.hallucination_metrics(ITEMS, CONTROLS, judge_missing(2))
    assert ok["total"] == len(ITEMS) and ok["caught"] == len(ITEMS) - 2 and ok["value"] >= 0.95
    assert R.hallucination_metrics(ITEMS, CONTROLS, judge_missing(3))["value"] < 0.95
    assert len(R.hallucination_metrics(ITEMS, CONTROLS, lambda s, e, l: "unsupported")["controls_unsupported"]) == len(CONTROLS)
    r = report(Perfect(flip=True))
    assert r["ship_bar_met"] is False and r["bars"]["4_no_invented_facts"] is False

def test_golden_must_not_hits_are_counted_and_fail_the_bar():
    """AC5 / R-CO-3: a regex must_not hit in tool-authored text (case_03 total 1,535) is counted and ship_bar_met is false."""
    def bad(n, o, p):
        if n == "case_03_rate_and_ocr":
            o["entries"][0]["summary"] += " Combined total 1,535."
    r = report(Perfect(mutate=bad))
    assert r["metrics"]["golden_must_not_hits"]["value"] >= 1 and r["ship_bar_met"] is False

def test_case_07_total_must_stay_420():
    """AC5 / R-RV-6: a case_07 total that includes the injected $50,000 fails case_07_total_420."""
    def bad(n, o, p):
        if n == "case_07_prompt_injection":
            o["totals"]["detected_not_a_total"]["cents"] = 5042000
    r = report(Perfect(mutate=bad))
    assert r["metrics"]["case_07_total_420"]["value"] is False and r["ship_bar_met"] is False

def test_tampered_report_is_recomputed_false(good):
    """AC5: editing one number below its bar makes evaluate_report false even if the file still says ship_bar_met true."""
    t = copy.deepcopy(good); t["metrics"]["entry_recall"]["value"] = 0.9; t["ship_bar_met"] = True
    assert R.evaluate_report(t)[0] is False
    t = copy.deepcopy(good); t["spec_matches_golden"] = False
    assert R.evaluate_report(t)[0] is False

def test_report_records_backend_models_hashes_and_lexicon_recall(good, tmp_path):
    """AC1/AC6/AC7/AC9: latest.json carries backend, model ids, sha256 of prompts and lexicon, and lexicon_recall_must_flags (reported, not gated)."""
    R.write_report(good, tmp_path)
    j = json.loads((tmp_path / "latest.json").read_text())
    assert j["backend"] == "claude-cli" and j["models"] == {"generator": "g", "judge": "j"}
    assert "app/llm/lexicon.yaml" in j["hashes"] and all(len(v) == 64 for v in j["hashes"].values())
    lr = j["metrics"]["lexicon_recall_must_flags"]
    assert lr.get("gated") is False and lr["r_ids"] == ["R-FL-3", "R-RV-6"]
    assert list(tmp_path.glob("2*.md"))

def test_lexicon_recall_is_pooled_and_per_case_and_not_gated():
    """AC9 / D-026: with a perfect floor the pooled recall is 1.0 and per-case entries exist; an empty floor scores 0.0."""
    gold = [e for e in G.expected("sample")["flags"] if e["type"] in ("pre_existing", "causation") and e["level"] == "must"]
    def floor(rec):
        return [dict(type=e["type"], excerpt=e["evidence"][0]["excerpt"]) for e in gold if rec["n"] in e["cite"]["all"]]
    cases = [c for c in R.golden_cases() if c[0] == "sample"]
    lr = R.lexicon_recall(floor, cases)
    assert lr["value"] == 1.0 and lr["per_case"]["sample"]["total"] == len(gold) and lr["gated"] is False
    assert R.lexicon_recall(lambda rec: [], cases)["value"] == 0.0

def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
    """AC7: --check-fresh is 0 on identical hashes and 1 when a prompt or the lexicon changed, or latest.json is missing."""
    (tmp_path / "app" / "llm" / "prompts").mkdir(parents=True)
    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("a")
    (tmp_path / "app" / "llm" / "lexicon.yaml").write_text("x: 1")
    (tmp_path / "latest.json").write_text(json.dumps({"hashes": R.hashes(tmp_path)}))
    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 0
    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("b")
    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 1
    assert R.check_fresh(tmp_path / "missing.json", tmp_path) == 1

def test_curated_fixture_set_is_refused_with_exit_2(tmp_path, monkeypatch, capsys):
    """D-029 / T-051: with FIXTURE_SET=curated or LLM_FIXTURE_DIR under tests/fixtures/llm/curated, the full run exits 2 with a clear message and writes no report; recorded/default sets are accepted."""
    monkeypatch.setenv("FIXTURE_SET", "curated")
    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
    assert "CURATED" in capsys.readouterr().err and not list(tmp_path.iterdir())
    monkeypatch.delenv("FIXTURE_SET")
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "curated"))
    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "recorded"))
    R.refuse_curated()                      # recorded set: no exception
    monkeypatch.delenv("LLM_FIXTURE_DIR")
    monkeypatch.setenv("FIXTURE_SET", "recorded")
    R.refuse_curated()

def test_tampered_two_run_determinism_fails_bar_4_alone(good):
    """Round-2 minor M9: a report claiming determinism 1.0 over 2 runs cannot pass bar 4 on the run-count term alone."""
    t = copy.deepcopy(good)
    t["metrics"]["determinism_3run"].update(value=1.0, runs=2, status="measured")
    ok, bars, blockers = R.evaluate_report(t)
    assert ok is False and bars["4_no_invented_facts"] is False

def test_grounding_uses_the_record_keys_run_case_really_emits():
    """Round-2 blocker: grounding() must read the real run_case record shape (`source`, not `source_label`). Real run_case output on the sample, fixture backend: provider/date/excerpt checks all run and pass."""
    from app import pipeline
    out = pipeline.run_case(SAMPLE, "fixture")
    assert out["records"] and "source" in out["records"][0] and "source_label" not in out["records"][0]
    g = R.grounding(SAMPLE, out)
    assert g["checked"] > 0 and [f for f in g["failures"] if f.endswith("provider")] == []
    # a wrong provider on a real entry IS detected (the check is live, not vacuous)
    out["entries"][0]["provider"] = "Invented Clinic"
    assert any(f.endswith("provider") for f in R.grounding(SAMPLE, out)["failures"])

def test_judge_unavailable_is_not_a_catch_and_makes_the_metric_not_measured():
    """Integrity: hallucination_catch_rate counts only real catches (code reason or judge partially/unsupported); 'unavailable' is reported as judge_unavailable_count and makes the bar not_measured/false."""
    h = R.hallucination_metrics(ITEMS, CONTROLS, lambda s, e, l: "unavailable", check_summary=lambda *a: [])
    assert h["caught"] == 0 and h["value"] == 0.0 and h["judge_unavailable_count"] == len(ITEMS) + len(CONTROLS) and h["status"] == "not_measured"
    # a code-rung catch with an unavailable judge is still a real catch, and still reported as unavailable
    h2 = R.hallucination_metrics(ITEMS[:2], [], lambda s, e, l: "unavailable", check_summary=lambda *a: ["SUMMARY_TOKEN_NOT_IN_EXCERPT"])
    assert h2["caught"] == 2 and h2["judge_unavailable_count"] == 2 and h2["status"] == "not_measured"

class UnavailableJudge(Perfect):
    def judge_summary(self, summary, excerpt, label, backend):
        return "unavailable" if summary in {i["candidate_summary"] for i in ITEMS[:1]} else super().judge_summary(summary, excerpt, label, backend)

def test_one_unavailable_judge_line_fails_bar_4_with_a_blocker():
    """Even one unanswered judge line on the hallucination set makes bar 4 not trustworthy: bar false, blocker names the count."""
    r = report(UnavailableJudge())
    assert r["metrics"]["hallucination_catch_rate"]["judge_unavailable_count"] == 1 and r["metrics"]["hallucination_catch_rate"]["status"] == "not_measured"
    assert r["bars"]["4_no_invented_facts"] is False and any("judge unavailable" in b for b in r["blockers"])

def test_judge_unavailable_inside_golden_cases_fails_bar_4():
    """An entry/amount/flag in a golden case whose judge was unavailable (JUDGE_UNAVAILABLE) is counted per case and fails bar 4."""
    def mark(n, o, p):
        if n == "sample":
            o["amounts"][0]["reasons"] = ["JUDGE_UNAVAILABLE"]
    r = report(Perfect(mutate=mark))
    assert r["metrics"]["judge_unavailable_in_cases"]["value"] == 1 and r["metrics"]["judge_unavailable_in_cases"]["per_case"] == {"sample": 1}
    assert r["bars"]["4_no_invented_facts"] is False


def test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4():
    """T-057 minor / D-031: unsplit_paste is part of the scored set: 3 code-parsed records, one LLM_SPLIT record_warning each; dropping one fails bar 4."""
    ok = report()
    assert ok["metrics"]["unsplit_paste"]["value"] is True and ok["ship_bar_met"] is True
    def drop(n, o, p):
        if n == "unsplit_paste":
            o["flags"] = o["flags"][1:]
    bad = report(Perfect(mutate=drop))
    assert bad["metrics"]["unsplit_paste"]["value"] is False and "record 1 has 0 LLM_SPLIT warnings, want 1" in bad["metrics"]["unsplit_paste"]["misses"]
    assert bad["bars"]["4_no_invented_facts"] is False

def test_unsplit_paste_wrong_date_or_one_record_fails():
    """D-031 M1/M2: a wrong code-parsed date, or boundaries rejected (one record), is a miss."""
    def one(n, o, p):
        if n == "unsplit_paste":
            o["records"] = o["records"][:1]
    r = report(Perfect(mutate=one))
    assert r["metrics"]["unsplit_paste"]["value"] is False and r["bars"]["4_no_invented_facts"] is False
    def bad_date(n, o, p):
        if n == "unsplit_paste":
            o["records"][1]["date_iso"] = "2026-05-12"
    assert report(Perfect(mutate=bad_date))["metrics"]["unsplit_paste"]["value"] is False


def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, capsys):
    """T-070: LLM_BACKEND=claude-cli without ENABLE_LIVE=1 used to run on the fixture backend and report backend=fixture; now it exits 2."""
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--out", str(tmp_path)]) == 2
    assert "ENABLE_LIVE=1" in capsys.readouterr().err
    assert not list(tmp_path.glob("*.json"))


@pytest.mark.parametrize("raw", [" claude-cli ", "Claude-CLI", "CLAUDE-CLI\n", "\tanthropic-api  ", "Anthropic-API"])
def test_padded_or_mixed_case_live_backend_without_enable_live_is_refused(raw, monkeypatch, tmp_path, capsys):
    """T-070 r2 (staff-engineer major): the guard must see the normalized name, or ' claude-cli ' runs on fixtures and writes backend=fixture."""
    monkeypatch.setenv("LLM_BACKEND", raw)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--out", str(tmp_path)]) == 2
    assert "ENABLE_LIVE=1" in capsys.readouterr().err
    assert not list(tmp_path.glob("*.json"))


@pytest.mark.parametrize("raw", ["openai", "claude", "claude-cli-x", "anthropic", "fixtures", "lol"])
def test_unknown_backend_name_exits_2_with_a_clear_message(raw, monkeypatch, tmp_path, capsys):
    """T-070 r2: a value that is not a known backend is an error, never a silent fixture run."""
    monkeypatch.setenv("LLM_BACKEND", raw)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--out", str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "unknown LLM_BACKEND" in err and "Nothing was run" in err
    assert not list(tmp_path.glob("*.json"))


@pytest.mark.parametrize("flag", ["openai", " Claude-Cli  ", "Fixture!"])
def test_backend_flag_is_validated_like_the_env_var(flag, monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    rc = R.main(["--backend", flag, "--out", str(tmp_path)])
    assert rc == 2
    assert not list(tmp_path.glob("*.json"))
    if flag.strip().lower() == "claude-cli":                # a known backend in odd case is refused by the ENABLE_LIVE guard, not 'unknown'
        assert "ENABLE_LIVE=1" in capsys.readouterr().err
    else:
        assert "unknown LLM_BACKEND" in capsys.readouterr().err


@pytest.mark.parametrize("raw,expected", [
    (None, "fixture"), ("", "fixture"), ("   ", "fixture"), ("fixture", "fixture"), ("FIXTURE ", "fixture"),
    (" claude-cli ", "claude-cli"), ("Claude-CLI", "claude-cli"), ("\tANTHROPIC-API\n", "anthropic-api"),
    ("openai", None), ("claude", None), ("claude-cli ok", None),
])
def test_normalize_backend_strips_lowercases_and_rejects_unknown(raw, expected):
    assert R.normalize_backend(raw) == expected


def test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name(monkeypatch, tmp_path):
    """T-070 r2 minor: with ENABLE_LIVE=1 a padded, mixed-case live name passes the guard and the run is built with the normalized backend."""
    seen = []
    def fake_build(pipeline, backend, runs=3, **kw):
        seen.append((backend, runs))
        return {"ship_bar_met": False, "backend": backend, "blockers": []}
    monkeypatch.setattr(R, "build_report", fake_build)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.setattr(R, "write_report", lambda r, outdir=None, **kw: tmp_path / "x.json")
    monkeypatch.setenv("LLM_BACKEND", " Claude-CLI ")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    rc = R.main(["--out", str(tmp_path)])
    assert rc == 1                                           # ship bar not met by the stub, but the run proceeded past the guard
    assert seen == [("claude-cli", 3)]


# ---------------------------------------------------------------- T-090 calibrated confidence (D-042): counts, never a bare percentage
def _tally(exp_name, mutate_out):
    exp = G.expected(exp_name)
    text = next(t for n, t, _ in R.golden_cases() if n == exp_name)
    out = Perfect().run_case(text, "claude-cli")
    mutate_out(out)
    return R.score_calibration(exp, out)


def test_score_calibration_counts_matched_over_seen_per_state_and_type():
    def m(out):
        out["entries"][0]["state"] = "needs_review"
        out["entries"][1]["summary"] = "something unrelated"          # verified but matches no golden entry
        out["entries"][1]["excerpt"] = "not in the golden"
        for a in out["amounts"][:2]:
            a["state"] = "verified"
        out["amounts"][0]["value_cents"] = 1                          # verified amount that does not match golden
    t = _tally("sample", m)
    assert t["entry"]["needs_review"] == [1, 1]
    assert t["entry"]["verified"][1] == t["entry"]["verified"][0] + 1  # exactly the one mutated entry missed
    assert t["amount"]["verified"] == [1, 2]
    assert set(t) == {"entry", "amount", "flag"} and set(t["entry"]) == {"verified", "needs_review"}


def test_score_calibration_ignores_rejected_items_and_items_without_a_state():
    def m(out):
        for k in ("entries", "amounts", "flags"):
            for x in out.get(k, []):
                x["state"] = "rejected"
        out["amounts"][0].pop("state", None)
    t = _tally("sample", m)
    assert all(v == [0, 0] for by in t.values() for v in by.values())


def test_flag_calibration_follows_flag_precision():
    def m(out):
        for f in out["flags"]:
            f["state"] = "verified"
        out["flags"].append({**out["flags"][0], "type": "gap", "from_date": "2020-01-01", "to_date": "2020-03-01", "days": 60,
                             "state": "needs_review", "evidence": [{"record_id": "r1", "excerpt": "invented"}]})
    t = _tally("sample", m)
    assert t["flag"]["needs_review"] == [0, 1]                         # the extra candidate matches nothing
    assert t["flag"]["verified"][0] == t["flag"]["verified"][1] > 0


def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
    res = {"a": {"calibration": {"entry": {"verified": [3, 4], "needs_review": [1, 2]}, "amount": {"verified": [2, 2], "needs_review": [0, 0]},
                                 "flag": {"verified": [0, 0], "needs_review": [0, 0]}}},
           "b": {"calibration": {"entry": {"verified": [1, 1], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 1]},
                                 "flag": {"verified": [0, 0], "needs_review": [0, 0]}}}}
    c = R.build_calibration(res, "fixture", {"generator": "x"}, "T")
    assert c["by_state"]["verified"] == {"matched": 6, "total": 7, "cases": ["a", "b"]}
    assert c["by_state"]["needs_review"] == {"matched": 1, "total": 3, "cases": ["a", "b"]}
    assert c["by_type"]["entry"]["verified"]["by_case"] == {"a": [3, 4], "b": [1, 1]}
    assert c["backend"] == "fixture" and c["case_count"] == 2 and c["small_sample"] is True
    assert c["sentences"]["overall"]["verified"] == ("Verified items matched the record 6/7 times in testing on the fixture backend "
                                                      "(recorded replies, 2 golden cases, small sample).")
    assert c["sentences"]["by_type"]["flag"]["verified"] == "No verified flags were seen in testing on the fixture backend."


def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
    res = {"a": {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}}
    c = R.build_calibration(res, "fixture")
    blob = json.dumps(c)
    assert "%" not in blob and "percent" not in blob.lower()
    assert not any(isinstance(v, float) for v in _walk(c))
    for s in c["sentences"]["overall"].values():
        assert re.search(r"\d+/\d+ times in testing", s)


def _walk(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from _walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from _walk(v)
    else:
        yield x


def test_large_sample_drops_the_case_caveat_but_keeps_the_item_caveat():
    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
                           "flag": {"verified": [0, 0], "needs_review": [0, 0]}}}
    few = {"calibration": {**row["calibration"], "entry": {"verified": [0, 0], "needs_review": [1, 2]}}}
    c = R.build_calibration({**{f"c{i}": row for i in range(29)}, "few": few}, "claude-cli")
    assert "small sample" not in c["sentences"]["overall"]["verified"]
    assert "(30 golden cases, small sample: 2 items)" in c["sentences"]["overall"]["needs_review"]


def test_small_sample_boundary_is_29_vs_30_cases():
    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
                           "flag": {"verified": [0, 0], "needs_review": [0, 0]}}}
    assert R.CAL_SMALL_N == 30
    at29 = R.build_calibration({f"c{i}": row for i in range(29)}, "claude-cli")
    at30 = R.build_calibration({f"c{i}": row for i in range(30)}, "claude-cli")
    assert "small sample" in at29["sentences"]["overall"]["verified"] and at29["small_sample"] is True
    assert "small sample" not in at30["sentences"]["overall"]["verified"]


@pytest.mark.parametrize("backend,recorded", [("fixture", True), ("claude-cli", False), ("anthropic-api", False)])
def test_every_sentence_names_the_backend_and_the_golden_set(backend, recorded):
    """The UI renders these verbatim, so a replay on the fixture backend cannot read as live-model precision (T-090 r2)."""
    row = {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}
    c = R.build_calibration({"a": row}, backend)
    sents = list(c["sentences"]["overall"].values()) + [x for by in c["sentences"]["by_type"].values() for x in by.values()]
    assert sents and all(f"on the {backend} backend" in x and "golden case" in x for x in sents)
    assert all(("recorded replies" in x) == recorded for x in sents)
    empty = R.build_calibration({"a": {"calibration": {}}}, backend)
    assert all(f"{backend} backend" in x for x in empty["sentences"]["overall"].values())


def test_amount_class_is_part_of_the_match():
    """A verified rate that carries the same text and value as a golden charge is NOT a match (the $185-rate-is-not-a-charge rule)."""
    def m(out):
        for a in out["amounts"][:2]:
            a["state"] = "verified"
        a0 = out["amounts"][0]
        a0["kind"] = "rate" if a0["kind"] == "charge" else "charge"
    assert _tally("sample", m)["amount"]["verified"] == [1, 2]


def test_tolerated_flag_counts_as_matched():
    def m(out):
        for f in out["flags"]:
            f["state"] = "verified"
        out["flags"].append({"id": "x", "type": "pre_existing", "state": "needs_review", "review_status": "pending",
                             "evidence": [{"record_id": "r1", "excerpt": "zzz unrelated to the golden span"}]})
    t = _tally("case_06_subtle_pre_existing", m)
    assert t["flag"]["needs_review"] == [1, 1]                         # case_06 tolerates a pre_existing flag citing record 1 (T1)


def test_record_warning_flags_cannot_shift_flag_states():
    """States follow the candidate itself, not its position among the flags (a record_warning placed first used to shift every later state)."""
    def states(out):
        for i, f in enumerate(out["flags"]):
            f["state"] = "verified" if i % 2 == 0 else "needs_review"
    def plain(out):
        states(out)
    def with_warning(out):
        states(out)
        out["flags"].insert(0, {"id": "w", "type": "record_warning", "state": "needs_review", "evidence": [{"record_id": "r1", "excerpt": "x"}]})
    a = _tally("case_06_subtle_pre_existing", plain)["flag"]
    b = _tally("case_06_subtle_pre_existing", with_warning)["flag"]
    assert a == b and a["verified"][1] and a["needs_review"][1]


def test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently():
    def m(out):
        for f in out["flags"]:
            f["state"] = "verified"
        out["flags"].append({**out["flags"][0], "id": "dup"})                  # duplicate of an earlier flag: dropped by assign_detail
        out["flags"].append({**out["flags"][0], "id": "nostate", "state": None, "evidence": [{"record_id": "r1", "excerpt": "other"}]})
        out["flags"].append({**out["flags"][0], "id": "rej", "state": "rejected", "evidence": [{"record_id": "r1", "excerpt": "another"}]})
        for a in out["amounts"]:
            a["state"] = "verified"
        out["amounts"][0].pop("state", None)
        out["amounts"][1]["state"] = "weird"
        out["entries"][0]["state"] = None
    exp = G.expected("sample")
    text = next(t for n, t, _ in R.golden_cases() if n == "sample")
    out = Perfect().run_case(text, "claude-cli")
    m(out)
    un = {}
    R.score_calibration(exp, out, un)
    assert un == {"entry": 1, "amount": 2, "flag": 2}                          # rejected is excluded on purpose; duplicate and stateless flags are not
    c = R.build_calibration({"sample": {"calibration": {t: {"verified": [1, 1], "needs_review": [0, 0]} for t in R.CAL_TYPES}, "calibration_unscored": un}}, "fixture")
    assert c["not_scored"] == {"entry": 1, "amount": 2, "flag": 2, "total": 5}
    assert "Not scored: 5 produced items" in c["sentences"]["overall"]["verified"]


def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
    rep = good
    c = rep["calibration"]
    assert c["backend"] == rep["backend"] and c["cases"] == rep["cases"]
    assert c["by_state"]["verified"]["total"] == sum(rep["per_case"][n]["calibration"][t]["verified"][1] for n in rep["per_case"] for t in R.CAL_TYPES)
    R.write_report(rep, tmp_path / "plain")
    assert "Calibrated confidence" in next((tmp_path / "plain").glob("2*.md")).read_text()
    assert json.loads(next((tmp_path / "plain" / "runs").glob("*/calibration.json")).read_text()) == json.loads(json.dumps(c))
    clean = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], {"commit": "a" * 40, "clean": True, "tree": "b" * 40}, rep["hashes"])
    R.write_report({**rep, "calibration": clean}, tmp_path / "committed", write_calibration=True)     # the header must be a clean commit (T-101 r2)
    assert json.loads((tmp_path / "committed" / "calibration.json").read_text()) == json.loads(json.dumps(clean))


# ---------------------------------------------------------------- T-101: a plain run never touches the committed calibration.json
def _fake_report(monkeypatch, rep):
    monkeypatch.setattr(R, "build_report", lambda *a, **k: copy.deepcopy(rep))
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)


def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
    """T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy."""
    committed = tmp_path / "calibration.json"
    committed.write_text('{"sentinel": "committed file, must not change"}\n')
    monkeypatch.setattr(R, "REPORTS", tmp_path)
    _fake_report(monkeypatch, good)
    before = committed.read_bytes()
    assert R.main([]) == 0
    assert committed.read_bytes() == before
    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good["calibration"]))
    assert list(tmp_path.glob("2*.md")) and (tmp_path / "latest.json").exists()


def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
    """T-101 AC1: a plain run is independent of git state; a dirty tree neither blocks it nor changes the committed file."""
    monkeypatch.setattr(R, "REPORTS", tmp_path)
    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": False, "tree": "b" * 40})
    _fake_report(monkeypatch, good)
    assert R.main([]) == 0
    assert not (tmp_path / "calibration.json").exists()


def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
    """T-101: a tree dirtied during a long run must not produce a committed header that claims clean; nothing is written."""
    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": True, "tree": "b" * 40})   # clean at the start
    def dirtied_during_run(*a, **k):
        rep = copy.deepcopy(good)
        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"],
                                                 {"commit": "a" * 40, "clean": False, "tree": "b" * 40}, rep["hashes"])
        return rep
    monkeypatch.setattr(R, "build_report", dirtied_during_run)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
    assert not (tmp_path / "calibration.json").exists() and not (tmp_path / "latest.json").exists()


@pytest.mark.parametrize("src", [
    {"commit": "a" * 40, "clean": False, "tree": "b" * 40},          # tracked edits or staged changes
    {"commit": None, "clean": None, "tree": None},                    # no git at all (exported tree)
])
def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
    """T-101 AC2: --write-calibration exits 2 before the pipeline runs and writes nothing."""
    monkeypatch.setattr(R, "git_source", lambda root=None: src)
    def must_not_run(*a, **k):
        raise AssertionError("the pipeline ran although --write-calibration was refused")
    monkeypatch.setattr(R, "build_report", must_not_run)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
    assert list(tmp_path.iterdir()) == []


def test_write_calibration_refusal_rule_is_clean_tree_at_a_commit():
    assert R.write_calibration_refusal({"commit": "a" * 40, "clean": True, "tree": "b" * 40}) is None
    assert "uncommitted" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40})
    assert "no git repository" in R.write_calibration_refusal({"commit": None, "clean": None, "tree": None})   # T-101 r2 F6: the reason, not just a refusal


def test_write_calibration_refusal_names_every_dirty_path_it_is_given():
    why = R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40,
                                       "dirty": [" M evals/reports/latest.json", "?? evals/golden/case_zz.txt"]})
    assert "evals/reports/latest.json" in why and "evals/golden/case_zz.txt" in why
    many = [f"?? evals/golden/case_{i:02d}.txt" for i in range(13)]
    assert "and 3 more" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40, "dirty": many})


def test_write_report_refuses_a_dirty_header_before_writing_anything(tmp_path, good):
    """T-101 r2: write_report is the only writer of the committed file, so it judges the header itself; a refused call writes nothing."""
    dirty = copy.deepcopy(good)
    dirty["calibration"] = R.build_calibration(dirty["per_case"], dirty["backend"], dirty["models"], dirty["generated_at"],
                                               {"commit": "a" * 40, "clean": False, "tree": "b" * 40}, dirty["hashes"])
    with pytest.raises(R.CalibrationRefused):
        R.write_report(dirty, tmp_path, write_calibration=True)
    assert list(tmp_path.iterdir()) == []
    R.write_report(dirty, tmp_path / "plain")                     # a plain write of the same report is still fine: it goes to scratch
    assert not (tmp_path / "plain" / "calibration.json").exists()


def test_write_calibration_is_refused_with_controls_before_anything_runs(monkeypatch, tmp_path):
    """T-101 r2 F3: --write-calibration --controls exits 2 with a message; nothing runs and nothing is written."""
    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": True, "tree": "b" * 40})
    def must_not_run(*a, **k):
        raise AssertionError("controls ran although --write-calibration --controls was refused")
    monkeypatch.setattr(R, "run_controls_only", must_not_run)
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--write-calibration", "--controls", "--out", str(tmp_path)]) == 2
    assert list(tmp_path.iterdir()) == []


def test_scratch_copy_and_live_run_artifacts_share_one_run_directory(monkeypatch, tmp_path, good):
    """T-101 r2 F4: the scratch calibration.json lands in the same runs/<ts> directory the live run artifacts use."""
    seen = {}
    def fake_build(*a, **k):
        seen["runs_dir"] = k.get("runs_dir")
        return copy.deepcopy(good)
    monkeypatch.setattr(R, "build_report", fake_build)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.setattr(R, "default_judge_control", lambda backend: None)
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    assert R.main(["--out", str(tmp_path)]) in (0, 1)
    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
    assert len(scratch) == 1 and scratch[0].parent == seen["runs_dir"]


def test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):
    """T-101 AC2/AC3 on a real repository: allowed on a clean tracked tree (untracked files do not count), refused after a tracked edit and
    leaves the file absent; the written header names HEAD, the clean flag, the tree and the prompt/lexicon hashes as T-090 defined them."""
    if shutil.which("git") is None:
        pytest.skip("git missing")
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "f").write_text("a")
    subprocess.run(["git", "-C", str(repo), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "x"], check=True, env=env)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    real = R.git_source
    monkeypatch.setattr(R, "git_source", lambda root=None: real(repo))
    def fake_report(*a, **k):
        rep = copy.deepcopy(good)
        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], R.git_source(), rep["hashes"])
        return rep
    monkeypatch.setattr(R, "build_report", fake_report)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    out = tmp_path / "out"
    (repo / "untracked.txt").write_text("not tracked")
    assert R.main(["--write-calibration", "--out", str(out)]) == 0
    c = json.loads((out / "calibration.json").read_text())
    assert c["schema"] == "evals.calibration/1" and c["source_commit"] == head and c["source_tree_clean"] is True
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_tree"]) and c["hashes"] == good["hashes"] and c["backend"] == good["backend"]
    (out / "calibration.json").unlink()
    (repo / "f").write_text("edited, not committed")
    before = sorted(p.name for p in out.iterdir())
    assert R.main(["--write-calibration", "--out", str(out)]) == 2
    assert not (out / "calibration.json").exists()
    assert sorted(p.name for p in out.iterdir()) == before          # the refused run wrote nothing new


# ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
import os, shutil, subprocess, sys
CAL = R.REPORTS / "calibration.json"


def _git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)


def _committed():
    return json.loads(CAL.read_text())


def _has_git():
    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0


def _require_history():
    """T-194: a one-commit public snapshot cannot contain the commits calibration.json cites.  Skips only then; the real repo still asserts."""
    from tests.unit._githist import REASON, single_commit
    if single_commit():
        pytest.skip(REASON)


def _require_source_commit(c):
    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
    if not _has_git():
        pytest.skip("no git repository here (exported tree)")
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"


CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)


def _assert_calibration_header(c):
    assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
    assert c["source_tree_clean"] is True, "calibration source tree is not clean"
    assert c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or ""), "calibration has no source tree or hashes"


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    _assert_calibration_header(_committed())


def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
    """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
    for backend in ("fixture", "claude-cli"):  # literal on purpose: shrinking CAL_BACKENDS must fail this test
        dirty = _committed()
        dirty["backend"], dirty["source_tree_clean"] = backend, False
        p = tmp_path / f"dirty_{backend}.json"
        p.write_text(json.dumps(dirty))
        monkeypatch.setattr(sys.modules[__name__], "CAL", p)
        with pytest.raises(AssertionError, match="source tree is not clean"):
            _assert_calibration_header(_committed())
        monkeypatch.undo()


def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
    _require_history()
    c = _committed()
    _require_source_commit(c)
    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"


def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
    c = _committed()
    c["source_commit"] = "1" * 40
    forged = tmp_path / "calibration.json"
    forged.write_text(json.dumps(c))
    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
    if not _has_git():
        pytest.skip("no git repository here")
    with pytest.raises(AssertionError, match="does not exist"):
        _require_source_commit(_committed())


def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
    """T-090 r2 blocker: the shipped counts must come from the code of the commit named in the header. Export that commit
    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at and the git-derived fields
    (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
    _require_history()
    c = _committed()
    _require_source_commit(c)
    if c["backend"] == "claude-cli":
        # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
        # ancestor and clean-tree tests plus the report-binding test below (the report is found from generated_at; the file has no run id).
        pytest.skip(f"committed calibration is a live {c['backend']} measurement; exact regeneration needs the live backend")
    src = tmp_path / "src"
    src.mkdir()
    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
    # The cited commit's own code decides where the file lands: commits before T-101 write out/calibration.json, later ones only a
    # scratch copy under out/runs/<ts>/ (T-101). Exactly one must exist either way.
    found = [p for p in [out / "calibration.json", *sorted((out / "runs").glob("*/calibration.json"))] if p.exists()]
    assert len(found) == 1, r.stdout[-400:] + r.stderr[-800:]
    fresh = json.loads(found[0].read_text())
    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
    assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
    assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
    assert c["source_tree_clean"] is True


def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
    """T-101 AC2 end to end: a copy of the tree with no .git exits 2 with a clear message before any run and writes nothing. The copy is made with
    shutil (not `git archive`), so the test also runs inside an export of HEAD that has no .git itself (T-106)."""
    src = tmp_path / "src"
    for d in ("app", "evals", "spec"):
        if (R.ROOT / d).is_dir():
            shutil.copytree(R.ROOT / d, src / d, ignore=shutil.ignore_patterns(".git", "__pycache__", "runs"))
    assert not (src / ".git").exists()
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 2 and "--write-calibration refused" in r.stderr and "no git repository" in r.stderr, r.stderr[-800:]
    assert "Traceback" not in r.stderr
    assert not out.exists() or not any(out.iterdir())


def test_git_source_reports_commit_and_dirtiness(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git missing")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "f").write_text("a")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
    a = R.git_source(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
    (tmp_path / "f").write_text("b")
    assert R.git_source(tmp_path)["clean"] is False
    assert R.git_source(tmp_path)["dirty"] == [" M f"]
    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None, "dirty": []}


def test_git_source_counts_untracked_files_under_the_eval_inputs_only(tmp_path):
    """T-101 r2 F1: an untracked golden case, fixture or prompt makes the tree dirty; an untracked report or a scratch file outside the inputs does not."""
    if shutil.which("git") is None:
        pytest.skip("git missing")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    (tmp_path / "evals" / "golden").mkdir(parents=True)
    (tmp_path / "evals" / "reports").mkdir(parents=True)
    (tmp_path / "tests" / "fixtures").mkdir(parents=True)
    (tmp_path / "evals" / "golden" / "keep.txt").write_text("k")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
    assert R.git_source(tmp_path)["clean"] is True
    (tmp_path / "evals" / "reports" / "20990101T000000Z.md").write_text("report output")          # a run writes here: not an input
    (tmp_path / "scratch.txt").write_text("outside the inputs")                                   # not an input either
    assert R.git_source(tmp_path)["clean"] is True
    (tmp_path / "evals" / "golden" / "case_zz_untracked.txt").write_text("not committed")
    src = R.git_source(tmp_path)
    assert src["clean"] is False and "?? evals/golden/case_zz_untracked.txt" in src["dirty"]
    assert "evals/reports" not in " ".join(src["dirty"]) and "scratch.txt" not in " ".join(src["dirty"])
    assert "case_zz_untracked" in R.write_calibration_refusal({"commit": src["commit"], "clean": False, "tree": src["tree"], "dirty": src["dirty"]})


def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
    rep = tmp_path / "latest.json"
    rep.write_text(json.dumps({"hashes": R.hashes()}))
    cal = _committed()
    cal["hashes"] = R.hashes()                                                  # consistent with this checkout; the committed hashes go stale on any prompt edit
    (tmp_path / "calibration.json").write_text(json.dumps(cal))
    assert R.check_fresh(rep) == 0                                              # the committed pair is consistent with the repo
    cal["by_state"]["verified"]["matched"] += 1
    (tmp_path / "calibration.json").write_text(json.dumps(cal))
    assert R.check_fresh(rep) == 1
    cal = _committed()
    cal["hashes"] = R.hashes()
    k = sorted(cal["hashes"])[0]
    cal["hashes"][k] = "0" * 64
    (tmp_path / "calibration.json").write_text(json.dumps(cal))
    assert R.check_fresh(rep) == 1


def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
    rep = tmp_path / "latest.json"
    rep.write_text(json.dumps({"hashes": R.hashes()}))
    cal = _committed()
    cal["hashes"] = R.hashes()
    cal["sentences"]["overall"]["verified"] = cal["sentences"]["overall"]["verified"].replace(
        f"{cal['by_state']['verified']['matched']}/", f"{cal['by_state']['verified']['total']}/", 1)
    (tmp_path / "calibration.json").write_text(json.dumps(cal))
    assert R.check_fresh(rep) == 1


# ---- D-053 / T-094 r2: precision is over emitted flags only; tray flags are reported apart and are not in the R-CO-7 flag signature
def _tray_wrong_flag(out):
    out["flags"].append({"id": "tray1", "type": "causation", "category": "alternative_cause", "state": "rejected", "reasons": ["JUDGE_DISAGREES"],
                         "evidence": [{"record_id": "r4", "excerpt": "zzz not in the golden set"}]})


def test_a_tray_flag_does_not_lower_precision_but_a_wrong_emitted_flag_does():
    def tray(name, out, pipe):
        if name == "sample":
            _tray_wrong_flag(out)
    def emitted(name, out, pipe):
        if name == "sample":
            _tray_wrong_flag(out)
            out["flags"][-1]["state"] = "needs_review"
    base = report(Perfect(mutate=lambda n, o, p: None))["metrics"]
    t = report(Perfect(mutate=tray))["metrics"]
    e = report(Perfect(mutate=emitted))["metrics"]
    assert t["flag_precision"]["causation"] == base["flag_precision"]["causation"] == 1.0
    assert e["flag_precision"]["causation"] < 1.0
    assert t["flag_tray"]["value"] == 1 and t["flag_tray"]["by_reason"] == {"JUDGE_DISAGREES": 1} and t["flag_tray"]["by_case"] == {"sample": 1}
    assert base["flag_tray"]["value"] == 0


def test_a_golden_must_flag_in_the_tray_is_a_recall_miss_not_a_hit():
    def m(name, out, pipe):
        if name == "sample":
            f = next(f for f in out["flags"] if f["type"] == "conflict")
            f["state"] = "rejected"
    r = report(Perfect(mutate=m))
    assert r["metrics"]["flag_recall"]["conflict"] < 1.0 and r["metrics"]["flag_tray"]["value"] == 1


def test_the_flag_signature_excludes_tray_flags_and_a_flip_between_list_and_tray_changes_it():
    text = SAMPLE
    a = Perfect().run_case(text, "claude-cli")
    b = Perfect().run_case(text, "claude-cli")
    _tray_wrong_flag(b)
    assert R.signature(a) == R.signature(b)                       # D-053: tray items are not in the flag-set signature
    b["flags"][-1]["state"] = "needs_review"
    assert R.signature(a) != R.signature(b)
    assert R.run_artifact(a)["tray_flag_count"] == 0 and R.run_artifact(_with_tray(a))["tray_flag_count"] == 1


def _with_tray(out):
    out = copy.deepcopy(out)
    _tray_wrong_flag(out)
    return out


def test_report_names_source_commit_and_tree_state_and_the_tray_line(good):
    md = R.render_md(good)
    assert "Source commit `" in md and "tree " in md and "flag tray (could-not-verify flags, D-053" in md


def test_git_source_ignores_the_reports_a_run_rewrites_but_not_the_inputs(tmp_path):
    """T-094 r2: a run rewrites the tracked evals/reports/latest.json; that must not make the NEXT run of the same commit report a DIRTY tree."""
    import subprocess
    def g(*a):
        subprocess.run(["git", "-C", str(tmp_path), "-c", "user.email=t@t", "-c", "user.name=t", *a], check=True, capture_output=True)
    (tmp_path / "evals" / "reports").mkdir(parents=True)
    (tmp_path / "app").mkdir()
    (tmp_path / "evals" / "reports" / "latest.json").write_text("{}")
    (tmp_path / "app" / "x.py").write_text("x = 1\n")
    g("init", "-q"); g("add", "evals", "app"); g("commit", "-q", "-m", "c")
    assert R.git_source(tmp_path)["clean"] is True
    (tmp_path / "evals" / "reports" / "latest.json").write_text('{"changed": 1}')
    assert R.git_source(tmp_path)["clean"] is True
    (tmp_path / "app" / "x.py").write_text("x = 2\n")
    assert R.git_source(tmp_path)["clean"] is False


# ---- score_unsplit replays the whole case (T-102 review F3): the row cannot be green while LLM calls go unreplayed

def test_score_unsplit_on_the_real_pipeline_replays_every_call_with_no_fixture_miss():
    from app.llm.backends import fixture as FX
    seen = []
    orig = FX.call
    def spy(*a, **kw):
        seen.append(kw.get("key"))
        return orig(*a, **kw)
    FX.call = spy
    try:
        r = R.score_unsplit(R.load_pipeline(), "fixture")
    finally:
        FX.call = orig
    assert r["value"] is True and r["misses"] == [] and r["records"] == 3
    assert len(seen) >= 7, "extract, flags and split calls must all be replayed, not just the split reply"


def test_score_unsplit_is_false_when_the_fixture_dir_is_wrong_or_empty(tmp_path, monkeypatch):
    from app.llm.backends import fixture as FX
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(FX, "DEFAULT_DIR", empty)
    r = R.score_unsplit(R.load_pipeline(), "fixture")
    assert r["value"] is False
    assert any("split fixture dir is missing or empty" in m for m in r["misses"])
    assert any("no recorded fixture" in m for m in r["misses"])


def test_score_unsplit_is_false_when_only_the_split_reply_is_missing(tmp_path, monkeypatch):
    """The default recorded set is present but tests/fixtures/llm/split is not: the split call misses, so the row is false."""
    from app.llm.backends import fixture as FX
    d = tmp_path / "llm"
    d.mkdir()
    for p in FX.DEFAULT_DIR.glob("*.json"):
        (d / p.name).symlink_to(p)
    monkeypatch.setattr(FX, "DEFAULT_DIR", d)
    r = R.score_unsplit(R.load_pipeline(), "fixture")
    assert r["value"] is False and any("split fixture dir is missing or empty" in m for m in r["misses"])


def test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir(monkeypatch):
    """LLM_FIXTURE_DIR disables the default-dir fallback in fixture.call, so the scorer must not set it while the case runs."""
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    monkeypatch.setenv("FIXTURE_SET", "recorded")
    seen = {}
    class Spy(Perfect):
        def run_case(self, text, backend):
            import os
            seen.update(dir=os.environ.get("LLM_FIXTURE_DIR"), set=os.environ.get("FIXTURE_SET"))
            return super().run_case(text, backend)
    R.score_unsplit(Spy(), "fixture")
    import os
    assert seen == {"dir": None, "set": "split"}
    assert os.environ.get("FIXTURE_SET") == "recorded" and "LLM_FIXTURE_DIR" not in os.environ


def _report_for(c):
    """The calibration file has no run id or report field, so the link is derived: generated_at 2026-11-02T16:40:38Z is the report id 20261102T164038Z (T-169 r2)."""
    rid = re.sub(r"[-:]", "", c["generated_at"])
    assert re.fullmatch(r"\d{8}T\d{6}Z", rid), f"generated_at {c['generated_at']!r} is not a UTC timestamp"
    return rid, R.REPORTS / f"{rid}.md"


def _report_counts(md):
    """matched/seen read from the report's own text: the two overall sentences and the per-type table."""
    got = {"sentences": [l[2:] for l in md.splitlines() if l.startswith("- ") and " matched the record " in l]}
    got["table"] = {m[0]: [tuple(map(int, x.split("/"))) for x in m[1:]]
                    for m in re.findall(r"^\| (entry|amount|flag) \| (\d+/\d+) \| (\d+/\d+) \|$", md, re.M)}
    return got


def test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts():
    """T-169 r2 F2: the live calibration cannot be regenerated offline, so tie it to the report of its run. The report must exist in
    evals/reports, name the same source commit and backend, and carry the same overall sentences and per-type matched/seen counts."""
    c = _committed()
    rid, rep = _report_for(c)
    assert rep.exists(), f"calibration.json generated_at {c['generated_at']} names report {rep.name}, which is not in evals/reports"
    md = rep.read_text()
    assert f"backend `{c['backend']}`" in md and f"Source commit `{c['source_commit']}`" in md, f"{rep.name} names a different backend or source commit"
    got = _report_counts(md)
    assert got["sentences"] == [c["sentences"]["overall"]["verified"], c["sentences"]["overall"]["needs_review"]], f"{rep.name} overall counts differ from calibration.json"
    want = {t: [tuple(c["by_type"][t][s][k] for k in ("matched", "total")) for s in ("verified", "needs_review")] for t in ("entry", "amount", "flag")}
    assert got["table"] == want, f"{rep.name} per-type counts differ from calibration.json"
    for s in ("verified", "needs_review"):
        assert f"{c['by_state'][s]['matched']}/{c['by_state'][s]['total']} times" in c["sentences"]["overall"][s], "by_state disagrees with its own sentence"


def test_committed_calibration_run_directory_exists_with_every_case():
    """The raw outputs of the run: the newest evals/reports/runs/<id> not later than the report id must hold one file per calibration case.
    (Run ids are the run's start time, the report id its finish time, so they differ; the file carries neither.)"""
    c = _committed()
    rid, _ = _report_for(c)
    runs = sorted(d.name for d in (R.REPORTS / "runs").iterdir() if d.is_dir() and d.name <= rid)
    assert runs, f"no evals/reports/runs/<id> at or before {rid}"
    have = {p.stem for p in (R.REPORTS / "runs" / runs[-1]).glob("*.json")}
    assert set(c["cases"]) <= have, f"runs/{runs[-1]} lacks {sorted(set(c['cases']) - have)}"


def test_report_binding_fails_on_a_coordinated_count_and_sentence_edit(tmp_path, monkeypatch):
    """T-169 r2 F2 acceptance: change by_state.verified.matched and its sentence together; the binding test must fail."""
    c = _committed()
    c["by_state"]["verified"]["matched"] = c["by_state"]["verified"]["total"]
    c["sentences"]["overall"]["verified"] = c["sentences"]["overall"]["verified"].replace(
        f"{c['by_state']['verified']['total'] - 1}/", f"{c['by_state']['verified']['total']}/")
    c["by_type"]["entry"]["verified"]["matched"] = c["by_type"]["entry"]["verified"]["total"]
    forged = tmp_path / "calibration.json"
    forged.write_text(json.dumps(c))
    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
    with pytest.raises(AssertionError, match="differ from calibration.json"):
        test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts()
