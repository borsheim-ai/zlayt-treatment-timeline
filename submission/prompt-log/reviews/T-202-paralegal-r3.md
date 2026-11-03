# T-202 round 3 (final): D-071 allow-list + fillable blank — paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** Round 3 fixes everything I raised in round 2, and the blank reads well in a demand letter. But the allow-list has a hole in the opposite direction, and it is the same class of error as my round 2 blocker: a wrong date printed in the date-of-service slot.

The words "visit date" and "seen on" are trusted even when they name a different visit (next, last, previous, initial), and in a visit note such a date overrides the note's own date. Take Appendix A's own ER note, with the follow-up written after the charge: "ER charges: $6,240, next visit date 01/16/2026." The build prints `Central ER discharge summary, January 16, 2026: $6,240.00`. The ER visit was January 9. The pre-T-202 build (bd72d5b) printed January 9 on the same text. letter_check passes the wrong line with 0 violations. In the visit-note probes (R1, R2, R17, R18, R19) it goes further: it reports the correct record-date line as the violation.

**What round 3 fixed (re-run on 973b542):**
- **Round 2 blocker (B1–B12, N11–N13).** Birth, injury/DOI, accident, onset, referral and order dates now give the blank in a bill. In visit notes they give the note's own date: B8 prints January 16 and B9 February 20 (probe_r3.out:221, :224).
- **Round 1 blockers.** These still hold: Posted-first ledgers print the DOS (T2, N1, N2, N24, N25), and the CMS-1500 "X and Y" list gives the blank.
- **Round 2 major ("service date not stated" above a quote that states one).** Gone. Every uncertain line now prints `date of service [__________] (statement dated X)`, which claims nothing (D-071 addendum).
- **Round 2 minors.**
  - "Trans Date" now gives the blank.
  - P10 and N17 periods print as ranges.
  - The notes now have a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section.
  - The not-stated string question is superseded by the addendum.
- **Corpus.** Letters for the sample, case_09, lib14 and lib10 are byte-identical to round 2 (UI download and in-process), and right. lib11's counted ledger lines print the blank.

**The blank, read as a demand letter.** `Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` works:
- it is as conspicuous as the Bates placeholder;
- it states nothing false;
- the statement date is labelled as a statement date;
- the notes list every blank.

I would fill it from the chart notes or a records request before sending. Two wording gaps remain (minor):
- The notes say "fill it from the quote" even when the quote has no date.
- The "treatment visits 1 through 14" line offers a single-date blank for what needs a range.

