# T-177 (D-065 honest demo provenance): staff-engineer review

**Verdict: fail (1 blocker, 2 majors, 1 minor, 1 nit).** The PM's acceptance test passes on commit 04ea2bf: no "AI draft" or "recorded AI answers" text on a curated item, the trace generator step reads `hand-checked (qa)` with a prepared-answer label, the audit rows carry `hand-checked (qa)`, and the recorded set keeps its AI labels. The provenance is not complete, though. On the curated demo, the "How the AI was checked" panel still says `Drafted by claude-sonnet-5-5`, and the case and judges payloads still name `claude-sonnet-5-5` as the generator. That is the exact over-claim D-065 forbids, and no test covers it. The badge tooltip also points to an eval report that does not hold the answers.

Scope: commit 04ea2bf (the card commit). HEAD de5cb3a has no diff under `app/` or `tests/` relative to 04ea2bf, so the archive matches HEAD for code. Evidence is under `artifacts/review-evidence/T-177-staff-engineer/` (git archive copy) and the `artifacts/review-evidence/T-177-staff-engineer-*` files.

## Acceptance checks (PM's test, curated and recorded)

| Check | Result |
|---|---|
| `tests/unit/test_prepared_provenance.py` | 6 passed |
| `E2E_REQUIRE_DB=1 tests/e2e/test_demo_provenance.py` | 4 passed |
| `/items/e1/trace` generator step model | `hand-checked (qa)`, label "Prepared answer, standing in for the AI draft" |
| `/audit` generator rows (curated) | 18 of 18 `hand-checked (qa)`, `prepared: true` |
| Curated page text | no "AI draft" or "recorded AI answers"; badge "Demo: sample answers prepared by our team" |
| Recorded set labels | "AI draft", model `claude-sonnet-5-5`, badge "Demo: recorded AI answers" |

## Findings

**F1 (blocker): the curated demo still names a model as drafter.** On the curated set, the "How the AI was checked" panel renders `Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5` and the label "how a second AI model checked the first AI's drafts". The same payloads name the generator as `claude-sonnet-5-5`. `app/backend/present.py:262` says the provenance exists "so no screen or payload names a model for an answer no model gave". The panel and payloads contradict that comment and D-065 ("never presented as model output"). The new tests pass because they only assert the trace, audit, item and health fields.

**F2 (major): the tooltip names a place the answers are not.** `app/frontend/app.js:16-17` says "The AI's own answers on these cases are in the evaluation report." The run files store `summary_sha`, not the summary or excerpt text. `evals/reports/runs/20261102T093020Z/sample.json` item keys are `date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha`. The only report text that contains the sample summary's opening words is a quoted phrase in `evals/reports/determinism-diagnosis.md:26`. The tooltip text is pinned by D-065, so this needs a decision (see questions).

**F3 (major): the curated banner says "checked by code" and omits the AI check.** `app/backend/api.py:37` (PREPARED_BANNER) reads "...prepared by our team and checked by code; you decide every item". On the same curated items, the trace has a "Second AI check" step (`judge_1`, model `claude-haiku-5-5`, `prepared: false`) and the judges endpoint counts 19 items checked by AI. The banner under-states who checked the items.

**F4 (minor): the banner is global, provenance is per call.** `app/backend/api.py:125-129` (`answers()`) decides prepared versus recorded from the fixture set name alone, while item provenance is per call (`app/backend/present.py:262-273`, `app/llm/audited.py:68-79`). `app/llm/backends/fixture.py:23-24` falls back to the recorded set when a curated key is missing. A curated run with one missing key would show a recorded AI answer labelled "AI draft" under a banner saying all summaries were prepared. Not reproduced on the sample: 9 of 9 extract and 9 of 9 flag calls are `prepared: true`.

**F5 (nit): prepared rows still carry a prompt version.** The curated probe's audit row has `"prompt_version": "extract_v1"`, a real `prompt_sha256`, and `"prepared": true`. `app/frontend/timeline.js` (why-generator line) shows "hand-checked (qa) · extract_v1". No prompt produced these answers.

## Commands and outputs

- `git show --stat 04ea2bf`; `git diff 04ea2bf HEAD -- app tests | wc -l` gives 0.
- `python3 tools/board.py show T-177`: status in_review, AC 1 done with evidence.
- `reviews/GATE-M3-product-manager.md` blocker read; `memory/ORCHESTRATOR_DECISIONS.md` D-065 to D-068 read.
- `git archive 04ea2bf` extracted to `artifacts/review-evidence/T-177-staff-engineer/`.
- Unit and e2e outputs: `artifacts/review-evidence/T-177-staff-engineer-unit-prepared.out`, `artifacts/review-evidence/T-177-staff-engineer-e2e-provenance.out`.
- API probes (TestClient, curated and recorded): `artifacts/review-evidence/T-177-staff-engineer-curated-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-curated-judges.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out`. Probe scripts: `artifacts/review-evidence/T-177-staff-engineer-probe.py`, `artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py`.
- Browser render of the curated case on a private server: `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out` and `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png`.
- Mutation checks, in the archive copy and restored from `git show 04ea2bf:...` (cmp identical): removing `_prepared_model` in `app/llm/audited.py` fails 5 tests; forcing `is_prepared` to False fails 3 unit tests.
- Grep of tests for `models` assertions: none for the judges or case payloads.
- The shared app on :7860 (PID 86899) was not touched. My two private server PIDs (94279, 94777) were terminated; `ps` confirms none alive.

