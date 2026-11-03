# GATE-M2 — claims-adjuster-reviewer (BI adjuster / defense adversary)

**Verdict: fail** (1 blocker, 1 major, 2 minor, 1 nit).

Scope: `git archive 0c24f5f` extracted to the session scratchpad (`tree/`). I ran the app from that tree on spare port 7873
(`HOST=127.0.0.1 PORT=7873 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch>/app.sqlite3`; `/api/health` →
`"backend":"fixture","demo_mode":true`). I created and ran the sample case and two library cases (`case_lib01_er_only_then_gap`,
`case_lib03_truck_rear_end_chiro`), accepted every item, exported, and also dismissed charges and edited an entry to see what the tool did.
Evidence: `artifacts/review-evidence/gate_m2_adjuster/` (views, exports, dismissed-amount export, eval report) and probe scripts
`artifacts/review-evidence/gate_m2_adjuster_probe.py` and `gate_m2_adjuster_accept.py`. The server (PID 82007) was stopped; afterwards
`curl /api/health` returned nothing.

**Sample case: I could not discredit it.** I checked each item on my attack list:
- The two accident dates are flagged as a conflict ("The records disagree; the tool does not choose between them. First recorded treatment: January 9, 2026"). No delay figure is computed (`grep delay` on the export finds nothing).
- The 73-day gap is flagged with both endpoints and the day count. The 28-day interval is not flagged, and its dates stay visible.
- New onset, missed appointments, the 12-visit plan vs visit 9, the 2023 low back pain, the degenerative hedge and the patient's self-report are each flagged with a verbatim quote.
- The MRI stays a "disc protrusion" and keeps "may represent degenerative change". The injection is "recommended", not given.
- The total line is exactly `Billed charges stated in these records: $8,390.00`. The $185 rate and the 3 lost work days appear only in the internal notes.
- I found none of these words in the export: severe, debilitating, significant, herniation, traumatic, acute, failure to mitigate, non-compliant, aggravation, intervening, "referred to pain".

Note: the sample replays the **curated** fixture set. The library cases replay the recorded model output, and that is where the tool breaks.

**Where I would attack the package:** in the library cases the letter quotes per-visit rates, and it keeps quoting charges the paralegal dismissed. Both happen because the
extract prompt tells the model to pick sentences that carry the "charge" (`app/llm/prompts/extract_v1.md:12`). Nothing in code removes
amount sentences from an entry's summary or quote, or warns that an entry still quotes an amount after its charge is dismissed.

Edit probe: I added "Severe" to the e7 summary. The internal notes recorded the original and the new text, and the letter carries no edit marker (D-010 holds). The token code check
does not catch an added adjective, and the judge is unavailable in demo mode. This works as R-RV-3 specifies, so it is not a finding.

Deterministic check: `evals.run --backend fixture` on the recorded set gives grounding 1.000 (241), all four flag types precision/recall 1.000,
gap_28_not_flagged and gap_73_flagged true, must_not hits 0. ship_bar_met=False only because the fixture backend cannot measure the live
determinism, unsupported-count and judge-control checks. The eval refuses the curated set by design (D-029).

