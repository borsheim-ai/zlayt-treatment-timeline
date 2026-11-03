# GATE-M3 — paralegal-reviewer (Maria Delgado, senior PI paralegal, Austin)

**Commit:** d0b04bc, run from a `git archive d0b04bc` copy in the session scratchpad. Port 7941, `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, scratch DB. The server was stopped by PID 49280. After the kill, `lsof` on 7941 exited 1 and curl returned 000.

**Verdict: changes** (0 blockers, 1 major, 7 minors, 2 nits). **verify_quickly = 4.** The D-015 ship bar is met.

I did the whole job on the sample case as a user. I pasted the sample text (analysis took 1.3 s) and reviewed all 23 items from the keyboard: 26 keys, 23.4 s of script time, one reload partway through. I edited the record-3 summary, dismissed the "New-onset wording" flag, kept $185 and the lost-work mention in the notes, and accepted the two charges. I opened records, checked every quote against `evals/golden/sample.txt`, then exported the letter (two-line and one-line layouts), copied the notes and downloaded both. A second sample case tested the draft treatment paragraph, a dismissed entry whose charge was accepted, and pending items. From the case overview I then did library case lib08 (second crash), also keyboard-first, with flag notes, charges, a reload and the export.

Before opening the output I listed what I expected from Appendix A. Every item is there and correct:
- 9 entries in date-of-service order. EMS and ER on 01-09 stay separate.
- One gap flag, "Gap of 73 days" (03-06 to 05-18). The 28-day interval is not flagged.
- The 01-09 vs 01-19 conflict shows both quotes, and the tool says "the tool does not choose between them".
- The PT plan (12 visits) vs the discharge at visit 9 is flagged.
- Both prior-condition mentions are flagged, and the missed-appointment wording raises a causation flag.
- The letter total is $8,390.00. $185 is listed as a rate with "visit count not stated (12 planned; discharged at visit 9)", in the notes only.
- "Missing 3 days of work" appears as a damages mention, not a charge.
- My edit is in the letter. The original wording stays visible in the app and in EDITED ITEMS. The dismissed flag appears only under FLAGS DISMISSED in the notes, and the letter has no flags.
- Decisions survived the reload.

## Where I distrusted the tool
1. **Major.** The accepted "TREATMENT SUMMARY" paragraph goes into the letter with short cites only: `(Austin EMS run report, January 9, 2026)`. It has no verbatim quote and no `[Ex. __ / Bates __]`, which D-002 rules out ("No short-cite mode"). It also restates the chronology in different words ("Discharged from PT" vs "Discharged from physical therapy"), and an adjuster will compare the two.
2. In the sample case the intake accident-date line is filed under "Causation language" with a "Needs review: phrase list found this flag but the AI did not" chip. The chip stays after I accept it.
3. The $185 rate row says "Accepted" in Status and "Kept in notes" under Decision. For a second I read it as an accepted charge.
4. I accepted the MRI charge, then dismissed the MRI entry. The letter still bills "$2,150.00" for a visit that is not in the chronology, and nothing warns me.
5. The draft paragraph failed after my edit (demo answers). The panel shows "could not draft ... after three tries" and also "Draft written. Read each sentence before you accept it."
6. lib08: ED "Denies LOC per patient" vs neurology "brief loss of consciousness" is not a conflict flag. The tool does say it does not check LOC history. Ortho's "numbness since the rear-end collision of 2026-01-12" (the AI's flag) was rejected by the second check and shows "Nothing to accept here", so I had no way to keep it in my notes except by writing a note on another flag.
7. After I save a flag note (Ctrl+Enter), focus stays on "Edit note" and `a` does nothing. `j` and `n` still work.
8. In the default "Needs review first" order, the edited Jan 16 entry stays above the Jan 9 entries after everything is decided.

## Exercised
See the JSON. The probe scripts and outputs are in `artifacts/review-evidence/GATE-M3-paralegal/` (p1 to p10, `unit-export.out.txt`).

```json
{"card": "GATE-M3", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit d0b04bc (git archive copy in session scratchpad); app http://127.0.0.1:7941 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB; listener PID 49280 killed, lsof exit 1, curl 000); sample case evals/golden/sample.txt pasted twice; library case case_lib08_second_crash_mri_after added from the case overview",
 "exercised": [
  "Server from git archive d0b04bc on port 7941; /api/health backend fixture, demo_mode true",
  "Unit tests in the archive: pytest tests/unit -k 'export or letter or narrative' -> 276 passed (artifacts/review-evidence/GATE-M3-paralegal/unit-export.out.txt)",
  "p1: pasted sample, Analyze, 1.3 s to overview; full text and screenshot p1-overview.txt/png",
  "p2: shortcuts list; Start review lands on $185 (a2); j forward only",
  "p3: full keyboard review of 23 items (26 keys, 23.4 s): a on entries/flags/charges, e + Ctrl+Enter edit of record 3 summary, compare prompt via a+Enter, d on New-onset flag, reload at step 8 (7 of 23 persisted), ends 23 of 23 decided",
  "p4: Export, letter + notes text, Copy letter -> clipboard equals letter (2729 chars)",
  "p5: Open record (record 3 modal shows full raw record), 'Not in an entry' on record 7, Why this status on record 8 (11 checks), draft paragraph after edit (failed), one-line letter layout, Download .txt for letter and notes",
  "p6/p7: second sample case: batch accept verified entries, draft paragraph, accept $2,150 then dismiss entry 8, accept paragraph, export letter + notes with 13 pending items",
  "p8: lib08 added from the case overview 'Add a synthetic case' (1.3 s); compared to evals/library/case_lib08_second_crash_mri_after.txt and .expected.json",
  "p9/p10: lib08 keyboard review, flag notes on f_r8_1 and the gap flag, keyboard after note save, three charges accepted, reload (21 of 21 persisted), export letter + notes ($11,240.00)",
  "Read personas/paralegal.md, CONTRACT M3 section, T-045 AC7, D-002, D-015, D-019, D-031, D-062, REQUIREMENTS non-goals, api.md narrative routes"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "sample_truths_found": 5, "export_fit_for_demand": 4, "keyboard_review": 4},
 "findings": [
  {"severity": "major", "title": "Accepted TREATMENT SUMMARY goes into the letter with short cites: no verbatim quote, no [Ex. __ / Bates __] (D-002)",
   "evidence": "artifacts/review-evidence/GATE-M3-paralegal/p7-letter.txt:35 'TREATMENT SUMMARY', :37 'On January 9, 2026, Austin EMS run report: Restrained driver rear-ended ... (Austin EMS run report, January 9, 2026)'; :42 'Discharged from PT after two missed appointments' vs chronology :24 'Discharged from physical therapy after two missed appointments'; tests/unit/test_narrative.py:120 asserts the '(Capital PT, visit 8, February 20, 2026)' form; memory/ORCHESTRATOR_DECISIONS.md:10 D-002 'No short-cite mode'",
   "why_it_matters": "The adjuster checks every letter line against the records. These sentences paraphrase the records with no quote and no Bates blank to fill in. They also repeat the chronology above them in different wording, so the same visit is described two ways in one demand.",
   "fix": "Give each TREATMENT SUMMARY sentence the D-002 citation: the quote and [Ex. __ / Bates __] (for example: ... pain 3/10. [Ex. __ / Bates __]). Alternatively, when the paragraph is accepted it replaces the chronology entries for those records instead of repeating them. If D-031 meant to allow a short cite, record it as an amendment to D-002.",
   "acceptance_test": "Unit + E2E: after narrative accept, every non-heading line of letter_text contains '[Ex. __ / Bates __]' or the configured Bates, and every TREATMENT SUMMARY sentence's entry excerpt appears verbatim in its line; test_narrative.py:120 updated."},
  {"severity": "minor", "title": "Accident-date line filed as 'Causation language'; Needs review chip stays after Accept",
   "evidence": "p3-after-walk.txt:327 'Accident date source' under 'Causation language (4)', :333 'Needs review: The phrase list found this flag but the AI did not; check that it applies.' shown beside 'Accepted'; p4-notes.txt 'Causation language: ... record 7 ... \"Date of accident per intake form: 2026-01-19.\"'",
   "why_it_matters": "An accident date source is not causation wording. In the notes my attorney reads it as a causation issue. The chip that stays after Accept makes me unsure whether my decision was recorded.",
   "fix": "Put accident-date-source flags under their own group (or under the conflict), both in the panel and in the notes. Clear or restate the reason chip once the item is decided.",
   "acceptance_test": "Sample: the notes have no 'Causation language' line quoting 'Date of accident per intake form'; after a on f_r7_1 the row shows no 'Needs review' text."},
  {"severity": "minor", "title": "Rate row shows Status 'Accepted' next to 'Kept in notes'",
   "evidence": "p3-after-walk.txt:450-462 '$185 ... Rate ... Accepted ... Not counted: This figure is a rate ... Kept in the internal notes only ... Kept in notes'",
   "why_it_matters": "'Accepted' in a charges table reads as an accepted charge. The total is correct ($8,390.00), but the row itself made me stop and check.",
   "fix": "For rate and damages rows, the Status column says 'Kept in notes' (or 'Noted'), never 'Accepted'.",
   "acceptance_test": "E2E: after a on amount-$185, the row text does not contain 'Accepted'."},
  {"severity": "minor", "title": "Dismissing an entry leaves its accepted charge in the letter with no warning",
   "evidence": "p6-letter.txt:37 'Austin Imaging, cervical MRI, May 29, 2026: $2,150.00', :40 'Billed charges accepted from these records: $2,150.00' while p6-notes.txt:31 '- Record 8 (Austin Imaging, cervical MRI, May 29, 2026) — dismissed'; p6-export.txt has no warning line about it",
   "why_it_matters": "The adjuster will ask why we bill an MRI the chronology leaves out. I accepted the charge myself, but nothing told me the two decisions conflict.",
   "fix": "When an entry is dismissed while its record has an accepted charge, show a one-line prompt in the charges panel and the export bar, and add a notes line. Let the paralegal keep the charge or dismiss it.",
   "acceptance_test": "E2E: accept $2,150, dismiss entry-8 -> a visible warning names record 8 and the internal notes list 'charge kept for a dismissed entry'."},
  {"severity": "minor", "title": "Draft paragraph failure shows a contradictory success line (demo, after an edit)",
   "evidence": "p5-narrative.txt:7 'The model could not draft the paragraph after three tries.' and :15 'Draft written. Read each sentence before you accept it.'; p5-narrative.png; server.log 'llm call failed ... step=narrative'",
   "why_it_matters": "I cannot tell whether a draft exists. In the demo, any edit makes the paragraph impossible to draft.",
   "fix": "Show only the failure message when no sentences come back. In demo mode, explain that edited entries have no recorded answer.",
   "acceptance_test": "E2E (fixture): edit an entry, press Draft -> 'Draft written' absent; message names the cause."},
  {"severity": "minor", "title": "lib08: LOC history change not flagged; the judge-vetoed onset flag cannot be kept in notes",
   "evidence": "p8-lib08-overview.txt:282 'Not checked: ... a change in loss of consciousness history between records'; :309 record 12 LOC line filed as 'Mention of another injury or event'; :233-246 'Could not verify (1)' 'Nothing to accept here' 'Reported onset — \"Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12.\"'; evals/library/case_lib08_second_crash_mri_after.expected.json flags C1 (must); evals/reports/library-latest.md:16 must flags 1/3",
   "why_it_matters": "Two incidents, a denied LOC vs a stated LOC, and an ortho note that dates the numbness to crash 1 are what the adjuster leads with. The tool discloses the limit, so it does not mislead, but the AI's correct onset flag was vetoed and I can only record it by writing a note on another flag.",
   "fix": "Let the paralegal 'Keep in notes' a rejected flag (it never goes in the letter). Add LOC-history change to the conflict kinds checked.",
   "acceptance_test": "lib08: the notes can list the record-11 onset line after a human keep; C1 raised as a conflict citing records 9 and 12."},
  {"severity": "minor", "title": "Keyboard stalls after saving a flag note",
   "evidence": "p10.out.txt:5 'after save ... tid btn-edit Edit note', :6 'after a 18 of 21 decided ... btn-edit' (no move, no message); j and n work (:7-8)",
   "why_it_matters": "The keyboard flow stalls on the flags where I write notes, which are the ones that matter. I had to work out that a does nothing there.",
   "fix": "After a note is saved, return focus to the flag row so a/d/j act on the item, or have a move to the next undecided item.",
   "acceptance_test": "E2E: e, type, Ctrl+Enter on a flag, then a -> focus is on the next undecided item."},
  {"severity": "minor", "title": "Default timeline order keeps a decided edited entry above earlier dates of service",
   "evidence": "p3-after-walk.txt:56-57 'January 16, 2026 / Dr. Alvarez, primary care' listed before the January 9, 2026 entries with '0 items need review'",
   "why_it_matters": "I check the chronology in date-of-service order, and an out-of-order row after review looks like a date error.",
   "fix": "Once nothing needs review, 'Needs review first' falls back to date order; or default to By date after all are decided.",
   "acceptance_test": "E2E: after editing and accepting entry 3, the timeline lists entries 1..9 in date order."},
  {"severity": "nit", "title": "Accident-date conflict shows an unrelated 'Quoted line' under record 7",
   "evidence": "p1-overview.txt:229-231 'Date of accident per intake form: 2026-01-19' then 'Quoted line from this record: New onset pain radiating to right arm ...'",
   "why_it_matters": "The second line is not the source of the date, so for a moment I thought the tool had quoted the wrong sentence.",
   "fix": "Drop the extra quoted line, or label it 'Entry quote for this record'.",
   "acceptance_test": "Conflict card for record 7 shows only the accident-date line or a labeled entry quote."},
  {"severity": "nit", "title": "One-line letter layout silently omits summary edits",
   "evidence": "p5-letter-oneline.txt line 5 quotes record 3 only; my edited summary (p4-letter.txt:12) is not in this layout",
   "why_it_matters": "The layout label says date, provider, quote, so this is by design, but an edit that disappears with no word about it is unsettling.",
   "fix": "Add a hint under the layout choice: 'summary edits are not shown in this layout'.",
   "acceptance_test": "Export UI shows the hint when one-line is chosen and any entry is edited."}
 ],
 "whats_right": [
  "Every Appendix A truth is present and correct: 73-day gap only, 01-09 vs 01-19 shown without choosing, both priors, PT plan vs discharge, $8,390.00 with $185 as a rate in the notes only.",
  "Each entry shows the summary beside the verbatim excerpt with its record number, and Open record shows the full raw record in one action; the edit keeps 'Original:' visible.",
  "The letter is clean plain text with D-002 cites, the D-062 total, my edit, nothing dismissed or pending; decisions survive reload; 23 items reviewed from the keyboard."
 ],
 "questions_for_chris": [
  "D-031 reinstated the draft paragraph and api.md puts it in the letter with '(provider, date)' cites, while D-002 says 'No short-cite mode'. Should an accepted paragraph carry quote + Bates like the chronology, or replace the chronology lines it covers?"
 ]}
```
