# Subagent: Frontend: T-068 r3 undated accept UI (Frontend: T-068 r3 undated accept UI)

Source: `agent-afe8cd028d795bf48.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:59:17.970Z

You own board card T-068, round 3 (final; claimed by "frontend") in /Users/arsis/zlayt-pm-project. Read reviews/T-068-paralegal-r2.md (1 major, 3 minors) and D-041 in memory/ORCHESTRATOR_DECISIONS.md.

- **Major:** accepting record 8's undated entry before a date is picked put "date not stated" in the letter. In the UI:
  - disable Accept (single and batch) on an undated entry, with the visible reason "Confirm the date first" and a link to its Dates-to-confirm row;
  - batch accept skips undated entries and says how many it skipped;
  - handle a server 422 DATE_UNCONFIRMED in plain words.
  The server rule itself is card T-076, landing in parallel from a backend worker.
- **Minors:** fix the 3 minors if they're cheap.

Update the e2e tests and declare any new test ids in tests/e2e/conftest.py (tests/unit/test_e2e_contract.py must stay green). Commit with the pathspec rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-068 in_review --agent frontend`. Reply in 2 lines.

### User / tool · 2026-11-02T02:59:17.978Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:20.247Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-068-paralegal-r2.md | head -150; grep -n \"D-041\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60; python3 tools/board.py show T-068 | head -60; ls app/frontend tests/e2e"
}
````

### User / tool · 2026-11-02T02:59:20.409Z

**tool result**
````
# T-068 round 2 review — paralegal-reviewer (Maria Delgado persona)

Scope: commit 37a76a8 (app/frontend/manual.js, app/frontend/timeline.js, tests/e2e/test_input.py), served from a `git archive 37a76a8` snapshot on http://127.0.0.1:7875 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch DB). Sample case: evals/golden/case_01_date_formats.txt pasted. The worktree is not the reviewed state (it has uncommitted fixture and board changes); the snapshot is. The :7875 server is stopped.

## Round-1 findings, status on 37a76a8

- F1 (major) confirm on an orphan row removed it from view: **fixed.** On the orphan branch, confirming April 5, 2026 moves record 8 to "Records without an entry (1)" with "Date confirmed: April 5, 2026. Not on the timeline yet: enter this record by hand below" and a visible "Enter this record by hand". Still there after reload. Caveat in finding N4.
- Major 2 (committed build shows zero entries for case_01): **fixed.** case_01 at 37a76a8 shows 7 dated entries and 1 undated entry (record 8). The server log has 2 lines "llm call failed ... step=j1" from this session (see questions).
- Minor (record 8 listed twice before confirm): **fixed.** Before confirm, record 8 appears once at every step (A0, B0, B1, B3).
- Minor (no verbatim excerpt in the Dates row): **fixed.** Undated row shows "Patient reports no new symptoms." (entry-excerpt). Orphan row shows it as date-to-confirm-excerpt. Both match the raw record (evals/golden/case_01_date_formats.txt, Record 8 Excerpt line).
- Minor (AC 1 e2e text-only): **fixed.** Two branch-specific tests now exist and pass (see exercised).

## What I checked this round

Branch A, undated-entry branch, real case_01 with no request rewriting:
- Before confirm: the row reads "undated / Dr. Orla Pennywhistle, phone note / Patient reports no new symptoms. / Written as “04/05/2026”. Which date? / April 5, 2026 / May 4, 2026". The tool does not pick a date.
- Confirm April 5, 2026: the Dates panel clears, and the timeline gains a 2026-04-05 entry from Dr. Orla Pennywhistle, phone note, with the verbatim excerpt. Record 8 lands on the timeline, as required.
- Reload: the 2026-04-05 entry and the cleared Dates panel persist.

Branch B, orphan branch, forced by rewriting the GET case response to strip record 8 from entries:
- Before confirm: one row, "Record 8: Dr. Orla Pennywhistle, phone note / Date to confirm / Patient reports no new symptoms. / Written as “04/05/2026”", with two confirm buttons and "Open record 8". Record 8 appears once.
- Open record 8: the modal shows "Date: 04/05/2026 / Source: Dr. Orla Pennywhistle, phone note / Excerpt: "Patient reports no new symptoms."".
- Confirm April 5, 2026: the row leaves the Dates panel and the card appears once under Records without an entry, with the confirmed date, the "Date confirmed ... enter this record by hand" note, and "Enter this record by hand".
- "Enter this record by hand" opens a form listing "Patient reports no new symptoms." as the selectable sentence.
- Reload: the confirmed card persists.

Side probe (not in the brief, but on the row this card changed): accepting the undated row before picking a date. See N1.

## Findings

**N1 (major) Accepting the undated row before a date is picked puts a date-less line in the letter.**
Evidence: artifacts/review-evidence/T-068-r2/T-068-r2-accept-undated-dump.json, key `export_letter_text`, verbatim:
`TREATMENT CHRONOLOGY / date not stated — Dr. Orla Pennywhistle, phone note / Patient reports no new symptoms. / Source [Ex. __ / Bates __]: "Patient reports no new symptoms."`
Also `accept_before_date_pick` shows the panel reading "Needs review / Accepted". Screenshots: artifacts/review-evidence/T-068-r2/C-01-accept-before-date-pick.png and C-02-export-after-accept-before-date.png. Script: artifacts/review-evidence/T-068-paralegal-r2-probe-accept-undated.py.
Why it matters: the Dates panel says these records are "left off the timeline and the gap check until you pick the right date", and the tool offers no way to resolve them except confirm. The accept button bypasses that, and the letter then carries a claim with no date of service, which the adjuster will ask about first. The excerpt is verbatim and nothing is invented, so I do not rate this a blocker. R-IN-5 and R-RV-2 say the resolution path is confirm_date, but neither says whether accept is blocked while a date is unresolved. That is a product decision (question 1).
Fix: block accept (and the export line) on an undated entry whose date is still in Dates to confirm; or disable Accept until a reading is confirmed. Show the reason in one sentence.
Acceptance test: E2E on case_01, no confirm: the Accept control on the record-8 undated row is disabled (or the accept produces no letter line), and the export letter does not contain "date not stated".

**N2 (minor) The undated-entry row has no record number.**
Evidence: T-068-r2-probe-dump.json, checks A0_before_confirm, `dates_to_confirm_panel_text`: "undated / Dr. Orla Pennywhistle, phone note ... Open record". The orphan row on the same case reads "Record 8: Dr. Orla Pennywhistle, phone note ... Open record 8". The Open button has no number in the undated branch.
Why it matters: checklist item 3 wants the record number visible in one action. Here it takes the modal to find it.
Fix: use the same "Record N: <source>" head and "Open record N" label in entryRow for undated entries.
Acceptance test: with case_01 loaded, the Dates row for record 8 contains "Record 8:" and "Open record 8".

**N3 (minor) The card that receives a confirmed orphan drops the verbatim excerpt.**
Evidence: T-068-r2-probe-dump.json, checks B0_orphan_row (excerpt "Patient reports no new symptoms.") vs B1_missing_card_r8 (`card_text` has provider, date, note and buttons, no excerpt). Excerpt is only visible after "Enter this record by hand" or "Open record 8".
Why it matters: the paralegal confirms a date while looking at the quote, and then the quote disappears from the card she has to act on.
Fix: keep the excerpt in the moved card, under the confirmed-date note.
Acceptance test: in B1, the missing-entry card for r8 contains "Patient reports no new symptoms." without opening the modal.

**N4 (minor) The orphan branch is not reachable with the shipped fixtures; its evidence is a rewritten response.**
Evidence: the e2e test test_confirming_a_date_with_no_entry_keeps_the_record_visible rewrites GET /api/cases/<token> to strip record 8 (tests/e2e/test_input.py, its route handler). The team handoff says the same ("orphan can't occur with the fixed fixtures, hence the forced test"). My branch B is also the rewritten state.
Why it matters: the orphan path is the one that protects the paralegal if a model call drops a record. As it stands, no real run shows it, so its behaviour is only proven against a synthetic response.
Fix: add a curated fixture or backend test in which a record has a date to confirm and no model entry, and run the orphan E2E without route rewriting.
Acceptance test: E2E with FIXTURE_SET=curated on that fixture, no page.route; the record moves to Records without an entry and the confirm, excerpt and manual-entry assertions pass.

## Test runs

- `E2E_BASE_URL=http://127.0.0.1:7875 .venv/bin/python -m pytest tests/e2e -k "date or confirm or ambiguous or dates" -v -rs` (run from the snapshot): test_ambiguous_date_goes_to_dates_to_confirm PASSED; test_confirming_a_date_with_no_entry_keeps_the_record_visible PASSED; test_nine_entries_in_date_order PASSED; test_record_7_dated_by_header_not_body PASSED; test_date_and_provider_not_editable PASSED; test_stepping_updates_the_highlight SKIPPED (T-046 stretch, not built). Result: 5 passed, 1 skipped.
- Full `tests/e2e` on :7875: 68 passed, 3 skipped, 78.9 s.

## Verdict

changes: 0 blockers, 1 major (N1), 3 minors (N2 to N4). Round-1 items all resolved. verify_quickly is 3, below the ship bar of 4: the chronology and the record's excerpt are now verifiable in one click, but the undated row has no record number, the moved card loses its quote, and accept can put a date-less line into the letter.

## Questions for Chris

