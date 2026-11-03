# T-057 review, round 2: LLM split fallback (LLM_SPLIT), staff-engineer-reviewer

Commit under review: b365af3 (pinned by `git archive`; HEAD has since moved to 08764e7, so I judged b365af3 plus the working tree where stated).
Verdict: **fail**. One blocker (a variant of round-1 blocker 2), three minors, one nit.

Round-1 items, checked one by one:
- Blocker 1 (eval report hash): fixed. `git show b365af3:app/llm/prompts/split_v1.md | shasum -a 256` is 9a2d0cff...; `evals/reports/20261102T022701Z.md:45` lists the same hash, and the report is committed in b365af3. The report is still `ship_bar_met: False` (fixture backend, 3-run live metrics not measured). It has no split row (see minor 2).
- Blocker 2 (stale spans on same-count re-run): fixed for the case where the re-run's split succeeds (`pipeline.py` now deletes and re-stores on every `split_method == "llm"` run; mutant M1 fails a test). **Not fixed when the re-run's split fails or is rejected** (new blocker below).
- Major swallowed except: fixed. `SplitFailed` carries a reason code, `LLM_FAILED_AFTER_RETRIES` with `stage: split` reaches `errors[]`, and code rejections give a `SPLIT_REJECTED` warning. Mutants M2 and M7 fail tests.
- Major prompt_version / call id: fixed. `PROMPT_OF_STEP` feeds `audited_call`, the flag ladder carries `call_id`; mutants M3 and M6 fail tests.
- Major coverage / contiguity mutants: fixed. Dropping the coverage check (M4) or the contiguity check (M8) now fails tests.
- Major LLM_VS_CODE row 1: fixed by 473ac2a (row 1 now describes the fallback and names `test_split_llm.py`).
- Minors (span, MAX_RECORDS): fixed and tested (`SPLIT_TOO_MANY`; absolute evidence span).

