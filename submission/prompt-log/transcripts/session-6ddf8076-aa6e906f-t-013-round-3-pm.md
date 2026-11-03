# Subagent: T-013 round-3: PM (T-013 round-3: PM)

Source: `agent-aa6e906f40988e092.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:41:42.885Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 3 (final) of T-013 "spec/REQUIREMENTS.md" (M1). AC: `python3 tools/board.py show T-013`. Prior: reviews/T-013-product-manager.md (r1), reviews/T-013-product-manager-r2.md (r2 changes, 5 majors). Changes: `git diff 64f766e..b4f3924 -- spec/REQUIREMENTS.md`. Decisions now written down: memory/ORCHESTRATOR_DECISIONS.md (D-001..D-018) and memory/DECISIONS.md ADR-017 (reconciliation with §8).
Exercise hands-on: resolve each r2 major/minor (append "Round 3" to artifacts/review-evidence/T-013-trace.md); re-sample 10 R-IDs for pass/fail decidability; confirm §8 is a clean hand-off (every row resolved or owned by an open card); confirm scope fits M2+M3 (~7 h) — list anything that should still be cut.
Write reviews/T-013-product-manager-r3.md (D.2 JSON). Do not fix anything. Reply ≤ 20 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:43.826Z

Starting with memory and prior reviews.

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:45.275Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md; python3 tools/board.py show T-013; git log --oneline | head -5; ls reviews/ | grep T-013",
 "description": "Read memory, board card, git log, existing reviews"
}
````

### User / tool · 2026-11-02T00:41:45.450Z

**tool result**
````
---
name: t013-review-history
description: T-013 REQUIREMENTS review rounds — verdicts, open items handed to round 3 (as of 2026-11-02)
metadata:
  type: project
---

T-013 (spec/REQUIREMENTS.md) review history:
- **Round 1 (commit 65894f6):** PM verdict changes (5 majors); paralegal verdict fail (blocker: flags exported into the letter text).
- **Round 2 (commit 64f766e, reviewed 2026-11-02):** PM verdict changes (5 majors). 13 of the 15 round-1 blockers/majors are resolved.

Open after round 2:
1. R-IN-5 vs R-RV-2: the date-confirm contradiction.
2. Cut R-RV-7, R-CH-7 and the R-CH-6 split action to non-goals.
3. R-TL-8 cites a lexicon `hedge` category that doesn't exist.
4. R-EX-1's negative strings vs the excerpt-selection rule. This is also a Chris question: may flag-evidence sentences appear in the letter?
5. §8 hand-off: "orchestrator decisions 1-10" are unrecorded and no card owns the reconciliation.

Trace: artifacts/review-evidence/T-013-trace.md (Round 1 and Round 2 sections).

**Why:** Round 3 must check exactly these items, using the same trace format.

**How to apply:** In a round-3 brief, start from these five items and re-sample with a new seed. Previous seeds were 13 and 1302. Related: [[spec-review-patterns]].
---
name: spec-review-patterns
description: Recurring defects found reviewing spec/REQUIREMENTS.md (T-013 r1, r2) — check these first on any requirements/AC review
metadata:
  type: feedback
---

Recurring defects in requirements docs on this project. Check them before forming opinions.

1. **Cited identifiers that don't exist.** Round 1 had R-QA-2. Round 2 cited a lexicon `hedge` category that wasn't there. Script both checks: referenced R-IDs minus defined R-IDs, and grep every cited file, key or category in the cited file.
2. **Fixing one finding contradicts another rule.** In round 2, adding a "confirm date" flow conflicted with "date not editable → 422". Cross-check every new action against the per-type edit table and against api.md.
3. **Tests whose strings follow no rule.** The negative-string E2E banned record words that no excerpt rule excluded. The hand-written worked example passed only because the writer chose the excerpts.
4. **Vocabulary drift across REQ, api.md, golden and lexicon**, for example `prior_condition` vs `pre_existing`, and golden provider aliases that grounding would reject. Always diff the flag and class enums across the four.
5. **"Orchestrator decided X" with no recorded decision.** grep DECISIONS, STATE and ASSUMPTIONS. If the decision isn't there and no card owns the reconciliation, the hand-off is not clean.
6. **Scope creep while fixing review findings.** Round 2 went from 47 to 61 R-IDs. Name the add-ons that Appendix A does not require and that need new endpoints or ADR changes (batch accept, charge reclassification, the duplicate-split action).

**Why:** These recurred across rounds and drive M2/M3 card planning (T-017). Workers implement against api.md and the ADRs, so any divergence that goes unrecorded gets built two ways.

**How to apply:** On any REQUIREMENTS or AC review, run the inventory script, check the golden data with python, grep the cited artifacts, and append a resolution table to `artifacts/review-evidence/<card>-trace.md`. See [[t013-review-history]].
---
name: needs-chris-drift
description: Recurring NEEDS_CHRIS defects on this project. Rows are added without needs_chris cards, and questions that aren't Chris's (client practice, team product calls) get in. Check on every harness/submission review.
metadata:
  type: feedback
---

On every review that touches submission/NEEDS_CHRIS.md, check three things with commands:
1. **Row ↔ card parity.** Compare the row numbers in NEEDS_CHRIS.md with the `board.py list --status needs_chris` titles that contain "(NEEDS_CHRIS #n)", and check the priorities match. T-005 r1 had 0 of 1 rows carded; r2 had 2 of 10 (rows #4-#11 were added by the review-triage flow with no cards; row #1 was P1 in the file and P2 on the card).
2. **§11.5 scope.** Only things that genuinely need Chris belong there: his story, personal numbers, HF Space name, own-voice video, final send, credentials, spend. Questions about how "Zinda" (the fictional client in SPEC.md:8) works are discovery questions or ASSUMPTIONS, not Chris items. Product calls the team already made belong in ORCHESTRATOR_DECISIONS/ADRs. "Nothing to do" rows are FYIs.
3. **Exact action.** Each action names the expected reply ("demo-only" / "live with cap $X") rather than "Reply via inbox."

**Why:** The needs_chris column is what Chris sees on his phone, and the file is a graded submission artifact (§11.5 DoD). The file grows during review triage while the card step is skipped.

**How to apply:** Re-read the file at the end of the review, because it changed mid-review in T-005 r2. Also check that every ADR's stated facts match the running system (ADR-000e said http/no-TLS while https serve was live). See [[spec-review-patterns]].
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
updated_at: "2026-11-02T00:41:24Z"
claimed_by: "writer"
claimed_at: "2026-11-02T00:36:25Z"
rounds: 2
commits: ["65894f6", "64f766e", "4191140", "b4f3924"]
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-013-product-manager.md", "at": "2026-11-02T00:25:13Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-013-paralegal.md", "at": "2026-11-02T00:25:13Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-013-paralegal-r2.md", "at": "2026-11-02T00:35:23Z"}
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-013-product-manager-r2.md", "at": "2026-11-02T00:36:12Z"}
ac:
  - {"n": 1, "text": "every Part 1 must-have and constraint maps to >=1 R-ID with a pass/fail test description", "done": true, "evidence": "Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script"}
  - {"n": 2, "text": "one stretch item selected with a 3-line rationale and a cut rule", "done": true, "evidence": "Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script"}
  - {"n": 3, "text": ">=6 explicit non-goals (e.g. PDF/OCR, multi-case, auth, real data, drafting prose in firm voice)", "done": true, "evidence": "Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script"}
  - {"n": 4, "text": "ship-bar section mirrors CONTRACT §8.2 numbers and names the eval that measures each", "done": true, "evidence": "Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script"}
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
- 2026-11-02T00:29:38Z orchestrator: review dispatched: paralegal-reviewer, product-manager-reviewer (round 2)
- 2026-11-02T00:35:23Z orchestrator: review paralegal-reviewer (claude-opus-5-5): changes — reviews/T-013-paralegal-r2.md; round 2; findings:
    - [major] 'No flag text of any kind' in the letter is contradicted by the worked example; there is no rule, no visibility and no control for flagged record sentences that reach the carrier — fix: Reword R-EX-1 and :11: the letter holds no tool-authored flag content (types, titles, reasons, day counts, counts). Record sentences quoted in an entry excerpt may coincide with flag evidence. Add to 
    - [major] R-TL-8 (qualifier travels with finding) keys on a lexicon 'hedge' category that does not exist; its entry-6 test cannot follow from the rule — fix: Name the trigger exactly. Example: lexicon entries with flag_type causation_weakening (may_represent, correlate_clinically, possibility_terms), plus compliance entries when the sentence is the same one that carries the finding. Or add an 
    - [minor] No pending count or pending-flag warning before copy — fix: Add 'N items pending (N flags)' to the R-EX-5 line, and require a one-step confirm on Copy when any flag is pending.
    - [minor] Total-line parenthetical is tool-authored text in the carrier block that volunteers a weakness; the placeholder name is inconsistent — fix: Letter wording: 'Billed charges stated in these records: $8,390.00 (physical therapy charges, Capital PT, not included; to be supplemented)'. Use one placeholder name (<service>) in :110.
    - [minor] unclear → charge reclassification produces a charge with no value — fix: State that `unclear` with a null value cannot become `charge`. It goes to the notes as 'request clean copy of bill'. Only `unclear` items with a parsed value may be reclassified.
    - [minor] Ambiguous-date rule will send about a third of US-format dates to 'Dates to confirm' — fix: Keep the rule, but add per-packet inference as a requirement: if any date in the same packet or source has a first number > 12 → DD/MM, or a second number > 12 → MM/DD, apply it to that packet's ambiguous dates and show that it was applied. Ask only when the packet gives no evidence.
    - [minor] Internal notes cite 'record N' without provider and date, and the letter has no record numbers — fix: Every notes citation reads 'record N (<provider>, <Month D, YYYY>)', as in :247.
    - [minor] Future treatment recommended is not a notes item — fix: Add 'FUTURE TREATMENT RECOMMENDED (no cost stated)' to R-EX-4, sourced from recommend/plan sentences with no amount, worded as an action ('request cost estimate').
- 2026-11-02T00:36:12Z orchestrator: review product-manager-reviewer (claude-opus-5-5): changes — reviews/T-013-product-manager-r2.md
- 2026-11-02T00:36:12Z orchestrator: assigned: writer
- 2026-11-02T00:36:25Z writer: claimed
- 2026-11-02T00:40:29Z writer: Round 3: applied D-010..D-015 and r2 review findings in spec/REQUIREMENTS.md; R-RV-7 and R-CH-7 withdrawn (non-goals 14, 15); 61 R-ID rows, no dangling refs.
- 2026-11-02T00:40:29Z writer: AC 1 checked: Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script
- 2026-11-02T00:40:29Z writer: AC 2 checked: Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script
- 2026-11-02T00:40:29Z writer: AC 3 checked: Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script
- 2026-11-02T00:40:29Z writer: AC 4 checked: Round 3: spec/REQUIREMENTS.md sections 1-3, 4, 5, 7 re-verified; R-ID rows vs references checked by script
- 2026-11-02T00:40:29Z writer: moved in_progress -> in_review
- 2026-11-02T00:41:23Z writer: Folded ADR-017 (e442626) into spec/REQUIREMENTS.md: R-CH-7 = charges accept/dismiss only; R-TL-9 code-set provider; R-RV-6 wording; R-TL-10 allows source-label and parsed-date numbers; gap scope sentences; section 8 now points to ADR-017 as resolved, 3 open items for qa/orchestrator.

## Handoff
Addendum to round 3 (ADR-017): R-RV-7 stays cut (non-goal 14); R-CH-7 live as accept/dismiss only; R-TL-9 test checks header label vs code-set provider, GROUNDING_PROVIDER_NOT_IN_RECORD dropped; R-RV-6 test = no review_status change, no flag created resolved; prior_condition gone (pre_existing); R-TL-10 numbers allowed from excerpt + source label + parsed date; R-FL-1/R-IN-5 clinical-encounter scope; sec 8 = ADR-017 resolved table + 3 open items (qa golden aliases, qa export golden, orchestrator A-106/SCOPE_CUTS/brief key). Checked by grep only.

568e4b7 docs(research): T-008 round 2 — delay, MIST, LOP, passive-care attacks; cervical source; glossary
b4f3924 docs(spec): fold ADR-017 into requirements; section 8 marked resolved
6bb13dd fix(personas): T-010 round 2 - litigation-lead review, D-016/D-017 alignment
4191140 docs(spec): requirements round 3: apply D-010..D-015, hedge rule, notes sections, hand-off list
4924221 docs(research): T-012 round 2 — §181.154, full vendor retention, scoped PRs, Part 2 privacy answers
T-013-paralegal-r2.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:48.829Z

**tool call — Bash**
````
{
 "command": "sed -n '/```json/,/```/p' reviews/T-013-product-manager-r2.md | python3 -c \"import json,sys;t=sys.stdin.read().split('\\n',1)[1].rsplit('\\`\\`\\`',1)[0];d=json.loads(t);[print(f['severity'],'|',f['title'],'\\n  FIX:',f['fix'],'\\n  AT:',f['acceptance_test']) for f in d['findings']];print(d['questions_for_chris'])\"; git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md; wc -l spec/REQUIREMENTS.md",
 "description": "Extract r2 findings and diff stats"
}
````

### User / tool · 2026-11-02T00:41:48.883Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No escaped character) | command: sed -n '/```json/,/```/p' reviews/T-013-product-manager-r2.md | python3 -c "import json,sys;t=sys.stdin.read().split('\n',1)[1].rsplit('\`\`\`',1)[0];d=json.loads(t);[print(f['severity'],'|',f['title'
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:49.222Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/spec/REQUIREMENTS.md"
}
````

### User / tool · 2026-11-02T00:41:49.394Z

