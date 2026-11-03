# T-149 paralegal review (paralegal-reviewer, Maria Delgado persona): multi-case overview and detail

Verdict: **changes** (0 blockers, 3 majors, 3 minors). Pinned commit 25f585c (HEAD at review start; the card lists 1394661, which is an ancestor). I ran `git archive 25f585c` into a fresh scratchpad directory (`r3-25f585c`) and served it on 127.0.0.1:7941 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. I seeded 6 cases through the API (library cases 01, 06, 02, 03, 09 plus the Rivera sample; 06 and 03 with entries accepted, 09 left unanalyzed), and my T-136 runs added five more pasted cases, so I also saw 11. The server (PID 21600) was stopped: `lsof -iTCP:7941 -sTCP:LISTEN` exit 1, curl 000. Port 7860 was not touched. Scripts and outputs: `artifacts/review-evidence/T-149-paralegal/`.

## The two questions I was asked

**1. With 5+ cases, can I see which need me, why, and what is ready to send? Partly. Which one is which, and what is ready, fail.**
- Each row shows a progress bar per kind, chips ("4 need review", "1 could not be verified", "Export blocked (1)") and the server's own blocker sentence. "Needs attention first" puts the blocked cases on top and both filters work (`o1.out.txt`, `o1-overview-1440.png`). The rows are readable and the counts match `GET /api/cases` (`setup.out.txt`).
- But "Ready to export" is green on a case with 1 of 7 entries accepted, 13 items not reviewed and 4 needing review (F-2), so I cannot tell what is ready to send. And the cases I pasted are all called "Untitled case, Nov 2" (F-1), so with 5 clients I cannot tell which row is which.

**2. Does the overview block tell me what to do first? No.** It tells me the status. The action is in a different block, and the three places that could say "do this first" disagree (F-3).

## Findings

**F-1 (major). Pasted cases all read "Untitled case, Nov 2"; there is no way to name one, so five clients are five identical rows.** The home screen has only the paste box and "Upload .txt" (`o6.out.txt`, "inputs on home: input-text, file-input"; no name field and no rename). With five pasted cases, the order by "Needs attention first" reads: `Untitled case, Nov 2 / Created Nov 2, 2026, 8:30 AM`, then 8:29, 8:28, 8:27, 8:26 (`o6.out.txt`; `o6-eleven-cases.png`). The rows differ only by the creation minute. A paralegal with Rivera, Smith and Ochoa open cannot pick the right one, and an overview of cases she cannot tell apart does not tell her which need her. Fix: a case name field next to Analyze (client or matter), a rename on the row and in the detail header, and when no name is given default the title to something she can recognise from the records (provider of record 1 and the date range, never a guessed client name). Acceptance test: paste two different texts without a name, open the overview, assert the two row titles differ and each contains text taken from its own records; rename a case and assert the new name shows in the row and the detail header after a reload.

**F-2 (major). "Ready to export" is green on cases that are far from ready to send; the "Needs attention" filter equals "All cases"; so "what is ready to send?" has no answer.** `GET /api/cases` marks `export_ready: true` when nothing blocks the gate, and the UI turns that into the same green chip a finished case would get. Rows as seen: "Truck rear-end, chiropractic plan: Entries 1 of 7, Flags 0 of 4, Amounts 0 of 3, 4 need review, Ready to export, 13 items are not reviewed" and "Letter of protection: Entries 5 of 7, 8 need review, 1 could not be verified, Ready to export, 14 items are not reviewed" (`o1.out.txt`). After I accepted ONE charge on the Rivera sample, that case went green with 21 items not reviewed (`o4.out.txt`: "sample after one charge accepted: export_ready True []"; the row then reads "Ready to export" with "21 items are not reviewed"). The filter chips read "All cases (6)", "Needs attention (6)", "Ready to export (2)" (`o1.out.txt`): all six cases need attention, including the two marked ready. The two counts on one row ("4 need review" and "13 items are not reviewed") are not explained, either. To a paralegal "ready to send" means everything is decided, or the rest was dismissed on purpose. A letter with one of seven entries in it is exactly the demand that gets sent half-finished. Fix: keep "Can export" (gate passes) apart from "Ready to send" (nothing left to decide). For a case with undecided items show an amber "Can export, 13 not reviewed" and keep the green chip for nothing pending; make the "Ready to export" filter use the stricter test and say so. Acceptance test: a case with undecided items has no element with `cases-chip-ready` and is not listed under the ready filter; a case with 0 pending and 0 edits to check shows the green chip and is listed.

