# T-133 r4 review (staff-engineer-reviewer), final round: qualified history headers, bare headers, parent comparison

Pinned to HEAD 128942d. In scope: 6fa8ecc (lexicon r3 header guard and tests, the lexicon blob is sha256 c0178e30...), f3ac48f (calibration report) and 128942d (memory/SCOPE_CUTS.md and memory/ASSUMPTIONS.md). Reviewed from `git archive HEAD` (scratchpad T-133-r4-archive-head) and from a clean clone at 128942d (scratchpad T133-r4-clone), because the parent-comparison tests need git objects. The main tree was not edited.

Verdict: **changes**. No blocker. One major, three minors, two nits. The r3 F1 request (qualified headers flag again) is met. The r3 fix brought a new over-flag for a bare History: header on its own line (a regression of r2 F1), and two memory records misstate the scope cut and the assumption pin.

## Brief checks

| Check | Result | Evidence |
|---|---|---|
| 'Past history:', 'Medical history:', 'Surgical history:', 'Past medical history:' flag again, full sentence | Pass | probe_r4.py REQ-POS: `FLAG  'Past medical history: significant for diabetes.' => ['Past medical history: significant for diabetes.']`; the other three are the same shape |
| Bare 'History:' header and HPI probes stay quiet | Partial. Same-line forms pass. A bare header on its own line flags when the line above ends in a letter (F1) | probe_r4.py REQ-QUIET 9 of 9 quiet; NEW-EDGE `Neck pain\nHistory: significant for lumbar strain.` FLAG on HEAD, quiet on 4065ef2 |
| Parity tests load the parent lexicons from git | Pass in a clone. Skip in an archive, by design (F4) | clone: `pytest tests/unit/test_t133_lexicon.py -k "parent or against_r1" -v` => 2 passed; archive: `SKIPPED ... test_t133_lexicon.py:303: git object e79c3aa^ not available` |
| Only the intended flags are lost | Pass | diff_parent_r1.py over 742 sentences: vs e79c3aa^ lost only 'Patient denying prior neck injury.'; vs e79c3aa lost 18 sentences, all HPI, a bare History: header, or the pinned semicolon form |
| 13d scope cut and patient-as-source assumption recorded | Recorded. The 13d premise and the ASSUMPTIONS pin claim are wrong (F2) | memory/SCOPE_CUTS.md:84; memory/ASSUMPTIONS.md:24 |
| Unit suite passes | Pass | archive `.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider`: 3444 passed, 8 skipped, exit 0. Clone 128942d with -rs: 3451 passed, 1 skipped, exit 0, which matches the card's 6fa8ecc count |

## Probe output (flags.lexicon_flags, HEAD; 4065ef2 result in brackets)

- `FLAG  'Neck pain\nHistory: significant for lumbar strain.' => ['History: significant for lumbar strain.']` [quiet]
- `FLAG  'CHIEF COMPLAINT: Neck pain\nHISTORY: notable for stiffness and headache.' => ['HISTORY: notable for stiffness and headache.']` [quiet]
- `FLAG  'Chief complaint: neck pain\nHistory: notable for neck pain.' => ['History: notable for neck pain.']` [quiet]
- `FLAG  'Neck pain history: notable for lumbar strain.' => ['Neck pain history: notable for lumbar strain.']` [quiet]
- `quiet 'Neck pain\n\nHistory: notable for lumbar strain.' => []` (blank line: quiet on both)
- `quiet 'Past history:\nsignificant for lumbar strain.' => []` (condition on the next line: quiet on both, not a regression; F6)

## Mutants (scratch copies of the HEAD archive, not committed)

| Mutant | Result |
|---|---|
| M1: f939ccb guard restored (qualified exemption removed) | 7 failed, 80 passed, 2 skipped |
| M3: only the 'and history' exclusion removed | 3 failed (2 on behaviour, 1 at the pattern-text precondition, :224) |
| Line-start arm of the header guard (F1) | No test fails when it is wrong: the HEAD suite is green with the F1 defect |

