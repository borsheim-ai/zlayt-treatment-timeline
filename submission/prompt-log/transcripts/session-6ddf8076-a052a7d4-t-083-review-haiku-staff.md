# Subagent: T-083 review (haiku staff) (T-083 review (haiku staff))

Source: `agent-a052a7d4c0612e376.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:25:21.955Z

Review board card T-083 in /Users/arsis/zlayt-pm-project (commit f218263: app/backend/billing.py, the GET /api/cases/{token}/billing route, tests/unit/test_billing.py). It's billing analysis on itemized ledgers, code only (D-042 in memory/ORCHESTRATOR_DECISIONS.md): billed, adjustment, paid and balance, each cited to a verbatim line; totals by provider; LOP and lien amounts separate; nothing totaled that isn't stated (D-019); rates never become charges.

Check against the traps in research/record-formats.md: CMS-1500 amounts with no decimal point, and a UB-04 rate on the charge line. Check that every figure's excerpt is a verbatim substring, that the arithmetic is right (recompute one ledger by hand), and that the tests fail when the rate guard is mutated in a scratch copy. Run `.venv/bin/python -m pytest -q tests/unit/test_billing.py`.

Write reviews/T-083-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:24.316Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:25:24.324Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:24.908Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/staff-engineer-reviewer/ && cat .claude/agent-memory/staff-engineer-reviewer/MEMORY.md && git log --oneline -3 f218263 && git show --stat f218263 | head -30",
 "description": "Read persona, memory index, and commit stats"
}
````

### User / tool · 2026-11-02T04:25:25.049Z

**tool result**
````
MEMORY.md
feedback_review_write_once.md
feedback_severity_vs_brief.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_r2_fix_verification_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_t065_batch_fallback_review_patterns.md
project_t066_no_model_reason_patterns.md
project_t067_r6_d043_patterns.md
project_t070_t067_review_patterns.md
project_t075_determinism_review_patterns.md
project_t080_trace_review_patterns.md
project_t093_signature_controls_patterns.md
project_wiring_review_patterns.md
- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad: J3 relabel after failure, controls gate without ADR, keyword-separable controls, scratch-mutant guard traps
f218263 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
7724412 fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
commit f218263298acd9939c9a9394fd0bbbfbd7c8f61d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:25:02 2026 -0600

    feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
    
    Code-only: ledger lines parse to billed/adjustment/paid/balance, each cited verbatim; totals by provider; LOP and lien amounts listed separately; rates, running balances, claim totals and EOB billed are never totaled. GET /api/cases/{token}/billing.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py         |   2 +
 app/backend/billing.py     | 642 +++++++++++++++++++++++++++++++++++++++++++++
 memory/contracts/api.md    |  37 +++
 tests/unit/test_billing.py | 330 +++++++++++++++++++++++
 4 files changed, 1011 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:27.719Z

**tool call — Bash**
````
{
 "command": "cat board/cards/T-083.md; echo ----; grep -n \"D-042\\|D-019\" -A8 memory/ORCHESTRATOR_DECISIONS.md | head -80; echo ----; ls research/ docs/ reviews/ | head -100",
 "description": "Read card T-083 and related decisions"
}
````

### User / tool · 2026-11-02T04:25:27.822Z

**tool result**
````
---
id: "T-083"
title: "Billing analysis on itemized ledgers: billed, adjusted, paid, LOP/lien (code only, cited)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:25:18Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: ["f218263"]
reviews: []
ac:
  - {"n": 1, "text": "Itemized ledger lines parse to billed/adjustment/paid/balance with each figure cited to its line; totals by provider; LOP/lien amounts listed separately; nothing totaled that is not stated; unit tests on synthetic ledgers", "done": true, "evidence": "tests/unit/test_billing.py: 27 passed (ledger table+prose, void netting, rate excluded, CMS-1500 implied decimals, UB-04 FL44 rate, EOB mismatch, LOP/lien separate, citations verbatim, route)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:25:10Z backend: AC 1 checked: tests/unit/test_billing.py: 27 passed (ledger table+prose, void netting, rate excluded, CMS-1500 implied decimals, UB-04 FL44 rate, EOB mismatch, LOP/lien separate, citations verbatim, route)
- 2026-11-02T04:25:10Z backend: UI needs (for a frontend card): GET /api/cases/{token}/billing (contract in api.md). A Billing panel per case: per-provider cards (billed, adjustment, paid, stated balance, 'complete' badge), expandable line table with the verbatim excerpt per line + highlight of the figure, line_flags/checks as stepper-style rows (code check pass/fail with both figures and cites; ledger-vs-EOB mismatch shows both documents' lines, no picking), separate 'LOP and lien amounts (not totaled)' list, separate 'Rates and excluded' list, skipped_records notice, and an 'internal view, not in the letter' label. Unclear figures show text with no value. All code-made: label 'checked by code', no judge step.
- 2026-11-02T04:25:10Z backend: moved in_progress -> in_review
- 2026-11-02T04:25:18Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: app/backend/billing.py (new, code only) + GET /api/cases/{token}/billing + api.md section; 2-line hook in api.py. Ledger tables (position-assigned columns), sentence ledgers, CMS-1500 (implied cents), UB-04 (FL44 rate excluded, 0001 compared), EOBs (never added; ledger-vs-EOB paid/billed checks), LOP/lien list. How verified: .venv/bin/python -m pytest -q tests/unit/test_billing.py (27 pass); full unit run 1260 pass, 2 unrelated fails (test_single_call_path in test_provider*.py: app/backend/pdf_ocr.py imports subprocess, T-086's file). Left: frontend panel (see note); no LLM step so no eval impact. Surprised: ADJ amounts are left-aligned under header while charges are right-aligned, so column match uses min(start,end) distance; demo mode refuses unrecorded text over HTTP so route test seeds via ingest_case.
----
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29-| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30-| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31-| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
32-| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
33-| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
34-| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
35-| D-027 | Two-digit years are never guessed: `03-17-98` is `date_ambiguous` with candidates (1998, 2098) and excluded from gap math until confirmed. Text outside recognised record blocks is never dropped: it becomes an 'unsplit text' record flagged for the paralegal. | 'Say so instead of guessing' (spec); silent drops lose facts. | T-032 staff review |
--
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
54-| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
----
docs/:
CONTRACT.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md
UI_DESIGN_BRIEF.md

research/:
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
case-library-sources-v2.md
case-library-sources.md
chronology-practice.md
lexicon_selfcheck.py
library_build.py
office-view-references.md
phi-and-ai-supervision.md
record-formats.md
record_formats_check.py
texas-pi-notes.md
ui-references.md
validate_library.py

reviews/:
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security-r3.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
T-026-ux-designer.md
T-027-legal-nurse.md
T-028-staff-engineer-r2.md
T-028-staff-engineer.md
T-029-staff-engineer-r2.md
T-029-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:28.337Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md .claude/agent-memory/staff-engineer-reviewer/feedback_severity_vs_brief.md .claude/agent-memory/staff-engineer-reviewer/project_backend_llm_review_patterns.md .claude/agent-memory/staff-engineer-reviewer/project_r2_fix_verification_patterns.md",
 "description": "Read relevant reviewer memory files"
}
````

### User / tool · 2026-11-02T04:25:28.424Z

**tool result**
````
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
---
name: severity-vs-brief
description: When the dispatch brief sets a default severity that conflicts with CONTRACT D.2 (for example "list mismatches as major"), rate per D.2 and state the deviation in the review
metadata:
  type: feedback
---

When the brief says to file a class of finding as a major, but the finding violates a spec constraint, rate it a blocker per CONTRACT D.2 (persona section 8) and say so in the review summary and in why_it_matters.

**Why:** T-063 brief said "list any mismatch as a major". The D-033 mismatch labelled a family member's statement as the patient's own self-report, which D-033 explicitly forbids. D.2 defines a spec-constraint violation as a blocker. I rated it a blocker, stated the deviation at the top of the review, and left the override to the orchestrator.

**How to apply:** for each finding, check the D.2 definition first; a brief's default is a starting point, not a cap. Put any deviation in the review's first paragraph so the orchestrator sees it without reading the JSON. Do not downgrade a finding to match a brief.

See also [[project_t063_doc_vs_code_review_patterns]].
---
name: backend-llm-review-patterns
description: T-035 r1 and T-033 r2 recurring findings - untested wiring, judge reason prose, label-window bleed in amount classification, scratch-copy controls
metadata:
  type: project
---

T-035 r1 (a2fc95a): pure-module tests (grounding, judges) pass while the stage module (generator.py) that wires them has none; mutate the call site in a scratch copy (cp -R app tests evals into scratchpad; avoid rm -rf, it is denied) to prove it.
**Why:** card ACs cite "scratch run" evidence and tests that depend on pipeline stubs (T-037), so nothing in the repo proves the wiring.
**How to apply:** on every backend LLM card, mutate the caller, not the helper; check ACs marked done whose named test fails.
Also check: judge schemas with a free `reason: str` vs LLM_VS_CODE row 5 / ADR-008.5 (enum only); labels (Source:) placed outside nonce delimiters.
Live check recipe: LLM_BACKEND=claude-cli, ingest.ingest(raw)["records"], DB.connect+create_case, audited.make_call -> generator.extract_one; 2 calls works and keeps "may represent" on record 8.

T-033 r2 (amounts.py): a fix that narrows the trigger words (per/each/rate -> per+unit noun) closes the reviewer's repro strings but leaves the six-word label window unbounded, so a rate phrase from the previous figure still leaks across a comma and reclassifies the next charge. Probe the same sentence with '.' and ',' in place of each other, and probe a figure after another figure's rate phrase, not only the reported strings.
**Why:** the r1 finding was a symptom (a charge reads as rate); the cause was the window, so word-list fixes recur.
**How to apply:** for any extraction/classification fix, re-run the original repro plus neighbouring-figure variants; check the window boundary, not only the trigger regex. Do not split on comma alone (it breaks 'Charge per visit, $185.').
Also: a scratch copy must include memory/ (tests read memory/contracts/*.md) or the full-suite control is invalid; cp -R of the tree minus .venv worked, an rsync-based copy was denied by the sandbox. Run mutations on test_<module>.py first, then the full suite only with a valid control.
T-035 r2: backend fixed both blockers well (9/9 scratch mutations killed); remaining = eval report/AC6 waiting on T-038/T-037.
T-038 (eval runner): gate code had `except Exception` fallbacks, ship_bar ignored runs>=3, --check-spec left stale ship_bar_met, tests assert only "ship_bar_met False" (mutate each bar term to check). Scratch copy needs memory/ dir too (tests read memory/contracts/api.md); run only test_eval_* files.
---
name: r2-fix-verification-patterns
description: T-058/T-055/T-059 r2 (2026-11-02): fix lands inside another card's commit, overstated mutant counts in commit messages, $-anchor sweep classification, word-list backstops miss diagnosis wording
metadata:
  type: project
---

Round-2 verification of fixes for T-058 (991dac4), T-055 (670ed09) and T-059 (06eb84b). All three were pinned by `git archive <fix-commit>` into artifacts/review-evidence/<card>-r2/head_<sha>; HEAD had moved 11 commits past 991dac4 and kept moving.

- **The fix can sit inside another card's commit.** T-058's regex fix is in 991dac4, whose subject is "patient_report chip ... (T-061 r4)" (shared git index). Find a fix by reading `git show --stat` and the diff for the named lines, not the subject line.
- **Commit-message and card mutant counts can be overstated.** T-055's commit says "drop the not_verified rule fails 3 tests"; reproduced: 2 (full `tests/unit`: 904 passed baseline, 2 failed with the rule dropped, both new state tests). Always reproduce the count and diff the FAILED sets (baseline vs mutant) before accepting a claimed number.
- **After a `$` to `\Z` sweep, classify every remaining `$`.** Value validators must end in `\Z` or use fullmatch. Line parsers with re.MULTILINE, lookaheads and context classifiers (`\s*$` on a label) are not validators. The one left in T-058 was `review.py:14` (`.search` on tokens that cannot contain a newline): nit, over-match only.
- **Word-list backstops test the listed words, not the banned category.** T-059's `_SEVERITY` covers the prompt's four adjectives (serious, severe, significant, ongoing) and recommendation/surgery words, but not "diagnosed as a herniation" or "a clear sign of nerve injury": both pass `check_sentence` and reach judge 1 alone. Probe each banned category with a sentence, not just the list.
- **Mutants that the r1 review named:** T-059 N3 (D-006 token check off) fails 5 tests, N11 (stale-basis clause off) 1, N12 (failed re-draft overwrites) 4, N13 (SEVERITY off) 4. T-058 round-1 regex restored fails exactly the two named cases (`[bad0]`, `[bad1]`).
- **Tracked fixtures are enough at these commits.** 670ed09 archive runs 904 passed with no working-tree fixtures copied; 06eb84b clean archive runs 928 passed (the narrative replay passes there). The known failure is the live working tree while another worker re-records narrative fixtures (`FixtureMiss`, step narrative). Not counted, as the brief says.

**Why:** a fix verified against HEAD, or a claimed mutant count taken on trust, proves nothing about the commit the card cites.
**How to apply:** pin to the card's fix commit; re-run each named mutant with its count; grep each validator family after a sweep; for a banned-wording rule, probe the category with a real sentence. Related: [[project_round2_snapshot_review_patterns]], [[project_split_llm_review_patterns]], [[project_harness_review_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:29.712Z

**tool call — Bash**
````
{
 "command": "cat research/record-formats.md",
 "description": "Read record formats research note"
}
````

### User / tool · 2026-11-02T04:25:29.799Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:29.987Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/billing.py | sed -n 1,220p",
 "description": "Read billing.py lines 1-220"
}
````

### User / tool · 2026-11-02T04:25:30.078Z

**tool result**
````
     1	"""Billing analysis on itemized ledgers, claim forms and EOBs (T-083, D-042). CODE ONLY: no model is asked anything here.
     2	
     3	What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
     4	record). Totals are per provider. LOP and lien amounts are listed separately and never added. Nothing is totaled that the records do not
     5	state (D-019): a rate is never a charge, a running balance is never summed, a claim-form total (UB-04 line 0001, CMS-1500 Item 28) is
     6	compared with the line sum and never added to it, an EOB's "amount billed" restates the bill and is never added, and a figure that cannot
     7	be read cleanly (OCR letters, odd decimals, a column that cannot be told apart) is LISTED with cents None and kept out of every total.
     8	The analysis is computed on read, never stored, and never reaches the letter: the letter's total line is still only accepted charges (D-019).
     9	Disagreements (ledger total vs line sum, ledger paid vs EOB paid, ...) are raised as `checks`; the code never picks a side.
    10	Money is whole cents (int); integer arithmetic only.
    11	"""
    12	import re
    13	
    14	from app.backend import amounts as A, dates
    15	
    16	# ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)
    17	CHECKS = {
    18	    "LEDGER_TOTAL_MISMATCH": "The statement's own total does not match the sum of its lines. Both figures are shown; check the original.",
    19	    "LEDGER_BALANCE_MISMATCH": "The stated balance does not equal the charges minus payments and adjustments on the parsed lines.",
    20	    "BALANCE_STEP_MISMATCH": "This line's running balance does not follow from the line before it, so a column may have been read wrongly.",
    21	    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed but not totaled.",
    22	    "CLAIM_TOTAL_MISMATCH": "The claim form's printed total does not match the sum of its lines. Both figures are shown.",
    23	    "CLAIM_LEDGER_BILLED_MISMATCH": "The claim form and the itemized ledger for this provider show different billed totals. The ledger is used; check both.",
    24	    "LEDGER_EOB_PAID_MISMATCH": "The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.",
    25	    "LEDGER_EOB_BILLED_MISMATCH": "The ledger's billed amount for this date and service differs from the amount billed on the EOB.",
    26	    "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
    27	}
    28	RULES = [
    29	    "Only figures stated in the records are totaled; nothing is derived or estimated.",
    30	    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is never a charge.",
    31	    "A running balance, a claim-form total and an EOB's amount billed are never added to the charges.",
    32	    "LOP, lien and attorney-reduction amounts are listed separately and never totaled with charges.",
    33	    "A figure that cannot be read cleanly is listed with no value and left out of every total.",
    34	    "This analysis is for review only. The letter's total line is still accepted charges only.",
    35	]
    36	
    37	# ------------------------------------------------------------------ money tokens
    38	_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
    39	_FIG = rf"\(?-?\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\.{_D}+\)?-?"
    40	_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
    41	_DATE = r"(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})"
    42	_ROW = re.compile(rf"^\s*({_DATE})\s+(?:({_DATE})\s+)?(.*)$")
    43	_VOID = re.compile(r"\b(?:void(?:ed)?|reverse[ds]?|reversal|rev\.?\s+chg)\b", re.IGNORECASE)
    44	_NEGOTIATED = re.compile(r"\b(?:atty|attorney|lawyer)\s+(?:reduction|adj\w*|discount)|\breduced\s+to\b|\bsettlement\s+(?:reduction|discount)\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
    45	_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
    46	_COLS = {"billed": re.compile(r"\b(?:CHARGES?|BILLED)\b", re.IGNORECASE), "paid": re.compile(r"\b(?:PAYMENTS?|PMTS?|PAID)\b", re.IGNORECASE),
    47	         "adjustment": re.compile(r"\b(?:ADJ(?:USTMENTS?|S)?)\b", re.IGNORECASE), "balance": re.compile(r"\b(?:BALANCE|BAL)\b", re.IGNORECASE)}
    48	TOL = 8        # characters a figure may sit away from its column header (left or right aligned) before the column is called unclear
    49	
    50	
    51	def fmt(cents):
    52	    if cents is None:
    53	        return None
    54	    return ("-" if cents < 0 else "") + f"${abs(cents) // 100:,}.{abs(cents) % 100:02d}"
    55	
    56	
    57	def parse_figure(token: str) -> dict:
    58	    """'(70.00)' -> {cents: -7000}, '45.00-' -> -4500, '1,234.50' -> 123450. Credit notation (parentheses, trailing or leading minus) makes it
    59	    negative. Exactly two decimals are required: '95.5' or '9.999' keep their text and cents None, never rounded."""
    60	    neg = token.startswith("(") or token.startswith("-") or token.endswith("-") or token.endswith(")")
    61	    digits = re.sub(r"[()\-$]", "", token)
    62	    cents = A.to_cents(digits) if re.fullmatch(r"[\d,]+\.\d\d", digits) else None
    63	    return {"text": token, "cents": None if cents is None else (-cents if neg else cents), "usd": None if cents is None else fmt(-cents if neg else cents)}
    64	
    65	
    66	def _mag(f):
    67	    """Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept. The running
    68	    balance step check is what catches a column that was read the wrong way."""
    69	    return {**f, "cents": None if f["cents"] is None else abs(f["cents"]), "usd": None if f["cents"] is None else fmt(abs(f["cents"]))}
    70	
    71	
    72	def _norm(s):
    73	    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").casefold().replace("(synthetic)", "")).split())
    74	
    75	
    76	def _provider(rec: dict) -> str:
    77	    src = (rec.get("source") or "").strip()
    78	    name = re.split(r",|\s[-–—]\s", src, maxsplit=1)[0].strip()
    79	    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
    80	    return name or "Unknown provider"
    81	
    82	
    83	def _dos(raw):
    84	    p = dates.parse_date(raw or "")
    85	    return p["iso"] if p.get("status") == "parsed" else None
    86	
    87	
    88	def _cite(rec, line):
    89	    return {"record_no": rec["n"], "excerpt": line.strip()}
    90	
    91	
    92	# ------------------------------------------------------------------ record forms
    93	def form_of(rec: dict) -> str:
    94	    """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
    95	    body = (rec.get("excerpt") or rec.get("text") or "")
    96	    src = rec.get("source") or ""
    97	    up = body.upper()
    98	    if "EXPLANATION OF BENEFITS" in up or "THIS IS NOT A BILL" in up or re.search(r"\bEOB\b", src, re.IGNORECASE) or ("PLAN PAID" in up and "BILLED" in up):
    99	        return "eob"
   100	    if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
   101	        return "ub04"
   102	    if "TOTAL CHARGE" in up and "AMOUNT PAID" in up or "1500" in src or "HEALTH INSURANCE CLAIM FORM" in up:
   103	        return "cms1500"
   104	    if _header(body.split("\n"))[0] is not None:
   105	        return "ledger_table"
   106	    if "$" in body and (A._is_billing_source(src) or re.search(r"\bitemized\s+(?:ledger|statement)\b|\bledger\b", body, re.IGNORECASE)):
   107	        return "ledger_text"
   108	    return None
   109	
   110	
   111	def _header(lines):
   112	    """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
   113	    for i, ln in enumerate(lines):
   114	        if _ROW.match(ln) or re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or "$" in ln or not re.search(r"\S\s{2,}\S", ln):
   115	            continue          # a header is a spaced-out row of column names: a sentence with a '$' figure is prose
   116	        cols = {}
   117	        for kind, rx in _COLS.items():
   118	            m = rx.search(ln)
   119	            if m:
   120	                cols[kind] = (m.start(), m.end())
   121	        if "billed" in cols and "balance" in cols and len(cols) >= 3:
   122	            return i, cols
   123	    return None, None
   124	
   125	
   126	def _column(token_span, cols):
   127	    """The column whose header the figure sits under (left- or right-aligned), or None when two are equally near or none within TOL."""
   128	    s, e = token_span
   129	    d = sorted((min(abs(s - hs), abs(e - he)), kind) for kind, (hs, he) in cols.items())
   130	    if d[0][0] > TOL or (len(d) > 1 and d[1][0] == d[0][0]):
   131	        return None
   132	    return d[0][1]
   133	
   134	
   135	# ------------------------------------------------------------------ itemized ledger table
   136	def _ledger_table(rec, lines):
   137	    hi, cols = _header(lines)
   138	    out, stated, balfwd = [], {}, None
   139	    for ln in lines[hi + 1:]:
   140	        if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
   141	            stated.update(_stated(rec, ln))
   142	            continue
   143	        if _BALFWD.search(ln):
   144	            figs = [m for m in _NUM.finditer(ln)]
   145	            if figs:
   146	                balfwd = {**parse_figure(figs[-1].group(0)), "cite": _cite(rec, ln)}
   147	            continue
   148	        m = _ROW.match(ln)
   149	        if not m:
   150	            continue
   151	        figs = list(_NUM.finditer(ln))
   152	        head = ln[:figs[0].start()] if figs else ln
   153	        row_m = _ROW.match(head + " ")
   154	        parts = (row_m.group(3) if row_m else "").split(None, 1)
   155	        code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
   156	        desc = (parts[1] if code and len(parts) > 1 else " ".join(parts)).strip() if parts else ""
   157	        line = {"record_no": rec["n"], "form": "ledger", "dos": m.group(1), "dos_iso": _dos(m.group(1)), "posted": m.group(2), "code": code,
   158	                "description": desc, "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "excerpt": ln.strip()}
   159	        for fm in figs:
   160	            kind = _column(fm.span(), cols)
   161	            f = parse_figure(fm.group(0))
   162	            if kind is None or f["cents"] is None:
   163	                line["unclear"].append(f["text"])
   164	            elif line[kind] is not None:
   165	                line["unclear"].append(f["text"])            # two figures in one column: not guessed
   166	            else:
   167	                line[kind] = _mag(f) if kind in ("paid", "adjustment") else f
   168	        out.append(line)
   169	    stated.update({k: v for k, v in _stated(rec, "\n".join(lines[hi + 1:])).items() if k not in stated})
   170	    return out, stated, balfwd
   171	
   172	
   173	_STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIG})", re.IGNORECASE),
   174	           "paid": re.compile(rf"TOTAL\s+(?:PMTS?|PAYMENTS?)\s*[:=]?\s*({_FIG})", re.IGNORECASE),
   175	           "adjustment": re.compile(rf"TOTAL\s+ADJ\w*\s*[:=]?\s*({_FIG})", re.IGNORECASE),
   176	           "balance": re.compile(rf"(?:BALANCE\s+DUE|AMOUNT\s+DUE|TOTAL\s+BALANCE)\s*[:=]?\s*({_FIG})", re.IGNORECASE)}
   177	
   178	
   179	def _stated(rec, text):
   180	    """Totals the statement prints itself. Returned with the line they were read from; compared with the parsed lines, never used instead."""
   181	    out = {}
   182	    for kind, rx in _STATED.items():
   183	        m = rx.search(text)
   184	        if m:
   185	            f = parse_figure(m.group(1))
   186	            f = _mag(f) if kind in ("paid", "adjustment") else f
   187	            ln = next((x for x in text.split("\n") if m.group(0) in x), m.group(0))
   188	            out[kind] = {**f, "cite": _cite(rec, ln)}
   189	    return out
   190	
   191	
   192	# ------------------------------------------------------------------ ledger written as a sentence ("New patient exam charge $250.00; ...")
   193	_PROSE = (("billed_total", re.compile(r"\btotal\s+(?:billed\s+)?charges?\b|\btotal\s+billed\b", re.IGNORECASE)),
   194	          ("paid", re.compile(r"\bpayments?\b|\bpaid\b|\bpmts?\b", re.IGNORECASE)),
   195	          ("adjustment", re.compile(r"\badjust\w*|\bdiscount\b|\bwrite-?off\b|\bcontractual\b|\bcourtesy\b|\bW/O\b", re.IGNORECASE)),
   196	          ("balance", re.compile(r"\bbalance\b|\bamount\s+due\b", re.IGNORECASE)))
   197	
   198	
   199	def _segments(text):
   200	    """[(start, end)] of clauses: split at ; ! ? newline and a period that ends a sentence (not the decimal point of a figure)."""
   201	    out, pos = [], 0
   202	    for m in re.finditer(r"(?<=[;!?])\s+|\n|(?<=[a-zA-Z)\d])\.(?=\s+[A-Z])\s*", text):
   203	        out.append((pos, m.start() + (1 if text[m.start()] == "." else 0)))
   204	        pos = m.end()
   205	    out.append((pos, len(text)))
   206	    return [(s, e) for s, e in out if text[s:e].strip()]
   207	
   208	
   209	def _ledger_text(rec, body):
   210	    lines, stated = [], {}
   211	    for s, e in _segments(body):
   212	        seg = body[s:e]
   213	        for a in A.find_amounts(seg):
   214	            if a["cents"] is None:
   215	                continue
   216	            label = A._label(seg, a["start"])
   217	            neg = seg[max(0, a["start"] - 1):a["start"]] == "-" or label.endswith("-")
   218	            raw = ("-" if neg else "") + a["raw"]
   219	            fig = {"text": raw, "cents": -a["cents"] if neg else a["cents"], "usd": fmt(-a["cents"] if neg else a["cents"])}
   220	            kind = next((k for k, rx in _PROSE if rx.search(label)), None)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:31.193Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/billing.py | sed -n 220,420p",
 "description": "Read billing.py lines 220-420"
}
````

### User / tool · 2026-11-02T04:25:31.283Z

**tool result**
````
   220	            kind = next((k for k, rx in _PROSE if rx.search(label)), None)
   221	            cite = _cite(rec, seg)
   222	            if kind == "billed_total":
   223	                stated["billed"] = {**fig, "cite": cite}
   224	            elif kind in ("paid", "adjustment"):
   225	                lines.append(_pline(rec, seg, kind, _mag(fig), _NEGOTIATED.search(seg) is not None))
   226	            elif kind == "balance":
   227	                stated["balance"] = {**fig, "cite": cite}
   228	            elif A.classify(seg, a, source=rec.get("source")) == "charge":
   229	                lines.append(_pline(rec, seg, "billed", fig))
   230	    return lines, stated
   231	
   232	
   233	def _pline(rec, seg, kind, fig, negotiated=False):
   234	    line = {"record_no": rec["n"], "form": "ledger", "dos": None, "dos_iso": None, "posted": None, "code": None, "description": seg.strip(),
   235	            "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "excerpt": seg.strip()}
   236	    line[kind] = fig
   237	    return line
   238	
   239	
   240	# ------------------------------------------------------------------ CMS-1500 service lines (24F is implied-cents)
   241	_AMT = r"[0-9O]+(?:\s*\|\s*[0-9O]{2}|[ ][0-9O]{2}(?![\d.O]))?"
   242	_CMS = re.compile(rf"^\s*(?:24\.\s*)?([0-9O]{{6}})\s+([0-9O]{{6}})\s+(\d{{2}})\s+([A-Z0-9]{{5}})(?:\s+[A-Z0-9]{{1,4}})*?\s+({_AMT})\s+(\d+)(?:\s+(\S+))?\s*$")
   243	_CMS_TOTAL = re.compile(rf"\bTOTAL\s+CHARGE\s+({_AMT}|{_FIG})")
   244	_CMS_PAID = re.compile(rf"\bAMOUNT\s+PAID\s+({_AMT}|{_FIG})")
   245	
   246	
   247	def box_amount(raw: str) -> dict:
   248	    """A CMS-1500 money box has no decimal point: '85 | 00', '85 00' and '8500' are all $85.00. A printed decimal point is honoured.
   249	    OCR letters (O for 0) keep the text, cents None."""
   250	    raw = raw.strip()
   251	    if "O" in raw.upper().replace("|", ""):
   252	        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
   253	    if re.fullmatch(_FIG, raw):
   254	        return {**parse_figure(raw), "implied_decimal": False}
   255	    if "|" in raw:
   256	        d, c = [x.strip() for x in raw.split("|")]
   257	        cents = int(d) * 100 + int(c)
   258	    elif re.fullmatch(r"\d+ \d\d", raw):
   259	        d, c = raw.split(" ")
   260	        cents = int(d) * 100 + int(c)
   261	    elif re.fullmatch(r"\d{3,}", raw):
   262	        cents = int(raw)
   263	    else:
   264	        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
   265	    return {"text": raw, "cents": cents, "usd": fmt(cents), "implied_decimal": True}
   266	
   267	
   268	def _cms1500(rec, lines):
   269	    out, stated = [], {}
   270	    for ln in lines:
   271	        m = _CMS.match(ln)
   272	        if m:
   273	            fig = box_amount(m.group(5))
   274	            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
   275	                    "posted": None, "code": m.group(4), "description": f"units {m.group(6)}", "billed": None, "adjustment": None, "paid": None,
   276	                    "balance": None, "unclear": [], "excerpt": ln.strip(), "units": int(m.group(6))}
   277	            if fig["cents"] is None:
   278	                line["unclear"].append(fig["text"])
   279	            else:
   280	                line["billed"] = fig
   281	            out.append(line)
   282	        else:
   283	            for kind, rx in (("billed", _CMS_TOTAL), ("paid", _CMS_PAID)):
   284	                t = rx.search(ln)
   285	                if t:
   286	                    f = box_amount(t.group(1))
   287	                    if f["cents"] is not None:
   288	                        stated[kind] = {**f, "cite": _cite(rec, ln)}
   289	    return out, stated
   290	
   291	
   292	# ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)
   293	_UBROW = re.compile(r"^\s*(\d{4})\s+(\S.*?)(?:\s{2,}|$)")
   294	
   295	
   296	def _ub04(rec, lines):
   297	    hi = next((i for i, ln in enumerate(lines) if re.search(r"TOTAL\s+CHARGES", ln, re.IGNORECASE) and re.search(r"\bREV\b|SERV", ln)), None)
   298	    if hi is None:
   299	        return [], {}, []
   300	    h = lines[hi]
   301	    cols = {}
   302	    for kind, rx in (("rate", r"HCPCS/RATE|RATE"), ("billed", r"TOTAL\s+CHARGES"), ("noncovered", r"NON-COVERED")):
   303	        m = re.search(rx, h)
   304	        if m:
   305	            cols[kind] = (m.start(), m.end())
   306	    out, rates, stated = [], [], {}
   307	    for ln in lines[hi + 1:]:
   308	        m = _UBROW.match(ln)
   309	        if not m:
   310	            continue
   311	        figs = [(f, _column(f.span(), cols)) for f in _NUM.finditer(ln)]
   312	        if m.group(1) == "0001":
   313	            for f, k in figs:
   314	                if k == "billed":
   315	                    stated["billed"] = {**parse_figure(f.group(0)), "cite": _cite(rec, ln)}
   316	            continue
   317	        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
   318	                "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "excerpt": ln.strip(), "non_covered": None}
   319	        sd = re.search(r"\b(\d{6})\b", ln[:figs[0][0].start()] if figs else ln)
   320	        line["dos"] = sd.group(1) if sd else None
   321	        for f, k in figs:
   322	            p = parse_figure(f.group(0))
   323	            if p["cents"] is None or k is None:
   324	                line["unclear"].append(p["text"])
   325	            elif k == "rate":
   326	                rates.append({"record_no": rec["n"], "kind": "rate", "why": "UB-04 line 44 is a rate, not a charge.", "figure": p, "excerpt": ln.strip()})
   327	            elif k == "noncovered":
   328	                line["non_covered"] = p
   329	            elif line["billed"] is None:
   330	                line["billed"] = p
   331	            else:
   332	                line["unclear"].append(p["text"])
   333	        out.append(line)
   334	    return out, stated, rates
   335	
   336	
   337	# ------------------------------------------------------------------ EOB (payer figures; never added to charges)
   338	_EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
   339	            ("coinsurance", r"COINS\w*"), ("plan_paid", r"PLAN\s+PAID"), ("patient_owes", r"YOU\s+MAY\s+OWE|PATIENT\s+RESP\w*"))
   340	
   341	
   342	def _eob(rec, lines):
   343	    hi = next((i for i, ln in enumerate(lines) if re.search(r"\bBILLED\b", ln) and re.search(r"PLAN\s+PAID", ln, re.IGNORECASE)), None)
   344	    prov = next((re.sub(r"\s+", " ", m.group(1)).strip() for ln in lines for m in [re.match(r"\s*Provider\s*:\s*(.+?)\s*$", ln, re.IGNORECASE)] if m), None)
   345	    if hi is None:
   346	        return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": []}
   347	    order = sorted(((m.start(), k) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m))
   348	    names = [k for _, k in order]
   349	    out = []
   350	    for ln in lines[hi + 1:]:
   351	        m = re.match(rf"^\s*({_DATE})\s+(\S+)\s+", ln)
   352	        if not m:
   353	            continue
   354	        figs = [parse_figure(f.group(0)) for f in _NUM.finditer(ln)]
   355	        row = {"record_no": rec["n"], "dos": m.group(1), "dos_iso": _dos(m.group(1)), "service": m.group(2), "excerpt": ln.strip(), "unclear": [],
   356	               "codes": (ln[list(_NUM.finditer(ln))[-1].end():].strip() or None) if figs else None}
   357	        if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
   358	            row.update({k: _mag(f) for k, f in zip(names, figs)})
   359	        else:
   360	            row["unclear"] = [f["text"] for f in figs]
   361	        out.append(row)
   362	    return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": out}
   363	
   364	
   365	# ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
   366	_LOP_SOURCE = re.compile(r"letter\s+of\s+protection|\bLOP\b|\blien\b|reduction\s+letter|assignment", re.IGNORECASE)
   367	_LOP_LABEL = re.compile(r"\b(?:LOP|lien)\b[^,;]{0,25}\b(?:balance|amount)|\b(?:balance|amount)\b[^,;]{0,25}\b(?:LOP|lien)\b|\breduced\s+to\b|\baccept\w*\b[^.;]{0,50}\bsatisf\w+|"
   368	                        r"\b(?:atty|attorney)\s+reduction\b|\bcurrent\s+balance\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
   369	
   370	
   371	def _lop_lien(rec):
   372	    body = rec.get("excerpt") or rec.get("text") or ""
   373	    doc = bool(_LOP_SOURCE.search(rec.get("source") or ""))
   374	    out = []
   375	    for s, e in _segments(body):
   376	        seg = body[s:e]
   377	        for a in A.find_amounts(seg):
   378	            if a["cents"] is None:
   379	                continue
   380	            label = A._label(seg, a["start"])
   381	            if not (doc or _LOP_LABEL.search(label) or _LOP_LABEL.search(seg)):
   382	                continue
   383	            kind = "reduction" if re.search(r"reduc|satisf", seg, re.IGNORECASE) else ("lien_amount" if re.search(r"\blien\b", seg, re.IGNORECASE) else "asserted_balance")
   384	            out.append({"record_no": rec["n"], "provider": _provider(rec), "kind": kind, "label": " ".join(label.split()) or None,
   385	                        "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, "excerpt": seg.strip(), "in_totals": False})
   386	    return out
   387	
   388	
   389	# ------------------------------------------------------------------ assembling
   390	def _line_around(body, start, end):
   391	    """The whole printed line a figure sits on (a verbatim excerpt); a single-line paragraph gives the clause around it."""
   392	    a, b = body.rfind("\n", 0, start) + 1, body.find("\n", end)
   393	    line = body[a:(b if b >= 0 else len(body))]
   394	    if len(line) > 240:
   395	        for s, e in _segments(body):
   396	            if s <= start < e:
   397	                return body[s:e].strip()
   398	    return line.strip()
   399	
   400	
   401	def _cents(fig):
   402	    return fig["cents"] if fig and fig["cents"] is not None else None
   403	
   404	
   405	def _checks_for_line(line, prev_balance):
   406	    """LINE_UNCLEAR when a figure could not be read; BALANCE_STEP_MISMATCH when this line's balance is not the previous balance plus its
   407	    charge minus its payment and adjustment (only checked when every figure on the line was read)."""
   408	    codes = []
   409	    if line["unclear"]:
   410	        codes.append("LINE_UNCLEAR")
   411	    elif _cents(line.get("balance")) is not None and prev_balance is not None:
   412	        delta = (_cents(line["billed"]) or 0) - (_cents(line["paid"]) or 0) - (_cents(line["adjustment"]) or 0)
   413	        if line["balance"]["cents"] - prev_balance != delta:
   414	            codes.append("BALANCE_STEP_MISMATCH")
   415	    return codes
   416	
   417	
   418	def _line_key(l):
   419	    g = lambda k: (l[k] or {}).get("cents") if l.get(k) else None
   420	    return (_norm(l.get("dos")), _norm(l.get("posted")), _norm(l.get("code")), _norm(l.get("description")), g("billed"), g("paid"), g("adjustment"), l.get("form"))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:32.367Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/billing.py | sed -n 420,650p",
 "description": "Read billing.py lines 420-650"
}
````

### User / tool · 2026-11-02T04:25:32.471Z

**tool result**
````
   420	    return (_norm(l.get("dos")), _norm(l.get("posted")), _norm(l.get("code")), _norm(l.get("description")), g("billed"), g("paid"), g("adjustment"), l.get("form"))
   421	
   422	
   423	def _merge_duplicates(lines):
   424	    """A line repeated in a later record (a re-sent statement, an attached copy) counts once and cites both. Repeats inside ONE record are real."""
   425	    out, seen = [], {}
   426	    for l in lines:
   427	        key = _line_key(l)
   428	        hit = next((o for o in seen.get(key, []) if l["record_no"] not in o["record_nos"] and l["record_no"] not in o["_taken"]), None)
   429	        if hit and key[4:7] != (None, None, None):
   430	            hit["record_nos"].append(l["record_no"])
   431	            hit["cites"].append({"record_no": l["record_no"], "excerpt": l["excerpt"]})
   432	            hit["_taken"].add(l["record_no"])
   433	            continue
   434	        l = {**l, "record_nos": [l["record_no"]], "cites": [{"record_no": l["record_no"], "excerpt": l["excerpt"]}], "_taken": set()}
   435	        seen.setdefault(key, []).append(l)
   436	        out.append(l)
   437	    for l in out:
   438	        l.pop("_taken")
   439	    return out
   440	
   441	
   442	def _sum(lines, kind):
   443	    vals = [l[kind]["cents"] for l in lines if l.get(kind) and l[kind]["cents"] is not None]
   444	    return sum(vals) if vals else None
   445	
   446	
   447	def _tot(cents):
   448	    return {"cents": cents, "usd": fmt(cents)}
   449	
   450	
   451	def analyze(records: list) -> dict:
   452	    """The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O."""
   453	    recs = [r for r in records if not r.get("duplicate_of")]
   454	    lines, stated_by_rec, eobs, lop, excluded, balfwds, rec_form, checks = [], {}, [], [], [], {}, {}, []
   455	    skipped = []
   456	    for r in recs:
   457	        body = r.get("excerpt") or r.get("text") or ""
   458	        ls = body.split("\n")
   459	        form = form_of(r)
   460	        if r.get("injection_tag") and (form or _lop_lien(r)):      # a figure inside instruction-like text has no trusted value (D-005)
   461	            skipped.append({"record_no": r["n"], "reason_code": "INJECTION_SUSPECTED"})
   462	            continue
   463	        before = len(lines)
   464	        rec_form[r["n"]] = form
   465	        if form == "ledger_table":
   466	            got, st, bf = _ledger_table(r, ls)
   467	            lines += got
   468	            stated_by_rec[r["n"]], balfwds[r["n"]] = st, bf
   469	        elif form == "ledger_text":
   470	            got, st = _ledger_text(r, body)
   471	            lines += got
   472	            stated_by_rec[r["n"]] = st
   473	        elif form == "cms1500":
   474	            got, st = _cms1500(r, ls)
   475	            lines += got
   476	            stated_by_rec[r["n"]] = st
   477	        elif form == "ub04":
   478	            got, st, rates = _ub04(r, ls)
   479	            lines += got
   480	            excluded += rates
   481	            stated_by_rec[r["n"]] = st
   482	        elif form == "eob":
   483	            eobs.append(_eob(r, ls))
   484	        text = (r.get("text") or "") + "\n" + body
   485	        for l in lines[before:]:                       # fail closed: a line that is not a verbatim excerpt of its record shows no figures
   486	            if l["excerpt"] not in text:
   487	                l.update(billed=None, adjustment=None, paid=None, balance=None, unclear=["(not verbatim)"])
   488	        if form in ("ledger_table", "ledger_text"):     # a statement's fee-schedule line is a rate and carries no date of service
   489	            for a in A.find_amounts(body):
   490	                if a["cents"] is not None and A.classify(body, a, source=r.get("source")) == "rate":
   491	                    excluded.append({"record_no": r["n"], "kind": "rate", "why": "A rate (per visit, per unit) is a price, not a charge.",
   492	                                     "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, "excerpt": _line_around(body, a["start"], a["end"])})
   493	        lop += _lop_lien(r)
   494	    for ln in lines:
   495	        ln["provider"] = _provider(next(r for r in recs if r["n"] == ln["record_no"]))
   496	    for ex in excluded:
   497	        ex["provider"] = _provider(next(r for r in recs if r["n"] == ex["record_no"]))
   498	    lines = _merge_duplicates(lines)
   499	    # per-line checks (running-balance steps follow the order printed within each record)
   500	    prev = {}
   501	    for l in lines:
   502	        n = l["record_no"]
   503	        bf = balfwds.get(n)
   504	        if n not in prev:
   505	            prev[n] = bf["cents"] if bf else None
   506	        l["checks"] = _checks_for_line(l, prev[n])
   507	        prev[n] = l["balance"]["cents"] if l.get("balance") and l["balance"]["cents"] is not None else prev[n]
   508	    for i, l in enumerate(lines, 1):
   509	        l["id"] = f"b{i}"
   510	        l["kind"] = ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
   511	                     "charge" if l["billed"] else
   512	                     "payment" if l["paid"] else
   513	                     "adjustment" if l["adjustment"] else
   514	                     "balance_only" if l["balance"] else "unclear")
   515	        l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
   516	        if l["form"] == "ledger" and l["billed"] and not l["dos"] and rec_form.get(l["record_no"]) == "ledger_text":
   517	            l["checks"].append("NO_DATE_OF_SERVICE")
   518	    # providers
   519	    by_prov = {}
   520	    for l in lines:
   521	        by_prov.setdefault(_norm(l["provider"]), {"provider": l["provider"], "lines": []})["lines"].append(l)
   522	    providers = []
   523	    for key, p in by_prov.items():
   524	        ls = p["lines"]
   525	        ledger = [l for l in ls if l["form"] == "ledger"]
   526	        claim = [l for l in ls if l["form"] != "ledger"]
   527	        basis = ledger or claim
   528	        pchecks = []
   529	        nego = [l for l in basis if l["negotiated"]]
   530	        adj_lines = [l for l in basis if not l["negotiated"]]
   531	        rec_nos = sorted({n for l in ls for n in l["record_nos"]})
   532	        stated = {}
   533	        for n in rec_nos:
   534	            for k, v in (stated_by_rec.get(n) or {}).items():
   535	                stated.setdefault(k, []).append(v)
   536	        # one stated figure per kind is compared; with several statements the latest-in-file one is shown and all are listed
   537	        comp = {}
   538	        for kind in ("billed", "paid", "adjustment", "balance"):
   539	            comp[kind] = stated.get(kind, [None])[-1] if stated.get(kind) else None
   540	        billed, paid, adj = _sum(basis, "billed"), _sum(basis, "paid"), _sum(adj_lines, "adjustment")
   541	        unclear = [l for l in basis if l["unclear"]]
   542	        if comp["billed"] and billed is not None and comp["billed"]["cents"] is not None and comp["billed"]["cents"] != billed:
   543	            pchecks.append({"code": "LEDGER_TOTAL_MISMATCH" if basis is ledger else "CLAIM_TOTAL_MISMATCH", "field": "billed", "stated": comp["billed"], "computed": _tot(billed)})
   544	        if comp["paid"] and paid is not None and basis is ledger and comp["paid"]["cents"] is not None and comp["paid"]["cents"] != paid:
   545	            pchecks.append({"code": "LEDGER_TOTAL_MISMATCH", "field": "paid", "stated": comp["paid"], "computed": _tot(paid)})
   546	        if comp["adjustment"] and basis is ledger and comp["adjustment"]["cents"] is not None and comp["adjustment"]["cents"] != (adj or 0) + (_sum(nego, "adjustment") or 0):
   547	            pchecks.append({"code": "LEDGER_TOTAL_MISMATCH", "field": "adjustment", "stated": comp["adjustment"], "computed": _tot((adj or 0) + (_sum(nego, "adjustment") or 0))})
   548	        if comp["balance"] and comp["balance"]["cents"] is not None and billed is not None and basis is ledger and not unclear:
   549	            derived = billed - (paid or 0) - ((adj or 0) + (_sum(nego, "adjustment") or 0))
   550	            if derived != comp["balance"]["cents"]:
   551	                pchecks.append({"code": "LEDGER_BALANCE_MISMATCH", "field": "balance", "stated": comp["balance"], "computed": _tot(derived)})
   552	        if ledger and claim:
   553	            cb = _sum(claim, "billed")
   554	            if cb is not None and billed is not None and cb != billed:
   555	                pchecks.append({"code": "CLAIM_LEDGER_BILLED_MISMATCH", "field": "billed", "stated": _tot(cb), "computed": _tot(billed)})
   556	        for c in pchecks:
   557	            c["message"] = CHECKS[c["code"]]
   558	        providers.append({
   559	            "provider": p["provider"], "record_nos": rec_nos,
   560	            "basis": "itemized_ledger" if ledger else "claim_form",
   561	            "billed": _tot(billed), "adjustment": _tot(adj), "paid": _tot(paid),
   562	            "negotiated_reductions": _tot(_sum(nego, "adjustment")),
   563	            "balance": comp["balance"], "stated_totals": {k: v for k, v in comp.items() if v},
   564	            "complete": not unclear, "unclear_lines": len(unclear),
   565	            "line_count": len(basis), "claim_lines_not_totaled": len(claim) if ledger else 0,
   566	            "checks": pchecks, "lines": ls})
   567	    # EOB cross-checks against the matching provider's ledger lines
   568	    payer = []
   569	    for e in eobs:
   570	        ledger_p = next((p for p in providers if p["basis"] == "itemized_ledger" and (_norm(p["provider"]) in _norm(e["provider"]) or _norm(e["provider"]) in _norm(p["provider"]))), None)
   571	        e["matched_provider"] = ledger_p["provider"] if ledger_p else None
   572	        e["not_added_note"] = "The EOB restates the provider's charge; its amounts are never added to the charges."
   573	        e["checks"] = []
   574	        if ledger_p:
   575	            for el in e["lines"]:
   576	                led = [l for l in ledger_p["lines"] if l["form"] == "ledger" and _norm(l["code"]) == _norm(el["service"]) and
   577	                       ((l["dos_iso"] and l["dos_iso"] == el["dos_iso"]) or _norm(l["dos"]) == _norm(el["dos"]))]
   578	                if not led or not el.get("billed"):
   579	                    continue
   580	                lb, lp = _sum(led, "billed"), _sum(led, "paid") or 0
   581	                cites = [{"record_no": el["record_no"], "excerpt": el["excerpt"]}] + [c for l in led for c in l["cites"]]
   582	                if lb is not None and lb != el["billed"]["cents"]:
   583	                    e["checks"].append({"code": "LEDGER_EOB_BILLED_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lb), "eob": el["billed"], "cites": cites})
   584	                if el.get("plan_paid") and lp != el["plan_paid"]["cents"]:
   585	                    e["checks"].append({"code": "LEDGER_EOB_PAID_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lp), "eob": el["plan_paid"], "cites": cites})
   586	        for c in e["checks"]:
   587	            c["message"] = CHECKS[c["code"]]
   588	        payer.append(e)
   589	    for i, x in enumerate(lop, 1):
   590	        x["id"] = f"l{i}"
   591	    for i, x in enumerate(excluded, 1):
   592	        x["id"] = f"x{i}"
   593	    allc = [c for p in providers for c in p["checks"]] + [c for e in payer for c in e["checks"]]
   594	    line_flags = [{"code": c, "line_id": l["id"], "provider": l["provider"], "message": CHECKS[c], "excerpt": l["excerpt"]} for p in providers for l in p["lines"] for c in l["checks"]]
   595	    for p in providers:
   596	        for l in p["lines"]:
   597	            l.pop("provider", None)
   598	    found = bool(providers or payer or lop)
   599	    return {
   600	        "status": "none_found" if not found else ("partial_unclear" if any(not p["complete"] for p in providers) else "analyzed"),
   601	        "providers": providers, "payer_reports": payer, "lop_lien": lop, "excluded": excluded, "skipped_records": skipped,
   602	        "checks": allc, "line_flags": line_flags,
   603	        "totals": {"billed": _tot(sum(p["billed"]["cents"] or 0 for p in providers)) if providers else _tot(None),
   604	                   "adjustment": _tot(sum(p["adjustment"]["cents"] or 0 for p in providers)) if providers else _tot(None),
   605	                   "paid": _tot(sum(p["paid"]["cents"] or 0 for p in providers)) if providers else _tot(None),
   606	                   "provider_count": len(providers), "not_for_letter": True},
   607	        "rules": RULES}
   608	
   609	
   610	def verify_citations(analysis: dict, records: list) -> list:
   611	    """[] when every line's excerpt is a verbatim substring of a cited record and every figure text appears in its excerpt; else the failures.
   612	    Run in tests and by the API before a response leaves: a line that fails is dropped from the response, never shown uncited."""
   613	    text_of = {r["n"]: (r.get("text") or "") + "\n" + (r.get("excerpt") or "") for r in records}
   614	    bad = []
   615	    for p in analysis["providers"]:
   616	        for l in p["lines"]:
   617	            for c in l["cites"]:
   618	                if c["excerpt"] not in text_of.get(c["record_no"], ""):
   619	                    bad.append({"line": l["id"], "reason": "excerpt_not_verbatim"})
   620	            for k in ("billed", "adjustment", "paid", "balance"):
   621	                if l.get(k) and l[k]["text"].lstrip("-") not in l["excerpt"] and l[k]["text"] not in l["excerpt"]:
   622	                    bad.append({"line": l["id"], "reason": f"{k}_not_in_excerpt"})
   623	    for x in analysis["lop_lien"] + analysis["excluded"]:
   624	        if x["excerpt"] not in text_of.get(x["record_no"], "") or x["figure"]["text"] not in x["excerpt"]:
   625	            bad.append({"line": x["id"], "reason": "excerpt_not_verbatim"})
   626	    return bad
   627	
   628	
   629	def for_case(conn, case_id: str) -> dict:
   630	    from app.backend import store      # imported here so unit tests of the pure functions need no database
   631	    return analyze(store.load_records(conn, case_id))
   632	
   633	
   634	def add_routes(app, *, conn, get_case):
   635	    @app.get("/api/cases/{token}/billing")
   636	    def billing_get(token: str):
   637	        c = conn()
   638	        try:
   639	            get_case(c, token)
   640	            return {"billing": for_case(c, token)}
   641	        finally:
   642	            c.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:33.917Z

**tool call — Bash**
````
{
 "command": "cat -n tests/unit/test_billing.py | sed -n 1,170p",
 "description": "Read test_billing.py lines 1-170"
}
````

### User / tool · 2026-11-02T04:25:34.005Z

**tool result**
````
     1	"""Billing analysis (T-083, D-042): code-only, every figure cited, nothing totaled that is not stated. SYNTHETIC ledgers from research/record-formats.md."""
     2	import time
     3	
     4	import pytest
     5	from fastapi.testclient import TestClient
     6	
     7	from app.backend import billing as B
     8	from app.backend import pipeline as PL
     9	from app.backend.api import create_app
    10	from app.db import db as DB
    11	
    12	LEDGER = """SYNTHETIC RECORD
    13	Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
    14	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
    15	DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
    16	05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
    17	06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
    18	06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
    19	06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
    20	06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
    21	06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
    22	07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
    23	                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
    24	Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection."""
    25	
    26	EOB = """SYNTHETIC RECORD - THIS IS NOT A BILL
    27	Quoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
    28	Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
    29	Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
    30	DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
    31	06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
    32	06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
    33	06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
    34	TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
    35	CO-97: payment included in allowance for another service."""
    36	
    37	CMS_CLEAN = """SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
    38	24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    39	    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
    40	    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    41	    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
    42	    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
    43	    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
    44	25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
    45	33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"""
    46	
    47	CMS_OCR = """SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
    48	24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001
    49	    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001
    50	    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001
    51	    060126 060326 11 97014 A 9000 3 SYN-NPI-0001
    52	    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001
    53	28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00"""
    54	
    55	UB_ROOM = """SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
    56	1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
    57	42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
    58	0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
    59	0450    EMERGENCY ROOM                               091526        1          1,975.00
    60	0250    PHARMACY                                     091526       14            412.75
    61	0300    LABORATORY                                   091526        6            688.00
    62	0320    DX X-RAY                                     091526        2            540.00
    63	0001    TOTAL                                        092226                   9,165.75
    64	67 S42.201A   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)"""
    65	
    66	PROSE = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
    67	         "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")
    68	
    69	LOP = ("Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction "
    70	       "of the account. Please send an itemized statement.")
    71	
    72	
    73	def rec(n, source, text, **kw):
    74	    return {"n": n, "source": source, "excerpt": text, "text": text, **kw}
    75	
    76	
    77	def one(records):
    78	    out = B.analyze(records)
    79	    assert B.verify_citations(out, records) == []
    80	    return out
    81	
    82	
    83	def provider(out, name):
    84	    return next(p for p in out["providers"] if p["provider"].startswith(name))
    85	
    86	
    87	# ------------------------------------------------------------------ itemized ledger
    88	def test_ledger_lines_parse_to_four_figures_each_cited():
    89	    r = [rec(1, "Larkspur Hollow Physical Therapy (SYNTHETIC), itemized statement", LEDGER)]
    90	    p = provider(one(r), "Larkspur")
    91	    ls = p["lines"]
    92	    assert [l["code"] for l in ls] == ["97162", "97110", "97140", "97014", "97140", "97140", "ADJ"]
    93	    first = ls[0]
    94	    assert (first["billed"]["cents"], first["balance"]["cents"], first["paid"], first["adjustment"]) == (21000, 21000, None, None)
    95	    assert first["dos"] == "05/27/26" and first["dos_iso"] == "2026-05-27" and first["posted"] == "05/28/26"
    96	    assert first["cites"] == [{"record_no": 1, "excerpt": first["excerpt"]}] and first["excerpt"] in LEDGER
    97	    adj = ls[-1]
    98	    assert adj["adjustment"]["cents"] == 4500 and adj["adjustment"]["text"] == "45.00-" and adj["balance"]["cents"] == 40000 and adj["kind"] == "adjustment"
    99	
   100	
   101	def test_void_nets_and_running_balance_is_never_summed():
   102	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]), "Larkspur")
   103	    void = next(l for l in p["lines"] if "VOID" in l["description"])
   104	    assert void["billed"]["cents"] == -7000 and void["kind"] == "reversal"
   105	    assert p["billed"]["cents"] == 44500           # 210+130+70+35-70+70, not the sum of the running balances
   106	    assert p["adjustment"]["cents"] == 4500 and p["paid"]["cents"] is None
   107	    assert p["balance"]["cents"] == 40000          # the statement's own BALANCE DUE
   108	    assert p["checks"] == [] and p["complete"] and not any(f["code"] == "BALANCE_STEP_MISMATCH" for f in one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])["line_flags"])
   109	
   110	
   111	def test_fee_schedule_rate_is_listed_and_never_a_charge():
   112	    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
   113	    assert [(x["figure"]["cents"], x["kind"]) for x in out["excluded"]] == [(6500, "rate")]
   114	    assert "Fee schedule" in out["excluded"][0]["excerpt"]
   115	    assert 6500 not in [l["billed"]["cents"] for l in provider(out, "Larkspur")["lines"] if l["billed"]]
   116	
   117	
   118	def test_stated_total_mismatch_is_flagged_not_corrected():
   119	    bad = LEDGER.replace("TOTAL CHARGES 445.00", "TOTAL CHARGES 455.00")
   120	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)]), "Larkspur")
   121	    assert p["billed"]["cents"] == 44500           # the lines, not the printed total
   122	    c = p["checks"][0]
   123	    assert c["code"] == "LEDGER_TOTAL_MISMATCH" and c["stated"]["cents"] == 45500 and c["computed"]["cents"] == 44500
   124	
   125	
   126	def test_running_balance_step_mismatch_is_flagged_on_the_line():
   127	    bad = LEDGER.replace("410.00\n", "415.00\n", 1)
   128	    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
   129	    assert [f["code"] for f in out["line_flags"] if f["code"] == "BALANCE_STEP_MISMATCH"] != []
   130	
   131	
   132	def test_unreadable_figure_is_listed_with_no_value_and_left_out_of_totals():
   133	    txt = LEDGER.replace("130.00    ", "13O.00    ", 1).replace("TOTAL CHARGES 445.00  ", "")
   134	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur")
   135	    bad = next(l for l in p["lines"] if l["code"] == "97110")
   136	    assert bad["billed"] is None and bad["unclear"] and "LINE_UNCLEAR" in bad["checks"]
   137	    assert p["billed"]["cents"] == 31500 and p["complete"] is False and p["unclear_lines"] == 1
   138	
   139	
   140	def test_extra_decimals_are_never_rounded():
   141	    txt = LEDGER.replace("130.00", "130.005")
   142	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur")
   143	    assert next(l for l in p["lines"] if l["code"] == "97110")["billed"] is None
   144	
   145	
   146	def test_duplicate_statement_counts_once_and_cites_both_records():
   147	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Larkspur Hollow Physical Therapy, statement (copy)", LEDGER)]
   148	    p = provider(one(r), "Larkspur")
   149	    assert p["billed"]["cents"] == 44500
   150	    assert all(l["record_nos"] == [1, 2] for l in p["lines"]) and p["lines"][0]["cites"][1]["record_no"] == 2
   151	
   152	
   153	def test_two_identical_lines_inside_one_record_both_count():
   154	    twice = LEDGER.replace("06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00",
   155	                           "06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00\n"
   156	                           "06/10/26  06/11/26  97014  E-stim unattended              35.00                         480.00")
   157	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", twice)]), "Larkspur")
   158	    assert sum(1 for l in p["lines"] if l["code"] == "97014") == 2
   159	
   160	
   161	def test_balance_forward_is_not_a_charge():
   162	    txt = LEDGER.replace("05/27/26  05/28/26  97162", "Bal fwd                                                                          100.00\n05/27/26  05/28/26  97162", 1) \
   163	                .replace("PT eval moderate complexity   210.00                         210.00", "PT eval moderate complexity   210.00                         310.00")
   164	    p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur")
   165	    assert p["billed"]["cents"] == 44500 and all("Bal" not in (l["description"] or "") for l in p["lines"])
   166	
   167	
   168	def test_payments_adjustments_in_their_own_columns_by_position():
   169	    txt = """DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
   170	03/01/26  03/02/26  99213  Office visit                  150.00                         150.00
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:35.253Z

**tool call — Bash**
````
{
 "command": "cat -n tests/unit/test_billing.py | sed -n 170,340p",
 "description": "Read test_billing.py lines 170-340"
}
````

### User / tool · 2026-11-02T04:25:35.337Z

**tool result**
````
   170	03/01/26  03/02/26  99213  Office visit                  150.00                         150.00
   171	03/15/26  03/15/26  PMT    Ins pmt - Ck #SYN-1043                    100.00             50.00
   172	03/15/26  03/15/26  CO45   Contractual adj                                   20.00-      30.00
   173	04/20/26  04/20/26  ATY    Atty reduction                                    10.00-      20.00
   174	                     TOTAL CHARGES 150.00  TOTAL PMTS 100.00  TOTAL ADJ (30.00)  BALANCE DUE 20.00"""
   175	    p = provider(one([rec(1, "Medlark Clinic, statement", txt)]), "Medlark")
   176	    assert (p["billed"]["cents"], p["paid"]["cents"], p["adjustment"]["cents"], p["negotiated_reductions"]["cents"]) == (15000, 10000, 2000, 1000)
   177	    assert p["checks"] == []                       # stated adjustments 30.00 = contractual 20.00 + attorney reduction 10.00; balance 150-100-30 = 20
   178	
   179	
   180	def test_ledger_prose_statement_parses_and_checks_its_own_total():
   181	    out = one([rec(9, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
   182	    p = provider(out, "Fennimoor")
   183	    assert [l["billed"]["cents"] for l in p["lines"] if l["billed"]] == [25000, 18000, 231000]
   184	    assert p["billed"]["cents"] == 274000 and p["paid"]["cents"] == 30000 and p["adjustment"]["cents"] == 27400
   185	    assert p["balance"]["cents"] == 216600 and p["checks"] == []
   186	    assert out["lop_lien"] == []                   # "held under letter of protection" has no amount
   187	
   188	
   189	# ------------------------------------------------------------------ totals by provider
   190	def test_totals_are_per_provider_and_only_of_stated_figures():
   191	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)]
   192	    out = one(r)
   193	    assert sorted((p["provider"], p["billed"]["cents"]) for p in out["providers"]) == [("Fennimoor Spine Clinic", 274000), ("Larkspur Hollow Physical Therapy", 44500)]
   194	    assert out["totals"]["billed"]["cents"] == 318500 and out["totals"]["not_for_letter"] is True
   195	
   196	
   197	def test_nothing_found_for_a_clinical_record():
   198	    out = one([rec(1, "Dr. Lee, progress note", "Neck pain 5/10 after the collision. Plan: continue therapy.")])
   199	    assert out["status"] == "none_found" and out["providers"] == [] and out["totals"]["billed"]["cents"] is None
   200	
   201	
   202	# ------------------------------------------------------------------ LOP / lien amounts are separate
   203	def test_lop_and_lien_amounts_are_listed_separately_and_never_totaled():
   204	    r = [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE), rec(2, "Pellingham and Rook PLLC, correspondence (letter of protection)", LOP)]
   205	    out = one(r)
   206	    assert [(x["figure"]["cents"], x["kind"]) for x in out["lop_lien"]] == [(486000, "asserted_balance"), (310000, "reduction")]
   207	    assert all(x["in_totals"] is False for x in out["lop_lien"])
   208	    assert provider(out, "Fennimoor")["billed"]["cents"] == 274000
   209	
   210	
   211	def test_atty_reduction_on_a_ledger_is_not_a_plain_adjustment():
   212	    txt = "Itemized ledger. Therapy charge $1,000.00. Balance reduced to $600.00 in full satisfaction. Balance due $1,000.00."
   213	    out = one([rec(1, "Medlark Clinic, itemized ledger", txt)])
   214	    assert [x["figure"]["cents"] for x in out["lop_lien"]] == [60000]
   215	    assert provider(out, "Medlark")["billed"]["cents"] == 100000
   216	
   217	
   218	# ------------------------------------------------------------------ CMS-1500 (implied decimals), UB-04 (rate on the charge line), EOB
   219	def test_cms1500_boxes_are_implied_cents_and_checked_against_item_28():
   220	    p = provider(one([rec(1, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)]), "Brightwater")
   221	    assert [l["billed"]["cents"] for l in p["lines"]] == [8500, 8500, 8500, 9000, 4500]
   222	    assert p["billed"]["cents"] == 39000 and p["stated_totals"]["billed"]["cents"] == 39000 and p["checks"] == []
   223	    assert p["stated_totals"]["paid"]["cents"] == 0 and p["basis"] == "claim_form"
   224	
   225	
   226	def test_cms1500_ocr_text_never_reads_8500_as_dollars():
   227	    p = provider(one([rec(1, "Brightwater Spine & Wellness, CMS-1500 (OCR)", CMS_OCR)]), "Brightwater")
   228	    cents = [l["billed"]["cents"] if l["billed"] else None for l in p["lines"]]
   229	    assert cents[:2] == [8500, 8500] and cents[3] == 9000          # 8500 -> $85.00, 9000 -> $90.00
   230	    assert cents[4] is None and "45 OO" in p["lines"][4]["unclear"]    # OCR letters: listed, not totaled
   231	    assert p["lines"][2]["billed"]["cents"] == 8500                # O in the date does not matter
   232	    assert p["billed"]["cents"] == 8500 * 3 + 9000 - 0 and p["complete"] is False
   233	    assert p["checks"][0]["code"] == "CLAIM_TOTAL_MISMATCH"        # 39000 stated vs the lines that could be read
   234	
   235	
   236	def test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added():
   237	    out = one([rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)])
   238	    p = provider(out, "Saltmarrow")
   239	    assert p["billed"]["cents"] == 916575          # 5550.00 + 1975.00 + 412.75 + 688.00 + 540.00, not 20,181.50
   240	    assert p["stated_totals"]["billed"]["cents"] == 916575 and p["checks"] == []
   241	    assert [(x["figure"]["cents"], x["kind"]) for x in out["excluded"]] == [(185000, "rate")]
   242	    assert all(l["code"] != "0001" for l in p["lines"])
   243	    assert next(l for l in p["lines"] if l["code"] == "0120")["billed"]["cents"] == 555000
   244	
   245	
   246	def test_eob_is_never_added_and_a_ledger_eob_paid_mismatch_is_raised():
   247	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)]
   248	    out = one(r)
   249	    assert provider(out, "Larkspur")["billed"]["cents"] == 44500          # EOB's 235.00 billed is not added
   250	    assert len(out["providers"]) == 1
   251	    e = out["payer_reports"][0]
   252	    assert e["matched_provider"].startswith("Larkspur") and len(e["lines"]) == 3
   253	    l140 = next(x for x in e["lines"] if x["service"] == "97140")
   254	    assert l140["plan_paid"]["cents"] == 1600 and l140["codes"] == "PR-1, PR-2, CO-45"
   255	    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
   256	    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
   257	    assert len(e["checks"][0]["cites"]) >= 3 and e["checks"][0]["cites"][0]["record_no"] == 2
   258	
   259	
   260	def test_claim_form_and_ledger_for_the_same_provider_are_not_double_counted():
   261	    claim = CMS_CLEAN
   262	    r = [rec(1, "Brightwater Spine & Wellness, itemized ledger", "Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00."),
   263	         rec(2, "Brightwater Spine & Wellness, CMS-1500", claim)]
   264	    p = provider(one(r), "Brightwater")
   265	    assert p["basis"] == "itemized_ledger" and p["billed"]["cents"] == 39000 and p["claim_lines_not_totaled"] == 5 and p["checks"] == []
   266	
   267	
   268	# ------------------------------------------------------------------ citations, API
   269	def test_verify_citations_catches_an_uncited_line():
   270	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
   271	    out = B.analyze(r)
   272	    out["providers"][0]["lines"][0]["cites"][0]["excerpt"] = "not in the record"
   273	    assert B.verify_citations(out, r)[0]["reason"] == "excerpt_not_verbatim"
   274	
   275	
   276	@pytest.fixture
   277	def client(tmp_path, monkeypatch):
   278	    monkeypatch.setenv("LLM_BACKEND", "fixture")
   279	    monkeypatch.setenv("ZLAYT_MODE", "local")
   280	    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
   281	    monkeypatch.delenv("ENABLE_LIVE", raising=False)
   282	    return TestClient(create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 5000))
   283	
   284	
   285	def test_billing_route_for_a_pasted_case(client):
   286	    text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
   287	            "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
   288	    conn = DB.connect(client.app.state.db_path)             # demo mode refuses unrecorded text over HTTP, so the case is seeded directly (code-only ingest)
   289	    tok = DB.create_case(conn, text, now=time.time())
   290	    PL.ingest_case(conn, tok, text, time.time())
   291	    conn.close()
   292	    r = client.get(f"/api/cases/{tok}/billing")
   293	    assert r.status_code == 200
   294	    b = r.json()["billing"]
   295	    assert b["providers"][0]["billed"]["cents"] == 274000
   296	    assert [x["figure"]["cents"] for x in b["lop_lien"]] == [486000, 310000]
   297	    assert client.get("/api/cases/nope/billing").status_code == 404
   298	
   299	
   300	def test_table_survives_ingest_with_the_quote_on_its_own_line_or_the_first_line(client):
   301	    from app.backend import store
   302	    body = LEDGER.split("\n", 3)[3]
   303	    for quoted in ('Excerpt: "' + body + '"', 'Excerpt: "\n' + body + '\n"'):
   304	        text = "=== Record 1 ===\nDate: 2026-07-31\nSource: Larkspur Hollow Physical Therapy, itemized statement\n" + quoted + "\n"
   305	        conn = DB.connect(client.app.state.db_path)
   306	        tok = DB.create_case(conn, text, now=time.time())
   307	        PL.ingest_case(conn, tok, text, time.time())
   308	        out = B.for_case(conn, tok)
   309	        assert B.verify_citations(out, store.load_records(conn, tok)) == []
   310	        conn.close()
   311	        p = out["providers"][0]
   312	        assert p["billed"]["cents"] == 44500 and p["adjustment"]["cents"] == 4500 and p["checks"] == [] and len(p["lines"]) == 7
   313	
   314	
   315	def test_prose_charges_without_a_date_of_service_are_counted_as_stated_and_flagged():
   316	    out = one([rec(9, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
   317	    assert {f["code"] for f in out["line_flags"]} == {"NO_DATE_OF_SERVICE"}
   318	
   319	
   320	def test_injection_tagged_record_is_skipped_not_totaled():
   321	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)]
   322	    out = one(r)
   323	    assert out["providers"] == [] and out["skipped_records"] == [{"record_no": 1, "reason_code": "INJECTION_SUSPECTED"}]
   324	
   325	
   326	def test_duplicate_records_are_ignored_and_no_model_is_imported():
   327	    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, duplicate_of=1)]
   328	    assert provider(one(r), "Larkspur")["lines"][0]["record_nos"] == [1]
   329	    import app.backend.billing as mod, inspect
   330	    assert "app.llm" not in inspect.getsource(mod) and "call(" not in inspect.getsource(mod)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:37.196Z

**tool call — Bash**
````
{
 "command": "ls -la .venv/bin/python && .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -30; echo \"EXIT=$?\"",
 "description": "Run billing unit tests"
}
````

### User / tool · 2026-11-02T04:25:38.084Z

**tool result**
````
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
...........................                                              [100%]
27 passed in 0.46s
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:40.308Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -20 && git diff --stat f218263 HEAD -- app/backend/billing.py tests/unit/test_billing.py app/backend/api.py | tail -3; echo ---; git show f218263 -- app/backend/api.py; echo ---; grep -n \"billing\" memory/contracts/api.md | head; echo ---; grep -n \"def find_amounts\\|def classify\\|def _label\\|def to_cents\\|def _is_billing_source\" -A3 app/backend/amounts.py",
 "description": "Check git state, api.py hook, amounts helpers"
}
````

### User / tool · 2026-11-02T04:25:40.514Z

**tool result**
````
ec33bf0
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/confidence.py
D  app/backend/date_convention.py
D  app/backend/dismissal_patterns.py
 M app/backend/flags.py
 M app/backend/generator.py
 M app/backend/judges.py
 app/backend/billing.py     | 642 ---------------------------------------------
 tests/unit/test_billing.py | 330 -----------------------
 3 files changed, 2 insertions(+), 974 deletions(-)
---
commit f218263298acd9939c9a9394fd0bbbfbd7c8f61d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:25:02 2026 -0600

    feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
    
    Code-only: ledger lines parse to billed/adjustment/paid/balance, each cited verbatim; totals by provider; LOP and lien amounts listed separately; rates, running balances, claim totals and EOB billed are never totaled. GET /api/cases/{token}/billing.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 4cd0b39..9547667 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -494,6 +494,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
+    from app.backend import billing
+    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
 
     @app.get("/api/cases/{token}/export")
---
39:| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
220:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
629:## GET /api/cases/{token}/billing  (T-083, D-042)
630:Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.
632:{ "billing": {
---
23:def to_cents(figure: str):
24-    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
25-    m = _VALID.match(figure)
26-    if not m:
--
32:def find_amounts(excerpt: str) -> list:
33-    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
34-    out = []
35-    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
--
45:def _label(excerpt: str, start: int) -> str:
46-    before = _BOUNDARY.split(excerpt[:start])[-1]
47-    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
48-    return " ".join((clauses[-1] if clauses else "").split()[-6:])
--
51:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
52-    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
53-    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
54-    needs it to be a billing document."""
--
72:def _is_billing_source(source: str) -> bool:
73-    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))
74-
75-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:45.027Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD=$(git rev-parse --short HEAD)\"; git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"ls-tree exit=$?\"; ls -la app/backend/billing.py tests/unit/test_billing.py 2>&1; echo ---; git log --oneline -8 -- app/backend/billing.py tests/unit/test_billing.py; echo ---; git log --oneline f218263..HEAD | head -40; echo ---; git log --oneline -1 --format='%h %s' -- app/backend/billing.py; git log --all --oneline --diff-filter=D -- app/backend/billing.py",
 "description": "Check whether billing files exist at HEAD and working tree"
}
````

### User / tool · 2026-11-02T04:25:45.323Z

**tool result**
````
HEAD=ec33bf0
ls-tree exit=0
-rw-r--r--@ 1 arsis  staff  36232 Nov  1 22:23 app/backend/billing.py
-rw-r--r--@ 1 arsis  staff  20976 Nov  1 22:23 tests/unit/test_billing.py
---
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
f218263 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
---
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
---
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:48.181Z

**tool call — Bash**
````
{
 "command": "git show --stat ec33bf0 | head -30; echo ---; git show ec33bf0 -- app/backend/billing.py | head -60; echo ---; git show ec33bf0 -- app/backend/api.py | head -60; echo ---; git status --short -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; git diff --stat f218263 HEAD -- app/backend/billing.py tests/unit/test_billing.py",
 "description": "Inspect what T-084 commit did to billing files"
}
````

### User / tool · 2026-11-02T04:25:48.359Z

**tool result**
````
commit ec33bf0de741de8857f7d9cb502ded21a85857f4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:25:03 2026 -0600

    feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py            |   4 +-
 app/backend/billing.py        | 642 ------------------------------------------
 app/backend/pipeline.py       |   5 +-
 app/backend/reclassify.py     | 175 ++++++++++++
 memory/contracts/api.md       |  61 ++--
 tests/unit/test_billing.py    | 330 ----------------------
 tests/unit/test_reclassify.py | 215 ++++++++++++++
 7 files changed, 419 insertions(+), 1013 deletions(-)
---
commit ec33bf0de741de8857f7d9cb502ded21a85857f4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:25:03 2026 -0600

    feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/billing.py b/app/backend/billing.py
deleted file mode 100644
index 7bc3ebb..0000000
--- a/app/backend/billing.py
+++ /dev/null
@@ -1,642 +0,0 @@
-"""Billing analysis on itemized ledgers, claim forms and EOBs (T-083, D-042). CODE ONLY: no model is asked anything here.
-
-What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
-record). Totals are per provider. LOP and lien amounts are listed separately and never added. Nothing is totaled that the records do not
-state (D-019): a rate is never a charge, a running balance is never summed, a claim-form total (UB-04 line 0001, CMS-1500 Item 28) is
-compared with the line sum and never added to it, an EOB's "amount billed" restates the bill and is never added, and a figure that cannot
-be read cleanly (OCR letters, odd decimals, a column that cannot be told apart) is LISTED with cents None and kept out of every total.
-The analysis is computed on read, never stored, and never reaches the letter: the letter's total line is still only accepted charges (D-019).
-Disagreements (ledger total vs line sum, ledger paid vs EOB paid, ...) are raised as `checks`; the code never picks a side.
-Money is whole cents (int); integer arithmetic only.
-"""
-import re
-
-from app.backend import amounts as A, dates
-
-# ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)
-CHECKS = {
-    "LEDGER_TOTAL_MISMATCH": "The statement's own total does not match the sum of its lines. Both figures are shown; check the original.",
-    "LEDGER_BALANCE_MISMATCH": "The stated balance does not equal the charges minus payments and adjustments on the parsed lines.",
-    "BALANCE_STEP_MISMATCH": "This line's running balance does not follow from the line before it, so a column may have been read wrongly.",
-    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed but not totaled.",
-    "CLAIM_TOTAL_MISMATCH": "The claim form's printed total does not match the sum of its lines. Both figures are shown.",
-    "CLAIM_LEDGER_BILLED_MISMATCH": "The claim form and the itemized ledger for this provider show different billed totals. The ledger is used; check both.",
-    "LEDGER_EOB_PAID_MISMATCH": "The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.",
-    "LEDGER_EOB_BILLED_MISMATCH": "The ledger's billed amount for this date and service differs from the amount billed on the EOB.",
-    "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
-}
-RULES = [
-    "Only figures stated in the records are totaled; nothing is derived or estimated.",
-    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is never a charge.",
-    "A running balance, a claim-form total and an EOB's amount billed are never added to the charges.",
-    "LOP, lien and attorney-reduction amounts are listed separately and never totaled with charges.",
-    "A figure that cannot be read cleanly is listed with no value and left out of every total.",
-    "This analysis is for review only. The letter's total line is still accepted charges only.",
-]
-
-# ------------------------------------------------------------------ money tokens
-_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
-_FIG = rf"\(?-?\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\.{_D}+\)?-?"
-_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
-_DATE = r"(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})"
-_ROW = re.compile(rf"^\s*({_DATE})\s+(?:({_DATE})\s+)?(.*)$")
-_VOID = re.compile(r"\b(?:void(?:ed)?|reverse[ds]?|reversal|rev\.?\s+chg)\b", re.IGNORECASE)
-_NEGOTIATED = re.compile(r"\b(?:atty|attorney|lawyer)\s+(?:reduction|adj\w*|discount)|\breduced\s+to\b|\bsettlement\s+(?:reduction|discount)\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
-_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
-_COLS = {"billed": re.compile(r"\b(?:CHARGES?|BILLED)\b", re.IGNORECASE), "paid": re.compile(r"\b(?:PAYMENTS?|PMTS?|PAID)\b", re.IGNORECASE),
---
commit ec33bf0de741de8857f7d9cb502ded21a85857f4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:25:03 2026 -0600

    feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 9547667..a0d6e60 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -494,8 +494,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import billing
-    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import reclassify
+    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
 
     @app.get("/api/cases/{token}/export")
---
 M memory/contracts/api.md
?? app/backend/billing.py
?? tests/unit/test_billing.py
 app/backend/billing.py     | 642 ---------------------------------------------
 tests/unit/test_billing.py | 330 -----------------------
 2 files changed, 972 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:33.905Z

**tool call — Bash**
````
{
 "command": "echo \"SCRATCH=$SCRATCHPAD\"; echo \"$TMPDIR\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -d \"$S\" && mkdir -p \"$S/pin-f218263\" && git archive f218263 | tar -x -C \"$S/pin-f218263\" && ls \"$S/pin-f218263\" && cd \"$S/pin-f218263\" && git -C /Users/arsis/zlayt-pm-project show f218263:app/backend/billing.py | diff -q - app/backend/billing.py && echo \"billing.py identical to f218263 blob\" ; diff -q \"/Users/arsis/zlayt-pm-project/app/backend/billing.py\" \"$S/pin-f218263/app/backend/billing.py\" && echo \"working-tree billing.py == f218263\"; diff -q /Users/arsis/zlayt-pm-project/tests/unit/test_billing.py \"$S/pin-f218263/tests/unit/test_billing.py\" && echo \"working-tree test == f218263\"; du -sh \"$S/pin-f218263\"",
 "description": "Pin f218263 tree into scratchpad via git archive"
}
````

### User / tool · 2026-11-02T04:27:34.363Z

**tool result**
````
SCRATCH=
/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
billing.py identical to f218263 blob
working-tree billing.py == f218263
working-tree test == f218263
 23M	/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pin-f218263
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:37.594Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_billing.py -p no:cacheprovider 2>&1 | tail -5; echo \"---- grep patterns\"; grep -n \"except\\|float(\\|sleep(\\|retry\\|requests\\|httpx\\|app.llm\\|import anthropic\" app/backend/billing.py tests/unit/test_billing.py; echo \"---- classify/to_cents\"; sed -n 20,32p app/backend/amounts.py; sed -n 51,71p app/backend/amounts.py",
 "description": "Run billing tests on pinned f218263 and grep for red-flag patterns"
}
````

### User / tool · 2026-11-02T04:27:38.430Z

**tool result**
````
...........................                                              [100%]
27 passed in 0.42s
---- grep patterns
tests/unit/test_billing.py:330:    assert "app.llm" not in inspect.getsource(mod) and "call(" not in inspect.getsource(mod)
---- classify/to_cents
_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


def find_amounts(excerpt: str) -> list:
def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
    needs it to be a billing document."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
        return "damages"
    if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
        return "charge"
    if _CHARGE_END.search(label):
        return "charge"
    return "unclear"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:40.166Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"cms-1500\\|1500\\|implied\\|decimal\\|ub-04\\|FL 44\\|line 44\\|rate\\|per visit\" research/record-formats.md | cut -c1-400 | head -80",
 "description": "Grep record-formats research for billing traps"
}
````

### User / tool · 2026-11-02T04:27:40.263Z

**tool result**
````
5:tool's hard parts: dates, charges versus rates versus adjustments, totals lines, multiple authors, Spanish text and OCR noise.
17:Section 22 lists every cross-specimen mismatch as fixed or DELIBERATE. Section 23 lists assumptions, gaps and the name-collision search.
27:| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter "Re:" line, intake form, narrative letter "Re:" line | It is the accident date, not a visit. Treating it as an encounter creates a phantom visit and hides the real first-treatment gap. |
28:| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line (unverified convention, see section 23), radiology "Signed", op-note "D:/T:" dictation and transcription stamps |
34:| Date ranges | CMS-1500 24A From/To with 24G units, UB-04 FL 6 statement period, PT "Visits 1 to 12" summary | One line can stand for many consecutive days (NUCC allows grouping only on consecutive days with identical code, charge and provider; days must equal units). |
40:### 1.2 Money: charges, rates, adjustments, estimates
44:| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
45:| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
51:**Number formats.** CMS-1500 boxes use no dollar sign, no comma and no decimal point, with cents in a separate box to the right of a vertical
52:line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
62:An ED visit produces a facility bill (UB-04), an emergency-physician bill (CMS-1500), and a radiologist bill (CMS-1500 with modifier 26) for
80:the UB-04 and CMS-1500.
125:(2 units); 97140 Manual 13 min (1 unit); 97014 E-stim unattended 15 min." "Total timed: 38 min. Total tx: 53 min." "Tolerated well. Continue
127:on the note; they appear on the CMS-1500 or ledger as units times a fee.
152:A: Tolerated well. Progressing toward goal of 70 deg rotation.
169:frequency; provider signature. Many PI chiropractic offices also keep a **travel card** (one row per visit with checkboxes for regions and
174:which may be a fee schedule **rate** or a charge for that visit depending on whether a date of service is attached.
205:Visits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,
218:spasm." "No acute fracture." "Chronic-appearing." "Clinical correlation recommended." Charges appear separately: a technical (facility) bill
229:- ACR *Practice Parameter for Communication of Diagnostic Imaging Findings* (rev. 2020): https://gravitas.acr.org/PPTS/GetDocumentView?docId=74 — **opened**, but only section headings rendered (II.B Components of the Report, II.C Final Report, II.D Preliminary Report). Takeaway from the search summary: a final report must be generated by the interpreting physician; follow-up studies suggeste
270:- One surgery date generates several bills (surgeon, assistant with modifier 80/AS, anesthesia time units, facility/ASC, implants); not duplicates.
295:(DELIBERATE: "12 weeks of therapy" is the surgeon's recital. From the PT evaluation (05/27/2026) to surgery (08/04/2026) is 69 days, about 9.9 weeks.
337:## 8. CMS-1500 (02/12) professional claim
346:line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
347:and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.
350:- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
352:- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
359:- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf — **opened** (text extracted locally). Takeaways: Items 14, 24A, 24F, 24G, 28, 29, 30 as stated above. Newer manual versions may exist (NUCC updates each July); field layout of the 02/12 f
360:- CMS MLN web-based training on the 1500 (lesson 5): https://cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson05/02/index.html — search result, not opened.
362:**Specimen (SYNTHETIC), clean boxed form** (as printed; money boxes have no decimal point, cents sit right of the bar):
364:SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
386:SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
394:(Expected tool behavior: money in 24F and Items 28-29 is parsed as implied-cents in code; the line sum is compared with Item 28 in code;
399:## 9. UB-04 (CMS-1450) institutional claim
405:43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
410:(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
415:- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
420:- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.
426:- Rhode Island EOHHS, *UB-04 Instructions*: https://eohhs.ri.gov/sites/g/files/xkgbur226/files/2021-03/ub04_instructions.pdf — **opened** (text extracted). Takeaways: FL 4 four-digit with leading zero; FL 6 MMDDYY; FL 42 enter "0001" after last revenue code for the total in column 47 (paper only); FL 47 per-line total plus grand total; FL 48 amount not covered by primary payer.
427:- NUBC, *Official UB-04 Data Specifications Manual 2024* (table of contents; FL 47 p.180, FL 48 p.181): https://www.nubc.org/system/files/media/file/2024/04/TOC%20FOR%20NUBC%20SITE%202024%20UB04%20Manual.pdf — search summary; the full manual is licensed.
430:- Assumption: FL 44 title "HCPCS/Rate/HIPPS code" and the creation-date-on-line-23 convention are from prior knowledge, confirmed only by the T-078 reviewer's working knowledge; verify against the NUBC manual before quoting.
434:SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
439:42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
450:**Specimen 2 (SYNTHETIC), inpatient claim with a room rate on the charge line** (a different synthetic patient):
452:SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
457:42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
467:(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money
468:figure adds the rate and the 0001 line and reports 20,181.50 instead of 9,165.75. Admitted 09/15, discharged 09/18 = 3 room days.
489:- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
503:05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
513:(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
515:review; the tool never picks paid or incurred. The $65.00 fee-schedule line has no date of service: a rate, not a charge.)
578:- D Law Group, *What is a Letter of Protection or Personal Injury Lien?*: https://dlawgroup.com/letter-of-protection-personal-injury-lien/ — search summary; LOP can operate as a contract; patient owes the balance if the case is lost.
580:- Assumption: Texas hospital liens (Property Code ch. 55) produce a separate filed notice; I did not open the statute for this card.
612:reposo relativo, cita en 1 semana." "Consulta: $650.00" (charge) vs "Costo por sesión de terapia: $400.00" (rate).
618:- Decimal comma and dot thousands in Latin American notes (`$1.250,00`); US-based clinics usually print `$1,250.00`. Currency may be MXN.
647:per-session rate, not a charge.)
666:| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
667:| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
672:| Skew, blur, shadow, bleed-through | Phone photo of a form | Character error rate rises; Tesseract was weakest on blur and shadow in one study |
714:"Moderate rear-end damage to pt's vehicle, airbags deployed." "Pt c/o neck pain 7/10, denies LOC." "GCS 15." "Pt placed in position of
741:Scene: Moderate rear damage to pt vehicle. Pt self-extricated, ambulatory at scene.
755:(Arrival at destination 23:47 here vs ED arrival 23:48 in section 2: same event, not a conflict. "Moderate rear damage" is the crew's
760:## 16. Ambulance invoice (base rate plus mileage)
764:units = loaded miles, fractional to the tenth); per-unit rate and line charge; supplies lines if itemized; total charges; payments (auto
772:- The per-mile figure (22.50/mi) is a **rate**; only the extended line (195.75) and the stated total are charges (D-042 rate-vs-charge guard;
773:  miles x rate is recomputed in code).
774:- Units are miles with a decimal (8.7), not visits and not integers. A parser that drops the decimal bills 87 miles.
784:- Assumption: the rates in the specimen are invented and do not reflect any fee schedule.
792:CODE      DESCRIPTION                          UNITS   RATE       CHARGE
799:(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)
868:estimated 12 additional visits at $150.00 per visit." "She has not reached MMI."
876:- Future-care costs are estimates and per-visit prices are rates (D-019, D-042): never charges.
896:Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).
900:(Conclusory on purpose, as in v2 pattern P3: no explanation of how or why. $150.00 per visit is a rate and $1,800.00 an estimate; neither is
901:a charge. July 20, 2026 is the letter date. The diagnoses match the CMS-1500 in section 8.)
1006:| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts as implied cents; line sum vs Item 28 compared; days = units checked |
1007:| UB-04 | 0001 total; FL 44 rate on the charge line; creation date; occurrence codes 01-06 | Total line not summed; rate not a charge (D-042 guard); any accident code = accident date |
1014:| Ambulance invoice | Per-mile rate vs line; fractional units | Miles x rate recomputed in code; only line totals are charges |
1022:1. *ER-only then gap*: EMS report + ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + ambulance invoice + fax headers.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:49.093Z

**tool call — Bash**
````
{
 "command": "F=research/record-formats.md; sed -n 40,56p $F | cut -c1-700; echo ....; sed -n 337,358p $F | cut -c1-600; echo ....; sed -n 399,420p $F | cut -c1-500; echo ....; sed -n 484,492p $F | cut -c1-500; echo ...; sed -n 760,800p $F | cut -c1-300",
 "description": "Read money, CMS-1500, UB-04 and fee-schedule sections"
}
````

### User / tool · 2026-11-02T04:27:49.188Z

**tool result**
````
### 1.2 Money: charges, rates, adjustments, estimates
| Wording | Meaning | Counted as a billed charge? (D-019, D-042) |
|---|---|---|
| "Charges", "Total charges", "$Charges", "Amount billed", "Gross charges" | A stated charge for a dated service | Yes, when tied to a date of service and accepted |
| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
| "Payment", "Ins pmt", "Pt pmt", "Plan paid", "Amount paid" (Item 29) | Money received | No |
| "Balance", "Balance due", "Amount due", "You owe", "Patient responsibility" | Remaining amount | No (it is a derived figure) |
| "Estimate", "Anticipated", "Quote", "Future care" | Not yet incurred | No |
| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |

**Number formats.** CMS-1500 boxes use no dollar sign, no comma and no decimal point, with cents in a separate box to the right of a vertical
line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
`(45.00)`, `-45.00`, `45.00-` or `45.00 CR`. Spanish-language clinics in Mexico and much of Latin America use `$1.250,00`; Texas clinics
serving Spanish speakers usually print US format. A running-balance column is cumulative and must never be summed.

### 1.3 Authorship and voice
....
## 8. CMS-1500 (02/12) professional claim

**Fields (NUCC numbering).** 1a insured ID; 2 patient name; 3 DOB (8-digit) and sex; 10a-c condition related to employment / **auto accident
(with state)** / other accident; 11 insured's policy; 14 date of current illness or injury with qualifier (431 onset); 17 referring provider;
21 ICD indicator (0 = ICD-10) and diagnoses A-L; 24A dates of service From/To; 24B place of service; 24D CPT/HCPCS with up to four modifiers;
24E diagnosis pointer (letters); 24F $charges; 24G days or units; 24J rendering provider NPI; 25 federal tax ID; 28 total charge; 29 amount
paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.

**Typical wording and number format.** 24F "is the total billed amount for each service line": dollars right-justified left of a vertical
line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.

**Extraction traps.**
- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
- 24A From/To with 24G = 10 means ten consecutive days on one line; one line is not one visit (NUCC: days must equal units).
- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
- Item 14 is the injury/onset date and Item 31 is the signature date: neither is a service date.
- Item 28 can disagree with the sum of lines (data entry), or a claim may run to a second page with its own lines; sum lines in code and
  compare to Item 28 rather than trusting either.
- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.

**Sources.**
....
## 9. UB-04 (CMS-1450) institutional claim

**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
e.g. 0131 hospital outpatient); **FL 6 statement covers period** From/Through; 8-11 patient name and demographics; 12-13 admission date/hour;
14 admission type; 15 source; 17 discharge status; 31-36 occurrence codes and dates (accident codes 01-06, see traps); 39-41 value codes; **FL 42
revenue code** (4-digit, e.g. 0450 emergency room, 0320 x-ray, 0350 CT, 0610 MRI, 0250 pharmacy, 0636 drugs requiring detailed coding);
43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
line, plus the total after the last line); **48 non-covered charges**; 50 payer; 67 principal diagnosis and 67A-Q other diagnoses; 72
external cause of injury codes; 74 principal procedure; 76 attending provider; 80 remarks.

**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line
(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
outpatient lines.

**Extraction traps.**
- Summing every amount in FL 47 includes the 0001 total line and doubles the bill.
- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
- FL 45 on the total line is the claim creation date (unverified convention), not a service date.
- Occurrence codes 01-06 all carry an accident date: 01 auto accident (current NUBC wording reported as accident/medical coverage), 02
  no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim. A PI claim may
  carry any of them (01 or 03 most often). Extraction treats every one as the accident date, never a service date; packets vary the code.
- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.
....
**Extraction traps.**
- Running balance is cumulative; summing it multiplies the bill.
- Balance forward from a prior statement re-counts earlier charges if two statements are both in the packet.
- Posting date versus date of service: a charge posted 06/30 for a 06/03 visit.
- Reversals ("Void", "Reverse chg") paired with a re-bill on a later line.
- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
- An attorney reduction recorded as an adjustment after settlement talks is a negotiated number, not a billed charge.

**Sources.**
...
## 16. Ambulance invoice (base rate plus mileage)

**Fields.** Agency billing name and tax ID; invoice number, invoice date and run number; date of service; patient; pick-up and drop-off
(origin/destination modifier letters); level of service line (HCPCS A0427 ALS1 emergency, A0429 BLS emergency, etc.); mileage line (A0425,
units = loaded miles, fractional to the tenth); per-unit rate and line charge; supplies lines if itemized; total charges; payments (auto
PIP/MedPay, health plan); adjustments; balance due; "out of network" or balance-billing notice.

**Typical wording.** "A0427-SH ALS emergency transport, Level 1 ... 1,450.00." "A0425-SH Ground mileage 8.7 mi @ 22.50/mi ... 195.75."
"Total charges 1,645.75." "Balance due upon receipt." Origin/destination modifiers pair a pick-up letter with a drop-off letter (S = scene of
accident or acute event, H = hospital, R = residence), so a crash scene to ED trip is SH.

**Extraction traps.**
- The per-mile figure (22.50/mi) is a **rate**; only the extended line (195.75) and the stated total are charges (D-042 rate-vs-charge guard;
  miles x rate is recomputed in code).
- Units are miles with a decimal (8.7), not visits and not integers. A parser that drops the decimal bills 87 miles.
- Every trip is normally two lines (service + mileage) for one encounter; they are not two encounters.
- Only loaded miles (patient on board) are billable for Medicare; commercial and auto carriers vary.
- The invoice date and any statement date are not the service date; the run number ties the invoice to the run report (section 15).
- A balance-billing notice states an asserted balance without a service line (notes only, D-019).

**Sources.**
- CMS, *Medicare Claims Processing Manual*, ch. 15 *Ambulance*: https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf — **opened** (text extracted). Takeaways: origin/destination modifier letters (S = scene of accident or acute event, H = hospital, R = residence ...
- Noridian JE, *Ambulance Mileage*: https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage — **opened**. Takeaway: only loaded miles are paid; round up to the tenth for 100 miles or less; leading zero below 1 mile; missing mileage defaults to 0.1.
- FAIR Health ground-ambulance brief (2023) via research/case-library-sources-v2.md P15 — search excerpt; most claim lines out of network.
- Assumption: the rates in the specimen are invented and do not reflect any fee schedule.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS
Fernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Run SYN-RUN-0912   DOS 05/14/2026
Pick-up: Scene (S)   Drop-off: Quillfeather Regional Medical Center (H)
CODE      DESCRIPTION                          UNITS   RATE       CHARGE
A0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00
A0425-SH  Ground mileage, loaded                8.7       22.50     195.75
                                          TOTAL CHARGES          1,645.75
PAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75
Account noted: attorney representation, letter of protection requested.
```
(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:03.225Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$S/pin-f218263\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\ndef show(tag, out):\n    print(\"==\", tag, \"status=\", out[\"status\"])\n    for p in out[\"providers\"]:\n        print(\"  provider\", p[\"provider\"], \"basis\", p[\"basis\"], \"billed\", p[\"billed\"][\"cents\"], \"adj\", p[\"adjustment\"][\"cents\"], \"paid\", p[\"paid\"][\"cents\"], \"complete\", p[\"complete\"], \"checks\", [c[\"code\"] for c in p[\"checks\"]])\n        for l in p[\"lines\"]:\n            print(\"    line\", l[\"code\"], l[\"description\"][:30], \"kind\", l[\"kind\"], \"billed\", l[\"billed\"] and l[\"billed\"][\"cents\"], \"unclear\", l[\"unclear\"])\n    print(\"  excluded\", [(x[\"figure\"][\"cents\"], x[\"kind\"], x[\"excerpt\"][:60]) for x in out[\"excluded\"]])\n    print(\"  lop\", [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in out[\"lop_lien\"]])\n    print(\"  totals\", out[\"totals\"][\"billed\"])\n# P-A: prose rate sentence\nt = \"Itemized ledger, statement date 06/15/2026. Office visit est. $150.00 per visit. Charge per visit $185.00. New patient exam charge $250.00. Total charges $250.00. Balance due $250.00.\"\nshow(\"A prose rates\", B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)]))\n# P-B: table row whose CHARGES column carries per-visit wording\nt2 = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n06/10/26  06/11/26  99213  Charge per visit              185.00                         185.00\n06/12/26  06/12/26  97110  Therapeutic exercise          130.00                         315.00\n                     TOTAL CHARGES 315.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 315.00\"\"\"\nshow(\"B table row per-visit in CHARGES\", B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t2)]))\n# P-C: unnamed RATE column between UNITS and CHARGES\nt3 = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  UNITS   RATE      CHARGES   PAYMENTS   ADJ     BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise            2     65.00      130.00                    130.00\n                     TOTAL CHARGES 130.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 130.00\"\"\"\nshow(\"C table with RATE column\", B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t3)]))\n# P-D: RATE column with the rate sitting close to CHARGES header, charge missing\nt4 = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  RATE     CHARGES   PAYMENTS   ADJ     BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise         65.00                                  65.00\n                     TOTAL CHARGES 0.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 0.00\"\"\"\nshow(\"D rate column adjacent, no charge\", B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t4)]))\n# P-E: ambulance invoice (no $ sign, no balance header)\namb = \"\"\"SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS\nFernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Run SYN-RUN-0912   DOS 05/14/2026\nCODE      DESCRIPTION                          UNITS   RATE       CHARGE\nA0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00\nA0425-SH  Ground mileage, loaded                8.7       22.50     195.75\n                                          TOTAL CHARGES          1,645.75\nPAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75\"\"\"\nshow(\"E ambulance\", B.analyze([R(1,\"Fernhollow County EMS Billing, ambulance invoice\", amb)]))\nEOF",
 "description": "Probe rate and ledger edge cases on pinned billing code"
}
````

### User / tool · 2026-11-02T04:28:03.595Z

**tool result**
````
== A prose rates status= analyzed
  provider Medlark Clinic basis itemized_ledger billed 25000 adj None paid None complete True checks []
    line None New patient exam charge $250.0 kind charge billed 25000 unclear []
  excluded [(15000, 'rate', 'Itemized ledger, statement date 06/15/2026. Office visit est'), (18500, 'rate', 'Itemized ledger, statement date 06/15/2026. Office visit est')]
  lop []
  totals {'cents': 25000, 'usd': '$250.00'}
== B table row per-visit in CHARGES status= analyzed
  provider Medlark Clinic basis itemized_ledger billed 31500 adj None paid None complete True checks []
    line 99213 Charge per visit kind charge billed 18500 unclear []
    line 97110 Therapeutic exercise kind charge billed 13000 unclear []
  excluded []
  lop []
  totals {'cents': 31500, 'usd': '$315.00'}
== C table with RATE column status= partial_unclear
  provider Medlark Clinic basis itemized_ledger billed 13000 adj None paid None complete False checks []
    line 97110 Therapeutic exercise           kind charge billed 13000 unclear ['65.00']
  excluded []
  lop []
  totals {'cents': 13000, 'usd': '$130.00'}
== D rate column adjacent, no charge status= partial_unclear
  provider Medlark Clinic basis itemized_ledger billed None adj None paid None complete False checks []
    line 97110 Therapeutic exercise kind balance_only billed None unclear ['65.00']
  excluded []
  lop []
  totals {'cents': 0, 'usd': '$0.00'}
== E ambulance status= none_found
  excluded []
  lop []
  totals {'cents': None, 'usd': None}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:20.451Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$S/pin-f218263\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n06/10/26  06/11/26  99213  Charge per visit            $185.00                         $185.00\n06/12/26  06/12/26  97110  Therapeutic exercise        $130.00                         $315.00\n                     TOTAL CHARGES $315.00  TOTAL PMTS $0.00  TOTAL ADJ $0.00  BALANCE DUE $315.00\"\"\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\np = o[\"providers\"][0]\nprint(\"billed\", p[\"billed\"][\"cents\"], \"lines\", [(l[\"code\"], l[\"billed\"] and l[\"billed\"][\"cents\"]) for l in p[\"lines\"]])\nprint(\"excluded\", [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in o[\"excluded\"]], \"checks\", p[\"checks\"])\nprint(\"line_flags\", o[\"line_flags\"])\nprint(\"status\", o[\"status\"], \"totals\", o[\"totals\"][\"billed\"])\n# prose charge variant, no date: rate must not be a charge\nt2 = \"Itemized ledger. Charge per visit $185.00. Total charges $185.00. Balance due $185.00.\"\no2 = B.analyze([R(2,\"Medlark Clinic, itemized ledger\", t2)])\nprint(\"prose-rate-with-total: billed\", o2[\"providers\"][0][\"billed\"][\"cents\"], [(l[\"billed\"] and l[\"billed\"][\"cents\"], l[\"description\"]) for l in o2[\"providers\"][0][\"lines\"]], [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in o2[\"excluded\"]], [c[\"code\"] for c in o2[\"providers\"][0][\"checks\"]])\nEOF",
 "description": "Probe table rows with per-visit rate in CHARGES column"
}
````

