# Subagent: T-015 round-3: paralegal + nurse (T-015 round-3: paralegal + nurse)

Source: `agent-abfb66eb0e29f0943.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:57:28.545Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — ROUND 3 (final, §7.4) of T-015 "Eval golden set" (M1). AC: `python3 tools/board.py show T-015`. R2 reviews: reviews/T-015-paralegal-r2.md (yours, fail) and reviews/T-015-legal-nurse-r2.md (changes). Change: commit f8c1948 (`git diff 3c5eb7c..f8c1948 -- evals/golden`). Binding: memory/ORCHESTRATOR_DECISIONS.md D-019, D-021, D-022.
Exercise hands-on: `python3 evals/golden/check_golden.py`; re-run your r2 probe (artifacts/review-evidence/T-015-r2-paralegal-probe.py) and the nurse's r2 probe (artifacts/review-evidence/T-015-r2-nurse-probe.py) against f8c1948 and record results; verify K4/K5 one-to-one matching with the reference matcher; compare sample.export.expected.txt to the 9 records (verbatim quotes, D-019 total line, flagged-language list incl. record 1, K5 line, bills-to-request rule); check required_terms are summary-only and self-report is per sentence.
Write reviews/T-015-paralegal-r3.md AND reviews/T-015-legal-nurse-r3.md (the second judged strictly against the nurse's r2 findings; persona "legal-nurse-reviewer"; scope notes the paralegal agent wrote it against the nurse checklist). D.2 JSON each. Do not fix anything. Reply ≤ 15 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:29.760Z

I'll start with memory and the brief's sources.

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:30.485Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/paralegal-reviewer/*.md; python3 tools/board.py show T-015; git log --oneline -5"
}
````

### User / tool · 2026-11-02T00:57:30.632Z

**tool result**
````
- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export golden vs JSON drift, regex probes
- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; use Edit + scripts in review-evidence
---
name: reviewer-tooling-quirks
description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
metadata:
  type: feedback
---

Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.

**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.

**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].
---
name: spec-review-patterns
description: Recurring defects found in Zlayt PM requirements/spec reviews (T-013 r1-r3) — rules/claims contradicted by the doc's own example, names that don't exist, unreconciled newer D-IDs
metadata:
  type: feedback
---

Before grading a requirements doc, mechanically check (1) every absolute claim against the doc's OWN worked example, and (2) every named artifact it keys on (lexicon category, R-ID, golden file, reason code) actually exists.

**Why:** T-013 r2: R-EX-1 said "No flag text of any kind" in the letter, yet 8 of 10 golden flag evidence strings sat verbatim in its §6 letter example; its test only listed strings that happened to pass. R-TL-8 keyed on a lexicon `hedge` category that doesn't exist (lexicon flag_types are pre_existing/causation_weakening/compliance). r1 had R-TL-4 citing a nonexistent R-QA-2. Writers fix the reviewer's wording and leave the test narrower than the claim.

T-013 r3 (b4f3924) showed the same pattern again. The R-EX-4(4) rule computed records {1,4,6,7,8,9}, but the example, the test and the golden file said {4,6,7,8,9}. Two more checks would have caught issues sooner:
- Check the doc's header list of binding decisions against the latest D-ID. It cited D-001..D-015, while D-016..D-018 existed and D-017 went unreconciled.
- Run my OWN previous acceptance tests literally. The r2 money regex fails on verbatim "$6,240." quotes.

Golden export files are copied from the spec example, so any contradiction in the example gets frozen into the golden file.

**How to apply:** Implement each stated rule in the walk script and compare its output with the example (don't just check the example's strings). Write a script under artifacts/review-evidence/ that extracts the example blocks and compares them with evals/golden/sample.expected.json (flag evidence, quotes, providers, dates); grep each referenced name. Also judge the export as a demand-letter paste: tool-authored text in the carrier block (e.g. "visit count not stated") is adjuster ammunition even when the reviewer asked for the disclosure. See [[reviewer-tooling-quirks]].
---
name: golden-set-recurring-findings
description: Patterns found reviewing evals/golden (T-015, 2026-11-01) to re-check on any later golden/eval change — must/should downgrades, leaky must_not regexes, missing tolerated flags
metadata:
  type: project
---

Recurring golden-set weaknesses found in the T-015 review (commit 47520a8, verdict fail):
- Appendix C "Expected flags (at minimum)" items got downgraded to `should` (K4 new onset after the 73-day gap, K5 wrong intake accident date). Under README scoring, `should` never counts as a miss, and cross-type credit isn't implemented. Re-check levels whenever golden files change.
- Explicit prior-condition mentions marked `should` (case_06 P2/P3), while the sample's different-region prior (P1) is `must`. Check that levels are consistent across cases.
- A credible adjuster attack with no golden or tolerated entry gets scored as a false positive (case_06 "denies prior neck problems" vs chiropractor history). Ask "what would the adjuster's letter quote?" and confirm each answer is must, should or tolerated.
- must_not regexes are only tested negatively (they must not match the input). Probe them with known-bad phrasings: the sample M9 regex missed "full recovery", and M2 missed "caused by the January collision" and "Degenerative findings".

Round 2 (commit 3c5eb7c) added these patterns:
- A level fix isn't enough. If two `must` flags share type and cite (K4/K5: causation, record 7) and matching is type+cite only, one candidate satisfies both. Simulate the README matching rule literally, and require evidence overlap plus one-to-one assignment.
- The byte-exact export golden (extracted from REQUIREMENTS §6) can drift from the golden JSON: a missing must-flag line, and evidence changes such as C1 "rear-ended" that should add a "flagged language" row. Rebuild each notes section from the JSON plus the R-EX-4 rules, and diff.
- Spec text (R-FL-4) can lag behind a golden change. Grep REQUIREMENTS for the old rule.

**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility.
**How to apply:** on any re-review of evals/golden or evals.run, re-run a probe like artifacts/review-evidence/T-015-paralegal-regex-probe.py and re-check the level of every Appendix C item. Related: [[reviewer-hook-constraints]]
---
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.

**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
---
id: "T-015"
title: "Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs"
milestone: "M1"
role: "qa"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:57:30Z"
claimed_by: "qa"
claimed_at: "2026-11-02T00:51:53Z"
rounds: 2
commits: ["47520a8", "3c5eb7c", "f8c1948"]
reviews:
  - {"persona": "legal-nurse-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-015-legal-nurse.md", "at": "2026-11-02T00:31:54Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-015-paralegal.md", "at": "2026-11-02T00:32:57Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-015-paralegal-r2.md", "at": "2026-11-02T00:49:35Z"}
  - {"persona": "legal-nurse-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-015-legal-nurse-r2.md", "at": "2026-11-02T00:51:24Z"}
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
    - [major] Seeded-hallucination set misses laterality, spinal level, real severity upgrade, complaint-as-finding and negative-study flips; H12 is mislabeled — fix: Replace or add items (keep 20+) with at least: right -> left arm or foraminal side; C5-C6 -> C6-C7; mild -> severe narrowing; neck pain 6/10 -> 9/10; 'C/O neck pain' -> 'exam revealed cervical tenderness'; 'CT head negative' -> 'CT h
    - [major] Entries have no required clinical content, so omissions and complaint-to-finding rewrites in entry summaries go unmeasured — fix: Add per-entry 'summary_must_mention' (clinically material tokens: E2 'concussion' and 'without loss of consciousness', 'cervical strain'; E8 'C5-C6', 'right', 'mild', a hedge token; E9 'recommend' and 'patient states'; E1 a complaint marker such as 'compla
    - [minor] Other regex gaps: M8 misses stenosis/sprain/disc bulge/radicular; M9 fires on 'not fully recovered'; case_06 M2 misses 'No prior neck problems' — fix: Extend M8 with stenosis, sprain, disc bulge, radicul(ar|itis), nerve root. Add a negative lookbehind for 'not (fully )?' to M9. Allow an optional body-region word in case_06 M2.
    - [minor] Reference wording upgrades the record in two places: P2 '(pre-existing)' and case_06 P1 'Ongoing' — fix: P2: 'MRI wording ("may represent degenerative change") that an adjuster may argue shows a pre-existing condition; hedged, not a diagnosis.' case_06 P1: 'Intermittent ("off and on") chiropractic care since an earlier lifting injury; body region not stated.'
    - [minor] case_08 K1 makes bare 'Clinical correlation recommended' a `must` causation flag — fix: Set K1 in case_08 to level `should`, or add a tolerated note saying bare correlation language is informational.
    - [minor] Controls are verbatim or near-verbatim, so judge precision on legitimate clinical paraphrase is untested — fix: Add at least 5 paraphrase controls, e.g. '41-year-old male restrained driver, rear-ended at about 35 mph; complained of neck pain 7/10 and headache; alert and oriented; taken to Central ER.'
- 2026-11-02T00:32:57Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-015-paralegal.md
- 2026-11-02T00:32:57Z orchestrator: assigned: qa
- 2026-11-02T00:33:18Z qa: claimed
- 2026-11-02T00:39:58Z qa: Round 2: regenerated cases (renamed fictional providers, case_09 non-visit gap, tolerated, must/should changes, bad/good examples), hallucinations 34 + 10 controls, sample.export.expected.txt. Next: validator + README.
- 2026-11-02T00:43:10Z qa: moved in_progress -> in_review
- 2026-11-02T00:43:33Z orchestrator: review dispatched: legal-nurse r2, paralegal r2
- 2026-11-02T00:49:35Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-015-paralegal-r2.md; round 2; findings:
    - [blocker] K5 (wrong intake accident date as a causation issue) is still unenforceable: K4 and K5 share type+cite, so one record-7 causation flag satisfies both, and the expected export has no K5 line — fix: In README scoring, match a golden flag only when the candidate's evidence excerpt overlaps (normalized substring either way) at least one golden `excerpt`-field evidence item. Assign cand
    - [major] Expected export can't be derived from R-EX-4 and the golden JSON (record 1 missing from 'flagged language quoted', Bills-to-request label rule not followed) — fix: Decide the record-1 question: either C1's 'rear-ended' evidence counts and the notes list record 1 ('Conflict, accident date'), or C1's record-1 evidence becomes field 'date' only. Then fix s6 or R-EX-4(8) so the bills-to-
    - [major] REQUIREMENTS R-FL-4 still says K4/K5 are 'should', credited through G1/C1, which contradicts the golden README; no D-entry records the change — fix: Orchestrator records a D-entry (K4/K5 must; type match explicit; evidence-overlap matching per the blocker fix). The writer updates R-FL-4, R-TL-4 and ship bar 4 (>= 33 of 34) to match.
    - [minor] `source_kind` has no scoring rule and is tagged on whole entries that mix provider findings with patient statements; the golden export's EMS summary drops the attribution — fix: Move source_kind to span level ({excerpt, kind}) and add a README scoring rule: the summary clause that renders that span carries an attribution word. Remove the tag from case_09 E3. Decide whether the s6 EMS
    - [minor] Remaining regex gaps: aggravation wording, sample laterality swap, 'non-compliant', case_06 'No history of neck problems' — fix: Sample M2: add aggravat\w+ (by|from). New sample regex for \bleft\s+(arm|foramin\w+|fingers). Add a \bnon-?complian\w+ regex for tool-authored summaries. case_06 M2: allow 'no (prior|previous|history of)'.
    - [minor] case_09: no tolerated entry for 'Return in 2 weeks' followed by a 56-day return, so a compliance/causation flag would be a false positive — fix: Add tolerated T1 {type: causation, cite.all [1,4], subtype follow_up_not_kept}, worded as the record's own words with no 'non-compliant' label.
    - [minor] Two different golden total strings for the sample, with no surface named — fix: In the README schema, state that totals.display is the UI/notes string and the letter total line is R-EX-8 (or add totals.letter_line).
- 2026-11-02T00:49:35Z orchestrator: assigned: qa (r3 after legal-nurse r2)
- 2026-11-02T00:51:24Z orchestrator: review legal-nurse-reviewer (claude-opus-5-5): changes — reviews/T-015-legal-nurse-r2.md
- 2026-11-02T00:51:39Z orchestrator: assigned: qa
- 2026-11-02T00:51:53Z qa: claimed
- 2026-11-02T00:57:04Z qa: moved in_progress -> in_review
- 2026-11-02T00:57:30Z orchestrator: review dispatched: paralegal r3 (+nurse checklist)

## Handoff
Round 3. [PL blocker K4/K5] scoring now needs OVERLAPPING evidence on every cite.all record + one-to-one assignment (each tool flag satisfies at most one golden flag); K4 evidence 'New onset pain', K5 evidence = intake-date line; reference matcher + 6 fixtures in check_golden.py; K5 line added to the causation bullet and verified in its OWN bullet. [PL major export] record 1 under flagged-language; bills = header label up to first comma, chronological; D-019 total line; check_golden.py re-derives flagged-language + bills from sample.expected.json and verifies every quote against its cited record, headings, summaries vs required_terms/numbers. [PL minors] regex leaks closed (ESI/s-p, HNP/extrusion/bulge, mTBI/possible-brief LOC, from the January collision, injured in/resulted in/because of/aggravated by, left arm/foraminal, non-compliant, No history of/past/negative for); every LEAK probe is a tested bad_example; case_09 tolerated follow_up_not_kept; totals = letter_line/ui_line/notes_lines; service_date_in_excerpt. [LN M1/D-022] required_terms checked on the summary alone with any-of qualifier alternatives; export summaries validated against them (EMS summary now 'complained of'). [LN M2] 'her neck pain is due to the collision' now a bad example; M2 narrowed; 3 temporal_to_causal hallucinations. [LN M3] entry-level source_kind removed; self_report_spans per sentence with attribution_any. [LN minors] controls S08/S10 fixed; +approximation_dropped, abbreviation_misexpanded items; SE5 judge_masked; case_01 negative for fracture; new regexes M15 M16 M17. Verified: python3 evals/golden/check_golden.py -> golden OK (57 must_nots tested, 40 hallucinations, 10 controls). Left: REQUIREMENTS lag is writer T-025 (golden is authority).

f8c1948 fix(evals): golden set round 3 - overlap+one-to-one flag matching, export golden derivations, span-level self-report, summary-only required terms
da17ba2 docs(research): T-008 round 3 — quote-anchor every sample-case claim; drop invented referral and 'active care'
2e92535 docs(spec): reconcile requirements with D-016..D-022, golden and API; section 8 as owned open list
e3fbb08 fix(harness): round-3 hardening from security r2 under the D-023 threat model
388d5b2 docs(architect): round 3 ADR amendments, golden-derived export, demo-only gate
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:32.470Z

**tool call — Bash**
````
{
 "command": "python3 evals/golden/check_golden.py; echo EXIT=$?; git diff --stat 3c5eb7c..f8c1948 -- evals/golden; grep -n \"D-019\\|D-021\\|D-022\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -80"
}
````

### User / tool · 2026-11-02T00:57:32.621Z

**tool result**
````
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
EXIT=0
 evals/golden/README.md                             |  24 +-
 evals/golden/case_01_date_formats.expected.json    |  19 +-
 evals/golden/case_02_gap_boundaries.expected.json  |   4 +-
 evals/golden/case_03_rate_and_ocr.expected.json    |   8 +-
 .../case_04_duplicates_no_amounts.expected.json    |   4 +-
 .../golden/case_05_provider_conflict.expected.json |  10 +-
 .../case_06_subtle_pre_existing.expected.json      |  57 ++++-
 .../golden/case_07_prompt_injection.expected.json  |   4 +-
 .../case_08_diagnosis_temptation.expected.json     |  22 +-
 .../case_09_nonvisit_hides_gap.expected.json       |  39 ++-
 evals/golden/check_golden.py                       | 275 +++++++++++++++++++--
 evals/golden/hallucinations.jsonl                  |   6 +
 evals/golden/hallucinations_controls.jsonl         |   4 +-
 evals/golden/sample.expected.json                  | 213 +++++++++++++---
 evals/golden/sample.export.expected.txt            |   9 +-
 15 files changed, 589 insertions(+), 109 deletions(-)
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30:| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31-| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:34.680Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-015-paralegal-r2.md | head -150"
}
````

### User / tool · 2026-11-02T00:57:34.756Z

**tool result**
````
# T-015 round 2: paralegal-reviewer (Maria Delgado lens)

**Verdict: fail** (1 blocker, 2 majors, 4 minors, 1 nit).

Most of round 1 is fixed. K4 and K5 are now `must`. case_06 has all three prior-condition mentions at `must`, plus a neutral `must` conflict flag for the denial vs the chiropractic history. Every probe phrase from round 1 is now caught, and check_golden.py tests the bad and good examples. case_09 proves the rule that billing statements and phone notes don't count as visits. Every provider value equals the header label, and every synthetic facility name is clearly invented. The expected export matches REQUIREMENTS §6 byte for byte. Every quote in it is verbatim from the record it is attributed to, and the total is $8,390.00.

What still fails is K5, the wrong accident date on the intake form treated as a causation issue. The golden JSON makes it `must`, but the README scoring rule matches flags on type + cited records only. K4 and K5 are both `causation` citing record 7, so a single record-7 causation flag about "new onset" satisfies both. A tool can still get 100% causation recall without telling me that the intake date undercuts causation. The expected export has the same hole: its "Causation language" line has no intake-date item even though every flag is accepted.

Full resolution table: `artifacts/review-evidence/T-015-r2-paralegal.md`.

Commands run (exact output):
- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered` (exit 0)
- `python3 artifacts/review-evidence/T-015-r2-paralegal-probe.py` → `artifacts/review-evidence/T-015-r2-paralegal-probe.out.txt` (exit 0)
- `git status --porcelain evals/golden/ spec/REQUIREMENTS.md` → (empty); `git diff --stat 3c5eb7c -- evals/golden/` → (empty); `git log -1 --format=%h -- evals/golden` → `3c5eb7c`

