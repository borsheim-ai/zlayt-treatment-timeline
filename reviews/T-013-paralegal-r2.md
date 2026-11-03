# T-013 review, round 2 — paralegal-reviewer

**Verdict: changes** (0 blockers, 2 majors, 6 minors, 1 nit).

Round 1's blocker is fixed as worded. Flag notes, labels, counts and the defense's arguments are out of the letter. Of my 9 round-1 majors,
8 are resolved and 1 is partial. All 5 PM majors are resolved. The table with line numbers is in `artifacts/review-evidence/T-013-r2-resolution.md`.

I re-walked the 9 sample records through §6 by script (`artifacts/review-evidence/T-013-r2-paralegal-walk.py`, output `…-walk.out.txt`):
- All 11 quotes are verbatim in `sample.txt`.
- All 9 headings use the provider as written and the header date, in order.
- Gaps are 0,7,7,28,14,73,11,14.
- The charges add to $8,390.

**Would I paste the treatment section as-is?** Almost. I would fill in the Ex/Bates placeholders, reword the total line's parenthetical,
and remove the dot leaders. That means a tool built to these requirements is close to letter-ready.

**What an adjuster could use.** Eight of the ten golden flags have evidence strings that sit verbatim in the letter block: "after two missed
appointments", "Plan of care: 12 visits", "New onset pain", "may represent degenerative change; correlate clinically", "CT head negative".
They are the record's own words, and quoting the hedge was my own round-1 ask, so this is not a fabrication problem. The problem is that
:103 says "No flag text of any kind" appears in the letter, and the doc's own example breaks that. Nothing decides when a flagged sentence
may enter a letter quote. Nothing tells the attorney which quotes carry flagged language. The excerpt can't be edited, so if she wants a
flagged sentence out, her only choice is to drop the whole visit, and then the letter looks like a longer gap. The other carrier-facing item
is the total's parenthetical, "visit count not stated". That is tool-written text, and it volunteers a weakness to the carrier.

**Still missing for a paralegal:** a pending count and a pending-flag warning before copy; provider and date next to "record N" in the notes;
a "future treatment recommended" notes item for the ESI.

Exercised: listed in the JSON. No app exists for this card, so this is a document and fixture review, run by script against the golden files.