### User / tool · 2026-11-02T04:28:20.646Z

**tool result (error)**
````
Exit code 1
billed 31500 lines [('99213', 18500), ('97110', 13000)]
excluded [(18500, 'rate'), (18500, 'rate')] checks []
line_flags []
status analyzed totals {'cents': 31500, 'usd': '$315.00'}
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
IndexError: list index out of range
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:38.951Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && grep -rn '\"text\"' app/backend/ingest.py | head -8; grep -rn \"def load_records\" -A12 app/backend/store.py | head -30; grep -n \"excerpt\" app/backend/ingest.py | head -12",
 "description": "Check how record text and excerpt are produced at ingest"
}
````

### User / tool · 2026-11-02T04:28:39.051Z

**tool result**
````
app/backend/ingest.py:139:            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}
app/backend/ingest.py:324:            at = r["text"].find(line)
app/backend/ingest.py:326:                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
app/backend/ingest.py:334:                                    "evidence": [{"field": "date", "text": r["date_raw"]}]})
app/backend/ingest.py:337:                                    "evidence": [{"field": h["field"], "text": h["phrase"], "start": h["start"], "end": h["end"]} for h in hits]})
app/backend/ingest.py:341:        ev = w["evidence"][0]["text"]
app/backend/ingest.py:356:    text, base = rec.get("text"), rec.get("char_start")
app/backend/ingest.py:357:    out = {"record_no": rec["n"], "field": field, "text": needle, "start": None, "end": None}
app/backend/store.py:14:def load_records(conn, case_id: str, raw: str = None) -> list:
app/backend/store.py-15-    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
app/backend/store.py-16-    if raw is None:
app/backend/store.py-17-        raw = DB.get_case(conn, case_id)["raw_text"]
app/backend/store.py-18-    out = []
app/backend/store.py-19-    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
app/backend/store.py-20-        d = DB._decode(r)
app/backend/store.py-21-        block = raw[d["char_start"]:d["char_end"]]
app/backend/store.py-22-        try:
app/backend/store.py-23-            body = ingest.split_records(block)[0]["excerpt"]
app/backend/store.py-24-        except Exception:
app/backend/store.py-25-            body = block
app/backend/store.py-26-        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
3:Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
60:def _excerpt_extent(rest: str):
61:    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
62:    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
79:    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
92:        exc, used = _excerpt_extent(block[e.end():])
93:        f["excerpt"] = exc
118:        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
131:        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
138:    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
191:        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
192:        if not f["excerpt"]:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:02.562Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/mutants\" && cat > \"$S/mutants/run_mutants.py\" <<'EOF'\nimport shutil, subprocess, sys, os, re\nPIN = sys.argv[1]\nMUT = sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nMUTANTS = {\n \"M1_ub04_rate_to_billed\": (\"app/backend/billing.py\", '            elif k == \"rate\":', '            elif k == \"__off__\":'),\n \"M2_ledger_rate_not_excluded\": (\"app/backend/billing.py\", 'A.classify(body, a, source=r.get(\"source\")) == \"rate\"', 'A.classify(body, a, source=r.get(\"source\")) == \"__off__\"'),\n \"M3_prose_rate_gate_open\": (\"app/backend/billing.py\", 'elif A.classify(seg, a, source=rec.get(\"source\")) == \"charge\":', 'elif A.classify(seg, a, source=rec.get(\"source\")) != \"estimate\":'),\n \"M4_ub04_rates_not_listed\": (\"app/backend/billing.py\", '        out.append(line)\\n    return out, stated, rates', '        out.append(line)\\n    return out, stated, []'),\n \"M5_cms_no_implied_cents\": (\"app/backend/billing.py\", '        cents = int(raw)\\n', '        cents = int(raw) * 100\\n'),\n \"M6_ub04_rate_header_missing\": (\"app/backend/billing.py\", '(\"rate\", r\"HCPCS/RATE|RATE\")', '(\"rate\", r\"ZZZZ_NOHEADER\")'),\n \"M7_failclosed_block_off\": (\"app/backend/billing.py\", '        for l in lines[before:]:', '        for l in []:'),\n \"M8_verifier_ref_text_only\": (\"app/backend/billing.py\", '    text_of = {r[\"n\"]: (r.get(\"text\") or \"\") + \"\\\\n\" + (r.get(\"excerpt\") or \"\") for r in records}', '    text_of = {r[\"n\"]: (r.get(\"text\") or \"\") for r in records}'),\n \"M9_verifier_stubbed\": (\"app/backend/billing.py\", '    text_of = {r[\"n\"]: (r.get(\"text\") or \"\") + \"\\\\n\" + (r.get(\"excerpt\") or \"\") for r in records}', '    return []\\n    text_of = {r[\"n\"]: (r.get(\"text\") or \"\") + \"\\\\n\" + (r.get(\"excerpt\") or \"\") for r in records}'),\n}\nresults = {}\nfor name, (path, old, new) in MUTANTS.items():\n    dst = os.path.join(MUT, name)\n    if os.path.exists(dst): shutil.rmtree(dst)\n    shutil.copytree(PIN, dst, ignore=shutil.ignore_patterns(\"__pycache__\"))\n    f = os.path.join(dst, path)\n    src = open(f, encoding=\"utf-8\").read()\n    n = src.count(old)\n    if n != 1:\n        print(name, \"ANCHOR COUNT\", n); continue\n    open(f, \"w\", encoding=\"utf-8\").write(src.replace(old, new))\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"tests/unit/test_billing.py\", \"-p\", \"no:cacheprovider\", \"-rf\"], cwd=dst, capture_output=True, text=True)\n    failed = re.findall(r\"^FAILED (\\S+)\", p.stdout, re.M)\n    tail = p.stdout.strip().splitlines()[-1]\n    print(f\"{name}: {tail}\")\n    for t in failed: print(\"   \", t)\nEOF\nmkdir -p \"$S/mutants/work\" && cd \"$S/mutants\" && /Users/arsis/zlayt-pm-project/.venv/bin/python run_mutants.py \"$S/pin-f218263\" \"$S/mutants/work\" 2>&1 | tail -60",
 "description": "Run mutation checks on rate, CMS, fail-closed and verifier guards"
}
````