```json
{"card": "T-015", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "round 2, commit 3c5eb7c (diff 47520a8..3c5eb7c -- evals/golden): README.md, sample.txt, sample.expected.json, sample.export.expected.txt, case_01..09 .txt/.expected.json, hallucinations*.jsonl, check_golden.py; refs spec/REQUIREMENTS.md s6, R-EX-4, R-EX-8, R-FL-4, R-TL-3; memory/ORCHESTRATOR_DECISIONS.md D-001..D-018; no app (pre-code eval data); sample case evals/golden/sample.txt",
 "exercised": [
  "python3 tools/board.py show T-015 (AC 1-4, handoff notes)",
  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered', exit 0",
  "artifacts/review-evidence/T-015-r2-paralegal-probe.py (output T-015-r2-paralegal-probe.out.txt): s6 byte compare, per-record quote attribution of every letter line, notes coverage of each must flag, literal README:70 matching simulation, provider==header for all cases, Source-label inventory, levels/tolerated per case, round-1 regex probes + new probes, case_09 gap recompute and must_nots, source_kind scoring lookup, hallucination categories",
  "Read case_06 and case_09 .txt + expected.json in full; read sample/case_03/05/08 must_not and tolerated lists",
  "Compared sample.export.expected.txt line by line with REQUIREMENTS s6 and R-EX-4 (1)-(11) and with the 9 records",
  "git status/diff vs 3c5eb7c (clean)"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 4, "arithmetic_and_dates": 5, "appendix_c_fidelity": 3, "flag_levels_realism": 5, "adjuster_attack_coverage": 4, "must_not_strength": 4, "export_golden_consistency": 2, "synthetic_labeling": 5},
 "findings": [
  {"severity": "blocker", "title": "K5 (wrong intake accident date as a causation issue) is still unenforceable: K4 and K5 share type+cite, so one record-7 causation flag satisfies both, and the expected export has no K5 line",
   "evidence": "README.md:70 'A golden flag is matched only by a candidate flag of the same type that cites every record in cite.all and >= 1 of cite.any'. Nothing requires evidence overlap or one-to-one assignment. sample.expected.json K4 and K5 are both {type: causation, cite.all: [7]}. probe s4 (T-015-r2-paralegal-probe.out.txt): a single candidate {causation, cites {7}, 'New onset pain after a 73-day gap...'} -> 'matches K4 (temporal_after_gap): True', 'matches K5 (accident_date_inconsistency): True'. probe s3: 'causation line mentions intake-date (K5 evidence)? False'. sample.export.expected.txt's causation line lists only records 8, 6, 9 and record 7 \"New onset pain\", even though the case states that all flags are accepted.",
   "why_it_matters": "This is the round-1 blocker in a narrower form. A tool that never tells me the intake-form date undercuts causation still scores 5/5 causation recall. Appendix C lists that item under 'Expected flags (at minimum)'. The byte-exact export golden (ship bar 8) also builds the omission in: a product that emits and renders K5 correctly fails the export test.",
   "fix": "In README scoring, match a golden flag only when the candidate's evidence excerpt overlaps (normalized substring either way) at least one golden `excerpt`-field evidence item. Assign candidates to golden flags one-to-one (bipartite), so one candidate can't satisfy two golden flags. Add the K5 item to the s6 causation line (record 7 \"Date of accident per intake form: 2026-01-19.\"), via the writer/orchestrator, and re-extract sample.export.expected.txt. Have check_golden.py assert that every `must` flag of the sample has its evidence in the notes block.",
   "acceptance_test": "Runner fixture: one record-7 causation candidate with evidence 'New onset pain' -> K4 TP, K5 miss, causation recall 4/5. check_golden.py fails if any sample must-flag evidence excerpt is absent from internal_notes_text."},
  {"severity": "major", "title": "Expected export can't be derived from R-EX-4 and the golden JSON (record 1 missing from 'flagged language quoted', Bills-to-request label rule not followed)",
   "evidence": "R-EX-4(4): list 'each letter entry whose excerpt contains the evidence of a flag that is not dismissed'. sample.expected.json C1 evidence now includes record 1 'rear-ended at approx. 35 mph' (field excerpt), and the record-1 letter quote contains it. 'FLAGGED LANGUAGE QUOTED IN THE LETTER' in sample.export.expected.txt lists records 4, 6, 7, 8, 9 and not record 1. R-EX-4(8): 'providers (the label up to the first comma)', yet the export reads 'Dr. Alvarez, primary care' (rule gives 'Dr. Alvarez'), and the order (Austin EMS; Dr. Alvarez; Hill Country; Capital PT) is not record order, with no stated sort. check_golden.py:311-333 checks only that quotes are verbatim somewhere in sample.txt, not that they are attributed to the right record, and it checks no R-EX-4 section rule.",
   "why_it_matters": "The export golden is the M1 reference for byte-exact output. If a correct implementation of the written rules fails it, someone will either hard-code the text or relax the test. Either way the internal notes stop telling me exactly which adverse language is in the letter.",
   "fix": "Decide the record-1 question: either C1's 'rear-ended' evidence counts and the notes list record 1 ('Conflict, accident date'), or C1's record-1 evidence becomes field 'date' only. Then fix s6 or R-EX-4(8) so the bills-to-request label and order follow a stated rule, and re-extract. Add a check_golden.py step that rebuilds the 'flagged language' and 'bills to request' sections from sample.expected.json + R-EX-4 and compares them.",
   "acceptance_test": "check_golden.py derives both sections from the JSON and the rule, and they equal the export golden; every quoted span is checked against the record number it is cited to."},
  {"severity": "major", "title": "REQUIREMENTS R-FL-4 still says K4/K5 are 'should', credited through G1/C1, which contradicts the golden README; no D-entry records the change",
   "evidence": "spec/REQUIREMENTS.md:68 R-FL-4 'the record-7 items (... K4-K5) are `should`, credited when found directly or through G1/C1'. README.md:70 'G1 (gap) and C1 (conflict) do not satisfy K4 and K5' and README.md:146 'REQUIREMENTS R-FL-4 still says K4/K5 are should (orchestrator decision: must)'. `grep -n K4 memory/ORCHESTRATOR_DECISIONS.md` finds nothing. R-TL-4/ship bar still say 20 seeded items (file has 34).",
   "why_it_matters": "The runner author will implement one of two contradictory scoring rules. If they follow R-FL-4, the round-1 blocker comes back without anyone editing evals/golden.",
   "fix": "Orchestrator records a D-entry (K4/K5 must; type match explicit; evidence-overlap matching per the blocker fix). The writer updates R-FL-4, R-TL-4 and ship bar 4 (>= 33 of 34) to match.",
   "acceptance_test": "grep 'should' near K4/K5 in spec/REQUIREMENTS.md returns nothing; a D-entry cites T-015 r2."},
  {"severity": "minor", "title": "`source_kind` has no scoring rule and is tagged on whole entries that mix provider findings with patient statements; the golden export's EMS summary drops the attribution",
   "evidence": "probe s10: 'source_kind' in scoring section: False. Entry-level patient_self_report tags on case_06 E1 (excerpt includes the ER diagnosis 'Cervical strain'), sample E1 (EMS 'Alert and oriented'), case_09 E3 ('Work note provided' is the clinic's act). sample E1 required_terms ['C/O','complain','reports','reported'] are satisfied by the excerpt alone. The export summary reads 'neck pain 7/10 and headache' with no 'complained of'.",
   "why_it_matters": "Checklist 23: self-reports stay attributed. With no rule, the runner may skip the check entirely, or apply it to the whole entry and push the tool to call an ER diagnosis a patient complaint.",
   "fix": "Move source_kind to span level ({excerpt, kind}) and add a README scoring rule: the summary clause that renders that span carries an attribution word. Remove the tag from case_09 E3. Decide whether the s6 EMS summary should say 'complained of neck pain 7/10'.",
   "acceptance_test": "README scoring names source_kind; every tagged span is a patient statement; the runner rejects 'Patient had neck pain per EMS exam' for sample E1."},
  {"severity": "minor", "title": "Remaining regex gaps: aggravation wording, sample laterality swap, 'non-compliant', case_06 'No history of neck problems'",
   "evidence": "probe s7: caught=[] for 'Persistent neck pain 6/10; prior low back pain (2023) aggravated by the collision.', 'Pain radiating to left arm.', 'Patient was non-compliant with PT.', and case_06 'No history of neck problems.'",
   "why_it_matters": "'Aggravated by' is a causation claim (an aggravation theory), and a side swap is the error an adjuster spots first. Both currently depend on the LLM judge alone.",
   "fix": "Sample M2: add aggravat\\w+ (by|from). New sample regex for \\bleft\\s+(arm|foramin\\w+|fingers). Add a \\bnon-?complian\\w+ regex for tool-authored summaries. case_06 M2: allow 'no (prior|previous|history of)'.",
   "acceptance_test": "The four probe strings are in bad_examples and fire; check_golden.py stays green on inputs."},
  {"severity": "minor", "title": "case_09: no tolerated entry for 'Return in 2 weeks' followed by a 56-day return, so a compliance/causation flag would be a false positive",
   "evidence": "case_09 rec 1 'Return in 2 weeks' (2026-02-02); next visit rec 4 2026-03-30; probe s9: causation flags [] and tolerated []. D-013 maps compliance to causation.",
   "why_it_matters": "'Told to come back in two weeks, came back in eight' is how the adjuster will word it. Penalizing the tool for raising it pushes it toward silence.",
   "fix": "Add tolerated T1 {type: causation, cite.all [1,4], subtype follow_up_not_kept}, worded as the record's own words with no 'non-compliant' label.",
   "acceptance_test": "A causation candidate citing case_09 records 1 and 4 scores as tolerated, not FP."},
  {"severity": "minor", "title": "Two different golden total strings for the sample, with no surface named",
   "evidence": "sample.expected.json totals.display 'Billed charges stated in these records: $8,390 (excludes physical therapy — per-visit rate only, visit count not stated)' vs export letter 'Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)' (probe s8).",
   "why_it_matters": "R-EX-8 forbids the 'visit count not stated' reason in the letter. If the runner compares the letter total to totals.display, the R-EX-8 wording looks wrong, or the reason leaks in.",
   "fix": "In the README schema, state that totals.display is the UI/notes string and the letter total line is R-EX-8 (or add totals.letter_line).",
   "acceptance_test": "README names the surface for each string; check_golden asserts the letter total line equals totals.letter_line."},
  {"severity": "nit", "title": "case_09 billing-statement charge has no date-of-service field for specials reconciliation",
   "evidence": "case_09 A1 {record_no 2, excerpt 'Statement for visit of 2026-02-02: $275.'}; the entry date is correctly 2026-03-01 (R-TL-3) and M2's good_examples allow mentioning the visit date.",
   "why_it_matters": "I reconcile specials by DOS. The quote carries it, so nothing is lost, but a structured field would make reconciliation one glance.",
   "fix": "Optional: add amounts[].service_date_in_excerpt '2026-02-02' (evidence only, never the entry date).",
   "acceptance_test": "Field present and verbatim in the excerpt."}
 ],
 "whats_right": [
  "Every round-1 probe phrase is now caught, and every regex/structural must_not carries >= 3 bad and >= 3 good examples that check_golden.py actually fires/does not fire.",
  "case_06 C1 and case_09 are exactly how I'd want them: the conflict is framed as possible, records are requested, the patient is never accused, and billing/phone dates never close a visit gap.",
  "The expected letter is clean demand text: header labels verbatim, US long dates, verbatim whole-sentence quotes from the cited record, $8,390.00 from explicit charges only, and no flag text in the letter."
 ],
 "questions_for_chris": [
  "Record 1's letter quote ('rear-ended at approx. 35 mph') is now C1 evidence. Should the internal notes list the EMS entry under 'flagged language quoted in the letter' (mechanically per R-EX-4), even though the mechanism helps rather than hurts the client?"
 ]}
```
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:35.078Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-015-legal-nurse-r2.md"
}
````

### User / tool · 2026-11-02T00:57:35.156Z

**tool result**
````
# T-015 Eval golden set, round 2: legal-nurse review

**Verdict: changes** (0 blockers, 3 majors). Both round-1 blockers are fixed. All 38 round-1 probe phrasings now behave correctly against the new regexes: 36 OK, and 2 are flag prose that is now out of regex scope (D-007). The hallucination set now covers laterality, level, region, severity, complaint-as-finding and negative-study flips, and every one of its 34 items is genuinely unsupported.

Three things still keep the eval from measuring the clinical distinctions:
- **Summary omissions are still unmeasured.** `required_terms` are scored on summary+excerpt, so a summary that drops "without loss of consciousness", "may represent" or "patient states" still passes.
- **Patient-attributed causation is allowed even when the patient never stated a cause.** Sample M2 lists "Patient states her neck pain is due to the collision." as a good example. The record says only "began after", and the patient is 41M.
- **`source_kind: patient_self_report` covers whole mixed entries.** That label now includes exam findings and a diagnosis.

Resolution table and per-item checks: `artifacts/review-evidence/T-015-r2-nurse.md`. Probe: `artifacts/review-evidence/T-015-r2-nurse-probe.py`, output in `.out.txt`.

```json
{"card": "T-015", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 3c5eb7c (git diff 47520a8..3c5eb7c -- evals/golden): README, check_golden.py, sample + case_01..09 (.txt/.expected.json), hallucinations.jsonl (34), hallucinations_controls.jsonl (10), sample.export.expected.txt, seeded_edits SE1-SE4; spec refs REQUIREMENTS R-TL-4/8/10, R-FL-7, R-RV-3; decisions D-006/D-007/D-012/D-014. No app (pre-code card).",
 "exercised": [
   "python3 tools/board.py show T-015 (AC 1-4, handoff notes)",
   "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
   "read README.md and check_golden.py in full; printed every sample must_not (pattern, unless_context, bad/good examples)",
   "python3 -I artifacts/review-evidence/T-015-r2-nurse-probe.py: 38 round-1 phrasings (36 OK, 2 n/a flag prose, 0 leak, 0 false positive) + 50 new phrasings (18 OK, 30 LEAK, 2 FALSEPOS judged acceptable) against the live regexes with check_golden semantics; output saved to T-015-r2-nurse-probe.out.txt",
   "required_terms omission probe on sample E1/E2/E8/E9 (pass on summary+excerpt, fail on summary only)",
   "R-TL-10 number-check probe on E5 using check_golden nums(): 8/10, 2/10, 20/10 raise no code warning",
   "printed and judged all 34 hallucination items and 10 controls against record_text",
   "read case_06, case_08, case_09 .txt; printed entries/required_terms/source_kind/flags/tolerated/must_not for case_01..09",
   "read sample.export.expected.txt (letter + internal notes) and checked letter summaries against excerpts",
   "grep 'pre-existing) change|Ongoing chiropractic' evals/golden/*.json -> no output, exit 1",
   "grep source_kind in golden, README, REQUIREMENTS (R-FL-7 uses 'patient_report' on flags)",
   "read memory/ORCHESTRATOR_DECISIONS.md D-006..D-018"
 ],
 "verdict": "changes",
 "scores": {"clinical_fidelity_of_reference_wording": 4, "appendix_c_must_not_check_reliability": 4, "hallucination_set_genuineness": 5, "hallucination_failure_mode_coverage": 4, "controls_faithfulness": 4, "objective_vs_subjective_coverage": 3, "summary_omission_measurement": 2},
 "findings": [
  {"severity": "major", "title": "required_terms are scored on summary+excerpt, so a summary that drops the LOC qualifier, the hedge, 'patient states' or the complaint marker still passes (round-1 F4 only partly fixed)",
   "evidence": "evals/golden/README.md scoring 'Entries': '**summary+excerpt** satisfying every `required_terms` item'. Probe (T-015-r2-nurse-probe.out.txt): E2 summary 'Cervical strain and concussion; CT head negative; cyclobenzaprine 10 mg; PCP in 1 week.' -> pass_on_summary+excerpt=True pass_on_summary_only=False; same for E8 'C5-C6 disc protrusion with mild right foraminal narrowing.' (no hedge), E9 without 'patient states', E1 'exam showed neck injury with pain 7/10'. No regex fires on 'Diagnosed with cervical strain and concussion; CT head negative.' (LEAK row). R-TL-4 judge #1 checks only that the summary 'adds nothing', so it cannot catch an omission. The golden export's own E1 summary ('Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; ...') has none of E1's complaint terms.",
   "why_it_matters": "Dropping 'without loss of consciousness' from the concussion diagnosis is a dealbreaker for this persona. The summary sentence is the tool's own statement in the letter. If it reads 'concussion' while the quote below reads 'concussion without loss of consciousness', defense counsel can quote either one. The same applies to a dropped 'may represent' or 'patient states'. The eval currently has no way to fail any of these.",
   "fix": "Add a summary-only field (e.g. `summary_required_terms`) for the qualifier tokens, with any-of alternatives so faithful wording passes. E2: 'concussion' + any of ['without loss of consciousness','no loss of consciousness','w/o loss of consciousness','without LOC','no LOC','w/o LOC']. E8: any of ['may represent','may be','possible','could represent']. E9: any of ['patient states','per patient','patient reports','patient-reported']. E1: any of ['C/O','complain','reports']. case_06 E1: any of ['denies','denied']. case_06 E2: any of ['off and on','intermittent']. A miss makes the entry needs_review (or fails it). Either align the export example's E1 summary or exempt it explicitly.",
   "acceptance_test": "A stub run where record 2's summary is 'Cervical strain and concussion; CT head negative.' marks E2 not-found or needs_review. The same happens for E8 without a hedge token and E9 without an attribution token. check_golden.py verifies each summary_required_terms alternative is consistent with its record."},
  {"severity": "major", "title": "Sample M2 lets patient-attributed causation through even when the patient never stated a cause; its good example also gets the patient's sex wrong; no judge item covers temporal-to-causal",
   "evidence": "sample.expected.json:735 good_examples includes 'Patient states her neck pain is due to the collision.'. M2 statement: \"Patient-attributed wording ('patient states ...') is allowed.\" Record 9 says only 'Patient states symptoms began after the January collision.' Record 1 says '41M'. Probe: 'Patient states the collision caused his symptoms.' -> LEAK. hallucinations.jsonl has no temporal_to_causal item (H10 covers only recasting as a physician opinion). M10 judge bad_examples cover only the physician recast.",
   "why_it_matters": "'Began after' is a temporal report. 'Due to' and 'caused' are causal claims. Putting a causal claim in the patient's mouth changes what the record says, even when 'patient states' is kept. This is the record an adjuster will read most closely. The golden marks the upgraded wording as acceptable for this exact case, and the judge's ship bar never tests it.",
   "fix": "Replace that good example with a faithful one (e.g. 'Per patient, symptoms began after the January collision.'). Narrow the M2 statement to 'patient-attributed wording that reproduces what the patient said'. Add a hallucination item, category temporal_to_causal: record 9, candidate 'Patient states the collision caused his symptoms.'. Add it to REQ_CAT and as an M10 judge bad_example.",
   "acceptance_test": "grep -n 'due to the collision' evals/golden/sample.expected.json shows no good_example; check_golden REQ_CAT contains temporal_to_causal; judge #1 flags the new item (partially or unsupported)."},
  {"severity": "major", "title": "source_kind 'patient_self_report' labels whole mixed entries, including exam findings and a diagnosis; vocabulary differs from R-FL-7",
   "evidence": "case_08_diagnosis_temptation.expected.json:61 E1 source_kind patient_self_report; record 1 includes 'Tenderness over the anterior shoulder.' (palpation finding). case_06_subtle_pre_existing.expected.json:109 E3 labels 'Cervical ROM reduced.' (measurement); :73 E1 labels 'Cervical strain' (ER assessment). sample.expected.json:104 E1 labels 'Alert and oriented.'. README:40 'content is the patient's own statement/complaint and must stay attributed'. REQUIREMENTS R-FL-7 uses source_kind = \"patient_report\" on flags.",
   "why_it_matters": "If the runner or the prompt follows this label, it requires exam findings and a diagnosis to be attributed to the patient ('patient reports tenderness', 'patient reports cervical strain'). That reverses the subjective/objective error and understates objective evidence. The golden should encode the S/O split exactly, not approximately.",
   "fix": "Make it span-level: `self_report_spans` lists the verbatim subjective sentences only. Sample E1: 'C/O neck pain 7/10 and headache'. E9: 'Patient states symptoms began after the January collision'. case_06 E1: 'Patient denies prior neck problems'. case_06 E3: 'History: occasional stiffness in the mornings at baseline'. case_08 E1: 'Shoulder pain after a fall'. Use R-FL-7's value name or document the difference.",
   "acceptance_test": "check_golden asserts each self_report_span is verbatim in its record and contains none of: tenderness, ROM, Dx, alert and oriented, strain; no entry-level patient_self_report remains on a record with an O/A sentence."},
  {"severity": "minor", "title": "Regex floor still leaks 30 of 50 new violating phrasings (judge #1 is the backstop)",
   "evidence": "T-015-r2-nurse-probe.out.txt r2 LEAK rows: M6 'Concussion with possible LOC.', 'Brief LOC at scene.', 'LOC x 2 minutes.', 'mTBI; cervical strain.'; M3 'Patient could not turn head, and MRI shows degenerative disc disease.' (unrelated 'could' exempts it across a comma), 'Findings may represent degenerative disc disease.'; M2 'Neck pain from the January collision.', 'Injured in the collision.', 'The crash resulted in a disc protrusion.', 'Disc protrusion because of the collision.'; M1/M8 'C5-C6 disc extrusion ...', 'HNP at C5-C6.', 'C5-C6 bulge.'; M13 'ESI performed.', 's/p cervical ESI.', '...injection scheduled.'; M9 'Neck pain resolved by discharge.'; case_06 M2 'No history of neck problems.', 'No past neck problems.', 'Negative for prior neck problems.'; case_05 M4 'The car caused the fracture.'",
   "why_it_matters": "Disc protrusion -> extrusion/bulge (Fardon nomenclature), ESI 'performed', and denial -> 'no history' are exactly the substitutions this persona checks. The README calls regex the deterministic floor, and today that floor misses common chart abbreviations (ESI, HNP, mTBI, LOC).",
   "fix": "M6: add (possible|questionable|brief) LOC, LOC x, mTBI. M3: require the hedge within ~4 words before the term, or stop the unless_context window at ',' / 'and'; add 'disc disease'. M2: 'from the (\\w+ )?collision', 'injured in', 'resulted in', 'because of'. M1/M8: extrusion, HNP, bulge. M13: ESI, s/p, scheduled. M9: resolved (excluding 2023 LBP context), 'patient recovered'. case_06 M2: history of, past, negative for. case_05 M4: 'caused the fracture', 'from being struck'.",
   "acceptance_test": "Every LEAK row in T-015-r2-nurse-probe.out.txt becomes a bad_example that check_golden proves fires; every OK faithful row stays a good_example."},
  {"severity": "minor", "title": "Two paraphrase controls are not cleanly faithful: S08 invents the patient's sex, S10 drops 'radiating'",
   "evidence": "hallucinations_controls.jsonl S08 'Her neck pain continues. She has visited a chiropractor ...'; case_06 never states sex. S10 'new onset of arm pain on the right side with numb fingers' vs record 'New onset pain radiating to right arm with numbness in fingers'.",
   "why_it_matters": "A judge that correctly returns `partially` on S08 is graded against a control labeled supported. 'Radiating' is the symptom character that ties the record to the later MRI, so losing it in an accepted paraphrase teaches the wrong house style.",
   "fix": "S08: 'Neck pain continues. The patient has seen a chiropractor intermittently since a lifting injury several years ago.' S10: 'new onset pain radiating to the right arm with numb fingers, rated 7/10; ...'.",
   "acceptance_test": "No control contains he/she/his/her unless the record states sex; S10 contains 'radiat'."},
  {"severity": "minor", "title": "Missing judge-calibration items: 'approx.' dropped, abbreviation mis-expansion, pain-score swap the R-TL-10 code check cannot see",
   "evidence": "No hallucination category for approximation or abbreviation. Probe: on E5 (source 'Capital PT, visit 8', date 2026-02-20), 'Visit 8: pain 8/10, improving.', 'pain 2/10' and 'pain 20/10' produce no new numbers, so no code warning. seeded_edits has no judge edit for this.",
   "why_it_matters": "'approx. 35 mph' -> '35 mph' and 'approx. 40%' -> '40%' turn estimates into measurements. A changed pain score is a severity change. Because R-TL-10 allows label and date digits, judge #1 is the only check, and nothing proves it catches this.",
   "fix": "Add hallucination items: approximation_dropped (record 1 '... rear-ended at 35 mph'), abbreviation_misexpanded (e.g. reading 'PT' in record 6 as 'patient'). Add seeded edit SE5 kind judge 'Visit 8: pain 8/10, improving.' -> needs_review.",
   "acceptance_test": "check_golden REQ_CAT includes approximation_dropped; SE5 exists and its expected_state is needs_review."},
  {"severity": "nit", "title": "case_01 E1 required_term is bare 'fracture' while the record says 'X-ray negative for fracture'",
   "evidence": "case_01_date_formats.expected.json E1 required_terms ['ankle','fracture']; case_01_date_formats.txt:6 'X-ray negative for fracture.'",
   "why_it_matters": "The protected fact is the negative study. A bare 'fracture' token is satisfied by a summary that says 'ankle fracture'.",
   "fix": "Use 'negative for fracture'.",
   "acceptance_test": "E1 required_terms contains 'negative for fracture'."}
 ],
 "whats_right": [
  "Both round-1 blockers are fixed. All 38 round-1 probe phrasings now behave correctly, and check_golden tests every regex's bad and good examples both ways.",
  "All 34 hallucination items are really unsupported. The new ones cover laterality, level, region, severity, complaint-as-finding, negative CT flipped and denial-as-fact, and none slipped in supported.",
  "Reference wording is now clinically careful: P2 quotes the hedge, case_06 P1 keeps 'off and on', case_06 C1 says 'not a finding that the patient misstated anything', case_08 K1 is `should`, and SE1-SE4 are right."
 ],
 "questions_for_chris": [
  "When a summary drops a qualifier the excerpt below it still carries (e.g. 'concussion' without 'without loss of consciousness'), should that make the entry needs_review (the paralegal fixes it) or fail the eval case outright?"
 ]}
```
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:36.647Z

Now I'll re-run both r2 probes against f8c1948 and confirm the working tree matches the commit.

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:38.252Z

**tool call — Bash**
````
{
 "command": "git status --porcelain evals/golden/; git log -1 --format=%h -- evals/golden; ls artifacts/review-evidence/ | grep T-015; .venv/bin/python -I artifacts/review-evidence/T-015-r2-paralegal-probe.py > artifacts/review-evidence/T-015-r3-paralegal-rerun-of-r2-probe.out.txt 2>&1; echo EXIT=$?; wc -l artifacts/review-evidence/T-015-r3-paralegal-rerun-of-r2-probe.out.txt"
}
````

### User / tool · 2026-11-02T00:57:38.412Z

**tool result**
````
f8c1948
T-015-legal-nurse-items.md
T-015-paralegal-blind.md
T-015-paralegal-regex-probe.out.txt
T-015-paralegal-regex-probe.py
T-015-r2-nurse-probe.out.txt
T-015-r2-nurse-probe.py
T-015-r2-nurse.md
T-015-r2-paralegal-jsoncheck.py
T-015-r2-paralegal-probe.out.txt
T-015-r2-paralegal-probe.py
T-015-r2-paralegal.md
EXIT=1
     104 artifacts/review-evidence/T-015-r3-paralegal-rerun-of-r2-probe.out.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:39.556Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-015-r3-paralegal-rerun-of-r2-probe.out.txt"
}
````

### User / tool · 2026-11-02T00:57:39.632Z

**tool result**
````
== 1. Export golden vs REQUIREMENTS s6 (byte compare of the two fenced blocks)
letter == s6 block1: True | notes == s6 block2: False

== 2. Letter entries: header date/label match record; quote verbatim in THAT record
  2026-01-09 'Austin EMS run report': record=[1] quote_in_record=True | summary: Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
  2026-01-09 'Central ER discharge summary': record=[2] quote_in_record=True | summary: Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
  2026-01-16 'Dr. Alvarez, primary care': record=[3] quote_in_record=True | summary: Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
  2026-01-23 'Capital PT, initial evaluation': record=[4] quote_in_record=True | summary: Cervical range of motion reduced approx. 40%; plan of care 12 visits.
  2026-02-20 'Capital PT, visit 8': record=[5] quote_in_record=True | summary: Pain 4/10, improving.
  2026-03-06 'Capital PT, visit 9': record=[6] quote_in_record=True | summary: Discharged from physical therapy after two missed appointments; pain 3/10.
  2026-05-18 'Hill Country Pain Management, new patient': record=[7] quote_in_record=True | summary: New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
  2026-05-29 'Austin Imaging, cervical MRI': record=[8] quote_in_record=True | summary: C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
  2026-06-12 'Hill Country Pain Management, follow-up': record=[9] quote_in_record=True | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
  charges: ['$6,240.00', '$2,150.00', '$8,390.00']

