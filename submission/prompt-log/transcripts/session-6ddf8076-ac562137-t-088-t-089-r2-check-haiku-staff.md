# Subagent: T-088/T-089 r2 check (haiku staff) (T-088/T-089 r2 check (haiku staff))

Source: `agent-ac56213716e0d5f16.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:35:59.461Z

Round-2 check of board cards T-088 and T-089 in /Users/arsis/zlayt-pm-project (commit 55300e9). Read reviews/T-088-staff-engineer.md and reviews/T-089-staff-engineer.md, and test a clean worktree of HEAD (`git worktree add <scratchpad>/wt HEAD`, then remove it).

- **T-088:** confirm the reason now names the records the evidence comes from (golden case_01 record 8), that it's never auto-applied, and that the AC1 correction is posted, with the UI moved to T-096.
- **T-089:** confirm the route-level demo-isolation tests fail when local mode is forced (mutate in a scratch copy) and that the minors are fixed.

Run `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`. Write reviews/T-088-staff-engineer-r2.md and reviews/T-089-staff-engineer-r2.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:01.418Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:36:01.426Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:01.686Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t088_t089_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:36:01.694Z

**tool result**
````
1	---
2	name: t088-t089-review-patterns
3	description: T-088 date-convention and T-089 dismissal suggestions (f667f08) r1 patterns: packet-scope reason wording, AC marked done with UI unbuilt, shared index staging card files deleted, route isolation untested
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns from the T-088 (date-convention suggestion) and T-089 (dismissal suggestions) r1 review of commit f667f08.
9	
10	- **Reason text states a scope the data does not have.** T-088 reason said "in this record" for evidence in other packet records (golden case_01 record 8). Pinned by the test itself, so a green suite did not catch it. Check every generated sentence's scope claim against the record ids in its evidence array.
11	- **AC marked done=true with a named UI or eval half unbuilt.** T-088 AC named "the UI pre-selects" and "eval case"; neither existed (frontend grep 0, golden expected 0). Check each AC noun against the file it names before accepting done.
12	- **Shared index staging deletion of card files.** `git diff --cached --name-status` showed 'D' for both cards' files while HEAD had them. Any commit from that index deletes the code. Run `git diff --cached --name-status` at the start of each review.
13	- **Named isolation test that asserts no isolation.** T-089 `test_routes_and_demo_mode_isolation` seeds one case only; forcing `local_mode=lambda: True` in api.py passes all tests. Mutate the route wiring, not just the function.
14	- **Eligibility rules masking each other.** Type list and lexicon-origin check each excluded the same test flags, so removing either alone was not caught. Test each rule with a flag that only the other rule would exclude.
15	- **Golden identity test sensitivity.** History seeded in one category; only the sample case is sensitive. Seed history per golden case's own categories.
16	- **Assertion precedence.** `A and B or C` in a test assertion passes whenever C holds regardless of A. Parenthesize.
17	
18	**How to apply:** mutation runs in this repo must write under `artifacts/review-evidence/` (scratchpad writes are blocked by reviewer-write-guard for Write; shell copies there were allowed). Remove the copied product tree afterwards, since a stray `tests/` copy under artifacts can break full-repo pytest collection. See [[feedback_review_write_once]] and [[project_t050_namespacing_review_patterns]].
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:01.973Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:36:01.980Z

**tool result**
````
1	---
2	name: t073-t084-review-patterns
3	description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording gate, commit deleted T-083 billing
4	metadata:
5	  type: project
6	---
7	
8	T-073 r1 (7724412): the narrowed guard (judge_guard.py) is right at the seam, but the production path still hides programmer bugs: `app/llm/audited.py:70` has its own `except Exception` that retries 3x and surfaces as JUDGE_UNAVAILABLE/NONE. The card's propagation test raises from a raw fake call one layer above, so it cannot see this. Also `judges._run` catches LLMFailed before the guard, so `error_class` is never recorded for the failure the AC names.
9	**Why:** a card's test proves the behaviour at the seam it fakes; the broad catch moved one layer down and the card's AC was still marked done.
10	**How to apply:** for any "narrow the except" card, run the real call path with the provider raising a plain RuntimeError (audited_call with complete_with_meta raising) and check llm_calls rows and the ladder. Do not accept a raw FakeCall as proof of propagation.
11	
12	T-084 r1 (ec33bf0): (a) restore (undo own demotion) skips both checks and reuses the judge answer for the OLD sentence; `carry_over` keys on figure text and cents only, so a rerun that flips the code class of the same figure lets a current rate become a charge with no check. (b) The code wording gate matches "Charge" in "Charge per visit $185." and "Billed" in "Billed $150 per visit", so the judge is the only gate; the test at test_reclassify.py:108-116 encodes the sneak as expected. (c) The commit deleted T-083's committed billing.py, test_billing.py, api billing hook and api.md section; the cards' commit list and the commit message did not say so.
13	**Why:** the gate tests cover each check alone; the bypass needs a rerun between two calls. Commit-level deletions are only visible in `git show --stat`.
14	**How to apply:** on any "skip checks when restored/previous" path, rerun the pipeline with a changed sentence before the restore and check the outcome. On any keyword gate, feed it the rate phrase the spec names. On every review, run `git show --stat <commit>` and grep for deletions of other cards' paths.
15	
16	Harness notes (this review): the brief's `-k "review or reclass"` selector collects zero tests from tests/unit/test_judge_guard.py, so name guard files explicitly. The working tree moved mid-review (reclassify.py and test_reclassify.py edited by another worker), so the review pinned HEAD with `git archive ec33bf0`. The review-write guard refused an Edit to my own T-084 file after I had written one unverified sentence ("the sample case is not affected"); I disclosed it in the reply instead of creating an -r2 file. Proof-read before the first Write, as in [[feedback_review_write_once]].
17	
18	Related: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes).
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:02.456Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -5 && git status --short | head -20 && ls reviews/ | grep -E \"T-08[89]|T-09\"",
 "description": "Show HEAD, recent log, status, and T-088/T-089 review files"
}
````

### User / tool · 2026-11-02T04:36:02.614Z

**tool result**
````
d3130e3
d3130e3 harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
55300e9 fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
49c4600 memory: T-091 speaker attribution v2 fails fresh adversary; stays cut (D-040)
e2b4e3f fix: restore T-083 billing deleted by ec33bf0
865b186 feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/backend/reclassify.py
T-088-staff-engineer.md
T-089-staff-engineer.md
T-090-staff-engineer.md
T-091-claims-adjuster.md
T-093-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:04.769Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-088-staff-engineer.md && echo ==========&& cat reviews/T-089-staff-engineer.md",
 "description": "Read the round-1 T-088 and T-089 reviews"
}
````

### User / tool · 2026-11-02T04:36:04.916Z

**tool result**
````
# T-088 review: date-convention suggestion (staff-engineer-reviewer)

**Verdict: fail.** One blocker: the suggestion's `reason` says the evidence dates are "in this record" when they sit in other records of the packet. I rated it a blocker, not a major, under CONTRACT D.2 and CLAUDE.md non-negotiable 5 (every statement traces to the input). The code-only, never-applied and D-041 parts hold.

Scope: commit f667f08 (`app/backend/date_convention.py`, `app/backend/present.py:122-135`, `tests/unit/test_date_convention.py`, the T-088 contract section in `memory/contracts/api.md`). Cross-checked against D-041 and D-042 in `memory/ORCHESTRATOR_DECISIONS.md` (lines 49-50) and the golden sample `evals/golden/case_01_date_formats.txt`.

**Checks against your four points**
1. Code only: holds. `date_convention.py` imports only `re` and `dates`, with no LLM or call path. Mutation 88e (a DB write that auto-confirms the ISO reading) is caught by 2 tests.
2. Never auto-applied, one confirm still required: holds. No server path reads `suggestion` except `present.py:129`, which only builds it. `review.confirm_date` (`review.py:172-181`) still takes the client's date and checks it against the candidates. The D-041 block reads `records.date_status`, not the suggestion (`review.py:45-50`).
3. Reason quotes a real date from the packet: the quoted dates are real (`02/17/2026`, `03-17-26`), but the scope is wrong. See F1.
4. Mixed or contradictory packets: `date_convention.py:54-55` returns `None` when the orders disagree or there is no evidence. Mutant 88a (mixed packets allowed through) is caught.

**Exercised**
- `python3 tools/board.py show T-088` and `show T-089`; `git show f667f08 --stat` and per-file diffs; `git show f667f08:<path>` for every file in scope; D-041/D-042 lines in `memory/ORCHESTRATOR_DECISIONS.md`.
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: 151 passed, 1106 deselected. `pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py -v`: 25 passed.
- Mutation suite in a scratch copy (`artifacts/review-evidence/T-088-T-089/mut`, runner `mutate.py`, output `mutation_run.txt`). Core rules 88a/88b/88c/88d/88e are all caught.
- Probe on golden case_01 through FastAPI `TestClient` (no live server, no network, `LLM_BACKEND=fixture`): output in `artifacts/review-evidence/T-088-T-089/probe_t088_output.txt`.
- `git diff --cached --name-status` and `git cat-file -e HEAD:<path>` (index state, see F3).
- `grep -rn suggestion app/frontend` returned 0 matches. `grep -c "suggestion\|dismissal" evals/golden/case_01_date_formats.expected.json` returned 0.

```json
{"card": "T-088", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f667f08: app/backend/date_convention.py, app/backend/present.py (dates_to_confirm), memory/contracts/api.md (T-088 section), tests/unit/test_date_convention.py; golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process)",
 "exercised": ["board.py show T-088 and T-089", "git show f667f08 --stat and per-file diffs", "git show f667f08:<path> for in-scope files", "memory/ORCHESTRATOR_DECISIONS.md D-041, D-042", "pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)", "pytest tests/unit/test_date_convention.py -v (8 passed)", "mutation suite 88a-88e in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)", "probe on golden case_01 via TestClient (artifacts/review-evidence/T-088-T-089/probe_t088_output.txt)", "git diff --cached --name-status; git cat-file -e HEAD:<path>", "grep suggestion app/frontend (0); golden case_01 expected.json (0)"],
 "verdict": "fail",
 "scores": {"code_only_no_llm": 5, "never_auto_applied_d041": 5, "reason_grounded_in_packet": 2, "mixed_packet_handling": 4, "tests_fail_on_mutation": 4, "ac_integrity": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Reason says the evidence dates are 'in this record' when they come from other records in the packet",
   "evidence": "app/backend/date_convention.py:64-65 builds 'Other dates in this record use ...' while `_evidence(records, raw_text)` (line 52) scans every packet record. Golden repro (probe_t088_output.txt): the 04/05/2026 suggestion on record r8 returns reason '4 other dates in this record use month first (02/17/2026) and (03-17-26)', with evidence record ids r2 and r6 (the other two counted dates, 3/25/26 in r7 and 04/14/2026 in r7's excerpt, are also outside r8). evals/golden/case_01_date_formats.txt: record 8 (lines 39-41) contains only 'Patient reports no new symptoms.' and no other date. The false wording is pinned by tests/unit/test_date_convention.py:32, :46 and :99 (line 99 asserts the exact golden reason). The T-088 AC text (board show T-088) says 'the reason (other dates in the packet)'.",
   "why_it_matters": "The paralegal reads a provenance claim about the record in front of them that is false for every golden case of this kind. The D-041 gate still stops an unconfirmed date from reaching the letter, so no wrong date is exported, but the stated reason sends the paralegal to look in the wrong record. CLAUDE.md non-negotiable 5 says every statement must trace to the input, and this one does not. Rated blocker per CONTRACT D.2 (invented fact), not major. The date strings quoted are real.",
   "fix": "Build the reason from the evidence's own record ids, e.g. 'Other dates in this packet use month first (02/17/2026, record 2) and (03-17-26, record 6)'. Remove the phrase 'in this record' everywhere. Update the expected strings at test_date_convention.py:32, :46 and :99.",
   "acceptance_test": "tests/unit/test_date_convention.py: (a) golden case_01 reason names the record of each quoted date and does not contain 'this record'; (b) packet r1 '03/14/2026' with ambiguous r2 '04/05/2026' yields a reason that names record 1. Mutation: restore the old wording, and tests (a) and (b) must fail."},
  {"severity": "major",
   "title": "AC 1 is marked done=true while two of its required parts are not in the codebase",
   "evidence": "board show T-088, AC 1: \"done\": true, evidence \"... UI pre-select is frontend's (see note)\". The AC text includes 'the UI pre-selects it' and 'eval case'. Handoff: 'Left: frontend pre-select; qa golden case.' grep -rn suggestion app/frontend: 0 matches. grep -c 'suggestion|dismissal' evals/golden/case_01_date_formats.expected.json: 0.",
   "why_it_matters": "The card says the AC is done, but the paralegal-facing behaviour (radio pre-selected with the reason, confirm on click only) does not exist, and the eval case the AC names does not exist either. Only the unit-level half is shipped. A required AC item that is present but incomplete is major under the persona calibration.",
   "fix": "Set AC 1 back to done=false until (a) the frontend pre-select ships and (b) a golden expected entry for case_01 record 8 asserts the MDY suggestion. Or split those two parts into follow-up cards and close the unit half only.",
   "acceptance_test": "grep -n suggestion evals/golden/case_01_date_formats.expected.json shows the MDY assertion. A frontend or E2E test shows the 04/05/2026 radio pre-selected with its reason, no confirm request is sent on load, and Accept stays blocked (422 DATE_UNCONFIRMED) until a click on Confirm."},
  {"severity": "major",
   "title": "Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)",
   "evidence": "git diff --cached --name-status: 'D app/backend/date_convention.py', 'D app/backend/dismissal_patterns.py', 'D tests/unit/test_date_convention.py', 'D tests/unit/test_dismissal_patterns.py' (also 'D app/llm/prompts/conflicts_v1.md'). git cat-file -e HEAD:app/backend/date_convention.py succeeds, and the on-disk files match HEAD byte for byte (checked with git show f667f08:<path> | diff). git status shows them as '??' untracked.",
   "why_it_matters": "The committed artifact at HEAD is intact, so this is not a defect in f667f08 itself. But the next commit made from this index deletes the T-088 and T-089 code and tests from the repository. That is a silent loss of both cards' deliverables.",
   "fix": "Orchestrator (not this reviewer) restores the index for the card paths without touching the working tree, then commits with explicit paths. The index then matches HEAD for these four files.",
   "acceptance_test": "git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py prints nothing, and git ls-files app/backend/date_convention.py lists the file."},
  {"severity": "minor",
   "title": "Weak assertion: `and`/`or` precedence lets the two-digit-year test pass with the wrong convention",
   "evidence": "tests/unit/test_date_convention.py:65: assert s[\"convention\"] == \"MDY\" and s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"]. Python parses this as (A and B) or C. When iso is not None and is in the candidates, C is True whatever the convention. In this packet iso is None, so the convention is pinned today; the defect is latent.",
   "why_it_matters": "A later change that makes iso non-null for this case could pass with the convention wrong, which is exactly the regression this test exists to catch.",
   "fix": "assert s[\"convention\"] == \"MDY\" and (s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"])",
   "acceptance_test": "Mutant: swap _LABEL so MDY reports DD/MM while iso is non-null for a two-digit-year packet. The fixed assertion must fail."},
  {"severity": "nit",
   "title": "Unused import",
   "evidence": "app/backend/date_convention.py:10: from app.backend import dates (no reference to dates in the module).",
   "why_it_matters": "Dead import; harmless.",
   "fix": "Delete the line.",
   "acceptance_test": "python -m pyflakes app/backend/date_convention.py (or a grep for 'dates\\.') reports nothing."}
 ],
 "whats_right": [
  "No server path reads the suggestion: present.py:129 only builds it, confirm_date (review.py:172-181) still takes the client's date and checks it against the candidates, and the D-041 block reads records.date_status (review.py:45-50).",
  "Mixed-order and no-evidence packets return None (date_convention.py:54-55); mutant 88a, which lets mixed packets through, fails test_no_suggestion_without_evidence_or_with_mixed_evidence.",
  "Code only with no LLM path, and the auto-confirm mutant 88e is caught by two tests (the write-check and the golden confirm test)."
 ],
 "questions_for_chris": ["For a packet whose dates disagree on order, should the paralegal see a short note that the packet is mixed, or is silence (no suggestion) the intended behaviour? The AC allows either."]
}
```
==========
# T-089 review: dismissal-pattern suggestions (staff-engineer-reviewer)

**Verdict: changes.** No blocker. The core rules hold: nothing is auto-dismissed, the GET is read-only, bulk-applied flags never feed back into the count, the pipeline does not read the history, and storage adds no identity. Two majors and one minor-level test gap need fixing before the gate. The majors are the demo-isolation test gap (F1) and the shared git index that stages deletion of this card's files (F3). Suggestions only, no auto-dismiss, and no change to pipeline output or golden recall are all verified, not assumed.

Scope: commit f667f08 (`app/backend/dismissal_patterns.py`, `app/backend/api.py:497`, `tests/unit/test_dismissal_patterns.py`, the T-089 contract section in `memory/contracts/api.md`). Checked against D-042 in `memory/ORCHESTRATOR_DECISIONS.md` line 50.

**Checks against your three points**
1. Nothing auto-dismissed: holds. `suggest()` (`dismissal_patterns.py:51-72`) only reads. The GET route (`:92-99`) does not call `apply`. The POST route (`:101-114`) is the only writer, and it needs a key. Mutants 89e (suggest writes) and 89f (GET auto-applies) are both caught.
2. No effect on pipeline output or golden recall: holds. `pipeline.py` does not import `dismissal_patterns`. The golden identity test (`test_dismissal_patterns.py:116-134`) passes, and mutant 89i (history filters pipeline flags) is caught. Sensitivity is limited, see F4.
3. Storage local only, no user identity: holds. The module reads the existing `flags` table with no new column, table, or identity field. `grep -n "user|email|identity|account"` on the module returns only the docstring that says there are no users. Scope is case-only unless `ZLAYT_MODE=local`, mutant 89g is caught.

**Exercised**
- `python3 tools/board.py show T-089`; `git show f667f08` (stat and per-file); `git show f667f08:<path>` for in-scope files; D-042 in `memory/ORCHESTRATOR_DECISIONS.md`.
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: 151 passed, 1106 deselected. `pytest tests/unit/test_dismissal_patterns.py -v`: 17 passed (of 25 across both cards).
- Mutation suite in scratch copy `artifacts/review-evidence/T-088-T-089/mut` (runner `mutate.py`, output `mutation_run.txt`): 89a, 89c, 89e, 89f, 89g, 89i caught; 89b, 89d, 89d2, 89h not caught (see findings).
- `git diff --cached --name-status`; `git cat-file -e HEAD:<path>` (F3).
- `grep -rn dismissal app/frontend`: 0 matches (no banner built yet).

```json
{"card": "T-089", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f667f08: app/backend/dismissal_patterns.py, app/backend/api.py:497 (route registration), tests/unit/test_dismissal_patterns.py, memory/contracts/api.md (T-089 section); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)",
 "exercised": ["board.py show T-089 and T-088", "git show f667f08 --stat and per-file diffs", "git show f667f08:<path> for in-scope files", "memory/ORCHESTRATOR_DECISIONS.md D-042", "pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)", "pytest tests/unit/test_dismissal_patterns.py -v (17 passed)", "mutation suite 89a-89i incl. 89d2 in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)", "git diff --cached --name-status; git cat-file -e HEAD:<path>", "grep -rn dismissal app/frontend (0)", "grep for pipeline imports of dismissal_patterns (none)"],
 "verdict": "changes",
 "scores": {"never_auto_dismiss": 5, "no_pipeline_or_recall_effect": 4, "local_only_no_identity": 4, "demo_isolation_tested": 2, "tests_fail_on_mutation": 3, "ac_integrity": 3},
 "findings": [
  {"severity": "major",
   "title": "Demo-mode isolation at the route is not tested; forcing local scope in the route passes all 25 tests",
   "evidence": "app/backend/api.py:497 registers the route with local_mode=local_mode. Mutant 89h replaces it with local_mode=lambda: True in the scratch copy: '25 passed' (artifacts/review-evidence/T-088-T-089/mutation_run.txt, line 'MUTANT 89h ... NOT CAUGHT'). tests/unit/test_dismissal_patterns.py:94-113 (test_routes_and_demo_mode_isolation) creates one case only and seeds history in that case, so it cannot tell local from non-local scope. The unit test at :84-91 tests the function with local=True/False, not the route. memory/contracts/api.md (T-089 section) says 'a public/demo token never sees another case's dismissals'; the test named 'demo-mode isolation' does not assert that.",
   "why_it_matters": "The suggestion message counts dismissals in other cases ('all cases on this computer'). If the route's scope regresses, a public demo token would see phrase counts from other cases. The data is synthetic and the counts carry little content, so this is a test-coverage gap, not a live leak; the code today is correct. Depth on exposure belongs to security-reviewer. The card's AC evidence names a demo-isolation test that does not test isolation.",
   "fix": "Add a route test: create case A with 3 dismissals of a phrase and case B with the pending match, run without ZLAYT_MODE, and assert GET /api/cases/B/dismissal_suggestions returns suggestions == []. Then run with ZLAYT_MODE=local and assert the suggestion appears. Rename the test to describe what it asserts.",
   "acceptance_test": "Mutant 89h (local_mode forced True in api.py:497) must fail the new test. The unmodified route must pass it."},
  {"severity": "major",
   "title": "Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)",
   "evidence": "git diff --cached --name-status: 'D app/backend/dismissal_patterns.py' and 'D tests/unit/test_dismissal_patterns.py' (plus the T-088 files and app/llm/prompts/conflicts_v1.md). git cat-file -e HEAD:app/backend/dismissal_patterns.py succeeds and the on-disk file matches HEAD (git show f667f08:<path> | diff: no output).",
   "why_it_matters": "HEAD is intact, so f667f08 itself is fine. The next commit made from this index deletes the T-089 module, its routes' code path and its tests, which is a silent loss of the deliverable.",
   "fix": "Orchestrator restores the index for these paths without touching the working tree, then commits with explicit paths. The reviewer does not run git reset.",
   "acceptance_test": "git diff --cached --name-status -- app/backend/dismissal_patterns.py tests/unit/test_dismissal_patterns.py prints nothing."},
  {"severity": "minor",
   "title": "Eligibility rules are tested only as a conjunction; neither the type rule nor the origin rule is isolated",
   "evidence": "app/backend/dismissal_patterns.py:22 (ELIGIBLE_TYPES) and :28 (origin must contain 'lexicon'). tests/unit/test_dismissal_patterns.py:49-50 builds the gap and record_warning flags with origin='code', so the origin check alone excludes them. Mutant 89d (gap added to ELIGIBLE_TYPES) and mutant 89d2 (origin requirement removed) both give '25 passed' (mutation_run.txt).",
   "why_it_matters": "The AC says 'ineligible types never offered'. Today a lexicon-origin gap flag would be offered for hiding if the type list were widened, and no test would notice.",
   "fix": "Add cases: a gap flag and a record_warning flag with origin 'lexicon+llm' (must not be suggested); a pre_existing flag with origin 'llm' only (must not be suggested).",
   "acceptance_test": "Mutants 89d and 89d2 must each fail a test."},
  {"severity": "minor",
   "title": "Category threshold boundary (CATEGORY_MIN) has no negative test; golden identity test seeds only one category",
   "evidence": "app/backend/dismissal_patterns.py:21 CATEGORY_MIN = 5. The category test (tests/unit/test_dismissal_patterns.py:54-63) only asserts the positive case at 5. Mutant 89b (CATEGORY_MIN = 4) gives '25 passed'. Also tests/unit/test_dismissal_patterns.py:15 defaults the seeded history to category 'new_onset'. Mutant 89i fails only the [sample] parametrization of the golden identity test (mutation_run.txt), so the other nine golden cases are not sensitive to history at all.",
   "why_it_matters": "The AC claim 'pipeline output identical on all golden cases with and without history' is true, but the test can only detect pipeline influence on flags of category new_onset. For the other nine cases it is a vacuous equality. The AC item also says 'eval shows no recall loss', and no eval report path exists; this unit equivalence test is the only evidence.",
   "fix": "Add a 4-dismissal negative case for the category rule. In the golden identity test, seed history with each case's own flag categories and phrases (taken from its pipeline output) so the equality is sensitive per case. Name the unit test as the recall evidence in the card, or add an eval report.",
   "acceptance_test": "Mutants 89b and 89i must each fail on at least one golden case other than sample."},
  {"severity": "minor",
   "title": "AC 'surface as a suggestion' is evidenced only by the API payload; the banner is not built",
   "evidence": "board show T-089, AC 1 done=true. Handoff: 'Left: frontend banner'. grep -rn dismissal app/frontend: 0 matches. The AC text does not name a UI element, so the API payload is the AC's surface.",
   "why_it_matters": "Acceptable for this AC as written, but the card's notes ask the frontend to show a banner with two buttons, and nothing in the card records that as a later AC. The surfacing will be lost unless a follow-up card tracks it.",
   "fix": "Create a follow-up frontend card for the banner, or add the banner to this card's AC before closing it.",
   "acceptance_test": "A UI test shows the banner after three dismissals, and flags stay unchanged until the 'Hide similar' click."},
  {"severity": "nit",
   "title": "apply() is not atomic across flags",
   "evidence": "app/backend/dismissal_patterns.py:86-87: the loop calls review.apply_review once per flag id with no transaction. A failure partway leaves earlier flags dismissed. Not reproduced; the flag ids come from pending flags and no test exercises a mid-loop failure.",
   "why_it_matters": "Low risk because each dismissal is individually logged and reversible with reset. Still a partial write with no explicit response.",
   "fix": "Wrap the loop in one transaction, or document the partial-write behaviour in api.md.",
   "acceptance_test": "A test that forces apply_review to raise on the second flag and asserts the first flag is not dismissed."}
 ],
 "whats_right": [
  "The GET path is read-only (mutant 89e, which writes on read, fails four tests; mutant 89f, which auto-applies on GET, fails the route test).",
  "Bulk-applied flags carry APPLIED_NOTE and are excluded from the count (dismissal_patterns.py:44); mutant 89c, which counts them, fails the self-reinforcement test.",
  "The pipeline does not import the module, and the history can change no pipeline output (mutant 89i is caught by the golden identity test)."
 ],
 "questions_for_chris": ["In local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?"]}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:05.314Z