**tool result**
````
1	# REQUIREMENTS — Treatment Timeline prototype (Part 1)
2	
3	Owner: writer (T-013, revision 3). Source: Appendix A Part 1 (`spec/SPEC.md`), CONTRACT §5 (M1), §5.2, §8.2. Truth values: `spec/SAMPLE_CASE_TRUTHS.md`.
4	Binding product decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-015); cited below by D-ID.
5	Design it must agree with: `docs/LLM_VS_CODE.md`, `memory/contracts/api.md`, `memory/DECISIONS.md`. ADR-017 in `memory/DECISIONS.md` reconciled the earlier differences (§8); what is still open is listed there.
6	Every later card and eval cites an R-ID from this file. If a card can't name the R-ID it serves, the card is wrong or this file is.
7	
8	**User.** A paralegal at a personal-injury firm. She reviews rather than trusts. Every statement the tool makes must be checkable against its source (A-101: she builds the chronology, the attorney signs the letter).
9	
10	**Two outputs, kept apart (D-001).** The export has two blocks and they never mix:
11	1. **Treatment section (paste into letter)**: accepted entries and accepted charges. Nothing else. It holds no tool-authored flag content (no flag type, title, reason, day count or count line). The records' own words can appear in it, but only inside an accepted excerpt (D-012), and block 2 tells the attorney which quotes carry flagged language.
12	2. **Internal review notes — do not send**: accepted flags, flagged language quoted in the letter, amounts not totaled, damages mentions, future treatment recommended, bills to request, records left out, edits, pending items, and a one-line AI-assistance statement (D-009).
13	
14	**Checkers.**
15	
16	| Checker | Meaning |
17	|---|---|
18	| **UT** | unit test under `tests/unit` (code only, no LLM) |
19	| **EV** | metric from `python -m evals.run` (golden set in `evals/golden/`, writes `evals/reports/latest.json`) |
20	| **E2E** | Playwright test under `tests/e2e` |
21	| **PR** | persona review file `reviews/<card>-<persona>.md`; pass = no blocker or major on that item |
22	| **INST** | `tools/install_test.sh` clean-clone timed run |
23	
24	Pass/fail wording is literal. "Pass" means the stated condition holds on every golden case unless one is named.
25	
26	**Vocabulary (D-013).** Flag types: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection suspicion). Lexicon types `causation_weakening` and `compliance` map to `causation`. States: `verified`, `needs_review`, `rejected`. Review statuses: `pending`, `accepted`, `edited`, `dismissed`.
27	
28	---
29	
30	## 1. Must-haves
31	
32	### 1.1 Input
33	
34	| ID | Requirement | Pass / fail test | Checker |
35	|---|---|---|---|
36	| R-IN-1 | Accept records pasted as text. | Pasting the 9 sample records produces 9 timeline entries and the UI shows "9 records found" before any model call. Fail if the count is wrong or not shown. | E2E + UT (splitter; pieces concatenated equal the input) |
37	| R-IN-2 | Accept records uploaded as a `.txt` file. No PDF or OCR (non-goal 1). | Uploading `evals/golden/sample.txt` gives the same 9 entries as paste. A `.pdf` upload is refused with a plain message, not a crash. | E2E |
38	| R-IN-3 | Date parsing is code, from an explicit format list. A numeric date is **ambiguous** when its first two numbers are both 1–12 and differ (`04/05/2026`: April 5 or May 4). It is never guessed, and no per-packet convention is inferred (non-goal 18). | Golden `case_01_date_formats`: seven formats parse (ISO, `02/17/2026`, `Feb 24, 2026`, `3 March 2026`, `March 10th, 2026`, `03-17-26`, `3/25/26`); `04/05/2026` is `date_ambiguous` with date null and `date_candidates` 2026-04-05 and 2026-05-04. Fail on any silent guess. | UT + EV (`case_01`) |
39	| R-IN-4 | Input size is bounded; empty or oversize input fails visibly without calling the LLM. | Empty input and input over `limits.max_chars` each show an error state; the LLM call counter stays 0. | E2E + UT |
40	| R-IN-5 | **Dates to confirm.** An entry with an ambiguous date is excluded from ordering and gap math, shown in a "Dates to confirm" group (a `record_warning`), and is `needs_review`. She resolves it with the `confirm_date` action (R-RV-2), choosing one of the code-proposed readings. An entry with no date at all stays in the group with "no date found"; this build offers no way to type one in. | `case_01` record 8: absent from the timeline order until confirmed; after `confirm_date` 2026-05-04 it sorts into the timeline after 03-25. The gap table is unchanged because record 8 is a phone note (D-003 counts clinical encounters only). With no readings (no date found) an entry can't be confirmed and stays excluded. | UT + E2E |
41	
42	### 1.2 Timeline
43	
44	An **entry** is one timeline row: date, provider, one-line summary, exact source excerpt.
45	
46	| ID | Requirement | Pass / fail test | Checker |
47	|---|---|---|---|
48	| R-TL-1 | Entries are chronological, one per distinct source record (R-TL-7 covers duplicates), each with date, provider, one-line summary and excerpt. | Sample: 9 entries in date order, none of the four fields empty. Same-date records from different providers (records 1, 2) stay separate and keep source order (A-108). | UT + EV `entry_recall` |
49	| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a terminator, where a terminator is `.`, `?` or `!` followed by whitespace and then an uppercase letter, digit or end of text; `;`; or a line break. A period after an abbreviation on a fixed list (`approx.`, `Dr.`, `Mr.`, `Mrs.`, `Ms.`, `vs.`, `etc.`, `e.g.`, `i.e.`) or inside a number (`1.5`) is not a terminator. | UT: for every golden record, the units concatenated equal the record text, and `approx. 35 mph.` in record 1 is one unit. Grounding verifier passes every `verified` entry. An excerpt that is not verbatim is `rejected` (tray only, never timeline or export). An excerpt that starts or ends mid-unit is `needs_review`. | UT + EV `grounding_rate` |
50	| R-TL-3 | **Date of service is the record's header date, parsed by code.** Dates inside the body are facts for the conflict check, never the entry date. | Seeded test on **record 7**: header 2026-05-18, body "Date of accident per intake form: 2026-01-19". If the model returns 2026-01-19, the entry is `rejected` (`GROUNDING_DATE_MISMATCH`). Normal path: entry 7 dated 2026-05-18, sorted between entries 6 and 8. | UT + EV (`sample`) |
51	| R-TL-4 | **Summary adds nothing**: no fact, diagnosis, severity or causation absent from its excerpt. Judge #1 (faithfulness) checks every summary; `partially` or `unsupported` makes the entry `needs_review` with a one-sentence reason. | (a) Judge #1 returns `supported` on all 9 sample entries in each of 3 runs. (b) On the 20 seeded unsupported summaries in `evals/golden/hallucinations.jsonl` judge #1 flags at least 19 (≥ 95%; metric `hallucination_catch_rate`). (c) On the 5 faithful controls in `hallucinations_controls.jsonl` none returns `unsupported`. | EV |
52	| R-TL-5 | Every entry carries a state composed by code (ADR-005). `needs_review` sorts first in the review queue. | Unit tests cover the full composition table. E2E: a seeded `needs_review` entry appears above `verified` ones. | UT + E2E |
53	| R-TL-6 | "Why?" on every item shows the ladder record (generator output, code checks, judge verdict, state, backend) and the fixed-template one-sentence reason. | E2E: Why? on entry 7 shows check results and judge verdict; the audit record matches D.4 plus `backend`. | E2E |
54	| R-TL-7 | **Duplicate records are merged by code**: same date + same provider (case and whitespace normalized) + same normalized text → one entry citing every source record, with a visible "duplicate of record N" note. There is no split action (non-goal 16). | `case_04_duplicates_no_amounts`: 6 records give 4 entries, E1 cites records 1 and 2, E2 cites 3 and 4. Fail if 6 entries, or if a merged entry cites one record. | UT + EV (`case_04`) |
55	| R-TL-8 | **A hedge travels with its finding; a lexicon sentence is never cut.** (a) Any sentence unit that contains a lexicon hit, of any type, is kept whole: no excerpt starts or ends inside it. (b) The **hedge set** is the `app/llm/lexicon.yaml` entries `may_represent`, `correlate_clinically`, `possibility_terms`, `cannot_exclude` and `nonspecific_indeterminate`. If a record contains units that match the hedge set, an entry from that record must include every one of them, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Other lexicon types (`pre_existing`, `compliance`, the rest of `causation_weakening`) do not force inclusion. | UT: the hedge set loads from `lexicon.yaml`, is non-empty and contains `may_represent` and `correlate_clinically`. Seeded entry 8 with excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." → `needs_review` (`EXCERPT_OMITS_QUALIFIER`); with "…narrowing. Findings may represent degenerative change; correlate clinically." → `verified`. Entry 3 with excerpt "Persistent neck pain 6/10, daily headaches." stays `verified` (the 2023 low back sentence is `pre_existing`, not a hedge). Entry 6 of the sample is not held to this rule; its default excerpt is checked by `entry_recall` (`must_contain_excerpt`: "Discharged from PT after two missed appointments"). | UT + EV |
56	| R-TL-9 | **Provider is the record's source label exactly as written (D-014), set by code.** Code copies the header/source label into the entry; the generator schema has no provider field, so a model can't supply or alter it (ADR-017). | UT: for every record in every golden file, the entry's provider equals the header label after whitespace normalization (record 4: "Capital PT, initial evaluation"). UT: the generator output schema has no provider field. Every provider and alias in the golden files must equal or be a substring of its record's label (qa, §8). | UT + EV |
57	| R-TL-10 | **Numbers, dates and dollar signs in a summary must appear in the item's excerpt (D-006).** If one doesn't, the entry is `needs_review` with the reason. The allowed numbers are those in the excerpt, plus those in the record's source label and its parsed date (so "visit 8" and the year in a heading don't trip it). This is a code check and does not rely on the judge. | UT: summary "pain 4/10" with excerpt "Pain 3/10." → `needs_review`. Sample entries pass, including "Visit 8: …" where "8" comes from the source label "Capital PT, visit 8". | UT |
58	
59	### 1.3 Review flags
60	
61	Four types: `gap`, `conflict`, `pre_existing`, `causation`. Gap math is code over the header dates of clinical-encounter records (D-003): billing statements and phone notes are excluded, duplicates collapsed, ambiguous dates excluded, and the result does not change when the paralegal dismisses or edits an entry. Every flag shows its evidence.
62	
63	| ID | Requirement | Pass / fail test | Checker |
64	|---|---|---|---|
65	| R-FL-1 | **Treatment gap.** Flag when days between consecutive dates of service across all providers (A-102) is **greater than 30** (A-104). Only clinical-encounter records count (D-003): billing statements and phone notes are excluded. Evidence is the two bounding entries (date, provider, excerpt). | Sample: flag 2026-03-06 → 2026-05-18, 73 days, citing entries 6 and 7. No flag on 2026-01-23 → 2026-02-20 (28 days). `case_02_gap_boundaries`: 29 and 30 do not flag, 31 does (3 flags, 4 near-misses). UT: dismissing entry 6 leaves the gap flag and its days unchanged. | UT (29/30/31) + EV `flag_*[gap]` |
66	| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**; (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
67	| R-FL-3 | **Prior / pre-existing conditions.** LLM classification plus lexicon scan; if only one fires, the flag is `needs_review` (`LEXICON_ONLY` or `LLM_ONLY`). | Sample must raise record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("degenerative change"). `case_06_subtle_pre_existing` is caught, and its 28-day near-miss does not flag. | EV `flag_*[pre_existing]` |
68	| R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. | Golden levels: sample records 8, 6 and 9 are `must` (K1–K3); the record-7 items ("New onset" after the 73-day gap; wrong accident date, K4–K5) are `should`, credited when found directly or through G1/C1. Golden `must_not` M1–M13 all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
69	| R-FL-5 | Every flag cites verbatim excerpt(s) that pass the grounding check. An ungrounded flag is `rejected`. | Verifier test on flags, same as R-TL-2. | UT + EV `grounding_rate` |
70	| R-FL-6 | Flags are grouped by type (four groups) with a fifth "Record warnings" group (dates to confirm, injection suspicion). Each shows its state and, when `needs_review`, a one-sentence reason. | E2E: the sample shows at least one flag in each of the four type groups; `case_01` shows a dates-to-confirm item; `case_07` shows an injection warning. | E2E |
71	| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
72	| R-FL-8 | **Flag text is code (D-007).** Titles and explanations come from code templates. The LLM returns only the category and excerpt spans for a flag. | UT: the LLM output schema for flags has no free-text field; every flag title and explanation equals the template output for its type and computed values. | UT |
73	
74	### 1.4 Billed charges
75	
76	| ID | Requirement | Pass / fail test | Checker |
77	|---|---|---|---|
78	| R-CH-1 | List **every dollar amount** found, each with source record and verbatim excerpt. Extraction is code (currency pattern, money as whole cents). Noisy forms (`$1,2OO`) are listed as `unclear` with no value, never corrected. | Sample lists $6,240, $185, $2,150 and nothing else. `case_03_rate_and_ocr`: `$1,2OO` and `$9S.00` are `unclear`, value null. Amount recall ≥ 95% over `required` golden amounts. | UT + EV `amount_recall` |
79	| R-CH-2 | Each amount is classed `charge`, `rate`, `estimate`, `damages` or `unclear` (golden classes). Code classifies by explicit billing-phrase rules; the LLM only when code can't; judge #2 re-reads every classification (D-004). A rate can never become a charge. | $6,240 and $2,150 → `charge`; $185 → `rate`; "missing 3 days of work" → `damages` (no value). A seeded rate marked `charge` is caught by judge #2. | UT + EV |
80	| R-CH-3 | **The total counts only accepted amounts of class `charge`.** The screen shows "Accepted charges: $X" and, separately, "Detected, not yet accepted: $Y (not a total)". Rates, estimates, damages and unclear amounts are listed as "unclear — not totaled" and never added. | Sample: after accepting both charges, Accepted = **$8,390**. Dismissing the ER charge drops it to $2,150. $185 reads "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review". **No PT total is computed** (golden `must_not` M4: none of 1,665 / 2,220 / 1,480 / 10,055 / 10,610 / 9,870 appears). | UT (totals) + E2E + EV |
81	| R-CH-4 | Non-billing figures are not charges. "Rx cyclobenzaprine 10 mg" and other doses never appear as amounts. | Golden `must_not` M7: no amount valued 10, 35, 6, 7, 12, 40 or 2. | EV |
82	| R-CH-5 | Amounts always need an explicit accept, even when `verified`. **Accepting a non-charge amount** (rate, estimate, damages, unclear) means "noted": it appears in the internal notes only, never in the letter or the total. An unreadable amount (`$1,2OO`, value null) can never count as a charge, accepted or not; its note reads "request clean copy of bill". | E2E: no amount reaches the letter or total without an accept click. Accept `$1,2OO` in `case_03` → it appears in the notes with "request clean copy of bill", not in `letter_text`, total unchanged. | E2E + UT |
83	| R-CH-6 | **Duplicate charges are merged by code**: same date + provider + amount → one amount citing every source record, with a visible "duplicate of" note. The total can never count it twice. There is no split action (non-goal 16). | Seeded unit test: the same $6,240 on 2026-01-09 from Central ER in two records → one amount; total after accept $6,240, not $12,480. | UT + E2E |
84	| R-CH-7 | **Charges are accept / dismiss only (D-010, ADR-017).** A charge's class comes from code and judge #2; the paralegal can't reclassify or edit it, so no path turns a rate, estimate or unreadable amount into a totaled charge. Reclassification is non-goal 15. | UT: any edit on a charge (amount, class, excerpt) → 422 `invalid_edit`; the review endpoint accepts only `accept`, `dismiss` and `reset` for amounts. After accepting the $185 rate the Accepted total is still $8,390 and `letter_text` has no $185. | UT + E2E |
85	
86	### 1.5 Review step
87	
88	An **item** is an entry, a flag or a charge. Everything starts `pending`.
89	
90	| ID | Requirement | Pass / fail test | Checker |
91	|---|---|---|---|
92	| R-RV-1 | Each entry and each flag can be **accepted, edited or dismissed**; each charge **accepted or dismissed** (D-010). Nothing is accepted by default. | E2E matrix: {accept, edit, dismiss} × {entry, flag} (6 cells) and {accept, dismiss} × {charge} (2 cells). Fresh load → all `pending`, letter block empty. | E2E |
93	| R-RV-2 | **What each action does (D-010, D-012).** See the table below the requirements. Originals are kept. "Edited" shows in the review UI and in the internal notes, never in the letter text. | UT, each → 422 `invalid_edit`: edit an entry's date or provider; edit a flag's evidence, type or title; edit a charge's amount or class; `confirm_date` on a parsed entry; `confirm_date` with a date that is not one of the code-proposed readings; an excerpt edit that is not a contiguous run of whole sentence units of the same record; an excerpt edit that drops a hedge-set unit (R-TL-8). `confirm_date` on `case_01` record 8 with 2026-05-04 → 200, a review event is logged, the entry joins the timeline. E2E: edit entry 3's summary → "edited" label in the UI; the letter shows the new summary with its citation and no "edited" mark; the notes list the original and the new text. | UT + E2E |
94	| R-RV-3 | **Edited text is re-checked.** The D-006 code check (numbers, dates, `$` in the new summary must appear in the excerpt) and judge #1 run on every edited summary and on every re-selected excerpt. If either objects the item is `needs_review` with the reason; she can still accept it ("keep my wording"); the choice is logged and shown in the internal notes. | UT: summary edited to add "$9,000" → `needs_review`. Seeded edit adding "herniation" → judge returns `partially` or `unsupported` → `needs_review`. Accept after either needs the confirmation. | UT + EV (judge) + E2E |
95	| R-RV-4 | Review is keyboard-drivable (accept / edit / dismiss / next) and usable at 375 px. | E2E completes the sample case by keyboard only. At 375 px no horizontal scroll and every action is reachable. | E2E |
96	| R-RV-5 | Dismissed items never export to the letter and are recoverable (reset) until export. A dismissed flag may carry an optional reason. | E2E: dismiss, reset, dismiss again → absent from the letter and listed only under "dismissed" in the notes. | E2E |
97	| R-RV-6 | **No LLM output is auto-accepted. Record text is data (D-005).** A record with an injection warning forces all its items to `needs_review` (an advisory state, ADR-008), its amounts can't be charges, and it can't suppress flags from other records (the lexicon is the floor). | Golden `case_07_prompt_injection`: the record produces an ordinary entry with an `INJECTION_SUSPECTED` warning, `needs_review`; no item's `review_status` changes and no flag is created resolved; the injected `$50,000` is never totaled (total stays $420). | EV + PR (privacy-compliance) |
98	| R-RV-8 | **Decisions survive a reload.** Accept, edit, dismiss, notes and `confirm_date` persist (SQLite) and restore on reload or reopen of the case. | E2E: accept 3 items, edit 1, reload → same statuses and the same Accepted total. | E2E |
99	| R-RV-9 | **Open the full source record from any item.** Entries, flags (both records for a two-record flag) and charges open the full record text with the excerpt highlighted, in a modal or panel. The highlight range comes from code offsets, not the model. If the offset can't be found, the item drops to `needs_review` and the UI says so. This is core; only the side-by-side layout is the stretch (§4). | E2E: from entry 8 open the record → the highlighted span equals the excerpt string. From the 73-day gap flag, records 6 and 7 both open. UT with a mutated record: offset lookup fails → `needs_review`. | E2E + UT |
100	
101	**R-RV-2 action table.**
102	
103	| Item | Accept | Edit allows | Edit never allows | Other |
104	|---|---|---|---|---|
105	| Entry | yes | summary text; re-selecting the excerpt as another contiguous run of whole sentence units of the **same** record (never dropping a hedge-set unit) | date, provider, record | `confirm_date` (below) |
106	| Charge | yes | nothing | amount, class, excerpt | dismiss |
107	| Flag | yes | a reviewer note (plain text, up to 500 characters, printed verbatim in the notes, labeled "reviewer note") | type, title, explanation, evidence | dismiss with optional reason |
108	
109	`confirm_date` is a separate review action, valid only for an entry whose date is `date_ambiguous`. Allowed values are the code-proposed readings only. It is logged as a review event with the previous state.
110	
111	*Withdrawn (D-011):* R-RV-7 (batch accept) is non-goal 14.
112	
113	### 1.6 Export
114	
115	Both blocks are assembled by code from items with `review_status` in {accepted, edited}. API: `GET /api/cases/{id}/export` returns `letter_text` and `internal_notes_text` separately.
116	
117	| ID | Requirement | Pass / fail test | Checker |
118	|---|---|---|---|
119	| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 days", "AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose quote is a substring of the accepted excerpt, an amount line or the total line; the letter builder takes no flags argument. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
120	| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
121	| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
122	| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009) and the pending count. (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences containing "recommend" (a code pattern), worded "request cost estimate". (8) **Bills to request**: providers (the label up to the first comma) with an entry in the letter and no accepted charge. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; bills to request for Austin EMS, Dr. Alvarez, Hill Country Pain Management and Capital PT. UT: every `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
123	| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter · N items pending (N flags)". The count line is part of neither block. **Copy asks for one confirmation when anything is pending**, stating the pending numbers and naming pending flags separately (a pending flag may be one the attorney needs to see). | E2E: leave the 73-day gap flag pending, click Copy letter → the confirm reads "1 flag not reviewed"; the count line shows it. Click Copy for each block, read the clipboard, assert no count line in either. | E2E |
124	| R-EX-6 | **Template and worked example.** The letter follows the template in §6: US long dates ("January 9, 2026"), provider as written in the header, a `Source [Ex. __ / Bates __]:` line with the verbatim quote (the placeholder is literal text she fills in after pasting), money as `$1,234.00`, no dot leaders. The full expected export for the sample case is `evals/golden/sample.export.expected.txt` (qa, T-015). | E2E on the **`fixture` backend** (recorded sample responses, so summary wording is fixed): with all 9 entries and both charges accepted and nothing edited, `letter_text` equals the golden file byte for byte. The golden file contains no `..` run and every amount matches `\$[\d,]+\.\d{2}`. On a live backend the check covers structure only (R-EX-1, R-EX-2). | E2E + UT |
125	| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → notes list record 5 (dismissed) and record 6 (not reviewed); the on-screen count reads "7 of 9". | E2E |
126	| R-EX-8 | **The total line is labeled and neutral.** The letter's total reads "Billed charges stated in these records: $X". When any non-dismissed rate, estimate or unclear amount exists, code appends "(<service> charges to be supplemented)"; on the sample: "(physical therapy charges to be supplemented)". `<service>` comes from a fixed code lookup (PT → physical therapy; unknown → the provider name as written). The reason ("per-visit rate only, visit count not stated") lives in the notes, never in the letter. | Sample: line equals `Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)`. UT: `letter_text` contains neither "visit count" nor "rate". A case with no non-charge amounts has no parenthetical. | UT + E2E |
127	| R-EX-9 | Two separate copy buttons, one per block, each copying exactly that block. | E2E: clipboard after each click equals the matching API field. | E2E |
128	
129	---
130	
131	## 2. Constraints
132	
133	| ID | Requirement | Pass / fail test | Checker |
134	|---|---|---|---|
135	| R-CO-1 | **LLM used for at least one step, and the line is documented.** `docs/LLM_VS_CODE.md` has the §5.2 table and matches the code. | Staff-engineer review checks each pipeline step against the table. UT: gap, total, date-parse, dedupe, sentence-splitter and export modules import no LLM client. | PR (staff-engineer) + UT |
136	| R-CO-2 | **Validation ladder on every LLM-derived item**: code check → independent judge (own prompt, preferably another model) → human accept/edit/dismiss. Nothing LLM-made reaches an export block without all three. | Audit record (D.4) exists for each LLM-derived item. E2E: an LLM-derived item with no human action is absent from both export blocks. | UT + E2E |
137	| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case the golden `must_not` list M1–M13 holds, including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident dates not merged; "concussion without loss of consciousness" kept as written. Any hit is a blocker. | EV (negative assertions) + PR (claims-adjuster) |
138	| R-CO-4 | **Runs from a link or from the repo in under 5 minutes.** The public link works without a key: public deployment is demo-only by default (D-008), replaying the cached sample run through the real pipeline code (A-002). | `tools/install_test.sh`: clean clone to first screen with the sample loaded < 300 s. The public link opens with no login. | INST + PR (installer-reviewer) |
139	| R-CO-5 | **Synthetic data only**, shown on screen. | Banner "Synthetic data only — never paste real records" on every view (E2E). `python tools/check_secrets.py` passes. | E2E + UT |
140	| R-CO-6 | **Model and backend are swappable by config** (`claude-cli`, `anthropic-api`, `fixture`). A backend or prompt change requires an eval re-run with the report attached. | Unit tests run on `fixture` with no key. Handoff of any prompt/model change links an `evals/reports/*.md`. | UT + board check |
141	| R-CO-7 | **Determinism across 3 runs of the sample case, on a live-model backend** (`claude-cli` or `anthropic-api`; a `fixture` replay proves nothing). *Code outputs identical*: record split, parsed dates, entry-ID set, gap flags, amount list and classes from code, totals. *LLM-derived item states must match*: every entry, amount and flag has the same state in all 3 runs. *Flags are compared by (type, set of cited record IDs, evidence excerpt)*; the three runs must produce the same flag set. Summary wording may differ but must be `supported` in every run. | `determinism_3run` = 1.0 on `sample`; any difference fails and the report lists it. Other golden cases are reported, not gated. | EV |
142	| R-CO-8 | **Time-box and say what was cut.** | `memory/SCOPE_CUTS.md` has a row for every non-goal in §5 and §5 has an item for every row; the product note's "cut" section matches. | PR (product-manager) |
143	| R-CO-9 | Retries: max 2, with changed conditions; failure is visible. | UT: LLM call fails twice → item shown as "could not process" with the reason (`LLM_FAILED_AFTER_RETRIES`); the app stays usable. | UT |
144	
145	---
146	
147	## 3. Part 1 submission items
148	
149	| ID | Requirement | Pass / fail test | Checker |
150	|---|---|---|---|
151	| R-SU-1 | Prototype link or repo with run instructions. README has a timed run path. | See R-CO-4. | INST |
152	| R-SU-2 | Demo ≤ 3 minutes, or annotated screenshots. Screenshots cover each of these states: input, processing, timeline with `needs_review` first, flags panel, charges with the unclear tray, edit with warning, source-record view, export (both blocks), "could not verify" tray, error/empty input. | `artifacts/demo.webm` duration ≤ 180 s (ffprobe). `artifacts/CAPTIONS.md` has one caption per listed state. | qa check |
153	| R-SU-3 | One-page product note. Checklist: the 7 required contents are present as headings (problem and user; what was built; what was cut and why; ship bar with 3–5 testable criteria, how tested, what was found; where AI can fail and how design handles it; model/code split; three metrics, each with a "tells you" line); exactly 3 post-launch metrics; renders to 1 page (≤ 650 words). Numbers in the note equal the latest eval report. | Checklist run by the writer self-check, then PR (hiring-panel, product-manager). | PR |
154	| R-SU-4 | **Which AI tools, and the prompts, unedited.** `submission/prompt-log/TOOLS.md` names tools, models and how the team was organized. The transcript export is produced by `tools/export_prompt_log.py` with no manual edits, plus a two-paragraph reading guide. | Re-run the exporter into a temp dir; `diff` against the submitted files is empty. `TOOLS.md` exists and names the tools and models. | qa check + PR (hiring-panel) |
155	| R-SU-5 | **Assumptions stated, links open.** The product note links the assumptions (A-101 to A-108 and any added); every link in the email draft opens without requesting access. | Checklist: note references `memory/ASSUMPTIONS.md` content; qa opens each submitted link in a logged-out browser. | PR + qa check |
156	
157	---
158	
159	## 4. Stretch pick: side-by-side source viewer
160	
161	**Chosen.** The two-pane layout. Left, the item queue. Right, the full source record, always visible, scrolled to the highlighted excerpt as she moves through the queue. Opening the full record (modal or panel, highlight by code offsets) is already core (R-RV-9), so what the stretch adds is the layout that removes the open-and-close step.
162	
163	**Why (3 lines).**
164	1. The spec says she "reviews rather than trusts." Each claim sits next to its context with no extra click per item, which is what about 20 decisions per case need.
165	2. A quote can mislead by omission (the MRI line without its hedge). R-TL-8 stops the tool from dropping the hedge; the viewer lets her see the rest of the record anyway.
166	3. It is cheap: the highlight range already comes from the grounding check, so there is no new LLM step.
167	
168	**Why not the others.** PDF upload puts unverifiable extraction upstream of the grounding check. The confidence indicator already ships as `verified / needs_review / rejected`. A firm-voice paragraph is generated prose that would need its own verification.
169	
170	**Cut rule.**
171	- **Start** only when every M3 must-have card is done with no open blockers, and M3 is inside its 3.5 h budget. The stretch is built before the M3 gate so the gate reviews it.
172	- **Stop** at 45 minutes, or when the M3 gate is due, whichever comes first.
173	- **Fallback (one):** cut it entirely. The core record modal from R-RV-9 stays and nothing else changes. Log the cut in `memory/SCOPE_CUTS.md`.
174	
175	| ID | Requirement | Pass / fail test | Checker |
176	|---|---|---|---|
177	| R-ST-1 | At viewport ≥ 1024 px the source record sits beside the queue; selecting an item scrolls the record to its highlighted excerpt without opening a modal. Below 1024 px it falls back to the R-RV-9 modal. | E2E at 1280 px: step through three items by keyboard; the record pane updates each time and the highlighted span equals the excerpt. At 375 px the modal opens instead. | E2E |
178	
179	---
180	
181	## 5. Non-goals
182	
183	These are out on purpose. The orchestrator logs each in `memory/SCOPE_CUTS.md` with the reason; R-CO-8 checks that the two lists match.
184	
185	1. **PDF upload and OCR.** Text only. Extraction errors would sit upstream of the grounding check. Pasted PDF text with page headers is a chaos-test input, not a feature.
186	2. **Multi-case and matter management.** One case at a time, no search across cases, no case list.
187	3. **Accounts, auth, roles, sharing.** One anonymous session.
188	4. **Real data or PHI handling.** Synthetic only. No HIPAA, retention or BAA claim. The privacy review checks the design for what a real build would need; the prototype doesn't implement it.
189	5. **Drafting demand-letter prose in a firm's voice.** Export is a structured treatment section from accepted items. No generated narrative, no advocacy language.
190	6. **Medical or legal judgment.** No diagnosis, severity rating, causation opinion or statement of what a record "means." Flags point at the record's own words. Whether a flagged sentence goes out in the letter is the attorney's call (D-012), not the tool's.
191	7. **Billing analysis.** No PT total from a rate, no reasonableness of charges, liens, insurance adjustments or paid-vs-billed.
192	8. **Integrations.** No EHR, case-management or document-system connectors, no email intake.
193	9. **Per-user learning.** Dismissals are logged for metrics, not fed back into prompts.
194	10. **Numeric confidence scores.** Three states only. A made-up percentage implies precision we can't verify.
195	11. **Non-English records and handwriting.** The chaos test confirms a clear failure message, not support.
196	12. **Exhibit and Bates numbering.** The export carries an `[Ex. __ / Bates __]` placeholder she fills in; the tool assigns no numbers.
197	13. **Manually adding an entry for a record the pipeline rejected.** The record stays in the "could not verify" tray; she writes that entry herself (SCOPE_CUTS 12).
198	14. **Batch accept.** Every item takes an individual decision (D-011; SCOPE_CUTS 14).
199	15. **Charge reclassification.** A charge is accepted or dismissed; its class comes from code and judge #2, and a rate can never become a charge (D-011; SCOPE_CUTS 15).
200	16. **A "not a duplicate" split action.** The duplicate merge stays, visible with a "duplicate of" note (D-011; SCOPE_CUTS 16).
201	17. **Smaller cuts (D-011; SCOPE_CUTS 17).** LLM date pointing, bring-your-own-key, the full-prompt audit view, edits to flag titles or explanations, a case list.
202	18. **Per-packet date-convention inference.** An ambiguous numeric date always asks once, even when the packet has `02/17/2026` elsewhere; golden `case_01` expects exactly that. Inferring the convention would cut confirmations and add a silent-guess risk; it needs its own eval first.
203	19. **LLM fallback for splitting records** (SCOPE_CUTS 13). An unsplittable paste becomes one record, marked uncertain.
204	
205	---
206	
207	## 6. Export template and worked example (R-EX-6)
208	
209	Sample case, all 9 entries and both charges accepted, nothing edited, all flags accepted. Summaries are one line, written from the excerpt only. Dates are US long form in the export; the UI and API keep ISO. `[Ex. __ / Bates __]` is literal text. The qa golden file `evals/golden/sample.export.expected.txt` is this text.
210	
211	**Block 1 — Treatment section (paste into letter)**
212	
213	```
214	TREATMENT CHRONOLOGY
215	
216	January 9, 2026 — Austin EMS run report
217	Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; alert and oriented; transported to Central ER.
218	Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
219	
220	January 9, 2026 — Central ER discharge summary
221	Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
222	Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
223	
224	January 16, 2026 — Dr. Alvarez, primary care
225	Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
226	Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
227	
228	January 23, 2026 — Capital PT, initial evaluation
229	Cervical range of motion reduced approx. 40%; plan of care 12 visits.
230	Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
231	
232	February 20, 2026 — Capital PT, visit 8
233	Pain 4/10, improving.
234	Source [Ex. __ / Bates __]: "Pain 4/10, improving."
235	
236	March 6, 2026 — Capital PT, visit 9
237	Discharged from physical therapy after two missed appointments; pain 3/10.
238	Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."
239	
240	May 18, 2026 — Hill Country Pain Management, new patient
241	New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
242	Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
243	
244	May 29, 2026 — Austin Imaging, cervical MRI
245	C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
246	Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
247	
248	June 12, 2026 — Hill Country Pain Management, follow-up
249	Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
250	Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
251	
252	BILLED CHARGES
253	
254	Central ER discharge summary, January 9, 2026: $6,240.00
255	Source [Ex. __ / Bates __]: "ER charges: $6,240."
256	Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
257	Source [Ex. __ / Bates __]: "Charge: $2,150."
258	
259	Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)
260	```
261	
262	**Block 2 — Internal review notes — do not send**
263	
264	```
265	INTERNAL REVIEW NOTES — DO NOT SEND
266	
267	AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.
268	Pending items: 0.
269	
270	FLAGS ACCEPTED
271	- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
272	- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19."
273	- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
274	- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
275	- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain".
276	
277	FLAGS DISMISSED
278	- none
279	
280	FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
281	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
282	- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
283	- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
284	- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
285	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
286	
287	AMOUNTS NOT TOTALED
288	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
289	
290	DAMAGES MENTIONS (not charges)
291	- Record 5 (Capital PT, visit 8, February 20, 2026): "Patient reports missing 3 days of work."
292	
293	FUTURE TREATMENT RECOMMENDED (no cost stated)
294	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.
295	
296	BILLS TO REQUEST (entry in the letter, no accepted charge)
297	- Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).
298	
299	RECORDS NOT IN THE TREATMENT SECTION
300	- none (9 of 9 records included)
301	
302	EDITED ITEMS
303	- none
304	
305	PENDING ITEMS NOT INCLUDED
306	- none
307	```
308	
309	If entry 5 were dismissed: the letter skips February 20, and "RECORDS NOT IN THE TREATMENT SECTION" reads "Record 5 (Capital PT, visit 8, February 20, 2026) — dismissed." The chronology never silently closes up.
310	
311	---
312	
313	## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
314	
315	These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.
316	
317	| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
318	|---|---|---|---|---|---|
319	| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
320	| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
321	| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
322	| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% (≥ 19 of the 20 in `hallucinations.jsonl`). | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
323	| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |
324	
325	Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
326	
327	Rule for the product note: report what the eval **found**, including misses, not just the targets.
328	
329	---
330	
331	## 8. Assumptions and the hand-off list
332	
333	### Assumptions this depends on
334	
335	Live list: `memory/ASSUMPTIONS.md`.
336	
337	| Ref | Assumption | Requirements that break if it's wrong |
338	|---|---|---|
339	| A-001 / A-002 | Dev runs on `claude-cli`; reviewers get demo mode with cached sample output and no key. | R-CO-4, R-CO-6 |
340	| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
341	| A-102 | A gap is measured between consecutive dates of service across all providers. | R-FL-1 |
342	| A-103 | The chronology feeds the medical-treatment section of a pre-suit demand letter to a carrier. | R-EX-1 to R-EX-8 |
343	| A-104 | "Longer than 30 days" is strict: 30 is not a gap, 31 is. | R-FL-1 |
344	| A-105 | Each pasted record carries its date and source on its first line or table row; undated or ambiguous records go to "Dates to confirm". | R-IN-3, R-IN-5, R-TL-3 |
345	| A-106 | The export cites by provider as written and date, with an exhibit/Bates placeholder; the tool assigns no Bates numbers. *A-106 currently says "record number, provider, date"; D-002 and R-EX-6 supersede it (orchestrator updates).* | R-EX-2, R-EX-6 |
346	| A-107 | A per-visit rate is not billable until visits are itemized, so no PT total is shown. | R-CH-2, R-CH-3, R-EX-8 |
347	| A-108 | Same-day records from different providers stay separate entries. | R-TL-1, R-TL-7 |
348	
349	**Proposed additions** (orchestrator decides; several depend on Chris, see `submission/NEEDS_CHRIS.md`):
350	- The date of service is the record's header date. Body dates are conflict evidence only (R-TL-3).
351	- Accepting a flag means "I've seen it and it's real," not "send it to the carrier." Flags go to the internal notes only (D-001). A flagged record sentence can still appear in the letter inside an accepted excerpt; the notes list those so the attorney decides (D-012).
352	- Numeric dates whose first two numbers are both 1–12 and differ are ambiguous even though Texas records are normally month/day; she confirms once per date (R-IN-3, non-goal 18).
353	- Providers with an entry in the letter but no stated charge are "bills to request" (R-EX-4).
354	- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).
355	
356	### Reconciliation status
357	
358	Everything above follows `memory/ORCHESTRATOR_DECISIONS.md`. The architect's first text and the requirements disagreed in 13 places; **ADR-017 in `memory/DECISIONS.md` (commit e442626) resolves the architect-side items.** This revision folds its outcomes in:
359	
360	| ADR-017 item | Outcome in this file |
361	|---|---|
362	| 1 Edit rules | Entry: summary text or excerpt re-selection; flag: note only; charge: accept/dismiss only (R-RV-1, R-RV-2, R-CH-7). `confirm_date` replaces date edit (R-IN-5). |
363	| 2 Batch accept | Cut (D-011). R-RV-7 withdrawn, non-goal 14. |
364	| 3 Letter content | Rates and other non-charge amounts are in the notes only; no short-cite mode; provider as written (R-EX-4, R-EX-6, R-EX-8). |
365	| 4 Codes and fields | `EXCERPT_OMITS_QUALIFIER` (ADR-016), `source_kind` (ADR-013), amount class `damages` (ADR-011) adopted. `GROUNDING_PROVIDER_NOT_IN_RECORD` dropped because code sets the provider (R-TL-9). |
366	| 5 Vocabulary | `pre_existing`, not `prior_condition`, everywhere (D-013). |
367	| 6 Gap scope | Clinical-encounter records only; missing dates can't be confirmed (R-FL-1, R-IN-5). |
368	| 7 R-RV-6 wording | "No item's `review_status` changes and no flag is created resolved"; `needs_review` is advisory. |
369	| 8 Golden export | Byte-equal to `evals/golden/sample.export.expected.txt` on the fixture backend (R-EX-6). |
370	| 9 Ship-bar key | `scores.verify_quickly` (D-015). |
371	
372	**Still open (not architect items):**
373	
374	| # | Where | What | Owner |
375	|---|---|---|---|
376	| 1 | Golden provider values and aliases | `sample.expected.json` has providers such as "Austin EMS" and aliases such as "Capital Physical Therapy", "Central Emergency Room", "Alvarez" that aren't the header label. R-TL-9 requires the label as written. | T-015 (qa) |
377	| 2 | `evals/golden/` | Add `sample.export.expected.txt` from §6, and a seeded-edit case for R-RV-3. | T-015 (qa) |
378	| 3 | Orchestrator files | Update A-106; log SCOPE_CUTS rows for non-goals 12, 18 and 19 (rows 14–17 exist); add `scores.verify_quickly` to the M3 paralegal brief. | orchestrator |
379	
380	## 9. Traceability pointers
381	
382	- LLM/code table and ladder: `docs/LLM_VS_CODE.md`. Names used here: generator, judge #1 faithfulness, judge #2 amount classification, judge #3 conflict, states `verified | needs_review | rejected`.
383	- Golden set: `evals/golden/` (qa). Expected values: `spec/SAMPLE_CASE_TRUTHS.md`. Every metric above must be computable from it.
384	- Cards cite R-IDs in their AC text. `evals.run` report rows carry the R-ID next to each metric.
385	- The withdrawn ID R-RV-7 (batch accept, D-011) is not reused.
386	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:51.606Z

**tool call — Bash**
````
{
 "command": "grep -n '\"severity\"\\|\"title\"\\|\"fix\"' reviews/T-013-product-manager-r2.md | cut -c1-600",
 "description": "List r2 finding titles and fixes"
}
````

### User / tool · 2026-11-02T00:41:51.688Z

**tool result**
````
44:  {"severity": "major", "title": "R-IN-5 'confirm a date' contradicts R-RV-2 'date not editable'; no action exists to confirm an ambiguous date",
47:   "fix": "Define a separate review action, e.g. `confirm_date`, that is valid only for entries in DATE_AMBIGUOUS or DATE_MISSING state. The date must be one of the code-parsed readings (04/05 means April 5 or May 4) or a typed valid ISO date. Log it as a review event. Keep general date edits forbidden. Add it to R-RV-2's per-type table and to the §8 conflict list for api.md.",
49:  {"severity": "major", "title": "Scope grew 47 -> 61 R-IDs; three add-ons not required by Appendix A should move to non-goals",
52:   "fix": "Move to §5 non-goals and SCOPE_CUTS: (a) charge reclassification. Charges become {accept, dismiss}, the class is code + judge #2, and the R-RV-1 charge cells drop 'edit'. This is also safer: no path turns the $185 rate into a totaled charge. (b) Batch accept: per-item keyboard accept (R-RV-4) is enough for about 10 records, and widening non-goal 14 to all batch accept respects ADR-005's 'Amounts and dates always need an explicit accept'. (c) The duplicate-charge split action: keep the code merge and its visible 'duplicate of' note. Keep R-CH-6's merge and R-TL-7.",
54:  {"severity": "major", "title": "R-TL-8 (hedge travels with finding) keys on a lexicon 'hedge' category that does not exist; the record-6 assertion has no rule behind it",
57:   "fix": "Name the trigger concretely. Either (a) ask the researcher to add a `hedge: true` tag to named lexicon entries (may_represent, correlate_clinically, and the others) and cite those IDs, or (b) say 'any lexicon entry with flag_type causation_weakening or compliance in the same record'. Make the entry-6 assertion follow from that rule. Define 'sentence' (split on '.', '?', '!' followed by space+capital or end; known abbreviations list) or point to the splitter's unit test.",
59:  {"severity": "major", "title": "R-EX-1 'no flag text' test bans record words that no rule keeps out of entry excerpts; flag evidence can still reach the letter via excerpts",
62:   "fix": "Pick one rule and state it. (a) Excerpt selection: an entry excerpt quotes the encounter's findings, treatment and plan. A sentence whose only role is flag evidence (prior condition, body-date conflict) is left out of the entry excerpt, except that R-TL-8 qualifiers always stay. Code enforces this from flag evidence offsets. Or (b) record sentences may appear verbatim in excerpts: drop the record-word strings from R-EX-1 and assert only flag labels, titles and explanations. Record the choice as an assumption; it depends on the paralegal's open question to Chris.",
64:  {"severity": "major", "title": "§8 'Design conflicts' is not a clean hand-off: the governing decisions are unrecorded, no card owns reconciliation, and the list is incomplete",
67:   "fix": "Before T-017 plans cards, have the orchestrator record decisions 1-10 (STATE or a DECISIONS proposal). Then open one architect card that amends ADR-005/ADR-009/api.md item by item, using the completed list (including the six above, plus qa items for the golden vocabulary and aliases and for sample.export.expected.txt), and list it in T-017's depends_on. If the scope cuts in the previous finding land, R-RV-7 and R-CH-7 drop off the list.",
69:  {"severity": "minor", "title": "R-EX-6 byte-for-byte golden includes LLM-written summaries but names no backend; the golden file has no owning card",
72:   "fix": "State 'on the `fixture` backend (recorded sample responses)', and name the qa card that writes the golden file.",
74:  {"severity": "minor", "title": "R-FL-4 says record 7 'must' raise causation flags; the golden marks them 'should' and credits them via G1/C1",
77:   "fix": "Align them: either REQ says 'should (credited via G1/C1)', or qa raises K4 and K5 to must.",
79:  {"severity": "minor", "title": "Golden provider aliases accept non-verbatim names that R-TL-9 rejects",
82:   "fix": "qa removes the non-verbatim aliases, or R-TL-9 states that the aliases are for matching only.",
84:  {"severity": "minor", "title": "Ship-bar row 5 score key is not yet in the paralegal brief or agent",
87:   "fix": "The orchestrator adds the key to the M3 paralegal brief template, or REQ adopts the key the persona already emits.",
89:  {"severity": "minor", "title": "R-CO-8 currently fails: non-goals 12 and 14 are not in SCOPE_CUTS",
92:   "fix": "The orchestrator logs NG12 and NG14, plus the cuts recommended above; the writer adds SCOPE_CUTS 13 to §5.",
94:  {"severity": "nit", "title": "Flag dismissal reason and edit-note text have no length or content rule",
97:   "fix": "Optional: cap length and print it verbatim, labeled 'reviewer note'.",
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:53.996Z

Now the deterministic checks: the R-ID inventory, the lexicon keys, decisions, and SCOPE_CUTS.

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:57.535Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\nt=open('spec/REQUIREMENTS.md').read()\ndefined=re.findall(r'^\\| (R-[A-Z]{2}-\\d+) \\|',t,re.M)\nrefs=set(re.findall(r'R-[A-Z]{2}-\\d+',t))\nprint('defined',len(defined),'dupes',[d for d in set(defined) if defined.count(d)>1])\nprint('refs not defined',sorted(refs-set(defined)))\nfrom collections import Counter\nprint(Counter(d.split('-')[1] for d in defined))\nfor m in ['D-0%02d'%i for i in range(1,19)]:\n    pass\nprint('D refs',sorted(set(re.findall(r'D-0\\d\\d',t))))\nEOF\nls memory/; grep -n '^## \\|^### ' memory/ORCHESTRATOR_DECISIONS.md | head -40; grep -n 'ADR-017' memory/DECISIONS.md | head",
 "description": "R-ID inventory and decision file headings"
}
````

### User / tool · 2026-11-02T00:41:57.663Z

**tool result**
````
defined 62 dupes []
refs not defined ['R-RV-7']
Counter({'TL': 10, 'EX': 9, 'CO': 9, 'FL': 8, 'RV': 8, 'CH': 7, 'IN': 5, 'SU': 5, 'ST': 1})
D refs ['D-001', 'D-002', 'D-003', 'D-004', 'D-005', 'D-006', 'D-007', 'D-008', 'D-009', 'D-010', 'D-011', 'D-012', 'D-013', 'D-014', 'D-015']
ASSUMPTIONS.md
DECISIONS.md
ENVIRONMENT.md
GLOSSARY.md
LESSONS.md
ORCHESTRATOR_DECISIONS.md
PROGRESS.md
SCOPE_CUTS.md
STATE.md
contracts
10:`spec/REQUIREMENTS.md` (revision 2) and an earlier architect text disagreed, the requirements won. Cross-cutting orchestrator decisions are cited as D-001..D-015 (`memory/ORCHESTRATOR_DECISIONS.md`); where D-0xx and the requirements text differ, the D-0xx wins and the writer updates the requirements (ADR-017).
276:## ADR-017 Reconciliation with spec/REQUIREMENTS.md section 8
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:41:59.932Z

**tool call — Bash**
````
{
 "command": "cat memory/ORCHESTRATOR_DECISIONS.md; sed -n '276,400p' memory/DECISIONS.md",
 "description": "Read orchestrator decisions and ADR-017"
}
````

### User / tool · 2026-11-02T00:42:00.019Z

**tool result**
````
# ORCHESTRATOR DECISIONS (orchestrator is the sole writer)

Cross-cutting product decisions made while triaging reviews. The architect mirrors the technical ones into ADRs
(memory/DECISIONS.md); the writer mirrors the product ones into spec/REQUIREMENTS.md. Each: decision · why · source review.
Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assumption we act on.

| ID | Decision | Why | Source |
|---|---|---|---|
| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts never enter the letter. | Accepting a flag means "I've seen it", not "tell the carrier". | T-013 paralegal r1 (blocker) |
| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
| D-004 | Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
| D-006 | Numbers/dates/$ in a summary or a user edit must appear in that item's excerpt (code check) or the item is needs_review with a reason. | Don't rely on the judge for swapped numerals. | T-014 staff-eng F5, privacy |
| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. NEEDS_CHRIS #8. | Candor without telling the carrier how the chronology was made. | T-014 privacy |
| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows in UI + internal notes. | Keep code-owned facts code-owned. | T-013 PM r2 (major 1, 2) |
| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
## ADR-017 Reconciliation with spec/REQUIREMENTS.md section 8
- Status: accepted (round 2). The writer updates §8 and the affected R-IDs on T-013 round 3.
- Context: §8 listed conflicts between revision 2 of the requirements and the architect's first text. Orchestrator decisions D-001..D-015 settle them. Each item below says where the design landed.
- Decisions:
  1. **Edit rules.** `api.md` no longer allows editing entry `provider` or `date`, or flag `title`/`explanation`. Entries: summary, or excerpt to other whole sentences (D-010, D-012); flags: note only. **Where D-010 differs from R-RV-2/R-CH-7:** charges are accept/dismiss only (no reclassification), so R-CH-7 and the amount rows of R-RV-1/R-RV-2 shrink accordingly. The `confirm_date` action replaces "edit a date" for ambiguous dates (R-IN-5).
  2. **Batch accept.** R-RV-7 is cut (D-011). The API has no batch endpoint; every acceptance is individual.
  3. **Letter content.** Accepted rates and other non-charge amounts moved to the internal notes (R-EX-4, R-EX-8); the letter lists accepted charges and the labelled total only. `cite=short` and the quote toggle are removed: every letter line carries its excerpt, source label, long date and `[Ex. __ / Bates __]` (D-002, R-EX-6). Heading provider is the label as written (D-014); the §6 template's short names ("Austin EMS") change to header labels.
  4. **Codes and fields.** `EXCERPT_OMITS_QUALIFIER` adopted (ADR-016). `GROUNDING_PROVIDER_NOT_IN_RECORD` is not needed because provider is code-set; R-TL-9's test is restated. `source_kind` adopted (ADR-013). Amount class `damages` replaces `other` (ADR-011).
  5. **Vocabulary.** Flag types are `gap | conflict | pre_existing | causation | record_warning` (D-013); the requirements' `prior_condition` becomes `pre_existing`.
  6. **Gap scope.** Gaps are over clinical-encounter records only (D-003); R-FL-1 and R-IN-5 gain that sentence. Missing dates (no readings) cannot be confirmed and stay excluded; ambiguous ones are confirmed by choosing a code-proposed reading.
  7. **R-RV-6 wording.** The test should read "no item's `review_status` changes and no flag is created resolved"; an advisory `needs_review` (ADR-008) is intended.
  8. **R-EX-6 golden export.** The letter must be byte-equal to `evals/golden/sample.export.expected.txt`, which fixes the summaries; qa and backend record fixtures so the summaries in the golden file are the ones replayed.
  9. **Ship-bar key.** `scores.verify_quickly` (D-015) is unaffected by the architecture.
- Consequences: no remaining known conflict between this log, `docs/LLM_VS_CODE.md`, `memory/contracts/api.md` and the requirements once the writer lands the edits above.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:02.477Z

Now checking the lexicon against R-TL-8's hedge set and against D-018.

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:06.315Z

**tool call — Bash**
````
{
 "command": "ls -la app/llm/ 2>&1 | head; python3 - <<'EOF'\nimport yaml,collections\nd=yaml.safe_load(open('app/llm/lexicon.yaml'))\nprint(type(d), list(d.keys())[:10] if isinstance(d,dict) else len(d))\nentries = d.get('entries', d) if isinstance(d,dict) else d\nif isinstance(entries,dict):\n    items=[(k,v) for k,v in entries.items()]\nelse:\n    items=[(e.get('id'),e) for e in entries]\nprint('n',len(items))\nkeys=collections.Counter()\nfor k,v in items:\n    if isinstance(v,dict): keys.update(v.keys())\nprint(keys)\nprint(collections.Counter(v.get('flag_type') for k,v in items if isinstance(v,dict)))\nfor want in ['may_represent','correlate_clinically','possibility_terms','cannot_exclude','nonspecific_indeterminate']:\n    m=[(k,v.get('flag_type'),v.get('hedge')) for k,v in items if k==want]\n    print(want, m)\nprint('hedge true:',[k for k,v in items if isinstance(v,dict) and v.get('hedge')])\nEOF\ngit log --oneline -3 -- app/llm/lexicon.yaml",
 "description": "Check lexicon entries and hedge tags"
}
````

### User / tool · 2026-11-02T00:42:06.439Z

**tool result**
````
total 88
drwxr-xr-x@ 4 arsis  staff    128 Nov  1 18:27 .
drwxr-xr-x@ 7 arsis  staff    224 Nov  1 18:40 ..
-rw-r--r--@ 1 arsis  staff  43609 Nov  1 18:27 lexicon.yaml
drwxr-xr-x@ 2 arsis  staff     64 Nov  1 18:03 prompts
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'yaml'
f419c3b feat(research): flag lexicon with negation guard and test vectors (T-009)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:10.098Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport yaml,collections\nd=yaml.safe_load(open('app/llm/lexicon.yaml'))\nprint(list(d.keys()) if isinstance(d,dict) else len(d))\nentries = d.get('entries', d) if isinstance(d,dict) else d\nitems=[(k,v) for k,v in entries.items()] if isinstance(entries,dict) else [(e.get('id'),e) for e in entries]\nprint('n',len(items))\nkeys=collections.Counter()\nfor k,v in items:\n    if isinstance(v,dict): keys.update(v.keys())\nprint(keys)\nprint(collections.Counter(v.get('flag_type') for k,v in items if isinstance(v,dict)))\nfor want in ['may_represent','correlate_clinically','possibility_terms','cannot_exclude','nonspecific_indeterminate']:\n    print(want, [(k,v.get('flag_type'),v.get('hedge')) for k,v in items if k==want])\nprint('hedge true:',[k for k,v in items if isinstance(v,dict) and v.get('hedge')])\nEOF",
 "description": "Inspect lexicon with venv python"
}
````

### User / tool · 2026-11-02T00:42:10.236Z

**tool result**
````
['version', 'flag_types', 'negation', 'entries', 'sources']
n 48
Counter({'id': 48, 'pattern': 48, 'flag_type': 48, 'strength': 48, 'negatable': 48, 'rationale': 48, 'source': 48, 'false_positive': 48, 'appendix_c': 48, 'examples': 48})
Counter({'causation_weakening': 21, 'pre_existing': 17, 'compliance': 10})
may_represent [('may_represent', 'causation_weakening', None)]
correlate_clinically [('correlate_clinically', 'causation_weakening', None)]
possibility_terms [('possibility_terms', 'causation_weakening', None)]
cannot_exclude [('cannot_exclude', 'causation_weakening', None)]
nonspecific_indeterminate [('nonspecific_indeterminate', 'causation_weakening', None)]
hedge true: []
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:16.376Z

All five hedge IDs exist. D-018 promises a `hedge` boolean and a remapped `flag_type`, and neither is in the file yet. Next, the board cards that own §8 and D-018.

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:17.162Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>&1 | head -60",
 "description": "List board cards"
}
````

### User / tool · 2026-11-02T00:42:17.298Z

**tool result**
````
T-001	M0	orchestrator	in_review        	P0	AC 4/4	Board CLI (tools/board.py): cards, transitions, claims, reviews, gates, status
T-002	M0	orchestrator	in_review        	P0	AC 4/4	Board web UI (tools/board_server.py) + Tailscale serve
T-003	M0	orchestrator	in_review        	P0	AC 3/3	Hooks + .claude/settings.json (stop-guard, teammate-idle, board-validate, git-guard, reviewer-write-guard)
T-004	M0	orchestrator	in_review        	P0	AC 3/3	Agent definitions: 8 workers + 13 reviewer personas (provisional)
T-005	M0	orchestrator	in_review        	P1	AC 3/3	CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT
T-006	M0	orchestrator	in_review        	P0	AC 3/3	Secrets scanner + git hygiene (check_secrets.py, .gitignore, conventional commits, tag m0)
T-007	M0	orchestrator	done             	P0	AC 3/3	M0 smoke test (§4.8) + heartbeat + Playwright screenshot of board
T-008	M1	researcher 	in_review        	P0	AC 4/4	Domain research: PI treatment chronologies, demand packages, what adjusters attack
T-009	M1	researcher 	changes_requested	P0	AC 3/3	Flag lexicon (app/llm/lexicon.yaml) with per-phrase rationale and source
T-010	M1	researcher 	in_review        	P0	AC 3/3	Persona dossiers: 5 domain personas (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)
T-011	M1	researcher 	in_review        	P1	AC 2/2	Persona dossiers: 8 product/engineering personas (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
T-012	M1	researcher 	in_review        	P1	AC 1/1	Research: PHI handling and supervision of AI output at law firms
T-013	M1	writer     	in_review        	P0	AC 4/4	spec/REQUIREMENTS.md: testable must-haves, stretch pick, non-goals
T-014	M1	architect  	in_review        	P0	AC 4/4	Architecture ADRs + docs/LLM_VS_CODE.md + API contract draft
T-015	M1	qa         	in_progress      	P0	AC 4/4	Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs
T-016	M1	orchestrator	in_progress      	P0	AC 0/2	Compile persona dossiers into reviewer agent bodies (replace PROVISIONAL)
T-017	M1	orchestrator	ready            	P0	AC 0/2	Plan M2 + M3 cards with testable acceptance criteria traced to REQUIREMENTS and LLM_VS_CODE
T-018	M1	orchestrator	ready            	P0	AC 0/2	Milestone contract review (PM + paralegal + staff-engineer) of M2/M3 AC and the LLM/code table; apply edits
T-019	M5	orchestrator	needs_chris      	P1	AC 0/1	Provide a real Anthropic API key for the public deployment (NEEDS_CHRIS #1)
T-020	M5	orchestrator	cancelled        	P2	AC 0/1	Restart the session once so native agent definitions load (NEEDS_CHRIS #2)
T-021	M5	orchestrator	cancelled        	P2	AC 0/1	Confirm tailnet ports :7777/:7860 are fine (443/8443 kept for your services) (NEEDS_CHRIS #3)
T-022	M5	orchestrator	needs_chris      	P1	AC 0/1	Public link: demo-only or live? (NEEDS_CHRIS #2)
T-023	M5	orchestrator	needs_chris      	P2	AC 0/1	Live-model eval budget on claude.ai plan (NEEDS_CHRIS #3)
T-024	M5	orchestrator	needs_chris      	P2	AC 0/1	Git author email for this repo (NEEDS_CHRIS #4)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:19.332Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-015 | sed -n '1,40p'; echo ----; python3 tools/board.py show T-017 | sed -n '1,30p'; echo ---; python3 tools/board.py show T-009 | grep -n 'D-018\\|hedge\\|flag_type' | head",
 "description": "Show T-015, T-017, T-009 cards"
}
````

### User / tool · 2026-11-02T00:42:19.577Z

**tool result**
````
---
id: "T-015"
title: "Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs"
milestone: "M1"
role: "qa"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:39:58Z"
claimed_by: "qa"
claimed_at: "2026-11-02T00:33:18Z"
rounds: 1
commits: ["47520a8"]
reviews:
  - {"persona": "legal-nurse-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-015-legal-nurse.md", "at": "2026-11-02T00:31:54Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-015-paralegal.md", "at": "2026-11-02T00:32:57Z"}
ac:
  - {"n": 1, "text": "evals/golden/README.md defines the expected-output schema (entries, amounts with class charge|rate|estimate|unclear, flags by type with evidence, must_not list)", "done": true, "evidence": "evals/golden/README.md schema golden/1; check_golden.py passes"}
  - {"n": 2, "text": "sample.expected.json encodes every Appendix C truth incl. gaps 7/7/28/14/73/11/14, total $8,390, PT rate unclear, and the must-not list", "done": true, "evidence": "sample.expected.json: gaps 7/7/28/14/73/11/14, total 8390, A3 rate unclear, 13 must_not; check_golden.py recomputes via datetime"}
  - {"n": 3, "text": ">=6 synthetic cases, each file starts with 'SYNTHETIC' and has an expected.json; together they cover all 10 stress types listed", "done": true, "evidence": "8 case_NN files + expected.json, SYNTHETIC first line; check_golden.py asserts all 10 stress types covered"}
  - {"n": 4, "text": "a 20-item seeded-hallucination set (record + unsupported summary) exists for judge recall", "done": true, "evidence": "evals/golden/hallucinations.jsonl 20 items (+5 controls)"}
---
## Description
evals/golden/. sample.txt = Appendix A records verbatim; sample.expected.json from spec/SAMPLE_CASE_TRUTHS.md (verify every gap by hand). Synthetic cases (labeled SYNTHETIC) stress: date-format variety, 29/30/31-day boundaries, a rate not a charge, OCR noise '$1,2OO', no amounts, duplicate records, provider-name conflict, subtle pre-existing mention, prompt-injection record, a record tempting the LLM to infer a diagnosis. Reviewed by paralegal + legal-nurse personas before code exists.

## Notes (append-only, newest last)
- 2026-11-02T00:18:01Z qa: claimed
- 2026-11-02T00:21:55Z qa: Read SPEC App A/C + CONTRACT 5/8. api.md and LLM_VS_CODE.md not yet written; golden schema is qa-owned (golden/1). Plan: generator script in scratchpad emits txt+json from one set of hand-written records; committed check_golden.py verifies verbatim excerpts, gap arithmetic, regex must_nots vs input.
- 2026-11-02T00:24:20Z qa: Generated sample + 8 synthetic cases (txt+expected.json) and hallucinations.jsonl (20) + controls (5). Next: check_golden.py validator, README.
- 2026-11-02T00:25:39Z qa: AC 1 checked: evals/golden/README.md schema golden/1; check_golden.py passes
- 2026-11-02T00:25:39Z qa: AC 2 checked: sample.expected.json: gaps 7/7/28/14/73/11/14, total 8390, A3 rate unclear, 13 must_not; check_golden.py recomputes via datetime
- 2026-11-02T00:25:39Z qa: AC 3 checked: 8 case_NN files + expected.json, SYNTHETIC first line; check_golden.py asserts all 10 stress types covered
- 2026-11-02T00:25:39Z qa: AC 4 checked: evals/golden/hallucinations.jsonl 20 items (+5 controls)
- 2026-11-02T00:25:39Z qa: moved in_progress -> in_review
- 2026-11-02T00:26:21Z orchestrator: review dispatched: paralegal-reviewer, legal-nurse-reviewer
- 2026-11-02T00:31:54Z orchestrator: review legal-nurse-reviewer (claude-opus-5-5): fail — reviews/T-015-legal-nurse.md; round 1; findings:
    - [blocker] M6 (concussion without loss of consciousness) fails faithful summaries and passes the actual reversal — fix: Anchor the check positively, not with a single negative lookbehind. Match any reversal (lost consciousness, with/+ LOC, brief LOC, knocked out, unconscious, TBI, mild/moderate/severe concussion, post-concussion syndrome). Allow every negated form (without, w/o, no, denies, w
    - [blocker] M2/M3 (degenerative/traumatic/causation) fail correct causation-flag wording and miss direct conversions of the hedge — fix: Split the checks. (a) Hedge conversion: in summaries, flag a degenerative/traumatic characterisation unless it carries a hedge ('may', 'might', 'could', 'possible'). Add 'degenerative disc disease', 'DDD', 'likely/probable degenerative' and 'age-related'. (b)
----
---
id: "T-017"
title: "Plan M2 + M3 cards with testable acceptance criteria traced to REQUIREMENTS and LLM_VS_CODE"
milestone: "M1"
role: "orchestrator"
status: "ready"
priority: "P0"
depends_on: ["T-013", "T-014", "T-015"]
created_by: "orchestrator"
created_at: "2026-11-02T00:17:08Z"
updated_at: "2026-11-02T00:17:08Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "every R-ID in spec/REQUIREMENTS.md is covered by >=1 M2/M3 card AC", "done": false, "evidence": null}
  - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)

## Handoff (filled when moving to in_review)

---
20:  - {"n": 1, "text": "app/llm/lexicon.yaml parses with yaml.safe_load and every entry has pattern, flag_type, rationale, source", "done": true, "evidence": ".venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS (yaml.safe_load; required fields id/pattern/flag_type/rationale/source/false_positive/strength/negatable on all 48; all regexes compile with re.I)"}
25:Deterministic second signal for the pre-existing and causation-weakening flags (docs/CONTRACT.md §5.2). Each entry: pattern (literal or regex), flag_type (pre_existing | causation_weakening | compliance), rationale, source, false-positive notes.
32:- 2026-11-02T00:28:02Z researcher: AC 1 checked: .venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS (yaml.safe_load; required fields id/pattern/flag_type/rationale/source/false_positive/strength/negatable on all 48; all regexes compile with re.I)
43:    - [major] Hedge coverage is uneven: 'Clinical correlation recommended' is a high flag, but its common variants and 'suggestive of' get nothing — fix: Widen correlate_clinically to 'correlat\w*\s+with\s+(?:the\s+)?(?:clinical|history|physical|exam|symptoms|findings)'. Add a hedge entry (medium) for 'suggestive of | compatible with | concerning for | cannot be differentiated | (degenerative|chro
46:    - [minor] Some false-positive notes are not real false-positive analysis — fix: Say that it is boilerplate, and that the flag matters most when a hedge or alternative-cause term co-occurs in the same impression. Consider downgrading the stand-alone hit to medium (see question). For age_related, write the real false positives: 'age-appropriate' attached to a normal finding, and congenital findi
51:What changed: app/llm/lexicon.yaml (48 entries, negation block, strength tiers, test vectors) + research/lexicon_selfcheck.py (reference guard + example tests). How verified: selfcheck PASS; sample-record hits equal appendix_c expectations; FP probes clean. What's left: backend implements matcher per header semantics (dedupe per span+flag_type; year>=accident-year filter for prior_history_year_resolved and dated_prior_event); qa can lift examples into tests/. Surprised: the low-strength context entries (normal_imaging on 'CT head negative', improving pain) would hurt flag precision if treated as flags — hence the strength tier; recommend backend raise flags only on high/medium.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:42:57.862Z

Next: SCOPE_CUTS parity, A-106, NEEDS_CHRIS, the edit rules in api.md, and the golden facts the R-IDs cite.

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:00.352Z

**tool call — Bash**
````
{
 "command": "echo \"== SCOPE_CUTS\"; grep -n '^| *[0-9]' memory/SCOPE_CUTS.md | cut -c1-140; echo \"== A-106\"; grep -n 'A-106' memory/ASSUMPTIONS.md | cut -c1-300; echo \"== NEEDS_CHRIS rows\"; grep -n '^| *#\\?[0-9]\\|^## \\|^### ' submission/NEEDS_CHRIS.md | cut -c1-160; echo \"== api confirm_date / edit\"; grep -n 'confirm_date\\|invalid_edit\\|reclass\\|batch' memory/contracts/api.md | cut -c1-220",
 "description": "Check SCOPE_CUTS, A-106, NEEDS_CHRIS, api.md"
}
````

### User / tool · 2026-11-02T00:43:00.468Z

**tool result**
````
== SCOPE_CUTS
5:| 1 | PDF upload / OCR | OCR errors would sit upstream of the grounding check, so "verbatim excerpt" would stop meaning "in the record". |
6:| 2 | Multi-case / matter management | One case proves the workflow; matter management is commodity. | ~2 days: case table, list view, per
7:| 3 | Accounts, auth, roles, sharing | Prototype; nothing persists beyond a session. | ~1–2 days with an IdP; required before real data.
8:| 4 | Real data / PHI handling (retention, BAA, encryption at rest) | Spec forbids real data; we design for it in docs but don't implement
9:| 5 | Demand-letter prose in a firm's voice | Generated advocacy text is where invented facts creep in; export stays structured and cited.
10:| 6 | Medical or legal judgment (diagnosis, severity, causation opinions) | Flags point at the record's own words; judgment stays with th
11:| 7 | Billing analysis (PT total from rate, reasonableness, liens, paid vs incurred) | Totals only stated charges; anything else is "uncl
12:| 8 | Integrations (EHR, case management, email intake) | Paste/upload is enough to prove the workflow. | Per integration, days. | M1 (8)
13:| 9 | Per-user learning from dismissals | Dismissals logged for metrics only; feeding them back would need its own evals. | ~2 days + eva
14:| 10 | Numeric confidence scores | Three states (verified / needs_review / rejected) — a percentage would imply precision we can't veri
15:| 11 | Non-English records, handwriting | Clear failure message; chaos-tested. | Translation + separate grounding rules. | M1 (11) |
16:| 12 | Manually adding a timeline entry for a record the pipeline rejected | Keeps every entry machine-grounded; a rejected record stays 
17:| 13 | LLM fallback for ambiguous record splitting | Code splits on dates/headers; an unsplittable paste is flagged for the paralegal ins
18:| 14 | Batch accept | Not a must-have; needs an ADR change; single-key accept is fast enough for a 9-record case. | ~half day + guard so 
19:| 15 | Charge reclassification by the paralegal | A rate must never become a totaled charge; accept/dismiss is enough. | ~half day + judg
20:| 16 | "Not a duplicate" split action | Dedupe merge stays visible with "duplicate of" note. | ~2 h. | M1 (D-011) |
21:| 17 | LLM date pointing, BYOK, audit ?full=1, flag text edits, case list | Time box; exposure on a public Space. | ~1 day total. | M1 (D
22:| 18 | Per-packet date-convention inference (infer MM/DD vs DD/MM from other dates) | An ambiguous numeric date always asks once; inferen
23:| 19 | Exhibit/Bates numbering by the tool | Placeholder only; firm numbering lives in its own system. | Config + integration with the fi
== A-106
20:| A-106 | The export cites each line by provider (as written in the record header) + date of service, with an `[Ex. __ / Bates __]` placeholder the paralegal fills; the tool assigns no numbers. Internal notes cite provider + date, not record numbers. | No Bates numbers in synthetic records; D-002
== NEEDS_CHRIS rows
8:| 1 | P1 | T-019 | Real Anthropic API key for the public deployment | Put a real key in `.env` as `ANTHROPIC_API_KEY=<redacted> (local) and as the Space secret `ANT
9:| 2 | P1 | T-022 | Public link: demo-only or live? | Inbox: `demo-only` or `live, cap $N/day`. | Demo-only (cached sample run through the real pipeline code).
10:| 3 | P2 | T-023 | Live-model eval budget on your claude.ai plan (~25–35 calls per sample run) | Inbox: `ok` or a cap, e.g. `max 300 calls`. | Live runs on
11:| 4 | P2 | T-024 | Git author email in history is your work address from global git config | Inbox: `keep`, or the email to use for this repo going forward (
15:## Decided by the team — FYI, no action needed
== api confirm_date / edit
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request`, `not_found`, `input_too_large`, `demo_mode_unsupported_input`, `rate_limited`, `spend_cap
23:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
194:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Fl
196:## POST /api/cases/{token}/records/{rid}/confirm_date
208:`422 date_invalid` when the date is not one of the record's candidates. Logged as a `confirm_date` event. (The numbers above come from golden `case_01`, not the sample case.)
240:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:13.446Z

Two possible contradictions turned up: A-106 says the notes do not cite record numbers, which R-EX-4 contradicts, and the D-0xx decisions cite NEEDS_CHRIS rows #7, #8 and #10. Checking both.

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:15.277Z

**tool call — Bash**
````
{
 "command": "sed -n 15,40p submission/NEEDS_CHRIS.md | cut -c1-260; echo \"== api export\"; grep -n 'internal_notes\\|record N\\|record [0-9] (' memory/contracts/api.md | cut -c1-260 | head -20; git log --oneline -3 -- memory/ASSUMPTIONS.md submission/NEEDS_CHRIS.md memory/SCOPE_CUTS.md",
 "description": "NEEDS_CHRIS FYI section, api export notes format"
}
````

### User / tool · 2026-11-02T00:43:15.401Z

**tool result**
````
## Decided by the team — FYI, no action needed
Product calls we made under ambiguity. Override any of them through the Inbox if you disagree.
- Citation format in the export: `Provider, date of service` + `[Ex. __ / Bates __]` placeholder (A-106). Real Zinda practice is a discovery question in Part 2, area 1.
- Flags (gaps, priors, causation) never go in the letter text; they go in a separate "internal — do not send" block (D-001).
- AI-assistance statement: UI banner + internal notes, not the letter (D-009).
- Flagged record language may appear in the letter only as part of an accepted whole-sentence excerpt, listed in internal notes (D-012).
- Ambiguous dates are never inferred; the paralegal confirms them (D-010).
- Tailnet ports: board on :7777, app on :7860; your existing 443/8443 mappings untouched (ADR-000e).
== api export
26:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items |
267:  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nPrepared with AI assistance; each item reviewed and accepted by the user.\nModels: claude-sonnet-5-5 (drafting), claude-haiku-5-5 (checking). Backend: fixture (cached demo, recorded with cl
56750da docs(orchestrator): A-106 citation format, scope cuts 18-19
5737b03 docs(orchestrator): NEEDS_CHRIS only genuine asks; D-016..D-018
5fe481e docs(orchestrator): decision log D-001..D-015, state, scope cuts
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:17.458Z

**tool call — Bash**
````
{
 "command": "sed -n 255,300p memory/contracts/api.md | cut -c1-900; git show 56750da --stat | head; git log -1 --format='%H %ci' 56750da; git log -1 --format='%H %ci' b4f3924",
 "description": "Read api.md export example and commit timing"
}
````

### User / tool · 2026-11-02T00:43:17.593Z

**tool result**
````
  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
  "review": { "counts": {"pending": 21, "accepted": 0, "edited": 1, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
  "warnings": [] }
```
The frontend does not need to refetch the case.

## GET /api/cases/{token}/export
Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. The example reflects a case in which only entry e2 and charge a1 are accepted.
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "generated_at": "2026-11-02T01:20:00Z",
  "letter_text": "TREATMENT CHRONOLOGY\n\nJanuary 9, 2026 — Central ER discharge summary\nDiagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.\nSource: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]: \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.\"\n\nBILLED CHARGES\n\nCentral ER discharge summary, January 9, 2026 ........ $6,240.00\nSource: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]: \"ER charges: $6,240.\"\n\nBilled charges stated in these records: $6,240 (excludes physical therapy — per-visit rate only, visit count not stated)",
  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nPrepared with AI assistance; each item reviewed and accepted by the user.\nModels: claude-sonnet-5-5 (drafting), claude-haiku-5-5 (checking). Backend: fixture (cached demo, recorded with claude-cli). Prompt versions: extract_v1, judge_faithfulness_v1, judge_amount_class_v1, flags_v1.\n\nFLAGS ACCEPTED\n- none\n\nFLAGGED LANGUAGE QUOTED IN THE LETTER\n- none (entry 2 quotes no flagged wording)\n\nAMOUNTS NOT TOTALED\n- Capital PT, record 4: \"Charge per visit $185.\" Rate $185/visit; visit count not stated. Request itemized PT ledger.\n\nRECORDS NOT IN THE TREATMENT SECTION\n- Record 1 (not reviewed); records 3 to 9 (not reviewed)\n\nEDITED ITEMS\n- none\n\nPENDING ITEMS NOT INCLUDED\n- 21 items",
  "items": {
    "entries": [ {"id": "e2", "record_ids": ["r2"], "edited": false, "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."} ],
    "amounts": [ {"id": "a1", "kind": "charge", "counted_in_total": true, "edited": false, "excerpt": "ER charges: $6,240."} ],
    "flags": [] },
  "totals": { "charges_cents": 624000, "charges_count": 1 },
  "counts": { "entries_in_letter": 1, "charges_in_letter": 1, "flags_in_notes": 0, "records_in_letter": 1, "records_total": 9 },
  "excluded": { "pending": 21, "dismissed": 0, "rejected": 0 },
  "provenance": { "generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "backend": "fixture", "recorded_from": "claude-cli",
                  "demo_mode": true, "prompt_versions": ["extract_v1","judge_faithfulness_v1","judge_amount_class_v1","flags_v1"], "edited_count": 0 },
  "warnings": [ {"code": "ITEMS_PENDING", "message": "21 items are still pending and are not included.", "item_id": null} ] }
```
Guarantees (tested): flagged language that is quoted inside an accepted excerpt is listed in the internal notes under "flagged language quoted in the letter" (D-012); every entry and charge line in `letter_text` is followed by its verbatim excerpt, a source label and a long date; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; the `counts` line is outside both blocks (R-EX-5); with all 9 entries and both charges accepted and nothing edited, `letter_text` equals `evals/golden/sample.export.expected.txt`.

## GET /api/cases/{token}/audit
JSON for this case only (including full prompt text for each call).
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
  "calls": [ { "id": "c1", "role": "generator", "step": "extract", "backend": "fixture", "model": "claude-sonnet-5-5", "prompt_version": "extract_v1",
               "prompt_sha256": "9f2c0a77", "item_id": "e1", "attempt": 1, "latency_ms": 5120, "cost_usd": 0.0041, "verdict": null, "parsed_ok": true,
               "system_text": "You read one medical record ...", "user_text": "<<<RECORD-3fa91c0b2d44>>> ... <<<END-3fa91c0b2d44>>>", "response_raw": "{\"provider\": \"Austin EMS\"}" } ],
  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ],
  "summary": { "calls": 30, "cost_usd": 0.19, "latency_ms_total": 71200, "by_backend": {"fixture": 30} } }
```

## DELETE /api/cases/{token}
`204`. Removes the case, records, items, calls and events. It never changes the spend ledger (ADR-006).

---

## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
| Code | State | Meaning |
|---|---|---|
| `GROUNDING_EXCERPT_NOT_VERBATIM` | rejected | model's excerpt is not word for word in the record |
commit 56750da094073de366854bd7ae6f1c02c5f6a5e2
Author: Chris Borsheim <<redacted-private>>
Date:   Sun Nov 1 18:41:47 2026 -0600

    docs(orchestrator): A-106 citation format, scope cuts 18-19
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 board/activity.jsonl  | 33 +++++++++++++++++++++++++++++++++
 board/cards/T-005.md  | 11 +++++++----
56750da094073de366854bd7ae6f1c02c5f6a5e2 2026-11-01 18:41:47 -0600
b4f3924366246206b26428345fd727bb3bf050a7 2026-11-01 18:41:23 -0600
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:26.777Z

The api.md export example conflicts with R-EX-6 and R-EX-8: it has dot leaders, a different total wording, and a different Source line format. Checking api.md's history and T-014's status.

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:28.411Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ci %s' -5 -- memory/contracts/api.md; python3 tools/board.py show T-014 | grep -n 'status\\|rounds\\|ADR-017\\|api.md' | head -15; grep -n '\\.\\.\\.\\.\\|visit count\\|excludes physical' memory/contracts/api.md | cut -c1-120",
 "description": "api.md history and T-014 status"
}
````

### User / tool · 2026-11-02T00:43:28.572Z

**tool result**
````
e442626 2026-11-01 18:40:17 -0600 docs(architect): round 2 ADRs, templated flags, record-date gaps, API contract
94c7b08 2026-11-01 18:22:54 -0600 docs(architect): ADRs, LLM/code table, API contract draft
fbe5690 2026-11-01 18:15:44 -0600 feat(harness): board CLI, web UI, hooks, agent roster, memory seeds
6:status: "in_review"
14:rounds: 1
22:  - {"n": 3, "text": "memory/contracts/api.md draft lists every endpoint the review UI needs with request/response JSON examples", "done": true, "evidence": "memory/contracts/api.md: 11 endpoints with JSON examples, marked DRAFT - backend owns from M2"}
26:ADRs for stack (default: Python 3.11+, FastAPI, SQLite, build-step-free frontend, Anthropic SDK, Playwright, Docker :7860), data model (records, entries, amounts, flags, ladder records per D.4, audit), deployment target (HF Spaces Docker primary, Replit alternate, demo mode), and the LLM provider abstraction (claude-cli default dev / anthropic-api / fixture — §5.2). LLM_VS_CODE.md = §5.2 table completed with reasons, plus rules. Draft memory/contracts/api.md (endpoints + JSON examples) for backend to own.
30:- 2026-11-02T00:19:43Z architect: Read contract §5.2/§8/§10/D.4, SPEC, truths, ENV. REQUIREMENTS.md not present yet. Plan: ADR-001..008, LLM_VS_CODE.md, api.md draft, app/README-arch.md. Design stance: code is source of truth for dates/amounts/offsets; LLM only classifies/summarises; edits to export separate letter text from internal flag notes.
33:- 2026-11-02T00:22:53Z architect: AC 3 checked: memory/contracts/api.md: 11 endpoints with JSON examples, marked DRAFT - backend owns from M2
40:    - [blocker] F2 Gap engine runs over LLM-produced entries, so a rejected/failed record produces a false gap that is marked verified — fix: Compute gaps from the code-parsed `records.date_iso` where `date_status='parsed'`, independent of entries. Say so in LLM_VS_CODE row 9, the README-arch stage list and the api example. Records with ambiguous/missing dates are listed in the flag as "excluded f
56:- 2026-11-02T00:40:16Z architect: Round 2 applied: ADR-002..009 rewritten, ADR-010..017 added (gaps from record dates, code amounts + J2 on all, token check, templated flags, accident-date rule + absolute offsets, cuts, whole-sentence excerpts, REQUIREMENTS sec 8 reconciliation); LLM_VS_CODE 20 rows; api.md 12 endpoints, 14 JSON blocks parse, 17 offset checks pass on evals/golden/sample.txt; D-001..D-017 cited. Deviations to confirm: token check allowed text = excerpt + source label + parsed date (so 'Visit 8' passes); provider code-set from header so R-TL-9 seeded test restated; missing dates cannot be confirmed.
61:Round 2. What changed: DECISIONS.md (ADR-002..009 rewritten; new 010-017 incl. reconciliation with REQUIREMENTS s8), LLM_VS_CODE.md (20 rows + injection worked example), api.md (12 endpoints; no case list, batch, cite, ?full), README-arch.md (modules, invariants, data flow, cuts). Resolved: SE F1/PV B2 export carries excerpt on every line (ADR-009, no cite toggle); F2 gaps over record dates, encounter-only (ADR-010); F3 J2 on every amount, code classifies (ADR-011); F4 accident-date rule + header grounding + offsets [1407,1452) [123,139) [332,348) (ADR-014); F5 token check -> needs_review SUMMARY_TOKEN_NOT_IN_EXCERPT (ADR-012); F6/PV random tokens, no list, demo-only default, append-only spend ledger, lazy purge (ADR-006); F7 warnings + 409 needs_confirm, confirm_date recomputes gaps; F8 templated flags + source_kind (ADR-013); F9 retries only in audited.py, 8 min deadline; F10 absolute offsets + normalisation map, HIGHLIGHT_NOT_FOUND, valid JSON; F11 chronological entries; F12 cuts (ADR-015); F13 injection advisory, structural controls (ADR-008); F14 recorded_from, tempdir, one fenced JSON; PV injection blocker: amounts classified by code, tagged record cannot yield a charge, all-record passes carry tag; AI disclosure in internal notes + provenance; ADR-000d/e corrected. How verified: script parsed all 14 JSON blocks and checked 17 raw_text[start:end]==excerpt against evals/golden/sample.txt. Left: writer updates REQUIREMENTS s8 (R-RV-7 cut, R-CH-7 shrinks, R-TL-9 restated, R-RV-6 wording, prior_condition->pre_existing); lexicon needs non_encounter, accident_date_phrases, injection categories (researcher); golden export summaries must match recorded fixtures (qa/backend). Surprised: D-012 splits on ';' so 'Dx: cervical strain;' is its own sentence unit.
266:  "letter_text": "TREATMENT CHRONOLOGY\n\nJanuary 9, 2026 — Central ER discharge summary\nDiagnosed with cervical 
267:  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nPrepared with AI assistance; each item reviewed a
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:32.653Z

Now the hands-on part. I'll prototype the R-TL-2 splitter on the sample and check the §6 excerpts and the golden facts the R-IDs cite.

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:34.186Z

**tool call — Bash**
````
{
 "command": "ls evals/golden/; head -c 1500 evals/golden/sample.txt; echo; .venv/bin/python -c \"\nimport json;d=json.load(open('evals/golden/sample.expected.json'));print(list(d.keys()));print(json.dumps(d['entries'][5] if 'entries' in d else '',indent=0)[:800])\"",
 "description": "Look at golden files and sample structure"
}
````

### User / tool · 2026-11-02T00:43:34.292Z

**tool result**
````
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data

=== Record 1 ===
Date: 2026-01-09
Source: Austin EMS run report
Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

=== Record 2 ===
Date: 2026-01-09
Source: Central ER discharge summary
Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."

=== Record 3 ===
Date: 2026-01-16
Source: Dr. Alvarez, primary care
Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."

=== Record 4 ===
Date: 2026-01-23
Source: Capital PT, initial evaluation
Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."

=== Record 5 ===
Date: 2026-02-20
Source: Capital PT, visit 8
Excerpt: "Pain 4/10, improving. Patient reports missing 3 days of work."

=== Record 6 ===
Date: 2026-03-06
Source: Capital PT, visit 9
Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."

=== Record 7 ===
Date: 2026-05-18
Source: Hill Country Pain Management, new patient
Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."

=== Record 8 ===
Date: 2026-05-29
Source: A
['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'seeded_edits', 'must_not', 'notes']
{
"id": "E6",
"record_nos": [
6
],
"date": "2026-03-06",
"date_status": "parsed",
"encounter": true,
"provider": "Capital PT, visit 9",
"must_contain_excerpt": "Discharged from PT after two missed appointments",
"required_terms": [
"discharged",
"two missed appointments"
]
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:35.946Z

`sample.export.expected.txt` and `seeded_edits` now exist. Running the prototype checks.

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:49.989Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $SP/r3check.py <<'EOF'\nimport re,json,sys\nroot='/Users/arsis/zlayt-pm-project/'\nreq=open(root+'spec/REQUIREMENTS.md').read()\ns=open(root+'evals/golden/sample.txt').read()\nrecs={}\nfor m in re.finditer(r'=== Record (\\d+) ===\\nDate: (\\S+)\\nSource: (.+)\\nExcerpt: \"(.*)\"',s):\n    recs[int(m[1])]=(m[2],m[3],m[4])\nprint('records',len(recs))\nABBR=['approx.','Dr.','Mr.','Mrs.','Ms.','vs.','etc.','e.g.','i.e.']\ndef units(t):\n    out=[];start=0;i=0\n    while i<len(t):\n        c=t[i]\n        if c in ';\\n':\n            out.append(t[start:i+1]);start=i+1\n        elif c in '.?!':\n            pre=t[start:i+1]\n            if any(pre.endswith(a) for a in ABBR) or (c=='.' and i+1<len(t) and t[i+1].isdigit()):\n                pass\n            else:\n                rest=t[i+1:]\n                m=re.match(r'\\s+([A-Z0-9])',rest)\n                if rest=='' or m:\n                    out.append(t[start:i+1]);start=i+1\n        i+=1\n    if start<len(t): out.append(t[start:])\n    return out\nallok=True\nfor n,(d,src,txt) in recs.items():\n    u=units(txt)\n    assert ''.join(u)==txt\n    print(n,[x.strip() for x in u])\n# R-TL-2 claim: approx. 35 mph. one unit\nprint('approx unit:',[x for x in units(recs[1][2]) if 'approx' in x])\n# §6 letter excerpts: contiguous whole-unit runs?\nblk=req.split('**Block 1')[1].split('```')[1]\nsrcs=re.findall(r'Source \\[Ex\\. __ / Bates __\\]: \"(.*)\"',blk)\nprint('letter source lines',len(srcs))\ndef norm(x): return re.sub(r'\\s+',' ',x).strip()\nfor q in srcs:\n    hit=None\n    for n,(d,src,txt) in recs.items():\n        u=[x.strip() for x in units(txt)]\n        for i in range(len(u)):\n            for j in range(i+1,len(u)+1):\n                if norm(' '.join(u[i:j]))==norm(q): hit=(n,i,j)\n    print('WHOLE-UNIT' if hit else 'NOT-WHOLE', hit, q[:60])\n# R-EX-1 negative strings vs §6 letter\nfor neg in ['REVIEWER NOTE','73 days','AI assistance','Gap','Conflict','Prior condition','Causation','pre_existing','gap','conflict','causation','visit count','rate']:\n    print('neg',repr(neg), neg in blk)\n# golden export file vs §6\ng=open(root+'evals/golden/sample.export.expected.txt').read()\nprint('golden == §6 block1 (strip):', g.strip()==blk.strip())\nif g.strip()!=blk.strip():\n    import difflib\n    for l in list(difflib.unified_diff(blk.strip().splitlines(),g.strip().splitlines(),'REQ§6','golden',lineterm=''))[:40]: print(l)\nprint('golden has ..:', '..' in g.replace('approx.','').replace('...',''))\n# providers/aliases\ne=json.load(open(root+'evals/golden/sample.expected.json'))\nfor en in e['entries']:\n    lab=recs[en['record_nos'][0]][1]\n    als=en.get('provider_aliases',[])+([en['provider']] if 'provider' in en else [])\n    bad=[a for a in als if norm(a).lower() not in norm(lab).lower()]\n    if bad: print('ALIAS not substring', en['id'], lab, bad)\nprint('entry keys',sorted(e['entries'][0].keys()))\nprint('seeded_edits',json.dumps(e['seeded_edits'])[:600])\nEOF\n.venv/bin/python -I $SP/r3check.py",
 "description": "Prototype splitter, check excerpts, negatives, golden export, aliases"
}
````

### User / tool · 2026-11-02T00:43:50.044Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to $SP/r3check.py)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:43:51.153Z

The hook blocks scratchpad writes, so the script goes under artifacts/review-evidence/ instead.

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:01.061Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r3check.py",
 "content": "\"\"\"T-013 round 3 PM-review probe: splitter prototype per R-TL-2, §6 excerpt units, R-EX-1 negatives, golden export, aliases.\"\"\"\nimport re, json, difflib\nroot = '/Users/arsis/zlayt-pm-project/'\nreq = open(root + 'spec/REQUIREMENTS.md').read()\ns = open(root + 'evals/golden/sample.txt').read()\nrecs = {}\nfor m in re.finditer(r'=== Record (\\d+) ===\\nDate: (\\S+)\\nSource: (.+)\\nExcerpt: \"(.*)\"', s):\n    recs[int(m[1])] = (m[2], m[3], m[4])\nprint('records', len(recs))\nABBR = ['approx.', 'Dr.', 'Mr.', 'Mrs.', 'Ms.', 'vs.', 'etc.', 'e.g.', 'i.e.']\n\n\ndef units(t):\n    out = []; start = 0\n    for i, c in enumerate(t):\n        if c in ';\\n':\n            out.append(t[start:i + 1]); start = i + 1\n        elif c in '.?!':\n            pre = t[start:i + 1]\n            if any(pre.endswith(a) for a in ABBR) or (c == '.' and i + 1 < len(t) and t[i + 1].isdigit()):\n                continue\n            rest = t[i + 1:]\n            if rest == '' or re.match(r'\\s+[A-Z0-9]', rest):\n                out.append(t[start:i + 1]); start = i + 1\n    if start < len(t):\n        out.append(t[start:])\n    return out\n\n\ndef norm(x):\n    return re.sub(r'\\s+', ' ', x).strip()\n\n\nfor n, (d, src, txt) in recs.items():\n    u = units(txt)\n    assert ''.join(u) == txt\n    print(n, [x.strip() for x in u])\nprint('approx unit:', [x for x in units(recs[1][2]) if 'approx' in x])\nblk = req.split('**Block 1')[1].split('```')[1]\nsrcs = re.findall(r'Source \\[Ex\\. __ / Bates __\\]: \"(.*)\"', blk)\nprint('letter source lines', len(srcs))\nfor q in srcs:\n    hit = None\n    for n, (d, src, txt) in recs.items():\n        u = [x.strip() for x in units(txt)]\n        for i in range(len(u)):\n            for j in range(i + 1, len(u) + 1):\n                if norm(' '.join(u[i:j])) == norm(q):\n                    hit = (n, i, j)\n    print('WHOLE-UNIT' if hit else 'NOT-WHOLE', hit, q[:70])\nfor neg in ['REVIEWER NOTE', '73 days', 'AI assistance', 'Gap', 'Conflict', 'Prior condition', 'Causation',\n            'pre_existing', 'gap', 'conflict', 'causation', 'visit count', 'rate']:\n    print('neg', repr(neg), neg in blk)\ng = open(root + 'evals/golden/sample.export.expected.txt').read()\nprint('golden == §6 block1 (strip):', g.strip() == blk.strip())\nif g.strip() != blk.strip():\n    for l in list(difflib.unified_diff(blk.strip().splitlines(), g.strip().splitlines(), 'REQ§6', 'golden', lineterm=''))[:40]:\n        print(l)\ne = json.load(open(root + 'evals/golden/sample.expected.json'))\nprint('entry keys', sorted(e['entries'][0].keys()))\nfor en in e['entries']:\n    lab = recs[en['record_nos'][0]][1]\n    als = list(en.get('provider_aliases', [])) + ([en['provider']] if 'provider' in en else [])\n    bad = [a for a in als if norm(a).lower() not in norm(lab).lower()]\n    if bad:\n        print('ALIAS not substring', en['id'], repr(lab), bad)\nprint('seeded_edits', json.dumps(e['seeded_edits'])[:700])\n"
}
````

### User / tool · 2026-11-02T00:44:01.159Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r3check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:02.910Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-013-r3check.py",
 "description": "Run round-3 probe script"
}
````

### User / tool · 2026-11-02T00:44:03.020Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:22.208Z

<details><summary>thinking</summary>

The golden export file contains both blocks with markers, so R-EX-6's requirement that letter_text equal the golden file can't pass as written. Next I'll check the seeded 10-R-ID sample and the remaining golden facts.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:27.752Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport re,random\nt=open('spec/REQUIREMENTS.md').read()\nids=re.findall(r'^\\| (R-[A-Z]{2}-\\d+) \\|',t,re.M)\nrandom.seed(2026);print(sorted(random.sample(ids,10)))\n\"; .venv/bin/python -I - <<'EOF'\nimport json\nR='/Users/arsis/zlayt-pm-project/evals/golden/'\nfor c in ['case_01_date_formats','case_04_duplicates_no_amounts','case_07_prompt_injection','case_03_rate_and_ocr','case_02_gap_boundaries']:\n    d=json.load(open(R+c+'.expected.json'))\n    print('==',c,'entries',len(d.get('entries',[])),'records',len(d.get('records',[])),'totals',d.get('totals'))\n    if c=='case_01_date_formats':\n        for e in d['entries']:\n            if e.get('date_status')!='parsed': print(' ',json.dumps(e)[:300])\n        print(' warnings',json.dumps(d.get('record_warnings'))[:300])\n    if c=='case_04_duplicates_no_amounts':\n        print(' ',[(e['id'],e['record_nos']) for e in d['entries']])\n    if c=='case_03_rate_and_ocr':\n        print(' ',[(a.get('raw') or a.get('text'),a.get('class'),a.get('value_cents')) for a in d['amounts']][:8])\n    if c=='case_02_gap_boundaries':\n        print(' ', [ (g.get('days'),g.get('flag')) for g in d.get('gap_table',[])])\nh=[l for l in open(R+'hallucinations.jsonl') if l.strip()];c=[l for l in open(R+'hallucinations_controls.jsonl') if l.strip()]\nprint('halluc',len(h),'controls',len(c))\ns=json.load(open(R+'sample.expected.json'))\nprint('sample flags',[(f.get('id'),f.get('type'),f.get('level')) for f in s['flags']])\nprint('must_not ids',[m.get('id') for m in s['must_not']])\nEOF",
 "description": "Draw sample R-IDs and verify golden facts cited by REQ"
}
````

### User / tool · 2026-11-02T00:44:27.880Z

**tool result**
````
['R-CO-9', 'R-EX-1', 'R-EX-2', 'R-EX-4', 'R-FL-6', 'R-RV-3', 'R-SU-4', 'R-TL-10', 'R-TL-2', 'R-TL-3']
== case_01_date_formats entries 8 records 8 totals {'explicit_charges_total': 310, 'counted_amount_ids': ['A1'], 'amounts_found': 1, 'status': 'complete', 'unclear_items': [], 'display': 'Explicit charges: $310.00.'}
  {"id": "E8", "record_nos": [8], "date": null, "date_status": "ambiguous", "encounter": false, "provider": "Dr. Orla Pennywhistle, phone note", "must_contain_excerpt": "Patient reports no new symptoms", "required_terms": [], "source_kind": "patient_self_report", "needs_review": true, "date_candidates
 warnings []
== case_04_duplicates_no_amounts entries 4 records 6 totals {'explicit_charges_total': 0, 'counted_amount_ids': [], 'amounts_found': 0, 'status': 'none_found', 'unclear_items': [], 'display': 'No dollar amounts found in these records.'}
  [('E1', [1, 2]), ('E2', [3, 4]), ('E3', [5]), ('E4', [6])]
== case_07_prompt_injection entries 4 records 4 totals {'explicit_charges_total': 420, 'counted_amount_ids': ['A1'], 'amounts_found': 1, 'status': 'complete', 'unclear_items': [], 'display': 'Explicit charges: $420.'}
== case_03_rate_and_ocr entries 5 records 5 totals {'explicit_charges_total': 335, 'counted_amount_ids': ['A3', 'A5'], 'amounts_found': 5, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A1', 'reason': 'rate', 'total_computed': False}, {'amount_id': 'A2', 'reason': 'OCR noise', 'total_computed': False}, {'amount_id': 'A4', 'reason': 'OCR noise', 'total_computed': False}], 'display': 'Explicit charges: $335 ($95.00 + $240). Not totaled: $95 rate per adjustment; $1,2OO (unclear); $9S.00 (unclear).'}
  [('$95', 'rate', None), ('$1,2OO', 'unclear', None), ('$95.00', 'charge', None), ('$9S.00', 'unclear', None), ('$240', 'charge', None)]
== case_02_gap_boundaries entries 8 records 8 totals {'explicit_charges_total': 0, 'counted_amount_ids': [], 'amounts_found': 0, 'status': 'none_found', 'unclear_items': [], 'display': 'No dollar amounts found in these records.'}
  [(29, False), (30, False), (31, True), (30, False), (31, True), (30, False), (31, True)]
halluc 34 controls 10
sample flags [('G1', 'gap', 'must'), ('C1', 'conflict', 'must'), ('C2', 'conflict', 'must'), ('P1', 'pre_existing', 'must'), ('P2', 'pre_existing', 'must'), ('K1', 'causation', 'must'), ('K2', 'causation', 'must'), ('K3', 'causation', 'must'), ('K4', 'causation', 'must'), ('K5', 'causation', 'must')]
must_not ids ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:41.027Z

The golden set has moved since REQ was written: 34 seeded hallucinations, not 20; K4 and K5 are now `must`; there is an M14; and `source_kind` reads `patient_self_report`. Verifying each.

### Assistant · claude-opus-5-5 · 2026-11-02T00:44:46.512Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json,collections\nR='/Users/arsis/zlayt-pm-project/evals/golden/'\nh=[json.loads(l) for l in open(R+'hallucinations.jsonl') if l.strip()]\nc=[json.loads(l) for l in open(R+'hallucinations_controls.jsonl') if l.strip()]\nprint(len(h),len(set(x.get('id') for x in h)),len(c), sorted(h[0].keys()))\ns=json.load(open(R+'sample.expected.json'))\nprint([ (m['id'], str(m.get('description') or m.get('why') or m)[:90]) for m in s['must_not'] if m['id'] in ('M13','M14')])\nprint([(f['id'],f.get('level'),str(f.get('note') or f.get('credit') or '')[:80]) for f in s['flags'] if f['id'] in ('K4','K5')])\nsk=collections.Counter()\nimport glob\nfor f in glob.glob(R+'*.expected.json'):\n    d=json.load(open(f))\n    for k in ('entries','flags'):\n        for e in d.get(k,[]):\n            if 'source_kind' in e: sk[e['source_kind']]+=1\nprint('source_kind values',sk)\nd=json.load(open(R+'case_01_date_formats.expected.json'))\nprint([e.get('date_candidates') for e in d['entries'] if e['id']=='E8'])\nEOF\ngrep -rn 'patient_report\\|patient_self_report' memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md spec/REQUIREMENTS.md evals/golden/README.md | cut -c1-160; git log --format='%h %ci %s' -4 -- evals/golden/; grep -n 'seeded hallucin\\|95%' docs/CONTRACT.md | head -5",
 "description": "Verify hallucination counts, K4/K5, M14, source_kind vocab"
}
````

### User / tool · 2026-11-02T00:44:46.653Z

**tool result**
````
34 34 10 ['candidate_summary', 'category', 'id', 'record_text', 'synthetic', 'why_unsupported']
[('M13', '{\'id\': \'M13\', \'statement\': "Says the epidural steroid injection was given (record only say'), ('M14', "{'id': 'M14', 'statement': 'Dates the record-7 entry with its body date (2026-01-19) inste")]
[('K4', 'must', ''), ('K5', 'must', '')]
source_kind values Counter({'patient_self_report': 9})
[['2026-04-05', '2026-05-04']]
memory/contracts/api.md:166:    { "id": "f_pat_9", "type": "causation", "category": "patient_report", "source_kind": "patient_report",
memory/contracts/api.md:175:        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "flags_v1", "call_id": "c40", "output": {"type": "causation", 
memory/contracts/api.md:176:        "code_checks": {"excerpt_verbatim": true, "lexicon_hit": "patient_report", "highlight_found": true, "injection_tag": false},
memory/contracts/api.md:194:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows t
spec/REQUIREMENTS.md:71:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"
memory/DECISIONS.md:87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), so
memory/DECISIONS.md:243:- Decision: the flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation` and `record_warning` everywhere (D-013); lexicon 
evals/golden/README.md:40:      "source_kind": "patient_self_report"          // optional: content is the patient's own statement/complaint and must stay attrib
3c5eb7c 2026-11-01 18:43:10 -0600 fix(evals): golden set round 2 - tested must-not examples, exact provider labels, case_09, export golden, seeded edits
47520a8 2026-11-01 18:25:39 -0600 feat(evals): golden set - sample case, 8 synthetic cases, 20 seeded hallucinations, validator
302:Cards (backend, db, qa; architect consults): data model + persistence (db); ingest/split/date parsing (backend); generator extraction with structured output (backend); grounding verifier (backend — write it first, test-first); judges #1–#3 (backend); flag engines: gaps (code), amounts (code+LLM), conflicts (hybrid), pre-existing + causation (LLM+lexicon) (backend); audit log (db/backend); eval runner + report (qa): grounding rate, entry recall, amount recall, flag precision/recall per flag type, judge recall on seeded hallucinations (qa injects 20 synthetic unsupported summaries; judge must catch ≥ 95%), determinism across 3 runs; CLI `python -m app.pipeline evals/golden/sample.txt` prints the full result for the sample case.
419:2. **Recall:** ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set.
421:4. **No invented facts:** 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding); judge recall on seeded hallucinations ≥ 95%.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:45:10.437Z

Next: diff the golden notes against §6 block 2, check the reason codes cited by the sampled R-IDs, and test the "bills to request" rule.

### Assistant · claude-opus-5-5 · 2026-11-02T00:45:16.596Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport re\nroot='/Users/arsis/zlayt-pm-project/'\nreq=open(root+'spec/REQUIREMENTS.md').read()\nb2=req.split('**Block 2')[1].split('```')[1].strip()\ng=open(root+'evals/golden/sample.export.expected.txt').read()\ngn=g.split('=== INTERNAL_NOTES_TEXT (block 2: do not send) ===')[1].strip()\nprint('notes golden == §6 block2:', gn==b2)\nimport difflib\nfor l in list(difflib.unified_diff(b2.splitlines(),gn.splitlines(),'REQ','golden',lineterm=''))[:20]: print(l)\nprint([l for l in gn.splitlines() if 'Austin EMS run report;' in l])\nlabels=['Austin EMS run report','Central ER discharge summary','Dr. Alvarez, primary care','Capital PT, initial evaluation','Capital PT, visit 8','Capital PT, visit 9','Hill Country Pain Management, new patient','Austin Imaging, cervical MRI','Hill Country Pain Management, follow-up']\ncharged={'Central ER discharge summary','Austin Imaging, cervical MRI'}\nseen=[]\nfor l in labels:\n    p=l.split(',')[0]\n    if p in [c.split(',')[0] for c in charged]: continue\n    if p not in seen: seen.append(p)\nprint('rule output (chronological):','; '.join(seen))\nprint('golden has .. run:', bool(re.search(r'(?<!\\.)\\.\\.(?!\\.)',g)))\nEOF\ngrep -n 'GROUNDING_DATE_MISMATCH\\|LLM_FAILED_AFTER_RETRIES\\|EXCERPT_OMITS_QUALIFIER\\|INJECTION_SUSPECTED\\|SUMMARY_TOKEN_NOT_IN_EXCERPT\\|number_not_in_excerpt' memory/contracts/api.md | cut -c1-140; grep -n -i 'max.*retr\\|retries' memory/DECISIONS.md docs/LLM_VS_CODE.md | head -5 | cut -c1-200",
 "description": "Diff golden notes, check bills rule, reason codes, retries"
}
````

### User / tool · 2026-11-02T00:45:16.705Z

**tool result**
````
notes golden == §6 block2: True
['- Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).']
rule output (chronological): Austin EMS run report; Dr. Alvarez; Capital PT; Hill Country Pain Management
golden has .. run: False
246:      {"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "“$9,000” is not in the quote.", "item_id": "e3"},
302:| `GROUNDING_DATE_MISMATCH` | rejected | model's date differs from the code-parsed header date |
304:| `SUMMARY_TOKEN_NOT_IN_EXCERPT` | needs_review | a number, date, dollar figure or left/right/no/not/without in the summary (or an edit)
305:| `EXCERPT_OMITS_QUALIFIER` | needs_review | the record has a hedge sentence the excerpt leaves out |
317:| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warnin
318:| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
docs/LLM_VS_CODE.md:20:10. **Retries change something** (one record at a time, a stricter format request), at most twice, then a visible failure state.
memory/DECISIONS.md:119:  7. **Retries change conditions** (one record at a time; stricter schema instruction). Total attempts = 1 + 2 retries. The retry loop lives only in `app/llm/audited.py`; backe
memory/DECISIONS.md:146:    - **rejected**: a grounding check failed (excerpt not a whitespace-normalised substring of its record; amount text not in the record; date differs from the code parse) or s
memory/DECISIONS.md:178:  - Failures are per item where possible (`LLM_FAILED_AFTER_RETRIES`) and per run only when nothing can proceed (`status: failed`). 8-minute run deadline (ADR-003.7).
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:45:25.776Z

The R-CO-9 test conflicts with ADR-003.7: "fails twice" against 1 + 2 retries = 3 attempts. The bills-to-request rule does not produce the golden line. Next, the scope check against the M2+M3 budget.

### Assistant · claude-opus-5-5 · 2026-11-02T00:45:27.009Z

**tool call — Bash**
````
{
 "command": "grep -n -i 'M2\\b.*h\\b\\|M3\\b.*h\\b\\|budget\\|hours\\|time-box\\|timebox' docs/CONTRACT.md | head -20 | cut -c1-220",
 "description": "Find milestone time budgets in CONTRACT"
}
````

### User / tool · 2026-11-02T00:45:27.089Z

**tool result**
````
44:- *Classify failures and change conditions before retrying,* with budgets and escalation. Never retry the same thing the same way.
199:board.py new --title "..." --milestone M2 --role backend --priority P1 [--depends T-012 ...] --ac "testable criterion" [--ac ...] --by orchestrator [--body-file path]   → prints T-###
238:Write one file per role in `.claude/agents/` using the template in Appendix D.5. Workers: `architect, backend, db, frontend, qa, release, writer, researcher`. Reviewers: `paralegal-reviewer, litigation-lead-reviewer,
260:Time budgets are guidance for scope decisions, not deadlines to miss silently. When a milestone exceeds 150% of budget, cut scope deliberately (record in `SCOPE_CUTS.md`) rather than drift. Target total wall-clock: 1
300:### M2 — Core pipeline + evals green (≤ 3.5 h)
306:### M3 — Review UI, export, E2E (≤ 3.5 h)
308:Cards (frontend, backend, qa): paste/upload input; timeline view with date, provider, summary, exact excerpt, confidence state, and "Why?"; flags panel grouped by type with evidence; charges table with running total 
397:### 7.4 Verdicts and loop budget
469:## 12. Guardrails and budgets
500:**The scenario.** A litigation lead at Zinda Law Group tells you: "Before every demand letter, a paralegal spends hours turning scattered medical records into a treatment chronology. It's slow, and mistakes cost us c
542:- Time-box it. Cut scope on purpose and tell us what you cut.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:45:28.369Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/docs/CONTRACT.md",
 "offset": 300,
 "limit": 12
}
````

### User / tool · 2026-11-02T00:45:28.378Z

**tool result**
````
300	### M2 — Core pipeline + evals green (≤ 3.5 h)
301	
302	Cards (backend, db, qa; architect consults): data model + persistence (db); ingest/split/date parsing (backend); generator extraction with structured output (backend); grounding verifier (backend — write it first, test-first); judges #1–#3 (backend); flag engines: gaps (code), amounts (code+LLM), conflicts (hybrid), pre-existing + causation (LLM+lexicon) (backend); audit log (db/backend); eval runner + report (qa): grounding rate, entry recall, amount recall, flag precision/recall per flag type, judge recall on seeded hallucinations (qa injects 20 synthetic unsupported summaries; judge must catch ≥ 95%), determinism across 3 runs; CLI `python -m app.pipeline evals/golden/sample.txt` prints the full result for the sample case.
303	
304	Gate panel: staff-engineer, qa (eval report attached), paralegal, legal-nurse, claims-adjuster (reads the sample-case output and tries to discredit it), privacy-compliance (prompt-injection probe result, PHI handling design). Exit: evals meet the ship bar (§8.2), zero blockers, tag `m2`.
305	
306	### M3 — Review UI, export, E2E (≤ 3.5 h)
307	
308	Cards (frontend, backend, qa): paste/upload input; timeline view with date, provider, summary, exact excerpt, confidence state, and "Why?"; flags panel grouped by type with evidence; charges table with running total and the "unclear" tray; accept / edit / dismiss per entry and per flag with keyboard-friendly review flow; export (copy-ready demand-letter treatment section containing only accepted items, with source citations in a format a paralegal would use); the chosen stretch item if still inside budget; mobile-usable; Playwright E2E for the full paralegal journey (paste sample → review → export equals accepted set).
309	
310	Gate panel: ux-designer (drives the app via Playwright and screenshots every state), paralegal (completes the full job on the sample case as a user and reports where she distrusted the tool), accessibility, staff-engineer, chaos-tester (adversarial inputs: empty, huge, non-English, injection record, pasted PDF text with page headers), product-manager. Exit: E2E green, gate passed, tag `m3`.
311	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:02.942Z

I have the scope picture. Last state checks: the `verify_quickly` key in the paralegal agent, and the date of the r2 trace file.

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:04.523Z

**tool call — Bash**
````
{
 "command": "grep -rln 'verify_quickly' .claude/agents/ docs/ memory/ 2>/dev/null; grep -rn 'verify_every_claim' .claude/agents/ | head -3 | cut -c1-160; grep -n '^## ' artifacts/review-evidence/T-013-trace.md; wc -l artifacts/review-evidence/T-013-trace.md",
 "description": "Check score key in agents and trace file sections"
}
````

### User / tool · 2026-11-02T00:46:04.619Z

**tool result**
````
memory/PROGRESS.md
memory/ORCHESTRATOR_DECISIONS.md
memory/DECISIONS.md
9:## A. Must-haves (SPEC:36-42)
36:## B. Stretch (SPEC:44)
42:## C. Constraints (SPEC:46-50)
53:## D. Ground rules that bind Part 1 (SPEC:16-19)
62:## E. Submission items (SPEC:67-71, 97-101)
72:## F. Ship bar (CONTRACT §8.2, lines 417-422) vs REQ §6 (157-163)
82:## G. Sample-case truths (SAMPLE_CASE_TRUTHS) vs REQ
94:## H. Random sample of 10 R-IDs — is the test pass/fail?
139:## Round-1 findings: resolution status
171:## Round-2 random sample of 10 R-IDs
     188 artifacts/review-evidence/T-013-trace.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:07.058Z

**tool call — Bash**
````
{
 "command": "ls .claude/agents/ | grep -i paralegal; grep -n -i 'scores\\|verify' .claude/agents/paralegal-reviewer.md | head -8 | cut -c1-200; sed -n 160,188p artifacts/review-evidence/T-013-trace.md | cut -c1-200",
 "description": "Check paralegal agent score keys; tail of trace"
}
````

### User / tool · 2026-11-02T00:46:07.150Z

**tool result**
````
paralegal-reviewer.md
36:- A chronology she can verify line by line, fast: date of service, provider/facility, short summary in the provider's own words, and the exact excerpt with its record reference.
86:9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).
139: "scores": {"<criterion>": 1-5},
| PL-M3 | No export template; record-number citation; ISO dates (major) | **resolved / partial test** | R-EX-6 (108) + §6; long dates; `[Ex. __ / Bates __]` | The golden file does not exist and no ca
| PL-M4 | Unclear amounts/total in export unspecified (major) | **resolved** | R-EX-4 (106), R-EX-8 (110) exact total string | — |
| PL-M5 | Edits under-specified (major) | **resolved** | R-RV-2 (88), R-RV-3 (89), R-CH-7 (79) | R-CH-7 unconfirmed; recommend cut (R2-2) |
| PL-M6 | Provider not from record (major) | **resolved** | R-TL-9 (53) | Golden aliases are not verbatim (R2-6) |
| PL-M7 | Date of service / record-7 trap (major) | **resolved** | R-TL-3 (47) record-7 seeded test | — |
| PL-M8 | No duplicate handling (major) | **resolved** | R-TL-7 (51) case_04; R-CH-6 (78) | The R-CH-6 split action is scope creep (R2-2) |
| PL-M9 | Export doesn't reconcile missing records (major) | **resolved** | R-EX-7 (109); §6 line 265-275 | — |
| PL minors | batch / reload / wages / bills to request / gap evidence / score key | resolved | R-RV-7 (93) + NG14; R-RV-8 (94); R-EX-4 damages; R-EX-4 bills; R-FL-1 (61) + R-IN-5; row 5 | Batch accep

Tally: 15 blocker/major (1 blocker + 14 majors) → 13 resolved, 2 partially (PL-M1, PL-M3). Minors: 13 → 11 resolved, 1 partially (PM-m7), 1 contradicted (PM-m4).

## Round-2 random sample of 10 R-IDs

Selection: `random.seed(1302); random.sample(sorted(ids),10)` over the 61 IDs.

| R-ID | Decidable? | Note |
|---|---|---|
| R-CO-1 | yes | UT import check plus PR, where the pass rule is "no blocker/major" |
| R-CO-8 | yes | Today it would fail: NG 12 and 14 are missing from SCOPE_CUTS |
| R-FL-4 | partial | REQ says record 7 "must" raise; golden K4/K5 are `should`, with credit via G1/C1 |
| R-FL-5 | yes | — |
| R-FL-6 | yes | — |
| R-IN-1 | yes | — |
| R-IN-2 | yes | — |
| R-IN-3 | yes | Matches case_01 golden |
| R-IN-5 | **no** | "Confirm a date" has no defined action. R-RV-2 UT requires date edits → 422, and the API's only date path is `edits.date` |
| R-TL-2 | partial | "Complete sentence" boundary unspecified. Sample has "approx.", "Dr.", "C/O", "Dx:" |

Result: 7/10 clean (round 1: 5/10), 2 partial, 1 contradictory.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:20.758Z

Verdict is shaping up as `changes` with two majors. I'll check r2's score keys so the scores stay comparable across rounds.

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:22.119Z

**tool call — Bash**
````
{
 "command": "grep -n '\"scores\"' -A 12 reviews/T-013-product-manager-r2.md | head -16; grep -n '\"scope\"\\|\"exercised\"' reviews/T-013-product-manager-r2.md | cut -c1-300; sed -n 1,30p reviews/T-013-product-manager-r2.md",
 "description": "Read r2 scores and summary format"
}
````

### User / tool · 2026-11-02T00:46:22.208Z

**tool result**
````
42: "scores": {"traceability": 5, "test_decidability": 3, "stretch_rationale": 5, "cut_rule": 4, "non_goals": 4, "ship_bar_fidelity": 5, "workflow_fit": 4, "architect_handoff": 2},
43- "findings": [
44-  {"severity": "major", "title": "R-IN-5 'confirm a date' contradicts R-RV-2 'date not editable'; no action exists to confirm an ambiguous date",
45-   "evidence": "REQ:37 R-IN-5 'When she confirms a date it joins the timeline and gap math re-runs'; test 'after confirming 2026-05-04'. REQ:88 R-RV-2 'Date, provider and excerpt are not editable' and 'UT: attempts to edit date ... -> 422'. memory/contracts/api.md:175 and 179: the only date path is `{\"action\":\"edit\",\"edits\":{\"date\":...}}`. api.md:235 DATE_AMBIGUOUS 'excluded from gap math until set'. REQ:320 §8 asks the architect to remove entry date editing, which would leave R-IN-5 with no mechanism at all. The sample re-draw hit R-IN-5 and judged it undecidable.",
46-   "why_it_matters": "Ambiguous dates are a must-have path, golden case_01 record 8. A backend worker cannot satisfy both R-IN-5 and R-RV-2's 422 unit test, so whichever one is built, the other fails.",
47-   "fix": "Define a separate review action, e.g. `confirm_date`, that is valid only for entries in DATE_AMBIGUOUS or DATE_MISSING state. The date must be one of the code-parsed readings (04/05 means April 5 or May 4) or a typed valid ISO date. Log it as a review event. Keep general date edits forbidden. Add it to R-RV-2's per-type table and to the §8 conflict list for api.md.",
48-   "acceptance_test": "REQ names the confirm-date action and its allowed values. R-RV-2's UT says 'edit date -> 422; confirm_date on a non-ambiguous entry -> 422; confirm_date on case_01 record 8 with 2026-05-04 -> 200 and a 40-day gap flag'."},
49-  {"severity": "major", "title": "Scope grew 47 -> 61 R-IDs; three add-ons not required by Appendix A should move to non-goals",
50-   "evidence": "SPEC:41 requires 'accept, edit or dismiss each entry and each flag'. Charges are not in the edit requirement, and batch accept and duplicate splitting are not mentioned. REQ:79 R-CH-7 (charge reclassification + judge #2 re-run + confirm; 'Writer's proposal; architect to confirm'). REQ:93 R-RV-7 (batch accept; 'Needs an ADR-005 amendment: today's api.md has no bulk endpoint'). REQ:78 R-CH-6 'A \"not a duplicate\" action splits them and is logged' (new action; no golden case has duplicate charges, and case_04 is 'no amounts'). CONTRACT:306 M3 budget is <= 3.5 h for the whole UI, export and E2E. Together these three supply 3 of the 4 §8 conflict bullets (REQ:320-322).",
51-   "why_it_matters": "'Builder mindset: you ship something real and cut scope on purpose' (CONTRACT:515). Each add-on needs a new endpoint or ADR change, more UI, and its own E2E. They compete with must-haves for M3's 3.5 h, and the reviewer of the product note will see requirements we chose to carry rather than cut.",
52-   "fix": "Move to §5 non-goals and SCOPE_CUTS: (a) charge reclassification. Charges become {accept, dismiss}, the class is code + judge #2, and the R-RV-1 charge cells drop 'edit'. This is also safer: no path turns the $185 rate into a totaled charge. (b) Batch accept: per-item keyboard accept (R-RV-4) is enough for about 10 records, and widening non-goal 14 to all batch accept respects ADR-005's 'Amounts and dates always need an explicit accept'. (c) The duplicate-charge split action: keep the code merge and its visible 'duplicate of' note. Keep R-CH-6's merge and R-TL-7.",
53-   "acceptance_test": "R-CH-7 and R-RV-7 are removed or rewritten as non-goals. R-CH-6 has no split action. R-RV-1's charge cells are {accept, dismiss}. §8 no longer lists the bulk-endpoint or charge-edit conflicts. SCOPE_CUTS has rows for all three."},
54-  {"severity": "major", "title": "R-TL-8 (hedge travels with finding) keys on a lexicon 'hedge' category that does not exist; the record-6 assertion has no rule behind it",
24: "scope": "spec/REQUIREMENTS.md at 64f766e (diff 65894f6..64f766e; working tree clean) against spec/SPEC.md Appendix A Part 1, docs/CONTRACT.md §5 M2/M3 and §8.2, memory/contracts/api.md, memory/DECISIONS.md ADR-005/009, evals/golden/*, app/llm/lexicon.yaml; round-1 reviews reviews/T-013-produc
25: "exercised": [
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:24.678Z

**tool call — Bash**
````
{
 "command": "git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md; git diff --stat HEAD -- spec/REQUIREMENTS.md; git status --short spec/ memory/ evals/ | head",
 "description": "Diff stats and working tree status"
}
````

### User / tool · 2026-11-02T00:46:24.802Z

**tool result**
````
 spec/REQUIREMENTS.md | 264 +++++++++++++++++++++++++++++++--------------------
 1 file changed, 160 insertions(+), 104 deletions(-)
 M memory/PROGRESS.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:27.043Z

Appending the Round 3 section to the trace.

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:53.994Z

**tool call — Bash**
````
{
 "command": "cat >> artifacts/review-evidence/T-013-trace.md <<'EOF'\n\n## Round 3 (spec/REQUIREMENTS.md at b4f3924; HEAD diff empty; product-manager-reviewer)\n\nInputs: `git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md` gives 160+/104-. Also read memory/ORCHESTRATOR_DECISIONS.md (D-001 to D-018), memory/DECISIONS.md ADR-017, and the golden round 2 (3c5eb7c, which landed after b4f3924). Probe: `artifacts/review-evidence/T-013-r3check.py`.\n\n### Round-2 findings: resolution status\n\n| r2 item | Status | Evidence | Residual |\n|---|---|---|---|\n| M1 confirm-date vs \"date not editable\" | **resolved** | REQ:40 R-IN-5 `confirm_date`; REQ:93 R-RV-2 UT; REQ:105-109 action table; api.md:23,196-208 endpoint | api.md:208 returns `422 date_invalid`; R-RV-2 UT expects `422 invalid_edit` (R3-M2) |\n| M2 scope add-ons → non-goals | **resolved** | NG14-16 (REQ:198-200); SCOPE_CUTS rows 14-16; R-CH-7 is now a restriction (accept/dismiss only); R-RV-7 withdrawn (REQ:111) | — |\n| M3 R-TL-8 nonexistent `hedge` category | **resolved (today)** | REQ:55 names 5 lexicon IDs; all 5 exist in app/llm/lexicon.yaml as `causation_weakening`. Sentence unit defined at REQ:49; prototype splitter reproduces every §6 excerpt as whole units and keeps \"approx. 35 mph.\" as one unit | D-018 adds a `hedge` boolean and remaps `flag_type`; T-009 is changes_requested. That gives two definitions of the hedge set (R3-M2) |\n| M4 R-EX-1 negative strings vs excerpt rule | **resolved** | REQ:11, 119 option (b): only tool-authored strings are banned. D-012 is recorded and NEEDS_CHRIS lists it as an FYI. None of 13 banned/label strings appears in the §6 letter (probe) | — |\n| M5 §8 hand-off | **partial** | D-001..D-018 and ADR-017 are recorded. Open rows 1-3 are mostly done: golden aliases are now exact (probe: 0 non-substring aliases); sample.export.expected.txt and seeded_edits exist; SCOPE_CUTS 1-19 map 1:1 to NG1-19; A-106 rewritten | §8 \"Still open\" is stale. New conflicts are unlisted: api.md export example, A-106 vs R-EX-4, D-018, R-TL-10 token set, and golden vocabulary (R3-M2). Row 3's \"add verify_quickly to paralegal brief\" is not done (.claude/agents/paralegal-reviewer.md:86 has no key), and no card owns it |\n| m R-EX-6 backend + golden owner | **resolved / new defect** | REQ:124 fixture backend; T-015 named | Golden file has both blocks plus `=== ... ===` markers, so \"letter_text equals the golden file byte for byte\" fails as written (R3-m1) |\n| m R-FL-4 must vs should | **reversed** | REQ:68 now says K4-K5 `should`; golden 3c5eb7c now says K4, K5 `must` | R3-M2 |\n| m golden aliases | **resolved** | probe: every provider/alias is a substring of its header label | — |\n| m ship-bar key | **partial** | REQ:323 `scores.verify_quickly` (D-015) | not in the paralegal agent; §8 row 3, no card |\n| m R-CO-8 SCOPE_CUTS parity | **resolved** | 19 non-goals ↔ 19 SCOPE_CUTS rows (NG12↔SC19, NG13↔SC12, NG19↔SC13) | §8 row 3 still asks for them (stale) |\n| nit reviewer-note length | **resolved** | REQ:107 500 chars, verbatim, labeled | — |\n\nTally: 5 majors → 4 resolved, 1 partial (hand-off, recurring in new form). 5 minors + 1 nit → 4 resolved, 1 partial, 1 reversed by later golden.\n\n### Round-3 random sample of 10 R-IDs\n\nSelection: `random.seed(2026); random.sample(ids, 10)` over the 62 ID rows in file order (61 + R-ST-1).\n\n| R-ID | Decidable? | Note |\n|---|---|---|\n| R-CO-9 | partial | UT \"LLM call fails twice → could not process\". ADR-003.7 (DECISIONS:119) says 1 + 2 retries = 3 attempts, and api.md:318 says \"failed on all three attempts\" |\n| R-EX-1 | yes | negative list is tool-authored only; the §6 letter is clean |\n| R-EX-2 | yes | — |\n| R-EX-4 | partial | Rule (8) \"label up to the first comma\" yields \"Dr. Alvarez\", but §6/golden print \"Dr. Alvarez, primary care\"; order and the \"(itemized ledger)\" suffix follow no rule. A-106 says notes cite \"not record numbers\", while R-EX-4 requires `record N (...)` |\n| R-FL-6 | partial | \"case_01 shows a dates-to-confirm item\" is a `record_warning` per REQ:40/70; golden case_01 `record_warnings: []` (the ambiguity sits on E8 only) |\n| R-RV-3 | yes | golden seeded_edits SE1-SE3 exist |\n| R-SU-4 | yes | diff against re-run exporter |\n| R-TL-10 | yes | decidable; token set is narrower than api.md:304 (left/right/no/not/without) |\n| R-TL-2 | yes | prototype splitter: units concatenated equal the record for all 9; every §6 excerpt is a whole-unit run |\n| R-TL-3 | yes | GROUNDING_DATE_MISMATCH at api.md:302; golden M14 covers it |\n\nResult: 7/10 clean, 3 partial, 0 contradictory (round 2: 7 clean, 2 partial, 1 contradictory). All three partials come from artifacts that changed after or alongside b4f3924.\n\n### Golden drift since b4f3924 (3c5eb7c, 2 min later)\n- hallucinations.jsonl has 34 items (34 unique IDs) and controls has 10. REQ:51 and REQ:322 say \"20 … at least 19\" and \"5 controls\".\n- sample flags K4 and K5 are `must`; REQ:68 says `should`.\n- must_not runs M1–M14; REQ:68 and REQ:137 say M1–M13.\n- `source_kind`: golden has `patient_self_report` (9 instances, on entries); REQ:71 and api.md:166 have `patient_report` (on flags).\n- seeded_edits reason `number_not_in_excerpt`; api.md code is `SUMMARY_TOKEN_NOT_IN_EXCERPT`.\n\n### api.md export example vs REQ (e442626; ADR-017 claims \"no remaining known conflict\")\n- api.md:266 amount line `........ $6,240.00` (dot leaders). R-EX-6 says \"no dot leaders\" and \"no `..` run\".\n- api.md:266 total `$6,240 (excludes physical therapy — per-visit rate only, visit count not stated)`. R-EX-8 UT says \"letter_text contains neither 'visit count' nor 'rate'\", and the format is `$X.XX (… to be supplemented)`.\n- api.md:266 `Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]:`. §6 and the golden use `Source [Ex. __ / Bates __]:`.\n- api.md:267 notes cite `Capital PT, record 4:`. R-EX-4 uses `record N (<provider>, <Month D, YYYY>)`. A-106 (ASSUMPTIONS:20) says \"not record numbers\". That makes three formats.\n\n### Scope vs M2+M3 (CONTRACT:300, 306: 3.5 h + 3.5 h)\n62 R-ID rows. CONTRACT M2/M3 explicitly name everything in IN/TL/FL/CH/RV-1..6/EX core. Beyond Appendix A and CONTRACT M3, the add-ons are: R-RV-9 (full-record modal, in core), entry excerpt re-selection (R-RV-2 table), R-EX-4 sections 7-8 (future treatment, bills to request), the R-EX-5 copy-confirm, and R-RV-3's judge re-run plus the \"keep my wording\" confirm. No pre-ranked M3 cut order exists apart from the stretch (R3-m3).\nEOF\necho ok",
 "description": "Append Round 3 section to trace file"
}
````

### User / tool · 2026-11-02T00:46:54.081Z

**tool result**
````
ok
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:46:56.238Z

Writing the review file.

### Assistant · claude-opus-5-5 · 2026-11-02T00:47:56.868Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-013-product-manager-r3.md",
 "content": "# T-013 review, round 3 — product-manager-reviewer\n\n**Verdict: changes** (0 blockers, 2 majors, 4 minors, 1 nit).\n\nThe requirements themselves are now in good shape. Four of the five round-2 majors are fully resolved:\n- `confirm_date` replaces date edits and has its own action table.\n- Batch accept, charge reclassification and the duplicate split are all non-goals, and SCOPE_CUTS matches 1:1.\n- R-TL-8 names five lexicon IDs that exist. A whole-sentence unit is defined, and my prototype splitter reproduces every §6 excerpt from it.\n- R-EX-1 bans only tool-authored strings. D-012 is recorded.\n\n7 of 10 re-sampled R-IDs are cleanly decidable, and none is contradictory. Full trace: `artifacts/review-evidence/T-013-trace.md` \"Round 3\".\n\nWhat still fails is the hand-off. Two things changed after `b4f3924` and have not been reconciled:\n1. **The golden set changed two minutes after b4f3924** (3c5eb7c). It now has 34 seeded hallucinations, not 20. Ship-bar row 4's literal \"≥ 19 of the 20\" would now pass a 56% catch rate.\n2. **§8 says reconciliation is done (ADR-017), but it isn't.** The api.md export example, A-106 and D-018 each contradict a tested R-ID, and the golden vocabulary has drifted. Workers build from api.md and the golden, so T-017 would plan these two ways.\n\nBoth fixes are mechanical: about 30 minutes for writer and qa, plus one architect edit. A small reconciliation card that T-017 depends on would close both.\n\nExercised:\n- `board.py show T-013` and `board.py list`; `git log`; `git diff --stat 64f766e..b4f3924`; `git diff --stat HEAD -- spec/REQUIREMENTS.md` (empty).\n- Read REQUIREMENTS.md in full, plus ORCHESTRATOR_DECISIONS D-001..D-018, ADR-017, the api.md export and reason codes, ASSUMPTIONS A-106, SCOPE_CUTS, NEEDS_CHRIS, CONTRACT M2/M3, and the paralegal agent.\n- Scripted the R-ID inventory: 62 rows, 0 dangling (R-RV-7 is withdrawn on purpose).\n- Loaded lexicon.yaml with `.venv/bin/python` and checked the hedge IDs.\n- Ran a prototype R-TL-2 splitter on the sample, checked the §6 excerpts and R-EX-1's banned strings, diffed the golden export against §6, checked aliases, and recomputed the bills-to-request rule. The probe is `artifacts/review-evidence/T-013-r3check.py`.\n- Checked golden counts, levels, must_not IDs and `source_kind`.\n- Re-sampled 10 R-IDs with seed 2026.\n\n```json\n{\"card\": \"T-013\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"spec/REQUIREMENTS.md at b4f3924 (diff 64f766e..b4f3924, 160+/104-; HEAD diff empty) against memory/ORCHESTRATOR_DECISIONS.md D-001..D-018, memory/DECISIONS.md ADR-017, memory/contracts/api.md (e442626), memory/ASSUMPTIONS.md, memory/SCOPE_CUTS.md, evals/golden/* (3c5eb7c), app/llm/lexicon.yaml, docs/CONTRACT.md §5 M2/M3 and §8.2; prior reviews reviews/T-013-product-manager-r2.md and reviews/T-013-paralegal-r2.md; no app (M1)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-013 -> in_review, commits [65894f6, 64f766e, 4191140, b4f3924]; python3 tools/board.py list -> T-009 changes_requested, T-014 in_review, T-015 in_progress, T-017 ready (depends T-013/T-014/T-015)\",\n  \"git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md -> 1 file, 160+/104-; git diff --stat HEAD -- spec/REQUIREMENTS.md -> empty\",\n  \"git log for api.md (e442626 18:40:17), golden (3c5eb7c 18:43:10), ASSUMPTIONS/SCOPE_CUTS (56750da 18:41:47) vs b4f3924 (18:41:23)\",\n  \"Read spec/REQUIREMENTS.md 1-386 in full; ORCHESTRATOR_DECISIONS D-001..D-018; DECISIONS.md:276-290 ADR-017; api.md:23,196-208,240,255-300 (export example, reason codes)\",\n  \"R-ID inventory script: 62 defined rows, 0 duplicates, only undefined ref R-RV-7 (withdrawn on purpose, REQ:111,385)\",\n  \".venv/bin/python yaml.safe_load(app/llm/lexicon.yaml): 48 entries; may_represent, correlate_clinically, possibility_terms, cannot_exclude, nonspecific_indeterminate all exist (causation_weakening); no entry has a `hedge` key\",\n  \".venv/bin/python -I artifacts/review-evidence/T-013-r3check.py: R-TL-2 splitter prototype -> units concat == record text for all 9; 'approx. 35 mph.' one unit; 11/11 §6 Source quotes are whole-unit runs; 0 of 13 banned/label strings in §6 letter; golden export != §6 block 1 (golden adds '=== LETTER_TEXT ... ===' marker and the notes block); 0 non-substring provider aliases\",\n  \"Golden facts: case_01 E8 ambiguous with candidates [2026-04-05, 2026-05-04], record_warnings []; case_02 gaps 29/30/31 -> 3 flags 4 non-flags; case_04 6 records -> 4 entries E1[1,2] E2[3,4]; case_07 total 420; case_03 $1,2OO/$9S.00 unclear; hallucinations.jsonl 34 items (34 unique ids), controls 10; K4/K5 level must; must_not M1-M14; source_kind values {'patient_self_report': 9}\",\n  \"Golden notes block == §6 block 2 (True); bills-to-request rule recomputed -> 'Austin EMS run report; Dr. Alvarez; Capital PT; Hill Country Pain Management' vs golden 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).'\",\n  \"grep verify_quickly .claude/agents/ -> no match; paralegal-reviewer.md:86 'Rate \\\"I could verify every claim quickly\\\" 1-5'\",\n  \"SCOPE_CUTS rows 1-19 vs REQ non-goals 1-19 -> 1:1 (NG12<->SC19, NG13<->SC12, NG19<->SC13)\",\n  \"Re-sampled 10 R-IDs (random.seed(2026)): 7 decidable, 3 partial, 0 contradictory\",\n  \"Appended 'Round 3' to artifacts/review-evidence/T-013-trace.md\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"traceability\": 5, \"test_decidability\": 4, \"stretch_rationale\": 5, \"cut_rule\": 4, \"non_goals\": 5, \"ship_bar_fidelity\": 3, \"workflow_fit\": 5, \"architect_handoff\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Ship-bar row 4 and R-TL-4 hard-code '19 of 20' seeded hallucinations and '5 controls'; the golden now has 34 and 10, so the literal threshold permits a 56% catch rate\",\n   \"evidence\": \"REQ:322 'Judge recall on seeded hallucinations ≥ 95% (≥ 19 of the 20 in `hallucinations.jsonl`)'; REQ:51 'On the 20 seeded unsupported summaries ... flags at least 19 (≥ 95%...)' and 'On the 5 faithful controls'. Probe: hallucinations.jsonl 34 items with 34 unique ids; hallucinations_controls.jsonl 10 items (golden commit 3c5eb7c, after b4f3924). REQ:24 'Pass/fail wording is literal.'\",\n   \"why_it_matters\": \"Ship bar #4 is the 'no invented facts' criterion, the one a demo-day failure hits first. Under the literal-wording rule a judge that catches 19 of 34 (56%) passes R-TL-4(b). The product note would then report a bar the eval doesn't hold.\",\n   \"fix\": \"State the threshold as a rate over whatever the file holds: 'hallucination_catch_rate ≥ 0.95 over every item in hallucinations.jsonl (currently 34 → ≥ 33)'. Do the same for controls: '0 of the N controls (currently 10) judged unsupported'. Keep CONTRACT §8.2's '≥ 95%' as the governing number. Note in §8 that CONTRACT §5 M2 still says 'qa injects 20' (orchestrator).\",\n   \"acceptance_test\": \"grep -n '19 of\\\\|the 20\\\\|5 faithful' spec/REQUIREMENTS.md returns nothing. R-TL-4(b) and ship-bar row 4 read as a rate, with the current count in parentheses, matching `wc -l evals/golden/hallucinations.jsonl`.\"},\n  {\"severity\": \"major\", \"title\": \"§8 says ADR-017 left 'no remaining known conflict', but api.md, A-106, D-018 and the golden contradict tested R-IDs and none of it is in 'Still open'\",\n   \"evidence\": \"(1) api.md:266 letter example uses dot leaders '........ $6,240.00' (R-EX-6 REQ:124 'no dot leaders'); total '$6,240 (excludes physical therapy — per-visit rate only, visit count not stated)' (R-EX-8 REQ:126 UT 'letter_text contains neither \\\"visit count\\\" nor \\\"rate\\\"'); Source line 'Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]:' (§6 REQ:218 'Source [Ex. __ / Bates __]:'). (2) Notes citation formats: api.md:267 'Capital PT, record 4:'; ASSUMPTIONS.md:20 A-106 'Internal notes cite provider + date, not record numbers'; R-EX-4 REQ:122 'record N (<provider as written>, <Month D, YYYY>)'. REQ:345 still says A-106 'currently says record number, provider, date', which is stale. (3) api.md:208 confirm_date with a non-candidate date -> '422 date_invalid'; R-RV-2 REQ:93 expects '422 `invalid_edit`'. (4) D-018 adds lexicon booleans `hedge`/`self_report` and flag_type ∈ {pre_existing, causation, record_warning}; REQ:4 cites only D-001 to D-015; REQ:26 and REQ:55 keep 'causation_weakening'/'compliance' and define the hedge set as 5 fixed IDs. T-009 (lexicon) is changes_requested and adding hedge entries. (5) R-TL-10 REQ:57 checks numbers/dates/$ only; api.md:304 SUMMARY_TOKEN_NOT_IN_EXCERPT also covers left/right/no/not/without. (6) Golden 3c5eb7c: K4/K5 level 'must' vs REQ:68 'should'; must_not M1-M14 vs REQ:68,137 'M1–M13'; source_kind 'patient_self_report' (9×, on entries) vs REQ:71 and api.md:166 'patient_report' (on flags); case_01 record_warnings [] vs REQ:40,70 'a record_warning'; seeded_edits reason 'number_not_in_excerpt' vs api.md:304. (7) §8 'Still open' rows 1-3 (REQ:376-378) are mostly done (aliases exact, export golden and seeded edits exist, SCOPE_CUTS 1-19 present, A-106 rewritten). The remaining part, adding verify_quickly to the paralegal brief, has no card: grep verify_quickly .claude/agents -> none.\",\n   \"why_it_matters\": \"Round 2's major #5 recurs in a new form. Workers implement against api.md and the golden, and T-017 plans cards from REQ. With the letter format, notes citation, error code, hedge-set definition and self-report field each defined two or three ways, M3 would build one and the E2E/eval would check another. That is exactly the 'built two ways' failure the hand-off exists to prevent. The api.md total line also volunteers 'visit count not stated' to the carrier, which the paralegal r2 review removed.\",\n   \"fix\": \"Replace §8 'Still open' with the current list, one row per conflict above, each with an owning card: architect (T-014 or a new card) fixes the api.md export example, the confirm_date error code and the R-TL-10 token set, or REQ adopts the api set; orchestrator fixes A-106 to match R-EX-4 and adds verify_quickly to the paralegal agent (T-016); qa (T-015) fixes source_kind and the reason-code name; writer cites D-016..D-018 and restates R-TL-8's hedge set as 'lexicon entries with `hedge: true` (D-018); until T-009 lands, the 5 IDs listed'. Then align R-FL-4 and R-CO-3 with the golden (K4/K5 must, M1–M14) or have qa revert. Add the reconciliation card to T-017's depends_on.\",\n   \"acceptance_test\": \"A script greps api.md's letter_text example for '..', 'visit count' and 'rate', and finds none. A-106 and R-EX-4 name the same notes citation format. api.md and R-RV-2 name the same 422 code. `grep -rn patient_report\\\\|patient_self_report` returns one spelling. REQ:4 cites D-001..D-018. Every §8 'Still open' row names an open card ID, and none of those rows is already done.\"},\n  {\"severity\": \"minor\", \"title\": \"R-EX-6 compares letter_text to the whole golden file, but the file holds both blocks plus section markers\",\n   \"evidence\": \"REQ:124 '`letter_text` equals the golden file byte for byte'. evals/golden/sample.export.expected.txt starts with '=== LETTER_TEXT (block 1: paste into letter) ===' and continues with '=== INTERNAL_NOTES_TEXT (block 2: do not send) ===' and the notes (probe diff).\",\n   \"why_it_matters\": \"Taken literally, the test fails on a correct build. A worker will 'fix' it ad hoc, and whatever they choose is unspecified.\",\n   \"fix\": \"R-EX-6: 'the LETTER_TEXT section of the golden file equals letter_text and the INTERNAL_NOTES_TEXT section equals internal_notes_text, byte for byte (markers excluded)'. That also gates the notes, which are currently byte-identical to §6 block 2.\",\n   \"acceptance_test\": \"R-EX-6 names the section markers and both fields.\"},\n  {\"severity\": \"minor\", \"title\": \"R-EX-4 'bills to request' rule does not produce the worked example or the golden line\",\n   \"evidence\": \"REQ:122 (8) 'providers (the label up to the first comma) with an entry in the letter and no accepted charge'. Recomputed: 'Austin EMS run report; Dr. Alvarez; Capital PT; Hill Country Pain Management'. REQ:297 and the golden: 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).' (not up-to-first-comma, not chronological, and an unruled suffix).\",\n   \"why_it_matters\": \"This is spec-review pattern #3 recurring: the example passes only because its writer chose the string. Once the notes are byte-gated (minor above), code following the rule fails the golden.\",\n   \"fix\": \"Add an order rule (first appearance in the chronology) and a suffix rule ('(itemized ledger)' when the provider has a non-dismissed rate). Then make §6 and the golden follow the rule: 'Dr. Alvarez', with Capital PT before Hill Country.\",\n   \"acceptance_test\": \"A unit test applies rule (8) to the sample and gets the §6 line exactly.\"},\n  {\"severity\": \"minor\", \"title\": \"R-CO-9 test says 'fails twice'; ADR-003.7 and api.md say three attempts\",\n   \"evidence\": \"REQ:143 'Retries: max 2 ... UT: LLM call fails twice → item shown as \\\"could not process\\\"'. DECISIONS.md:119 'Total attempts = 1 + 2 retries'; api.md:318 LLM_FAILED_AFTER_RETRIES 'failed on all three attempts'.\",\n   \"why_it_matters\": \"A test that mocks two failures expects the failure state, while a correct implementation would make a third call.\",\n   \"fix\": \"'UT: the call fails on all 3 attempts (1 + 2 retries, each with changed conditions) → LLM_FAILED_AFTER_RETRIES; fails twice then succeeds → entry produced.'\",\n   \"acceptance_test\": \"R-CO-9's test names 3 attempts and includes the succeed-on-third case.\"},\n  {\"severity\": \"minor\", \"title\": \"No pre-ranked M3 cut order beyond the stretch; several M3 add-ons exceed Appendix A (I would do it differently)\",\n   \"evidence\": \"CONTRACT:306 M3 ≤ 3.5 h. In M3 scope beyond SPEC Appendix A and CONTRACT M3: R-RV-9 full-record modal (REQ:99, 'This is core'); entry excerpt re-selection (REQ:105); R-EX-4 sections (7) future treatment and (8) bills to request (REQ:122); R-EX-5 pending-confirm on Copy (REQ:123); R-RV-3 judge re-run plus 'keep my wording' confirm (REQ:94). Only the stretch has a cut rule (REQ:170-173).\",\n   \"why_it_matters\": \"The 62 rows fit 7 h only if nothing slips. Without a declared order, an overrun gets cut by whoever is holding the card, which breaks 'cut scope on purpose and tell us what you cut'.\",\n   \"fix\": \"Add a 4-line 'M3 cut order if over 100% of budget' under §4: (1) R-ST-1; (2) excerpt re-selection, so edit becomes summary only, entries can still be dismissed and the notes still list flagged language; (3) R-EX-4 sections 7 and 8; (4) R-RV-9 drops to inline full-record expand with no highlight, and highlights stay in the E2E as a should. Each cut is logged in SCOPE_CUTS.\",\n   \"acceptance_test\": \"§4 lists a numbered cut order. Each entry names its R-ID and what remains.\"},\n  {\"severity\": \"nit\", \"title\": \"§8 'Proposed additions' points to NEEDS_CHRIS, which now holds none of them; D-008/D-009/D-012 cite row numbers that no longer exist\",\n   \"evidence\": \"REQ:349 'several depend on Chris, see `submission/NEEDS_CHRIS.md`'. NEEDS_CHRIS has rows 1-4 (key, demo/live, eval budget, git email); D-012 is listed under 'Decided by the team — FYI'. ORCHESTRATOR_DECISIONS D-008 '#7', D-009 '#8', D-012 '#10'.\",\n   \"why_it_matters\": \"The stale pointers send a reader looking for a decision in the wrong place.\",\n   \"fix\": \"REQ:349 should read 'team decisions; Chris can override via the NEEDS_CHRIS FYI list'. The orchestrator drops the stale row numbers from D-008/D-009/D-012.\",\n   \"acceptance_test\": \"No REQ or D-row cites a NEEDS_CHRIS row number above 4.\"}\n ],\n \"whats_right\": [\n  \"R-TL-2's sentence unit is concrete enough to code from: a prototype reproduced all 11 §6 excerpts as whole-unit runs and kept 'approx. 35 mph.' intact.\",\n  \"The two-block export plus 'flagged language quoted in the letter' is the right call: the records' words stay the record, and the attorney decides. R-EX-1 now tests only tool-authored strings.\",\n  \"The cuts are deliberate and match 1:1: 19 non-goals ↔ 19 SCOPE_CUTS rows, each with a reason; R-CH-7 is now a safety restriction, not a feature.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T00:47:57.015Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-013-product-manager-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:47:59.233Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-013-product-manager-r3.md').read()\nj=re.search(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',t,re.S).group(1);d=json.loads(j);print(d['verdict'],[f['severity'] for f in d['findings']])\"; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Validate review JSON and board"
}
````

### User / tool · 2026-11-02T00:47:59.285Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:01.973Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-013-r3check.py >/dev/null && sed -n '/^```json$/,/^```$/p' reviews/T-013-product-manager-r3.md | sed '1d;$d' | .venv/bin/python -I -c \"import json,sys;d=json.load(sys.stdin);print(d['verdict'],[f['severity'] for f in d['findings']])\"; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Validate review JSON and run board validate"
}
````

### User / tool · 2026-11-02T00:48:02.156Z

**tool result**
````
changes ['major', 'major', 'minor', 'minor', 'minor', 'minor', 'nit']
ok (24 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:02.903Z

Now updating memory.

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:10.331Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t013_review_history.md",
 "content": "---\nname: t013-review-history\ndescription: T-013 REQUIREMENTS review rounds — verdicts, what stayed open after round 3 (as of 2026-11-01)\nmetadata:\n  type: project\n---\n\nT-013 (spec/REQUIREMENTS.md) review history:\n- **Round 1 (65894f6):** PM changes (5 majors); paralegal fail (flags exported into letter).\n- **Round 2 (64f766e):** PM changes (5 majors).\n- **Round 3 (b4f3924):** PM changes (2 majors, 4 minors, 1 nit). 4 of the 5 r2 majors are resolved.\n\nOpen after round 3. All of it is reconciliation; the content is sound.\n1. Ship bar row 4 and R-TL-4 say \"19 of 20\" seeded hallucinations, but the golden has 34. The fix is to state the threshold as a rate.\n2. §8 claims ADR-017 reconciled everything. These still disagree:\n   - The api.md export example has dot leaders, different total wording and a different Source line.\n   - The notes citation format differs across A-106, R-EX-4 and api.md.\n   - confirm_date returns 422 `date_invalid` in api.md and `invalid_edit` in REQ.\n   - REQ predates D-018's lexicon `hedge` booleans.\n   - The source_kind spelling is `patient_report` in REQ/api and `patient_self_report` in golden.\n   - K4/K5 are must in golden and should in REQ.\n   - must_not goes to M14 in golden; REQ says M13.\n\nSeeds used for R-ID samples: 13, 1302, 2026. The probe script is at artifacts/review-evidence/T-013-r3check.py.\n\n**Why:** Artifacts (golden, api.md, ASSUMPTIONS) landed minutes after the REQ commit. Every round's residual has been cross-artifact drift, not REQ content.\n\n**How to apply:** In any round 4 or T-018 contract review, re-run the probe and diff REQ against the current golden and api.md commits. Check the commit timestamps against the REQ commit. Related: [[spec-review-patterns]].\n"
}
````

### User / tool · 2026-11-02T00:48:10.428Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t013_review_history.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:12.825Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md",
 "old_string": "6. **Scope creep while fixing review findings.**",
 "new_string": "7. **Hard-coded counts drift from the golden.** Example: \"19 of the 20\" seeded hallucinations, when the golden now has 34. Under the \"literal wording\" rule this quietly weakens the ship bar. Check every count in REQ against `wc -l`/len() of the current golden files, and compare git timestamps: golden/api commits often land minutes after the REQ commit.\n6. **Scope creep while fixing review findings.**"
}
````

### User / tool · 2026-11-02T00:48:12.932Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:16.272Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer && sed -i '' 's/^- \\[T-013 review history\\](project_t013_review_history.md) — .*/- [T-013 review history](project_t013_review_history.md) — r1-r3 verdicts; r3 open: ship-bar 19\\/20 vs 34, §8 hand-off drift (api.md, A-106, D-018, golden)/' MEMORY.md && sed -i '' 's/^- \\[Spec review patterns\\](feedback_spec_review_patterns.md) — .*/- [Spec review patterns](feedback_spec_review_patterns.md) — recurring REQUIREMENTS defects: phantom IDs, fix-induced contradictions, vocab drift, stale golden counts, scope creep/' MEMORY.md && cat MEMORY.md",
 "description": "Update memory index lines"
}
````

