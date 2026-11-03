# Subagent: T-124 review (haiku) (T-124 review (haiku))

Source: `agent-a4e2cc0c900f86d32.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:06:35.849Z

Review board card T-124 (commit d56328a) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-124`. It added the ids `sort`, `copy-confirm` and `btn-copy-anyway` to the e2e conftest contract.

Check three things:
- the frontend actually renders each id (grep app/frontend);
- tests/e2e/test_polish_r3.py uses each id;
- `test_e2e_contract` passes on a `git archive HEAD` copy.

Write reviews/T-124-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:39.329Z

**tool call — Bash**
````
{
 "command": "cat /Users/arsis/zlayt-pm-project/personas/staff-engineer.md",
 "description": "Read the live staff-engineer persona dossier"
}
````

### User / tool · 2026-11-02T11:06:39.421Z

**tool result**
````
# Persona dossier — staff-engineer-reviewer

## 1. Identity
**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.

## 2. Day-to-day context
- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.

## 3. Goals and success criteria for this artifact
- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
- Tests fail when the code breaks and pass reproducibly.

## 4. Review checklist
1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
6. Money is handled as integer cents or `Decimal`, never float.
7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.

## 5. Red flags / dealbreakers
Each item here is a **blocker** (rate it so; never major or minor).
- A silent fallback (e.g., on judge error, mark item `verified`).
- An LLM computes a date difference, a total, or decides what is exported.
- Float arithmetic on money; a total that includes the $185 rate.
- Tests that call the real API or pass even when the verifier is stubbed out.
- Secrets or `.env` contents in code, fixtures, or logs.

## 6. Vocabulary
determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.

## 7. How I review
1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
6. File findings with file:line and the command that reproduces them.

## 8. Calibration
Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.

## 9. Sources
- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.

## 10. Limits
Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:39.595Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-124",
 "description": "Show board card T-124"
}
````

### User / tool · 2026-11-02T11:06:39.729Z

**tool result**
````
---
id: "T-124"
title: "test_e2e_contract fails: missing test ids after T-060 r3"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:02:26Z"
updated_at: "2026-11-02T11:06:32Z"
claimed_by: "qa"
claimed_at: "2026-11-02T11:02:43Z"
rounds: 0
commits: ["d56328a"]
reviews: []
ac:
  - {"n": 1, "text": "tests/unit/test_e2e_contract passes on a clean HEAD; ids added or the contract updated with a reason", "done": true, "evidence": "tests/unit/test_e2e_contract.py 3 passed; full unit suite 2808 passed, 1 failed (unrelated: test_t114 lib09 j4 judge fixture f_r1_1)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:02:43Z qa: claimed
- 2026-11-02T11:06:25Z qa: AC 1 checked: tests/unit/test_e2e_contract.py 3 passed; full unit suite 2808 passed, 1 failed (unrelated: test_t114 lib09 j4 judge fixture f_r1_1)
- 2026-11-02T11:06:25Z qa: Unrelated unit failure seen: test_t114_rates_and_demo_judges[case_lib09_spanish_interpreter_espalda] JUDGE_NOT_RUN f_r1_1 (j4 call failed). Needs its own card.
- 2026-11-02T11:06:25Z qa: moved in_progress -> in_review
- 2026-11-02T11:06:32Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: the 3 missing ids (sort, copy-confirm, btn-copy-anyway) are used by tests/e2e/test_polish_r3.py and rendered by app/frontend (timeline.js, export.js) but were never declared in the conftest contract. Nothing dropped, so declared them with a reason; no coverage lost. How verified: test_e2e_contract 3 passed; full unit 2808 pass, 1 unrelated fail (t114 lib09 j4 fixture). Left: lib09 failure needs its own card.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:39.960Z

**tool call — Bash**
````
{
 "command": "git show --stat d56328a && git log --oneline -3 && git rev-parse HEAD",
 "description": "Show commit d56328a stats and HEAD"
}
````

### User / tool · 2026-11-02T11:06:40.102Z

**tool result**
````
commit d56328a2f6d37d0a09c4a9e14c66e726a417eb82
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:06:22 2026 -0600

    test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
    
    Used by test_polish_r3 and rendered by the frontend; they were never added to the conftest contract. No ids dropped or renamed.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 tests/e2e/conftest.py | 2 ++
 1 file changed, 2 insertions(+)
d56328a test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
db7f6d0 docs(orchestrator): D-054 states the T-112 r2 salient-content trim rule (T-112 r2 major 2)
e1ce8dc fix(backend): a never-judged LLM_ONLY tray item carries its real reason, not JUDGE_UNAVAILABLE (T-122; case_05 f_r1_1 judge_unavailable 1 -> 0)
d56328a2f6d37d0a09c4a9e14c66e726a417eb82
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:43.359Z

**tool call — Bash**
````
{
 "command": "git show d56328a -- tests/e2e/conftest.py && echo \"---CONTRACT---\" && cat tests/e2e/conftest.py | head -150 && echo \"---GREP FRONTEND---\" && grep -rn -E \"sort|copy-confirm|btn-copy-anyway\" app/frontend | grep -E \"id=|id:|getElementById|querySelector|data-testid|'sort'|\\\"sort\\\"|copy-confirm|btn-copy-anyway\" | head -60",
 "description": "Show conftest diff, contract and frontend id grep"
}
````

### User / tool · 2026-11-02T11:06:43.481Z

**tool result**
````
commit d56328a2f6d37d0a09c4a9e14c66e726a417eb82
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:06:22 2026 -0600

    test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
    
    Used by test_polish_r3 and rendered by the frontend; they were never added to the conftest contract. No ids dropped or renamed.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/conftest.py b/tests/e2e/conftest.py
index e855fc6..2f4102f 100644
--- a/tests/e2e/conftest.py
+++ b/tests/e2e/conftest.py
@@ -37,6 +37,8 @@ T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an i
   (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
   A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
 T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
+T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
+  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
 T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
 T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
   dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
---CONTRACT---
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('AI suggested a flag that the second check did not confirm; it is not in the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

@pytest.fixture
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)



class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."

    def __init__(self, page, token, ids):
        self.page, self.token, self.ids = page, token, list(ids)
        self.base = {i: self._summary(i) for i in self.ids}
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
            page.route(self._re.compile(pat), fn)

    def _summary(self, i):
---GREP FRONTEND---
app/frontend/batch.js:96:    if (tb) { const old = tb.querySelector(":scope > .rv-batchbar"); if (old) old.remove(); tb.insertBefore(b, tb.querySelector(".toolbar-sort")); } else root.append(b);   // the button sits in the Timeline toolbar (T-060 r3)
app/frontend/export.js:37:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
app/frontend/export.js:38:      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
app/frontend/export.js:40:    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
app/frontend/timeline.js:257:          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
app/frontend/timeline.js:261:      el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, sortedEntries(c).map((e) => entryRow(e, c))),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:43.908Z

**tool call — Bash**
````
{
 "command": "cat tests/e2e/test_polish_r3.py | head -200; echo \"---GREP USES---\"; grep -n -E \"sort|copy-confirm|btn-copy-anyway\" tests/e2e/test_polish_r3.py",
 "description": "Read test_polish_r3 and grep id uses"
}
````

### User / tool · 2026-11-02T11:06:43.996Z

**tool result**
````
"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def active(page):
    return page.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")


def tab_until(page, testid, limit=40):
    for _ in range(limit):
        page.keyboard.press("Tab")
        a = active(page)
        if a and a["tid"] == testid:
            return a
    raise AssertionError(f"Tab never reached {testid}; last {active(page)}")


# ---- 1. the shortcut sheet
def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-shortcuts").click()
    dlg = page.get_by_test_id("shortcuts-modal"); expect(dlg).to_be_visible()
    lst = dlg.get_by_test_id("shortcuts-list")
    expect(lst.locator("kbd")).to_have_count(9)
    expect(lst.locator("dt")).to_have_count(9); expect(lst.locator("dd")).to_have_count(9)
    txt = dlg.inner_text()
    assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    # '?' from an item row opens the same sheet
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()


def test_no_object_undefined_or_null_text_on_the_review_page(page, sample_case):
    open_case(page, sample_case)
    assert not BAD_TEXT.search(page.locator("body").inner_text()), BAD_TEXT.findall(page.locator("body").inner_text())


# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
def _snapshot(page):
    return page.evaluate("""() => ({ accepted: document.querySelectorAll('[data-review=accepted],[data-review=dismissed],[data-review=edited]').length,
        dialogs: document.querySelectorAll('dialog[open]').length, active: (document.activeElement || {}).tagName + ':' + ((document.activeElement || {}).getAttribute ? document.activeElement.getAttribute('data-testid') : '') })""")


def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
    open_case(page, sample_case)
    before = _snapshot(page)
    # from the page body
    page.evaluate("document.activeElement && document.activeElement.blur()")
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    assert _snapshot(page) == {**before, "active": _snapshot(page)["active"]}, "a key acted from the page body"
    assert page.evaluate("!document.activeElement.closest || !document.activeElement.closest('[data-item-id]')")
    # from the Export button
    page.get_by_test_id("btn-export").focus()
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0 and s["active"].endswith("btn-export"), s
    # from an input: the edit box of an item, and the sort control
    page.get_by_test_id("entry-1").get_by_test_id("btn-edit").click()
    ta = page.get_by_test_id("entry-1").get_by_test_id("edit-summary"); expect(ta).to_be_focused()
    start = ta.input_value()
    for k in ("j", "a", "d", "Shift+A"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0, s
    assert ta.input_value() == start + "jadA"                       # they were typed, not run
    page.keyboard.press("Escape")
    page.get_by_test_id("sort").focus()
    for k in ("j", "a", "Shift+A"):
        page.keyboard.press(k)
    assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0


def test_letter_key_with_a_window_open_says_so(page, sample_case):
    """paralegal F11: o then a used to do nothing, silently."""
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("o"); expect(page.get_by_test_id("record-modal")).to_be_visible()
    page.keyboard.press("a")
    expect(page.locator("#rv-live")).to_contain_text("Press Escape")
    assert page.locator("[data-review=accepted]").count() == 0


# ---- 3. Tab, Enter and Space only: review one item, then export (R-RV-4)
def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_case):
    tok = sample_case
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] == "verified" and e["date"]]
    assert api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})[0] == 200   # setup by API: the checked entries are in the letter
    open_case(page, tok)
    # (a) one item reviewed by keyboard: Tab to the first skip link, Enter, then Tab to the item's Dismiss button, Enter
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-review", 6)
    page.keyboard.press("Enter")
    row = active(page); assert row["item"], row
    item = row["item"]
    tab_until(page, "btn-dismiss", 12)
    page.keyboard.press("Enter")
    expect(page.locator(f'[data-item-id="{item}"]').first).to_have_attribute("data-review", "dismissed")
    # (b) the export, from a fresh load, by keyboard only
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-export", 10)
    page.keyboard.press("Enter")
    assert active(page)["tid"] == "btn-export"
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    tab_until(page, "btn-copy-letter", 6)
    page.keyboard.press("Space")
    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
    page.keyboard.press("Enter")
    expect(page.locator("#export-status")).to_contain_text("Copied the treatment section")


