# T-092 claims-adjuster review (commit 81aa55e, D-043)

Reviewer: claims-adjuster-reviewer (Gary Pruitt persona), model claude-haiku-5-5 (the model I am running as).
Scope: commit 81aa55e, extracted with `git archive HEAD` into the session scratchpad. The live tree's flags.py, credibility.py and tests/unit/test_flags_pass.py are identical to the commit (`git diff --stat 81aa55e` empty for those files). The T-067 r5 comparison commit 0f58181 was extracted the same way.

## Coordinator question (answered)

'Waddell testing not performed.' and 'Waddell testing not done.' were **silent at 0f58181 and flag at 81aa55e** (N01, N02; `artifacts/review-evidence/T-092-claims-adjuster-probe-on-0f58181.out.txt:2-3` vs `artifacts/review-evidence/T-092-claims-adjuster-probe.out.txt:2-4`). The change is silent to flag, not flag again. The same change hits 'Waddell tests not performed.' and 'Waddell testing not tested.', while 'Waddell signs not performed.' stays silent.

D-043's literal form is 'Not tested/not performed.' with no subject (memory/ORCHESTRATOR_DECISIONS.md:51). It does not name 'Waddell testing'. Under fail-toward-flagging, a sentence not literally listed flags, so the flag is what the literal text requires. If Chris reads the form as covering any subject, these must be silent, and the error is one extra click, not a lost fact. Rated **minor**, not a blocker and not a regression under the literal text. The ruling is Chris's (questions 1 and 2).

## Three checks

- **Merged flag keeps the full period sentence: pass.** A model causation quote that overlaps a credibility sentence no longer replaces the excerpt (flags.py:139-140). N03, N04 and the r5 F01/F02 strings return 'Straight leg raise positive; Waddell signs negative.' with origin both, and evidence text and offsets equal the excerpt (test_flags_pass.py:302-312).
- **Allow-list matches D-043 exactly: no (minor).** credibility.py:26 says 'exactly the decision's six forms', and the comment at :27 quotes 'Waddell signs not tested / not performed.' where D-043 says 'Not tested/not performed.'. The code silences 'Waddell signs not tested/performed' (:34), which the literal form does not name. The silent pins at test_flags_pass.py:196 and :298-299 follow that reading. The flag side is consistent with the literal text, and the silence side is clean negations with no second clause, so no credibility fact is hidden.
- **Hedge run does not quote a neighbour: pass.** D01-D03 and N05-N06 quote only the credibility sentence (flags.py:93-94; test_flags_pass.py:315-320). The hedge run stays for other categories by design (R-TL-8).

