# T-013 review, round 3 (final) — paralegal-reviewer

**Verdict: changes** (0 blockers, 2 majors, 4 minors, 1 nit).

**r2 status.**
- Both r2 majors are resolved:
  - The letter now holds no tool-authored flag content.
  - A "flagged language quoted in the letter" notes section exists.
  - The excerpt can be re-selected as whole sentences, and hedge sentences can't be dropped.
  - R-TL-8 names five lexicon ids, and all five exist.
- Of my 6 r2 minors, 5 are resolved. The ambiguous-date one is declined as non-goal 18 with a stated reason, which I accept.
- The nit is resolved, but my own acceptance test for it over-reaches (see the new minor below).
- Table: `artifacts/review-evidence/T-013-r3-resolution.md`.

**Re-walk by script** (`artifacts/review-evidence/T-013-r3-paralegal-walk.py` → `…-walk.out.txt`; `…-golden-cmp.py` → `…-golden-cmp.out.txt`):
- All 11 letter quotes and all 17 notes quotes are verbatim in `sample.txt`.
- All 9 headings equal the header label exactly, with the header date, in order.
- R-TL-10: no summary contains a number missing from its excerpt, label or date.
- The charges add to $8,390, and the total line matches R-EX-8 exactly.
- No tool-authored flag content is in the letter. The only "record" word is the attribution "the record states" in entry 8, which is correct.
- The notes have all 11 sections in R-EX-4 order. They include the $185 "Request itemized PT ledger", the lost-work mention, and the ESI with "Request cost estimate".
- Every notes citation reads (label as written, Month D, YYYY) and matches the sample.
- The golden `sample.export.expected.txt` equals §6 byte for byte, so the golden file carries the two inconsistencies below.

**Would I paste the treatment section into a demand?** Yes, after filling in the Ex/Bates placeholders.
- Dates are long-form, providers are as written, and every line has a verbatim quote.
- Self-report stays attributed, and the hedge is quoted with the finding.
- The total is neutral. There is no "verified" label, no markdown and no dot leaders.

What I would *not* do is paste it without first deciding about entries 6, 7 and 8 with my attorney. Right now the spec only tells me after export that those quotes carry flagged language (major 2).

**Majors**
1. **The accident-date conflict cites only one side.**
   - The C1 line in the notes gives record 7's excerpt. For records 1 and 2 it uses tool wording ("show treatment on that date") with no quote.
   - The golden C1 evidence on record 1 is "rear-ended at approx. 35 mph". That sentence is in the letter, so by R-EX-4(4)'s own rule entry 1 belongs under "flagged language quoted in the letter". The example, the test text and the golden file list only 4, 6, 7, 8 and 9.
2. **D-016 to D-018 are not cited, and D-017's "adverse facts are never auto-included in the letter" is not reconciled.**
   - Entry 6's default excerpt is required to contain "Discharged from PT after two missed appointments".
   - Accepting the entry puts that sentence in the letter.
   - Nothing on the review screen tells me, at the moment I accept, that the quote carries flagged language. The notes tell the attorney only after export.

Exercised: listed in the JSON. This is a document and fixture review: there is no app for this card.

