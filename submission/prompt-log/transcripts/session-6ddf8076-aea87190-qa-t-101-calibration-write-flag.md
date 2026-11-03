# Subagent: QA: T-101 calibration write flag (QA: T-101 calibration write flag)

Source: `agent-aea871904f36a31cf.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:21:18.985Z

You own board card T-101 (claimed by "qa") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-101`.

Every `python -m evals.run` rewrites the committed evals/reports/calibration.json, so workers' runs keep dirtying the shared tree. Change evals/run.py so a plain run leaves calibration.json untouched; it may write a scratch copy under evals/reports/runs/ instead. A new `--write-calibration` flag writes the committed file, but only on a clean tree (`git status --porcelain` is empty for tracked files) at HEAD, and it records the provenance header as T-090 defined it. Add tests for both behaviours.

Then restore the dirty working-tree calibration.json from HEAD: `git show HEAD:evals/reports/calibration.json > evals/reports/calibration.json`. Commit with `git add <paths>` and then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Then `board.py ac`, the handoff, and `move T-101 in_review --agent qa`. Reply in 1 line.

### User / tool · 2026-11-02T05:21:18.989Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:20.813Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-101 && echo ---- && python3 tools/board.py show T-090 && echo ---- && git status --porcelain && echo ---- && git log --oneline -3 && echo ---- && cat evals/run.py && ls evals evals/reports tests tests/unit 2>/dev/null",
 "description": "Show card T-101, T-090, git state, and eval runner"
}
````

### User / tool · 2026-11-02T05:21:21.065Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:23.785Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-101; echo ----; git status --porcelain; echo ----; git log --oneline -3; echo ----; wc -l evals/run.py; ls evals evals/reports tests tests/unit 2>&1 | head -60",
 "description": "Show T-101 card, git status, and eval directory listing"
}
````

### User / tool · 2026-11-02T05:21:24.039Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:25.995Z

**tool call — Bash**
````
{
 "command": "git status --porcelain -- evals tests tools | head -40; echo ----; git log --oneline -3; echo ----; wc -l evals/run.py; ls -la evals evals/reports | head -60; echo ----; ls tests tests/unit 2>&1 | head -80",
 "description": "Check status of owned paths and list eval/test files"
}
````

### User / tool · 2026-11-02T05:21:26.151Z

**tool result**
````
 M evals/reports/calibration.json
 M evals/reports/latest.json
 D tests/fixtures/llm/curated/1db15db3cba3733c5e00a8732ecddb694b45c2637be29b83e3bfa35576123f24.json
 D tests/fixtures/llm/curated/b8bf558be04cc588cd8da6cbb2e7678ce1d970a0dceeb367ddc03c19ccb87729.json
D  tests/unit/_pdf_probe.py
MM tests/unit/test_billing.py
 M tests/unit/test_flags_injection.py
 M tests/unit/test_flags_pass.py
D  tests/unit/test_pdf_hidden_r2.py
D  tests/unit/test_pdf_ocr_limits.py
 M tests/unit/test_pipeline.py
 M tests/unit/test_spanish_records.py
 M tests/unit/test_t075_determinism.py
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
?? evals/reports/20261102T024653Z.md
?? evals/reports/20261102T024822Z.md
?? evals/reports/20261102T025055Z.md
?? evals/reports/20261102T025526Z.md
?? evals/reports/20261102T030405Z.md
?? evals/reports/20261102T031209Z.md
?? evals/reports/20261102T032024Z.md
?? evals/reports/20261102T043845Z.md
?? evals/reports/20261102T051136Z.md
?? evals/reports/controls-20261102T043911Z.json
?? evals/reports/controls-20261102T043911Z.md
?? evals/reports/controls-20261102T044933Z.json
?? evals/reports/controls-20261102T044933Z.md
?? evals/reports/controls-20261102T045207Z.json
?? evals/reports/controls-20261102T045207Z.md
?? evals/reports/runs/20261102T042232Z/
?? evals/reports/runs/20261102T045543Z/
?? evals/reports/runs/20261102T051136Z/
----
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
e63e564 docs: D-051 code checks bind accept for every item
----
    1149 evals/run.py
evals:
total 368
drwxr-xr-x@ 12 arsis  staff    384 Nov  1 22:30 .
drwxr-xr-x  27 arsis  staff    864 Nov  1 20:37 ..
-rw-r--r--@  1 arsis  staff      0 Nov  1 19:49 __init__.py
drwxr-xr-x@  3 arsis  staff     96 Nov  1 22:23 adversarial
drwxr-xr-x@ 32 arsis  staff   1024 Nov  1 22:23 golden
-rw-r--r--@  1 arsis  staff  18635 Nov  1 20:14 lexicon_heldout.jsonl
drwxr-xr-x@ 32 arsis  staff   1024 Nov  1 22:10 library
-rw-r--r--@  1 arsis  staff  87051 Nov  1 22:11 library_build_v2.py
-rw-r--r--@  1 arsis  staff   2756 Nov  1 22:20 library_report.py
-rw-r--r--@  1 arsis  staff   2577 Nov  1 19:49 matching.py
drwxr-xr-x@ 46 arsis  staff   1472 Nov  1 23:11 reports
-rw-r--r--@  1 arsis  staff  69130 Nov  1 22:47 run.py

evals/reports:
total 728
drwxr-xr-x@ 46 arsis  staff   1472 Nov  1 23:11 .
drwxr-xr-x@ 12 arsis  staff    384 Nov  1 22:30 ..
-rw-r--r--@  1 arsis  staff   2694 Nov  1 20:08 20261102T020824Z.md
-rw-r--r--@  1 arsis  staff   2791 Nov  1 20:09 20261102T020933Z.md
-rw-r--r--@  1 arsis  staff   2605 Nov  1 20:10 20261102T021029Z.md
-rw-r--r--@  1 arsis  staff   2732 Nov  1 20:10 20261102T021046Z.md
-rw-r--r--@  1 arsis  staff   2737 Nov  1 20:27 20261102T022701Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:29 20261102T022927Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:30 20261102T023039Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:31 20261102T023155Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023203Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023204Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023208Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:36 20261102T023603Z.md
-rw-r--r--@  1 arsis  staff   2883 Nov  1 20:39 20261102T023911Z.md
-rw-r--r--@  1 arsis  staff   2966 Nov  1 20:39 20261102T023916Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:43 20261102T024348Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:43 20261102T024355Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:46 20261102T024653Z.md
-rw-r--r--@  1 arsis  staff   2831 Nov  1 20:48 20261102T024822Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:50 20261102T025055Z.md
-rw-r--r--@  1 arsis  staff   2708 Nov  1 20:52 20261102T025219Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:55 20261102T025526Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:57 20261102T025715Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 21:04 20261102T030405Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 21:12 20261102T031209Z.md
-rw-r--r--@  1 arsis  staff   3008 Nov  1 21:20 20261102T032024Z.md
-rw-r--r--@  1 arsis  staff   2884 Nov  1 21:28 20261102T032823Z.md
-rw-r--r--@  1 arsis  staff   3407 Nov  1 21:57 20261102T035750Z.md
-rw-r--r--@  1 arsis  staff   3559 Nov  1 22:09 20261102T040933Z.md
-rw-r--r--@  1 arsis  staff  10094 Nov  1 22:38 20261102T043845Z.md
-rw-r--r--@  1 arsis  staff  10022 Nov  1 23:11 20261102T051136Z.md
-rw-r--r--@  1 arsis  staff   6816 Nov  1 23:11 calibration.json
-rw-r--r--@  1 arsis  staff  26485 Nov  1 22:25 controls-20261102T042306Z.json
-rw-r--r--@  1 arsis  staff   6556 Nov  1 22:25 controls-20261102T042306Z.md
-rw-r--r--@  1 arsis  staff  26497 Nov  1 22:41 controls-20261102T043911Z.json
-rw-r--r--@  1 arsis  staff   6557 Nov  1 22:41 controls-20261102T043911Z.md
-rw-r--r--@  1 arsis  staff  26483 Nov  1 22:52 controls-20261102T044933Z.json
-rw-r--r--@  1 arsis  staff   6557 Nov  1 22:52 controls-20261102T044933Z.md
-rw-r--r--@  1 arsis  staff  26403 Nov  1 22:54 controls-20261102T045207Z.json
-rw-r--r--@  1 arsis  staff   6543 Nov  1 22:54 controls-20261102T045207Z.md
-rw-r--r--@  1 arsis  staff   8669 Nov  1 21:44 determinism-diagnosis.md
-rw-r--r--@  1 arsis  staff  53668 Nov  1 23:11 latest.json
----
tests:
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit

tests/unit:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
_pdf_probe.py
_pdf_raw.py
language_routing_heldout.jsonl
spanish_translation_pairs.jsonl
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_backend_no_speaker_label.py
test_billing.py
test_boundaries.py
test_calibration_route.py
test_case_extras.py
test_confidence.py
test_conflict_candidates.py
test_conflicts.py
test_date_convention.py
test_date_unconfirmed.py
test_dates.py
test_db.py
test_dismissal_patterns.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_frontend_no_speaker_label.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_ingest.py
test_injection.py
test_judge_guard.py
test_judges.py
test_language_routing_heldout.py
test_library_denylist.py
test_manual_and_split.py
test_multicase.py
test_narrative.py
test_ocr_invariant.py
test_pdf_checks_api.py
test_pdf_hidden.py
test_pdf_hidden_r2.py
test_pdf_ocr.py
test_pdf_ocr_limits.py
test_pdf_upload.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_reclassify.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_spanish_failsafe.py
test_spanish_records.py
test_speaker.py
test_split_llm.py
test_t033_backend.py
test_t037_backend.py
test_t075_determinism.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:29.498Z

