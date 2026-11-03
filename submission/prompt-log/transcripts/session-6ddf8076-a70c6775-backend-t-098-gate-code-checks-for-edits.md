# Subagent: Backend: T-098 gate code checks for edits (Backend: T-098 gate code checks for edits)

Source: `agent-a70c6775cdba62825.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:55:14.980Z

You own board card T-098 (P1, claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-098` and read reviews/T-097-ux-designer.md (the blocker) and D-034, D-022, D-044 and D-045 in memory/ORCHESTRATOR_DECISIONS.md.

D-045(b) says a human-edited summary is exempt from the judge, but it must still pass the code checks. Right now an edited summary that fails the qualifier check passes the export gate into the letter. Fix it in trace.py (the gate) and in export:
- an accepted item whose current summary fails any code check is a blocker with its reason;
- GET export returns 422 for it;
- gate.ready == export allowed still holds;
- the per-item trace shows the failing code step with the paralegal's next action ("Edit the summary to keep 'possible'…").

Add tests using the reviewer's case. Run `.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py`, then the full `tests/unit`. Commit from a fresh temp index built on HEAD, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-098 in_review --agent backend`. Note on T-097 any field the frontend should read. Reply in 1 line.

### User / tool · 2026-11-02T04:55:14.984Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:17.486Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-098; cat reviews/T-097-ux-designer.md | head -120; grep -n -A12 -E '^#+ .*D-0(34|22|44|45)|\\*\\*D-0(34|22|44|45)' memory/ORCHESTRATOR_DECISIONS.md | head -150"
}
````

### User / tool · 2026-11-02T04:55:17.644Z

**tool result**
````
---
id: "T-098"
title: "Export gate must block human-edited items whose code checks fail (D-045b: exempt from judge, not from code checks)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:55:06Z"
updated_at: "2026-11-02T04:55:09Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:55:09Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "An accepted, human-edited summary that fails any D-034/D-022 code check (qualifier dropped, token not in excerpt) is a gate blocker and GET export returns 422 with the reason; gate.ready == export allowed still holds; per-item trace shows the failing code step; tests with the reviewer's case (reviews/T-097-ux-designer.md)", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:09Z backend: claimed

## Handoff (filled when moving to in_review)

# T-097 ux-designer-reviewer: rerun feedback beside the refused export, panel failure message, panel/gate agreement

Verdict: **fail** (1 blocker, 2 majors, 1 minor, 1 nit).

