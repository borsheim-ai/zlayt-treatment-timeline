# Subagent: T-013 round-2 review: paralegal (T-013 round-2 review: paralegal)

Source: `agent-a7075e19338be2d0c.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:29:32.497Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 2.
Card T-013 "spec/REQUIREMENTS.md" — M1. AC: `python3 tools/board.py show T-013`. Round-1 reviews: reviews/T-013-paralegal.md (yours, fail) and reviews/T-013-product-manager.md (changes). New version: commit 64f766e (`git diff 65894f6..64f766e -- spec/REQUIREMENTS.md`).
Exercise hands-on: for every round-1 blocker and major in BOTH reviews, decide resolved / partially / not, citing the new line numbers (table in artifacts/review-evidence/T-013-r2-resolution.md). Re-walk the 9 sample records through the new export template (§6 worked example): would you paste the treatment section into a demand letter as-is? Is anything in it that an adjuster could use against the client? Is anything missing that a paralegal needs? Note §8 lists conflicts with the architect's API — those are being resolved on T-014; judge the requirements on their own merits.
Write reviews/T-013-paralegal-r2.md (D.2 JSON). Include scores.verify_quickly (1–5: "a tool meeting these requirements would let me verify every claim quickly"). Do not fix anything. Reply ≤ 30 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:33.768Z

Starting with memory, the round-1 reviews, and the board state.

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:34.950Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py show T-013; git log --oneline -8; git status --short | head -20",
 "description": "Check memory, board card, git log"
}
````

### User / tool · 2026-11-02T00:29:35.122Z

**tool result**
````
total 0
drwxr-xr-x@ 2 arsis  staff   64 Nov  1 18:26 .
drwxr-xr-x@ 8 arsis  staff  256 Nov  1 18:28 ..
---
id: "T-013"
title: "spec/REQUIREMENTS.md: testable must-haves, stretch pick, non-goals"
milestone: "M1"
role: "writer"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:29:00Z"
claimed_by: "writer"
claimed_at: "2026-11-02T00:25:26Z"
rounds: 1
commits: ["65894f6", "64f766e"]
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-013-product-manager.md", "at": "2026-11-02T00:25:13Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-013-paralegal.md", "at": "2026-11-02T00:25:13Z"}
ac:
  - {"n": 1, "text": "every Part 1 must-have and constraint maps to >=1 R-ID with a pass/fail test description", "done": true, "evidence": "Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)"}
  - {"n": 2, "text": "one stretch item selected with a 3-line rationale and a cut rule", "done": true, "evidence": "Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)"}
  - {"n": 3, "text": ">=6 explicit non-goals (e.g. PDF/OCR, multi-case, auth, real data, drafting prose in firm voice)", "done": true, "evidence": "Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)"}
  - {"n": 4, "text": "ship-bar section mirrors CONTRACT §8.2 numbers and names the eval that measures each", "done": true, "evidence": "Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)"}
---
## Description
Turn Appendix A Part 1 into testable requirements (R-IDs) the M2/M3 cards and evals trace to. Stretch: default recommendation side-by-side source viewer (serves 'reviews rather than trusts'); argue it or pick another, cut if time runs out. Explicit non-goals. Writer owns this file for this card.

## Notes (append-only, newest last)
- 2026-11-02T00:17:51Z writer: claimed
- 2026-11-02T00:19:27Z writer: Wrote spec/REQUIREMENTS.md: 48 R-IDs across IN/TL/FL/CH/RV/EX/CO/SU/ST, stretch=source viewer w/ 45-min cut rule, 11 non-goals, ship bar table, assumptions. Metric names in ship bar are proposed; qa to confirm. Ask orchestrator: log non-goals in SCOPE_CUTS.md and add 5 proposed assumptions (strict >30, record header format, citation format, rate-not-billable, same-day not merged) to ASSUMPTIONS.md. Proposed R-RV-3 (edit adds number/date warning) needs architect confirm.
- 2026-11-02T00:19:27Z writer: AC 1 checked: spec/REQUIREMENTS.md sections 1-3: R-IN/TL/FL/CH/RV/EX/CO/SU, each with pass/fail test + checker
- 2026-11-02T00:19:27Z writer: AC 2 checked: spec/REQUIREMENTS.md section 4: source viewer, 3-line rationale, 45-min/150%-M3 cut rule, R-ST-1/2
- 2026-11-02T00:19:27Z writer: AC 3 checked: spec/REQUIREMENTS.md section 5: 11 non-goals incl. PDF/OCR, multi-case, auth, real data, firm-voice drafting
- 2026-11-02T00:19:27Z writer: AC 4 checked: spec/REQUIREMENTS.md section 6: five CONTRACT 8.2 criteria with numbers, metric names, run commands, R-IDs
- 2026-11-02T00:19:28Z writer: moved in_progress -> in_review
- 2026-11-02T00:20:37Z orchestrator: Orchestrator merged the 11 non-goals into memory/SCOPE_CUTS.md (rows 1-11) and proposed assumptions into memory/ASSUMPTIONS.md (A-104..A-108).
- 2026-11-02T00:21:18Z orchestrator: review dispatched: product-manager-reviewer, paralegal-reviewer
- 2026-11-02T00:25:13Z orchestrator: review product-manager-reviewer (claude-opus-5-5): changes — reviews/T-013-product-manager.md; round 1; findings:
    - [major] Review-step must-have: 'edit each flag' is undefined and no test exercises the action-by-item matrix — fix: Define the edit field for each item type: entry = summary; flag = reason or note text, with the excerpt fixed; charge = classification only, or not editable, stated explicitly. Add an E2E row covering {accept, edit, dismiss} x {entry, flag} (6 cells) plus the decided charge beh
    - [major] What an accepted flag becomes in the copy-ready letter export is undecidable and risky for the user's job — fix: Decide and state what accepting a flag means: acknowledged or include in letter. Specify the export layout, for example a treatment section of entries and charges, followed by a separated 'Reviewer notes, not for the letter' block for flags. Make R-EX-4's wording rule a ch
    - [major] Stretch cut rule's start condition can never be met inside M3 — fix: Scope the start condition to M3: all R-IDs with M2/M3 checkers passing (name them, or 'all R-IN/TL/FL/CH/RV/EX + R-CO-1..3,6,7,9'), E2E green, and M3 under 100% of budget. Then build the stretch before the M3 gate so the gate reviews it. Say which fallback applies when: minimum modal if >= 20 of the 45 min remain, e
    - [major] R-TL-4 (no invented facts) cites nonexistent R-QA-2 and has no catch threshold — fix: Replace '(see R-QA-2)' with the threshold inline: 'judge #1 flags >= 95% of the 20 seeded unsupported summaries (metric hallucination_catch_rate)'. Alternatively, create R-QA-2 with that text.
    - [major] R-CO-7 determinism test is circular and does not test what the requirement claims — fix: Test the claim directly: across 3 runs, the set of entry IDs, the set of (flag type, record IDs, excerpt) tuples, every item's state and the totals are identical. Summary text may vary but must be judged `supported` each run. If LLM flag sets cannot be held identical, change the requirement to a 
    - [minor] R-SU-3 product-note test is a panel opinion, not a checklist — fix: Add a checklist: 7 headings present, 3-5 ship criteria, exactly 3 metrics each with a 'tells you' line, and a page limit (for example the pandoc PDF is 1 page, or <= 650 words).
    - [minor] Ground rule 'tell us which AI tools' has no R-ID; R-SU-4 does not test 'unedited' — fix: Add the TOOLS.md requirement to R-SU-4 (tools, models, team organisation) and require that the export is produced by tools/export_prompt_log.py with no manual edits (diff against a re-run).
    - [minor] R-FL-4 'labeled as patient self-report' has no decidable check — fix: Name the field, for example flag.source_kind == 'patient_report', and the UI text, for example 'Patient self-report'.
    - [minor] Placement of an ambiguous-date record in the timeline and gap math is unspecified — fix: State the rule, for example 'excluded from ordering and gap math, shown in a Dates to confirm tray; once she confirms a date it re-enters'.
    - [minor] R-EX-3 and R-EX-2 tests cover less than their requirements — fix: Add an order assertion on exported item dates. Restrict R-EX-2 to statement and amount lines.
    - [minor] Ship bar row 5 measurement path and score key don't match repo convention — fix: Use `reviews/<card>-paralegal.md`, `scores.verify_every_claim_quickly >= 4`, and name it in the paralegal reviewer brief.
    - [minor] §7 proposed assumptions are stale and R-RV-3 is unconfirmed but sits in the must-have table — fix: Cite A-104..A-108 by ID in §7. Mark R-RV-3 as 'proposed' in the table, or confirm it via ADR.
    - [minor] Running total reads $0 on first load (I would do differently) — fix: Show 'Accepted: $X · Pending review: $Y (N charges)'. Only Accepted exports.
- 2026-11-02T00:25:13Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-013-paralegal.md
- 2026-11-02T00:25:13Z orchestrator: assigned: writer
- 2026-11-02T00:25:26Z writer: claimed
- 2026-11-02T00:29:00Z writer: Round 2: rewrote spec/REQUIREMENTS.md against PM + paralegal findings and orchestrator decisions 1-10. 61 R-ID rows (previous note said 48; file had 47).
- 2026-11-02T00:29:00Z writer: AC 1 checked: Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)
- 2026-11-02T00:29:00Z writer: AC 2 checked: Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)
- 2026-11-02T00:29:00Z writer: AC 3 checked: Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)
- 2026-11-02T00:29:00Z writer: AC 4 checked: Round 2: spec/REQUIREMENTS.md re-verified (sections 1-3, 4, 5, 7)
- 2026-11-02T00:29:00Z writer: moved in_progress -> in_review

## Handoff
Round 2. Changed per finding: BLOCKER flags in letter -> R-EX-1/4/5/9 two blocks, flags only in internal notes, E2E asserts no flag text; template+worked example sec 6, R-EX-6 golden file. Majors: edit defined per type R-RV-2/3, R-CH-7; stretch start/fallback rewritten sec 4; R-TL-4 inline 19/20 + controls; R-CO-7 rewritten; hedge travels with finding R-TL-8; source record open is core R-RV-9; provider verbatim R-TL-9; header date R-TL-3 (record-7 test); dedupe R-TL-7/R-CH-6; unclear/total label R-EX-4/8; reconciliation R-EX-7. Minors: batch R-RV-7, reload R-RV-8, damages->notes, bills to request, R-IN-5 dates to confirm, R-FL-7 source_kind, TOOLS.md/unedited R-SU-4, SU-3 checklist, scores.verify_quickly. Not run: docs only. OPEN: api.md/ADR-005/009 conflict with R-RV-2, R-RV-7, R-EX-4/6 (listed sec 8); needs new reason codes; qa to add evals/golden/sample.export.expected.txt; R-CH-7 rate->charge block is my proposal.

64f766e docs(spec): requirements round 2: split letter vs internal notes, edit rules, export template
f419c3b feat(research): flag lexicon with negation guard and test vectors (T-009)
0a10094 feat(personas): product/engineering reviewer dossiers (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
34e9398 feat(personas): domain reviewer dossiers (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)
47520a8 feat(evals): golden set - sample case, 8 synthetic cases, 20 seeded hallucinations, validator
94c7b08 docs(architect): ADRs, LLM/code table, API contract draft
2c76cda docs(research): PI chronology practice, adjuster attacks, Texas notes, glossary (T-008)
1e9b348 feat(harness): assign/dispatch markers so the stop guard ignores queued work
 M .claude/hooks/git_guard.py
 M .gitignore
 M board/activity.jsonl
 M board/cards/T-001.md
 M board/cards/T-002.md
 M board/cards/T-003.md
 M board/cards/T-004.md
 M board/cards/T-006.md
 M board/cards/T-007.md
 M board/cards/T-008.md
 M board/cards/T-009.md
 M board/cards/T-010.md
 M board/cards/T-011.md
 M board/cards/T-012.md
 M board/cards/T-013.md
 M board/cards/T-014.md
 M board/cards/T-015.md
 M board/cards/T-020.md
 M memory/LESSONS.md
 M memory/PROGRESS.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:36.886Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-013-paralegal.md; echo ======; wc -l spec/REQUIREMENTS.md; git diff --stat 65894f6..64f766e; git status --short spec/ reviews/",
 "description": "Read round-1 paralegal review and diff stats"
}
````

### User / tool · 2026-11-02T00:29:37.013Z

**tool result**
````
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
======
     329 spec/REQUIREMENTS.md
 .claude/agents/accessibility-reviewer.md           |   1 +
 .claude/agents/chaos-tester-reviewer.md            |   1 +
 .claude/agents/claims-adjuster-reviewer.md         |   1 +
 .claude/agents/hiring-panel-reviewer.md            |   1 +
 .claude/agents/installer-reviewer.md               |   1 +
 .claude/agents/legal-nurse-reviewer.md             |   1 +
 .claude/agents/litigation-lead-reviewer.md         |   1 +
 .claude/agents/paralegal-reviewer.md               |   1 +
 .claude/agents/privacy-compliance-reviewer.md      |   1 +
 .claude/agents/product-manager-reviewer.md         |   1 +
 .claude/agents/security-reviewer.md                |   1 +
 .claude/agents/staff-engineer-reviewer.md          |   1 +
 .claude/agents/ux-designer-reviewer.md             |   1 +
 CLAUDE.md                                          |  14 +-
 app/README-arch.md                                 |  61 ++
 app/llm/lexicon.yaml                               | 699 +++++++++++++++++++++
 artifacts/m0-smoke/agent-load-tests.md             |  21 +
 artifacts/m0-smoke/live-feed.md                    |   9 +
 board/activity.jsonl                               |  67 ++
 board/cards/T-001.md                               |   3 +-
 board/cards/T-002.md                               |   3 +-
 board/cards/T-003.md                               |   3 +-
 board/cards/T-004.md                               |   3 +-
 board/cards/T-005.md                               |  21 +-
 board/cards/T-006.md                               |  21 +-
 board/cards/T-007.md                               |  37 +-
 board/cards/T-008.md                               |  30 +
 board/cards/T-009.md                               |  28 +
 board/cards/T-010.md                               |  29 +
 board/cards/T-011.md                               |  29 +
 board/cards/T-012.md                               |  26 +
 board/cards/T-013.md                               |  38 ++
 board/cards/T-014.md                               |  30 +
 board/cards/T-015.md                               |  29 +
 board/cards/T-016.md                               |  26 +
 board/cards/T-017.md                               |  26 +
 board/cards/T-018.md                               |  26 +
 board/cards/T-019.md                               |  25 +
 board/cards/T-020.md                               |  25 +
 board/cards/T-021.md                               |  25 +
 board/milestones.md                                |   4 +-
 docs/LLM_VS_CODE.md                                |  94 +++
 docs/RUNBOOK.md                                    |  19 +-
 evals/golden/README.md                             | 138 ++++
 evals/golden/case_01_date_formats.expected.json    | 324 ++++++++++
 evals/golden/case_01_date_formats.txt              |  42 ++
 evals/golden/case_02_gap_boundaries.expected.json  | 410 ++++++++++++
 evals/golden/case_02_gap_boundaries.txt            |  42 ++
 evals/golden/case_03_rate_and_ocr.expected.json    | 296 +++++++++
 evals/golden/case_03_rate_and_ocr.txt              |  27 +
 .../case_04_duplicates_no_amounts.expected.json    | 212 +++++++
 evals/golden/case_04_duplicates_no_amounts.txt     |  32 +
 .../golden/case_05_provider_conflict.expected.json | 261 ++++++++
 evals/golden/case_05_provider_conflict.txt         |  27 +
 .../case_06_subtle_pre_existing.expected.json      | 292 +++++++++
 evals/golden/case_06_subtle_pre_existing.txt       |  27 +
 .../golden/case_07_prompt_injection.expected.json  | 277 ++++++++
 evals/golden/case_07_prompt_injection.txt          |  22 +
 .../case_08_diagnosis_temptation.expected.json     | 223 +++++++
 evals/golden/case_08_diagnosis_temptation.txt      |  22 +
 evals/golden/check_golden.py                       | 205 ++++++
 evals/golden/hallucinations.jsonl                  |  20 +
 evals/golden/hallucinations_controls.jsonl         |   5 +
 evals/golden/sample.expected.json                  | 683 ++++++++++++++++++++
 evals/golden/sample.txt                            |  47 ++
 memory/ASSUMPTIONS.md                              |  24 +-
 memory/DECISIONS.md                                | 189 +++++-
 memory/GLOSSARY.md                                 |  52 +-
 memory/LESSONS.md                                  |   2 +
 memory/PROGRESS.md                                 |   9 +
 memory/SCOPE_CUTS.md                               |  11 +
 memory/STATE.md                                    |  24 +-
 memory/contracts/api.md                            | 243 ++++++-
 personas/accessibility.md                          |  70 +++
 personas/chaos-tester.md                           |  72 +++
 personas/claims-adjuster.md                        |  74 +++
 personas/hiring-panel.md                           |  87 +++
 personas/installer.md                              |  65 ++
 personas/legal-nurse.md                            |  74 +++
 personas/litigation-lead.md                        |  73 +++
 personas/paralegal.md                              |  82 +++
 personas/privacy-compliance.md                     |  78 +++
 personas/product-manager.md                        |  74 +++
 personas/security.md                               |  75 +++
 personas/staff-engineer.md                         |  71 +++
 personas/ux-designer.md                            |  75 +++
 research/ASSUMPTIONS-proposed.md                   |  23 +
 research/adjuster-attacks.md                       | 110 ++++
 research/chronology-practice.md                    |  90 +++
 research/lexicon_selfcheck.py                      | 135 ++++
 research/texas-pi-notes.md                         | 110 ++++
 spec/REQUIREMENTS.md                               | 328 +++++++---
 submission/NEEDS_CHRIS.md                          |   2 +
 tools/board.py                                     |  51 +-
 tools/compile_agents.py                            |   1 +
 tools/export_prompt_log.py                         | 108 ++++
 tools/tests/test_board.py                          |  16 +
 97 files changed, 7454 insertions(+), 162 deletions(-)
?? reviews/
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:37.965Z

**tool call — Bash**
````
{
 "command": "sed -n '/```json/,/```/p' reviews/T-013-product-manager.md | head -5; grep -c severity reviews/T-013-product-manager.md",
 "description": "Check PM review JSON presence"
}
````

### User / tool · 2026-11-02T00:29:38.058Z

**tool result**
````
```json
{"card": "T-013", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md at commit 65894f6 (unchanged in working tree) against spec/SPEC.md Appendix A Part 1, spec/SAMPLE_CASE_TRUTHS.md, docs/CONTRACT.md §5, §5.2, §8.2; no app (M1)",
 "exercised": [
  "python3 tools/agent_prompt.py product-manager-reviewer; python3 tools/board.py show T-013",
15
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:40.160Z

The paralegal dossier now exists. I'll read it, the full new REQUIREMENTS.md, and confirm there's no uncommitted drift.

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:41.163Z

**tool call — Bash**
````
{
 "command": "git diff --stat 64f766e -- spec/REQUIREMENTS.md; echo \"rc=$?\"; cat personas/paralegal.md",
 "description": "Check working-tree drift and read paralegal dossier"
}
````

### User / tool · 2026-11-02T00:29:41.258Z

**tool result**
````
rc=0
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.**
She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.

## 2. Day-to-day context
- Tools: case-management system (Filevine/Clio-style), a PDF viewer with Bates stamps, Word templates for the demand, Excel for specials, Outlook for records requests.
- Volume: several demand packages a week; records arrive piecemeal from EMS, ER, PCP, PT, imaging, pain management, often with duplicates and copy-forward notes.
- Pressures: Stowers/time-limited demands with deadlines; attorneys who want the demand out today; adjusters who cross-check every claim against the records.
- A bad day: the adjuster's response letter quotes a record she summarized wrong, or points to a gap or prior injury she missed. The firm's credibility on that file — and her attorney's trust in her — drops.

## 3. Goals and success criteria for this artifact
- A chronology she can verify line by line, fast: date of service, provider/facility, short summary in the provider's own words, and the exact excerpt with its record reference.
- The tool surfaces what the adjuster will attack (gaps, prior conditions, conflicts, missed appointments, hedged causation) before the demand goes out, so the attorney decides how to handle it.
- Billed charges she can reconcile: every amount with its source, a total of explicit charges only, and unclear amounts called out rather than guessed.
- An export she can paste into the treatment section of the demand letter with minimal reformatting, containing only what she accepted.

## 4. Review checklist
1. Every date in the timeline appears verbatim (or as an unambiguous reformat) in its source record; nothing is dated by when a note was entered rather than the date of service.
2. Every entry shows provider and facility as written in the record (e.g., "Capital PT", "Dr. Alvarez, primary care"), not a guessed full name.
3. Every entry's excerpt is a verbatim quote from that record, and I can see which record (# / source / date) it came from in one action.
4. The one-line summary uses the provider's own clinical words (e.g., "cervical strain; concussion without loss of consciousness") and adds nothing that is not in the excerpt.
5. Entries are in date-of-service order; same-day records (EMS and ER on 2026-01-09) are both present and not merged.
6. The 73-day gap (2026-03-06 PT discharge → 2026-05-18 pain management) is flagged with both dates and the day count; the 28-day interval (01-23 → 02-20) is not flagged.
7. The accident-date conflict is flagged: 2026-01-09 (EMS/ER) vs "Date of accident per intake form: 2026-01-19" (record 7), with both excerpts; the tool does not pick one.
8. The PT plan vs actual discrepancy is surfaced: "Plan of care: 12 visits" vs "Discharged from PT after two missed appointments" at visit 9.
9. Prior-condition mentions are flagged: "low back pain in 2023, resolved" (record 3) and "may represent degenerative change" (record 8), each with its excerpt.
10. PT discharge notes that mention missed appointments are flagged as causation/compliance risk.
11. Charges list shows $6,240 (ER) and $2,150 (MRI) with sources, and the running total of explicit charges is $8,390.
12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total.
13. "Missing 3 days of work" is not listed as a billed charge (it may be noted as a lost-wages mention).
14. Every entry and every flag has accept, edit, and dismiss; edits keep the original visible somewhere so I can see what I changed.
15. I can review with the keyboard (move to next item, accept, dismiss) without reaching for the mouse on every row.
16. Items that need review are shown first and say why in one sentence.
17. I can see how many items remain unreviewed before I export.
18. Export contains only items I accepted (and my edits, not the original text); dismissed items never appear.
19. Each exported line has date, provider, what happened, and a cite back to the record (e.g., "(Rec. 3, Dr. Alvarez, 2026-01-16)").
20. Export pastes into Word as clean text: no HTML, no UI labels like "verified", no markdown symbols that would print.
21. Billed charges in the export are labeled as billed amounts with their sources; unclear amounts are not silently included in the total.
22. Nothing in the timeline or export states causation, diagnosis, or severity the records do not state (e.g., no "disc herniation caused by the collision").
23. Patient self-reports stay attributed ("Patient states symptoms began after the January collision"), never turned into the provider's finding.

## 5. Red flags / dealbreakers
- Any statement, date, or amount I cannot trace to a verbatim excerpt.
- A total that includes the $185 rate multiplied by a guessed visit count.
- The two accident dates merged into one, or the tool "resolving" the conflict.
- Export that includes something I dismissed or never reviewed.
- Losing my edits on refresh or export.

## 6. Vocabulary
med chron, treatment chronology, DOS (date of service), DOI/DOA (date of injury/accident), provider/facility, records received through, Bates/page cite, specials, billed vs paid, demand package, treatment section, gap in treatment, prior/pre-existing, aggravation, missed appointments, discharged / non-compliant, MMI, plan of care, "records request", Stowers demand, "the adjuster will say...".

## 7. How I review
1. Load the sample case exactly as a user would (paste or the load-sample control). Note how long processing takes.
2. Before looking at the tool's output, list from Appendix A what I expect: 9 records, the 73-day gap, the 01-09/01-19 conflict, two prior-condition mentions, $8,390 explicit, $185 rate unclear.
3. Go entry by entry: check date, provider, summary, excerpt against the raw record text. Mark any mismatch.
4. Go flag by flag: check evidence excerpts, check nothing expected is missing, check the 28-day interval is not flagged.
5. Check the charges table and the total; try to find where the $185 went.
6. Review the whole case keyboard-first: accept most, edit one summary (record 3), dismiss one flag. Time the full review.
7. Export; paste into a plain-text file under `artifacts/review-evidence/`; confirm the dismissed item is absent and my edit is present.
8. Refresh mid-review once and confirm my decisions persist (or note that they don't).
9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).

## 8. Calibration
- **blocker — PT total invented.** Evidence: charges table row "Capital PT — $2,220 (12 × $185)". Fix: list "$185 per visit — rate, visit count not stated; needs review"; total stays $8,390. Test: eval asserts no PT total and total = 8390.
- **major — Export has no citations.** Evidence: export line "Patient treated at Capital PT for neck pain." Fix: "2026-01-23 — Capital PT (initial evaluation): cervical ROM reduced approx. 40%; plan of care 12 visits. [Rec. 4]". Test: E2E asserts every exported line contains a date, provider, and record cite.
- **minor — No remaining count.** Evidence: review screen of 9 entries + 8 flags has no counter. Fix: sticky "11 of 17 reviewed".

## 9. Sources
- https://www.evenuplaw.com/guides/how-to-prepare-medical-chronology — EvenUp (vendor): chronology columns are source page, DOS, provider/facility, encounter, complaint, diagnoses, treatment, referrals; ends with a review checklist.
- https://www.evenuplaw.com/guides/what-is-a-medical-chronology/ — EvenUp: paralegal drafts, attorney reviews; demand medical facts must match the chronology; a bill without a matching note is a gap to flag.
- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor, 2026): common errors are entry-timestamp vs visit dates, copy-forward duplication, missing page/Bates cites, unflagged conflicting onset histories.
- https://davislaw.betterteam.com/personal-injury-litigation-paralegal-3 — Davis Law Firm (San Antonio) posting: PI paralegals summarize records, bills, and wage loss and build demand packages; Filevine preferred.
- https://www.builtinaustin.com/job/litigation-paralegal/11851661 — Brown Sims (Houston) posting: medical and billing chronologies are a core paralegal duty on the defense side too.
- https://nala.org/events/2025-11-24/?ical=1 — NALA CLE (Nov 2025): PI discovery guide for paralegals; organizing records for attorney and expert use.
- https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ — RMD Law (PI firm, 2026): no carrier publishes a gap threshold; delay-to-first-care, mid-treatment gaps, and early stopping are distinct.
- https://www.blackchapman.com/?p=396 — Black Chapman (PI firm) on Colossus: documented diagnoses per body part and objective findings drive valuation.
- Assumptions: Texas setting and Filevine are from the postings; the "Rec. N" cite format is our assumption because Appendix A records have no Bates numbers. Vendor and plaintiff-firm sources are advocacy, not neutral.

## 10. Limits
Do not opine on legal strategy (whether to disclose a gap in the demand — litigation-lead), clinical interpretation beyond reading the words (legal-nurse), code quality, or security. Do not judge visual design except where it slows verification.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:41.552Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/spec/REQUIREMENTS.md"
}
````

