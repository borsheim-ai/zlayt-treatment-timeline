# T-067 round 3 claims-adjuster review (commit b05a8f3)

Reviewer: claims-adjuster-reviewer (Gary Pruitt persona), model claude-haiku-5-5. Rule: D-038 (memory/ORCHESTRATOR_DECISIONS.md:46) and the orchestrator's rule that unsure cases flag.
Scope: HEAD is b05a8f3; product files are identical to HEAD (no uncommitted change to the T-067 files). Function-level review through `credibility.scan` and `flags.run_flag_pass`. No app server or sample case was run, because this card is a function change.

**Verdict: fail.** Two blockers, three majors, two minors.

The brief asked for four confirmations. Results:

| Brief check | Result |
| --- | --- |
| Mixed-side Waddell sentences flag in either word order | **Not confirmed.** Term-first forms flag (M01-M03, M06, M08-M12, P05). Forms that name the positive result before the Waddell term are silent (M04, P01, P02, P04). Those four flagged at f6fa2dd, so b05a8f3 traded one mixed-side silence for another. Blocker 1. |
| "not done/performed" stays silent | Confirmed for the listed forms (D01-D06). Synonyms outside the closed verb list still flag (D07, D08): minor 1. |
| Clean negations stay silent ("no Waddell signs", "0/5 Waddell", "effort consistent") | Confirmed for C01-C07, C10, C11. Not for "Negative Waddell signs." (C08) or "Waddell signs: no positive findings." (X14): major 1. |
| The variants flag | Confirmed for V01-V09. Missed: "Effort was not consistent across trials." (X01): blocker 2. Bare "pain behaviors" flagged at 59c7edb and is silent since f6fa2dd (E13): major 2. |

## Exercised