# ---- 4. density
def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
    try:
        rows = pg.locator('[data-testid=queue] > article')
        assert rows.count() >= 5
        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
        first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
        assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
        visible = [bx for bx in boxes if bx[0] + bx[1] <= 900]
        assert len(visible) >= 3, boxes
        for top, h, state in boxes:
            assert h <= (170 if state == "needs_review" else 150), boxes
    finally:
        b.close()


def test_row_opens_with_more_and_closes_with_less(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
    h0 = row.bounding_box()["height"]
    expect(t).to_have_attribute("aria-expanded", "false"); t.click(); expect(t).to_have_attribute("aria-expanded", "true")
    assert "is-open" in row.get_attribute("class")
    t.click(); expect(t).to_have_attribute("aria-expanded", "false"); assert abs(row.bounding_box()["height"] - h0) < 2


def test_390_needs_review_row_is_at_most_420(pw, lib09):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
    try:
        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
        assert hs and max(hs) <= 420, hs
        assert pg.evaluate("document.documentElement.scrollWidth") <= 391
    finally:
        b.close()


# ---- 5. decided rows show a state, not a filled Accept
def test_accepted_row_has_no_filled_accept_and_undo_returns(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1")
    acc = row.get_by_test_id("btn-accept"); expect(acc).to_have_class(re.compile(r"btn--primary"))
    acc.click(); expect(row).to_have_attribute("data-review", "accepted")
    acc = row.get_by_test_id("btn-accept")
    assert "btn--primary" not in acc.get_attribute("class") and acc.inner_text().strip().startswith("Accepted")
    assert page.locator("[data-testid=entry-1] .btn--primary:visible").count() == 0
    row.get_by_test_id("btn-reset").click(); expect(row).to_have_attribute("data-review", "pending")
    expect(row.get_by_test_id("btn-accept")).to_have_class(re.compile(r"btn--primary"))


def test_dismissed_row_keeps_no_filled_accept(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-2")
    row.get_by_test_id("btn-dismiss").click(); expect(row).to_have_attribute("data-review", "dismissed")
    assert "btn--primary" not in row.get_by_test_id("btn-accept").get_attribute("class")
    assert row.get_by_test_id("btn-dismiss").inner_text().strip().startswith("Dismissed")
    assert row.get_by_test_id("btn-reset").inner_text().strip() == "Undo"

---GREP USES---
89:    # from an input: the edit box of an item, and the sort control
99:    page.get_by_test_id("sort").focus()
140:    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
141:    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
290:            if page.get_by_test_id("copy-confirm").count():
291:                page.get_by_test_id("btn-copy-anyway").click()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:44.560Z

**tool call — Bash**
````
{
 "command": "ls tests/unit | grep -i e2e_contract; find tests -name \"*e2e_contract*\"; echo \"---\"; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md",
 "description": "Locate e2e contract test and read prior memory notes"
}
````

### User / tool · 2026-11-02T11:06:44.662Z

**tool result**
````
test_e2e_contract.py
tests/unit/test_e2e_contract.py
tests/unit/__pycache__/test_e2e_contract.cpython-312-pytest-9.2.0.pyc
---
---
name: e2e-contract-review-patterns
description: T-039 round 1-2 (tests-first unit + E2E specs) patterns - contract docstring vs spec hooks, vacuous negatives, optional hooks, judge-path mutation, stub-server E2E method
metadata:
  type: project
---

Recurring patterns from the T-039 review (tests/unit/test_review_rules.py, tests/e2e/*, conftest contract docstring; reviews/T-039-staff-engineer.md and -r2.md).

- **Check the path a test actually reaches before calling a mutation "uncaught".** The first judge mutation (review.py except-branch) passed the suite, but the existing test never reaches that branch: judges.py:33 converts LLMFailed to "unavailable" first. A mutation on the reached path (judges.py to_ladder) was caught. Map which layer raises before mutating.
- **Stub-server E2E run without the app.** Serve /api/health, /api/cases, /run, /status, GET case, /review, /export in-process on a free port and point E2E_BASE_URL at it. Modes: control (golden letter), review-409, empty letter. Script: artifacts/review-evidence/T-039-r2-letter-stub.py. Useful for any E2E spec with a fixture-only dependency.
- **A contract docstring can be complete while enforcement stays needle-presence.** tests/unit/test_e2e_contract.py checks fixed substrings for roles/keys/tabindex; it does not parse keyboard.press() or get_by_role(). Re-check any "declared" claim by extracting hooks from the specs, not by grep of needles.
- **Optional hooks make proofs conditional.** `if page.evaluate("typeof window.__debugInjectRecordHtml === 'function'")` (test_source_record.py) means the textContent proof runs only when the frontend opts in. Require the hook in the contract.
- **Broad except in a health probe hides broken servers as skips.** tests/e2e/conftest.py `_up()` catches Exception; an HTTP 500 on /api/health becomes 57 green skips.
- **Red evidence goes stale.** T-039 r1 saw 39 failed / NotImplementedError; r2 saw 23 passed after the T-037 pipeline commit (d67a82d) landed. Re-run before quoting a red state; quote the run with its date and HEAD.
- **Default-argument footgun in fakes.** which_record(user, case="sample") returns [] silently for other cases; the r1 IndexError came from exactly this.

**Why:** these produced the T-039 r1 majors (contract incomplete, record_nos/IndexError, vacuous letter) and the r2 major (judge except-branch unguarded).
**How to apply:** on any E2E or tests-first card, extract hooks from specs, run a stub-server mode with a 409 and an empty output, mutate the path the test reaches, and grep for optional-hook `if` guards.

Environment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard "could not parse command safely" on long for-loops with quotes and em-dashes; put the check in a file under artifacts/review-evidence and run it. Use `-p no:cacheprovider` for pytest runs from the reviewer. `timeout` is not on this macOS shell; use the tool timeout parameter.

Related: [[project_db_review_patterns]], [[project_design_review_patterns]], [[project_harness_review_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:48.346Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_e2e_contract.py; echo \"---EXPORT.JS 25-45---\"; sed -n 25,45p app/frontend/export.js; echo \"---TIMELINE 248-262---\"; sed -n 248,262p app/frontend/timeline.js",
 "description": "Read e2e contract unit test and rendering code"
}
````

### User / tool · 2026-11-02T11:06:48.441Z

**tool result**
````
"""E2E hook contract (R-ST-1, R-RV-8): every data-testid, data-attribute, role and shortcut used by tests/e2e specs is declared in tests/e2e/conftest.py's docstring,
so the frontend builds to one source (T-039 review)."""
import pathlib, re
E2E = pathlib.Path(__file__).resolve().parents[1] / "e2e"

def contract():
    s = (E2E / "conftest.py").read_text().split('"""')[1]
    return s

def specs():
    return [p for p in E2E.glob("test_*.py")]

def test_every_test_id_is_declared():
    """R-ST-1: get_by_test_id hooks in specs are named in the conftest contract (<seq>/<raw> placeholders allowed)."""
    c = contract(); used = set()
    for p in specs():
        for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
            used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
    missing = []
    for u in used:
        pat = u.replace("<seq>", "<seq>") 
        if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
            missing.append(u)
    assert not missing, missing

def test_data_attributes_declared():
    """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
    c = contract()
    for p in specs():
        for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
            assert a in c, (p.name, a)

def test_roles_and_inputs_and_keys_declared():
    """R-RV-8: role=alert, tabindex, input names and a/d/j shortcuts are declared."""
    c = contract()
    for needle in ("role=alert", "tabindex", "input named date or provider", "a = accept", "d = dismiss", "j = next"):
        assert needle in c
---EXPORT.JS 25-45---
    if (!cs) return null;
    const bits = [[(cs.entries || []).concat(cs.undated_entries || []).filter(pend).length, "entry", "entries"], [(cs.amounts || []).filter((a) => pend(a) && a.kind === "charge").length, "charge", "charges"],
      [(cs.amounts || []).filter((a) => pend(a) && a.kind !== "charge").length, "unclear amount", "unclear amounts"], [c.pending_flags, "flag", "flags"]].filter(([n]) => n);
    return bits.map(([n, one, many]) => plural(n, one, many) + " not reviewed");
  }
  // One primary button for one task: while the confirmation is showing, Copy letter steps down and Copy anyway is the primary.
  function askConfirm(c, then, verb) {
    verb = verb || "Copy";
    const box = ZL.$("#export-confirm"), main = ZL.$('[data-testid="btn-copy-letter"]'); clear(box); box.hidden = false;
    if (main) main.classList.remove("btn--primary");
    const parts = pendingWords(c) || [plural(c.pending, "item", "items") + " not reviewed"];
    const close = () => { box.hidden = true; if (main) { main.classList.add("btn--primary"); main.focus(); } };
    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-copy-cancel", onclick: close }, "Go back")));
    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
  }
  function render() {
    const root = ZL.$("#export-body"); clear(root);
    ZL.$("#view-export").hidden = !open;
    if (!open || !data) return;
---TIMELINE 248-262---
    wrap.append(...[
      el("div", { class: "toolbar" },
        el("h2", { id: "h-timeline" }, "Timeline"),
        el("span", { class: "toolbar-counts", "data-testid": "review-counts" },
          el("span", { class: "chip chip--muted" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"}`),
          el("span", { class: "chip chip--warn", "data-icon": "alert" }, `${nNeeds} ${nNeeds === 1 ? "entry needs" : "entries need"} review`),
          el("span", { class: "chip chip--info", "data-icon": "match" }, `${nVer} quote ${nVer === 1 ? "matches" : "match"}`),
          c.undated_entries.length ? el("span", { class: "muted small" }, `${c.undated_entries.length} in Dates to confirm`) : null),
        el("label", { class: "toolbar-sort" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      ZL.stepper ? ZL.stepper.exportNotice() : null,
      hasDates ? dates : null,
      el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, sortedEntries(c).map((e) => entryRow(e, c))),
      hasDates ? null : dates, tray(c), ZL.sg ? ZL.sg.calibration() : null].filter(Boolean));   // never hand append() a bare null: it prints the word null
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:06:49.170Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; echo \"---\"; git ls-files tests/unit/test_e2e_contract.py tests/e2e/conftest.py tests/e2e/test_polish_r3.py app/frontend/timeline.js app/frontend/export.js; echo \"---ignored/untracked fixtures---\"; git ls-files --others --exclude-standard | head -20",
 "description": "Read contract test and check git tracking state"
}
````

### User / tool · 2026-11-02T11:06:49.693Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/conflicts.py
 M app/backend/export.py
 M app/backend/export_routes.py
 M app/backend/gaps.py
 M app/backend/lexicon_scan.py
 M app/backend/pipeline.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
---
app/frontend/export.js
app/frontend/timeline.js
tests/e2e/conftest.py
tests/e2e/test_polish_r3.py
tests/unit/test_e2e_contract.py
---ignored/untracked fixtures---
.claude/agent-memory/accessibility-reviewer/MEMORY.md
.claude/agent-memory/accessibility-reviewer/feedback_review_write_once.md
.claude/agent-memory/accessibility-reviewer/project_t060_pass1_findings.md
.claude/agent-memory/accessibility-reviewer/project_t060_pass2_findings.md
.claude/agent-memory/accessibility-reviewer/project_t060_pass3_findings.md
.claude/agent-memory/accessibility-reviewer/reference_a11y_harness.md
.claude/agent-memory/architect/MEMORY.md
.claude/agent-memory/architect/project_llm_boundary_docs.md
.claude/agent-memory/backend/project_t113_conflict_rules.md
.claude/agent-memory/claims-adjuster-reviewer/feedback_persona_identity_on_filing.md
.claude/agent-memory/claims-adjuster-reviewer/feedback_reviewer_write_and_parse_guards.md
.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md
.claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md
.claude/agent-memory/claims-adjuster-reviewer/project_t067_credibility_negation_and_recall.md
.claude/agent-memory/claims-adjuster-reviewer/project_t071_chip_cut_harness_sweep.md
.claude/agent-memory/claims-adjuster-reviewer/project_t092_allow_list_reading.md
.claude/agent-memory/claims-adjuster-reviewer/project_t111_positive_count_recall.md
.claude/agent-memory/claims-adjuster-reviewer/reference_spare_port_app_server.md
.claude/agent-memory/frontend/project_t060_polish.md
.claude/agent-memory/legal-nurse-reviewer/feedback_spanish_routing_and_cues.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:03.117Z

**tool call — Bash**
````
{
 "command": "H=$(git rev-parse HEAD) && echo \"HEAD=$H\" && S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head\" && mkdir -p \"$S\" && git archive HEAD | tar -x -C \"$S\" && echo \"ARCHIVE=$S\" && ls \"$S\" | head -50 && echo \"--- untracked-fixture check ---\" && ls \"$S/tests/e2e\" && echo \"--- .venv present in repo? ---\" && ls -d /Users/arsis/zlayt-pm-project/.venv && /Users/arsis/zlayt-pm-project/.venv/bin/python --version",
 "description": "Extract git archive of HEAD into scratchpad and check venv"
}
````

### User / tool · 2026-11-02T11:07:03.605Z

**tool result**
````
HEAD=d56328a2f6d37d0a09c4a9e14c66e726a417eb82
ARCHIVE=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
--- untracked-fixture check ---
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charges.py
test_code_check_refusal.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_polish_r3.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
--- .venv present in repo? ---
/Users/arsis/zlayt-pm-project/.venv
Python 3.12.2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:06.372Z

**tool call — Bash**
````
{
 "command": "S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head\"; cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider -v 2>&1 | tail -30",
 "description": "Run test_e2e_contract on the HEAD archive copy"
}
````

### User / tool · 2026-11-02T11:07:06.670Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0
rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head
plugins: platformdirs-4.14.3, anyio-4.16.0
collected 3 items

tests/unit/test_e2e_contract.py ...                                      [100%]

============================== 3 passed in 0.02s ===============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:08.537Z

**tool call — Bash**
````
{
 "command": "S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head\"; cd \"$S\" && grep -rn -E 'data-testid=\"(sort|copy-confirm|btn-copy-anyway)\"' app/frontend; echo \"--- working-tree vs HEAD for frontend ids ---\"; cd /Users/arsis/zlayt-pm-project && git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py | tail -3; echo \"(end diff stat)\"; echo \"--- parent commit contract test state ---\"; git show db7f6d0:tests/e2e/conftest.py | grep -c -E \"copy-confirm|btn-copy-anyway\"; git show db7f6d0:tests/e2e/conftest.py | grep -n -o -E \".{30}sort.{20}\" | head",
 "description": "Grep archived frontend for ids and check parent contract"
}
````

### User / tool · 2026-11-02T11:07:08.749Z

**tool result**
````
app/frontend/export.js:40:    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
--- working-tree vs HEAD for frontend ids ---
(end diff stat)
--- parent commit contract test state ---
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:12.906Z

**tool call — Bash**
````
{
 "command": "echo \"--- frontend ids (object-literal form) at HEAD ---\"; git grep -n -E '\"data-testid\": *\"(sort|copy-confirm|btn-copy-anyway)\"|data-testid=\"(sort|copy-confirm|btn-copy-anyway)\"' HEAD -- app/frontend; echo \"--- sort/copy-confirm/btn-copy-anyway occurrences in HEAD contract docstring ---\"; git show HEAD:tests/e2e/conftest.py | grep -n -o -E \".{0,25}(sort|copy-confirm|btn-copy-anyway).{0,25}\"; echo \"--- same at parent db7f6d0 ---\"; git show db7f6d0:tests/e2e/conftest.py | grep -n -o -E \".{0,25}(sort|copy-confirm|btn-copy-anyway).{0,25}\"; echo \"(end parent)\"; echo \"--- spec uses at HEAD ---\"; git grep -n -E 'get_by_test_id\\(f?\"(sort|copy-confirm|btn-copy-anyway)\"\\)' HEAD -- tests/e2e",
 "description": "Verify frontend ids at HEAD and contract occurrences before and after"
}
````

### User / tool · 2026-11-02T11:07:13.739Z

**tool result**
````
--- frontend ids (object-literal form) at HEAD ---
HEAD:app/frontend/export.js:37:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
HEAD:app/frontend/export.js:38:      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
HEAD:app/frontend/export.js:40:    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
HEAD:app/frontend/timeline.js:257:          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
--- sort/copy-confirm/btn-copy-anyway occurrences in HEAD contract docstring ---
40: contract, not dropped): sort (select in the timeline 
41:  copy-confirm (role=alert box shown wh
41: pending; export.js) and btn-copy-anyway ('Copy anyway'; takes fo
--- same at parent db7f6d0 ---
(end parent)
--- spec uses at HEAD ---
HEAD:tests/e2e/test_polish_r3.py:99:    page.get_by_test_id("sort").focus()
HEAD:tests/e2e/test_polish_r3.py:140:    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
HEAD:tests/e2e/test_polish_r3.py:290:            if page.get_by_test_id("copy-confirm").count():
HEAD:tests/e2e/test_polish_r3.py:291:                page.get_by_test_id("btn-copy-anyway").click()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:33.220Z

**tool call — Bash**
````
{
 "command": "P=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && mkdir -p \"$P/T-124-r1-parent\" && git archive db7f6d0 | tar -x -C \"$P/T-124-r1-parent\" && cd \"$P/T-124-r1-parent\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -15; echo \"--- server on 7860? ---\"; curl -s -m 3 -o /dev/null -w \"%{http_code}\\n\" http://localhost:7860/api/health || echo \"no server (curl exit $?)\"",
 "description": "Run contract test on parent archive and check server status"
}
````

### User / tool · 2026-11-02T11:07:33.946Z

**tool result**
````
            for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
                used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
        missing = []
        for u in used:
            pat = u.replace("<seq>", "<seq>")
            if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
                missing.append(u)
>       assert not missing, missing
E       AssertionError: ['copy-confirm', 'sort', 'btn-copy-anyway']
E       assert not ['copy-confirm', 'sort', 'btn-copy-anyway']

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
1 failed, 2 passed in 0.03s
--- server on 7860? ---
200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:41.110Z

**tool call — Bash**
````
{
 "command": "P=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"; S=\"$P/T-124-r1-head\"; M=\"$P/T-124-r1-mut\"; rm -rf \"$M\" && cp -R \"$S\" \"$M\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport pathlib\nm=pathlib.Path('$M')\n# mutation A: stop the frontend rendering copy-confirm (declared id, no longer rendered)\nf=m/'app/frontend/export.js'; t=f.read_text(); assert t.count('\\\"data-testid\\\": \\\"copy-confirm\\\"')==1; f.write_text(t.replace('\\\"data-testid\\\": \\\"copy-confirm\\\"','\\\"data-testid\\\": \\\"copy-confirm-gone\\\"')); print('mutA applied')\n# mutation B: spec references an undeclared id that is a substring of a declared one\n(m/'tests/e2e/test_probe_zz.py').write_text('def test_probe(page):\\n    page.get_by_test_id(\\\"btn-copy\\\").click()\\n')\nprint('mutB written')\n\" && cd \"$M\" && echo \"--- contract test on mutated copy (A: frontend stops rendering copy-confirm; B: spec uses undeclared 'btn-copy') ---\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -4; echo \"--- grep for the undeclared id the probe used ---\"; grep -n -o -E \".{0,10}btn-copy.{0,12}\" tests/e2e/conftest.py | head -3; echo \"--- health (read-only GET) ---\"; curl -s -m 3 http://localhost:7860/api/health; echo",
 "description": "Mutate scratch copy to test contract gaps and run contract test"
}
````

### User / tool · 2026-11-02T11:07:41.202Z

**tool result (error)**
````
Permission to use Bash with command P="/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad"; S="$P/T-124-r1-head"; M="$P/T-124-r1-mut"; rm -rf "$M" && cp -R "$S" "$M" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c "
import pathlib
m=pathlib.Path('$M')
# mutation A: stop the frontend rendering copy-confirm (declared id, no longer rendered)
f=m/'app/frontend/export.js'; t=f.read_text(); assert t.count('\"data-testid\": \"copy-confirm\"')==1; f.write_text(t.replace('\"data-testid\": \"copy-confirm\"','\"data-testid\": \"copy-confirm-gone\"')); print('mutA applied')
# mutation B: spec references an undeclared id that is a substring of a declared one
(m/'tests/e2e/test_probe_zz.py').write_text('def test_probe(page):\n    page.get_by_test_id(\"btn-copy\").click()\n')
print('mutB written')
" && cd "$M" && echo "--- contract test on mutated copy (A: frontend stops rendering copy-confirm; B: spec uses undeclared 'btn-copy') ---" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -4; echo "--- grep for the undeclared id the probe used ---"; grep -n -o -E ".{0,10}btn-copy.{0,12}" tests/e2e/conftest.py | head -3; echo "--- health (read-only GET) ---"; curl -s -m 3 http://localhost:7860/api/health; echo has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:44.062Z

**tool call — Bash**
````
{
 "command": "P=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"; cp -R \"$P/T-124-r1-head\" \"$P/T-124-r1-mut2\" && ls \"$P/T-124-r1-mut2/tests/e2e\" | wc -l",
 "description": "Copy HEAD archive to a fresh mutation directory"
}
````

### User / tool · 2026-11-02T11:07:44.812Z

**tool result**
````
      23
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:45.416Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-mut2/tests/e2e/test_probe_zz.py",
 "content": "def test_probe(page):\n    # 'btn-copy' is not declared in the contract; it is only a substring of btn-copy-letter / btn-copy-anyway\n    page.get_by_test_id(\"btn-copy\").click()\n"
}
````

### User / tool · 2026-11-02T11:07:45.464Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-mut2/tests/e2e/test_probe_zz.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:54.440Z

**tool call — Bash**
````
{
 "command": "S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head\"; R=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1; mkdir -p \"$R/mutA/app\" \"$R/mutB/app\" && cp -R \"$S/tests\" \"$R/mutA/\" && cp -R \"$S/app/frontend\" \"$R/mutA/app/\" && cp -R \"$S/tests\" \"$R/mutB/\" && cp -R \"$S/app/frontend\" \"$R/mutB/app/\" && echo copied && ls \"$R\"",
 "description": "Create mutation copies under the review-evidence directory"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:54.950Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/mutB/tests/e2e/test_probe_zz.py",
 "content": "def test_probe(page):\n    # 'btn-copy' is not declared in the contract; it is only a substring of btn-copy-letter / btn-copy-anyway\n    page.get_by_test_id(\"btn-copy\").click()\n"
}
````

### User / tool · 2026-11-02T11:07:55.305Z

**tool result**
````
copied
mutA
mutB
````

### User / tool · 2026-11-02T11:07:55.414Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/mutB/tests/e2e/test_probe_zz.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:56.706Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/mutA/app/frontend/export.js",
 "offset": 36,
 "limit": 3
}
````

### User / tool · 2026-11-02T11:07:56.717Z

**tool result**
````
36	    const close = () => { box.hidden = true; if (main) { main.classList.add("btn--primary"); main.focus(); } };
37	    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
38	      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:07:57.948Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1; cd \"$R/mutB\" && echo \"=== B: spec uses undeclared 'btn-copy' (substring of declared ids) ===\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -3; echo \"--- is 'btn-copy' a literal declared id in the contract? ---\"; grep -c '`btn-copy`\\|, btn-copy,\\|btn-copy ' tests/e2e/conftest.py; grep -n -o -E \".{0,12}btn-copy.{0,14}\" tests/e2e/conftest.py | head -5",
 "description": "Run contract test on mutation B and check the probe id is undeclared"
}
````

### User / tool · 2026-11-02T11:07:58.290Z

**tool result**
````
=== B: spec uses undeclared 'btn-copy' (substring of declared ids) ===
...                                                                      [100%]
3 passed in 0.02s
--- is 'btn-copy' a literal declared id in the contract? ---
0
8:port-notes, btn-copy-letter, count
41:ort.js) and btn-copy-anyway ('Copy
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:00.054Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/mutA/app/frontend/export.js",
 "old_string": "\"data-testid\": \"copy-confirm\", role: \"alert\"",
 "new_string": "\"data-testid\": \"copy-confirm-gone\", role: \"alert\""
}
````

### User / tool · 2026-11-02T11:08:00.156Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/mutA/app/frontend/export.js has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:00.797Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1; cd \"$R/mutA\" && echo \"=== A: frontend no longer renders copy-confirm ===\" && grep -c '\"data-testid\": \"copy-confirm\"' app/frontend/export.js; grep -c 'copy-confirm-gone' app/frontend/export.js; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -3",
 "description": "Run contract test on mutation A where the frontend stops rendering copy-confirm"
}
````

### User / tool · 2026-11-02T11:08:01.146Z

**tool result**
````
=== A: frontend no longer renders copy-confirm ===
0
1
...                                                                      [100%]
3 passed in 0.02s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:04.271Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/test_polish_r3.py | sed -n 270,300p",
 "description": "Read the conditional copy-anyway branch in test_polish_r3 at HEAD"
}
````

### User / tool · 2026-11-02T11:08:04.365Z

**tool result**
````
    target.check()
    box.get_by_test_id("btn-confirm-date").first.click()
    note = page.get_by_test_id("gap-change-note")
    expect(note).to_be_visible(timeout=10000)
    expect(note).to_contain_text(re.compile(r"Gap recalculated"))
    assert not BAD_TEXT.search(note.inner_text())


# ---- 8. export view
def test_export_letter_box_fits_its_text_and_can_be_downloaded(page, sample_case):
    tok = sample_case
    ids = [e["id"] for e in api("GET", f"/api/cases/{tok}")[1]["entries"] if e["state"] == "verified" and e["date"]]
    api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})
    open_case(page, tok); page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-letter"); expect(box).to_be_visible()
    assert page.evaluate("(() => { const e = document.querySelector('[data-testid=export-letter]'); return e.scrollHeight <= e.clientHeight + 1; })()")
    assert page.get_by_test_id("btn-download-letter").count() == 1 and page.get_by_test_id("btn-download-notes").count() == 1
    if page.get_by_test_id("btn-download-letter").is_enabled():
        with page.expect_download() as dl:
            page.get_by_test_id("btn-download-letter").click()
            if page.get_by_test_id("copy-confirm").count():
                page.get_by_test_id("btn-copy-anyway").click()
        assert dl.value.suggested_filename.endswith(".txt")
        text = open(dl.value.path(), encoding="utf-8").read()
        assert text.startswith("TREATMENT CHRONOLOGY")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:18.927Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/exact_token_check.py",
 "content": "\"\"\"Reviewer check for T-124 (staff-engineer): does test_every_test_id_is_declared pass only by substring?\n\nSame id extraction as tests/unit/test_e2e_contract.py, run against a given tree (argv[1]).\nFor each id used by a spec, report whether it is declared as a whole token in the contract docstring\n(exact match, hyphen-aware word boundaries) or only as a substring of another declared id.\n\"\"\"\nimport pathlib\nimport re\nimport sys\n\nroot = pathlib.Path(sys.argv[1])\ne2e = root / \"tests\" / \"e2e\"\ncontract = (e2e / \"conftest.py\").read_text().split('\"\"\"')[1]\n\nused = {}\nfor p in sorted(e2e.glob(\"test_*.py\")):\n    for m in re.finditer(r'get_by_test_id\\(f?\"([^\"]+)\"\\)', p.read_text()):\n        u = re.sub(r\"entry-\\d+$\", \"entry-<seq>\", re.sub(r\"\\{[^}]*\\}\", \"<seq>\", m.group(1)))\n        used.setdefault(u, set()).add(p.name)\n\nsubstring_only = []\nfor u in sorted(used):\n    substr_ok = (u in contract) or (u.startswith(\"amount-\") and \"amount-<raw>\" in contract)\n    token = re.compile(r\"(?<![\\w-])\" + re.escape(u) + r\"(?![\\w-])\")\n    exact_ok = bool(token.search(contract)) or (u.startswith(\"amount-\") and \"amount-<raw>\" in contract)\n    if substr_ok and not exact_ok:\n        substring_only.append((u, sorted(used[u])))\n\nprint(\"ids used by specs:\", len(used))\nprint(\"ids that pass the contract test ONLY as a substring of another declared id:\")\nfor u, files in substring_only:\n    print(\"  \", u, files)\nprint(\"count:\", len(substring_only))\n"
}
````

### User / tool · 2026-11-02T11:08:19.046Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/exact_token_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:21.583Z

**tool call — Bash**
````
{
 "command": "S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/exact_token_check.py \"$S\"",
 "description": "Run exact-token check of spec ids against HEAD contract"
}
````

### User / tool · 2026-11-02T11:08:21.714Z

**tool result**
````
ids used by specs: 162
ids that pass the contract test ONLY as a substring of another declared id:
count: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:34.274Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep -E \"T-124|T-119|T-060\" ; echo \"---\"; f=$(ls reviews/T-119-staff-engineer*.md 2>/dev/null | head -1); echo \"sample=$f\"; [ -n \"$f\" ] && sed -n 1,12p \"$f\"; echo \"--- HEAD still pinned? ---\"; git rev-parse HEAD; echo \"--- live app health (GET only) ---\"; curl -s -m 3 http://localhost:7860/api/health; echo",
 "description": "Check existing review files, HEAD pin, and app health"
}
````

### User / tool · 2026-11-02T11:08:34.437Z

**tool result**
````
T-060-accessibility-pass1.md
T-060-accessibility-pass2.md
T-060-accessibility-pass3.md
T-060-paralegal-pass1.md
T-060-paralegal-pass2.md
T-060-ux-designer-pass1.md
T-060-ux-designer-pass2.md
T-060-ux-designer-pass3.md
T-119-staff-engineer.md
---
sample=reviews/T-119-staff-engineer.md
# T-119 review: staff-engineer-reviewer (round 1)

**Verdict: changes.** No blocker. Two majors: the WCAG 2.1.4 row-only key rule that the card's rewritten tests were built around has no negative test (two scratch mutants survive the keyboard files), and no e2e test reaches a row by Tab, so the spec's keyboard-only E2E (R-RV-4) is still unproven.

## What I ran

- Pinned the review to `git archive 288affc` (HEAD at review time; 288affc touches only `evals/` and one unit test, no `app/` or `tests/e2e/`). Card commit is 6e880e6. Working tree was dirty and was not used.
- Own fixture server on 127.0.0.1:7972, env `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch>/zlayt.sqlite`, pytest with the same env. Full `tests/e2e`: **172 passed, 1 skipped, 1 xfailed** in 229.47s. Server stopped by PID; port closed.
- Changed files re-run twice on a second server (127.0.0.1:7973): `test_side_by_side.py test_stepper.py test_suggestions.py` gave 50 passed, 1 xfailed both times. Judge-panel tests from `test_stepper.py` repeated 5 times: 3 passed each run.
- `tests/unit/test_e2e_contract.py`: 3 passed.
- Probe (scratch copy only, saved to `artifacts/review-evidence/T-119/probe_t119_keys.py`): Tab from page load reaches an item row after 20 presses, and `a` then accepts. Pressing `a`, `d`, `j`, `p` from the body changes nothing.
- Mutants (scratch copies, product code untouched):
--- HEAD still pinned? ---
d56328a2f6d37d0a09c4a9e14c66e726a417eb82
--- live app health (GET only) ---
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:54.473Z

**tool call — Bash**
````
{
 "command": "git grep -n -E \"if pat not in c|assert not missing\" HEAD -- tests/unit/test_e2e_contract.py; git grep -n -E \"data-testid\\\": \\\"sort\\\"|\\\"data-testid\\\": \\\"copy-confirm\\\"|\\\"data-testid\\\": \\\"btn-copy-anyway\\\"|focus\\(\\); *$|b\\.focus\\(\\)\" HEAD -- app/frontend/timeline.js app/frontend/export.js | cut -c1-120; git grep -n -c \"\" HEAD -- tests/e2e/conftest.py >/dev/null && git show HEAD:tests/e2e/conftest.py | grep -n -E \"^T-060 r3 / T-124|btn-copy-anyway\" | cut -c1-80; git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py | wc -l; git show d56328a --numstat",
 "description": "Confirm exact line numbers and card diff numstat"
}
````

### User / tool · 2026-11-02T11:08:54.675Z

**tool result**
````
HEAD:tests/unit/test_e2e_contract.py:22:        if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
HEAD:tests/unit/test_e2e_contract.py:24:    assert not missing, missing
HEAD:app/frontend/export.js:37:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "a
HEAD:app/frontend/export.js:38:      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary
HEAD:app/frontend/export.js:40:    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
HEAD:app/frontend/timeline.js:257:          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.targ
40:T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the 
41:  copy-confirm (role=alert box shown when Copy letter is pressed while items 
       9
commit d56328a2f6d37d0a09c4a9e14c66e726a417eb82
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:06:22 2026 -0600

    test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
    
    Used by test_polish_r3 and rendered by the frontend; they were never added to the conftest contract. No ids dropped or renamed.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

2	0	tests/e2e/conftest.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:08:57.259Z

**tool call — Bash**
````
{
 "command": "git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py; echo \"--- status of those paths ---\"; git status --short -- app/frontend tests/e2e tests/unit/test_e2e_contract.py",
 "description": "Check working-tree differences in frontend and e2e paths vs HEAD"
}
````

### User / tool · 2026-11-02T11:08:57.377Z

**tool result**
````
 app/frontend/app.js      |  4 ++--
 app/frontend/dom.js      | 12 +++++++++++
 app/frontend/flags.js    |  8 +++++++
 app/frontend/review.css  |  6 ++++++
 app/frontend/review.js   | 42 +++++++++++++++++++++++++++++++-----
 app/frontend/styles.css  |  9 +++++---
 app/frontend/switcher.js |  6 ++----
 app/frontend/timeline.js | 55 ++++++++++++++++++++++++++++++++++++++++++++----
 8 files changed, 124 insertions(+), 18 deletions(-)
--- status of those paths ---
 M app/frontend/app.js
 M app/frontend/dom.js
 M app/frontend/flags.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/styles.css
 M app/frontend/switcher.js
 M app/frontend/timeline.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:01.060Z

**tool call — Bash**
````
{
 "command": "echo \"working tree:\"; grep -n -E \"\\\"data-testid\\\": \\\"sort\\\"|\\\"data-testid\\\": \\\"copy-confirm\\\"|\\\"data-testid\\\": \\\"btn-copy-anyway\\\"\" app/frontend/*.js | cut -c1-110; echo \"HEAD:\"; git grep -n -E \"\\\"data-testid\\\": \\\"(sort|copy-confirm|btn-copy-anyway)\\\"\" HEAD -- app/frontend | cut -c1-110",
 "description": "Compare the three frontend ids in working tree versus HEAD"
}
````

### User / tool · 2026-11-02T11:09:01.187Z

**tool result**
````
working tree:
app/frontend/export.js:37:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", rol
app/frontend/export.js:38:      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--pr
app/frontend/timeline.js:303:          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev
HEAD:
HEAD:app/frontend/export.js:37:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm"
HEAD:app/frontend/export.js:38:      el("div", { class: "row" }, el("button", { type: "button", class: "btn bt
HEAD:app/frontend/timeline.js:257:          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:23.701Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-124-staff-engineer.md",
 "content": "# T-124 review: staff-engineer-reviewer (round 1)\n\n**Verdict: pass.** No blocker, no major. The three ids are declared, rendered and used, and the contract test is green on the pinned HEAD. Two minors on the contract test itself (one-directional check, substring match); neither affects T-124's three ids.\n\n## What I ran\n\n- Pinned to `git archive d56328a` (HEAD `d56328a2f6d37d0a09c4a9e14c66e726a417eb82` at review time). Extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head`.\n- `pytest tests/unit/test_e2e_contract.py -v -p no:cacheprovider` on that archive: **3 passed**.\n- Frontend render, at HEAD (`git grep`) and in the archive: `app/frontend/timeline.js:257` (`sort`, select in the Timeline toolbar); `app/frontend/export.js:37` (`copy-confirm`, role=alert); `app/frontend/export.js:38` (`btn-copy-anyway`); `export.js:40` (focus moves to it when the confirm opens).\n- Spec use, at HEAD: `tests/e2e/test_polish_r3.py:99` (`sort`), `:140` and `:290` (`copy-confirm`), `:141` and `:291` (`btn-copy-anyway`).\n- Parent `db7f6d0` archive, same test: **1 failed, 2 passed**; failure `AssertionError: ['copy-confirm', 'sort', 'btn-copy-anyway']`. The card's two added lines are what turn it green.\n- Card diff: `git show d56328a --numstat` gives `2 0 tests/e2e/conftest.py` (2 insertions, 0 deletions, no id renamed or dropped).\n- Mutation A (`artifacts/review-evidence/T-124-r1/mutA`): `export.js:37` renamed `copy-confirm` to `copy-confirm-gone`. Contract test: **3 passed**. The check never looks at the frontend.\n- Mutation B (`artifacts/review-evidence/T-124-r1/mutB`): added `tests/e2e/test_probe_zz.py:3` with `get_by_test_id(\"btn-copy\")`, an id not declared anywhere. Contract test: **3 passed** (`btn-copy` is a substring of the declared `btn-copy-letter`, `conftest.py:8`).\n- `artifacts/review-evidence/T-124-r1/exact_token_check.py` on the HEAD archive: 162 spec ids, **0** that pass only as a substring of a declared id. The B hole is latent today.\n- Working tree: `git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py` shows 8 modified frontend files (uncommitted, not part of this card). The three ids are still present in the working tree (`timeline.js:303`, `export.js:37-40`), but I reviewed HEAD only.\n- Read-only: `curl http://localhost:7860/api/health` (fixture backend, live tree).\n\n**Not run:** `tests/e2e/test_polish_r3.py` itself. It needs a fixture server on a pinned tree; the live server on 7860 serves the dirty working tree, and the brief asked for the three checks above only. Use of the ids is established by grep, not by a run.\n\n## Findings\n\n1. **minor, contract check is one-directional.** The contract test only asserts spec → contract. A declared id that the frontend stops rendering still passes (Mutation A). The T-124 drift came from the same gap in the other direction. The docstring's \"all already rendered by the frontend\" is true at HEAD but unenforced. Fix: add a unit test that every id named in the contract's test-id lists appears as a `data-testid` literal in `app/frontend`. Acceptance: Mutation A fails it; HEAD passes it.\n2. **minor, the id check matches substrings.** `tests/unit/test_e2e_contract.py:22` uses `if pat not in c`. An undeclared id that is a substring of a declared one passes (Mutation B). Latent: no current spec relies on it (exact-token scan: 0 of 162). Fix: match whole tokens, e.g. `re.search(r\"(?<![\\w-])\" + re.escape(pat) + r\"(?![\\w-])\", c)`. Acceptance: Mutation B fails with `['btn-copy']`; HEAD still passes with 162 ids.\n\nNo blocker: no money, LLM, fallback, or network path is touched by this diff.\n\n## Scores\n\n| criterion | score |\n|---|---|\n| frontend renders each declared id | 5 |\n| specs use each declared id | 5 |\n| contract test green on pinned HEAD | 5 |\n| contract test fails when an id is removed | 4 |\n| contract test enforcement strength (both directions, whole tokens) | 3 |\n\n## What's right\n\n- All three ids are rendered at HEAD with the behaviour the contract text describes (`timeline.js:257`, `export.js:37-40`).\n- The change is two docstring lines, no renames or drops. Parent `db7f6d0` fails with exactly these three ids and HEAD passes 3/3.\n- The contract entry names the file and behaviour of each id, so the next reader can find the hook without grepping.\n\n```json\n{\"card\": \"T-124\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit d56328a (tests/e2e/conftest.py, +2 lines); pinned to git archive d56328a (HEAD d56328a2f6d37d0a09c4a9e14c66e726a417eb82); live app http://localhost:7860 read-only (/api/health) only; sample case not run\",\n \"exercised\": [\n   \"read personas/staff-engineer.md, board show T-124, git show d56328a --numstat and diff\",\n   \"git archive d56328a -> scratchpad T-124-r1-head; pytest tests/unit/test_e2e_contract.py -v -p no:cacheprovider: 3 passed\",\n   \"git grep HEAD app/frontend for sort, copy-confirm, btn-copy-anyway: timeline.js:257, export.js:37, :38, :40\",\n   \"grep HEAD tests/e2e/test_polish_r3.py for the three ids: lines 99, 140, 141, 290, 291\",\n   \"git archive db7f6d0 (parent) contract test: 1 failed, missing ['copy-confirm','sort','btn-copy-anyway']\",\n   \"Mutation A artifacts/review-evidence/T-124-r1/mutA: export.js:37 id renamed; contract test 3 passed\",\n   \"Mutation B artifacts/review-evidence/T-124-r1/mutB: spec uses undeclared btn-copy; contract test 3 passed\",\n   \"artifacts/review-evidence/T-124-r1/exact_token_check.py on HEAD archive: 162 ids, 0 substring-only\",\n   \"git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py: working tree dirty (8 frontend files), HEAD reviewed\",\n   \"curl GET http://localhost:7860/api/health: ok, backend fixture\",\n   \"NOT run: tests/e2e/test_polish_r3.py (needs a fixture server on the pinned tree)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"frontend_renders_declared_ids\": 5, \"specs_use_declared_ids\": 5, \"contract_test_green_on_pinned_head\": 5, \"contract_test_fails_when_id_removed\": 4, \"contract_enforcement_strength\": 3},\n \"findings\": [\n   {\"severity\": \"minor\", \"title\": \"Contract check is one-directional: a declared id the frontend stops rendering still passes\",\n    \"evidence\": \"artifacts/review-evidence/T-124-r1/mutA/app/frontend/export.js:37 renamed data-testid copy-confirm -> copy-confirm-gone; cd artifacts/review-evidence/T-124-r1/mutA && .venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider -> 3 passed\",\n    \"why_it_matters\": \"The conftest says every declared id is rendered; nothing checks it. T-124 was the same gap seen from the other side (spec ids missing from the contract).\",\n    \"fix\": \"Add a unit test that every id listed in the tests/e2e/conftest.py contract appears as a data-testid literal in app/frontend (object-literal or attribute form).\",\n    \"acceptance_test\": \"Mutation A fails the new test naming copy-confirm; HEAD d56328a passes it.\"},\n   {\"severity\": \"minor\", \"title\": \"Id check matches substrings: an undeclared id inside a declared one passes\",\n    \"evidence\": \"tests/unit/test_e2e_contract.py:22 `if pat not in c`; artifacts/review-evidence/T-124-r1/mutB/tests/e2e/test_probe_zz.py:3 get_by_test_id(\\\"btn-copy\\\"); tests/e2e/conftest.py:8 declares btn-copy-letter; contract test 3 passed. Latent: artifacts/review-evidence/T-124-r1/exact_token_check.py finds 0 of 162 HEAD ids relying on a substring.\",\n    \"why_it_matters\": \"R-ST-1 is the only enforcement that spec hooks are named in the contract; a substring match lets a typo or a truncated id through.\",\n    \"fix\": \"Match whole tokens: re.search(r\\\"(?<![\\\\w-])\\\" + re.escape(pat) + r\\\"(?![\\\\w-])\\\", c) in test_every_test_id_is_declared.\",\n    \"acceptance_test\": \"Mutation B fails with ['btn-copy']; HEAD d56328a still passes with all 162 ids.\"}\n ],\n \"whats_right\": [\n   \"All three ids are rendered at HEAD with the behaviour the contract describes (timeline.js:257; export.js:37-40).\",\n   \"The change is two docstring lines with no renames or drops; parent db7f6d0 fails with exactly these three ids and HEAD passes 3/3.\",\n   \"The contract entry names each id's file and behaviour, so the hook is findable without grep.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:09:23.857Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-124-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:27.269Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-124-staff-engineer.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\`\\`\\`', t, re.S)\nassert len(blocks)==1, len(blocks)\nj=json.loads(blocks[0])\nsev=[f['severity'] for f in j['findings']]\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('card',j['card'],'persona',j['persona'],'model',j['model'],'verdict',j['verdict'],'expected',exp,'OK' if exp==j['verdict'] else 'MISMATCH')\nprint('findings',sev)\n\" && python3 tools/board.py show T-124 | sed -n 1,3p",
 "description": "Parse the review JSON and check the verdict rule"
}
````

### User / tool · 2026-11-02T11:09:27.331Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:29.685Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/check_review_json.py",
 "content": "\"\"\"Parse reviews/T-124-staff-engineer.md: one json block, and the verdict follows the D.2 rule.\"\"\"\nimport json\nimport pathlib\nimport re\n\ntext = pathlib.Path(\"/Users/arsis/zlayt-pm-project/reviews/T-124-staff-engineer.md\").read_text()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\" + fence, text, re.S)\nassert len(blocks) == 1, len(blocks)\nj = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in j[\"findings\"]]\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", j[\"card\"], \"persona\", j[\"persona\"], \"model\", j[\"model\"])\nprint(\"verdict\", j[\"verdict\"], \"expected\", expected, \"OK\" if expected == j[\"verdict\"] else \"MISMATCH\")\nprint(\"findings\", sev)\n"
}
````

### User / tool · 2026-11-02T11:09:29.785Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/check_review_json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:31.220Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-124-r1/check_review_json.py && cd /Users/arsis/zlayt-pm-project && python3 tools/board.py show T-124 | sed -n 1,4p",
 "description": "Run the review JSON check and read card status"
}
````

### User / tool · 2026-11-02T11:09:31.389Z

**tool result**
````
card T-124 persona staff-engineer-reviewer model claude-haiku-5-5
verdict pass expected pass OK
findings ['minor', 'minor']
---
id: "T-124"
title: "test_e2e_contract fails: missing test ids after T-060 r3"
milestone: "M3"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:34.660Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md"
}
````

### User / tool · 2026-11-02T11:09:34.667Z

**tool result**
````
1	---
2	name: e2e-contract-review-patterns
3	description: T-039 round 1-2 (tests-first unit + E2E specs) patterns - contract docstring vs spec hooks, vacuous negatives, optional hooks, judge-path mutation, stub-server E2E method
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns from the T-039 review (tests/unit/test_review_rules.py, tests/e2e/*, conftest contract docstring; reviews/T-039-staff-engineer.md and -r2.md).
9	
10	- **Check the path a test actually reaches before calling a mutation "uncaught".** The first judge mutation (review.py except-branch) passed the suite, but the existing test never reaches that branch: judges.py:33 converts LLMFailed to "unavailable" first. A mutation on the reached path (judges.py to_ladder) was caught. Map which layer raises before mutating.
11	- **Stub-server E2E run without the app.** Serve /api/health, /api/cases, /run, /status, GET case, /review, /export in-process on a free port and point E2E_BASE_URL at it. Modes: control (golden letter), review-409, empty letter. Script: artifacts/review-evidence/T-039-r2-letter-stub.py. Useful for any E2E spec with a fixture-only dependency.
12	- **A contract docstring can be complete while enforcement stays needle-presence.** tests/unit/test_e2e_contract.py checks fixed substrings for roles/keys/tabindex; it does not parse keyboard.press() or get_by_role(). Re-check any "declared" claim by extracting hooks from the specs, not by grep of needles.
13	- **Optional hooks make proofs conditional.** `if page.evaluate("typeof window.__debugInjectRecordHtml === 'function'")` (test_source_record.py) means the textContent proof runs only when the frontend opts in. Require the hook in the contract.
14	- **Broad except in a health probe hides broken servers as skips.** tests/e2e/conftest.py `_up()` catches Exception; an HTTP 500 on /api/health becomes 57 green skips.
15	- **Red evidence goes stale.** T-039 r1 saw 39 failed / NotImplementedError; r2 saw 23 passed after the T-037 pipeline commit (d67a82d) landed. Re-run before quoting a red state; quote the run with its date and HEAD.
16	- **Default-argument footgun in fakes.** which_record(user, case="sample") returns [] silently for other cases; the r1 IndexError came from exactly this.
17	
18	**Why:** these produced the T-039 r1 majors (contract incomplete, record_nos/IndexError, vacuous letter) and the r2 major (judge except-branch unguarded).
19	**How to apply:** on any E2E or tests-first card, extract hooks from specs, run a stub-server mode with a 409 and an empty output, mutate the path the test reaches, and grep for optional-hook `if` guards.
20	
21	Environment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard "could not parse command safely" on long for-loops with quotes and em-dashes; put the check in a file under artifacts/review-evidence and run it. Use `-p no:cacheprovider` for pytest runs from the reviewer. `timeout` is not on this macOS shell; use the tool timeout parameter.
22	
23	Related: [[project_db_review_patterns]], [[project_design_review_patterns]], [[project_harness_review_patterns]].
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:39.596Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md",
 "old_string": "**Why:** these produced the T-039 r1 majors (contract incomplete, record_nos/IndexError, vacuous letter) and the r2 major (judge except-branch unguarded).\n**How to apply:** on any E2E or tests-first card, extract hooks from specs, run a stub-server mode with a 409 and an empty output, mutate the path the test reaches, and grep for optional-hook `if` guards.\n\nEnvironment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard \"could not parse command safely\" on long for-loops with quotes and em-dashes; put the check in a file under artifacts/review-evidence and run it. Use `-p no:cacheprovider` for pytest runs from the reviewer. `timeout` is not on this macOS shell; use the tool timeout parameter.",
 "new_string": "- **T-124 (d56328a, r1 pass): the contract test is one-directional and substring-based.** It checks spec ids -> contract text only (`if pat not in c`, test_e2e_contract.py:22). Mutants: a declared id the frontend stopped rendering still passes; an undeclared `btn-copy` (substring of declared `btn-copy-letter`) passes. Latent: 0 of 162 HEAD spec ids relied on a substring. Verify the card's claim \"rendered by the frontend\" with git grep on the pinned HEAD, not the working tree.\n- **Working tree is not HEAD.** At T-124 review the frontend had 8 uncommitted files; `timeline.js` moved `sort` from line 257 (HEAD) to 303 (tree). Cite HEAD line numbers and say so.\n\n**Why:** these produced the T-039 r1 majors (contract incomplete, record_nos/IndexError, vacuous letter) and the r2 major (judge except-branch unguarded). T-124 added the one-directional and substring gaps.\n**How to apply:** on any E2E or tests-first card, extract hooks from specs, run a stub-server mode with a 409 and an empty output, mutate the path the test reaches, grep for optional-hook `if` guards, and mutate both directions (drop a declared id from the frontend; add an undeclared substring id to a spec).\n\nEnvironment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard \"could not parse command safely\" on long for-loops with quotes and em-dashes, and on python -c one-liners with escaped backticks or `\\\"`; put the check in a file under artifacts/review-evidence and run it. The reviewer Write guard refuses the shell scratchpad; mutation copies go under artifacts/review-evidence/<card>-r<n>/ (cp -R from the scratchpad archive works). Use `-p no:cacheprovider` for pytest runs from the reviewer. `timeout` is not on this macOS shell; use the tool timeout parameter."
}
````

### User / tool · 2026-11-02T11:09:39.717Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:40.786Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T11:09:40.795Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1-r2 (fail) and r4 3223e50 (changes): H3V5 label contradicts judge rule 1, reachability mutants red, relabel second-agent test
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263, r2 8bc7f90, r3 db08276 (all fail): bare figures vanish in prose/CMS/balance-forward, second balance-forward overwrites, counter blind to bare numbers, mutant label checks
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4 6bca71e (fail): repeated statement totals overwritten while counted as placed, skipped billing records leave complete true, stray bare-number definition gap
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untested); T-099 r2 f345bc8 pass: case_count clause untested, F2 debt needs SCOPE_CUTS row
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — r5 690a0e3 fail: ledger+CMS totals share a [-1] slot, bare charge beyond TOL=8 dropped, complete ignores reconciliation checks
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — r1 4c5f9bf changes; r2 fdc2506 pass: guard tested for golden only, recheck test passes via backstop, latest.json blocks run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — dd84122 fail: summary-only edit bypasses accept guard, gate recomputes 2 of 5 checks, notes print AI wording
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — r1 fail; r2b fail; r3 changes; r4 8a2b934 changes: UB-04 room total vs other_figures, offset comparisons open on Q1, redundant holder branches
35	- [Exact count vs presence](feedback_exact_count_vs_presence.md) — presence oracles miss a dropped second copy; run the test module's random generator with exact per-record counts
36	- [T-100 r2 patterns](project_t100_r2_patterns.md) — r2 288c1d3 changes: shared new_tokens, vocabulary narrower than _EN_* lists, fixture eval diff method, Spanish branches unpinned
37	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — 1335f21 pass: choke point verified by grep+probe; unchecked removed narrative text still printed; 4 unrelated unit failures
38	- [T-106 patterns](project_t106_review_patterns.md) — c2a5d1f changes: pdf_hidden regex bypass via from-subprocess-import, notes-only fix leaves narrative panel printing, loose fixture filter
39	- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — r1 d3e127c changes; r2 a271014 pass: masked route checks, sentences_reason unrendered, store.py broad except, clone for .git count
40	- [Shared scratchpad](feedback_shared_scratchpad.md) — scratchpad is shared with other agents: unique card-round subdirs, diff -rq archive checks, no backgrounded setup chains
41	- [T-109 doc-vs-code patterns](project_t109_doc_vs_code_patterns.md) — r1 bf0c748 changes; r2 4bdf366 fail: model conflicts silently dropped in run_flag_pass (tray claim unreachable), balance-due wording, uncommitted eval cites, stale cut text, HEAD moved
42	- [T-106 r2 audit patterns](project_t106_r2_audit_patterns.md) — r2 e3a62fa changes: AST audit misses os alias/ctypes/asyncio, ps argv tail unpinned, rest-of-app still regex
43	- [T-102 stale-calibration patterns](project_t102_stale_calibration_patterns.md) — r1 276991b fail; r2 03206ca changes: stale fix verified via clone (archive can't discriminate), T-096 owner still missing, wrong-dir guard is a literal pin
44	- [T-115 e2e/curated patterns](project_t115_e2e_curated_patterns.md) — r1 400a8c0 changes: evidence cites older commit than HEAD, regen re-keys prompts with scripted answers, ZLAYT_DB skips, inner_text race
45	- [T-112 trim patterns](project_t112_trim_patterns.md) — r1 afcde06, r2 1b93582 changes: stems then abbreviations over-trim, doc/D-054 on old rule, unpinned counter
46	- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes: focus() replaces key route, no WCAG 2.1.4 negative test (mutants survive), no Tab E2E, stale conftest copy
47	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:42.530Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E",
 "new_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E; T-124 d56328a pass: one-way and substring id check"
}
````

### User / tool · 2026-11-02T11:09:42.667Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:09:44.142Z

Verdict: pass, no blockers or majors. The three ids are rendered and used, and `test_e2e_contract` passes 3/3 on `git archive` of HEAD d56328a; there are two minors on the contract test itself. Review written to `/Users/arsis/zlayt-pm-project/reviews/T-124-staff-engineer.md`.
