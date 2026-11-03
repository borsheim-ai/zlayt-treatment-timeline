# Subagent: Staff review T-120/121/123/125 (Staff review T-120/121/123/125)

Source: `agent-ad01baad295176ba6.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:14:38.503Z

You are the staff-engineer reviewer for board cards T-120, T-121, T-123 and T-125 in /Users/arsis/zlayt-pm-project. Read each card with `python3 tools/board.py show T-###`, including its handoff and commits. Run the diffs on a `git archive HEAD` copy in your scratchpad, and run the unit suite there.

Check each card for:
- correctness and determinism;
- the LLM/code boundary;
- test quality: would the test fail on a regression? Mutate to check.

T-125 has one more check: any re-recorded judge answer must be a real live recording, never written by hand (D-056). Verify that tests/unit/test_curated_fixtures.py passes, and check the fixture provenance.

Write one file per card, reviews/T-###-staff-engineer.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Write any key values as <redacted>. Stop only your own PIDs. Reply in 4 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:40.547Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:14:40.561Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:41.466Z

**tool call — Bash**
````
{
 "command": "for t in T-120 T-121 T-123 T-125; do echo \"=== $t\"; python3 tools/board.py show $t; done; git log --oneline | head -15; git status --short | head"
}
````

### User / tool · 2026-11-02T11:14:41.823Z

**tool result**
````
=== T-120
---
id: "T-120"
title: "No prior-condition flag on an interpreter sentence ('Hx obtained via patient's son, who interpreted')"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:41:17Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:02:21Z"
rounds: 0
commits: ["1cb8707"]
reviews: []
ac:
  - {"n": 1, "text": "lib09 raises no 'Mention of a prior or pre-existing condition' flag on the interpreter-history sentence of record 2; a real prior-condition mention in another record still raises the flag (unit test for both)", "done": true, "evidence": "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)"}
  - {"n": 2, "text": "tests/unit covers the rule so it cannot regress; evals report unchanged otherwise", "done": true, "evidence": "17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:41:20Z frontend: Filed by frontend from T-060 pass-2 paralegal F13 (reviews/T-060-paralegal-pass2.md). Frontend cannot change it: the flag comes from the backend flag engine.
- 2026-11-02T11:02:21Z backend: claimed
- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)
- 2026-11-02T11:11:31Z backend: AC 2 checked: 17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change
- 2026-11-02T11:11:31Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: lexicon_scan skips a pre_existing hit on bare Hx/h/o/PHx/history directly followed by a source phrase (obtained/taken/provided... via/from/by, or per/via). Code guard; lexicon.yaml untouched (researcher-owned). How verified: new tests; evals.run fixture flag P/R 1.000. Surprised: dropping the lexicon flag renumbered lib09 record 1 flag ids, so the J4 fixture key missed (see T-125). Left: none.

