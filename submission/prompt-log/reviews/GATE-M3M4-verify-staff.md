# GATE-M3M4 verify pass, staff engineer and installer (HEAD 43ce6eb)

Verdict: **pass** (no blockers, no majors; D-075 blockers-only rule applied). All three prior blockers are fixed at `43ce6eb682746e185787de808597312ddce8b0fb`. Two minors go to SCOPE_CUTS.

Scope: a fresh `git archive HEAD` and a fresh `git clone` of HEAD, both under the scratchpad (`vs/arc`, `vs/clone`, plus pristine `vs/arc2`, `vs/arc3`). The working tree of the main repo is dirty (README, app/ and evals/ files show `MM`), so nothing was read from the tree; everything is from the committed HEAD. HEAD is the same commit the T-216 handoff names, so there are no `app/` changes since the 614-passed e2e run and I did not re-run e2e (`git diff HEAD --stat -- app` is empty).

## Prior blockers
1. **B1, LLM_VS_CODE row 19: fixed.** `grep -c 'stated in these records' docs/LLM_VS_CODE.md` is 0. Row 19 now reads: each treatment line carries its date, each charge line carries the fillable blank "date of service [__________]", and "The total line is always exactly 'Billed charges accepted from these records: $X'". That matches `export.py` TOTAL_PREFIX, the golden file and the letter I downloaded in the walk ("Billed charges accepted from these records: $8,390.00").
2. **B2, api.md: fixed.** `grep -n 'Exactly two sources' memory/contracts/api.md` finds nothing. Line 574 says an entry line carries a long date and a charge line carries the blank, and a new "D-073 FALLBACK APPLIED (T-202 r7)" paragraph states the rule: `date of service [__________]` plus `(statement dated X)` or `(record dated X)` or the bare blank, `service_date.state` always `not_stated`, reader kept but not called. It matches `export.charge_when` and my downloaded letter. One leftover sentence is wrong (minor 2).
3. **Installer blocker, README `make evals`: fixed.** On a fresh clone under `env -i` (python 3.12 first on PATH), `make evals` exits 2 with "Error 1" and the last lines name exactly three `blocker:` items (`4_no_invented_facts`, `backend=fixture: determinism_3run ...`, `judge_controls ... not measured`). `grep -c spec_matches_golden` on the output is 0. `python -m evals.run --check-spec` prints `{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}` with exit 0 in both the clone and the archive. `spec/REQUIREMENTS.md:260` now reads "date of service [__________] (record dated January 9, 2026): $6,240.00", equal to golden line 42.

## Suite
- Full `tests/unit` in the fresh clone (`./run.sh test`): 5950 passed, 6 skipped, 1 failed (447 s). The one failure, `test_t045_r2.py::test_the_committed_latest_json_still_matches_what_record_latest_would_write`, was caused by my own earlier `--check-spec` run, not by HEAD: `--check-spec` rewrites the tracked `evals/reports/latest.json` (adds `letter_equal` and `internal_notes_equal`), and the committed file lacks those keys. On a pristine archive that test passes (19 passed), and after `--check-spec` it fails (minor 1). `make evals` leaves `latest.json` byte-identical to HEAD (cmp) and the test still passes after it. So the suite is green on a pristine HEAD, and the one failing test reproduces only after the gate's own `--check-spec` command.
- e2e: not re-run, per brief (HEAD equals the handoff sha 43ce6eb; T-216 AC 1 cites 614 passed, 1 skipped, 0 failed).

## README walk on a fresh clone
`env -i PORT=7931 ./run.sh` built the venv and served in demo mode (`/api/health` ok, `demo_mode` true, backend fixture). A Playwright script (`artifacts/review-evidence/GATE-M3M4-verify-staff/walk.py`) followed the README: Open the sample case, "We found 9 records", Draft the timeline, "19 timeline items and 4 bill amounts", answered all 19 and 4, "You checked every bill amount", `$8,390.00`, "Your letter is ready", Download letter. Zero page errors. The letter has the two charge lines with the fillable blank and the exact total line. The server PID 42551 (cwd confirmed as my clone) was killed; port 7931 has no listener. `python -m app.pipeline evals/golden/sample.txt` run twice gives identical output (3842 bytes, `cmp` silent).