**tool call — Bash**
````
{
 "command": "grep -n \"calibration\\|provenance\\|argparse\\|add_argument\\|def main\\|reports\\|latest.json\\|def _write\\|json.dump\\|write_text\" evals/run.py | head -120",
 "description": "Find calibration and output-writing code in eval runner"
}
````

### User / tool · 2026-11-02T05:21:29.585Z

**tool result**
````
2:evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
6:    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
17:import argparse
30:REPORTS = ROOT / "evals" / "reports"
69:    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
247:def score_calibration(exp, out, unscored=None):
287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
288:    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
319:    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
326:                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
339:    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
342:    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
343:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
473:                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
620:    return sorted(rows, key=lambda r: json.dumps(r, sort_keys=True, default=str))
649:    return json.dumps(signature_parts(out), sort_keys=True, default=str)
659:            ja, jb = [json.dumps(x, sort_keys=True, default=str) for x in a[k]], [json.dumps(x, sort_keys=True, default=str) for x in b[k]]
662:            d[k] = {"first": json.dumps(a.get(k), sort_keys=True, default=str)[:500], "other": json.dumps(b.get(k), sort_keys=True, default=str)[:500]}
698:    """Write evals/reports/runs/<ts>/<fname>.json. Refuses (raises) if anything secret-looking would be written."""
701:    body = json.dumps(run_artifact(out, name, run), indent=1, sort_keys=True, default=str) + "\n"
706:    (d / f"{fname}.json").write_text(body)
917:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
956:def render_calibration(c):
971:    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
990:    L += render_calibration(r.get("calibration"))
992:    L += [f"Assertions: {json.dumps(r['assertions'])}", f"spec_matches_golden: {r['spec_matches_golden']}", "",
993:          "## Misses (report what was found)", "", f"- entry misses: {json.dumps(m['entry_recall']['misses'])}",
994:          f"- missed must flags: {json.dumps(m['flag_recall']['missed_must'])}", f"- grounding failures: {json.dumps(m['grounding_rate']['failures'])}",
995:          f"- seeded hallucinations not caught: {h['missed']}", f"- must_not detail: {json.dumps(m['golden_must_not_hits']['detail'])}", "",
997:          *( ["- determinism differences: " + json.dumps(m["determinism_3run"]["differences"])] if m["determinism_3run"].get("differences") else [] ),
1006:    (outdir / f"{ts}.md").write_text(render_md(r))
1007:    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
1008:    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
1013:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1014:    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
1017:        print("check-fresh: no latest.json", file=sys.stderr)
1023:    bad = check_calibration(p.parent / "calibration.json", root)
1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
1029:def check_calibration(path, root=ROOT):
1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
1041:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
1080:    """Live J3/J4 controls alone (no pipeline): per-item verdicts on every repeat, written next to the other reports."""
1087:    (out / f"controls-{ts}.md").write_text("\n".join(md) + "\n")
1088:    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
1094:def main(argv=None, pipeline=None):
1095:    ap = argparse.ArgumentParser(prog="python -m evals.run")
1096:    ap.add_argument("--check-fresh", action="store_true")
1097:    ap.add_argument("--check-spec", action="store_true")
1098:    ap.add_argument("--backend", default=None)
1099:    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
1100:    ap.add_argument("--out", default=str(REPORTS))
1101:    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
1105:        return check_fresh(out / "latest.json")
1108:        latest = out / "latest.json"
1114:        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
1115:        print(json.dumps(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:30.827Z

**tool call — Bash**
````
{
 "command": "sed -n 55,110p evals/run.py; echo ......; sed -n 895,1149p evals/run.py",
 "description": "Read calibration provenance and main/write logic in evals/run.py"
}
````

### User / tool · 2026-11-02T05:21:30.913Z

**tool result**
````
    return norm(s).lower()


def ratio(num, den):
    return None if den == 0 else num / den


def golden_cases():
    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]


def git_source(root=ROOT):
    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
    import subprocess
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        tree = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        return {"commit": head, "clean": not dirty, "tree": tree}
    except Exception:
        return {"commit": None, "clean": None, "tree": None}


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def hashes(root=ROOT):
    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
    out = {}
    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
        out[p.relative_to(root).as_posix()] = sha256_file(p)
    lex = root / "app" / "llm" / "lexicon.yaml"
    if lex.exists():
        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
    return out


def split_regex_text(s):
    return re.sub(r'"[^"]*"', " ", s or "")


def regex_hits(mn, text):
    """Golden must_not regex semantics (README): strip double-quoted spans, ignore a match when unless_context matches the 80 chars before it."""
    s = split_regex_text(text)
    rx = re.compile(mn["pattern"])
    ctx = re.compile(mn["unless_context"]) if mn.get("unless_context") else None
    return [m.group(0) for m in rx.finditer(s) if not (ctx and ctx.search(s[max(0, m.start() - 80):m.start()]))]


# ---------------------------------------------------------------- per-case scoring (pure; tested with fake pipeline output)
def product_entries(out):
    return list(out.get("entries") or []) + list(out.get("undated_entries") or [])

......
    sample = next(t for n, t, _ in cases if n == "sample")
    if backend in LIVE_BACKENDS:
        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
    else:
        m["determinism_3run"] = dict(NOT_MEASURED, r_ids=RIDS["determinism_3run"])
        m["unsupported_count_3run"] = dict(NOT_MEASURED, r_ids=RIDS["unsupported_count_3run"])
    if lexicon_flags is None:
        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
        lexicon_flags = FL.lexicon_flags
    m["lexicon_recall_must_flags"] = lexicon_recall(lexicon_flags, cases)
    if judge_control is None:
        m["judge_controls"] = {"status": "not_measured", "value": None, "reason": "no judge_control supplied", "r_ids": ["R-CO-2", "R-CO-3"]}
    else:
        m["judge_controls"] = judge_controls_metrics(load_controls(), judge_control, repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1)
    a = assertions(results)
    spec = check_spec(req_path)
    sample_out = outs.get("sample", {})
    source = git_source()
    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
              "thresholds": THRESHOLDS, "cases": list(results)}
    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
    if runs_dir is not None:
        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
    met, bars, blockers = evaluate_report(report)
    report.update(ship_bar_met=met, bars=bars, blockers=blockers)
    return report


# ---------------------------------------------------------------- output
def pct(x):
    return "n/a" if x is None else f"{x:.3f}"


def render_controls(jc):
    if not jc or "j3" not in jc:
        return ["| judge_controls (J3/J4 seeded) | not_measured | catch every wrong item on every repeat, 0 false agree | R-CO-2 |"]
    L = []
    for j in ("j3", "j4"):
        x = jc[j]
        sp = "; ".join(f"{k.replace('_', '-')} {v['wrong_caught']}/{v['wrong_total']}" for k, v in x.get("by_split", {}).items())
        L.append(f"| {j.upper()} {x['prompt']} seeded catch rate | {pct(x['catch_rate'])} ({x['wrong_caught']}/{x['wrong_total']} wrong caught x{x.get('repeats', 1)} runs; {sp}; "
                 f"false agree {len(x['false_agree'])} {x['false_agree']}; correct accepted {x['correct_accepted']}/{x['correct_total']}; "
                 f"unstable {x.get('unstable', [])}; unavailable {len(x['judge_unavailable_ids'])}) | all wrong caught, 0 false agree | R-CO-2 |")
    return L


def render_control_items(jc):
    """Per-item verdict on every repeat. in-sample controls share authors and rules with the prompts (not independent evidence); held-out controls were written
    before the next prompt edit."""
    if not jc or "rows" not in jc:
        return []
    L = ["", "## Judge controls, per item", "", "In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. "
         "A wrong item is caught when no repeat confirms it.", "", "| id | judge | split | kind | pair | expected | verdict per run | ok |", "|---|---|---|---|---|---|---|---|"]
    for r in jc["rows"]:
        ok = (r["verdict"] not in (POSITIVE[r["judge"]], "unavailable")) if r["kind"] == "wrong" else all(v == POSITIVE[r["judge"]] for v in r["verdicts"])
        L.append(f"| {r['id']} | {r['judge']} | {r['split'].replace('_', '-')} | {r['kind']} | {r.get('pair') or ''} | {r['expected']} | {' / '.join(r['verdicts'])} | {'yes' if ok else 'NO'} |")
    return L + [""]


def render_calibration(c):
    """Calibrated confidence (T-090): counts per state and per type, backend named, no percentages."""
    if not c:
        return []
    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases, source commit `{(c.get('source_commit') or 'unknown')[:10]}`)", ""]
    L += [f"- {c['sentences']['overall'][s]}" for s in CAL_STATES]
    L += ["", "| Item type | Verified (matched/seen) | Needs review (matched/seen) |", "|---|---|---|"]
    for t in CAL_TYPES:
        v, n = c["by_type"][t]["verified"], c["by_type"][t]["needs_review"]
        L.append(f"| {t} | {v['matched']}/{v['total']} | {n['matched']}/{n['total']} |")
    return L + [""]