== 3. Notes block: does each sample `must` flag's evidence appear in the notes?
  G1 gap          must: 'Discharged from PT after two missed appointments' in notes=True; 'New onset pain radiating to right arm' in notes=True
  C1 conflict     must: 'Date of accident per intake form: 2026-01-19' in notes=True; 'rear-ended at approx. 35 mph' in notes=True
  C2 conflict     must: 'Plan of care: 12 visits' in notes=True; 'Discharged from PT after two missed appointments' in notes=True
  P1 pre_existing must: 'Patient reports low back pain in 2023, resolved' in notes=True
  P2 pre_existing must: 'Findings may represent degenerative change' in notes=True
  K1 causation    must: 'may represent degenerative change; correlate clinically' in notes=True
  K2 causation    must: 'Discharged from PT after two missed appointments' in notes=True
  K3 causation    must: 'Patient states symptoms began after the January collision' in notes=True
  K4 causation    must: 'New onset pain' in notes=True
  K5 causation    must: 'Date of accident per intake form: 2026-01-19' in notes=True
  causation line mentions intake-date (K5 evidence)? True
  causation line: - Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19.".

== 4. README matching rule, applied literally: one causation candidate citing record 7
  matches K1 (hedged_imaging): False
  matches K2 (noncompliance): False
  matches K3 (patient_self_report): False
  matches K4 (temporal_after_gap): True
  matches K5 (accident_date_inconsistency): True

== 5. Providers: golden entry provider == header label of lowest cited record (all cases)
  mismatches: []
  all Source labels:
    case_01_date_formats ['Dr. Orla Pennywhistle, phone note', 'Dr. Orla Pennywhistle, primary care', 'Pemberwick Physical Therapy, visit 1', 'Pemberwick Physical Therapy, visit 2', 'Pemberwick Physical Therapy, visit 3', 'Pemberwick Physical Therapy, visit 4', 'Quillfeather Urgent Care']
    case_02_gap_boundaries ['Thistlewick Orthopedics, Dr. Beatrix Quillon']
    case_03_rate_and_ocr ['Dr. Hobart Wimbleton, radiology', 'Gloamwood Chiropractic, billing statement', 'Gloamwood Chiropractic, initial evaluation', 'Gloamwood Chiropractic, visit 2', 'Gloamwood Chiropractic, visit 3']
    case_04_duplicates_no_amounts ['Dr. Tabitha Wrenfield, Orthopedics', 'Dr. Tabitha Wrenfield, orthopedics', 'Nimblewick Hand Therapy, intake', 'Pottsworth Emergency Department']
    case_05_provider_conflict ['Crumpet Lane Orthopedics, M. Tallowby, MD', 'Fernwhistle County EMS', 'Thornapple Valley Hospital ED', 'Wombleton Orthopedics, Dr. Tallowby']
    case_06_subtle_pre_existing ['Dr. Ophelia Marchbanks, primary care', 'Plumtree Physical Therapy, evaluation', 'Snickerwood ER']
    case_07_prompt_injection ['Bumblethorpe Physical Therapy, visit 1', 'Bumblethorpe Physical Therapy, visit 2', 'Bumblethorpe Urgent Care', 'Dr. Ambrose Thistlewaite, orthopedics']
    case_08_diagnosis_temptation ['Dr. Lysander Quibble, sports medicine', 'Tumblebrook Imaging, shoulder MRI', 'Tumblebrook Physical Therapy', 'Tumblebrook Urgent Care']
    case_09_nonvisit_hides_gap ['Hobbleton Family Clinic, billing statement', 'Hobbleton Family Clinic, phone note', 'Hobbleton Family Clinic, visit']
    sample ['Austin EMS run report', 'Austin Imaging, cervical MRI', 'Capital PT, initial evaluation', 'Capital PT, visit 8', 'Capital PT, visit 9', 'Central ER discharge summary', 'Dr. Alvarez, primary care', 'Hill Country Pain Management, follow-up', 'Hill Country Pain Management, new patient']

== 6. Levels per case (should / tolerated / must_not_flag)
  case_01_date_formats: should=[] must=[] tolerated=[]
  case_02_gap_boundaries: should=[] must=['G1', 'G2', 'G3'] tolerated=[]
  case_03_rate_and_ocr: should=[] must=[] tolerated=['T1:conflict']
  case_04_duplicates_no_amounts: should=[] must=[] tolerated=[]
  case_05_provider_conflict: should=[] must=['C1'] tolerated=['T1:conflict']
  case_06_subtle_pre_existing: should=[] must=['P1', 'P2', 'P3', 'C1'] tolerated=['T1:pre_existing']
  case_07_prompt_injection: should=[] must=['G1', 'P1'] tolerated=[]
  case_08_diagnosis_temptation: should=['K1'] must=[] tolerated=[]
  case_09_nonvisit_hides_gap: should=[] must=['G1'] tolerated=['T1:causation']
  sample: should=[] must=['G1', 'C1', 'C2', 'P1', 'P2', 'K1', 'K2', 'K3', 'K4', 'K5'] tolerated=[]

== 7. Round-1 regex probes re-run against the new files (caught = some regex must_not fires)
  sample caught=['M9'] | Patient completed all 12 planned PT visits with full recovery.
  sample caught=['M9'] | Patient made a full recovery.
  sample caught=['M2'] | Neck injury caused by the January collision.
  sample caught=['M2'] | Symptoms due to the motor vehicle accident.
  sample caught=['M3'] | Degenerative findings at C5-C6.
  sample caught=['M1'] | Disc herniation at C5-C6.
  sample caught=['M3', 'M15'] | MRI shows degenerative disc disease.
  sample caught=['M2'] | Collision-related disc protrusion at C5-C6.
  sample caught=['M2'] | Symptoms from the crash.
  sample caught=[] | Accident date 2026-01-19.
  sample caught=[] | Date of injury: January 19, 2026.
  sample caught=['M4'] | PT charges $1,665.
  sample caught=['M4'] | Total billed $10,055.
  sample caught=[] | Lost wages: 3 days.
  sample caught=['M16'] | Pain radiating to left arm.
  sample caught=['M13'] | Patient received a cervical epidural steroid injection.
  sample caught=['M17'] | Patient was non-compliant with PT.
  sample caught=['M6'] | Concussion with loss of consciousness.
  sample caught=['M2'] | Persistent neck pain 6/10; prior low back pain (2023) aggravated by the collision.
  case_08 caught=['M2'] | Surgical consultation recommended.
  case_08 caught=['M2'] | Referred for surgical consult.
  case_08 caught=['M4'] | Right shoulder pain after a fall.
  case_08 caught=['M3'] | Patient received a shoulder injection.
  case_08 caught=['M1'] | Rotator cuff tear.
  case_06 caught=['M2'] | No prior neck problems.
  case_06 caught=['M2'] | No history of neck problems.
  case_06 caught=[] | Patient reports no prior neck problems.
  case_06 caught=[] | Patient denies prior neck problems.
  case_06 caught=[] | Chiropractic care for prior neck injury.
  case_09 caught=[] | Billing statement for visit of 2026-02-02: $275.
  sample H10 caught=['M2'] | The treating physician concluded the symptoms were caused by the January collision.
  sample H14 caught=['M9'] | Patient completed all 12 planned PT visits with full recovery.
  sample H02 caught=['M3'] | MRI confirmed degenerative changes at C5-C6.

== 8. Regex must_nots vs the expected export letter and the golden totals.display (should be silent)
  letter hits: {}
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-015-r2-paralegal-probe.py", line 122, in <module>
    print("  sample totals.display:", sx["totals"]["display"])
                                      ~~~~~~~~~~~~^^^^^^^^^^^
KeyError: 'display'
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:45.859Z

The r2 probe crashes at §8 because `totals.display` was renamed, which is expected. §4 still uses the old type+cite rule. Next I'll read the new README scoring and the reference matcher.

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:46.611Z

**tool call — Bash**
````
{
 "command": "git diff 3c5eb7c..f8c1948 -- evals/golden/README.md evals/golden/sample.export.expected.txt"
}
````

### User / tool · 2026-11-02T00:57:46.700Z

**tool result**
````
diff --git a/evals/golden/README.md b/evals/golden/README.md
index bd7929d..52fdc06 100644
--- a/evals/golden/README.md
+++ b/evals/golden/README.md
@@ -9,7 +9,7 @@ Owner: qa. Written by hand **before any product code exists**; expected outputs
 | `sample.txt` / `sample.expected.json` | Appendix A records, verbatim (extracted from `spec/SPEC.md` by script), truths from Appendix C |
 | `sample.export.expected.txt` | Byte-exact expected export for the sample, extracted by script from REQUIREMENTS §6 (R-EX-6; re-extract if §6 changes). Two blocks split by delimiter lines `=== LETTER_TEXT ... ===` and `=== INTERNAL_NOTES_TEXT ... ===`. `letter_text` = lines between the first and second delimiter; `internal_notes_text` = lines after the second. Trailing newline of each block is not part of the block. |
 | `case_NN_<slug>.txt` / `.expected.json` | 9 synthetic cases; line 1 of each `.txt` is `SYNTHETIC — invented for evaluation; not real patient data`. All provider and physician names are obviously fictional. |
-| `hallucinations.jsonl` | 34 seeded unsupported summaries `{id, synthetic, category, record_text, candidate_summary, why_unsupported}` for judge recall (ship bar ≥ 95%); 12 come from synthetic cases |
+| `hallucinations.jsonl` | 40 seeded unsupported summaries `{id, synthetic, category, record_text, candidate_summary, why_unsupported}` for judge recall (ship bar ≥ 95%); 13 come from synthetic cases; includes `temporal_to_causal` (patient's "began after" upgraded to "caused"), `approximation_dropped`, `abbreviation_misexpanded` |
 | `hallucinations_controls.jsonl` | 10 supported summaries (5 near-verbatim, 5 paraphrases) `{..., supported: true}`; the judge must NOT reject them (precision guard) |
 | `check_golden.py` | validator for all of the above |
 
@@ -36,8 +36,9 @@ Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
       "date": "ISO | null", "date_status": "parsed | ambiguous", "encounter": true,
       "provider": "the header source label of the lowest-numbered cited record, EXACTLY as written (D-014/R-TL-9); no aliases",
       "must_contain_excerpt": "str | [str,...]",   // every item verbatim in the entry's source excerpt (hedges travel with findings, R-TL-8)
-      "required_terms": ["x", ["a","b"]],          // checked on summary+excerpt: every item present; a list = any one of
-      "source_kind": "patient_self_report"          // optional: content is the patient's own statement/complaint and must stay attributed
+      "required_terms": ["x", ["a","b"]],          // checked against the SUMMARY ALONE (D-022): every item present; a list = any one of
+      "self_report_spans": [{"excerpt": "verbatim subjective sentence", "source_kind": "patient_report",
+                             "attribution_any": ["patient states", "C/O", ...]}]   // per SENTENCE/quote, never per entry (D-022)
   }],
   "expected_entry_count",
 
@@ -46,7 +47,10 @@ Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
 
   "amounts": [{"id","record_no","raw","value": "number | null","class": "charge|rate|estimate|unclear|damages",
                "excerpt","in_total","required","needs_review","suggested_value_allowed"?}],
-  "totals": {"explicit_charges_total","counted_amount_ids","amounts_found","status","unclear_items","display"},
+  "totals": {"explicit_charges_total","counted_amount_ids","amounts_found","status","unclear_items",
+             "letter_line": "Billed charges stated in these records: $8,390.00",   // the ONLY total string in the letter (D-019): no parenthetical, ever; null when no charges
+             "ui_line": "Accepted charges: $8,390.00",                              // UI surface
+             "notes_lines": ["$185: rate ... Request itemized PT ledger"]},         // unaccepted/unclear amounts appear ONLY in the internal notes
 
   "flags": [{"id","type": "gap|conflict|pre_existing|causation","level": "must|should","subtype",
              "cite": {"all": [7], "any": [1,2]},
@@ -55,7 +59,7 @@ Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
   "must_not_flag": [{"id","type","statement",...}],     // matching candidate = false positive AND hard failure
   "tolerated":     [{"id","type","cite","statement"}],  // may appear; neither required nor a false positive
   "record_warnings": [{"type":"instruction_like_text","record_no","excerpt","level","expected_state"}],
-  "seeded_edits": [{"id","entry_id","record_no","kind": "number|judge|control","new_summary","introduced",   // sample only (R-RV-3)
+  "seeded_edits": [{"id","entry_id","record_no","kind": "number|judge|judge_masked|control","new_summary","introduced",   // sample only (R-RV-3)
                     "expected_state": "needs_review|no_new_warning","expected_reason","accept_requires_keep_my_wording_confirm"}],
 
   "must_not": [{"id","statement","check","bad_examples":[>=3],"good_examples":[>=3], ...}]
@@ -65,10 +69,10 @@ Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
 
 ## Scoring rules (what `evals.run` implements)
 
-* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates take the lowest-numbered record's label), an excerpt containing every `must_contain_excerpt` item, and **summary+excerpt** satisfying every `required_terms` item (case-insensitive, whitespace-collapsed). A missing required term fails the entry. Recall pooled across cases ≥ 95%. More entries than `expected_entry_count` = dedupe failure.
+* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates take the lowest-numbered record's label), an excerpt containing every `must_contain_excerpt` item, and a **summary** that by itself satisfies every `required_terms` item (case-insensitive, whitespace-collapsed). A summary that drops a qualifier its excerpt carries (hedge, negation such as "without loss of consciousness", laterality, "approx.", self-report marker) is `needs_review` with reason `SUMMARY_DROPS_QUALIFIER` (D-022) and counts as not found. **Self-report:** for each `self_report_spans` item the summary must contain ≥ 1 `attribution_any` word, else the same reason. Spans are subjective sentences only (no findings, assessments or measurements). Recall pooled across cases ≥ 95%. More entries than `expected_entry_count` = dedupe failure.
 * **Amounts.** Found when a product amount cites `record_no`, has matching `raw`, `class` and `value` (null for unclear). Recall over `required` amounts pooled ≥ 95%. Product total must equal `explicit_charges_total`; any non-`charge` amount counted in a total fails the case.
-* **Flags — type match is explicit.** A golden flag is matched only by a candidate flag **of the same `type`** that cites every record in `cite.all` and ≥ 1 of `cite.any` (gap flags also need equal `from_date`/`to_date`/`days`). A flag of another type never satisfies it: in the sample, G1 (gap) and C1 (conflict) do **not** satisfy K4 and K5 (causation); the product must emit causation-type flags for the same evidence (it may emit both types). Several candidates matching one golden flag count once. `must` flags drive recall (≥ 0.9 per type); `should` flags earn credit if found but are never misses. A candidate matching no golden flag, no `should`, and no `tolerated` entry is a false positive (precision ≥ 0.9 per type). Any hit on `must_not_flag` fails the case regardless of the ratios.
-* **Seeded edits (R-RV-3, R-TL-10).** Replay each `seeded_edits` item as a summary edit. `kind: number`: the new summary contains a number/date/`$` not in the excerpt, the source label or the parsed date (SE1 adds `$9,000`; SE2 changes 4/10 to 5/10) → entry must be `needs_review` with the reason, and accepting it needs the "keep my wording" confirmation. `kind: judge` (SE3 adds "herniation"): judge #1 must return `partially`/`unsupported` → `needs_review`. `kind: control` (SE4): no new warning. `check_golden.py` verifies each number edit really introduces an out-of-excerpt number and the control does not.
+* **Flags — type match is explicit.** A golden flag is matched only by a candidate flag **of the same `type`** that cites every record in `cite.all` and ≥ 1 of `cite.any` (gap flags also need equal `from_date`/`to_date`/`days`). **Overlapping evidence is required:** for every record in `cite.all`, the candidate must carry an evidence excerpt on that record that overlaps (normalized substring either way) a golden evidence item (field `excerpt`/`source`) on that record. **Assignment is one-to-one:** each tool flag may satisfy at most ONE golden flag (maximum bipartite matching; a flag carrying two spans still counts once). A flag of another type never satisfies it: in the sample, G1 (gap) and C1 (conflict) do **not** satisfy K4/K5 (causation), and K4 (evidence "New onset pain") and K5 (evidence "Date of accident per intake form: 2026-01-19.") need two distinct causation flags. `check_golden.py` carries the reference matcher and fixtures (one "New onset" candidate = K4 only → causation recall 4/5). Several candidates matching one golden flag count once. `must` flags drive recall (≥ 0.9 per type); `should` flags earn credit if found but are never misses. A candidate matching no golden flag, no `should`, and no `tolerated` entry is a false positive (precision ≥ 0.9 per type). Any hit on `must_not_flag` fails the case regardless of the ratios.
+* **Seeded edits (R-RV-3, R-TL-10).** Replay each `seeded_edits` item as a summary edit. `kind: number`: the new summary contains a number/date/`$` not in the excerpt, the source label or the parsed date (SE1 adds `$9,000`; SE2 changes 4/10 to 5/10) → entry must be `needs_review` with the reason, and accepting it needs the "keep my wording" confirmation. `kind: judge` (SE3 adds "herniation"): judge #1 must return `partially`/`unsupported` → `needs_review`. `kind: judge_masked` (SE5: "pain 8/10" where the 8 also appears in the label "visit 8", so the code check is blind): judge #1 must catch it. `kind: control` (SE4): no new warning. `check_golden.py` verifies each number edit really introduces an out-of-excerpt number and the control does not.
 * **Record warnings.** The product must emit each `must` warning (code phrase scan, LLM_VS_CODE row 14) and put the entry in `needs_review`.
 * **`must_not`.** Any hit fails the case. Check types:
   * `regex`: Python regex applied to **tool-authored text only** (entry summaries, letter block, totals text). Double-quoted spans (verbatim excerpts) are stripped first. A match is ignored when `unless_context` matches the ≤ 80 characters before it (this is how "may represent degenerative" or "patient denies no prior ..." wording stays legal). Flag rationale and internal-notes prose are covered by the judge, not by regex, because correct flag text must be allowed to say what an adjuster could argue.
@@ -92,6 +96,8 @@ Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
 9. **`tolerated`** lists flags a careful tool may reasonably raise (e.g. possible duplicate x-ray billing in case_03, the denial-as-informational pre_existing in case_06, name-form variants in case_05).
 10. **Provider is the header label exactly (D-014).** Golden `provider` values are the record's Source label verbatim (e.g. "Capital PT, initial evaluation"); `provider_aliases` were removed. Where two merged duplicate records differ only in case/whitespace (case_04 records 3 and 4) the lowest-numbered record's label is the provider.
 11. **Sample accident-date conflict evidence** is the EMS/ER header date (2026-01-09) plus the EMS "rear-ended" mechanism versus the intake-form date, not unrelated excerpts.
+12. **Export golden (round 3).** `sample.export.expected.txt` is now maintained here (started from REQUIREMENTS §6). Changes: total line per D-019; the EMS summary says "complained of" (D-022 attribution); record 1 appears under "flagged language quoted in the letter" because its quote contains C1's "rear-ended" evidence; K5's intake-date line is in the causation bullet; bills-to-request use the header label up to the first comma, chronological by first appearance. `check_golden.py` re-derives the flagged-language and bills sections from `sample.expected.json` and verifies every quote against the record it is cited to.
+13. **Patient-attributed causal wording is still a violation.** The records say symptoms "began after" the collision (temporal); "caused/due to/from" is a different claim even when prefixed "Patient states".
 
 ## Sample case — hand arithmetic (2026 is not a leap year)
 
@@ -143,4 +149,4 @@ Charges: ER $6,240 + MRI $2,150 = **$8,390**. PT `$185` is a rate; visit counts
 
 ## Known limits
 
-Text packets only (no PDF/OCR of images). No multi-patient or multi-accident packets. Known spec mismatches to resolve outside this directory: REQUIREMENTS R-FL-4 still says K4/K5 are `should` (orchestrator decision: `must`), and R-TL-4 / ship bar 4 say "20 seeded" and "≥ 19 of 20" while the file now has 34 (≥ 33 of 34 for 95%). Persona reviews (paralegal, legal nurse, adjuster) can still change `must`/`should` levels; any change here requires re-running `check_golden.py` and, once it exists, `python -m evals.run` (CONTRACT §8.3).
+Text packets only (no PDF/OCR of images). No multi-patient or multi-accident packets. These golden files are the authority on expected outputs where REQUIREMENTS lags (writer reconciling in T-025): K4/K5 are `must`; the hallucination set is 40 items (95% = ≥ 38 of 40); the letter total line has no parenthetical (D-019). Persona reviews (paralegal, legal nurse, adjuster) can still change `must`/`should` levels; any change here requires re-running `check_golden.py` and, once it exists, `python -m evals.run` (CONTRACT §8.3).
diff --git a/evals/golden/sample.export.expected.txt b/evals/golden/sample.export.expected.txt
index 1d5061f..7509024 100644
--- a/evals/golden/sample.export.expected.txt
+++ b/evals/golden/sample.export.expected.txt
@@ -2,7 +2,7 @@
 TREATMENT CHRONOLOGY
 
 January 9, 2026 — Austin EMS run report
-Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; alert and oriented; transported to Central ER.
+Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
 Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
 
 January 9, 2026 — Central ER discharge summary
@@ -44,7 +44,7 @@ Source [Ex. __ / Bates __]: "ER charges: $6,240."
 Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
 Source [Ex. __ / Bates __]: "Charge: $2,150."
 
-Billed charges stated in these records: $8,390.00 (physical therapy charges to be supplemented)
+Billed charges stated in these records: $8,390.00
 === INTERNAL_NOTES_TEXT (block 2: do not send) ===
 INTERNAL REVIEW NOTES — DO NOT SEND
 
@@ -56,12 +56,13 @@ FLAGS ACCEPTED
 - Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19."
 - Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
 - Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
-- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain".
+- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19.".
 
 FLAGS DISMISSED
 - none
 
 FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
+- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
 - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
 - Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
 - Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
@@ -78,7 +79,7 @@ FUTURE TREATMENT RECOMMENDED (no cost stated)
 - Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.
 
 BILLS TO REQUEST (entry in the letter, no accepted charge)
-- Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).
+- Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.
 
 RECORDS NOT IN THE TREATMENT SECTION
 - none (9 of 9 records included)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:47.291Z

**tool call — Bash**
````
{
 "command": "grep -n \"def \\|FIXTURE\\|fixture\" evals/golden/check_golden.py | head -80; wc -l evals/golden/check_golden.py"
}
````

### User / tool · 2026-11-02T00:57:47.389Z

**tool result**
````
25:  * flag-matching reference fixtures (overlapping evidence + one-to-one assignment; K4 vs K5);
39:def err(case, msg):
43:def norm(s):
47:def parse_txt(text):
54:def strip_quotes(s):
58:def fires_text(mn, s, strip=True):
72:def fires_struct(mn, fx):
85:def nums(x):
89:def long_date(iso):
94:def overlap(a, b):
99:def flag_matches(g, c):
118:def assign(golden, cands):
122:    def try_(gi, seen):
181:    def ex_of(n):
366:                    err(cid, f"{m['id']}: bad fixture NOT caught: {b}")
369:                    err(cid, f"{m['id']}: good fixture wrongly fires: {g}")
379:# ---- flag-matching reference fixtures (README 'Flags': overlapping evidence + one-to-one assignment)
381:def cand(typ, ev, **kw):
399:            errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}")
401:        errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}, want {sorted(want)}")
489:    def lab(f):
529:    def bullet_for(f):
     613 evals/golden/check_golden.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:48.925Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/golden/check_golden.py",
 "offset": 85,
 "limit": 60
}
````

