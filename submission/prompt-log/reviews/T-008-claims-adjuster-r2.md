# T-008 round 2 review — claims-adjuster-reviewer

**Verdict: fail** (1 blocker, 1 major, 1 minor, 2 nits).

All six round-1 findings are resolved. The resolution table with the exact greps is in
`artifacts/review-evidence/T-008-r2-adjuster.md`. A12 (delay to first treatment) follows D-017: it states "first recorded
treatment = 2026-01-09", names both accident dates, and computes no delay. I am judging whether the research documents the
attack, not whether the tool computes it, and it does. Brinjikji is now labeled lumbar-only, and the cervical study added for
the neck point (Nakashima, src 19) checks out against its PubMed abstract. The PIC clause is gone. The glossary has 46 terms.

The new A15 row creates the problem I'm here to catch. It says Rivera had a "referral to pain management". No record says
that. Record 7 names no referral source, and A14, one line above in the same table, says "the records do not say who referred
him". My checklist item 19 says a pain-management referral stated anywhere is an invented fact. This table goes to T-009,
the persona files, and the golden files, so the invented referral would spread from here. A15 also calls Rivera's care
"active", which no record supports. Separately, A14 cites src 1 for attorney-timing scrutiny, but src 1 says nothing about
it.

```json
{"card": "T-008", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 568e4b7 vs 2c76cda: research/adjuster-attacks.md, research/ASSUMPTIONS-proposed.md, research/texas-pi-notes.md, memory/GLOSSARY.md; no app (research card); Jordan Rivera sample (evals/golden/sample.txt)",
 "exercised": [
  "python3 tools/board.py show T-008 (status in_review, rounds 1, commits 2c76cda, 568e4b7)",
  "git log --oneline -- research memory/GLOSSARY.md | head -5 -> 568e4b7 top",
  "git diff 2c76cda 568e4b7 -- the four T-008 files (read in full)",
  "Re-ran every round-1 acceptance grep (first treatment, P-14, Delay in treatment, MIST|attorney|passive, lumbar, PIC, src-ref resolution, glossary count, approx. 40%); outputs in artifacts/review-evidence/T-008-r2-adjuster.md",
  "grep -cE '^[0-9]+\\. .*https?://' -> chronology 10, adjuster-attacks 19, texas-pi-notes 12; grep -cE '^- \\*\\*' GLOSSARY -> 46",
  "Read evals/golden/sample.txt (records 1-9) and grep -n -i refer -> only rec 3 'Refer to physical therapy'",
  "Read evals/golden/sample.expected.json flags (G1, C1, C2, P1, P2, K1) to check flag types against A2/A4",
  "Read memory/ORCHESTRATOR_DECISIONS.md D-013, D-017, D-018",
  "curl NCBI efetch PMID 25584950 (Nakashima, src 19) HTTP 200 -> figures confirmed",
  "curl IRMI Stowers doctrine (TX src 12) HTTP 200 -> confirmed",
  "curl Braun Law (AA src 18, MIST glossary source) HTTP 200 -> MIST definition confirmed",
  "curl Claims Journal (AA src 1) HTTP 200 -> searched for attorney/retain/referr/letter of protection: no attorney-timing or LOP text"
 ],
 "verdict": "fail",
 "scores": {"source_quality_and_labeling": 4, "adversarial_coverage": 4, "accuracy_vs_sources": 2, "texas_relevance": 4, "usefulness_to_flags_and_lexicon": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A15 invents a 'referral to pain management' for Rivera",
   "evidence": "research/adjuster-attacks.md:35 A15 Rivera column: 'active care (PT, referral to pain management, ESI recommended)'. evals/golden/sample.txt record 7 verbatim: 'New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.' (no referral source). `grep -n -i refer evals/golden/sample.txt` -> only line 16, rec 3 'Refer to physical therapy'. Same file :34 (A14) says: 'the records do not say who referred him'.",
   "why_it_matters": "Persona checklist item 19: record 7 names no referral source, so 'referred to pain management' anywhere is an invented fact. A referral from the PCP would close my 73-day-gap argument, because it makes pain management look like a continuation of care. This table is the stated input to T-009, the personas and the golden files, so a fact invented here ends up in prompts and expected outputs. The file also contradicts itself (A14 vs A15).",
   "fix": "Replace with what the records say: 'PT (rec 4-6), pain-management new-patient visit 2026-05-18 with no referral source stated (rec 7), cervical ESI recommended, not performed (rec 9)'.",
   "acceptance_test": "grep -n -i 'referral to pain\\|referred to pain' research/ memory/ -r -> no output; A15 Rivera cell cites rec 7 with 'no referral source stated'."},
  {"severity": "major",
   "title": "A15 calls Rivera's care 'active', which no record supports",
   "evidence": "research/adjuster-attacks.md:35 'active care (PT, …, ESI recommended)' and :98 'Rivera's care is active and shorter than planned.' Records 4-6 verbatim give only 'Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.' / 'Pain 4/10, improving…' / 'Discharged from PT after two missed appointments. Pain 3/10.' No modality or exercise is named. Record 9 ESI is 'Recommend' (not performed), and an injection is not active care in the src 1 sense ('Was it active or passive?'). Record 2 prescribes cyclobenzaprine.",
   "why_it_matters": "Active vs passive care is a value driver I score. The research answers that question for the claimant with no record behind it. Downstream, a persona or prompt may treat 'active care' as a sample truth, and that is an overstated finding I would discount.",
   "fix": "State 'records do not say whether PT was active or passive; plan 12 visits, discharged at visit 9 (rec 4, 6)'. Keep 'shorter than planned', because rec 4 and rec 6 support it.",
   "acceptance_test": "grep -n -i 'care is active\\|active care (' research/adjuster-attacks.md -> no output; A15 row says modality is not stated in the records."},
  {"severity": "minor",
   "title": "A14 cites src 1 for attorney-timing scrutiny that src 1 does not contain",
   "evidence": "research/adjuster-attacks.md:34 A14 Evidence column '1, TX §3 (K&L), 3'; :92-93 'Adjusters compare the attorney-retention date with when care started or escalated.' (no citation). curl Claims Journal src 1 (HTTP 200): all 7 'attorney' hits are about attorneys sending BI demands or requests, e.g. 'Just because the attorney says it is so, doesn't make it so.' There are no hits for 'retain', 'referr' or 'letter of protection'. (My round-1 memory note that src 1 listed attorney timing was also wrong; I've corrected it.)",
   "why_it_matters": "An attack row with a citation that doesn't support it is the same kind of defect as the round-1 'Australian PIC' clause. Lexicon `litigation_referral` rationales will cite this row.",
   "fix": "Drop src 1 from A14, or cite only its provider-type item. Label the retention-timing sentence 'assumption (adjuster practice; persona §2)', or add a source that states it.",
   "acceptance_test": "Every source number in the A14 row supports the attorney/LOP claim, or the claim is marked 'assumption'."},
  {"severity": "nit",
   "title": "Nakashima src line says 'mostly at C5-C6'; abstract says 41%",
   "evidence": "research/adjuster-attacks.md:141 'cord compression 5.3%, mostly at C5-C6'. PubMed abstract verbatim: 'predominantly occurred at C5-C6 (41%) and C6-C7 (27%)'. The study measured bulging, not protrusion, in Japanese volunteers.",
   "why_it_matters": "41% is the largest share, not most of the cases. Defense counsel would catch it.",
   "fix": "Write 'most often at C5-C6 (41%)' and note that the study measured disc bulging.",
   "acceptance_test": "src 19 line includes '41%'."},
  {"severity": "nit",
   "title": "GLOSSARY soft-tissue definition adds a clause that src 18 doesn't state",
   "evidence": "memory/GLOSSARY.md:26 'sprain/strain/whiplash-type injury without fracture or neurological deficit … Source: AA A9, src 18'. Src 18 (Braun, curl 200): 'The most common MIST injuries are a sprained/strained neck or back'. Src 18 has no fracture/neurological-deficit language.",
   "why_it_matters": "This is minor, but the glossary rule is source-or-assumption for every claim.",
   "fix": "Mark the 'without fracture or neurological deficit' clause as an assumption, or drop it.",
   "acceptance_test": "The glossary line matches its source or carries 'assumption'."}
 ],
 "whats_right": [
  "A12/P-14 follow D-017 exactly: first recorded treatment 2026-01-09, both accident dates named, no delay computed.",
  "A13 is accurate to rec 1 ('approx. 35 mph', 'Transported to Central ER') and says honestly that the records have no vehicle-damage facts.",
  "The lumbar/cervical split is now honest, and the Nakashima and IRMI/Stowers sources check out verbatim."
 ],
 "questions_for_chris": []}
```