=== T-121
---
id: "T-121"
title: "Letter text: optional one-line entry form, and the Spanish translation note as a bracketed removable phrase (paralegal T-060 pass 2 F9)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:41:20Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:11:33Z"
rounds: 0
commits: ["c26ff04"]
reviews: []
ac:
  - {"n": 1, "text": "GET /export accepts an option (e.g. ?style=oneline) giving one line per entry: 'date — provider: \"quote\" [Ex. __ / Bates __]' built by code; the default letter is unchanged and still equals evals/golden", "done": true, "evidence": "tests/unit/test_t121_letter_styles.py (oneline, config/page, standard==golden, API ?style) + test_export.py golden byte-equal pass"}
  - {"n": 2, "text": "In every letter style an AI-translation note is a bracketed phrase at the end of the entry, [AI translation of the Spanish original; check before sending], never a line that starting with 'AI translation:'; golden and unit tests updated", "done": true, "evidence": "test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles; test_spanish_records/test_d050 updated"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:41:23Z frontend: Filed by frontend from T-060 pass-2 paralegal F9. The letter is built by the server and the UI copies it verbatim, so the prefix/layout cannot change in app/frontend. Frontend side is done: letter box sized to its text, Download .txt for letter and notes (T-060 r3).
- 2026-11-02T11:11:31Z backend: AC 1 checked: tests/unit/test_t121_letter_styles.py (oneline, config/page, standard==golden, API ?style) + test_export.py golden byte-equal pass
- 2026-11-02T11:11:31Z backend: AC 2 checked: test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles; test_spanish_records/test_d050 updated
- 2026-11-02T11:11:33Z backend: claimed
- 2026-11-02T11:11:34Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: export.build_export/build_letter take style (standard|oneline); GET /export?style= (422 invalid_style otherwise); translation label becomes a bracketed note at the end of the entry in both styles; api.md updated. How verified: new tests, golden byte equality. Left: frontend can add a style toggle (note for frontend). Surprised: none.

=== T-123
---
id: "T-123"
title: "Accident baseline: never call same-day paperwork or questionnaire/authorization headers the first recorded treatment (T-116 r5 major)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:50:55Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T10:55:45Z"
rounds: 0
commits: ["0c47356"]
reviews: []
ac:
  - {"n": 1, "text": "Accident-baseline text uses the warn wording for same-day paperwork and questionnaire/authorization headers; tests with the reviewer's r5 probes", "done": true, "evidence": "tests/unit/test_t123_baseline_same_day_paperwork.py (21) + test_t116_gap_endpoints.py pass; r5 headers probe: first_recorded_treatment=False for all 11 headers; B2 same-day both orders name no paperwork as treatment"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:55:45Z backend: claimed
- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t123_baseline_same_day_paperwork.py (21) + test_t116_gap_endpoints.py pass; r5 headers probe: first_recorded_treatment=False for all 11 headers; B2 same-day both orders name no paperwork as treatment
- 2026-11-02T11:11:30Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: conflicts.accident_date_conflicts uses the warn wording whenever ANY record on the earliest date is paperwork (alone or sharing the date with a visit, either order); gaps admin list gains bare questionnaire and authorization request (header-only). An older test that asserted no warning for same-day paperwork was updated to the r5 reading. How verified: new tests, r5 probe scripts, unit suite green except test_summary_trim (another worker's in-flight summary_trim.py). Left: none. Surprised: the J4/judge keys do not matter here; wording is code-only.

=== T-125
---
id: "T-125"
title: "lib09 demo: f_r1_1 j4 judge fixture miss (JUDGE_NOT_RUN) fails test_t114_rates_and_demo_judges"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:06:32Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:06:51Z"
rounds: 0
commits: ["4e294d7"]
reviews: []
ac:
  - {"n": 1, "text": "test_t114_rates_and_demo_judges passes for all cases on a clean HEAD; any re-recorded judge answer is a real live recording (D-056), cause noted (likely a prompt-version key change from T-113 v6)", "done": true, "evidence": "tests/unit/test_t114_rates_and_demo_judges.py 20 passed; fixture 0a68ecb1... recorded live via claude-cli (recorded_from claude-cli, haiku-5-5), commit 4e294d7"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:06:51Z backend: claimed
- 2026-11-02T11:11:31Z backend: AC 1 checked: tests/unit/test_t114_rates_and_demo_judges.py 20 passed; fixture 0a68ecb1... recorded live via claude-cli (recorded_from claude-cli, haiku-5-5), commit 4e294d7
- 2026-11-02T11:11:31Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Cause: T-120 removed the lexicon pre_existing flag on lib09 record 1, so the model's patient_report flag moved from f_r1_2 to f_r1_1; the J4 prompt carries the item id, so the recorded key missed. No prompt change. Re-recorded only that J4 answer with --fill-missing under claude-cli (real recording, D-056). Verified: the t114 file passes.

c26ff04 feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
c89ac86 docs(orchestrator): D-057 rule-filtered model proposals are listed collapsed, not dropped
4e294d7 test(backend): T-125 record the lib09 f_r1_1 J4 answer live (claude-cli); T-120 renumbered the flag so the old key missed
0410c52 test(evals): T-113 live 3-run on e1ce8dc, ship_bar_met, J3 v6 16/16 caught 0 false agree
1cb8707 fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
0c47356 fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
d56328a test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
db7f6d0 docs(orchestrator): D-054 states the T-112 r2 salient-content trim rule (T-112 r2 major 2)
e1ce8dc fix(backend): a never-judged LLM_ONLY tray item carries its real reason, not JUDGE_UNAVAILABLE (T-122; case_05 f_r1_1 judge_unavailable 1 -> 0)
7d5a45f fix(frontend): refusal, edit box and blocked notice span the full row inside the compact grid (T-060 r3)
f8f358e fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
1b93582 fix(backend): D-054 trims only salient new content; split-off and tray-trace fixes (T-112 r2)
d9efc5c test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export, compact rows, decided rows, 320 px reflow, theme-toggle name, held rechecks (T-060 r3, T-119)
5d975ed feat(frontend): compact review rows, one checks card, batch button in the Timeline toolbar, Start review, compact charges rows with cents, letter box sized to its text and Download .txt (T-060 r3)
c8e36fb fix(frontend): shortcut sheet prints its keys; theme toggle name follows state; skip-link targets exist; Tab start reset after a case opens; decided rows show Accepted/Dismissed and Undo; tray items named with a record cue in the AI-check panel (T-060 r3, T-117)
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:46.203Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/r1/a && git archive HEAD | tar -x -C $S/r1/a && cd $S/r1/a && ls && ls .venv 2>/dev/null | head -2; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md | head -20; git -C /Users/arsis/zlayt-pm-project status --short | grep -v agent-memory | head -20"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:46.548Z

**tool call — Bash**
````
{
 "command": "git show --stat 1cb8707 c26ff04 0c47356 4e294d7 | grep -v '^$'"
}
````

### User / tool · 2026-11-02T11:14:46.801Z

**tool result**
````
c26ff04c64ae77bd0ef7385b843c1702ef759ce2
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
---
name: feedback_shared_scratchpad
description: the scratchpad path is shared with other agents; use a unique card-round subdir, verify archive copies with diff -rq against a fresh git archive, never background a setup chain you depend on
metadata:
  type: feedback
---

Name scratch directories with the card and round (for example `T108_verify`), and run `ls -la` before reusing any directory. Check an archive copy with `diff -rq` against a fresh `git archive <sha>` before trusting results.

**Why:** during T-108 r1 the `probe/` folder I used already held another agent's repo archive, and sibling folders (`T106_*`) appeared in the same scratchpad during my run. My own setup line `mkdir -p X && cp ... && cd ... &` was backgrounded as one chain, so the following commands ran before the directory existed and wrote nothing.

**How to apply:** do not background setup you depend on; run it in the foreground or wait on it. Keep probe scripts in your own unique directory and copy the final ones to `artifacts/review-evidence/<card>/` as the evidence.

Related: [[project_t108_quote_units_patterns]].
 M app/backend/api.py
 M app/backend/confidence.py
 M app/backend/flag_templates.py
 M app/backend/flags.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/store.py
M  app/backend/summary_trim.py
 M app/backend/trace.py
 M app/backend/why.py
 M app/frontend/app.js
 M app/frontend/dom.js
 M app/frontend/flags.js
 M app/frontend/judges.js
 M app/frontend/manual.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/styles.css
 M app/frontend/switcher.js
 M app/frontend/timeline.js
````

### User / tool · 2026-11-02T11:14:46.908Z

**tool result**
````
commit 1cb8707129c6e7890a765e695d15c0be73683a0b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:45 2026 -0600
    fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
 app/backend/lexicon_scan.py                     |  6 ++++
 tests/unit/test_t120_history_source_sentence.py | 47 +++++++++++++++++++++++++
 2 files changed, 53 insertions(+)
commit c26ff04c64ae77bd0ef7385b843c1702ef759ce2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:11:18 2026 -0600
    feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
 app/backend/api.py                     |   6 +-
 app/backend/export.py                  |  41 +++++++++---
 app/backend/export_routes.py           |  14 +++--
 memory/contracts/api.md                |   4 +-
 tests/unit/test_d050_never_verified.py |   2 +-
 tests/unit/test_spanish_records.py     |   4 +-
 tests/unit/test_t121_letter_styles.py  | 112 +++++++++++++++++++++++++++++++++
 7 files changed, 163 insertions(+), 20 deletions(-)
commit 0c473563bed3cd6b74ac0db83ee47cb13785fb71
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:33 2026 -0600
    fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
 app/backend/conflicts.py                           | 15 +++--
 app/backend/gaps.py                                |  4 +-
 tests/unit/test_t116_gap_endpoints.py              |  4 +-
 .../unit/test_t123_baseline_same_day_paperwork.py  | 64 ++++++++++++++++++++++
 4 files changed, 78 insertions(+), 9 deletions(-)
commit 4e294d7d137e4b39b07bcf3082411c90c67071ab
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:52 2026 -0600
    test(backend): T-125 record the lib09 f_r1_1 J4 answer live (claude-cli); T-120 renumbered the flag so the old key missed
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
 ...b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a.json | 11 +++++++++++
 1 file changed, 11 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:50.431Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a; git show 1cb8707 -- app tests; ls $S/tests; ls .venv/bin/python; cat $S/pytest.ini $S/pyproject.toml 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T11:14:50.574Z

**tool result**
````
commit 1cb8707129c6e7890a765e695d15c0be73683a0b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:45 2026 -0600

    fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/lexicon_scan.py b/app/backend/lexicon_scan.py
index d998fe4..f7858b7 100644
--- a/app/backend/lexicon_scan.py
+++ b/app/backend/lexicon_scan.py
@@ -9,6 +9,10 @@ TOKEN = re.compile(r"[\w'/-]+|[;,]")
 SENT_END = re.compile(r"[.!?](?=\s|$)|\n")
 YEAR = re.compile(r"\b(19|20)\d{2}\b")
 RAISES = ("high", "medium")
+# T-120: "Hx obtained via patient's son, who interpreted" names who GAVE the history; it states no prior condition. Only the bare history
+# abbreviation or word, directly followed by a source word, is skipped ("Hx of lumbar strain", "Hx: neck pain" still hit).
+_HISTORY_WORD = re.compile(r"(?:hx|h/o|phx|history)\Z", re.I)
+_HISTORY_SOURCE = re.compile(r"\s+(?:(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+(?:via|from|by|through|per|with)\b|(?:per|via)\s)", re.I)
 
 
 def _sentence_bounds(text, start, end):
@@ -129,6 +133,8 @@ def scan(text: str, accident_year=None) -> list:
                     continue
             if sup and sup.search(_clause_after(text, m.end())):
                 continue
+            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _HISTORY_SOURCE.match(text, m.end()):
+                continue
             u = next(((a, b) for a, b in units if a <= m.start() < b), (m.start(), m.end()))
             out.append({"id": e["id"], "flag_type": e["flag_type"], "category": e["category"], "strength": e["strength"],
                         "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": u[0], "unit_end": u[1]})
diff --git a/tests/unit/test_t120_history_source_sentence.py b/tests/unit/test_t120_history_source_sentence.py
new file mode 100644
index 0000000..3021697
--- /dev/null
+++ b/tests/unit/test_t120_history_source_sentence.py
@@ -0,0 +1,47 @@
+"""T-120 (T-060 pass-2 F13): a history-SOURCE sentence ('Hx obtained via patient's son, who interpreted') names who gave the history,
+not a prior condition, so the phrase list does not raise 'Mention of a prior or pre-existing condition' on it. A real prior-condition
+mention still raises the flag, in the same record and in others. Deterministic code guard in lexicon_scan (the lexicon is researcher-owned)."""
+import pathlib
+
+import pytest
+
+from app.backend import flags as FL, ingest as I, lexicon_scan as LS
+
+ROOT = pathlib.Path(__file__).resolve().parents[2]
+SOURCE = ["Hx obtained via patient's son, who interpreted.", "Hx obtained from patient's daughter.", "Hx taken per interpreter.",
+          "History obtained via interpreter.", "History provided by patient's husband.", "hx was obtained through a telephone interpreter.",
+          "H/o obtained via family member.", "Hx per patient's son, who interpreted.", "Hx via interpreter."]
+REAL = ["Hx of lumbar strain.", "Hx: lumbar strain 2019.", "History of migraines.", "Hx neck pain.", "h/o lumbar strain",
+        "Prior history of neck pain 2019, resolved."]
+
+
+def _prior(text):
+    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]
+
+
+@pytest.mark.parametrize("s", SOURCE)
+def test_history_source_sentence_raises_no_prior_condition_hit(s):
+    assert _prior(s) == []
+    assert _prior(s + " Patient states she was struck by a car. Left shoulder pain 7/10.") == []
+
+
+@pytest.mark.parametrize("s", REAL)
+def test_real_prior_condition_mentions_still_hit(s):
+    assert _prior(s)
+
+
+def test_source_sentence_does_not_hide_a_real_prior_condition_next_to_it():
+    t = "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. Left shoulder pain 7/10."
+    hits = _prior(t)
+    assert len(hits) >= 1 and all("lumbar strain" in t[h["unit_start"]:h["unit_end"]] for h in hits)
+    t2 = "Hx obtained via patient's son. Prior neck injury in 2018."
+    assert _prior(t2)
+
+
+def test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do():
+    recs = I.ingest((ROOT / "evals/library/case_lib09_spanish_interpreter_espalda.txt").read_text(encoding="utf-8"))["records"]
+    interp = next(r for r in recs if "Hx obtained via" in r["excerpt"])
+    assert [f for f in FL.lexicon_flags(interp) if f["type"] == "pre_existing"] == []
+    real = dict(interp, excerpt="Hx obtained via patient's son, who interpreted. Prior history of left shoulder dislocation 2019. Pain 7/10.")
+    pre = [f for f in FL.lexicon_flags(real) if f["type"] == "pre_existing"]
+    assert pre and all("Hx obtained via" not in f["excerpt"] for f in pre)
__init__.py
conftest.py
e2e
fixtures
unit
.venv/bin/python
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:56.024Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && $PY -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:18:11.684Z

**tool result**
````
........................................................................ [ 68%]
........................................................................ [ 71%]
........................................................................ [ 74%]
..............................................s......................... [ 76%]
........................................................................ [ 79%]
........................................................................ [ 81%]
........................................................................ [ 84%]
........................................................................ [ 86%]
........................................................................ [ 89%]
........................................................................ [ 91%]
........................................................................ [ 94%]
........................................................................ [ 97%]
........................................................................ [ 99%]
............                                                             [100%]
2816 passed, 4 skipped in 194.08s (0:03:14)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:16.731Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && cat > ../probe120.py <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import lexicon_scan as LS\ncases = [\"Hx per patient: lumbar strain 2019.\", \"History from patient: prior lumbar strain.\", \"Hx obtained via son. Hx of lumbar strain.\",\n \"Hx obtained via patient. Prior back injury.\", \"History per chart: previous neck fracture 2018.\", \"Hx via interpreter: pre-existing disc herniation.\",\n \"Hx obtained via son; h/o lumbar strain 2019.\", \"Hx obtained via patient's son, who interpreted pre-existing arthritis.\",\n \"History provided by patient: chronic neck pain since 2019.\",\"hx obtained from patient, history of migraines\"]\nfor c in cases:\n    print([ (h['id'],h['text']) for h in LS.scan(c) if h['flag_type']=='pre_existing'], '<-', c)\nEOF\n$PY -I ../probe120.py; ls evals; "
}
````

### User / tool · 2026-11-02T11:18:16.949Z

**tool result**
````
[] <- Hx per patient: lumbar strain 2019.
[('prior_injury_or_condition', 'prior lumbar strain')] <- History from patient: prior lumbar strain.
[('hx_abbrev', 'Hx')] <- Hx obtained via son. Hx of lumbar strain.
[('prior_injury_or_condition', 'Prior back injury')] <- Hx obtained via patient. Prior back injury.
[('prior_injury_or_condition', 'previous neck fracture')] <- History per chart: previous neck fracture 2018.
[('pre_existing_literal', 'pre-existing')] <- Hx via interpreter: pre-existing disc herniation.
[('hx_abbrev', 'h/o')] <- Hx obtained via son; h/o lumbar strain 2019.
[('pre_existing_literal', 'pre-existing')] <- Hx obtained via patient's son, who interpreted pre-existing arthritis.
[('chronic', 'chronic'), ('condition_since_year', 'pain since 2019')] <- History provided by patient: chronic neck pain since 2019.
[('history_of', 'history of')] <- hx obtained from patient, history of migraines
__init__.py
adversarial
golden
j3_controls.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:23.488Z

**tool call — Bash**
````
{
 "command": "git show 0c47356 -- app tests/unit/test_t116_gap_endpoints.py; cat tests/unit/test_t123_baseline_same_day_paperwork.py"
}
````

### User / tool · 2026-11-02T11:18:23.602Z

**tool result**
````
commit 0c473563bed3cd6b74ac0db83ee47cb13785fb71
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:33 2026 -0600

    fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/conflicts.py b/app/backend/conflicts.py
index 28bef66..2b9e91f 100644
--- a/app/backend/conflicts.py
+++ b/app/backend/conflicts.py
@@ -59,18 +59,21 @@ def accident_date_conflicts(records: list) -> list:
     else:
         a = later[0]
         category = "accident_date_after_treatment"
-        # D-055 (T-116 r4): never state paperwork as the first treatment. If every record on the earliest date looks like paperwork, the sentence names
-        # that record, says it looks like paperwork, and gives the other reading (the first recorded visit); the paralegal decides.
+        # D-055 (T-116 r4/T-123): never state paperwork as the first treatment. If ANY record on the earliest date looks like paperwork (alone, or
+        # sharing the date with a visit, in either order), the sentence names that record, says it looks like paperwork, and gives the other reading
+        # (the first recorded visit); the paralegal decides.
         extra = {}
-        if all(gaps.admin_label(r) for r in first_recs):
+        paper = [r for r in first_recs if gaps.admin_label(r)]
+        if paper:
             visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
-            extra = {"record_no": first_recs[0]["n"]}
+            extra = {"record_no": paper[0]["n"]}
             if visits:
                 extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
                              alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
+        ordered = paper + [r for r in first_recs if r not in paper]
         title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
-                                            provider_a=first_recs[0].get("source"),
-                                            provider_b=first_recs[1].get("source") if len(first_recs) > 1 else None, **extra)
+                                            provider_a=ordered[0].get("source"),
+                                            provider_b=ordered[1].get("source") if len(ordered) > 1 else None, **extra)
         cited = [a]
     ev = [evidence_span(by_n[s["record_no"]], "excerpt", s["quote"]) for s in cited] + [evidence_span(r, "date") for r in first_recs]
     nos = sorted({s["record_no"] for s in cited} | {r["n"] for r in first_recs})
diff --git a/app/backend/gaps.py b/app/backend/gaps.py
index 5e408cb..547997b 100644
--- a/app/backend/gaps.py
+++ b/app/backend/gaps.py
@@ -18,7 +18,7 @@ THRESHOLD_DAYS = 30
 _NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (
     ("intake form", r"\b(?:(?:new[- ]patient\s+)?(?:intake|registration|admission|admissions|check-?in)\s+(?:form|forms|packet|paperwork|questionnaire|sheet)"
                     r"|new[- ]patient\s+(?:paperwork|forms?|questionnaire|packet)|patient\s+(?:information|history|health\s+history|registration)\s+(?:form|questionnaire|sheet)"
-                    r"|health\s+history\s+(?:form|questionnaire)|pain\s+(?:diagram|questionnaire)|consent\s+form|assignment\s+of\s+benefits)\b"
+                    r"|health\s+history\s+(?:form|questionnaire)|pain\s+(?:diagram|questionnaire)|consent\s+form|assignment\s+of\s+benefits|questionnaires?)\b"
                     r"|\bformulario\s+de\s+(?:admisi[oó]n|ingreso|registro)\b|\bhoja\s+de\s+(?:admisi[oó]n|ingreso)\b"),
     ("explanation of benefits", r"\b(?:explanation\s+of\s+benefits|EOB|remittance(?:\s+advice)?)\b"),
     ("claim form", r"\b(?:UB-?04|CMS-?1500|HCFA|claim\s+form)\b"),
@@ -26,7 +26,7 @@ _NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (
     ("billing statement", r"\b(?:billing|statement\s+of\s+account|account\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|invoice|superbill|balance\s+due)\b|^statement$"
                           r"|\bestado\s+de\s+cuenta\b|\bfactura\b"),
     ("affidavit", r"\b(?:affidavit|custodian\s+of\s+records|records\s+custodian|certification\s+of\s+records|business\s+records|cover\s+(?:page|sheet))\b"),
-    ("records request", r"\b(?:records?\s+request|request\s+for\s+records|records\s+retrieval|authorization\s+form|HIPAA\s+authorization)\b"),
+    ("records request", r"\b(?:records?\s+request|request\s+for\s+records|records\s+retrieval|authorization\s+(?:form|request)|HIPAA\s+authorization)\b"),
     ("records review", r"\b(?:records?|chart|peer|utili[sz]ation)\s+review\b|\bIME\b|\bindependent\s+medical\s+(?:exam|examination|evaluation)\b"),
     ("narrative letter", r"\bnarrative\s+(?:letter|report)\b|\bmedical[- ]legal\s+(?:report|narrative)\b|\bsummary\s+letter\b|\bdemand\s+letter\b"),
     ("letter or correspondence", r"^fax$|\b(?:correspondence|letter(?:\s+of\s+protection)?|LOP|fax\s+cover(?:\s+sheet)?|referral\s+(?:form|letter)|prior\s+authori[sz]ation)\b"),
diff --git a/tests/unit/test_t116_gap_endpoints.py b/tests/unit/test_t116_gap_endpoints.py
index 376cf9a..564aa0b 100644
--- a/tests/unit/test_t116_gap_endpoints.py
+++ b/tests/unit/test_t116_gap_endpoints.py
@@ -200,7 +200,9 @@ def test_accident_date_conflict_has_no_warning_when_a_visit_holds_the_earliest_d
     assert "paperwork" not in c["explanation"]
     recs[0]["source"] = "Capital PT, intake form"
     recs.append(rec(3, "2026-01-12", "Capital PT, new patient visit", excerpt="Exam: ok."))
-    assert "paperwork" not in CF.accident_date_conflicts(recs)[0]["explanation"]
+    # T-123 (T-116 r5 M1): a paperwork record sharing the earliest date with a visit is never named as part of the first recorded treatment
+    e = CF.accident_date_conflicts(recs)[0]["explanation"]
+    assert "first recorded treatment" not in e and "looks like paperwork" in e and "record 3: Capital PT, new patient visit" in e
 
 
 @pytest.fixture
"""T-123 (T-116 r5 M1): the accident baseline never calls a paperwork-headed record part of the 'first recorded treatment' (D-055),
including when paperwork and a visit share the earliest date (either record order) and for bare questionnaire / authorization headers."""
import pytest

from app.backend import conflicts as CF, gaps as G, ingest as I

HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
PAPER_HEADERS = ["Capital PT, intake form", "Capital PT, questionnaire", "Capital PT, authorization request", "Capital PT, pain questionnaire",
                 "Capital PT, prior authorization request", "Capital PT, new patient questionnaire (faxed)"]


def _rec(n, date, src, txt):
    return f"=== Record {n} ===\nDate: {date}\nSource: {src}\nExcerpt: \"{txt}\"\n\n"


def _conflict(items):
    t = HDR + "".join(_rec(i, d, s, e) for i, (d, s, e) in enumerate(items, 1))
    (c,) = CF.accident_date_conflicts(I.ingest(t)["records"])
    return c


PAPER_TXT = "Date of accident: 2026-01-15."
VISIT_TXT = "Cervical range of motion reduced approx. 40%."


@pytest.mark.parametrize("hdr", PAPER_HEADERS)
def test_bare_questionnaire_and_authorization_headers_are_paperwork(hdr):
    rec = I.ingest(HDR + _rec(1, "2026-01-12", hdr, PAPER_TXT))["records"][0]
    assert G.admin_label(rec)


@pytest.mark.parametrize("hdr", PAPER_HEADERS)
def test_paperwork_alone_on_first_date_is_warned(hdr):
    c = _conflict([("2026-01-12", hdr, PAPER_TXT), ("2026-01-20", "Capital PT, initial evaluation", VISIT_TXT)])
    assert "first recorded treatment" not in c["explanation"]
    assert "looks like paperwork" in c["explanation"]


@pytest.mark.parametrize("hdr", PAPER_HEADERS[:3])
@pytest.mark.parametrize("paper_first", [True, False])
def test_same_day_paperwork_and_visit_never_call_the_paperwork_treatment(hdr, paper_first):
    items = [("2026-01-12", hdr, PAPER_TXT), ("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT)]
    c = _conflict(items if paper_first else items[::-1])
    e = c["explanation"]
    assert "first recorded treatment" not in e
    assert "looks like paperwork" in e
    assert "initial evaluation" in e                       # the visit is named as the first recorded visit
    assert c["first_treatment_date"] == "2026-01-12"


def test_visit_only_first_date_keeps_the_plain_wording():
    c = _conflict([("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT + " Date of accident: 2026-01-15.")])
    assert "first recorded treatment" in c["explanation"]


def test_same_day_two_visits_and_no_paperwork_keeps_plain_wording():
    c = _conflict([("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT + " Date of accident: 2026-01-15."),
                   ("2026-01-12", "Capital PT, daily note", VISIT_TXT)])
    assert "first recorded treatment" in c["explanation"]


def test_same_day_alternative_names_the_visit_and_says_not_later():
    c = _conflict([("2026-01-12", "Capital PT, intake form", PAPER_TXT), ("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT)])
    assert "the first recorded visit is January 12, 2026" in c["explanation"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:29.302Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && sed -n 1,16p app/backend/gaps.py; sed -n 32,90p app/backend/gaps.py; grep -rn \"admin_label\" app | grep -v \"def admin_label\""
}
````

### User / tool · 2026-11-02T11:18:29.422Z

**tool result**
````
"""Treatment gaps, computed by code over code-parsed header dates (ADR-010, D-003, R-FL-1, row 9, D-055).
Entry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).
Ambiguous or missing dates are never endpoints.
D-055 (T-116 rounds 3 and 4): the gap math NEVER guesses a record out. EVERY dated record is an endpoint, whatever ingest called it (the ingest
`kind` is a label guess and is not read here). When a paperwork-looking record (intake form, records request, bill or ledger, affidavit, records
review...) starts, ends or splits a gap, the gap carries a visible warning with BOTH numbers: the gap as counted, and the gap if that record is
paperwork, not a visit. A span over 30 days that such a record splits into pieces of 30 days or fewer shows as a conditional flag. The paralegal
decides. A warning cannot invent or hide a gap; an exclusion did, in two review rounds."""
import re

from app.backend import dates, flag_templates, ingest
from app.backend.ingest import evidence_span

THRESHOLD_DAYS = 30

# (label shown to the paralegal, header-label regex), first match wins. A bare "intake" (an intake evaluation or visit) is a treatment
    ("letter or correspondence", r"^fax$|\b(?:correspondence|letter(?:\s+of\s+protection)?|LOP|fax\s+cover(?:\s+sheet)?|referral\s+(?:form|letter)|prior\s+authori[sz]ation)\b"),
    ("phone or message note", r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b"),
)]
# A document that names itself on its first line (an intake form whose Source label only says "new patient"). Anchored: a clinical note that
# merely mentions a form further in does not match.
_TITLE = re.compile(r"^\W*(?:new[- ]patient\s+)?(?:intake|registration|admission)\s+(?:form|packet|questionnaire)\b|^\W*(?:business\s+records\s+)?affidavit\b", re.IGNORECASE)


# Words that name a treatment visit in the record-type head. If one is left in the head after the administrative phrase is removed, the
# record is treated as a visit ("records review visit", "initial evaluation", "progress note"). English and Spanish.
_VISIT_WORD = re.compile(r"\b(?:visits?|evaluations?|evals?|exams?|examinations?|consult\w*|follow-?ups?|progress|sessions?|treatments?|therapy|"
                         r"procedures?|injections?|operative|surgery|imaging|mri|x-?rays?|notes?|soap|daily|new\s+patient|initial|discharge|esi|epidural|"
                         r"visita|consulta|nota|sesi[oó]n|evaluaci[oó]n|terapia|tratamiento|cita)\b", re.IGNORECASE)


def _bare(src: str) -> str:
    """The header label with every parenthetical dropped ("(OCR)", "(faxed)", "(intake form completed same day)")."""
    h = (src or "").strip()
    while True:
        n = re.sub(r"\s*\([^()]*\)", "", h)
        if n == h:
            return h.strip()
        h = n


def admin_label(rec: dict):
    """The plain label of a record whose header looks administrative ("intake form", "billing statement", ...), or None. WARNING ONLY (D-055):
    it never changes a gap. It stays conservative so a warning means something: (1) the administrative type is read from the record-type head
    (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
    outside the provider name (first segment) once that phrase is removed ("records review visit", "Capital PT, daily note, fax" are visits); (3) the record's text is never consulted
    for treatment words (T-116 r5): a bill, EOB, request or form routinely lists diagnoses and services performed, and a warning costs a click while a hidden span
    costs the case. Fail toward warning."""
    bare = _bare(rec.get("source"))
    head = bare.rsplit(",", 1)[-1].strip()
    label, rest = None, ""
    for lab, rx in _NON_VISIT:
        m = rx.search(head)
        if m:
            label, rest = lab, head[:m.start()] + " " + head[m.end():]
            mid = bare[:len(bare) - len(head)].split(",", 1)[1] if "," in bare else ""      # segments after the provider name
            rest = mid + " " + rest
            break
    if not label:
        first = (rec.get("excerpt") or "").lstrip().split("\n", 1)[0][:120]
        if first and _TITLE.search(first):
            label, rest = ("affidavit" if "affidavit" in first.lower() else "intake form"), re.sub(r"new[- ]patient", "", bare.split(",", 1)[-1], flags=re.IGNORECASE)
    if not label:
        k = ingest.record_kind(bare)           # the ingest lexicon, on the label without parentheticals: same families, still a warning only (D-055)
        if k not in ("encounter", "unsplit_text"):
            label = {"billing_statement": "billing statement", "phone_note": "phone or message note"}.get(k, "administrative record")
            rest = bare.split(",", 1)[1] if "," in bare else ""
    if not label or _VISIT_WORD.search(rest):
        return None
    return label


def is_gap(days: int) -> bool:
    return days > THRESHOLD_DAYS

app/backend/conflicts.py:66:        paper = [r for r in first_recs if gaps.admin_label(r)]
app/backend/conflicts.py:68:            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
app/backend/gaps.py:125:    return sorted({r["date_iso"] for r in records if r.get("date_iso") and not admin_label(r)})
app/backend/gaps.py:135:    dropped = sorted((r for r in records if r.get("date_iso") and admin_label(r) and (lo is None or r["date_iso"] > lo) and (hi is None or r["date_iso"] < hi)),
app/backend/gaps.py:139:            "sentence": flag_templates.admin_alternative([(r["n"], r.get("source") or admin_label(r)) for r in dropped], days, lo, hi)}
app/backend/gaps.py:151:        labs = [admin_label(by_n[n]) for n in nos if n in by_n]
app/backend/gaps.py:155:            out.append({"side": side, "record_no": cited, "record_type": admin_label(r) or labs[0], "date": date,
app/backend/gaps.py:156:                        "warning": flag_templates.admin_endpoint_warning(side, cited, r.get("source") or admin_label(r) or labs[0]),
app/backend/gaps.py:180:        a = max(r["n"] for r in records if r.get("date_iso") == lo and not admin_label(r))
app/backend/gaps.py:181:        b = min(r["n"] for r in records if r.get("date_iso") == hi and not admin_label(r))
app/backend/gaps.py:186:        split = flag_templates.admin_split_warning([(r["n"], r.get("source") or admin_label(r), r["date_iso"]) for r in inside], pieces)
app/backend/gaps.py:190:        w = [{"side": "inside", "record_no": r["n"], "record_type": admin_label(r), "date": r["date_iso"], "warning": split,
app/backend/conflict_candidates.py:81:    T-116 is renaming non_visit_label to admin_label; either answers the same question."""
app/backend/conflict_candidates.py:82:    test = getattr(gaps, "admin_label", None) or gaps.non_visit_label
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:33.528Z

**tool call — Bash**
````
{
 "command": "git show c26ff04 -- app memory tests/unit/test_d050_never_verified.py tests/unit/test_spanish_records.py; "
}
````

### User / tool · 2026-11-02T11:18:33.633Z

**tool result**
````
commit c26ff04c64ae77bd0ef7385b843c1702ef759ce2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:11:18 2026 -0600

    feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 7e0f062..81a97a0 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -517,14 +517,16 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
 
     @app.get("/api/cases/{token}/export")
-    def export(token: str):
+    def export(token: str, style: str = None):
         from app.backend import export_routes as XR
+        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
+            raise ApiError(422, "invalid_style", XR.invalid_style_message())
         c = conn()
         try:
             get_case(c, token)
             case = store.export_case(c, token)
             try:
-                ex = XR.export_payload(token, case)
+                ex = XR.export_payload(token, case, style=style)
             except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                 raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
             calls = DB.list_llm_calls(c, token)
diff --git a/app/backend/export.py b/app/backend/export.py
index c7d9445..c8eb83f 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -32,6 +32,10 @@ FLAGGED_HEADING = ("FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it
                    "dismiss the entry to remove it; hedge sentences cannot be removed)")
 
 IN = ("accepted", "edited")
+STYLES = ("standard", "oneline")      # T-121: "standard" (default) is the golden layout; "oneline" gives one line per entry
+# T-121: the translation note is a bracketed, removable phrase at the end of the entry, keyed by the item's translation label (never a line prefix).
+TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
+                    "Translation (edited by reviewer)": "[Translation of the Spanish original, edited by reviewer; check before sending]"}
 NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
 OUT = ("dismissed", "rejected")
 
@@ -159,6 +163,12 @@ class _View:
         head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
         return head + (": " if pg is None else f", p. {pg}: ")
 
+    def oneline_bracket(self, n):
+        """'[Ex. 7 / Bates RIV-0001]' for the one-line style; a PDF page goes inside the bracket: '[Ex. __ / Bates __, p. 3]'."""
+        pg = (self.records.get(n) or {}).get("page")
+        head = SOURCE_PREFIX[len("Source "):-2] if self.export_config is None else self._bracket(n)[len("Source "):]
+        return head if pg is None else head[:-1] + f", p. {pg}]"
+
     def _bracket(self, n):
         """'Source [Ex. 7 / Bates RIV-0001]' from the per-case export config; unset parts stay '__'. Bates = first number + record number - 1, 4 digits."""
         c = self.export_config
@@ -224,20 +234,33 @@ def _status(item):
 
 
 # ---------------------------------------------------------------- letter (takes no flags)
-def build_letter(case: dict) -> str:
+def build_letter(case: dict, style: str = None) -> str:
     """The treatment section. Deliberately has no flags parameter (R-EX-1): flag content cannot reach the letter."""
-    return _letter(_View(case))
+    return _letter(_View(case), style)
+
 
+def _translation_note(e):
+    """D-042/T-121: a translated entry says so in a bracketed phrase at the end of the entry, which the paralegal deletes after checking."""
+    lab = e.get("translation_label")
+    return " " + TRANSLATION_NOTE.get(lab, f"[{lab}; check before sending]") if lab else ""
 
-def _summary_line(e):
-    """D-042: the summary of a Spanish record is a translation; the quote under it is the original Spanish. The letter says which."""
-    return f'{e["translation_label"]}: {e["summary"]}' if e.get("translation_label") else e["summary"]
 
+def _one_line(s):
+    return " ".join(str(s).split())
 
-def _letter(v):
+
+def _letter(v, style=None):
+    if style not in (None, *STYLES):
+        raise ValueError(f"unknown letter style {style!r}")
     out = [LETTER_TITLE, ""]
     for e in v.in_entries:
-        out += [f"{_long_date(v.date_of(e))} — {v.source(e['record_no'])}", _summary_line(e), f'{v.source_prefix(e["record_no"])}"{e["excerpt"]}"', ""]
+        n = e["record_no"]
+        if style == "oneline":
+            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{_translation_note(e)}']
+        else:
+            out += [f"{_long_date(v.date_of(e))} — {v.source(n)}", e["summary"], f'{v.source_prefix(n)}"{e["excerpt"]}"{_translation_note(e)}', ""]
+    if style == "oneline" and v.in_entries:
+        out.append("")
     sents = v.narrative_sentences
     if sents:
         out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
@@ -616,7 +639,7 @@ class JudgeNotRun(ExportBlocked):
     """D-044 alias kept for callers that only care about the judge dimension."""
 
 
-def build_export(case: dict) -> dict:
+def build_export(case: dict, style: str = None) -> dict:
     """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
     Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
     blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
@@ -635,4 +658,4 @@ def build_export(case: dict) -> dict:
         "pending": len(pend),
         "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
     }
-    return {"letter_text": _letter(v), "internal_notes_text": notes, "counts": counts}
+    return {"letter_text": _letter(v, style), "internal_notes_text": notes, "counts": counts}
diff --git a/app/backend/export_routes.py b/app/backend/export_routes.py
index dddcd10..365e6bd 100644
--- a/app/backend/export_routes.py
+++ b/app/backend/export_routes.py
@@ -24,10 +24,10 @@ def _not_found():
     return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})
 
 
-def export_payload(token: str, case: dict, now: datetime = None) -> dict:
+def export_payload(token: str, case: dict, now: datetime = None, style: str = None) -> dict:
     if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
         raise export.ExportBlocked(case["export_blockers"])
-    out = export.build_export(case)
+    out = export.build_export(case, style)
     now = now or datetime.now(timezone.utc)
     ok = ("accepted", "edited")
     return {
@@ -49,6 +49,10 @@ def export_payload(token: str, case: dict, now: datetime = None) -> dict:
     }
 
 
+def invalid_style_message() -> str:
+    return "The letter style must be 'standard' or 'oneline'."
+
+
 def blocked_message(e) -> str:
     if e.code == "judge_not_run":
         return judge_not_run_message(len(e.items))
@@ -60,12 +64,14 @@ def judge_not_run_message(n: int) -> str:
 
 
 @router.get("/api/cases/{token}/export")
-def get_export(token: str):
+def get_export(token: str, style: str = None):
     case = _loader(token) if _loader else None
     if case is None:
         return _not_found()
+    if style not in (None, *export.STYLES):
+        return JSONResponse(status_code=422, content={"error": {"code": "invalid_style", "message": invalid_style_message(), "detail": {}}})
     try:
-        return export_payload(token, case)
+        return export_payload(token, case, style=style)
     except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
         return JSONResponse(status_code=422, content={"error": {"code": e.code, "message": blocked_message(e),
                                                                 "detail": {"blockers": e.items}}})
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 3cb5ce6..d4fbb18 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -370,7 +370,7 @@ Note `item.kind` is the item type (`"amount"`, as in the review response); the a
 
 ## GET /api/cases/{token}/export
 **D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
-Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
+Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
 ```json
 {
   "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
@@ -715,7 +715,7 @@ Languages: English and Spanish. Code detects the language of every record (`app/
 - **Never auto-verified (D-050).** Every item (entry, amount, flag) made from a record routed `es` or `uncertain` is `needs_review` with reason `AI_TRANSLATION` ("AI translation — check against the original"), whatever the Spanish code checks and the translation judge said. Their failures still show in the trace; passing them never yields `verified`. Enforced once, in `confidence.compose_state` (ctx `translated`), and every path that rewrites a state passes it: pipeline, rerun, rejudge, edit and manual entry, date confirmation, reclassify, flags. The entry `translation` block also carries `review_label: "AI translation — check against the original"`. Batch accept refuses such an item (`not_verified`); the paralegal's single accept is the gate and still works, and export needs nothing more than that accept.
 - **Record view** has `language`: `"en"` | `"es"` | `"other"` | `"uncertain"`.
 - **Uncertain language** (`LANGUAGE_UNCERTAIN`). A record with some non-English evidence but no confident answer (a short line with accents and no clear language; Spanish against French or Portuguese on too little text) is neither run as English nor refused. It goes through the translation path (Spanish prompt, Spanish token checks, translation judge), its `translation` block has `source_language: "uncertain"`, `source_language_name: "an unidentified language"`, and the entry is always `needs_review` with reason `LANGUAGE_UNCERTAIN`. The run warning `LANGUAGE_UNCERTAIN` (`record_no`, `message` with the cause) says so. The English token checks never run for it. French, Portuguese, Italian and German lines of any length that reach two or more distinct words in their own language are `other` (refused as `UNSUPPORTED_LANGUAGE`).
-- **Export.** In the letter, a translated entry's summary line starts `AI translation: ` (or `Translation (edited by reviewer): `); the quote line below is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
+- **Export.** In the letter, a translated entry ends with a bracketed, removable note (T-121): `[AI translation of the Spanish original; check before sending]` (or `[Translation of the Spanish original, edited by reviewer; check before sending]`), at the end of its last line; no line starts with `AI translation:`. The quote is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
 - **Warnings** (in `POST /api/cases` and the run result): `SPANISH_RECORDS` (`record_nos`; says that the pre-existing and causation phrase lists are English only, so Spanish records' flags come from the AI check alone) and `UNSUPPORTED_LANGUAGE` (`record_no`; a record in a mixed packet that looks like another language: not sent to any model, no entry, plus a run `errors[]` item with code `UNSUPPORTED_LANGUAGE`, stage `extract`).
 - **Unsupported language, whole case.** If no record is English or Spanish: `POST /api/cases` (and `/pdf`) answers `400 unsupported_language`, `message` "This tool reads English and Spanish records. The text looks like French, which is not supported, so nothing was run. ...", `detail: {languages: ["French"], supported: ["English", "Spanish"]}`; nothing is stored and no model is called. Detected names: French, German, Portuguese, Italian, or a script (Chinese, Japanese, Korean, Cyrillic, Arabic, Hebrew, Devanagari, Thai, Greek).
 - **Dates.** A `Date:` header such as `14 de mayo de 2026`, `14-ago-2026` parses (day first, month spelled out, never ambiguous).
diff --git a/tests/unit/test_d050_never_verified.py b/tests/unit/test_d050_never_verified.py
index 6a5b44b..659630d 100644
--- a/tests/unit/test_d050_never_verified.py
+++ b/tests/unit/test_d050_never_verified.py
@@ -116,7 +116,7 @@ def test_api_batch_accept_refuses_the_translated_item_and_single_accept_is_the_g
     # the paralegal's own accept still works, and the export gate asks for nothing more than it
     assert c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "accept"}).status_code == 200
     ex = c.get(f"/api/cases/{tok}/export")
-    assert ex.status_code == 200 and f"AI translation: {ES_SUMMARY}" in ex.json()["letter_text"]
+    assert ex.status_code == 200 and ES_SUMMARY in ex.json()["letter_text"] and "[AI translation of the Spanish original; check before sending]" in ex.json()["letter_text"]
     after = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == es["id"])
     assert after["review_status"] == "accepted" and after["state"] == "needs_review"        # accepting does not rewrite the machine state
 
diff --git a/tests/unit/test_spanish_records.py b/tests/unit/test_spanish_records.py
index e5012f8..6cd803c 100644
--- a/tests/unit/test_spanish_records.py
+++ b/tests/unit/test_spanish_records.py
@@ -362,7 +362,7 @@ def test_api_spanish_case_end_to_end_label_edit_export(api):
     ex = c.get(f"/api/cases/{tok}/export")
     assert ex.status_code == 200
     letter = ex.json()["letter_text"]
-    assert "Translation (edited by reviewer): Patient reports pain 6/10; denies loss of consciousness." in letter
+    assert "Patient reports pain 6/10; denies loss of consciousness." in letter and "[Translation of the Spanish original, edited by reviewer; check before sending]" in letter and "Translation (edited by reviewer):" not in letter
     assert f'"{ES_QUOTE}"' in letter
     assert "Left shoulder pain 7/10." in letter and "AI translation: Left" not in letter
 
@@ -375,7 +375,7 @@ def test_api_unedited_spanish_entry_carries_the_ai_translation_label_in_the_lett
     es = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if "r2" in e["record_ids"])
     assert c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "accept"}).status_code == 200
     letter = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
-    assert f"AI translation: {ES_SUMMARY}" in letter and f'"{ES_QUOTE}"' in letter
+    assert ES_SUMMARY in letter and "AI translation:" not in letter and f'"{ES_QUOTE}"' in letter and letter.count("[AI translation of the Spanish original; check before sending]") == 1
     # the firm-voice paragraph is English-only: a translated entry is not fed to it
     r = c.post(f"/api/cases/{tok}/narrative")
     assert r.status_code == 400
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:33.802Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_t121_letter_styles.py"
}
````

### User / tool · 2026-11-02T11:18:33.886Z

**tool result**
````
"""T-121 (T-060 pass-2 F9): optional one-line letter style, and the translation note as a bracketed, removable phrase at the end of the entry.
All code (export.py); the default letter for an English case is unchanged and still equals the golden."""
import pytest

from app.backend import export as X
from tests.unit import _golden as G
from tests.unit.test_export import build_case
from tests.unit.test_spanish_records import ES_QUOTE, ES_SUMMARY, MIXED, _wait, api   # noqa: F401  (api is a fixture)

NOTE = "[AI translation of the Spanish original; check before sending]"
NOTE_EDITED = "[Translation of the Spanish original, edited by reviewer; check before sending]"


def _case(label=None, extra=None):
    case = build_case()
    if label:
        e = next(e for e in case["entries"] if e["record_no"] == 1)
        e["translation_label"] = label
        e["summary"] = "Restrained driver rear-ended."
    return case


def test_default_letter_still_equals_the_golden_and_style_standard_is_the_same():
    letter, _ = G.export_blocks()
    case = build_case()
    assert X.build_export(case)["letter_text"] == letter.rstrip("\n")
    assert X.build_export(case, style="standard")["letter_text"] == letter.rstrip("\n")
    assert X.build_export(case, style=None)["letter_text"] == letter.rstrip("\n")


def test_oneline_gives_one_line_per_entry_built_from_the_same_items():
    case = build_case()
    out = X.build_export(case, style="oneline")["letter_text"]
    lines = out.split("\n")
    n_entries = len([e for e in case["entries"] if e["review_status"] == "accepted"])
    entry_lines = [l for l in lines if " — " in l and l.rstrip().endswith("]") and '"' in l]
    assert len(entry_lines) == n_entries
    first = entry_lines[0]
    assert first.startswith('January 9, 2026 — Austin EMS run report: "41M restrained driver, rear-ended at approx. 35 mph.')
    assert first.endswith('Transported to Central ER." [Ex. __ / Bates __]')
    assert "Source [" not in "\n".join(entry_lines)
    assert out.startswith("TREATMENT CHRONOLOGY\n\n")
    assert "Billed charges stated in these records: $8,390.00" in out            # charges section unchanged
    assert out.count("BILLED CHARGES") == 1


def test_oneline_quote_is_still_a_substring_of_the_record_and_has_no_newline():
    case = build_case()
    out = X.build_export(case, style="oneline")["letter_text"]
    for e in case["entries"]:
        assert e["excerpt"] in out


def test_oneline_uses_the_export_config_and_the_pdf_page():
    case = build_case()
    case["export_config"] = {"exhibit": "7", "bates_prefix": "RIV-", "bates_start": 1}
    out = X.build_export(case, style="oneline")["letter_text"]
    assert '" [Ex. 7 / Bates RIV-0001]' in out
    case["export_config"] = None
    case["records"][0]["page"] = 3
    assert '" [Ex. __ / Bates __, p. 3]' in X.build_export(case, style="oneline")["letter_text"]


def test_oneline_is_deterministic_and_leaves_flags_out_of_the_letter():
    case = build_case()
    a = X.build_export(case, style="oneline")
    assert a == X.build_export(case, style="oneline")
    for bad in ("73 days", "Conflict", "REVIEWER NOTE", "INTERNAL"):
        assert bad not in a["letter_text"]


def test_unknown_style_is_refused():
    with pytest.raises(ValueError):
        X.build_export(build_case(), style="fancy")


@pytest.mark.parametrize("label,note", [("AI translation", NOTE), ("Translation (edited by reviewer)", NOTE_EDITED)])
def test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles(label, note):
    case = _case(label)
    std = X.build_export(case)["letter_text"]
    one = X.build_export(case, style="oneline")["letter_text"]
    for out in (std, one):
        assert "AI translation:" not in out and "Translation (edited by reviewer):" not in out
        assert not any(l.startswith(("AI translation", "Translation (edited")) for l in out.split("\n"))
        assert out.count(note) == 1
        line = next(l for l in out.split("\n") if note in l)
        assert line.endswith(note)
    assert "Restrained driver rear-ended.\n" in std                              # the summary line carries no label prefix
    assert next(l for l in std.split("\n") if note in l).startswith("Source [Ex. __ / Bates __]: ")
    assert next(l for l in one.split("\n") if note in l).startswith("January 9, 2026 — Austin EMS run report: ")


def test_english_entries_never_carry_the_note():
    assert "check before sending" not in X.build_export(build_case(), style="oneline")["letter_text"]


def test_api_style_param_and_unknown_style(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    for e in c.get(f"/api/cases/{tok}").json()["entries"]:
        assert c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"}).status_code == 200
    std = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    assert NOTE in std and "AI translation:" not in std and ES_SUMMARY in std
    one = c.get(f"/api/cases/{tok}/export?style=oneline")
    assert one.status_code == 200
    lt = one.json()["letter_text"]
    assert f'"{ES_QUOTE}"' in lt and lt.count(NOTE) == 1 and "Source [" not in lt
    assert c.get(f"/api/cases/{tok}/export?style=standard").json()["letter_text"] == std
    bad = c.get(f"/api/cases/{tok}/export?style=fancy")
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_style"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:45.329Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && grep -rn \"_summary_line\\|AI translation:\\|Translation (edited\" app tests evals/*.py docs 2>/dev/null | grep -v \"^tests/unit/test_t121\" | head -20; grep -rn \"build_letter\\|build_export\" app | grep -v \"def \" | head"
}
````

### User / tool · 2026-11-02T11:18:45.472Z

**tool result**
````
app/llm/prompts/extract_es_v1.md:15:- One short line, in English, that translates only what your excerpt says. Plain clinical wording. It is an AI translation: the software labels it as one.
app/backend/spanish_text.py:17:LABEL_EDITED = "Translation (edited by reviewer)"
app/backend/export.py:38:                    "Translation (edited by reviewer)": "[Translation of the Spanish original, edited by reviewer; check before sending]"}
tests/unit/test_d050_never_verified.py:197:    assert item["translation"]["label"] == "Translation (edited by reviewer)"
tests/unit/test_spanish_records.py:359:    assert ok.json()["item"]["translation"]["label"] == "Translation (edited by reviewer)"
tests/unit/test_spanish_records.py:365:    assert "Patient reports pain 6/10; denies loss of consciousness." in letter and "[Translation of the Spanish original, edited by reviewer; check before sending]" in letter and "Translation (edited by reviewer):" not in letter
tests/unit/test_spanish_records.py:367:    assert "Left shoulder pain 7/10." in letter and "AI translation: Left" not in letter
tests/unit/test_spanish_records.py:378:    assert ES_SUMMARY in letter and "AI translation:" not in letter and f'"{ES_QUOTE}"' in letter and letter.count("[AI translation of the Spanish original; check before sending]") == 1
tests/unit/test_lib09_t110.py:188:def test_statement_summary_lines_and_same_record_figures_never_pair():
app/backend/store.py:37:    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
app/backend/store.py:82:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/trace.py:1050:    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
app/backend/narrative.py:157:    """The small dict export.build_export() reads."""
app/backend/export.py:4:    build_export(case) -> {"letter_text": str, "internal_notes_text": str, "counts": {...}}  (counts: R-EX-5, outside both blocks)
app/backend/export_routes.py:1:"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.
app/backend/export_routes.py:30:    out = export.build_export(case, style)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:51.620Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && cat > ../probe121.py <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import export as X\nfrom tests.unit.test_export import build_case\nc = build_case()\ne = next(e for e in c[\"entries\"] if e[\"record_no\"]==1)\ne[\"translation_label\"]=\"AI translation\"; e[\"summary\"]=\"Restrained driver rear-ended.\"\ne[\"excerpt\"]=\"Conductor con cinturon.\\n  Dolor   lumbar 7/10.\"\nfor r in c[\"records\"]:\n    if r.get(\"n\")==1 or r.get(\"record_no\")==1: r[\"excerpt\"]=e[\"excerpt\"]\nfor s in (\"standard\",\"oneline\"):\n    print(\"----\",s); print(\"\\n\".join(X.build_export(c, style=s)[\"letter_text\"].split(\"\\n\")[:8]))\nprint(repr(e[\"excerpt\"] in X.build_export(c, style=\"oneline\")[\"letter_text\"]))\nEOF\n$PY -I ../probe121.py"
}
````

### User / tool · 2026-11-02T11:18:51.836Z

**tool result**
````
---- standard
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended.
Source [Ex. __ / Bates __]: "Conductor con cinturon.
  Dolor   lumbar 7/10." [AI translation of the Spanish original; check before sending]

January 9, 2026 — Central ER discharge summary
---- oneline
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report: "Conductor con cinturon. Dolor lumbar 7/10." [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]
January 9, 2026 — Central ER discharge summary: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week." [Ex. __ / Bates __]
January 16, 2026 — Dr. Alvarez, primary care: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks." [Ex. __ / Bates __]
January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]
February 20, 2026 — Capital PT, visit 8: "Pain 4/10, improving." [Ex. __ / Bates __]
March 6, 2026 — Capital PT, visit 9: "Discharged from PT after two missed appointments. Pain 3/10." [Ex. __ / Bates __]
False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:57.210Z

**tool call — Bash**
````
{
 "command": "git show 4e294d7 | head -40; grep -n \"D-056\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; ls tests/unit/test_curated_fixtures.py"
}
````

### User / tool · 2026-11-02T11:18:57.359Z

**tool result**
````
commit 4e294d7d137e4b39b07bcf3082411c90c67071ab
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:10:52 2026 -0600

    test(backend): T-125 record the lib09 f_r1_1 J4 answer live (claude-cli); T-120 renumbered the flag so the old key missed
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/fixtures/llm/0a68ecb1704b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a.json b/tests/fixtures/llm/0a68ecb1704b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a.json
new file mode 100644
index 0000000..c0842c4
--- /dev/null
+++ b/tests/fixtures/llm/0a68ecb1704b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a.json
@@ -0,0 +1,11 @@
+{
+ "output": {
+  "reason_code": "NONE",
+  "verdict": "agree"
+ },
+ "recorded_from": {
+  "backend": "claude-cli",
+  "model": "claude-haiku-5-5",
+  "recorded_at": "2026-11-02T11:06:45Z"
+ }
+}
\ No newline at end of file
64:| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
65-| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
tests/unit/test_curated_fixtures.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:19:04.315Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && grep -rn \"recorded_from\" app tools evals/*.py tests/unit/*.py | head -20; ls tests/fixtures/llm | wc -l; F=tests/fixtures/llm; for f in $(ls -t $F | head -3); do echo $f; cat $F/$f | head -12; done"
}
````

### User / tool · 2026-11-02T11:19:04.430Z

**tool result**
````
app/llm/_types.py:32:    recorded_from: dict = field(default_factory=dict)
app/llm/audited.py:101:                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
app/llm/backends/fixture.py:33:                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})
app/llm/backends/fixture.py:42:           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
app/frontend/stepper.js:356:      kv("recorded from", ev.recorded_from && ev.recorded_from.backend), kv("latency", ev.latency_ms != null ? ev.latency_ms + " ms" : null), kv("parsed", ev.parsed_ok == null ? null : ev.parsed_ok ? "yes" : "no"));
app/frontend/audit.js:21:    const rf = c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
app/frontend/mock.js:72:      generator: { model: "claude-sonnet-5-5", prompt_version: "extract_v1", call_id: "c" + id, recorded_from: { backend: "claude-cli", model: "claude-sonnet-5-5", recorded_at: "2026-11-02T00:50:00Z" }, output: { summary: opts.summary, excerpt: ex.text } },
app/backend/trace.py:174:        for k in ("prompt_sha256", "backend", "recorded_from", "latency_ms", "parsed_ok"):
app/backend/present.py:280:    rf = c.get("recorded_from")
app/backend/present.py:281:    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
app/backend/api.py:541:                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
app/db/schema.sql:53:  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
tests/unit/test_curated_fixtures.py:47:    (d / f"{key}.json").write_text(json.dumps({"output": output, "recorded_from": {"backend": "x", "model": "m", "recorded_at": "t"}}))
tests/unit/test_provider_backends.py:132:    assert r.output == {"summary": "ok"} and r.recorded_from["backend"] == "claude-cli"
tests/unit/test_provider_backends.py:144:def test_audit_row_records_backend_and_recorded_from(tmp_path, monkeypatch):
tests/unit/test_provider_backends.py:147:    (tmp_path / f"{P.prompt_hash('m', 's', 'u', SCHEMA)}.json").write_text(json.dumps(dict(output={"summary": "ok"}, recorded_from=dict(backend="claude-cli", model="m", recorded_at="t"))))
tests/unit/test_provider_backends.py:152:    assert json.loads(row["recorded_from_json"] if "recorded_from_json" in row else json.dumps(row["recorded_from"]))["backend"] == "claude-cli"
tests/unit/test_provider.py:18:    (dirp / f"{h}.json").write_text(json.dumps(dict(output=output, recorded_from=dict(backend="claude-cli", model=model, recorded_at="2026-11-02"))))
tests/unit/test_provider.py:51:def test_meta_surfaces_recorded_from(fx):
tests/unit/test_provider.py:52:    """ADR-004 / ADR-003: LLMResult carries backend='fixture' and recorded_from for the audit trail."""
    1095
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
{
 "output": {
  "reason_code": "NONE",
  "verdict": "supported"
 },
 "recorded_from": {
  "backend": "claude-cli",
  "model": "claude-haiku-5-5",
  "recorded_at": "2026-11-02T02:36:40Z"
 }
}003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
{
 "output": {
  "reason_code": "ADDS_CAUSATION",
  "verdict": "partially"
 },
 "recorded_from": {
  "backend": "claude-cli",
  "model": "claude-haiku-5-5",
  "recorded_at": "2026-11-02T02:18:03Z"
 }
}00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
{
 "output": {
  "excerpt": "Pain 5/10, unchanged from visit 1. Continue plan.",
  "summary": "Pain 5/10, unchanged from visit 1; plan to continue."
 },
 "recorded_from": {
  "backend": "claude-cli",
  "model": "claude-sonnet-5-5",
  "recorded_at": "2026-11-02T02:23:59Z"
 }
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:19:10.900Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && sed -n 1,80p tests/unit/test_curated_fixtures.py; sed -n 1,60p app/llm/backends/fixture.py; grep -rn \"fill-missing\\|fill_missing\" --include=*.py . | head"
}
````

### User / tool · 2026-11-02T11:19:11.002Z

**tool result**
````
"""Integrity of the curated fixture set (D-029; T-115 round 2).

Rule: a CURATED answer may stand in for a generator/narrative response (it reproduces the golden letter byte for byte), but a JUDGE answer
(any output with a "verdict") must be a real recorded model answer. So in tests/fixtures/llm/curated/:
  1. no judge file may exist under the same key as a recording in tests/fixtures/llm/ (it would shadow what the model really said; the
     fixture backend reads curated first), and
  2. no judge file may exist without a recorded counterpart,
unless the key is on JUDGE_ALLOW_LIST below with a documented reason. The list is empty on purpose: every judge answer is recorded
(claude-cli, claude-haiku-5-5) and tests/fixtures/make_curated.py writes none. Adding an entry needs a card and a DECISIONS/ASSUMPTIONS note.
"""
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECORDED = ROOT / "tests" / "fixtures" / "llm"
CURATED = RECORDED / "curated"

# key (full sha256) -> reason it may be a curated judge answer with no recorded counterpart. Keep empty.
JUDGE_ALLOW_LIST: dict = {}


def _is_judge(path: pathlib.Path) -> bool:
    out = json.loads(path.read_text()).get("output")
    return isinstance(out, dict) and "verdict" in out


def judge_problems(curated: pathlib.Path, recorded: pathlib.Path, allow: dict) -> list:
    """Human-readable problems for the curated dir: shadowed recordings, and curated judge answers with no recording (not allow-listed)."""
    problems = []
    for p in sorted(curated.glob("*.json")):
        if not _is_judge(p):
            continue
        key = p.stem
        if (recorded / p.name).is_file():
            problems.append(f"SHADOWS_RECORDING {key[:12]}: curated judge answer overrides the recorded model answer")
        elif key not in allow:
            problems.append(f"SCRIPTED_JUDGE {key[:12]}: curated judge answer with no recorded counterpart and not on the allow-list")
    return problems


def _write(d: pathlib.Path, key: str, output: dict):
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{key}.json").write_text(json.dumps({"output": output, "recorded_from": {"backend": "x", "model": "m", "recorded_at": "t"}}))


JUDGE_OUT = {"verdict": "supported", "reason_code": "NONE"}


def test_shipped_curated_set_has_no_shadowing_or_scripted_judge_answers():
    assert CURATED.is_dir() and any(CURATED.glob("*.json"))
    assert judge_problems(CURATED, RECORDED, JUDGE_ALLOW_LIST) == []


def test_allow_list_entries_are_documented_and_still_needed():
    for key, reason in JUDGE_ALLOW_LIST.items():
        assert isinstance(reason, str) and len(reason) >= 20, f"{key[:12]}: the allow-list needs a written reason"
        p = CURATED / f"{key}.json"
        assert p.is_file() and _is_judge(p), f"{key[:12]}: allow-listed key is not a curated judge file; remove it"
        assert not (RECORDED / p.name).is_file(), f"{key[:12]}: now recorded; remove it from the allow-list and the curated file"


def test_detector_fails_when_curated_judge_shadows_a_recording(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(rec, "a" * 64, JUDGE_OUT)
    _write(cur, "a" * 64, {"verdict": "supported", "reason_code": "ADDS_CAUSATION"})
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SHADOWS_RECORDING"]
    assert [p.split()[0] for p in judge_problems(cur, rec, {"a" * 64: "allow-listing must not hide a shadow of a recording"})] == ["SHADOWS_RECORDING"]


def test_detector_fails_on_scripted_judge_without_recording_unless_allow_listed(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(cur, "b" * 64, JUDGE_OUT)
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SCRIPTED_JUDGE"]
    assert judge_problems(cur, rec, {"b" * 64: "documented: no live model available for this prompt"}) == []


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
evals/library_report.py:69:              "(T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call)."]
app/llm/record.py:26:def record_file(path: str, *, run=None, fill_missing: bool = False) -> int:
app/llm/record.py:28:    fill_missing: replay recorded answers and call the live backend only for prompts with no fixture (T-085: new prompts for one record type)."""
app/llm/record.py:49:        if fill_missing:
app/llm/record.py:106:    fill = "--fill-missing" in argv
app/llm/record.py:107:    argv = [a for a in argv if a != "--fill-missing"]
app/llm/record.py:109:        print("usage: python -m app.llm.record [--fill-missing] evals/golden/<case>.txt | --judges", file=sys.stderr)
app/llm/record.py:112:        n = record_file(argv[0], fill_missing=fill)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:19:19.608Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && K=0a68ecb1704b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a; F=tests/fixtures/llm/$K.json; $PY -I - <<EOF\nimport json\nraw=open(\"$F\").read(); d=json.loads(raw)\nprint(json.dumps(d,indent=1,sort_keys=True)==raw)\nEOF\nls tests/fixtures/llm/curated | grep -c $K; mv $F ../$K.bak; $PY -m pytest tests/unit/test_t114_rates_and_demo_judges.py -q -p no:cacheprovider 2>&1 | tail -5; mv ../$K.bak $F; $PY -m pytest tests/unit/test_t114_rates_and_demo_judges.py tests/unit/test_curated_fixtures.py -q -p no:cacheprovider 2>&1 | tail -3; grep -n \"f_r1_1\\|lib09\" tests/unit/test_t114_rates_and_demo_judges.py | head",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:19:37.736Z

**tool result**
````
True
0
------------------------------ Captured log call -------------------------------
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c65a10d113d34 step=j4 attempt=1 prompt_hash=0a68ecb1704b8c9e5647e59946bb8c5a42bbf88d732d3067533730df9420472a
=========================== short test summary info ============================
FAILED tests/unit/test_t114_rates_and_demo_judges.py::test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run[case_lib09_spanish_interpreter_espalda]
1 failed, 19 passed in 8.01s
..........................                                               [100%]
26 passed in 9.45s
15:LIB09 = "case_lib09_spanish_interpreter_espalda"
119:    """lib09 record 4 (an intake form): reading it as 5 March moves the one gap from 42 to 40 days; the response says so, old to new."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:19:48.726Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && sed -n 1,30p evals/run.py | head -40; git -C /Users/arsis/zlayt-pm-project show 1cb8707 --stat | tail -3; ls evals/reports | tail -5"
}
````

### User / tool · 2026-11-02T11:19:48.827Z

**tool result**
````
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
    python -m evals.run --write-calibration
                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm
 app/backend/lexicon_scan.py                     |  6 ++++
 tests/unit/test_t120_history_source_sentence.py | 47 +++++++++++++++++++++++++
 2 files changed, 53 insertions(+)
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:19:54.807Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && ($PY -m evals.run 2>&1 | tail -15); $PY -m evals.run --check-spec 2>&1 | tail -3; $PY -m app.pipeline evals/golden/sample.txt > ../o1.txt 2>&1; $PY -m app.pipeline evals/golden/sample.txt > ../o2.txt 2>&1; cmp ../o1.txt ../o2.txt && echo deterministic; wc -c ../o1.txt; head -c 300 ../o1.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:19:57.100Z

**tool result**
````
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a/evals/reports/20261102T111956Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}
deterministic
    3884 ../o1.txt