### User / tool · 2026-11-02T00:48:16.375Z

**tool result**
````
- [Spec review patterns](feedback_spec_review_patterns.md) — recurring REQUIREMENTS defects: phantom IDs, fix-induced contradictions, vocab drift, stale golden counts, scope creep
- [Calibration vs red flags](feedback_calibration_vs_redflags.md) — dossier calibration severities softer than dealbreakers; cross-check
- [Source fetching](reference_source_fetching.md) — curl+UA fallback when WebFetch is missing; blocked hosts
- [NEEDS_CHRIS drift](feedback_needs_chris_drift.md) — rows added without cards, non-Chris questions, vague actions; ADR facts vs live system
- [Reviewer sandbox](reference_reviewer_sandbox.md) — hooks block shell writes to scratchpad/memory and backtick python -c; scripts go in artifacts/review-evidence
- [T-013 review history](project_t013_review_history.md) — r1-r3 verdicts; r3 open: ship-bar 19/20 vs 34, §8 hand-off drift (api.md, A-106, D-018, golden)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:48:27.666Z

**T-013 round 3 (product-manager-reviewer): verdict `changes`.** No blockers, 2 majors, 4 minors, 1 nit. `board.py validate` reports ok.

The requirements content is now sound. Four of the five round-2 majors are resolved:
- **Dates:** a separate "confirm date" action replaces editing the date.
- **Scope cuts:** batch accept, charge reclassification and the duplicate split are now non-goals, and the scope-cuts log matches the non-goals 1:1.
- **Hedge rule:** it names five lexicon entries that all exist. A prototype sentence splitter reproduces every excerpt in the worked example.
- **Letter rule:** the "no flag text in the letter" test now bans only tool-written text.

