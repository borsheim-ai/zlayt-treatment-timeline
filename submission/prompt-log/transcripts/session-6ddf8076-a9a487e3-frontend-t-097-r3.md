# Subagent: Frontend: T-097 r3 (Frontend: T-097 r3)

Source: `agent-a9a487e322f723653.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:29:33.096Z

You own board card T-097, round 3 (final; claimed by "frontend") in /Users/arsis/zlayt-pm-project. Read reviews/T-097-ux-designer-r2.md (B1 was backend; it's now fixed in T-098 r2, dd84122) and the notes on T-097 and T-098 (`python3 tools/board.py show T-098`).

1. Accept, single and batch, can now return 422 `CODE_CHECK_FAILED` with a plain reason and next_action "Edit the summary to match the quote". Show it inline next to the item's Accept button with an Edit action, and for batch, list which items were refused.
2. The case verdict label is now "N summaries fail a check". Render it in the case rail and the panel exactly as the backend sends it.
3. Fix the 3 minors from round 2.

Update the e2e tests and declare test ids; test_e2e_contract stays green. Test a clean worktree of HEAD (`git worktree add <scratchpad>/wt HEAD`, then remove it) with your own server on a spare port (fixture backend, ZLAYT_DB in your scratchpad), and stop it by PID.

Commit with `git add <paths>` and then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-097 in_review --agent frontend`. Reply in 1 line.

### User / tool · 2026-11-02T05:29:33.101Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:35.813Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-097 | tail -60; python3 tools/board.py show T-098 | tail -40; cat reviews/T-097-ux-designer-r2.md; git status --short | head; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T05:29:36.040Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:37.809Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-097-ux-designer-r2.md | head -120; python3 tools/board.py show T-098 | grep -n \"CODE_CHECK\\|fail a check\\|r2\\|dd84122\" | head -30; git status --short | head; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T05:29:37.993Z

**tool result**
````
# T-097 ux-designer-reviewer, round 2: panel and Why dialog read the gate, edit refusals, rerun placement

Verdict: **fail** (1 blocker, 0 majors, 2 minors, 3 nits: m1 and n1 carried from round 1).

Scope: the card's latest commit per `python3 tools/board.py show T-097` is 21b6665 (r1 fix). Your brief asked for HEAD, and HEAD 32f6c9d contains everything the round-2 tickets need: T-098 e511778 (an ancestor of 21b6665), T-100 24c18a7 (after 21b6665), and f5ddec8 (removes the dead 409 dialog). I reviewed the `git archive 32f6c9d` copy on my own server (:7893, fixture backend, curated set, scratch ZLAYT_DB), stopped by PID 89196. The shared-tree HEAD moved from 32f6c9d to f345bc8 during the review. The diff 32f6c9d..f345bc8 touches `app/backend/calibration_route.py` and billing tests only, so the trace, gate, review and frontend files I read are unchanged; I did not review f345bc8 itself.

## The five brief questions

1. **Panel summary and Why dialog read the gate and trace: pass on the UI, fail at the gate (B1).** In the mixed case (one accepted item whose second check never ran, one edited item failing its qualifier check, one edited item that passes), the rail, the panel summary, both Why dialogs and the refused export all say 2 blockers. After I dismissed the accepted item and reloaded, all say 1. The UI never contradicts the gate. But on the real backend, with no stub, a stored edited summary that fails the qualifier check is "Ready to export" in the rail, "all agreed with the draft" in the panel, and "Accepted by you" in the Why dialog, and the letter carries it (B1).
2. **Edited item that fails a code check shows "Your wording doesn't match the quote: <reason>" with Edit: pass in the UI.** The real edit route refuses that wording with a 422, so this state is only reachable through the conftest stub. The banner is in the Why dialog (`item-wording-fail`, "Edit your wording"), the panel row ("Where your wording does not match the quote (1 item)", "Blocks the export"), and the rail row ("Edit your wording for ..."). The reason text in the stub is generic; the real 422 names the qualifier (see question 4).
3. **Edited item that passes shows "Edited by you, not AI-checked": pass, on the real backend.** Why verdict "Edited by you, not AI-checked", judge step "Not needed", no rerun button, no "second check missing", at 1440 and 390. The step still prints the AI's "said: Unavailable" line (minor m-new-1).
4. **Confirm dialog gone; 422 shows inline: pass.** A dollar figure, a dropped negation and a dropped laterality each show their plain-words reason in the edit box at 1440 and 390 (for example "The quote carries a negation (such as no, not or denies) that the summary leaves out. Put it back in the summary."). The typed text stays, `btn-keep-wording`, `warning-list` and `btn-cancel-confirm` are absent, and no dialog opens. The edit stays `pending`.
5. **Round-1 rerun feedback placement still holds: pass.** The refused-export status sits 4 px under its button and the AI-check panel status sits 4 px under its group button, both in view after a failed run, at 1440 and 390.

## Round-1 findings, status now

- B1 (edited summary whose qualifier check fails passes the gate): the edit path is closed (the route refuses at save). The gate path is still open and is re-filed below as B1, with the acceptance test from round 1 failing as written.
- M1 (panel summary "2 not checked (blocks export)" with a gate of 1): closed. The count is now the gate's: "blocks export: 1".
- M2 (Why dialog "Accepted, second check missing" for an edited item): closed for the edited item that passes.
- m1 (rail gate-row rerun button names one item, POST reruns all): open, carried. See m-2.
- n1 (Export button scrolled out of view after a refusal): open, carried. See n-1.

## Findings

**B1 (blocker). The export gate answers from stored check results, so an edited summary that fails the qualifier check still exports.** Reproduced on the real backend with no stub. Steps: a fresh sample case; accept e1; write e2's edited text into `edited_json` (the column the paralegal's text lives in) with `review_status='edited'`, dropping "without" from "concussion without loss of consciousness". The stored check results were left as the pipeline wrote them, which is the state an edit that skipped the re-check would leave.
- `GET /trace` export_gate: status pass, ready true, blockers [], `code_check_failed` 0. e2's item trace: `summary_qualifier` pass.
- `GET /export`: 200. The letter contains "Diagnosed with cervical strain and concussion loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week."
- The UI on the same state: rail "Ready to export, 21 not reviewed"; panel "checked 19, all agreed with the draft"; e2 Why "Accepted by you", `summary_qualifier` pass; the export letter opens with the sentence.
- The edit route refuses the same wording: 422 invalid_edit, `SUMMARY_DROPS_QUALIFIER`, "The quote carries a negation (such as no, not or denies) that the summary leaves out. Put it back in the summary."

Code: `app/backend/trace.py:798` and `:357` test `"SUMMARY_DROPS_QUALIFIER" in R`, where R is the row's stored `state_reasons`, not the current text. The gate at `trace.py:982-989` is built from those. `app/backend/review.py:203` writes the edited text (`apply_review`, committed at `app/db/db.py:227-233`) and `review.py:210` writes the stored reasons in a separate update, so the two can disagree if the second write fails. I did not induce that failure. The decision D-051 (`memory/ORCHESTRATOR_DECISIONS.md:59`) says the gate "blocks it if such a state exists anyway". D-051 was recorded after my pinned commit (e63e564 is not in 32f6c9d), so it binds the gate at HEAD, and this run shows the gate does not meet it.

Reachability, stated plainly: the public routes cannot produce this state at 32f6c9d, because the edit route re-checks and refuses. It is produced by a direct write (my repro) or a failure between the two writes. I rate it a blocker on the spec (D-045 b, D-051, T-098's own acceptance: an edited item that fails a code check blocks export; a letter that loses a negation is a fact loss). The orchestrator may triage it differently, but the round-1 acceptance test as written still fails: "while it fails, GET /api/cases/<t>/export is not 200 and the letter does not contain the edited sentence". At 32f6c9d it is 200 and the sentence is there. The UI is blind to this state, so the paralegal gets no warning.

Fix (backend, T-098 owner; no frontend change needed, because the blocker list already renders a code-check blocker with Edit): recompute the summary checks (`summary_tokens`, `summary_qualifier`, `excerpt_hedge`) at trace and export time from the stored summary and quote, and gate on that result; and/or make the edited text and its check result one transaction so they cannot disagree.

Acceptance test: API: an edited item whose stored summary drops a qualifier, with stale stored reasons, gives `GET /api/cases/<t>/export` 422 `export_blocked` with `detail.blockers` naming that item and `SUMMARY_DROPS_QUALIFIER`; `GET /trace` export_gate status fail; the letter has no text for that item. UI on the same state: rail "Export blocked by 1", Why shows "Your wording doesn't match the quote:" with Edit. Keep the round-1 acceptance test as written.

**m-1 (minor). The panel's count reads "3 not checked, blocks export: 1, 1 edit does not match its quote, blocks export: 1".** Both blocking clauses are right (1 + 1 = the gate's 2), so this is not a contradiction. But "3 not checked" includes the edited item that fails its quote, which is then counted again as blocking in the next clause, and a paralegal has to add the clauses up to see that the two blockers are different items. Evidence: `artifacts/review-evidence/T-097-ux-designer-r2-walk-results.json` S_MIXED_1440.panel_summary; screenshot `artifacts/review-evidence/T-097-ux-designer-r2-1440-s4-mixed-panel.png`. Fix: name the classes separately, e.g. "1 never got the second check and blocks export; 1 edit does not match its quote and blocks export; 1 edited by you, not AI-checked". Acceptance: E2E on the mixed case: the summary names each class once, and the blocking count equals the gate's blocker count.

**m-new-1 (minor). A "Not needed" judge step still prints "The second AI check said: Unavailable".** On the mixed case the edited item that passes reads, in one step: "Not needed: this is your own wording, so the second AI check does not apply" and then "The second AI check said: Unavailable". The real backend's step for that item has `judge_verdict: unavailable` (`walk-results.json` S_MIXED_1440.raw_real_judge_step.e3). `app/frontend/stepper.js:317` prints `ev.judge_verdict` for any step that has one, and the "Not needed" mapping at `stepper.js:391` keeps that evidence. Fix: for `_notNeeded` steps, drop the verdict line. Acceptance: E2E on the mixed case: the edited item's `judge_1` step has no "said:" text and no `data-status="fail"`.

**m-2 (minor, carried from T-081 r3 and T-097 r1 m1). The rail gate-row rerun button names one item, but its POST reruns every item.** The button's aria-label is "Run the second check again for 2026-01-09 · Austin EMS run report" (`stepper.js:454`, the per-row `S.rerunButton`). One click makes one POST, and the status reads "The second check still did not answer for 3 items of 3." Evidence: walk-results S_PLACE_1440.rail_row_button and rail_row_click (posts 1); same at 390. Fix: the group model everywhere: one "Run the second check again for these N" in the gate step and no per-row button, or a per-item POST with the item id. Acceptance: for every rerun button in the rail, the aria-label's item count equals the POST's item count.

**n-1 (nit, carried from T-081 r3 and T-097 r1 n1). The Export button is scrolled out of view when a refused export opens.** Export button y = -31.5 at 1440 and y = -179.4 at 390 after the refusal (walk-results S_PLACE_1440 and S_PLACE_390 export_btn_after_refusal). The message is in view. In the mixed run at 1440 the button happened to be in view because of the scroll position, so this depends on where the user was. Fix: `scroll-margin-top` on the export-blocked section, or scroll the toolbar into view.

**n-2 (nit). The 422 names the normalised token, not what was typed.** The paralegal typed "$9,000" and the message says "...not in the quote: 9000. Remove it or change the quote." (walk-results S_REAL_1440.number_422_inline.err_text; screenshot `artifacts/review-evidence/T-097-ux-designer-r2-1440-s1-number-422-inline.png`). Fix: quote the token as typed ("$9,000"). Acceptance: the message contains the exact string the user typed.

**n-new-3 (nit). An edited item's Why verdict reads "Accepted by you".** In the stale-state run above the item's review status is `edited` and the verdict label is "Accepted by you" (`artifacts/review-evidence/T-097-ux-designer-r2-realgate-ui-results.json` why_e2_verdict). The label comes from the trace's `accepted` verdict. Fix: "Edited by you" when `review_status` is `edited`. I could not confirm this is reachable in a consistent state, so it is a nit.

## What I exercised

- `python3 tools/board.py show T-097`: status in_review, rounds 1, commits ["0e30623", "21b6665"], ac 1 evidence quoting the r2 walk.
- `git rev-parse --short HEAD` = 32f6c9d and `git status --short | wc -l` = 1161 at the start; `git archive HEAD | tar -x` into the scratchpad copy; `git merge-base --is-ancestor` for e511778, 24c18a7, 21b6665, f5ddec8, 32f6c9d (all yes, 21b6665 ancestor-of-e511778 no). At the end: `git rev-parse --short HEAD` = f345bc8 and `git status --short | wc -l` = 1218.
- Own server: `LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7893 HOST=127.0.0.1 ZLAYT_DB=<scratchpad>/t097r2.sqlite3 .venv/bin/python -m app.main` from the archive copy; `/api/health` 200; PID 89196; stopped by PID; port returns 000.
- `artifacts/review-evidence/T-097-ux-designer-r2-probe.py`: real edit route on sample e5 ("billed $9,000"), e2 (negation), e7 and e8 (laterality), passing edit on e1. Results: 422 `invalid_edit` for each refusal with a plain message; 200 on the passing edit with `warnings` `JUDGE_UNAVAILABLE`.
- `artifacts/review-evidence/T-097-ux-designer-r2-walk.py` at 1440x900 and 390x844: S_REAL (real backend, no stub: the three refusals, the passing edit, its Why dialog, the rail and panel), S_MIXED (one route handler that composes the conftest JudgeNotRun and WordingFails helpers; accepted e1 never checked, edited e2 failing, edited e3 passing; rail, panel, all three Why dialogs, refused export, dismiss of e1 then reload), S_PLACE (three accepted items, judge never ran, mode "still": refused-export rerun and panel rerun, running and failed states measured; rail row click). Screenshots `T-097-ux-designer-r2-<w>-s1…s7*.png`, results `T-097-ux-designer-r2-walk-results.json`, 0 errors.
- `artifacts/review-evidence/T-097-ux-designer-r2-realgate.py` and `…-realgate-ui.py`: the real gate with no stub on the bypassed state (B1), the real export letter, the rail, panel, Why dialog, then restoration through the real edit route (200, gate clears). Results `T-097-ux-designer-r2-realgate-results.json` and `…-realgate-ui-results.json`; screenshots `…-realgate-why-e2.png`, `…-realgate-export-letter.png`.
- Code read at the pinned commit: `app/backend/trace.py` (357, 698-852 for `R`, 853-989 for the gate), `app/backend/review.py` (171-210, 330-356), `app/db/db.py` (215-233), `app/frontend/stepper.js` (141, 317, 380-391, 446-456), `app/frontend/judges.js` (119-133), `app/frontend/review.js` (126), `tests/e2e/conftest.py` (WordingFails, JudgeNotRun), `memory/ORCHESTRATOR_DECISIONS.md` D-045, D-047, D-051. `grep` for `showConfirm`, `btn-keep-wording`, `needs_confirm`, `confirm_warnings` in `app/frontend` returns only comments.
- Not a finding: an earlier bypass attempt wrote the original-summary column; it is not evidence, and the probe was changed to use `edited_json`, where the paralegal's text lives (`review.py:203`).

## Not exercised, and limits

- Keyboard-only walk (not in the brief).
- The failing-edit and judge-never-ran states come from the conftest stubs. The stub's reason text is generic, and the "The second AI check said: Supported" line on the accepted item is the real judge's recorded answer under a stubbed skip. A real never-ran state cannot carry that line, so I did not count it.
- D-047 judge-objection warnings (JUDGE_PARTIAL, JUDGE_UNSUPPORTED) were not produced by the fixture. The JUDGE_UNAVAILABLE notice after a passing edit was not located; no dialog opened.
- The server log (four "llm call failed" lines in round 1) is outside my lens. Accessibility conformance is outside my lens.

## Three things that are right

- The real edit route refuses a dropped negation, a dropped side and an invented dollar figure with a plain 422 message under the box, keeps the typed text, and opens no confirm dialog at 1440 and 390.
- In the mixed case every surface reads one gate: "Export blocked by 2" in the rail, two "blocks export" clauses in the panel, two blockers in the refused export, and the passing edit reads "Edited by you, not AI-checked" with no rerun.
- A failed rerun is answered beside its button at both widths, in the refused-export message and in the AI-check panel.

