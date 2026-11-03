# T-133 r5 review (staff-engineer-reviewer): fix-up 15be212, scoped check

Scope: the r4 fix-up commit 15be212 (`app/llm/lexicon.yaml`, `tests/unit/test_t133_lexicon.py`), pinned to `git archive HEAD` (HEAD 330fc0c). HEAD's product tree is identical to 15be212; the only file that differs is `reviews/GATE-M2-round1-triage.md`. The main tree was not edited. Scratch work is under the scratchpad (`T-133-r5-*`).

Verdict: **pass**. No blocker, no major. The code fix holds: a bare `History:` on its own line stays quiet, and qualified headers still flag. The findings are four minors and two nits, mostly in memory records and in the test design. One minor is carried from r4 and is deferred by the orchestrator to the M2 run.

## Brief checks

| Check | Result | Evidence |
|---|---|---|
| Bare `History:` on its own line stays quiet, whatever the previous line ends with (LF, CRLF, blank line, CR-only) | Pass | 12 previous-line endings x 5 separators x 4 header forms = 240 of 240 quiet on HEAD and on 15be212 (`T-133-r5-probe.py`). The r4 archive (6fa8ecc) is quiet on 234 of 240; its 6 failures are a letter then LF or CR, which is the control that shows the probe can fail |
| `Past history:` and `Medical history:` on their own line still flag | Pass | 144 of 144 on HEAD (6 qualified headers x LF/CRLF x 12 endings), each flag quotes the whole sentence |
| Restoring `\s` makes the new tests fail | Pass, one row | Scratch copy of HEAD with the lexicon arm set back to `(?<=[a-z]\shistory)`: `pytest tests/unit/test_t133_lexicon.py -q -rfE` gives 3 failed, 91 passed, 2 skipped. The own-line LF row fails on behaviour. See F4 |
| Unit suite passes | Pass | `.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider -rs` on the HEAD archive: 3457 passed, 8 skipped, exit 0. The 8 skips are the git-backed parity tests (test_t133_lexicon.py:303, :322, :333), which need git objects; the card's 3464 from a clone is 7 more, which matches |
| Scope cut 13d reads correctly | Partly. The cut and its "never before T-133" premise are right; the `PMH:` clause is not (F1) | `memory/SCOPE_CUTS.md:84`; probes on e79c3aa^, e79c3aa and HEAD |

## Findings

**F1 (minor, new). Row 13d says `PMH:` still flags. A generic `PMH:` sentence never flagged on any build.**
`memory/SCOPE_CUTS.md:84` ends "PMH:/Hx:/'history of'/'Past ... history:' still flag." Probes on the parent e79c3aa^, the T-133 r1 build e79c3aa and HEAD: `PMH: significant for diabetes.` is quiet on all three. `PMH: significant for lumbar strain.` flags only through `pmh_psh_spine` (spine terms). `Hx:`, `history of`, and `Past history:` / `Past medical history:` do flag. The row's main claim is right: `History reviewed; significant for diabetes.` is quiet on e79c3aa^ and HEAD and flagged on e79c3aa.
Fix: change the tail of the row to say `PMH:` flags for spine terms only (`pmh_psh_spine`), and that `Hx:`, `history of` and `Past ... history:` still flag.

**F2 (minor, carried from r4 F2, second half still open). ASSUMPTIONS.md:24 says `patient reports history of` is pinned by the T-133 test file. No test line contains it.**
`git show HEAD:memory/ASSUMPTIONS.md | sed -n 24p` ends "pinned by tests/unit/test_t133_lexicon.py." `git show HEAD:tests/unit/test_t133_lexicon.py | grep -i -n "reports history"` prints nothing. `Patient reports history of neck pain.` flags through `history_of` on HEAD. The `per patient` half is true: the test file pins `History per patient: significant for lumbar strain.` at lines 261 and 290.
Fix (orchestrator-owned): name only the pinned forms on line 24, or add `Patient reports history of` as a test input.

