# T-015 — paralegal-reviewer (Maria Delgado lens)

**Verdict: fail** (1 blocker, 3 majors, 5 minors, 2 nits).

The arithmetic holds up. I recomputed all 8 sample gaps (0/7/7/28/14/73/11/14) and every gap in the 8 synthetic cases with python `datetime`, and they match the golden files exactly. The $8,390 total is right. `sample.txt` matches SPEC Appendix A word for word (all 9 records). `check_golden.py` passes. The problems are in the levels: what the golden set lets a tool skip, and what it would mark a tool down for. Two of the adjuster's strongest arguments in the sample case (new onset after the 73-day gap, and the wrong accident date on the intake form) are optional ("should") here. Appendix C lists them under "Expected flags (at minimum)". In case_06, two of the three prior-condition mentions are optional too. A flag on the "denies prior neck problems" vs "chiropractor since a lifting injury" inconsistency would be counted as a false positive. Some of the hard-fail regexes also miss phrasings from the project's own hallucination set.

Blind comparison: I wrote my chronology, flags and charges for all 8 synthetic cases before opening any expected.json (`artifacts/review-evidence/T-015-paralegal-blind.md`). Entries, dates, amounts and classes match mine on every case. One difference: I read the case_01 date `04/05/2026` as April 5, because the same provider wrote `02/17/2026`. The golden set leaves it null and sends it to a human. I accept that, since reading it as May 4 would create a 40-day gap flag. The differences that matter are all in flags (see findings).

Commands run (exact output):
- `python3 evals/golden/check_golden.py` → `golden OK: 9 cases (8 synthetic), 20 hallucination items, all stress types covered` (exit 0)
- `python3 artifacts/review-evidence/T-015-paralegal-regex-probe.py` → output saved to `artifacts/review-evidence/T-015-paralegal-regex-probe.out.txt` (all gaps OK; the regex misses listed below)
- `git status --porcelain evals/golden/` → (empty); `git diff --stat 47520a8 -- evals/golden/` → (empty), so the working tree equals commit 47520a8
- First line of every `evals/golden/*.txt` is `SYNTHETIC — ...` (head -1 loop). `grep -c -i synthetic evals/golden/hallucinations*.jsonl` → `0` and `0`