### User / tool · 2026-11-02T00:29:41.686Z

**tool result**
````
1	# REQUIREMENTS — Treatment Timeline prototype (Part 1)
2	
3	Owner: writer (T-013, revision 2). Source: Appendix A Part 1 (`spec/SPEC.md`), CONTRACT §5 (M1), §5.2, §8.2. Truth values: `spec/SAMPLE_CASE_TRUTHS.md`.
4	Design it must agree with: `docs/LLM_VS_CODE.md`, `memory/contracts/api.md`, `memory/DECISIONS.md` (ADR-003, 005, 009).
5	Every later card and eval cites an R-ID from this file. If a card can't name the R-ID it serves, the card is wrong or this file is.
6	
7	**User.** A paralegal at a personal-injury firm. She reviews rather than trusts. Every statement the tool makes must be checkable against its source (A-101: she builds the chronology, the attorney signs the letter).
8	
9	**Two outputs, kept apart.** The export has two blocks and they never mix:
10	1. **Treatment section (paste into letter)**: accepted entries and accepted charges. Nothing else.
11	2. **Internal review notes — do not send**: accepted flags, unclear amounts, damages mentions, bills to request, records left out, edits. Flags are what an adjuster would use against the client, so they never enter block 1.
12	
13	**Checkers.**
14	
15	| Checker | Meaning |
16	|---|---|
17	| **UT** | unit test under `tests/unit` (code only, no LLM) |
18	| **EV** | metric from `python -m evals.run` (golden set in `evals/golden/`, writes `evals/reports/latest.json`) |
19	| **E2E** | Playwright test under `tests/e2e` |
20	| **PR** | persona review file `reviews/<card>-<persona>.md`; pass = no blocker or major on that item |
21	| **INST** | `tools/install_test.sh` clean-clone timed run |
22	
23	Pass/fail wording is literal. "Pass" means the stated condition holds on every golden case unless one is named.
24	
25	---
26	
27	## 1. Must-haves
28	
29	### 1.1 Input
30	
31	| ID | Requirement | Pass / fail test | Checker |
32	|---|---|---|---|
33	| R-IN-1 | Accept records pasted as text. | Pasting the 9 sample records produces 9 timeline entries and the UI shows "9 records found" before any model call. Fail if the count is wrong or not shown. | E2E + UT (splitter; pieces concatenated equal the input) |
34	| R-IN-2 | Accept records uploaded as a `.txt` file. No PDF or OCR (non-goal 1). | Uploading `evals/golden/sample.txt` gives the same 9 entries as paste. A `.pdf` upload is refused with a plain message, not a crash. | E2E |
35	| R-IN-3 | Date parsing is code, from an explicit format list. A numeric date is **ambiguous** when its first two numbers are both 1–12 and differ (`04/05/2026`: April 5 or May 4). It is never guessed. | Golden `case_01_date_formats`: seven formats parse (ISO, `02/17/2026`, `Feb 24, 2026`, `3 March 2026`, `March 10th, 2026`, `03-17-26`, `3/25/26`); `04/05/2026` is `date_ambiguous`, keeps its raw string, and its entry carries date null. Fail on any silent guess. | UT + EV (`case_01`) |
36	| R-IN-4 | Input size is bounded; empty or oversize input fails visibly without calling the LLM. | Empty input and input over `limits.max_chars` each show an error state; the LLM call counter stays 0. | E2E + UT |
37	| R-IN-5 | **Dates to confirm.** An entry with an ambiguous or missing date is excluded from ordering and gap math, shown in a "Dates to confirm" group, and is `needs_review`. When she confirms a date it joins the timeline and gap math re-runs. A gap flag that touches an unconfirmed entry is `needs_review` (reason `ENDPOINT_NOT_VERIFIED`). | `case_01`: record 8 absent from gap table until confirmed; after confirming 2026-05-04 it appears in order and the 03-25 → 05-04 gap (40 days) is flagged. | UT + E2E |
38	
39	### 1.2 Timeline
40	
41	An **entry** is one timeline row: date, provider, one-line summary, exact source excerpt.
42	
43	| ID | Requirement | Pass / fail test | Checker |
44	|---|---|---|---|
45	| R-TL-1 | Entries are chronological, one per distinct source record (see R-TL-7 for duplicates), each with date, provider, one-line summary and excerpt. | Sample case: 9 entries in date order, none of the four fields empty. Same-date records from different providers (records 1, 2) stay separate and keep source order (A-108). | UT + EV `entry_recall` |
46	| R-TL-2 | **Excerpt is verbatim and whole-sentence.** The excerpt is one or more complete sentences of its source record, a substring after whitespace normalization, never cut mid-sentence. | Grounding verifier passes every `verified` entry. An entry whose excerpt is not verbatim is `rejected`: shown only in the "could not verify" tray, never in the timeline or export. A mid-sentence excerpt is `needs_review`. | UT + EV `grounding_rate` |
47	| R-TL-3 | **Date of service is the record's header date, parsed by code.** Dates inside the body are facts for the conflict check, never the entry date. | Seeded test on **record 7**: header 2026-05-18, body "Date of accident per intake form: 2026-01-19". If the model returns 2026-01-19, the entry is `rejected` (`GROUNDING_DATE_MISMATCH`). Normal path: entry 7 dated 2026-05-18, sorted between entries 6 and 8. | UT + EV (`sample`) |
48	| R-TL-4 | **Summary adds nothing**: no fact, diagnosis, severity or causation absent from its excerpt. Judge #1 (faithfulness) checks every summary; `partially` or `unsupported` makes the entry `needs_review` with a one-sentence reason. | (a) Judge #1 returns `supported` on all 9 sample entries in each of 3 runs. (b) On the 20 seeded unsupported summaries in `evals/golden/hallucinations.jsonl` judge #1 flags at least 19 (≥ 95%; metric `hallucination_catch_rate`). (c) On the 5 faithful controls in `hallucinations_controls.jsonl` none returns `unsupported`. | EV |
49	| R-TL-5 | Every entry carries a state composed by code: `verified`, `needs_review`, `rejected` (ADR-005). `needs_review` sorts first in the review queue. | Unit tests cover the full composition table. E2E: a seeded `needs_review` entry appears above `verified` ones. | UT + E2E |
50	| R-TL-6 | "Why?" on every item shows the ladder record (generator output, code checks, judge verdict, state, backend) and the fixed-template one-sentence reason. | E2E: Why? on entry 7 shows check results and judge verdict; the audit record matches D.4 plus `backend`. | E2E |
51	| R-TL-7 | **Duplicate records are merged by code**: same date + same provider (case and whitespace normalized) + same normalized text → one entry citing every source record, shown with a visible "duplicate of record N" note. | `case_04_duplicates_no_amounts`: 6 records give 4 entries, E1 cites records 1 and 2, E2 cites 3 and 4. Fail if 6 entries, or if a merged entry cites one record. | UT + EV (`case_04`) |
52	| R-TL-8 | **A qualifier travels with its finding.** If a record contains a sentence matching the `hedge` category of `app/llm/lexicon.yaml` (for example "may represent", "correlate clinically"), any entry from that record includes that sentence in its excerpt, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Patient self-report phrases are not hedges and don't trigger this rule. | Golden assertions on `sample`: entry 8 excerpt contains `may represent degenerative change; correlate clinically`; entry 6 excerpt contains `after two missed appointments`. A seeded entry 8 with the shortened excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." is `needs_review`, not `verified`. | UT + EV |
53	| R-TL-9 | **Provider is verbatim from the record's source line.** The provider string must appear in the record's source/header line after normalization. | Seeded test: model returns "Capital Physical Therapy, LLC" for record 4 (source line "Capital PT, initial evaluation") → `rejected` (`GROUNDING_PROVIDER_NOT_IN_RECORD`, new code for the closed list). "Capital PT" passes. Counted in `grounding_rate`. | UT + EV |
54	
55	### 1.3 Review flags
56	
57	Four types: `gap`, `conflict`, `prior_condition`, `causation`. A gap is measured between consecutive dates of service across all providers (A-102). Every flag shows its evidence.
58	
59	| ID | Requirement | Pass / fail test | Checker |
60	|---|---|---|---|
61	| R-FL-1 | **Treatment gap.** Flag when days between consecutive dated entries is **greater than 30** (A-104). Arithmetic is code. Evidence is the two bounding entries (date, provider, excerpt). | Sample: flag 2026-03-06 → 2026-05-18, 73 days, citing entries 6 and 7. No flag on 2026-01-23 → 2026-02-20 (28 days). `case_02_gap_boundaries`: 29 and 30 do not flag, 31 does (3 flags, 4 near-misses). | UT (29/30/31) + EV `flag_*[gap]` |
62	| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**; (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
63	| R-FL-3 | **Prior / pre-existing conditions.** LLM classification plus lexicon scan; if only one fires, the flag is `needs_review` (`LEXICON_ONLY` or `LLM_ONLY`). | Sample must raise record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("degenerative change"). `case_06_subtle_pre_existing` is caught, and its 28-day near-miss does not flag. | EV `flag_*[prior_condition]` |
64	| R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. | Sample must raise records 8 ("may represent degenerative change; correlate clinically"), 6 (discharge after two missed appointments), 9 (patient self-report), 7 ("New onset" after the 73-day gap; wrong accident date). Golden `must_not` M1–M13 all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
65	| R-FL-5 | Every flag cites verbatim excerpt(s) that pass the grounding check. An ungrounded flag is `rejected`. | Verifier test on flags, same as R-TL-2. | UT + EV `grounding_rate` |
66	| R-FL-6 | Flags are grouped by type; each shows its state and, when `needs_review`, a one-sentence reason. | E2E: four groups; the sample shows at least one flag in each. | E2E |
67	| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". The tool never presents it as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
68	
69	### 1.4 Billed charges
70	
71	| ID | Requirement | Pass / fail test | Checker |
72	|---|---|---|---|
73	| R-CH-1 | List **every dollar amount** found, each with source record and verbatim excerpt. Extraction is code (currency pattern, money as whole cents). Noisy forms (`$1,2OO`) are listed as `unclear` with no value, never corrected. | Sample lists $6,240, $185, $2,150 and nothing else. `case_03_rate_and_ocr`: `$1,2OO` and `$9S.00` are `unclear`, value null. Amount recall ≥ 95% over `required` golden amounts. | UT + EV `amount_recall` |
74	| R-CH-2 | Each amount is classified `charge`, `rate`, `estimate`, `damages` or `unclear` (golden classes). Code classifies by cue words first; the LLM only when code can't; judge #2 re-reads every LLM classification. | $6,240 and $2,150 → `charge`; $185 → `rate`; "missing 3 days of work" → `damages` (no value). A seeded rate marked `charge` is caught by judge #2. | UT + EV |
75	| R-CH-3 | **Total counts only accepted amounts of class `charge`.** The screen shows both "Accepted: $X" and "Pending review: $Y (N charges)" so a first-load $0 isn't read as "no charges". Rates, estimates, damages and unclear amounts are listed as "unclear — not totaled" and never added. | Sample: after accepting both, Accepted = **$8,390**, Pending = $0. Dismissing the ER charge drops Accepted to $2,150. $185 reads "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review". **No PT total is computed** (golden `must_not` M4: none of 1,665 / 2,220 / 1,480 / 10,055 / 10,610 / 9,870 appears). | UT (totals) + E2E + EV |
76	| R-CH-4 | Non-billing figures are not charges. "Rx cyclobenzaprine 10 mg" and other doses never appear as amounts. | Golden `must_not` M7: no amount valued 10, 35, 6, 7, 12, 40 or 2. | EV |
77	| R-CH-5 | Amounts always need an explicit accept, even when `verified`. | E2E: no amount reaches the letter or the total without an accept click. | E2E |
78	| R-CH-6 | **Duplicate charges are merged by code**: same date + provider + amount → one amount citing every source record, with a visible "duplicate of" note. The total can never count it twice. A "not a duplicate" action splits them and is logged. | Seeded unit test: the same $6,240 on 2026-01-09 from Central ER in two records → one amount, total after accept $6,240, not $12,480. | UT + E2E |
79	| R-CH-7 | **Reclassifying a charge** (edit) changes the class only; the amount and excerpt are immutable. A `rate` cannot be reclassified to `charge` (the fix for a rate is to request the itemized ledger). `unclear` or `estimate` → `charge` re-runs judge #2 and requires a confirmation. *(Writer's proposal; architect to confirm in the api edit rules.)* | UT: edit `value` → 422 `invalid_edit`; `rate` → `charge` → 422; `unclear` → `charge` triggers judge #2. | UT |
80	
81	### 1.5 Review step
82	
83	An **item** is an entry, a flag or a charge. Everything starts `pending`.
84	
85	| ID | Requirement | Pass / fail test | Checker |
86	|---|---|---|---|
87	| R-RV-1 | Each entry, flag and charge can be **accepted, edited or dismissed**. Nothing is accepted by default. | E2E matrix, six cells plus charges: {accept, edit, dismiss} × {entry, flag}, and {accept, edit (class), dismiss} × {charge}. Fresh load → all `pending`, letter block empty. | E2E |
88	| R-RV-2 | **What "edit" means, by type.** *Entry*: the summary text. Date, provider and excerpt are not editable. *Charge*: the classification only (R-CH-7). *Flag*: a reviewer note only; the quoted evidence, type and title are not editable. The original is kept. An edited item shows "edited" in the review UI and in the internal notes, never in the letter text. | E2E: edit entry 3's summary → "edited" label in the UI; letter text shows the new summary with its citation and no "edited" mark; internal notes list "entry 3 edited" with original and new text. UT: attempts to edit date, provider, excerpt, amount value or flag evidence → 422. | E2E + UT |
89	| R-RV-3 | **Edited text is re-checked.** Code checks that the edit adds no number or date absent from the excerpt; judge #1 re-runs against the excerpt. If code or judge objects, she sees the reason before accepting and must confirm "keep my wording"; the confirmation is logged and shown in the internal notes. | UT: summary edited to add "$9,000" → code warning. Seeded edit adding "herniation" → judge returns `partially`/`unsupported` → warning. The accept button needs the confirm in both cases. | UT + EV (judge) + E2E |
90	| R-RV-4 | Review is keyboard-drivable (accept / edit / dismiss / next) and usable at 375 px. | E2E completes the sample case by keyboard only. At 375 px no horizontal scroll and every action is reachable. | E2E |
91	| R-RV-5 | Dismissed items never export and are recoverable (reset) until export. A dismissed flag may carry an optional reason. | E2E: dismiss, reset, dismiss again → absent from both blocks except the internal-notes "dismissed" list. | E2E |
92	| R-RV-6 | No LLM output is auto-accepted. Instruction-like text inside a record is treated as record text only. | Golden `case_07_prompt_injection`: the record produces an ordinary entry with an `INJECTION_SUSPECTED` warning, `needs_review`; no flag changes state; the injected `$50,000` is never totaled (total stays $420). | EV + PR (privacy-compliance) |
93	| R-RV-7 | **Batch accept** (keyboard command). Accepts every entry that is `verified` in the current view, after a confirmation that states the count. It never accepts amounts, flags or any `needs_review` item. One batch action is logged in the audit with the item IDs. *(Needs an ADR-005 amendment: today's api.md has no bulk endpoint.)* | E2E: seed 9 entries (7 verified, 2 needs_review) → batch accepts 7; amounts and flags stay `pending`; audit shows one batch event with 7 IDs. | E2E + UT |
94	| R-RV-8 | **Decisions survive a reload.** Accept, edit, dismiss, notes and batch actions persist (SQLite) and restore on reload or reopen of the case. | E2E: accept 3 items, edit 1, reload → same statuses and the same Accepted total. | E2E |
95	| R-RV-9 | **Open the full source record from any item.** Entries, flags (both records for a two-record flag) and charges open the full record text with the excerpt highlighted, in a modal or panel. The highlight range comes from code offsets, not the model. If the offset can't be found, the item drops to `needs_review` and the UI says so. This is core; only the side-by-side layout is the stretch (section 4). | E2E: from entry 8 open the record → the highlighted span equals the excerpt string. From the 73-day gap flag, records 6 and 7 both open. UT with a mutated record: offset lookup fails → `needs_review`. | E2E + UT |
96	
97	### 1.6 Export
98	
99	Both blocks are assembled by code from items with `review_status` in {accepted, edited}. API: `GET /api/cases/{id}/export` returns `letter_text` and `internal_notes_text` separately.
100	
101	| ID | Requirement | Pass / fail test | Checker |
102	|---|---|---|---|
103	| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted charges only. **No flag text of any kind** appears in it. | E2E: accept all 9 entries, both charges and all flags. Assert `letter_text` contains none of: "REVIEWER NOTE", any flag type label or title, "73 days", "low back pain", "intake form", "2026-01-19". UT: the letter builder has no flags parameter. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
104	| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
105	| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
106	| R-EX-4 | **Internal review notes — do not send** contain, in this order: accepted flags with their evidence and record numbers; dismissed flags with any reason; amounts not totaled (rate, estimate, unclear) worded as an action ("request itemized ledger"); damages mentions that aren't charges (for example "Patient reports missing 3 days of work", record 5) with their excerpt; **bills to request** (providers with a treatment entry in the records but no accepted charge); items edited, with original and new text and any "keep my wording" confirmation; pending items not included. | Sample, everything accepted: the notes list the gap, both conflicts, both prior mentions, the causation flags; "rate $185/visit; visit count not stated (12 planned; discharged at visit 9) — request itemized PT ledger"; the record 5 damages mention; bills to request for Austin EMS, Dr. Alvarez, Hill Country Pain Management and Capital PT itemization. | UT + E2E |
107	| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter". The count line is part of neither block. | E2E: click Copy for each block, read clipboard, assert no count line; assert counts on screen match. | E2E |
108	| R-EX-6 | **Template and worked example.** The letter block follows the template in section 6, in US long dates ("January 9, 2026"), with a source line per entry and an exhibit/Bates placeholder `[Ex. __ / Bates __]` she fills in after pasting. Internal record numbers appear in the internal notes only. The full expected export for the sample case is checked in as `evals/golden/sample.export.expected.txt` (a qa card). | E2E: with all 9 entries and both charges accepted and nothing edited, `letter_text` equals the golden file byte for byte. | E2E + UT |
109	| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → notes list record 5 (dismissed) and record 6 (not reviewed); the on-screen count reads "7 of 9". | E2E |
110	| R-EX-8 | **The total line is labeled.** The letter's total reads "Billed charges stated in these records: $X". When the case holds any rate, estimate or unclear amount, code appends "(excludes <provider> — <reason>)"; on the sample: "(excludes physical therapy — per-visit rate only, visit count not stated)". Never "Total" alone. `<service>` comes from a fixed code lookup (PT → physical therapy); an unknown service falls back to the provider name as written. | Sample: line equals `Billed charges stated in these records: $8,390 (excludes physical therapy — per-visit rate only, visit count not stated)`. A case with no non-charge amounts has no parenthetical. | UT + E2E |
111	| R-EX-9 | Two separate copy buttons, one per block, each copying exactly that block. | E2E: clipboard after each click equals the matching API field. | E2E |
112	
113	---
114	
115	## 2. Constraints
116	
117	| ID | Requirement | Pass / fail test | Checker |
118	|---|---|---|---|
119	| R-CO-1 | **LLM used for at least one step, and the line is documented.** `docs/LLM_VS_CODE.md` has the §5.2 table and matches the code. | Staff-engineer review checks each pipeline step against the table. UT: gap, total, date-parse, dedupe and export modules import no LLM client. | PR (staff-engineer) + UT |
120	| R-CO-2 | **Validation ladder on every LLM-derived item**: code check → independent judge (own prompt, preferably another model) → human accept/edit/dismiss. Nothing LLM-made reaches an export block without all three. | Audit record (D.4) exists for each LLM-derived item. E2E: an LLM-derived item with no human action is absent from both export blocks. | UT + E2E |
121	| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case the golden `must_not` list M1–M13 holds, including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident dates not merged; "concussion without loss of consciousness" kept as written. Any hit is a blocker. | EV (negative assertions) + PR (claims-adjuster) |
122	| R-CO-4 | **Runs from a link or from the repo in under 5 minutes.** The public link works without a key in demo mode (cached sample output, A-002). | `tools/install_test.sh`: clean clone to first screen with the sample loaded < 300 s. The public link opens with no login. | INST + PR (installer-reviewer) |
123	| R-CO-5 | **Synthetic data only**, shown on screen. | Banner "Synthetic data only — never paste real records" on every view (E2E). `python tools/check_secrets.py` passes. | E2E + UT |
124	| R-CO-6 | **Model and backend are swappable by config** (`claude-cli`, `anthropic-api`, `fixture`). A backend or prompt change requires an eval re-run with the report attached. | Unit tests run on `fixture` with no key. Handoff of any prompt/model change links an `evals/reports/*.md`. | UT + board check |
125	| R-CO-7 | **Determinism across 3 runs of the sample case.** *Code outputs identical*: record split, parsed dates, entry-ID set, gap flags, amount list and classes from code, totals. *LLM-derived item states must match*: every entry, amount and flag has the same state (`verified`/`needs_review`/`rejected`) in all 3 runs. *Flags are compared by (type, set of cited record IDs, evidence excerpt)*; the three runs must produce the same flag set. Summary wording may differ but must be `supported` in every run. | `determinism_3run` = 1.0 on `sample`; any difference fails and the report lists it. Other golden cases are reported, not gated. | EV |
126	| R-CO-8 | **Time-box and say what was cut.** | `memory/SCOPE_CUTS.md` has an entry for every non-goal in section 5 and for the stretch if cut; the product note's "cut" section matches it. | PR (product-manager) |
127	| R-CO-9 | Retries: max 2, with changed conditions; failure is visible. | UT: LLM call fails twice → item shown as "could not process" with the reason (`LLM_FAILED_AFTER_RETRIES`); the app stays usable. | UT |
128	
129	---
130	
131	## 3. Part 1 submission items
132	
133	| ID | Requirement | Pass / fail test | Checker |
134	|---|---|---|---|
135	| R-SU-1 | Prototype link or repo with run instructions. README has a timed run path. | See R-CO-4. | INST |
136	| R-SU-2 | Demo ≤ 3 minutes, or annotated screenshots. Screenshots cover each of these states: input, processing, timeline with `needs_review` first, flags panel, charges with the unclear tray, edit with warning, source-record view, export (both blocks), "could not verify" tray, error/empty input. | `artifacts/demo.webm` duration ≤ 180 s (ffprobe). `artifacts/CAPTIONS.md` has one caption per listed state. | qa check |
137	| R-SU-3 | One-page product note. Checklist: the 7 required contents are present as headings (problem and user; what was built; what was cut and why; ship bar with 3–5 testable criteria, how tested, what was found; where AI can fail and how design handles it; model/code split; three metrics, each with a "tells you" line); exactly 3 post-launch metrics; renders to 1 page (≤ 650 words). Numbers in the note equal the latest eval report. | Checklist run by the writer self-check, then PR (hiring-panel, product-manager). | PR |
138	| R-SU-4 | **Which AI tools, and the prompts, unedited.** `submission/prompt-log/TOOLS.md` names tools, models and how the team was organized. The transcript export is produced by `tools/export_prompt_log.py` with no manual edits, plus a two-paragraph reading guide. | Re-run the exporter into a temp dir; `diff` against the submitted files is empty. `TOOLS.md` exists and names the tools and models. | qa check + PR (hiring-panel) |
139	| R-SU-5 | **Assumptions stated, links open.** The product note links the assumptions (A-101 to A-108 and any added); every link in the email draft opens without requesting access. | Checklist: note references `memory/ASSUMPTIONS.md` content; qa opens each submitted link in a logged-out browser. | PR + qa check |
140	
141	---
142	
143	## 4. Stretch pick: side-by-side source viewer
144	
145	**Chosen.** The two-pane layout. Left, the item queue. Right, the full source record, always visible, scrolled to the highlighted excerpt as she moves through the queue. Opening the full record (modal or panel, highlight by code offsets) is already core (R-RV-9), so what the stretch adds is the layout that removes the open-and-close step.
146	
147	**Why (3 lines).**
148	1. The spec says she "reviews rather than trusts." Each claim sits next to its context, with no extra click per item, which is what 20-odd decisions per case need.
149	2. A quote can mislead by omission (the MRI line without its hedge). R-TL-8 stops the tool from dropping the hedge; the viewer lets her see the rest of the record anyway.
150	3. It is cheap: the highlight range already comes from the grounding check, so there is no new LLM step.
151	
152	**Why not the others.** PDF upload puts unverifiable extraction upstream of the grounding check. The confidence indicator already ships as `verified / needs_review / rejected`. A firm-voice paragraph is generated prose that would need its own verification.
153	
154	**Cut rule.**
155	- **Start** only when every M3 must-have card is done with no open blockers, and M3 is inside its 3.5 h budget. The stretch is built before the M3 gate so the gate reviews it.
156	- **Stop** at 45 minutes, or when the M3 gate is due, whichever comes first.
157	- **Fallback (one):** cut it entirely. The core record modal from R-RV-9 stays and nothing else changes. Log the cut in `memory/SCOPE_CUTS.md`.
158	
159	| ID | Requirement | Pass / fail test | Checker |
160	|---|---|---|---|
161	| R-ST-1 | At viewport ≥ 1024 px the source record sits beside the queue; selecting an item scrolls the record to its highlighted excerpt without opening a modal. Below 1024 px it falls back to the R-RV-9 modal. | E2E at 1280 px: step through three items by keyboard; the record pane updates each time and the highlighted span equals the excerpt. At 375 px the modal opens instead. | E2E |
162	
163	---
164	
165	## 5. Non-goals
166	
167	These are out on purpose. The orchestrator logs each in `memory/SCOPE_CUTS.md` with the reason.
168	
169	1. **PDF upload and OCR.** Text only. Extraction errors would sit upstream of the grounding check. Pasted PDF text with page headers is a chaos-test input, not a feature.
170	2. **Multi-case and matter management.** One case at a time, no search across cases.
171	3. **Accounts, auth, roles, sharing.** One anonymous session.
172	4. **Real data or PHI handling.** Synthetic only. No HIPAA, retention or BAA claim. The privacy review checks the design for what a real build would need; the prototype doesn't implement it.
173	5. **Drafting demand-letter prose in a firm's voice.** Export is a structured treatment section from accepted items. No generated narrative, no advocacy language.
174	6. **Medical or legal judgment.** No diagnosis, severity rating, causation opinion or statement of what a record "means." Flags point at the record's own words.
175	7. **Billing analysis.** No PT total from a rate, no reasonableness of charges, liens, insurance adjustments or paid-vs-billed.
176	8. **Integrations.** No EHR, case-management or document-system connectors, no email intake.
177	9. **Per-user learning.** Dismissals are logged for metrics, not fed back into prompts.
178	10. **Numeric confidence scores.** Three states only. A made-up percentage implies precision we can't verify.
179	11. **Non-English records and handwriting.** The chaos test confirms a clear failure message, not support.
180	12. **Exhibit and Bates numbering.** The export carries an `[Ex. __ / Bates __]` placeholder she fills in; the tool assigns no numbers.
181	13. **Manually adding an entry for a record the pipeline rejected.** The record stays visible in the "could not verify" tray; she writes that entry herself (SCOPE_CUTS 12).
182	14. **Batch accept of anything but verified entries.** Amounts, dates-to-confirm and flags always take an individual decision (R-RV-7).
183	
184	---
185	
186	## 6. Export template and worked example (R-EX-6)
187	
188	Sample case, all 9 entries and both charges accepted, nothing edited. Summaries are one line, written from the excerpt only. Dates are US long form in the export; the UI and API keep ISO. `[Ex. __ / Bates __]` is literal text.
189	
190	**Block 1 — Treatment section (paste into letter)**
191	
192	```
193	TREATMENT CHRONOLOGY
194	
195	January 9, 2026 — Austin EMS
196	Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; alert and oriented; transported to Central ER.
197	Source: Austin EMS run report, January 9, 2026 [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
198	
199	January 9, 2026 — Central ER
200	Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
201	Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
202	
203	January 16, 2026 — Dr. Alvarez
204	Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
205	Source: Dr. Alvarez, primary care, January 16, 2026 [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
206	
207	January 23, 2026 — Capital PT
208	Initial evaluation: cervical range of motion reduced approx. 40%; plan of care 12 visits.
209	Source: Capital PT, initial evaluation, January 23, 2026 [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
210	
211	February 20, 2026 — Capital PT
212	Visit 8: pain 4/10, improving.
213	Source: Capital PT, visit 8, February 20, 2026 [Ex. __ / Bates __]: "Pain 4/10, improving."
214	
215	March 6, 2026 — Capital PT
216	Visit 9: discharged from physical therapy after two missed appointments; pain 3/10.
217	Source: Capital PT, visit 9, March 6, 2026 [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."
218	
219	May 18, 2026 — Hill Country Pain Management
220	New patient: new onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
221	Source: Hill Country Pain Management, new patient, May 18, 2026 [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
222	
223	May 29, 2026 — Austin Imaging
224	Cervical MRI: C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
225	Source: Austin Imaging, cervical MRI, May 29, 2026 [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
226	
227	June 12, 2026 — Hill Country Pain Management
228	Follow-up: cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
229	Source: Hill Country Pain Management, follow-up, June 12, 2026 [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
230	
231	BILLED CHARGES
232	
233	Central ER, January 9, 2026 ........ $6,240.00
234	Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]: "ER charges: $6,240."
235	Austin Imaging, May 29, 2026 ....... $2,150.00
236	Source: Austin Imaging, cervical MRI, May 29, 2026 [Ex. __ / Bates __]: "Charge: $2,150."
237	
238	Billed charges stated in these records: $8,390 (excludes physical therapy — per-visit rate only, visit count not stated)
239	```
240	
241	**Block 2 — Internal review notes — do not send**
242	
243	```
244	INTERNAL REVIEW NOTES — DO NOT SEND
245	
246	FLAGS ACCEPTED
247	- Gap: 73 days, March 6, 2026 (Capital PT, record 6) to May 18, 2026 (Hill Country Pain Management, record 7).
248	- Conflict, accident date: records 1 and 2 show treatment on January 9, 2026; record 7: "Date of accident per intake form: 2026-01-19."
249	- Conflict, PT plan: record 4 "Plan of care: 12 visits"; record 6 "Discharged from PT after two missed appointments."
250	- Prior condition: record 3 "Patient reports low back pain in 2023, resolved."; record 8 "Findings may represent degenerative change".
251	- Causation language: record 8 "may represent degenerative change; correlate clinically"; record 6 "Discharged from PT after two missed appointments."; record 9 "Patient states symptoms began after the January collision." (patient self-report); record 7 "New onset pain".
252	
253	FLAGS DISMISSED
254	- none
255	
256	AMOUNTS NOT TOTALED
257	- Capital PT, record 4: "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
258	
259	DAMAGES MENTIONS (not charges)
260	- Record 5: "Patient reports missing 3 days of work."
261	
262	BILLS TO REQUEST (treatment in the records, no charge stated)
263	- Austin EMS (record 1); Dr. Alvarez (record 3); Hill Country Pain Management (records 7, 9); Capital PT itemization (records 4, 5, 6).
264	
265	RECORDS NOT IN THE TREATMENT SECTION
266	- none (9 of 9 records included)
267	
268	EDITED ITEMS
269	- none
270	
271	PENDING ITEMS NOT INCLUDED
272	- none
273	```
274	
275	If entry 5 were dismissed: the letter skips February 20, and "RECORDS NOT IN THE TREATMENT SECTION" reads "Record 5 — dismissed." The chronology never silently closes up.
276	
277	---
278	
279	## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
280	
281	These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.
282	
283	| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
284	|---|---|---|---|---|---|
285	| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
286	| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
287	| 3 | **Flags** | Per flag type (gap, conflict, prior_condition, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
288	| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% (≥ 19 of the 20 in `hallucinations.jsonl`). | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-CH-2, R-CO-3, R-CO-7 |
289	| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` ≥ 4 (named in the paralegal reviewer brief); `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag text; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-9, R-EX-1 to R-EX-9 |
290	
291	Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
292	
293	Rule for the product note: report what the eval **found**, including misses, not just the targets.
294	
295	---
296	
297	## 8. Assumptions this depends on
298	
299	Live list: `memory/ASSUMPTIONS.md`.
300	
301	| Ref | Assumption | Requirements that break if it's wrong |
302	|---|---|---|
303	| A-001 / A-002 | Dev runs on `claude-cli`; reviewers get demo mode with cached sample output and no key. | R-CO-4, R-CO-6 |
304	| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1 |
305	| A-102 | A gap is measured between consecutive dates of service across all providers. | R-FL-1 |
306	| A-103 | The chronology feeds the medical-treatment section of a pre-suit demand letter to a carrier. | R-EX-1 to R-EX-8 |
307	| A-104 | "Longer than 30 days" is strict: 30 is not a gap, 31 is. | R-FL-1 |
308	| A-105 | Each pasted record carries its date and source on its first line or table row; undated records go to `date_ambiguous`. | R-IN-3, R-IN-5, R-TL-3 |
309	| A-106 | The export cites by source label and date with an exhibit/Bates placeholder; the tool assigns no Bates numbers. *(Round 2 changes the stand-in from "record number" to source label + date; internal record numbers stay in the notes only. Orchestrator to update A-106.)* | R-EX-2, R-EX-6 |
310	| A-107 | A per-visit rate is not billable until visits are itemized, so no PT total is shown. | R-CH-2, R-CH-3, R-EX-8 |
311	| A-108 | Same-day records from different providers stay separate entries. | R-TL-1, R-TL-7 |
312	
313	**Proposed additions** (orchestrator decides):
314	- The date of service is the record's header date. Body dates are conflict evidence only (R-TL-3).
315	- Accepting a flag means "I've seen it and it's real," not "send it to the carrier." Flags go to internal notes only (ADR-009; R-EX-1).
316	- Numeric dates whose first two numbers are both 1–12 and differ are ambiguous, even though Texas records are normally month/day; she confirms once per date (R-IN-3). Whether to infer a per-packet convention is deferred.
317	- Providers with treatment in the records but no stated charge are "bills to request" (R-EX-4).
318	
319	**Design conflicts to reconcile.** These requirements follow the orchestrator's round-2 decisions; where they differ from the architect's committed text, the architect or backend updates it by card:
320	- `api.md` allows editing entry `provider` and `date`, and flag `title` and `explanation`. R-RV-2 says entry summary only, charge class only, flag note only.
321	- `api.md` says "no bulk-accept endpoint exists on purpose"; R-RV-7 adds a constrained batch accept.
322	- `api.md` and ADR-009 list accepted rates under the letter's "not included in total" heading; R-EX-4 and R-EX-8 move rates and other non-charge amounts to the internal notes. `cite=short` with a record number is the API default; R-EX-6 needs the quote and source label in the letter.
323	- Reason codes `EXCERPT_OMITS_QUALIFIER` and `GROUNDING_PROVIDER_NOT_IN_RECORD` are new; flag `source_kind` is new; amount class `damages` replaces `other`.
324	
325	## 9. Traceability pointers
326	
327	- LLM/code table and ladder: `docs/LLM_VS_CODE.md`. Names used here: generator, judge #1 faithfulness, judge #2 amount classification, judge #3 conflict, states `verified | needs_review | rejected`.
328	- Golden set: `evals/golden/` (qa). Expected values: `spec/SAMPLE_CASE_TRUTHS.md`. Every metric above must be computable from it.
329	- Cards cite R-IDs in their AC text. `evals.run` report rows carry the R-ID next to each metric.
330	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:44.111Z

Now the sample records, the lexicon `hedge` category R-TL-8 depends on, and the golden fixtures the tests cite.

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:45.547Z

**tool call — Bash**
````
{
 "command": "cat -n evals/golden/sample.txt; echo ====; grep -n -A40 '^  *hedge\\|^hedge' app/llm/lexicon.yaml | head -80; echo ===; grep -n 'category\\|^[a-z_]*:' app/llm/lexicon.yaml | head -40",
 "description": "Read sample case and lexicon hedge category"
}
````

### User / tool · 2026-11-02T00:29:45.649Z

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
====
===
18:version: 1
19:flag_types: [pre_existing, causation_weakening, compliance]
21:negation:
39:entries:
693:sources:
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:48.439Z

<details><summary>thinking</summary>

The rule R-TL-8 refers to a "hedge" lexicon category, but the lexicon's flag_types don't include it. I'm searching for "hedge" across the project and checking how "may represent" and "missed appointments" are classified.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:29:49.553Z

**tool call — Bash**
````
{
 "command": "grep -n -i 'hedge' app/llm/lexicon.yaml | head; echo \"hedge hits: $(grep -ci hedge app/llm/lexicon.yaml)\"; sed -n 15,60p app/llm/lexicon.yaml; grep -n -i -B2 -A8 'may represent\\|correlate clinically\\|missed appointment' app/llm/lexicon.yaml | head -70",
 "description": "Search lexicon for hedge category and key phrases"
}
````

### User / tool · 2026-11-02T00:29:49.662Z

**tool result**
````
286:  rationale: 'Possibility language. Texas causation requires reasonable medical probability; "may" signals possibility, and the defense reads "may represent degenerative change" as an alternative cause. Keep the hedge verbatim.'
288:  false_positive: '"May return to work" / "may follow up" are permissions, not hedges — they do not match because a diagnostic verb is required.'
300:  source: 'AA A5; AA src 7 (radiology: "clinical correlation" as hedge), src 8; Appendix C record 8'
314:  false_positive: 'Plans ("possible ESI if no improvement") are about treatment, not causation — LLM checks whether the hedge attaches to a diagnosis or cause. Medium strength for that reason.'
325:  rationale: 'Radiology hedge: the finding is possible but unconfirmed; defense cites it to show uncertainty.'
hedge hits: 5
#   but be suppressed by the negation guard. Run `.venv/bin/python research/lexicon_selfcheck.py`.
# - Overlapping hits on the same span (e.g. "resolved" via two entries) are deduped by code per (span, flag_type).

version: 1
flag_types: [pre_existing, causation_weakening, compliance]

negation:
  # NegEx-style guard (Chapman et al. 2001; ConText/pyConText, Chapman et al. 2011 — see sources at bottom).
  # A pre-cue within `window_tokens` tokens BEFORE the hit, in the same sentence, with no terminator between,
  # negates the hit. Post-cues within the window AFTER the hit also negate.
  window_tokens: 6
  pre_cues: ['no', 'not', 'denies', 'denied', 'deny', 'negative for', 'no history of', 'no prior', 'no previous',
             'no known', 'no evidence of', 'without', 'free of', 'never', 'absence of', 'rules out', 'ruled out']
  post_cues: ['denied', 'ruled out', 'is absent', 'was absent', 'not seen', 'not present']
  terminators: ['but', 'however', 'although', 'though', 'except', 'aside from', 'apart from', 'which', ';']
  pseudo_negations: ['no increase', 'no change', 'not only', 'not necessarily', 'no significant change',
                     'cannot be excluded', 'can not be excluded', 'cannot exclude', 'not ruled out',
                     'cannot be ruled out', 'no further', 'did not show', 'did not attend', 'did not return',
                     'not complian', 'non-complian', 'not doing', 'not performing', 'not related']
  note: >
    Pseudo-negations are phrases containing a negation word that do NOT negate a finding (they are themselves
    hits or neutral). "no change from prior" still implies a prior study. The guard never applies to
    compliance entries whose meaning is already negative ("did not attend").

entries:

# ───────────────────────── pre_existing ─────────────────────────

- id: prior_history_year_resolved
  pattern: '\b(?:19|20)\d{2}\b\s*[,;:-]?\s*(?:now\s+|since\s+|which\s+(?:has\s+)?|and\s+(?:has\s+)?)?(?:fully\s+|completely\s+)?(?:resolved|healed|recovered)\b'
  flag_type: pre_existing
  strength: high
  negatable: false
  rationale: >
    A dated prior condition described as resolved ("low back pain in 2023, resolved") is still a documented
    prior condition; adjusters and ISO ClaimSearch hunt for exactly these, and concealment costs credibility.
    "Resolved" helps the claimant, but the paralegal must see it and decide relevance (different body region here).
  source: 'AA A3; AA src 2 (Verisk ISO ClaimSearch), src 15; Appendix C record 3'
  false_positive: >
    The year may be the accident year or later (e.g. "headache 2026, resolved" after the crash) — code must
    compare the year with the earliest accident date and drop hits whose year >= accident year from pre_existing
    (they may still matter as "recovery" context).
  appendix_c: [3]
  examples:
    hit: ['Patient reports low back pain in 2023, resolved.', 'neck strain 2019 - fully resolved']
    miss: ['Seen 2026-01-16 for neck pain.', 'Symptoms improving since visit 3.']
192-  appendix_c: [8]
193-  examples:
194:    hit: ['Findings may represent degenerative change', 'mild disc degeneration at C5-C6', 'DDD L4-5']
195-    miss: ['generated report']
196-    negated: ['No degenerative change identified.']
197-
198-- id: degenerative_imaging_terms
199-  pattern: '\b(?:spondylo(?:sis|tic)|osteoarthrit\w*|arthropath\w*|osteophyt\w*|desiccat\w*|uncovertebral\s+(?:joint\s+)?hypertroph\w*|facet\s+(?:joint\s+)?(?:hypertroph\w*|arthropath\w*|arthros\w*)|endplate\s+(?:changes?|sclerosis)|Modic\s+(?:type\s+)?[123I]+|loss\s+of\s+disc\s+height|disc\s+space\s+narrowing)\b'
200-  flag_type: pre_existing
201-  strength: high
202-  negatable: true
--
284-  strength: high
285-  negatable: false
286:  rationale: 'Possibility language. Texas causation requires reasonable medical probability; "may" signals possibility, and the defense reads "may represent degenerative change" as an alternative cause. Keep the hedge verbatim.'
287-  source: 'AA A5; AA src 11 (Jelinek v. Casas), src 7, src 8; Appendix C record 8'
288-  false_positive: '"May return to work" / "may follow up" are permissions, not hedges — they do not match because a diagnostic verb is required.'
289-  appendix_c: [8]
290-  examples:
291:    hit: ['Findings may represent degenerative change; correlate clinically.', 'may be related to the prior injury']
292-    miss: ['May return to work Monday.', 'may follow up as needed']
293-
294-- id: correlate_clinically
295-  pattern: '\bcorrelate\s+clinically\b|\bclinical(?:ly)?\s+correlat\w*|\bcorrelation\s+with\s+(?:clinical|symptoms|exam)'
296-  flag_type: causation_weakening
297-  strength: high
298-  negatable: false
299-  rationale: 'The radiologist declines to tie the finding to symptoms and hands interpretation to the clinician; it is not a causation opinion and defense treats it as equivocal.'
--
302-  appendix_c: [8]
303-  examples:
304:    hit: ['correlate clinically', 'Clinical correlation recommended.', 'clinically correlate']
305-    miss: ['clinic visit scheduled']
306-
307-- id: possibility_terms
308-  pattern: '\b(?:possibl[ey]|could\s+(?:be|represent|reflect|indicate)|might\s+(?:be|represent|reflect)|perhaps|questionabl[ey]|cannot\s+say)\b'
309-  flag_type: causation_weakening
310-  strength: medium
311-  negatable: false
312-  rationale: 'Possibility/conjecture words. Texas courts treat "possibly"/"perhaps" opinions as conjecture, not reasonable medical probability.'
--
570-  appendix_c: [6]
571-  examples:
572:    hit: ['Discharged from PT after two missed appointments.', 'failed to attend 3 sessions', 'skipped follow-up']
573-    miss: ['Patient reports missing 3 days of work.']
574-    negated: ['Has not missed any sessions.']
575-
576-- id: no_show_cancel
577-  pattern: '\b(?:no-?\s?show(?:ed|s)?|NS\s+x\s?\d|DNKA|did\s+not\s+(?:show|attend|return|keep|present)|cancell?ed\s+(?:\w+\s+){0,2}(?:appointments?|appts?|visits?|sessions?)|rescheduled\s+(?:\w+\s+){0,2}times)\b'
578-  flag_type: compliance
579-  strength: high
580-  negatable: false
--
597-  appendix_c: [6]
598-  examples:
599:    hit: ['Discharged from PT after two missed appointments.', 'self-discharged from therapy', 'dismissed from the practice']
600-    miss: ['Central ER discharge summary', 'discharged home in stable condition']
601-
602-- id: noncompliance
603-  pattern: '\bnon-?\s?complian(?:t|ce)\b|\bnot\s+(?:being\s+)?complian(?:t|ce)\b|\bpoor\s+(?:compliance|adherence|attendance|follow-?\s?through)\b|\bnon-?\s?adheren(?:t|ce)\b'
604-  flag_type: compliance
605-  strength: high
606-  negatable: false
607-  rationale: 'Explicit provider statement of non-compliance; the strongest mitigation evidence.'
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:31.576Z

<details><summary>thinking</summary>

I'm checking the requirements' claims about the fixtures: the case_04 counts, the hallucination files, whether the export golden exists, and how api.md words flag titles. That last point bears on the overlap between R-EX-1 and R-TL-8.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:34.393Z

**tool call — Bash**
````
{
 "command": "ls evals/golden/ | grep -i export; echo \"export golden exists? rc=$?\"; wc -l evals/golden/hallucinations.jsonl evals/golden/hallucinations_controls.jsonl; grep -c '=== Record' evals/golden/case_04_duplicates_no_amounts.txt; python3 -c \"\nimport json;d=json.load(open('evals/golden/case_04_duplicates_no_amounts.expected.json'));print(list(d.keys()));e=d.get('entries') or d.get('timeline');print('entries',len(e) if e else None)\ns=json.load(open('evals/golden/sample.expected.json'));fl=s.get('flags');print('sample flags',len(fl));\n[print(f.get('type'),'|',f.get('title') or f.get('id'),'|',str(f.get('evidence') or f.get('excerpts'))[:110]) for f in fl]\"; grep -n -i 'title' memory/contracts/api.md | head -15; sed -n 180,192p app/llm/lexicon.yaml; sed -n 276,284p app/llm/lexicon.yaml",
 "description": "Verify golden fixtures, flag titles, lexicon ids"
}
````

### User / tool · 2026-11-02T00:31:34.526Z

**tool result**
````
export golden exists? rc=1
      20 evals/golden/hallucinations.jsonl
       5 evals/golden/hallucinations_controls.jsonl
      25 total
6
['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated_flags', 'record_warnings', 'must_not', 'notes']
entries 4
sample flags 10
gap | G1 | [{'record_no': 6, 'field': 'excerpt', 'excerpt': 'Discharged from PT after two missed appointments'}, {'record
conflict | C1 | [{'record_no': 7, 'field': 'excerpt', 'excerpt': 'Date of accident per intake form: 2026-01-19'}, {'record_no'
conflict | C2 | [{'record_no': 4, 'field': 'excerpt', 'excerpt': 'Plan of care: 12 visits'}, {'record_no': 6, 'field': 'excerp
pre_existing | P1 | [{'record_no': 3, 'field': 'excerpt', 'excerpt': 'Patient reports low back pain in 2023, resolved'}]
pre_existing | P2 | [{'record_no': 8, 'field': 'excerpt', 'excerpt': 'Findings may represent degenerative change'}]
causation | K1 | [{'record_no': 8, 'field': 'excerpt', 'excerpt': 'may represent degenerative change; correlate clinically'}]
causation | K2 | [{'record_no': 6, 'field': 'excerpt', 'excerpt': 'Discharged from PT after two missed appointments'}]
causation | K3 | [{'record_no': 9, 'field': 'excerpt', 'excerpt': 'Patient states symptoms began after the January collision'}]
causation | K4 | [{'record_no': 7, 'field': 'excerpt', 'excerpt': 'New onset pain radiating to right arm'}]
causation | K5 | [{'record_no': 7, 'field': 'excerpt', 'excerpt': 'Date of accident per intake form: 2026-01-19'}]
120:    { "id": "f1", "type": "gap", "title": "Treatment gap of 73 days",
128:    { "id": "f2", "type": "conflict", "title": "Two different accident dates",
179:Allowed `edits` keys by item type: entry `summary`, `provider`, `date`; amount `kind` (the value and excerpt are immutable); flag `title`, `explanation`. Unknown or immutable keys return `422 invalid_edit`. Editing a date re-validates it as a real ISO date and re-sorts. `rejected` items return `409 item_rejected` for accept/edit (dismiss is allowed). Accepting is idempotent. `edit` implies accept: `review_status` becomes `edited` and the original is stored in `review_events`.
  examples:
    hit: ['exacerbation of underlying degenerative disease', 'aggravation of pre-existing cervical condition']
    miss: ['pain aggravated by turning head']

- id: degenerative
  pattern: '\bdegenerat(?:ive|ion)\b|\bDDD\b|\bDJD\b'
  flag_type: pre_existing
  strength: high
  negatable: true
  rationale: 'Degenerative findings are the most common defense explanation for spinal imaging; they are common in asymptomatic adults (Brinjikji 2015). The tool must surface them and never resolve them to "degenerative" or "traumatic".'
  source: 'AA A4; AA src 6 (Brinjikji, AJNR 2015), src 16; Appendix C record 8'
  false_positive: '"No degenerative change" negated by guard. Must not be paraphrased to a conclusion — the flag text quotes the record.'
  appendix_c: [8]
    hit: ['Comparison: MRI cervical spine 2021-03-04.', 'Unchanged from prior study.', 'no interval change from 2020']
    miss: ['Comparison: none.']

# ───────────────────────── causation_weakening ─────────────────────────

- id: may_represent
  pattern: '\bmay\s+(?:represent|reflect|indicate|suggest|be\s+(?:due\s+to|related\s+to|secondary\s+to|consistent\s+with|from|a\s+result\s+of))\b'
  flag_type: causation_weakening
  strength: high
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:40.166Z

<details><summary>thinking</summary>

The golden flag evidence strings (G1, K1, K2, K4, P2) seem to sit inside the §6 letter block. I'll verify that with checks on quote grounding, provider substrings, dates and the total.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:57.035Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-walk.py",
 "content": "\"\"\"T-013 round 2 (paralegal-reviewer): re-walk the 9 sample records through the §6 worked example.\n\nRead-only. Extracts Block 1 / Block 2 from spec/REQUIREMENTS.md, then checks:\n  1. every quoted excerpt in the letter is verbatim in evals/golden/sample.txt (whitespace-normalised)\n  2. every letter heading provider is a substring of its record's Source line (R-TL-9)\n  3. letter dates are non-decreasing and match header dates (R-TL-3, R-EX-3)\n  4. which golden flag evidence strings appear inside the letter block (R-EX-1 \"no flag text of any kind\")\n  5. R-EX-1's forbidden-string list against the letter\n  6. total arithmetic and the R-EX-8 total line\n\"\"\"\nimport json\nimport re\nfrom datetime import date, datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[2]\nreq = (ROOT / \"spec/REQUIREMENTS.md\").read_text().splitlines()\nsample = (ROOT / \"evals/golden/sample.txt\").read_text()\ngolden = json.loads((ROOT / \"evals/golden/sample.expected.json\").read_text())\n\n\ndef norm(s):\n    return re.sub(r\"\\s+\", \" \", s).strip()\n\n\n# --- extract the two fenced blocks in section 6 -------------------------------------------\nsec6 = req.index(next(l for l in req if l.startswith(\"## 6. Export template\")))\nfences = [i for i in range(sec6, len(req)) if req[i].startswith(\"```\")][:4]\nletter = req[fences[0] + 1:fences[1]]\nnotes = req[fences[2] + 1:fences[3]]\nprint(f\"letter block = REQUIREMENTS.md:{fences[0]+2}-{fences[1]}; notes block = :{fences[2]+2}-{fences[3]}\")\nletter_text = \"\\n\".join(letter)\n\n# --- records ---------------------------------------------------------------------------------\nrecs = {}\nfor m in re.finditer(r\"=== Record (\\d+) ===\\nDate: (\\S+)\\nSource: (.+)\\nExcerpt: \\\"(.+)\\\"\", sample):\n    recs[int(m.group(1))] = dict(date=m.group(2), source=m.group(3), text=m.group(4))\nprint(f\"records parsed: {len(recs)}\")\nall_text = norm(\" \".join(r[\"text\"] for r in recs.values()))\n\n# 1. grounding of every quoted excerpt in the letter\nprint(\"\\n[1] letter quotes verbatim in sample.txt\")\nquotes = re.findall(r'\\]: \"(.+)\"$', letter_text, flags=re.M)\nfor q in quotes:\n    print(f\"  {'OK ' if norm(q) in all_text else 'MISS'} {q[:70]}\")\n\n# 2/3. headings: '<Month D, YYYY> — <provider>'\nprint(\"\\n[2,3] headings: provider substring of Source line; date equals header; order\")\nheads = re.findall(r\"^([A-Z][a-z]+ \\d{1,2}, \\d{4}) — (.+)$\", letter_text, flags=re.M)\nprev = None\nfor (d, prov), (n, r) in zip(heads, sorted(recs.items())):\n    dd = datetime.strptime(d, \"%B %d, %Y\").date()\n    ok_p = norm(prov).lower() in norm(r[\"source\"]).lower()\n    ok_d = dd.isoformat() == r[\"date\"]\n    ok_o = prev is None or dd >= prev\n    prev = dd\n    print(f\"  rec {n}: {d:<18} {prov:<30} provider_in_source={ok_p} date_matches={ok_d} order_ok={ok_o}\")\nprint(f\"  headings={len(heads)}\")\n\n# 4. golden flag evidence present in letter block\nprint(\"\\n[4] golden flag evidence strings found INSIDE the letter block (R-EX-1 says 'no flag text of any kind')\")\nfor f in golden[\"flags\"]:\n    for ev in f.get(\"evidence\", []):\n        hit = norm(ev[\"excerpt\"]) in norm(letter_text)\n        print(f\"  {f['id']:<3} {f['type']:<13} rec {ev['record_no']} in_letter={hit}  \\\"{ev['excerpt']}\\\"\")\n\n# 5. R-EX-1 forbidden list (REQUIREMENTS.md:103)\nprint(\"\\n[5] R-EX-1 forbidden strings in letter\")\nfor s in [\"REVIEWER NOTE\", \"73 days\", \"low back pain\", \"intake form\", \"2026-01-19\", \"needs review\", \"edited\", \"Record \"]:\n    print(f\"  {s!r}: {'PRESENT' if s in letter_text else 'absent'}\")\n\n# 6. totals and gaps\nprint(\"\\n[6] arithmetic\")\namts = [int(a.replace(\",\", \"\")) for a in re.findall(r\"\\$([\\d,]+)\\.00$\", letter_text, flags=re.M)]\nprint(f\"  charge lines {amts} sum={sum(amts)}\")\nprint(\"  total line:\", [l for l in letter if l.startswith(\"Billed charges\")])\nds = [date.fromisoformat(r[\"date\"]) for _, r in sorted(recs.items())]\nprint(\"  gaps:\", [(ds[i + 1] - ds[i]).days for i in range(len(ds) - 1)])\n\n# 7. tool-authored (non-quoted, non-heading) text in the letter that is not in any record\nprint(\"\\n[7] letter lines that are tool-authored and contain words absent from the records\")\nfor l in letter:\n    if l.startswith(\"Billed charges\"):\n        extra = [w for w in [\"per-visit rate only\", \"visit count not stated\", \"excludes physical therapy\"] if w in l]\n        print(f\"  total line carries tool wording: {extra}\")\n\n# 8. notes block: citations with record number but no provider/date\nprint(\"\\n[8] notes lines citing 'record N' without provider or date\")\nfor l in notes:\n    if re.search(r\"record \\d\", l) and not re.search(r\"\\d{4}\", l):\n        print(\"  \", l[:110])\n"
}
````

### User / tool · 2026-11-02T00:31:57.123Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-walk.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:58.809Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-013-r2-paralegal-walk.py 2>&1 | tee artifacts/review-evidence/T-013-r2-paralegal-walk.out.txt",
 "description": "Run worked-example walkthrough checks"
}
````

### User / tool · 2026-11-02T00:31:58.915Z

**tool result**
````
letter block = REQUIREMENTS.md:193-238; notes block = :244-272
records parsed: 9

[1] letter quotes verbatim in sample.txt
  OK  41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/1
  OK  Dx: cervical strain; concussion without loss of consciousness. CT head
  OK  Persistent neck pain 6/10, daily headaches. Refer to physical therapy 
  OK  Cervical range of motion reduced approx. 40%. Plan of care: 12 visits.
  OK  Pain 4/10, improving.
  OK  Discharged from PT after two missed appointments. Pain 3/10.
  OK  New onset pain radiating to right arm with numbness in fingers. Pain 7
  OK  C5-C6 disc protrusion with mild right foraminal narrowing. Findings ma
  OK  Recommend cervical epidural steroid injection. Patient states symptoms
  OK  ER charges: $6,240.
  OK  Charge: $2,150.

[2,3] headings: provider substring of Source line; date equals header; order
  rec 1: January 9, 2026    Austin EMS                     provider_in_source=True date_matches=True order_ok=True
  rec 2: January 9, 2026    Central ER                     provider_in_source=True date_matches=True order_ok=True
  rec 3: January 16, 2026   Dr. Alvarez                    provider_in_source=True date_matches=True order_ok=True
  rec 4: January 23, 2026   Capital PT                     provider_in_source=True date_matches=True order_ok=True
  rec 5: February 20, 2026  Capital PT                     provider_in_source=True date_matches=True order_ok=True
  rec 6: March 6, 2026      Capital PT                     provider_in_source=True date_matches=True order_ok=True
  rec 7: May 18, 2026       Hill Country Pain Management   provider_in_source=True date_matches=True order_ok=True
  rec 8: May 29, 2026       Austin Imaging                 provider_in_source=True date_matches=True order_ok=True
  rec 9: June 12, 2026      Hill Country Pain Management   provider_in_source=True date_matches=True order_ok=True
  headings=9

[4] golden flag evidence strings found INSIDE the letter block (R-EX-1 says 'no flag text of any kind')
  G1  gap           rec 6 in_letter=True  "Discharged from PT after two missed appointments"
  G1  gap           rec 7 in_letter=True  "New onset pain radiating to right arm"
  C1  conflict      rec 7 in_letter=False  "Date of accident per intake form: 2026-01-19"
  C1  conflict      rec 1 in_letter=True  "rear-ended at approx. 35 mph"
  C1  conflict      rec 2 in_letter=True  "CT head negative"
  C2  conflict      rec 4 in_letter=True  "Plan of care: 12 visits"
  C2  conflict      rec 6 in_letter=True  "Discharged from PT after two missed appointments"
  P1  pre_existing  rec 3 in_letter=False  "Patient reports low back pain in 2023, resolved"
  P2  pre_existing  rec 8 in_letter=True  "Findings may represent degenerative change"
  K1  causation     rec 8 in_letter=True  "may represent degenerative change; correlate clinically"
  K2  causation     rec 6 in_letter=True  "Discharged from PT after two missed appointments"
  K3  causation     rec 9 in_letter=True  "Patient states symptoms began after the January collision"
  K4  causation     rec 7 in_letter=True  "New onset pain radiating to right arm"
  K5  causation     rec 7 in_letter=False  "Date of accident per intake form: 2026-01-19"

[5] R-EX-1 forbidden strings in letter
  'REVIEWER NOTE': absent
  '73 days': absent
  'low back pain': absent
  'intake form': absent
  '2026-01-19': absent
  'needs review': absent
  'edited': absent
  'Record ': absent

[6] arithmetic
  charge lines [6240, 2150] sum=8390
  total line: ['Billed charges stated in these records: $8,390 (excludes physical therapy — per-visit rate only, visit count not stated)']
  gaps: [0, 7, 7, 28, 14, 73, 11, 14]

[7] letter lines that are tool-authored and contain words absent from the records
  total line carries tool wording: ['per-visit rate only', 'visit count not stated', 'excludes physical therapy']

[8] notes lines citing 'record N' without provider or date
   - Conflict, PT plan: record 4 "Plan of care: 12 visits"; record 6 "Discharged from PT after two missed appoint
   - Causation language: record 8 "may represent degenerative change; correlate clinically"; record 6 "Discharged
   - Capital PT, record 4: "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharg
   - Austin EMS (record 1); Dr. Alvarez (record 3); Hill Country Pain Management (records 7, 9); Capital PT itemi
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:32:36.004Z

<details><summary>thinking</summary>

Mechanical checks passed: all 11 quotes are verbatim and the providers and dates match. But 8 of the 10 golden flags' evidence strings appear in the letter block, which breaks requirement R-EX-1, so I'm writing the resolution table next.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:32:58.012Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-resolution.md",
 "content": "# T-013 round 2: resolution of round-1 findings (paralegal-reviewer)\n\nReviewed: `spec/REQUIREMENTS.md` @ 64f766e (`git diff --stat 64f766e -- spec/REQUIREMENTS.md`: empty, rc=0). Line numbers below are from that file.\nWalk-through evidence: `artifacts/review-evidence/T-013-r2-paralegal-walk.py` → `T-013-r2-paralegal-walk.out.txt`.\n\n## Paralegal round 1 (reviews/T-013-paralegal.md)\n\n| # | Sev | Finding | Status | New lines / evidence |\n|---|---|---|---|---|\n| P1 | blocker | Accepted flags export into the letter text | **Resolved as worded** (two blocks, no flag notes, labels, titles or counts in the letter). **Residual → new major N1**: the evidence strings of 8 of 10 golden flags appear verbatim in the §6 letter block, contradicting \":103 No flag text of any kind\". | :9-11, R-EX-1 :103, R-EX-4 :106, R-EX-5 :107, R-EX-9 :111, §6 :190-273; walk.out [4] |\n| P2 | major | Excerpt can drop the hedge | **Partial.** Whole-sentence rule added (R-TL-2 :46) and R-TL-8 :52. But R-TL-8 triggers on \"the `hedge` category of `app/llm/lexicon.yaml`\", and that category does not exist (`flag_types: [pre_existing, causation_weakening, compliance]`, lexicon.yaml:19; \"hedge\" appears only in rationale text :286,288,300,314,325). The entry-6 assertion (\"after two missed appointments\") is a `compliance` entry, so it cannot follow from any hedge reading. → new major N2 | :46, :52; lexicon.yaml:19 |\n| P3 | major | Full source record was stretch only | **Resolved.** R-RV-9 is core, code offsets, all three item types, and a two-record flag opens both. | :95, :145, :157 |\n| P4 | major | No export template; record-number cite; ISO dates | **Resolved.** Template, long dates, `[Ex. __ / Bates __]`, record numbers in notes only, golden file named. `evals/golden/sample.export.expected.txt` not yet present (`ls evals/golden \\| grep export` → rc=1), which is acceptable because it is assigned to a qa card. | R-EX-6 :108, §6 :186-275, non-goal 12 :180 |\n| P5 | major | Unclear amounts / total wording undefined | **Resolved.** Accepted and pending shown, rate goes to notes as an action, total labeled. Residual wording issue → minor N4. | R-CH-3 :75, R-EX-4 :106, R-EX-8 :110, :238, :257 |\n| P6 | major | Edits under-specified | **Resolved.** Per-type edit rules, amount/date/excerpt immutable, original kept, judge re-run, \"edited\" never in letter. Residual: unclear → charge with null value → minor N5. | R-CH-7 :79, R-RV-2 :88, R-RV-3 :89 |\n| P7 | major | Provider not checked against record | **Resolved.** | R-TL-9 :53; walk.out [2]: 9/9 headings are substrings of Source lines |\n| P8 | major | Date of service not pinned; record-7 trap | **Resolved.** Header date by code; the seeded test now uses record 7. | R-TL-3 :47, :314; walk.out [3] |\n| P9 | major | No duplicate record/charge rule | **Resolved.** case_04: 6 records → `entries 4` in expected.json (verified). | R-TL-7 :51, R-CH-6 :78 |\n| P10 | major | Export doesn't disclose missing records | **Resolved.** | R-EX-7 :109, :265-266, :275 |\n| P11 | minor | Batch accept | Resolved | R-RV-7 :93, non-goal 14 :182 |\n| P12 | minor | Reload persistence | Resolved | R-RV-8 :94 |\n| P13 | minor | Lost wages had no home | Resolved | R-EX-4 :106, :259-260 |\n| P14 | minor | Bills to request | Resolved | R-EX-4 :106, :262-263 |\n| P15 | minor | Gap evidence / date_ambiguous | Resolved (gap cites bounding entries :61; ambiguity defined :35; tray :37). Residual noise of the rule → minor N6 | :35-37, :61 |\n| P16 | minor | Ship-bar key unnamed | Resolved | :289 `scores.verify_quickly`, `reviews/<card>-paralegal.md` |\n\n## Product-manager round 1 (reviews/T-013-product-manager.md) majors\n\n| # | Finding | Status | New lines |\n|---|---|---|---|\n| PM1 | \"edit each flag\" undefined; no action×item matrix | **Resolved.** 6 cells plus charge cells; per-type edit field | R-RV-1 :87, R-RV-2 :88, R-CH-7 :79 |\n| PM2 | What an accepted flag becomes in the letter | **Resolved as worded**, same residual as P1 → N1 | :9-11, :103, :106 |\n| PM3 | Stretch start condition unreachable | **Resolved** (start after M3 must-have cards done and within budget, built before the gate, one fallback). Scheduling is outside my lens; PM to confirm. | :154-157 |\n| PM4 | R-TL-4 cites nonexistent R-QA-2 | **Resolved.** 19/20 inline plus 5 controls; `wc -l` = 20 and 5 lines | :48 |\n| PM5 | R-CO-7 circular | **Resolved** (states, flag tuples, code outputs compared across 3 runs). Eval design is outside my lens; reads decidable. | :125 |\n\nPM minors, spot-checked: R-SU-3 checklist :137 ✔; TOOLS.md and unedited :138 ✔; R-FL-7 `source_kind` :67 ✔; ambiguous-date placement :37 ✔; R-EX-3 order :105 and R-EX-2 scope :104 ✔; ship-bar row 5 :289 ✔; assumptions cited by ID :301-317 ✔; R-CH-7 marked as proposal :79 ✔; accepted/pending total :75 ✔.\n\n## New in round 2\n\n| # | Sev | Title | Evidence |\n|---|---|---|---|\n| N1 | major | \"No flag text of any kind\" in the letter is contradicted by §6; flagged record sentences reach the carrier with no rule, no visibility and no control | :103 vs :216-225; walk.out [4] |\n| N2 | major | R-TL-8 keys on a lexicon category that does not exist | :52; lexicon.yaml:19 |\n| N3 | minor | No pending-item count or pending-flag warning before copy | R-EX-5 :107 |\n| N4 | minor | Total parenthetical is tool-authored text in the carrier block that volunteers a weakness; `<provider>`/`<service>` placeholder mismatch | :110, :238 |\n| N5 | minor | `unclear` → `charge` reclassification leaves a null-value charge | :73 vs :79 |\n| N6 | minor | Ambiguity rule sends most early-month MM/DD dates to \"Dates to confirm\" | :35, :316 |\n| N7 | minor | Internal notes cite \"record N\" without provider/date, and the letter has no record numbers | :249-263; walk.out [8] |\n| N8 | minor | Future treatment recommended (ESI) is not a notes item | :106, :228-229 |\n| N9 | nit | Dot leaders and mixed `$8,390` / `$6,240.00` formatting | :233-238 |\n"
}
````

### User / tool · 2026-11-02T00:32:58.100Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-resolution.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:01.942Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-resolution.md",
 "old_string": "Ambiguity rule sends most early-month MM/DD dates",
 "new_string": "Ambiguity rule sends about a third of all MM/DD dates (any day 1-12 that isn't equal to the month, 11 of ~30 per month)"
}
````

### User / tool · 2026-11-02T00:33:02.036Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-resolution.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:59.977Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-013-paralegal-r2.md",
 "content": "# T-013 review, round 2 — paralegal-reviewer\n\n**Verdict: changes** (0 blockers, 2 majors, 6 minors, 1 nit).\n\nRound 1's blocker is fixed as worded. Flag notes, labels, counts and the defense's arguments are out of the letter. Of my 9 round-1 majors,\n8 are resolved and 1 is partial. All 5 PM majors are resolved. The table with line numbers is in `artifacts/review-evidence/T-013-r2-resolution.md`.\n\nI re-walked the 9 sample records through §6 by script (`artifacts/review-evidence/T-013-r2-paralegal-walk.py`, output `…-walk.out.txt`):\n- All 11 quotes are verbatim in `sample.txt`.\n- All 9 headings use the provider as written and the header date, in order.\n- Gaps are 0,7,7,28,14,73,11,14.\n- The charges add to $8,390.\n\n**Would I paste the treatment section as-is?** Almost. I would fill in the Ex/Bates placeholders, reword the total line's parenthetical,\nand remove the dot leaders. That means a tool built to these requirements is close to letter-ready.\n\n**What an adjuster could use.** Seven of the ten golden flags have evidence strings that sit verbatim in the letter block: \"after two missed\nappointments\", \"Plan of care: 12 visits\", \"New onset pain\", \"may represent degenerative change; correlate clinically\", \"CT head negative\".\nThey are the record's own words, and quoting the hedge was my own round-1 ask, so this is not a fabrication problem. The problem is that\n:103 says \"No flag text of any kind\" appears in the letter, and the doc's own example breaks that. Nothing decides when a flagged sentence\nmay enter a letter quote. Nothing tells the attorney which quotes carry flagged language. The excerpt can't be edited, so if she wants a\nflagged sentence out, her only choice is to drop the whole visit, and then the letter looks like a longer gap. The other carrier-facing item\nis the total's parenthetical, \"visit count not stated\". That is tool-written text, and it volunteers a weakness to the carrier.\n\n**Still missing for a paralegal:** a pending count and a pending-flag warning before copy; provider and date next to \"record N\" in the notes;\na \"future treatment recommended\" notes item for the ESI.\n\nExercised: listed in the JSON. No app exists for this card, so this is a document and fixture review, run by script against the golden files.\n\n```json\n{\"card\": \"T-013\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"spec/REQUIREMENTS.md @ 64f766e (diff 65894f6..64f766e; no working-tree drift); against SPEC Appendix A Part 1, SAMPLE_CASE_TRUTHS, evals/golden/sample.txt + sample.expected.json, app/llm/lexicon.yaml, memory/contracts/api.md, personas/paralegal.md; round-1 reviews reviews/T-013-paralegal.md and reviews/T-013-product-manager.md; no app URL (requirements card)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-013 -> status in_review, rounds 1, commits [65894f6, 64f766e], AC 1-4 done\",\n  \"git diff --stat 64f766e -- spec/REQUIREMENTS.md -> empty, rc=0 (reviewing committed text)\",\n  \"read spec/REQUIREMENTS.md:1-330 in full; personas/paralegal.md (checklist §4 used); both round-1 reviews\",\n  \".venv/bin/python artifacts/review-evidence/T-013-r2-paralegal-walk.py -> artifacts/review-evidence/T-013-r2-paralegal-walk.out.txt: 11/11 letter quotes verbatim; 9/9 headings provider-in-source, header date, non-decreasing; gaps [0,7,7,28,14,73,11,14]; charges sum 8390; R-EX-1 forbidden strings all absent; golden flag evidence in letter: G1,C1(rec1,rec2),C2,P2,K1,K2,K3,K4 present, C1(rec7),P1,K5 absent\",\n  \"grep -ci hedge app/llm/lexicon.yaml -> 5 (rationale text only, lines 286,288,300,314,325); lexicon.yaml:19 flag_types: [pre_existing, causation_weakening, compliance]\",\n  \"python3 json check: case_04_duplicates_no_amounts.expected.json entries=4 from 6 records; sample.expected.json flags=10\",\n  \"wc -l evals/golden/hallucinations.jsonl hallucinations_controls.jsonl -> 20, 5\",\n  \"ls evals/golden | grep export -> rc=1 (sample.export.expected.txt not yet created; assigned to qa)\",\n  \"grep -n title memory/contracts/api.md -> :120 'Treatment gap of 73 days', :128 'Two different accident dates', :179 edit keys (conflict listed in §8, judged on merits only)\",\n  \"hand read of §6 Block 1 as a demand-letter paste and Block 2 as attorney notes against persona checklist items 1-23\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 4, \"verifiability_of_every_claim\": 4, \"workflow_fit\": 4, \"export_usability_in_demand_letter\": 4, \"adjuster_safety\": 3, \"charges_handling\": 4, \"flag_coverage_vs_truths\": 5},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"'No flag text of any kind' in the letter is contradicted by the worked example; there is no rule, no visibility and no control for flagged record sentences that reach the carrier\",\n   \"evidence\": \"spec/REQUIREMENTS.md:11 'Flags are what an adjuster would use against the client, so they never enter block 1'; :103 R-EX-1 'No flag text of any kind appears in it'. §6 letter :216-217 quotes 'Discharged from PT after two missed appointments.', :220-221 'New onset pain radiating to right arm', :224-225 'Findings may represent degenerative change; correlate clinically.', :208-209 'Plan of care: 12 visits.' walk.out [4]: evidence of G1, C1 (rec 1, 2), C2, P2, K1, K2, K3, K4 in_letter=True. :88 R-RV-2 'Date, provider and excerpt are not editable.' No R-ID stops the generator from choosing all three sentences of record 3, which would put 'low back pain in 2023, resolved' into the letter.\",\n   \"why_it_matters\": \"The R-EX-1 test passes only because its forbidden-string list happens to leave these phrases out. The requirement's actual claim is false for its own example, so the implementer can't tell what is allowed. Which record sentences go to the carrier is decided by whatever excerpt the model picked. The attorney is never told that the letter quotes the missed appointments or the degenerative hedge. If I want one of those quotes out, I can't trim the excerpt. I can only dismiss the whole visit, and dismissing entry 6 turns the letter's gap into 02/20 → 05/18. Whether to disclose is the attorney's call (litigation-lead lens). Making that call visible and possible is mine.\",\n   \"fix\": \"Reword R-EX-1 and :11: the letter holds no tool-authored flag content (types, titles, reasons, day counts, counts). Record sentences quoted in an entry excerpt may coincide with flag evidence. Add to R-EX-4 a notes section 'FLAGGED LANGUAGE QUOTED IN THE LETTER' that lists each letter entry whose excerpt contains a flag's evidence string, with the flag id. Under R-RV-2, allow an excerpt edit limited to choosing a different set of whole sentences from the same record, code-verified. R-TL-8 qualifiers can't be removed. Log it as an edit with the original kept. State a default for non-qualifier flagged sentences, e.g. a prior-condition sentence about another body part is not in the default excerpt.\",\n   \"acceptance_test\": \"UT on the §6 example: the notes list entries 4, 6, 7, 8, 9 under 'FLAGGED LANGUAGE QUOTED IN THE LETTER' with flag ids. UT: the letter contains no flag type label, title or reason string from sample.expected.json. E2E: on entry 6, select only 'Pain 3/10.' → the letter shows that excerpt and the notes show the original. On entry 8, trying to drop 'Findings may represent degenerative change; correlate clinically.' is refused (R-TL-8).\"},\n  {\"severity\": \"major\",\n   \"title\": \"R-TL-8 (qualifier travels with finding) keys on a lexicon 'hedge' category that does not exist; its entry-6 test cannot follow from the rule\",\n   \"evidence\": \"spec/REQUIREMENTS.md:52 'a sentence matching the `hedge` category of `app/llm/lexicon.yaml`'. app/llm/lexicon.yaml:19 'flag_types: [pre_existing, causation_weakening, compliance]'. grep -ci hedge lexicon.yaml = 5, all in rationale/false_positive text (:286,288,300,314,325). :52 test requires 'entry 6 excerpt contains after two missed appointments', which matches lexicon entries of flag_type compliance (lexicon.yaml:572, :599), not any hedge.\",\n   \"why_it_matters\": \"This is the rule that stops a quote from dropping the radiologist's hedge, which was my round-1 credibility finding. As written, nobody can implement or test it literally. One reasonable reading (causation_weakening) misses entry 6. Another (all categories) pulls 'low back pain in 2023' into entry 3's letter excerpt, which R-EX-1's test forbids.\",\n   \"fix\": \"Name the trigger exactly. Example: lexicon entries with flag_type causation_weakening (may_represent, correlate_clinically, possibility_terms), plus compliance entries when the sentence is the same one that carries the finding. Or add an explicit `qualifier: true` key to named lexicon entries (a T-009 card change) and cite those ids.\",\n   \"acceptance_test\": \"UT: the trigger set loaded from lexicon.yaml is non-empty and includes may_represent and correlate_clinically. Seeded entry 8 with the shortened excerpt → needs_review EXCERPT_OMITS_QUALIFIER. Entry 3 with excerpt 'Persistent neck pain 6/10, daily headaches.' stays verified (the pre_existing sentence does not trigger).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"No pending count or pending-flag warning before copy\",\n   \"evidence\": \"spec/REQUIREMENTS.md:107 R-EX-5 count line 'N entries, N charges in letter · N flags in internal notes · N of 9 records in letter' has no pending figure; pending items appear only inside the notes block (:106, :271). personas/paralegal.md §4 item 17.\",\n   \"why_it_matters\": \"If I copy with the 73-day gap flag still pending, the attorney's notes show it only as a line under 'pending'. I need to see '3 flags not reviewed' before I hit Copy.\",\n   \"fix\": \"Add 'N items pending (N flags)' to the R-EX-5 line, and require a one-step confirm on Copy when any flag is pending.\",\n   \"acceptance_test\": \"E2E: leave the gap flag pending, click Copy letter → the confirm states '1 flag not reviewed'; the count line shows it.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Total-line parenthetical is tool-authored text in the carrier block that volunteers a weakness; the placeholder name is inconsistent\",\n   \"evidence\": \"spec/REQUIREMENTS.md:238 '(excludes physical therapy — per-visit rate only, visit count not stated)'; :110 template '(excludes <provider> — <reason>)' then '`<service>` comes from a fixed code lookup'. walk.out [7].\",\n   \"why_it_matters\": \"'Visit count not stated' tells the carrier our PT billing is undocumented. Next to 'Plan of care: 12 visits' and the discharge at visit 9, it invites the non-compliance argument. The exclusion should be disclosed (that was my round-1 ask), but in neutral wording. The reasoning ('rate only, count not stated') belongs in the notes, where :257 already has it.\",\n   \"fix\": \"Letter wording: 'Billed charges stated in these records: $8,390.00 (physical therapy charges, Capital PT, not included; to be supplemented)'. Use one placeholder name (<service>) in :110.\",\n   \"acceptance_test\": \"UT: the sample total line equals the new string; the letter contains neither 'visit count' nor 'rate'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"unclear → charge reclassification produces a charge with no value\",\n   \"evidence\": \"spec/REQUIREMENTS.md:73 '`$1,2OO` and `$9S.00` are `unclear`, value null'; :79 'the amount and excerpt are immutable … `unclear` or `estimate` → `charge` re-runs judge #2'.\",\n   \"why_it_matters\": \"If I reclassify the OCR-garbled $1,2OO as a charge, it can't be totaled because it has no value, and I'm not allowed to type $1,200. The total is then quietly wrong, or the action does nothing.\",\n   \"fix\": \"State that `unclear` with a null value cannot become `charge`. It goes to the notes as 'request clean copy of bill'. Only `unclear` items with a parsed value may be reclassified.\",\n   \"acceptance_test\": \"UT: reclassify a null-value unclear → 422 invalid_edit. The notes contain 'request clean copy' for $1,2OO.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Ambiguous-date rule will send about a third of US-format dates to 'Dates to confirm'\",\n   \"evidence\": \"spec/REQUIREMENTS.md:35 'ambiguous when its first two numbers are both 1–12 and differ'; :316 'she confirms once per date … per-packet convention is deferred'. Any day 1-12 that isn't equal to the month (11 of ~30 days a month) qualifies, e.g. 01/09/2026, 03/06/2026.\",\n   \"why_it_matters\": \"Texas records are MM/DD. On a 100-record packet that is about 35 confirmations, and every unconfirmed entry is left out of gap math. That's noise I'll learn to click through.\",\n   \"fix\": \"Keep the rule, but add per-packet inference as a requirement: if any date in the same packet or source has a first number > 12 → DD/MM, or a second number > 12 → MM/DD, apply it to that packet's ambiguous dates and show that it was applied. Ask only when the packet gives no evidence.\",\n   \"acceptance_test\": \"UT: a packet containing 02/17/2026 and 03/06/2026 → 03/06 parses as March 6 with 'inferred MM/DD from 02/17/2026'; case_01's 04/05/2026 with no evidence still asks.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Internal notes cite 'record N' without provider and date, and the letter has no record numbers\",\n   \"evidence\": \"spec/REQUIREMENTS.md:249-251, :257, :263 (walk.out [8]); :108 'Internal record numbers appear in the internal notes only.'\",\n   \"why_it_matters\": \"The attorney reads 'record 8 \\\"may represent…\\\"' and has to work out which letter entry that is. The gap line (:247) already does it correctly.\",\n   \"fix\": \"Every notes citation reads 'record N (<provider>, <Month D, YYYY>)', as in :247.\",\n   \"acceptance_test\": \"UT: every 'record \\\\d' in internal_notes_text is followed by a provider and a date.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Future treatment recommended is not a notes item\",\n   \"evidence\": \"spec/REQUIREMENTS.md:106 R-EX-4 lists damages mentions and bills to request but not recommended future care. Record 9 'Recommend cervical epidural steroid injection' appears only in the letter (:228-229).\",\n   \"why_it_matters\": \"Future medicals are a specials element alongside lost wages. The doc already collects the other to-dos (bills to request, damages mentions). The ESI needs a cost estimate request too.\",\n   \"fix\": \"Add 'FUTURE TREATMENT RECOMMENDED (no cost stated)' to R-EX-4, sourced from recommend/plan sentences with no amount, worded as an action ('request cost estimate').\",\n   \"acceptance_test\": \"Sample: the notes list 'record 9 (Hill Country Pain Management, June 12, 2026): \\\"Recommend cervical epidural steroid injection.\\\" Request cost estimate.'\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Dot leaders and mixed money formatting in the letter template\",\n   \"evidence\": \"spec/REQUIREMENTS.md:233 '........ $6,240.00', :235 '....... $2,150.00', :238 '$8,390'.\",\n   \"why_it_matters\": \"Dot leaders don't line up once pasted into Word in a proportional font, and they print. The total uses a different format from the line items.\",\n   \"fix\": \"'Central ER, January 9, 2026: $6,240.00'; total '$8,390.00'.\",\n   \"acceptance_test\": \"The golden export contains no '..' run, and every amount matches \\\\$[\\\\d,]+\\\\.\\\\d{2}.\"}\n ],\n \"whats_right\": [\n  \"The two-block export with the flag commentary kept out of the letter, reconciliation ('N of 9 records'), and the dismissed-entry-5 note at :275 is how I want to hand off to the attorney\",\n  \"R-RV-9 core source modal with code offsets, plus R-TL-3 header date, R-TL-9 verbatim provider and R-TL-2 whole sentences: every letter line in §6 checked clean by script\",\n  \"Charges: $185 never totaled, rate worded as 'request itemized PT ledger', duplicates merged by code, amount and excerpt immutable (R-CH-3/6/7, :257)\"\n ],\n \"questions_for_chris\": [\n  \"Should record sentences the tool flagged (missed appointments, 'new onset', the degenerative hedge) appear in the treatment-section quotes by default, or does the attorney pick per entry? This decides the default excerpt in finding 1 (litigation-lead's call, not mine).\",\n  \"For US-format dates like 03/06/2026, may the tool infer MM/DD from other dates in the same packet, or must she confirm each one?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T00:34:00.120Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-013-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:05.386Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/Seven of the ten golden flags have evidence strings that sit verbatim/Eight of the ten golden flags have evidence strings that sit verbatim/' reviews/T-013-paralegal-r2.md && python3 -c \"\nimport re,json;t=open('reviews/T-013-paralegal-r2.md').read();b=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',t,re.S);assert len(b)==1;d=json.loads(b[0]);s=[f['severity'] for f in d['findings']];print(d['verdict'],{k:s.count(k) for k in set(s)},d['scores']['verify_quickly'])\"; grep -c 'Eight of the ten' reviews/T-013-paralegal-r2.md; ls tools/ | grep -i valid; python3 tools/board.py --help 2>&1 | head -20",
 "description": "Fix count, validate review JSON, find validator"
}
````

### User / tool · 2026-11-02T00:34:05.445Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not edit s/Seven of the ten golden flags have evidence strings that sit verbatim/Eight of the ten golden flags have evidence strings that sit verbatim/ in place
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:07.248Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-013-paralegal-r2.md",
 "old_string": "Seven of the ten golden flags",
 "new_string": "Eight of the ten golden flags"
}
````

### User / tool · 2026-11-02T00:34:07.396Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-013-paralegal-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:09.188Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport re,json;t=open('reviews/T-013-paralegal-r2.md').read();b=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',t,re.S);assert len(b)==1;d=json.loads(b[0]);s=[f['severity'] for f in d['findings']];print(d['verdict'],{k:s.count(k) for k in set(s)},d['scores']['verify_quickly'])\"; python3 tools/board.py --help 2>&1 | head -25",
 "description": "Validate review JSON and list board commands"
}
````

### User / tool · 2026-11-02T00:34:09.241Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No escaped character) | command: python3 -c "
import re,json;t=open('reviews/T-013-paralegal-r2.md').read();b=re.findall(r'\`\`\`json\n(.*?)\n\`\`\`',t,re.S);assert len(b)==1;d=json.loads(b[0]);s=[f['severity'] for f in d['findings']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:13.115Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py",
 "content": "\"\"\"Parse the single JSON block in reviews/T-013-paralegal-r2.md and check the §7.4 verdict rule.\"\"\"\nimport json\nimport re\nfrom pathlib import Path\n\nt = Path(__file__).resolve().parents[2].joinpath(\"reviews/T-013-paralegal-r2.md\").read_text()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nassert len(blocks) == 1, len(blocks)\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexpected = \"fail\" if \"blocker\" in sev else \"changes\" if \"major\" in sev else \"pass\"\nprint(\"verdict\", d[\"verdict\"], \"expected\", expected, {k: sev.count(k) for k in sorted(set(sev))},\n      \"verify_quickly\", d[\"scores\"][\"verify_quickly\"], \"whats_right\", len(d[\"whats_right\"]))\nassert d[\"verdict\"] == expected\n"
}
````

### User / tool · 2026-11-02T00:34:13.209Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:14.605Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py",
 "description": "Validate review JSON and verdict rule"
}
````

### User / tool · 2026-11-02T00:34:14.712Z

**tool result**
````
verdict changes expected changes {'major': 2, 'minor': 6, 'nit': 1} verify_quickly 4 whats_right 3
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:17.358Z

Review written and validated. Now saving recurring patterns to agent memory.

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:23.254Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_spec_review_patterns.md",
 "content": "---\nname: spec-review-patterns\ndescription: Recurring defects found in Zlayt PM requirements/spec reviews (T-013 r1, r2) — absolute claims contradicted by the doc's own example, references to names that don't exist\nmetadata:\n  type: feedback\n---\n\nBefore grading a requirements doc, mechanically check (1) every absolute claim against the doc's OWN worked example, and (2) every named artifact it keys on (lexicon category, R-ID, golden file, reason code) actually exists.\n\n**Why:** T-013 r2: R-EX-1 said \"No flag text of any kind\" in the letter, yet 8 of 10 golden flag evidence strings sat verbatim in its §6 letter example; its test only listed strings that happened to pass. R-TL-8 keyed on a lexicon `hedge` category that doesn't exist (lexicon flag_types are pre_existing/causation_weakening/compliance). r1 had R-TL-4 citing a nonexistent R-QA-2. Writers fix the reviewer's wording and leave the test narrower than the claim.\n\n**How to apply:** Write a script under artifacts/review-evidence/ that extracts the example blocks and compares them with evals/golden/sample.expected.json (flag evidence, quotes, providers, dates); grep each referenced name. Also judge the export as a demand-letter paste: tool-authored text in the carrier block (e.g. \"visit count not stated\") is adjuster ammunition even when the reviewer asked for the disclosure. See [[reviewer-tooling-quirks]].\n"
}
````

### User / tool · 2026-11-02T00:34:23.348Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_spec_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:26.606Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "content": "---\nname: reviewer-tooling-quirks\ndescription: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround\nmetadata:\n  type: feedback\n---\n\nDon't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.\n\n**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.\n\n**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].\n"
}
````

### User / tool · 2026-11-02T00:34:26.696Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:28.392Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "content": "- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture\n- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; use Edit + scripts in review-evidence\n"
}
````