**tool call — Bash**
````
{
 "command": "git show --stat 55300e9 && echo ==== && git show --stat d3130e3 | head -30 && echo ==== && git cat-file -t 55300e9 && git merge-base --is-ancestor 55300e9 HEAD && echo ancestor-ok",
 "description": "Show stat for round-2 commit and HEAD commit"
}
````

### User / tool · 2026-11-02T04:36:05.479Z

**tool result**
````
commit 55300e97ffb8916f705a1b8baa3c317f8585ced4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:34:35 2026 -0600

    fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/date_convention.py        |  9 ++--
 memory/contracts/api.md               | 13 ++---
 tests/unit/test_date_convention.py    | 29 +++++++++--
 tests/unit/test_dismissal_patterns.py | 93 ++++++++++++++++++++++++++++++-----
 4 files changed, 116 insertions(+), 28 deletions(-)
====
commit d3130e3122e9244c4a34873922b9d964166cfc5a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:35:51 2026 -0600

    harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 .claude/hooks/git_guard.py    |  6 ++++++
 tools/tests/test_git_guard.py | 20 ++++++++++++++++++++
 2 files changed, 26 insertions(+)
====
commit
ancestor-ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:07.664Z

**tool call — Bash**
````
{
 "command": "git show 55300e9 -- app/backend/date_convention.py tests/unit/test_date_convention.py memory/contracts/api.md",
 "description": "Show round-2 diff for date convention, its tests, and API contract"
}
````

### User / tool · 2026-11-02T04:36:07.767Z

**tool result**
````
commit 55300e97ffb8916f705a1b8baa3c317f8585ced4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:34:35 2026 -0600

    fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/date_convention.py b/app/backend/date_convention.py
index 226b57d..a3249a9 100644
--- a/app/backend/date_convention.py
+++ b/app/backend/date_convention.py
@@ -7,8 +7,6 @@ The suggestion is a hint the UI pre-selects; the paralegal still confirms once t
 accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
 import re
 
-from app.backend import dates
-
 _NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
 MAX_EVIDENCE = 2
 _LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}
@@ -38,7 +36,8 @@ def _evidence(records, raw_text):
 
 
 def _example(ev):
-    return f"({ev['raw']})"
+    """'(Record 3: 03/14/2026)': names the record the date sits in, so the paralegal looks in the right place."""
+    return f"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})"
 
 
 def suggest(rec: dict, records: list, raw_text: str):
@@ -61,7 +60,7 @@ def suggest(rec: dict, records: list, raw_text: str):
     shown = ev[:MAX_EVIDENCE]
     n = len(ev)
     first = "month first" if order == "MDY" else "day first"
-    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
-              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
+    reason = (f"Another date in this packet uses {first} {_example(shown[0])}" if n == 1 else
+              f"{n} other dates in this packet use {first} " + " and ".join(_example(e) for e in shown))
     return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
             "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 73079de..573575e 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -36,6 +36,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 | GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
 | GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
 | GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
+| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
 | GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
 
 ---
@@ -77,7 +78,6 @@ Request text is normalised first (CRLF and CR become LF; leading/trailing whites
 Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
 Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).
 
-## POST /api/cases/{token}/review/batch (D-031)
 ### PDF hidden text and local OCR (T-087, T-086; D-042)
 Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server.
 
@@ -100,6 +100,7 @@ Response and `GET /api/cases/{token}` gain, for PDF cases only:
 **Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, date confirmation or rejudge clears it. Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
 **`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page that has none. The UI shows it beside the page's text.
 
+## POST /api/cases/{token}/review/batch (D-031)
 Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
 
 ## /api/cases/{token}/export_config (D-031)
@@ -260,10 +261,10 @@ Every entry of `dates_to_confirm` (in `GET /api/cases/{token}` and in the `confi
 ```json
 { "record_id": "r8", "raw": "04/05/2026", "candidates": ["2026-04-05", "2026-05-04"], "status": "ambiguous",
   "suggestion": { "convention": "MDY", "label": "MM/DD", "iso": "2026-04-05",
-                  "reason": "Other dates in this record use month first (03/14/2026)",
+                  "reason": "Another date in this packet uses month first (Record 1: 03/14/2026)",
                   "evidence": [{"record_id": "r3", "raw": "03/14/2026"}], "evidence_count": 1, "auto_applied": false } }
 ```
-`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Other dates in this record use month first (03/14/2026)"; several read "4 other dates in this record use month first (02/17/2026) and (03-17-26)" (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
+`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Another date in this packet uses month first (Record 1: 03/14/2026)"; several read "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)" (each example names the record the date sits in; the evidence dates come from the packet, never described as "in this record") (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
 
 The suggestion changes nothing: the record stays `ambiguous`, its entry stays in `undated_entries`, and Accept stays blocked (D-041, `DATE_UNCONFIRMED`) until the paralegal confirms through `confirm_date`, which still accepts only a code candidate (`422 date_invalid` otherwise). **UI:** pre-select the radio for `suggestion.iso` (when not null), show `reason` under it, keep the confirm button enabled only on an explicit click, and let the paralegal pick the other reading freely. Do not confirm on load.
 
@@ -280,7 +281,7 @@ Response 200:
 `kind` is `phrase` (same lexicon phrase group dismissed at least `min_phrase` times) or `category` (same category at least `min_category` times, listing only flags a phrase suggestion does not already cover). `flag_ids` are this case's still-**pending** flags that match. The list is empty when nothing qualifies. This GET is read-only and changes no flag, state or pipeline result.
 
 ### POST /api/cases/{token}/dismissal_suggestions/apply
-Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
+Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed (reversible with `reset`); the response is then an error and the refreshed list shows what remains. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
 
 ## GET /api/cases/{token}/items/{item_id}  — "Why?"
 Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
@@ -647,7 +648,6 @@ Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays tok
 `GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
 `POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).
 
-## DELETE /api/cases/{token}
 ## GET /api/cases/{token}/billing  (T-083, D-042)
 Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.
 ```json
@@ -698,6 +698,7 @@ Languages: English and Spanish. Code detects the language of every record (`app/
 - **Dates.** A `Date:` header such as `14 de mayo de 2026`, `14-ago-2026` parses (day first, month spelled out, never ambiguous).
 - **Not covered:** amounts in Spanish records are classified by the English billing phrases, so a Spanish charge or rate is usually `unclear` and goes to the paralegal (T-084 reclassify); Latin-American `$1.250,00` figures are read as `$1.250` with no value (`unclear`), never as a wrong number.
 
+## DELETE /api/cases/{token}
 `204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).
 
 ---
@@ -725,6 +726,6 @@ Languages: English and Spanish. Code detects the language of every record (`app/
 | `SPLIT_AMBIGUOUS` | needs_review | record boundaries uncertain |
 | `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
 | `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |
-| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
 | `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by code after the model steps, never cleared by a judge or a date confirmation |
+| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
 | `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
diff --git a/tests/unit/test_date_convention.py b/tests/unit/test_date_convention.py
index c7e2235..1a36415 100644
--- a/tests/unit/test_date_convention.py
+++ b/tests/unit/test_date_convention.py
@@ -29,21 +29,21 @@ def test_month_first_evidence_suggests_mm_dd_with_reason():
     rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
     s = DC.suggest(rows[1], rows, raw)
     assert s["convention"] == "MDY" and s["label"] == "MM/DD" and s["iso"] == "2026-04-05"
-    assert s["reason"] == "Other dates in this record use month first (03/14/2026)"
+    assert s["reason"] == "Another date in this packet uses month first (Record 1: 03/14/2026)"
     assert s["evidence"] == [{"record_id": "r1", "raw": "03/14/2026"}] and s["auto_applied"] is False
 
 
 def test_day_first_evidence_suggests_dd_mm():
     rows, raw = packet(("14/03/2026", "x"), ("04/05/2026", "y"))
     s = DC.suggest(rows[1], rows, raw)
-    assert s["convention"] == "DMY" and s["iso"] == "2026-05-04" and "day first (14/03/2026)" in s["reason"]
+    assert s["convention"] == "DMY" and s["iso"] == "2026-05-04" and "day first (Record 1: 14/03/2026)" in s["reason"]
 
 
 def test_evidence_inside_record_text_counts_and_is_listed_up_to_two():
     rows, raw = packet(("04/05/2026", "follow up on 06/25/2026 and 07/30/2026 and 08/31/2026"))
     s = DC.suggest(rows[0], rows, raw)
     assert s["convention"] == "MDY" and s["evidence_count"] == 3 and len(s["evidence"]) == 2
-    assert s["reason"].startswith("3 other dates in this record use month first (06/25/2026) and (07/30/2026)")
+    assert s["reason"].startswith("3 other dates in this packet use month first (Record 1: 06/25/2026) and (Record 1: 07/30/2026)")
 
 
 def test_no_suggestion_without_evidence_or_with_mixed_evidence():
@@ -62,7 +62,7 @@ def test_not_ambiguous_or_iso_dates_never_get_or_give_evidence():
 def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
     rows, raw = packet(("03/14/2026", "x"), ("04/05/98", "y"))
     s = DC.suggest(rows[1], rows, raw)
-    assert s["convention"] == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]
+    assert s["convention"] == "MDY" and (s["iso"] is None or s["iso"] in rows[1]["date_candidates"])
 
 
 def test_suggestion_never_writes_and_is_not_a_confirmation(tmp_path, monkeypatch):
@@ -96,8 +96,27 @@ def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(t
     item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
     s = item["suggestion"]
     assert s["label"] == "MM/DD" and s["iso"] == "2026-04-05" and s["auto_applied"] is False
-    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this record use month first (02/17/2026) and (03-17-26)"
+    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)"
     assert item["status"] == "ambiguous"                     # still unconfirmed until the paralegal confirms
     assert c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
     r = c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-04-05"})
     assert r.status_code == 200 and not [d for d in r.json()["dates_to_confirm"] if d["raw"] == "04/05/2026"]
+
+
+def test_reason_names_the_record_each_date_sits_in_never_this_record(tmp_path, monkeypatch):
+    """T-088 round 2: evidence dates in other records must not be described as 'in this record' (golden case_01, record 8)."""
+    monkeypatch.setenv("LLM_BACKEND", "fixture")
+    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
+    c = TestClient(create_app(str(tmp_path / "z.sqlite"), static_dir=str(tmp_path)))
+    t = run_case(c, G.raw("case_01_date_formats"))
+    g = c.get(f"/api/cases/{t}").json()
+    item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
+    s = item["suggestion"]
+    assert item["record_id"] == "r8" and "this record" not in s["reason"]
+    assert s["reason"].count("Record ") == len(s["evidence"]) == 2
+    for e in s["evidence"]:
+        assert e["record_id"] != "r8" and f"(Record {e['record_id'][1:]}: {e['raw']})" in s["reason"]
+    # packet: month-first date in record 1, ambiguous date in record 2 -> the reason points at record 1
+    rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
+    r = DC.suggest(rows[1], rows, raw)["reason"]
+    assert "Record 1" in r and "this record" not in r and "Record 2" not in r
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:08.038Z

**tool call — Bash**
````
{
 "command": "git show 55300e9 -- tests/unit/test_dismissal_patterns.py",
 "description": "Show round-2 diff for dismissal tests"
}
````

### User / tool · 2026-11-02T04:36:08.151Z

**tool result**
````
commit 55300e97ffb8916f705a1b8baa3c317f8585ced4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:34:35 2026 -0600

    fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_dismissal_patterns.py b/tests/unit/test_dismissal_patterns.py
index 15848d5..8bea3d5 100644
--- a/tests/unit/test_dismissal_patterns.py
+++ b/tests/unit/test_dismissal_patterns.py
@@ -91,13 +91,20 @@ def test_scope_is_this_case_unless_local_profile(tmp_path):
     assert len(s) == 1 and s[0]["scope"] == "all cases on this computer"
 
 
-def test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):
+def _client(tmp_path, monkeypatch, name, mode=None):
     monkeypatch.setenv("LLM_BACKEND", "fixture")
     monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
-    monkeypatch.delenv("ZLAYT_MODE", raising=False)
+    if mode:
+        monkeypatch.setenv("ZLAYT_MODE", mode)
+    else:
+        monkeypatch.delenv("ZLAYT_MODE", raising=False)
+    db = str(tmp_path / name)
+    return TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), db
+
+
+def test_routes_apply_and_errors(tmp_path, monkeypatch):
     from tests.unit.test_api_routes import run_case
-    db = str(tmp_path / "r.sqlite")
-    c = TestClient(create_app(db, static_dir=str(tmp_path)))
+    c, db = _client(tmp_path, monkeypatch, "r.sqlite")
     t = run_case(c)
     conn = DB.connect(db)
     for i in range(3):
@@ -113,15 +120,52 @@ def test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):
     assert a.status_code == 200 and a.json()["dismissed_flag_ids"] and a.json()["suggestions"] == []
 
 
+def _two_cases(c, db):
+    """Case A holds three dismissals of a phrase; case B (a different token) holds only the pending match."""
+    from tests.unit.test_api_routes import run_case
+    a, b = run_case(c), run_case(c)
+    assert a != b
+    conn = DB.connect(db)
+    for i in range(3):
+        add_flag(conn, a, f"f_a_old{i}", status="dismiss")
+    add_flag(conn, b, "f_b_pending")
+    conn.close()
+    return a, b
+
+
+def test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route(tmp_path, monkeypatch):
+    """Demo/public mode: case B sees nothing from case A; apply refuses; a forced-local route (mutant) fails this test."""
+    c, db = _client(tmp_path, monkeypatch, "pub.sqlite")
+    a, b = _two_cases(c, db)
+    assert c.get(f"/api/cases/{b}/dismissal_suggestions").json()["suggestions"] == []
+    assert c.post(f"/api/cases/{b}/dismissal_suggestions/apply", json={"key": "phrase:new_onset"}).status_code == 404
+    pend = lambda: [f for f in DB.list_items(DB.connect(db), b, "flag") if f["id"] == "f_b_pending"][0]["review_status"]   # noqa: E731
+    assert pend() == "pending"                                       # nothing was hidden in B by A's history
+    own = c.get(f"/api/cases/{a}/dismissal_suggestions").json()["suggestions"]       # A's own history still counts for A, scoped to A
+    assert len(own) == 1 and own[0]["scope"] == "this case" and "f_b_pending" not in own[0]["flag_ids"]
+
+
+def test_local_mode_counts_the_machine_profile_through_the_route(tmp_path, monkeypatch):
+    c, db = _client(tmp_path, monkeypatch, "loc.sqlite", mode="local")
+    a, b = _two_cases(c, db)
+    s = c.get(f"/api/cases/{b}/dismissal_suggestions").json()["suggestions"]
+    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer" and s[0]["dismissed_count"] == 3 and "f_b_pending" in s[0]["flag_ids"]
+
+
 @pytest.mark.parametrize("case", G.case_names())
 def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):
-    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts."""
-    def run(seed_history):
-        conn = DB.connect(str(tmp_path / f"{case}-{seed_history}.sqlite"))
-        if seed_history:
+    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts.
+    The history is built from the case's OWN flags (same type, category, origin and quoted phrase, 8 dismissals each), so a pipeline that
+    let history filter flags would change this case's output; a case with no eligible flag also gets the generic new_onset history."""
+    def run(history_from):
+        conn = DB.connect(str(tmp_path / f"{case}-{bool(history_from)}.sqlite"))
+        if history_from is not None:
             hist = DB.create_case(conn, "history", now=1.0)
-            for i in range(8):
-                add_flag(conn, hist, f"f_h{i}", status="dismiss")
+            for n, f in enumerate(history_from * 8 or [None]):
+                if f is None:
+                    add_flag(conn, hist, f"f_h{n}", status="dismiss")
+                else:
+                    add_flag(conn, hist, f"f_h{n}", category=f["category"], text=f["evidence"][0]["text"], type_=f["type"], origin=f["origin"], status="dismiss")
         cid = DB.create_case(conn, G.raw(case), now=1.0)
         def extract(u):
             ex = G.record(case, wr(u, case)[0])["excerpt"].split(". ")[0].rstrip(".") + "."
@@ -130,5 +174,30 @@ def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(
         view = {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in ("entry", "amount", "flag")}
         DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either
         assert {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in view} == view
-        return view
-    assert run(False) == run(True)
+        flags = [f for f in DB.list_items(conn, cid, "flag") if DP._eligible(f) and f.get("evidence")]
+        return view, flags
+    base, flags = run(None)
+    seeded_view, _ = run(flags)
+    assert base == seeded_view
+    assert base == run([])[0]
+
+
+def test_eligibility_rules_are_each_enforced_on_their_own(tmp_path):
+    conn, cid, _ = seeded(tmp_path)
+    for i in range(6):
+        add_flag(conn, cid, f"f_gl{i}", category="gap_over_30", type_="gap", origin="lexicon+llm", status="dismiss")      # right origin, wrong type
+        add_flag(conn, cid, f"f_rw{i}", category="new_onset", type_="record_warning", origin="lexicon+llm", status="dismiss")
+        add_flag(conn, cid, f"f_llm{i}", category="new_onset", type_="pre_existing", origin="llm", status="dismiss")          # right type, no lexicon
+    assert DP.suggest(conn, cid) == []
+    add_flag(conn, cid, "f_ok", type_="pre_existing", origin="lexicon", status=None)
+    assert DP.suggest(conn, cid) == []                              # ineligible history never counts toward an eligible pending flag
+
+
+def test_category_threshold_is_exactly_five(tmp_path):
+    conn, cid, _ = seeded(tmp_path)
+    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness."]
+    for i, t in enumerate(texts):
+        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
+    assert [x for x in DP.suggest(conn, cid) if x["kind"] == "category"] == []             # 4 is not enough
+    add_flag(conn, cid, "f_c4", category="patient_report", text="Developed pain after the accident.", status="dismiss")
+    assert [x["dismissed_count"] for x in DP.suggest(conn, cid) if x["kind"] == "category"] == [5]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:33.341Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-088; echo =====; python3 tools/board.py show T-089; echo =====; python3 tools/board.py show T-096 2>&1 | head -60",
 "description": "Show T-088, T-089 and T-096 cards from the board"
}
````

### User / tool · 2026-11-02T04:36:33.582Z