**F-3 (major). The case overview block does not say what to do first; the block, "Open decisions" and "What you need to do" give different answers, and the action names no item.**
- Rivera sample (`o3.out.txt`, `o2-detail-sample-1440.png`): the overview block says "Export blocked (1): Nothing is accepted or edited yet, so the letter would be empty." The "Open decisions" card says "Start review, 3 items need review" and its button moves focus to flag `f_r7_1` (the accident-date source), not to the first entry. The "What you need to do" bar says "Decide the 2 detected charges: accept the ones that are billed charges, dismiss the rest." Three different first steps in one screen. Accepting a charge does clear the blocker (I checked: `export_ready` turned true), but that is not what a paralegal does first with a nine-entry case.
- Slip and fall (lib02, `o3.out.txt`, `o2-detail-lib02-1440.png`): "What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record." No item is named ("this item"), while the overview block above it shows 7 entries and 8 flags to decide. The item only appears after "Show this step" (`o4-lib01-show-step.png`, which also shows a raw `record ids ["r3"]` line).
- On a 900 px screen the case overview, "Open decisions" and "Case checks" blocks are stacked above the timeline, and the first screen holds two entry rows (`o2-detail-sample-1440.png`).
Fix: one line, "Do this first: ...", inside the overview block, built from the server's next action and naming the item (record number and provider), with one button that goes to it; show "Start review" and the case-checks bar only as the same action, never as a second one. Acceptance test: on the Rivera sample and lib02 the overview block contains exactly one "Do this first" line; its text names a record or provider; clicking its button focuses the item it names; the line, "Start review" and the case-checks bar never name different targets.

**F-4 (minor). A case that was never analyzed shows "9 need review" and "Export blocked: Nothing is accepted or edited yet" and no hint to run the analysis.** Spanish-language records, back pain: status chip "Not analyzed yet", Entries "None", "9 need review", "Export blocked (1)" (`o1.out.txt`, `o1-overview-1440.png`). The honest next step, Analyze, shows only after opening the case ("Read by code only. No model has been called yet." `o2.out.txt`, lib09). Fix: for an ingested case show "Not analyzed. Open it and press Analyze" as the row's reason and drop the review and blocker chips.

**F-5 (minor). The row says how many but never why.** "4 need review" does not say that one is a date conflict, one a gap, one a prior condition. Maria's rule 16 is "say why in one sentence". The server has the kinds (`kinds: gap 1, conflict 2, pre existing 2, causation 5` is in the case trace). Fix: a one-line "why" under the chips, for example "1 date conflict, 1 gap, 2 prior conditions".

**F-6 (minor). The card's AC evidence "test_multicase.py 17 pass" did not reproduce.** In the archive, run with plain pytest (own private server, `env -u ZLAYT_DB`): `16 passed, 1 skipped, 1 failed`; the failure is `test_keyboard_only_open_move_between_rows_and_return_with_focus_on_the_case`, "ArrowDown moves to the next row's link" (`pytest-multicase.out.txt`; same failure in a second run). In the live app on my server ArrowDown, j and Tab all moved row to row and Enter opened the case, 3 of 3 times with a 600 ms wait after load (`o5.out.txt`), so I believe the key handler is bound after a delay or after a poll render, and the test presses before it. A paralegal who presses a key at once after the list paints loses the key. Fix: bind the handler before the rows paint, or have the test wait on a ready marker, and say which in the card.

## What I ran

1. `git rev-parse --short HEAD` = 25f585c; `git archive 25f585c | tar -x -C <scratchpad>/r3-25f585c`; server under `.venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py`; curl 200; stopped by PID 21600 (lsof exit 1, curl 000).
2. `setup_cases.py`: 6 cases seeded and GET /api/cases read (`setup.out.txt`).
3. `o1_overview.py`: overview text, default order, filters, all four sorts (`o1.out.txt`).
4. `o2_detail.py` and `o3_next.py`: opened five cases from the overview; read the overview block, next action, case summary and the trace's next_action per step (`o2.out.txt`, `o3.out.txt`).
5. `o4_actions.py`: "Show this step", one charge accepted via the API (gate), one entry accepted in the detail, back to the overview (counts, "Last activity", focus lands on the case link), reload (returns to the overview), 390 px overview and detail with no horizontal overflow (`o4.out.txt`).
6. `o5_keys.py`: ArrowDown, j, Tab, Enter on the overview, 3 runs (`o5.out.txt`). `o6_many.py`: 11 cases, name inputs, sort by attention (`o6.out.txt`).
7. `tests/e2e/test_multicase.py` from the archive with plain pytest, twice (`pytest-multicase.out.txt`).
8. Screenshots read: `o1-overview-1440.png`, `o2-detail-sample-1440.png`, `o2-detail-lib06-1440.png`, `o4-lib01-show-step.png`, `o4-detail-390.png`.

