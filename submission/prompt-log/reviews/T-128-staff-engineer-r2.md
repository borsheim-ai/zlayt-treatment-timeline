# T-128 review, round 2 - staff-engineer-reviewer

Card: summary trim must never leave a fragment, kill the T-112 r3 surviving mutants, and (orchestrator note) read negation words from the lexicon. Commits 180138c (structural rule) and 2790918 (lexicon negation). I worked on `git archive` copies in my scratchpad: `T128_9_r2/repo` is 1f0a164 (the code of 180138c), `T128_9_r2b/repo` is 2790918. After the second archive HEAD moved to 5dfba88; `git diff 2790918 HEAD --stat -- app tests/unit memory/contracts` is empty, so the code I reviewed is HEAD's. Scripts are in `artifacts/review-evidence/T-128-129-r2/`.

**Verdict: changes.** One major, three minors, one nit. The rule is implemented as the orchestrator specified and it holds every probe from round 1. But the claim "fragments are impossible by construction" (module docstring, api.md, handoff) is false: the rule guards the start of the summary and `,` / `and` / `with` joins, and does not guard a kept later clause that is itself dependent. 12 of 17 fresh probes of that shape leave a fragment or a mis-attached result.

## 1. Deterministic checks
- `tests/unit` at 1f0a164: 3186 passed, 4 skipped, 0 failed (the handoff says 3189; the working tree had more tests than HEAD). At 2790918: 3214 passed, 4 skipped, 0 failed. `tests/unit/test_summary_trim.py` at 2790918: 286 passed.
- No model or network: `summary_trim.py` is pure code.

## 2. Round-1 probes re-run (probe_t128_r2.py, probe_t128b_r2.py)
- 31 fragment probes: 27 stay whole, 3 go to the tray (`''`, every clause unsupported), 1 trims to a whole clause (`MRI done; mild disc bulge noted at L4.` -> `MRI done.`). None leaves a fragment. The 10 clear fragments of round 1 now stay whole.
- 12 should-trim probes: 10 trim to whole clauses (the four two-sentence pairs that the round-1 guard blocked now trim). 2 stay whole: `Was seen at the ER; surgery recommended.` (prefix has one content word, `ER`) and `Headache; CT scan ordered; ibuprofen advised.` (one content word). Both fail safe, the judge sees them. The handoff says `Was seen at the ER` trims; the test (test_summary_trim.py:613-615) asserts it does not.

