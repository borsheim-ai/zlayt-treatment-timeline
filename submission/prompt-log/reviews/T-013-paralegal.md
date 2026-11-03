# T-013 review — paralegal-reviewer

**Verdict: fail** (1 blocker, 9 majors, 6 minors).

The requirements get the hard truths right: the rate-not-charge handling, the "not merged" accident dates, the self-report label on
record 9, nothing accepted by default, and the negative assertions are all there, word for word. The document fails at the end of
the job, though. As written, the copy-ready letter text includes the flags I accepted, so the defense's arguments end up in our own
demand letter. The export also has no template, so nothing says what a pasted line looks like. Several gaps let a correct-looking
chronology mislead an adjuster: excerpts can drop the hedge, provider names are never checked against the record, nothing stops a
duplicate bill from being totaled twice, records that drop out of the chronology are never disclosed, and the PT rate and the total
have no export wording.

Exercised (paper walkthrough; no app exists at this card): I ran all 9 sample records by hand through every R-ID group and wrote down the
timeline, flags, charges and the literal export → `artifacts/review-evidence/T-013-paralegal-walkthrough.md`. I recomputed the gaps and
the total in Python. I read spec/REQUIREMENTS.md@65894f6 (no diff to HEAD), SPEC Appendix A, SAMPLE_CASE_TRUTHS, CONTRACT §5 M1/§5.2/§8.2/D.2/D.4,
memory/ASSUMPTIONS.md, and docs/LLM_VS_CODE.md (written 2 minutes after this commit; cited where it contradicts REQUIREMENTS). Agent memory
directory was empty; I did not write to it because it is outside my permitted paths.