Things outside my lens: whether the overview should show Stowers/limitation deadlines per case is a product call (see the question below); visual design beyond what slowed verification.

```json
{"card": "T-149", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 25f585c (HEAD at review start; card commit 1394661 is an ancestor) served on http://127.0.0.1:7941 (PID 21600, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; 6 seeded cases (library 01, 06, 02, 03, 09 + Rivera sample) plus 5 pasted cases; live dev app 7860 not touched",
 "exercised": [
  "git archive 25f585c into a fresh scratchpad dir; server on 7941 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 21600 (lsof exit 1, curl 000)",
  "seeded 6 cases through the API and read GET /api/cases (setup_cases.py, setup.out.txt)",
  "overview in the browser: row text, default order, three filters, four sorts (o1_overview.py)",
  "opened five cases from the overview and read the case overview block, next action and case checks; read the trace next_action per step (o2_detail.py, o3_next.py)",
  "Show this step on lib01; one charge accepted via API to read the gate; one entry accepted in the detail then All cases (counts, last activity, focus); reload; 390 px overview and detail (o4_actions.py)",
  "keyboard on the overview: ArrowDown, j, Tab, Enter, 3 runs (o5_keys.py)",
  "11-case overview, name inputs on the home screen, attention sort (o6_many.py)",
  "tests/e2e/test_multicase.py from the archive with plain pytest, twice: 16 passed, 1 skipped, 1 failed (keyboard test)",
  "read the card, the handoff, overview.js header and sort/filter code, api.md case-list section; screenshots o1-overview-1440, o2-detail-sample-1440, o2-detail-lib06-1440, o4-lib01-show-step, o4-detail-390"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "overview_triage": 3, "ready_to_send_signal": 2, "detail_first_action": 2, "identify_case": 2},
 "findings": [
  {"severity": "major", "title": "Pasted cases all read 'Untitled case, Nov 2' and cannot be named, so five clients are five identical rows",
   "evidence": "artifacts/review-evidence/T-149-paralegal/o6.out.txt: inputs on home = input-text and file-input only; attention order lists five rows 'Untitled case, Nov 2 / Created Nov 2, 2026, 8:30 AM' ... 8:26 AM; o6-eleven-cases.png",
   "why_it_matters": "She manages 5+ cases. An overview of rows she cannot tell apart does not show which cases need her, and she may open or export the wrong client's file.",
   "fix": "Name field beside Analyze, rename on the row and in the detail header, and a recognisable default title taken from the records (provider of record 1 and date range), never a guessed client name.",
   "acceptance_test": "e2e: paste two different texts with no name; the two overview row titles differ and each contains text from its own records; rename a case and the new name shows in the row and the detail header after reload."},
  {"severity": "major", "title": "'Ready to export' is green on cases far from ready to send; the Needs attention filter equals All cases",
   "evidence": "o1.out.txt: 'Truck rear-end, chiropractic plan | Entries 1 of 7 ... 4 need review | Ready to export | 13 items are not reviewed'; 'Letter of protection ... 5 of 7 ... 8 need review ... Ready to export | 14 items are not reviewed'; filters 'All cases (6)', 'Needs attention (6)', 'Ready to export (2)'; o4.out.txt: one charge accepted -> 'export_ready True []' and the row reads Ready to export with 21 items not reviewed",
   "why_it_matters": "A green ready chip on a letter that carries 1 of 7 entries invites a half-finished demand to go out; the paralegal cannot answer 'what is ready to send' from the overview.",
   "fix": "Separate 'Can export' (gate passes, items undecided; amber, with the unreviewed count) from 'Ready to send' (nothing pending, no edit to check; green). The Ready filter uses the stricter test.",
   "acceptance_test": "e2e: a case with pending items has no cases-chip-ready and is not under the ready filter; a case with 0 pending and 0 edits to check shows the green chip and is listed."},
  {"severity": "major", "title": "The case overview block does not say what to do first; overview block, Open decisions and What you need to do disagree, and the action names no item",
   "evidence": "o3.out.txt sample: block 'Export blocked (1): Nothing is accepted or edited yet'; Open decisions 'Start review' focuses f_r7_1 (flag); case-next-action 'Decide the 2 detected charges'. lib02: case-next-action 'This item cannot be used. Dismiss it, or write the entry by hand from the record.' with no item named while the block shows 7 entries and 8 flags to decide; o2-detail-sample-1440.png; o4-lib01-show-step.png (raw 'record ids [\"r3\"]')",
   "why_it_matters": "She asked 'what do I do first?' on opening the case and got three answers or an unnamed 'this item'; the first screen at 900 px holds only two entry rows.",
   "fix": "One 'Do this first' line in the overview block from the server's next action, naming record and provider, with one button to it; 'Start review' and the case-checks bar repeat the same action only.",
   "acceptance_test": "e2e on the Rivera sample and lib02: the overview block has exactly one 'Do this first' line naming a record or provider; its button focuses that item; Start review and the case-checks bar never name a different target."},
  {"severity": "minor", "title": "A never-analyzed case shows '9 need review' and 'Export blocked: Nothing is accepted' with no hint to run the analysis",
   "evidence": "o1.out.txt row 'Spanish-language records, back pain | Not analyzed yet | Entries None | 9 need review | Export blocked (1) | Nothing is accepted or edited yet'; o2.out.txt lib09 detail 'Read by code only. No model has been called yet.'",
   "why_it_matters": "The reason shown is not the reason she must act; the real next step (Analyze) is only visible after opening the case.",
   "fix": "For an ingested case the row's reason reads 'Not analyzed. Open it and press Analyze' and the review and blocker chips are dropped.",
   "acceptance_test": "e2e: an ingested case row has no cases-chip-blocked and no cases-chip-needs-review and its reason text contains 'Analyze'."},
  {"severity": "minor", "title": "Row says how many items need review but never why",
   "evidence": "o1.out.txt chips '4 need review', '8 need review' with no kind; case trace 'kinds: gap 1, conflict 2, pre existing 2, causation 5' exists on the server (r2 stepper text in T-136-paralegal-r3/r2.stdout.txt)",
   "why_it_matters": "Checklist item 16: items needing review say why in one sentence; she cannot rank cases by what the adjuster will attack (a date conflict, a gap).",
   "fix": "One line under the chips: '1 date conflict, 1 gap, 2 prior conditions', from the server's counts.",
   "acceptance_test": "e2e: the Rivera sample row contains 'conflict' and 'gap' counts equal to the flags of those kinds in GET /api/cases/{token}."},
  {"severity": "minor", "title": "AC evidence 'test_multicase.py 17 pass' does not reproduce: the keyboard test fails on HEAD",
   "evidence": "artifacts/review-evidence/T-149-paralegal/pytest-multicase.out.txt: '1 failed, 16 passed, 1 skipped'; tests/e2e/test_multicase.py:253 'ArrowDown moves to the next row's link'; the same failure in a second run; live check o5.out.txt ArrowDown/j/Tab move focus 3 of 3 with a 600 ms wait",
   "why_it_matters": "The card's own AC (keyboard usable) is evidenced by a test that fails in a clean archive; a key pressed right after the list paints is lost.",
   "fix": "Bind the key handler before the rows paint, or wait on a ready marker in the test, and state which in the card.",
   "acceptance_test": "plain pytest tests/e2e/test_multicase.py in a clean archive: 17 passed, 3 runs in a row."}
 ],
 "whats_right": [
  "Overview rows carry the server's own plain blocker sentence, per-kind decided/total bars and counts that match GET /api/cases; Back and All cases return with focus on the case link and the counts refresh after an accept.",
  "Sorting by 'Needs attention first' puts blocked and unanalyzed cases on top, filters and sort hold across open and back, and the 390 px overview and detail have no horizontal overflow.",
  "The detail's export-gate steps open with 'Show this step' and land on the right step with its 'Go to the record' button."
 ],
 "questions_for_chris": ["Should the overview show a deadline per case (Stowers or limitation date)? A paralegal sorts her cases by it; the records carry no such date, so it would be a field she types. Outside my lens to decide, but it changes what 'needs me first' means."]}
```

Erratum (appended, same review): where I wrote that ArrowDown, j and Tab moved focus (the F-6 paragraph and the F-6 evidence field), read "ArrowDown and Tab moved focus; j did nothing" (o5.out.txt, 3 of 3 runs). It does not change any finding.