1. Should Accept on an undated entry be blocked until its date is confirmed (N1), or is a date-less letter line acceptable? R-IN-5 and R-RV-2 do not say.
2. Queue order: a pending entry sorts above dated verified entries (2026-04-05 appears above 2026-02-03 after confirm). Checklist item 5 asks for date order, item 16 asks for review-first. Which one wins in the queue? Export order is separate.
3. Outside my lens: the server log has 2 lines "llm call failed ... step=j1" during this session's three case_01 analyses (log: artifacts/review-evidence/T-068-r2/ is not the log; scratch log t068r2-server.log). Backend/qa should say whether the judge rung falls back on the curated set.

```json
{"card": "T-068", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 37a76a8 (app/frontend/manual.js, app/frontend/timeline.js, tests/e2e/test_input.py) served from a git archive snapshot on http://127.0.0.1:7875 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local); sample case evals/golden/case_01_date_formats.txt pasted",
 "exercised": [
   "read personas/paralegal.md, docs/RUNBOOK.md, board show T-068, reviews/T-068-paralegal.md (round 1), memory t068-dates-to-confirm-patterns.md, git show --stat 37a76a8, app/frontend/timeline.js and manual.js confirm paths, tests/e2e/test_input.py",
   "git archive 37a76a8 into scratch; started app on :7875 from snapshot (curl / 200, /api/health 200); stopped it afterwards",
   "Playwright branch A (real case_01): analyze, read Dates row before confirm, confirm 2026-04-05, read timeline entries and excerpts, reload; artifacts/review-evidence/T-068-r2/A-01..A-03 png; dump T-068-r2-probe-dump.json",
   "Playwright branch B (orphan via route rewrite of GET case): row text and excerpt, Open record 8 modal, confirm, Records without an entry card, manual-entry form, reload; B-01..B-05 png; same dump",
   "Playwright side probe: accept undated row before date pick, then Export; artifacts/review-evidence/T-068-r2/T-068-r2-accept-undated-dump.json, C-01, C-02 png",
   "pytest tests/e2e -k date/confirm/ambiguous (5 passed, 1 skipped) and full tests/e2e (68 passed, 3 skipped) against :7875",
   "read server log t068r2-server.log (2 lines llm call failed step=j1)",
   "viewed screenshots B-03-orphan-after-confirm.png and C-02-export-after-accept-before-date.png"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "round1_f1_orphan_confirm_fixed": 5, "record_8_listed_once": 5, "excerpt_verbatim_in_row": 5, "undated_accept_gate": 2, "record_number_on_every_row": 3},
 "findings": [
   {"severity": "major", "title": "Accepting the undated row before a date is picked puts a date-less line in the letter",
    "evidence": "artifacts/review-evidence/T-068-r2/T-068-r2-accept-undated-dump.json export_letter_text: \"TREATMENT CHRONOLOGY / date not stated — Dr. Orla Pennywhistle, phone note / Patient reports no new symptoms. / Source [Ex. __ / Bates __]: ...\"; accept_before_date_pick panel reads \"Needs review / Accepted\"; screenshots artifacts/review-evidence/T-068-r2/C-01-accept-before-date-pick.png and C-02-export-after-accept-before-date.png; script artifacts/review-evidence/T-068-paralegal-r2-probe-accept-undated.py",
    "why_it_matters": "The Dates panel says these records are left off the timeline and the gap check until a date is picked, and confirm is the only resolution the tool offers. Accept bypasses that, so an undated claim reaches the demand letter and the adjuster's first question is the date. Excerpt is verbatim and nothing is invented, so not a blocker; the spec does not say whether accept is gated.",
    "fix": "Disable Accept (or block the letter line) on an entry whose date is still in Dates to confirm; show one sentence giving the reason.",
    "acceptance_test": "E2E on case_01 with no confirm: Accept on the record-8 undated row is disabled or produces no letter line, and the export letter does not contain \"date not stated\"."},
   {"severity": "minor", "title": "Undated-entry row has no record number and its Open button has no number",
    "evidence": "artifacts/review-evidence/T-068-r2/T-068-r2-probe-dump.json checks.A0_before_confirm.dates_to_confirm_panel_text: \"undated / Dr. Orla Pennywhistle, phone note ... Open record\"; orphan row on the same case: \"Record 8: Dr. Orla Pennywhistle, phone note ... Open record 8\"",
    "why_it_matters": "Checklist item 3: the record number should be visible in one action. Here the paralegal must open the modal to find it.",
    "fix": "Use the same \"Record N: <source>\" head and \"Open record N\" label for undated entries in entryRow.",
    "acceptance_test": "With case_01 loaded, the Dates row for record 8 contains \"Record 8:\" and \"Open record 8\"."},
   {"severity": "minor", "title": "Card that receives a confirmed orphan date drops the verbatim excerpt",
    "evidence": "artifacts/review-evidence/T-068-r2/T-068-r2-probe-dump.json checks.B0_orphan_row.excerpt = [\"Patient reports no new symptoms.\"] vs checks.B1_missing_card_r8.card_text (no excerpt); screenshot artifacts/review-evidence/T-068-r2/B-03-orphan-after-confirm.png",
    "why_it_matters": "The paralegal confirms the date while reading the quote, then the quote is gone from the card she acts on.",
    "fix": "Keep the excerpt in the moved card, under the confirmed-date note.",
    "acceptance_test": "In the B1 state, the missing-entry card for r8 contains \"Patient reports no new symptoms.\" without opening the modal."},
   {"severity": "minor", "title": "Orphan branch is unreachable with the shipped fixtures; evidence is a rewritten response",
    "evidence": "tests/e2e/test_input.py test_confirming_a_date_with_no_entry_keeps_the_record_visible (page.route rewrite of GET /api/cases/<token>); team handoff on T-068 round 2: \"orphan can't occur with the fixed fixtures, hence the forced test\"",
    "why_it_matters": "The orphan path is the protection if a model call drops a record. No real run shows it, so it is only proven against a synthetic response.",
    "fix": "Add a curated fixture or backend test where a record has a date to confirm and no model entry; run the orphan E2E without route rewriting.",
    "acceptance_test": "E2E with FIXTURE_SET=curated on that fixture, no page.route: the record moves to Records without an entry and the confirm, excerpt and manual-entry assertions pass."}
 ],
 "whats_right": [
   "Confirming an orphan date no longer removes the record: it moves to Records without an entry with 'Date confirmed ... enter this record by hand' and a manual-entry control, and survives reload (B1, B3).",
   "Record 8 is listed once at every step on both branches, and the Dates row shows the verbatim excerpt \"Patient reports no new symptoms.\" matching the raw record.",
   "On the real case_01 the undated branch lands the record on the timeline after confirm (2026-04-05 entry with its excerpt), and the state persists after reload (A1, A2)."],
 "questions_for_chris": [
   "Should Accept on an undated entry be blocked until its date is confirmed (N1), or is a date-less letter line acceptable? R-IN-5 and R-RV-2 do not say.",
   "Queue order: a pending entry sorts above dated verified entries after confirm (2026-04-05 above 2026-02-03). Checklist item 5 asks for date order and item 16 for review-first. Which wins in the queue?",
   "Outside my lens: the server log has 2 'llm call failed ... step=j1' lines during this session's case_01 analyses. Backend/qa should say whether the judge rung falls back on the curated set."]}
```
49:| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
---
id: "T-068"
title: "Dates to confirm empty for case_01 record 8"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:40:24Z"
updated_at: "2026-11-02T02:59:07Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T02:59:07Z"
rounds: 2
commits: ["89a323a", "37a76a8"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-068-paralegal.md", "at": "2026-11-02T02:49:28Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-068-paralegal-r2.md", "at": "2026-11-02T02:59:07Z"}
ac:
  - {"n": 1, "text": "case_01 record 8 date-to-confirm item appears under Dates to confirm; qa strict xfail in T-045 suite flips to pass", "done": true, "evidence": "tests/e2e/test_input.py::test_ambiguous_date_goes_to_dates_to_confirm (undated branch, asserts excerpt, 2 confirm buttons, once-only, lands on timeline) and ::test_confirming_a_date_with_no_entry_keeps_the_record_visible (orphan branch); full e2e 68 passed 3 skipped on :7873"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:40:38Z frontend: claimed
- 2026-11-02T02:44:11Z frontend: Cause: frontend. API sends dates_to_confirm [{record_id r8, raw 04/05/2026, candidates}] but timeline.js rendered that panel only from undated_entries (curated fixture gives case_01 no entries). Fixed: render orphan dates_to_confirm rows; also reads contract field raw. Unrelated: tests/e2e/test_edit.py::test_notes_list_edited_item_with_both_texts fails (backend EDITED ITEMS, xfail removed uncommitted by someone else).
- 2026-11-02T02:44:12Z frontend: AC 1 checked: tests/e2e/test_input.py::test_ambiguous_date_goes_to_dates_to_confirm passes without xfail; full e2e 63 passed on :7871 fixture/curated
- 2026-11-02T02:44:12Z frontend: moved in_progress -> in_review
- 2026-11-02T02:44:21Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T02:49:28Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-068-paralegal.md; round 1; findings:
    - [major] Confirming the date of an orphan Dates-to-confirm row does not put the record on the timeline — fix: Either create the timeline entry from the confirmed record (backend), or keep the row after confirm with text such as “Date confirmed April 5, 2026. Not yet on the timeline: enter this record by hand” and a btn-manual-entry control. Correct the panel copy to match.
    - [major] Committed 89a323a shows no timeline entries for case_01 under the curated fixture set — fix: Owner backend/qa: make the committed backend and the committed fixture set agree (commit the missing fixtures and the backend changes they were recorded against), then re-run the curated case_01 at the commit being reviewed.
    - [minor] Record 8 is listed twice before any confirm (Dates row and Records without an entry) — fix: Exclude records shown in the Dates row from the records-without-entry panel (filter in app/frontend/manual.js), or fold the manual-entry control into the Dates row.
    - [minor] Dates-to-confirm row shows no verbatim excerpt — fix: Show the verbatim excerpt (record text quote) in the orphan row beneath the date question.
    - [minor] AC 1 e2e assertion is text-only and passes on either branch — fix: Assert the orphan branch and both actions explicitly.
- 2026-11-02T02:49:36Z frontend: claimed
- 2026-11-02T02:49:36Z orchestrator: Round 2 waits on backend-1 committing the fixture fallback (major 2). Then frontend: an orphan Dates-to-confirm row, once confirmed, must land the record on the timeline (or under Records without an entry with the manual-entry path), show the verbatim excerpt, avoid listing it twice, and make the AC1 e2e assertion branch-specific.
- 2026-11-02T02:49:36Z orchestrator: assigned: frontend
- 2026-11-02T02:49:44Z backend: Commit d7dbfde: fixture backend now tries FIXTURE_SET (curated) first, then the recorded tests/fixtures/llm set. Fixes case_01 (and case_02..09, library) showing zero entries on the curated live app: verified case_01 -> 7 dated + 1 undated entries (golden has 8 records), 0 errors, with and without FIXTURE_SET=curated. Restart the app (tools/serve_app.sh) to pick it up.
- 2026-11-02T02:53:28Z frontend: Round 2: case_01 on own instance :7873 (fixture/curated) = 7 dated + 1 undated entry, r8 via undated branch. Orphan branch (no entry) forced in e2e by rewriting the GET case response. API: no change needed; optional backend nicety: confirm_date could create/draft an entry for a record with none (today entry:null, record just gets date_status confirmed). Frontend path: orphan row -> confirm -> Records without an entry with 'Date confirmed ... enter by hand' + btn-manual-entry.
- 2026-11-02T02:53:28Z frontend: AC 1 checked: tests/e2e/test_input.py::test_ambiguous_date_goes_to_dates_to_confirm (undated branch, asserts excerpt, 2 confirm buttons, once-only, lands on timeline) and ::test_confirming_a_date_with_no_entry_keeps_the_record_visible (orphan branch); full e2e 68 passed 3 skipped on :7873
- 2026-11-02T02:53:28Z frontend: moved in_progress -> in_review
- 2026-11-02T02:53:31Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T02:58:27Z frontend: Declared T-068 test ids and attrs in tests/e2e/conftest.py docstring (date-to-confirm-item, date-to-confirm-excerpt, confirm-date, missing-entry, missing-date-confirmed, btn-manual-entry; attrs data-testid, data-record-id, data-date). tests/unit/test_e2e_contract.py green (3 passed). Commit b6f3755 (test(e2e): declare T-068 test ids).
- 2026-11-02T02:59:07Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-068-paralegal-r2.md; round 2; findings:
    - [major] Accepting the undated row before a date is picked puts a date-less line in the letter — fix: Disable Accept (or block the letter line) on an entry whose date is still in Dates to confirm; show one sentence giving the reason.
    - [minor] Undated-entry row has no record number and its Open button has no number — fix: Use the same "Record N: <source>" head and "Open record N" label for undated entries in entryRow.
    - [minor] Card that receives a confirmed orphan date drops the verbatim excerpt — fix: Keep the excerpt in the moved card, under the confirmed-date note.
    - [minor] Orphan branch is unreachable with the shipped fixtures; evidence is a rewritten response — fix: Add a curated fixture or backend test where a record has a date to confirm and no model entry; run the orphan E2E without route rewriting.
- 2026-11-02T02:59:07Z frontend: claimed

## Handoff
What changed: M1 confirming an orphan Dates row moves it to Records without an entry with 'Date confirmed <date>. Not on the timeline yet: enter this record by hand' + manual-entry control (never removed); copy in row says so. Minors: r8 listed once (manual.js skips confirmable dates_to_confirm records; non-confirmable no-date orphans listed once there), verbatim excerpt in Dates row (date-to-confirm-excerpt), e2e now branch-specific (undated branch real fixture; orphan branch via route rewrite). Verified: case_01 = 7 dated + 1 undated on :7873; e2e 68 pass. Left: nothing; optional backend: confirm_date could draft an entry when none exists. Surprise: orphan can't occur with the fixed fixtures, hence the forced test.

app/frontend:
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
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
source.js
state.js
styles.css
switcher.js
timeline.js

tests/e2e:
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
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_timeline.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:22.228Z

**tool call — Bash**
````
{
 "command": "wc -l app/frontend/timeline.js app/frontend/manual.js app/frontend/review.js app/frontend/batch.js; grep -n \"undated\\|accept\\|Accept\" app/frontend/timeline.js | head -80; python3 tools/board.py show T-076 | head -40; git log --oneline | head -5; git status --short | head -20"
}
````

### User / tool · 2026-11-02T02:59:22.405Z

**tool result**
````
     150 app/frontend/timeline.js
     102 app/frontend/manual.js
     280 app/frontend/review.js
      62 app/frontend/batch.js
     594 total
7:  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
21:        el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
50:    if (!c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length)) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
66:    c.undated_entries.forEach((e) => {
69:      const row = entryRow(e, c); row.classList.add("undated");
81:      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
112:    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
113:    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
135:    const shown = c.entries.concat(c.undated_entries), nNeeds = shown.filter((e) => e.state === "needs_review").length, nVer = shown.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
141:        el("span", { class: "muted", "data-testid": "review-counts" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"} · ${nNeeds} needs review · ${nVer} verified` + (c.undated_entries.length ? ` (${c.undated_entries.length} in Dates to confirm below)` : "")),
---
id: "T-076"
title: "Server: block accept of undated entries until date confirmed (D-041)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:59:07Z"
updated_at: "2026-11-02T02:59:09Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:59:09Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "POST accept (single and batch) on an entry with no confirmed date returns 422 DATE_UNCONFIRMED and changes nothing; after confirm_date it accepts; export treatment section never contains 'date not stated'; unit tests; api.md updated", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:59:09Z backend: claimed

## Handoff (filled when moving to in_review)

7763998 docs: D-041 undated entries need a confirmed date before accept (T-068 r2)
b6f3755 test(e2e): declare T-068 test ids
43fc69e chore(backend): re-record sample narrative fixtures against current summaries; eval report
b9d3ead chore(backend): narrative fixtures for sample and case_01-09 (curated + recorded), make_curated drafts the narrative; A-109
f6fa2dd fix(backend): credibility wording is a negation-aware family match; neutral template (T-067 r2, D-038)
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/backend/ingest.py
 M app/backend/pipeline.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:23.618Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat timeline.js manual.js batch.js; grep -n \"accept\" review.js api.js | head -50"
}
````

### User / tool · 2026-11-02T02:59:23.808Z

**tool result**
````
/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
   T-043 plugs in through ZL.registerRowActions(fn(entry,rowEl)) and ZL.registerPanel(fn(case, mountEl)). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological

  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
  const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled" };
  const reasonText = (r) => REASON[r] || String(r).toLowerCase().replace(/_/g, " ");

  function stateChip(e) {
    return el("span", { class: "chip st-" + e.state, "data-testid": "entry-state" }, STATE_LABEL[e.state] || e.state);
  }
  function entryRow(e, c) {
    const rec = c.records.find((r) => r.id === e.record_ids[0]);
    const row = el("article", { class: "entry st-" + e.state, "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    row.append(...[
      el("div", { class: "entry-head" },
        el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, e.provider),
        stateChip(e),
        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag" }, "AI-drafted") : null),
      e.edited ? el("p", { class: "muted small", "data-testid": "edited-note" }, "Edited by you. Original: " + e.edited.original_summary) : null,
      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt),
      e.duplicate_note ? el("p", { class: "muted small" }, e.duplicate_note) : null,
      e.state === "needs_review" && e.reasons.length ? el("p", { class: "reason", "data-testid": "entry-reasons" }, "Check: " + e.reasons.map(reasonText).join("; ")) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
        el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, "Open record"))].filter(Boolean));
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    return row;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => ZL.firstRank(e.id, e.state);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
  }
  // The record's own quoted text (verbatim, as in the record body), shown so the date can be judged next to what the record says.
  function recordExcerpt(rec) {
    const m = /(?:^|\n)Excerpt:\s*"?([\s\S]*?)"?\s*$/.exec(rec.text || "");
    return m ? m[1].trim() : "";
  }
  function datesToConfirm(c) {
    const box = el("section", { class: "group", "data-testid": "dates-to-confirm" }, el("h2", {}, "Dates to confirm"));
    if (!c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length)) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    const confirmBar = (d) => {
      const raw = d.raw || d.date_raw || "";
      const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${raw}”. Which date?`));
      d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn small", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
        try {
          await ZL.api.confirmDate(ZL.state.get().token, d.record_id, cand);
          ZL.state.set({ case: await ZL.api.getCase(ZL.state.get().token) });
          const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + d.record_id + '"]');
          if (left) { const rec = ZL.state.get().case.records.find((r) => r.id === d.record_id); if (ZL.rv && ZL.rv.say) ZL.rv.say(`Date confirmed: ${ZL.fmtDate(cand)}. Record ${rec ? rec.seq : ""} has no entry yet; it is listed under Records without an entry.`); left.scrollIntoView({ block: "center" }); }
        } catch (er) { alert(er.message); }
      } }, ZL.fmtDate(cand))));
      return bar;
    };
    const shown = {};
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d) shown[d.record_id] = true;
      if (d && d.candidates.length) row.insertBefore(confirmBar(d), row.querySelector(".row-actions"));
      else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
    // A record with an ambiguous date but no entry at all (no model entry for it): still list it here so the date can be confirmed.
    // Once confirmed it is not removed: it moves to "Records without an entry" (manual.js) with a note and the by-hand path.
    // A record with no readable date and no entry has no date to confirm; it is listed once, under "Records without an entry".
    c.dates_to_confirm.filter((d) => !shown[d.record_id] && d.candidates.length).forEach((d) => {
      const rec = c.records.find((r) => r.id === d.record_id);
      const quote = rec ? recordExcerpt(rec) : "";
      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip" }, "Date to confirm")),
        quote ? el("blockquote", { class: "excerpt", "data-testid": "date-to-confirm-excerpt" }, quote) : null);
      row.append(confirmBar(d));
      row.append(el("p", { class: "muted small", "data-testid": "date-to-confirm-note" }, "No entry was drafted for this record. After you pick the date it is listed under Records without an entry, where you enter it by hand."));
      if (rec) row.append(el("div", { class: "row-actions" }, el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource([{ record_id: rec.id, start: null, end: null }], `Record ${rec.seq}: ${rec.source_label}`) }, `Open record ${rec.seq}`)));
      box.append(row);
    });
    return box;
  }
  function tray(c) {
    const box = el("section", { class: "group tray", "data-testid": "rejected-tray" }, el("h2", {}, `Could not verify (${c.tray.length})`));
    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here. Every record produced an entry that passed the code checks.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip st-rejected" }, "Could not verify")),
        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
        el("p", { class: "summary" }, t.why),
        t.attempt ? el("p", { class: "muted small" }, "The model's attempt (not used): " + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
        el("div", { class: "row-actions" }, recs.map((r) => el("button", { type: "button", class: "btn small", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
      box.append(item);
    });
    return box;
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    try {
      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
      clear(body);
      body.append(...[
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
        el("dl", { class: "kv", "data-testid": "why-ladder" },
          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openWhy = openWhy;

  ZL.renderReview = function (s) {
    const c = s.case, mount = ZL.$("#review-body"); clear(mount);
    if (!c || c.status !== "ready") return;
    const shown = c.entries.concat(c.undated_entries), nNeeds = shown.filter((e) => e.state === "needs_review").length, nVer = shown.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
    wrap.append(
      el("div", { class: "toolbar" },
        el("h2", {}, "Timeline"),
        el("button", { type: "button", class: "btn primary", "data-testid": "btn-export", onclick: () => ZL.openExport() }, "Export"),
        el("span", { class: "muted", "data-testid": "review-counts" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"} · ${nNeeds} needs review · ${nVer} verified` + (c.undated_entries.length ? ` (${c.undated_entries.length} in Dates to confirm below)` : "")),
        el("label", { class: "muted small" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      el("div", { class: "timeline", "data-testid": "queue" }, sortedEntries(c).map((e) => entryRow(e, c))),
      datesToConfirm(c), tray(c));
    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
    ZL.hooks.panels.forEach((fn) => fn(c, side));
  };
})();
/* Manual entry for a record in the could-not-verify tray (T-056 B1, D-031). The paralegal picks whole sentences of that record
   (the excerpt is cut from the record text by code, so it is verbatim) and writes her own summary: POST /records/{rid}/entry.
   Server refusals (422) and the token check (409 needs_confirm, "keep my wording") are shown in plain words. Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  const draft = {};   // tray item id -> {open, picked:[sentence index], summary}
  const REASON = {
    EXCERPT_NOT_WHOLE_SENTENCE: "The quote must start and end at a sentence boundary.",
    EXCERPT_NOT_VERBATIM: "The quote is not word for word in the record.",
    EXCERPT_OMITS_QUALIFIER: "A hedge sentence in the record qualifies your quote; include it.",
  };

  // Quotable sentences of a record: header lines are not part of any excerpt, and the opening `Excerpt: "` / closing quote are not quoted text.
  function quotable(rec) {
    const out = [];
    (rec.sentences || []).forEach((s) => {
      let a = s.start, b = s.end, txt = rec.text.slice(a - rec.char_start, b - rec.char_start);
      if (/^(===|Date:|Source:)/.test(txt)) return;
      const m = /^Excerpt:\s*"?/.exec(txt); if (m) { a += m[0].length; txt = txt.slice(m[0].length); }
      if (/"\s*$/.test(txt) && !txt.slice(0, -1).includes('"')) { const k = txt.length - txt.replace(/"\s*$/, "").length; b -= k; txt = txt.slice(0, txt.length - k); }
      if (txt.trim()) out.push({ text: txt, start: a, end: b });
    });
    return out;
  }

  function control(c, t, rec) {
    const d = draft[t.id] || (draft[t.id] = { open: false, picked: [], summary: "" });
    const sents = quotable(rec);
    const msg = el("p", { class: "rv-error", role: "alert", "data-testid": "manual-error" });
    const confirmBox = el("div", { class: "rv-confirm", hidden: true });
    const sum = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: "summary", "data-testid": "manual-summary", "aria-label": "Your summary, written from the quote" });
    sum.value = d.summary; sum.addEventListener("input", () => { d.summary = sum.value; });
    const boxes = sents.map((s, i) => {
      const cb = el("input", { type: "checkbox", name: "sent", value: String(i), checked: d.picked.includes(i) || null, onchange: () => { d.picked = boxes.filter((b) => b.input.checked).map((b) => +b.input.value); } });
      return { input: cb, label: el("label", { class: "rv-radio" }, cb, s.text) };
    });
    async function submit(confirmWarnings) {
      msg.textContent = ""; confirmBox.hidden = true;
      const idx = d.picked.slice().sort((a, b) => a - b);
      if (!idx.length) { msg.textContent = "Pick at least one sentence to quote."; return; }
      if (idx.some((v, k) => k && v !== idx[k - 1] + 1)) { msg.textContent = "Pick sentences that sit next to each other in the record."; return; }
      if (!d.summary.trim()) { msg.textContent = "Write your summary of the quote."; return; }
      const a = sents[idx[0]], b = sents[idx[idx.length - 1]];
      const body = { summary: d.summary.trim(), excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
      if (confirmWarnings) body.confirm_warnings = true;
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/records/" + encodeURIComponent(rec.id) + "/entry", body);
      if (r.status === 200 || r.status === 201) {
        delete draft[t.id]; ZL.state.set({ case: await ZL.api.getCase(c.token) }); RV.say("Entry added for record " + rec.seq + ". It is not reviewed yet."); return;
      }
      const err = (r.body && r.body.error) || {}, detail = err.detail || {};
      if (r.status === 409 && err.code === "needs_confirm") {
        clear(confirmBox); confirmBox.hidden = false;
        confirmBox.append(el("p", {}, err.message || "This summary adds something that is not in the quote."),
          el("ul", { "data-testid": "warning-list", class: "rv-warnings" }, ((detail.warnings) || []).map((w) => el("li", {}, w.message))),
          el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => submit(true) }, "Keep my wording"),
            el("button", { type: "button", class: "rv-btn rv-secondary", onclick: () => { confirmBox.hidden = true; sum.focus(); } }, "Go back and change it")));
        RV.say("This summary adds something that is not in the quote.", true); return;
      }
      const why = (detail.reasons || []).map((x) => REASON[x]).filter(Boolean);
      msg.textContent = (err.message || "That entry was refused.") + (why.length ? " " + why.join(" ") : "");
      RV.say(msg.textContent, true);
    }
    const form = el("form", { class: "rv-edit rv-manual-form", hidden: !d.open, "data-testid": "manual-form", onsubmit: (ev) => { ev.preventDefault(); submit(false); } },
      el("fieldset", { class: "rv-fieldset" }, el("legend", {}, "Pick the sentences to quote from Record " + rec.seq + " (whole sentences, next to each other)"),
        sents.length ? boxes.map((b) => b.label) : el("p", { class: "rv-empty" }, "This record has no sentences to pick from.")),
      el("label", { class: "rv-label" }, "Your summary (written from the quote; numbers and dates must be in the quote)", sum),
      el("div", { class: "rv-actions" }, el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-save-manual" }, "Add entry"),
        el("button", { type: "button", class: "rv-btn rv-secondary", onclick: () => toggle(false) }, "Cancel")), msg, confirmBox);
    const open = el("button", { type: "button", class: "btn small", "data-testid": "btn-manual-entry", "aria-expanded": String(d.open), onclick: () => toggle(!d.open) }, "Enter this record by hand");
    function toggle(v) { d.open = v; form.hidden = !v; open.setAttribute("aria-expanded", String(v)); if (v) { const f = form.querySelector("input,textarea"); if (f) f.focus(); } else open.focus(); }
    form.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.stopPropagation(); toggle(false); } });
    return el("div", { class: "rv-manual", "data-testid": "manual-entry", "data-record-id": rec.id }, el("div", { class: "rv-actions" }, open), form);
  }

  RV.registerPanel("manual", (root, c) => {
    ZL.clear(root); root.className = "rv-batchhost"; root.removeAttribute("data-testid");
    const wrap = root.closest('[data-testid="timeline"]'); if (!wrap) return;
    const inTray = {};
    wrap.querySelectorAll('[data-testid="tray-item"]').forEach((node) => {
      const t = (c.tray || []).find((x) => x.id === node.getAttribute("data-item-id"));
      const rec = t && (t.record_ids || []).length === 1 ? (c.records || []).find((r) => r.id === t.record_ids[0]) : null;
      if (!rec || (t.kind && t.kind !== "entry")) return;
      inTray[rec.id] = true;
      if (!node.querySelector(":scope > .rv-manual")) node.append(control(c, t, rec));
    });
    // Records that produced no entry and are not in the tray (for example the model call failed): same control.
    const has = {}; (c.entries || []).concat(c.undated_entries || [], c.tray || []).forEach((e) => (e.record_ids || []).forEach((id) => { has[id] = true; }));
    const toConfirm = {}; (c.dates_to_confirm || []).forEach((d) => { if ((d.candidates || []).length) toConfirm[d.record_id] = true; });  // listed once, under Dates to confirm
    const missing = (c.records || []).filter((r) => !has[r.id] && !inTray[r.id] && !toConfirm[r.id] && !r.duplicate_of);
    if (!missing.length || c.status !== "ready") return;
    root.className = "rv-panel"; root.setAttribute("data-testid", "records-without-entry");
    root.append(el("h2", {}, "Records without an entry (" + missing.length + ")"),
      el("p", { class: "rv-help" }, "These records did not produce an entry, so they are not in the timeline or the letter. Read the record, quote the sentences yourself and write the summary."));
    missing.forEach((r) => {
      const card = el("article", { class: "rv-card", "data-testid": "missing-entry", "data-record-id": r.id },
        el("div", { class: "rv-head" }, el("h3", { class: "rv-title" }, "Record " + r.seq + ": " + r.source_label), el("span", { class: "rv-chip" }, r.date_iso ? ZL.fmtDate(r.date_iso) : "undated")),
        r.date_status === "confirmed" ? el("p", { class: "rv-help", "data-testid": "missing-date-confirmed" }, `Date confirmed: ${ZL.fmtDate(r.date_iso)}. Not on the timeline yet: enter this record by hand below.`) : null,
        el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn rv-secondary", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], "Record " + r.seq + ": " + r.source_label) }, "Open record " + r.seq)));
      card.append(control(c, { id: "rec:" + r.id }, r)); root.append(card);
    });
  });
})();
/* Batch accept for verified entries only (T-055, D-031). Button + Shift+A; the server enforces "verified pending entries only" (422 otherwise).
   Never touches amounts or flags. Undo resets exactly the entries this batch accepted. Any error (including 404/405) shows a plain message and accepts nothing: no per-item fallback, so the server's verified-only check cannot be bypassed (T-065). */