def render_md(r):
    m = r["metrics"]
    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
    if r["blockers"]:
        L += ["Blockers: " + "; ".join(r["blockers"]), ""]
    L += ["| Metric | Value | Bar | R-IDs |", "|---|---|---|---|"]
    L += [f"| grounding_rate | {pct(m['grounding_rate']['value'])} ({m['grounding_rate']['checked']} checked) | 1.0 | {', '.join(RIDS['grounding_rate'])} |",
          f"| entry_recall | {pct(m['entry_recall']['value'])} | >= 0.95 | {', '.join(RIDS['entry_recall'])} |",
          f"| amount_recall | {pct(m['amount_recall']['value'])} | >= 0.95 | R-CH-1 |"]
    for t in FLAG_TYPES:
        L.append(f"| flag_precision[{t}] / flag_recall[{t}] | {pct(m['flag_precision'][t])} / {pct(m['flag_recall'][t])} | >= 0.9 each | R-FL-1..4 |")
    h = m["hallucination_catch_rate"]
    L += [f"| hallucination_catch_rate | {pct(h['value'])} ({h['caught']}/{h['total']}; {h['status']}; judge unavailable {h['judge_unavailable_count']}) | >= 0.95 | R-TL-4, R-TL-10 |",
          f"| controls judged unsupported | {len(h['controls_unsupported'])} of {h['controls_total']} | 0 | R-TL-4 |",
          f"| unsupported_count_3run | {m['unsupported_count_3run'].get('value', 'not_measured')} | 0 | R-TL-4 |",
          f"| determinism_3run | {m['determinism_3run'].get('value', 'not_measured')} | 1.0 | R-CO-7 |",
          *render_controls(m.get("judge_controls")),
          f"| golden_must_not_hits | {m['golden_must_not_hits']['value']} | 0 | R-CO-3 |",
          f"| unsplit_paste (LLM split, D-031) | {m['unsplit_paste']['value']} {m['unsplit_paste']['misses']} | true | R-IN-1 |",
          f"| case_07_total_420 | {m['case_07_total_420']['value']} | true | R-RV-6 |",
          f"| lexicon_recall_must_flags (reported, not gated) | {pct(m['lexicon_recall_must_flags'].get('value'))} | none (D-026) | R-FL-3, R-RV-6 |", ""]
    L += render_calibration(r.get("calibration"))
    L += render_control_items(m.get("judge_controls"))
    L += [f"Assertions: {json.dumps(r['assertions'])}", f"spec_matches_golden: {r['spec_matches_golden']}", "",
          "## Misses (report what was found)", "", f"- entry misses: {json.dumps(m['entry_recall']['misses'])}",
          f"- missed must flags: {json.dumps(m['flag_recall']['missed_must'])}", f"- grounding failures: {json.dumps(m['grounding_rate']['failures'])}",
          f"- seeded hallucinations not caught: {h['missed']}", f"- must_not detail: {json.dumps(m['golden_must_not_hits']['detail'])}", "",
          *( [f"- per-run artifacts: `{r['run_artifacts']}`"] if r.get("run_artifacts") else [] ),
          *( ["- determinism differences: " + json.dumps(m["determinism_3run"]["differences"])] if m["determinism_3run"].get("differences") else [] ),
          "", "## Prompt and lexicon hashes", ""] + [f"- `{k}` {v}" for k, v in r["hashes"].items()]
    return "\n".join(L) + "\n"


def write_report(r, outdir=REPORTS):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = r["generated_at"].replace(":", "").replace("-", "")
    (outdir / f"{ts}.md").write_text(render_md(r))
    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
    return outdir / f"{ts}.md"


def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
    p = pathlib.Path(latest_path)
    if not p.exists():
        print("check-fresh: no latest.json", file=sys.stderr)
        return 1
    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
    for k in diff:
        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
    bad = check_calibration(p.parent / "calibration.json", root)
    for m in bad:
        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
    return 1 if diff or bad else 0


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad


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


