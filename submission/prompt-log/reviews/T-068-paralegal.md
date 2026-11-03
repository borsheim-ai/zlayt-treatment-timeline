# T-068 review — paralegal-reviewer (Maria Delgado persona)

Scope: commit 89a323a (app/frontend/timeline.js, tests/e2e/test_input.py). Verified on a committed snapshot of 89a323a served on http://127.0.0.1:7881 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local), case_01 pasted from evals/golden/case_01_date_formats.txt.

## What I checked

The row I was asked about is there and it is verifiable. Record 8 appears under "Dates to confirm" with no undated entry: "Record 8: Dr. Orla Pennywhistle, phone note / Date to confirm / Written as “04/05/2026”. Which date? / April 5, 2026 / May 4, 2026 / Open record 8". The provider is as written, the raw date is verbatim, both readings are offered, and the tool does not pick one. "Open record 8" opens the verbatim block, including "Excerpt: "Patient reports no new symptoms."".

The confirm action does not do what the panel promises. After clicking April 5, 2026, the row disappears and the panel reads "None. Every record has a readable date." The timeline has zero entries. Record 8 only reappears under "Records without an entry (8)" with an April 5, 2026 chip and "Enter this record by hand". The panel copy says records are "left off the timeline ... until you pick the right date", but picking the date does not put it on the timeline. Nothing is lost (the record stays visible and recoverable by hand), so I rate this major, not blocker.

Record 8 is also listed twice before any confirm: once in the Dates row and once as an "undated" card in "Records without an entry".

The e2e test that carries AC 1 asserts only that the text "04/05/2026" appears in the panel. It passes whichever branch renders the row, so it does not test the confirm or open-record actions this card is about.

Separately, the committed build shows no timeline entries at all for case_01 under the curated fixtures. That is not caused by this diff, but it means the chronology is empty at 89a323a.

Recorded run notes: the brief's launch line `--port 7881` is ignored, because app/main.py reads the PORT env var (app/main.py:14). I used `PORT=7881` and a scratch DATA_DIR. The live app on :7860 was not touched. My server on :7881 is stopped.

## Verdict

changes (0 blockers, 3 majors, 2 minors). Ship bar for verify_quickly (≥ 4) is not met: 3.

## Evidence

- artifacts/review-evidence/T-068/T-068-explore-dump-commit-89a323a.json (orphan row text, confirm buttons, zero entries)
- artifacts/review-evidence/T-068/T-068-confirm-dump-commit-89a323a.json (steps 1 to 4: before/after confirm, reload)
- artifacts/review-evidence/T-068/T-068-dup-probe-commit-89a323a.json (record 8 counted once in each panel)
- artifacts/review-evidence/T-068/T-068-commit-01-dates-to-confirm-before.png
- artifacts/review-evidence/T-068/T-068-commit-02-open-record-8-modal.png
- artifacts/review-evidence/T-068/T-068-commit-03-after-confirm-april-5.png
- artifacts/review-evidence/T-068/T-068-commit-04-after-reload.png
- Scripts: artifacts/review-evidence/T-068-paralegal-explore.py, T-068-paralegal-confirm.py, T-068-paralegal-dup-probe.py

Server log for the empty-timeline finding: scratchpad t068-server-commit2.log (18 lines "llm call failed ... step=flags", logged by app/llm/audited.py:87).

## Findings

F1 (major) confirm on an orphan row leaves the record off the timeline. See the confirm dump and the after-confirm screenshot. Backend review.confirm_date only moves an existing entry (`moved=None` when none exists, app/backend/review.py ~line 154 to 180), so confirm sets the date and nothing reaches the timeline.

F2 (minor) record 8 appears in two panels before confirm. Dup probe: `dates_row_r8_count: 1`, `missing_card_r8_count: 1`.

F3 (minor) the Dates row has no verbatim excerpt. The excerpt is one click away in the modal.

F4 (minor) AC 1 evidence is text-only. tests/e2e/test_input.py lines 29 to 32 assert `to_contain_text("04/05/2026")` only.