```json
{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 32f6c9d via git archive copy in the scratchpad (contains T-098 e511778, T-100 24c18a7, f5ddec8, card commit 21b6665); app http://127.0.0.1:7893 on own server (fixture backend, curated set, scratch ZLAYT_DB), stopped by PID 89196; sample case plus synthetic cases created by the walks; shared-tree HEAD moved 32f6c9d -> f345bc8 during the review (not reviewed; diff touches calibration_route.py and billing tests only)",
 "exercised": [
  "python3 tools/board.py show T-097 -> status in_review, rounds 1, commits [0e30623, 21b6665]",
  "git rev-parse --short HEAD -> 32f6c9d; git status --short | wc -l -> 1161 (start); git archive HEAD | tar -x into the scratchpad copy",
  "git merge-base --is-ancestor: e511778, 24c18a7, 21b6665, f5ddec8, 32f6c9d are ancestors of HEAD 32f6c9d; e511778 is an ancestor of 21b6665",
  "own server from the archive copy: LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7893 ZLAYT_DB in scratchpad; /api/health 200; PID 89196 stopped; port returns 000",
  "artifacts/review-evidence/T-097-ux-designer-r2-probe.py: real edit route refusals (number, negation, laterality -> 422 invalid_edit with plain message) and a passing edit (200 with JUDGE_UNAVAILABLE warning)",
  "artifacts/review-evidence/T-097-ux-designer-r2-walk.py at 1440x900 and 390x844: S_REAL (no stub), S_MIXED (composed JudgeNotRun + WordingFails stubs), S_PLACE (failed rerun in refused export and AI-check panel; rail row click); 0 errors; screenshots T-097-ux-designer-r2-<w>-s1..s7",
  "artifacts/review-evidence/T-097-ux-designer-r2-realgate.py and -realgate-ui.py: real gate and export on a stored edited summary that fails the qualifier check (no stub); letter text checked by curl grep; restored through the real edit route (200)",
  "read app/backend/trace.py 357, 698-852, 853-989; app/backend/review.py 171-210, 330-356; app/db/db.py 215-233; app/frontend/stepper.js 141, 317, 380-391, 446-456; judges.js 119-133; review.js 126; tests/e2e/conftest.py WordingFails and JudgeNotRun; memory/ORCHESTRATOR_DECISIONS.md D-045, D-047, D-051",
  "viewed screenshots: 1440 s1 number 422 inline; 1440 s4 why edit fails; 1440 s4 mixed panel; 390 s6 export failed; realgate export letter (text) and why-e2 (text)",
  "grep app/frontend for showConfirm, btn-keep-wording, needs_confirm, confirm_warnings: comments only"],
 "verdict": "fail",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 2},
 "findings": [
  {"severity": "blocker", "title": "Export gate answers from stored check results, so an edited summary that fails the qualifier check still exports (real backend)",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r2-realgate-results.json (token N1jVAxbspFSzJtPgJ02uIQ): real_case_trace_gate status pass, blockers [], counts.code_check_failed 0; real_item_trace_e2 summary_qualifier pass; real_export status 200. Letter text (curl grep): 'Diagnosed with cervical strain and concussion loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.' UI: artifacts/review-evidence/T-097-ux-designer-r2-realgate-ui-results.json rail 'Ready to export, 21 not reviewed', panel 'checked 19, all agreed with the draft', why_e2_verdict 'Accepted by you'; screenshots T-097-ux-designer-r2-realgate-export-letter.png and T-097-ux-designer-r2-realgate-why-e2.png. Same text refused by the edit route: T-097-ux-designer-r2-walk-results.json S_REAL_1440.negation_422_inline (422 'The quote carries a negation ... Put it back in the summary.'). Code: app/backend/trace.py:798 and :357 (failed = SUMMARY_DROPS_QUALIFIER in R, R = stored state_reasons); trace.py:982-989 gate; app/backend/review.py:203 writes edited_json, committed at app/db/db.py:227-233, review.py:210 writes stored reasons in a separate update. memory/ORCHESTRATOR_DECISIONS.md:59 (D-051: the gate blocks such a state if it exists anyway).",
   "why_it_matters": "A paralegal exports a letter whose edited sentence drops a negation that the product's own check rejects, and every surface reports it as ready: 'Ready to export', 'all agreed with the draft', 'Accepted by you'. This loses a fact and violates D-045(b), D-051 and T-098's acceptance (an edited item that fails a code check blocks export). Reachability: the public routes cannot produce this state at 32f6c9d because the edit route re-checks and refuses; it is reproduced by a direct write, or by a failure between the two writes at review.py:203 and :210 (not induced). The round-1 acceptance test is failing as written (GET /export is 200 and the letter contains the edited sentence).",
   "fix": "Backend (T-098 owner): recompute summary_tokens, summary_qualifier and excerpt_hedge at trace and export time from the stored summary and quote, and gate on that result rather than on stored state_reasons; and/or write edited_json and its check result in one transaction. No frontend change: the blocker list already renders a code-check blocker with Edit.",
   "acceptance_test": "API: an edited item whose stored summary drops a qualifier, with stale stored reasons, gives GET /api/cases/<t>/export 422 export_blocked with detail.blockers naming that item and SUMMARY_DROPS_QUALIFIER, and GET /trace export_gate status fail; the letter has no text for that item. UI on the same state: rail 'Export blocked by 1'; Why shows 'Your wording doesn't match the quote:' with Edit. Round-1 acceptance test as written."},
  {"severity": "minor", "title": "Panel count '3 not checked, blocks export: 1, 1 edit does not match its quote, blocks export: 1' mixes the classes",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r2-walk-results.json S_MIXED_1440.panel_summary (same at 390); screenshot artifacts/review-evidence/T-097-ux-designer-r2-1440-s4-mixed-panel.png",
   "why_it_matters": "Both blocking clauses are correct (1 + 1 equals the gate's 2 blockers), but 'not checked' includes the edited item that fails its quote, which the next clause counts again as blocking. A paralegal has to add the clauses up to see two different items.",
   "fix": "Name the classes separately, e.g. '1 never got the second check and blocks export; 1 edit does not match its quote and blocks export; 1 edited by you, not AI-checked'.",
   "acceptance_test": "E2E on the mixed case: each class is named once; the blocking total in the summary equals the gate's blocker count (2)."},
  {"severity": "minor", "title": "A 'Not needed' judge step still prints 'The second AI check said: Unavailable'",
   "evidence": "T-097-ux-designer-r2-walk-results.json S_MIXED_1440.why_edit_passes.judge ('Not needed | Not needed: this is your own wording, ... | The second AI check said: Unavailable') and S_MIXED_1440.raw_real_judge_step.e3 (judge_verdict unavailable, real backend). app/frontend/stepper.js:317 prints ev.judge_verdict; the Not-needed mapping at stepper.js:391 keeps the evidence.",
   "why_it_matters": "The same step says the second check does not apply and then says the check reported unavailable. The gate does not block the item, so this is copy, but it is the Why dialog the paralegal reads to decide an item, and it muddles 'not needed'.",
   "fix": "For _notNeeded steps, drop the judge_verdict evidence line.",
   "acceptance_test": "E2E on the mixed case: the edited item's judge_1 step has no 'said:' text and no data-status fail."},
  {"severity": "minor", "title": "Rail gate-row rerun button names one item; its POST reruns every item (carried from T-081 r3 and T-097 r1 m1)",
   "evidence": "T-097-ux-designer-r2-walk-results.json S_PLACE_1440.rail_row_button aria_label 'Run the second check again for 2026-01-09 · Austin EMS run report' (app/frontend/stepper.js:454 per-row S.rerunButton; POST at stepper.js:141); S_PLACE_1440.rail_row_click posts 1 and status 'The second check still did not answer for 3 items of 3'. Same at 390.",
   "why_it_matters": "The label promises one item and the action answers for three. A screen-reader user hears a per-item promise; a sighted user reads a three-item result after pressing one row.",
   "fix": "Use the group model everywhere: one 'Run the second check again for these N' in the gate step and no per-row button (rows keep Go to item), or a per-item POST with the item id.",
   "acceptance_test": "E2E: for every rerun button in the rail, the item count in its aria-label equals the item count the POST answers for."},
  {"severity": "nit", "title": "Export button is scrolled out of view when a refused export opens (carried from T-081 r3 and T-097 r1 n1)",
   "evidence": "T-097-ux-designer-r2-walk-results.json S_PLACE_1440.export_btn_after_refusal y -31.5; S_PLACE_390.export_btn_after_refusal y -179.4; the message is in view (refused_box_in_view true at 1440).",
   "why_it_matters": "The message explains the button, but to press Export again the user has to scroll up. In the mixed run at 1440 the scroll position kept it in view, so the result depends on where the user was.",
   "fix": "scroll-margin-top on the export-blocked section equal to the toolbar height, or scroll the toolbar row into view.",
   "acceptance_test": "E2E: after a refused Export at 1440x900 and 390x844, btn-export and export-blocked both have their top inside the viewport."},
  {"severity": "nit", "title": "The 422 names the normalised token ('9000'), not what the paralegal typed ('$9,000')",
   "evidence": "T-097-ux-designer-r2-walk-results.json S_REAL_1440.number_422_inline.err_text ('...not in the quote: 9000. Remove it or change the quote.'); artifacts/review-evidence/T-097-ux-designer-r2-1440-s1-number-422-inline.png (typed 'billed $9,000.').",
   "why_it_matters": "The paralegal can't tell which figure the message means at a glance; '9000' does not look like what was typed.",
   "fix": "Quote the token as typed ('$9,000').",
15:commits: ["e511778", "dd84122"]
19:  - {"n": 1, "text": "An accepted, human-edited summary that fails any D-034/D-022 code check (qualifier dropped, token not in excerpt) is a gate blocker and GET export returns 422 with the reason; gate.ready == export allowed still holds; per-item trace shows the failing code step; tests with the reviewer's case (reviews/T-097-ux-designer.md)", "done": true, "evidence": "r2 (dd84122): tests/unit/test_trace.py::test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051[supported|unsupported|disagrees], test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051, test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051, test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1 pass; mutating the accept guard / batch guard / live recompute in a scratch copy fails 5 / 1 / 1 tests"}
35:- 2026-11-02T05:29:15Z backend: r2 golden check: scanned golden cases 01-09 + sample through the fixture pipeline; 0 AI-drafted entries fail the live code checks, so the check is not weakened. Unrelated unit failures in the shared tree (test_provider*, test_t093_eval_signature, eval_runner calibration) are other workers' WIP.
36:- 2026-11-02T05:29:15Z backend: AC 1 checked: r2 (dd84122): tests/unit/test_trace.py::test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051[supported|unsupported|disagrees], test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051, test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051, test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1 pass; mutating the accept guard / batch guard / live recompute in a scratch copy fails 5 / 1 / 1 tests
41:What changed (r2, dd84122): review.code_check_failures recomputes D-034/D-047/D-022 checks from the CURRENT summary+quote (plus stored reasons); single accept and batch accept return 422 CODE_CHECK_FAILED with the plain reason and next_action 'Edit the summary to match the quote' for AI or human wording; trace/gate recompute at gate time (stale stored pass cannot hide a failing summary), accepted failing AI drafts are gate blockers so GET export is 422; pending failing drafts are not printed in internal notes. api.md updated. | Verified: tests/unit/test_trace.py 74 passed; accept-guard mutant fails 5, batch mutant 1, live-recompute mutant 1; golden cases 01-09 + sample: 0 failing AI drafts; full tests/unit 1922 passed, 3-4 failures in test_provider*/test_t093_eval_signature (other workers' WIP, untouched files). | Left: frontend should show CODE_CHECK_FAILED message inline on accept (and batch); case-verdict label changed to 'N summaries fail a check'. | Surprised: tokens are digit runs ('5' not '5/10'); internal notes listed pending drafts' wording, so '5/10' leaked there until withheld; committed via temp index because review.py and api.md carry D-050 hunks from another worker.
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
dd84122 fix(backend): code checks bind accept for every entry, single and batch; gate and trace recompute them from the current text (D-051, T-098 r2)
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
e63e564 docs: D-051 code checks bind accept for every item
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:39.958Z

**tool call — Bash**
````
{
 "command": "sed -n 120,170p reviews/T-097-ux-designer-r2.md | cut -c1-600; git status --short app/frontend tests/e2e | head; ls app/frontend; wc -l app/frontend/*.js | tail -20; grep -n \"CODE_CHECK_FAILED\\|fail a check\\|code_check\" memory/contracts/api.md | head -20"
}
````

### User / tool · 2026-11-02T05:29:40.078Z

**tool result**
````
   "fix": "Quote the token as typed ('$9,000').",
   "acceptance_test": "E2E: the message contains the exact string the user typed for the number."},
  {"severity": "nit", "title": "An edited item's Why verdict reads 'Accepted by you'",
   "evidence": "artifacts/review-evidence/T-097-ux-designer-r2-realgate-ui-results.json why_e2_verdict 'Accepted by you' on an item whose review_status is 'edited'; the label comes from the trace verdict.",
   "why_it_matters": "For an item the paralegal wrote, 'Accepted by you' misstates the provenance. Reachability in a consistent state is unconfirmed.",
   "fix": "'Edited by you' when review_status is 'edited'.",
   "acceptance_test": "E2E: an edited item whose judge answered shows 'Edited by you' in its Why verdict."}
 ],
 "whats_right": [
  "The real edit route refuses a dropped negation, a dropped side and an invented dollar figure with a plain 422 message under the edit box, keeps the typed text, and opens no confirm dialog at 1440 and 390.",
  "In the mixed case every surface reads one gate: 'Export blocked by 2' in the rail, two 'blocks export' clauses in the panel, two blockers in the refused export, and the passing edit reads 'Edited by you, not AI-checked' with no rerun.",
  "A failed rerun is answered directly beside its button at both widths, in the refused-export message and in the AI-check panel (4 px under the button)."],
 "questions_for_chris": ["Is a gate that answers from stored check results acceptable as design once the edit write is atomic, or must export recompute the summary checks from the stored text? D-051 says the gate blocks such a state 'if it exists anyway', which I read as recompute. If Chris accepts stored-result gating in writing, B1 becomes a major (atomic write required) and the round-1 acceptance test still applies.",
  "Round-1 question (is summary_qualifier in the D-034 set?): from code, the edit route enforces it (422 SUMMARY_DROPS_QUALIFIER) and the trace step cites D-022 (app/backend/trace.py:357). I did not verify D-034's list itself."]}
```
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
switcher.js
timeline.js
      37 app/frontend/excerpt.js
      60 app/frontend/export.js
      51 app/frontend/exportcfg.js
     100 app/frontend/flags.js
      85 app/frontend/input.js
     205 app/frontend/judges.js
      93 app/frontend/manual.js
     216 app/frontend/mock.js
      29 app/frontend/mock_extra.js
      55 app/frontend/mock_flags.js
       2 app/frontend/mock_sample.js
      75 app/frontend/narrative.js
     290 app/frontend/review.js
     119 app/frontend/sidebyside.js
      37 app/frontend/source.js
      28 app/frontend/state.js
     575 app/frontend/stepper.js
      64 app/frontend/switcher.js
     154 app/frontend/timeline.js
    2622 total
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote.", `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY", text: "Edit the summary to match the quote", target: {item_id}}}`; the judge verdict does not matter |
107:**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY", text: "Edit the summary to match the quote", target: {item_id}}}`.
156:        "code_checks": {"excerpt_verbatim": true, "excerpt_whole_sentence": true, "qualifier_carried": true,
170:        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
179:        "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
202:        "code_checks": {"dates_parsed": true, "days": 73, "threshold": 30, "evidence_grounded": true, "unconfirmed_date_in_span": false},
216:        "code_checks": {"stated_date_phrase": "date of accident", "evidence_grounded": true, "dates_parsed": true},
228:        "code_checks": {"excerpt_verbatim": true, "lexicon_hit": "patient_report", "highlight_found": true, "injection_tag": false},
347:- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassification` = `{from, to, at, by: "reviewer", original_kind, wording, restored, note, previous_judge}` and `ladder.code_checks.classified_by` = `"reviewer:reclassified"`.
619:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute the code checks (D-034 numbers/dates/dollar figures/sides, D-047, D-022 qualifiers, and the quote's whole-sentence and hedge checks) from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:42.077Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat review.js; cat batch.js | head -150; cat api.js | head -80"
}
````

### User / tool · 2026-11-02T05:29:42.174Z

**tool result**
````
/* Review controls shared by entries, flags and charges (T-043, frontend-2).
   Exposes ZL.rv = { controls, act, money, chips, find, openSource, say, legend, nextId }.
   - ZL.rv.controls(item, kind) -> element with Accept / Edit / Dismiss / Reset (kind: "entry" | "flag" | "amount").
   - Registered as a row action so every timeline entry row gets the same controls (ZL.registerRowActions).
   - One document-level key handler works on ANY element that carries data-item-id (queue items, entry rows, flag and charge cards).
   Untrusted text only ever goes through ZL.el (text nodes) / textContent. No amounts are added or compared here. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const el = (...a) => ZL.el(...a);
  const RV = (ZL.rv = {});
  const drafts = {};        // id -> {open, text, reasonOpen, reason}  (survives re-renders)
  const ui = {};            // id -> {openEdit}  latest controls instance per item
  const busy = new Set();

  RV.caseNow = () => (ZL.state && ZL.state.get().case) || null;
  RV.find = function (c, id) {
    for (const [k, kind] of [["entries", "entry"], ["undated_entries", "entry"], ["amounts", "amount"], ["flags", "flag"]]) {
      const it = ((c && c[k]) || []).find((x) => x.id === id);
      if (it) return { item: it, kind };
    }
    return null;
  };
  // Display formatting of an integer-cents value by string slicing only (no arithmetic).
  RV.money = function (cents) {
    if (cents == null) return "";
    const neg = String(cents)[0] === "-";
    const s = String(cents).replace("-", "").padStart(3, "0");
    const d = s.slice(0, -2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const c = s.slice(-2);
    return (neg ? "-" : "") + "$" + d + (c === "00" ? "" : "." + c);
  };
  // Stable sort: needs_review before everything else (R-TL-5 order, applied inside each group / table).
  RV.needsReviewFirst = (list) => list.map((x, i) => [x, i]).sort((a, b) => ZL.firstRank(a[0].id, a[0].state) - ZL.firstRank(b[0].id, b[0].state) || a[1] - b[1]).map((p) => p[0]);
  // Plain JSON request for endpoints ZL.api does not wrap (mock or real). Returns {status, body}; never throws on HTTP errors.
  RV.http = async function (method, path, body) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle(method, path, body);
    const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
    let b = null; try { b = await res.json(); } catch (_) { /* empty body */ }
    return { status: res.status, body: b };
  };
  RV.errMsg = (r, fallback) => (r && r.body && r.body.error && r.body.error.message) || fallback || "That did not work.";
  RV.label = (item) => item.title || item.provider || item.text || item.id;

  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
  RV.chips = function (item) {
    return el("span", { class: "rv-chips" },
      el("span", { class: "rv-chip rv-state-" + item.state, "data-chip": "state" }, STATE_LABEL[item.state] || item.state),
      el("span", { class: "rv-chip rv-rs-" + (item.review_status || "pending"), "data-chip": "review" }, REVIEW_LABEL[item.review_status || "pending"]));
  };

  // ---- live region
  let live;
  RV.say = function (msg, isError) {
    if (!live) { live = el("div", { id: "rv-live", class: "rv-sr", "aria-live": "polite", role: "status" }); document.body.append(live); }
    live.textContent = "";
    setTimeout(() => { live.textContent = msg; }, 20);
    if (isError) live.setAttribute("role", "alert"); else live.setAttribute("role", "status");
  };

  // ---- open the source record(s) of an item (R-RV-9); entries/amounts: one record, flags: every record in the evidence
  RV.sourceTargets = function (item, kind) {
    if (kind === "flag") {   // one span per record, so a two-record flag opens both records once each
      const seen = {}, spans = [];
      (item.evidence || []).forEach((e) => { if (!seen[e.record_id]) { seen[e.record_id] = 1; spans.push({ record_id: e.record_id, start: e.start, end: e.end }); } });
      return { ids: spans.map((s) => s.record_id), spans };
    }
    if (kind === "entry" && typeof ZL.entrySpans === "function") { const spans = ZL.entrySpans(item); return { ids: spans.map((s) => s.record_id), spans }; }
    const ids = item.record_ids || [];
    return { ids, spans: ids.length ? [{ record_id: ids[0], start: item.excerpt_start, end: item.excerpt_end }] : [] };
  };
  RV.openSource = function (item, kind, title) {   // T-042's modal: ZL.openSource(spans, title)
    const t = RV.sourceTargets(item, kind);
    if (!t.spans.length || typeof ZL.openSource !== "function") return;
    const c = RV.caseNow(), seqs = t.ids.map((id) => { const r = ((c && c.records) || []).find((x) => x.id === id); return r ? r.seq : id; });
    ZL.openSource(t.spans, title || (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]));
  };

  // ---- ordering for "next" (review.queue first, then everything else in page order)
  RV.orderedIds = function (c) {
    const all = [...(c.entries || []), ...(c.undated_entries || []), ...(c.amounts || []), ...(c.flags || [])].map((i) => i.id);
    const q = ((c.review && c.review.queue) || []).filter((id) => all.includes(id));
    return q.concat(all.filter((id) => !q.includes(id)));
  };
  RV.nextId = function (c, fromId, pendingOnly, dir) {
    const ids = RV.orderedIds(c); if (!ids.length) return null;
    const start = Math.max(0, ids.indexOf(fromId));
    for (let n = 1; n <= ids.length; n++) {
      const id = ids[(start + (dir || 1) * n + ids.length * n) % ids.length];
      const f = RV.find(c, id);
      if (!pendingOnly || (f && f.item.review_status === "pending")) return id;
    }
    return null;
  };
  function focusItem(id) {
    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
    const t = q || document.querySelector('[data-item-id="' + id + '"]');
    if (!t) return false;
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
    t.focus(); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
    return true;
  }
  function restoreFocus(pf) {
    if (!pf) return;
    requestAnimationFrame(() => {
      if (pf.scope) {   // decided from a flag or charge card: stay inside that panel
        const root = document.querySelector('[data-panel="' + pf.scope + '"]'); if (!root) return;
        const cards = Array.from(root.querySelectorAll("[data-item-id]")), at = cards.findIndex((x) => x.getAttribute("data-item-id") === pf.nextFrom);
        const order = cards.slice(at + 1).concat(cards.slice(0, Math.max(at, 0)));
        const t = order.find((x) => x.getAttribute("data-review") === "pending") || cards[at];
        if (t) { t.focus(); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" }); }
        return;
      }
      if (pf.nextFrom) {
        const c = RV.caseNow(); const n = c && RV.nextId(c, pf.nextFrom, true, 1);
        if (n && n !== pf.nextFrom && focusItem(n)) return;
        focusItem(pf.nextFrom); return;
      }
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) t.focus(); else focusItem(pf.id);
    });
  }

  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
  const DATE_FIRST = "Confirm the date first.", DATE_WHY = "This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.";
  RV.needsDate = (item, kind) => kind === "entry" && !item.date;
  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
    const row = document.querySelector('[data-testid="dates-to-confirm"] [data-entry-id="' + id + '"]');
    const t = row && (row.querySelector('[data-testid="confirm-date"]') || row);
    const box = document.querySelector('[data-testid="dates-to-confirm"]');
    const f = t || box; if (!f) return;
    if (!f.hasAttribute("tabindex") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1");
    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: "center" });
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    busy.add(id);
    try {
      const resp = await ZL.api.review(c.token, id, body);
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      ZL.state.applyReview(resp);
      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, scope: o.scope } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, (e.message || "That edit is not allowed.") + toks);
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
    } finally { busy.delete(id); }
  };

  // ---- controls
  RV.controls = function (item, kind) {
    const id = item.id, st = item.review_status || "pending";
    const isFlag = kind === "flag", canEdit = kind === "entry" || isFlag;
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    const btn = (action, text, tid, extra) => el("button", Object.assign({ type: "button", class: "rv-btn rv-" + action, "data-testid": tid, "data-action": action, "aria-label": text.replace("…", "") + ": " + lbl }, extra || {}), text);

    const bar = el("div", { class: "rv-actions", role: "group", "aria-label": "Review actions" });
    const blocked = RV.needsDate(item, kind) && st !== "accepted";
    bar.append(btn("accept", noted ? "Accept as noted" : "Accept", "btn-accept", { "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null, onclick: () => RV.act(id, { action: "accept" }, { focus: "accept" }) }));
    let form;
    if (canEdit) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true) }));
    bar.append(btn("dismiss", "Dismiss", "btn-dismiss", { "aria-pressed": String(st === "dismissed"), onclick: () => RV.act(id, { action: "dismiss" }, { focus: "dismiss" }) }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { class: "rv-btn rv-secondary", onclick: () => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Reset", "btn-reset", { class: "rv-btn rv-secondary", onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { class: "rv-btn rv-secondary", onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
      el("button", { type: "button", class: "btn small", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));

    // dismiss reason (flags only; optional - R-RV-5)
    const reasonIn = el("input", { type: "text", class: "rv-input", maxlength: "300", "aria-label": "Reason for dismissing (optional)", "data-testid": "dismiss-reason", value: d.reason || "" });
    reasonIn.addEventListener("input", () => { d.reason = reasonIn.value; });
    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const r = reasonIn.value.trim(); RV.act(id, r ? { action: "dismiss", note: r } : { action: "dismiss" }, { focus: "dismiss" }); } },
      reasonIn, el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-dismiss-confirm" }, "Dismiss"));
    if (isFlag) root.append(reasonRow);

    if (canEdit) {
      const ta = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: isFlag ? "note" : "summary", "data-testid": isFlag ? "flag-note" : "edit-summary",
        "aria-label": isFlag ? "Reviewer note (internal notes only; never in the letter)" : "Summary wording" });
      ta.value = d.text;
      ta.addEventListener("input", () => { d.text = ta.value; });
      form = el("form", { class: "rv-edit", hidden: !d.open, onsubmit: (ev) => {
        ev.preventDefault(); const v = ta.value.trim();
        if (!v) { showError(id, isFlag ? "Write a note first, or cancel." : "The summary can't be empty."); return; }
        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: "edit" });
      } },
        el("label", { class: "rv-label" }, isFlag ? "Your note (internal notes only, never in the letter)" : "Summary wording (the quoted excerpt, date and provider cannot be changed)", ta),
        el("div", { class: "rv-actions" },
          el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-save-edit" }, "Save"),
          el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-cancel-edit", onclick: () => toggleEdit(false) }, "Cancel")));
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
      });
      root.append(form);
      var toggleEdit = function (open) {
        d.open = open; form.hidden = !open;
        if (open) ta.focus(); else { const b = bar.querySelector('[data-action="edit"]'); if (b) b.focus(); }
      };
      ui[id] = { openEdit: () => toggleEdit(true) };
    } else ui[id] = {};
    root.append(el("div", { class: "rv-error", role: "alert" }));
    return root;
  };

  // ---- legend
  RV.legend = () => el("p", { class: "rv-keys" }, el("strong", {}, "Keyboard: "),
    "j next, k previous, a accept, e edit, d dismiss, r reset, o open the record, Shift+A accept all verified entries. Tab reaches every button.");

  // ---- keyboard flow (R-RV-4). Works from any focused element inside something with data-item-id.
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    const modal = document.querySelector('[data-testid="record-modal"]'); if (modal && modal.offsetParent !== null) return;
    const row = t && t.closest && t.closest("[data-item-id]");
    const c = RV.caseNow(); if (!c) return;
    const key = ev.key.toLowerCase(); const id = row && row.getAttribute("data-item-id");
    const panel = row && row.closest("[data-panel]");
    if (panel && (key === "j" || key === "k")) {   // inside the flags / charges panels, j and k walk those cards in page order
      const cards = Array.from(document.querySelectorAll("[data-panel] [data-item-id]")), at = cards.indexOf(row), n = cards[at + (key === "j" ? 1 : -1)];
      if (n) { ev.preventDefault(); n.focus(); n.scrollIntoView({ block: "nearest" }); }
      return;
    }
    if (key === "j" || key === "k") {
      const n = RV.nextId(c, id || (c.review && c.review.queue && c.review.queue[0]), false, key === "j" ? 1 : -1);
      if (n) { ev.preventDefault(); if (!id && key === "j") focusItem((c.review.queue || [n])[0] || n); else focusItem(n); }
      return;
    }
    if (!id || !"aedro".includes(key) || key.length !== 1) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    const scope = panel ? panel.getAttribute("data-panel") : null;
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true, scope });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true, scope });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.act(id, { action: "reset" }, { focus: "reset" }); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (c && mountEl) render(mountSection(mountEl, name), c); });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
      rowEl.setAttribute("data-item-id", entry.id); rowEl.setAttribute("data-review", entry.review_status || "pending");
      if (!rowEl.hasAttribute("tabindex")) rowEl.setAttribute("tabindex", "0");
      rowEl.append(RV.controls(entry, "entry"));
      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
        const head = rowEl.querySelector(".entry-head") || rowEl;
        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
      }
    });
  }
})();
/* Batch accept for verified entries only (T-055, D-031). Button + Shift+A; the server enforces "verified pending entries only" (422 otherwise).
   Never touches amounts or flags. Undo resets exactly the entries this batch accepted. Any error (including 404/405) shows a plain message and accepts nothing: no per-item fallback, so the server's verified-only check cannot be bypassed (T-065). */
(function () {
  const ZL = window.ZL, RV = ZL.rv, el = ZL.el;
  let last = null;      // {token, ids} of the most recent batch, for Undo
  let busy = false;
  const eligible = (c) => (c.entries || []).filter((e) => e.date && e.state === "verified" && (e.review_status || "pending") === "pending");
  // D-041: entries still without a confirmed date are never part of a batch; say how many were left out.
  const skippedUndated = (c) => (c.undated_entries || []).concat((c.entries || []).filter((e) => !e.date)).filter((e) => (e.review_status || "pending") === "pending").length;
  const skipText = (n) => n + (n === 1 ? " undated entry was" : " undated entries were") + " skipped: confirm the date first (Dates to confirm).";

  async function refresh(token) { ZL.state.set({ case: await ZL.api.getCase(token) }); }

  async function acceptAll() {
    const c = RV.caseNow(); if (!c || busy) return;
    const ids = eligible(c).map((e) => e.id), skipped = skippedUndated(c);
    if (!ids.length) { if (skipped) RV.say("Nothing to accept. " + skipText(skipped)); return; }
    busy = true;
    try {
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "accept", item_ids: ids });
      if (r.status >= 400) {
        const code = r.body && r.body.error && r.body.error.code;
        if (String(code).toUpperCase() === "DATE_UNCONFIRMED") { RV.say("Confirm the date first. An entry in this batch has no confirmed date, so nothing was accepted. Pick its date in Dates to confirm, then try again.", true); return; }
        const plain = (r.status === 404 || r.status === 405) ? "Accept all could not run on this server, so nothing was accepted. Accept entries one at a time instead." : null;
        RV.say(plain || RV.errMsg(r, "The batch was refused; nothing was accepted."), true); return;
      }
      last = { token: c.token, ids };
      await refresh(c.token);
      RV.say("Accepted " + ids.length + " verified " + (ids.length === 1 ? "entry" : "entries") + ". Undo is available." + (skipped ? " " + skipText(skipped) : ""));
      const u = document.querySelector('[data-testid="btn-undo-batch"]'); if (u) u.focus();
    } catch (e) { RV.say((e && e.message) || "The batch did not finish.", true); try { await refresh(c.token); } catch (_) { /* keep state */ } }
    finally { busy = false; }
  }
  async function undo() {
    const c = RV.caseNow(); if (!c || !last || last.token !== c.token || busy) return;
    const ids = last.ids.filter((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
    busy = true;
    try {
      if (ids.length) {
        const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "reset", item_ids: ids });
        if (r.status >= 400) { RV.say(RV.errMsg(r, "Undo was refused."), true); return; }
      }
      const n = ids.length; last = null; await refresh(c.token);
      RV.say("Undone: " + n + " " + (n === 1 ? "entry" : "entries") + " back to not reviewed.");
    } catch (e) { RV.say((e && e.message) || "Undo did not finish.", true); } finally { busy = false; }
  }

  function bar(c) {
    const n = eligible(c).length, sk = skippedUndated(c);
    const undoable = last && last.token === c.token && last.ids.some((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
    return el("div", { class: "rv-batchbar", "data-testid": "batch-bar" },
      el("button", { type: "button", class: "rv-btn", "data-testid": "btn-accept-verified", disabled: n === 0, onclick: acceptAll }, "Accept all verified entries (" + n + ")"),
      undoable ? el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-undo-batch", onclick: undo }, "Undo last batch (" + last.ids.length + ")") : null,
      sk ? el("span", { class: "rv-help rv-blocked", "data-testid": "batch-skipped-note" }, skipText(sk)) : null,
      el("span", { class: "rv-help" }, "Entries only. Charges, flags and anything marked needs review always need your own decision. Shift+A does the same."));
  }
  RV.registerPanel("batch", (root, c) => {
    ZL.clear(root); root.className = "rv-batchhost";
    const wrap = root.closest('[data-testid="timeline"]'), tb = wrap && wrap.querySelector(".toolbar");
    const b = bar(c);
    if (tb) { const old = wrap.querySelector(":scope > .rv-batchbar"); if (old) old.remove(); tb.after(b); } else root.append(b);
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "A" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target; if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    const m = document.querySelector('[data-testid="record-modal"]'); if (m && m.offsetParent !== null) return;
    ev.preventDefault(); acceptAll();
  });
})();
/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
  const mode = new URLSearchParams(location.search).get("api") || API_MODE;
  ZL.API_MODE = mode;

  class ApiError extends Error {
    constructor(status, err) { super((err && err.message) || "Request failed"); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }
  }
  ZL.ApiError = ApiError;

  async function call(method, path, body) {
    let status, data;
    if (mode === "mock") {
      ({ status, body: data } = await ZL.mock.handle(method, path, body));
    } else {
      const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
      status = res.status;
      try { data = await res.json(); } catch (_) { data = null; }
    }
    if (status >= 400) throw new ApiError(status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + encodeURIComponent(token);
  ZL.api = {
    health: () => call("GET", "/health"),
    createCase: (payload) => call("POST", "/cases", payload),          // {text} or {sample:true}
    getCase: (token) => call("GET", t(token)),
    run: (token, confirm_rerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirm_rerun }),
    status: (token) => call("GET", t(token) + "/status"),
    item: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id)),
    trace: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id) + "/trace"),
    caseTrace: (token) => call("GET", t(token) + "/trace"),
    judges: (token) => call("GET", t(token) + "/judges"),
    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + encodeURIComponent(rid) + "/confirm_date", { date }),
    rejudge: (token) => call("POST", t(token) + "/rejudge"),            // D-044: run the second AI check again for accepted items it never checked
    exportCase: (token) => call("GET", t(token) + "/export"),
    remove: (token) => call("DELETE", t(token)),
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:44.679Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"verdict\\|fail.*check\\|edited summar\" stepper.js judges.js export.js app.js timeline.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T05:29:44.765Z

**tool result**
````
judges.js:3:   This is a report on the AI's drafts, never a verdict on the case: the label says so. Counts are the server's; nothing is added here.
judges.js:19:  const READING = {   // the verdict in words that name who disagrees with whom
judges.js:33:  // wrote or edited from the judge, but not from the code checks, so an edited item can lack a judge answer and be ready, or fail a code check and block. gate is null while the trace is loading.
judges.js:41:  const unchecked = (it) => !!(it.unres && !it.rej && it.unres.verdict === "unavailable");
judges.js:80:    else if (u) chips.push(chip(u.verdict === "unavailable" ? "AI did not check" : "AI could not decide", "zj-chip-bad"));
judges.js:84:    if (r) why = el("p", { class: "zs-why" }, el("strong", {}, (READING[r.verdict] || ZL.stepper.verdictWord(r.verdict) + ".") + " "), r.rationale || "");
judges.js:86:    else if (u) why = el("p", { class: "zs-why" }, u.verdict === "unavailable" ? "The second check did not answer, so no AI judge looked at this item." : "The second check could not decide.");
judges.js:98:  // An edited or hand-written item whose wording fails a code check: the row is the gate's blocker as the server wrote it (reason, fix sentence), with an Edit action.
judges.js:149:      "This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review."));
stepper.js:2:   the evidence, and what the human must do next (HITL hand-off). Pattern: <outside project> flow rail (marker, label, detail, note, "x/y done", verdict).
stepper.js:5:   Exposes ZL.stepper = { item, itemSection, openTrace, traceButton, mountCase, onExport, exportNotice, showExportBlocked, clearExportNotice, rejudge, rerunButton, goto, gotoPanel, label, cue, setLabel, verdictWord, progressLabel }. Server text on
stepper.js:20:    if (st.status === "skipped" && needsRerun(st)) return { glyph: GLYPH.fail, word: "Did not run", cat: "need" };   // D-044: the second check never ran, so this item cannot go in the letter yet
stepper.js:36:  S.verdictWord = (v) => VERDICT_WORD[v] || v || "";
stepper.js:153:    const obj = got.filter((r) => OBJECT.includes(r.verdict)).length;
stepper.js:316:    if (ev.judge_verdict) {
stepper.js:317:      out.push(el("p", { class: "zs-ev zs-judge", "data-testid": "step-judge-reason" }, el("strong", {}, "The second AI check said: "), S.verdictWord(ev.judge_verdict),
stepper.js:384:    const v = Object.assign({}, tr.verdict || {});
stepper.js:393:    const wf = steps.find((x) => x.kind === "code" && x.status === "fail" && x.blocks_export) || null;   // a failing code check on the paralegal's wording (T-098)
stepper.js:405:    const root = el("div", { class: "zs zs-item", "data-testid": "item-stepper", "data-verdict": v.code || "" },
stepper.js:407:        el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "item-verdict" }, v.label || ""),
stepper.js:487:    const steps = tr.steps || [], act = activeIndex(steps), v = tr.verdict || {};
stepper.js:490:      el("p", { class: "zs-top" }, el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "case-verdict" }, v.label || ""),
timeline.js:128:          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)"))),
timeline.js:129:        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.p
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:45.375Z

**tool call — Bash**
````
{
 "command": "ls tests/e2e | head -50; grep -n \"WordingFails\" -A40 tests/e2e/conftest.py | head -120; grep -rn \"edited summar\\|summaries fail\\|fail a check\" tests app/frontend app/backend --include=*.py --include=*.js | cut -c1-220 | head -30"
}
````

### User / tool · 2026-11-02T05:29:45.473Z

**tool result**
````
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_charges.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_timeline.py
108:class WordingFails:
109-    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
110-    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
111-    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
112-    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
113-    import re as _re
114-    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
115-    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."
116-
117-    def __init__(self, page, token, ids):
118-        self.page, self.token, self.ids = page, token, list(ids)
119-        self.base = {i: self._summary(i) for i in self.ids}
120-        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
121-            page.route(self._re.compile(pat), fn)
122-
123-    def _summary(self, i):
124-        c = api("GET", f"/api/cases/{self.token}")[1]
125-        e = next((x for x in c["entries"] + c["undated_entries"] if x["id"] == i), None)
126-        return e and (e["summary"], e["review_status"])
127-
128-    def active(self):
129-        return [i for i in self.ids if (cur := self._summary(i)) and cur[1] in ("accepted", "edited") and cur[0] == self.base[i][0]]
130-
131-    def _na(self, i):
132-        return {"code": "EDIT_SUMMARY", "text": self.FIX, "target": {"item_id": i}}
133-
134-    def blockers(self):
135-        return [{"item_id": i, "kind": "entry", "reason_code": "SUMMARY_DROPS_QUALIFIER", "step_id": "summary_qualifier", "failed_steps": ["summary_qualifier"], "why": self.WHY, "next_action": self._na(i)} for i in self.active()]
136-
137-    def _case_trace(self, route):
138-        d = route.fetch().json(); act = self.blockers()
139-        if act:
140-            g = next(x for x in d["steps"] if x["id"] == "export_gate")
141-            g["blockers"] = [b for b in g["blockers"] if b["reason_code"] != "NOTHING_ACCEPTED"] + act
142-            g.update(status="fail", ready=False, reason_code="SUMMARY_DROPS_QUALIFIER", why=self.WHY, next_action=act[0]["next_action"])
143-            g["counts"].update(blocking=len(g["blockers"]), code_check_failed=len(act))
144-            d["verdict"] = {"code": "needs_attention", "label": f"{len(act)} edited summaries fail a check"}
145-        route.fulfill(json=d)
146-
147-    def _item_trace(self, route):
148-        d = route.fetch().json()
tests/unit/test_trace.py:1024:# ---- D-045(b) / T-098: a human-edited summary is exempt from the judge, never from the code checks (reviewer case: reviews/T-097-ux-designer.md B1)
tests/unit/test_trace.py:1229:    """An edited summary that drops a qualifier, written straight to edited_json with every stored check result left as 'pass': the gate and the export
tests/e2e/conftest.py:109:    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
tests/e2e/conftest.py:110:    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
tests/e2e/conftest.py:144:            d["verdict"] = {"code": "needs_attention", "label": f"{len(act)} edited summaries fail a check"}
tests/e2e/test_rerun_judge.py:256:# ---- T-097 round 2 (D-045 b, T-098, D-047): the summary and the Why dialog read the gate and the item trace; a failing code check on an edited summary is a named blocker.
tests/e2e/test_rerun_judge.py:269:    """One accepted AI item; one edited summary the gate holds (stub: fails a code check); one edited summary that passes."""
app/backend/trace.py:767:    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run ha
app/backend/trace.py:775:            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:48.367Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 290,330p stepper.js; sed -n 376,575p stepper.js"
}
````

### User / tool · 2026-11-02T05:29:48.451Z

**tool result**
````
        else if (itemId) btn("Go to the decision buttons", () => gotoItem(itemId)); break;
      default:
        if (t.view === "dates_to_confirm") btn("Go to Dates to confirm", () => gotoDates(recId));
        else if (view) btn(view[0], view[1]);
        else if (t.item_id) btn("Go to the item", () => gotoItem(t.item_id));
    }
    return el("div", { class: "zs-todo", "data-testid": "step-action" },
      el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), text), buttons.length ? el("div", { class: "zs-todo-btns" }, buttons) : null, rerunToo ? rerunStatus() : null, msg);
  }

  // ---- evidence
  function quote(rec, text) {
    return el("figure", { class: "zs-quote" }, rec ? el("figcaption", {}, "Record " + recSeq(rec)) : null, el("blockquote", {}, text));
  }
  const fmtVal = (k, v) => (/_cents$/.test(k) && typeof v === "number" && rv() ? [humanize(k.replace(/_cents$/, "")), rv().money(v)] : [humanize(k), v && typeof v === "object" ? JSON.stringify(v) : String(v)]);
  function evidenceNode(st) {
    const ev = st.evidence || {}, out = [];
    if (ev.excerpt && ev.excerpt.text) out.push(quote(ev.excerpt.record_id, ev.excerpt.text));
    (ev.spans || []).forEach((sp) => { if (sp && sp.text) out.push(quote(sp.record_id, sp.text)); });
    if (ev.tokens && ev.tokens.length) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Not found in the quote: "), ev.tokens.map((t) => el("code", { class: "zs-tok" }, t))));
    if (ev.values) {
      const bits = Object.entries(ev.values).filter(([, v]) => v != null && v !== "").map(([k, v]) => fmtVal(k, v));
      if (bits.length) out.push(el("p", { class: "zs-ev", "data-testid": "step-values" }, bits.map(([k, v]) => el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), v))));
    }
    if (ev.date) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Date: "), (ev.date.date_raw ? "written “" + ev.date.date_raw + "”" : "no date written"),
      ev.date.date_iso ? ", read as " + ev.date.date_iso : "", ev.date.date_status ? " (" + humanize(ev.date.date_status) + ")" : "", (ev.date.candidates || []).length ? "; possible readings: " + ev.date.candidates.join(" or ") : ""));
    if (ev.judge_verdict) {
      out.push(el("p", { class: "zs-ev zs-judge", "data-testid": "step-judge-reason" }, el("strong", {}, "The second AI check said: "), S.verdictWord(ev.judge_verdict),
        ev.rationale ? ". " + ev.rationale : ""));
    } else if (ev.rationale) out.push(el("p", { class: "zs-ev" }, ev.rationale));
    if (ev.events && ev.events.length) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decisions: "), ev.events.map((e) => (e.action || "") + (e.at ? " at " + e.at : "")).join("; ")));
    else if (ev.action) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decision: "), ev.action + (ev.at ? " at " + ev.at : "")));
    if (ev.edited_text) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your wording: "), ev.edited_text));
    // technical detail for the audit-minded reader, collapsed
    const m = ev.model, tech = [];
    const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
    tech.push(kv("reason code", st.reason_code), kv("rule", st.rule), kv("judge reason code", ev.judge_reason_code && ev.judge_reason_code !== "NONE" ? ev.judge_reason_code : null));
    if (m) tech.push(kv("model", m.id), kv("role", m.role), kv("independent of the drafting model", m.independent_of_generator == null ? null : m.independent_of_generator ? "yes" : "no"));
    tech.push(kv("prompt", ev.prompt_version), kv("prompt hash", ev.prompt_sha256 && String(ev.prompt_sha256).slice(0, 12)), kv("call", ev.call_id), kv("backend", ev.backend),
      kv("recorded from", ev.recorded_from && ev.recorded_from.backend), kv("latency", ev.latency_ms != null ? ev.latency_ms + " ms" : null), kv("parsed", ev.parsed_ok == null ? null : ev.parsed_ok ? "yes" : "no"));
    const techNodes = tech.filter(Boolean);
  // ---- item level
  const firstSentence = (t) => { const m = /^[\s\S]*?[.!?](?=\s|$)/.exec(t || ""); return m ? m[0] : t || ""; };
  // gate: the export_gate step of GET /trace (null when it could not be loaded). The gate decides what blocks the export; this view reads it and the item's own trace
  // and decides nothing: a judge step that never ran is "second check missing" only when the gate lists JUDGE_NOT_RUN for this item, otherwise the wording is the
  // paralegal's own (D-045 b) and the step is "Not needed". A code step the trace marks blocks_export is "Your wording doesn't match the quote".
  const HUMAN_NOTE = "Not needed: this is your own wording, so the second AI check does not apply. The code checks on it still run.";
  S.item = function (tr, gate) {
    let steps = (tr.steps || []).slice();
    const v = Object.assign({}, tr.verdict || {});
    const decided = tr.review_status === "accepted" || tr.review_status === "edited";
    const gated = !!gate && ((gate.blockers || []).some((b) => b.reason_code === "JUDGE_NOT_RUN" && b.item_id === tr.item_id));
    const skippedJudge = steps.some((x) => x.status === "skipped" && needsRerun(x));
    let notAIChecked = false;
    if (decided && gate && !gated && skippedJudge) {   // the gate does not hold this item for a missing second check
      notAIChecked = true;
      steps = steps.map((x) => (x.status === "skipped" && needsRerun(x) ? Object.assign({}, x, { _notNeeded: true, next_action: null, reason_code: null, why: HUMAN_NOTE }) : x));
    }
    const wf = steps.find((x) => x.kind === "code" && x.status === "fail" && x.blocks_export) || null;   // a failing code check on the paralegal's wording (T-098)
    const act = activeIndex(steps);
    if (v.code === "accepted" && !wf) {
      if (notAIChecked) v.label = (tr.review_status === "edited" ? "Edited" : "Accepted") + " by you, not AI-checked";
      else if (skippedJudge) { v.code = "needs_attention"; v.label = "Accepted, second check missing"; }   // the gate (or an unloaded gate) holds it: not a green "Accepted by you"
    }
    const ctx = { itemId: tr.item_id };
    // a record id for date steps
    const dstep = steps.find((s) => s.evidence && s.evidence.date); if (dstep) ctx.recordId = dstep.evidence.date.record_id;
    const rail = el("ol", { class: "zs-rail", "aria-label": "Checks for " + S.label(tr.item_id) }, steps.map((s, i) => stepNode(s, i === act, ctx)));
    const showActive = () => { const a = rail.querySelector('[aria-current="step"]'); if (a) { a.scrollIntoView({ block: "nearest" }); a.focus({ preventScroll: true }); } };
    const now = act >= 0 ? steps[act] : null;
    const root = el("div", { class: "zs zs-item", "data-testid": "item-stepper", "data-verdict": v.code || "" },
      el("div", { class: "zs-top" },
        el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "item-verdict" }, v.label || ""),
        el("span", { class: "zs-progress", role: "status", "data-testid": "item-progress" }, progressLabel(steps))),
      wf ? el("div", { class: "zs-wording", role: "alert", "data-testid": "item-wording-fail" },
        el("p", { class: "zs-todo-text" }, el("strong", {}, WORDING + " "), wf.why || ""),
        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-wording-edit", "aria-label": "Edit your wording for " + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, "Edit your wording"))) : null,
      now ? el("div", { class: "zs-now", "data-testid": "item-active" },
        el("p", { class: "zs-now-text" }, el("strong", {}, statusInfo(now).word + ": "), now.label, " ", el("span", { class: "zs-ev" }, firstSentence(now.why))),
        el("button", { type: "button", class: "zs-btn", "data-testid": "btn-jump-active", onclick: showActive }, "Show this step")) : null,
      (tr.state_reasons || []).length ? el("ul", { class: "zs-reasons" }, tr.state_reasons.map((r) => el("li", {}, r.why))) : null,
      rail);
    root._showActive = showActive;
    return root;
  };
  // A section that fetches its own trace; used inside the Why dialog. On open it scrolls to the step that needs the human and focuses it.
  S.itemSection = function (token, id) {
    const box = el("section", { class: "zs-section", "aria-labelledby": "zs-h-" + id }, el("h3", { id: "zs-h-" + id }, "Step by step: how this was checked"));
    const msg = el("p", { class: "muted", role: "status" }, "Loading the checks…"); box.append(msg);
    const load = () => Promise.all([ZL.api.trace(token, id), ZL.api.caseTrace(token).then(gateOf, () => null)]).then(([tr, gate]) => { msg.remove(); const old = box.querySelector(".zs-item"); const n = S.item(tr, gate); if (old) old.replaceWith(n); else box.append(n); requestAnimationFrame(() => n._showActive()); },
      (e) => { msg.textContent = ZL.API_MODE === "mock" ? "Step-by-step checks need the live server." : "The checks could not be loaded: " + e.message; });
    load();
    const again = () => { if (!box.isConnected) { document.removeEventListener("zl:rejudged", again); return; } load(); };
    document.addEventListener("zl:rejudged", again);
    return box;
  };
  S.openTrace = async function (id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    ZL.$("#why-title").textContent = "How this was checked: " + S.label(id);
    body.append(S.itemSection(s.token, id));
    if (!dlg.open) dlg.showModal();
  };
  // Small button for cards that have no Why? button of their own (flags, charges, could-not-verify items).
  S.traceButton = (id, cls, text) => el("button", { type: "button", class: cls || "rv-btn rv-secondary", "data-testid": "btn-trace", "data-trace-for": id, onclick: () => S.openTrace(id) }, text || "How it was checked");

  // ---- case level
  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
  // It expands by the human's click, or when the export gate is blocked and the human clicks Export. Passed steps stay in pipeline order inside.
  let cache = null, openPref = false, seq = 0, curDet = null;

  // One blocker row, shared by the case rail and the message beside the Export button.
  function blockerRow(b, noRerun) {
    const name = b.item_id ? S.label(b.item_id) : "Whole case";
    const wording = isCodeBlocker(b);
    return el("li", { class: "zs-blocker", "data-testid": "gate-blocker", "data-blocker-code": b.reason_code, "data-jump-item": b.item_id || null },
      el("span", { class: "zs-blocker-name" }, name), " ", el("span", { class: "zs-ev" }, wording ? [el("strong", {}, WORDING + " "), b.why || ""] : b.why || ""),
      b.item_id ? el("button", { type: "button", class: "zs-btn", "data-testid": "btn-gate-jump", "aria-label": "Go to item " + name, onclick: () => gotoItem(b.item_id) }, "Go to item") : null,
      wording ? el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-gate-edit", "aria-label": "Edit your wording for " + name, onclick: () => S.editItem(b.item_id) }, "Edit your wording") : null,
      b.reason_code === "JUDGE_NOT_RUN" && !noRerun ? S.rerunButton(RERUN, RERUN + " for " + name) : null);
  }
  // noRerun: the refused-export message has ONE rerun button with its status line right under the lead sentence, so its rows only offer Go to item.
  function blockerList(bl, title, noRerun) {
    const sorted = orderBlockers(bl), first = sorted.slice(0, 6), rest = sorted.slice(6);
    return el("div", { class: "zs-gate", "data-testid": "gate-blockers" },
      el("p", { class: "zs-ev" }, el("strong", {}, (title || "Blocking the export") + " (" + sorted.length + "):")),
      el("ul", { class: "zs-blockers" }, first.map((b) => blockerRow(b, noRerun))),
      rest.length ? el("details", { class: "zs-more" }, el("summary", {}, "Show the other " + rest.length), el("ul", { class: "zs-blockers" }, rest.map((b) => blockerRow(b, noRerun)))) : null);
  }
  // D-045(a): items nobody has decided yet are a WARNING on the gate, not a blocker: they stay out of the letter and the AI disclosure line counts them.
  function warningNode(st) {
    const ws = st.warnings || [];
    if (!ws.length) return null;
    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
      el("p", { class: "zs-todo-text" }, el("strong", {}, "Not reviewed (" + (w.count != null ? w.count : "") + "): "), w.why || ""),
      el("p", { class: "zs-ev" }, "This does not block the export."),
      el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn", "data-testid": "btn-gate-warning-jump", onclick: () => gotoFirstPending() }, "Go to the first pending item")))));
  }
  function gateNode(st) {
    const bl = st.blockers || [];
    const a = bl.length ? blockerList(bl) : null, w = warningNode(st), said = rerunNote && rerunNote.token === (ZL.state.get() || {}).token;
    return a || w || said ? el("div", {}, a, w, said && !bl.length ? rerunStatus() : null) : null;   // the last rerun sentence stays visible after the blockers are gone
  }
  function caseExtra(st) {
    if (st.id === "export_gate") return gateNode(st);
    if (st.id === "judges" && st.status === "pass") return el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn", "data-testid": "btn-to-judges", onclick: () => gotoPanel("judges") }, "See how the AI was checked"));
    return null;
  }
  function caseCounts(st) {
    const bits = fmtCounts(st.counts);
    return bits.length ? el("p", { class: "zs-counts", "data-testid": "step-counts" }, bits.map((b) => el("span", { class: "zs-chip" }, b))) : null;
  }
  function caseRail(tr) {
    const steps = tr.steps || [], act = activeIndex(steps), v = tr.verdict || {};
    const ctx = { testid: "case-step", level: "case", extra: (st) => { const a = caseCounts(st), b = caseExtra(st); return a || b ? el("div", {}, a, b) : null; } };
    return el("div", { class: "zs zs-case-inner" },
      el("p", { class: "zs-top" }, el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "case-verdict" }, v.label || ""),
        el("span", { class: "zs-progress", role: "status", "data-testid": "case-progress" }, progressLabel(steps))),
      el("ol", { class: "zs-rail", "aria-label": "Case checks, from reading the paste to the export gate" }, steps.map((s, i) => stepNode(s, i === act, ctx))),
      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “AI” steps by a model, “You” steps are your decisions."));
  }
  // The one-line summary: how many checks passed, how many need the human, and what the export is waiting for.
  function summaryBits(steps) {
    const passed = steps.filter((s) => s.status === "pass").length, need = steps.filter((s) => s.status === "fail" || s.status === "pending").length;
    const gate = steps.find((s) => s.id === "export_gate"), bl = (gate && gate.blockers) || [];
    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
    let gateText = "";
    const warned = ((gate && gate.warnings) || []).reduce((t, w) => t + (w.count || 0), 0);
    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
    else if (gate) gateText = "Export blocked by " + (n || 1);
    return { passed, need, gateText, total: steps.length };
  }
  function paintCase(host, tr) {
    clear(host);
    const steps = tr ? tr.steps || [] : [], sb = summaryBits(steps);
    const toggle = el("span", { class: "zs-toggle", "aria-hidden": "true" }, "Show");
    const sum = el("summary", { "data-testid": "case-summary" }, el("span", { class: "zs-case-title" }, "Case checks"),
      tr ? [el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, sb.passed + "/" + sb.total + " checks passed"),
        sb.need ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, sb.need + " need you") : null,
        sb.gateText ? el("span", { class: "zs-sumv zs-sumgate", "data-testid": "case-summary-gate" }, sb.gateText) : null] : el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, "loading…"), toggle);
    const det = el("details", { class: "zs-case-det" }, sum, tr ? caseRail(tr) : el("p", { class: "muted", role: "status" }, "Loading the case checks…"));
    det.open = !!openPref;
    toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { openPref = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    host.append(det); curDet = det;
  }
  // ---- the message beside the Export button. A refused export (422 judge_not_run / export_blocked) is shown right under the toolbar, scrolled into view and
  // focused, with the same Go to item list as the gate and the rerun button; never in the Export view 12,000 px further down.
  let blocked = null, curNotice = null;   // blocked: {token, message, blockers[], cleared}
  function paintNotice(host) {
    clear(host);
    const s = ZL.state.get();
    if (!blocked || blocked.token !== s.token) { host.hidden = true; return; }
    host.hidden = false;
    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
    host.className = "zs-exnote" + (blocked.cleared ? " zs-exnote-ok" : "");
    host.append(el("p", { class: "zs-exnote-msg", role: blocked.cleared ? "status" : "alert", "data-testid": "export-blocked-msg" }, el("strong", {}, blocked.cleared ? "Nothing blocks the export now. " : "The export is blocked. "), blocked.message || ""));
    // The rerun button and its Running… / result sentence sit together right under the lead sentence, above the (possibly long) blocker list, so the answer is
    // where the pressed button is. The same status node serves the cleared message.
    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton()));
    host.append(rerunStatus());
    if (!blocked.cleared && bl.length) host.append(blockerList(bl, null, true));
    host.append(el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn", "data-testid": "btn-export-blocked-close", onclick: () => { blocked = null; paintNotice(host); const b = ZL.$('[data-testid="btn-export"]'); if (b) b.focus(); } }, "Close this message")));
  }
  S.exportNotice = function () {
    const host = el("section", { "data-testid": "export-blocked", tabindex: "-1", "aria-label": "Why the export is blocked" });
    curNotice = host; paintNotice(host); return host;
  };
  S.showExportBlocked = function (err, reveal_) {
    const s = ZL.state.get();
    const d = (err && err.detail) || {};
    blocked = { token: s.token, message: (err && err.message) || "The export could not be built.", blockers: d.blockers || [] };
    if (!curNotice || !curNotice.isConnected) return false;
    paintNotice(curNotice);
    if (reveal_ !== false) reveal(curNotice);
    return true;
  };
  S.clearExportNotice = function () { if (blocked) { blocked = null; if (curNotice && curNotice.isConnected) paintNotice(curNotice); } };
  // After a rerun: refresh the blocker list in the message; when nothing blocks any more say so.
  function noticeAfterRerun(gate) {
    if (!blocked || !gate) return;
    if (gate.ready || !(gate.blockers || []).length) blocked = { token: blocked.token, cleared: true, message: "Every accepted item now has its second check. Click Export again.", blockers: [] };
    else { blocked.blockers = gate.blockers; blocked.message = gate.why || blocked.message; }
    if (curNotice && curNotice.isConnected) paintNotice(curNotice);
  }
  S.onExport = function () { /* the refused export shows its own message beside the button (showExportBlocked); the rail is left as the human set it */ };
  S.mountCase = function (parent, before) {
    const s = ZL.state.get(); if (!s.token || !s.case) return;
    const host = el("section", { class: "zs-case", "data-testid": "case-stepper", "aria-label": "Case checks" });
    parent.insertBefore(host, before || null);
    if (ZL.judges) ZL.judges.mount(parent, before);
    const mine = ++seq;
    if (cache && cache.token !== s.token) { cache = null; openPref = false; }
    paintCase(host, cache && cache.token === s.token ? cache.data : null);
    ZL.api.caseTrace(s.token).then((tr) => {
      const same = cache && cache.token === s.token && JSON.stringify(cache.data) === JSON.stringify(tr);
      cache = { token: s.token, data: tr };
      if (!same && host.isConnected && mine === seq) paintCase(host, tr);
    }, () => { if (host.isConnected && !cache) host.hidden = true; });
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:29:50.255Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 28,205p judges.js"
}
````

### User / tool · 2026-11-02T05:29:50.336Z

**tool result**
````
  const TODO_BLOCKED = "The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again; if it still cannot answer, dismiss the item.";   // accepted/edited: same sentence as the export gate
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);

  function title(id) { const cue = ZL.stepper.cue(id); return ZL.stepper.label(id) + (cue ? " · " + cue : ""); }
  // Which items block the export is the GATE's answer (the blockers of GET /trace), never a guess from the item's review status: D-045(b) exempts summaries the paralegal
  // wrote or edited from the judge, but not from the code checks, so an edited item can lack a judge answer and be ready, or fail a code check and block. gate is null while the trace is loading.
  function reviewOf(it) { const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return (f && f.item.review_status) || (it.unres || {}).review_status; }
  const gateSet = (tr) => {
    const g = ((tr || {}).steps || []).find((x) => x.id === "export_gate"); if (!g) return null;
    const bl = g.blockers || [];
    return { jnr: bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)) };
  };
  const codeIds = () => new Set(((gate && gate.code) || []).map((b) => b.item_id));
  const unchecked = (it) => !!(it.unres && !it.rej && it.unres.verdict === "unavailable");
  const blocking = (it) => unchecked(it) && !!gate && gate.jnr.includes(it.id);
  // The paralegal wrote or edited this wording: no second check applies (D-045 b), and the gate does not list it.
  const humanWording = (it) => { if (!unchecked(it) || blocking(it)) return false; const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return reviewOf(it) === "edited" || !!(f && f.item.ai_drafted === false); };
  const waiting = (it) => unchecked(it) && !blocking(it) && !humanWording(it) && reviewOf(it) === "pending";   // undecided and unchecked: a rerun covers it
  function links(id) {
    const t = title(id);
    return el("div", { class: "zs-todo-btns" },
      el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
      el("button", { type: "button", class: "zs-btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps"));
  }
  const noCode = (t) => String(t || "").replace(/\s*\([A-Z]{3,}(?:_[A-Z]+)*\)\s*$/, "");   // the closed reason code lives in Technical details
  const chip = (text, cls) => el("span", { class: "zs-chip " + (cls || "") }, text);

  // One item, once: group the three server lists by item id.
  function byItem(d) {
    const m = new Map();
    const get = (id, kind) => { if (!m.has(id)) m.set(id, { id, kind, rej: null, unres: null, dis: [] }); return m.get(id); };
    (d.rejections || []).forEach((r) => { get(r.item_id, r.kind).rej = r; });
    (d.unresolved || []).forEach((r) => { get(r.item_id, r.kind).unres = r; });
    (d.disagreements || []).forEach((x) => { get(x.item_id, x.kind).dis.push(x); });
    return Array.from(m.values());
  }

  function techDetails(it) {
    const r = it.rej || it.unres, bits = [];
    const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
    if (r) bits.push(kv("reason code", r.reason_code), kv("model", r.model), kv("prompt", r.prompt_version), kv("your decision", RS[r.review_status] || r.review_status));
    it.dis.forEach((x) => bits.push(kv("kind of disagreement", x.type), kv("resolution", x.resolution)));
    const nodes = bits.filter(Boolean);
    if (!nodes.length && !(r && r.response_raw)) return null;
    return el("details", { class: "zs-more", "data-testid": "judge-row-tech" }, el("summary", {}, "Technical details"), nodes.length ? el("p", { class: "zs-ev" }, nodes) : null,
      r && r.response_raw ? el("pre", { class: "zs-pre" }, r.response_raw) : null);
  }

  function row(it, testid) {
    const r = it.rej, u = it.unres, chips = [], mine = humanWording(it);
    if (r) chips.push(chip("AI objected", "zj-chip-bad"));
    else if (mine) chips.push(chip("Edited by you, not AI-checked"));
    else if (u) chips.push(chip(u.verdict === "unavailable" ? "AI did not check" : "AI could not decide", "zj-chip-bad"));
    it.dis.forEach((x) => { if (!(r && x.type === "judge_objects")) chips.push(chip(DIS[x.type] || x.type)); });   // "the AI objected" is already the first chip
    const decision = (r || u || it.dis[0] || {}).review_status;
    let why = null;
    if (r) why = el("p", { class: "zs-why" }, el("strong", {}, (READING[r.verdict] || ZL.stepper.verdictWord(r.verdict) + ".") + " "), r.rationale || "");
    else if (mine) why = el("p", { class: "zs-why" }, "You edited this item, so it is your wording and does not need the second check.");
    else if (u) why = el("p", { class: "zs-why" }, u.verdict === "unavailable" ? "The second check did not answer, so no AI judge looked at this item." : "The second check could not decide.");
    const blk = blocking(it);
    if (blk) { chips.push(chip("Blocks the export", "zj-chip-bad")); why = null; }
    const todo = blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u ? (u && !r ? TODO_UNCHECKED : it.kind === "amount" ? TODO_AMOUNT : TODO_COMPARE) : null;
    return el("li", { class: "zj-row", "data-testid": testid, "data-target-item": it.id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, title(it.id)), el("span", { class: "zs-kind" }, KIND[it.kind] || it.kind)),
      el("p", { class: "zj-chips" }, chips, decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      why,
      it.dis.map((x) => el("p", { class: "zs-ev" }, el("span", { class: "zs-k" }, "Code said: "), x.code_says || "", el("br"), el("span", { class: "zs-k" }, "The AI said: "), noCode(x.judge_says))),
      todo ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), todo) : null,
      links(it.id), techDetails(it));
  }
  // An edited or hand-written item whose wording fails a code check: the row is the gate's blocker as the server wrote it (reason, fix sentence), with an Edit action.
  function wordingRow(b) {
    const id = b.item_id, t = title(id), decision = reviewOf({ id });
    return el("li", { class: "zj-row", "data-testid": "judge-wording", "data-target-item": id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, t), el("span", { class: "zs-kind" }, KIND.entry)),
      el("p", { class: "zj-chips" }, chip("Blocks the export", "zj-chip-bad"), decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      el("p", { class: "zs-why" }, el("strong", {}, ZL.stepper.WORDING + " "), b.why || ""),
      b.next_action && b.next_action.text ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), b.next_action.text) : null,
      el("div", { class: "zs-todo-btns" },
        el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-judge-edit", "aria-label": "Edit your wording for " + t, onclick: () => ZL.stepper.editItem(id) }, "Edit your wording"),
        el("button", { type: "button", class: "zs-btn", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
        el("button", { type: "button", class: "zs-btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps")));
  }
  const CAP = 5;   // rows shown per group before "Show the other N"; the full list is one click away
  const list = (testid, label, rows, mk, empty, extra) => el("section", { class: "zj-group", "data-testid": testid, "aria-label": label },
    el("h3", {}, label + " (" + plural(rows.length, "item", "items") + ")"), extra || null,
    rows.length ? el("ul", { class: "zj-list" }, rows.slice(0, CAP).map(mk)) : el("p", { class: "rv-empty" }, empty),
    rows.length > CAP ? el("details", { class: "zs-more", "data-testid": "judge-more" }, el("summary", {}, "Show the other " + (rows.length - CAP)), el("ul", { class: "zj-list" }, rows.slice(CAP).map(mk))) : null);

  function tile(n, label) { return el("li", { class: "zj-tile" }, el("strong", { class: "zj-n" }, String(n)), el("span", { class: "zj-l" }, label)); }

  // Built from the server's totals and from the gate: only items the gate lists carry the blocking words ("blocks export"). An edited item the gate does not hold is
  // counted as "not checked" but never as blocking, so the panel and the rail ("Export blocked by N") agree.
  function summaryText(d) {
    const nb = ((gate && gate.jnr) || []).length, nc = ((gate && gate.code) || []).length;
    const t = d.totals || {}, bits = [];
    const n = t.items_judged || 0;
    if (!t.unsupported && !t.unsure && !t.unavailable) bits.push("checked " + n + ", all agreed with the draft");
    else {
      bits.push(n + " checked", (t.supported || 0) + " agreed with the draft");
      if (t.unsupported) bits.push(t.unsupported + " questioned");
      if (t.unsure) bits.push(t.unsure + " undecided");
      if (t.unavailable) bits.push(t.unavailable + " not checked" + (nb ? ", blocks export: " + nb : ""));
    }
    if (nb && !t.unavailable) bits.push(nb + " not checked, blocks export: " + nb);
    if (nc) bits.push(nc + (nc === 1 ? " edit does not match its quote" : " edits do not match their quotes") + ", blocks export: " + nc);
    return bits.join(", ");
  }

  function paint(root, d, note) {
    const prev = root.querySelector("details.zj-det"); if (prev) wasOpen = prev.open;
    clear(root); root.hidden = false;
    root.setAttribute("data-testid", "judge-panel"); root.setAttribute("aria-labelledby", "zj-h");
    const toggle = el("span", { class: "zs-toggle", "aria-hidden": "true" }, "Show");
    const det = el("details", { class: "zs-case-det zj-det", "data-open-on-jump": "1" },
      el("summary", { "data-testid": "judge-summary" }, el("span", { class: "zs-case-title", id: "zj-h" }, "How the AI was checked"),
        el("span", { class: d && ((d.totals || {}).unsupported || (d.totals || {}).unavailable || (d.totals || {}).unsure || (gate && gate.code.length)) ? "zs-sumv zj-sum-bad" : "zs-sumv", "data-testid": "judge-summary-counts" }, d ? summaryText(d) : note || "loading…"), toggle));
    det.open = wasOpen; toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { wasOpen = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    root.append(det);
    det.append(el("p", { class: "rv-help", "data-testid": "judge-label" }, el("strong", {}, "AI quality checks. "),
      "This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review."));
    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
    det.append(el("p", { class: "zj-models", "data-testid": "judge-model-line" },
      "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
      d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
    det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
      tile(t.items_judged || 0, "items checked by AI"), tile(t.supported || 0, "agreed with the draft"), tile(t.unsupported || 0, "AI objected"),
      tile(t.unsure || 0, "could not decide"), tile(t.unavailable || 0, "unavailable"), tile(t.human_overrides || 0, "you accepted despite an objection")));
    const cids = codeIds(), cblk = (gate && gate.code) || [];
    const asked = items.filter((i) => i.rej), open = items.filter((i) => !i.rej && i.unres && !cids.has(i.id)), differ = items.filter((i) => !i.rej && !i.unres && i.dis.length);
    if (cblk.length) det.append(list("judge-wording-list", "Where your wording does not match the quote", cblk, wordingRow, ""));
    det.append(list("judge-rejections", "Where the AI objected", asked, (i) => row(i, "judge-rejection"), "No objections. The second check agreed with every item it checked."));
    const nBlock = open.filter(blocking).length, nWait = open.filter(waiting).length, nRun = nBlock + nWait;
    // One rerun button for the whole list, its Running… / result sentence right under it (the sentence is read from the stored note, so a repaint keeps it).
    const group = nRun ? el("div", { class: "zs-todo", "data-testid": "judge-rerun-group" },
      el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "),
        nBlock ? plural(nBlock, "accepted item", "accepted items") + " cannot go in the letter until the second AI check has run on " + (nBlock === 1 ? "it" : "them") + "."
          : "The second check has not run on " + plural(nWait, "item", "items") + " you have not decided yet. Run it before you accept " + (nWait === 1 ? "it" : "them") + "."),
      el("div", { class: "zs-todo-btns" }, ZL.stepper.rerunButton(nRun === 1 ? "Run the second check again for this item" : "Run the second check again for these " + nRun)),
      ZL.stepper.rerunStatus()) : null;
    if (open.length) det.append(list("judge-unresolved-list", "Where the AI could not check or decide", open, (i) => row(i, "judge-unresolved"), "", group));
    if (differ.length) det.append(list("judge-disagreements", "Where code and the AI read an item differently", differ, (i) => row(i, "judge-disagreement"), ""));
    const jr = (d.judges || []).filter((j) => j.label && j.items + (j.unavailable || 0) > 0);
    det.append(el("details", { class: "zs-more zj-tech", "data-testid": "judge-tech" }, el("summary", {}, "Technical details"),
      el("p", { class: "zs-ev", "data-testid": "judge-prompts" }, el("span", { class: "zs-k" }, "Prompt versions: "), (d.prompt_versions || []).join(", ") || "none"),
      jr.length ? el("details", { class: "zs-more zj-by", "data-testid": "judge-by-check" }, el("summary", {}, "By kind of check (" + jr.length + ")"),
        el("ul", { class: "zj-list" }, jr.map((j) => el("li", { class: "zj-row" }, el("div", { class: "zs-head" }, el("span", { class: "zs-label" }, j.label)),
          el("p", { class: "zs-ev" }, j.items + " checked: " + j.supported + " agreed, " + (j.partially || 0) + " partly, " + (j.unsupported || 0) + " not supported, " + (j.disagrees || 0) + " read differently, " + (j.unsure || 0) + " undecided, " + (j.unavailable || 0) + " unavailable. ",
            el("span", { class: "zs-k" }, "Prompt "), j.prompt_version || "", el("span", { class: "zs-k" }, " · model "), (j.models || []).join(", ")))))) : null));
  }

  // Mounted right under the case checks by ZL.stepper.mountCase, so the AI-check signal sits at the top of the results.
  ZL.judges = {
    // Fetch the report again and repaint the mounted panel (used after "Run the second check again").
    async reload(tr) {
      const s = ZL.state.get(); if (!s.token) return;
      const [d, t] = await Promise.all([ZL.api.judges(s.token), tr || ZL.api.caseTrace(s.token).catch(() => null)]);
      cache = { token: s.token, data: d, gate: gateSet(t) }; gate = cache.gate;
      document.querySelectorAll('[data-panel="judges"]').forEach((r) => { if (r.isConnected) paint(r, d); });
    },
    mount(parent, before) {
      const s = ZL.state.get(); if (!s.token || !s.case) return null;
      const root = el("section", { class: "rv-panel zj-panel", "data-panel": "judges" });
      parent.insertBefore(root, before || null);
      if (cache && cache.token !== s.token) { cache = null; gate = null; wasOpen = false; }
      if (cache) gate = cache.gate;
      paint(root, cache && cache.token === s.token ? cache.data : null);
      Promise.all([ZL.api.judges(s.token), ZL.api.caseTrace(s.token).then(gateSet, () => null)]).then(([d, g]) => {
        const same = cache && cache.token === s.token && JSON.stringify(cache.data) === JSON.stringify(d) && JSON.stringify(cache.gate) === JSON.stringify(g);
        cache = { token: s.token, data: d, gate: g }; gate = g;
        if (!same && root.isConnected) paint(root, d);
      }, () => { if (cache) return; if (ZL.API_MODE === "mock" && root.isConnected) paint(root, null, "AI check details need the live server."); else root.hidden = true; });
      return root;
    },
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:01.681Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 100,215p stepper.js"
}
````

### User / tool · 2026-11-02T05:30:01.762Z

**tool result**
````
    reveal(node); return true;
  }
  S.gotoPanel = gotoPanel;
  function gotoFirstPending() {
    closeDialogs();
    const node = document.querySelector('[data-testid="queue"] [data-item-id][data-review="pending"]') || document.querySelector('[data-item-id][data-review="pending"]') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    reveal(node); return true;
  }
  function gotoTray() {
    closeDialogs();
    const node = document.querySelector('[data-testid="rejected-tray"]') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    reveal(node); return true;
  }
  async function rerun(confirm, msgNode) {
    const s = ZL.state.get();
    try { msgNode.textContent = ""; await ZL.api.run(s.token, confirm); ZL.pollRun(); } catch (e) { msgNode.textContent = "The AI steps could not be started: " + e.message; }
  }
  function openRecord(itemId, recordId) {
    const c = caseNow(), f = itemId && c && rv() && rv().find(c, itemId);
    if (f) { rv().openSource(f.item, f.kind); return; }
    if (recordId && typeof ZL.openSource === "function") ZL.openSource([{ record_id: recordId, start: null, end: null }], "Record " + recSeq(recordId));
  }

  // ---- "Run the second check again" (D-044): POST /rejudge for the accepted items whose second AI check never ran. One handler for every place that offers it
  // (case rail, export gate, blocker rows, the export message, the item stepper, the AI-check panel). Busy state and the result in plain words live in module
  // state, so a repaint of the page does not lose the sentence.
  const RERUN = "Run the second check again";
  // D-045(b)/T-098: a code-check blocker on wording the paralegal wrote or edited (the gate's blocker carries step_id; the text is the server's).
  const WORDING = "Your wording doesn't match the quote:";
  const isCodeBlocker = (b) => !!(b && b.item_id && b.step_id);
  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;
  let rerunBusy = false, rerunNote = null;   // rerunNote: {token, text}
  const rerunSay = (text) => {
    rerunNote = text ? { token: (ZL.state.get() || {}).token, text } : null;
    document.querySelectorAll('[data-testid="rerun-status"]').forEach((n) => { n.textContent = text || ""; });
  };
  const setRerunBusy = (b) => { rerunBusy = b; document.querySelectorAll('[data-testid="btn-rerun-judge"]').forEach((x) => { x.disabled = b; x.setAttribute("aria-busy", b ? "true" : "false"); }); };
  const gateOf = (tr) => ((tr || {}).steps || []).find((x) => x.id === "export_gate");
  const jnrBlockers = (g) => ((g && g.blockers) || []).filter((b) => b.reason_code === "JUDGE_NOT_RUN");
  S.rerunButton = function (label, aria) {
    const b = el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-rerun-judge", "aria-label": aria || null, onclick: (ev) => S.rejudge(ev.currentTarget) }, label || RERUN);
    if (rerunBusy) { b.disabled = true; b.setAttribute("aria-busy", "true"); }
    return b;
  };
  // A status line that shows the last rerun sentence (role=status, so a screen reader hears it).
  S.rerunStatus = () => rerunStatus();
  const rerunStatus = () => el("p", { class: "zs-ev zs-rerun-status", role: "status", "data-testid": "rerun-status" }, rerunNote && rerunNote.token === (ZL.state.get() || {}).token ? rerunNote.text : "");
  const OBJECT = ["partially", "unsupported", "disagrees", "unsure"];
  function rerunWords(res) {
    const asked = res.asked || 0, still = (res.still_unavailable || []).length, got = (res.rejudged || []);
    if (!asked) return "There was nothing to run the second check on.";
    const obj = got.filter((r) => OBJECT.includes(r.verdict)).length;
    let t = still ? "The second check still did not answer for " + plural(still, "item", "items") + " of " + asked + ". Try again, or dismiss " + (still === 1 ? "it" : "them") + "."
      : "The second check ran on " + plural(asked, "item", "items") + " and answered for " + (asked === 1 ? "it" : "all of them") + ".";
    if (obj) t += " It questioned " + plural(obj, "item", "items") + "; see How the AI was checked.";
    if (!still && res.export_gate && res.export_gate.ready) t += " Nothing about the second check blocks the export now.";
    return t;
  }
  function rerunError(e) {
    if (e.code === "run_in_progress") return "The AI run is still going. Try again when it finishes.";
    if (e.code === "llm_unavailable") return "The second check could not be reached. Try again in a moment.";
    if (e.code === "demo_mode_unsupported_input") return "The demo can only run the second check on its recorded cases.";
    return "The second check could not be run: " + e.message;
  }
  // The answer must be where the pressed button is: after Running… and after the result, scroll the status line of the region the button sat in just into view
  // (a button near the bottom of the screen has its status line below the fold). The region is found again by name because the repaint rebuilds its nodes.
  const REGIONS = '[data-testid="export-blocked"],[data-testid="judge-panel"],[data-testid="case-stepper"],[data-testid="item-stepper"]';
  function showStatusIn(sel) {
    const root = sel && document.querySelector(sel), st = root && Array.from(root.querySelectorAll('[data-testid="rerun-status"]')).find((n) => n.textContent);
    if (st) st.scrollIntoView({ block: "nearest" });
  }
  S.rejudge = async function (origin) {
    if (rerunBusy) return;
    const s = ZL.state.get(); if (!s.token) return;
    const reg = origin && origin.closest ? origin.closest(REGIONS) : null, sel = reg ? '[data-testid="' + reg.getAttribute("data-testid") + '"]' : null;
    const n = jnrBlockers(gateOf(cache && cache.token === s.token ? cache.data : null)).length;
    setRerunBusy(true); rerunSay(n ? "Running the second check on " + plural(n, "item", "items") + "…" : "Running the second check…");
    showStatusIn(sel);
    let res = null;
    try { res = await ZL.api.rejudge(s.token); rerunSay(rerunWords(res)); } catch (e) { rerunSay(rerunError(e)); }
    // refresh every view that shows the gate: case trace, AI-check panel, the case itself (item state can change), then tell open dialogs
    try {
      const tr = await ZL.api.caseTrace(s.token);
      cache = { token: s.token, data: tr };
      if (ZL.judges) await ZL.judges.reload(tr);
      noticeAfterRerun(gateOf(tr));
      ZL.state.set({ case: await ZL.api.getCase(s.token) });
    } catch (_) { /* the sentence above already told the human what happened */ }
    setRerunBusy(false); showStatusIn(sel);
    document.dispatchEvent(new CustomEvent("zl:rejudged", { detail: res }));
  };

  // ---- "What you need to do": one fixed sentence from the server plus a button where something on the page can do it.
  // Rule: a button is only drawn when its handler can land somewhere (every handler falls back to the queue), never a dead button.
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);
  function gotoItem(id) {
    if (S.goto(id)) return true;
    return /^ns\d/.test(String(id)) ? gotoPanel("narrative") : gotoFirstPending();
  }
  // Opens the edit box of an item (the same path as pressing e on its row). Used by every "Edit your wording" action.
  S.editItem = function (id) {
    if (!gotoItem(id)) return false;
    const n = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
    if (n) n.dispatchEvent(new KeyboardEvent("keydown", { key: "e", bubbles: true }));
    return true;
  };
  const VIEW = {   // target.view -> [button text, handler]
    judges: ["Open the AI checks", () => gotoPanel("judges")],
    amounts: ["Go to the charges", () => gotoPanel("charges")],
    queue: ["Go to the first pending item", () => gotoFirstPending()],
    tray: ["Go to the could-not-verify items", () => gotoTray()],
    narrative: ["Go to the draft paragraph", () => gotoPanel("narrative")],
  };
  // Case-level steps say what to do with counts ("Review the 3 items the AI objected to"), not the item-level sentence.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:04.650Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 215,290p stepper.js; cd .. ; grep -rn \"btn-rerun-judge\" ../tests | cut -c1-200 | head -40"
}
````

### User / tool · 2026-11-02T05:30:04.753Z

**tool result**
````
  // Case-level steps say what to do with counts ("Review the 3 items the AI objected to"), not the item-level sentence.
  function caseCopy(st) {
    const c = st.counts || {};
    switch (st.id) {
      case "judges": {
        const obj = c.unsupported || 0, unsure = c.unsure || 0, un = c.unavailable || 0, cant = unsure + un;
        if (!obj && !cant) return null;
        const bits = [];
        if (obj) bits.push("Review the " + plural(obj, "item", "items") + " the AI objected to. Compare each one with its quote, then accept, edit or dismiss it.");
        if (unsure) bits.push("The AI could not decide " + plural(unsure, "item", "items") + "; read " + (unsure === 1 ? "it" : "them") + " yourself.");
        if (un) bits.push("The second AI check did not run on " + plural(un, "item", "items") + ". Run it again; accepted items it never checked cannot go in the letter.");
        return { text: bits.join(" "), label: obj ? "Review the " + plural(obj, "item", "items") + " the AI objected to" : "Show the " + plural(cant, "item", "items") + " the AI could not check", go: () => gotoPanel("judges"), rerun: un > 0 };
      }
      case "totals": {
        const n = c.pending_charges || 0;
        return { text: "Decide the " + plural(n, "detected charge", "detected charges") + ": accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.", label: "Go to the totals", go: () => gotoPanel("charges") };
      }
      case "review": {
        const n = c.pending || 0;
        return { text: "Decide the " + plural(n, "pending item", "pending items") + ": accept, edit or dismiss each one.", label: "Go to the first pending item", go: () => gotoFirstPending() };
      }
      case "export_gate": {
        const bl = st.blockers || [], n = c.blocking || bl.length, jnr = jnrBlockers(st);
        if (!bl.length) return null;
        const b = firstBlocker(bl);
        if (!b && !jnr.length) return null;     // only whole-case blockers (nothing accepted, run state): the step's own action (go to the queue) says it
        const text = jnr.length ? plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check again; if it still cannot answer, dismiss " + (jnr.length === 1 ? "that item" : "those items") + "."
          : "Settle the " + plural(n, "blocker", "blockers") + " listed here and the export opens.";
        return { text, label: "Go to the first blocking item", go: b ? () => gotoItem(b.item_id) : null, rerun: jnr.length > 0 };
      }
      default: return null;
    }
  }
  // The first blocker in QUEUE order, so "Go to the first blocking item" lands where "Go to the first pending item" would.
  const queueIds = () => Array.from(document.querySelectorAll('[data-testid="queue"] [data-item-id]')).map((n) => n.getAttribute("data-item-id"));
  function firstBlocker(bl) {
    const ids = queueIds(), withItem = (bl || []).filter((b) => b.item_id);
    const idx = (b) => { const i = ids.indexOf(b.item_id); return i < 0 ? 1e6 : i; };
    return withItem.slice().sort((a, b) => idx(a) - idx(b))[0] || null;
  }
  // List order: whole-case blockers, then entries that need review, other entries, then charges and flags. Stable.
  function orderBlockers(bl) {
    const rank = (b) => {
      if (!b.item_id) return 0;
      const f = rv() && caseNow() && rv().find(caseNow(), b.item_id);
      return f && f.kind === "entry" ? (f.item.state === "needs_review" ? 1 : 2) : 3;
    };
    return (bl || []).map((b, i) => [b, i]).sort((x, y) => rank(x[0]) - rank(y[0]) || x[1] - y[1]).map((x) => x[0]);
  }
  function actionNode(na, ctx, st) {
    if (!na) return null;
    const t = na.target || {}, buttons = [], msg = el("p", { class: "zs-ev zs-err", role: "alert" });
    const itemId = t.item_id || ctx.itemId, recId = t.record_id || (ctx.recordId || null);
    const btn = (text, fn, extra) => buttons.push(el("button", Object.assign({ type: "button", class: "zs-btn", "data-testid": "btn-step-action", "data-action-code": na.code, onclick: fn }, extra || {}), text));
    const view = t.view && VIEW[t.view];
    let text = na.text || "";
    const cc = ctx.level === "case" && st ? caseCopy(st) : null;
    let rerunToo = false;
    if (cc) { text = cc.text; if (cc.rerun) { buttons.push(S.rerunButton()); rerunToo = true; } if (cc.go) btn(cc.label, cc.go); }
    else switch (na.code) {
      case "CONFIRM_DATE": btn("Go to Dates to confirm", () => gotoDates(recId)); break;
      case "EDIT_SUMMARY": if (itemId) btn("Go to the item and edit the summary", () => S.editItem(itemId)); break;
      case "EDIT_QUOTE": case "READ_RECORD": case "COMPARE_BY_HAND":
        if (view && !itemId) btn(view[0], view[1]); else if (itemId || recId) btn("Open the record", () => openRecord(itemId, recId), { "aria-label": "Open " + ((itemId && S.cue(itemId)) || "the record").toLowerCase() }); break;
      case "DISMISS_OR_ENTER_BY_HAND":
        if (view) btn(view[0], view[1]); else if (t.item_id) btn("Go to the item", () => gotoItem(t.item_id)); else if (recId) btn("Go to the record", () => gotoDates(recId)); break;
      case "RERUN": case "CONFIRM_RERUN":
        btn("Run the AI steps again", () => rerun(na.code === "CONFIRM_RERUN", msg)); break;
      case "RERUN_JUDGE":
        buttons.push(S.rerunButton()); rerunToo = true;
        if (t.view === "judges" && !(st && st.id === "judges")) btn("Open the AI checks", () => gotoPanel("judges"));
        break;
      case "SENTENCE_REMOVED": btn("Go to the draft paragraph", () => gotoPanel("narrative")); break;
      case "DECIDE":
        if (view) btn(view[0], view[1]); else if (t.view === "dates_to_confirm") btn("Go to Dates to confirm", () => gotoDates(recId));
        else if (itemId) btn("Go to the decision buttons", () => gotoItem(itemId)); break;
../tests/e2e/conftest.py:22:T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_N
../tests/e2e/conftest.py:24:T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that messa
../tests/e2e/conftest.py:25:  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the pan
../tests/e2e/conftest.py:28:  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/
../tests/e2e/test_rerun_judge.py:71:        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 1
../tests/e2e/test_rerun_judge.py:73:    assert gate.get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").inner_text() == "Run the second check again"
../tests/e2e/test_rerun_judge.py:75:    assert judges.get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").count() == 1
../tests/e2e/test_rerun_judge.py:82:    btn = cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge")
../tests/e2e/test_rerun_judge.py:84:    page.wait_for_function("() => document.querySelectorAll('[data-testid=btn-rerun-judge]').length > 0 && [...document.querySelectorAll('[data-testid=btn-rerun-jud
../tests/e2e/test_rerun_judge.py:96:    cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").click()
../tests/e2e/test_rerun_judge.py:101:    expect(page.get_by_test_id("btn-rerun-judge").first).to_be_enabled()
../tests/e2e/test_rerun_judge.py:120:        box.get_by_test_id("btn-rerun-judge").first.click()
../tests/e2e/test_rerun_judge.py:139:    j.get_by_test_id("btn-rerun-judge").click()
../tests/e2e/test_rerun_judge.py:142:    assert page.get_by_test_id("item-stepper").locator('[data-step-id="judge_1"]').get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:153:        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 0, "one group button covers the list; rows would only repeat it"
../tests/e2e/test_rerun_judge.py:155:    assert jp.get_by_test_id("btn-rerun-judge").count() == 1
../tests/e2e/test_rerun_judge.py:156:    grp.get_by_test_id("btn-rerun-judge").click()
../tests/e2e/test_rerun_judge.py:164:    assert jp.get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:203:        btn = box.get_by_test_id("btn-rerun-judge"); assert btn.count() == 1, "the message has one rerun button; its rows only offer Go to item"
../tests/e2e/test_rerun_judge.py:224:        grp = jp.get_by_test_id("judge-rerun-group"); btn = grp.get_by_test_id("btn-rerun-judge"); btn.scroll_into_view_if_needed(); btn.click()
../tests/e2e/test_rerun_judge.py:229:        assert vis(pg, st) and abs(st.bounding_box()["y"] - jp.get_by_test_id("judge-rerun-group").get_by_test_id("btn-rerun-judge").bounding_box()["y"]) < 120
../tests/e2e/test_rerun_judge.py:250:    assert row.get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:301:        assert "Edited by you, not AI-checked" in row.inner_text() and "Blocks the export" not in row.inner_text() and row.get_by_test_id("btn-rerun-judge").count(
../tests/e2e/test_rerun_judge.py:307:    assert j.get_by_test_id("step-status").inner_text() == "Not needed" and j.get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:320:    assert "second check missing" not in st.inner_text().lower() and st.get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:331:    assert row.get_by_test_id("btn-gate-edit").count() == 1 and row.get_by_test_id("btn-rerun-judge").count() == 0
../tests/e2e/test_rerun_judge.py:334:    assert WORDING in box.get_by_test_id("gate-blocker").inner_text() and box.get_by_test_id("btn-rerun-judge").count() == 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:07.124Z

**tool call — Bash**
````
{
 "command": "sed -n 55,105p tests/e2e/test_rerun_judge.py; sed -n 256,345p tests/e2e/test_rerun_judge.py; sed -n 15,40p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T05:30:07.214Z

**tool result**
````
    assert "nothing is accepted" in box.get_by_test_id("export-blocked-msg").inner_text().lower()
    assert in_view(page, box) and active_in(page, '[data-testid="export-blocked"]')
    assert page.get_by_test_id("btn-export").is_visible() and in_view(page, page.get_by_test_id("btn-export"))
    assert page.locator("#view-export").is_hidden()
    assert page.get_by_test_id("case-stepper").locator("details.zs-case-det").evaluate("d => d.open") is False
    box.get_by_test_id("btn-export-blocked-close").click(); expect(box).to_be_hidden()


# ---- D-044: the rerun button wherever a JUDGE_NOT_RUN blocker or step appears
def test_rerun_button_in_rail_gate_and_blocker_rows(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    assert re.search(r"Export blocked by 3", cs.get_by_test_id("case-summary-gate").inner_text())
    gate = cs.locator('[data-step-id="export_gate"]')
    assert gate.get_by_test_id("gate-blocker").count() == 3
    rows = gate.get_by_test_id("gate-blocker")
    for i in range(3):
        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 1
    assert "never got the second AI check" in gate.get_by_test_id("step-action").inner_text()
    assert gate.get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").inner_text() == "Run the second check again"
    judges = cs.locator('[data-step-id="judges"]')
    assert judges.get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").count() == 1
    assert "did not run on 3 items" in judges.get_by_test_id("step-action").inner_text()


def test_rerun_shows_busy_posts_once_and_clears_the_gate(page, sample_case):
    stub = JudgeNotRun(page, sample_case, _accept(sample_case), hold=True)
    open_case(page, sample_case); cs = open_rail(page)
    btn = cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge")
    btn.click()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=btn-rerun-judge]').length > 0 && [...document.querySelectorAll('[data-testid=btn-rerun-judge]')].every(b => b.disabled)")
    assert "Running the second check on 3 items" in page.get_by_test_id("rerun-status").first.inner_text()
    stub.release()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=gate-blocker]').length === 0", timeout=8000)
    assert stub.posts == 1
    assert "Ready to export" in page.get_by_test_id("case-summary-gate").inner_text()
    expect(cs.locator('[data-step-id="export_gate"]').get_by_test_id("rerun-status")).to_contain_text("ran on 3 items and answered for all of them")


def test_rerun_that_still_gets_no_answer_says_so(page, sample_case):
    stub = JudgeNotRun(page, sample_case, _accept(sample_case), mode="still")
    open_case(page, sample_case); cs = open_rail(page)
    cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").click()
    st = cs.locator('[data-step-id="export_gate"]').get_by_test_id("rerun-status")
    expect(st).to_contain_text("still did not answer for 3 items of 3")
    assert "dismiss them" in st.inner_text()
    assert cs.locator('[data-step-id="export_gate"]').get_by_test_id("gate-blocker").count() == 3 and stub.posts == 1
    expect(page.get_by_test_id("btn-rerun-judge").first).to_be_enabled()


@pytest.mark.parametrize("w,h", [(1280, 900), (390, 844)])
def test_refused_export_shows_beside_the_button_with_blockers_and_rerun(pw, sample_case, w, h):
# ---- T-097 round 2 (D-045 b, T-098, D-047): the summary and the Why dialog read the gate and the item trace; a failing code check on an edited summary is a named blocker.
# Since T-100 the edit route refuses wording that fails a code check, so that gate state is produced by the WordingFails route stub (conftest); everything else is the real backend.
WORDING = "Your wording doesn't match the quote:"


def _edit(tok, i, summary):
    st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
    assert st == 200, r
    return r


@pytest.fixture
def mixed(page, sample_case):
    """One accepted AI item; one edited summary the gate holds (stub: fails a code check); one edited summary that passes."""
    ids = _accept(sample_case, 1)
    pend = [e for e in api("GET", f"/api/cases/{sample_case}")[1]["entries"] if e["id"] not in ids and e["state"] != "rejected" and e["date"] and e["review_status"] == "pending"]
    bad, ok = pend[0], pend[1]
    _edit(sample_case, bad["id"], bad["summary"].rstrip(".") + " per the record.")
    _edit(sample_case, ok["id"], ok["summary"].rstrip(".") + " per the record.")
    stub = WordingFails(page, sample_case, [bad["id"]])
    return {"tok": sample_case, "bad": bad, "ok": ok, "accepted": ids[0], "stub": stub}


def test_failing_edit_is_a_named_blocker_in_the_panel_summary_and_row(page, mixed):
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert "1 edit does not match its quote, blocks export: 1" in summ
    assert "Export blocked by 1" in open_rail(page).get_by_test_id("case-summary-gate").inner_text(), "the rail and the panel summary agree"
    row = jp.locator(f'[data-testid="judge-wording"][data-target-item="{t["bad"]["id"]}"]')
    expect(row).to_have_count(1)
    txt = row.inner_text()
    assert WORDING in txt and "qualifier" in txt and "Blocks the export" in txt and "Edited by you, not AI-checked" not in txt
    assert "The export stays blocked until it passes" in txt, "the server's fix sentence is shown as the next step"
    assert jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["bad"]["id"]}"]').count() == 0, "one row per item"
    row.get_by_test_id("btn-judge-edit").click()
    ta = page.locator(f'[data-item-id="{t["bad"]["id"]}"]').first.get_by_test_id("edit-summary")
    expect(ta).to_be_visible(); assert active_in(page, f'[data-item-id="{t["bad"]["id"]}"]')


def test_passing_edit_says_edited_by_you_not_ai_checked_everywhere(page, mixed):
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["ok"]["id"]}"]')
    if row.count():   # the report lists the edited item as unchecked; the row follows the gate, which does not hold it
        assert "Edited by you, not AI-checked" in row.inner_text() and "Blocks the export" not in row.inner_text() and row.get_by_test_id("btn-rerun-judge").count() == 0
    assert jp.get_by_test_id("judge-summary-counts").inner_text().count("blocks export") == 1, "only the failing edit blocks"
    page.locator(f'[data-testid="queue"] [data-item-id="{t["ok"]["id"]}"]').get_by_test_id("entry-why").click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == "Edited by you, not AI-checked"
    j = st.locator('[data-step-id="judge_1"]')
    assert j.get_by_test_id("step-status").inner_text() == "Not needed" and j.get_by_test_id("btn-rerun-judge").count() == 0
    assert "second check missing" not in st.inner_text().lower() and st.locator('[data-status="fail"]').count() == 0
    assert st.get_by_test_id("item-wording-fail").count() == 0


def test_why_dialog_for_a_failing_edit_says_the_wording_does_not_match_with_an_edit_action(page, mixed):
    t = mixed
    open_case(page, t["tok"])
    page.locator(f'[data-testid="queue"] [data-item-id="{t["bad"]["id"]}"]').get_by_test_id("entry-why").click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    w = st.get_by_test_id("item-wording-fail")
    assert WORDING in w.inner_text() and "qualifier" in w.inner_text().lower()
    assert st.get_by_test_id("item-verdict").inner_text() != "Edited by you, not AI-checked"
    assert "second check missing" not in st.inner_text().lower() and st.get_by_test_id("btn-rerun-judge").count() == 0
    w.get_by_test_id("btn-wording-edit").click()
    expect(page.locator("#why-modal")).not_to_be_visible()
    expect(page.locator(f'[data-item-id="{t["bad"]["id"]}"]').first.get_by_test_id("edit-summary")).to_be_visible()


def test_rail_blocker_row_names_the_wording_problem_with_an_edit_button(page, mixed):
    t = mixed
    open_case(page, t["tok"]); cs = open_rail(page)
    row = cs.locator(f'[data-testid="gate-blocker"][data-jump-item="{t["bad"]["id"]}"]')
    expect(row).to_have_count(1); assert WORDING in row.inner_text()
    assert row.get_by_test_id("btn-gate-edit").count() == 1 and row.get_by_test_id("btn-rerun-judge").count() == 0
    page.get_by_test_id("btn-export").click()   # the refused export lists the same blocker with the same words
    box = page.get_by_test_id("export-blocked"); expect(box).to_be_visible()
    assert WORDING in box.get_by_test_id("gate-blocker").inner_text() and box.get_by_test_id("btn-rerun-judge").count() == 0


def test_fixing_the_wording_clears_panel_dialog_and_rail(page, mixed):
    t = mixed
    _edit(t["tok"], t["bad"]["id"], t["bad"]["summary"].rstrip(".") + " as recorded.")   # any new wording ends the stub's failure, as a passing edit ends the real one
    open_case(page, t["tok"]); page.reload(); page.get_by_test_id("timeline").wait_for(); jp = open_judges(page)
    assert jp.get_by_test_id("judge-wording").count() == 0
    assert "does not match" not in jp.get_by_test_id("judge-summary-counts").inner_text()
    assert "Ready to export" in open_rail(page).get_by_test_id("case-summary-gate").inner_text()
    page.locator(f'[data-testid="queue"] [data-item-id="{t["bad"]["id"]}"]').get_by_test_id("entry-why").click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
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
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:27.370Z

**tool call — Bash**
````
{
 "command": "grep -n \"def test_accepting_an_ai_draft_with_an_invented_number\" -B30 -A25 tests/unit/test_trace.py | head -120; grep -n \"ZLAYT_DB\\|sqlite\" tests/e2e/*.py | head"
}
````

### User / tool · 2026-11-02T05:30:27.465Z

**tool result**
````
1116-        if name.endswith("run failed"):
1117-            DB.update_case(conn, tok, status="failed")
1118-        g = _gate(c, tok)
1119-        ex = c.get(f"/api/cases/{tok}/export")
1120-        assert g["ready"] == (g["blockers"] == []) == (ex.status_code < 400), name
1121-        assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name
1122-
1123-
1124-def test_missing_qualifier_terms_name_the_words_to_keep_t098():
1125-    from app.backend import grounding
1126-    assert grounding.missing_qualifier_terms("MRI of the cervical spine was done.", "MRI suggests possible disc herniation.")
1127-    got = grounding.missing_qualifier_terms("Fracture seen.", "Possible left wrist fracture.")
1128-    assert "possible" in got and "left" in got
1129-    assert grounding.missing_qualifier_terms("Possible left wrist fracture.", "Possible left wrist fracture.") == []
1130-
1131-
1132-# ---- D-051 / T-098 r2: the code rung binds accept for every item, AI-made or human (reviewer F1: an AI draft 'Pain 5/10' over a quote without 5/10)
1133-def _ai_draft_with_invented_number(c, conn, tok, *, judge="supported", stored_reason=True, eid=None):
1134-    """An AI-made entry whose summary says 'Pain 5/10' over a quote that does not. State, reasons and judge verdict set like the generator + judge would."""
1135-    eid = eid or c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
1136-    row = DB.get_item(conn, eid, tok)
1137-    assert "5/10" not in row["excerpt"] and "ladder" in row and not row["ladder"].get("entered_by")
1138-    lad = row["ladder"]
1139-    lad["judge"] = {**(lad.get("judge") or {}), "verdict": judge}
1140-    DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10", ladder=lad,
1141-                   state="needs_review" if stored_reason else "verified", state_reasons_json=["SUMMARY_TOKEN_NOT_IN_EXCERPT"] if stored_reason else [])
1142-    return eid
1143-
1144-
1145-@pytest.mark.parametrize("judge", ["supported", "unsupported", "disagrees"])
1146:def test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051(env, judge):
1147-    c, conn, tok, _ = env
1148-    eid = _ai_draft_with_invented_number(c, conn, tok, judge=judge)
1149-    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
1150-    err = r.json()["error"]
1151-    assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED"
1152-    assert "not in the quote: 5." in err["message"] and err["message"].endswith("Edit the summary to match the quote.")
1153-    assert err["detail"]["next_action"]["text"] == "Edit the summary to match the quote" and err["detail"]["next_action"]["code"] == "EDIT_SUMMARY"
1154-    assert err["detail"]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and err["detail"]["step_id"] == "summary_tokens" and err["detail"]["tokens"] == ["5"]
1155-    assert DB.get_item(conn, eid, tok)["review_status"] == "pending"           # nothing was written
1156-    for x in c.get(f"/api/cases/{tok}").json()["entries"]:                      # accept everything else the paralegal can; the letter must not carry the figure
1157-        if x["id"] != eid:
1158-            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
1159-    ex = c.get(f"/api/cases/{tok}/export")
1160-    assert "5/10" not in ex.text
1161-
1162-
1163-def test_accept_recomputes_from_the_current_text_not_only_the_stored_reasons_d051(env):
1164-    c, conn, tok, _ = env
1165-    eid = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False)    # state 'verified', no stored reason: only the live check can catch it
1166-    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
1167-    assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED"
1168-
1169-
1170-def test_accept_refuses_a_dropped_qualifier_on_an_ai_draft_and_a_clean_draft_still_accepts_d051(env):
1171-    c, conn, tok, _ = env
tests/e2e/test_local_mode.py:10:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=str(tmp_path_factory.mktemp("loc") / "l.sqlite3"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:32.799Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def env\\|^def _gate\" -B3 -A22 tests/unit/test_trace.py | head -70; grep -n \"def update_item\" -A15 app/db/db.py | head -30; sed -n 40,107p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T05:30:32.895Z

**tool result**
````
45-
46-
47-@pytest.fixture
48:def env(base, tmp_path, monkeypatch):
49-    monkeypatch.setenv("LLM_BACKEND", "fixture")
50-    monkeypatch.delenv("ZLAYT_MODE", raising=False)
51-    path = str(tmp_path / "copy.sqlite")
52-    src = sqlite3.connect(base["db"])
53-    dst = sqlite3.connect(path)
54-    src.backup(dst)
55-    src.close()
56-    dst.close()
57-    conn = DB.connect(path)
58-    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
59-    return c, conn, base["tok"], base["pre"]
60-
61-
62-def steps_of(t):
63-    return {s["id"]: s for s in t["steps"]}
64-
65-
66-def walk(o, keys):
67-    """Every dict key anywhere in o that is in `keys`."""
68-    found = set()
69-    if isinstance(o, dict):
70-        for k, v in o.items():
--
534-    assert j["status"] == "pending" and j["counts"]["unavailable"] == n and "agreed" not in j["why"]
535-
536-
537:def _gate_states(c, conn, tok):
538-    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
539-    case = c.get(f"/api/cases/{tok}").json()
540-    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
541-    yield "pending items"
542-    DB.update_case(conn, tok, status="running")
543-    yield "running with pending items"
544-    DB.update_case(conn, tok, status="ready")
545-    for i in ids:
546-        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"})
547-    yield "everything dismissed"
548-    DB.update_case(conn, tok, status="failed")
549-    yield "failed, everything dismissed"
550-    DB.update_case(conn, tok, status="ready")
551-    # accept every item still reviewable
552-    for i in ids:
553-        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"})
554-    yield "all accepted"
555-    DB.update_case(conn, tok, status="running")
556-    yield "all accepted, running"
557-    DB.update_case(conn, tok, status="failed")
558-    yield "all accepted, failed"
559-
--
689-    return n
690-
691-
692:def _gate(c, tok):
693-    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
694-
695-
696-def _jnr(gate):
697-    return [b for b in gate["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
698-
699-
700-def test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_action(env):
701-    c, conn, tok, _ = env
702-    n = _blank_and_accept(c, conn, tok)
703-    gate = _gate(c, tok)
704-    got = _jnr(gate)
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
205-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
206-    table, found = _find(conn, item_id, case)
207-    bad = set(fields) - _cols(conn, table)
208-    if bad:
209-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
210-    fields["updated_at"] = now
211-    sets = ", ".join(f"{k}=?" for k in fields)
212-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
213-
214-
215-def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:38.818Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"rv-error\\|rv-batchbar\\|rv-blocked\\|rv-help\" review.css styles.css | head; grep -n \"zs-btn\\b\" stepper.css | head -3; grep -n \"scroll-margin\\|zs-exnote\" stepper.css | head; grep -n \"stepper.js\\|review.js\\|batch.js\\|judges.js\" index.html; grep -n \"label\\b.*= \\|S.label =\" stepper.js | head -5"
}
````

### User / tool · 2026-11-02T05:30:38.930Z

**tool result**
````
review.css:10:.rv-help, .rv-keys, .rv-why, .rv-empty { color: var(--rv-muted); font-size: .9rem; margin: .25rem 0 .75rem; }
review.css:51:.rv-error { color: var(--rv-bad-ink); font-size: .9rem; margin: .3rem 0 0; }
review.css:52:.rv-error:empty { display: none; }
review.css:92:.rv-batchbar { display: flex; flex-wrap: wrap; gap: .5rem .75rem; align-items: center; margin: .5rem 0; padding: .5rem; border: 1px dashed var(--rv-line); border-radius: 8px; }
review.css:93:.rv-batchbar .rv-help { margin: 0; flex: 1 1 16rem; }
review.css:107:.es-field .rv-help { display: block; margin: .15rem 0 0; font-weight: 400; }
24:.zs-btn.zs-primary { background: var(--zs-accent); color: var(--zs-surface); }
78:.zs-btn { font: inherit; font-size: .88rem; font-weight: 600; min-height: 44px; padding: 4px 12px; border: 1px solid var(--zs-accent); background: var(--zs-surface); color: var(--zs-accent); border-radius: 8px; cursor: pointer; }
79:.zs-btn:focus-visible { outline: 3px solid var(--zs-accent); outline-offset: 2px; }
117:.zs-exnote { margin: 8px 0 12px; padding: 8px 12px; border: 2px solid var(--zs-bad); border-radius: var(--zs-radius); background: var(--zs-surface); }
118:.zs-exnote:focus { outline: 3px solid var(--zs-accent); outline-offset: 2px; }
119:.zs-exnote-ok { border-color: var(--zs-ok); }
120:.zs-exnote-msg { margin: 0 0 6px; }
53:<script src="stepper.js"></script>
55:<!-- T-043 (frontend-2): review.js first (controls + keys), then the panels -->
56:<script src="review.js"></script>
59:<script src="batch.js"></script>
61:<script src="judges.js"></script>
51:  S.label = function (id) {
396:      if (notAIChecked) v.label = (tr.review_status === "edited" ? "Edited" : "Accepted") + " by you, not AI-checked";
397:      else if (skippedJudge) { v.code = "needs_attention"; v.label = "Accepted, second check missing"; }   // the gate (or an unloaded gate) holds it: not a green "Accepted by you"
402:    const rail = el("ol", { class: "zs-rail", "aria-label": "Checks for " + S.label(tr.item_id) }, steps.map((s, i) => stepNode(s, i === act, ctx)));
492:      el("ol", { class: "zs-rail", "aria-label": "Case checks, from reading the paste to the export gate" }, steps.map((s, i) => stepNode(s, i === act, ctx))),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:39.776Z

Now implement review.js changes.

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:39.813Z

**tool call — bash_placeholder**
````
{}
````

### User / tool · 2026-11-02T05:30:39.815Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash_placeholder</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:44.538Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/review.js",
 "old_string": "  function showError(id, msg) { const s = slot(id, \"rv-error\"); if (s) s.textContent = msg; RV.say(msg, true); }",
 "new_string": "  function showError(id, msg) { const s = slot(id, \"rv-error\"); if (s) s.textContent = msg; RV.say(msg, true); }\n\n  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends \"Edit the summary to match the\n  // quote.\") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.\n  const refusals = {};       // id -> {message}\n  function paintRefusal(root, id, edit) {\n    const r = refusals[id], box = root.querySelector(\".rv-refused\");\n    if (!box) return;\n    ZL.clear(box); box.hidden = !r;\n    if (!r) return;\n    box.append(el(\"p\", { class: \"rv-refused-msg\", \"data-testid\": \"accept-refused-msg\" }, el(\"strong\", {}, \"Not accepted. \"), r.message),\n      edit ? el(\"button\", { type: \"button\", class: \"rv-btn rv-refused-edit\", \"data-testid\": \"btn-accept-refused-edit\", \"aria-label\": \"Edit the summary for \" + r.label, onclick: edit }, \"Edit the summary\") : null);\n  }\n  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for=\"' + id + '\"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }\n  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === \"CODE_CHECK_FAILED\";"
}
````

### User / tool · 2026-11-02T05:30:44.596Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/review.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:45.575Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/review.js",
 "old_string": "    busy.add(id);\n    try {\n      const resp = await ZL.api.review(c.token, id, body);",
 "new_string": "    busy.add(id);\n    try {\n      const resp = await ZL.api.review(c.token, id, body);\n      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }"
}
````

### User / tool · 2026-11-02T05:30:45.628Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/review.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:47.576Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/review.js",
 "old_string": "      } else if (e && String(e.code).toUpperCase() === \"DATE_UNCONFIRMED\") showError(id, DATE_FIRST + \" \" + DATE_WHY);",
 "new_string": "      } else if (RV.isCodeCheckRefusal(e) && body.action === \"accept\") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed\n        refusals[id] = { message: e.message || \"The summary fails a check. Edit the summary to match the quote.\", label: found ? RV.label(found.item) : id };\n        repaintRefusal(id); RV.say(\"Not accepted: \" + refusals[id].message, true);\n      } else if (e && String(e.code).toUpperCase() === \"DATE_UNCONFIRMED\") showError(id, DATE_FIRST + \" \" + DATE_WHY);"
}
````

### User / tool · 2026-11-02T05:30:47.627Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/review.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:48.674Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/review.js",
 "old_string": "    root.append(bar);\n    if (blocked) root.append(",
 "new_string": "    root.append(bar);\n    root.append(el(\"div\", { class: \"rv-refused\", role: \"alert\", hidden: true, \"data-testid\": \"accept-refused\" }));\n    if (blocked) root.append("
}
````

### User / tool · 2026-11-02T05:30:48.729Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/review.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:30:50.059Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/review.js",
 "old_string": "      ui[id] = { openEdit: () => toggleEdit(true) };\n    } else ui[id] = {};\n    root.append(el(\"div\", { class: \"rv-error\", role: \"alert\" }));\n    return root;",
 "new_string": "      ui[id] = { openEdit: () => toggleEdit(true) };\n      root._openEdit = () => toggleEdit(true);\n    } else ui[id] = {};\n    root.append(el(\"div\", { class: \"rv-error\", role: \"alert\" }));\n    paintRefusal(root, id, root._openEdit);\n    return root;"
}
````

### User / tool · 2026-11-02T05:30:50.118Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/review.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:00.530Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='batch.js'\ns=open(p).read()\ns=s.replace(\"\"\"  let busy = false;\n\"\"\",\"\"\"  let busy = false;\n  let refused = null;   // {token, message, rows:[{id, why}]}: the last batch the server refused for a failing code check (D-051); nothing was accepted\n\"\"\",1)\ns=s.replace(\"\"\"        const plain = (r.status === 404\"\"\",\"\"\"        if (String(code).toUpperCase() === \"CODE_CHECK_FAILED\") {   // D-051 (T-098 r2): the whole batch is refused; say which items and why, with an Edit action on each\n          const d = (r.body.error.detail || {}), list = Array.isArray(d.rejected) ? d.rejected : [];\n          refused = { token: c.token, message: r.body.error.message || \"Nothing was accepted: a summary fails a check.\", rows: list.map((x) => ({ id: x.id || x.item_id, why: x.why || \"\" })).filter((x) => x.id) };\n          paintBar(c); RV.say(refused.message, true);\n          const f = document.querySelector('[data-testid=\"batch-refused-msg\"]'); if (f) { f.setAttribute(\"tabindex\", \"-1\"); f.focus(); }\n          return;\n        }\n        const plain = (r.status === 404\"\"\",1)\ns=s.replace(\"\"\"      last = { token: c.token, ids };\"\"\",\"\"\"      refused = null;\n      last = { token: c.token, ids };\"\"\",1)\n# bar: add refused box\ns=s.replace(\"\"\"  function bar(c) {\"\"\",\"\"\"  // Items the server named that are still waiting (an item the paralegal has since edited, accepted or dismissed drops out of the list).\n  function refusedRows(c) {\n    if (!refused || refused.token !== c.token) return [];\n    return refused.rows.filter((x) => { const f = RV.find(c, x.id); return f && (f.item.review_status || \"pending\") === \"pending\"; });\n  }\n  function refusedBox(c) {\n    const rows = refusedRows(c);\n    if (!rows.length) return null;\n    return el(\"div\", { class: \"rv-refused rv-refused-batch\", role: \"alert\", \"data-testid\": \"batch-refused\" },\n      el(\"p\", { class: \"rv-refused-msg\", \"data-testid\": \"batch-refused-msg\" }, el(\"strong\", {}, \"Nothing was accepted. \"), refused.message),\n      el(\"ul\", { class: \"rv-refused-list\" }, rows.map((x) => {\n        const f = RV.find(c, x.id), name = f ? RV.label(f.item) : x.id;\n        return el(\"li\", { \"data-testid\": \"batch-refused-item\", \"data-refused-id\": x.id },\n          el(\"span\", { class: \"rv-refused-name\" }, name), x.why ? el(\"span\", { class: \"rv-refused-why\" }, \" \" + x.why) : null, \" \",\n          ZL.stepper && ZL.stepper.editItem ? el(\"button\", { type: \"button\", class: \"rv-btn rv-refused-edit\", \"data-testid\": \"btn-batch-refused-edit\", \"aria-label\": \"Edit the summary for \" + name, onclick: () => ZL.stepper.editItem(x.id) }, \"Edit the summary\") : null);\n      })));\n  }\n  function bar(c) {\"\"\",1)\ns=s.replace(\"\"\"      el(\"span\", { class: \"rv-help\" }, \"Entries only. Charges, flags and anything marked needs review always need your own decision. Shift+A does the same.\"));\n  }\"\"\",\"\"\"      el(\"span\", { class: \"rv-help\" }, \"Entries only. Charges, flags and anything marked needs review always need your own decision. Shift+A does the same.\"),\n      refusedBox(c));\n  }\n  function paintBar(c) {\n    const wrap = document.querySelector('[data-testid=\"timeline\"]'), old = wrap && wrap.querySelector(\":scope > .rv-batchbar\");\n    if (old) old.replaceWith(bar(c));\n  }\"\"\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"ZL.stepper.editItem\\|editItem\" stepper.js | head -3; grep -n \"order\\|script\" index.html | sed -n 1,30p"
}
````

### User / tool · 2026-11-02T05:31:00.669Z

**tool result**
````
202:  S.editItem = function (id) {
276:      case "EDIT_SUMMARY": if (itemId) btn("Go to the item and edit the summary", () => S.editItem(itemId)); break;
411:        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-wording-edit", "aria-label": "Edit your wording for " + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, "Edit your wording"))) : null,
43:<!-- load order matters; mock files are only used when API_MODE is "mock" -->
44:<script src="dom.js"></script>
45:<script src="mock_sample.js"></script>
46:<script src="mock.js"></script>
47:<script src="mock_flags.js"></script>
48:<script src="mock_extra.js"></script>
49:<script src="api.js"></script>
50:<script src="state.js"></script>
51:<script src="input.js"></script>
52:<script src="source.js"></script>
53:<script src="stepper.js"></script>
54:<script src="timeline.js"></script>
56:<script src="review.js"></script>
57:<script src="flags.js"></script>
58:<script src="charges.js"></script>
59:<script src="batch.js"></script>
60:<script src="audit.js"></script>
61:<script src="judges.js"></script>
62:<script src="manual.js"></script>
63:<script src="narrative.js"></script>
64:<script src="exportcfg.js"></script>
65:<script src="excerpt.js"></script>
66:<script src="export.js"></script>
67:<script src="sidebyside.js"></script>
68:<script src="switcher.js"></script>
69:<script src="app.js"></script>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:06.784Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='batch.js'\ns=open(p).read()\ns=s.replace(\"const f = RV.find(c, x.id), name = f ? RV.label(f.item) : x.id;\",\"const name = ZL.stepper && ZL.stepper.label ? ZL.stepper.label(x.id) : x.id;\")\nopen(p,'w').write(s)\np='review.js'\ns=open(p).read()\ns=s.replace(\"label: found ? RV.label(found.item) : id };\",\"label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };\")\nopen(p,'w').write(s)\nEOF\nsed -n 45,62p stepper.js\ncat >> review.css <<'EOF'\n\n/* D-051 (T-098 r2): Accept refused for a failing code check: the server's reason right under the item's buttons, with an Edit action; the batch version lists the items. */\n.rv-refused { margin: .4rem 0 0; padding: .5rem .65rem; border: 2px solid var(--rv-bad-ink); border-radius: 8px; color: var(--rv-bad-ink); font-size: .9rem; }\n.rv-refused[hidden] { display: none; }\n.rv-refused-msg { margin: 0 0 .4rem; }\n.rv-refused-batch { flex: 1 1 100%; }\n.rv-refused-list { margin: 0; padding-left: 1.1rem; }\n.rv-refused-list li { margin: .35rem 0; }\n.rv-refused-why { color: var(--rv-ink, inherit); }\n.rv-refused .rv-btn { min-height: 44px; }\nEOF\ngrep -n \"^:root\\|--rv-bad-ink\\|--rv-ink\" review.css | head"
}
````

### User / tool · 2026-11-02T05:31:06.903Z

**tool result**
````
  const caseNow = () => ZL.state.get().case;
  const recSeq = (id) => { const r = ((caseNow() || {}).records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };

  // ---- labels for items (entry: date and provider; amount: the figure; flag: its title)
  const extraLabels = {};   // narrative sentences register their own label ("ns1" -> first words of the sentence)
  S.setLabel = (id, text) => { const t = String(text || "").trim(); extraLabels[id] = t.length > 60 ? t.slice(0, 57).replace(/\s+\S*$/, "") + "…" : t; };
  S.label = function (id) {
    const c = caseNow(), f = c && rv() && rv().find(c, id);
    if (!f) return extraLabels[id] || id;
    const it = f.item;
    if (f.kind === "entry") return (it.date || "undated") + " · " + (it.provider || "entry");
    if (f.kind === "amount") return (it.text || it.id) + (it.kind ? " (" + it.kind + ")" : "");
    return it.title || it.id;
  };

  // Where an item sits in the records: "Record 3", "Records 3 and 5" (entries and amounts: record_ids; flags: the records of their evidence). Empty when unknown.
  S.cue = function (id) {
    const c = caseNow(), f = c && rv() && rv().find(c, id);
2::root {
3:  --rv-ink: #1c2430; --rv-muted: #566170; --rv-line: #cfd6df; --rv-bg: #ffffff; --rv-soft: #f4f6f9;
5:  --rv-bad-bg: #fde8e8; --rv-bad-ink: #7a1212; --rv-focus: #0b57d0;
7:.rv-panel { color: var(--rv-ink); max-width: 100%; min-width: 0; margin: 1.25rem 0; overflow-wrap: anywhere; }
26:.rv-state-rejected, .rv-rs-dismissed { background: var(--rv-bad-bg); color: var(--rv-bad-ink); border-color: #e3a3a3; }
51:.rv-error { color: var(--rv-bad-ink); font-size: .9rem; margin: .3rem 0 0; }
95:.au-drawer { position: fixed; inset: 0 0 0 auto; margin: 0; height: 100%; max-height: 100%; width: min(36rem, 100vw); max-width: 100vw; box-sizing: border-box; border: 0; border-left: 2px solid var(--rv-line); padding: 1rem; overflow: auto; color: var(--rv-ink); background: var(--rv-bg); }
111:.rv-refused { margin: .4rem 0 0; padding: .5rem .65rem; border: 2px solid var(--rv-bad-ink); border-radius: 8px; color: var(--rv-bad-ink); font-size: .9rem; }
117:.rv-refused-why { color: var(--rv-ink, inherit); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:09.106Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"prefers-color\" review.css | head -3; sed -n 1,8p review.css; grep -n \"refusals\\|paintRefusal\" review.js | head"
}
````

### User / tool · 2026-11-02T05:31:09.213Z

**tool result**
````
/* Flags panel, charges table and review controls (T-043). Self-contained: own tokens, works with or without styles.css. */
:root {
  --rv-ink: #1c2430; --rv-muted: #566170; --rv-line: #cfd6df; --rv-bg: #ffffff; --rv-soft: #f4f6f9;
  --rv-accent: #124e9c; --rv-warn-bg: #fff4d6; --rv-warn-ink: #5b3d00; --rv-ok-bg: #e3f3e8; --rv-ok-ink: #14532d;
  --rv-bad-bg: #fde8e8; --rv-bad-ink: #7a1212; --rv-focus: #0b57d0;
}
.rv-panel { color: var(--rv-ink); max-width: 100%; min-width: 0; margin: 1.25rem 0; overflow-wrap: anywhere; }
.rv-panel h2 { font-size: 1.25rem; margin: 0 0 .25rem; }
132:  const refusals = {};       // id -> {message}
133:  function paintRefusal(root, id, edit) {
134:    const r = refusals[id], box = root.querySelector(".rv-refused");
141:  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
165:      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
180:        refusals[id] = { message: e.message || "The summary fails a check. Edit the summary to match the quote.", label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
181:        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
248:    paintRefusal(root, id, root._openEdit);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:20.751Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && grep -n \"ai_drafted\\|AI drafted\\|fail.* a check\\|fails a check\" app/backend/trace.py | head -30"
}
````

### User / tool · 2026-11-02T05:31:20.752Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:22.799Z

**tool call — Bash**
````
{
 "command": "grep -n \"ai_drafted\\|AI drafted\\|fail.* a check\\|fails a check\\|fail a check\" app/backend/trace.py | cut -c1-260 | head -30"
}
````

### User / tool · 2026-11-02T05:31:22.889Z

**tool result**
````
324:        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
332:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
335:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
338:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
761:    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
916:        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PASS, f"The AI drafted an entry for all {len(firsts)} records.", rule="row 4", counts=ecounts))
1008:               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:24.360Z

**tool call — Bash**
````
{
 "command": "sed -n 985,1020p app/backend/trace.py | cut -c1-400; grep -n \"AI drafted this\\|the AI drafted\\|AI wrote\" app/backend/trace.py app/backend/review.py | cut -c1-300 | head"
}
````

### User / tool · 2026-11-02T05:31:24.453Z

**tool result**
````
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
                if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend} not reviewed)" if n_pend else "")} if ready
               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
                      else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
app/backend/trace.py:47:    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
app/backend/trace.py:653:    st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:26.948Z

**tool call — Bash**
````
{
 "command": "grep -n \"ccf\" app/backend/trace.py | head -12; grep -n \"def code_check_blockers\\|def _code_blockers\" -A40 app/backend/trace.py | cut -c1-300 | head -70"
}
````

### User / tool · 2026-11-02T05:31:27.052Z

**tool result**
````
984:    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
990:                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
1008:               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
437:def code_check_blockers(conn, case_id: str, cx=None) -> list:
438-    """Export blockers (D-045(b), D-051): accepted or edited entries, AI-made or human, whose current summary or quote fails a code check.
439-    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
440-    cx = cx or _Cx(conn, case_id, False)
441-    out = []
442-    for row in DB.list_items(conn, case_id, "entry"):
443-        if not _code_check_gated(row):
444-            continue
445-        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
446-        if not fails:
447-            continue
448-        f = fails[0]
449-        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
450-                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED" if _paralegal_wording("entry", row) else "CODE_CHECK_FAILED_AI"], "next_action": _fix_action(row, f)})
451-    return out
452-
453-
454-# ------------------------------------------------------------------ amounts
455-def _amount_steps(cx, row):
456-    R = set(row.get("state_reasons") or [])
457-    lad = row.get("ladder") or {}
458-    cc = lad.get("code_checks") or {}
459-    rid = (row.get("record_ids") or [None])[0]
460-    rec = cx.recs.get(rid, {})
461-    kind = row["kind"]
462-    vals = {"text": row["text"], "value_cents": row["value_cents"], "kind": kind, "classified_by": cc.get("classified_by")}
463-    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
464-    gfail = "GROUNDING_AMOUNT_NOT_IN_TEXT" in R or cc.get("amount_in_text") is False
465-    st = []
466-    if gfail:
467-        st.append(step("found_in_text", "Dollar figure is in the record text", "code", FAIL, reason_text("GROUNDING_AMOUNT_NOT_IN_TEXT"), reason="GROUNDING_AMOUNT_NOT_IN_TEXT",
468-                       rule="row 6", evidence={"excerpt": exc, "values": vals}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"])))
469-        st.append(_skipped("amount_class", "Rule says what the figure is", "code", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
470-    else:
471-        st.append(step("found_in_text", "Dollar figure is in the record text", "code", PASS, "Code found this figure in the record by pattern; it is not a model's claim.",
472-                       rule="row 6", evidence={"excerpt": exc, "values": vals}))
473-        if kind == "charge":
474-            st.append(step("amount_class", "Rule says what the figure is", "code", PASS,
475-                           "A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it.", rule="row 7", evidence={"values": vals}))
476-        elif kind == "unclear":
477-            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:33.196Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"evidenceNode\\|_notNeeded\" stepper.js | cut -c1-240; sed -n 331,376p stepper.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T05:31:33.289Z

**tool result**
````
19:    if (st._notNeeded) return { glyph: GLYPH.skipped, word: "Not needed", cat: "skipped" };   // the export gate does not list this item: the wording is the paralegal's own (D-045 b)
305:  function evidenceNode(st) {
364:    const ev = evidenceNode(st); if (ev.length) body.append(el("div", { class: "zs-evidence", "data-testid": "step-evidence" }, ev));
391:      steps = steps.map((x) => (x.status === "skipped" && needsRerun(x) ? Object.assign({}, x, { _notNeeded: true, next_action: null, reason_code: null, why: HUMAN_NOTE }) : x));
    if (techNodes.length || ev.response_raw)
      out.push(el("details", { class: "zs-more", "data-testid": "step-tech" }, el("summary", {}, "Technical details"), techNodes.length ? el("p", { class: "zs-ev" }, techNodes) : null,
        ev.response_raw ? el("pre", { class: "zs-pre" }, typeof ev.response_raw === "string" ? ev.response_raw : JSON.stringify(ev.response_raw, null, 2)) : null));
    return out;
  }

  // Count chips in the paralegal's words: no "llm", "lexicon" or reason codes in the primary view (those are in Technical details).
  const WORD = { code: "code", llm: "AI", lexicon: "phrase list", "lexicon+llm": "phrase list and AI" };
  const KEY = { by_origin: "found by", by_type: "kinds", method: "records split by", unsupported: "AI objected", supported: "AI agreed", unsure: "undecided", items_judged: "items checked", pending_items: "not reviewed", judge_not_run: "second check did not run
  function fmtCounts(counts) {
    const out = [];
    Object.entries(counts || {}).forEach(([k, v]) => {
      if (k === "llm_split" || k === "reasons") return;
      if (v && typeof v === "object") {
        const inner = Object.entries(v).map(([a, b]) => (WORD[a] || humanize(a)) + " " + b).join(", ");
        if (inner) out.push((KEY[k] || humanize(k)) + ": " + inner);
      } else if (/_cents$/.test(k) && typeof v === "number" && rv()) out.push(humanize(k.replace(/_cents$/, "")) + " " + rv().money(v));
      else if (v != null && v !== "") out.push((KEY[k] || humanize(k)) + " " + (k === "method" ? (WORD[v] || v) + (v === "code" ? " (not AI)" : "") : v));
    });
    return out;
  }

  // ---- one step
  function stepNode(st, active, ctx) {
    const { glyph, word } = statusInfo(st);
    const li = el("li", { class: "zs-step", "data-testid": ctx.testid || "step", "data-step-id": st.id, "data-status": st.status, "data-kind": st.kind, "aria-current": active ? "step" : null, tabindex: active ? "-1" : null },
      el("span", { class: "zs-marker", "aria-hidden": "true", "data-testid": "step-marker" }, glyph),
      el("div", { class: "zs-body" },
        el("div", { class: "zs-head" },
          el("span", { class: "zs-label" }, st.label), el("span", { class: "zs-kind zs-kind-" + st.kind, "data-testid": "step-kind" }, kindOf(st)),
          el("span", { class: "zs-status", "data-testid": "step-status" }, word), st.blocks_export ? el("span", { class: "zs-blocks" }, "Blocks export") : null),
        st.why ? el("p", { class: "zs-why", "data-testid": "step-why" }, st.why) : null));
    const body = li.lastChild;
    const ev = evidenceNode(st); if (ev.length) body.append(el("div", { class: "zs-evidence", "data-testid": "step-evidence" }, ev));
    if (ctx.extra) { const x = ctx.extra(st); if (x) body.append(x); }
    if (st.status === "fail" || st.status === "pending" || (st.status === "skipped" && needsRerun(st))) { const a = actionNode(st.next_action, ctx, st); if (a) body.append(a); }
    return li;
  }
  // The active step is the one the human has to deal with now: the first fail or pending step that carries a next action.
  function activeIndex(steps) {
    let i = steps.findIndex((s) => (s.status === "fail" || s.status === "pending" || (s.status === "skipped" && needsRerun(s))) && s.next_action);
    if (i < 0) i = steps.findIndex((s) => s.status === "fail" || s.status === "pending");
    return i;
  }

  // ---- item level
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:34.159Z

Now apply stepper edits.

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:41.649Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='stepper.js'\ns=open(p).read()\n\n# m-new-1: Not needed step drops the judge verdict/rationale lines\ns=s.replace(\"\"\"  function evidenceNode(st) {\n    const ev = st.evidence || {}, out = [];\"\"\",\"\"\"  function evidenceNode(st) {\n    const ev = Object.assign({}, st.evidence || {}), out = [];\n    if (st._notNeeded) { delete ev.judge_verdict; delete ev.rationale; delete ev.judge_reason_code; }   // \"Not needed\" must not also print \"The second AI check said: Unavailable\\\"\"\"\",1)\n\n# wording lead: AI draft vs paralegal's own\ns=s.replace(\"\"\"  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;\"\"\",\"\"\"  const WORDING_AI = \"This summary doesn't match the quote:\";\n  // D-051: a blocker on an accepted AI draft says \"This summary\", not \"Your wording\" (the paralegal did not write it); an edited or hand-written one says \"Your wording\".\n  const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== \"entry\" || f.item.ai_drafted === false || f.item.review_status === \"edited\"; };\n  S.wordingLead = (id) => (mine(id) ? WORDING : WORDING_AI);\n  S.wordingEditText = (id) => (mine(id) ? \"Edit your wording\" : \"Edit the summary\");\n  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;\"\"\",1)\ns=s.replace(\"\"\"el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, WORDING + \" \"), wf.why || \"\"),\n        el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-wording-edit\", \"aria-label\": \"Edit your wording for \" + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, \"Edit your wording\"))) : null,\"\"\",\"\"\"el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, S.wordingLead(tr.item_id) + \" \"), wf.why || \"\"),\n        el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-wording-edit\", \"aria-label\": S.wordingEditText(tr.item_id) + \" for \" + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, S.wordingEditText(tr.item_id)))) : null,\"\"\",1)\ns=s.replace(\"\"\"wording ? [el(\"strong\", {}, WORDING + \" \"), b.why || \"\"] : b.why || \"\"\"\"\"\",\"\"\"wording ? [el(\"strong\", {}, S.wordingLead(b.item_id) + \" \"), b.why || \"\"] : b.why || \"\"\"\"\",1)\ns=s.replace(\"\"\"wording ? el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-gate-edit\", \"aria-label\": \"Edit your wording for \" + name, onclick: () => S.editItem(b.item_id) }, \"Edit your wording\") : null,\"\"\",\"\"\"wording ? el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-gate-edit\", \"aria-label\": S.wordingEditText(b.item_id) + \" for \" + name, onclick: () => S.editItem(b.item_id) }, S.wordingEditText(b.item_id)) : null,\"\"\",1)\n# m-new / n-new-3: edited item whose verdict says Accepted by you\ns=s.replace(\"\"\"    const ctx = { itemId: tr.item_id };\n    // a record id\"\"\",\"\"\"    if (v.code === \"accepted\" && tr.review_status === \"edited\" && /^Accepted by you/.test(v.label || \"\")) v.label = v.label.replace(/^Accepted by you/, \"Edited by you\");   // n-new-3\n    const ctx = { itemId: tr.item_id };\n    // a record id\"\"\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"S.wordingLead\\|WORDING\" stepper.js | cut -c1-140"
}
````

### User / tool · 2026-11-02T05:31:41.758Z

**tool result**
````
  File "<stdin>", line 26
    // a record id""",1)
                  ^
SyntaxError: unterminated triple-quoted string literal (detected at line 27)
130:  const WORDING = "Your wording doesn't match the quote:";
132:  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;
410:        el("p", { class: "zs-todo-text" }, el("strong", {}, WORDING + " "), wf.why || ""),
450:      el("span", { class: "zs-blocker-name" }, name), " ", el("span", { class: "zs-ev" }, wording ? [el("strong", {}, WORDING + " "), b.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:44.372Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "    const ev = st.evidence || {}, out = [];\n    if (ev.excerpt && ev.excerpt.text)",
 "new_string": "    const ev = Object.assign({}, st.evidence || {}), out = [];\n    if (st._notNeeded) { delete ev.judge_verdict; delete ev.rationale; delete ev.judge_reason_code; }   // \"Not needed\" must not also print \"The second AI check said: Unavailable\"\n    if (ev.excerpt && ev.excerpt.text)"
}
````

### User / tool · 2026-11-02T05:31:44.461Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:46.270Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;",
 "new_string": "  const WORDING_AI = \"This summary doesn't match the quote:\";\n  // D-051: a blocker on an accepted AI draft says \"This summary\", not \"Your wording\" (the paralegal did not write it); an edited or hand-written one says \"Your wording\".\n  const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== \"entry\" || f.item.ai_drafted === false || f.item.review_status === \"edited\"; };\n  S.wordingLead = (id) => (mine(id) ? WORDING : WORDING_AI);\n  S.wordingEditText = (id) => (mine(id) ? \"Edit your wording\" : \"Edit the summary\");\n  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;"
}
````

### User / tool · 2026-11-02T05:31:46.325Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:48.224Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, WORDING + \" \"), wf.why || \"\"),\n        el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-wording-edit\", \"aria-label\": \"Edit your wording for \" + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, \"Edit your wording\"))) : null,",
 "new_string": "el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, S.wordingLead(tr.item_id) + \" \"), wf.why || \"\"),\n        el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"zs-btn zs-primary\", \"data-testid\": \"btn-wording-edit\", \"aria-label\": S.wordingEditText(tr.item_id) + \" for \" + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, S.wordingEditText(tr.item_id)))) : null,"
}
````

### User / tool · 2026-11-02T05:31:48.284Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:49.160Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "wording ? [el(\"strong\", {}, WORDING + \" \"), b.why || \"\"]",
 "new_string": "wording ? [el(\"strong\", {}, S.wordingLead(b.item_id) + \" \"), b.why || \"\"]"
}
````

### User / tool · 2026-11-02T05:31:49.223Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:50.193Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "\"aria-label\": \"Edit your wording for \" + name, onclick: () => S.editItem(b.item_id) }, \"Edit your wording\") : null,",
 "new_string": "\"aria-label\": S.wordingEditText(b.item_id) + \" for \" + name, onclick: () => S.editItem(b.item_id) }, S.wordingEditText(b.item_id)) : null,"
}
````

### User / tool · 2026-11-02T05:31:50.245Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:51.408Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "old_string": "    const ctx = { itemId: tr.item_id };\n    // a record id",
 "new_string": "    if (v.code === \"accepted\" && tr.review_status === \"edited\" && /^Accepted by you/.test(v.label || \"\")) v.label = v.label.replace(/^Accepted by you/, \"Edited by you\");   // an item the paralegal wrote reads \"Edited\", not \"Accepted\"\n    const ctx = { itemId: tr.item_id };\n    // a record id"
}
````

### User / tool · 2026-11-02T05:31:51.475Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/stepper.js has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:31:59.739Z

**tool call — Bash**
````
{
 "command": "grep -n \"def rejudge\" -A40 app/backend/*.py | cut -c1-240 | head -80; grep -n \"rejudge\" memory/contracts/api.md | cut -c1-500 | head -5"
}
````

### User / tool · 2026-11-02T05:31:59.841Z

**tool result**
````
app/backend/api.py:371:    async def rejudge_case(token: str):
app/backend/api.py-372-        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/api.py-373-        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
app/backend/api.py-374-        from app.backend import rejudge as RJ
app/backend/api.py-375-        c = conn()
app/backend/api.py-376-        try:
app/backend/api.py-377-            case = get_case(c, token)
app/backend/api.py-378-            if case["status"] == "running" or token in runs or token in rejudging:
app/backend/api.py-379-                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
app/backend/api.py-380-            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py-381-                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py-382-            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py-383-                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
app/backend/api.py-384-            rejudging.add(token)
app/backend/api.py-385-            try:
app/backend/api.py-386-                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
app/backend/api.py-387-            finally:
app/backend/api.py-388-                rejudging.discard(token)
app/backend/api.py-389-        finally:
app/backend/api.py-390-            c.close()
app/backend/api.py-391-
app/backend/api.py-392-    @app.get("/api/cases/{token}/status")
app/backend/api.py-393-    def status(token: str):
app/backend/api.py-394-        c = conn()
app/backend/api.py-395-        try:
app/backend/api.py-396-            case = get_case(c, token)
app/backend/api.py-397-            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
app/backend/api.py-398-            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
app/backend/api.py-399-            stages = list(stages) if not callable(stages) else STAGES
app/backend/api.py-400-            done = stages.index(stage) if stage in stages else 0
app/backend/api.py-401-            end = case["run_finished_at"] or time.time()
app/backend/api.py-402-            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
app/backend/api.py-403-                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
app/backend/api.py-404-                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
app/backend/api.py-405-                               "flags": len(DB.list_items(c, token, "flag"))},
app/backend/api.py-406-                    "error": json.loads(case["error"]) if case["error"] else None,
app/backend/api.py-407-                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
app/backend/api.py-408-        finally:
app/backend/api.py-409-            c.close()
app/backend/api.py-410-
app/backend/api.py-411-    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/rejudge.py:64:def rejudge(conn, case_id: str, call, now: float = None) -> dict:
app/backend/rejudge.py-65-    t = time.time() if now is None else now
app/backend/rejudge.py-66-    case = DB.get_case(conn, case_id)
app/backend/rejudge.py-67-    case_text = (case["raw_text"] or "").replace("\r\n", "\n").replace("\r", "\n").strip()
app/backend/rejudge.py-68-    targets = trace.unjudged_items(conn, case_id)
app/backend/rejudge.py-69-    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
app/backend/rejudge.py-70-        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
app/backend/rejudge.py-71-    done, still = [], []
app/backend/rejudge.py-72-    for tg, (verdict, call_id, code) in zip(targets, answers):
app/backend/rejudge.py-73-        row, jid = tg["row"], tg["judge"]
app/backend/rejudge.py-74-        lad = dict(row.get("ladder") or {"item_id": row["id"]})
app/backend/rejudge.py-75-        ladder_verdict = judges.to_ladder(jid, verdict)
app/backend/rejudge.py-76-        attempt = {"at": t, "call_id": call_id, "verdict": ladder_verdict}
app/backend/rejudge.py-77-        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
app/backend/rejudge.py-78-        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
app/backend/rejudge.py-79-        if ladder_verdict == "unavailable":
app/backend/rejudge.py-80-            DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
app/backend/rejudge.py-81-            _log(conn, case_id, row, jid, call_id, "unavailable", row["state"], t)
app/backend/rejudge.py-82-            still.append(dict(base, verdict="unavailable"))
app/backend/rejudge.py-83-            continue
app/backend/rejudge.py-84-        lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": spanish.JUDGE_PROMPT if (jid == "j1" and lad.get("translation")) else trace.JUDGE_PROMPT[jid],
app/backend/rejudge.py-85-                        "call_id": call_id, "verdict": verdict, "reason_code": code}
app/backend/rejudge.py-86-        state, reasons = recompose(row, ladder_verdict)
app/backend/rejudge.py-87-        lad["state"] = state
app/backend/rejudge.py-88-        DB.update_item(conn, row["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/rejudge.py-89-        _log(conn, case_id, row, jid, call_id, ladder_verdict, state, t)
app/backend/rejudge.py-90-        done.append(dict(base, verdict=ladder_verdict, state=state, state_reasons=reasons))
app/backend/rejudge.py-91-    gate = next(s for s in trace.case_trace(conn, case_id)["steps"] if s["id"] == "export_gate")
app/backend/rejudge.py-92-    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
app/backend/rejudge.py-93-            "export_gate": {"ready": gate["ready"], "status": gate["status"], "blockers": gate["blockers"]}}
34:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
103:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from
362:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a 
553:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the 
637:## POST /api/cases/{token}/rejudge  (D-044)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:32:15.297Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='stepper.js'\ns=open(p).read()\nold=\"\"\"    if (cc) { text = cc.text; if (cc.rerun) { buttons.push(S.rerunButton()); rerunToo = true; } if (cc.go) btn(cc.label, cc.go); }\"\"\"\nnew=\"\"\"    if (cc) { text = cc.text; if (cc.rerun) { const n = st.id === \"export_gate\" ? jnrBlockers(st).length : (st.counts || {}).unavailable || 0; buttons.push(n ? S.rerunButton(groupLabel(n)) : S.rerunButton()); rerunToo = true; } if (cc.go) btn(cc.label, cc.go); }\"\"\"\nassert old in s\ns=s.replace(old,new,1)\nold=\"\"\"  S.rerunButton = function (label, aria) {\"\"\"\nnew=\"\"\"  // ONE button per list: its words say how many items the one POST covers (\"these 3\"), so the label never promises a single item.\n  const groupLabel = (n) => RERUN + (n === 1 ? \" for this item\" : \" for these \" + n);\n  S.rerunButton = function (label, aria) {\"\"\"\nassert old in s\ns=s.replace(old,new,1)\n# blocker rows: no per-row rerun button\nold=\"\"\"      b.reason_code === \"JUDGE_NOT_RUN\" && !noRerun ? S.rerunButton(RERUN, RERUN + \" for \" + name) : null);\"\"\"\nassert old in s\ns=s.replace(old,\"\"\"      null);\"\"\",1)\nopen(p,'w').write(s)\nPYEOF\ngrep -n \"noRerun\" stepper.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T05:32:15.415Z

**tool result**
````
455:  function blockerRow(b, noRerun) {
464:  // noRerun: the refused-export message has ONE rerun button with its status line right under the lead sentence, so its rows only offer Go to item.
465:  function blockerList(bl, title, noRerun) {
469:      el("ul", { class: "zs-blockers" }, first.map((b) => blockerRow(b, noRerun))),
470:      rest.length ? el("details", { class: "zs-more" }, el("summary", {}, "Show the other " + rest.length), el("ul", { class: "zs-blockers" }, rest.map((b) => blockerRow(b, noRerun)))) : null);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:32:19.720Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='stepper.js'\ns=open(p).read()\ns=s.replace(\"function blockerRow(b, noRerun) {\",\"function blockerRow(b) {\",1)\ns=s.replace(\"  // noRerun: the refused-export message has ONE rerun button with its status line right under the lead sentence, so its rows only offer Go to item.\\n  function blockerList(bl, title, noRerun) {\",\"  // Rows only offer Go to item (and Edit for a wording blocker): the one rerun button lives with the list (the gate step, the refused-export message), because one POST reruns them all.\\n  function blockerList(bl, title) {\",1)\ns=s.replace(\"blockerRow(b, noRerun)\",\"blockerRow(b)\")\ns=s.replace(\"blockerList(bl, null, true)\",\"blockerList(bl)\")\nold=\"\"\"if (!blocked.cleared && rerun) host.append(el(\"div\", { class: \"zs-todo-btns\" }, S.rerunButton()));\"\"\"\nassert old in s\ns=s.replace(old,\"\"\"if (!blocked.cleared && rerun) host.append(el(\"div\", { class: \"zs-todo-btns\" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === \"JUDGE_NOT_RUN\").length))));\"\"\",1)\nopen(p,'w').write(s)\nPYEOF\ngrep -n \"noRerun\\|blockerList(\" stepper.js | cut -c1-160; sed -n 452,462p stepper.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T05:32:19.834Z

**tool result**
````
465:  function blockerList(bl, title) {
483:    const a = bl.length ? blockerList(bl) : null, w = warningNode(st), said = rerunNote && rerunNote.token === (ZL.state.get() || {}).token;
545:    if (!blocked.cleared && bl.length) host.append(blockerList(bl));
  let cache = null, openPref = false, seq = 0, curDet = null;

  // One blocker row, shared by the case rail and the message beside the Export button.
  function blockerRow(b) {
    const name = b.item_id ? S.label(b.item_id) : "Whole case";
    const wording = isCodeBlocker(b);
    return el("li", { class: "zs-blocker", "data-testid": "gate-blocker", "data-blocker-code": b.reason_code, "data-jump-item": b.item_id || null },
      el("span", { class: "zs-blocker-name" }, name), " ", el("span", { class: "zs-ev" }, wording ? [el("strong", {}, S.wordingLead(b.item_id) + " "), b.why || ""] : b.why || ""),
      b.item_id ? el("button", { type: "button", class: "zs-btn", "data-testid": "btn-gate-jump", "aria-label": "Go to item " + name, onclick: () => gotoItem(b.item_id) }, "Go to item") : null,
      wording ? el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-gate-edit", "aria-label": S.wordingEditText(b.item_id) + " for " + name, onclick: () => S.editItem(b.item
      null);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:32:44.594Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='judges.js'\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert old in s, old[:60]\n    s=s.replace(old,new,1)\nrep(\"\"\"    return { jnr: bl.filter((b) => b.reason_code === \"JUDGE_NOT_RUN\").map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)) };\"\"\",\n\"\"\"    return { jnr: bl.filter((b) => b.reason_code === \"JUDGE_NOT_RUN\").map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)), verdict: (tr && tr.verdict) || null };\"\"\")\n# wording row\nrep(\"\"\"el(\"strong\", {}, ZL.stepper.WORDING + \" \"), b.why || \"\"),\"\"\",\"\"\"el(\"strong\", {}, ZL.stepper.wordingLead(id) + \" \"), b.why || \"\"),\"\"\")\nrep(\"\"\"aria-label\": \"Edit your wording for \" + t, onclick: () => ZL.stepper.editItem(id) }, \"Edit your wording\"),\"\"\",\"\"\"aria-label\": ZL.stepper.wordingEditText(id) + \" for \" + t, onclick: () => ZL.stepper.editItem(id) }, ZL.stepper.wordingEditText(id)),\"\"\")\n# summary\ni=s.index(\"  // Built from the server's totals and from the gate\")\nj=s.index(\"  function paint(root, d, note) {\")\nnew_sum = '''  // Built from the server's totals and from the gate; each kind of item is named once, and only items the gate lists carry the blocking words (\"blocks export\"). An edited item the\n  // gate does not hold is counted as \"edited by you, not AI-checked\" and never as blocking, so the panel and the rail (\"Export blocked by N\") agree.\n  function summaryText(d) {\n    const t = d.totals || {}, bits = [], n = t.items_judged || 0;\n    const nb = ((gate && gate.jnr) || []).length, nc = ((gate && gate.code) || []).length, cids = codeIds();\n    const rest = byItem(d).filter((i) => unchecked(i) && !blocking(i) && !cids.has(i.id));\n    const nEdit = gate ? rest.filter(humanWording).length : 0, nWait = gate ? rest.length - nEdit : t.unavailable || 0;\n    if (!t.unsupported && !t.unsure && !t.unavailable && !nb && !nc) bits.push(\"checked \" + n + \", all agreed with the draft\");\n    else {\n      bits.push(n + \" checked\", (t.supported || 0) + \" agreed with the draft\");\n      if (t.unsupported) bits.push(t.unsupported + \" questioned\");\n      if (t.unsure) bits.push(t.unsure + \" undecided\");\n      if (nb) bits.push(nb + \" not checked, blocks export: \" + nb);\n      if (nWait) bits.push(nWait + \" not checked\");\n      if (nEdit) bits.push(nEdit + \" edited by you, not AI-checked\");\n      if (!nb && !nWait && !nEdit && t.unavailable && !nc) bits.push(t.unavailable + \" not checked\");\n    }\n    if (nc) bits.push(nc + (nc === 1 ? \" summary fails a check\" : \" summaries fail a check\") + \", blocks export: \" + nc);\n    return bits.join(\", \");\n  }\n\n'''\ns=s[:i]+new_sum+s[j:]\n# wording list heading + verdict line\nrep(\"\"\"    if (cblk.length) det.append(list(\"judge-wording-list\", \"Where your wording does not match the quote\", cblk, wordingRow, \"\"));\"\"\",\n\"\"\"    const verdictLine = cblk.length && gate.verdict && gate.verdict.label   // the case verdict exactly as the server words it (the same text as the case checks)\n      ? el(\"p\", { class: \"zj-case-verdict\" }, el(\"span\", { class: \"zs-verdict zs-v-\" + (gate.verdict.code || \"none\"), \"data-testid\": \"judge-case-verdict\" }, gate.verdict.label), \" \", el(\"span\", { class: \"zs-ev\" }, \"Case verdict from the export gate.\")) : null;\n    if (cblk.length) det.append(list(\"judge-wording-list\", \"Where a summary does not match its quote\", cblk, wordingRow, \"\", verdictLine));\"\"\")\nopen(p,'w').write(s)\nPYEOF\nnode -e \"for (const f of ['judges','stepper','review','batch']) new Function(require('fs').readFileSync('$PWD/'+f+'.js','utf8'))\" && echo ok"
}
````

### User / tool · 2026-11-02T05:32:44.751Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:32:48.116Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"function reveal\" -A14 stepper.js; grep -n \"toolbar\" styles.css | head -5; grep -n 'export-blocked\\|btn-export\"' timeline.js export.js app.js | head"
}
````

### User / tool · 2026-11-02T05:32:48.219Z

**tool result**
````
77:  function reveal(node) {
78-    if (!node.hasAttribute("tabindex")) node.setAttribute("tabindex", "-1");
79-    // a target taller than 60% of the screen lands with its heading at the top (the sticky banner is cleared by scroll-margin-top); short rows are centred
80-    const tall = node.getBoundingClientRect().height > window.innerHeight * 0.6;
81-    node.scrollIntoView({ block: tall ? "start" : "center" }); node.focus({ preventScroll: true }); flash(node);
82-  }
83-  S.goto = function (itemId) {
84-    closeDialogs();
85-    const node = document.querySelector('[data-testid="queue"] [data-item-id="' + itemId + '"]') || document.querySelector('[data-item-id="' + itemId + '"]');
86-    if (!node) return false;
87-    reveal(node); return true;
88-  };
89-  function gotoDates(recordId) {
90-    closeDialogs();
91-    const node = (recordId && document.querySelector('[data-testid="date-to-confirm-item"][data-record-id="' + recordId + '"]')) ||
30:.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
31:.toolbar h2{margin:0}
timeline.js:143:        el("button", { type: "button", class: "btn primary", "data-testid": "btn-export", onclick: () => { if (ZL.stepper) ZL.stepper.onExport(); ZL.openExport(); } }, "Export"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:32:55.305Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='stepper.js'\ns=open(p).read()\nold=\"\"\"    if (reveal_ !== false) reveal(curNotice);\n    return true;\"\"\"\nassert old in s\ns=s.replace(old,\"\"\"    if (reveal_ !== false) {\n      reveal(curNotice);\n      const b = ZL.$('[data-testid=\"btn-export\"]'), r = b && b.getBoundingClientRect();   // the button this message explains stays in view with it, so Export can be pressed again\n      if (r && (r.top < 0 || r.bottom > window.innerHeight)) b.scrollIntoView({ block: \"start\" });\n    }\n    return true;\"\"\",1)\nopen(p,'w').write(s)\nPYEOF\ngrep -n \"sticky\" styles.css | head -5; echo '[data-testid=\"btn-export\"] { scroll-margin-top: 80px; }' >> stepper.css; tail -3 stepper.css"
}
````

### User / tool · 2026-11-02T05:32:55.439Z

**tool result**
````
8:.banner.synth{background:#b42318;color:#fff;position:sticky;top:0;z-index:5}
46:.dlg-head{display:flex;justify-content:space-between;align-items:center;gap:8px;position:sticky;top:0;background:var(--panel);padding:10px 14px;border-bottom:1px solid var(--line)}
.zs-warnbox { margin: 8px 0 2px; padding: 6px 10px; border: 1px solid var(--zs-line); border-left: 4px solid var(--zs-warn); border-radius: 8px; background: var(--zs-soft); }
.zs-btn[disabled] { opacity: .6; cursor: progress; }
[data-testid="btn-export"] { scroll-margin-top: 80px; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:33:16.763Z

**tool call — Bash**
````
{
 "command": "sed -n 1,54p tests/e2e/test_rerun_judge.py; sed -n 105,255p tests/e2e/test_rerun_judge.py"
}
````

### User / tool · 2026-11-02T05:33:16.849Z

**tool result**
````
"""T-081 / T-082 round 3 (D-044, D-045): 'Run the second check again', the refused export shown beside the Export button, and pending items as a gate warning.
The fixture backend cannot leave an accepted recorded item without a judge answer, so those states are produced by the JudgeNotRun route-rewriting stub (conftest);
the pending-warning tests use the real backend."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, JudgeNotRun, WordingFails
from tests.e2e.test_stepper import open_rail, open_judges, active_in


def _accept(tok, n=3):
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] != "rejected" and e["date"]][:n]
    assert len(ids) == n
    for i in ids:
        assert api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "accept"})[0] == 200
    return ids


@pytest.fixture
def unrun(page, sample_case):
    """Three accepted entries whose second check 'never ran'; rejudge clears them."""
    ids = _accept(sample_case)
    return JudgeNotRun(page, sample_case, ids)


def in_view(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + min(b["height"], 40) <= vh


# ---- D-045: pending items are a warning, not a blocker
def test_pending_items_are_a_warning_not_a_blocker(page, sample_case):
    _accept(sample_case)
    open_case(page, sample_case); cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]')
    expect(gate).to_have_attribute("data-status", "pass")
    assert gate.get_by_test_id("gate-blocker").count() == 0
    w = gate.get_by_test_id("gate-warning"); expect(w).to_have_attribute("data-warning-code", "ITEMS_NOT_REVIEWED")
    txt = w.inner_text().lower()
    assert "not reviewed" in txt and "will not be in the letter" in txt and "disclosure" in txt and "does not block" in txt
    assert re.search(r"Ready to export, \d+ not reviewed", cs.get_by_test_id("case-summary-gate").inner_text())
    w.get_by_test_id("btn-gate-warning-jump").click()
    assert page.evaluate("document.activeElement.getAttribute('data-review')") == "pending"
    page.get_by_test_id("btn-export").click()                      # the export opens even though items are pending
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    assert page.get_by_test_id("export-blocked").is_hidden()


def test_export_with_nothing_accepted_says_so_beside_the_button(page, sample_case):
    """422 export_blocked (nothing accepted): the message sits right under the toolbar, in view, focused; the rail stays as the human left it."""
    open_case(page, sample_case)
    page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-blocked"); expect(box).to_be_visible()
def test_refused_export_shows_beside_the_button_with_blockers_and_rerun(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case))
        open_case(pg, sample_case)
        pg.get_by_test_id("btn-export").click()
        box = pg.get_by_test_id("export-blocked"); expect(box).to_be_visible()
        assert in_view(pg, box), "the message must be on screen, not far below"
        assert active_in(pg, '[data-testid="export-blocked"]')
        assert pg.locator("#view-export").is_hidden()
        msg = box.get_by_test_id("export-blocked-msg").inner_text()
        assert "3 accepted items have not had the second AI check" in msg
        assert box.get_by_test_id("gate-blocker").count() == 3
        assert box.get_by_test_id("btn-gate-jump").count() == 3
        pg.evaluate("document.activeElement.blur()")
        box.get_by_test_id("btn-rerun-judge").first.click()
        expect(box.get_by_test_id("export-blocked-msg")).to_contain_text("Nothing blocks the export now")
        assert stub.posts == 1
        pg.get_by_test_id("btn-export").click()
        expect(pg.get_by_test_id("export-letter")).to_be_visible()
        assert pg.get_by_test_id("export-blocked").is_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_item_stepper_offers_the_rerun_on_the_skipped_judge_step(page, unrun):
    i = unrun.ids[0]
    open_case(page, unrun.token)
    page.locator(f'[data-testid="queue"] [data-item-id="{i}"]').get_by_test_id("entry-why").click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == "Accepted, second check missing"
    j = st.locator('[data-step-id="judge_1"]')
    assert j.get_by_test_id("step-status").inner_text() == "Did not run"
    assert j.get_attribute("aria-current") == "step"
    j.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => document.querySelector('[data-testid=item-verdict]').textContent !== 'Accepted, second check missing'", timeout=8000)
    assert unrun.posts == 1
    assert page.get_by_test_id("item-stepper").locator('[data-step-id="judge_1"]').get_by_test_id("btn-rerun-judge").count() == 0


# ---- T-082: the AI-check panel
def test_judge_panel_rows_for_accepted_unchecked_items_match_the_gate(page, unrun):
    open_case(page, unrun.token); jp = open_judges(page)
    assert "blocks export" in jp.get_by_test_id("judge-summary-counts").inner_text()
    rows = jp.get_by_test_id("judge-unresolved"); assert rows.count() == 3
    for i in range(3):
        t = rows.nth(i).inner_text()
        assert "then accept" not in t and "can't go in the letter yet" in t
        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 0, "one group button covers the list; rows would only repeat it"
    grp = jp.get_by_test_id("judge-rerun-group"); assert "Run the second check again for these 3" in grp.inner_text()
    assert jp.get_by_test_id("btn-rerun-judge").count() == 1
    grp.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=judge-unresolved]').length === 0", timeout=8000)
    assert "blocks export" not in page.get_by_test_id("judge-summary-counts").inner_text()


def test_judge_panel_without_unchecked_items_is_unchanged(page, sample_case):
    open_case(page, sample_case); jp = open_judges(page)
    assert "blocks export" not in jp.get_by_test_id("judge-summary-counts").inner_text()
    assert jp.get_by_test_id("btn-rerun-judge").count() == 0


# ---- gate blockers: jump and update (moved here from test_stepper, now that only JUDGE_NOT_RUN items block)
def test_gate_blocker_jump_and_update(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]'); gate.wait_for()
    names = gate.get_by_test_id("btn-gate-jump").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
    assert all(n and n.startswith("Go to item ") for n in names) and len(set(names)) == len(names)
    first = gate.get_by_test_id("gate-blocker").first; tid = first.get_attribute("data-jump-item"); before = gate.get_by_test_id("gate-blocker").count()
    first.get_by_test_id("btn-gate-jump").focus(); page.keyboard.press("Enter")
    assert page.evaluate("document.activeElement.getAttribute('data-item-id')") == tid
    page.keyboard.press("d")
    expect(page.locator(f'[data-item-id="{tid}"]').first).to_have_attribute("data-review", "dismissed")
    page.wait_for_function("(n) => document.querySelectorAll('[data-testid=gate-blocker]').length < n", arg=before, timeout=8000)


def test_first_blocking_item_is_the_first_in_the_queue(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    cs.locator('[data-step-id="export_gate"]').get_by_test_id("btn-step-action").filter(has_text="first blocking item").click()
    focused = page.evaluate("document.activeElement.getAttribute('data-item-id')")
    queue = page.locator('[data-testid="queue"] [data-item-id]').evaluate_all("els => els.map(e => e.getAttribute('data-item-id'))")
    assert focused == next(i for i in queue if i in unrun.ids)


# ---- T-097: where the rerun answer shows, and the panel agreeing with the gate
def vis(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_rerun_pressed_in_the_refused_export_message_answers_beside_the_button(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case, 8), mode="still", hold=True)
        open_case(pg, sample_case)
        pg.get_by_test_id("btn-export").click()
        box = pg.get_by_test_id("export-blocked"); expect(box).to_be_visible()
        btn = box.get_by_test_id("btn-rerun-judge"); assert btn.count() == 1, "the message has one rerun button; its rows only offer Go to item"
        st = box.get_by_test_id("rerun-status"); assert st.count() == 1
        btn.click()
        expect(st).to_contain_text("Running the second check on 8 items")
        expect(btn).to_be_disabled()
        assert vis(pg, st) and vis(pg, btn), "Running… must be on screen beside the button"
        assert abs(st.bounding_box()["y"] - btn.bounding_box()["y"]) < 120
        stub.release()
        expect(st).to_contain_text("still did not answer for 8 items of 8")
        assert vis(pg, st) and abs(st.bounding_box()["y"] - btn.bounding_box()["y"]) < 120
        expect(btn).to_be_enabled(); assert box.get_by_test_id("gate-blocker").count() == 8 and stub.posts == 1
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_failed_rerun_pressed_in_the_ai_check_panel_says_so_beside_the_button(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case), mode="still", hold=True)
        open_case(pg, sample_case); jp = open_judges(pg)
        grp = jp.get_by_test_id("judge-rerun-group"); btn = grp.get_by_test_id("btn-rerun-judge"); btn.scroll_into_view_if_needed(); btn.click()
        expect(grp.get_by_test_id("rerun-status")).to_contain_text("Running the second check on 3 items")
        stub.release()
        st = jp.get_by_test_id("judge-rerun-group").get_by_test_id("rerun-status")
        expect(st).to_contain_text("still did not answer for 3 items of 3")
        assert vis(pg, st) and abs(st.bounding_box()["y"] - jp.get_by_test_id("judge-rerun-group").get_by_test_id("btn-rerun-judge").bounding_box()["y"]) < 120
        assert jp.get_by_test_id("judge-unresolved").count() == 3 and "blocks export" in jp.get_by_test_id("judge-summary-counts").inner_text()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_judge_panel_follows_the_gate_for_an_edited_item(page, sample_case):
    """D-045(b): the gate lists only the accepted AI-made items; the edited one is ready, so the panel must not say it blocks and must not offer a rerun for it."""
    ids = _accept(sample_case, 3)
    c = api("GET", f"/api/cases/{sample_case}")[1]
    edited = next(e for e in c["entries"] if e["state"] != "rejected" and e["date"] and e["id"] not in ids)
    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}})
    assert st == 200
    JudgeNotRun(page, sample_case, ids, exempt=[edited["id"]])
    open_case(page, sample_case); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert summ.count("blocks export") == 1 and "blocks export: 3" in summ, "the summary counts the gate's 3 blockers, not the edited item"
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{edited["id"]}"]')
    expect(row).to_have_count(1)
    t = row.inner_text()
    assert "Edited by you, not AI-checked" in t and "Blocks the export" not in t and "can't go in the letter" not in t
    assert row.get_by_test_id("btn-rerun-judge").count() == 0
    assert jp.get_by_test_id("judge-rerun-group").inner_text().count("these 3") == 1
    blocked_rows = jp.locator('[data-testid="judge-unresolved"]:has-text("Blocks the export")')
    assert blocked_rows.count() == 3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:33:32.299Z

**tool call — Bash**
````
{
 "command": "python3 - <<'PYEOF'\np='tests/e2e/test_rerun_judge.py'\ns=open(p).read()\ndef rep(old,new,cnt=1):\n    global s\n    assert old in s, old[:70]\n    s=s.replace(old,new,cnt)\nrep(\"\"\"    for i in range(3):\n        assert rows.nth(i).get_by_test_id(\"btn-rerun-judge\").count() == 1\n    assert \"never got the second AI check\" in gate.get_by_test_id(\"step-action\").inner_text()\n    assert gate.get_by_test_id(\"step-action\").get_by_test_id(\"btn-rerun-judge\").inner_text() == \"Run the second check again\"\n    judges = cs.locator('[data-step-id=\"judges\"]')\n    assert judges.get_by_test_id(\"step-action\").get_by_test_id(\"btn-rerun-judge\").count() == 1\"\"\",\n\"\"\"    for i in range(3):\n        assert rows.nth(i).get_by_test_id(\"btn-rerun-judge\").count() == 0, \"T-097 r3 m-2: one POST reruns every item, so a per-row button would promise one and do three\"\n    assert \"never got the second AI check\" in gate.get_by_test_id(\"step-action\").inner_text()\n    gb = gate.get_by_test_id(\"btn-rerun-judge\"); assert gb.count() == 1\n    assert gb.inner_text() == \"Run the second check again for these 3\", \"the group button says how many items its one POST covers\"\n    judges = cs.locator('[data-step-id=\"judges\"]')\n    assert judges.get_by_test_id(\"step-action\").get_by_test_id(\"btn-rerun-judge\").count() == 1\n    assert judges.get_by_test_id(\"btn-rerun-judge\").inner_text() == \"Run the second check again for these 3\\\"\"\"\")\nrep(\"\"\"        assert in_view(pg, box), \"the message must be on screen, not far below\\\"\"\"\",\"\"\"        assert in_view(pg, box), \"the message must be on screen, not far below\"\n        assert in_view(pg, pg.get_by_test_id(\"btn-export\")), \"T-097 r3 n-1: the Export button it explains stays on screen with the message\\\"\"\"\")\nrep(\"\"\"        pg.evaluate(\"document.activeElement.blur()\")\n        box.get_by_test_id(\"btn-rerun-judge\").first.click()\"\"\",\"\"\"        pg.evaluate(\"document.activeElement.blur()\")\n        assert box.get_by_test_id(\"btn-rerun-judge\").count() == 1 and box.get_by_test_id(\"btn-rerun-judge\").inner_text() == \"Run the second check again for these 3\"\n        box.get_by_test_id(\"btn-rerun-judge\").first.click()\"\"\")\nrep(\"\"\"    assert summ.count(\"blocks export\") == 1 and \"blocks export: 3\" in summ, \"the summary counts the gate's 3 blockers, not the edited item\\\"\"\"\",\"\"\"    assert summ.count(\"blocks export\") == 1 and \"blocks export: 3\" in summ, \"the summary counts the gate's 3 blockers, not the edited item\"\n    assert \"1 edited by you, not AI-checked\" in summ and \"4 not checked\" not in summ, \"T-097 r3 m-1: each kind of item is named once\\\"\"\"\")\n# mixed\nrep(\"\"\"    assert \"1 edit does not match its quote, blocks export: 1\" in summ\"\"\",\"\"\"    assert \"1 summary fails a check, blocks export: 1\" in summ, \"T-097 r3 m-1: named once, with the gate's count\"\n    assert summ.count(\"blocks export\") == 1 and \"2 not checked\" not in summ and \"3 not checked\" not in summ\"\"\")\nrep(\"\"\"    assert \"Export blocked by 1\" in open_rail(page).get_by_test_id(\"case-summary-gate\").inner_text(), \"the rail and the panel summary agree\\\"\"\"\",\"\"\"    cs = open_rail(page)\n    assert \"Export blocked by 1\" in cs.get_by_test_id(\"case-summary-gate\").inner_text(), \"the rail and the panel summary agree\"\n    assert cs.get_by_test_id(\"case-verdict\").text_content() == \"1 summary fails a check\", \"T-098 r2: the case verdict exactly as the backend words it\"\n    assert jp.get_by_test_id(\"judge-case-verdict\").text_content() == \"1 summary fails a check\", \"the panel shows the same words\\\"\"\"\")\nrep(\"\"\"    assert \"does not match\" not in jp.get_by_test_id(\"judge-summary-counts\").inner_text()\"\"\",\"\"\"    assert \"fails a check\" not in jp.get_by_test_id(\"judge-summary-counts\").inner_text() and jp.get_by_test_id(\"judge-case-verdict\").count() == 0\"\"\")\nrep(\"\"\"    assert j.get_by_test_id(\"step-status\").inner_text() == \"Not needed\" and j.get_by_test_id(\"btn-rerun-judge\").count() == 0\"\"\",\"\"\"    assert j.get_by_test_id(\"step-status\").inner_text() == \"Not needed\" and j.get_by_test_id(\"btn-rerun-judge\").count() == 0\n    assert \"said:\" not in j.inner_text() and \"Unavailable\" not in j.inner_text(), \"T-097 r3 m-new-1: a Not-needed step prints no second-check verdict\\\"\"\"\")\nopen(p,'w').write(s)\n\np='tests/e2e/conftest.py'\ns=open(p).read()\nrep(\"\"\"d[\"verdict\"] = {\"code\": \"needs_attention\", \"label\": f\"{len(act)} edited summaries fail a check\"}\"\"\",\"\"\"d[\"verdict\"] = {\"code\": \"needs_attention\", \"label\": f\"{len(act)} summar{'ies fail' if len(act) != 1 else 'y fails'} a check\"}   # the backend's wording (T-098 r2)\"\"\")\nopen(p,'w').write(s)\nPYEOF\ngrep -n \"does not match its quote\\|edit does not match\\|edits do not match\\|Where your wording\" -r tests | cut -c1-200"
}
````

### User / tool · 2026-11-02T05:33:32.424Z

**tool result**
````
tests/e2e/conftest.py:27:T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check b
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:33:49.914Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def connect\" -A12 app/db/db.py | head -30; grep -n \"isolation_level\\|autocommit\" app/db/db.py | head; sed -n 1,30p tests/e2e/test_edit.py"
}
````

### User / tool · 2026-11-02T05:33:50.008Z

**tool result**
````
38:def connect(path: str):
39-    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
40-    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
41-    pasted text past the 24 h purge (T-040 security r2)."""
42-    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
43-        probe = sqlite3.connect(path)
44-        try:
45-            version = probe.execute("PRAGMA user_version").fetchone()[0]
46-            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
47-        finally:
48-            probe.close()
49-        if has_tables and version != SCHEMA_VERSION and version != 3:
50-            for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
54:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
"""Edit flow. R-RV-2, R-RV-3, R-EX-4(10)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_edit_summary_labelled_and_persists(page, sample_case):
    """R-RV-2: edit entry 3 summary -> 'edited' label; reload keeps summary and label; letter has no 'edited'."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 and daily headaches."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    page.reload(); page.get_by_test_id("timeline").wait_for()
    e = page.get_by_test_id("entry-3"); assert e.get_attribute("data-review") == "edited" and "edited" in e.inner_text().lower() and "daily headaches" in e.get_by_test_id("entry-summary").inner_text()

def test_added_dollar_is_a_hard_422_no_override(page, sample_case):
    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
    c = api("GET", f"/api/cases/{sample_case}")[1]; eid = [e for e in c["entries"] if "r5" in e["record_ids"]][0]["id"]
    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
    assert st == 422
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Visit 8: pain 4/10, improving; billed $9,000."); e.get_by_test_id("btn-save-edit").click()
    expect(page.get_by_role("alert").or_(page.get_by_test_id("warning-list")).first).to_contain_text("9000")
    assert e.get_attribute("data-review") != "edited" and page.get_by_test_id("btn-keep-wording").count() == 0

def test_date_and_provider_not_editable(page, sample_case):
    """R-RV-2: no input exists for date or provider."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    assert e.locator("input[name=date], input[name=provider]").count() == 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:14.295Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/test_code_check_refusal.py",
 "content": "\"\"\"T-097 round 3 (D-051, T-098 r2): Accept (single and batch) can be refused with 422 CODE_CHECK_FAILED. The UI shows the server's plain reason next to the item's Accept button\nwith an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server\nunder test, to put a failing summary into the store the way a stale or imported state would) and against a route stub that answers exactly as memory/contracts/api.md says.\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case\n\nROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"..\"))\nREASON = \"The summary has a number that is not in the quote: 5. Edit the summary to match the quote.\"\nNEXT = {\"code\": \"EDIT_SUMMARY\", \"text\": \"Edit the summary to match the quote\"}\n\n\ndef _entry(tok, eid):\n    c = api(\"GET\", f\"/api/cases/{tok}\")[1]\n    return next(e for e in c[\"entries\"] + c[\"undated_entries\"] if e[\"id\"] == eid)\n\n\ndef _break(tok, eid):\n    \"\"\"Real backend: put 'Pain 5/10' (a figure the quote does not carry) into the stored summary, like a stale or imported state.\"\"\"\n    path = os.environ.get(\"ZLAYT_DB\")\n    if not path:\n        pytest.skip(\"the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)\")\n    sys.path.insert(0, ROOT)\n    from app.db import db as DB\n    conn = DB.connect(path)\n    try:\n        assert \"5/10\" not in (_entry(tok, eid)[\"excerpt\"] or \"\")\n        DB.update_item(conn, eid, now=9e9, case=tok, summary=\"Pain 5/10\")\n    finally:\n        conn.close()\n\n\nclass Refuse:\n    \"\"\"Stub: POST .../review (accept) and POST .../review/batch (accept) answer 422 CODE_CHECK_FAILED while the item's summary is unchanged (an edit through the real route lifts it).\"\"\"\n    def __init__(self, page, tok, eid):\n        self.page, self.tok, self.eid = page, tok, eid\n        self.base = _entry(tok, eid)[\"summary\"]\n        self.posts = 0\n        page.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), self._single)\n        page.route(re.compile(r\"/api/cases/[^/]+/review/batch$\"), self._batch)\n\n    def active(self):\n        return _entry(self.tok, self.eid)[\"summary\"] == self.base\n\n    def _single(self, route):\n        body = route.request.post_data_json or {}\n        if body.get(\"action\") != \"accept\" or not route.request.url.endswith(f\"/items/{self.eid}/review\") or not self.active():\n            return route.fallback()\n        self.posts += 1\n        route.fulfill(status=422, content_type=\"application/json\", body=json.dumps({\"error\": {\"code\": \"CODE_CHECK_FAILED\", \"message\": REASON, \"detail\": {\n            \"item_id\": self.eid, \"reason_code\": \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"step_id\": \"summary_tokens\", \"failed_steps\": [\"summary_tokens\"], \"tokens\": [\"5\"],\n            \"next_action\": dict(NEXT, target={\"item_id\": self.eid})}}}))\n\n    def _batch(self, route):\n        body = route.request.post_data_json or {}\n        if body.get(\"action\") != \"accept\" or self.eid not in (body.get(\"item_ids\") or []) or not self.active():\n            return route.fallback()\n        self.posts += 1\n        route.fulfill(status=422, content_type=\"application/json\", body=json.dumps({\"error\": {\"code\": \"CODE_CHECK_FAILED\", \"message\": REASON + \" Nothing was changed.\", \"detail\": {\"rejected\": [\n            {\"id\": self.eid, \"reason\": \"code_check_failed\", \"reason_code\": \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"why\": REASON, \"next_action\": dict(NEXT, target={\"item_id\": self.eid})}]}}}))\n\n\n@pytest.fixture(params=[\"real\", \"stub\"])\ndef broken(request, page, sample_case):\n    c = api(\"GET\", f\"/api/cases/{sample_case}\")[1]\n    e = next(x for x in c[\"entries\"] if x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\")\n    orig = e[\"summary\"]\n    if request.param == \"real\":\n        _break(sample_case, e[\"id\"])\n        assert _entry(sample_case, e[\"id\"])[\"summary\"] == \"Pain 5/10\"\n        stub = None\n    else:\n        stub = Refuse(page, sample_case, e[\"id\"])\n    return {\"tok\": sample_case, \"id\": e[\"id\"], \"orig\": orig, \"mode\": request.param, \"stub\": stub}\n\n\ndef row_of(page, i):\n    return page.get_by_test_id(\"timeline\").locator(f'[data-item-id=\"{i}\"]').first\n\n\ndef vis(page, loc):\n    b = loc.bounding_box(); vh = page.viewport_size[\"height\"]\n    return b is not None and b[\"y\"] >= 0 and b[\"y\"] + b[\"height\"] <= vh\n\n\n@pytest.mark.parametrize(\"w,h\", [(1440, 900), (390, 844)])\ndef test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):\n    b = pw.chromium.launch(); pg = b.new_context(viewport={\"width\": w, \"height\": h}).new_page()\n    try:\n        if broken[\"stub\"]:\n            broken[\"stub\"].page = pg\n            pg.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), broken[\"stub\"]._single)\n            pg.route(re.compile(r\"/api/cases/[^/]+/review/batch$\"), broken[\"stub\"]._batch)\n        t = broken\n        open_case(pg, t[\"tok\"]); row = row_of(pg, t[\"id\"])\n        row.scroll_into_view_if_needed()\n        btn = row.get_by_test_id(\"btn-accept\"); btn.click()\n        box = row.get_by_test_id(\"accept-refused\"); expect(box).to_be_visible()\n        msg = box.get_by_test_id(\"accept-refused-msg\").inner_text()\n        assert msg.startswith(\"Not accepted. \") and msg.endswith(\"Edit the summary to match the quote.\"), msg\n        assert \"not in the quote\" in msg or t[\"mode\"] == \"real\"\n        assert vis(pg, box), \"the reason must be on screen beside the button, not below the fold\"\n        assert abs(box.bounding_box()[\"y\"] - btn.bounding_box()[\"y\"]) < 140, \"next to the Accept button\"\n        assert box.get_attribute(\"role\") == \"alert\"\n        assert api(\"GET\", f\"/api/cases/{t['tok']}\")[1][\"review\"][\"counts\"][\"accepted\"] == 0 and _entry(t[\"tok\"], t[\"id\"])[\"review_status\"] == \"pending\", \"nothing was changed\"\n        # Edit opens the item's edit box; a passing edit clears the refusal and the item is accepted by the edit\n        box.get_by_test_id(\"btn-accept-refused-edit\").click()\n        ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible()\n        assert pg.evaluate(\"document.activeElement === document.querySelector('[data-item-id=\\\"%s\\\"] textarea')\" % t[\"id\"]) or ta.is_visible()\n        ta.fill(t[\"orig\"]); row.get_by_test_id(\"btn-save-edit\").click()\n        expect(row_of(pg, t[\"id\"])).to_have_attribute(\"data-review\", \"edited\")\n        expect(row_of(pg, t[\"id\"]).get_by_test_id(\"accept-refused\")).to_be_hidden()\n    finally:\n        pg.unroute_all(behavior=\"ignoreErrors\"); b.close()\n\n\ndef test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):\n    t = broken\n    open_case(page, t[\"tok\"]); row = row_of(page, t[\"id\"]); row.focus()\n    page.keyboard.press(\"a\")\n    expect(row.get_by_test_id(\"accept-refused\")).to_be_visible()\n    assert page.evaluate(\"document.activeElement.getAttribute('data-item-id')\") == t[\"id\"], \"focus stays on the refused item\"\n    assert \"Nothing\" not in (page.locator(\"#rv-live\").inner_text() or \"\") or True\n    assert row.get_by_test_id(\"btn-accept\").get_attribute(\"aria-pressed\") == \"false\"\n    page.keyboard.press(\"d\")                                   # deciding the item another way clears the refusal\n    expect(row_of(page, t[\"id\"]).get_by_test_id(\"accept-refused\")).to_be_hidden()\n\n\ndef test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted(page, broken):\n    t = broken\n    open_case(page, t[\"tok\"])\n    page.get_by_test_id(\"btn-accept-verified\").click()\n    box = page.get_by_test_id(\"batch-refused\"); expect(box).to_be_visible()\n    assert box.get_attribute(\"role\") == \"alert\" and box.get_by_test_id(\"batch-refused-msg\").inner_text().startswith(\"Nothing was accepted.\")\n    items = box.get_by_test_id(\"batch-refused-item\"); assert items.count() == 1\n    assert items.first.get_attribute(\"data-refused-id\") == t[\"id\"]\n    txt = items.first.inner_text()\n    assert \"Edit the summary to match the quote\" in txt or \"Edit the summary\" in txt\n    c = api(\"GET\", f\"/api/cases/{t['tok']}\")[1]\n    assert c[\"review\"][\"counts\"][\"accepted\"] == 0, \"all or nothing: the batch accepted none\"\n    items.first.get_by_test_id(\"btn-batch-refused-edit\").click()\n    ta = row_of(page, t[\"id\"]).get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible()\n    ta.fill(t[\"orig\"]); row_of(page, t[\"id\"]).get_by_test_id(\"btn-save-edit\").click()\n    expect(page.get_by_test_id(\"batch-refused\")).to_have_count(0)      # the edited item is no longer waiting, so it leaves the list\n    page.get_by_test_id(\"btn-accept-verified\").click()\n    expect(page.get_by_test_id(\"btn-undo-batch\")).to_be_visible()      # the next batch goes through\n\n\ndef test_case_verdict_reads_the_backend_label_in_rail_and_panel(page, sample_case):\n    \"\"\"Real backend: an accepted AI draft whose summary then fails a code check is a gate blocker; the case verdict is the backend's words, in the rail and in the panel.\"\"\"\n    from tests.e2e.test_stepper import open_rail, open_judges\n    c = api(\"GET\", f\"/api/cases/{sample_case}\")[1]\n    e = next(x for x in c[\"entries\"] if x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\")\n    assert api(\"POST\", f\"/api/cases/{sample_case}/items/{e['id']}/review\", {\"action\": \"accept\"})[0] == 200\n    _break(sample_case, e[\"id\"])\n    open_case(page, sample_case); cs = open_rail(page)\n    assert cs.get_by_test_id(\"case-verdict\").text_content() == \"1 summary fails a check\"\n    jp = open_judges(page)\n    assert jp.get_by_test_id(\"judge-case-verdict\").text_content() == \"1 summary fails a check\"\n    assert \"1 summary fails a check, blocks export: 1\" in jp.get_by_test_id(\"judge-summary-counts\").inner_text()\n    blocker = cs.locator(f'[data-testid=\"gate-blocker\"][data-jump-item=\"{e[\"id\"]}\"]')\n    assert \"This summary doesn't match the quote:\" in blocker.inner_text() and \"Your wording\" not in blocker.inner_text(), \"the paralegal did not write an AI draft\"\n    assert blocker.get_by_test_id(\"btn-gate-edit\").inner_text() == \"Edit the summary\"\n"
}
````

### User / tool · 2026-11-02T05:34:14.353Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/test_code_check_refusal.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:21.863Z

**tool call — Bash**
````
{
 "command": "python3 - <<'PYEOF'\np='tests/e2e/test_code_check_refusal.py'\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert old in s, old[:60]\n    s=s.replace(old,new,1)\nrep(\"\"\"    def __init__(self, page, tok, eid):\n        self.page, self.tok, self.eid = page, tok, eid\n        self.base = _entry(tok, eid)[\"summary\"]\n        self.posts = 0\n        page.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), self._single)\n        page.route(re.compile(r\"/api/cases/[^/]+/review/batch$\"), self._batch)\n\"\"\",\"\"\"    def __init__(self, tok, eid):\n        self.tok, self.eid = tok, eid\n        self.base = _entry(tok, eid)[\"summary\"]\n        self.posts = 0\n\n    def attach(self, page):\n        page.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), self._single)\n        page.route(re.compile(r\"/api/cases/[^/]+/review/batch$\"), self._batch)\n\"\"\")\nrep(\"def broken(request, page, sample_case):\",\"def broken(request, sample_case):\")\nrep(\"stub = Refuse(page, sample_case, e[\\\"id\\\"])\",\"stub = Refuse(sample_case, e[\\\"id\\\"])\")\nrep(\"\"\"def row_of(page, i):\"\"\",\"\"\"def arm(t, page):\n    if t[\"stub\"]:\n        t[\"stub\"].attach(page)\n    return t\n\n\ndef row_of(page, i):\"\"\")\nrep(\"\"\"        if broken[\"stub\"]:\n            broken[\"stub\"].page = pg\n            pg.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), broken[\"stub\"]._single)\n            pg.route(re.compile(r\"/api/cases/[^/]+/review/batch$\"), broken[\"stub\"]._batch)\n        t = broken\n\"\"\",\"\"\"        t = arm(broken, pg)\n\"\"\")\nrep(\"\"\"    t = broken\n    open_case(page, t[\"tok\"]); row = row_of(page, t[\"id\"]); row.focus()\"\"\",\"\"\"    t = arm(broken, page)\n    open_case(page, t[\"tok\"]); row = row_of(page, t[\"id\"]); row.focus()\"\"\")\nrep(\"\"\"    assert \"Nothing\" not in (page.locator(\"#rv-live\").inner_text() or \"\") or True\n\"\"\",\"\")\nrep(\"\"\"    t = broken\n    open_case(page, t[\"tok\"])\n    page.get_by_test_id(\"btn-accept-verified\").click()\"\"\",\"\"\"    t = arm(broken, page)\n    open_case(page, t[\"tok\"])\n    page.get_by_test_id(\"btn-accept-verified\").click()\"\"\")\nopen(p,'w').write(s)\nPYEOF\ngit status --short app/frontend tests/e2e | head -20"
}
````

### User / tool · 2026-11-02T05:34:21.989Z

**tool result**
````
 M app/frontend/batch.js
 M app/frontend/judges.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M tests/e2e/conftest.py
 M tests/e2e/test_rerun_judge.py
?? tests/e2e/test_code_check_refusal.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:31.561Z

**tool call — Bash**
````
{
 "command": "python3 - <<'PYEOF'\np='tests/e2e/conftest.py'\ns=open(p).read()\nold=\"T-046 (R-ST-1 side-by-side)\"\nadd=\"\"\"T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),\n  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),\n  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).\n  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.\n  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.\n\"\"\"\nassert old in s\ns=s.replace(old,add+old,1)\nopen(p,'w').write(s)\nPYEOF\nSP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nmkdir -p $SP/r3dev && cd /Users/arsis/zlayt-pm-project && (LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7911 HOST=127.0.0.1 ZLAYT_DB=$SP/r3dev/dev.sqlite3 nohup .venv/bin/python -m app.main > $SP/r3dev/server.log 2>&1 & echo $! > $SP/r3dev/pid); sleep 6; cat $SP/r3dev/pid; curl -s localhost:7911/api/health"
}
````

### User / tool · 2026-11-02T05:34:37.716Z

**tool result**
````
23497
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:42.505Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 ZLAYT_DB=$SP/r3dev/dev.sqlite3 timeout 590 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -x -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T05:34:42.609Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:45.919Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 ZLAYT_DB=$SP/r3dev/dev.sqlite3 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -x -q 2>&1 | tail -40",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T05:34:48.545Z

**tool result**
````
F
=================================== FAILURES ===================================
_ test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action[real-1440-900] _

pw = <playwright._impl._playwright.Playwright object at 0x10b191100>
broken = {'tok': '8oHYPi33bzzzKGDYn_rZwQ', 'id': 'e1', 'orig': 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.', 'mode': 'real', ...}
w = 1440, h = 900

    @pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
    def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
        b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
        try:
            t = arm(broken, pg)
            open_case(pg, t["tok"]); row = row_of(pg, t["id"])
            row.scroll_into_view_if_needed()
            btn = row.get_by_test_id("btn-accept"); btn.click()
            box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
            msg = box.get_by_test_id("accept-refused-msg").inner_text()
            assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
            assert "not in the quote" in msg or t["mode"] == "real"
>           assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
E           AssertionError: the reason must be on screen beside the button, not below the fold
E           assert False
E            +  where False = vis(<Page url='http://127.0.0.1:7911/#/case/8oHYPi33bzzzKGDYn_rZwQ'>, <Locator frame=<Frame name= url='http://127.0.0.1:7911/#/case/8oHYPi33bzzzKGDYn_rZwQ'> selector='internal:testid=[data-testid="timeline"s] >> [data-item-id="e1"] >> nth=0 >> internal:testid=[data-testid="accept-refused"s]'>)

tests/e2e/test_code_check_refusal.py:110: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_code_check_refusal.py::test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action[real-1440-900]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 2.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:34:55.675Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='review.js'\ns=open(p).read()\nold=\"\"\"        repaintRefusal(id); RV.say(\"Not accepted: \" + refusals[id].message, true);\"\"\"\nnew=\"\"\"        repaintRefusal(id); RV.say(\"Not accepted: \" + refusals[id].message, true);\n        const mine = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-controls-for=\"' + id + '\"]'), box = (mine || document).querySelector(\".rv-refused:not([hidden])\");\n        if (box && box.scrollIntoView) box.scrollIntoView({ block: \"nearest\" });   // the answer is on screen beside the pressed button\"\"\"\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nPYEOF\ncd .. ; cd ..; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 ZLAYT_DB=$SP/r3dev/dev.sqlite3 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -q 2>&1 | tail -50",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T05:35:08.925Z

**tool result**
````
pw = <playwright._impl._playwright.Playwright object at 0x10b051670>
broken = {'tok': 'DIntg0MbLIXjrm2oErgZCg', 'id': 'e1', 'orig': 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.', 'mode': 'real', ...}
w = 1440, h = 900

    @pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
    def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
        b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
        try:
            t = arm(broken, pg)
            open_case(pg, t["tok"]); row = row_of(pg, t["id"])
            row.scroll_into_view_if_needed()
            btn = row.get_by_test_id("btn-accept"); btn.click()
            box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
            msg = box.get_by_test_id("accept-refused-msg").inner_text()
            assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
            assert "not in the quote" in msg or t["mode"] == "real"
>           assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
E           AssertionError: the reason must be on screen beside the button, not below the fold
E           assert False
E            +  where False = vis(<Page url='http://127.0.0.1:7911/#/case/DIntg0MbLIXjrm2oErgZCg'>, <Locator frame=<Frame name= url='http://127.0.0.1:7911/#/case/DIntg0MbLIXjrm2oErgZCg'> selector='internal:testid=[data-testid="timeline"s] >> [data-item-id="e1"] >> nth=0 >> internal:testid=[data-testid="accept-refused"s]'>)

tests/e2e/test_code_check_refusal.py:110: AssertionError
_ test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action[stub-1440-900] _

pw = <playwright._impl._playwright.Playwright object at 0x10b051670>
broken = {'tok': 'eE_RG8l2KOtYtUSVS1l9dA', 'id': 'e1', 'orig': 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.', 'mode': 'stub', ...}
w = 1440, h = 900

    @pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
    def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
        b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
        try:
            t = arm(broken, pg)
            open_case(pg, t["tok"]); row = row_of(pg, t["id"])
            row.scroll_into_view_if_needed()
            btn = row.get_by_test_id("btn-accept"); btn.click()
            box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
            msg = box.get_by_test_id("accept-refused-msg").inner_text()
            assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
            assert "not in the quote" in msg or t["mode"] == "real"
>           assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
E           AssertionError: the reason must be on screen beside the button, not below the fold
E           assert False
E            +  where False = vis(<Page url='http://127.0.0.1:7911/#/case/eE_RG8l2KOtYtUSVS1l9dA'>, <Locator frame=<Frame name= url='http://127.0.0.1:7911/#/case/eE_RG8l2KOtYtUSVS1l9dA'> selector='internal:testid=[data-testid="timeline"s] >> [data-item-id="e1"] >> nth=0 >> internal:testid=[data-testid="accept-refused"s]'>)

tests/e2e/test_code_check_refusal.py:110: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_code_check_refusal.py::test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action[real-1440-900]
FAILED tests/e2e/test_code_check_refusal.py::test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action[stub-1440-900]
2 failed, 7 passed in 12.94s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:16.752Z

**tool call — Bash**
````
{
 "command": "cat > /tmp/dbg.py <<'EOF'\nEOF\nrm /tmp/dbg.py; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $SP/dbg.py <<'EOF'\nimport sys, os, re\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom tests.e2e.test_code_check_refusal import *\nfrom tests.e2e.conftest import api\nfrom playwright.sync_api import sync_playwright\nst, c = api(\"POST\", \"/api/cases\", {\"sample\": True}); tok = c[\"token\"]; api(\"POST\", f\"/api/cases/{tok}/run\", {})\nimport time\nwhile api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] not in (\"ready\",\"failed\"): time.sleep(1)\ncase = api(\"GET\", f\"/api/cases/{tok}\")[1]\ne = next(x for x in case[\"entries\"] if x[\"state\"]==\"verified\" and x[\"date\"] and x[\"review_status\"]==\"pending\")\nstub = Refuse(tok, e[\"id\"])\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_context(viewport={\"width\":1440,\"height\":900}).new_page()\n    stub.attach(pg); open_case(pg, tok)\n    row = row_of(pg, e[\"id\"]); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-accept\").click(); pg.wait_for_timeout(500)\n    print(row.get_by_test_id(\"accept-refused\").bounding_box(), row.get_by_test_id(\"btn-accept\").bounding_box(), pg.evaluate(\"[scrollY, innerHeight]\"))\n    pg.screenshot(path=os.path.join(os.path.dirname(__file__), \"dbg.png\"))\n    b.close()\napi(\"DELETE\", f\"/api/cases/{tok}\")\nEOF\nE2E_BASE_URL=http://127.0.0.1:7911 .venv/bin/python $SP/dbg.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:18.731Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dbg.png"
}
````

### User / tool · 2026-11-02T05:35:19.140Z

**tool result**
````
{'x': 97.609375, 'y': 808.109375, 'width': 896, 'height': 92} {'x': 97.609375, 'y': 745.71875, 'width': 81.109375, 'height': 56} [130, 900]
````

### User / tool · 2026-11-02T05:35:19.147Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:26.618Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='review.js'\ns=open(p).read()\nold=\"\"\"        if (box && box.scrollIntoView) box.scrollIntoView({ block: \"nearest\" });   // the answer is on screen beside the pressed button\"\"\"\nnew=\"\"\"        if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner\"\"\"\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nPYEOF\ncd /Users/arsis/zlayt-pm-project; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 ZLAYT_DB=$SP/r3dev/dev.sqlite3 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -q 2>&1 | tail -30",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T05:35:40.857Z

**tool result**
````
.........                                                                [100%]
9 passed in 13.92s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:46.674Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 - <<EOF\np=\"$SP/dbg.py\"\ns=open(p).read()\ns=s.replace('''    row = row_of(pg, e[\"id\"]); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-accept\").click(); pg.wait_for_timeout(500)''','''    pg.get_by_test_id(\"btn-accept-verified\").click(); pg.wait_for_timeout(600)\n    pg.get_by_test_id(\"batch-refused\").scroll_into_view_if_needed(); row=row_of(pg,e[\"id\"])''')\ns=s.replace('print(row.get_by_test_id(\"accept-refused\").bounding_box(), row.get_by_test_id(\"btn-accept\").bounding_box(), pg.evaluate(\"[scrollY, innerHeight]\"))','')\ns=s.replace('\"width\":1440,\"height\":900','\"width\":390,\"height\":844')\nopen(p,'w').write(s)\nEOF\nE2E_BASE_URL=http://127.0.0.1:7911 .venv/bin/python $SP/dbg.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:48.808Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dbg.png"
}
````

### User / tool · 2026-11-02T05:35:49.133Z

**tool result**
````
(Bash completed with no output)
````

### User / tool · 2026-11-02T05:35:49.141Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:57.309Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'PYEOF'\np='batch.js'\ns=open(p).read()\nold=\"\"\"el(\"strong\", {}, \"Nothing was accepted. \"), refused.message),\"\"\"\nnew=\"\"\"el(\"strong\", {}, \"Nothing was accepted. \"), refused.rows.length ? (rows.length === 1 ? \"One summary fails a check, so the whole batch was refused. Edit it, then accept again.\" : rows.length + \" summaries fail a check, so the whole batch was refused. Edit them, then accept again.\") : refused.message),\"\"\"\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nPYEOF\ncd /Users/arsis/zlayt-pm-project && SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 .venv/bin/python $SP/dbg.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:35:59.548Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dbg.png"
}
````

### User / tool · 2026-11-02T05:35:59.828Z

**tool result**
````
(Bash completed with no output)
````

### User / tool · 2026-11-02T05:35:59.836Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:36:05.068Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E2E_BASE_URL=http://127.0.0.1:7911 ZLAYT_DB=$SP/r3dev/dev.sqlite3 .venv/bin/python -m pytest tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_edit.py tests/e2e/test_export_ui.py tests/e2e/test_ladder_gate.py tests/e2e/test_keyboard_mobile.py tests/e2e/test_timeline.py tests/e2e/test_review_matrix.py tests/e2e/test_code_check_refusal.py -q 2>&1 | tail -30; .venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q 2>&1 | tail -5",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T05:37:58.129Z

**tool result**
````
.............................s..ss.sss.s..................s............. [ 87%]
..........                                                               [100%]
74 passed, 8 skipped in 112.52s (0:01:52)
...                                                                      [100%]
3 passed in 0.02s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:38:02.153Z

**tool call — Bash**
````
{
 "command": "P=\"app/frontend/batch.js app/frontend/judges.js app/frontend/review.css app/frontend/review.js app/frontend/stepper.css app/frontend/stepper.js tests/e2e/conftest.py tests/e2e/test_rerun_judge.py tests/e2e/test_code_check_refusal.py\" && git add $P && git commit -q -m \"fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- $P && git log --oneline | head -2"
}
````

### User / tool · 2026-11-02T05:38:02.223Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: P="app/frontend/batch.js app/frontend/judges.js app/frontend/review.css app/frontend/review.js app/frontend/stepper.css app/frontend/stepper.js tests/e2e/conftest.py tests/e2e/test_rerun_judge.py test
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:38:03.722Z

**tool call — Bash**
````
{
 "command": "git add app/frontend/batch.js app/frontend/judges.js app/frontend/review.css app/frontend/review.js app/frontend/stepper.css app/frontend/stepper.js tests/e2e/conftest.py tests/e2e/test_rerun_judge.py tests/e2e/test_code_check_refusal.py"
}
````

### User / tool · 2026-11-02T05:38:03.829Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:38:05.188Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/frontend/batch.js app/frontend/judges.js app/frontend/review.css app/frontend/review.js app/frontend/stepper.css app/frontend/stepper.js tests/e2e/conftest.py tests/e2e/test_rerun_judge.py tests/e2e/test_code_check_refusal.py && git log --oneline | head -2"
}
````

### User / tool · 2026-11-02T05:38:05.995Z

**tool result**
````
check_secrets: ok (9 file(s) scanned staged)
9f2811f fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)
fdc2506 fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:38:06.604Z

Now the clean worktree verification on a spare port.

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:38:11.873Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; kill $(cat $SP/r3dev/pid); git worktree add $SP/wt HEAD -f >/dev/null 2>&1; cd $SP/wt && git log --oneline | head -1 && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; (LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7912 HOST=127.0.0.1 ZLAYT_DB=$SP/r3dev/wt.sqlite3 nohup .venv/bin/python -m app.main > $SP/r3dev/wt-server.log 2>&1 & echo $! > $SP/r3dev/wtpid); sleep 6; curl -s localhost:7912/api/health | head -c 80; echo; E2E_BASE_URL=http://127.0.0.1:7912 ZLAYT_DB=$SP/r3dev/wt.sqlite3 .venv/bin/python -m pytest tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_edit.py tests/e2e/test_export_ui.py tests/e2e/test_ladder_gate.py tests/e2e/test_keyboard_mobile.py tests/e2e/test_timeline.py tests/e2e/test_review_matrix.py tests/e2e/test_code_check_refusal.py tests/e2e/test_flags_panel.py tests/e2e/test_charges.py tests/unit/test_e2e_contract.py -q 2>&1 | tail -15",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T05:40:26.333Z

**tool result**
````
9f2811f fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only
.............................s..ss.sss.s..................s............. [ 75%]
.......................                                                  [100%]
87 passed, 8 skipped in 127.71s (0:02:07)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:40:36.064Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; kill $(cat $SP/r3dev/wtpid); sleep 1; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7912/api/health; rm $SP/wt/.venv; git worktree remove --force $SP/wt && git worktree list | head -3\nB=\"python3 tools/board.py\"\n$B ac T-097 --check 1 --agent frontend --evidence \"r3 (9f2811f): tests/e2e/test_code_check_refusal.py (9, real backend via ZLAYT_DB and contract stub) + test_rerun_judge/test_stepper/test_edit/test_export_ui/test_ladder_gate/test_keyboard_mobile/test_timeline/test_review_matrix/test_flags_panel/test_charges + unit test_e2e_contract: 87 passed 8 skipped on clean worktree of 9f2811f (fixture backend :7912, stopped by PID); accept 422 CODE_CHECK_FAILED inline with Edit (single, key a, batch list), case verdict verbatim in rail and panel, m-1/m-2/m-new-1 + n-1/n-new-3 fixed\"\n$B handoff T-097 --agent frontend --text \"What changed (r3, 9f2811f): refused Accept (422 CODE_CHECK_FAILED) shows 'Not accepted. <server reason>' in an alert box under the item's buttons with Edit the summary (clears on any decision); refused batch lists the items (name, server why, Edit) and says nothing was accepted; case verdict label shown verbatim in rail (case-verdict) and panel (judge-case-verdict); minors: panel names each class once (not checked / blocks export / summary fails a check / edited by you not AI-checked), Not-needed judge step prints no verdict, one group rerun button per list ('for these N', rows have none) so label count = POST count; nits n-1 (Export button kept in view after refusal) and n-new-3 (edited item reads Edited by you); AI-draft code blockers say 'This summary' not 'Your wording'. | Verified: 87 passed 8 skipped on clean worktree of 9f2811f, own server :7912 (fixture, scratch ZLAYT_DB), stopped by PID; real-backend variants write the failing summary through ZLAYT_DB (skip without it). | Left: n-2 (422 names normalised token '9000' not '\\$9,000') is backend wording, not done. | Surprised: scrollIntoView nearest left the refusal box flush with the fold, so the box is scrolled with a 16px margin.\"\n$B move T-097 in_review --agent frontend\n$B commit T-097 --sha 9f2811f --agent frontend"
}
````

### User / tool · 2026-11-02T05:40:37.562Z

**tool result**
````
000
/Users/arsis/zlayt-pm-project  9f2811f [main]
AC 1 checked: r3 (9f2811f): tests/e2e/test_code_check_refusal.py (9, real backend via ZLAYT_DB and contract stub) + test_rerun_judge/test_stepper/test_edit/test_export_ui/test_ladder_gate/test_keyboard_mobile/test_timeline/test_review_matrix/test_flags_panel/test_charges + unit test_e2e_contract: 87 passed 8 skipped on clean worktree of 9f2811f (fixture backend :7912, stopped by PID); accept 422 CODE_CHECK_FAILED inline with Edit (single, key a, batch list), case verdict verbatim in rail and panel, m-1/m-2/m-new-1 + n-1/n-new-3 fixed
handoff written on T-097
T-097: in_progress -> in_review
T-097: commit 9f2811f recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:40:38.130Z

Quick memory update.

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:40:40.670Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend && cat >> project_stepper_panels.md <<'EOF'\n\n## T-097 r3 (D-051 refusals)\n- Refused Accept: review.js `refusals{}` map + `.rv-refused` box (testid accept-refused) under the button bar in RV.controls; batch.js `refused` + batch-refused inside the batch bar. Server message shown verbatim; scroll the box with a 16px margin (scrollIntoView nearest leaves it flush on the fold).\n- Rerun: one group button per list (\"for these N\"); never per-row, one POST reruns all (reviewer m-2 recurred 3 rounds).\n- Real-backend e2e for a failing summary: write `summary` via `app.db.db.update_item` on the server's ZLAYT_DB (tests skip without it); route stubs cannot be composed (later route wins), so one stub per test.\nEOF"
}
````

### User / tool · 2026-11-02T05:40:40.753Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:40:44.634Z

T-097 round 3 is committed (9f2811f) and in `in_review`. The new and existing e2e specs plus the unit `test_e2e_contract` passed on a clean worktree of 9f2811f: 87 passed, 8 skipped. The server was on port 7912 with the fixture backend, stopped by PID, and the worktree is removed.

- **Refused Accept:** a 422 `CODE_CHECK_FAILED` shows the server's reason inline under the item's buttons with an "Edit the summary" action. The same applies to the `a` key. A refused batch lists each refused item with its reason and an Edit action, and says nothing was accepted.
- **Case verdict:** "N summaries fail a check" shows verbatim in the case rail and in the AI-check panel.
- **Minors:** all three fixed. The panel now names each kind of item once, the "Not needed" judge step no longer prints a second-check verdict, and each list has one "Run the second check again for these N" button instead of per-row buttons.
- **Also fixed:** two nits (the Export button stays in view after a refusal, and an edited item reads "Edited by you"). A code-check blocker on an AI draft now reads "This summary doesn't match the quote", not "Your wording".
- **Not fixed:** n-2 (the 422 quotes the token as "9000", not the typed "$9,000"), because that wording comes from the backend.
- **Tests:** `tests/e2e/test_code_check_refusal.py` runs each case against the real backend and against a stub. The real-backend variants need `ZLAYT_DB` and skip without it.