```json
{"card": "T-015", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 47520a8: evals/golden/** (README.md, sample.txt, sample.expected.json, case_01..08 .txt/.expected.json, hallucinations.jsonl, hallucinations_controls.jsonl, check_golden.py); refs spec/SPEC.md App A, spec/SAMPLE_CASE_TRUTHS.md, docs/LLM_VS_CODE.md, personas/paralegal.md, personas/claims-adjuster.md; no app (card is pre-code eval data); sample case evals/golden/sample.txt",
 "exercised": [
  "python3 tools/board.py show T-015 (AC 1-4 read)",
  "python3 evals/golden/check_golden.py -> 'golden OK: 9 cases (8 synthetic), 20 hallucination items, all stress types covered', exit 0",
  "Recomputed every sample gap and the $8,390 total with python datetime -> [0, 7, 7, 28, 14, 73, 11, 14], 8390",
  "Script check: all 9 Appendix A rows of spec/SPEC.md appear verbatim (Date/Source/Excerpt) in sample.txt -> 9x True",
  "Wrote blind chronology/flags/charges for case_01..08 before opening expected.json -> artifacts/review-evidence/T-015-paralegal-blind.md, then diffed against each expected.json",
  "artifacts/review-evidence/T-015-paralegal-regex-probe.py: recomputed all synthetic gap tables (all OK) and probed must_not regexes with known-bad phrasings (output in T-015-paralegal-regex-probe.out.txt)",
  "Read all 20 hallucinations.jsonl items + 5 controls; checked H17/H19 record_text is verbatim in case_07/case_03 and H01-H20 sample excerpts are verbatim in sample.txt",
  "head -1 of every evals/golden/*.txt (SYNTHETIC label); grep SYNTHETIC in jsonl; git status/diff vs 47520a8 (clean)"
 ],
 "verdict": "fail",
 "scores": {"arithmetic_and_dates": 5, "appendix_c_fidelity": 3, "flag_levels_realism": 2, "adjuster_attack_coverage": 3, "must_not_strength": 3, "synthetic_labeling": 4},
 "findings": [
  {"severity": "blocker", "title": "Appendix C 'at minimum' causation items K4 (new onset after 73-day gap) and K5 (wrong accident date) are downgraded to optional 'should'",
   "evidence": "spec/SAMPLE_CASE_TRUTHS.md:5 'Expected flags (at minimum):' and :9 lists '\"New onset\" symptoms after a 73-day gap (7); the wrong accident date (7)' as causation-weakening. evals/golden/sample.expected.json:540-578 K4/K5 have \"level\": \"should\". README.md:76 '`should` flags earn credit if found but never count as misses'. README.md:83 claims a tool 'that surfaces them only through those flags still gets credit', but the scoring rule at README.md:76 matches on type, so a gap (G1) or conflict (C1) flag can never satisfy a causation-type golden flag. docs/LLM_VS_CODE.md:77 (the project's own worked example) expects a model flag that 'new onset after a 73-day gap could be used to argue a new cause'. personas/claims-adjuster.md:22 lists it as a check.",
   "why_it_matters": "These are the adjuster's lead causation arguments on this file: the radiating arm symptoms first appear 129 days after the collision, and the intake form gives the wrong accident date. As written, a tool that never tells me either one weakens causation scores 100% causation recall and passes the ship bar. AC 2 requires encoding 'every Appendix C truth'. Encoding a minimum expectation as optional does not meet that.",
   "fix": "Set K4 and K5 to level 'must'. If double-counting with G1/C1 is the concern, add an explicit cross-type rule in README scoring (e.g. K4 is satisfied by a causation flag citing record 7 OR by G1 text that names 'new onset' as a causation risk) and implement it in evals.run. Do not use 'should'.",
   "acceptance_test": "jq '.flags[]|select(.id==\"K4\" or .id==\"K5\")|.level' evals/golden/sample.expected.json returns \"must\" twice; an evals.run fixture with G1+C1 but no causation flag on record 7 reports causation recall < 1.0 for the sample."},
  {"severity": "major", "title": "case_06: two of three explicit prior-condition mentions are 'should' (P2 baseline stiffness, P3 'old shoulder problem'), inconsistent with the sample's P1",
   "evidence": "evals/golden/case_06_subtle_pre_existing.expected.json:193-215 P2 and P3 \"level\": \"should\"; P3 evidence 'the old shoulder problem is acting up again'; P2 'occasional stiffness in the mornings at baseline'. Compare sample.expected.json:440 P1 (prior low back pain, a different body region, resolved) = 'must'. SPEC.md:39 must-have: 'mentions of prior or pre-existing conditions'.",
   "why_it_matters": "The case exists to test subtle pre-existing conditions, yet a tool that catches only the chiropractor line and misses 'old shoulder problem ... again' and 'stiffness ... at baseline' still gets full pre_existing recall here. Both are things an adjuster quotes back in a response letter (MIST defense: prior neck/shoulder problems). My blind list had all three as required.",
   "fix": "Make P2 and P3 'must'. Keep M1/M4 (do not assign a body region to the chiropractic care; do not relate the shoulder to the collision).",
   "acceptance_test": "All case_06 pre_existing flags are level 'must'; an evals.run fixture surfacing only P1 scores pre_existing recall 1/3 on case_06."},
  {"severity": "major", "title": "case_06: the ER denial vs prior chiropractic history inconsistency would be scored as a false positive",
   "evidence": "case_06_subtle_pre_existing.txt rec 1 'Patient denies prior neck problems' vs rec 2 'Has been seeing a chiropractor off and on since a lifting injury several years ago'. expected.json has no conflict flag, and the only tolerated entry, T1 (line 250), is type pre_existing. Per README.md:76 a candidate matching no golden/should/tolerated flag is a false positive (precision >= 0.9 per type). personas/paralegal.md:73 cites 'unflagged conflicting onset histories' as a common chronology error.",
   "why_it_matters": "'Your client told the ER he had no prior neck problems but had been seeing a chiropractor for years' is the credibility attack I most need to see before the demand goes out, so the attorney can request the chiropractic records. As written, a tool that surfaces it is penalized, which pushes the product toward hiding it.",
   "fix": "Add a conflict flag at level 'should' (at minimum 'tolerated'), subtype history_inconsistency, cite all [1,2], summary worded as 'possible inconsistency; body region of the chiropractic care not stated; request records'. Add a must_not (judge) against stating that the patient misrepresented or lied, or that the chiropractic care was for the neck.",
   "acceptance_test": "A candidate conflict flag citing records 1 and 2 of case_06 is scored TP or tolerated, not FP, by evals.run."},
  {"severity": "major", "title": "Hard-fail must_not regexes miss common phrasings, including the project's own seeded hallucinations; check_golden.py has no positive tests",
   "evidence": "artifacts/review-evidence/T-015-paralegal-regex-probe.out.txt: sample M9 (sample.expected.json:654) caught=False for H14 'Patient completed all 12 planned PT visits with full recovery.' and for 'Patient made a full recovery.' Sample M2 (line 605) caught=False for 'Neck injury caused by the January collision.', 'Symptoms due to the motor vehicle accident.', 'Degenerative findings at C5-C6.' check_golden.py:163-175 only proves that regexes do NOT match the input. It never checks that they DO match a known-bad example.",
   "why_it_matters": "Appendix C says the tool must not turn 'may represent degenerative change' into 'degenerative' and must not state causation. The deterministic layer that is supposed to guarantee this lets through the most likely wordings, so the eval relies entirely on the LLM judge for exactly the statements that cost the firm credibility.",
   "fix": "Add a 'must_hit' list of bad example strings to every regex must_not (include the matching hallucinations.jsonl candidate_summary) and have check_golden.py assert each one matches. Widen M9 (recover(y|ed)|full recovery|resolved completely), M2 (caused by|due to|from) + optional modifiers before collision|accident|crash|MVA|motor vehicle, and a bare '^|\\. ?Degenerative' when not preceded by 'may represent'.",
   "acceptance_test": "check_golden.py fails if any must_hit string is not matched; the probe script reports caught=True for all sample probes."},
  {"severity": "minor", "title": "case_08 is missing must_nots for invented laterality, injection-as-performed, and 'surgical consult recommended'",
   "evidence": "case_08_diagnosis_temptation.txt never states left/right and says 'Plan: injection versus surgical consult, patient to decide'. must_not ids M1-M5 (expected.json:186-210) contain none of these. Probe: 'Right shoulder pain after a fall.', 'Patient received a shoulder injection.' and 'Surgical consultation recommended.' all caught=False.",
   "why_it_matters": "A wrong side in a demand letter is the error an adjuster spots first. 'Received an injection' invents treatment, the same as sample M13 / H20 for the ESI.",
   "fix": "Add regex must_nots: (?i)\\b(left|right|bilateral)\\s+shoulder; (?i)(received|underwent|administered|given)\\b.{0,20}injection; (?i)surgical consult\\w*\\s+(was\\s+)?(recommended|ordered|scheduled)|referred (for|to) surgical.",
   "acceptance_test": "The three probe strings are caught by case_08 must_nots; check_golden.py still proves none match the input."},
  {"severity": "minor", "title": "Gap math counts non-visit records (billing statement, phone note) as treatment dates, and no case tests a non-visit record hiding a >30-day gap",
   "evidence": "README.md:44 'consecutive DISTINCT parsed dates, all providers'. case_03 E2 (expected.json:60) is 'Bayview Chiropractic, billing statement' dated 2026-08-10 and is a gap endpoint (08-03->08-10, 08-10->08-17). case_01 rec 8 is a 'phone note'. personas/paralegal.md:20 'nothing is dated by when a note was entered rather than the date of service'.",
   "why_it_matters": "Adjusters measure gaps between treatment visits. A billing statement or phone call between two visits 45 days apart would hide a real gap. No numbers change in the current set, but the golden rule as written would bless that behavior once it matters.",
   "fix": "Decide and document whether non-encounter records (billing statement, phone note, records request) break a gap. Add one synthetic case where a billing statement sits inside a 40+ day gap between visits, with the expected flag.",
   "acceptance_test": "A case exists with a non-visit record inside a >30-day interval between visits, and its expected gap flag is present and documented in README."},
  {"severity": "minor", "title": "No tolerated_flags for legitimate paralegal observations, so a careful tool is charged false positives",
   "evidence": "case_03: chiro billing statement 'Statement for initial exam and x-ray: $1,2OO.' (rec 2, 08-10) plus a separate radiology 'Lumbar spine X-ray, 2 views. Radiology charge: $240' (rec 5, 09-02). Possible duplicate imaging/billing, and nothing tolerated. case_04/case_02 tolerated_flags are empty. personas/claims-adjuster.md:10 'bills that don't match the notes'. Scoring rule README.md:76 counts unmatched candidates as FP.",
   "why_it_matters": "Precision is scored per type at >= 0.9 on small counts, so one legitimate extra conflict flag on case_03 can sink conflict precision. That pushes the product toward silence on the billing questions I would want raised.",
   "fix": "Add tolerated conflict T1 on case_03 citing [2,5] (possible duplicate x-ray billing). Review each case for other legitimate-but-not-required observations and tolerate them.",
   "acceptance_test": "A conflict candidate citing case_03 records 2 and 5 is scored as tolerated, not FP."},
  {"severity": "minor", "title": "Sample C1 evidence for the 2026-01-09 accident date quotes irrelevant text",
   "evidence": "sample.expected.json:407 evidence for record 2 is 'CT head negative'. The 01-09 date comes from the record Date line and the EMS mechanism, not from that phrase.",
   "why_it_matters": "If the product copies this pattern, the side-by-side conflict view shows me 'CT head negative' as proof of a date. I cannot verify the conflict from that excerpt.",
   "fix": "Use field 'source'/date evidence for records 1-2 (Date: 2026-01-09 with 'Austin EMS run report' / 'rear-ended at approx. 35 mph'), and drop 'CT head negative'.",
   "acceptance_test": "C1 evidence for each cited record contains or points to the 2026-01-09 date or the collision mechanism."},
  {"severity": "minor", "title": "Hallucination set is 18/20 from the sample case and has no laterality-swap or provider-attribution-swap item",
   "evidence": "Probe count: Counter({'sample': 18, 'synthetic': 2}) (only H17 case_07 and H19 case_03). No category in hallucinations.jsonl swaps left/right (e.g. record 7 'right arm' -> 'left arm') or attributes a finding to the wrong provider.",
   "why_it_matters": "Side swaps and wrong-provider attribution are the most common chronology errors I correct. A judge measured almost entirely on one case can reach 95% recall and still miss them on real files.",
   "fix": "Replace 2-4 sample items with synthetic-case items, including one laterality swap and one wrong-provider attribution (e.g. case_05 'Lone Star' finding attributed to Alamo).",
   "acceptance_test": "hallucinations.jsonl contains >= 1 laterality_swap and >= 1 wrong_provider item, and >= 6 items come from synthetic cases."},
  {"severity": "nit", "title": "Seeded-hallucination files carry no SYNTHETIC label",
   "evidence": "grep -c -i synthetic evals/golden/hallucinations.jsonl evals/golden/hallucinations_controls.jsonl -> 0 / 0",
   "why_it_matters": "If they are copied out of the repo, nothing marks them as fictional. The .txt cases are labeled properly.",
   "fix": "Add \"synthetic\": true to each JSONL object (and assert it in check_golden.py).",
   "acceptance_test": "Every JSONL line has synthetic=true; check_golden.py enforces it."},
  {"severity": "nit", "title": "Several record dates are after today's date (2026-11-01)",
   "evidence": "case_02 all 2028 dates; case_06 rec 5 2026-11-16; case_08 rec 3-4 2026-11-03 / 2026-11-24.",
   "why_it_matters": "If the product later adds a 'date of service in the future' sanity check (a reasonable data-entry catch), these golden cases will trip it unexpectedly.",
   "fix": "Note in README that future dates are intentional (leap-year 2028), or decide now how a future-date warning is scored.",
   "acceptance_test": "README states the policy for future-dated records."}
 ],
 "whats_right": [
  "Every gap (sample 7/7/28/14/73/11/14; all 8 synthetic, incl. 2028 leap-year 30-day Feb->Mar) and the $8,390 total match my independent datetime recomputation, and sample.txt is verbatim Appendix A.",
  "Rates and OCR-garbled amounts ($185, $95-per-adjustment, $1,2OO, $9S.00) are never totaled, have value null where unclear, and forbidden guess-sums are enumerated.",
  "Real paralegal nuance: case_01 N2 (a completed-program 'Discharged' is not noncompliance), case_06 T1/M1 (a denial is not a finding; chiropractic body region not invented), case_05 Alamo-vs-Lone-Star practice conflict kept verbatim."
 ],
 "questions_for_chris": [
  "Facility names in synthetic cases (e.g. 'Harlan County EMS', 'Alamo Orthopedics', 'Lone Star Orthopedics', 'Brookside ER') may match real Texas/US providers; I could not verify offline. Do you want a rule that synthetic facility names be checked as non-existent or obviously fictional?",
  "case_04 'Fell from a ladder at a worksite' carries a workers'-comp/non-subscriber question the attorney would want; M4 correctly forbids the tool from concluding it. Is surfacing such a fact (via the excerpt only) enough for the firm, or should there be a non-scored 'attorney attention' note type?"
 ]}
```