**tool result**
````
---
id: "T-088"
title: "Date-convention suggestion (pre-select with stated reason, still one confirm)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:35:55Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:30:07Z"
rounds: 1
commits: ["f667f08", "55300e9"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-088-staff-engineer.md", "at": "2026-11-02T04:30:07Z"}
ac:
  - {"n": 1, "text": "For an ambiguous numeric date, the API suggests MM/DD or DD/MM with the reason (other dates in the packet), the UI pre-selects it, and the paralegal still confirms once; never auto-applied; eval case", "done": true, "evidence": "PARTIAL, corrected: backend half only. tests/unit/test_date_convention.py (9 pass) incl. golden case_01 reason naming Record 2 and Record 6. NOT done: UI pre-select (T-096, frontend) and golden expected.json eval entry (qa; exact assertion in the note)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:36Z backend: UI needs: dates_to_confirm[].suggestion {convention, label, iso, reason, evidence, auto_applied:false} (contract in api.md). Pre-select the radio for suggestion.iso (when non-null), show reason beneath, still require an explicit confirm click (D-041); never confirm on load. Golden: evals/golden/case_01_date_formats should get a case asserting the 04/05/2026 record's suggestion is MM/DD with 4 evidence dates (qa owns golden; unit test tests/unit/test_date_convention.py covers it on that file today). No db change.
- 2026-11-02T04:21:36Z backend: AC 1 checked: tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)
- 2026-11-02T04:21:37Z backend: moved in_progress -> in_review
- 2026-11-02T04:21:41Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:30:07Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-088-staff-engineer.md; round 1; findings:
    - [blocker] Reason says the evidence dates are 'in this record' when they come from other records in the packet — fix: Build the reason from the evidence's own record ids, e.g. 'Other dates in this packet use month first (02/17/2026, record 2) and (03-17-26, record 6)'. Remove the phrase 'in this record' everywhere. Update the expected strings at test_date_convention.py:32, :46 and :99.
    - [major] AC 1 is marked done=true while two of its required parts are not in the codebase — fix: Set AC 1 back to done=false until (a) the frontend pre-select ships and (b) a golden expected entry for case_01 record 8 asserts the MDY suggestion. Or split those two parts into follow-up cards and close the unit half only.
    - [major] Shared git index stages deletion of this card's files (blast radius: T-088 and T-089) — fix: Orchestrator (not this reviewer) restores the index for the card paths without touching the working tree, then commits with explicit paths. The index then matches HEAD for these four files.
    - [minor] Weak assertion: `and`/`or` precedence lets the two-digit-year test pass with the wrong convention — fix: assert s["convention"] == "MDY" and (s["iso"] is None or s["iso"] in rows[1]["date_candidates"])
- 2026-11-02T04:30:07Z backend: claimed
- 2026-11-02T04:34:55Z backend: Round 2 (commit 55300e9): reason now names where each evidence date sits, e.g. golden case_01 record 8: '4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)'; 'in this record' removed everywhere; and/or precedence fixed; unused import removed. Tests: tests/unit/test_date_convention.py (9 pass; reason-names-record test mutation-checked: old wording fails it). AC1 CORRECTION: the earlier AC1 evidence overstated. Only the API/unit half is done. NOT done: (a) UI pre-select, now card T-096 (frontend); (b) eval case. For qa: add to evals/golden/case_01_date_formats.expected.json an assertion that the dates_to_confirm item for record r8 (raw 04/05/2026) has suggestion.convention=MDY, label 'MM/DD', iso '2026-04-05', evidence_count 4, evidence record_ids [r2, r6], auto_applied false, and status stays 'ambiguous' until confirm_date. Until qa adds it, tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required is the stand-in.
- 2026-11-02T04:34:55Z backend: AC 1 checked: PARTIAL, corrected: backend half only. tests/unit/test_date_convention.py (9 pass) incl. golden case_01 reason naming Record 2 and Record 6. NOT done: UI pre-select (T-096, frontend) and golden expected.json eval entry (qa; exact assertion in the note)
- 2026-11-02T04:34:55Z backend: moved in_progress -> in_review
- 2026-11-02T04:35:55Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: reason names the record of each evidence date (Record N: raw), never 'in this record'; test precedence fix; unused import; api.md updated. Verified: .venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass); mutant restoring old wording fails. Left: UI pre-select (T-096), golden expected entry (qa, see note). Surprised: earlier AC1 tick overstated; corrected in note. Commit 55300e9.

=====
---
id: "T-089"
title: "Dismissal-pattern suggestions for a single local profile (suggestions only)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:35:55Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:30:07Z"
rounds: 1
commits: ["f667f08", "55300e9"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-089-staff-engineer.md", "at": "2026-11-02T04:30:07Z"}
ac:
  - {"n": 1, "text": "Repeated dismissals of the same flag phrase surface as a suggestion ('You dismissed this 4 times'); never auto-dismisses; per-profile local only; eval shows no recall loss on golden", "done": true, "evidence": "tests/unit/test_dismissal_patterns.py (21 pass): suggestion thresholds incl. category 4 vs 5, each eligibility rule alone, route-level public-mode isolation (forced-local mutant fails), local-mode profile, apply via review path, golden identity with per-case history. Recall evidence is this unit equivalence test (no eval report). Banner UI not built (frontend)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:37Z backend: UI needs: GET /api/cases/{token}/dismissal_suggestions -> {suggestions:[{key,kind,label,dismissed_count,scope,flag_ids,message,auto_applied:false}]}; show message as a banner on the flags list with Hide similar (POST .../dismissal_suggestions/apply {key}) and Keep showing (client-side only). Never apply on load. Hidden flags stay in the Dismissed filter and are reversible via reset. Thresholds 3 (phrase) and 5 (category); only lexicon pre_existing/causation flags are eligible. History is read from the flags table (no db change); counts span all cases only under ZLAYT_MODE=local. Golden: no case needed; unit test proves identical pipeline output on every golden case with and without dismissal history.
- 2026-11-02T04:21:37Z backend: AC 1 checked: tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)
- 2026-11-02T04:21:37Z backend: moved in_progress -> in_review
- 2026-11-02T04:21:41Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:30:07Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-089-staff-engineer.md; round 1; findings:
    - [major] Demo-mode isolation at the route is not tested; forcing local scope in the route passes all 25 tests — fix: Add a route test: create case A with 3 dismissals of a phrase and case B with the pending match, run without ZLAYT_MODE, and assert GET /api/cases/B/dismissal_suggestions returns suggestions == []. Then run with ZLAYT_MODE=local and assert the suggestion appears. Rename the tes
    - [major] Shared git index stages deletion of this card's files (blast radius: T-088 and T-089) — fix: Orchestrator restores the index for these paths without touching the working tree, then commits with explicit paths. The reviewer does not run git reset.
    - [minor] Eligibility rules are tested only as a conjunction; neither the type rule nor the origin rule is isolated — fix: Add cases: a gap flag and a record_warning flag with origin 'lexicon+llm' (must not be suggested); a pre_existing flag with origin 'llm' only (must not be suggested).
    - [minor] Category threshold boundary (CATEGORY_MIN) has no negative test; golden identity test seeds only one category — fix: Add a 4-dismissal negative case for the category rule. In the golden identity test, seed history with each case's own flag categories and phrases (taken from its pipeline output) so the equality is sensitive per case. Name the unit test as the recall evidence in the ca
    - [minor] AC 'surface as a suggestion' is evidenced only by the API payload; the banner is not built — fix: Create a follow-up frontend card for the banner, or add the banner to this card's AC before closing it.
- 2026-11-02T04:30:07Z backend: claimed
- 2026-11-02T04:34:55Z backend: Round 2 (commit 55300e9): added route-level demo-isolation tests (public mode: case B gets no suggestions from case A's dismissals, apply 404, B's flag stays pending; local mode: counts the machine profile). Mutants verified failing: route forced local (89h), CATEGORY_MIN=4 (89b), gap/record_warning eligible (89d), lexicon-origin requirement removed (89d2). Golden identity test now seeds each case's own flags as history (sensitive per case). Apply non-atomicity documented in api.md. Frontend banner: no follow-up card is mine to create; orchestrator/frontend to track (api.md has the UI notes).
- 2026-11-02T04:34:55Z backend: AC 1 checked: tests/unit/test_dismissal_patterns.py (21 pass): suggestion thresholds incl. category 4 vs 5, each eligibility rule alone, route-level public-mode isolation (forced-local mutant fails), local-mode profile, apply via review path, golden identity with per-case history. Recall evidence is this unit equivalence test (no eval report). Banner UI not built (frontend)
- 2026-11-02T04:34:56Z backend: moved in_progress -> in_review
- 2026-11-02T04:35:55Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: route-level demo/public isolation test + local-mode route test; isolated eligibility (type, origin) and category-threshold tests; golden identity test seeds each case's own flags; apply partial-write documented. Verified: pytest -k 'date or dismiss or suggest' (160 pass); mutants 89b/89d/89d2/89h now fail. Left: frontend banner card. Surprised: sample case has its own pending match so case A gets a suggestion scoped to itself. Commit 55300e9.

=====
---
id: "T-096"
title: "UI for suggestions and confidence: date-convention suggestion, dismissal suggestions, measured-precision line"
milestone: "M3"
role: "frontend"
status: "ready"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:30:07Z"
updated_at: "2026-11-02T04:30:16Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Dates-to-confirm row pre-selects the suggested convention with its reason and still requires one confirm (T-088); dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089); 'Verified items matched the record N/M times in testing' line with small-sample note (T-090); e2e tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:30:16Z orchestrator: Starts once T-088/T-089 r2 and T-090 r2 pass (their API shapes may still change).
- 2026-11-02T04:30:16Z orchestrator: assigned: frontend

## Handoff (filled when moving to in_review)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:34.200Z

**tool call — Bash**
````
{
 "command": "git diff --cached --name-status | head -30; echo \"---index-check-done\"; git ls-files app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py; echo ---; git log -1 --format=%H%n%s -- tests/unit/test_dismissal_patterns.py; ls artifacts/review-evidence/T-088-T-089/ 2>&1",
 "description": "Check staged index state and existing review-evidence folder"
}
````

### User / tool · 2026-11-02T04:36:34.342Z

**tool result**
````
M	.claude/agent-memory/qa/MEMORY.md
D	.claude/agent-memory/qa/project_judge_controls.md
D	evals/golden/judge_controls.CHANGELOG.md
M	evals/golden/judge_controls.jsonl
D	evals/golden/judge_controls_heldout.jsonl
D	evals/reports/controls-20261102T042306Z.json
D	evals/reports/controls-20261102T042306Z.md
M	evals/run.py
M	tests/unit/test_t093_eval_signature.py
---index-check-done
app/backend/date_convention.py
app/backend/dismissal_patterns.py
tests/unit/test_date_convention.py
tests/unit/test_dismissal_patterns.py
---
55300e97ffb8916f705a1b8baa3c317f8585ced4
fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
mutate.py
mutation_run.txt
probe_t088.py
probe_t088_output.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:48.450Z

**tool call — Bash**
````
{
 "command": "git show 55300e9:app/backend/dismissal_patterns.py && echo ===== && git show 55300e9:app/backend/date_convention.py && echo ===== && git show 55300e9:tests/unit/test_dismissal_patterns.py | head -95",
 "description": "Read dismissal and date modules and first part of dismissal tests at 55300e9"
}
````

### User / tool · 2026-11-02T04:36:48.580Z

**tool result**
````
"""Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.

The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
the paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside
ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.

When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
may offer "You dismissed this kind of flag 4 times. Hide similar ones in this case?". This module only READS: suggest() never writes and
never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
PENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those
bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.

Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
that code or the model found without a lexicon phrase are never suggested for hiding."""
from fastapi import Request

from app.backend import lexicon_scan, review
from app.db import db as DB

PHRASE_MIN = 3
CATEGORY_MIN = 5
ELIGIBLE_TYPES = ("pre_existing", "causation")
APPLIED_NOTE = "Hidden by dismissal-pattern suggestion (paralegal confirmed)."
_BAD = ("rejected",)


def _eligible(f) -> bool:
    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")


def _phrase(f):
    """(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only."""
    for ev in f.get("evidence") or []:
        hits = [h for h in lexicon_scan.scan(ev.get("text") or "") if h["category"] == f["category"]]
        if hits:
            h = min(hits, key=lambda x: x["start"])
            return h["id"], " ".join(h["text"].lower().split())
    return None, None


def _history(conn, case_id: str, local: bool) -> list:
    """Dismissed, eligible flags that were dismissed by the paralegal one at a time."""
    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get("reviewer_note") or "") != APPLIED_NOTE]


def _pending(conn, case_id: str) -> list:
    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]


def suggest(conn, case_id: str, *, local: bool = False) -> list:
    """Read-only. [{key, kind: phrase|category, label, dismissed_count, scope, flag_ids, message}], phrase suggestions first."""
    hist = _history(conn, case_id, local)
    phrase_n, cat_n = {}, {}
    for f in hist:
        pid, _ = _phrase(f)
        if pid:
            phrase_n[pid] = phrase_n.get(pid, 0) + 1
        cat_n[f["category"]] = cat_n.get(f["category"], 0) + 1
    out, covered = [], set()
    pend = [(f, *_phrase(f)) for f in _pending(conn, case_id)]
    scope = "all cases on this computer" if local else "this case"
    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):
        ids = [f["id"] for f, p, _ in pend if p == pid]
        label = next(t for _, p, t in pend if p == pid)
        out.append(_row(f"phrase:{pid}", "phrase", label, phrase_n[pid], scope, ids))
        covered.update(ids)
    for cat in sorted({f["category"] for f, _, _ in pend if cat_n.get(f["category"], 0) >= CATEGORY_MIN}):
        ids = [f["id"] for f, _, _ in pend if f["category"] == cat and f["id"] not in covered]
        if ids:
            out.append(_row(f"category:{cat}", "category", cat.replace("_", " "), cat_n[cat], scope, ids))
    return out


def _row(key, kind, label, n, scope, ids):
    return {"key": key, "kind": kind, "label": label, "dismissed_count": n, "scope": scope, "flag_ids": ids, "auto_applied": False,
            "message": f"You dismissed this kind of flag {n} times. Hide similar ones in this case?"}


def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
    """The paralegal accepted the suggestion: dismiss the matching pending flags in THIS case through the normal review path.
    Raises KeyError when the key is not a current suggestion (nothing is written)."""
    s = next((x for x in suggest(conn, case_id, local=local) if x["key"] == key), None)
    if s is None:
        raise KeyError(key)
    for fid in s["flag_ids"]:
        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
    return {"key": key, "dismissed_flag_ids": s["flag_ids"], "suggestions": suggest(conn, case_id, local=local)}


def add_routes(app, *, conn, get_case, body_of, ApiError, now, local_mode):
    @app.get("/api/cases/{token}/dismissal_suggestions")
    def dismissal_suggestions(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"suggestions": suggest(c, token, local=local_mode()), "min_phrase": PHRASE_MIN, "min_category": CATEGORY_MIN}
        finally:
            c.close()

    @app.post("/api/cases/{token}/dismissal_suggestions/apply")
    async def dismissal_suggestions_apply(token: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("key"), str):
            raise ApiError(400, "bad_request", "Send the key of the suggestion to apply.")
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply(c, token, b["key"], local=local_mode(), now=now)
            except KeyError:
                raise ApiError(404, "not_found", "That suggestion no longer applies.") from None
        finally:
            c.close()