(function () {
  const ZL = window.ZL, RV = ZL.rv, el = ZL.el;
  let last = null;      // {token, ids} of the most recent batch, for Undo
  let busy = false;
  const eligible = (c) => (c.entries || []).filter((e) => e.state === "verified" && (e.review_status || "pending") === "pending");

  async function refresh(token) { ZL.state.set({ case: await ZL.api.getCase(token) }); }

  async function acceptAll() {
    const c = RV.caseNow(); if (!c || busy) return;
    const ids = eligible(c).map((e) => e.id); if (!ids.length) return;
    busy = true;
    try {
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "accept", item_ids: ids });
      if (r.status >= 400) {
        const plain = (r.status === 404 || r.status === 405) ? "Accept all could not run on this server, so nothing was accepted. Accept entries one at a time instead." : null;
        RV.say(plain || RV.errMsg(r, "The batch was refused; nothing was accepted."), true); return;
      }
      last = { token: c.token, ids };
      await refresh(c.token);
      RV.say("Accepted " + ids.length + " verified " + (ids.length === 1 ? "entry" : "entries") + ". Undo is available.");
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
    const n = eligible(c).length;
    const undoable = last && last.token === c.token && last.ids.some((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
    return el("div", { class: "rv-batchbar", "data-testid": "batch-bar" },
      el("button", { type: "button", class: "rv-btn", "data-testid": "btn-accept-verified", disabled: n === 0, onclick: acceptAll }, "Accept all verified entries (" + n + ")"),
      undoable ? el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-undo-batch", onclick: undo }, "Undo last batch (" + last.ids.length + ")") : null,
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
review.js:44:  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
review.js:140:  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
review.js:152:      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
review.js:176:    bar.append(btn("accept", noted ? "Accept as noted" : "Accept", "btn-accept", { "aria-pressed": String(st === "accepted"), onclick: () => RV.act(id, { action: "accept" }, { focus: "accept" }) }));
review.js:223:    "j next, k previous, a accept, e edit, d dismiss, r reset, o open the record, Shift+A accept all verified entries. Tab reaches every button.");
review.js:249:    if (key === "a") RV.act(id, { action: "accept" }, { advance: true, scope });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:26.085Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 100,280p review.js; grep -n \"errMsg\" review.js | head -3"
}
````

### User / tool · 2026-11-02T02:59:26.165Z

**tool result**
````
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

  // ---- errors and the "keep my wording" confirmation (R-RV-3)
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }
  function showConfirm(id, err, body) {
    const s = slot(id, "rv-confirm"); if (!s) return;
    ZL.clear(s); s.hidden = false;
    const warns = (err.detail && err.detail.warnings) || [{ message: err.message }];
    s.append(el("p", { class: "rv-confirm-msg" }, err.message || "This edit adds something that is not in the quote."),
      el("ul", { "data-testid": "warning-list", class: "rv-warnings" }, warns.map((w) => el("li", {}, w.message))),
      el("div", { class: "rv-actions" },
        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => RV.act(id, Object.assign({}, body, { confirm_warnings: true }), { focus: "edit" }) }, "Keep my wording"),
        el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-cancel-confirm", onclick: () => { s.hidden = true; ZL.clear(s); } }, "Go back and change it")));
    RV.say("This edit adds something that is not in the quote. Choose keep my wording or go back.", true);
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
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
      if (e && e.code === "needs_confirm") showConfirm(id, e, body);
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
    bar.append(btn("accept", noted ? "Accept as noted" : "Accept", "btn-accept", { "aria-pressed": String(st === "accepted"), onclick: () => RV.act(id, { action: "accept" }, { focus: "accept" }) }));
    let form;
    if (canEdit) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true) }));
    bar.append(btn("dismiss", "Dismiss", "btn-dismiss", { "aria-pressed": String(st === "dismissed"), onclick: () => RV.act(id, { action: "dismiss" }, { focus: "dismiss" }) }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { class: "rv-btn rv-secondary", onclick: () => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Reset", "btn-reset", { class: "rv-btn rv-secondary", onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { class: "rv-btn rv-secondary", onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);

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
    root.append(el("div", { class: "rv-error", role: "alert" }), el("div", { class: "rv-confirm", hidden: true }));
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
41:  RV.errMsg = (r, fallback) => (r && r.body && r.body.error && r.body.error.message) || fallback || "That did not work.";
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:35.468Z

**tool call — Bash**
````
{
 "command": "sed -n 1,100p app/frontend/review.js; grep -n \"review\\b\\|review:\\|code\" app/frontend/api.js | head -20; grep -n \"def test_\\|^import\\|^from\" tests/e2e/test_input.py | head -40; sed -n 1,60p tests/e2e/conftest.py; grep -rn \"DATE_UNCONFIRMED\" memory/contracts/api.md app/backend | head"
}
````

### User / tool · 2026-11-02T02:59:35.585Z

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
10:    constructor(status, err) { super((err && err.message) || "Request failed"); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }
26:  const t = (token) => "/cases/" + encodeURIComponent(token);
33:    item: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id)),
34:    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
35:    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + encodeURIComponent(rid) + "/confirm_date", { date }),
2:import re
3:import pytest
4:from playwright.sync_api import expect
5:from tests.e2e.conftest import api, open_case, golden_text, BASE
8:def test_synthetic_banner_always_visible(page):
12:def test_load_sample_shows_nine_records_before_any_model_call(page):
17:def test_pdf_upload_refused_with_plain_message(page, tmp_path):
23:def test_txt_upload_equals_paste(page, tmp_path):
33:def test_ambiguous_date_goes_to_dates_to_confirm(page):
46:def test_confirming_a_date_with_no_entry_keeps_the_record_visible(page):
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:37.314Z