**F3 (minor, carried from r2 F5, r3 F3 and r4 F3). Criterion 18: no live claude-cli report with 3-run metrics at or after the T-133 lexicon commits.**
The r4 statement that the live reports are all judge-controls was wrong: `evals/reports/20261102T120809Z.md` (backend `claude-cli`, determinism_3run 1.0, unsupported_count_3run 0) exists. But its source commit `63e18ed` is an ancestor of 6fa8ecc, so it predates the T-133 r3 and r4 lexicon changes. The lexicon-change report `evals/reports/20261102T124856Z.md` is backend `fixture`. The orchestrator deferred the live re-measure to the M2 run (card note 2026-11-02T13:01:01Z). This is minor because that run is the planned acceptance point. If the M2 gate does not cite a claude-cli report with numeric determinism_3run and unsupported_count_3run for a commit at or after 15be212, this becomes major.
Fix: run the live claude-cli eval on the current lexicon and cite its report path on T-133 before the M2 gate.

**F4 (nit, new). Only one of the four own-line rows kills a restored `\s`. The CRLF and blank-line rows cannot, and a CR-only row would.**
In the `\s` mutant run, the only failing own-line row is `test_a_bare_history_header_on_its_own_line_stays_quiet[Patient seen in clinic\nHistory: significant for neck pain.]` (test_t133_lexicon.py:355). The CRLF row (`Rear-ended at a light\r\nHistory - ...`) and the blank-line row pass under the mutant. This is by construction: the byte before `\n` is `\r` or `\n`, never a letter. The 6fa8ecc archive, which has the `\s` guard, flags `Neck pain\rHistory: significant for lumbar strain.`, a CR-only layout that no row covers.
Fix: add `Neck pain\rHistory: significant for lumbar strain.` to `OWN_LINE` (test_t133_lexicon.py:346).

**F5 (nit, carried from r4 F5). The mutant tests depend on the regex text, so a lexicon-level mutation fails at a precondition.**
`tests/unit/test_t133_lexicon.py:224` (`assert guard in pat`) and `:377` (`assert mpat != pat`). In my yaml-level mutant run, the `:371` test failed at `:377` because the mutated yaml had no `\s` text left to replace, not on a scan result.
Fix: build the mutant from the scan result or drop the text precondition, so a lexicon-only mutation is caught by behaviour.

## What is right

- A bare `History:` on its own line is quiet in 240 of 240 layouts on HEAD and 15be212, and the control archive fails exactly the letter-then-newline cases, so the probe discriminates.
- Qualified own-line headers (Past, Medical, Surgical, Past medical, Prior, Previous history:) flag with the full sentence in 144 of 144 layouts on HEAD.
- The 13d cut itself is right: the semicolon form flagged only in the T-133 r1 build e79c3aa, and the parent e79c3aa^ is quiet.

## Exercised