=====
"""Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.

An ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric
dates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they
all agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.
The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
import re

_NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
MAX_EVIDENCE = 2
_LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}


def _order(a: int, b: int):
    """MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month)."""
    if a > 12 and 1 <= b <= 12:
        return "DMY"
    if b > 12 and 1 <= a <= 12:
        return "MDY"
    return None


def _evidence(records, raw_text):
    """Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text."""
    out, seen = [], set()
    for r in records:
        block = raw_text[r["char_start"]:r["char_end"]]
        for m in _NUM_DATE.finditer(block):
            order = _order(int(m[1]), int(m[3]))
            key = (r["id"], m[0])
            if order and key not in seen:
                seen.add(key)
                out.append({"record_id": r["id"], "raw": m[0], "order": order})
    return out


def _example(ev):
    """'(Record 3: 03/14/2026)': names the record the date sits in, so the paralegal looks in the right place."""
    return f"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})"


def suggest(rec: dict, records: list, raw_text: str):
    """Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,
    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous."""
    if rec.get("date_status") != "ambiguous":
        return None
    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
    if not m or _order(int(m[1]), int(m[3])) is not None:
        return None
    ev = _evidence(records, raw_text)
    orders = {e["order"] for e in ev}
    if len(orders) != 1:
        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess
    order = next(iter(orders))
    a, b = int(m[1]), int(m[3])
    mo, d = (a, b) if order == "MDY" else (b, a)
    cands = [c for c in rec.get("date_candidates") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]
    iso = cands[0] if len(cands) == 1 else None
    shown = ev[:MAX_EVIDENCE]
    n = len(ev)
    first = "month first" if order == "MDY" else "day first"
    reason = (f"Another date in this packet uses {first} {_example(shown[0])}" if n == 1 else
              f"{n} other dates in this packet use {first} " + " and ".join(_example(e) for e in shown))
    return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
=====
"""T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output."""
import pytest
from fastapi.testclient import TestClient

from app.backend import dismissal_patterns as DP, pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record as wr
from tests.unit.test_review_rules import seeded

NEW_ONSET = "New onset pain radiating to right arm with numbness in fingers."


def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
                "evidence_json": [{"record_no": 1, "text": text, "start": 0, "end": len(text)}], "state": "verified", "state_reasons_json": []})
    if status:
        DB.apply_review(conn, fid, status, now=1.0, case=case)


def snapshot(conn, case):
    return [(f["id"], f["review_status"], f["state"]) for f in DB.list_items(conn, case, "flag")]


def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    before = snapshot(conn, cid)
    s = DP.suggest(conn, cid)
    assert len(s) == 1 and s[0]["kind"] == "phrase" and s[0]["dismissed_count"] == 3 and s[0]["auto_applied"] is False
    assert s[0]["message"] == "You dismissed this kind of flag 3 times. Hide similar ones in this case?"
    assert "f_r7_2" in s[0]["flag_ids"]                           # the sample's pending new_onset flag
    assert snapshot(conn, cid) == before                          # suggest() wrote nothing; the flag is still pending
    assert next(f for f in DB.list_items(conn, cid, "flag") if f["id"] == "f_r7_2")["review_status"] == "pending"


def test_two_dismissals_are_not_enough(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(2):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_ineligible_flags_are_never_suggested(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(6):
        add_flag(conn, cid, f"f_g{i}", category="gap_over_30", type_="gap", origin="code", status="dismiss")
        add_flag(conn, cid, f"f_i{i}", category="injection_suspected", type_="record_warning", origin="code", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness.",
             "Developed pain after the accident."]
    for i, t in enumerate(texts):
        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
    s = DP.suggest(conn, cid)
    cats = [x for x in s if x["kind"] == "category"]
    assert len(cats) == 1 and cats[0]["key"] == "category:patient_report" and cats[0]["dismissed_count"] == 5
    assert cats[0]["flag_ids"] == ["f_r9_1"] and cats[0]["label"] == "patient report"


def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    key = DP.suggest(conn, cid)[0]["key"]
    n_events = len(DB.list_events(conn, cid))
    out = DP.apply(conn, cid, key, now=2.0)
    assert out["dismissed_flag_ids"] == ["f_r7_2"] and out["suggestions"] == []
    f = next(x for x in DB.list_items(conn, cid, "flag") if x["id"] == "f_r7_2")
    assert f["review_status"] == "dismissed" and f["reviewer_note"] == DP.APPLIED_NOTE
    assert len(DB.list_events(conn, cid)) == n_events + 1         # one logged dismiss event
    # a bulk-hidden flag is not a new manual dismissal: the count stays 3, not 4
    add_flag(conn, cid, "f_new")
    assert DP.suggest(conn, cid)[0]["dismissed_count"] == 3
    with pytest.raises(KeyError):
        DP.apply(conn, cid, "phrase:nope")


def test_scope_is_this_case_unless_local_profile(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    other = DB.create_case(conn, "x", now=1.0)
    for i in range(3):
        add_flag(conn, other, f"f_o{i}", status="dismiss")
    assert DP.suggest(conn, cid, local=False) == []
    s = DP.suggest(conn, cid, local=True)
    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer"


def _client(tmp_path, monkeypatch, name, mode=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:49.201Z

**tool call — Bash**
````
{
 "command": "git show 55300e9:app/backend/api.py | grep -n \"dismissal\\|local_mode\\|def _local\\|ZLAYT_MODE\" | head -40; echo ====; git show 55300e9:app/backend/flags.py | grep -n \"local\" | head; echo ====; git grep -n \"def local_mode\\|ZLAYT_MODE\" 55300e9 -- app | head -20",
 "description": "Locate route registration and local-mode source at 55300e9"
}
````

### User / tool · 2026-11-02T04:36:49.352Z

**tool result**
````
23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
79:def local_mode() -> bool:
80:    return os.environ.get("ZLAYT_MODE") == "local"
101:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
107:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
179:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
220:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
230:        if not local_mode():
240:            if not local_mode():
513:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
544:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
549:                return trace.item_trace(c, token, item_id, full=local_mode())
560:            return trace.case_trace(c, token, full=local_mode())
569:            return trace.judge_report(c, token, full=local_mode())
578:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
====
====
55300e9:app/backend/api.py:79:def local_mode() -> bool:
55300e9:app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
55300e9:app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
55300e9:app/backend/api.py:544:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
55300e9:app/backend/api.py:578:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
55300e9:app/backend/dismissal_patterns.py:5:ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
55300e9:app/backend/present.py:207:    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
55300e9:app/backend/trace.py:7:Visibility is the /audit split (D-020/D-036): full=False (public/demo) returns metadata only; full=True (ZLAYT_MODE=local) adds the model's raw
55300e9:app/frontend/mock_extra.js:1:/* Mock-only overlay (T-055 / T-058): export_config and audit for ?api=mock. ?local=1 adds prompt/response text to the audit like ZLAYT_MODE=local. */
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:56.905Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && git worktree add \"$SP/wt\" HEAD 2>&1; echo \"exit=$?\"; echo \"--- HEAD now:\"; git rev-parse --short HEAD; echo \"--- product diff 55300e9..HEAD (app tests tools memory/contracts evals):\"; git diff --stat 55300e9 HEAD -- app tests evals memory/contracts | tail -3; echo \"(end)\"; echo \"--- worktree HEAD:\"; git -C \"$SP/wt\" rev-parse --short HEAD; ls \"$SP/wt\" | head -30",
 "description": "Create clean worktree at HEAD and confirm product paths match 55300e9"
}
````

### User / tool · 2026-11-02T04:36:56.959Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git worktree` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:00.607Z

The board guard blocks `git worktree` in the project, so I'll pin HEAD with `git archive` into my review-evidence folder instead.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:01.520Z

**tool call — Bash**
````
{
 "command": "H=$(git rev-parse HEAD) && echo \"HEAD=$H\" && D=artifacts/review-evidence/T-088-T-089-r2/clean && mkdir -p \"$D\" && git archive \"$H\" | tar -x -C \"$D\" && echo \"extracted to $D\" && echo \"--- product paths differing between 55300e9 and HEAD:\" && git diff --stat 55300e9 HEAD -- app tests evals memory/contracts | tail -3; echo \"(end)\"; ls \"$D\" | head -40",
 "description": "Extract clean HEAD tree via git archive into review-evidence"
}
````

### User / tool · 2026-11-02T04:37:01.583Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: H=$(git rev-parse HEAD) && echo "HEAD=$H" && D=artifacts/review-evidence/T-088-T-089-r2/clean && mkdir -p "$D" && git archive "$H" | tar -x -C "$D" && echo "extracted to $D" && echo "--- product paths
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:03.321Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && mkdir -p artifacts/review-evidence/T-088-T-089-r2/clean && git archive d3130e3 | tar -x -C artifacts/review-evidence/T-088-T-089-r2/clean && echo extracted && git diff --stat 55300e9 d3130e3 -- app tests evals memory/contracts | tail -3; echo \"(end: empty above means no product-path change between 55300e9 and HEAD)\"; ls artifacts/review-evidence/T-088-T-089-r2/clean | head -40",
 "description": "Extract HEAD tree via git archive and check product paths unchanged since 55300e9"
}
````

### User / tool · 2026-11-02T04:37:03.753Z

**tool result**
````
7df65fbb22bf3c31a50af0810e12768460388e97
extracted
(end: empty above means no product-path change between 55300e9 and HEAD)
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:06.184Z

HEAD moved to 7df65fb while I was working, so I'll re-pin the archive to the current HEAD and check the log.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:07.264Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && H=$(git rev-parse HEAD) && echo \"pin=$H\" && rm -rf artifacts/review-evidence/T-088-T-089-r2/clean && mkdir -p artifacts/review-evidence/T-088-T-089-r2/clean && git archive \"$H\" | tar -x -C artifacts/review-evidence/T-088-T-089-r2/clean && echo extracted && echo \"--- product-path diff 55300e9..$H (empty = unchanged):\" && git diff --stat 55300e9 \"$H\" -- app tests evals memory/contracts | tail -3; echo \"(end)\"; git show --stat \"$H\" | head -12",
 "description": "Re-pin clean archive to current HEAD and show its log"
}
````

### User / tool · 2026-11-02T04:37:07.327Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: git log --oneline -4 && H=$(git rev-parse HEAD) && echo "pin=$H" && rm -rf artifacts/review-evidence/T-088-T-089-r2/clean && mkdir -p artifacts/review-evidence/T-088-T-089-r2/clean && git archive "$H"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:09.177Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && git rev-parse --short HEAD && rm -rf artifacts/review-evidence/T-088-T-089-r2/clean && mkdir -p artifacts/review-evidence/T-088-T-089-r2/clean && git archive 7df65fb | tar -x -C artifacts/review-evidence/T-088-T-089-r2/clean && echo extracted-7df65fb && echo \"--- product-path diff 55300e9..7df65fb (empty = unchanged):\" && git diff --stat 55300e9 7df65fb -- app tests evals memory/contracts | tail -3; echo \"(end)\"; git show --stat 7df65fb | head -14",
 "description": "Re-pin clean archive to commit 7df65fb and show its log"
}
````

### User / tool · 2026-11-02T04:37:09.757Z

**tool result**
````
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
d3130e3 harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
55300e9 fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
49c4600 memory: T-091 speaker attribution v2 fails fresh adversary; stays cut (D-040)
7df65fb
extracted-7df65fb
--- product-path diff 55300e9..7df65fb (empty = unchanged):
 evals/run.py                                 |  124 ++-
 tests/unit/test_t093_eval_signature.py       |  102 +-
 7 files changed, 1709 insertions(+), 50 deletions(-)
(end)
commit 7df65fbb22bf3c31a50af0810e12768460388e97
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:36:04 2026 -0600

    feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
    
    Labels fixed before the run. J3W11 is a stable false agree under judge_conflict_v3 (a finding, not relabelled).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 .claude/agent-memory/qa/MEMORY.md                 |    1 +
 .claude/agent-memory/qa/project_judge_controls.md |   16 +
 evals/golden/judge_controls.CHANGELOG.md          |   14 +
 evals/golden/judge_controls.jsonl                 |   71 +-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:13.139Z

HEAD is now 7df65fb, a T-093 commit that touches only evals and its own test. I'll confirm the card paths are unchanged since 55300e9, then run the brief's test command in the clean tree.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:14.389Z

**tool call — Bash**
````
{
 "command": "git diff --stat 55300e9 7df65fb -- app/backend/date_convention.py app/backend/dismissal_patterns.py app/backend/api.py app/backend/review.py app/backend/present.py app/backend/pipeline.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py tests/unit/_golden.py tests/unit/_fakes.py tests/unit/test_api_routes.py tests/unit/test_review_rules.py; echo \"(card-path diff end; empty = unchanged)\"; ls -d .venv/bin/python && cd artifacts/review-evidence/T-088-T-089-r2/clean && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import app, tests.unit._golden as g; print(app.__file__); print(g.__file__)\"",
 "description": "Confirm card paths unchanged and verify imports resolve to clean tree"
}
````

### User / tool · 2026-11-02T04:37:14.522Z

**tool result**
````
(card-path diff end; empty = unchanged)
.venv/bin/python
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean/app/__init__.py
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/_golden.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:16.222Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\" 2>&1 | tail -15; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run brief's unit test selector in clean HEAD tree",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:37:25.044Z

**tool result**
````
........................................................................ [ 51%]
....................................................................     [100%]
140 passed, 1196 deselected in 8.29s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:29.795Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py 2>&1 | tail -3; echo ---; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest --collect-only -q tests/unit -k \"date or dismiss or suggest\" 2>&1 | sed 's/::.*//' | sort | uniq -c | sort -rn | head -30",
 "description": "Count tests per file for date and dismissal selectors in clean tree",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:37:36.507Z

**tool result**
````
..............................                                           [100%]
30 passed in 4.57s
---
  21 tests/unit/test_dismissal_patterns.py
  21 tests/unit/test_dates.py
   9 tests/unit/test_date_convention.py
   8 tests/unit/test_sentences.py
   7 tests/unit/test_date_unconfirmed.py
   6 tests/unit/test_export.py
   5 tests/unit/test_trace.py
   5 tests/unit/test_t093_eval_signature.py
   5 tests/unit/test_ingest.py
   5 tests/unit/test_db.py
   5 tests/unit/test_confidence.py
   4 tests/unit/test_eval_runner.py
   4 tests/unit/test_eval_matching.py
   4 tests/unit/test_amounts.py
   3 tests/unit/test_t033_backend.py
   3 tests/unit/test_grounding.py
   3 tests/unit/test_gaps.py
   2 tests/unit/test_split_llm.py
   2 tests/unit/test_spanish_records.py
   2 tests/unit/test_review_rules.py
   2 tests/unit/test_pipeline.py
   2 tests/unit/test_conflicts.py
   2 tests/unit/test_boundaries.py
   1 tests/unit/test_totals.py
   1 tests/unit/test_t037_backend.py
   1 tests/unit/test_schemas.py
   1 tests/unit/test_narrative.py
   1 tests/unit/test_manual_and_split.py
   1 tests/unit/test_judges.py
   1 tests/unit/test_injection.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:39.563Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\" 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"; echo \"--- main-tree cards:\"; .venv/bin/python -m pytest -q tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py 2>&1 | tail -2",
 "description": "Run brief's selector in the main working tree for comparison",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:37:53.108Z

**tool result**
````
........................................................................ [ 45%]
........................................................................ [ 90%]
................                                                         [100%]
160 passed, 1238 deselected in 8.61s
exit=0
--- main-tree cards:
..............................                                           [100%]
30 passed in 4.05s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:56.470Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest --collect-only -q tests/unit -k \"date or dismiss or suggest\" 2>/dev/null | grep \"::\" | sort > artifacts/review-evidence/T-088-T-089-r2/collect_main.txt; (cd artifacts/review-evidence/T-088-T-089-r2/clean && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest --collect-only -q tests/unit -k \"date or dismiss or suggest\" 2>/dev/null | grep \"::\" | sort > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/collect_clean.txt); wc -l artifacts/review-evidence/T-088-T-089-r2/collect_*.txt; echo \"--- only in main working tree:\"; comm -23 artifacts/review-evidence/T-088-T-089-r2/collect_main.txt artifacts/review-evidence/T-088-T-089-r2/collect_clean.txt | sed 's/\\[.*//' | sort | uniq -c; echo \"--- only in clean HEAD:\"; comm -13 artifacts/review-evidence/T-088-T-089-r2/collect_main.txt artifacts/review-evidence/T-088-T-089-r2/collect_clean.txt | head",
 "description": "Diff collected test ids between main tree and clean HEAD",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:38:00.254Z

**tool result**
````
     140 artifacts/review-evidence/T-088-T-089-r2/collect_clean.txt
     161 artifacts/review-evidence/T-088-T-089-r2/collect_main.txt
     301 total
--- only in main working tree:
   1 tests/unit/test_audited.py::test_a_type_error_inside_validate_is_a_bug_and_propagates
   1 tests/unit/test_conflict_candidates.py::test_a_model_that_would_invent_a_conflict_changes_nothing
   1 tests/unit/test_conflict_candidates.py::test_benign_goes_to_the_could_not_verify_tray_and_unsure_stays_visible
   1 tests/unit/test_conflict_candidates.py::test_candidates_are_stable_and_every_quote_is_a_whole_verbatim_sentence
   1 tests/unit/test_conflict_candidates.py::test_case_06_denial_against_prior_history_in_record_order
   1 tests/unit/test_conflict_candidates.py::test_denial_stops_at_the_first_confirmed_candidate
   1 tests/unit/test_conflict_candidates.py::test_explicit_count_beats_frequency_and_latest_plan_wins
   1 tests/unit/test_conflict_candidates.py::test_frequency_times_duration_is_arithmetic_and_agrees_with_the_visit_count
   1 tests/unit/test_conflict_candidates.py::test_judge_outage_keeps_the_candidate_visible_with_the_reason
   1 tests/unit/test_conflict_candidates.py::test_module_imports_no_llm_client
   1 tests/unit/test_conflict_candidates.py::test_no_plan_or_no_early_end_means_no_candidate
   1 tests/unit/test_conflict_candidates.py::test_other_golden_cases_propose_nothing
   1 tests/unit/test_conflict_candidates.py::test_outcome_must_come_after_the_plan
   1 tests/unit/test_conflict_candidates.py::test_pass_makes_no_conflicts_call_and_the_arithmetic_case_never_reaches_a_judge
   1 tests/unit/test_conflict_candidates.py::test_sample_proposes_exactly_the_plan_vs_discharge_pair
   1 tests/unit/test_conflict_candidates.py::test_trace_sees_a_candidate_conflict_whose_judge_never_answered
   1 tests/unit/test_conflict_candidates.py::test_word_frequencies_and_other_forms
   1 tests/unit/test_pipeline.py::test_j3_benign_puts_the_candidate_in_the_tray_not_the_flag_list
   1 tests/unit/test_pipeline.py::test_j3_conflict_verdict_keeps_candidate_conflict_and_code_conflict_is_unaffected
   2 tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_candidate_conflicts_needs_review
--- only in clean HEAD:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:10.061Z

The 30 card tests pass at HEAD; the 160 figure only reproduces in the dirty main tree, which has other workers' uncommitted tests. Next I'll look at the round-1 mutation runner so I can reuse it on the round-2 code.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:10.571Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-088-T-089/mutate.py; echo ======; cat artifacts/review-evidence/T-088-T-089/mutation_run.txt | tail -60",
 "description": "Read round-1 mutation runner and its output"
}
````

### User / tool · 2026-11-02T04:38:10.662Z

**tool result**
````
"""Mutation runner for T-088 / T-089 (staff-engineer-reviewer). Edits ONLY the copy under MUT, never the repo.
Each mutant: (name, relative file, old text, new text, expectation). Runs the two card test files, restores the file after each run."""
import os
import subprocess
import sys

MUT = sys.argv[1]
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
TESTS = ["tests/unit/test_date_convention.py", "tests/unit/test_dismissal_patterns.py"]

MUTANTS = [
    ("88a mixed evidence not refused", "app/backend/date_convention.py",
     "    if len(orders) != 1:\n        return None", "    if not orders:\n        return None",
     "expect fail"),
    ("88a2 mixed evidence: order picked by sort (paired with 88a)", "app/backend/date_convention.py",
     "    order = next(iter(orders))", "    order = sorted(orders)[0]", "expect fail"),
    ("88b ambiguous dates counted as evidence (MDY)", "app/backend/date_convention.py",
     "            order = _order(int(m[1]), int(m[3]))\n            key", "            order = _order(int(m[1]), int(m[3])) or 'MDY'\n            key",
     "expect fail"),
    ("88c reason quotes a fabricated date", "app/backend/date_convention.py",
     "def _example(ev):\n    return f\"({ev['raw']})\"", "def _example(ev):\n    return \"(01/01/2026)\"",
     "expect fail"),
    ("88d iso month/day swapped", "app/backend/date_convention.py",
     "    mo, d = (a, b) if order == \"MDY\" else (b, a)", "    mo, d = (b, a) if order == \"MDY\" else (a, b)",
     "expect fail"),
    ("88e suggestion auto-confirmed on read (DB write in dates_to_confirm)", "app/backend/present.py",
     "def dates_to_confirm(conn, case_id):\n    recs = list(_recs_by_id(conn, case_id).values())\n",
     "def dates_to_confirm(conn, case_id):\n    recs = list(_recs_by_id(conn, case_id).values())\n"
     "    from app.backend import date_convention as _DCM\n"
     "    for _r in recs:\n"
     "        _s = _DCM.suggest(_r, recs, DB.get_case(conn, case_id)['raw_text']) if _r['date_status']=='ambiguous' else None\n"
     "        if _s and _s['iso']:\n"
     "            conn.execute(\"UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?\", (_s['iso'], _r['id'], case_id))\n"
     "    recs = list(_recs_by_id(conn, case_id).values())\n",
     "expect fail (write + confirm)"),
    ("89a phrase threshold 3 -> 2", "app/backend/dismissal_patterns.py", "PHRASE_MIN = 3", "PHRASE_MIN = 2", "expect fail"),
    ("89b category threshold 5 -> 4 (boundary)", "app/backend/dismissal_patterns.py", "CATEGORY_MIN = 5", "CATEGORY_MIN = 4",
     "predict: NOT caught"),
    ("89c bulk-applied flags counted as new dismissals", "app/backend/dismissal_patterns.py",
     "if _eligible(f) and (f.get(\"reviewer_note\") or \"\") != APPLIED_NOTE]", "if _eligible(f)]", "expect fail"),
    ("89d gap type made eligible", "app/backend/dismissal_patterns.py",
     'ELIGIBLE_TYPES = ("pre_existing", "causation")', 'ELIGIBLE_TYPES = ("pre_existing", "causation", "gap")', "expect fail"),
    ("89e suggest() writes: dismisses matching pending flags on read", "app/backend/dismissal_patterns.py",
     "    return out\n\n\ndef _row",
     "    for _s in out:\n        for _fid in _s['flag_ids']:\n            conn.execute(\"UPDATE flags SET review_status='dismissed' WHERE id=?\", (_fid,))\n    return out\n\n\ndef _row",
     "expect fail"),
    ("89f GET route auto-applies suggestions (no click)", "app/backend/dismissal_patterns.py",
     "            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"",
     "            for _s in suggest(c, token, local=local_mode()):\n                apply(c, token, _s[\"key\"], local=local_mode(), now=now)\n            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"",
     "expect fail"),
    ("89g case scope ignored: history counts all cases", "app/backend/dismissal_patterns.py",
     "    rows = conn.execute(\"SELECT * FROM flags WHERE review_status='dismissed'\" + (\"\" if local else \" AND case_id=?\"), () if local else (case_id,)).fetchall()",
     "    rows = conn.execute(\"SELECT * FROM flags WHERE review_status='dismissed'\").fetchall()",
     "expect fail"),
    ("89d2 origin (lexicon) requirement dropped", "app/backend/dismissal_patterns.py",
     'return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")', 'return f["type"] in ELIGIBLE_TYPES',
     "expect fail"),
    ("89h route forces local scope (demo token would count other cases)", "app/backend/api.py",
     "now=time.time, local_mode=local_mode)   # T-089", "now=time.time, local_mode=lambda: True)   # T-089",
     "predict: NOT caught"),
    ("89i dismissal history feeds pipeline flags", "app/backend/pipeline.py",
     "    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t)",
     "    from app.backend import dismissal_patterns as _DPM\n    _hc = {f[\"category\"] for f in _DPM._history(conn, cid, True)}\n"
     "    flag_items = [f for f in flag_items if f.get(\"category\") not in _hc]\n"
     "    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t)",
     "expect fail (golden identity test)"),
]


def run_tests():
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + TESTS, cwd=MUT,
                       capture_output=True, text=True, env=env)
    lines = [l for l in p.stdout.strip().splitlines() if l.strip()]
    last = lines[-1] if lines else p.stderr.strip()[-200:]
    failed = [l.split()[1] for l in p.stdout.splitlines() if l.startswith("FAILED") and len(l.split()) > 1]
    return p.returncode, last, failed


def main():
    rc, last, _ = run_tests()
    print(f"BASELINE rc={rc} :: {last}")
    for name, rel, old, new, expect in MUTANTS:
        path = os.path.join(MUT, rel)
        with open(path, encoding="utf-8") as fh:
            orig = fh.read()
        n = orig.count(old)
        if n != 1:
            print(f"MUTANT {name}: ANCHOR COUNT {n} (need 1) -> NOT APPLIED")
            continue
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(orig.replace(old, new, 1))
            rc, last, failed = run_tests()
        finally:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(orig)
        verdict = "CAUGHT" if rc != 0 else "NOT CAUGHT"
        print(f"MUTANT {name} [{expect}] -> {verdict} :: {last}")
        for f in failed[:5]:
            print(f"    failed: {f}")
    rc, last, _ = run_tests()
    print(f"RESTORED rc={rc} :: {last}")


if __name__ == "__main__":
    main()
======
BASELINE rc=0 :: 25 passed in 2.36s
MUTANT 88a mixed evidence not refused [expect fail] -> CAUGHT :: 1 failed, 24 passed in 3.99s
    failed: tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence
MUTANT 88a2 mixed evidence: order picked by sort (paired with 88a) [expect fail] -> NOT CAUGHT :: 25 passed in 2.67s
MUTANT 88b ambiguous dates counted as evidence (MDY) [expect fail] -> CAUGHT :: 6 failed, 19 passed in 2.31s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence
    failed: tests/unit/test_date_convention.py::test_not_ambiguous_or_iso_dates_never_get_or_give_evidence
MUTANT 88c reason quotes a fabricated date [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.40s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 88d iso month/day swapped [expect fail] -> CAUGHT :: 3 failed, 22 passed in 2.56s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 88e suggestion auto-confirmed on read (DB write in dates_to_confirm) [expect fail (write + confirm)] -> CAUGHT :: 2 failed, 23 passed in 2.23s
    failed: tests/unit/test_date_convention.py::test_suggestion_never_writes_and_is_not_a_confirmation
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 89a phrase threshold 3 -> 2 [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.61s
    failed: tests/unit/test_dismissal_patterns.py::test_two_dismissals_are_not_enough
MUTANT 89b category threshold 5 -> 4 (boundary) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.58s
MUTANT 89c bulk-applied flags counted as new dismissals [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.51s
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
MUTANT 89d gap type made eligible [expect fail] -> NOT CAUGHT :: 25 passed in 2.39s
MUTANT 89e suggest() writes: dismisses matching pending flags on read [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.96s
    failed: tests/unit/test_dismissal_patterns.py::test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
    failed: tests/unit/test_dismissal_patterns.py::test_routes_and_demo_mode_isolation
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
MUTANT 89f GET route auto-applies suggestions (no click) [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.60s
    failed: tests/unit/test_dismissal_patterns.py::test_routes_and_demo_mode_isolation
MUTANT 89g case scope ignored: history counts all cases [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.36s
    failed: tests/unit/test_dismissal_patterns.py::test_scope_is_this_case_unless_local_profile
MUTANT 89d2 origin (lexicon) requirement dropped [expect fail] -> NOT CAUGHT :: 25 passed in 2.39s
MUTANT 89h route forces local scope (demo token would count other cases) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.18s
MUTANT 89i dismissal history feeds pipeline flags [expect fail (golden identity test)] -> CAUGHT :: 1 failed, 24 passed in 2.38s
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
RESTORED rc=0 :: 25 passed in 2.41s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:33.969Z

The round-1 runner is reusable. Before mutating, I'll check the golden source text for the record numbering the reason now claims, and look at the round-1 probe.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:34.634Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-088-T-089/probe_t088.py; echo =====; grep -n -i \"record\\|02/17\\|03-17\\|3/25\\|04/14\\|04/05\\|no new symptoms\" evals/golden/case_01_date_formats.txt | head -60",
 "description": "Read round-1 probe and golden case_01 record markers"
}
````

### User / tool · 2026-11-02T04:38:34.760Z

**tool result**
````
"""Probe for T-088 (staff-engineer-reviewer). Runs in the scratch copy; prints what the API returns for golden case_01 and
checks the reason's scope claim against the record each evidence date actually sits in. Read-only on the repo."""
import json
import os
import sys
import tempfile

MUT = sys.argv[1]
sys.path.insert(0, MUT)
os.chdir(MUT)
os.environ["LLM_BACKEND"] = "fixture"
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.pop("ZLAYT_MODE", None)

from fastapi.testclient import TestClient  # noqa: E402

