# CONTRACT M2/M3: paralegal-reviewer (T-018, paralegal lens, covered by the PM agent per D-024)

**Verdict: changes.** 0 blockers, 4 majors, 4 minors.

The review-and-export journey is mostly pinned down. The letter is accepted-only, flags are kept out of it, the $185 rate is never totaled, keyboard and 375 px are covered, and reload restores statuses. Four gaps would let a build pass every AC and still lose her trust. (1) Nothing proves her edits survive a reload or show up in the notes with the original. (2) The reconciliation count in one test-first AC is wrong. (3) No AC renders the accident-date conflict as two dates. (4) A record whose model call fails three times has no visible place in the UI.

Evidence: card AC text via `board.py show`, the golden export at `evals/golden/sample.export.expected.txt`, and `artifacts/review-evidence/T-018-contract-probe.out.txt`. There is no app yet, so this is a contract review. `scores.verify_quickly` is projected from the AC, not measured.

```json
{"card": "T-018", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "Contract review of M3 journey AC (T-039..T-046) plus M2 items she sees (T-032, T-033, T-036), against spec/REQUIREMENTS.md §1.5-1.6, §6, ORCHESTRATOR_DECISIONS D-001/D-002/D-010/D-017/D-019, evals/golden/sample.export.expected.txt; commit e5733a1. No running app (M1).",
 "exercised": [
  "python3 tools/board.py show T-039 T-040 T-041 T-042 T-043 T-044 T-045 T-046 (AC text read item by item against the paralegal checklist 1-23)",
  "grep -n '12 planned' evals/golden/sample.export.expected.txt -> line 72 rate note",
  "grep -n LLM_FAILED_AFTER_RETRIES memory/contracts/api.md -> :454 'the record has no entry from it'",
  "read personas/paralegal.md in full; REQUIREMENTS R-RV-2, R-RV-8, R-EX-4, R-EX-7, R-FL-2, R-FL-6, R-CH-3, R-CO-9"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "letter_isolation": 5, "charges_reconcilable": 4, "edits_safe": 2, "adverse_facts_surfaced": 3},
 "findings": [
  {"severity": "major", "title": "No AC proves her edit survives a reload, or that the notes show original and new text",
   "evidence": "R-RV-8 test: 'accept 3 items, edit 1, reload -> same statuses'. T-043 AC3 'reload restores statuses and total' (no edit in the matrix). T-044 AC1 checks the 'edited' label and the letter, not the reload or notes. R-RV-2: 'the notes list the original and the new text'. T-039 AC2 notes tests cover order, cites, bills line and dismissal, not EDITED ITEMS content. Golden notes show only 'EDITED ITEMS - none'.",
   "why_it_matters": "'Losing my edits on refresh or export' is a dealbreaker for her. As written, a build that drops edited summaries on reload, or prints 'EDITED ITEMS - none' after an edit, passes every AC.",
   "fix": "T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'.",
   "acceptance_test": "tests/e2e/test_edit.py::test_edit_survives_reload and tests/unit/test_export.py::test_edited_items_section, both red before T-044/T-041."},
  {"severity": "major", "title": "T-039 AC2 reconciliation count contradicts R-EX-7",
   "evidence": "T-039 AC2: 'dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9'. R-EX-7: 'dismiss entry 5 and leave entry 6 pending -> ... \"7 of 9\"'. With only entry 5 dismissed and the rest accepted, 8 of 9 records are in the letter. T-044 AC4 has it right.",
   "why_it_matters": "'N of 9 records in letter' is how she knows nothing dropped silently. A test-first suite that encodes the wrong count either fails a correct build or teaches the builder to miscount.",
   "fix": "T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives \"Record 5 ... dismissed\", \"Record 6 ... not reviewed\" and 7 of 9'.",
   "acceptance_test": "test_export::test_reconciliation asserts both record lines and '7 of 9'."},
  {"severity": "major", "title": "No UI AC shows the accident-date conflict as two unmerged dates with both quotes",
   "evidence": "T-043 AC1: 'four flag groups ... sample has >=1 flag per group' (only a count). T-033 AC4 covers the backend rule. R-FL-2(a): '2026-01-09 (records 1, 2) vs \"Date of accident per intake form: 2026-01-19\" (record 7) ... not merged ... no choice made'.",
   "why_it_matters": "Merging or resolving the two accident dates is one of her dealbreakers, and it is the first thing an adjuster checks. The backend can be right while the card shows one date, or wording like 'corrected', and no test would fail.",
   "fix": "T-043 AC1 append: 'the accident-date conflict card shows \"Date of accident per intake form: 2026-01-19.\" and the 2026-01-09 header line(s) of records 1 and 2 side by side, and contains none of \"resolved\", \"correct date\", \"delay\"'.",
   "acceptance_test": "tests/e2e/test_flags_panel.py::test_accident_date_conflict_two_dates."},
  {"severity": "major", "title": "A record whose model call fails three times has no visible state in any M3 AC",
   "evidence": "R-CO-9: 'the item shows \"could not process\" with the reason, and the app stays usable'. api.md:454 'LLM_FAILED_AFTER_RETRIES | needs_review | ... the record has no entry from it'. T-034 AC2 tests the retry wrapper only; T-042 AC2 tray covers 'rejected' items; R-EX-7 reasons list 'rejected, dismissed or not reviewed', with nothing for failed. No M3 card names LLM_FAILED_AFTER_RETRIES.",
   "why_it_matters": "A record that silently has no entry is a lost fact, maybe the visit that closes a gap. She has to see 'record 4: could not process' and find it in the notes reconciliation.",
   "fix": "T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.",
   "acceptance_test": "tests/e2e/test_timeline.py::test_llm_failed_record_visible and test_export::test_failed_record_reconciled."},
  {"severity": "minor", "title": "Needs-review reason sentence not asserted on the item itself",
   "evidence": "R-FL-6 'when needs_review, a one-sentence reason'. T-042 AC2 'rows show date, provider, summary, excerpt, state'; T-043 AC1 shows groups only. The reason is only tested via Why? (T-042 AC3).",
   "why_it_matters": "Checklist 16: items needing review say why in one sentence, on sight, without an extra click per item.",
   "fix": "T-042 AC2 append: 'every needs_review row shows its why-template sentence inline'.",
   "acceptance_test": "test_timeline.py::test_reason_inline on case_07 record 3 shows the INJECTION_SUSPECTED sentence."},
  {"severity": "minor", "title": "$185 UI string is truncated relative to R-CH-3",
   "evidence": "T-043 AC2 \"'rate $185/visit; visit count not stated'\"; R-CH-3 \"rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review\".",
   "why_it_matters": "The '12 planned; discharged at visit 9' context is what lets her write the ledger request without opening two records.",
   "fix": "Quote the full R-CH-3 string in T-043 AC2.", "acceptance_test": "test_charges.py asserts the full string."},
  {"severity": "minor", "title": "Charges and injection banner not covered by the source-record and banner tests",
   "evidence": "R-RV-9 'Entries, flags ... and charges open the full record'; T-042 AC4 entry 8, T-043 AC5 gap flag, no charge. LLM_VS_CODE row 16 'a banner names the record and says flags may be incomplete'; T-043 AC1 'case_07 shows an injection warning'.",
   "why_it_matters": "She reconciles the $6,240 against the ER record, and she needs to know which record may have suppressed flags.",
   "fix": "T-043 AC5 append 'and the $6,240 charge opens record 2 with \"ER charges: $6,240.\" highlighted'. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'.",
   "acceptance_test": "test_source_record.py::test_charge_highlight; test_flags_panel.py::test_injection_banner_names_record."},
  {"severity": "minor", "title": "Dismissed-flag reason not proven to reach the notes",
   "evidence": "R-RV-5 'A dismissed flag may carry an optional reason'; R-EX-4(3) 'Flags dismissed, with any reason'. T-043 AC3 dismiss -> reset -> dismiss has no reason; T-039 AC2 has no FLAGS DISMISSED content case.",
   "why_it_matters": "The attorney reads why she dismissed the 'new onset' flag. If the reason is lost, the dismissal looks like an oversight.",
   "fix": "T-043 AC3 append 'dismiss the gap flag with reason \"treating elsewhere, records requested\" -> notes FLAGS DISMISSED shows it verbatim'.",
   "acceptance_test": "test_review_matrix.py::test_dismiss_reason_in_notes."}
 ],
 "whats_right": [
  "Letter isolation is tested from both sides: builder has no flags argument (T-039 AC1) and E2E bans note text, labels, '73 days', counts (T-045 AC2)",
  "$185 can't reach the total by any path: T-033 AC2, T-039 AC3 accept-$185 keeps $8,390, T-043 AC2 no PT total",
  "Copy asks once when a flag is pending, '1 flag not reviewed' (T-044 AC4), and the count line is in neither block (T-044 AC3)"
 ],
 "questions_for_chris": []}
```