```json
{"card": "T-013", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md @ 64f766e (diff 65894f6..64f766e; no working-tree drift); against SPEC Appendix A Part 1, SAMPLE_CASE_TRUTHS, evals/golden/sample.txt + sample.expected.json, app/llm/lexicon.yaml, memory/contracts/api.md, personas/paralegal.md; round-1 reviews reviews/T-013-paralegal.md and reviews/T-013-product-manager.md; no app URL (requirements card)",
 "exercised": [
  "python3 tools/board.py show T-013 -> status in_review, rounds 1, commits [65894f6, 64f766e], AC 1-4 done",
  "git diff --stat 64f766e -- spec/REQUIREMENTS.md -> empty, rc=0 (reviewing committed text)",
  "read spec/REQUIREMENTS.md:1-330 in full; personas/paralegal.md (checklist §4 used); both round-1 reviews",
  ".venv/bin/python artifacts/review-evidence/T-013-r2-paralegal-walk.py -> artifacts/review-evidence/T-013-r2-paralegal-walk.out.txt: 11/11 letter quotes verbatim; 9/9 headings provider-in-source, header date, non-decreasing; gaps [0,7,7,28,14,73,11,14]; charges sum 8390; R-EX-1 forbidden strings all absent; golden flag evidence in letter: G1,C1(rec1,rec2),C2,P2,K1,K2,K3,K4 present, C1(rec7),P1,K5 absent",
  "grep -ci hedge app/llm/lexicon.yaml -> 5 (rationale text only, lines 286,288,300,314,325); lexicon.yaml:19 flag_types: [pre_existing, causation_weakening, compliance]",
  "python3 json check: case_04_duplicates_no_amounts.expected.json entries=4 from 6 records; sample.expected.json flags=10",
  "wc -l evals/golden/hallucinations.jsonl hallucinations_controls.jsonl -> 20, 5",
  "ls evals/golden | grep export -> rc=1 (sample.export.expected.txt not yet created; assigned to qa)",
  "grep -n title memory/contracts/api.md -> :120 'Treatment gap of 73 days', :128 'Two different accident dates', :179 edit keys (conflict listed in §8, judged on merits only)",
  "hand read of §6 Block 1 as a demand-letter paste and Block 2 as attorney notes against persona checklist items 1-23"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "verifiability_of_every_claim": 4, "workflow_fit": 4, "export_usability_in_demand_letter": 4, "adjuster_safety": 3, "charges_handling": 4, "flag_coverage_vs_truths": 5},
 "findings": [
  {"severity": "major",
   "title": "'No flag text of any kind' in the letter is contradicted by the worked example; there is no rule, no visibility and no control for flagged record sentences that reach the carrier",
   "evidence": "spec/REQUIREMENTS.md:11 'Flags are what an adjuster would use against the client, so they never enter block 1'; :103 R-EX-1 'No flag text of any kind appears in it'. §6 letter :216-217 quotes 'Discharged from PT after two missed appointments.', :220-221 'New onset pain radiating to right arm', :224-225 'Findings may represent degenerative change; correlate clinically.', :208-209 'Plan of care: 12 visits.' walk.out [4]: evidence of G1, C1 (rec 1, 2), C2, P2, K1, K2, K3, K4 in_letter=True. :88 R-RV-2 'Date, provider and excerpt are not editable.' No R-ID stops the generator from choosing all three sentences of record 3, which would put 'low back pain in 2023, resolved' into the letter.",
   "why_it_matters": "The R-EX-1 test passes only because its forbidden-string list happens to leave these phrases out. The requirement's actual claim is false for its own example, so the implementer can't tell what is allowed. Which record sentences go to the carrier is decided by whatever excerpt the model picked. The attorney is never told that the letter quotes the missed appointments or the degenerative hedge. If I want one of those quotes out, I can't trim the excerpt. I can only dismiss the whole visit, and dismissing entry 6 turns the letter's gap into 02/20 → 05/18. Whether to disclose is the attorney's call (litigation-lead lens). Making that call visible and possible is mine.",
   "fix": "Reword R-EX-1 and :11: the letter holds no tool-authored flag content (types, titles, reasons, day counts, counts). Record sentences quoted in an entry excerpt may coincide with flag evidence. Add to R-EX-4 a notes section 'FLAGGED LANGUAGE QUOTED IN THE LETTER' that lists each letter entry whose excerpt contains a flag's evidence string, with the flag id. Under R-RV-2, allow an excerpt edit limited to choosing a different set of whole sentences from the same record, code-verified. R-TL-8 qualifiers can't be removed. Log it as an edit with the original kept. State a default for non-qualifier flagged sentences, e.g. a prior-condition sentence about another body part is not in the default excerpt.",
   "acceptance_test": "UT on the §6 example: the notes list entries 4, 6, 7, 8, 9 under 'FLAGGED LANGUAGE QUOTED IN THE LETTER' with flag ids. UT: the letter contains no flag type label, title or reason string from sample.expected.json. E2E: on entry 6, select only 'Pain 3/10.' → the letter shows that excerpt and the notes show the original. On entry 8, trying to drop 'Findings may represent degenerative change; correlate clinically.' is refused (R-TL-8)."},
  {"severity": "major",
   "title": "R-TL-8 (qualifier travels with finding) keys on a lexicon 'hedge' category that does not exist; its entry-6 test cannot follow from the rule",
   "evidence": "spec/REQUIREMENTS.md:52 'a sentence matching the `hedge` category of `app/llm/lexicon.yaml`'. app/llm/lexicon.yaml:19 'flag_types: [pre_existing, causation_weakening, compliance]'. grep -ci hedge lexicon.yaml = 5, all in rationale/false_positive text (:286,288,300,314,325). :52 test requires 'entry 6 excerpt contains after two missed appointments', which matches lexicon entries of flag_type compliance (lexicon.yaml:572, :599), not any hedge.",
   "why_it_matters": "This is the rule that stops a quote from dropping the radiologist's hedge, which was my round-1 credibility finding. As written, nobody can implement or test it literally. One reasonable reading (causation_weakening) misses entry 6. Another (all categories) pulls 'low back pain in 2023' into entry 3's letter excerpt, which R-EX-1's test forbids.",
   "fix": "Name the trigger exactly. Example: lexicon entries with flag_type causation_weakening (may_represent, correlate_clinically, possibility_terms), plus compliance entries when the sentence is the same one that carries the finding. Or add an explicit `qualifier: true` key to named lexicon entries (a T-009 card change) and cite those ids.",
   "acceptance_test": "UT: the trigger set loaded from lexicon.yaml is non-empty and includes may_represent and correlate_clinically. Seeded entry 8 with the shortened excerpt → needs_review EXCERPT_OMITS_QUALIFIER. Entry 3 with excerpt 'Persistent neck pain 6/10, daily headaches.' stays verified (the pre_existing sentence does not trigger)."},
  {"severity": "minor",
   "title": "No pending count or pending-flag warning before copy",
   "evidence": "spec/REQUIREMENTS.md:107 R-EX-5 count line 'N entries, N charges in letter · N flags in internal notes · N of 9 records in letter' has no pending figure; pending items appear only inside the notes block (:106, :271). personas/paralegal.md §4 item 17.",
   "why_it_matters": "If I copy with the 73-day gap flag still pending, the attorney's notes show it only as a line under 'pending'. I need to see '3 flags not reviewed' before I hit Copy.",
   "fix": "Add 'N items pending (N flags)' to the R-EX-5 line, and require a one-step confirm on Copy when any flag is pending.",
   "acceptance_test": "E2E: leave the gap flag pending, click Copy letter → the confirm states '1 flag not reviewed'; the count line shows it."},
  {"severity": "minor",
   "title": "Total-line parenthetical is tool-authored text in the carrier block that volunteers a weakness; the placeholder name is inconsistent",
   "evidence": "spec/REQUIREMENTS.md:238 '(excludes physical therapy — per-visit rate only, visit count not stated)'; :110 template '(excludes <provider> — <reason>)' then '`<service>` comes from a fixed code lookup'. walk.out [7].",
   "why_it_matters": "'Visit count not stated' tells the carrier our PT billing is undocumented. Next to 'Plan of care: 12 visits' and the discharge at visit 9, it invites the non-compliance argument. The exclusion should be disclosed (that was my round-1 ask), but in neutral wording. The reasoning ('rate only, count not stated') belongs in the notes, where :257 already has it.",
   "fix": "Letter wording: 'Billed charges stated in these records: $8,390.00 (physical therapy charges, Capital PT, not included; to be supplemented)'. Use one placeholder name (<service>) in :110.",
   "acceptance_test": "UT: the sample total line equals the new string; the letter contains neither 'visit count' nor 'rate'."},
  {"severity": "minor",
   "title": "unclear → charge reclassification produces a charge with no value",
   "evidence": "spec/REQUIREMENTS.md:73 '`$1,2OO` and `$9S.00` are `unclear`, value null'; :79 'the amount and excerpt are immutable … `unclear` or `estimate` → `charge` re-runs judge #2'.",
   "why_it_matters": "If I reclassify the OCR-garbled $1,2OO as a charge, it can't be totaled because it has no value, and I'm not allowed to type $1,200. The total is then quietly wrong, or the action does nothing.",
   "fix": "State that `unclear` with a null value cannot become `charge`. It goes to the notes as 'request clean copy of bill'. Only `unclear` items with a parsed value may be reclassified.",
   "acceptance_test": "UT: reclassify a null-value unclear → 422 invalid_edit. The notes contain 'request clean copy' for $1,2OO."},
  {"severity": "minor",
   "title": "Ambiguous-date rule will send about a third of US-format dates to 'Dates to confirm'",
   "evidence": "spec/REQUIREMENTS.md:35 'ambiguous when its first two numbers are both 1–12 and differ'; :316 'she confirms once per date … per-packet convention is deferred'. Any day 1-12 that isn't equal to the month (11 of ~30 days a month) qualifies, e.g. 01/09/2026, 03/06/2026.",
   "why_it_matters": "Texas records are MM/DD. On a 100-record packet that is about 35 confirmations, and every unconfirmed entry is left out of gap math. That's noise I'll learn to click through.",
   "fix": "Keep the rule, but add per-packet inference as a requirement: if any date in the same packet or source has a first number > 12 → DD/MM, or a second number > 12 → MM/DD, apply it to that packet's ambiguous dates and show that it was applied. Ask only when the packet gives no evidence.",
   "acceptance_test": "UT: a packet containing 02/17/2026 and 03/06/2026 → 03/06 parses as March 6 with 'inferred MM/DD from 02/17/2026'; case_01's 04/05/2026 with no evidence still asks."},
  {"severity": "minor",
   "title": "Internal notes cite 'record N' without provider and date, and the letter has no record numbers",
   "evidence": "spec/REQUIREMENTS.md:249-251, :257, :263 (walk.out [8]); :108 'Internal record numbers appear in the internal notes only.'",
   "why_it_matters": "The attorney reads 'record 8 \"may represent…\"' and has to work out which letter entry that is. The gap line (:247) already does it correctly.",
   "fix": "Every notes citation reads 'record N (<provider>, <Month D, YYYY>)', as in :247.",
   "acceptance_test": "UT: every 'record \\d' in internal_notes_text is followed by a provider and a date."},
  {"severity": "minor",
   "title": "Future treatment recommended is not a notes item",
   "evidence": "spec/REQUIREMENTS.md:106 R-EX-4 lists damages mentions and bills to request but not recommended future care. Record 9 'Recommend cervical epidural steroid injection' appears only in the letter (:228-229).",
   "why_it_matters": "Future medicals are a specials element alongside lost wages. The doc already collects the other to-dos (bills to request, damages mentions). The ESI needs a cost estimate request too.",
   "fix": "Add 'FUTURE TREATMENT RECOMMENDED (no cost stated)' to R-EX-4, sourced from recommend/plan sentences with no amount, worded as an action ('request cost estimate').",
   "acceptance_test": "Sample: the notes list 'record 9 (Hill Country Pain Management, June 12, 2026): \"Recommend cervical epidural steroid injection.\" Request cost estimate.'"},
  {"severity": "nit",
   "title": "Dot leaders and mixed money formatting in the letter template",
   "evidence": "spec/REQUIREMENTS.md:233 '........ $6,240.00', :235 '....... $2,150.00', :238 '$8,390'.",
   "why_it_matters": "Dot leaders don't line up once pasted into Word in a proportional font, and they print. The total uses a different format from the line items.",
   "fix": "'Central ER, January 9, 2026: $6,240.00'; total '$8,390.00'.",
   "acceptance_test": "The golden export contains no '..' run, and every amount matches \\$[\\d,]+\\.\\d{2}."}
 ],
 "whats_right": [
  "The two-block export with the flag commentary kept out of the letter, reconciliation ('N of 9 records'), and the dismissed-entry-5 note at :275 is how I want to hand off to the attorney",
  "R-RV-9 core source modal with code offsets, plus R-TL-3 header date, R-TL-9 verbatim provider and R-TL-2 whole sentences: every letter line in §6 checked clean by script",
  "Charges: $185 never totaled, rate worded as 'request itemized PT ledger', duplicates merged by code, amount and excerpt immutable (R-CH-3/6/7, :257)"
 ],
 "questions_for_chris": [
  "Should record sentences the tool flagged (missed appointments, 'new onset', the degenerative hedge) appear in the treatment-section quotes by default, or does the attorney pick per entry? This decides the default excerpt in finding 1 (litigation-lead's call, not mine).",
  "For US-format dates like 03/06/2026, may the tool infer MM/DD from other dates in the same packet, or must she confirm each one?"
 ]}
```