### User / tool · 2026-11-02T00:34:28.490Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:41.672Z

**Verdict: changes.** No blockers, 2 majors, 6 minors, 1 nit. scores.verify_quickly = 4.

**Round-1 status** (line numbers are in the resolution table):
- My blocker (flags were going into the letter) is fixed as worded: two separate blocks, and no flag notes, labels or counts in the letter.
- Of my 9 majors, 8 are resolved and 1 is partial (the hedge rule, see major 2).
- All 5 PM majors are resolved. The stretch timing and the determinism eval are outside my lens, so the PM should confirm those two.

**Re-walking the 9 records through §6:** I checked the worked example with a script. All 11 quotes are word-for-word from the records. All 9 headings use the provider as written and the record's header date, in order. The gaps come out as 0, 7, 7, 28, 14, 73, 11 and 14 days, and the charges add to $8,390. I would paste the treatment section almost as-is after three changes: fill in the Ex/Bates placeholders, reword the parenthetical on the total line, and drop the dot leaders.

**Majors:**
1. **The letter does contain flagged record text.** REQUIREMENTS.md:103 says "No flag text of any kind" goes in the letter, but the doc's own example breaks that (:208-225). Evidence quotes from 8 of the 10 expected flags appear word-for-word in the letter: "after two missed appointments", "New onset pain", the "may represent degenerative change" hedge, "Plan of care: 12 visits". The R-EX-1 test passes only because its banned-phrase list leaves these out.
   - Nothing decides when a flagged sentence may go into a quote, and nothing tells the attorney it is there.
   - The quote can't be edited. Her only way to remove one is to drop the whole visit, and dropping visit 6 makes the gap look longer.
   - Fix: list flagged language quoted in the letter in the internal notes, and let her pick which whole sentences of the record to quote. A hedge can never be dropped.
