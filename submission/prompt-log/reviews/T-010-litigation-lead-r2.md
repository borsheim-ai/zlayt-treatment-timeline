# T-010 review, round 2 — litigation-lead-reviewer

**Verdict: changes** (0 blockers, 2 majors, 2 minors, 2 nits).

All four round-1 majors are fixed, and the Texas law now holds up against the primary text. I re-fetched Rule 1.05 (the State Bar PDF and legalethicstexas), Rule 4.01 comment 3, Op. 705 and §§181.001/.151/.154. Every corrected statement in the dossiers matches. Specifically:
- The adjuster no longer makes the tool pick an accident date. Item 2 reads "first recorded treatment" and computes no delay figure (D-017).
- The adjuster's red flag now targets tool omissions, not my disclosure decisions.
- My own dealbreaker now separates the synthetic-only prototype from a controlled post-launch test set built from real work product (D-016).
- Six of my eight minors and the nit are resolved. The resolution table for both round-1 reviews is in `artifacts/review-evidence/T-010-r2-resolution.md`.

Two majors remain:
1. **Charges content placed in the letter (D-001 / R-EX-4 / R-EX-8).** My round-1 fix asked the charges section to list encounters that have no stated charge, and the dossiers copied that wording. Lit-lead #19 and adjuster #21 now put that list in "the charges section", and #21 adds that otherwise "I value only the two bills". That places it in the letter the carrier reads. My own calibration fix also writes "PT billed at $185/visit; visit count not stated" into the export. The binding decisions put both items in the internal notes ("Bills to request", "Amounts not totaled"). R-EX-8 tests that the letter text contains neither "visit count" nor "rate". A reviewer following these dossiers would push missing-bill and rate disclosures into the demand. That decision is mine, not the tool's.
2. **The round-2 text has not reached the reviewers.** Every `.claude/agents/<persona>-reviewer.md` was last compiled at f413e84, three minutes before 6bb13dd. Fourteen lit-lead lines, 11 adjuster lines and 14 privacy lines are missing from the compiled bodies. That includes the Rule 1.05 correction, the delay item and both red-flag rewrites. Any domain review dispatched now runs on the round-1 errors.

Minor issues: the §181.154 source takeaway narrows subsection (c), and old flag-type names that D-013 retired are still in use.

