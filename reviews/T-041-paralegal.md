# T-041 paralegal review (Maria Delgado persona)

Verdict: changes. The export logic is what I need. Everything-accepted output matches the golden byte for byte, and nothing dismissed or unreviewed reaches the letter. One AC is ticked done with its named proof test missing, and `export.py` does nothing to stop a non-verbatim quote reaching the letter.

Would I paste the letter block into a demand? Yes, for the sample.
- Each line has a long-form date, the provider as written, a summary, and a verbatim quote with `[Ex. __ / Bates __]`.
- The total reads exactly "Billed charges stated in these records: $8,390.00" (or $420.00 for case_07).
- The only non-ASCII character is the em dash. There are no markdown symbols, flag labels or counts.
- I would still check the MRI summary line, "the record states findings may represent degenerative change", with the attorney. The golden file puts it in the letter and the notes list it under "flagged language quoted in the letter".

What I ran (script: `artifacts/review-evidence/T-041-export.py`; outputs saved alongside it):
- `.venv/bin/python -m pytest tests/unit/test_export.py -q` -> `19 passed`. With `test_boundaries.py` the count is 47 passed.
- Everything accepted, diffed against `sample.export.expected.txt`: 0 diff lines for the letter and 0 for the notes. Records are parsed from `sample.txt` in my script, not through the test's `build_case`.
- Dismiss entry 5 and leave entry 6 pending:
  - February 20 and March 6 are gone from the letter.
  - Notes list "Record 5 (Capital PT, visit 8, February 20, 2026) — dismissed" and "Record 6 (Capital PT, visit 9, March 6, 2026) — not reviewed".
  - The same notes show "Items not reviewed: 1" and a PENDING ITEMS entry.
  - `counts` is records_in_letter 7, records_total 9. "7 of 9" appears in neither block.
- case_07 with the $420 charge and the $50,000 unclear amount both accepted: the total line is exactly `Billed charges stated in these records: $420.00`. The letter contains no "50,000" and no "IGNORE". The notes list $50,000 as unclear and say "Request clean copy of bill."
- Letter content checks: no flag label, note, "AI assistance", count line, `$185`, or markdown tokens. All 11 `Source [...]` quotes are substrings of their raw records.
- Other scenarios:
  - A pending MRI charge drops the total to $6,240.00 and lands in the notes.
  - Dismissing the ER entry and its charge leaves the Bills to request line unchanged.
  - A record flagged `could_not_process` shows in the notes as "Record 4 ... — could not process" and is absent from the letter.
  - Output is deterministic.
  - With everything dismissed or pending, the letter is only the "TREATMENT CHRONOLOGY" title line.
- Not exercised: the HTTP route. `curl http://localhost:7860/api/cases/x/export` returned 000 (no app running), and the loader is not wired until T-040.

