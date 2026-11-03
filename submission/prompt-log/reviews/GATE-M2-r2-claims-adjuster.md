# GATE-M2 round 2 — claims-adjuster-reviewer (BI adjuster / defense adversary)

**Verdict: changes** (0 blockers, 2 majors, 2 minors).

Scope: commit 7cfdb0b, extracted with `git archive 7cfdb0b` into the session scratchpad (`tree_r2/`). HEAD moved to 56004f0 during the review. That commit is T-168 r2, which changes only JSON parsing. `git diff --stat 7cfdb0b -- app/backend/export.py app/backend/amounts.py app/backend/gaps.py` prints nothing, so every finding below also holds at HEAD.

I ran two servers from the tree:
- port 7874: `ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, scratch ZLAYT_DB. This is the operator's demo configuration.
- port 7875: the recorded-only set, no FIXTURE_SET. This shows how the sample reads on recorded model output.

Both servers (PIDs 4069 and 4123) were stopped with kill. Afterwards `lsof` shows neither port listening, and `curl /api/health` exits 7.

Evidence and probe scripts are in `artifacts/review-evidence/gate_m2_r2_adjuster/`.

**My round-1 blocker and major are closed.** I ran the sample and all 15 library cases and accepted every item one at a time (charges with their named confirm). Then I searched every letter for '$', 'per visit', rate, estimate, balance and paid.
- Every '$' sits on a BILLED CHARGES line or on the total line.
- The rates ($140, $120, $145, $155, $175, $400, $1,640/day, $21.50/mile, $150) appear only in the notes.
- No letter total is above the hand-checked golden total. Undercounts in lib04/05/06/09/11/12/15 are D-060 default-deny, which favours me, so I do not attack them.
- After I dismissed the first charge on the sample, lib01, lib10 and lib14, the dismissed figure is gone from the letter. Its provider leaves "Bills to request".
- When amounts are still pending, the letter has no BILLED CHARGES section.
- Entries whose quote states an amount return 422 CODE_CHECK_FAILED at accept, for example lib10 CMS-1500 '18500' and lib14 '24F 25500'.

**Deterministic checks.** I ran `evals.run --backend fixture`: grounding 1.000 (241), all flag types P/R 1.000, gap_28_not_flagged and gap_73_flagged true, must_not 0, letter_currency_outside_charges 0. ship_bar_met is False only because the fixture backend cannot measure determinism, unsupported-count or judge controls. QA's live 3-run in 7cfdb0b covers those.

I also ran `evals.library_report`. Must-flag misses: lib08 1/3, lib09 1/2, lib10 0/1, lib13 1/3, lib15 1/3. All are conflict types covered by scope cut 13 and the T-142 disclosure, or the lib10 gap endpoint (finding 3), or the lib15 K1 sentence. That sentence is shown in the T-143 "also in this record" list.

**Sample, on both the curated and the recorded set: I still cannot discredit it.**
- Both accident dates are quoted and no date is chosen.
- The 73-day gap is flagged and the 28-day interval is not.
- The new onset, missed PT, 2023 low back pain and the degenerative hedge are flagged.
- The ESI reads "recommended" and the MRI reads "protrusion".
- The total line is `Billed charges accepted from these records: $8,390.00` (D-062).

In the recorded run, e5 quotes "Patient reports missing 3 days of work." That is verbatim and not counted, so it is not a finding. The AI paragraph (POST /narrative, then accepted) restates the accepted summaries and adds nothing.

**New paths found (all in the firm's internal notes, none in the carrier letter):**
1. The "Amounts not totaled" rate line is a fixed template. It invents "/visit" and "visit count not stated". In lib15 it calls a 12-visit future-care estimate total "Rate $1,800/visit".
2. The accident-date conflict line in the notes recomputes "First recorded treatment" as the earliest date of ANY record. It ignores the flag's own first_treatment_date and its D-055 paperwork logic.
3. The notes' gap line drops the D-055 endpoint warning and the "possible gap" wording that the UI shows (lib10 43 vs 49 days; lib06 "Possible gap").
4. An entry accepted over the judge's "partially (ADDS_CAUSATION)" prints a mechanism sentence that is not in its printed Source quote (lib10 e1, lib11 e2). This is minor: the ladder ran and a human accepted.

**Still open from round 1 (not re-filed; carried as minors):**
- lib03 notes say "visit count not stated" although the record states 31 visits. This has the same root as finding 1.
- The lib03 plan (36) vs 31 visits conflict is missing.

**Not re-attacked (accepted debt):**
- 7c–7f;
- 13 (conflict coverage: lib08 LOC, lib09 side, lib13 cross-provider, lib15 low-speed vs violent);
- 13f;
- D-018 (speed not flagged).

```json
{"card": "GATE-M2", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 7cfdb0b (git archive into session scratchpad tree_r2/; HEAD moved to 56004f0 during review, export.py/amounts.py/gaps.py unchanged); app at http://127.0.0.1:7874 (fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB) and http://127.0.0.1:7875 (fixture, recorded set only); sample + all 15 library cases",
 "exercised": [
  "Read personas/claims-adjuster.md, reviews/GATE-M2-claims-adjuster.md, reviews/GATE-M2-round1-triage.md, D-059..D-062, SCOPE_CUTS 7c-7f/13/13f, every library input .txt and expected.json totals/flags",
  "env -u FIXTURE_SET LLM_BACKEND=fixture python -m evals.run --backend fixture on the 7cfdb0b tree: grounding 1.000 (241), flag P/R 1.000 all types, must_not 0, letter_currency_outside_charges 0, ship_bar_met False (fixture cannot measure live checks)",
  "python -m evals.library_report on the tree: must flags lib08 1/3, lib09 1/2, lib10 0/1 (gap rows wrong 1), lib13 1/3, lib15 1/3; accept-all totals ok",
  "run_all.py on :7874 for sample + 15 library cases: POST /api/cases, /run, poll /status, accept every entry/amount/flag one at a time (confirm when flagged), GET /export; letters and notes saved as cur_<case>_letter.txt / _notes.txt",
  "run_all.py on :7875 (recorded set) for sample: rec_sample_letter.txt / rec_sample_notes.txt",
  "grep of all 16 letters for $, per visit, rate, estimate, balance, paid, total, charge; totals_vs_golden.py letter total vs golden explicit_charges_total",
  "summary_vs_quote.py: summary words absent from the printed Source quote for every letter entry; read flagged blocks (lib08 MRI herniation is verbatim; lib10 e1, lib11 e2 add mechanism)",
  "grep of letters for severe/debilitating/significant/traumatic/acute/aggravation/intervening/referred/delay/caused (only verbatim record words found)",
  "dismiss_probe.py on sample, lib01, lib10, lib14: export with amounts pending (no BILLED CHARGES), then accept all and dismiss the first charge (figure gone from letter)",
  "narrative_probe.py on sample, lib01, lib03, lib07: POST /narrative, accept, export TREATMENT SUMMARY (sample only has a recorded paragraph; it restates accepted summaries)",
  "first_treatment_probe.py: store.export_case on the accepted sample case (read-only scratch DB) plus one added earlier-dated record, export.build_export notes line",
  "Read lib10/lib06/lib15/lib11/lib08 view JSON (flags, endpoint_warnings, conditional, amounts ladder) and app/backend/export.py _flag_line/_amounts_not_totaled, amounts.py classify, gaps.py",
  "Stopped servers PID 4069 and 4123 with kill; lsof shows no listener on 7874/7875; curl /api/health exit 7"
 ],
 "verdict": "changes",
 "scores": {"no_invented_facts": 3, "weaknesses_surfaced": 4, "billing_accuracy": 4, "letter_neutrality": 5, "source_cites": 4},
 "findings": [
  {"severity": "major",
   "title": "Notes 'Amounts not totaled' rate line is a fixed template that misstates the record: lib15 future-care estimate total printed as 'Rate $1,800/visit'; 'visit count not stated' printed where the quote states the count",
   "evidence": "artifacts/review-evidence/gate_m2_r2_adjuster/cur_case_lib15_conclusory_letter_mist_notes.txt: '- Record 6 (Sunderland Chiropractic, correspondence, narrative letter, January 11, 2027): \"Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).\" Rate $1,800/visit; visit count not stated. Request itemized ledger from Sunderland Chiropractic.' and the $150 line: 'Rate $150/visit; visit count not stated.' (record states 12 visits). Same template elsewhere: lib09 '\"4 sesiones a $400.00 por sesión.\" Rate $400; visit count not stated.'; lib10 '\"FL44 rate $1,640.00 per day\" Rate $1,640; visit count not stated.' (FL46 3 days); lib14 '\"8.7 miles at $21.50 per mile\" Rate $21.50; visit count not stated.'. Root: app/backend/export.py:499-500 'per = \"/visit\" if re.search(r\"per visit\", a[\"excerpt\"]...)' and 'body = f\"Rate {m}{per}; visit count not stated...' (suffix keyed on the whole excerpt, count text hard-coded); app/backend/amounts.py classify checks rate before estimate, so the parenthetical $1,800 after 'per visit' is class rate. View a3: kind rate, judge 'disagree' reason SHOULD_BE_ESTIMATE. Golden lib15 A3: 'Future care estimate (12 x 150), not incurred (D-019)'.",
   "why_it_matters": "The tool states a per-visit figure ($1,800) and a missing count that the records contradict. If the firm takes the future-care number from its notes into a demand, 12 x $1,800 = $21,600 against a stated $1,800, and I discount the whole future-medical claim as inflated. It also tells the firm to 'request itemized ledger' for care that has not happened. It does not reach the carrier letter and is not totaled, so it is major, not blocker.",
   "fix": "In code: (1) a figure in parentheses right after a rate expression (or equal to count x rate in the same sentence) is the extended amount: class estimate when the sentence carries 'estimated'/'future', else unclear with its reason; never rate. (2) Build the rate note from the amount's own clause: the unit from the words right after the figure (per visit/session/day/mile), and 'N stated' when the sentence states a count ('12 additional visits', '4 sesiones', 'FL46 3 days', '8.7 miles'). Say 'billed visit count not stated' only when no count is stated. (3) Future-care rates and estimates get 'Request cost estimate', not 'Request itemized ledger'.",
   "acceptance_test": "UT on lib15 notes: no line contains '$1,800/visit'; the $1,800 line reads as an estimate ('Estimate $1,800; not a billed charge'); the $150 line contains '12' and no 'visit count not stated'. Same UT on lib09 ('4'), lib10 ('3 days'), lib14 ('8.7 miles'): none says 'visit count not stated'. Library sweep: no notes line contains 'Rate $X/visit' where X is not the figure next to 'per visit' in its quote."},
  {"severity": "major",
   "title": "Notes accident-date conflict line recomputes 'First recorded treatment' as the earliest date of ANY record (pre-accident visit, intake form, paperwork), not the flag's first_treatment_date",
   "evidence": "app/backend/export.py:385-387: 'known = [r[\"date_iso\"] for r in v.records.values() if r.get(\"date_iso\")]' then 'tail += f\" First recorded treatment: {_long_date(min(known))}.\"'. By contrast app/backend/conflicts.py accident_date_conflicts computes first_treatment_date over encounters, re-anchors to the records that describe the collision (T-141 r2), and per D-055/T-123 'never state paperwork as the first treatment'. Repro: artifacts/review-evidence/gate_m2_r2_adjuster/first_treatment_probe.py on the accepted sample (token KOkGa8Uok2DsJha2RuPA8w). As run: '... The tool does not choose between the dates. First recorded treatment: January 9, 2026.' Plus one pre-accident record 'Dr. Alvarez, primary care, annual visit' 2025-11-03: '... First recorded treatment: November 3, 2025.' Plus an intake form dated 2026-01-02: '... First recorded treatment: January 2, 2026.' The flag's own UI text stays January 9. Library packets carry pre-accident records (lib11 record 1 2026-03-04, lib02 2021 history), so the shape is realistic. Demo mode cannot paste unrecorded text, so this is a code-path repro, not an end-to-end run.",
   "why_it_matters": "This is the one sentence D-017 lets the tool state about the accident-date conflict. In the notes it can name a pre-accident annual physical or an intake form as the 'first recorded treatment'. If the attorney repeats it, the demand says treatment began before the crash. I would use that to argue the condition pre-existed and that the chronology cannot be trusted. It is notes-only and needs a packet with an earlier-dated record, so it is major, not blocker.",
   "fix": "Render the notes tail from the flag's computed first_treatment_date and its paperwork alternative (the same sentence the UI shows). Never take min() over all records in export.py.",
   "acceptance_test": "UT: the sample case plus a pre-accident PCP record dated 2025-11-03 (no collision words) and, separately, plus an intake form dated 2026-01-02. The notes conflict line still ends 'First recorded treatment: January 9, 2026.' (or names the intake form as paperwork with the visit reading, as the flag does) and equals the flag's first_treatment_date."},
  {"severity": "minor",
   "title": "Notes gap line drops the D-055 endpoint warning and the conditional 'possible gap' wording the UI shows",
   "evidence": "lib10 UI flag f_gap_r8_r9: 'Gap of 43 days ... This gap starts at record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), which looks like paperwork, not a visit... the gap would be 49 days (July 8, 2026 to August 26, 2026).' Notes (cur_case_lib10_eob_ub04_cms1500_notes.txt:6): '- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), July 14, 2026) to record 9 (...)'. lib06 UI f_gap_r3_r5: 'Possible gap of 35 days ... No gap is counted here because record 4: Gannet and Moor Injury Clinic, billing statement (June 3, 2026) falls inside this span'. Notes: '- Gap: 35 days, May 13, 2026 to June 17, 2026: record 3 (...) to record 5 (...)'. Root: export.py _flag_line gap branch reads only days/from_date/to_date/evidence, never endpoint_warnings or conditional. Library report: lib10 'gap rows wrong 1', must flag G1 (49 days, records 7 to 9) unmatched.",
   "why_it_matters": "The attorney reads the notes, not the review screen. The notes give a 43-day gap measured from a claim form, where the last visit makes it 49 days. They also state a definite 35-day gap where the tool itself says the counted math finds none. I will measure from the last visit, so the firm's figure is wrong in the direction that understates my argument. The gap is still surfaced, so this is minor.",
   "fix": "When a gap flag carries endpoint_warnings or conditional, the notes line appends the same warning and alternative sentence (or says 'Possible gap') exactly as the flag explanation does.",
   "acceptance_test": "UT: lib10 notes gap line contains '49 days (July 8, 2026 to August 26, 2026)' and 'paperwork'; lib06 notes line for records 3-5 starts 'Possible gap' or carries the 'No gap is counted here' sentence."},
  {"severity": "minor",
   "title": "Entry accepted over a judge 'partially (ADDS_CAUSATION)' prints a mechanism clause that its printed Source quote does not contain; the notes keep no trace of the override",
   "evidence": "cur_case_lib10_eob_ub04_cms1500_letter.txt:3-5: 'June 9, 2026 — Rainhollow Fire-Rescue run report / Driver of a pickup struck at an intersection; patient states chest wall and left knee pain. / Source [Ex. __ / Bates __]: \"Pt states chest wall and left knee pain.\"'. cur_case_lib11_priors_and_ledger_letter.txt: 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' with Source '\"Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.\"'. View e1/e2: state needs_review, reasons ['JUDGE_PARTIAL'], judge reason_code ADDS_CAUSATION; code_checks summary_tokens_not_in_excerpt [] (the word check covers numbers/dates/side/negation only). The accept returned 200 with no warnings (cur_*_accept_log.json). Notes have no line for items accepted over a judge objection.",
   "why_it_matters": "I check each summary against the quote printed under it. A mechanism clause with no quoted support reads as the firm adding facts, even though the record itself has the sentence. The ladder did run and a human accepted, so this is minor.",
   "fix": "Either list 'accepted over the second check' items (item, judge reason) in the internal notes, or make the accept of a JUDGE_PARTIAL entry return a warning naming the unsupported clause, so the paralegal widens the quote or trims the summary.",
   "acceptance_test": "E2E: lib10, accept e1 as drafted. The response carries a warning naming the judge reason, and the notes list e1 under an 'accepted over the second check' line; or the export shows the quote widened to include 'Driver of a pickup struck at an intersection.'"}
 ],
 "whats_right": [
  "Carrier letters: across sample + 15 library cases, accept-all, dismiss and pending runs, every '$' is on a BILLED CHARGES line or the D-062 total line; no rate, estimate or dismissed figure prints.",
  "No letter total exceeds the hand-checked golden total; quotes that state money are held at accept with 422 CODE_CHECK_FAILED naming the figures.",
  "Sample (curated and recorded sets): both accident dates quoted, no date chosen, 73-day gap flagged and 28 not, hedges/'protrusion'/'recommended'/'patient states' intact, $185 and lost work days only in the notes."
 ],
 "questions_for_chris": []}
```