## Findings

**F1 (major). A bare 'History:' header on its own line flags pre_existing when the line above ends in a letter. This is a regression of r2 F1 introduced in 6fa8ecc.**
The guard at app/llm/lexicon.yaml:187 has an arm `(?<=[a-z]\shistory)`. Its `\s` matches a newline, and scan() compiles the pattern with re.I|re.M on the raw text (app/backend/lexicon_scan.py:112). So a letter, a newline, then "History:" takes the first arm and skips the colon guard. The comment at app/llm/lexicon.yaml:180-185 promises the bare header is quiet at "line or sentence start". The layouts in the table above are all new in r4. Parity and quiet corpora (`_corpus` at tests/unit/test_t133_lexicon.py:273, `R3_HPI` at :231) have no line-separated layout. Fix: a closed qualifier list (past, medical, surgical, prior, previous) with a space or tab class in place of `\s`, and keep `(?!\s*[:\-])` for every other history word. Acceptance test in the JSON below.

**F2 (minor). Two memory records overstate.** memory/SCOPE_CUTS.md:84, row 13d, says the semicolon form "flagged before T-133". The parent e79c3aa^ does not flag it (`quiet 'History reviewed; significant for diabetes.' => []`). It flagged only in the first T-133 build e79c3aa (`FLAG ['History reviewed;']`). memory/ASSUMPTIONS.md:24 says "patient reports history of" is pinned by tests/unit/test_t133_lexicon.py. That phrase flags through the history_of entry (app/llm/lexicon.yaml:125-126), and no test line names it. Chris is asked to decide 13d on a false premise. Orchestrator-owned files, so I only report it.

**F3 (minor, carried from r2 F5 and r3 F3). The live claude-cli eval for the lexicon change is still owed.** The newest claude-cli report, evals/reports/controls-20261102T123937Z.md:1-4, is a judge-controls report at bea3984 with no determinism_3run or unsupported_count_3run. The lexicon-change report evals/reports/20261102T124856Z.md:3-6 is `backend fixture`. Criterion 18 is met by path only.

**F4 (minor). The parity and corpus checks cannot see the line-separated layout, and the git-backed guards skip in any export.** The parity tests at tests/unit/test_t133_lexicon.py:322 and :333 compare only against e79c3aa^ and e79c3aa. They cannot see a gain of flags over r2, which is what F1 is. In an archive both skip (:303). In a clone they pass (`2 passed, 87 deselected`).

**F5 (nit). The guard mutant tests assert the regex text.** tests/unit/test_t133_lexicon.py:174 and :224. Under M3 the test at :224 fails at its precondition, not on behaviour.

**F6 (nit). A qualified header with the condition on the next line stays quiet.** Not a regression: the same on 4065ef2. The condition search `[^.;\n]` at app/llm/lexicon.yaml:187 does not cross a line break. Record it as an accepted miss.

## What is right

- Qualified headers flag again with the full sentence: Past, Medical, Surgical, Past medical, Prior and Previous history each give one pre_existing flag quoting the whole sentence on HEAD.
- The parity tests load the lexicons from git and hold in a clone (89 passed, 0 skipped). The only prior-condition loss vs the parent is the intended denial.
- M1 fails 7 tests. The deny, wife, diabetes and prior-assault forms still flag. The sample CLI output is identical across two runs.

## Exercised

