# T-111 round 2 review: claims-adjuster-reviewer

Commit under review: 4a560d8 (`app/backend/credibility.py`, `tests/unit/test_flags_pass.py`), parent 8a2b934. Pre-T-111 base 8c190e8 used for comparison. Reviewed from `git archive`; `git diff --stat HEAD` on the two files is empty, so the working tree matches the commit for these files.

**Verdict: changes** (0 blockers, 1 major, 3 minor, 1 nit).

**Closed from round 1.** The four named forms flag the whole sentence verbatim (probes R01 to R04). A bare "3/5 positive." right after a Waddell not-performed sentence now flags, with excerpt "3/5 positive." (R05; parent 8a2b934 was silent). The single-clause not-performed forms stay silent (R07 to R10). Reversed "Positive Waddell." and hyphen "Waddell-signs positive." now flag (r1 minor 3 closed).

**Still open.** The bare-count rule only looks back at the immediately preceding sentence. A count that comes first (A02), a word-form count (A06) and a non-adjacent count (A03) stay silent, so the r1 major is only partly closed. Two new over-flags came with r2: a straight-leg-raise count after a Waddell sentence (A01) and a hyphenated single-clause not-performed form (A04). The quoted single clause (A05) and the inert "Not tested." entry carry over from r1.

**Scope.** No Waddell text appears in the Appendix A sample (`spec/` has no match) and no lib12 record pairs a not-performed sentence with a count (`evals/library/case_lib12_records_review_credibility.txt` lines 21 to 46), so none of these gaps is in a record in this tree. They are recall and precision gaps in the flag pass, not omissions from the records.

**Probe results** (production `run_flag_pass`, `python -I`, output in `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t111r2-head.out.json`, same name with `t111r2-parent` and `t111r2-base`):

| Probe | Text | HEAD 4a560d8 | Parent 8a2b934 | Base 8c190e8 |
|---|---|---|---|---|
| R01 | Positive Waddell signs. | FLAG whole | FLAG whole | FLAG whole |
| R02 | Waddell 3/5 positive. | FLAG whole | FLAG whole | FLAG whole |
| R03 | 3 of 5 Waddell signs. | FLAG whole | FLAG whole | FLAG whole |
| R04 | Waddell's signs positive. | FLAG whole | FLAG whole | FLAG whole |
| R05 | Waddell testing not performed. 3/5 positive. | FLAG "3/5 positive." | silent | FLAG "Waddell testing not performed." |
| R06 | 3/5 positive. | silent | silent | silent |
| R07 | Waddell testing not performed. | silent | silent | FLAG |
| R08 | Waddell testing not done. | silent | silent | FLAG |
| R09 | Waddell signs not tested. | silent | silent | silent |
| R10 | Not tested. | silent | silent | silent |
| A01 | Waddell testing not performed. Straight leg raise 3/5 positive. | FLAG "Straight leg raise 3/5 positive." | silent | FLAG "Waddell testing not performed." |
| A02 | 3/5 positive. Waddell testing not performed. | silent | silent | FLAG "Waddell testing not performed." |
| A03 | Waddell signs positive. Straight leg raise negative. 3/5 positive. | FLAG "Waddell signs positive." only | same | same |
| A04 | Waddell-testing not performed. | FLAG whole | silent | silent |
| A05 | "Waddell testing not performed." (curly quotes) | FLAG whole | FLAG whole | FLAG whole |
| A06 | Waddell testing not performed. Three of five positive. | silent | silent | FLAG "Waddell testing not performed." |

Test runs: `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py` in the repo gives 35 passed. The same command on the HEAD archive gives 35 passed and on the parent archive 34 passed.

## Findings

