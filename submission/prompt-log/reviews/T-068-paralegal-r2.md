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