**tool call — Bash**
````
{
 "command": "sed -n 28,100p tests/e2e/test_input.py; sed -n 1,40p tests/unit/test_e2e_contract.py; grep -n \"def open_case\" -A15 tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T02:59:37.411Z

**tool result**
````
def _analyze_case_01(page):
    page.goto(BASE); page.get_by_test_id("input-text").fill(golden_text("case_01_date_formats.txt")); page.get_by_test_id("btn-analyze").click()
    expect(page.get_by_test_id("dates-to-confirm")).to_contain_text("04/05/2026", timeout=120000)

def test_ambiguous_date_goes_to_dates_to_confirm(page):
    """R-IN-3/R-IN-5, undated-entry branch (T-068): case_01 record 8 (04/05/2026) has an undated entry. It is listed ONCE, in
    'Dates to confirm', with both readings and its verbatim excerpt; confirming it moves the entry onto the timeline."""
    _analyze_case_01(page)
    box = page.get_by_test_id("dates-to-confirm")
    assert page.get_by_test_id("date-to-confirm-item").count() == 0, "this case has an undated entry, so the no-entry row must not render"
    expect(box.get_by_test_id("confirm-date")).to_have_count(2)
    expect(box.get_by_test_id("entry-excerpt")).to_contain_text("Patient reports no new symptoms.")
    expect(page.locator('[data-testid="missing-entry"][data-record-id="r8"]')).to_have_count(0)   # not listed twice
    box.locator('[data-testid="confirm-date"][data-date="2026-04-05"]').click()
    expect(box).to_contain_text("None. Every record has a readable date.")
    expect(page.get_by_test_id("queue").get_by_test_id("entry-date").filter(has_text="2026-04-05")).to_have_count(1)

def test_confirming_a_date_with_no_entry_keeps_the_record_visible(page):
    """T-068 round 2 (orphan branch, forced: the case response is rewritten so record 8 has no entry anywhere). The row shows the
    verbatim excerpt, offers both dates and Open record; confirming does NOT make the record vanish: it moves to
    'Records without an entry' with the confirmed date and the by-hand entry control. The record is listed once at every step."""
    def strip_r8(route):
        r = route.fetch(); body = r.json()
        for k in ("entries", "undated_entries", "tray"):
            body[k] = [x for x in body.get(k, []) if "r8" not in x.get("record_ids", [])]
        route.fulfill(response=r, json=body)
    page.route(re.compile(r"/api/cases/[^/?]+$"), lambda route: strip_r8(route) if route.request.method == "GET" else route.continue_())
    _analyze_case_01(page)
    row = page.locator('[data-testid="date-to-confirm-item"][data-record-id="r8"]')
    expect(row).to_have_count(1)
    expect(row.get_by_test_id("date-to-confirm-excerpt")).to_have_text("Patient reports no new symptoms.")
    expect(row.get_by_test_id("confirm-date")).to_have_count(2)
    expect(page.locator('[data-testid="missing-entry"][data-record-id="r8"]')).to_have_count(0)   # not listed twice before confirming
    row.get_by_test_id("btn-source").click()
    expect(page.get_by_test_id("record-modal")).to_contain_text("Patient reports no new symptoms.")
    page.keyboard.press("Escape")
    row.locator('[data-testid="confirm-date"][data-date="2026-04-05"]').click()
    expect(page.get_by_test_id("date-to-confirm-item")).to_have_count(0)
    left = page.locator('[data-testid="missing-entry"][data-record-id="r8"]')
    expect(left).to_have_count(1)
    expect(left.get_by_test_id("missing-date-confirmed")).to_contain_text("April 5, 2026")
    expect(left.get_by_test_id("btn-manual-entry")).to_be_visible()
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
85:def open_case(page, tok):
86-    page.goto(f"{BASE}/#/case/{tok}")
87-    page.get_by_test_id("timeline").wait_for(timeout=15000)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:51.828Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"disabled\\|rv-help\\|\\.rv-error\" review.css styles.css | head; grep -n \"ZL.el = \\|function el\" -A14 dom.js | head -30; grep -n \"<script\" index.html"
}
````

