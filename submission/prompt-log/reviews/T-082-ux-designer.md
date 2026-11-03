# T-082 review, ux-designer-reviewer: "How the AI was checked" panel

Verdict: **changes** (0 blockers, 2 majors). Commit df5dddd, app/frontend/judges.js, stepper.css.

Exercised: own servers at HEAD on :7871 (ZLAYT_MODE=local, fixture curated) and :7872 (demo); Playwright at 1440x900 and 390x844 on lib06 (3 objections, 7 disagreements), the sample (0 objections, 1 disagreement) and case_01 (none); GET /judges compared against the DOM; clicked See the steps / Go to item; checked the mock API mode. Evidence: `artifacts/review-evidence/T-082-ux-*.png`, `T-082-ux-designer-walk*.py`. Servers stopped after.

Your questions:
- "AI quality check" vs verdict on the case: the wording is right. Heading "How the AI was checked", lead "AI quality checks. ... It is not a verdict on the case, the care or the claim, and it does not replace your review", tile "AI objected" instead of "unsupported". Pass. One nit: tile "13 supported" could be read as the claim being supported; "agreed with the draft" is safer.
- "Attorney referral" listed twice: partly confirmed. They are two different flags (f_r3_2 on record 3 and f_r4_1 on record 4) with identical title and text and no record cue, so they read as a duplicate. The real duplication is bigger: every objected item is also listed again under disagreements, and "Degenerative wording" (f_r5_1) appears three times (finding 2).
- Collapse by default: yes. Panel is 2318 px (2.6 screens) at 1440 and 3569 px (4.2 screens) at 390 on lib06, and sits last on the page (finding 1).
- Mock API mode hides the panel: confirmed (`hidden=true`), nit.
- Failed step to fix in one click: each row has `See the steps` and `Go to item`, both worked; rows do not say what to do (finding 3).