- `python3 tools/board.py show T-133`: status in_review, rounds 3, commits end with 15be212; `personas/staff-engineer.md` and `reviews/T-133-staff-engineer-r4.md` read in full.
- `git rev-parse HEAD` (330fc0c); `git show --stat 15be212` (lexicon.yaml and the test file); `git diff 6fa8ecc 15be212` on both files; `git diff --stat 15be212 HEAD` (only `reviews/GATE-M2-round1-triage.md`).
- `git archive HEAD` into scratchpad `T-133-r5-head`, `git archive 15be212` into `T-133-r5-15be212`, `git archive 6fa8ecc` into `T-133-r5-6fa8ecc`, `git archive e79c3aa^` into `T-133-r5-parent`, `git archive e79c3aa` into `T-133-r5-r1`. `sha256sum app/llm/lexicon.yaml` = fbefe801... in HEAD and 15be212. `diff -rq -x __pycache__` between HEAD and 15be212: identical apart from the GATE file.
- `.venv/bin/python -I T-133-r5-probe.py <archive>` on HEAD, 15be212 and 6fa8ecc: bare own-line 240 cases (240/240, 240/240, 234/240); qualified own-line 144 cases (144/144 on all three); same-line controls (`Chief complaint and history:`, `History:` at start, `Past history:`, `Neck pain history:`).
- Mutant: `T-133-r5-mut-backslash` (copy of HEAD archive; `(?<=[a-z][ \t]history)(?<!\band[ \t]history)` replaced by `(?<=[a-z]\shistory)(?<!\band\shistory)`, one occurrence asserted in Python). `.venv/bin/python -I -m pytest tests/unit/test_t133_lexicon.py -q -p no:cacheprovider -rfE`: 3 failed (own-line LF row; `:224` precondition; `:377` precondition), 91 passed, 2 skipped. Probe on the mutant: 234/240 quiet.
- Unit suite on the HEAD archive: `.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider -rs`: 3457 passed, 8 skipped, exit 0 (195 s). Log: `T-133-r5-unit-head.log` in scratchpad.
- 13d premise: `T-133-r5-13d.py` and `T-133-r5-pmh.py` on e79c3aa^, e79c3aa and HEAD (results in F1 and F2 above). `git show HEAD:memory/SCOPE_CUTS.md | grep -n "^| 13d"` (line 84).
- Eval records: `grep -l` of claude-cli report headers; per-file `Source commit` and 3-run rows for the report list; `git merge-base --is-ancestor 63e18ed 6fa8ecc` (true); `evals/reports/20261102T120809Z.md:3-4`.
- Not run: the live claude-cli backend (no LLM calls from the reviewer); the app at localhost:7860 (no UI change in scope); the parity tests from a clone (outside this brief); the sample CLI (outside this brief).
- Outside my lens: whether a pre_existing flag is clinically right; whether the model pass recovers these forms.

