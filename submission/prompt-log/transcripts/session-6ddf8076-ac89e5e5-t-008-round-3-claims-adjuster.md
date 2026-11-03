# Subagent: T-008 round-3: claims-adjuster (T-008 round-3: claims-adjuster)

Source: `agent-ac89e5e523113b87f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:57:11.678Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 3 (final) of T-008 "Domain research" (M1). AC: `python3 tools/board.py show T-008`. Your r2 review: reviews/T-008-claims-adjuster-r2.md (fail: invented "referral to pain management"; "active" care). Change: commit da17ba2 (`git diff 568e4b7..da17ba2 -- research memory/GLOSSARY.md`). Exercise: verify each r2 finding resolved; re-grep research/*.md for any statement about the sample case that is not a quote of spec/SPEC.md's records (list each hit and whether it's quoted); curl the new Insurance Journal source. Write reviews/T-008-claims-adjuster-r3.md (D.2 JSON). Do not fix anything. Reply ≤ 12 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:13.813Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/claims-adjuster-reviewer/*.md; echo ----; cat reviews/T-008-claims-adjuster-r2.md; echo ----; python3 tools/board.py show T-008",
 "description": "Read memory, r2 review, and card"
}
````

### User / tool · 2026-11-02T00:57:13.947Z

**tool result**
````
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1 omissions, r2 invented Rivera facts in new rows; verified source facts
---
name: lexicon-review-method
description: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes
metadata:
  type: feedback
---

A lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real
adjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).

**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.

**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo
guard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).
Always probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) "No acute fracture, chronic degenerative changes"
(comma-scope negation); (3) intake checkboxes "Prior injuries: No."; (4) ROS denial lists >6 tokens; (5) "did not present
with"; (6) MIST/scene facts and "out of proportion". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,
compliance→causation mapping). See [[research-attack-map-gaps]].
---
name: research-attack-map-gaps
description: Recurring adjuster-attack issues in Zlayt research (omitted attacks in r1; invented Rivera facts in fix rows in r2) and verified source facts
metadata:
  type: project
---

T-008 round 1 (2026-11-01): adjuster-attacks.md A1–A11 omitted delay-to-first-treatment, MIST/transport, attorney/LOP timing,
duration/passive care. Round 2 (568e4b7) added A12–A15 — but the new rows invented Rivera facts: A15 "referral to pain
management" (rec 7 names no referral source) and "Rivera's care is active" (no modality in recs 4-6). Rated blocker + major.

**Why:** researchers fill "Rivera records that trigger it" cells from memory of the case, not from sample.txt; fix rounds
are where new invented facts slip in.

**How to apply:** on every re-review, grep each NEW row's Rivera cell against evals/golden/sample.txt (esp. "refer", "active",
"performed", severity words). Correction: Claims Journal src 1 does NOT mention attorney retention/referral/LOP (curl
re-checked r2) — it covers transport, vehicle damage, start/gaps, provider type, active/passive, duration. Verified by curl:
Brinjikji AJNR 2015 = LUMBAR only; Nakashima Spine 2015 PMID 25584950 = cervical, bulging 87.6%, SCC 5.3% (C5-C6 41%);
Herrera v. Madrak >12 missed PT; VLW src 16 "eight days later"; IRMI Stowers ok; Braun src 18 defines MIST; Fletcher v.
Simmons 403. D-017: tool never computes delay — judge research, not code, on that. Use curl (no WebFetch); write curl
output only to a literal artifacts/review-evidence/ path (hook rejects `mkdir $VAR`). Evidence:
artifacts/review-evidence/T-008-adjuster-source-checks.txt, T-008-r2-adjuster.md. Related: [[lexicon-review-method]].
----
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
----
---
id: "T-008"
title: "Domain research: PI treatment chronologies, demand packages, what adjusters attack"
milestone: "M1"
role: "researcher"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:56:08Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T00:54:35Z"
rounds: 2
commits: ["2c76cda", "568e4b7", "da17ba2"]
reviews:
  - {"persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-008-claims-adjuster.md", "at": "2026-11-02T00:39:42Z"}
  - {"persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-008-claims-adjuster-r2.md", "at": "2026-11-02T00:54:30Z"}
ac:
  - {"n": 1, "text": "research/chronology-practice.md and research/adjuster-attacks.md exist, each with >=6 cited sources (URL + one-line takeaway)", "done": true, "evidence": "research/chronology-practice.md: 10 cited sources; research/adjuster-attacks.md: 18 cited sources (grep -cE '^[0-9]+\\. .*https?://'); each URL + one-line takeaway + read-depth label"}
  - {"n": 2, "text": "research/texas-pi-notes.md covers Texas-specific norms relevant to billed charges and records, with sources, and lists assumptions where sources are thin", "done": true, "evidence": "research/texas-pi-notes.md: §41.0105/Haygood (full text read), §18.001 current text + In re Allstate PDF read (2019 amendment: not causation evidence), K&L Auto Crushers, Prop Code §55.004 liens, TRE 902(10); 11 sources; 'Assumptions where sources are thin' T1-T3 + unverified items labeled"}
  - {"n": 3, "text": "memory/GLOSSARY.md has >=25 terms, each with a one-line definition and source or 'assumption'", "done": true, "evidence": "memory/GLOSSARY.md: 35 terms, each one line with research-file source # or 'assumption'"}
  - {"n": 4, "text": "research/ASSUMPTIONS-proposed.md lists >=8 proposed PI-practice assumptions for memory/ASSUMPTIONS.md, each with evidence", "done": true, "evidence": "research/ASSUMPTIONS-proposed.md: 13 proposals P-01..P-13 with evidence refs and confidence; refines A-101..A-103"}
---
## Description
How PI paralegals build treatment chronologies/medical summaries for demand packages; what adjusters and defense counsel attack (gaps, pre-existing/degenerative findings, inconsistent dates, missed appointments, subjective vs objective, causation hedges like 'may represent', 'correlate clinically', 'patient reports'); Texas PI norms relevant to the scenario (e.g., CPRC §41.0105 paid-vs-incurred, §18.001 affidavits) — verify, don't assume. Feeds GLOSSARY, lexicon, personas, ASSUMPTIONS. Use WebSearch/WebFetch; cite URLs.

## Notes (append-only, newest last)
- 2026-11-02T00:17:32Z researcher: claimed
- 2026-11-02T00:19:54Z researcher: Sources gathered: Tex statutes (18.001 via rulesofcivilprocedure mirror; statutes.capitol.texas.gov pages render as nav-only to WebFetch), Haygood (FindLaw), Allstate PDF text extracted (fn: 2019 amendment says 18.001 affidavits not causation evidence), K&L Auto Crushers, Guevara, JLG Trucking, Jelinek, Prop Code 55.004, Claims Journal adjuster checklist, Brinjikji AJNR 2015, EvenUp chronology guide. Writing research files now.
- 2026-11-02T00:22:47Z researcher: AC 1 checked: research/chronology-practice.md: 10 cited sources; research/adjuster-attacks.md: 18 cited sources (grep -cE '^[0-9]+\. .*https?://'); each URL + one-line takeaway + read-depth label
- 2026-11-02T00:22:47Z researcher: AC 2 checked: research/texas-pi-notes.md: §41.0105/Haygood (full text read), §18.001 current text + In re Allstate PDF read (2019 amendment: not causation evidence), K&L Auto Crushers, Prop Code §55.004 liens, TRE 902(10); 11 sources; 'Assumptions where sources are thin' T1-T3 + unverified items labeled
- 2026-11-02T00:22:47Z researcher: AC 3 checked: memory/GLOSSARY.md: 35 terms, each one line with research-file source # or 'assumption'
- 2026-11-02T00:22:47Z researcher: AC 4 checked: research/ASSUMPTIONS-proposed.md: 13 proposals P-01..P-13 with evidence refs and confidence; refines A-101..A-103
- 2026-11-02T00:22:47Z researcher: moved in_progress -> in_review
- 2026-11-02T00:31:54Z orchestrator: review dispatched: claims-adjuster-reviewer
- 2026-11-02T00:39:42Z orchestrator: review claims-adjuster-reviewer (claude-opus-5-5): changes — reviews/T-008-claims-adjuster.md; round 1; findings:
    - [major] Attack map omits delay to first treatment, the adjuster's first check — fix: Add attack A12 'Delay to first treatment': what the defense argues; sources 1 and 16; Rivera = same day (record 1 EMS, record 2 ER). Note that code computes it from the earliest accident date to the first date of service, and that it must use both accident dates when they conflict (01-09 vs 01-19). Propose a
    - [major] MIST/vehicle damage, attorney-driven care, and passive/over-long treatment are missing from the attack map even though the cited source lists them — fix: Add rows for: A13 mechanism/MIST (vehicle damage, speed, airbags, ambulatory or transported at scene; Rivera records 1-2), A14 attorney involvement timing / LOP-funded care (texas-pi-notes §3; flag only if the record says it), A15 d
    - [minor] Brinjikji (lumbar-only review) used to argue about a cervical C5-C6 finding — fix: Say explicitly that Brinjikji covers the lumbar spine, and add a cervical asymptomatic-MRI source if the research wants to make the C5-C6 point. Otherwise, limit the claim to 'spinal (lumbar) degeneration is common in asymptomatic adults'.
    - [minor] Unlisted source cited: 'Australian PIC' — fix: Either add the PIC source with a URL and a 'non-US' label, or remove the clause and keep only what src 17 supports (impeachment with the claimant's intake forms).
    - [minor] GLOSSARY lacks core adjuster vocabulary — fix: Add one-line entries for MIST, delay in treatment, specials vs generals, value drivers (Colossus), Stowers demand (texas-pi-notes §7 already names it), and BI, each with a source or 'assumption'.
- 2026-11-02T00:39:42Z orchestrator: assigned: researcher-a
- 2026-11-02T00:40:21Z researcher: claimed
- 2026-11-02T00:41:39Z researcher: Round 2 per reviews/T-008-claims-adjuster.md: M1 A12 delay to first treatment (src 1, 16; Rivera first recorded treatment 2026-01-09; per D-017 the tool states first recorded treatment, never computes delay — reviewer's 'code computes it' fix overridden by D-017), P-14, GLOSSARY 'Delay in treatment'. M2 A13 mechanism/MIST + transport, A14 attorney involvement/LOP timing, A15 duration/passive care, each with flag type per D-013/D-018 or 'context only'. Minor Brinjikji: labeled lumbar; added Nakashima 2015 cervical (src 19). Minor Australian PIC clause removed. Minor GLOSSARY +8 (MIST, delay in treatment, soft tissue, active vs passive, value drivers, generals, BI, Stowers w/ TX src 12). Nit 'approx. 40%' restored. Flag-type column moved to D-013 vocabulary.
- 2026-11-02T00:41:39Z researcher: moved in_progress -> in_review
- 2026-11-02T00:51:39Z orchestrator: review dispatched: claims-adjuster r2
- 2026-11-02T00:54:30Z orchestrator: review claims-adjuster-reviewer (claude-opus-5-5): fail — reviews/T-008-claims-adjuster-r2.md; round 2; findings:
    - [blocker] A15 invents a 'referral to pain management' for Rivera — fix: Replace with what the records say: 'PT (rec 4-6), pain-management new-patient visit 2026-05-18 with no referral source stated (rec 7), cervical ESI recommended, not performed (rec 9)'.
    - [major] A15 calls Rivera's care 'active', which no record supports — fix: State 'records do not say whether PT was active or passive; plan 12 visits, discharged at visit 9 (rec 4, 6)'. Keep 'shorter than planned', because rec 4 and rec 6 support it.
    - [minor] A14 cites src 1 for attorney-timing scrutiny that src 1 does not contain — fix: Drop src 1 from A14, or cite only its provider-type item. Label the retention-timing sentence 'assumption (adjuster practice; persona §2)', or add a source that states it.
- 2026-11-02T00:54:30Z orchestrator: assigned: researcher-a
- 2026-11-02T00:54:35Z researcher: claimed
- 2026-11-02T00:56:03Z researcher: Round 3 per reviews/T-008-claims-adjuster-r2.md. BLOCKER: A15 rewritten from quoted record text only ('Plan of care: 12 visits'; 'Discharged from PT after two missed appointments' under 'Capital PT, visit 9'; 'Hill Country Pain Management, new patient' with no referral source stated; 'Recommend cervical epidural steroid injection', not performed). MAJOR: 'active' removed; records 4-6 name no modality. MINOR: src 1 dropped from A14; added insurer-side src 20 (Insurance Journal 2026, referral steering / pain-management centers); retention-timing check labeled assumption. NITS: Nakashima '41%' + bulging-not-protrusion; soft-tissue glossary matched to src 18, extra clause marked assumption. SWEEP: research/*.md sample-case claims re-anchored to quotes: A2, A7, A8, A9, A12 (records 1-2 state no accident date; only rec 7 does), P-04, P-11, P-14, texas-pi-notes scenario + EMS/ER line, chronology-practice ESI line.
- 2026-11-02T00:56:03Z researcher: moved in_progress -> in_review

## Handoff
Round 3: blocker (invented pain-management referral) fixed with quotes only; major ('active care') removed, modality marked not stated; A14 now cites src 20, and the retention-timing check is an assumption; nits (41%, soft-tissue wording) fixed. Sweep also caught that the files said 'EMS/ER give accident date 01-09'. Records 1-2 state no accident date, only header dates; fixed in A7, A12, P-14 and texas-pi-notes. Verified: reviewer greps 'referral to pain|referred to pain|care is active|active care (' return nothing; src 19 has 41%; 20 sources.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:15.985Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 -- research memory/GLOSSARY.md; git diff --stat 568e4b7..da17ba2 -- research memory/GLOSSARY.md; git diff 568e4b7..da17ba2 -- research memory/GLOSSARY.md",
 "description": "Show round-3 diff"
}
````

### User / tool · 2026-11-02T00:57:16.119Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:18.042Z

**tool call — Bash**
````
{
 "command": "git diff 568e4b7..da17ba2 -- research/*.md memory/GLOSSARY.md; git show --stat da17ba2 | head -20",
 "description": "Show markdown diffs only"
}
````

### User / tool · 2026-11-02T00:57:18.163Z

**tool result**
````
diff --git a/memory/GLOSSARY.md b/memory/GLOSSARY.md
index 93bd157..d1879d2 100644
--- a/memory/GLOSSARY.md
+++ b/memory/GLOSSARY.md
@@ -23,7 +23,7 @@ pins it down. CP = research/chronology-practice.md · AA = research/adjuster-att
 ## Flags and attacks
 - **Delay in treatment (delay to first treatment)** — time from the accident to the first medical visit; adjusters' first check. The tool shows only "first recorded treatment" and never computes the delay (D-017). Source: AA A12, src 1, 16.
 - **MIST (minor impact soft tissue)** — carrier category for low-speed collisions with soft-tissue injuries, valued low; attacked with vehicle-damage and scene facts. Source: AA A13, src 18 (plaintiff-side; carrier programs not public).
-- **Soft-tissue injury** — sprain/strain/whiplash-type injury without fracture or neurological deficit; often lacks objective findings. Source: AA A9, src 18.
+- **Soft-tissue injury** — sprained or strained neck or back (the most common MIST injuries per src 18); often lacks objective findings. Source: AA A9, src 18. "No fracture or neurological deficit" as a defining limit: **assumption**.
 - **Active vs passive care** — exercise-based therapy vs modalities applied to the patient (heat, massage, e-stim); adjusters discount long passive care. Source: AA A15, src 1.
 - **Value drivers** — the claim features (injury type, treatment duration, objective findings, impairment) that claim-valuation software such as Colossus scores. Source: AA src 3 (second-hand).
 - **Gap in treatment** — period without care between dates of service; adjusters argue recovery or an intervening cause. Prototype threshold >30 days is the Zlayt spec's, not an industry rule. Source: AA src 1, 4.
diff --git a/research/ASSUMPTIONS-proposed.md b/research/ASSUMPTIONS-proposed.md
index 61c6678..1aee616 100644
--- a/research/ASSUMPTIONS-proposed.md
+++ b/research/ASSUMPTIONS-proposed.md
@@ -8,17 +8,17 @@ Each has evidence (research file + source #) and a confidence. CP / AA / TX = ch
 | P-01 | The paralegal assembles the chronology; an LNC may interpret clinical meaning on larger cases; the attorney decides what goes in the demand and signs it. | CP src 1, 8, 9 | Medium (vendor + bar blog) | A-101 |
 | P-02 | A treatment gap is measured between consecutive dates of service across **all** providers (case-level), and the 30-day threshold comes from the Zlayt spec, not an industry rule — make it configurable. | AA src 1, 4, 5 (no source sets a number); spec | High for "case-level"; threshold is spec-given | A-102 |
 | P-03 | The chronology feeds the medical-treatment section of a **pre-suit** demand to the at-fault driver's liability carrier (Texas is an at-fault state). | CP src 5; TX §7 | Medium | A-103 |
-| P-04 | Demands are usually sent after MMI/completion; the Rivera records are mid-treatment (ESI only recommended), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
+| P-04 | Demands are usually sent after MMI/completion; the Rivera records end mid-treatment (rec 9: "Recommend cervical epidural steroid injection", recommended, not performed), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
 | P-05 | Dollar amounts in clinical notes are **billed** charges; the tool must never label the total "damages" or "recoverable" because Texas limits recovery to paid/incurred amounts (Haygood). | TX src 1 | High (primary law) | new |
 | P-06 | Surfacing a gap, prior condition or conflict is the tool's job; deciding whether and how to explain it in the letter is the attorney's. Hiding a known weakness costs credibility with adjusters. | CP src 1; AA src 5, 15 | Medium-high | new |
 | P-07 | A patient's statement that symptoms began after the collision is history, not a causation opinion; Texas generally requires expert testimony for causation. The tool attributes it ("patient states") and never restates it as fact. | AA src 9, 11 | High (primary law) | new |
 | P-08 | Hedged imaging language ("may represent degenerative change; correlate clinically") is equivocal by design; adjusters read it as pre-existing, plaintiffs as aggravation. The tool preserves the hedge verbatim and flags it. | AA src 6, 7, 8 | High | new |
 | P-09 | Missed appointments/early discharge are review flags (mitigation is the defendant's burden and outcomes vary), not conclusions. | AA src 13, 14 | Medium | new |
 | P-10 | A second, different accident date in any record is material — defense uses it to suggest a different incident (JLG Trucking). Both dates must be surfaced; neither is "corrected". | AA src 10, 17 | High | new |
-| P-11 | A prior condition in a **different body region** (2023 low back vs 2026 neck) is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
+| P-11 | A prior condition in a **different body region** (rec 3 "Patient reports low back pain in 2023, resolved" vs rec 3 "Persistent neck pain 6/10") is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
 | P-12 | Firms cite records by Bates/page; the prototype's record # + verbatim excerpt stands in for that. | TX src 8; CP src 1 | Low-medium (assumption) | new |
 | P-13 | Paralegals at PI firms are not covered by a single chronology standard; conventions vary by firm, so the export format should be plain, editable text, not a fixed template. | CP src 9 (no standard found) | Medium | new |
-| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera 01-09 vs 01-19), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
+| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera: rec 7 "Date of accident per intake form: 2026-01-19" vs treatment records dated 2026-01-09 that state no accident date), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
 | P-15 | Scene and mechanism facts (speed, transport, ambulatory, vehicle damage) usually appear only in EMS/police records, and they cut both ways. Surface them as internal-notes flags (D-018/D-001), never as letter text chosen by the tool. | adjuster-attacks.md A13 (src 1) | Medium | new |
 
 Not proposed (insufficient evidence): any number for time spent per chronology or for settlement-value impact of
diff --git a/research/adjuster-attacks.md b/research/adjuster-attacks.md
index be9406c..151110e 100644
--- a/research/adjuster-attacks.md
+++ b/research/adjuster-attacks.md
@@ -19,20 +19,20 @@ lexicon's former `causation_weakening` and `compliance` both map to `causation`.
 | # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
 |---|---|---|---|---|---|
 | A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
-| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments"; 12 planned vs 9 | causation + conflict |
+| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9") vs rec 4 "Plan of care: 12 visits" | causation + conflict |
 | A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
 | A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation |
 | A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation |
 | A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation |
-| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs EMS/ER 2026-01-09 | conflict (code) |
-| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm" after 73-day gap | causation |
-| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Pain 7/10 → 3/10 subjective; objective: "Cervical range of motion reduced approx. 40%" (rec 4), CT negative (rec 2), MRI C5-C6 (rec 8) | (context; not a required flag) |
+| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs rec 1 (EMS) and rec 2 (ER), whose header dates are 2026-01-09; neither excerpt states an accident date | conflict (code) |
+| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm"; header date 2026-05-18, 73 days after rec 6 (2026-03-06), by code date arithmetic | causation |
+| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Subjective: rec 1 "C/O neck pain 7/10", rec 6 "Pain 3/10"; objective: rec 4 "Cervical range of motion reduced approx. 40%", rec 2 "CT head negative", rec 8 "C5-C6 disc protrusion with mild right foraminal narrowing" | (context; not a required flag) |
 | A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | PT rate $185/visit with no visit count → cannot total | amounts (code) |
 | A11 | **Prior claims history** | ISO ClaimSearch shows earlier injury claims | 2 | Not in records — out of scope for the tool | — |
-| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. (EMS/ER give accident 01-09; rec 7 says 01-19.) | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
+| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. Only rec 7 states an accident date ("Date of accident per intake form: 2026-01-19"); records 1–2 state none | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
 | A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at scene or refused transport → no injury | 1, 3, 18 | Rec 1 "rear-ended at approx. 35 mph", "Transported to Central ER" (both *help* the claimant). No vehicle-damage facts in the records | causation (lexicon: scene facts such as ambulatory at scene, refused transport, minimal damage — D-018) |
-| A14 | **Attorney involvement / LOP-funded care** | Care began or escalated after the attorney was retained; charges inflated under a letter of protection | 1, TX §3 (K&L), 3 | Not in records. Rivera's pain-management intake (rec 7) comes 73 days after PT; the records do not say who referred him | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
-| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | PT plan "12 visits" (rec 4), discharged at visit 9 (rec 6); active care (PT, referral to pain management, ESI recommended) | context only — not a required flag; duration is visible from the timeline itself |
+| A14 | **Attorney involvement / LOP-funded care** | Counsel steered the claimant to high-cost providers; charges inflated under a letter of protection; (assumption) care began or escalated after the attorney was retained | 20, TX §3 (K&L); retention timing = assumption | Not in records. Rec 7 is a "new patient" visit dated 2026-05-18; no record states a referral source or an attorney | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
+| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | Rec 4 "Plan of care: 12 visits"; rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9"); records 4–6 name no PT modality, so active vs passive is not stated; rec 7 "Hill Country Pain Management, new patient", no referral source stated; rec 9 "Recommend cervical epidural steroid injection" (recommended, not performed) | context only — not a required flag; duration is visible from the timeline itself |
 
 ## Notes per attack
 
@@ -56,7 +56,8 @@ False-positive risk: "denies prior neck injury" is a *negative* — it must not
 reviewed **lumbar** imaging: disc bulge prevalence rose from ~30% at age 20 to ~84% at 80, protrusion from 29% to
 43% (src 6). It says nothing directly about the neck. For the **cervical** spine, Nakashima et al. (Spine 2015,
 1,211 asymptomatic volunteers aged 20–70) found disc bulging in 87.6% overall and in most subjects in their 20s.
-Bulging increased with age, and cord compression was uncommon (5.3%) and concentrated at C5-C6 (src 19). The
+Bulging increased with age; cord compression was uncommon (5.3%) and most often at C5-C6 (41% of compressions) (src 19). The
+study measured bulging, not protrusion, in Japanese volunteers. The
 defense uses this kind of evidence to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
 radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
 equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
@@ -77,9 +78,10 @@ The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.
 
 **A12 Delay to first treatment.** The insurer-side checklist asks "How soon did treatment start?" before it asks
 about gaps (src 1). In the Virginia record-review case the defense relied on a report made "eight days later"
-(src 16). Rivera went from EMS to the ER the same day (2026-01-09). That helps him, and the paralegal should see
-it. Per D-017 the tool does not compute a delay from an accident date, because the records give two accident dates
-and the tool must never pick one. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
+(src 16). Rivera's EMS run report (rec 1, "Transported to Central ER.") and ER discharge summary (rec 2) both carry
+the header date 2026-01-09. That helps him, and the paralegal should see it. Per D-017 the tool does not compute a
+delay from an accident date: the only stated accident date is rec 7's "2026-01-19", which is later than the first
+recorded treatment, and the tool must never pick a date. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
 against whichever accident date the facts support.
 
 **A13 Mechanism / MIST.** Src 1 lists the police report (transported?), vehicle photos (does the damage match? what
@@ -88,14 +90,20 @@ a category by many carriers (src 18, plaintiff-side; carrier MIST programs are n
 scene facts live: speed, restraint, airbag deployment, ambulatory at scene, refused transport. Per D-018 those
 phrases are `causation` flags citing the excerpt, and they go to the internal notes only (D-001).
 
-**A14 Attorney involvement / LOP.** Src 1 asks about provider type and credentials. Texas made providers'
-negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). Adjusters
-compare the attorney-retention date with when care started or escalated. The tool cannot know the retention date
-from medical records, so it flags only what a record says ("referred by attorney", "letter of protection").
+**A14 Attorney involvement / LOP.** An insurer-side trade article describes providers, attorneys and clinics that
+"steer claimants into higher cost services", with plaintiffs' counsel referring claimants to pain-management
+centers, and says defense counsel then "may challenge causation or necessity" (src 20). Texas made providers'
+negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). **Assumption
+(adjuster practice; claims-adjuster persona §2, no source found):** adjusters compare the attorney-retention date
+with when care started or escalated. The tool cannot know the retention date from medical records, so it flags
+only what a record says ("referred by attorney", "letter of protection"). Rivera's records name no referral source.
 
 **A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
-anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). Rivera's
-care is active and shorter than planned. This is context for the adjuster persona, not a required flag.
+anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). For Rivera
+the records do not say whether PT was active or passive: records 4–6 name no modality. They do support "shorter than
+planned": rec 4 "Plan of care: 12 visits", and rec 6 "Discharged from PT after two missed appointments" under the
+source label "Capital PT, visit 9". The ESI is only recommended (rec 9). This is context for the adjuster persona, not
+a required flag.
 
 **A9 Subjective vs objective.** Adjusters weigh objective findings (imaging, ROM measurements, spasm) above pain
 scores (src 1, 18). Not a required flag; useful for the one-line summary (keep numbers verbatim) and for the
@@ -138,7 +146,9 @@ see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcodin
 17. Georgia Court of Appeals decision on impeachment with prior intake forms — https://caselaw.findlaw.com/court/ga-court-of-appeals/1418582.html — Defense may impeach with the claimant's own medical intake forms listing prior accidents/complaints. (Primary, non-Texas; via search summary.)
 18. Braun Law, "Objective vs. Subjective" — https://braunslaw.com/claimclinic/claim-worth/specific-injuries/ — Claim evaluation software weighs objective injuries more heavily. (Plaintiff firm.)
 
-19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of the cervical spines in 1211 asymptomatic subjects," Spine 40(6):392–398 (2015) — https://pubmed.ncbi.nlm.nih.gov/25584950/ — Cervical disc bulging in 87.6% of asymptomatic adults aged 20–70, most already in their 20s; cord compression 5.3%, mostly at C5-C6. (Peer-reviewed; abstract figures via search index.)
+19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of the cervical spines in 1211 asymptomatic subjects," Spine 40(6):392–398 (2015) — https://pubmed.ncbi.nlm.nih.gov/25584950/ — Cervical disc bulging in 87.6% of asymptomatic adults aged 20–70, most already in their 20s; cord compression 5.3%, most often at C5-C6 (41%) and C6-C7 (27%). The study measured disc bulging (not protrusion) in Japanese volunteers. (Peer-reviewed; abstract figures confirmed by the claims-adjuster reviewer via NCBI efetch.)
+
+20. Insurance Journal, P. Dhakal, "Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims" (2026-01-21) — https://www.insurancejournal.com/news/national/2026/01/21/854959.htm — Insurer-side view: referral networks "steer claimants into higher cost services"; plaintiffs' counsel refer claimants to pain-management centers; defense "may challenge causation or necessity". Says nothing about retention timing or LOPs. (Insurance trade press, opinion piece.)
 
 Assumptions where sources are thin: (a) no public adjuster manual quantifies how much each attack reduces value;
 (b) Colossus specifics are second-hand; (c) the 30-day gap threshold is the Zlayt spec's, not an industry rule —
diff --git a/research/chronology-practice.md b/research/chronology-practice.md
index 42c2bc4..f2b2334 100644
--- a/research/chronology-practice.md
+++ b/research/chronology-practice.md
@@ -16,7 +16,7 @@ the conventions below as *industry practice*, not rules. Where all vendors agree
   and the summary as the demand letter's "medical treatment" section. (Sources 1, 2.)
 - **When it is built.** Usually after the client reaches maximum medical improvement (MMI) or finishes
   treatment, so the demand can state total specials; earlier for policy-limits cases. (Source 2.) Our sample
-  case is mid-treatment (an epidural steroid injection is only *recommended* on 2026-06-12) — the export must
+  case is mid-treatment (rec 9, dated 2026-06-12: "Recommend cervical epidural steroid injection", recommended, not performed) — the export must
   not imply treatment is complete. **Assumption** (see ASSUMPTIONS-proposed P-04).
 - **Who builds it.** Paralegal or case manager; nurse/LNC on larger cases; attorney reviews and signs the
   demand. Chronologies "do not decide causation" — they display the documented sequence; causation opinions
diff --git a/research/texas-pi-notes.md b/research/texas-pi-notes.md
index d8fd091..0bd9f78 100644
--- a/research/texas-pi-notes.md
+++ b/research/texas-pi-notes.md
@@ -1,7 +1,7 @@
 # Texas PI norms relevant to billed charges and medical records
 
 Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
-Scenario: Zinda Law Group (Austin), fictional client Jordan Rivera, Austin MVA 2026-01-09. **Not legal advice**;
+Scenario: Zinda Law Group (Austin), fictional client Jordan Rivera, rear-ended in Austin (spec Appendix A); first records dated 2026-01-09. **Not legal advice**;
 this is product research so the prototype does not mislead a Texas paralegal.
 
 Method note: statutes.capitol.texas.gov renders only navigation to our fetch tool, so statute text was read via
@@ -55,7 +55,7 @@ mirrors (rulesofcivilprocedure.com, texas.public.law) and cross-checked against
 - §55.004(b): a hospital lien is for the lesser of charges for the first 100 days of hospitalization or 50% of
   the patient's recovery (or the awarded hospital charges less a proportional share of fees). §55.004(f): an
   EMS lien may not exceed $1,000 and covers services within 72 hours after the accident. (Src 7 — mirror text.)
-- Rivera has an EMS transport (record 1, no charge shown) and an ER visit ($6,240). **Assumption:** whether
+- Rivera has an EMS transport (rec 1 "Transported to Central ER.", no charge stated) and an ER visit (rec 2 "ER charges: $6,240."). **Assumption:** whether
   Central ER/Austin EMS filed liens is unknowable from clinical excerpts; lien tracking is a settlement-stage
   task, out of scope. County-population and filing-requirement details were **not verified** (official page
   unreadable to our tool; secondary sources conflict).
commit da17ba2c2b622a003fa3d7326a72bffa0c5fa5fd
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 18:56:06 2026 -0600

    docs(research): T-008 round 3 — quote-anchor every sample-case claim; drop invented referral and 'active care'
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 memory/GLOSSARY.md               |  2 +-
 research/ASSUMPTIONS-proposed.md |  6 +++---
 research/adjuster-attacks.md     | 46 ++++++++++++++++++++++++----------------
 research/chronology-practice.md  |  2 +-
 research/texas-pi-notes.md       |  4 ++--
 5 files changed, 35 insertions(+), 25 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:20.330Z

**tool call — Bash**
````
{
 "command": "cat -n evals/golden/sample.txt; grep -n -i \"rivera\\|record 1\\|Austin EMS\\|35 mph\\|rear-ended\" spec/SPEC.md | head -40",
 "description": "Read sample records and spec references"
}
````

### User / tool · 2026-11-02T00:57:20.416Z

**tool result**
````
     1	SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data
     2	
     3	=== Record 1 ===
     4	Date: 2026-01-09
     5	Source: Austin EMS run report
     6	Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
     7	
     8	=== Record 2 ===
     9	Date: 2026-01-09
    10	Source: Central ER discharge summary
    11	Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
    12	
    13	=== Record 3 ===
    14	Date: 2026-01-16
    15	Source: Dr. Alvarez, primary care
    16	Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."
    17	
    18	=== Record 4 ===
    19	Date: 2026-01-23
    20	Source: Capital PT, initial evaluation
    21	Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."
    22	
    23	=== Record 5 ===
    24	Date: 2026-02-20
    25	Source: Capital PT, visit 8
    26	Excerpt: "Pain 4/10, improving. Patient reports missing 3 days of work."
    27	
    28	=== Record 6 ===
    29	Date: 2026-03-06
    30	Source: Capital PT, visit 9
    31	Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."
    32	
    33	=== Record 7 ===
    34	Date: 2026-05-18
    35	Source: Hill Country Pain Management, new patient
    36	Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."
    37	
    38	=== Record 8 ===
    39	Date: 2026-05-29
    40	Source: Austin Imaging, cervical MRI
    41	Excerpt: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."
    42	
    43	=== Record 9 ===
    44	Date: 2026-06-12
    45	Source: Hill Country Pain Management, follow-up
    46	Excerpt: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
    47	
53:Fictional case: Jordan Rivera, 41, rear-ended at a red light in Austin. These records are intentionally imperfect, like real ones.
57:| 1 | 2026-01-09 | Austin EMS run report | "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:25.198Z

**tool call — Bash**
````
{
 "command": "ls research/; sed -n 45,70p spec/SPEC.md; grep -n -i -E \"rivera|\\brec(ord)?s? ?[0-9]|sample case|2026-0[1-6]|\\\\\\$[0-9]|C5-C6|73[- ]day|Capital PT|Hill Country|Alvarez|Central ER|Austin (EMS|Imaging)\" research/*.md | grep -v \"^research/lexicon\" | wc -l",
 "description": "List research files, spec Appendix A, count hits"
}
````

### User / tool · 2026-11-02T00:57:25.305Z

**tool result**
````
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
chronology-practice.md
lexicon_selfcheck.py
phi-and-ai-supervision.md
texas-pi-notes.md

#### Constraints
- Use an LLM for at least one step. Everything else can be ordinary code, and we want to see where you drew that line and why. For example, date arithmetic is a decision, not a given.
- The output must contain nothing that is not in the records. Do not let the tool invent medical facts.
- Any stack and any hosting. We must be able to run it from a link, or from your repo in under 5 minutes.
- Time-box it. Cut scope on purpose and tell us what you cut.

#### Sample records (synthetic)
Fictional case: Jordan Rivera, 41, rear-ended at a red light in Austin. These records are intentionally imperfect, like real ones.

| # | Date | Source | Excerpt |
|---|---|---|---|
| 1 | 2026-01-09 | Austin EMS run report | "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." |
| 2 | 2026-01-09 | Central ER discharge summary | "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240." |
| 3 | 2026-01-16 | Dr. Alvarez, primary care | "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved." |
| 4 | 2026-01-23 | Capital PT, initial evaluation | "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185." |
| 5 | 2026-02-20 | Capital PT, visit 8 | "Pain 4/10, improving. Patient reports missing 3 days of work." |
| 6 | 2026-03-06 | Capital PT, visit 9 | "Discharged from PT after two missed appointments. Pain 3/10." |
| 7 | 2026-05-18 | Hill Country Pain Management, new patient | "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19." |
| 8 | 2026-05-29 | Austin Imaging, cervical MRI | "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150." |
| 9 | 2026-06-12 | Hill Country Pain Management, follow-up | "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision." |

#### What to submit for Part 1
- A link to the working prototype, or a repo with run instructions.
- A demo of 3 minutes or less (screen recording), or annotated screenshots.
- A one-page product note covering: the problem and user, what you built, and what you deliberately cut and why; your "good enough to ship" bar: 3 to 5 testable criteria, how you tested the prototype against them, and what you found; where the AI can fail or mislead a paralegal, and how the design handles it; how you split the work between the model and ordinary code; three metrics you would track after launch, and what each one tells you.
      47
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:27.289Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"rivera|\\brec(ord)?s? ?[0-9]|sample case|sample records|2026-0[1-6]|\\\\\\$[0-9]|C5-C6|73[- ]day|Capital PT|Hill Country|Alvarez|Central ER|Austin (EMS|Imaging)|41-year|cyclobenzaprine|35 mph\" research/*.md",
 "description": "List every sample-case hit in research files"
}
````

### User / tool · 2026-11-02T00:57:27.372Z

**tool result**
````
research/ASSUMPTIONS-proposed.md:11:| P-04 | Demands are usually sent after MMI/completion; the Rivera records end mid-treatment (rec 9: "Recommend cervical epidural steroid injection", recommended, not performed), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
research/ASSUMPTIONS-proposed.md:18:| P-11 | A prior condition in a **different body region** (rec 3 "Patient reports low back pain in 2023, resolved" vs rec 3 "Persistent neck pain 6/10") is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
research/ASSUMPTIONS-proposed.md:21:| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera: rec 7 "Date of accident per intake form: 2026-01-19" vs treatment records dated 2026-01-09 that state no accident date), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
research/chronology-practice.md:5:what that implies for the prototype. Synthetic case only (Jordan Rivera, spec Appendix A).
research/chronology-practice.md:19:  case is mid-treatment (rec 9, dated 2026-06-12: "Recommend cervical epidural steroid injection", recommended, not performed) — the export must
research/adjuster-attacks.md:14:## Attack map, applied to the Jordan Rivera sample
research/adjuster-attacks.md:19:| # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
research/adjuster-attacks.md:21:| A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
research/adjuster-attacks.md:22:| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9") vs rec 4 "Plan of care: 12 visits" | causation + conflict |
research/adjuster-attacks.md:23:| A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
research/adjuster-attacks.md:24:| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation |
research/adjuster-attacks.md:25:| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation |
research/adjuster-attacks.md:26:| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation |
research/adjuster-attacks.md:27:| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs rec 1 (EMS) and rec 2 (ER), whose header dates are 2026-01-09; neither excerpt states an accident date | conflict (code) |
research/adjuster-attacks.md:28:| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm"; header date 2026-05-18, 73 days after rec 6 (2026-03-06), by code date arithmetic | causation |
research/adjuster-attacks.md:29:| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Subjective: rec 1 "C/O neck pain 7/10", rec 6 "Pain 3/10"; objective: rec 4 "Cervical range of motion reduced approx. 40%", rec 2 "CT head negative", rec 8 "C5-C6 disc protrusion with mild right foraminal narrowing" | (context; not a required flag) |
research/adjuster-attacks.md:30:| A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | PT rate $185/visit with no visit count → cannot total | amounts (code) |
research/adjuster-attacks.md:32:| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. Only rec 7 states an accident date ("Date of accident per intake form: 2026-01-19"); records 1–2 state none | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
research/adjuster-attacks.md:33:| A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at scene or refused transport → no injury | 1, 3, 18 | Rec 1 "rear-ended at approx. 35 mph", "Transported to Central ER" (both *help* the claimant). No vehicle-damage facts in the records | causation (lexicon: scene facts such as ambulatory at scene, refused transport, minimal damage — D-018) |
research/adjuster-attacks.md:34:| A14 | **Attorney involvement / LOP-funded care** | Counsel steered the claimant to high-cost providers; charges inflated under a letter of protection; (assumption) care began or escalated after the attorney was retained | 20, TX §3 (K&L); retention timing = assumption | Not in records. Rec 7 is a "new patient" visit dated 2026-05-18; no record states a referral source or an attorney | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
research/adjuster-attacks.md:35:| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | Rec 4 "Plan of care: 12 visits"; rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9"); records 4–6 name no PT modality, so active vs passive is not stated; rec 7 "Hill Country Pain Management, new patient", no referral source stated; rec 9 "Recommend cervical epidural steroid injection" (recommended, not performed) | context only — not a required flag; duration is visible from the timeline itself |
research/adjuster-attacks.md:59:Bulging increased with age; cord compression was uncommon (5.3%) and most often at C5-C6 (41% of compressions) (src 19). The
research/adjuster-attacks.md:61:defense uses this kind of evidence to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
research/adjuster-attacks.md:77:The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.
research/adjuster-attacks.md:81:(src 16). Rivera's EMS run report (rec 1, "Transported to Central ER.") and ER discharge summary (rec 2) both carry
research/adjuster-attacks.md:82:the header date 2026-01-09. That helps him, and the paralegal should see it. Per D-017 the tool does not compute a
research/adjuster-attacks.md:83:delay from an accident date: the only stated accident date is rec 7's "2026-01-19", which is later than the first
research/adjuster-attacks.md:84:recorded treatment, and the tool must never pick a date. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
research/adjuster-attacks.md:99:only what a record says ("referred by attorney", "letter of protection"). Rivera's records name no referral source.
research/adjuster-attacks.md:102:anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). For Rivera
research/adjuster-attacks.md:103:the records do not say whether PT was active or passive: records 4–6 name no modality. They do support "shorter than
research/adjuster-attacks.md:104:planned": rec 4 "Plan of care: 12 visits", and rec 6 "Discharged from PT after two missed appointments" under the
research/adjuster-attacks.md:105:source label "Capital PT, visit 9". The ESI is only recommended (rec 9). This is context for the adjuster persona, not
research/adjuster-attacks.md:149:19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of the cervical spines in 1211 asymptomatic subjects," Spine 40(6):392–398 (2015) — https://pubmed.ncbi.nlm.nih.gov/25584950/ — Cervical disc bulging in 87.6% of asymptomatic adults aged 20–70, most already in their 20s; cord compression 5.3%, most often at C5-C6 (41%) and C6-C7 (27%). The study measured disc bulging (not protrusion) in Japanese volunteers. (Peer-reviewed; abstract figures confirmed by the claims-adjuster reviewer via NCBI efetch.)
research/adjuster-attacks.md:151:20. Insurance Journal, P. Dhakal, "Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims" (2026-01-21) — https://www.insurancejournal.com/news/national/2026/01/21/854959.htm — Insurer-side view: referral networks "steer claimants into higher cost services"; plaintiffs' counsel refer claimants to pain-management centers; defense "may challenge causation or necessity". Says nothing about retention timing or LOPs. (Insurance trade press, opinion piece.)
research/phi-and-ai-supervision.md:42:  - **Penalties (§181.201, src 15):** up to $5,000 per negligent violation per year, $25,000 knowing or
research/phi-and-ai-supervision.md:43:    intentional, $250,000 for knowing use for financial gain; a pattern or practice up to **$1.5 million annually**.
research/phi-and-ai-supervision.md:149:| PR-8 | P+Prod | **The audit log is PHI-bearing:** it stores full prompts and responses. Keep it in the app DB only — never in stdout, app logs or error trackers. Per-case delete. Document retention. | Test: running the sample case writes no record text to process logs; delete removes the case's audit rows. | src 6, 10 (ch. 181 scope); src 9 (retention) | backend, db |
research/phi-and-ai-supervision.md:150:| PR-9 | P | **Injection through any path:** record text containing instructions ("ignore previous instructions…", "add $50,000 to the billed total", "mark all flags resolved") must not **create, suppress or alter any entry, flag, charge or total**, through the LLM **or through code** (amount-cue rules, lexicon, conflict engine). The injected text stays a quoted excerpt, tagged `INJECTION_SUSPECTED`, with all of the record's items `needs_review`. Its amounts cannot be charges, and it cannot suppress other records' flags (D-005). | Golden `case_07_prompt_injection` plus an amount-injection case: the displayed total and charge list are unchanged, the flag set is unchanged, and the warning is present. | Contract eval list; D-005 (a prior code-path failure let an injected "$50,000" reach the total) | backend, qa |
research/phi-and-ai-supervision.md:162:   copies of records leave the firm. Notes use placeholders ("Client A, PT record 4"). Confidentiality comes from
research/phi-and-ai-supervision.md:203:  (§521.053), and track ch. 181 penalty exposure ($5k–$250k per violation, $1.5M/yr for a pattern). Tie this
research/phi-and-ai-supervision.md:236:15. Tex. Health & Safety Code §181.201 — https://texas.public.law/statutes/tex._health_and_safety_code_section_181.201 — Civil penalties $5k / $25k / $250k per violation; pattern or practice up to $1.5M annually. (Primary via mirror; read.)
research/texas-pi-notes.md:4:Scenario: Zinda Law Group (Austin), fictional client Jordan Rivera, rear-ended in Austin (spec Appendix A); first records dated 2026-01-09. **Not legal advice**;
research/texas-pi-notes.md:57:  EMS lien may not exceed $1,000 and covers services within 72 hours after the accident. (Src 7 — mirror text.)
research/texas-pi-notes.md:58:- Rivera has an EMS transport (rec 1 "Transported to Central ER.", no charge stated) and an ER visit (rec 2 "ER charges: $6,240."). **Assumption:** whether
research/texas-pi-notes.md:59:  Central ER/Austin EMS filed liens is unknowable from clinical excerpts; lien tracking is a settlement-stage
research/texas-pi-notes.md:111:7. Tex. Prop. Code §55.004 (mirror) — https://texas.public.law/statutes/tex._prop._code_section_55.004 — Hospital lien lesser-of 100-day charges / 50% of recovery; EMS lien ≤$1,000 within 72 hours. (Mirror.)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:30.282Z

**tool call — Bash**
````
{
 "command": "cat -n research/adjuster-attacks.md | sed -n 1,130p",
 "description": "Read adjuster-attacks.md body"
}
````

### User / tool · 2026-11-02T00:57:30.363Z

**tool result**
````
     1	# What adjusters and defense counsel attack in a treatment chronology
     2	
     3	Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
     4	Purpose: ground the four required flags (gap, conflict, prior/pre-existing, causation-weakening language), the
     5	claims-adjuster reviewer persona, and `app/llm/lexicon.yaml`.
     6	
     7	**Source balance.** Plaintiff-firm blogs dominate search results. We deliberately added insurer-side and
     8	neutral sources: Claims Journal (adjuster trade press, src 1), Verisk/ISO (insurer data vendor, src 2), Texas
     9	Supreme Court opinions (srcs 9–12), and peer-reviewed radiology literature (srcs 6–8). Colossus internals are
    10	proprietary; claims about it are second-hand (src 3) and labeled as such.
    11	**Read depth.** Sources 1 and 12 were fetched and read in full; the rest were assessed from search-engine
    12	excerpts of the page (the takeaway lines quote only what the excerpt showed). Verify before quoting externally.
    13	
    14	## Attack map, applied to the Jordan Rivera sample
    15	
    16	Flag-type column uses the D-013 vocabulary (`gap`, `conflict`, `pre_existing`, `causation`, `record_warning`); the
    17	lexicon's former `causation_weakening` and `compliance` both map to `causation`.
    18	
    19	| # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
    20	|---|---|---|---|---|---|
    21	| A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
    22	| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9") vs rec 4 "Plan of care: 12 visits" | causation + conflict |
    23	| A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
    24	| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation |
    25	| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation |
    26	| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation |
    27	| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs rec 1 (EMS) and rec 2 (ER), whose header dates are 2026-01-09; neither excerpt states an accident date | conflict (code) |
    28	| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm"; header date 2026-05-18, 73 days after rec 6 (2026-03-06), by code date arithmetic | causation |
    29	| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Subjective: rec 1 "C/O neck pain 7/10", rec 6 "Pain 3/10"; objective: rec 4 "Cervical range of motion reduced approx. 40%", rec 2 "CT head negative", rec 8 "C5-C6 disc protrusion with mild right foraminal narrowing" | (context; not a required flag) |
    30	| A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | PT rate $185/visit with no visit count → cannot total | amounts (code) |
    31	| A11 | **Prior claims history** | ISO ClaimSearch shows earlier injury claims | 2 | Not in records — out of scope for the tool | — |
    32	| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. Only rec 7 states an accident date ("Date of accident per intake form: 2026-01-19"); records 1–2 state none | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
    33	| A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at scene or refused transport → no injury | 1, 3, 18 | Rec 1 "rear-ended at approx. 35 mph", "Transported to Central ER" (both *help* the claimant). No vehicle-damage facts in the records | causation (lexicon: scene facts such as ambulatory at scene, refused transport, minimal damage — D-018) |
    34	| A14 | **Attorney involvement / LOP-funded care** | Counsel steered the claimant to high-cost providers; charges inflated under a letter of protection; (assumption) care began or escalated after the attorney was retained | 20, TX §3 (K&L); retention timing = assumption | Not in records. Rec 7 is a "new patient" visit dated 2026-05-18; no record states a referral source or an attorney | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
    35	| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | Rec 4 "Plan of care: 12 visits"; rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9"); records 4–6 name no PT modality, so active vs passive is not stated; rec 7 "Hill Country Pain Management, new patient", no referral source stated; rec 9 "Recommend cervical epidural steroid injection" (recommended, not performed) | context only — not a required flag; duration is visible from the timeline itself |
    36	
    37	## Notes per attack
    38	
    39	**A1 Gaps.** The adjuster checklist in Claims Journal names "treatment timing and gaps" explicitly (src 1).
    40	Colossus is reported to score duration and frequency per injury (src 3, second-hand). Plaintiff firms say even
    41	short gaps are used (src 4, 5). Nothing authoritative sets 30 days; the 30-day threshold is the Zlayt spec's.
    42	Practitioners advise *explaining* a gap rather than hiding it (src 5) → the tool flags, the lawyer explains.
    43	
    44	**A2 Missed appointments.** Mitigation is an affirmative defense — the defendant bears the burden and must show
    45	the failure increased damages (src 13). Courts split on outcomes: an instruction was justified where >12 PT
    46	sessions were missed (Herrera v. Madrak, src 14) but not where the plaintiff had reasons (Fletcher v. Simmons,
    47	same source). So "two missed appointments" is a *review* flag, not a conclusion. The 12-planned-vs-discharged-at-9
    48	discrepancy is a conflict an adjuster will see immediately.
    49	
    50	**A3 Prior conditions.** Verisk sells ISO ClaimSearch to let adjusters "identify preexisting or subsequent injury"
    51	(src 2). Concealing priors is described as a credibility killer (src 15). Even a *resolved, different-region*
    52	prior (2023 low back vs 2026 neck) must be surfaced; the paralegal decides relevance.
    53	False-positive risk: "denies prior neck injury" is a *negative* — it must not be flagged as a prior condition.
    54	
    55	**A4/A5 Degenerative findings and hedges.** Brinjikji et al. (AJNR 2015, 33 studies, 3,110 asymptomatic people)
    56	reviewed **lumbar** imaging: disc bulge prevalence rose from ~30% at age 20 to ~84% at 80, protrusion from 29% to
    57	43% (src 6). It says nothing directly about the neck. For the **cervical** spine, Nakashima et al. (Spine 2015,
    58	1,211 asymptomatic volunteers aged 20–70) found disc bulging in 87.6% overall and in most subjects in their 20s.
    59	Bulging increased with age; cord compression was uncommon (5.3%) and most often at C5-C6 (41% of compressions) (src 19). The
    60	study measured bulging, not protrusion, in Japanese volunteers. The
    61	defense uses this kind of evidence to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
    62	radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
    63	equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
    64	Radiology literature treats "clinical correlation" and "cannot be excluded" as hedges that shift
    65	interpretation to the clinician (src 7, 8). In Texas, causation testimony must reach *reasonable medical
    66	probability*; possibility language does not (Jelinek v. Casas, src 11, secondary).
    67	
    68	**A6 Patient self-report.** In Texas, lay testimony can prove causation only for conditions within common
    69	knowledge; otherwise expert testimony is required (Guevara v. Ferrer, src 9). A PM-clinic note that the
    70	"patient states symptoms began after the January collision" records history, not a physician's causation
    71	opinion. The export may quote it but must attribute it ("patient states"), never restate it as fact.
    72	
    73	**A7 Inconsistent dates.** Defense impeaches with the claimant's own intake forms (Georgia appeal, src 17);
    74	a treating physician's causation opinion is only as good as the history the patient gave. In
    75	JLG Trucking v. Garza (Tex. 2015) evidence of a *second* accident was relevant to causation and its exclusion
    76	was reversible error (src 10) — a second accident date in the records is exactly what defense counsel looks for.
    77	The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.
    78	
    79	**A12 Delay to first treatment.** The insurer-side checklist asks "How soon did treatment start?" before it asks
    80	about gaps (src 1). In the Virginia record-review case the defense relied on a report made "eight days later"
    81	(src 16). Rivera's EMS run report (rec 1, "Transported to Central ER.") and ER discharge summary (rec 2) both carry
    82	the header date 2026-01-09. That helps him, and the paralegal should see it. Per D-017 the tool does not compute a
    83	delay from an accident date: the only stated accident date is rec 7's "2026-01-19", which is later than the first
    84	recorded treatment, and the tool must never pick a date. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
    85	against whichever accident date the facts support.
    86	
    87	**A13 Mechanism / MIST.** Src 1 lists the police report (transported?), vehicle photos (does the damage match? what
    88	direction was the force?) and mechanism as first-line checks. Minor-impact soft-tissue (MIST) files are handled as
    89	a category by many carriers (src 18, plaintiff-side; carrier MIST programs are not public). EMS run reports are where
    90	scene facts live: speed, restraint, airbag deployment, ambulatory at scene, refused transport. Per D-018 those
    91	phrases are `causation` flags citing the excerpt, and they go to the internal notes only (D-001).
    92	
    93	**A14 Attorney involvement / LOP.** An insurer-side trade article describes providers, attorneys and clinics that
    94	"steer claimants into higher cost services", with plaintiffs' counsel referring claimants to pain-management
    95	centers, and says defense counsel then "may challenge causation or necessity" (src 20). Texas made providers'
    96	negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). **Assumption
    97	(adjuster practice; claims-adjuster persona §2, no source found):** adjusters compare the attorney-retention date
    98	with when care started or escalated. The tool cannot know the retention date from medical records, so it flags
    99	only what a record says ("referred by attorney", "letter of protection"). Rivera's records name no referral source.
   100	
   101	**A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
   102	anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). For Rivera
   103	the records do not say whether PT was active or passive: records 4–6 name no modality. They do support "shorter than
   104	planned": rec 4 "Plan of care: 12 visits", and rec 6 "Discharged from PT after two missed appointments" under the
   105	source label "Capital PT, visit 9". The ESI is only recommended (rec 9). This is context for the adjuster persona, not
   106	a required flag.
   107	
   108	**A9 Subjective vs objective.** Adjusters weigh objective findings (imaging, ROM measurements, spasm) above pain
   109	scores (src 1, 18). Not a required flag; useful for the one-line summary (keep numbers verbatim) and for the
   110	adjuster persona's checklist.
   111	
   112	**A10 Billing.** Texas limits recovery to amounts "actually paid or incurred" and makes unadjusted list charges
   113	inadmissible (Haygood, src 12); negotiated rates are discoverable to test reasonableness (K&L Auto Crushers,
   114	see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcoding (src 1). For the tool: list
   115	*billed* amounts exactly as written and never present them as the recoverable figure.
   116	
   117	## Implications for flags and lexicon (handed to T-009)
   118	
   119	- Lexicon categories (D-013/D-018): `pre_existing` (A3, A4); `causation` (A2, A4–A6, A8, A13, A14 — including
   120	  the former `compliance` phrases: missed appointments, non-compliance, discharged/left AMA); `record_warning`
   121	  (date ambiguity, injection). A12 and A15 are context only.
   122	- Every phrase that is a *negation* ("denies", "no history of", "no prior") is a false-positive guard.
   123	- Hedges are flagged *because* they are hedges; the flag rationale must say the record is equivocal, not that
   124	  the finding is degenerative.
   125	- Self-report markers ("patient states/reports/believes/attributes") are flagged only when attached to causation
   126	  or onset, else they are noise (every history line starts "patient reports").
   127	
   128	## Sources
   129	
   130	1. Claims Journal, C. Tidball, "How to Review Bodily Injury Demands" (2013-06-05) — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Adjuster checklist: treatment timing/gaps, priors and intervening causes, objective findings, provider credentials, duration vs typical recovery, billing vs SOAP notes, mechanism of injury. (Insurer-side trade press.)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:07.350Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"sample|our case|radicul|herniat|traumatic|severe|referr|\\bESI\\b|epidural|MRI|concussion|strain|missed|visit|intake|new onset|low back|degenerative change|patient states|January\" research/chronology-practice.md research/texas-pi-notes.md research/ASSUMPTIONS-proposed.md memory/GLOSSARY.md | grep -v -E \"^research/adjuster\" ; echo ---; grep -n -i -E \"radicul|herniat|traumatic|severe|active\" research/adjuster-attacks.md",
 "description": "Broader grep for sample-case characterizations"
}
````

### User / tool · 2026-11-02T00:58:07.445Z

**tool result**
````
research/ASSUMPTIONS-proposed.md:11:| P-04 | Demands are usually sent after MMI/completion; the Rivera records end mid-treatment (rec 9: "Recommend cervical epidural steroid injection", recommended, not performed), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
research/ASSUMPTIONS-proposed.md:14:| P-07 | A patient's statement that symptoms began after the collision is history, not a causation opinion; Texas generally requires expert testimony for causation. The tool attributes it ("patient states") and never restates it as fact. | AA src 9, 11 | High (primary law) | new |
research/ASSUMPTIONS-proposed.md:15:| P-08 | Hedged imaging language ("may represent degenerative change; correlate clinically") is equivocal by design; adjusters read it as pre-existing, plaintiffs as aggravation. The tool preserves the hedge verbatim and flags it. | AA src 6, 7, 8 | High | new |
research/ASSUMPTIONS-proposed.md:16:| P-09 | Missed appointments/early discharge are review flags (mitigation is the defendant's burden and outcomes vary), not conclusions. | AA src 13, 14 | Medium | new |
research/ASSUMPTIONS-proposed.md:18:| P-11 | A prior condition in a **different body region** (rec 3 "Patient reports low back pain in 2023, resolved" vs rec 3 "Persistent neck pain 6/10") is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
research/ASSUMPTIONS-proposed.md:21:| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera: rec 7 "Date of accident per intake form: 2026-01-19" vs treatment records dated 2026-01-09 that state no accident date), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
research/texas-pi-notes.md:58:- Rivera has an EMS transport (rec 1 "Transported to Central ER.", no charge stated) and an ER visit (rec 2 "ER charges: $6,240."). **Assumption:** whether
research/texas-pi-notes.md:70:- Not verified: how TRE 803(4) (statements for medical diagnosis) applies to "patient states…" lines. Treat
research/chronology-practice.md:18:  treatment, so the demand can state total specials; earlier for policy-limits cases. (Source 2.) Our sample
research/chronology-practice.md:19:  case is mid-treatment (rec 9, dated 2026-06-12: "Recommend cervical epidural steroid injection", recommended, not performed) — the export must
research/chronology-practice.md:33:| Treatment, referrals, plan | 1, 2 | summary | "Recommend ESI" ≠ "received ESI" |
research/chronology-practice.md:46:5. Cross-check bills against treatment dates; a bill with no matching visit (or a visit with no bill) is a
research/chronology-practice.md:65:- R3. The summary must preserve hedges: "may represent degenerative change" stays hedged; "recommend" stays a
research/chronology-practice.md:66:  recommendation; "patient states" stays attributed to the patient.
memory/GLOSSARY.md:24:- **Delay in treatment (delay to first treatment)** — time from the accident to the first medical visit; adjusters' first check. The tool shows only "first recorded treatment" and never computes the delay (D-017). Source: AA A12, src 1, 16.
memory/GLOSSARY.md:26:- **Soft-tissue injury** — sprained or strained neck or back (the most common MIST injuries per src 18); often lacks objective findings. Source: AA A9, src 18. "No fracture or neurological deficit" as a defining limit: **assumption**.
memory/GLOSSARY.md:32:- **Degenerative change** — age-related spinal wear (bulge, protrusion, disc desiccation) common in asymptomatic adults. Source: AA src 6.
memory/GLOSSARY.md:38:- **Subjective vs objective findings** — patient-reported symptoms (pain scores) vs measured or imaged findings (ROM, MRI); adjusters weight objective higher. Source: AA src 1, 18.
memory/GLOSSARY.md:39:- **Patient self-report** — history recorded as "patient states/reports"; records what the patient said, not a physician's causation opinion. Source: AA src 9.
---
35:| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | Rec 4 "Plan of care: 12 visits"; rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9"); records 4–6 name no PT modality, so active vs passive is not stated; rec 7 "Hill Country Pain Management, new patient", no referral source stated; rec 9 "Recommend cervical epidural steroid injection" (recommended, not performed) | context only — not a required flag; duration is visible from the timeline itself |
62:radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
63:equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
101:**A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
103:the records do not say whether PT was active or passive: records 4–6 name no modality. They do support "shorter than
134:5. Young Injury Law, "Gap in medical treatment" — https://younginjurylaw.com/blog/gap-in-medical-treatment-ohio-injury-claim/ — Explain gaps proactively with referral/appointment paperwork; not every pause hurts. (Plaintiff firm.)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:10.201Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json;d=json.load(open('evals/golden/sample.expected.json'))\nfor f in d.get('flags',[]): print(json.dumps(f)[:400])\n\"; grep -n \"D-017\" -A6 memory/ORCHESTRATOR_DECISIONS.md | head -20",
 "description": "Read golden flags and D-017"
}
````

### User / tool · 2026-11-02T00:58:10.328Z

**tool result**
````
{"id": "G1", "type": "gap", "level": "must", "from_date": "2026-03-06", "to_date": "2026-05-18", "days": 73, "cite": {"all": [6, 7], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}, {"record_no": 7, "field": "excerpt", "excerpt": "New onset pain radiating to right arm"}], "summary": "Treatment gap of 73 days (2026-03-06 t
{"id": "C1", "type": "conflict", "level": "must", "cite": {"all": [7], "any": [1, 2]}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}, {"record_no": 1, "field": "date", "excerpt": "2026-01-09"}, {"record_no": 1, "field": "excerpt", "excerpt": "rear-ended at approx. 35 mph"}, {"record_no": 2, "field": "date", "excerpt": "2026-01-09"}], "
{"id": "C2", "type": "conflict", "level": "must", "cite": {"all": [4, 6], "any": []}, "evidence": [{"record_no": 4, "field": "excerpt", "excerpt": "Plan of care: 12 visits"}, {"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Treatment-plan discrepancy: 12 visits planned (record 4) vs discharge at visit 9 after two missed appointments 
{"id": "P1", "type": "pre_existing", "level": "must", "cite": {"all": [3], "any": []}, "evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "Patient reports low back pain in 2023, resolved"}], "summary": "Prior low back pain (2023), reported resolved. Different body region from the cervical complaints; the tool must not relate it to the neck.", "subtype": "prior_condition_reported"}
{"id": "P2", "type": "pre_existing", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "Findings may represent degenerative change"}], "summary": "MRI wording (\"may represent degenerative change\") that an adjuster may argue shows a pre-existing condition; hedged, not a diagnosis.", "subtype": "degenerative_language"}
{"id": "K1", "type": "causation", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "may represent degenerative change; correlate clinically"}], "summary": "Hedged imaging language that an adjuster can use against causation.", "subtype": "hedged_imaging"}
{"id": "K2", "type": "causation", "level": "must", "cite": {"all": [6], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Missed appointments / early discharge weaken the treatment-compliance narrative.", "subtype": "noncompliance"}
{"id": "K3", "type": "causation", "level": "must", "cite": {"all": [9], "any": []}, "evidence": [{"record_no": 9, "field": "excerpt", "excerpt": "Patient states symptoms began after the January collision"}], "summary": "Causation rests on patient self-report, not a physician's causation opinion.", "subtype": "patient_self_report"}
{"id": "K4", "type": "causation", "level": "must", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "New onset pain"}], "summary": "'New onset' symptoms after a 73-day gap can be argued as a new cause. Must be a causation-type flag (see README: type match is explicit); G1 does not satisfy it.", "subtype": "temporal_after_gap"}
{"id": "K5", "type": "causation", "level": "must", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}], "summary": "Wrong accident date on the intake form undermines reliability of the history. Must be a causation-type flag; C1 does not satisfy it.", "subtype": "accident_date_inconsistency"}
25:| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
27-| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29-| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30-| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31-| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:12.195Z

**tool call — Bash**
````
{
 "command": "curl -sS -L -A \"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120 Safari/537.36\" -o artifacts/review-evidence/T-008-r3-insurancejournal-854959.html -w \"HTTP %{http_code} %{size_download} bytes %{url_effective}\\n\" https://www.insurancejournal.com/news/national/2026/01/21/854959.htm",
 "description": "Fetch Insurance Journal source 20"
}
````

### User / tool · 2026-11-02T00:58:12.399Z

**tool result**
````
HTTP 200 103085 bytes https://www.insurancejournal.com/news/national/2026/01/21/854959.htm
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:18.657Z

**tool call — Bash**
````
{
 "command": "python3 -I -c \"\nimport re,html,sys\nt=open(sys.argv[1],encoding='utf-8',errors='replace').read()\nm=re.search(r'<title>(.*?)</title>',t,re.S);print('TITLE:',html.unescape(m.group(1)).strip())\nfor k in ['author','article:published_time','datePublished']:\n  for mm in re.finditer(k+r'[^>]{0,200}',t): print(k,'::',mm.group(0)[:200]);break\nbody=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)\ntxt=html.unescape(re.sub(r'<[^>]+>',' ',body));txt=re.sub(r'\\s+',' ',txt)\nfor q in ['higher cost','steer','pain management','pain-management','causation or necessity','letter of protection','LOP','retain','retention','refer','Dhakal','Viewpoint']:\n  hits=[mm.start() for mm in re.finditer(re.escape(q),txt,re.I)]\n  print('==',q,len(hits))\n  for h in hits[:3]: print('   ',txt[max(0,h-160):h+160])\n\" artifacts/review-evidence/T-008-r3-insurancejournal-854959.html > artifacts/review-evidence/T-008-r3-insurancejournal-checks.txt; cat artifacts/review-evidence/T-008-r3-insurancejournal-checks.txt",
 "description": "Extract and search Insurance Journal article text"
}
````

### User / tool · 2026-11-02T00:58:18.776Z

**tool result**
````
TITLE: Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims
author :: author" content="Pragatee Dhakal" /
article:published_time :: article:published_time" content="2026-01-21T06:19:04+00:00" /
datePublished :: datePublished":"2026-01-21T06:19:04+00:00","mainEntityOfPage":{"@id":"https:\/\/www.insurancejournal.com\/news\/national\/2026\/01\/21\/854959.htm"},"wordCount":1541,"publisher":{"@id":"https:\/\/www.
== higher cost 1
    the referral network, or “treating-provider ecosystem” model, where providers, attorneys and clinics collaborate (sometimes implicitly) to steer claimants into higher cost services. For instance, the regulatory commentary on WC fraud identifies providers or attorneys engaging in referral-based billing as a common schem
== steer 3
    lies that were not actually provided or lacked medical justification. Referral or kick-back schemes : Networks of providers, attorneys, clinics or other actors steering claimants into high-cost modalities or prolonged treatment for financial gain. Misleading or boilerplate provider reports/evaluations : Providers issui
    se in GL/WC lines is the referral network, or “treating-provider ecosystem” model, where providers, attorneys and clinics collaborate (sometimes implicitly) to steer claimants into higher cost services. For instance, the regulatory commentary on WC fraud identifies providers or attorneys engaging in referral-based bill
    eases indemnity cost (especially in WC when treatment prolongs disability). Claims afflicted by medical abuse often last longer. For example, a claimant who is steered into extended therapy or multiple procedures may remain under treatment for months or years, delaying closure. In WC, this extended treatment delays ret
== pain management 0
== pain-management 1
    ii] In GL (e.g., auto liability or general liability bodily injury), the analogous phenomenon is when plaintiffs’ counsel refer injured claimants to clinics or pain-management centers known for high-volume injections, durable medical equipment (DME) orders, or long-term therapy — even when the documented injury might s
== causation or necessity 1
     questionable provider networks also increase litigation and subrogation complexity. When treatment is excessive or questionable, defense counsel may challenge causation or necessity, amplifying legal cost and liability. From a subrogation perspective (particularly in GL claims with third-party liability exposures), in
== letter of protection 0
== LOP 1
    Crypto Insurance Works Some Trends Signal Potential Hope for US Commercial Auto: AM Best Markel Expects to See Runoff Certainty With Enstar’s $1.2B Adverse Development Cover More News Features Read This Next Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims Florida AG Says His Office Investigating 'A
== retain 0
== retention 0
== refer 13
    im contexts, maps how they can distort the claims life cycle, and supports arguments with regulatory and investigative evidence. In this article, medical abuse refers to provider or system behaviors in the adjudication, delivery and billing of medical treatment associated with insured injuries that deviate from accepte
    ted billing/services not rendered : Providers billing for examinations, treatments or supplies that were not actually provided or lacked medical justification. Referral or kick-back schemes : Networks of providers, attorneys, clinics or other actors steering claimants into high-cost modalities or prolonged treatment fo
    on. From a claims management standpoint, this is highly significant: Costs increase without commensurate value, and it may mask or grease other abuses, such as referral schemes and prolonged treatment. Moreover, damages are increased because inflated medical costs may escalate settlement demands. Referral or Kickback S
== Dhakal 3
    ket Directories Quotes Polls Rankings & Awards Insurance Giving Back Subscribe Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims By Pragatee Dhakal | January 21, 2026 Email This Subscribe to Newsletter Article Within the realms of general liability (GL) and workers’ compensation (WC) insurance lines,
     Federal Ban on Intoxicating Hemp Products Will Reshape Risk, Coverage Update: Spanish Train Crash Kills at Least 64 People South of Madrid Written By Pragatee Dhakal Pragatee Dhakal is the director of product strategy and enablement at CLARA Analytics, a leading provider of artificial intelligence (AI) technology for 
    Intoxicating Hemp Products Will Reshape Risk, Coverage Update: Spanish Train Crash Kills at Least 64 People South of Madrid Written By Pragatee Dhakal Pragatee Dhakal is the director of product strategy and enablement at CLARA Analytics, a leading provider of artificial intelligence (AI) technology for insurance claims
== Viewpoint 3
     Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims Skip to content MyNewMarkets.com Claims Journal Insurance Journal TV Academy of Insurance C
    ral Southeast West Magazines Research Directories Jobs Features Events Forums Market Directories Quotes Polls Rankings & Awards Insurance Giving Back Subscribe Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims By Pragatee Dhakal | January 21, 2026 Email This Subscribe to Newsletter Article Within the
    ial Hope for US Commercial Auto: AM Best Markel Expects to See Runoff Certainty With Enstar’s $1.2B Adverse Development Cover More News Features Read This Next Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims Florida AG Says His Office Investigating 'Anti-Public Adjuster' Endorsements in Policies Ho
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:27.778Z

**tool call — Bash**
````
{
 "command": "{ echo '$ grep -rn -i \"referral to pain\\|referred to pain\" research/ memory/'; grep -rn -i \"referral to pain\\|referred to pain\" research/ memory/; echo \"exit $?\"; echo '$ grep -n -i \"care is active\\|active care (\" research/adjuster-attacks.md'; grep -n -i \"care is active\\|active care (\" research/adjuster-attacks.md; echo \"exit $?\"; echo '$ grep -n \"41%\" research/adjuster-attacks.md | cut -c1-80'; grep -n \"41%\" research/adjuster-attacks.md | cut -c1-80; echo '$ grep -cE \"^[0-9]+\\. .*https?://\" research/adjuster-attacks.md research/chronology-practice.md research/texas-pi-notes.md'; grep -cE '^[0-9]+\\. .*https?://' research/adjuster-attacks.md research/chronology-practice.md research/texas-pi-notes.md; echo '$ grep -cE \"^- \\*\\*\" memory/GLOSSARY.md'; grep -cE '^- \\*\\*' memory/GLOSSARY.md; echo '$ git show 568e4b7:research/adjuster-attacks.md | grep -n radicular'; git show 568e4b7:research/adjuster-attacks.md | grep -n radicular; git show 2c76cda:research/adjuster-attacks.md | grep -n radicular; echo '$ grep -n -i \"refer\" evals/golden/sample.txt spec/SPEC.md | grep -i \"physical\\|pain man\"'; grep -n -i \"refer\" evals/golden/sample.txt | head; echo '$ grep -rn -i radicul evals/ app/ personas/ 2>/dev/null | head'; grep -rn -i radicul evals/ app/ personas/ 2>/dev/null | head; } 2>&1 | tee artifacts/review-evidence/T-008-r3-adjuster-greps.txt",
 "description": "Run r2 acceptance greps and r3 checks, save evidence"
}
````

### User / tool · 2026-11-02T00:58:27.951Z

**tool result**
````
$ grep -rn -i "referral to pain\|referred to pain" research/ memory/
memory/LESSONS.md:17:- 2026-11-02T00:54:30Z **orchestrator**: Research text invented a fact about the sample case ('referral to pain management'). Research is an input to personas, lexicon and golden files, so an invented fact there propagates. Harness change: research rows that describe the sample case must quote the record (adjuster r2 caught it).
memory/LESSONS.md:18:- 2026-11-02T00:56:08Z **researcher**: T-008 r2 failed on one invented sample-case fact ('referral to pain management') written as a paraphrase in a research table. Rule: every statement about the sample case in research/ quotes the record (or names the header date); before handoff, grep for rec/record/Rivera and check each hit.
exit 0
$ grep -n -i "care is active\|active care (" research/adjuster-attacks.md
exit 1
$ grep -n "41%" research/adjuster-attacks.md | cut -c1-80
59:Bulging increased with age; cord compression was uncommon (5.3%) and most oft
149:19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of 
$ grep -cE "^[0-9]+\. .*https?://" research/adjuster-attacks.md research/chronology-practice.md research/texas-pi-notes.md
research/texas-pi-notes.md:12
research/adjuster-attacks.md:20
research/chronology-practice.md:10
$ grep -cE "^- \*\*" memory/GLOSSARY.md
46
$ git show 568e4b7:research/adjuster-attacks.md | grep -n radicular
61:radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
51:radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
$ grep -n -i "refer" evals/golden/sample.txt spec/SPEC.md | grep -i "physical\|pain man"
16:Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."
$ grep -rn -i radicul evals/ app/ personas/ 2>/dev/null | head
evals/golden/hallucinations.jsonl:16:{"id": "H16", "synthetic": true, "category": "diagnosis_from_symptoms", "record_text": "Record 7 | 2026-05-18 | Hill Country Pain Management, new patient | \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\"", "candidate_summary": "Diagnosed with cervical radiculopathy.", "why_unsupported": "Record describes symptoms (radiating pain, numbness) and orders an MRI. No diagnosis is stated."}
evals/golden/sample.expected.json:956:      "statement": "Invents or substitutes a diagnosis not in the records (whiplash, radiculopathy/radicular, stenosis, sprain, disc bulge, nerve root/impingement, spondylosis, myelopathy, fracture).",
evals/golden/sample.expected.json:959:        "Cervical radiculopathy.",
evals/golden/sample.expected.json:960:        "Radicular symptoms in right arm.",
evals/golden/sample.expected.json:974:      "pattern": "(?i)whiplash|radicul\\w+|\\bstenosis\\b|\\bsprain\\b|\\bbulg\\w+|nerve (?:damage|impingement|compression|root|irritation)|pinched nerve|spondyl\\w+|myelopath\\w+|\\bfractur\\w+"
app/llm/lexicon.yaml:117:    hit: ['History of migraines.', 'past medical history of cervical radiculopathy', 'No LOC, history of migraines.', 'No neck complaints before the accident, history of lumbar strain.', 'Prior history of neck pain 2019, resolved.']
app/llm/lexicon.yaml:151:    hit: ['PMH significant for lumbar strain.', 'Past medical history significant for cervical radiculopathy.']
app/llm/lexicon.yaml:620:    hit: ['possible radiculopathy', 'could represent post-traumatic change', 'questionable relationship to MVA']
app/llm/lexicon.yaml:925:  false_positive: 'Round 2 narrowed "did not show" to "did not show up/for" and "did not present" to "did not present for <appointment>": "did not show signs of radiculopathy" and "did not present with LOC" are clinical negatives.'
app/llm/lexicon.yaml:929:    miss: ['showed improvement', 'Did not present with loss of consciousness.', 'Patient did not show signs of radiculopathy.']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:06.553Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r3-adjuster-hits.md",
 "content": "# T-008 r3 — sample-case statement sweep (claims-adjuster-reviewer)\n\nCommands:\n- `grep -n -i -E \"rivera|\\brec(ord)?s? ?[0-9]|sample case|sample records|2026-0[1-6]|\\$[0-9]|C5-C6|73[- ]day|Capital PT|Hill Country|Alvarez|Central ER|Austin (EMS|Imaging)|41-year|cyclobenzaprine|35 mph\" research/*.md`\n- `grep -n -i -E \"sample|our case|radicul|herniat|traumatic|severe|referr|\\bESI\\b|epidural|MRI|concussion|strain|missed|visit|intake|new onset|low back|degenerative change|patient states|January\" research/chronology-practice.md research/texas-pi-notes.md research/ASSUMPTIONS-proposed.md memory/GLOSSARY.md`\n- `grep -n -i -E \"radicul|herniat|traumatic|severe|active\" research/adjuster-attacks.md`\n- Read research/adjuster-attacks.md lines 1-130 in full.\nRecords compared against: spec/SPEC.md Appendix A table (lines 53-65) = evals/golden/sample.txt.\n\n| File:line | Statement about the sample | Quoted? | Supported? |\n|---|---|---|---|\n| AA:21 A1 | 6→7: 73 days (2026-03-06 → 2026-05-18) | header dates | yes (73 verified by hand) |\n| AA:22 A2 | rec 6 quote + label \"Capital PT, visit 9\" vs rec 4 \"Plan of care: 12 visits\" | yes | yes; matches golden C2/K2 |\n| AA:23 A3 | rec 3 \"low back pain in 2023, resolved\" | yes | yes |\n| AA:24-25 A4/A5 | rec 8 \"may represent\", \"correlate clinically\" | yes | yes |\n| AA:26 A6 | rec 9 \"Patient states symptoms began after the January collision\" | yes | yes |\n| AA:27 A7 | rec 7 date quote vs rec 1/2 header dates; \"neither excerpt states an accident date\" | yes | yes |\n| AA:28 A8 | rec 7 \"New onset pain radiating to right arm\"; 73 days | yes | yes |\n| AA:29 A9 | rec 1 \"C/O neck pain 7/10\", rec 6 \"Pain 3/10\", rec 4 ROM, rec 2 \"CT head negative\", rec 8 impression | yes | yes |\n| AA:30 A10 | \"PT rate $185/visit with no visit count → cannot total\" | no (paraphrase) | PARTLY: rate correct; \"no visit count\" wrong — labels say \"visit 8\", \"visit 9\"; rec 4 \"12 visits\" (finding m1) |\n| AA:31 A11 | \"Not in records\" | n/a | yes |\n| AA:32 A12 | rec 1/2 dated 01-09; only rec 7 states an accident date | yes | yes |\n| AA:33 A13 | rec 1 \"rear-ended at approx. 35 mph\", \"Transported to Central ER\"; no vehicle-damage facts | yes | yes |\n| AA:34 A14 | rec 7 \"new patient\" 05-18; \"no record states a referral source or an attorney\" | partly | OVERBROAD: rec 3 \"Refer to physical therapy\" (finding m2) |\n| AA:35 A15 | rec 4, rec 6, rec 7, rec 9 quotes; modality not stated | yes | yes (r2 B1/M1 resolved) |\n| AA:47-48 | \"two missed appointments\"; \"12-planned-vs-discharged-at-9\" | partly | yes (label \"visit 9\") |\n| AA:52 | \"(2023 low back vs 2026 neck)\" | no (paraphrase) | yes (rec 3) |\n| AA:61-62 | \"a C5-C6 protrusion in a 41-year-old ... the 'new onset' radicular symptoms\" | NO | NO: \"radicular\" is not in any record; golden sample.expected.json:956-960 lists \"Radicular symptoms in right arm.\" as an invented diagnosis (finding B1) |\n| AA:70 | \"patient states symptoms began after the January collision\" | yes | yes |\n| AA:77 | do not \"fix\" 2026-01-19 to 2026-01-09 | dates | yes |\n| AA:81-85 | rec 1 \"Transported to Central ER.\"; header 01-09; rec 7 \"2026-01-19\" later than first treatment | yes | yes; no delay computed (D-017) |\n| AA:99 | \"Rivera's records name no referral source.\" | no | OVERBROAD: rec 3 \"Refer to physical therapy 2x/week for 6 weeks.\" (finding m2) |\n| AA:102-106 | records 4-6 name no modality; rec 4/6 quotes; ESI only recommended | yes | yes |\n| AP:11 P-04 | rec 9 quote, recommended not performed | yes | yes |\n| AP:18 P-11 | rec 3 two quotes | yes | yes |\n| AP:21 P-14 | rec 7 quote vs records dated 01-09 that state no accident date | yes | yes |\n| CP:5 | \"Synthetic case only (Jordan Rivera, spec Appendix A)\" | n/a | yes |\n| CP:18-19 | rec 9 quote, dated 2026-06-12 | yes | yes |\n| CP:33 | \"Recommend ESI\" ≠ \"received ESI\" (generic rule) | n/a | yes |\n| TX:4 | \"rear-ended in Austin (spec Appendix A); first records dated 2026-01-09\" | paraphrase of spec | yes |\n| TX:58-59 | rec 1 \"Transported to Central ER.\", no charge; rec 2 \"ER charges: $6,240.\" | yes | yes |\n| GLOSSARY | no sample-case statements (generic terms only) | n/a | n/a |\n\nResult: 31 hits; 27 quoted or header-date anchored and supported; 1 invented characterization (AA:61-62 \"radicular\");\n2 overbroad/inaccurate paraphrases (AA:30 \"no visit count\"; AA:34/AA:99 \"no referral source\"); AA:52 paraphrase is supported.\n\"radicular\" was already present in 2c76cda (line 51) and 568e4b7 (line 61); I missed it in rounds 1 and 2.\n"
}
````

