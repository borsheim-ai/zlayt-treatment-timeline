# T-120 paralegal review

**Verdict: fail.** One blocker. The fix for "Hx obtained via ..." also hides a real prior condition that the pre-T-120 build flags. Lib09 itself is clean.

Scope: T-120 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09, lib02, lib11, sample, plus engine-level probes of flags.lexicon_flags.

What I checked:
- lib09 on HEAD: no pre_existing flag (T-120-123-paralegal-probe.out.json, A_lib09_pre_existing_flags = []). The parent flags the sentence on record 1 (T-120-paralegal-before-after-parent.txt). The other lib09 flags are unchanged (T-120-paralegal-flags-diff-parent.txt vs -HEAD.txt; only the pre_existing flag is gone).
- The card's "record 2" is wrong: the sentence is in record 1 of the library file and in app record r1 (A_raw_lib09_interpreter_sentence_in = [1]).
- Real prior controls on HEAD: sample still flags record 3 "Patient reports low back pain in 2023, resolved." and record 8 "Findings may represent degenerative change" (A_sample_pre_existing_flags). lib02 and lib11 still flag (A_lib02_pre_existing_flags, A_lib11_pre_existing_flags).
- Variants on the flag engine (T-120-paralegal-variants-HEAD.txt vs -parent.txt):
  - "Hx obtained via interpreter: lumbar strain 2019." raises nothing on HEAD; the parent flags the whole sentence.
  - "PHx obtained via patient's son: lumbar strain 2019." raises nothing on HEAD; the parent flags it.
  - Period-joined variants still flag on HEAD.
- Unit tests test_t120, test_t121 and test_t123 on the HEAD copy: 48 passed. None of them uses the colon form, so the regression is not covered.

Ship-bar score (verify_quickly 2): the lib09 entries verify quickly, but the prior-condition list cannot be trusted as complete until the colon case is fixed. A reviewer who relies on the flag list would miss the prior.

Findings are in the JSON block.