from app.backend import date_convention as DC  # noqa: E402
from app.backend.api import create_app  # noqa: E402
from tests.unit import _golden as G  # noqa: E402
from tests.unit.test_api_routes import run_case  # noqa: E402
from tests.unit.test_date_convention import packet  # noqa: E402

out_dir = tempfile.mkdtemp(prefix="t088probe-")
db = os.path.join(out_dir, "probe.sqlite")
c = TestClient(create_app(db, static_dir=out_dir))
t = run_case(c, G.raw("case_01_date_formats"))
g = c.get(f"/api/cases/{t}").json()
recs = {r["id"]: r for r in g["records"]}
print("RECORDS:", [(r["id"], r.get("seq"), r["date_raw"], r["date_status"]) for r in g["records"]])
for d in g["dates_to_confirm"]:
    if d["raw"] == "04/05/2026":
        print("SUGGESTION_FOR_04/05/2026:", json.dumps(d, indent=1))
        ev_ids = sorted({e["record_id"] for e in d["suggestion"]["evidence"]})
        print("AMBIGUOUS_RECORD:", d["record_id"], "| evidence sits in records:", ev_ids)
        print("reason says 'in this record' ->", "this record" in d["suggestion"]["reason"],
              "| evidence record ids other than the ambiguous record:", [i for i in ev_ids if i != d["record_id"]])

# two-digit-year case: the test's assertion is `A and B or C`; check what it really pins
rows, raw = packet(("03/14/2026", "x"), ("04/05/98", "y"))
s = DC.suggest(rows[1], rows, raw)
print("TWO_DIGIT_YEAR suggestion:", s)
print("test expression value with convention forced wrong:",
      ("DMY" == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]))
=====
3:=== Record 1 ===
8:=== Record 2 ===
9:Date: 02/17/2026
13:=== Record 3 ===
18:=== Record 4 ===
23:=== Record 5 ===
28:=== Record 6 ===
29:Date: 03-17-26
33:=== Record 7 ===
34:Date: 3/25/26
36:Excerpt: "Ankle exam normal. Optional recheck on 04/14/2026 if symptoms return."
38:=== Record 8 ===
39:Date: 04/05/2026
41:Excerpt: "Patient reports no new symptoms."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:39.048Z

The golden headers are `=== Record N ===`, so `Record 2` and `Record 6` match the source. I'll write a round-2 probe that checks each named record against the golden text independently of the app.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:43.726Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2.py",
 "content": "\"\"\"Round-2 probe for T-088 (staff-engineer-reviewer). Runs against the clean HEAD archive passed as argv[1].\nChecks the suggestion reason on golden case_01 against the golden SOURCE TEXT (parsed here, not by the app):\neach named '(Record N: raw)' must sit inside '=== Record N ===' in evals/golden/case_01_date_formats.txt.\nAlso checks: no 'this record' wording, auto_applied false, status stays ambiguous, confirm of a non-candidate is refused.\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport tempfile\n\nMUT = sys.argv[1]\nsys.path.insert(0, MUT)\nos.chdir(MUT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ZLAYT_MODE\", None)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend import date_convention as DC  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\nfrom tests.unit import _golden as G  # noqa: E402\nfrom tests.unit.test_api_routes import run_case  # noqa: E402\nfrom tests.unit.test_date_convention import packet  # noqa: E402\n\n# 1. independent parse of the golden source text\nsrc = open(os.path.join(MUT, \"evals/golden/case_01_date_formats.txt\"), encoding=\"utf-8\").read()\nblocks = {}\nfor m in re.finditer(r\"=== Record (\\d+) ===\\n(.*?)(?=\\n=== Record |\\Z)\", src, re.S):\n    blocks[int(m[1])] = m[2]\nprint(\"SOURCE_RECORDS:\", sorted(blocks))\n\nout_dir = tempfile.mkdtemp(prefix=\"t088r2probe-\")\nc = TestClient(create_app(os.path.join(out_dir, \"p.sqlite\"), static_dir=out_dir))\nt = run_case(c, G.raw(\"case_01_date_formats\"))\ng = c.get(f\"/api/cases/{t}\").json()\nitem = next(d for d in g[\"dates_to_confirm\"] if d[\"raw\"] == \"04/05/2026\")\ns = item[\"suggestion\"]\nprint(\"AMBIGUOUS_RECORD:\", item[\"record_id\"], \"| status:\", item[\"status\"])\nprint(\"REASON:\", s[\"reason\"])\nprint(\"EVIDENCE:\", json.dumps(s[\"evidence\"]), \"| evidence_count:\", s[\"evidence_count\"], \"| auto_applied:\", s[\"auto_applied\"])\nprint(\"this record in reason:\", \"this record\" in s[\"reason\"])\nok = True\nfor e in s[\"evidence\"]:\n    n = int(e[\"record_id\"][1:])\n    named = f\"(Record {n}: {e['raw']})\" in s[\"reason\"]\n    in_src = e[\"raw\"] in blocks.get(n, \"\")\n    print(f\"  check {e['record_id']} {e['raw']}: named_in_reason={named} sits_in_source_record_{n}={in_src}\")\n    ok = ok and named and in_src\nprint(\"ALL_NAMED_RECORDS_VERIFIED:\", ok)\nconf = c.post(f\"/api/cases/{t}/records/{item['record_id']}/confirm_date\", json={\"date\": \"2026-06-06\"})\nprint(\"CONFIRM_NON_CANDIDATE_STATUS:\", conf.status_code)\nacc = c.get(f\"/api/cases/{t}\").json()\nprint(\"STILL_UNCONFIRMED:\", any(d[\"raw\"] == \"04/05/2026\" for d in acc[\"dates_to_confirm\"]))\n\n# 2. packet from the unit test: the reason points at record 1, not record 2\nrows, raw = packet((\"03/14/2026\", \"seen\"), (\"04/05/2026\", \"seen again\"))\nprint(\"PACKET_REASON:\", DC.suggest(rows[1], rows, raw)[\"reason\"])\n"
}
````

### User / tool · 2026-11-02T04:38:43.868Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:45.656Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2.py \"$PWD\" 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt | tail -30",
 "description": "Run round-2 T-088 probe against clean HEAD tree",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:38:46.665Z

**tool result**
````
SOURCE_RECORDS: [1, 2, 3, 4, 5, 6, 7, 8]
AMBIGUOUS_RECORD: r8 | status: ambiguous
REASON: 4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)
EVIDENCE: [{"record_id": "r2", "raw": "02/17/2026"}, {"record_id": "r6", "raw": "03-17-26"}] | evidence_count: 4 | auto_applied: False
this record in reason: False
  check r2 02/17/2026: named_in_reason=True sits_in_source_record_2=True
  check r6 03-17-26: named_in_reason=True sits_in_source_record_6=True
ALL_NAMED_RECORDS_VERIFIED: True
CONFIRM_NON_CANDIDATE_STATUS: 422
STILL_UNCONFIRMED: True
PACKET_REASON: Another date in this packet uses month first (Record 1: 03/14/2026)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:00.309Z

The reason fix checks out: both named records sit in the golden source, and the reason is never auto-applied. Next I'll build the round-2 mutation runner on a scratch copy and run the route and eligibility mutants.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:10.643Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/mutate_r2.py",
 "content": "\"\"\"Round-2 mutation runner for T-088 / T-089 (staff-engineer-reviewer). Edits ONLY the scratch copy passed as argv[1]\n(never the repo). Each mutant: (name, relative file, old text, new text, expectation). Each run is restored before the next.\nRuns the two card test files; prints the failing test ids for each caught mutant.\"\"\"\nimport os\nimport subprocess\nimport sys\n\nMUT = sys.argv[1]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nTESTS = [\"tests/unit/test_date_convention.py\", \"tests/unit/test_dismissal_patterns.py\"]\n\nMUTANTS = [\n    # ---- T-088 round-2 reason wording (the round-1 blocker) ----\n    (\"R2-88a singular reason reverted to 'in this record'\", \"app/backend/date_convention.py\",\n     'f\"Another date in this packet uses {first} {_example(shown[0])}\"', 'f\"Other dates in this record use {first} {_example(shown[0])}\"',\n     \"expect fail\"),\n    (\"R2-88b plural reason reverted to 'in this record'\", \"app/backend/date_convention.py\",\n     'f\"{n} other dates in this packet use {first} \"', 'f\"{n} other dates in this record use {first} \"', \"expect fail\"),\n    (\"R2-88c example drops the record number\", \"app/backend/date_convention.py\",\n     \"return f\\\"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})\\\"\", \"return f\\\"({ev['raw']})\\\"\", \"expect fail\"),\n    (\"R2-88d example names the wrong record (off by one)\", \"app/backend/date_convention.py\",\n     \"return f\\\"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})\\\"\",\n     \"return f\\\"(Record {int(str(ev['record_id']).lstrip('r')) + 1}: {ev['raw']})\\\"\", \"expect fail\"),\n    (\"R2-88e suggestion marked auto_applied true\", \"app/backend/date_convention.py\",\n     '\"evidence_count\": n, \"auto_applied\": False}', '\"evidence_count\": n, \"auto_applied\": True}', \"expect fail\"),\n    (\"R2-88f mixed packets allowed (round-1 88a, regression)\", \"app/backend/date_convention.py\",\n     \"    if len(orders) != 1:\\n        return None\", \"    if not orders:\\n        return None\", \"expect fail\"),\n    (\"R2-88g iso month/day swapped (regression)\", \"app/backend/date_convention.py\",\n     '    mo, d = (a, b) if order == \"MDY\" else (b, a)', '    mo, d = (b, a) if order == \"MDY\" else (a, b)', \"expect fail\"),\n    (\"R2-88h auto-confirm on read (regression, round-1 88e)\", \"app/backend/present.py\",\n     \"def dates_to_confirm(conn, case_id):\\n    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"def dates_to_confirm(conn, case_id):\\n    recs = list(_recs_by_id(conn, case_id).values())\\n\"\n     \"    from app.backend import date_convention as _DCM\\n\"\n     \"    for _r in recs:\\n\"\n     \"        _s = _DCM.suggest(_r, recs, DB.get_case(conn, case_id)['raw_text']) if _r['date_status']=='ambiguous' else None\\n\"\n     \"        if _s and _s['iso']:\\n\"\n     \"            conn.execute(\\\"UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?\\\", (_s['iso'], _r['id'], case_id))\\n\"\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"expect fail\"),\n    # ---- T-089 ----\n    (\"89a phrase threshold 3 -> 2\", \"app/backend/dismissal_patterns.py\", \"PHRASE_MIN = 3\", \"PHRASE_MIN = 2\", \"expect fail\"),\n    (\"89b category threshold 5 -> 4 (round-1 minor, now expected caught)\", \"app/backend/dismissal_patterns.py\",\n     \"CATEGORY_MIN = 5\", \"CATEGORY_MIN = 4\", \"expect fail\"),\n    (\"89c bulk-applied flags counted as new dismissals\", \"app/backend/dismissal_patterns.py\",\n     'if _eligible(f) and (f.get(\"reviewer_note\") or \"\") != APPLIED_NOTE]', 'if _eligible(f)]', \"expect fail\"),\n    (\"89d gap type made eligible (round-1 minor, now expected caught)\", \"app/backend/dismissal_patterns.py\",\n     'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\")', 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\", \"gap\")', \"expect fail\"),\n    (\"89d2 origin (lexicon) requirement dropped (round-1 minor, now expected caught)\", \"app/backend/dismissal_patterns.py\",\n     'return f[\"type\"] in ELIGIBLE_TYPES and \"lexicon\" in (f.get(\"origin\") or \"\")', 'return f[\"type\"] in ELIGIBLE_TYPES',\n     \"expect fail\"),\n    (\"89e suggest() writes: dismisses matching pending flags on read\", \"app/backend/dismissal_patterns.py\",\n     \"    return out\\n\\n\\ndef _row\",\n     \"    for _s in out:\\n        for _fid in _s['flag_ids']:\\n            conn.execute(\\\"UPDATE flags SET review_status='dismissed' WHERE id=?\\\", (_fid,))\\n    return out\\n\\n\\ndef _row\",\n     \"expect fail\"),\n    (\"89f GET route auto-applies suggestions (no click)\", \"app/backend/dismissal_patterns.py\",\n     '            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"',\n     '            for _s in suggest(c, token, local=local_mode()):\\n                apply(c, token, _s[\"key\"], local=local_mode(), now=now)\\n'\n     '            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"', \"expect fail\"),\n    (\"89g case scope ignored: history counts all cases in public mode\", \"app/backend/dismissal_patterns.py\",\n     '    rows = conn.execute(\"SELECT * FROM flags WHERE review_status=\\'dismissed\\'\" + (\"\" if local else \" AND case_id=?\"), () if local else (case_id,)).fetchall()',\n     '    rows = conn.execute(\"SELECT * FROM flags WHERE review_status=\\'dismissed\\'\").fetchall()', \"expect fail\"),\n    (\"89h ROUTE forces local scope (public demo token sees other cases)\", \"app/backend/api.py\",\n     \"now=time.time, local_mode=local_mode)   # T-089\", \"now=time.time, local_mode=lambda: True)   # T-089\", \"expect fail (route tests)\"),\n    (\"89h2 ROUTE forces public scope (local profile lost)\", \"app/backend/api.py\",\n     \"now=time.time, local_mode=local_mode)   # T-089\", \"now=time.time, local_mode=lambda: False)   # T-089\", \"expect fail (local route test)\"),\n    (\"89i dismissal history feeds pipeline flags\", \"app/backend/pipeline.py\",\n     '    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t)',\n     \"    from app.backend import dismissal_patterns as _DPM\\n    _hc = {f[\\\"category\\\"] for f in _DPM._history(conn, cid, True)}\\n\"\n     \"    flag_items = [f for f in flag_items if f.get(\\\"category\\\") not in _hc]\\n\"\n     '    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t)',\n     \"expect fail (golden identity test)\"),\n]\n\n\ndef run_tests():\n    env = {**os.environ, \"PYTHONDONTWRITEBYTECODE\": \"1\"}\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\"] + TESTS, cwd=MUT,\n                       capture_output=True, text=True, env=env)\n    lines = [l for l in p.stdout.strip().splitlines() if l.strip()]\n    last = lines[-1] if lines else p.stderr.strip()[-300:]\n    failed = [l.split(\" \")[1] for l in p.stdout.splitlines() if l.startswith(\"FAILED\") and len(l.split(\" \")) > 1]\n    return p.returncode, last, failed\n\n\ndef main():\n    rc, last, _ = run_tests()\n    print(f\"BASELINE rc={rc} :: {last}\", flush=True)\n    for name, rel, old, new, expect in MUTANTS:\n        path = os.path.join(MUT, rel)\n        with open(path, encoding=\"utf-8\") as fh:\n            orig = fh.read()\n        n = orig.count(old)\n        if n != 1:\n            print(f\"MUTANT {name}: ANCHOR COUNT {n} (need 1) -> NOT APPLIED\", flush=True)\n            continue\n        try:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig.replace(old, new, 1))\n            rc, last, failed = run_tests()\n        finally:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig)\n        verdict = \"CAUGHT\" if rc != 0 else \"NOT CAUGHT\"\n        print(f\"MUTANT {name} [{expect}] -> {verdict} :: {last}\", flush=True)\n        for f in failed[:8]:\n            print(f\"    failed: {f}\", flush=True)\n    rc, last, _ = run_tests()\n    print(f\"RESTORED rc={rc} :: {last}\", flush=True)\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T04:39:10.756Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/mutate_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:13.273Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2 && rm -rf mut && mkdir mut && (cd clean && tar --exclude=./artifacts --exclude=./reviews -cf - .) | (cd mut && tar -xf -) && cd /Users/arsis/zlayt-pm-project && .venv/bin/python artifacts/review-evidence/T-088-T-089-r2/mutate_r2.py artifacts/review-evidence/T-088-T-089-r2/mut 2>&1 | tee artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt",
 "description": "Run round-2 mutation suite on scratch copy of HEAD",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:40:50.126Z

**tool result**
````
BASELINE rc=0 :: 30 passed in 4.73s
MUTANT R2-88a singular reason reverted to 'in this record' [expect fail] -> CAUGHT :: 2 failed, 28 passed in 4.64s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_reason_names_the_record_each_date_sits_in_never_this_record
MUTANT R2-88b plural reason reverted to 'in this record' [expect fail] -> CAUGHT :: 3 failed, 27 passed in 4.64s
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
    failed: tests/unit/test_date_convention.py::test_reason_names_the_record_each_date_sits_in_never_this_record
MUTANT R2-88c example drops the record number [expect fail] -> CAUGHT :: 5 failed, 25 passed in 3.87s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
    failed: tests/unit/test_date_convention.py::test_reason_names_the_record_each_date_sits_in_never_this_record
MUTANT R2-88d example names the wrong record (off by one) [expect fail] -> CAUGHT :: 5 failed, 25 passed in 4.41s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
    failed: tests/unit/test_date_convention.py::test_reason_names_the_record_each_date_sits_in_never_this_record
MUTANT R2-88e suggestion marked auto_applied true [expect fail] -> CAUGHT :: 3 failed, 27 passed in 4.39s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_suggestion_never_writes_and_is_not_a_confirmation
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT R2-88f mixed packets allowed (round-1 88a, regression) [expect fail] -> CAUGHT :: 1 failed, 29 passed in 4.24s
    failed: tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence
MUTANT R2-88g iso month/day swapped (regression) [expect fail] -> CAUGHT :: 3 failed, 27 passed in 4.17s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT R2-88h auto-confirm on read (regression, round-1 88e) [expect fail] -> CAUGHT :: 3 failed, 27 passed in 4.36s
    failed: tests/unit/test_date_convention.py::test_suggestion_never_writes_and_is_not_a_confirmation
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
    failed: tests/unit/test_date_convention.py::test_reason_names_the_record_each_date_sits_in_never_this_record
MUTANT 89a phrase threshold 3 -> 2 [expect fail] -> CAUGHT :: 1 failed, 29 passed in 4.00s
    failed: tests/unit/test_dismissal_patterns.py::test_two_dismissals_are_not_enough
MUTANT 89b category threshold 5 -> 4 (round-1 minor, now expected caught) [expect fail] -> CAUGHT :: 1 failed, 29 passed in 3.89s
    failed: tests/unit/test_dismissal_patterns.py::test_category_threshold_is_exactly_five
MUTANT 89c bulk-applied flags counted as new dismissals [expect fail] -> CAUGHT :: 1 failed, 29 passed in 4.19s
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
MUTANT 89d gap type made eligible (round-1 minor, now expected caught) [expect fail] -> NOT CAUGHT :: 30 passed in 4.14s
MUTANT 89d2 origin (lexicon) requirement dropped (round-1 minor, now expected caught) [expect fail] -> CAUGHT :: 1 failed, 29 passed in 4.34s
    failed: tests/unit/test_dismissal_patterns.py::test_eligibility_rules_are_each_enforced_on_their_own
MUTANT 89e suggest() writes: dismisses matching pending flags on read [expect fail] -> CAUGHT :: 7 failed, 23 passed in 4.18s
    failed: tests/unit/test_dismissal_patterns.py::test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
    failed: tests/unit/test_dismissal_patterns.py::test_routes_apply_and_errors
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_06_subtle_pre_existing]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_07_prompt_injection]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_08_diagnosis_temptation]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
MUTANT 89f GET route auto-applies suggestions (no click) [expect fail] -> CAUGHT :: 3 failed, 27 passed in 4.00s
    failed: tests/unit/test_dismissal_patterns.py::test_routes_apply_and_errors
    failed: tests/unit/test_dismissal_patterns.py::test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route
    failed: tests/unit/test_dismissal_patterns.py::test_local_mode_counts_the_machine_profile_through_the_route
MUTANT 89g case scope ignored: history counts all cases in public mode [expect fail] -> CAUGHT :: 2 failed, 28 passed in 4.19s
    failed: tests/unit/test_dismissal_patterns.py::test_scope_is_this_case_unless_local_profile
    failed: tests/unit/test_dismissal_patterns.py::test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route
MUTANT 89h ROUTE forces local scope (public demo token sees other cases) [expect fail (route tests)] -> CAUGHT :: 1 failed, 29 passed in 4.16s
    failed: tests/unit/test_dismissal_patterns.py::test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route
MUTANT 89h2 ROUTE forces public scope (local profile lost) [expect fail (local route test)] -> CAUGHT :: 1 failed, 29 passed in 3.84s
    failed: tests/unit/test_dismissal_patterns.py::test_local_mode_counts_the_machine_profile_through_the_route
MUTANT 89i dismissal history feeds pipeline flags [expect fail (golden identity test)] -> CAUGHT :: 4 failed, 26 passed in 3.87s
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_06_subtle_pre_existing]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_07_prompt_injection]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_08_diagnosis_temptation]
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
RESTORED rc=0 :: 30 passed in 3.94s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:04.271Z