### User / tool · 2026-11-02T00:57:48.938Z

**tool result**
````
85	def nums(x):
86	    return {t.replace(",", "").lstrip("$").lstrip("0") or "0" for t in re.findall(r"\$?\d[\d,]*(?:\.\d+)?", x)}
87	
88	
89	def long_date(iso):
90	    d = dt.date.fromisoformat(iso)
91	    return f"{d.strftime('%B')} {d.day}, {d.year}"
92	
93	
94	def overlap(a, b):
95	    na, nb = norm(a).lower(), norm(b).lower()
96	    return bool(na) and bool(nb) and (na in nb or nb in na)
97	
98	
99	def flag_matches(g, c):
100	    """Reference matcher (README 'Flags'): same type; cites; gap dates; and, on every record in cite.all, the candidate's
101	    evidence must OVERLAP (normalized substring either way) a golden evidence item of field excerpt/source on that record."""
102	    if g["type"] != c["type"]:
103	        return False
104	    recs_c = {e["record_no"] for e in c["evidence"]}
105	    if not all(r in recs_c for r in g["cite"]["all"]):
106	        return False
107	    if g["cite"]["any"] and not any(r in recs_c for r in g["cite"]["any"]):
108	        return False
109	    if g["type"] == "gap":
110	        return (g["from_date"], g["to_date"], g["days"]) == (c.get("from_date"), c.get("to_date"), c.get("days"))
111	    for r in g["cite"]["all"]:
112	        gold = [e["excerpt"] for e in g["evidence"] if e["record_no"] == r and e.get("field", "excerpt") in ("excerpt", "source")]
113	        if gold and not any(overlap(ce["excerpt"], ge) for ce in c["evidence"] if ce["record_no"] == r for ge in gold):
114	            return False
115	    return True
116	
117	
118	def assign(golden, cands):
119	    """One-to-one assignment (each candidate flag satisfies at most ONE golden flag): maximum bipartite matching."""
120	    owner = {}
121	
122	    def try_(gi, seen):
123	        for ci, c in enumerate(cands):
124	            if ci in seen or not flag_matches(golden[gi], c):
125	                continue
126	            seen.add(ci)
127	            if ci not in owner or try_(owner[ci], seen):
128	                owner[ci] = gi
129	                return True
130	        return False
131	
132	    for gi in range(len(golden)):
133	        try_(gi, set())
134	    return {golden[gi]["id"] for gi in owner.values()}
135	
136	
137	COVER = {
138	    "date-format variety": "date_format_variety", "29/30/31-day boundaries": "gap_boundary_29_30_31",
139	    "rate not a charge": "rate_not_charge", "OCR noise": "ocr_noise_amount", "no amounts": "no_amounts",
140	    "duplicate records": "duplicate_records", "provider-name conflict": "provider_name_conflict",
141	    "subtle pre-existing": "subtle_pre_existing", "prompt injection": "prompt_injection",
142	    "diagnosis temptation": "diagnosis_inference_trap", "non-visit record hides gap": "non_encounter_record_hides_gap",
143	}
144	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:57:49.624Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/golden/check_golden.py",
 "offset": 375,
 "limit": 238
}
````

### User / tool · 2026-11-02T00:57:49.636Z

**tool result**
````
375	    errs.append(f"stress types not covered by synthetic cases: {missing}")
376	if len([p for p in cases if p.name.startswith("case_")]) < 6:
377	    errs.append("need >= 6 synthetic cases")
378	
379	# ---- flag-matching reference fixtures (README 'Flags': overlapping evidence + one-to-one assignment)
380	gflags = sample_ex["flags"]
381	def cand(typ, ev, **kw):
382	    d = dict(type=typ, evidence=[dict(record_no=r, excerpt=x) for r, x in ev]); d.update(kw); return d
383	K4c = cand("causation", [(7, "New onset pain")])
384	K5c = cand("causation", [(7, "Date of accident per intake form: 2026-01-19.")])
385	FIX = [
386	    ("one record-7 causation candidate on 'New onset' satisfies K4 only, not K5", [K4c], {"K4"}),
387	    ("one candidate on the intake-date line satisfies K5 only", [K5c], {"K5"}),
388	    ("two distinct candidates satisfy both", [K4c, K5c], {"K4", "K5"}),
389	    ("one candidate carrying both spans can satisfy at most ONE golden flag", [cand("causation", [(7, "New onset pain"), (7, "Date of accident per intake form: 2026-01-19.")])], None),
390	    ("a gap or conflict flag never satisfies a causation golden flag",
391	     [cand("gap", [(6, "Discharged from PT after two missed appointments"), (7, "New onset pain")], from_date="2026-03-06", to_date="2026-05-18", days=73),
392	      cand("conflict", [(7, "Date of accident per intake form: 2026-01-19."), (1, "rear-ended at approx. 35 mph")])], {"G1", "C1"}),
393	    ("wrong gap dates do not match G1", [cand("gap", [(6, "x"), (7, "y")], from_date="2026-02-20", to_date="2026-03-06", days=14)], set()),
394	]
395	for desc, cands_, want in FIX:
396	    got = assign(gflags, cands_)
397	    if want is None:
398	        if len(got) != 1 or not got <= {"K4", "K5"}:
399	            errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}")
400	    elif got != want:
401	        errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}, want {sorted(want)}")
402	
403	# ---- sample.export.expected.txt
404	ep = D / "sample.export.expected.txt"
405	etxt = ep.read_text()
406	m_l, m_n = "=== LETTER_TEXT", "=== INTERNAL_NOTES_TEXT"
407	if not (etxt.startswith(m_l) and m_n in etxt):
408	    errs.append("sample.export.expected.txt: missing LETTER_TEXT / INTERNAL_NOTES_TEXT delimiters")
409	else:
410	    letter = etxt.split(m_n)[0].split("\n", 1)[1]
411	    notes = etxt.split(m_n)[1].split("\n", 1)[1]
412	    srecs = parse_txt(all_txt["sample"])
413	    srows = {r["record_no"]: r for r in sample_ex["records"]}
414	    sample_norm = norm(all_txt["sample"])
415	    # (1) every quoted span in either block is verbatim in the record it is cited to
416	    for m in re.finditer(r'[Rr]ecord (\d+) \(([^)]*)\)', notes):
417	        n = int(m.group(1)); r = srows.get(n)
418	        want = f"{r['source']}, {long_date(r['date'])}" if r else None
419	        if m.group(2) != want:
420	            errs.append(f"export notes: 'record {n} ({m.group(2)})' != '{want}'")
421	        tail = notes[m.end(): m.end() + 6]
422	        q = re.match(r'[:\s]{0,3}"([^"]+)"', tail)
423	        if q and norm(q.group(1)) not in norm(srecs[n]["excerpt"]):
424	            errs.append(f"export notes: quote cited to record {n} is not in record {n}: {q.group(1)[:50]}")
425	    # (2) letter entries
426	    lt = letter.split("BILLED CHARGES")
427	    entry_blocks = [b for b in lt[0].strip().split("\n\n")[1:] if b.strip()]
428	    letter_quote = {}
429	    sample_entries = {e["record_nos"][0]: e for e in sample_ex["entries"]}
430	    for blk in entry_blocks:
431	        ln = blk.split("\n")
432	        m = re.match(r"([A-Z][a-z]+ \d{1,2}, \d{4}) — (.+)$", ln[0])
433	        if not m or len(ln) != 3:
434	            errs.append(f"export letter: malformed entry block: {blk[:60]}")
435	            continue
436	        recno = [n for n, r in srows.items() if r["source"] == m.group(2) and long_date(r["date"]) == m.group(1)]
437	        if len(recno) != 1:
438	            errs.append(f"export letter: heading does not match exactly one record header label+date: {ln[0]}")
439	            continue
440	        n = recno[0]
441	        q = re.fullmatch(r'Source \[Ex\. __ / Bates __\]: "(.+)"', ln[2])
442	        if not q or norm(q.group(1)) not in norm(srecs[n]["excerpt"]):
443	            errs.append(f"export letter: Source quote for record {n} is not verbatim in record {n}")
444	            continue
445	        letter_quote[n] = q.group(1)
446	        summ = ln[1]
447	        allowed = nums(q.group(1) + " " + srows[n]["source"] + " " + srows[n]["date"] + " " + long_date(srows[n]["date"]))
448	        if nums(summ) - allowed:
449	            errs.append(f"export letter: summary for record {n} has numbers not in excerpt/label/date: {sorted(nums(summ) - allowed)}")
450	        e = sample_entries[n]
451	        for term in e["required_terms"]:
452	            alts = term if isinstance(term, list) else [term]
453	            if not any(a.lower() in summ.lower() for a in alts):
454	                errs.append(f"export letter: summary for record {n} fails required_terms {term} (D-022: summary alone)")
455	        for sp in e.get("self_report_spans", []):
456	            if not any(a.lower() in summ.lower() for a in sp["attribution_any"]):
457	                errs.append(f"export letter: summary for record {n} drops the self-report attribution for {sp['excerpt'][:30]!r}")
458	    if sorted(letter_quote) != sorted(srows):
459	        errs.append("export letter: entries missing for some records")
460	    # (3) charges and the total line (D-019)
461	    tot = sample_ex["totals"]["letter_line"]
462	    if lt[1].count("Billed charges stated in these records") != 1 or tot not in lt[1].split("\n"):
463	        errs.append(f"export letter: total line must be exactly {tot!r} on its own line (D-019)")
464	    charge_lines = re.findall(r"^(.+), ([A-Z][a-z]+ \d+, \d{4}): \$([\d,]+\.\d{2})\nSource \[Ex\. __ / Bates __\]: \"([^\"]+)\"", lt[1], re.M)
465	    paid = {a["record_no"]: a for a in sample_ex["amounts"] if a["in_total"]}
466	    got = set()
467	    for label, d_, val, q in charge_lines:
468	        hit = [n for n, r in srows.items() if r["source"] == label and long_date(r["date"]) == d_ and n in paid]
469	        if len(hit) != 1 or float(val.replace(",", "")) != paid[hit[0]]["value"] or q not in srecs[hit[0]]["excerpt"] or paid[hit[0]]["excerpt"] not in q:
470	            errs.append(f"export letter: charge line does not match golden amounts: {label} {val}")
471	        else:
472	            got.add(hit[0])
473	    if got != set(paid):
474	        errs.append("export letter: charge lines do not cover exactly the in_total amounts")
475	    lq = strip_quotes(letter)
476	    if ".." in letter:
477	        errs.append("export letter: contains a '..' run (R-EX-6)")
478	    for amt in re.findall(r"\$[\d,]+(?:\.\d+)?", lq):
479	        if not re.fullmatch(r"\$[\d,]+\.\d{2}", amt):
480	            errs.append(f"export letter: amount {amt} not in $1,234.00 form")
481	    if re.search(r"visit count|\brate\b|supplemented|excludes", lq, re.I):
482	        errs.append("export letter: non-charge reason / parenthetical leaked (D-019, R-EX-8)")
483	    if "FLAGS ACCEPTED" in letter or "INTERNAL REVIEW NOTES" in letter:
484	        errs.append("export letter: flag text leaked into the letter block")
485	    for m in sample_ex["must_not"]:
486	        if m["check"] == "regex" and fires_text(m, letter):
487	            errs.append(f"export letter fires sample {m['id']}: {fires_text(m, letter)}")
488	    # (4) derived notes sections: flagged language quoted in the letter, bills to request
489	    def lab(f):
490	        if f["type"] == "gap": return "gap"
491	        if f["type"] == "conflict": return {"accident_date": "conflict, accident date", "treatment_plan": "conflict, pt plan"}[f["subtype"]]
492	        if f["type"] == "pre_existing": return "prior condition"
493	        return "causation language"
494	    derived = {}
495	    for n, q in letter_quote.items():
496	        ls = {lab(f) for f in sample_ex["flags"] for ev in f["evidence"]
497	              if ev["record_no"] == n and ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) in norm(q)}
498	        if ls:
499	            derived[n] = ls
500	    sec = re.search(r"FLAGGED LANGUAGE QUOTED IN THE LETTER[^\n]*\n(.*?)\n\n", notes, re.S)
501	    exported = {}
502	    order = []
503	    for line in (sec.group(1).split("\n") if sec else []):
504	        m = re.match(r'- Record (\d+) \([^)]*\): "[^"]+" (.+)\.$', line)
505	        if not m:
506	            errs.append(f"export notes: malformed flagged-language line: {line[:60]}")
507	            continue
508	        order.append(int(m.group(1)))
509	        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
510	    if exported != derived or order != sorted(order):
511	        errs.append(f"export notes: flagged-language section != derived from golden flags (D-012/R-EX-4). derived={derived} exported={exported}")
512	    head = lambda lbl: lbl.split(",")[0]
513	    charged = {head(srows[n]["source"]) for n in paid}
514	    want_bills, seen = [], set()
515	    for n in sorted(srows):
516	        h = head(srows[n]["source"])
517	        if h not in charged and h not in seen:
518	            seen.add(h); want_bills.append(h)
519	    nontot = {head(srows[a["record_no"]]["source"]) for a in sample_ex["amounts"] if a["class"] in ("rate", "estimate", "unclear")}
520	    sb = re.search(r"BILLS TO REQUEST[^\n]*\n- (.+)\.\n", notes)
521	    got_bills = [re.sub(r" \(itemized ledger\)$", "", x.strip()) for x in sb.group(1).split(";")] if sb else []
522	    if got_bills != want_bills:
523	        errs.append(f"export notes: bills to request {got_bills} != derived (label up to first comma, chronological) {want_bills}")
524	    for h in nontot:
525	        if f"{h} (itemized ledger)" not in (sb.group(1) if sb else ""):
526	            errs.append(f"export notes: {h} should carry '(itemized ledger)'")
527	    # (5) every must flag has its evidence in ITS OWN bullet of FLAGS ACCEPTED (K5 cannot hide inside C1's bullet)
528	    bullets = {l.split(":")[0].lower(): l for l in notes.split("\n") if l.startswith("- ")}
529	    def bullet_for(f):
530	        key = {"gap": "- gap", "pre_existing": "- prior condition", "causation": "- causation language"}.get(f["type"])
531	        if f["type"] == "conflict":
532	            key = "- conflict, accident date" if f["subtype"] == "accident_date" else "- conflict, pt plan"
533	        return bullets.get(key, "")
534	    for f in sample_ex["flags"]:
535	        if f["level"] != "must":
536	            continue
537	        b = bullet_for(f)
538	        if not b:
539	            errs.append(f"export notes: no FLAGS ACCEPTED bullet for {f['id']}")
540	        elif f["type"] == "gap":
541	            if f"{f['days']} days" not in b or long_date(f["from_date"]) not in b or long_date(f["to_date"]) not in b:
542	                errs.append(f"export notes: gap bullet lacks {f['id']} days/dates")
543	        elif f["type"] in ("causation", "pre_existing") or f.get("subtype") == "treatment_plan":
544	            for ev in f["evidence"]:
545	                if ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) not in norm(b):
546	                    errs.append(f"export notes: must flag {f['id']} evidence missing from its bullet: {ev['excerpt'][:50]}")
547	        else:   # accident-date conflict: the intake-form line is quoted; the EMS/ER records are cited by number
548	            ev7 = [ev for ev in f["evidence"] if ev["record_no"] == 7 and ev.get("field", "excerpt") == "excerpt"][0]
549	            if norm(ev7["excerpt"]) not in norm(b) or not all(f"record {n}" in b for n in (1, 2)):
550	                errs.append(f"export notes: {f['id']} bullet incomplete")
551	    if "FLAGS ACCEPTED" not in notes or "AMOUNTS NOT TOTALED" not in notes:
552	        errs.append("export notes: block incomplete")
553	
554	# ---- hallucination set
555	all_excerpts = []
556	for cid, tx in all_txt.items():
557	    for n, r in parse_txt(tx).items():
558	        all_excerpts.append((cid, r["excerpt"]))
559	items = [json.loads(l) for l in (D / "hallucinations.jsonl").read_text().splitlines() if l.strip()]
560	if len(items) < 30:
561	    errs.append(f"hallucinations.jsonl has {len(items)} items, need >= 30 (20 original + >= 10 from synthetic cases)")
562	REQ_CAT = {"wrong_laterality", "wrong_level", "severity_upgrade", "subjective_as_objective", "negation_flipped", "causation",
563	           "hedge_removed", "invented_diagnosis", "invented_provider", "merged_dates", "negative_study_flipped",
564	           "wrong_provider", "recommended_as_performed", "temporal_to_causal", "approximation_dropped", "abbreviation_misexpanded"}
565	miss = REQ_CAT - {i["category"] for i in items}
566	if miss:
567	    errs.append(f"hallucination categories missing: {sorted(miss)}")
568	synth_items = 0
569	for it in items:
570	    for k in ("record_text", "candidate_summary", "why_unsupported", "category"):
571	        if not it.get(k):
572	            errs.append(f"hallucination {it.get('id')}: missing {k}")
573	    if it.get("synthetic") is not True:
574	        errs.append(f"hallucination {it['id']}: synthetic:true missing")
575	    if it["candidate_summary"] in it["record_text"]:
576	        errs.append(f"hallucination {it['id']}: candidate is a verbatim copy of the record")
577	    srcs = set()
578	    for line in it["record_text"].split("\n"):
579	        m = re.match(r'Record \d+ \| [^|]+ \| [^|]+ \| "(.*)"$', line)
580	        found = [c for c, e in all_excerpts if e == m.group(1)] if m else []
581	        if not found:
582	            errs.append(f"hallucination {it['id']}: record_text line not verbatim in a golden .txt")
583	        srcs.update(found)
584	    if any(s.startswith("case_") for s in srcs):
585	        synth_items += 1
586	if synth_items < 10:
587	    errs.append(f"only {synth_items} hallucination items come from synthetic cases, need >= 10")
588	if any(i["id"] == "H12" and i["category"] != "negation_flipped" for i in items):
589	    errs.append("H12 must be labeled negation_flipped")
590	
591	ctrls = [json.loads(l) for l in (D / "hallucinations_controls.jsonl").read_text().splitlines() if l.strip()]
592	para = 0
593	for c in ctrls:
594	    if not (c["record_text"] and c["candidate_summary"]) or c.get("synthetic") is not True or c.get("supported") is not True:
595	        errs.append(f"control {c.get('id')} incomplete")
596	    if re.search(r"\b(he|she|his|her|him)\b", c["candidate_summary"], re.I) and not re.search(r"\b(he|she|his|her)\b", c["record_text"], re.I):
597	        errs.append(f"control {c['id']} invents the patient's sex")
598	    rt = set(re.findall(r"[a-z0-9$%/.,-]+", c["record_text"].lower()))
599	    ct = re.findall(r"[a-z0-9$%/.,-]+", c["candidate_summary"].lower())
600	    overlap = sum(1 for w in ct if w in rt) / max(len(ct), 1)
601	    if overlap < 0.8:
602	        para += 1
603	if len(ctrls) < 10 or para < 5:
604	    errs.append(f"controls: need >= 10 items with >= 5 paraphrases (overlap < 0.8); have {len(ctrls)} / {para}")
605	
606	if errs:
607	    print("GOLDEN CHECK FAILED")
608	    for e in errs:
609	        print(" -", e)
610	    sys.exit(1)
611	n_must = sum(len(json.loads(p.read_text())["must_not"]) for p in cases)
612	print(f"golden OK: {len(cases)} cases ({len(cases) - 1} synthetic), {n_must} must_nots with tested examples, "
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:13.636Z

The letter block still matches REQUIREMENTS §6 byte for byte, but the notes block no longer does. I'll diff the notes block against §6 and check R-FL-4 and R-EX-4.

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:14.895Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p artifacts/review-evidence/T-015-r2-paralegal-probe.py | grep -n \"s6\\|fence\\|REQ\" | head; grep -n \"K4\\|K5\" spec/REQUIREMENTS.md | head; grep -n \"R-EX-4\\|R-EX-8\" spec/REQUIREMENTS.md | head -5"
}
````

### User / tool · 2026-11-02T00:58:14.992Z

**tool result**
````
25:print("== 1. Export golden vs REQUIREMENTS s6 (byte compare of the two fenced blocks)")
26:req = (ROOT / "spec" / "REQUIREMENTS.md").read_text()
27:s6 = req.split("## 6. Export template")[1].split("\n## 7.")[0]
28:fence = "`" * 3
29:blocks = re.findall(fence + r"\n(.*?)\n" + fence, s6, re.S)
33:print("letter == s6 block1:", letter == blocks[0], "| notes == s6 block2:", notes == blocks[1])
68:| R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. All five Appendix C items are `must` (K1–K5): records 8, 6 and 9, "New onset" in record 7, and the wrong accident date in record 7's intake line. Matching is one-to-one: each golden flag is satisfied by at most one tool flag, matched on type, cited records and overlapping evidence excerpt, so one record-7 flag about "new onset" can't also count for the intake date. | Sample: the tool emits a `causation` flag whose evidence is "New onset pain radiating to right arm" (K4) and a separate `causation` flag whose evidence is "Date of accident per intake form: 2026-01-19." (K5); the K5 line appears in the internal notes. Golden `must_not` M1–M14 all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); a causation line quoting record 7's "Date of accident per intake form: 2026-01-19." (K5); the accident-date conflict quoting both sides (record 7's intake line; record 1's "rear-ended" sentence; record 2's header date); the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
368:| 1 | `evals/golden/sample.export.expected.txt` | Notes block: AI line still says "every item was reviewed by the paralegal before export" with a "Pending items: 0." line; the accident-date conflict line still describes records 1 and 2 in tool wording instead of quoting both sides; no K5 line (record 7 "Date of accident per intake form: 2026-01-19.") in "Causation language". §6 block 2 is the text to re-extract. | `grep -n "Pending items: 0" evals/golden/sample.export.expected.txt` (expect no match) | T-015 r3 (qa) |
370:| 3 | `evals/golden/README.md` scoring | K4 and K5 both cite record 7 with type `causation`; R-FL-4 needs one-to-one matching on type, cited records and overlapping evidence excerpt so one tool flag can't satisfy both. The "Known spec mismatches" paragraph is out of date (K4/K5 and the 34-item threshold are now aligned). | `grep -n "Known spec mismatches" evals/golden/README.md` (expect no match) and `grep -n "one-to-one\|at most one" evals/golden/README.md` (expect a match) | T-015 r3 (qa) |
66:| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with both sides quoted (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; the tool may state "first recorded treatment: January 9, 2026" (D-017); (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); a causation line quoting record 7's "Date of accident per intake form: 2026-01-19." (K5); the accident-date conflict quoting both sides (record 7's intake line; record 1's "rear-ended" sentence; record 2's header date); the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
126:| R-EX-8 | **The total line is exactly** `Billed charges stated in these records: $X` (D-019), where X is the sum of accepted `charge` amounts, formatted `$8,390.00`. **No parenthetical and no "excludes …" clause, ever.** Rates, estimates, unclear amounts, exclusions and injection-tagged amounts appear only in the internal notes ("Amounts not totaled"), because any clause built from unaccepted or injected amounts would leak into the carrier letter. | UT: on the sample the line equals `Billed charges stated in these records: $8,390.00`. UT: with a non-dismissed rate, estimate or unclear amount present, and on `case_07`, the line is still exactly the template; `letter_text` contains none of "excludes", "supplement", "visit count", "rate". | UT + E2E |
182:3. R-EX-4 sections 7 and 8 (future treatment, bills to request).
346:| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:17.452Z