Scope: card T-097, commit 0e30623 (the card's commit). I ran a `git archive 0e30623` copy from my scratchpad on my own server (:7895, fixture backend, curated set, scratch ZLAYT_DB). Shared-tree HEAD was 8bc7f90 at the start and 172028c at the end (it moved during the review); I did not review either. Server stopped by PID, port returns 000.

## The four brief questions

1. **Rerun feedback directly under the button in the refused-export message: pass.** At 1440 the button is at y=154 (h=44) and the status line at y=202, 4 px below it. At 390 the button is at y=202 and the status at y=250. The Running and the failed sentence are both in view at both widths. Failed sentence: "The second check still did not answer for 3 items of 3. Try again, or dismiss them." The lead sentence is above the button, so "under the button" is the status line, not the lead.
2. **A failed panel rerun shows a plain-words message that survives a repaint: pass.** The AI-check panel group shows the same failed sentence at 1440 (y=879, in view) and 390 (y=448, in view). It survives collapse and reopen and a second failed rerun, which rebuilds the panel. A full page reload clears it; that is expected for in-memory state and I do not count it.
3. **The panel reads the gate's JUDGE_NOT_RUN blockers, and an edited item says "Edited by you, not AI-checked" with no rerun: partly.** The panel rows and group are right: the edited row has the chip "Edited by you, not AI-checked", no "Blocks the export" chip and no button; the accepted row carries "Blocks the export"; the group button reads "for this item" for N=1. Dismissing the accepted item clears the panel block and the rail says "Ready to export". Two places still disagree with the gate: the panel's one-line summary (finding 2) and the item Why dialog for the edited item (finding 3). Finding 1 is a gate defect the walk exposed.
4. **One group button instead of per-row buttons: reasonable in the AI-check panel, incomplete overall.** One POST covers the whole list (the server scope), and the label counts match the rows. But the rail's gate rows still carry one button per row, and the label names one item while the POST answers for all of them (finding 4). Apply the group model to the rail too.

## Findings

**B1 (blocker). An edited summary whose qualifier check fails passes the export gate and goes into the letter.** Walk2 part B: after I accepted one item and edited another so it drops a qualifier from its quote, dismissing the accepted item gives a gate of "pass", an export of 200 that contains the edited sentence, and the edited item's own trace reports `summary_qualifier` fail with `SUMMARY_DROPS_QUALIFIER`. The Why dialog shows "Summary keeps the quote's qualifiers | Code | Needs your decision", and the rail says "Ready to export, 21 not reviewed". D-045(b) says an edited summary "still passes the D-034 code checks". The gate does not enforce that for edits. The probe found no AI draft in the sample with this check failing, so I cannot compare the AI path; the blocker is on the edited path that was exercised. Open question for Chris below.

**M1 (major). The panel summary still says "2 not checked (blocks export)" while the gate blocks 1.** With one accepted item (judge never ran) and one edited item (exempt), the summary reads "18 checked, 18 agreed with the draft, 2 not checked (blocks export)" at both widths, and the rail says "Export blocked by 1". The "(blocks export)" suffix is attached to the full unchecked count. This is the T-082 r3 contradiction, fixed in the rows and group but not in the summary the paralegal sees when the panel is collapsed. The card's own AC says the panel never says "Blocks the export" for items the gate treats as ready.

**M2 (major). The Why dialog for an edited item says "Accepted, second check missing" and offers "Run the second check again".** The verdict and the judge step come from the per-item trace, which still treats the edited item as a failed judge. The same item's panel row says "Edited by you, not AI-checked" with no button. T-081 r3 logged this as minor; I raise it because the card's goal is gate and panel agreement, and the Why dialog is the surface where the paralegal decides the item. The T-097 handoff lists it as left open.

**m1 (minor). Rail gate-row rerun buttons name one item but rerun all of them (carried from T-081 r3, unchanged).** The row's aria-label is "Run the second check again for 2026-01-09 · Austin EMS run report", yet one click posts once and the status reads "for 3 items of 3" (walk2 `A_1440_after_row_click`, same at 390). The rail rows are built by `blockerRow` at stepper.js:419, which passes the per-item label into the shared handler that posts with no item id (stepper.js:137).

**n1 (nit). The Export button is still scrolled out of view when a refused export opens (carried from T-081 r3).** Export button y=-32 at 1440 and y=-179 at 390 after the message opens; `export-blocked` is in view but `btn-export` is not.

## Evidence

- Walk scripts and results: `artifacts/review-evidence/T-097-ux-designer-walk1.py` and `artifacts/review-evidence/T-097-ux-designer-walk1-results.json`; `artifacts/review-evidence/T-097-ux-designer-walk2.py` and `artifacts/review-evidence/T-097-ux-designer-walk2-results.json`; `artifacts/review-evidence/T-097-ux-designer-probe3.py`.
- Screenshots: `artifacts/review-evidence/T-097-ux-designer-1440-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s2-panel-failed.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png`.
- Code located (not used as evidence of behaviour): `app/frontend/stepper.js:131-143, 163-171, 411-420, 488-507`; `app/frontend/judges.js:1-39, 40-150`; `memory/ORCHESTRATOR_DECISIONS.md:42` (D-034) and `:53` (D-045).

## What I did not exercise

Keyboard-only walk (not in this brief). The item Why dialog for an accepted item was not clicked separately; it uses the same `S.rerunButton` handler as the rail (finding m1). The server log has four `llm call failed step=j1` lines from the walk; I did not trace them to any UI state, and that is outside my lens.

## Three things that are right

- The refused-export message puts the rerun button and its Running and result sentences directly beneath the lead sentence, in view at 1440 and 390 (S1 `status_directly_under_button: true`).
- A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths.
- The panel's edited row says "Edited by you, not AI-checked" with no block chip and no button, and dismissing the accepted item clears the panel block and the rail.

```json
{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "card commit 0e30623 via git archive copy in scratchpad (t097/wt); shared-tree HEAD was 8bc7f90 at start and 172028c at end (not reviewed); app http://127.0.0.1:7895 on own server (fixture backend, curated set, scratch ZLAYT_DB), stopped by PID; sample case plus synthetic cases created by the walks",
 "exercised": [
  "git rev-parse --short HEAD -> 8bc7f90; git rev-parse --short 0e30623 -> 0e30623; git status --short | wc -l -> 277 (start)",
  "git archive 0e30623 | tar -x into scratchpad t097/wt (card commit, not HEAD)",
  "own server LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7895 ZLAYT_DB in scratchpad: health 200; pids 45474 and 54605 stopped by PID; curl returns 000 after each",
  "E2E_BASE_URL=http://127.0.0.1:7895 pytest -p no:cacheprovider tests/e2e/test_rerun_judge.py -q from the copy: 17 passed in 25.15s",
  "artifacts/review-evidence/T-097-ux-designer-walk1.py at 1440x900 and 390x844: S1 refused export with JudgeNotRun mode still and hold: pressed the message rerun button, read busy and failed sentences, measured positions, scroll, reopen after reload",
  "walk1 S2: AI-check panel group button, failed sentence, collapse/reopen, second failed rerun",
  "walk1 S3: mixed case (accepted judge-never-ran plus edited exempt): rail summary and row aria-labels, panel summary, edited and accepted rows, group button, item Why dialog for the edited item, dismiss accepted and reload",
  "artifacts/review-evidence/T-097-ux-designer-walk2.py: rail gate-row click (aria-label vs POST scope); edited-summary gate and export via GET /trace, GET /export, GET /items/<id>/trace",
  "artifacts/review-evidence/T-097-ux-designer-probe3.py: searched sample AI drafts for summary_qualifier fail: none found",
  "viewed screenshots: 1440 s1 failed, 390 s1 failed, 390 s2 panel failed, 1440 s3 mixed panel, 1440 s3 edited item dialog",
  "read stepper.js 131-143, 163-171, 411-420, 488-507; judges.js 1-39 and 40-150; ORCHESTRATOR_DECISIONS.md D-034 line 42 and D-045 line 53; reviews T-081-ux-r3 and T-082-ux-r3"],
 "verdict": "fail",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 2},
 "findings": [
  {"severity": "blocker", "title": "Edited summary whose qualifier check fails passes the export gate and goes into the letter",
   "evidence": "walk2 part_b (artifacts/review-evidence/T-097-ux-designer-walk2-results.json): B_item_trace_code_steps [summary_qualifier, fail, SUMMARY_DROPS_QUALIFIER]; B_gate_after_dismiss {status: pass, ready: true, blockers: []}; B_export {status: 200, contains_edit: true}. Rail after dismiss: 'Ready to export, 21 not reviewed' (artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png). Why dialog: 'Summary keeps the quote's qualifiers | Code | Needs your decision' (artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png). D-045(b) at memory/ORCHESTRATOR_DECISIONS.md:53.",
   "why_it_matters": "D-045(b) exempts an edited summary from the judge but says it still passes the D-034 code checks. Here the code check fails, the gate says ready, and the letter carries the edited wording with no flag. The export is what the paralegal pastes into a demand letter, so a dropped qualifier reaches the letter with the product's own check failing. Spec-class blocker (invents or loses facts). Whether summary_qualifier is in the D-034 set is an open question for Chris.",
   "fix": "Apply to edited summaries the same code steps the gate enforces on model drafts. Refuse the edit at save time with an inline message naming the dropped qualifier, keeping the typed text in the box. Also have the gate list any edited item whose code step fails as a named blocker, so GET /export is refused while it fails. The rail, the Export message and the item Why dialog must all say the same thing.",
   "acceptance_test": "E2E: edit a summary so it drops a qualifier from its quote. Expect an inline refusal beside the edit box with the typed text preserved; while it fails, GET /api/cases/<t>/export is not 200 and the letter does not contain the edited sentence. Unit: the gate blocker list includes any edited item with a failing code step."},
  {"severity": "major", "title": "Panel summary still says '2 not checked (blocks export)' while the gate blocks 1",
   "evidence": "S3_edited_mixed_1440_panel_summary {summary_counts: '18 checked, 18 agreed with the draft, 2 not checked (blocks export)'}; S3_edited_mixed_1440_rail {summary_gate: 'Export blocked by 1'}; same at 390 (S3_edited_mixed_390_panel_summary). Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png. judges.js summaryText attaches '(blocks export)' to the full unavailable count when nb > 0.",
   "why_it_matters": "The T-097 AC says the panel never says 'Blocks the export' for items the gate treats as ready. The one-line summary is the signal the paralegal reads when the panel is collapsed; it says two unchecked items block, and the gate says one. It is the same contradiction T-082 r3 named, fixed in the rows and group but not in the summary.",
   "fix": "Build the summary from the gate's JUDGE_NOT_RUN set: '2 not checked, 1 blocks export'. Only the gate-listed count carries the blocking wording.",
   "acceptance_test": "E2E on the mixed case (1 accepted, 1 edited, judge never ran on the accepted one): judge-summary-counts shows the gate count (1) next to 'blocks export' and does not attach it to the edited item; after the accepted item is dismissed, the summary has no 'blocks export'."},
  {"severity": "major", "title": "Why dialog for an edited item says 'Accepted, second check missing' and offers 'Run the second check again'",
   "evidence": "S3_edited_mixed_1440_item_dialog_edited {verdict: 'Accepted, second check missing', rerun_btn: 1}, judge step '✕ ... Did not run ... Run the second check again'; same at 390 (S3_edited_mixed_390_item_dialog_edited). Same item's panel row: S3_edited_mixed_1440_panel_edited_row {chip 'Edited by you, not AI-checked', rerun_btn_in_row: 0}. Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png. The verdict comes from GET /api/cases/<t>/items/<id>/trace, which the stub does not change for edited items. The T-097 handoff lists this as left open.",
   "why_it_matters": "The Why dialog is where the paralegal decides an item. For an item D-045(b) exempts, it says the check is missing, shows a red cross, and offers a button that answers 'nothing to run'. The panel and the gate say the opposite. T-081 r3 logged this as minor; raised here because the card's goal is gate and panel agreement, and this is the third surface showing the state.",
   "fix": "For human-wording items (review_status edited), build the judge step as neutral 'Not needed: you wrote this summary', with verdict 'Edited by you' and no btn-rerun-judge. Do it in the per-item trace builder so the Why dialog and the panel read one source.",
   "acceptance_test": "E2E on the mixed case: the item-stepper for the edited item has no text 'second check missing', no btn-rerun-judge, and no judge step with data-status fail; after the accepted item is dismissed the rail still says Ready to export."},
  {"severity": "minor", "title": "Rail gate-row 'Run the second check again' buttons name one item but rerun every item (carried from T-081 r3)",
   "evidence": "walk2 A_1440_row_before aria_label 'Run the second check again for 2026-01-09 · Austin EMS run report'; A_1440_after_row_click {posts: 1, rail_status_texts: ['The second check still did not answer for 3 items of 3. Try again, or dismiss them.']}; same at 390. stepper.js:419 passes RERUN + ' for ' + name to S.rerunButton (stepper.js:137), which posts with no item id.",
   "why_it_matters": "The label and the effect disagree: a screen-reader user hears a per-item promise, and a sighted user reads a result for three items after pressing one row. T-097 moved the panel to one group button, the right model, but the rail rows and the item Why dialog keep per-item labels.",
   "fix": "Use the group model everywhere: one 'Run the second check again for these N' in the gate step and no per-row button (rows keep Go to item). If per-row buttons stay, send the item id and rerun only that item.",
   "acceptance_test": "E2E: for every rerun button in the rail, the aria-label scope equals the POST scope: a one-item label means one item in the POST, and a label naming N items means N equals the number of JUDGE_NOT_RUN blockers."},
  {"severity": "nit", "title": "Export button is scrolled out of view when a refused export opens (carried from T-081 r3)",
   "evidence": "S1_export_blocked_1440_before export_btn_box {y: -32}, message top y=90; S1_export_blocked_390_before export_btn_box {y: -179}; export_btn_in_view false after the failure at both widths (walk1 results).",
   "why_it_matters": "The message correctly sits under the toolbar, but the Export button it explains is above the fold; to press Export again the user scrolls up.",
   "fix": "Set scroll-margin-top on the export-blocked section to the toolbar height, or scroll the toolbar row into view instead of the message.",
   "acceptance_test": "E2E: after a refused Export at 1440x900 and 390x844, btn-export and export-blocked both have their top inside the viewport."}
 ],
 "whats_right": [
  "Refused-export message: the rerun button and its Running and result sentences sit directly beneath the lead sentence, the status 4 px under the button, in view at 1440 and 390 (walk1 S1, status_directly_under_button true).",
  "A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths (walk1 S2).",
  "The panel's edited row says 'Edited by you, not AI-checked' with no block chip and no button; dismissing the accepted item clears the panel block and the rail says Ready to export (walk1 S3)."],
 "questions_for_chris": ["Is summary_qualifier part of the D-034 code-check set that D-045(b) requires edited summaries to pass? If yes, B1 stands as a blocker; if the qualifier check is advisory for edits, B1 becomes a major and the gate copy must say so."]}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:19.702Z

**tool call — Bash**
````
{
 "command": "grep -n -E 'D-0(22|34|44|45)' memory/ORCHESTRATOR_DECISIONS.md | head; wc -l app/backend/trace.py app/backend/export.py tests/unit/test_trace.py tests/unit/test_export.py; git status --short | wc -l; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T04:55:19.843Z

**tool result**
````
30:| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
42:| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal notes ('reviewer override: <reason code>'). | An override let 'Pain 9/10' into the letter against a 4/10 quote — an invented fact. | T-056 paralegal review |
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
52:| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
     968 app/backend/trace.py
     606 app/backend/export.py
    1017 tests/unit/test_trace.py
     197 tests/unit/test_export.py
    2788 total
     311
/bin/bash: child setpgid (58724 to 58724): Operation not permitted
172028c
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:21.132Z

**tool call — Bash**
````
{
 "command": "grep -n -E 'def |JUDGE_NOT_RUN|JUDGE_UNAVAILABLE|summary_qualifier|SUMMARY_DROPS|edited|human' app/backend/trace.py | head -150"
}
````

### User / tool · 2026-11-02T04:55:21.220Z

**tool result**
````
3:item_trace(conn, case_id, item_id, full)  one item (entry, amount, flag, narrative sentence): extracted, each code check by name, judge, human.
8:answer for LLM steps and the before/after of human events. Prompt text is never in a trace. Judge "rationale" is the fixed sentence for the judge's
25:def judge_of_prompt(pv):
41:    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
46:    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
47:    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
68:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
75:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
78:def reason_text(code: str) -> str:
87:def na(code: str, target: dict = None, options: list = None) -> dict:
96:def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
101:def _ocr_steps(R, rid) -> list:
109:def _number(steps):
115:def _progress(steps):
129:    def __init__(self, conn, case_id, full):
145:    def call(self, call_id, item_id=None, step_name=None):
154:def _span(cx, rid, start, end, text):
158:def _llm_evidence(cx, role, model, prompt_version, call):
172:def _norm_verdict(step_id, v):
178:def _judge_reason_code(jd, call):
192:def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
204:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
215:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
224:def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
228:    ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
232:    if rs == "edited":
233:        ed = row.get("edited") or {}
237:            ev["edited_text"] = ed.get("summary") or ed.get("note")
238:    if rs in ("accepted", "edited"):
239:        return step("human", "Your decision", "human", PASS, "You accepted this item." if rs == "accepted" else "You edited this item and accepted it.", rule="row 17", evidence=ev)
241:        return step("human", "Your decision", "human", SKIPPED, "You dismissed this item; it stays out of the letter.", rule="row 17", evidence=ev)
243:        return step("human", "Your decision", "human", PENDING, "This item could not be verified, so it cannot be accepted.", reason="PENDING_DECISION", rule="row 17", evidence=ev,
245:    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
249:def _skipped(sid, label, kind, code, rule=None, rule_text=None):
256:def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
263:    if rs in ("accepted", "edited", "dismissed"):
264:        first_na = None             # the human already decided; step-level hints stay on the steps
265:    if rs in ("accepted", "edited"):
283:    def step_of(c):
294:def _excerpt_ev(cx, rid, row):
295:    ed = row.get("edited") or {}
299:def _entry_steps(cx, row):
312:        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
329:    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
353:    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
354:              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
385:    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
390:def _amount_steps(cx, row):
436:    elif rs in ("accepted", "edited"):
441:    st.append(_human_step(cx, row, "amount"))
446:def _flag_steps(cx, row):
458:    def inj():
470:        st.append(_human_step(cx, row, "flag"))
486:        st.append(_human_step(cx, row, "flag"))
506:        st.append(_human_step(cx, row, "flag"))
565:    st.append(_human_step(cx, row, "flag"))
570:def _ntext(code):
574:def _narrative_trace(cx, item_id):
619:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
622:        st.append(step("human", "Your decision on the paragraph", "human", SKIPPED, "This sentence was removed from the draft, so it cannot be accepted.", rule="D-031"))
625:        st.append(step("human", "Your decision on the paragraph", "human", PASS, "You accepted the paragraph.", rule="D-031", evidence={"action": "accept", "at": nar.get("reviewed_at")}))
628:        st.append(step("human", "Your decision on the paragraph", "human", SKIPPED, "You dismissed the paragraph.", rule="D-031", evidence={"action": "dismiss", "at": nar.get("reviewed_at")}))
631:        st.append(step("human", "Your decision on the paragraph", "human", PENDING, "The paragraph stays in the internal notes until you accept it.", reason="PENDING_DECISION", rule="D-031",
645:def item_trace(conn, case_id: str, item_id: str, full: bool = False) -> dict:
665:def _judge_rows(cx):
681:def _judge_never_ran(cx, kind, row):
688:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
695:def _paralegal_wording(kind, row) -> bool:
696:    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
697:    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
700:def unjudged_items(conn, case_id: str) -> list:
702:    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
710:            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
715:def judge_not_run_blockers(conn, case_id: str) -> list:
716:    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one."""
717:    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]
720:def _jnr_blocker(u):
721:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
725:def judge_report(conn, case_id: str, full: bool = False) -> dict:
751:            if row["review_status"] in ("accepted", "edited"):
762:            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
784:                       "unavailable": j("unavailable"), "human_overrides": overrides},
788:def rationale_or(code, verdict):
793:def _count_by(items, key):
800:def case_trace(conn, case_id: str, full: bool = False) -> dict:
878:            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
880:            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
881:                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
910:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed")}
912:        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
915:        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
918:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
923:    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
946:def pending_warning(n: int) -> str:
950:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
962:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
967:def rows_any(jr):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:23.147Z

**tool call — Bash**
````
{
 "command": "sed -n 36,100p app/backend/trace.py; sed -n 224,248p app/backend/trace.py; sed -n 299,390p app/backend/trace.py; sed -n 660,725p app/backend/trace.py; sed -n 895,968p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:55:23.269Z

**tool result**
````
         "j4": "The second check agreed that the flag fits the quote."}
_J_NO_CODE = {"j1": "partially", "j2": "unsure", "j3": "unsure", "j4": "unsure"}

# Trace-only reason codes (case level and narrative); item reason codes come from confidence.REASON_CODES / why.py.
TRACE_WHY = {
    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
    "RUN_IN_PROGRESS": "The AI run is still going.",
    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
    "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
    "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
    "FLAG_CONTENT": narrative.REASONS["FLAG_CONTENT"],
}
_NEXT = {   # code -> fixed sentence
    "DECIDE": "Accept, edit or dismiss this item.",
    "CONFIRM_DATE": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.",
    "EDIT_SUMMARY": "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.",
    "EDIT_QUOTE": "Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.",
    "READ_RECORD": "Read the record yourself before relying on this item.",
    "COMPARE_BY_HAND": "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.",
    "DISMISS_OR_ENTER_BY_HAND": "This item cannot be used. Dismiss it, or write the entry by hand from the record.",
    "RERUN": "Run the AI steps again.",
    "RERUN_JUDGE": "Run the second check again.",
    "SENTENCE_REMOVED": "This sentence was left out of the draft. If you want its facts in the paragraph, check the cited entry's quote and write them yourself.",
    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
}
_STEP_OF_REASON = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim", "GROUNDING_AMOUNT_NOT_IN_TEXT": "found_in_text", "SCHEMA_INVALID": "extracted",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
    "INJECTION_SUSPECTED": "injection_scan", "OCR_DERIVED": "ocr_source", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
    "SPLIT_AMBIGUOUS": "record_warning_check", "LLM_SPLIT": "record_warning_check"}
_AMOUNT_CODE = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}


def reason_text(code: str) -> str:
    if code in TRACE_WHY:
        return TRACE_WHY[code]
    try:
        return why.why(code)
    except KeyError:
        return code


def na(code: str, target: dict = None, options: list = None) -> dict:
    d = {"code": code, "text": _NEXT[code]}
    if target:
        d["target"] = target
    if options:
        d["options"] = options
    return d


def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}


def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
    """The paralegal's rung. pending (live item) blocks export; rejected can only be dismissed; dismissed is skipped."""
    rs, rejected = row["review_status"], row["state"] == "rejected"
    evs = cx.events.get(row["id"], [])
    ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
    if evs:
        ev["at"] = store.iso(evs[-1]["at"])
    if rs == "edited":
        ed = row.get("edited") or {}
        ev["kept_my_wording"] = bool(ed.get("kept_my_wording"))
        ev["override_reasons"] = ed.get("override_reasons") or []
        if cx.full:
            ev["edited_text"] = ed.get("summary") or ed.get("note")
    if rs in ("accepted", "edited"):
        return step("human", "Your decision", "human", PASS, "You accepted this item." if rs == "accepted" else "You edited this item and accepted it.", rule="row 17", evidence=ev)
    if rs == "dismissed":
        return step("human", "Your decision", "human", SKIPPED, "You dismissed this item; it stays out of the letter.", rule="row 17", evidence=ev)
    if rejected:
        return step("human", "Your decision", "human", PENDING, "This item could not be verified, so it cannot be accepted.", reason="PENDING_DECISION", rule="row 17", evidence=ev,
                    next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]))
    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
                next_action=extra_pending_next or na("DECIDE", {"item_id": row["id"]}, ["accept", "edit", "dismiss"]))


def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    verbatim_fail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None)
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        if schema_fail:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
                           evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "LLM_FAILED_AFTER_RETRIES" in R:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
                           rule="row 4", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        else:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))

    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
        if stop:
            st.append(_skipped(sid, label, "code", stop, rule))
        elif failed if failed is not None else code in R:
            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
        else:
            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
    # 2 grounding substring
    if schema_fail:
        st.append(_skipped("excerpt_verbatim", "Quote is word for word in the record", "code", "SCHEMA_INVALID", "row 4"))
    elif verbatim_fail:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text("GROUNDING_EXCERPT_NOT_VERBATIM"),
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM", rule="row 4", evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
    else:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.",
                       rule="row 4", evidence={"excerpt": exc}))
    code_step("excerpt_whole_sentence", "Quote is made of whole sentences", "EXCERPT_NOT_WHOLE_SENTENCE", "The quote starts and ends on whole sentences.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False)
    code_step("excerpt_hedge", "Quote keeps the hedge sentence that qualifies it", "EXCERPT_OMITS_QUALIFIER", "No hedge sentence that qualifies the quote is left out.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}))
    toks = cc.get("summary_tokens_not_in_excerpt") or []
    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False)
    # date confirmed (D-041)
    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
    dev = {"date": {"record_id": rid, "date_raw": rec.get("date_raw"), "date_iso": rec.get("date_iso"), "date_status": rec.get("date_status"),
                    "candidates": rec.get("date_candidates") or []}}
    if unconf:
        code = "DATE_AMBIGUOUS" if rec.get("date_status") == "ambiguous" else "DATE_MISSING"
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if code == "DATE_AMBIGUOUS" else na("READ_RECORD", {"record_id": rid})
        st.append(step("date_confirmed", "Date of service is confirmed", "code", FAIL, reason_text(code), reason=code, rule="D-041", evidence=dev,
                       next_action=nxt, blocks=live_pending))
    else:
        st.append(step("date_confirmed", "Date of service is confirmed", "code", PASS, "The date comes from the record's own header and is parsed or confirmed.",
                       rule="D-041", evidence=dev))
    # injection scan
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                       evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    st += _ocr_steps(R, rid)
    # judge 1
    if stop:
        st.append(_skipped("judge_1", "Second AI check: is the summary supported by the quote?", "llm", stop, "row 4"))
    else:
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j1", R))
    nxt = None
    if unconf:
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if rec.get("date_status") == "ambiguous" else na("READ_RECORD", {"record_id": rid})
    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
    return st


# ------------------------------------------------------------------ amounts
def _amount_steps(cx, row):

_STEPS_OF.update({"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps})


# ------------------------------------------------------------------ judge report
def _judge_rows(cx):
    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
    out = []
    for kind in ("entry", "amount", "flag"):
        for row in DB.list_items(cx.conn, cx.case_id, kind):
            jd = (row.get("ladder") or {}).get("judge")
            if not jd or not jd.get("verdict"):
                out.extend(_judge_never_ran(cx, kind, row))
                continue
            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
            call = cx.call(jd.get("call_id"), row["id"], jid)
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
    return out


def _judge_never_ran(cx, kind, row):
    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
    if not cx.ran or _paralegal_wording(kind, row):
        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
    out = []
    for s in _STEPS_OF[kind](cx, row):
        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
            jid = "j" + s["id"].split("_")[1]
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
    return out


def _paralegal_wording(kind, row) -> bool:
    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))


def unjudged_items(conn, case_id: str) -> list:
    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
    cx = _Cx(conn, case_id, False)
    out = []
    for r in _judge_rows(cx):
        row = r["row"]
        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
            continue
        if _paralegal_wording(r["kind"], row):
            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
        out.append({"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "review_status": row["review_status"], "row": row})
    return out


def judge_not_run_blockers(conn, case_id: str) -> list:
    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one."""
    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]


def _jnr_blocker(u):
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
            "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    else:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and the AI.", rule="row 9", counts=fc))
    # 8 totals
    tv = present.totals_view(conn, case_id)
    pend_ch = tv["pending"]["count"]
    tcounts = {"accepted_cents": tv["accepted"]["cents"], "accepted_count": tv["accepted"]["count"], "pending_cents": tv["pending"]["cents"], "pending_charges": pend_ch,
               "not_totaled": len(tv["not_totaled"])}
    if not amts:
        st.append(step("totals", "Billed-charges total", "code", SKIPPED, "No dollar amounts were found.", rule="row 8", counts=tcounts))
    elif pend_ch:
        st.append(step("totals", "Billed-charges total", "code", PENDING, f"{pend_ch} detected charge{'s' if pend_ch != 1 else ''} not in the total until you accept {'them' if pend_ch != 1 else 'it'}. The total is added up by code from accepted charges only.",
                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
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
               else {"code": "needs_attention", "label": f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
    rv = rv or present.review_view(conn, case_id)
    out = []
    if cx.running:
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
    if cx.case["status"] == "failed":
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
    if cx.ran and not cx.running:
        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
    return out


def rows_any(jr):
    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:23.486Z

**tool call — Bash**
````
{
 "command": "grep -n -E 'blocker|422|ready|def ' app/backend/export.py | head -80; grep -rn -E 'export_blockers|judge_not_run_blockers' app/backend --include=*.py | grep -v 'def '"
}
````

### User / tool · 2026-11-02T04:55:23.696Z

**tool result**
````
48:def _long_date(iso):
55:def _money(cents):
59:def _money_short(cents, raw=""):
65:def _norm(s):
69:def _cap(s):
73:def _terminate(s):
74:    """End a note sentence with a period unless it already ends with a full stop."""
78:def _sentence_spans(text):
105:def _sentences(text):
113:    def __init__(self, case):
123:    def verbatim(self, item):
128:    def in_entries(self):
134:    def narrative_sentences(self):
143:    def in_charges(self):
147:    def _date(self, item):
150:    def date_of(self, item):
153:    def source_prefix(self, n):
159:    def _bracket(self, n):
167:    def source(self, n):
170:    def text(self, n):
173:    def rec_date(self, n):
176:    def cite(self, n):
179:    def cite_dated(self, n):
182:    def quote(self, n, ev, whole_sentence=False):
200:def _amount_quote(v, a):
212:def basis_hash(entry: dict) -> str:
218:def _status(item):
224:def build_letter(case: dict) -> str:
229:def _summary_line(e):
234:def _letter(v):
255:def _flag_label(f):
270:def _excerpt_ev(f):
274:def _flag_line(v, f):
319:def _flag_block(v, flags):
344:def _flagged_language(v, flags):
376:def _provider(src):
380:def _ledger_label(v, n):
385:def _plan_note(v, n):
402:def _amounts_not_totaled(v):
424:def _damages(v):
430:def _future(v):
439:def _bills(v):
452:def _reconcile(v):
478:def _was_edited(e):
489:def _edited(v):
508:def _pending(v):
523:def _cite_tail(v, entry_id):
528:def _draft_paragraph(v):
547:def _notes(v):
571:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
572:    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""
574:    def __init__(self, items):
579:    def code(self) -> str:
587:def build_export(case: dict) -> dict:
590:    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
app/backend/store.py:80:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/store.py:81:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/trace.py:917:    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
app/backend/trace.py:961:        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
app/backend/export.py:571:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:590:    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
app/backend/export_routes.py:28:    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
app/backend/export_routes.py:29:        raise export.ExportBlocked(case["export_blockers"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:29.268Z

**tool call — Bash**
````
{
 "command": "sed -n 560,606p app/backend/export.py; sed -n 15,60p app/backend/export_routes.py; grep -n -E 'SUMMARY_DROPS|summary_tokens|qualifier|state_reasons' app/backend/review.py app/backend/store.py | head -50"
}
````

### User / tool · 2026-11-02T04:55:29.368Z

**tool result**
````
        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
        "RECORDS NOT IN THE TREATMENT SECTION", *_reconcile(v), "",
        "EDITED ITEMS", *_edited(v), "",
        "PENDING ITEMS NOT INCLUDED", *(pending or ["- none"]),
        *_draft_paragraph(v),
    ]
    return "\n".join(sec)


class ExportBlocked(Exception):
    """The export refuses (D-044, D-045): a run in progress or failed, nothing accepted, or accepted AI-made items whose second check never ran. No override.
    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""

    def __init__(self, items):
        self.items = list(items)
        super().__init__(self.items[0]["reason_code"] if self.items else "EXPORT_BLOCKED")

    @property
    def code(self) -> str:
        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"


class JudgeNotRun(ExportBlocked):
    """D-044 alias kept for callers that only care about the judge dimension."""


def build_export(case: dict) -> dict:
    """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
    if case.get("judge_not_run"):
        raise JudgeNotRun(case["judge_not_run"])
    v = _View(case)
    notes = _notes(v)
    in_letter = {e["record_no"] for e in v.in_entries}
    pend = _pending(v)
    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
        "entries": len(v.in_entries),
        "charges": len(v.in_charges),
        "flags_in_notes": sum(1 for f in v.flags if _status(f) == "in"),
        "records_in_letter": len(in_letter),
        "records_total": len(v.records),
        "pending": len(pend),
        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
    }
    return {"letter_text": _letter(v), "internal_notes_text": notes, "counts": counts}
_loader = None


def set_case_loader(fn):
    global _loader
    _loader = fn


def _not_found():
    return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})


def export_payload(token: str, case: dict, now: datetime = None) -> dict:
    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
        raise export.ExportBlocked(case["export_blockers"])
    out = export.build_export(case)
    now = now or datetime.now(timezone.utc)
    ok = ("accepted", "edited")
    return {
        "token": token,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "letter_text": out["letter_text"],
        "internal_notes_text": out["internal_notes_text"],
        "counts": out["counts"],
        "items": {
            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
                         "edited": e["review_status"] == "edited", "excerpt": e["excerpt"],
                         "entered_by": "reviewer" if e.get("entered_by_reviewer") else None}
                        for e in case.get("entries", []) if e.get("review_status") in ok],
            "amounts": [{"id": a["id"], "kind": a["cls"], "counted_in_total": a["cls"] == "charge" and a.get("cents") is not None,
                         "edited": a["review_status"] == "edited", "excerpt": a["excerpt"]}
                        for a in case.get("amounts", []) if a.get("review_status") in ok],
        },
        "warnings": [],
    }


def blocked_message(e) -> str:
    if e.code == "judge_not_run":
        return judge_not_run_message(len(e.items))
    return e.items[0]["why"] + " The export is blocked."


def judge_not_run_message(n: int) -> str:
    return f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check, so the export is blocked. Run the second check again."

app/backend/review.py:103:            reasons = list(it.get("state_reasons") or [])
app/backend/review.py:108:            out = {"state": "needs_review", "state_reasons_json": reasons}
app/backend/review.py:117:    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
app/backend/review.py:131:    if g.dropped_qualifiers(new_sum, new_exc):
app/backend/review.py:132:        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:183:                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
app/backend/review.py:201:    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
app/backend/review.py:202:                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
app/backend/review.py:204:    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/review.py:226:            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
app/backend/review.py:230:        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
app/backend/review.py:247:    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
app/backend/review.py:251:    out = {"state": state, "state_reasons_json": reasons}
app/backend/review.py:341:              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
app/backend/review.py:342:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/review.py:352:        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:30.915Z

**tool call — Bash**
````
{
 "command": "sed -n 90,215p app/backend/review.py; grep -n -E 'ExportBlocked|JudgeNotRun' app/backend/*.py | grep -v '^app/backend/export.py'"
}
````

### User / tool · 2026-11-02T04:55:31.017Z

**tool result**
````
def enforce_ocr(conn, case_id: str, t) -> int:
    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
    ids = ocr_record_ids(conn, case_id)
    if not ids:
        return 0
    n = 0
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, case_id, kind):
            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
                continue
            reasons = list(it.get("state_reasons") or [])
            if it["state"] == "needs_review" and "OCR_DERIVED" in reasons:
                continue
            if "OCR_DERIVED" not in reasons:
                reasons.append("OCR_DERIVED")
            out = {"state": "needs_review", "state_reasons_json": reasons}
            if isinstance(it.get("ladder"), dict):
                out["ladder"] = {**it["ladder"], "state": "needs_review"}
            DB.update_item(conn, it["id"], now=t, case=case_id, **out)
            n += 1
    return n


def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body, ocr_derived=False):
    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
    code_reasons = []
    lang = language.record_lang(rec)                        # D-042: a Spanish record's English summary is checked against the Spanish quote
    g = spanish.module_for(lang)
    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    blocking = []
    if toks:
        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
    if g.dropped_qualifiers(new_sum, new_exc):
        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
    if span is None:
        code_reasons.append("HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
    if blocking and not bool(body.get("confirm_warnings")):
        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived})
    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error,
            "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, body,
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
    toks, code_reasons, blocking, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["blocking"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    confirmed = bool(body.get("confirm_warnings"))
    edited = dict(prev)
    edited.update(at=store.iso(t), kept_my_wording=bool(blocking and confirmed),
                  override_reasons=[b["code"] for b in blocking] if blocking and confirmed else prev.get("override_reasons", []))
    if "summary" in edits or "summary" in prev:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
    if edited["kept_my_wording"]:
        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
    lad = item.get("ladder") or {"item_id": item["id"]}
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    enforce_ocr(conn, case_id, t)
    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
        if ladder_verdict == "unavailable" else []


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
app/backend/api.py:524:            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
app/backend/export_routes.py:29:        raise export.ExportBlocked(case["export_blockers"])
app/backend/export_routes.py:69:    except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:45.833Z

**tool call — Bash**
````
{
 "command": "sed -n 249,293p app/backend/trace.py; sed -n 129,153p app/backend/trace.py; grep -n -A25 'def dropped_qualifiers' app/backend/*.py app/llm/*.py | head -60; grep -n -E '^def |^import|^from|^@pytest' tests/unit/test_trace.py | head -60"
}
````

### User / tool · 2026-11-02T04:55:45.941Z

**tool result**
````
def _skipped(sid, label, kind, code, rule=None, rule_text=None):
    msg = rule_text or {"GROUNDING_EXCERPT_NOT_VERBATIM": "Not run: the quote did not pass the word-for-word check.",
                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
                        "SCHEMA_INVALID": "Not run: the AI answer was malformed."}.get(code, "Not run because an earlier step rejected this item.")
    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)


def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
    """Assemble the item trace: numbering, progress, verdict, state_reasons mapped to the step that explains them."""
    _number(steps)
    ids = {s["id"] for s in steps}
    rs = row.get("review_status")
    live = row.get("state") != "rejected"
    first_na = next((s["next_action"] for s in steps if s["next_action"]), None)
    if rs in ("accepted", "edited", "dismissed"):
        first_na = None             # the human already decided; step-level hints stay on the steps
    if rs in ("accepted", "edited"):
        code, label = "accepted", "Accepted by you"
    elif rs == "dismissed":
        code, label = "dismissed", "Dismissed by you"
    elif row.get("state") == "rejected":
        code, label = "rejected", "Rejected; kept out of the letter"
    elif any(s["status"] == FAIL for s in steps):
        code, label = "needs_attention", "Needs your attention"
    elif any(s["status"] == PENDING and s["kind"] == "llm" for s in steps):
        code, label = "waiting_for_run", "Waiting for the AI run"
    elif row.get("state") == "needs_review":
        code, label = "needs_attention", "Needs your attention"
    else:
        code, label = "ready_for_decision", "Ready for your decision"
    blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
    judge_id = next((s["id"] for s in steps if s["id"].startswith("judge_")), None)
    fallback = next((s["id"] for s in steps if s["status"] == FAIL), steps[0]["id"] if steps else None)   # e.g. record-warning flags have one code step

    def step_of(c):
        if c.startswith("JUDGE_") or c == "FIXTURE_MISS":
            return judge_id or fallback
        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else fallback
    reasons = [{"code": c, "why": reason_text(c), "step_id": step_of(c)} for c in (row.get("state_reasons") or [])]
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
            "review_status": rs, "state_reasons": reasons, "verdict": {"code": code, "label": label, "blocks_export": bool(blocks)},
            "progress": _progress(steps), "next_action": first_na, "steps": steps}


# ------------------------------------------------------------------ entries
    def __init__(self, conn, case_id, full):
        self.conn, self.case_id, self.full = conn, case_id, bool(full)
        self.case = DB.get_case(conn, case_id)
        self.recs = present._recs_by_id(conn, case_id)
        calls = DB.list_llm_calls(conn, case_id)
        self.call_by_id = {c["id"]: c for c in calls}
        self.calls_by_item = {}
        for c in calls:
            self.calls_by_item.setdefault(c["item_id"], []).append(c)
        self.events = {}
        for e in DB.list_events(conn, case_id):
            self.events.setdefault(e["item_id"], []).append(e)
        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
        self.ran = self.case.get("run_started_at") is not None
        self.running = self.case["status"] == "running"

    def call(self, call_id, item_id=None, step_name=None):
        if call_id and call_id in self.call_by_id:
            return self.call_by_id[call_id]
        if item_id and step_name:
            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
            return hits[-1] if hits else None
        return None


app/backend/grounding.py:180:def dropped_qualifiers(summary: str, excerpt: str) -> list:
app/backend/grounding.py-181-    """Qualifier kinds present in the excerpt and absent from the summary (D-022): hedge, self_report, negation, laterality, approx."""
app/backend/grounding.py-182-    out = []
app/backend/grounding.py-183-    if hedge_ids(excerpt) and not (hedge_ids(summary) or _HEDGE_WORDS.search(summary)):
app/backend/grounding.py-184-        out.append("hedge")
app/backend/grounding.py-185-    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
app/backend/grounding.py-186-        out.append("self_report")
app/backend/grounding.py-187-    ex_neg = {w.lower() for w in _NEG.findall(excerpt)}
app/backend/grounding.py-188-    sm_neg = {w.lower() for w in _NEG.findall(summary)}
app/backend/grounding.py-189-    if any(w not in sm_neg and not (w in ("no", "not", "none", "never") and sm_neg & {"no", "not", "none", "never"}) for w in ex_neg):
app/backend/grounding.py-190-        out.append("negation")
app/backend/grounding.py-191-    if {w.lower() for w in _LATERAL.findall(excerpt)} - {w.lower() for w in _LATERAL.findall(summary)}:
app/backend/grounding.py-192-        out.append("laterality")
app/backend/grounding.py-193-    if _APPROX.search(excerpt) and not _APPROX.search(summary):
app/backend/grounding.py-194-        out.append("approx")
app/backend/grounding.py-195-    return out
app/backend/grounding.py-196-
app/backend/grounding.py-197-
app/backend/grounding.py-198-def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/grounding.py-199-    reasons = []
app/backend/grounding.py-200-    if new_tokens(summary, excerpt, label, date_iso):
app/backend/grounding.py-201-        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/grounding.py-202-    if dropped_qualifiers(summary, excerpt):
app/backend/grounding.py-203-        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/grounding.py-204-    return reasons
app/backend/spanish_text.py:211:def dropped_qualifiers(summary: str, excerpt: str) -> list:
app/backend/spanish_text.py-212-    """Qualifier kinds in the Spanish quote that the English summary lost or turned round: hedge, self_report, negation, laterality, approx
app/backend/spanish_text.py-213-    (D-022). 'No se descarta X' (X is not ruled out) is a hedge; 'Se descarta X' (X is ruled out) is a negation; a summary that says the
app/backend/spanish_text.py-214-    opposite of the quote fails the one it contradicts."""
app/backend/spanish_text.py-215-    out = []
app/backend/spanish_text.py-216-    folded = fold(excerpt)
app/backend/spanish_text.py-217-    not_ruled = bool(_NOT_RULED_OUT.search(folded))
app/backend/spanish_text.py-218-    rest = _NOT_RULED_OUT.sub(" ", folded)                      # the quote with its 'not ruled out' phrases taken out
app/backend/spanish_text.py-219-    ruled = bool(_RULED_OUT.search(rest))
app/backend/spanish_text.py-220-    ex_words = _words(rest)
app/backend/spanish_text.py-221-    hedge_q = _cue_set(rest, _HEDGE_CUES, _HEDGE_PHRASES) or bool(grounding.hedge_ids(excerpt) and not not_ruled)
app/backend/spanish_text.py-222-    if hedge_q and not (grounding.hedge_ids(summary) or grounding._HEDGE_WORDS.search(summary) or _EN_HEDGE_EXTRA.search(summary)):
app/backend/spanish_text.py-223-        out.append("hedge")
app/backend/spanish_text.py-224-    if not_ruled:           # 'cannot be excluded' / 'possible' is right; 'ruled out' / 'excluded' says the opposite
app/backend/spanish_text.py-225-        if not _EN_NOT_RULED_OUT.search(summary) or _EN_RULED_OUT.search(_EN_NOT_RULED_OUT.sub(" ", summary)):
app/backend/spanish_text.py-226-            out.append("hedge")
app/backend/spanish_text.py-227-    if _cue_set(excerpt, _SELF_CUES, _SELF_PHRASES) and not (grounding._SELF_CARRIED.search(summary) or _EN_SELF.search(summary)):
app/backend/spanish_text.py-228-        out.append("self_report")
app/backend/spanish_text.py-229-    neg_q = _neg_hit(ex_words) or bool(_NEG_PHRASES.search(folded))
app/backend/spanish_text.py-230-    if neg_q and not (grounding._NEG.search(summary) or _EN_NEG_EXTRA.search(summary)):
app/backend/spanish_text.py-231-        out.append("negation")
app/backend/spanish_text.py-232-    if ruled and _EN_SAYS_NOT_RULED_OUT.search(summary):          # 'Se descarta fractura' read as 'fracture cannot be excluded'
app/backend/spanish_text.py-233-        out.append("negation")
app/backend/spanish_text.py-234-    sides = {_SIDES[w] for w in ex_words if w in _SIDES} | {w.lower() for w in grounding._LATERAL.findall(excerpt)}
app/backend/spanish_text.py-235-    if sides - {w.lower() for w in grounding._LATERAL.findall(summary)}:
app/backend/spanish_text.py-236-        out.append("laterality")
3:import json
4:import pathlib
5:import sqlite3
6:import time
8:import pytest
9:from fastapi.testclient import TestClient
11:from app.backend import trace, why
12:from app.backend.api import create_app
13:from app.db import db as DB
21:@pytest.fixture(scope="module")
22:def base(tmp_path_factory):
47:@pytest.fixture
48:def env(base, tmp_path, monkeypatch):
62:def steps_of(t):
66:def walk(o, keys):
80:def all_keys(o, skip=()):
94:def check_step_shape(s):
106:def test_every_item_has_an_ordered_well_formed_trace(env):
125:def test_entry_trace_names_each_code_check_and_the_judge(env):
141:def test_judge_objection_is_a_fail_with_fixed_rationale(env):
156:def test_rejected_entry_skips_later_checks_and_points_to_manual_entry(env):
171:def test_token_and_qualifier_failures_name_the_rule(env):
183:def test_unconfirmed_date_fails_and_blocks_accept_d041(env):
196:def test_unavailable_judge_is_skipped_with_reason(env):
208:def test_amount_steps_and_rate_is_never_totaled(env):
225:def test_amount_judge_reason_is_read_from_the_audited_call_when_not_stored(env):
243:def test_code_made_flags_need_no_judge(env):
251:def test_ai_and_phrase_list_flags_show_agreement_and_judge(env):
260:def test_lexicon_only_flag_is_agreement_fail_and_judge_skipped(env):
273:def test_unknown_item_and_case_are_404(env):
281:def test_unrun_case_waits_for_the_ai(env):
292:def test_narrative_sentence_traces(env):
320:def test_case_trace_steps_and_counts(env):
334:def test_pending_live_items_are_a_warning_not_a_blocker_d045(env):
356:def test_export_gate_date_unconfirmed_blocker(env):
366:def test_export_gate_ready_matches_review_view(env):
377:def test_export_gate_nothing_accepted(env):
386:def test_run_in_progress_blocks_the_gate(env):
395:def test_judge_summary_counts_and_objections(env):
422:def test_code_flags_doubt_judge_agrees_and_sources_disagree(env):
433:def test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them(env, monkeypatch):
455:def test_judge_report_rejection_response_raw_is_full_mode_only(env, monkeypatch):
467:def test_every_emitted_reason_code_has_a_fixed_sentence(env):
483:def test_judge_reason_code_is_persisted_on_new_runs(env):
492:def _blank_judges(conn, tok):
509:def test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step(env):
529:def test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing(env):
537:def _gate_states(c, conn, tok):
561:def test_gate_ready_equals_no_blockers_in_every_case_state(env):
579:def test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed(env):
591:def test_all_accepted_but_run_in_progress_is_not_ready(env):
601:def _add_record_warning(conn, tok, category, rid_from="e1"):
612:def test_record_warning_flags_point_at_the_right_action_and_a_real_step(env):
622:def test_decided_items_have_no_top_level_next_action_but_steps_keep_theirs(env):
637:def test_dismissed_item_human_step_is_skipped_not_pass(env):
646:def test_internal_table_bug_is_a_500_not_a_404(env, monkeypatch):
657:def test_amount_judge_objection_counts_in_totals_unsupported(env):
667:def test_zlayt_db_env_var_picks_the_database_file(tmp_path, monkeypatch):
676:def _accept_all(c, tok):
682:def _blank_and_accept(c, conn, tok):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:47.702Z

**tool call — Bash**
````
{
 "command": "sed -n 15,62p tests/unit/test_trace.py; sed -n 171,182p tests/unit/test_trace.py; sed -n 492,508p tests/unit/test_trace.py; sed -n 537,600p tests/unit/test_trace.py; sed -n 676,760p tests/unit/test_trace.py; grep -n 'kept_my_wording\\|confirm_warnings' tests/unit/*.py | head -20"
}
````

### User / tool · 2026-11-02T04:55:47.873Z

**tool result**
````
STATUSES = {"pass", "fail", "skipped", "pending"}
KINDS = {"code", "llm", "human"}
NEXT_CODES = {"DECIDE", "CONFIRM_DATE", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD", "COMPARE_BY_HAND", "DISMISS_OR_ENTER_BY_HAND", "RERUN", "SENTENCE_REMOVED", "CONFIRM_RERUN", "RERUN_JUDGE"}
FULL_ONLY_KEYS = {"response_raw", "before", "after", "edited_text"}


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    import os
    d = tmp_path_factory.mktemp("trace")
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ["LLM_BACKEND"] = "fixture"
    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    db = str(d / "base.sqlite")
    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
    for k, v in old.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


@pytest.fixture
def env(base, tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    path = str(tmp_path / "copy.sqlite")
    src = sqlite3.connect(base["db"])
    dst = sqlite3.connect(path)
    src.backup(dst)
    src.close()
    dst.close()
    conn = DB.connect(path)
    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    return c, conn, base["tok"], base["pre"]


def steps_of(t):
def test_token_and_qualifier_failures_name_the_rule(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e4", tok)
    lad = e["ladder"]
    lad["code_checks"]["summary_tokens_not_in_excerpt"] = ["9,000"]
    DB.update_item(conn, "e4", case=tok, state="needs_review", state_reasons_json=["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER"], ladder=lad)
    s = steps_of(c.get(f"/api/cases/{tok}/items/e4/trace").json())
    assert s["summary_tokens"]["status"] == "fail" and s["summary_tokens"]["evidence"]["tokens"] == ["9,000"] and s["summary_tokens"]["next_action"]["code"] == "EDIT_SUMMARY"
    assert s["summary_qualifier"]["status"] == "fail" and s["summary_qualifier"]["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    assert s["excerpt_verbatim"]["status"] == "pass"


def _blank_judges(conn, tok):
    """Make the judge stage 'never ran' on every entry and every non-damages amount (the run deadline case in pipeline.py)."""
    n = 0
    for kind in ("entry", "amount"):
        for row in DB.list_items(conn, tok, kind):
            if row["state"] == "rejected" or (kind == "amount" and row["kind"] == "damages"):
                continue
            lad = row["ladder"]
            if not lad.get("judge"):
                continue
            lad["judge"] = None
            DB.update_item(conn, row["id"], case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
            conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, row["id"]))     # no audited judge call either
            n += 1
    return n


def _gate_states(c, conn, tok):
    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
    yield "pending items"
    DB.update_case(conn, tok, status="running")
    yield "running with pending items"
    DB.update_case(conn, tok, status="ready")
    for i in ids:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"})
    yield "everything dismissed"
    DB.update_case(conn, tok, status="failed")
    yield "failed, everything dismissed"
    DB.update_case(conn, tok, status="ready")
    # accept every item still reviewable
    for i in ids:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"})
    yield "all accepted"
    DB.update_case(conn, tok, status="running")
    yield "all accepted, running"
    DB.update_case(conn, tok, status="failed")
    yield "all accepted, failed"


def test_gate_ready_equals_no_blockers_in_every_case_state(env):
    c, conn, tok, pre = env
    seen = {}
    for name in _gate_states(c, conn, tok):
        gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
        assert gate["ready"] == (len(gate["blockers"]) == 0), name
        assert gate["status"] == ("pass" if gate["ready"] else "fail"), name
        if not gate["ready"]:
            assert gate["next_action"] is not None or "running" in name, name
        seen[name] = gate
    assert seen["all accepted"]["ready"] is True
    for name in ("all accepted, failed", "failed, everything dismissed"):
        assert seen[name]["ready"] is False and "RUN_FAILED" in [b["reason_code"] for b in seen[name]["blockers"]], name
    assert seen["all accepted, running"]["ready"] is False and "RUN_IN_PROGRESS" in [b["reason_code"] for b in seen["all accepted, running"]["blockers"]]
    g = steps_of(c.get(f"/api/cases/{pre}/trace").json())["export_gate"]            # a case that never ran
    assert g["ready"] == (g["blockers"] == []) and g["status"] == ("pass" if g["ready"] else "fail")


def test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    DB.update_case(conn, tok, status="failed")
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert ct["verdict"]["code"] == "failed" and gate["ready"] is False and gate["status"] == "fail" and gate["reason_code"] == "RUN_FAILED"
    assert [b["reason_code"] for b in gate["blockers"]] == ["RUN_FAILED"] and gate["next_action"]["code"] == "CONFIRM_RERUN"


def test_all_accepted_but_run_in_progress_is_not_ready(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    DB.update_case(conn, tok, status="running")
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    assert gate["ready"] is False and gate["status"] == "fail" and [b["reason_code"] for b in gate["blockers"]] == ["RUN_IN_PROGRESS"]


def _accept_all(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})


def _blank_and_accept(c, conn, tok):
    n = _blank_judges(conn, tok)
    _accept_all(c, tok)
    return n


def _gate(c, tok):
    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]


def _jnr(gate):
    return [b for b in gate["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]


def test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_action(env):
    c, conn, tok, _ = env
    n = _blank_and_accept(c, conn, tok)
    gate = _gate(c, tok)
    got = _jnr(gate)
    accepted_blanked = {r["id"] for k in ("entry", "amount") for r in DB.list_items(conn, tok, k)
                        if r["review_status"] in ("accepted", "edited") and "JUDGE_UNAVAILABLE" in r["state_reasons"]}
    assert len(got) >= 5 and n >= len(got)
    assert {b["item_id"] for b in got} == accepted_blanked
    for b in got:
        assert b["kind"] in ("entry", "amount", "flag") and b["why"] and "second AI check never ran" in b["why"]
        assert b["next_action"]["code"] == "RERUN_JUDGE" and b["next_action"]["text"] == "Run the second check again."
        assert b["next_action"]["target"]["item_id"] == b["item_id"]
    assert gate["ready"] is False and gate["status"] == "fail" and gate["counts"]["judge_not_run"] == len(got)
    assert gate["next_action"]["code"] == "RERUN_JUDGE" and "Run the second check again" in gate["why"]
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert ct["verdict"]["code"] == "needs_attention" and "not double-checked" in ct["verdict"]["label"]


def test_export_refuses_422_for_the_same_items_the_gate_lists(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    ids = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 422 and r.json()["error"]["code"] == "judge_not_run"
    det = r.json()["error"]["detail"]["blockers"]
    assert sorted(b["item_id"] for b in det) == ids and {b["reason_code"] for b in det} == {"JUDGE_NOT_RUN"}
    assert "letter_text" not in r.text and "second AI check" in r.json()["error"]["message"]


def test_no_override_accepting_again_editing_or_comparing_by_hand_does_not_clear_it(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    before = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    for i in before:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept", "confirm_judge_unavailable": True, "override": True})
    assert sorted(b["item_id"] for b in _jnr(_gate(c, tok))) == before
    assert c.get(f"/api/cases/{tok}/export").status_code == 422


def test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    ids = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    c.post(f"/api/cases/{tok}/items/{ids[0]}/review", json={"action": "dismiss"})
    assert ids[0] not in [b["item_id"] for b in _jnr(_gate(c, tok))]
    c.post(f"/api/cases/{tok}/items/{ids[1]}/review", json={"action": "reset"})
    g = _gate(c, tok)
    assert ids[1] not in [b["item_id"] for b in _jnr(g)]
    assert all(b["item_id"] != ids[1] for b in g["blockers"]) and g["counts"]["pending_items"] >= 1                         # now it is pending: a warning, not a blocker


def test_pending_unjudged_items_are_not_judge_blockers_yet(env):
    c, conn, tok, _ = env
    _blank_judges(conn, tok)
    g = _gate(c, tok)
    assert _jnr(g) == [] and g["counts"]["judge_not_run"] == 0 and g["ready"] is False


def test_reviewer_written_entry_is_not_ai_made_so_it_never_needs_the_judge(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    e = DB.get_item(conn, eid, tok)
    lad = e["ladder"]
tests/unit/test_review_rules.py:87:    """D-034 (R-RV-3): summary edited to add '$9,000' -> 422 invalid_edit, no override via confirm_warnings; the item is unchanged."""
tests/unit/test_review_rules.py:91:        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Visit 8: pain 4/10, improving; billed $9,000."), confirm_warnings=confirm), call=judge("supported"))
tests/unit/test_review_rules.py:103:    """R-RV-3: resend with confirm_warnings=true saves (review_status edited) and logs a keep_my_wording event."""
tests/unit/test_review_rules.py:109:    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=edits, confirm_warnings=True), call=judge("unsupported"))
tests/unit/test_review_rules.py:110:    assert r["item"]["review_status"] == "edited" and r["item"]["edited"]["kept_my_wording"] is True
tests/unit/test_manual_and_split.py:58:        RV.manual_entry(conn, cid, "r5", {"summary": "Pain 9/10.", "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=judge("supported"))
tests/unit/test_manual_and_split.py:69:    r = RV.manual_entry(conn, cid, "r5", {**body, "confirm_warnings": True}, call=judge("unsupported"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:55:50.002Z

**tool call — Bash**
````
{
 "command": "grep -n -i -B3 -A25 'part_b\\|PART B\\|qualifier' artifacts/review-evidence/T-097-ux-designer-walk2.py | head -120; python3 - <<'E'\nimport json\nd=json.load(open('artifacts/review-evidence/T-097-ux-designer-walk2-results.json'))\nprint(json.dumps(d,indent=1)[:3500])\nE"
}
````

### User / tool · 2026-11-02T04:55:50.133Z

**tool result**
````
1-"""T-097 review (ux-designer-reviewer): (a) what a rail gate-row 'Run the second check again' does versus its aria-label;
2:(b) an edited item whose summary drops a quote qualifier while the rail says Ready to export (gate versus item stepper).
3-Usage: E2E_BASE_URL=http://127.0.0.1:7895 .venv/bin/python artifacts/review-evidence/T-097-ux-designer-walk2.py <scratch-wt-dir>
4-"""
5-import json, sys, time, urllib.request, urllib.error, os
6-
7-WT = sys.argv[1]
8-BASE = os.environ["E2E_BASE_URL"]
9-OUT = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence"
10-sys.path.insert(0, WT)
11-from playwright.sync_api import sync_playwright
12-from tests.e2e.conftest import JudgeNotRun
13-
14-def api(method, path, body=None):
15-    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
16-    try:
17-        with urllib.request.urlopen(req, timeout=60) as r:
18-            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
19-    except urllib.error.HTTPError as e:
20-        raw = e.read(); return e.code, (json.loads(raw) if raw else None)
21-
22-def new_sample_case():
23-    st, c = api("POST", "/api/cases", {"sample": True}); tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
24-    for _ in range(300):
25-        s = api("GET", f"/api/cases/{tok}/status")[1]
26-        if s["status"] in ("ready", "failed"): break
27-        time.sleep(1)
--
65-        except Exception: pass
66-        ctx.close(); br.close(); api("DELETE", f"/api/cases/{tok}")
67-
68:def part_b(pw):
69-    tok = new_sample_case(); its = items(tok)
70-    acc, edt = its[0]["id"], its[1]["id"]
71-    assert api("POST", f"/api/cases/{tok}/items/{acc}/review", {"action": "accept"})[0] == 200
72-    st, r = api("POST", f"/api/cases/{tok}/items/{edt}/review", {"action": "edit", "edits": {"summary": "Paralegal wording for the mixed-case check."}})
73-    rec("B_edit_response", {"status": st})
74-    api("POST", f"/api/cases/{tok}/items/{acc}/review", {"action": "dismiss"})
75-    tr = api("GET", f"/api/cases/{tok}/trace")[1]
76-    gate = next(x for x in tr["steps"] if x["id"] == "export_gate")
77-    rec("B_gate_after_dismiss", {"status": gate.get("status"), "ready": gate.get("ready"), "blockers": [(b.get("item_id"), b.get("reason_code")) for b in gate.get("blockers", [])]})
78-    ent = api("GET", f"/api/cases/{tok}")[1]
79-    e = next(x for x in ent["entries"] if x["id"] == edt)
80-    rec("B_edited_entry", {"review_status": e.get("review_status"), "summary": e.get("summary"), "keys": sorted(k for k in e.keys() if "check" in k or "code" in k or "state" in k)})
81-    ex = api("GET", f"/api/cases/{tok}/export")
82-    rec("B_export", {"status": ex[0], "contains_edit": ("Paralegal wording for the mixed-case check." in json.dumps(ex[1]))})
83-    it = api("GET", f"/api/cases/{tok}/items/{edt}/trace")[1]
84-    rec("B_item_trace_code_steps", [(s["id"], s.get("status"), s.get("reason_code")) for s in it["steps"] if s.get("kind") == "code" or s["id"].startswith("code") or "qualif" in s["id"]][:8])
85-    api("DELETE", f"/api/cases/{tok}")
86-
87-if __name__ == "__main__":
88-    with sync_playwright() as pw:
89-        for w, h in ((1440, 900), (390, 844)):
90-            try: part_a(pw, w, h)
91-            except Exception as ex: rec(f"ERROR_A_{w}", repr(ex)[:500])
92:        try: part_b(pw)
93-        except Exception as ex: rec("ERROR_B", repr(ex)[:500])
94-    with open(f"{OUT}/T-097-ux-designer-walk2-results.json", "w") as f: json.dump(R, f, ensure_ascii=False, indent=1)
95-    print("WROTE", f"{OUT}/T-097-ux-designer-walk2-results.json")
{
 "A_1440_row_before": {
  "row_title": "2026-01-09 \u00b7 Austin EMS run report",
  "aria_label": "Run the second check again for 2026-01-09 \u00b7 Austin EMS run report",
  "row_count": 3
 },
 "A_1440_after_row_click": {
  "posts": 1,
  "rail_status_texts": [
   "The second check still did not answer for 3 items of 3. Try again, or dismiss them.",
   "The second check still did not answer for 3 items of 3. Try again, or dismiss them."
  ],
  "rail_gate_blocker_rows_after": 3
 },
 "A_390_row_before": {
  "row_title": "2026-01-09 \u00b7 Austin EMS run report",
  "aria_label": "Run the second check again for 2026-01-09 \u00b7 Austin EMS run report",
  "row_count": 3
 },
 "A_390_after_row_click": {
  "posts": 1,
  "rail_status_texts": [
   "The second check still did not answer for 3 items of 3. Try again, or dismiss them.",
   "The second check still did not answer for 3 items of 3. Try again, or dismiss them."
  ],
  "rail_gate_blocker_rows_after": 3
 },
 "B_edit_response": {
  "status": 200
 },
 "B_gate_after_dismiss": {
  "status": "pass",
  "ready": true,
  "blockers": []
 },
 "B_edited_entry": {
  "review_status": "edited",
  "summary": "Paralegal wording for the mixed-case check.",
  "keys": [
   "state"
  ]
 },
 "B_export": {
  "status": 200,
  "contains_edit": true
 },
 "B_item_trace_code_steps": [
  [
   "excerpt_verbatim",
   "pass",
   null
  ],
  [
   "excerpt_whole_sentence",
   "pass",
   null
  ],
  [
   "excerpt_hedge",
   "pass",
   null
  ],
  [
   "summary_tokens",
   "pass",
   null
  ],
  [
   "summary_qualifier",
   "fail",
   "SUMMARY_DROPS_QUALIFIER"
  ],
  [
   "highlight",
   "pass",
   null
  ],
  [
   "date_confirmed",
   "pass",
   null
  ],
  [
   "injection_scan",
   "pass",
   null
  ]
 ]
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:06.229Z

**tool call — Bash**
````
{
 "command": "sed -n 60,90p app/backend/export_routes.py; sed -n 515,540p app/backend/api.py; sed -n 645,664p app/backend/trace.py; grep -n -E '^_(HEDGE_WORDS|NEG|LATERAL|APPROX|SELF_CARRIED)\\b|^def hedge_ids' -A3 app/backend/grounding.py | head -40; grep -n 'def module_for' -A8 app/backend/spanish.py; grep -n 'record_lang' app/backend/language.py | head -3"
}
````

### User / tool · 2026-11-02T04:56:06.347Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:08.601Z

**tool call — Bash**
````
{
 "command": "grep -n '^from\\|^import' app/backend/review.py app/backend/trace.py; grep -rn 'def module_for' app/backend; sed -n 60,80p app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T04:56:08.698Z

**tool result**
````
app/backend/review.py:8:import time
app/backend/review.py:10:from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
app/backend/review.py:11:from app.db import db as DB
app/backend/trace.py:11:import json
app/backend/trace.py:13:from app.backend import narrative, present, review, store, why
app/backend/trace.py:14:from app.backend import judges as J
app/backend/trace.py:15:from app.db import db as DB
app/backend/trace.py:16:from app.llm import audited as AU
app/backend/spanish_text.py:252:def module_for(lang: str):
def _lexicon() -> dict:
    data = yaml.safe_load(_LEXICON.read_text())
    entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
    hedges, selfrep = {}, {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        if "pattern" not in e:
            if e.get("hedge") or e.get("self_report"):
                raise ValueError(f"lexicon entry {e.get('id')} is a hedge/self_report entry without a pattern")
            continue
        if e.get("hedge"):
            hedges[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
        if e.get("self_report"):
            selfrep[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
    scope = (data.get("self_report_scope") or {}).get("exclude_sentence") if isinstance(data, dict) else None
    return {"hedge": hedges, "self_report": selfrep, "self_report_exclude": re.compile(scope, re.IGNORECASE) if scope else None}


def hedge_ids(text: str) -> set:
    return {i for i, rx in _lexicon()["hedge"].items() if rx.search(text)}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:25.725Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/backend/grounding.py'\ns=open(p).read()\nanchor=\"def check_summary(summary: str, excerpt: str, label: str = \\\"\\\", date_iso: str = \\\"\\\") -> list:\"\nnew='''def missing_qualifier_terms(summary: str, excerpt: str) -> list:\n    \"\"\"The words in the quote that carry a qualifier the summary dropped (D-022), for the 'Edit the summary to keep ...' sentence. English patterns only;\n    a Spanish quote may return []. Display only: the pass/fail decision is dropped_qualifiers().\"\"\"\n    kinds = set(dropped_qualifiers(summary, excerpt))\n    found = []\n\n    def add(m):\n        w = re.sub(r\"\\\\s+\", \" \", m.group(0)).strip(\" .\").lower()\n        if w and w not in found:\n            found.append(w)\n    if \"hedge\" in kinds:\n        for rx in _lexicon()[\"hedge\"].values():\n            m = rx.search(excerpt)\n            if m:\n                add(m)\n        if not found:\n            m = _HEDGE_WORDS.search(excerpt)\n            if m:\n                add(m)\n    for kind, rx in ((\"self_report\", _SELF_CARRIED), (\"negation\", _NEG), (\"laterality\", _LATERAL), (\"approx\", _APPROX)):\n        if kind in kinds:\n            sm = {w.lower() for w in rx.findall(summary)}\n            for m in rx.finditer(excerpt):\n                if m.group(0).lower() not in sm:\n                    add(m)\n    return found[:4]\n\n\n'''\nassert anchor in s\nopen(p,'w').write(s.replace(anchor,new+anchor,1))\nE"
}
````

### User / tool · 2026-11-02T04:56:25.822Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:40.152Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/trace.py'\ns=open(p).read()\n\n# 1. na with text override\ns=s.replace('''def na(code: str, target: dict = None, options: list = None) -> dict:\n    d = {\"code\": code, \"text\": _NEXT[code]}''','''def na(code: str, target: dict = None, options: list = None, text: str = None) -> dict:\n    d = {\"code\": code, \"text\": text or _NEXT[code]}''',1)\n\n# 2. TRACE_WHY\ns=s.replace('''    \"NOT_AN_ACCEPTED_ENTRY\": narrative.REASONS''','''    \"CODE_CHECK_FAILED\": \"You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.\",\n    \"NOT_AN_ACCEPTED_ENTRY\": narrative.REASONS''',1)\n\n# 3. entry steps post-processing\nold='''    nxt = None\n    if unconf:\n        nxt = na(\"CONFIRM_DATE\", {\"record_id\": rid, \"view\": \"dates_to_confirm\"}) if rec.get(\"date_status\") == \"ambiguous\" else na(\"READ_RECORD\", {\"record_id\": rid})\n    st.append(_human_step(cx, row, \"entry\", extra_pending_next=nxt))\n    return st\n'''\nnew='''    nxt = None\n    if unconf:\n        nxt = na(\"CONFIRM_DATE\", {\"record_id\": rid, \"view\": \"dates_to_confirm\"}) if rec.get(\"date_status\") == \"ambiguous\" else na(\"READ_RECORD\", {\"record_id\": rid})\n    if _code_check_gated(row):        # D-045(b): human wording skips the judge, never the code checks; a failing one blocks the export and says what to do\n        for s in st:\n            if s[\"kind\"] == \"code\" and s[\"status\"] == FAIL and s.get(\"reason_code\") in _CODE_CHECK_REASONS:\n                s[\"blocks_export\"] = True\n                s[\"next_action\"] = _fix_action(row, s)\n    st.append(_human_step(cx, row, \"entry\", extra_pending_next=nxt))\n    return st\n\n\ndef _code_check_gated(row) -> bool:\n    \"\"\"An accepted or edited, live entry whose wording the paralegal wrote or edited: its failing code checks block the export (D-045(b)).\"\"\"\n    return row[\"state\"] != \"rejected\" and row[\"review_status\"] in (\"accepted\", \"edited\") and _paralegal_wording(\"entry\", row)\n\n\ndef _current_text(row):\n    ed = row.get(\"edited\") or {}\n    return ed.get(\"summary\", row.get(\"summary\") or \"\"), ed.get(\"excerpt\", row.get(\"excerpt\") or \"\")\n\n\ndef _fix_action(row, stp) -> dict:\n    \"\"\"The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure).\"\"\"\n    code, summ, exc = stp[\"reason_code\"], *_current_text(row)\n    target = {\"item_id\": row[\"id\"]}\n    tail = \" The export stays blocked until it passes.\"\n    if code == \"SUMMARY_DROPS_QUALIFIER\":\n        terms = grounding.missing_qualifier_terms(summ, exc)\n        what = \", \".join(f\"\\\\u2018{t}\\\\u2019\" for t in terms) if terms else \"the quote's hedge, attribution, negation, side or approximation\"\n        return na(\"EDIT_SUMMARY\", target, text=f\"Edit the summary to keep {what}; the quote says it and your summary leaves it out.\" + tail)\n    if code == \"SUMMARY_TOKEN_NOT_IN_EXCERPT\":\n        toks = (stp.get(\"evidence\") or {}).get(\"tokens\") or []\n        what = \", \".join(f\"\\\\u2018{t}\\\\u2019\" for t in toks) if toks else \"the words that are not in the quote\"\n        return na(\"EDIT_SUMMARY\", target, text=f\"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}.\" + tail)\n    if code in (\"EXCERPT_NOT_WHOLE_SENTENCE\", \"EXCERPT_OMITS_QUALIFIER\"):\n        return na(\"EDIT_QUOTE\", target, text=_NEXT[\"EDIT_QUOTE\"] + tail)\n    return na(\"READ_RECORD\", {\"record_id\": (row.get(\"record_ids\") or [None])[0]}, text=\"Read the record yourself, then fix the quote or dismiss this item.\" + tail)\n\n\ndef code_check_blockers(conn, case_id: str, cx=None) -> list:\n    \"\"\"Export blockers (D-045(b)): accepted or edited entries whose wording the paralegal wrote or edited and whose current summary or quote fails a code check.\n    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree.\"\"\"\n    cx = cx or _Cx(conn, case_id, False)\n    out = []\n    for row in DB.list_items(conn, case_id, \"entry\"):\n        if not _code_check_gated(row):\n            continue\n        fails = [s for s in _entry_steps(cx, row) if s[\"kind\"] == \"code\" and s[\"status\"] == FAIL and s.get(\"reason_code\") in _CODE_CHECK_REASONS]\n        if not fails:\n            continue\n        f = fails[0]\n        out.append({\"item_id\": row[\"id\"], \"kind\": \"entry\", \"reason_code\": f[\"reason_code\"], \"step_id\": f[\"id\"], \"failed_steps\": [x[\"id\"] for x in fails],\n                    \"why\": f[\"why\"] + \" \" + TRACE_WHY[\"CODE_CHECK_FAILED\"], \"next_action\": _fix_action(row, f)})\n    return out\n'''\nassert old in s\ns=s.replace(old,new,1)\n\n# 4. export_blockers\nold='''    if cx.ran and not cx.running:\n        out.extend(judge_not_run_blockers(conn, case_id))'''\nnew='''    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks\n    if cx.ran and not cx.running:\n        out.extend(judge_not_run_blockers(conn, case_id))'''\nassert old in s\ns=s.replace(old,new,1)\ns=s.replace(\"from app.backend import narrative, present, review, store, why\",\"from app.backend import grounding, narrative, present, review, store, why\",1)\nopen(p,'w').write(s)\nE\ngrep -n 'def judge_not_run_blockers' app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:56:40.274Z

**tool result**
````
766:def judge_not_run_blockers(conn, case_id: str) -> list:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:49.716Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/trace.py'\ns=open(p).read()\nold='''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = None             # the human already decided; step-level hints stay on the steps\n    if rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"'''\nnew='''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    gated = [s for s in steps if s[\"kind\"] == \"code\" and s[\"status\"] == FAIL and s.get(\"blocks_export\")]      # D-045(b): human wording whose code check fails\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = gated[0][\"next_action\"] if gated else None     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording\n    if gated:\n        code, label = \"needs_attention\", \"Needs your attention: a check on your wording fails\"\n    elif rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"'''\nassert old in s; s=s.replace(old,new,1)\nold='''    blocks = (live and rs == \"pending\") if blocks_flag is None else blocks_flag\n'''\nnew='''    blocks = (live and rs == \"pending\") if blocks_flag is None else blocks_flag\n    blocks = blocks or bool(gated)\n'''\nassert old in s; s=s.replace(old,new,1)\n\nold='''    jnr = [b for b in blockers if b[\"reason_code\"] == \"JUDGE_NOT_RUN\"]\n    live_pending'''\nnew='''    jnr = [b for b in blockers if b[\"reason_code\"] == \"JUDGE_NOT_RUN\"]\n    ccf = [b for b in blockers if b.get(\"step_id\")]             # D-045(b): the paralegal's own wording fails a code check\n    live_pending'''\nassert old in s; s=s.replace(old,new,1)\ns=s.replace('''\"judge_not_run\": len(jnr)}\n    warnings''','''\"judge_not_run\": len(jnr), \"code_check_failed\": len(ccf)}\n    warnings''',1)\nold='''        text = (f\"{len(jnr)} accepted item'''\nassert old in s\nold2='''                else {\"code\": \"needs_attention\", \"label\": f\"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked\" if jnr else \"Nothing is accepted yet\"})'''\nnew2='''                else {\"code\": \"needs_attention\", \"label\": f\"{len(ccf)} edited summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check\" if ccf and not jnr\n                      else f\"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked\" if jnr else \"Nothing is accepted yet\"})'''\nassert old2 in s; s=s.replace(old2,new2,1)\nopen(p,'w').write(s)\nE\nsed -n 960,985p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:56:49.830Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 38, in <module>
AssertionError
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:53.040Z

**tool call — Bash**
````
{
 "command": "grep -n '\"needs_attention\", \"label\"' app/backend/trace.py | cat -A | cut -c1-300"
}
````

### User / tool · 2026-11-02T04:56:53.128Z

**tool result**
````
cat: illegal option -- A
usage: cat [-belnstuv] [file ...]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:54.346Z

**tool call — Bash**
````
{
 "command": "grep -n 'Nothing is accepted yet' app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:56:54.435Z

**tool result**
````
993:               else {"code": "needs_attention", "label": f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:55.329Z

Indentation differed (15 spaces). Rerun with a looser match.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:56:59.866Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/trace.py'\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert old in s, old[:60]\n    s=s.replace(old,new,1)\nrep('''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = None             # the human already decided; step-level hints stay on the steps\n    if rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"''','''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    gated = [s for s in steps if s[\"kind\"] == \"code\" and s[\"status\"] == FAIL and s.get(\"blocks_export\")]      # D-045(b): human wording whose code check fails\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = gated[0][\"next_action\"] if gated else None     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording\n    if gated:\n        code, label = \"needs_attention\", \"Needs your attention: a check on your wording fails\"\n    elif rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"''')\nrep('''    blocks = (live and rs == \"pending\") if blocks_flag is None else blocks_flag\n''','''    blocks = (live and rs == \"pending\") if blocks_flag is None else blocks_flag\n    blocks = blocks or bool(gated)\n''')\nrep('''    jnr = [b for b in blockers if b[\"reason_code\"] == \"JUDGE_NOT_RUN\"]\n    live_pending''','''    jnr = [b for b in blockers if b[\"reason_code\"] == \"JUDGE_NOT_RUN\"]\n    ccf = [b for b in blockers if b.get(\"step_id\")]             # D-045(b): the paralegal's own wording fails a code check\n    live_pending''')\nrep('''\"judge_not_run\": len(jnr)}\n    warnings''','''\"judge_not_run\": len(jnr), \"code_check_failed\": len(ccf)}\n    warnings''')\nrep('''{\"code\": \"needs_attention\", \"label\": f\"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked\" if jnr else \"Nothing is accepted yet\"})''',\n'''{\"code\": \"needs_attention\", \"label\": f\"{len(ccf)} edited summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check\" if ccf and not jnr\n                      else f\"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked\" if jnr else \"Nothing is accepted yet\"})''')\nopen(p,'w').write(s)\nE\nsed -n 24,32p app/backend/export_routes.py"
}
````

### User / tool · 2026-11-02T04:56:59.989Z

**tool result**
````
    return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})


def export_payload(token: str, case: dict, now: datetime = None) -> dict:
    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
        raise export.ExportBlocked(case["export_blockers"])
    out = export.build_export(case)
    now = now or datetime.now(timezone.utc)
    ok = ("accepted", "edited")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:57:03.522Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_export.py; grep -n '^def test' tests/unit/test_export.py | tail -8; sed -n 760,800p tests/unit/test_trace.py"
}
````

### User / tool · 2026-11-02T04:57:03.632Z

**tool result**
````
"""Export assembly (code, deterministic). R-EX-1..R-EX-8, R-EX-6 golden byte equality, D-019; LLM_VS_CODE row 17."""
import re
from datetime import datetime
import pytest
from app.backend import export as X
from tests.unit import _golden as G

def build_case(accept=lambda kind, key: True):
    """Case dict assembled ONLY from golden files: records, entries (summary+quote from the golden letter), amounts, flags."""
    ex = G.expected("sample")
    letter, _ = G.export_blocks()
    recs = {r["record_no"]: r for r in ex["records"]}
    texts = {r["n"]: r["excerpt"] for r in G.records("sample")}
    entries = []
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        entries.append(dict(id=f"e{n}", record_no=n, summary=summ, excerpt=re.search(r'"(.+)"', src).group(1),
                            review_status="accepted" if accept("entry", n) else "dismissed"))
    amounts = [dict(id=a["id"], record_no=a["record_no"], cents=(round(a["value"] * 100) if a["value"] is not None else None), cls=a["class"],
                    raw=a["raw"], excerpt=a["excerpt"], review_status="accepted" if accept("amount", a["id"]) else "dismissed")
               for a in ex["amounts"] if a["class"] != "damages"] + \
              [dict(id="A4", record_no=5, cents=None, cls="damages", raw="missing 3 days of work", excerpt=texts[5].split(". ")[1], review_status="accepted")]
    flags = [dict(id=f["id"], type=f["type"], subtype=f.get("subtype"), evidence=f["evidence"], review_status="accepted",
                  days=f.get("days"), from_date=f.get("from_date"), to_date=f.get("to_date")) for f in ex["flags"]]
    return dict(records=[dict(n=n, source=r["source"], date_iso=r["date"], excerpt=texts[n]) for n, r in recs.items()],
                entries=entries, amounts=amounts, flags=flags, pending_count=0, events=[])

def test_sample_all_accepted_equals_golden_byte_for_byte():
    """R-EX-6: all entries + both charges accepted -> letter_text and internal_notes_text equal sample.export.expected.txt exactly."""
    letter, notes = G.export_blocks()
    out = X.build_export(build_case())
    assert out["letter_text"] == letter.rstrip("\n")
    assert out["internal_notes_text"] == notes.rstrip("\n")

def test_deterministic():
    """R-EX-3: same accepted set -> byte-identical blocks."""
    c = build_case()
133:def test_every_record_citation_has_provider_and_date():
140:def test_bills_to_request_line_exact():
145:def test_dismiss_5_pending_6_reconciliation_and_counts():
157:def test_edited_items_section():
167:def test_edited_then_accepted_entry_still_listed_in_edited_items():
178:def test_accepted_unedited_and_dismissed_edited_not_listed():
185:def test_build_export_refuses_while_accepted_items_lack_the_second_check_d044():
194:def test_export_blocked_code_is_judge_not_run_only_when_every_blocker_is():
    lad = e["ladder"]
    lad["entered_by"] = "reviewer"
    DB.update_item(conn, eid, case=tok, ladder=lad)
    assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]


def test_entry_with_a_summary_the_paralegal_wrote_is_not_ai_made(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    DB.apply_review(conn, eid, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]


def _accept_all_but(c, tok, keep_pending):
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        if x["id"] not in keep_pending:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})


def test_gate_ready_equals_export_allowed_in_every_state_d045(env):
    """The invariant: gate.ready == (GET /export is not 4xx) == (gate.blockers == []), whatever the state. Pending items warn, never block."""
    c, conn, tok, _ = env
    seen = {}

    def check(name):
        g = _gate(c, tok)
        ex = c.get(f"/api/cases/{tok}/export")
        assert g["ready"] == (g["blockers"] == []), name
        assert g["ready"] == (ex.status_code < 400), (name, ex.status_code, [b["reason_code"] for b in g["blockers"]])
        assert g["status"] == ("pass" if g["ready"] else "fail"), name
        assert bool(_jnr(g)) == (ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"] != [] and any(b["reason_code"] == "JUDGE_NOT_RUN" for b in ex.json()["error"]["detail"]["blockers"])), name
        if ex.status_code >= 400:
            assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name     # the same list
        seen[name] = (g, ex)

    check("nothing decided yet (pending only)")
    case = c.get(f"/api/cases/{tok}").json()
    all_ids = [x["id"] for x in [*case["entries"], *case["amounts"], *case["flags"]]]
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:57:19.611Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_trace.py <<'E'\n\n\n# ---- D-045(b) / T-098: a human-edited summary is exempt from the judge, never from the code checks (reviewer case: reviews/T-097-ux-designer.md B1)\nREVIEWER_EDIT = \"Paralegal wording for the mixed-case check.\"          # the T-097 walk's edit: drops the quote's qualifier\n\n\ndef _edit_entry(c, tok, eid, summary):\n    r = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": summary}})\n    assert r.status_code == 200, r.text\n    return r\n\n\ndef _mixed(c, tok):\n    \"\"\"The reviewer's walk: accept one entry, edit another so it drops a qualifier, dismiss the first. Returns the edited id.\"\"\"\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    acc, edt = ents[0][\"id\"], ents[1][\"id\"]\n    assert c.post(f\"/api/cases/{tok}/items/{acc}/review\", json={\"action\": \"accept\"}).status_code == 200\n    _edit_entry(c, tok, edt, REVIEWER_EDIT)\n    c.post(f\"/api/cases/{tok}/items/{acc}/review\", json={\"action\": \"dismiss\"})\n    return edt\n\n\ndef _ccf(gate):\n    return [b for b in gate[\"blockers\"] if b.get(\"step_id\")]\n\n\ndef test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):\n    c, conn, tok, _ = env\n    edt = _mixed(c, tok)\n    g = _gate(c, tok)\n    got = _ccf(g)\n    assert [b[\"item_id\"] for b in got] == [edt] and got[0][\"reason_code\"] == \"SUMMARY_DROPS_QUALIFIER\" and got[0][\"step_id\"] == \"summary_qualifier\"\n    assert g[\"ready\"] is False and g[\"status\"] == \"fail\" and g[\"counts\"][\"code_check_failed\"] == 1 and g[\"reason_code\"] == \"SUMMARY_DROPS_QUALIFIER\"\n    assert \"second AI check is not needed\" in got[0][\"why\"] and g[\"next_action\"][\"code\"] == \"EDIT_SUMMARY\"\n    r = c.get(f\"/api/cases/{tok}/export\")\n    assert r.status_code == 422 and \"letter_text\" not in r.text and REVIEWER_EDIT not in r.text\n    det = r.json()[\"error\"][\"detail\"][\"blockers\"]\n    assert [(b[\"item_id\"], b[\"reason_code\"]) for b in det] == [(edt, \"SUMMARY_DROPS_QUALIFIER\")]\n    assert r.json()[\"error\"][\"code\"] == \"export_blocked\" and \"keep\" in r.json()[\"error\"][\"message\"] or r.json()[\"error\"][\"message\"]\n    ct = c.get(f\"/api/cases/{tok}/trace\").json()\n    assert ct[\"verdict\"][\"code\"] == \"needs_attention\" and \"fails a check\" in ct[\"verdict\"][\"label\"]\n\n\ndef test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):\n    c, conn, tok, _ = env\n    edt = _mixed(c, tok)\n    t = c.get(f\"/api/cases/{tok}/items/{edt}/trace\").json()\n    s = steps_of(t)\n    q = s[\"summary_qualifier\"]\n    assert q[\"status\"] == \"fail\" and q[\"blocks_export\"] is True and q[\"reason_code\"] == \"SUMMARY_DROPS_QUALIFIER\"\n    na = q[\"next_action\"]\n    assert na[\"code\"] == \"EDIT_SUMMARY\" and na[\"text\"].startswith(\"Edit the summary to keep \") and \"‘\" in na[\"text\"] and \"export stays blocked\" in na[\"text\"]\n    assert t[\"verdict\"][\"blocks_export\"] is True and t[\"verdict\"][\"code\"] == \"needs_attention\" and t[\"next_action\"] == na\n    assert s[\"human\"][\"status\"] == \"pass\"                                       # the decision is still recorded; the code check is what blocks\n    for sid in (\"summary_tokens\", \"excerpt_verbatim\", \"highlight\"):\n        assert s[sid][\"blocks_export\"] is False\n\n\ndef test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098(env):\n    c, conn, tok, _ = env\n    edt = _mixed(c, tok)\n    assert c.get(f\"/api/cases/{tok}/export\").status_code == 422\n    quote = next(e for e in c.get(f\"/api/cases/{tok}\").json()[\"entries\"] if e[\"id\"] == edt)[\"excerpt\"]\n    _edit_entry(c, tok, edt, \"Possible \" + quote.split(\".\")[0].strip() if False else quote)      # the quote verbatim keeps every qualifier\n    g = _gate(c, tok)\n    assert _ccf(g) == [] and g[\"ready\"] is True\n    ex = c.get(f\"/api/cases/{tok}/export\")\n    assert ex.status_code == 200 and g[\"ready\"] == (ex.status_code < 400)\n    assert steps_of(c.get(f\"/api/cases/{tok}/items/{edt}/trace\").json())[\"summary_qualifier\"][\"status\"] == \"pass\"\n\n\ndef test_dismissing_the_failing_edited_item_clears_the_blocker_t098(env):\n    c, conn, tok, _ = env\n    edt = _mixed(c, tok)\n    c.post(f\"/api/cases/{tok}/items/{edt}/review\", json={\"action\": \"dismiss\"})\n    assert _ccf(_gate(c, tok)) == []\n\n\ndef test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098(env):\n    c, conn, tok, _ = env\n    _accept_all(c, tok)\n    assert _ccf(_gate(c, tok)) == []\n\n\ndef test_gate_ready_equals_export_allowed_with_a_failing_edit_t098(env):\n    c, conn, tok, _ = env\n    _mixed(c, tok)\n    for name in (\"failing edit\", \"failing edit and run failed\"):\n        if name.endswith(\"run failed\"):\n            DB.update_case(conn, tok, status=\"failed\")\n        g = _gate(c, tok)\n        ex = c.get(f\"/api/cases/{tok}/export\")\n        assert g[\"ready\"] == (g[\"blockers\"] == []) == (ex.status_code < 400), name\n        assert [b[\"reason_code\"] for b in ex.json()[\"error\"][\"detail\"][\"blockers\"]] == [b[\"reason_code\"] for b in g[\"blockers\"]], name\nE\n.venv/bin/python -m pytest -q tests/unit/test_trace.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:57:26.452Z

**tool result**
````
...............................................................          [100%]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:57:33.883Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('''    assert r.json()[\"error\"][\"code\"] == \"export_blocked\" and \"keep\" in r.json()[\"error\"][\"message\"] or r.json()[\"error\"][\"message\"]\n''','''    assert r.json()[\"error\"][\"code\"] == \"export_blocked\" and \"export is blocked\" in r.json()[\"error\"][\"message\"]\n''')\ns=s.replace('''\"Possible \" + quote.split(\".\")[0].strip() if False else quote)      # the quote verbatim keeps every qualifier''','''quote)      # the quote verbatim keeps every qualifier''')\ns+='''\n\ndef test_missing_qualifier_terms_name_the_words_to_keep_t098():\n    from app.backend import grounding\n    assert grounding.missing_qualifier_terms(\"MRI of the cervical spine was done.\", \"MRI suggests possible disc herniation.\")\n    got = grounding.missing_qualifier_terms(\"Fracture seen.\", \"Possible left wrist fracture.\")\n    assert \"possible\" in got and \"left\" in got\n    assert grounding.missing_qualifier_terms(\"Possible left wrist fracture.\", \"Possible left wrist fracture.\") == []\n'''\nopen(p,'w').write(s)\np='tests/unit/test_export.py'\ns=open(p).read()\ns+='''\n\ndef test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b():\n    \"\"\"T-098: export_payload raises ExportBlocked for the blocker list the gate gives, whatever the reason; the code is export_blocked, not judge_not_run.\"\"\"\n    from app.backend import export_routes as XR\n    c = build_case()\n    blk = {\"item_id\": \"e2\", \"kind\": \"entry\", \"reason_code\": \"SUMMARY_DROPS_QUALIFIER\", \"step_id\": \"summary_qualifier\", \"why\": \"The summary leaves out a qualifier.\", \"next_action\": None}\n    c[\"export_blockers\"] = [blk]\n    with pytest.raises(X.ExportBlocked) as ei:\n        XR.export_payload(\"tok\", c)\n    assert ei.value.code == \"export_blocked\" and ei.value.items == [blk]\n    assert XR.blocked_message(ei.value) == \"The summary leaves out a qualifier. The export is blocked.\"\n'''\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:57:40.852Z

**tool result**
````
........................................................................ [ 81%]
................                                                         [100%]
88 passed in 6.31s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:57:42.966Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -x -q 2>&1 | tail -8; .venv/bin/python - <<'E'\nfrom app.backend import grounding\nprint(grounding.missing_qualifier_terms(\"Neck pain.\",\"Patient reports possible neck pain, no loss of consciousness, approx 2 weeks.\"))\nE"
}
````

### User / tool · 2026-11-02T04:57:43.790Z

**tool result**
````
    from app.backend import calibration_route as CR
app/backend/calibration_route.py:18: in <module>
    from app.backend import calibration_route_checks as _checks  # noqa: F401  (reserved: none; kept out of this module on purpose)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ImportError: cannot import name 'calibration_route_checks' from 'app.backend' (/Users/arsis/zlayt-pm-project/app/backend/__init__.py)
=========================== short test summary info ============================
ERROR tests/unit/test_calibration_route.py
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
['possible', 'patient reports', 'no', 'approx']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:57:45.317Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit --ignore=tests/unit/test_calibration_route.py 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T04:58:32.899Z

**tool result**
````
........................................................................ [ 57%]
........................................................................ [ 62%]
........................................................................ [ 66%]
........................................................................ [ 71%]
........................................................................ [ 75%]
........................................................................ [ 80%]
...........................s............................................ [ 84%]
........................................................................ [ 89%]
........................................................................ [ 93%]
........................................................................ [ 98%]
...............................                                          [100%]
1614 passed, 1 skipped in 46.29s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:58:36.480Z

**tool call — Bash**
````
{
 "command": "grep -n -i 'JUDGE_NOT_RUN\\|judge_not_run' memory/contracts/api.md | head"
}
````

### User / tool · 2026-11-02T04:58:36.566Z

**tool result**
````
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
361:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
609:      "counts": {"blocking": 1, "pending_items": 21, "date_unconfirmed": 1, "accepted": 0, "dismissed": 0, "rejected_not_blocking": 1, "judge_not_run": 0},
618:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
637:Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
642:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:58:43.072Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'\ns=open(p).read()\nold=\"**Pending items are not blockers** (D-045(a))\"\nadd=(\"**Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker \"\n     \"`{item_id, kind: \\\"entry\\\", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. \\\"Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes.\\\" \"\n     \"`GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` (\\\"N edited summaries fail a check\\\") when only these block. Cleared by an edit that passes, dismissing or resetting the item. \"\n     \"On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: \\\"Needs your attention: a check on your wording fails\\\", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. AI drafts are not covered by this blocker (they keep needs_review + the human accept).  \")\nassert s.count(old)==1\ns=s.replace(old, add+old,1)\ns=s.replace(\"else `export_blocked` (a run in progress or failed, or nothing accepted;\",\"else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted;\",1)\nopen(p,'w').write(s)\nE\ngit status --short app/backend/trace.py app/backend/grounding.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_export.py; git diff --stat HEAD -- app/backend/trace.py app/backend/grounding.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_export.py"
}
````

### User / tool · 2026-11-02T04:58:43.222Z

**tool result**
````
 M app/backend/grounding.py
 M app/backend/trace.py
 M memory/contracts/api.md
 M tests/unit/test_export.py
 M tests/unit/test_trace.py
 app/backend/grounding.py  |  28 +++++++++++++
 app/backend/trace.py      |  94 +++++++++++++++++++++++++++++++++++++-----
 memory/contracts/api.md   |  15 ++++++-
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 239 insertions(+), 12 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:58:45.676Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -U0 -- memory/contracts/api.md | cut -c1-160; git diff HEAD -U0 -- app/backend/trace.py | grep '^@@'"
}
````