### User / tool · 2026-11-02T04:29:13.423Z

**tool result**
````
M1_ub04_rate_to_billed: 1 failed, 26 passed in 0.42s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M2_ledger_rate_not_excluded: 1 failed, 26 passed in 0.43s
    tests/unit/test_billing.py::test_fee_schedule_rate_is_listed_and_never_a_charge
M3_prose_rate_gate_open: 27 passed in 0.39s
M4_ub04_rates_not_listed: 1 failed, 26 passed in 0.46s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M5_cms_no_implied_cents: 1 failed, 26 passed in 0.42s
    tests/unit/test_billing.py::test_cms1500_ocr_text_never_reads_8500_as_dollars
M6_ub04_rate_header_missing: 1 failed, 26 passed in 0.49s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M7_failclosed_block_off: 27 passed in 0.44s
M8_verifier_ref_text_only: 27 passed in 0.39s
M9_verifier_stubbed: 1 failed, 26 passed in 0.46s
    tests/unit/test_billing.py::test_verify_citations_catches_an_uncited_line
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:20.376Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/mutants/work/M3_prose_rate_gate_open\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\np = o[\"providers\"][0]\nprint(\"MUTANT M3 billed\", p[\"billed\"][\"cents\"], \"lines\", [(l[\"description\"][:40], l[\"billed\"] and l[\"billed\"][\"cents\"]) for l in p[\"lines\"]], \"checks\", [c[\"code\"] for c in p[\"checks\"]])\nprint(\"excluded\", [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in o[\"excluded\"]])\nEOF\necho \"--- same probe on pinned f218263:\"; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\np = o[\"providers\"][0]\nprint(\"PINNED billed\", p[\"billed\"][\"cents\"], \"lines\", [(l[\"description\"][:40], l[\"billed\"] and l[\"billed\"][\"cents\"]) for l in p[\"lines\"]], \"checks\", [c[\"code\"] for c in p[\"checks\"]])\nprint(\"excluded\", [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in o[\"excluded\"]])\nEOF",
 "description": "Confirm the prose rate gate mutant changes totals"
}
````