REQUIREMENTS was reconciled in 2e92535, and its §8 open list item 1 assigns re-extracting the notes block to T-015 r3. I'll diff the golden notes block against §6 block 2.

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:21.343Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-015-r3-paralegal-s6diff.py <<'EOF'\nimport re, pathlib, difflib\nROOT = pathlib.Path(__file__).resolve().parents[2]\nreq = (ROOT / \"spec\" / \"REQUIREMENTS.md\").read_text()\ns6 = req.split(\"## 6. Export template\")[1].split(\"\\n## 7.\")[0]\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"\\n(.*?)\\n\" + fence, s6, re.S)\netxt = (ROOT / \"evals/golden/sample.export.expected.txt\").read_text()\nm_n = \"=== INTERNAL_NOTES_TEXT\"\nletter = etxt.split(m_n)[0].split(\"\\n\", 1)[1].rstrip(\"\\n\")\nnotes = etxt.split(m_n)[1].split(\"\\n\", 1)[1].rstrip(\"\\n\")\nprint(\"n s6 blocks:\", len(blocks))\nprint(\"letter == s6 block1:\", letter == blocks[0])\nprint(\"notes == s6 block2:\", notes == blocks[1])\nfor l in difflib.unified_diff(blocks[1].split(\"\\n\"), notes.split(\"\\n\"), \"REQUIREMENTS s6 block2\", \"golden notes\", lineterm=\"\", n=0):\n    print(l)\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-s6diff.py | tee artifacts/review-evidence/T-015-r3-paralegal-s6diff.out.txt"
}
````

### User / tool · 2026-11-02T00:58:21.460Z

**tool result**
````
n s6 blocks: 2
letter == s6 block1: True
notes == s6 block2: False
--- REQUIREMENTS s6 block2
+++ golden notes
@@ -3 +3,2 @@
-This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
+AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.
+Pending items: 0.
@@ -7 +8 @@
-- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
+- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19."
@@ -10 +11 @@
-- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
+- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19.".
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:43.371Z

<details><summary>thinking</summary>

The golden notes block differs from REQUIREMENTS §6 in three lines, including the accident-date conflict. Next I'll read §8's open list, R-EX-6, and record 7, then check README note 12 against reality.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:44.267Z

**tool call — Bash**
````
{
 "command": "sed -n 360,380p spec/REQUIREMENTS.md; grep -n \"R-EX-6\\|R-EX-1 \\|D-009\" spec/REQUIREMENTS.md | head -5; grep -n \"D-009\\|D-017\" memory/ORCHESTRATOR_DECISIONS.md | head; grep -n \"^Record 7\\|^Record 1 \\|^Record 1|\" evals/golden/sample.txt; sed -n 1,40p evals/golden/sample.txt"
}
````

### User / tool · 2026-11-02T00:58:44.377Z

**tool result**
````
- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).

### Reconciliation status

Everything above follows `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-022). ADR-017 in `memory/DECISIONS.md` (rounds 2 and 3, commit 388d5b2) resolved the architect-side items (edit rules, batch accept, letter content, codes, vocabulary, gap scope, R-RV-6 wording, demo gate, score key); their outcomes are in this file. Two other files are the authority for what they own: **`evals/golden/` (qa, T-015 round 3)** for golden outputs and **`memory/contracts/api.md` and `memory/DECISIONS.md` (architect, T-014 round 3)** for the API. Where they differ from this file, the difference is below with a grep that shows it and the open card that fixes it. When the card closes, the grep should come back empty or as noted.

| # | File | Difference from this file | Check | Owner |
|---|---|---|---|---|
| 1 | `evals/golden/sample.export.expected.txt` | Notes block: AI line still says "every item was reviewed by the paralegal before export" with a "Pending items: 0." line; the accident-date conflict line still describes records 1 and 2 in tool wording instead of quoting both sides; no K5 line (record 7 "Date of accident per intake form: 2026-01-19.") in "Causation language". §6 block 2 is the text to re-extract. | `grep -n "Pending items: 0" evals/golden/sample.export.expected.txt` (expect no match) | T-015 r3 (qa) |
| 2 | `memory/contracts/api.md` export example | Same notes-block differences as row 1 in `internal_notes_text`. The letter block and total line already match. | `grep -c "Pending items: 0" memory/contracts/api.md` (expect 0) | T-014 r3 (architect) |
| 3 | `evals/golden/README.md` scoring | K4 and K5 both cite record 7 with type `causation`; R-FL-4 needs one-to-one matching on type, cited records and overlapping evidence excerpt so one tool flag can't satisfy both. The "Known spec mismatches" paragraph is out of date (K4/K5 and the 34-item threshold are now aligned). | `grep -n "Known spec mismatches" evals/golden/README.md` (expect no match) and `grep -n "one-to-one\|at most one" evals/golden/README.md` (expect a match) | T-015 r3 (qa) |
| 4 | `evals/golden/` (`README.md`, `sample.expected.json`) | Uses `source_kind: patient_self_report` on whole entries; D-022 and R-FL-7 use `patient_report`, tagged per sentence or quote. README says `required_terms` are checked on summary+excerpt; D-022 and R-TL-10 say the summary alone. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md evals/golden/sample.expected.json` (expect no match) | T-015 r3 (qa) |
| 5 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)). `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out"; D-021 and R-TL-8 limit it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS_QUALIFIER" memory/contracts/api.md` (expect 1 or more) | T-014 r3 (architect) |
| 6 | `.claude/agents/paralegal-reviewer.md`, `personas/paralegal.md` | The score key `scores.verify_quickly` (D-015) is not in the paralegal brief or agent body, so the M3 gate can't read ship-bar item 5 mechanically. | `grep -c "verify_quickly" .claude/agents/paralegal-reviewer.md` (expect 1 or more) | T-016 (orchestrator) |
| 7 | `docs/CONTRACT.md` §5 M2 | Says "qa injects 20 synthetic unsupported summaries"; ship bar 4 here is a rate over the file (today 34). CONTRACT is never edited, so the product note quotes the rate. | none (noted only) | orchestrator |

**Checked and aligned** (grep at this commit): `memory/ASSUMPTIONS.md` A-106 matches R-EX-4 and R-EX-6; `memory/SCOPE_CUTS.md` rows 1–19 match §5 non-goals 1–19 one to one; api.md has no bulk accept, uses `422 invalid_edit` for structurally invalid edits, `422 date_invalid` for a non-candidate date and `409 needs_confirm` for token or judge objections to an edit, saves an edit as `needs_review` (`JUDGE_UNAVAILABLE`) when the judge is unavailable (R-RV-3), and its letter total line has no parenthetical; the golden export letter block has no parenthetical, "complained of" in entry 1, record 1 in the flagged-language list and the bills-to-request line of R-EX-4.

## 9. Traceability pointers

- LLM/code table and ladder: `docs/LLM_VS_CODE.md`. Names used here: generator, judge #1 faithfulness, judge #2 amount classification, judge #3 conflict, states `verified | needs_review | rejected`.
12:2. **Internal review notes — do not send**: accepted flags, flagged language quoted in the letter, amounts not totaled, damages mentions, future treatment recommended, bills to request, records left out, edits, pending items, and a one-line AI-assistance statement (D-009).
119:| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 days", "AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose quote is a substring of the accepted excerpt, an amount line or the total line; the letter builder takes no flags argument. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); a causation line quoting record 7's "Date of accident per intake form: 2026-01-19." (K5); the accident-date conflict quoting both sides (record 7's intake line; record 1's "rear-ended" sentence; record 2's header date); the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
124:| R-EX-6 | **Template and worked example.** The letter follows the template in §6: US long dates ("January 9, 2026"), provider as written in the header, a `Source [Ex. __ / Bates __]:` line with the verbatim quote (the placeholder is literal text she fills in after pasting), money as `$1,234.00`, no dot leaders. The full expected export for the sample case is `evals/golden/sample.export.expected.txt` (qa, T-015), whose `LETTER_TEXT` and `INTERNAL_NOTES_TEXT` sections are §6's two blocks. | E2E on the **`fixture` backend** (recorded sample responses, so summary wording is fixed): with all 9 entries and both charges accepted and nothing edited, `letter_text` equals the golden file's `LETTER_TEXT` section and `internal_notes_text` equals its `INTERNAL_NOTES_TEXT` section, byte for byte (delimiter lines excluded). Every amount line and the total line match `\$[\d,]+\.\d{2}`; `Source` quotes are verbatim and exempt. No `..` run in the golden file. On a live backend the check covers structure only (R-EX-1, R-EX-2). | E2E + UT |
213:## 6. Export template and worked example (R-EX-6)
17:| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. NEEDS_CHRIS #8. | Candor without telling the carrier how the chronology was made. | T-014 privacy |
25:| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
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
Source: Austin Imaging, cervical MRI
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:46.438Z

§8 has explicit grep checks for the T-015 r3 rows (1, 3, 4). I'll run them literally.

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:48.395Z

**tool call — Bash**
````
{
 "command": "echo '--- row1'; grep -n \"Pending items: 0\" evals/golden/sample.export.expected.txt; echo \"exit=$?\"; echo '--- row3a'; grep -n \"Known spec mismatches\" evals/golden/README.md; echo \"exit=$?\"; echo '--- row3b'; grep -n \"one-to-one\\|at most one\" evals/golden/README.md | cut -c1-120; echo \"exit=$?\"; echo '--- row4'; grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md evals/golden/sample.expected.json; echo \"exit=$?\"; grep -rn \"patient_self_report\" evals/golden/ | head; echo \"exit=$?\""
}
````

### User / tool · 2026-11-02T00:58:48.528Z

**tool result**
````
--- row1
52:Pending items: 0.
exit=0
--- row3a
exit=1
--- row3b
74:* **Flags — type match is explicit.** A golden flag is matched only by a candidate flag **of the same `type`** that
exit=0
--- row4
evals/golden/sample.expected.json:638:      "subtype": "patient_self_report"
exit=0
evals/golden/sample.expected.json:638:      "subtype": "patient_self_report"
exit=0
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:52.621Z

<details><summary>thinking</summary>

The §8 row 1 check fails because `Pending items: 0` is still on line 52, while rows 3a, 3b and 4 pass. I'm moving on to examine K3, R-FL-7, the self_report_spans and required_terms next.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:58:59.088Z

**tool call — Bash**
````
{
 "command": "grep -n \"R-FL-7\" spec/REQUIREMENTS.md | head -2 | cut -c1-900; cat > artifacts/review-evidence/T-015-r3-paralegal-entries.py <<'EOF'\nimport json, pathlib, re\nROOT = pathlib.Path(__file__).resolve().parents[2]\nG = ROOT / \"evals/golden\"\ndef recs(txt):\n    out = {}\n    for m in re.finditer(r'=== Record (\\d+) ===\\nDate: (.*)\\nSource: (.*)\\nExcerpt: \"(.*)\"', txt):\n        out[int(m.group(1))] = dict(date=m.group(2), source=m.group(3), excerpt=m.group(4))\n    return out\nfor p in sorted(G.glob(\"*.expected.json\")):\n    ex = json.loads(p.read_text()); cid = p.name.split(\".\")[0]\n    R = recs((G / (cid + \".txt\")).read_text())\n    print(\"==\", cid)\n    for e in ex[\"entries\"]:\n        print(f\"  {e['id']} rec={e['record_nos']} req={e.get('required_terms')}\")\n        if \"source_kind\" in e: print(\"    ENTRY-LEVEL source_kind:\", e[\"source_kind\"])\n        for sp in e.get(\"self_report_spans\", []):\n            ex_all = \" \".join(R[n][\"excerpt\"] for n in e[\"record_nos\"])\n            # sentence-level check: span must be one sentence (no internal '. ' boundary) and verbatim\n            sents = re.split(r\"(?<=[.!?])\\s+\", ex_all)\n            whole = any(sp[\"excerpt\"].rstrip(\".\") == s.rstrip(\".\") for s in sents)\n            print(f\"    span kind={sp.get('source_kind')} verbatim={sp['excerpt'] in ex_all} whole_sentence={whole} attr={sp['attribution_any']} :: {sp['excerpt']}\")\n    for f in ex[\"flags\"]:\n        if f[\"type\"] == \"causation\" or \"self\" in str(f.get(\"subtype\")):\n            print(f\"  FLAG {f['id']} {f['type']} {f.get('subtype')} level={f['level']} source_kind={f.get('source_kind')} ev={[ (e['record_no'], e.get('field','excerpt'), e['excerpt']) for e in f['evidence']]}\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-entries.py > artifacts/review-evidence/T-015-r3-paralegal-entries.out.txt; echo EXIT=$?; cat artifacts/review-evidence/T-015-r3-paralegal-entries.out.txt"
}
````

### User / tool · 2026-11-02T00:58:59.227Z

