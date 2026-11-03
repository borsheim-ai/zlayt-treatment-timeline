# T-045 staff-engineer review, round 3 (scoped)

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commits under review: b824a6c and 964505b (HEAD 964505b). Scope: the r2 blocker (`--record-latest` trusted the header) and the five checks in the brief. Verdict: **pass** (0 blockers, 0 majors, 1 minor, 2 nits).

## Result
The r2 blocker is closed for the case it named. A hand-flipped header is refused, the ship bar is recomputed with the runner's own `ship_bar()`, the report's sha256 and source commit are recorded, `--check-fresh` exits 0 on the real report, and `tests/unit/test_t045_r2.py` passes 19 of 19. Seven mutants of `evals/run.py` each fail that file, and the file was restored byte-identical to HEAD afterwards.

The caveat in the brief (full metrics never committed) is accepted. I probed its reach. It is wider than one table row: a consistent hand-forgery of a fixture report, with its backend label relabelled, records as live. That is finding 1 (minor). Under the brief's accepted caveat it does not change the verdict, but Chris should confirm the caveat covers it.

## Checks against the brief
- **Refuses a non-live backend:** the committed fixture report, unmodified (C1), and the same report with its header flipped to True (C2), both exit 2 with "backend `fixture` is not a live backend". Evidence: artifacts/review-evidence/T-045-r3/probe_record_latest.out.
- **Refuses a hand-flipped header:** C2 as above. A live report with its header flipped to False (C3) exits 2 with "header says ship_bar_met False but the ship bar recomputed ... is True". A live report with entry_recall edited to 0.500 and the header kept True (C7) exits 2 with "is False (failing: 2_recall)".
- **Refuses a missing per-run directory:** C5 (the `- per-run artifacts:` line removed) exits 2 "names no per-run directory". C6 (line pointing at runs/20261102T000000Z) exits 2 "is missing or does not hold exactly run1.json, run2.json and run3.json".
- **Recomputes with the runner's function:** `recompute_ship_bar` calls `ship_bar(m, a, hd["backend"], spec)` at evals/run.py:1256. The runner's own path uses the same function: `evaluate_report` at evals/run.py:959, called from `build_report` at evals/run.py:1003. Mutant M1 (header trusted, recompute bypassed) fails 8 tests.
- **Records sha256 and source commit:** C4 (live report, unmodified) is accepted. `evals/reports/latest.json` at HEAD records `recorded_from.sha256` 03eafb83f90c3d46cf8b9bc009dbab0ef17fc7056d7ab4e453e12117036bb5e3, which equals `shasum -a 256` of `evals/reports/20261102T164038Z.md`, and `source_commit` 312efe663327539df1b712832e23bf1d2c495d42, which is the report's own `Source commit` line.
- **`--check-fresh` exits 0 with the real report:** exit 0 on the clean clone before the probes and again after them.
- **`tests/unit/test_t045_r2.py`:** 19 passed in 27.71s.

## Findings

1. **Minor: a consistent hand-forgery of a fixture report records as live.** The r2 blocker was a one-line header flip. r3 closes that. The recompute reads the report body, and the backend label and the per-run pointer are also read from editable text. Evidence: `probe_forgery.out` shows `exit 0` and `latest.json backend claude-cli ship_bar_met True recorded_from.report probe_forgery_fixture_as_live.md sha256_matches_copy True`. The forgery relabels the header backend (evals/run.py:1162 reads it, the refusal at evals/run.py:1275 keys on it), appends a per-run line, and copies the J3/J4 rows and the unsupported row from the live report. The bar is then recomputed from the forged body (evals/run.py:1243-1256), and the sha256 at evals/run.py:1284 is taken after the edit, so it proves nothing about origin. Why minor and not blocker: the brief accepts the root cause (metrics not committed), the forgery is deliberate and multi-line, and it is visible in `git diff` of the committed report. Why it still matters: the caveat as worded covers "a hand-edited table row"; this path also needs the backend label and the per-run pointer, which the caveat does not name. Fix: name the unsealed fields (report body, backend label, per-run pointer) in the accepted-debt note, or commit the aggregate sidecar r2 proposed and derive the bar from it. Acceptance test: if the sidecar route is taken, a consistent forged body is refused because the sidecar disagrees; if the note route is taken, the note names the three fields and Chris confirms in writing.