- `git rev-parse --short HEAD` printed `b05a8f3`. `git status --short -- app/backend/credibility.py app/backend/flags.py app/backend/flag_templates.py app/backend/lexicon_scan.py app/backend/sentences.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py` printed nothing. `git diff --stat b05a8f3 HEAD -- app tests | tail -3` printed nothing.
- `git show --stat b05a8f3` (2 files: credibility.py, test_flags_pass.py). `git show b05a8f3:app/backend/credibility.py | cat -n` (82 lines, read in full). `git show b05a8f3 -- tests/unit/test_flags_pass.py` (the two new tests, lines 241-262).
- `git archive b05a8f3`, `59c7edb`, `f6fa2dd` each extracted into a scratchpad directory (`t067r3`, `t067_59c7edb`, `t067_f6fa2dd`) for the round comparison.
- `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider` on the live tree printed `28 passed in 0.42s`.
- `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py tests/unit/test_flag_templates.py -p no:cacheprovider` printed `67 passed in 0.55s`.
- Wrote `artifacts/review-evidence/T-067-claims-adjuster-r3-probe.py` (60 rows: 12 mixed-side, 6 post-term negation, 6 clean negation, 9 brief variants, 14 own near-miss probes, 6 positive-before-term probes). Ran `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r3-probe.py <tree>` on the b05a8f3 archive and on the live tree: both print `rows=60 mismatches=9`, and the same nine rows (M04, M07, X01, X13, X14, P01, P02, P03, P04) are reported.
- Ran the same probe on the f6fa2dd and 59c7edb archives to compare the rows across rounds (quoted below).
- Re-ran the two r1 probes on the b05a8f3 archive: `artifacts/review-evidence/T-067-claims-adjuster-probe.py` prints `TOTAL cases=30 mismatches=1` (E13, bare pain behaviors); `T-067-claims-adjuster-recall-probe.py` shows the four named-family rows as FLAG.
- Ran `$S/r3_rootcause.py` and `$S/r3_acceptance_strings.py` with `-I` on the b05a8f3 archive (outputs quoted in the findings).
- Read `app/backend/sentences.py:1-40` (';' is a unit boundary at line 35), `app/llm/lexicon.yaml:1159-1169`, `memory/ORCHESTRATOR_DECISIONS.md` D-032/D-038/D-040, and the r1 and r2 review files in full.
- `grep -rn -i "pain behavio" memory/` returned no decision record for the bare pain-behavior narrowing.
- Not exercised: the sample case in the app, and the eval harness (outside this card's function scope).

## Probe evidence (verbatim, b05a8f3 archive unless marked)

```
M04 want=flag  got=none n=0 ... :: Positive Waddell signs on the left, negative on the right.
P01 want=flag  got=none n=0 ... :: Positive Waddell signs on the left but negative on the right.
P02 want=flag  got=none n=0 ... :: Positive Waddell testing on the left, negative on the right.
P04 want=flag  got=none n=0 ... :: Abnormal Waddell signs on the left, negative on the right.
   same four rows at f6fa2dd: got=flag n=1
M05 want=flag  got=flag  :: Negative Waddell signs on the left, positive on the right.   (control, flags)
P05 want=flag  got=flag  :: Waddell signs positive on the left, negative on the right.   (control, flags)
X01 want=flag  got=none n=0 ... :: Effort was not consistent across trials.
E13 (r1 probe) want=flag  got=none ... :: Patient exhibits pain behaviors during examination.
   59c7edb: E13 OK (flag); f6fa2dd: E13 MISMATCH (none); b05a8f3: E13 MISMATCH (none)
C08 want=none(judge) got=flag n=1 excerpt='Negative Waddell signs.'      (f6fa2dd: flag too)
X14 want=none  got=flag n=1 excerpt='Waddell signs: no positive findings.'   (f6fa2dd: none)
X04 judge      got=none :: Waddell signs negative or equivocal.
X03            got=flag excerpt='Waddell signs' :: Waddell signs inconclusive.
M07 excerpt='Waddell signs positive on the right;'   (whole_sentence=False)
X13 excerpt='Subjective complaints out of proportion to exam findings;'   (whole_sentence=False)
P03 excerpt='Positive Waddell signs on the left;'   (whole_sentence=False)
D07 got=flag :: Waddell testing was not conducted.      D08 got=flag :: Waddell signs were not repeated.
```

Root-cause probe on b05a8f3 (`-I`, scan output):
```
'Positive Waddell signs on the left, negative on the right.' scan-> []
'Waddell signs positive on the right; negative on the left.' scan-> ['Waddell signs']  units-> ['Waddell signs positive on the right;', 'negative on the left.']
'Negative Waddell signs.' scan-> ['Waddell signs']
```

Acceptance-string probe on b05a8f3 (`-I`, scan output):
```
'Negative Waddell signs on the left, negative on the right.' -> []
'No Waddell signs on the left, negative on the right.' -> []
'Effort was not inconsistent.' -> []
'Effort was consistent across trials.' -> []
'Effort is not consistent on grip.' -> []
'Effort was not consistent across trials.' -> []
'Waddell signs negative or equivocal.' -> []
'Waddell signs inconclusive.' -> ['Waddell signs']
```

## Findings

**Blocker 1. A positive result named before the Waddell term is dropped (regression from f6fa2dd).** `credibility.py:38-40` builds the result segments only from the matched term and the text after it, so "Positive" or "Abnormal" in front of the term never reaches `_has_positive` (line 43-44). Then `_waddell_negative` (lines 52-56) finds "negative on the right" and silences the hit. The commit's test (`test_d038_mixed_result_waddell_sentence_flags_in_either_order`, tests/unit/test_flags_pass.py:241-253) lists only term-first forms, so the regression is not caught. This is the r2 blocker-1 class ("mixed result drops its positive side") in a form the brief names.

**Blocker 2. "Effort was not consistent across trials." is silent.** `credibility.py:20` and `:22` match only the adjectives inconsistent, sub-maximal, variable, poor. "not consistent" matches none, so the family term is absent from the flags. The same IME claim is flagged as V02 ("Effort was inconsistent across repeated trials."). Under the unsure-flags rule this is a flag. The sentence is not a clean negation of the credibility claim: it is the claim.

**Major 1. Clean negatives flag: "Negative Waddell signs." (C08) and "Waddell signs: no positive findings." (X14).** `credibility.py:52-56` reads negation only after the term, so a leading "Negative" is never read; `_NEG_CUE` at line 31 has no "no" alone. X14 is a regression: it was silent at f6fa2dd. The direction is the safe one and the template is neutral, so this is not a factual error. It is a D-032 breach for a normal result, and the brief lists the clean-negation form as a silent case.

**Major 2. "Waddell signs negative or equivocal." is silent, while "Waddell signs inconclusive." flags.** `credibility.py:52-56` lets any one negative segment silence the hit, and "equivocal" is not treated as unsure (`_POS_CUE` line 33). Under the unsure-flags rule the paralegal should see this. Question for Chris below on whether "equivocal" counts as unsure.

**Major 3. Bare "pain behaviors" stopped flagging after f6fa2dd, with no decision record.** The probe row E13 flagged at 59c7edb and is silent at f6fa2dd and b05a8f3. The lexicon still names pain behaviours in the symptom_magnification pattern (`app/llm/lexicon.yaml:1160`, rationale: "A credibility attack"). The credibility.py docstring (line 2) now says bare "pain behavior" is a neutral descriptor, but no entry in memory/DECISIONS.md or memory/ORCHESTRATOR_DECISIONS.md records it, and D-038 says the family comes "from the lexicon". Major rather than blocker because the narrowing is deliberate in the code, so it may be a decision that Chris makes. If the decision is to keep it neutral, it must be recorded. If not, it should flag.

**Minor 1. Synonyms of "not done" still flag.** "Waddell testing was not conducted." (D07), "Waddell signs were not repeated." (D08) and "Possible symptom magnification, ruled out later." (X09) flag because `_DONE` (credibility.py:29) is a closed verb list. This is the over-flag direction. Minor because the r2 major asked for the post-term tail, and the r3 list closes the verbs it names.

**Minor 2. The flag excerpt is cut at a semicolon.** `app/backend/sentences.py:35` ends a unit at ';' (shared splitter, ADR-016). M07 shows the excerpt "Waddell signs positive on the right;", X13 "Subjective complaints out of proportion to exam findings;", P03 "Positive Waddell signs on the left;". Each excerpt is verbatim, so no text is invented, but the second clause is not on the flag. The whole-sentence excerpt that r1 asked for does not hold for semicolon sentences. Cross-boundary: sentences.py is not a T-067 file.

Not findings (noted for completeness): "Waddell signs negative, straight leg raise positive." flags on the non-Waddell positive (over-flag, safe direction, D-038 unsure rule); "Positive Waddell signs on the left, not on the right." flags.

## Scores

Scores are on a 1-5 scale against the brief's four checks and the r1 criteria.

## Whats right

- Term-first mixed-side sentences flag in both orders with the whole-sentence excerpt: M01, M02, M03, M06, M08-M12, P05.
- The listed not-done and clean-negation forms are silent: D01-D06, C01-C07, C10, C11, X08. "Malingering ruled out." (C09) is silent.
- The brief's family variants flag with the whole sentence: V01-V09, and "Waddell signs inconclusive." (X03) flags.

## Questions for Chris

1. Should "equivocal" (and "unclear", "inconclusive", "possible") count as unsure, so a "negative or equivocal" Waddell result flags? My reading of the unsure-flags rule says yes (major 2).
2. Is bare "pain behavior" a neutral descriptor by decision? If yes, record it in D-038 and a test; if no, restore it (major 3).
3. Should a semicolon end the credibility excerpt, or should the flag show the containing sentence? The shared splitter is an ADR-016 decision (minor 2).

```json
{"card": "T-067", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit b05a8f3 (HEAD; product files identical to HEAD); git archive copies of b05a8f3, f6fa2dd and 59c7edb in the session scratchpad for the round comparison; live tree; function-level probes through credibility.scan and flags.run_flag_pass with FakeCall; no app URL and no sample case run",
 "exercised": [
   "read personas/claims-adjuster.md in full; read memory/ORCHESTRATOR_DECISIONS.md D-032, D-038, D-040 by grep; read the r1 and r2 review files in full",
   "git rev-parse --short HEAD -> b05a8f3; git status --short on the T-067 product files -> empty; git diff --stat b05a8f3 HEAD -- app tests -> empty",
   "git show --stat b05a8f3; git show b05a8f3:app/backend/credibility.py | cat -n (82 lines); git show b05a8f3 -- tests/unit/test_flags_pass.py",
   "git archive b05a8f3, f6fa2dd and 59c7edb extracted to scratchpad copies",
   ".venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider -> 28 passed in 0.42s",
   ".venv/bin/python -m pytest -q tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py tests/unit/test_flag_templates.py -p no:cacheprovider -> 67 passed in 0.55s",
   "artifacts/review-evidence/T-067-claims-adjuster-r3-probe.py (60 rows written this round) via .venv/bin/python -I on b05a8f3 and the live tree -> rows=60 mismatches=9 on both; on f6fa2dd and 59c7edb for the cross-round rows",
   "artifacts/review-evidence/T-067-claims-adjuster-probe.py on b05a8f3 -> TOTAL cases=30 mismatches=1 (E13); T-067-claims-adjuster-recall-probe.py on b05a8f3 -> named-family rows FLAG",
   "scratchpad r3_rootcause.py and r3_acceptance_strings.py via .venv/bin/python -I on b05a8f3",
   "read app/backend/sentences.py:1-40; app/llm/lexicon.yaml:1159-1169; grep -rn -i 'pain behavio' memory/ -> no decision record"
 ],
 "verdict": "fail",
 "scores": {"mixed_result_word_order": 2, "not_done_after_term_silent": 4, "clean_negations_silent": 3, "named_family_variants_flag": 3, "unsure_flags_rule": 2, "whole_sentence_excerpt": 3, "tests_match_claimed_behaviour": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Positive result named before the Waddell term is silent: mixed-side sentence regressed from f6fa2dd",
   "evidence": "probe (-I, b05a8f3 archive): 'M04 want=flag got=none n=0 :: Positive Waddell signs on the left, negative on the right.'; 'P01 got=none :: Positive Waddell signs on the left but negative on the right.'; 'P02 got=none :: Positive Waddell testing on the left, negative on the right.'; 'P04 got=none :: Abnormal Waddell signs on the left, negative on the right.'. Same four rows at f6fa2dd: got=flag n=1. scan at b05a8f3: 'Positive Waddell signs on the left, negative on the right.' -> []. Cause: app/backend/credibility.py:38-40 (_result_segments builds segments from the match and the text after it only, so the leading 'Positive' never reaches _has_positive at :43-44), :52-56 (_waddell_negative silences on 'negative on the right'). Test gap: tests/unit/test_flags_pass.py:241-253 (test_d038_mixed_result_waddell_sentence_flags_in_either_order) lists term-first forms only.",
   "why_it_matters": "The brief requires mixed-side Waddell sentences to flag in either word order. 'Negative Waddell signs on the left, positive on the right.' flags (M05) and 'Positive Waddell signs on the left, negative on the right.' does not, so the flag depends on where the words sit. A positive Waddell result is a credibility finding under D-038. The paralegal loses it with no state or note. No fact is invented, but a credibility flag is dropped, and b05a8f3 introduced the drop (f6fa2dd flagged these rows). Same class as r2 blocker 1.",
   "fix": "Segment the whole sentence unit (unit_start to unit_end), not only the text from the match onward, using the same _SEG_SPLIT. Keep the rule that only a segment-wide negative with no positive cue silences. Add the positive-prefix forms to test_d038_mixed_result_waddell_sentence_flags_in_either_order.",
   "acceptance_test": "Probe rows M04, P01, P02, P04 print flag with the whole-sentence excerpt; M05 and P05 still flag; 'Negative Waddell signs on the left, negative on the right.' and 'No Waddell signs on the left, negative on the right.' stay silent (both silent on b05a8f3 now, keep them so); the new positive-prefix forms are in the test."},
  {"severity": "blocker",
   "title": "'Effort was not consistent across trials.' is silent: a family variant the regex does not match",
   "evidence": "probe X01 want=flag got=none n=0 at b05a8f3 (also none at f6fa2dd and 59c7edb). Cause: app/backend/credibility.py:20 (inconsistent|sub-maximal|variable|poor adjectives only) and :22 (effort ... (?P<adj>inconsistent|sub-maximal|variable)); 'not consistent' matches none of them. Compare V02 'Effort was inconsistent across repeated trials.' -> flag excerpt verbatim.",
   "why_it_matters": "'Effort was not consistent' is the same IME claim as 'effort was inconsistent'. The sentence is the credibility claim, not a negation of it, so under D-038 and the unsure-flags rule the paralegal must see it. The brief's silent 'effort consistent' form is not the same sentence. A hidden credibility phrase in the most common family wording is a blocker under the r2 named-family class.",
   "fix": "Add 'not consistent' (and 'not reliable' if the family list is to be read generously) to the effort adjective alternatives at credibility.py:20 and :22, keeping the double-negative 'effort was not inconsistent' silent.",
   "acceptance_test": "'Effort was not consistent across trials.' and 'Effort is not consistent on grip.' flag with the whole-sentence excerpt; 'Effort was consistent across trials.' and 'Effort was not inconsistent.' stay silent (both silent now, keep them so)."},
  {"severity": "major",
   "title": "Bare 'pain behaviors' stopped flagging after f6fa2dd, and the narrowing is not in any decision record",
   "evidence": "r1 probe row E13 'Patient exhibits pain behaviors during examination.': OK (flag) at 59c7edb; MISMATCH got=none at f6fa2dd and at b05a8f3. Lexicon still names it: app/llm/lexicon.yaml:1160 (symptom_magnification pattern includes pain behaviou?rs?; rationale line 1167 'A credibility attack'). Narrowing only in the docstring at app/backend/credibility.py:2 ('bare \"pain behavior\" is a neutral descriptor and counts only with \"out of proportion\"'). grep -rn -i 'pain behavio' memory/ -> no match.",
   "why_it_matters": "D-038 defines the family as 'defense credibility phrases from the lexicon'. The lexicon names pain behaviours as a credibility term, and the adjuster quotes pain-behaviour wording against the claimant. The code drops it silently from the flags, under the unsure-flags rule it should flag, and the narrowing exists only in a code docstring. Major rather than blocker because the drop is deliberate in code, so the fix may be a recorded decision.",
   "fix": "Either flag bare 'pain behavior(s)' and remove the docstring exception, or record the narrowing as a decision (D-038 addendum or SCOPE_CUTS.md with reason) and add a test that asserts the silence.",
   "acceptance_test": "Probe E13 flags, or memory/ORCHESTRATOR_DECISIONS.md names bare pain behavior as neutral and a test in tests/unit/test_flags_pass.py asserts 'Patient exhibits pain behaviors during examination.' raises nothing."},
  {"severity": "major",
   "title": "Clean negative results flag: 'Negative Waddell signs.' and 'Waddell signs: no positive findings.' (X14 is a regression from f6fa2dd)",
   "evidence": "probe C08 want=none got=flag excerpt='Negative Waddell signs.' (flag at f6fa2dd too); X14 want=none got=flag excerpt='Waddell signs: no positive findings.' (none at f6fa2dd, so b05a8f3 introduced it). Cause: app/backend/credibility.py:52-56 (negation read only after the term; for C08 no segment follows the term, so 'Negative' is never read), :31 (_NEG_CUE has no bare 'no' for 'no positive findings').",
   "why_it_matters": "The brief's silent list is 'no Waddell signs', '0/5 Waddell', 'effort consistent'. 'Negative Waddell signs.' is the reversed form of 'Waddell signs negative.' (silent, C05). D-032 says negative results never flag. Both are over-flags, in the safe direction, and the template is neutral, so no fact is wrong. Major because D-032 is stated as a hard rule and X14 is a regression.",
   "fix": "Read a negative word before the term as well (same unit-wide segment fix as blocker 1). Add 'no positive' / bare 'no' followed by a positive word to the negative-result cues in _waddell_negative.",
   "acceptance_test": "C08 and X14 print none; 'Negative Waddell signs on the left, positive on the right.' still flags; C05 and C10 still silent."},
  {"severity": "major",
   "title": "'Waddell signs negative or equivocal.' is silent while 'Waddell signs inconclusive.' flags",
   "evidence": "probe X04 'Waddell signs negative or equivocal.' -> got=none (b05a8f3); X03 'Waddell signs inconclusive.' -> flag excerpt 'Waddell signs' (b05a8f3). Cause: app/backend/credibility.py:52-56 (any one negative segment silences the hit), :33 (_POS_CUE has no unsure terms).",
   "why_it_matters": "The orchestrator rule is that unsure cases flag. A result the record calls 'negative or equivocal' is not clearly negative, and the code treats the equivocal half as if it were not there. The paralegal then does not see a Waddell result the record does not call negative. Major rather than blocker because the second segment is a qualifier, not a positive finding.",
   "fix": "Add unsure terms (equivocal, unclear, questionable, borderline, possible) to the cues that block silence in _waddell_negative, so any unsure segment keeps the hit.",
   "acceptance_test": "'Waddell signs negative or equivocal.' flags with the whole-sentence excerpt; 'Waddell signs inconclusive.' still flags; 'Waddell signs negative.' and 'No Waddell signs.' stay silent."},
  {"severity": "minor",
   "title": "Synonyms of 'not done' still flag: 'not conducted', 'not repeated', 'ruled out later'",
   "evidence": "probe D07 'Waddell testing was not conducted.' -> flag; D08 'Waddell signs were not repeated.' -> flag; X09 'Possible symptom magnification, ruled out later.' -> flag (all b05a8f3). Cause: app/backend/credibility.py:29-30 (_DONE is a closed verb list).",
   "why_it_matters": "A test that was not conducted is not a credibility finding. These are over-flags in the safe direction, so the paralegal sees an extra flag. Minor because the r2 major asked for the post-term tail, and r3 closes the verbs it names; these are outside the list.",
   "fix": "Widen _DONE or use a generic 'not + past participle' tail, and add a 'ruled out' tail check for post-term negation.",
   "acceptance_test": "D07 and D08 print none, or are listed in SCOPE_CUTS.md with a reason."},
  {"severity": "minor",
   "title": "The flag excerpt is cut at a semicolon, so the second clause is not on the flag",
   "evidence": "probe M07 excerpt='Waddell signs positive on the right;' (whole_sentence=False); X13 excerpt='Subjective complaints out of proportion to exam findings;' (whole_sentence=False); P03 excerpt='Positive Waddell signs on the left;' (whole_sentence=False). Cause: app/backend/sentences.py:35 (';' ends a unit in the shared splitter; module docstring line 5).",
   "why_it_matters": "Each excerpt is verbatim, so no text is invented, but the r1 criterion was a whole-sentence excerpt and the second clause (for example 'negative on the left' in M07) is not shown on the flag. Minor, and cross-boundary because sentences.py is not a T-067 file.",
   "fix": "Decide: the credibility excerpt uses the containing sentence (up to . ? ! or a line break), or record the semicolon split for flag excerpts as a scope cut with a reason.",
   "acceptance_test": "M07 and X13 excerpts equal the whole sentence, or SCOPE_CUTS.md names the semicolon excerpt rule."}
 ],
 "whats_right": [
  "Term-first mixed-side sentences flag in both orders with the whole-sentence excerpt: M01, M02, M03, M06, M08-M12, P05.",
  "The listed not-done and clean-negation forms are silent: 'Waddell testing was not done.', 'Waddell testing was not performed.', 'Malingering was not suspected.', 'No Waddell signs.', '0/5 Waddell.', 'Effort consistent during grip testing.', and 'Malingering ruled out.'.",
  "The brief's family variants flag with the whole sentence (V01-V09), and 'Waddell signs inconclusive.' flags."
 ],
 "questions_for_chris": [
  "Should 'equivocal' (and 'unclear', 'inconclusive', 'possible') count as unsure, so 'negative or equivocal' flags? My reading of the unsure-flags rule says yes (major 'equivocal').",
  "Is bare 'pain behavior' a neutral descriptor by decision? If yes, record it in D-038 with a test; if no, restore it (major 'pain behaviors').",
  "Should a semicolon end the credibility excerpt, or should the flag show the containing sentence? The shared splitter is an ADR-016 decision (minor 'semicolon')."
 ]}
```
