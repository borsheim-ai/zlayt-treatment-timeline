# T-177 round 2 (D-065 honest demo provenance): staff-engineer-reviewer

**Verdict: fail (2 blockers, 1 major, 1 nit).** The round-1 fixes hold on the surfaces round 1 named: the judge panel, the badge tooltip, the banner, and the case, judges, health and export `models` fields. The round is not complete. On the curated demo, the flag Why panels still say "AI found it" with the kind tag "AI draft". A curated item whose summary fails a code check is still labelled "AI drafted". A curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5. The last one is a different path from the accepted mixed-set F4, and I have not treated it as covered by that acceptance.

**Scope.** Card commit 4fcf9cd. HEAD moved during the review from ac678bc to 4671eee, so the review is on `git archive 4671eee` (`artifacts/review-evidence/T-177-staff-engineer-r2/archive-source-sha.txt`). The later commits are d07bf9d (D-065 tooltip wording, docs only) and 4671eee (T-183: create-case error text and the /classic mount). Neither touches provenance code. The curated set is FIXTURE_SET=curated; the recorded set is the control.

**Round-1 status**

| Round-1 item | Status at 4671eee |
|---|---|
| F1 blocker: drafter named on the judge panel and in case/judges payloads | Fixed for the judge panel, case, judges, health, export and case-level trace. Not complete: flags (F-A) and failure branches (F-B) |
| F2 major: tooltip points at the eval report | Fixed. The tooltip string equals the committed D-065 text |
| F3 major: banner says "checked by code" only | Fixed. The banner names the second AI model |
| F4 minor: per-call provenance vs per-set banner | Accepted as debt for the mixed set (per Chris). A missing-key variant is F-C, not covered by that acceptance |
| F5 nit: prompt version on prepared rows | Hidden in the UI only. The API and export still carry it (F-D) |

## Findings

**F-A blocker: flag items on the curated demo are labelled "AI found it" / "AI draft".** Rendered Why panels, own server, curated set: `render-flags-r2.out` shows f_r3_1 and f_r6_1 with step `proposed_by_ai`, kind `AI draft`, text "AI found it ... The AI proposed this flag as a category and a quote". Seven flag items on the sample carry this step (`probe-r2-flags.out`). The audit has 9 `flags` generator rows, all `hand-checked (qa)` with `prepared: true` (`probe-r2-flags-audit.out`). The flag items themselves have `prepared=False` and `generator={}`. Root cause: `app/backend/flags.py:56,238,290` set `ladder.generator` to None, so `trace.py:179-181` finds no call and `prepared` is false, and `trace.py:692` prints "AI found it". The Dockerfile (line 21), run.sh (line 34) and .env.example (line 11) make the curated set the public demo default. D-065 says a curated item is never "AI draft"; the card's AC1 says the same. The r2 e2e tests open only entry Why panels, and `tests/e2e/test_demo_provenance.py` has no flag test (grep for "flag" returns nothing), so the suite stayed green.

**F-B blocker: a failed prepared item's trace says "AI drafted a summary and picked a quote".** The shipped sample does not reach it (all nine entries pass, `probe-r2.out`). Reproduction: `probe-r2-branch.out`. I replaced e1's curated summary with text no clause of which is in the quote, and the run is ready. e1's extracted step reads label "AI drafted a summary and picked a quote", status fail, reason SUMMARY_NOT_IN_QUOTE, while its evidence says `hand-checked (qa)`, `prepared: true`. The hard-coded labels are at `app/backend/trace.py:400`, `:403` and `:407`; only the PASS branch at `:411-414` reads the prepared flag. Any curated answer that fails a code check hits this.

**F-C major: a curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5.** Reproduction: `probe-r2-branch-missing.out`. I removed e1's curated answer file, and it is absent from the recorded set too. e1 is `rejected` with reason FIXTURE_MISS. Its extracted step is `pass`, "The AI read this record and proposed a one-line summary and a quote", with evidence model `claude-sonnet-5-5`, `prepared: false`. The case-level extract step in the same run is `fail` ("1 record has no AI-made entry"). Health answers `prepared` in that run. FIXTURE_MISS is not in the handled reasons at `trace.py:398-407`, so it falls to the PASS else-branch at `:411-414`. The accepted F4 debt is the mixed set. This is a missing key, so I have not treated it as covered.