```json
{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); sample evals/golden/sample.txt; library case_lib09, case_lib02, case_lib11; engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan",
 "exercised": [
  "read board show T-120, personas/paralegal.md, CLAUDE.md",
  "pytest on tests/unit/test_t120_history_source_sentence.py, test_t121_letter_styles.py, test_t123_baseline_same_day_paperwork.py on the HEAD copy: 48 passed",
  "HTTP on :7893 and :7894: POST /api/cases {library: case_lib09...}, poll status to ready, GET case flags (artifacts/review-evidence/T-120-paralegal-before-after-parent.txt, T-120-paralegal-flags-diff-parent.txt, T-120-paralegal-flags-diff-HEAD.txt)",
  "HTTP on :7893: sample, lib02, lib11 pre_existing flags (artifacts/review-evidence/T-120-123-paralegal-probe.out.json)",
  "in-process flags.lexicon_flags on lib09 record 1 with the excerpt replaced by 3 variants, HEAD and parent (T-120-paralegal-engine-HEAD.txt, T-120-paralegal-engine-parent.txt)",
  "in-process lexicon_scan.scan on 11 variant texts, HEAD and parent (T-120-paralegal-variants-HEAD.txt, T-120-paralegal-variants-parent.txt)",
  "raw record check of the library file: the sentence is in record 1 (A_raw_lib09_interpreter_sentence_in)"],
 "verdict": "fail",
 "scores": {"verify_quickly": 2, "prior_mentions_flagged": 2, "interpreter_sentence_not_flagged": 5},
 "findings": [
  {"severity": "blocker",
   "title": "The skip drops the whole prior hit, so a real prior after a colon on a history-source line is no longer flagged (regression vs 0c47356)",
   "evidence": "artifacts/review-evidence/T-120-paralegal-engine-HEAD.txt: 'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag; \"PHx obtained via patient's son: lumbar strain 2019.\" -> NO pre_existing flag. artifacts/review-evidence/T-120-paralegal-engine-parent.txt, same inputs: ['Hx obtained via interpreter: lumbar strain 2019.'] and [\"PHx obtained via patient's son: lumbar strain 2019.\"]. Same result in T-120-paralegal-variants-HEAD.txt vs -parent.txt.",
   "why_it_matters": "Checklist 9 and card AC 1 (a real prior-condition mention still raises the flag) are broken for this shape. The record still says lumbar strain 2019, but the tool no longer surfaces it, which is the prior injury the adjuster will find and the paralegal missed. The fix removes a guess (a source phrase is not a prior) and deletes a fact next to it.",
   "fix": "Drop only the source-phrase span (for example 'Hx obtained via interpreter') from the hit, and keep any lexicon match that extends past it, including after a colon or semicolon. Keep the current sentence-level behaviour for 'Hx obtained via ..., who interpreted. Hx of lumbar strain 2019.'.",
   "acceptance_test": "Add both colon inputs above to REAL in tests/unit/test_t120_history_source_sentence.py and assert FL.lexicon_flags(record) returns a pre_existing flag for each. Re-run the T-120 probe: lib09 still has no pre_existing flag, and sample still flags record 3 and record 8. Re-run the parent-vs-HEAD variant probe and expect no row to lose a flag that the parent raised except the source-phrase-only row."},
  {"severity": "minor",
   "title": "Card AC and test name cite lib09 'record 2' for the interpreter sentence; it is record 1",
   "evidence": "board/cards/T-120.md AC 1 text: 'the interpreter-history sentence of record 2'; test name test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do; evals/library/case_lib09_spanish_interpreter_espalda.txt, '=== Record 1 ===' Excerpt starts 'Hx obtained via patient's son, who interpreted.'; record 2 (14/04/2026, Consultorio Médico Aguaclara) has no such sentence; A_raw_lib09_interpreter_sentence_in = [1].",
   "why_it_matters": "Checklist 3 needs the record reference to point at the right source in one action. A paralegal who opens record 2 to check the AC will not find the sentence.",
   "fix": "Change the AC text, the test name and the handoff to record 1 (app id r1).",
   "acceptance_test": "grep of the AC and test name shows record 1; the lib09 record list in the case JSON shows the sentence under r1."},
  {"severity": "nit",
   "title": "Flag ids are positional: f_r1_1 names a different flag on HEAD than on the parent",
   "evidence": "artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt: id f_r1_1 = pre_existing (Hx sentence), f_r1_2 = causation 'Reported onset'. T-120-paralegal-flags-diff-HEAD.txt: id f_r1_1 = causation 'Reported onset'; f_r1_2 is gone.",
   "why_it_matters": "If any saved decision is keyed by flag id, it could attach to a different flag after a re-run. I did not test whether decisions carry over, so this is a risk to check, not a loss I reproduced.",
   "fix": "Derive flag ids from category and record so they survive a removed flag, or confirm that decisions are not keyed by id across builds.",
   "acceptance_test": "A flag decision made on a case before a flag is removed still points at the same flag after a re-run on the new build."}
 ],
 "whats_right": [
  "lib09 on HEAD raises no pre_existing flag on the 'Hx obtained via patient's son, who interpreted.' sentence, and the gap (42 days), date-to-confirm and three patient-report flags are unchanged against the parent",
  "the sample's two real prior mentions (record 3 'low back pain in 2023, resolved', record 8 'may represent degenerative change') still raise flags, with verbatim evidence",
  "the period-joined 'Hx ... Hx of lumbar strain 2019.' and 'Hx ... Prior low back pain 2023, resolved.' forms still flag on HEAD"],
 "questions_for_chris": [
  "On the live backend the model may also propose a prior-condition flag. Does the merge at flags.py:249 keep an LLM prior flag on the Hx sentence? The fixture set cannot show this; I only tested the lexicon path."]
}
```
