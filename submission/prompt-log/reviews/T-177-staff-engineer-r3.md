# T-177 round 3 (final; D-065 honest provenance): staff-engineer-reviewer

**Verdict: fail (2 blockers, 1 major, 2 minors, 1 nit).** The three round-2 items are fixed on everything the shipped sample reaches: the 19 Why panels of the sample (10 flags, 9 entries) show no "AI found it", "AI draft" or model name, and an HTTP walk of the sample's case, judges, audit, trace, status, every item, every item trace and the export finds no authorship wording on a prepared item. They are not closed on the failure paths the round-2 brief named. A malformed curated answer flips the whole case back to "Drafted by claude-sonnet-5-5" (the round-1 blocker). A failed curated answer and a missing one still have seven trace steps that call the summary or answer "the AI's". A closed swap table (`why.to_prepared`) is the root cause: any fixed sentence that is not on the list leaks. The shipped curated files do not reach these paths, so the demo a reader sees today is clean; I rated them the way round 2 rated the latent F-B, by the rule and not by reach.

**Scope.** Card commit 2e58e18, reviewed from `git archive 2e58e18` (`artifacts/review-evidence/T-177-staff-engineer-r3/archive-source-sha.txt`). HEAD is now fa4f79e; it changes `app/backend/export.py` and `app/backend/present.py` after 2e58e18, and I did not review those hunks. Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r3/`.

**Round-2 status**

| Round-2 item | Status at 2e58e18 |
|---|---|
| F-A blocker: curated flag Why panels said "AI found it" / "AI draft" | Fixed on the sample. `render-flags-r3.out`: 19 Why panels, 0 bad hits; 6 flags read "Prepared answer, standing in for the AI draft" and f_r7_1 (the phrase list's own flag) reads "Prepared answers did not include this flag" and its sentence agrees (F-E also fixed) |
| F-B blocker: failed prepared item says "AI drafted" | Not closed. The headline step now keeps the Prepared label; seven other steps of the same trace still say "the whole AI summary" (F1 below) |
| F-C major: missing curated answer shows a passing AI step naming a model | Partly closed. The step is now a FAIL with no model. The item's own `why` and seven more steps still say "recorded AI answer" / "the AI gave no usable answer" (F2); the schema variant of the same fault flips the case to claude-sonnet-5-5 (F3) |
| F-D nit: prompt version and hash on prepared rows | Fixed at the API (audit rows null, export `prompt_versions` has only judge prompts). No test guards it (F4) |
| F-E minor: "AI found it" beside "AI did not find it" | Fixed |

## Residuals the worker listed (item 3)

| Residual | Decision | Why |
|---|---|---|
| `/health` answers `prepared` with a curated key missing | Fine | It states which fixture set the process uses, not who wrote an answer. In the missing-key run `probe-r3-branch-missing.out` shows run status `failed`, e1 `rejected` with FIXTURE_MISS, and `models.generator` still `hand-checked (qa)`. The per-item truth is on the item. The mixed library case under a curated process is the accepted round-1 F4 |
| Export disclosure line "drafted with AI assistance" | Not a blocker or major; minor (F5) | `export.py:29` and `:733` put it in the INTERNAL REVIEW NOTES block only; the letter text has none (D-009 holds). It labels no item and names no model. It still sits badly beside a badge that says the answers were not written by an AI model, so it should have a prepared variant |
| review.py edit and manual warnings say "AI wording" | The claim is wrong about where; nothing to fix in review.py | In `review.py` the phrase is in comments only (lines 72, 464, 484). The edit and manual-entry warnings I read (`review.py:399-401`) say "The second check ...". The same phrase is a real message at `export.py:662` and `:719` (internal notes, only for an edited entry whose original failed a code check). I did not reach that path; it is latent and a nit |

## Findings

**F1 blocker: a malformed curated answer flips the whole case back to "Drafted by claude-sonnet-5-5" and "AI-made".** Reproduction: `probe-r3-branch-schema.out` (curated copy, e1's `summary` key removed). `case.models` and `/judges` `models` are `generator: claude-sonnet-5-5, generator_prepared: false`; the case trace `extract` step reads "AI drafts a summary and a quote for each record" / "no AI-made entry", the `judges` step "Second AI check on every AI-made item". The other eight answers are unchanged curated answers. Cause: the first attempt is a SCHEMA_INVALID row with no `recorded_from`, the retry is FIXTURE_MISS and is excluded, so `present.py:309-310` computes `all(is_prepared(...))` over one non-prepared row and gets False. `judges.js:168-171` prints "Drafted by " plus `m.generator` whenever `prepared` is false, so the judge panel would name claude-sonnet-5-5 (I read the code; I did not render this variant). `/api/health` in the same run still says `answers: prepared`. This is round-1 F1. The worker's `test_failed_prepared_item_trace_says_prepared[schema]` (`tests/unit/test_prepared_provenance_r3.py:144`) reads only e1's `extracted` step.

**F2 blocker: fixed AI-authorship sentences that are not in the swap table survive on prepared items.** Two families, both reproduced:
- Failed prepared answer: `probe-r3-branch-unsupported.out`. e1 is `prepared: true`, model `hand-checked (qa)`, and seven steps (`excerpt_verbatim`, `excerpt_whole_sentence`, `excerpt_hedge`, `summary_tokens`, `summary_qualifier`, `highlight`, `judge_1`) read "Not run: code removed the whole AI summary because the quote does not support it" (`trace.py:306`). The team wrote that summary.
- Code trims on a prepared answer that states an amount: `probe-r3-branch-amount.out` (ER entry's curated quote and summary carry "$6,240"). e2 is `prepared: true`, `verified`; its `excerpt_narrowed` step says "from the quote the AI picked" (`trace.py:387`) and `charge_clause_removed` says "from the end of the AI's summary" (`trace.py:393`; `:407` says the same after a quote edit). The shipped curated files hold no amount in a quote, so the sample does not reach this.
The swap table (`why.py:89-111`) lists 23 sentences; `_skipped` (`trace.py:302-309`) and the trim sentences are not on it. The worker's scan regex (`test_prepared_provenance_r3.py:16`) has no "AI summary", "AI picked", "AI gave" or "AI answer", so a test that only ran the happy sample could not see them.

**F3 major: a missing or unusable curated answer still reads as an AI matter on the item and in seven steps.** `probe-r3-branch-missing.out`: e1's own `why` in `GET /api/cases/{tok}` and `GET .../items/e1` is "The demo has no recorded AI answer for this step" (`why.py:17`; `present.py:276` swaps only when `item.prepared`, and a miss is `prepared: false`), while the trace reason for the same item says "no prepared answer". The seven check steps say "Not run: the AI gave no usable answer for this record" (`trace.py:307-308`); no AI was asked. AC1 forbids "recorded AI answers" on a curated item. The extracted step itself is now correct (FAIL, no model, "There is no prepared answer for this record in the demo").

**F4 minor: the prompt-version and hash fix has no test.** Mutants on the archive copy that put the prompt version back survive: M6 (`trace.py` evidence), M7 (`present.py` `_call`, audit rows) and M8 (`api.py` export `prompt_versions`) all leave the 22 prepared-provenance tests and the 144 trace, audit and export tests green (`mutants-r3.out`). The round-2 acceptance test for F-D was not written.

**F5 minor: the export notes line says "drafted with AI assistance" for a curated export.** `export.py:29`, used at `:733`; `probe-r3-curated.out` shows it in `internal_notes_text` of the sample export while `provenance.generator_prepared` is true. Not item-level and not in the letter, so I did not rate it above minor. Fix: a prepared variant ("built from answers prepared by the team and checked by a second AI model") when the case's models are prepared.

**F6 nit: the skipped "Prepared answers did not include this flag" step carries the kind tag "AI check".** `render-flags-r3.out`, f_r7_1: key step `('proposed_by_ai', 'AI check', ...)`. The step ran no AI.

## What I exercised

Own servers from the archive on loopback ports 54310 (demo mode, no `ZLAYT_MODE`) and 54311 (`ZLAYT_MODE=local`), both `LLM_BACKEND=fixture FIXTURE_SET=curated`. PIDs 25329 and 26866; cwd checked before `kill`; both listeners gone afterwards. The shared app and other agents' processes were not touched.

Grep of every API response (health, case, judges, audit, trace, status, every item and item trace, export after accept-all) for "AI drafted", "AI found" and model names:
- **Sample, demo mode** (`probe-r3-curated.out`): 16 of 23 items prepared (9 entries, 7 flags; the 4 amounts and 3 code-made flags are not model answers). Two hits, neither on an item: the case trace "the AI disclosure line will count them" and the export notes line (F5). No model name anywhere.
- **Sample, local mode** (`probe-r3-curated-local.out`): the same two hits.
- **Library cases** (local mode only; the library route is 404 in demo mode): case_lib01, lib02, lib09, lib10 run on the recorded answers (the curated set has 19 files, all for the sample). `prepared==True` on 0 items, `models.generator` claude-sonnet-5-5, and the AI labels there are correct. The banner under a curated process saying "prepared by our team" while a library case shows recorded labels is the accepted F4 mixed set. No finding.

`/classic`: demo mode, `GET /classic`, `/classic/`, `/classic/index.html`, `/classic/app.js` all 307 to `/`. Local mode: `/classic` 307 to `/classic/`, which is 200, and `/classic/app.js` 200. `ZLAYT_CLASSIC=1` over HTTP I did not run; the worker's unit tests for it pass.

Tests in the archive: `pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py`: 22 passed (`unit-prepared.out`). `E2E_REQUIRE_DB=1 pytest tests/e2e/test_demo_provenance.py`, base URL unset: 7 passed (`e2e-provenance.out`); that file still has no flag test (`grep -c -i flag` returns 0). Mutants, each restored from `git show 2e58e18:<path>` and cmp-identical: M1 `to_prepared` identity, M2 flag call lookup off, M3 `/classic` always open, M4 placeholder branch off, M5 FIXTURE_MISS not excluded from `models_for` are all killed; M6, M7, M8 survive (F4). Not run: the full unit suite and the eval runner, which the brief did not ask for.

## Verdict rule

Two blockers (F1, F2), so `fail`. F3 is major; F4 and F5 minor; F6 nit.

```json
{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 3 (final). git archive of 2e58e18 (HEAD is now fa4f79e, which changes export.py and present.py after 2e58e18; those hunks not reviewed); sample case on FIXTURE_SET=curated in demo mode (port 54310) and local mode (port 54311); library cases lib01, lib02, lib09, lib10 on the local server; own PIDs 25329 and 26866 stopped",
 "exercised": [
  "python3 tools/board.py show T-177; reviews/T-177-staff-engineer-r2.md; D-065 row in memory/ORCHESTRATOR_DECISIONS.md; git show 2e58e18 -- app/ memory/contracts/api.md (full diff read)",
  "git archive 2e58e18 into artifacts/review-evidence/T-177-staff-engineer-r3/archive (archive-source-sha.txt = 2e58e18)",
  "python -m app.main from the archive, demo mode, port 54310, PID 25329; local mode, port 54311, PID 26866 (cwd checked with lsof before kill, listeners gone after)",
  "probe_r3_http.py: sample on demo and local servers, plus library lib01, lib02, lib09, lib10 on the local server; every payload scanned for AI-authorship wording and model names (probe-r3-curated.out, probe-r3-curated-local.out)",
  "render_flags_r3.py (Playwright, /classic on the local server): Why panel of all 10 flags and 9 entries via ZL.stepper.openTrace; 0 bad hits, 0 page errors; screenshots render-r3-*.png (render-flags-r3.out)",
  "probe_r3_branch.py modes unsupported, missing, schema, amount: curated copy in a dir named curated with one answer changed; every sentence of the affected item, case trace, judges models, audit row (probe-r3-branch-*.out)",
  "probe_r3_edit.py on the demo server: quote edit, summary edit and flag note edit of curated items; edits refused 422 by code checks or clean; export notes line (probe-r3-edit.out)",
  "curl of /classic, /classic/, /classic/index.html, /classic/app.js on both servers: 307 to / in demo mode; 307 to /classic/ then 200 in local mode",
  "pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py in the archive: 22 passed (unit-prepared.out)",
  "E2E_REQUIRE_DB=1 pytest tests/e2e/test_demo_provenance.py in the archive, base URL unset: 7 passed (e2e-provenance.out)",
  "mutate_r3.py M1-M8 on the archive copy, restored from git show 2e58e18 and cmp-identical: M1-M5 killed, M6-M8 survive (mutants-r3.out)",
  "grep over archive app/backend for AI-authorship sentences (trace.py, why.py, present.py, pipeline.py, review.py, export.py) compared with the why.py swap table"
 ],
 "verdict": "fail",
 "scores": {"provenance_honesty": 3, "pm_acceptance_criteria": 3, "test_strength": 3, "llm_boundary": 5},
 "findings": [
  {"severity": "blocker", "title": "A malformed curated answer flips the whole case back to 'Drafted by claude-sonnet-5-5' and 'AI-made'",
   "evidence": "probe-r3-branch-schema.out (curated copy, e1 summary key removed): case.models and /judges models = {generator: claude-sonnet-5-5, generator_prepared: false}; case-trace extract label 'AI drafts a summary and a quote for each record', why '1 record has no AI-made entry. The AI step failed on all three attempts'; judges label 'Second AI check on every AI-made item'; /api/health in the same run still answers 'prepared'. Cause: attempt 1 is a SCHEMA_INVALID row with no recorded_from, attempt 2 is FIXTURE_MISS (excluded), so app/backend/present.py:309-310 gets all(is_prepared) over one non-prepared row = False. app/frontend/judges.js:168-171 prints 'Drafted by ' + m.generator when prepared is false (read, not rendered for this variant). tests/unit/test_prepared_provenance_r3.py:144 (schema param) reads only e1's extracted step.",
   "why_it_matters": "This is round-1 F1 (a blocker): the case, judges and trace payloads name a model as the drafter of eight hand-written answers. D-065 and AC1 forbid it. The shipped curated files do not reach it, but any edit that breaks one curated answer does, and the run then also contradicts /health.",
   "fix": "In models_for, decide prepared from the answers that exist: ignore generator rows that failed (parsed_ok false, or error SCHEMA_INVALID / FIXTURE_MISS) when the set in use is the curated one, or take it from AU.answers_prepared(). When it is prepared, the case trace extract/judges labels and the judge panel must read the prepared wording whatever one record did.",
   "acceptance_test": "Unit: curated copy named curated with e1's summary key removed, run the sample (partial run allowed); assert case.models.generator == 'hand-checked (qa)' and generator_prepared is true on GET /api/cases/{tok} and /judges, the case-trace extract label has no 'AI drafts' and no 'AI-made', and no payload contains 'claude-sonnet'. Mutation: restoring the all(...) over unfiltered rows must fail it."},
  {"severity": "blocker", "title": "Fixed AI-authorship sentences outside the swap table survive on prepared items (failed answer, code trims)",
   "evidence": "probe-r3-branch-unsupported.out: e1 prepared true, model 'hand-checked (qa)'; seven steps (excerpt_verbatim, excerpt_whole_sentence, excerpt_hedge, summary_tokens, summary_qualifier, highlight, judge_1) say 'Not run: code removed the whole AI summary because the quote does not support it' (app/backend/trace.py:306). probe-r3-branch-amount.out: e2 prepared true and verified; excerpt_narrowed says 'from the quote the AI picked' (trace.py:387), charge_clause_removed says 'from the end of the AI's summary' (trace.py:393; :407 after a quote edit). The swap table at app/backend/why.py:89-111 has none of these; _skipped (trace.py:302-309) is not run through it. Test regex tests/unit/test_prepared_provenance_r3.py:16 has no 'AI summary', 'AI picked', 'AI gave', 'AI answer'.",
   "why_it_matters": "These sentences tell the reader an AI wrote or picked text the team wrote, on a prepared item. That is the D-065 rule and the orchestrator's round-3 brief ('every backend-generated text for a prepared item says prepared, never AI drafted'). Round 2 rated the same class of latent failed-prepared text a blocker (F-B) and the headline step alone was fixed. A closed list of sentences fails for the next sentence added.",
   "fix": "Route every first-answer sentence of a prepared item through one place: add the missing sentences to to_prepared and run _skipped and the trim steps through it for prepared items; better, build those sentences from the prepared flag at the source. Extend the test regex with 'AI summary', 'AI picked', 'AI gave', 'AI answer', \"AI's\".",
   "acceptance_test": "Unit, curated copies: (a) e1 summary with no supported clause; (b) ER entry quote and summary stating $6,240. For every step, state_reason and next_action of the affected item, no match for the extended regex. Plus a source scan: every string literal in trace.py and why.py that matches r\"\\bAI\\b\" authorship phrases either is in the swap table or is marked as a second-check sentence. Mutation: remove one swap row and one routing call; each must fail."},
  {"severity": "major", "title": "A missing or unusable curated answer still reads as an AI matter on the item and in seven steps",
   "evidence": "probe-r3-branch-missing.out (curated copy, e1 answer file removed): GET /api/cases/{tok} and GET .../items/e1 give why 'The demo has no recorded AI answer for this step, so this item has not been checked.' (app/backend/why.py:17; present.py:276 swaps only when item.prepared, and a miss is prepared false) while the trace reason for the same item reads 'no prepared answer'. Seven steps read 'Not run: the AI gave no usable answer for this record.' (trace.py:307-308). AC1: no 'recorded AI answers' on a curated item.",
   "why_it_matters": "Two surfaces disagree about one item, and the item-level one uses the phrase the card forbids; the steps say an AI was asked when only a fixture lookup missed. The extracted step itself is now correct, so the round-2 F-C fix is half done.",
   "fix": "On the curated set, treat a FIXTURE_MISS or unusable generator row as a prepared-answer matter for the item's why/explanation as well (answers_prepared() already exists), and give _skipped a prepared wording ('Not run: there is no prepared answer for this record.').",
   "acceptance_test": "Unit: curated copy minus e1's answer file; e1 item why and explanation, all trace steps and reasons contain none of 'recorded AI', 'AI gave', 'the AI'; the item payload and the trace reason agree on 'prepared answer'."},
  {"severity": "minor", "title": "The prompt-version and hash fix (round-2 F-D) has no test: three mutants survive",
   "evidence": "mutants-r3.out: M6 (trace.py _llm_evidence puts prompt_version back), M7 (present.py _call puts prompt_version and prompt_sha256 back), M8 (api.py export prompt_versions includes prepared calls) each leave tests/unit/test_prepared_provenance_r3.py + test_prepared_provenance.py (22 passed) and test_t183_hardening + test_trace + test_audited + test_export (144 passed) green.",
   "why_it_matters": "A prompt version and hash on a hand-written answer says a prompt produced it. The round-2 acceptance test was not written, so the next edit can bring it back unnoticed.",
   "fix": "Add the round-2 acceptance test.",
   "acceptance_test": "Unit on the curated sample: every audit row with prepared true has prompt_version None and prompt_sha256 None; every prepared step has evidence.prompt_version None; export provenance.prompt_versions has no extract_v1 or flags_v1. M6, M7 and M8 must each fail it."},
  {"severity": "minor", "title": "Export notes say 'drafted with AI assistance' for a curated export (not a blocker: internal notes only, labels no item)",
   "evidence": "app/backend/export.py:29 (AI_LINE), used at :733; probe-r3-curated.out: the sample export's internal_notes_text contains 'This chronology was drafted with AI assistance' while provenance.generator_prepared is true. The letter text carries no AI statement (D-009 holds).",
   "why_it_matters": "The badge says the answers were not written by an AI model; the exported notes of the same demo say the chronology was drafted with AI help. A reader can see both. It is accurate that a second AI model checked the items.",
   "fix": "When the case's models are prepared, use a variant: 'This chronology was built from answers prepared by the team and checked by a second AI model; every item in the treatment section was accepted by the paralegal. Items not reviewed: {n}.'",
   "acceptance_test": "Unit: GET /export on the curated sample: internal_notes_text has no 'drafted with AI'; on the recorded set it still does."},
  {"severity": "nit", "title": "The skipped flag step 'Prepared answers did not include this flag' carries the kind tag 'AI check'",
   "evidence": "render-flags-r3.out, f_r7_1: key step ('proposed_by_ai', 'AI check', '- / Prepared answers did not include this flag / AI check / Skipped ...').",
   "why_it_matters": "The tag says an AI check ran on a step that was skipped.",
   "fix": "Use the 'Prepared answer' or 'Skipped' tag for prepared skipped steps.",
   "acceptance_test": "E2E on the curated sample: the f_r7_1 Why panel's proposed_by_ai step-kind is not 'AI check'."}
 ],
 "whats_right": [
  "On the shipped curated sample all 19 Why panels (10 flags, 9 entries) and every API payload are free of 'AI found it', 'AI drafted' and model names on prepared items; the judge line reads 'Prepared by our team'.",
  "The failed-prepared headline step keeps the Prepared label, and a missing answer is a FAIL step with no model evidence; the M1-M5 mutants (swap table, flag call lookup, /classic gate, placeholder branch, FIXTURE_MISS exclusion) are each killed by the new tests.",
  "/classic redirects to / in demo mode (all four paths) and stays reachable in local mode; the recorded set keeps its AI labels and model ids."
 ],
 "questions_for_chris": [
  "Should the exported internal-notes line differ for the prepared demo (F5)? I rated it minor because it sits in notes marked DO NOT SEND and labels no item; if you read D-065 as covering document-level wording, it is a major."
 ]}
```
