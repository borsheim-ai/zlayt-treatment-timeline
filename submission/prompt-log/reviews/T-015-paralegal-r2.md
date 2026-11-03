# T-015 round 2: paralegal-reviewer (Maria Delgado lens)

**Verdict: fail** (1 blocker, 2 majors, 4 minors, 1 nit).

Most of round 1 is fixed. K4 and K5 are now `must`. case_06 has all three prior-condition mentions at `must`, plus a neutral `must` conflict flag for the denial vs the chiropractic history. Every probe phrase from round 1 is now caught, and check_golden.py tests the bad and good examples. case_09 proves the rule that billing statements and phone notes don't count as visits. Every provider value equals the header label, and every synthetic facility name is clearly invented. The expected export matches REQUIREMENTS §6 byte for byte. Every quote in it is verbatim from the record it is attributed to, and the total is $8,390.00.

What still fails is K5, the wrong accident date on the intake form treated as a causation issue. The golden JSON makes it `must`, but the README scoring rule matches flags on type + cited records only. K4 and K5 are both `causation` citing record 7, so a single record-7 causation flag about "new onset" satisfies both. A tool can still get 100% causation recall without telling me that the intake date undercuts causation. The expected export has the same hole: its "Causation language" line has no intake-date item even though every flag is accepted.

Full resolution table: `artifacts/review-evidence/T-015-r2-paralegal.md`.

