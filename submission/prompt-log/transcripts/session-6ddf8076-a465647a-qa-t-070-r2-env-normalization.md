# Subagent: QA: T-070 r2 env normalization (QA: T-070 r2 env normalization)

Source: `agent-a465647a242ff9e16.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:02:25.983Z

You own board card T-070, round 2 (claimed by "qa") in /Users/arsis/zlayt-pm-project. Read reviews/T-070-staff-engineer.md.

Major: a padded or mixed-case LLM_BACKEND (" claude-cli ", "Claude-CLI") still silently runs on fixtures. In evals/run.py, normalize the value (strip, lower) before the live-without-ENABLE_LIVE guard. Any value that isn't a known backend must exit 2 with a clear message. Add parametrized tests.

If app/llm/provider.py should normalize the same way, post a card note for backend rather than editing it. Run `.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py`. Commit with `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-070 in_review --agent qa`. Reply in 1 line.

### User / tool · 2026-11-02T03:02:25.988Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:29.283Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-070-staff-engineer.md && echo ---- && cat evals/run.py && echo ---- && cat tests/unit/test_eval_runner.py && echo ---- && git status --short | head -30",
 "description": "Read review, eval runner, and its tests"
}
````

### User / tool · 2026-11-02T03:02:29.461Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:31.654Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -20; echo ----; grep -n \"LLM_BACKEND\\|ENABLE_LIVE\\|exit\\|def \\|import\" evals/run.py | head -80; echo ----; grep -n \"LLM_BACKEND\\|ENABLE_LIVE\\|def test\\|parametrize\" tests/unit/test_eval_runner.py; echo ----; grep -n \"LLM_BACKEND\\|claude-cli\\|fixture\" app/llm/provider.py | head -30",
 "description": "Check git state and locate backend guard code"
}
````

### User / tool · 2026-11-02T03:02:31.786Z

**tool result**
````
88a3393
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/frontend/batch.js
 M app/frontend/manual.js
 M app/frontend/review.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
----
4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
6:    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
17:import argparse
18:import datetime as dt
19:import hashlib
20:import json
21:import os
22:import pathlib
23:import re
24:import sys
26:from evals.matching import assign_detail, norm
45:def rn(rid):
53:def low(s):
57:def ratio(num, den):
61:def golden_cases():
66:def sha256_file(p):
70:def hashes(root=ROOT):
81:def split_regex_text(s):
85:def regex_hits(mn, text):
94:def product_entries(out):
98:def entry_found(g, prod):
130:def score_entries(exp, out):
143:def score_amounts(exp, out):
162:def to_candidates(out):
175:def tolerated_match(t, c):
180:def score_flags(exp, out):
214:def score_record_warnings(exp, out):
227:def check_must_not(exp, out):
253:def unsupported_summaries(out):
262:def judge_unavailable_in(out):
268:def grounding(text, out):
274:    def chk(label, ok):
295:def score_unsplit(pipeline, backend):
334:def run_cases(pipeline, backend, cases=None):
347:def parse_record_text(rt):
355:def judge_item(item, judge, check_summary):
362:def hallucination_metrics(items, controls, judge, check_summary=None):
377:def load_jsonl(p):
382:def signature(out):
392:def live_metrics(pipeline, backend, text, runs=3):
406:def lexicon_recall(lexicon_flags, cases=None):
428:def spec_blocks(req_text):
434:def golden_blocks(export_text):
442:def check_spec(req_path=REQUIREMENTS, golden_path=GOLD / "sample.export.expected.txt"):
449:def aggregate(results):
482:def assertions(results):
492:def case_07_total(results, outs):
500:def ship_bar(m, a, backend, spec_ok):
503:    def ge(x, t):
535:def evaluate_report(report):
541:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
547:        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
560:        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
576:def pct(x):
580:def render_md(r):
608:def write_report(r, outdir=REPORTS):
617:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
630:def load_pipeline():
631:    from app import pipeline
639:def refuse_curated(env=None):
652:def main(argv=None, pipeline=None):
679:    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
680:    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
681:        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
683:        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
684:              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
695:    sys.exit(main())
----
86:def test_perfect_run_meets_ship_bar_on_a_live_backend(good):
95:def test_fixture_backend_never_meets_the_bar_and_live_metrics_are_not_measured():
103:def test_determinism_detects_a_run_that_differs():
116:@pytest.mark.parametrize("bar,mut", [
125:def test_each_missed_bar_names_the_failed_bar_and_only_that_bar(bar, mut):
130:def test_controls_judged_unsupported_fail_bar_4_alone():
139:def test_case_07_not_run_fails_bar_4():
145:def test_missing_record_warning_counts_as_a_must_not_hit():
154:def test_summary_that_drops_a_qualifier_is_an_entry_miss():
163:@pytest.mark.parametrize("runs", [1, 2, 4])
164:def test_fewer_or_more_than_three_live_runs_cannot_meet_the_bar(runs):
171:def test_cli_runs_1_does_not_crash(tmp_path):
175:def test_raising_code_check_fails_loudly():
182:def test_report_splits_code_caught_and_judge_caught():
187:def test_check_spec_recomputes_the_bar_in_a_full_report(tmp_path, monkeypatch):
197:def test_gap_28_flagged_or_73_missing_fails_the_assertions():
211:def test_hallucination_rate_is_over_every_line_and_controls_must_pass():
224:def test_golden_must_not_hits_are_counted_and_fail_the_bar():
232:def test_case_07_total_must_stay_420():
240:def test_tampered_report_is_recomputed_false(good):
247:def test_report_records_backend_models_hashes_and_lexicon_recall(good, tmp_path):
257:def test_lexicon_recall_is_pooled_and_per_case_and_not_gated():
267:def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
278:def test_curated_fixture_set_is_refused_with_exit_2(tmp_path, monkeypatch, capsys):
292:def test_tampered_two_run_determinism_fails_bar_4_alone(good):
299:def test_grounding_uses_the_record_keys_run_case_really_emits():
310:def test_judge_unavailable_is_not_a_catch_and_makes_the_metric_not_measured():
322:def test_one_unavailable_judge_line_fails_bar_4_with_a_blocker():
328:def test_judge_unavailable_inside_golden_cases_fails_bar_4():
338:def test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4():
349:def test_unsplit_paste_wrong_date_or_one_record_fails():
362:def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, capsys):
363:    """T-070: LLM_BACKEND=claude-cli without ENABLE_LIVE=1 used to run on the fixture backend and report backend=fixture; now it exits 2."""
364:    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
365:    monkeypatch.delenv("ENABLE_LIVE", raising=False)
367:    assert "ENABLE_LIVE=1" in capsys.readouterr().err
----
3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
5:Record mode (RECORD_FIXTURES=1 or LLM_FIXTURE_RECORD=1, live backend only) writes tests/fixtures/llm/<hash>.json and is
16:from app.llm.backends import fixture as _fixture
24:    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
29:        return "fixture"
95:    if name == "fixture":
96:        res = _fixture.call(model, system, user, json_schema, key=key)
97:    elif name in ("claude-cli", "anthropic-api"):
100:        if name == "claude-cli":
108:    if name != "fixture" and _recording():
109:        _fixture.write(key, res, model)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:33.284Z

**tool call — Bash**
````
{
 "command": "sed -n 26,45p evals/run.py; echo ----; sed -n 630,700p evals/run.py; echo ----; sed -n 355,372p tests/unit/test_eval_runner.py; echo ----; sed -n 1,30p tests/unit/test_eval_runner.py; echo ----; sed -n 20,40p app/llm/provider.py; echo ----; sed -n 90,112p app/llm/provider.py",
 "description": "Read guard, main, test and provider code"
}
````

### User / tool · 2026-11-02T03:02:33.396Z

**tool result**
````
from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
NOT_MEASURED = {"value": None, "status": "not_measured"}

THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
              "hallucination_catch_rate": 0.95, "unsupported_count_3run": 0, "determinism_3run": 1.0}
RIDS = {"grounding_rate": ["R-TL-2", "R-TL-9", "R-FL-5", "R-EX-2"], "entry_recall": ["R-TL-1", "R-TL-7"], "amount_recall": ["R-CH-1"],
        "flag_precision": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"], "flag_recall": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"],
        "hallucination_catch_rate": ["R-TL-4", "R-TL-10"], "unsupported_count_3run": ["R-TL-4", "R-CH-7"], "determinism_3run": ["R-CO-7"],
        "lexicon_recall_must_flags": ["R-FL-3", "R-RV-6"], "golden_must_not_hits": ["R-CO-3"], "case_07_total_420": ["R-RV-6"]}
FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")


# ---------------------------------------------------------------- helpers
def rn(rid):
----
def load_pipeline():
    from app import pipeline
    return pipeline


class CuratedFixtures(Exception):
    pass


def refuse_curated(env=None):
    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
    env = os.environ if env is None else env
    d = env.get("LLM_FIXTURE_DIR", "").strip()
    curated_dir = ROOT / "tests" / "fixtures" / "llm" / "curated"
    in_curated = bool(d) and (pathlib.Path(d).resolve() == curated_dir.resolve() or curated_dir.resolve() in pathlib.Path(d).resolve().parents)
    if env.get("FIXTURE_SET", "").strip() == "curated" or in_curated:
        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under "
                              "tests/fixtures/llm/curated): curated responses reproduce the golden answers by construction (D-029). "
                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")


def main(argv=None, pipeline=None):
    ap = argparse.ArgumentParser(prog="python -m evals.run")
    ap.add_argument("--check-fresh", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.check_fresh:
        return check_fresh(out / "latest.json")
    if a.check_spec:
        s = check_spec()
        latest = out / "latest.json"
        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
        data.update(s)
        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
        out.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps(s))
        return 0 if s["spec_matches_golden"] else 1
    try:
        refuse_curated()
    except CuratedFixtures as e:
        print(f"evals.run: {e}", file=sys.stderr)
        return 2
    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    report = build_report(pipeline or load_pipeline(), backend, a.runs)
    path = write_report(report, out)
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)


if __name__ == "__main__":
    sys.exit(main())
----
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
----
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
----
_record_ok = False


def backend_name() -> str:
    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
        return "fixture"
    return name


def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()
----


def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
    name = backend_name()
    key = prompt_hash(model, system, user, json_schema)
    if name == "fixture":
        res = _fixture.call(model, system, user, json_schema, key=key)
    elif name in ("claude-cli", "anthropic-api"):
        if _recording() and not _record_ok:
            raise ValueError("record mode needs record_context() over text from evals/golden")
        if name == "claude-cli":
            from app.llm.backends import claude_cli as be
        else:
            from app.llm.backends import anthropic_api as be
        res = be.call(model, system, user, json_schema, key=key)
    else:
        raise LLMError(f"UNKNOWN_BACKEND {name}")
    validate_schema(res.output, json_schema)
    if name != "fixture" and _recording():
        _fixture.write(key, res, model)
    return res
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:45.654Z

**tool call — Bash**
````
{
 "command": "grep -rn \"main(\\|LLM_BACKEND\\|\\.backend\\b\" tests/unit/test_eval_runner.py evals/*.py | head -30; echo ----; grep -n \"T-070\" -r board/cards/T-070.md | head -3; sed -n 1,60p board/cards/T-070.md",
 "description": "Find main() callers and read card T-070"
}
````

### User / tool · 2026-11-02T03:02:45.769Z

**tool result**
````
tests/unit/test_eval_runner.py:173:    assert R.main(["--runs", "1", "--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 1
tests/unit/test_eval_runner.py:193:    assert R.main(["--check-spec", "--out", str(tmp_path)]) == 1
tests/unit/test_eval_runner.py:281:    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
tests/unit/test_eval_runner.py:285:    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
tests/unit/test_eval_runner.py:363:    """T-070: LLM_BACKEND=claude-cli without ENABLE_LIVE=1 used to run on the fixture backend and report backend=fixture; now it exits 2."""
tests/unit/test_eval_runner.py:364:    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
tests/unit/test_eval_runner.py:366:    assert R.main(["--out", str(tmp_path)]) == 2
evals/run.py:4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
evals/run.py:547:        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
evals/run.py:560:        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
evals/run.py:652:def main(argv=None, pipeline=None):
evals/run.py:679:    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
evals/run.py:684:              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
evals/run.py:695:    sys.exit(main())
----
board/cards/T-070.md:2:id: "T-070"
board/cards/T-070.md:17:  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-070-staff-engineer.md", "at": "2026-11-02T03:02:22Z"}
board/cards/T-070.md:30:- 2026-11-02T03:02:22Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-070-staff-engineer.md; round 1; findings:
---
id: "T-070"
title: "Live eval: evals.run honors LLM_BACKEND=claude-cli (reported backend=fixture)"
milestone: "M2"
role: "qa"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:40:24Z"
updated_at: "2026-11-02T03:02:22Z"
claimed_by: "qa"
claimed_at: "2026-11-02T03:02:22Z"
rounds: 1
commits: ["815d616"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-070-staff-engineer.md", "at": "2026-11-02T03:02:22Z"}
ac:
  - {"n": 1, "text": "LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --runs 3 reports backend=claude-cli and measures determinism/unsupported; report path noted", "done": true, "evidence": "evals/reports/20261102T025219Z.md: backend=claude-cli (sonnet-5-5/haiku-5-5), 3 live runs measured: determinism_3run=0.0 (bar 1.0), unsupported_count_3run=0, ship_bar_met=False (bar 4). tests/unit/test_eval_runner.py::test_live_backend_without_enable_live_is_refused passes"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:40:38Z qa: claimed
- 2026-11-02T02:41:37Z qa: Cause: app.llm.provider.backend_name() serves fixture for any live backend without ENABLE_LIVE=1 (D-008/D-020, by design; no app/llm change needed). Without ENABLE_LIVE the runner reported backend=fixture silently. Fix in evals/run.py: refuse (exit 2) with explicit message when a live backend is requested w/o ENABLE_LIVE and no injected pipeline; test added. Live 3-run launched in background, log /private/tmp/claude-501/live_eval_T070.log
- 2026-11-02T02:55:46Z qa: AC 1 checked: evals/reports/20261102T025219Z.md: backend=claude-cli (sonnet-5-5/haiku-5-5), 3 live runs measured: determinism_3run=0.0 (bar 1.0), unsupported_count_3run=0, ship_bar_met=False (bar 4). tests/unit/test_eval_runner.py::test_live_backend_without_enable_live_is_refused passes
- 2026-11-02T02:55:46Z qa: moved in_progress -> in_review
- 2026-11-02T02:56:06Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T03:02:22Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-070-staff-engineer.md; round 1; findings:
    - [major] Guard matches the raw LLM_BACKEND string, so padded or mixed-case live names still run as fixture — fix: Normalise and validate the name before the check: backend = (a.backend or os.environ.get("LLM_BACKEND", "fixture")).strip(); refuse (rc 2, same message, no report written) any value not in ("fixture",) + LIVE_BACKENDS, since an unknown name is an error, not a fixture run. Keep the
    - [minor] No unit assertion that a correctly configured live run reaches the pipeline — fix: Add a test with ENABLE_LIVE=1 and LLM_BACKEND=claude-cli, monkeypatching load_pipeline (or passing a fake pipeline is not enough, since the guard skips injected pipelines) to a recorder, and assert the run proceeds past the guard (rc != 2).
- 2026-11-02T03:02:22Z qa: claimed

## Handoff
What changed: cause = app.llm.provider.backend_name() serves fixture for live backends without ENABLE_LIVE=1 (D-008/D-020, by design, no app/llm change). evals/run.py now refuses (exit 2, explicit message) when a live backend is requested without ENABLE_LIVE and no injected pipeline; test added. How verified: LLM_BACKEND=claude-cli alone -> rc=2; with ENABLE_LIVE=1 python -m evals.run --runs 3 -> evals/reports/20261102T025219Z.md (latest.json was since overwritten by a fixture run, use the timestamped file). Result: backend=claude-cli, ship_bar_met=False, unsupported_count_3run=0, determinism_3run=0.0 (needs 1.0; runs 2,3 differ from run 1 in entries/amounts/flags signature), entry_recall 0.982 (case_06 E3 excerpt miss). What's left: backend/prompt owner to investigate live nondeterminism (temperature/ordering in signature) - R-CO-7 bar. Surprise: evals/reports/latest.json is clobbered by any later run.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:49.961Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "LIVE_BACKENDS = (\"claude-cli\", \"anthropic-api\")\nNOT_MEASURED",
 "new_string": "LIVE_BACKENDS = (\"claude-cli\", \"anthropic-api\")\nKNOWN_BACKENDS = (\"fixture\",) + LIVE_BACKENDS\nNOT_MEASURED"
}
````

### User / tool · 2026-11-02T03:02:50.024Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:51.228Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "def main(argv=None, pipeline=None):\n    ap = argparse.ArgumentParser(prog=\"python -m evals.run\")",
 "new_string": "def normalize_backend(raw):\n    \"\"\"T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli\n    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;\n    the caller must exit 2 rather than fall back to fixtures.\"\"\"\n    name = (raw or \"\").strip().lower() or \"fixture\"\n    return name if name in KNOWN_BACKENDS else None\n\n\ndef main(argv=None, pipeline=None):\n    ap = argparse.ArgumentParser(prog=\"python -m evals.run\")"
}
````

### User / tool · 2026-11-02T03:02:51.286Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:52.752Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    backend = a.backend or os.environ.get(\"LLM_BACKEND\", \"fixture\")\n    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get(\"ENABLE_LIVE\") != \"1\":   # an injected (fake) pipeline never reaches the provider",
 "new_string": "    raw = a.backend if a.backend is not None else os.environ.get(\"LLM_BACKEND\", \"\")\n    backend = normalize_backend(raw)\n    if backend is None:\n        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).\n        print(f\"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). \"\n              f\"Nothing was run.\", file=sys.stderr)\n        return 2\n    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get(\"ENABLE_LIVE\") != \"1\":   # an injected (fake) pipeline never reaches the provider"
}
````

### User / tool · 2026-11-02T03:02:52.805Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:54.182Z

Guard is in place. Now the tests: parametrized refusal cases, a normalization check, and the minor's "live run proceeds past the guard" assertion.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:02:59.744Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_eval_runner.py <<'EOF'\n\n\n@pytest.mark.parametrize(\"raw\", [\" claude-cli \", \"Claude-CLI\", \"CLAUDE-CLI\\n\", \"\\tanthropic-api  \", \"Anthropic-API\"])\ndef test_padded_or_mixed_case_live_backend_without_enable_live_is_refused(raw, monkeypatch, tmp_path, capsys):\n    \"\"\"T-070 r2 (staff-engineer major): the guard must see the normalized name, or ' claude-cli ' runs on fixtures and writes backend=fixture.\"\"\"\n    monkeypatch.setenv(\"LLM_BACKEND\", raw)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    assert R.main([\"--out\", str(tmp_path)]) == 2\n    assert \"ENABLE_LIVE=1\" in capsys.readouterr().err\n    assert not list(tmp_path.glob(\"*.json\"))\n\n\n@pytest.mark.parametrize(\"raw\", [\"openai\", \"claude\", \"claude-cli-x\", \"anthropic\", \"fixtures\", \"lol\"])\ndef test_unknown_backend_name_exits_2_with_a_clear_message(raw, monkeypatch, tmp_path, capsys):\n    \"\"\"T-070 r2: a value that is not a known backend is an error, never a silent fixture run.\"\"\"\n    monkeypatch.setenv(\"LLM_BACKEND\", raw)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    assert R.main([\"--out\", str(tmp_path)]) == 2\n    err = capsys.readouterr().err\n    assert \"unknown LLM_BACKEND\" in err and \"Nothing was run\" in err\n    assert not list(tmp_path.glob(\"*.json\"))\n\n\n@pytest.mark.parametrize(\"flag\", [\"openai\", \" Claude-Cli  \", \"Fixture!\"])\ndef test_backend_flag_is_validated_like_the_env_var(flag, monkeypatch, tmp_path, capsys):\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    rc = R.main([\"--backend\", flag, \"--out\", str(tmp_path)])\n    assert rc == 2\n    assert not list(tmp_path.glob(\"*.json\"))\n    if flag.strip().lower() == \"claude-cli\":                # a known backend in odd case is refused by the ENABLE_LIVE guard, not 'unknown'\n        assert \"ENABLE_LIVE=1\" in capsys.readouterr().err\n    else:\n        assert \"unknown LLM_BACKEND\" in capsys.readouterr().err\n\n\n@pytest.mark.parametrize(\"raw,expected\", [\n    (None, \"fixture\"), (\"\", \"fixture\"), (\"   \", \"fixture\"), (\"fixture\", \"fixture\"), (\"FIXTURE \", \"fixture\"),\n    (\" claude-cli \", \"claude-cli\"), (\"Claude-CLI\", \"claude-cli\"), (\"\\tANTHROPIC-API\\n\", \"anthropic-api\"),\n    (\"openai\", None), (\"claude\", None), (\"claude-cli ok\", None),\n])\ndef test_normalize_backend_strips_lowercases_and_rejects_unknown(raw, expected):\n    assert R.normalize_backend(raw) == expected\n\n\ndef test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name(monkeypatch, tmp_path):\n    \"\"\"T-070 r2 minor: with ENABLE_LIVE=1 a padded, mixed-case live name passes the guard and the run is built with the normalized backend.\"\"\"\n    seen = []\n    def fake_build(pipeline, backend, runs=3, **kw):\n        seen.append((backend, runs))\n        return {\"ship_bar_met\": False, \"backend\": backend, \"blockers\": []}\n    monkeypatch.setattr(R, \"build_report\", fake_build)\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.setattr(R, \"write_report\", lambda r, outdir=None: tmp_path / \"x.json\")\n    monkeypatch.setenv(\"LLM_BACKEND\", \" Claude-CLI \")\n    monkeypatch.setenv(\"ENABLE_LIVE\", \"1\")\n    rc = R.main([\"--out\", str(tmp_path)])\n    assert rc == 1                                           # ship bar not met by the stub, but the run proceeded past the guard\n    assert seen == [(\"claude-cli\", 3)]\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py 2>&1 | tail -15",
 "description": "Append parametrized backend-normalization tests and run runner tests"
}
````

### User / tool · 2026-11-02T03:03:02.093Z

**tool result**
````
................................................................         [100%]
64 passed in 1.99s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:05.755Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- evals/run.py tests/unit/test_eval_runner.py && git diff -- evals/run.py | head -80 && git log --oneline -3 -- evals/run.py",
 "description": "Review diff of the two files before committing"
}
````

### User / tool · 2026-11-02T03:03:05.918Z

**tool result**
````
 evals/run.py                   | 17 +++++++++++-
 tests/unit/test_eval_runner.py | 59 ++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 75 insertions(+), 1 deletion(-)
diff --git a/evals/run.py b/evals/run.py
index eb3b0e2..0b5059f 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -30,6 +30,7 @@ GOLD = ROOT / "evals" / "golden"
 REPORTS = ROOT / "evals" / "reports"
 REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
 LIVE_BACKENDS = ("claude-cli", "anthropic-api")
+KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
 NOT_MEASURED = {"value": None, "status": "not_measured"}
 
 THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
@@ -649,6 +650,14 @@ def refuse_curated(env=None):
                               "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")
 
 
+def normalize_backend(raw):
+    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
+    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
+    the caller must exit 2 rather than fall back to fixtures."""
+    name = (raw or "").strip().lower() or "fixture"
+    return name if name in KNOWN_BACKENDS else None
+
+
 def main(argv=None, pipeline=None):
     ap = argparse.ArgumentParser(prog="python -m evals.run")
     ap.add_argument("--check-fresh", action="store_true")
@@ -676,7 +685,13 @@ def main(argv=None, pipeline=None):
     except CuratedFixtures as e:
         print(f"evals.run: {e}", file=sys.stderr)
         return 2
-    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
+    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
+    backend = normalize_backend(raw)
+    if backend is None:
+        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
+        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
+              f"Nothing was run.", file=sys.stderr)
+        return 2
     if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
         # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
         # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
815d616 fix(evals): refuse live backend without ENABLE_LIVE instead of silently running fixture (T-070)
bee1844 feat(evals): score unsplit_paste (D-031) in evals.run; report on recorded fixtures (T-057 minor)
d6a89ad fix(evals): judge-unavailable is never a catch; reported separately and makes bar 4 not_measured (T-038)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:10.563Z

Diff is scoped to my two files. Staging and committing those paths now.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:11.595Z

**tool call — Bash**
````
{
 "command": "git add evals/run.py tests/unit/test_eval_runner.py && git commit -m \"fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)\" -m \"Strip and lower-case the requested backend so ' Claude-CLI ' is guarded like claude-cli; any unknown value exits 2 instead of running fixtures. Adds parametrized tests.\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/run.py tests/unit/test_eval_runner.py && git rev-parse --short HEAD",
 "description": "Stage eval runner files and commit with trailer"
}
````

### User / tool · 2026-11-02T03:03:11.661Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git add evals/run.py tests/unit/test_eval_runner.py && git commit -m "fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)" -m "Strip and lower-case the requested backend so
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:12.775Z

The git guard wants staging and committing as separate commands. Splitting them.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:13.203Z

**tool call — Bash**
````
{
 "command": "git add evals/run.py tests/unit/test_eval_runner.py && git diff --cached --stat",
 "description": "Stage the two eval runner files"
}
````

### User / tool · 2026-11-02T03:03:13.310Z

**tool result**
````
 evals/run.py                   | 17 +++++++++++-
 tests/unit/test_eval_runner.py | 59 ++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 75 insertions(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:13.988Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)\" -m \"Strip and lower-case the requested backend so ' Claude-CLI ' is guarded like claude-cli; any unknown value exits 2 instead of running fixtures. Adds parametrized tests.\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/run.py tests/unit/test_eval_runner.py && git rev-parse --short HEAD",
 "description": "Commit the two eval runner files with trailer"
}
````

### User / tool · 2026-11-02T03:03:14.273Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 20471a7] fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)
 2 files changed, 75 insertions(+), 1 deletion(-)
20471a7
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:16.163Z

Committed as 20471a7. Recording it on the board, posting the provider note for backend, then handing off.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:19.679Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B commit T-070 --sha 20471a7 --agent qa && $B note T-070 --agent qa --text \"round 2: evals/run.py normalises LLM_BACKEND (strip+lower) via normalize_backend(); unknown values exit 2 with 'unknown LLM_BACKEND' message; live guard uses normalized name. 64 tests pass in tests/unit/test_eval_runner.py incl. 5 padded/mixed-case refusals, 6 unknown-name refusals, --backend flag, normalize mapping, and padded live run reaching build_report with 'claude-cli'.\" && $B note T-070 --agent qa --text \"for backend (not edited by qa): app/llm/provider.py backend_name() strips but does not lower-case. Without ENABLE_LIVE it returns 'fixture' for any non-fixture name (so 'Claude-CLI' or 'openai' silently serves fixtures); with ENABLE_LIVE=1, 'Claude-CLI' raises UNKNOWN_BACKEND. Suggest the same strip+lower normalisation there so both sides agree on the name.\" && $B ac T-070 --check 1 --agent qa --evidence \"tests/unit/test_eval_runner.py::test_live_backend_without_enable_live_is_refused and ::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused pass (commit 20471a7); prior live report evals/reports/20261102T025219Z.md\" && $B handoff T-070 --agent qa --text \"What changed: evals/run.py normalize_backend() strips and lower-cases LLM_BACKEND/--backend before the ENABLE_LIVE guard; unknown names exit 2 ('unknown LLM_BACKEND ... Nothing was run'). Test file adds parametrized refusals for padded/mixed-case live names and unknown names, a --backend flag test, a normalize mapping test, and a padded live run that reaches build_report as 'claude-cli' (staff minor). How verified: .venv/bin/python -m pytest -q tests/unit/test_eval_runner.py -> 64 passed. What's left: provider.py lower-casing is for backend (noted on card); live nondeterminism (determinism_3run=0.0) remains a separate card T-075. Surprise: the git-guard rejects 'git add && git commit' in one command; stage and commit separately.\"",
 "description": "Record commit, notes, AC evidence and handoff on board"
}
````

### User / tool · 2026-11-02T03:03:20.040Z

**tool result**
````
T-070: commit 20471a7 recorded
noted on T-070
noted on T-070
AC 1 checked: tests/unit/test_eval_runner.py::test_live_backend_without_enable_live_is_refused and ::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused pass (commit 20471a7); prior live report evals/reports/20261102T025219Z.md
handoff written on T-070
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:21.276Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py move T-070 in_review --agent qa && python3 tools/board.py show T-070 | head -12",
 "description": "Move T-070 to in_review and confirm status"
}
````

### User / tool · 2026-11-02T03:03:21.458Z

**tool result**
````
T-070: in_progress -> in_review
---
id: "T-070"
title: "Live eval: evals.run honors LLM_BACKEND=claude-cli (reported backend=fixture)"
milestone: "M2"
role: "qa"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:40:24Z"
updated_at: "2026-11-02T03:03:21Z"
claimed_by: "qa"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:22.679Z

T-070 round 2 is in review at commit 20471a7: `evals/run.py` now strips and lower-cases `LLM_BACKEND` before the ENABLE_LIVE guard, and any unknown name exits 2. `tests/unit/test_eval_runner.py` passes (64 tests). The provider-side normalization is posted as a card note for backend, not edited.