**F-D nit: prepared answers still carry a prompt version and hash in the API and export.** `probe-r2.out` has 45 `extract_v1` and 93 `prompt_sha256` hits on curated payloads, for example an audit row `{model: hand-checked (qa), prompt_version: extract_v1, prompt_sha256: 98b1735e..., prepared: true}`. `probe-r2-export.out` gives curated provenance `prompt_versions: [extract_v1, flags_v1, ...]` next to `generator_prepared: true`. The UI hides these fields, but the round-1 acceptance test (prepared audit rows have no prompt_version and no prompt_sha256) is not met at the API.

**F-E minor (outside T-177 scope, observed): a flag can read "AI found it" when the why says the AI did not find it.** `probe-r2-flags.out`, f_r7_1: label "AI found it", why "The phrase list found this flag but the AI did not; check that it applies". Same branch as F-A (`trace.py:689-692`). I did not check whether recorded flags do the same.

## What I checked and found right

- The tooltip string at `app/frontend/app.js:16` equals the committed D-065 text (`git show HEAD:memory/ORCHESTRATOR_DECISIONS.md`). The rendered tooltip matches it (`render-r2.out`).
- The rendered curated page: badge "Demo: sample answers prepared by our team"; banner names "a second AI model"; judge line "Prepared by our team (not by an AI model), checked by claude-haiku-5-5". The only AI-draft text on the whole page is the D-065 phrase "standing in for the AI draft". The recorded control still says "Drafted by claude-sonnet-5-5" (`render-r2.out`).
- Mutants in the archive copy, restored from HEAD and `cmp`-identical: forcing `models_for` prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test.

## Commands, sources and what I did not run

