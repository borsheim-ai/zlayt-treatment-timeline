# T-104 review: ux-designer-reviewer (Priya Raman persona)

Scope: app/frontend at commit 3462ad0, served from a `git archive` copy on my own server (127.0.0.1:7931, fixture backend, curated set, scratch ZLAYT_DB). Repo HEAD at review start was c2a5d1f, one commit ahead (T-106), not used.

Verdict: **pass** (0 blockers, 0 majors, 3 minors, 1 nit).

The routing is right. EDIT_QUOTE reads "Change the quote" and EDIT_SUMMARY reads "Edit the summary" on the item refusal, batch rows, the Why dialog, the case rail and the AI-check panel. A refused edit renders inline under the box with the typed text and focus kept. The Why lead follows the verdict string. My 33-check walk passed 32. The one failure is a 390 px placement issue (F2).

The three minors are copy and placement, not wrong actions:
- F1: quote-level refusals are explained as a summary problem. The sentence names the wrong fix.
- F2: at 390 px the edit refusal sits below the fold after Save.
- F3: 8 Tab presses from the row to the quote fix.

Evidence: `artifacts/review-evidence/T-104-ux-designer-walk.py`, `T-104-ux-designer-results.json`, `T-104-ux-designer-mobile.py`, `T-104-ux-designer-rail.py`, `T-104-ux-designer-setup.py`, and the screenshots `artifacts/review-evidence/T-104-ux-desk-*.png` and `T-104-ux-mob-*.png`. Nothing was saved in the walk: pending 21, accepted 2 (the two pre-accepted AI drafts), edited 0 after the run. Saving through the quote picker is not scored (T-108).

