# T-114 round 3 — paralegal-reviewer (Maria Delgado persona)

Verdict: **pass** (0 blockers, 0 majors, 3 minors, 0 nits). The round-2 major is closed: the gap card keeps "now 40 days (was 42)" with the before and after dates through Got it and a reload. The reviewed commit is e293daa. At e293daa the change lives in this browser only; at HEAD f7829c1 (which contains 93de5f2, T-127) the change is stored on the gap flag and survives a fresh browser profile. My reading of what I saw is below, with the commit each line applies to.

## What I ran
- Two app copies: `git archive e293daa` on 127.0.0.1:7897 (PID 27007) and `git archive HEAD` (f7829c1) on 127.0.0.1:7898 (PID 61750). Fixture backend, curated set, `ZLAYT_MODE=local`, scratchpad SQLite. Playwright, Chromium, 1440x900.
- Library case lib09 (Spanish, interpreter). Opened "1 date to confirm", chose "March 5, 2026 (2026-03-05)", clicked Confirm date. Script: `p8c-t114-confirm-gotit-reload.py`, output saved for both commits (`p8c-t114-confirm-gotit-reload-e293daa.out.txt`, `...-head.out.txt`).
- Clicked Got it, then reloaded and reopened the case.
- Fresh browser profile (no localStorage) on the confirmed case: `p8h-fresh-profile-confirmed-case.py`, outputs `p8h-fresh-e293daa.out.txt` and `p8h-fresh-head.out.txt`.
- API check of the flag: `p16-gap-change-api.py` (`p16-gap-change-api-e293daa.out.txt`: 0 flags with gap_change; `...-head.out.txt`: the gap flag carries gap_change with old_days 42, new_days 40, dates and the sentence).
- Rate row after Keep in notes (round-2 minor), read from the T-060 pass-4 walk on e293daa (`p5-after-walk-body-e293daa.txt` lines 476-493).
- Spot check that the lib09 lines in the gap card match the record dates (`Date: 03/05/2026` in record 4, Quillmere ED 2026-03-03, Consultorio 14/04/2026).

## Results
| Check | e293daa | HEAD f7829c1 |
|---|---|---|
| Confirm March 5 shows the notice | Yes: "A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). [Got it]" | Same |
| Gap card after confirm | "Gap recalculated after you confirmed record 4: now 40 days (was 42). Before: 42 days (March 3, 2026 to April 14, 2026). Now: 40 days (March 5, 2026 to April 14, 2026)." | Same |
| After Got it | Banner gone; card keeps the sentence and both dates | Same |
| After reload (same browser) | Card keeps the sentence and both dates; banner not repeated | Same |
| Fresh browser profile, same case | "Gap of 40 days" with no "was 42" sentence (browser-only) | Card keeps the sentence and both dates (server field) |
| Rate row kept in notes | One chip, "Accepted" (round-2 two-chip fault fixed) | not checked (same frontend) |

Screenshot: `artifacts/review-evidence/T-060-paralegal-pass4/p8c-01-after-confirm.png` shows the banner with Got it and the header "0 of 18 decided · 12 need review".

## Minors
**t1. (e293daa only) The "was 42" explanation exists only in this browser.** A second browser or profile opens the same case as "Gap of 40 days" with no hint that it moved from 42. Evidence: `p8h-fresh-e293daa.out.txt`: "gap card head: Gap of 40 days | Needs review | Gap of 40 days between March 5, 2026 ..." with "notice: None". HEAD closes this: the flag carries gap_change (`p16-gap-change-api-head.out.txt`) and the fresh profile shows the sentence (`p8h-fresh-head.out.txt`). Status: closed at HEAD by T-127 (93de5f2); not a fault at HEAD. Fix at e293daa: none needed if e293daa is not shipped; otherwise ship with HEAD. Test: fresh profile on the confirmed case shows "now 40 days (was 42)".

**t2. The notice states the new figure without the card's own caveat about record 4.** The notice says "now 40 days (was 42)". The same card says: "This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4 ... is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026)." Evidence: `p8c-t114-confirm-gotit-reload-e293daa.out.txt` (GAP CARDS after confirm). A paralegal who reads the notice alone takes 40 as settled, and the card says it may not be. This is the intake-form question already open since round 1 (question 1 below). Fix: the notice names the assumption, e.g. "now 40 days (was 42), counting record 4 as the start". Test: the notice text contains "counting record 4" or the card's caveat.

**t3. The rate row still says "needs review" after Keep in notes.** The round-2 two-chip fault is fixed (one chip, "Accepted"). The reason line still reads "Not counted: a rate, not a bill. rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review" under the Accepted chip, and the row says "Kept in the internal notes only; not in the letter or the total." Evidence: `p5-after-walk-body-e293daa.txt` lines 476-493. "Accepted" reads as counted. Fix: chip "Kept in notes"; drop "needs review" from the reason once kept. Test: after Keep in notes, no "Accepted" chip and no "needs review" text on the row.