I ran the unit file and the e2e file as the brief asked. I did not run the full `tests/unit` suite or the eval runner; neither is in the brief. Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r2/`. My own servers were on loopback ports 54001, 54056, 54205, 54304, 54440 and 54892. Their PIDs (52291, 52392, 52754, 53030, 53689) are gone. The app processes 23429, 37589, 52326 and 52906 belong to other agents, and the shared app on :7860 (86897, 86899) was not touched.

## Verdict rule

Two blockers (F-A, F-B), so `fail`. F-C is major and F-D and F-E are nit and minor.

```json
{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2. git archive of HEAD 4671eee (card commit 4fcf9cd; later commits d07bf9d docs and 4671eee T-183 api.py create-case text and /classic mount, no provenance code); archive at artifacts/review-evidence/T-177-staff-engineer-r2/archive; sample case on FIXTURE_SET=curated (prepared) and on the recorded set (control); own private servers on loopback ports 54001, 54056, 54205, 54304, 54440, 54892 (all stopped); shared app on :7860 (PID 86899) untouched",
 "exercised": [
  "python3 tools/board.py show T-177 (in_review; commits 04ea2bf, 4fcf9cd; AC1 done with evidence); reviews/T-177-staff-engineer.md read as the round-1 list",
  "git log -n 8 and git rev-parse HEAD: HEAD moved ac678bc -> 4671eee during the review; git show 4fcf9cd -- app/ (full r2 diff read); git show d07bf9d; git show 4671eee -- app/backend/api.py",
  "git show HEAD:memory/ORCHESTRATOR_DECISIONS.md D-065 row, compared byte-for-byte with app/frontend/app.js:16 tooltip: equal",
  "git archive HEAD into artifacts/review-evidence/T-177-staff-engineer-r2/archive (2432 files); archive-source-sha.txt = 4671eee",
  ".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q in the archive: 10 passed (unit-prepared.out)",
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v in the archive, base URL and ZLAYT_DB unset so the conftest starts its own private server on a free loopback port: 7 passed, 0 skipped (e2e-provenance.out)",
  "probe_r2.py (TestClient, curated and recorded): /api/health, /api/cases/{tok}, /judges, /audit, /trace, /status, /api/cases, /export and every item and item trace; pattern hits (probe-r2.out)",
  "probe_r2_export.py: accept every item, GET /export; provenance block and word scan on curated and recorded (probe-r2-export.out)",
  "probe_r2_flags.py and probe_r2_flags_audit.py: flag and amount items on curated; audit rows grouped by role, model, prepared, prompt_version (probe-r2-flags.out, probe-r2-flags-audit.out)",
  "probe_r2_branch.py: curated e1 with an unsupported summary (probe-r2-branch.out) and with the answer file removed (probe-r2-branch-missing.out)",
  "render_r2.py on own curated and recorded servers (Playwright): badge text and title, banner, judge label, judge model line, judge totals, whole-document scan (text, title, aria-label); screenshots render-*.png (render-r2.out)",
  "render_flags_r2.py on own curated server: Why panels of f_r3_1 and f_r6_1 opened via ZL.stepper.openTrace, the call btn-trace makes; step labels, kinds and whole-document scan (render-flags-r2.out; render-curated-flag-*-why.png)",
  "race_r2.py: /api/health held 3 s on own curated server; banner-ai sampled while held (race-r2.out): banner hidden until health answered, so no fallback text was shown. Not a finding",
  "mutant M1: present.py:288 prepared forced False; pytest unit file: 2 failed, 8 passed (console output, not saved); restored from HEAD, cmp identical",
  "mutant M2: judges.js:163 prepared forced false; pytest e2e -k 'judge or surface': 1 failed, 2 passed; restored from HEAD, cmp identical",
  "grep over app/ for model-name literals and drafter wording; app/frontend/mock*.js is dev-only (api.js:5 API_MODE = real)",
  "Dockerfile:21, run.sh:34, .env.example:11: curated set is the public demo default",
  "ps and lsof: my PIDs 52291, 52392, 52754, 53030, 53689 gone; other app.main PIDs (23429, 37589, 52326, 52906) and shared 86897/86899 left alone after cwd and port check"
 ],
 "verdict": "fail",
 "scores": {"provenance_honesty": 2, "pm_acceptance_criteria": 2, "test_strength": 2, "llm_boundary": 5},
 "findings": [
  {"severity": "blocker", "title": "Curated flag items show 'AI found it' with kind 'AI draft' in the Why panel; the flag items are not marked prepared",
   "evidence": "render-flags-r2.out: f_r3_1 step proposed_by_ai kind='AI draft' text='AI found it ... The AI proposed this flag as a category and a quote; it wrote no explanation' (same for f_r6_1). probe-r2-flags.out: 7 flag items with 'AI found it'; 'flags f_r3_1 ... prepared=False generator={}'. probe-r2-flags-audit.out: 9 rows (generator, flags, hand-checked (qa), True, flags_v1); 'f_r3_1 proposed_by_ai step evidence: model hand-checked (qa), prepared: false'. Root cause: app/backend/flags.py:56,238,290 set ladder.generator None; app/backend/trace.py:179-181 sets prepared from the call, which is None, so false; trace.py:692 prints 'AI found it'. Public demo default: Dockerfile:21 FIXTURE_SET=curated; run.sh:34; .env.example:11.",
   "why_it_matters": "D-065 (binding): a curated item is never 'AI draft'; card T-177 AC1: no 'AI draft' on a curated item. The public demo serves the curated set by default, so a reader sees 'AI draft' on seven flag items. The r2 e2e tests open only entry Why panels, and tests/e2e/test_demo_provenance.py has no flag test, so the suite passed.",
   "fix": "Record the generator call on each flag ladder (flags.py: generator with model, prompt_version, call_id) and take prepared from that call, or take it from the case's models.generator_prepared as models_for does. For prepared flags, proposed_by_ai uses PREPARED_LABEL and PREPARED_WHY, the stepper kind reads 'Prepared answer', the item is prepared true, and evidence.model.prepared matches the audit row.",
   "acceptance_test": "E2E on FIXTURE_SET=curated (own server): open the Why panel of every flag with an AI proposal (f_r3_1, f_r6_1, f_r8_1, f_r7_1, f_r7_2, f_r8_2, f_r9_1); assert no 'AI found it', no step-kind 'AI draft', step reads 'Prepared answer'; whole-panel scan with the D-065 phrase removed has none of 'AI draft', 'AI found it', 'claude-sonnet'. Unit: GET /api/cases/{tok}/items/f_r3_1/trace has proposed_by_ai evidence.model.prepared true and label PREPARED_LABEL on the curated set; the recorded set keeps 'AI found it' and prepared false."},
  {"severity": "blocker", "title": "A failed prepared item's trace says 'AI drafted a summary and picked a quote' (latent on the shipped sample)",
   "evidence": "app/backend/trace.py:400, :403 and :407 hard-code the label 'AI drafted a summary and picked a quote' whatever prepared is; only the PASS branch at :411-414 reads prepared. Reproduction: probe-r2-branch.out (curated copy, e1 summary replaced by text no clause of which is in the quote): e1 extracted step label 'AI drafted a summary and picked a quote', status fail, reason SUMMARY_NOT_IN_QUOTE, evidence model 'hand-checked (qa)' prepared true. Shipped sample: 9 of 9 entries pass (probe-r2.out).",
   "why_it_matters": "Same rule as F-A. The shipped sample does not reach this branch, but any edit to a curated answer that fails a code check does, and the product would tell the reader that an AI wrote a summary the team wrote.",
   "fix": "At trace.py:400, :403 and :407 choose the label and why from the prepared flag (PREPARED_LABEL and a prepared why). The reason sentence for SUMMARY_NOT_IN_QUOTE must not say 'the AI's summary' for a prepared item.",
   "acceptance_test": "Unit, curated fixture dir named curated with one e1 summary holding no supported clause: e1 extracted label contains 'Prepared' and not 'AI drafted'; repeat for SCHEMA_INVALID and LLM_FAILED_AFTER_RETRIES. Mutation: restoring the hard-coded label fails the test."},
  {"severity": "major", "title": "A curated run with one missing answer file reports a passing AI step that names claude-sonnet-5-5 (not covered by accepted F4)",
   "evidence": "probe-r2-branch-missing.out: e1 state rejected, reasons ['FIXTURE_MISS'] (absent from curated and recorded sets). e1 extracted step status 'pass', label 'AI drafted a summary and picked a quote', why 'The AI read this record and proposed a one-line summary and a quote.', evidence model claude-sonnet-5-5 prepared false. Same run: case-level extract step 'fail' ('1 record has no AI-made entry'); health answers 'prepared'. trace.py:398-407 does not handle FIXTURE_MISS; it falls to the PASS else-branch at :411-414.",
   "why_it_matters": "Accepted F4 is the mixed set. This is a missing key on the curated set. The item's own trace says an AI read a record and proposed a summary, names a model, and passes, while the item is rejected and the case trace says the step failed. The claim is invented provenance on the demo's own fixture set.",
   "fix": "Any reason not handled by the branches above gets a FAIL step that carries the reason, never PASS; a rejected item cannot show a passing generator step. Health answers and the run must not report 'prepared' when a curated set misses a key (round-1 F4 acceptance).",
   "acceptance_test": "Unit: copy the curated set minus e1's generator file to a temp dir named curated (LLM_FIXTURE_DIR) and run; e1 extracted status is not 'pass', its why does not say 'The AI read this record', and health answers is not 'prepared' (or the run fails)."},
  {"severity": "nit", "title": "Prepared answers still carry a prompt version and hash in the API and export (round-1 F5 hidden in the UI only)",
   "evidence": "probe-r2.out: 45 'extract_v1' and 93 'prompt_sha256' hits on curated payloads, e.g. audit row model 'hand-checked (qa)', prompt_version 'extract_v1', prompt_sha256 '98b1735e...', prepared true. probe-r2-export.out: curated provenance generator_model 'hand-checked (qa)', generator_prepared true, prompt_versions ['extract_v1', 'flags_v1', ...]. UI hides these in audit.js, stepper.js, timeline.js (4fcf9cd).",
   "why_it_matters": "A prompt version and hash say a prompt produced an answer nothing prompted. The round-1 acceptance test is not met at the API.",
   "fix": "On prepared rows set prompt_version and prompt_sha256 to null, and leave the prompt versions of prepared calls out of provenance.prompt_versions.",
   "acceptance_test": "Unit on the curated set: every audit row with prepared true has prompt_version None and prompt_sha256 None; GET /api/cases/{tok}/export provenance.prompt_versions has no extract_v1 or flags_v1 when generator_prepared is true."},
  {"severity": "minor", "title": "A flag can read 'AI found it' while its why says the AI did not find it (outside T-177 scope, observed)",
   "evidence": "probe-r2-flags.out, f_r7_1: step proposed_by_ai label 'AI found it', why 'The phrase list found this flag but the AI did not; check that it applies.' Same branch as F-A (trace.py:689-692).",
   "why_it_matters": "A label that contradicts its own sentence is the same honesty problem in a different field. I did not check whether recorded flags do the same.",
   "fix": "Derive the proposed_by_ai label from whether the AI proposed the flag, and state that in the same sentence.",
   "acceptance_test": "Unit: a flag the phrase list found and the AI did not has no 'AI found it' label and its why agrees with its label."}
 ],
 "whats_right": [
  "The badge tooltip (app/frontend/app.js:16) equals the committed D-065 text, and the rendered tooltip matches it (render-r2.out).",
  "On the curated page the rendered banner names the second AI model, the judge line reads 'Prepared by our team (not by an AI model)', and the only AI-draft wording is the D-065 phrase; the recorded control still names claude-sonnet-5-5.",
  "The unit and e2e guards are real: forcing models_for prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test (both restored from HEAD, cmp-identical)."
 ],
 "questions_for_chris": [
  "Does the accepted F4 debt cover a curated run with a missing answer file (F-C), or only the mixed set? I have treated F-C as not covered."
 ]}
```
