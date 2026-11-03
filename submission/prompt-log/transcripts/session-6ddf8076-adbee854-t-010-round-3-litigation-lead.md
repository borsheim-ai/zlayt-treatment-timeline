# Subagent: T-010 round-3: litigation-lead (T-010 round-3: litigation-lead)

Source: `agent-adbee8544b586a641.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:51:36.631Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 3 (final) of T-010 "Persona dossiers: 5 domain personas" (M1). AC: `python3 tools/board.py show T-010`. Your round-2 review: reviews/T-010-litigation-lead-r2.md (2 majors) and reviews/T-010-product-manager-r2.md (pass, 2 minors). Changes: `git diff 6bb13dd..2687094 -- personas/`. Decisions: memory/ORCHESTRATOR_DECISIONS.md D-001..D-022 (D-019: letter total line exactly "Billed charges stated in these records: $X").
Exercise hands-on: resolution table for each r2 finding (artifacts/review-evidence/T-010-r3-resolution.md); grep all 5 dossiers for anything that would put charges content, flags, or adverse facts into the letter; re-verify the §181.154 wording against texas.public.law with curl; confirm the compiled agents match (`python3 tools/compile_agents.py --check`).
Write reviews/T-010-litigation-lead-r3.md (D.2 JSON). Do not fix anything. Reply ≤ 15 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:40.764Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/litigation-lead-reviewer/feedback_texas_law_checks.md; echo ---; python3 tools/board.py show T-010; echo ---; ls artifacts/review-evidence/ | grep T-010; ls reviews | grep T-010; git rev-parse --is-inside-work-tree; git log --oneline -5",
 "description": "Read memory, card, evidence listing, git state"
}
````

### User / tool · 2026-11-02T00:51:40.955Z

**tool result**
````
---
name: texas-law-checks
description: Recurring Texas-law misstatements and source-fetch workarounds seen in persona/ethics content on this project (Rule 1.05, Op. 705, Haygood, ch. 181)
metadata:
  type: feedback
---

Re-check these every time ethics/damages law shows up in dossiers, product note or Part 2. They were wrong or overstated in T-010 (2026-11-01).

- Tex. Disc. R. 1.05 has NO ABA 1.6(c)-style "reasonable efforts" clause; duty is "shall not knowingly reveal". Precautions come from 1.01 cmt. 8 + Ops. 680/705.
- Op. 705 (Feb 2025) only analogizes AI to "overconfident nonlawyer assistants. Cf. Rule 5.03" — not a holding that 5.03 governs AI. ABA 512 is the one tying AI to 5.1/5.3.
- Demand letters go to adjusters: the relevant rule is Tex. R. 4.01 (truthfulness to third persons), not 3.03 candor/Mata.
- Haygood: recoverable = "have been or must be paid"; billed is not categorically an overstatement (LOP/unpaid).
- Tex. H&S §181.154 (electronic disclosure authorization) is the ch. 181 provision relevant to sending records to an LLM vendor.
- §41.0105 unchanged since 2003; 2025 SB 30 died in conference (last action 05/30/2025).

**Why:** these become reviewer prompts and submission prose read by lawyers; a wrong rule costs the same credibility as a wrong date in a demand.
**How to apply:** fetch primaries with curl (WebFetch unavailable): Haygood via search.txcourts.gov cn=09-0377; statutes via texas.public.law (statutes.capitol.texas.gov /Docs htm links return a JS shell); ABA 512 PDF via web.archive.org id_ snapshot (americanbar.org 403). Bash `>` redirects into scratchpad are blocked by the reviewer hook; use `curl -o`.

- §181.154(c)(2) is "authorized OR required by state or federal law"; (c)(1) exceptions apply only to disclosures TO another covered entity. Paraphrases drop both.
- Rule 4.01 cmt 3 (verified): "no duty to inform a third person of relevant or material facts, except as required by law..."

Round-2 traps (T-010, 2026-11-01): (1) dossier fixes are inert until `tools/compile_agents.py` recompiles `.claude/agents/*-reviewer.md` — always line-diff dossier vs compiled body; (2) my own round-1 fix wording can contradict later binding decisions (D-001 / R-EX-4/R-EX-8: missing bills and rate reasons belong in internal notes, never the letter) — re-check my prior fixes against ORCHESTRATOR_DECISIONS. Reviewer hook blocks heredoc/`>` into scratchpad; put helper scripts under artifacts/review-evidence/.

Also recurring: watch for persona checklists that make the tool resolve the accident-date conflict or decide what adverse facts go into the export — that is attorney strategy, and the spec says export = only accepted items.
---
---
id: "T-010"
title: "Persona dossiers: 5 domain personas (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)"
milestone: "M1"
role: "researcher"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:51:39Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T00:48:18Z"
rounds: 2
commits: ["34e9398", "6404549", "6bb13dd", "3f9dd58", "2687094"]
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-010-product-manager.md", "at": "2026-11-02T00:35:23Z"}
  - {"persona": "litigation-lead-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-010-litigation-lead.md", "at": "2026-11-02T00:38:58Z"}
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "pass", "file": "reviews/T-010-product-manager-r2.md", "at": "2026-11-02T00:48:09Z"}
  - {"persona": "litigation-lead-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-010-litigation-lead-r2.md", "at": "2026-11-02T00:48:09Z"}
ac:
  - {"n": 1, "text": "personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md exist with all 10 §6.3 sections", "done": true, "evidence": "personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md each have sections 1-10 (regex check of '## N.' headers)"}
  - {"n": 2, "text": "each has >=5 sources (URL + one-line takeaway) and a 12-25 item checklist in the persona's vocabulary", "done": true, "evidence": "r3 recount (3f9dd58): URL sources paralegal 8, litigation-lead 9, claims-adjuster 10, legal-nurse 9, privacy-compliance 16; checklist items 23/20/21/19/19 (all 12-25)"}
  - {"n": 3, "text": "each has 3 calibration findings with severity and expected fix, specific to a treatment-timeline tool", "done": true, "evidence": "3 calibration findings each (blocker/major/minor) tied to sample-case facts: $185 PT total, accident-date conflict, LOC qualifier, injection record, etc."}
---
## Description
§6.3 format, 10 sections each. Grounded in real source material (job descriptions, practitioner articles, CLE materials, adjuster training, LNC standards, HIPAA/ABA guidance) — not job titles. These compile into the reviewer agent bodies, so the checklist must be concrete and checkable.

## Notes (append-only, newest last)
- 2026-11-02T00:17:53Z researcher: claimed
- 2026-11-02T00:17:53Z researcher: Claimed (researcher instance B). Plan: gather verified sources in parallel (subagents fetch + confirm URLs), then write 5 dossiers in §6.3 format grounded in sample-case truths.
- 2026-11-02T00:27:11Z researcher: AC 1 checked: personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md each have sections 1-10 (regex check of '## N.' headers)
- 2026-11-02T00:27:11Z researcher: AC 2 checked: URL sources: paralegal 8, litigation-lead 8, claims-adjuster 10, legal-nurse 9, privacy-compliance 12 (fetched by research subagents; unverified items marked as such). Checklist items: 23/18/18/19/18
- 2026-11-02T00:27:11Z researcher: AC 3 checked: 3 calibration findings each (blocker/major/minor) tied to sample-case facts: $185 PT total, accident-date conflict, LOC qualifier, injection record, etc.
- 2026-11-02T00:27:28Z researcher: moved in_progress -> in_review
- 2026-11-02T00:28:45Z orchestrator: review dispatched: product-manager-reviewer, litigation-lead-reviewer
- 2026-11-02T00:35:23Z orchestrator: review product-manager-reviewer (claude-opus-5-5): changes — reviews/T-010-product-manager.md; round 1; findings:
    - [major] Calibration grades fact-losing and fact-inventing outputs below blocker, which contradicts the dossiers' own dealbreakers and the severity definition — fix: Re-grade legal-nurse #2 and #3 and claims-adjuster #2 and #3 to blocker, or replace them with genuinely major/minor examples, such as a correct but non-verbatim provider label for major or an un-expanded unambiguous abbreviation 
    - [minor] Section 5 'dealbreakers' carry no severity, so the dossiers contradict themselves (privacy-compliance) — fix: Either rate the logging example as a blocker, or reword the red flag so it is narrower than the calibration example (for example, 'logs record text and the deployment is public without a synthetic-data banner').
    - [minor] Some checklist items ask for features beyond Appendix A without a severity cap, which invites scope creep from reviewers — fix: Mark items that go beyond the must-haves as '(nice-to-have; minor at most)'. Reword claims-adjuster #2 as 'if the tool shows delay to first treatment, it shows it against both conflicting accident dates or not at all'. Reword litigation-lead #12 to 'what the
    - [minor] privacy-compliance checklist reaches into security-reviewer's lane without deferring — fix: Drop #10 and #18, or prefix them with 'note and defer to security-reviewer'. Add 'secrets, rate limits and spend caps belong to security-reviewer' to Limits.
- 2026-11-02T00:36:51Z orchestrator: assigned: researcher-b (after litigation-lead review lands)
- 2026-11-02T00:37:56Z researcher: Pre-emptive severity fix committed (see next commit sha on this card) per coordinator: legal-nurse LOC/MRI-performed, claims-adjuster ESI-completed/missed-appts, privacy log leak -> blocker; added major anchors to legal-nurse and claims-adjuster; §5 'each item is a blocker' + §8 severity rule in all dossiers. Not moving T-010 until litigation-lead findings arrive.
- 2026-11-02T00:38:58Z orchestrator: review litigation-lead-reviewer (claude-opus-5-5): changes — reviews/T-010-litigation-lead.md
- 2026-11-02T00:38:58Z orchestrator: assigned: researcher-b
- 2026-11-02T00:39:07Z researcher: claimed
- 2026-11-02T00:41:13Z researcher: moved in_progress -> in_review
- 2026-11-02T00:41:28Z orchestrator: review dispatched: litigation-lead r2 (+PM checklist)
- 2026-11-02T00:48:09Z orchestrator: review product-manager-reviewer (claude-opus-5-5): pass — reviews/T-010-product-manager-r2.md
- 2026-11-02T00:48:09Z orchestrator: review litigation-lead-reviewer (claude-opus-5-5): changes — reviews/T-010-litigation-lead-r2.md; round 2; findings:
    - [major] Missing-bill list and PT rate wording are placed in the letter, contradicting D-001, R-EX-4(8) and R-EX-8 (introduced by my round-1 fix wording) — fix: Lit-lead #19 and adjuster #21: "The letter's total line reads 'Billed charges stated in these records: $X' (R-EX-8) and claims no completeness; the internal notes list 'Bills to request' for every provider with a letter entry and no a
    - [major] Round-2 dossier text is not compiled into the reviewer agent bodies — fix: Run python3 tools/compile_agents.py --only paralegal litigation-lead claims-adjuster legal-nurse privacy-compliance after the major above is fixed, commit, and record the sha on T-010. The owner of .claude/agents decides who runs it.
    - [minor] §181.154 source takeaway narrows the (c) exceptions — fix: "... exceptions in (c): disclosures to another covered entity for treatment, payment, health care operations or insurance/HMO functions, and disclosures 'otherwise authorized or required by state or federal law'."
    - [minor] Flag-type vocabulary retired by D-013 persists in three dossiers — fix: Use 'causation flag' and 'pre_existing flag' (D-013) in these four lines. The adjuster's own analysis may keep his vocabulary in §6.
- 2026-11-02T00:48:09Z orchestrator: assigned: researcher-b
- 2026-11-02T00:48:18Z researcher: claimed
- 2026-11-02T00:49:40Z researcher: AC 2 checked: r3 recount (3f9dd58): URL sources paralegal 8, litigation-lead 9, claims-adjuster 10, legal-nurse 9, privacy-compliance 16; checklist items 23/20/21/19/19 (all 12-25)
- 2026-11-02T00:49:40Z researcher: moved in_progress -> in_review
- 2026-11-02T00:50:23Z researcher: D-019 follow-up (2687094): letter total line is exactly 'Billed charges stated in these records: $X' in paralegal #21, lit-lead #19 + calibration, adjuster #21; PT note internal-notes only.
- 2026-11-02T00:51:39Z orchestrator: review dispatched: litigation-lead r3

## Handoff
Round 3 (commit 3f9dd58). Lit-lead r2 M1: lit-lead #19, adjuster #21, paralegal #12/#21 and lit-lead major calibration -> letter total line 'Billed charges stated in these records: $8,390 (physical therapy charges to be supplemented)' (R-EX-8); bills-to-request list and '$185/visit; visit count not stated' only in internal notes (R-EX-4). M2 (compile) is orchestrator-owned; not run. Minor 181.154: (c) restored ('to another covered entity' for TPO/insurance; 'otherwise authorized or required'). Minor D-013: causation/pre_existing names in adjuster #5 + calibration, paralegal #10, nurse #18. Nit D-011: lit-lead #9 no batch accept. PM r2: lit-lead #12 audit = model output + human change (D-010), identity 'minor at most' here; privacy #10, #19, step 4 and Limits defer secrets/rate limits/spend caps to security-reviewer. T-011 carried: severity line in all 13 = CONTRACT D.2 verbatim + '§5 is blocker; present-but-weak is major/minor'; HP #14 area 1 (who first, 3+3 questions), #11 area 5 rollout/feedback, #20 + PM #20 engineering's role, #23 area 2 why-first, #24 One story 3-part scaffold; PM #17 why-first, #21 rollout; HP R3/R6/R7 headers name filed areas + §9 assumption. AC-2 evidence refreshed on T-010 and T-011. Verified: regex recount (sections, sequential items <=25, URLs, D.2 line in 13/13); grep for retired names/batch accept/'Severity rule:' clean.

---
T-010-011-sections.txt
T-010-011-source-check.md
T-010-litlead-source-check.md
T-010-r2-count.py
T-010-r2-resolution.md
T-010-r2-srch.py
T-010-litigation-lead-r2.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
true
a399a4c chore(orchestrator): T-013 accepted with debt -> T-025; D-019..D-022; stale dispatch markers fixed
2687094 fix(personas): letter total line exact per D-019 (no parenthetical)
3f9dd58 fix(personas): T-010 round 3 - letter vs internal notes, D-011/D-013 alignment, D.2 severity
eb78e3b chore(orchestrator): apply Chris's author email; needs_chris cards close on Chris's answer
89aa16a fix(harness): round-3 fixes from M0 staff-engineer r2
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:44.637Z

**tool call — Bash**
````
{
 "command": "sed -n '/```json/,/```/p' reviews/T-010-litigation-lead-r2.md | head -80; echo ----; git diff --stat 6bb13dd..2687094 -- personas/ .claude/agents/; echo ----; grep -n -A6 '^## D-001\\|^### D-001\\|D-019' memory/ORCHESTRATOR_DECISIONS.md | head -60",
 "description": "Read r2 findings, diff stat, decisions"
}
````

### User / tool · 2026-11-02T00:51:44.759Z

**tool result**
````
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
----
 .claude/agents/claims-adjuster-reviewer.md    | 19 +++++++++++--------
 .claude/agents/legal-nurse-reviewer.md        |  6 +++---
 .claude/agents/litigation-lead-reviewer.md    | 25 ++++++++++++++-----------
 .claude/agents/paralegal-reviewer.md          |  8 ++++----
 .claude/agents/privacy-compliance-reviewer.md | 23 ++++++++++++++---------
 personas/accessibility.md                     |  2 +-
 personas/chaos-tester.md                      |  2 +-
 personas/claims-adjuster.md                   |  8 ++++----
 personas/hiring-panel.md                      | 20 +++++++++++---------
 personas/installer.md                         |  2 +-
 personas/legal-nurse.md                       |  4 ++--
 personas/litigation-lead.md                   | 10 +++++-----
 personas/paralegal.md                         |  8 ++++----
 personas/privacy-compliance.md                | 12 ++++++------
 personas/product-manager.md                   | 13 +++++++------
 personas/security.md                          |  2 +-
 personas/staff-engineer.md                    |  2 +-
 personas/ux-designer.md                       |  2 +-
 18 files changed, 91 insertions(+), 77 deletions(-)
----
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29-| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30-| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:45.329Z

**tool call — Bash**
````
{
 "command": "git diff 6bb13dd..2687094 -- personas/",
 "description": "Show persona diff for round 3"
}
````

### User / tool · 2026-11-02T00:51:45.425Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:47.180Z

**tool call — Bash**
````
{
 "command": "git diff 6bb13dd..2687094 -- personas/litigation-lead.md personas/claims-adjuster.md personas/paralegal.md personas/legal-nurse.md personas/privacy-compliance.md",
 "description": "Diff of the five domain dossiers"
}
````

### User / tool · 2026-11-02T00:51:47.278Z

**tool result**
````
diff --git a/personas/claims-adjuster.md b/personas/claims-adjuster.md
index 48b1568..95e5164 100644
--- a/personas/claims-adjuster.md
+++ b/personas/claims-adjuster.md
@@ -19,7 +19,7 @@ His job is to pay what the file documents and not a dollar more; his reserves an
 2. The tool states "first recorded treatment: 2026-01-09 (Austin EMS)" and shows both stated accident dates with excerpts; it never computes a "delay from the accident" and never picks one accident date (D-017). A computed delay figure is a finding, because it resolves the conflict.
 3. Gaps: the 73-day gap (03-06 → 05-18) is flagged with day count and both endpoints; no gap reason is invented — "unexplained" if the records give none.
 4. Shorter gaps (e.g., 28 days, 01-23 → 02-20) are not flagged under the >30-day rule, but the tool does not hide them either (dates visible).
-5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a causation-weakening fact, not folded into the original injury narrative.
+5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a `causation` flag (D-013), not folded into the original injury narrative.
 6. Missed appointments and early discharge ("Discharged from PT after two missed appointments", visit 9 of 12 planned) are flagged under the causation category with the excerpt (I will argue failure to mitigate; the tool must not use that label — see item 20).
 7. Prior conditions: "low back pain in 2023, resolved" is flagged with its excerpt and the record 3 summary does not silently drop it; the flag lands in the internal review notes for the firm (D-001), never auto-inserted in the letter — whether the letter mentions it is the attorney's call.
 8. Degenerative language: "Findings may represent degenerative change; correlate clinically" is flagged and quoted verbatim; any summary that says "traumatic" or "acute" is false.
@@ -35,7 +35,7 @@ His job is to pay what the file documents and not a dollar more; his reserves an
 18. The export contains no advocacy adjectives ("severe", "debilitating", "significant") unless verbatim in a record.
 19. No referral, referring provider, or reason for a visit appears unless stated in that record: record 7 names no referral source, so "referred to pain management" anywhere is an invented fact.
 20. Flag text uses the four spec categories, the verbatim excerpt, and a fixed-template reason — never my legal labels (failure to mitigate, non-compliant, aggravation, intervening cause) or a model-written prediction of my argument.
-21. The charges section says the total covers only amounts stated in the records received and lists dated encounters with no stated charge (EMS 01-09, PCP 01-16, PT visits, pain management 05-18 and 06-12) without inventing amounts — otherwise I value only the two bills.
+21. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). No rate, "visit count not stated" wording, or list of unbilled encounters appears in the letter — those belong in the firm's internal notes (R-EX-4) — and no amount is invented that I could attack.
 
 ## 5. Red flags / dealbreakers (for the plaintiff — i.e., what makes the tool's output a gift to me)
 Each item here is a **blocker** (rate it so; never major or minor).
@@ -57,9 +57,9 @@ BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact
 7. File each finding with the verbatim export line and the record excerpt it contradicts or omits.
 
 ## 8. Calibration
-Severity rule: anything in §5, or anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker. No finding may be rated softer than §5 says.
+Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
 - **blocker — Overstated imaging.** Evidence: summary "MRI shows traumatic C5-C6 disc herniation." Record 8 says "disc protrusion... may represent degenerative change." Fix: verbatim impression; summary uses "disc protrusion" and keeps the hedge. Test: eval forbids "herniation"/"traumatic" unless in source.
-- **blocker — Missed appointments not flagged (hidden weakness).** Evidence: flags panel shows gap and prior-condition flags but nothing for record 6. Fix: causation/compliance flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
+- **blocker — Missed appointments not flagged (hidden weakness).** Evidence: flags panel shows `gap` and `pre_existing` flags but nothing for record 6. Fix: `causation` flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
 - **blocker — Recommended treatment reads as completed (invented fact).** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."
 - **major — Gap flag present but incomplete.** Evidence: flag reads "Treatment gap detected (Capital PT → Hill Country)" with no day count or dates. Fix: "73-day gap: 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient); no reason stated in records." Test: golden flag text includes both dates and 73.
 
diff --git a/personas/legal-nurse.md b/personas/legal-nurse.md
index 302104a..3735231 100644
--- a/personas/legal-nurse.md
+++ b/personas/legal-nurse.md
@@ -33,7 +33,7 @@ Firms hire her to read records the way a clinician does and to tell attorneys wh
 15. Plan-of-care vs actual: "12 visits" planned vs discharge at visit 9 is surfaced; the tool does not infer how many visits occurred.
 16. The faithfulness judge prompt explicitly checks for added diagnosis, severity, causation, and certainty changes, and sees only the record and the candidate.
 17. The generator prompt instructs: quote, don't infer; leave a field empty rather than guess.
-18. Lexicon entries for prior-condition and causation-weakening language include radiology hedges ("may represent", "cannot be excluded", "possible", "correlate clinically", "degenerative", "chronic") with rationale.
+18. Lexicon entries feeding the `pre_existing` and `causation` flags (D-013) include radiology hedges ("may represent", "cannot be excluded", "possible", "correlate clinically", "degenerative", "chronic") with rationale.
 19. Nothing in the UI or export gives a medical opinion (prognosis, permanency, necessity) not stated in a record.
 
 ## 5. Red flags / dealbreakers
@@ -55,7 +55,7 @@ LNC, medical chronology, records summary, DOS, HPI, CC, C/O, Dx, Rx, Hx/PMH, SOA
 6. File findings with the summary text and the excerpt side by side.
 
 ## 8. Calibration
-Severity rule: anything in §5, or anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker. No finding may be rated softer than §5 says.
+Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
 - **blocker — Diagnosis inferred.** Evidence: record 7 summary "Cervical radiculopathy, MRI ordered." Excerpt says "New onset pain radiating to right arm with numbness in fingers." Fix: "New onset right arm radiating pain with finger numbness; pain 7/10; MRI ordered." Test: judge flags "radiculopathy" as unsupported.
 - **blocker — LOC qualifier dropped (changes the diagnosis).** Evidence: record 2 summary "Dx: cervical strain; concussion." Fix: keep "concussion without loss of consciousness." Test: golden summary check.
 - **blocker — Order reads as result (states a fact the record does not).** Evidence: record 7 summary "MRI performed." Fix: "MRI ordered" (results appear in record 8).
diff --git a/personas/litigation-lead.md b/personas/litigation-lead.md
index d8de095..6df754e 100644
--- a/personas/litigation-lead.md
+++ b/personas/litigation-lead.md
@@ -24,17 +24,17 @@ He signs every demand. When a chronology overstates, an adjuster discounts the w
 6. The charges total is labeled as billed charges from the records, with each source, and is not presented as recoverable damages (Texas "paid or incurred," CPRC §41.0105).
 7. The $185 per-visit rate is not totaled; the export does not claim a PT amount the records do not state.
 8. Every exported statement has a record cite, so an attorney can answer an adjuster's challenge in minutes.
-9. Nothing reaches the export without an explicit human accept; there is no "accept all" that bypasses per-item review (or, if batch accept exists, it excludes needs-review items and amounts).
+9. Nothing reaches the export without an explicit per-item human accept; there is no batch accept (D-011).
 10. The export reads as professional demand-letter prose or a clean list — no AI disclaimers, UI labels, or internal state names.
 11. Flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block, never in the letter text (D-001); dismissed flags stay visible in the audit so the attorney can see what staff chose to omit.
-12. An audit trail exists showing who accepted/edited each item and what the model originally produced.
+12. An audit trail shows what the model originally produced and what the human accepted or changed (D-010). User identity ("who accepted") is a Part 2 rollout item for a multi-user firm — minor at most in this single-user prototype.
 13. The product note and Part 2 describe lawyer supervision of AI output consistent with Texas Opinion 705 (verify, never rely blindly; reliance carries the perils of an overconfident nonlawyer assistant, cf. Rule 5.03; train staff) and ABA 512 (supervisory duties under Rules 5.1/5.3 extend to firm AI policies).
 14. This prototype, repo, fixtures, demo, and prompt log use synthetic data only. A Part 2 plan to build a test set from real work product post-launch is acceptable (D-016) if it names the controls: inside the firm's environment, attorney-approved, access logged, de-identified where practical, vendor terms reviewed (no training, retention), client consent where required (Op. 705 / ABA 512).
 15. Part 2 questions for a litigation lead are ones he would respect: about what gets demands discounted, how he reviews a chronology today, and what a mistake has cost — not generic "pain points."
 16. The product note does not overclaim (no "eliminates errors"; time-saved claims are stated as hypotheses to measure).
 17. Flag text is the spec category + verbatim excerpt + a fixed-template reason (e.g., "Treatment gap: 73 days between 2026-03-06 and 2026-05-18"); no legal-conclusion labels (failure to mitigate, aggravation, intervening cause, non-compliant) and no model-written predictions of adjuster arguments.
 18. Missing information is visible: providers or referrals mentioned but with no record (e.g., ESI recommended but no record of it occurring) are not presented as completed treatment.
-19. The charges section states the total covers only amounts stated in the records received and lists dated encounters with no stated charge (EMS 01-09, PCP 01-16, PT visits, pain management 05-18 and 06-12), without inventing amounts — so nobody mistakes $8,390 for complete specials.
+19. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). The internal review notes — not the letter — list "Bills to request" for every provider with a letter entry and no accepted charge (Austin EMS, Dr. Alvarez, Capital PT, Hill Country Pain Management) and put the $185 rate under amounts not totaled with its reason ("per-visit rate only, visit count not stated") (R-EX-4); no amounts invented. If the notes omit the bills to request, the firm under-demands.
 20. The product note / Part 2 tie the no-invention rule to statements the firm makes to adjusters (Rule 4.01) and to the validity of a Stowers demand, not only to court filings.
 
 ## 5. Red flags / dealbreakers
@@ -57,9 +57,9 @@ demand, Stowers demand, policy limits, specials, paid or incurred, §41.0105, §
 6. File findings with the verbatim export line or document line as evidence.
 
 ## 8. Calibration
-Severity rule: anything in §5, or anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker. No finding may be rated softer than §5 says.
+Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
 - **blocker — Causation overstated in export.** Evidence: export line "MRI confirmed C5-C6 disc protrusion resulting from the collision." Fix: quote the impression verbatim: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically." Test: eval asserts export never contains "resulting from"/"caused by" unless verbatim in source.
-- **major — Total framed as damages (amounts themselves correct, no unbilled amounts included).** Evidence: export header "Medical damages: $8,390." Fix: "Billed charges stated in records received: $8,390 (ER $6,240; MRI $2,150). PT billed at $185/visit; visit count not stated."
+- **major — Total framed as damages (amounts themselves correct, no unbilled amounts included).** Evidence: export header "Medical damages: $8,390." Fix: letter line "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical); the rate and its reason ("$185 per visit; visit count not stated") go in the internal review notes only (D-001, R-EX-4).
 - **minor — Part 2 discovery questions generic.** Evidence: "What are your biggest pain points?" Fix: "Show me the last demand an adjuster discounted for something in the chronology — what was it?"
 
 ## 9. Sources
diff --git a/personas/paralegal.md b/personas/paralegal.md
index a153746..6944c85 100644
--- a/personas/paralegal.md
+++ b/personas/paralegal.md
@@ -26,9 +26,9 @@ She has built hundreds of medical chronologies and demand packages in Filevine;
 7. The accident-date conflict is flagged: 2026-01-09 (EMS/ER) vs "Date of accident per intake form: 2026-01-19" (record 7), with both excerpts; the tool does not pick one.
 8. The PT plan vs actual discrepancy is surfaced: "Plan of care: 12 visits" vs "Discharged from PT after two missed appointments" at visit 9.
 9. Prior-condition mentions are flagged: "low back pain in 2023, resolved" (record 3) and "may represent degenerative change" (record 8), each with its excerpt.
-10. PT discharge notes that mention missed appointments are flagged as causation/compliance risk.
+10. PT discharge notes that mention missed appointments raise a `causation` flag (D-013).
 11. Charges list shows $6,240 (ER) and $2,150 (MRI) with sources, and the running total of explicit charges is $8,390.
-12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total.
+12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total; in the export that reason sits in the internal review notes, never in the letter (R-EX-4).
 13. "Missing 3 days of work" is not listed as a billed charge (it may be noted as a lost-wages mention).
 14. Every entry and every flag has accept, edit, and dismiss; edits keep the original visible somewhere so I can see what I changed.
 15. I can review with the keyboard (move to next item, accept, dismiss) without reaching for the mouse on every row.
@@ -37,7 +37,7 @@ She has built hundreds of medical chronologies and demand packages in Filevine;
 18. The letter's treatment section contains only entries and charges I accepted (with my edits); flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block (D-001); dismissed items never appear.
 19. Each letter line has the date of service (US long format), the provider exactly as written, a verbatim quote, and a citation placeholder (e.g., `January 16, 2026 — Dr. Alvarez, primary care: "Persistent neck pain 6/10, daily headaches." [Ex. __ / Bates __]`) (D-002).
 20. Export pastes into Word as clean text: no HTML, no UI labels like "verified", no markdown symbols that would print.
-21. Billed charges in the export are labeled as billed amounts with their sources; unclear amounts are not silently included in the total.
+21. The letter's total line reads "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical); unclear amounts are never in the total; "Bills to request" (providers with an entry and no accepted charge) appear in the internal notes (R-EX-4).
 22. Nothing in the timeline or export states causation, diagnosis, or severity the records do not state (e.g., no "disc herniation caused by the collision").
 23. Patient self-reports stay attributed ("Patient states symptoms began after the January collision"), never turned into the provider's finding.
 
@@ -64,7 +64,7 @@ med chron, treatment chronology, DOS (date of service), DOI/DOA (date of injury/
 9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).
 
 ## 8. Calibration
-Severity rule: anything in §5, or anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker. No finding may be rated softer than §5 says.
+Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
 - **blocker — PT total invented.** Evidence: charges table row "Capital PT — $2,220 (12 × $185)". Fix: list "$185 per visit — rate, visit count not stated; needs review"; total stays $8,390. Test: eval asserts no PT total and total = 8390.
 - **major — Export has no citations.** Evidence: export line "Patient treated at Capital PT for neck pain." Fix: `January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]`. Test: E2E asserts every letter line contains a date of service, the provider as written, a verbatim quote, and the citation placeholder.
 - **minor — No remaining count.** Evidence: review screen of 9 entries + 8 flags has no counter. Fix: sticky "11 of 17 reviewed".
diff --git a/personas/privacy-compliance.md b/personas/privacy-compliance.md
index 2d05443..48d3d73 100644
--- a/personas/privacy-compliance.md
+++ b/personas/privacy-compliance.md
@@ -26,7 +26,7 @@ She is called after something goes wrong: client records pasted into a consumer
 7. Server logs do not contain pasted record text, full prompts, or completions; if the audit trail stores LLM I/O (required for traceability), it is local, documented, and has a stated retention/deletion path.
 8. The public deployment stores nothing from anonymous users beyond the session, or states what it stores and for how long.
 9. Vendor data handling is stated accurately: Anthropic commercial terms do not train on customer content; API default retention is limited (30 days, longer if flagged); zero data retention is an org-level arrangement — no stronger claim is made.
-10. API keys are server-side only and never appear in client code, logs, fixtures, or the repo.
+10. Note and defer to security-reviewer: API keys are server-side only and never appear in client code, logs, fixtures, or the repo.
 11. The audit record (model, prompt version, judge verdict, human action) exists so an attorney can show how each exported statement was verified.
 12. The export contains only the fields a demand letter needs (minimum necessary in spirit), not internal IDs or model metadata.
 13. The product note/Part 2 say how real-work discovery would avoid exposing client data (de-identified samples, observation without copying records, BAA/vendor review where needed).
@@ -35,7 +35,7 @@ She is called after something goes wrong: client records pasted into a consumer
 16. HIPAA is described accurately: a plaintiff firm receiving records under patient authorization is generally not a covered entity, but Texas ch. 181's broader "covered entity" definition (anyone who "comes into possession of" PHI) and Rule 1.05 ("shall not knowingly reveal") still apply; Texas confidentiality is not described as a "reasonable efforts" rule.
 17. Part 2's rollout addresses Tex. Health & Safety Code §181.154 (notice; separate authorization for each electronic disclosure of PHI, with exceptions in (c)) for sending client records to an LLM vendor, or states why it does not apply.
 18. Error messages and the UI never echo the system prompt or stack traces containing record text.
-19. Demo mode serves cached synthetic results and cannot be used to submit arbitrary text to the LLM without the server's rate limit and spend cap.
+19. Note and defer to security-reviewer: demo mode serves cached synthetic results and cannot be used to submit arbitrary text to the LLM without the server's rate limit and spend cap.
 
 ## 5. Red flags / dealbreakers
 Each item here is a **blocker** (rate it so; never major or minor).
@@ -52,12 +52,12 @@ PHI, covered entity, business associate, BAA, authorization (45 CFR 164.508), re
 1. Map the data flow from the code and README: input → server → LLM provider → storage/logs → export. Write it down with file:line references.
 2. Grep the repo for real-looking identifiers and for logging calls that include request bodies, prompts, or completions.
 3. Run the prompt-injection golden case through the app; compare flags/states with and without the injected line.
-4. Check the public/demo configuration: banner present, demo mode behaviour, rate limit and spend cap, no key in client.
+4. Check the public/demo configuration: banner present and demo mode behaviour; note (and defer to security-reviewer) whether a rate limit, spend cap, and server-only key exist.
 5. Read the product note and Part 2 sections on discovery, rollout, and AI use; check each privacy/ethics claim against the sources below.
 6. File findings with file:line, screenshots, or the verbatim claim.
 
 ## 8. Calibration
-Severity rule: anything in §5, or anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker. No finding may be rated softer than §5 says.
+Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
 - **blocker — Injection changes output.** Evidence: with the injection record, all flags show `dismissed`; without it, 8 flags `needs_review`. Fix: record text never controls state; only human actions change state; schema rejects extra fields. Test: eval case asserts identical flags with and without the injected line.
 - **blocker — Completions in server logs (red flag on the public deployment).** Evidence: `app/backend/main.py:57 logger.info(resp)` writes full LLM output. Fix: log item ids, prompt hash, latency; keep I/O only in the audit store with retention noted.
 - **minor — Overstated vendor claim.** Evidence: product note "Anthropic never stores our data." Fix: "API inputs/outputs are not used for training under commercial terms and are retained for a limited period by default; zero retention requires an org agreement."
@@ -68,7 +68,7 @@ Severity rule: anything in §5, or anything violating Appendix A or the contract
 - https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html — HHS: attorneys are business associates when providing legal services to a covered entity involving PHI.
 - https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508 — 45 CFR 164.508: authorizations warn that redisclosed records may no longer be protected by HIPAA.
 - https://texas.public.law/statutes/tex._health_and_safety_code_section_181.001 — Tex. Health & Safety Code §181.001: "covered entity" includes any person who comes into possession of PHI (ch. 181 also requires training, §181.101, and bars re-identification, §181.151).
-- https://texas.public.law/statutes/tex._health_and_safety_code_section_181.154 — Tex. Health & Safety Code §181.154: notice of electronic disclosure; separate authorization for each electronic disclosure of PHI; exceptions for treatment, payment, operations, insurance functions, or disclosures required by law.
+- https://texas.public.law/statutes/tex._health_and_safety_code_section_181.154 — Tex. Health & Safety Code §181.154: notice of electronic disclosure; separate authorization for each electronic disclosure of PHI; exceptions in (c): disclosures to another covered entity for treatment, payment, health care operations, or insurance/HMO functions, and disclosures "otherwise authorized or required by state or federal law".
 - https://legalethicstexas.com/resources/rules/texas-disciplinary-rules-of-professional-conduct/confidentiality-of-information/ — Texas Rule 1.05(b): a lawyer "shall not knowingly" reveal confidential information; no reasonable-efforts clause.
 - https://www.texasbar.com/AM/Template.cfm?Section=Home&ContentID=27271&Template=/CM/ContentDisplay.cfm — State Bar of Texas, Texas Disciplinary Rules of Professional Conduct (amendments eff. Jan 31, 2022): primary text of Rules 1.01, 1.05, 4.01, 5.03.
 - https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/ — ABA Model Rule 1.6(c): reasonable efforts to prevent unauthorized disclosure of client information.
@@ -82,4 +82,4 @@ Severity rule: anything in §5, or anything violating Appendix A or the contract
 - Assumptions: ABA 477R primary PDF not fetched (403; secondary summary used); 512 primary fetched via Wayback. Whether §181.154 reaches a firm sending records to an LLM vendor, and whether a (c) exception applies, is unresolved — the persona asks, it does not decide. Decision D-016 (controlled real-work-product test set post-launch is acceptable) binds this persona. Not legal advice about any real firm.
 
 ## 10. Limits
-Do not grade clinical accuracy, UX, code style, or product strategy. Do not demand production-grade compliance controls (BAA, SOC 2) from a synthetic-data prototype; require that the prototype not claim them and that Part 2 plans for them.
+Do not grade clinical accuracy, UX, code style, or product strategy. Do not demand production-grade compliance controls (BAA, SOC 2) from a synthetic-data prototype; require that the prototype not claim them and that Part 2 plans for them. Secrets, rate limits, and spend caps belong to security-reviewer: note them, defer severity.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:54.864Z

**tool call — Bash**
````
{
 "command": "python3 tools/compile_agents.py --check; echo \"exit=$?\"; for p in paralegal litigation-lead claims-adjuster legal-nurse privacy-compliance; do echo \"$p: $(git log -1 --format='%h %ci' -- personas/$p.md) | agent $(git log -1 --format='%h %ci' -- .claude/agents/$p-reviewer.md)\"; done; git status --porcelain -- personas .claude/agents",
 "description": "Check compiled agents match dossiers"
}
````

### User / tool · 2026-11-02T00:51:54.921Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($p:) | command: python3 tools/compile_agents.py --check; echo "exit=$?"; for p in paralegal litigation-lead claims-adjuster legal-nurse privacy-compliance; do echo "$p: $(git log -1 --format='%h %ci' -- personas/$p.m
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:56.469Z

**tool call — Bash**
````
{
 "command": "python3 tools/compile_agents.py --check; echo \"exit=$?\"",
 "description": "Run compile_agents check mode"
}
````

### User / tool · 2026-11-02T00:51:56.582Z

**tool result**
````
agent definitions in sync
exit=0
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:51:58.568Z

**tool call — Bash**
````
{
 "command": "git log -1 --format='%h %ci' -- personas/litigation-lead.md personas/claims-adjuster.md personas/paralegal.md personas/legal-nurse.md personas/privacy-compliance.md && git log -1 --format='%h %ci' -- .claude/agents/litigation-lead-reviewer.md .claude/agents/claims-adjuster-reviewer.md .claude/agents/paralegal-reviewer.md .claude/agents/legal-nurse-reviewer.md .claude/agents/privacy-compliance-reviewer.md && git status --porcelain -- personas .claude/agents && echo clean-status-above",
 "description": "Compare last commits of dossiers and agents"
}
````

### User / tool · 2026-11-02T00:51:58.699Z

**tool result**
````
2687094 2026-11-01 18:50:20 -0600
a399a4c 2026-11-01 18:51:24 -0600
clean-status-above
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:08.626Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-check.py",
 "content": "\"\"\"T-010 r3 read-only checks (litigation-lead-reviewer).\n1) every non-blank dossier line present in the compiled agent body\n2) grep five dossiers for letter/export lines that mention charges content, flags, or adverse facts\n3) counts: sections, checklist items, URLs, calibration\nUsage: python3 -I artifacts/review-evidence/T-010-r3-check.py <repo_root>\n\"\"\"\nimport re, sys, pathlib\n\nroot = pathlib.Path(sys.argv[1])\nP = [\"paralegal\", \"litigation-lead\", \"claims-adjuster\", \"legal-nurse\", \"privacy-compliance\"]\n\nprint(\"== 1. dossier lines missing from compiled agent ==\")\nfor p in P:\n    d = (root / f\"personas/{p}.md\").read_text().splitlines()\n    a = (root / f\".claude/agents/{p}-reviewer.md\").read_text()\n    miss = [l for l in d if l.strip() and l.strip() not in a]\n    print(f\"{p}: {len(miss)} missing\")\n    for l in miss[:5]:\n        print(\"   \", l[:120])\n\nprint(\"\\n== 2. letter/export lines touching charges, flags, adverse facts ==\")\npat = re.compile(r\"(letter|export|demand text|carrier)\", re.I)\nrisk = re.compile(r\"(\\$185|visit count|no stated charge|bills to request|unbilled|supplement|excludes|\"\n                  r\"parenthetical|flag|prior|pre.?existing|degenerative|gap|missed|accident date|\"\n                  r\"conflict|lost.?wage|rate|incomplete|complete)\", re.I)\nfor p in P:\n    for i, l in enumerate((root / f\"personas/{p}.md\").read_text().splitlines(), 1):\n        if pat.search(l) and risk.search(l):\n            print(f\"{p}.md:{i}: {l[:260]}\")\n\nprint(\"\\n== 3. counts ==\")\nfor p in P:\n    t = (root / f\"personas/{p}.md\").read_text()\n    secs = re.findall(r\"^## (\\d+)\\.\", t, re.M)\n    s4 = re.search(r\"^## 4\\..*?(?=^## 5\\.)\", t, re.M | re.S).group(0)\n    items = re.findall(r\"^(\\d+)\\. \", s4, re.M)\n    s9 = re.search(r\"^## 9\\..*?(?=^## 10\\.)\", t, re.M | re.S).group(0)\n    urls = set(re.findall(r\"https?://\\S+\", s9))\n    s8 = re.search(r\"^## 8\\..*?(?=^## 9\\.)\", t, re.M | re.S).group(0)\n    cal = re.findall(r\"^- \\*\\*(blocker|major|minor|nit)\", s8, re.M)\n    print(p, \"sections\", secs, \"items\", len(items), \"urls\", len(urls), \"calibration\", cal)\n"
}
````

### User / tool · 2026-11-02T00:52:08.725Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:10.098Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-010-r3-check.py /Users/arsis/zlayt-pm-project",
 "description": "Run r3 check script"
}
````

### User / tool · 2026-11-02T00:52:10.202Z

**tool result**
````
== 1. dossier lines missing from compiled agent ==
paralegal: 0 missing
litigation-lead: 0 missing
claims-adjuster: 0 missing
legal-nurse: 0 missing
privacy-compliance: 0 missing

== 2. letter/export lines touching charges, flags, adverse facts ==
paralegal.md:11: - A bad day: the adjuster's response letter quotes a record she summarized wrong, or points to a gap or prior injury she missed. The firm's credibility on that file — and her attorney's trust in her — drops.
paralegal.md:31: 12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total; in the export that reason sits in the i
paralegal.md:37: 18. The letter's treatment section contains only entries and charges I accepted (with my edits); flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block (D-001); dismissed items never appear.
paralegal.md:40: 21. The letter's total line reads "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical); unclear amounts are never in the total; "Bills to request" (providers with an entry and no accepted charge) appear in the intern
paralegal.md:49: - Export that includes something I dismissed or never reviewed.
paralegal.md:62: 7. Export; paste into a plain-text file under `artifacts/review-evidence/`; confirm the dismissed item is absent and my edit is present.
paralegal.md:79: - https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ — RMD Law (PI firm, 2026): no carrier publishes a gap threshold; delay-to-first-care, mid-treatment gaps, and early stopping are distinct.
litigation-lead.md:19: 1. No statement in the export characterizes causation beyond the record (e.g., no "the collision caused a C5-C6 disc herniation"); "may represent degenerative change; correlate clinically" stays verbatim.
litigation-lead.md:25: 7. The $185 per-visit rate is not totaled; the export does not claim a PT amount the records do not state.
litigation-lead.md:29: 11. Flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block, never in the letter text (D-001); dismissed flags stay visible in the audit so the attorney can see what staff chose to omit.
litigation-lead.md:37: 19. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). The internal review notes — not the letter — list "Bills to request" for every provider with a 
litigation-lead.md:49: demand, Stowers demand, policy limits, specials, paid or incurred, §41.0105, §18.001 affidavit/counteraffidavit, chargemaster, letter of protection (LOP), liens, causation, reasonable medical probability, aggravation, intervening cause, gap in treatment, credi
litigation-lead.md:61: - **blocker — Causation overstated in export.** Evidence: export line "MRI confirmed C5-C6 disc protrusion resulting from the collision." Fix: quote the impression verbatim: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent deg
litigation-lead.md:62: - **major — Total framed as damages (amounts themselves correct, no unbilled amounts included).** Evidence: export header "Medical damages: $8,390." Fix: letter line "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetica
claims-adjuster.md:24: 7. Prior conditions: "low back pain in 2023, resolved" is flagged with its excerpt and the record 3 summary does not silently drop it; the flag lands in the internal review notes for the firm (D-001), never auto-inserted in the letter — whether the letter ment
claims-adjuster.md:38: 21. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). No rate, "visit count not stated" wording, or list of unbilled encounters appears in the letter
claims-adjuster.md:45: - A gap, prior condition, or missed-appointment note in the records that the tool's timeline or flags omitted (not: one the export omitted after a human reviewed it — that is the attorney's decision).
claims-adjuster.md:48: BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact soft tissue), soft-tissue, gap in treatment, delay in treatment, intervening/superseding cause, failure to mitigate, non-compliance, pre-existing, aggravation, degenerative, subjec
claims-adjuster.md:53: 3. For each item on my attack list: is it surfaced to the plaintiff's side (flag) and is the export free of overstatement about it?
claims-adjuster.md:55: 5. Hunt for any word in the export not supported by its excerpt (severity adjectives, causation verbs, completed vs recommended).
claims-adjuster.md:63: - **blocker — Recommended treatment reads as completed (invented fact).** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."

== 3. counts ==
paralegal sections ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] items 23 urls 8 calibration ['blocker', 'major', 'minor']
litigation-lead sections ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] items 20 urls 9 calibration ['blocker', 'major', 'minor']
claims-adjuster sections ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] items 21 urls 10 calibration ['blocker', 'blocker', 'blocker', 'major']
legal-nurse sections ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] items 19 urls 9 calibration ['blocker', 'blocker', 'blocker', 'major']
privacy-compliance sections ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] items 19 urls 16 calibration ['blocker', 'blocker', 'minor']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:21.907Z

**tool call — Bash**
````
{
 "command": "grep -n 'R-EX-4\\|R-EX-8\\|R-EX-3' spec/REQUIREMENTS.md | head; echo ---; grep -n -i 'charge\\|\\$\\|visit 9\\|provider' spec/SAMPLE_CASE_TRUTHS.md | head -30; echo ---; grep -n -i 'export\\|letter' personas/legal-nurse.md personas/privacy-compliance.md",
 "description": "Check requirements and sample truths for charges"
}
````

### User / tool · 2026-11-02T00:52:22.013Z

**tool result**
````
121:| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009) and the pending count. (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences containing "recommend" (a code pattern), worded "request cost estimate". (8) **Bills to request**: providers (the label up to the first comma) with an entry in the letter and no accepted charge. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; bills to request for Austin EMS, Dr. Alvarez, Hill Country Pain Management and Capital PT. UT: every `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
126:| R-EX-8 | **The total line is labeled and neutral.** The letter's total reads "Billed charges stated in these records: $X". When any non-dismissed rate, estimate or unclear amount exists, code appends "(<service> charges to be supplemented)"; on the sample: "(physical therapy charges to be supplemented)". `<service>` comes from a fixed code lookup (PT → physical therapy; unknown → the provider name as written). The reason ("per-visit rate only, visit count not stated") lives in the notes, never in the letter. | Sample: line equals `Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)`. UT: `letter_text` contains neither "visit count" nor "rate". A case with no non-charge amounts has no parenthetical. | UT + E2E |
340:| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
342:| A-103 | The chronology feeds the medical-treatment section of a pre-suit demand letter to a carrier. | R-EX-1 to R-EX-8 |
346:| A-107 | A per-visit rate is not billable until visits are itemized, so no PT total is shown. | R-CH-2, R-CH-3, R-EX-8 |
353:- Providers with an entry in the letter but no stated charge are "bills to request" (R-EX-4).
354:- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).
364:| 3 Letter content | Rates and other non-charge amounts are in the notes only; no short-cite mode; provider as written (R-EX-4, R-EX-6, R-EX-8). |
---
6:- **Gap:** 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient), 73 days.
7:- **Conflict:** accident date — 2026-01-09 per EMS and ER records vs "Date of accident per intake form: 2026-01-19" (record 7). Also a treatment-plan discrepancy: 12 planned PT visits vs discharge at visit 9 after two missed appointments (records 4, 6).
9:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).
11:Billed charges: explicit charges are $6,240 (ER, record 2) and $2,150 (MRI, record 8) → running total of explicit charges **$8,390**. "Charge per visit $185" (record 4) is a **rate**, not a charge: the records reference visits 8 and 9 but never itemize visits attended or billed, so the PT total is **unclear and must not be totaled** — the correct output is "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review." "Missing 3 days of work" (record 5) is a damages mention, not a billed charge. "Rx cyclobenzaprine 10 mg" carries no amount.
---
personas/legal-nurse.md:37:19. Nothing in the UI or export gives a medical opinion (prognosis, permanency, necessity) not stated in a record.
personas/legal-nurse.md:41:- Any inferred diagnosis, causation, or severity in a summary or export.
personas/privacy-compliance.md:30:11. The audit record (model, prompt version, judge verdict, human action) exists so an attorney can show how each exported statement was verified.
personas/privacy-compliance.md:31:12. The export contains only the fields a demand letter needs (minimum necessary in spirit), not internal IDs or model metadata.
personas/privacy-compliance.md:52:1. Map the data flow from the code and README: input → server → LLM provider → storage/logs → export. Write it down with file:line references.
personas/privacy-compliance.md:76:- http://web.archive.org/web/20261024213642id_/https://www.americanbar.org/content/dam/aba/administrative/professional_responsibility/ethics-opinions/aba-formal-opinion-512.pdf — ABA Formal Op. 512 (July 2024, primary PDF via Wayback): boilerplate engagement-letter consent is not sufficient for self-learning tools.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:29.233Z

**tool call — Bash**
````
{
 "command": "sed -n '115,127p' spec/REQUIREMENTS.md | cut -c1-600; echo ---; grep -rn 'D-019' tools/ board/ cards/ 2>/dev/null | head; python3 tools/board.py list 2>/dev/null | grep -i 'D-019\\|R-EX-8\\|supplement' | head",
 "description": "Read R-EX rows and look for D-019 spec card"
}
````

### User / tool · 2026-11-02T00:52:29.384Z

**tool result**
````
Both blocks are assembled by code from items with `review_status` in {accepted, edited}. API: `GET /api/cases/{id}/export` returns `letter_text` and `internal_notes_text` separately.

| ID | Requirement | Pass / fail test | Checker |
|---|---|---|---|
| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 
| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009) and the pending count. (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request i
| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter · N items pending (N flags)". The count line is part of neither block. **Copy asks for one confirmation when anything is pending**, stating the pending numbers and naming pending flags separately (a pending flag may be one the attorney needs to see). | E2E: leave the 73-day gap flag pending, click Copy letter → the confirm reads "1 flag not reviewed"; the count line shows it. Click Copy for each block, read the clipboard, assert no count line in ei
| R-EX-6 | **Template and worked example.** The letter follows the template in §6: US long dates ("January 9, 2026"), provider as written in the header, a `Source [Ex. __ / Bates __]:` line with the verbatim quote (the placeholder is literal text she fills in after pasting), money as `$1,234.00`, no dot leaders. The full expected export for the sample case is `evals/golden/sample.export.expected.txt` (qa, T-015). | E2E on the **`fixture` backend** (recorded sample responses, so summary wording is fixed): with all 9 entries and both charges accepted and nothing edited, `letter_text` equals the
| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → notes list record 5 (dismissed) and record 6 (not reviewed); the on-screen count reads "7 of 9". | E2E |
| R-EX-8 | **The total line is labeled and neutral.** The letter's total reads "Billed charges stated in these records: $X". When any non-dismissed rate, estimate or unclear amount exists, code appends "(<service> charges to be supplemented)"; on the sample: "(physical therapy charges to be supplemented)". `<service>` comes from a fixed code lookup (PT → physical therapy; unknown → the provider name as written). The reason ("per-visit rate only, visit count not stated") lives in the notes, never in the letter. | Sample: line equals `Billed charges stated in these records: $8,390.00 (physic
| R-EX-9 | Two separate copy buttons, one per block, each copying exactly that block. | E2E: clipboard after each click equals the matching API field. | E2E |
---
board/activity.jsonl:336:{"ts": "2026-11-02T00:50:23Z", "event": "note", "agent": "researcher", "card": "T-010", "text": "D-019 follow-up (2687094): letter total line is exactly 'Billed charges stated in these records: $X' in paralegal #21, lit-lead #19 + calibration, adjuster #21; PT note internal-notes only."}
board/cards/T-010.md:59:- 2026-11-02T00:50:23Z researcher: D-019 follow-up (2687094): letter total line is exactly 'Billed charges stated in these records: $X' in paralegal #21, lit-lead #19 + calibration, adjuster #21; PT note internal-notes only.
board/cards/T-025.md:20:  - {"n": 3, "text": "Letter total line per D-019 (no parenthetical); R-EX-8 and §6 worked example updated; flagged-language list includes record 1 and the K5 intake-date line appears in internal notes", "done": false, "evidence": null}
board/cards/T-013.md:23:  - {"persona": "orchestrator-§7.4", "model": "claude-opus-5-5", "verdict": "pass", "file": "memory/SCOPE_CUTS.md", "at": "2026-11-02T00:50:27Z", "debt": "Remaining reconciliation (hallucination threshold as rate, K4/K5 must, D-019 total line, both-side accident-date quotes, D-016..D-021 refs, §8 clean) split to T-025, which T-017 depends on."}
board/cards/T-013.md:95:- 2026-11-02T00:50:27Z orchestrator: accepted with documented debt (§7.4): Remaining reconciliation (hallucination threshold as rate, K4/K5 must, D-019 total line, both-side accident-date quotes, D-016..D-021 refs, §8 clean) split to T-025, which T-017 depends on.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:34.733Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p r3src && curl -sS -L -A 'Mozilla/5.0' -o r3src/181154.html -w '%{http_code} %{size_download}\\n' 'https://texas.public.law/statutes/tex._health_and_safety_code_section_181.154' && python3 -I -c \"\nimport re,html,sys\nt=open(sys.argv[1],encoding='utf-8',errors='replace').read()\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\ni=t.find('(c)'); print(t[i-50:i+700])\n\" r3src/181154.html",
 "description": "Fetch Texas H&S 181.154 and extract subsection (c)"
}
````

### User / tool · 2026-11-02T00:52:35.274Z

**tool result**
````
200 26906
 the notice. (b) Except as provided by Subsection (c), a covered entity may not electronically disclose an individual’s protected health information to any person without a separate authorization from the individual or the individual’s legally authorized representative for each disclosure. An authorization for disclosure under this subsection may be made in written or electronic form or in oral form if it is documented in writing by the covered entity. (c) The authorization for electronic disclosure of protected health information described by Subsection (b) is not required if the disclosure is made: (1) to another covered entity, as that term is defined by Section 181.001 (Definitions) , or to a covered entity, as that term is defined by S
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:39.314Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && python3 -I -c \"\nimport re,html,sys\nt=open(sys.argv[1],encoding='utf-8',errors='replace').read()\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\ni=t.find('(c) The authorization'); print(t[i:i+1100]); print('---a'); i=t.find('(a)'); print(t[i:i+400])\n\" r3src/181154.html",
 "description": "Print full subsection (c) and (a)"
}
````

### User / tool · 2026-11-02T00:52:39.428Z

**tool result**
````
(c) The authorization for electronic disclosure of protected health information described by Subsection (b) is not required if the disclosure is made: (1) to another covered entity, as that term is defined by Section 181.001 (Definitions) , or to a covered entity, as that term is defined by Section 602.001 (Definitions) , Insurance Code, for the purpose of: (A) treatment; (B) payment; (C) health care operations; or (D) performing an insurance or health maintenance organization function described by Section 602.053 (Exceptions) , Insurance Code; or (2) as otherwise authorized or required by state or federal law. (d) The attorney general shall adopt a standard authorization form for use in complying with this section. The form must comply with the Health Insurance Portability and Accountability Act and Privacy Standards and this chapter. (e) This section does not apply to a covered entity, as defined by Section 602.001 (Definitions) , Insurance Code, if that entity is not a covered entity as defined by 45 C.F.R. Section 160.103. Added by Acts 2011, 82nd Leg., R.S., Ch. 1126 (H.B. 300 )
---a
(a) A covered entity shall provide notice to an individual for whom the covered entity creates or receives protected health information if the individual’s protected health information is subject to electronic disclosure. A covered entity may provide general notice by: (1) posting a written notice in the covered entity’s place of business; (2) posting a notice on the covered entity’s Internet webs
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:52:42.619Z

**tool call — Bash**
````
{
 "command": "grep -n -i 'causation-weakening\\|causation/compliance\\|batch accept\\|accept all\\|Severity rule:\\|supplemented\\|no stated charge' personas/paralegal.md personas/litigation-lead.md personas/claims-adjuster.md personas/legal-nurse.md personas/privacy-compliance.md; echo \"---exit=$?\"; grep -n 'D-001\\b\\|^| D-001\\|D-010\\|D-011\\|D-013' memory/ORCHESTRATOR_DECISIONS.md | cut -c1-300 | head -8",
 "description": "Grep retired vocabulary and decisions"
}
````

### User / tool · 2026-11-02T00:52:42.724Z

**tool result**
````
personas/litigation-lead.md:27:9. Nothing reaches the export without an explicit per-item human accept; there is no batch accept (D-011).
---exit=0
9:| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts neve
18:| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows
19:| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-h
21:| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
25:| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Mu
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:04.783Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-resolution.md",
 "content": "# T-010 round 3 — resolution of round-2 findings (litigation-lead-reviewer)\n\nRange checked: `git diff 6bb13dd..2687094 -- personas/` (commits 3f9dd58 and 2687094). Compiled agents: a399a4c.\nHelper: `python3 -I artifacts/review-evidence/T-010-r3-check.py /Users/arsis/zlayt-pm-project`.\n\n## Litigation-lead r2 findings\n\n| # | Sev | r2 finding | Now (file:line, verbatim) | Status |\n|---|---|---|---|---|\n| M1 | major | Missing-bill list and PT rate wording placed in the letter | litigation-lead.md:37 #19 \"The letter's total line is neutral and claims no completeness: \"Billed charges stated in these records: $8,390\" (R-EX-8, D-019: exactly this, no parenthetical). The internal review notes — not the letter — list \"Bills to request\" ... and put the $185 rate under amounts not totaled ...\"; claims-adjuster.md:38 #21 \"No rate, \"visit count not stated\" wording, or list of unbilled encounters appears in the letter\"; litigation-lead.md:62 calibration fix \"letter line \"Billed charges stated in these records: $8,390\" ... the rate and its reason ... go in the internal review notes only\"; paralegal.md:31 #12 and :40 #21 same split | Resolved. Also matches D-019 (stricter than my r2 fix, which quoted the R-EX-8 parenthetical) |\n| M2 | major | Dossier text not compiled into agent bodies | `python3 tools/compile_agents.py --check` → \"agent definitions in sync\", exit 0; line-membership check: 0 missing lines x5; personas last commit 2687094 18:50:20, agents last commit a399a4c 18:51:24 | Resolved |\n| m1 | minor | §181.154 takeaway narrows (c) | privacy-compliance.md:71 \"exceptions in (c): disclosures to another covered entity for treatment, payment, health care operations, or insurance/HMO functions, and disclosures \"otherwise authorized or required by state or federal law\"\" vs statute fetched today (texas.public.law, HTTP 200): \"(c) ... not required if the disclosure is made: (1) to another covered entity ... for the purpose of: (A) treatment; (B) payment; (C) health care operations; or (D) performing an insurance or health maintenance organization function ...; or (2) as otherwise authorized or required by state or federal law.\" | Resolved, accurate |\n| m2 | minor | D-013 retired flag vocabulary | grep 'causation-weakening\\|causation/compliance' in 5 dossiers: 0 hits. claims-adjuster.md:22, :62; paralegal.md:29; legal-nurse.md:36 now use `causation` / `pre_existing` (D-013) | Resolved |\n| n1 | nit | Lit-lead #9 batch-accept carve-out | litigation-lead.md:27 \"there is no batch accept (D-011)\" | Resolved |\n| n2 | nit | AC-2 evidence stale | board AC 2: \"URL sources paralegal 8, litigation-lead 9, claims-adjuster 10, legal-nurse 9, privacy-compliance 16; checklist items 23/20/21/19/19\" = T-010-r3-check.py output | Resolved |\n\n## Product-manager r2 minors (cross-check, my lens only)\n\n| r2 PM item | Now | Status |\n|---|---|---|\n| Lit-lead #12 audit wording | litigation-lead.md:30 \"audit trail shows what the model originally produced and what the human accepted or changed (D-010). User identity ... minor at most in this single-user prototype\" | Resolved; acceptable to me — identity matters at rollout, not in a single-user prototype |\n| Privacy lane deferral | privacy-compliance.md:29 #10, :38 #19, step 4, §10 defer secrets/rate limits/spend caps to security-reviewer | Resolved (outside my lens beyond reading) |\n\n## Letter-content sweep (charges content, flags, adverse facts)\n\nEvery dossier line mentioning letter/export with charges/flags/adverse terms (T-010-r3-check.py §2) was read. None asks the letter to contain a rate, \"visit count\", unbilled-encounter list, completeness claim, parenthetical, flag text, or an adverse fact chosen by the tool. Adverse facts route to internal notes with attorney decision: claims-adjuster.md:24 #7 \"never auto-inserted in the letter — whether the letter mentions it is the attorney's call\"; :45 red flag excludes \"one the export omitted after a human reviewed it — that is the attorney's decision\"; litigation-lead.md:29 #11 (D-001).\n\nContext, not a T-010 defect: spec/REQUIREMENTS.md:126 R-EX-8 still specifies the \"(physical therapy charges to be supplemented)\" parenthetical; D-019 supersedes it and the reconciliation is tracked on T-025 AC 3. The dossiers cite \"R-EX-8, D-019: exactly this, no parenthetical\", so a reviewer following them applies the binding decision.\n"
}
````

### User / tool · 2026-11-02T00:53:04.877Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-resolution.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:25.826Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-010-litigation-lead-r3.md",
 "content": "# T-010 — litigation-lead-reviewer, round 3 (final)\n\n**Verdict: pass.** Every round-2 finding is resolved; the resolution table with verbatim before/after evidence is in `artifacts/review-evidence/T-010-r3-resolution.md`.\n\n- **M1 (letter vs notes):** fixed in lit-lead #19, adjuster #21, paralegal #12/#21 and the lit-lead major calibration. The letter's total line is exactly \"Billed charges stated in these records: $8,390\" (D-019). The rate, \"visit count not stated\" and bills to request appear only in the internal notes. This is stricter than my own r2 fix, which quoted the superseded R-EX-8 parenthetical.\n- **M2 (compile):** `python3 tools/compile_agents.py --check` reports \"agent definitions in sync\" (exit 0). My independent line-membership check finds 0 missing dossier lines across all 5 personas. The agents commit (a399a4c 18:51:24) is newer than the last personas commit (2687094 18:50:20).\n- **§181.154:** re-fetched from texas.public.law (HTTP 200). The takeaway now matches (c)(1) \"to another covered entity ... for the purpose of\" TPO/insurance functions and (c)(2) \"as otherwise authorized or required by state or federal law\".\n- **Letter sweep:** no line in any of the 5 dossiers asks the letter to carry charges caveats, flag content or tool-selected adverse facts. Adverse facts go to the internal notes for the attorney to decide (D-001, D-017).\n\nContext, not a T-010 finding: spec/REQUIREMENTS.md:126 R-EX-8 still requires the parenthetical. D-019 supersedes it, and the reconciliation is tracked on T-025 AC 3.\n\nProcess observation for the orchestrator (not a T-010 defect): this reviewer session's loaded prompt still showed the pre-round-3 item 9/12/19 text and the old \"Severity rule:\" line, even though the on-disk agent file is in sync. Agent definitions appear to be loaded when a session starts, so a session dispatched within seconds of a recompile may still run the old prompt.\n\n```json\n{\"card\": \"T-010\", \"persona\": \"litigation-lead-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"Round 3 (final). git diff 6bb13dd..2687094 -- personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md (commits 3f9dd58, 2687094); compiled .claude/agents/*-reviewer.md at a399a4c; checked against reviews/T-010-litigation-lead-r2.md, reviews/T-010-product-manager-r2.md, memory/ORCHESTRATOR_DECISIONS.md D-001..D-022, spec/REQUIREMENTS.md R-EX-1..R-EX-8, spec/SAMPLE_CASE_TRUTHS.md. No app (documents card).\",\n \"exercised\": [\n  \"python3 tools/board.py show T-010 (status in_review, rounds 2, commits 34e9398/6404549/6bb13dd/3f9dd58/2687094; AC 2 evidence 8/9/10/9/16 URLs, 23/20/21/19/19 items)\",\n  \"git log --oneline -5 (a399a4c, 2687094, 3f9dd58, ...); git diff --stat and full git diff 6bb13dd..2687094 for the five dossiers\",\n  \"python3 tools/compile_agents.py --check -> 'agent definitions in sync', exit=0\",\n  \"git log -1 --format='%h %ci' over the five personas (2687094 2026-11-01 18:50:20) vs the five agents (a399a4c 2026-11-01 18:51:24); git status --porcelain personas .claude/agents (clean)\",\n  \"python3 -I artifacts/review-evidence/T-010-r3-check.py: dossier-vs-compiled line membership 0 missing x5; letter/export sweep for charges content, flags and adverse facts across 5 dossiers (all hits read); counts sections 1-10 x5, items 23/20/21/19/19, URLs 8/9/10/9/16, calibration severities\",\n  \"grep 'causation-weakening|causation/compliance|batch accept|accept all|Severity rule:|supplemented|no stated charge' in 5 dossiers -> only lit-lead.md:27 'there is no batch accept (D-011)'\",\n  \"curl -L texas.public.law Tex. H&S §181.154 (HTTP 200, 26906 bytes) -> extracted (a)-(c) and compared to privacy-compliance.md:71\",\n  \"read spec/REQUIREMENTS.md R-EX-1..R-EX-8 rows, SAMPLE_CASE_TRUTHS charges paragraph, ORCHESTRATOR_DECISIONS D-001/D-010/D-011/D-013/D-017/D-019; grep board for D-019 reconciliation (T-025 AC 3)\",\n  \"wrote artifacts/review-evidence/T-010-r3-resolution.md (resolution table for all LL r2 findings + PM r2 minors in my lens + letter sweep)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"texas_law_accuracy\": 5, \"catches_what_gets_demands_discounted\": 5, \"adjuster_adversarial\": 5, \"keeps_tool_out_of_legal_medical_judgment\": 5, \"spec_alignment\": 5, \"source_grounding\": 5},\n \"findings\": [],\n \"whats_right\": [\n  \"Letter/notes split is now exact everywhere: lit-lead #19 and adjuster #21 hold the total line to 'Billed charges stated in these records: $8,390' (D-019), with rate, visit-count wording and bills to request only in the internal notes (R-EX-4).\",\n  \"Adverse facts stay the attorney's call: adjuster #7 'never auto-inserted in the letter — whether the letter mentions it is the attorney's call' and the adjuster red flag excludes human-reviewed omissions.\",\n  \"§181.154 takeaway now tracks the statute verbatim on both (c)(1) 'to another covered entity' and (c)(2) 'otherwise authorized or required by state or federal law'.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T00:53:25.969Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-010-litigation-lead-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:27.427Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; python3 tools/board.py --help 2>&1 | head -20",
 "description": "Validate board and review file format"
}
````

### User / tool · 2026-11-02T00:53:27.613Z

**tool result**
````
ok (25 file(s))
usage: board.py [-h]
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
                ...

Zlayt PM project board CLI

positional arguments:
  {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}

options:
  -h, --help            show this help message and exit
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:30.216Z

**tool call — Bash**
````
{
 "command": "python3 -I -c \"\nimport re,json,sys\nt=open('reviews/T-010-litigation-lead-r3.md').read()\nb=re.findall(r'\\x60\\x60\\x60json\\n(.*?)\\n\\x60\\x60\\x60',t,re.S); assert len(b)==1\nj=json.loads(b[0]); print(j['verdict'], len(j['findings']), list(j))\"",
 "description": "Parse review JSON block"
}
````

### User / tool · 2026-11-02T00:53:30.321Z

**tool result**
````
pass 0 ['card', 'persona', 'model', 'scope', 'exercised', 'verdict', 'scores', 'findings', 'whats_right', 'questions_for_chris']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:31.062Z

Now the memory update.

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:34.257Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/litigation-lead-reviewer/feedback_texas_law_checks.md",
 "old_string": "Also recurring: watch for",
 "new_string": "Round-3 (T-010, 2026-11-01): D-019 superseded R-EX-8's \"(... charges to be supplemented)\" parenthetical — letter total line is exactly \"Billed charges stated in these records: $X\"; spec reconciliation lives on T-025. Don't quote R-EX-8's sample line in fixes. My session's loaded prompt can lag the on-disk agent file (recompile seconds before dispatch) — trust `compile_agents.py --check` + line-diff, not my own prompt text. Shell hook rejects `for p in ...; do echo \"$p: $(...)\"` (git-guard); list paths explicitly instead.\n\nAlso recurring: watch for"
}
````

### User / tool · 2026-11-02T00:53:34.357Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/litigation-lead-reviewer/feedback_texas_law_checks.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:35.459Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/litigation-lead-reviewer/MEMORY.md",
 "old_string": "r2: stale compiled agents, letter-vs-notes",
 "new_string": "r2: stale compiled agents, letter-vs-notes; r3: D-019 total line, prompt lag"
}
````

### User / tool · 2026-11-02T00:53:35.571Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/litigation-lead-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:53:43.519Z

T-010 round 3 litigation-lead verdict: **pass**, with no findings. All six round-2 items are resolved.

- **Major 1 (letter vs notes): resolved.** In lit-lead #19, adjuster #21, paralegal #12/#21 and the lit-lead calibration, the letter's total line is now exactly "Billed charges stated in these records: $8,390", as D-019 requires. The $185 rate, the "visit count not stated" wording and the bills to request appear only in the internal notes.
- **Major 2 (agents not recompiled): resolved.** `python3 tools/compile_agents.py --check` printed "agent definitions in sync" (exit 0). My own line-by-line check found 0 dossier lines missing from any of the 5 agents. The agents commit (a399a4c, 18:51:24) is newer than the last dossier commit (2687094, 18:50:20).
- **§181.154 wording: resolved.** I re-fetched the statute from texas.public.law with curl (HTTP 200). The takeaway at privacy-compliance.md:71 now matches both branches of (c): disclosures "to another covered entity" and disclosures "otherwise authorized or required by state or federal law".
- **The rest are resolved too.** The retired D-013 flag names return 0 grep hits. Lit-lead #9 now says "there is no batch accept (D-011)". The card's AC 2 counts match my recount.
- **Letter sweep:** no line in the 5 dossiers puts charges caveats, flag content or tool-chosen adverse facts into the letter. Adverse facts go to the internal notes for the attorney to decide.

Two notes that are not T-010 defects:
- spec/REQUIREMENTS.md:126 (R-EX-8) still requires the "(physical therapy charges to be supplemented)" parenthetical, which D-019 dropped. T-025 AC 3 already tracks that fix.
- The prompt this session started with still had the pre-round-3 text, although the agent file on disk is in sync. I think agent definitions load when a session starts. If so, a reviewer dispatched seconds after a recompile can run the old prompt.

Files:
- /Users/arsis/zlayt-pm-project/reviews/T-010-litigation-lead-r3.md
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-resolution.md
- /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-010-r3-check.py