Status: done   backend: fixture   records: 9   entries: 9   flags: 10   amounts: 3

TIMELINE
  January 9, 2026 - Austin EMS run report [verified]
      41-year-old male restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache, alert and oriented, transported to Centr
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:14.210Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && cat > ../mut.py <<'EOF'\nimport subprocess, sys, shutil, pathlib\nPY=\"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nmuts = [\n (\"T120 M1 drop guard\", \"app/backend/lexicon_scan.py\", 'if e[\"flag_type\"] == \"pre_existing\" and _HISTORY_WORD.match(m.group(0)) and _HISTORY_SOURCE.match(text, m.end()):', 'if False:', \"tests/unit/test_t120_history_source_sentence.py\"),\n (\"T120 M2 guard skips every Hx hit\", \"app/backend/lexicon_scan.py\", 'and _HISTORY_SOURCE.match(text, m.end()):', 'and True:', \"tests/unit/test_t120_history_source_sentence.py\"),\n (\"T120 M3 guard on any pre_existing source word\", \"app/backend/lexicon_scan.py\", '(?:per|via)\\\\s)\", re.I)', '(?:per|via)\\\\s|:)\", re.I)', \"tests/unit/test_t120_history_source_sentence.py\"),\n (\"T123 M1 all() not any\", \"app/backend/conflicts.py\", \"        if paper:\\n\", \"        if paper and len(paper) == len(first_recs):\\n\", \"tests/unit/test_t123_baseline_same_day_paperwork.py\"),\n (\"T123 M2 no bare questionnaire\", \"app/backend/gaps.py\", \"|assignment\\\\s+of\\\\s+benefits|questionnaires?)\\\\b\", \"|assignment\\\\s+of\\\\s+benefits)\\\\b\", \"tests/unit/test_t123_baseline_same_day_paperwork.py\"),\n (\"T123 M3 no authorization request\", \"app/backend/gaps.py\", \"authorization\\\\s+(?:form|request)\", \"authorization\\\\s+form\", \"tests/unit/test_t123_baseline_same_day_paperwork.py\"),\n (\"T123 M4 ordered=first_recs\", \"app/backend/conflicts.py\", \"ordered = paper + [r for r in first_recs if r not in paper]\", \"ordered = list(first_recs)\", \"tests/unit/test_t123_baseline_same_day_paperwork.py\"),\n (\"T123 M5 alt visit dropped\", \"app/backend/conflicts.py\", \"if visits:\\n                extra.update\", \"if False:\\n                extra.update\", \"tests/unit/test_t123_baseline_same_day_paperwork.py\"),\n (\"T121 M1 no note\", \"app/backend/export.py\", 'return \" \" + TRANSLATION_NOTE.get(lab, f\"[{lab}; check before sending]\") if lab else \"\"', 'return \"\"', \"tests/unit/test_t121_letter_styles.py\"),\n (\"T121 M2 one_line noop\", \"app/backend/export.py\", 'return \" \".join(str(s).split())', 'return str(s)', \"tests/unit/test_t121_letter_styles.py\"),\n (\"T121 M3 oneline drops page\", \"app/backend/export.py\", 'return head if pg is None else head[:-1] + f\", p. {pg}]\"', 'return head', \"tests/unit/test_t121_letter_styles.py\"),\n (\"T121 M4 style ignored\", \"app/backend/export.py\", '\"letter_text\": _letter(v, style)', '\"letter_text\": _letter(v, None)', \"tests/unit/test_t121_letter_styles.py\"),\n (\"T121 M5 api no validation (api.py)\", \"app/backend/api.py\", 'if style not in (None, *export_mod.STYLES):', 'if False:', \"tests/unit/test_t121_letter_styles.py\"),\n (\"T121 M6 note-in-oneline dropped\", \"app/backend/export.py\", '{v.oneline_bracket(n)}{_translation_note(e)}', '{v.oneline_bracket(n)}', \"tests/unit/test_t121_letter_styles.py\"),\n]\nfor name,f,a,b,t in muts:\n    p=pathlib.Path(f); orig=p.read_text()\n    if a not in orig: print(\"NOAPPLY\",name); continue\n    p.write_text(orig.replace(a,b,1))\n    r=subprocess.run([PY,\"-m\",\"pytest\",t,\"-q\",\"-x\",\"-p\",\"no:cacheprovider\"],capture_output=True,text=True)\n    p.write_text(orig)\n    print(name, \"->\", \"KILLED\" if r.returncode else \"SURVIVED\", r.stdout.strip().splitlines()[-1][:100])\nEOF\n$PY -I ../mut.py",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:20:21.658Z