F5 (major) committed 89a323a shows zero timeline entries for case_01 under the curated fixtures. Root cause is the fixture and prompt mismatch (step=flags misses), which is outside my lens. Owner backend/qa. The working tree, which has uncommitted backend and fixture changes, shows 8 entries including an undated entry for record 8, so the orphan branch is not reached there. That run's JSON was overwritten; the output is in the transcript.

```json
{"card": "T-068", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 89a323a (app/frontend/timeline.js, tests/e2e/test_input.py); app http://127.0.0.1:7881 served from a git-archive snapshot of 89a323a (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local); sample case evals/golden/case_01_date_formats.txt pasted",
 "exercised": [
   "read personas/paralegal.md, docs/RUNBOOK.md, board show T-068, git show 89a323a diff of app/frontend/timeline.js and tests/e2e/test_input.py",
   "started a committed-snapshot app on :7881 with a scratch DATA_DIR (PORT env var; --port flag is ignored by app/main.py), confirmed HTTP 200, stopped it afterwards; :7860 untouched",
   "Playwright (.venv) paste case_01, Analyze, read Dates to confirm: orphan row for r8 with raw 04/05/2026, candidates April 5, 2026 and May 4, 2026, Open record 8",
   "Playwright Open record 8: read record modal text (Date 04/05/2026, Source Dr. Orla Pennywhistle, phone note, Excerpt Patient reports no new symptoms.)",
   "Playwright click confirm-date 2026-04-05: read Dates panel, timeline entries (0), record count, Records without an entry card; reload and re-read",
   "Playwright duplicate count of record 8 across Dates row and Records without an entry before confirm",
   "viewed screenshot T-068-commit-03-after-confirm-april-5.png",
   "grep and read tests/e2e/test_input.py assertion at lines 29 to 32; read app/backend/review.py confirm_date; read app/frontend/manual.js records-without-entry panel",
   "git status and ls-files comparison of worktree vs committed fixtures; read server log for fixture-miss lines"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "record_8_listed_with_verbatim_date_and_provider": 4, "confirm_outcome_clear": 2, "ac_evidence_matches_actions": 2},
 "findings": [
   {"severity": "major", "title": "Confirming the date of an orphan Dates-to-confirm row does not put the record on the timeline",
    "evidence": "artifacts/review-evidence/T-068/T-068-confirm-dump-commit-89a323a.json steps 3_row_count_after_confirm=0, 3_dates_to_confirm_panel_after=“None. Every record has a readable date.”, 3_timeline_entries_after=[]; screenshot artifacts/review-evidence/T-068/T-068-commit-03-after-confirm-april-5.png shows Record 8 only under “Records without an entry (8)” with chip April 5, 2026 and “Enter this record by hand”; backend app/backend/review.py confirm_date sets moved=None when no entry exists",
    "why_it_matters": "The panel says records are left off the timeline until the paralegal picks the date, but picking the date does not add the record. The paralegal must notice the record moved to another panel and enter it by hand. The record is not lost, so this is not a blocker, but the confirm action is a dead end on screen.",
    "fix": "Either create the timeline entry from the confirmed record (backend), or keep the row after confirm with text such as “Date confirmed April 5, 2026. Not yet on the timeline: enter this record by hand” and a btn-manual-entry control. Correct the panel copy to match.",
    "acceptance_test": "E2E on a build where r8 has no entry: paste case_01, confirm 2026-04-05; assert either a timeline entry dated April 5, 2026 whose excerpt contains “Patient reports no new symptoms.”, or the Dates panel keeps r8 with a visible manual-entry control and the confirmed date text."},
   {"severity": "major", "title": "Committed 89a323a shows no timeline entries for case_01 under the curated fixture set",
    "evidence": "artifacts/review-evidence/T-068/T-068-explore-dump-commit-89a323a.json timeline_entry_testids has no entry-N; scratchpad t068-server-commit2.log has 18 lines 'llm call failed ... step=flags' (logged at app/llm/audited.py:87). The working-tree server (uncommitted app/backend/*.py and app/llm/backends/fixture.py changes) rendered entry-1 to entry-8 including an undated entry-8 for record 8 (transcript output; that JSON was overwritten).",
    "why_it_matters": "At the reviewed commit the chronology for the sample case is empty, so none of the Dates-to-confirm behaviour can be checked against neighbouring entries. Root cause is outside timeline.js (fixture and prompt mismatch and uncommitted backend changes), so it is outside my lens to fix; I report it because it makes the reviewed state unusable.",
    "fix": "Owner backend/qa: make the committed backend and the committed fixture set agree (commit the missing fixtures and the backend changes they were recorded against), then re-run the curated case_01 at the commit being reviewed.",
    "acceptance_test": "On the commit under review, serving LLM_BACKEND=fixture FIXTURE_SET=curated, case_01 produces entries for records 1 to 7 and zero 'llm call failed' log lines."},
   {"severity": "minor", "title": "Record 8 is listed twice before any confirm (Dates row and Records without an entry)",
    "evidence": "artifacts/review-evidence/T-068/T-068-dup-probe-commit-89a323a.json: dates_row_r8_count 1, missing_card_r8_count 1, missing_card_r8_text “Record 8: Dr. Orla Pennywhistle, phone note / undated / Open record 8 / Enter this record by hand”",
    "why_it_matters": "Two cards for one record with different chips (undated vs Date to confirm) make the paralegal check whether they are two records. The manual-entry control is only in the second card and the confirm control only in the first.",
    "fix": "Exclude records shown in the Dates row from the records-without-entry panel (filter in app/frontend/manual.js), or fold the manual-entry control into the Dates row.",
    "acceptance_test": "With case_01 loaded, count of [data-record-id=r8] nodes across dates-to-confirm and records-without-entry equals 1, and that node has both a confirm control and a manual-entry control, or the two controls are shown once."},
   {"severity": "minor", "title": "Dates-to-confirm row shows no verbatim excerpt",
    "evidence": "artifacts/review-evidence/T-068/T-068-confirm-dump-commit-89a323a.json 1_row_text_before_confirm = “Record 8: Dr. Orla Pennywhistle, phone note / Date to confirm / Written as “04/05/2026”. Which date? / April 5, 2026 / May 4, 2026 / Open record 8”; the excerpt appears only in 2_record_modal_text",
    "why_it_matters": "Persona checklist item 3: I should see the record and its exact excerpt in one action. Today it is two actions (Open record, then read the modal), and the row gives no quote to compare against the date.",
    "fix": "Show the verbatim excerpt (record text quote) in the orphan row beneath the date question.",
    "acceptance_test": "Row innerText for r8 contains “Patient reports no new symptoms.” without opening the modal."},
   {"severity": "minor", "title": "AC 1 e2e assertion is text-only and passes on either branch",
    "evidence": "tests/e2e/test_input.py:29-32: expect(page.get_by_test_id(\"dates-to-confirm\")).to_contain_text(\"04/05/2026\"). It does not check the date-to-confirm-item testid, the confirm-date button, or Open record.",
    "why_it_matters": "The card's brief requires confirm-date and open-record actions on record 8 even with no undated entry. The test would still pass if the orphan branch were removed, because the undated-entry branch already prints 04/05/2026.",
    "fix": "Assert the orphan branch and both actions explicitly.",
    "acceptance_test": "In test_input.py: locate [data-testid=date-to-confirm-item][data-record-id=r8]; assert [data-testid=confirm-date][data-date=2026-04-05] is visible inside it and that clicking its Open record 8 button opens a modal containing “Patient reports no new symptoms.”"}
 ],
 "whats_right": [
   "Record 8 row shows the provider as written (Dr. Orla Pennywhistle, phone note), the raw date 04/05/2026 verbatim, both readings, and no date picked by the tool.",
   "Open record 8 shows the verbatim record block (Date, Source, Excerpt “Patient reports no new symptoms.”) in one click.",
   "The Dates panel only clears after the date is actually confirmed, and the confirmed date is shown in Records without an entry, so nothing is silently dropped."
 ],
 "questions_for_chris": [
   "Should the reviewed state be commit 89a323a or the working tree? The working tree has uncommitted backend and fixture changes that produce timeline entries; the commit alone produces none for case_01.",
   "After confirming an orphan date, should the system create the entry itself, or should the paralegal always enter it by hand (D-031)? The answer decides which fix for F1 is right."
 ]}
```
