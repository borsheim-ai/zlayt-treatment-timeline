# T-063 round 3: staff-engineer-reviewer

Scope: docs/LLM_VS_CODE.md and memory/DECISIONS.md at commit 4808b77 (r3 fixes), checked against code pinned to git archive 4808b77 (artifacts/review-evidence/T-063-staff-engineer-r3/head-4808b779b7aedfcc1edb6f9bb5a3a9a30f1a70a6). HEAD moved to 83b4353 during the review (3b6a3fe T-072, 4594bb7, 83b4353 T-074). The delta was checked and the unit suite was rerun at 83b4353 (943 passed).

Verdict: **pass**. No blockers, no majors. The brief's three items are confirmed. Of the r2 items, both majors and minors F3, F4 and F5 are fixed. F6 (judge-path except) is still open and the doc still says it has no card, although T-073 exists. Three minors and one nit are new or carried; all should be fixed before the M3 gate, none blocks T-063.

## Brief items

- **D-038 described as decided: confirmed.** docs/LLM_VS_CODE.md:41 and :100 state credibility phrases raise a flag under `credibility_language` (D-038, T-067, commit 59c7edb). memory/DECISIONS.md:339-341 (ADR-018) says D-038 narrows D-032. The code matches: app/backend/flags.py:16-23 and :95-97. The probe (section 2) gives 10 of 10 expected results. `grep -rn "question for Chris" docs memory/DECISIONS.md` returns nothing.
- **D-040 replaces the chip text: confirmed.** docs/LLM_VS_CODE.md:41 and :101 say the patient self-report chip is cut (D-040). memory/DECISIONS.md:286 agrees. At 4808b77 no code sets `source_kind="patient_report"` (grep over app/ finds only the test assertion at tests/unit/test_flags_pass.py:153). The helpers are gone per tests/unit/test_flags_pass.py:148-151. Still present at 4808b77, all under T-072 (cited as open): app/backend/flag_templates.py:126 (title "Patient self-report"), app/backend/export.py:310 and :365 (suffix). Mock-only: app/frontend/mock_flags.js:24, app/frontend/dev/mock-data.js:748.
- **Row 1 gives NO_MODEL and NOT_ATTEMPTED reasons: partly confirmed.** NO_MODEL is confirmed (probe 1a; 1e with FIXTURE_MISS). NOT_ATTEMPTED is confirmed for several records plus an unsplit tail (probe 1b). Two gaps remain, M1 and M2 below.

## R2 status

| R2 item | Status at 4808b77 | Evidence |
|---|---|---|
| F1 major, D-038 open question | Fixed | section above |
| F2 major, D-040 chip still described as current | Fixed (doc and ADR); code gone except T-072 items | section above |
| F3 minor, row 1 no-model reason | Fixed for NO_MODEL; reason gaps are M1, M2 | probe 1a, 1e |
| F4 minor, batch 404/405 fallback | Fixed | docs/LLM_VS_CODE.md:94-95 (batch bullet); app/frontend/batch.js:17-19 shows an error and accepts nothing; tests/e2e/test_edit.py:42 exists (not run) |
| F5 minor, LLM_UNAVAILABLE wording | Fixed | app/backend/review.py:311 text matches the doc's "has not been drafted yet" |
| F6 minor, broad except in judge path | Open; doc says no card, T-073 exists | M3 |

## Findings

**M1 (minor). Row 1 says SPLIT_REJECTED always names the reason; the run path after a decision drops it.**
Reproduced by probe sections 1d and 1f: `split_failure=None` and only SPLIT_AMBIGUOUS is emitted. Mechanism: pipeline.py:123 (the replay answers None when fewer than two records are stored); ingest.py:267-274 (a None from the splitter sets no split_failure); ingest.py:299-306 (SPLIT_REJECTED is only emitted when split_failure is set). Section 1f uses a test double for "one entry decided"; the reachability through the real path is by code reading (_frozen_splitter returns a replay as soon as any item is non-pending). The state stays visible (SPLIT_AMBIGUOUS shows), so this is not silent.

**M2 (minor). NOT_ATTEMPTED is also emitted for a one-visit paste with a date and source but no excerpt label, with a message that says "several records".**
Probe 1c (probe_t063_r3_1c_output.txt): "Date: March 3, 2026 / Source: Dr. Pell / Dr. Pell notes right wrist swelling." gives 2 records (a header record with empty excerpt, and an unsplit body record), SPLIT_REJECTED with NOT_ATTEMPTED and "The paste has several records and some text outside them". Mechanism: a record is complete only with three labels (ingest.py:96 `found == 3`); eligibility (ingest.py:262) needs a missing date or source; a date plus source paste with no excerpt label is neither, so it falls into NOT_ATTEMPTED (ingest.py:265-266). Row 1's "lacks a date or a source label" does not describe the excerpt-label case. The paralegal sees a false count; no fact is invented.