**tool result**
````
T120 M1 drop guard -> KILLED 1 failed in 0.23s
T120 M2 guard skips every Hx hit -> KILLED 1 failed, 9 passed in 0.22s
T120 M3 guard on any pre_existing source word -> SURVIVED 17 passed in 0.28s
T123 M1 all() not any -> KILLED 1 failed, 12 passed in 0.11s
T123 M2 no bare questionnaire -> KILLED 1 failed, 1 passed in 0.12s
T123 M3 no authorization request -> KILLED 1 failed, 2 passed in 0.12s
T123 M4 ordered=first_recs -> SURVIVED 21 passed in 0.11s
T123 M5 alt visit dropped -> KILLED 1 failed, 12 passed in 0.13s
T121 M1 no note -> KILLED 1 failed, 6 passed in 0.36s
T121 M2 one_line noop -> SURVIVED 10 passed in 0.73s
T121 M3 oneline drops page -> KILLED 1 failed, 3 passed in 0.40s
T121 M4 style ignored -> KILLED 1 failed, 1 passed in 0.35s
T121 M5 api no validation (api.py) -> KILLED 1 failed, 9 passed in 0.78s
T121 M6 note-in-oneline dropped -> KILLED 1 failed, 6 passed in 0.35s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:39.328Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r1/a && grep -rlE \"Hx (obtained|taken|per)|History (obtained|provided)|[Hh]x per|via interpreter\" evals tests/fixtures/*.txt tests/e2e app/frontend 2>/dev/null | head; git -C /Users/arsis/zlayt-pm-project show 1cb8707:app/backend/lexicon_scan.py >/dev/null && echo ok; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; $PY -I - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import lexicon_scan as LS\nfor t in [\"PMH per patient: diabetes since 2015.\",\"Hx per chart review: lumbar strain 2019, resolved.\",\"History per patient: left knee surgery in 2017.\",\"Hx per patient of lumbar strain\"]:\n    print([h['text'] for h in LS.scan(t)], t)\nEOF"
}
````