```json
{"card": "T-010", "persona": "litigation-lead-reviewer", "model": "claude-opus-5-5",
 "scope": "Round 2. git diff 34e9398..6bb13dd -- personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md (commits 6404549, 6bb13dd; git diff --stat 6bb13dd -- personas/ empty, so the working tree = 6bb13dd). Checked against reviews/T-010-litigation-lead.md, reviews/T-010-product-manager.md, memory/ORCHESTRATOR_DECISIONS.md D-001..D-018, spec/SPEC.md Appendix A, spec/SAMPLE_CASE_TRUTHS.md, spec/REQUIREMENTS.md R-EX-4/R-EX-8. Also checked the compiled .claude/agents/*-reviewer.md bodies. No app (documents card).",
 "exercised": [
  "python3 tools/board.py show T-010 (status in_review, rounds 1, commits 34e9398/6404549/6bb13dd, handoff)",
  "git log --oneline -8; git diff --stat 34e9398..6bb13dd -- personas/; git diff --stat 6bb13dd -- personas/ (empty)",
  "read all five dossiers at 6bb13dd in full (cat -n), both round-1 reviews, ORCHESTRATOR_DECISIONS D-001..D-018, SPEC Appendix A must-haves, SAMPLE_CASE_TRUTHS, REQUIREMENTS R-EX-4/R-EX-8 (grep)",
  "python3 -I artifacts/review-evidence/T-010-r2-count.py: sections 1-10 x5; checklist 23/20/21/19/19; unique URLs 8/9/10/9/16; calibration 3/3/4/4/3 with severities; §5 blocker line present x5",
  "curl-fetched Tex. R. 1.05 and 4.01 (legalethicstexas, 200), State Bar TDRPC PDF (texasbar.com ContentID=27271, 200; pdftotext: Rule 1.05 = lines 841-1122, 0 'reasonable efforts' inside; Rule 1.01 cmt 8 'relevant technology'), Op. 705 (200), Tex. H&S §§181.001/.151/.154 (texas.public.law, 200), txcourts Haygood docket (200), Wayback ABA 512 (429 rate-limited; 200 in r1); text extracted with artifacts/review-evidence/T-010-r2-srch.py",
  "grep across five dossiers: 'supervise like|supervise AI' 0 hits; 'computed from the accident' 0; 'billed totals overstate' 0; 'minor at most|nice-to-have' 0; 'defer' 0; remaining 'reasonable efforts' all scoped to ABA 1.6(c)",
  "compared every dossier line against .claude/agents/<persona>-reviewer.md (python, read-only): missing lines lit-lead 14, adjuster 11, nurse 3, paralegal 4, privacy 14; git log -1 shows agents at f413e84 18:38:21 vs dossiers at 6bb13dd 18:41:05",
  "cross-checked every §8 calibration severity against its own §5 red flags and the §8 severity rule; checked each dossier against D-001/D-011/D-012/D-013/D-016/D-017",
  "wrote artifacts/review-evidence/T-010-r2-resolution.md (resolution table for all LL and PM round-1 findings + source checks)"
 ],
 "verdict": "changes",
 "scores": {"texas_law_accuracy": 4, "catches_what_gets_demands_discounted": 5, "adjuster_adversarial": 5, "keeps_tool_out_of_legal_medical_judgment": 4, "spec_alignment": 3, "source_grounding": 5},
 "findings": [
  {"severity": "major",
   "title": "Missing-bill list and PT rate wording are placed in the letter, contradicting D-001, R-EX-4(8) and R-EX-8 (introduced by my round-1 fix wording)",
   "evidence": "personas/litigation-lead.md:37 \"19. The charges section states the total covers only amounts stated in the records received and lists dated encounters with no stated charge (EMS 01-09, PCP 01-16, PT visits, pain management 05-18 and 06-12)\"; personas/claims-adjuster.md:38 \"21. The charges section says ... lists dated encounters with no stated charge ... — otherwise I value only the two bills\" (the adjuster only ever sees the letter); personas/litigation-lead.md:62 calibration fix \"Billed charges stated in records received: $8,390 (ER $6,240; MRI $2,150). PT billed at $185/visit; visit count not stated.\" vs memory/ORCHESTRATOR_DECISIONS.md D-001 (\"Internal review notes — do not send (accepted flags, unclear amounts, records not included, bills to request ...)\"), spec/REQUIREMENTS.md:122 R-EX-4 \"(8) Bills to request: providers ... with an entry in the letter and no accepted charge\" and :126 R-EX-8 \"The reason ('per-visit rate only, visit count not stated') lives in the notes, never in the letter ... UT: letter_text contains neither 'visit count' nor 'rate'\".",
   "why_it_matters": "These lines become reviewer prompts. A reviewer following them would file findings until the demand itself tells the carrier which bills we don't have and that PT is a rate with no visit count. That is an invitation to discount the specials, and whether to say it is my call, not the tool's. It is the same failure as round-1 M2 (the dossier deciding letter content), and it contradicts binding decisions and a tested requirement. R-EX-8 already gives the correct letter line: 'Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)'.",
   "fix": "Lit-lead #19 and adjuster #21: \"The letter's total line reads 'Billed charges stated in these records: $X' (R-EX-8) and claims no completeness; the internal notes list 'Bills to request' for every provider with a letter entry and no accepted charge (Austin EMS, Dr. Alvarez, Capital PT, Hill Country Pain Management) and the $185 rate under 'Amounts not totaled' (R-EX-4) — no amounts invented.\" Drop 'otherwise I value only the two bills', or reword it to 'if the notes don't list them, the firm under-demands'. Calibration fix at litigation-lead.md:62: use the R-EX-8 line, with the rate in the internal notes.",
   "acceptance_test": "No item or calibration fix in the five dossiers asks the letter/export text to contain 'no stated charge', 'visit count' or '$185'. Lit-lead #19 and adjuster #21 name the internal-notes 'Bills to request' section. Lit-lead :62 fix equals or is compatible with the R-EX-8 sample line."},
  {"severity": "major",
   "title": "Round-2 dossier text is not compiled into the reviewer agent bodies",
   "evidence": "git log -1 --format='%h %ci': each of .claude/agents/{litigation-lead,claims-adjuster,legal-nurse,paralegal,privacy-compliance}-reviewer.md = f413e84 2026-11-01 18:38:21; each personas/<p>.md = 6bb13dd 18:41:05. Dossier lines absent from the compiled body (python line-membership check): litigation-lead 14 (incl. :5 Rule 4.01, :31 Op. 705, :32 item 14, :37, :45 red flag), claims-adjuster 11 (incl. :19 delay item, :24, :45 red flag, :56), privacy-compliance 14 (incl. :5 Rule 1.05, :34-:38, :72), legal-nurse 3, paralegal 4. My own loaded prompt still contains the old item 14 / red flag 'Any suggestion of using real client records in development or testing.'",
   "why_it_matters": "The card exists so that these dossiers 'compile into the reviewer agent bodies'. Until they are recompiled, every domain review runs on the round-1 errors. The privacy reviewer would grade Part 2 against a Rule 1.05 'reasonable efforts' duty that does not exist. The adjuster reviewer would demand a delay-from-accident figure, which resolves the date conflict. My own reviewer would fail a D-016-compliant Part 2. All of the round-2 fixes are inert until then.",
   "fix": "Run python3 tools/compile_agents.py --only paralegal litigation-lead claims-adjuster legal-nurse privacy-compliance after the major above is fixed, commit, and record the sha on T-010. The owner of .claude/agents decides who runs it.",
   "acceptance_test": "For each of the five personas, every non-blank line of personas/<p>.md appears in .claude/agents/<p>-reviewer.md (0 missing). The agents commit is newer than the last personas commit."},
  {"severity": "minor",
   "title": "§181.154 source takeaway narrows the (c) exceptions",
   "evidence": "personas/privacy-compliance.md:71 \"exceptions for treatment, payment, operations, insurance functions, or disclosures required by law\" vs statute text (texas.public.law, fetched 200): \"(c) ... not required if the disclosure is made: (1) to another covered entity ... for the purpose of: (A) treatment; (B) payment; (C) health care operations; or (D) performing an insurance or health maintenance organization function ...; or (2) as otherwise authorized or required by state or federal law.\"",
   "why_it_matters": "The (c)(2) 'authorized' branch is the one a firm would most plausibly rely on. Dropping it, and leaving out that (c)(1) applies only to disclosures to another covered entity, sends the privacy reviewer into Part 2 with a wrong map of the statute. Item 17 (:36) is accurate, so this is a takeaway problem, not a checklist problem.",
   "fix": "\"... exceptions in (c): disclosures to another covered entity for treatment, payment, health care operations or insurance/HMO functions, and disclosures 'otherwise authorized or required by state or federal law'.\"",
   "acceptance_test": "privacy-compliance.md:71 contains 'authorized or required' and 'to another covered entity'."},
  {"severity": "minor",
   "title": "Flag-type vocabulary retired by D-013 persists in three dossiers",
   "evidence": "personas/claims-adjuster.md:22 \"causation-weakening fact\", :62 \"Fix: causation/compliance flag\"; personas/paralegal.md:29 \"flagged as causation/compliance risk\"; personas/legal-nurse.md:36 \"prior-condition and causation-weakening language\" vs D-013 \"Flag-type vocabulary everywhere: gap, conflict, pre_existing, causation, plus record_warning ... Lexicon causation_weakening and compliance map to causation.\"",
   "why_it_matters": "D-013 exists because three vocabularies caused triage noise. A reviewer whose calibration fix asks for a 'causation/compliance flag' may file a finding against a D-013-correct `causation` flag.",
   "fix": "Use 'causation flag' and 'pre_existing flag' (D-013) in these four lines. The adjuster's own analysis may keep his vocabulary in §6.",
   "acceptance_test": "grep -n 'causation-weakening\\|causation/compliance' in §4 and §8 of the five dossiers returns nothing."},
  {"severity": "nit",
   "title": "Lit-lead item 9 still contemplates batch accept, which D-011 cut",
   "evidence": "personas/litigation-lead.md:27 \"(or, if batch accept exists, it excludes needs-review items and amounts)\" vs D-011 \"Cut (non-goals): batch accept\".",
   "why_it_matters": "This is harmless today. But it signals that a batch accept would pass review, and the decision says it is out of scope.",
   "fix": "\"Nothing reaches the export without an explicit per-item human accept; there is no batch accept (D-011).\"",
   "acceptance_test": "Item 9 cites D-011 and has no batch-accept carve-out."},
  {"severity": "nit",
   "title": "Board AC-2 evidence counts are stale after round 2",
   "evidence": "python3 tools/board.py show T-010: AC 2 evidence \"litigation-lead 8 ... privacy-compliance 12 ... Checklist items: 23/18/18/19/18\" vs T-010-r2-count.py: URLs 8/9/10/9/16, checklist 23/20/21/19/19.",
   "why_it_matters": "The counts are still within thresholds, but the gate reads evidence that no longer describes the files.",
   "fix": "Re-check AC 2 with the r2 counts.",
   "acceptance_test": "AC 2 evidence matches T-010-r2-count.py output."}
 ],
 "whats_right": [
  "The Texas ethics text now matches primary sources: Rule 1.05 'shall not knowingly' with no reasonable-efforts clause, Rule 4.01 and comment 3, Op. 705 as a 'cf. Rule 5.03' analogy, §181.154 in the privacy checklist.",
  "D-016 and D-017 are encoded precisely: adjuster #2 shows 'first recorded treatment' and both dates with no delay figure; lit-lead #14 and its red flag split the synthetic prototype from a controlled post-launch test set.",
  "The adjuster red flag (:45) and the legal-label bans (lit-lead #17, adjuster #20) keep disclosure strategy and legal conclusions with the attorney."
 ],
 "questions_for_chris": []}
```