### User / tool · 2026-11-02T00:59:06.646Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r3-adjuster-hits.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:39.603Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster-r3.md",
 "content": "# T-008 round 3 review — claims-adjuster-reviewer\n\n**Verdict: fail** (1 blocker, 0 major, 2 minor, 1 nit).\n\nAll five round-2 findings are resolved. The invented pain-management referral is gone, and A15 now quotes rec 4, 6, 7 and 9.\n\"Active care\" is replaced by \"records 4–6 name no modality\". A14 drops src 1 and cites the new Insurance Journal piece\n(src 20), which I fetched: the author, date and all three quotes match. The retention-timing check is now labeled an\nassumption. Nakashima says 41%, and the soft-tissue glossary entry is fixed. The sweep also correctly removed the old\nclaim that EMS/ER \"give accident 01-09\". Records 1 and 2 state no accident date.\n\nI re-swept research/*.md and checked 31 sample-case hits; the hit-by-hit table is in\n`artifacts/review-evidence/T-008-r3-adjuster-hits.md`. One invented characterization survives. adjuster-attacks.md:61-62\ncalls Rivera's rec 7 symptoms \"the 'new onset' radicular symptoms\". No record says \"radicular\". The project's own golden\nfile lists \"Radicular symptoms in right arm.\" as an invented diagnosis (sample.expected.json:956-960), and hallucination\ncase H16 is this exact record. The sentence has been there since round 1, and I missed it in rounds 1 and 2. It is the same\nclass of defect as the r2 referral blocker: a research paraphrase of the sample that the records don't support. Persona §5\nmakes it a blocker. Two smaller paraphrases are inaccurate: A10 says the PT rate has \"no visit count\" (the labels say\n\"visit 8\" and \"visit 9\"), and line 99 says \"Rivera's records name no referral source\" (rec 3 says \"Refer to physical therapy\").\n\n```json\n{\"card\": \"T-008\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit da17ba2 vs 568e4b7: research/adjuster-attacks.md, research/ASSUMPTIONS-proposed.md, research/chronology-practice.md, research/texas-pi-notes.md, memory/GLOSSARY.md (lexicon_selfcheck.py diff belongs to T-009 commit 2fee2df, not reviewed); no app (research card); Jordan Rivera sample (spec/SPEC.md Appendix A = evals/golden/sample.txt)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-008 -> status in_review, rounds 2, commits [2c76cda, 568e4b7, da17ba2]\",\n  \"git log --oneline -4 -- research memory/GLOSSARY.md -> da17ba2 top; git show --stat da17ba2 -> 5 files, 35+/25-\",\n  \"git diff 568e4b7..da17ba2 -- research/*.md memory/GLOSSARY.md (read in full)\",\n  \"Read spec/SPEC.md:53-65 and evals/golden/sample.txt (records 1-9); read research/adjuster-attacks.md:1-130 in full\",\n  \"r2 acceptance greps (artifacts/review-evidence/T-008-r3-adjuster-greps.txt): grep -rn -i 'referral to pain|referred to pain' research/ memory/ -> only memory/LESSONS.md:17-18 (lesson text, not research); grep 'care is active|active care (' -> exit 1 (none); '41%' at adjuster-attacks.md:59,149; source counts AA 20, CP 10, TX 12; GLOSSARY terms 46\",\n  \"Sample-case sweep: 3 greps over research/*.md + GLOSSARY (commands and 31-hit table in artifacts/review-evidence/T-008-r3-adjuster-hits.md)\",\n  \"git show 2c76cda / 568e4b7 :research/adjuster-attacks.md | grep -n radicular -> lines 51 / 61 (pre-existing)\",\n  \"grep -rn -i radicul evals/ app/ personas/ -> sample.expected.json:956-974 must-not pattern incl. 'Radicular symptoms in right arm.'; hallucinations.jsonl:16 H16 on record 7\",\n  \"Read evals/golden/sample.expected.json flags G1, C1, C2, P1, P2, K1-K5 (A2 'causation + conflict' matches C2/K2)\",\n  \"Read memory/ORCHESTRATOR_DECISIONS.md D-017, D-018\",\n  \"curl -L insurancejournal.com/news/national/2026/01/21/854959.htm -> HTTP 200, 103085 bytes; title, author Pragatee Dhakal, published 2026-01-21; verbatim 'steer claimants into higher cost services', 'plaintiffs' counsel refer injured claimants to clinics or pain-management centers', 'defense counsel may challenge causation or necessity'; 0 hits for 'letter of protection', 'retain', 'retention' (artifacts/review-evidence/T-008-r3-insurancejournal-checks.txt)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"source_quality_and_labeling\": 4, \"adversarial_coverage\": 5, \"accuracy_vs_sources\": 3, \"texas_relevance\": 4, \"usefulness_to_flags_and_lexicon\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Research labels Rivera's rec 7 symptoms 'radicular', a diagnosis term no record uses\",\n   \"evidence\": \"research/adjuster-attacks.md:61-62 'the plaintiff uses the \\\"new onset\\\" radicular symptoms to argue aggravation.' Rec 7 verbatim: 'New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.' grep -rn -i radicul evals/ -> evals/golden/sample.expected.json:956 must-not 'Invents or substitutes a diagnosis not in the records (whiplash, radiculopathy/radicular, ...)', :960 example 'Radicular symptoms in right arm.'; evals/golden/hallucinations.jsonl:16 H16 'Record describes symptoms (radiating pain, numbness) and orders an MRI. No diagnosis is stated.' Present since 2c76cda:51 and 568e4b7:61; the round-3 sweep (handoff: 'every sample-case claim re-anchored to quotes') missed it.\",\n   \"why_it_matters\": \"If 'radicular' ends up in a summary, that is an upgrade I can attack: no physician diagnosed radiculopathy, and the MRI is hedged. The project's own golden file treats the phrase as an invented diagnosis. Research feeds personas, lexicon and golden files (LESSONS.md:17), so the term spreads from here. This is the same defect class as the r2 referral blocker.\",\n   \"fix\": \"Replace with the record's words: 'the plaintiff uses rec 7 \\\"New onset pain radiating to right arm with numbness in fingers\\\" to argue aggravation.'\",\n   \"acceptance_test\": \"grep -rn -i 'radicul' research/*.md -> no hit that describes the sample (citations of literature titles excepted).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A10 says the PT rate has 'no visit count'; the records carry visit numbers\",\n   \"evidence\": \"research/adjuster-attacks.md:30 'PT rate $185/visit with no visit count → cannot total'. Rec 4 'Plan of care: 12 visits. Charge per visit $185.'; source labels rec 5 'Capital PT, visit 8', rec 6 'Capital PT, visit 9'.\",\n   \"why_it_matters\": \"The conclusion is right, but the reason given is wrong. It implies that a visit count would allow a total (9 × $185), and that is exactly the extrapolation I reject (checklist item 11). The records do give counts. They give no PT charge.\",\n   \"fix\": \"'Rec 4 \\\"Charge per visit $185\\\" is a rate; no PT charge is stated for any visit, so no PT amount is totaled (visit labels 8 and 9 and plan \\\"12 visits\\\" do not change that).'\",\n   \"acceptance_test\": \"A10 row no longer says 'no visit count' and states that the rate is not multiplied.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"'Rivera's records name no referral source' is overbroad; rec 3 is a PCP referral to PT\",\n   \"evidence\": \"research/adjuster-attacks.md:99 'Rivera's records name no referral source.'; :34 A14 'no record states a referral source or an attorney'. Rec 3 verbatim: 'Refer to physical therapy 2x/week for 6 weeks.' A15 (:35) scopes it correctly: 'rec 7 \\\"Hill Country Pain Management, new patient\\\", no referral source stated'.\",\n   \"why_it_matters\": \"An unscoped negative about the records is still a paraphrase the records contradict. The PCP referral to PT is a fact that helps the claimant, because physician-directed PT answers 'self-directed care'. A golden or persona author could copy the line as written.\",\n   \"fix\": \"Scope it: 'Rec 7 names no referral source; the only stated referral is rec 3 \\\"Refer to physical therapy\\\".'\",\n   \"acceptance_test\": \"Lines 34 and 99 refer to rec 7 or quote rec 3.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Src 20 label omits the author's vendor affiliation\",\n   \"evidence\": \"research/adjuster-attacks.md:151 '(Insurance trade press, opinion piece.)'. Page byline: 'Pragatee Dhakal is the director of product strategy and enablement at CLARA Analytics, a leading provider of artificial intelligence (AI) technology for insurance claims'.\",\n   \"why_it_matters\": \"Source balance is labeled per source elsewhere. A claims-AI vendor writing about medical abuse has a commercial angle.\",\n   \"fix\": \"Append '; author is at CLARA Analytics, a claims-AI vendor'.\",\n   \"acceptance_test\": \"Src 20 line names the affiliation.\"}\n ],\n \"whats_right\": [\n  \"A15 and A14 now quote rec 4, 6, 7 and 9 only, with 'no referral source stated' and 'recommended, not performed' scoped to the right records.\",\n  \"A7/A12/P-14 correctly say only rec 7 states an accident date (records 1-2 carry header dates only), and no delay is computed (D-017).\",\n  \"Src 20 checks out verbatim (author, date, three quotes), and the retention-timing claim is honestly labeled an assumption.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T00:59:39.757Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:40.492Z

