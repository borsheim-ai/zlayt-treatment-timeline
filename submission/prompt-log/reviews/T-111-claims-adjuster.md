# T-111 review: claims-adjuster-reviewer

Commit under review: 99c2b32 (D-043 single-clause "Waddell testing not performed/done." and "Not tested." stay silent). Baseline: parent 8c190e8.
Reviewed from `git archive`, not the dirty working tree (other files have uncommitted edits).

**Verdict: changes** (0 blockers, 1 major, 2 minor, 1 nit).

**What holds.** The four requested forms are silent at HEAD. Every second-clause, contrast, side-qualifier and extra-word variant I tried still flags, and the excerpt is the whole sentence, verbatim. Full unit suite is green with no regression.

**What does not.** The allow-list is not the cause of the main gap. Waddell-term recall predates this commit: a positive count with no Waddell word ("3/5 positive") and a reversed "Positive Waddell" never flag. The parent gave the not-performed sentence a flag in the two-sentence pairs; T-111 removes it, so those pairs now show nothing. That is the adjuster-facing exposure, and it is why finding 1 is major.

**Why major, not blocker.** D-043 triggers on a credibility term. These sentences contain none, so no literal line of D-043 is broken. If Chris rules a bare count is in scope, re-rate to blocker (question 1).

**Outside my lens:** the commit trailer model name (the handoff asks the orchestrator to confirm it).

**Scratch evidence (absolute paths):** `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t111-archive` (HEAD 99c2b32) and `.../scratchpad/t111-parent` (8c190e8). Probe script: `artifacts/review-evidence/T-111-probe.py`, run with `python -I` against both trees.

## Probe results (HEAD 99c2b32 vs parent 8c190e8)

| Probe | Text | HEAD | Parent |
|---|---|---|---|
| P01 | Waddell testing not performed. | SILENT | FLAG |
| P02 | Waddell testing not done. | SILENT | FLAG |
| P03 | Waddell testing not performed; 3/5 positive. | FLAG (whole) | FLAG (whole) |
| P04 | Waddell not done but effort inconsistent. | FLAG (whole) | FLAG (whole) |
| P05 | Waddell signs not tested. | SILENT | SILENT |
| P06 | Not tested. | SILENT | SILENT |
| P07 | Waddell testing not performed, but pain persisted. | FLAG (whole) | FLAG (whole) |
| P08 | Waddell testing not performed on the left. | FLAG (whole) | FLAG (whole) |
| P09 | Waddell testing not performed. Symptom magnification noted. | only 2nd sentence | both sentences |
| P10 | Waddell testing not performed\nstraight leg raise positive. | FLAG (whole) | FLAG (whole) |
| X17 | Waddell testing not performed. 3/5 positive. | SILENT | only 1st sentence |
| Y06 | Waddell testing not performed. Positive Waddell. | SILENT | only 1st sentence |
| X12 | "Waddell testing not performed." (quoted) | FLAG | FLAG |
| X18 | Waddell-testing not performed; straight leg raise positive. | SILENT | SILENT |
| X19 | Waddell-signs positive. | SILENT | SILENT |

The remaining X and Y probes are in the probe script output. All second-clause, contrast and side variants (X03-X10, X22, X25) flag with the whole sentence as excerpt.

## Findings

1. **major, Positive Waddell count after a not-performed sentence now yields no flag.** Pre-existing recall gap, exposed by the silence. See the JSON below.
2. **minor, quoted or bracketed single-clause forms flag.** The sentence splitter treats a closing quote or bracket as a terminator, but the clean check does not strip it.
3. **minor, hyphenated Waddell is not recognized.** Pre-existing at 8c190e8.
4. **nit, "Not tested." allow-list entry is inert.** The output is correct, but the pin proves nothing about the allow-list.

