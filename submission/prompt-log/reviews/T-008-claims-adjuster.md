# T-008 review — claims-adjuster-reviewer

**Verdict: changes** (0 blockers, 2 majors, 3 minors, 1 nit).

All four ACs are met as written: `grep -cE '^[0-9]+\. .*https?://'` returns chronology-practice.md 10, adjuster-attacks.md 18,
texas-pi-notes.md 11. GLOSSARY has 38 `- **` term lines, all with a source or "assumption". ASSUMPTIONS-proposed has 13 P-rows.
The attack map ties each attack to the exact Rivera excerpt, and the day counts are right (73 days 03-06→05-18; 129 days 01-09→05-18).
As the adjuster, my objection is what the map leaves out. The insurer-side checklist the researcher cites (Claims Journal, src 1)
starts with "How soon did treatment start?", vehicle damage, and whether the claimant was transported from the scene. None of those
made it into A1–A11. Attorney-driven care, active vs. passive care, and duration vs. expected recovery are missing too. Those are my
first moves on a soft-tissue demand, and because T-009 builds on this map, the lexicon misses them as well (see T-009 review).
One cited study is stretched beyond its scope (a lumbar review used for a cervical finding), and one claim cites a source that isn't
listed.

Exercised: `python3 tools/board.py show T-008` (ACs above). I read all four research files and memory/GLOSSARY.md at HEAD (commit
2c76cda content). I re-counted sources, glossary terms and P-rows with grep (output above). I ran a coverage grep:
`grep -n -i "delay\|first treatment\|property damage\|MIST\|minor impact\|attorney\|passive\|IME" research/adjuster-attacks.md` →
no output. I spot-checked 4 sources with curl (WebFetch isn't in my toolset): Claims Journal src 1, Brinjikji src 6 (PubMed abstract
plus PMC full text), Herrera v. Madrak src 14 (vLex), and Virginia Lawyers Weekly src 16. Fletcher v. Simmons returned HTTP 403
(paywall). Verbatim excerpts are in `artifacts/review-evidence/T-008-adjuster-source-checks.txt`. I checked the claims against
personas/claims-adjuster.md §2/§4, spec Appendix A/C, and evals/golden/sample.expected.json. Agent memory was empty at start.