## Findings
1. **minor** (SCOPE_CUTS) `python -m evals.run --check-spec` writes the tracked `evals/reports/latest.json` and the committed copy has no `letter_equal` or `internal_notes_equal` keys, so running the gate's own check turns one unit test red until the file is reset. The main repo shows the same state now (`MM evals/reports/latest.json`) and that test fails there.
2. **minor** (SCOPE_CUTS) `memory/contracts/api.md:574` (retained-reader text) says "a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line". `export.charge_when` ignores `dos_iso` and prints the blank, and the same paragraph says dos_* are ignored. Sentence is inside the block labelled "retained reader, not what the letter prints", so not a blocker.

```json
{"card": "GATE-M3M4-verify", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD and git clone at 43ce6eb682746e185787de808597312ddce8b0fb; README run via ./run.sh on 127.0.0.1:7931 under env -i; sample case walk to the letter; docs/LLM_VS_CODE.md row 19, memory/contracts/api.md D-073 text, README Tests and evals, evals.run --check-spec",
 "exercised": [
  "git log -1 and git diff HEAD --stat -- app (empty): HEAD 43ce6eb equals the T-216 e2e sha; main working tree is dirty so only git archive/clone content was used",
  "grep -c 'stated in these records' docs/LLM_VS_CODE.md = 0; read row 19; compared with export.py TOTAL_PREFIX and the downloaded letter",
  "grep 'Exactly two sources' memory/contracts/api.md = none; read api.md 574-575 and export.charge_when",
  "env -i make evals on a fresh clone: exit 2, three blocker lines, no spec_matches_golden line",
  "python -m evals.run --check-spec in clone and archive: all three true, exit 0; spec/REQUIREMENTS.md:260 vs golden line 42",
  "./run.sh test (tests/unit) in fresh clone: 5950 passed, 6 skipped, 1 failed (test_t045_r2 latest.json) ; pristine archive test_t045_r2.py: 19 passed; after --check-spec: 1 failed; after make-evals path: 19 passed",
  "env -i PORT=7931 ./run.sh on a fresh clone; Playwright README walk steps 1-5 with letter download; pageerrors empty; PID 42551 verified by cwd and killed",
  "python -m app.pipeline evals/golden/sample.txt twice from a pristine archive: cmp identical",
  "e2e not re-run (HEAD unchanged since T-216 handoff 614 passed, 0 failed)"],
 "verdict": "pass",
 "scores": {"prior_blockers_fixed": 5, "doc_accuracy": 4, "suite_green_on_pristine_head": 4, "readme_install_and_walk": 5},
 "findings": [
  {"severity": "minor", "title": "--check-spec rewrites tracked latest.json and the committed copy lacks the new keys, so a unit test goes red after it",
   "evidence": "In a pristine git archive: pytest tests/unit/test_t045_r2.py -> 19 passed; python -m evals.run --check-spec; cmp evals/reports/latest.json <(git show HEAD:evals/reports/latest.json) -> differ; pytest again -> 1 failed (test_the_committed_latest_json_still_matches_what_record_latest_would_write: 'Left contains 2 more items: internal_notes_equal, letter_equal'). evals/run.py:9 docstring: '--check-spec ... writes spec_matches_golden'.",
   "why_it_matters": "A reviewer or QA running the gate's check-spec command then the suite sees a red test that is not a product defect, and the tracked file is dirtied.",
   "fix": "Commit latest.json with the two keys, or have the test ignore them, or have --check-spec write elsewhere.",
   "acceptance_test": "From a pristine archive: python -m evals.run --check-spec then pytest tests/unit/test_t045_r2.py passes."},
  {"severity": "minor", "title": "api.md retained-reader text claims a hand-built case without dos_iso keeps the old record-date line",
   "evidence": "memory/contracts/api.md:574 'a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line, and one without `dos_text` prints the blank'; app/backend/export.py:210-215 charge_when always prints the blank and never reads dos_iso; same paragraph says 'A case dict's dos_iso / dos_end_iso / dos_text are ignored by the letter'.",
   "why_it_matters": "Two sentences in one paragraph disagree; the first is false for the code.",
   "fix": "Delete that clause from the retained-reader description.",
   "acceptance_test": "grep -c 'keeps the old' memory/contracts/api.md returns 0."}
 ],
 "whats_right": [
  "The three prior blockers are fixed and the doc text now matches the code, the golden file and the downloaded letter.",
  "README path holds on a fresh clone under env -i: server healthy, walk reaches $8,390.00 and a downloadable letter with the date blanks, zero page errors.",
  "make evals behaves exactly as the README now says (three blocker lines, exit 2) and leaves the committed latest.json untouched."],
 "questions_for_chris": []}
```