```json
{"card": "T-013", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md @ 65894f6 (no diff to working tree); against spec/SPEC.md Appendix A Part 1 and spec/SAMPLE_CASE_TRUTHS.md; cross-read docs/LLM_VS_CODE.md (created after commit); no app URL (requirements card); sample case = Appendix A 9 records",
 "exercised": [
  "python3 tools/board.py show T-013 (AC 1-4)",
  "read spec/REQUIREMENTS.md lines 1-193, SPEC Appendix A Part 1, SAMPLE_CASE_TRUTHS, CONTRACT §5 M1, §5.2, §8.2, D.2, D.4, memory/ASSUMPTIONS.md",
  "git diff --stat 65894f6 -- spec/REQUIREMENTS.md -> empty (reviewing the committed text)",
  "python3 date arithmetic over the 9 header dates -> gaps 0,7,7,28,14,73,11,14; 6240+2150=8390 (matches truths)",
  "hand walkthrough of records 1-9 through R-IN, R-TL, R-FL, R-CH, R-RV, R-EX: built the timeline table, flag list (~9-10 flags), charges table, and the literal export -> artifacts/review-evidence/T-013-paralegal-walkthrough.md",
  "drafted the export I would need and compared it line by line with what R-EX-1..5 produce",
  "grep REQUIREMENTS for provider / dedupe / duplicate; grep docs/LLM_VS_CODE.md for provider, edit, export"
 ],
 "verdict": "fail",
 "scores": {"verifiability_of_every_claim": 3, "workflow_fit": 2, "export_usability_in_demand_letter": 1, "adjuster_safety": 2, "charges_handling": 4, "flag_coverage_vs_truths": 4},
 "findings": [
  {"severity": "blocker",
   "title": "Accepted flags export into the copy-ready demand-letter text",
   "evidence": "spec/REQUIREMENTS.md:82 R-EX-1 'copy-ready plain text for the treatment section of a demand letter and contains only what she accepted: entries, charges and flags'; :85 R-EX-4 'A flag she accepted exports as a reviewer note'; :86 R-EX-5 counts 'N flags exported'. Contradicted by docs/LLM_VS_CODE.md:78 'The flag appears only in the internal notes, never in the letter.' Walkthrough §6 shows the literal paste: 'REVIEWER NOTE — Prior condition: \"Patient reports low back pain in 2023, resolved.\"' etc. inside the treatment section.",
   "why_it_matters": "When I accept a flag, I am saying 'I've seen this and it is real.' I am not saying 'send this to the carrier.' A tool that meets R-EX-1 exactly puts the 2023 back pain, the degenerative language, the 73-day gap and the wrong accident date into the text I paste into our own demand. That hands the adjuster the defense, and it makes the export must-have unusable for its stated purpose.",
   "fix": "Split the export into two blocks with separate copy buttons: (1) 'Treatment section', which holds accepted entries and accepted charges only; (2) 'Internal review notes, do not send', which holds accepted flags, dismissed flags with an optional reason, amounts not totaled, records not represented, and edited items. Rewrite R-EX-1, R-EX-4 and R-EX-5 so flags never appear in block 1 and the count line is not part of either copied text. Align with docs/LLM_VS_CODE.md:78.",
   "acceptance_test": "E2E: accept all entries, charges and flags on the sample case, then copy the treatment section. The clipboard contains no flag text, no 'needs review' and no count line. Copy internal notes: it contains every accepted and dismissed flag."},
  {"severity": "major",
   "title": "Excerpt may be any substring, so a quote can drop the hedge; the only guard is a cuttable stretch",
   "evidence": "spec/REQUIREMENTS.md:38 R-TL-2 'Each excerpt is a substring of its source record'; :40 R-TL-4 checks the summary only against 'the excerpt'; :123 'Verbatim excerpt alone can mislead by omission (for example \"may represent degenerative change\"...)'; :126 the stretch may be 'cut entirely'. Walkthrough §2 entry 8: excerpt 'C5-C6 disc protrusion with mild right foraminal narrowing.' passes R-TL-2 and R-TL-4 and drops 'Findings may represent degenerative change; correlate clinically.' Same mechanism drops 'after two missed appointments' from entry 6.",
   "why_it_matters": "The adjuster has the MRI report. A demand that quotes the protrusion and leaves out the radiologist's hedge on the next line gets thrown back at us. 'Mistakes cost us credibility with adjusters' is the whole brief.",
   "fix": "Add an R-TL rule: an excerpt is one or more whole sentences, never cut mid-sentence. If the record contains a sentence flagged prior or causation that qualifies the cited finding (same record, adjacent sentence), the entry's excerpt includes it, or the entry is needs_review with the reason 'excerpt omits qualifying language'. Add a golden assertion for record 8.",
   "acceptance_test": "Eval: on the sample case, entry 8's exported excerpt contains 'may represent degenerative change'. Unit test: a mid-sentence excerpt fails the excerpt-boundary check."},
  {"severity": "major",
   "title": "Clicking back to the full source record is stretch, not core",
   "evidence": "spec/REQUIREMENTS.md:119-131: full record with highlighted excerpt exists only as R-ST-1/2; :126 the minimum modal can also be cut. SPEC Part 1: 'every statement the tool makes must be checkable against its source.'",
   "why_it_matters": "I reject any statement I can't click back to. An excerpt alone shows me what the model chose to show me. I need the whole record to check what it left out (see the finding above). A requirements doc that lets this be cut lets the core promise be cut.",
   "fix": "Promote the minimum (the full record text with the excerpt highlighted by code offsets, in a modal or panel) to a must-have R-ID under Review. Keep the side-by-side layout as the stretch.",
   "acceptance_test": "E2E: from every entry, flag and charge, one click or key opens the full source record with the excerpt highlighted. It passes with the stretch cut."},
  {"severity": "major",
   "title": "No export template or example; the citation stand-in ('record number') and ISO dates are not letter-ready",
   "evidence": "spec/REQUIREMENTS.md:83 R-EX-2 cites 'record number, provider, date'; :185 'Real firms use their own Bates or exhibit format; we state this is a stand-in.' No R-ID specifies a line layout, date format, or a sample export for the 9 records. Walkthrough §6 had to guess the layout.",
   "why_it_matters": "'Record 3' is the order I pasted things in. It means nothing to the adjuster, whose package is cited by exhibit or Bates page. '2026-01-16' reads as machine output in a letter. 'Copy-ready' can't be tested without a written expected output, and ship-bar item 5 depends on it.",
   "fix": "Add R-EX-6 with a fixed template and the full expected export for the sample case checked into evals/golden: MM/DD/YYYY dates, provider and record type, summary, then 'Source: <provider> <record type>, <date> [Ex. __ / Bates __]: \"<excerpt>\"', with an editable exhibit/Bates placeholder. The internal record number appears in internal notes only.",
   "acceptance_test": "Unit: the export of the accepted sample set is byte-identical to evals/golden/sample.export.txt. No '[Record N' string appears in the treatment section."},
  {"severity": "major",
   "title": "How 'unclear' amounts and the running total appear in the export is unspecified",
   "evidence": "spec/REQUIREMENTS.md:63 R-CH-3 defines the on-screen string 'rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review'; R-EX-1..5 (:82-86) never say whether an accepted rate or unclear amount exports, in what words, or how the total is labeled. Walkthrough §4, §6.",
   "why_it_matters": "If the R-CH-3 string exports, my letter says 'needs review'. If the total exports as a bare '$8,390' next to nine PT visits, the adjuster reads 'PT billed nothing' or takes it as complete medical specials. Either way the number is wrong in context. In Texas, recovery is limited to amounts actually paid or incurred, and bills are proved by affidavit, so the label has to say 'billed charges stated in these records' and nothing broader. (Texas practice point from my lens; confirm with research.)",
   "fix": "Add R-EX rules: the treatment section lists only accepted amounts classed `charge`. The total is labeled 'Total billed charges stated in these records' and names what it excludes (e.g. 'does not include physical therapy; itemized PT billing not in records'). Rates, estimates and unclear amounts go only to internal notes, worded as an action: 'request itemized ledger'.",
   "acceptance_test": "E2E on the sample case: the treatment section contains '$8,390.00' and the exclusion sentence, and contains neither '$185' nor 'needs review'. Internal notes contain the R-CH-3 string."},
  {"severity": "major",
   "title": "Edits are under-specified: charges and flags undefined, edited text not re-checked for facts, original not retained, label placement unclear",
   "evidence": "spec/REQUIREMENTS.md:71 R-RV-1 'Each entry, flag and charge can be accepted, edited or dismissed'; :72 R-RV-2 defines editing for 'the summary text only'; :73 R-RV-3 checks only added dates/numbers; :72 'export text shows the edited summary with its citation'.",
   "why_it_matters": "I can type 'herniation' into the MRI summary and it exports under the radiologist's citation, so the citation now vouches for words the record doesn't contain. Nothing says I can't edit $6,240 to $6,420, which would break ship-bar item 1. If the 'edited' label lands in the pasted text, it's embarrassing; if it lands nowhere, the attorney can't tell what I changed.",
   "fix": "State that the amount and date are never editable (only accept or dismiss, plus an optional note). A flag edit means a note only, not a change to its quoted evidence. An edited summary keeps the original model text in the audit, re-runs the R-RV-3 code check, and re-runs judge #1 against the excerpt, warning before accept if the judge returns partially or unsupported. The 'edited' label shows in the review UI and internal notes, never in the treatment-section text.",
   "acceptance_test": "E2E: the charge amount field is not editable. Editing entry 8 to add 'herniation' shows a warning before accept. The treatment section contains no 'edited' string. The audit shows before and after."},
  {"severity": "major",
   "title": "Provider name is not required to come from the record",
   "evidence": "spec/REQUIREMENTS.md:37 R-TL-1 requires a provider field; :38 R-TL-2 grounds only the excerpt; no R-ID checks provider. docs/LLM_VS_CODE.md:31 (post-commit) does: 'the provider string appears in the record'.",
   "why_it_matters": "Provider names go into the letter, and adjusters match providers to bills. 'Capital Physical Therapy, LLC' or 'Dr. Maria Alvarez, MD' would be invented facts, and nothing in the requirements would catch them.",
   "fix": "Add to R-TL-2: the provider string must appear in the record's header or body after normalization; otherwise the entry is needs_review. Add it to grounding_rate.",
   "acceptance_test": "Unit: the model returns provider 'Capital Physical Therapy' for record 4 and the entry becomes needs_review. Eval: every exported provider is a substring of its record."},
  {"severity": "major",
   "title": "Date of service source not pinned; the record-7 trap (body date 2026-01-19) is untested",
   "evidence": "spec/REQUIREMENTS.md:39 R-TL-3 seeded test uses record 3 ('model returns 2026-01-19 for record 3'); record 3 has no second date. Record 7's body contains 'Date of accident per intake form: 2026-01-19'. The header-date rule exists only as a proposed assumption (:184).",
   "why_it_matters": "If record 7 is dated by the body date, pain management sorts to 01/19, ahead of the PCP visit. The 73-day gap disappears and the chronology is wrong in a way I'd only catch by re-reading every record.",
   "fix": "Make it a requirement, not an assumption: the date of service is the record's header or row date, parsed by code. Dates found in the body are never the date of service. Change the R-TL-3 seeded test to record 7.",
   "acceptance_test": "Unit and eval: entry 7 date = 2026-05-18, and the gap flag is 73 days, even when the generator returns 2026-01-19."},
  {"severity": "major",
   "title": "No requirement for duplicate records or duplicate charges",
   "evidence": "Grep 'duplicate' in spec/REQUIREMENTS.md: 0 hits. 'dedupe' appears only in passing at :94 (R-CO-1 list of code steps). R-TL-1 :37 'one per source record'; R-CH-3 :63 sums every accepted charge. CONTRACT §5 M1 requires a duplicate-records golden case.",
   "why_it_matters": "Duplicate pages are routine in record stacks (the ER summary plus the ER bill). Two accepts of $6,240 make the total $14,630. An inflated special-damages number is exactly the credibility loss the brief describes.",
   "fix": "Add R-TL-7 and R-CH-6: code detects duplicate records and duplicate amounts (same provider, date and amount). It shows them as one item with both sources and never adds the same charge twice without an explicit 'these are separate bills' action.",
   "acceptance_test": "Eval on the golden duplicate case: entry count and total equal the hand-written expected values. Unit: two identical $6,240 charges from the same provider and date total $6,240."},
  {"severity": "major",
   "title": "The export never tells me which source records are missing from it",
   "evidence": "spec/REQUIREMENTS.md:38 rejected entries go 'only in the \"could not verify\" tray, never in the timeline or export'; :82 export = accepted set; docs/LLM_VS_CODE.md (post-commit) 'manual add is a deliberate cut'. No R-ID reconciles records in against entries out.",
   "why_it_matters": "If entry 5 is rejected, unreviewed, or dismissed by mistake, the treatment section jumps from 01/23 to 03/06 and looks complete. Dropping a visit understates treatment, and I would not know to add it by hand.",
   "fix": "Add R-EX-7: internal notes list every input record not represented in the treatment section, with its reason (rejected, dismissed, not reviewed). The UI shows 'N of 9 records in export' before copy.",
   "acceptance_test": "E2E: leave entry 5 unreviewed and export. Internal notes say 'Record 5 (Capital PT, 02/20/2026): not reviewed', and the UI shows '8 of 9 records'."},
  {"severity": "minor",
   "title": "Batch accept is neither required nor a stated non-goal",
   "evidence": "spec/REQUIREMENTS.md:71-76 (R-RV-1..6) have no batch action; §5 non-goals :139-149 don't list it. Walkthrough §3: about 21-22 single decisions on a 9-record case.",
   "why_it_matters": "A real file has 100+ entries. One-by-one accepting is where the time savings go. An unrestricted 'accept all' breeds rubber-stamping, so the requirements need to make the call either way.",
   "fix": "Either add R-RV-7, 'accept all verified entries in view' (never amounts, dates or flags, logged as a batch action in the audit), or list batch accept as a non-goal with the reason.",
   "acceptance_test": "E2E: batch accept on the sample case accepts only verified non-amount entries; charges remain pending."},
  {"severity": "minor",
   "title": "Review decisions are not required to survive a reload",
   "evidence": "spec/REQUIREMENTS.md:67-76: no persistence requirement for accept, edit or dismiss state.",
   "why_it_matters": "I get interrupted constantly. Losing a half-finished review to a refresh means I stop trusting the tool and go back to Word.",
   "fix": "Add an R-RV requirement: review state persists for the session (SQLite) and survives a page reload.",
   "acceptance_test": "E2E: accept 3 items, reload, and the 3 items are still accepted."},
  {"severity": "minor",
   "title": "The lost-wages mention ('missing 3 days of work') has nowhere to go",
   "evidence": "spec/REQUIREMENTS.md:64 R-CH-4 keeps it out of charges; no other R-ID surfaces it. SAMPLE_CASE_TRUTHS: 'a damages mention, not a billed charge'.",
   "why_it_matters": "Lost wages are a damages element I track. If the generator's excerpt for record 5 is only 'Pain 4/10, improving.', the fact disappears from everything I see.",
   "fix": "Require damages mentions that aren't charges (lost work and similar) to be listed in internal notes with their excerpt.",
   "acceptance_test": "Eval: on the sample case, internal notes contain 'missing 3 days of work' with a record 5 citation."},
  {"severity": "minor",
   "title": "No 'bills still to request' list",
   "evidence": "spec/REQUIREMENTS.md:57-65: charges cover found amounts only. Sample: EMS, Dr. Alvarez, Hill Country (x2) and Capital PT itemization have no billed amount.",
   "why_it_matters": "Before a demand, I chase bills for every provider in the chronology. The tool already knows which providers have no amount.",
   "fix": "Internal notes list providers with treatment entries but no `charge` amount.",
   "acceptance_test": "Eval: the sample list is Austin EMS, Dr. Alvarez, Capital PT (rate only), and Hill Country Pain Management."},
  {"severity": "minor",
   "title": "Flag evidence for gaps and the home of date_ambiguous flags are undefined",
   "evidence": "spec/REQUIREMENTS.md:54 R-FL-5 'Every flag cites verbatim excerpt(s)'. A gap is an absence, and nothing says what it cites. :30 R-IN-3 raises 'date_ambiguous' but :55 R-FL-6 says 'four groups'. :30 does not define what makes '03/04/26' ambiguous when Texas records are MM/DD.",
   "why_it_matters": "If ambiguity isn't defined, either every MM/DD/YY date flags (noise) or none do. A gap flag with no cited bounds can't be checked.",
   "fix": "A gap flag cites the two bounding entries (date, provider, excerpt). date_ambiguous is a named fifth group or lives in the input panel. Define the ambiguity rule (for example: a 2-digit year, or a document mixing DD/MM and MM/DD evidence).",
   "acceptance_test": "Unit: the gap flag carries entry IDs 6 and 7. Unit: '01/16/2026' does not flag in a US-format case."},
  {"severity": "minor",
   "title": "Ship-bar item 5 names no score key",
   "evidence": "spec/REQUIREMENTS.md:163 'reviews/<card>-paralegal-reviewer.md score field' — no field name. This brief writes reviews/<card>-paralegal.md, so the file name differs too.",
   "why_it_matters": "If the key and the path aren't fixed, '>= 4/5' can't be checked mechanically at the M3 gate.",
   "fix": "Name the key (e.g. scores.verify_every_claim_quickly) and the review path pattern.",
   "acceptance_test": "A gate script reads the key from the M3 paralegal review file and compares it to 4."}
 ],
 "whats_right": [
  "R-CH-3 handles $185 exactly per truths: rate, no PT total, $8,390 only after both charges are accepted (REQUIREMENTS.md:63)",
  "R-FL-2/R-FL-4 keep the two accident dates unmerged and label record 9 as patient self-report, not a physician opinion (:51, :53)",
  "Nothing accepted by default, amounts always need an explicit accept, and the R-CO-3 negative assertions are named golden checks (:65, :71, :96)"
 ],
 "questions_for_chris": [
  "How does Zinda cite medical records in a demand: exhibit number, Bates page, or provider and date only? This sets the R-EX citation template.",
  "Does Zinda's treatment section address gaps or prior conditions proactively, or are those attorney-only notes? This decides whether any flag-derived text belongs in the letter."
 ]}
```
