# T-067 staff-engineer r6: re-check of the r2 fail under D-043

**Verdict: pass.** The two r2 findings I scored (mixed-side Waddell blocker, "not done" over-flag) are closed at HEAD under D-043. One minor, new: the D-043 text and the code's allow-list disagree on the "not done" form. The r5 findings are routed to T-092 and were not re-scored.

**HEAD.** The brief names HEAD as 0f58181. The current HEAD is e3cea6f (T-080). `git diff --stat 0f58181 HEAD -- app/backend/credibility.py app/backend/flags.py app/backend/flag_templates.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py tests/unit/_fakes.py` printed nothing, so the T-067 files are the same at both commits. I pinned e3cea6f with `git archive` and ran the tests and probes there as well as in the working tree. Working-tree `app/backend/flags.py` has uncommitted edits (R-CO-7 sort in `merge`, judge prompt `judge_flag_v2`). They are outside T-067 scope and the flags tests pass with them. Anyone who changes `judge_flag_v2` needs an eval re-run report (checklist item 18).

**Closure of the r2 findings (D-043, probes through `flags.run_flag_pass` with `FakeCall`, pinned e3cea6f):**

| r2 finding | Check | HEAD result |
|---|---|---|
| F1 blocker: mixed-side sentence drops positive side, order-dependent | 'Waddell signs negative on the left, positive on the right.' | FLAG (whole sentence, pending) |
| | 'Waddell signs negative on the left but positive on the right.' | FLAG |
| | 'Waddell signs positive on the right and negative on the left.' | FLAG |
| | 'Positive Waddell signs on the left, negative on the right.' | FLAG |
| F2 major: post-term negation flags | 'Waddell testing was not done.' | silent |
| | 'Waddell testing was not performed.' | silent |
| F3 minor: count-first '3/5 Waddell.' silent | '3/5 Waddell.' | FLAG |

Brief variants (must flag): 'Effort is inconsistent.', 'Submaximal effort noted.', 'Magnifying symptoms noted.', 'Pain behavior out of proportion to the injury.' all FLAG.

**Superseded by D-043, not re-scored.** The r2 "six negated strings must be silent" list no longer holds at HEAD. 'Waddell signs negative.' and 'No Waddell signs.' are silent. '0/5 Waddell', 'Effort consistent during grip testing.', 'No symptom magnification.' and 'Pain is not out of proportion to the injury.' FLAG. D-043 allows only the listed whole-sentence forms and says extra words flag. The r2 acceptance clause "'Malingering was not suspected.' == []" also flags at HEAD, which matches D-043 and the test list at `tests/unit/test_flags_pass.py` (the "everything else flags" test). I did not re-score these. See the question below.

**Commands and output (verbatim):**

```
$ .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py      (working tree)
..............................                                           [100%]
30 passed in 0.42s

$ cd <scratch>/t067_head_archive && .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py      (git archive e3cea6f)
..............................                                           [100%]
30 passed in 0.71s
```

**Mutants (scratch copies of the e3cea6f archive; the repo was not edited):**
- M1, `if False and _clean_negation(...)` (negation guard off): 5 failed, 25 passed. Failing tests include `test_d038_only_allow_listed_clean_negations_are_silent` and `test_d038_negated_credibility_phrase_raises_nothing`.
- M2, `not (?:tested|performed|done)` with 'done' removed: 1 failed, 29 passed (`test_d038_only_allow_listed_clean_negations_are_silent`). The "not done" check is non-vacuous.
- M3, first-clause-only guard (the r2 bug reintroduced): 3 failed, 27 passed (`test_d038_everything_else_with_a_credibility_term_flags`, `test_d038_mixed_result_waddell_sentence_flags_in_either_order`, `test_d043_semicolon_and_line_break_are_clause_separators_and_excerpt_is_the_full_sentence`).

**Minor finding.** The allow-list comment says it is "exactly the decision's forms". The code accepts 'not done' and an optional 'was/were', which D-043 does not list. The user's silence check needs 'not done', so the decision text is what should change.