def normalize_backend(raw):
    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
    the caller must exit 2 rather than fall back to fixtures."""
    name = (raw or "").strip().lower() or "fixture"
    return name if name in KNOWN_BACKENDS else None


def run_controls_only(backend, out, ts):
    """Live J3/J4 controls alone (no pipeline): per-item verdicts on every repeat, written next to the other reports."""
    jc = judge_controls_metrics(load_controls(), default_judge_control(backend), repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1,
                                workers=4 if backend in LIVE_BACKENDS else 1)
    ok = controls_ok(jc)
    out.mkdir(parents=True, exist_ok=True)
    md = [f"# Judge controls {ts}", "", f"**controls_ok: {ok}**  backend `{backend}`  prompts `{control_prompt('j3')}`, `{control_prompt('j4')}` (hashes in the json)",
          "", "| Metric | Value | Bar | R-IDs |", "|---|---|---|---|", *render_controls(jc), *render_control_items(jc)]
    (out / f"controls-{ts}.md").write_text("\n".join(md) + "\n")
    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
                                                         "hashes": hashes(), "judge_controls": jc}, indent=1, sort_keys=True) + "\n")
    print(f"controls_ok={ok} backend={backend} report={out / f'controls-{ts}.md'}")
    return 0 if ok else 1


def main(argv=None, pipeline=None):
    ap = argparse.ArgumentParser(prog="python -m evals.run")
    ap.add_argument("--check-fresh", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
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
    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
    backend = normalize_backend(raw)
    if backend is None:
        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
              f"Nothing was run.", file=sys.stderr)
        return 2
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
    path = write_report(report, out)
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)


if __name__ == "__main__":
    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:40.680Z

**tool call — Bash**
````
{
 "command": "sed -n 316,350p evals/run.py; echo ....; grep -n \"write_report\\|calibration.json\\|git_source\\|source_commit\\|source_clean\\|provenance\" -r evals tests tools app --include=*.py | grep -v \"^evals/run.py:3[0-4]\" | head -60; echo ....; grep -n -i \"provenance\\|header\\|source\" board/cards/T-090.md | head -60",
 "description": "Read build_calibration and find callers and T-090 provenance definition"
}
````

### User / tool · 2026-11-02T05:21:40.803Z

**tool result**
````
def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
    names = list(results)
    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
    for n, r in results.items():
        for t in CAL_TYPES:
            for s in CAL_STATES:
                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
                c = cells[t][s]
                c["matched"] += m
                c["total"] += tot
                if tot:
                    c["by_case"][n] = [m, tot]
    by_state = {}
    for s in CAL_STATES:
        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
        by_state[s] = {"matched": m, "total": tot, "cases": cs}
    small_cases = len(names) < CAL_SMALL_N
    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)

    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
            "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
            "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
                          "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
            "not_scored": not_scored,
            "cases": names, "case_count": len(names), "small_sample": small_cases or any(by_state[s]["total"] < CAL_SMALL_N for s in CAL_STATES),
....
evals/run.py:67:def git_source(root=ROOT):
evals/run.py:912:    source = git_source()
evals/run.py:960:    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases, source commit `{(c.get('source_commit') or 'unknown')[:10]}`)", ""]
evals/run.py:1002:def write_report(r, outdir=REPORTS):
evals/run.py:1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
evals/run.py:1023:    bad = check_calibration(p.parent / "calibration.json", root)
evals/run.py:1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
evals/run.py:1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
evals/run.py:1141:    path = write_report(report, out)
tests/unit/test_t037_backend.py:101:    """T-037 AC2: every fixture file is a recorded answer with provenance; the recorder refuses text outside evals/golden."""
tests/unit/test_calibration_route.py:1:"""T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct
tests/unit/test_calibration_route.py:28:        "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642", "generated_at": "2026-11-02T04:48:31Z",
tests/unit/test_calibration_route.py:42:def write(tmp_path, doc, name="calibration.json"):
tests/unit/test_calibration_route.py:56:def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
tests/unit/test_calibration_route.py:60:    assert c["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
tests/unit/test_calibration_route.py:76:    assert body["status"] == "ok" and body["calibration"]["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
tests/unit/test_calibration_route.py:81:        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
tests/unit/test_calibration_route.py:112:    "missing_source_commit": lambda d: d.update(source_commit=""),
tests/unit/test_calibration_route.py:128:        p = tmp_path / "calibration.json"
tests/unit/test_api_routes.py:169:    assert ex["totals"]["charges_cents"] == 839000 and ex["provenance"]["backend"] == "fixture" and "counts" in ex
tests/unit/test_eval_runner.py:196:    R.write_report(full, tmp_path)
tests/unit/test_eval_runner.py:254:    R.write_report(good, tmp_path)
tests/unit/test_eval_runner.py:427:    monkeypatch.setattr(R, "write_report", lambda r, outdir=None: tmp_path / "x.json")
tests/unit/test_eval_runner.py:495:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
tests/unit/test_eval_runner.py:606:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
tests/unit/test_eval_runner.py:611:    R.write_report(rep, tmp_path)
tests/unit/test_eval_runner.py:612:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
tests/unit/test_eval_runner.py:616:# ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
tests/unit/test_eval_runner.py:618:CAL = R.REPORTS / "calibration.json"
tests/unit/test_eval_runner.py:633:def _require_source_commit(c):
tests/unit/test_eval_runner.py:637:    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
tests/unit/test_eval_runner.py:638:    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"
tests/unit/test_eval_runner.py:641:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
tests/unit/test_eval_runner.py:643:    assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
tests/unit/test_eval_runner.py:647:def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
tests/unit/test_eval_runner.py:649:    _require_source_commit(c)
tests/unit/test_eval_runner.py:650:    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
tests/unit/test_eval_runner.py:651:    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"
tests/unit/test_eval_runner.py:654:def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
tests/unit/test_eval_runner.py:656:    c["source_commit"] = "1" * 40
tests/unit/test_eval_runner.py:657:    forged = tmp_path / "calibration.json"
tests/unit/test_eval_runner.py:663:        _require_source_commit(_committed())
tests/unit/test_eval_runner.py:666:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
tests/unit/test_eval_runner.py:671:    _require_source_commit(c)
tests/unit/test_eval_runner.py:674:    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
tests/unit/test_eval_runner.py:680:    assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
tests/unit/test_eval_runner.py:681:    fresh = json.loads((out / "calibration.json").read_text())
tests/unit/test_eval_runner.py:682:    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
tests/unit/test_eval_runner.py:688:def test_git_source_reports_commit_and_dirtiness(tmp_path):
tests/unit/test_eval_runner.py:696:    a = R.git_source(tmp_path)
tests/unit/test_eval_runner.py:699:    assert R.git_source(tmp_path)["clean"] is False
tests/unit/test_eval_runner.py:701:    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None}
tests/unit/test_eval_runner.py:709:    (tmp_path / "calibration.json").write_text(json.dumps(cal))
tests/unit/test_eval_runner.py:712:    (tmp_path / "calibration.json").write_text(json.dumps(cal))
tests/unit/test_eval_runner.py:718:    (tmp_path / "calibration.json").write_text(json.dumps(cal))
tests/unit/test_eval_runner.py:729:    (tmp_path / "calibration.json").write_text(json.dumps(cal))
app/llm/backends/fixture.py:37:    """Record mode: store a live result keyed by the prompt hash, with provenance."""
app/backend/calibration_route.py:3:Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
app/backend/calibration_route.py:19:REPORT = ROOT / "evals" / "reports" / "calibration.json"
app/backend/calibration_route.py:24:SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
....
20:  - {"persona": "orchestrator-§7.4", "model": "claude-opus-5-5", "verdict": "pass", "file": "memory/SCOPE_CUTS.md", "at": "2026-11-02T04:55:58Z", "debt": "3 rounds; calibration reproducible from its recorded commit. Major (serving route) moved to T-099; minor (no-.git copy skips provenance tests) carried."}
22:  - {"n": 1, "text": "evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)", "done": true, "evidence": "calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)"}
37:    - [major] The sentence the UI will render verbatim names no backend and no provenance — fix: Put the backend and the golden-set basis into the sentence, for example 'Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases).' Build it in build_calibration so the UI cannot drop it.
44:- 2026-11-02T04:31:37Z qa: AC 1 checked: evals/reports/calibration.json generated from a clean worktree of 823b718 (source_commit, source_tree_clean=true, backend=fixture in header): verified 83/84, needs_review 10/10; tests/unit/test_eval_runner.py regenerates it from git archive of source_commit and compares; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed
45:- 2026-11-02T04:31:37Z qa: r2: commits 823b718 (code, tests) and 02ff244 (calibration.json from clean worktree 823b718, worktree removed). Blocker: header has source_commit, source_tree_clean, backend, hashes; tests: ancestor-of-HEAD, regenerate-from-source-commit equality, check-fresh fails on edited count/changed hashes. Major 2: AC 1 narrowed to the eval side, served field + UI line is T-096. Major 3: amount class test. Major 4: sentences name backend + golden set (+ 'recorded replies' for fixture). Minors: 29/30 boundary, tolerated flag, record_warning alignment (state now travels with the candidate, no zip), not_scored counts, check-fresh covers calibration.json. Nit: 7 tests originally, not 6; selector now gives 84. generated_at kept in file (test ignores it). Not done: latest.json/.md not regenerated (latest.json is the live claude-cli report). FOR FRONTEND T-096: sentences now end with backend+basis already, render verbatim.
49:    - [blocker] The r2 provenance fix and its tests are reverted at HEAD by commit 2fca530; the card's test evidence is not reproducible from HEAD — fix: Restore the 823b718 versions of evals/run.py and tests/unit/test_eval_runner.py in a new commit that stages those two paths explicitly (git show 823b718:evals/run.py and :tests/unit/test_eval_runner.py are the reference). Do not hand-merge the un
50:    - [major] A forged source_commit that names no existing commit passes the two provenance tests by skipping — fix: Skip only when there is no git repository (git rev-parse --git-dir fails). When a repository exists and the cited commit is missing, or the commit is not an ancestor of HEAD, fail with the commit name.
53:    - [minor] The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes — fix: Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.
55:- 2026-11-02T04:39:56Z orchestrator: r2 blocker (code reverted by 2fca530) is being restored by the revert audit; r3 then fixes the forged source_commit skip and moves the served field to T-096 (backend serve + UI).
58:- 2026-11-02T04:48:59Z qa: AC 1 checked: calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)
63:    - [minor] A copy without .git skips both provenance tests, so a forged source_commit passes with 3 skips — fix: When there is no repository, fail unless an explicit opt-out variable is set by the export step (for example CALIBRATION_EXPORT_NO_GIT=1), so an export that is meant to be checked cannot skip the guard silently.
66:- 2026-11-02T04:55:58Z orchestrator: accepted with documented debt (§7.4): 3 rounds; calibration reproducible from its recorded commit. Major (serving route) moved to T-099; minor (no-.git copy skips provenance tests) carried.
70:r3. Changed: r2 code confirmed in HEAD (a850be0); provenance tests now fail (not skip) on a missing or non-ancestor source_commit when a git repo exists, skip only with no repo; source_tree recorded and checked against git (replaces copying the clean flag); check_calibration rebuilds sentences from counts (calibration_sentences) so edited sentences fail check-fresh; calibration.json regenerated from a clean worktree of b85fc1b (83/84, 10/10), worktree removed. Verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; forged source_commit mutant fails 2 tests. Left: served field + UI line on T-096 (note with field shape posted). Surprise: shared tree's calibration.json had been overwritten by another run without provenance.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:45.889Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_eval_runner.py | head -60; echo ....; sed -n 180,260p tests/unit/test_eval_runner.py; echo ....; sed -n 410,450p tests/unit/test_eval_runner.py",
 "description": "Read eval runner test setup and main-related tests"
}
````

### User / tool · 2026-11-02T05:21:45.984Z

**tool result**
````
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
....
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
....
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
    monkeypatch.setattr(R, "write_report", lambda r, outdir=None: tmp_path / "x.json")
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:47.141Z

**tool call — Bash**
````
{
 "command": "sed -n 600,740p tests/unit/test_eval_runner.py",
 "description": "Read calibration provenance and regeneration tests"
}
````

### User / tool · 2026-11-02T05:21:47.228Z

**tool result**
````
    assert un == {"entry": 1, "amount": 2, "flag": 2}                          # rejected is excluded on purpose; duplicate and stateless flags are not
    c = R.build_calibration({"sample": {"calibration": {t: {"verified": [1, 1], "needs_review": [0, 0]} for t in R.CAL_TYPES}, "calibration_unscored": un}}, "fixture")
    assert c["not_scored"] == {"entry": 1, "amount": 2, "flag": 2, "total": 5}
    assert "Not scored: 5 produced items" in c["sentences"]["overall"]["verified"]


def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
    rep = good
    c = rep["calibration"]
    assert c["backend"] == rep["backend"] and c["cases"] == rep["cases"]
    assert c["by_state"]["verified"]["total"] == sum(rep["per_case"][n]["calibration"][t]["verified"][1] for n in rep["per_case"] for t in R.CAL_TYPES)
    R.write_report(rep, tmp_path)
    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
    assert "Calibrated confidence" in next(tmp_path.glob("2*.md")).read_text()


# ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
import os, shutil, subprocess, sys
CAL = R.REPORTS / "calibration.json"


def _git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)


def _committed():
    return json.loads(CAL.read_text())


def _has_git():
    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0


def _require_source_commit(c):
    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
    if not _has_git():
        pytest.skip("no git repository here (exported tree)")
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    c = _committed()
    assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")


def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
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
    c = _committed()
    _require_source_commit(c)
    src = tmp_path / "src"
    src.mkdir()
    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
    assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
    fresh = json.loads((out / "calibration.json").read_text())
    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
    assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
    assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
    assert c["source_tree_clean"] is True


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
    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None}


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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:18.124Z