```json
{"card": "GATE-M2", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 0c24f5f (git archive into session scratchpad tree/); app at http://127.0.0.1:7873 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB); sample case + library case_lib01_er_only_then_gap + case_lib03_truck_rear_end_chiro",
 "exercised": [
  "Read personas/claims-adjuster.md, spec/SAMPLE_CASE_TRUTHS.md, Appendix A sample records, library inputs lib01/lib03 and their expected.json",
  "Started app from the 0c24f5f tree on port 7873; GET /api/health -> backend fixture, demo_mode true",
  "POST /api/cases {sample:true}, {library:case_lib01_er_only_then_gap}, {library:case_lib03_truck_rear_end_chiro}; POST /run; polled /status to ready (sample 9 entries/4 amounts/10 flags; lib01 6/2/3; lib03 7/3/5)",
  "GET /api/cases/{token}, /billing, /audit, /export (blocked 422 NOTHING_ACCEPTED before review)",
  "Accepted every entry, amount and flag one by one via /items/{id}/review; GET /export default, style=oneline, style=standard; read letter_text and internal_notes_text for all three cases",
  "Edited sample e7 summary to add 'Severe' (edits.summary), accepted it, exported; read EDITED ITEMS and /items/e7/trace",
  "Dismissed lib01 a1 ($3,915 charge) and a2 ($140 rate), re-exported letter (artifacts/review-evidence/gate_m2_adjuster/lib01_dismissed_amounts_export.txt)",
  "POST /narrative on sample (returned LLM_FAILED_AFTER_RETRIES after the edit; fails closed)",
  "env -u FIXTURE_SET LLM_BACKEND=fixture python -m evals.run --backend fixture (report copied to artifacts/review-evidence/gate_m2_adjuster/20261102T125917Z.md)",
  "grep of sample export for advocacy/defense-label words (0 hits) and for 'delay' (0 hits)",
  "Stopped server PID 82007 by kill; port 7873 no longer listening, /api/health no response"
 ],
 "verdict": "fail",
 "scores": {"no_invented_facts": 4, "weaknesses_surfaced": 5, "billing_accuracy": 2, "letter_neutrality": 3, "source_cites": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Per-visit rates reach the carrier letter through entry summaries and quotes (library cases)",
   "evidence": "lib01 export after accepting all items, letter_text: 'April 13, 2026 — Plumtree Physical Therapy, initial evaluation\\nCervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140.\\nSource [Ex. __ / Bates __]: \"Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140.\"' ; lib03 letter_text: 'Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. Charge per visit $120.' next to 'Discharged at maximum chiropractic benefit after 31 visits'. Same rate lines are classed rate/AMOUNT_RATE_NOT_TOTALED (view a2). Spec: R-CH-7 acceptance 'After accepting the $185 rate ... letter_text has no $185'; R-EX-8/D-019 'Rates ... appear only in the internal notes'. Cause: app/llm/prompts/extract_v1.md:12 'Choose the sentences that carry the treatment, findings, diagnosis, plan or charge'. Files: artifacts/review-evidence/gate_m2_adjuster/case_lib01_er_only_then_gap_after_accept.json, case_lib03_truck_rear_end_chiro_after_accept.json",
   "why_it_matters": "The letter prints a rate and a visit count next to a total that leaves both out. That invites 31 x $120 = $3,720 math the records do not support, and I would answer that the specials are undocumented and the chronology is padded. The sample passes only because its curated fixture leaves out the rate sentence; recorded model output does not.",
   "fix": "Keep amount-bearing sentences classed as rate/estimate/unclear/damages (and dismissed charges, see major) out of entry quotes and summaries before export. Do it in code, e.g. drop that sentence from the excerpt span and strip the clause from the summary, and leave the figure to the internal notes. Change the extract prompt so it no longer asks for 'charge' sentences.",
   "acceptance_test": "UT/E2E: for lib01 and lib03 with every item accepted, letter_text contains neither '$140' nor '$120' nor 'per visit'. Same on any case whose amounts include a non-charge class. A golden must_not regex '(?i)per visit' applies to letter_text across the library."},
  {"severity": "major",
   "title": "A dismissed charge is still quoted in the letter, and the notes contradict it",
   "evidence": "lib01: dismissed a1 ($3,915 charge) and a2 ($140 rate), re-exported. letter_text still reads 'Diagnosis of cervical strain; ... follow up with primary care in 1 week; ED charge $3,915.' and 'Source ...: \"... ED charge: $3,915.\"' and 'Charge per visit $140.', with no BILLED CHARGES section. internal_notes_text: 'BILLS TO REQUEST ... Dunmarrow Fire-Rescue run report; Marrowgate General ED; Plumtree Physical Therapy.' and 'AMOUNTS NOT TOTALED - none'. File: artifacts/review-evidence/gate_m2_adjuster/lib01_dismissed_amounts_export.txt",
   "why_it_matters": "The paralegal dismissed the figure, but the carrier letter still states it. The firm's own notes then say to request that bill. A letter that quotes a charge it neither totals nor stands behind lets me attack the specials. The gate bar says dismissed items never export.",
   "fix": "When an amount is dismissed (or is not a charge), the entry that quotes it must lose that sentence and clause in the letter, or the review step must block or warn ('this entry still quotes $3,915, which you dismissed') before export.",
   "acceptance_test": "E2E: on lib01, accept all entries, dismiss a1. letter_text contains no '$3,915' (or export returns a named blocker or warning naming e2), and the notes do not both list the provider under Bills to request and quote its charge in the letter."},
  {"severity": "minor",
   "title": "lib03 internal note says the visit count is not stated; record 6 states 31 visits",
   "evidence": "lib03 internal_notes_text: 'Record 3 (Thimbleby Chiropractic, initial exam, April 9, 2026): \"Charge per visit $120.\" Rate $120/visit; visit count not stated. Request itemized ledger from Thimbleby Chiropractic.' Record 6: 'Discharged at maximum chiropractic benefit after 31 visits.' Golden totals.unclear_items: 'rate $120/visit; billed visit count not stated (36 planned, 31 attended); needs review'. The lib01 note does carry '(8 planned)'.",
   "why_it_matters": "The tool's own sentence is wrong about the records, and it drops the plan/attended context the firm needs to scope the ledger request. It only reaches the do-not-send notes, so the carrier never sees it.",
   "fix": "Write the note as 'billed visit count not stated' and include planned/attended counts when a record states them, the same way the sample does ('12 planned; discharged at visit 9').",
   "acceptance_test": "UT on lib03: the notes rate line contains 'billed visit count not stated' and '31' and '36' (or '3 visits per week for 12 weeks'), and never the bare 'visit count not stated.'"},
  {"severity": "minor",
   "title": "lib03 chiropractic plan (36) vs discharge after 31 visits is not raised as a conflict",
   "evidence": "lib03 flags: only f_gap_r6_r7, f_r7_1, f_r7_2, f_r7_3. Golden flag C1 (level should): 'Plan of 36 visits (3 per week for 12 weeks) vs discharge after 31 visits; shown side by side, not resolved.' The sample's analogous f_cx1 (12 planned vs discharged at visit 9) is raised.",
   "why_it_matters": "A plan-vs-actual discrepancy is the first thing I check on a chiro-heavy soft-tissue claim. The plaintiff's side should see it before I raise it. It is a 'should' flag, so it is not a hidden-weakness blocker.",
   "fix": "Extend the code conflict candidate for plan-vs-discharge to 'N visits per week for M weeks' plans and 'after K visits' discharges, or list the miss in SCOPE_CUTS.",
   "acceptance_test": "Library report: lib03 C1 matched (conflict citing records 3 and 6), or a SCOPE_CUTS row naming the uncovered plan pattern."},
  {"severity": "nit",
   "title": "lib01 record 3 (post-gap visit) is missing from the timeline, and the tray's reason contradicts A-109",
   "evidence": "lib01 view: tray e3 state rejected, reasons ['FIXTURE_MISS'], why 'The demo has no recorded AI answer for this step'. memory/ASSUMPTIONS.md A-109 says record 3 keeps a recorded live failure (LLM_FAILED_AFTER_RETRIES). The letter goes from 'February 14, 2026 — Marrowgate General ED' to 'April 13, 2026 — Plumtree Physical Therapy' with no referral visit. The notes do list 'Record 3 ... — no entry'.",
   "why_it_matters": "This is documented and surfaced, so not a hidden weakness. But a letter sent as-is shows a 58-day jump from ED to PT with no referral, and the gap flag cites a record the letter leaves out. The tray reason also misstates why the record has no entry.",
   "fix": "Make the tray why-text name the recorded live failure, not a fixture miss (or align A-109).",
   "acceptance_test": "lib01 view tray e3 why names the recorded extract failure consistently with A-109."}
 ],
 "whats_right": [
  "Sample accident date: shown as a conflict with both dates quoted; no date chosen and no delay computed; 'first recorded treatment: January 9, 2026' only.",
  "Sample hedges and qualifiers survive: 'disc protrusion', 'may represent degenerative change; correlate clinically', 'without loss of consciousness', ESI 'recommended', 'patient states'.",
  "Sample total line is exactly 'Billed charges stated in these records: $8,390.00'; the $185 rate, the lost work days and the ESI cost request appear only in the internal notes."
 ],
 "questions_for_chris": []}
```