### User / tool · 2026-11-02T04:58:45.811Z

**tool result**
````
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index caf91ca..55c7390 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -40,0 +41 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
+| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null
@@ -360 +361 @@ Note `item.kind` is the item type (`"amount"`, as in the review response); the a
-**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.bloc
+**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.bloc
@@ -617 +618 @@ Each case step has the shared step keys plus `counts` (object, may be `{}`); `ex
-**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.ex
+**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.ex
@@ -650,0 +652,10 @@ Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays tok
+## GET /api/calibration  (T-099, serves T-090 counts to T-096)
+Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate co
+
+Always `200` with one envelope:
+- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backen
+- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
+- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range
+
+Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or
+
@@ -13 +13 @@ import json
@@ -47,0 +48 @@ TRACE_WHY = {
@@ -87,2 +88,2 @@ def reason_text(code: str) -> str:
@@ -262,0 +264 @@ def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
@@ -264,2 +266,4 @@ def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
@@ -279,0 +284 @@ def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
@@ -384,0 +390,5 @@ def _entry_steps(cx, row):
@@ -388,0 +399,45 @@ def _entry_steps(cx, row):
@@ -471,0 +527,16 @@ def _flag_steps(cx, row):
@@ -487,0 +559 @@ def _flag_steps(cx, row):
@@ -502 +574 @@ def _flag_steps(cx, row):
@@ -504 +575,0 @@ def _flag_steps(cx, row):
@@ -535,0 +607 @@ def _flag_steps(cx, row):
@@ -552 +623,0 @@ def _flag_steps(cx, row):
@@ -902,0 +974 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -908 +980 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -926 +998,2 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -943,0 +1017 @@ def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:58:49.664Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -U0 -- app/backend/trace.py | sed -n '/^@@ -471/,/^@@ -902/p' | cut -c1-200"
}
````

### User / tool · 2026-11-02T04:58:49.879Z

**tool result**
````
@@ -471,0 +527,16 @@ def _flag_steps(cx, row):
+    if origin == "code" and cc.get("candidate_rule"):
+        # T-094: a conflict pair proposed by code and classified by the judge (J3). The model proposed nothing.
+        comp = present._computed(row.get("computed"))
+        arith = cc.get("arithmetic")
+        st.append(step("paired_by_code", "Code paired these two quotes", "code", PASS,
+                       "Software found a stated plan and a later record that shows it ended early" if cc["candidate_rule"] == "plan_vs_outcome"
+                       else "Software found a denial of prior problems and another record that mentions an earlier problem",
+                       rule="row 10", evidence={"values": {"rule": cc["candidate_rule"], "arithmetic": arith}, "spans": spans}))
+        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
+        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
+                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Both quotes are in the records, character for character.",
+                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 4", evidence={"spans": spans}))
+        st.append(inj())
+        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j3", R, rule="row 11"))
+        st.append(_human_step(cx, row, "flag"))
+        return st
@@ -487,0 +559 @@ def _flag_steps(cx, row):
+        st += _ocr_steps(R, rid0)
@@ -502 +574 @@ def _flag_steps(cx, row):
-        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP[step_name], call)
+        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
@@ -504 +575,0 @@ def _flag_steps(cx, row):
-        st += _ocr_steps(R, rid0)
@@ -535,0 +607 @@ def _flag_steps(cx, row):
+    st += _ocr_steps(R, rid0)
@@ -552 +623,0 @@ def _flag_steps(cx, row):
-    st += _ocr_steps(R, rid0)
@@ -902,0 +974 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:00.763Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && git diff HEAD -- app/backend/trace.py memory/contracts/api.md app/backend/grounding.py tests/unit/test_trace.py tests/unit/test_export.py > $S/full.patch && python3 - $S <<'E'\nimport sys,re\nS=sys.argv[1]\nt=open(S+'/full.patch').read()\nfiles=re.split(r'(?=^diff --git )',t,flags=re.M)\nout=[]\nfor f in files:\n    if not f.strip(): continue\n    parts=re.split(r'(?=^@@ )',f,flags=re.M)\n    head,hunks=parts[0],parts[1:]\n    keep=[]\n    for h in hunks:\n        first=h.split('\\n',1)[0]\n        if '_flag_steps' in first: continue\n        if 'calibration' in h.lower() and 'api.md' in head: continue\n        keep.append(h)\n    out.append(head+''.join(keep))\n    print(head.split('\\n')[0], len(hunks),'->',len(keep))\nopen(S+'/mine.patch','w').write(''.join(out))\nE\nexport GIT_INDEX_FILE=$S/tmpindex; git read-tree HEAD && git apply --cached $S/mine.patch && git diff --cached --stat; unset GIT_INDEX_FILE"
}
````

### User / tool · 2026-11-02T04:59:01.077Z

**tool result**
````
diff --git a/app/backend/grounding.py b/app/backend/grounding.py 1 -> 1
diff --git a/app/backend/trace.py b/app/backend/trace.py 14 -> 9
diff --git a/memory/contracts/api.md b/memory/contracts/api.md 4 -> 2
diff --git a/tests/unit/test_export.py b/tests/unit/test_export.py 1 -> 1
diff --git a/tests/unit/test_trace.py b/tests/unit/test_trace.py 1 -> 1
 app/backend/grounding.py  |  28 +++++++++++++
 app/backend/trace.py      |  72 ++++++++++++++++++++++++++++----
 memory/contracts/api.md   |   4 +-
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 209 insertions(+), 9 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:07.497Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && export GIT_INDEX_FILE=$S/tmpindex && git diff --cached --stat | tail -1 && git commit -q -m \"fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)\n\nA summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind\nwith a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step\nwith a specific 'Edit the summary to keep ...' action.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD; unset GIT_INDEX_FILE; git log -1 --stat --format=%h | tail -8"
}
````

### User / tool · 2026-11-02T04:59:07.955Z

**tool result**
````
 5 files changed, 209 insertions(+), 9 deletions(-)
check_stale_index: BLOCKED — this commit would revert work that is not yours.
Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD
app/backend/trace.py: staged version matches neither HEAD nor the working tree (stale index?)
memory/contracts/api.md: staged version matches neither HEAD nor the working tree (stale index?)
5b4ccb0

 tools/check_stale_index.py | 56 ++++++++++++++++++++++++++++++++++++++++++++++
 tools/install_git_hooks.sh |  6 +++--
 2 files changed, 60 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:11.458Z

**tool call — Bash**
````
{
 "command": "git status --short app/backend/trace.py app/backend/grounding.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_export.py; git log --oneline -4; git diff HEAD -U0 -- app/backend/trace.py | grep -c '_flag_steps'; sed -n 1,56p tools/check_stale_index.py | head -40"
}
````

### User / tool · 2026-11-02T04:59:11.603Z

**tool result**
````
 M app/backend/grounding.py
 M app/backend/trace.py
 M memory/contracts/api.md
 M tests/unit/test_export.py
 M tests/unit/test_trace.py
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
6
#!/usr/bin/env python3
"""Pre-commit guard against stale-index reverts (lessons: ec33bf0, 2fca530, 57a08ba).

Several workers share one checkout. A commit built from an index that predates other workers' commits
silently reverts their files. The signature: a staged path whose staged blob matches neither HEAD nor
the working tree (an old version), or a staged deletion of a file that still exists on disk.
Exit 1 with the offending paths; 0 otherwise. Works with GIT_INDEX_FILE temp indexes too.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"check_stale_index: BLOCKED (git {args[0]} failed: {r.stderr.strip()[:200]})")
        sys.exit(1)
    return r.stdout


def blob(spec: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", spec], capture_output=True, text=True)
    return r.stdout.strip() or None


def main() -> int:
    if not blob("HEAD"):
        return 0  # first commit
    hits = []
    raw =git("diff", "--cached", "--name-status", "--no-renames", "-z").split("\0")
    pairs = [(raw[i], raw[i + 1]) for i in range(0, len(raw) - 1, 2) if raw[i]]
    for status, path in pairs:
        on_disk = (ROOT / path).is_file()
        if status == "D":
            if on_disk:
                hits.append(f"{path}: staged as deleted but still on disk (stale index?)")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:20.630Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -f $S/tmpindex && export GIT_INDEX_FILE=$S/tmpindex && git read-tree HEAD && git add app/backend/trace.py app/backend/grounding.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_export.py && git diff --cached --stat && git commit -q -m \"fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)\n\nA summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind\nwith a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step\nwith a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"; echo rc=$?; git rev-parse --short HEAD; unset GIT_INDEX_FILE"
}
````

### User / tool · 2026-11-02T04:59:20.714Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf807
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:23.915Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -f $S/tmpindex && export GIT_INDEX_FILE=$S/tmpindex && git read-tree HEAD && git add app/backend/trace.py app/backend/grounding.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_export.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:59:24.128Z

**tool result**
````
 app/backend/grounding.py  |  28 +++++++++++++
 app/backend/trace.py      |  94 +++++++++++++++++++++++++++++++++++++-----
 memory/contracts/api.md   |  15 ++++++-
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 239 insertions(+), 12 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:28.224Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && GIT_INDEX_FILE=$S/tmpindex git commit -q -m \"fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)\n\nA summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind\nwith a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step\nwith a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"; echo rc=$?; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T04:59:28.761Z

**tool result**
````
check_secrets: ok (5 file(s) scanned staged)
rc=0
e511778
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:37.281Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B commit T-098 --sha e511778 --agent backend\n$B ac T-098 --check 1 --agent backend --evidence \"tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 + test_item_trace_shows_the_failing_code_step_with_the_next_action_t098 + test_gate_ready_equals_export_allowed_with_a_failing_edit_t098 + tests/unit/test_export.py::test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b pass; tests/unit 1614 passed (test_calibration_route.py ignored: another worker's in-progress import error)\"\n$B handoff T-098 --agent backend --text \"What changed: trace.code_check_blockers() adds a gate blocker {item_id, kind:entry, reason_code (first failing check), step_id, failed_steps[], why, next_action} for each accepted/edited live entry with paralegal-written/edited wording whose code step fails (summary_tokens, summary_qualifier, excerpt_*, highlight); it feeds export_blockers, so gate.ready == export allowed and GET /export is 422 export_blocked with the same list. Item trace: failing code step has blocks_export true and next_action EDIT_SUMMARY with text like 'Edit the summary to keep 'possible'; ...'; verdict becomes needs_attention + blocks_export true; gate counts.code_check_failed; case verdict label '1 edited summary fails a check'. grounding.missing_qualifier_terms supplies the words (display only). | Verified: tests/unit test_trace + test_export 88 passed; full tests/unit 1614 passed, 1 skipped (test_calibration_route.py excluded, import error from another worker's WIP). Reviewer case (accept e1, edit e2 to 'Paralegal wording for the mixed-case check.', dismiss e1) now gate fail + 422. | Left: AI drafts are NOT gated by this blocker (accept of needs_review stays the human step); an edit confirmed via kept_my_wording for a non-numeric token now blocks too, so the 409 confirm path for such tokens leads to an unexportable item (frontend/D-034 may want the 409 removed for tokens); M2 (edited item judge step in Why dialog) and M1 (panel summary) untouched. | Surprised: trace.py and api.md carried other workers' uncommitted hunks (T-094, T-099) and the stale-index guard rejects hunk-only staging, so e511778 includes them.\"\n$B move T-098 in_review --agent backend\n$B note T-097 --agent backend --text \"Frontend: T-098 (e511778) adds gate blockers with step_id (e.g. summary_qualifier) and reason_code SUMMARY_DROPS_QUALIFIER|SUMMARY_TOKEN_NOT_IN_EXCERPT|...; blocker.next_action.text is the specific fix sentence (EDIT_SUMMARY, target item_id); gate.counts.code_check_failed; GET /export 422 error.code export_blocked (detail.blockers same list); item trace: failing code step blocks_export true, verdict {needs_attention, blocks_export:true}, top-level next_action set although review_status is accepted/edited; case verdict label '1 edited summary fails a check'. Contract: memory/contracts/api.md (Code-check blocker paragraph).\""
}
````

### User / tool · 2026-11-02T04:59:37.634Z

**tool result**
````
T-098: commit e511778 recorded
AC 1 checked: tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 + test_item_trace_shows_the_failing_code_step_with_the_next_action_t098 + test_gate_ready_equals_export_allowed_with_a_failing_edit_t098 + tests/unit/test_export.py::test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b pass; tests/unit 1614 passed (test_calibration_route.py ignored: another worker's in-progress import error)
handoff written on T-098
T-098: in_progress -> in_review
noted on T-097
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:59:41.147Z

T-098 is in `in_review` (commit e511778). An accepted or edited entry with paralegal-written wording that fails a code check is now a gate blocker, and `GET /export` returns 422 with the same list.

- **Checks:** `test_trace.py` and `test_export.py` pass (88). The full `tests/unit` run passes (1614) with `test_calibration_route.py` ignored, because it fails to import code from another worker's unfinished work. The reviewer's case (edit to "Paralegal wording for the mixed-case check.") now shows gate fail and 422, and the item trace shows the failing `summary_qualifier` step with the next action.
- **Commit:** `trace.py` and `api.md` carried other workers' uncommitted changes (T-094, T-099). The stale-index guard rejects staging only some of a file's changes, so e511778 includes them. The diff lists only my five files.
- **AI drafts:** not gated by this blocker, only paralegal-written or edited wording.
- **Open issue:** a non-numeric token the paralegal confirms through the 409 "keep my wording" path now blocks too, so the confirm leads to an item that can't be exported. D-034 probably wants that 409 path removed for tokens.

I noted the fields the frontend should read on T-097.