## What is right

- Audit and trace model swap is mutation-guarded: removing the audit model swap or forcing the prepared flag off makes 3 to 5 tests fail.
- The PM's acceptance points hold on 04ea2bf: prepared trace label, `hand-checked (qa)` audit rows, recorded set keeps AI labels and model ids.
- `memory/contracts/api.md:57` and `:836-841` document `answers`, `prepared` on items, audit, trace and narrative, and the payloads I observed match them.

## Verdict rule

One blocker (F1), so `fail`. Majors F2 and F3 must also be fixed before the gate.

```json
{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 04ea2bf (card commit; HEAD de5cb3a has no app/ or tests/ diff from it); git archive copy at artifacts/review-evidence/T-177-staff-engineer/; no app URL (private servers on random loopback ports; shared :7860 untouched); sample case (sample=True) on FIXTURE_SET=curated and on the recorded set",
 "exercised": [
  "python3 tools/board.py show T-177; git show --stat 04ea2bf; git diff 04ea2bf HEAD -- app tests (0 lines)",
  "reviews/GATE-M3-product-manager.md blocker; memory/ORCHESTRATOR_DECISIONS.md D-065 to D-068",
  "git archive 04ea2bf extracted; read app/backend/present.py, trace.py, api.py, app/llm/audited.py, app/llm/backends/fixture.py, app/frontend/app.js, judges.js, stepper.js, timeline.js, audit.js; read the two new test files",
  ".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q: 6 passed",
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v: 4 passed",
  "TestClient probes on curated and recorded sets: /api/health, /api/cases/{tok}, /audit, /items/e1/trace, /judges",
  "Playwright on a private curated server: read badge, badge title, banner, judge-label, judge-model-line, judge-totals; screenshot of the judge panel",
  "Mutation checks in the archive copy: audit model swap removed (5 failed); is_prepared forced False (3 failed); file restored and cmp-verified",
  "Inspected evals/reports/runs/20261102T093020Z/sample.json keys; grep of evals/reports for the sample summary text",
  "Grep of tests for models/judge-model-line assertions (none for judges or case payloads)",
  "memory/contracts/api.md lines 57 and 836-841 read against the code"
 ],
 "verdict": "fail",
 "scores": {"provenance_honesty": 2, "pm_acceptance_criteria": 4, "api_fields_documented": 4, "test_strength": 3, "llm_boundary": 5},
 "findings": [
  {"severity": "blocker", "title": "Curated demo still names claude-sonnet-5-5 as the drafter of hand-written answers (judge panel, case and judges payloads)",
   "evidence": "Rendered curated case (artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out): judge-model-line 'Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5'; judge-label \"how a second AI model checked the first AI's drafts\"; screenshot artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png. app/frontend/judges.js:166-168 renders m.generator from d.models. app/backend/trace.py:1003 returns 'models': cx.models (config). GET /api/cases/{tok}/judges on FIXTURE_SET=curated returns models.generator 'claude-sonnet-5-5' (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out). GET /api/cases/{tok} on curated returns models.generator 'claude-sonnet-5-5'. app/backend/present.py:262 comment says no payload names a model for an answer no model gave.",
   "why_it_matters": "D-065 (binding): curated answers are never presented as model output. The panel is part of the demo the PM tested and it attributes the team's hand-written summaries to a named model. The paralegal or a reviewer reading the panel gets the wrong provenance. The new tests pass because they check trace, audit, item and health fields only, so the same blocker class would pass CI again.",
   "fix": "On a prepared case, the drafter line says the summaries were prepared by the team (no model), for example 'Drafted by: prepared answers (hand-checked by the team), checked by claude-haiku-5-5'. GET /api/cases/{tok} and GET /judges return models.generator as null or 'hand-checked (qa)' when the case's generator answers are prepared. The judge-label sentence follows the same rule. Recorded and live cases are unchanged.",
   "acceptance_test": "Unit: on FIXTURE_SET=curated, GET /api/cases/{tok}/judges and GET /api/cases/{tok} have models.generator != 'claude-sonnet-5-5'. E2E (curated): the judge-model-line text does not contain 'claude-sonnet-5-5' and says the summaries were prepared. E2E (recorded set): the same line still says 'claude-sonnet-5-5'."},
  {"severity": "major", "title": "Badge tooltip says the AI's answers are in the evaluation report; they are not",
   "evidence": "app/frontend/app.js:16-17: \"The AI's own answers on these cases are in the evaluation report.\" evals/reports/runs/20261102T093020Z/sample.json item keys: date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha (no summary or excerpt text). The only evals/reports text with the sample summary's opening words is a quoted phrase at evals/reports/determinism-diagnosis.md:26.",
   "why_it_matters": "The tooltip is the one place the demo tells a reader where to verify the AI's own answers. It sends them to a file that holds hashes and verdicts. That is a false pointer on a provenance label, the kind of over-claim the PM blocked.",
   "fix": "Either write each entry's generator summary and excerpt for the sample case into the eval report (an eval-runner change, with a report path) or reword the tooltip to what the report holds. The sentence is pinned by D-065, so the wording needs a decision (see questions_for_chris).",
   "acceptance_test": "Either: a new evals/reports/*.md contains the sample case's generator summaries and excerpts, and a unit test greps for one of them. Or: the tooltip text is changed, and the e2e test asserts the new text."},
  {"severity": "major", "title": "Curated banner says 'checked by code' and omits the AI check that runs on the same items",
   "evidence": "api.py:37 PREPARED_BANNER: 'In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item' (rendered: artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out line 2). Same curated items: trace step judge_1 'Second AI check: is the summary supported by the quote?', model claude-haiku-5-5, prepared false (artifacts/review-evidence/T-177-staff-engineer-curated-probe.out); /judges items_judged 19 (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out).",
   "why_it_matters": "The banner states who checked the items. It leaves out that a second AI model checked every item, so the page contradicts itself ('checked by code' above a 'Second AI check' step). D-065 requires plain wording to stay truthful.",
   "fix": "Rewrite the prepared banner to name both: prepared by the team, then a second AI model checked each summary against its quote, and the reader decides every item.",
   "acceptance_test": "Unit: GET /api/health on FIXTURE_SET=curated has answers 'prepared' and an ai_banner that mentions a second AI check and does not say 'checked by code' alone."},
  {"severity": "minor", "title": "Banner and badge are decided per fixture set, while provenance is per call; a missing curated key would mislabel an item",
   "evidence": "app/backend/api.py:125-129 answers() uses fixture.answer_source() (app/llm/backends/fixture.py:48-50, fixture_dir().name only). Per-call provenance: app/backend/present.py:262-273, app/llm/audited.py:68-79. app/llm/backends/fixture.py:23-24 falls back to the recorded set when a curated key file is missing. Not reproduced: curated probe shows 9 of 9 extract and 9 of 9 flags calls prepared true.",
   "why_it_matters": "On a curated run with one missing key, the item would be a recorded AI answer labelled 'AI draft' under a banner saying all summaries were prepared by the team. Provenance would be wrong on exactly the case where the fixtures are incomplete.",
   "fix": "Derive the badge and banner from the items shown (all prepared, all recorded, or mixed), or fail the run when a curated set misses a key instead of falling back.",
   "acceptance_test": "Unit: copy the curated set minus one generator file into a temp LLM_FIXTURE_DIR named curated and FIXTURE_SET=curated; the run fails or the health answers value is 'mixed', never 'prepared'."},
  {"severity": "nit", "title": "Prepared rows still show a prompt version and prompt hash",
   "evidence": "Curated probe, audit row: \"prompt_version\": \"extract_v1\", \"prompt_sha256\": \"b74b563d...\", \"prepared\": true (artifacts/review-evidence/T-177-staff-engineer-probe.py, AUDIT_ONE line). app/frontend/timeline.js why-generator line shows '${lad.generator.model} · ${lad.generator.prompt_version}', which renders 'hand-checked (qa) · extract_v1'.",
   "why_it_matters": "A prompt version and hash say a prompt produced the answer. Nothing was prompted; the team wrote it. Small, but it is the same provenance question in a different field.",
   "fix": "On prepared rows, set prompt_version to null and show 'hand-written for the demo' in the why line, or omit the prompt hash.",
   "acceptance_test": "Unit: prepared audit rows have prompt_version null (or a 'hand-written' marker) and no prompt_sha256 used as a model prompt."}
 ],
 "whats_right": [
  "Audit model swap and prepared flag are mutation-guarded: removing the audit model swap fails 5 tests; forcing is_prepared False fails 3 (archive copy, restored, cmp-verified).",
  "PM acceptance holds on 04ea2bf: trace generator step model 'hand-checked (qa)' with the prepared label; the recorded set keeps 'claude-sonnet-5-5' and the AI wording.",
  "memory/contracts/api.md:57 and :836-841 document answers, prepared fields on items, audit, trace and narrative; the observed payloads match."
 ],
 "questions_for_chris": [
  "D-065 pins the tooltip 'The AI's own answers on these cases are in the evaluation report.' The report does not hold them. Do you want the sample case's per-entry answers written into the eval report (a runner change), or the tooltip reworded now?",
  "On the curated demo, the second AI check is a real recorded model answer (claude-haiku-5-5). Should the 'How the AI was checked' panel stay on the curated set with the wording fixed (F1), or be hidden there?"
 ]}
```
