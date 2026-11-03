# T-132 staff-engineer review, round 5 (scoped final check after the r4 fix-up, ed45b4a)

Verdict: pass. No blockers, no majors. One minor and one nit, neither changes the verdict.

Scope was the five checks the orchestrator set on `git archive HEAD` (HEAD 5de16d3; the only commit after ed45b4a is `memory/SCOPE_CUTS.md` +1 line, no code change):

1. The extension stops only at an ALL-CAPS label, a closed-list section or vitals label followed by a colon (Dx included), a bullet, a blank line or a sentence end. Checked by a 49-row probe (`T-132-r5-items-HEAD.txt`): 49 of 49 PASS.
2. 'Left wrist swollen:' and similar clinical phrases ending in a colon do not stop it. Rows N1-N13 PASS. The r4 regex put back in a scratch copy fails 8 T-132 tests, so the test file guards this shape.
3. The r4 major is fixed. K1 (`Hx obtained via patient's son;\nLeft wrist swollen: since Monday.`) now gives one pre_existing flag whose quote contains the condition; K3 (`Dx:`) still stops at `Hx per EMS;`. Evidence: `T-132-r5-lost-HEAD.txt`.
4. The fuzz oracle shows 0 non-verbatim quotes: `T-132-128-r3/T-132-r3-fuzz.py` on the archive, 20,000 texts, seed 1 → 0 not-verbatim, 0 blank-line, 0 overlap, 57 ends-inside-phrase (the 13e leftover, not failed). `T-132-r3-fuzz2.py` → 0 failing at 12,000 seed 7 and 6,000 seed 1; the r4 control fails 76 of 6,000, so the oracle discriminates.
5. The unit suite passes. T-132 file plus summary_trim: 506 passed. Full `tests/unit` on the archive: 3,783 passed, 1 skipped, 1 deselected (see the note below on the deselected test).

## Findings

- **minor, not a verdict driver.** An ALL-CAPS condition line ends the quote, and the condition then appears in no flag: `Hx per EMS;\nNECK PAIN: onset 2019.` gives only `Hx per EMS;`, and `LEFT WRIST SWOLLEN: since Monday.` does the same. This follows the stated rule (a), which names ALL-CAPS labels as stops, so it is not a violation of the rule as written. It is the same loss the r4 major described (a condition dropped from its quote), and the orchestrator's own principle was that a quote dropping the condition is worse than one that runs long. Recorded for a decision, see `questions_for_chris`.
- **nit.** The card AC says `tests/unit/test_t132_attribution_unit.py (189 pass)`. At HEAD the file collects 188 (`pytest tests/unit/test_t132_attribution_unit.py --co -q`: `188 tests collected`), and its run is `188 passed`. Correct the count in the AC evidence.

## Notes outside the verdict

- The deselected test, `tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit`, fails in any export whose `git archive` runs from a subtree (the archive dir): `git archive HEAD | tar -t | wc -l` run inside `artifacts/review-evidence/T-132-r5/arc` gives `0`. The same test passes in the live root (`1 passed`). This is the placement artifact r4 documented. It is a test that depends on a live git checkout, not a T-132 defect; qa-owned, not this card.
- Probe row B8 (`Hx per EMS.\nNeck pain.`) was first written with a wrong expectation (a flag `Hx per EMS.`). Control and HEAD both give no flag, because an attribution-only sentence raises nothing. I corrected the expectation to match and recorded that in the file. The first run is not counted.
- The r4 minor on the wall-clock bound is fixed: no `perf_counter`, `time.time` or `assert dt` in the archived T-132 test file (`grep` exit 1).
- The r4 minors on X3 (sentence-final `Dr.`), bare initials and the 57 fragments are the 13e scope cut. Not failed here, as instructed. Titled-name who-clauses (D6, X4) were not re-probed in this scoped check.

## What I exercised