Route forcing is caught by the new route tests (89h, 89h2). Two results need follow-up: 89d (gap type made eligible) survives, and 89i is caught on only 4 golden cases. I'll test both on the scratch copy to see whether the cause is the test or the code.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:10.682Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py",
 "content": "\"\"\"Round-2 follow-up experiments for T-089 (staff-engineer-reviewer). Edits ONLY the scratch copy mut/ (never the repo or clean/).\nExp A: does mutant 89d (gap type eligible) get caught once a PENDING gap flag exists in the eligibility test?\nExp B: which golden cases are sensitive to dismissal history, and how many history rows the identity test really seeds?\"\"\"\nimport os\nimport shutil\nimport subprocess\nimport sys\n\nBASE = os.path.dirname(os.path.abspath(__file__))\nMUT = os.path.join(BASE, \"mut\")\nCLEAN_TEST = os.path.join(BASE, \"clean\", \"tests\", \"unit\", \"test_dismissal_patterns.py\")\nMUT_TEST = os.path.join(MUT, \"tests\", \"unit\", \"test_dismissal_patterns.py\")\nMUT_DP = os.path.join(MUT, \"app\", \"backend\", \"dismissal_patterns.py\")\nCLEAN_DP = os.path.join(BASE, \"clean\", \"app\", \"backend\", \"dismissal_patterns.py\")\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n\n\ndef pytest(args):\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\"] + args, cwd=MUT, capture_output=True, text=True,\n                       env={**os.environ, \"PYTHONDONTWRITEBYTECODE\": \"1\"})\n    return p.returncode, (p.stdout + p.stderr)\n\n\ndef restore():\n    shutil.copyfile(CLEAN_TEST, MUT_TEST)\n    shutil.copyfile(CLEAN_DP, MUT_DP)\n\n\ndef exp_a():\n    restore()\n    src = open(MUT_TEST, encoding=\"utf-8\").read()\n    anchor = \"    assert DP.suggest(conn, cid) == []\\n    add_flag(conn, cid, \\\"f_ok\\\"\"\n    assert src.count(anchor) == 1, src.count(anchor)\n    src = src.replace(anchor, \"    assert DP.suggest(conn, cid) == []\\n\"\n                              \"    add_flag(conn, cid, \\\"f_gap_pending\\\", category=\\\"gap_over_30\\\", type_=\\\"gap\\\", origin=\\\"lexicon+llm\\\", status=None)\\n\"\n                              \"    assert DP.suggest(conn, cid) == []                              # pending gap flag must not be offered\\n\"\n                              \"    add_flag(conn, cid, \\\"f_ok\\\"\", 1)\n    open(MUT_TEST, \"w\", encoding=\"utf-8\").write(src)\n    code, out = pytest([\"tests/unit/test_dismissal_patterns.py\", \"-k\", \"eligibility\"])\n    print(\"EXP_A baseline (gap pending, unmutated):\", out.strip().splitlines()[-1])\n    dp = open(MUT_DP, encoding=\"utf-8\").read()\n    anchor2 = 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\")'\n    assert dp.count(anchor2) == 1\n    open(MUT_DP, \"w\", encoding=\"utf-8\").write(dp.replace(anchor2, 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\", \"gap\")', 1))\n    code, out = pytest([\"tests/unit/test_dismissal_patterns.py\", \"-k\", \"eligibility\"])\n    print(\"EXP_A mutant 89d with pending gap flag:\", \"CAUGHT\" if code else \"NOT CAUGHT\", \"::\", out.strip().splitlines()[-1])\n    for line in out.splitlines():\n        if line.startswith(\"E \") or \"assert\" in line and \"Error\" not in line[:5]:\n            pass\n    restore()\n\n\ndef exp_b():\n    restore()\n    src = open(MUT_TEST, encoding=\"utf-8\").read()\n    anchor = \"        seeded_view, _ = run(flags)\\n\"\n    assert src.count(anchor) == 1\n    src = src.replace(anchor, anchor + \"        print(f'EXPB {case} eligible_flags={len(flags)}')\\n\", 1)\n    open(MUT_TEST, \"w\", encoding=\"utf-8\").write(src)\n    anchor_h = \"        cid = DB.create_case(conn, G.raw(case), now=1.0)\\n\"\n    assert src.count(anchor_h) == 1\n    src = src.replace(anchor_h, \"        print(f'EXPB {case} history_rows_seeded={len(history_from * 8 or [None]) if history_from is not None else 0}')\\n\" + anchor_h, 1)\n    open(MUT_TEST, \"w\", encoding=\"utf-8\").write(src)\n    code, out = pytest([\"tests/unit/test_dismissal_patterns.py\", \"-k\", \"golden\", \"-s\"])\n    for line in out.splitlines():\n        if line.startswith(\"EXPB\"):\n            print(line)\n    print(\"EXP_B summary line:\", out.strip().splitlines()[-1])\n    restore()\n\n\nif __name__ == \"__main__\":\n    exp_a()\n    exp_b()\n    restore()\n    print(\"RESTORED\", open(MUT_TEST, encoding=\"utf-8\").read() == open(CLEAN_TEST, encoding=\"utf-8\").read())\n"
}
````

### User / tool · 2026-11-02T04:41:10.792Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:12.187Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py 2>&1 | tee artifacts/review-evidence/T-088-T-089-r2/experiments_r2_output.txt",
 "description": "Run eligibility-with-pending-gap and golden sensitivity experiments in scratch copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:41:14.163Z

**tool result**
````
EXP_A baseline (gap pending, unmutated): 1 passed, 20 deselected in 0.60s
EXP_A mutant 89d with pending gap flag: CAUGHT :: 1 failed, 20 deselected in 0.62s
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py", line 74, in <module>
    exp_b()
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py", line 57, in exp_b
    assert src.count(anchor) == 1
AssertionError
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:16.534Z

Experiment A confirms the gap: once a pending gap flag exists, mutant 89d is caught, so the shipped eligibility test leaves that rule unchecked. Experiment B has a wrong indentation anchor, so I'll fix it and rerun.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:18.739Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2 && grep -n \"seeded_view, _ = run\\|cid = DB.create_case(conn, G.raw(case)\" clean/tests/unit/test_dismissal_patterns.py && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport re\np = \"experiments_r2.py\"\ns = open(p, encoding=\"utf-8\").read()\ns = s.replace('anchor = \"        seeded_view, _ = run(flags)\\\\n\"', 'anchor = \"    seeded_view, _ = run(flags)\\\\n\"')\ns = s.replace('src = src.replace(anchor, anchor + \"        print(f\\'EXPB {case} eligible_flags={len(flags)}\\')\\\\n\", 1)',\n              'src = src.replace(anchor, anchor + \"    print(f\\'EXPB {case} eligible_flags={len(flags)}\\')\\\\n\", 1)')\ns = s.replace('anchor_h = \"        cid = DB.create_case(conn, G.raw(case), now=1.0)\\\\n\"', 'anchor_h = \"        cid = DB.create_case(conn, G.raw(case), now=1.0)\\\\n\"')\nopen(p, \"w\", encoding=\"utf-8\").write(s)\nprint(\"patched\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python artifacts/review-evidence/T-088-T-089-r2/experiments_r2.py 2>&1 | tee artifacts/review-evidence/T-088-T-089-r2/experiments_r2_output.txt",
 "description": "Fix experiment anchors and rerun both experiments",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:41:22.517Z

**tool result**
````
169:        cid = DB.create_case(conn, G.raw(case), now=1.0)
180:    seeded_view, _ = run(flags)
patched
EXP_A baseline (gap pending, unmutated): 1 passed, 20 deselected in 0.61s
EXP_A mutant 89d with pending gap flag: CAUGHT :: 1 failed, 20 deselected in 0.63s
EXPB case_01_date_formats history_rows_seeded=0
EXPB case_01_date_formats history_rows_seeded=1
EXPB case_01_date_formats eligible_flags=0
EXPB case_01_date_formats history_rows_seeded=1
EXPB case_02_gap_boundaries history_rows_seeded=1
EXPB case_02_gap_boundaries eligible_flags=0
EXPB case_02_gap_boundaries history_rows_seeded=1
EXPB case_03_rate_and_ocr history_rows_seeded=1
EXPB case_03_rate_and_ocr eligible_flags=0
EXPB case_03_rate_and_ocr history_rows_seeded=1
EXPB case_04_duplicates_no_amounts history_rows_seeded=1
EXPB case_04_duplicates_no_amounts eligible_flags=0
EXPB case_04_duplicates_no_amounts history_rows_seeded=1
EXPB case_05_provider_conflict history_rows_seeded=1
EXPB case_05_provider_conflict eligible_flags=0
EXPB case_05_provider_conflict history_rows_seeded=1
EXPB case_06_subtle_pre_existing history_rows_seeded=24
EXPB case_06_subtle_pre_existing eligible_flags=3
EXPB case_06_subtle_pre_existing history_rows_seeded=1
EXPB case_07_prompt_injection history_rows_seeded=8
EXPB case_07_prompt_injection eligible_flags=1
EXPB case_07_prompt_injection history_rows_seeded=1
EXPB case_08_diagnosis_temptation history_rows_seeded=8
EXPB case_08_diagnosis_temptation eligible_flags=1
EXPB case_08_diagnosis_temptation history_rows_seeded=1
EXPB case_09_nonvisit_hides_gap history_rows_seeded=1
EXPB case_09_nonvisit_hides_gap eligible_flags=0
EXPB case_09_nonvisit_hides_gap history_rows_seeded=1
EXPB sample history_rows_seeded=56
EXPB sample eligible_flags=7
EXPB sample history_rows_seeded=1
EXP_B summary line: 10 passed, 11 deselected in 1.33s
RESTORED True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:39.690Z

Experiment B shows the golden identity test seeds real history for only 4 of 10 cases; the other six get one generic row, not the 8 its comment states. Next I'll check the remaining round-1 items: the AC1 board state, the eval entry, stale wording, and the staged index.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:42.059Z

**tool call — Bash**
````
{
 "command": "echo \"--- index for the 4 card paths (empty = not staged):\"; git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py; echo \"(end)\"; echo \"--- all staged paths:\"; git diff --cached --name-status | wc -l; echo \"--- qa cards:\"; python3 tools/board.py list --role qa 2>&1 | head -20; echo \"--- golden expected entry for suggestion (clean HEAD):\"; grep -c \"suggestion\\|dismissal\" artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/case_01_date_formats.expected.json; echo \"--- frontend:\"; grep -rn \"suggestion\\|dismissal\" artifacts/review-evidence/T-088-T-089-r2/clean/app/frontend | wc -l; echo \"--- 'this record' in code/contracts/tests/evals (clean HEAD):\"; grep -rn \"this record\" artifacts/review-evidence/T-088-T-089-r2/clean/app/backend artifacts/review-evidence/T-088-T-089-r2/clean/memory/contracts artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/test_date_convention.py artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/test_dismissal_patterns.py artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden 2>/dev/null; echo \"(end)\"; echo \"--- unused dates import / reference:\"; grep -n \"import\\|dates\\.\" artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/date_convention.py",
 "description": "Check index, qa cards, eval expectations, frontend, and stale wording"
}
````

### User / tool · 2026-11-02T04:41:42.313Z

**tool result**
````
--- index for the 4 card paths (empty = not staged):
(end)
--- all staged paths:
      14
--- qa cards:
T-015	M1	qa         	done             	P0	AC 4/4	Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs
T-029	M2	qa         	done             	P0	AC 7/7	Test-first unit suites for all deterministic modules (red before any backend code)
T-038	M2	qa         	done             	P0	AC 9/9	Eval runner: python -m evals.run -> evals/reports/latest.json with ship_bar_met
T-039	M3	qa         	done             	P0	AC 9/9	Test-first export/review unit suites and E2E specs (red before build)
T-045	M3	qa         	in_review        	P0	AC 0/8	Playwright E2E: full paralegal journey, adversarial inputs, all sensors
T-048	M2	qa         	done             	P0	AC 2/2	M2 LLM-stage tests first (provider, audited, schemas, judges, flags, pipeline, conflicts, templates)
T-051	M2	qa         	done             	P0	AC 3/3	Curated golden-conformant fixture set for demo + E2E (D-029)
T-070	M2	qa         	done             	P0	AC 1/1	Live eval: evals.run honors LLM_BACKEND=claude-cli (reported backend=fixture)
T-079	M3	qa         	in_progress      	P1	AC 2/2	Build library packets lib08..lib15 from the v2 research (synthetic, with expected.json)
T-090	M3	qa         	in_progress      	P2	AC 1/1	Calibrated confidence: measured precision per state from evals
T-093	M2	qa         	in_review        	P0	AC 2/2	Eval determinism signature must match R-CO-7 in full; keep per-run artifacts; seeded controls for judge v2 prompts
--- golden expected entry for suggestion (clean HEAD):
0
--- frontend:
       0