Now I'll update my memory.

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:41.271Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Validate board including new review"
}
````

### User / tool · 2026-11-02T00:59:41.417Z

**tool result**
````
ok (26 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:44.899Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md",
 "old_string": "**Why:** researchers fill",
 "new_string": "Round 3 (da17ba2): r2 items fixed, but \"radicular symptoms\" (adjuster-attacks.md notes A4/A5) had survived since r1;\nI missed it twice. Rated blocker: golden sample.expected.json must-not lists \"Radicular symptoms in right arm.\" Also overbroad\nnegatives (\"records name no referral source\" vs rec 3 \"Refer to physical therapy\") and \"no visit count\" (labels say visit 8/9).\n\n**Why:** researchers fill"
}
````

### User / tool · 2026-11-02T00:59:45.003Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:47.153Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md",
 "old_string": "**How to apply:** on every re-review, grep each NEW row's",
 "new_string": "**How to apply:** sweep NOTES prose too, not just table cells; grep research for the golden must-not diagnosis regex\n(sample.expected.json ~:974: whiplash|radicul|stenosis|sprain|bulg|nerve root|spondyl) and for unscoped negatives. On every re-review, grep each NEW row's"
}
````

### User / tool · 2026-11-02T00:59:47.249Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:49.693Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && sed -i '' 's|^- \\[Research attack-map gaps\\](project_research_attack_map_gaps.md) — .*|- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r3: omissions, invented Rivera facts (referral, \"radicular\"); sweep notes prose + golden must-not regex|' MEMORY.md && cat MEMORY.md",
 "description": "Update memory index line"
}
````