**tool call — Bash**
````
{
 "command": "git status --porcelain -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json; echo \"rc=$?\"; git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py; echo ....; grep -n \"^def report\\|^def good\\|@pytest.fixture\" -A6 tests/unit/test_eval_runner.py | head -40; echo ....; git show HEAD:evals/reports/calibration.json | head -12; echo; cmp <(git show HEAD:evals/reports/calibration.json) evals/reports/calibration.json && echo SAME || echo DIFFERS",
 "description": "Check owned files are clean and inspect fixtures and committed calibration"
}
````

### User / tool · 2026-11-02T05:22:18.387Z

**tool result**
````
 M evals/reports/calibration.json
rc=0
....
82:def report(pipe=None, backend="claude-cli", **kw):
83-    kw.setdefault("lexicon_flags", gold_floor)
84-    kw.setdefault("judge_control", perfect_control)
85-    return R.build_report(pipe or Perfect(backend), backend, **kw)
86-
87:@pytest.fixture(scope="module")
88:def good():
89-    return report()
90-
91-def test_perfect_run_meets_ship_bar_on_a_live_backend(good):
92-    """AC1/AC6: with every metric at its bar on a live backend ship_bar_met is true and all named metrics carry R-IDs."""
93-    assert good["blockers"] == [] and good["ship_bar_met"] is True
94-    m = good["metrics"]
....
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,

/dev/fd/63 evals/reports/calibration.json differ: char 16, line 2
DIFFERS
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:20.064Z

**tool call — Bash**
````
{
 "command": "timeout 900 .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -15",
 "description": "Run baseline calibration and eval runner unit tests",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:22:20.149Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:21.386Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -15",
 "description": "Run baseline calibration and eval runner unit tests",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:22:29.233Z

**tool result**
````
        git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
>       assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
E       AssertionError: assert ({'needs_revie... 'total': 84}} == {'needs_revie... 'total': 85}}
E         
E         Differing items:
E         {'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', ...], 'matched': 83, 'total': 84}} != {'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', ...], 'matched': 84, 'total': 85}}
E         {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_06_subtle_pre_existing',...
E         
E         ...Full output truncated, use '-vv' to show)

tests/unit/test_eval_runner.py:683: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 114 passed, 1750 deselected in 7.46s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:31.636Z

**tool call — Bash**
````
{
 "command": "sed -n 1,16p evals/run.py; grep -n \"^ROOT\\|^REPORTS\\|^GOLD\" evals/run.py",
 "description": "Read eval runner module docstring and path constants"
}
````

### User / tool · 2026-11-02T05:22:31.726Z

**tool result**
````
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
28:ROOT = pathlib.Path(__file__).resolve().parents[1]
29:GOLD = ROOT / "evals" / "golden"
30:REPORTS = ROOT / "evals" / "reports"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:32.706Z

Now the runner edits. First the docstring and the `write_report` change.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:34.265Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)\n    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden\n    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk",
 "new_string": "    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,\n                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)\n    python -m evals.run --write-calibration\n                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).\n                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)\n    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden\n    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk"
}
````

### User / tool · 2026-11-02T05:22:34.334Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:38.363Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "def write_report(r, outdir=REPORTS):\n    outdir = pathlib.Path(outdir)\n    outdir.mkdir(parents=True, exist_ok=True)\n    ts = r[\"generated_at\"].replace(\":\", \"\").replace(\"-\", \"\")\n    (outdir / f\"{ts}.md\").write_text(render_md(r))\n    (outdir / \"latest.json\").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + \"\\n\")\n    if r.get(\"calibration\"):                      # small file the app serves (T-090); regenerated by every full run\n        (outdir / \"calibration.json\").write_text(json.dumps(r[\"calibration\"], indent=1, sort_keys=True) + \"\\n\")\n    return outdir / f\"{ts}.md\"",
 "new_string": "def write_calibration_refusal(src):\n    \"\"\"T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit\n    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source().\"\"\"\n    if src.get(\"commit\") is None or src.get(\"clean\") is None:\n        return \"no git repository or HEAD commit is available to name as the source\"\n    if not src[\"clean\"]:\n        return \"the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD\"\n    return None\n\n\ndef write_report(r, outdir=REPORTS, write_calibration=False):\n    \"\"\"latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch\n    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101).\"\"\"\n    outdir = pathlib.Path(outdir)\n    outdir.mkdir(parents=True, exist_ok=True)\n    ts = r[\"generated_at\"].replace(\":\", \"\").replace(\"-\", \"\")\n    (outdir / f\"{ts}.md\").write_text(render_md(r))\n    (outdir / \"latest.json\").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + \"\\n\")\n    if r.get(\"calibration\"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)\n        body = json.dumps(r[\"calibration\"], indent=1, sort_keys=True) + \"\\n\"\n        if write_calibration:\n            (outdir / \"calibration.json\").write_text(body)\n        else:\n            scratch = outdir / \"runs\" / ts\n            scratch.mkdir(parents=True, exist_ok=True)\n            (scratch / \"calibration.json\").write_text(body)\n    return outdir / f\"{ts}.md\""
}
````

### User / tool · 2026-11-02T05:22:38.424Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:40.685Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    ap.add_argument(\"--controls\", action=\"store_true\", help=\"run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json\")\n    a = ap.parse_args(argv)",
 "new_string": "    ap.add_argument(\"--controls\", action=\"store_true\", help=\"run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json\")\n    ap.add_argument(\"--write-calibration\", action=\"store_true\",\n                    help=\"also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)\")\n    a = ap.parse_args(argv)"
}
````

### User / tool · 2026-11-02T05:22:40.743Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:43.338Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    ts = dt.datetime.now(dt.timezone.utc).strftime(\"%Y%m%dT%H%M%SZ\")\n    if a.controls:\n        return run_controls_only(backend, out, ts)\n    real = pipeline is None\n    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / \"runs\" / ts if backend in LIVE_BACKENDS else None,\n                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)\n    path = write_report(report, out)",
 "new_string": "    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration\n        why = write_calibration_refusal(git_source())\n        if why:\n            print(f\"evals.run: --write-calibration refused, nothing was run or written: {why}.\", file=sys.stderr)\n            return 2\n    ts = dt.datetime.now(dt.timezone.utc).strftime(\"%Y%m%dT%H%M%SZ\")\n    if a.controls:\n        return run_controls_only(backend, out, ts)\n    real = pipeline is None\n    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / \"runs\" / ts if backend in LIVE_BACKENDS else None,\n                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)\n    path = write_report(report, out, write_calibration=a.write_calibration)"
}
````

### User / tool · 2026-11-02T05:22:43.396Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:57.720Z

Runner side is in place. Now the tests: update the three existing tests that assumed a plain run writes the committed file, then add the new ones.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:58.337Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    monkeypatch.setattr(R, \"write_report\", lambda r, outdir=None: tmp_path / \"x.json\")",
 "new_string": "    monkeypatch.setattr(R, \"write_report\", lambda r, outdir=None, **kw: tmp_path / \"x.json\")"
}
````