```json
{"card": "T-111", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 99c2b32 (app/backend/credibility.py, tests/unit/test_flags_pass.py) via git archive; parent 8c190e8 as baseline; unit-level, no app URL; sample golden lib12 (evals/library_build_v2.py) referenced",
 "exercised": [
   "Read personas/claims-adjuster.md in full; read my memory index and the lexicon-method, T-092 and T-067 allow-list memory files",
   "Read memory/ORCHESTRATOR_DECISIONS.md D-043 (line 51); ran board.py show T-111",
   "git rev-parse HEAD -> 99c2b32a4fdfec66a90ceb5c0da4ad570f594785; git rev-parse 99c2b32^ -> 8c190e82e0a3234f0025afef3e7c3ac75d1afe34",
   "git show --stat 99c2b32; git show 99c2b32 -- app/backend/credibility.py tests/unit/test_flags_pass.py",
   "git archive 99c2b32 and git archive 8c190e8 extracted to scratchpad t111-archive and t111-parent (working tree has uncommitted edits, so the commit was reviewed, not the tree)",
   ".venv/bin/python -m pytest -q tests/unit/test_flags_pass.py on t111-archive -> '34 passed in 0.79s'",
   ".venv/bin/python -m pytest -q tests/unit on t111-archive -> '2238 passed, 4 skipped in 155.63s'; on t111-parent -> '2236 passed, 4 skipped in 158.76s'",
   "artifacts/review-evidence/T-111-probe.py run with python -I against both trees: 10 requested probes (P01-P10), 27 adversarial (X01-X27), 7 subject-variant probes (Y01-Y07), production run_flag_pass path",
   "Read app/backend/credibility.py lines 1-75; tests/unit/test_flags_pass.py lines 188-190 and 290-325; app/llm/lexicon.yaml Waddell entry (around lines 1160-1172); evals/library_build_v2.py lines 391-457; evals/library/case_lib12_records_review_credibility.txt"
 ],
 "verdict": "changes",
 "scores": {"d043_single_clause_silence": 4, "second_clause_contrast_side_still_flags": 5, "excerpt_verbatim_whole_sentence": 5, "waddell_term_recall": 2, "no_regression_full_unit": 5},
 "findings": [
  {"severity": "major",
   "title": "Positive Waddell count after a not-performed sentence now produces no flag (recall gap, pre-existing at 8c190e8; exposed by the T-111 silence)",
   "evidence": "Probe artifacts/review-evidence/T-111-probe.py. HEAD 99c2b32: 'Waddell testing not performed. 3/5 positive.' -> SILENT; 'Waddell testing not performed. Positive Waddell.' -> SILENT. Parent 8c190e8, same two texts -> FLAG-PART, excerpts ['Waddell testing not performed.'] (only the first sentence). 'Waddell not performed; 3/5 positive.' and '3/5 positive.' are SILENT on both trees. app/backend/credibility.py:12-13 (_WADDELL) has no alternative matching a bare N/5 positive or Positive Waddell. Golden lib12 (evals/library_build_v2.py:403) uses only the 'Waddell 3/5 positive' form, so the eval cannot see the gap.",
   "why_it_matters": "D-043 says a missed flag costs credibility at the adjuster. The positive count is the Waddell result an adjuster would argue. In these pairs the not-performed sentence was the only flag the parent gave, and T-111 removes it, so the pair now carries no flag. Rated major, not blocker: D-043 triggers on a credibility term and these sentences contain none, so no literal D-043 line is broken, and the gap predates this commit. If Chris rules that a bare count or reversed Positive Waddell is a D-043 trigger, re-rate to blocker under my section 5 (a silently omitted weakness).",
   "fix": "Either add these forms to the trigger set (bare N/5 positive and positive Waddell, in credibility.py and in app/llm/lexicon.yaml, which the researcher owns), or record in SCOPE_CUTS that they are not covered and why. Do not leave the pair silent without a recorded decision.",
   "acceptance_test": "Probe 'Waddell testing not performed. Positive Waddell.' flags exactly one sentence with excerpt 'Positive Waddell.' and the first sentence stays silent. If Chris adds bare counts, 'Waddell testing not performed. 3/5 positive.' flags the second sentence. Both pinned in tests/unit/test_flags_pass.py beside test_t111_single_clause_not_performed_or_not_done_is_silent (line 302)."},
  {"severity": "minor",
   "title": "Quoted or bracketed single-clause not-performed form flags (over-flag direction)",
   "evidence": "Probe X12 on HEAD: the quoted form 'Waddell testing not performed.' with curly double quotes around it -> FLAG. X13 '(Waddell testing not performed.)' -> FLAG. Unquoted P01 -> SILENT. app/backend/credibility.py:39 _END accepts a closing quote or bracket as a sentence terminator, but app/backend/credibility.py:43 _clean_negation strips only '.!? ', so the same single clause is not clean.",
   "why_it_matters": "D-043 says trailing punctuation varies and single-clause forms stay silent. A quoted single clause is still one clause. The direction is fail-toward-flag, so the cost is one extra paralegal click, not a missed flag. The splitter and the clean check disagree on what ends a sentence.",
   "fix": "In the normalizer at credibility.py:43, strip closing quote and bracket characters (the same set as _END) before the clean match, and pin it.",
   "acceptance_test": "The quoted and bracketed forms of 'Waddell testing not performed.' return [] from run_flag_pass; both are added to test_t111_single_clause_not_performed_or_not_done_is_silent."},
  {"severity": "minor",
   "title": "Hyphenated Waddell is not recognized (pre-existing at 8c190e8)",
   "evidence": "Probe X19 'Waddell-signs positive.' -> SILENT and X18 'Waddell-testing not performed; straight leg raise positive.' -> SILENT, on both HEAD and parent. app/backend/credibility.py:12 requires whitespace after Waddell in _WADDELL; sibling families use [\\s-]* (credibility.py:10 _SEP).",
   "why_it_matters": "A typed hyphen drops a Waddell count. The form is uncommon, but the same hyphen is accepted by the sibling patterns, so the omission is inconsistent and it is a missed flag.",
   "fix": "Use [\\s-]+ after Waddell in _WADDELL. Decide whether 'Waddell-testing not performed.' should be silent; if so, let _CLEAN accept the hyphen too.",
   "acceptance_test": "'Waddell-signs positive.' flags with the whole sentence as excerpt; a probe row for the hyphen forms is added to the flag-pass test set."},
  {"severity": "nit",
   "title": "'Not tested.' allow-list entry is inert; its pin cannot distinguish the allow-list",
   "evidence": "app/backend/credibility.py:37 adds r'not tested' to _CLEAN. Parent 8c190e8 has no such entry, and probe P06 'Not tested.' is SILENT there too. No _PATTERNS entry (credibility.py:15-24) matches 'Not tested.', so the entry cannot change output. test_t111_single_clause_not_performed_or_not_done_is_silent (tests/unit/test_flags_pass.py:302) passes with or without the entry.",
   "why_it_matters": "The output is correct, so this is not a spec violation. The card AC says the allow-list includes 'Not tested/not performed', and that is met literally, but the test does not prove the allow-list does anything for this form.",
   "fix": "Either drop the r'not tested' entry and document that 'Not tested.' is silent because no term matches, or keep it and add an assertion that no credibility pattern matches 'Not tested.'.",
   "acceptance_test": "A test asserts that no _PATTERNS entry matches 'Not tested.', so the silence cannot be credited to the allow-list by accident."}
 ],
 "whats_right": [
  "All 10 requested probes match D-043 on HEAD 99c2b32; the two-sentence probe excerpts only the flagged second sentence, verbatim (P09).",
  "Every second-clause, contrast, side-qualifier and extra-word variant tried (X03-X10, X22, X25) flags, with the whole sentence as its verbatim excerpt.",
  "Full tests/unit passes on HEAD (2238 passed, 4 skipped) against the parent (2236 passed, 4 skipped): no regression, and the T-111 pins are in place."
 ],
 "questions_for_chris": [
  "Is a bare count ('3/5 positive') or a reversed 'Positive Waddell' a D-043 credibility trigger? Finding 1 turns on the answer; if yes, it becomes a blocker.",
  "D-043 now splits silence by noun: 'Waddell testing not done.' is silent while 'Waddell signs not done.' still flags (credibility.py:35; test_flags_pass.py:290). Is that split intended, or should not-done forms match across signs and testing? This is the open T-092 item."
 ]}
```
