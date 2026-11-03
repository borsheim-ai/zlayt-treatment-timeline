# Review T-028 (staff-engineer-reviewer): ADR consistency pass

Verdict: **fail** (1 blocker, 3 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).

Card ACs against the output: AC1 supported. AC2 category names supported, per-category templates not. AC3 confirm_date gap, date_invalid and cut line supported; the mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit. AC4 golden reference supported; the AI line claim is false; the D-id wording overstates the citations.

The blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris).

Mechanical results (artifacts/review-evidence/T-028-review-checks.py): 8 of 12 checks pass. Failing: AC2 per-category templates, AC4b api.md mg. units, AC5 AI line, SPEC-8.1 export diff.

```json
{"card": "T-028", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git de749c2 (= HEAD for memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; no uncommitted edits to them); spec/REQUIREMENTS.md and evals/golden at HEAD f454c41; no app URL (app/backend and app/pipeline.py do not exist); sample case evals/golden/sample.txt",
 "exercised": [
   "python3 tools/board.py show T-028 -> EXIT=0, status in_review, 4 ACs read (claims not trusted)",
   "read personas/staff-engineer.md in full",
   "grep -c SUMMARY_DROPS_QUALIFIER memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md -> 1 / 3 / 1; grep -n shows api.md:439, DECISIONS.md:147,244,309, LLM_VS_CODE.md:43",
   ".venv/bin/python -I yaml load app/llm/lexicon.yaml -> version 2, 66 entries, 13 distinct categories: accident_date_provenance, alternative_cause, degenerative_language, litigation_referral, missed_care, new_onset, objective_negative, patient_report, pre_existing, prior_surgery, recovery_context, scene_facts, speculative_language",
   "read memory/DECISIONS.md ADR-013 (lines 246-263): all 13 lexicon names present in the closed list; per-category template text: 0 of 13; only generic template statements at lines 258-259; grep template -> lines 243, 258, 259, 261",
   "ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty",
   "read memory/contracts/api.md error codes (line 9) and confirm_date section (lines 199-212); grep date_invalid / non-candidate -> date_invalid is the only non-candidate code",
   "api.md:209-210 gap_flags [] checked against evals/golden/case_01_date_formats.expected.json: gap_excluded_records [8], record 8 kind phone_note, date null, flags [], record_warnings []",
   "read app/llm/lexicon.yaml code_lists.non_encounter: phone_or_message pattern matches 'Dr. Orla Pennywhistle, phone note' (golden case_01 record 8)",
   "verified api.md:86-92 sentence offsets against evals/golden/sample.txt absolute positions: sample[396:416]='Dx: cervical strain;', sample[477:502]='Rx cyclobenzaprine 10 mg.', sample[503:532]='Follow up with PCP in 1 week.', sample[533:552]='ER charges: $6,240.'",
   "applied R-TL-2 splitter (abbreviation list incl. mg., D-021) to sample record 2 excerpt via artifacts/review-evidence/T-028-review-checks.py: units [(396,416),(417,458),(459,476),(477,532),(533,552)]; api.md:91 gives (477,502),(503,532) -> mismatch",
   "grep -n 'AI assistance' memory/DECISIONS.md spec/REQUIREMENTS.md; exact-string counts: R-EX-4(1) sentence in spec 1, in DECISIONS 0; golden-variant sentence in DECISIONS 1, spec 1, LLM_VS_CODE 1, golden 1",
   "git show de749c2 -- memory/DECISIONS.md: ADR-009 internal-notes bullet changed from the R-EX-4(1) text ('AI assistance: this chronology ... before export.' + 'Pending items') to the golden text, label kept as 'the fixed text of R-EX-4(1)'",
   "read spec/REQUIREMENTS.md R-EX-4 (line 122), spec section 8 reconciliation rows 1-3 (lines 362-371), R-TL-2 (line 49), R-TL-10 (line 57), R-CH-4 (line 81)",
   "read memory/ORCHESTRATOR_DECISIONS.md D-003, D-021, D-022, D-023, D-024; D-021 contains the mg. abbreviation rule; ids cited in the four docs all resolve (AC8 PASS)",
   "read app/README-arch.md in full; cut line (lines 80-82) keeps the per-record flag pass; line 36 lists v1 lexicon category names",
   "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered'; exit 0",
   "grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches (the AC3 evidence count is not reproducible from the repo)",
   ".venv/bin/python -m pytest tests/unit -q -> 'no tests ran in 0.00s', exit 5 (tests/unit is empty)",
   ".venv/bin/python -m app.pipeline evals/golden/sample.txt -> 'No module named app.pipeline', exit 1 (CLI not built; not runnable at this commit)",
   "python3 tools/board.py validate -> 'ok (28 file(s))', exit 0",
   "python3 -I artifacts/review-evidence/T-028-review-checks.py -> SUMMARY: 8/12 checks passed, exit 1"
 ],
 "verdict": "fail",
 "scores": {"AC1_summary_drops_qualifier": 5, "AC2_lexicon_names_in_adr013": 4, "AC2_flag_template_per_category": 1, "AC3_confirm_date_phone_gap": 5, "AC3_date_invalid_only_noncandidate": 5, "AC3_mg_abbreviation_consistency": 2, "AC3_cut_line_per_record_pass": 5, "AC4_export_golden_reference": 3, "AC4_ai_line_matches_R-EX-4_1": 1, "AC4_d_ids_resolve": 5, "evidence_honesty": 2},
 "findings": [
  {"severity": "blocker",
   "title": "DECISIONS AI line is not the R-EX-4(1) fixed text, and ADR-009 says it is",
   "evidence": "memory/DECISIONS.md:204: 'beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`)'. spec/REQUIREMENTS.md:122 (R-EX-4(1)): 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' followed by 'Pending items: N.'. Repro: grep -c of the R-EX-4(1) sentence in memory/DECISIONS.md = 0. git show de749c2 -- memory/DECISIONS.md replaces the R-EX-4(1) text with the golden text (sample.export.expected.txt:51) and keeps the label 'fixed text of R-EX-4(1)'. Card AC4 evidence says 'AI line aligned to R-EX-4(1)'; that is false.",
   "why_it_matters": "The disclosure text is a fixed string the spec names as fixed. DECISIONS says it matches the spec when it does not, so the golden test and the spec will disagree on the first export pytest. The spec is also internally inconsistent: R-EX-4(1) (spec:122) differs from the spec section 6 worked example (spec:273) and the golden file, which section 8's authority rule prefers. The architect followed the authority rule silently and mislabelled the source. Recorded as blocker because the card's stated spec alignment is false and the spec row check (section 8 row 3) fails as written; severity drops to major if Chris rules the golden text canonical and the spec row is amended.",
   "fix": "Get Chris's ruling (questions_for_chris[0]). Then keep one string. If R-EX-4(1) wins: change DECISIONS.md:204, the ADR-009 text, LLM_VS_CODE.md:103, spec/REQUIREMENTS.md:273 and golden sample.export.expected.txt:51 (qa owns the golden). If the section 6 / golden text wins: amend R-EX-4(1) at spec/REQUIREMENTS.md:122 and remove 'the fixed text of R-EX-4(1)' from DECISIONS.md:204. Do not keep the label unless the strings are equal.",
   "acceptance_test": "artifacts/review-evidence/T-028-review-checks.py AC5 PASS; the chosen sentence appears identically in spec, DECISIONS, LLM_VS_CODE and the golden file (grep -c equal in each); an export test compares the internal-notes block to the golden block byte for byte."},
  {"severity": "major",
   "title": "api.md sentence array splits 'Rx cyclobenzaprine 10 mg.' at the abbreviation, contradicting R-TL-2, D-021 and ADR-016",
   "evidence": "memory/contracts/api.md:91: '{\"text\": \"Rx cyclobenzaprine 10 mg.\", \"start\": 477, \"end\": 502}, {\"text\": \"Follow up with PCP in 1 week.\", \"start\": 503, \"end\": 532}'. memory/DECISIONS.md:285 says this exact sentence is one unit. Repro: artifacts/review-evidence/T-028-review-checks.py AC4b: api.md span [(477,502),(503,532)] vs R-TL-2 splitter span [(477,532)] on evals/golden/sample.txt record 2. This is the T-014 r3 M4 finding, which the card closes but the file still contradicts.",
   "why_it_matters": "api.md records[].sentences is the unit list the excerpt editor builds on (ADR-016). An implementer who copies this array lets an excerpt end at 'mg.', a fragment, which breaks the whole-sentence rule (R-TL-2) and the 'hedge travels with its finding' rule. The card AC3 evidence 'mg. one unit [477,532)' is contradicted by the file it cites.",
   "fix": "Replace api.md:91 with one unit: {\"text\": \"Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.\", \"start\": 477, \"end\": 532}; keep the 533-552 unit. Generate the example from the splitter output rather than by hand.",
   "acceptance_test": "AC4b in T-028-review-checks.py passes; a unit test runs the real sentence splitter on evals/golden/sample.txt record 2 and asserts equality with the sentences array in api.md (the test reads the array from api.md, so the example cannot drift)."},
  {"severity": "major",
   "title": "'Each with a flag template' is asserted, not shown: ADR-013 has no per-category template and the template module does not exist",
   "evidence": "memory/DECISIONS.md:258: 'Every category has a code template and a flag_type.' memory/DECISIONS.md:259: 'renders title and explanation from a template per category (app/backend/flag_templates.py; a unit test asserts every category has one), for example \"Wording that could be used to question causation...\"'. Only one template is worded. Repro: T-028-review-checks.py AC2b: 0 of 13 lexicon categories have template text in ADR-013. ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty.",
   "why_it_matters": "The 'every flag is code-rendered from a fixed template' rule (docs/LLM_VS_CODE.md row 14) is the control that stops the model writing causation wording. Categories such as recovery_context (strength low, never raises) and the lexicon-only categories have no wording anywhere in the design, so the backend would invent it. A generic sentence is not a template, and the card's 'each with a flag template' is not supported by the ADR.",
   "fix": "Add a table to ADR-013 with one template per category: the 13 lexicon categories plus the conflict, gap and record_warning codes it lists. Or check in app/backend/flag_templates.py as a key list equal to the closed category list and cite that file.",
   "acceptance_test": "T-028-review-checks.py AC2b reports 13 of 13 lexicon categories with explicit template text (or the template file's key set equals the closed list); a unit test asserts it."},
  {"severity": "major",
   "title": "Spec section 8 row 1 check cannot pass: the api.md export example abbreviates the notes block",
   "evidence": "spec/REQUIREMENTS.md:362-371 section 8 row 1: 'internal_notes_text should equal the golden notes block' with check 'diff of the example against evals/golden/sample.export.expected.txt (expect none)'. memory/contracts/api.md:272: '\"internal_notes_text\": \"INTERNAL REVIEW NOTES — DO NOT SEND\\n\\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]\"'. Repro: T-028-review-checks.py SPEC-8.1 FAIL.",
   "why_it_matters": "Replacing the copy with a pointer (card AC4) is the right call, and T-014 r3 m1 recommended it. But the spec row still demands an empty diff, so the spec and the card now disagree on how this is verified, and a reviewer following the spec will fail the doc. The choice has not been recorded in an ADR.",
   "fix": "Either amend spec section 8 row 1 to 'the example names the golden file; a pytest compares real export output with it' and record that in ADR-009, or embed the full block. Make the spec row and the example agree.",
   "acceptance_test": "The spec row's check command and the api.md example describe the same verification; a pytest asserts real export output equals evals/golden/sample.export.expected.txt."},
  {"severity": "minor",
   "title": "README-arch lexicon line lists v1 category names that lexicon v2 does not contain",
   "evidence": "app/README-arch.md:36: 'lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection'. Lexicon v2 entries[].category (13 names, yaml load) contains none of causation_weakening, compliance or hedge; accident_date_phrases, damages, non_encounter and injection are code_lists keys.",
   "why_it_matters": "A backend worker reading the architecture map would look for categories that do not exist. ADR-013 maps causation_weakening and compliance to causation; the README does not say so.",
   "fix": "Rewrite README-arch.md:36 as the 13 v2 category names plus the 4 code_lists keys, with a pointer to ADR-013.",
   "acceptance_test": "A grep or unit test: every name on README-arch.md:36 is in lexicon v2 categories or code_lists keys."},
  {"severity": "minor",
   "title": "confirm_date example clears a date_ambiguous warning that the golden case does not expect",
   "evidence": "memory/contracts/api.md:209: '\"removed_flag_ids\": [\"f_warn_date_r8\"]'. evals/golden/case_01_date_formats.expected.json: \"record_warnings\": [], \"flags\": [], \"gap_excluded_records\": [8]. Golden description: 'Ambiguous date must be marked ambiguous and surfaced for review.' evals/golden/README.md:61 record_warnings schema lists only instruction_like_text.",
   "why_it_matters": "The gap example is correct (gap_flags [] matches D-003 and golden). But the example refers to a warning the golden never expects, so either the golden is missing the date_ambiguous expectation or the example names a flag the pipeline is not required to create. Golden is the stated authority for expected outputs (spec section 8).",
   "fix": "qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden, or the architect rewrites the example to 'removed_flag_ids: [] (no warning in golden)' and records which one wins.",
   "acceptance_test": "check_golden.py asserts a date_ambiguous warning for case_01 record 8 (or the api example has no removed id not present in the golden)."},
  {"severity": "minor",
   "title": "AC3 evidence cites a count that no checked-in script produces",
   "evidence": "Card T-028 AC3 evidence: 'check script 14/14 blocks, 17/17 offsets'. Repro: grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches. The offsets themselves verify (sample.txt positions 396, 477, 503, 533 match api.md), but nothing prints the counts.",
   "why_it_matters": "A count with no script cannot be re-run by the next reviewer. The same claim covers the mg. offsets, which are wrong (finding 2).",
   "fix": "Check the offset and block script into artifacts/review-evidence/ and quote its output in the card; use the output, not a hand count.",
   "acceptance_test": "python3 -I artifacts/review-evidence/<script>.py exits 0 and prints the counts quoted in the card."},
  {"severity": "nit",
   "title": "AC4 evidence 'D-001..D-024 in all three docs' overstates the citations",
   "evidence": "Distinct D-ids: memory/DECISIONS.md 22 (no D-016, no D-023); memory/contracts/api.md 8 (D-001 D-003 D-010 D-012 D-013 D-020 D-022 D-024); docs/LLM_VS_CODE.md 2 (D-001, D-024). Every cited id resolves (T-028-review-checks.py AC8 PASS).",
   "why_it_matters": "The substance passes; the evidence sentence does not describe the files.",
   "fix": "Restate the evidence as 'every cited D-id resolves to a row in ORCHESTRATOR_DECISIONS (D-001..D-024)'.",
   "acceptance_test": "T-028-review-checks.py AC8 PASS (already true)."}
 ],
 "whats_right": [
   "SUMMARY_DROPS_QUALIFIER is present and consistent: api.md 1, DECISIONS.md 3, LLM_VS_CODE.md 1, matching R-TL-10(b) and D-022.",
   "ADR-013 names all 13 lexicon v2 categories, and the confirm_date example's gap_flags [] matches golden gap_excluded_records [8] and D-003 (phone note, not in gap math).",
   "The README-arch cut line keeps the per-record flag pass (README-arch.md:82), and money stays integer cents with the $185 rate outside the 839000 total (api.md:6, 124, 135)."
 ],
 "questions_for_chris": [
   "Which AI disclosure line is canonical: R-EX-4(1) ('AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' + 'Pending items: N.') or the section 6 / golden line ('This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.')? The spec currently has both.",
   "Should api.md embed the notes block (spec section 8 row 1 says diff expect none) or point to the golden file (card AC4 chose a pointer)?",
   "D-024 puts Tier-1 card reviews on sonnet. This review ran as claude-haiku-5-5. Accept it for mechanical doc passes, or re-run on sonnet?"
 ]}
```
