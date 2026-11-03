# T-109 round-4 review (staff-engineer-reviewer), fix-up commits 5f1a7e2 and 425095f

Scope: the two r3 corrections only. HEAD pin 425095fa7ec682aae9b3773af230e6e3b20a0f3f (checked at start and before writing; unchanged).
The working tree is dirty with other agents' uncommitted edits, so every check below reads HEAD (`git show HEAD:...`, `git archive HEAD`), not the working tree.

Verdict: pass. Both corrections close the r3 findings against HEAD code: row 11 now matches `evals/j3_controls.py` (the reachability test passes, `--check` exits 0, and no control pairs a dosage or a left/right laterality), and row 4 plus ADR-020 item 5 describe the suffix-only trim at `summary_trim.py:417-423` (four probes at HEAD return the documented results). The `flags.py:185-209` cite contains `_model_conflicts` but starts two blank lines early (nit). No blocker, no major.

Findings:
- nit: `flags.py:185-209` starts on two blank lines; `_model_conflicts` is at 187.
- nit: row 11's "neither proposed nor measured" is accurate, but three controls contain "left knee" or "right knee" text, which a reader may take for laterality; they are body-part mismatches.

```json
{"card": "T-109", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "docs/LLM_VS_CODE.md rows 4 and 11 and memory/DECISIONS.md ADR-020 items 2 and 5, as changed by 5f1a7e2 and 425095f; checked against HEAD 425095fa7ec682aae9b3773af230e6e3b20a0f3f (git show HEAD:path; git archive HEAD into the scratchpad); no app URL (docs review); sample case not run (outside the two corrections)",
 "exercised": [
  "python3 tools/board.py show T-109 (read the 12:25:49Z orchestrator section 7.4 decision: accept after a mechanical fix-up, verify only the two edits against HEAD); git rev-parse HEAD -> 425095fa7ec682aae9b3773af230e6e3b20a0f3f (re-checked before writing, unchanged); git log -n 8",
  "git diff --stat HEAD -- docs/LLM_VS_CODE.md memory/DECISIONS.md app/backend/summary_trim.py app/backend/flags.py evals/j3_controls.py tests/unit/test_t093_eval_signature.py -> empty (exit 0; the working tree is dirty elsewhere, not in these files)",
  "git show --stat 5f1a7e2 425095f; git diff 425095f~2 425095f -- docs/LLM_VS_CODE.md memory/DECISIONS.md (5f1a7e2: row 4 and ADR-020 item 5 line swapped, row 11 J3 sentence swapped; 425095f: ADR-020 item 2 cite flags.py:187-212 -> flags.py:185-209)",
  "git show HEAD:docs/LLM_VS_CODE.md and HEAD:memory/DECISIONS.md, HEAD:app/backend/summary_trim.py, HEAD:app/backend/flags.py, HEAD:evals/j3_controls.py, HEAD:tests/unit/test_t093_eval_signature.py written to scratchpad t109r4/; grep -c 'not left behind' and grep -c 'include dosage and laterality' on the HEAD doc and ADR -> 0 and 0",
  "row 11 (LLM_VS_CODE.head.md:39) and ADR-020 item 2 (DECISIONS.head.md:364) and item 5 (:367) read in full; row 4 (:32) read in full: structural rule cites summary_trim.py:417-423, SUMMARY_NOT_IN_QUOTE cites :414-415",
  "sed -n '1,30p' and '175,215p', '258,270p', '370,390p' of HEAD flags.py with nl -ba: _model_conflicts def at 187 (185-186 blank), body ends at 209; call site :265 (_model_conflicts(conflicts, record, tagged)); judge_flags backstop :381-383 (conflict with origin llm -> _to_tray LLM_ONLY, continue)",
  "sed -n '14,34p' and '385,435p' of HEAD summary_trim.py with nl -ba: docstring rule (1) SUFFIX ONLY at :26-27; code :417 drop[0] return, :419-421 first_cut / all(drop[first_cut:]) suffix check, :422-423 kept prefix >= 2 content words; no comma/and/with arm remains in trim()",
  "tests and CHANGELOG at HEAD: git show HEAD:tests/unit/test_t093_j3_controls_reachable.py grep -n def test_every_j3_control_input_is_producible_by_the_candidate_generator -> :30; git show HEAD:tests/unit/test_summary_trim.py grep -n def test_a_trim_never_leaves_a_fragment / test_the_first_clause_is_never_removed / test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed -> :162, :635, :646; git show HEAD:evals/golden/judge_controls.CHANGELOG.md line 27 ('Removed ... because the generator does not propose them'); git cat-file -t 822ff38 -> commit; git show --stat 822ff38 lists evals/j3_controls.py and test_t093_j3_controls_reachable.py",
  "cd head_tree (git archive HEAD) && .venv/bin/python -m evals.j3_controls --check -> exit 0 (no live model, no network)",
  "cd head_tree && .venv/bin/python -m pytest tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t093_eval_signature.py -q -p no:cacheprovider -> 76 passed",
  "scan of HEAD evals/golden/judge_controls.jsonl and judge_controls_heldout.jsonl (all 32 J3/H3 rows, pair and excerpt_b fields) for left|right|bilateral|mg|dose|units: four hits, all body-part or verb uses (J3V4 'left PT'; J3V7 and J3V12 'left knee'; H3V9 'right knee'); no row pairs left against right; no dose pair",
  "git show HEAD:app/backend/conflict_candidates.py grep -n -i 'left|right|lateral|dose|mg|dosage' -> line 17 (not covered) and line 40 ('left care' in the early-end pattern); no laterality or dosage candidate rule",
  "scratchpad probe_trim.py run against head_tree with .venv/bin/python: row-4 example 'Wrist pain 6/10; splint fitted; patient tolerated well.' over 'Wrist pain 6/10. Patient tolerated well.' -> changed=False, unchanged; 'Neck pain 4/10; splint fitted.' over 'Neck pain 4/10.' -> trimmed to 'Neck pain 4/10.' (suffix); 'Neck pain 4/10; splint fitted; patient tolerated well.' over 'Neck pain 4/10. Patient tolerated well.' -> unchanged (middle removed, tail kept); 'Splint fitted; neck pain 4/10.' -> unchanged (first clause unsupported); 'Pain; splint fitted.' over 'Pain.' -> unchanged (prefix under 2 content words)",
  "cited-line check of ADR-020 item 2 and row 11 (DECISIONS.head.md:364, LLM_VS_CODE.head.md:39) against the code: every cited function and line range re-read; ranges 185-209 and 381-383 and 265 checked as above"
 ],
 "verdict": "pass",
 "scores": {"claims_match_code": 5, "tests_backing_claims": 5, "decisions_consistency": 5, "citation_precision": 4, "honest_limits_disclosed": 4},
 "findings": [
  {"severity": "nit",
   "title": "flags.py:185-209 starts two blank lines before _model_conflicts (def at 187)",
   "evidence": "docs/LLM_VS_CODE.md:39 (row 11): '`_model_conflicts`, `flags.py:185-209`, called at `:265`'; memory/DECISIONS.md:364 (ADR-020 item 2): '(`flags.py:185-209`, `:381-383`)'. HEAD app/backend/flags.py via sed -n '185,187p' | nl -ba -v185: 185 (blank), 186 (blank), 187 'def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:'. The body ends at 209 ('    return out'). The call at :265 and the backstop at :381-383 (judge_flags, origin llm -> _to_tray LLM_ONLY, continue) are exact. The r3 nit asked for the range to contain exactly the named function.",
   "why_it_matters": "The range contains the function, so the claim is not false; it is two lines loose. Cosmetic, but a reader who opens the cited first line lands on whitespace, and the r3 acceptance test ('the cited ranges contain exactly the named functions') is not met to the letter.",
   "fix": "Architect: change 'flags.py:185-209' to 'flags.py:187-209' in docs/LLM_VS_CODE.md row 11 (line 39) and memory/DECISIONS.md ADR-020 item 2 (line 364).",
   "acceptance_test": "grep -n 'flags.py:185-209' docs/LLM_VS_CODE.md memory/DECISIONS.md returns nothing; sed -n '187p' app/backend/flags.py at HEAD prints 'def _model_conflicts(...'; 'flags.py:187-209' appears in row 11 and ADR-020 item 2."},
  {"severity": "nit",
   "title": "Row 11 'laterality not measured' is true, but three controls carry left/right knee text",
   "evidence": "evals/golden/judge_controls.jsonl J3V7 (wrong): excerpt_a 'Patient denies prior neck problems.', excerpt_b 'History: left knee injury in 2022 treated with physical therapy.'; J3V12 (correct): excerpt_a 'Patient denies any prior injury.', excerpt_b 'History: left knee injury in 2022 treated with physical therapy.'; evals/golden/judge_controls_heldout.jsonl H3V9 (wrong): excerpt_a 'Denies prior back surgery.', excerpt_b 'Prior surgery on the right knee in 2019.' Each is a denial against a different body part (rule 2a), not a left-versus-right pair. Scan of all 32 J3/H3 rows at HEAD found no row that pairs left with right and no dose pair.",
   "why_it_matters": "The row's claim (no dosage or laterality pair is measured) is correct. A reader who greps evals/j3_controls.py or the control files for 'left' or 'right' finds three hits and may conclude the claim is wrong. One clause removes the ambiguity. Optional.",
   "fix": "Architect (optional): in row 11 after 'neither proposed by code nor measured', add 'no control sets one side against the other; the three side words in the controls (J3V7, J3V12, H3V9) are body-part mismatches under rule 2a'.",
   "acceptance_test": "grep -n 'sets one side against the other' docs/LLM_VS_CODE.md returns the row 11 line; the three control ids named in that sentence appear with 'left knee' or 'right knee' in judge_controls*.jsonl; the row still says dosage and laterality are not measured."}
 ],
 "whats_right": [
  "Row 11's J3 sentence now matches evals/j3_controls.py: 'every J3 control is a pair the candidate generator proposes' is backed by test_every_j3_control_input_is_producible_by_the_candidate_generator (76 passed with the signature test) and '--check' exits 0 at HEAD; no 'dosage and laterality pairs' sentence remains",
  "Row 4 and ADR-020 item 5 describe the suffix-only trim with the right range: summary_trim.py:417-423 covers the first-clause, suffix and kept-prefix checks, and the four probes at HEAD return the documented results; 'not left behind' is gone from both files",
  "The removal history is cited truthfully: commit 822ff38 exists and changed evals/j3_controls.py and the reachability test, and judge_controls.CHANGELOG.md line 27 gives the reason for the removed dose and laterality controls"
 ],
 "questions_for_chris": []}
```