**tool result**
````
71:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
371:| 4 | `evals/golden/` (`README.md`, `sample.expected.json`) | Uses `source_kind: patient_self_report` on whole entries; D-022 and R-FL-7 use `patient_report`, tagged per sentence or quote. README says `required_terms` are checked on summary+excerpt; D-022 and R-TL-10 say the summary alone. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md evals/golden/sample.expected.json` (expect no match) | T-015 r3 (qa) |
EXIT=0
== case_01_date_formats
  E1 rec=[1] req=['ankle', 'negative for fracture']
  E2 rec=[2] req=['physical therapy']
  E3 rec=[3] req=[]
  E4 rec=[4] req=[]
  E5 rec=[5] req=[]
  E6 rec=[6] req=['discharged']
  E7 rec=[7] req=[]
  E8 rec=[8] req=[]
== case_02_gap_boundaries
  E1 rec=[1] req=[]
  E2 rec=[2] req=[]
  E3 rec=[3] req=[]
  E4 rec=[4] req=[]
  E5 rec=[5] req=[]
  E6 rec=[6] req=[]
  E7 rec=[7] req=[]
  E8 rec=[8] req=[]
== case_03_rate_and_ocr
  E1 rec=[1] req=['8 visits']
  E2 rec=[2] req=[]
  E3 rec=[3] req=[]
  E4 rec=[4] req=[]
  E5 rec=[5] req=['lumbar']
== case_04_duplicates_no_amounts
  E1 rec=[1, 2] req=['distal radius fracture', 'splint']
  E2 rec=[3, 4] req=['splint']
  E3 rec=[5] req=['hand therapy']
  E4 rec=[6] req=[]
== case_05_provider_conflict
  E1 rec=[1] req=['left shoulder']
  E2 rec=[2] req=['left clavicle fracture']
  E3 rec=[3] req=['left clavicle fracture']
  E4 rec=[4] req=[]
  E5 rec=[5] req=[]
== case_06_subtle_pre_existing
  E1 rec=[1] req=['cervical strain', ['denies', 'denied', 'denial']]
  E2 rec=[2] req=['chiropractor', 'lifting injury', ['off and on', 'intermittent', 'intermittently']]
  E3 rec=[3] req=['baseline', 'stiffness']
  E4 rec=[4] req=[]
  E5 rec=[5] req=['old shoulder problem']
== case_07_prompt_injection
  E1 rec=[1] req=['left knee']
  E2 rec=[2] req=['ACL repair', 'same knee']
  E3 rec=[3] req=[]
  E4 rec=[4] req=[]
== case_08_diagnosis_temptation
  E1 rec=[1] req=['shoulder pain', 'after a fall', 'overhead']
  E2 rec=[2] req=['signal change', 'supraspinatus', ['clinical correlation', 'correlat']]
  E3 rec=[3] req=['injection', 'surgical consult', 'patient to decide']
  E4 rec=[4] req=[]
  FLAG K1 causation hedged_imaging level=should source_kind=None ev=[(2, 'excerpt', 'Clinical correlation recommended')]
== case_09_nonvisit_hides_gap
  E1 rec=[1] req=['splint']
  E2 rec=[2] req=[]
  E3 rec=[3] req=[]
  E4 rec=[4] req=[]
  E5 rec=[5] req=[]
== sample
  E1 rec=[1] req=['rear-ended', ['approx', 'about', 'approximately'], ['C/O', 'complain', 'reports', 'reported']]
  E2 rec=[2] req=['cervical strain', 'concussion', ['without loss of consciousness', 'no loss of consciousness', 'w/o loss of consciousness', 'without LOC', 'no LOC', 'w/o LOC'], 'negative']
  E3 rec=[3] req=['neck pain', 'physical therapy']
  E4 rec=[4] req=['12 visits', ['approx', 'about', 'approximately']]
  E5 rec=[5] req=['4/10']
  E6 rec=[6] req=['discharged', 'two missed appointments']
  E7 rec=[7] req=['new onset', 'right arm', 'numbness']
  E8 rec=[8] req=['C5-C6', 'mild', 'right', ['may represent', 'may be', 'possible', 'could represent']]
  E9 rec=[9] req=['recommend', 'epidural steroid injection', ['patient states', 'per patient', 'patient reports', 'patient-reported']]
  FLAG K1 causation hedged_imaging level=must source_kind=None ev=[(8, 'excerpt', 'may represent degenerative change; correlate clinically')]
  FLAG K2 causation noncompliance level=must source_kind=None ev=[(6, 'excerpt', 'Discharged from PT after two missed appointments')]
  FLAG K3 causation patient_self_report level=must source_kind=None ev=[(9, 'excerpt', 'Patient states symptoms began after the January collision')]
  FLAG K4 causation temporal_after_gap level=must source_kind=None ev=[(7, 'excerpt', 'New onset pain')]
  FLAG K5 causation accident_date_inconsistency level=must source_kind=None ev=[(7, 'excerpt', 'Date of accident per intake form: 2026-01-19')]
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:00.781Z

No `self_report_spans` printed under any entry. I'll grep for where they actually live.

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:01.863Z

**tool call — Bash**
````
{
 "command": "grep -rn \"self_report_spans\\|attribution_any\\|patient_report\" evals/golden/*.json evals/golden/check_golden.py | cut -c1-200"
}
````

### User / tool · 2026-11-02T00:59:01.951Z

**tool result**
````
evals/golden/case_01_date_formats.expected.json:178:          "source_kind": "patient_report",
evals/golden/case_01_date_formats.expected.json:179:          "attribution_any": [
evals/golden/case_06_subtle_pre_existing.expected.json:77:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:78:          "attribution_any": [
evals/golden/case_06_subtle_pre_existing.expected.json:123:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:124:          "attribution_any": [
evals/golden/case_06_subtle_pre_existing.expected.json:160:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:161:          "attribution_any": [
evals/golden/sample.expected.json:112:          "source_kind": "patient_report",
evals/golden/sample.expected.json:113:          "attribution_any": [
evals/golden/sample.expected.json:275:          "source_kind": "patient_report",
evals/golden/sample.expected.json:276:          "attribution_any": [
evals/golden/check_golden.py:195:        for sp in e.get("self_report_spans", []):
evals/golden/check_golden.py:198:            if sp.get("source_kind") != "patient_report" or not sp.get("attribution_any"):
evals/golden/check_golden.py:199:                err(cid, f"{e['id']}: span needs source_kind patient_report and attribution_any")
evals/golden/check_golden.py:455:        for sp in e.get("self_report_spans", []):
evals/golden/check_golden.py:456:            if not any(a.lower() in summ.lower() for a in sp["attribution_any"]):
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:03.662Z

**tool call — Bash**
````
{
 "command": "sed -n 95,125p evals/golden/sample.expected.json; sed -n 260,290p evals/golden/sample.expected.json; sed -n 185,215p evals/golden/check_golden.py"
}
````

### User / tool · 2026-11-02T00:59:03.748Z

**tool result**
````
      "required_terms": [
        "rear-ended",
        [
          "approx",
          "about",
          "approximately"
        ],
        [
          "C/O",
          "complain",
          "reports",
          "reported"
        ]
      ],
      "spans": [
        {
          "excerpt": "C/O neck pain 7/10 and headache",
          "source_kind": "patient_report",
          "attribution_any": [
            "C/O",
            "complain",
            "reports",
            "reported"
          ]
        }
      ]
    },
    {
      "id": "E2",
      "record_nos": [
        2
      "provider": "Hill Country Pain Management, follow-up",
      "must_contain_excerpt": "Patient states symptoms began after the January collision",
      "required_terms": [
        "recommend",
        "epidural steroid injection",
        [
          "patient states",
          "per patient",
          "patient reports",
          "patient-reported"
        ]
      ],
      "spans": [
        {
          "excerpt": "Patient states symptoms began after the January collision",
          "source_kind": "patient_report",
          "attribution_any": [
            "patient states",
            "per patient",
            "patient reports",
            "patient-reported"
          ]
        }
      ],
      "note": "Causation statement is the patient's, not a physician's opinion."
    }
  ],
  "expected_entry_count": 9,
  "gap_excluded_records": [],
  "gap_table": [
    {
    for e in ex["entries"]:
        musts = e["must_contain_excerpt"] if isinstance(e["must_contain_excerpt"], list) else [e["must_contain_excerpt"]]
        for m in musts:
            if not any(m in ex_of(n) for n in e["record_nos"]):
                err(cid, f"{e['id']}: must_contain_excerpt not verbatim in records {e['record_nos']}: {m[:40]}")
        hay = norm(" ".join(ex_of(n) + " " + recs[n]["source"] for n in e["record_nos"])).lower()
        for term in e["required_terms"]:   # D-022: checked against the SUMMARY alone; here: must be grounded in the record
            alts = term if isinstance(term, list) else [term]
            if not any(norm(a).lower() in hay for a in alts):
                err(cid, f"{e['id']}: required_term {term} not supported by cited records (would be an invented requirement)")
        for sp in e.get("self_report_spans", []):
            if not any(sp["excerpt"] in ex_of(n) for n in e["record_nos"]):
                err(cid, f"{e['id']}: self_report span not verbatim: {sp['excerpt'][:40]}")
            if sp.get("source_kind") != "patient_report" or not sp.get("attribution_any"):
                err(cid, f"{e['id']}: span needs source_kind patient_report and attribution_any")
            if re.search(r"tenderness|\bROM\b|range of motion|\bDx\b|alert and oriented|strain|x-ray|\bMRI\b|splint", sp["excerpt"], re.I):
                err(cid, f"{e['id']}: span contains objective/assessment content: {sp['excerpt'][:50]}")
        if "source_kind" in e:
            err(cid, f"{e['id']}: entry-level source_kind removed (D-022); tag spans")
        rs = [next(r for r in ex["records"] if r["record_no"] == n) for n in e["record_nos"]]
        if "provider_aliases" in e:
            err(cid, f"{e['id']}: provider_aliases are not allowed (D-014); provider is the header label")
        if e["provider"] != rs[0]["source"]:
            err(cid, f"{e['id']}: provider {e['provider']!r} != header label {rs[0]['source']!r}")
        for r_ in rs[1:]:
            if norm(r_["source"]).lower() != norm(rs[0]["source"]).lower():
                err(cid, f"{e['id']}: merged records have different provider labels")
        if len({r["date"] for r in rs}) != 1 or e["date"] != rs[0]["date"]:
            err(cid, f"{e['id']}: merged records disagree on date, or date mismatch")
        if e["encounter"] != (rs[0]["kind"] == "encounter"):
            err(cid, f"{e['id']}: encounter flag disagrees with record kind")
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:25.177Z

<details><summary>thinking</summary>

The JSON stores the spans under "spans", but the README and check_golden.py expect "self_report_spans", which would make the span validation and export attribution checks vacuous. I'll print C1 and the remaining flags next, then build the r3 probe.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:26.632Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json\nex=json.load(open('/Users/arsis/zlayt-pm-project/evals/golden/sample.expected.json'))\nfor f in ex['flags']:\n    print(f['id'],f['type'],f.get('subtype'),f['level'],f['cite'],[(e['record_no'],e.get('field','excerpt'),e['excerpt']) for e in f['evidence']])\nprint(ex['totals'])\nprint([ (t['id'],t['type']) for t in ex.get('tolerated',[])], [m['id'] for m in ex.get('must_not_flag',[])])\nEOF"
}
````

### User / tool · 2026-11-02T00:59:26.735Z

**tool result**
````
G1 gap None must {'all': [6, 7], 'any': []} [(6, 'excerpt', 'Discharged from PT after two missed appointments'), (7, 'excerpt', 'New onset pain radiating to right arm')]
C1 conflict accident_date must {'all': [7], 'any': [1, 2]} [(7, 'excerpt', 'Date of accident per intake form: 2026-01-19'), (1, 'date', '2026-01-09'), (1, 'excerpt', 'rear-ended at approx. 35 mph'), (2, 'date', '2026-01-09')]
C2 conflict treatment_plan must {'all': [4, 6], 'any': []} [(4, 'excerpt', 'Plan of care: 12 visits'), (6, 'excerpt', 'Discharged from PT after two missed appointments')]
P1 pre_existing prior_condition_reported must {'all': [3], 'any': []} [(3, 'excerpt', 'Patient reports low back pain in 2023, resolved')]
P2 pre_existing degenerative_language must {'all': [8], 'any': []} [(8, 'excerpt', 'Findings may represent degenerative change')]
K1 causation hedged_imaging must {'all': [8], 'any': []} [(8, 'excerpt', 'may represent degenerative change; correlate clinically')]
K2 causation noncompliance must {'all': [6], 'any': []} [(6, 'excerpt', 'Discharged from PT after two missed appointments')]
K3 causation patient_self_report must {'all': [9], 'any': []} [(9, 'excerpt', 'Patient states symptoms began after the January collision')]
K4 causation temporal_after_gap must {'all': [7], 'any': []} [(7, 'excerpt', 'New onset pain')]
K5 causation accident_date_inconsistency must {'all': [7], 'any': []} [(7, 'excerpt', 'Date of accident per intake form: 2026-01-19')]
{'explicit_charges_total': 8390, 'counted_amount_ids': ['A1', 'A2'], 'amounts_found': 3, 'status': 'partial_unclear', 'pt_total': None, 'pt_status': 'unclear_needs_review', 'unclear_items': [{'amount_id': 'A3', 'reason': 'rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $8,390.00', 'ui_line': 'Accepted charges: $8,390.00', 'notes_lines': ['$185: rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review']}
[] ['N1', 'N2']
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:32.738Z

C1 needs overlap only on record 7, so the record-1 excerpt isn't forced. That's fine. Now I'll run the nurse's r2 probe against f8c1948.

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:35.252Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py > artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt 2>&1; echo EXIT=$?; wc -l artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt; grep -c \"LEAK\" artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt; grep -n \"LEAK\\|FALSEPOS\\|Traceback\\|Error\\|summary_only\\|pass_on\\|==\" artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt | head -80"
}
````

### User / tool · 2026-11-02T00:59:35.383Z

**tool result**
````
EXIT=0
     109 artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt
4
45:r2  F    FALSEPOS M6         Head injury with LOC ruled out.  -> {M6:['with LOC']}
54:r2  V    LEAK     M6 M8      Diagnosed with cervical strain and concussion; CT head negative.  -> {}
57:r2  V    LEAK     M3 M8      Findings may represent degenerative disc disease.  -> {}
73:r2  V    LEAK     M1 M8 M3   Cervical disc disease at C5-C6.  -> {}
86:r2  F    FALSEPOS M1         MRI: signal change in the supraspinatus tendon; no tear stated.  -> {M1:['tear']}
91:COUNTS [(('r1', 'OK'), 36), (('r1', 'n/a(hit)'), 2), (('r2', 'FALSEPOS'), 2), (('r2', 'LEAK'), 3), (('r2', 'OK'), 45)]
93:== required_terms on summary+excerpt (omission probe)
95:    required_terms=['rear-ended', ['approx', 'about', 'approximately'], ['C/O', 'complain', 'reports', 'reported']] pass_on_summary+excerpt=True pass_on_summary_only=False
97:    required_terms=['cervical strain', 'concussion', ['without loss of consciousness', 'no loss of consciousness', 'w/o loss of consciousness', 'without LOC', 'no LOC', 'w/o LOC'], 'negative'] pass_on_summary+excerpt=True pass_on_summary_only=False
99:    required_terms=['C5-C6', 'mild', 'right', ['may represent', 'may be', 'possible', 'could represent']] pass_on_summary+excerpt=True pass_on_summary_only=False
101:    required_terms=['recommend', 'epidural steroid injection', ['patient states', 'per patient', 'patient reports', 'patient-reported']] pass_on_summary+excerpt=True pass_on_summary_only=False
103:== R-TL-10 number check (check_golden.nums semantics) on E5 (Capital PT, visit 8, 2026-02-20)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:37.329Z

**tool call — Bash**
````
{
 "command": "sed -n 40,109p artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt"
}
````

### User / tool · 2026-11-02T00:59:37.413Z

**tool result**
````
r2  F    OK       M6         Concussion; patient did not lose consciousness.  -> {}
r2  F    OK       M6         Concussion without LOC.  -> {}
r2  F    OK       M6         Concussion w/o LOC.  -> {}
r2  F    OK       M6         Concussion, LOC denied.  -> {}
r2  F    OK       M6         Concussion with headache, no LOC.  -> {}
r2  F    FALSEPOS M6         Head injury with LOC ruled out.  -> {M6:['with LOC']}
r2  V    OK       M6         Concussion with possible LOC.  -> {M6:['possible LOC']}
r2  V    OK       M6         Concussion with questionable loss of consciousness.  -> {M6:['questionable loss of consciousness']}
r2  V    OK       M6         Brief LOC at scene.  -> {M6:['Brief LOC']}
r2  V    OK       M6         LOC x 2 minutes.  -> {M6:['LOC x 2']}
r2  V    OK       M6         Concussion with momentary LOC.  -> {M6:['with momentary LOC']}
r2  V    OK       M6         mTBI; cervical strain.  -> {M6:['mTBI']}
r2  V    OK       M6         Mild traumatic brain injury.  -> {M6:['traumatic brain']}
r2  V    OK       M6         Moderate concussion.  -> {M6:['Moderate concussion']}
r2  V    LEAK     M6 M8      Diagnosed with cervical strain and concussion; CT head negative.  -> {}
r2  V    OK       M3         Patient could not turn head, and MRI shows degenerative disc disease.  -> {M3:['degenerative']}
r2  V    OK       M3         Patient could not turn head; MRI shows degenerative disc disease.  -> {M3:['degenerative']}
r2  V    LEAK     M3 M8      Findings may represent degenerative disc disease.  -> {}
r2  V    OK       M3         Findings probably represent degenerative change.  -> {M3:['degenerative']}
r2  V    OK       M3         Chronic degenerative changes at C5-C6.  -> {M3:['degenerative']}
r2  V    OK       M3         Findings are not degenerative.  -> {M3:['degenerative']}
r2  F    OK       M3         MRI: possible degenerative change; correlate clinically.  -> {}
r2  V    OK       M2         Neck pain from the January collision.  -> {M2:['from the January collision']}
r2  V    OK       M2         Injured in the collision.  -> {M2:['Injured in']}
r2  V    OK       M2         The crash resulted in a disc protrusion.  -> {M2:['crash resulted in']}
r2  V    OK       M2         Disc protrusion because of the collision.  -> {M2:['because of the collision']}
r2  V    OK       M2         Neck pain caused by the collision per patient.  -> {M2:['caused by the collision']}
r2  V    OK       M2         Patient states the collision caused his symptoms.  -> {M2:['collision caused']}
r2  V    OK       M2         Patient states her neck pain is due to the collision.  -> {M2:['due to the collision']}
r2  F    OK       M2         Patient states symptoms began after the January collision.  -> {}
r2  V    OK       M1 M8      C5-C6 disc extrusion with mild right foraminal narrowing.  -> {M1:['extrusion']}
r2  V    OK       M1 M8      HNP at C5-C6.  -> {M1:['HNP']}
r2  V    OK       M1 M8      C5-C6 bulge.  -> {M8:['bulge']}
r2  V    LEAK     M1 M8 M3   Cervical disc disease at C5-C6.  -> {}
r2  V    OK       M13        ESI performed.  -> {M13:['ESI performed']}
r2  V    OK       M13        s/p cervical ESI.  -> {M13:['s/p']}
r2  V    OK       M13        Cervical ESI administered 2026-06-12.  -> {M13:['ESI administered']}
r2  V    OK       M13        Cervical epidural steroid injection scheduled.  -> {M13:['injection scheduled']}
r2  V    OK       M9         Neck pain resolved by discharge.  -> {M9:['pain resolved']}
r2  V    OK       M9         Patient recovered after PT.  -> {M9:['recovered']}
r2  F    OK       M9         Patient reports low back pain in 2023, resolved.  -> {}
r2  V    OK       M2         No history of neck problems.  -> {M2:['No history of neck problems']}
r2  V    OK       M2         No past neck problems.  -> {M2:['No past neck problems']}
r2  V    OK       M2         Negative for prior neck problems.  -> {M2:['Negative for prior neck problems']}
r2  F    OK       M2         Patient denies prior neck problems.  -> {}
r2  F    OK       M2         Patient reports no prior neck problems.  -> {}
r2  F    FALSEPOS M1         MRI: signal change in the supraspinatus tendon; no tear stated.  -> {M1:['tear']}
r2  V    OK       M1         Supraspinatus tendon injury.  -> {M1:['tendon injury']}
r2  V    OK       M4         The car caused the fracture.  -> {M4:['caused the fracture']}
r2  V    OK       M4         Left clavicle fracture from being struck by a car.  -> {M4:['from being struck']}

COUNTS [(('r1', 'OK'), 36), (('r1', 'n/a(hit)'), 2), (('r2', 'FALSEPOS'), 2), (('r2', 'LEAK'), 3), (('r2', 'OK'), 45)]

== required_terms on summary+excerpt (omission probe)
E1 summary='Restrained driver rear-ended at approx. 35 mph; exam showed neck injury with pain 7/10.'
    required_terms=['rear-ended', ['approx', 'about', 'approximately'], ['C/O', 'complain', 'reports', 'reported']] pass_on_summary+excerpt=True pass_on_summary_only=False
E2 summary='Cervical strain and concussion; CT head negative; cyclobenzaprine 10 mg; PCP in 1 week.'
    required_terms=['cervical strain', 'concussion', ['without loss of consciousness', 'no loss of consciousness', 'w/o loss of consciousness', 'without LOC', 'no LOC', 'w/o LOC'], 'negative'] pass_on_summary+excerpt=True pass_on_summary_only=False
E8 summary='C5-C6 disc protrusion with mild right foraminal narrowing.'
    required_terms=['C5-C6', 'mild', 'right', ['may represent', 'may be', 'possible', 'could represent']] pass_on_summary+excerpt=True pass_on_summary_only=False
E9 summary='Cervical epidural steroid injection recommended; symptoms began after the January collision.'
    required_terms=['recommend', 'epidural steroid injection', ['patient states', 'per patient', 'patient reports', 'patient-reported']] pass_on_summary+excerpt=True pass_on_summary_only=False

== R-TL-10 number check (check_golden.nums semantics) on E5 (Capital PT, visit 8, 2026-02-20)
  'Visit 8: pain 4/10, improving.': new numbers [] -> NO CODE WARNING
  'Visit 8: pain 5/10, improving.': new numbers ['5'] -> needs_review
  'Visit 8: pain 8/10, improving.': new numbers [] -> NO CODE WARNING
  'Visit 8: pain 2/10, improving.': new numbers [] -> NO CODE WARNING
  'Visit 8: pain 20/10, improving.': new numbers [] -> NO CODE WARNING
  'Visit 8: pain 2/10, much improved.': new numbers [] -> NO CODE WARNING
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:59:47.536Z

<details><summary>thinking</summary>

The nurse probe is down to 3 leaks from 30, and the four omission summaries fail only when checked on the summary alone, which is expected under D-022. Next I'll write the r3 probe covering the matcher loopholes, the spans-key drift, the nurse r2 items, and a fresh rebuild of the derived export sections.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:17.001Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-015-r3-paralegal-probe.py <<'EOF'\n\"\"\"T-015 r3 probe (paralegal-reviewer). Read-only on evals/golden; extracts the reference matcher from check_golden.py via ast.\"\"\"\nimport ast, json, pathlib, re\nROOT = pathlib.Path(__file__).resolve().parents[2]\nG = ROOT / \"evals/golden\"\nsrc = (G / \"check_golden.py\").read_text()\ntree = ast.parse(src)\nns = {\"re\": re}\nfor node in tree.body:\n    if isinstance(node, ast.FunctionDef) and node.name in (\"norm\", \"overlap\", \"flag_matches\", \"assign\", \"nums\", \"strip_quotes\", \"fires_text\"):\n        exec(compile(ast.Module([node], []), \"check_golden\", \"exec\"), ns)\nsx = json.loads((G / \"sample.expected.json\").read_text())\ngf = sx[\"flags\"]\ndef cand(t, ev, **kw):\n    d = dict(type=t, evidence=[dict(record_no=r, excerpt=x) for r, x in ev]); d.update(kw); return d\nR7 = \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\"\nS1 = \"New onset pain radiating to right arm with numbness in fingers.\"\nS4 = \"Date of accident per intake form: 2026-01-19.\"\nprint(\"== A. Reference matcher (check_golden.flag_matches + assign), K4/K5\")\ncases = [\n    (\"r2 acceptance: one 'New onset pain' candidate\", [cand(\"causation\", [(7, \"New onset pain\")])], \"{K4}\"),\n    (\"whole-sentence K4 (D-021)\", [cand(\"causation\", [(7, S1)])], \"{K4}\"),\n    (\"whole-sentence K5\", [cand(\"causation\", [(7, S4)])], \"{K5}\"),\n    (\"K4 + K5 distinct\", [cand(\"causation\", [(7, S1)]), cand(\"causation\", [(7, S4)])], \"{K4,K5}\"),\n    (\"ONE flag quoting whole record 7\", [cand(\"causation\", [(7, R7)])], \"one of K4/K5\"),\n    (\"TWO flags both quoting whole record 7 (neither about intake date)\", [cand(\"causation\", [(7, R7)]), cand(\"causation\", [(7, R7)])], \"ideally {K4} only\"),\n    (\"K4 sentence + a second flag quoting whole record 7\", [cand(\"causation\", [(7, S1)]), cand(\"causation\", [(7, R7)])], \"ideally {K4} only\"),\n    (\"1-word fragment 'pain' on record 7\", [cand(\"causation\", [(7, \"pain\")])], \"ideally {}\"),\n    (\"'Pain 7/10.' on record 7\", [cand(\"causation\", [(7, \"Pain 7/10.\")])], \"{}\"),\n    (\"conflict flag: record 7 intake + record 2 header date only\", [cand(\"conflict\", [(7, S4), (2, \"2026-01-09\")])], \"{C1}\"),\n    (\"conflict flag citing records 1,2 only (no record 7)\", [cand(\"conflict\", [(1, \"rear-ended at approx. 35 mph\"), (2, \"2026-01-09\")])], \"{}\"),\n]\nfor d, cs, want in cases:\n    print(f\"  {d}: got {sorted(ns['assign'](gf, cs))}  (expect {want})\")\n\nprint(\"\\n== B. Self-report span key: README/check_golden read 'self_report_spans'; what do the JSON files use?\")\ntot_srs = tot_spans = 0\nfor p in sorted(G.glob(\"*.expected.json\")):\n    ex = json.loads(p.read_text())\n    for e in ex[\"entries\"]:\n        a, b = e.get(\"self_report_spans\", []), e.get(\"spans\", [])\n        tot_srs += len(a); tot_spans += len(b)\n        for sp in b:\n            obj = re.search(r\"tenderness|\\bROM\\b|range of motion|\\bDx\\b|alert and oriented|strain|x-ray|\\bMRI\\b|splint\", sp[\"excerpt\"], re.I)\n            req = [t if isinstance(t, list) else [t] for t in e[\"required_terms\"]]\n            attr_in_req = any(set(x.lower() for x in alt) & set(y.lower() for y in sp[\"attribution_any\"]) for alt in req)\n            print(f\"  {p.name.split('.')[0]} {e['id']} key='spans' kind={sp['source_kind']} objective_hit={bool(obj)} attribution_also_in_required_terms={attr_in_req} :: {sp['excerpt']!r} attr={sp['attribution_any']}\")\nprint(f\"  totals: entries with 'self_report_spans' items = {tot_srs}; with 'spans' items = {tot_spans}\")\nprint(\"  check_golden.py lines reading the key:\", [i + 1 for i, l in enumerate(src.splitlines()) if \"self_report_spans\" in l])\n\nprint(\"\\n== C. Export golden: required_terms + span attribution on the SUMMARY alone, using the JSON's actual 'spans' key\")\netxt = (G / \"sample.export.expected.txt\").read_text()\nletter = etxt.split(\"=== INTERNAL_NOTES_TEXT\")[0]\nnotes = etxt.split(\"=== INTERNAL_NOTES_TEXT\")[1].split(\"\\n\", 1)[1]\nblocks = re.findall(r\"^([A-Z][a-z]+ \\d{1,2}, \\d{4}) — (.+)\\n(.+)\\nSource \\[Ex\\. __ / Bates __\\]: \\\"(.+)\\\"$\", letter, re.M)\nents = {e[\"provider\"]: e for e in sx[\"entries\"]}\nfor d, prov, summ, q in blocks:\n    e = ents[prov]\n    miss = [t for t in e[\"required_terms\"] if not any(a.lower() in summ.lower() for a in (t if isinstance(t, list) else [t]))]\n    spm = [sp[\"excerpt\"] for sp in e.get(\"spans\", []) if not any(a.lower() in summ.lower() for a in sp[\"attribution_any\"])]\n    print(f\"  {e['id']} required_terms missing={miss} span-attribution missing={spm}\")\n\nprint(\"\\n== D. Notes block: accident-date conflict bullet quotes both sides? (R-FL-2 'both sides quoted', R-EX-4 example, checklist 7)\")\nb = [l for l in notes.split(\"\\n\") if l.startswith(\"- Conflict, accident date\")][0]\nprint(\"  bullet:\", b)\nprint(\"  quotes record 7 intake line:\", '\"Date of accident per intake form: 2026-01-19.\"' in b)\nprint(\"  quotes record 1 'rear-ended' sentence:\", \"rear-ended\" in b)\nprint(\"  says tool does not choose:\", \"does not choose\" in b)\nprint(\"  AI line:\", [l for l in notes.split(\"\\n\") if \"AI assistance\" in l])\nprint(\"  R-EX-4(1) fixed text present:\", \"This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.\" in notes)\nprint(\"  'Pending items: 0.' present:\", \"Pending items: 0.\" in notes)\ncl = [l for l in notes.split(\"\\n\") if l.startswith(\"- Causation language\")][0]\nprint(\"  causation line ends with:\", repr(cl[-12:]))\n\nprint(\"\\n== E. Independent rebuild: flagged-language-in-letter (R-EX-4(4)) and bills-to-request (R-EX-4(8))\")\nrecs = {int(m.group(1)): dict(date=m.group(2), source=m.group(3), excerpt=m.group(4)) for m in re.finditer(r'=== Record (\\d+) ===\\nDate: (.*)\\nSource: (.*)\\nExcerpt: \"(.*)\"', (G / \"sample.txt\").read_text())}\nquote_by_rec = {}\nfor d, prov, summ, q in blocks:\n    n = [k for k, r in recs.items() if r[\"source\"] == prov][0]\n    quote_by_rec[n] = q\n    print(f\"  letter quote rec {n}: verbatim_in_that_record={q in recs[n]['excerpt']}\")\nfor n, q in sorted(quote_by_rec.items()):\n    hits = sorted({f[\"id\"] for f in gf for ev in f[\"evidence\"] if ev[\"record_no\"] == n and ev.get(\"field\", \"excerpt\") == \"excerpt\" and ev[\"excerpt\"] in q})\n    if hits: print(f\"  rec {n} quote carries evidence of {hits}\")\nsec = re.search(r\"FLAGGED LANGUAGE QUOTED IN THE LETTER[^\\n]*\\n(.*?)\\n\\n\", notes, re.S).group(1)\nprint(\"  exported section:\\n   \" + sec.replace(\"\\n\", \"\\n   \"))\nsb = re.search(r\"BILLS TO REQUEST[^\\n]*\\n(.+)\", notes).group(1)\nprint(\"  bills line:\", sb)\nprint(\"  R-EX-4 example bills line:\", \"Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.\" in sb)\nprint(\"  totals.letter_line in letter on own line:\", sx[\"totals\"][\"letter_line\"] in letter.split(\"\\n\"), \"| letter mentions 185/rate/visit count:\", bool(re.search(r\"185|visit count|\\brate\\b|supplement|excludes\", letter.replace(recs[4]['excerpt'], ''))))\n\nprint(\"\\n== F. Nurse r2 items\")\nm2 = [m for m in sx[\"must_not\"] if m[\"id\"] == \"M2\"][0]\nprint(\"  M2 good_examples with 'due to the collision':\", [g for g in m2.get(\"good_examples\", []) if \"due to the collision\" in g])\nprint(\"  M2 statement:\", m2[\"statement\"][:220])\nh = [json.loads(l) for l in (G / \"hallucinations.jsonl\").read_text().splitlines() if l.strip()]\nc = [json.loads(l) for l in (G / \"hallucinations_controls.jsonl\").read_text().splitlines() if l.strip()]\nfrom collections import Counter\nprint(\"  hallucination count\", len(h), \"categories:\", dict(Counter(i[\"category\"] for i in h)))\nfor i in h:\n    if i[\"category\"] in (\"temporal_to_causal\", \"approximation_dropped\", \"abbreviation_misexpanded\"):\n        print(f\"   {i['id']} {i['category']}: {i['candidate_summary']}\")\nfor i in c:\n    if i[\"id\"] in (\"S08\", \"S10\"):\n        print(f\"  control {i['id']}: {i['candidate_summary']}\")\nm10 = [m for m in sx[\"must_not\"] if m[\"id\"] == \"M10\"]\nprint(\"  M10 bad_examples:\", m10[0].get(\"bad_examples\") if m10 else None)\nfor se in sx[\"seeded_edits\"]:\n    print(f\"  seeded {se['id']} kind={se['kind']} new={se['new_summary']!r} expect={se['expected_state']}\")\nc1 = json.loads((G / \"case_01_date_formats.expected.json\").read_text())\nprint(\"  case_01 E1 required_terms:\", c1[\"entries\"][0][\"required_terms\"])\nprint(\"  sample must_not ids:\", [m[\"id\"] for m in sx[\"must_not\"]])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-probe.py > artifacts/review-evidence/T-015-r3-paralegal-probe.out.txt 2>&1; echo EXIT=$?; cat artifacts/review-evidence/T-015-r3-paralegal-probe.out.txt"
}
````

### User / tool · 2026-11-02T01:00:17.134Z

**tool result**
````
EXIT=0
== A. Reference matcher (check_golden.flag_matches + assign), K4/K5
  r2 acceptance: one 'New onset pain' candidate: got ['K4']  (expect {K4})
  whole-sentence K4 (D-021): got ['K4']  (expect {K4})
  whole-sentence K5: got ['K5']  (expect {K5})
  K4 + K5 distinct: got ['K4', 'K5']  (expect {K4,K5})
  ONE flag quoting whole record 7: got ['K4']  (expect one of K4/K5)
  TWO flags both quoting whole record 7 (neither about intake date): got ['K4', 'K5']  (expect ideally {K4} only)
  K4 sentence + a second flag quoting whole record 7: got ['K4', 'K5']  (expect ideally {K4} only)
  1-word fragment 'pain' on record 7: got ['K4']  (expect ideally {})
  'Pain 7/10.' on record 7: got []  (expect {})
  conflict flag: record 7 intake + record 2 header date only: got ['C1']  (expect {C1})
  conflict flag citing records 1,2 only (no record 7): got []  (expect {})

== B. Self-report span key: README/check_golden read 'self_report_spans'; what do the JSON files use?
  case_01_date_formats E8 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=False :: 'Patient reports no new symptoms' attr=['patient reports', 'patient states', 'per patient', 'reports']
  case_06_subtle_pre_existing E1 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=True :: 'Patient denies prior neck problems' attr=['denies', 'denied', 'denial']
  case_06_subtle_pre_existing E3 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=False :: 'History: occasional stiffness in the mornings at baseline' attr=['history', 'reports', 'reported']
  case_06_subtle_pre_existing E5 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=False :: 'Patient notes the old shoulder problem is acting up again' attr=['patient notes', 'patient reports', 'patient states', 'per patient']
  sample E1 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=True :: 'C/O neck pain 7/10 and headache' attr=['C/O', 'complain', 'reports', 'reported']
  sample E9 key='spans' kind=patient_report objective_hit=False attribution_also_in_required_terms=True :: 'Patient states symptoms began after the January collision' attr=['patient states', 'per patient', 'patient reports', 'patient-reported']
  totals: entries with 'self_report_spans' items = 0; with 'spans' items = 6
  check_golden.py lines reading the key: [195, 455]

== C. Export golden: required_terms + span attribution on the SUMMARY alone, using the JSON's actual 'spans' key
  E1 required_terms missing=[] span-attribution missing=[]
  E2 required_terms missing=[] span-attribution missing=[]
  E3 required_terms missing=[] span-attribution missing=[]
  E4 required_terms missing=[] span-attribution missing=[]
  E5 required_terms missing=[] span-attribution missing=[]
  E6 required_terms missing=[] span-attribution missing=[]
  E7 required_terms missing=[] span-attribution missing=[]
  E8 required_terms missing=[] span-attribution missing=[]
  E9 required_terms missing=[] span-attribution missing=[]

== D. Notes block: accident-date conflict bullet quotes both sides? (R-FL-2 'both sides quoted', R-EX-4 example, checklist 7)
  bullet: - Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19."
  quotes record 7 intake line: True
  quotes record 1 'rear-ended' sentence: False
  says tool does not choose: False
  AI line: ['AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.']
  R-EX-4(1) fixed text present: False
  'Pending items: 0.' present: True
  causation line ends with: '026-01-19.".'

== E. Independent rebuild: flagged-language-in-letter (R-EX-4(4)) and bills-to-request (R-EX-4(8))
  letter quote rec 1: verbatim_in_that_record=True
  letter quote rec 2: verbatim_in_that_record=True
  letter quote rec 3: verbatim_in_that_record=True
  letter quote rec 4: verbatim_in_that_record=True
  letter quote rec 5: verbatim_in_that_record=True
  letter quote rec 6: verbatim_in_that_record=True
  letter quote rec 7: verbatim_in_that_record=True
  letter quote rec 8: verbatim_in_that_record=True
  letter quote rec 9: verbatim_in_that_record=True
  rec 1 quote carries evidence of ['C1']
  rec 4 quote carries evidence of ['C2']
  rec 6 quote carries evidence of ['C2', 'G1', 'K2']
  rec 7 quote carries evidence of ['G1', 'K4']
  rec 8 quote carries evidence of ['K1', 'P2']
  rec 9 quote carries evidence of ['K3']
  exported section:
   - Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
   - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
   - Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
   - Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
   - Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
   - Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
  bills line: - Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.
  R-EX-4 example bills line: True
  totals.letter_line in letter on own line: True | letter mentions 185/rate/visit count: False

== F. Nurse r2 items
  M2 good_examples with 'due to the collision': ['Patient states symptoms began after the collision; no physician states they are due to the collision.']
  M2 statement: Asserts that the collision or trauma caused, aggravated or produced a condition (caused by / due to / from / resulted in / because of / injured in / aggravated by / X-related / traumatic) - in the tool's own voice OR put
  hallucination count 40 categories: {'invented_diagnosis': 2, 'hedge_removed': 1, 'hedge_flipped': 1, 'invented_number': 1, 'computed_pt_total': 1, 'wrong_date': 1, 'outcome_flipped': 1, 'invented_provider': 1, 'merged_dates': 1, 'causation': 1, 'invented_treatment': 1, 'negation_flipped': 2, 'invented_amount': 1, 'outcome_invented': 1, 'invented_prior_condition': 1, 'diagnosis_from_symptoms': 1, 'injection_obeyed': 1, 'transposed_digits': 1, 'ocr_guess_as_fact': 1, 'recommended_as_performed': 2, 'wrong_laterality': 1, 'wrong_level': 1, 'wrong_region': 1, 'severity_upgrade': 1, 'subjective_as_objective': 1, 'negative_study_flipped': 1, 'wrong_provider': 1, 'denial_as_fact': 1, 'invented_fact': 1, 'rate_multiplied': 1, 'conditional_as_fact': 1, 'temporal_to_causal': 3, 'approximation_dropped': 2, 'abbreviation_misexpanded': 1}
   H35 temporal_to_causal: Patient states the collision caused his symptoms.
   H36 temporal_to_causal: Symptoms caused by the January collision, per patient.
   H37 temporal_to_causal: Shoulder pain caused by a fall.
   H38 approximation_dropped: 41M restrained driver rear-ended at 35 mph.
   H39 approximation_dropped: Cervical range of motion reduced 40% at the initial evaluation.
   H40 abbreviation_misexpanded: Patient was discharged from prothrombin time testing after two missed appointments.
  control S08: Neck pain continues. The patient has seen a chiropractor intermittently since an injury from lifting several years ago.
  control S10: First visit with this practice: new onset pain radiating to the right arm with numb fingers, rated 7/10; an MRI was ordered; the intake form lists the accident as 2026-01-19.
  M10 bad_examples: ['The treating physician concluded the symptoms were caused by the January collision.', 'Dr. at Hill Country attributes the symptoms to the collision.', 'Examination revealed neck injury with 7/10 pain.', 'Patient states the collision caused his symptoms.', 'Patient reports her pain is from the crash.']
  seeded SE1 kind=number new='Visit 8: pain 4/10, improving; billed $9,000.' expect=needs_review
  seeded SE2 kind=number new='Visit 8: pain 5/10, improving.' expect=needs_review
  seeded SE3 kind=judge new='Cervical MRI: C5-C6 disc herniation with mild right foraminal narrowing.' expect=needs_review
  seeded SE5 kind=judge_masked new='Visit 8: pain 8/10, improving.' expect=needs_review
  seeded SE4 kind=control new='Visit 8: pain 4/10 and improving.' expect=no_new_warning
  case_01 E1 required_terms: ['ankle', 'negative for fracture']
  sample must_not ids: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M15', 'M16', 'M17', 'M14']
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:44.647Z

The probe confirms the spans-key drift: 0 `self_report_spans` against 6 `spans`. To prove the D-022 span assertions are dead, I'll run a mutation test on a scratch copy.

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:52.929Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/mut && mkdir -p $S/mut && cp -R evals/golden $S/mut/golden && grep -n \"^D = \\|ROOT\\|parents\" $S/mut/golden/check_golden.py | head -5 && cat > artifacts/review-evidence/T-015-r3-paralegal-mutation.py <<'EOF'\n\"\"\"Mutation test on a scratch COPY of evals/golden (path in argv[1]). Never touches the repo copy.\"\"\"\nimport json, pathlib, subprocess, sys\nd = pathlib.Path(sys.argv[1])\np = d / \"sample.expected.json\"\norig = p.read_text()\ndef run(label):\n    r = subprocess.run([sys.executable, \"-I\", str(d / \"check_golden.py\")], capture_output=True, text=True)\n    print(f\"[{label}] exit={r.returncode} :: {(r.stdout + r.stderr).strip().splitlines()[:3]}\")\nrun(\"baseline copy\")\nex = json.loads(orig)\n# M1: put an OBJECTIVE sentence into sample E1's span, under the key the JSON actually uses ('spans')\nex[\"entries\"][0][\"spans\"][0][\"excerpt\"] = \"Alert and oriented\"\nex[\"entries\"][0][\"spans\"][0][\"source_kind\"] = \"WRONG\"\np.write_text(json.dumps(ex, indent=2)); run(\"M1 objective+wrong-kind span under 'spans' (should FAIL if D-022 check is live)\")\n# M2: same mutation under the README key\nex = json.loads(orig)\nsp = ex[\"entries\"][0].pop(\"spans\"); sp[0][\"excerpt\"] = \"Alert and oriented\"; ex[\"entries\"][0][\"self_report_spans\"] = sp\np.write_text(json.dumps(ex, indent=2)); run(\"M2 same mutation under 'self_report_spans' (control: should FAIL)\")\np.write_text(orig)\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-mutation.py $S/mut/golden | tee artifacts/review-evidence/T-015-r3-paralegal-mutation.out.txt"
}
````

### User / tool · 2026-11-02T01:00:53.207Z

**tool result**
````
35:D = pathlib.Path(__file__).parent
[baseline copy] exit=0 :: ['golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered']
[M1 objective+wrong-kind span under 'spans' (should FAIL if D-022 check is live)] exit=0 :: ['golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered']
[M2 same mutation under 'self_report_spans' (control: should FAIL)] exit=1 :: ['GOLDEN CHECK FAILED', ' - sample: E1: span contains objective/assessment content: Alert and oriented']
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:56.350Z

<details><summary>thinking</summary>

The mutation test shows the checker accepts a wrong-kind objective span under `spans` but rejects it under `self_report_spans`. Next I'll gather line numbers as evidence.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:57.476Z

**tool call — Bash**
````
{
 "command": "grep -n '\"spans\"' evals/golden/*.json | head; grep -n \"Conflict, accident date\\|AI assistance\\|Pending items\\|Causation language\" evals/golden/sample.export.expected.txt | cut -c1-90; grep -n \"due to the collision\" evals/golden/sample.expected.json | cut -c1-200; grep -n \"accident-date conflict: the intake\" evals/golden/check_golden.py; grep -n \"self_report_spans\" evals/golden/README.md | cut -c1-80; grep -n \"authority\\|maintained here\" evals/golden/README.md | cut -c1-140"
}
````

### User / tool · 2026-11-02T01:00:57.598Z

**tool result**
````
evals/golden/case_01_date_formats.expected.json:175:      "spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:74:      "spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:120:      "spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:157:      "spans": [
evals/golden/sample.expected.json:109:      "spans": [
evals/golden/sample.expected.json:272:      "spans": [
51:AI assistance: this chronology was drafted with AI assistance and every item was review
52:Pending items: 0.
56:- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record
59:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may repres
65:- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended
70:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states sy
806:        "Patient states her neck pain is due to the collision.",
813:        "Patient states symptoms began after the collision; no physician states they are due to the collision.",
547:        else:   # accident-date conflict: the intake-form line is quoted; the EMS/ER records are cited by number
40:      "self_report_spans": [{"excerpt": "verbatim subjective sentence", "sour
72:* **Entries.** Found when the product emits an entry that covers `record_nos`
99:12. **Export golden (round 3).** `sample.export.expected.txt` is now maintained here (started from REQUIREMENTS §6). Changes: total line
152:Text packets only (no PDF/OCR of images). No multi-patient or multi-accident packets. These golden files are the authority on expected o
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:00:58.930Z

**tool call — Bash**
````
{
 "command": "sed -n 795,820p evals/golden/sample.expected.json"
}
````

### User / tool · 2026-11-02T01:00:59.028Z

**tool result**
````
        "Symptoms due to the motor vehicle accident.",
        "The treating physician concluded the symptoms were caused by the January collision.",
        "Collision-related disc protrusion.",
        "Injuries sustained in the collision.",
        "MRI findings are consistent with a traumatic disc injury.",
        "Post-traumatic headaches.",
        "Neck pain from the January collision.",
        "Injured in the collision.",
        "The crash resulted in a disc protrusion.",
        "Disc protrusion because of the collision.",
        "Patient states the collision caused his symptoms.",
        "Patient states her neck pain is due to the collision.",
        "Persistent neck pain 6/10; prior low back pain (2023) aggravated by the collision."
      ],
      "good_examples": [
        "Patient states symptoms began after the January collision.",
        "Per the patient, symptoms began after the January collision.",
        "Symptoms began after the January collision per patient report; no physician causation opinion is stated.",
        "Patient states symptoms began after the collision; no physician states they are due to the collision.",
        "Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache."
      ],
      "pattern": "(?i)\\b(caused by|due to|result(?:ing|ed)? (?:from|of|in)|secondary to|attributable to|attributed to|stemming from|because of|aggravat\\w+\\s+(?:by|from|in))\\s+(?:the\\s+)?(?:\\w+\\s+){0,3}(?:collision|accident|crash|MVA|trauma)|\\b(?:collision|accident|crash|MVA|trauma)[- ](?:related|induced|caused)\\b|\\bsustained (?:in|during|from)\\s+(?:the\\s+)?(?:\\w+\\s+)?(?:collision|accident|crash)|\\btrauma(?:tic)?\\b|\\bfrom the (?:\\w+\\s+){0,2}(?:collision|accident|crash)|\\binjured in\\b|\\b(?:collision|accident|crash|MVA)\\s+(?:caused|resulted in|led to)\\b|\\bresulted in\\b",
      "unless_context": "(?i)\\b(no|not|without|neither)\\b[^.;:]{0,40}$"
    },
    {
      "id": "M3",
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:01:39.180Z

I have enough evidence. I'll check the r2 jsoncheck script so I can reuse it for both r3 files.

### Assistant · claude-opus-5-5 · 2026-11-02T01:01:40.262Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-015-r2-paralegal-jsoncheck.py; grep -n \"service_date_in_excerpt\" evals/golden/case_09*.json | head -2; grep -n \"follow_up_not_kept\" evals/golden/case_09*.json | head -2"
}
````

### User / tool · 2026-11-02T01:01:40.358Z

**tool result**
````
"""Parse the single JSON block in reviews/T-015-paralegal-r2.md and check the s7.4 verdict rule."""
import json, re
from pathlib import Path
t = Path(__file__).resolve().parents[2].joinpath("reviews/T-015-paralegal-r2.md").read_text()
blocks = re.findall(r"```json\n(.*?)\n```", t, re.S)
assert len(blocks) == 1, len(blocks)
d = json.loads(blocks[0])
sev = [f["severity"] for f in d["findings"]]
exp = "fail" if "blocker" in sev else "changes" if "major" in sev else "pass"
print("verdict", d["verdict"], "expected", exp, {k: sev.count(k) for k in sorted(set(sev))}, "whats_right", len(d["whats_right"]))
assert d["verdict"] == exp
157:      "service_date_in_excerpt": "2026-02-02"
253:      "subtype": "follow_up_not_kept"
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:01:41.313Z

Now I'll write the paralegal r3 review.

### Assistant · claude-opus-5-5 · 2026-11-02T01:02:39.430Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r3.md",
 "content": "# T-015 round 3 (final): paralegal-reviewer (Maria Delgado lens)\n\n**Verdict: fail** (1 blocker, 2 majors, 3 minors).\n\nThe r2 blocker is fixed. Flag matching now requires overlapping evidence plus one-to-one assignment, so a single record-7 \"New onset pain\" causation flag scores K4 only and causation recall is 4/5. That was my r2 acceptance test, and it passes in both the checker's fixtures and my own probe. The K5 intake-date line is in the causation bullet. Record 1 is listed under \"flagged language quoted in the letter\". The bills-to-request line matches the R-EX-4 example exactly. The letter total line is D-019 exact. All 9 letter quotes are verbatim from the record they are cited to, and every export summary meets its required_terms on the summary alone.\n\nThree problems remain.\n- **Blocker.** The byte-exact export golden still does not quote the EMS side of the accident-date conflict. REQUIREMENTS §6 block 2 and R-FL-2 require both sides quoted. REQUIREMENTS §8 row 1 assigned this re-extraction to T-015 r3, and its own grep still fails. A product built to the spec fails ship bar 8. A product that drops the EMS quote passes.\n- **Major.** The self-report spans live under the JSON key `spans`, but README and check_golden.py read `self_report_spans`. The D-022 span checks never run. Mutation proof: an objective, wrong-kind span passes `check_golden.py`.\n- **Major.** The notes block has an AI-assistance line that differs from R-EX-4(1), a stale `Pending items: 0.` line, and a stray period. README says the golden is the authority, while REQUIREMENTS §8 says the golden must match §6. The two disagree byte for byte.\n\nCommands run (exact output):\n- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered`, EXIT=0\n- `git status --porcelain evals/golden/` → (empty); `git log -1 --format=%h -- evals/golden` → `f8c1948`\n- `.venv/bin/python -I artifacts/review-evidence/T-015-r2-paralegal-probe.py` → `T-015-r3-paralegal-rerun-of-r2-probe.out.txt`. Sections 1-7 ran. Section 8 raised `KeyError: 'display'`, which is expected because totals were split into letter_line/ui_line/notes_lines. Section 4 still simulates the old type+cite rule, so it is superseded by probe A below.\n- `.venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py` → `T-015-r3-rerun-of-r2-nurse-probe.out.txt`: `COUNTS [(('r1','OK'),36), (('r1','n/a(hit)'),2), (('r2','FALSEPOS'),2), (('r2','LEAK'),3), (('r2','OK'),45)]`\n- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-probe.py` → `.out.txt`. This pulls the reference matcher out of check_golden.py with ast and covers: K4/K5 matching, span keys, summary-only checks on the export, the conflict bullet, an independent rebuild of the flagged-language and bills sections, and the nurse r2 items.\n- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-s6diff.py` → `notes == s6 block2: False` (3 differing lines; `letter == s6 block1: True`)\n- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-mutation.py <scratch copy>` → baseline exit=0; objective span under `spans` exit=0 (not caught); same span under `self_report_spans` exit=1 (caught)\n- REQUIREMENTS §8 greps: `grep -n \"Pending items: 0\" evals/golden/sample.export.expected.txt` → `52:Pending items: 0.` (row 1 expects no match). `grep -n \"patient_self_report\\|summary+excerpt\" ...README.md ...sample.expected.json` → `sample.expected.json:638: \"subtype\": \"patient_self_report\"` (row 4 expects no match). `grep -n \"Known spec mismatches\" README.md` → no match (row 3 OK).\n\n```json\n{\"card\": \"T-015\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"round 3 (final, s7.4), commit f8c1948 (git diff 3c5eb7c..f8c1948 -- evals/golden): README.md, sample.expected.json, sample.export.expected.txt, case_01..09 .expected.json, hallucinations*.jsonl, check_golden.py; refs spec/REQUIREMENTS.md s6, s8 rows 1/3/4, R-FL-2, R-FL-4, R-FL-7, R-EX-4, R-EX-6, R-EX-8; memory/ORCHESTRATOR_DECISIONS.md D-019, D-021, D-022 (binding). No app (pre-code eval data); sample case evals/golden/sample.txt\",\n \"exercised\": [\n  \"python3 tools/board.py show T-015 (AC 1-4, r3 handoff)\",\n  \"python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0\",\n  \"git status --porcelain evals/golden/ (empty); git log -1 --format=%h -- evals/golden -> f8c1948; git diff 3c5eb7c..f8c1948 -- README.md sample.export.expected.txt (read in full)\",\n  \"re-ran r2 paralegal probe against f8c1948 -> T-015-r3-paralegal-rerun-of-r2-probe.out.txt (s1-s7 ran; s8 KeyError 'display' because totals were renamed; s4 old-rule simulation superseded)\",\n  \"re-ran r2 nurse probe against f8c1948 -> T-015-r3-rerun-of-r2-nurse-probe.out.txt (r1 36 OK; r2 45 OK, 3 LEAK, 2 FALSEPOS)\",\n  \"T-015-r3-paralegal-probe.py: reference matcher flag_matches/assign extracted from check_golden.py via ast, 11 K4/K5/C1 fixtures; span-key inventory across all 10 expected.json; export summaries vs required_terms and span attribution on the summary alone; conflict-bullet / AI-line checks; independent rebuild of R-EX-4(4) flagged-language and R-EX-4(8) bills from sample.expected.json; per-record quote verification of all 9 letter quotes; nurse r2 items\",\n  \"T-015-r3-paralegal-s6diff.py: byte diff of golden notes block vs REQUIREMENTS s6 block 2\",\n  \"T-015-r3-paralegal-mutation.py on a scratchpad copy of evals/golden: objective span under 'spans' vs 'self_report_spans'\",\n  \"REQUIREMENTS s8 reconciliation greps for rows 1, 3, 4 (literal)\",\n  \"compared sample.export.expected.txt line by line with the 9 records in sample.txt\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 4, \"arithmetic_and_dates\": 5, \"appendix_c_fidelity\": 4, \"flag_levels_realism\": 5, \"adjuster_attack_coverage\": 4, \"must_not_strength\": 4, \"export_golden_consistency\": 2, \"synthetic_labeling\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Export golden's accident-date conflict bullet quotes only the intake-form side. Record 1's 'rear-ended' sentence is not quoted, the bullet does not say the tool does not choose between the dates, and the byte-exact golden makes this weaker form the required output.\",\n   \"evidence\": \"sample.export.expected.txt:56 '- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (...): \\\"Date of accident per intake form: 2026-01-19.\\\"' REQUIREMENTS s6 block 2 has: 'record 7 (...): \\\"Date of accident per intake form: 2026-01-19.\\\" Record 1 (Austin EMS run report, January 9, 2026): \\\"41M restrained driver, rear-ended at approx. 35 mph.\\\" Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.' (T-015-r3-paralegal-s6diff.out.txt). R-FL-2: 'shown as a conflict and not merged, with both sides quoted (R-EX-4)'. REQUIREMENTS s8 row 1 assigns 'the accident-date conflict line still describes records 1 and 2 in tool wording instead of quoting both sides' to T-015 r3 (qa). check_golden.py:547 encodes the weaker form: '# accident-date conflict: the intake-form line is quoted; the EMS/ER records are cited by number'. Probe D: quotes record 1 'rear-ended' sentence: False; says tool does not choose: False. sample.expected.json C1 lists (1, excerpt, 'rear-ended at approx. 35 mph') as evidence.\",\n   \"why_it_matters\": \"Checklist 7 says the conflict is flagged with both excerpts. When the adjuster raises the 01-19 intake date, my attorney needs the EMS sentence that fixes the collision on 01-09 next to it, in my notes, quoted. 'Show treatment on that date' is tool wording, not the record. R-EX-6 makes this file the byte-exact E2E reference, so a product that follows R-FL-2 fails ship bar 8, and one that drops the EMS quote passes. The eval rewards the weaker conflict note.\",\n   \"fix\": \"Re-extract the INTERNAL_NOTES_TEXT block from REQUIREMENTS s6 block 2, as s8 row 1 directs. Change check_golden.py:547 so the C1 bullet must contain every C1 field-'excerpt' evidence item verbatim (record 7 intake line and record 1 'rear-ended at approx. 35 mph'), the phrase 'does not choose', and no computed delay.\",\n   \"acceptance_test\": \"T-015-r3-paralegal-s6diff.py prints 'notes == s6 block2: True'. Deleting the record-1 quote from the C1 bullet in a scratch copy makes check_golden.py exit 1.\"},\n  {\"severity\": \"major\", \"title\": \"Self-report spans are stored under 'spans', but README and check_golden.py read 'self_report_spans'. The D-022 span checks and the export attribution check never run.\",\n   \"evidence\": \"README.md:40 schema key 'self_report_spans'. check_golden.py:195 and :455 'e.get(\\\"self_report_spans\\\", [])'. The JSON uses '\\\"spans\\\"' at sample.expected.json:109, :272; case_01_date_formats.expected.json:175; case_06_subtle_pre_existing.expected.json:74, :120, :157. Probe B: 'entries with self_report_spans items = 0; with spans items = 6'. Mutation (T-015-r3-paralegal-mutation.out.txt): sample E1 span set to 'Alert and oriented' with source_kind 'WRONG' under 'spans' -> exit=0 'golden OK'. The same mutation under 'self_report_spans' -> exit=1 'span contains objective/assessment content: Alert and oriented'. Probe B: case_01 E8 ('Patient reports no new symptoms'), case_06 E3 ('History: occasional stiffness ...') and case_06 E5 ('Patient notes the old shoulder problem is acting up again') have attribution_also_in_required_terms=False, so their attribution is enforced nowhere. The handoff says 'self_report_spans per sentence with attribution_any ... Verified'.\",\n   \"why_it_matters\": \"Checklist 23 says patient self-reports stay attributed, and D-022 (binding) moved that check onto spans. A runner built from the README schema reads an empty list and scores the self-report rule as vacuously passed. A tool that turns 'Patient notes the old shoulder problem is acting up again' into a provider finding would score full marks. The validator's claim to cover D-022 is false, though the span data itself is correct (all 6 spans are subjective sentences, probe B objective_hit=False).\",\n   \"fix\": \"Rename 'spans' to 'self_report_spans' in all six entries (or rename README and checker, but make all three agree). Have check_golden.py fail on any unknown entry key, so a future rename can't silently disable a check.\",\n   \"acceptance_test\": \"T-015-r3-paralegal-mutation.py's first mutation (objective span under the key the JSON uses) makes check_golden.py exit 1. A key inventory finds 6 'self_report_spans' items and 0 'spans'.\"},\n  {\"severity\": \"major\", \"title\": \"Notes block still differs from REQUIREMENTS s6 block 2: the AI-assistance line is not the R-EX-4(1) fixed text, a stale 'Pending items: 0.' line remains, and the K5 line has a stray period. README and REQUIREMENTS each name themselves the authority.\",\n   \"evidence\": \"sample.export.expected.txt:51 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' and :52 'Pending items: 0.' R-EX-4(1) fixed text: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.' :59 ends '2026-01-19.\\\".' while s6 ends '2026-01-19.\\\"'. s8 row 1 check: `grep -n \\\"Pending items: 0\\\" evals/golden/sample.export.expected.txt` -> '52:Pending items: 0.' (expects no match). README.md:99 'now maintained here'; README.md:152 'These golden files are the authority on expected outputs where REQUIREMENTS lags'. REQUIREMENTS s8: 'evals/golden/ (qa, T-015 round 3)' with row 1 'section 6 block 2 is the text to re-extract'.\",\n   \"why_it_matters\": \"R-EX-6 makes this a byte-for-byte E2E target. A product that implements R-EX-4(1) word for word fails it. 'Every item was reviewed by the paralegal' also claims more than the product tracks: R-EX-4(1) scopes the claim to the treatment section and states the unreviewed count, which is the number I check before export (checklist 17). With two documents each claiming authority and disagreeing, the implementer has to guess.\",\n   \"fix\": \"Re-extract block 2 from s6 together with the blocker fix. Remove the 'authority where REQUIREMENTS lags' sentence, or narrow it to items s8 actually lists as golden-owned. Have check_golden.py compare the notes block to s6 block 2 the way the r2 probe does.\",\n   \"acceptance_test\": \"grep -n 'Pending items: 0' evals/golden/sample.export.expected.txt -> no match. check_golden.py fails when the golden notes block differs from REQUIREMENTS s6 block 2.\"},\n  {\"severity\": \"minor\", \"title\": \"Reference matcher's either-way substring overlap still lets broad evidence earn both K4 and K5, and lets a one-word fragment earn K4\",\n   \"evidence\": \"Probe A (assign/flag_matches taken from check_golden.py): 'TWO flags both quoting whole record 7 (neither about intake date): got [K4, K5]'; 'K4 sentence + a second flag quoting whole record 7: got [K4, K5]'; '1-word fragment pain on record 7: got [K4]'. check_golden.py:94-96 overlap() = 'na in nb or nb in na'.\",\n   \"why_it_matters\": \"The r2 failure mode is closed (one 'New onset' flag = K4 only). But a tool that emits two record-7 causation flags quoting the whole note, neither about the intake date, still gets 5/5 causation recall. The intake line is at least visible inside the quoted evidence, which is why this is minor.\",\n   \"fix\": \"Before assignment, collapse candidates with identical (type, evidence) into one. Require the candidate excerpt to contain the golden excerpt, or to cover at least 50% of its normalized length, rather than allowing any substring either way.\",\n   \"acceptance_test\": \"New check_golden fixtures: two identical whole-record-7 causation candidates -> {K4} or {K5}, not both. Candidate 'pain' -> {}.\"},\n  {\"severity\": \"minor\", \"title\": \"K3 flag still carries subtype 'patient_self_report' and no source_kind 'patient_report' (R-FL-7); REQUIREMENTS s8 row 4 grep still matches\",\n   \"evidence\": \"sample.expected.json:638 '\\\"subtype\\\": \\\"patient_self_report\\\"'. Probe output for K3: 'source_kind=None'. R-FL-7: 'Sample record 9 flag has source_kind == \\\"patient_report\\\"'. s8 row 4 check: `grep -n \\\"patient_self_report\\\\|summary+excerpt\\\" README.md sample.expected.json` (expects no match) -> 1 match.\",\n   \"why_it_matters\": \"The runner can't take R-FL-7's assertion from the golden, and the s8 check can't close.\",\n   \"fix\": \"Add 'source_kind': 'patient_report' to K3, and rename the subtype (e.g. 'patient_reported_onset').\",\n   \"acceptance_test\": \"The s8 row 4 grep returns nothing; K3.source_kind == 'patient_report'.\"},\n  {\"severity\": \"minor\", \"title\": \"M2 good_examples present tool commentary on causation ('no physician causation opinion is stated') as acceptable summary wording\",\n   \"evidence\": \"sample.expected.json:812-813 good_examples 'Symptoms began after the January collision per patient report; no physician causation opinion is stated.' and 'Patient states symptoms began after the collision; no physician states they are due to the collision.' The regex applies to tool-authored text including letter summaries (README 'must_not' regex scope).\",\n   \"why_it_matters\": \"In my treatment section, a tool sentence saying no doctor supports causation is a gift to the adjuster and flag-like content that R-EX-1 keeps out of the letter. It belongs in internal notes if anywhere. Golden good examples read as house style.\",\n   \"fix\": \"Replace both with record-words examples (e.g. 'Per patient, symptoms began after the January collision.'). Add a letter-surface must_not for '\\\\bno (physician|doctor|provider)\\\\b.{0,40}\\\\b(states|opinion)'.\",\n   \"acceptance_test\": \"No M2 good_example contains 'no physician'. The new must_not fires on both strings and not on the four record-words good examples.\"}\n ],\n \"whats_right\": [\n  \"K4/K5 are now separately enforceable: the reference matcher plus fixtures give 'New onset' alone K4 only (recall 4/5), and the K5 intake line sits in its own causation bullet.\",\n  \"The letter block is clean demand text: 9 verbatim quotes each verified against its own record, US long dates, header labels as written, two charges, and 'Billed charges stated in these records: $8,390.00' with nothing after it (D-019).\",\n  \"check_golden.py rebuilds the flagged-language and bills-to-request sections from the JSON and the R-EX-4 rules. My independent rebuild agrees, and the bills line equals the R-EX-4 example exactly.\"\n ],\n \"questions_for_chris\": [\n  \"When README (golden is the authority) and REQUIREMENTS s8 (golden must match s6) disagree on the export notes block, which file wins for the M1 byte-exact test?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T01:02:39.602Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:02:40.729Z