### User / tool · 2026-11-02T02:59:51.944Z

**tool result**
````
styles.css:56:.btn[disabled]{opacity:.5;cursor:not-allowed}.entry,[tabindex],.btn{scroll-margin-top:90px}
review.css:10:.rv-help, .rv-keys, .rv-why, .rv-empty { color: var(--rv-muted); font-size: .9rem; margin: .25rem 0 .75rem; }
review.css:45:.rv-btn:disabled { opacity: .5; cursor: not-allowed; }
review.css:51:.rv-error { color: var(--rv-bad-ink); font-size: .9rem; margin: .3rem 0 0; }
review.css:52:.rv-error:empty { display: none; }
review.css:94:.rv-batchbar .rv-help { margin: 0; flex: 1 1 16rem; }
review.css:108:.es-field .rv-help { display: block; margin: .15rem 0 0; font-weight: 400; }
5:  ZL.el = function (tag, attrs, ...kids) {
6-    const e = document.createElement(tag);
7-    for (const [k, v] of Object.entries(attrs || {})) {
8-      if (v === false || v == null) continue;
9-      if (k === "class") e.className = v;
10-      else if (k === "text") e.textContent = v;
11-      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
12-      else e.setAttribute(k, v === true ? "" : String(v));
13-    }
14-    for (const c of kids.flat()) {
15-      if (c == null || c === false) continue;
16-      e.append(c.nodeType ? c : document.createTextNode(String(c)));
17-    }
18-    return e;
19-  };
42:<script src="dom.js"></script>
43:<script src="mock_sample.js"></script>
44:<script src="mock.js"></script>
45:<script src="mock_flags.js"></script>
46:<script src="mock_extra.js"></script>
47:<script src="api.js"></script>
48:<script src="state.js"></script>
49:<script src="input.js"></script>
50:<script src="source.js"></script>
51:<script src="timeline.js"></script>
53:<script src="review.js"></script>
54:<script src="flags.js"></script>
55:<script src="charges.js"></script>
56:<script src="batch.js"></script>
57:<script src="audit.js"></script>
58:<script src="manual.js"></script>
59:<script src="narrative.js"></script>
60:<script src="exportcfg.js"></script>
61:<script src="excerpt.js"></script>
62:<script src="export.js"></script>
63:<script src="switcher.js"></script>
64:<script src="app.js"></script>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:53.322Z