```json
{"card": "T-104", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "app/frontend at commit 3462ad0 (git archive copy, not the repo root); app http://127.0.0.1:7931 (my own server: fixture backend, curated set, scratch ZLAYT_DB); sample case token LSx5Yirp9S2KvZOp_puLBw; repo HEAD at review start c2a5d1f (one commit ahead, T-106, not used)",
 "exercised": [
  "python3 tools/board.py show T-104 (status in_review, AC 1 evidence read); read personas/ux-designer.md and the memory directory",
  "git rev-parse --short HEAD -> c2a5d1f; git status --short | wc -l -> 1307 (repo root, not used); git merge-base --is-ancestor 3462ad0 HEAD -> ancestor; git log --oneline 3462ad0..HEAD -> c2a5d1f",
  "git archive 3462ad0 | tar -x into a scratch directory; started app.main there with PORT=7931 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated; GET /api/health -> 200, backend fixture, synthetic_only true (PID 77878, stopped at the end)",
  "artifacts/review-evidence/T-104-ux-designer-setup.py: created a sample case, injected e1 (quote cut to start mid-sentence, EDIT_QUOTE), e2 (summary 'Pain 5/10', EDIT_SUMMARY), accepted e3 and e4 and then broke their quote and summary (AI-draft gate blockers). Same method as tests/e2e/test_code_check_refusal.py",
  "curl probes on the real backend: accept e1 -> 422 CODE_CHECK_FAILED, EDIT_QUOTE; summary-only edit on e1 -> 422 CODE_CHECK_FAILED, EDIT_QUOTE; accept e2 -> 422 CODE_CHECK_FAILED, EDIT_SUMMARY; edit e2 with a new number -> 422 invalid_edit SUMMARY_NUMBER_NOT_IN_EXCERPT; edit e1 dropping the self-report qualifier -> 422 invalid_edit SUMMARY_DROPS_QUALIFIER; GET .../items/{e1..e4}/trace and the case trace gate blockers",
  "Playwright at 1440x900 (artifacts/review-evidence/T-104-ux-designer-walk.py, 33 checks, results in T-104-ux-designer-results.json): item row accept refusal for e1 and e2 incl. button sets and quote picker open; batch refusal list and per-row buttons, picker from the batch row; inline edit refusal on e1 (real backend) with typed text, focus and role=alert; Why dialog for e3 and e4 (real verdict), Why with route-rewritten verdict label ('your wording') on e3 and e4 and 'this summary' on e4 (STUB: trace label rewritten, nothing else); rail gate blockers e3 and e4 and their buttons; AI-check panel wording rows; keyboard: 'a' on e1 then Tab count then Enter; stub edit refusal CODE_CHECK_FAILED/EDIT_SUMMARY on e2 (STUB: route answers the edit; the real backend never returned this shape for a summary edit)",
  "390x844 (artifacts/review-evidence/T-104-ux-designer-mobile.py): geometry of the edit refusal after Save and after scrolling; horizontal overflow 0 px; Tab count from the textarea to the quote button (3). Screenshots T-104-ux-mob-01..03",
  "Rail gate-blocker list screenshot (artifacts/review-evidence/T-104-ux-desk-17-rail-gate-blockers-list.png)",
  "Read app/frontend diff at 3462ad0 (review.js, stepper.js, batch.js, excerpt.js, judges.js) and app/backend/trace.py:48,:275 for the copy source; tests/e2e/test_code_check_refusal.py for the method",
  "Not scored: saving a quote choice through the picker (T-108, known limitation)"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor",
   "title": "Quote-level refusals are explained as a summary problem, and the sentence names the wrong fix",
   "evidence": "app/backend/trace.py:48 (fixed why 'This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.') and trace.py:275 (verdict label chosen by who wrote the wording, not by the failing check). Real trace for e3 (first failing check EXCERPT_NOT_WHOLE_SENTENCE, next_action EDIT_QUOTE): verdict label 'Needs your attention: a check on this summary fails'. Shown on the Why alert 'This summary doesn't match the quote: The quote starts or ends in the middle of a sentence ... until the summary matches the quote.' with button 'Change the quote' (artifacts/review-evidence/T-104-ux-desk-09-why-e3-quote.png); the same text on the rail gate blocker (artifacts/review-evidence/T-104-ux-desk-17-rail-gate-blockers-list.png) and on the AI-check panel row (artifacts/review-evidence/T-104-ux-desk-14-judges-wording.png). The frontend lead (app/frontend/stepper.js:137) follows the verdict string as T-104 requires, so the defect is in the backend strings.",
   "why_it_matters": "The button is right, but the sentence tells the paralegal to make the summary match the quote. A summary-only edit does not clear this check: a summary-only edit on e1 returned 422 CODE_CHECK_FAILED / EDIT_QUOTE again. A paralegal who follows the sentence loops. This is a wrong explanation next to a correct action, so minor, not blocker.",
   "fix": "In app/backend/trace.py, choose the verdict label and the blocker 'why' by the failing check's next_action code. For EDIT_QUOTE, say the quote fails and that the quote must change, e.g. 'Needs your attention: a check on the quote fails' and 'until the quote is fixed'. Keep the summary wording for EDIT_SUMMARY. The frontend then needs no change, because it follows the string.",
   "acceptance_test": "E2E on a real backend with an accepted AI draft whose quote is cut mid-sentence: the item Why alert, the rail gate-blocker row and the AI-check row contain no 'until the summary matches the quote' and name the quote. The same item with a broken summary (Pain 5/10) still reads 'This summary doesn't match the quote' and 'Edit the summary'."},
  {"severity": "minor",
   "title": "At 390 px the edit refusal sits below the fold after Save, and the edit path does not bring it into view",
   "evidence": "Measured by artifacts/review-evidence/T-104-ux-designer-mobile.py on e1 at 390x844: after Save, edit-refused-msg top y=853.7 and btn-edit-refused-quote y=916.5, viewport height 844; after scrollIntoView the button is at y=399.5. Screenshot artifacts/review-evidence/T-104-ux-mob-02-edit-refused-quote.png shows the textarea (focused) and Save with the reason cut off below. Walk check '390px: inline edit refusal and Change the quote are reachable' FAILED for this reason (results JSON; horizontal overflow 0). The accept path scrolls its refusal into view (app/frontend/review.js:200, window.scrollBy); showEditRefusal (review.js:133-141) only writes the message and focuses the textarea. At 1440x900 the message is visible under the box (artifacts/review-evidence/T-104-ux-desk-07-edit-refused-quote.png).",
   "why_it_matters": "On a phone, Save is the only feedback for a refused edit, and the reason is one scroll away and unseen. The message is near its input, so criterion 12 holds; the gap is that the screen gives no signal. Minor, not blocker, because nothing is lost and the box stays open.",
   "fix": "In showEditRefusal (app/frontend/review.js:133), after writing the message, scroll the rv-error line into view with block 'nearest', as the accept path does at review.js:200.",
   "acceptance_test": "E2E at 390x844: after Save on a refused quote edit, edit-refused-msg is within the viewport (its bounding box bottom is at or below 844 and its top is at or above 844) without a manual scroll; the typed-text and focus asserts still pass."},
  {"severity": "minor",
   "title": "Keyboard route to the quote fix is 8 Tab presses from the row",
   "evidence": "Keyboard run on e1 at 1440x900: 'a' shows the refusal, focus stays on the row (data-item-id e1), 8 Tab presses reach btn-accept-refused-quote, Enter opens the picker (results JSON, check 'keyboard (e1 EDIT_QUOTE)': tabs_to_quote_button 8). The refusal box comes after the row's six action buttons (Why, Open record, Change quote, Accept, Edit, Dismiss, Audit). At 390 px the inline edit route is 3 Tabs from the textarea (T-104-ux-designer-mobile.py output).",
   "why_it_matters": "The fix is reachable, but a keyboard-first paralegal has to walk the whole row to reach it (criterion 7: efficient correction, keyboard equivalents). Verification is not affected, because the excerpt stays inline. Minor.",
   "fix": "Either move focus to the refusal's action after 'a' refuses (the way the edit path moves focus to its textarea), or add a row key for the quote picker and name it in the refusal text.",
   "acceptance_test": "After 'a' on a refused EDIT_QUOTE row, the active element is btn-accept-refused-quote or a documented key opens the picker; the test asserts the picker opens within 2 key presses after the refusal appears."},
  {"severity": "nit",
   "title": "Two names for the same picker in one row, and the refusal repeats its button text",
   "evidence": "artifacts/review-evidence/T-104-ux-desk-02-row-e1-accept-refused-quote.png: the row toolbar says 'Change quote' (app/frontend/excerpt.js:47) and the refusal below says 'Change the quote' (also batch, Why, rail, AI-check). The refusal text reads 'Change the quote to whole sentences of the record that keep the hedge sentence.' right before the button 'Change the quote' (same screenshot).",
   "why_it_matters": "Two labels for one action in the same row make the paralegal check whether they are different actions. Nit only.",
   "fix": "Use one label everywhere (for example 'Change the quote' on the toolbar too), and consider dropping the trailing imperative from the backend sentence when a button with the same words follows it.",
   "acceptance_test": "Grep the rendered label set on an EDIT_QUOTE row: one string for the picker action across the toolbar, refusal, batch, Why and rail."}
 ],
 "whats_right": [
  "Each next_action code gets the right button on every surface: EDIT_QUOTE reads 'Change the quote' and EDIT_SUMMARY reads 'Edit the summary' on the item refusal, batch rows, Why, rail and AI-check panel (33-check walk, 32 pass).",
  "A refused edit renders inline under its box: the server's sentence sits in a role=alert line, the typed text stays in the box, focus stays in the textarea, and nothing is saved (artifacts/review-evidence/T-104-ux-desk-07-edit-refused-quote.png, T-104-ux-desk-16-stub-edit-summary-refused.png).",
  "The Why lead follows the verdict string: rewriting the label to 'your wording' changed the lead to 'Your wording doesn't match the quote:' and the button to 'Edit your wording', and the real 'this summary' label gave 'This summary doesn't match the quote:' (results JSON)."
 ],
 "questions_for_chris": [
  "The real backend answers a summary-only edit that drops a qualifier or adds a number with 422 invalid_edit (SUMMARY_DROPS_QUALIFIER / SUMMARY_NUMBER_NOT_IN_EXCERPT), not CODE_CHECK_FAILED with EDIT_SUMMARY as memory/contracts/api.md describes for edits. The UI shows both inline with the text kept, so I scored the UI. The EDIT_SUMMARY-from-edit path was only reachable through a route stub here. Which shape is intended?"
 ]}
```