### User / tool · 2026-11-02T04:29:20.707Z

**tool result**
````
MUTANT M3 billed 43500 lines [('New patient exam charge $250.00.', 25000), ('Charge per visit $185.00.', 18500)] checks []
excluded [(18500, 'rate')]
--- same probe on pinned f218263:
PINNED billed 25000 lines [('New patient exam charge $250.00.', 25000)] checks ['LEDGER_TOTAL_MISMATCH', 'LEDGER_BALANCE_MISMATCH']
excluded [(18500, 'rate')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:36.752Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\nfrom app.backend.billing import box_amount as bx\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nbase = \"\"\"SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060326   060326   11     97014              A      90 | 00       3      SYN-NPI-0001\n28. TOTAL CHARGE  260 | 00     29. AMOUNT PAID  0 | 00\"\"\"\ndef run(tag, t):\n    o = B.analyze([R(1,\"Brightwater Spine & Wellness, CMS-1500\", t)])\n    ps = o[\"providers\"]\n    if not ps: print(tag, \"NO PROVIDER; status\", o[\"status\"]); return\n    p = ps[0]\n    print(tag, \"billed\", p[\"billed\"][\"cents\"], \"lines\", len(p[\"lines\"]), \"checks\", [c[\"code\"] for c in p[\"checks\"]], \"complete\", p[\"complete\"], \"status\", o[\"status\"])\nrun(\"base            \", base)\nrun(\"V1 24F 85.00    \", base.replace(\"AB     85 | 00       1\", \"AB     85.00   1\"))\nrun(\"V2 slash dates  \", base.replace(\"060126   060126\", \"06/01/26 06/01/26\"))\nrun(\"V3 no units col \", base.replace(\"AB     85 | 00       1      SYN\", \"AB     85 | 00      SYN\"))\nrun(\"V4 no item 28   \", base.replace(\"28. TOTAL CHARGE  260 | 00     \", \"\"))\nprint(\"box_amount:\", {k: bx(k)[\"cents\"] for k in [\"85\", \"85|00\", \"85 00\", \"8500\", \"0 00\", \"1850\", \"85.00\", \"45 OO\"]})\nEOF",
 "description": "Probe CMS-1500 line parsing variants and box_amount values"
}
````