1. **major, bare count before a not-performed sentence, a word-form count and a non-adjacent count stay silent.** A02 and A06 are silent on HEAD and A02 is silent on the parent; the pre-T-111 base flagged the not-performed sentence in A02 and A06. Code: `app/backend/credibility.py:80` starts the loop at `range(1, len(units))`, so the first sentence never gets the bare-count check, and `:83` requires the immediately preceding sentence to match `_WADDELL`. `:17` matches digits and a denominator of 5 only.
2. **minor, new over-flag: a straight-leg-raise count after a Waddell sentence.** A01 HEAD flags `Straight leg raise 3/5 positive.` as `credibility_language`; the parent was silent. `credibility.py:82` searches the whole sentence with no subject check. The excerpt is verbatim, so nothing is invented, but a non-Waddell result is filed as a credibility line.
3. **minor, new over-flag on the hyphenated single-clause form.** A04 `Waddell-testing not performed.` flags on HEAD; the parent and base were silent. r2 added the hyphen to `_WADDELL` (`credibility.py:15`), but `_CLEAN` (`:40`) has no hyphen, and `_clean_negation` (`:47`) normalizes whitespace only. r1 minor 3 left the silence decision open and r2 did not record one.
4. **minor, carry-over from r1 minor 2: quoted single clause flags.** A05 flags on HEAD. `credibility.py:43` (`_END`) accepts a closing quote or bracket as a terminator, while `:47` strips only `.!? ` before the clean match.
5. **nit, carry-over from r1 nit 4: "Not tested." entry is inert.** R10 is silent on the base 8c190e8, which has no T-111 entry, so the `r"not tested"` entry at `credibility.py:41` cannot change output.

