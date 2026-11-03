# T-067 round 2 review (commit f6fa2dd)

**Persona note.** The brief asked for persona `claims-adjuster-reviewer`. I am `staff-engineer-reviewer`, so I did not write the adjuster-lens judgment (whether a phrase reads as defense credibility wording). That judgment needs a fresh claims-adjuster-reviewer dispatch. This file records my engineering probes of the function and its tests, and the JSON `persona` field is `staff-engineer-reviewer`.

**Verdict: fail.** Pinned to f6fa2dd with `git archive` (no change to the T-067 files between f6fa2dd and HEAD b9d3ead).

**Are the r1 blockers closed?**
- Blocker 1 (negated or negative wording raises a flag): closed for the six strings in the brief and for the r1 cases N04, N09, N10, N15. Not closed in general. A mixed-result sentence now drops a positive finding (F1, blocker, new). Post-term negation still flags (F2, major). The r1 harm (the template stated the opposite of the record) is gone because the template is now neutral, so the post-term residual is rated major. That is a deviation from r1's blocker rating, stated here.
- Blocker 2 (named-family variants missed): closed. All four brief variants and the six r1 misses flag, with the whole sentence as the excerpt and `pending` state.

**Probe method.** `credibility.scan` directly, and `flags.run_flag_pass` with `tests.unit._fakes.FakeCall` (the production path, as the tests use it). Output below is verbatim from the pinned copy.

```
Brief negated (must be silent): all six silent
  'Waddell signs negative.' / 'No Waddell signs.' / '0/5 Waddell' / 'Effort consistent during grip testing.' / 'No symptom magnification.' / 'Pain is not out of proportion to the injury.'
Brief variants (must flag): all four FLAG
  'Effort is inconsistent.' ['Effort is inconsistent'] / 'Submaximal effort noted.' ['Submaximal effort'] / 'Magnifying symptoms noted.' ['Magnifying symptoms'] / 'Pain behavior out of proportion to the injury.' ['out of proportion']
Own probes, mismatches only:
  MISMATCH 'Waddell signs negative on the left but positive on the right.' -> silent []
  MISMATCH 'Waddell testing was not performed.' -> FLAG ['Waddell testing']
run_flag_pass:
  silent 'Waddell signs negative on the left, positive on the right.'
  silent 'Waddell signs negative on the left but positive on the right.'
  FLAG   'Waddell signs positive on the right and negative on the left.'  [pending]
  FLAG   'Waddell testing was not done.'  [pending]
  FLAG   'Malingering was not suspected.'  [pending]
  silent 'Waddell signs negative on the left and negative on the right.'
```