### User / tool · 2026-11-02T04:29:36.951Z

**tool result**
````
base             billed 26000 lines 3 checks [] complete True status analyzed
V1 24F 85.00     billed 9000 lines 1 checks ['CLAIM_TOTAL_MISMATCH'] complete True status analyzed
V2 slash dates   billed 17500 lines 2 checks ['CLAIM_TOTAL_MISMATCH'] complete True status analyzed
V3 no units col  billed 9000 lines 1 checks ['CLAIM_TOTAL_MISMATCH'] complete True status analyzed
V4 no item 28    billed 26000 lines 3 checks [] complete True status analyzed
box_amount: {'85': None, '85|00': 8500, '85 00': 8500, '8500': 8500, '0 00': 0, '1850': 1850, '85.00': 8500, '45 OO': None}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:47.107Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"\"\"SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n    060126   060126   11     98941              AB     85.00       1      SYN-NPI-0001\n    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060326   060326   11     97014              A      90 | 00       3      SYN-NPI-0001\"\"\"\no = B.analyze([R(1,\"Brightwater Spine & Wellness, CMS-1500\", t)])\np = o[\"providers\"][0]\nprint(\"V5 billed\", p[\"billed\"][\"cents\"], \"lines\", len(p[\"lines\"]), \"unclear_lines\", p[\"unclear_lines\"], \"complete\", p[\"complete\"], \"checks\", p[\"checks\"], \"line_flags\", o[\"line_flags\"], \"status\", o[\"status\"])\nprint(\"excerpt-count-in-text\", t.count(\"85.00\"))\nEOF",
 "description": "Probe a dropped CMS-1500 line with no Item 28 total"
}
````