Commands run (exact output):
- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered` (exit 0)
- `python3 artifacts/review-evidence/T-015-r2-paralegal-probe.py` → `artifacts/review-evidence/T-015-r2-paralegal-probe.out.txt` (exit 0)
- `git status --porcelain evals/golden/ spec/REQUIREMENTS.md` → (empty); `git diff --stat 3c5eb7c -- evals/golden/` → (empty); `git log -1 --format=%h -- evals/golden` → `3c5eb7c`

```json
{"card": "T-015", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "round 2, commit 3c5eb7c (diff 47520a8..3c5eb7c -- evals/golden): README.md, sample.txt, sample.expected.json, sample.export.expected.txt, case_01..09 .txt/.expected.json, hallucinations*.jsonl, check_golden.py; refs spec/REQUIREMENTS.md s6, R-EX-4, R-EX-8, R-FL-4, R-TL-3; memory/ORCHESTRATOR_DECISIONS.md D-001..D-018; no app (pre-code eval data); sample case evals/golden/sample.txt",
 "exercised": [
  "python3 tools/board.py show T-015 (AC 1-4, handoff notes)",
  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered', exit 0",
  "artifacts/review-evidence/T-015-r2-paralegal-probe.py (output T-015-r2-paralegal-probe.out.txt): s6 byte compare, per-record quote attribution of every letter line, notes coverage of each must flag, literal README:70 matching simulation, provider==header for all cases, Source-label inventory, levels/tolerated per case, round-1 regex probes + new probes, case_09 gap recompute and must_nots, source_kind scoring lookup, hallucination categories",
  "Read case_06 and case_09 .txt + expected.json in full; read sample/case_03/05/08 must_not and tolerated lists",
  "Compared sample.export.expected.txt line by line with REQUIREMENTS s6 and R-EX-4 (1)-(11) and with the 9 records",
  "git status/diff vs 3c5eb7c (clean)"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 4, "arithmetic_and_dates": 5, "appendix_c_fidelity": 3, "flag_levels_realism": 5, "adjuster_attack_coverage": 4, "must_not_strength": 4, "export_golden_consistency": 2, "synthetic_labeling": 5},
 "findings": [
  {"severity": "blocker", "title": "K5 (wrong intake accident date as a causation issue) is still unenforceable: K4 and K5 share type+cite, so one record-7 causation flag satisfies both, and the expected export has no K5 line",
   "evidence": "README.md:70 'A golden flag is matched only by a candidate flag of the same type that cites every record in cite.all and >= 1 of cite.any'. Nothing requires evidence overlap or one-to-one assignment. sample.expected.json K4 and K5 are both {type: causation, cite.all: [7]}. probe s4 (T-015-r2-paralegal-probe.out.txt): a single candidate {causation, cites {7}, 'New onset pain after a 73-day gap...'} -> 'matches K4 (temporal_after_gap): True', 'matches K5 (accident_date_inconsistency): True'. probe s3: 'causation line mentions intake-date (K5 evidence)? False'. sample.export.expected.txt's causation line lists only records 8, 6, 9 and record 7 \"New onset pain\", even though the case states that all flags are accepted.",
   "why_it_matters": "This is the round-1 blocker in a narrower form. A tool that never tells me the intake-form date undercuts causation still scores 5/5 causation recall. Appendix C lists that item under 'Expected flags (at minimum)'. The byte-exact export golden (ship bar 8) also builds the omission in: a product that emits and renders K5 correctly fails the export test.",
   "fix": "In README scoring, match a golden flag only when the candidate's evidence excerpt overlaps (normalized substring either way) at least one golden `excerpt`-field evidence item. Assign candidates to golden flags one-to-one (bipartite), so one candidate can't satisfy two golden flags. Add the K5 item to the s6 causation line (record 7 \"Date of accident per intake form: 2026-01-19.\"), via the writer/orchestrator, and re-extract sample.export.expected.txt. Have check_golden.py assert that every `must` flag of the sample has its evidence in the notes block.",
   "acceptance_test": "Runner fixture: one record-7 causation candidate with evidence 'New onset pain' -> K4 TP, K5 miss, causation recall 4/5. check_golden.py fails if any sample must-flag evidence excerpt is absent from internal_notes_text."},
  {"severity": "major", "title": "Expected export can't be derived from R-EX-4 and the golden JSON (record 1 missing from 'flagged language quoted', Bills-to-request label rule not followed)",
   "evidence": "R-EX-4(4): list 'each letter entry whose excerpt contains the evidence of a flag that is not dismissed'. sample.expected.json C1 evidence now includes record 1 'rear-ended at approx. 35 mph' (field excerpt), and the record-1 letter quote contains it. 'FLAGGED LANGUAGE QUOTED IN THE LETTER' in sample.export.expected.txt lists records 4, 6, 7, 8, 9 and not record 1. R-EX-4(8): 'providers (the label up to the first comma)', yet the export reads 'Dr. Alvarez, primary care' (rule gives 'Dr. Alvarez'), and the order (Austin EMS; Dr. Alvarez; Hill Country; Capital PT) is not record order, with no stated sort. check_golden.py:311-333 checks only that quotes are verbatim somewhere in sample.txt, not that they are attributed to the right record, and it checks no R-EX-4 section rule.",
   "why_it_matters": "The export golden is the M1 reference for byte-exact output. If a correct implementation of the written rules fails it, someone will either hard-code the text or relax the test. Either way the internal notes stop telling me exactly which adverse language is in the letter.",
   "fix": "Decide the record-1 question: either C1's 'rear-ended' evidence counts and the notes list record 1 ('Conflict, accident date'), or C1's record-1 evidence becomes field 'date' only. Then fix s6 or R-EX-4(8) so the bills-to-request label and order follow a stated rule, and re-extract. Add a check_golden.py step that rebuilds the 'flagged language' and 'bills to request' sections from sample.expected.json + R-EX-4 and compares them.",
   "acceptance_test": "check_golden.py derives both sections from the JSON and the rule, and they equal the export golden; every quoted span is checked against the record number it is cited to."},
  {"severity": "major", "title": "REQUIREMENTS R-FL-4 still says K4/K5 are 'should', credited through G1/C1, which contradicts the golden README; no D-entry records the change",
   "evidence": "spec/REQUIREMENTS.md:68 R-FL-4 'the record-7 items (... K4-K5) are `should`, credited when found directly or through G1/C1'. README.md:70 'G1 (gap) and C1 (conflict) do not satisfy K4 and K5' and README.md:146 'REQUIREMENTS R-FL-4 still says K4/K5 are should (orchestrator decision: must)'. `grep -n K4 memory/ORCHESTRATOR_DECISIONS.md` finds nothing. R-TL-4/ship bar still say 20 seeded items (file has 34).",
   "why_it_matters": "The runner author will implement one of two contradictory scoring rules. If they follow R-FL-4, the round-1 blocker comes back without anyone editing evals/golden.",
   "fix": "Orchestrator records a D-entry (K4/K5 must; type match explicit; evidence-overlap matching per the blocker fix). The writer updates R-FL-4, R-TL-4 and ship bar 4 (>= 33 of 34) to match.",
   "acceptance_test": "grep 'should' near K4/K5 in spec/REQUIREMENTS.md returns nothing; a D-entry cites T-015 r2."},
  {"severity": "minor", "title": "`source_kind` has no scoring rule and is tagged on whole entries that mix provider findings with patient statements; the golden export's EMS summary drops the attribution",
   "evidence": "probe s10: 'source_kind' in scoring section: False. Entry-level patient_self_report tags on case_06 E1 (excerpt includes the ER diagnosis 'Cervical strain'), sample E1 (EMS 'Alert and oriented'), case_09 E3 ('Work note provided' is the clinic's act). sample E1 required_terms ['C/O','complain','reports','reported'] are satisfied by the excerpt alone. The export summary reads 'neck pain 7/10 and headache' with no 'complained of'.",
   "why_it_matters": "Checklist 23: self-reports stay attributed. With no rule, the runner may skip the check entirely, or apply it to the whole entry and push the tool to call an ER diagnosis a patient complaint.",
   "fix": "Move source_kind to span level ({excerpt, kind}) and add a README scoring rule: the summary clause that renders that span carries an attribution word. Remove the tag from case_09 E3. Decide whether the s6 EMS summary should say 'complained of neck pain 7/10'.",
   "acceptance_test": "README scoring names source_kind; every tagged span is a patient statement; the runner rejects 'Patient had neck pain per EMS exam' for sample E1."},
  {"severity": "minor", "title": "Remaining regex gaps: aggravation wording, sample laterality swap, 'non-compliant', case_06 'No history of neck problems'",
   "evidence": "probe s7: caught=[] for 'Persistent neck pain 6/10; prior low back pain (2023) aggravated by the collision.', 'Pain radiating to left arm.', 'Patient was non-compliant with PT.', and case_06 'No history of neck problems.'",
   "why_it_matters": "'Aggravated by' is a causation claim (an aggravation theory), and a side swap is the error an adjuster spots first. Both currently depend on the LLM judge alone.",
   "fix": "Sample M2: add aggravat\\w+ (by|from). New sample regex for \\bleft\\s+(arm|foramin\\w+|fingers). Add a \\bnon-?complian\\w+ regex for tool-authored summaries. case_06 M2: allow 'no (prior|previous|history of)'.",
   "acceptance_test": "The four probe strings are in bad_examples and fire; check_golden.py stays green on inputs."},
  {"severity": "minor", "title": "case_09: no tolerated entry for 'Return in 2 weeks' followed by a 56-day return, so a compliance/causation flag would be a false positive",
   "evidence": "case_09 rec 1 'Return in 2 weeks' (2026-02-02); next visit rec 4 2026-03-30; probe s9: causation flags [] and tolerated []. D-013 maps compliance to causation.",
   "why_it_matters": "'Told to come back in two weeks, came back in eight' is how the adjuster will word it. Penalizing the tool for raising it pushes it toward silence.",
   "fix": "Add tolerated T1 {type: causation, cite.all [1,4], subtype follow_up_not_kept}, worded as the record's own words with no 'non-compliant' label.",
   "acceptance_test": "A causation candidate citing case_09 records 1 and 4 scores as tolerated, not FP."},
  {"severity": "minor", "title": "Two different golden total strings for the sample, with no surface named",
   "evidence": "sample.expected.json totals.display 'Billed charges stated in these records: $8,390 (excludes physical therapy — per-visit rate only, visit count not stated)' vs export letter 'Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)' (probe s8).",
   "why_it_matters": "R-EX-8 forbids the 'visit count not stated' reason in the letter. If the runner compares the letter total to totals.display, the R-EX-8 wording looks wrong, or the reason leaks in.",
   "fix": "In the README schema, state that totals.display is the UI/notes string and the letter total line is R-EX-8 (or add totals.letter_line).",
   "acceptance_test": "README names the surface for each string; check_golden asserts the letter total line equals totals.letter_line."},
  {"severity": "nit", "title": "case_09 billing-statement charge has no date-of-service field for specials reconciliation",
   "evidence": "case_09 A1 {record_no 2, excerpt 'Statement for visit of 2026-02-02: $275.'}; the entry date is correctly 2026-03-01 (R-TL-3) and M2's good_examples allow mentioning the visit date.",
   "why_it_matters": "I reconcile specials by DOS. The quote carries it, so nothing is lost, but a structured field would make reconciliation one glance.",
   "fix": "Optional: add amounts[].service_date_in_excerpt '2026-02-02' (evidence only, never the entry date).",
   "acceptance_test": "Field present and verbatim in the excerpt."}
 ],
 "whats_right": [
  "Every round-1 probe phrase is now caught, and every regex/structural must_not carries >= 3 bad and >= 3 good examples that check_golden.py actually fires/does not fire.",
  "case_06 C1 and case_09 are exactly how I'd want them: the conflict is framed as possible, records are requested, the patient is never accused, and billing/phone dates never close a visit gap.",
  "The expected letter is clean demand text: header labels verbatim, US long dates, verbatim whole-sentence quotes from the cited record, $8,390.00 from explicit charges only, and no flag text in the letter."
 ],
 "questions_for_chris": [
  "Record 1's letter quote ('rear-ended at approx. 35 mph') is now C1 evidence. Should the internal notes list the EMS entry under 'flagged language quoted in the letter' (mechanically per R-EX-4), even though the mechanism helps rather than hurts the client?"
 ]}
```
