# T-013 review, round 2 — product-manager-reviewer

**Verdict: changes** (0 blockers, 5 majors, 5 minors, 1 nit).

Round 2 is a real improvement. The paralegal's blocker is fixed: flags now go only into a separate internal-notes block. That block has its own copy button, a worked template (§6) and a "no flag text" E2E. Of the 15 round-1 blocker and major findings, 13 are resolved and 2 are partially resolved. The full trace is in `artifacts/review-evidence/T-013-trace.md` under "Round 2". R-IDs are now 61, with no dangling references, and 7 of 10 re-sampled R-IDs are cleanly decidable (round 1: 5 of 10).

The card does not pass. Five problems remain, and each would be built into M2/M3 cards by T-017:
1. R-IN-5 ("confirm a date") contradicts R-RV-2 ("date not editable, 422"). The API has no other way to set a date.
2. Scope grew by 14 R-IDs. Three of them, none required by Appendix A, each need a new endpoint or an ADR change and create most of the architect conflicts. They should be non-goals.
3. R-TL-8, the hedge rule that partly fixes the paralegal's major, keys on a lexicon `hedge` category that does not exist.
4. R-EX-1's "no flag text" test bans record words that no rule keeps out of entry excerpts. Flag evidence can still reach the letter that way.
5. §8 is not a clean hand-off. The orchestrator decisions it relies on are recorded nowhere, no card owns the reconciliation, and the conflict list is incomplete.

Exercised:
- `board.py show T-013`, `git log`, `git diff --stat` (working tree clean at 64f766e).
- Read REQUIREMENTS.md end to end, both round-1 reviews (parsed their JSON), api.md, ADR-005 and ADR-009, LLM_VS_CODE.md, CONTRACT §5 M2/M3 and "What we evaluate", SCOPE_CUTS and ASSUMPTIONS.
- Scripted R-ID inventory and dangling-reference check.
- Checked every golden-case fact the tests cite with a Python script.
- Grepped lexicon.yaml for `hedge`, and searched for the recorded "orchestrator decisions 1-10".
- Re-sampled 10 R-IDs with seed 1302.