### User / tool · 2026-11-02T04:29:47.288Z

**tool result**
````
V5 billed 17500 lines 2 unclear_lines 0 complete True checks [] line_flags [] status analyzed
excerpt-count-in-text 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:56.149Z

**tool call — Bash**
````
{
 "command": "echo \"--- HEAD api.py billing refs:\"; git show HEAD:app/backend/api.py | grep -n \"billing\" ; echo \"exit=$?\"; echo \"--- HEAD contracts billing refs:\"; git show HEAD:memory/contracts/api.md | grep -c \"billing\"; echo \"--- working tree api.py billing refs:\"; grep -n \"billing\" app/backend/api.py; echo \"--- route in pinned f218263 billing.py:\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n \"verify_citations\" \"$S/pin-f218263/app/backend/billing.py\" \"$S/pin-f218263/app/backend/api.py\"; echo \"--- multiplication / float in billing.py:\"; grep -n \"[^*]\\*[^*]\" \"$S/pin-f218263/app/backend/billing.py\" | grep -v '^\\s*#' | head; grep -n \"float\\|round(\" \"$S/pin-f218263/app/backend/billing.py\"; echo \"--- route lines:\"; sed -n 634,642p \"$S/pin-f218263/app/backend/billing.py\"; echo \"--- wrap in except/finally count:\"; grep -c \"except\" \"$S/pin-f218263/app/backend/billing.py\"",
 "description": "Verify HEAD state for billing route and route verifier wiring"
}
````

### User / tool · 2026-11-02T04:29:56.371Z

**tool result**
````
--- HEAD api.py billing refs:
exit=1
--- HEAD contracts billing refs:
1
--- working tree api.py billing refs:
507:    from app.backend import billing
508:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
--- route in pinned f218263 billing.py:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pin-f218263/app/backend/billing.py:610:def verify_citations(analysis: dict, records: list) -> list:
--- multiplication / float in billing.py:
40:_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
42:_ROW = re.compile(rf"^\s*({_DATE})\s+(?:({_DATE})\s+)?(.*)$")
44:_NEGOTIATED = re.compile(r"\b(?:atty|attorney|lawyer)\s+(?:reduction|adj\w*|discount)|\breduced\s+to\b|\bsettlement\s+(?:reduction|discount)\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
45:_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
79:    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
114:        if _ROW.match(ln) or re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or "$" in ln or not re.search(r"\S\s{2,}\S", ln):
140:        if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
173:_STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIG})", re.IGNORECASE),
174:           "paid": re.compile(rf"TOTAL\s+(?:PMTS?|PAYMENTS?)\s*[:=]?\s*({_FIG})", re.IGNORECASE),
175:           "adjustment": re.compile(rf"TOTAL\s+ADJ\w*\s*[:=]?\s*({_FIG})", re.IGNORECASE),
390:def _line_around(body, start, end):
492:                                     "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, "excerpt": _line_around(body, a["start"], a["end"])})
--- route lines:
def add_routes(app, *, conn, get_case):
    @app.get("/api/cases/{token}/billing")
    def billing_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"billing": for_case(c, token)}
        finally:
            c.close()
--- wrap in except/finally count:
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:30:05.120Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD:$PWD/tests/unit\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport json\nimport test_billing as T\nfrom app.backend import billing as B\nfrom app.backend.billing import analyze\ncases = {\n \"ledger+eob\": [T.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", T.LEDGER), T.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", T.EOB)],\n \"cms_clean\": [T.rec(1, \"Brightwater Spine & Wellness, CMS-1500\", T.CMS_CLEAN)],\n \"cms_ocr\": [T.rec(1, \"Brightwater Spine & Wellness, CMS-1500 (OCR)\", T.CMS_OCR)],\n \"ub04\": [T.rec(1, \"Saltmarrow General Hospital, UB-04\", T.UB_ROOM)],\n \"prose+lop\": [T.rec(1, \"Fennimoor Spine Clinic, itemized ledger\", T.PROSE), T.rec(2, \"Pellingham and Rook PLLC, correspondence (letter of protection)\", T.LOP)],\n}\ndef walk(o, rec_text, path, bad, counts):\n    if isinstance(o, dict):\n        rn = o.get(\"record_no\")\n        for k, v in o.items():\n            if k in (\"excerpt\",) and isinstance(v, str):\n                counts[\"excerpt\"] += 1\n                if rn is not None and v not in rec_text.get(rn, \"\"): bad.append((path + \".\" + k, v[:60]))\n            if k == \"cite\" and isinstance(v, dict):\n                counts[\"cite\"] += 1\n                if v[\"excerpt\"] not in rec_text.get(v[\"record_no\"], \"\"): bad.append((path + \".cite\", v[\"excerpt\"][:60]))\n            if k == \"cites\" and isinstance(v, list):\n                for c in v:\n                    counts[\"cites\"] += 1\n                    if c[\"excerpt\"] not in rec_text.get(c[\"record_no\"], \"\"): bad.append((path + \".cites\", c[\"excerpt\"][:60]))\n            if k == \"figure\" and isinstance(v, dict) and rn is not None:\n                counts[\"figure\"] += 1\n                if v[\"text\"].lstrip(\"-\") not in rec_text.get(rn, \"\") and v[\"text\"] not in rec_text.get(rn, \"\"): bad.append((path + \".figure\", v[\"text\"]))\n            walk(v, rec_text, path + \".\" + k, bad, counts)\n    elif isinstance(o, list):\n        for i, v in enumerate(o): walk(v, rec_text, f\"{path}[{i}]\", bad, counts)\nfor name, recs in cases.items():\n    out = analyze(recs)\n    rec_text = {r[\"n\"]: r[\"text\"] for r in recs}\n    bad, counts = [], {\"excerpt\": 0, \"cite\": 0, \"cites\": 0, \"figure\": 0}\n    walk(out, rec_text, name, bad, counts)\n    print(name, \"status\", out[\"status\"], \"checked\", counts, \"verbatim-violations\", len(bad), \"verify_citations\", B.verify_citations(out, recs))\n    if bad: print(\"  BAD\", bad[:5])\nEOF",
 "description": "Independently check every excerpt and cite against record text"
}
````

### User / tool · 2026-11-02T04:30:05.628Z

