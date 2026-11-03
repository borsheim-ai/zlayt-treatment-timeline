# GATE-M3M4 paralegal review (Maria Delgado, senior PI paralegal)

Pinned commit f6d5c19 (`git archive f6d5c19`, extracted to the session scratchpad). Rules applied: D-075 (blockers only) and the D-073 fallback.
Demo-mode server on port 7931 (`ZLAYT_MODE` unset, fixture backend, no `ENABLE_LIVE`, health `demo_mode:true`). The demo refuses lib10 and lib11 text
(409 `demo_mode_unsupported_input`, same as the public demo), so those two ran on a second archive server on port 7932 with `ZLAYT_MODE=local`
and the same fixtures. Both servers were stopped by PID afterward (curl on 7931 and 7932 returns 000, no listener). No private value was handled; none is quoted here.

**Verdict: pass. No blockers.**

## What I checked

**Sample case, record to letter, timed.** Draft step 1.3 s. A scripted keyboard run (A to accept every item) reached the finished letter in 17.4 s total
(19 timeline items, 4 bill amounts). That is script speed, not human speed; the point is that nothing stalls.
- Records: 9 found, all dates read correctly (Jan 9 twice, Jan 16, Jan 23, Feb 20, Mar 6, May 18, May 29, Jun 12).
- Total: letter line reads `Billed charges accepted from these records: $8,390.00` (wording is D-062 / R-EX-8, not the older D-019 text). ER $6,240 plus MRI $2,150 = $8,390. Verified by hand.
- PT rate: `$185` is on the Step 3 "Never counted" list as a rate. No PT total anywhere in the letter. Internal notes say
  `Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.` "Missing 3 days of work" is not a charge and sits under Damages mentions.
- Gap: 73 days, March 6 to May 18, with both dates and both records. The 28-day interval (Jan 23 to Feb 20) is not flagged.
- Conflict: accident-date flag shows 2026-01-09 (EMS, ER) against "Date of accident per intake form: 2026-01-19" (record 7), "the tool does not choose between the dates". PT plan "12 visits" against "Discharged from PT after two missed appointments" is flagged. Both priors (record 3 low back 2023; record 8 degenerative wording) are flagged with excerpts.
- Every letter line has the long-format date, the provider as written, a summary, and a verbatim quote. I compared all 9 quotes with `evals/golden/sample.txt`. Each is an exact substring.
- Every charge line prints `date of service [__________] (record dated X)`, the D-073 fallback format. Two blanks plus `[Ex. __ / Bates __]` on each source line. After you fill them in, the letter is sendable.
- Letter downloaded as .txt: same text as the screen. No HTML, markdown, "verified" or other UI words. Flags, notes and "Bills to request" appear only in the internal block.
- Bates panel: Exhibit A, prefix RIV, start 1 turns record 2 into `[Ex. A / Bates RIV0002]`, MRI into RIV0008. Correct mapping.
- Edit, dismiss, pending, reload: I edited the record 3 summary, dismissed one flag, left one flag on "Decide later", and reloaded the page mid-review. The answer counter carried on from where I was. The letter holds my edited wording. Notes show EDITED ITEMS with the original and the new text, FLAGS DISMISSED with the dismissed flag, and PENDING ITEMS NOT INCLUDED with the undecided one. The letter was identical after a second reload.

**case_09 (golden, demo server).** The billing statement entry came up with Yes unavailable (it holds a dollar figure), so I dismissed it; the $275 still counts from Step 3. Letter: 4 visit/phone entries and `Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00`; total $275.00. Notes: gap of 56 days, Feb 2 to Mar 30; the statement and phone note did not split the gap. The Feb 2 service date inside the statement sentence is not used for the letter date, so there is no wrong date.

**lib10 (local server).** Letter charges are the four UB-04 line charges, $4,920.00, $2,105.00, $386.50 and $712.00, total `$8,123.50`. That equals the hand sum. Not in the total: the $1,640 rate, the 0001 repeat of $8,123.50, and every EOB figure; the CMS-1500 amounts are not in the total either. All of these are in the notes as not totaled (the CMS-1500 figures are the exception, see below). Charge lines print the blank with `(statement dated June 19, 2026)`.

**lib11 (local server).** I ticked the two confirm boxes the app requires before the three ledger lines could be counted. Letter charges: ED $3,260.00, new patient exam $250.00, x-ray $180.00, visits 1 to 14 $2,310.00. Total `$6,000.00`, which matches `expected.json` and my hand sum. The $2,740 ledger total, the $300 payment, the -$274 adjustment and the $2,166 balance are in the notes, not in the total. Gap 35 days (Apr 24 to May 29). The 28-day interval (Mar 27 to Apr 24) is not flagged. The intake-form "Prior accidents: No" and the 2019/2022 history are both quoted in a conflict flag, and the tool does not say which is right.