```json
{"card": "T-133", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 330fc0c (product tree identical to fix commit 15be212: app/llm/lexicon.yaml sha256 fbefe801..., tests/unit/test_t133_lexicon.py); memory/SCOPE_CUTS.md row 13d; memory/ASSUMPTIONS.md:24 (carried); eval report records for the lexicon change; archive-based (git-backed parity tests skip); no app URL (no server run)",
 "exercised": [
  "python3 tools/board.py show T-133 (status in_review, rounds 3, commits end at 15be212); personas/staff-engineer.md and reviews/T-133-staff-engineer-r4.md read in full",
  "git rev-parse HEAD (330fc0c); git show --stat 15be212; git diff 6fa8ecc 15be212 -- app/llm/lexicon.yaml tests/unit/test_t133_lexicon.py; git diff --stat 15be212 HEAD (only reviews/GATE-M2-round1-triage.md)",
  "git archive HEAD, 15be212, 6fa8ecc, e79c3aa^ and e79c3aa into scratchpad T-133-r5-*; sha256sum app/llm/lexicon.yaml fbefe801... in HEAD and 15be212; diff -rq -x __pycache__ HEAD vs 15be212 identical apart from the GATE file",
  "T-133-r5-probe.py (flags.lexicon_flags and lexicon_scan.scan) on HEAD, 15be212 and 6fa8ecc archives: bare own-line 240 cases, 240/240 quiet on HEAD and 15be212, 234/240 on 6fa8ecc; qualified own-line 144 cases, 144/144 flag with the full sentence on all three; same-line controls",
  "mutant T-133-r5-mut-backslash (HEAD archive copy, lexicon arm restored to (?<=[a-z]\\shistory)(?<!\\band\\shistory), one occurrence asserted): .venv/bin/python -I -m pytest tests/unit/test_t133_lexicon.py -q -p no:cacheprovider -rfE gives 3 failed, 91 passed, 2 skipped; probe on the mutant 234/240 quiet",
  "unit suite on HEAD archive: .venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider -rs gives 3457 passed, 8 skipped, exit 0 (195 s); 8 skips are the git-backed parity tests (test_t133_lexicon.py:303, :322, :333)",
  "T-133-r5-13d.py and T-133-r5-pmh.py on e79c3aa^, e79c3aa and HEAD: History reviewed; significant for diabetes quiet/flag/quiet; PMH: significant for diabetes quiet on all three; PMH: significant for lumbar strain flags via pmh_psh_spine; Hx: via hx_abbrev; history of via history_of; Past history: and Past medical history: via history_significant_for",
  "git show HEAD:memory/SCOPE_CUTS.md | grep -n '^| 13d' (line 84); git show HEAD:memory/ASSUMPTIONS.md | sed -n 24p; git show HEAD:tests/unit/test_t133_lexicon.py | grep -i -n 'reports history' (no output); per patient pinned at lines 261 and 290",
  "eval records: grep -l of backend claude-cli report headers; per-file Source commit and determinism_3run / unsupported_count_3run rows; git merge-base --is-ancestor 63e18ed 6fa8ecc (true); evals/reports/20261102T120809Z.md:3-4 (claude-cli, source 63e18ed); evals/reports/20261102T124856Z.md (fixture, lexicon-change report)",
  "Not run: live claude-cli backend (no LLM calls from the reviewer); app at localhost:7860 (no UI change in scope); parity tests from a clone; sample CLI (outside this brief). Outside my lens: clinical correctness of pre_existing flags; whether the model pass recovers these forms"
 ],
 "verdict": "pass",
 "scores": {"bare_own_line_header_quiet": 5, "qualified_own_line_headers_flag": 5, "mutant_killability": 4, "unit_suite": 5, "scope_cut_13d_accuracy": 4, "assumption_and_eval_records": 3},
 "findings": [
  {"severity": "minor",
   "title": "SCOPE_CUTS 13d says PMH: still flags; a generic PMH: sentence never flagged on any build",
   "evidence": "memory/SCOPE_CUTS.md:84: 'PMH:/Hx:/history of/Past ... history: still flag.' Probe (T-133-r5-pmh.py) on e79c3aa^, e79c3aa and HEAD: 'PMH: significant for diabetes.' => quiet on all three. 'PMH: significant for lumbar strain.' flags only via pmh_psh_spine. Hx:, history of, Past history: and Past medical history: flag on HEAD.",
   "why_it_matters": "The row is the decision record Chris must act on. Its main premise (the semicolon form flagged only in T-133 r1, never before) is correct, but the PMH: example describes behaviour that was never there, so the row overstates what the cut costs.",
   "fix": "Change the tail of row 13d to say PMH: flags for spine terms only (pmh_psh_spine), and that Hx:, history of and Past ... history: still flag.",
   "acceptance_test": "git show HEAD:memory/SCOPE_CUTS.md | sed -n 84p has no unqualified PMH: example; a python -I probe of 'PMH: significant for diabetes.' on HEAD is quiet, as the row says."},
  {"severity": "minor",
   "title": "ASSUMPTIONS.md:24 says patient reports history of is pinned by the T-133 test file; no test line contains it (carried from r4 F2)",
   "evidence": "git show HEAD:memory/ASSUMPTIONS.md | sed -n 24p ends 'pinned by tests/unit/test_t133_lexicon.py.' git show HEAD:tests/unit/test_t133_lexicon.py | grep -i -n 'reports history' prints nothing. Patient reports history of neck pain. flags via history_of on HEAD. The per-patient half is pinned at test_t133_lexicon.py:261 and :290.",
   "why_it_matters": "An assumption record claims a test pin that does not exist. The per-patient half is true, so the record is half right. Not changed by 15be212.",
   "fix": "Orchestrator edits memory/ASSUMPTIONS.md:24 to name only the pinned forms (per patient, obtained from patient), or adds Patient reports history of as a test input.",
   "acceptance_test": "Every phrase named on memory/ASSUMPTIONS.md:24 appears as a test input in tests/unit/test_t133_lexicon.py (grep -i)."},
  {"severity": "minor",
   "title": "Criterion 18: no live claude-cli 3-run report at or after the T-133 lexicon commits (carried from r2 F5, r3 F3, r4 F3; deferred to M2)",
   "evidence": "evals/reports/20261102T120809Z.md:3-4 is backend claude-cli with determinism_3run 1.0 and unsupported_count_3run 0, but its source commit 63e18ed is an ancestor of 6fa8ecc (git merge-base --is-ancestor 63e18ed 6fa8ecc: true), so it predates the T-133 r3 and r4 lexicon changes. evals/reports/20261102T124856Z.md is backend fixture. Card T-133 note 2026-11-02T13:01:01Z: 'Live eval rides with the M2 confirming run.' The r4 statement that the only claude-cli reports are judge controls was wrong; the conclusion (no 3-run measurement on the lexicon commits) stands.",
   "why_it_matters": "Criterion 18 asks for a re-run eval report path for a lexicon change. The live determinism and unsupported-count numbers for the current lexicon are not measured. This is minor because the M2 run is the planned acceptance point; if the M2 gate does not cite such a report, it becomes major.",
   "fix": "Run the live claude-cli eval on the current lexicon and cite its report path on T-133 before the M2 gate.",
   "acceptance_test": "An evals/reports/ file with backend claude-cli, numeric determinism_3run and unsupported_count_3run, a source commit at or after 15be212, cited on the T-133 card."},
  {"severity": "nit",
   "title": "Only one own-line row kills a restored \\s; the CRLF and blank-line rows cannot, and no CR-only row exists",
   "evidence": "Mutant run (T-133-r5-mut-backslash): the only failing own-line row is test_a_bare_history_header_on_its_own_line_stays_quiet[Patient seen in clinic\\nHistory: significant for neck pain.] (tests/unit/test_t133_lexicon.py:355). The CRLF row and the blank-line row pass under the mutant. The 6fa8ecc archive (same guard) flags 'Neck pain\\rHistory: significant for lumbar strain.' (T-133-r5-probe.py), a CR-only layout no row covers.",
   "why_it_matters": "The brief's LF, CRLF and blank-line set is met. But the CRLF and blank-line rows cannot detect the \\s regression by construction, so the kill rests on one row. A CR-only row would be a second kill and covers a line ending the suite does not name.",
   "fix": "Add 'Neck pain\\rHistory: significant for lumbar strain.' to OWN_LINE (tests/unit/test_t133_lexicon.py:346).",
   "acceptance_test": "With the \\s arm restored, the new CR-only row fails; on HEAD it passes."},
  {"severity": "nit",
   "title": "The mutant tests depend on the regex text, so a lexicon-level mutation fails at a precondition (carried from r4 F5)",
   "evidence": "tests/unit/test_t133_lexicon.py:224 (assert guard in pat) and :377 (assert mpat != pat). In the yaml-level mutant run the test at :371 failed at :377 because the mutated yaml had no \\s text left to replace, not on a scan result.",
   "why_it_matters": "A reworded guard fails these tests for a reason that is not the behaviour they pin (checklist 13).",
   "fix": "Build the mutant from the scan result, or drop the text precondition, so a lexicon-only mutation is caught on behaviour.",
   "acceptance_test": "A lexicon-only mutation that restores the \\s arm fails the own-line quiet test on its scan assertion, with no precondition failure."}
 ],
 "whats_right": [
  "A bare History: on its own line is quiet in 240 of 240 layouts on HEAD and 15be212 (12 previous-line endings x LF, CRLF, blank line, CR-only x 4 header forms); the 6fa8ecc control fails exactly the letter-then-newline cases, so the probe discriminates.",
  "Qualified own-line headers (Past, Medical, Surgical, Past medical, Prior, Previous history:) flag with the full sentence in 144 of 144 layouts on HEAD.",
  "The 13d cut is right: the semicolon form flagged only in the T-133 r1 build e79c3aa; the parent e79c3aa^ is quiet on it."
 ],
 "questions_for_chris": []}
```