### User / tool · 2026-11-02T11:20:39.554Z

**tool result**
````
evals/library_build_v2.py
evals/adversarial/speaker_attribution.jsonl
evals/library/case_lib09_spanish_interpreter_espalda.txt
ok
[] PMH per patient: diabetes since 2015.
['2019, resolved'] Hx per chart review: lumbar strain 2019, resolved.
['surgery in 2017'] History per patient: left knee surgery in 2017.
[] Hx per patient of lumbar strain
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:49.170Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/lexicon_scan.py | grep -n \"_HISTORY_SOURCE\\|_HISTORY_WORD\" ; git show HEAD:app/backend/export.py | grep -n \"def _one_line\\|def _translation_note\\|oneline\\|_one_line(\" ; git show HEAD:app/backend/conflicts.py | grep -n \"ordered\" ; ls reviews | grep -E \"T-12[0135]\"; git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T11:20:49.339Z

**tool result**
````
14:_HISTORY_WORD = re.compile(r"(?:hx|h/o|phx|history)\Z", re.I)
15:_HISTORY_SOURCE = re.compile(r"\s+(?:(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+(?:via|from|by|through|per|with)\b|(?:per|via)\s)", re.I)
136:            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _HISTORY_SOURCE.match(text, m.end()):
35:STYLES = ("standard", "oneline")      # T-121: "standard" (default) is the golden layout; "oneline" gives one line per entry
166:    def oneline_bracket(self, n):
242:def _translation_note(e):
248:def _one_line(s):
258:        if style == "oneline":
259:            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{_translation_note(e)}']
262:    if style == "oneline" and v.in_entries:
73:        ordered = paper + [r for r in first_recs if r not in paper]
75:                                            provider_a=ordered[0].get("source"),
76:                                            provider_b=ordered[1].get("source") if len(ordered) > 1 else None, **extra)
6d0177472fb85c0775f9869027c2fd6e54209a70
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:52.512Z