I read the letter lines for all four cases against the raw records. Every quote is a substring of its record. I found no wrong date, no wrong amount, and no total that disagrees with the hand sum.

## Not blockers (D-075: for SCOPE_CUTS, not rated)
- lib10 notes say `Gap: 43 days, July 14, 2026 to August 26, 2026` from a CMS-1500 claim form. The review card carries the warning "looks like paperwork... the gap would be 49 days (July 8...)", but the notes line drops that sentence. This is the D-055 design, and earlier reviews (T-116 paralegal r4, GATE-M2 adjuster) already rated it minor or nit.
- lib10 letter has a chronology line `June 19, 2026 — ... UB-04 itemized bill` (the statement date) whose summary ends with the fragment "room". It is labelled a bill and its quote shows the 06/09 to 06/12 period.
- lib10: the card says the notes will name the CMS-1500 amounts so the paralegal can request the bill; after dismissing record 8 the notes list the record as dismissed but print none of its figures.
- lib10 EMS and lib11 EMS lines were disputed by the second check and accepted after I ticked "I read this line myself". The letter's Source quote then omits the sentence the summary uses ("struck at an intersection", "struck from behind"). The human gate worked as designed; widening the highlight would fix it.

## Evidence (under artifacts/review-evidence/)
`GATE-M3M4-paralegal-sample-letter.txt`, `-sample-notes.txt`, `-sample-letter-bates.txt`, `-sample-cards.txt`, `-sample-bills.txt`, `-sample2.out` (timing), `-case09-letter.txt`, `-case09-notes.txt`, `-lib10-letter.txt`, `-lib10-notes.txt`, `-lib11-letter.txt`, `-lib11-notes.txt`, `-edit-letter.txt`, `-edit-notes.txt`, screenshots `GATE-M3M4-paralegal-0N-*.png`, probe scripts `GATE-M3M4-paralegal-*.py` and `gate_m3m4_lib.py`, server logs.

```json
{"card": "GATE-M3M4", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive f6d5c19; demo-mode app on :7931 (sample, case_09), local-mode archive server on :7932 (lib10, lib11, demo refuses them); D-075 blockers only, D-073 fallback",
 "exercised": [
  "git archive f6d5c19 into scratchpad; started demo server (ZLAYT_MODE unset, fixture backend) on 7931; /api/health showed demo_mode true",
  "Playwright: sample case from Open the sample case to the finished letter, keyboard A on every card, 17.4 s scripted total, draft step 1.3 s",
  "Read every Step 2 card and Step 3 amount for the sample against evals/golden/sample.txt and spec/SAMPLE_CASE_TRUTHS.md (total 8390, PT rate not totaled, gap 73, 28-day not flagged, 01-09 vs 01-19 conflict, plan vs discharge, two priors)",
  "Downloaded letter and notes as .txt, diffed against the screen text, grepped for HTML, markdown and UI words",
  "Set Bates panel (Ex A, prefix RIV, start 1) and checked the per-record mapping in the letter",
  "Edited the record 3 summary, dismissed one flag, left one flag undecided, reloaded mid-review and again at the letter; checked the letter and notes",
  "case_09 via POST /api/cases (golden text accepted) and the UI; letter and notes read against the raw record",
  "lib10 and lib11 on a local-mode archive server (demo returned 409 demo_mode_unsupported_input); drove all items, compare and separate boxes ticked where required; letters and notes read against the raw records and expected.json",
  "Hand arithmetic: 6240+2150=8390; 4920+2105+386.50+712=8123.50; 3260+250+180+2310=6000",
  "Stopped both servers by PID (53027, 59925); curl on 7931 and 7932 returns 000"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "totals_correct": 5, "dates_correct": 5, "letter_sendable_after_blanks": 5},
 "findings": [],
 "whats_right": [
  "Every charge line prints the same fillable blank with the statement or record date in parentheses, and no case printed a service date the records do not state.",
  "Totals match the hand sums on all four cases ($8,390, $275, $8,123.50, $6,000); the $185 rate, the 0001 repeat, EOB and ledger totals never enter a total.",
  "Edits, dismissals and undecided items survive reload and show up correctly in the notes (original kept, dismissed listed, pending excluded from the letter)."
 ],
 "questions_for_chris": []}
```
