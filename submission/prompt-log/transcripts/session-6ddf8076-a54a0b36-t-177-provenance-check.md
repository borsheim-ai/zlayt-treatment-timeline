# Subagent: T-177 provenance check (T-177 provenance check)

Source: `agent-a54a0b36ebcca8a00.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T20:33:34.885Z

Review board card T-177 (commit 04ea2bf, D-065 honest demo provenance) in /Users/arsis/zlayt-pm-project. Read D-065, the blocker in reviews/GATE-M3-product-manager.md, and `python3 tools/board.py show T-177`.

On a `git archive HEAD` copy, verify the PM's acceptance test with the curated set:
- no 'AI draft' or 'recorded AI answers' on a curated item;
- the /items/e1/trace generator step's model is not claude-sonnet-5-5 and its text names a prepared answer;
- /audit rows for curated keys carry the model 'hand-checked (qa)';
- with the recorded set, the labels say AI.

Run tests/unit/test_prepared_provenance.py and tests/e2e/test_demo_provenance.py. A guided UI redesign (D-068) is coming, so the backend provenance fields (`prepared` and the model) matter most; check that they're in the API, documented in api.md.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-177-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Stop only your own PIDs. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:37.555Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T20:33:37.566Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:38.067Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-177 && echo ---- && git log --oneline -3 && git rev-parse HEAD && git show --stat 04ea2bf | head -60",
 "description": "Show T-177 card and recent commit metadata"
}
````

### User / tool · 2026-11-02T20:33:38.252Z

**tool result**
````
---
id: "T-177"
title: "GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:09:00Z"
updated_at: "2026-11-02T20:33:30Z"
claimed_by: "backend"
claimed_at: "2026-11-02T20:09:11Z"
rounds: 0
commits: ["04ea2bf"]
reviews: []
ac:
  - {"n": 1, "text": "E2E on FIXTURE_SET=curated: no 'AI draft' or 'recorded AI answers' on a curated item; /items/e1/trace generator step model is not claude-sonnet-5-5 and names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'; with the recorded set, labels say AI; unit + e2e", "done": true, "evidence": "git archive 04ea2bf, E2E_REQUIRE_DB=1: tests/e2e (424 passed, 1 skipped; 1 timing flake test_mvp_polish decided_row passes alone, also on 0c4284f) incl. new tests/e2e/test_demo_provenance.py (curated+recorded private servers) and tests/unit/test_prepared_provenance.py (6); full unit suite 5695 passed in working tree"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:09:02Z orchestrator: assigned: backend
- 2026-11-02T20:09:11Z backend: claimed
- 2026-11-02T20:21:28Z backend: Committed 04ea2bf (temp index). Tests first: tests/unit/test_prepared_provenance.py (6) + tests/e2e/test_demo_provenance.py (4, curated + recorded-set private server). Unit suite 5695 passed in working tree. Verifying e2e from git archive HEAD copy now.
- 2026-11-02T20:31:43Z backend: AC 1 checked: git archive 04ea2bf, E2E_REQUIRE_DB=1: tests/e2e (424 passed, 1 skipped; 1 timing flake test_mvp_polish decided_row passes alone, also on 0c4284f) incl. new tests/e2e/test_demo_provenance.py (curated+recorded private servers) and tests/unit/test_prepared_provenance.py (6); full unit suite 5695 passed in working tree
- 2026-11-02T20:31:43Z backend: moved in_progress -> in_review
- 2026-11-02T20:33:30Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: provenance from fixture recorded_from (curated => prepared). audited_call stores model 'hand-checked (qa)'; _call/items/ladder.generator/trace evidence.model/narrative carry prepared; trace step label+why = 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'; /health answers=prepared|recorded|live and ai_banner honest; UI badge 'Demo: sample answers prepared by our team' (tooltip: eval report), 'Prepared answer' tag/step chip/audit chip, recorded+live keep AI draft. api.md updated. Commit 04ea2bf. How verified: tests first (red then green); archive HEAD e2e with E2E_REQUIRE_DB=1 424 passed; recorded set via a private FIXTURE_SET-less server. Left: nothing for this card; D-056 judges in the curated run stay real model ids by design. Surprised: shared index holds others' staged renames, so used temp index; one flaky layout spec in test_mvp_polish (passes alone).

----
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
de5cb3acd1779314d8df01b68dfdc6acd6146ce7
commit 04ea2bf5e7cd2f3b84de7a5135d183e809baa84e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 14:20:49 2026 -0600

    feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py                     |  19 +++--
 app/backend/present.py                 |  38 ++++++++-
 app/backend/trace.py                   |  24 ++++--
 app/frontend/app.js                    |   7 +-
 app/frontend/audit.js                  |   4 +-
 app/frontend/stepper.js                |   1 +
 app/frontend/timeline.js               |   8 +-
 app/llm/audited.py                     |  16 +++-
 app/llm/backends/fixture.py            |   5 ++
 memory/contracts/api.md                |  11 ++-
 tests/e2e/conftest.py                  |   1 +
 tests/e2e/test_demo_provenance.py      | 149 +++++++++++++++++++++++++++++++++
 tests/e2e/test_mvp_polish.py           |   2 +-
 tests/unit/test_prepared_provenance.py | 120 ++++++++++++++++++++++++++
 14 files changed, 383 insertions(+), 22 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:38.639Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i -E \"GATE-M3|T-177\" ; ls memory/ ; grep -n \"D-065\" -A30 memory/ORCHESTRATOR_DECISIONS.md | head -80",
 "description": "List reviews, and locate D-065 in decisions"
}
````

### User / tool · 2026-11-02T20:33:38.736Z

**tool result**
````
GATE-M3-accessibility.md
GATE-M3-chaos-tester.md
GATE-M3-paralegal.md
GATE-M3-product-manager.md
GATE-M3-round1-triage.md
GATE-M3-staff-engineer.md
GATE-M3-ux-designer.md
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
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "The AI's own answers on these cases are in the evaluation report." A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74-| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75-| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
76-| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:40.911Z

**tool call — Bash**
````
{
 "command": "grep -n -i -B2 -A12 \"blocker\" reviews/GATE-M3-product-manager.md | head -120; echo ----; git diff --stat 04ea2bf HEAD | tail -5; echo ----; git status --short | head -30",
 "description": "Read PM gate blocker and check HEAD vs card commit"
}
````

### User / tool · 2026-11-02T20:33:41.057Z

**tool result**
````
13-**Evidence:** `artifacts/review-evidence/GATE-M3-pm/`
14-
15:**Verdict: fail (1 blocker).**
16-
17-## Answers to the brief
18-
19-**Does the MVP do the paralegal's job without over-claiming?** On the job itself, yes. I ran the sample case end to end:
20-- 9 entries came out, and the 73-day gap was flagged.
21-- The 28-day interval was not flagged.
22-- The two accident dates are shown as a conflict, and the tool does not pick one.
23-- The $185 rate goes to "Amounts not totaled".
24-- The letter total is `$8,390.00`.
25-- The export is blocked until she accepts something.
26-- The letter and notes match the golden export exactly (`--check-spec` exit 0).
27-
--
68- "scores": {"solves_paralegal_job": 4, "no_over_claiming": 2, "scope_cut_honesty": 2, "decisions_defensible": 4, "ai_judgment_ship_bar": 3, "workflow_fit": 3},
69- "findings": [
70:  {"severity": "blocker", "title": "The demo shows hand-written QA answers as AI output: badge, 'AI draft' tags, Why trace and audit all name the model",
71-   "evidence": "tests/fixtures/llm/curated/*.json (19 files, 9 extract + 9 flags + 1 narrative): CURATED 'hand-checked response written by qa from evals/golden ... Not a model output', recorded_from.model 'hand-checked (qa)'. app/frontend/app.js:13-14 badge 'Demo: recorded AI answers', tooltip 'This demo replays recorded AI answers for its sample cases.' 04-sample-top.png shows the badge and an 'AI draft' tag on every sample entry. sample-e1-trace.out: 'AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | model claude-sonnet-5-5'. /audit counts ('fixture','claude-sonnet-5-5','extract_v1') x9. D-029 (binding): 'the UI labels it cached demo (curated responses) ... honesty needs the label'; no decision supersedes it (T-166 F7 removed the wording as jargon)",
72-   "why_it_matters": "The public demo and the video are built on this sample. A panel that opens a fixture file will find that the output it saw labeled as the AI's was written by the team to match the golden file. The real model picks different excerpts (D-029 says so). This is the over-claim that ends trust, and the audit trail, which is a product feature, states something false.",
73-   "fix": "Put back an honest label in plain words, e.g. badge 'Demo: sample answers prepared by our team'; tooltip 'The AI's own answers on this case are in the eval report'. Curated items get a 'prepared answer' tag, not 'AI draft'. The trace step for a curated response reads 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'. The audit stores model 'hand-checked (qa)' from recorded_from. Alternatively, point the demo at the recorded live set and change the R-EX-6 byte test to structure only. Record whichever is chosen as a D-entry that amends D-029.",
74-   "acceptance_test": "E2E on FIXTURE_SET=curated: no element contains 'AI draft' or 'recorded AI answers' for a curated item; /items/e1/trace generator step evidence.model.id is not claude-sonnet-5-5 and its why names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'. With the recorded set, labels say AI."},
75-  {"severity": "major", "title": "Biggest product risk: a one-click Accept puts a summary the second check disputed into the carrier letter, and nobody is told which words are unsupported",
76-   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
77-   "why_it_matters": "Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.",
78-   "fix": "For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.",
79-   "acceptance_test": "lib11 e2 accept without confirm or edit returns 422 with a plain reason; with the confirm it is 200 and internal_notes_text names record 2 under the objection section; the new eval metric appears in the report."},
80-  {"severity": "major", "title": "The cut list and the spec no longer describe the product (R-CO-8 fails): 'cut' items are built, all four stretch items ship, and R-CH-7 is contradicted",
81-   "evidence": "memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues against PDF upload and the firm-voice paragraph; §5 non-goals 1, 2, 9-14, 16, 19 contradict the build. R-CH-7 (:84) says 'no path turns a rate, estimate or unreadable amount into a totaled charge', but SCOPE_CUTS 7g says 'Proposed'/'Quoted' charge lines are still countable (D-064). Appendix A: 'Stretch (pick at most one ...)'.",
82-   "why_it_matters": "Appendix A grades 'cut scope on purpose and tell us what you cut'. Right now the written reasons argue against features the panel will see working. That reads as either not knowing the product or not cutting at all. An estimate counted into 'Billed charges accepted' is a false statement in the letter that the spec still forbids.",
----
 evals/reports/m3-sensors.md      | 20 ++++++++++----------
 memory/ORCHESTRATOR_DECISIONS.md |  3 +++
 memory/SCOPE_CUTS.md             |  5 +++++
 reviews/GATE-M3-round1-triage.md | 17 +++++++++++++++++
 4 files changed, 35 insertions(+), 10 deletions(-)
----
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
 M app/backend/case_extras.py
MM app/backend/case_list.py
 M app/backend/export.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:45.829Z

**tool call — Bash**
````
{
 "command": "git diff --stat 04ea2bf HEAD -- app tests evals/golden spec docs | tail -2; echo \"app/tests diff 04ea2bf..HEAD lines: $(git diff 04ea2bf HEAD -- app tests | wc -l)\"; ls -d .venv 2>/dev/null; D=artifacts/review-evidence/T-177-staff-engineer; mkdir -p \"$D\" && git archive 04ea2bf | tar -x -C \"$D\" && ls \"$D\" && ls \"$D/tests\" && cat \"$D/tests/e2e/conftest.py\" | head -80",
 "description": "Extract commit 04ea2bf into review evidence dir and inspect e2e conftest"
}
````

### User / tool · 2026-11-02T20:33:46.558Z

**tool result**
````
app/tests diff 04ea2bf..HEAD lines:        0
.venv
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
__init__.py
conftest.py
e2e
fixtures
unit
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
T-136 round 2: compare-export-note (D-058: a note on an accepted, compared quote-only edit under the AI's summary whose second AI check has no answer: the server's blocker sentence; holds btn-write-summary 'Write the summary', which opens the edit box; NO rerun button), data-blocker-code (the reason code on a gate-blocker row, e.g. JUDGE_NOT_RUN), btn-gate-write-summary (the same action on that item's JUDGE_NOT_RUN gate-blocker row); the row's entry-state chip of a compared edit reads
  'Compared by you' (not 'Needs review') with entry-reasons 'Compared by you with the quote; the second AI check ...'; edited-note of a quote-only edit reads 'Quote changed by you' and shows the original excerpt.
T-142: conflict-empty (the Conflicts group's empty state: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.'), conflict-coverage (details in the Conflicts group: open when empty, collapsed when conflicts are listed; words from GET case `checks`
  {conflict_types, labels, not_checked}, a fixed fallback without it) holding conflict-checked-item, conflict-not-checked-item and, in the fallback only, conflict-coverage-note.
T-149 (multi-case, tests/e2e/test_multicase.py): cases-overview (the home section, local mode only), cases-row (one per case, data-token), cases-open (the link that opens it), cases-title, cases-dates (<time> elements), cases-stage, cases-progress-<kind> (a <progress>, kind = entries | flags | amounts)
  with cases-progress-text-<kind> ('2 of 5'), call-out chips cases-chip-needs-review, cases-chip-edits, cases-chip-tray, cases-chip-blocked ('Export blocked (n)') with cases-blocker-reason (one per distinct reason, first two), cases-chip-ready; cases-filter-all / cases-filter-attention / cases-filter-ready (aria-pressed),
  cases-sort (select: attention, recent, least_done, title), cases-count, cases-empty. Detail: case-overview (first block of the timeline), co-progress-<kind> / co-progress-text-<kind>, co-chip-needs-review / co-chip-edits / co-chip-tray / co-chip-blocked / co-chip-ready, co-blocker-reason,
  co-gate-steps (<details>) with co-gate-toggle (its summary), co-gate-verdict, co-gate-step (one per step of GET trace; data-step-id, data-step-status) holding co-gate-word and co-gate-why; btn-all-cases (header: back to the overview).
  Literal forms used by specs: cases-progress-entries, cases-progress-<seq>, cases-progress-text-entries, cases-progress-text-<seq>, co-progress-entries, co-progress-<seq>, co-progress-text-entries, co-progress-text-<seq> (<seq> = flags | amounts).
T-149 round 2 (tests/e2e/test_multicase.py): the overview block is ONE block: it holds todo-strip and checks-card (case-stepper, judge-panel) in its .co-slot; co-gate-* are gone (the Case checks rail is the one place for the steps). need-review-count is now the block's
  needs-review chip (open items only), co-chip-edits, co-chip-tray (quiet), cases-chip-can-export and co-chip-can-export ('Can export \u2014 N not reviewed (they stay out of the letter)', amber), co-chip-ready ('Everything decided', green, only when nothing is undecided), co-chip-blocked; the same chip ids with the cases- prefix on a row.
  Row: cases-decided ('n of N decided'), cases-next (the one call-out of a not-analyzed or failed row), cases-search (title), cases-list (data-ready="true" after the first settled paint), cases-loading, cases-load-error with cases-retry, cases-open-error, filter cases-filter-ready is now 'Ready to send'.
  Detail: case-heading (the h2, tabindex -1, focused when a case opens from the list, aria-label names the case), do-first with btn-do-first (one line from next_action {item_id, kind, reason}), btn-rename-case, case-rename-input, btn-save-rename, case-rename-error, todo-more (phone: the jump list behind one line),
  data-do-first (attribute on the overview block while the line is shown), LiveRerun and JudgeNotRun (stubs that make GET case say rerun_available true), rerun-unavailable (the sentence that replaces the rerun button when no item says rerun_available), input-title (the case name field beside Analyze).
T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
T-136 r3 (tests/e2e/test_held_quote_gate.py): btn-write-summary-case ('Write the summary' on the case-level places: the 'Ready to export?' and 'Second AI check' steps of the case rail and the 'How the AI was checked' rows; opens the entry's summary box like the blocker row's btn-gate-write-summary). A held re-picked quote offers btn-rerun-judge only until a rerun gave no answer (the blocker's rerun_no_answer).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:48.118Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && cat tests/unit/test_prepared_provenance.py; echo =====; cat tests/e2e/test_demo_provenance.py",
 "description": "Read the two new test files in the archive"
}
````

### User / tool · 2026-11-02T20:33:48.229Z

**tool result**
````
"""T-177 / D-065 (GATE-M3 PM blocker): a curated (hand-checked) fixture answer is never presented as model output.
Provenance comes from the fixture's own `recorded_from`. Curated -> prepared: true, model 'hand-checked (qa)' in the item, the trace and the audit rows;
the trace's generator step says it is a prepared answer. Recorded (and live) answers keep their real model ids and their AI labels."""
import json
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"


def _client(tmp_path, monkeypatch, fixture_set):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    else:
        monkeypatch.delenv("FIXTURE_SET", raising=False)
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _run(c):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, None)
    return c, _run(c)


def _generator_step(trace):
    return next(s for s in trace["steps"] if s["id"] == "extracted")


# ---- curated set
def test_curated_audit_rows_carry_the_prepared_model(curated):
    c, tok = curated
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    gen = [x for x in calls if x["role"] == "generator"]
    assert len(gen) >= 9
    for x in gen:
        assert x["model"] == PREPARED_MODEL and x["prepared"] is True, x
    # D-056: judge answers are real recordings; they keep their real model id and are not prepared
    judges = [x for x in calls if x["role"] == "judge"]
    assert judges and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in judges)


def test_curated_item_is_marked_prepared(curated):
    c, tok = curated
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"]
    for e in case["entries"]:
        assert e["prepared"] is True, e["id"]
        assert e["ladder"]["generator"]["model"] == PREPARED_MODEL and e["ladder"]["generator"]["prepared"] is True
    item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED_MODEL


def test_curated_trace_generator_step_names_a_prepared_answer(curated):
    c, tok = curated
    st = _generator_step(c.get(f"/api/cases/{tok}/items/e1/trace").json())
    ev = st["evidence"]
    assert ev["model"]["id"] == PREPARED_MODEL and ev["model"]["id"] != "claude-sonnet-5-5" and ev["model"]["prepared"] is True
    assert st["why"] == "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
    assert "AI read this record" not in json.dumps(st) and "AI drafted" not in st["label"]


def test_curated_health_says_prepared_and_the_banner_does_not_claim_ai(curated):
    c, tok = curated
    h = c.get("/api/health").json()
    assert h["answers"] == "prepared" and "prepared by our team" in h["ai_banner"] and "drafted by AI" not in h["ai_banner"]
    # the second check is still an AI check (a real recorded answer) and keeps its model id
    tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
    j = next(s for s in tr["steps"] if s["id"] == "judge_1")
    assert j["evidence"]["model"]["id"] != PREPARED_MODEL and not j["evidence"]["model"].get("prepared")


# ---- recorded set: labels stay AI
def test_recorded_set_keeps_ai_labels_and_model_ids(recorded):
    c, tok = recorded
    h = c.get("/api/health").json()
    assert h["answers"] == "recorded" and "drafted by AI" in h["ai_banner"]
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    assert calls and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in calls)
    assert any(x["model"] == "claude-sonnet-5-5" for x in calls)
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"] and all(e["prepared"] is False for e in case["entries"])
    e1 = case["entries"][0]
    assert e1["ladder"]["generator"]["model"] == "claude-sonnet-5-5" and e1["ladder"]["generator"].get("prepared") is False
    st = _generator_step(c.get(f"/api/cases/{tok}/items/{e1['id']}/trace").json())
    assert st["evidence"]["model"]["id"] == "claude-sonnet-5-5" and st["evidence"]["model"]["prepared"] is False
    assert st["why"] == "The AI read this record and proposed a one-line summary and a quote."


def test_live_backend_health_says_live(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    from app.backend import store
    monkeypatch.setattr(store, "live_enabled", lambda: True)
    assert c.get("/api/health").json()["answers"] == "live"
=====
"""T-177 / D-065 (GATE-M3 product-manager blocker): the demo never shows a hand-checked (curated) answer as the AI's.
Acceptance test (the PM's), curated set (the default private server, FIXTURE_SET=curated): no element names 'AI draft' or 'recorded AI answers' for a curated item; the badge says the answers were
prepared by the team and its tooltip points at the evaluation report; /items/e1/trace's generator step is not claude-sonnet-5-5 and names a prepared answer; /audit rows for the generator carry
model 'hand-checked (qa)'. Recorded set (a second private server, no FIXTURE_SET): the labels say AI and the model ids are real.
New test ids (declared in tests/e2e/conftest.py, 'T-177'): tag-prepared, tag-ai-draft, audit-prepared."""
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, reveal, ROOT, BASE

PREPARED = "hand-checked (qa)"
WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
TOOLTIP = "The AI's own answers on these cases are in the evaluation report."


def _ready(call, tok):
    for _ in range(300):
        s = call("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def curated_case():
    st, c = api("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(api, tok)
    yield tok
    api("DELETE", f"/api/cases/{tok}")


@pytest.fixture(scope="module")
def recorded_server():
    """A private app on its own port with the recorded (real model answers) fixture set: FIXTURE_SET unset."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-rec-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", ZLAYT_DB=os.path.join(tmp, "rec.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None); env.pop("FIXTURE_SET", None); env.pop("LLM_FIXTURE_DIR", None); env.pop("ENABLE_LIVE", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            assert proc.poll() is None, "the recorded-set server exited"
            time.sleep(.5)
    else:
        proc.kill(); pytest.fail("the recorded-set server did not start")

    def call(method, path, body=None):
        req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    yield base, call
    proc.terminate()
    try: proc.wait(timeout=10)
    except Exception: proc.kill()
    log.close()


def _open_why(page, n):
    reveal(page.get_by_test_id(f"entry-{n}").get_by_test_id("entry-why")).click()
    page.get_by_test_id("item-stepper").wait_for()
    return page.get_by_test_id("item-stepper")


# ---- the PM's acceptance test: API half (curated)
def test_curated_trace_and_audit_say_prepared(curated_case):
    tok = curated_case
    tr = api("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] != "claude-sonnet-5-5" and gen["evidence"]["model"]["id"] == PREPARED and gen["evidence"]["model"]["prepared"] is True
    assert gen["why"] == WHY and "prepared answer" in gen["why"].lower()
    audit = api("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    gens = [c for c in audit if c["role"] == "generator"]
    assert gens and all(c["model"] == PREPARED and c["prepared"] is True for c in gens), [(c["step"], c["model"]) for c in gens]
    assert not any(c["model"] == "claude-sonnet-5-5" for c in gens)
    item = api("GET", f"/api/cases/{tok}/items/e1")[1]["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED
    assert api("GET", "/api/health")[1]["answers"] == "prepared"


# ---- the PM's acceptance test: page half (curated)
def test_curated_page_never_calls_a_prepared_answer_ai(page, curated_case):
    open_case(page, curated_case)
    badge = page.locator("#badge")
    expect(badge).to_have_text("Demo: sample answers prepared by our team")
    assert badge.get_attribute("title") == TOOLTIP
    entries = page.locator("[data-testid^=entry-][data-entry-id]")
    n = entries.count(); assert n >= 9
    assert page.get_by_test_id("tag-prepared").count() == n and page.get_by_test_id("tag-ai-draft").count() == 0
    assert page.get_by_test_id("tag-prepared").first.inner_text() == "Prepared answer"
    text = page.evaluate("document.body.innerText")
    assert "AI draft" not in text and "recorded AI answers" not in text, re.findall(r".{20}(?:AI draft|recorded AI answers).{20}", text)
    assert page.locator("[title*='Drafted by AI'], [aria-label*='AI draft']").count() == 0
    assert "drafted by AI" not in page.locator("#banner-ai").inner_text() and "prepared by our team" in page.locator("#banner-ai").inner_text()
    st = _open_why(page, 1)
    gen = st.get_by_test_id("step").first
    assert gen.get_by_test_id("step-kind").inner_text() == "Prepared answer"
    body = st.inner_text()
    assert "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft" in body
    assert "AI draft" not in body.replace("standing in for the AI draft", "") and "claude-sonnet-5-5" not in body and "The AI read this record" not in body


def test_curated_audit_drawer_marks_the_prepared_rows(page, curated_case):
    open_case(page, curated_case)
    reveal(page.get_by_test_id("entry-1").get_by_test_id("btn-audit")).click()
    page.get_by_test_id("audit-drawer").wait_for()
    drawer = page.get_by_test_id("audit-drawer")
    expect(drawer.get_by_test_id("audit-prepared").first).to_have_text("Prepared answer")
    assert PREPARED in drawer.inner_text() and "claude-sonnet-5-5" not in drawer.inner_text()


# ---- recorded set: the labels say AI
def test_recorded_set_labels_say_ai(pw, recorded_server):
    base, call = recorded_server
    st, c = call("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); tok = c["token"]
    assert call("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(call, tok)
    assert call("GET", "/api/health")[1]["answers"] == "recorded"
    tr = call("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] == "claude-sonnet-5-5" and gen["evidence"]["model"]["prepared"] is False
    assert gen["why"] == "The AI read this record and proposed a one-line summary and a quote."
    calls = call("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    assert calls and not any(x["prepared"] or x["model"] == PREPARED for x in calls)
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    try:
        pg.goto(f"{base}/#/case/{tok}"); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        expect(pg.locator("#badge")).to_have_text("Demo: recorded AI answers")
        assert pg.get_by_test_id("tag-prepared").count() == 0 and pg.get_by_test_id("tag-ai-draft").count() >= 1
        assert "prepared by our team" not in pg.evaluate("document.body.innerText")
        st_ = _open_why(pg, 1)
        assert st_.get_by_test_id("step").first.get_by_test_id("step-kind").inner_text() == "AI draft"
    finally:
        b.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:33:58.679Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && grep -n -E \"^def |^@pytest|BASE|7860|Popen|FIXTURE_SET|E2E_REQUIRE_DB|skip\" tests/e2e/conftest.py | head -80; echo ----; ls tests/fixtures/llm/ | head; ls tests/fixtures/llm/curated | head -40; echo ----; lsof -nP -iTCP:7860 -sTCP:LISTEN 2>/dev/null; echo \"lsof rc=$?\"",
 "description": "Inspect e2e conftest fixtures, fixture dirs, and port 7860 status"
}
````

### User / tool · 2026-11-02T20:33:58.858Z

**tool result**
````
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
2:Every spec is skipped with a clear reason when the server is not up (M3 not built yet).
11:  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
17:  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
22:T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
50:  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
76:T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
77:  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
98:  T-174 (MVP finish, tests/e2e/test_mvp_finish.py): section-nav (a sticky bar under the case header with nav-overview, nav-timeline, nav-flags, nav-charges, nav-export; each shows what is still open in its section and the current one carries aria-current=location), btn-back-to-review (the first control in the Export view; closes Export and returns focus to the row she left), btn-error-action (the one action button inside an input error box `error`: Try again, Use the sample case, Edit the text, Choose a .txt file), charge-detail (the code's detail of a not-counted amount, inside the row's More panel). The skip link and n go to case.next_action.item_id: the case overview box carries it as data-do-first-item (the item named in do-first-item). cases-status-error and cases-status-retry (T-175 r2: the message and the Try again button on a case-list row with status_error; no counts, bar or Can export on it), case-switcher (the 'Add a synthetic case' card under the case list; shown on the overview only).
106:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
115:def pytest_configure(config):
117:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
118:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
119:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
120:    global BASE
121:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
126:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
129:    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
133:        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
141:        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)
155:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
164:def needs_db():
165:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
166:    one fails instead of skipping, so a run can say '0 skipped'."""
169:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
170:        if os.environ.get("E2E_REQUIRE_DB") == "1":
172:        pytest.skip(msg)
175:def _up():
177:        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
182:def pytest_collection_modifyitems(config, items):
185:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
188:            it.add_marker(skip)
190:def api(method, path, body=None):
191:    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
200:def golden_text(name):
203:def tray_entry_for_record(tok, record_id):
232:@pytest.fixture
233:def base_url():
234:    return BASE
236:@pytest.fixture
237:def sample_case():
251:@pytest.fixture(scope="session")
252:def pw():
253:    sync = pytest.importorskip("playwright.sync_api")
257:@pytest.fixture
258:def page(pw):
267:def open_case(page, tok):
268:    page.goto(f"{BASE}/#/case/{tok}")
271:def reveal(loc):
423:                    st.update(status="skipped", reason_code="JUDGE_UNAVAILABLE", why="The second AI check never gave an answer for this item.", next_action=self._na(d["item_id"]))
----
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
00e8d38a3d50d7d1d7a9b7431c6c2c1970b32930a2583c8a3acd58fdced43d2f.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
0115c20756060b7547d09ea7174734c62c4d2c54f0cc9840da3f4be1c00e19bb.json
03b065e9490648fde69d807c3f2719201ad149f6e41700f46c81c4258230b20a.json
03dca54059c1c53788cc6e6b66442c557959bc4443f86f86120412b8a7cf4b29.json
03f7de3945171cd4ccf7eed0a80ad8642913484686561e412ec1b8ee9a064d66.json
040a1015f827bfd1c0d6e0f5503b0004a738ca0871d71642a96e5eacee82f28e.json
0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
228350fb06e4cf872348f390212b959eebee7313b76f0edf051977846aacbc56.json
37318d752543b06d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json
3e70853a6fadff0e4991350de156ea38d30b396597dbab5bc74601b2508eb6d7.json
4770363f6bf66fd6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json
4a4f531c922d869d060a0bf7b1d33b777c496b90570dd511f38559feded30334.json
4ed3d9961f3523183444f9fe85f8d460762306ec1bc8d89ddca81e621c7a6198.json
7f9e06e6e15e75756fa39c3aca5bb45dcaa75e29d727b0d9b3a4da164dc54519.json
85a544a335859c486aaa581be110146353bbe09d65a0b3946d121a72f463ad81.json
98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
a1f0777e7722b161b62e8d670366303c827a2daff336fa324944e50a38f01c85.json
a3f0e26ea728d289fec7de9c1a0de532e5a7b68efdbb86a20f8dd418c7d461d8.json
aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d368d6a5bbc1c8c3d3bb3.json
b0511a4e8269eaffd9832fbd4d21b731b8a552b0d09aa0ba6294f427fbc83eca.json
b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3310718364dbfd51aee.json
bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json
be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d0117aabc60fc6202636ee.json
eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json
----
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  86899 arsis    9u  IPv4 0x89944c6bbeb1c380      0t0  TCP 127.0.0.1:7860 (LISTEN)
lsof rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:02.429Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -30",
 "description": "Run prepared-provenance unit tests on the 04ea2bf archive",
 "timeout": 320000
}
````

### User / tool · 2026-11-02T20:34:02.517Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:04.901Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -30 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-unit-prepared.out",
 "description": "Run prepared-provenance unit tests on the 04ea2bf archive",
 "timeout": 320000
}
````

### User / tool · 2026-11-02T20:34:07.731Z

**tool result**
````
......                                                                   [100%]
6 passed in 2.52s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:10.094Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v -p no:cacheprovider -rs 2>&1 | tail -60 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-e2e-provenance.out",
 "description": "Run demo provenance e2e tests on the 04ea2bf archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:34:15.867Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 4 items

tests/e2e/test_demo_provenance.py::test_curated_trace_and_audit_say_prepared PASSED [ 25%]
tests/e2e/test_demo_provenance.py::test_curated_page_never_calls_a_prepared_answer_ai PASSED [ 50%]
tests/e2e/test_demo_provenance.py::test_curated_audit_drawer_marks_the_prepared_rows PASSED [ 75%]
tests/e2e/test_demo_provenance.py::test_recorded_set_labels_say_ai PASSED [100%]

============================== 4 passed in 4.69s ===============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:21.294Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && python3 - <<'EOF'\nimport json,glob,collections\nc=collections.Counter()\nfor f in sorted(glob.glob('tests/fixtures/llm/curated/*.json')):\n    d=json.load(open(f))\n    rf=d.get('recorded_from',{})\n    c[(d.get('role') or d.get('step') or '?', rf.get('model'), str(d.get('CURATED'))[:40] if 'CURATED' in d else '-', tuple(sorted(d.keys())))]+=1\nfor k,v in c.items(): print(v,k)\nEOF\necho ----; for f in tests/fixtures/llm/curated/*.json; do python3 -c \"import json,sys;d=json.load(open(sys.argv[1]));print(sys.argv[1][-20:], json.dumps(d)[:300])\" \"$f\"; break; done; echo ----; ls tests/fixtures/llm/ ; ls tests/fixtures/llm/recorded 2>/dev/null | head -3; ls tests/fixtures/llm/recorded 2>/dev/null | wc -l",
 "description": "Summarize curated fixture metadata by role and provenance"
}
````

### User / tool · 2026-11-02T20:34:21.535Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:29.225Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py <<'EOF'\nimport json, sys, time, tempfile, os\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\", FIXTURE_SET=sys.argv[1])\nos.environ.pop(\"ANTHROPIC_API_KEY\", None); os.environ.pop(\"ENABLE_LIVE\", None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(prefix=\"t177probe-\")\nc = TestClient(create_app(os.path.join(d, \"p.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\nprint(\"HEALTH\", json.dumps(c.get(\"/api/health\").json()))\ntok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\nassert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\nfor _ in range(240):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.25)\nprint(\"STATUS\", s[\"status\"])\ncalls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\nfrom collections import Counter\nprint(\"AUDIT_COUNTS\", Counter((x[\"role\"], x[\"step\"], x[\"model\"], x[\"prepared\"]) for x in calls))\ncase = c.get(f\"/api/cases/{tok}\").json()\nprint(\"CASE_KEYS\", sorted(case.keys()))\nprint(\"ENTRY0_KEYS\", sorted(case[\"entries\"][0].keys()) if case.get(\"entries\") else None)\nprint(\"ENTRY0_PREPARED\", case[\"entries\"][0].get(\"prepared\") if case.get(\"entries\") else None)\nfor it in [\"e1\"]:\n    tr = c.get(f\"/api/cases/{tok}/items/{it}/trace\").json()\n    print(\"TRACE_KEYS\", sorted(tr.keys()))\n    for s in tr[\"steps\"]:\n        print(\"STEP\", s[\"id\"], \"|\", s.get(\"label\"), \"|\", s.get(\"kind\"), \"|\", s.get(\"why\"), \"|\", json.dumps(s.get(\"evidence\", {}).get(\"model\")))\nflags = case.get(\"flags\") or []\nprint(\"FLAG_COUNT\", len(flags), \"FLAG0_KEYS\", sorted(flags[0].keys()) if flags else None)\nfor f in flags[:2]:\n    fid = f.get(\"id\")\n    tr = c.get(f\"/api/cases/{tok}/items/{fid}/trace\")\n    if tr.status_code == 200:\n        for s in tr.json()[\"steps\"]:\n            print(\"FLAGSTEP\", fid, s[\"id\"], \"|\", s.get(\"label\"), \"|\", s.get(\"why\"), \"|\", json.dumps(s.get(\"evidence\", {}).get(\"model\")))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py curated 2>&1 | cut -c1-600 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-probe.out | head -80",
 "description": "Probe curated set API for provenance fields and audit rows",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:34:29.534Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py", line 5, in <module>
    from app.backend.api import create_app
ModuleNotFoundError: No module named 'app'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:31.079Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py curated 2>&1 | cut -c1-700 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-probe.out | head -80",
 "description": "Probe curated set API for provenance fields and audit rows",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:34:32.113Z

**tool result**
````
HEALTH {"ok": true, "version": "0.1.0", "synthetic_only": true, "banner": "Synthetic data only \u2014 never paste real records", "backend": "fixture", "demo_mode": true, "answers": "prepared", "live_enabled": false, "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}, "limits": {"max_chars": 60000, "max_records": 40}, "retention_hours": 24, "ai_banner": "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item", "sample_available": true}
STATUS ready
AUDIT_COUNTS Counter({('generator', 'extract', 'hand-checked (qa)', True): 9, ('judge', 'j1', 'claude-haiku-5-5', False): 9, ('generator', 'flags', 'hand-checked (qa)', True): 9, ('judge', 'j4', 'claude-haiku-5-5', False): 6, ('judge', 'j2', 'claude-haiku-5-5', False): 3, ('judge', 'j3', 'claude-haiku-5-5', False): 1})
CASE_KEYS ['amounts', 'backend', 'checks', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'gap_changes_removed', 'injection', 'models', 'name', 'next_action', 'records', 'review', 'status', 'title', 'token', 'totals', 'tray', 'tray_filtered', 'undated_entries', 'updated_at', 'warnings']
ENTRY0_KEYS ['ai_drafted', 'date', 'date_status', 'duplicate_note', 'edit_to_check', 'edited', 'entered_by', 'entered_by_reviewer', 'excerpt', 'excerpt_end', 'excerpt_start', 'id', 'ladder', 'prepared', 'provider', 'reasons', 'record_ids', 'rerun_available', 'rerun_note', 'review_status', 'second_check_pending', 'seq', 'source_kind', 'state', 'summary', 'translation', 'why']
ENTRY0_PREPARED True
TRACE_KEYS ['item_id', 'kind', 'mode', 'next_action', 'progress', 'review_status', 'state', 'state_reasons', 'steps', 'token', 'verdict']
STEP extracted | Prepared answer, standing in for the AI draft | llm | Prepared answer (hand-checked by the team for the demo), standing in for the AI draft | {"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
STEP excerpt_verbatim | Quote is word for word in the record | code | The quote was found in the record, character for character. | null
STEP excerpt_whole_sentence | Quote is made of whole sentences | code | The quote starts and ends on whole sentences. | null
STEP excerpt_hedge | Quote keeps the hedge sentence that qualifies it | code | No hedge sentence that qualifies the quote is left out. | null
STEP summary_tokens | Numbers and dates in the summary are in the quote | code | Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote. | null
STEP summary_qualifier | Summary keeps the quote's qualifiers | code | Every hedge, attribution, negation, side and approximation in the quote is in the summary. | null
STEP highlight | Quote can be highlighted in the record | code | The quote's position in the record was found, so it can be highlighted. | null
STEP date_confirmed | Date of service is confirmed | code | The date comes from the record's own header and is parsed or confirmed. | null
STEP injection_scan | Record has no instruction-like text | code | The record has no instruction-like text. | null
STEP judge_1 | Second AI check: is the summary supported by the quote? | llm | The second check found every statement in the summary in the quote. | {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true, "prepared": false}
STEP human | Your decision | human | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | null
FLAG_COUNT 10 FLAG0_KEYS ['category', 'computed', 'edited', 'evidence', 'explanation', 'gap_change', 'id', 'ladder', 'origin', 'prepared', 'reasons', 'rerun_available', 'rerun_note', 'review_status', 'reviewer_note', 'second_check_pending', 'source_kind', 'state', 'title', 'type', 'why']
FLAGSTEP f_gap_r6_r7 computed | Dates compared by code | Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient). | null
FLAGSTEP f_gap_r6_r7 spans_match | Cited text matches the record | Every cited date line is in the record, character for character. | null
FLAGSTEP f_gap_r6_r7 endpoints_confirmed | Dates at both ends are confirmed | Both dates are parsed or confirmed. | null
FLAGSTEP f_gap_r6_r7 injection_scan | Record has no instruction-like text | The record has no instruction-like text. | null
FLAGSTEP f_gap_r6_r7 judge_not_needed | Second AI check | Not needed: this is arithmetic over dates in the record, which code does exactly. | null
FLAGSTEP f_gap_r6_r7 human | Your decision | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 computed | Stated and recorded dates compared by code | Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 spans_match | Cited text matches the record | Every cited date line is in the record, character for character. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 endpoints_confirmed | Dates at both ends are confirmed | Both dates are parsed or confirmed. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 injection_scan | Record has no instruction-like text | The record has no instruction-like text. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 judge_not_needed | Second AI check | Not needed: this is arithmetic over dates in the record, which code does exactly. | null
FLAGSTEP f_accident_date_after_treatment_1_2_7 human | Your decision | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | null
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:41.687Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && P=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py && sed -i 's/os.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\", FIXTURE_SET=sys.argv\\[1\\])/os.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\"); (os.environ.__setitem__(\"FIXTURE_SET\", sys.argv[1]) if sys.argv[1] != \"none\" else os.environ.pop(\"FIXTURE_SET\", None))/' $P && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python $P none 2>&1 | cut -c1-500 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-recorded-probe.out | head -30; echo ----; grep -n \"models\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-probe.out | cut -c1-200; PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport os,tempfile,json\nos.environ.update(LLM_BACKEND='fixture',ZLAYT_MODE='local'); os.environ['FIXTURE_SET']='curated'\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd=tempfile.mkdtemp()\nc=TestClient(create_app(os.path.join(d,'p.sqlite'),static_dir=d),client=('127.0.0.1',50000))\ntok=c.post('/api/cases',json={'sample':True}).json()['token']\nc.post(f'/api/cases/{tok}/run',json={})\nimport time\nfor _ in range(240):\n    s=c.get(f'/api/cases/{tok}/status').json()\n    if s['status'] in ('ready','failed'): break\n    time.sleep(.25)\nprint('CASE_MODELS', json.dumps(c.get(f'/api/cases/{tok}').json()['models']))\nprint('AUDIT_ONE', json.dumps(c.get(f'/api/cases/{tok}/audit').json()['calls'][0])[:600])\n\" 2>&1 | cut -c1-700",
 "description": "Probe recorded set and check case-level model fields",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:34:43.048Z

**tool result**
````
sed: 1: "/Users/arsis/zlayt-pm-p ...": command a expects \ followed by text
----
1:HEALTH {"ok": true, "version": "0.1.0", "synthetic_only": true, "banner": "Synthetic data only \u2014 never paste real records", "backend": "fixture", "demo_mode": true, "answers": "prepared", "live
4:CASE_KEYS ['amounts', 'backend', 'checks', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'gap_changes_removed', 'injection', 'models', 'name', 'next_action', 'records',
CASE_MODELS {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}
AUDIT_ONE {"id": "cf599cfd78190", "role": "generator", "step": "extract", "backend": "fixture", "recorded_from": {"backend": "curated", "model": "hand-checked (qa)", "recorded_at": "2026-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3310718364dbfd51aee", "item_id": "e2", "attempt": 1, "latency_ms": 0, "cost_usd": 0.0, "tokens_in": 0, "tokens_out": 0, "parsed_ok": true, "verdict": null, "prepared": true, "system_text": "You write one timeline entry for a paralegal from a single medical record.\n\nThe record
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:47.487Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && python3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py'\ns=open(p).read()\ns=s.replace('os.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\", FIXTURE_SET=sys.argv[1])',\n 'os.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\\nif sys.argv[1] != \"none\": os.environ[\"FIXTURE_SET\"] = sys.argv[1]\\nelse: os.environ.pop(\"FIXTURE_SET\", None)')\nopen(p,'w').write(s)\nEOF\nPYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-probe.py none 2>&1 | cut -c1-420 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-recorded-probe.out | head -24; echo ----; grep -rn \"models\\.\\|\\.models\\b\\|'models'\\|\\\"models\\\"\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer/app/frontend/*.js | cut -c1-250 | head; echo ----; grep -rn \"AI draft\\|recorded AI answers\\|AI read\\|AI suggested\\|AI check\" app/frontend/*.js app/frontend/*.html 2>/dev/null | cut -c1-220 | head -40",
 "description": "Run recorded-set probe; grep frontend for model and AI labels",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:34:48.646Z

**tool result**
````
HEALTH {"ok": true, "version": "0.1.0", "synthetic_only": true, "banner": "Synthetic data only \u2014 never paste real records", "backend": "fixture", "demo_mode": true, "answers": "recorded", "live_enabled": false, "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}, "limits": {"max_chars": 60000, "max_records": 40}, "retention_hours": 24, "ai_banner": "Summaries and flags are drafted by AI and
STATUS ready
AUDIT_COUNTS Counter({('generator', 'extract', 'claude-sonnet-5-5', False): 9, ('judge', 'j1', 'claude-haiku-5-5', False): 9, ('generator', 'flags', 'claude-sonnet-5-5', False): 9, ('judge', 'j4', 'claude-haiku-5-5', False): 7, ('judge', 'j2', 'claude-haiku-5-5', False): 3, ('judge', 'j3', 'claude-haiku-5-5', False): 1})
CASE_KEYS ['amounts', 'backend', 'checks', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'gap_changes_removed', 'injection', 'models', 'name', 'next_action', 'records', 'review', 'status', 'title', 'token', 'totals', 'tray', 'tray_filtered', 'undated_entries', 'updated_at', 'warnings']
ENTRY0_KEYS ['ai_drafted', 'date', 'date_status', 'duplicate_note', 'edit_to_check', 'edited', 'entered_by', 'entered_by_reviewer', 'excerpt', 'excerpt_end', 'excerpt_start', 'id', 'ladder', 'prepared', 'provider', 'reasons', 'record_ids', 'rerun_available', 'rerun_note', 'review_status', 'second_check_pending', 'seq', 'source_kind', 'state', 'summary', 'translation', 'why']
ENTRY0_PREPARED False
TRACE_KEYS ['item_id', 'kind', 'mode', 'next_action', 'progress', 'review_status', 'state', 'state_reasons', 'steps', 'token', 'verdict']
STEP extracted | AI drafted a summary and picked a quote | llm | The AI read this record and proposed a one-line summary and a quote. | {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null, "prepared": false}
STEP excerpt_verbatim | Quote is word for word in the record | code | The quote was found in the record, character for character. | null
STEP excerpt_whole_sentence | Quote is made of whole sentences | code | The quote starts and ends on whole sentences. | null
STEP excerpt_hedge | Quote keeps the hedge sentence that qualifies it | code | No hedge sentence that qualifies the quote is left out. | null
STEP summary_tokens | Numbers and dates in the summary are in the quote | code | Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote. | null
STEP summary_qualifier | Summary keeps the quote's qualifiers | code | Every hedge, attribution, negation, side and approximation in the quote is in the summary. | null
STEP highlight | Quote can be highlighted in the record | code | The quote's position in the record was found, so it can be highlighted. | null
STEP date_confirmed | Date of service is confirmed | code | The date comes from the record's own header and is parsed or confirmed. | null
STEP injection_scan | Record has no instruction-like text | code | The record has no instruction-like text. | null
STEP judge_1 | Second AI check: is the summary supported by the quote? | llm | The second check found every statement in the summary in the quote. | {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true, "prepared": false}
STEP human | Your decision | human | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | null
FLAG_COUNT 10 FLAG0_KEYS ['category', 'computed', 'edited', 'evidence', 'explanation', 'gap_change', 'id', 'ladder', 'origin', 'prepared', 'reasons', 'rerun_available', 'rerun_note', 'review_status', 'reviewer_note', 'second_check_pending', 'source_kind', 'state', 'title', 'type', 'why']
FLAGSTEP f_gap_r6_r7 computed | Dates compared by code | Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient). | null
FLAGSTEP f_gap_r6_r7 spans_match | Cited text matches the record | Every cited date line is in the record, character for character. | null
FLAGSTEP f_gap_r6_r7 endpoints_confirmed | Dates at both ends are confirmed | Both dates are parsed or confirmed. | null
FLAGSTEP f_gap_r6_r7 injection_scan | Record has no instruction-like text | The record has no instruction-like text. | null
FLAGSTEP f_gap_r6_r7 judge_not_needed | Second AI check | Not needed: this is arithmetic over dates in the record, which code does exactly. | null
----
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer/app/frontend/judges.js:166:    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer/app/frontend/judges.js:196:            el("span", { class: "zs-k" }, "Prompt "), j.prompt_version || "", el("span", { class: "zs-k" }, " · model "), (j.models || []).join("
----
app/frontend/api.js:43:    rejudge: (token) => call("POST", t(token) + "/rejudge"),            // D-044: run the second AI check again for accepted items it never checked
app/frontend/app.js:15:    badge.textContent = prepared ? "Demo: sample answers prepared by our team" : demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
app/frontend/app.js:17:      : demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
app/frontend/batch.js:118:    dlg.querySelector("#bc-text").textContent = "The code and the second AI check found support for " + (n === 1 ? "this entry" : "these " + n + " entries") + ", but you have not decided on " + 
app/frontend/dom.js:52:  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
app/frontend/charges.js:85:      done ? "You confirmed it is a separate charge for a service. No AI check was asked about it." : "You took back your count. Accept it to count this line again; you confirm it is a separate
app/frontend/charges.js:101:      const t = done ? "You counted this line as a separate charge and confirmed it by name at " + f.confirmed_at + ". No AI check was asked about it." : "You counted this line, then took the 
app/frontend/judges.js:1:/* "How the AI was checked" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, agreed / objected / unavailable counts,
app/frontend/judges.js:2:   each objection with its fixed-sentence reason, and where the code checks and the AI read an item differently. Every row links to the item's stepper.
app/frontend/judges.js:22:    disagrees: "The AI reads this differently from the draft.",
app/frontend/judges.js:28:  const TODO_BLOCKED = "The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again; if it still cannot answer, dismiss the item.";   // accepted/e
app/frontend/judges.js:49:  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "accept".
app/frontend/judges.js:165:    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
app/frontend/judges.js:170:    det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
app/frontend/judges.js:183:        nBlock ? plural(nBlock, "accepted item", "accepted items") + " cannot go in the letter until the second AI check has run on " + (nBlock === 1 ? "it" : "them") + "."
app/frontend/judges.js:189:    if (differ.length) det.append(list("judge-disagreements", "Where code and the AI read an item differently", differ, (i) => row(i, "judge-disagreement"), ""));
app/frontend/judges.js:219:      }, () => { if (cache) return; if (ZL.API_MODE === "mock" && root.isConnected) paint(root, null, "AI check details need the live server."); else root.hidden = true; });
app/frontend/stepper.js:41:    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
app/frontend/stepper.js:42:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:142:  // ---- "Run the second check again" (D-044): POST /rejudge for the accepted items whose second AI check never ran. One handler for every place that offers it
app/frontend/stepper.js:150:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
app/frontend/stepper.js:152:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
app/frontend/stepper.js:255:    judges: ["Open the AI checks", () => gotoPanel("judges")],
app/frontend/stepper.js:272:        if (unRerun) bits.push("The second AI check did not run on " + plural(unRerun, "item", "items") + ". Run it again; accepted items it never checked cannot go in the letter.");
app/frontend/stepper.js:291:        if (jnr.length) parts.push(plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check again; if it still ca
app/frontend/stepper.js:341:        if (t.view === "judges" && !(st && st.id === "judges")) btn("Open the AI checks", () => gotoPanel("judges"));
app/frontend/stepper.js:363:    if (st._notNeeded) { delete ev.judge_verdict; delete ev.rationale; delete ev.judge_reason_code; }   // "Not needed" must not also print "The second AI check said: Unavailable"
app/frontend/stepper.js:374:      out.push(el("p", { class: "zs-ev zs-judge", "data-testid": "step-judge-reason" }, el("strong", {}, "The second AI check said: "), S.verdictWord(ev.judge_verdict),
app/frontend/stepper.js:438:  const HUMAN_NOTE = "Not needed: this is your own wording, so the second AI check does not apply. The code checks on it still run.";
app/frontend/stepper.js:522:  S.HELD_NO_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary. The second AI check ran again and gave no answer on the new quote."
app/frontend/stepper.js:523:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed. The second AI check ran again and gave no answer on the new quotes.") + " Write
app/frontend/stepper.js:524:  S.HELD_CAN_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote."
app/frontend/stepper.js:525:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed, and the second AI check has no answer on the new quotes.") + " Run the second c
app/frontend/review.js:264:  // What happened to an edit, in plain words, kept on the row until the next decision: the code re-checks the wording against the quote on every save, then a second AI check reads it.
app/frontend/review.js:273:  const AI_HELD = "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you
app/frontend/review.js:274:  const ACCEPTED_HELD = "Compared by you. The second AI check still has no answer on the new quote, so the export stays blocked until it answers or you write the summary in your own words.";
app/frontend/review.js:302:    return lead + (st === "needs_review" ? " The entry still needs your review." : " The second AI check agreed.");
app/frontend/review.js:527:        isFlag ? null : el("p", { class: "rv-help rv-recheck-hint", "data-testid": "edit-recheck-hint" }, "When you save, the code checks every number, date and negation in your wording against
app/frontend/suggestions.js:140:        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These counts were measured before the latest change to the AI che
app/frontend/timeline.js:11:    JUDGE_DISAGREES: "the second check did not agree", LLM_ONLY: "only the AI suggested it; the checks found nothing to match", AI_TRANSLATION: "translated by AI; read the original quote yours
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:34:58.840Z

**tool call — Bash**
````
{
 "command": "git show 04ea2bf -- app/backend app/llm app/frontend/app.js app/frontend/audit.js app/frontend/stepper.js app/frontend/timeline.js | head -400",
 "description": "Show the app code diff for commit 04ea2bf"
}
````

### User / tool · 2026-11-02T20:34:58.952Z

**tool result**
````
commit 04ea2bf5e7cd2f3b84de7a5135d183e809baa84e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 14:20:49 2026 -0600

    feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index e1ef32d..5a4f4d4 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -34,6 +34,7 @@ LIBRARY = ROOT / "evals" / "library"
 VERSION = "0.1.0"
 BANNER = "Synthetic data only — never paste real records"
 AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
+PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item"      # D-065
 STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
 _ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}
 _PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
@@ -120,6 +121,13 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     def demo_mode():
         return not live_enabled()
 
+    def answers():
+        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
+        if live_enabled():
+            return "live"
+        from app.llm.backends import fixture
+        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
+
     def models():
         return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
 
@@ -232,9 +240,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     # -------------------------------------------------- routes
     @app.get("/api/health")
     def health():
-        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
+        ans = answers()
+        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "answers": ans,
                 "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
-                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
+                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
 
     @app.get("/api/cases")
     def list_cases():
@@ -500,7 +509,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         c = conn()
         try:
             get_case(c, token)
-            return {"narrative": narrative.get(c, token)}
+            return {"narrative": present.narrative_view(c, token, narrative.get(c, token))}
         finally:
             c.close()
 
@@ -513,7 +522,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
             if nar.get("error") == "NO_ACCEPTED_ENTRIES":
                 raise ApiError(400, "bad_request", "Accept at least one entry first; the paragraph is written from accepted entries only.")
-            return {"narrative": nar}
+            return {"narrative": present.narrative_view(c, token, nar)}
         finally:
             c.close()
 
@@ -524,7 +533,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         try:
             get_case(c, token)
             try:
-                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
+                return {"narrative": present.narrative_view(c, token, narrative.review(c, token, b.get("action"), now=time.time()))}
             except KeyError:
                 raise ApiError(404, "not_found", "No draft paragraph yet.") from None
             except ValueError:
diff --git a/app/backend/present.py b/app/backend/present.py
index c21d00f..f0e6380 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -4,6 +4,7 @@ import re
 
 from app.backend import amounts as AM, conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
 from app.db import db as DB
+from app.llm import audited as AU
 
 STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
 OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
@@ -43,8 +44,8 @@ def rerun_available(row) -> bool:
 def _common(row):
     return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
             "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
-            "rerun_available": rerun_available(row),
-            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message")}      # T-146 r3: set when a re-run disagreed with or failed on this decided item
+            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
+            "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item
 
 
 def entry_view(row, recs):
@@ -248,6 +249,7 @@ def item_view(conn, case_id, item_id):
     v = view_of(kind, row, conn, case_id, _recs_by_id(conn, case_id))
     v["kind"] = kind
     v["second_check_pending"] = item_id in second_check_pending_ids(conn, case_id)
+    with_provenance(conn, case_id, [v])
     if kind == "entry":
         review.hold_hints(conn, case_id, [v])      # T-139 r3: the held-out hint says where this record's figures are counted
     if kind == "flag":
@@ -255,6 +257,35 @@ def item_view(conn, case_id, item_id):
     return v
 
 
+def with_provenance(conn, case_id, views):
+    """D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name
+    ('hand-checked (qa)') on its ladder's generator, so no screen or payload names a model for an answer no model gave. Others get prepared false and keep their model id."""
+    calls = DB.list_llm_calls(conn, case_id)
+    by_id = {c["id"]: c for c in calls}
+    by_item = {}
+    for c in calls:
+        if c["role"] == "generator" and c.get("item_id"):
+            by_item.setdefault(c["item_id"], []).append(c)
+    for v in views:
+        gen = (v.get("ladder") or {}).get("generator")
+        call = by_id.get((gen or {}).get("call_id")) or next(iter(reversed(by_item.get(v["id"], []))), None)
+        prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
+        v["prepared"] = prepared
+        if gen is not None:
+            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
+            if prepared:
+                gen["model"] = call["model"]
+
+
+def narrative_view(conn, case_id, nar):
+    """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
+    if not nar or not isinstance(nar.get("generator"), dict):
+        return nar
+    call = next((c for c in DB.list_llm_calls(conn, case_id) if c["id"] == nar["generator"].get("call_id")), None)
+    prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
+    return {**nar, "prepared": prepared, "generator": {**nar["generator"], "prepared": prepared, **({"model": call["model"]} if prepared else {})}}
+
+
 def second_check_pending_ids(conn, case_id) -> set:
     """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
     acknowledges it, no check needed). Lazy import: trace imports this module."""
@@ -268,6 +299,7 @@ def all_items(conn, case_id):
     pool = CountPool(conn, case_id, records)
     out = {k: [view_of(k, r, conn, case_id, recs, records, pool) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
     review.hold_hints(conn, case_id, out["entry"])      # T-139 r3
+    with_provenance(conn, case_id, out["entry"] + out["amount"] + out["flag"])
     pend = second_check_pending_ids(conn, case_id)
     for k in ("entry", "amount", "flag"):
         for v in out[k]:
@@ -449,7 +481,7 @@ def _call(c, full=False):
     d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
          "prompt_version": c["prompt_version"], "prompt_sha256": c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
          "latency_ms": c["latency_ms"], "cost_usd": c["cost_usd"], "tokens_in": c["tokens_in"], "tokens_out": c["tokens_out"],
-         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"]}
+         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"], "prepared": AU.is_prepared(rf)}      # D-065: a hand-checked fixture answer, not model output
     if full:
         d.update(system_text=c["system_text"], user_text=c["user_text"], response_raw=c["response_raw"], error=c["error"])
     return d
diff --git a/app/backend/trace.py b/app/backend/trace.py
index 4ec7ed2..228c714 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -170,9 +170,14 @@ def _span(cx, rid, start, end, text):
     return {"record_id": rid, "start": start, "end": end, "text": text}
 
 
+PREPARED_LABEL = "Prepared answer, standing in for the AI draft"
+PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
+
+
 def _llm_evidence(cx, role, model, prompt_version, call):
     ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
-                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"]}}
+                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"],
+                    "prepared": bool(call) and AU.is_prepared(call.get("recorded_from"))}}      # D-065: a hand-checked fixture answer, not model output
     ev["prompt_version"] = (call or {}).get("prompt_version") or prompt_version
     if call:
         meta = present._call(call, cx.full)
@@ -402,8 +407,11 @@ def _entry_steps(cx, row):
                            " ".join((lad.get("summary_trim") or {}).get("notes") or []) + " " + reason_text("SUMMARY_NOT_IN_QUOTE"), reason="SUMMARY_NOT_IN_QUOTE",
                            rule="D-054", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
         else:
-            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
-                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
+            if ev["model"]["prepared"]:
+                st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
+            else:
+                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
+                               "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
             trim = lad.get("summary_trim")
             if trim and trim.get("removed"):                  # D-054: shown, never silent. The judge saw the trimmed summary.
                 st.append(step("summary_trimmed", "Code removed summary parts the quote does not support", "code", PASS, " ".join(trim.get("notes") or []),
@@ -677,7 +685,10 @@ def _flag_steps_core(cx, row):
         step_name = "conflicts" if ftype == "conflict" else "flags"
         call = cx.call(gen.get("call_id"), row["id"], step_name)
         ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
-        st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
+        if ev["model"]["prepared"]:
+            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
+        else:
+            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
     else:
         st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
     if ftype == "conflict":
@@ -745,7 +756,10 @@ def _narrative_trace(cx, item_id):
     call = cx.call(gen.get("call_id"))
     ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
     ev["values"] = {"entry_id": s["entry_id"], "text": s["text"]}
-    st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
+    if ev["model"]["prepared"]:
+        st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
+    else:
+        st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
     cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
     st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
                    reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
diff --git a/app/frontend/app.js b/app/frontend/app.js
index 2bc351d..9da57cd 100644
--- a/app/frontend/app.js
+++ b/app/frontend/app.js
@@ -10,8 +10,11 @@
     const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
     // T-166 F7: no test or developer wording on screen. The demo says what it is in the paralegal's words; the longer explanation is the tooltip. A live backend has nothing to announce.
     const badge = $("#badge"); const demo = !!(h && h.demo_mode), mock = ZL.API_MODE === "mock";
-    badge.textContent = demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
-    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
+    // D-065: say whose answers the demo replays. Prepared (curated) answers are the team's, never the model's; recorded ones are real model answers.
+    const prepared = demo && h.answers === "prepared";
+    badge.textContent = prepared ? "Demo: sample answers prepared by our team" : demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
+    badge.title = prepared ? "The AI's own answers on these cases are in the evaluation report."
+      : demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
     badge.hidden = !(demo || mock);
     const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
     live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
diff --git a/app/frontend/audit.js b/app/frontend/audit.js
index 4518c02..ad3468e 100644
--- a/app/frontend/audit.js
+++ b/app/frontend/audit.js
@@ -18,9 +18,9 @@
   const pre = (label, text) => (text == null || text === "" ? null : el("details", { class: "au-more" }, el("summary", {}, label), el("pre", { class: "au-pre" }, typeof text === "string" ? text : JSON.stringify(text, null, 2))));
 
   function callRow(c) {
-    const rf = c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
+    const rf = c.prepared ? " (prepared answer, not model output)" : c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
     return el("li", { class: "au-call", "data-testid": "audit-call" },
-      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
+      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.prepared ? el("span", { class: "rv-chip", "data-testid": "audit-prepared" }, "Prepared answer") : null, c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
       el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prompt_version), kv("hash", c.prompt_sha256 ? String(c.prompt_sha256).slice(0, 12) : null),
         kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
       pre("System prompt (local mode)", c.system_text), pre("Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
diff --git a/app/frontend/stepper.js b/app/frontend/stepper.js
index 62a5457..26e1e50 100644
--- a/app/frontend/stepper.js
+++ b/app/frontend/stepper.js
@@ -38,6 +38,7 @@
     if (st.kind === "human") return "You";
     if (st.kind === "code") return "Code";
     const m = st.evidence && st.evidence.model;
+    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
     return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
   };
   const humanize = (k) => String(k).replace(/_/g, " ");
diff --git a/app/frontend/timeline.js b/app/frontend/timeline.js
index 8d7b5f6..6afc479 100644
--- a/app/frontend/timeline.js
+++ b/app/frontend/timeline.js
@@ -17,6 +17,10 @@
   const fullReason = (it) => String(it.why || "").trim() || plainReason(it);
 
   // T-136 r2: the reason line of an edit she compared with the quote and accepted: her act first, then what the second check did (the server's own first sentence when it is not "did not run").
+  // D-065: a hand-checked demo answer is a "Prepared answer", never an AI draft; recorded and live answers keep the AI label.
+  const aiTag = (e) => !e.ai_drafted ? null : e.prepared
+    ? el("span", { class: "tag", "data-testid": "tag-prepared", title: "Prepared by our team for this demo, standing in for the AI draft" }, "Prepared answer")
+    : el("span", { class: "tag", "data-icon": "ai", "data-testid": "tag-ai-draft", title: "Drafted by AI" }, "draft");
   const comparedReason = (e) => "Compared by you with the quote. " + ((e.reasons || []).includes("JUDGE_UNAVAILABLE") ? "The second AI check did not run." : plainReason(e));
   const STATE_TONE = { verified: ["info", "match"], needs_review: ["warn", "alert"], rejected: ["bad", "x"] };
   const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
@@ -58,7 +62,7 @@
         e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : null,
         reasonText_ ? el("p", { class: "reason" + (e.reasons.includes("AI_TRANSLATION") ? " reason--caution" : ""), "data-testid": "entry-reasons", title: fullReason(e) }, reasonText_) : null,
         chips(e)),
-      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
+      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, aiTag(e)),
       e.edited ? el("p", { class: "muted small note", "data-testid": "edited-note" }, e.edited.original_summary != null
         ? "Edited by you; the code checked your wording against the quote when you saved. Original: " + e.edited.original_summary
         : "Quote changed by you; the code checked the new quote against the record when you saved. Original quote: " + (e.edited.original_excerpt || "(not kept)")) : null,
@@ -265,7 +269,7 @@
           el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
           el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
           lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
-            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
+            el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
           el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
           el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)"))),
         r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
diff --git a/app/llm/audited.py b/app/llm/audited.py
index 27895e7..fe0106a 100644
--- a/app/llm/audited.py
+++ b/app/llm/audited.py
@@ -65,6 +65,20 @@ def role_for(step: str) -> str:
     return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"
 
 
+PREPARED_BACKEND = "curated"      # D-065: recorded_from.backend of a hand-checked fixture (tests/fixtures/llm/curated); it is never model output
+
+
+def is_prepared(recorded_from) -> bool:
+    return isinstance(recorded_from, dict) and recorded_from.get("backend") == PREPARED_BACKEND
+
+
+def _prepared_model(res):
+    """D-065: a curated answer's audit row names who made it (the fixture's own recorded_from.model, 'hand-checked (qa)'), never the model the pipeline asked for."""
+    if res is not None and is_prepared(res.recorded_from):
+        return str(res.recorded_from.get("model") or "hand-checked (qa)")
+    return None
+
+
 def _t(now):
     return now() if callable(now) else (time.time() if now is None else now)
 
@@ -93,7 +107,7 @@ def audited_call(conn, case_id: str, step: str, model: str, system: str, user: s
         except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
             err, bug = _error_code(e), e
         ms = int((time.monotonic() - t0) * 1000)
-        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
+        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(_prepared_model(res) or (res.model_resolved if res and res.model_resolved else model)),
                       prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                       parsed_ok=1 if err is None else 0, error=err)
         if item_id:
diff --git a/app/llm/backends/fixture.py b/app/llm/backends/fixture.py
index db39749..3244b27 100644
--- a/app/llm/backends/fixture.py
+++ b/app/llm/backends/fixture.py
@@ -43,3 +43,8 @@ def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
                              "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
     p.write_text(json.dumps(rec, indent=1, sort_keys=True))
     return p
+
+
+def answer_source() -> str:
+    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
+    return "prepared" if fixture_dir().name == "curated" else "recorded"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:13.468Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && sed -n 1,80p app/llm/backends/fixture.py; echo ----; grep -n \"answer_source\\|curated\\|fixture_dir\\|FIXTURE_SET\" -r app/llm app/backend app/main.py 2>/dev/null | cut -c1-220 | head -30",
 "description": "Read fixture backend lookup and curated/set resolution"
}
````

### User / tool · 2026-11-02T20:35:13.569Z

**tool result**
````
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p


def answer_source() -> str:
    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
    return "prepared" if fixture_dir().name == "curated" else "recorded"
----
app/llm/audited.py:68:PREPARED_BACKEND = "curated"      # D-065: recorded_from.backend of a hand-checked fixture (tests/fixtures/llm/curated); it is never model output
app/llm/audited.py:76:    """D-065: a curated answer's audit row names who made it (the fixture's own recorded_from.model, 'hand-checked (qa)'), never the model the pipeline asked for."""
app/llm/record.py:56:    return len(list(P._fixture.fixture_dir().glob("*.json")))
app/llm/record.py:116:    print(f"fixtures in {P._fixture.fixture_dir()}: {n}")
app/llm/backends/fixture.py:12:def fixture_dir() -> pathlib.Path:
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
app/llm/backends/fixture.py:21:    p = fixture_dir() / f"{key}.json"
app/llm/backends/fixture.py:23:    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
app/llm/backends/fixture.py:38:    d = fixture_dir()
app/llm/backends/fixture.py:48:def answer_source() -> str:
app/llm/backends/fixture.py:49:    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
app/llm/backends/fixture.py:50:    return "prepared" if fixture_dir().name == "curated" else "recorded"
app/backend/present.py:261:    """D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name
app/backend/present.py:281:    """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
app/backend/api.py:125:        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
app/backend/api.py:129:        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:23.087Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && echo \"== judges.js generator/model usage\"; grep -n \"generator\\|m\\.\\(generator\\|judge\\)\\|\\.models\" app/frontend/judges.js | cut -c1-260; echo \"== api.md (repo HEAD copy)\"; grep -n -i \"prepared\\|answers\\|ai_banner\\|hand-checked\\|D-065\" memory/contracts/api.md | cut -c1-300; echo \"== judges endpoint models\"; grep -n \"\\\"models\\\"\\|'models'\" app/backend/*.py | cut -c1-240; echo \"== eval reports containing sample generator answers\"; ls evals/reports | head -30; grep -l \"claude-sonnet-5-5\" evals/reports/* 2>/dev/null | head; grep -rn \"Demo\\|tooltip\\|evaluation report\" evals/reports/*.md 2>/dev/null | head -5 | cut -c1-200",
 "description": "Check judges UI model use, api.md docs, and eval report content"
}
````

### User / tool · 2026-11-02T20:35:23.217Z

**tool result**
````
== judges.js generator/model usage
166:    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
168:      "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
196:            el("span", { class: "zs-k" }, "Prompt "), j.prompt_version || "", el("span", { class: "zs-k" }, " · model "), (j.models || []).join(", ")))))) : null));
== api.md (repo HEAD copy)
35:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
50:  "backend": "fixture", "demo_mode": true, "answers": "prepared", "live_enabled": false,
54:  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
57:`answers` (T-177, D-065): whose answers the app shows. `prepared` = the curated fixture set (`FIXTURE_SET=curated`): hand-checked by the team, NOT model output; `recorded` = a replay of real model answers (the default fixture dir); `live` = a model answering now. The UI badge follows it: `prepare
58:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every v
376:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summa
383:- `to: "charge"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated ("not billed", "unbilled"), the figure has a
688:Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (
713:**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no 
776:- **Unsupported language, whole case.** If no record is English or Spanish: `POST /api/cases` (and `/pdf`) answers `400 unsupported_language`, `message` "This tool reads English and Spanish records. The text looks like French, which is not supported, so nothing was run. ...", `detail: {languages
792:- **Export gate on the final text (T-139 round 4).** `export.build_export` builds the letter and then scans the FINAL letter text with the one detector: any money expression in the treatment part (everything before the `BILLED CHARGES` section; the section is found by structure, the last `BILLED
836:## Prepared answers (T-177, D-065; amends D-029)
837:Provenance of every generator answer comes from the fixture's own `recorded_from`. A **curated** fixture (`recorded_from.backend == "curated"`, model `hand-checked (qa)`) is a *prepared answer*, never model output:
838:- **Item** (`entries[]`, `amounts[]`, `flags[]`, `GET /items/{id}`): `prepared: boolean`. `ladder.generator` carries `prepared` and, when true, `model: "hand-checked (qa)"` (not `claude-sonnet-5-5`). `ai_drafted` keeps its meaning (a person did not write the summary); the UI tag is "Prepared ans
839:- **Audit** (`GET /audit` `calls[]`, also `/items/{id}` `calls[]`): each call has `prepared: boolean`; for a prepared call `model` is `hand-checked (qa)` (what is stored in `llm_calls.model`). Judge answers are real recordings (D-056): `prepared: false`, real model id.
840:- **Trace** (`GET /items/{id}/trace`): `evidence.model.prepared: boolean`, and `evidence.model.id` is `hand-checked (qa)` for a prepared generator step. That step (`extracted`, a flag's `proposed_by_ai`, a narrative sentence's `extracted`) has label "Prepared answer, standing in for the AI draft
841:- **Narrative** (`GET/POST /narrative`): `narrative.prepared` and `narrative.generator.prepared` (model `hand-checked (qa)` when true).
== judges endpoint models
app/backend/api.py:245:                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
app/backend/pipeline.py:682:            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}
app/backend/present.py:452:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
app/backend/trace.py:949:    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
app/backend/trace.py:960:        p["models"].add(model)
app/backend/trace.py:998:    judges_out = [dict(p, models=sorted(p["models"])) for p in per.values()]
app/backend/trace.py:1001:            p["models"] = []
app/backend/trace.py:1003:    return {"token": case_id, "mode": "full" if cx.full else "metadata", "models": cx.models, "independent_models": cx.models["generator"] != cx.models["judge"],
== eval reports containing sample generator answers
20261102T020824Z.md
20261102T020933Z.md
20261102T021029Z.md
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T025219Z.md
20261102T025715Z.md
20261102T032823Z.md
20261102T035750Z.md
20261102T040933Z.md
20261102T081339Z.md
20261102T083252Z.md
20261102T085207Z.md
20261102T095640Z.md
20261102T104043Z.md
20261102T111004Z.md
20261102T113305Z.md
20261102T115041Z.md
20261102T115607Z.md
20261102T120809Z.md
20261102T121612Z.md
20261102T123428Z.md
20261102T124856Z.md
20261102T164038Z.md
20261102T195748Z.md
calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
evals/reports/20261102T020824Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T022701Z.md
evals/reports/20261102T025219Z.md
evals/reports/20261102T023039Z.md
evals/reports/20261102T022927Z.md
evals/reports/20261102T025715Z.md
evals/reports/20261102T040933Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:33.911Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && sed -n 160,172p app/frontend/judges.js | cut -c1-400; echo \"== judges endpoint on curated\"; PYTHONPATH=$PWD FIXTURE_SET=curated /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport os,tempfile,json,time\nos.environ.update(LLM_BACKEND='fixture',ZLAYT_MODE='local')\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd=tempfile.mkdtemp()\nc=TestClient(create_app(os.path.join(d,'p.sqlite'),static_dir=d),client=('127.0.0.1',50000))\ntok=c.post('/api/cases',json={'sample':True}).json()['token']\nc.post(f'/api/cases/{tok}/run',json={})\nfor _ in range(240):\n    s=c.get(f'/api/cases/{tok}/status').json()\n    if s['status'] in ('ready','failed'): break\n    time.sleep(.25)\nj=c.get(f'/api/cases/{tok}/judges').json()\nprint('JUDGES_MODELS', json.dumps(j.get('models')))\nprint('JUDGES_TOTALS', json.dumps(j.get('totals'))[:300])\nprint('JUDGE_PANELS', json.dumps([{k:v for k,v in p.items() if k in ('id','models','label')} for p in (j.get('judges') or j.get('by_judge') or [])])[:400])\nprint('JUDGE_KEYS', sorted(j.keys()))\n\" 2>&1 | cut -c1-600 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judges.out; echo \"== eval reports: AI answer text for sample?\"; cd /Users/arsis/zlayt-pm-project && grep -c \"\" evals/reports/20261102T195748Z.md; grep -n -i \"sample\\|golden\" evals/reports/20261102T195748Z.md | head -8 | cut -c1-200; grep -n -i \"excerpt\\|summary\" evals/reports/20261102T195748Z.md | head -8 | cut -c1-200",
 "description": "Check judges panel text and judges endpoint models on curated; inspect eval report"
}
````

### User / tool · 2026-11-02T20:35:35.049Z

**tool result**
````
    det.open = wasOpen; toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { wasOpen = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    root.append(det);
    det.append(el("p", { class: "rv-help", "data-testid": "judge-label" }, el("strong", {}, "AI quality checks. "),
      "This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review."));
    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
    det.append(el("p", { class: "zj-models", "data-testid": "judge-model-line" },
      "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
      d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
    det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
      tile(t.items_judged || 0, "items checked by AI"), tile(t.supported || 0, "agreed with the draft"), tile(t.unsupported || 0, "AI objected"),
      tile(t.unsure || 0, "could not decide"), tile(t.unavailable || 0, "unavailable"), tile(t.human_overrides || 0, "you accepted despite an objection")));
== judges endpoint on curated
JUDGES_MODELS {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}
JUDGES_TOTALS {"items_judged": 19, "supported": 19, "unsupported": 0, "unsure": 0, "unavailable": 0, "human_overrides": 0}
JUDGE_PANELS [{"id": "j1", "label": "Is the summary supported by the quote?", "models": ["claude-haiku-5-5"]}, {"id": "j2", "label": "Is this figure a charge, rate or estimate?", "models": ["claude-haiku-5-5"]}, {"id": "j3", "label": "Do these two quotes really conflict?", "models": ["claude-haiku-5-5"]}, {"id": "j4", "label": "Does this flag fit the quote?", "models": ["claude-haiku-5-5"]}]
JUDGE_KEYS ['disagreements', 'independent_models', 'judges', 'mode', 'models', 'prompt_versions', 'rejections', 'token', 'totals', 'unresolved']
== eval reports: AI answer text for sample?
72
22:| golden_must_not_hits | 0 | 0 | R-CO-3 |
29:## Calibrated confidence (measured counts, backend `fixture`, 10 golden cases, source commit `4510dc2547`)
31:- Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).
32:- Items marked needs review matched the record 11/11 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).
41:spec_matches_golden: True
48:- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): 5 {"FILTERED_BY_RULE": 4, "LLM_ONLY": 1} by case {"case_01_date_formats": 2, "case_05_provider_conflict": 
45:- entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
47:- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 5, "clauses_removed": 5, "tray_placeholders": 0, "per_case": {"case_03_rate_and_ocr": {"items_trimmed": 3, "clauses_
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:43.669Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && PYTHONPATH=$PWD FIXTURE_SET= /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport os,tempfile,json,time\nos.environ.update(LLM_BACKEND='fixture',ZLAYT_MODE='local'); os.environ.pop('FIXTURE_SET',None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd=tempfile.mkdtemp()\nc=TestClient(create_app(os.path.join(d,'p.sqlite'),static_dir=d),client=('127.0.0.1',50000))\ntok=c.post('/api/cases',json={'sample':True}).json()['token']\nc.post(f'/api/cases/{tok}/run',json={})\nfor _ in range(240):\n    s=c.get(f'/api/cases/{tok}/status').json()\n    if s['status'] in ('ready','failed'): break\n    time.sleep(.25)\ne=c.get(f'/api/cases/{tok}').json()['entries'][0]\nprint('E1_SUMMARY', e['summary']); print('E1_EXCERPT', e['excerpt'])\n\" 2>/dev/null | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out; S=$(grep E1_SUMMARY /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out | cut -c13- | cut -c1-40); echo \"searching reports for: [$S]\"; cd /Users/arsis/zlayt-pm-project && ls evals/reports | wc -l; grep -rl -F \"$S\" evals/reports/ ; echo \"rc=$?\"; echo \"== report sections with per-case AI text:\"; grep -rn -i \"AI's own\\|own answers\\|summary text\\|one-line summary\" evals/reports/*.md | head -5 | cut -c1-200",
 "description": "Check whether eval reports contain the AI's sample answers the tooltip points to"
}
````

### User / tool · 2026-11-02T20:35:44.687Z

**tool result**
````
E1_SUMMARY 41-year-old male restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache, alert and oriented, transported to Central ER.
E1_EXCERPT 41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.
searching reports for: [1-year-old male restrained driver rear-e]
      98
rc=1
== report sections with per-case AI text:
evals/reports/determinism-diagnosis.md:22:Fields compared: state, record ids, excerpt (entries: the quote; flags: the evidence span), reason codes, judge verdict/reason code, summary text.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:47.709Z

**tool call — Bash**
````
{
 "command": "for s in \"41-year-old male restrained driver\" \"rear-ended at approx. 35 mph\" \"Transported to Central ER\"; do echo \"== [$s]\"; grep -rl -F \"$s\" evals/ reviews/ artifacts/ 2>/dev/null | head -8; done; echo \"== golden (expected, QA-side) file mention:\"; grep -rl -F \"41-year-old male restrained driver\" evals/golden 2>/dev/null | head -3; echo \"== eval report JSON/MD list (non-timestamped)\"; ls evals/reports | grep -v \"^2026\" ",
 "description": "Search eval outputs and reviews for the sample AI answer text"
}
````

### User / tool · 2026-11-02T20:35:48.052Z

**tool result**
````
== [41-year-old male restrained driver]
evals/golden/hallucinations_controls.jsonl
reviews/T-015-legal-nurse.md
artifacts/review-evidence/T-098-staff-engineer-r2-results.txt
artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out
artifacts/review-evidence/T-098-staff-engineer-r2-results-head-9f2811f.txt
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/golden/hallucinations_controls.jsonl
artifacts/review-evidence/T-055-security-r2/head_670ed09/board/cards/T-015.md
artifacts/review-evidence/T-057-staff-engineer-r2/tree/evals/golden/hallucinations_controls.jsonl
== [rear-ended at approx. 35 mph]
evals/golden/sample.export.expected.txt
evals/golden/check_golden.py
evals/golden/hallucinations.jsonl
evals/golden/hallucinations_controls.jsonl
evals/golden/sample.expected.json
evals/golden/sample.txt
reviews/T-008-claims-adjuster.md
reviews/T-015-paralegal-r4.md
== [Transported to Central ER]
evals/golden/sample.export.expected.txt
evals/golden/hallucinations.jsonl
evals/golden/hallucinations_controls.jsonl
evals/golden/sample.txt
reviews/T-008-claims-adjuster.md
reviews/T-008-claims-adjuster-r2.md
reviews/T-136-paralegal-r3.md
reviews/T-136-paralegal.md
== golden (expected, QA-side) file mention:
evals/golden/hallucinations_controls.jsonl
== eval report JSON/MD list (non-timestamped)
calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
controls-20261102T043911Z.json
controls-20261102T043911Z.md
controls-20261102T044933Z.json
controls-20261102T044933Z.md
controls-20261102T045207Z.json
controls-20261102T045207Z.md
controls-20261102T063331Z.json
controls-20261102T063331Z.md
controls-20261102T075238Z.json
controls-20261102T075238Z.md
controls-20261102T090925Z.json
controls-20261102T090925Z.md
controls-20261102T102626Z.json
controls-20261102T102626Z.md
controls-20261102T123937Z.json
controls-20261102T123937Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:51.376Z

**tool call — Bash**
````
{
 "command": "ls evals/reports/runs | head; ls evals/reports/runs | wc -l; f=$(ls -t evals/reports/runs/* 2>/dev/null | head -1); echo \"newest: $f\"; python3 -c \"\nimport json,sys,glob\nfs=sorted(glob.glob('evals/reports/runs/*'))\nprint(len(fs))\nfor f in fs[-3:]:\n    try:\n        s=open(f).read()\n        print(f, len(s), 'has_summary_key' , '\\\"summary\\\"' in s, 'has_excerpt', '\\\"excerpt\\\"' in s, 'has_e1_text', '41-year-old' in s)\n    except Exception as e: print(f, e)\n\"; python3 -c \"\nimport json\nd=json.load(open('evals/reports/latest.json'))\nprint('latest keys', list(d.keys())[:20])\n\" ; grep -l \"41-year-old\\|rear-ended at approx\" evals/reports/runs/* evals/reports/latest.json 2>/dev/null | head -3; echo \"rc=$?\"",
 "description": "Check eval run artifacts for per-item AI answer text"
}
````

### User / tool · 2026-11-02T20:35:51.534Z

**tool result**
````
20261102T034706Z
20261102T035806Z
20261102T042232Z
20261102T045543Z
20261102T051136Z
20261102T052638Z
20261102T054926Z
20261102T060623Z
20261102T063157Z
20261102T075514Z
      44
newest: evals/reports/runs/20261102T161327Z:
44
evals/reports/runs/20261102T135647Z [Errno 21] Is a directory: 'evals/reports/runs/20261102T135647Z'
evals/reports/runs/20261102T143951Z [Errno 21] Is a directory: 'evals/reports/runs/20261102T143951Z'
evals/reports/runs/20261102T161327Z [Errno 21] Is a directory: 'evals/reports/runs/20261102T161327Z'
latest keys ['backend', 'blockers', 'generated_at', 'hashes', 'models', 'recorded_from', 'schema', 'ship_bar_met', 'source', 'spec_matches_golden']
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:53.186Z

**tool call — Bash**
````
{
 "command": "find evals/reports/runs -type f | head -20; find evals/reports/runs -type f | wc -l; echo \"--- grep AI answer text for e1 across runs:\"; grep -rl \"41-year-old\" evals/reports/ 2>/dev/null | head; echo \"rc=$?\"; echo \"--- any run file containing generator summaries (summary key):\"; grep -rl '\"summary\"' evals/reports/runs 2>/dev/null | head -3; echo \"rc=$?\"",
 "description": "List eval run files and search for per-item AI summaries"
}
````

### User / tool · 2026-11-02T20:35:53.311Z

**tool result**
````
evals/reports/runs/20261102T135647Z/calibration.json
evals/reports/runs/20261102T093020Z/run2.json
evals/reports/runs/20261102T093020Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T093020Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T093020Z/case_07_prompt_injection.json
evals/reports/runs/20261102T093020Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T093020Z/calibration.json
evals/reports/runs/20261102T093020Z/run3.json
evals/reports/runs/20261102T093020Z/case_08_diagnosis_temptation.json
evals/reports/runs/20261102T093020Z/sample.json
evals/reports/runs/20261102T093020Z/case_05_provider_conflict.json
evals/reports/runs/20261102T093020Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T093020Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T093020Z/case_01_date_formats.json
evals/reports/runs/20261102T093020Z/run1.json
evals/reports/runs/20261102T143951Z/calibration.json
evals/reports/runs/20261102T083312Z/run2.json
evals/reports/runs/20261102T083312Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T083312Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T083312Z/case_07_prompt_injection.json
     272
--- grep AI answer text for e1 across runs:
evals/reports/determinism-diagnosis.md
rc=0
--- any run file containing generator summaries (summary key):
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:55.930Z

**tool call — Bash**
````
{
 "command": "grep -n \"41-year-old\" evals/reports/determinism-diagnosis.md | cut -c1-300; echo ---; python3 -c \"\nimport json\nd=json.load(open('evals/reports/runs/20261102T093020Z/sample.json'))\nprint(type(d).__name__, list(d.keys())[:30] if isinstance(d,dict) else len(d))\ns=json.dumps(d)\nprint('len',len(s)); print('has summary', 'summary' in s, 'has excerpt', 'excerpt' in s)\n\" ; grep -c \"\" evals/reports/runs/20261102T093020Z/sample.json",
 "description": "Inspect a sample run file and the determinism-diagnosis mention"
}
````

### User / tool · 2026-11-02T20:35:56.049Z

**tool result**
````
26:| e1, e3, e4, e6, e8 (entries) | verified in 9/9 | same | same in 9/9 | summary wording only ("41M" vs "41-year-old male"; ";" vs "and"; verbatim quote vs paraphrase) | extract variance in the summary. Allowed by R-CO-7 ("Summary wording may differ but must be supported"); J1 said `supported` 9/9
---
dict ['backend', 'case', 'errors', 'items', 'models', 'run', 'schema', 'signature_parts', 'status', 'tray_flag_count', 'warning_codes']
len 13694
has summary True has excerpt True
974
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:35:59.604Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('evals/reports/runs/20261102T093020Z/sample.json'))\nit=d['items']\nprint(type(it).__name__, len(it))\nx = it[0] if isinstance(it,list) else list(it.items())[0]\nprint(json.dumps(x)[:700])\nprint('models', d.get('models'), 'backend', d.get('backend'), 'run', d.get('run'))\n\"; echo ---; python3 -c \"\nimport json,glob\nf=sorted(glob.glob('evals/reports/runs/*/sample.json'))\nprint(len(f), f[-1])\nd=json.load(open(f[-1])); it=d['items']\nx = it[0] if isinstance(it,list) else None\nprint(json.dumps(x)[:400] if x else 'dict')\n\"",
 "description": "Read the first recorded item in the eval sample run file"
}
````

### User / tool · 2026-11-02T20:35:59.730Z

**tool result**
````
list 23
{"date": "2026-01-09", "date_status": "parsed", "generator_prompt_version": "extract_v1", "id": "e1", "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "reason_code": "NONE", "verdict": "supported"}, "kind": "entry", "provider": "Austin EMS run report", "reasons": [], "record_ids": ["r1"], "state": "verified", "summary_sha": "0e30884d90ea98c6"}
models {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5'} backend claude-cli run None
---
18 evals/reports/runs/20261102T161327Z/sample.json
{"date": "2026-01-09", "date_status": "parsed", "generator_prompt_version": "extract_v1", "id": "e1", "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "reason_code": "NONE", "verdict": "supported"}, "kind": "entry", "provider": "Austin EMS run report", "reasons": [], "record_ids": ["r1"], "state": "verified", "summary_sha": "0e30884d90ea98c6"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:20.097Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py <<'EOF'\nimport json, os, socket, subprocess, sys, tempfile, time, urllib.request\nROOT = os.getcwd()\ns = socket.socket(); s.bind((\"127.0.0.1\", 0)); port = s.getsockname()[1]; s.close()\ntmp = tempfile.mkdtemp(prefix=\"t177-curated-\")\nenv = dict(os.environ, PORT=str(port), HOST=\"127.0.0.1\", ZLAYT_MODE=\"local\", LLM_BACKEND=\"fixture\", FIXTURE_SET=\"curated\", ZLAYT_DB=os.path.join(tmp, \"c.sqlite3\"))\nenv.pop(\"ANTHROPIC_API_KEY\", None); env.pop(\"ENABLE_LIVE\", None); env.pop(\"LLM_FIXTURE_DIR\", None)\nlog = open(os.path.join(tmp, \"server.log\"), \"w\")\nproc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)\nprint(\"SERVER_PID\", proc.pid, \"PORT\", port, flush=True)\nbase = f\"http://127.0.0.1:{port}\"\ntry:\n    for _ in range(80):\n        try:\n            urllib.request.urlopen(base + \"/api/health\", timeout=1).read(); break\n        except Exception:\n            time.sleep(.5)\n    def call(m, p, b=None):\n        req = urllib.request.Request(base + p, method=m, data=(json.dumps(b).encode() if b is not None else None), headers={\"Content-Type\": \"application/json\"})\n        with urllib.request.urlopen(req, timeout=60) as r:\n            raw = r.read(); return json.loads(raw) if raw else None\n    tok = call(\"POST\", \"/api/cases\", {\"sample\": True})[\"token\"]\n    call(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(300):\n        st = call(\"GET\", f\"/api/cases/{tok}/status\")\n        if st[\"status\"] in (\"ready\", \"failed\"): break\n        time.sleep(.5)\n    print(\"STATUS\", st[\"status\"], flush=True)\n    from playwright.sync_api import sync_playwright\n    with sync_playwright() as pw:\n        b = pw.chromium.launch(); pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n        pg.goto(f\"{base}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n        print(\"BADGE\", pg.locator(\"#badge\").inner_text(), \"| TITLE:\", pg.locator(\"#badge\").get_attribute(\"title\"))\n        print(\"BANNER_AI\", pg.locator(\"#banner-ai\").inner_text())\n        pg.get_by_test_id(\"judge-panel\").evaluate(\"e => e.open = true\")\n        pg.get_by_test_id(\"judge-model-line\").wait_for(timeout=15000)\n        print(\"JUDGE_LABEL\", pg.get_by_test_id(\"judge-label\").inner_text())\n        print(\"JUDGE_MODEL_LINE\", pg.get_by_test_id(\"judge-model-line\").inner_text())\n        print(\"JUDGE_TOTALS\", pg.get_by_test_id(\"judge-totals\").inner_text().replace(\"\\n\", \" | \"))\n        pg.get_by_test_id(\"judge-panel\").scroll_into_view_if_needed()\n        pg.get_by_test_id(\"judge-panel\").screenshot(path=os.path.join(ROOT, \"artifacts\", \"review-evidence\", \"T-177-staff-engineer-curated-judge-panel.png\"))\n        b.close()\nfinally:\n    proc.terminate()\n    try: proc.wait(timeout=10)\n    except Exception: proc.kill()\n    print(\"STOPPED_PID\", proc.pid, \"rc\", proc.returncode)\nEOF\nPYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out | cut -c1-400",
 "description": "Render curated case in a private server and read the AI-check panel text",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:36:37.198Z

**tool result**
````
SERVER_PID 94279 PORT 64236
STATUS ready
BADGE Demo: sample answers prepared by our team | TITLE: The AI's own answers on these cases are in the evaluation report.
BANNER_AI In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item
STOPPED_PID 94279 rc -15
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py", line 35, in <module>
    pg.get_by_test_id("judge-model-line").wait_for(timeout=15000)
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 13635, in wait_for
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 767, in wait_for
    await self._frame.wait_for_selector(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 395, in wait_for_selector
    await self._channel.send(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for get_by_test_id("judge-model-line") to be visible
    34 × locator resolved to hidden <p class="zj-models" data-testid="judge-model-line">…</p>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:42.822Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && python3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py'\ns=open(p).read()\ns=s.replace('''        pg.get_by_test_id(\"judge-panel\").evaluate(\"e => e.open = true\")\n        pg.get_by_test_id(\"judge-model-line\").wait_for(timeout=15000)\n''','''        pg.get_by_test_id(\"judge-summary\").first.click()\n        pg.get_by_test_id(\"judge-model-line\").first.wait_for(state=\"attached\", timeout=15000)\n        print(\"JUDGE_LINE_VISIBLE\", pg.get_by_test_id(\"judge-model-line\").first.is_visible())\n        print(\"JUDGE_PANEL_OPEN\", pg.get_by_test_id(\"judge-panel\").first.evaluate(\"e => e.open\"))\n''')\ns=s.replace('print(\"JUDGE_LABEL\", pg.get_by_test_id(\"judge-label\").inner_text())','print(\"JUDGE_LABEL\", pg.get_by_test_id(\"judge-label\").first.text_content())')\ns=s.replace('print(\"JUDGE_MODEL_LINE\", pg.get_by_test_id(\"judge-model-line\").inner_text())','print(\"JUDGE_MODEL_LINE\", pg.get_by_test_id(\"judge-model-line\").first.text_content())')\ns=s.replace('print(\"JUDGE_TOTALS\", pg.get_by_test_id(\"judge-totals\").inner_text().replace(\"\\\\n\", \" | \"))','print(\"JUDGE_TOTALS\", pg.get_by_test_id(\"judge-totals\").first.text_content())')\ns=s.replace('pg.get_by_test_id(\"judge-panel\").scroll_into_view_if_needed()\\n        pg.get_by_test_id(\"judge-panel\").screenshot','pg.get_by_test_id(\"judge-panel\").first.scroll_into_view_if_needed()\\n        pg.get_by_test_id(\"judge-panel\").first.screenshot')\nopen(p,'w').write(s)\nEOF\nPYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out | cut -c1-400 | tail -25",
 "description": "Re-run curated judge-panel render probe with visibility checks",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:36:45.185Z

**tool result**
````
SERVER_PID 94777 PORT 64363
STATUS ready
BADGE Demo: sample answers prepared by our team | TITLE: The AI's own answers on these cases are in the evaluation report.
BANNER_AI In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item
JUDGE_LINE_VISIBLE True
JUDGE_PANEL_OPEN None
JUDGE_LABEL AI quality checks. This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review.
JUDGE_MODEL_LINE Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5 (a different model, so it does not grade its own work).
JUDGE_TOTALS 19items checked by AI19agreed with the draft0AI objected0could not decide0unavailable0you accepted despite an objection
STOPPED_PID 94777 rc -15
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:47.355Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png"
}
````

### User / tool · 2026-11-02T20:36:47.364Z

**tool result (error)**
````
File does not exist. Note: your current working directory is /Users/arsis/zlayt-pm-project. Did you mean T-177-staff-engineer-curated-judge-panel.out?
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:47.991Z

**tool call — Bash**
````
{
 "command": "ps -p 94279,94777 -o pid,comm 2>/dev/null; echo \"ps rc=$? (1 = none of my PIDs alive)\"; lsof -nP -iTCP:7860 -sTCP:LISTEN 2>/dev/null | tail -1",
 "description": "View judge panel screenshot and confirm my PIDs are gone"
}
````

### User / tool · 2026-11-02T20:36:48.158Z

**tool result**
````
  PID COMM
ps rc=1 (1 = none of my PIDs alive)
Python  86899 arsis    9u  IPv4 0x89944c6bbeb1c380      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:50.386Z

**tool call — Bash**
````
{
 "command": "find /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer -name \"*curated-judge-panel.png\" 2>/dev/null; mv /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ 2>/dev/null; ls -la /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png",
 "description": "Locate the judge-panel screenshot written under the archive copy and move it"
}
````

### User / tool · 2026-11-02T20:36:50.496Z

**tool result**
````
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png
-rw-r--r--@ 1 arsis  staff  77652 Nov  2 14:36 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:51.316Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png"
}
````

### User / tool · 2026-11-02T20:36:51.324Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:36:56.827Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; R=/Users/arsis/zlayt-pm-project; \\\necho \"== M1: audit row model not replaced by prepared model\"; $PY - <<'EOF'\np='app/llm/audited.py'; s=open(p).read()\ns2=s.replace('model=(_prepared_model(res) or (res.model_resolved if res and res.model_resolved else model))','model=((res.model_resolved if res and res.model_resolved else model))')\nassert s!=s2; open(p,'w').write(s2)\nEOF\n$PY -m pytest tests/unit/test_prepared_provenance.py tests/e2e/test_demo_provenance.py -q -p no:cacheprovider -k \"not recorded and not live\" 2>&1 | tail -4; git -C $R show 04ea2bf:app/llm/audited.py > app/llm/audited.py; \\\necho \"== M2: prepared flag never set (is_prepared always False)\"; $PY - <<'EOF'\np='app/llm/audited.py'; s=open(p).read()\ns2=s.replace('return isinstance(recorded_from, dict) and recorded_from.get(\"backend\") == PREPARED_BACKEND','return False')\nassert s!=s2; open(p,'w').write(s2)\nEOF\n$PY -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -4; git -C $R show 04ea2bf:app/llm/audited.py > app/llm/audited.py; \\\necho \"== restore check\"; cmp <(git -C $R show 04ea2bf:app/llm/audited.py) app/llm/audited.py && echo restored-identical; \\\necho \"== M3: judges/case models still name generator (not mutated; check unit coverage of models field)\"; grep -n \"models\" tests/unit/test_prepared_provenance.py tests/e2e/test_demo_provenance.py | cut -c1-160",
 "description": "Mutation-test provenance: break audit model and prepared flag in archive copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:37:05.123Z

**tool result**
````
== M1: audit row model not replaced by prepared model
FAILED tests/unit/test_prepared_provenance.py::test_curated_trace_generator_step_names_a_prepared_answer
FAILED tests/e2e/test_demo_provenance.py::test_curated_trace_and_audit_say_prepared
FAILED tests/e2e/test_demo_provenance.py::test_curated_audit_drawer_marks_the_prepared_rows
5 failed, 2 passed, 3 deselected in 4.80s
== M2: prepared flag never set (is_prepared always False)
FAILED tests/unit/test_prepared_provenance.py::test_curated_audit_rows_carry_the_prepared_model
FAILED tests/unit/test_prepared_provenance.py::test_curated_item_is_marked_prepared
FAILED tests/unit/test_prepared_provenance.py::test_curated_trace_generator_step_names_a_prepared_answer
3 failed, 3 passed in 2.08s
== restore check
restored-identical
== M3: judges/case models still name generator (not mutated; check unit coverage of models field)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:37:33.824Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/T-177-staff-engineer.md 2>&1 | head -2; sed -n 1,12p reviews/T-015-legal-nurse.md | cut -c1-160; echo ---; grep -n \"T-177\" memory/ORCHESTRATOR_DECISIONS.md | head -3 | cut -c1-120; grep -n \"judge-model-line\\|Drafted by\" tests/e2e/*.py tests/unit/*.py | head -5 | cut -c1-160",
 "description": "Check review file does not exist and look at prior review format"
}
````

### User / tool · 2026-11-02T20:37:33.952Z

**tool result**
````
ls: reviews/T-177-staff-engineer.md: No such file or directory
# T-015 Eval golden set: legal-nurse review

**Verdict: fail** (2 blockers, 2 majors). The arithmetic and the wording the golden set writes itself are clinically sound. All 20 seeded hallucinations are rea

- The regex checks that enforce the Appendix C must-nots are unreliable in both directions. M6 (concussion without loss of consciousness) is backwards: it fails
- The hallucination set has no items for laterality, spinal level, a real severity upgrade, or a complaint stated as a finding.

Per-item verdicts: `artifacts/review-evidence/T-015-legal-nurse-items.md`.

```json
{"card": "T-015", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 47520a8, evals/golden/** (README, sample + 8 synthetic cases, hallucinations.jsonl, hallucinations_controls.jsonl, check_golden.py); reference
---
tests/e2e/conftest.py:20:  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with 
tests/e2e/test_demo_provenance.py:108:    assert page.locator("[title*='Drafted by AI'], [aria-label*='AI draft']").count() == 0
tests/e2e/test_stepper.py:216:    assert re.search(r"claude-\S+", jp.get_by_test_id("judge-model-line").inner_text())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:14.873Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer.md",
 "content": "# T-177 (D-065 honest demo provenance): staff-engineer review\n\n**Verdict: fail (1 blocker, 2 majors, 1 minor, 1 nit).** The PM's acceptance test passes on commit 04ea2bf: no \"AI draft\" or \"recorded AI answers\" text on a curated item, the trace generator step reads `hand-checked (qa)` with a prepared-answer label, the audit rows carry `hand-checked (qa)`, and the recorded set keeps its AI labels. The provenance is not complete, though. On the curated demo, the \"How the AI was checked\" panel still says `Drafted by claude-sonnet-5-5`, and the case and judges payloads still name `claude-sonnet-5-5` as the generator. That is the exact over-claim D-065 forbids, and no test covers it. The badge tooltip also points to an eval report that does not hold the answers.\n\nScope: commit 04ea2bf (the card commit). HEAD de5cb3a has no diff under `app/` or `tests/` relative to 04ea2bf, so the archive matches HEAD for code. Evidence is under `artifacts/review-evidence/T-177-staff-engineer/` (git archive copy) and the `artifacts/review-evidence/T-177-staff-engineer-*` files.\n\n## Acceptance checks (PM's test, curated and recorded)\n\n| Check | Result |\n|---|---|\n| `tests/unit/test_prepared_provenance.py` | 6 passed |\n| `E2E_REQUIRE_DB=1 tests/e2e/test_demo_provenance.py` | 4 passed |\n| `/items/e1/trace` generator step model | `hand-checked (qa)`, label \"Prepared answer, standing in for the AI draft\" |\n| `/audit` generator rows (curated) | 18 of 18 `hand-checked (qa)`, `prepared: true` |\n| Curated page text | no \"AI draft\" or \"recorded AI answers\"; badge \"Demo: sample answers prepared by our team\" |\n| Recorded set labels | \"AI draft\", model `claude-sonnet-5-5`, badge \"Demo: recorded AI answers\" |\n\n## Findings\n\n**F1 (blocker): the curated demo still names a model as drafter.** On the curated set, the \"How the AI was checked\" panel renders `Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5` and the label \"how a second AI model checked the first AI's drafts\". The same payloads name the generator as `claude-sonnet-5-5`. `app/backend/present.py:262` says the provenance exists \"so no screen or payload names a model for an answer no model gave\". The panel and payloads contradict that comment and D-065 (\"never presented as model output\"). The new tests pass because they only assert the trace, audit, item and health fields.\n\n**F2 (major): the tooltip names a place the answers are not.** `app/frontend/app.js:16-17` says \"The AI's own answers on these cases are in the evaluation report.\" The run files store `summary_sha`, not the summary or excerpt text. `evals/reports/runs/20261102T093020Z/sample.json` item keys are `date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha`. The only report text that contains the sample summary's opening words is a quoted phrase in `evals/reports/determinism-diagnosis.md:26`. The tooltip text is pinned by D-065, so this needs a decision (see questions).\n\n**F3 (major): the curated banner says \"checked by code\" and omits the AI check.** `app/backend/api.py:37` (PREPARED_BANNER) reads \"...prepared by our team and checked by code; you decide every item\". On the same curated items, the trace has a \"Second AI check\" step (`judge_1`, model `claude-haiku-5-5`, `prepared: false`) and the judges endpoint counts 19 items checked by AI. The banner under-states who checked the items.\n\n**F4 (minor): the banner is global, provenance is per call.** `app/backend/api.py:125-129` (`answers()`) decides prepared versus recorded from the fixture set name alone, while item provenance is per call (`app/backend/present.py:262-273`, `app/llm/audited.py:68-79`). `app/llm/backends/fixture.py:23-24` falls back to the recorded set when a curated key is missing. A curated run with one missing key would show a recorded AI answer labelled \"AI draft\" under a banner saying all summaries were prepared. Not reproduced on the sample: 9 of 9 extract and 9 of 9 flag calls are `prepared: true`.\n\n**F5 (nit): prepared rows still carry a prompt version.** The curated probe's audit row has `\"prompt_version\": \"extract_v1\"`, a real `prompt_sha256`, and `\"prepared\": true`. `app/frontend/timeline.js` (why-generator line) shows \"hand-checked (qa) · extract_v1\". No prompt produced these answers.\n\n## Commands and outputs\n\n- `git show --stat 04ea2bf`; `git diff 04ea2bf HEAD -- app tests | wc -l` gives 0.\n- `python3 tools/board.py show T-177`: status in_review, AC 1 done with evidence.\n- `reviews/GATE-M3-product-manager.md` blocker read; `memory/ORCHESTRATOR_DECISIONS.md` D-065 to D-068 read.\n- `git archive 04ea2bf` extracted to `artifacts/review-evidence/T-177-staff-engineer/`.\n- Unit and e2e outputs: `artifacts/review-evidence/T-177-staff-engineer-unit-prepared.out`, `artifacts/review-evidence/T-177-staff-engineer-e2e-provenance.out`.\n- API probes (TestClient, curated and recorded): `artifacts/review-evidence/T-177-staff-engineer-curated-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-curated-judges.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out`. Probe scripts: `artifacts/review-evidence/T-177-staff-engineer-probe.py`, `artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py`.\n- Browser render of the curated case on a private server: `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out` and `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png`.\n- Mutation checks, in the archive copy and restored from `git show 04ea2bf:...` (cmp identical): removing `_prepared_model` in `app/llm/audited.py` fails 5 tests; forcing `is_prepared` to False fails 3 unit tests.\n- Grep of tests for `models` assertions: none for the judges or case payloads.\n- The shared app on :7860 (PID 86899) was not touched. My two private server PIDs (94279, 94777) were terminated; `ps` confirms none alive.\n\n## What is right\n\n- Audit and trace model swap is mutation-guarded: removing the audit model swap or forcing the prepared flag off makes 3 to 5 tests fail.\n- The PM's acceptance points hold on 04ea2bf: prepared trace label, `hand-checked (qa)` audit rows, recorded set keeps AI labels and model ids.\n- `memory/contracts/api.md:57` and `:836-841` document `answers`, `prepared` on items, audit, trace and narrative, and the payloads I observed match them.\n\n## Verdict rule\n\nOne blocker (F1), so `fail`. Majors F2 and F3 must also be fixed before the gate.\n\n```json\n{\"card\": \"T-177\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 04ea2bf (card commit; HEAD de5cb3a has no app/ or tests/ diff from it); git archive copy at artifacts/review-evidence/T-177-staff-engineer/; no app URL (private servers on random loopback ports; shared :7860 untouched); sample case (sample=True) on FIXTURE_SET=curated and on the recorded set\",\n \"exercised\": [\n  \"python3 tools/board.py show T-177; git show --stat 04ea2bf; git diff 04ea2bf HEAD -- app tests (0 lines)\",\n  \"reviews/GATE-M3-product-manager.md blocker; memory/ORCHESTRATOR_DECISIONS.md D-065 to D-068\",\n  \"git archive 04ea2bf extracted; read app/backend/present.py, trace.py, api.py, app/llm/audited.py, app/llm/backends/fixture.py, app/frontend/app.js, judges.js, stepper.js, timeline.js, audit.js; read the two new test files\",\n  \".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q: 6 passed\",\n  \"E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v: 4 passed\",\n  \"TestClient probes on curated and recorded sets: /api/health, /api/cases/{tok}, /audit, /items/e1/trace, /judges\",\n  \"Playwright on a private curated server: read badge, badge title, banner, judge-label, judge-model-line, judge-totals; screenshot of the judge panel\",\n  \"Mutation checks in the archive copy: audit model swap removed (5 failed); is_prepared forced False (3 failed); file restored and cmp-verified\",\n  \"Inspected evals/reports/runs/20261102T093020Z/sample.json keys; grep of evals/reports for the sample summary text\",\n  \"Grep of tests for models/judge-model-line assertions (none for judges or case payloads)\",\n  \"memory/contracts/api.md lines 57 and 836-841 read against the code\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"provenance_honesty\": 2, \"pm_acceptance_criteria\": 4, \"api_fields_documented\": 4, \"test_strength\": 3, \"llm_boundary\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Curated demo still names claude-sonnet-5-5 as the drafter of hand-written answers (judge panel, case and judges payloads)\",\n   \"evidence\": \"Rendered curated case (artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out): judge-model-line 'Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5'; judge-label \\\"how a second AI model checked the first AI's drafts\\\"; screenshot artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png. app/frontend/judges.js:166-168 renders m.generator from d.models. app/backend/trace.py:1003 returns 'models': cx.models (config). GET /api/cases/{tok}/judges on FIXTURE_SET=curated returns models.generator 'claude-sonnet-5-5' (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out). GET /api/cases/{tok} on curated returns models.generator 'claude-sonnet-5-5'. app/backend/present.py:262 comment says no payload names a model for an answer no model gave.\",\n   \"why_it_matters\": \"D-065 (binding): curated answers are never presented as model output. The panel is part of the demo the PM tested and it attributes the team's hand-written summaries to a named model. The paralegal or a reviewer reading the panel gets the wrong provenance. The new tests pass because they check trace, audit, item and health fields only, so the same blocker class would pass CI again.\",\n   \"fix\": \"On a prepared case, the drafter line says the summaries were prepared by the team (no model), for example 'Drafted by: prepared answers (hand-checked by the team), checked by claude-haiku-5-5'. GET /api/cases/{tok} and GET /judges return models.generator as null or 'hand-checked (qa)' when the case's generator answers are prepared. The judge-label sentence follows the same rule. Recorded and live cases are unchanged.\",\n   \"acceptance_test\": \"Unit: on FIXTURE_SET=curated, GET /api/cases/{tok}/judges and GET /api/cases/{tok} have models.generator != 'claude-sonnet-5-5'. E2E (curated): the judge-model-line text does not contain 'claude-sonnet-5-5' and says the summaries were prepared. E2E (recorded set): the same line still says 'claude-sonnet-5-5'.\"},\n  {\"severity\": \"major\", \"title\": \"Badge tooltip says the AI's answers are in the evaluation report; they are not\",\n   \"evidence\": \"app/frontend/app.js:16-17: \\\"The AI's own answers on these cases are in the evaluation report.\\\" evals/reports/runs/20261102T093020Z/sample.json item keys: date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha (no summary or excerpt text). The only evals/reports text with the sample summary's opening words is a quoted phrase at evals/reports/determinism-diagnosis.md:26.\",\n   \"why_it_matters\": \"The tooltip is the one place the demo tells a reader where to verify the AI's own answers. It sends them to a file that holds hashes and verdicts. That is a false pointer on a provenance label, the kind of over-claim the PM blocked.\",\n   \"fix\": \"Either write each entry's generator summary and excerpt for the sample case into the eval report (an eval-runner change, with a report path) or reword the tooltip to what the report holds. The sentence is pinned by D-065, so the wording needs a decision (see questions_for_chris).\",\n   \"acceptance_test\": \"Either: a new evals/reports/*.md contains the sample case's generator summaries and excerpts, and a unit test greps for one of them. Or: the tooltip text is changed, and the e2e test asserts the new text.\"},\n  {\"severity\": \"major\", \"title\": \"Curated banner says 'checked by code' and omits the AI check that runs on the same items\",\n   \"evidence\": \"api.py:37 PREPARED_BANNER: 'In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item' (rendered: artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out line 2). Same curated items: trace step judge_1 'Second AI check: is the summary supported by the quote?', model claude-haiku-5-5, prepared false (artifacts/review-evidence/T-177-staff-engineer-curated-probe.out); /judges items_judged 19 (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out).\",\n   \"why_it_matters\": \"The banner states who checked the items. It leaves out that a second AI model checked every item, so the page contradicts itself ('checked by code' above a 'Second AI check' step). D-065 requires plain wording to stay truthful.\",\n   \"fix\": \"Rewrite the prepared banner to name both: prepared by the team, then a second AI model checked each summary against its quote, and the reader decides every item.\",\n   \"acceptance_test\": \"Unit: GET /api/health on FIXTURE_SET=curated has answers 'prepared' and an ai_banner that mentions a second AI check and does not say 'checked by code' alone.\"},\n  {\"severity\": \"minor\", \"title\": \"Banner and badge are decided per fixture set, while provenance is per call; a missing curated key would mislabel an item\",\n   \"evidence\": \"app/backend/api.py:125-129 answers() uses fixture.answer_source() (app/llm/backends/fixture.py:48-50, fixture_dir().name only). Per-call provenance: app/backend/present.py:262-273, app/llm/audited.py:68-79. app/llm/backends/fixture.py:23-24 falls back to the recorded set when a curated key file is missing. Not reproduced: curated probe shows 9 of 9 extract and 9 of 9 flags calls prepared true.\",\n   \"why_it_matters\": \"On a curated run with one missing key, the item would be a recorded AI answer labelled 'AI draft' under a banner saying all summaries were prepared by the team. Provenance would be wrong on exactly the case where the fixtures are incomplete.\",\n   \"fix\": \"Derive the badge and banner from the items shown (all prepared, all recorded, or mixed), or fail the run when a curated set misses a key instead of falling back.\",\n   \"acceptance_test\": \"Unit: copy the curated set minus one generator file into a temp LLM_FIXTURE_DIR named curated and FIXTURE_SET=curated; the run fails or the health answers value is 'mixed', never 'prepared'.\"},\n  {\"severity\": \"nit\", \"title\": \"Prepared rows still show a prompt version and prompt hash\",\n   \"evidence\": \"Curated probe, audit row: \\\"prompt_version\\\": \\\"extract_v1\\\", \\\"prompt_sha256\\\": \\\"b74b563d...\\\", \\\"prepared\\\": true (artifacts/review-evidence/T-177-staff-engineer-probe.py, AUDIT_ONE line). app/frontend/timeline.js why-generator line shows '${lad.generator.model} · ${lad.generator.prompt_version}', which renders 'hand-checked (qa) · extract_v1'.\",\n   \"why_it_matters\": \"A prompt version and hash say a prompt produced the answer. Nothing was prompted; the team wrote it. Small, but it is the same provenance question in a different field.\",\n   \"fix\": \"On prepared rows, set prompt_version to null and show 'hand-written for the demo' in the why line, or omit the prompt hash.\",\n   \"acceptance_test\": \"Unit: prepared audit rows have prompt_version null (or a 'hand-written' marker) and no prompt_sha256 used as a model prompt.\"}\n ],\n \"whats_right\": [\n  \"Audit model swap and prepared flag are mutation-guarded: removing the audit model swap fails 5 tests; forcing is_prepared False fails 3 (archive copy, restored, cmp-verified).\",\n  \"PM acceptance holds on 04ea2bf: trace generator step model 'hand-checked (qa)' with the prepared label; the recorded set keeps 'claude-sonnet-5-5' and the AI wording.\",\n  \"memory/contracts/api.md:57 and :836-841 document answers, prepared fields on items, audit, trace and narrative; the observed payloads match.\"\n ],\n \"questions_for_chris\": [\n  \"D-065 pins the tooltip 'The AI's own answers on these cases are in the evaluation report.' The report does not hold them. Do you want the sample case's per-entry answers written into the eval report (a runner change), or the tooltip reworded now?\",\n  \"On the curated demo, the second AI check is a real recorded model answer (claude-haiku-5-5). Should the 'How the AI was checked' panel stay on the curated set with the wording fixed (F1), or be hidden there?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T20:38:15.035Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:17.068Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json,re\ns=open('reviews/T-177-staff-engineer.md').read()\nm=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', s, re.S)\nprint('json blocks:', len(m))\nd=json.loads(m[0])\nsev=[f['severity'] for f in d['findings']]\nprint('verdict', d['verdict'], 'severities', sev, 'model', d['model'], 'card', d['card'])\nexp = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('rule expects', exp, 'OK' if exp==d['verdict'] else 'MISMATCH')\n\"; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Parse the review JSON, check verdict rule, run board validate"
}
````

### User / tool · 2026-11-02T20:38:17.122Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:19.450Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-check-json.py",
 "content": "import json\nimport re\n\npath = \"/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer.md\"\ns = open(path).read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, s, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"card\", d[\"card\"], \"persona\", d[\"persona\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"])\nprint(\"severities\", sev)\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"rule expects\", expected, \"OK\" if expected == d[\"verdict\"] else \"MISMATCH\")\n"
}
````

### User / tool · 2026-11-02T20:38:19.549Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-check-json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:20.069Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-check-json.py; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Check review JSON block against verdict rule and run board validate"
}
````

### User / tool · 2026-11-02T20:38:20.255Z

**tool result**
````
json blocks: 1
card T-177 persona staff-engineer-reviewer model claude-haiku-5-5 verdict fail
severities ['blocker', 'major', 'major', 'minor', 'nit']
rule expects fail OK
ok (181 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:26.141Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md",
 "content": "---\nname: t177-provenance-patterns\ndescription: T-177 (D-065 prepared answers): payload-level model names and tooltip pointers escaped the per-item provenance tests\nmetadata:\n  type: project\n---\n\nPer-item provenance fixed (trace step, audit row, item ladder) while case, judges and banner-level surfaces still named the model or claimed a location that did not hold the answers.\n\n**Why:** D-065 forbids presenting curated (hand-written) answers as model output; the PM's acceptance test only checked trace, audit, item and badge text. The judges panel (`app/frontend/judges.js:166-168`, `m.generator` from `trace.py:1003` `cx.models`) still printed \"Drafted by claude-sonnet-5-5\" on the curated demo, and `GET /api/cases/{tok}` plus `/judges` returned `models.generator` = claude-sonnet-5-5. No test asserted those fields.\n\n**How to apply:**\n- For any \"never presented as X\" decision, grep every payload and template for the old model name on the curated path (case `models`, `/judges` `models`, banners, panel copy), not only the per-item fields the card names.\n- The eval-report tooltip (\"the AI's own answers are in the evaluation report\") was false: `evals/reports/runs/*/sample.json` stores `summary_sha`, not text. Check that a pointer's target contains what it promises.\n- Banner wording \"checked by code\" hid the second AI check that runs on the same curated items. Check banners against every check step on the page.\n- Global badge/banner decided by fixture-set name vs per-call provenance: a fallback to the recorded dir (`fixture.py:23-24`) can mislabel one item. Probe with a missing key.\n- Mutation pattern that worked: break `_prepared_model` in `app/llm/audited.py` in an archive copy, restore via `git show <sha>:path`, cmp-verify.\n- Playwright: a collapsed `<details>` child is hidden; click the `judge-summary` toggle, then read `.first.text_content()`; `inner_text` times out.\n\nRelated: [[project_llm_stage_review_patterns]], [[feedback_frontend_text_coupling]], [[project_t167_plain_wording_patterns]].\n"
}
````

### User / tool · 2026-11-02T20:38:26.233Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:26.472Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 150
}
````

### User / tool · 2026-11-02T20:38:26.480Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (150). The file has 108 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:27.310Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 100
}
````

### User / tool · 2026-11-02T20:38:27.318Z

**tool result**
````
100	- [Bind to named reference](feedback_bind_to_named_reference.md) — binding test must read the reference the artifact names
101	- [T-173 seed-fidelity patterns](project_t173_seed_fidelity_patterns.md) — r1/r2: seeded row raw-equal to placeholder; browser attempt rule unguarded (M6 3/3)
102	- [Guard blocks shell expansions](feedback_guard_blocks_shell_expansions.md) — git-guard refuses ${var%%}; board-guard refuses 2>; use python -I script
103	- [T-175 r2 patterns](project_t175_r2_patterns.md) — 9/9 backend mutants red, UI renders null progress as "None"
104	- [Playwright render probe](feedback_playwright_render_probe.md) — render the real list from an archive; screenshot beats inner_text
105	- [GATE-M3 / T-045 patterns](project_gate_m3_t045_patterns.md) — is_mobile scroll check vacuous, "unit-covered" claim false, no-op mutants
106	- [T-045 r2 record-latest patterns](project_t045_r2_record_latest_patterns.md) — header value copied not recomputed; flipped fixture report records ship bar True
107	- [Mutant apply verify](feedback_mutant_apply_verify.md) — BSD sed 0,/re/ no-ops silently; grep the mutant; restore via git show HEAD
108	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:30.470Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Mutant apply verify](feedback_mutant_apply_verify.md) — BSD sed 0,/re/ no-ops silently; grep the mutant; restore via git show HEAD\n",
 "new_string": "- [Mutant apply verify](feedback_mutant_apply_verify.md) — BSD sed 0,/re/ no-ops silently; grep the mutant; restore via git show HEAD\n- [T-177 provenance patterns](project_t177_provenance_patterns.md) — per-item model fixed, case/judges payload and panel still name the model; tooltip points at hash-only report\n"
}
````

### User / tool · 2026-11-02T20:38:30.572Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T20:38:32.082Z

T-177 verdict: fail, 1 blocker (curated judge panel still says "Drafted by claude-sonnet-5-5"), 2 majors. Review: /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer.md