## Tests and probes

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider`: 32 passed on the archive (0.41s) and on the live tree (0.67s).
- The r5 corpus re-run on 81aa55e: 28 counted rows, mismatches=0. C01-C10 now all flag, so the superset of silent forms is 0 (`artifacts/review-evidence/T-092-claims-adjuster-r5rerun.out.txt`).
- Six new strings N01-N06 plus diagnostic rows X01-X05: N03-N06 pass; N01-N02 are the coordinator's question (`artifacts/review-evidence/T-092-claims-adjuster-probe.out.txt`).
- Merge absorption (`artifacts/review-evidence/T-092-claims-adjuster-probe2.out.txt`): the model's speculative_language label is replaced by credibility_language. This predates the commit and is not in the card's AC; it is raised as a question.
- Citations checked with `artifacts/review-evidence/T-092-validate.py` against the archive, along with the verdict rule and JSON parse, before the single write.

Not exercised: the eval harness (the worker cites evals/reports/20261102T063158Z.md, not rerun), the app server, the sample case, and the full tests/unit suite (the worker reports 3 unrelated failures in test_t093_eval_signature.py).

## Verdict

**pass** by rule: no blocker, no major, two minor (findings 1 and 2 in the JSON). Both minors need Chris's reading of D-043 before the code or comment changes.

```json
{"card": "T-092", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 81aa55e (T-092, HEAD of main at review time), extracted with git archive HEAD into the session scratchpad (t092); the T-067 r5 comparison commit 0f58181 extracted the same way (t067r5); live tree flags.py, credibility.py and tests/unit/test_flags_pass.py are identical to the commit (git diff --stat 81aa55e empty); function-level probes through flags.run_flag_pass with FakeCall; no app URL, no sample case, no eval harness run",
 "exercised": [
   "python3 tools/board.py show T-092 (status in_review, commits [81aa55e], AC1 done, handoff lines)",
   "git rev-parse HEAD -> 81aa55ecb8b8c11727d064cce9e30919561929c3; git show --stat 81aa55e (credibility.py, flags.py, tests/unit/test_flags_pass.py only; sentences.py not in the commit)",
   "git archive HEAD | tar -x -C <scratchpad>/t092; git archive 0f58181 | tar -x -C <scratchpad>/t067r5",
   "personas/claims-adjuster.md read in full; reviews/T-067-claims-adjuster-r5.md read in full (F01 major, C01-C10 and D01 minor)",
   "memory/ORCHESTRATOR_DECISIONS.md:51 D-043 read verbatim: allow-list lists 'Not tested/not performed.' (no subject)",
   "coordinator question: artifacts/review-evidence/T-092-claims-adjuster-probe.py (6 new strings N01-N06 plus diagnostic X01-X05) run with .venv/bin/python -I on t092 -> artifacts/review-evidence/T-092-claims-adjuster-probe.out.txt; same script on t067r5 -> artifacts/review-evidence/T-092-claims-adjuster-probe-on-0f58181.out.txt: 'Waddell testing not performed.' and 'Waddell testing not done.' are silent at 0f58181 and flag at 81aa55e (N01, N02)",
   "r5 corpus: artifacts/review-evidence/T-067-claims-adjuster-r5-probe.py run with .venv/bin/python -I on t092 -> artifacts/review-evidence/T-092-claims-adjuster-r5rerun.out.txt: counted rows 28 (A01-A16, B01-B05, G01-G07) mismatches=0; C01-C10 now all flag (superset silent 0); D01-D03 excerpts are the credibility sentence only; F01-F02 excerpt is the whole sentence with origin both; E01-E03 silent, E04 flags",
   "artifacts/review-evidence/T-092-claims-adjuster-probe2.py run on t092 -> artifacts/review-evidence/T-092-claims-adjuster-probe2.out.txt: one model causation flag (category speculative_language) merges into one flag with category credibility_language, origin both, whole-sentence excerpt",
   "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider: archive t092 -> 32 passed in 0.41s; live tree (same command) -> 32 passed in 0.67s",
   "git diff --stat 81aa55e -- app/backend/flags.py app/backend/credibility.py tests/unit/test_flags_pass.py -> empty (live tree equals commit for these files)",
   "grep -n of every cited line on the archive: credibility.py 26-28, 33-34; flags.py 93-94, 137-140; tests/unit/test_flags_pass.py 196, 290-299, 302-312, 315-320; memory/ORCHESTRATOR_DECISIONS.md:51; artifacts/review-evidence/T-092-validate.py checks the same citations and the verdict rule before the write",
   "not exercised: evals harness (worker cites evals/reports/20261102T063158Z.md, not rerun), app server, sample case, full tests/unit suite (worker reports 3 unrelated fails in test_t093_eval_signature.py)"
 ],
 "verdict": "pass",
 "scores": {"merge_keeps_whole_sentence": 5, "hedge_run_no_neighbour_quote": 5, "allow_list_matches_d043": 3, "no_new_silent_misses_vs_r5": 5, "verbatim_and_grounded": 5, "commit_tests_green": 5},
 "findings": [
  {"severity": "minor",
   "title": "Allow-list is not exactly D-043: the code comment misquotes D-043 and the Waddell-scoped 'not tested/performed' form is not the decision's literal form",
   "evidence": "app/backend/credibility.py:26 says 'D-043 allow-list: exactly the decision's six forms and no others'; credibility.py:27 quotes 'Waddell signs not tested / not performed.' as the sixth form; memory/ORCHESTRATOR_DECISIONS.md:51 (D-043) reads 'Not tested/not performed.' with no subject; credibility.py:34 is r\"waddell signs not (?:tested|performed)\". Probe rows silent on t092: artifacts/review-evidence/T-092-claims-adjuster-r5rerun.out.txt:39-40 (B04 'Waddell signs not tested.', B05 'Waddell signs not performed.'). Pins at tests/unit/test_flags_pass.py:196 and :298-299 assert these stay silent under a test named test_t092_allow_list_is_exactly_the_d043_forms (line 290).",
   "why_it_matters": "The code and its test say the list is exactly D-043's, but the comment quotes D-043 with words the decision does not contain, and the code silences a subject-scoped form the literal list does not name. The silence side is clean negations with no second clause, so no credibility fact is hidden and this stays minor, the same class and rating as T-067 r5 C01-C10. What matters for the adjuster is that the record says 'exactly' when the list is an interpretation that Chris has not ruled on.",
   "fix": "Quote D-043 verbatim in the credibility.py:26-27 comment ('Not tested/not performed.'). Either record the Waddell-signs subject scope as a D-043 amendment or SCOPE_CUTS row (Chris decides, see questions_for_chris 1 and 2), or change the code to the generic form. Rename test_t092_allow_list_is_exactly_the_d043_forms to say what it pins.",
   "acceptance_test": "credibility.py comment equals memory/ORCHESTRATOR_DECISIONS.md:51 wording for the six forms (grep -n 'Not tested/not performed' returns a hit in the comment); test name no longer claims 'exactly' unless the pinned set is cited verbatim; the silent pins at test_flags_pass.py:196 and :298-299 match whichever reading Chris records."},
  {"severity": "minor",
   "title": "'Waddell testing' and 'Waddell tests' negations now flag (silent at r5); 'Waddell signs not performed.' stays silent, so the same negation flags or not depending on the noun",
   "evidence": "Silent at 0f58181, flag at 81aa55e: 'Waddell testing not performed.' (N01) and 'Waddell testing not done.' (N02) in artifacts/review-evidence/T-092-claims-adjuster-probe-on-0f58181.out.txt:2-3 vs artifacts/review-evidence/T-092-claims-adjuster-probe.out.txt:2-4; also 'Waddell tests not performed.' (X03, probe-on-0f58181 line 16 silent vs probe line 18 flag) and 'Waddell testing not tested.' (X05, line 18 silent vs line 21 flag). Still silent at 81aa55e: 'Waddell signs not performed.' (X04, probe line 20). Pinned flag at tests/unit/test_flags_pass.py:292-294.",
   "why_it_matters": "Coordinator premise checked: these were not flagged at r5 and flag now; the change is silent to flag, not flag again. Under the literal D-043 text ('Not tested/not performed.' names no 'Waddell testing' subject) a non-listed sentence flags, so this flag is what fail-toward-flagging requires. If Chris reads the form as any subject, these sentences must be silent, and the error is an extra click, not a lost fact. The noun-dependent split (signs silent, testing flag) matches no stated rule, so it is not defensible either way. Rated minor, not blocker, not major: no second clause, no contrast word, and no credibility fact is hidden on the flag side.",
   "fix": "Chris rules the reading (questions_for_chris 1). Then apply one rule to 'signs', 'testing' and 'tests' alike, and pin it. Do not change the code before the ruling.",
   "acceptance_test": "Probe rows N01, N02, X03, X04, X05 print the same state for the same negation across the nouns (signs, testing, tests); tests/unit/test_flags_pass.py:292-299 pins that state, with a D-043 citation in the test docstring."}
 ],
 "whats_right": [
  "Merge fix holds: when a model causation quote overlaps a credibility sentence, the merged flag keeps the whole period sentence and evidence text and offsets equal the excerpt (N03, N04, r5 F01 and F02 at 81aa55e: excerpt 'Straight leg raise positive; Waddell signs negative.', origin both; flags.py:139-140; test_flags_pass.py:302-312).",
  "Hedge fix holds: a credibility flag quotes only its own sentence beside hedge neighbours (r5 D01-D03, N05, N06; flags.py:93-94; tests at :315-320); the hedge run stays for other categories by design (flags.py:94 else branch).",
  "The allow-list is a strict subset of r5's (no new silent misses): all ten r5 C-forms now flag, the r5 corpus counted rows give mismatches=0 (28 rows), and test_flags_pass.py is 32 passed on both the archive and the live tree."
 ],
 "questions_for_chris": [
  "Does D-043's 'Not tested/not performed.' cover any subject, or only the 'Waddell signs' form that the code silences? The answer decides finding 1 (the silent B04/B05 pins) and finding 2 (the flagged 'Waddell testing' forms). Note the coded split: 'Waddell signs not performed.' is silent, 'Waddell testing not performed.' flags.",
  "Is D-043's parenthetical the exhaustive allow-list? Carried from T-067 r5 question 2. If yes, the silent 'Waddell signs not tested/performed' forms are a literal D-043 violation on the silence side. I rate them minor on the same basis as r5 (clean negations, no second clause), so a yes changes the comment's accuracy, not the severity.",
  "Carried from T-067 r5 question 1: D-030 or D-043 governs the excerpt when a model quote overlaps a credibility sentence? 81aa55e chose D-043 (flags.py:137-140). Should that be recorded in D-043 or a SCOPE_CUTS row?",
  "Carried from T-067 r5 question 3: should abbreviation periods ('pt.', 'Lt.') end a sentence? sentences.py is untouched by 81aa55e; E01-E03 are still silent and E04 flags (T-092-claims-adjuster-r5rerun.out.txt:63-66).",
  "Out of this card's AC, but in my lens: the merged flag takes the lexicon category (credibility_language) and drops the model's speculative_language label (artifacts/review-evidence/T-092-claims-adjuster-probe2.out.txt). This predates 81aa55e (r5 identical). Is that the intended behaviour, or should the model's category be shown?"
 ]}
```
