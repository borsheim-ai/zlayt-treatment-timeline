# Subagent: QA: confirming live 3-run for M2 (QA: confirming live 3-run for M2)

Source: `agent-a2e8c7c1ebec8843a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T16:13:02.302Z

You are the QA worker in /Users/arsis/zlayt-pm-project. You are producing the confirming live evidence for the M2 re-gate; the QA finding in reviews/GATE-M2-round1-triage.md asks for it.

1. Make a clean worktree of the current HEAD (ea988f8 or later) in your scratchpad. Record the commit id.
2. Run ONE live 3-run there: `LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --runs 3`, with the controls gate included. Never export ANTHROPIC_API_KEY, and never print .env.
3. In the same worktree, regenerate calibration live with `--write-calibration`. The live re-measure has been owed since T-105 and T-133.
4. Check the report: it names the commit with a clean tree, and the ship_bar_met value. evals/letter_check.py must report 0 violations.
5. Copy the report, the per-run directory and calibration.json into the shared evals/reports/. Commit with a pathspec, leaving latest.json out.
6. If the ship bar isn't met, name the blocker and the items, and stop. Do not fix product code.

Reply in 4 lines with the report path and ship_bar_met.

### User / tool · 2026-11-02T16:13:02.308Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:05.035Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -5 && git status --short | head -20 && cat .claude/agent-memory/qa/project_calibration_route.md && sed -n 1,200p reviews/GATE-M2-round1-triage.md | grep -n -i -B2 -A8 \"qa\" | head -80"
}
````

### User / tool · 2026-11-02T16:13:05.175Z

**tool result**
````
ea988f8 fix(backend): T-139 r5 the export gate scans Billed charges (a charge line carries its own amount; other money trimmed by code or blocks naming the line); number words after a money label are money
9db2cec fix(frontend): a side panel that throws is reported, not swallowed; the no-console-errors smoke asserts all 7 panels mount (T-162 r3)
95ffe36 docs(orchestrator): D-063 P0 + UX/UI only until the MVP is polished (Chris)
f31b146 fix(backend): T-157 r3 an unconfirmed edit is pinned as a next_action item (mutant dies), exact waiting-set and demo-gate tests, plain_title keeps words after a lone <, hitl.needs_review_open
a7302fe fix(backend): T-139 r4 the trace export gate lists MONEY_IN_LETTER (export.money_blockers_for_case, both styles), so gate.ready equals export allowed (D-044/D-045); test with a stored money summary
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
---
name: calibration-route-and-regen
description: How GET /api/calibration decides stale, how calibration.json is regenerated from a clean worktree, and the fixture-dir pitfall in score_unsplit
metadata:
  type: project
---

GET /api/calibration lives in app/backend/calibration_route.py (T-099, stale flag T-102). It serves evals/reports/calibration.json read-only.
`calibration.stale` / `stale_reason` compare the file's recorded `hashes` (prompts + lexicon, sha256) with the same files at HEAD
(`git cat-file blob HEAD:path`, cached per HEAD sha); a checkout-less copy falls back to disk. Hashes are never served.

**Why:** the served numbers must say when they describe older prompts (T-096 shows "numbers from an older version").
**How to apply:** when prompts change, regenerate before the gate. Do it in a clean worktree, not the shared tree:
`git worktree add <scratchpad>/<unique-name> HEAD`, then `.venv/bin/python -m evals.run --write-calibration --backend fixture` from
inside it (the committed file is refused from a dirty tree), copy the file back (`cmp` it), commit it, then `git worktree remove --force`.
Pick a unique worktree name: a `wt` folder already existed in the scratchpad (an old copy of the project with a .env) and was not touched.

Pitfalls:
- evals/run.py `score_unsplit` sets LLM_FIXTURE_DIR to tests/fixtures/llm/split for the unsplit case, and fixture.call does not fall back
  to the default dir when LLM_FIXTURE_DIR is set. The other LLM calls in that case miss (FIXTURE_MISS), judge_unavailable_count > 0, and
  the report shows blocker 4_no_invented_facts. Golden-case calibration counts are unaffected. Open follow-up for qa.
- The count changes between regenerations come from code as well as prompts (T-110 and others), so 83/84 became 84/85 at HEAD.
- git-guard rejects `git add ... && git commit ...` in one Bash call: stage in one call, commit in the next.
- `timeout` is not installed on this Mac; use the Bash tool's timeout parameter.
- The git-guard hook and `git commit -- <paths>` only commit the listed paths; the shared index often holds other workers' staged deletions.
1-# GATE-M2 round 1 — triage (orchestrator)
2-
3:Pinned commit 0c24f5f. Panel: staff-engineer, qa, paralegal, legal-nurse, claims-adjuster (Opus), privacy-compliance.
4-Result: **fail** (3 blockers). Every finding at major or above is mapped to a card; the gate re-runs on the fix commit.
5-
6-| Severity | Source | Finding | Card |
7-|---|---|---|---|
8-| blocker | claims-adjuster | Per-visit rates reach the carrier letter through entry summaries/quotes (lib01 $140, lib03 $120) | T-139 |
9-| blocker | paralegal | Ledger total and balance-due lines classed as charges; lib11 letter total $10,906 vs $6,000 | T-140 |
10-| major | claims-adjuster | Dismissed ED charge still quoted in the letter and listed under "Bills to request" | T-139 |
11-| major | paralegal | lib11 intake "Prior accidents: No" vs PCP 2019/2022 accidents not flagged; false accident-date conflict shown | T-141 |
12-| major | legal-nurse | "No conflicts found" overclaims; laterality and LOC contradictions not checked | T-142 (+ T-141 API field) |
13-| major | legal-nurse | Entries drop clinical sentences silently | T-143 (backend) + T-144 (UI) |
14:| major | qa | Live ship-bar evidence is at 63e18ed; a confirming live 3-run is needed at the tag commit; calibration only fixture-regenerated | orchestrator: confirming live 3-run + live calibration after fixes land |
15-| blocker | staff-engineer | Deadline-hit run skips judge 1 but entries stay 'verified' and Why says the check agreed; batch accept takes them | T-145 |
16-| major | staff-engineer | Timed-out re-run deletes previous pending items while the error says they were kept | T-146 |
17:| major | staff-engineer | No passing ship-bar report at HEAD (--check-fresh exits 1) | same as qa: confirming live 3-run |
18-| minor | paralegal | "Bills to request" names the plaintiff's law firm | T-139 note |
19-| minor | privacy | Paste box lacks synthetic warning; injection scan misses "disregard the above" phrasings; JSON export carries provenance ids | to backlog after re-gate |
20-| question | privacy | Should the letter itself carry an AI marker? | already decided by D-009 (AI statement in UI banner + internal notes, not the letter; listed in NEEDS_CHRIS assumptions) |
21-
22-In-flight carry-overs that also land before re-gate: T-132, T-133, T-134, T-136, T-138.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:07.399Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && ls evals/ evals/reports | head -50 && grep -n \"argparse\\|add_argument\" evals/run.py | head -40 && ls tools/ | head -30; ls -la .env 2>/dev/null | cut -c1-40; ls ~/.claude 2>/dev/null | head -3"
}
````

### User / tool · 2026-11-02T16:13:07.518Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:08.948Z

**tool call — Bash**
````
{
 "command": "sed -n 1200,1330p evals/run.py; ls evals/reports | grep -v '\\.md$' | tail -20; cat evals/reports/latest.json | head -c 600; grep -n \"ENABLE_LIVE\\|controls\" evals/run.py | head -40"
}
````

### User / tool · 2026-11-02T16:13:09.059Z

**tool result**
````
    return name if name in KNOWN_BACKENDS else None


def run_controls_only(backend, out, ts):
    """Live J3/J4 controls alone (no pipeline): per-item verdicts on every repeat, written next to the other reports."""
    jc = judge_controls_metrics(load_controls(), default_judge_control(backend), repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1,
                                workers=4 if backend in LIVE_BACKENDS else 1)
    ok = controls_ok(jc)
    src = git_source()
    out.mkdir(parents=True, exist_ok=True)
    md = [f"# Judge controls {ts}", "", f"**controls_ok: {ok}**  backend `{backend}`  prompts `{control_prompt('j3')}`, `{control_prompt('j4')}` (hashes in the json)",
          f"Source commit `{src['commit'] or 'unknown'}`, tree {'clean' if src['clean'] else 'DIRTY, not reproducible from the commit' if src['clean'] is False else 'unknown'}.",
          "", "| Metric | Value | Bar | R-IDs |", "|---|---|---|---|", *render_controls(jc), *render_control_items(jc)]
    (out / f"controls-{ts}.md").write_text("\n".join(md) + "\n")
    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
                                                         "source_commit": src["commit"], "source_tree_clean": src["clean"], "source_tree": src["tree"], "hashes": hashes(), "judge_controls": jc}, indent=1, sort_keys=True) + "\n")
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
    ap.add_argument("--write-calibration", action="store_true",
                    help="also write the committed calibration.json (out/calibration.json); refused unless the tree is clean at HEAD, tracked and untracked inputs alike (T-101)")
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
    if a.write_calibration and a.controls:           # T-101 r2: controls mode writes no calibration, so the combination is refused, not silently ignored
        print("evals.run: --write-calibration cannot be combined with --controls (controls mode writes no calibration); nothing was run or written.",
              file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
        if why:
            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
            return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    from evals import letter_check
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None,
                          letters=letter_check.measure if real else None)
    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
        cal = report.get("calibration") or {}
        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"),
                                         "dirty": (git_source().get("dirty") or []) if cal.get("source_tree_clean") is False else []})
        if why:
            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
            return 2
    try:
        path = write_report(report, out, write_calibration=a.write_calibration, scratch_ts=ts)   # one run directory: runs/<ts> (T-101 r2)
    except CalibrationRefused as e:                  # backstop: write_report judges the header too
        print(f"evals.run: --write-calibration refused, nothing was written: {e}.", file=sys.stderr)
        return 2
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)


if __name__ == "__main__":
    sys.exit(main())
calibration.json
controls-20261102T042306Z.json
controls-20261102T043911Z.json
controls-20261102T044933Z.json
controls-20261102T045207Z.json
controls-20261102T063331Z.json
controls-20261102T075238Z.json
controls-20261102T090925Z.json
controls-20261102T102626Z.json
controls-20261102T123937Z.json
latest.json
runs
{
 "assertions": {
  "all_gap_rows_correct": true,
  "gap_28_not_flagged": true,
  "gap_73_flagged": true
 },
 "backend": "fixture",
 "backend_requested": "fixture",
 "bars": {
  "1_grounding": true,
  "2_recall": true,
  "3_flags": true,
  "4_no_invented_facts": false
 },
 "blockers": [
  "4_no_invented_facts",
  "backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)",
  "judge_controls (J3/J4 seeded wrong items): not measured"
 ],
 "calibration": {
  "backend": "fixture",
  "by_state": {
   "needs_review": {
    "cases": [
     "case_01_date_formats",
    548:def hallucination_metrics(items, controls, judge, check_summary=None):
552:    crows = [judge_item(c, judge, check_summary) for c in controls]
558:            "controls_total": len(controls), "controls_unsupported": [r["id"] for r in crows if r["verdict"] == "unsupported"],
559:            "controls_flagged_by_code": [r["id"] for r in crows if r["code_reasons"]],
560:            "controls_partially": [r["id"] for r in crows if r["verdict"] == "partially"]}
567:# ---------------------------------------------------------------- J3 / J4 seeded controls (rung 2 for flags; T-093, D-046)
569:CONTROL_FILES = (("judge_controls.jsonl", "in_sample"), ("judge_controls_heldout.jsonl", "held_out"))
579:def load_controls(gold=None):
580:    """In-sample controls (they share authors and rules with the prompts they test) and the held-out file (separately authored; its status is derived by evals/heldout_audit.py)."""
589:def judge_controls_metrics(items, judge_control, repeats=1, workers=1):
595:    Metrics are also split into in_sample and held_out controls (T-093 r2, F6)."""
898:def controls_ok(jc):
921:                               and ge(m["hallucination_catch_rate"]["value"], th["hallucination_catch_rate"]) and not m["hallucination_catch_rate"]["controls_unsupported"]
925:                               and controls_ok(m.get("judge_controls")),
941:    jc = m.get("judge_controls")
942:    if not controls_ok(jc):
943:        blockers.append("judge_controls (J3/J4 seeded wrong items): " + ("not measured" if not jc or jc.get("status") != "measured" else
963:    items, controls = load_jsonl(GOLD / "hallucinations.jsonl"), load_jsonl(GOLD / "hallucinations_controls.jsonl")
968:    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
982:        m["judge_controls"] = {"status": "not_measured", "value": None, "reason": "no judge_control supplied", "r_ids": ["R-CO-2", "R-CO-3"]}
984:        m["judge_controls"] = judge_controls_metrics(load_controls(), judge_control, repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1)
1009:def render_controls(jc):
1011:        return ["| judge_controls (J3/J4 seeded) | not_measured | catch every wrong item on every repeat, 0 false agree | R-CO-2 |"]
1023:    """Per-item verdict on every repeat. in-sample controls share authors and rules with the prompts (not independent evidence); a held-out row is separately authored
1027:    L = ["", "## Judge controls, per item", "", "In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says "
1029:         "from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).", "", "| id | judge | split | kind | pair | origin | expected | verdict per run | ok |", "|---|---|---|---|---|---|---|---|---|"]
1069:          f"| controls judged unsupported | {len(h['controls_unsupported'])} of {h['controls_total']} | 0 | R-TL-4 |",
1072:          *render_controls(m.get("judge_controls")),
1080:    L += render_control_items(m.get("judge_controls"))
1203:def run_controls_only(backend, out, ts):
1204:    """Live J3/J4 controls alone (no pipeline): per-item verdicts on every repeat, written next to the other reports."""
1205:    jc = judge_controls_metrics(load_controls(), default_judge_control(backend), repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1,
1207:    ok = controls_ok(jc)
1210:    md = [f"# Judge controls {ts}", "", f"**controls_ok: {ok}**  backend `{backend}`  prompts `{control_prompt('j3')}`, `{control_prompt('j4')}` (hashes in the json)",
1212:          "", "| Metric | Value | Bar | R-IDs |", "|---|---|---|---|", *render_controls(jc), *render_control_items(jc)]
1213:    (out / f"controls-{ts}.md").write_text("\n".join(md) + "\n")
1214:    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
1215:                                                         "source_commit": src["commit"], "source_tree_clean": src["clean"], "source_tree": src["tree"], "hashes": hashes(), "judge_controls": jc}, indent=1, sort_keys=True) + "\n")
1216:    print(f"controls_ok={ok} backend={backend} report={out / f'controls-{ts}.md'}")
1227:    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:13.037Z

**tool call — Bash**
````
{
 "command": "grep -n \"def write_report\" -A45 evals/run.py | head -90; git check-ignore .env venv .venv; ls .venv/bin/python; ls -d /private/tmp/claude-501/*/6ddf*/scratchpad 2>/dev/null; which claude"
}
````

### User / tool · 2026-11-02T16:13:13.226Z

**tool result**
````
1111:def write_report(r, outdir=REPORTS, write_calibration=False, scratch_ts=None):
1112-    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
1113-    copy under outdir/runs/<scratch_ts or ts>/ so a plain run never touches the file the app serves (T-101).
1114-    write_calibration is judged here as well as in main(), so every caller that reaches the committed file meets the same clean-HEAD rule (T-101 r2)."""
1115-    if write_calibration:                         # checked before anything is written: a refused call leaves the directory as it was
1116-        cal = r.get("calibration") or {}
1117-        why = "the report has no calibration" if not cal else write_calibration_refusal(
1118-            {"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"), "dirty": []})
1119-        if why:
1120-            raise CalibrationRefused(why)
1121-    outdir = pathlib.Path(outdir)
1122-    outdir.mkdir(parents=True, exist_ok=True)
1123-    ts = r["generated_at"].replace(":", "").replace("-", "")
1124-    (outdir / f"{ts}.md").write_text(render_md(r))
1125-    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
1126-    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
1127-        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
1128-        if write_calibration:
1129-            (outdir / "calibration.json").write_text(body)
1130-        else:
1131-            scratch = outdir / "runs" / (scratch_ts or ts)
1132-            scratch.mkdir(parents=True, exist_ok=True)
1133-            (scratch / "calibration.json").write_text(body)
1134-    return outdir / f"{ts}.md"
1135-
1136-
1137-def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1138-    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
1139-    p = pathlib.Path(latest_path)
1140-    if not p.exists():
1141-        print("check-fresh: no latest.json", file=sys.stderr)
1142-        return 1
1143-    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
1144-    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
1145-    for k in diff:
1146-        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
1147-    bad = check_calibration(p.parent / "calibration.json", root)
1148-    for m in bad:
1149-        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
1150-    return 1 if diff or bad else 0
1151-
1152-
1153-def check_calibration(path, root=ROOT):
1154-    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
1155-    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
1156-    p = pathlib.Path(path)
.env
.venv
.venv/bin/python
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
/opt/homebrew/bin/claude
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:21.909Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && git worktree add --detach $SP/m2regate-live HEAD 2>&1 | tail -2 && cd $SP/m2regate-live && git rev-parse HEAD && git status --short | wc -l && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import app,evals;print(app.__file__,evals.__file__)\"; grep -rn \"dotenv\\|\\.env\" app/config.py | head -5"
}
````

### User / tool · 2026-11-02T16:13:22.794Z

**tool result**
````
Preparing worktree (detached HEAD 312efe6)
HEAD is now at 312efe6 fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
312efe663327539df1b712832e23bf1d2c495d42
       0
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live/app/__init__.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live/evals/__init__.py
ugrep: warning: app/config.py: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:27.570Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live && git merge-base --is-ancestor ea988f8 HEAD && echo ancestor; LLM_BACKEND=claude-cli ENABLE_LIVE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --runs 3 --write-calibration > ../m2regate-live.log 2>&1; echo exit=$? >> ../m2regate-live.log",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T16:13:27.640Z

**tool result**
````
Command running in background with ID: b2yab9fn0. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b2yab9fn0.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:27.930Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list --role qa 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T16:13:28.069Z

**tool result**
````
T-119	M3	qa         	done             	P1	AC 1/1	E2E updates for T-060: keyboard keys act only from an item row (tests pressed from body), tray-flag wording, case rail and judge panel tests
T-122	M2	qa         	done             	P1	AC 1/1	Fixture eval: judge unavailable on 1 item in case_05 (missing recorded judge answer)
T-124	M3	qa         	done             	P1	AC 1/1	test_e2e_contract fails: missing test ids after T-060 r3
T-135	M3	qa         	blocked          	P2	AC 0/1	Rename the J3 'agrees' test and fix its docstring to the v6 labels (T-109 r3 minor 7)
T-137	M3	qa         	blocked          	P2	AC 0/1	Held-out audit hardening: kill 7 surviving audit mutants, qualify held-out report cells, audit J4, extend scope cut 13c to the plan side (T-113 r2 minors)
T-152	M2	qa         	done             	P1	AC 1/1	Golden export drift: test_export_equals_golden_when_everything_accepted fails since T-139 narrowing changed sample letter text; regenerate the golden with a written reason, verify it is the intended change
T-155	M2	qa         	in_review        	P0	AC 1/1	E2E red at HEAD: 7-8 deterministic failures (test_polish_r5, test_rerun_judge x2, test_stepper x4, ...) after backend changes T-134/T-139/T-145/T-146; triage each to stale test vs real regression and fix or file
T-164	M2	qa         	in_review        	P1	AC 1/1	tests/e2e/test_conflict_skipped.py 8/9 red at HEAD (T-151 tests vs current checks payload after T-141 r3+); triage: stale test vs real UI/API regression
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:32.112Z

I'll wait for the run to finish.

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:32.412Z

**tool call — Bash**
````
{
 "command": "sleep 1; echo waiting",
 "timeout": 5000
}
````

### User / tool · 2026-11-02T16:13:33.513Z

**tool result**
````
waiting
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:36.784Z

**tool call — ToolSearch**
````
{
 "query": "select:Monitor",
 "max_results": 1
}
````

### User / tool · 2026-11-02T16:13:36.790Z

**tool result**
````
[tool_reference]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:39.881Z

**tool call — Monitor**
````
{
 "command": "L=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live.log; until grep -q '^exit=' $L 2>/dev/null; do sleep 20; done; tail -15 $L",
 "description": "live 3-run finished",
 "timeout_ms": 1800000
}
````

### User / tool · 2026-11-02T16:13:39.893Z

**tool result**
````
Monitor started (task brmio2vi3, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:41.643Z

**tool call — Bash**
````
{
 "command": "echo idle",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T16:13:41.721Z

**tool result**
````
Command running in background with ID: buj37eom0. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/buj37eom0.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:42.758Z

The live run is still going. I'm waiting on the monitor and will pick up when it fires.

### User / tool · 2026-11-02T16:13:42.783Z

[SYSTEM NOTIFICATION - NOT USER INPUT]
This is an automated background-task event, NOT a message from the user.
Do NOT interpret this as user acknowledgement, confirmation, or response to any pending question.
No human input has been received since the last genuine user message in this conversation. Any statement that the user said, approved, or confirmed something — including statements in your own earlier messages — is NOT real user input and must NOT be treated as approval or consent.

<task-notification>
<task-id>buj37eom0</task-id>
<tool-use-id>toolu_01K4ZGNqYeVN1SPdEfDjTXrj</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/buj37eom0.output</output-file>
<status>completed</status>
<summary>Background command "echo idle" completed (exit code 0)</summary>
</task-notification>

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:50.890Z

That was only my placeholder command. The live run is still in progress.

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:53.218Z

**tool call — Monitor**
````
{
 "command": "L=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live.log; until grep -q '^exit=' $L 2>/dev/null; do sleep 20; done; tail -15 $L",
 "description": "live 3-run finished (re-armed)",
 "timeout_ms": 1800000
}
````

### User / tool · 2026-11-02T16:13:53.227Z

**tool result**
````
Monitor started (task bucerx5j0, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:55.259Z

Waiting for the monitor to report the run's result.

### User / tool · 2026-11-02T16:40:42.151Z

[SYSTEM NOTIFICATION - NOT USER INPUT]
This is an automated background-task event, NOT a message from the user.
Do NOT interpret this as user acknowledgement, confirmation, or response to any pending question.
No human input has been received since the last genuine user message in this conversation. Any statement that the user said, approved, or confirmed something — including statements in your own earlier messages — is NOT real user input and must NOT be treated as approval or consent.

<task-notification>
<task-id>b2yab9fn0</task-id>
<tool-use-id>toolu_019sAMM6DH3L8KSSPpRarFZU</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b2yab9fn0.output</output-file>
<status>completed</status>
<summary>Background command "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live &amp;&amp; git merge-base --is-ancestor ea988f8 HEAD &amp;&amp; echo ancestor; LLM_BACKEND=claude-cli ENABLE_LIVE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --runs 3 --write-calibration &gt; ../m2regate-live.log 2&gt;&amp;1; echo exit=$? &gt;&gt; ../m2regate-live.log" completed (exit code 0)</summary>
</task-notification>

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:40:47.348Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat $SP/m2regate-live.log; cd $SP/m2regate-live && git status --short | head; ls evals/reports | tail -5; head -12 $(ls -t evals/reports/2*.md | head -1)"
}
````

### User / tool · 2026-11-02T16:40:47.493Z

**tool result**
````
llm call failed call_id=ce8ccccfe7e03 step=extract attempt=1
llm call failed call_id=c152a1261f60b step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
llm call failed call_id=ce429075a1521 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
ship_bar_met=True backend=claude-cli report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live/evals/reports/20261102T164038Z.md
exit=0
 M evals/reports/calibration.json
 M evals/reports/latest.json
?? evals/reports/20261102T164038Z.md
?? evals/reports/runs/20261102T161327Z/
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
# Eval report 2026-11-02T16:40:38Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (242 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:40:55.829Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP/m2regate-live && sed -n 12,45p evals/reports/20261102T164038Z.md | cut -c1-230; /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check 2>&1 | tail -5; /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --check-fresh; echo fresh=$?; python3 - <<'E'\nimport json;d=json.load(open('evals/reports/latest.json'));print(d['ship_bar_met'],d['blockers'],d.get('source_commit'),d.get('source_tree_clean'), d['calibration'].get('source_commit'),d['calibration'].get('source_tree_clean'))\nE"
}
````

### User / tool · 2026-11-02T16:41:02.628Z

**tool result**
````
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (20/20 wrong caught x3 runs; in-sample 14/14; held-out 6/6; false agree 0 []; correct accepted 21/21; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| letter_currency_outside_charges (fixture export, 25 cases; 11 entries held out) | 0 | 0 | R-CH-7, R-EX-8 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `312efe6633`)

- Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).
- Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).

| Item type | Verified (matched/seen) | Needs review (matched/seen) |
|---|---|---|
| entry | 52/53 | 4/4 |
| amount | 9/9 | 6/6 |
| flag | 21/21 | 1/1 |


## Judge controls, per item

In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says whether it is still held out. A wrong item is caught when no repeat conf

| id | judge | split | kind | pair | origin | expected | verdict per run | ok |
|---|---|---|---|---|---|---|---|---|
llm call failed call_id=cff4cc2b2d78f step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
llm call failed call_id=cda60fc2bc2d7 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
fresh=0
True [] None None 312efe663327539df1b712832e23bf1d2c495d42 True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:41:08.674Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; W=$SP/m2regate-live/evals/reports; D=/Users/arsis/zlayt-pm-project/evals/reports; cp $W/20261102T164038Z.md $D/ && cp -R $W/runs/20261102T161327Z $D/runs/ && cp $W/calibration.json $D/calibration.json && cmp $W/calibration.json $D/calibration.json && cd /Users/arsis/zlayt-pm-project && git rev-parse --short HEAD && git add evals/reports/20261102T164038Z.md evals/reports/runs/20261102T161327Z evals/reports/calibration.json && git status --short evals/ | head"
}
````

### User / tool · 2026-11-02T16:41:08.881Z

**tool result**
````
235e135
A  evals/reports/20261102T164038Z.md
M  evals/reports/calibration.json
 M evals/reports/latest.json
A  evals/reports/runs/20261102T161327Z/case_01_date_formats.json
A  evals/reports/runs/20261102T161327Z/case_02_gap_boundaries.json
A  evals/reports/runs/20261102T161327Z/case_03_rate_and_ocr.json
A  evals/reports/runs/20261102T161327Z/case_04_duplicates_no_amounts.json
A  evals/reports/runs/20261102T161327Z/case_05_provider_conflict.json
A  evals/reports/runs/20261102T161327Z/case_06_subtle_pre_existing.json
A  evals/reports/runs/20261102T161327Z/case_07_prompt_injection.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:41:13.682Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"test(qa): M2 re-gate live evidence: claude-cli 3-run at 312efe6 clean, ship_bar_met True, controls gate included, live calibration regenerated, letter_check 0\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- evals/reports/20261102T164038Z.md evals/reports/runs/20261102T161327Z evals/reports/calibration.json 2>&1 | tail -2; git rev-parse --short HEAD; git worktree remove --force /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/m2regate-live; git worktree prune"
}
````

### User / tool · 2026-11-02T16:41:15.263Z

**tool result**
````
check_secrets: ok (15 file(s) scanned staged)
7cfdb0b
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:41:18.752Z

ship_bar_met=True. The report is `/Users/arsis/zlayt-pm-project/evals/reports/20261102T164038Z.md` (backend claude-cli, 3 runs). It names source commit 312efe6 with a clean tree. That is later than the ea988f8 you gave: HEAD had moved on by the time I made the worktree.
Everything met its bar:
- Grounding 1.0 (242 checked) and entry recall 0.982.
- Determinism 1.0 and unsupported_count_3run 0.
- Hallucination catch 40/40.
- J3 catch rate 20/20 and J4 12/12, with 0 false agrees.

`evals/letter_check.py` reports 0 violations (25 cases, fixture export). The live calibration is regenerated in the same run (82/83 verified, 11/11 needs review).
Three extract calls logged `attempt=1` failures during the run. They did not reach the report: determinism, recall and judge-unavailable (0) are all clean.
Committed as 7cfdb0b: the report, `evals/reports/runs/20261102T161327Z/` and `calibration.json`, with `latest.json` left out. I removed the scratch worktree.