```json
{"card": "T-013", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md @ b4f3924 (diff 64f766e..b4f3924, 160+/104-); against evals/golden/sample.txt, sample.expected.json, sample.export.expected.txt (3c5eb7c), app/llm/lexicon.yaml, memory/ORCHESTRATOR_DECISIONS.md D-001..D-018, reviews/T-013-paralegal-r2.md; no app URL (requirements card)",
 "exercised": [
  "python3 tools/board.py show T-013 -> status in_review, rounds 2, commits [65894f6, 64f766e, 4191140, b4f3924], AC 1-4 done",
  "git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md -> 1 file changed, 160 insertions(+), 104 deletions(-)",
  "read spec/REQUIREMENTS.md:1-385 in full; memory/ORCHESTRATOR_DECISIONS.md D-001..D-018; reviews/T-013-paralegal-r2.md",
  ".venv/bin/python artifacts/review-evidence/T-013-r3-paralegal-walk.py -> T-013-r3-paralegal-walk.out.txt: [1] letter 11/11, notes 17/17 quotes verbatim; [2] 9/9 provider_equals_label, date_ok, order_ok; [3] extra_numbers=[] for all 9; [4] sum=8390, total line equals R-EX-8 string True, '..' False, 'all amounts $x.xx' False; [5] only 'record ' (entry 8 'the record states'); [6] rule gives records [1,4,6,7,8,9], §6 lists [4,6,7,8,9]; [7] all notes citations match; [8] C1 line: rec 1 'rear-ended at approx. 35 mph' in_line=False, rec 7 True; [9] 12 section markers present and in order; [10] bills rule ['Austin EMS run report','Dr. Alvarez','Capital PT','Hill Country Pain Management'] vs example 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).'; [13] gaps [0,7,7,28,14,73,11,14]",
  ".venv/bin/python artifacts/review-evidence/T-013-r3-paralegal-golden-cmp.py -> golden letter == §6 block 1 True; golden notes == §6 block 2 True; spec lines citing D-016/17/18: []; 'adverse|auto-includ': []; lexicon 'hedge:' key False; 5 R-TL-8 hedge ids all present",
  "read evals/golden/sample.export.expected.txt:1-90",
  "hand read of §6 Block 1 as a demand-letter treatment-section paste and Block 2 as attorney notes against persona checklist items 1-23",
  "wrote artifacts/review-evidence/T-013-r3-resolution.md (r2 finding -> r3 status)"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "verifiability_of_every_claim": 4, "workflow_fit": 4, "export_usability_in_demand_letter": 5, "adjuster_safety": 4, "charges_handling": 5, "flag_coverage_vs_truths": 4},
 "findings": [
  {"severity": "major",
   "title": "The accident-date conflict cites only one side in the notes, and the 'flagged language quoted in the letter' rule contradicts its own example on entry 1",
   "evidence": "spec/REQUIREMENTS.md:272 '- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (...): \"Date of accident per intake form: 2026-01-19.\"' Golden C1 evidence includes (1, 'rear-ended at approx. 35 mph'), and walk [8] shows in_line=False. R-FL-2 :66 says 'citing both excerpts'. R-EX-4(4) :122 says 'each letter entry whose excerpt contains the evidence of a flag that is not dismissed'. Walk [6]: the rule gives records [1,4,6,7,8,9]. The §6 notes :281-285, the R-EX-4 test ('entries 4, 6, 7, 8, 9') and the golden sample.export.expected.txt:65-69 list [4,6,7,8,9].",
   "why_it_matters": "The 01/09 vs 01/19 conflict is the first thing the adjuster raises. Checklist item 7 requires both excerpts so the attorney sees what each record says without opening it. 'Show treatment on that date' is tool wording, not the record's words. It says nothing about why 01/09 is the accident date, which is the EMS 'rear-ended' line. Second problem: an implementer can't satisfy both the R-EX-4(4) rule and its test, and qa has already frozen the test's side into the golden file.",
   "fix": "C1 notes line: 'Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) \"41M restrained driver, rear-ended at approx. 35 mph.\"; record 2 (Central ER discharge summary, January 9, 2026) [header date]; record 7 (...) \"Date of accident per intake form: 2026-01-19.\"' Do not choose between the dates (D-017). Then either add 'Record 1 (...): \"...rear-ended at approx. 35 mph...\" Conflict, accident date.' to the flagged-language list, or narrow the rule to 'evidence on the side of the flag that weakens the claim' and say how code knows which side that is. Update the R-EX-4 test text and ask qa to regenerate the golden file.",
   "acceptance_test": "UT on the §6 scenario: the C1 line in internal_notes_text contains 'rear-ended at approx. 35 mph' and 'Date of accident per intake form: 2026-01-19', and neither date is labelled as correct. UT: the set of records under FLAGGED LANGUAGE equals the set computed by the R-EX-4(4) rule from sample.expected.json flags; golden file regenerated."},
  {"severity": "major",
   "title": "D-016 to D-018 are not cited; D-017 ('adverse facts are never auto-included in the letter') is not reconciled with default excerpts that carry adverse sentences, and the paralegal isn't shown this at accept time",
   "evidence": "spec/REQUIREMENTS.md:4 'Binding product decisions: ... (D-001 to D-015)'. golden-cmp [14]: lines citing D-016/17/18 = []; 'adverse|auto-includ' = []. ORCHESTRATOR_DECISIONS D-017: 'Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides.' R-TL-8 :55 says 'Entry 6 ... default excerpt is checked by entry_recall (must_contain_excerpt: \"Discharged from PT after two missed appointments\")'. §6 letter :238 quotes it. The only place that discloses this is R-EX-4(4), which is in the export notes; R-RV-1/R-RV-2/R-TL-5 :92-93, :52 have no per-entry marker.",
   "why_it_matters": "When I accept entry 6, I'm checking that the date, provider and quote match the record, not deciding to tell the carrier about missed appointments. Under this spec the model's default excerpt puts that sentence into the letter. I learn it was flagged language only from the notes, after I've copied the letter. That is the 'adjuster quotes our own letter back at us' day. D-017 says the attorney decides, but nothing makes that decision happen before the paste.",
   "fix": "Cite D-016 to D-018 in the header and wherever they apply. Add an R-RV requirement: any entry whose excerpt contains the evidence of a non-dismissed flag shows 'Quotes flagged language: <flag type(s)>' on its row and in its accept control, and the accept is logged as including it. Alternatively, have the default excerpt omit non-hedge flagged sentences (compliance, pre_existing) and let her add them, then change the entry-6 golden must_contain_excerpt to match. Whichever path is chosen, state how it satisfies D-017.",
   "acceptance_test": "E2E: on the sample, entries 1, 4, 6, 7, 8 and 9 show the 'Quotes flagged language' marker before accept, and entries 2, 3 and 5 do not. Grep: spec/REQUIREMENTS.md cites D-017 on the R-ID that implements it."},
  {"severity": "minor",
   "title": "BILLS TO REQUEST: the rule, the example and the test name the providers three different ways",
   "evidence": "R-EX-4(8) :122 'providers (the label up to the first comma)'. The test text says 'Austin EMS, Dr. Alvarez, Hill Country Pain Management and Capital PT'. The example :297 and golden :81 say 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).' Walk [10]: the rule gives ['Austin EMS run report','Dr. Alvarez','Capital PT','Hill Country Pain Management'] in record order.",
   "why_it_matters": "This is the list I turn into records-request letters. If the code follows the rule, it fails the golden file. If it follows the golden file, the rule is wrong. Neither the order nor the '(itemized ledger)' suffix is specified.",
   "fix": "Pick one. Example: the label up to the first comma, in first-appearance date order, with ' (itemized ledger)' appended when an accepted rate exists for that provider. Make the example, the test text and the golden file match.",
   "acceptance_test": "UT: the BILLS TO REQUEST line built from the sample equals the golden line, and the golden line equals the rule's output."},
  {"severity": "minor",
   "title": "The fixed AI-assistance sentence says 'every item was reviewed', but Copy is allowed with items pending",
   "evidence": "§6 :267 'every item was reviewed by the paralegal before export.' R-EX-5 :123 lets Copy proceed after one confirm when items are pending. R-EX-4(11) lists pending items in the same block.",
   "why_it_matters": "If I copy with the gap flag pending, the attorney's notes say every item was reviewed and then list an unreviewed one. That is a false statement about my work, in the document the attorney relies on.",
   "fix": "'...drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.'",
   "acceptance_test": "UT: with one flag pending, internal_notes_text does not contain 'every item was reviewed' and contains 'Items not reviewed: 1'."},
  {"severity": "minor",
   "title": "R-EX-6 money-format test fails on the verbatim quotes it requires; R-TL-8 lists hedge ids where D-018 specifies a lexicon `hedge` boolean",
   "evidence": "R-EX-6 :124 'every amount matches `\\$[\\d,]+\\.\\d{2}`'. The golden Source quotes read '\"ER charges: $6,240.\"' and '\"Charge: $2,150.\"' (walk [4] 'all amounts $x.xx: False'). This is my own r2 test wording. D-018 says entries carry 'booleans `hedge` and `self_report`'; R-TL-8 :55 lists 5 ids, and the lexicon has no hedge key yet (golden-cmp [15]).",
   "why_it_matters": "A literal implementation of the test would 'fix' verbatim quotes into $6,240.00, and that breaks grounding. With hedge ids listed in the spec and a hedge flag in the lexicon, the two lists can drift apart once T-009 lands, and then a new hedge term could be cut from an excerpt.",
   "fix": "Change the R-EX-6 test to 'every amount line and the total line match \\$[\\d,]+\\.\\d{2}; Source quotes are verbatim'. Change R-TL-8(b) to 'lexicon entries with hedge: true (D-018); today: <5 ids>'.",
   "acceptance_test": "UT passes on the golden file as written. UT: the hedge set equals {e.id for e in lexicon if e.hedge} once the key exists."},
  {"severity": "minor",
   "title": "Future-treatment trigger is the single word 'recommend'",
   "evidence": "R-EX-4(7) :122 'from sentences containing \"recommend\" (a code pattern)'.",
   "why_it_matters": "Future medicals in real packets read 'candidate for', 'will need', 'plan: ...', 'consider', 'refer to'. The sample passes, but the next case would silently miss a specials item.",
   "fix": "Use a small named pattern list in the lexicon (recommend, candidate for, will need, plan, consider, refer to) and treat it as notes-only context.",
   "acceptance_test": "UT: 'Patient is a candidate for C5-C6 ACDF.' produces a FUTURE TREATMENT line; 'MRI ordered.' followed by a completed MRI record does not."},
  {"severity": "nit",
   "title": "R-EX-4 citation UT regex is lowercase-only",
   "evidence": "R-EX-4 :122 'every `record \\d+` in internal_notes_text is followed by a parenthesis'. The §6 notes use 'Record 4 (' at :281-294.",
   "why_it_matters": "As written, the test skips half the citations. They are correct today.",
   "fix": "Use a case-insensitive pattern.",
   "acceptance_test": "The UT matches 'Record 4 (' lines."}
 ],
 "whats_right": [
  "Letter block: 11/11 verbatim quotes, providers exactly as written, header dates, neutral '$8,390.00 (physical therapy charges to be supplemented)' total; I would paste it",
  "Notes block: every citation is 'record N (label, date)', with $185 as 'Request itemized PT ledger', lost wages as a damages mention, and the ESI as 'Request cost estimate'",
  "Charges accept/dismiss only (R-CH-7) and hedge sentences that can't be cut (R-TL-8, R-RV-2), so no path to a PT total and no misquoted MRI"
 ],
 "questions_for_chris": []}
```