```json
{"card": "T-008", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "research/chronology-practice.md, research/adjuster-attacks.md, research/texas-pi-notes.md, research/ASSUMPTIONS-proposed.md, memory/GLOSSARY.md (commit 2c76cda, read at HEAD 9e759a2); no app; Jordan Rivera sample case",
 "exercised": [
  "python3 tools/board.py show T-008 (4 ACs, all marked done)",
  "grep -cE '^[0-9]+\\. .*https?://' on the three research files -> 10 / 18 / 11",
  "grep -cE '^- \\*\\*' memory/GLOSSARY.md -> 38 terms; every line contains 'Source:'",
  "grep -cE '^\\| P-[0-9]+' research/ASSUMPTIONS-proposed.md -> 13",
  "grep -n -i 'delay|first treatment|property damage|MIST|minor impact|attorney|passive|IME' research/adjuster-attacks.md -> no output",
  "curl Claims Journal src 1 (HTTP 200) and extracted the 10-point medical-records checklist verbatim",
  "curl PubMed efetch 25430861 + PMC4464797 BioC full text for Brinjikji src 6 (figures confirmed; lumbar-only scope found)",
  "curl vLex Herrera v. Madrak src 14 (holding confirmed: >12 missed PT appointments warranted mitigation charge)",
  "curl Virginia Lawyers Weekly src 16 (takeaway confirmed; 'eight days later' delayed report found)",
  "curl studicata Fletcher v. Simmons -> HTTP 403, unverifiable",
  "Recomputed Rivera day counts by hand: 73 (03-06->05-18), 129 (01-09->05-18), 28 (01-23->02-20)",
  "Read personas/claims-adjuster.md, spec/SPEC.md Appendix A, spec/SAMPLE_CASE_TRUTHS.md, evals/golden/sample.expected.json"
 ],
 "verdict": "changes",
 "scores": {"source_quality_and_labeling": 4, "adversarial_coverage": 2, "accuracy_vs_sources": 3, "texas_relevance": 4, "usefulness_to_flags_and_lexicon": 3},
 "findings": [
  {"severity": "major",
   "title": "Attack map omits delay to first treatment, the adjuster's first check",
   "evidence": "research/adjuster-attacks.md:16-28 (A1-A11) has no delay/first-treatment row; coverage grep for 'delay|first treatment' -> no output. Cited src 1 says verbatim: '5) Treatment patterns – How soon did treatment start? Were there gaps in treatment?' and '7) Duration and frequency – When did treatment start?' Src 16 (also cited) says verbatim: 'did not report injury until eight days later when he was seen at an urgent care facility.' personas/claims-adjuster.md §2: 'What he looks for first: accident date vs first-treatment date'; §4 item 2.",
   "why_it_matters": "Delay between the accident and first care is the strongest 'not really hurt' argument and is separate from a gap between visits (A1). It isn't in the research, so it isn't in the lexicon or ASSUMPTIONS, and no flag or field is planned for it. For Rivera the delay is 0 days (EMS on 2026-01-09), which helps the claimant, and the paralegal should see it. On another case, a 5-day delay will be the first line of my response.",
   "fix": "Add attack A12 'Delay to first treatment': what the defense argues; sources 1 and 16; Rivera = same day (record 1 EMS, record 2 ER). Note that code computes it from the earliest accident date to the first date of service, and that it must use both accident dates when they conflict (01-09 vs 01-19). Propose a matching P-row and a GLOSSARY term ('delay in treatment').",
   "acceptance_test": "grep -n -i 'first treatment' research/adjuster-attacks.md returns an attack-map row citing src 1 with the Rivera value (0 days from 2026-01-09); ASSUMPTIONS-proposed.md has a P-row for it; GLOSSARY has 'Delay in treatment'."},
  {"severity": "major",
   "title": "MIST/vehicle damage, attorney-driven care, and passive/over-long treatment are missing from the attack map even though the cited source lists them",
   "evidence": "Src 1 verbatim: '1) Police report – ... Was the injured party transported to a medical facility?'; '2) Vehicle photographs – Does the damage match? ... What is the directional force of impact?'; '6) Provider type – Was the claimant seen by a chiropractor or medical doctor?'; '7) ... Was it active or passive? Was it longer than an anticipated expected recovery date...'. adjuster-attacks.md:89 summarizes src 1 as including 'duration vs typical recovery, ... mechanism of injury', but no A-row covers them. Attorney referral/LOP appears only in texas-pi-notes.md §3 and lexicon.yaml:547 (litigation_referral), not as an attack. Coverage grep for 'property damage|MIST|minor impact|attorney|passive' -> no output.",
   "why_it_matters": "These are value drivers I use on every soft-tissue claim: low impact or no visible damage, ambulatory at scene or refused transport, care that starts or escalates after an attorney is retained, months of passive modalities beyond the expected recovery, and chiropractor-only care. Rivera record 1 has 'rear-ended at approx. 35 mph' and 'Transported to Central ER', both mechanism and transport facts. Because the map is the stated basis for T-009 and the adjuster persona, those layers inherit the gap. My T-009 probes confirm the lexicon misses 'Minimal damage to vehicle; airbags did not deploy', 'Ambulatory at scene, refused transport', and 'Referred to this clinic by attorney'.",
   "fix": "Add rows for: A13 mechanism/MIST (vehicle damage, speed, airbags, ambulatory or transported at scene; Rivera records 1-2), A14 attorney involvement timing / LOP-funded care (texas-pi-notes §3; flag only if the record says it), A15 duration and type of care vs expected recovery (active vs passive, provider type; src 1, src 3 Colossus duration). For each, state the flag type, or 'context only, not a required flag', and whether code or lexicon owns it.",
   "acceptance_test": "adjuster-attacks.md attack map has rows covering mechanism/MIST, attorney/LOP timing, and duration/passive care, each citing src 1 (and src 3 or TX §3 where relevant) and naming the Rivera record or 'not in records'; T-009 re-run of artifacts/review-evidence/T-009-adjuster-probes.py MIST/transport/attorney probes reflects the new rows."},
  {"severity": "minor",
   "title": "Brinjikji (lumbar-only review) used to argue about a cervical C5-C6 finding",
   "evidence": "adjuster-attacks.md:48-50: 'disc bulge prevalence rose from ~30% at age 20 to ~84% at 80 ... The defense uses this to say a C5-C6 protrusion in a 41-year-old may be pre-existing'. Brinjikji full text (PMC4464797) verbatim: 'additional studies that reported lumbar spine CT or MR imaging findings in individuals without low back pain.' Figures themselves confirmed against the PubMed abstract.",
   "why_it_matters": "If the firm repeats this in a demand or a rebuttal, defense counsel will point out that the study is about the low back, not the neck. The direction of the point (degeneration is common in people without symptoms) probably holds for the cervical spine too, but this is the wrong citation for it.",
   "fix": "Say explicitly that Brinjikji covers the lumbar spine, and add a cervical asymptomatic-MRI source if the research wants to make the C5-C6 point. Otherwise, limit the claim to 'spinal (lumbar) degeneration is common in asymptomatic adults'.",
   "acceptance_test": "adjuster-attacks.md A4 text and src 6 line both say 'lumbar'; any cervical prevalence claim cites a cervical study with URL."},
  {"severity": "minor",
   "title": "Unlisted source cited: 'Australian PIC'",
   "evidence": "adjuster-attacks.md:62-63: 'contemporaneous records outweigh an expert relying on an incorrect history (src 17, Australian PIC)'. Src 17 (line 105) is a Georgia Court of Appeals decision; no Australian Personal Injury Commission source appears in the 18-item list.",
   "why_it_matters": "A claim with no URL can't be checked, and it is also foreign law. lexicon.yaml:538 (inconsistent_history rationale: 'contemporaneous records outweigh later accounts') rests on it.",
   "fix": "Either add the PIC source with a URL and a 'non-US' label, or remove the clause and keep only what src 17 supports (impeachment with the claimant's intake forms).",
   "acceptance_test": "Every parenthetical source reference in adjuster-attacks.md resolves to a numbered entry with a URL."},
  {"severity": "minor",
   "title": "GLOSSARY lacks core adjuster vocabulary",
   "evidence": "memory/GLOSSARY.md (38 terms) has no entry for MIST / minor impact soft tissue, delay in treatment, specials vs generals, soft-tissue injury, value drivers, Stowers demand, or BI. personas/claims-adjuster.md §6 lists these as the adjuster's vocabulary.",
   "why_it_matters": "Workers and reviewers who write flag rationales and persona checks use the GLOSSARY. If these terms are missing, the adversary's actual arguments never make it into the vocabulary those people work from.",
   "fix": "Add one-line entries for MIST, delay in treatment, specials vs generals, value drivers (Colossus), Stowers demand (texas-pi-notes §7 already names it), and BI, each with a source or 'assumption'.",
   "acceptance_test": "grep -c -E 'MIST|Delay in treatment|Generals|Value drivers|Stowers' memory/GLOSSARY.md >= 5."},
  {"severity": "nit",
   "title": "Attack map drops 'approx.' from the ROM finding",
   "evidence": "adjuster-attacks.md:26: 'objective: ROM −40% (rec 4)'. Record 4 verbatim: 'Cervical range of motion reduced approx. 40%.'",
   "why_it_matters": "This is the same kind of hedge-stripping the research tells the product never to do (chronology-practice.md R3). Research tables get copied into prompts and golden files.",
   "fix": "Quote as 'reduced approx. 40%'.",
   "acceptance_test": "grep -n 'approx. 40%' research/adjuster-attacks.md matches the A9 row."}
 ],
 "whats_right": [
  "Attack map ties each attack to the exact Rivera excerpt, and the day counts (73, 129) are right; keep this record-anchored format.",
  "Read-depth and source-side labels (insurer, plaintiff, vendor, primary) are honest; the Herrera and Virginia takeaways check out against the sources.",
  "Billed-not-damages (Haygood / §41.0105) and '§18.001 is not causation evidence' are correctly turned into product rules."
 ],
 "questions_for_chris": [
  "Should delay-to-first-treatment be a visible computed field in the timeline (outside the four required flags), or research context only? The adjuster persona checklist item 2 assumes it is shown."
 ]}
```