- Read `personas/staff-engineer.md`, `reviews/T-132-staff-engineer-r4.md`, `board show T-132` (status in_review; orchestrator note 2026-11-02T13:32:16Z), `memory/SCOPE_CUTS.md` row 13e, `git show ed45b4a -- app/backend/lexicon_scan.py`.
- `git rev-parse HEAD` → `5de16d3801004abdeae1c5c86cc0fde3811e5ee8`; `git diff --stat ed45b4a HEAD` → `memory/SCOPE_CUTS.md | 1 +` only.
- `git archive HEAD | tar -x -C artifacts/review-evidence/T-132-r5/arc` (2,190 entries); `diff -q` of `app/backend/lexicon_scan.py`, `app/backend/flags.py`, `tests/unit/test_t132_attribution_unit.py` against the archive: identical.
- Import check with `.venv/bin/python -I`: the archive's `app.backend.lexicon_scan` and `app.backend.flags` resolve to the archive path; `_LINE_LABEL` pattern printed.
- `T-132-r5-items.py` on the HEAD archive: 49 PASS, 0 FAIL (`T-132-r5-items-HEAD.txt`). Same script on the r4 archive (`T-132-r5-items-r4arc.txt`): 13 FAIL. On the r3 control (`T-132-r5-items-ctl.txt`): 26 FAIL.
- `T-132-r4/T-132-r4-lost.py` on HEAD, r4 and control: K1 one flag with the condition on HEAD; attribution-only on r4; K3 stops on HEAD.
- `T-132-r5-caps-condition-HEAD.txt`: the ALL-CAPS probe above.
- `pytest tests/unit/test_t132_attribution_unit.py -q -p no:cacheprovider` on the archive: `188 passed`. With `tests/unit/test_summary_trim.py`: `506 passed`.
- Full `pytest tests/unit -q -p no:cacheprovider` on the archive: `1 failed, 3783 passed, 1 skipped` (`T-132-r5-unit-HEAD.txt`), the failure being the placement artifact above. Re-run with that one test deselected: `3783 passed, 1 skipped, 1 deselected`, exit 0 (`T-132-r5-unit-HEAD-deselect-calib.txt`).
- `T-132-128-r3/T-132-r3-fuzz.py <arc> 20000 1` → `samples 20000 problems 57` (`T-132-r5-fuzz-HEAD-20000-s1.txt`): 57 lines, all ends-inside-phrase; `grep -c not-verbatim` = 0, `blank-line` = 0, `OVERLAP` = 0, `EXC` = 0.
- `T-132-128-r3/T-132-r3-fuzz2.py <arc> 12000 7` → `failing 0`; `<arc> 6000 1` → `failing 0`; control `T-132-r4/ctl 6000 1` → `failing 76` (`T-132-r5-fuzz2-*.txt`).
- Mutants in scratch copies under `artifacts/review-evidence/T-132-r5/mut/`: `r4regex` (the r4 `_LINE_LABEL` restored) → `8 failed, 180 passed`, including the `Left wrist swollen` and `Neck pain:` rows; `nolabel` (`_LINE_LABEL` disabled) → `32 failed, 156 passed`.
- Grep for wall-clock in the archived T-132 test file (`perf_counter|dt <|import time|time.time`): no match.

Not exercised: the sample CLI `python -m app.pipeline evals/golden/sample.txt` and the evals runner (the change is confined to scan-side code and the T-132 tests); browser and API views; `flags.merge` live path.