```json
{"card": "T-067", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f6fa2dd (app/backend/credibility.py, flags.py, flag_templates.py, tests/unit/test_flags_pass.py); pinned via git archive; HEAD during review b9d3ead (no T-067 file changes since f6fa2dd); no app URL; function-level probes, no sample case run",
 "exercised": [
   "reviews/T-067-claims-adjuster.md read in full (r1 blockers, findings, JSON)",
   "git show --stat f6fa2dd; git diff --stat f6fa2dd HEAD -- app/backend/credibility.py app/backend/flags.py app/backend/flag_templates.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py tests/unit/ (empty: no drift)",
   "git archive f6fa2dd | tar -x -C <scratchpad>/t067",
   "Read app/backend/credibility.py (57 lines), flags.py:88 (hits += credibility.scan), flag_templates.py:133 (neutral template), tests/unit/test_flags_pass.py:168-240, tests/unit/_fakes.py",
   "scratchpad probe_t067.py: credibility.scan on the 6 brief negated strings, 4 brief variants, 12 own strings; 2 mismatches (mixed-result sentence; 'Waddell testing was not performed.')",
   "scratchpad probe2_t067.py: 12 more own strings; 3 mismatches ('3/5 Waddell.' silent; 'Malingering was not suspected.' flags; 'Waddell testing was not done.' flags) plus the mixed-result sentence",
   "scratchpad probe3_t067.py: flags.run_flag_pass with tests.unit._fakes.FakeCall on 6 sentences (mixed order, post-term negation, negated both sides)",
   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit/test_flags*.py tests/unit/test_flag_templates.py -q at f6fa2dd: 74 passed (test_flags*.py alone: 48)",
   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit -q at f6fa2dd: 2 failed (test_e2e_contract x2, untouched by T-067), 947 passed",
   "Mutants in scratch copy (credibility.py restored and cmp-identical to f6fa2dd after each): Waddell negative check off -> 2 failed, 46 passed; negated() guard off -> 2 failed, 46 passed",
   "Not exercised: claims-adjuster probe artifacts under artifacts/review-evidence/ and the adjuster-lens wording judgment (outside my lens)"
 ],
 "verdict": "fail",
 "scores": {"negation_handling": 2, "named_family_recall": 4, "mixed_result_handling": 1, "test_non_vacuous": 5, "neutral_template": 5, "no_network_in_tests": 5},
 "findings": [
   {"severity": "blocker",
    "title": "Mixed-result Waddell sentence drops its positive side, and the result depends on word order",
    "evidence": "run_flag_pass at f6fa2dd: 'Waddell signs negative on the left, positive on the right.' -> silent; 'Waddell signs negative on the left but positive on the right.' -> silent; 'Waddell signs positive on the right and negative on the left.' -> FLAG (excerpt verbatim, pending). Cause: app/backend/credibility.py:35 `clause = re.split(r\"[,;.\\n]\", text[m.end():], maxsplit=1)[0]` keeps only the first clause; line 36 `return bool(_NEG_RESULT.match(clause))` tests only the leading words (_NEG_RESULT, lines 24-25), so 'positive on the right' is never read; line 49-50 suppresses the hit on that result.",
    "why_it_matters": "This is a new under-flag, not the r1 over-flag. D-038 says these credibility phrases are what the paralegal must see first, and the card AC 1 requires credibility phrases to raise a flag. A Waddell sign that is positive on one side is removed from the flags because the sentence starts with 'negative'. The same two results flip with word order. The source sentence stays in the record, so no fact is invented, but a credibility finding is lost without any state or note. Whether a mixed result should flag is a claims-adjuster question (see questions_for_chris); the silent drop of the positive side is an engineering defect either way.",
    "fix": "Judge a Waddell result per result, not per prefix. Split the clause at conjunctive and contrastive cues ('but', 'and', 'while', 'on the other hand', 'however', as well as the existing separators), and treat the hit as negative only when every result segment is negative. Equivalently: suppress only when no segment contains a positive cue ('positive', 'present', 'abnormal', 'pos').",
    "acceptance_test": "tests/unit/test_flags_pass.py: 'Waddell signs negative on the left, positive on the right.' and 'Waddell signs negative on the left but positive on the right.' each raise one credibility_language flag whose excerpt is the whole sentence; 'Waddell signs negative on the left and negative on the right.' raises nothing; the reversed-order sentence keeps flagging."},
   {"severity": "major",
    "title": "Negation after the term still raises a credibility flag (residual of r1 blocker 1)",
    "evidence": "run_flag_pass at f6fa2dd: 'Waddell testing was not done.' -> FLAG (pending); 'Malingering was not suspected.' -> FLAG (pending); 'Waddell testing was not performed.' -> FLAG (scan). The negated-wording test list (tests/unit/test_flags_pass.py:206-216) covers 'was negative', 'not present', 'none', '0/5', 'No ...', and 'Symptom magnification was ruled out.', but not 'not done', 'not performed' or 'not suspected' after the term. credibility.py:24-25 (_NEG_RESULT) and credibility.py:51 (lexicon_scan.negated, which looks before the match) do not cover a negation that follows the term.",
    "why_it_matters": "r1 blocker 1 said negated wording must not raise a credibility flag, and the card claims that is closed. Rated major, not blocker, because the template is now neutral ('Wording in X that uses a credibility term: <quote>.', flag_templates.py:133), so the flag no longer asserts the opposite of the record. The paralegal still sees a credibility-term flag for a test that was not done. This deviates from r1's blocker rating, and the reason is stated here.",
    "fix": "Add a post-term negation check in credibility.py, for example a tail after the match of the form (was|were|is|are) (not|never) (done|performed|tested|suspected|elicited|present|identified|seen), and treat a match with that tail as negated.",
    "acceptance_test": "_cred('Waddell testing was not done.') == [], _cred('Malingering was not suspected.') == [], _cred('Waddell testing was not performed.') == [], added to test_d038_negative_or_negated_credibility_wording_raises_nothing; the existing list still passes."},
   {"severity": "minor",
    "title": "Count-first positive Waddell result is silent",
    "evidence": "credibility.scan('3/5 Waddell.') -> [] (probe2). credibility.py:11-12 `_WADDELL` requires a trailing result word (signs, testing, positive, ...), so a bare count-first sentence matches no pattern. The brief's '0/5 Waddell' is silent for that same reason (no match), not because negation was applied, so the negated-list test passes for the wrong reason.",
    "why_it_matters": "A positive count written before the name is a credibility-phrase variant that the family does not cover. Minor because the forms r1 named ('Waddell 3 of 5 positive', '3/5 Waddell signs positive', 'Waddell testing positive') are covered.",
    "fix": "Add a count-first alternative to _WADDELL, for example r'\\d+\\s*(?:/|of)\\s*\\d+\\s+Waddell\\b', keeping the existing zero-count check so '0/5 Waddell.' stays silent for a negation reason.",
    "acceptance_test": "credibility.scan('3/5 Waddell.') flags with excerpt '3/5 Waddell'; credibility.scan('0/5 Waddell.') stays [] and the test asserts the negative-count branch was taken."}
 ],
 "whats_right": [
   "Named-family recall is closed: the brief variants and the six r1 misses flag with whole-sentence excerpts and pending state (probe 1, probe3, tests test_d038_family_variants_flag_with_the_sentence_excerpt).",
   "The negation guard is non-vacuous: disabling either the Waddell negative-result check or the lexicon negated() guard makes two flag tests fail.",
   "The credibility template is neutral (no 'defense', no 'questions'), and tests/unit/test_flags*.py run with the fake call, with no network."
 ],
 "questions_for_chris": [
   "Should a sentence that reports one side negative and the other positive ('negative on the left, positive on the right') raise a credibility flag? I assume yes, because the positive side is a credibility finding under D-038. This is a clinical and adjuster-meaning call, so the claims-adjuster reviewer should confirm; it is not blocking the engineering fix."
 ]}
```