```json
{"card": "T-041", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/export.py, app/backend/export_routes.py (commits fa95e58, 52a1f49); tests/unit/test_export.py; sample case via build_export (no running app; HTTP route not exercised)",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit/test_export.py -q -> 19 passed; with test_boundaries.py -> 47 passed",
  "artifacts/review-evidence/T-041-export.py: all-accepted export diffed against evals/golden/sample.export.expected.txt (0 diff lines, letter and notes)",
  "same script: dismiss entry 5 + pending entry 6 -> Record 5 dismissed, Record 6 not reviewed, Items not reviewed: 1, counts 7 of 9 outside both blocks (artifacts/review-evidence/T-041-export-dismiss5-pending6.txt)",
  "same script: case_07 total line exactly 'Billed charges stated in these records: $420.00', $50,000 only in notes as unclear (artifacts/review-evidence/T-041-export-case07.txt)",
  "same script: letter free of flag labels/notes/AI line/count/$185/markdown; all 11 letter quotes are verbatim substrings of the raw records",
  "same script: pending charge, all dismissed, all pending, determinism; T-041-cnp.py: record 4 could_not_process listed in the notes",
  "curl http://localhost:7860/api/cases/x/export -> 000 (no server); grep -rn test_export_endpoint tests -> no matches"],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "only_accepted_in_letter": 5, "total_line_exact": 5, "notes_reconcile_dismissed_pending": 5, "ac_evidence_honest": 2},
 "findings": [
  {"severity": "major", "title": "AC4 is ticked done but its named proof test does not exist and the route cannot be reached",
   "evidence": "board show T-041 AC4: 'proved by test_api::test_export_endpoint', evidence field: 'test_api::test_export_endpoint does not exist yet - T-040 wires loader'. grep -rn test_export_endpoint tests -> no matches. curl http://localhost:7860/api/cases/x/export -> 000. app/backend/export_routes.py:3-4: the loader and include_router are left to T-040.",
   "why_it_matters": "I cannot confirm that pending, dismissed or rejected items are excluded through the real endpoint (row 19), which is the 'Export that includes something I dismissed or never reviewed' dealbreaker. The AC is marked done on the strength of a TestClient check run by hand.",
   "fix": "Untick AC4 or re-scope it to the function. Add test_api::test_export_endpoint (qa) and wire the loader in T-040 so the endpoint is covered.",
   "acceptance_test": "test_api::test_export_endpoint: via the loader, set entry 5 to dismissed and entry 6 to pending, GET /api/cases/{token}/export -> 200 with separate letter_text and internal_notes_text; February 20 and March 6 are absent from the letter; 404 for an unknown token."},
  {"severity": "minor", "title": "export.py trusts entry['excerpt'] and writes it as the verbatim quote with no check against the record",
   "evidence": "T-041-export.py scenario 6: entry 3 given edited excerpt 'Persistent neck pain 6/10, daily headaches. Patient has chronic condition.' -> 'Patient has chronic condition' appears in letter_text. app/backend/export.py:167 emits f'{SOURCE_PREFIX}\"{e[\"excerpt\"]}\"' unchanged. (R-RV-2 says the edit layer rejects such edits, but that is T-040, not built here.)",
   "why_it_matters": "If the edit layer ever lets a non-verbatim excerpt through, the letter would present invented text as a record quote. That is the adjuster-finds-a-mismatch scenario I get blamed for.",
   "fix": "Add a cheap invariant in build_letter: skip the line and list the entry in the notes as 'excerpt not found in record' when the excerpt is not a substring of the record's excerpt.",
   "acceptance_test": "unit: entry with excerpt not contained in its record's excerpt -> absent from letter_text, listed in the notes."},
  {"severity": "minor", "title": "Could-not-process path (AC3/AC6) and the rate-parenthetical regex have no dedicated test",
   "evidence": "grep -rn 'could_not_process\\|could not process' tests -> no matches. Handoff: 'no dedicated test for could-not-process record'; the '(12 planned; discharged at visit 9)' wording is regex-derived from same-provider records at export.py:308-312.",
   "why_it_matters": "I confirmed by hand that record 4 shows as 'could not process' in the notes, and the rate reason is correct for the sample. Neither is locked by a test; a regex change could silently alter the visit-count reason.",
   "fix": "Add the two tests the handoff lists as missing.",
   "acceptance_test": "unit: record with could_not_process=True appears under RECORDS NOT IN THE TREATMENT SECTION as 'Record N (...) — could not process'; the rate line for the sample contains '12 planned; discharged at visit 9'."}
 ],
 "whats_right": [
  "Golden byte equality holds for both blocks, and the total line has no parenthetical, so the $185 rate never touches the total.",
  "Dismissed and pending items are reconciled in the notes (Record 5 dismissed, Record 6 not reviewed, Items not reviewed: 1) and never appear in the letter.",
  "The injected '$50,000' in case_07 is kept out of the letter and the total, and surfaces in the notes as an unclear amount with an action."],
 "questions_for_chris": []}
```