```json
{"card": "T-067", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD e3cea6f (T-080); T-067 files unchanged since 0f58181 (empty git diff --stat). Files: app/backend/credibility.py, app/backend/flags.py (credibility hook at :88), tests/unit/test_flags_pass.py. Pinned via git archive e3cea6f and also run in the working tree. Working-tree flags.py has uncommitted R-CO-7 edits outside T-067 scope. No app URL; no sample case run.",
 "exercised": [
   "personas/staff-engineer.md read in full; reviews/T-067-claims-adjuster-r2.md read in full (r2 findings F1-F3 and acceptance tests)",
   "memory/ORCHESTRATOR_DECISIONS.md D-038, D-043 read; board/cards/T-092.md exists (r5 routing)",
   "git log --oneline -5 (HEAD e3cea6f); git diff --stat 0f58181 HEAD -- <T-067 files> (empty)",
   ".venv/bin/python -m pytest -q tests/unit/test_flags_pass.py in the working tree: 30 passed",
   "git archive e3cea6f into a new scratch dir; credibility.py cmp-identical to git show e3cea6f; pytest there: 30 passed",
   "scratch probe (python -I, archive on sys.path) through flags.run_flag_pass + tests.unit._fakes.FakeCall: 4 mixed/positive-first sentences, 6 negated brief strings, 4 brief variants, 'not done'/'not performed'/'Malingering'/'3/5 Waddell'; all FLAG/silent results recorded in the review",
   "Mutants in scratch copies only: M1 negation guard off (5 failed), M2 'done' removed from allow-list (1 failed), M3 first-clause guard (3 failed); archive re-verified pristine after",
   "Read app/backend/credibility.py lines 1-73 at HEAD"
 ],
 "verdict": "pass",
 "scores": {"mixed_result_handling": 5, "not_done_silent": 5, "named_family_recall": 5, "negation_allow_list_matches_decision_text": 4, "test_non_vacuous": 5, "no_network_in_tests": 5},
 "findings": [
   {"severity": "minor",
    "title": "D-043 text and the code's clean-negation allow-list disagree on the 'not done' form",
    "evidence": "app/backend/credibility.py:28 comment 'D-043 allow-list (exactly the decision's forms ...)'; app/backend/credibility.py:34 `rf\"{_W} {_WT}:? (?:(?:was|were) )?not (?:tested|performed|done)\"`; memory/ORCHESTRATOR_DECISIONS.md:51 (D-043) lists 'Not tested/not performed.' only. Repro: grep -n 'not (?:tested|performed|done)' app/backend/credibility.py; grep -n 'Not tested/not performed' memory/ORCHESTRATOR_DECISIONS.md",
    "why_it_matters": "The silent 'Waddell testing was not done.' behaviour the user requires is not in the decision text. The next reviewer who reads D-043 literally will expect 'not done' to flag and reopen the r2 loop. The comment's 'exactly' claim is also false.",
    "fix": "Orchestrator amends D-043 to list the implemented forms ('Waddell testing [was|were] not tested/performed/done.'). Then change the credibility.py:28 comment to match the decision text.",
    "acceptance_test": "tests/unit/test_flags_pass.py::test_d038_only_allow_listed_clean_negations_are_silent keeps 'Waddell testing was not done.' and 'Waddell testing was not performed.' silent, and D-043 in memory/ORCHESTRATOR_DECISIONS.md lists both forms verbatim. Mutant with 'done' removed fails that test (verified: 1 failed)."}
 ],
 "whats_right": [
   "Mixed-result Waddell sentences flag in both orders with the whole sentence as the excerpt at e3cea6f (probe + test_d038_mixed_result_waddell_sentence_flags_in_either_order); the r2 blocker is closed.",
   "'Waddell testing was not done.' and 'not performed' are silent, and removing 'done' from the allow-list fails a test (M2), so the silence is not vacuous.",
   "An r2-style first-clause guard (M3) fails 3 tests, so the mixed-sentence fix is covered by tests and not by coincidence."
 ],
 "questions_for_chris": [
   "'Malingering was not suspected.' flags at HEAD because it is not on the D-043 allow-list. The r2 acceptance clause asked for it to be silent. Should D-043 be amended to make it silent, or does 'fail toward flagging' stand? I did not re-score it and assumed D-043 governs."
 ]}
```