### User / tool · 2026-11-02T00:59:49.782Z

**tool result**
````
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r3: omissions, invented Rivera facts (referral, "radicular"); sweep notes prose + golden must-not regex
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:58.045Z

T-008 round 3 verdict: **fail** (1 blocker, 0 major, 2 minor, 1 nit). Review is in `/Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster-r3.md` and `board.py validate` returns "ok (26 file(s))".

- **All five round-2 findings are fixed.** The invented pain-management referral is gone (that grep now only hits `memory/LESSONS.md`), "active care" returns nothing, 41% is in, and the soft-tissue glossary entry is fixed. A14 now cites src 20 and labels the retention-timing check an assumption.
- **Insurance Journal source:** curl got HTTP 200. The author (Dhakal), the date (2026-01-21) and all three quotes match the page. The article says nothing about letters of protection or retention timing, as the research says.
- **Blocker:** `research/adjuster-attacks.md:61-62` calls rec 7's symptoms "the 'new onset' radicular symptoms". No record says "radicular". The project's golden file lists "Radicular symptoms in right arm." as an invented diagnosis (`sample.expected.json:956-960`, and H16). The sentence has been there since round 1. I missed it in rounds 1 and 2, and the round-3 sweep missed it too.
- **Minor 1:** A10 says the PT rate has "no visit count", but the source labels say "visit 8" and "visit 9". The real reason not to total PT is that no PT charge is stated.
- **Minor 2:** line 99 says "Rivera's records name no referral source", but rec 3 says "Refer to physical therapy". The A15 cell scopes the same point correctly to rec 7.
- **Nit:** the src 20 label leaves out that the author works for CLARA Analytics, a claims-AI vendor.
- **Sweep:** I checked 31 statements about the sample case. 27 are quoted or tied to a record date and are supported; the other 4 are the three findings above. The hit-by-hit table is in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r3-adjuster-hits.md`.
- **Other evidence files:** `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r3-adjuster-greps.txt` and `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r3-insurancejournal-checks.txt`. My reviewer memory is updated.