```json
{"card": "T-132", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD 5de16d3 (artifacts/review-evidence/T-132-r5/arc; code identical to ed45b4a, only memory/SCOPE_CUTS.md differs after it); app/backend/lexicon_scan.py (_LINE_LABEL, _soft_wraps, _extend_attribution_unit), app/backend/flags.py, tests/unit/test_t132_attribution_unit.py; fixture-only, no network, no server; sample CLI not re-run in this scoped check",
 "exercised": [
  "personas/staff-engineer.md read; reviews/T-132-staff-engineer-r4.md read; board show T-132 and orchestrator note 2026-11-02T13:32:16Z read; memory/SCOPE_CUTS.md 13e read; git show ed45b4a -- app/backend/lexicon_scan.py read",
  "git rev-parse HEAD = 5de16d3; git diff --stat ed45b4a HEAD = memory/SCOPE_CUTS.md only; git archive HEAD into artifacts/review-evidence/T-132-r5/arc (2190 entries); diff -q of lexicon_scan.py, flags.py, the T-132 test: identical to archive",
  "python -I import check: archive app.backend.lexicon_scan and flags resolve to the archive path; _LINE_LABEL pattern printed",
  "T-132-r5-items.py on HEAD archive: 49 PASS / 0 FAIL (T-132-r5-items-HEAD.txt); same on r4 archive: 13 FAIL (T-132-r5-items-r4arc.txt); on r3 control: 26 FAIL (T-132-r5-items-ctl.txt); expectation for row B8 corrected before the counted run",
  "T-132-r4-lost.py on HEAD / r4 / control: K1 one pre_existing flag containing 'Left wrist swollen' on HEAD (T-132-r5-lost-HEAD.txt); K3 stops at 'Hx per EMS;' on HEAD",
  "T-132-r5-caps-condition-HEAD.txt: 'Hx per EMS;\\nNECK PAIN: onset 2019.' and 'LEFT WRIST SWOLLEN' -> flag 'Hx per EMS;' only (condition in no flag)",
  "pytest tests/unit/test_t132_attribution_unit.py -q on archive: 188 passed (file collects 188); with tests/unit/test_summary_trim.py: 506 passed",
  "pytest tests/unit -q on archive: 1 failed, 3783 passed, 1 skipped (T-132-r5-unit-HEAD.txt); failure test_committed_calibration_regenerates_exactly_from_its_source_commit is a subtree-archive artifact (git archive HEAD inside the archive dir = 0 entries; live root: 1 passed); with that test deselected: 3783 passed, 1 skipped, 1 deselected, exit 0 (T-132-r5-unit-HEAD-deselect-calib.txt)",
  "T-132-128-r3/T-132-r3-fuzz.py <archive> 20000 1: 57 problems, all ends-inside-phrase; 0 not-verbatim, 0 blank-line, 0 overlap, 0 exceptions (T-132-r5-fuzz-HEAD-20000-s1.txt)",
  "T-132-128-r3/T-132-r3-fuzz2.py <archive> 12000 7 and 6000 1: failing 0 and 0 (T-132-r5-fuzz2-HEAD-*.txt); control T-132-r4/ctl 6000 1: failing 76 (oracle discriminates)",
  "Mutants in scratch copies under artifacts/review-evidence/T-132-r5/mut/: r4 _LINE_LABEL restored -> 8 failed, 180 passed (incl. Left wrist swollen and Neck pain: rows); _LINE_LABEL disabled -> 32 failed, 156 passed",
  "grep of archived T-132 test file for perf_counter, 'dt <', import time, time.time: no match (wall-clock bound removed)",
  "Not exercised: python -m app.pipeline evals/golden/sample.txt and the evals runner; browser/API view; flags.merge live path"],
 "verdict": "pass",
 "scores": {"correctness": 4, "determinism": 4, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [
  {"severity": "minor",
   "title": "An ALL-CAPS condition line ends the prior-condition quote, so the condition is in no flag",
   "evidence": "artifacts/review-evidence/T-132-r5/T-132-r5-caps-condition-HEAD.txt: 'Hx per EMS;\\nNECK PAIN: onset 2019.' -> [('pre_existing', 'Hx per EMS;')]; 'Hx per EMS;\\nLEFT WRIST SWOLLEN: since Monday.' -> [('pre_existing', 'Hx per EMS;')]. Cause: app/backend/lexicon_scan.py:151 _SECTION_HEADER (caps label) used as a hard break at :177 in _soft_wraps. Probe row S24 in T-132-r5-items-HEAD.txt passes as designed.",
   "why_it_matters": "The stop follows the stated rule (a) (ALL-CAPS labels stop), so it is not a violation of the rule as written and is rated minor. But the shape is the same one the r4 major described (a condition dropped from every flag), and the orchestrator's principle was that a quote which drops the condition is worse than one that runs long. A paralegal reading the flag sees prior history with no condition for an all-caps line. Nothing is invented and the record is intact.",
   "fix": "Decide and record it. Either (i) accept the stop and add a SCOPE_CUTS row citing 'NECK PAIN: onset 2019.' as the example, or (ii) stop only on ALL-CAPS labels that are section headers (a closed list or a header-only line with no trailing content), so an all-caps condition with content continues.",
   "acceptance_test": "Either a SCOPE_CUTS row names 'Hx per EMS;\\nNECK PAIN: onset 2019.' and the probe row S24 is kept as a documented stop, or the row gives one pre_existing flag whose quote contains 'NECK PAIN: onset 2019.' while 'Dx:' and 'DX: sprain' still stop (rows S1 and S27 in T-132-r5-items.py)."},
  {"severity": "nit",
   "title": "The card AC cites 189 passing tests for the T-132 file; the file has 188",
   "evidence": "`.venv/bin/python -m pytest tests/unit/test_t132_attribution_unit.py -q -p no:cacheprovider --co` at HEAD 5de16d3 (archive): '188 tests collected'; the run: '188 passed in 1.26s'. Card AC 1 text: 'tests/unit/test_t132_attribution_unit.py (189 pass)'.",
   "why_it_matters": "Evidence accuracy only; the tests pass. A miscounted AC makes the next reviewer distrust the rest of the evidence line.",
   "fix": "Correct the count in the AC 1 evidence to the collected number at the commit that is reviewed.",
   "acceptance_test": "`pytest tests/unit/test_t132_attribution_unit.py --co -q` count equals the number in AC 1 evidence."}
 ],
 "whats_right": [
  "K1 and 'Left wrist swollen:' now keep the condition in one pre_existing flag, and K3 still stops at 'Hx per EMS;': the 49-row probe passes 49 of 49 on HEAD, where r4 failed 13.",
  "The test file guards the r4 regression: the r4 _LINE_LABEL restored in a scratch copy fails 8 T-132 tests, including the 'Left wrist swollen' and 'Neck pain:' rows, and the closed-list rows are parametrised over the list.",
  "The verbatim invariant holds: 0 not-verbatim and 0 blank-line quotes in 20,000 fuzz texts, and 0 failing in the partial-overlap oracle at two seeds where the r4 control fails 76 of 6,000."],
 "questions_for_chris": ["Should an ALL-CAPS condition line such as 'NECK PAIN: onset 2019.' end a prior-condition quote? The rule as decided (a) stops there, so the condition appears in no flag (T-132-r5-caps-condition-HEAD.txt). Rated minor because the stated rule names ALL-CAPS labels; the decision is yours, and it should go in SCOPE_CUTS either way."]
}
```