2. **The hedge rule (R-TL-8, :52) points at something that doesn't exist.** It triggers on a `hedge` category in `app/llm/lexicon.yaml`, but the lexicon's only categories are `pre_existing`, `causation_weakening` and `compliance` (lexicon.yaml:19). The rule's own test for visit 6 ("missed appointments") matches a `compliance` entry, so it can't follow from any reading of the rule as written.

**Could an adjuster use anything in the letter?** The record quotes above are the records' own words; whether to send them is the attorney's call (litigation-lead's lens). The one piece of text the tool writes itself is the total line's "(excludes physical therapy — per-visit rate only, visit count not stated)" (:238). That tells the carrier our PT billing is undocumented. I logged it as minor with neutral wording ("to be supplemented").

**Other minors:**
- No count of pending items, and no warning before copying when a flag is unreviewed.
- Reclassifying an unreadable amount (like `$1,2OO`) as a charge leaves a charge with no dollar value.
- The ambiguous-date rule sends about a third of US-format dates to "Dates to confirm".
- The internal notes cite "record N" without provider and date, and the letter has no record numbers to match them to.
- No notes item for recommended future treatment (the epidural injection in record 9).

I asked Chris two questions in the review: whether flagged sentences go in the letter quotes by default, and whether the tool may infer month/day order from other dates in the same packet. I also saved two notes on recurring patterns to my agent memory.

Files:
- /Users/arsis/zlayt-pm-project/reviews/T-013-paralegal-r2.md
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-resolution.md
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-walk.py
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-walk.out.txt
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py