--- 'this record' in code/contracts/tests/evals (clean HEAD):
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/why.py:26:    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/why.py:27:    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/why.py:30:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/trace.py:327:                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/trace.py:517:            st.append(step("agreement", "Phrase list and AI agree", "code", SKIPPED, reason_text(other) if other else "Only one source looked at this record, so there is nothing to compare.",
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/flag_templates.py:112:            f"{_at(v)} contains instruction-like text{_quote(v)}. It is shown unchanged and everything from this record needs review.")
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/review.py:183:        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/review.py:294:        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
artifacts/review-evidence/T-088-T-089-r2/clean/memory/contracts/api.md:267:`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Another date in this packet uses month first (Record 1: 03/14/2026)"; several read "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)" (each example names the record the date sits in; the evidence dates come from the packet, never described as "in this record") (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
artifacts/review-evidence/T-088-T-089-r2/clean/memory/contracts/api.md:565:      "why": "The AI read this record and proposed a one-line summary and a quote.", "reason_code": null, "rule": "row 4", "blocks_export": false,
artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/hallucinations.jsonl:4:{"id": "H04", "synthetic": true, "category": "invented_number", "record_text": "Record 4 | 2026-01-23 | Capital PT, initial evaluation | \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\"", "candidate_summary": "Cervical range of motion was reduced approx. 40% and pain was 8/10 at the initial evaluation.", "why_unsupported": "No pain score appears in this record. '8/10' is invented; only the 40% range-of-motion figure is supported."}
artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/hallucinations.jsonl:40:{"id": "H40", "synthetic": true, "category": "abbreviation_misexpanded", "record_text": "Record 6 | 2026-03-06 | Capital PT, visit 9 | \"Discharged from PT after two missed appointments. Pain 3/10.\"", "candidate_summary": "Patient was discharged from prothrombin time testing after two missed appointments.", "why_unsupported": "'PT' in this record is physical therapy (see the source label 'Capital PT, visit 9'). The abbreviation is mis-expanded."}
artifacts/review-evidence/T-088-T-089-r2/clean/app/backend/flags.py:189:    """One model call for this record only, merged with the lexicon floor. A failed or missed model call leaves the lexicon flags in place."""
artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/test_date_convention.py:107:    """T-088 round 2: evidence dates in other records must not be described as 'in this record' (golden case_01, record 8)."""
artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/test_date_convention.py:115:    assert item["record_id"] == "r8" and "this record" not in s["reason"]
artifacts/review-evidence/T-088-T-089-r2/clean/tests/unit/test_date_convention.py:122:    assert "Record 1" in r and "this record" not in r and "Record 2" not in r
(end)
--- unused dates import / reference:
7:accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
8:import re
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:49.068Z

The index no longer stages the four card paths, and the qa board has no card for the golden expected entry. Two more checks: whether the "Record N" label matches how the app numbers records, and the staged-index contents.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:50.387Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && grep -rn \"f\\\"r{\\|'r{\\|\\\"r\\\" *+\\|f'r{\" app/backend/*.py | head -8; echo \"--- UI record labels:\"; grep -rn \"Record \\${\\|\\\"Record \\\"\\|'Record '\\|Record {\" app/frontend --include=*.js --include=*.html | head -6; echo \"--- marker parse in split:\"; grep -rln \"=== Record\\|Record (\\\\\\\\d\" app/backend | head -5; cd /Users/arsis/zlayt-pm-project && echo \"--- staged entries:\" && git diff --cached --name-status",
 "description": "Check record id assignment, UI record labels, and staged entries"
}
````

### User / tool · 2026-11-02T04:41:50.533Z

**tool result**
````
app/backend/export_routes.py:40:            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
app/backend/flags.py:51:         "record_id": record.get("id", f"r{record['n']}"), "review_status": "pending",
app/backend/flags.py:179:    return {"type": "record_warning", "category": "injection_suspected", "record_no": record["n"], "record_id": record.get("id", f"r{record['n']}"),
app/backend/flags.py:253:             "record_no": ref["n"], "record_id": ref.get("id", f"r{ref['n']}"), "review_status": "pending", "source_kind": "record",
app/backend/generator.py:38:    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
app/backend/ingest.py:318:        rid = f"r{r['n']}"
app/backend/ingest.py:320:                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
app/backend/pdf_checks.py:110:    ocr_ids = {f"r{r['n']}" for r in recs if is_ocr_span(pages, r["char_start"], r["char_end"])}
--- UI record labels:
app/frontend/flags.js:24:        el("span", { class: "rv-ev-cap" }, "Record " + recSeq(c, e.record_id) + (r ? " · " + r.source_label : "")),
app/frontend/review.js:76:    ZL.openSource(t.spans, title || (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]));
app/frontend/manual.js:96:        el("div", { class: "rv-head" }, el("h3", { class: "rv-title" }, "Record " + r.seq + ": " + r.source_label), el("span", { class: "rv-chip" }, r.date_iso ? ZL.fmtDate(r.date_iso) : "undated")),
app/frontend/manual.js:99:        el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn rv-secondary", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], "Record " + r.seq + ": " + r.source_label) }, "Open record " + r.seq)));
app/frontend/sidebyside.js:55:    titleEl.textContent = (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]) + " (source of the selected item)";
app/frontend/stepper.js:67:    return !seqs.length ? "" : seqs.length === 1 ? "Record " + seqs[0] : "Records " + seqs.slice(0, -1).join(", ") + " and " + seqs[seqs.length - 1];
--- marker parse in split:
app/backend/ingest.py
--- staged entries:
M	.claude/agent-memory/qa/MEMORY.md
D	.claude/agent-memory/qa/project_judge_controls.md
M	app/backend/rejudge.py
M	app/db/db.py
M	app/db/schema.sql
D	evals/golden/judge_controls.CHANGELOG.md
M	evals/golden/judge_controls.jsonl
D	evals/golden/judge_controls_heldout.jsonl
D	evals/reports/controls-20261102T042306Z.json
D	evals/reports/controls-20261102T042306Z.md
M	evals/run.py
M	tests/unit/test_db.py
M	tests/unit/test_t093_eval_signature.py
M	tests/unit/test_trace.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:10.057Z

The `Record N` label matches the app's own record numbering (`r{n}` with `seq = n`), so the reason uses the same label the UI shows. I'll collect exact line numbers for the evidence citations.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:11.589Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && grep -n \"def _example\\|Another date in this packet\\|other dates in this packet\\|auto_applied\\\": False\" app/backend/date_convention.py; echo ---; grep -n \"and (s\\[\\\"iso\\\"\\] is None\\|def test_reason_names\\|def test_two_digit\" tests/unit/test_date_convention.py; echo ---; grep -n \"def test_\\|def _client\\|def _two_cases\\|history_from \\* 8\\|CATEGORY_MIN\\|ELIGIBLE_TYPES\" tests/unit/test_dismissal_patterns.py | head -40; echo ---; grep -n \"dismissal_patterns.add_routes\" app/backend/api.py; echo ---; grep -n \"not one transaction\" memory/contracts/api.md | cut -c1-80; echo ---; grep -n \"^ *\\\"\\\"\\\"Same case through\\|a case with no eligible flag\" tests/unit/test_dismissal_patterns.py",
 "description": "Collect line numbers for evidence citations in clean HEAD tree"
}
````

### User / tool · 2026-11-02T04:42:11.712Z

**tool result**
````
38:def _example(ev):
63:    reason = (f"Another date in this packet uses {first} {_example(shown[0])}" if n == 1 else
64:              f"{n} other dates in this packet use {first} " + " and ".join(_example(e) for e in shown))
66:            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
---
62:def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
65:    assert s["convention"] == "MDY" and (s["iso"] is None or s["iso"] in rows[1]["date_candidates"])
81:            assert s["auto_applied"] is False and item["candidates"] and (s["iso"] is None or s["iso"] in item["candidates"])
106:def test_reason_names_the_record_each_date_sits_in_never_this_record(tmp_path, monkeypatch):
---
26:def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
39:def test_two_dismissals_are_not_enough(tmp_path):
46:def test_ineligible_flags_are_never_suggested(tmp_path):
54:def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
66:def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
84:def test_scope_is_this_case_unless_local_profile(tmp_path):
94:def _client(tmp_path, monkeypatch, name, mode=None):
105:def test_routes_apply_and_errors(tmp_path, monkeypatch):
123:def _two_cases(c, db):
136:def test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route(tmp_path, monkeypatch):
148:def test_local_mode_counts_the_machine_profile_through_the_route(tmp_path, monkeypatch):
156:def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):
164:            for n, f in enumerate(history_from * 8 or [None]):
185:def test_eligibility_rules_are_each_enforced_on_their_own(tmp_path):
196:def test_category_threshold_is_exactly_five(tmp_path):
---
513:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
---
284:Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hid
---
157:    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts.
159:    let history filter flags would change this case's output; a case with no eligible flag also gets the generic new_onset history."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:17.260Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && grep -rn \"other dates in this record\\|Other dates in this record\" --include=*.py --include=*.js --include=*.json --include=*.jsonl --include=*.md --include=*.html . | grep -v \"^./artifacts\" | cut -c1-160; echo \"(stale-wording grep end)\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"h=[]; print('[] * 8 or [None] ->', [] * 8 or [None], '| rows seeded:', len(h * 8 or [None]))\"",
 "description": "Grep for stale reason wording and confirm the empty-history seeding arithmetic"
}
````

### User / tool · 2026-11-02T04:42:17.390Z

**tool result**
````
(stale-wording grep end)
[] * 8 or [None] -> [None] | rows seeded: 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:19.178Z

No stale wording remains, and the empty-history arithmetic is confirmed. As a last deterministic check, I'll run the full unit suite on the clean HEAD tree to catch regressions outside the selector.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:20.337Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && PYTHONDONTWRITEBYTECODE=1 timeout 580 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run full unit suite on clean HEAD tree",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:42:20.421Z

**tool result**
````
/bin/bash: timeout: command not found
exit=127
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:21.978Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run full unit suite on clean HEAD tree",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:42:58.922Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s
FAILED tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2
FAILED tests/unit/test_trace.py::test_every_item_has_an_ordered_well_formed_trace
FAILED tests/unit/test_trace.py::test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them
FAILED tests/unit/test_trace.py::test_every_emitted_reason_code_has_a_fixed_sentence
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
6 failed, 1330 passed in 35.84s
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:01.842Z

The full suite at HEAD shows 6 failures, none in the card files. I need to know whether they predate this round, so I'll check the messages and compare against the 55300e9 tree.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:02.838Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_trace.py tests/unit/test_t075_determinism.py tests/unit/test_t037_backend.py 2>&1 | grep -E \"^E   |Error|assert\" | head -20",
 "description": "Show error lines for the six failing tests at HEAD",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:43:08.887Z

**tool result**
````
        assert len(ids) >= 20
>           assert r.status_code == 200, iid
E           AssertionError: f_cx1
E           assert 500 == 200
E            +  where 500 = <Response [500 Internal Server Error]>.status_code
tests/unit/test_trace.py:113: AssertionError
ERROR    zlayt.api:api.py:184 unhandled KeyError
        assert c.post(f"/api/cases/{tok}/items/{fid}/review", json={"action": "edit", "edits": {"note": "Ask the client about 2023."}}).status_code == 200
>           assert pub[u]["mode"] == "metadata" and loc[u]["mode"] == "full"
E           KeyError: 'mode'
tests/unit/test_trace.py:444: KeyError
ERROR    zlayt.api:api.py:184 unhandled KeyError
ERROR    zlayt.api:api.py:184 unhandled KeyError
E                   KeyError: 'steps'
tests/unit/test_trace.py:478: KeyError
ERROR    zlayt.api:api.py:184 unhandled KeyError
        assert n >= 5
E           KeyError: 'steps'
tests/unit/test_trace.py:519: KeyError
ERROR    zlayt.api:api.py:184 unhandled KeyError
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:10.811Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-088-T-089-r2/prev && mkdir -p artifacts/review-evidence/T-088-T-089-r2/prev && git archive 55300e9 | tar -x -C artifacts/review-evidence/T-088-T-089-r2/prev && cd artifacts/review-evidence/T-088-T-089-r2/prev && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run full unit suite on the round-2 commit 55300e9 tree for comparison",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:43:46.093Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s
FAILED tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2
FAILED tests/unit/test_trace.py::test_every_item_has_an_ordered_well_formed_trace
FAILED tests/unit/test_trace.py::test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them
FAILED tests/unit/test_trace.py::test_every_emitted_reason_code_has_a_fixed_sentence
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
6 failed, 1316 passed in 33.98s
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:49.249Z

The same 6 tests fail at 55300e9, so they predate this round and are not from T-088/T-089. I'll check whether they also fail in the dirty main tree, to tell a committed-state failure from an archive artifact.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:49.835Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run full unit suite in the main working tree for comparison",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:44:31.827Z

**tool result**
````
FAILED tests/unit/test_trace.py::test_rejudge_in_demo_mode_replays_recorded_answers_and_clears_the_gate
FAILED tests/unit/test_trace.py::test_rejudge_with_nothing_to_do_asks_nothing
FAILED tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran
21 failed, 1397 passed in 40.77s
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:01.252Z

The six committed-state failures predate this round and do not touch the card files; the dirty main tree has 21, from other workers' in-progress tests. Before writing the reviews, I'll confirm the remaining line citations.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:02.532Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/clean && grep -n \"^PHRASE_MIN\\|^CATEGORY_MIN\\|^ELIGIBLE_TYPES\\|def _eligible\\|def apply\" app/backend/dismissal_patterns.py; grep -n \"for fid in s\\[\\\"flag_ids\\\"\\]\" app/backend/dismissal_patterns.py; echo ---; sed -n '105,108p;123,125p' tests/unit/test_dismissal_patterns.py | cut -c1-120; echo ---; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py show T-089 | grep -n '\"done\"' | cut -c1-140",
 "description": "Confirm remaining line numbers and T-089 AC done flag"
}
````

### User / tool · 2026-11-02T04:45:02.694Z

**tool result**
````
20:PHRASE_MIN = 3
21:CATEGORY_MIN = 5
22:ELIGIBLE_TYPES = ("pre_existing", "causation")
27:def _eligible(f) -> bool:
80:def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
86:    for fid in s["flag_ids"]:
---
def test_routes_apply_and_errors(tmp_path, monkeypatch):
    from tests.unit.test_api_routes import run_case
    c, db = _client(tmp_path, monkeypatch, "r.sqlite")
    t = run_case(c)
def _two_cases(c, db):
    """Case A holds three dismissals of a phrase; case B (a different token) holds only the pending match."""
    from tests.unit.test_api_routes import run_case
---
19:  - {"n": 1, "text": "Repeated dismissals of the same flag phrase surface as a suggestion ('You dismissed this 4 times'); never auto-dism
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:28.913Z

I have the citations I need. Before the first write to `reviews/`, I'll validate both JSON blocks in scratch files so the board validator does not reject them.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:36.120Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/t088_r2_block.json",
 "content": "{\"card\": \"T-088\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2, commit 55300e9 (app/backend/date_convention.py reason, memory/contracts/api.md, tests/unit/test_date_convention.py); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process, LLM_BACKEND=fixture)\",\n \"exercised\": [\"python3 tools/board.py show T-088, show T-096, list --role qa\", \"git show 55300e9 for the three in-scope files (full diff read)\", \"git diff 55300e9 7df65fb for the card paths and their helpers (empty)\", \".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; in the dirty main tree: 160 passed, 1238 deselected\", \"pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py in clean HEAD: 30 passed\", \"pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)\", \"probe_t088_r2.py on clean HEAD (artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt): golden reason, each named record checked against the golden source text, confirm of a non-candidate, packet reason\", \"mutate_r2.py on a scratch copy: R2-88a to R2-88h (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt), all caught\", \"git diff --cached --name-status -- the four card paths (empty); grep 'this record' and 'other dates in this record' over app, memory/contracts, tests and evals (only the contract's 'never described as' sentence and unrelated copy)\", \"grep -c 'suggestion|dismissal' on evals/golden/case_01_date_formats.expected.json (0); grep on app/frontend (0)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"code_only_no_llm\": 5, \"never_auto_applied_d041\": 5, \"reason_grounded_in_packet\": 5, \"mixed_packet_handling\": 4, \"tests_fail_on_mutation\": 5, \"ac_integrity\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"AC 1 is still done=true, and its eval half has no card\",\n   \"evidence\": \"python3 tools/board.py show T-088 → \\\"done\\\": true, \\\"evidence\\\": \\\"PARTIAL, corrected: backend half only. ...\\\"; the AC text still reads 'the UI pre-selects it' and 'eval case'. python3 tools/board.py list --role qa shows 11 cards (T-015 to T-093); none covers evals/golden/case_01_date_formats.expected.json. grep -c 'suggestion|dismissal' artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/case_01_date_formats.expected.json → 0.\",\n   \"why_it_matters\": \"The correction note is honest and the UI is now on T-096, but the gate still reads done=true, and the eval entry exists only as a note addressed to qa. Round 1 asked for done=false or a split into cards; only the UI was split. Until one of those is done, the board says AC 1 is met while two of its parts are not. Kept at major, not downgraded, because it is the same open round-1 finding.\",\n   \"fix\": \"Either set AC 1 done=false (the UI part stays on T-096, the eval part stays open), or amend the AC text to the backend half and open a qa card for the expected.json entry, using the assertion written in the T-088 note. Do not tick the eval part until expected.json contains it.\",\n   \"acceptance_test\": \"board show T-088 shows AC 1 done=false, or its text names only the backend half and a qa card exists for the eval entry; grep -c 'MM/DD' evals/golden/case_01_date_formats.expected.json is at least 1 once qa closes that card.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The handoff's '(160 pass)' does not reproduce at the commit\",\n   \"evidence\": \"T-088 handoff: \\\"pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass)\\\". Clean HEAD (artifacts/review-evidence/T-088-T-089-r2/clean): '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the 20 extra passes come from uncommitted tests (test_conflict_candidates.py, J3 tests in test_pipeline.py), not from this card. The card's own 30 tests pass in both trees.\",\n   \"why_it_matters\": \"A reviewer or the Stop hook that reruns the handoff command in a clean checkout gets a different number, so the quoted evidence cannot be reproduced at the commit.\",\n   \"fix\": \"Quote the card's own files in the handoff: pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py (30 passed), or the selector count taken from a clean checkout of the commit.\",\n   \"acceptance_test\": \"Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output.\"}\n ],\n \"whats_right\": [\"The reason names the record each example date sits in, and both names match the golden source: Record 2 holds 02/17/2026 and Record 6 holds 03-17-26 (probe_t088_r2_output.txt, checked against the '=== Record N ===' blocks in the golden text).\", \"Never auto-applied: auto_applied is false, the record stays ambiguous, and a non-candidate confirm is refused with 422.\", \"Every reason-wording mutant (singular and plural 'in this record', dropped or off-by-one record number) fails a named test, and the round-1 regression mutants (mixed order, swapped iso, auto-confirm) still fail.\"],\n \"questions_for_chris\": [\"Round-1 question, still open: for a packet whose dates disagree on order, should the paralegal see a short 'mixed packet' note, or is silence (no suggestion) the intended behaviour?\"]}\n"
}
````

### User / tool · 2026-11-02T04:45:36.227Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/t088_r2_block.json (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:45.644Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/t089_r2_block.json",
 "content": "{\"card\": \"T-089\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2, commit 55300e9 (tests/unit/test_dismissal_patterns.py; api.md T-089 section; app/backend/api.py:513 route wiring unchanged); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)\",\n \"exercised\": [\"python3 tools/board.py show T-089, show T-096, list --role qa\", \"git show 55300e9 -- tests/unit/test_dismissal_patterns.py and memory/contracts/api.md (full diff read)\", \"git diff 55300e9 7df65fb for the card paths (empty)\", \".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; dirty main tree: 160 passed, 1238 deselected\", \"pytest tests/unit/test_dismissal_patterns.py in clean HEAD: 21 passed\", \"pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)\", \"mutate_r2.py on a scratch copy (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt): 89a, 89b, 89c, 89d, 89d2, 89e, 89f, 89g, 89h, 89h2, 89i\", \"experiments_r2.py on the scratch copy (experiments_r2_output.txt): EXP_A pending gap flag with mutant 89d; EXP_B history rows seeded per golden case\", \"python3 -c '[] * 8 or [None]' → [None] (one history row)\", \"git diff --cached --name-status -- the four card paths (empty); grep -rn 'dismissal' app/frontend (0)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"never_auto_dismiss\": 5, \"no_pipeline_or_recall_effect\": 4, \"local_only_no_identity\": 4, \"demo_isolation_tested\": 5, \"tests_fail_on_mutation\": 4, \"ac_integrity\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"The gap-type eligibility rule still has no test that fails when it is removed\",\n   \"evidence\": \"artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt: 'MUTANT 89d gap type made eligible ... -> NOT CAUGHT :: 30 passed'. tests/unit/test_dismissal_patterns.py:185-194 (test_eligibility_rules_are_each_enforced_on_their_own) has the 6 gap dismissals but no pending gap flag, so no category suggestion can be offered for them. experiments_r2_output.txt: 'EXP_A mutant 89d with pending gap flag: CAUGHT' after a pending gap flag is added in the scratch copy.\",\n   \"why_it_matters\": \"The AC says ineligible types are never offered. The type rule (ELIGIBLE_TYPES, app/backend/dismissal_patterns.py:22) can be widened to gap flags without any test failing, which is the round-1 minor left open. The origin rule (89d2) is now caught.\",\n   \"fix\": \"In test_eligibility_rules_are_each_enforced_on_their_own, after the 6-dismissal history, add a pending flag with category gap_over_30, type gap, origin lexicon+llm and status None, then assert DP.suggest(conn, cid) == [] for it.\",\n   \"acceptance_test\": \"Mutant 89d (ELIGIBLE_TYPES includes gap) fails test_eligibility_rules_are_each_enforced_on_their_own; the unmutated file passes.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The golden identity test's comment says 8 generic dismissals; the code seeds 1, so six of ten golden cases are not history-sensitive\",\n   \"evidence\": \"tests/unit/test_dismissal_patterns.py:164 'for n, f in enumerate(history_from * 8 or [None]):'. With no eligible flag, history_from is [], [] * 8 is [], and the expression gives [None] (python3 -c \\\"print([] * 8 or [None])\\\" → [None]). The docstring at lines 157-159 says 'the generic new_onset history' of 8 dismissals. experiments_r2_output.txt 'EXPB' lines: history_rows_seeded=1 for case_01, case_02, case_03, case_04, case_05 and case_09 (eligible_flags=0); 8 or 24 or 56 rows for the cases that have eligible flags. Mutant 89i is caught only on case_06, case_07, case_08 and sample.\",\n   \"why_it_matters\": \"One dismissal is below PHRASE_MIN=3, so the 'generic' history cannot change any output, and a history-fed pipeline would pass the identity test on six of ten cases. The pipeline does not read history today (no output change), so this is a test-strength gap, not a live recall loss. Round 1 asked for per-case sensitivity; that is met for the four cases with eligible flags only.\",\n   \"fix\": \"Seed the generic history with 8 rows: change line 164 to 'for n, f in enumerate((history_from or [None]) * 8):'. Then the docstring is true. Note in the docstring that the six cases with no eligible flag are covered only through the generic new_onset history.\",\n   \"acceptance_test\": \"A test asserts that each golden case seeds 8 history rows; mutant 89i fails for every golden case that has a new_onset flag in its pipeline output, not only for case_06, case_07, case_08 and sample.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The handoff's '(160 pass)' does not reproduce at the commit\",\n   \"evidence\": \"T-089 handoff: \\\"pytest -k 'date or dismiss or suggest' (160 pass)\\\". Clean HEAD: '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the extra passes come from uncommitted tests in other cards. tests/unit/test_dismissal_patterns.py alone: 21 passed in both trees.\",\n   \"why_it_matters\": \"The quoted number cannot be reproduced at the commit, so the evidence in the handoff is not checkable from git.\",\n   \"fix\": \"Quote the card's own file: pytest tests/unit/test_dismissal_patterns.py (21 passed), or the selector count from a clean checkout of the commit.\",\n   \"acceptance_test\": \"Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output.\"}\n ],\n \"whats_right\": [\"Route wiring is now tested in both directions: forcing local scope (mutant 89h, api.py:513) fails test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route, and forcing public scope (89h2) fails test_local_mode_counts_the_machine_profile_through_the_route.\", \"The golden identity test now fails for a history-fed pipeline (89i) on case_06, case_07, case_08 and sample, not only on the sample, which meets the round-1 acceptance item.\", \"The category threshold boundary (89b, CATEGORY_MIN 4 vs 5) and the origin rule (89d2) now fail named tests; the apply partial-write behaviour is documented in api.md; the banner is tracked on T-096.\"],\n \"questions_for_chris\": [\"Round-1 question, still open: in local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?\"]}\n"
}
````

### User / tool · 2026-11-02T04:45:45.745Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2/t089_r2_block.json (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:48.920Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089-r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,sys\nfor p in ['t088_r2_block.json','t089_r2_block.json']:\n    d=json.load(open(p,encoding='utf-8'))\n    v=d['verdict']; sev=[f['severity'] for f in d['findings']]\n    rule='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\n    print(p, 'parsed OK', 'verdict', v, 'rule-verdict', rule, 'match' if v==rule else 'MISMATCH', 'findings', sev, 'whats_right', len(d['whats_right']))\n\"",
 "description": "Validate both JSON blocks and check verdict rule"
}
````

### User / tool · 2026-11-02T04:45:49.023Z

**tool result**
````
t088_r2_block.json parsed OK verdict changes rule-verdict changes match findings ['major', 'minor'] whats_right 3
t089_r2_block.json parsed OK verdict pass rule-verdict pass match findings ['minor', 'minor', 'minor'] whats_right 3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:50.268Z

Both blocks parse and match the verdict rule. Now I'll write the two review files.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:04.497Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer-r2.md",
 "content": "# T-088 round-2 review: date-convention suggestion (staff-engineer-reviewer)\n\n**Verdict: changes.** The round-1 blocker is closed: the reason now names the record each evidence date sits in, and both names match the golden source. Round-1 minors and the nit are closed. One major stays open: AC 1 is still `done: true` on the board, and its eval half has no card.\n\nScope: commit 55300e9 (round 2) on top of f667f08. HEAD moved during the review (d3130e3, then 7df65fb, a T-093 commit); I pinned the tree at 7df65fb. The card paths are byte-identical between 55300e9 and 7df65fb.\n\n**Round-1 items**\n\n| Round-1 item | Status | Evidence |\n|---|---|---|\n| Blocker: reason says \"in this record\" for dates in other records | Closed | `artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt`: REASON \"4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)\"; both records checked against the golden source; mutants R2-88a and R2-88b (old wording) fail named tests |\n| Major: AC 1 done while UI and eval are unbuilt | Open (partly corrected) | `board show T-088`: `\"done\": true`; AC text still names the UI and the eval case; no qa card (see F1) |\n| Major: shared index stages deletion of card files | Closed for these four paths | `git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py` prints nothing |\n| Minor: `and`/`or` precedence in the two-digit-year test | Closed | `tests/unit/test_date_convention.py:65` now `... and (s[\"iso\"] is None or s[\"iso\"] in ...)` |\n| Nit: unused `dates` import | Closed | `app/backend/date_convention.py` imports only `re` (line 8) |\n\n**Your checks**\n1. Reason names the records (golden case_01 record 8): holds. The ambiguous record is r8 (04/05/2026). Evidence is r2 (02/17/2026) and r6 (03-17-26), and the reason names both. Both dates sit inside `=== Record 2 ===` and `=== Record 6 ===` in `evals/golden/case_01_date_formats.txt`. The packet case in the unit test names Record 1 (`Another date in this packet uses month first (Record 1: 03/14/2026)`).\n2. Never auto-applied: holds. `auto_applied: False` (`date_convention.py:66`). The record stays `ambiguous`. A confirm with a non-candidate date returns 422 (probe). The UI pre-select is not built, so nothing reads the suggestion on the server path.\n3. AC 1 correction posted, UI moved to T-096: the correction is in the T-088 notes (04:34:55Z) and the UI is on T-096 (`ready`, AC includes the pre-select). **Not done:** the eval half has no card. The T-088 note asks qa to add the case_01 expected.json entry, but `board list --role qa` shows no card for it, and the expected file still has 0 matches for suggestion or dismissal. The AC flag stays `true`, which is F1.\n\n**Findings**\n- **F1 (major, open).** AC 1 is `done: true`. The correction is honest, but the gate still reads done. The round-1 options were done=false or a split into cards, and only the UI was split. Fix: set done=false, or amend the AC to the backend half and open a qa card for the eval entry.\n- **F2 (minor).** The handoff's \"(160 pass)\" does not reproduce at the commit. At 7df65fb the selector gives 140 passed. The 160 comes from the dirty main tree, which holds other workers' uncommitted tests. The card's own 30 tests pass in both trees.\n\n**Exercised** (all run by me; exact outputs in the files named)\n- `python3 tools/board.py show T-088`, `show T-096`, `list --role qa`.\n- `git show 55300e9` for the three in-scope files (full diff read); `git diff 55300e9 7df65fb` for the card paths and their helpers (empty).\n- `.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\"`: clean HEAD **140 passed, 1196 deselected**; dirty main tree **160 passed, 1238 deselected**.\n- `pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py`: **30 passed** (clean HEAD).\n- `pytest tests/unit` on clean HEAD: **6 failed, 1330 passed**. The same 6 fail at 55300e9 (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); none touches the card files. Outside these cards; see below.\n- `probe_t088_r2.py` on clean HEAD (`probe_t088_r2_output.txt`).\n- `mutate_r2.py` on a scratch copy (`mutation_run_r2.txt`): R2-88a to R2-88h all CAUGHT (singular and plural old wording, dropped and off-by-one record number, auto_applied true, mixed-order, swapped iso, auto-confirm).\n- `grep -rn \"other dates in this record\\|this record\"` over app, memory/contracts, tests, evals: no stale wording in the reason path.\n\n**Process note.** `git worktree add` was refused by the board-guard (reviewers may not run `git worktree` in the project). I pinned the same tree with `git archive` into `artifacts/review-evidence/T-088-T-089-r2/clean`.\n\n**Outside these cards (not findings on T-088 or T-089)**\n- Clean HEAD has 6 failing unit tests (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); the same 6 fail at 55300e9. The dirty main tree has 21 failures from in-progress work.\n- The shared index currently stages deletions of other cards' paths (`evals/reports/controls-20261102T042306Z.*`, `evals/golden/judge_controls_heldout.jsonl`, `.claude/agent-memory/qa/project_judge_controls.md`). That is the round-1 F3 hazard, for T-093's paths.\n\n```json\n{\"card\": \"T-088\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2, commit 55300e9 (app/backend/date_convention.py reason, memory/contracts/api.md, tests/unit/test_date_convention.py); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process, LLM_BACKEND=fixture)\",\n \"exercised\": [\"python3 tools/board.py show T-088, show T-096, list --role qa\", \"git show 55300e9 for the three in-scope files (full diff read)\", \"git diff 55300e9 7df65fb for the card paths and their helpers (empty)\", \".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; in the dirty main tree: 160 passed, 1238 deselected\", \"pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py in clean HEAD: 30 passed\", \"pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)\", \"probe_t088_r2.py on clean HEAD (artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt): golden reason, each named record checked against the golden source text, confirm of a non-candidate, packet reason\", \"mutate_r2.py on a scratch copy: R2-88a to R2-88h (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt), all caught\", \"git diff --cached --name-status -- the four card paths (empty); grep 'this record' and 'other dates in this record' over app, memory/contracts, tests and evals (only the contract's 'never described as' sentence and unrelated copy)\", \"grep -c 'suggestion|dismissal' on evals/golden/case_01_date_formats.expected.json (0); grep on app/frontend (0)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"code_only_no_llm\": 5, \"never_auto_applied_d041\": 5, \"reason_grounded_in_packet\": 5, \"mixed_packet_handling\": 4, \"tests_fail_on_mutation\": 5, \"ac_integrity\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"AC 1 is still done=true, and its eval half has no card\",\n   \"evidence\": \"python3 tools/board.py show T-088 → \\\"done\\\": true, \\\"evidence\\\": \\\"PARTIAL, corrected: backend half only. ...\\\"; the AC text still reads 'the UI pre-selects it' and 'eval case'. python3 tools/board.py list --role qa shows 11 cards (T-015 to T-093); none covers evals/golden/case_01_date_formats.expected.json. grep -c 'suggestion|dismissal' artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/case_01_date_formats.expected.json → 0.\",\n   \"why_it_matters\": \"The correction note is honest and the UI is now on T-096, but the gate still reads done=true, and the eval entry exists only as a note addressed to qa. Round 1 asked for done=false or a split into cards; only the UI was split. Until one of those is done, the board says AC 1 is met while two of its parts are not. Kept at major, not downgraded, because it is the same open round-1 finding.\",\n   \"fix\": \"Either set AC 1 done=false (the UI part stays on T-096, the eval part stays open), or amend the AC text to the backend half and open a qa card for the expected.json entry, using the assertion written in the T-088 note. Do not tick the eval part until expected.json contains it.\",\n   \"acceptance_test\": \"board show T-088 shows AC 1 done=false, or its text names only the backend half and a qa card exists for the eval entry; grep -c 'MM/DD' evals/golden/case_01_date_formats.expected.json is at least 1 once qa closes that card.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The handoff's '(160 pass)' does not reproduce at the commit\",\n   \"evidence\": \"T-088 handoff: \\\"pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass)\\\". Clean HEAD (artifacts/review-evidence/T-088-T-089-r2/clean): '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the 20 extra passes come from uncommitted tests (test_conflict_candidates.py, J3 tests in test_pipeline.py), not from this card. The card's own 30 tests pass in both trees.\",\n   \"why_it_matters\": \"A reviewer or the Stop hook that reruns the handoff command in a clean checkout gets a different number, so the quoted evidence cannot be reproduced at the commit.\",\n   \"fix\": \"Quote the card's own files in the handoff: pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py (30 passed), or the selector count taken from a clean checkout of the commit.\",\n   \"acceptance_test\": \"Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output.\"}\n ],\n \"whats_right\": [\"The reason names the record each example date sits in, and both names match the golden source: Record 2 holds 02/17/2026 and Record 6 holds 03-17-26 (probe_t088_r2_output.txt, checked against the '=== Record N ===' blocks in the golden text).\", \"Never auto-applied: auto_applied is false, the record stays ambiguous, and a non-candidate confirm is refused with 422.\", \"Every reason-wording mutant (singular and plural 'in this record', dropped or off-by-one record number) fails a named test, and the round-1 regression mutants (mixed order, swapped iso, auto-confirm) still fail.\"],\n \"questions_for_chris\": [\"Round-1 question, still open: for a packet whose dates disagree on order, should the paralegal see a short 'mixed packet' note, or is silence (no suggestion) the intended behaviour?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:46:04.640Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:21.122Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer-r2.md",
 "content": "# T-089 round-2 review: dismissal-pattern suggestions (staff-engineer-reviewer)\n\n**Verdict: pass.** No blocker and no major. Both round-1 majors are closed: the route-level demo-isolation tests fail when the route is forced to local or public scope, and the card files are no longer staged for deletion. Three minors remain: one eligibility rule still has no failing test, the golden identity test's comment does not match what it seeds, and the handoff's \"(160 pass)\" does not reproduce at the commit. The brief asked for the minors to be fixed; two of the four round-1 minors are closed and one is partly closed, and the new minor comes from the round-2 test rewrite.\n\nScope: commit 55300e9 (round 2) on top of f667f08. HEAD moved during the review (d3130e3, then 7df65fb, a T-093 commit); I pinned the tree at 7df65fb. The card paths are byte-identical between 55300e9 and 7df65fb. The route wiring at `app/backend/api.py:513` is unchanged.\n\n**Round-1 items**\n\n| Round-1 item | Status | Evidence |\n|---|---|---|\n| Major: route forced to local passes all tests (89h) | Closed | `mutation_run_r2.txt`: \"MUTANT 89h ROUTE forces local scope ... -> CAUGHT :: 1 failed\" (`test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route`); 89h2 (route forced public) also CAUGHT by `test_local_mode_counts_the_machine_profile_through_the_route` |\n| Major: shared index stages deletion of card files | Closed for these four paths | `git diff --cached --name-status -- <4 paths>` prints nothing |\n| Minor: eligibility rules tested only as a conjunction | Partly closed | 89d2 (origin rule) CAUGHT by `test_eligibility_rules_are_each_enforced_on_their_own`; 89d (type rule) still NOT CAUGHT (F1) |\n| Minor: category boundary and golden identity sensitivity | Closed for the stated acceptance; comment wrong (F2) | 89b CAUGHT by `test_category_threshold_is_exactly_five`; 89i CAUGHT on case_06, case_07, case_08 and sample (not only sample) |\n| Minor: banner not built | Closed by tracking | T-096 AC: \"dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089)\" |\n| Nit: apply not atomic | Closed by documenting | `memory/contracts/api.md:284` now says \"The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed\" (the round-1 fix allowed documenting) |\n\n**Your checks**\n1. Route-level isolation: the tests fail when the route is forced. Mutant 89h (`app/backend/api.py:513`, `local_mode=lambda: True`) fails `test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route`. Mutant 89h2 (forced public) fails `test_local_mode_counts_the_machine_profile_through_the_route`. Both are in the scratch copy; the repo was not edited.\n2. Minors: 89b, 89d2 and 89i are caught; 89d is not (F1). The golden identity test is sensitive on four of ten cases (F2).\n3. Sanity: suggest() is still read-only (89e caught by 7 tests), the GET does not apply (89f caught), bulk-applied flags are not counted (89c caught), and history is scoped to the case in public mode (89g caught).\n\n**Findings**\n- **F1 (minor, open).** The gap-type eligibility rule has no failing test. Mutant 89d (gap added to ELIGIBLE_TYPES) gives 30 passed. Adding one pending gap flag to the existing eligibility test makes 89d fail (`experiments_r2_output.txt`, EXP_A). Fix: add that flag and assert `suggest() == []`.\n- **F2 (minor, new in round 2).** `tests/unit/test_dismissal_patterns.py:164` seeds `history_from * 8 or [None]`. When a case has no eligible flag, that is `[None]`, one dismissal, not the 8 the docstring states. One dismissal is below PHRASE_MIN, so six of ten golden cases (case_01 to case_05 and case_09) have no sensitivity to history (`experiments_r2_output.txt`, EXP_B: `history_rows_seeded=1`). The pipeline does not read history today, so there is no output change; this is a test-strength and comment-accuracy gap.\n- **F3 (minor).** The handoff's \"(160 pass)\" does not reproduce at the commit. At 7df65fb the selector gives 140 passed; the extra passes come from uncommitted tests in other cards. `tests/unit/test_dismissal_patterns.py` alone gives 21 passed in both trees.\n\n**Exercised** (all run by me; exact outputs in the files named)\n- `python3 tools/board.py show T-089`, `show T-096`, `list --role qa`.\n- `git show 55300e9` for `tests/unit/test_dismissal_patterns.py` and `memory/contracts/api.md` (full diff read); `git diff 55300e9 7df65fb` for the card paths (empty).\n- `.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\"`: clean HEAD **140 passed, 1196 deselected**; dirty main tree **160 passed, 1238 deselected**.\n- `pytest tests/unit/test_dismissal_patterns.py` (clean HEAD): **21 passed**.\n- `pytest tests/unit` (clean HEAD): **6 failed, 1330 passed**; the same 6 fail at 55300e9. None touches these cards. Outside these cards; see below.\n- `mutate_r2.py` on a scratch copy (`mutation_run_r2.txt`): 89a, 89b, 89c, 89d, 89d2, 89e, 89f, 89g, 89h, 89h2, 89i run; baseline and restored both 30 passed.\n- `experiments_r2.py` on the scratch copy (`experiments_r2_output.txt`): EXP_A (pending gap flag with mutant 89d: CAUGHT); EXP_B (history rows seeded per golden case).\n- `python3 -c \"print([] * 8 or [None])\"` → `[None]`.\n- `git diff --cached --name-status -- <4 card paths>` (empty); `grep -rn dismissal app/frontend` (0).\n\n**Process note.** `git worktree add` was refused by the board-guard (reviewers may not run `git worktree` in the project). I pinned the same tree with `git archive` into `artifacts/review-evidence/T-088-T-089-r2/clean`.\n\n**Outside these cards (not findings on T-089)**\n- Clean HEAD has 6 failing unit tests (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); the same 6 fail at 55300e9. The dirty main tree has 21 failures from in-progress work.\n- The shared index currently stages deletions of other cards' paths (`evals/reports/controls-20261102T042306Z.*`, `evals/golden/judge_controls_heldout.jsonl`, `.claude/agent-memory/qa/project_judge_controls.md`). That is the round-1 F3 hazard, for T-093's paths.\n\n```json\n{\"card\": \"T-089\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2, commit 55300e9 (tests/unit/test_dismissal_patterns.py; api.md T-089 section; app/backend/api.py:513 route wiring unchanged); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)\",\n \"exercised\": [\"python3 tools/board.py show T-089, show T-096, list --role qa\", \"git show 55300e9 -- tests/unit/test_dismissal_patterns.py and memory/contracts/api.md (full diff read)\", \"git diff 55300e9 7df65fb for the card paths (empty)\", \".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; dirty main tree: 160 passed, 1238 deselected\", \"pytest tests/unit/test_dismissal_patterns.py in clean HEAD: 21 passed\", \"pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)\", \"mutate_r2.py on a scratch copy (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt): 89a, 89b, 89c, 89d, 89d2, 89e, 89f, 89g, 89h, 89h2, 89i\", \"experiments_r2.py on the scratch copy (experiments_r2_output.txt): EXP_A pending gap flag with mutant 89d; EXP_B history rows seeded per golden case\", \"python3 -c 'print([] * 8 or [None])' → [None] (one history row)\", \"git diff --cached --name-status -- the four card paths (empty); grep -rn 'dismissal' app/frontend (0)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"never_auto_dismiss\": 5, \"no_pipeline_or_recall_effect\": 4, \"local_only_no_identity\": 4, \"demo_isolation_tested\": 5, \"tests_fail_on_mutation\": 4, \"ac_integrity\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"The gap-type eligibility rule still has no test that fails when it is removed\",\n   \"evidence\": \"artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt: 'MUTANT 89d gap type made eligible ... -> NOT CAUGHT :: 30 passed'. tests/unit/test_dismissal_patterns.py:185-194 (test_eligibility_rules_are_each_enforced_on_their_own) has the 6 gap dismissals but no pending gap flag, so no category suggestion can be offered for them. experiments_r2_output.txt: 'EXP_A mutant 89d with pending gap flag: CAUGHT' after a pending gap flag is added in the scratch copy.\",\n   \"why_it_matters\": \"The AC says ineligible types are never offered. The type rule (ELIGIBLE_TYPES, app/backend/dismissal_patterns.py:22) can be widened to gap flags without any test failing, which is the round-1 minor left open. The origin rule (89d2) is now caught.\",\n   \"fix\": \"In test_eligibility_rules_are_each_enforced_on_their_own, after the 6-dismissal history, add a pending flag with category gap_over_30, type gap, origin lexicon+llm and status None, then assert DP.suggest(conn, cid) == [] for it.\",\n   \"acceptance_test\": \"Mutant 89d (ELIGIBLE_TYPES includes gap) fails test_eligibility_rules_are_each_enforced_on_their_own; the unmutated file passes.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The golden identity test's comment says 8 generic dismissals; the code seeds 1, so six of ten golden cases are not history-sensitive\",\n   \"evidence\": \"tests/unit/test_dismissal_patterns.py:164 'for n, f in enumerate(history_from * 8 or [None]):'. With no eligible flag, history_from is [], [] * 8 is [], and the expression gives [None] (python3 -c \\\"print([] * 8 or [None])\\\" → [None]). The docstring at lines 157-159 says 'the generic new_onset history' of 8 dismissals. experiments_r2_output.txt 'EXPB' lines: history_rows_seeded=1 for case_01, case_02, case_03, case_04, case_05 and case_09 (eligible_flags=0); 8, 24 or 56 rows for the cases that have eligible flags. Mutant 89i is caught only on case_06, case_07, case_08 and sample.\",\n   \"why_it_matters\": \"One dismissal is below PHRASE_MIN=3, so the 'generic' history cannot change any output, and a history-fed pipeline would pass the identity test on six of ten cases. The pipeline does not read history today (no output change), so this is a test-strength gap, not a live recall loss. Round 1 asked for per-case sensitivity; that is met for the four cases with eligible flags only.\",\n   \"fix\": \"Seed the generic history with 8 rows: change line 164 to 'for n, f in enumerate((history_from or [None]) * 8):'. Then the docstring is true. Note in the docstring that the six cases with no eligible flag are covered only through the generic new_onset history.\",\n   \"acceptance_test\": \"A test asserts that each golden case seeds 8 history rows; mutant 89i fails for every golden case that has a new_onset flag in its pipeline output, not only for case_06, case_07, case_08 and sample.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The handoff's '(160 pass)' does not reproduce at the commit\",\n   \"evidence\": \"T-089 handoff: \\\"pytest -k 'date or dismiss or suggest' (160 pass)\\\". Clean HEAD: '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the extra passes come from uncommitted tests in other cards. tests/unit/test_dismissal_patterns.py alone: 21 passed in both trees.\",\n   \"why_it_matters\": \"The quoted number cannot be reproduced at the commit, so the evidence in the handoff is not checkable from git.\",\n   \"fix\": \"Quote the card's own file: pytest tests/unit/test_dismissal_patterns.py (21 passed), or the selector count from a clean checkout of the commit.\",\n   \"acceptance_test\": \"Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output.\"}\n ],\n \"whats_right\": [\"Route wiring is now tested in both directions: forcing local scope (mutant 89h, api.py:513) fails test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route, and forcing public scope (89h2) fails test_local_mode_counts_the_machine_profile_through_the_route.\", \"The golden identity test now fails for a history-fed pipeline (89i) on case_06, case_07, case_08 and sample, not only on the sample, which meets the round-1 acceptance item.\", \"The category threshold boundary (89b, CATEGORY_MIN 4 vs 5) and the origin rule (89d2) now fail named tests; the apply partial-write behaviour is documented in api.md; the banner is tracked on T-096.\"],\n \"questions_for_chris\": [\"Round-1 question, still open: in local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:46:21.292Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:28.019Z

Both files are written. The T-089 summary miscounts the round-1 minors (there were three minors plus a nit, not four minors). I'll correct that sentence.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:29.038Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer-r2.md",
 "old_string": "The brief asked for the minors to be fixed; two of the four round-1 minors are closed and one is partly closed, and the new minor comes from the round-2 test rewrite.",
 "new_string": "Round 1 had two majors, three minors and a nit. Both majors are closed. Of the minors, two are closed (the banner is tracked on T-096; the category and golden-identity tests now fail on the mutants, with a comment error recorded as F2), and one is partly closed (the origin rule is tested, the type rule is not, F1). The nit is closed by documentation. So the brief's \"minors fixed\" is not fully met."
}
````