**tool result**
````
/bin/bash: child setpgid (14431 to 14431): Operation not permitted
ledger+eob status analyzed checked {'excerpt': 31, 'cite': 5, 'cites': 15, 'figure': 1} verbatim-violations 0 verify_citations []
cms_clean status analyzed checked {'excerpt': 12, 'cite': 2, 'cites': 5, 'figure': 0} verbatim-violations 0 verify_citations []
cms_ocr status partial_unclear checked {'excerpt': 15, 'cite': 4, 'cites': 5, 'figure': 0} verbatim-violations 0 verify_citations []
ub04 status analyzed checked {'excerpt': 12, 'cite': 1, 'cites': 5, 'figure': 1} verbatim-violations 0 verify_citations []
prose+lop status analyzed checked {'excerpt': 18, 'cite': 3, 'cites': 5, 'figure': 2} verbatim-violations 0 verify_citations []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:30:12.330Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD:$PWD/tests/unit\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport test_billing as T\nfrom app.backend.billing import analyze\nrecs = [T.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", T.LEDGER), T.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", T.EOB)]\nout = analyze(recs)\ntxt = {r[\"n\"]: r[\"text\"] for r in recs}\nn = bad = 0\nfor p in out[\"providers\"]:\n    for l in p[\"lines\"]:\n        for k in (\"billed\", \"adjustment\", \"paid\", \"balance\"):\n            f = l.get(k)\n            if f:\n                n += 1\n                t = f[\"text\"].lstrip(\"-\")\n                if t not in l[\"excerpt\"] or f.get(\"cite\") and False: bad += 1; print(\"NOT IN EXCERPT\", k, f[\"text\"], l[\"excerpt\"])\nprint(\"figure-in-excerpt checked\", n, \"bad\", bad)\np = out[\"providers\"][0]\nprint(\"\\nHAND RECOMPUTE vs CODE (Larkspur ledger)\")\nprint(\"lines (code, billed, adj, bal):\")\nfor l in p[\"lines\"]:\n    g = lambda k: (l[k][\"cents\"] if l.get(k) else None)\n    print(f\"  {l['dos']:9} {l['code']:6} {l['description'][:26]:26} billed={g('billed')} adj={g('adjustment')} bal={g('balance')} kind={l['kind']}\")\nprint(\"code: billed\", p[\"billed\"][\"cents\"], \"adj\", p[\"adjustment\"][\"cents\"], \"paid\", p[\"paid\"], \"balance(stated)\", p[\"balance\"][\"cents\"], \"stated\", {k: v[\"cents\"] for k, v in p[\"stated_totals\"].items()}, \"checks\", p[\"checks\"])\nhand = {\"billed\": 21000+13000+7000+3500-7000+7000, \"adj\": 4500, \"bal\": 40000}\nprint(\"hand:  billed\", hand[\"billed\"], \"adj\", hand[\"adj\"], \"balance = 44500-0-4500 =\", 44500-0-4500)\nprint(\"rate excluded:\", [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in out[\"excluded\"]])\nEOF",
 "description": "Recompute Larkspur ledger by hand and compare to code output"
}
````

### User / tool · 2026-11-02T04:30:12.833Z

**tool result**
````
figure-in-excerpt checked 14 bad 0

HAND RECOMPUTE vs CODE (Larkspur ledger)
lines (code, billed, adj, bal):
  05/27/26  97162  PT eval moderate complexit billed=21000 adj=None bal=21000 kind=charge
  06/10/26  97110  Therapeutic exercise x2    billed=13000 adj=None bal=34000 kind=charge
  06/10/26  97140  Manual therapy x1          billed=7000 adj=None bal=41000 kind=charge
  06/10/26  97014  E-stim unattended          billed=3500 adj=None bal=44500 kind=charge
  06/10/26  97140  Manual therapy x1 VOID     billed=-7000 adj=None bal=37500 kind=reversal
  06/10/26  97140  Manual therapy x1          billed=7000 adj=None bal=44500 kind=charge
  07/15/26  ADJ    Courtesy discount          billed=None adj=4500 bal=40000 kind=adjustment
code: billed 44500 adj 4500 paid {'cents': None, 'usd': None} balance(stated) 40000 stated {'billed': 44500, 'paid': 0, 'adjustment': 4500, 'balance': 40000} checks []
hand:  billed 44500 adj 4500 balance = 44500-0-4500 = 40000
rate excluded: [(6500, 'rate')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:30:53.858Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && grep -n 'A rate (per visit\\|_CMS = re.compile\\|def box_amount\\|def _cms1500\\|elif k == \"rate\"\\|if not m:\\|m = _ROW.match(ln)\\|A.classify(body, a\\|A.classify(seg, a\\|for l in lines\\[before:\\]\\|if l\\[\"excerpt\"\\] not in text\\|def verify_citations\\|Run in tests and by the API\\|text_of = \\|def add_routes\\|return {\"billing\"\\|sum(p\\[\"billed\"\\]\\[\"cents\"\\] or 0\\|elif k == \"rate\"\\|excluded += rates\\|cents = int(raw)\\|\"rate\", r\"HCPCS\\|if l\\[\"billed\"\\] is None\\|elif line\\[\"billed\"\\] is None' app/backend/billing.py; echo ---; grep -n 'for every' app/backend/amounts.py; echo ---; grep -n \"def test_\" tests/unit/test_billing.py | sed -n 1,40p | grep -n \"fee_schedule\\|ub04\\|cms1500\\|verify_citations\\|route\\|prose\\|ledger_prose\\|ledger_lines\\|injection\" ; echo ---; echo \"git ls-tree HEAD:\"; cd /Users/arsis/zlayt-pm-project && git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"rc=$?\"; git show --stat --format='%h %ad %s' ec33bf0 | head -1; ls reviews/T-083* 2>&1",
 "description": "Proof-read cited line numbers and check review file absence"
}
````

### User / tool · 2026-11-02T04:30:54.049Z

**tool result (error)**
````
Exit code 1
30:    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is never a charge.",
148:        m = _ROW.match(ln)
149:        if not m:
228:            elif A.classify(seg, a, source=rec.get("source")) == "charge":
242:_CMS = re.compile(rf"^\s*(?:24\.\s*)?([0-9O]{{6}})\s+([0-9O]{{6}})\s+(\d{{2}})\s+([A-Z0-9]{{5}})(?:\s+[A-Z0-9]{{1,4}})*?\s+({_AMT})\s+(\d+)(?:\s+(\S+))?\s*$")
247:def box_amount(raw: str) -> dict:
262:        cents = int(raw)
268:def _cms1500(rec, lines):
302:    for kind, rx in (("rate", r"HCPCS/RATE|RATE"), ("billed", r"TOTAL\s+CHARGES"), ("noncovered", r"NON-COVERED")):
309:        if not m:
325:            elif k == "rate":
329:            elif line["billed"] is None:
352:        if not m:
480:            excluded += rates
485:        for l in lines[before:]:                       # fail closed: a line that is not a verbatim excerpt of its record shows no figures
486:            if l["excerpt"] not in text:
490:                if a["cents"] is not None and A.classify(body, a, source=r.get("source")) == "rate":
491:                    excluded.append({"record_no": r["n"], "kind": "rate", "why": "A rate (per visit, per unit) is a price, not a charge.",
603:        "totals": {"billed": _tot(sum(p["billed"]["cents"] or 0 for p in providers)) if providers else _tot(None),
610:def verify_citations(analysis: dict, records: list) -> list:
612:    Run in tests and by the API before a response leaves: a line that fails is dropped from the response, never shown uncited."""
613:    text_of = {r["n"]: (r.get("text") or "") + "\n" + (r.get("excerpt") or "") for r in records}
634:def add_routes(app, *, conn, get_case):
640:            return {"billing": for_case(c, token)}
---
33:    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
116:    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
---
1:88:def test_ledger_lines_parse_to_four_figures_each_cited():
3:111:def test_fee_schedule_rate_is_listed_and_never_a_charge():
12:180:def test_ledger_prose_statement_parses_and_checks_its_own_total():
17:219:def test_cms1500_boxes_are_implied_cents_and_checked_against_item_28():
18:226:def test_cms1500_ocr_text_never_reads_8500_as_dollars():
19:236:def test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added():
22:269:def test_verify_citations_catches_an_uncited_line():
23:285:def test_billing_route_for_a_pasted_case(client):
25:315:def test_prose_charges_without_a_date_of_service_are_counted_as_stated_and_flagged():
26:320:def test_injection_tagged_record_is_skipped_not_totaled():
---
git ls-tree HEAD:
rc=0
ec33bf0 Sun Nov 1 22:25:03 2026 -0600 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
ls: reviews/T-083*: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:00.458Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise          130.00                         130.00\n          06/11/26  97014  E-stim unattended              35.00                         165.00\n06/12/26  06/12/26  97140  Manual therapy                 70.00                         235.00\n                     TOTAL CHARGES 235.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 235.00\"\"\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\np = o[\"providers\"][0]\nprint(\"table row without DOS: billed\", p[\"billed\"][\"cents\"], \"lines\", [l[\"code\"] for l in p[\"lines\"]], \"complete\", p[\"complete\"], \"checks\", [c[\"code\"] for c in p[\"checks\"]], \"status\", o[\"status\"])\nEOF\necho \"--- second run of billing tests on pinned copy (determinism)\"; cd \"$S/pin-f218263\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_billing.py -p no:cacheprovider 2>&1 | tail -1",
 "description": "Probe ledger table row without date and rerun tests for determinism"
}
````

### User / tool · 2026-11-02T04:31:01.428Z

**tool result**
````
table row without DOS: billed 23500 lines ['97110', '97014', '97140'] complete True checks [] status analyzed
--- second run of billing tests on pinned copy (determinism)
27 passed in 0.45s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:12.171Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise          130.00                         130.00\n                            97014  E-stim unattended              35.00                         165.00\n06/12/26  06/12/26  97140  Manual therapy                 70.00                         235.00\n                     TOTAL CHARGES 235.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 235.00\"\"\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\np = o[\"providers\"][0]\nprint(\"row with no date: billed\", p[\"billed\"][\"cents\"], \"lines\", [l[\"code\"] for l in p[\"lines\"]], \"complete\", p[\"complete\"], \"checks\", [c[\"code\"] for c in p[\"checks\"]], \"status\", o[\"status\"])\nEOF",
 "description": "Probe a ledger table row with no date at all"
}
````

### User / tool · 2026-11-02T04:31:12.365Z

**tool result**
````
row with no date: billed 20000 lines ['97110', '97140'] complete True checks ['LEDGER_TOTAL_MISMATCH', 'LEDGER_BALANCE_MISMATCH'] status analyzed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:28.025Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nfrom app.backend import billing as B\ndef R(n, src, t): return {\"n\": n, \"source\": src, \"excerpt\": t, \"text\": t}\nt = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise          130.00                         130.00\n          06/11/26  97014  E-stim unattended              35.00                         165.00\n                     TOTAL CHARGES 165.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 165.00\"\"\"\no = B.analyze([R(1,\"Medlark Clinic, itemized ledger\", t)])\nprint([(l[\"code\"], l[\"dos\"], l[\"posted\"]) for l in o[\"providers\"][0][\"lines\"]])\nEOF\nE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1; mkdir -p \"$E\" && cp \"$S/mutants/run_mutants.py\" \"$E/run_mutants.py\" && cd \"$S/mutants\" && /Users/arsis/zlayt-pm-project/.venv/bin/python run_mutants.py \"$S/pin-f218263\" \"$S/mutants/work\" > \"$E/mutants.log\" 2>&1; cat \"$E/mutants.log\"; ls -la \"$E\"",
 "description": "Confirm posted-date DOS case and save mutation evidence log"
}
````

### User / tool · 2026-11-02T04:31:39.575Z

**tool result**
````
[('97110', '06/10/26', '06/11/26'), ('97014', '06/11/26', None)]
M1_ub04_rate_to_billed: 1 failed, 26 passed in 0.43s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M2_ledger_rate_not_excluded: 1 failed, 26 passed in 0.44s
    tests/unit/test_billing.py::test_fee_schedule_rate_is_listed_and_never_a_charge
M3_prose_rate_gate_open: 27 passed in 0.52s
M4_ub04_rates_not_listed: 1 failed, 26 passed in 0.43s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M5_cms_no_implied_cents: 1 failed, 26 passed in 0.44s
    tests/unit/test_billing.py::test_cms1500_ocr_text_never_reads_8500_as_dollars
M6_ub04_rate_header_missing: 1 failed, 26 passed in 0.44s
    tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added
M7_failclosed_block_off: 27 passed in 0.42s
M8_verifier_ref_text_only: 27 passed in 0.41s
M9_verifier_stubbed: 1 failed, 26 passed in 0.44s
    tests/unit/test_billing.py::test_verify_citations_catches_an_uncited_line
total 16
drwxr-xr-x@   4 arsis  staff    128 Nov  1 22:31 .
drwxr-xr-x@ 727 arsis  staff  23264 Nov  1 22:31 ..
-rw-r--r--@   1 arsis  staff   1018 Nov  1 22:31 mutants.log
-rw-r--r--@   1 arsis  staff   2427 Nov  1 22:31 run_mutants.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:44.980Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-083-r1 && { echo \"# T-083 r1 repo-state evidence (reviewer: staff-engineer-reviewer)\"; echo \"\\$ git rev-parse --short HEAD\"; git rev-parse --short HEAD; echo \"\\$ git log --format='%h %ad %s' --date=iso -3 -- app/backend/billing.py tests/unit/test_billing.py\"; git log --format='%h %ad %s' --date=iso -3 -- app/backend/billing.py tests/unit/test_billing.py; echo \"\\$ git show --stat --format='%h %ad' ec33bf0 | sed -n 1,12p\"; git show --stat --format='%h %ad' --date=iso ec33bf0 | sed -n 1,12p; echo \"\\$ git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py   (empty output = absent at HEAD)\"; git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"\\$ git show HEAD:app/backend/api.py | grep -n billing ; echo rc=\\$?\"; git show HEAD:app/backend/api.py | grep -n billing; echo \"rc=$?\"; echo \"\\$ git show f218263 --stat --format='%h %ad' --date=iso | sed -n 1,8p\"; git show f218263 --stat --format='%h %ad' --date=iso | sed -n 1,8p; echo \"\\$ git status --short -- app/backend/billing.py tests/unit/test_billing.py\"; git status --short -- app/backend/billing.py tests/unit/test_billing.py; echo \"\\$ diff working-tree billing.py vs f218263 blob\"; git show f218263:app/backend/billing.py | diff -q - app/backend/billing.py && echo identical; } > \"$E/head_state.txt\" 2>&1; cat \"$E/head_state.txt\"",
 "description": "Save repo-state evidence for the HEAD deletion finding"
}
````

### User / tool · 2026-11-02T04:31:45.269Z

**tool result**
````
# T-083 r1 repo-state evidence (reviewer: staff-engineer-reviewer)
$ git rev-parse --short HEAD
02ff244
$ git log --format='%h %ad %s' --date=iso -3 -- app/backend/billing.py tests/unit/test_billing.py
ec33bf0 2026-11-01 22:25:03 -0600 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
f218263 2026-11-01 22:25:02 -0600 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
$ git show --stat --format='%h %ad' ec33bf0 | sed -n 1,12p
ec33bf0 2026-11-01 22:25:03 -0600

 app/backend/api.py            |   4 +-
 app/backend/billing.py        | 642 ------------------------------------------
 app/backend/pipeline.py       |   5 +-
 app/backend/reclassify.py     | 175 ++++++++++++
 memory/contracts/api.md       |  61 ++--
 tests/unit/test_billing.py    | 330 ----------------------
 tests/unit/test_reclassify.py | 215 ++++++++++++++
 7 files changed, 419 insertions(+), 1013 deletions(-)
$ git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py   (empty output = absent at HEAD)
$ git show HEAD:app/backend/api.py | grep -n billing ; echo rc=$?
rc=1
$ git show f218263 --stat --format='%h %ad' --date=iso | sed -n 1,8p
f218263 2026-11-01 22:25:02 -0600

 app/backend/api.py         |   2 +
 app/backend/billing.py     | 642 +++++++++++++++++++++++++++++++++++++++++++++
 memory/contracts/api.md    |  37 +++
 tests/unit/test_billing.py | 330 +++++++++++++++++++++++
 4 files changed, 1011 insertions(+)
$ git status --short -- app/backend/billing.py tests/unit/test_billing.py
?? app/backend/billing.py
?? tests/unit/test_billing.py
$ diff working-tree billing.py vs f218263 blob
identical
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:48.982Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && echo --- && git show --stat --format='%h %s' HEAD | sed -n 1,8p && echo --- && git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"ls-tree rc=$?\"; git show HEAD:app/backend/api.py | grep -c \"billing\"; echo \"--- head_state append\"; E=artifacts/review-evidence/T-083-r1; { echo; echo \"\\$ git log --oneline -4   (HEAD moved from ec33bf0 to 02ff244 during review)\"; git log --oneline -4; echo \"\\$ git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py   (re-run at 02ff244: empty)\"; git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"\\$ git show HEAD:app/backend/api.py | grep -c billing   -> $(git show HEAD:app/backend/api.py | grep -c billing)\"; } >> \"$E/head_state.txt\"; tail -12 \"$E/head_state.txt\"",
 "description": "Re-check HEAD after it moved and append to evidence"
}
````

### User / tool · 2026-11-02T04:31:49.045Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  $(git show HEAD:app/backend/api.py | grep -c billing))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:52.017Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && echo --- && git show --stat --format='%h %s' HEAD | sed -n 1,8p && echo --- && git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py; echo \"ls-tree rc=$?\"; git show HEAD:app/backend/api.py | grep -c billing",
 "description": "Re-check HEAD state after it moved"
}
````

### User / tool · 2026-11-02T04:31:52.214Z

**tool result**
````
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
823b718 feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
---
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)

 evals/reports/calibration.json | 70 ++++++++++++++++++++++++++----------------
 1 file changed, 44 insertions(+), 26 deletions(-)
---
ls-tree rc=0
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:30.637Z

**tool call — Bash**
````
{
 "command": "grep -n \"per visit\\|per unit\\|est\\. \\$\" tests/unit/test_billing.py | cut -c1-160; echo \"rc=$?\"; echo ---; grep -n \"verify_citations\" app/backend/api.py; echo \"api rc=$?\"; echo ---; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD\" /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nfrom app.backend import billing as B\nr=[{'n':1,'source':'Medlark Clinic, itemized ledger','excerpt':'x','text':'x'}]\nt='''DOS       POSTED    CODE   DESCRIPTION                  UNITS   RATE      CHARGES   PAYMENTS   ADJ     BALANCE\n06/10/26  06/11/26  97110  Therapeutic exercise            2     65.00      130.00                    130.00\n                     TOTAL CHARGES 130.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 130.00'''\nr[0]['excerpt']=t; r[0]['text']=t\no=B.analyze(r); print('F9 probe billed', o['providers'][0]['billed']['cents'], 'unclear', o['providers'][0]['lines'][0]['unclear'], 'excluded', o['excluded'], 'complete', o['providers'][0]['complete'])\n\"",
 "description": "Confirm test coverage gaps and rate-column probe before writing"
}
````

### User / tool · 2026-11-02T04:32:30.791Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No closing quotation)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:32.896Z

**tool call — Bash**
````
{
 "command": "grep -n -F \"per visit\" tests/unit/test_billing.py | cut -c1-160; grep -n -F \"per unit\" tests/unit/test_billing.py | cut -c1-160; grep -c -F \"verify_citations\" app/backend/api.py",
 "description": "Check test file for prose rate wording and api verifier wiring"
}
````

### User / tool · 2026-11-02T04:32:33.004Z

**tool result**
````
24:Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection."""
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:26.728Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-083-staff-engineer.md",
 "content": "# T-083 review (r1): billing analysis on itemized ledgers (staff-engineer-reviewer)\n\n**Verdict: fail.** Three blockers, three majors, three minors.\n\nNotes for the orchestrator, before the findings:\n- **Model.** This review is by claude-haiku-5-5, as the brief states and as this session runs. CLAUDE.md section 6 and D-024 call for Sonnet on engineering reviewers, and the persona file expects claude-sonnet-5-5. The dispatch needs a check.\n- **F1 is a repo-state defect, not a defect in f218263.** It was caused by another card's commit (ec33bf0, T-084). I rated it blocker under D.2 (\"makes the must-have unusable\"), because on HEAD the D-042 billing route does not exist. F2 and F3 are code defects that stand on their own.\n- **Brief checks.** Verbatim excerpts: pass (independent check, zero violations). Hand recompute of the Larkspur ledger: matches the code. Rate guard mutation in a scratch copy: UB-04 and table-ledger rate guards are caught; the prose rate guard is not (F4), and table-row rates are not guarded at all (F2). CMS-1500 implied cents: handled and tested (mutant M5 caught).\n\n## What I exercised\n\n- Read: `personas/staff-engineer.md`, `board/cards/T-083.md`, `memory/ORCHESTRATOR_DECISIONS.md` (D-019 line 27, D-042 line 50), `research/record-formats.md` (sections 1.1, 1.2, 8, 9, 16 and the fee-schedule trap at line 489), `app/backend/billing.py` (642 lines, full), `tests/unit/test_billing.py` (330 lines, full), `app/backend/amounts.py` (`find_amounts` line 33, `classify` 51-70).\n- Pinned f218263 with `git archive f218263` into the session scratchpad (`pin-f218263`). Working-tree `billing.py` and `test_billing.py` are byte-identical to the f218263 blobs (`git show f218263:... | diff -q`).\n- `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: **27 passed** on the working tree, **27 passed** on the pinned copy, **27 passed** on a second run (determinism).\n- Repo state at HEAD (`git ls-tree`, `git show --stat ec33bf0`, `git show HEAD:app/backend/api.py | grep -c billing`): evidence in `artifacts/review-evidence/T-083-r1/head_state.txt`.\n- Mutation runner `artifacts/review-evidence/T-083-r1/run_mutants.py` on scratch copies (log `artifacts/review-evidence/T-083-r1/mutants.log`): nine mutants, results in F4 and F5.\n- Probes (python against the pinned copy and mutant copies): prose rate sentences; table rows with per-visit wording, with and without `$`; unnamed RATE column; RATE column with no charge; ambulance invoice (research section 16 specimen); CMS-1500 variants (printed decimal, slash dates, no Item 28); `box_amount` values; ledger rows with blank DOS and with no date.\n- Independent verbatim check: every `excerpt`, `cite`, `cites[]`, and figure text in the five billing output shapes (ledger+EOB, CMS clean, CMS OCR, UB-04, prose+LOP) checked as a substring of the record's own `text` field. 0 violations across 31 excerpts, 15 cites and 14 line figures, not using `verify_citations`.\n- Hand recompute of the Larkspur ledger (tests/unit/test_billing.py `LEDGER`): lines 210.00, 130.00, 70.00, 35.00, (70.00) VOID, 70.00, ADJ 45.00 credit. Billed = 210+130+70+35-70+70 = 445.00 (44500 cents). Adjustment = 45.00. Balance = 445.00 - 0.00 - 45.00 = 400.00 (40000). Code output matches on all three, and on every running-balance step.\n- Red-flag greps on `billing.py` and `test_billing.py`: no `except` (count 0), no `float(`/`round(`, no multiplication of a rate by a count, no `sleep`, `retry` or network call. `test_billing.py:330` checks that `app.llm` is absent from the source text (a string check, not an import check).\n- Route read: `billing.py:634-641`; `grep -c verify_citations app/backend/api.py` returns 0.\n- Not exercised: a live server (no app URL), the evals/sample case (`evals/golden/sample.txt`), the frontend. The billing route is exercised only through the TestClient test.\n\n## Findings\n\n**F1 blocker. The card's code and route are absent from HEAD.** T-084's commit ec33bf0 deletes `app/backend/billing.py` (642 lines) and `tests/unit/test_billing.py` (330 lines), and replaces the billing hook in `app/backend/api.py` with the reclassify hook. Both commits are one second apart (22:25:02 and 22:25:03), which is consistent with a shared-index race. I did not verify the cause. At HEAD 02ff244 (checked after HEAD moved), `git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py` prints nothing and `grep -c billing` on `HEAD:app/backend/api.py` gives 0. The only copies are untracked working-tree files. Card T-083 cites commit f218263, which no longer reaches the branch's content.\n\n**F2 blocker. Per-visit rate rows in an itemized table are totaled as charges; a rate with `$` is also listed as an excluded rate.** Probe on the pinned copy, table with a CHARGES column and the row `06/10/26  06/11/26  99213  Charge per visit  185.00  185.00`: line 99213 has kind `charge` and billed 18500; `totals.billed` = $315.00 (31500); `excluded` = []. Same row with `$185.00`: billed 31500 and `excluded` lists `(18500, rate)` twice. The code path: `billing.py:465-468` appends table lines with no rate check; `billing.py:489` only classifies figures returned by `find_amounts`, and `amounts.py:33` says it finds only `$` figures. RULES line 30 says a per-visit rate is never a charge, and research section 1.2 agrees. This is the persona's red flag (\"a total that includes the $185 rate\").\n\n**F3 blocker. Service lines that do not match a strict pattern are dropped silently; the output still says complete.**\n- CMS-1500, printed decimal in 24F, no Item 28 line: lines `060126 060126 11 98941 AB 85.00 1`, `060226 060226 11 98941 AB 85 | 00 1`, `060326 060326 11 97014 A 90 | 00 3`. Output: billed 17500 (expected 26000), 2 lines, `complete` True, `checks` [], `status` analyzed. Cause: `billing.py:242` (`_AMT` accepts no `.`), and `billing.py:282-288` lets a non-matching line fall through with no record of it. The same happens with slash dates (`06/01/26`).\n- Ledger table, row with no date (`97014 E-stim unattended 35.00 165.00` under a DOS-less line): billed 20000, `complete` True. The stated total flags only an aggregate (`LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`) that does not name the row. Cause: `billing.py:148-150` (`if not m: continue`).\n- Under D.2, \"loses facts\" is a blocker. D-027 (\"text outside recognised blocks is never dropped\") is the same principle.\n\n**F4 major. No test pins the prose rate guard; a mutant that lets a rate become a charge passes all 27 tests.** Mutant M3 changes `billing.py:228` from `== \"charge\"` to `!= \"estimate\"`. `mutants.log`: `M3_prose_rate_gate_open: 27 passed`. Probe sentence: `Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.` Mutant: billed 43500 with a line for the $185 rate, `checks` []. Pinned f218263: billed 25000, `checks` [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH]. The stated total was written to include the rate, so the mutant passes every check. `grep -n -F \"per visit\" tests/unit/test_billing.py` finds nothing; the only rate wording is the table's `Fee schedule ... per unit` at line 24, which runs through the table path.\n\n**F5 major. The grounding verifier cannot fail on real output, and the route never calls it.**\n- `billing.py:612` says \"Run in tests and by the API before a response leaves: a line that fails is dropped from the response\". The route (`billing.py:634-641`) calls only `get_case` and `for_case`. `grep -c verify_citations app/backend/api.py` gives 0. The docstring is false.\n- `billing.py:613` builds the reference as `text + \"\\n\" + excerpt`, so any cite that is a substring of its own excerpt passes. The fail-closed check at `billing.py:485-487` cannot fire: every line excerpt is sliced from `body`, and `text` contains `body`.\n- Mutants: M7 (fail-closed block disabled) `27 passed`; M8 (reference = record text only) `27 passed`; M9 (verifier returns []) fails one test. The verifier is only caught when it is stubbed to return [], not when its reference is weakened.\n- `verify_citations` also does not cover `payer_reports[].lines[].excerpt`, `line_flags[].excerpt`, `checks[].cites`, or the `stated_totals[].cite` fields.\n- The verbatim property holds today (independent check, zero violations), but nothing enforces it.\n\n**F6 major. The grand total treats an unreadable provider as $0.00.** `billing.py:603-605` uses `sum(p[\"billed\"][\"cents\"] or 0 ...)`. Probe: a provider whose only line has an unreadable figure gives `providers[0].billed` = None and `totals.billed` = `{\"cents\": 0, \"usd\": \"$0.00\"}`, status `partial_unclear`. A default value is shown as a total; the spec says unreadable figures are kept out of totals, not reported as zero.\n\n**F7 minor. A blank DOS cell takes the POSTED date as date of service.** Probe: row `          06/11/26  97014  E-stim unattended  35.00  165.00` gives `dos` = `06/11/26`, `posted` = None. `billing.py:148-157` treats the first date in the row as DOS. Research section 1.1 names the posting-versus-service trap. No totals change, but EOB matching (`billing.py:576-577`) can pair on the wrong date.\n\n**F8 minor. A billing record that matches no form is absent, with no notice.** Probe with the research section 16 ambulance invoice (no `$` sign, no balance column): `status` none_found, `providers` [], `skipped_records` []. `form_of` (`billing.py:93-108`) returns None and `analyze` has no branch for it (`billing.py:465-483`). The case reports \"none found\" for a case with a bill. Ambulance invoices are outside the card's named forms, so this is minor.\n\n**F9 minor. A rate in an unnamed RATE column is listed as unclear, not as an excluded rate.** Probe: header `UNITS  RATE  CHARGES`, row `2  65.00  130.00`. Output: billed 13000 (correct), line `unclear` ['65.00'], `complete` False, `excluded` []. `billing.py:46-47` (`_COLS`) has no RATE entry. Not totaled, so this is conservative, but the rate is not shown under \"Rates and excluded\".\n\n**What is right (not to break):**\n- Money is integer cents throughout; no floats; no rate is multiplied by a count; the Larkspur ledger hand recompute matches (44500 / 4500 / 40000).\n- UB-04: the FL 44 rate is excluded, the 0001 total is compared and not added (9,165.75); mutants M1, M4 and M6 each fail the UB-04 test.\n- CMS-1500 implied cents: `85 | 00`, `85 00` and `8500` read as $85.00; OCR letters (`45 OO`) are listed unclear, not guessed; mutant M5 fails the OCR test.\n\n## Mutation results (scratch copies of f218263, `mutants.log`)\n\n| Mutant | Change | Result |\n|---|---|---|\n| M1 | UB-04 rate branch disabled (`billing.py:325`) | fails 1 (UB-04 test) |\n| M2 | ledger rate exclusion disabled (`billing.py:490`) | fails 1 (fee-schedule test) |\n| M3 | prose rate gate opened (`billing.py:228`) | **passes 27 (F4)** |\n| M4 | UB-04 rates not listed (`billing.py:480`) | fails 1 |\n| M5 | CMS-1500 raw digits not implied cents (`billing.py:262`) | fails 1 (OCR test) |\n| M6 | UB-04 rate header not found (`billing.py:302`) | fails 1 |\n| M7 | fail-closed block disabled (`billing.py:485`) | **passes 27 (F5)** |\n| M8 | verifier reference = record text only (`billing.py:613`) | **passes 27 (F5)** |\n| M9 | verifier returns [] (`billing.py:613`) | fails 1 |\n\n## Process\n\n- Verdict by the D.2 rule: blocker present, so fail. The first-round count of blockers does not change if F1 is resolved by restoring the files, because F2 and F3 are independent.\n- No finding rests on a claim I did not run. Where a claim depends on HEAD, the commands and outputs are in `artifacts/review-evidence/T-083-r1/head_state.txt`.\n\n```json\n{\"card\": \"T-083\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit f218263 (app/backend/billing.py, app/backend/api.py +2 lines, tests/unit/test_billing.py, memory/contracts/api.md +37), pinned by git archive to the session scratchpad (pin-f218263); HEAD checked at 02ff244; no app URL exercised (route exercised via TestClient in tests/unit/test_billing.py); sample case: synthetic fixtures LEDGER, EOB, CMS_CLEAN, CMS_OCR, UB_ROOM, PROSE, LOP from tests/unit/test_billing.py\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, board/cards/T-083.md, memory/ORCHESTRATOR_DECISIONS.md D-019 and D-042, research/record-formats.md sections 1.1, 1.2, 8, 9, 16 and line 489, app/backend/billing.py (full), tests/unit/test_billing.py (full), app/backend/amounts.py find_amounts and classify\",\n  \".venv/bin/python -m pytest -q tests/unit/test_billing.py: 27 passed (working tree), 27 passed (pinned f218263 copy), 27 passed (second run)\",\n  \"git archive f218263 to scratchpad pin-f218263; git show f218263:app/backend/billing.py | diff -q against working tree: identical; test file identical\",\n  \"git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py: empty at 02ff244; git show --stat ec33bf0 shows billing.py 642 deletions and test_billing.py 330 deletions; git show HEAD:app/backend/api.py | grep -c billing: 0 (artifacts/review-evidence/T-083-r1/head_state.txt)\",\n  \"mutation runner artifacts/review-evidence/T-083-r1/run_mutants.py on scratch copies, log artifacts/review-evidence/T-083-r1/mutants.log: M1-M9 results\",\n  \"probes against pinned copy: prose rate sentences; table rows with per-visit wording with and without $; unnamed RATE column; RATE column without charge; ambulance invoice specimen; CMS-1500 printed decimal, slash dates, missing Item 28; box_amount values; ledger rows with blank DOS and no date\",\n  \"independent verbatim check of every excerpt, cite, cites[] and figure text in five output shapes against record text: 0 violations (31 excerpts, 15 cites, 14 line figures)\",\n  \"hand recompute of the Larkspur ledger: billed 445.00, adjustment 45.00, balance 400.00 = 445.00 - 0.00 - 45.00; matches code output and running-balance steps\",\n  \"grep for except, float(, round(, sleep, retry, network calls in billing.py and test_billing.py: none; grep -n -F per visit in test_billing.py: no match; grep -c verify_citations app/backend/api.py: 0; route read at billing.py:634-641\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"delivered_on_branch\": 1, \"integer_cents_no_llm\": 5, \"rate_guard\": 2, \"grounding_verifier\": 2, \"honest_failure_visible\": 2, \"test_quality\": 3, \"determinism_and_reproducibility\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Card code and route absent from HEAD: T-084 commit ec33bf0 deletes billing.py, test_billing.py and the billing hook\",\n   \"evidence\": \"artifacts/review-evidence/T-083-r1/head_state.txt | git show --stat ec33bf0: 'app/backend/billing.py | 642 ----', 'tests/unit/test_billing.py | 330 ----'; git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py prints nothing at 02ff244; git show HEAD:app/backend/api.py | grep -c billing prints 0; git status shows '?? app/backend/billing.py' and '?? tests/unit/test_billing.py'\",\n   \"why_it_matters\": \"The D-042 billing route GET /api/cases/{token}/billing is not served by any committed code and its tests exist only as untracked files. Card T-083 cites f218263, which no longer reaches the branch. Rated blocker under D.2 (must-have unusable). Commits ec33bf0 and f218263 are one second apart, consistent with a shared-index race; cause not verified.\",\n   \"fix\": \"Backend or orchestrator: restore app/backend/billing.py and tests/unit/test_billing.py from f218263 and re-add the billing.add_routes call beside reclassify.add_routes in app/backend/api.py, so both routes are wired. Commit with explicit git add paths. Do not revert T-084.\",\n   \"acceptance_test\": \"git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py lists both paths; .venv/bin/python -m pytest -q tests/unit/test_billing.py passes at HEAD; test_billing_route_for_a_pasted_case passes; the reclassify route still resolves\"},\n  {\"severity\": \"blocker\", \"title\": \"Per-visit rate rows in an itemized table are totaled as charges; a rate with $ is also listed as an excluded rate\",\n   \"evidence\": \"Probe on pinned f218263. Table row '06/10/26  06/11/26  99213  Charge per visit  185.00  185.00' (CHARGES column): line 99213 kind=charge billed=18500, totals.billed=31500, excluded=[]. Same row with '$185.00': billed 31500 and excluded=[(18500,rate),(18500,rate)]. billing.py:465-468 appends table lines with no rate check; billing.py:489 classifies only find_amounts results; app/backend/amounts.py:33 says find_amounts finds only '$' figures.\",\n   \"why_it_matters\": \"billing.py:30 (RULES) says a per-visit rate is never a charge; D-042 and research/record-formats.md section 1.2 agree. The $185 per-visit price enters the billed total: the persona red flag 'a total that includes the $185 rate'. The $-form lists the same figure as both a charge and a rate, so the output contradicts itself. A stated total that includes the rate hides the error from the total check.\",\n   \"fix\": \"Apply A.classify to each table figure with its row label (the rule the prose path already uses at billing.py:228) before assigning to billed. A rate-classified figure goes to excluded only, never to billed. Run the exclusion over every money figure in table rows, not only '$' figures, and never list one figure as both charge and rate.\",\n   \"acceptance_test\": \"New tests in tests/unit/test_billing.py: (a) table row 'Charge per visit 185.00' in the CHARGES column gives billed excluding 18500 and excluded listing it exactly once; (b) the same row with '$185.00' gives the same result; (c) a statement whose stated total excludes the rate gives checks == []. Mutant: remove the new guard, and the test fails.\"},\n  {\"severity\": \"blocker\", \"title\": \"Unmatched service lines are dropped silently: complete=true, no unclear entry, no check when no stated total exists\",\n   \"evidence\": \"Probe on pinned f218263: CMS-1500 with lines '060126 060126 11 98941 AB 85.00 1 SYN-NPI-0001' (printed decimal), '060226 060226 11 98941 AB 85 | 00 1', '060326 060326 11 97014 A 90 | 00 3', no Item 28: billed 17500 (expected 26000), lines 2, complete True, checks [], status analyzed. Slash dates '06/01/26' also dropped. Ledger row with no date: billed 20000, complete True, checks [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH] (aggregate only). Causes: billing.py:242 (_AMT accepts no '.'); billing.py:282-288 non-matching lines fall through with no record; billing.py:148-150 ('if not m: continue').\",\n   \"why_it_matters\": \"A billed fact disappears while the provider reports complete. D.2 'loses facts' is a blocker. D-027 ('text outside recognised blocks is never dropped') is the same principle. When the aggregate mismatch does fire, it does not say which row was lost.\",\n   \"fix\": \"Any CMS-1500 or ledger-table line that is not parsed but carries a money figure or a date-like token is emitted as a line with unclear=[figure text], LINE_UNCLEAR, and complete=false. Either parse a printed decimal in 24F as a stated amount or list it unclear; the silent drop is the defect. Add an unparsed-line count to each provider.\",\n   \"acceptance_test\": \"Tests: the CMS fixture with a '85.00' line and no Item 28 gives an unclear line with its excerpt, complete False, and billed excluding it; a ledger row with no date is listed unclear and complete False; a slash-dated CMS line is listed, not dropped.\"},\n  {\"severity\": \"major\", \"title\": \"No test pins the prose rate guard; mutant M3 passes all 27 tests and lets a $185 rate become a charge\",\n   \"evidence\": \"mutants.log: 'M3_prose_rate_gate_open: 27 passed'. Mutant changes billing.py:228 '== \\\"charge\\\"' to '!= \\\"estimate\\\"'. Sentence: 'Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.' Mutant: billed 43500 with a line for the $185 rate, checks []. Pinned f218263: billed 25000, checks [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH]. grep -n -F 'per visit' tests/unit/test_billing.py: no match; the only rate wording is 'per unit' at line 24, which runs through the table path.\",\n   \"why_it_matters\": \"The prose-path rate guard is the only thing keeping a rate out of totals on prose ledgers. The stated-total check hides the error when the statement's own total was computed the same way. The brief asks that the rate guard be proven by tests, and this one is not.\",\n   \"fix\": \"Add a prose-ledger test with 'Charge per visit $185.00' and a stated total that excludes it; assert the rate is excluded once and checks == [].\",\n   \"acceptance_test\": \"The new prose test passes on f218263 and fails on mutant M3 (billed becomes 43500).\"},\n  {\"severity\": \"major\", \"title\": \"The grounding verifier cannot fail on real output and the route never calls it\",\n   \"evidence\": \"billing.py:612 docstring: 'Run in tests and by the API before a response leaves: a line that fails is dropped'. billing.py:634-641 route calls only get_case and for_case; grep -c verify_citations app/backend/api.py: 0. billing.py:613 text_of = text + excerpt, so any cite that is a substring of its own excerpt passes. Fail-closed check at billing.py:485-487 cannot fire (excerpts are slices of body; text contains body). Mutants: M7 (fail-closed off) 27 passed; M8 (reference = record text only) 27 passed; M9 (verifier returns []) 1 failed.\",\n   \"why_it_matters\": \"Persona checklist items 4 and 13: the verifier must check each excerpt against its own record and fail visibly. Here the docstring claims an API gate that does not exist, and the in-analysis guard is unreachable. The verbatim property holds today (independent check: 0 violations), but nothing enforces it. verify_citations also skips payer_reports excerpts, line_flags excerpts, checks[].cites and stated_totals cite fields.\",\n   \"fix\": \"Call verify_citations in billing_get and return a visible citation_failures list when it is non-empty. Build the reference from the record text only, normalised as documented. Extend the check to every cite-bearing field. Delete the dead fail-closed block or turn it into a checked assertion.\",\n   \"acceptance_test\": \"A record with text 'A' and excerpt 'B $10.00' makes verify_citations non-empty; mutant M8 and M7 each fail a test; a route test with a patched non-verbatim cite shows a citation_failures entry.\"},\n  {\"severity\": \"major\", \"title\": \"Grand total treats an unreadable provider as $0.00\",\n   \"evidence\": \"billing.py:603-605: sum(p['billed']['cents'] or 0 for p in providers). Probe: RATE column row with no charge gives providers[0].billed None and totals.billed {'cents': 0, 'usd': '$0.00'} with status partial_unclear.\",\n   \"why_it_matters\": \"A default value is shown as a total. The spec says unreadable figures are kept out of totals, not reported as zero. A paralegal who reads 'Billed $0.00' is misled.\",\n   \"fix\": \"Set totals.billed.cents to None when any provider's billed is None, or add totals.complete=false and totals.unreadable_providers.\",\n   \"acceptance_test\": \"The probe fixture gives totals.billed.cents None (or totals.complete False); a test in tests/unit/test_billing.py asserts it.\"},\n  {\"severity\": \"minor\", \"title\": \"A blank DOS cell takes the POSTED date as the date of service\",\n   \"evidence\": \"Probe: row '          06/11/26  97014  E-stim unattended  35.00  165.00' gives dos '06/11/26', posted None. billing.py:148-157 treats the first date in the row as DOS.\",\n   \"why_it_matters\": \"A service date is attributed to a row whose DOS cell is blank (research/record-formats.md section 1.1 posting-versus-service trap). No totals change, but EOB matching at billing.py:576-577 can pair on the wrong date.\",\n   \"fix\": \"Assign dates by column position when the header has separate DOS and POSTED columns; flag a row with an empty DOS cell as NO_DATE_OF_SERVICE.\",\n   \"acceptance_test\": \"A blank-DOS row gives dos None, posted kept, and the flag.\"},\n  {\"severity\": \"minor\", \"title\": \"A billing record that matches no form is absent with no notice\",\n   \"evidence\": \"Probe with the research/record-formats.md section 16 ambulance invoice (no $ sign, no balance column): status none_found, providers [], skipped_records []. form_of at billing.py:93-108 returns None; analyze has no branch for it (billing.py:465-483).\",\n   \"why_it_matters\": \"A case with a bill reports 'none found'. Ambulance invoices are outside the card's named forms, so this is minor; D-027's principle applies.\",\n   \"fix\": \"Record form None on a billing-looking source or with money figures as skipped_records with reason_code UNRECOGNISED_BILLING_FORM, shown to the paralegal.\",\n   \"acceptance_test\": \"The ambulance specimen appears in skipped_records and status is not none_found.\"},\n  {\"severity\": \"minor\", \"title\": \"A rate in an unnamed RATE column is listed as unclear, not as an excluded rate\",\n   \"evidence\": \"Probe: header 'UNITS  RATE  CHARGES' and row '2  65.00  130.00': billed 13000 (correct), line unclear ['65.00'], complete False, excluded []. billing.py:46-47 (_COLS) has no RATE entry.\",\n   \"why_it_matters\": \"The rate is not totaled, which is conservative. But it is not shown under 'Rates and excluded', and the provider is marked incomplete for a figure its own column calls a rate.\",\n   \"fix\": \"Add a RATE column kind to _COLS and route its figures to excluded with kind 'rate'.\",\n   \"acceptance_test\": \"A RATE-column table gives excluded containing 6500 with kind rate, and complete True.\"}\n ],\n \"whats_right\": [\n  \"Money is integer cents with no floats or rate-times-count arithmetic; the Larkspur ledger hand recompute matches the code (44500 billed, 4500 adjustment, 40000 balance = 44500 - 0 - 4500).\",\n  \"UB-04: the FL 44 rate is excluded, the 0001 total is compared and not added (916575 cents); mutants M1, M4 and M6 each fail the UB-04 test.\",\n  \"CMS-1500 implied cents: '85 | 00', '85 00' and '8500' read as $85.00; OCR letters ('45 OO') are listed unclear, not guessed; mutant M5 fails the OCR test.\"\n ],\n \"questions_for_chris\": [\n  \"Was the deletion of app/backend/billing.py and tests/unit/test_billing.py in T-084 commit ec33bf0 intended? If intended, T-083 should be cancelled, not reviewed as done.\",\n  \"A dated ledger row whose description says 'per visit' but whose amount sits in the CHARGES column: my reading of D-042 and RULES line 30 is that it is a rate and must not be totaled. Confirm, or tell me the judge re-check path you intend for it.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T04:33:26.913Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-083-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:30.024Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport re, json\nt = open('reviews/T-083-staff-engineer.md', encoding='utf-8').read()\nblocks = re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd = json.loads(blocks[0])\nprint('card', d['card'], 'persona', d['persona'], 'model', d['model'], 'verdict', d['verdict'])\nsev = [f['severity'] for f in d['findings']]\nprint('severities', sev)\nexp = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('verdict rule ok:', exp == d['verdict'])\nprint('whats_right', len(d['whats_right']), 'questions', len(d['questions_for_chris']))\n\"",
 "description": "Validate review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T04:33:30.081Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:33.365Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/validate_t083.py",
 "content": "import json\nimport re\nimport sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"severities\", sev)\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule ok:\", expected == d[\"verdict\"], \"expected\", expected)\nprint(\"whats_right\", len(d[\"whats_right\"]), \"questions\", len(d[\"questions_for_chris\"]))\n"
}
````

### User / tool · 2026-11-02T04:33:33.415Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/validate_t083.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:36.135Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/validate_review_json.py",
 "content": "import json\nimport re\nimport sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"severities\", sev)\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule ok:\", expected == d[\"verdict\"], \"expected\", expected)\nprint(\"whats_right\", len(d[\"whats_right\"]), \"questions\", len(d[\"questions_for_chris\"]))\n"
}
````

### User / tool · 2026-11-02T04:33:36.236Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/validate_review_json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:37.827Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I artifacts/review-evidence/T-083-r1/validate_review_json.py /Users/arsis/zlayt-pm-project/reviews/T-083-staff-engineer.md",
 "description": "Validate review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T04:33:37.937Z

**tool result**
````
json blocks: 1
card T-083 | persona staff-engineer-reviewer | model claude-haiku-5-5 | verdict fail
severities ['blocker', 'blocker', 'blocker', 'major', 'major', 'major', 'minor', 'minor', 'minor']
verdict rule ok: True expected fail
whats_right 3 questions 2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:52.910Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.py",
 "content": "\"\"\"Independent verbatim check for T-083 (staff-engineer-reviewer, r1).\n\nRun from the pinned f218263 tree (git archive) with PYTHONPATH pointing at it:\n  PYTHONPATH=<pin>:<pin>/tests/unit <venv python> -I this_file.py\nEvery excerpt, cite, cites[] item and figure text in the billing output must be a substring of its record's own text.\nThis does not use billing.verify_citations.\n\"\"\"\nimport test_billing as T\nfrom app.backend.billing import analyze\n\nSETS = {\n    \"ledger+eob\": [T.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", T.LEDGER),\n                   T.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", T.EOB)],\n    \"cms_clean\": [T.rec(1, \"Brightwater Spine & Wellness, CMS-1500\", T.CMS_CLEAN)],\n    \"cms_ocr\": [T.rec(1, \"Brightwater Spine & Wellness, CMS-1500 (OCR)\", T.CMS_OCR)],\n    \"ub04\": [T.rec(1, \"Saltmarrow General Hospital, UB-04\", T.UB_ROOM)],\n    \"prose+lop\": [T.rec(1, \"Fennimoor Spine Clinic, itemized ledger\", T.PROSE),\n                  T.rec(2, \"Pellingham and Rook PLLC, correspondence (letter of protection)\", T.LOP)],\n}\n\nTOTAL = {\"excerpt\": 0, \"cite\": 0, \"cites_item\": 0, \"figure_key\": 0, \"line_figure\": 0}\nBAD = []\n\n\ndef check_text(rec_text, rn, s, where):\n    if s not in rec_text.get(rn, \"\"):\n        BAD.append((where, s[:70]))\n\n\ndef walk(o, rec_text, path, counts):\n    if isinstance(o, dict):\n        rn = o.get(\"record_no\")\n        for k, v in o.items():\n            if k == \"excerpt\" and isinstance(v, str) and rn is not None:\n                counts[\"excerpt\"] += 1\n                check_text(rec_text, rn, v, path + \".excerpt\")\n            if k == \"cite\" and isinstance(v, dict):\n                counts[\"cite\"] += 1\n                check_text(rec_text, v[\"record_no\"], v[\"excerpt\"], path + \".cite\")\n            if k == \"cites\" and isinstance(v, list):\n                for c in v:\n                    counts[\"cites_item\"] += 1\n                    check_text(rec_text, c[\"record_no\"], c[\"excerpt\"], path + \".cites\")\n            if k == \"figure\" and isinstance(v, dict) and rn is not None:\n                counts[\"figure_key\"] += 1\n                t = v[\"text\"].lstrip(\"-\")\n                if t not in rec_text.get(rn, \"\") and v[\"text\"] not in rec_text.get(rn, \"\"):\n                    BAD.append((path + \".figure\", v[\"text\"]))\n            walk(v, rec_text, path + \".\" + k, counts)\n    elif isinstance(o, list):\n        for i, v in enumerate(o):\n            walk(v, rec_text, f\"{path}[{i}]\", counts)\n\n\nfor name, recs in SETS.items():\n    out = analyze(recs)\n    rec_text = {r[\"n\"]: r[\"text\"] for r in recs}\n    counts = {\"excerpt\": 0, \"cite\": 0, \"cites_item\": 0, \"figure_key\": 0, \"line_figure\": 0}\n    walk(out, rec_text, name, counts)\n    for p in out[\"providers\"]:\n        for l in p[\"lines\"]:\n            for k in (\"billed\", \"adjustment\", \"paid\", \"balance\"):\n                f = l.get(k)\n                if f:\n                    counts[\"line_figure\"] += 1\n                    t = f[\"text\"].lstrip(\"-\")\n                    if t not in l[\"excerpt\"] and f[\"text\"] not in l[\"excerpt\"]:\n                        BAD.append((name + \".line_figure.\" + k, f[\"text\"]))\n    for k, v in counts.items():\n        TOTAL[k] += v\n    print(name, \"status\", out[\"status\"], counts)\n\nprint(\"TOTAL\", TOTAL)\nprint(\"verbatim violations:\", len(BAD), BAD[:5])\n"
}
````