```json
{"card": "T-082", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit df5dddd app/frontend/judges.js, stepper.css; local app :7871 and demo :7872; lib06, sample, case_01; 1440x900 and 390x844",
 "exercised": [
  "Started own servers at HEAD on :7871 (local) and :7872 (demo), fixture curated",
  "GET /api/cases/{tok}/judges for sample, case_01, lib06 vs the rendered rows and tiles",
  "Playwright 1440x900 and 390x844: panel height, position, headings, row titles, tiles, buttons; screenshot per case and width",
  "Opened the item stepper from a judge row (See the steps) and Go to item",
  "Mock API mode (?api=mock) panel visibility",
  "Read judges.js and stepper.css; read D-042 and the <outside project> pattern"],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "Panel is a full-page, non-collapsible block at the bottom of the page",
   "evidence": "lib06: panel 2318 px tall at 1440 (2.6 screens), 3569 px at 390 (4.2 screens), last section of a 13480/18884 px page (T-082-ux-designer-walk1.py output; screenshot artifacts/review-evidence/T-082-ux-lib06-1440-panel.png). judges.js paint() always renders all three lists open; panel is not inside a details element ('panel in <details>? False'). Only entry point is the rail button 'See how the AI was checked' deep in the case rail.",
   "why_it_matters": "Chris wants the judge process visible from every case analysis, not buried under 13,000 px. A 4-screen scroll on a phone hides it as effectively as no panel, and it competes with the review work.",
   "fix": "Wrap the panel in details, closed by default, with a summary that carries the signal: 'How the AI was checked: 16 checked, 13 agreed, 3 questioned'. Open automatically only when objections or unavailable > 0 and then show just the objected rows; put 'Where code and the AI disagree' and 'By kind of check' in nested closed details. Add the same one-line summary near the top of the results (beside the review count).",
   "acceptance_test": "E2E on lib06 at 1440x900: judge-panel summary visible, details closed on load, height of the closed panel < 120 px; opening shows the 3 objection rows. On the sample (0 objections) the closed summary reads 'checked 19, all agreed'."},
  {"severity": "major", "title": "The same item is listed up to three times, and two different flags look like duplicates",
   "evidence": "lib06 disagreement rows: [e5], [a3 'Code checks passed, the AI objected'], [a7 same], [f_r5_1 'Code checks passed, the AI objected'], [f_r5_1 'The phrase list and the AI disagree'], [f_r3_2 'Attorney referral'], [f_r4_1 'Attorney referral']. a3, a7 and f_r5_1 also appear under 'Where the AI objected (3)' (artifacts/review-evidence/T-082-ux-lib06-1440-panel.png). Row titles come from ZL.stepper.label(id) = flag title only (stepper.js:33), so f_r3_2 and f_r4_1 render identically with the same 'Code said / The AI said'.",
   "why_it_matters": "'7 disagreements' overstates by counting rows not items (really 4 items); the paralegal reads the same objection twice and wonders if it is a bug. It also inflates the trust-calibration signal.",
   "fix": "One row per item. Merge the disagreement types into chips on that row ('AI objected', 'phrase list and AI disagree'). Remove from the disagreement list any item already shown under 'Where the AI objected' or show only the code-vs-AI line inside that row. Count items in the heading. For flags and amounts prefix the title with the record: 'Attorney referral, Record 3' (data is on the item).",
   "acceptance_test": "E2E on lib06: count of unique data-target-item across judge-rejection + judge-disagreement rows equals the row count; no two visible row titles are identical; heading count equals the number of distinct items."},
  {"severity": "minor", "title": "Objection rows say what the AI thought, not what the human should do",
   "evidence": "judge-rejection rows (artifacts/review-evidence/T-082-ux-lib06-1440-panel.png): '$450 (unclear). Disagrees. The second check reads this figure as a billed charge.' then buttons 'See the steps' / 'Go to item'; no 'What you need to do' sentence, unlike the item stepper. Verdict word 'Disagrees.' does not say with whom.",
   "why_it_matters": "D-042 asks for a HITL hand-off with each fail; this panel is where the paralegal lands first.",
   "fix": "Add the server's next-action sentence ('Compare the amount with the quote yourself. Accept it as a charge, leave it unclear, or dismiss it.') and make 'Go to item' the primary button; relabel 'Disagrees' as 'The AI reads this differently from the draft'.",
   "acceptance_test": "E2E: each judge-rejection row contains a 'What you need to do' sentence and a primary Go to item button."},
  {"severity": "minor", "title": "Model and prompt internals sit in the main view",
   "evidence": "Rows show 'SHOULD_BE_CHARGE', 'NOT_SUPPORTED_BY_QUOTE', 'model claude-haiku-5-5 . prompt judge_amount_class_v1', 'Prompt versions: judge_amount_class_v1, judge_faithfulness_v1, judge_flag_v2' (T-082-ux-lib06-1440-panel.png).",
   "why_it_matters": "Checklist item 18. The audit audience wants it, the paralegal does not; keep it one click away, as the item stepper already does under 'Technical details'.",
   "fix": "Keep 'Drafted by X, checked by Y (a different model)' visible (it is a good trust line), move prompt versions, reason codes and per-row model/prompt into a closed 'Technical details'.",
   "acceptance_test": "E2E: no reason code or prompt_version text is visible while the 'Technical details' details is closed."},
  {"severity": "nit", "title": "Mock API mode hides the panel silently; 'supported' tile wording",
   "evidence": "?api=mock: judge-panel `hidden=true` (T-082-ux-designer-walk3.py). Tile '13 supported' next to a note that it is not a verdict on the claim.",
   "why_it_matters": "Dev-only; 'supported' near a legal claim invites a misread.",
   "fix": "Show 'AI check details need the live server' in mock mode; tile label 'agreed with the draft'.",
   "acceptance_test": "Mock mode shows a visible note in place of the panel."}
 ],
 "whats_right": [
  "The lead sentence 'AI quality checks ... not a verdict on the case, the care or the claim, and it does not replace your review' is the right scope-of-AI explanation, and 'AI objected' is a safer tile label than 'unsupported'.",
  "'Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5 (a different model, so it does not grade its own work)' says in one line why the check is independent.",
  "Zero-state rows are explicit ('No objections. The second check supported every item it checked.') and every row links into the item stepper and the item."],
 "questions_for_chris": []}
```
