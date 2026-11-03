# T-067 round 5 claims-adjuster review (commit 0f58181, D-043)

Reviewer: claims-adjuster-reviewer (Gary Pruitt persona), model claude-haiku-5-5 (the model I am running as).
Binding rule: D-043 (memory/ORCHESTRATOR_DECISIONS.md:51), with the period-delimited sentence as the unit; ';' and line breaks are clause separators.
Scope: commit 0f58181, extracted with `git archive` into the session scratchpad. The live tree has uncommitted flags.py edits from another card; the probes ran on the archive.

## Answers to the three checks

- **"Straight leg raise positive; Waddell signs negative." flags, and line-break variants flag.** Yes. A01 to A16 flag, including LF, CRLF, CR, LS, blank-line and no-space variants (`artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt:2-33`).
- **The flag excerpt is the whole period sentence, verbatim and grounded.** Yes on the lexicon path (verbatim=True, whole_sentence=True for every single-sentence row). Two exceptions: a hedge neighbour is quoted into the excerpt (D01, minor), and a model flag that overlaps the sentence replaces the excerpt with a clause (F01, major).
- **The allow-list equals D-043's list.** No. Nine silent forms are not among the six D-043 literal forms (C01 to C10). The r5 handoff says the list was trimmed to D-043 forms only; it was not fully trimmed.

## Summary

**Verdict: changes.** No blocker. One major, two minor.

- **major**: the merge path (flags.py:127, :134) overwrites a credibility flag's whole-sentence excerpt with a model clause when a causation flag overlaps the sentence (F01). Same defect class as r4 F2, on a second path.
- **minor**: the allow-list still silences nine forms the D-043 literal list does not name, carried from r4 F3. The r4 F3 finding is partly closed, not closed.
- **minor**: a hedge sentence pulls a neighbouring hedge sentence into the excerpt (D01).

Re-run of the attack corpus: the r4 probe (139 rows, which carries the r1, r2, r3 and r4 strings) gives mismatches=0 on 0f58181. The r1, r3 and recall probe literals are all in that corpus; the r2 and r3 prose strings that were missing are in probe section G, and all pass.