### User / tool · 2026-11-02T04:46:29.088Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-089-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:32.081Z

The guard blocks edits to an existing review, so I can't fix that sentence in place. I'll disclose it in my reply rather than create a third file. Next I'll confirm the JSON blocks in both reviews parse, then remove the scratch copies of the product tree.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:33.771Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,re\nfor p in ['reviews/T-088-staff-engineer-r2.md','reviews/T-089-staff-engineer-r2.md']:\n    t=open(p,encoding='utf-8').read()\n    blocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\n    d=json.loads(blocks[0]) if len(blocks)==1 else None\n    print(p, 'json blocks:', len(blocks), 'parsed:', d is not None, '| card', d and d['card'], '| verdict', d and d['verdict'], '| findings', d and [f['severity'] for f in d['findings']])\n\"; echo \"--- removing scratch product copies (keep evidence files)\"; rm -rf artifacts/review-evidence/T-088-T-089-r2/clean artifacts/review-evidence/T-088-T-089-r2/mut artifacts/review-evidence/T-088-T-089-r2/prev && ls artifacts/review-evidence/T-088-T-089-r2/; git status --short reviews/ artifacts/review-evidence/T-088-T-089-r2 | head",
 "description": "Verify review JSON blocks parse and remove scratch product copies"
}
````

### User / tool · 2026-11-02T04:46:33.828Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:36.159Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-088-T-089-r2/check_blocks.py 2>/dev/null; cat > artifacts/review-evidence/T-088-T-089-r2/check_blocks.py <<'EOF'\nimport json\nimport re\n\nfor p in [\"reviews/T-088-staff-engineer-r2.md\", \"reviews/T-089-staff-engineer-r2.md\"]:\n    t = open(p, encoding=\"utf-8\").read()\n    blocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\n    d = json.loads(blocks[0]) if len(blocks) == 1 else None\n    print(p, \"json blocks:\", len(blocks), \"parsed:\", d is not None, \"| card:\", d and d[\"card\"], \"| verdict:\", d and d[\"verdict\"],\n          \"| findings:\", d and [f[\"severity\"] for f in d[\"findings\"]])\nEOF\n.venv/bin/python artifacts/review-evidence/T-088-T-089-r2/check_blocks.py",
 "description": "Verify review JSON blocks parse using a scratch checker script"
}
````

### User / tool · 2026-11-02T04:46:36.393Z

**tool result**
````
reviews/T-088-staff-engineer-r2.md json blocks: 1 parsed: True | card: T-088 | verdict: changes | findings: ['major', 'minor']
reviews/T-089-staff-engineer-r2.md json blocks: 1 parsed: True | card: T-089 | verdict: pass | findings: ['minor', 'minor', 'minor']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:37.804Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-088-T-089-r2/clean artifacts/review-evidence/T-088-T-089-r2/mut artifacts/review-evidence/T-088-T-089-r2/prev && ls artifacts/review-evidence/T-088-T-089-r2/",
 "description": "Remove scratch product copies and keep evidence files"
}
````

### User / tool · 2026-11-02T04:46:38.404Z

**tool result**
````
check_blocks.py
collect_clean.txt
collect_main.txt
experiments_r2.py
experiments_r2_output.txt
mutate_r2.py
mutation_run_r2.txt
probe_t088_r2.py
probe_t088_r2_output.txt
t088_r2_block.json
t089_r2_block.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:44.038Z

Scratch copies are removed and the evidence files remain. Last step is memory: I'll record the round-2 patterns in my existing T-088/T-089 note and the harness note.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:44.642Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat MEMORY.md | grep -n \"T-088\\|harness\" ; echo ---; tail -5 project_harness_review_patterns.md",
 "description": "Read memory index entries and harness note tail"
}
````

### User / tool · 2026-11-02T04:46:44.731Z

**tool result**
````
1:- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
25:- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason says "in this record" for packet evidence, AC done with UI unbuilt, index stages card deletions, route isolation untested
---
- (T-070 r2, 2026-11-01) A shell `>` redirect into the scratchpad is denied by board-guard ("reviewers may only write under reviews/..."), even though `tar -x -C` and `cp -R` into the same dir pass. Capture output with `2>&1; echo rc=$?` inside the command instead of redirecting. Chained `$(...)` loops with nested quotes trip git-guard's parser; use one probe per Bash call.
- (T-090 r2, 2026-11-01) `->` inside a `python -c` print string is read as a redirect ("redirect to 84"); `git worktree` is denied in the project ("allowed only in scratch repos under /tmp"). Use `git clone <project> <scratch>/clone` then `git checkout --detach <sha>` inside the clone. `git checkout` in the clone was denied once when the Bash cwd had been the project; split the call and use a saved pristine copy plus `cp` to restore a mutated file. `-I` runs need `sys.path.insert(0, clone)` plus `runpy.run_module` because `-I` drops cwd from sys.path.
- (T-093 r2, 2026-11-02) board-guard denies `git worktree` in the project and `git worktree list` too, even with a scratchpad path under /private/tmp ("allowed only in scratch repos under /tmp"). Use `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-<sha>/` for a clean HEAD tree; it covers tracked files only, which is what a clean worktree gives. `rm -rf` of that copy was denied, so leave it and say so in `exercised`.
- (T-093 r2) HEAD moved twice during one review (7df65fb -> bc12d44 -> a850be0). Pin every citation with `git show <sha>:path`, and say in scope which sha was reviewed. `git status` changed between two calls in the same review (staged deletions and untracked copies of the same path).
- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command (even in a grep pattern such as `pending > 0`) as a redirect and denies the call. Use `grep -e` patterns without angle brackets. A `Write` into the scratchpad is denied by reviewer-write-guard, but a `cat <<'EOF' > scratchpad/file` heredoc in Bash works (no `>` problem there). `rm -rf` is denied; `mkdir -p` plus `cp -R` works. macOS has no `timeout` binary; pass the pytest/e2e timeout parameter instead. Kill the scratch server by its PID from `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:51.210Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t088_t089_review_patterns.md",
 "old_string": "**How to apply:** mutation runs in this repo must write under `artifacts/review-evidence/`",
 "new_string": "**r2 (55300e9, reviewed at HEAD 7df65fb) additions:**\n- A correction posted in the card notes does not clear a gate: T-088 AC1 still read `done: true` while its eval half had no card (only a note to qa). Read `board.py list --role <r>` to see whether an untracked half has a card, and check the `done` flag, not the evidence prose.\n- A test fix for a conjunction rule only works with a pending match in place. T-089 eligibility test had 6 gap dismissals but no pending gap flag, so widening ELIGIBLE_TYPES to gap survived. Add one pending flag and the mutant is caught (EXP_A).\n- Seeding `history * 8 or [None]` gives ONE row when history is empty (`[] * 8` is falsy). The comment said 8. Count the seeded rows per case, not the comment; six of ten golden cases were not history-sensitive.\n- Reason-scope fixes verify best against the golden SOURCE text parsed separately (`=== Record N ===` blocks), not the app's own parser.\n- Handoff counts must reproduce at the commit: the \"160 pass\" came from the dirty main tree (other workers' untracked tests); clean HEAD gave 140. Card-file counts (30) were stable.\n- Committed-HEAD full suite had 6 failures (test_trace x4, t075, t037) that predate the card. Report as outside scope, do not attribute.\n- Mutants that need a copy: `mutate_r2.py` with anchors; re-check anchor counts after each commit (they were all still unique at 7df65fb).\n\n**How to apply:** mutation runs in this repo must write under `artifacts/review-evidence/`"
}
````

### User / tool · 2026-11-02T04:46:51.313Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t088_t089_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:52.292Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason says \"in this record\" for packet evidence, AC done with UI unbuilt, index stages card deletions, route isolation untested",
 "new_string": "- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row"
}
````

### User / tool · 2026-11-02T04:46:52.397Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:53.756Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command",
 "new_string": "- (T-088/T-089 r2, 2026-11-02) board-guard denied `git worktree` in the project; `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-r2/clean` worked. git-guard failed closed on `H=$(git rev-parse HEAD)` in command position, so use literal shas. reviewer-write-guard denied an Edit to my own existing `reviews/T-089-staff-engineer-r2.md` (append-only), so a wrong summary sentence stayed and was disclosed in the reply; proof-read the summary before the first Write.\n- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command"
}
````

### User / tool · 2026-11-02T04:46:53.853Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:57.470Z

T-088 r2: changes (AC1 still `done: true`, major); T-089 r2: pass (three minors, route-isolation mutants caught). Reviews: `/Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer-r2.md` and `/Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer-r2.md` (the T-089 summary miscounts round-1 minors and the write guard blocked my fix).
