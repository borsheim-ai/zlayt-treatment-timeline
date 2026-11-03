# T-008 round 3 review — claims-adjuster-reviewer

**Verdict: fail** (1 blocker, 0 major, 2 minor, 1 nit).

All five round-2 findings are resolved. The invented pain-management referral is gone, and A15 now quotes rec 4, 6, 7 and 9.
"Active care" is replaced by "records 4–6 name no modality". A14 drops src 1 and cites the new Insurance Journal piece
(src 20), which I fetched: the author, date and all three quotes match. The retention-timing check is now labeled an
assumption. Nakashima says 41%, and the soft-tissue glossary entry is fixed. The sweep also correctly removed the old
claim that EMS/ER "give accident 01-09". Records 1 and 2 state no accident date.

I re-swept research/*.md and checked 31 sample-case hits; the hit-by-hit table is in
`artifacts/review-evidence/T-008-r3-adjuster-hits.md`. One invented characterization survives. adjuster-attacks.md:61-62
calls Rivera's rec 7 symptoms "the 'new onset' radicular symptoms". No record says "radicular". The project's own golden
file lists "Radicular symptoms in right arm." as an invented diagnosis (sample.expected.json:956-960), and hallucination
case H16 is this exact record. The sentence has been there since round 1, and I missed it in rounds 1 and 2. It is the same
class of defect as the r2 referral blocker: a research paraphrase of the sample that the records don't support. Persona §5
makes it a blocker. Two smaller paraphrases are inaccurate: A10 says the PT rate has "no visit count" (the labels say
"visit 8" and "visit 9"), and line 99 says "Rivera's records name no referral source" (rec 3 says "Refer to physical therapy").

```json
{"card": "T-008", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit da17ba2 vs 568e4b7: research/adjuster-attacks.md, research/ASSUMPTIONS-proposed.md, research/chronology-practice.md, research/texas-pi-notes.md, memory/GLOSSARY.md (lexicon_selfcheck.py diff belongs to T-009 commit 2fee2df, not reviewed); no app (research card); Jordan Rivera sample (spec/SPEC.md Appendix A = evals/golden/sample.txt)",
 "exercised": [
  "python3 tools/board.py show T-008 -> status in_review, rounds 2, commits [2c76cda, 568e4b7, da17ba2]",
  "git log --oneline -4 -- research memory/GLOSSARY.md -> da17ba2 top; git show --stat da17ba2 -> 5 files, 35+/25-",
  "git diff 568e4b7..da17ba2 -- research/*.md memory/GLOSSARY.md (read in full)",
  "Read spec/SPEC.md:53-65 and evals/golden/sample.txt (records 1-9); read research/adjuster-attacks.md:1-130 in full",
  "r2 acceptance greps (artifacts/review-evidence/T-008-r3-adjuster-greps.txt): grep -rn -i 'referral to pain|referred to pain' research/ memory/ -> only memory/LESSONS.md:17-18 (lesson text, not research); grep 'care is active|active care (' -> exit 1 (none); '41%' at adjuster-attacks.md:59,149; source counts AA 20, CP 10, TX 12; GLOSSARY terms 46",
  "Sample-case sweep: 3 greps over research/*.md + GLOSSARY (commands and 31-hit table in artifacts/review-evidence/T-008-r3-adjuster-hits.md)",
  "git show 2c76cda / 568e4b7 :research/adjuster-attacks.md | grep -n radicular -> lines 51 / 61 (pre-existing)",
  "grep -rn -i radicul evals/ app/ personas/ -> sample.expected.json:956-974 must-not pattern incl. 'Radicular symptoms in right arm.'; hallucinations.jsonl:16 H16 on record 7",
  "Read evals/golden/sample.expected.json flags G1, C1, C2, P1, P2, K1-K5 (A2 'causation + conflict' matches C2/K2)",
  "Read memory/ORCHESTRATOR_DECISIONS.md D-017, D-018",
  "curl -L insurancejournal.com/news/national/2026/01/21/854959.htm -> HTTP 200, 103085 bytes; title, author Pragatee Dhakal, published 2026-01-21; verbatim 'steer claimants into higher cost services', 'plaintiffs' counsel refer injured claimants to clinics or pain-management centers', 'defense counsel may challenge causation or necessity'; 0 hits for 'letter of protection', 'retain', 'retention' (artifacts/review-evidence/T-008-r3-insurancejournal-checks.txt)"
 ],
 "verdict": "fail",
 "scores": {"source_quality_and_labeling": 4, "adversarial_coverage": 5, "accuracy_vs_sources": 3, "texas_relevance": 4, "usefulness_to_flags_and_lexicon": 4},
 "findings": [
  {"severity": "blocker",
   "title": "Research labels Rivera's rec 7 symptoms 'radicular', a diagnosis term no record uses",
   "evidence": "research/adjuster-attacks.md:61-62 'the plaintiff uses the \"new onset\" radicular symptoms to argue aggravation.' Rec 7 verbatim: 'New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.' grep -rn -i radicul evals/ -> evals/golden/sample.expected.json:956 must-not 'Invents or substitutes a diagnosis not in the records (whiplash, radiculopathy/radicular, ...)', :960 example 'Radicular symptoms in right arm.'; evals/golden/hallucinations.jsonl:16 H16 'Record describes symptoms (radiating pain, numbness) and orders an MRI. No diagnosis is stated.' Present since 2c76cda:51 and 568e4b7:61; the round-3 sweep (handoff: 'every sample-case claim re-anchored to quotes') missed it.",
   "why_it_matters": "If 'radicular' ends up in a summary, that is an upgrade I can attack: no physician diagnosed radiculopathy, and the MRI is hedged. The project's own golden file treats the phrase as an invented diagnosis. Research feeds personas, lexicon and golden files (LESSONS.md:17), so the term spreads from here. This is the same defect class as the r2 referral blocker.",
   "fix": "Replace with the record's words: 'the plaintiff uses rec 7 \"New onset pain radiating to right arm with numbness in fingers\" to argue aggravation.'",
   "acceptance_test": "grep -rn -i 'radicul' research/*.md -> no hit that describes the sample (citations of literature titles excepted)."},
  {"severity": "minor",
   "title": "A10 says the PT rate has 'no visit count'; the records carry visit numbers",
   "evidence": "research/adjuster-attacks.md:30 'PT rate $185/visit with no visit count → cannot total'. Rec 4 'Plan of care: 12 visits. Charge per visit $185.'; source labels rec 5 'Capital PT, visit 8', rec 6 'Capital PT, visit 9'.",
   "why_it_matters": "The conclusion is right, but the reason given is wrong. It implies that a visit count would allow a total (9 × $185), and that is exactly the extrapolation I reject (checklist item 11). The records do give counts. They give no PT charge.",
   "fix": "'Rec 4 \"Charge per visit $185\" is a rate; no PT charge is stated for any visit, so no PT amount is totaled (visit labels 8 and 9 and plan \"12 visits\" do not change that).'",
   "acceptance_test": "A10 row no longer says 'no visit count' and states that the rate is not multiplied."},
  {"severity": "minor",
   "title": "'Rivera's records name no referral source' is overbroad; rec 3 is a PCP referral to PT",
   "evidence": "research/adjuster-attacks.md:99 'Rivera's records name no referral source.'; :34 A14 'no record states a referral source or an attorney'. Rec 3 verbatim: 'Refer to physical therapy 2x/week for 6 weeks.' A15 (:35) scopes it correctly: 'rec 7 \"Hill Country Pain Management, new patient\", no referral source stated'.",
   "why_it_matters": "An unscoped negative about the records is still a paraphrase the records contradict. The PCP referral to PT is a fact that helps the claimant, because physician-directed PT answers 'self-directed care'. A golden or persona author could copy the line as written.",
   "fix": "Scope it: 'Rec 7 names no referral source; the only stated referral is rec 3 \"Refer to physical therapy\".'",
   "acceptance_test": "Lines 34 and 99 refer to rec 7 or quote rec 3."},
  {"severity": "nit",
   "title": "Src 20 label omits the author's vendor affiliation",
   "evidence": "research/adjuster-attacks.md:151 '(Insurance trade press, opinion piece.)'. Page byline: 'Pragatee Dhakal is the director of product strategy and enablement at CLARA Analytics, a leading provider of artificial intelligence (AI) technology for insurance claims'.",
   "why_it_matters": "Source balance is labeled per source elsewhere. A claims-AI vendor writing about medical abuse has a commercial angle.",
   "fix": "Append '; author is at CLARA Analytics, a claims-AI vendor'.",
   "acceptance_test": "Src 20 line names the affiliation."}
 ],
 "whats_right": [
  "A15 and A14 now quote rec 4, 6, 7 and 9 only, with 'no referral source stated' and 'recommended, not performed' scoped to the right records.",
  "A7/A12/P-14 correctly say only rec 7 states an accident date (records 1-2 carry header dates only), and no delay is computed (D-017).",
  "Src 20 checks out verbatim (author, date, three quotes), and the retention-timing claim is honestly labeled an assumption."
 ],
 "questions_for_chris": []}
```