- `python3 tools/board.py show T-133`; personas/staff-engineer.md and reviews/T-133-staff-engineer-r3.md read in full.
- `git log --oneline -8`; `git show --stat 6fa8ecc f3ac48f 128942d`; `git show 6fa8ecc -- app/llm/lexicon.yaml`.
- `git archive HEAD` into scratchpad T-133-r4-archive-head; sha256 of app/llm/lexicon.yaml equals `git show HEAD:app/llm/lexicon.yaml`.
- A clean clone of the repo at 128942d in scratchpad T133-r4-clone; `git archive` of 4065ef2, e79c3aa and e79c3aa^ into scratchpad.
- Unit suite: archive 3444 passed, 8 skipped, exit 0; clone 3451 passed, 1 skipped, exit 0. T-133 file: archive 87 passed, 2 skipped; clone 89 passed; `-k "parent or against_r1"` 2 passed.
- probe_r4.py, probe_r4b.py, probe_r4c.py (flags.lexicon_flags) on HEAD, 4065ef2, e79c3aa and e79c3aa^ archives; diff_parent_r1.py on the clone (742-sentence corpus).
- Mutants M1 and M3 on scratch copies of the HEAD archive.
- Sample CLI: `LLM_BACKEND=fixture` runpy of app.pipeline evals/golden/sample.txt on the HEAD archive, twice: identical output (`$2,150 (charge) record 8 [verified]`, `Charges detected, pending review (not a total): $8,390.00`).
- git grep for history headers in HEAD evals/golden and spec: no match.
- `grep -l 'backend `claude-cli`' evals/reports/*.md`; heads of evals/reports/controls-20261102T123937Z.md and 20261102T124856Z.md; grep for determinism_3run and unsupported_count_3run in the controls report: no match.
- memory/SCOPE_CUTS.md row 13d and memory/ASSUMPTIONS.md:24 read at HEAD; grep of the test file for "history of" and "Patient reports".
- Not run: the live claude-cli backend (no LLM calls from the reviewer); the app server at localhost:7860 (no UI change in scope). Outside my lens: whether a pre_existing flag is clinically right, and whether the model pass recovers these forms.

## Machine-readable record

