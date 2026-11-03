# T-082 round 2, ux-designer-reviewer: "How the AI was checked" panel

Verdict: **changes** (0 blockers, 1 major). Frontend commit 8e3c26c (`git diff 8e3c26c HEAD -- app/frontend` is empty at HEAD f49c4c2); backend fe4ee80.

Exercised: own servers at HEAD (fixture, curated, `ZLAYT_DB` in my scratchpad): :7881 local mode (lib06 with 3 objections, sample, case_01, and a sample case with the judge records blanked and every item accepted) and :7882 demo mode (sample, case_01). Playwright at 1440x900 and 390x844: closed height and position, open height, every row (title, record cue, chips, "What you need to do"), duplicates by item id, text outside Technical details, scrollW. Servers stopped (curl 000). Evidence: `artifacts/review-evidence/T-082-ux-r2-*.png`, `T-082-ux-r2-walk1.py`, `walk2.py`.

Round-1 majors:
1. Panel was a full-page non-collapsible block at the bottom: **fixed**. It is a `details`, closed on load, directly under "Case checks" and above the timeline. Closed height 58 px at 1440 (88 to 110 at 390), summary carries the signal: lib06 "16 checked, 13 agreed with the draft, 3 questioned", sample "checked 19, all agreed with the draft", unjudged case "7 checked, 7 agreed with the draft, 12 not checked". Demo sample: panel top y=475 at 1440. Opening lib06 shows 1896 px (2.1 screens) at 1440; that is on demand.
2. Same item listed up to three times, identical flag titles: **fixed**. lib06: 3 objection rows (a3, a7, f_r5_1) + 3 disagreement rows (e5, f_r3_2, f_r4_1) = 6 distinct item ids, 6 rows, each once; headings count items ("Where the AI objected (3 items)"). Chips on the row carry the second reason (f_r5_1: "AI objected" + "The phrase list and the AI disagree"). Titles are unique and every one carries the record cue: "Attorney referral · Record 3" vs "Attorney referral · Record 4", "$450 (unclear) · Record 4", "$1,150 (unclear) · Record 5". Sample and unjudged case: record cue on all 13 and 1 rows respectively.
Round-1 minors: objection rows now say "What you need to do: Compare the amount with the quote yourself. Accept it as a charge, leave it unclear, or dismiss it." with Go to item as the primary button; reason codes and prompt versions sit in Technical details; the tile reads "agreed with the draft". The one line "Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5 (a different model...)" is still in the main view on purpose; I accept that as the trust line.

New finding from the T-080 r3 check (finding 1): for items the AI never checked, the panel gives advice that contradicts the export gate.

```json
{"card": "T-082", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "frontend commit 8e3c26c (identical at HEAD f49c4c2) app/frontend/judges.js, stepper.css; backend fe4ee80; local app :7881 and demo :7882; lib06, sample, case_01, sample with judges blanked; 1440x900 and 390x844",
 "exercised": [
  "Started own servers at HEAD on :7881 (local) and :7882 (demo), fixture curated, ZLAYT_DB in scratchpad; stopped after (curl 000)",
  "Playwright 1440x900 and 390x844 on lib06, sample, case_01 and the blanked-judges case: closed/open bbox, position vs queue, summary text, details.open on load",
  "Counted rows per item id, duplicate titles, record cue on every row, 'What you need to do' presence, groups and headings",
  "Regex for reason codes, prompt ids and rule text outside Technical details",
  "Opened the panel on the blanked-judges case with all items accepted; read the unresolved rows, buttons and network (no POST); curled /judges and compared with judges.js",
  "Read judges.js (byItem, row, TODO_UNCHECKED) and the round-1 review"],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "Rows for items the AI never checked tell an accepted item to 'accept' it again, contradicting the export gate, and offer no rerun",
   "evidence": "Blanked-judges case, 12 items accepted: panel group 'Where the AI could not check or decide (12 items)', each row 'AI did not check / Your decision: Accepted ... What you need to do: Read it yourself, then accept, edit or dismiss it. The AI did not give an answer you can rely on.' buttons Go to item and See the steps only (T-082-ux-r2-walk2.py output, T-082-ux-r2-jnr-1440-panel-top.png). judges.js:26 TODO_UNCHECKED is a hard-coded client string. The same case's gate says 'You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it' and Export returns 422 judge_not_run (D-044, backend fe4ee80). No button in the panel calls POST /rejudge (network log empty; grep rejudge in app/frontend is empty).",
   "why_it_matters": "The panel is where the paralegal lands to understand what the AI did not check. For an already-accepted item it recommends the one action that D-044 says does nothing for the gate, and it omits the only action that does (run the second check again). Two panels on one screen give opposite instructions.",
   "fix": "In row(), branch on review_status: for accepted/edited + unavailable rows say 'The second AI check never ran on this item, so it blocks the export even though you accepted it. Run the second check again.' with a primary 'Run the second check again' button (POST /rejudge, same handler as the gate; status line while running; repaint panel from the response). Keep 'Read it yourself, then accept, edit or dismiss it' only for items not yet decided. Add a group-level 'Run the second check again for these 12' button. Show the live gate state in the summary: '12 not checked, export blocked'.",
   "acceptance_test": "E2E on the unjudged case with all items accepted: no judge-unresolved row contains 'then accept'; each row (or the group) has a 'Run the second check again' button; clicking it sends one POST /api/cases/{token}/rejudge and the panel summary updates from the response; if the backend answers still_unavailable the rows stay and a plain message names the count."},
  {"severity": "minor", "title": "Panel summary does not say the export is blocked by unchecked items",
   "evidence": "Unjudged case: panel summary '7 checked, 7 agreed with the draft, 12 not checked' in neutral styling while the case strip says 'Export blocked by 12' (T-082-ux-r2-jnr-1440-top.png). Summary class is zs-sumv zj-sum-bad only; no link between 'not checked' and the gate.",
   "why_it_matters": "'12 not checked' reads as informational; under D-044 it is a hard blocker.",
   "fix": "Append 'blocks export' to the summary when any unchecked item is accepted or edited.",
   "acceptance_test": "E2E: summary text contains 'blocks export' on the unjudged case with accepted items and not on lib06."},
  {"severity": "nit", "title": "Opened panel is long on a phone",
   "evidence": "lib06 at 390: opened height 3087 px; unjudged case 5683 px (T-082-ux-r2-walk1.py output).",
   "why_it_matters": "Collapsed by default so it no longer competes with the queue; only an issue once opened.",
   "fix": "Cap the visible rows at 5 per group with 'Show the other N' as the gate step already does.",
   "acceptance_test": "E2E at 390x844: opened unjudged panel shows at most 5 rows per group before 'Show the other 7'."}
 ],
 "whats_right": [
  "Collapsed by default, placed right under Case checks, with a one-line count that carries the signal (16 checked, 13 agreed with the draft, 3 questioned).",
  "One row per item with the second reason as a chip and a record cue on every title, so the two 'Attorney referral' flags are told apart (Record 3 / Record 4).",
  "Each objection row now ends with a plain 'What you need to do' sentence and a primary Go to item button, with codes and prompt versions behind Technical details."],
 "questions_for_chris": []}
```