Now the edits.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:07.096Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\nimport re\np='review.js'; s=open(p).read()\n\n# 1. plain-words DATE_UNCONFIRMED + client guard in RV.act\ns=s.replace('''    const found = RV.find(c, id);\n    busy.add(id);''','''    const found = RV.find(c, id);\n    if (body.action === \"accept\" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + \" \" + DATE_WHY); return false; }   // D-041: never sent; the server refuses too\n    busy.add(id);''')\ns=s.replace('''      if (e && e.code === \"needs_confirm\") showConfirm(id, e, body);''','''      if (e && e.code === \"needs_confirm\") showConfirm(id, e, body);\n      else if (e && String(e.code).toUpperCase() === \"DATE_UNCONFIRMED\") showError(id, DATE_FIRST + \" \" + DATE_WHY);''')\ns=s.replace('''  // ---- the one place a decision is sent''','''  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter\n  const DATE_FIRST = \"Confirm the date first.\", DATE_WHY = \"This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.\";\n  RV.needsDate = (item, kind) => kind === \"entry\" && !item.date;\n  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices\n    const row = document.querySelector('[data-testid=\"dates-to-confirm\"] [data-entry-id=\"' + id + '\"]');\n    const t = row && (row.querySelector('[data-testid=\"confirm-date\"]') || row);\n    const box = document.querySelector('[data-testid=\"dates-to-confirm\"]');\n    const f = t || box; if (!f) return;\n    if (!f.hasAttribute(\"tabindex\") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute(\"tabindex\", \"-1\");\n    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: \"center\" });\n  }\n\n  // ---- the one place a decision is sent''',1)\n\n# 2. disable accept + reason\ns=s.replace('''    bar.append(btn(\"accept\", noted ? \"Accept as noted\" : \"Accept\", \"btn-accept\", { \"aria-pressed\": String(st === \"accepted\"), onclick:''','''    const blocked = RV.needsDate(item, kind) && st !== \"accepted\";\n    bar.append(btn(\"accept\", noted ? \"Accept as noted\" : \"Accept\", \"btn-accept\", { \"aria-pressed\": String(st === \"accepted\"), disabled: blocked, \"aria-describedby\": blocked ? \"why-blocked-\" + id : null, onclick:''')\ns=s.replace('''    root.append(bar);\n\n    // dismiss reason''','''    root.append(bar);\n    if (blocked) root.append(el(\"p\", { class: \"rv-help rv-blocked\", id: \"why-blocked-\" + id, \"data-testid\": \"accept-blocked-reason\" }, DATE_FIRST + \" \",\n      el(\"button\", { type: \"button\", class: \"btn small\", \"data-testid\": \"link-confirm-date\", onclick: () => goToDateRow(id) }, \"Go to its date choices\")));\n\n    // dismiss reason''')\nopen(p,'w').write(s)\n\np='batch.js'; s=open(p).read()\ns=s.replace('''const eligible = (c) => (c.entries || []).filter((e) => e.state === \"verified\" && (e.review_status || \"pending\") === \"pending\");''','''const eligible = (c) => (c.entries || []).filter((e) => e.date && e.state === \"verified\" && (e.review_status || \"pending\") === \"pending\");\n  // D-041: entries still without a confirmed date are never part of a batch; say how many were left out.\n  const skippedUndated = (c) => (c.undated_entries || []).concat((c.entries || []).filter((e) => !e.date)).filter((e) => (e.review_status || \"pending\") === \"pending\").length;\n  const skipText = (n) => n + (n === 1 ? \" undated entry was\" : \" undated entries were\") + \" skipped: confirm the date first (Dates to confirm).\";''')\ns=s.replace('''    const ids = eligible(c).map((e) => e.id); if (!ids.length) return;''','''    const ids = eligible(c).map((e) => e.id), skipped = skippedUndated(c);\n    if (!ids.length) { if (skipped) RV.say(\"Nothing to accept. \" + skipText(skipped)); return; }''')\ns=s.replace('''        const plain = (r.status === 404''','''        const code = r.body && r.body.error && r.body.error.code;\n        if (String(code).toUpperCase() === \"DATE_UNCONFIRMED\") { RV.say(\"Confirm the date first. An entry in this batch has no confirmed date, so nothing was accepted. Pick its date in Dates to confirm, then try again.\", true); return; }\n        const plain = (r.status === 404''')\ns=s.replace('''\" left to review.\"''','''\" left to review.\"''')\ns=s.replace('''(ids.length === 1 ? \"entry\" : \"entries\") + \". Undo is available.\");''','''(ids.length === 1 ? \"entry\" : \"entries\") + \". Undo is available.\" + (skipped ? \" \" + skipText(skipped) : \"\"));''')\ns=s.replace('''    const n = eligible(c).length;\n''','''    const n = eligible(c).length, sk = skippedUndated(c);\n''')\ns=s.replace('''      el(\"span\", { class: \"rv-help\" }, \"Entries only.''','''      sk ? el(\"span\", { class: \"rv-help rv-blocked\", \"data-testid\": \"batch-skipped-note\" }, skipText(sk)) : null,\n      el(\"span\", { class: \"rv-help\" }, \"Entries only.''')\nopen(p,'w').write(s)\n\np='timeline.js'; s=open(p).read()\n# N2 record number for undated\ns=s.replace('''        el(\"span\", { class: \"provider\", \"data-testid\": \"entry-provider\" }, e.provider),\n        stateChip(e),''','''        el(\"span\", { class: \"provider\", \"data-testid\": \"entry-provider\" }, (!e.date && rec ? `Record ${rec.seq}: ` : \"\") + e.provider),\n        stateChip(e),''')\ns=s.replace('''ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : \"\"}: ${e.provider}`) }, \"Open record\"))''','''ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : \"\"}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : \"Open record\"))''')\ns=s.replace('''  function datesToConfirm(c) {''','''  ZL.recordExcerpt = recordExcerpt;\n  function datesToConfirm(c) {''')\nopen(p,'w').write(s)\n\np='manual.js'; s=open(p).read()\ns=s.replace('''        el(\"div\", { class: \"rv-actions\" }, el(\"button\", { type: \"button\", class: \"rv-btn rv-secondary\", onclick: () => ZL.openSource([{ record_id: r.id''','''        r.date_status === \"confirmed\" && ZL.recordExcerpt && ZL.recordExcerpt(r) ? el(\"blockquote\", { class: \"excerpt\", \"data-testid\": \"missing-entry-excerpt\" }, ZL.recordExcerpt(r)) : null,\n        el(\"div\", { class: \"rv-actions\" }, el(\"button\", { type: \"button\", class: \"rv-btn rv-secondary\", onclick: () => ZL.openSource([{ record_id: r.id''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"skipped\" batch.js | head; grep -n \"blocked\\|goToDateRow\" review.js | head; grep -n \"\\.excerpt\" styles.css review.css | head -3"
}
````

