# T-144 review: "Also in this record, not in an entry (n)" (legal-nurse-reviewer)

Verdict: pass (0 blocker, 0 major, 2 minor, 1 nit).

Exercised at HEAD d34182b (`git archive HEAD` into the scratchpad, fixture backend, curated set, ZLAYT_MODE=local, own DB, port 7968, stopped by PID 37299). Library cases lib09, lib14 and the sample were driven with Playwright. The full library (15 cases) was scanned through the API. The author's e2e file `tests/e2e/test_uncovered_ui.py` was run against my server (7 passed).

- Collapsed by default: on lib09 (5 toggles), lib14 (4) and the sample (3), every list was hidden on load and every toggle read `aria-expanded=false`. Each toggle count equals the API's `records[].uncovered[]` total for that entry's records.
- Verbatim: every listed sentence equals the record text sliced at the API offsets (offsets are case-global, so `start - char_start`). 8 of 8 on lib09, 7 of 7 on lib14, 3 of 3 on the sample. OCR slips are kept as written ("03/O5/2026", "Next visit 1O/2O"). The UI shows no kind tags and no subjective/objective labels.
- One-click jump: all 18 sentences across the three cases open the record modal with exactly one highlight, and the highlighted text equals the sentence. Clicking a list item never alters an entry's summary or quote.
- Keyboard: the toggle is a `<button>`, and Enter and Space both toggle it. Tab runs from the toggle through Accept, Edit and Dismiss to the jump button. The jump's accessible name is "Show in record 1: Hx obtained via patient's son, who interpreted.". Enter opens the modal on the highlighted sentence, Esc closes it, and focus returns to the jump button. The focus outline is 2px solid.
- 390px wide: no sideways scroll on any of the three cases. The toggle is 44px tall and inside the viewport. Jump buttons are at least 36px tall, no text overflows, and the modal highlight is correct.
- Letter and copied text: after export, the letter pane contains no uncovered sentence and no list controls. The `GET /export` `letter_text` contains none of the 3, 8 or 7 sentences. The clipboard, after the app's "Copy anyway" confirm, contains none of them on the sample, lib09 or lib14.
- Internal notes text on the sample holds 3 of the 3 uncovered sentences, and one more on lib09 and lib14 each. These are the same sentences quoted as flag evidence, which is the existing flags contract. The list's own note says only "They are not in the letter".
- Useful or noisy: collapsed, the list costs only a short link in the entry's head line. Open, it holds 1 to 4 sentences per entry. The sentences are the ones I flagged at GATE-M2: "Pain 5/10.", "Accidentes anteriores? Si [ ] No [X].", "Patient reports low back pain in 2023, resolved.", the patient-stated mechanism, and interpreter attribution. In lib15 it also holds "Prognosis: guarded." and "The services were necessary and the charges reasonable.", which a chronology must not absorb and which are left out of the letter.
- About 3 of the 15 sentences on lib09 and lib14 are provenance or heading noise ("Re-examination.", "OCR of scanned CMS-1500.", "Next visit 1O/2O."). That is tolerable behind a collapsed link.

Not covered: the Dismiss-then-refresh path was only partly probed. The Dismiss click on a verified entry left its state unchanged, so I could not see the list change on dismissal. The quote-change refresh is covered by the author's e2e (passed). No library case has a multi-record entry that also has uncovered sentences, so the "Show in record N" labels are untested with real data. Medical opinion (prognosis, permanency, necessity) is not given by the UI. Visual design and code structure are outside my lens.

