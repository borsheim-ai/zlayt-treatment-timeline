# Subagent: T-008 round-2: claims-adjuster (T-008 round-2: claims-adjuster)

Source: `agent-aa5e77ec50df49f95.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:51:28.617Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 2 of T-008 "Domain research" (M1). AC: `python3 tools/board.py show T-008`. Your round-1 review: reviews/T-008-claims-adjuster.md. Changes: `git log --oneline -- research memory/GLOSSARY.md | head -5` and diff since 2c76cda. Decisions: memory/ORCHESTRATOR_DECISIONS.md (note D-017 overrides your round-1 suggestion that code compute delay-to-treatment: the tool states first recorded treatment only — judge whether the research now documents the attack, not whether the tool computes it).
Exercise hands-on: resolution table for each round-1 finding (artifacts/review-evidence/T-008-r2-adjuster.md); spot-check 2 new sources with curl; check the new attack rows are accurate and each has a flag type per D-013/D-018 or "context only".
Write reviews/T-008-claims-adjuster-r2.md (D.2 JSON). Do not fix anything. Reply ≤ 15 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:30.927Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/claims-adjuster-reviewer/ && cat .claude/agent-memory/claims-adjuster-reviewer/*.md; python3 tools/board.py show T-008; git log --oneline -- research memory/GLOSSARY.md | head -5; git status | head -5",
 "description": "Read memory, board card, and git log"
}
````

### User / tool · 2026-11-02T00:51:31.109Z

**tool result**
````
MEMORY.md
feedback_lexicon_review_method.md
project_research_attack_map_gaps.md
/bin/bash: child setpgid (78149 to 78149): Operation not permitted
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 omissions (delay, MIST, attorney, passive care) + verified source facts
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
description: Recurring adjuster-attack omissions in Zlayt research (delay to first treatment, MIST, attorney timing, passive care) and source-check notes
metadata:
  type: project
---

As of 2026-11-01 (T-008 round 0), research/adjuster-attacks.md A1–A11 omitted delay-to-first-treatment, MIST/vehicle damage/
transport at scene, attorney-referral timing/LOP care, and duration/passive care/provider type — all listed verbatim in its own
src 1 (Claims Journal 2013 checklist items 1, 2, 5, 6, 7).

**Why:** researcher summarized src 1 but built rows only from the spec's four flags; downstream lexicon and personas inherit gaps.

**How to apply:** on re-review, grep adjuster-attacks.md for these rows first. Source facts already verified by curl:
Brinjikji AJNR 2015 is a LUMBAR review (don't accept it for cervical claims); Herrera v. Madrak (Conn. App. 2000) >12 missed PT
sessions confirmed; Virginia Lawyers Weekly src 16 says "eight days later" (not "weeks"); studicata Fletcher v. Simmons is
paywalled (403). WebFetch is not in this reviewer's toolset — use curl. Evidence: artifacts/review-evidence/T-008-adjuster-source-checks.txt.
Related: [[lexicon-review-method]].
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
updated_at: "2026-11-02T00:41:40Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T00:40:21Z"
rounds: 1
commits: ["2c76cda", "568e4b7"]
reviews:
  - {"persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-008-claims-adjuster.md", "at": "2026-11-02T00:39:42Z"}
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

## Handoff
Round 2 per finding: M1 delay to first treatment → A12 + P-14 + glossary, framed per D-017 (show 'first recorded treatment', never compute delay) · M2 A13 MIST/transport, A14 attorney/LOP timing, A15 duration/passive care, each with D-018 flag type or context-only · minor Brinjikji marked lumbar-only + Nakashima cervical study (src 19) · minor 'Australian PIC' clause removed (every 'src N' resolves to 1–19) · minor GLOSSARY 46 terms incl. MIST, Delay in treatment, generals, value drivers, Stowers (TX src 12), BI · nit 'approx. 40%'. Also P-15 (scene facts → internal notes). Verified by reviewer's acceptance greps. Question for Chris (from reviewer) is answered by D-017.

568e4b7 docs(research): T-008 round 2 — delay, MIST, LOP, passive-care attacks; cervical source; glossary
4924221 docs(research): T-012 round 2 — §181.154, full vendor retention, scoped PRs, Part 2 privacy answers
8a22a5c docs(research): PHI handling and AI-output supervision for Texas PI firm (T-012)
f419c3b feat(research): flag lexicon with negation guard and test vectors (T-009)
2c76cda docs(research): PI chronology practice, adjuster attacks, Texas notes, glossary (T-008)
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:31.321Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster.md"
}
````

### User / tool · 2026-11-02T00:51:31.331Z

**tool result**
````
1	# T-008 review — claims-adjuster-reviewer
2	
3	**Verdict: changes** (0 blockers, 2 majors, 3 minors, 1 nit).
4	
5	All four ACs are met as written: `grep -cE '^[0-9]+\. .*https?://'` returns chronology-practice.md 10, adjuster-attacks.md 18,
6	texas-pi-notes.md 11. GLOSSARY has 38 `- **` term lines, all with a source or "assumption". ASSUMPTIONS-proposed has 13 P-rows.
7	The attack map ties each attack to the exact Rivera excerpt, and the day counts are right (73 days 03-06→05-18; 129 days 01-09→05-18).
8	As the adjuster, my objection is what the map leaves out. The insurer-side checklist the researcher cites (Claims Journal, src 1)
9	starts with "How soon did treatment start?", vehicle damage, and whether the claimant was transported from the scene. None of those
10	made it into A1–A11. Attorney-driven care, active vs. passive care, and duration vs. expected recovery are missing too. Those are my
11	first moves on a soft-tissue demand, and because T-009 builds on this map, the lexicon misses them as well (see T-009 review).
12	One cited study is stretched beyond its scope (a lumbar review used for a cervical finding), and one claim cites a source that isn't
13	listed.
14	
15	Exercised: `python3 tools/board.py show T-008` (ACs above). I read all four research files and memory/GLOSSARY.md at HEAD (commit
16	2c76cda content). I re-counted sources, glossary terms and P-rows with grep (output above). I ran a coverage grep:
17	`grep -n -i "delay\|first treatment\|property damage\|MIST\|minor impact\|attorney\|passive\|IME" research/adjuster-attacks.md` →
18	no output. I spot-checked 4 sources with curl (WebFetch isn't in my toolset): Claims Journal src 1, Brinjikji src 6 (PubMed abstract
19	plus PMC full text), Herrera v. Madrak src 14 (vLex), and Virginia Lawyers Weekly src 16. Fletcher v. Simmons returned HTTP 403
20	(paywall). Verbatim excerpts are in `artifacts/review-evidence/T-008-adjuster-source-checks.txt`. I checked the claims against
21	personas/claims-adjuster.md §2/§4, spec Appendix A/C, and evals/golden/sample.expected.json. Agent memory was empty at start.
22	
23	```json
24	{"card": "T-008", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
25	 "scope": "research/chronology-practice.md, research/adjuster-attacks.md, research/texas-pi-notes.md, research/ASSUMPTIONS-proposed.md, memory/GLOSSARY.md (commit 2c76cda, read at HEAD 9e759a2); no app; Jordan Rivera sample case",
26	 "exercised": [
27	  "python3 tools/board.py show T-008 (4 ACs, all marked done)",
28	  "grep -cE '^[0-9]+\\. .*https?://' on the three research files -> 10 / 18 / 11",
29	  "grep -cE '^- \\*\\*' memory/GLOSSARY.md -> 38 terms; every line contains 'Source:'",
30	  "grep -cE '^\\| P-[0-9]+' research/ASSUMPTIONS-proposed.md -> 13",
31	  "grep -n -i 'delay|first treatment|property damage|MIST|minor impact|attorney|passive|IME' research/adjuster-attacks.md -> no output",
32	  "curl Claims Journal src 1 (HTTP 200) and extracted the 10-point medical-records checklist verbatim",
33	  "curl PubMed efetch 25430861 + PMC4464797 BioC full text for Brinjikji src 6 (figures confirmed; lumbar-only scope found)",
34	  "curl vLex Herrera v. Madrak src 14 (holding confirmed: >12 missed PT appointments warranted mitigation charge)",
35	  "curl Virginia Lawyers Weekly src 16 (takeaway confirmed; 'eight days later' delayed report found)",
36	  "curl studicata Fletcher v. Simmons -> HTTP 403, unverifiable",
37	  "Recomputed Rivera day counts by hand: 73 (03-06->05-18), 129 (01-09->05-18), 28 (01-23->02-20)",
38	  "Read personas/claims-adjuster.md, spec/SPEC.md Appendix A, spec/SAMPLE_CASE_TRUTHS.md, evals/golden/sample.expected.json"
39	 ],
40	 "verdict": "changes",
41	 "scores": {"source_quality_and_labeling": 4, "adversarial_coverage": 2, "accuracy_vs_sources": 3, "texas_relevance": 4, "usefulness_to_flags_and_lexicon": 3},
42	 "findings": [
43	  {"severity": "major",
44	   "title": "Attack map omits delay to first treatment, the adjuster's first check",
45	   "evidence": "research/adjuster-attacks.md:16-28 (A1-A11) has no delay/first-treatment row; coverage grep for 'delay|first treatment' -> no output. Cited src 1 says verbatim: '5) Treatment patterns – How soon did treatment start? Were there gaps in treatment?' and '7) Duration and frequency – When did treatment start?' Src 16 (also cited) says verbatim: 'did not report injury until eight days later when he was seen at an urgent care facility.' personas/claims-adjuster.md §2: 'What he looks for first: accident date vs first-treatment date'; §4 item 2.",
46	   "why_it_matters": "Delay between the accident and first care is the strongest 'not really hurt' argument and is separate from a gap between visits (A1). It isn't in the research, so it isn't in the lexicon or ASSUMPTIONS, and no flag or field is planned for it. For Rivera the delay is 0 days (EMS on 2026-01-09), which helps the claimant, and the paralegal should see it. On another case, a 5-day delay will be the first line of my response.",
47	   "fix": "Add attack A12 'Delay to first treatment': what the defense argues; sources 1 and 16; Rivera = same day (record 1 EMS, record 2 ER). Note that code computes it from the earliest accident date to the first date of service, and that it must use both accident dates when they conflict (01-09 vs 01-19). Propose a matching P-row and a GLOSSARY term ('delay in treatment').",
48	   "acceptance_test": "grep -n -i 'first treatment' research/adjuster-attacks.md returns an attack-map row citing src 1 with the Rivera value (0 days from 2026-01-09); ASSUMPTIONS-proposed.md has a P-row for it; GLOSSARY has 'Delay in treatment'."},
49	  {"severity": "major",
50	   "title": "MIST/vehicle damage, attorney-driven care, and passive/over-long treatment are missing from the attack map even though the cited source lists them",
51	   "evidence": "Src 1 verbatim: '1) Police report – ... Was the injured party transported to a medical facility?'; '2) Vehicle photographs – Does the damage match? ... What is the directional force of impact?'; '6) Provider type – Was the claimant seen by a chiropractor or medical doctor?'; '7) ... Was it active or passive? Was it longer than an anticipated expected recovery date...'. adjuster-attacks.md:89 summarizes src 1 as including 'duration vs typical recovery, ... mechanism of injury', but no A-row covers them. Attorney referral/LOP appears only in texas-pi-notes.md §3 and lexicon.yaml:547 (litigation_referral), not as an attack. Coverage grep for 'property damage|MIST|minor impact|attorney|passive' -> no output.",
52	   "why_it_matters": "These are value drivers I use on every soft-tissue claim: low impact or no visible damage, ambulatory at scene or refused transport, care that starts or escalates after an attorney is retained, months of passive modalities beyond the expected recovery, and chiropractor-only care. Rivera record 1 has 'rear-ended at approx. 35 mph' and 'Transported to Central ER', both mechanism and transport facts. Because the map is the stated basis for T-009 and the adjuster persona, those layers inherit the gap. My T-009 probes confirm the lexicon misses 'Minimal damage to vehicle; airbags did not deploy', 'Ambulatory at scene, refused transport', and 'Referred to this clinic by attorney'.",
53	   "fix": "Add rows for: A13 mechanism/MIST (vehicle damage, speed, airbags, ambulatory or transported at scene; Rivera records 1-2), A14 attorney involvement timing / LOP-funded care (texas-pi-notes §3; flag only if the record says it), A15 duration and type of care vs expected recovery (active vs passive, provider type; src 1, src 3 Colossus duration). For each, state the flag type, or 'context only, not a required flag', and whether code or lexicon owns it.",
54	   "acceptance_test": "adjuster-attacks.md attack map has rows covering mechanism/MIST, attorney/LOP timing, and duration/passive care, each citing src 1 (and src 3 or TX §3 where relevant) and naming the Rivera record or 'not in records'; T-009 re-run of artifacts/review-evidence/T-009-adjuster-probes.py MIST/transport/attorney probes reflects the new rows."},
55	  {"severity": "minor",
56	   "title": "Brinjikji (lumbar-only review) used to argue about a cervical C5-C6 finding",
57	   "evidence": "adjuster-attacks.md:48-50: 'disc bulge prevalence rose from ~30% at age 20 to ~84% at 80 ... The defense uses this to say a C5-C6 protrusion in a 41-year-old may be pre-existing'. Brinjikji full text (PMC4464797) verbatim: 'additional studies that reported lumbar spine CT or MR imaging findings in individuals without low back pain.' Figures themselves confirmed against the PubMed abstract.",
58	   "why_it_matters": "If the firm repeats this in a demand or a rebuttal, defense counsel will point out that the study is about the low back, not the neck. The direction of the point (degeneration is common in people without symptoms) probably holds for the cervical spine too, but this is the wrong citation for it.",
59	   "fix": "Say explicitly that Brinjikji covers the lumbar spine, and add a cervical asymptomatic-MRI source if the research wants to make the C5-C6 point. Otherwise, limit the claim to 'spinal (lumbar) degeneration is common in asymptomatic adults'.",
60	   "acceptance_test": "adjuster-attacks.md A4 text and src 6 line both say 'lumbar'; any cervical prevalence claim cites a cervical study with URL."},
61	  {"severity": "minor",
62	   "title": "Unlisted source cited: 'Australian PIC'",
63	   "evidence": "adjuster-attacks.md:62-63: 'contemporaneous records outweigh an expert relying on an incorrect history (src 17, Australian PIC)'. Src 17 (line 105) is a Georgia Court of Appeals decision; no Australian Personal Injury Commission source appears in the 18-item list.",
64	   "why_it_matters": "A claim with no URL can't be checked, and it is also foreign law. lexicon.yaml:538 (inconsistent_history rationale: 'contemporaneous records outweigh later accounts') rests on it.",
65	   "fix": "Either add the PIC source with a URL and a 'non-US' label, or remove the clause and keep only what src 17 supports (impeachment with the claimant's intake forms).",
66	   "acceptance_test": "Every parenthetical source reference in adjuster-attacks.md resolves to a numbered entry with a URL."},
67	  {"severity": "minor",
68	   "title": "GLOSSARY lacks core adjuster vocabulary",
69	   "evidence": "memory/GLOSSARY.md (38 terms) has no entry for MIST / minor impact soft tissue, delay in treatment, specials vs generals, soft-tissue injury, value drivers, Stowers demand, or BI. personas/claims-adjuster.md §6 lists these as the adjuster's vocabulary.",
70	   "why_it_matters": "Workers and reviewers who write flag rationales and persona checks use the GLOSSARY. If these terms are missing, the adversary's actual arguments never make it into the vocabulary those people work from.",
71	   "fix": "Add one-line entries for MIST, delay in treatment, specials vs generals, value drivers (Colossus), Stowers demand (texas-pi-notes §7 already names it), and BI, each with a source or 'assumption'.",
72	   "acceptance_test": "grep -c -E 'MIST|Delay in treatment|Generals|Value drivers|Stowers' memory/GLOSSARY.md >= 5."},
73	  {"severity": "nit",
74	   "title": "Attack map drops 'approx.' from the ROM finding",
75	   "evidence": "adjuster-attacks.md:26: 'objective: ROM −40% (rec 4)'. Record 4 verbatim: 'Cervical range of motion reduced approx. 40%.'",
76	   "why_it_matters": "This is the same kind of hedge-stripping the research tells the product never to do (chronology-practice.md R3). Research tables get copied into prompts and golden files.",
77	   "fix": "Quote as 'reduced approx. 40%'.",
78	   "acceptance_test": "grep -n 'approx. 40%' research/adjuster-attacks.md matches the A9 row."}
79	 ],
80	 "whats_right": [
81	  "Attack map ties each attack to the exact Rivera excerpt, and the day counts (73, 129) are right; keep this record-anchored format.",
82	  "Read-depth and source-side labels (insurer, plaintiff, vendor, primary) are honest; the Herrera and Virginia takeaways check out against the sources.",
83	  "Billed-not-damages (Haygood / §41.0105) and '§18.001 is not causation evidence' are correctly turned into product rules."
84	 ],
85	 "questions_for_chris": [
86	  "Should delay-to-first-treatment be a visible computed field in the timeline (outside the four required flags), or research context only? The adjuster persona checklist item 2 assumes it is shown."
87	 ]}
88	```
89	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:33.112Z

**tool call — Bash**
````
{
 "command": "git diff --stat 2c76cda 568e4b7 -- research memory/GLOSSARY.md; git diff 2c76cda 568e4b7 -- research memory/GLOSSARY.md",
 "description": "Show research diff for round 2"
}
````

### User / tool · 2026-11-02T00:51:33.224Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:34.016Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-013\\|D-017\\|D-018\" -A8 memory/ORCHESTRATOR_DECISIONS.md | head -80",
 "description": "Read decisions D-013, D-017, D-018"
}
````

### User / tool · 2026-11-02T00:51:34.093Z

**tool result**
````
21:| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
22-| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
23-| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
24-| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
25:| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
27-| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29-| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30-| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:35.687Z

**tool call — Bash**
````
{
 "command": "git diff 2c76cda 568e4b7 -- research/adjuster-attacks.md research/ASSUMPTIONS-proposed.md research/texas-pi-notes.md memory/GLOSSARY.md",
 "description": "Show research diff limited to T-008 files"
}
````

### User / tool · 2026-11-02T00:51:35.780Z

**tool result**
````
diff --git a/memory/GLOSSARY.md b/memory/GLOSSARY.md
index 4297888..93bd157 100644
--- a/memory/GLOSSARY.md
+++ b/memory/GLOSSARY.md
@@ -7,6 +7,9 @@ pins it down. CP = research/chronology-practice.md · AA = research/adjuster-att
 - **Demand letter / demand package** — pre-suit letter (plus records, bills, chronology) to the at-fault party's liability insurer stating liability, damages and a settlement demand. Source: CP src 5, 6.
 - **Treatment chronology** — date-ordered list of every medical encounter with provider, findings, charges and a citation to the source record. Source: CP src 1.
 - **Medical summary** — narrative grouped by provider/injury rather than date; often the demand letter's treatment section. Source: CP src 2.
+- **General damages (generals)** — non-economic damages (pain, mental anguish, impairment) as opposed to specials (economic: medical bills, lost wages). Source: **assumption** (standard PI usage; Texas recovery rules for specials in TX src 1).
+- **BI (bodily injury) claim / BI adjuster** — third-party liability claim for injuries, handled by the at-fault driver's carrier. Source: AA src 1.
+- **Stowers demand** — time-limited settlement demand within policy limits; if the insurer unreasonably rejects it, it can be liable for an excess judgment (Texas, 1929). Source: TX src 12.
 - **Medical specials (specials)** — economic damages for medical expenses, itemized by provider. Source: CP src 2 (itemized expenses); term usage: **assumption** (common PI usage, no single cited definition).
 - **MMI (maximum medical improvement)** — point where further treatment is not expected to improve the condition; demands are usually sent after it. Source: CP src 2.
 - **Records index / missing records log** — list of records requested vs received. Source: CP src 1.
@@ -18,6 +21,11 @@ pins it down. CP = research/chronology-practice.md · AA = research/adjuster-att
 - **Legal nurse consultant (LNC)** — registered nurse who interprets medical records for attorneys; does not practice law. Source: CP src 8, 9.
 
 ## Flags and attacks
+- **Delay in treatment (delay to first treatment)** — time from the accident to the first medical visit; adjusters' first check. The tool shows only "first recorded treatment" and never computes the delay (D-017). Source: AA A12, src 1, 16.
+- **MIST (minor impact soft tissue)** — carrier category for low-speed collisions with soft-tissue injuries, valued low; attacked with vehicle-damage and scene facts. Source: AA A13, src 18 (plaintiff-side; carrier programs not public).
+- **Soft-tissue injury** — sprain/strain/whiplash-type injury without fracture or neurological deficit; often lacks objective findings. Source: AA A9, src 18.
+- **Active vs passive care** — exercise-based therapy vs modalities applied to the patient (heat, massage, e-stim); adjusters discount long passive care. Source: AA A15, src 1.
+- **Value drivers** — the claim features (injury type, treatment duration, objective findings, impairment) that claim-valuation software such as Colossus scores. Source: AA src 3 (second-hand).
 - **Gap in treatment** — period without care between dates of service; adjusters argue recovery or an intervening cause. Prototype threshold >30 days is the Zlayt spec's, not an industry rule. Source: AA src 1, 4.
 - **Pre-existing condition** — injury or condition documented before the incident; defense argues it, not the crash, explains symptoms. Source: AA src 2, 15.
 - **Aggravation (of a pre-existing condition)** — worsening of a prior condition by the incident; compensable for the worsening, argued separately from a new injury. Source: CP src 1.
@@ -44,4 +52,7 @@ pins it down. CP = research/chronology-practice.md · AA = research/adjuster-att
 ## Privacy and AI supervision (filled by T-012)
 - **PHI (protected health information)** — individually identifiable health information held by a HIPAA covered entity or business associate. Source: PHI file.
 - **Covered entity / business associate** — HIPAA-regulated providers, plans, clearinghouses / their contracted service providers handling PHI. Source: PHI file.
+- **Texas Medical Records Privacy Act (HSC ch. 181 / HB 300)** — Texas law whose "covered entity" includes anyone who comes into possession of PHI; staff training within 90 days; re-identification banned. Source: PHI src 6, 10.
+- **ABA Formal Opinion 512 / Texas Opinion 705** — ethics guidance on lawyers' generative-AI use: competence, confidentiality (informed consent for self-learning tools), verification, supervision. Source: PHI src 1-3.
+- **BAA / HIPAA readiness** — business associate agreement; an LLM vendor setting that permits PHI processing on covered API features only. Source: PHI src 9.
 - **Human-in-the-loop review** — a person accepts, edits or dismisses each AI output before use; required by ABA Op. 512 duties. Source: PHI file.
diff --git a/research/ASSUMPTIONS-proposed.md b/research/ASSUMPTIONS-proposed.md
index 10d4bc0..61c6678 100644
--- a/research/ASSUMPTIONS-proposed.md
+++ b/research/ASSUMPTIONS-proposed.md
@@ -18,6 +18,8 @@ Each has evidence (research file + source #) and a confidence. CP / AA / TX = ch
 | P-11 | A prior condition in a **different body region** (2023 low back vs 2026 neck) is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
 | P-12 | Firms cite records by Bates/page; the prototype's record # + verbatim excerpt stands in for that. | TX src 8; CP src 1 | Low-medium (assumption) | new |
 | P-13 | Paralegals at PI firms are not covered by a single chronology standard; conventions vary by firm, so the export format should be plain, editable text, not a fixed template. | CP src 9 (no standard found) | Medium | new |
+| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera 01-09 vs 01-19), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
+| P-15 | Scene and mechanism facts (speed, transport, ambulatory, vehicle damage) usually appear only in EMS/police records, and they cut both ways. Surface them as internal-notes flags (D-018/D-001), never as letter text chosen by the tool. | adjuster-attacks.md A13 (src 1) | Medium | new |
 
 Not proposed (insufficient evidence): any number for time spent per chronology or for settlement-value impact of
 gaps (only a vendor's "up to 20%" claim, AA/CP src 7).
diff --git a/research/adjuster-attacks.md b/research/adjuster-attacks.md
index c5911fc..be9406c 100644
--- a/research/adjuster-attacks.md
+++ b/research/adjuster-attacks.md
@@ -13,19 +13,26 @@ excerpts of the page (the takeaway lines quote only what the excerpt showed). Ve
 
 ## Attack map, applied to the Jordan Rivera sample
 
+Flag-type column uses the D-013 vocabulary (`gap`, `conflict`, `pre_existing`, `causation`, `record_warning`); the
+lexicon's former `causation_weakening` and `compliance` both map to `causation`.
+
 | # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
 |---|---|---|---|---|---|
 | A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
-| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments"; 12 planned vs 9 | causation_weakening + conflict |
+| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments"; 12 planned vs 9 | causation + conflict |
 | A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
-| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6, 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation_weakening |
-| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation_weakening |
-| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation_weakening |
+| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation |
+| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation |
+| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation |
 | A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs EMS/ER 2026-01-09 | conflict (code) |
-| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm" after 73-day gap | causation_weakening |
-| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Pain 7/10 → 3/10 subjective; objective: ROM −40% (rec 4), CT negative (rec 2), MRI C5-C6 (rec 8) | (context; not a required flag) |
+| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm" after 73-day gap | causation |
+| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Pain 7/10 → 3/10 subjective; objective: "Cervical range of motion reduced approx. 40%" (rec 4), CT negative (rec 2), MRI C5-C6 (rec 8) | (context; not a required flag) |
 | A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | PT rate $185/visit with no visit count → cannot total | amounts (code) |
 | A11 | **Prior claims history** | ISO ClaimSearch shows earlier injury claims | 2 | Not in records — out of scope for the tool | — |
+| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. (EMS/ER give accident 01-09; rec 7 says 01-19.) | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
+| A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at scene or refused transport → no injury | 1, 3, 18 | Rec 1 "rear-ended at approx. 35 mph", "Transported to Central ER" (both *help* the claimant). No vehicle-damage facts in the records | causation (lexicon: scene facts such as ambulatory at scene, refused transport, minimal damage — D-018) |
+| A14 | **Attorney involvement / LOP-funded care** | Care began or escalated after the attorney was retained; charges inflated under a letter of protection | 1, TX §3 (K&L), 3 | Not in records. Rivera's pain-management intake (rec 7) comes 73 days after PT; the records do not say who referred him | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
+| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | PT plan "12 visits" (rec 4), discharged at visit 9 (rec 6); active care (PT, referral to pain management, ESI recommended) | context only — not a required flag; duration is visible from the timeline itself |
 
 ## Notes per attack
 
@@ -45,9 +52,12 @@ discrepancy is a conflict an adjuster will see immediately.
 prior (2023 low back vs 2026 neck) must be surfaced; the paralegal decides relevance.
 False-positive risk: "denies prior neck injury" is a *negative* — it must not be flagged as a prior condition.
 
-**A4/A5 Degenerative findings and hedges.** Brinjikji et al. (AJNR 2015, 33 studies, 3,110 asymptomatic people):
-disc bulge prevalence rose from ~30% at age 20 to ~84% at 80; protrusion from 29% to 43% (src 6). The defense
-uses this to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
+**A4/A5 Degenerative findings and hedges.** Brinjikji et al. (AJNR 2015, 33 studies, 3,110 asymptomatic people)
+reviewed **lumbar** imaging: disc bulge prevalence rose from ~30% at age 20 to ~84% at 80, protrusion from 29% to
+43% (src 6). It says nothing directly about the neck. For the **cervical** spine, Nakashima et al. (Spine 2015,
+1,211 asymptomatic volunteers aged 20–70) found disc bulging in 87.6% overall and in most subjects in their 20s.
+Bulging increased with age, and cord compression was uncommon (5.3%) and concentrated at C5-C6 (src 19). The
+defense uses this kind of evidence to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
 radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
 equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
 Radiology literature treats "clinical correlation" and "cannot be excluded" as hedges that shift
@@ -60,11 +70,33 @@ knowledge; otherwise expert testimony is required (Guevara v. Ferrer, src 9). A
 opinion. The export may quote it but must attribute it ("patient states"), never restate it as fact.
 
 **A7 Inconsistent dates.** Defense impeaches with the claimant's own intake forms (Georgia appeal, src 17);
-contemporaneous records outweigh an expert relying on an incorrect history (src 17, Australian PIC). In
+a treating physician's causation opinion is only as good as the history the patient gave. In
 JLG Trucking v. Garza (Tex. 2015) evidence of a *second* accident was relevant to causation and its exclusion
 was reversible error (src 10) — a second accident date in the records is exactly what defense counsel looks for.
 The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.
 
+**A12 Delay to first treatment.** The insurer-side checklist asks "How soon did treatment start?" before it asks
+about gaps (src 1). In the Virginia record-review case the defense relied on a report made "eight days later"
+(src 16). Rivera went from EMS to the ER the same day (2026-01-09). That helps him, and the paralegal should see
+it. Per D-017 the tool does not compute a delay from an accident date, because the records give two accident dates
+and the tool must never pick one. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
+against whichever accident date the facts support.
+
+**A13 Mechanism / MIST.** Src 1 lists the police report (transported?), vehicle photos (does the damage match? what
+direction was the force?) and mechanism as first-line checks. Minor-impact soft-tissue (MIST) files are handled as
+a category by many carriers (src 18, plaintiff-side; carrier MIST programs are not public). EMS run reports are where
+scene facts live: speed, restraint, airbag deployment, ambulatory at scene, refused transport. Per D-018 those
+phrases are `causation` flags citing the excerpt, and they go to the internal notes only (D-001).
+
+**A14 Attorney involvement / LOP.** Src 1 asks about provider type and credentials. Texas made providers'
+negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). Adjusters
+compare the attorney-retention date with when care started or escalated. The tool cannot know the retention date
+from medical records, so it flags only what a record says ("referred by attorney", "letter of protection").
+
+**A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
+anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). Rivera's
+care is active and shorter than planned. This is context for the adjuster persona, not a required flag.
+
 **A9 Subjective vs objective.** Adjusters weigh objective findings (imaging, ROM measurements, spasm) above pain
 scores (src 1, 18). Not a required flag; useful for the one-line summary (keep numbers verbatim) and for the
 adjuster persona's checklist.
@@ -76,8 +108,9 @@ see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcodin
 
 ## Implications for flags and lexicon (handed to T-009)
 
-- Lexicon categories: `pre_existing` (A3, A4), `causation_weakening` (A2, A4–A6, A8), `compliance` (A2 — missed
-  appointments, non-compliance, discharged/left AMA).
+- Lexicon categories (D-013/D-018): `pre_existing` (A3, A4); `causation` (A2, A4–A6, A8, A13, A14 — including
+  the former `compliance` phrases: missed appointments, non-compliance, discharged/left AMA); `record_warning`
+  (date ambiguity, injection). A12 and A15 are context only.
 - Every phrase that is a *negation* ("denies", "no history of", "no prior") is a false-positive guard.
 - Hedges are flagged *because* they are hedges; the flag rationale must say the record is equivocal, not that
   the finding is degenerative.
@@ -91,7 +124,7 @@ see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcodin
 3. Simmons & Fletcher, "What is Colossus Claims Adjusting Software?" — https://www.simmonsandfletcher.com/car-accidents/auto-insurance-claims/colossus/ — Second-hand: Colossus records duration of treatment per injury, prognosis, future treatment. (Plaintiff firm; Colossus is proprietary — unverified.)
 4. Butler Firm, "How insurance companies use gaps in medical treatment against you" — https://butlerfirm.com/blog/how-insurance-companies-use-gaps-in-medical-treatment-against-you/ — Gaps let insurers argue injuries were minor or unrelated. (Plaintiff firm.)
 5. Young Injury Law, "Gap in medical treatment" — https://younginjurylaw.com/blog/gap-in-medical-treatment-ohio-injury-claim/ — Explain gaps proactively with referral/appointment paperwork; not every pause hurts. (Plaintiff firm.)
-6. Brinjikji W. et al., "Systematic literature review of imaging features of spinal degeneration in asymptomatic populations," AJNR 36(4):811 (2015) — https://www.ajnr.org/content/36/4/811 — Degenerative disc findings are common in pain-free adults and rise with age (bulge ~30%→84%, protrusion 29%→43%, age 20→80). (Peer-reviewed; abstract figures via search index — page 403'd to WebFetch.)
+6. Brinjikji W. et al., "Systematic literature review of imaging features of spinal degeneration in asymptomatic populations," AJNR 36(4):811 (2015) — https://www.ajnr.org/content/36/4/811 — Degenerative disc findings are common in pain-free adults and rise with age (bulge ~30%→84%, protrusion 29%→43%, age 20→80). **Lumbar spine only** — for cervical prevalence see src 19. (Peer-reviewed; abstract figures via search index — page 403'd to WebFetch.)
 7. AuntMinnie Europe, "Banned: top 8 words or phrases to avoid in radiology reports" — https://www.auntminnieeurope.com/clinical-news/article/15646568/banned-top-8-words-or-phrases-to-avoid-in-radiology-reports — Radiology chair lists "cannot rule out" and "clinical correlation" as hedges that can mislead. (Radiology trade press.)
 8. UCSF study of uncertainty terms in 642,569 radiology impressions — https://escholarship.org/content/qt3f22329f/qt3f22329f.pdf — Hedging terms vary by radiologist and subspecialty; "cannot exclude" signals uncertainty. (Academic.)
 9. Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007) — https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html — Expert testimony generally required for causation of conditions outside lay knowledge; lay evidence suffices only for basic, immediate injuries. (Primary; summary page.)
@@ -105,6 +138,8 @@ see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcodin
 17. Georgia Court of Appeals decision on impeachment with prior intake forms — https://caselaw.findlaw.com/court/ga-court-of-appeals/1418582.html — Defense may impeach with the claimant's own medical intake forms listing prior accidents/complaints. (Primary, non-Texas; via search summary.)
 18. Braun Law, "Objective vs. Subjective" — https://braunslaw.com/claimclinic/claim-worth/specific-injuries/ — Claim evaluation software weighs objective injuries more heavily. (Plaintiff firm.)
 
+19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of the cervical spines in 1211 asymptomatic subjects," Spine 40(6):392–398 (2015) — https://pubmed.ncbi.nlm.nih.gov/25584950/ — Cervical disc bulging in 87.6% of asymptomatic adults aged 20–70, most already in their 20s; cord compression 5.3%, mostly at C5-C6. (Peer-reviewed; abstract figures via search index.)
+
 Assumptions where sources are thin: (a) no public adjuster manual quantifies how much each attack reduces value;
 (b) Colossus specifics are second-hand; (c) the 30-day gap threshold is the Zlayt spec's, not an industry rule —
 real adjusters may treat shorter gaps as material, so the prototype's threshold should be configurable.
diff --git a/research/texas-pi-notes.md b/research/texas-pi-notes.md
index 369e24a..d8fd091 100644
--- a/research/texas-pi-notes.md
+++ b/research/texas-pi-notes.md
@@ -84,7 +84,12 @@ mirrors (rulesofcivilprocedure.com, texas.public.law) and cross-checked against
   more than 50% responsible recovers nothing, otherwise damages reduced by percentage (CPRC §33.001, §33.012).
   (Src 10, 11 — secondary; verify before relying.) Texas is an at-fault (tort) auto state; PIP is optional
   coverage. **Assumption**, not researched further: pre-suit demands go to the at-fault driver's liability carrier.
-- Stowers (time-limited policy-limits demands) affects demand-letter *strategy*, not the chronology — not researched.
+- Stowers doctrine: *G.A. Stowers Furniture Co. v. American Indemnity Co.*, 15 S.W.2d 544 (Tex. Comm'n App. 1929).
+  A liability insurer that unreasonably rejects a demand within policy limits can be liable for the excess
+  judgment. A valid Stowers demand covers the whole claim and is within limits; *American Physicians Ins. Exch. v.
+  Garcia* (Tex. 1994) narrowed the doctrine (src 12). This affects demand-letter *strategy* (time-limited
+  policy-limits demands), not the chronology. One more reason the chronology must be accurate: the carrier tests
+  a Stowers demand's reasonableness against the records.
 
 ## Assumptions where sources are thin
 
@@ -108,3 +113,4 @@ mirrors (rulesofcivilprocedure.com, texas.public.law) and cross-checked against
 9. Senate Research Center bill analysis, SB 679 (83rd Leg.) — https://capitol.texas.gov/tlodocs/83R/analysis/pdf/SB00679F.pdf — Records served with a 902(10) affidavit need not be filed with the court beforehand. (Official legislative analysis; via search snippet.)
 10. Tex. Civ. Prac. & Rem. Code §33.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-33-001/ — Claimant >50% responsible may not recover. (Mirror; via search snippet.)
 11. Blass Law, "Texas 51 percent rule" — https://www.blasslaw.com/faqs/texas-51-percent-rule-comparative-fault/ — Practitioner explanation of modified comparative fault and the two-year limitations period. (Plaintiff firm.)
+12. IRMI, "Stowers doctrine" (insurance glossary) — https://irmi.com/term/insurance-definitions/stowers-doctrine — Insurer liable for the excess when it unreasonably refuses a within-limits demand; Thompson Coe practice paper https://www.thompsoncoe.com/content/uploads/2019/02/Stowers.pdf covers the elements and *Garcia*. (Secondary; via search excerpts.)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:39.304Z

**tool call — Bash**
````
{
 "command": "ls spec evals/golden | head -30; find . -path ./node_modules -prune -o -name \"*sample*\" -print | grep -v .venv | head",
 "description": "Locate sample case records"
}
````

### User / tool · 2026-11-02T00:51:39.403Z

**tool result**
````
evals/golden:
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt

spec:
REQUIREMENTS.md
SAMPLE_CASE_TRUTHS.md
./evals/golden/sample.export.expected.txt
./evals/golden/sample.expected.json
./evals/golden/sample.txt
./.git/hooks/commit-msg.sample
./.git/hooks/pre-rebase.sample
./.git/hooks/sendemail-validate.sample
./.git/hooks/pre-commit.sample
./.git/hooks/applypatch-msg.sample
./.git/hooks/fsmonitor-watchman.sample
./.git/hooks/pre-receive.sample
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:40.834Z

**tool call — Bash**
````
{
 "command": "cat evals/golden/sample.txt; grep -n -i \"refer\" evals/golden/sample.txt",
 "description": "Read Rivera sample records"
}
````

### User / tool · 2026-11-02T00:51:40.913Z

**tool result**
````
SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data

=== Record 1 ===
Date: 2026-01-09
Source: Austin EMS run report
Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

=== Record 2 ===
Date: 2026-01-09
Source: Central ER discharge summary
Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."

=== Record 3 ===
Date: 2026-01-16
Source: Dr. Alvarez, primary care
Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."

=== Record 4 ===
Date: 2026-01-23
Source: Capital PT, initial evaluation
Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."

=== Record 5 ===
Date: 2026-02-20
Source: Capital PT, visit 8
Excerpt: "Pain 4/10, improving. Patient reports missing 3 days of work."

=== Record 6 ===
Date: 2026-03-06
Source: Capital PT, visit 9
Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."

=== Record 7 ===
Date: 2026-05-18
Source: Hill Country Pain Management, new patient
Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."

=== Record 8 ===
Date: 2026-05-29
Source: Austin Imaging, cervical MRI
Excerpt: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."

=== Record 9 ===
Date: 2026-06-12
Source: Hill Country Pain Management, follow-up
Excerpt: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

16:Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:01.822Z

**tool call — Bash**
````
{
 "command": "echo \"--- AT1\"; grep -n -i 'first treatment' research/adjuster-attacks.md | cut -c1-160; grep -n 'P-14' research/ASSUMPTIONS-proposed.md | cut -c1-80; grep -n 'Delay in treatment' memory/GLOSSARY.md | cut -c1-80; echo \"--- AT2\"; grep -n -i -E 'MIST|attorney|passive' research/adjuster-attacks.md | cut -c1-120; echo \"--- AT3\"; grep -n -i 'lumbar' research/adjuster-attacks.md | cut -c1-120; echo \"--- AT4\"; grep -n 'PIC' research/adjuster-attacks.md; grep -o -E 'src [0-9]+' research/adjuster-attacks.md | sort -u | tr '\\n' ' '; echo; grep -cE '^[0-9]+\\. .*https?://' research/adjuster-attacks.md research/texas-pi-notes.md research/chronology-practice.md; echo \"--- AT5\"; grep -c -E 'MIST|Delay in treatment|Generals|Value drivers|Stowers' memory/GLOSSARY.md; grep -c -i -E 'MIST|Delay in treatment|Generals|Value drivers|Stowers' memory/GLOSSARY.md; grep -cE '^- \\*\\*' memory/GLOSSARY.md; echo \"--- nit\"; grep -n 'approx. 40%' research/adjuster-attacks.md | cut -c1-60; echo \"--- referral\"; grep -n -i 'referr\\|refer ' research/adjuster-attacks.md research/ASSUMPTIONS-proposed.md memory/GLOSSARY.md | cut -c1-200",
 "description": "Run round-1 acceptance greps"
}
````

### User / tool · 2026-11-02T00:52:02.014Z

**tool result**
````
--- AT1
32:| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first record
78:**A12 Delay to first treatment.** The insurer-side checklist asks "How soon did treatment start?" before it asks
21:| P-14 | Adjusters check delay from accident to first treatment before anythi
24:- **Delay in treatment (delay to first treatment)** — time from the acciden
--- AT2
33:| A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at sce
34:| A14 | **Attorney involvement / LOP-funded care** | Care began or escalated after the attorney was retained; charges
35:| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor
82:and the tool must never pick one. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
85:**A13 Mechanism / MIST.** Src 1 lists the police report (transported?), vehicle photos (does the damage match? what
86:direction was the force?) and mechanism as first-line checks. Minor-impact soft-tissue (MIST) files are handled as
87:a category by many carriers (src 18, plaintiff-side; carrier MIST programs are not public). EMS run reports are where
91:**A14 Attorney involvement / LOP.** Src 1 asks about provider type and credentials. Texas made providers'
93:compare the attorney-retention date with when care started or escalated. The tool cannot know the retention date
94:from medical records, so it flags only what a record says ("referred by attorney", "letter of protection").
96:**A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
--- AT3
24:| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 
56:reviewed **lumbar** imaging: disc bulge prevalence rose from ~30% at age 20 to ~84% at 80, protrusion from 29% to
127:6. Brinjikji W. et al., "Systematic literature review of imaging features of spinal degeneration in asymptomatic pop
--- AT4
src 1 src 10 src 11 src 12 src 13 src 14 src 15 src 16 src 17 src 18 src 19 src 2 src 3 src 4 src 5 src 6 src 7 src 9 
research/chronology-practice.md:10
research/adjuster-attacks.md:19
research/texas-pi-notes.md:12
--- AT5
4
5
46
--- nit
29:| A9 | **Subjective vs objective** | Pain scores only; no
--- referral
research/adjuster-attacks.md:34:| A14 | **Attorney involvement / LOP-funded care** | Care began or escalated after the attorney was retained; charges inflated under a letter of protection | 1, TX §3 
research/adjuster-attacks.md:35:| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery ti
research/adjuster-attacks.md:94:from medical records, so it flags only what a record says ("referred by attorney", "letter of protection").
research/adjuster-attacks.md:126:5. Young Injury Law, "Gap in medical treatment" — https://younginjurylaw.com/blog/gap-in-medical-treatment-ohio-injury-claim/ — Explain gaps proactively with refer
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:05.196Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | grep -i T-008; grep -n -i \"attorney\\|lawyer\\|letter of protection\\|active or passive\\|transported\\|Vehicle\\|chiropract\" artifacts/review-evidence/T-008-adjuster-source-checks.txt | cut -c1-250",
 "description": "Check round-1 src 1 excerpts for attorney mention"
}
````

### User / tool · 2026-11-02T00:52:05.290Z

**tool result**
````
T-008-adjuster-source-checks.txt
4:   Verbatim: "1) Police report – Was there mention of any injury at the scene? Was the injured party transported to a medical facility?"
5:   Verbatim: "2) Vehicle photographs (auto claims) – Does the damage match? Are there paint transfers? What is the directional force of impact?"
7:   Verbatim: "6) Provider type – Was the claimant seen by a chiropractor or medical doctor?"
8:   Verbatim: "7) Duration and frequency – When did treatment start? How long did it last? Was it active or passive? Was it longer than an anticipated expected recovery date..."
9:   Result: takeaway in AA is accurate, but the attack map (A1-A11) has no row for delay-to-first-treatment, vehicle damage/MIST,
11:   `grep -n -i "delay\|first treatment\|property damage\|MIST\|minor impact\|attorney\|passive\|IME" research/adjuster-attacks.md` -> no output.
25:4) AA src 16 — Virginia Lawyers Weekly 2014 — https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/ (HTTP 200)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:06.406Z

Now curl the new sources (Nakashima src 19, IRMI Stowers TX src 12, Braun src 18 for MIST) and re-check src 1 for attorney language.

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:10.492Z

**tool call — Bash**
````
{
 "command": "D=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src; mkdir -p $D 2>&1; cd $D 2>/dev/null || D=$(mktemp -d); cd $D; UA=\"Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36\"\ncurl -s -o naka.xml -w \"efetch %{http_code}\\n\" \"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25584950&rettype=abstract&retmode=text\"\ncurl -sL -A \"$UA\" -o pm.html -w \"pubmed %{http_code}\\n\" https://pubmed.ncbi.nlm.nih.gov/25584950/\ncurl -sL -A \"$UA\" -o irmi.html -w \"irmi %{http_code}\\n\" https://irmi.com/term/insurance-definitions/stowers-doctrine\ncurl -sL -A \"$UA\" -o braun.html -w \"braun %{http_code}\\n\" https://braunslaw.com/claimclinic/claim-worth/specific-injuries/\ncurl -sL -A \"$UA\" -o cj.html -w \"cj %{http_code}\\n\" https://www.claimsjournal.com/news/national/2013/06/05/230291.htm\necho $D; ls -la",
 "description": "Fetch new sources with curl"
}
````

### User / tool · 2026-11-02T00:52:10.545Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (mkdir $)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:15.809Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src && cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src && UA=\"Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36\"\ncurl -s -o /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src/naka.txt -w \"efetch %{http_code}\\n\" \"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25584950&rettype=abstract&retmode=text\"\ncurl -sL -A \"$UA\" -o /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src/irmi.html -w \"irmi %{http_code}\\n\" https://irmi.com/term/insurance-definitions/stowers-doctrine\ncurl -sL -A \"$UA\" -o /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src/braun.html -w \"braun %{http_code}\\n\" https://braunslaw.com/claimclinic/claim-worth/specific-injuries/\ncurl -sL -A \"$UA\" -o /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src/cj.html -w \"cj %{http_code}\\n\" https://www.claimsjournal.com/news/national/2013/06/05/230291.htm\nls -la /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src",
 "description": "Fetch new sources into evidence dir"
}
````

### User / tool · 2026-11-02T00:52:19.376Z

**tool result**
````
efetch 200
irmi 200
braun 200
cj 200
total 712
drwxr-xr-x@  6 arsis  staff     192 Nov  1 18:52 .
drwxr-xr-x@ 99 arsis  staff    3168 Nov  1 18:52 ..
-rw-r--r--@  1 arsis  staff  193724 Nov  1 18:52 braun.html
-rw-r--r--@  1 arsis  staff   74517 Nov  1 18:52 cj.html
-rw-r--r--@  1 arsis  staff   83949 Nov  1 18:52 irmi.html
-rw-r--r--@  1 arsis  staff    2825 Nov  1 18:52 naka.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:22.733Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src && cat naka.txt; echo ======IRMI; sed -e 's/<[^>]*>/ /g' irmi.html | tr -s ' \\n' | grep -i -o \".\\{0,300\\}Stowers.\\{0,400\\}\" | head -5; echo =====BRAUN; sed -e 's/<[^>]*>/ /g' braun.html | tr -s ' \\n' | grep -i -o \".\\{0,200\\}\\(MIST\\|minor impact\\|soft tissue\\|soft-tissue\\).\\{0,200\\}\" | head -6; echo ====CJ; sed -e 's/<[^>]*>/ /g' cj.html | tr -s ' \\n' | grep -i -o \".\\{0,150\\}\\(attorney\\|lawyer\\|letter of protection\\).\\{0,150\\}\" | head -5",
 "description": "Extract key text from fetched sources"
}
````

### User / tool · 2026-11-02T00:52:26.035Z

**tool result**
````
1. Spine (Phila Pa 1976). 2015 Mar 15;40(6):392-8. doi: 
10.1097/BRS.0000000000000775.

Abnormal findings on magnetic resonance images of the cervical spines in 1211 
asymptomatic subjects.

Nakashima H(1), Yukawa Y, Suda K, Yamagata M, Ueta T, Kato F.

Author information:
(1)*Department of Orthopedic Surgery, Nagoya University Graduate School of 
Medicine, Aichi, Japan †Department of Orthopedic Surgery, Chubu Rosai Hospital, 
Chubu, Japan ‡Department of Orthopedic Surgery, Hokkaido Chuo Rosai Hospital 
Sekison Center, Hokkaido, Japan §Department of Orthopedic Surgery, Chiba Rosai 
Hospital, Chiba, Japan; and ¶Department of Orthopedic Surgery, Spinal Injuries 
Center, Fukuoka, Japan.

STUDY DESIGN: Cross-sectional study.
OBJECTIVE: The purpose of this study was to determine the prevalence and 
distribution of abnormal findings on cervical spine magnetic resonance image 
(MRI).
SUMMARY OF BACKGROUND DATA: Neurological symptoms and abnormal findings on MR 
images are keys to diagnose the spinal diseases. To determine the significance 
of MRI abnormalities, we must take into account the (1) frequency and (2) 
spectrum of structural abnormalities, which may be asymptomatic. However, no 
large-scale study has documented abnormal findings of the cervical spine on MR 
image in asymptomatic subjects.
METHODS: MR images were analyzed for the anteroposterior spinal cord diameter, 
disc bulging diameter, and axial cross-sectional area of the spinal cord in 1211 
healthy volunteers. The age of healthy volunteers prospectively enrolled in this 
study ranged from 20 to 70 years, with approximately 100 individuals per decade, 
per sex. These data were used to determine the spectrum and degree of disc 
bulging, spinal cord compression (SCC), and increased signal intensity changes 
in the spinal cord.
RESULTS: Most subjects presented with disc bulging (87.6%), which significantly 
increased with age in terms of frequency, severity, and number of levels. Even 
most subjects in their 20s had bulging discs, with 73.3% and 78.0% of males and 
females, respectively. In contrast, few asymptomatic subjects were diagnosed 
with SCC (5.3%) or increased signal intensity (2.3%). These numbers increased 
with age, particularly after age 50 years. SCC mainly involved 1 level (58%) or 
2 levels (38%), and predominantly occurred at C5-C6 (41%) and C6-C7 (27%).
CONCLUSION: Disc bulging was frequently observed in asymptomatic subjects, even 
including those in their 20s. The number of patients with minor disc bulging 
increased from age 20 to 50 years. In contrast, the frequency of SCC and 
increased signal intensity increased after age 50 years, and this was 
accompanied by increased severity of disc bulging.
LEVEL OF EVIDENCE: 2.

DOI: 10.1097/BRS.0000000000000775
PMID: 25584950 [Indexed for MEDLINE]======IRMI
ugrep: error: error at position 86
-\xbf][\x80-\xbf]*){0,400}
                          \___exceeds complexity limits


=====BRAUN
ugrep: error: error at position 122
f][\x80-\xbf]*){0,200}
                      \___exceeds complexity limits


====CJ
ugrep: error: error at position 117
etter of protection)(?:[^\n\x80-\xbf][\x80-\xbf]*){0,150}
                            exceeds complexity limits___/
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:30.843Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src && /usr/bin/python3 -I -c '\nimport re,sys,html\nfor f,pats in [(\"irmi.html\",[\"Stowers\"]),(\"braun.html\",[\"MIST\",\"minor impact\",\"soft tissue\",\"soft-tissue\",\"Colossus\",\"objective\"]),(\"cj.html\",[\"attorney\",\"lawyer\",\"letter of protection\",\"Provider type\",\"active or passive\"])]:\n    t=html.unescape(re.sub(r\"<script.*?</script>|<style.*?</style>\",\"\",open(f,encoding=\"utf-8\",errors=\"ignore\").read(),flags=re.S))\n    t=re.sub(r\"<[^>]+>\",\" \",t); t=re.sub(r\"\\s+\",\" \",t)\n    print(\"=====\",f,len(t))\n    for p in pats:\n        ms=[m.start() for m in re.finditer(re.escape(p),t,flags=re.I)]\n        print(\"--\",p,len(ms))\n        for s in ms[:2]: print(\"   \",t[max(0,s-200):s+300])\n'",
 "description": "Extract source text around key terms"
}
````

### User / tool · 2026-11-02T00:52:31.005Z

**tool result**
````
===== irmi.html 9067
-- Stowers 16
     Stowers Doctrine The Stowers doctrine holds that a liability insurer that undertakes the defense of an insured has a duty to act in good faith in settling a liability claim. It is named for a seminal Texas case, G.A. Stowers Furniture Co. v. American Indem. Co. , 15 S.W.2d 544 (Tex. Comm'n App. 1929
     Stowers Doctrine The Stowers doctrine holds that a liability insurer that undertakes the defense of an insured has a duty to act in good faith in settling a liability claim. It is named for a seminal Texas case, G.A. Stowers Furniture Co. v. American Indem. Co. , 15 S.W.2d 544 (Tex. Comm'n App. 1929). Courts have interp
===== braun.html 20012
-- MIST 9
    rsus subjective ones. Soft Tissue Claims The majority of car accident personal injury claims involve soft tissue injuries. These are called M.I.S.T. case, or Minor Impact Soft Tissue. The most common MIST injuries are a sprained/strained neck or back, but can also involve your shoulders, chest, knees, and hips. MIST injuries are usually caused by the kinetic energy that comes from the force of impact between two cars. The majority of MIST claims will be subjective. Objective evidence of MIST inj
    injuries. These are called M.I.S.T. case, or Minor Impact Soft Tissue. The most common MIST injuries are a sprained/strained neck or back, but can also involve your shoulders, chest, knees, and hips. MIST injuries are usually caused by the kinetic energy that comes from the force of impact between two cars. The majority of MIST claims will be subjective. Objective evidence of MIST injuries includes: Stress fractures in x-rays Arthrograms MRI’s Increased space in joints EMG tests CT Scans Loss of
-- minor impact 1
    r offers if you have objective injuries versus subjective ones. Soft Tissue Claims The majority of car accident personal injury claims involve soft tissue injuries. These are called M.I.S.T. case, or Minor Impact Soft Tissue. The most common MIST injuries are a sprained/strained neck or back, but can also involve your shoulders, chest, knees, and hips. MIST injuries are usually caused by the kinetic energy that comes from the force of impact between two cars. The majority of MIST claims will be 
-- soft tissue 6
    for an injury. Overall, adjusters and their claims software will give more weight to objective injuries. So you can expect to have bigger offers if you have objective injuries versus subjective ones. Soft Tissue Claims The majority of car accident personal injury claims involve soft tissue injuries. These are called M.I.S.T. case, or Minor Impact Soft Tissue. The most common MIST injuries are a sprained/strained neck or back, but can also involve your shoulders, chest, knees, and hips. MIST inju
    ht to objective injuries. So you can expect to have bigger offers if you have objective injuries versus subjective ones. Soft Tissue Claims The majority of car accident personal injury claims involve soft tissue injuries. These are called M.I.S.T. case, or Minor Impact Soft Tissue. The most common MIST injuries are a sprained/strained neck or back, but can also involve your shoulders, chest, knees, and hips. MIST injuries are usually caused by the kinetic energy that comes from the force of impa
-- soft-tissue 1
    merous medical studies showing cervical strain (neck) is a common cause of long term disability and that 40% of cervical strain/sprain patients have permanent symptoms and disabilities. Adjuster’s in soft-tissue cases usually look only at the facts/data and as mentioned in the information box are hard pressed to look at this type of case as anything other than a standard MIST case. Nevertheless, you can Google these types of phrases and quote some medical studies in your Demand Letter to support
-- Colossus 0
-- objective 7
    ury Slips & Falls Wrongful Death Resources FAQs Legal Guides Blog DIY ClaimClinic View All Resources Contact 404.418.8244 Claim Worth: Specific Injuries Home ClaimClinic Home Claim Worth Injury Types Objective vs. Subjective Adjusters and their claim evaluation software distinguish between objective and subjective injuries. Objective injuries are those that are observable or measurable. This usually means a diagnostic image (x-ray, MRI, etc) or lab test will show the injury. Objective injuries i
    Resources Contact 404.418.8244 Claim Worth: Specific Injuries Home ClaimClinic Home Claim Worth Injury Types Objective vs. Subjective Adjusters and their claim evaluation software distinguish between objective and subjective injuries. Objective injuries are those that are observable or measurable. This usually means a diagnostic image (x-ray, MRI, etc) or lab test will show the injury. Objective injuries include broken bones and herniated discs. Subjective injuries do not show up on any diagnost
===== cj.html 13578
-- attorney 7
    ing, Evaluating and Negotiating Your Way to a Competitive Advantage We see it time and time again, the stacks of papers that pile up on adjusters’ desks in the form of bodily injury (BI) demands from attorneys for injuries being claimed as the result of an accident. Of course, the attorney’s client is never at fault and most certainly the alleged injuries are always the result of your insured’s negligence. Attorneys are well aware that adjusters are very busy, often to the point of being overwor
     and time again, the stacks of papers that pile up on adjusters’ desks in the form of bodily injury (BI) demands from attorneys for injuries being claimed as the result of an accident. Of course, the attorney’s client is never at fault and most certainly the alleged injuries are always the result of your insured’s negligence. Attorneys are well aware that adjusters are very busy, often to the point of being overworked. The same often holds true for attorneys, who often utilize a staff of associa
-- lawyer 0
-- letter of protection 0
-- Provider type 1
    ion of symptoms other than what may be related to the accident? 5) Treatment patterns – How soon did treatment start? Were there gaps in treatment? Was there treatment on evenings and/or weekends? 6) Provider type – Was the claimant seen by a chiropractor or medical doctor? If the latter, what was their specialty? What are their credentials? Is their licensure current? Are there any prior or pending disciplinary actions with their current state, or prior states? 7) Duration and frequency – When 
-- active or passive 1
    ir licensure current? Are there any prior or pending disciplinary actions with their current state, or prior states? 7) Duration and frequency – When did treatment start? How long did it last? Was it active or passive? Was it longer than an anticipated expected recovery date among the general population for a similar complaint? 8) Objectivity – Were there objective findings (X-Ray, MRI, CT Scan)? Were the records and films obtained and reviewed by an independent medical expert? 9) Pain managemen
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:37.156Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-src && /usr/bin/python3 -I -c '\nimport re,html\nt=open(\"cj.html\",encoding=\"utf-8\",errors=\"ignore\").read()\nt=html.unescape(re.sub(r\"<script.*?</script>|<style.*?</style>\",\"\",t,flags=re.S)); t=re.sub(r\"<[^>]+>\",\" \",t); t=re.sub(r\"\\s+\",\" \",t)\nfor m in re.finditer(\"attorney|retain|referr\",t,flags=re.I): print(\"CJ>>\",t[max(0,m.start()-120):m.start()+160]); print()\nt=open(\"irmi.html\",encoding=\"utf-8\",errors=\"ignore\").read()\nt=html.unescape(re.sub(r\"<script.*?</script>|<style.*?</style>\",\"\",t,flags=re.S)); t=re.sub(r\"<[^>]+>\",\" \",t); t=re.sub(r\"\\s+\",\" \",t)\ni=t.find(\"Stowers Doctrine The\"); print(\"IRMI>>\",t[i:i+900])\n'",
 "description": "Print all attorney mentions in src 1 and IRMI definition"
}
````

### User / tool · 2026-11-02T00:52:37.309Z

**tool result**
````
CJ>> me and time again, the stacks of papers that pile up on adjusters’ desks in the form of bodily injury (BI) demands from attorneys for injuries being claimed as the result of an accident. Of course, the attorney’s client is never at fault and most certainly the alleged injuries ar

CJ>> rm of bodily injury (BI) demands from attorneys for injuries being claimed as the result of an accident. Of course, the attorney’s client is never at fault and most certainly the alleged injuries are always the result of your insured’s negligence. Attorneys are well aware that ad

CJ>> ’s client is never at fault and most certainly the alleged injuries are always the result of your insured’s negligence. Attorneys are well aware that adjusters are very busy, often to the point of being overworked. The same often holds true for attorneys, who often utilize a staf

CJ>> neys are well aware that adjusters are very busy, often to the point of being overworked. The same often holds true for attorneys, who often utilize a staff of associates, or negotiators, to push through an even greater volume of work. Fortunately, this latter bit of information 

CJ>>  request may not be granted. It is an important aspect of the claim to document when and why this request was made. The attorney needs to understand early on that you have an obligation to thoroughly investigate causation, duration and frequency of treatment. There should be due 

CJ>> otiations, arbitration or litigation. Another key component of the BI demand are the medical specials. Just because the attorney says it is so, doesn’t make it so. In many instances, there is a wide variety of subjectivity to findings. There are also numerous opportunities for bi

CJ>> nsure a timely response. Generally, this requirement is met by either tendering money (when warranted) or notifying the attorney, in writing, of additional documentation necessary to complete the injury evaluation. When reviewing the medical records, it is important to look at a 

IRMI>> Stowers Doctrine The Stowers doctrine holds that a liability insurer that undertakes the defense of an insured has a duty to act in good faith in settling a liability claim. It is named for a seminal Texas case, G.A. Stowers Furniture Co. v. American Indem. Co. , 15 S.W.2d 544 (Tex. Comm'n App. 1929). Courts have interpreted the "duty to defend" language in standard insurance policies as giving liability insurers absolute control over the conduct of the defense. Whether to settle a liability claim is therefore completely within the discretion of the liability insurer under the terms of the policy contract. If the injured party makes a pretrial offer to settle a liability claim for an amount within the liability policy limit, the insurer is not obligated to accept the offer and has the contractual right to take the claim to trial. To protect insureds from abusive practices, courts impose
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:57.386Z

**tool call — Bash**
````
{
 "command": "/usr/bin/python3 -I -c '\nimport json;d=json.load(open(\"evals/golden/sample.expected.json\"))\nfl=d.get(\"flags\") or d.get(\"must_flags\") or d\nprint(json.dumps(fl,indent=0)[:2500])' ; grep -n -i \"first recorded treatment\" spec/REQUIREMENTS.md | head -3",
 "description": "Check golden flag types for sample"
}
````

### User / tool · 2026-11-02T00:52:57.540Z

**tool result**
````
[
{
"id": "G1",
"type": "gap",
"level": "must",
"from_date": "2026-03-06",
"to_date": "2026-05-18",
"days": 73,
"cite": {
"all": [
6,
7
],
"any": []
},
"evidence": [
{
"record_no": 6,
"field": "excerpt",
"excerpt": "Discharged from PT after two missed appointments"
},
{
"record_no": 7,
"field": "excerpt",
"excerpt": "New onset pain radiating to right arm"
}
],
"summary": "Treatment gap of 73 days (2026-03-06 to 2026-05-18), longer than 30."
},
{
"id": "C1",
"type": "conflict",
"level": "must",
"cite": {
"all": [
7
],
"any": [
1,
2
]
},
"evidence": [
{
"record_no": 7,
"field": "excerpt",
"excerpt": "Date of accident per intake form: 2026-01-19"
},
{
"record_no": 1,
"field": "date",
"excerpt": "2026-01-09"
},
{
"record_no": 1,
"field": "excerpt",
"excerpt": "rear-ended at approx. 35 mph"
},
{
"record_no": 2,
"field": "date",
"excerpt": "2026-01-09"
}
],
"summary": "Accident date conflict: EMS (record 1) and ER (record 2) show the collision-day encounter on 2026-01-09; the intake form in record 7 gives 2026-01-19. Both shown side by side, never merged.",
"subtype": "accident_date"
},
{
"id": "C2",
"type": "conflict",
"level": "must",
"cite": {
"all": [
4,
6
],
"any": []
},
"evidence": [
{
"record_no": 4,
"field": "excerpt",
"excerpt": "Plan of care: 12 visits"
},
{
"record_no": 6,
"field": "excerpt",
"excerpt": "Discharged from PT after two missed appointments"
}
],
"summary": "Treatment-plan discrepancy: 12 visits planned (record 4) vs discharge at visit 9 after two missed appointments (records 5-6).",
"subtype": "treatment_plan"
},
{
"id": "P1",
"type": "pre_existing",
"level": "must",
"cite": {
"all": [
3
],
"any": []
},
"evidence": [
{
"record_no": 3,
"field": "excerpt",
"excerpt": "Patient reports low back pain in 2023, resolved"
}
],
"summary": "Prior low back pain (2023), reported resolved. Different body region from the cervical complaints; the tool must not relate it to the neck.",
"subtype": "prior_condition_reported"
},
{
"id": "P2",
"type": "pre_existing",
"level": "must",
"cite": {
"all": [
8
],
"any": []
},
"evidence": [
{
"record_no": 8,
"field": "excerpt",
"excerpt": "Findings may represent degenerative change"
}
],
"summary": "MRI wording (\"may represent degenerative change\") that an adjuster may argue shows a pre-existing condition; hedged, not a diagnosis.",
"subtype": "degenerative_language"
},
{
"id": "K1",
"type": "causation",
"level": "must",
"cite": {
"all": [
8
],
"any": []
},
"evidence": [
{
"record_no": 8,
"field": "excerpt",
"exc
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:17.891Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-adjuster.md",
 "content": "# T-008 round 2 — claims-adjuster-reviewer evidence\n\nCommit under review: 568e4b7 (diff `git diff 2c76cda 568e4b7 -- research/adjuster-attacks.md research/ASSUMPTIONS-proposed.md research/texas-pi-notes.md memory/GLOSSARY.md`).\nRaw source captures: artifacts/review-evidence/T-008-r2-src/ (naka.txt, irmi.html, braun.html, cj.html).\n\n## Resolution table (round-1 findings)\n\n| R1 finding | Sev | Acceptance test run | Output | Status |\n|---|---|---|---|---|\n| Delay to first treatment missing | major | `grep -n -i 'first treatment' research/adjuster-attacks.md`; `grep -n P-14 research/ASSUMPTIONS-proposed.md`; `grep -n 'Delay in treatment' memory/GLOSSARY.md` | adjuster-attacks.md:32 (A12 row, src 1, 16, \"first recorded treatment = 2026-01-09\") and :78 (notes); ASSUMPTIONS-proposed.md:21 P-14; GLOSSARY.md:24 | RESOLVED. Framed per D-017 (no computed delay); the R1 \"code computes it\" fix was overridden by D-017. Row value checked against sample.txt rec 1/2 (both 2026-01-09). |\n| MIST / attorney / passive care missing | major | `grep -n -i -E 'MIST\\|attorney\\|passive' research/adjuster-attacks.md` | rows A13 :33, A14 :34, A15 :35; notes :85-98 | RESOLVED in coverage, but the new rows carry new problems (see N1, N2, N3 below). T-009 probe re-run belongs to T-009, not this card. |\n| Brinjikji lumbar-only | minor | `grep -n -i lumbar research/adjuster-attacks.md` | :24 \"6 (lumbar), 19 (cervical)\", :56 \"reviewed **lumbar** imaging\", :127 \"**Lumbar spine only**\" | RESOLVED. Src 19 (Nakashima) verified by curl, see below. |\n| \"Australian PIC\" unlisted source | minor | `grep -n PIC research/adjuster-attacks.md`; `grep -o -E 'src [0-9]+' … \\| sort -u` | no PIC match; src refs = 1-7, 9-19, all in the list (19 numbered URL lines) | RESOLVED |\n| GLOSSARY adjuster vocabulary | minor | `grep -c -E 'MIST\\|Delay in treatment\\|Generals\\|Value drivers\\|Stowers' memory/GLOSSARY.md` → 4; with `-i` → 5; `grep -cE '^- \\*\\*'` → 46 | case-sensitive 4 only because the entry is \"General damages (generals)\"; my R1 test was case-sensitive by mistake | RESOLVED (intent met: MIST, Delay in treatment, generals, Value drivers, Stowers, BI, Soft-tissue, Active vs passive all present) |\n| \"approx.\" dropped from ROM | nit | `grep -n 'approx. 40%' research/adjuster-attacks.md` | :29 A9 row | RESOLVED |\n\n## New rows: accuracy and flag type (D-013/D-018)\n\n| Row | Flag type stated | Accurate vs records/sources? |\n|---|---|---|\n| A12 delay | context only (D-017) | Yes. Rec 1 & 2 dated 2026-01-09; both accident dates named; no delay computed. |\n| A13 MIST | causation (D-018 scene facts) | Yes. Rec 1 verbatim \"rear-ended at approx. 35 mph\", \"Transported to Central ER\". \"No vehicle-damage facts in the records\" — correct. Src 18 (Braun) verified: \"These are called M.I.S.T. case, or Minor Impact Soft Tissue.\" |\n| A14 attorney/LOP | causation (`litigation_referral`, D-018) | Rivera part correct (\"Not in records\"; \"the records do not say who referred him\"). Sourcing defect: cites src 1, but src 1 (Claims Journal, curl 200) has no text on attorney retention, referral or LOP — all 7 \"attorney\" hits are about attorneys sending demands/requests. The sentence \"Adjusters compare the attorney-retention date with when care started or escalated\" has no source. → N3 |\n| A15 duration/type | context only | NOT accurate. Row says \"active care (PT, referral to pain management, ESI recommended)\". sample.txt has one \"refer\" — rec 3 \"Refer to physical therapy\". Rec 7 names no referral source; A14 in the same file says \"the records do not say who referred him\". → N1. \"active care\" / \"Rivera's care is active\" (:98) is not in any record: rec 4-6 give ROM, plan, pain, discharge — no modality; ESI is recommended-only and is not active care. → N2 |\n\n## Source spot-checks (curl, 2026-11-01)\n\n1. Src 19 Nakashima, Spine 2015 — NCBI efetch PMID 25584950, HTTP 200. Verbatim: \"Most subjects presented with disc bulging (87.6%) … Even most subjects in their 20s had bulging discs, with 73.3% and 78.0% of males and females … few asymptomatic subjects were diagnosed with SCC (5.3%) … predominantly occurred at C5-C6 (41%) and C6-C7 (27%).\" Research figures CONFIRMED. Small wording stretch: src line says \"mostly at C5-C6\" (41% is a plurality, not most); study measured bulging, not protrusion; Japanese volunteers. Nit.\n2. TX src 12 IRMI Stowers — HTTP 200. Verbatim: \"named for a seminal Texas case, G.A. Stowers Furniture Co. v. American Indem. Co., 15 S.W.2d 544 (Tex. Comm'n App. 1929)… If the injured party makes a pretrial offer to settle a liability claim for an amount within the liability policy limit…\" CONFIRMED.\n3. AA src 18 Braun (MIST glossary source) — HTTP 200, MIST definition CONFIRMED (above). GLOSSARY \"Soft-tissue injury … without fracture or neurological deficit\" — that clause is not in src 18 (it says \"sprained/strained neck or back\"). Nit.\n4. AA src 1 Claims Journal — HTTP 200; re-checked for attorney/LOP/referral text: none (see A14).\n"
}
````

### User / tool · 2026-11-02T00:53:17.988Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-008-r2-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:20.458Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"referral to pain management|care is active|records do not say who referred|Adjusters$|attorney-retention\" research/adjuster-attacks.md | cut -c1-140; grep -n \"Soft-tissue injury\" memory/GLOSSARY.md | cut -c1-60; grep -n \"^19\\. Nakashima\" research/adjuster-attacks.md | cut -c1-30",
 "description": "Get line numbers for findings"
}
````

### User / tool · 2026-11-02T00:53:20.564Z

**tool result**
````
34:| A14 | **Attorney involvement / LOP-funded care** | Care began or escalated after the attorney was retained; charges inflated under a le
35:| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treat
92:negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). Adjusters
93:compare the attorney-retention date with when care started or escalated. The tool cannot know the retention date
98:care is active and shorter than planned. This is context for the adjuster persona, not a required flag.
26:- **Soft-tissue injury** — sprain/strain/whiplash-type 
141:19. Nakashima H. et al., "
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:52.796Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster-r2.md",
 "content": "# T-008 round 2 review — claims-adjuster-reviewer\n\n**Verdict: fail** (1 blocker, 1 major, 1 minor, 2 nits).\n\nAll six round-1 findings are resolved. The resolution table with the exact greps is in\n`artifacts/review-evidence/T-008-r2-adjuster.md`. A12 (delay to first treatment) follows D-017: it states \"first recorded\ntreatment = 2026-01-09\", names both accident dates, and computes no delay. I am judging whether the research documents the\nattack, not whether the tool computes it, and it does. Brinjikji is now labeled lumbar-only, and the cervical study added for\nthe neck point (Nakashima, src 19) checks out against its PubMed abstract. The PIC clause is gone. The glossary has 46 terms.\n\nThe new A15 row creates the problem I'm here to catch. It says Rivera had a \"referral to pain management\". No record says\nthat. Record 7 names no referral source, and A14, one line above in the same table, says \"the records do not say who referred\nhim\". My checklist item 19 says a pain-management referral stated anywhere is an invented fact. This table goes to T-009,\nthe persona files, and the golden files, so the invented referral would spread from here. A15 also calls Rivera's care\n\"active\", which no record supports. Separately, A14 cites src 1 for attorney-timing scrutiny, but src 1 says nothing about\nit.\n\n```json\n{\"card\": \"T-008\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit 568e4b7 vs 2c76cda: research/adjuster-attacks.md, research/ASSUMPTIONS-proposed.md, research/texas-pi-notes.md, memory/GLOSSARY.md; no app (research card); Jordan Rivera sample (evals/golden/sample.txt)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-008 (status in_review, rounds 1, commits 2c76cda, 568e4b7)\",\n  \"git log --oneline -- research memory/GLOSSARY.md | head -5 -> 568e4b7 top\",\n  \"git diff 2c76cda 568e4b7 -- the four T-008 files (read in full)\",\n  \"Re-ran every round-1 acceptance grep (first treatment, P-14, Delay in treatment, MIST|attorney|passive, lumbar, PIC, src-ref resolution, glossary count, approx. 40%); outputs in artifacts/review-evidence/T-008-r2-adjuster.md\",\n  \"grep -cE '^[0-9]+\\\\. .*https?://' -> chronology 10, adjuster-attacks 19, texas-pi-notes 12; grep -cE '^- \\\\*\\\\*' GLOSSARY -> 46\",\n  \"Read evals/golden/sample.txt (records 1-9) and grep -n -i refer -> only rec 3 'Refer to physical therapy'\",\n  \"Read evals/golden/sample.expected.json flags (G1, C1, C2, P1, P2, K1) to check flag types against A2/A4\",\n  \"Read memory/ORCHESTRATOR_DECISIONS.md D-013, D-017, D-018\",\n  \"curl NCBI efetch PMID 25584950 (Nakashima, src 19) HTTP 200 -> figures confirmed\",\n  \"curl IRMI Stowers doctrine (TX src 12) HTTP 200 -> confirmed\",\n  \"curl Braun Law (AA src 18, MIST glossary source) HTTP 200 -> MIST definition confirmed\",\n  \"curl Claims Journal (AA src 1) HTTP 200 -> searched for attorney/retain/referr/letter of protection: no attorney-timing or LOP text\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"source_quality_and_labeling\": 4, \"adversarial_coverage\": 4, \"accuracy_vs_sources\": 2, \"texas_relevance\": 4, \"usefulness_to_flags_and_lexicon\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A15 invents a 'referral to pain management' for Rivera\",\n   \"evidence\": \"research/adjuster-attacks.md:35 A15 Rivera column: 'active care (PT, referral to pain management, ESI recommended)'. evals/golden/sample.txt record 7 verbatim: 'New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.' (no referral source). `grep -n -i refer evals/golden/sample.txt` -> only line 16, rec 3 'Refer to physical therapy'. Same file :34 (A14) says: 'the records do not say who referred him'.\",\n   \"why_it_matters\": \"Persona checklist item 19: record 7 names no referral source, so 'referred to pain management' anywhere is an invented fact. A referral from the PCP would close my 73-day-gap argument, because it makes pain management look like a continuation of care. This table is the stated input to T-009, the personas and the golden files, so a fact invented here ends up in prompts and expected outputs. The file also contradicts itself (A14 vs A15).\",\n   \"fix\": \"Replace with what the records say: 'PT (rec 4-6), pain-management new-patient visit 2026-05-18 with no referral source stated (rec 7), cervical ESI recommended, not performed (rec 9)'.\",\n   \"acceptance_test\": \"grep -n -i 'referral to pain\\\\|referred to pain' research/ memory/ -r -> no output; A15 Rivera cell cites rec 7 with 'no referral source stated'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"A15 calls Rivera's care 'active', which no record supports\",\n   \"evidence\": \"research/adjuster-attacks.md:35 'active care (PT, …, ESI recommended)' and :98 'Rivera's care is active and shorter than planned.' Records 4-6 verbatim give only 'Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.' / 'Pain 4/10, improving…' / 'Discharged from PT after two missed appointments. Pain 3/10.' No modality or exercise is named. Record 9 ESI is 'Recommend' (not performed), and an injection is not active care in the src 1 sense ('Was it active or passive?'). Record 2 prescribes cyclobenzaprine.\",\n   \"why_it_matters\": \"Active vs passive care is a value driver I score. The research answers that question for the claimant with no record behind it. Downstream, a persona or prompt may treat 'active care' as a sample truth, and that is an overstated finding I would discount.\",\n   \"fix\": \"State 'records do not say whether PT was active or passive; plan 12 visits, discharged at visit 9 (rec 4, 6)'. Keep 'shorter than planned', because rec 4 and rec 6 support it.\",\n   \"acceptance_test\": \"grep -n -i 'care is active\\\\|active care (' research/adjuster-attacks.md -> no output; A15 row says modality is not stated in the records.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A14 cites src 1 for attorney-timing scrutiny that src 1 does not contain\",\n   \"evidence\": \"research/adjuster-attacks.md:34 A14 Evidence column '1, TX §3 (K&L), 3'; :92-93 'Adjusters compare the attorney-retention date with when care started or escalated.' (no citation). curl Claims Journal src 1 (HTTP 200): all 7 'attorney' hits are about attorneys sending BI demands or requests, e.g. 'Just because the attorney says it is so, doesn't make it so.' There are no hits for 'retain', 'referr' or 'letter of protection'. (My round-1 memory note that src 1 listed attorney timing was also wrong; I've corrected it.)\",\n   \"why_it_matters\": \"An attack row with a citation that doesn't support it is the same kind of defect as the round-1 'Australian PIC' clause. Lexicon `litigation_referral` rationales will cite this row.\",\n   \"fix\": \"Drop src 1 from A14, or cite only its provider-type item. Label the retention-timing sentence 'assumption (adjuster practice; persona §2)', or add a source that states it.\",\n   \"acceptance_test\": \"Every source number in the A14 row supports the attorney/LOP claim, or the claim is marked 'assumption'.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Nakashima src line says 'mostly at C5-C6'; abstract says 41%\",\n   \"evidence\": \"research/adjuster-attacks.md:141 'cord compression 5.3%, mostly at C5-C6'. PubMed abstract verbatim: 'predominantly occurred at C5-C6 (41%) and C6-C7 (27%)'. The study measured bulging, not protrusion, in Japanese volunteers.\",\n   \"why_it_matters\": \"41% is the largest share, not most of the cases. Defense counsel would catch it.\",\n   \"fix\": \"Write 'most often at C5-C6 (41%)' and note that the study measured disc bulging.\",\n   \"acceptance_test\": \"src 19 line includes '41%'.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"GLOSSARY soft-tissue definition adds a clause that src 18 doesn't state\",\n   \"evidence\": \"memory/GLOSSARY.md:26 'sprain/strain/whiplash-type injury without fracture or neurological deficit … Source: AA A9, src 18'. Src 18 (Braun, curl 200): 'The most common MIST injuries are a sprained/strained neck or back'. Src 18 has no fracture/neurological-deficit language.\",\n   \"why_it_matters\": \"This is minor, but the glossary rule is source-or-assumption for every claim.\",\n   \"fix\": \"Mark the 'without fracture or neurological deficit' clause as an assumption, or drop it.\",\n   \"acceptance_test\": \"The glossary line matches its source or carries 'assumption'.\"}\n ],\n \"whats_right\": [\n  \"A12/P-14 follow D-017 exactly: first recorded treatment 2026-01-09, both accident dates named, no delay computed.\",\n  \"A13 is accurate to rec 1 ('approx. 35 mph', 'Transported to Central ER') and says honestly that the records have no vehicle-damage facts.\",\n  \"The lumbar/cervical split is now honest, and the Nakashima and IRMI/Stowers sources check out verbatim.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T00:53:52.942Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:54.861Z

**tool call — Bash**
````
{
 "command": "/usr/bin/python3 -I -c '\nimport re,json;t=open(\"reviews/T-008-claims-adjuster-r2.md\").read();j=json.loads(re.search(r\"```json\\n(.*?)```\",t,re.S).group(1));print(j[\"verdict\"],[f[\"severity\"] for f in j[\"findings\"]])'; python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate review JSON and board"
}
````

### User / tool · 2026-11-02T00:53:55.062Z

**tool result**
````
fail ['blocker', 'major', 'minor', 'nit', 'nit']
ok (25 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:55.847Z

Now I'll update memory (correct the wrong src-1 claim, add the new pattern).

### Assistant · claude-opus-5-5 · 2026-11-02T00:54:03.388Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md",
 "content": "---\nname: research-attack-map-gaps\ndescription: Recurring adjuster-attack issues in Zlayt research (omitted attacks in r1; invented Rivera facts in fix rows in r2) and verified source facts\nmetadata:\n  type: project\n---\n\nT-008 round 1 (2026-11-01): adjuster-attacks.md A1–A11 omitted delay-to-first-treatment, MIST/transport, attorney/LOP timing,\nduration/passive care. Round 2 (568e4b7) added A12–A15 — but the new rows invented Rivera facts: A15 \"referral to pain\nmanagement\" (rec 7 names no referral source) and \"Rivera's care is active\" (no modality in recs 4-6). Rated blocker + major.\n\n**Why:** researchers fill \"Rivera records that trigger it\" cells from memory of the case, not from sample.txt; fix rounds\nare where new invented facts slip in.\n\n**How to apply:** on every re-review, grep each NEW row's Rivera cell against evals/golden/sample.txt (esp. \"refer\", \"active\",\n\"performed\", severity words). Correction: Claims Journal src 1 does NOT mention attorney retention/referral/LOP (curl\nre-checked r2) — it covers transport, vehicle damage, start/gaps, provider type, active/passive, duration. Verified by curl:\nBrinjikji AJNR 2015 = LUMBAR only; Nakashima Spine 2015 PMID 25584950 = cervical, bulging 87.6%, SCC 5.3% (C5-C6 41%);\nHerrera v. Madrak >12 missed PT; VLW src 16 \"eight days later\"; IRMI Stowers ok; Braun src 18 defines MIST; Fletcher v.\nSimmons 403. D-017: tool never computes delay — judge research, not code, on that. Use curl (no WebFetch); write curl\noutput only to a literal artifacts/review-evidence/ path (hook rejects `mkdir $VAR`). Evidence:\nartifacts/review-evidence/T-008-adjuster-source-checks.txt, T-008-r2-adjuster.md. Related: [[lexicon-review-method]].\n"
}
````

### User / tool · 2026-11-02T00:54:03.482Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:54:05.029Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "old_string": "- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 omissions (delay, MIST, attorney, passive care) + verified source facts",
 "new_string": "- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1 omissions, r2 invented Rivera facts in new rows; verified source facts"
}
````