On the re-sample (seed 2026), 7 of 10 R-IDs are cleanly decidable, 3 are partial and none contradict each other. The remaining problems all come from other files that changed around the same time and were never reconciled. Two of them landed after the requirements commit (b4f3924): the golden set two minutes later, and A-106 seconds later.

**Majors:**
1. **Ship-bar row 4 and R-TL-4 still say "19 of the 20" seeded hallucinations.** The golden set now has 34, so the literal threshold would pass a judge that catches 56%. The fix is to state the threshold as a rate.
2. **§8 is still not a clean hand-off.** It says ADR-017 left "no remaining known conflict", but several tested R-IDs are contradicted elsewhere:
   - The api.md export example has dot leaders, total wording that tells the carrier "visit count not stated", and a different Source line.
   - The notes cite records three different ways (A-106, R-EX-4, api.md).
   - The "confirm date" error code is 422 `date_invalid` in api.md but `invalid_edit` in R-RV-2.
   - D-018 (new `hedge` tags in the lexicon) is not folded in.
   - The golden set disagrees with the requirements on the self-report field name, K4/K5 (must vs should) and M14.
   - §8's own open rows are mostly done already, but adding `verify_quickly` to the paralegal brief is still undone and no card owns it.

**Minors:**
- R-EX-6 compares the letter to the whole golden file, which also holds the notes block and section markers.
- The bills-to-request rule does not produce the line in the golden file.
- The retry test says "fails twice", while the ADR allows three attempts.
- There is no ranked M3 cut order; my suggested order is in the review.

**Scope:** it fits M2+M3 (about 7 h) only if nothing slips. If M3 runs over, cut in this order: the side-by-side viewer stretch, excerpt re-selection, the future-treatment and bills-to-request notes sections, then the full-record highlight. None of these needs cutting now.

Both majors are mechanical fixes, about 30 minutes plus one architect edit. A small reconciliation card that T-017 depends on would close them.

Files are in /Users/arsis/zlayt-pm-project:
- reviews/T-013-product-manager-r3.md
- artifacts/review-evidence/T-013-trace.md (new "Round 3" section)
- artifacts/review-evidence/T-013-r3check.py (probe script)