**tool call — Bash**
````
{
 "command": "git diff --stat c26ff04 HEAD -- app/backend/lexicon_scan.py app/backend/export.py app/backend/conflicts.py app/backend/gaps.py tests/fixtures/llm | tail -3; git log --oneline c26ff04..HEAD"
}
````

### User / tool · 2026-11-02T11:20:52.625Z

**tool result**
````
6d01774 feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:53.696Z

Neither new commit touches the files in scope, so the c26ff04 archive results stand. Writing the four reviews.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:04.350Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-staff-engineer.md",
 "content": "# T-120 staff-engineer review (commit 1cb8707, archive of c26ff04)\n\nVerdict: changes. The guard works for the cases it lists, but the `per`/`via` branch is unconditional and silently drops a flag on a real prior-condition mention.\n\nExercised (all on a `git archive` copy of c26ff04, run with the project venv):\n- `pytest tests/unit -q`: 2816 passed, 4 skipped.\n- `python -m evals.run` on the fixture backend: runs; `--check-spec` gives spec_matches_golden true. The fixture run reports ship_bar_met=False on the usual live-only items.\n- `python -m app.pipeline evals/golden/sample.txt` twice: byte-identical output.\n- Probe script calling `lexicon_scan.scan` on 10 phrasings (below).\n- Mutants against tests/unit/test_t120_history_source_sentence.py: removing the guard is killed, and widening it to every Hx hit is killed. My third mutant (adding `|:`) was inert, because the `\\s+` prefix blocks it. It proves nothing and is not counted.\n- Read the diff in full. There is no LLM call, no float, no network and no clock. The guard is code only, in lexicon_scan.\n\n```json\n{\"card\": \"T-120\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive c26ff04 (T-120 commit 1cb8707): app/backend/lexicon_scan.py, tests/unit/test_t120_history_source_sentence.py; no app URL; sample case plus lib09\",\n \"exercised\": [\"pytest tests/unit -q on archive: 2816 passed, 4 skipped\", \"python -m evals.run (fixture) and --check-spec: spec_matches_golden true\", \"python -m app.pipeline evals/golden/sample.txt twice: identical\", \"probe of lexicon_scan.scan on 10 Hx/History phrasings\", \"mutants: drop guard (killed), guard hits every Hx (killed)\", \"read git show 1cb8707 in full\"],\n \"verdict\": \"changes\",\n \"scores\": {\"correctness\": 3, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The `Hx per ...` branch drops the flag on real prior-condition mentions\",\n   \"evidence\": \"app/backend/lexicon_scan.py:15 `(?:per|via)\\\\s` is unconditional, and :136 skips the hit. Probe with `.venv/bin/python -I` on the archive: scan('Hx per patient: lumbar strain 2019.') -> [] ; scan('Hx per patient of lumbar strain') -> [] ; scan('PMH per patient: diabetes since 2015.') -> []. 'Hx per patient: ...' is ordinary note phrasing. tests/unit/test_t120_history_source_sentence.py REAL list has no 'per' case, so the suite is green.\",\n   \"why_it_matters\": \"The skip is meant for sentences that name who gave the history. 'Hx per patient: lumbar strain 2019' names the source and a prior condition together, and the whole condition mention disappears. That is a lost recall flag with no trace, on a defense-relevant item (R-FL pre_existing).\",\n   \"fix\": \"Narrow the `per`/`via` branch so it skips only when the source phrase ends the clause or is followed by an interpreter/family-member noun and no condition text (or only skip the `Hx` token and let the remaining clause scan run). Do not skip when a colon, 'of', a year or a condition word follows the source.\",\n   \"acceptance_test\": \"Add to REAL: 'Hx per patient: lumbar strain 2019.', 'Hx per patient of lumbar strain', 'History per patient: left knee surgery in 2017.' and assert a pre_existing hit; keep every SOURCE case green. Mutant widening `(?:per|via)\\\\s` to any following text must fail.\"}\n ],\n \"whats_right\": [\"Guard is deterministic code in lexicon_scan; lexicon.yaml untouched; evals fixture flag P/R unchanged.\", \"The sentence-adjacent test proves a real prior mention next to a source sentence still hits.\", \"Removing or broadening the guard fails the new tests.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:21:04.502Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-120-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:18.260Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-121-staff-engineer.md",
 "content": "# T-121 staff-engineer review (commit c26ff04)\n\nVerdict: changes. The style option is built by code, the default letter still equals the golden, and the API rejects bad styles. The one-line style has two defects: it prints a \"translation\" note over a letter line with no translation in it, and it rewrites the quote's whitespace without a test that would notice.\n\nExercised (archive of c26ff04, project venv):\n- `pytest tests/unit -q`: 2816 passed, 4 skipped. This includes the golden byte-equal test and the updated Spanish and D-050 tests.\n- `python -m evals.run --check-spec`: letter_equal true, internal_notes_equal true.\n- A probe script (scratch) building the letter with a Spanish-labelled entry that has a multi-line excerpt, in both styles.\n- Six mutants against tests/unit/test_t121_letter_styles.py: dropping the note, ignoring the style, dropping the PDF page, removing the API check and dropping the note from one-line are all killed. A no-op `_one_line` survives.\n- Read the diff in full (export.py, export_routes.py, api.py, api.md). There is no LLM call, no float and no network. Both routes validate the style before building.\n\n```json\n{\"card\": \"T-121\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive c26ff04: app/backend/export.py, export_routes.py, api.py, memory/contracts/api.md, tests/unit/test_t121_letter_styles.py, test_spanish_records.py, test_d050_never_verified.py\",\n \"exercised\": [\"pytest tests/unit -q on archive: 2816 passed, 4 skipped\", \"python -m evals.run --check-spec: letter_equal true\", \"probe: Spanish-labelled entry with multi-line excerpt, standard vs oneline\", \"6 mutants on test_t121_letter_styles.py: 5 killed, 1 survived (_one_line no-op)\", \"read git show c26ff04 in full\"],\n \"verdict\": \"changes\",\n \"scores\": {\"correctness\": 3, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"One-line style prints an 'AI translation' note on a line that has no translation\",\n   \"evidence\": \"app/backend/export.py:259 the oneline branch emits only the date, provider, quote and bracket, plus `_translation_note(e)`; the summary (the English translation, or the reviewer's edited translation) is never printed. Probe output: `January 9, 2026 — Austin EMS run report: \\\"Conductor con cinturon. Dolor lumbar 7/10.\\\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]`. The standard style prints the translation on the line above the quote. tests/unit/test_t121_letter_styles.py::test_api_style_param_and_unknown_style only asserts the note count and that ES_QUOTE is present, not that any translation is.\",\n   \"why_it_matters\": \"The note tells the paralegal an AI translation is here to check. In this style there is nothing to check, and the reviewer's edited translation (Translation (edited by reviewer)) is lost from the letter. A Spanish quote may reach the demand letter with a note about a translation that was never written.\",\n   \"fix\": \"For a translated entry in the one-line style, either append the translation inside the line (for example after the quote, before the bracketed note) or reword the note to say the quote is untranslated. Do not claim a translation that is not on the line.\",\n   \"acceptance_test\": \"Add a test: a Spanish-labelled entry in style=oneline must contain its summary text on the same line as the note (or the reworded note), for both labels AI translation and Translation (edited by reviewer). Mutant dropping the summary from that line must fail.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"One-line style collapses whitespace inside the quote, so it is no longer a verbatim substring; the test cannot see it\",\n   \"evidence\": \"export.py:248-250 `_one_line` and :259 `_one_line(e[\\\"excerpt\\\"])`. Probe: excerpt 'Conductor con cinturon.\\\\n  Dolor   lumbar 7/10.' gives `excerpt in oneline_letter` False, while the standard style keeps it verbatim. Mutant `_one_line` -> `str(s)` SURVIVED all 10 tests in test_t121_letter_styles.py, because the sample excerpts are single-line (test_oneline_quote_is_still_a_substring_of_the_record_and_has_no_newline is therefore vacuous for its 'no newline' half).\",\n   \"why_it_matters\": \"The letter's quote is the product's grounded text. Whitespace-only normalization is acceptable if it is documented, but here it is undocumented and unpinned, so a later change could silently change quotes.\",\n   \"fix\": \"Document the normalization (whitespace only) in the docstring and api.md, and add a multi-line-excerpt test that asserts the collapsed form equals the whitespace-normalized excerpt and contains no newline.\",\n   \"acceptance_test\": \"Test with excerpt 'a\\\\n  b' asserts the one-line letter contains '\\\"a b\\\"' and no other newline inside the entry line; the no-op mutant must fail.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Style validation is duplicated in two routes\",\n   \"evidence\": \"app/backend/api.py:520-523 and app/backend/export_routes.py:71 both check the style and build the 422.\",\n   \"why_it_matters\": \"Two copies of the same check will drift; only one route answers at a time.\",\n   \"fix\": \"Keep one route and call a shared helper.\",\n   \"acceptance_test\": \"Optional: a test that both routes return the same body for ?style=fancy.\"}\n ],\n \"whats_right\": [\"Default and style=standard letters stay byte-equal to evals/golden; build_export stays a pure function of accepted items.\", \"Invalid style fails fast with 422 invalid_style and a ValueError in the pure builder, no silent fallback.\", \"The bracketed note is keyed to the translation label and tested to end the entry in both styles.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:21:18.414Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-121-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:25.950Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-123-staff-engineer.md",
 "content": "# T-123 staff-engineer review (commit 0c47356)\n\nVerdict: pass. The baseline sentence now uses the warn wording whenever any record on the earliest date is paperwork, in either order, and the bare questionnaire and authorization request headers count as paperwork. The change is code only and warning-only; it cannot add or hide a gap.\n\nExercised (archive of c26ff04, project venv):\n- `pytest tests/unit -q`: 2816 passed, 4 skipped, which includes tests/unit/test_t123_baseline_same_day_paperwork.py and test_t116_gap_endpoints.py.\n- Five mutants against test_t123: `any` changed to `all`, removing bare `questionnaires?`, removing `authorization request`, and dropping the alternative-visit extra are all killed. Replacing the paperwork-first provider ordering survives (see the minor finding).\n- Read the diff in full. `admin_label` reads the header only, with a visit-word guard, and is used for warnings only. There is no LLM call and no float. The older test that asserted no warning was changed to the new reading, with a comment citing T-116 r5.\n\n```json\n{\"card\": \"T-123\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive c26ff04: app/backend/conflicts.py, app/backend/gaps.py, tests/unit/test_t123_baseline_same_day_paperwork.py, tests/unit/test_t116_gap_endpoints.py\",\n \"exercised\": [\"pytest tests/unit -q on archive: 2816 passed, 4 skipped\", \"5 mutants on test_t123: 4 killed, 1 survived (provider ordering)\", \"read git show 0c47356 in full\", \"read gaps.admin_label and its callers\"],\n \"verdict\": \"pass\",\n \"scores\": {\"correctness\": 4, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Provider ordering in the same-day sentence is untested\",\n   \"evidence\": \"app/backend/conflicts.py:73-76 `ordered = paper + [...]` feeds provider_a/provider_b. Mutant `ordered = list(first_recs)` SURVIVED all 21 tests in test_t123_baseline_same_day_paperwork.py. The tests assert the absence of 'first recorded treatment', the presence of 'looks like paperwork' and 'initial evaluation', but not which provider is named as the paperwork.\",\n   \"why_it_matters\": \"The reorder exists so the paperwork record is named as paperwork when it is second in file order; nothing fails if it regresses.\",\n   \"fix\": \"In test_same_day_paperwork_and_visit_never_call_the_paperwork_treatment, also assert the paperwork header appears in the sentence in both orders and is the one named with 'looks like paperwork'.\",\n   \"acceptance_test\": \"The ordered=first_recs mutant must fail the paper_first=False case.\"}\n ],\n \"whats_right\": [\"Warning-only: gap math and endpoints are untouched, so the fix cannot invent or hide a gap (D-055).\", \"Tests cover both record orders and six header spellings, including the faxed and parenthetical forms.\", \"The old test was updated to the new reading with a comment, not deleted.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:21:26.184Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-123-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:33.078Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-125-staff-engineer.md",
 "content": "# T-125 staff-engineer review (commit 4e294d7)\n\nVerdict: pass. The commit adds one fixture file and no code. The fixture is needed, it matches the key the test asks for, and it sits in the recorded set, not the curated set, so D-056 is not breached.\n\nProvenance (D-056), checked on the archive of c26ff04:\n- The file is `tests/fixtures/llm/0a68ecb1....json` (key prefix 0a68ecb1; full name in the commit). The same path listed in tests/fixtures/llm/curated: 0 matches. Nothing shadows a recording.\n- Its bytes equal `json.dumps(d, indent=1, sort_keys=True)` of its own content, which is what `app/llm/backends/fixture.py:write` produces, so the shape matches the recorder.\n- `recorded_from` is claude-cli, claude-haiku-5-5, 2026-11-02T11:06:45Z, the same shape as its neighbours. The recorded time is a few seconds before the board claim (11:06:51Z), which is consistent with work starting before the claim.\n- I cannot prove from the file that a live call happened; no tool can. The format, the key match and the absence of a curated copy are what can be checked, and all hold.\n- Control: with the file moved aside, `test_t114_rates_and_demo_judges.py` fails 1 of 20 (the lib09 walk) with `llm call failed ... step=j4 ... prompt_hash=0a68ecb1...`. With it back, 26 passed (t114 plus tests/unit/test_curated_fixtures.py).\n- Full unit suite on the archive: 2816 passed, 4 skipped.\n\n```json\n{\"card\": \"T-125\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive c26ff04: tests/fixtures/llm/<0a68ecb1...>.json (commit 4e294d7), tests/unit/test_t114_rates_and_demo_judges.py, tests/unit/test_curated_fixtures.py\",\n \"exercised\": [\"pytest tests/unit -q on archive: 2816 passed, 4 skipped\", \"pytest test_t114_rates_and_demo_judges.py + test_curated_fixtures.py: 26 passed\", \"control: fixture moved aside -> t114 lib09 walk fails with J4 prompt_hash 0a68ecb1\", \"byte-compare of the fixture with the recorder's json.dumps(indent=1, sort_keys=True) output: equal\", \"ls tests/fixtures/llm/curated for the key: absent\", \"read fixture.py write() and test_curated_fixtures.py\"],\n \"verdict\": \"pass\",\n \"scores\": {\"correctness\": 5, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 4},\n \"findings\": [],\n \"whats_right\": [\"The fixture is a recorded answer in tests/fixtures/llm, not a curated judge file, and test_curated_fixtures.py passes with an empty allow-list.\", \"Cause is stated precisely (T-120 renumbered the flag, the J4 prompt carries the item id) and no prompt changed.\", \"Only the one missing key was added, so no recorded answer was overwritten.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:21:33.223Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-125-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:36.979Z