### User / tool · 2026-11-02T05:22:58.402Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:08.759Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):\n    rep = good\n    c = rep[\"calibration\"]\n    assert c[\"backend\"] == rep[\"backend\"] and c[\"cases\"] == rep[\"cases\"]\n    assert c[\"by_state\"][\"verified\"][\"total\"] == sum(rep[\"per_case\"][n][\"calibration\"][t][\"verified\"][1] for n in rep[\"per_case\"] for t in R.CAL_TYPES)\n    R.write_report(rep, tmp_path)\n    assert json.loads((tmp_path / \"calibration.json\").read_text()) == json.loads(json.dumps(c))\n    assert \"Calibrated confidence\" in next(tmp_path.glob(\"2*.md\")).read_text()",
 "new_string": "def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):\n    rep = good\n    c = rep[\"calibration\"]\n    assert c[\"backend\"] == rep[\"backend\"] and c[\"cases\"] == rep[\"cases\"]\n    assert c[\"by_state\"][\"verified\"][\"total\"] == sum(rep[\"per_case\"][n][\"calibration\"][t][\"verified\"][1] for n in rep[\"per_case\"] for t in R.CAL_TYPES)\n    R.write_report(rep, tmp_path / \"plain\")\n    assert \"Calibrated confidence\" in next((tmp_path / \"plain\").glob(\"2*.md\")).read_text()\n    assert json.loads(next((tmp_path / \"plain\" / \"runs\").glob(\"*/calibration.json\")).read_text()) == json.loads(json.dumps(c))\n    R.write_report(rep, tmp_path / \"committed\", write_calibration=True)\n    assert json.loads((tmp_path / \"committed\" / \"calibration.json\").read_text()) == json.loads(json.dumps(c))\n\n\n# ---------------------------------------------------------------- T-101: a plain run never touches the committed calibration.json\ndef _fake_report(monkeypatch, rep):\n    monkeypatch.setattr(R, \"build_report\", lambda *a, **k: copy.deepcopy(rep))\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n\n\ndef test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):\n    \"\"\"T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy.\"\"\"\n    committed = tmp_path / \"calibration.json\"\n    committed.write_text('{\"sentinel\": \"committed file, must not change\"}\\n')\n    monkeypatch.setattr(R, \"REPORTS\", tmp_path)\n    _fake_report(monkeypatch, good)\n    before = committed.read_bytes()\n    assert R.main([]) == 0\n    assert committed.read_bytes() == before\n    scratch = list((tmp_path / \"runs\").glob(\"*/calibration.json\"))\n    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good[\"calibration\"]))\n    assert list(tmp_path.glob(\"2*.md\")) and (tmp_path / \"latest.json\").exists()\n\n\ndef test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):\n    \"\"\"T-101 AC1: a plain run is independent of git state; a dirty tree neither blocks it nor changes the committed file.\"\"\"\n    monkeypatch.setattr(R, \"REPORTS\", tmp_path)\n    monkeypatch.setattr(R, \"git_source\", lambda root=None: {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40})\n    _fake_report(monkeypatch, good)\n    assert R.main([]) == 0\n    assert not (tmp_path / \"calibration.json\").exists()\n\n\n@pytest.mark.parametrize(\"src\", [\n    {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40},          # tracked edits or staged changes\n    {\"commit\": None, \"clean\": None, \"tree\": None},                    # no git at all (exported tree)\n])\ndef test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):\n    \"\"\"T-101 AC2: --write-calibration exits 2 before the pipeline runs and writes nothing.\"\"\"\n    monkeypatch.setattr(R, \"git_source\", lambda root=None: src)\n    def must_not_run(*a, **k):\n        raise AssertionError(\"the pipeline ran although --write-calibration was refused\")\n    monkeypatch.setattr(R, \"build_report\", must_not_run)\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    assert R.main([\"--write-calibration\", \"--out\", str(tmp_path)]) == 2\n    assert list(tmp_path.iterdir()) == []\n\n\ndef test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():\n    assert R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40}) is None\n    assert \"uncommitted\" in R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40})\n    assert R.write_calibration_refusal({\"commit\": None, \"clean\": None, \"tree\": None}) is not None\n\n\ndef test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):\n    \"\"\"T-101 AC2/AC3 on a real repository: allowed on a clean tracked tree (untracked files do not count), refused after a tracked edit and\n    leaves the file absent; the written header names HEAD, the clean flag, the tree and the prompt/lexicon hashes as T-090 defined them.\"\"\"\n    if shutil.which(\"git\") is None:\n        pytest.skip(\"git missing\")\n    repo = tmp_path / \"repo\"\n    repo.mkdir()\n    env = {**os.environ, \"GIT_AUTHOR_NAME\": \"t\", \"GIT_AUTHOR_EMAIL\": \"t@t\", \"GIT_COMMITTER_NAME\": \"t\", \"GIT_COMMITTER_EMAIL\": \"t@t\"}\n    subprocess.run([\"git\", \"init\", \"-q\", str(repo)], check=True)\n    (repo / \"f\").write_text(\"a\")\n    subprocess.run([\"git\", \"-C\", str(repo), \"add\", \"f\"], check=True)\n    subprocess.run([\"git\", \"-C\", str(repo), \"commit\", \"-qm\", \"x\"], check=True, env=env)\n    head = subprocess.run([\"git\", \"-C\", str(repo), \"rev-parse\", \"HEAD\"], capture_output=True, text=True, check=True).stdout.strip()\n    real = R.git_source\n    monkeypatch.setattr(R, \"git_source\", lambda root=None: real(repo))\n    def fake_report(*a, **k):\n        rep = copy.deepcopy(good)\n        rep[\"calibration\"] = R.build_calibration(rep[\"per_case\"], rep[\"backend\"], rep[\"models\"], rep[\"generated_at\"], R.git_source(), rep[\"hashes\"])\n        return rep\n    monkeypatch.setattr(R, \"build_report\", fake_report)\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    out = tmp_path / \"out\"\n    (repo / \"untracked.txt\").write_text(\"not tracked\")\n    assert R.main([\"--write-calibration\", \"--out\", str(out)]) == 0\n    c = json.loads((out / \"calibration.json\").read_text())\n    assert c[\"schema\"] == \"evals.calibration/1\" and c[\"source_commit\"] == head and c[\"source_tree_clean\"] is True\n    assert re.fullmatch(r\"[0-9a-f]{40}\", c[\"source_tree\"]) and c[\"hashes\"] == good[\"hashes\"] and c[\"backend\"] == good[\"backend\"]\n    (out / \"calibration.json\").unlink()\n    (repo / \"f\").write_text(\"edited, not committed\")\n    assert R.main([\"--write-calibration\", \"--out\", str(out)]) == 2\n    assert not (out / \"calibration.json\").exists()\n    assert not list(out.glob(\"*.md\")) and not (out / \"latest.json\").exists()"
}
````

### User / tool · 2026-11-02T05:23:08.824Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:14.244Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    (out / \"calibration.json\").unlink()\n    (repo / \"f\").write_text(\"edited, not committed\")\n    assert R.main([\"--write-calibration\", \"--out\", str(out)]) == 2\n    assert not (out / \"calibration.json\").exists()\n    assert not list(out.glob(\"*.md\")) and not (out / \"latest.json\").exists()",
 "new_string": "    (out / \"calibration.json\").unlink()\n    (repo / \"f\").write_text(\"edited, not committed\")\n    before = sorted(p.name for p in out.iterdir())\n    assert R.main([\"--write-calibration\", \"--out\", str(out)]) == 2\n    assert not (out / \"calibration.json\").exists()\n    assert sorted(p.name for p in out.iterdir()) == before          # the refused run wrote nothing new"
}
````

### User / tool · 2026-11-02T05:23:14.303Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:15.238Z

Now the regeneration test, which assumed a plain run writes `out/calibration.json`.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:16.086Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    assert (out / \"calibration.json\").exists(), r.stdout[-400:] + r.stderr[-800:]\n    fresh = json.loads((out / \"calibration.json\").read_text())",
 "new_string": "    scratch = list((out / \"runs\").glob(\"*/calibration.json\"))         # T-101: a plain run writes only this scratch copy\n    assert len(scratch) == 1 and not (out / \"calibration.json\").exists(), r.stdout[-400:] + r.stderr[-800:]\n    fresh = json.loads(scratch[0].read_text())"
}
````

### User / tool · 2026-11-02T05:23:16.143Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:17.890Z

**tool call — Bash**
````
{
 "command": "git show HEAD:evals/reports/calibration.json > evals/reports/calibration.json && git status --porcelain -- evals/reports/calibration.json; echo \"restored rc=$?\"; .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -30",
 "description": "Restore calibration.json from HEAD and run calibration and eval runner tests",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:23:26.344Z

**tool result**
````
restored rc=0
        c = _committed()
        _require_source_commit(c)
        src = tmp_path / "src"
        src.mkdir()
        tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
        env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
        env["PYTHONPATH"] = str(src)
        out = tmp_path / "out"
        r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
        scratch = list((out / "runs").glob("*/calibration.json"))         # T-101: a plain run writes only this scratch copy
>       assert len(scratch) == 1 and not (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
E       AssertionError: ship_bar_met=False backend=fixture report=/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-3300/test_committed_calibration_reg0/out/20261102T052325Z.md
E           blocker: 4_no_invented_facts
E           blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
E           blocker: judge_controls (J3/J4 seeded wrong items): not measured
E         c461447d92e36 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
E         llm call failed call_id=c32f1f259cbb8 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
E         llm call failed call_id=c61546397bfd7 step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
E         llm call failed call_id=c3bd288c2bbc4 step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
E         llm call failed call_id=cc0e37f377a12 step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
E         llm call failed call_id=c670bb15b2d5c step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
E         
E       assert (0 == 1)
E        +  where 0 = len([])

tests/unit/test_eval_runner.py:774: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
1 failed, 121 passed, 1750 deselected in 7.99s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:35.761Z

The regeneration test replays the code at the cited commit (`git archive` of `source_commit`), and that commit predates `--write-calibration`, so it still writes `out/calibration.json`. The test should accept either location. I'll also add a real CLI check for the no-git refusal.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:36.971Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    scratch = list((out / \"runs\").glob(\"*/calibration.json\"))         # T-101: a plain run writes only this scratch copy\n    assert len(scratch) == 1 and not (out / \"calibration.json\").exists(), r.stdout[-400:] + r.stderr[-800:]\n    fresh = json.loads(scratch[0].read_text())",
 "new_string": "    # The cited commit's own code decides where the file lands: commits before T-101 write out/calibration.json, later ones only a\n    # scratch copy under out/runs/<ts>/ (T-101). Exactly one must exist either way.\n    found = [p for p in [out / \"calibration.json\", *sorted((out / \"runs\").glob(\"*/calibration.json\"))] if p.exists()]\n    assert len(found) == 1, r.stdout[-400:] + r.stderr[-800:]\n    fresh = json.loads(found[0].read_text())"
}
````

### User / tool · 2026-11-02T05:23:37.034Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:39.563Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "def test_git_source_reports_commit_and_dirtiness(tmp_path):",
 "new_string": "def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):\n    \"\"\"T-101 AC2 end to end: an export of HEAD with no .git exits 2 before any run and writes nothing.\"\"\"\n    if shutil.which(\"git\") is None:\n        pytest.skip(\"git missing\")\n    src = tmp_path / \"src\"\n    src.mkdir()\n    tar = subprocess.run([\"git\", \"archive\", \"HEAD\"], cwd=R.ROOT, capture_output=True, check=True).stdout\n    subprocess.run([\"tar\", \"-x\", \"-C\", str(src)], input=tar, check=True)\n    env = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    env[\"PYTHONPATH\"] = str(src)\n    out = tmp_path / \"out\"\n    r = subprocess.run([sys.executable, \"-m\", \"evals.run\", \"--write-calibration\", \"--out\", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)\n    assert r.returncode == 2 and \"--write-calibration refused\" in r.stderr, r.stderr[-800:]\n    assert not out.exists() or not any(out.iterdir())\n\n\ndef test_git_source_reports_commit_and_dirtiness(tmp_path):"
}
````