Tests: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider` gives 30 passed on the live tree and 30 passed on the archive.

## Exercised

- `python3 tools/board.py show T-067`; `git log -8`; `git show --stat 0f58181`; `git diff 0f58181 -- app/backend/credibility.py app/backend/sentences.py tests/unit/test_flags_pass.py` (empty).
- D-043 (line 51), D-030 (line 38), D-038 (line 46), read verbatim; r4 review read in full.
- `git archive 0f58181 | tar -x` into the scratchpad; `pytest` on the archive and the live tree (30 passed each).
- `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py <archive>` gives rows=139 mismatches=0 (saved as `artifacts/review-evidence/T-067-claims-adjuster-r5-r4corpus.out.txt`).
- `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r5-probe.py <archive> artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt` gives counted rows 28, mismatches=0; the excerpt and superset rows are reported in the output file.
- `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r5-corpus-check.py /Users/arsis/zlayt-pm-project` for the earlier-review string coverage.
- Printed `credibility._CLEAN.pattern` and compared it against the six D-043 forms.
- Committed line numbers were grepped on the archive, not the dirty live tree.
- Not exercised: the eval harness, the app server and the sample case (outside this function-level card; the AC2 golden claim is outside my lens).

## Findings

Details are in the JSON block. Verdict by rule: no blocker, one major, so `changes`.

- **major** (F01): merge overrides the whole-sentence excerpt with a model clause (flags.py:127, :134; probe F01 at out.txt:69-70).
- **minor** (C01 to C10): allow-list wider than D-043's six forms; credibility.py:28 comment and the r5 handoff say otherwise; test pins at tests/unit/test_flags_pass.py:210.
- **minor** (D01): hedge run quotes a neighbour sentence (flags.py:64-76 via :93; out.txt:55-56).

Questions for Chris are in the JSON block: which decision governs an overlapping model quote (D-030 or D-043), whether D-043's list is exhaustive (which decides whether the allow-list is blocker or minor), and whether abbreviation periods such as 'pt.' end a sentence.

```json
{"card": "T-067", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 0f58181 (T-067 r5, D-043), extracted with git archive into the session scratchpad (t067r5); credibility.py, sentences.py and tests/unit/test_flags_pass.py are identical to the commit (git diff empty on the live tree); the live tree has uncommitted app/backend/flags.py edits from another card, not probed; function-level probes through flags.run_flag_pass with FakeCall; no app URL, no sample case, no eval harness run",
 "exercised": [
   "python3 tools/board.py show T-067 (status in_review, rounds 4, handoff line 78 claims 'Allow-list trimmed to D-043 forms only'); git log -8; git show --stat 0f58181",
   "git diff 0f58181 -- app/backend/credibility.py app/backend/sentences.py tests/unit/test_flags_pass.py -> empty",
   "memory/ORCHESTRATOR_DECISIONS.md D-043 (line 51), D-030 (line 38), D-038 (line 46) read verbatim",
   "reviews/T-067-claims-adjuster-r4.md read in full (F1 blocker, F2 major, F3 minor, the 139-row corpus); r1, r2, r3 review files checked for attack strings with artifacts/review-evidence/T-067-claims-adjuster-r5-corpus-check.py (.venv/bin/python -I): r1 probe, r3 probe and recall probe literals are all in the r4 corpus; only format strings are absent; r2 and r3 prose strings checked, the missing ones added as probe section G",
   "git archive 0f58181 | tar -x -C <scratchpad>/t067r5",
   "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider -> live tree: 30 passed in 0.64s; archive: 30 passed in 0.51s",
   ".venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py <archive> -> rows=139 mismatches=0 [] (output artifacts/review-evidence/T-067-claims-adjuster-r5-r4corpus.out.txt); O01, O03, O04 now flag with whole-sentence excerpts; O02 (line break) now flags; B03, B05, C02, C08 now flag",
   ".venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r5-probe.py <archive> artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt -> counted rows A+B 28, mismatches=0; A01-A16 (';', LF, CRLF, CR, LS, blank line, no-space variants) flag with verbatim whole-sentence excerpts; B01-B05 silent; C01-C10 (superset forms); D01-D03 (hedge neighbours); E01-E04 (abbreviation periods); F01-F02 (LLM overlap, merge); G01-G07 (earlier-review strings)",
   "print of credibility._CLEAN.pattern on the archive (allow-list regex) compared against the six D-043 literal forms",
   "grep -n of committed line numbers (credibility.py 4, 28-35, 43-57; sentences.py 10, 35, 37; flags.py 64-76, 93, 111, 127, 134; tests/unit/test_flags_pass.py 206-210) run against the archive, not the dirty live tree",
   "not exercised: eval harness (LLM_BACKEND=fixture python -m evals.run), app server, sample case; the card AC2 golden claim is outside my lens"
 ],
 "verdict": "changes",
 "scores": {"d043_second_clause_flags": 5, "d043_allow_list_equals_d043_list": 2, "lexicon_path_excerpt_is_whole_sentence": 4, "merge_path_excerpt_is_whole_sentence": 2, "verbatim_and_grounded": 5, "prior_attack_strings_regression": 5, "commit_suite_green": 5},
 "findings": [
  {"severity": "major",
   "title": "A model flag that overlaps a credibility sentence replaces the whole-sentence excerpt with its clause (merge override)",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt:69-70: 'F01 llm_excerpt=\"Waddell signs negative.\" -> credibility flags=1' then '      excerpt=\"Waddell signs negative.\" origin=both whole_sentence=False' (input 'Straight leg raise positive; Waddell signs negative.'). Cause at commit 0f58181: app/backend/flags.py:127 (merge matches on flag type and span overlap, not on category) and app/backend/flags.py:134 (lx[\"excerpt\"] = uniq[match][\"excerpt\"]). F02 (LLM quotes the full sentence) keeps the whole sentence, so the defect is the clause quote only.",
   "why_it_matters": "credibility.py:4 and D-043 say the flag excerpt is the whole period sentence, so the paralegal sees the second clause. When flags_v1 returns a causation flag that overlaps a credibility sentence, the merge overwrites the code's whole-sentence excerpt with the model's clause, and the positive side ('Straight leg raise positive;') drops off the flag. This is the r4 F2 defect (major) on a second path. The quote is verbatim, so no fact is invented, and the flag still exists, so it is not a blocker. Reachable in the claude-cli dev backend, where the flags step is live; the fixture backend never reaches it, which is why the r5 suite and evals do not show it.",
   "fix": "In merge, when the lexicon flag's category is credibility_language, keep the lexicon whole-sentence excerpt and span (skip flags.py:134 and the evidence rewrite for that category), or record in D-043 that a model quote may replace the credibility excerpt, with a SCOPE_CUTS row. Chris decides which decision governs (see questions_for_chris).",
   "acceptance_test": "Probe F01 prints excerpt == 'Straight leg raise positive; Waddell signs negative.' with origin both; a tests/unit/test_flags_pass.py case runs run_flag_pass with FakeCall({'flags': {'flags': [causation flag quoting 'Waddell signs negative.']}}) and asserts the credibility flag's excerpt is the whole sentence."},
  {"severity": "minor",
   "title": "The allow-list still silences nine forms that the six D-043 literal forms do not name; the r5 handoff says it is trimmed to D-043 forms only",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt:43-52 (C01-C10: 'Waddell testing was not done.', 'No Waddell testing.', 'Waddell testing negative.', 'Waddell signs were not performed.', 'Waddell signs not done.', 'No Waddell criteria.', '0 / 5 Waddell signs.', 'Waddell signs: negative.', 'Waddell testing: not performed.' all silent) and line 92 (superset count 9). credibility.py:28 says the list is 'exactly the decision's forms'; credibility.py:29-35 (_CLEAN) allows done, (was|were), testing|tests|criteria|findings, a colon and '0 / 5'. tests/unit/test_flags_pass.py:210 pins 'Waddell testing was not done.' and 'Waddell testing: not performed.' as silent. board/cards/T-067.md:78 handoff: 'Allow-list trimmed to D-043 forms only'. Inconsistent within the code: C09 'Waddell signs were negative.' flags while C04 'Waddell signs were not performed.' is silent.",
   "why_it_matters": "D-043 (memory/ORCHESTRATOR_DECISIONS.md:51) says a credibility sentence flags unless it is wholly one of the listed forms. A silent 'Waddell testing was not done.' is a clean negative, so no credibility fact is hidden and this stays minor, as r4 F3 rated it. But the code comment and the handoff say the list matches D-043, and it does not. The r4 F3 finding is only partly closed: the three r4 examples now flag, and the 'done', '(was|were)' and noun forms still do not match D-043.",
   "fix": "Narrow _CLEAN (credibility.py:29-35) to the six D-043 literal forms (drop 'done', '(was|were)', the testing/tests/criteria/findings nouns outside 'Waddell signs', the colon and the '0 / 5' spacing), and update the pinned silent list at tests/unit/test_flags_pass.py:206-212; or Chris adds the full list to D-043 and the test pins it. Correct the comment at credibility.py:28 either way.",
   "acceptance_test": "Probe rows C01-C08 print flag; B01-B03 stay silent; tests/unit/test_flags_pass.py asserts silence only for the six D-043 forms (or for the forms recorded in D-043)."},
  {"severity": "minor",
   "title": "Hedge run quotes a neighbouring sentence into a credibility flag excerpt",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-r5-probe.out.txt:55-56: 'D01 :: Findings may represent degenerative change. Possible symptom magnification noted.' then 'excerpt=\"Findings may represent degenerative change. Possible symptom magnification noted.\" whole_sentence=False'. Cause: app/backend/flags.py:93 calls _hedge_run; app/backend/flags.py:64-76 expands the span through adjacent hedge units when the credibility sentence is itself a single splitter unit (grounding.py:83 is_hedge_unit). D02 ('Waddell signs negative. Possible symptom magnification noted.') quotes only the flagged sentence.",
   "why_it_matters": "The r5 handoff says the flag excerpt is the whole period sentence. For a hedge-worded credibility sentence it is the flagged sentence plus the neighbouring hedge sentence. Verbatim and not invented, so minor; but it puts a degenerative-change sentence inside a credibility flag.",
   "fix": "Exempt credibility_language hits from _hedge_run (their span is already the whole sentence), or record the exception in D-043 with a SCOPE_CUTS row.",
   "acceptance_test": "Probe D01 prints excerpt == 'Possible symptom magnification noted.'; a test pins it."}
 ],
 "whats_right": [
  "A clean-looking term clause after ';' or a line break now flags: all 16 A-rows (A01-A16, including LF, CRLF, CR, LS and blank-line variants) flag with verbatim whole-sentence excerpts on the lexicon path (r4 F1 closed).",
  "The r1-r4 attack strings (139 rows, artifacts/review-evidence/T-067-claims-adjuster-r5-r4corpus.out.txt) show mismatches=0 on 0f58181, and the three r4 silent-superset examples (0/5 Waddell, Negative Waddell signs, No symptom magnification) now flag, matching D-043's literal list.",
  "tests/unit/test_flags_pass.py is green on the live tree and on the committed archive (30 passed in each), including the new test_d043_semicolon_and_line_break_* test."
 ],
 "questions_for_chris": [
  "For finding 1: when a model flag and a credibility lexicon hit overlap, which governs the excerpt, D-030 (model's verbatim span as evidence) or D-043 (whole period sentence)? I read D-043 as governing a credibility flag; if D-030 governs, D-043 needs an amendment and a SCOPE_CUTS row.",
  "For finding 2: is D-043's parenthetical list exhaustive? If yes, the nine silent forms are a literal D-043 violation and the rating goes to blocker under the spec constraint; I rated minor as r4 did, because the silenced sentences are clean negatives with no second clause.",
  "Does a period after an abbreviation not in the splitter list end a sentence? 'Straight leg raise positive on the right, pt. Waddell signs negative.' is silent (probe E01), and so are 'PT.' (E02) and 'Lt.' (E03), because sentences.py:10 lists no 'pt', 'lt' or 'rt'. Under the period-delimited unit a split there is correct; if not, add the abbreviations to _ALWAYS_ABBREV. Single capitals such as 'R.' already do not split (E04 flags)."
 ]}
```