**tool call — Bash**
````
{
 "command": "for t in 120 121 123 125; do python3 tools/board.py validate reviews/T-$t-staff-engineer.md 2>&1 | tail -2; done"
}
````

### User / tool · 2026-11-02T11:21:37.238Z

**tool result**
````
ok (1 file(s))
ok (1 file(s))
ok (1 file(s))
ok (1 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:41.547Z

T-120 and T-121 are `changes` (one major each). T-123 and T-125 are `pass`. The four files in `/Users/arsis/zlayt-pm-project/reviews/` (`T-120-staff-engineer.md` to `T-125-staff-engineer.md`) pass `board.py validate`.
- **Test runs:** on a `git archive` copy of c26ff04, the unit suite gave 2816 passed and 4 skipped. `test_curated_fixtures.py` passes, and the sample CLI output is identical across two runs.
- **T-120:** the `Hx per ...` branch drops the flag unconditionally (`app/backend/lexicon_scan.py:15`, `:136`). `scan('Hx per patient: lumbar strain 2019.')` returns `[]`, a lost prior-condition flag. No test covers it.
- **T-121:** the one-line style prints "[AI translation of the Spanish original…]" on a line that has no translation (`export.py:259`). Minor: it collapses quote whitespace, and a no-op mutant of that step survives all its tests.
- **T-123 and T-125:** T-123 has one minor: the provider-ordering mutant survives. For T-125, the fixture file's bytes are exactly what the recorder writes, it is not in `curated/`, and removing it fails `test_t114_rates_and_demo_judges.py`. I can't prove a live call from the file alone, so D-056 is checked by format, key match and the empty allow-list.
