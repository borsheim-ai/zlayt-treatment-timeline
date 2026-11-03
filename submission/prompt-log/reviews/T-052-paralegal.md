# T-052 paralegal review

Verdict: pass (no blockers or majors). Validator passes; expected.json answers recompute by hand for lib01, lib05, lib06 (and lib03/04 gap math). Packet identifiers do not overlap the four sources I could fetch. Five minors and one nit concern a rate-vs-count edge case, a mis-typed causation flag, one unflagged PT shortfall, thin record formats and two sources I could not open.

```json
{
 "card": "T-052",
 "persona": "paralegal-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "evals/library/case_lib01..07 (.txt + .expected.json); research/case-library-sources.md; research/validate_library.py; no running app (data/eval card)",
 "exercised": [
  "python3 tools/board.py show T-052 (AC1-3 read)",
  "python3 research/validate_library.py -> 'golden OK: 17 cases (16 synthetic), 85 must_nots ... all stress types covered' and 'identifier check: ok (7 packets, 26 denylist terms)'",
  "curl -sL (browser UA) of 6 source URLs into artifacts/review-evidence/T-052-src/: S1 rmdlaw 200, S3 oklahomalawyer 200, S4 plasticsurgerypractice 200, S6 thompsoncoe 200; S5 valawyersweekly 403 and S7 rissman 403 (not verifiable by me)",
  "artifacts/review-evidence/T-052-paralegal-srccheck.py: capitalised-word and number overlap, each packet vs its source (S1/S3/S4/S6); only generic words (Date, Home, Chiropractic, Insurance, Source, Patient, Revision); 0 numbers",
  "artifacts/review-evidence/T-052-paralegal-scan.py: SYNTHETIC first line in 7 of 7 packets; synthetic:true in 7 of 7 JSON; 6-word phrase overlap of all 7 packets vs the 4 fetched sources: 0 hits",
  "hand-checked expected.json for lib01, lib05, lib06 (gap day counts, totals, amounts) and read lib03, lib04, lib07 flags: lib01 44d / $3,915 correct; lib05 49d, 119d, 26d near-miss unflagged, $38,420+$6,150=$44,570 correct, $175 rate not totaled; lib06 35d and 56d, billing statement (06-03) excluded from gap endpoints, 2,880+1,100+450+2,400=6,830, balance/adjustment/amount-due left unclear (no double count) correct; lib04 273d correct"
 ],
 "verdict": "pass",
 "scores": {
  "packet_realism": 3,
  "expected_json_correctness": 5,
  "source_mirroring_no_identifier_copy": 5,
  "synthetic_labelling": 5
 },
 "findings": [
  {
   "severity": "minor",
   "title": "lib03: per-visit rate left unclear although the packet states 31 visits at discharge",
   "evidence": "evals/library/case_lib03_truck_rear_end_chiro.txt record 6 'Discharged at maximum chiropractic benefit after 31 visits' and record 3 'Charge per visit $120'; expected.json A2 note 'Rate, not a charge: 36 visits planned, 31 attended; no visit count billed.' total stays 7500",
   "why_it_matters": "Checklist 12 says the rate is excluded 'unless the visit count is stated'. Here a count is stated (attended, not billed). Not totalling is the safe call and matches D-019, but the packet now sets a precedent that 'attended' is not 'billed' that the spec does not say. A paralegal would want the reason line to show 31 x $120 is a candidate she can confirm against the ledger, without the tool computing it.",
   "fix": "Add a one-line rule to the golden README or REQUIREMENTS (stated attendance count is not a billed visit count) so the packet is not just the author's judgment; keep total at $7,500.",
   "acceptance_test": "README/REQUIREMENTS grep finds the rule text; lib03 total remains 7500 and no value 3720 appears in letter or notes."
  },
  {
   "severity": "minor",
   "title": "lib06: attorney referral / letter-of-protection is typed 'causation'",
   "evidence": "case_lib06 expected.json K1 type causation level should, evidence 'Patient referred by attorney', summary 'Attorney referral and letter-of-protection treatment (internal notes only...)'",
   "why_it_matters": "Referral source is a treatment-provenance and billing point, not a causation statement. Using the causation type makes the golden score a tool that raises 'causation' on every attorney-referred note, and a paralegal reading the internal notes sees it filed under the wrong heading.",
   "fix": "Use a type that fits (or tolerated with a note) instead of causation, or keep it only as tolerated.",
   "acceptance_test": "lib06 has no flag of type causation whose only evidence is a referral or LOP sentence."
  },
  {
   "severity": "minor",
   "title": "lib05: PT stops at visit 12 of 16 planned with no discharge record and nothing flags it",
   "evidence": "case_lib05 record 5 'Plan of care: 16 visits', record 6 'visit 12' (2026-04-23), next record 2026-08-20; expected.json flags G1, G2, P1, K1 only; no tolerated entry",
   "why_it_matters": "In practice this is a records-request item (no PT discharge, 4 planned visits unaccounted for) and an adjuster will say 'she quit PT'. The 119-day gap covers the dates but not the plan-vs-actual shortfall that lib03 does surface.",
   "fix": "Add a tolerated conflict or record_warning for 'plan 16 visits; last PT record is visit 12; no discharge in packet'.",
   "acceptance_test": "lib05 expected.json lists a conflict or tolerated entry citing records 5 and 6."
  },
  {
   "severity": "minor",
   "title": "Packet format is thinner than a real records set",
   "evidence": "All 7 packets: one quoted sentence per record, charges inside clinical notes (e.g. lib01 'ED charge: $3,915.', lib05 'Surgeon fee: $6,150.'), no itemized ledger by DOS, no CPT codes, no Bates/page numbers, no stated date of accident; none of lib01-07 has a missed-appointment PT discharge, an intake-form accident-date conflict, an ambiguous date, or a copy-forward note",
   "why_it_matters": "Real bills arrive as separate UB-04/HCFA ledgers and the biggest adjuster attacks I deal with (onset-date conflict, missed appointments, copy-forward) are covered only by the older golden cases. The library widens scenarios and gaps but not record formats, so it cannot show the app handles a billing ledger with several DOS lines.",
   "fix": "Add one library packet whose bill is a multi-line ledger by date of service (some lines unreadable) and one with a stated accident date that differs between records, or say in research/case-library-sources.md that format coverage is left to evals/golden.",
   "acceptance_test": "At least one packet has a billing_statement record with 3+ dated charge lines, or the sources doc states the limit explicitly."
  },
  {
   "severity": "minor",
   "title": "Two of the six sources I could not fetch; one is marked unopened by the author",
   "evidence": "curl with browser UA: valawyersweekly.com (S5) HTTP 403, rissman.com/?p=2203 (S7) HTTP 403; research/case-library-sources.md S2 'no (HTTP 403)'. S1, S3, S4, S6 returned 200 and match the described scenarios.",
   "why_it_matters": "I can confirm 4 of 7 sources; lib02, lib05 and lib07 rest on pages I could not open, so the 'opened' claims for S5 and S7 are unverified by me (the author fetched them by another route). Packets themselves contain no identifier from any source I could read.",
   "fix": "Save a short text excerpt or archive link for S5 and S7 under research/ so reviewers can verify; open S2 or drop it from the AC1 count (6 other sources still meet the minimum).",
   "acceptance_test": "research/case-library-sources.md gives an archive URL or saved excerpt for each source marked opened."
  },
  {
   "severity": "nit",
   "title": "lib03 'unchanged from visit 1' has no visit-1 pain score in the packet",
   "evidence": "case_lib03 record 3 has no pain rating; record 4 'Pain 5/10, unchanged from visit 1.'",
   "why_it_matters": "The comparison cannot be checked in the packet; a reviewer cannot confirm 'unchanged' from the record text.",
   "fix": "Add 'Pain 5/10' to record 3.",
   "acceptance_test": "record 3 excerpt contains a pain score equal to record 4."
  }
 ],
 "whats_right": [
  "Gap day counts, near-miss intervals (28, 26) and totals all recompute by hand; billing statements are kept out of gap endpoints and the LOP balance/adjustment/amount due are never added to the total (lib06 $6,830).",
  "Every hedge, prior and patient self-report is quoted and attributed, and must_not lists block the tool from explaining a gap or turning 'tingling' or 'may be needed' into a finding.",
  "No name, provider, place or number from the four sources I could read appears in any packet, and all 7 carry the SYNTHETIC header."
 ],
 "questions_for_chris": [
  "Should a stated attendance count at discharge (lib03 '31 visits') ever let the tool show a candidate rate x count figure in internal notes, or must it stay silent until a billed count appears?"
 ]
}
```