**M3 (minor). The judge-path except is still uncarded in the doc, but T-073 exists.**
docs/LLM_VS_CODE.md:97 says narrowing it "is a code change with no card yet". `python3 tools/board.py show T-073` gives status "ready": "Narrow the broad except in review.py:83 judge path (keep error class, log reason)". The code at 4808b77 still has app/backend/review.py:83 `except Exception:` and :84 `verdict, call_id = "unavailable", None`. The brief's acceptance rule for an open item is that the doc cites its card. This one does not.

**N1 (nit). The T-072 "Open" note is stale at HEAD, and the mock overlay still shows the cut label.**
docs/LLM_VS_CODE.md:101 says "Open: T-072 gives ...". Commit 3b6a3fe (in HEAD 83b4353) removes the export suffix and retitles the flag ("Reported onset"). T-072 is still in_review. Mock mode still labels the flag "Patient self-report" (app/frontend/mock_flags.js:24, app/frontend/dev/mock-data.js:748; mock_flags.js is loaded only in mock mode, app/frontend/index.html:45). Row 13's absolute "No code or model labels who is speaking" is true at 83b4353 but not at 4808b77 (flag_templates.py:126). Keep the open note until T-072 closes, then remove it from docs/LLM_VS_CODE.md:101 and memory/DECISIONS.md:286.

**Not charged to T-063.** At the pinned archive 4808b77, `tests/unit` gives 941 passed and 1 failed: tests/unit/test_e2e_contract.py:24, `test_every_test_id_is_declared`, missing `btn-undo-batch`. At 83b4353 it gives 943 passed. Commit 4594bb7 declares the id; the failure is a code/test issue, not in the doc.

## Exercised

- Read personas/staff-engineer.md; reviews/T-063-staff-engineer-r2.md; the T-063 project memory file; `git show 4808b77 -- docs/LLM_VS_CODE.md memory/DECISIONS.md`.
- `git rev-parse HEAD` gave 4808b77 at the start and 83b4353 later. `git merge-base --is-ancestor` for 59c7edb, a27e3a4, d148e0f, e0ca2b0, 1c0bae2, 5900040, e7c1912 against HEAD: all yes.
- `git archive 4808b77 | tar -x` into artifacts/review-evidence/T-063-staff-engineer-r3/head-4808b779b7aedfcc1edb6f9bb5a3a9a30f1a70a6; `git archive 83b4353` into the matching head-83b4353... directory.
- `python3 tools/board.py show` for T-063, T-065, T-066, T-067, T-071, T-072, T-073.
- Greps at 4808b77: split reason codes in app/ and memory/contracts/api.md; patient_report, self-report and credibility across app/ and tests/; objective_negative; LLM_UNAVAILABLE and "not been drafted"; `except` in app/backend/review.py; stale phrases in docs/LLM_VS_CODE.md and memory/DECISIONS.md.
- Code read at 4808b77: app/backend/ingest.py:96, 113-134, 249-310; app/backend/pipeline.py:111-126; app/backend/flags.py:12-30, 80-100; app/backend/review.py:76-90, 296-312; app/frontend/batch.js:1-40; app/llm/lexicon.yaml:1146-1170.
- Probe: `.venv/bin/python -I artifacts/review-evidence/T-063-staff-engineer-r3/probe_t063_r3.py` (output in probe_t063_r3_output.txt; sections 1a-1f, 2).
- Probe: `.venv/bin/python -I artifacts/review-evidence/T-063-staff-engineer-r3/probe_t063_r3_1c.py` (output in probe_t063_r3_1c_output.txt).
- `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` in the 4808b77 archive: 941 passed, 1 failed (see above). Same command in the 83b4353 archive: 943 passed.
- `git show --stat 3b6a3fe 4594bb7 83b4353` and `git show 3b6a3fe -- app/backend/export.py app/backend/flag_templates.py`.
- Not run: the eval runner, the CLI on the sample case, the Playwright E2E (tests/e2e/test_edit.py:42 was read, not run), the browser UI, mutation spot-checks. The doc does not claim any of these for T-063.