```json
{"card": "T-144", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD d34182b via git archive in scratchpad t144r1; app http://127.0.0.1:7968 (fixture backend, curated set, ZLAYT_MODE=local); cases lib09, lib14, sample, plus API scan of lib01-lib15; app/frontend/uncovered.js and uncovered.css",
 "exercised": [
  "git archive HEAD copy; app started with LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local on port 7968 with a scratchpad DB; stopped by PID 37299 (curl afterwards returned 000)",
  "python3 tools/board.py show T-144 (AC and handoff read)",
  "tests/e2e/test_uncovered_ui.py against my server: 7 passed",
  "Playwright on lib09, lib14, sample: per-entry toggle count vs API uncovered totals; all lists hidden on load, aria-expanded=false",
  "Verbatim check of every uncovered sentence against record text at API offsets (8, 7, 3; 0 mismatches)",
  "Jump click on all 18 sentences across the three cases: modal opens, exactly one highlight, highlight text equals the sentence",
  "Keyboard-only on lib09 r1: Enter and Space on the toggle, Tab order, aria-label on the jump, Enter opens the modal, Esc closes it, focus returns to the jump, focus outline",
  "390x844 viewport on all three cases: no horizontal scroll, toggle 44px tall, jump buttons at least 36px, no text overflow; screenshots lib09_390.png and lib09_390_modal.png viewed",
  "Export on sample, lib09 and lib14: letter pane, GET /export letter_text and notes text, and the clipboard after the Copy anyway confirm, each checked for the uncovered sentences",
  "API scan of all 15 library cases for records with uncovered sentences but no entry row",
  "lib15 per-entry toggle counts and verbatim lists (including Prognosis and necessity sentences)",
  "Dismiss probe on lib09 (inconclusive: state unchanged)",
  "personas/legal-nurse.md and memory notes from T-143 and GATE-M2 read first"],
 "verdict": "pass",
 "scores": {"verbatim_no_inference": 5, "collapsed_by_default": 5, "one_click_to_highlight": 5, "keyboard_and_390px": 5, "never_in_letter_or_copy": 5, "useful_not_noisy": 4, "coverage_of_unlisted_sentences": 3},
 "findings": [
  {"severity": "minor", "title": "Sentences of a record with no entry row are not listed anywhere",
   "evidence": "case_lib01_er_only_then_gap record 3 (Quarrington, the first visit after the 44-day gap) has no entry (entries e1, e2, e4, e5, e6) but API records[2].uncovered holds 3 sentences: 'Neck pain 5/10 with new left arm tingling.', 'Patient states she could not get an earlier appointment because the clinic was closed.', 'Refer to physical therapy.'. uncovered.js attaches the list only to an entry row, and uncovered-summary count on the page is 0. API scan: 3 of 66 uncovered sentences across the library are on a record with no entry. The page does carry a tray notice ('did not produce something you can use. They are not in the timeline and will not be in the letter. Open the record to read it yourself.') with 'Open record 3', and the causation flag quotes the first sentence. The patient-stated reason for the delay and the PT referral appear nowhere on the page.",
   "why_it_matters": "A whole record missing from the timeline is the largest omission. The tray tells the user to open the record, so the omission is disclosed, but the user must hunt for sentences the list would otherwise show in one place.",
   "fix": "Show the record's uncovered[] under the tray item for that record (same collapsed list, same jump), or give the tray item the count.",
   "acceptance_test": "In lib01 with the fixture backend, the tray item for record 3 shows 'Not in an entry (3)' or equivalent, verbatim, with jumps to the highlighted sentences."},
  {"severity": "minor", "title": "Letter-pane wording 'They are not in the letter' is true, but internal notes can repeat the same sentence",
   "evidence": "Sample export: GET /export internal_notes_text contains 'Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.' and 'Date of accident per intake form: 2026-01-19.', all listed as 'not in an entry'. They are flag evidence (existing contract). Note text under the list in uncovered.js: 'Sentences from this record that no entry quotes. They are not in the letter. To use one, add it by hand or change the quote.'",
   "why_it_matters": "A paralegal who sees a sentence in both places may take the note as a contradiction. The statement is accurate for the letter; 'in the letter' is not the same as 'anywhere in the export'.",
   "fix": "Say 'They are not in the letter or its source entries' or add 'a flag may quote one in the internal notes'.",
   "acceptance_test": "The note text on the sample's record 3 list states the flag possibility, or the sentence is marked 'also quoted by a flag'."},
  {"severity": "nit", "title": "Toggle count mixes records in a multi-record entry under a singular heading",
   "evidence": "uncovered.js: heading is 'Also in this record, not in an entry (n)' where n sums every record of the entry; the items show 'Show in record N' only when the entry spans more than one record. lib15 e7 spans r7 and r8, but neither record has uncovered sentences, so the labels were not exercised with real data.",
   "why_it_matters": "Minor wording mismatch only.",
   "fix": "Use 'Also in these records' when more than one record contributes.",
   "acceptance_test": "A fixture entry spanning two records with uncovered sentences shows the plural heading and per-record jump labels."}
 ],
 "whats_right": [
  "Every uncovered sentence is shown exactly as written (OCR slips, Spanish, 'Pain 5/10.') with no tag, kind label or filter, and each jump highlights exactly that sentence.",
  "Collapsed by default behind a head-line link; keyboard path, focus return and 390px layout all work.",
  "The list never reaches the letter pane, the letter_text or the clipboard."],
 "questions_for_chris": []}
```