```json
{"card": "T-133", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 128942d: lexicon change 6fa8ecc (T-133 r3 header guard; lexicon sha256 c0178e30...), tests/unit/test_t133_lexicon.py, f3ac48f (calibration report), 128942d (memory/SCOPE_CUTS.md, memory/ASSUMPTIONS.md); lexicon-only, no app URL (no server run); HEAD also contains other cards' commits (out of scope)",
 "exercised": [
  "python3 tools/board.py show T-133 (card, notes and handoff read); reviews/T-133-staff-engineer-r3.md read in full; personas/staff-engineer.md read in full",
  "git log --oneline -8; git show --stat 6fa8ecc f3ac48f 128942d; git show 6fa8ecc -- app/llm/lexicon.yaml (r3 diff read)",
  "git archive HEAD | tar -x into scratchpad T-133-r4-archive-head; sha256 of app/llm/lexicon.yaml equals git show HEAD:app/llm/lexicon.yaml (c0178e30...)",
  "git clone of the repo into scratchpad T133-r4-clone, checkout 128942d (clean) so the git-backed parent tests can run; git archive of 4065ef2, e79c3aa and e79c3aa^ into scratchpad",
  ".venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider on the HEAD archive: 3444 passed, 8 skipped, exit 0 (183.75s); on the clone at 128942d with -rs: 3451 passed, 1 skipped, exit 0 (274.24s)",
  "pytest tests/unit/test_t133_lexicon.py: archive 87 passed, 2 skipped (both git-backed parity tests skip with 'git object e79c3aa^ not available'); clone 89 passed; clone -k 'parent or against_r1' -v: 2 passed",
  "probe_r4.py (flags.lexicon_flags): 11 qualified and positive sentences, 9 bare-header and HPI sentences, 12 line/whitespace variants on HEAD, 4065ef2 (r2) and e79c3aa (r1) archives",
  "probe_r4b.py: 10 extra forms (History reviewed; Hx:, PMH:, history of, uppercase headers, History:\\nnewline, per patient, obtained from patient) on e79c3aa^, e79c3aa, 4065ef2 and HEAD",
  "probe_r4c.py: multi-line realistic layouts (CHIEF COMPLAINT / HISTORY on separate lines, Past history: with the condition on the next line) on HEAD and 4065ef2",
  "diff_parent_r1.py on the clone: prior-condition flags over the test module's _corpus (742 sentences), HEAD vs e79c3aa^ (lost: only 'Patient denying prior neck injury.') and HEAD vs e79c3aa (lost: 18 sentences, all HPI, bare History: header or the pinned semicolon form)",
  "mutants on scratch copies of the HEAD archive (mutate.py): M1 restore the f939ccb guard -> 7 failed, 80 passed, 2 skipped; M3 drop only the 'and history' exclusion -> 3 failed (one of them at the 'assert guard in pat' precondition, tests/unit/test_t133_lexicon.py:224)",
  "sample CLI: LLM_BACKEND=fixture python -I runpy app.pipeline evals/golden/sample.txt on the HEAD archive, twice: identical output (Status line, '$2,150 (charge) record 8 [verified]', 'Charges detected, pending review (not a total): $8,390.00')",
  "git grep -n -i -E history-header pattern on HEAD evals/golden and spec: no match (the golden and spec text contain no bare or qualified history header)",
  "grep -l backend claude-cli evals/reports/*.md; head of evals/reports/controls-20261102T123937Z.md and 20261102T124856Z.md; grep determinism_3run and unsupported_count_3run in the controls report: no match",
  "memory/SCOPE_CUTS.md row 13d and memory/ASSUMPTIONS.md line 24 read at HEAD; grep of tests/unit/test_t133_lexicon.py for 'history of' and 'Patient reports': no pinning test line",
  "Not run: live claude-cli backend (no LLM calls from the reviewer); app server at localhost:7860 (no UI change in scope). Outside my lens: whether a pre_existing flag is clinically right; whether the model pass recovers these forms"
 ],
 "verdict": "changes",
 "scores": {"deterministic_no_llm": 5, "deny_forms_grounded_and_sourced": 5, "qualified_past_history_flags": 5, "bare_header_and_hpi_quiet": 2, "parent_and_r1_diff_only_intended": 4, "mutation_killability": 4, "scope_cut_and_assumption_records": 3, "eval_evidence_criterion_18": 3},
 "findings": [
  {"severity": "major",
   "title": "Bare 'History:' header at line start flags pre_existing when the line above ends in a letter (r2 F1 regression in 6fa8ecc)",
   "evidence": "probe_r4.py on the HEAD archive: 'Neck pain\\nHistory: significant for lumbar strain.' => FLAG ['History: significant for lumbar strain.'] ; 'CHIEF COMPLAINT: Neck pain\\nHISTORY: notable for stiffness and headache.' => FLAG ['HISTORY: notable for stiffness and headache.'] ; 'Chief complaint: neck pain\\nHistory: notable for neck pain.' => FLAG ['History: notable for neck pain.'] ; 'Neck pain history: notable for lumbar strain.' => FLAG. The same three inputs are quiet on the 4065ef2 (r2) archive. Cause: app/llm/lexicon.yaml:187 guard '(?:(?<=[a-z]\\shistory)(?<!\\band\\shistory)|(?!\\s*[:\\-]))'. The first arm is satisfied by a letter then any whitespace, and \\s matches a newline; the pattern is compiled with re.I|re.M on the raw text (app/backend/lexicon_scan.py:112). The comment at app/llm/lexicon.yaml:180-185 says the bare header is quiet at 'line or sentence start'. Nothing in tests/unit/test_t133_lexicon.py covers a line-separated layout (_corpus at line 273 and R3_HPI at line 231 have none).",
   "why_it_matters": "r2 F1 (major) asked that bare History: HPI text not raise pre_existing. The r3 fix holds only for same-line text. Line-separated notes are the usual chart layout, so the over-flag returns there, and it quotes HPI text as a prior condition. The record text is not changed and no fact is invented, so this is major and not blocker, the same rating r2 F1 got. The sample golden and spec have no history header, so the eval does not see it.",
   "fix": "(a) In the first arm, replace the \\s with a space or tab class. (b) Replace 'any word before history' with a closed qualifier list, for example (?<=\\b(?:past|medical|surgical|prior|previous)[ \\t])history with re.I (past medical is covered by the medical arm); then the 'and' exclusion is no longer needed. Keep (?!\\s*[:\\-]) for every other history word. Update the comment at app/llm/lexicon.yaml:180-185 to match the regex. Whether 'Neck pain history:' and 'Stiffness or history:' should flag is question 1 for Chris; the closed list makes both quiet.",
   "acceptance_test": "In tests/unit/test_t133_lexicon.py add to the quiet list, checked with lexicon_scan.scan and flags.lexicon_flags: 'Neck pain\\nHistory: significant for lumbar strain.', 'CHIEF COMPLAINT: Neck pain\\nHISTORY: notable for stiffness and headache.', 'Chief complaint: neck pain\\nHistory: notable for neck pain.' (and 'Stiffness or history: notable for neck pain.' if the closed list is adopted). The four QUALIFIED sentences still flag with the full sentence. A mutant with the old \\s arm (?<=[a-z]\\shistory) makes the new test fail. probe_r4.py NEW-EDGE group: every line-start and same-line bare-header form quiet."},
  {"severity": "minor",
   "title": "Two memory records overstate: scope cut 13d says the semicolon form 'flagged before T-133'; the ASSUMPTIONS line says 'patient reports history of' is pinned",
   "evidence": "memory/SCOPE_CUTS.md:84 row 13d: '(it flagged before T-133)'. Parent archive e79c3aa^ (probe_r4b.py): quiet 'History reviewed; significant for diabetes.' => []. The form flagged only in the first T-133 build e79c3aa: FLAG ['History reviewed;']. memory/ASSUMPTIONS.md:24 says 'patient reports history of' is 'pinned by tests/unit/test_t133_lexicon.py'. 'Patient reports history of neck pain.' flags on every build through the history_of entry (app/llm/lexicon.yaml:126), not through history_significant_for, and grep of tests/unit/test_t133_lexicon.py finds no test line that names it.",
   "why_it_matters": "Chris is asked to decide 13d on a premise that is false: the loss is relative to the T-133 r1 build, not to the product before T-133. The assumption record claims a pin that does not exist.",
   "fix": "Orchestrator edits memory (not my path): row 13d to say 'flagged in the T-133 r1 build (e79c3aa), not before T-133'; the ASSUMPTIONS line to name the pinned forms ('per patient', 'obtained from patient') or to pin 'Patient reports history of' in the test file.",
   "acceptance_test": "git show HEAD:memory/SCOPE_CUTS.md shows no 'before T-133' in row 13d; every phrase the ASSUMPTIONS line names appears as a test input in tests/unit/test_t133_lexicon.py."},
  {"severity": "minor",
   "title": "Live claude-cli eval for the lexicon change still owed (r2 F5 and r3 F3 still open)",
   "evidence": "grep -l backend `claude-cli` evals/reports/*.md lists only controls-*.md reports. The newest, evals/reports/controls-20261102T123937Z.md:1-4, is 'Judge controls ... backend `claude-cli` ... Source commit `bea39845...`' and has no determinism_3run or unsupported_count_3run (grep empty). The lexicon-change report evals/reports/20261102T124856Z.md:3-6 is 'backend `fixture`' and says determinism_3run and unsupported_count_3run need a live backend.",
   "why_it_matters": "Criterion 18 asks for a re-run eval report for a lexicon change. The path exists, but the live determinism and unsupported-count numbers are not measured, and the judge-controls report does not cover them.",
   "fix": "Run the live claude-cli eval on the commit that carries the F1 fix and cite its report path on the card before the M3 gate.",
   "acceptance_test": "A report under evals/reports/ has backend claude-cli, numeric determinism_3run and unsupported_count_3run, a source commit at or after 6fa8ecc, and the card cites it."},
  {"severity": "minor",
   "title": "The parity and corpus tests cannot see the line-separated layout and compare only against the parent and r1; the git-backed guards skip in any export",
   "evidence": "tests/unit/test_t133_lexicon.py:273 _corpus (742 sentences) and :231 R3_HPI hold no line-separated history header. The parity tests at :322 and :333 compare only with e79c3aa^ and e79c3aa. In the git archive copy both skip: 'SKIPPED [1] tests/unit/test_t133_lexicon.py:303: git object e79c3aa^ not available (archive or shallow clone)'. In the clone at 128942d they run: pytest -k 'parent or against_r1' -v => 2 passed, 87 deselected.",
   "why_it_matters": "F1 is a gain of flags over r2, and the parity design checks losses against the parent and r1, so it cannot see a gain. The archive run silently drops both git-backed guards. The parity result is real only when the suite runs from a clone.",
   "fix": "Add the F1 layout sentences to R3_HPI (the quiet list) so the quiet test covers them. Say in the test module docstring that the parity tests skip in an export and must run from a clone for review.",
   "acceptance_test": "With the F1 fix reverted locally, the new R3_HPI quiet test fails. The docstring names the export skip. Clone run of tests/unit/test_t133_lexicon.py: 89 passed, 0 skipped."},
  {"severity": "nit",
   "title": "Guard mutant tests assert the regex text, so a mutant fails at a precondition rather than on behaviour",
   "evidence": "tests/unit/test_t133_lexicon.py:174 assert r'(?!\\s*[:\\-])' in pat; :224 assert guard in pat. Mutant M3 (only the 'and history' exclusion dropped, from the HEAD archive) gives 3 failed: the two HPI tests on 'Chief complaint and history: notable for neck pain.' (behaviour) and test_without_the_qualifier_exemption_the_qualified_headers_lose_the_flag, which fails at :224 before any scan.",
   "why_it_matters": "A reworded guard would fail these tests for a reason that is not the behaviour they are meant to pin, which is the 'assert behaviour, not implementation' rule (checklist 13).",
   "fix": "Build the mutant pattern and assert the scan result only; drop the text precondition or keep it as a second check.",
   "acceptance_test": "M3 is killed by a scan assertion on 'Chief complaint and history: notable for neck pain.' alone, with no pattern-text assertion."},
  {"severity": "nit",
   "title": "A qualified header with the condition on the next line stays quiet (not a regression)",
   "evidence": "probe_r4c.py: 'Past history:\\nsignificant for lumbar strain.' => quiet on HEAD and on 4065ef2. The condition search in app/llm/lexicon.yaml:187 is [^.;\\n] and cannot cross the newline.",
   "why_it_matters": "The qualified-header AC is met for same-line text only. It is the same limit the other history entries have, so it is a documented miss, not a defect.",
   "fix": "Record it as an accepted miss in the entry's miss list or in SCOPE_CUTS, or state the single-line limit in the comment.",
   "acceptance_test": "The entry comment or SCOPE_CUTS names the form, and no test claims the qualified header flags across a line break."}
 ],
 "whats_right": [
  "Qualified headers flag again with the full sentence: Past history, Medical history, Surgical history, Past medical history, Prior history and Previous history all give one pre_existing flag quoting the whole sentence on HEAD (probe_r4.py REQ-POS).",
  "The parent and r1 comparisons load the lexicons from git and hold: in a clone all 89 T-133 tests pass, and the only prior-condition loss vs the parent is the intended 'Patient denying prior neck injury.' (diff_parent_r1.py).",
  "The mutant M1 (the f939ccb guard restored) fails 7 tests, and the deny, wife, diabetes and prior-assault forms still flag; the sample CLI output is identical across two runs."
 ],
 "questions_for_chris": [
  "Should only the closed list (past, medical, surgical, prior, previous) make a history word a past-history header? Under that rule 'Neck pain history:' and 'Stiffness or history:' stay quiet; under the current rule they flag. The F1 fix assumes the closed list.",
  "Is the patient-as-source decision (memory/ASSUMPTIONS.md:24, r3 F4) accepted as the product decision, so that 'History obtained from patient, notable for neck pain.' keeps flagging?"
 ]}
```
