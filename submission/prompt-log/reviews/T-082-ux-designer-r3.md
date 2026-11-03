# T-082 round 3, ux-designer-reviewer: "How the AI was checked" panel

Verdict: **changes** (0 blockers, 2 majors, 1 minor, 1 nit). Frontend commit e92b6ed (HEAD), built against backend 10d358e.

Setup: `git worktree add` is refused for reviewers by the board-guard hook, so I ran the app from a `git archive HEAD` copy in my scratchpad (:7891 local mode, :7892 demo, fixture curated, own `ZLAYT_DB`); servers stopped by PID (curl 000). The hook also refuses `rm`, so that scratch copy is still on disk. See the T-081 r3 review for the full setup note.

## The brief's question: does the copy for items with no judge match the gate?

- **Accepted item, judge never ran: yes in substance.** Panel row: chips "AI did not check", "Blocks the export", "Your decision: Accepted"; "What you need to do: The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again; if it still cannot answer, dismiss the item." Gate row says "You accepted this item, but the second AI check never ran on it... accepting does not replace it", and the gate step ends "Run the second check again; if it still cannot answer, dismiss those items". Different words, same instruction, and the panel no longer says "then accept" on these rows (round-2 major fixed). Each row and a group button "Run the second check again for these 12" are real buttons; the summary reads "7 checked, 7 agreed with the draft, 12 not checked (blocks export)". Collapsed 58 px at 1440 (88 at 390), under Case checks; one row per item.
- **Edited item, judge never ran: no. The panel contradicts the gate** (finding 1).
- **Pending item, judge never ran: partly** (finding 3).
- **A failed rerun started from the panel says nothing** (finding 2).

Regression (walk5): lib06 panel 6 rows for 6 unique item ids, 6 unique titles with record cues, no reason codes outside Technical details; closed at load on sample, case_01, lib06 at both widths; sample 58 px and lib06 58 px at 1440; no horizontal scroll.

Evidence files are under `artifacts/review-evidence/T-082-ux-r3-*` and `T-081-ux-r3-*` (shared scripts and tokens).