### User / tool · 2026-11-02T03:00:07.225Z

**tool result**
````
9:  const skippedUndated = (c) => (c.undated_entries || []).concat((c.entries || []).filter((e) => !e.date)).filter((e) => (e.review_status || "pending") === "pending").length;
10:  const skipText = (n) => n + (n === 1 ? " undated entry was" : " undated entries were") + " skipped: confirm the date first (Dates to confirm).";
16:    const ids = eligible(c).map((e) => e.id), skipped = skippedUndated(c);
17:    if (!ids.length) { if (skipped) RV.say("Nothing to accept. " + skipText(skipped)); return; }
29:      RV.say("Accepted " + ids.length + " verified " + (ids.length === 1 ? "entry" : "entries") + ". Undo is available." + (skipped ? " " + skipText(skipped) : ""));
49:    const n = eligible(c).length, sk = skippedUndated(c);
54:      sk ? el("span", { class: "rv-help rv-blocked", "data-testid": "batch-skipped-note" }, skipText(sk)) : null,
143:  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
190:    const blocked = RV.needsDate(item, kind) && st !== "accepted";
191:    bar.append(btn("accept", noted ? "Accept as noted" : "Accept", "btn-accept", { "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null, onclick: () => RV.act(id, { action: "accept" }, { focus: "accept" }) }));
199:    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
200:      el("button", { type: "button", class: "btn small", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));
styles.css:40:.excerpt{margin:6px 0;padding:6px 10px;border-left:3px solid var(--line);color:var(--muted);font-style:italic;overflow-wrap:anywhere}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:22.100Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_input.py'; s=open(p).read()\ns=s.replace('''    expect(left.get_by_test_id(\"btn-manual-entry\")).to_be_visible()''','''    expect(left.get_by_test_id(\"btn-manual-entry\")).to_be_visible()\n    expect(left.get_by_test_id(\"missing-entry-excerpt\")).to_have_text(\"Patient reports no new symptoms.\")   # the quote stays on the card she acts on (T-068 r3)\n\ndef test_undated_row_shows_record_number(page):\n    \"\"\"T-068 r3 (paralegal N2): the undated entry in Dates to confirm names its record and its Open button carries the number.\"\"\"\n    _analyze_case_01(page)\n    row = page.get_by_test_id(\"dates-to-confirm\").locator('[data-testid^=\"entry-\"][data-entry-id]').first\n    expect(row.get_by_test_id(\"entry-provider\")).to_contain_text(\"Record 8:\")\n    expect(row.get_by_test_id(\"btn-source\")).to_have_text(\"Open record 8\")\n\ndef test_undated_entry_cannot_be_accepted_until_date_confirmed(page):\n    \"\"\"T-068 r3 / D-041: on an undated entry Accept is disabled with the visible reason 'Confirm the date first' and a link to the date choices;\n    the keyboard shortcut and 'Accept all verified' do not accept it (the batch says how many it skipped); the letter never says 'date not stated';\n    after the date is confirmed Accept is enabled.\"\"\"\n    _analyze_case_01(page)\n    box = page.get_by_test_id(\"dates-to-confirm\")\n    row = box.locator('[data-testid^=\"entry-\"][data-entry-id]').first\n    expect(row.get_by_test_id(\"btn-accept\")).to_be_disabled()\n    expect(row.get_by_test_id(\"accept-blocked-reason\")).to_contain_text(\"Confirm the date first\")\n    row.get_by_test_id(\"link-confirm-date\").click()\n    expect(row.get_by_test_id(\"confirm-date\").first).to_be_focused()\n    page.keyboard.press(\"Escape\")\n    row.focus(); page.keyboard.press(\"a\")\n    expect(row).to_have_attribute(\"data-review\", \"pending\")\n    expect(page.get_by_test_id(\"batch-skipped-note\")).to_contain_text(\"1 undated entry was skipped\")\n    page.get_by_test_id(\"btn-accept-verified\").click()\n    expect(row).to_have_attribute(\"data-review\", \"pending\")\n    expect(page.locator('#rv-live')).to_contain_text(\"1 undated entry was skipped\")\n    page.get_by_test_id(\"btn-export\").click()\n    expect(page.get_by_test_id(\"export-letter\")).not_to_contain_text(\"date not stated\")\n    page.keyboard.press(\"Escape\")\n    box.locator('[data-testid=\"confirm-date\"][data-date=\"2026-04-05\"]').click()\n    entry = page.get_by_test_id(\"queue\").locator('[data-testid^=\"entry-\"][data-entry-id]').filter(has_text=\"2026-04-05\")\n    expect(entry.get_by_test_id(\"btn-accept\")).to_be_enabled()\n\ndef test_server_date_unconfirmed_is_explained_in_plain_words(page):\n    \"\"\"T-068 r3: a 422 DATE_UNCONFIRMED from the server (T-076) is shown as a plain sentence, not a raw code.\"\"\"\n    page.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/review$\"), lambda route: route.fulfill(status=422, json={\"error\": {\"code\": \"DATE_UNCONFIRMED\", \"message\": \"DATE_UNCONFIRMED\"}}))\n    _analyze_case_01(page)\n    entry = page.get_by_test_id(\"queue\").locator('[data-testid^=\"entry-\"][data-entry-id]').first\n    entry.get_by_test_id(\"btn-accept\").click()\n    expect(entry.locator(\".rv-error\")).to_contain_text(\"Confirm the date first\")\n    expect(entry.locator(\".rv-error\")).not_to_contain_text(\"DATE_UNCONFIRMED\")''')\nopen(p,'w').write(s)\np='tests/e2e/conftest.py'; s=open(p).read()\ns=s.replace('''btn-manual-entry (by-hand entry control on a missing-entry row).''','''btn-manual-entry (by-hand entry control on a missing-entry row).\n  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"export-letter\" tests/e2e/test_export_ui.py | head -3; grep -n \"btn-export\" -B2 -A4 tests/e2e/test_export_ui.py | head -20; ls tools | grep serve; cat tools/serve_app.sh 2>/dev/null | head -20"
}
````

### User / tool · 2026-11-02T03:00:22.254Z

**tool result**
````
22:    assert "7 of 9" in page.get_by_test_id("count-line").inner_text() and "7 of 9" not in page.get_by_test_id("export-letter").inner_text()
29:    assert page.get_by_test_id("export-letter").inner_text().strip() == g.strip()
34:    assert "February 20, 2026" not in page.get_by_test_id("export-letter").inner_text()
11-def test_two_blocks_and_copy_buttons(page, sample_case):
12-    """R-EX-1/R-EX-5: two separate blocks with a Copy button each; clipboard of the letter has no count line."""
13:    open_case(page, sample_case); accept_everything(page); page.get_by_test_id("btn-export").click()
14-    page.get_by_test_id("btn-copy-letter").click(); clip = page.evaluate("navigator.clipboard.readText()")
15-    assert clip.startswith("TREATMENT CHRONOLOGY") and "of 9" not in clip
16-
17-def test_count_line_outside_both_blocks(page, sample_case):
--
19-    open_case(page, sample_case)
20-    for i in (1, 2, 3, 4, 7, 8, 9): page.get_by_test_id(f"entry-{i}").get_by_test_id("btn-accept").click()
21:    page.get_by_test_id("entry-5").get_by_test_id("btn-dismiss").click(); page.get_by_test_id("btn-export").click()
22-    assert "7 of 9" in page.get_by_test_id("count-line").inner_text() and "7 of 9" not in page.get_by_test_id("export-letter").inner_text()
23-    n = page.get_by_test_id("export-notes").inner_text(); assert "Record 5" in n and "dismissed" in n and "not reviewed" in n
24-
25-def test_letter_equals_golden_when_everything_accepted(page, sample_case):
26-    """R-EX-6: byte equality with sample.export.expected.txt letter block (fixture backend)."""
27:    open_case(page, sample_case); accept_everything(page); page.get_by_test_id("btn-export").click()
28-    g = golden_text("sample.export.expected.txt").split("=== INTERNAL_NOTES_TEXT")[0].split("\n", 1)[1].rstrip("\n")
29-    assert page.get_by_test_id("export-letter").inner_text().strip() == g.strip()
30-
board_server.py
serve_app.sh
serve_board.sh
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:26.485Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_input.py'; s=open(p).read()\ns=s.replace('''    page.keyboard.press(\"Escape\")\n    row.focus(); page.keyboard.press(\"a\")''','''    page.keyboard.press(\"a\")''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"PORT\\|port\" app/main.py app/config.py 2>/dev/null | head -5\nmkdir -p artifacts/tmp; (PORT=7881 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/tmp/r3.sqlite3 nohup .venv/bin/python -m app.main > /tmp/r3.log 2>&1 &); sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7881/api/health; tail -3 /tmp/r3.log"
}
````

### User / tool · 2026-11-02T03:00:30.680Z

**tool result**
````
2:import os
4:import uvicorn
6:from app.backend.api import create_app
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:32.392Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://127.0.0.1:7881 .venv/bin/python -m pytest tests/e2e/test_input.py tests/unit/test_e2e_contract.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T03:01:14.157Z

**tool result**
````
..........F.                                                             [100%]
=================================== FAILURES ===================================
________________________ test_data_attributes_declared _________________________

    def test_data_attributes_declared():
        """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
        c = contract()
        for p in specs():
            for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
>               assert a in c, (p.name, a)
E               AssertionError: ('test_input.py', 'data-entry-id')
E               assert 'data-entry-id' in 'E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fi...bugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).\n'

tests/unit/test_e2e_contract.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_data_attributes_declared - Asser...
1 failed, 11 passed in 41.38s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:17.413Z

**tool call — Bash**
````
{
 "command": "sed -i 's/\\[data-entry-id\\]/[data-item-id]/g' tests/e2e/test_input.py && E2E_BASE_URL=http://127.0.0.1:7881 .venv/bin/python -m pytest tests/e2e tests/unit/test_e2e_contract.py -q 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T03:01:17.518Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/e2e/test_input.py
": undefined label 'ests/e2e/test_input.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:19.106Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/\\[data-entry-id\\]/[data-item-id]/g' tests/e2e/test_input.py && E2E_BASE_URL=http://127.0.0.1:7881 .venv/bin/python -m pytest tests/e2e tests/unit/test_e2e_contract.py -q 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T03:02:40.454Z

**tool result**
````
....................................................s...........ss...... [ 93%]
.....                                                                    [100%]
74 passed, 3 skipped in 80.95s (0:01:20)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:02:45.844Z

**tool call — Bash**
````
{
 "command": "pkill -f \"PORT=7881\" ; lsof -ti :7881 | xargs kill 2>/dev/null\ngit add app/frontend/review.js app/frontend/batch.js app/frontend/timeline.js app/frontend/manual.js tests/e2e/test_input.py tests/e2e/conftest.py && git commit -q -m \"feat(frontend): block accept on undated entries until the date is confirmed; record no. and excerpt on date rows (T-068 r3, D-041)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && SHA=$(git rev-parse --short HEAD) && echo $SHA\nB=\"python3 tools/board.py\"\n$B ac T-068 --check 1 --agent frontend --evidence \"tests/e2e/test_input.py::test_undated_entry_cannot_be_accepted_until_date_confirmed, ::test_server_date_unconfirmed_is_explained_in_plain_words, ::test_undated_row_shows_record_number; e2e 74 passed 3 skipped on :7881; test_e2e_contract green\"\n$B commit T-068 --sha $SHA --agent frontend\n$B handoff T-068 --agent frontend --text \"What changed: D-041 UI. Accept disabled on undated entries (review.js) with visible 'Confirm the date first' + link to the date choices; a-key and RV.act also refuse; Accept all (batch.js) skips undated and says how many; server 422 DATE_UNCONFIRMED shown in plain words (single and batch). Minors: record no. + 'Open record N' on undated rows (N2), verbatim excerpt kept on the confirmed-orphan card (N3). Verified: 74 e2e passed on :7881, contract test green. Left: N4 (curated fixture with a date-to-confirm record and no entry) is backend/qa-owned, not done; T-076 server rule lands separately. Surprise: undated entries are rendered only in Dates to confirm, so the link just focuses their own date buttons.\"\n$B move T-068 in_review --agent frontend"
}
````

### User / tool · 2026-11-02T03:02:45.930Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: pkill -f "PORT=7881" ; lsof -ti :7881 | xargs kill 2>/dev/null
git add app/frontend/review.js app/frontend/batch.js app/frontend/timeline.js app/frontend/manual.js tests/e2e/test_input.py tests/e2e/co
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:02:47.821Z

**tool call — Bash**
````
{
 "command": "lsof -ti :7881 | xargs kill 2>/dev/null; git add app/frontend/review.js app/frontend/batch.js app/frontend/timeline.js app/frontend/manual.js tests/e2e/test_input.py tests/e2e/conftest.py; git status --short | grep '^[AM]'"
}
````

### User / tool · 2026-11-02T03:02:48.028Z

**tool result**
````
M  app/frontend/batch.js
M  app/frontend/manual.js
M  app/frontend/review.js
M  app/frontend/timeline.js
M  tests/e2e/conftest.py
M  tests/e2e/test_input.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:02:48.762Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(frontend): block accept on undated entries until the date is confirmed; record no. and excerpt on date rows (T-068 r3, D-041)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/frontend/review.js app/frontend/batch.js app/frontend/timeline.js app/frontend/manual.js tests/e2e/test_input.py tests/e2e/conftest.py; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T03:02:49.184Z

**tool result**
````
check_secrets: ok (6 file(s) scanned staged)
5f71a65
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:02:52.322Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B ac T-068 --check 1 --agent frontend --evidence \"tests/e2e/test_input.py::test_undated_entry_cannot_be_accepted_until_date_confirmed, ::test_server_date_unconfirmed_is_explained_in_plain_words, ::test_undated_row_shows_record_number; e2e 74 passed 3 skipped on :7881; test_e2e_contract green\"\n$B commit T-068 --sha 5f71a65 --agent frontend\n$B handoff T-068 --agent frontend --text \"What changed: D-041 UI. Accept disabled on undated entries (review.js) with visible 'Confirm the date first' + link to the date choices; a-key and RV.act also refuse; Accept all (batch.js) skips undated and says how many; server 422 DATE_UNCONFIRMED shown in plain words (single and batch). Minors: record no. + 'Open record N' on undated rows (N2), verbatim excerpt kept on the confirmed-orphan card (N3). Verified: 74 e2e passed on :7881, contract test green. Left: N4 (curated fixture with a date-to-confirm record and no entry) is backend/qa-owned, not done; T-076 server rule lands separately. Surprise: undated entries render only in Dates to confirm, so the link just focuses their own date buttons.\"\n$B move T-068 in_review --agent frontend"
}
````

### User / tool · 2026-11-02T03:02:52.640Z

**tool result**
````
AC 1 checked: tests/e2e/test_input.py::test_undated_entry_cannot_be_accepted_until_date_confirmed, ::test_server_date_unconfirmed_is_explained_in_plain_words, ::test_undated_row_shows_record_number; e2e 74 passed 3 skipped on :7881; test_e2e_contract green
T-068: commit 5f71a65 recorded
handoff written on T-068
T-068: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:02:54.738Z

T-068 round 3 is committed (5f71a65) and moved to `in_review`. Accept is now disabled on undated entries with "Confirm the date first" and a link to their date choices, and batch accept skips undated entries and says how many. A server 422 DATE_UNCONFIRMED shows as a plain sentence. The full e2e suite passed (74 passed, 3 skipped) and the contract test is green.

Minors N2 (record number and "Open record N" on undated rows) and N3 (excerpt kept on the confirmed-orphan card) are fixed. N4, a curated fixture for the orphan branch, isn't done because fixtures aren't mine. I tested the 422 handling with a mocked response, not against the server rule from T-076.