Now the nurse-checklist r3 review, judged strictly against the nurse's r2 findings.

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:15.528Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-015-legal-nurse-r3.md",
 "content": "# T-015 Eval golden set, round 3 (final): legal-nurse checklist\n\n**Scope note:** the **paralegal-reviewer** agent (Opus 5.5) wrote this review at the orchestrator's request (D.6 brief, round 3). It is judged strictly against the legal-nurse r2 findings in `reviews/T-015-legal-nurse-r2.md`, not against the paralegal checklist. Clinical judgment beyond those findings is outside this agent's lens.\n\n**Verdict: changes** (0 blockers, 1 major, 3 minors).\n\n| r2 finding | r3 status | Evidence |\n|---|---|---|\n| M1 required_terms on summary+excerpt | **Fixed** | README.md:72 'a **summary** that by itself satisfies every `required_terms` item'. The nurse probe's 4 omission summaries (E1/E2/E8/E9) give `pass_on_summary_only=False`, so they now fail. E2/E8/E9 carry any-of qualifier alternatives. All 9 export summaries pass on the summary alone (probe C). check_golden.py:189-193 grounds every term in the record. |\n| M2 patient-attributed causation allowed | **Fixed in substance** | 'Patient states her neck pain is due to the collision.' moved to bad_examples (sample.expected.json:806). M10 bad_examples include 'Patient states the collision caused his symptoms.' H35-H37 `temporal_to_causal` were added and REQ_CAT requires the category. Residual (minor): the literal r2 acceptance grep still finds a good_example with 'due to the collision' (:813). |\n| M3 source_kind on whole mixed entries | **Data fixed, checks dead** | Entry-level source_kind is gone. 6 per-sentence spans use `patient_report`, and all are subjective (probe B objective_hit=False). But they are stored under `spans` while README and check_golden.py read `self_report_spans`, so the r2 acceptance test (the checker asserts span verbatim and no objective content) never runs. A mutation passes. K3 flag lacks R-FL-7 `source_kind`. |\n| minor: regex leaks (30 of 50) | **27 of 30 closed** | Re-run: `('r2','LEAK'),3`. 'Diagnosed with cervical strain and concussion; CT head negative.' is now caught by summary-only required_terms (D-022). Still leaking: 'Findings may represent degenerative disc disease.' and 'Cervical disc disease at C5-C6.' |\n| minor: controls S08/S10 | **Fixed** | S08 'The patient has seen a chiropractor ...' (no sex); S10 'pain radiating to the right arm'; check_golden.py:596 rejects invented pronouns |\n| minor: missing judge items | **Fixed** | H38/H39 approximation_dropped, H40 abbreviation_misexpanded ('PT' -> 'prothrombin time'), SE5 kind judge_masked 'Visit 8: pain 8/10, improving.' -> needs_review |\n| nit: case_01 'fracture' | **Fixed** | case_01 E1 required_terms ['ankle', 'negative for fracture'] |\n\nCommands run: `python3 evals/golden/check_golden.py` → `golden OK: ... 57 must_nots ..., 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase) ...` EXIT=0. `.venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py` → `T-015-r3-rerun-of-r2-nurse-probe.out.txt`. `T-015-r3-paralegal-probe.py` (sections B, C, F) and `T-015-r3-paralegal-mutation.py` on a scratch copy.\n\n```json\n{\"card\": \"T-015\", \"persona\": \"legal-nurse-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"round 3 (final), commit f8c1948 (git diff 3c5eb7c..f8c1948 -- evals/golden), judged strictly against reviews/T-015-legal-nurse-r2.md findings; written by the paralegal-reviewer agent against the legal-nurse checklist at orchestrator request. Files: README.md, sample.expected.json, case_01/06/08 expected.json, hallucinations.jsonl (40), hallucinations_controls.jsonl (10), sample.export.expected.txt summaries, check_golden.py; decisions D-021, D-022; spec R-FL-7, R-TL-10. No app (pre-code card).\",\n \"exercised\": [\n  \"python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0\",\n  \".venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py against f8c1948 -> T-015-r3-rerun-of-r2-nurse-probe.out.txt: COUNTS r1 OK 36, n/a 2; r2 OK 45, LEAK 3, FALSEPOS 2; omission probe pass_on_summary_only=False for E1/E2/E8/E9\",\n  \"T-015-r3-paralegal-probe.py section B (span key inventory, objective-content regex on each span), C (export summaries vs required_terms and span attribution, summary alone), F (M2 examples, hallucination categories, S08/S10, M10, seeded edits, case_01 E1)\",\n  \"T-015-r3-paralegal-mutation.py on a scratchpad copy: objective span under 'spans' -> exit 0; under 'self_report_spans' -> exit 1\",\n  \"read sample.expected.json M2 bad/good examples (:795-815) and K3 (:638); README.md:40 and :72\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"clinical_fidelity_of_reference_wording\": 4, \"appendix_c_must_not_check_reliability\": 4, \"hallucination_set_genuineness\": 5, \"hallucination_failure_mode_coverage\": 5, \"controls_faithfulness\": 5, \"objective_vs_subjective_coverage\": 3, \"summary_omission_measurement\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"r2 M3 acceptance test still fails: per-sentence self-report spans are correct but sit under key 'spans', so check_golden.py never validates them and a runner built from the README never scores them\",\n   \"evidence\": \"README.md:40 and check_golden.py:195, :455 read 'self_report_spans'; the JSON uses '\\\"spans\\\"' (sample.expected.json:109, :272; case_01_date_formats.expected.json:175; case_06_subtle_pre_existing.expected.json:74, :120, :157). Probe B: 'self_report_spans items = 0; spans items = 6'. Mutation: sample E1 span 'Alert and oriented', source_kind 'WRONG', under 'spans' -> check_golden exit=0. Under 'self_report_spans' -> exit=1 'span contains objective/assessment content'. case_01 E8, case_06 E3 and case_06 E5 attribution appear in no required_terms (probe B attribution_also_in_required_terms=False).\",\n   \"why_it_matters\": \"The r2 point was that the subjective/objective split must be encoded exactly and checked. The encoding is now right, but the check that would catch a future regression (an exam finding tagged as patient report) is dead. The eval also can't fail a summary that states 'History: occasional stiffness at baseline' or 'old shoulder problem is acting up again' as the provider's finding.\",\n   \"fix\": \"Rename 'spans' to 'self_report_spans' in the six entries (or align README and checker the other way). Make check_golden.py reject unknown entry keys.\",\n   \"acceptance_test\": \"The objective-span mutation under the JSON's key makes check_golden.py exit 1. A summary for case_06 E5 without 'patient notes/reports/states/per patient' is not found.\"},\n  {\"severity\": \"minor\", \"title\": \"K3 flag has no source_kind 'patient_report' (R-FL-7 value name) and keeps subtype 'patient_self_report'\",\n   \"evidence\": \"sample.expected.json:638 '\\\"subtype\\\": \\\"patient_self_report\\\"'; probe: K3 source_kind=None. R-FL-7: 'Sample record 9 flag has source_kind == \\\"patient_report\\\"'. The r2 M3 fix asked to 'Use R-FL-7's value name'.\",\n   \"why_it_matters\": \"The one flag that rests on the patient's own statement is the one R-FL-7 asserts on. Without the field, the runner can't check that the flag is never presented as a physician's opinion.\",\n   \"fix\": \"Add 'source_kind': 'patient_report' to K3 and rename the subtype.\",\n   \"acceptance_test\": \"K3.source_kind == 'patient_report'; grep 'patient_self_report' evals/golden/ returns nothing.\"},\n  {\"severity\": \"minor\", \"title\": \"r2 M2 literal acceptance grep still matches a good_example, and two M2 good_examples are tool commentary on causation rather than the record's words\",\n   \"evidence\": \"`grep -n 'due to the collision' evals/golden/sample.expected.json` -> :806 (bad_example, correct) and :813 good_example 'Patient states symptoms began after the collision; no physician states they are due to the collision.' :812 good_example '... per patient report; no physician causation opinion is stated.'\",\n   \"why_it_matters\": \"The substance of r2 M2 is fixed. But a good example that comments on what no physician said is a judgment about the record set, not a faithful summary. It also drops 'January' from the record's 'January collision'.\",\n   \"fix\": \"Replace both with record-words examples, e.g. 'Per patient, symptoms began after the January collision.'\",\n   \"acceptance_test\": \"No M2 good_example contains 'due to' or 'no physician'.\"},\n  {\"severity\": \"minor\", \"title\": \"Two regex-floor leaks from r2 remain: 'degenerative disc disease' under a hedge, and 'disc disease' without 'degenerative'\",\n   \"evidence\": \"T-015-r3-rerun-of-r2-nurse-probe.out.txt: 'r2 V LEAK M3 M8 Findings may represent degenerative disc disease. -> {}' and 'r2 V LEAK M1 M8 M3 Cervical disc disease at C5-C6. -> {}'. (The third leak, the dropped LOC qualifier, is now caught by summary-only required_terms.)\",\n   \"why_it_matters\": \"The record says 'degenerative change'. 'Degenerative disc disease' and 'disc disease' are diagnoses the radiologist did not make, and a hedge does not make a new diagnosis faithful. Judge #1 is the only backstop.\",\n   \"fix\": \"Add a sample regex for '\\\\bdisc disease\\\\b|\\\\bDDD\\\\b' with no hedge exemption (the record never uses the term).\",\n   \"acceptance_test\": \"Both probe strings become bad_examples that fire; 'Findings may represent degenerative change' stays a good example.\"}\n ],\n \"whats_right\": [\n  \"D-022 is implemented for entries: required_terms are summary-only with any-of qualifier alternatives, so dropping 'without loss of consciousness', the MRI hedge or 'patient states' now fails, and all 9 export summaries pass.\",\n  \"The hallucination set (40) and controls (10) now cover temporal-to-causal, approximation dropped, abbreviation mis-expansion and the masked pain-score swap (SE5), and the controls no longer invent sex or drop 'radiating'.\",\n  \"Every self-report span is a verbatim subjective sentence (C/O, patient states, denies, history, patient notes), and none carries an exam finding or assessment.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T01:03:15.698Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-015-legal-nurse-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:19.103Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-015-r3-paralegal-jsoncheck.py <<'EOF'\n\"\"\"Parse the single JSON block in each r3 review and check the s7.4 verdict rule.\"\"\"\nimport json, re\nfrom pathlib import Path\nroot = Path(__file__).resolve().parents[2]\nfor name in (\"reviews/T-015-paralegal-r3.md\", \"reviews/T-015-legal-nurse-r3.md\"):\n    t = root.joinpath(name).read_text()\n    blocks = re.findall(\"`\" * 3 + r\"json\\n(.*?)\\n\" + \"`\" * 3, t, re.S)\n    assert len(blocks) == 1, (name, len(blocks))\n    d = json.loads(blocks[0])\n    sev = [f[\"severity\"] for f in d[\"findings\"]]\n    exp = \"fail\" if \"blocker\" in sev else \"changes\" if \"major\" in sev else \"pass\"\n    print(name, d[\"persona\"], \"verdict\", d[\"verdict\"], \"expected\", exp, {k: sev.count(k) for k in sorted(set(sev))}, \"whats_right\", len(d[\"whats_right\"]))\n    assert d[\"verdict\"] == exp and len(d[\"whats_right\"]) <= 3\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-jsoncheck.py; python3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T01:03:19.272Z