2. **Nit: the parity unit test covers part of the bar inputs.** `tests/unit/test_t045_r2.py:198` (`test_report_body_parse_matches_the_runner_on_a_rendered_report`) asserts the assertions dict, spec_matches_golden, grounding, entry and amount values, and flag precision and recall. It does not assert unsplit_paste, the letter_currency row, the J3/J4 seeded rows, the hallucination judge-unavailable count, the controls-judged-unsupported count, or spec_matches_golden through the record path. I hand-edited six of those inputs in the committed live report with the header kept True (P1 to P6). All six were refused with exit 2 (`probe_parser_inputs.out`), so the parser does read them. This is a test gap, not a correctness defect. Fix: extend the parity test to compare `metrics_from_report_md` against the runner's dict for every input `ship_bar` reads, or pin P1 to P6 as record-latest unit tests.

3. **Nit: the recompute reads a 3-decimal rendering.** `pct()` at evals/run.py:1009-1010 formats `%.3f`, and `metrics_from_report_md` reads the rounded string through `_num` at evals/run.py:1218. Reasoned from the code, not reproduced: grounding's threshold is 1.0 (evals/run.py:43), and 2000 of 2001 checks displays as 1.000. The recompute would then disagree with a runner False, and `record_latest` refuses that at evals/run.py:1281. So rounding can cause a refusal of a legitimate report, but I found no path where it causes a false accept. The commit message says "exact at these N", which is true for the current N (241 or 242 checked). Fix: state the bound in the `metrics_from_report_md` docstring, or read the unrounded value from the per-run files.

Also observed, not a finding: the committed fixture report `evals/reports/20261102T195748Z.md:6` still reads "4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7); judge_controls ...", with no clause on why bar 4 fails. The r2 F-2 text is in code at evals/run.py:935-936 and only appears on the next fixture run. The unit test `test_the_fixture_bar_4_blocker_names_its_live_only_clauses` passes, so the code fix is covered.

## Mutation results (all in a clean clone, each applied once, file restored byte-identical to HEAD)
- M1 header trusted, recompute bypassed: 8 failed, 11 passed.
- M2 non-live refusal removed: 1 failed (`test_record_latest_refuses_a_hand_flipped_fixture_report`).
- M3 header-vs-recompute refusal removed: 4 failed.
- M4 missing run directory no longer refused: 1 failed (`test_record_latest_refuses_when_the_per_run_directory_is_missing`).
- M5 determinism taken from the table (1.0) instead of the run directory: 1 failed (`test_record_latest_takes_determinism_from_the_run_directory_not_the_table`).
- M6 sha256 not recorded: 4 failed.
- M7 source commit not recorded: 2 failed.
Evidence: artifacts/review-evidence/T-045-r3/mutants.out and mutants.py.

## Evidence
All under /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-045-r3/: probe_record_latest.py and .out (C1 to C7), probe_forgery.py and .out (finding 1), probe_parser_inputs.py and .out (P1 to P6, finding 2), mutants.py and .out (M1 to M7). The clean clone was detached at 964505b under the session scratchpad (`t045r3-clean`); `git status --short` was empty before the probes.

## Not exercised
- The full unit suite (the 5782 figure in m3-sensors.md) and the e2e suite were not re-run.
- The live eval was not re-run (cost).
- A run directory that holds only some of run1 to run3 was not probed; the code requires exactly three files.
- No app URL; the scope is the eval runner.
- The line counts and figures in the card handoff for F-3 were not checked.