### User / tool · 2026-11-02T00:54:05.124Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:54:12.242Z

**Verdict: fail** (1 blocker, 1 major, 1 minor, 2 nits). The round-1 findings are all fixed, but the new A15 row invents facts about Rivera. The review passes `python3 tools/board.py validate` (output: `ok (25 file(s))`).

**Round 1:** all 6 findings are resolved, checked by re-running each acceptance grep. A12 and P-14 follow D-017: they state "first recorded treatment = 2026-01-09", name both accident dates and compute no delay. Brinjikji is now labelled lumbar-only, the PIC clause is removed, "approx. 40%" is restored, and the glossary has 46 terms.

**Blocker:** `research/adjuster-attacks.md:35` (A15) lists Rivera's care as "referral to pain management". Record 7 names no referral source, and the only "refer" in `sample.txt` is record 3's "Refer to physical therapy". A14, one row above, says "the records do not say who referred him". Under checklist item 19 this is an invented fact, and this table feeds T-009, the personas and the golden files.

**Major:** A15 (`:35`, `:98`) calls Rivera's care "active". Records 4–6 name no modality, and the ESI is only recommended.

**Minor:** A14 cites src 1 for adjusters checking when the attorney was retained. I curled src 1 (Claims Journal) and it has no text on retention, referral or LOP. My round-1 memory note said it did; I've corrected that note.

**Nits:** the src 19 line says cord compression was "mostly at C5-C6", but the abstract says 41%. The glossary's soft-tissue entry adds "without fracture or neurological deficit", which src 18 doesn't state.

**New rows:** each row's flag type fits D-013/D-018. A12 and A15 are context only, A13 and A14 are causation. A13 matches record 1.

**Sources curled:** Nakashima (PMID 25584950), IRMI Stowers and Braun (MIST) are confirmed word for word. Claims Journal was re-checked for the A14 citation.

Files are in /Users/arsis/zlayt-pm-project:
- reviews/T-008-claims-adjuster-r2.md
- artifacts/review-evidence/T-008-r2-adjuster.md (resolution table)
- artifacts/review-evidence/T-008-r2-src/ (source captures)