## 3. Fresh probes (fresh_t128_r2.py, 26 pairs): the claim "impossible by construction" fails
Clean results: `Neck pain with stiffness; surgery recommended.` -> `Neck pain with stiffness.`, `Ankle pain; X-ray taken; no fracture.` -> `Ankle pain; no fracture.`, `Neck pain, injection given, relief noted.` stays whole (comma join), `Pain; MRI ordered; ...` stays whole (one-word prefix), `Surgery recommended; neck pain.` stays whole. Then the kept-later-clause shape, where the clause before it is removed and the separator is `;` or `.`:
- `Neck pain; injection given; resulting in relief.` -> `Neck pain; resulting in relief.`
- `Wrist pain; splint applied; which helped.` -> `Wrist pain; which helped.`
- `Neck pain; cast applied; however, improving.` -> `Neck pain; however, improving.`
- `Shoulder pain; surgery performed; due to torn labrum.` -> `Shoulder pain; due to torn labrum.` (the card title's own example, `Due to torn meniscus.`, with `;` instead of `,`)
- `Back pain; ultrasound done; thereafter, improvement.` -> `Back pain; thereafter, improvement.`
- `Back pain; epidural given; as a result, less pain.` -> `Back pain; as a result, less pain.`
- `Wrist fracture; cast applied; including follow-up.` -> `Wrist fracture; including follow-up.`
- `Neck pain; ibuprofen prescribed; 3 times daily.` -> `Neck pain; 3 times daily.`; `Neck pain; physical therapy started; for six weeks.` -> `Neck pain; for six weeks.`; `Knee pain; brace issued; as needed.` -> `Knee pain; as needed.`
- Mis-attached result: `Head injury; CT ordered; negative.` -> `Head injury; negative.`; `Hip pain; X-ray taken; unremarkable.` -> `Hip pain; unremarkable.` (the imaging result now reads as the finding on the injury).
That is 10 dependent fragments and 2 mis-attached results of 17 probes of this shape. Rule 3 (summary_trim.py, the loop over `clauses[i - 1][1]`) only looks at `,` `and` `with`; the docstring says "only ';' or a sentence end lets a clause stand alone", which is true of the grammar only for independent clauses.

## 4. Mutation of the tests (mut_t128_r2.py on 1f0a164; mut2_t128_r2.py on 2790918)
- Rule mutants, 16 on 1f0a164: 14 killed (prefix <1, <3, prefix to the LAST cut, rule 3 off, rule 3 without `,`, without `and`, without `with`, rule 3 ignoring the previous removal, tray condition, participle merge off, join strength reversed, final period dropped, no-removal marks changed, quote negation off). Survived 2: "rule 1 off" (equivalent: an empty prefix has 0 content words, rule 2 fires; the handoff says so) and "capitalise off" (dead code since the first kept clause is always clause 0).
- Abbreviation sweep (sweep_r2.py, absolute script path): 27 entries, each set to a dead word, `survivors: []`. IV, hep, ekg were deleted from the table as inert rather than tested; orif is now killed. Reverse-direction pairs (rev_r2.py): 0 of 18 over-trim, including `ORIF wrist.` and `RCR performed.` that over-trimmed in round 1.
- Lexicon mutants on 2790918 (8): 6 killed (quote extra=False, quote negation off, clause negation only `no`, never, clause side words never, prefix <1). Survived 2: the `n't` contraction branch (`Neck pain; couldn't sleep.` over `Neck pain.` stays whole under the mutant and 286 tests pass) and `quote sides ignored` (not shown to be equivalent).

## 5. Negation moved to the lexicon (commit 2790918): behaviour change
Checked: no `_NEG`, `_NEG_WORDS` or `_SIDE_WORDS` assignment remains (`grep -n` of summary_trim.py at 2790918 shows `grounding.aq("side")`, `grounding.is_negation_word`, `grounding.has_negation(ex, extra=True)`), and a test pins that. Old (1f0a164) against new, same pairs (neg_diff_t128_r2.py, neg_diff2, neg_diff3: 75 pairs):
- Summary side, now trimmed (was kept, correct): `absence of numbness`, `lacks radiation`, `free of numbness`, `nothing abnormal found`, `absence of weakness`, `lacks coordination`, `free of weakness`, each over `Neck pain.` -> `Neck pain.` These were under-trims.
- Quote side, a negation word now vouches (was trimmed): `Neck pain; no numbness.` over `Neck pain. Nothing else reported.` and over `Neck pain. Absence of tingling.` now stay whole (judge sees them). Looser, in the safe direction; same lenient design as `unremarkable`.
- `deny`: `Neck pain; no trouble breathing.` over `Neck pain. Deny dyspnea.` changes from kept to trimmed (`Neck pain.`), a faithful paraphrase over-trimmed because the quote's only negation is the bare word `deny`. Pairs that share a word with the quote (`no nausea` over `Deny N/V`, `no loss of consciousness` over `Deny syncope`) stay whole. `Denying` and `Denial of` were never recognised by either version (`no trouble breathing` over `Denying dyspnea.` trims in both).
- `denies fever` as a summary clause trims in both. Under-trim: none found beyond the unrecognised deny forms.

```json
{"card": "T-128", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 1f0a164 (180138c code) and 2790918 in scratchpad T128_9_r2 / T128_9_r2b; HEAD at end of review 5dfba88 (app/tests/contract unchanged since 2790918); app/backend/summary_trim.py, tests/unit/test_summary_trim.py, app/backend/grounding.py has_negation/is_negation_word, memory/contracts/api.md summary-trim section; fixture/no backend, no network",
 "exercised": [
  "python3 tools/board.py show T-128, T-129; read reviews/T-128-staff-engineer.md and T-129-staff-engineer.md; git show 1f0a164; git diff HEAD on the working tree",
  ".venv/bin/python -m pytest tests/unit -q in the 1f0a164 archive: 3186 passed, 4 skipped; in the 2790918 archive: 3214 passed, 4 skipped; test_summary_trim.py: 286 passed",
  "probe_t128_r2.py (the 31 round-1 fragment probes) and probe_t128b_r2.py (the 12 should-trim pairs) against 1f0a164",
  "fresh_t128_r2.py: 26 new pairs (9 should-trim or should-hold, 17 kept-later-clause fragment shapes)",
  "mut_t128_r2.py: 16 rule mutants on summary_trim.py; mut2_t128_r2.py: 8 lexicon mutants on 2790918",
  "sweep_r2.py: 27 abbreviation entries set dead one at a time (survivors: none); rev_r2.py: 18 reverse-direction pairs (0 over-trim)",
  "neg_diff_t128_r2.py, neg_diff2_t128_r2.py, neg_diff3_t128_r2.py: 75 negation pairs, old (1f0a164) against new (2790918) in separate processes",
  "manual mutant: n't branch removed from new_salient on a copy of 2790918 -> 286 passed and three contraction clauses stay whole",
  "grep of summary_trim.py for _NEG, _NEG_WORDS, _SIDE_WORDS, has_negation, is_negation_word"
 ],
 "verdict": "changes",
 "scores": {"deterministic_trim_is_code": 5, "fragment_safety": 3, "unsupported_removal_precision": 4, "faithful_paraphrase_survival": 4, "test_strength": 4, "lexicon_single_source": 5, "doc_matches_code": 2},
 "findings": [
  {"severity": "major",
   "title": "'Fragments are impossible by construction' is false: a kept later clause that depends on a removed one survives when the separator is ';' or '.' (12 of 17 fresh probes)",
   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/fresh_t128_r2.py <archive>`: 'Shoulder pain; surgery performed; due to torn labrum.' -> 'Shoulder pain; due to torn labrum.'; 'Neck pain; injection given; resulting in relief.' -> 'Neck pain; resulting in relief.'; 'Wrist pain; splint applied; which helped.' -> 'Wrist pain; which helped.'; 'Neck pain; cast applied; however, improving.' -> 'Neck pain; however, improving.'; 'Back pain; epidural given; as a result, less pain.' -> 'Back pain; as a result, less pain.'; 'Wrist fracture; cast applied; including follow-up.' -> 'Wrist fracture; including follow-up.'; 'Neck pain; physical therapy started; for six weeks.' -> 'Neck pain; for six weeks.'; 'Head injury; CT ordered; negative.' -> 'Head injury; negative.'; 'Hip pain; X-ray taken; unremarkable.' -> 'Hip pain; unremarkable.'. summary_trim.py trim(), rule (3) checks only clauses[i - 1][1] in (',', 'and', 'with'). Docstring: 'Fragments are impossible by CONSTRUCTION'; api.md summary-trim section says the same; D-054 'never leaving a fragment'.",
   "why_it_matters": "This is the round-1 finding (fragment class) with a different separator, and the card title names 'Due to torn meniscus.' as the thing that must not happen. The word list is gone but the guarantee is not delivered: the first clause and the prefix are safe, the tail is not. Nothing is invented, the quote and trace stay and judge 1 sees the text, so it is not a blocker, but 'Head injury; negative.' attaches an imaging result to the wrong finding and the docs promise it cannot happen.",
   "fix": "Keep the structural approach and extend it to the tail: either (a) allow a removal only when every clause after the first removal is also removed (suffix cut; otherwise the whole summary goes to judge 1), or (b) require a kept clause that follows a removed one to start with a content word that is not in _STOP and not a participle (reuse _STOP and _PARTICIPLE, no new list) and to carry its own head noun. Or soften the docstring, api.md and D-054 to name exactly what is guaranteed (first clause, 2-word prefix, no comma/and/with orphan).",
   "acceptance_test": "tests/unit/test_summary_trim.py: the 12 summaries above return changed False (or, for option b, none of them yields a kept clause starting with resulting/which/however/due/as/including/for/negative/unremarkable); 'Ankle pain; X-ray taken; no fracture.' still trims to 'Ankle pain; no fracture.' and 'Neck pain. Surgery recommended; follow-up in two weeks.' still trims."},
  {"severity": "minor",
   "title": "The lexicon move makes bare 'deny' count as no negation: a faithful paraphrase is now trimmed ('no trouble breathing' over 'Deny dyspnea.')",
   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/neg_diff3_t128_r2.py <1f0a164 archive> <2790918 archive>`: DIFF 'Neck pain; no trouble breathing.' | 'Neck pain. Deny dyspnea.' | old: [False, 'Neck pain; no trouble breathing.'] | new: [True, 'Neck pain.']. grounding.has_negation('Deny N/V.', extra=True) is False; lexicon.yaml:1412 negation_word is '\\b(?:no|not|none|never|without|denies|denied|negative|neither|nor|absent)\\b' (no deny, denying, denial).",
   "why_it_matters": "A clause is removed (and in a one-clause summary the entry goes to the could-not-verify tray) when the summary says 'no X' and the quote's only negation is 'deny' with a different noun. Fail-direction is visible (the paralegal sees the trim note), and the orchestrator already queued a researcher card for the lexicon, so this is minor. The same gap hides 'denying' and 'denial of' in both old and new code.",
   "fix": "Researcher card: add deny, denying, denial of to negation_word (and a hit/miss example) in app/llm/lexicon.yaml; add the pair above as a test in test_summary_trim.py so it goes red until then.",
   "acceptance_test": "T.trim('Neck pain; no trouble breathing.', 'Neck pain. Deny dyspnea.')['changed'] is False and the same for 'Denying dyspnea.' and 'Denial of dyspnea.'."},
  {"severity": "minor",
   "title": "Test gap: the n't contraction branch of new_salient is untested; removing it leaves 286 tests green and contraction clauses unsupported-but-kept",
   "evidence": "Copy of 2790918 with `w.endswith(\"n't\") or grounding.is_negation_word(w)` changed to `grounding.is_negation_word(w)`: `pytest tests/unit/test_summary_trim.py` -> 286 passed; T.trim(\"Neck pain; couldn't sleep.\", 'Neck pain.')['changed'] False, same for \"didn't miss work\" and \"can't lift\" (the unmutated code trims all three). Also 'quote sides ignored' (mut2_t128_r2.py) survives.",
   "why_it_matters": "The card's second half is 'kill the surviving mutants'; this refactor opened a new one in code it rewrote, and a regression there would silently stop trimming negated clauses with contractions.",
   "fix": "Add a parametrized test over couldn't / didn't / can't clauses with a quote that has no negation (trimmed) and one that has (kept); add one quote-side test where the quote says 'bilateral' only.",
   "acceptance_test": "The contraction-branch mutant and the quote-sides mutant in mut2_t128_r2.py print KILLED."},
  {"severity": "nit",
   "title": "Handoff says 'Was seen at the ER' trims; the test asserts it does not; two dead lines remain",
   "evidence": "Handoff: '8 positive controls trim incl. the two-sentence and Was seen at the ER cases'. tests/unit/test_summary_trim.py:613-615 test_the_first_clause_is_never_removed: `assert not r['changed']` for that pair. summary_trim.py `if drop[0]: return unchanged` is equivalent to rule 2 (the handoff says so) and `out = out[:1].upper() + out[1:]` survives deletion (the first kept clause is always clause 0).",
   "why_it_matters": "Handoff accuracy and dead code only; behaviour is the safe one.",
   "fix": "Correct the handoff wording; delete or comment the capitalise line.",
   "acceptance_test": "none needed"}
 ],
 "whats_right": [
  "All 31 round-1 fragment probes now stay whole or go to the tray, and the 4 two-sentence should-trim pairs that the old guard blocked trim again; prefix and first-clause rules are each killed by a named test.",
  "Abbreviation table sweep is clean (27 entries, no survivors) and the reverse ORIF/RCR over-trim is gone (0 of 18).",
  "Negation and side words come from the lexicon through grounding (no private lists), with a source-level guard test; the move closes under-trims for absence of, lacks, free of and nothing."
 ],
 "questions_for_chris": []}
```