## Right already
- The confirm, Got it and reload sequence keeps "now 40 days (was 42)" on the gap card with both before and after dates, on both commits.
- Got it removes only the banner, not the card's explanation.
- The date shows as a long date ("March 5, 2026") in the notice and on the card; the record quote stays in the record pane.

```json
{"card": "T-114", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 3; reviewed commit e293daa served on http://127.0.0.1:7897 (PID 27007); HEAD f7829c1 served on http://127.0.0.1:7898 (PID 61750), which contains T-127 93de5f2; fixture backend, curated set, ZLAYT_MODE=local; library case lib09 (Spanish, interpreter); 1440x900; no code changes",
 "exercised": [
  "git archive e293daa and HEAD into scratchpad copies; app started with artifacts/review-evidence/T-060-paralegal-pass4-serve.py under .venv/bin/python -I",
  "lib09 loaded from the library; 1 date to confirm opened; March 5, 2026 chosen and Confirm date clicked (p8c script, both commits)",
  "gap-change notice read after confirm: 'now 40 days (was 42)'; gap card read: before 42 days (March 3, 2026 to April 14, 2026), now 40 days (March 5, 2026 to April 14, 2026)",
  "Got it clicked; banner gone, card still carries the sentence",
  "page reloaded and the case reopened; card still carries the sentence and both dates",
  "fresh browser profile opened the confirmed case by its token (p8h script, both commits): e293daa shows no 'was 42'; HEAD shows it",
  "API GET of the gap flag on both servers (p16 script): e293daa has no gap_change; HEAD has gap_change with old_days 42, new_days 40, and the sentence",
  "rate row after Keep in notes read from the T-060 pass-4 walk output (p5 body text) and the chip count checked",
  "screenshot p8c-01-after-confirm.png read; record 4 and billing record dates checked against the excerpts shown in the record pane"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "gap_change_persistence": 4, "rate_row_clarity": 3},
 "findings": [
  {"severity": "minor", "title": "At e293daa the 'was 42' explanation exists only in this browser; closed at HEAD by T-127",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p8h-fresh-e293daa.out.txt: 'Gap of 40 days | Needs review | Gap of 40 days between March 5, 2026 ...' with 'notice: None'; p16-gap-change-api-e293daa.out.txt: 0 gap flags with gap_change; HEAD: p8h-fresh-head.out.txt shows 'Gap recalculated after you confirmed record 4: now 40 days (was 42)' and p16-gap-change-api-head.out.txt shows gap_change on f_gap_r4_r2",
   "why_it_matters": "A second browser or profile sees a 40-day gap with no sign it moved from 42. At HEAD the field is stored with the case, so this is closed there.",
   "fix": "Ship HEAD (T-127) or keep the browser copy as an interim only; the card does not say the change is browser-only.",
   "acceptance_test": "Fresh profile on the confirmed case shows 'now 40 days (was 42)' with both dates."},
  {"severity": "minor", "title": "Notice says now 40 days without the card's caveat about record 4 being paperwork",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p8c-t114-confirm-gotit-reload-e293daa.out.txt, GAP CARDS after confirm: 'This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4 ... is paperwork, not a visit, the gap would be 42 days'; screenshot p8c-01-after-confirm.png",
   "why_it_matters": "The notice reads as settled; the card says the start may not count. A paralegal reading only the banner would send 40.",
   "fix": "Name the assumption in the notice (counting record 4 as the start). The intake-form question is Chris's.",
   "acceptance_test": "Notice text includes the record 4 assumption."},
  {"severity": "minor", "title": "Rate row kept in notes still reads needs review under an Accepted chip",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p5-after-walk-body-e293daa.txt lines 476-493: chip 'Accepted'; 'Not counted: a rate, not a bill. rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review'; 'Kept in the internal notes only; not in the letter or the total.'",
   "why_it_matters": "Round-2 minor is half fixed: one chip now, but the chip says Accepted and the reason says needs review, so the row reads as counted.",
   "fix": "Chip reads Kept in notes; drop needs review from the reason once kept.",
   "acceptance_test": "After Keep in notes the row has no Accepted chip and no needs review text."}
 ],
 "whats_right": [
  "Confirm, Got it and reload keep 'now 40 days (was 42)' on the gap card with both before and after dates, on both commits",
  "Got it removes only the banner; the card keeps the explanation",
  "Dates in the notice and card are long dates (March 5, 2026); the verbatim record date stays in the record pane"
 ],
 "questions_for_chris": [
  "Is the lib09 record 4 intake form (formulario de admision) a treatment endpoint? The 40-day figure starts there while the card calls it paperwork (t2). Open since T-114 round 1.",
  "Should the T-127 server field ship before T-114 is called done, given that e293daa keeps the change in the browser only (t1)?"
 ]}
```