```json
{"card": "T-013", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md at 64f766e (diff 65894f6..64f766e; working tree clean) against spec/SPEC.md Appendix A Part 1, docs/CONTRACT.md §5 M2/M3 and §8.2, memory/contracts/api.md, memory/DECISIONS.md ADR-005/009, evals/golden/*, app/llm/lexicon.yaml; round-1 reviews reviews/T-013-product-manager.md and reviews/T-013-paralegal.md; no app (M1)",
 "exercised": [
  "python3 tools/board.py show T-013 -> in_review, commits [65894f6, 64f766e]",
  "git log --oneline -8; git diff --stat 65894f6..64f766e; git diff --stat 64f766e -- spec/REQUIREMENTS.md -> empty",
  "Read spec/REQUIREMENTS.md lines 1-329 in full",
  "python3 parse of the JSON blocks in both round-1 reviews; listed every blocker/major/minor",
  "R-ID inventory script: 61 defined, 0 referenced-but-undefined, 0 duplicates",
  "python3 script over evals/golden/*.expected.json: case_01 rec 8 ambiguous + 40-day gap; case_02 3 flags/4 near-misses; case_03 unclear values; case_04 6->4 entries; case_06 28-day; case_07 total 420; sample must_not M1-M13; flag type vocabulary; provider_aliases",
  "grep -n hedge app/llm/lexicon.yaml; read lexicon.yaml:19 flag_types and the may_represent entry",
  "grep api.md for edit/bulk/cite rules (lines 150, 175, 179, 187, 190, 193, 235); read DECISIONS.md ADR-005 (137-149) and ADR-009 (182-188)",
  "grep -rn 'decisions 1-10|orchestrator decision' across *.md/*.jsonl -> only the writer's note",
  "Read board cards T-016..T-021 titles/status and T-017 AC",
  "Read CONTRACT §5 M2/M3 (300-310) and 'What we evaluate' (513-522)",
  "Read memory/SCOPE_CUTS.md and memory/ASSUMPTIONS.md A-104..A-108",
  "random.seed(1302) sample of 10 R-IDs, judged for decidability (7 clean, 2 partial, 1 contradictory)",
  "Appended the Round 2 resolution table to artifacts/review-evidence/T-013-trace.md"
 ],
 "verdict": "changes",
 "scores": {"traceability": 5, "test_decidability": 3, "stretch_rationale": 5, "cut_rule": 4, "non_goals": 4, "ship_bar_fidelity": 5, "workflow_fit": 4, "architect_handoff": 2},
 "findings": [
  {"severity": "major", "title": "R-IN-5 'confirm a date' contradicts R-RV-2 'date not editable'; no action exists to confirm an ambiguous date",
   "evidence": "REQ:37 R-IN-5 'When she confirms a date it joins the timeline and gap math re-runs'; test 'after confirming 2026-05-04'. REQ:88 R-RV-2 'Date, provider and excerpt are not editable' and 'UT: attempts to edit date ... -> 422'. memory/contracts/api.md:175 and 179: the only date path is `{\"action\":\"edit\",\"edits\":{\"date\":...}}`. api.md:235 DATE_AMBIGUOUS 'excluded from gap math until set'. REQ:320 §8 asks the architect to remove entry date editing, which would leave R-IN-5 with no mechanism at all. The sample re-draw hit R-IN-5 and judged it undecidable.",
   "why_it_matters": "Ambiguous dates are a must-have path, golden case_01 record 8. A backend worker cannot satisfy both R-IN-5 and R-RV-2's 422 unit test, so whichever one is built, the other fails.",
   "fix": "Define a separate review action, e.g. `confirm_date`, that is valid only for entries in DATE_AMBIGUOUS or DATE_MISSING state. The date must be one of the code-parsed readings (04/05 means April 5 or May 4) or a typed valid ISO date. Log it as a review event. Keep general date edits forbidden. Add it to R-RV-2's per-type table and to the §8 conflict list for api.md.",
   "acceptance_test": "REQ names the confirm-date action and its allowed values. R-RV-2's UT says 'edit date -> 422; confirm_date on a non-ambiguous entry -> 422; confirm_date on case_01 record 8 with 2026-05-04 -> 200 and a 40-day gap flag'."},
  {"severity": "major", "title": "Scope grew 47 -> 61 R-IDs; three add-ons not required by Appendix A should move to non-goals",
   "evidence": "SPEC:41 requires 'accept, edit or dismiss each entry and each flag'. Charges are not in the edit requirement, and batch accept and duplicate splitting are not mentioned. REQ:79 R-CH-7 (charge reclassification + judge #2 re-run + confirm; 'Writer's proposal; architect to confirm'). REQ:93 R-RV-7 (batch accept; 'Needs an ADR-005 amendment: today's api.md has no bulk endpoint'). REQ:78 R-CH-6 'A \"not a duplicate\" action splits them and is logged' (new action; no golden case has duplicate charges, and case_04 is 'no amounts'). CONTRACT:306 M3 budget is <= 3.5 h for the whole UI, export and E2E. Together these three supply 3 of the 4 §8 conflict bullets (REQ:320-322).",
   "why_it_matters": "'Builder mindset: you ship something real and cut scope on purpose' (CONTRACT:515). Each add-on needs a new endpoint or ADR change, more UI, and its own E2E. They compete with must-haves for M3's 3.5 h, and the reviewer of the product note will see requirements we chose to carry rather than cut.",
   "fix": "Move to §5 non-goals and SCOPE_CUTS: (a) charge reclassification. Charges become {accept, dismiss}, the class is code + judge #2, and the R-RV-1 charge cells drop 'edit'. This is also safer: no path turns the $185 rate into a totaled charge. (b) Batch accept: per-item keyboard accept (R-RV-4) is enough for about 10 records, and widening non-goal 14 to all batch accept respects ADR-005's 'Amounts and dates always need an explicit accept'. (c) The duplicate-charge split action: keep the code merge and its visible 'duplicate of' note. Keep R-CH-6's merge and R-TL-7.",
   "acceptance_test": "R-CH-7 and R-RV-7 are removed or rewritten as non-goals. R-CH-6 has no split action. R-RV-1's charge cells are {accept, dismiss}. §8 no longer lists the bulk-endpoint or charge-edit conflicts. SCOPE_CUTS has rows for all three."},
  {"severity": "major", "title": "R-TL-8 (hedge travels with finding) keys on a lexicon 'hedge' category that does not exist; the record-6 assertion has no rule behind it",
   "evidence": "REQ:52 'a sentence matching the `hedge` category of `app/llm/lexicon.yaml`'. lexicon.yaml:19 `flag_types: [pre_existing, causation_weakening, compliance]`. `grep -n hedge app/llm/lexicon.yaml` finds the word only inside rationale/false_positive prose (lines 286, 288, 300, 314, 325). REQ:52's test asserts 'entry 6 excerpt contains `after two missed appointments`'. That sentence is lexicon `compliance` (lexicon.yaml:572, 599), not a hedge, so the stated rule would not require it. REQ:46 R-TL-2 'complete sentences' has no boundary definition, and the sample text contains 'approx.', 'Dr.', 'C/O' and 'Dx:'.",
   "why_it_matters": "This is the fix for the paralegal's round-1 major (a quote misleads by omission). As written, two implementers will pick different sentence sets, and the entry-6 golden assertion can fail on an output that follows the rule.",
   "fix": "Name the trigger concretely. Either (a) ask the researcher to add a `hedge: true` tag to named lexicon entries (may_represent, correlate_clinically, and the others) and cite those IDs, or (b) say 'any lexicon entry with flag_type causation_weakening or compliance in the same record'. Make the entry-6 assertion follow from that rule. Define 'sentence' (split on '.', '?', '!' followed by space+capital or end; known abbreviations list) or point to the splitter's unit test.",
   "acceptance_test": "Every identifier REQ cites in lexicon.yaml exists (grep). Both golden assertions in R-TL-8 are implied by the rule text. R-TL-2 names the sentence-boundary rule or its unit test."},
  {"severity": "major", "title": "R-EX-1 'no flag text' test bans record words that no rule keeps out of entry excerpts; flag evidence can still reach the letter via excerpts",
   "evidence": "REQ:103 asserts that `letter_text` contains none of \"low back pain\", \"intake form\", \"2026-01-19\". But sample record 3 is 'Persistent neck pain 6/10, daily headaches. Refer to physical therapy ... Patient reports low back pain in 2023, resolved.', and R-TL-2 (REQ:46) lets the generator pick 'one or more complete sentences'. A verified entry-3 excerpt of all three sentences passes every grounding rule and fails R-EX-1. The same holds for record 7's 'Date of accident per intake form: 2026-01-19.' Meanwhile R-TL-8 (REQ:52) forces 'may represent degenerative change; correlate clinically' (golden flag P2/K1 evidence) into the letter, and §6 REQ:225 shows it there. The §6 worked example avoids the banned sentences only because the writer chose excerpts by hand.",
   "why_it_matters": "This is the paralegal's round-1 blocker by another route. Whether a prior-condition or wrong-date sentence reaches the carrier now depends on which sentences the model quotes. The test treats that as a failure, but no requirement tells the generator or code to avoid it, so the test is not decidable from the rules.",
   "fix": "Pick one rule and state it. (a) Excerpt selection: an entry excerpt quotes the encounter's findings, treatment and plan. A sentence whose only role is flag evidence (prior condition, body-date conflict) is left out of the entry excerpt, except that R-TL-8 qualifiers always stay. Code enforces this from flag evidence offsets. Or (b) record sentences may appear verbatim in excerpts: drop the record-word strings from R-EX-1 and assert only flag labels, titles and explanations. Record the choice as an assumption; it depends on the paralegal's open question to Chris.",
   "acceptance_test": "R-EX-1's negative-string list follows from a written rule. A seeded entry-3 excerpt with all three sentences either becomes needs_review under rule (a) or passes R-EX-1 under rule (b), never both."},
  {"severity": "major", "title": "§8 'Design conflicts' is not a clean hand-off: the governing decisions are unrecorded, no card owns reconciliation, and the list is incomplete",
   "evidence": "REQ:319 'These requirements follow the orchestrator's round-2 decisions'. `grep -rn 'decisions 1-10|orchestrator decision'` finds only the writer's note (board/cards/T-013.md:55; board/activity.jsonl:185). Nothing is in DECISIONS, STATE or ASSUMPTIONS. DECISIONS.md:1 says 'architect is the sole writer'. ADR-005 (DECISIONS:145) and ADR-009 (DECISIONS:185) still contradict R-RV-2, R-RV-7 and R-EX-4/8, and REQ:309 asks the orchestrator to update A-106. No card in T-016..T-021 owns the reconciliation, and T-017's AC covers only R-ID and LLM-table coverage. Missing from the list: (1) R-IN-5 vs removing date edits (api.md:179); (2) flag-type vocabulary: REQ/api `prior_condition` vs golden `pre_existing` vs lexicon `pre_existing`/`causation_weakening`/`compliance`; (3) golden provider_aliases 'Capital Physical Therapy' and 'Central Emergency Room' vs R-TL-9; (4) api.md:193 example letter in MM/DD/YYYY with 'MEDICAL CHARGES' / 'Total of charges listed' vs R-EX-6/R-EX-8; (5) ADR-005 'Amounts and dates always need an explicit accept' vs batch-accepting dated entries; (6) R-CH-7 marked 'architect to confirm' in a must-have table.",
   "why_it_matters": "M2/M3 workers implement against api.md and the ADRs. When those disagree with REQUIREMENTS and the tie-breaker is an unrecorded conversation, each worker resolves the conflict differently, and the gate panels then review against two specs. 'Decisions made under ambiguity, explained plainly' (CONTRACT:521) needs the decision written where the builder reads it.",
   "fix": "Before T-017 plans cards, have the orchestrator record decisions 1-10 (STATE or a DECISIONS proposal). Then open one architect card that amends ADR-005/ADR-009/api.md item by item, using the completed list (including the six above, plus qa items for the golden vocabulary and aliases and for sample.export.expected.txt), and list it in T-017's depends_on. If the scope cuts in the previous finding land, R-RV-7 and R-CH-7 drop off the list.",
   "acceptance_test": "Every §8 bullet names an owning card ID and the recorded decision it follows. `grep` finds no contrary text left in api.md/ADR-005/ADR-009 once that card closes. Golden flag types equal the REQ/api types."},
  {"severity": "minor", "title": "R-EX-6 byte-for-byte golden includes LLM-written summaries but names no backend; the golden file has no owning card",
   "evidence": "REQ:108 '`letter_text` equals the golden file byte for byte' for a block that contains generator summaries. REQ:125 R-CO-7 'Summary wording may differ'. `ls evals/golden/` shows no sample.export.expected.txt, and the 'qa card' is unnamed.",
   "why_it_matters": "On a live backend the test fails whenever summary wording differs, which R-CO-7 allows, so the template check would report false failures.",
   "fix": "State 'on the `fixture` backend (recorded sample responses)', and name the qa card that writes the golden file.",
   "acceptance_test": "R-EX-6 names the backend; a board card exists whose AC creates evals/golden/sample.export.expected.txt."},
  {"severity": "minor", "title": "R-FL-4 says record 7 'must' raise causation flags; the golden marks them 'should' and credits them via G1/C1",
   "evidence": "REQ:64 'Sample must raise records 8, 6, 9, 7 (\"New onset\" after the 73-day gap; wrong accident date)'. sample.expected.json K4 and K5 have `level: should`, and K4's summary says 'credit if surfaced either here or on G1'.",
   "why_it_matters": "The eval and the requirement give different pass results for the same output, and flag recall per type is a ship-bar number.",
   "fix": "Align them: either REQ says 'should (credited via G1/C1)', or qa raises K4 and K5 to must.",
   "acceptance_test": "The R-FL-4 wording and the golden `level` for the record-7 flags agree."},
  {"severity": "minor", "title": "Golden provider aliases accept non-verbatim names that R-TL-9 rejects",
   "evidence": "sample.expected.json E4 provider_aliases contains 'Capital Physical Therapy' and E2 contains 'Central Emergency Room'. REQ:53 R-TL-9 says 'Capital Physical Therapy, LLC' -> rejected.",
   "why_it_matters": "The recall eval would treat as acceptable a provider name that the grounding rule rejects.",
   "fix": "qa removes the non-verbatim aliases, or R-TL-9 states that the aliases are for matching only.",
   "acceptance_test": "Every golden provider alias is a substring of its record's Source line after normalization."},
  {"severity": "minor", "title": "Ship-bar row 5 score key is not yet in the paralegal brief or agent",
   "evidence": "REQ:289 `scores.verify_quickly` '(named in the paralegal reviewer brief)'. `grep verify_quickly .claude/agents/paralegal-reviewer.md personas/paralegal.md` finds nothing. The round-1 paralegal review emitted `verifiability_of_every_claim`.",
   "why_it_matters": "If the key is missing, the ship-bar number cannot be read mechanically at the M3 gate.",
   "fix": "The orchestrator adds the key to the M3 paralegal brief template, or REQ adopts the key the persona already emits.",
   "acceptance_test": "The paralegal's M3 review JSON contains the key named in REQ:289."},
  {"severity": "minor", "title": "R-CO-8 currently fails: non-goals 12 and 14 are not in SCOPE_CUTS",
   "evidence": "REQ:180 and 182 (non-goals 12, 14). memory/SCOPE_CUTS.md has rows 1-13, where row 12 = manual add and row 13 = LLM split fallback. Bates and the batch limit are absent, and SCOPE_CUTS 13 has no counterpart in REQ §5.",
   "why_it_matters": "'Say what was cut' must match between the product note, REQ §5 and SCOPE_CUTS.",
   "fix": "The orchestrator logs NG12 and NG14, plus the cuts recommended above; the writer adds SCOPE_CUTS 13 to §5.",
   "acceptance_test": "Every REQ §5 non-goal has a SCOPE_CUTS row, and the reverse."},
  {"severity": "nit", "title": "Flag dismissal reason and edit-note text have no length or content rule",
   "evidence": "REQ:88 'Flag: a reviewer note only'; REQ:91 'optional reason'. Both print into internal notes (REQ:106).",
   "why_it_matters": "Low risk: internal-only free text.",
   "fix": "Optional: cap length and print it verbatim, labeled 'reviewer note'.",
   "acceptance_test": "n/a"}
 ],
 "whats_right": [
  "Two-block export with no-flags-in-letter E2E, a flags-free letter builder signature, and a worked §6 example: this closes the round-1 blocker; do not merge the blocks back.",
  "R-TL-3's record-7 seeded test, R-TL-9 provider grounding, and R-EX-8's exact total string with the PT exclusion are concrete and match the sample-case truths.",
  "The stretch cut rule now fits inside M3 with one fallback, and the full-record modal (R-RV-9) is core, so cutting the stretch costs no verifiability."
 ],
 "questions_for_chris": [
  "May a demand-letter treatment section quote record sentences that are also flag evidence (e.g. 'Patient reports low back pain in 2023, resolved.' or the MRI hedge), or should the entry quote leave them out and leave them to the attorney's notes? This decides R-EX-1/R-TL-8 (finding 4) and echoes the paralegal's round-1 question."
 ]}
```