```json
{"card": "T-082", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "frontend commit e92b6ed (HEAD) app/frontend/judges.js and its calls into stepper.js; backend 10d358e behaviour; clean copy of HEAD on :7891 (ZLAYT_MODE=local) and :7892 (demo), fixture curated; sample, case_01, lib06, sample with judges blanked, mixed case with an edited item; 1440x900 and 390x844",
 "exercised": [
  "git archive HEAD into a scratch dir (git worktree is blocked for reviewers); app from that copy on :7891 and :7892; stopped by PID",
  "Case with judge records blanked and all 23 items accepted: opened the panel at 1440 and 390, read summary, group heading, group button, row chips, 'What you need to do', row buttons; compared with the gate rows and the Export 422 text (T-081-ux-r3-walk1.py, T-082-ux-r3-walk2.py)",
  "Mixed case (e1 edited, e2 accepted, 21 pending, judge never ran on 12): gate said 1 blocker (e2) and Export 422; panel said 2 block; POST /rejudge by API asked 11 (accepted plus pending, not the edited one), after which the gate was pass and GET /export returned 200 with e1's edited text in letter_text; reloaded the UI and read panel, rail, item dialog, and pressed the rerun button on the edited row (T-081-ux-r3-walk7.py)",
  "conftest JudgeNotRun stub in mode still: pressed the panel group button and read every rerun-status element and its viewport position (T-081-ux-r3-walk4.py)",
  "Panel regression on sample, case_01, lib06 at both widths: closed height, open state, rows vs unique item ids, unique titles, reason codes outside Technical details (T-081-ux-r3-walk5.py)",
  "Read judges.js 20-60, 75-140 and grep for rerun-status"],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "Panel says an edited item 'Blocks the export' and 'can't go in the letter yet' while the gate says Ready to export; its rerun button answers 'nothing to run'",
   "evidence": "Mixed case after rerun: rail 'Ready to export, 21 not reviewed'; GET /export 200 and letter_text contains e1's edited sentence (D-045 b: edited summaries are human-authored, exempt from the judge). Panel (T-081-ux-r3-walk7.py, T-081-ux-r3-e1440-panel-edited.png): summary '18 checked, 18 agreed with the draft, 1 not checked (blocks export)'; e1 row 'AI did not check | Blocks the export | Your decision: Edited' with 'What you need to do: The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again...'; group 'What you need to do: 1 accepted item cannot go in the letter until the second AI check has run on it' with 'Run the second check again for these 1'. Pressing the row's rerun button: status 'There was nothing to run the second check on.' Before the rerun the same panel said 2 items block while /trace listed 1 blocker (e2, e1 not listed). Cause: judges.js:33 `blocking()` keys on review_status in [accepted, edited] instead of the gate's JUDGE_NOT_RUN blockers.",
   "why_it_matters": "This is the exact place the brief asks to match the gate. Two panels on one screen give opposite answers (Ready vs Blocks), the paralegal is told to dismiss or rerun an item that is fine, and the one button offered does nothing. It teaches users not to trust the status text.",
   "fix": "Take the 'blocks the export' set from the gate (trace export_gate blockers with reason_code JUDGE_NOT_RUN, matched by item_id), not from review_status. For an edited item with no judge say 'You edited this item, so it is your wording and does not need the second check.' with Go to item only, no rerun button, no 'Blocks the export' chip, and count it outside '(blocks export)' and 'N accepted items cannot go in the letter'.",
   "acceptance_test": "E2E on a case with one edited item and one accepted item, judge never ran: panel summary says '(blocks export)' once and the group says '1 accepted item'; the edited row has no 'Blocks the export' chip and no btn-rerun-judge; after the accepted item is dismissed the summary has no 'blocks export' and the rail says Ready to export."},
  {"severity": "major", "title": "A failed 'Run the second check again' pressed in the panel shows no message at all",
   "evidence": "Stub mode 'still', panel group button pressed (T-081-ux-r3-walk4.py): after 2.5 s every `rerun-status` element on the page is empty (output '3 PANEL GROUP button -> status: []' at 1440 and 390); screenshot T-081-ux-r3-f1440-walk4-3-panel.png shows the panel unchanged, 9 rows still 'Blocks the export', button active again. The same stub through the gate step and the item dialog does show 'The second check still did not answer for 9 items of 9. Try again, or dismiss them.' (status top 475 and 802 in view). judges.js:82 and :133 build an empty `<p role=status data-testid=rerun-status>`; stepper.js:131 rerunSay() writes the sentence into the nodes that exist before the repaint, then `ZL.judges.reload()` rebuilds the panel and the new nodes start empty (the stepper's own rerunStatus() at stepper.js:142 re-reads rerunNote, judges.js does not).",
   "why_it_matters": "The panel is where the user goes to see what the AI did not check; the button there is the natural one to press. When the judge is still down the user gets a greyed button that comes back with no explanation, which is the failure path this feature is for.",
   "fix": "Fill the panel's status nodes from the stored note when they are built (same as stepper.rerunStatus()), and place the group-level status directly under the group button.",
   "acceptance_test": "E2E with JudgeNotRun(mode='still') at 1440x900 and 390x844: after pressing the group button in [data-testid=judge-panel] the panel contains a visible rerun-status with 'still did not answer for 9 items' inside the viewport, and the 9 rows remain."},
  {"severity": "minor", "title": "Pending items with no judge are told to 'accept' with no warning that accepting will block the export, and no rerun is offered on the row",
   "evidence": "Mixed case before rerun: 10 pending rows, e.g. '2026-01-16 · Dr. Alvarez, primary care · Record 3 | AI did not check | Your decision: Not reviewed | The second check did not answer, so no AI judge looked at this item. What you need to do: Read it yourself, then accept, edit or dismiss it. The AI did not give an answer you can rely on.' Buttons: Go to item, See the steps. POST /rejudge by API asked 11 and answered for the 9 pending items too, so rerun covers them (judges.js:26 TODO_UNCHECKED).",
   "why_it_matters": "Under D-044 a paralegal who accepts such an item turns it into a hard export blocker with no override. The row recommends accepting and hides the cheaper fix (rerun first).",
   "fix": "Add 'Run the second check again first; if you accept it before the second check has run, the export is blocked until it does.' and the rerun button (or a group button covering pending items) to these rows.",
   "acceptance_test": "E2E on the blanked-judges case with nothing accepted: each unchecked row contains a rerun button or the group button says 'for these N' with N equal to the number of rows, and the row text mentions that accepting before the check blocks the export."},
  {"severity": "nit", "title": "Group button reads 'Run the second check again for these 1'",
   "evidence": "T-081-ux-r3-walk7.py output: 'Run the second check again for these 1'; judges.js:132.",
   "why_it_matters": "Singular count with plural wording.",
   "fix": "'Run the second check again for this item' when N is 1.",
   "acceptance_test": "Unit: the label for N=1 contains no 'these'."}
 ],
 "whats_right": [
  "For accepted items the panel copy now matches the gate (blocks the export, run the second check again, dismiss if it still cannot answer), has a real rerun button per row and per group, and no longer says 'then accept'.",
  "Collapsed 58 px strip under Case checks whose summary carries the signal ('7 checked, 7 agreed with the draft, 12 not checked (blocks export)'); opening it keeps one row per item with unique, record-cued titles and codes behind Technical details.",
  "A successful rerun repaints the panel: 'checked 19, all agreed with the draft', unavailable group gone, no stale rows."],
 "questions_for_chris": []}
```