**Scope.**
- **Build:** `git archive 973b542` (tree 4c457a4b…) extracted to the session scratchpad (pr3_973b542/).
- **Pre-T-202 comparison:** a bd72d5b archive (pre_bd72d5b/).
- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true, local_mode true), http://127.0.0.1:7981.
- **Shutdown:** listener PID 24454 killed. `lsof` exit 1, `curl` 000.
- **Private values:** 1 <redacted> (a commit author line in `git show` output), not quoted.
- **Not graded:** Step 3 wording (separate card).

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 973b542 (git archive, tree 4c457a4bfb6c, extracted to session scratchpad pr3_973b542/); bd72d5b archive (pre-T-202, T-200) for the before/after on the new blocker. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7981 (health demo_mode true, local_mode true); listener PID 24454 stopped (lsof exit 1, curl 000). Cases: sample (sample tile), case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 (library tile); in-process letters for the same five plus three SYNTHETIC variants. Evidence: artifacts/review-evidence/T-202-paralegal-r3/. Step 3 wording not graded (separate card). Private values seen: 1 <redacted>.",
 "exercised": [
  "Read personas/paralegal.md, my round 2 review, D-071 + amendment + clarification + addendum (memory/ORCHESTRATOR_DECISIONS.md:84-93), board.py show T-202 (notes, handoff), git show 973b542 (service_date.py, export.py, store.py)",
  "From the archive: pytest test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '211 passed in 7.88s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
  "Every round 1 and round 2 bill text, loaded verbatim from my r2 probe files (P1-P10, T1-T3, N1-N25, B1-B12), plus 16 new R shapes, through the shipped store.charge_service_date (probe_r3.py -> probe_r3.out, 66 probes)",
  "Other-visit labels in visit notes and bills (R1, R2, R17-R23) and letter_check.charge_date_violations on the build's line vs the record-date line (probe_r3b.out); sample-styled punctuation variants C1-C7 (probe_r3c.out)",
  "SYNTHETIC sample variant 'ER charges: $6,240, next visit date 01/16/2026.' through the full letter on 973b542 (letters_dump_r3.out) and on bd72d5b (before_t202.out)",
  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, Step 3 cards logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); sample/case_09/lib14/lib10 letters cmp-identical to round 2",
  "In-process letters + notes, all_accepted and counted (letters_dump_r3.py): sample, case_09, lib14, lib10, lib11, synth_ambiguous_dos, synth_cms1500_two_dates, synth_sample_er_next_visit (letters/); diffed against round 2 (letters_vs_r2.out); read as a demand letter"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 4, "letter_dates_correct_on_corpus": 5, "blank_in_demand_letter": 4, "adjuster_credibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date",
   "evidence": "artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.out: SYNTHETIC sample variant (Appendix A record 2, ER note dated 2026-01-09, excerpt ending 'ER charges: $6,240, next visit date 01/16/2026.') prints 'Central ER discharge summary, January 16, 2026: $6,240.00' with 'date violations: []'. Same text on bd72d5b (before_t202.out) prints 'Central ER discharge summary, January 9, 2026: $6,240.00'. probe_r3b.out: R1 'Next visit date 01/30/2026, office visit charge $150.00.' (note 2026-01-16) -> 'Dr. Alvarez, primary care, January 30, 2026'; R2 'Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.' -> January 9; R17 'Visit charge: $150.00   Next visit date: 01/30/2026' -> January 30; R18 'Last visit date: 01/09/2026   Visit charge: $150.00' -> January 9; R19 PT discharge 2026-03-06 'Initial visit date 01/23/2026, discharge visit charge $185.00.' -> January 23; R23 bill 'next visit date 02/28/2026' after the figure -> February 28. probe_r3c.out: C4 'ER charges: $6,240, next visit date 01/16/2026.' and C7 'Follow-up visit date: 01/16/2026  ER charges: $6,240' -> January 16; C6 PT eval 01/23 'Next visit date: 01/27/2026   Charge per visit $185' -> January 27. Only a sentence break protects the line (C1, C3, C5 keep the record date). letter_check: for R1, R2, R17, R18, R19 the build's wrong line gives 'violations: []' and the record-date line gives 'charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-30)' (probe_r3b.out). Cause: service_date.py:43 _SVC_CORE accepts 'visit date' and 'seen' with no check of the word before them (next/last/previous/initial/return/follow-up), and a labeled date wins before the record-date fallback at service_date.py:375-376; the after-statement check runs only for bills (service_date.py:291), so a visit note accepts a date after its own date (January 30 on a January 16 note). evals/letter_check.py:190 _SERVICE_PHRASES carries the same 'visit date'/'seen' entries. tests/unit/test_t202_r3_allow_list.py has no next/last/previous/initial visit fixture (grep printed nothing).",
   "why_it_matters": "The brief and D-071 allow exactly two outputs for a charge line: a certain service date or the blank. 'January 16, 2026: $6,240.00' for an ER visit on January 9 is a wrong date of service on the largest charge in the sample case. The January 16 date belongs to the PCP follow-up, so the adjuster sees the ER bill dated to a different provider's visit. In a case with a disputed accident date (01/09 vs 01/19), any charge-date error is ammunition. It is a regression: the same text printed January 9 before T-202. And the eval now treats the correct date as the violation, so a later fix would be pushed back. Charges inside clinical notes are Appendix A's own pattern ('ER charges: $6,240.', 'Charge per visit $185.'), and checkout lines ('Visit charge ... Next visit date ...') are common in EHR visit summaries.",
   "fix": "In a dated encounter record (not a bill), the record's date is the visit. A labeled date there prints only when it equals the record's date; any other labeled date gives the record's date, or the blank with a note naming both. Everywhere (bills too), a visit or seen label preceded by next, last, previous, prior, initial, first, return, follow-up, scheduled or upcoming is not a service label. A date after the record's own date is never a service date in any record (extend the service_date.py:291 check beyond bills). Mirror both rules in letter_check with its own word list.",
   "acceptance_test": "Unit fixtures R1, R2, R17, R18, R19, R23 and C4, C6, C7 from probe_r3b.py/probe_r3c.py. Visit notes print the record's date (January 16, 2026; January 9 for C4/C7; January 23 for C6; March 6 for R19) or the blank, never January 30, 27 or 23 or the prior-visit date. R23 gives the blank. letter_check reports a violation on each of the build's current R1/R2/R17/R18/R19 lines and none on the record-date line. A SYNTHETIC golden or library case whose ER or visit note writes the next visit date after the charge with a comma prints the ER date."},
  {"severity": "minor",
   "title": "The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A)",
   "evidence": "probe_r3.out R15 'DOS Feb. 2nd, 2026 office visit charge $275.00.' gives the blank with reason=no_date and 'The line states no date of service.'. N20 'FL6 statement covers period FROM 060926 THROUGH 061226.' gives the same. N8 'Item 24A 06/24/2026 CPT 99204 $185.00.' gives 'The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting...'. Text at service_date.py:100. The blank is safe in all three; only the note is wrong.",
   "why_it_matters": "The note and the notes section are where I learn what to fill in. 'States no date' sends me to request a bill I already hold. Calling Item 24A 'possibly a birth or injury date' is wrong on its face to anyone who reads CMS-1500s, and it erodes trust in every other note.",
   "fix": "When a service label (DOS, 24A, FL6 / statement covers period) is present but its date is not parsed, use the written-date note naming the text as written ('The quote labels \"Feb. 2nd, 2026\" as the date of service; the code could not read it'). Add 24A as an inline label, and parse the six-digit FROM/THROUGH form under FL6.",
   "acceptance_test": "Fixtures R15, N20 and N8: no note says 'states no date' or 'not labeled'; each note quotes the labeled date as written (or N8 prints June 24 / July 8, N20 'June 9–12, 2026')."},
  {"severity": "minor",
   "title": "Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line",
   "evidence": "ui-lib11-notes.txt:39-41 '- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' The quotes are 'New patient exam charge $250.00', 'x-ray charge $180.00', 'treatment visits 1 through 14 charge $2,310.00' (no date). export.py:614 uses one sentence for every reason. The $2,310.00 line covers visits 1 through 14 (March 27 to May 29 in the chronology), but the letter offers 'date of service [__________]'.",
   "why_it_matters": "For a no-date line the only real action is to request a dated ledger, or to match the charge to the chart notes myself. 'From the quote' wastes a look. A 14-visit charge needs a range ('dates of service'), and a singular blank invites a single date that undercounts the treatment span.",
   "fix": "Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request a dated itemized bill'. Written-date reasons: 'the quote writes \"04/05/2026\"; confirm and fill'. When the quote counts visits ('visits 1 through 14', 'x 9 visits'), print 'dates of service [__________]'.",
   "acceptance_test": "lib11 counted notes contain no 'fill it from the quote' for the three Fennimoor lines; the $2,310.00 letter line reads 'dates of service [__________]'; the synth_ambiguous_dos note keeps 'fill it from the quote' with the date as written."},
  {"severity": "minor",
   "title": "Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints",
   "evidence": "ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'. The handoff lists the quote-span minor as not done.",
   "why_it_matters": "I cannot check the printed September 14 or June 9–12 against the quote under it without opening the record.",
   "fix": "Quote the bill line from its code or description through the figure.",
   "acceptance_test": "Every charge Source line in the 25-case letters contains a service word or code as well as the figure."},
  {"severity": "nit",
   "title": "A CMS-1500 claim-level 'dates of service from X to Y' prints the whole span on each coded line",
   "evidence": "probe_r3.out N10 'CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.' prints 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026' on both lines (round 2: the not-stated form).",
   "why_it_matters": "It is what the bill states, and so not a wrong date. But a new-patient visit (99204) shown across two weeks reads oddly to an adjuster. On a real CMS-1500 the span sits per line in 24A.",
   "fix": "Optional: on a CMS-1500 (not a UB-04 or a unit-count line), a claim-level span over several coded lines gives the blank with a note quoting the span.",
   "acceptance_test": "N10 lines print the blank with 'claim dates of service 06/24/2026 to 07/08/2026' in the note; P10 (9 units over the period) keeps 'January 23–March 6, 2026'."}
 ],
 "whats_right": [
  "Round 2 blocker closed: birth, DOI, accident, onset, referral and order dates never print. Bills give the blank, and visit notes keep their own date (B8 January 16, B9 February 20)",
  "The blank 'date of service [__________] (statement dated June 15, 2026)' is honest, pastes cleanly, and is listed under CHARGES WITHOUT A CERTAIN DATE OF SERVICE in the notes",
  "Corpus letters (sample, case_09, lib14, lib10) unchanged and right, including lib10 'June 9–12, 2026'; Posted-first ledgers and the CMS-1500 'and' list still right"
 ],
 "questions_for_chris": [
  "Still open from round 2, outside T-202: the export gate blocks a SYNTHETIC CMS-1500 coded line ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r3.out synth_cms1500_two_dates). Should this get its own card?"
 ]}
```