### User / tool · 2026-11-02T05:23:39.628Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:41.246Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -15; echo ----; git status --porcelain -- evals/reports/calibration.json evals/run.py tests/unit/test_eval_runner.py; echo ----; cmp <(git show HEAD:evals/reports/calibration.json) evals/reports/calibration.json && echo calibration-identical-to-HEAD",
 "description": "Run target tests and confirm calibration.json unchanged from HEAD",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:23:50.223Z

**tool result**
````
        r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
>       assert r.returncode == 2 and "--write-calibration refused" in r.stderr, r.stderr[-800:]
E       AssertionError: usage: python -m evals.run [-h] [--check-fresh] [--check-spec]
E                                    [--backend BACKEND] [--runs RUNS] [--out OUT]
E                                    [--controls]
E         python -m evals.run: error: unrecognized arguments: --write-calibration
E         
E       assert (2 == 2 and '--write-calibration refused' in 'usage: python -m evals.run [-h] [--check-fresh] [--check-spec]\n                           [--backend BACKEND] [--run...T]\n                           [--controls]\npython -m evals.run: error: unrecognized arguments: --write-calibration\n')
E        +  where 2 = CompletedProcess(args=['/Users/arsis/zlayt-pm-project/.venv/bin/python', '-m', 'evals.run', '--write-calibration', '--...]\n                           [--controls]\npython -m evals.run: error: unrecognized arguments: --write-calibration\n').returncode
E        +  and   'usage: python -m evals.run [-h] [--check-fresh] [--check-spec]\n                           [--backend BACKEND] [--run...T]\n                           [--controls]\npython -m evals.run: error: unrecognized arguments: --write-calibration\n' = CompletedProcess(args=['/Users/arsis/zlayt-pm-project/.venv/bin/python', '-m', 'evals.run', '--write-calibration', '--...]\n                           [--controls]\npython -m evals.run: error: unrecognized arguments: --write-calibration\n').stderr

tests/unit/test_eval_runner.py:796: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git
1 failed, 122 passed, 1750 deselected in 8.53s
----
 M evals/run.py
 M tests/unit/test_eval_runner.py
----
calibration-identical-to-HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:52.436Z

The export test ran HEAD's old `run.py`, which predates the flag. It should run the working-tree runner, so I'll overlay that file on the export.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:54.020Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    tar = subprocess.run([\"git\", \"archive\", \"HEAD\"], cwd=R.ROOT, capture_output=True, check=True).stdout\n    subprocess.run([\"tar\", \"-x\", \"-C\", str(src)], input=tar, check=True)\n    env = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    env[\"PYTHONPATH\"] = str(src)\n    out = tmp_path / \"out\"\n    r = subprocess.run([sys.executable, \"-m\", \"evals.run\", \"--write-calibration\"",
 "new_string": "    tar = subprocess.run([\"git\", \"archive\", \"HEAD\"], cwd=R.ROOT, capture_output=True, check=True).stdout\n    subprocess.run([\"tar\", \"-x\", \"-C\", str(src)], input=tar, check=True)\n    shutil.copy(R.ROOT / \"evals\" / \"run.py\", src / \"evals\" / \"run.py\")      # the working-tree runner (T-101 is not committed yet)\n    env = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    env[\"PYTHONPATH\"] = str(src)\n    out = tmp_path / \"out\"\n    r = subprocess.run([sys.executable, \"-m\", \"evals.run\", \"--write-calibration\""
}
````

### User / tool · 2026-11-02T05:23:54.080Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:55.615Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -8; echo ----; git status --porcelain -- evals/reports/calibration.json evals/run.py tests/unit/test_eval_runner.py; cmp <(git show HEAD:evals/reports/calibration.json) evals/reports/calibration.json && echo calibration-identical-to-HEAD",
 "description": "Rerun target tests and confirm calibration.json still matches HEAD",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:24:04.372Z

**tool result**
````
........................................................................ [ 58%]
...................................................                      [100%]
123 passed, 1767 deselected in 8.29s
----
 M evals/run.py
 M tests/unit/test_eval_runner.py
calibration-identical-to-HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:08.321Z

All 123 pass and the committed `calibration.json` is back to HEAD bytes. Next, an end-to-end check with the real CLI: a plain run into a scratch dir, and `--write-calibration` on this dirty tree, which should refuse.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:10.564Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101 && mkdir -p \"$S\" && env -u LLM_BACKEND -u ENABLE_LIVE .venv/bin/python -m evals.run --out \"$S/plain\" > \"$S/plain.log\" 2>&1; echo \"plain rc=$?\"; tail -3 \"$S/plain.log\"; ls \"$S/plain/runs\" 2>/dev/null; env -u LLM_BACKEND -u ENABLE_LIVE .venv/bin/python -m evals.run --write-calibration --out \"$S/refused\" ; echo \"write rc=$?\"; ls \"$S/refused\" 2>&1; cmp <(git show HEAD:evals/reports/calibration.json) evals/reports/calibration.json && echo calibration-identical-to-HEAD",
 "description": "Run plain and refused CLI evals into scratch dir and check calibration",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:24:11.904Z

**tool result**
````
plain rc=1
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
20261102T052411Z
evals.run: --write-calibration refused, nothing was run or written: the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD.
write rc=2
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/refused: No such file or directory
calibration-identical-to-HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:16.619Z

Plain run wrote the scratch copy and the repo calibration is unchanged. The refusal fired with exit 2 and nothing written. Before committing, a quick look at the diff of the two code paths.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:17.036Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- evals/run.py tests/unit/test_eval_runner.py && git diff -- evals/run.py | head -150",
 "description": "Review the runner diff before committing"
}
````

### User / tool · 2026-11-02T05:24:17.289Z

**tool result**
````
 evals/run.py                   |  39 +++++++++++--
 tests/unit/test_eval_runner.py | 125 +++++++++++++++++++++++++++++++++++++++--
 2 files changed, 153 insertions(+), 11 deletions(-)
diff --git a/evals/run.py b/evals/run.py
index 47b0807..dd32cc1 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -1,7 +1,11 @@
 """Eval runner: `python -m evals.run` scores the product against the golden set and writes
 evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
 
-    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
+    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
+                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
+    python -m evals.run --write-calibration
+                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
+                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
     python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
     python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
 
@@ -999,14 +1003,32 @@ def render_md(r):
     return "\n".join(L) + "\n"
 
 
-def write_report(r, outdir=REPORTS):
+def write_calibration_refusal(src):
+    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit
+    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source()."""
+    if src.get("commit") is None or src.get("clean") is None:
+        return "no git repository or HEAD commit is available to name as the source"
+    if not src["clean"]:
+        return "the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD"
+    return None
+
+
+def write_report(r, outdir=REPORTS, write_calibration=False):
+    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
+    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101)."""
     outdir = pathlib.Path(outdir)
     outdir.mkdir(parents=True, exist_ok=True)
     ts = r["generated_at"].replace(":", "").replace("-", "")
     (outdir / f"{ts}.md").write_text(render_md(r))
     (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
-    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
-        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
+    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
+        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
+        if write_calibration:
+            (outdir / "calibration.json").write_text(body)
+        else:
+            scratch = outdir / "runs" / ts
+            scratch.mkdir(parents=True, exist_ok=True)
+            (scratch / "calibration.json").write_text(body)
     return outdir / f"{ts}.md"
 
 
@@ -1099,6 +1121,8 @@ def main(argv=None, pipeline=None):
     ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
     ap.add_argument("--out", default=str(REPORTS))
     ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
+    ap.add_argument("--write-calibration", action="store_true",
+                    help="also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)")
     a = ap.parse_args(argv)
     out = pathlib.Path(a.out)
     if a.check_fresh:
@@ -1132,13 +1156,18 @@ def main(argv=None, pipeline=None):
         print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
               f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
         return 2
+    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
+        why = write_calibration_refusal(git_source())
+        if why:
+            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
+            return 2
     ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
     if a.controls:
         return run_controls_only(backend, out, ts)
     real = pipeline is None
     report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                           judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
-    path = write_report(report, out)
+    path = write_report(report, out, write_calibration=a.write_calibration)
     print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
     for b in report["blockers"]:
         print("  blocker:", b)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:22.989Z

The pre-run check is correct, but `git_source()` is recomputed after a multi-minute run. If a worker dirties a tracked file mid-run, the header would still be written as clean-looking. The header itself should be re-checked before the write, so I'll add that guard.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:24.235Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    path = write_report(report, out, write_calibration=a.write_calibration)\n    print(f\"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}\")",
 "new_string": "    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)\n        cal = report.get(\"calibration\") or {}\n        why = write_calibration_refusal({\"commit\": cal.get(\"source_commit\"), \"clean\": cal.get(\"source_tree_clean\")})\n        if why:\n            print(f\"evals.run: --write-calibration refused after the run, nothing was written: {why}.\", file=sys.stderr)\n            return 2\n    path = write_report(report, out, write_calibration=a.write_calibration)\n    print(f\"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}\")"
}
````

### User / tool · 2026-11-02T05:24:24.291Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:27.143Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "@pytest.mark.parametrize(\"src\", [\n    {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40},          # tracked edits or staged changes",
 "new_string": "def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):\n    \"\"\"T-101: a tree dirtied during a long run must not produce a committed header that claims clean; nothing is written.\"\"\"\n    monkeypatch.setattr(R, \"git_source\", lambda root=None: {\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40})   # clean at the start\n    def dirtied_during_run(*a, **k):\n        rep = copy.deepcopy(good)\n        rep[\"calibration\"] = R.build_calibration(rep[\"per_case\"], rep[\"backend\"], rep[\"models\"], rep[\"generated_at\"],\n                                                 {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40}, rep[\"hashes\"])\n        return rep\n    monkeypatch.setattr(R, \"build_report\", dirtied_during_run)\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    assert R.main([\"--write-calibration\", \"--out\", str(tmp_path)]) == 2\n    assert not (tmp_path / \"calibration.json\").exists() and not (tmp_path / \"latest.json\").exists()\n\n\n@pytest.mark.parametrize(\"src\", [\n    {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40},          # tracked edits or staged changes"
}
````

### User / tool · 2026-11-02T05:24:27.202Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:28.833Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -4; echo ----; git status --porcelain -- evals/reports/calibration.json; cmp <(git show HEAD:evals/reports/calibration.json) evals/reports/calibration.json && echo calibration-identical-to-HEAD; git status --porcelain --untracked-files=no -- evals/run.py tests/unit/test_eval_runner.py",
 "description": "Rerun target tests after post-run guard and confirm state",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:24:37.665Z

**tool result**
````
........................................................................ [ 58%]
....................................................                     [100%]
124 passed, 1769 deselected in 8.34s
----
calibration-identical-to-HEAD
 M evals/run.py
 M tests/unit/test_eval_runner.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:39.226Z

Tests pass (124) and the committed file is untouched. Staging only my two paths now.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:39.680Z

**tool call — Bash**
````
{
 "command": "git add evals/run.py tests/unit/test_eval_runner.py",
 "description": "Stage the runner and its test file explicitly"
}
````

### User / tool · 2026-11-02T05:24:39.777Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:40.014Z

**tool call — Bash**
````
{
 "command": "git diff --cached --stat",
 "description": "Show staged diff stat for the two paths"
}
````

### User / tool · 2026-11-02T05:24:40.110Z

**tool result**
````
 app/backend/api.py                |   2 -
 app/backend/billing.py            | 332 +++++-----------------------
 app/backend/grounding.py          |  28 ---
 evals/run.py                      |  45 +++-
 memory/contracts/api.md           |   4 +-
 tests/unit/_pdf_probe.py          |  66 ------
 tests/unit/test_billing.py        | 448 --------------------------------------
 tests/unit/test_eval_runner.py    | 141 +++++++++++-
 tests/unit/test_pdf_hidden_r2.py  | 235 --------------------
 tests/unit/test_pdf_ocr_limits.py | 114 ----------
 10 files changed, 225 insertions(+), 1190 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:41.987Z

The index already holds other agents' staged changes (billing, grounding, and others). `git commit -- <paths>` commits only the named paths and leaves those staged changes alone, which is what the instruction calls for. Committing now.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:43.325Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)\" -m \"A plain run now writes a scratch copy under evals/reports/runs/<ts>/calibration.json and never touches the committed file the app serves. --write-calibration writes evals/reports/calibration.json with the T-090 provenance header (source_commit, source_tree_clean, source_tree, hashes, backend), and is refused before any run unless the tracked tree is clean at HEAD; the header is re-checked after the run. Tests cover both behaviours, the real-git cleanliness rule, the no-git export, and the regeneration test (accepts the cited commit's own output location).\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/run.py tests/unit/test_eval_runner.py",
 "description": "Commit only the runner and its test file"
}
````

### User / tool · 2026-11-02T05:24:43.809Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 4c5f9bf] fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
 2 files changed, 175 insertions(+), 11 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:45.154Z

**tool call — Bash**
````
{
 "command": "git show --stat HEAD | head -12; .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3",
 "description": "Verify the commit contents and rerun the target tests",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:24:53.848Z

**tool result**
````
commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:24:43 2026 -0600

    fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
    
    A plain run now writes a scratch copy under evals/reports/runs/<ts>/calibration.json and never touches the committed file the app serves. --write-calibration writes evals/reports/calibration.json with the T-090 provenance header (source_commit, source_tree_clean, source_tree, hashes, backend), and is refused before any run unless the tracked tree is clean at HEAD; the header is re-checked after the run. Tests cover both behaviours, the real-git cleanliness rule, the no-git export, and the regeneration test (accepts the cited commit's own output location).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/run.py                   |  45 +++++++++++--
 tests/unit/test_eval_runner.py | 141 +++++++++++++++++++++++++++++++++++++++--
........................................................................ [ 58%]
....................................................                     [100%]
124 passed, 1801 deselected in 8.30s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:56.248Z

Commit `4c5f9bf` holds only the two paths, and the target tests pass on it. Now the board: AC evidence, commit record, handoff, and move to review.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:59.631Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-101 --check 1 --agent qa --evidence \"tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed\" && $B commit T-101 --sha 4c5f9bf --agent qa && $B handoff T-101 --agent qa --text \"What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json with the T-090 header (source_commit, source_tree_clean, source_tree, hashes, backend), refused (exit 2, nothing run) unless the tracked tree is clean at HEAD, re-checked after the run. Tests: tests/unit/test_eval_runner.py (+6 new, 4 updated for the new location). How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed, 0 skipped; committed calibration.json is byte-identical to HEAD (restored and still identical after the run); real CLI plain run to a scratch --out rc=1 (fixture ship bar, expected) with calibration untouched; --write-calibration on this dirty tree rc=2, nothing written. Left: latest.json and the .md are still written by every run as before (not in scope). Other agents' uncommitted changes in the shared tree were left alone; the commit used --only paths. Surprise: the regeneration test replays the cited commit's own code, so it accepts the old out/calibration.json location as well as the new runs/ scratch copy. Note for orchestrator: --write-calibration does not restrict backend; the committed-header test pins backend=fixture, so a live write would fail that test by design.\" && $B move T-101 in_review --agent qa && $B show T-101 | head -30",
 "description": "Record AC evidence, commit, handoff, and move T-101 to review"
}
````

### User / tool · 2026-11-02T05:25:00.072Z

**tool result**
````
AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed
T-101: commit 4c5f9bf recorded
handoff written on T-101
T-101: in_progress -> in_review
---
id: "T-101"
title: "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:21:08Z"
updated_at: "2026-11-02T05:25:00Z"
claimed_by: "qa"
claimed_at: "2026-11-02T05:21:14Z"
rounds: 0
commits: ["4c5f9bf"]
reviews: []
ac:
  - {"n": 1, "text": "Plain 'python -m evals.run' leaves evals/reports/calibration.json untouched; --write-calibration refuses on a dirty tree; test", "done": true, "evidence": "tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:21:14Z qa: claimed
- 2026-11-02T05:24:59Z qa: AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed
- 2026-11-02T05:25:00Z qa: moved in_progress -> in_review

## Handoff
What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json with the T-090 header (source_commit, source_tree_clean, source_tree, hashes, backend), refused (exit 2, nothing run) unless the tracked tree is clean at HEAD, re-checked after the run. Tests: tests/unit/test_eval_runner.py (+6 new, 4 updated for the new location). How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed, 0 skipped; committed calibration.json is byte-identical to HEAD (restored and still identical after the run); real CLI plain run to a scratch --out rc=1 (fixture ship bar, expected) with calibration untouched; --write-calibration on this dirty tree rc=2, nothing written. Left: latest.json and the .md are still written by every run as before (not in scope). Other agents' uncommitted changes in the shared tree were left alone; the commit used --only paths. Surprise: the regeneration test replays the cited commit's own code, so it accepts the old out/calibration.json location as well as the new runs/ scratch copy. Note for orchestrator: --write-calibration does not restrict backend; the committed-header test pins backend=fixture, so a live write would fail that test by design.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:02.727Z

**tool call — mcp__ccd_turn__wrap_up**
````
{
 "recap": "T-101 is in_review at commit 4c5f9bf. A plain evals.run no longer touches the committed calibration.json (it writes a scratch copy under evals/reports/runs/), and --write-calibration writes it only from a clean tracked tree, re-checked after the run. The committed file is restored to HEAD bytes, and 124 calibration/eval_runner tests pass. Not done: the card is not marked done, and the review is pending."
}
````

### User / tool · 2026-11-02T05:25:02.738Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__wrap_up hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:03.778Z

T-101 is in_review at commit 4c5f9bf: plain `evals.run` leaves the committed calibration.json untouched, `--write-calibration` writes it only from a clean tracked tree, and 124 calibration/eval_runner tests pass.