```json
{"card": "T-111", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 4a560d8 (app/backend/credibility.py, tests/unit/test_flags_pass.py) via git archive; parent 8a2b934 and pre-T-111 base 8c190e8 for comparison; unit-level production run_flag_pass path, no app URL; Appendix A sample and lib12 library checked for Waddell text",
 "exercised": [
   "Read personas/claims-adjuster.md in full; read reviews/T-111-claims-adjuster.md (round 1); read my memory files project_t111_positive_count_recall and reviewer-write-and-parse-guards",
   "git rev-parse HEAD -> 4a560d81ff72cff9bd316a85223856108cfc64dc; git rev-parse 4a560d8^ -> 8a2b934ada770a29cc90bd677015cd1f62e2726a; git cat-file -t 8c190e8 -> commit",
   "git show 4a560d8 -- app/backend/credibility.py tests/unit/test_flags_pass.py (r2 diff read in full)",
   "git diff --stat HEAD -- app/backend/credibility.py tests/unit/test_flags_pass.py -> empty (working tree equals HEAD for the reviewed files)",
   "git archive 4a560d8, 8a2b934 and 8c190e8 extracted to the session scratchpad (t111r2-head, t111r2-parent, t111r2-base)",
   ".venv/bin/python -m pytest -q tests/unit/test_flags_pass.py in the repo -> '35 passed in 0.42s'; same command in t111r2-head -> '35 passed in 0.47s'; in t111r2-parent -> '34 passed in 0.45s'",
   "Read app/backend/credibility.py lines 1-88 with line numbers (archive t111r2-head); read tests/unit/test_flags_pass.py _cred helper (line 188) and T-111 and T-111 r2 test blocks (lines 302-344)",
   "Wrote artifacts/review-evidence/T-111-r2-probe.py (16 probes: R01-R10 from the brief, A01-A06 mine); ran with python -I against t111r2-head, t111r2-parent and t111r2-base; outputs in the scratchpad as t111r2-*.out.json",
   "Inline python -I check on HEAD and base: 'Waddell-signs positive.' flags on HEAD (silent on base); 'Waddell-testing not performed; straight leg raise positive.' flags on HEAD (silent on base); 'Waddell testing not performed. Positive Waddell.' flags only 'Positive Waddell.' on HEAD; 'Not tested.' silent on both",
   "grep -rn -i waddell spec/ evals/ and sed of evals/library/case_lib12_records_review_credibility.txt (grep for not performed, not done, not tested, positive): no Waddell text in spec/; lib12 Waddell lines are 21, 31, 36, 46 and contain no not-performed/count pair",
   "python3 tools/board.py show T-111 (grep of notes): round-2 note lists the quoted and inert-entry items as left untouched and does not record a bare-count scope decision; memory/SCOPE_CUTS.md has no bare-count row"
 ],
 "verdict": "changes",
 "scores": {"d043_single_clause_silence": 4, "waddell_term_recall_word_orders": 4, "bare_count_recall": 2, "excerpt_verbatim_whole_sentence": 5, "new_overflag_absence": 3, "flag_pass_unit_tests": 5},
 "findings": [
  {"severity": "major",
   "title": "Bare positive count before a not-performed sentence, word-form count and non-adjacent count stay silent (r1 major only partly closed)",
   "evidence": "Probe artifacts/review-evidence/T-111-r2-probe.py on 4a560d8: A02 '3/5 positive. Waddell testing not performed.' -> silent; A06 'Waddell testing not performed. Three of five positive.' -> silent; A03 'Waddell signs positive. Straight leg raise negative. 3/5 positive.' -> only 'Waddell signs positive.'. Parent 8a2b934: A02 silent. Base 8c190e8: A02 and A06 flag 'Waddell testing not performed.'. app/backend/credibility.py:80 range(1, len(units)) never checks the first sentence as the count; :83 requires the immediately preceding sentence to match _WADDELL; :17 _BARE_COUNT matches digits with denominator 5 only.",
   "why_it_matters": "A positive Waddell count is the result an adjuster argues. T-111 silenced the single-clause not-performed sentence, so in A02 the pair now carries no flag, although the base flagged the not-performed sentence. r2 closes the count-after order (R05) but not count-before or word-form counts. D-043 is met literally: a bare count is not a credibility trigger and the not-performed clause is allow-listed. So this is a recall gap in the scope r2 chose, not a literal D-043 break, and it stays major for the same reason as r1. It is not in any record in this tree (see scope). If Chris rules that a bare count is a D-043 trigger, I re-rate it to blocker, since the flags would then omit a Waddell result the records contain.",
   "fix": "Chris rules bare-count scope (question 1). If in scope: flag a bare N/5 or N of 5 positive whether it precedes or follows a Waddell sentence in the same record, and accept word-form counts ('three of five'). If out of scope: add a memory/SCOPE_CUTS.md row naming the excluded orders and word forms, as r1 fix (b) asked; that row does not yet exist.",
   "acceptance_test": "A02 flags exactly '3/5 positive.' and A06 flags 'Three of five positive.' in tests/unit/test_flags_pass.py beside test_t111_r2_reversed_and_counted_waddell_forms_flag_and_bare_count_after_a_waddell_sentence_flags; or a SCOPE_CUTS row names both forms and the reason. The r2 pin 'Waddell testing not performed. 3/5 positive.' -> ['3/5 positive.'] keeps passing."},
  {"severity": "minor",
   "title": "New over-flag: straight-leg-raise count after a Waddell sentence is filed as credibility_language",
   "evidence": "Probe A01 'Waddell testing not performed. Straight leg raise 3/5 positive.' on 4a560d8 -> flag excerpt 'Straight leg raise 3/5 positive.' (category credibility_language). Parent 8a2b934 -> silent. app/backend/credibility.py:82 _BARE_COUNT.search(text, a, b) matches the count in any sentence with no check of its subject.",
   "why_it_matters": "The excerpt is verbatim, so no text is invented. But a straight-leg-raise result is filed under the Waddell credibility category, and the paralegal sees a credibility line that belongs to a different test. D-043 says fail toward flagging, so the cost is one click and the direction is acceptable. Still, it is a precision regression introduced by r2.",
   "fix": "Limit the bare-count match to a sentence whose subject is the count itself (the count opens the sentence, or the sentence names Waddell), or exclude sentences that name another test (straight leg raise, SLR, Lasegue). Pin the exclusion.",
   "acceptance_test": "'Waddell testing not performed. Straight leg raise 3/5 positive.' -> [] on the bare-count path; the test pins it beside the r2 bare-count pin."},
  {"severity": "minor",
   "title": "New over-flag: hyphenated single-clause 'Waddell-testing not performed.' flags",
   "evidence": "Probe A04 'Waddell-testing not performed.' on 4a560d8 -> flag 'Waddell-testing not performed.'. Parent 8a2b934 and base 8c190e8 -> silent. app/backend/credibility.py:15 (_WADDELL third alternative) now matches the hyphen; :40 _CLEAN has 'waddell testing not (?:performed|done)' with no hyphen; :47 _clean_negation normalizes whitespace only.",
   "why_it_matters": "The brief says single-clause not-performed forms stay silent. The hyphen form is a single clause of that kind. D-043 literally flags anything not on the allow-list, so this is a fail-toward-flag consequence and not a literal break, but r2 changed the behaviour without deciding it. r1 minor 3 asked for that decision.",
   "fix": "Decide. If silent, add a hyphen-or-space separator between 'waddell' and 'testing' in the _CLEAN entry at credibility.py:40 and pin it. If flagging, record the decision in memory/SCOPE_CUTS.md or DECISIONS and pin the flag.",
   "acceptance_test": "'Waddell-testing not performed.' -> [] (and the hyphen 'done' form too) in test_t111_single_clause_not_performed_or_not_done_is_silent, or the flag is pinned with a recorded decision."},
  {"severity": "minor",
   "title": "Carry-over from r1 minor 2: quoted single-clause not-performed form flags",
   "evidence": "Probe A05 on 4a560d8: the curly-quoted sentence -> flag '“Waddell testing not performed.”'. Same on parent 8a2b934 and base 8c190e8. app/backend/credibility.py:43 _END accepts a closing quote or bracket as a terminator; :47 strips only '.!? ' before the clean match.",
   "why_it_matters": "A quoted single clause is still one clause and is allow-listed. The direction is fail-toward-flag, so the cost is one click. Unchanged from r1, and the r2 card note lists it as left untouched.",
   "fix": "In _clean_negation at credibility.py:47, strip the closing quote and bracket characters that _END accepts before the clean match, then pin the quoted and bracketed forms.",
   "acceptance_test": "The straight-quoted, curly-quoted and bracketed forms of 'Waddell testing not performed.' return [] from run_flag_pass and are pinned in test_t111_single_clause_not_performed_or_not_done_is_silent."},
  {"severity": "nit",
   "title": "Carry-over from r1 nit 4: 'Not tested.' allow-list entry cannot change output",
   "evidence": "Probe R10 'Not tested.' is silent on 4a560d8, on parent 8a2b934 and on base 8c190e8, which has no T-111 entry. app/backend/credibility.py:41 r'not tested' in _CLEAN; no _PATTERNS entry matches 'Not tested.'.",
   "why_it_matters": "The output is correct and no spec line is broken. The pin does not show the allow-list doing anything for this form.",
   "fix": "Drop the entry and document that 'Not tested.' is silent because no term matches, or keep it and assert that no _PATTERNS entry matches 'Not tested.'.",
   "acceptance_test": "A test asserts no _PATTERNS entry matches 'Not tested.', so its silence is not credited to the allow-list by accident."}
 ],
 "whats_right": [
  "The four named forms (R01 to R04) flag the whole sentence verbatim on 4a560d8, and the bare '3/5 positive.' after a Waddell not-performed sentence (R05) now flags with its own verbatim excerpt.",
  "The single-clause not-performed and not-done forms (R07 to R10) stay silent, and the reversed 'Positive Waddell.' and hyphen 'Waddell-signs positive.' now flag (base 8c190e8 was silent on the hyphen form).",
  "tests/unit/test_flags_pass.py: 35 passed on HEAD and 34 on the parent, with no test broken by the r2 change."
 ],
 "questions_for_chris": [
  "Is a bare N/5 positive a D-043 credibility trigger, in both orders and as a word-form count? Finding 1 turns on the answer. If yes, it becomes a blocker under my section 5, because the flags would omit a Waddell result. If no, the scope needs a SCOPE_CUTS row.",
  "Should 'Waddell-testing not performed.' (hyphen, single clause) be silent like its space form? Findings 3 and 4 both depend on the answer. The r2 change made it flag without a recorded decision.",
  "CLAUDE.md section 6 says judgment reviewers run on Opus, and my dossier expects claude-opus-5-5. This round ran as claude-haiku-5-5, as the brief asked. Should this persona's gate be re-run on Opus before T-111 closes?"
 ]}
```

Outside my lens: the full unit suite (the card note cites 2378 passed; I did not run it), the lexicon.yaml consistency check (researcher-owned), and the golden eval runner.