```json
{"card": "T-045", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits b824a6c and 964505b (HEAD 964505b): evals/run.py, tests/unit/test_t045_r2.py, evals/reports/latest.json, evals/reports/m3-sensors.md; clean clone detached at 964505b under the session scratchpad (t045r3-clean); committed reports evals/reports/20261102T164038Z.md (live) and evals/reports/20261102T195748Z.md (fixture); no app URL",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-045-staff-engineer-r2.md, memory notes for T-045 r2, and python3 tools/board.py show T-045 (status in_review, rounds 2).",
  "git show b824a6c -- evals/run.py, latest.json, tests/unit/test_t045_r2.py; git show 964505b -- evals/reports/m3-sensors.md.",
  "git clone of the repo into the session scratchpad, git checkout --detach 964505b; git status --short empty (CLEAN_OK).",
  ".venv/bin/python -m evals.run --check-fresh in the clean clone: exit 0, before and after the probes.",
  ".venv/bin/python -m pytest tests/unit/test_t045_r2.py -q: 19 passed in 27.71s.",
  "artifacts/review-evidence/T-045-r3/probe_record_latest.py (C1 fixture unmodified, C2 fixture header flipped True, C3 live header flipped False, C4 live unmodified, C5 per-run line removed, C6 per-run dir absent, C7 entry_recall 0.500 with header True): exit 2 on C1, C2, C3, C5, C6, C7; exit 0 on C4 with recorded sha256 and source_commit; output in probe_record_latest.out; latest.json restored.",
  "artifacts/review-evidence/T-045-r3/mutants.py: seven mutants of evals/run.py (M1 header trusted, M2 non-live refusal removed, M3 mismatch refusal removed, M4 missing run dir allowed, M5 determinism from table, M6 sha256 unrecorded, M7 source commit unrecorded), each anchor count-checked and applied once; failures 8, 1, 4, 1, 1, 4, 2 respectively; file restored byte-identical to HEAD; output in mutants.out.",
  "artifacts/review-evidence/T-045-r3/probe_forgery.py: fixture report with header relabelled backend claude-cli and True, per-run line added, J3/J4 rows and unsupported row copied from the live report: exit 0, latest.json backend claude-cli ship_bar_met True, sha256 matches the forged file; output in probe_forgery.out; latest.json restored.",
  "artifacts/review-evidence/T-045-r3/probe_parser_inputs.py: six single-row edits to the committed live report with header True (unsplit_paste, letter_currency, J3 seeded, hallucination judge unavailable, controls judged unsupported, spec_matches_golden): all six exit 2; output in probe_parser_inputs.out.",
  "Read evals/run.py: LIVE_BACKENDS 39; THRESHOLDS 43; ship_bar 913-960; evaluate_report 957-960; build_report use 1003; render_md 1058-1092; write_report 1115-1142; parse_report_md 1154-1171 (backend from header at 1162); metrics_from_report_md 1179-1231; determinism_from_run_dir 1233-1241; recompute_ship_bar 1243-1257; record_latest 1260-1291; check_fresh 1294-1313; pct 1009-1010; fixture bar-4 why text 935-936.",
  "Grepped the committed reports: 20261102T164038Z.md header True claude-cli, Source commit 312efe6, per-run line at 131; 20261102T195748Z.md header False fixture, Blockers line 6; shasum -a 256 of 20261102T164038Z.md = 03eafb83...; git show b824a6c of latest.json: recorded_from sha256, source_commit 312efe66...",
  "Not exercised: full tests/unit suite (5782 claim in m3-sensors.md), tests/e2e suite, live claude-cli eval (cost), a run directory with fewer than three run files, the F-3 count in m3-sensors.md."
 ],
 "verdict": "pass",
 "scores": {"refuses_non_live_backend": 5, "refuses_hand_flipped_header": 5, "refuses_missing_per_run_dir": 5, "recomputes_with_runner_ship_bar": 4, "records_sha256_and_source_commit": 5, "check_fresh_real_report": 5, "unit_file_passes": 5, "provenance_beyond_header_and_table": 3},
 "findings": [
  {"severity": "minor",
   "title": "A consistent hand-forgery of a fixture report records as live; the accepted caveat covers the root cause, not this reach",
   "evidence": "artifacts/review-evidence/T-045-r3/probe_forgery.out: exit 0; 'latest.json backend claude-cli ship_bar_met True recorded_from.report probe_forgery_fixture_as_live.md sha256_matches_copy True'. Forgery edits the header backend (evals/run.py:1162 reads it; refusal at evals/run.py:1275 keys on it), appends a per-run line, and copies the J3/J4 rows and unsupported row from the live report. Bar recomputed from the forged body at evals/run.py:1243-1256; sha256 at evals/run.py:1284 is taken after the edit.",
   "why_it_matters": "The r2 blocker was a one-line header flip and r3 closes that case. The record still trusts an unsealed body, backend label and per-run pointer. The accepted caveat names a hand-edited table row, not these fields. Detection depends on git diff and review, not on record-latest. Rated minor because the brief accepts the root cause, the forgery is deliberate and multi-line, and it is visible in git diff.",
   "fix": "Name the unsealed fields (report body, backend label, per-run pointer) in the accepted-debt note, or commit the aggregate sidecar r2 proposed and derive the bar from it.",
   "acceptance_test": "Sidecar route: a consistent forged body is refused because the sidecar disagrees (probe_forgery.py exits 2). Note route: the note names the three fields and Chris confirms in writing."},
  {"severity": "nit",
   "title": "The parity unit test covers only part of the bar inputs",
   "evidence": "tests/unit/test_t045_r2.py:198 asserts assertions, spec_matches_golden, grounding, entry and amount values, and flag precision/recall only. Hand edits to unsplit_paste, letter_currency, J3 seeded row, hallucination judge-unavailable, controls judged unsupported, and spec_matches_golden were all refused (artifacts/review-evidence/T-045-r3/probe_parser_inputs.out, six exit=2 lines).",
   "why_it_matters": "The parser does read these inputs today; a future parser change could silently stop reading one and no unit test would notice.",
   "fix": "Extend the parity test to compare metrics_from_report_md with the runner's dict for every input ship_bar reads, or pin cases P1 to P6 as record-latest unit tests.",
   "acceptance_test": "Each of the six single-row edits in probe_parser_inputs.py makes record-latest exit 2 in a unit test that runs without a clone."},
  {"severity": "nit",
   "title": "The recompute reads a 3-decimal rendering, not the runner's value",
   "evidence": "evals/run.py:1009-1010 pct() formats %.3f; evals/run.py:1218 reads the rounded string through _num. Grounding threshold 1.0 at evals/run.py:43. Reasoned from code, not reproduced: 2000 of 2001 displays as 1.000.",
   "why_it_matters": "A runner False could be recomputed as True and then refused at evals/run.py:1281, so a legitimate report may be refused. I found no path to a false accept. The commit message says exact at these N, which holds for the current 241 and 242 checked.",
   "fix": "State the bound in the metrics_from_report_md docstring, or read the unrounded values from the per-run files.",
   "acceptance_test": "A unit test with 2000 of 2001 grounded checks shows the recompute and the runner agree, or the docstring names the N limit."}
 ],
 "whats_right": [
  "The header is no longer trusted: a fixture header flipped to True is refused as a non-live backend and a live header flipped to False is refused as a mismatch (probe_record_latest.out C2, C3).",
  "Seven mutants of evals/run.py each fail tests/unit/test_t045_r2.py, and the file was restored byte-identical to HEAD (mutants.out).",
  "The committed live report is accepted with recorded sha256 03eafb83... equal to the file and source_commit 312efe66..., and --check-fresh exits 0 before and after the probes."
 ],
 "questions_for_chris": ["Does the accepted caveat cover the backend label and the per-run pointer as well as the table row? probe_forgery.out records a fixture as live with a consistent multi-line edit. If not, the r2 sidecar fix is the route; if so, please confirm in the accepted-debt note."]}
```
