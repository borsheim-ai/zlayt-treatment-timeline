# T-097 ux-designer-reviewer, round 3: refused Accept, case verdict, the three minors, and the r2 blocker on the real backend

Verdict: **changes** (0 blockers, 1 major, 2 minors, 2 nits). Scope: card commit 9f2811f, own server on :7941 (fixture backend, curated set, scratch ZLAYT_DB), stopped by PID 30824, port returns 000.

## What the brief asked, and the answer

1. **Refused accept (422 CODE_CHECK_FAILED) shows inline with "Edit the summary": pass.** Click, the `a` key, and the refused batch with a per-item list all show it at 1440 and 390. The click box sits 62 px (1440) and 118 px (390) under the Accept button. The `a` key keeps focus on the refused row. The batch says "Nothing was accepted." and lists each item with "Edit the summary". Accepted count stays 0 after each refusal (`T-097-ux-designer-r3-walk-results.json` S_REFUSE_*). The 390 key path has a position problem, see F3.
2. **"N summaries fail a check" verbatim in the rail and the panel: pass.** Two accepted AI drafts that fail: rail `case-verdict` "2 summaries fail a check", panel `judge-case-verdict` the same words, panel counts "2 summaries fail a check, blocks export: 2", gate "Export blocked by 2", export 422 with two blockers (S_TWO_1440 / S_TWO_390; API results `two_fail_case`).
3. **The three minors: fixed.** m-1: the panel names each class once ("1 not checked, blocks export: 1, 1 edited by you, not AI-checked, 1 summary fails a check, blocks export: 1"; the two blocking clauses equal the gate's 2). m-2: at three items the rail and panel labels say "for these 3", one press makes one POST and the status says it answered for all 3; no gate row carries a rerun button (`T-097-ux-designer-r3-walk2-results.json` N3_*). m-new-1: the Not-needed judge step on the edited, passing item has no "said:" line and no fail status (S_MINORS_1440.why_e3_judge_step_text). n-1 (Export in view after refusal) and n-new-3 ("Edited by you, not AI-checked") also read fixed.
4. **Panel, Why dialog and gate never disagree: partly.** Counts agree in every measured state: S_TWO 2/2/2, S_B1 1/1/1, S_MINORS 2/2/2. But the Why verdict label on an accepted AI draft names the wrong author (F1), and the rerun sentence and the rail disagree for about three seconds after a rerun (F2).
5. **The r2 blocker (B1) on the real backend, no stub: closed.** I wrote the edited text that drops "without" past the edit route, as r2 did. Gate: status fail, ready false, blockers [e2] with SUMMARY_DROPS_QUALIFIER. GET export: 422 export_blocked naming e2. Rail "Export blocked by 1", Why "Your wording doesn't match the quote:" with "Edit your wording", panel "1 summary fails a check, blocks export: 1", refused-export message says the wording does not match. Restoring through the real edit route returns 200 and the rail reads "Ready to export, 21 not reviewed" after reload. The gate now recomputes from the current text (dd84122, D-051).

## Findings

**F1 (major). An accepted AI draft's Why verdict says "a check on your wording fails"; its own blocker row says "This summary doesn't match the quote".** The label comes from `app/backend/trace.py:275`, which uses "your wording" for any gated code step on an accepted item, whoever wrote the text. On the 1440 and 390 runs, the Why verdict for e1 and e2 (AI drafts, accepted, then broken) reads "Needs your attention: a check on your wording fails". The blocker row for the same item in the rail reads "This summary doesn't match the quote". The step under it says "Edit the summary". Graded major and not blocker: no export or letter is affected and the step and gate copy are correct. The label misstates who wrote the text, on the decision surface the paralegal reads.

**F2 (minor). After a rerun, the status says nothing blocks the export while the rail still says "Export blocked by 3" for about three seconds.** Evidence: `T-097-ux-designer-r3-walk3-results.json` after_3s_status "...Nothing about the second check blocks the export now." with after_3s_gate "Export blocked by 3". The page logged the trace that returned pass/ready 3.2 s after the press (trace_responses_seen_by_page). After reload the rail reads "Ready to export, 20 not reviewed". The sentence comes from the rerun answer (`app/frontend/stepper.js:164`); the rail is refreshed by a second GET trace after it (`S.rejudge`, stepper.js:180-196). Caveat: this run used the E2E stub's rejudge answer (ready true). The real rejudge in a blocked state returns ready false with blockers [e2] (walk2 REJUDGE_REAL), so the sentence would not print there.

**F3 (minor). On 390, the refusal under a row focused by the `a` key can sit below the fold.** Walk 1 (row e2 under e1's refusal): the box starts at the bottom edge, `key_box_in_view` false, `artifacts/review-evidence/T-097-ux-designer-r3-390-s2-accept-key.png`. Walk 2 (row at top 262): the box at 667 to 824 is fully visible (`KEY_390` in walk2 results). Focus stays on the row either way. The click path scrolls the box into view and the key path does not.

**F4 (nit, carried from r2 n-2, still open). The 422 names the normalised figure, not what was typed.** Typed "$7,777" in an edit; the 422 says "...not in the quote: 7777. Remove it or change the quote." (`S_NUMBERS.message`, `typed_figure_in_message` false). The refused accept says "not in the quote: 5" for "Pain 5/10". The handoff lists this as not done.

**F5 (nit). The same rerun control appears three times on one screen.** In the three-item state the case rail has two buttons and the panel one, all "Run the second check again for these 3" (walk2 N3_1440.rail_rerun_buttons, panel_rerun_buttons). Same label, same POST, so nothing is misread. Optional: one per screen.

## What I exercised

- `python3 tools/board.py show T-097`: status in_review, rounds 2, commits include 9f2811f; reviews r1 and r2 fail.
- `git rev-parse --short HEAD` = 9f2811f, `git status --short | wc -l` = 1234 at start. `git merge-base --is-ancestor 9f2811f HEAD`: yes. `git archive 9f2811f | tar -x` into a scratch copy; checked the copy has tests/e2e/test_code_check_refusal.py.
- End: `git rev-parse --short HEAD` = 841be23, `git status --short | wc -l` = 1286. `git log --oneline 9f2811f..841be23` = one docs commit (D-052). `git diff --stat 9f2811f 841be23 -- app/ tests/e2e/` is empty. The move touches memory/ORCHESTRATOR_DECISIONS.md and memory/SCOPE_CUTS.md only, so the pinned result holds.
- Own server from the archive copy: `LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7941 HOST=127.0.0.1 ZLAYT_DB=<scratch>/t097r3.sqlite3 .venv/bin/python -m app.main`; cwd confirmed with lsof; `/api/health` 200; PID 30824 stopped; `curl` to :7941 returns 000.
- `E2E_BASE_URL=http://127.0.0.1:7941 ZLAYT_DB=<scratch>/t097r3.sqlite3 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -q -p no:cacheprovider -rA` from the archive copy: **9 passed in 12.38s** (click x4, key x2, batch x2, case verdict x1; real and stub variants).
- `artifacts/review-evidence/T-097-ux-designer-r3-api.py` (results `T-097-ux-designer-r3-api-results.json`): B1 on the real backend (direct write, stored reasons left as they were); the gate, the item trace, export 422, and the restore; a single accept and a batch refused with 422 CODE_CHECK_FAILED, statuses stay pending; two accepted AI drafts broken: gate, verdict and export all count 2.
- `artifacts/review-evidence/T-097-ux-designer-r3-walk.py` at 1440x900 and 390x844 (results `T-097-ux-designer-r3-walk-results.json`, 0 errors): S_REFUSE, S_TWO, S_B1 (no stub), S_MINORS (JudgeNotRun stub from tests/e2e/conftest.py for the judge-not-run state only; the failing and passing edits are real), S_NUMBERS. Screenshots `artifacts/review-evidence/T-097-ux-designer-r3-<w>-s1..s14*.png`, for example `T-097-ux-designer-r3-1440-s1-accept-click.png`, `T-097-ux-designer-r3-1440-s6-why-e1.png`, `T-097-ux-designer-r3-390-s7-export-refused.png`.
- `artifacts/review-evidence/T-097-ux-designer-r3-walk2.py` (results `T-097-ux-designer-r3-walk2-results.json`): three-item rerun (labels, one POST, 3 answered); the 390 key path with the row focused and no script scroll; REJUDGE_REAL (no stub).
- `artifacts/review-evidence/T-097-ux-designer-r3-walk3.py` (results `T-097-ux-designer-r3-walk3-results.json`): rail readings after the press, the trace responses the page logged, and a reload.
- Code read: `app/backend/trace.py:275`, `app/frontend/stepper.js:164` and `:180-196`, `app/frontend/judges.js:136`, `app/frontend/batch.js:27,66`, `app/frontend/review.js:180`, `memory/ORCHESTRATOR_DECISIONS.md:59` (D-051).

Not exercised: an end-to-end keyboard-only walk of the whole case (only the refusal path was keyboard-driven); accessibility conformance (outside my lens); the JudgeNotRun-stub export (the stub replaces the 422 body, so I read export only in the real-backend states).

## Three things that are right

- The real gate, the export and the rail/panel/Why counts agree on the B1 state and on the two-failure state; restoring through the real edit route clears the gate on reload.
- A refused accept says why, beside the button, with "Edit the summary" and the typed text kept, for click, the `a` key and the batch.
- The counts and the verdict words read the backend ("2 summaries fail a check, blocks export: 2"), and the three r2 minors are fixed.

```json
{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "card commit 9f2811f via git archive copy in scratchpad (t097r3-archive-9f2811f); HEAD moved to 841be23 during the review, diff 9f2811f..841be23 touches memory/ORCHESTRATOR_DECISIONS.md and memory/SCOPE_CUTS.md only (no app/ or tests/ change); app http://127.0.0.1:7941 own server, fixture backend, curated set, scratch ZLAYT_DB (t097r3.sqlite3), stopped by PID 30824, port 000; sample case plus synthetic cases created by the walks; the persona dossier names claude-opus-5-5 as the expected reviewer model, this run was claude-haiku-5-5 as the brief and the runtime state",
 "exercised": [
  "python3 tools/board.py show T-097 -> status in_review, rounds 2, commits include 9f2811f, reviews r1 and r2 fail",
  "git rev-parse --short HEAD -> 9f2811f (start), git status --short | wc -l -> 1234; git merge-base --is-ancestor 9f2811f HEAD -> yes; git archive 9f2811f | tar -x into the scratch copy",
  "end: git rev-parse --short HEAD -> 841be23, git status --short | wc -l -> 1286; git log --oneline 9f2811f..841be23 -> one docs commit (D-052); git diff --stat 9f2811f 841be23 -- app/ tests/e2e/ -> empty",
  "own server from the archive copy: LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7941 HOST=127.0.0.1 ZLAYT_DB=<scratch>/t097r3.sqlite3; /api/health 200; PID 30824 stopped; port 7941 returns 000",
  "E2E: pytest tests/e2e/test_code_check_refusal.py -q -rA against :7941 with ZLAYT_DB -> 9 passed in 12.38s (real and stub variants)",
  "artifacts/review-evidence/T-097-ux-designer-r3-api.py -> T-097-ux-designer-r3-api-results.json (real backend: B1 gate, export 422, restore 200; single and batch 422 CODE_CHECK_FAILED with statuses pending; two-failure gate, verdict and export count 2)",
  "artifacts/review-evidence/T-097-ux-designer-r3-walk.py at 1440x900 and 390x844 -> T-097-ux-designer-r3-walk-results.json, 0 errors: S_REFUSE (click, a key, batch list), S_TWO (rail, panel, Why, export), S_B1 (no stub), S_MINORS (JudgeNotRun for the judge-not-run state only), S_NUMBERS; 14 screenshots under artifacts/review-evidence/T-097-ux-designer-r3-*",
  "artifacts/review-evidence/T-097-ux-designer-r3-walk2.py -> T-097-ux-designer-r3-walk2-results.json: three-item rerun (labels, one POST, 3 answered); 390 key path with row focused; REJUDGE_REAL (ready false, blockers [e2])",
  "artifacts/review-evidence/T-097-ux-designer-r3-walk3.py -> T-097-ux-designer-r3-walk3-results.json: rail after the press, trace responses logged by the page, reload",
  "read app/backend/trace.py:275; app/frontend/stepper.js:164 and 180-196; app/frontend/judges.js:136; app/frontend/batch.js:27,66; app/frontend/review.js:180; memory/ORCHESTRATOR_DECISIONS.md:59 (D-051)",
  "viewed screenshots: 1440 s1 accept-click, 1440 s6 why-e1, 390 s2 accept-key, 390 s3 batch-refused, 390 s7 export-refused"],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major", "title": "Accepted AI draft's Why verdict says 'a check on your wording fails'; its own blocker row says 'This summary doesn't match the quote'",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk-results.json S_TWO_1440.why_e1_verdict = 'Needs your attention: a check on your wording fails' (same at S_TWO_390); S_TWO_1440.rail_gate_blockers e1 = \"This summary doesn't match the quote: ...\"; screenshot artifacts/review-evidence/T-097-ux-designer-r3-1440-s6-why-e1.png shows the step 'Edit the summary to remove 5'; code app/backend/trace.py:275 hard-codes 'your wording' for any gated code step on an accepted item",
   "why_it_matters": "On an AI draft the paralegal accepted, the Why header tells her she wrote the wording, while the blocker row and the step say the AI drafted it. Provenance is the decision the paralegal makes (D-045 b exempts human wording from the judge, so authorship changes what the gate asks). Panel, Why and gate should read one source. No export or letter is affected, so graded major, not blocker.",
   "fix": "In app/backend/trace.py _finish, pick the label by author: 'a check on this summary fails' when the summary is the AI draft (no edited_json), 'a check on your wording fails' only when the paralegal edited it.",
   "acceptance_test": "E2E: accept an AI draft, then break its summary (as tests/e2e/test_code_check_refusal.py does): the item's Why verdict contains 'this summary' and not 'your wording', matching the blocker row. An edited item whose check fails still says 'your wording' (S_B1_1440.why_e2_verdict stays)."},
  {"severity": "minor", "title": "After a rerun, the status says nothing blocks the export while the rail still says 'Export blocked by 3' for about three seconds",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk3-results.json after_3s_status 'The second check ran on 3 items and answered for all of them. Nothing about the second check blocks the export now.' with after_3s_gate 'Export blocked by 3'; trace_responses_seen_by_page shows the pass/ready trace 3.2 s after the press; after_reload_gate 'Ready to export, 20 not reviewed'. Sentence built at app/frontend/stepper.js:164 from the rerun answer; rail refreshed by a later GET trace in S.rejudge (stepper.js:180-196). Stub caveat: the rerun answer came from the E2E stub (ready true); the real rejudge in a blocked state returns ready false with blockers [e2] (walk2-results REJUDGE_REAL).",
   "why_it_matters": "For the seconds between the two updates, the same screen says the export is both blocked and unblocked. The brief asks the status, the Why dialog and the gate never to disagree.",
   "fix": "Print the rerun sentence after the trace refresh, or build it from the same refreshed gate the rail uses, and show the rail update in the same step.",
   "acceptance_test": "E2E on the three-item JudgeNotRun state: after a rerun, the 'Nothing about the second check blocks the export now' sentence appears only in the same render in which the rail reads 'Ready to export'; no moment with both on screen."},
  {"severity": "minor", "title": "On 390, the refusal under a row focused by the a key can sit below the fold",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk-results.json S_REFUSE_390.key_box_in_view false (row e2 under e1's refusal); screenshot artifacts/review-evidence/T-097-ux-designer-r3-390-s2-accept-key.png shows the e2 box starting at the bottom edge. In walk2-results KEY_390 with the row at top 262 the box (667 to 824) is fully visible. Focus stays on the row (key_focus_item e2) in both. The click path scrolls the box into view.",
   "why_it_matters": "Pressing a produces no visible change in the viewport in the first layout. The message is announced (role=alert), so this is minor, but the keyboard path should show its reason as the click path does.",
   "fix": "When a refusal is set, scroll the refused box into view with block nearest, as the click path does, on the key path too.",
   "acceptance_test": "E2E at 390x844: focus a row whose refusal lies below the fold, press a: the accept-refused box is fully inside the viewport."},
  {"severity": "nit", "title": "The 422 names the normalised figure, not the one typed (r2 n-2, still open)",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk-results.json S_NUMBERS: typed '$7,777' -> 422 invalid_edit 'The summary has a number, date or dollar figure that is not in the quote: 7777. Remove it or change the quote.' typed_figure_in_message false; the refused accept says 'not in the quote: 5' for 'Pain 5/10'. The r3 handoff lists it as not done.",
   "why_it_matters": "The paralegal cannot match '7777' to the '$7,777' she typed at a glance.",
   "fix": "Quote the token as typed ('$7,777').",
   "acceptance_test": "API: an edit adding '$7,777' that the quote lacks returns a message containing '$7,777'."},
  {"severity": "nit", "title": "The same rerun control appears three times on one screen",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk2-results.json N3_1440.rail_rerun_buttons (two in the case rail, the gate step and the judges step) and panel_rerun_buttons (one); all read 'Run the second check again for these 3' and one press makes one POST.",
   "why_it_matters": "Same label and same action, so nothing is misread; it is redundant on one screen.",
   "fix": "Optional: one rerun control per screen.",
   "acceptance_test": "Optional: with three JudgeNotRun items, the count of btn-rerun-judge on the case-stepper and judge-panel together is 1."}
 ],
 "whats_right": [
  "The real gate, export, rail, panel and Why agree on the reviewer's r2 state (B1) and on the two-failure state; restoring through the real edit route clears the gate on reload.",
  "A refused accept says why beside the button with 'Edit the summary' and keeps the typed text, for the click, the a key and the batch list (accepted count stays 0).",
  "The rail and panel show the backend's words '2 summaries fail a check, blocks export: 2' and the three r2 minors (m-1, m-2, m-new-1) are fixed."],
 "questions_for_chris": ["Does the spec treat an authorship label on a decision surface (Why 'your wording' on an AI draft) as a fact constraint? I graded F1 major. If you read provenance as a constraint, F1 becomes a blocker and the verdict becomes fail."]}
```