### User / tool · 2026-11-02T04:33:53.013Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:55.790Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD:$PWD/tests/unit\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.log 2>&1; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.log",
 "description": "Run verbatim check script on pinned tree and save log"
}
````

### User / tool · 2026-11-02T04:33:55.909Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.py", line 8, in <module>
    import test_billing as T
ModuleNotFoundError: No module named 'test_billing'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:59.327Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/pin-f218263\" && PYTHONPATH=\"$PWD:$PWD/tests/unit\" /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.log 2>&1; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/verbatim_check.log",
 "description": "Run verbatim check script on pinned tree and save log"
}
````

### User / tool · 2026-11-02T04:33:59.843Z

**tool result**
````
ledger+eob status analyzed {'excerpt': 31, 'cite': 5, 'cites_item': 15, 'figure_key': 1, 'line_figure': 14}
cms_clean status analyzed {'excerpt': 12, 'cite': 2, 'cites_item': 5, 'figure_key': 0, 'line_figure': 5}
cms_ocr status partial_unclear {'excerpt': 14, 'cite': 4, 'cites_item': 5, 'figure_key': 0, 'line_figure': 4}
ub04 status analyzed {'excerpt': 12, 'cite': 1, 'cites_item': 5, 'figure_key': 1, 'line_figure': 5}
prose+lop status analyzed {'excerpt': 15, 'cite': 3, 'cites_item': 5, 'figure_key': 2, 'line_figure': 5}
TOTAL {'excerpt': 84, 'cite': 15, 'cites_item': 35, 'figure_key': 4, 'line_figure': 33}
verbatim violations: 0 []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:05.018Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/count_correction.txt",
 "content": "Correction to reviews/T-083-staff-engineer.md (written after the review file was created; the review file is append-only).\n\nThe review says the independent verbatim check covered \"31 excerpts, 15 cites and 14 line figures\". Those numbers are the ledger+EOB set only.\nThe canonical count across all five output shapes, from verbatim_check.py / verbatim_check.log, is:\n  excerpt keys 84; cite objects 15; cites[] items 35; figure keys 4; line figures 33; verbatim violations 0.\nThe conclusion (0 violations) is unchanged. Sources: verbatim_check.log in this directory.\n"
}
````

### User / tool · 2026-11-02T04:34:05.119Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-083-r1/count_correction.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:10.015Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && grep -n -i \"scratch\\|git-guard\\|board-guard\\|reviewer-write\" *.md | cut -c1-220 | head -20",
 "description": "Check existing memory for scratch-path and guard gotchas"
}
````

### User / tool · 2026-11-02T04:34:10.107Z

**tool result**
````
feedback_review_write_once.md:3:description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
feedback_review_write_once.md:8:Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("re
MEMORY.md:1:- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
MEMORY.md:3:- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
MEMORY.md:6:- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
MEMORY.md:22:- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad: J3 relabel after failure, controls gate without ADR, keyword-separable controls, scratch-mutant guard tr
project_backend_llm_review_patterns.md:3:description: T-035 r1 and T-033 r2 recurring findings - untested wiring, judge reason prose, label-window bleed in amount classification, scratch-copy controls
project_backend_llm_review_patterns.md:8:T-035 r1 (a2fc95a): pure-module tests (grounding, judges) pass while the stage module (generator.py) that wires them has none; mutate the call site in a scratch copy (cp -R app te
project_backend_llm_review_patterns.md:9:**Why:** card ACs cite "scratch run" evidence and tests that depend on pipeline stubs (T-037), so nothing in the repo proves the wiring.
project_backend_llm_review_patterns.md:17:Also: a scratch copy must include memory/ (tests read memory/contracts/*.md) or the full-suite control is invalid; cp -R of the tree minus .venv worked, an rsync-based copy was d
project_backend_llm_review_patterns.md:18:T-035 r2: backend fixed both blockers well (9/9 scratch mutations killed); remaining = eval report/AC6 waiting on T-038/T-037.
project_backend_llm_review_patterns.md:19:T-038 (eval runner): gate code had `except Exception` fallbacks, ship_bar ignored runs>=3, --check-spec left stale ship_bar_met, tests assert only "ship_bar_met False" (mutate ea
project_db_review_patterns.md:3:description: T-031 (app/db) round-1/round-2 review patterns - partial re-fixes, regex guard blind spots, scratch-copy mutation method, hook gotchas for reviewers
project_db_review_patterns.md:11:- **Source-regex guard tests have blind spots.** test_review_status_only_via_apply_review matches `review_status=?`, `SET review_status`, `review_status='...'`. It misses a multi-column `
project_db_review_patterns.md:13:- **Mutation method that works:** copy app/ and tests/ to the scratchpad, `sed -i.bak` one guard, run `pytest tests/unit/test_db.py -q`, restore from .bak. Do not touch repo files.
project_db_review_patterns.md:16:- The Bash git-guard hook denies commands containing backticks inside a `python -c "..."` string ("could not parse command safely"). Put scripts in a file and run the file.
project_db_review_patterns.md:17:- reviewer-write-guard blocks Write to the scratchpad. Scripts and probes must go under artifacts/review-evidence/.
project_e2e_contract_review_patterns.md:21:Environment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard "could not pars
project_eval_runner_review_patterns.md:3:description: T-038 r1-r2 eval runner (evals/run.py) review patterns: test doubles hiding real key shapes, bar-level mutation coverage, scratch-copy mutation method for eval tests
project_eval_runner_review_patterns.md:17:- **Method (scratch copy):** copy `app/ evals/ tests/ spec/ docs/ memory/` into the scratchpad (not `.env`; `memory/contracts/api.md` is read by tests, so `memory/` must be inclu
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:19.317Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t083_billing_review_patterns.md",
 "content": "---\nname: t083-billing-review-patterns\ndescription: T-083 r1 (f218263) billing analysis - card files deleted from HEAD by a sibling commit, per-visit rate rows totaled in tables, silent line drops, tautological verbatim verifier, $0.00 grand total\nmetadata:\n  type: project\n---\n\nT-083 r1 (billing on itemized ledgers, code only, f218263). Verdict fail: 3 blockers, 3 majors, 3 minors. Review at reviews/T-083-staff-engineer.md.\n\n- **Check the card's files at HEAD first.** `git ls-tree --name-only HEAD <card files>` came back empty: T-084 commit ec33bf0 (one second after f218263) deleted billing.py, test_billing.py and the billing hook in api.py. Same shared-index pattern as [[project_r2_fix_verification_patterns]]. Pin with `git archive <card commit>` and diff the working tree against the blob.\n- **Rate guards are keyed to `$` figures.** `amounts.find_amounts` finds only `$` figures, so a ledger table row whose CHARGES column holds `185.00` under the description \"Charge per visit\" is totaled with no rate check, and with a `$` it is listed as a rate AND totaled. Probe table rows with and without `$`. Prose rate gates (`classify == \"charge\"`) had no test: mutant `!= \"estimate\"` passed 27/27.\n- **A \"verbatim\" verifier whose reference includes the excerpt cannot fail.** `text + excerpt` as reference; the route never called it although the docstring said the API did; the fail-closed block was unreachable. Mutants that weaken the reference (M8) or disable the block (M7) pass. Only a stubbed-to-[] verifier fails a test. Check the reference set, the route call site, and every cite-bearing field.\n- **Silent drops in parsers.** `if not m: continue` on table rows and a regex that accepts no `.` in 24F let a billed line vanish while `complete` stays True. With no stated total there is no aggregate check either. Probe each regex with a printed decimal, slash dates, and a missing date.\n- **`or 0` in a grand total** shows $0.00 when a provider's billed is unreadable (None).\n- **Count claims in the review must come from a saved script log, not memory.** I first wrote \"31 excerpts, 15 cites, 14 line figures\" from one fixture subset; the canonical log says 84 / 15 / 35 / 4 / 33. Put the counting script in artifacts/review-evidence and cite its log. Review files are write-once, so the correction went to artifacts/review-evidence/T-083-r1/count_correction.txt.\n\n**Why:** the code was clean on the things a fixture tests (integer cents, verbatim substrings, UB-04 rate, CMS implied cents), and the holes were in what the fixtures never contain (table rates, unmatched rows, prose rates, a non-empty verifier reference).\n\n**How to apply:** on any extraction or totals card, probe the input shapes the tests do not contain (table rows, unlabeled figures, missing dates, printed decimals) and check `complete`/status after each. Mutate the rate or citation branch in the caller, not only the helper.\n\nModel note for this card: dispatched as claude-haiku-5-5 although CLAUDE.md section 6 and D-024 call for Sonnet on engineering reviewers. Flagged in the review's first paragraph. See [[feedback_severity_vs_brief]] for rating a brief's default down or up per D.2.\n"
}
````

### User / tool · 2026-11-02T04:34:19.417Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t083_billing_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:21.327Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad: J3 relabel after failure, controls gate without ADR, keyword-separable controls, scratch-mutant guard traps",
 "new_string": "- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad: J3 relabel after failure, controls gate without ADR, keyword-separable controls, scratch-mutant guard traps\n- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263: card files deleted at HEAD by sibling commit, table rate rows totaled, silent line drops, tautological verifier, $0.00 total"
}
````

### User / tool · 2026-11-02T04:34:21.423Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:24.031Z

T-083 verdict fail: three blockers (card files gone from HEAD after ec33bf0, per-visit rate rows totaled, unmatched CMS-1500/ledger rows dropped silently), three majors, three minors. Review: /Users/arsis/zlayt-pm-project/reviews/T-083-staff-engineer.md