```json
{"card": "T-057", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit b365af3 (r1 fixes to 099732b): app/backend/ingest.py, pipeline.py, split_llm.py, app/llm/audited.py, app/llm/prompts/split_v1.md, evals/reports/20261102T022701Z.md, tests/unit/test_split_llm.py, deleted fixture e89d4fba...json. Pinned via git archive of b365af3 under artifacts/review-evidence/T-057-staff-engineer-r2/tree (with the then-untracked split fixture copied in for the control run). HEAD is now 08764e7 and the working tree is dirty. No app URL exercised. Golden case evals/golden/unsplit_paste.txt (synthetic) and a stub-split case.",
 "exercised": [
  "read personas/staff-engineer.md in full; read reviewer memory MEMORY.md and project_split_llm_review_patterns.md; read reviews/T-057-staff-engineer.md (round 1)",
  "python3 tools/board.py show T-059 and show T-057 -> T-057 rounds 1, commits [099732b, b365af3], round-1 findings listed",
  "git log --oneline | head -8 -> b365af3 is the r1 fix commit; git rev-parse HEAD at start -> b365af3f83d9; git log -4 later -> HEAD moved to fa8a36e / 08764e7 (bee1844 scores unsplit_paste in evals.run; 31070c3 commits the split fixture)",
  ".venv/bin/python -m pytest tests/unit -q -k split (working tree) -> 60 passed, 823 deselected in 1.61s",
  ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider (working tree, later) -> 895 passed in 17.46s",
  "git show b365af3 -- app/ evals/reports tests/unit/test_split_llm.py read in full",
  "git archive b365af3 into artifacts/review-evidence/T-057-staff-engineer-r2/tree: ls tests/fixtures/llm/split -> 'No such file or directory'; pytest -k split -> 3 failed, 57 passed (test_golden_unsplit_paste_replays_recorded_split_through_audited, test_run_pipeline_replaces_the_single_stored_record, test_split_audit_row_has_prompt_version_and_flag_resolves_to_call); git ls-files tests/fixtures/llm/split at that time printed nothing and git status showed '?? tests/fixtures/llm/split/'; after copying the untracked fixture d143a9a0...json in: 60 passed",
  "eval report provenance: git show b365af3:app/llm/prompts/split_v1.md | shasum -a 256 -> 9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b; grep -n split_v1 evals/reports/20261102T022701Z.md -> line 45 same hash; git log --oneline -- evals/reports/20261102T022701Z.md -> b365af3",
  "mutants (scratch copies of the pinned tree, pytest -k split, baseline 60 passed): M1 revert to replace-only-if-count-differs -> 1 failed; M2 drop the errors[] append for split failures -> 1 failed; M3 drop prompt_version in make_call -> 1 failed; M4 drop coverage check -> 1 failed; M5 drop SPLIT_TOO_MANY -> 1 failed; M6 drop call_id on the flag -> 2 failed; M7 swallow SplitFailed -> 2 failed; M8 drop contiguity -> 2 failed (script: artifacts/review-evidence/T-057-staff-engineer-r2/mutants.py)",
  "probe artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py on the pinned tree: run 1 split OK (3 records), run 2 same case split call raises LLMFailed",
  "grep of narrow scope: no float( or sleep( in split_llm.py or test_split_llm.py; the only except clauses in the split path are ingest.py:267 (SplitFailed), :269 (ValueError), split_llm.py:21,23,27 (specific types)",
  "docs/LLM_VS_CODE.md row 1 (line 29) read: describes the fallback, names test_split_llm.py; git log -3 -- docs/LLM_VS_CODE.md -> 473ac2a is the update",
  "Not exercised: frontend rendering of LLM_SPLIT; live claude-cli or API backend; python -m app.pipeline evals/golden/sample.txt (not in this card's brief); the live 3-run eval"
 ],
 "verdict": "fail",
 "scores": {"boundary_validation_fail_closed": 5, "llm_split_flagging_every_record": 4, "audit_routing_and_prompt_version": 5, "eval_regression_discipline_8_3": 4, "silent_failure_visibility": 5, "state_consistency_on_rerun": 2, "test_strength_on_ac1": 5, "doc_contract_alignment": 5, "commit_self_containedness": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A re-run whose split fails or is rejected keeps the earlier run's model-split records; the new run's entries then cite text outside the stored record",
   "evidence": "pipeline.py at b365af3: 'if ing[\"split_method\"] == \"llm\": conn.execute(\"DELETE FROM records WHERE case_id=?\", (cid,))' then '_store_records(conn, cid, ing)', which returns early when rows already exist (pipeline.py:101-102). When run 2's split fails or is invalid, split_method is 'ambiguous', the DELETE is skipped, and run 1's three records stay. Repro: .venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py <pinned tree> prints: \"run1 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors []\", \"run2 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors [('LLM_FAILED_AFTER_RETRIES', 'split')] split_method None\", \"entry e1 record ['r1'] stored span (0, 47) excerpt 'Splint removed.' in stored record text: False\", \"INCONSISTENT\". The same holds for a code-rejected proposal (SPLIT_* reason), which takes the same branch. The new test test_rerun_with_different_boundaries_replaces_the_stored_records only covers a second successful split.",
   "why_it_matters": "This is the round-1 blocker again on a different path: the records table (what the case view renders from char_start/char_end, present.py:131) and the run's entries disagree. A visible LLM_FAILED_AFTER_RETRIES error is shown, but the stored record text for r1 is 47 characters while the entry cites a sentence from r3's text, so a quote is attributed to the wrong record. A split timeout on a re-run (POST /api/cases/{token}/run) is exactly the failure a live model produces, so it is reachable in production.",
   "fix": "Replace the stored records on every run in which the run's record set differs from the stored one, in the same transaction and before any entry or flag is written: delete and re-store whenever split_method != 'code' (or always, keyed on the ing records). Alternatively keep the first accepted split and do not re-ask the model on a re-run. Either way a failed re-split must leave records and entries consistent.",
   "acceptance_test": "test_split_llm.py: run_pipeline with a split stub giving boundaries A (3 records), then run_pipeline again with a split stub raising AU.LLMFailed (and a second case with invalid spans). After run 2: SELECT char_start, char_end FROM records matches the run's own records (one record 0..len(text)), and every entry excerpt is a substring of raw[char_start:char_end] of its own record. probe_rerun_fail2.py prints 'consistent'."},
  {"severity": "minor",
   "title": "The fix commit is not self-contained: it deleted the tracked split fixture and the replacement was left untracked",
   "evidence": "git show b365af3 --name-status -> 'D tests/fixtures/llm/split/e89d4fba...json'; git status at review start -> '?? tests/fixtures/llm/split/'; git archive b365af3 then 'pytest tests/unit -q -k split' -> '3 failed, 57 passed' (the three replay tests; the log shows the call with prompt_hash d143a9a0... found no fixture). After copying the untracked d143a9a0...json into the archive: 60 passed. Later commit 31070c3 adds the file (git ls-files tests/fixtures/llm/split now prints it).",
   "why_it_matters": "A clean checkout of the reviewed commit has three red split tests, and the 'recorded live' evidence for AC2 is not in that commit. This is resolved at HEAD by 31070c3, so the remaining point is process: the card's evidence commit must contain its fixtures.",
   "fix": "Already fixed in 31070c3. Add the fixture to the commit that changes the prompt hash, and check with a clean `git archive` run before in_review.",
   "acceptance_test": "git archive of the card's last commit + pytest tests/unit -q -k split -> 0 failed."},
  {"severity": "minor",
   "title": "The eval report at b365af3 has no row for the split step",
   "evidence": "evals/reports/20261102T022701Z.md (committed in b365af3) lists split_v1.md's hash at line 45 but no metric or assertion for unsplit_paste; grep -n unsplit evals/run.py at b365af3 -> no hits. HEAD has score_unsplit (evals/run.py:295, added in bee1844).",
   "why_it_matters": "Per your note, the unit replay is accepted evidence for the split eval; this is only to record that the committed report does not score it. The report is evidence for the prompt hash, not for split behaviour.",
   "fix": "Re-run evals.run at HEAD so a committed report contains the unsplit_paste row, and cite that report path in the card.",
   "acceptance_test": "A committed report under evals/reports lists an unsplit_paste result and split_v1.md hash 9a2d0cff...."},
  {"severity": "minor",
   "title": "The report is not a passing report: ship_bar_met is False and one entry-recall miss is in the committed numbers",
   "evidence": "evals/reports/20261102T022701Z.md:3 'ship_bar_met: False'; line 5 'Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)'; line 'entry misses: {\"case_06_subtle_pre_existing\": [{\"entry\": \"E3\", ...}]}', entry_recall 0.982.",
   "why_it_matters": "These come from the fixture backend and are not caused by T-057, and the prompt hash is the part this card is accountable for. Noted so nobody reads the report path as a green ship bar.",
   "fix": "Say in the card handoff that the report attests to the prompt hash only, and that the ship bar waits for the live 3-run.",
   "acceptance_test": "Card notes state what the report does and does not show."},
  {"severity": "nit",
   "title": "except ValueError in ingest wraps the splitter call and _llm_records, not just validate_split",
   "evidence": "app/backend/ingest.py:263-270 at b365af3: one try covers splitter(text), validate_split(...) and _llm_records(...); 'except ValueError as e' maps any ValueError to SPLIT_INVALID.",
   "why_it_matters": "A programming error in _llm_records that raises ValueError would be reported as a rejected AI proposal. It is visible (SPLIT_REJECTED) but mislabelled.",
   "fix": "Narrow the try to validate_split only, or raise a dedicated exception from it.",
   "acceptance_test": "A ValueError raised inside _llm_records propagates; a SPLIT_* ValueError from validate_split still yields SPLIT_REJECTED."}
 ],
 "whats_right": [
  "Every round-1 clause is now pinned by its own test: eight single-clause mutants of the split path each fail at least one test, including coverage and contiguity.",
  "Split failures are visible: SplitFailed carries a reason code, errors[] gets stage 'split', and unexpected exceptions propagate (test_unexpected_splitter_errors_propagate).",
  "The audit row carries prompt_version 'split_v1' and the LLM_SPLIT flag's ladder carries the call_id, and the committed eval report hash matches the committed prompt."
 ],
 "questions_for_chris": []}
```