```json
{"card": "T-063", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "docs/LLM_VS_CODE.md and memory/DECISIONS.md at 4808b77 (r3 fixes); code at git archive 4808b77 (artifacts/review-evidence/T-063-staff-engineer-r3/head-4808b779b7aedfcc1edb6f9bb5a3a9a30f1a70a6); HEAD moved to 83b4353 during review (T-072 landed in 3b6a3fe, plus 4594bb7 and 83b4353; delta checked, unit suite rerun at 83b4353); no app URL; no CLI or E2E run",
 "exercised": [
  "read personas/staff-engineer.md; reviews/T-063-staff-engineer-r2.md; project_t063_doc_vs_code_review_patterns.md; git show 4808b77 -- docs/LLM_VS_CODE.md memory/DECISIONS.md",
  "git rev-parse HEAD (4808b77, later 83b4353); git merge-base --is-ancestor 59c7edb a27e3a4 d148e0f e0ca2b0 1c0bae2 5900040 e7c1912 HEAD -> all yes",
  "git archive 4808b77 | tar -x into artifacts/review-evidence/T-063-staff-engineer-r3/head-4808b779b7aedfcc1edb6f9bb5a3a9a30f1a70a6; git archive 83b4353 into head-83b4353d1eba35aad357815fb0a1266f25be4320",
  "python3 tools/board.py show T-063, T-065, T-066, T-067, T-071, T-072, T-073; board.py list",
  "grep split reason codes in app/ and memory/contracts/api.md; grep patient_report, self-report, credibility, objective_negative, LLM_UNAVAILABLE, except in review.py, stale phrases in docs and DECISIONS",
  "code read at 4808b77: app/backend/ingest.py:96, 113-134, 249-310; app/backend/pipeline.py:111-126; app/backend/flags.py:12-30, 80-100; app/backend/review.py:76-90, 296-312; app/frontend/batch.js:1-40; app/llm/lexicon.yaml:1146-1170",
  "artifacts/review-evidence/T-063-staff-engineer-r3/probe_t063_r3.py via .venv/bin/python -I (probe_t063_r3_output.txt): sections 1a-1f (split reasons, replay path with a test double for one decided entry) and section 2 (10 of 10 credibility and context-only cases match)",
  "artifacts/review-evidence/T-063-staff-engineer-r3/probe_t063_r3_1c.py via .venv/bin/python -I (probe_t063_r3_1c_output.txt): one-visit paste record counts",
  ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider in the 4808b77 archive: 941 passed, 1 failed (test_e2e_contract.py:24, btn-undo-batch); in the 83b4353 archive: 943 passed",
  "git show --stat 3b6a3fe 4594bb7 83b4353; git show 3b6a3fe -- app/backend/export.py app/backend/flag_templates.py",
  "not run: eval runner, CLI on the sample case, Playwright E2E (tests/e2e/test_edit.py:42 read only), browser UI, mutation spot-checks"
 ],
 "verdict": "pass",
 "scores": {"r2_findings_fixed": 4, "doc_matches_code_at_head": 4, "doc_reflects_binding_decisions": 5, "failures_visible_in_doc": 4, "tests_reproducible_at_pinned_sha": 4},
 "findings": [
  {"severity": "minor", "title": "Row 1 says SPLIT_REJECTED always names the reason on runs; the replay path after a decision emits none",
   "evidence": "docs/LLM_VS_CODE.md:29 ('SPLIT_REJECTED always names the reason, on case creation and on runs'); probe_t063_r3_output.txt sections 1d and 1f (split_failure=None, only SPLIT_AMBIGUOUS); app/backend/pipeline.py:123 (replay returns None when fewer than two stored records); app/backend/ingest.py:267-274 (a None from the splitter sets no split_failure); app/backend/ingest.py:299-306 (SPLIT_REJECTED only when split_failure is set)",
   "why_it_matters": "The doc is the reason-code contract the paralegal and an auditor read. SPLIT_AMBIGUOUS stays visible, so this is not silent, but on one re-run path the reason is lost and the doc says it is never lost. Section 1f uses a test double for the decided item; reachability through the real path is by code reading.",
   "fix": "In ingest.py, when the paste is eligible and the splitter returns None, set split_failure to a named code (for example NOT_REPLAYED); or change row 29 to say SPLIT_REJECTED names the reason 'when one exists'.",
   "acceptance_test": "Unit test: a single unsplit stored record with one decided entry, re-run through run_pipeline or run_ingest with the frozen splitter, asserts a SPLIT_REJECTED warning carrying a reason code; probe_t063_r3.py section 1f prints a reason."},
  {"severity": "minor", "title": "NOT_ATTEMPTED fires on a one-visit paste with date and source but no excerpt label, and its message says several records",
   "evidence": "probe_t063_r3_1c_output.txt: 'Date: March 3, 2026 / Source: Dr. Pell / Dr. Pell notes right wrist swelling.' gives method ambiguous, 2 records (header record with empty excerpt; unsplit body record), SPLIT_REJECTED NOT_ATTEMPTED 'The paste has several records and some text outside them'; app/backend/ingest.py:96 (complete requires found == 3), :262 (eligible), :265-266 (NOT_ATTEMPTED), :301 (message); docs/LLM_VS_CODE.md:29 ('lacks a date or a source label'; NOT_ATTEMPTED described as several records plus an unsplit tail)",
   "why_it_matters": "The paralegal is told her one-visit paste has several records, which is false, and the header record is left with no body text. The state is visible and no fact is invented, but the doc's trigger description does not match the code, so a reader cannot predict this outcome.",
   "fix": "Either describe the excerpt-label case in row 29 and make the message say 'the paste has a date and source but no excerpt label, so the text after the header stays its own record'; or make a date plus source paste eligible for the split step (decision for Chris, see questions_for_chris).",
   "acceptance_test": "repro: .venv/bin/python -I artifacts/review-evidence/T-063-staff-engineer-r3/probe_t063_r3_1c.py; after the fix, the message names the case that occurred and the doc sentence matches the output."},
  {"severity": "minor", "title": "Judge-path except: doc says no card exists, but T-073 is on the board",
   "evidence": "docs/LLM_VS_CODE.md:97 ('narrowing it to provider errors is a code change with no card yet'); python3 tools/board.py show T-073 -> status 'ready', 'Narrow the broad except in review.py:83 judge path (keep error class, log reason)'; app/backend/review.py:83 'except Exception:' and :84 'verdict, call_id = \"unavailable\", None' at 4808b77",
   "why_it_matters": "The brief accepts an open item only when the doc cites its card. This one has a card and the doc denies it, so a reader cannot find the owner. This is the r2 F6 minor, carried; the state stays visible (JUDGE_UNAVAILABLE) and the error class is lost.",
   "fix": "In docs/LLM_VS_CODE.md:97 replace 'with no card yet' with 'T-073, ready'. Keep the sentence about the lost error class.",
   "acceptance_test": "grep -n 'no card yet' docs/LLM_VS_CODE.md returns nothing; grep -n 'T-073' docs/LLM_VS_CODE.md returns line 97."},
  {"severity": "nit", "title": "T-072 open note is stale at HEAD; mock overlay still shows the cut patient self-report label",
   "evidence": "docs/LLM_VS_CODE.md:101 ('Open: T-072 gives ...'); commit 3b6a3fe (in HEAD 83b4353) removes the export suffix (app/backend/export.py) and retitles the flag 'Reported onset' (app/backend/flag_templates.py); T-072 status in_review; app/frontend/mock_flags.js:24 and app/frontend/dev/mock-data.js:748 still show 'Patient self-report' (mock mode only, app/frontend/index.html:45); app/backend/flag_templates.py:126 still titled 'Patient self-report' at 4808b77",
   "why_it_matters": "The doc calls landed code open, and row 13's 'No code or model labels who is speaking' is absolute while the flag title still says Patient self-report at 4808b77. Mock mode still shows the cut label.",
   "fix": "Keep the open note until T-072 closes; then delete the 'Open: T-072' sentence at docs/LLM_VS_CODE.md:101 and memory/DECISIONS.md:286. Put the mock overlay labels under T-072 or a new card.",
   "acceptance_test": "git grep -n 'Patient self-report' -- app/frontend returns nothing outside tests and dev mock data; docs/LLM_VS_CODE.md:101 has no 'Open: T-072' sentence after T-072 closes."}
 ],
 "whats_right": [
  "Credibility phrases: 10 of 10 probe cases match the doc (probe_t063_r3_output.txt section 2); negation and context-only findings raise nothing (app/backend/flags.py:16-23)",
  "Patient self-report chip: no code at 4808b77 sets source_kind 'patient_report'; tests/unit/test_flags_pass.py:148-153 asserts the helpers are gone",
  "Batch fallback closed: app/frontend/batch.js:17-19 shows an error and accepts nothing on 404/405; tests/e2e/test_edit.py:42 covers it (read, not run)"
 ],
 "questions_for_chris": [
  "For M2: should a one-visit paste with a date and source but no Excerpt label be split (header and body as separate records, as the code does now) or kept as one record? The answer decides whether row 1 should describe that case or the code should change."
 ]}
```