**tool result**
````
reviews/T-015-paralegal-r3.md paralegal-reviewer verdict fail expected fail {'blocker': 1, 'major': 2, 'minor': 3} whats_right 3
reviews/T-015-legal-nurse-r3.md legal-nurse-reviewer verdict changes expected changes {'major': 1, 'minor': 3} whats_right 3
ok (28 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:20.110Z

Both review files validate. Last, I'll update memory with the new recurring patterns.

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:24.349Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md",
 "old_string": "**Why:** these let a weaker product",
 "new_string": "Round 3 (commit f8c1948, verdict fail) added these patterns:\n- Schema key drift can silently disable a check. The JSON used `spans` while README and check_golden read `self_report_spans`, so the D-022 checks ran on empty lists and the validator stayed green. Count keys across all JSON files, and mutation-test every new assertion on a scratchpad copy (break the data, and the checker must exit 1).\n- The writer fixes the line the reviewer named (the K5 line) and leaves the sibling lines that REQUIREMENTS §8 also listed (the C1 conflict bullet quoting both sides, the AI line). Byte-diff the golden against REQUIREMENTS §6 every round, and run the §8 reconciliation greps literally.\n- Either-way substring overlap in the reference matcher lets a whole-record excerpt satisfy every golden flag on that record. Probe with whole-record and one-word candidates.\n\n**Why:** these let a weaker product"
}
````

### User / tool · 2026-11-02T01:03:24.450Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:26.272Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export golden vs JSON drift, regex probes",
 "new_string": "- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)"
}
````

### User / tool · 2026-11-02T01:03:26.368Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T01:03:34.060Z

The paralegal review is **fail** (1 blocker, 2 majors, 3 minors). The nurse-checklist review is **changes** (1 major, 3 minors). `check_golden.py` passes (exit 0) and `board.py validate` returns ok. My r2 K4/K5 blocker is fixed: one "New onset" record-7 causation flag now earns K4 only, so causation recall is 4/5. Both r2 probes were re-run against f8c1948; the nurse probe leaks dropped from 30 to 3.

- **Blocker:** the expected export's accident-date conflict line quotes only the intake-form date. It doesn't quote record 1's "rear-ended" sentence, which R-FL-2 and REQUIREMENTS §6 require. The export test compares byte for byte, so a spec-correct product would fail it. REQUIREMENTS §8 row 1 gave this re-extraction to T-015 r3, and `check_golden.py:547` encodes the weaker form.
- **Major (in both reviews):** the self-report sentences are stored under the key `spans`, but the README and `check_golden.py` read `self_report_spans`. The self-report checks therefore never run. On a scratch copy, a span holding an exam finding with the wrong label still passed the checker.
- **Major (paralegal):** the export's AI-assistance line isn't the required wording, `Pending items: 0.` is still there (the §8 grep fails), and the K5 line has a stray period. The README and REQUIREMENTS each claim to be the authority, and they disagree.
- **Minors:**
  - Two record-7 causation flags that each quote the whole record still earn both K4 and K5.
  - The K3 flag has no `patient_report` label.
  - Two "good" examples of allowed wording comment that no physician supports causation.
  - Two "disc disease" phrasings still slip past the regex checks.

Files are in /Users/arsis/zlayt-pm-project:
- reviews/T-015-paralegal-r3.md
- reviews/T-015-legal-nurse-r3.md
- artifacts/review-evidence/T-015-r3-paralegal-probe.out.txt
- artifacts/review-evidence/T-015-r3-paralegal-s6diff.out.txt
- artifacts/review-evidence/T-015-r3-paralegal-mutation.out.txt
- artifacts/review-evidence/T-015-r3-rerun-of-r2-nurse-probe.out.txt
