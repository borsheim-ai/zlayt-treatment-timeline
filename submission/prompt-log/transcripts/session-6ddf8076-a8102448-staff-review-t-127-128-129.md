# Subagent: Staff review T-127/128/129 (Staff review T-127/128/129)

Source: `agent-a810244862421a0b5.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:38:01.631Z

You are the staff-engineer reviewer in /Users/arsis/zlayt-pm-project for three cards. Read each with `python3 tools/board.py show T-###`, plus the reviews it links.

- **T-128 (3d53ca5), summary_trim.** It must never leave a fragment; the source findings are in reviews/T-112-staff-engineer-r3.md. Probe at least 20 fresh fragment-prone summaries. Confirm that unsupported clauses still trim when no fragment would remain, and that the mutant-killing tests are real.
- **T-129 (3a74f75), ingest.** A preamble must not become record 1. D-027 says nothing is dropped. Check record numbering stability: are citations elsewhere keyed by sequence, and do existing fixtures, golden sets or evals shift?
- **T-127 (93de5f2), gap_change persisted.** Check that it is stored through review events and exposed on GET case. Check the contract in memory/contracts/api.md. Check the undo and re-confirm paths, and that the result is deterministic.

On a `git archive HEAD` copy in your scratchpad, run the unit suite and mutate the code to test the tests.

Write reviews/T-128-staff-engineer.md, reviews/T-129-staff-engineer.md and reviews/T-127-staff-engineer.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Stop only your own PIDs. Reply in 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:02.950Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:38:02.960Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:03.660Z

**tool call — Bash**
````
{
 "command": "for t in T-128 T-129 T-127; do python3 tools/board.py show $t; echo =====; done; git log --oneline | head -8"
}
````

### User / tool · 2026-11-02T11:38:03.908Z

**tool result**
````
---
id: "T-128"
title: "Summary trim: never leave a fragment (Back. / Due to torn meniscus. / Including a sling.) and kill T-112 r3 surviving mutants"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:24:58Z"
updated_at: "2026-11-02T11:37:56Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:26:18Z"
rounds: 0
commits: ["3d53ca5"]
reviews: []
ac:
  - {"n": 1, "text": "the 5 fragments from reviews/T-112-staff-engineer-r3.md are not produced (trim skipped, whole summary goes to judge); tests kill the us/im case, label body-part vouch and quote-negation mutants and each abbreviation-table entry deletion", "done": true, "evidence": "tests/unit/test_summary_trim.py: 7 fragment probes stay whole; 3 injected mutants (us/im case, label body vouch, quote negation) each fail the suite; per-entry deletion test for tha/acdf/lle/rle/bue/rue/lue/u/s/UE; full unit 3056 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:26:09Z orchestrator: assigned: backend
- 2026-11-02T11:26:18Z backend: claimed
- 2026-11-02T11:37:46Z backend: AC 1 checked: tests/unit/test_summary_trim.py: 7 fragment probes stay whole; 3 injected mutants (us/im case, label body vouch, quote negation) each fail the suite; per-entry deletion test for tha/acdf/lle/rle/bue/rue/lue/u/s/UE; full unit 3056 passed
- 2026-11-02T11:37:46Z backend: moved in_progress -> in_review
- 2026-11-02T11:37:56Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: summary_trim.trim skips the trim (whole summary to judge) when a kept clause follows a removed ' with ' clause, opens with a connector (due/which/including/was...) after a removed clause or at the start, or the kept text is one bare body part. Verified: test_summary_trim.py 259 pass; injected the 3 mutants (each fails); per-entry deletion tests; full unit 3056 pass. Left: no live eval (no prompt/model change; judge and generator prompts untouched). Surprised: a blanket one-word rule broke 'Pain.', so it is limited to body parts.

=====
---
id: "T-129"
title: "Ingest: a non-library preamble counts as a phantom record 1"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:25:56Z"
updated_at: "2026-11-02T11:37:56Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:26:18Z"
rounds: 0
commits: ["3a74f75"]
reviews: []
ac:
  - {"n": 1, "text": "a pasted preamble with no record header/date is not counted as a record (or is shown as a preamble, not a record); unit test; reviews/T-123-paralegal.md minor", "done": true, "evidence": "tests/unit/test_ingest.py::test_a_preamble_does_not_shift_the_record_numbers (3 preambles x 2 separators): real records stay r1,r2; preamble kept (D-027) as unsplit preamble:true, numbered last"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:26:09Z orchestrator: assigned: backend
- 2026-11-02T11:26:18Z backend: claimed
- 2026-11-02T11:37:46Z backend: AC 1 checked: tests/unit/test_ingest.py::test_a_preamble_does_not_shift_the_record_numbers (3 preambles x 2 separators): real records stay r1,r2; preamble kept (D-027) as unsplit preamble:true, numbered last
- 2026-11-02T11:37:46Z backend: moved in_progress -> in_review
- 2026-11-02T11:37:56Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: ingest numbers unsplit text (preamble, between-record notes) after the real records; text above the first real record has preamble:true. Nothing dropped (D-027). Verified: 6 new tests in test_ingest.py; full unit 3056 pass. Left: frontend may label preamble records. Surprised: without --- separators the first block starts at 0, so preamble is judged by where the block's fields begin.

=====
---
id: "T-127"
title: "Keep the gap-change record on the gap flag: GET case returns gap_change {old_days,new_days,old_from,old_to,new_from,new_to,record_seq,sentence} on a gap flag whose figures moved after a confirm_date (T-114 r3)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "frontend"
created_at: "2026-11-02T11:14:29Z"
updated_at: "2026-11-02T11:37:56Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:32:58Z"
rounds: 0
commits: ["93de5f2"]
reviews: []
ac:
  - {"n": 1, "text": "A gap flag whose figures changed in confirm_date carries gap_change (same shape as gap_changes[] plus record_seq) in GET /cases/{token}, until that gap changes again; a gap that was removed is listed in the case as gap_changes_removed[] with its sentence; contract updated; unit test", "done": true, "evidence": "tests/unit/test_t127_gap_change_kept.py (4 tests): gap_change on the flag in GET case, survives a new app on the same DB file, dropped when figures move; gap_changes_removed[]; api.md updated"}
---
## Description
From T-060 r4 / T-114 r2 paralegal major. The UI now keeps the change per case in the browser (localStorage zlayt.gapchg.<token>) so it survives Got it and a reload, but it is lost on another browser or after clearing site data. app/frontend/timeline.js (gapChangeFor) already prefers flag.gap_change when present, so the backend field switches it over with no further UI work; the browser copy can then be dropped.

## Notes (append-only, newest last)
- 2026-11-02T11:31:09Z orchestrator: assigned: backend
- 2026-11-02T11:32:58Z backend: claimed
- 2026-11-02T11:37:46Z backend: AC 1 checked: tests/unit/test_t127_gap_change_kept.py (4 tests): gap_change on the flag in GET case, survives a new app on the same DB file, dropped when figures move; gap_changes_removed[]; api.md updated
- 2026-11-02T11:37:46Z backend: moved in_progress -> in_review
- 2026-11-02T11:37:56Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: confirm_date stores gap_changes (with record_seq, sentence) in its review event; present adds gap_change per gap flag and top-level gap_changes_removed[] to GET case; api.md updated. No schema change (derived from review_events, so db role untouched). Verified: test_t127_gap_change_kept.py 4 pass; full unit 3056 pass. Left: frontend can drop the localStorage copy.

=====
93de5f2 feat(backend): T-127 keep gap_change on the gap flag, gap_changes_removed in GET case
3a74f75 fix(backend): T-129 a preamble no longer shifts record numbers
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
433ac1c test(backend): T-123 pin which record is named as paperwork in either order (kills the provider-ordering mutant)
aa6ae9f feat(backend): T-105 added-qualifier word lists (attribution, hedge, approximation, inability) come from lexicon.yaml code_lists.added_qualifier; curly apostrophes, Spanish-helper negations, faithful paraphrases; lexicon text updated to D-055
4c59fac fix(backend): T-121 r2 one-line style carries the translated summary, whitespace-only quote collapse documented and tested, translation note on its own line
07dbd2b fix(backend): T-120 r2 history-source skip only when the sentence names no condition (colon, year, 'of' keep the flag); per/via only before a person or channel
1a0106b docs(orchestrator): T-112 accepted-debt row (§7.4 after round 3)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:04.050Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t112_trim_patterns.md"
}
````

### User / tool · 2026-11-02T11:38:04.057Z

**tool result**
````
1	---
2	name: project_t112_trim_patterns
3	description: T-112 r1 (afcde06) and r2 (1b93582) changes - over-trim of faithful paraphrases (stems, then abbreviations), not_duplicate tray, doc/D-054 left on old rule, unpinned counter
4	metadata:
5	  type: project
6	---
7	
8	T-112 r1 verdict changes (2 major, 5 minor/nit). Patterns worth re-checking on similar "code trims/filters model output" cards:
9	- Stem/synonym matchers: probe 20+ faithful pairs with y/i morphology (dizzy/dizziness) and splitter-on-"with" fragments ("Patient ambulating with a cane" -> "A cane."). Card tests chose pairs that pass.
10	- A new failure code wired in pipeline.py only: grep every extract_one caller (review.not_duplicate keeps no tray item, message says "AI could not draft").
11	- Placeholder trace: trace.py `verbatim_fail` recomputes from empty excerpt, so tray items claim "not word for word".
12	- Eval reports did not count trim firings; clean runs alone are weak evidence (3 clean 3-runs ~0.3 by luck at 1-in-3 flap).
13	- git archive of the card sha can be red from another card (T-102 calibration_route) while HEAD is green; run both.
14	- Reviews are write-once: a miscount in the prose (said 50 probes, was 55; 4 tray vs 6) could not be edited. Proof-read prose counts against the probe output before Write.
15	
16	**Why:** [[feedback_review_write_once]] applies; counts were typed from memory instead of the probe output.
17	**How to apply:** tally probe outputs with a script and paste the numbers.
18	
19	**r2 (1b93582, changes: 2 major, 3 minor):** r1 probes 0/20 hard pairs over-trimmed, but a fresh 40-pair abbreviation set (lac, DJD, ESI, BLE, IM, US, c-collar) over-trimmed 9, 8 to the tray; _GROUPS not consulted for family hits; _fragment checks only leading stopwords ('Sutures.' survives). Binding texts (LLM_VS_CODE row 4, D-054) still named the old rule. Counter mutant (always 0) survived whole suite; handoff test counts (126, 2758) did not reproduce (106, 2755).
20	- Method that worked: re-run last round's probe scripts unchanged on a git-archive, then write a fresh corpus; mutate each fix (label arg, counter, trace) and run the full suite for survivors.
21	- Reviewer sandbox: Write to scratchpad is blocked by reviewer-write-guard and `cp` to a scratch path is blocked by board-guard; use python in Bash to write scratch files, and json-validate the review by writing it once to reviews/ then parsing.
22	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:04.725Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md"
}
````

### User / tool · 2026-11-02T11:38:04.733Z

**tool result**
````
1	---
2	name: feedback_shared_scratchpad
3	description: the scratchpad path is shared with other agents; use a unique card-round subdir, verify archive copies with diff -rq against a fresh git archive, never background a setup chain you depend on
4	metadata:
5	  type: feedback
6	---
7	
8	Name scratch directories with the card and round (for example `T108_verify`), and run `ls -la` before reusing any directory. Check an archive copy with `diff -rq` against a fresh `git archive <sha>` before trusting results.
9	
10	**Why:** during T-108 r1 the `probe/` folder I used already held another agent's repo archive, and sibling folders (`T106_*`) appeared in the same scratchpad during my run. My own setup line `mkdir -p X && cp ... && cd ... &` was backgrounded as one chain, so the following commands ran before the directory existed and wrote nothing.
11	
12	**How to apply:** do not background setup you depend on; run it in the foreground or wait on it. Keep probe scripts in your own unique directory and copy the final ones to `artifacts/review-evidence/<card>/` as the evidence.
13	
14	Related: [[project_t108_quote_units_patterns]].
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:06.420Z

**tool call — Bash**
````
{
 "command": "git status --short | head; git log -1 --format=%H; git show --stat 3d53ca5 3a74f75 93de5f2 | cat; ls reviews | grep T-112"
}
````

### User / tool · 2026-11-02T11:38:06.592Z

**tool result**
````
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
93de5f2e47a18f3eeff9edf8e6bc7b34fbb02dfb
commit 3d53ca53bd4541b1a916729723678cc322d46e7b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:37:36 2026 -0600

    feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/summary_trim.py     | 28 ++++++++++++--
 tests/unit/test_summary_trim.py | 86 +++++++++++++++++++++++++++++++++++++++++
 2 files changed, 111 insertions(+), 3 deletions(-)

commit 3a74f75caafbfa9d7484bf67bc0d8fdfe53467b7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:37:38 2026 -0600

    fix(backend): T-129 a preamble no longer shifts record numbers
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/ingest.py     | 12 ++++++++++--
 tests/unit/test_ingest.py | 28 ++++++++++++++++++++++++++++
 2 files changed, 38 insertions(+), 2 deletions(-)

commit 93de5f2e47a18f3eeff9edf8e6bc7b34fbb02dfb
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:37:39 2026 -0600

    feat(backend): T-127 keep gap_change on the gap flag, gap_changes_removed in GET case
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/present.py                  | 43 ++++++++++++++++++++-
 app/backend/review.py                   |  7 ++--
 memory/contracts/api.md                 |  4 +-
 tests/unit/test_t127_gap_change_kept.py | 66 +++++++++++++++++++++++++++++++++
 4 files changed, 113 insertions(+), 7 deletions(-)
T-112-staff-engineer-r2.md
T-112-staff-engineer-r3.md
T-112-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:09.454Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la $S; mkdir -p $S/T128_9_127_r1/repo && git archive 93de5f2 | tar -x -C $S/T128_9_127_r1/repo && ls $S/T128_9_127_r1/repo | head -30; git diff 3d53ca5~1 3d53ca5 -- app | cat"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:09.843Z

**tool call — Bash**
````
{
 "command": "sed -n 1,400p reviews/T-112-staff-engineer-r3.md | head -150"
}
````

### User / tool · 2026-11-02T11:38:10.412Z

**tool result**
````
<outside-repo file omitted>
````

### User / tool · 2026-11-02T11:38:10.495Z

**tool result**
````
# T-112 review, round 3 - staff-engineer-reviewer

Card: D-054 summary trimming. Commit under review 63e18ed (T-112 r3). HEAD at review time is c559ce2; `git diff --stat 63e18ed HEAD -- app/backend/summary_trim.py docs/LLM_VS_CODE.md` is empty, and `grep -c "not yet committed" docs/LLM_VS_CODE.md` on HEAD prints 1. I worked on `git archive HEAD` in my scratchpad (`T112_r3`, taken when HEAD was 63e18ed; the working tree carries other agents' uncommitted edits, so I did not use it). I re-ran my r2 probes unchanged, wrote a fresh corpus (`probe5.py`: 43 faithful pairs, 30 unsupported clauses; `probe6.py`: 24 fragment-shape probes), and mutated the code against `tests/unit/test_summary_trim.py`.

**Verdict: changes.** Three majors, no blocker. The r2 abbreviation set, the negation wording and the counter are fixed. The same defect classes are still open: a fresh set over-trims 12 of 43 faithful pairs, the fragment guard still covers only article/preposition starts and a lone noun after ` with `, and the graded doc row 4 still states the old rule and "not yet committed".

## 1. r2 probes, unchanged
- `probe4.py` (r2 fresh set): over-trimmed **0 of 40** (r2: 9); unsupported 28 of 28 trimmed.
- `probe2.py`: 0 of 20 over-trimmed. `probe3.py`: 4 of 4 invented clauses on a shared-word quote trimmed.
- `probe.py`: 4 of 30 differ from my r1 expectations. Two are the known narrowing ('seen at urgent care', 'permanent disability' stay, r2 minor 5). Two are 'Cast applied' over 'splint applied' and 'Wrist cast applied' over 'Wrist X-ray negative': a cast is not a splint, so the trim is right and my r1 label was wrong. 'Sutured laceration on forehead' over 'Forehead lac repaired...' now survives (r2: trimmed).
- `tests/unit/test_summary_trim.py` in the archive: 223 passed (matches the handoff). Full `tests/unit` in the archive: 2933 passed, 4 skipped, 0 failed (handoff: 2934 passed, 2 failed, working tree).

## 2. Fresh set (probe5.py)
- **Faithful pairs: 12 of 43 over-trimmed, all 12 to the tray (empty text).** 31 survived. Abbreviation misses: 'Low back pain.' over 'LBP x 2 weeks.'; 'Discharged home.' over 'D/C home.'; 'Neck sprain.' over 'C-spine sprain.'; 'Lower back strain.' over 'LS strain.'; 'Lumbar puncture performed.' over 'LP done.'; 'Hip replacement surgery.' over 'THR.'; 'Uses a wheelchair.' over 'W/C bound.'. Word-family misses: 'Flu shot given.' over 'Influenza vaccine administered.'; 'Knee surgery scheduled.' over 'Surgery planned for knee.' ('planned' is not in the plan family); 'Sore throat.' over 'Pharyngitis.'; 'Stomach ache.' over 'GI upset.'; 'Chest wall bruising.' over 'Seatbelt sign across chest.'. The last four are synonym leaps a judge could argue about; the first eight are plain abbreviation or word-form misses. 'LBP' is in `_GROUPS` (summary_trim.py:53) and still does not support 'back': the family check never consults `_GROUPS`.
- **Unsupported clauses: 21 of 30 trimmed, 9 kept.** Kept: 'carpal tunnel diagnosed', 'patient was intoxicated', 'amputation', 'blood clot', 'cannot work', 'plaster applied', 'metformin', 'seen at urgent care', 'permanent impairment'. All are outside the family lists; judge 1 still sees them. Five are procedure/drug/diagnosis terms in D-054's own wording.
- **Recorded outputs:** `sweep.py` over 188 recorded generator outputs fires on 7: five Spanish (excluded in production by `is_translated`) and two English. With the record's source label ('Tumblebrook Imaging, shoulder MRI'; 'Larchmont Ridge Imaging, right shoulder MRI', taken from evals/golden/case_08 and evals/library/case_lib06) both English cases stay whole. So on recorded real output the trim has no over-trim; my fresh corpus is synthetic.

## 3. Fragment rule
Kept and working: `Laceration repaired with sutures.` over `Sutures placed.` stays whole; over `Laceration.` it becomes `Laceration repaired.`; `Back pain; diagnosed with diabetes.` removes `diagnosed with diabetes` as one clause.
Not covered (24 probes, `probe6.py`): 5 clear fragments, 2 borderline.
- `Pain in the neck and back.` over `Back pain.` -> `Back.`; `Pain in the neck and shoulder.` over `Shoulder pain.` -> `Shoulder.` (the lone-noun rule at summary_trim.py:423-425 fires only for ` with `, not ` and `).
- `Knee surgery recommended, due to torn meniscus.` -> `Due to torn meniscus.`; `MRI ordered, which showed a torn meniscus.` -> `Which showed a torn meniscus.`; `Cast applied, including a sling.` -> `Including a sling.` (`_LEAD` at :279 has articles and prepositions only).
- Borderline: `Wrist splint with ice packs.` -> `Ice packs.`; `Splint applied and was advised to rest.` -> `Was advised to rest.`
D-054 (memory/ORCHESTRATOR_DECISIONS.md:62) says "whole clauses only, never leaving a fragment"; the code guards three lexical shapes.

## 4. The worker's deviations vs the docs
- **Negation contract narrowed: confirmed.** `grounding.new_tokens('No cervical strain.', 'X-ray: no acute fracture. Cervical strain.')` returns `[]` and `trim(...)['changed']` is False. The summary_trim.py docstring (lines 16-19) and memory/contracts/api.md:725 say exactly that: guaranteed to reach judge 1 and the human only. r2 minor 4 is closed.
- **`_GROUPS` support fallback skipped.** The worker's reason is sound for the general case (a group member such as 'injection' would vouch for 'steroid'). The cost is visible: LBP (and any other group-only abbreviation) over-trims. A fallback limited to abbreviation members, or table entries for the missing abbreviations, avoids the cost. Finding 1.
- **Docs do not match the code.** D-054 was amended (db7f6d0) and api.md describes the committed rule. `docs/LLM_VS_CODE.md:32` row 4 still reads "T-112, in progress: `app/backend/summary_trim.py`, not yet committed): a summary clause whose content words no word of its excerpt supports is removed". Finding 3.
- **Trims-fired counter now pinned (r2 minor 3 closed).** Mutant `clauses_removed: 0` in evals/run.py -> `test_the_eval_report_counts_what_code_trimmed` fails.

## 5. Mutation of the tests (test_summary_trim.py, 223 tests)
Behaviour mutants, 16: 13 killed (abbreviation expansion off, C-collar rule off, extremity rule off, lone-noun rule off, participle merge off, article guard off, label modality off, capitalized-name rule off, a-c always count, d-f never count, covered_by ignored, empty-left check off, lone-noun rule widened to ` and `), 3 survived:
- US/IM matching made case-insensitive (the handoff's "Surprised" point): 'Neck pain; ultrasound performed.' over 'Neck pain; he told us it hurts.' is trimmed by the code and kept by the mutant; 'Back pain; injection given.' over 'Back pain. Im in pain.' likewise.
- Label vouching for body parts removed: 'Neck pain.' over 'MRI findings.' with label 'Valley Imaging, cervical spine MRI' is kept by the code and trimmed by the mutant.
- Quote negation-like words ignored (docstring rule c): 'Wrist pain; denies numbness.' over 'Wrist pain. X-ray unremarkable.' is kept by the code and trimmed by the mutant.
Table sweep: deleting one of the 30 `_ABBR`/`_ABBR_CASE` entries at a time left 11 survivors (tha, orif, acdf, lle, bue, rue, hep, ekg, u/s, UE, IV). I confirmed a behaviour change for 7 (tha, acdf, lle, bue, rue, u/s, UE); hep, ekg and IV have no family effect as far as I can see, and my orif pair was not faithful in the full code either, so I do not count those four.

## Not checked
AC 2 (live 3-runs from a clean tree at the final commit): open, as the handoff says; no live report exists for the r2/r3 rule. Pipeline-level behaviour of the fragments in section 3 (judge 1 and accept on `Shoulder.`): not run. Frontend rendering of the `summary_trim` step.

```json
{"card": "T-112", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of HEAD (63e18ed content for all files in scope; HEAD c559ce2 has no diff in scope) in scratchpad T112_r3; app/backend/summary_trim.py, generator.py:62-81, evals/run.py:410-417, tests/unit/test_summary_trim.py, docs/LLM_VS_CODE.md row 4, memory/ORCHESTRATOR_DECISIONS.md D-054, memory/contracts/api.md:724-726; fake/no backend, no network",
 "exercised": [
  "python3 tools/board.py show T-112; read reviews/T-112-staff-engineer-r2.md, D-054 in memory/ORCHESTRATOR_DECISIONS.md, app/backend/summary_trim.py in full",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_summary_trim.py in the archive: 223 passed",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit in the archive: 2933 passed, 4 skipped, 0 failed (180 s)",
  "r2 probes unchanged: probe.py (30 pairs, 4 differ), probe2.py (0/20 over-trimmed), probe3.py (4/4 trimmed), probe4.py (0/40 over-trimmed, 28/28 unsupported trimmed)",
  "probe5.py fresh: 43 faithful pairs (12 over-trimmed), 30 unsupported clauses (21 trimmed, 9 kept)",
  "probe6.py: label rescue of the 2 recorded English trims; 24 fragment-shape probes (5 clear fragments, 2 borderline)",
  "sweep.py over 188 recorded outputs in tests/fixtures/llm: fires on 7 (5 Spanish, 2 English kept whole once the record label is passed)",
  "grounding.new_tokens and summary_trim.trim on the negation-flip example",
  "mut.py: 16 behaviour mutants and a one-at-a-time deletion of 30 abbreviation-table entries against test_summary_trim.py; direct behaviour checks for the 3 surviving behaviour mutants and 7 table survivors; evals/run.py counter mutant (killed)",
  "grep of docs/LLM_VS_CODE.md for 'not yet committed' and D-054 / row 4 text; memory/contracts/api.md:725; git log --oneline for docs and decisions files"
 ],
 "verdict": "changes",
 "scores": {"deterministic_trim_is_code": 5, "unsupported_removal_precision": 4, "faithful_paraphrase_survival": 3, "fragment_safety": 2, "trace_visibility": 5, "empty_to_tray_all_paths": 5, "human_summaries_untouched": 5, "judge_sees_trimmed": 5, "test_strength": 3, "doc_matches_code": 2},
 "findings": [
  {"severity": "major",
   "title": "A fresh faithful set is still over-trimmed (12 of 43, all to the tray): common abbreviations and word forms outside the tables; _GROUPS is not consulted",
   "evidence": "`.venv/bin/python -I probe5.py <archive>`: 'Low back pain.' | 'LBP x 2 weeks.' -> ''; 'Discharged home.' | 'D/C home.' -> ''; 'Neck sprain.' | 'C-spine sprain.' -> ''; 'Lower back strain.' | 'LS strain.' -> ''; 'Lumbar puncture performed.' | 'LP done.' -> ''; 'Hip replacement surgery.' | 'THR.' -> ''; 'Uses a wheelchair.' | 'W/C bound.' -> ''; 'Flu shot given.' | 'Influenza vaccine administered.' -> ''; 'Knee surgery scheduled.' | 'Surgery planned for knee.' -> ''; 'Sore throat.' | 'Pharyngitis.' -> ''; 'Stomach ache.' | 'GI upset.' -> ''; 'Chest wall bruising.' | 'Seatbelt sign across chest.' -> ''. summary_trim.py:53 puts 'lbp' with low/back/pain in _GROUPS, but new_salient (:348-351) tests only `quote['fams']`, so the group never helps a family hit. The plan family (:222) has 'schedul' and no 'plan'. handoff: 'the _GROUPS-based support fallback from the review was NOT added'. r2 probe4 (40 pairs) now passes 0/40; the new set has the same rate (12/43) that r2 had (9/40).",
   "why_it_matters": "'Faithful paraphrases survive' is the card's bar (AC 1, D-054). A closed vocabulary moves the failure to the next abbreviation the model expands: each miss sends a correct entry to the could-not-verify tray and lowers entry_recall. Nothing is invented and the human gate follows, so this is not a blocker; and 188 recorded outputs show no English over-trim once the label is passed, so the live rate is probably lower than my synthetic one. The worker's reason for skipping the fallback is valid for general words ('injection' would vouch for 'steroid'), but then the abbreviations need entries, and the test lists were written from my previous round's failures, so they pass by construction.",
   "fix": "(1) Add LBP, D/C, C-spine/CSP, LS, LP, THR, W/C, vaccine~shot, planned~plan, pharyngitis~throat, GI~abdomen to the expansion table or families. (2) Let a hit word be supported when it, or an abbreviation whose _GROUPS entry contains it, appears in the quote (apply the group only to abbreviation keys, not to ordinary words). (3) Replace the hand-picked FAITHFUL list with pairs drawn from recorded generator outputs and the golden/library packets, so that new failures come from data and not from reviewer rounds.",
   "acceptance_test": "tests/unit/test_summary_trim.py: the 12 pairs above return changed False; a parametrized sweep over tests/fixtures/llm English outputs, passing the record label, asserts trim fires only on pairs listed as unsupported."},
  {"severity": "major",
   "title": "The fragment guard covers three lexical shapes; D-054 says 'never leaving a fragment' and 5 clear fragments still reach judge 1 and the paralegal",
   "evidence": "summary_trim.py:279 (`_LEAD`: articles and prepositions), :379-381 (`_fragment`), :423-425 (lone noun only when the removed clause was joined by ' with '). `.venv/bin/python -I probe6.py <archive>`: 'Pain in the neck and back.' | 'Back pain.' -> 'Back.'; 'Pain in the neck and shoulder.' | 'Shoulder pain.' -> 'Shoulder.'; 'Knee surgery recommended, due to torn meniscus.' | 'Torn meniscus.' -> 'Due to torn meniscus.'; 'MRI ordered, which showed a torn meniscus.' | 'Torn meniscus.' -> 'Which showed a torn meniscus.'; 'Cast applied, including a sling.' | 'Sling provided.' -> 'Including a sling.'; borderline: 'Wrist splint with ice packs.' -> 'Ice packs.'; 'Splint applied and was advised to rest.' -> 'Was advised to rest.'. memory/ORCHESTRATOR_DECISIONS.md:62 (D-054): 'whole clauses only, never leaving a fragment'.",
   "why_it_matters": "This is the r2 finding-1 sub-point (noun-led fragments); the fix handled ' with ' and the 'diagnosed' participle only. 'Shoulder.' over 'Shoulder pain.' loses the fact that it is pain and is a summary the paralegal would put in a letter after one accept click; judge 1 sees a clause the quote supports word for word. D-054 promises more than the guard does. Not a blocker: no fact is invented, the quote stays and the removal is shown in the trace; I rate it major because the binding decision says 'never' and r2 already named the class.",
   "fix": "Replace the lexical test with a structural one: when a removal leaves a kept clause with no verb or no content word besides one noun, or whose first word is not a content word (due, which, including, because, since, following, causing, resulting, secondary), keep the whole summary and let judge 1 see it (as the code already does for articles). Extend the lone-noun rule to ' and ' joins. Or soften D-054 to say which shapes are guarded.",
   "acceptance_test": "Parametrized unit test: the five clear fragments above (and the two borderline) return changed False; 'Pain in the neck and back.' over 'Neck pain.' still becomes 'Pain in the neck.'."},
  {"severity": "major",
   "title": "docs/LLM_VS_CODE.md row 4 (graded) still says the code is uncommitted and states the old trimming rule; D-054 text overclaims 'never leaving a fragment'",
   "evidence": "docs/LLM_VS_CODE.md:32: \"Before Rung 2, code trims the summary (D-054; T-112, in progress: `app/backend/summary_trim.py`, not yet committed): a summary clause whose content words no word of its excerpt supports is removed\". `grep -c \"not yet committed\" docs/LLM_VS_CODE.md` -> 1 at HEAD c559ce2. `git log --oneline -3 -- docs/LLM_VS_CODE.md memory/ORCHESTRATOR_DECISIONS.md` shows db7f6d0 (D-054 amended) but no change to the doc. The committed rule removes a clause only for salient new content: 'Back pain, seen at urgent care.' over 'Back pain 7/10.' stays; so do 'permanent impairment' and 'cannot work' (probe5). memory/contracts/api.md:725 and the module docstring are accurate (negation, ' with ' fragment, abbreviations).",
   "why_it_matters": "Checklist item 1: the implementation must match LLM_VS_CODE.md row by row, and the doc is graded. This was r2 finding 2; D-054 was fixed, the doc the architect owns was not. The row's rule would predict removal of clauses that now reach judge 1.",
   "fix": "Architect: rewrite row 4's trim sentence to the committed rule (salient procedure/device/drug, body part, diagnosis by word family; number, side, negation only when no content word is shared; abbreviations expanded; clauses outside those families, such as visit setting and prognosis, reach judge 1 untouched), drop 'in progress ... not yet committed'. Orchestrator: change 'never leaving a fragment' in D-054 to the shapes the guard covers, or keep it and fix finding 2.",
   "acceptance_test": "grep -n 'not yet committed' docs/LLM_VS_CODE.md returns nothing; row 4 contains 'salient' and 'D-034'; D-054 and the fragment tests agree."},
  {"severity": "minor",
   "title": "Tests do not pin the case-sensitive US/IM guard, the label's body-part vouch, quote negation words, or 7 abbreviation entries",
   "evidence": "mut.py against tests/unit/test_summary_trim.py (223 tests): mutant 'US/IM case-insensitive' -> 223 passed; mutant 'label body vouch off' -> 223 passed; mutant 'quote negation words ignored' -> 223 passed. Deleting `tha`, `acdf`, `lle`, `bue`, `rue`, `u/s` or `UE` from the tables -> 223 passed each, and each deletion changes a trim result (e.g. 'Hip replacement surgery.' | 'THA.' is untouched with the entry and trimmed without it). Behaviour: 'Neck pain; ultrasound performed.' | 'Neck pain; he told us it hurts.' -> code trims, mutant keeps; 'Wrist pain; denies numbness.' | 'Wrist pain. X-ray unremarkable.' -> code keeps, mutant trims.",
   "why_it_matters": "The handoff says 'US' and 'IM' match upper case only because they collide with ordinary words; nothing fails if that is lost, and a lower-case 'us' would then vouch for an unsupported 'ultrasound' clause (under-trim). The other survivors are rules the docstring states.",
   "fix": "Add: a lower-case 'us'/'im' quote does not support 'ultrasound'/'injection'; a label naming 'cervical' supports a 'neck pain' clause over a quote without a body word; 'denies numbness' stays over 'X-ray unremarkable'; one faithful pair per table entry (tha, acdf, lle, bue, rue, u/s, UE).",
   "acceptance_test": "The three behaviour mutants and the seven deletions each fail at least one test."},
  {"severity": "minor",
   "title": "Unsupported clauses outside the family lists (clinical and non-clinical) reach judge 1 untrimmed: 9 of 30 in the fresh set; AC 2 evidence for the r2/r3 rule is still missing",
   "evidence": "probe5.py KEPT-UNSUPPORTED: 'Wrist pain; carpal tunnel diagnosed.', 'Neck pain; patient was intoxicated.', 'Hand pain; amputation.', 'Leg pain; blood clot.', 'Elbow pain; cannot work.', 'Ankle pain; plaster applied.', 'Hip pain; metformin.', 'Neck pain; seen at urgent care.', 'Knee pain; permanent impairment.'. Board AC 2 `done: false`, evidence null; handoff: 'AC 2 ... left to the orchestrator'. No live report exists at 63e18ed.",
   "why_it_matters": "I would have done it differently, not a spec violation: the amended D-054 names 'salient' content by family and sends the rest to judge 1, which is the stated design. The converse of finding 1: a closed list also misses new invented clauses. The ship-bar flap that opened D-054 is a judge-1 flap, so the live runs are what show whether the narrower rule holds.",
   "fix": "Add a visit-setting / prognosis / work-status family and the missing procedure, drug and diagnosis names only if the next three clean-tree live 3-runs show a case_02 unsupported item; attach the report paths and a non-zero trims row.",
   "acceptance_test": "Three consecutive live 3-runs at the final commit with unsupported_count_3run 0 and a trims row for case_02, or the families added with unit tests."}
 ],
 "whats_right": [
  "The r2 failure set is gone and the negation contract is honest: summary_trim.py docstring lines 16-19 and api.md:725 say a same-token negation reaches judge 1 and the human only, and grounding.new_tokens confirms it.",
  "Trimming is still pure code (no model or network import), whole clauses only, original model output kept in ladder.generator.output; the trims-fired counter mutant now fails test_the_eval_report_counts_what_code_trimmed.",
  "Recorded real output is not over-trimmed: of 188 recorded generator outputs only 2 English ones trim without a label, and both stay whole when the record's source label is passed."
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:12.522Z

**tool call — Bash**
````
{
 "command": "git diff 3d53ca5~1 3d53ca5 | cat; ls /private/tmp/claude-501/*/*/scratchpad/ 2>/dev/null | head -0; ls -d /private/tmp/claude-501/*/*/scratchpad 2>/dev/null"
}
````

### User / tool · 2026-11-02T11:38:12.756Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:17.026Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_127_r1/repo; ls $R | head -20; ls $R/.venv 2>&1 | head -2; ls /Users/arsis/zlayt-pm-project/.venv/bin/python; cd /Users/arsis/zlayt-pm-project && git diff 3a74f75~1 3a74f75 | cat"
}
````

### User / tool · 2026-11-02T11:38:17.146Z

**tool result**
````
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
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo/.venv: No such file or directory
/Users/arsis/zlayt-pm-project/.venv/bin/python
diff --git a/app/backend/ingest.py b/app/backend/ingest.py
index 0bfb90b..efca1fa 100644
--- a/app/backend/ingest.py
+++ b/app/backend/ingest.py
@@ -126,17 +126,25 @@ def _split(text: str):
         if not f["complete"]:
             method = "ambiguous"
         end = max(e for _, e in cov)
+        f["first"] = min(x for x, _ in cov)             # where the block's own fields start (a block can begin with a preamble line)
         items.append((a, end, f))
     for s, e in _leftovers(text, cov_all):
         items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
         method = "ambiguous"
-    items.sort(key=lambda t: t[0])
+    # T-129: record numbers are the paralegal's citations, so they count only the real records, in paste order. Unsplit text (a preamble, a note between separators) is kept
+    # (D-027: nothing is dropped) but numbered AFTER the real records, so a fax cover sheet on top never shifts "record 1" to "record 2". Text above the first real record
+    # is marked `preamble`.
+    items.sort(key=lambda t: (bool(t[2].get("unsplit")), t[0]))
+    first_real = min((f["first"] for _a, _e, f in items if not f.get("unsplit")), default=None)
+    for _a, e, f in items:
+        if f.get("unsplit") and first_real is not None and e <= first_real:
+            f["preamble"] = True
     return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method
 
 
 def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
     return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
-            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}
+            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit")), "preamble": bool(p.get("preamble"))}
 
 
 class SplitFailed(Exception):
diff --git a/tests/unit/test_ingest.py b/tests/unit/test_ingest.py
index 6944bb5..d9d7bba 100644
--- a/tests/unit/test_ingest.py
+++ b/tests/unit/test_ingest.py
@@ -140,3 +140,31 @@ def test_only_the_exact_banner_line_is_set_aside():
     o = I.ingest(t)
     assert o["banner"] is None and any("prior neck surgery" in r["text"] and r["unsplit"] for r in o["records"])
     assert "SPLIT_AMBIGUOUS" in [w["code"] for w in o["warnings"]]
+
+
+# ---- T-129 (T-123 paralegal minor): a preamble must not shift the record numbers ---------------------------------------------------------------------------------
+_REC1 = 'Date: 2026-01-09\nSource: Lakeside Clinic, intake form\nExcerpt: "Patient completed intake paperwork."'
+_REC2 = 'Date: 2026-01-16\nSource: Lakeside Clinic, initial evaluation\nExcerpt: "Seen for neck pain."'
+
+
+@pytest.mark.parametrize("pre", ["SYNTHETIC — invented for a review probe;", "FAX COVER SHEET\nTo: Dr X\nPages: 3", "SYNTHETIC but the patient also had a prior neck surgery"])
+@pytest.mark.parametrize("sep", ["\n\n", "\n---\n"])
+def test_a_preamble_does_not_shift_the_record_numbers(pre, sep):
+    out = I.ingest(pre + sep + _REC1 + "\n---\n" + _REC2)
+    real = [r for r in out["records"] if not r["unsplit"]]
+    assert [(r["n"], r["id"], r["source"]) for r in real] == [(1, "r1", "Lakeside Clinic, intake form"), (2, "r2", "Lakeside Clinic, initial evaluation")]
+    pre_recs = [r for r in out["records"] if r["unsplit"]]
+    assert len(pre_recs) == 1 and pre_recs[0]["preamble"] and pre_recs[0]["n"] == 3 and pre.split("\n")[0] in pre_recs[0]["text"]     # kept (D-027), numbered last
+    assert "UNSPLIT_TEXT" in [w["code"] for w in out["warnings"]]
+
+
+def test_no_preamble_means_no_extra_record_and_the_library_wording_is_set_aside():
+    out = I.ingest(_REC1 + "\n---\n" + _REC2)
+    assert [r["n"] for r in out["records"]] == [1, 2] and not any(r["unsplit"] or r["preamble"] for r in out["records"])
+    out = I.ingest(I.BANNERS[0] + "\n\n" + _REC1)
+    assert [r["n"] for r in out["records"]] == [1] and out["banner"] == I.BANNERS[0]
+
+
+def test_text_between_records_is_numbered_after_the_real_records_and_is_not_a_preamble():
+    out = I.ingest(_REC1 + "\n---\nfree text between separators\n---\n" + _REC2)
+    assert [(r["n"], r["unsplit"], r["preamble"]) for r in out["records"]] == [(1, False, False), (2, False, False), (3, True, False)]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:19.865Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p app/backend/ingest.py"
}
````

### User / tool · 2026-11-02T11:38:19.946Z

**tool result**
````
"""Stage 0 ingest (all code): split, header date/source, kind, duplicate merge, limits, injection tag, warnings.
R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
import re

from app.backend import dates, flag_templates, injection, lexicon

MAX_CHARS = 60000
MAX_RECORDS = 40

# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")

_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
_SEP = re.compile(r"^[ \t]*---+[ \t]*$", re.MULTILINE)
_DATE_LINE = re.compile(r"^Date:", re.MULTILINE)
_F_DATE = re.compile(r"^Date:[ \t]*(.*)$", re.MULTILINE)
_F_SRC = re.compile(r"^Source:[ \t]*(.*)$", re.MULTILINE)
_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)


class IngestError(ValueError):
    """Input refused before any processing; str(e) is the API error code ('bad_request' | 'input_too_large')."""

    @property
    def code(self) -> str:
        return str(self)


def normalize_text(raw: str) -> str:
    """CRLF and CR become LF; leading and trailing whitespace trimmed (api.md POST /api/cases)."""
    return (raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
    t = normalize_text(text)
    if not t:
        raise IngestError("bad_request")
    if len(t) > max_chars:
        raise IngestError("input_too_large")
    return t


def _spans(text: str):
    """Candidate block (start, end) spans and the method that found them; None when nothing is confident."""
    heads = [m.start() for m in _HEADER.finditer(text)]
    if heads:
        return list(zip(heads, heads[1:] + [len(text)]))
    if _SEP.search(text):
        cuts = [0] + [x for m in _SEP.finditer(text) for x in (m.start(), m.end())] + [len(text)]
        return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2)]
    starts = [m.start() for m in _DATE_LINE.finditer(text)]
    if starts and (_F_SRC.search(text) or _F_EXC.search(text)):
        return list(zip(starts, starts[1:] + [len(text)]))
    return None


def _excerpt_extent(rest: str):
    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
    if rest.startswith('"'):
        i = 0
        while True:
            j = rest.find("\n", i)
            seg = rest[i:len(rest) if j < 0 else j].rstrip()
            if seg.endswith('"') and i + len(seg) > 1:
                return rest[1:i + len(seg) - 1], i + len(seg)
            if j < 0:
                break
            i = j + 1
    return rest.strip(), len(rest.rstrip())


def _scan_block(text: str, a: int, b: int):
    """Parse one block. Returns (fields | None, covered spans). Covered spans are absolute; whatever lies outside them is leftover."""
    block = text[a:b]
    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
    h = _HEADER.match(block)
    if h:
        cov.append((a, a + h.end()))
    found = 0
    for key, pat in (("date_raw", _F_DATE), ("source", _F_SRC)):
        m = pat.search(block)
        if m:
            f[key] = m.group(1).strip()
            cov.append((a + m.start(), a + m.end()))
            found += 1
    e = _F_EXC.search(block)
    if e:
        exc, used = _excerpt_extent(block[e.end():])
        f["excerpt"] = exc
        cov.append((a + e.start(), a + e.end() + used))
        found += 1
    f["complete"] = found == 3
    return (f if found else None), cov


def _leftovers(text: str, cov: list):
    """Non-blank segments of `text` not inside any covered span, as (start, end); an exact golden banner line (BANNERS) on line 1 is exempt."""
    out, pos = [], 0
    for s, e in sorted(cov) + [(len(text), len(text))]:
        if s > pos:
            seg = text[pos:s]
            if seg.strip():
                lead = len(seg) - len(seg.lstrip())
                out.append((pos + lead, pos + len(seg.rstrip())))
        pos = max(pos, e)
    return [(s, e) for s, e in out if not (s == 0 and text[s:e] in BANNERS)]


def _split(text: str):
    """(records, method). Every non-blank character of the input ends up inside some record; text outside a recognised block becomes
    an `unsplit` record (D-027) and the split is reported ambiguous."""
    spans = _spans(text)
    if not spans:
        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
    items, method = [], "code"
    cov_all = [] if _HEADER.search(text) else [(m.start(), m.end()) for m in _SEP.finditer(text)]   # separator lines carry no content
    for a, b in spans:
        f, cov = _scan_block(text, a, b)
        cov_all += cov
        if f is None:
            continue
        if not f["complete"]:
            method = "ambiguous"
        end = max(e for _, e in cov)
        f["first"] = min(x for x, _ in cov)             # where the block's own fields start (a block can begin with a preamble line)
        items.append((a, end, f))
    for s, e in _leftovers(text, cov_all):
        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
        method = "ambiguous"
    # T-129: record numbers are the paralegal's citations, so they count only the real records, in paste order. Unsplit text (a preamble, a note between separators) is kept
    # (D-027: nothing is dropped) but numbered AFTER the real records, so a fax cover sheet on top never shifts "record 1" to "record 2". Text above the first real record
    # is marked `preamble`.
    items.sort(key=lambda t: (bool(t[2].get("unsplit")), t[0]))
    first_real = min((f["first"] for _a, _e, f in items if not f.get("unsplit")), default=None)
    for _a, e, f in items:
        if f.get("unsplit") and first_real is not None and e <= first_real:
            f["preamble"] = True
    return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method


def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit")), "preamble": bool(p.get("preamble"))}


class SplitFailed(Exception):
    """The model could not give a split (call failed, no recorded answer, unusable output). `code` is a reason code; never model text."""
    def __init__(self, code: str, replayed: bool = False):
        super().__init__(code)
        self.code = code
        self.replayed = replayed           # True: the reason was stored by an earlier run; no call was made, so it is not a new failure


def validate_split(text: str, spans, max_records: int = None) -> list:
    """Code check on the model's record boundaries (D-031). `spans` = [(start, end)]. Valid only if they cover `text` exactly
    (first start 0, each end == next start, last end == len(text)), every start falls on a line start, and there are at least two.
    Returns the list of (start, end) or raises ValueError; the caller then keeps the single unsplit record."""
    sp = [(int(a), int(b)) for a, b in spans]
    if max_records is not None and len(sp) > max_records:
        raise ValueError("SPLIT_TOO_MANY")
    if len(sp) < 2 or sp[0][0] != 0 or sp[-1][1] != len(text):
        raise ValueError("SPLIT_NOT_COVERING")
    for i, (a, b) in enumerate(sp):
        if not a < b or (i and a != sp[i - 1][1]):
            raise ValueError("SPLIT_NOT_CONTIGUOUS")
        if a and text[a - 1] != "\n":
            raise ValueError("SPLIT_NOT_ON_LINE_START")
        if not text[a:b].strip():
            raise ValueError("SPLIT_EMPTY_RECORD")
    return sp


def numbered(text: str) -> str:
    """The text with an '@OFFSET| ' label on every line, so the model can name boundaries without counting characters."""
    out, pos = [], 0
    for line in text.split("\n"):
        out.append(f"@{pos}| {line}")
        pos += len(line) + 1
    return "\n".join(out)


def _llm_records(text: str, spans: list) -> list:
    """Records from validated spans. Fields come from code only (labelled lines, or a first line that parses as a date)."""
    out = []
    for a, b in spans:
        s0 = a + (len(text[a:b]) - len(text[a:b].lstrip()))
        first_line = text[s0:b].split("\n", 1)[0].rstrip()
        if s0 == 0 and first_line in BANNERS:       # the golden banner line belongs to no record
            s0 += len(first_line)
            s0 += len(text[s0:b]) - len(text[s0:b].lstrip())
        e0 = a + len(text[a:b].rstrip())
        if s0 >= e0:
            continue
        f, _cov = _scan_block(text, s0, e0)
        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
        if not f["excerpt"]:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:20.361Z

**tool call — Bash**
````
{
 "command": "grep -rn \"unsplit\\|\\\"preamble\\\"\\|preamble\" app --include=*.py --include=*.js --include=*.html -l; grep -rn \"preamble\" app memory/contracts/api.md docs | grep -v \"^app/backend/ingest.py\" | head -20"
}
````

### User / tool · 2026-11-02T11:38:20.469Z

**tool result**
````
app/backend/ingest.py
app/backend/split_llm.py
app/backend/pipeline.py
app/backend/gaps.py
memory/contracts/api.md:76:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:23.280Z

**tool call — Bash**
````
{
 "command": "sed -n 200,420p app/backend/ingest.py; grep -n \"unsplit\\|preamble\\|\\\"n\\\"\\]\\|\\['n'\\]\" app/backend/split_llm.py app/backend/pipeline.py app/backend/gaps.py | head -40"
}
````

### User / tool · 2026-11-02T11:38:23.380Z

**tool result**
````
        if not f["excerpt"]:
            f["excerpt"] = text[s0:e0].strip()
        if not f["date_raw"]:
            first = text[s0:e0].split("\n", 1)[0].strip()
            left, _, right = re.split(r"(\s+[\u2014\u2013|-]\s+)", first, maxsplit=1)[:3] if re.search(r"\s+[\u2014\u2013|-]\s+", first) else (first, "", "")
            if dates.parse_date(left.strip())["status"] == "parsed":     # 'May 4, 2026 - Pottsworth Emergency Department' or a bare date line
                f["date_raw"] = left.strip()
                if right.strip() and not f["source"]:
                    f["source"] = right.strip()
                    f["excerpt"] = text[s0:e0].split("\n", 1)[1].strip() if "\n" in text[s0:e0] else f["excerpt"]
        out.append(_record(len(out) + 1, text[s0:e0], s0, e0, f))
    return out


def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
    text = check_limits(raw_text, max_chars)
    recs, _ = _split(text)
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    return recs


def record_kind(source: str, excerpt: str = "") -> str:
    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
    if not (source or "").strip():
        return "unsplit_text"
    for e in lexicon.code_list("non_encounter"):
        if e["regex"].search(source or ""):
            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
    return "encounter"


def _norm(s: str) -> str:
    return " ".join((s or "").split()).casefold()


def dedupe(records: list) -> list:
    """Groups of record numbers (in file order): same date + same normalised provider label + same normalised text merge (R-TL-7)."""
    groups, order = {}, []
    for r in records:
        p = dates.parse_date(r["date_raw"])
        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(r["n"])
    return [sorted(groups[k]) for k in order]


_PHI = [re.compile(p, re.IGNORECASE) for p in (
    r"\b\d{3}-\d{2}-\d{4}\b",                                  # SSN
    r"(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b",  # phone
    r"\bMRN\s*[:#]?\s*[A-Z0-9-]{5,}")]                         # MRN


def _warn(code: str, message: str, item_id=None) -> dict:
    return {"code": code, "message": message, "item_id": item_id}


def warnings(raw_text: str) -> list:
    return ingest(raw_text)["warnings"]


def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS, splitter=None, not_duplicates=()) -> dict:
    """Everything stage 0 knows. Zero model calls unless `splitter(text) -> [(start, end)] | None` is given AND the code split found one
    unsplit block (D-031); its answer is accepted only if validate_split passes, else the single record stays.
    `not_duplicates`: record ids ('r2') the paralegal said are NOT duplicates of the record they matched; they stay separate (D-031).
    Raises IngestError('bad_request'|'input_too_large') first."""
    text = check_limits(raw_text, max_chars)
    recs, method = _split(text)
    llm_split, split_failure, split_detail, split_call_id = False, None, None, None
    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
    if eligible and not splitter:
        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
    elif method == "ambiguous" and not eligible and len(recs) > 1:
        split_failure = "NOT_ATTEMPTED"    # several records plus an unsplit tail: the model is only asked about a single block, so say that
        # (one labelled but incomplete record gets no reason: SPLIT_AMBIGUOUS already describes it, and "several records" would be false)
    if splitter and eligible:
        try:
            got = splitter(text)
        except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
            got, split_failure, split_detail = None, e.code, None if e.replayed else e.code
            if e.code == "FIXTURE_MISS":   # no recorded answer is the same user-facing state as no model; the detail stays for the run's error entry
                split_failure = "NO_MODEL"
        if got is not None:
            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
            try:
                checked = validate_split(text, spans or [], max_records)
            except ValueError as e:        # the code check refused the proposal: keep the one record, with the reason code
                split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
            else:
                recs, method, llm_split = _llm_records(text, checked), "llm", True
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    groups = dedupe(recs)
    if not_duplicates:
        nd = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
        out = []
        for grp in groups:
            out.append([grp[0]] + [n for n in grp[1:] if n not in nd])
            out += [[n] for n in grp[1:] if n in nd]
        groups = out
        groups.sort(key=lambda g: g[0])
    first_of = {n: g[0] for g in groups for n in g}
    warns, to_confirm, record_warnings = [], [], []
    if llm_split:
        warns.append(_warn("LLM_SPLIT", "The pasted text had no recognisable record markers; the AI proposed the record boundaries and code checked them. Check the split."))
    elif method == "ambiguous":
        warns.append(_warn("SPLIT_AMBIGUOUS", "Record boundaries could not be found with confidence; check the split."))
        if split_failure:
            if split_failure == "NOT_ATTEMPTED":
                msg = "The paste has several records and some text outside them; the AI is only asked to split a single unsplit block, so that text stays its own record (NOT_ATTEMPTED)."
            elif split_failure == "NO_MODEL":
                msg = "No model was available to propose record boundaries; the paste stays one record."
            else:
                msg = "The AI's proposed record boundaries were not used (" + split_failure + "); the paste stays one record."
            warns.append(_warn("SPLIT_REJECTED", msg))
    if any(len(g) > 1 for g in groups):
        warns.append(_warn("DUPLICATE_MERGED", "Identical records were merged into one entry that cites all of them."))
    if any(p.search(text) for p in _PHI):
        warns.append(_warn("PHI_PATTERN", "Text looks like it contains an SSN, phone number or MRN. This tool is for synthetic data only."))
    for r in recs:
        p = dates.parse_date(r["date_raw"])
        kind = record_kind(r["source"], r["excerpt"])
        hits = [{**h, "field": "excerpt"} for h in injection.scan(r["excerpt"])] + \
               [{**h, "field": "source"} for h in injection.scan(r["source"])]
        rid = f"r{r['n']}"
        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
                 injection_tag=bool(hits), injection_hits=hits)
        if llm_split:
            line = r["excerpt"].split("\n", 1)[0][:160]
            at = r["text"].find(line)
            record_warnings.append({"type": "record_warning", "category": "llm_split", "record_no": r["n"], "call_id": split_call_id,
                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
                                                  "end": r["char_start"] + at + len(line) if at >= 0 else None}]})
        if r["unsplit"]:
            warns.append(_warn("UNSPLIT_TEXT", "Text outside any recognised record was kept as its own record; check it and add separators if it belongs to one.", rid))
        if p["status"] != "parsed":
            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
            record_warnings.append({"type": "record_warning", "category": "date_ambiguous", "record_no": r["n"],
                                    "evidence": [{"field": "date", "text": r["date_raw"]}]})
        if hits:   # one flag per tagged record; evidence = every matched phrase (offsets into the excerpt)
            record_warnings.append({"type": "record_warning", "category": "injection_suspected", "record_no": r["n"],
                                    "evidence": [{"field": h["field"], "text": h["phrase"], "start": h["start"], "end": h["end"]} for h in hits]})
    by_n = {r["n"]: r for r in recs}
    for w in record_warnings:       # title/explanation come from flag_templates only (R-FL-8)
        r = by_n[w["record_no"]]
        ev = w["evidence"][0]["text"]
        w["id"] = f"f_{ {'injection_suspected': 'inj', 'llm_split': 'split'}.get(w['category'], 'date') }_r{r['n']}"
        w["title"], w["explanation"] = flag_templates.render("record_warning", w["category"], provider=r["source"] or None,
                                                             date=r["date_iso"], quote=ev if w["category"] == "injection_suspected" else None,
                                                             raw=r["date_raw"] if w["category"] == "date_ambiguous" else None)
        w["reasons"] = {"injection_suspected": ["INJECTION_SUSPECTED"], "llm_split": ["LLM_SPLIT"]}.get(w["category"], [])
    first = text.split("\n", 1)[0].rstrip()
    return {"banner": first if first in BANNERS else None, "records": recs, "groups": groups, "split_method": method if method in ("code", "llm") else "ambiguous", "split_failure": split_failure, "split_detail": split_detail, "warnings": warns,
            "dates_to_confirm": to_confirm, "record_warnings": record_warnings,
            "injection_records": [r["id"] for r in recs if r["injection_tag"]]}


def evidence_span(rec: dict, field: str, needle: str = None) -> dict:
    """Evidence item for a record: field 'date' | 'source' (the header line) or 'excerpt' (`needle`, a verbatim substring of the record).
    Offsets are absolute in the normalised input when the record carries `text` and `char_start`; otherwise they are None."""
    text, base = rec.get("text"), rec.get("char_start")
    out = {"record_no": rec["n"], "field": field, "text": needle, "start": None, "end": None}
    if field in ("date", "source"):
        pat = _F_DATE if field == "date" else _F_SRC
        m = pat.search(text) if text else None
        out["text"] = m.group(0) if m else (rec.get("date_iso") if field == "date" else rec.get("source"))
        if m and base is not None:
            out["start"], out["end"] = base + m.start(), base + m.end()
    elif text and base is not None and needle:
        i = text.find(needle)
        if i >= 0:
            out["start"], out["end"] = base + i, base + i + len(needle)
    return out
app/backend/split_llm.py:1:"""LLM split fallback (D-031): ask the model for record-boundary character offsets when the code split found one unsplit block.
app/backend/pipeline.py:51:    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
app/backend/pipeline.py:56:    by_n = {r["n"]: r for r in recs}
app/backend/pipeline.py:96:            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
app/backend/pipeline.py:158:            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
app/backend/pipeline.py:228:    by_n = {r["n"]: r for r in ing["records"]}
app/backend/pipeline.py:283:    by_n = {r["n"]: r for r in recs}
app/backend/pipeline.py:347:                f["id"] = f"f_r{r['n']}_{k}"
app/backend/gaps.py:80:        if k not in ("encounter", "unsplit_text"):
app/backend/gaps.py:97:            by_date.setdefault(r["date_iso"], []).append(r["n"])
app/backend/gaps.py:111:        if r.get("kind") == "unsplit_text" or r.get("date_iso"):
app/backend/gaps.py:118:    if any(r.get("injection_tag") for r in records if r["n"] in ends):
app/backend/gaps.py:136:                     key=lambda r: (r["date_iso"], r["n"]))
app/backend/gaps.py:139:            "sentence": flag_templates.admin_alternative([(r["n"], r.get("source") or admin_label(r)) for r in dropped], days, lo, hi)}
app/backend/gaps.py:146:    by_n = {r["n"]: r for r in records}
app/backend/gaps.py:170:    by_n = {r["n"]: r for r in records}
app/backend/gaps.py:177:        inside = sorted((r for r in records if r.get("date_iso") and lo < r["date_iso"] < hi), key=lambda r: (r["date_iso"], r["n"]))
app/backend/gaps.py:180:        a = max(r["n"] for r in records if r.get("date_iso") == lo and not admin_label(r))
app/backend/gaps.py:181:        b = min(r["n"] for r in records if r.get("date_iso") == hi and not admin_label(r))
app/backend/gaps.py:186:        split = flag_templates.admin_split_warning([(r["n"], r.get("source") or admin_label(r), r["date_iso"]) for r in inside], pieces)
app/backend/gaps.py:190:        w = [{"side": "inside", "record_no": r["n"], "record_type": admin_label(r), "date": r["date_iso"], "warning": split,
app/backend/gaps.py:194:                    "record_nos": sorted({a, b} | {r["n"] for r in inside}), "evidence": ev,
app/backend/gaps.py:201:    by_n = {r["n"]: r for r in records}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:30.860Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/T128_9_127_r1/parent && git archive 3a74f75~1 | tar -x -C $S/T128_9_127_r1/parent; diff -rq <(cd $S/T128_9_127_r1/repo && git -C /Users/arsis/zlayt-pm-project ls-files 2>/dev/null | head -0) /dev/null; git archive 93de5f2 | tar -t | wc -l; (cd $S/T128_9_127_r1/repo && find . -type f | wc -l); ls evals evals/golden | head -40; ls evals/library | head"
}
````

### User / tool · 2026-11-02T11:38:31.775Z

**tool result**
````
head: illegal line count -- 0
    2102
    2040
evals:
__init__.py
__pycache__
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

evals/golden:
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
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:38.524Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; mkdir -p $S/scripts; cat > $S/scripts/cmp_ingest.py <<'EOF'\nimport sys, json, glob, importlib.util, os\ndef load(root):\n    sys.path.insert(0, root)\n    for k in list(sys.modules):\n        if k==\"app\" or k.startswith(\"app.\"): del sys.modules[k]\n    import app.backend.ingest as I\n    m = I\n    sys.path.pop(0)\n    return m\nold_root, new_root = sys.argv[1], sys.argv[2]\nold = load(old_root); \nmods_old = {k:v for k,v in sys.modules.items() if k.startswith(\"app\")}\nnew = load(new_root)\nfiles = sorted(set(glob.glob(new_root+\"/evals/**/*.txt\", recursive=True)+glob.glob(new_root+\"/tests/**/*.txt\", recursive=True)+glob.glob(new_root+\"/spec/**/*.txt\", recursive=True)+glob.glob(new_root+\"/app/**/*.txt\", recursive=True)+glob.glob(new_root+\"/evals/**/*.json\", recursive=True)))\ndiff=0; n=0\nfor f in files:\n    if f.endswith(\".json\"): continue\n    t = open(f, encoding=\"utf-8\").read()\n    try:\n        a = old.ingest(t); b = new.ingest(t)\n    except Exception as e:\n        continue\n    n+=1\n    ka = [(r[\"n\"], r[\"source\"], r[\"unsplit\"]) for r in a[\"records\"]]\n    kb = [(r[\"n\"], r[\"source\"], r[\"unsplit\"]) for r in b[\"records\"]]\n    if ka != kb:\n        diff+=1; print(\"DIFF\", f.replace(new_root+\"/\",\"\"), ka, kb)\nprint(\"files\", n, \"diff\", diff)\nEOF\n.venv/bin/python -I $S/scripts/cmp_ingest.py $S/parent $S/repo 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T11:38:38.856Z

**tool result**
````
files 27 diff 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:47.192Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/ab.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nimport app.backend.ingest as I\nprint(I.__file__)\nR1='Date: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Patient completed intake paperwork.\"'\nR2='Date: 2026-01-16\\nSource: Lakeside Clinic, initial evaluation\\nExcerpt: \"Seen for neck pain.\"'\ncases = {\n \"pre+sep\": \"FAX COVER\\nPages: 3\\n---\\n\"+R1+\"\\n---\\n\"+R2,\n \"mid-note\": R1+\"\\n---\\nfree text between\\n---\\n\"+R2,\n \"header-style\": \"=== Record 1 ===\\n\"+R1+\"\\n=== Record 2 ===\\n\"+R2,\n \"pre+header-style\": \"cover note\\n=== Record 1 ===\\n\"+R1+\"\\n=== Record 2 ===\\n\"+R2,\n \"pre no sep\": \"Cover note from firm\\n\"+R1+\"\\n\\n\"+R2,\n \"pre blank sep\": \"Cover note\\n\\n\"+R1+\"\\n\\n\"+R2,\n \"trailing note\": R1+\"\\n---\\n\"+R2+\"\\n---\\nSigned: records dept\",\n \"trailing no sep\": R1+\"\\n\\n\"+R2+\"\\nSigned: records dept\",\n \"date-only pre\": \"Date: 2026-01-01\\nrandom\\n---\\n\"+R1+\"\\n---\\n\"+R2,\n}\nfor k,t in cases.items():\n    o=I.ingest(t)\n    print(k, [(r[\"n\"], r[\"id\"], r[\"unsplit\"], r.get(\"preamble\"), (r[\"source\"] or r[\"text\"][:25]).replace(\"\\n\",\"|\")) for r in o[\"records\"]], o[\"split_method\"], [w[\"code\"] for w in o[\"warnings\"]])\nEOF\nfor d in parent repo; do echo == $d; .venv/bin/python -I $S/scripts/ab.py $S/$d; done"
}
````

### User / tool · 2026-11-02T11:38:47.503Z

**tool result**
````
== parent
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/parent/app/backend/ingest.py
pre+sep [(1, 'r1', True, None, 'FAX COVER|Pages: 3'), (2, 'r2', False, None, 'Lakeside Clinic, intake form'), (3, 'r3', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
mid-note [(1, 'r1', False, None, 'Lakeside Clinic, intake form'), (2, 'r2', True, None, 'free text between'), (3, 'r3', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
header-style [(1, 'r1', False, None, 'Lakeside Clinic, intake form'), (2, 'r2', False, None, 'Lakeside Clinic, initial evaluation')] code []
pre+header-style [(1, 'r1', True, None, 'cover note'), (2, 'r2', False, None, 'Lakeside Clinic, intake form'), (3, 'r3', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
pre no sep [(1, 'r1', True, None, 'Cover note from firm'), (2, 'r2', False, None, 'Lakeside Clinic, intake form'), (3, 'r3', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
pre blank sep [(1, 'r1', True, None, 'Cover note'), (2, 'r2', False, None, 'Lakeside Clinic, intake form'), (3, 'r3', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
trailing note [(1, 'r1', False, None, 'Lakeside Clinic, intake form'), (2, 'r2', False, None, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, None, 'Signed: records dept')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
trailing no sep [(1, 'r1', False, None, 'Lakeside Clinic, intake form'), (2, 'r2', False, None, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, None, 'Signed: records dept')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
date-only pre [(1, 'r1', False, None, 'Date: 2026-01-01'), (2, 'r2', True, None, 'random'), (3, 'r3', False, None, 'Lakeside Clinic, intake form'), (4, 'r4', False, None, 'Lakeside Clinic, initial evaluation')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
== repo
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo/app/backend/ingest.py
pre+sep [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, True, 'FAX COVER|Pages: 3')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
mid-note [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, False, 'free text between')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
header-style [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation')] code []
pre+header-style [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, True, 'cover note')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
pre no sep [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, True, 'Cover note from firm')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
pre blank sep [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, True, 'Cover note')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
trailing note [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, False, 'Signed: records dept')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
trailing no sep [(1, 'r1', False, False, 'Lakeside Clinic, intake form'), (2, 'r2', False, False, 'Lakeside Clinic, initial evaluation'), (3, 'r3', True, False, 'Signed: records dept')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
date-only pre [(1, 'r1', False, False, 'Date: 2026-01-01'), (2, 'r2', False, False, 'Lakeside Clinic, intake form'), (3, 'r3', False, False, 'Lakeside Clinic, initial evaluation'), (4, 'r4', True, False, 'random')] ambiguous ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:52.232Z

**tool call — Bash**
````
{
 "command": "grep -rn \"ingest\\.ingest\\|ingest(\\|split_records(\\|I\\.ingest\" app --include=*.py | grep -v \"^app/backend/ingest.py\" | head -20; grep -rn \"char_start\" app --include=*.py --include=*.js | grep -v \"^app/backend/ingest.py\" | head -20"
}
````

### User / tool · 2026-11-02T11:38:52.350Z

**tool result**
````
app/backend/store.py:23:            body = ingest.split_records(block)[0]["excerpt"]
app/backend/split_llm.py:5:record_warning LLM_SPLIT (ingest.ingest). Fields (date, source, excerpt) never come from the model.
app/backend/present.py:241:        body = ingest.split_records(block)[0]["excerpt"]
app/backend/pipeline.py:49:def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
app/backend/pipeline.py:52:    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
app/backend/pipeline.py:217:    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
app/backend/pipeline.py:278:        ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
app/backend/pipeline.py:505:        language.case_check(language.annotate(IN.ingest(raw)["records"]))
app/backend/language.py:322:        body = ingest.split_records(block)[0]["excerpt"]
app/frontend/manual.js:17:      let a = s.start, b = s.end, txt = rec.text.slice(a - rec.char_start, b - rec.char_start);
app/frontend/manual.js:43:      const body = { summary: d.summary.trim(), excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
app/frontend/sidebyside.js:16:    const rs = span.start == null ? null : span.start - rec.char_start, re = span.end == null ? null : span.end - rec.char_start;
app/frontend/mock_flags.js:9:  const find = (recs, rn, sub) => { const r = recs.find((x) => x.seq === rn); const i = r ? r.text.indexOf(sub) : -1; if (i < 0) return null; return { record_id: r.id, excerpt: sub, start: r.char_start + i, end: r.char_start + i + sub.length }; };
app/frontend/excerpt.js:38:      const text = rec.text.slice(units[lo].start - rec.char_start, units[hi].end - rec.char_start);
app/frontend/mock.js:57:        injection_tag: false, encounter: true, char_start: h.at, char_end: h.at + block.length, text: block,
app/frontend/mock.js:67:    return { start: use[0].start, end: use[use.length - 1].end, text: rec.text.slice(use[0].start - rec.char_start, use[use.length - 1].end - rec.char_start), sents: sentences(rec._ex, rec._exStart) };
app/frontend/mock.js:98:        const at = r.char_start + r.text.indexOf(t); const sent = r.sentences.find((s) => s.start <= at && at < s.end) || { text: t, start: at, end: at + t.length };
app/frontend/mock.js:113:        computed: { from: enc[i - 1].date_iso, to: enc[i].date_iso, days, threshold: 30 }, evidence: [enc[i - 1], enc[i]].map((r) => ({ record_id: r.id, excerpt: "Date: " + r.date_iso, start: r.char_start + r.text.indexOf("Date:"), end: r.char_start + r.text.indexOf("Date:") + 16 })),
app/frontend/mock.js:178:        const source = recs.map((rid) => { const r = c.records.find((x) => x.id === rid); return { record_id: rid, char_start: r.char_start, char_end: r.char_end, highlight_start: it.excerpt_start, highlight_end: it.excerpt_end }; });
app/frontend/source.js:9:    const rs = span.start - rec.char_start, re = span.end - rec.char_start;
app/frontend/dev/harness.js:9:      m.append(el("mark", { "data-testid": "record-highlight" }, r.text.slice(s.start - r.char_start, s.end - r.char_start))); });
app/frontend/dev/mock-data.js:20:   "char_start": 106,
app/frontend/dev/mock-data.js:35:   "char_start": 315,
app/frontend/dev/mock-data.js:50:   "char_start": 555,
app/frontend/dev/mock-data.js:65:   "char_start": 775,
app/frontend/dev/mock-data.js:80:   "char_start": 954,
app/frontend/dev/mock-data.js:95:   "char_start": 1090,
app/frontend/dev/mock-data.js:110:   "char_start": 1225,
app/frontend/dev/mock-data.js:125:   "char_start": 1455,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:54.596Z

**tool call — Bash**
````
{
 "command": "sed -n 205,300p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T11:38:54.678Z

**tool result**
````
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing)
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
    a["state"], a["reasons"] = state, reasons
    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None)}
    return a


def _entry_for(entries: list, record_no: int):
    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)


def _err(code, stage, record_no=None, cause=None) -> dict:
    d = {"code": code, "stage": stage}
    if record_no is not None:
        d["record_no"] = record_no
    if cause:
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = call or AU.make_call(conn, cid, now=clock)
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    try:
        ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
    except language.UnsupportedLanguage:               # D-042: a clear failure, never a run that guesses; the case is not left 'running'
        DB.update_case(conn, cid, status="failed", error=json.dumps({"code": "unsupported_language", "message": "The records are not in English or Spanish."}))
        raise
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    _store_split_failure(conn, cid, ing.get("split_failure"))
    if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing)
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
    status = "done"
    timed_out = False

    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:01.843Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo && (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q > ../unit_full.txt 2>&1 &) ; sleep 1; echo started",
 "run_in_background": false
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:02.239Z

**tool call — Bash**
````
{
 "command": "git diff 93de5f2~1 93de5f2 -- app memory | cat"
}
````

### User / tool · 2026-11-02T11:39:02.942Z

**tool result**
````
started
````

### User / tool · 2026-11-02T11:39:03.041Z

**tool result**
````
diff --git a/app/backend/present.py b/app/backend/present.py
index 40c403f..9e1d949 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -103,6 +103,41 @@ def flag_view(row, recs):
             "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
 
 
+def gap_change_index(events, current: dict):
+    """T-127: which gap figures a confirm_date moved, kept with the case. `events` are the case's review events (oldest first); each `confirm_date` event's `after.gap_changes`
+    holds what confirm_date reported (with record_seq and sentence). `current` maps gap flag id -> {days, from, to}. Returns ({flag_id: change} for gaps whose CURRENT figures
+    are the ones that change produced, [removed changes whose gap is still gone]). A later change to the same gap replaces the earlier one; once the figures differ from the
+    ones the change produced, nothing is claimed. Code over stored figures, never a model."""
+    latest, gone = {}, {}
+    for e in events:
+        if e.get("action") != "confirm_date":
+            continue
+        for ch in (e.get("after") or {}).get("gap_changes") or []:
+            fid = ch.get("flag_id")
+            if ch.get("change") == "removed":
+                latest.pop(fid, None)
+                gone[fid] = ch
+            else:
+                gone.pop(fid, None)
+                latest[fid] = ch
+    kept = {}
+    for fid, ch in latest.items():
+        cur = current.get(fid)
+        if cur and cur.get("days") == ch.get("new_days") and (ch.get("new_from") is None or cur.get("from") == ch["new_from"]) and (ch.get("new_to") is None or cur.get("to") == ch["new_to"]):
+            kept[fid] = ch
+    return kept, [ch for fid, ch in gone.items() if fid not in current]
+
+
+def _with_gap_changes(conn, case_id, flags):
+    """Adds `gap_change` (or None) to every gap flag view; returns (flags, gap_changes_removed)."""
+    cur = {f["id"]: {"days": f["computed"].get("days"), "from": f["computed"].get("from"), "to": f["computed"].get("to")} for f in flags if f["type"] == "gap"}
+    kept, removed = gap_change_index(DB.list_events(conn, case_id), cur)
+    for f in flags:
+        if f["type"] == "gap":
+            f["gap_change"] = kept.get(f["id"])
+    return flags, removed
+
+
 _VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
 _ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
 
@@ -116,12 +151,16 @@ def item_view(conn, case_id, item_id):
     kind = _ID_KIND[item_id[0]]
     v = _VIEW[kind](row, _recs_by_id(conn, case_id))
     v["kind"] = kind
+    if kind == "flag":
+        _with_gap_changes(conn, case_id, [v])
     return v
 
 
 def all_items(conn, case_id):
     recs = _recs_by_id(conn, case_id)
-    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
+    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
+    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
+    return out
 
 
 def totals_view(conn, case_id):
@@ -263,7 +302,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
     return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
             "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
diff --git a/app/backend/review.py b/app/backend/review.py
index 26be476..f15febe 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -353,9 +353,10 @@ def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None)
     gap_changes = []
     removed += _recompute_gaps(conn, case_id, t, gap_changes)
     for ch in gap_changes:
+        ch["record_seq"] = rec["seq"]
         ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
     # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
-    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
+    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
     enforce_ocr(conn, case_id, t)
     from app.backend import present
     return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
@@ -379,9 +380,9 @@ def _without_date_doubt(item: dict) -> dict:
     return out
 
 
-def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
+def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
     after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
-             "cleared_date_ambiguous": cleared}
+             "cleared_date_ambiguous": cleared, "gap_changes": list(gap_changes)}       # T-127: the change is kept with the case; GET case reads it back (present.gap_change_index)
     before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
     conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                  (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index e889028..ea1064c 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -73,7 +73,7 @@ Request text is normalised first (CRLF and CR become LF; leading/trailing whites
   "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
   "warnings": [] }
 ```
-(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
+(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
 
 ## POST /api/cases/pdf (D-031)
 Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
@@ -265,7 +265,7 @@ Response 200: the record with `date_status: "confirmed"`, its entry's date, the
 - Accident-date conflict: the earliest dated record of ANY kind sets the comparison. If every record on that earliest date looks like paperwork, the explanation never says "first recorded treatment" for it: title "Stated accident date is later than the earliest record"; "... is later than the earliest recorded date, January 12, 2026 (record 1: <header>), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: <header> is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: <header>), and the stated date is not later than it. Check when treatment actually began before relying on this comparison." (`also later` when it is; "there is no recorded visit to compare with." when no visit exists). `first_treatment_date` keeps the earliest recorded date. A visit on the earliest date keeps the plain wording.
 - Golden `gap_table` rows describe the visit-only reading (what `alternative_*` shows); the product's counted rows can have more rows. Code-built from fixed templates, never model text. (Replaces the T-116 r1/r2 `excluded_records`, removed.)
 
-**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
+**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. Each element also has `record_seq` (the record whose date was confirmed). **T-127: the change is kept with the case.** `confirm_date` writes `gap_changes[]` into its `confirm_date` review event (`after.gap_changes`), and `GET /api/cases/{token}` reads it back: a gap flag in `flags[]` whose figures were moved by a confirm_date has `gap_change` (the same element: `{flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to, record_seq, sentence}`), otherwise `gap_change: null`; it stays through reload, another browser and review actions, and goes when that gap's current figures differ from the ones the change produced (a later confirm_date that moves it again replaces it). A gap that no longer applies has no flag, so `GET case` lists it in top-level `gap_changes_removed[]` (same element, `change: "removed"`, `sentence` included) until a gap with the same id exists again. Both are always present (`null` / `[]`). Stored in the DB (the audit event), not in `computed`. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
 
 ## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
 Every entry of `dates_to_confirm` (in `GET /api/cases/{token}` and in the `confirm_date` response) now has a `suggestion`: `null`, or a hint for an **ambiguous** numeric date. Code only (`app/backend/date_convention.py`). It looks at the other numeric dates in the packet whose order is certain (one number above 12: `03/14/2026` is month first, `14/03/2026` is day first), in each record's date label and text. It suggests only when all of that evidence agrees; no evidence, or evidence in both orders, gives `null`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:14.756Z

**tool call — Bash**
````
{
 "command": "grep -n \"def \\|confirm_date\" app/backend/review.py | sed -n 1,120p"
}
````

### User / tool · 2026-11-02T11:39:14.850Z

**tool result**
````
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
22:    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
27:def _now(now):
31:def _item(conn, case_id, item_id):
41:def _bad(msg, **detail):
45:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
57:def _date_unconfirmed_error():
76:def current_text(item: dict):
81:def code_check_failures(rec, item: dict) -> dict:
106:def code_check_message(fails: dict) -> str:
131:def code_check_detail(item_id: str, fails: dict) -> dict:
139:def code_check_error(item_id: str, rec, item: dict):
147:def entry_record(item: dict, recs: list):
152:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None) -> dict:
170:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
192:def ocr_record_ids(conn, case_id: str) -> set:
202:def enforce_ocr(conn, case_id: str, t) -> int:
231:def _quoted_words(toks) -> str:
236:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False):
276:def _edit(conn, case_id, kind, item, body, call, t):
329:# ---------------------------------------------------------------- confirm_date
330:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
359:    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
368:def _without_date_doubt(item: dict) -> dict:
383:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
388:                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
391:def _drop(conn, case_id, flag_id):
396:def _gap_figures(flag: dict) -> dict:
401:def _gap_changes(old: dict, new: dict) -> list:
424:def _gap_change_sentence(ch: dict, seq) -> str:
433:def _recompute_gaps(conn, case_id, t, changes=None):
477:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
525:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
588:def _upsert(conn, case_id, kind, item, t):
598:def judges_for(dollars, call, case_text):
604:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:15.225Z

**tool call — Bash**
````
{
 "command": "grep -n \"def list_events\" -A12 app/db/*.py | head -30; cat tests/unit/test_t127_gap_change_kept.py"
}
````

### User / tool · 2026-11-02T11:39:15.326Z

**tool result**
````
app/db/db.py:257:def list_events(conn, case_id: str, item_id: str = None) -> list:
app/db/db.py-258-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
app/db/db.py-259-    if item_id:
app/db/db.py-260-        q, a = q + " AND item_id=?", a + [item_id]
app/db/db.py-261-    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
app/db/db.py-262-
app/db/db.py-263-
app/db/db.py-264-def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
app/db/db.py-265-    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
app/db/db.py-266-    cid = fields.pop("id", None) or _tok("c")
app/db/db.py-267-    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
app/db/db.py-268-           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
app/db/db.py-269-    _insert(conn, "llm_calls", row)
"""T-127 (T-114 r3): the gap-change record lives with the case, not in one browser. A gap flag whose figures moved in confirm_date carries `gap_change` in
GET /api/cases/{token} until that gap's figures change again; a gap that no longer applies is listed in `gap_changes_removed[]` with its sentence. Fixture backend."""
import pytest

from app.backend import present
from app.db import db as DB
from tests.unit.test_t114_rates_and_demo_judges import LIB09, _load, client  # noqa: F401  (fixture)


def _gap(case):
    return next(f for f in case["flags"] if f["type"] == "gap")


def test_the_changed_gap_flag_carries_gap_change_in_get_case_and_it_survives_a_new_connection(client):
    c, path = client
    tok = _load(c, LIB09)
    assert "gap_change" not in _gap(c.get(f"/api/cases/{tok}").json()) or _gap(c.get(f"/api/cases/{tok}").json())["gap_change"] is None
    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
    want = out["gap_changes"][0]
    for _ in range(2):                                              # a fresh GET (and, below, a fresh app on the same file) gives the same record
        g = _gap(c.get(f"/api/cases/{tok}").json())
        gc = g["gap_change"]
        assert gc["flag_id"] == g["id"] == want["flag_id"] and gc["change"] == "changed" and gc["record_seq"] == 4
        assert (gc["old_days"], gc["new_days"], gc["old_from"], gc["old_to"], gc["new_from"], gc["new_to"]) == (42, 40, "2026-03-03", "2026-04-14", "2026-03-05", "2026-04-14")
        assert gc["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)." == want["sentence"]
        assert "gap_change" not in g["computed"]
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    c2 = TestClient(create_app(path, static_dir="."), client=("127.0.0.1", 50000))
    assert _gap(c2.get(f"/api/cases/{tok}").json())["gap_change"]["new_days"] == 40
    assert c2.get(f"/api/cases/{tok}").json()["gap_changes_removed"] == []
    # reviewing the gap does not lose it
    acc = c.post(f"/api/cases/{tok}/items/{_gap(c.get(f'/api/cases/{tok}').json())['id']}/review", json={"action": "accept"})
    assert acc.status_code == 200 and _gap(c.get(f"/api/cases/{tok}").json())["gap_change"]["new_days"] == 40


def test_gap_change_goes_when_the_gaps_figures_move_again():
    """The kept record matches only the gap's CURRENT figures: a later recompute that moves them again replaces it (the latest event wins; a stale one is never shown)."""
    ev = [{"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r4_r5", "change": "changed", "old_days": 42, "new_days": 40, "old_from": "a", "old_to": "b",
                                                                 "new_from": "2026-03-05", "new_to": "2026-04-14", "record_seq": 4, "sentence": "s1"}]}},
          {"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r4_r5", "change": "changed", "old_days": 40, "new_days": 35, "old_from": "2026-03-05", "old_to": "2026-04-14",
                                                                 "new_from": "2026-03-10", "new_to": "2026-04-14", "record_seq": 6, "sentence": "s2"}]}}]
    cur = {"f_gap_r4_r5": {"days": 35, "from": "2026-03-10", "to": "2026-04-14"}}
    changes, removed = present.gap_change_index(ev, cur)
    assert changes["f_gap_r4_r5"]["sentence"] == "s2" and removed == []
    changes, removed = present.gap_change_index(ev, {"f_gap_r4_r5": {"days": 30, "from": "2026-03-15", "to": "2026-04-14"}})        # moved by something else since: no stale claim
    assert changes == {} and removed == []


def test_a_gap_that_no_longer_applies_is_listed_with_its_sentence_until_it_comes_back():
    ev = [{"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r2_r3", "change": "removed", "old_days": 31, "new_days": None, "old_from": "2026-01-01",
                                                                 "old_to": "2026-02-01", "new_from": None, "new_to": None, "record_seq": 3, "sentence": "A gap of 31 days no longer applies after you confirmed the date of record 3."}]}}]
    changes, removed = present.gap_change_index(ev, {})
    assert changes == {} and [r["sentence"] for r in removed] == ["A gap of 31 days no longer applies after you confirmed the date of record 3."]
    assert removed[0]["flag_id"] == "f_gap_r2_r3" and removed[0]["old_days"] == 31
    _c, removed = present.gap_change_index(ev, {"f_gap_r2_r3": {"days": 31, "from": "2026-01-01", "to": "2026-02-01"}})        # the same gap exists again
    assert removed == []


def test_confirm_date_writes_the_change_into_its_audit_event(client):
    c, path = client
    tok = _load(c, LIB09)
    c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"})
    conn = DB.connect(path)
    ev = [e for e in DB.list_events(conn, tok) if e["action"] == "confirm_date"]
    assert ev and ev[-1]["after"]["gap_changes"][0]["record_seq"] == 4 and ev[-1]["after"]["gap_changes"][0]["new_days"] == 40
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:16.670Z

**tool call — Bash**
````
{
 "command": "sed -n 329,476p app/backend/review.py; grep -n \"undo\\|reset\" app/backend/api.py | head -20"
}
````

### User / tool · 2026-11-02T11:39:16.759Z

**tool result**
````
# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved, cleared = None, []
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
                cleared.append(e["id"])
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
            cleared.append(a["id"])
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    gap_changes = []
    removed += _recompute_gaps(conn, case_id, t, gap_changes)
    for ch in gap_changes:
        ch["record_seq"] = rec["seq"]
        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "gap_changes": gap_changes,
            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
        reasons.append("AI_TRANSLATION")
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    out = {"state": state, "state_reasons_json": reasons}
    if isinstance(item.get("ladder"), dict):
        out["ladder"] = {**item["ladder"], "state": state}
    return out


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
             "cleared_date_ambiguous": cleared, "gap_changes": list(gap_changes)}       # T-127: the change is kept with the case; GET case reads it back (present.gap_change_index)
    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _gap_figures(flag: dict) -> dict:
    c = flag.get("computed") or {}
    return {"flag_id": flag["id"], "from": c.get("from_date"), "to": c.get("to_date"), "days": c.get("days"), "record_nos": list(c.get("record_nos") or [])}


def _gap_changes(old: dict, new: dict) -> list:
    """Which gap figures a recompute changed (T-114). `old`/`new` map flag id -> _gap_figures. A gap whose id survives and whose figures moved is `changed`; an
    old gap that vanished and a new one that shares a record number with it are ONE `changed` entry (an endpoint moved); the rest are `removed` / `added`.
    Each: {flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to}; the side that does not exist is null. Code over the figures, never a model."""
    rows = []
    fresh = [n for i, n in new.items() if i not in old]
    for i, n in new.items():
        o = old.get(i)
        if o is not None and any(o[k] != n[k] for k in ("from", "to", "days")):
            rows.append(("changed", o, n))
    for i, o in old.items():
        if i in new:
            continue
        mate = next((n for n in fresh if set(n["record_nos"]) & set(o["record_nos"])), None)
        if mate is not None:
            fresh.remove(mate)
        rows.append(("changed" if mate else "removed", o, mate))
    rows += [("added", None, n) for n in fresh]
    nul = {"flag_id": None, "from": None, "to": None, "days": None}
    return [{"flag_id": (n or o)["flag_id"], "change": ch, "old_days": (o or nul)["days"], "new_days": (n or nul)["days"],
             "old_from": (o or nul)["from"], "old_to": (o or nul)["to"], "new_from": (n or nul)["from"], "new_to": (n or nul)["to"]} for ch, o, n in rows]


def _gap_change_sentence(ch: dict, seq) -> str:
    """The plain-words line the UI can announce. The numbers come from the figures in the entry, not from a model."""
    if ch["change"] == "removed":
        return f"A gap of {ch['old_days']} days no longer applies after you confirmed the date of record {seq}."
    if ch["change"] == "added":
        return f"A gap of {ch['new_days']} days now applies after you confirmed the date of record {seq}."
    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."


def _recompute_gaps(conn, case_id, t, changes=None):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002). `changes` (a list) receives the gap figures that moved (T-114)."""
    from app.backend import pipeline as PL
    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    if changes is not None:
        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:36.434Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat $S/unit_full.txt | tail -5; grep -n \"_recompute_gaps\\|gap_change\" app/backend/*.py | grep -v \"^app/backend/review.py:4[0-9][0-9]\" | head -20"
}
````

### User / tool · 2026-11-02T11:39:36.527Z

**tool result**
````
........................................................................ [ 40%]
........................................................................ [ 42%]
........................................................................ [ 44%]
........................................................................ [ 47%]
............................................app/backend/review.py:353:    gap_changes = []
app/backend/review.py:354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
app/backend/review.py:355:    for ch in gap_changes:
app/backend/review.py:357:        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
app/backend/review.py:359:    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
app/backend/review.py:364:            "removed_flag_ids": removed, "gap_changes": gap_changes,
app/backend/review.py:383:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
app/backend/review.py:385:             "cleared_date_ambiguous": cleared, "gap_changes": list(gap_changes)}       # T-127: the change is kept with the case; GET case reads it back (present.gap_change_index)
app/backend/review.py:579:    _recompute_gaps(conn, case_id, t)
app/backend/present.py:106:def gap_change_index(events, current: dict):
app/backend/present.py:107:    """T-127: which gap figures a confirm_date moved, kept with the case. `events` are the case's review events (oldest first); each `confirm_date` event's `after.gap_changes`
app/backend/present.py:115:        for ch in (e.get("after") or {}).get("gap_changes") or []:
app/backend/present.py:131:def _with_gap_changes(conn, case_id, flags):
app/backend/present.py:132:    """Adds `gap_change` (or None) to every gap flag view; returns (flags, gap_changes_removed)."""
app/backend/present.py:134:    kept, removed = gap_change_index(DB.list_events(conn, case_id), cur)
app/backend/present.py:137:            f["gap_change"] = kept.get(f["id"])
app/backend/present.py:155:        _with_gap_changes(conn, case_id, [v])
app/backend/present.py:162:    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
app/backend/present.py:305:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:39:43.661Z

**tool call — Bash**
````
{
 "command": "sed -n 270,480p app/backend/summary_trim.py"
}
````

### User / tool · 2026-11-02T11:39:43.747Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:40:07.109Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/probe_t128.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import summary_trim as T\n# (summary, excerpt, label) fragment-prone: a clause is unsupported and removal could leave a stub\nP = [\n # noun-phrase stubs\n (\"Pain in the neck and lower back.\", \"Lower back pain.\"),\n (\"Pain in the neck and right shoulder.\", \"Right shoulder pain.\"),\n (\"Pain in the neck, back and shoulder.\", \"Shoulder pain.\"),\n (\"Wrist fracture and surgery.\", \"Surgery.\"),\n (\"Wrist fracture, then splint.\", \"Splint applied.\"),\n (\"Neck pain and numbness in the hand.\", \"Hand numbness.\"),\n (\"Laceration repaired with sutures and a dressing.\", \"Dressing applied.\"),\n # connector-led stubs, words outside the list\n (\"MRI ordered, pending insurance approval.\", \"MRI approved.\"),\n (\"Knee surgery recommended, requiring six weeks of crutches.\", \"Crutches issued.\"),\n (\"Neck pain with spasm, prompting a collar.\", \"Collar given.\"),\n (\"Brace applied, despite swelling.\", \"Brace applied.\"),\n (\"Ankle sprain, likely from the fall.\", \"Fall at home.\"),\n (\"Back pain, worse with sitting.\", \"Sitting tolerance reduced.\"),\n (\"Epidural injection given, after which pain eased.\", \"Pain eased.\"),\n (\"Wrist cast placed, along with a sling.\", \"Sling provided.\"),\n (\"Shoulder surgery performed, leading to a sling.\", \"Sling provided.\"),\n (\"Fracture seen on X-ray, suggesting an old injury.\", \"Old injury.\"),\n (\"Physical therapy started, plus home exercises.\", \"Exercises given.\"),\n (\"Neck collar fitted; again advised to rest.\", \"Advised to rest.\"),\n (\"MRI done; mild disc bulge noted at L4.\", \"MRI done.\"),\n (\"Sutured laceration, remains tender to touch.\", \"Sutured laceration.\"),\n (\"Hand numbness; resolved after splinting.\", \"Numbness.\"),\n (\"Wrist pain, with swelling noted over the scaphoid.\", \"Wrist pain.\"),\n (\"Patient reports headache and was prescribed ibuprofen.\", \"Ibuprofen prescribed.\"),\n (\"Rear-ended at a stoplight, now has neck pain.\", \"Neck pain.\"),\n (\"Neck sprain diagnosed, treated with ice.\", \"Ice applied.\"),\n (\"Ankle X-ray negative, however pain persists.\", \"X-ray negative.\"),\n (\"Back pain; also referred to orthopedics.\", \"Referred to orthopedics.\"),\n (\"Knee brace issued, not weight bearing.\", \"Brace issued.\"),\n (\"Fracture of the left wrist, cast applied, not yet healed.\", \"Cast applied.\"),\n (\"Neck pain, no radiation.\", \"Radiation to arm.\"),\n]\nn=0; frag=0\ndef looks_frag(t):\n    import re\n    w = re.findall(r\"[A-Za-z']+\", t.lower())\n    return bool(w) and (len(w)==1 or w[0] in T._LEAD or w[0] in T._CONNECTOR)\nfor s, e in P:\n    r = T.trim(s, e)\n    n+=1\n    flag = r[\"changed\"] and r[\"text\"] and looks_frag(r[\"text\"])\n    frag += bool(flag)\n    print((\"CHANGED \" if r[\"changed\"] else \"whole   \") + (\"FRAG? \" if flag else \"      \") + repr(s), \"|\", repr(e), \"->\", repr(r[\"text\"]) if r[\"changed\"] else \"\", r[\"removed\"] if r[\"changed\"] else \"\")\nprint(n, \"probes; changed:\", sum(T.trim(s,e)[\"changed\"] for s,e in P))\nEOF\n.venv/bin/python -I $S/scripts/probe_t128.py $S/repo"
}
````

### User / tool · 2026-11-02T11:40:07.246Z

**tool result**
````
CHANGED       'Pain in the neck and lower back.' | 'Lower back pain.' -> 'Lower back.' ['Pain in the neck']
CHANGED       'Pain in the neck and right shoulder.' | 'Right shoulder pain.' -> 'Right shoulder.' ['Pain in the neck']
whole         'Pain in the neck, back and shoulder.' | 'Shoulder pain.' ->  
CHANGED FRAG? 'Wrist fracture and surgery.' | 'Surgery.' -> 'Surgery.' ['Wrist fracture']
whole         'Wrist fracture, then splint.' | 'Splint applied.' ->  
CHANGED       'Neck pain and numbness in the hand.' | 'Hand numbness.' -> 'Numbness in the hand.' ['Neck pain']
whole         'Laceration repaired with sutures and a dressing.' | 'Dressing applied.' ->  
CHANGED       'MRI ordered, pending insurance approval.' | 'MRI approved.' -> 'Pending insurance approval.' ['MRI ordered']
CHANGED       'Knee surgery recommended, requiring six weeks of crutches.' | 'Crutches issued.' -> 'Requiring six weeks of crutches.' ['Knee surgery recommended']
whole         'Neck pain with spasm, prompting a collar.' | 'Collar given.' ->  
whole         'Brace applied, despite swelling.' | 'Brace applied.' ->  
CHANGED       'Ankle sprain, likely from the fall.' | 'Fall at home.' -> 'Likely from the fall.' ['Ankle sprain']
CHANGED       'Back pain, worse with sitting.' | 'Sitting tolerance reduced.' -> 'Worse with sitting.' ['Back pain']
CHANGED       'Epidural injection given, after which pain eased.' | 'Pain eased.' -> 'After which pain eased.' ['Epidural injection given']
whole         'Wrist cast placed, along with a sling.' | 'Sling provided.' ->  
CHANGED       'Shoulder surgery performed, leading to a sling.' | 'Sling provided.' -> 'Leading to a sling.' ['Shoulder surgery performed']
CHANGED       'Fracture seen on X-ray, suggesting an old injury.' | 'Old injury.' -> '' ['Fracture seen on X-ray', 'suggesting an old injury']
CHANGED       'Physical therapy started, plus home exercises.' | 'Exercises given.' -> 'Plus home exercises.' ['Physical therapy started']
CHANGED       'Neck collar fitted; again advised to rest.' | 'Advised to rest.' -> 'Again advised to rest.' ['Neck collar fitted']
CHANGED       'MRI done; mild disc bulge noted at L4.' | 'MRI done.' -> 'MRI done.' ['mild disc bulge noted at L4']
whole         'Sutured laceration, remains tender to touch.' | 'Sutured laceration.' ->  
CHANGED       'Hand numbness; resolved after splinting.' | 'Numbness.' -> '' ['Hand numbness', 'resolved after splinting']
whole         'Wrist pain, with swelling noted over the scaphoid.' | 'Wrist pain.' ->  
whole         'Patient reports headache and was prescribed ibuprofen.' | 'Ibuprofen prescribed.' ->  
whole         'Rear-ended at a stoplight, now has neck pain.' | 'Neck pain.' ->  
CHANGED       'Neck sprain diagnosed, treated with ice.' | 'Ice applied.' -> 'Treated with ice.' ['Neck sprain diagnosed']
whole         'Ankle X-ray negative, however pain persists.' | 'X-ray negative.' ->  
whole         'Back pain; also referred to orthopedics.' | 'Referred to orthopedics.' ->  
CHANGED       'Knee brace issued, not weight bearing.' | 'Brace issued.' -> '' ['Knee brace issued', 'not weight bearing']
CHANGED       'Fracture of the left wrist, cast applied, not yet healed.' | 'Cast applied.' -> 'Cast applied.' ['Fracture of the left wrist', 'not yet healed']
CHANGED       'Neck pain, no radiation.' | 'Radiation to arm.' -> 'No radiation.' ['Neck pain']
31 probes; changed: 19
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:40:29.700Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/probe_t128b.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import summary_trim as T\nPOS = [   # an unsupported clause exists and a whole supported clause stays: trim SHOULD fire\n (\"Neck pain. Surgery recommended. Also reports headaches.\", \"Neck pain. Headaches reported.\"),\n (\"Was seen at the ER; surgery recommended.\", \"Seen at ER.\"),\n (\"Neck pain; MRI ordered. Was prescribed ibuprofen.\", \"Neck pain. Ibuprofen prescribed.\"),\n (\"Back pain; injection given. Is improving.\", \"Back pain. Improving.\"),\n (\"Neck pain; surgery recommended.\", \"Neck pain.\"),\n (\"Wrist pain; cast applied; discharged home.\", \"Wrist pain. Discharged home.\"),\n (\"Knee pain, MRI ordered; then physical therapy.\", \"Knee pain. Physical therapy.\"),\n (\"Back pain; ultrasound done. Had a follow-up visit.\", \"Back pain. Follow-up visit.\"),\n (\"Neck pain; epidural given. Which was tolerated.\", \"Neck pain. Tolerated.\"),\n (\"Shoulder pain; sling provided; pain 7/10.\", \"Shoulder pain 7/10.\"),\n (\"Ankle sprain; splint applied; follow-up in two weeks.\", \"Ankle sprain. Follow-up in two weeks.\"),\n (\"Headache; CT scan ordered; ibuprofen advised.\", \"Headache. Ibuprofen advised.\"),\n]\nfor s,e in POS:\n    r=T.trim(s,e)\n    print((\"CHANGED \" if r[\"changed\"] else \"WHOLE   \"), repr(s),\"|\",repr(e),\"->\",repr(r[\"text\"]) if r[\"changed\"] else \"\", r[\"removed\"])\nEOF\n.venv/bin/python -I $S/scripts/probe_t128b.py $S/repo; tail -3 $S/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:40:29.869Z

**tool result**
````
WHOLE    'Neck pain. Surgery recommended. Also reports headaches.' | 'Neck pain. Headaches reported.' ->  []
WHOLE    'Was seen at the ER; surgery recommended.' | 'Seen at ER.' ->  []
WHOLE    'Neck pain; MRI ordered. Was prescribed ibuprofen.' | 'Neck pain. Ibuprofen prescribed.' ->  []
WHOLE    'Back pain; injection given. Is improving.' | 'Back pain. Improving.' ->  []
CHANGED  'Neck pain; surgery recommended.' | 'Neck pain.' -> 'Neck pain.' ['surgery recommended']
CHANGED  'Wrist pain; cast applied; discharged home.' | 'Wrist pain. Discharged home.' -> 'Wrist pain; discharged home.' ['cast applied']
WHOLE    'Knee pain, MRI ordered; then physical therapy.' | 'Knee pain. Physical therapy.' ->  []
WHOLE    'Back pain; ultrasound done. Had a follow-up visit.' | 'Back pain. Follow-up visit.' ->  []
WHOLE    'Neck pain; epidural given. Which was tolerated.' | 'Neck pain. Tolerated.' ->  []
CHANGED  'Shoulder pain; sling provided; pain 7/10.' | 'Shoulder pain 7/10.' -> 'Shoulder pain; pain 7/10.' ['sling provided']
CHANGED  'Ankle sprain; splint applied; follow-up in two weeks.' | 'Ankle sprain. Follow-up in two weeks.' -> 'Ankle sprain; follow-up in two weeks.' ['splint applied']
CHANGED  'Headache; CT scan ordered; ibuprofen advised.' | 'Headache. Ibuprofen advised.' -> 'Headache; ibuprofen advised.' ['CT scan ordered']
........................................................................ [ 49%]
........................................................................ [ 51%]
............................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:40:42.279Z

**tool call — Bash**
````
{
 "command": "sleep 100; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; tail -4 $S/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:40:42.281Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1 tail -4 $S/unit_full.txt. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:40:46.766Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; mkdir -p $S/mut && git archive 93de5f2 | tar -x -C $S/mut && diff -rq $S/mut $S/repo | head -3; echo ok"
}
````

### User / tool · 2026-11-02T11:40:47.615Z

**tool result**
````
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo/app: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo/app/backend: __pycache__
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:40:48.533Z

Now a mutation harness for all three cards.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:41:06.832Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/mut.py <<'EOF'\nimport sys, subprocess, pathlib\nroot = pathlib.Path(sys.argv[1]); PY=\"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nM = [\n # (name, file, old, new, tests)\n (\"T128 connector rule off\", \"app/backend/summary_trim.py\", \"if (after_removed or not any(not d for d in drop[:i])) and _connector_led(clauses[i][0]):\", \"if False:\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector only after_removed (drop leading arm)\", \"app/backend/summary_trim.py\", \"if (after_removed or not any(not d for d in drop[:i])) and _connector_led(clauses[i][0]):\", \"if after_removed and _connector_led(clauses[i][0]):\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector only leading arm (drop after_removed)\", \"app/backend/summary_trim.py\", \"if (after_removed or not any(not d for d in drop[:i])) and _connector_led(clauses[i][0]):\", \"if (not any(not d for d in drop[:i])) and _connector_led(clauses[i][0]):\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 with-join guard off\", \"app/backend/summary_trim.py\", \"if after_removed and _joined_by_with(clauses[i - 1][1]):\", \"if False:\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 bare body part off\", \"app/backend/summary_trim.py\", \"if len(only) == 1 and len(_WORD.findall(summary.lower())) > 1 and any(k == \\\"body\\\"\", \"if False and any(k == \\\"body\\\"\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 bare body part: drop 'summary has >1 word' check\", \"app/backend/summary_trim.py\", \"len(_WORD.findall(summary.lower())) > 1 and\", \"\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 bare body part: any noun not only body\", \"app/backend/summary_trim.py\", \"any(k == \\\"body\\\" for k, _w in _family_hits(_words(only[0])).values())\", \"True\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'which'\", \"app/backend/summary_trim.py\", \"due which who\", \"due who\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'including'\", \"app/backend/summary_trim.py\", \"following followed including includes\", \"following followed includes\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'was'\", \"app/backend/summary_trim.py\", \"unless until if so then also but nor yet was were\", \"unless until if so then also but nor yet were\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'due'\", \"app/backend/summary_trim.py\", \"\"\"\\\"\\\"\\\"due which\"\"\", \"\"\"\\\"\\\"\\\"which\"\"\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'also'\", \"app/backend/summary_trim.py\", \"unless until if so then also but\", \"unless until if so then but\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'however'\", \"app/backend/summary_trim.py\", \"thus therefore however hence\", \"thus therefore hence\", \"tests/unit/test_summary_trim.py\"),\n (\"T128 connector: remove 'consistent'\", \"app/backend/summary_trim.py\", \"hence consistent related\", \"hence related\", \"tests/unit/test_summary_trim.py\"),\n (\"T129 sort unsplit last off\", \"app/backend/ingest.py\", \"items.sort(key=lambda t: (bool(t[2].get(\\\"unsplit\\\")), t[0]))\", \"items.sort(key=lambda t: t[0])\", \"tests/unit/test_ingest.py\"),\n (\"T129 preamble flag never set\", \"app/backend/ingest.py\", \"f[\\\"preamble\\\"] = True\", \"pass\", \"tests/unit/test_ingest.py\"),\n (\"T129 preamble: e <= first_real -> True always\", \"app/backend/ingest.py\", \"first_real is not None and e <= first_real\", \"first_real is not None\", \"tests/unit/test_ingest.py\"),\n (\"T129 first = block start not field start\", \"app/backend/ingest.py\", \"f[\\\"first\\\"] = min(x for x, _ in cov)\", \"f[\\\"first\\\"] = a\", \"tests/unit/test_ingest.py\"),\n (\"T129 preamble kept? drop unsplit (D-027)\", \"app/backend/ingest.py\", \"items.append((s, e, {\\\"date_raw\\\": \\\"\\\", \\\"source\\\": \\\"\\\", \\\"excerpt\\\": text[s:e], \\\"unsplit\\\": True}))\", \"pass\", \"tests/unit/test_ingest.py\"),\n (\"T127 record_seq not stored\", \"app/backend/review.py\", \"ch[\\\"record_seq\\\"] = rec[\\\"seq\\\"]\\n\", \"\\n\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 gap_changes not in event\", \"app/backend/review.py\", \"\\\"cleared_date_ambiguous\\\": cleared, \\\"gap_changes\\\": list(gap_changes)}\", \"\\\"cleared_date_ambiguous\\\": cleared, \\\"gap_changes\\\": []}\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 days check dropped\", \"app/backend/present.py\", \"if cur and cur.get(\\\"days\\\") == ch.get(\\\"new_days\\\") and\", \"if cur and\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 from/to check dropped\", \"app/backend/present.py\", \"and (ch.get(\\\"new_from\\\") is None or cur.get(\\\"from\\\") == ch[\\\"new_from\\\"]) and (ch.get(\\\"new_to\\\") is None or cur.get(\\\"to\\\") == ch[\\\"new_to\\\"]):\", \":\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 new_to check dropped only\", \"app/backend/present.py\", \" and (ch.get(\\\"new_to\\\") is None or cur.get(\\\"to\\\") == ch[\\\"new_to\\\"]):\", \":\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 removed pop on re-add dropped\", \"app/backend/present.py\", \"                gone.pop(fid, None)\\n\", \"\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 removed does not clear latest\", \"app/backend/present.py\", \"                latest.pop(fid, None)\\n\", \"\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 removed list ignores current\", \"app/backend/present.py\", \"return kept, [ch for fid, ch in gone.items() if fid not in current]\", \"return kept, [ch for fid, ch in gone.items()]\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 later event does not replace (first wins)\", \"app/backend/present.py\", \"                latest[fid] = ch\\n\", \"                latest.setdefault(fid, ch)\\n\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 gap_changes_removed not in case_view\", \"app/backend/present.py\", \"\\\"gap_changes_removed\\\": its[\\\"gap_changes_removed\\\"], \", \"\", \"tests/unit/test_t127_gap_change_kept.py\"),\n (\"T127 gap_change not set on flag\", \"app/backend/present.py\", \"            f[\\\"gap_change\\\"] = kept.get(f[\\\"id\\\"])\", \"            f[\\\"gap_change\\\"] = None\", \"tests/unit/test_t127_gap_change_kept.py\"),\n]\nsel = sys.argv[2:] \nfor name, f, old, new, tests in M:\n    if sel and not any(s in name for s in sel): continue\n    p = root/f; src = p.read_text()\n    if old not in src: print(\"NOMATCH\", name); continue\n    p.write_text(src.replace(old, new, 1))\n    try:\n        r = subprocess.run([PY, \"-m\", \"pytest\", tests, \"-q\", \"-x\", \"-p\", \"no:cacheprovider\"], cwd=root, capture_output=True, text=True, timeout=900)\n        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n        print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", tail, flush=True)\n    finally:\n        p.write_text(src)\nEOF\n.venv/bin/python -I $S/scripts/mut.py $S/mut 2>&1 | tail -40",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:41:44.180Z

**tool result**
````
KILLED   T128 connector rule off | 1 failed, 225 passed in 3.42s
SURVIVED T128 connector only after_removed (drop leading arm) | 259 passed in 1.09s
KILLED   T128 connector only leading arm (drop after_removed) | 1 failed, 230 passed in 1.03s
KILLED   T128 with-join guard off | 1 failed, 210 passed in 0.47s
KILLED   T128 bare body part off | 1 failed, 223 passed in 1.04s
SURVIVED T128 bare body part: drop 'summary has >1 word' check | 259 passed in 1.07s
KILLED   T128 bare body part: any noun not only body | 1 failed, 75 passed in 0.33s
KILLED   T128 connector: remove 'which' | 1 failed, 226 passed in 1.03s
KILLED   T128 connector: remove 'including' | 1 failed, 227 passed in 1.02s
KILLED   T128 connector: remove 'was' | 1 failed, 229 passed in 1.03s
KILLED   T128 connector: remove 'due' | 1 failed, 225 passed in 1.06s
SURVIVED T128 connector: remove 'also' | 259 passed in 1.05s
SURVIVED T128 connector: remove 'however' | 259 passed in 1.05s
SURVIVED T128 connector: remove 'consistent' | 259 passed in 1.12s
KILLED   T129 sort unsplit last off | 1 failed, 48 passed in 0.18s
KILLED   T129 preamble flag never set | 1 failed, 48 passed in 0.17s
KILLED   T129 preamble: e <= first_real -> True always | 1 failed, 55 passed in 0.17s
KILLED   T129 first = block start not field start | 1 failed, 48 passed in 0.17s
KILLED   T129 preamble kept? drop unsplit (D-027) | 1 failed, 33 passed in 0.16s
KILLED   T127 record_seq not stored | 1 failed in 0.91s
KILLED   T127 gap_changes not in event | 1 failed in 0.85s
SURVIVED T127 days check dropped | 4 passed in 1.27s
SURVIVED T127 from/to check dropped | 4 passed in 1.55s
SURVIVED T127 new_to check dropped only | 4 passed in 1.28s
SURVIVED T127 removed pop on re-add dropped | 4 passed in 2.40s
SURVIVED T127 removed does not clear latest | 4 passed in 1.28s
KILLED   T127 removed list ignores current | 1 failed, 2 passed in 1.02s
KILLED   T127 later event does not replace (first wins) | 1 failed, 1 passed in 0.92s
KILLED   T127 gap_changes_removed not in case_view | 1 failed in 0.95s
KILLED   T127 gap_change not set on flag | 1 failed in 0.88s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:41:57.066Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; tail -5 $S/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:41:57.145Z

**tool result**
````
........................................................................ [ 89%]
........................................................................ [ 91%]
........................................................................ [ 94%]
........................................................................ [ 96%]
..............................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:02.880Z

**tool call — Bash**
````
{
 "command": "grep -n \"unsplit\" app/backend/pipeline.py app/backend/present.py app/backend/store.py app/db/*.py | head; grep -n \"def record_view\" -A14 app/backend/present.py; grep -n \"def load_records\" -A30 app/backend/store.py | head -50; grep -n \"unsplit\\|preamble\" memory/contracts/api.md | head"
}
````

### User / tool · 2026-11-02T11:42:02.999Z

**tool result**
````
app/backend/pipeline.py:51:    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
208:def record_view(r, raw, with_sentences=True, pages=None):
209-    block = raw[r["char_start"]:r["char_end"]]
210-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
211-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
212-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
213-         "char_end": r["char_end"], "text": block, "language": language.block_lang(block)}
214-    if pages:                                    # PDF source (D-031): the page where the record starts
215-        v["page"] = pdf_text.page_for(pages, r["char_start"])
216-        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
217-        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
218-    if with_sentences:
219-        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
220-        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
221-        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in units]
222-        if why_none:
14:def load_records(conn, case_id: str, raw: str = None) -> list:
15-    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
16-    if raw is None:
17-        raw = DB.get_case(conn, case_id)["raw_text"]
18-    out = []
19-    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
20-        d = DB._decode(r)
21-        block = raw[d["char_start"]:d["char_end"]]
22-        try:
23-            body = ingest.split_records(block)[0]["excerpt"]
24-        except Exception:
25-            body = block
26-        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
27-                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
28-    return out
29-
30-
31-def _by_id(records):
32-    return {r["id"]: r for r in records}
33-
34-
35-# ---------------------------------------------------------------- unit dicts for export / totals
36-def export_case(conn, case_id: str) -> dict:
37-    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
38-    case = DB.get_case(conn, case_id)
39-    recs = load_records(conn, case_id, case["raw_text"])
40-    n_of = {r["id"]: r["n"] for r in recs}
41-    rec_of = {r["id"]: r for r in recs}
42-    from app.backend import review as review_mod        # lazy: review imports store
43-    ents = []
44-    for e in DB.list_items(conn, case_id, "entry"):
76:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:10.128Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_t114_rates_and_demo_judges.py; tail -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:42:10.220Z

**tool result**
````
"""T-114 (T-060 pass 1 F3/F4): a rate is acknowledged, never offered as a letter accept that later blocks export (D-019/D-042, accept needs no judge);
every acceptable item on every demo library packet has its judge fixture (no JUDGE_NOT_RUN dead end); confirm_date reports which gap figures moved.
Fixture backend, no network."""
import os
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace
from app.backend.api import create_app, library_cases
from app.db import db as DB

LIB09 = "case_lib09_spanish_interpreter_espalda"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    path = str(tmp_path / "t114.sqlite")
    return TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), path


def _load(c, lib_id):
    tok = c.post("/api/cases", json={"library": lib_id}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready", lib_id
    return tok


def _gate(c, tok):
    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"]}["export_gate"]


def _blank_judge(conn, tok, item_id):
    row = DB.get_item(conn, item_id, tok)
    lad = row["ladder"]
    lad["judge"] = None
    DB.update_item(conn, item_id, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, item_id))


# ------------------------------------------------------------ 1. a rate is acknowledged, not a letter accept
def test_a_rate_accepted_without_a_judge_does_not_block_export_but_a_charge_still_does(client):
    c, path = client
    tok = _load(c, LIB09)
    conn = DB.connect(path)
    amounts = {a["id"]: a for a in c.get(f"/api/cases/{tok}").json()["amounts"]}
    rates = [i for i, a in amounts.items() if a["kind"] == "rate"]
    charge = next(i for i, a in amounts.items() if a["kind"] == "charge")
    assert rates
    for i in rates:
........................................................................ [ 96%]
........................................................................ [ 98%]
.................................                                        [100%]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:13.446Z

**tool call — Bash**
````
{
 "command": "sleep 20; tail -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:42:33.536Z

**tool result**
````
........................................................................ [ 96%]
........................................................................ [ 98%]
.................................                                        [100%]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:39.445Z

**tool call — Bash**
````
{
 "command": "ps aux | grep \"pytest tests/unit\" | grep -v grep | head -3; wc -l /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/unit_full.txt; grep -c \"F\\|E\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/unit_full.txt"
}
````

### User / tool · 2026-11-02T11:42:39.615Z

**tool result**
````
      43 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/unit_full.txt
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:43.893Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1 && python3 -c \"\nt=open('unit_full.txt').read()\nbody=''.join(l.split(' [')[0] for l in t.splitlines())\nprint(len(body), body.count('.'), body.count('s'), body.count('F'), body.count('E'))\""
}
````

### User / tool · 2026-11-02T11:42:43.994Z

**tool result**
````
3096 3053 4 0 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:49.818Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/repo && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit --co -q -p no:cacheprovider 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T11:42:52.342Z

**tool result**
````
3057 tests collected in 2.15s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:01.053Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/api129.py <<'EOF'\nimport sys, os, tempfile, json\nroot, label = sys.argv[1], sys.argv[2]\nsys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\",\"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(); path = d + \"/t.sqlite\"\nc = TestClient(create_app(path, static_dir=d), client=(\"127.0.0.1\", 50000))\nR1='Date: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Patient completed intake paperwork.\"'\nR2='Date: 2026-01-16\\nSource: Lakeside Clinic, initial evaluation\\nExcerpt: \"Seen for neck pain.\"'\nfor name, text in {\"preamble\": \"FAX COVER SHEET\\nTo: Dr X\\n---\\n\"+R1+\"\\n---\\n\"+R2, \"midnote\": R1+\"\\n---\\nfree text between\\n---\\n\"+R2}.items():\n    r = c.post(\"/api/cases\", json={\"text\": text})\n    j = r.json(); tok = j[\"token\"]\n    print(label, name, r.status_code, \"POST records:\", [{k: x.get(k) for k in (\"id\",\"seq\",\"n\",\"unsplit\",\"preamble\")} for x in j.get(\"records\", [])])\n    g = c.get(f\"/api/cases/{tok}\").json()\n    print(label, name, \"GET records:\", [{k: x.get(k) for k in (\"id\",\"seq\",\"unsplit\",\"preamble\",\"char_start\")} for x in g[\"records\"]], \"undated:\", [(e[\"id\"], e[\"record_ids\"]) for e in g[\"undated_entries\"]])\nEOF\nfor d in parent repo; do .venv/bin/python -I $S/scripts/api129.py $S/$d $d 2>&1 | tail -8; done"
}
````

### User / tool · 2026-11-02T11:43:01.985Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py", line 14, in <module>
    j = r.json(); tok = j["token"]
                        ~^^^^^^^^^
KeyError: 'token'
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py", line 14, in <module>
    j = r.json(); tok = j["token"]
                        ~^^^^^^^^^
KeyError: 'token'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:03.373Z

**tool call — Bash**
````
{
 "command": "grep -n '\"/api/cases\"' -B2 -A25 app/backend/api.py | head -70"
}
````

### User / tool · 2026-11-02T11:43:03.463Z

**tool result**
````
216-                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
217-
218:    @app.get("/api/cases")
219-    def list_cases():
220-        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
221-            raise ApiError(404, "not_found", "Not found.")
222-        c = conn()
223-        try:
224-            return {"cases": present.case_list(c)}
225-        finally:
226-            c.close()
227-
228-    @app.get("/api/library")
229-    def library():
230-        if not local_mode():
231-            raise ApiError(404, "not_found", "Not found.")
232-        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
233-
234:    @app.post("/api/cases", status_code=201)
235-    async def create_case(request: Request):
236-        b = await body_of(request)
237-        sample = b.get("sample") is True
238-        lib = None
239-        if isinstance(b.get("library"), str):
240-            if not local_mode():
241-                raise ApiError(404, "not_found", "Not found.")
242-            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
243-            if lib is None:
244-                raise ApiError(404, "not_found", "No such library case.")
245-        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
246-        if not isinstance(text, str):
247-            raise ApiError(400, "bad_request", "Provide text or sample: true.")
248-        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
249-
250-    @app.post("/api/cases/pdf", status_code=201)
251-    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
252-        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
253-        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
254-        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
255-            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
256-        cl = request.headers.get("content-length")
257-        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
258-            raise ApiError(413, "input_too_large", "The PDF is too large.")
259-        data = b""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:08.037Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; sed -i 's/j = r.json(); tok = j\\[\"token\"\\]/j = r.json(); print(r.status_code, str(j)[:200]) if \"token\" not in j else None; tok = j[\"token\"]/' $S/scripts/api129.py; .venv/bin/python -I $S/scripts/api129.py $S/repo repo 2>&1 | head -5; grep -n \"def make_case\" -A25 app/backend/api.py | head -50"
}
````

### User / tool · 2026-11-02T11:43:08.504Z

**tool result**
````
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py'
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py", line 14, in <module>
    j = r.json(); tok = j["token"]
                        ~^^^^^^^^^
KeyError: 'token'
282:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
283-        try:
284-            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
285-        except ingest.IngestError as e:
286-            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
287-        if demo_mode() and digest(text) not in allowed_hashes():
288-            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
289-        c = conn()
290-        try:
291-            now = time.time()
292-            DB.purge_expired(c, now)
293-            name = name if isinstance(name, str) else ("Sample case" if sample else None)
294-            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
295-                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
296-                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
297-            try:
298-                ing = pipeline_mod().ingest_case(c, cid, text, now)
299-                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
300-                flags = DB.list_items(c, cid, "flag")
301-            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
302-                DB.delete_case(c, cid)
303-                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
304-                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, *language.api_fields(e)) from None
305-                log.error("create failed %s", type(e).__name__)
306-                raise ApiError(500, "internal", "Something went wrong.") from None
307-            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:16.848Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/api129.py <<'EOF'\nimport sys, os, tempfile, json\nroot, label = sys.argv[1], sys.argv[2]\nsys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\",\"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom app.db import db as DB\nfrom app.backend import pipeline, present\nd = tempfile.mkdtemp(); path = d + \"/t.sqlite\"\nconn = DB.connect(path)\nR1='Date: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Patient completed intake paperwork.\"'\nR2='Date: 2026-01-16\\nSource: Lakeside Clinic, initial evaluation\\nExcerpt: \"Seen for neck pain.\"'\nfor name, text in {\"preamble\": \"FAX COVER SHEET\\nTo: Dr X\\n---\\n\"+R1+\"\\n---\\n\"+R2, \"midnote\": R1+\"\\n---\\nfree text between\\n---\\n\"+R2}.items():\n    cid = DB.create_case(conn, text, now=1.0, name=name, source=\"paste\", backend=\"fixture\", demo_mode=0)\n    ing = pipeline.ingest_case(conn, cid, text, 1.0)\n    recs = [present.record_view(r, text, with_sentences=False) for r in present._recs_by_id(conn, cid).values()]\n    print(label, name, \"record_view keys:\", sorted(recs[0].keys()))\n    print(label, name, [(r[\"id\"], r[\"seq\"], r[\"char_start\"], r.get(\"unsplit\"), r.get(\"preamble\"), r[\"text\"][:18].replace(\"\\n\",\"|\")) for r in sorted(recs, key=lambda r: r[\"seq\"])])\n    print(label, name, \"flags:\", [(f[\"id\"], f[\"category\"], f[\"record_ids\"]) for f in DB.list_items(conn, cid, \"flag\")])\nEOF\nfor d in parent repo; do .venv/bin/python -I $S/scripts/api129.py $S/$d $d 2>&1 | tail -9; done"
}
````

### User / tool · 2026-11-02T11:43:17.392Z

**tool result**
````
parent preamble record_view keys: ['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'id', 'injection_tag', 'language', 'seq', 'source_label', 'text']
parent preamble [('r1', 1, 0, None, None, 'FAX COVER SHEET|To'), ('r2', 2, 28, None, None, '|Date: 2026-01-09|'), ('r3', 3, 133, None, None, '|Date: 2026-01-16|')]
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py", line 18, in <module>
    print(label, name, "flags:", [(f["id"], f["category"], f["record_ids"]) for f in DB.list_items(conn, cid, "flag")])
                                                           ~^^^^^^^^^^^^^^
KeyError: 'record_ids'
repo preamble record_view keys: ['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'id', 'injection_tag', 'language', 'seq', 'source_label', 'text']
repo preamble [('r1', 1, 28, None, None, '|Date: 2026-01-09|'), ('r2', 2, 133, None, None, '|Date: 2026-01-16|'), ('r3', 3, 0, None, None, 'FAX COVER SHEET|To')]
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/api129.py", line 18, in <module>
    print(label, name, "flags:", [(f["id"], f["category"], f["record_ids"]) for f in DB.list_items(conn, cid, "flag")])
                                                           ~^^^^^^^^^^^^^^
KeyError: 'record_ids'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:27.215Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _store_records\" -A25 app/backend/pipeline.py; grep -n \"def _persist\" -A22 app/backend/pipeline.py | head -50"
}
````

### User / tool · 2026-11-02T11:43:27.309Z

**tool result**
````
146:def _store_records(conn, cid: str, ing: dict) -> None:
147-    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
148-    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
149-    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
150-    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
151-    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
152-        return
153-    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
154-    try:
155-        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
156-        for r in ing["records"]:
157-            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
158-            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
159-                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
160-                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
161-                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
162-                          encounter=int(r["encounter"]))
163-        conn.execute("COMMIT")
164-    except Exception:
165-        conn.execute("ROLLBACK")
166-        raise
167-
168-
169-def _row(kind: str, it: dict) -> dict:
170-    ladder = _clean(it.get("ladder") or {})
171-    if kind == "entry":
186:def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
187-    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
188-    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
189-    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
190-    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
191-    for it in items:
192-        old = existing.get(it["id"])
193-        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
194-            from app.backend import reclassify as RC
195-            it = RC.carry_over(old, it)
196-        row = _row(kind, it)
197-        if old is None:
198-            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
199-            continue
200-        DB.update_item(conn, it["id"], now=now, case=cid, **row)
201-        if kind == "flag" and old["review_status"] != "pending":
202-            oc = old.get("computed") or {}
203-            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
204-                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
205-            else:
206-                it["review_status"] = old["review_status"]
207-        elif old["review_status"] != "pending":
208-            it["review_status"] = old["review_status"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:33.296Z

**tool call — Bash**
````
{
 "command": "grep -n \"RETENTION_SECONDS *=\" app/db/db.py; grep -rn \"unsplit\\|preamble\\|UNSPLIT\" tests/unit/*.py tests/e2e 2>/dev/null | grep -v \"test_ingest.py\" | cut -c1-150 | head -12; grep -rln \"UNSPLIT_TEXT\\|unsplit\" evals/golden evals/library evals/*.py tests/fixtures 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T11:43:33.430Z

**tool result**
````
17:RETENTION_SECONDS = 24 * 3600
tests/unit/test_eval_runner.py:14:UNSPLIT = (R.GOLD / "unsplit_paste.txt").read_text()
tests/unit/test_eval_runner.py:15:USPLIT = json.loads((R.GOLD / "unsplit_paste.split.json").read_text())
tests/unit/test_eval_runner.py:22:        if text == UNSPLIT:
tests/unit/test_eval_runner.py:23:            return self.unsplit(backend)
tests/unit/test_eval_runner.py:58:    def unsplit(self, backend):
tests/unit/test_eval_runner.py:63:            self.mutate("unsplit_paste", out, self)
tests/unit/test_eval_runner.py:343:def test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4():
tests/unit/test_eval_runner.py:344:    """T-057 minor / D-031: unsplit_paste is part of the scored set: 3 code-parsed records, one LLM_SPLIT record_wa
tests/unit/test_eval_runner.py:346:    assert ok["metrics"]["unsplit_paste"]["value"] is True and ok["ship_bar_met"] is True
tests/unit/test_eval_runner.py:348:        if n == "unsplit_paste":
tests/unit/test_eval_runner.py:351:    assert bad["metrics"]["unsplit_paste"]["value"] is False and "record 1 has 0 LLM_SPLIT warnings, want 1" in bad
tests/unit/test_eval_runner.py:354:def test_unsplit_paste_wrong_date_or_one_record_fails():
evals/golden/unsplit_paste.split.json
evals/run.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:45.450Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/ov129.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nimport app.backend.ingest as I\nR1='Date: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Patient completed intake paperwork.\"'\nR2='Date: 2026-01-16\\nSource: Lakeside Clinic, initial evaluation\\nExcerpt: \"Seen for neck pain.\"'\nfor name,t in {\"no-sep preamble\":\"Cover note from firm\\n\"+R1+\"\\n\\n\"+R2, \"blank-line preamble (no ---)\":\"Cover note\\n\\n\"+R1+\"\\n\\n\"+R2,\n  \"hdr preamble\":\"cover\\n=== Record 1 ===\\n\"+R1+\"\\n=== Record 2 ===\\n\"+R2,\n  \"preamble holds Date-like\":\"Re: Date: of loss unknown\\n---\\n\"+R1+\"\\n---\\n\"+R2,\n  \"two preambles\":\"Cover A\\n---\\nCover B\\n---\\n\"+R1+\"\\n---\\n\"+R2,\n  \"preamble then incomplete record\":\"Cover\\n---\\nDate: 2026-01-09\\nSource: X Clinic\\nSeen.\\n---\\n\"+R2}.items():\n    o=I.ingest(t)\n    print(name, [(r[\"n\"], r[\"char_start\"], r[\"char_end\"], r[\"unsplit\"], r[\"preamble\"], r[\"text\"][:12].replace(\"\\n\",\"|\")) for r in o[\"records\"]])\n    spans=sorted((r[\"char_start\"], r[\"char_end\"], r[\"n\"]) for r in o[\"records\"])\n    ov=[(a,b) for a,b in zip(spans, spans[1:]) if a[1]>b[0]]\n    print(\"   overlaps:\", ov)\nEOF\nfor d in parent repo; do echo == $d; .venv/bin/python -I $S/scripts/ov129.py $S/$d; done"
}
````

### User / tool · 2026-11-02T11:43:45.744Z

**tool result**
````
== parent
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/ov129.py", line 12, in <module>
    print(name, [(r["n"], r["char_start"], r["char_end"], r["unsplit"], r["preamble"], r["text"][:12].replace("\n","|")) for r in o["records"]])
                                                                        ~^^^^^^^^^^^^
KeyError: 'preamble'
== repo
no-sep preamble [(1, 21, 121, False, False, 'Date: 2026-0'), (2, 123, 214, False, False, 'Date: 2026-0'), (3, 0, 20, True, True, 'Cover note f')]
   overlaps: []
blank-line preamble (no ---) [(1, 12, 112, False, False, 'Date: 2026-0'), (2, 114, 205, False, False, 'Date: 2026-0'), (3, 0, 10, True, True, 'Cover note')]
   overlaps: []
hdr preamble [(1, 6, 123, False, False, '=== Record 1'), (2, 124, 232, False, False, '=== Record 2'), (3, 0, 5, True, True, 'cover')]
   overlaps: []
preamble holds Date-like [(1, 29, 130, False, False, '|Date: 2026-'), (2, 134, 226, False, False, '|Date: 2026-'), (3, 0, 25, True, True, 'Re: Date: of')]
   overlaps: []
two preambles [(1, 23, 124, False, False, '|Date: 2026-'), (2, 128, 220, False, False, '|Date: 2026-'), (3, 0, 7, True, True, 'Cover A'), (4, 12, 19, True, True, 'Cover B')]
   overlaps: []
preamble then incomplete record [(1, 9, 43, False, False, '|Date: 2026-'), (2, 53, 145, False, False, '|Date: 2026-'), (3, 0, 5, True, True, 'Cover'), (4, 44, 49, True, False, 'Seen.')]
   overlaps: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:43:55.798Z

**tool call — Bash**
````
{
 "command": "grep -rn \"UNSPLIT\\|unsplit\\|preamble\" app/frontend/*.js app/frontend/*.html | cut -c1-200 | head; grep -n \"warnings\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T11:43:55.901Z

**tool result**
````
312:                    "warnings": ing["warnings"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:01.751Z

**tool call — Bash**
````
{
 "command": "grep -n \"@app\\.\\(get\\|post\\|patch\\|put\\|delete\\)\" app/backend/api.py | cut -c1-120 | head -40; grep -n \"gap_change\" memory/contracts/api.md | cut -c1-80 | head"
}
````

### User / tool · 2026-11-02T11:44:01.851Z

**tool result**
````
212:    @app.get("/api/health")
218:    @app.get("/api/cases")
228:    @app.get("/api/library")
234:    @app.post("/api/cases", status_code=201)
250:    @app.post("/api/cases/pdf", status_code=201)
316:    @app.get("/api/cases/{token}")
325:    @app.delete("/api/cases/{token}", status_code=204)
349:    @app.post("/api/cases/{token}/run", status_code=202)
372:    @app.post("/api/cases/{token}/rejudge")
394:    @app.get("/api/cases/{token}/status")
413:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
425:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
436:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
449:    @app.get("/api/cases/{token}/narrative")
458:    @app.post("/api/cases/{token}/narrative")
471:    @app.post("/api/cases/{token}/narrative/review")
486:    @app.get("/api/cases/{token}/items/{item_id}")
498:    @app.post("/api/cases/{token}/items/{item_id}/review")
519:    @app.get("/api/cases/{token}/export")
548:    @app.get("/api/cases/{token}/items/{item_id}/trace")
561:    @app.get("/api/cases/{token}/trace")
570:    @app.get("/api/cases/{token}/judges")
579:    @app.get("/api/cases/{token}/audit")
262:**T-116 / D-055 (rounds 3 and 4): gap math runs over EVERY dated record, wha
268:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:13.591Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/probe127.py <<'EOF'\nimport sys, os, tempfile, json, time\nroot = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\",\"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(); path = d + \"/t.sqlite\"\nc = TestClient(create_app(path, static_dir=d), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"library\": \"case_lib09_spanish_interpreter_espalda\"}).json()[\"token\"]\nc.post(f\"/api/cases/{tok}/run\", json={})\nfor _ in range(480):\n    if c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] in (\"ready\",\"failed\",\"done_with_errors\"): break\n    time.sleep(0.25)\ng = c.get(f\"/api/cases/{tok}\").json()\nprint(\"status\", g[\"status\"], \"dates_to_confirm\", [(x[\"record_id\"], x[\"candidates\"]) for x in g[\"dates_to_confirm\"]])\ngap = lambda g: [(f[\"id\"], f[\"computed\"].get(\"days\"), f.get(\"gap_change\") and (f[\"gap_change\"][\"old_days\"], f[\"gap_change\"][\"new_days\"], f[\"gap_change\"][\"record_seq\"])) for f in g[\"flags\"] if f[\"type\"]==\"gap\"]\nprint(\"before\", gap(g), \"removed\", g[\"gap_changes_removed\"])\namb = [x for x in g[\"dates_to_confirm\"]]\nx = amb[0]\nr = c.post(f\"/api/cases/{tok}/records/{x['record_id']}/confirm_date\", json={\"date\": x[\"candidates\"][-1]})\nprint(\"confirm 1\", r.status_code, [ (ch[\"flag_id\"], ch[\"change\"], ch[\"old_days\"], ch[\"new_days\"]) for ch in r.json().get(\"gap_changes\", [])])\ng1 = c.get(f\"/api/cases/{tok}\").json(); print(\"after1\", gap(g1), g1[\"gap_changes_removed\"])\n# undo (reset) of gap review\nfor f in g1[\"flags\"]:\n    if f[\"type\"]==\"gap\":\n        a = c.post(f\"/api/cases/{tok}/items/{f['id']}/review\", json={\"action\":\"accept\"}); \n        u = c.post(f\"/api/cases/{tok}/items/{f['id']}/review\", json={\"action\":\"reset\"})\n        print(\"accept\", a.status_code, \"reset\", u.status_code)\ng2 = c.get(f\"/api/cases/{tok}\").json(); print(\"after reset\", gap(g2))\nitem = [f for f in g2[\"flags\"] if f[\"type\"]==\"gap\"]\nif item:\n    it = c.get(f\"/api/cases/{tok}/items/{item[0]['id']}\").json(); print(\"item GET gap_change:\", it.get(\"gap_change\") and it[\"gap_change\"][\"sentence\"])\n# re-confirm same record\nr = c.post(f\"/api/cases/{tok}/records/{x['record_id']}/confirm_date\", json={\"date\": x[\"candidates\"][0]}); print(\"re-confirm\", r.status_code, r.json().get(\"error\", r.json()).get(\"code\") if isinstance(r.json(), dict) else \"\")\nfor y in amb[1:]:\n    r = c.post(f\"/api/cases/{tok}/records/{y['record_id']}/confirm_date\", json={\"date\": y[\"candidates\"][0]})\n    print(\"confirm other\", y[\"record_id\"], r.status_code, [(ch[\"flag_id\"], ch[\"change\"], ch[\"old_days\"], ch[\"new_days\"]) for ch in r.json().get(\"gap_changes\", [])])\ng3 = c.get(f\"/api/cases/{tok}\").json(); print(\"after other\", gap(g3), \"removed\", [(r[\"flag_id\"], r[\"sentence\"]) for r in g3[\"gap_changes_removed\"]])\na = json.dumps(c.get(f\"/api/cases/{tok}\").json(), sort_keys=True); b = json.dumps(c.get(f\"/api/cases/{tok}\").json(), sort_keys=True)\nc2 = TestClient(create_app(path, static_dir=d), client=(\"127.0.0.1\", 50000)); e = json.dumps(c2.get(f\"/api/cases/{tok}\").json(), sort_keys=True)\nvol = lambda s: json.loads(s); \ndef strip(j):\n    j.pop(\"updated_at\", None); return j\nprint(\"GET twice equal:\", a == b, \"| fresh app equal:\", a == e)\nprint(\"keys: top has gap_changes_removed:\", \"gap_changes_removed\" in g3, \"| non-gap flags have gap_change key:\", [(\"gap_change\" in f) for f in g3[\"flags\"] if f[\"type\"]!=\"gap\"][:3])\nEOF\n.venv/bin/python -I $S/scripts/probe127.py $S/repo 2>&1 | tail -20",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:44:14.618Z

**tool result**
````
status ready dates_to_confirm [('r4', ['2026-03-05', '2026-05-03'])]
before [('f_gap_r1_r2', 42, None)] removed []
confirm 1 200 []
after1 [('f_gap_r1_r2', 42, None)] []
accept 200 reset 200
after reset [('f_gap_r1_r2', 42, None)]
item GET gap_change: None
re-confirm 422 invalid_edit
after other [('f_gap_r1_r2', 42, None)] removed []
GET twice equal: True | fresh app equal: True
keys: top has gap_changes_removed: True | non-gap flags have gap_change key: [False, False, False]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:19.784Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; sed -i 's/\"date\": x\\[\"candidates\"\\]\\[-1\\]/\"date\": x[\"candidates\"][0]/' $S/scripts/probe127.py; .venv/bin/python -I $S/scripts/probe127.py $S/repo 2>&1 | tail -14",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:44:20.814Z

**tool result**
````
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1/scripts/probe127.py'
status ready dates_to_confirm [('r4', ['2026-03-05', '2026-05-03'])]
before [('f_gap_r1_r2', 42, None)] removed []
confirm 1 200 []
after1 [('f_gap_r1_r2', 42, None)] []
accept 200 reset 200
after reset [('f_gap_r1_r2', 42, None)]
item GET gap_change: None
re-confirm 422 invalid_edit
after other [('f_gap_r1_r2', 42, None)] removed []
GET twice equal: True | fresh app equal: True
keys: top has gap_changes_removed: True | non-gap flags have gap_change key: [False, False, False]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:25.771Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; python3 - \"$S/scripts/probe127.py\" <<'EOF'\nimport sys; p=sys.argv[1]; s=open(p).read().replace('\"date\": x[\"candidates\"][-1]','\"date\": x[\"candidates\"][0]'); open(p,\"w\").write(s)\nEOF\n.venv/bin/python -I $S/scripts/probe127.py $S/repo 2>&1 | tail -14",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:44:26.781Z

**tool result**
````
status ready dates_to_confirm [('r4', ['2026-03-05', '2026-05-03'])]
before [('f_gap_r1_r2', 42, None)] removed []
confirm 1 200 [('f_gap_r4_r2', 'changed', 42, 40)]
after1 [('f_gap_r4_r2', 40, (42, 40, 4))] []
accept 200 reset 200
after reset [('f_gap_r4_r2', 40, (42, 40, 4))]
item GET gap_change: None
re-confirm 422 invalid_edit
after other [('f_gap_r4_r2', 40, (42, 40, 4))] removed []
GET twice equal: True | fresh app equal: True
keys: top has gap_changes_removed: True | non-gap flags have gap_change key: [False, False, False]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:28.968Z

**tool call — Bash**
````
{
 "command": "sed -n 486,520p app/backend/api.py"
}
````

### User / tool · 2026-11-02T11:44:29.056Z

**tool result**
````
    @app.get("/api/cases/{token}/items/{item_id}")
    def item(token: str, item_id: str):
        c = conn()
        try:
            get_case(c, token)
            try:
                return present.why_view(c, token, item_id)
            except (KeyError, IndexError):
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()

    @app.post("/api/cases/{token}/items/{item_id}/review")
    async def review_item(token: str, item_id: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
        finally:
            c.close()

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
    from app.backend import billing
    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
    from app.backend import pdf_routes
    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
    from app.backend import reclassify
    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
    from app.backend import calibration_route
    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)

    @app.get("/api/cases/{token}/export")
    def export(token: str, style: str = None):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:31.457Z

**tool call — Bash**
````
{
 "command": "grep -n \"item_view(\" app/backend/*.py | head; grep -n \"def why_view\" -A12 app/backend/present.py | head -24; sed -n 170,191p app/backend/review.py"
}
````

### User / tool · 2026-11-02T11:44:31.577Z

**tool result**
````
app/backend/present.py:149:def item_view(conn, case_id, item_id):
app/backend/present.py:314:    item = item_view(conn, case_id, item_id)
app/backend/review.py:188:    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
app/backend/review.py:520:    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
app/backend/review.py:584:    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
app/backend/reclassify.py:185:    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
313:def why_view(conn, case_id, item_id):
314-    item = item_view(conn, case_id, item_id)
315-    recs = _recs_by_id(conn, case_id)
316-    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
317-    seen, src = set(), []
318-    for rid in ids:
319-        if rid in recs and rid not in seen:
320-            seen.add(rid)
321-            r = recs[rid]
322-            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
323-            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
324-    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
325-    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:44:37.748Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; python3 - \"$S/scripts/probe127.py\" <<'EOF'\nimport sys; p=sys.argv[1]; s=open(p).read()\ns=s.replace('print(\"item GET gap_change:\", it.get(\"gap_change\") and it[\"gap_change\"][\"sentence\"])','print(\"item GET keys:\", list(it)[:6]); print(\"item GET gap_change:\", (it.get(\"item\") or it).get(\"gap_change\") and (it.get(\"item\") or it)[\"gap_change\"][\"sentence\"])')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -I $S/scripts/probe127.py $S/repo 2>&1 | grep \"item GET\"; grep -n \"gap_change\\|items/{\" memory/contracts/api.md | cut -c1-110 | head",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:44:38.827Z

**tool result**
````
item GET keys: ['item', 'source', 'calls', 'events']
item GET gap_change: Gap recalculated after you confirmed record 4: now 40 days (was 42).
27:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry:
30:| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
31:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `
36:| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted
262:**T-116 / D-055 (rounds 3 and 4): gap math runs over EVERY dated record, whatever ingest called it; paperw
268:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change
297:## GET /api/cases/{token}/items/{item_id}  — "Why?"
315:## POST /api/cases/{token}/items/{item_id}/review
347:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:45:01.325Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/probe127b.py <<'EOF'\nimport sys, os, tempfile, json\nroot = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfrom app.db import db as DB\nfrom app.backend import pipeline, present, review\nd = tempfile.mkdtemp(); conn = DB.connect(d + \"/t.sqlite\")\ndef rec(date, src, ex): return f'Date: {date}\\nSource: {src}\\nExcerpt: \"{ex}\"'\ntext = \"\\n---\\n\".join([rec(\"2026-01-20\",\"Lakeside Clinic, initial evaluation\",\"Seen for neck pain.\"), rec(\"02/03/2026\",\"Lakeside Clinic, follow-up\",\"Neck pain improving.\"), rec(\"2026-03-05\",\"Lakeside Clinic, discharge\",\"Discharged.\")])\ncid = DB.create_case(conn, text, now=1.0, name=\"x\", source=\"paste\", backend=\"fixture\", demo_mode=0)\npipeline.ingest_case(conn, cid, text, 1.0)\ndef gaps(): return [(f[\"id\"], f[\"computed\"].get(\"days\"), (f.get(\"gap_change\") or {}).get(\"sentence\")) for f in present.all_items(conn, cid)[\"flag\"] if f[\"type\"]==\"gap\"]\nprint(\"before\", gaps())\nout = review.confirm_date(conn, cid, \"r2\", \"2026-02-03\", now=2.0)\nprint(\"changes\", [(c[\"change\"], c[\"flag_id\"], c[\"sentence\"]) for c in out[\"gap_changes\"]])\nit = present.all_items(conn, cid)\nprint(\"after gaps\", gaps(), \"| removed:\", [(r[\"flag_id\"], r[\"sentence\"]) for r in it[\"gap_changes_removed\"]])\nev = [e for e in DB.list_events(conn, cid) if e[\"action\"]==\"confirm_date\"]; print(\"events\", len(ev), ev[-1][\"after\"][\"gap_changes\"][0][\"change\"])\nEOF\n.venv/bin/python -I $S/scripts/probe127b.py $S/repo 2>&1 | tail -8",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T11:45:01.689Z

**tool result**
````
before [('f_gap_r1_r3', 44, None)]
changes [('removed', 'f_gap_r1_r3', 'A gap of 44 days no longer applies after you confirmed the date of record 2.')]
after gaps [] | removed: [('f_gap_r1_r3', 'A gap of 44 days no longer applies after you confirmed the date of record 2.')]
events 1 removed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:45:07.211Z

**tool call — Bash**
````
{
 "command": "grep -n \"_ABBR\" app/backend/summary_trim.py | head -20"
}
````

### User / tool · 2026-11-02T11:45:07.299Z

**tool result**
````
47:_ABBR_BEFORE_PERIOD = frozenset({"dr", "mr", "mrs", "ms", "st", "jr", "sr", "vs", "approx", "e.g", "i.e", "etc", "no", "dept", "inc", "ref", "fig", "cf", "est"})
95:_ABBR_CASE = {"US": "ultrasound", "IM": "intramuscular injection", "OA": "osteoarthritis", "RA": "rheumatoid arthritis", "LE": "lower extremity leg",
97:_ABBR = {"lac": "laceration", "lacs": "laceration", "djd": "degenerative joint disease", "esi": "epidural steroid injection", "tpi": "trigger point injection",
103:_ABBR_RX = re.compile(r"(?<![a-z0-9/])(" + "|".join(sorted((re.escape(k) for k in _ABBR), key=len, reverse=True)) + r")(?![a-z0-9/])")
104:_ABBR_CASE_RX = re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(_ABBR_CASE) + r")(?![A-Za-z0-9/])")
109:    t = _ABBR_CASE_RX.sub(lambda m: _ABBR_CASE[m.group(1)], text)
114:    return _ABBR_RX.sub(lambda m: _ABBR[m.group(1)], t)
181:            if tail.strip(".") in _ABBR_BEFORE_PERIOD or len(tail) == 1:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:45:15.535Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/sweep.py <<'EOF'\nimport sys, os, re, subprocess, json\nroot = sys.argv[1]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nsys.path.insert(0, root); os.chdir(root)\nimport app.backend.summary_trim as T\nkeys = [(\"c\", k) for k in T._ABBR_CASE] + [(\"l\", k) for k in T._ABBR]\nprint(len(keys), \"entries\")\nif len(sys.argv) > 2:\n    kind, key = sys.argv[2], sys.argv[3]\n    import pytest\n    if kind == \"c\":\n        T._ABBR_CASE[key] = \"zzqx\"\n        T._ABBR_CASE_RX = re.compile(r\"(?<![A-Za-z0-9/])(\" + \"|\".join(T._ABBR_CASE) + r\")(?![A-Za-z0-9/])\")\n    else:\n        T._ABBR[key] = \"zzqx\"\n    sys.exit(pytest.main([\"tests/unit/test_summary_trim.py\", \"-q\", \"-x\", \"-p\", \"no:cacheprovider\", \"--no-header\"]))\nsurv = []\nfor kind, key in keys:\n    r = subprocess.run([PY, \"-I\", sys.argv[0], root, kind, key], capture_output=True, text=True, cwd=root)\n    if r.returncode == 0:\n        surv.append(key)\nprint(\"survivors:\", surv)\nEOF\n.venv/bin/python -I $S/scripts/sweep.py $S/mut 2>&1 | tail -4",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:45:38.248Z

**tool result**
````
30 entries
survivors: ['IV', 'orif', 'hep', 'ekg']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:45:46.410Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; sed -n 95,102p app/backend/summary_trim.py | cut -c1-400; cat > $S/scripts/entries.py <<'EOF'\nimport sys; sys.path.insert(0, sys.argv[1])\nimport app.backend.summary_trim as T\npairs = [(\"Open reduction internal fixation of wrist.\", \"ORIF wrist.\"), (\"ORIF wrist.\",\"Open reduction internal fixation of wrist.\"), (\"Hip fracture repair with plate and screws.\",\"ORIF hip.\"),\n (\"Intravenous fluids given.\",\"IV fluids given.\"), (\"IV fluids given.\",\"Intravenous fluids given.\"), (\"Electrocardiogram done.\",\"EKG done.\"), (\"EKG done.\",\"Electrocardiogram done.\"),\n (\"Home exercise program given.\",\"HEP given.\"), (\"HEP given.\",\"Home exercise program given.\"), (\"ECG done.\",\"EKG done.\"), (\"Home exercises given.\",\"HEP.\")]\ndef run():\n    return [(s,e,T.trim(s,e)[\"changed\"]) for s,e in pairs]\nbase = run()\nfor k in (\"orif\",\"hep\",\"ekg\"): T._ABBR[k]=\"zzqx\"\nT._ABBR[\"IV\"]=\"zzqx\" if \"IV\" in T._ABBR else None\nif \"IV\" in T._ABBR_CASE: T._ABBR_CASE[\"IV\"]=\"zzqx\"\nimport re\nT._ABBR_CASE_RX = re.compile(r\"(?<![A-Za-z0-9/])(\" + \"|\".join(T._ABBR_CASE) + r\")(?![A-Za-z0-9/])\")\nmut = run()\nfor b,m in zip(base,mut):\n    print(\"DIFF\" if b[2]!=m[2] else \"same\", b[0],\"|\",b[1], \"base changed:\",b[2],\"mut changed:\",m[2])\nEOF\n.venv/bin/python -I $S/scripts/entries.py $S/mut"
}
````

### User / tool · 2026-11-02T11:45:46.543Z

**tool result**
````
_ABBR_CASE = {"US": "ultrasound", "IM": "intramuscular injection", "OA": "osteoarthritis", "RA": "rheumatoid arthritis", "LE": "lower extremity leg",
              "UE": "upper extremity arm", "IV": "intravenous"}
_ABBR = {"lac": "laceration", "lacs": "laceration", "djd": "degenerative joint disease", "esi": "epidural steroid injection", "tpi": "trigger point injection",
         "rcr": "rotator cuff repair surgery", "tka": "total knee arthroplasty surgery", "tha": "total hip arthroplasty surgery", "orif": "open reduction internal fixation surgery",
         "acdf": "anterior cervical discectomy fusion surgery neck", "apap": "acetaminophen", "abx": "antibiotic", "cp": "chest pain", "cxr": "chest xray",
         "ble": "bilateral lower extremity leg", "lle": "left lower extremity leg", "rle": "right lower extremity leg",
         "bue": "bilateral upper extremity arm", "lue": "left upper extremity arm", "rue": "right upper extremity arm", "hep": "home exercise program",
         "ekg": "ecg", "u/s": "ultrasound"}
same Open reduction internal fixation of wrist. | ORIF wrist. base changed: False mut changed: False
DIFF ORIF wrist. | Open reduction internal fixation of wrist. base changed: True mut changed: False
same Hip fracture repair with plate and screws. | ORIF hip. base changed: False mut changed: False
same Intravenous fluids given. | IV fluids given. base changed: False mut changed: False
same IV fluids given. | Intravenous fluids given. base changed: False mut changed: False
same Electrocardiogram done. | EKG done. base changed: False mut changed: False
same EKG done. | Electrocardiogram done. base changed: False mut changed: False
same Home exercise program given. | HEP given. base changed: False mut changed: False
same HEP given. | Home exercise program given. base changed: False mut changed: False
same ECG done. | EKG done. base changed: False mut changed: False
same Home exercises given. | HEP. base changed: False mut changed: False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:45:58.694Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/rev.py <<'EOF'\nimport sys; sys.path.insert(0, sys.argv[1])\nimport app.backend.summary_trim as T\nP = [(\"ORIF wrist.\",\"Open reduction internal fixation of wrist.\"),(\"THA performed.\",\"Total hip arthroplasty performed.\"),(\"TKA performed.\",\"Total knee arthroplasty performed.\"),\n (\"RCR performed.\",\"Rotator cuff repair performed.\"),(\"ACDF done.\",\"Anterior cervical discectomy and fusion done.\"),(\"TPI given.\",\"Trigger point injection given.\"),\n (\"ESI given.\",\"Epidural steroid injection given.\"),(\"LLE pain.\",\"Left lower extremity pain.\"),(\"BUE numbness.\",\"Bilateral upper extremity numbness.\"),\n (\"DJD noted.\",\"Degenerative joint disease noted.\"),(\"CXR negative.\",\"Chest x-ray negative.\"),(\"Lac repaired.\",\"Laceration repaired.\"),\n (\"APAP given.\",\"Acetaminophen given.\"),(\"CP reported.\",\"Chest pain reported.\"),(\"OA noted.\",\"Osteoarthritis noted.\"),(\"RA noted.\",\"Rheumatoid arthritis noted.\"),\n (\"IM injection given.\",\"Intramuscular injection given.\"),(\"US performed.\",\"Ultrasound performed.\")]\nfor s,e in P:\n    r=T.trim(s,e); print(\"OVERTRIM\" if r[\"changed\"] else \"ok      \", repr(s),\"|\",repr(e),\"->\",repr(r[\"text\"]) if r[\"changed\"] else \"\")\nEOF\n.venv/bin/python -I $S/scripts/rev.py $S/mut"
}
````

### User / tool · 2026-11-02T11:45:58.831Z

**tool result**
````
OVERTRIM 'ORIF wrist.' | 'Open reduction internal fixation of wrist.' -> ''
ok       'THA performed.' | 'Total hip arthroplasty performed.' -> 
ok       'TKA performed.' | 'Total knee arthroplasty performed.' -> 
OVERTRIM 'RCR performed.' | 'Rotator cuff repair performed.' -> ''
ok       'ACDF done.' | 'Anterior cervical discectomy and fusion done.' -> 
ok       'TPI given.' | 'Trigger point injection given.' -> 
ok       'ESI given.' | 'Epidural steroid injection given.' -> 
ok       'LLE pain.' | 'Left lower extremity pain.' -> 
ok       'BUE numbness.' | 'Bilateral upper extremity numbness.' -> 
ok       'DJD noted.' | 'Degenerative joint disease noted.' -> 
ok       'CXR negative.' | 'Chest x-ray negative.' -> 
ok       'Lac repaired.' | 'Laceration repaired.' -> 
ok       'APAP given.' | 'Acetaminophen given.' -> 
ok       'CP reported.' | 'Chest pain reported.' -> 
ok       'OA noted.' | 'Osteoarthritis noted.' -> 
ok       'RA noted.' | 'Rheumatoid arthritis noted.' -> 
ok       'IM injection given.' | 'Intramuscular injection given.' -> 
ok       'US performed.' | 'Ultrasound performed.' ->
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:46:12.190Z

**tool call — Bash**
````
{
 "command": "grep -c \"not yet committed\" docs/LLM_VS_CODE.md; grep -n \"fragment\" docs/LLM_VS_CODE.md memory/ORCHESTRATOR_DECISIONS.md memory/contracts/api.md | cut -c1-260; python3 tools/board.py show T-112 | grep -n \"accepted\\|debt\" | head -3; grep -n \"T-112\" memory/SCOPE_CUTS.md | cut -c1-200 | head -3"
}
````

### User / tool · 2026-11-02T11:46:12.352Z

**tool result**
````
1
memory/ORCHESTRATOR_DECISIONS.md:62:| D-054 | Summary clauses the quote does not support are removed by code (2026-11-02, after T-094 r2). Before judging, code splits an AI summary into clauses; a clause is removed only when it adds salient content the excerpt
memory/contracts/api.md:732:Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the joins ` and ` / ` with `) and removes a clause only when it adds salient content its own quote lacks (T-11
64:- 2026-11-02T11:24:58Z orchestrator: §7.4 decision after round 3: close with accepted debt once AC2 (live 3-runs on 63e18ed, running) is met. Reason: every residual failure is in the safe direction or still laddered: an over-trim sends the item to the could-not-verify tray (visible, the human recovers it); an unsupported clause that is kept still goes to judge 1 and the human; on 188 recorded outputs the trim never fires on English. A vocabulary-bound trimmer cannot be complete; chasing more abbreviation lists has diminishing returns. Follow-ups: T-127 (no fragments: a trim that would leave a single bare noun or a clause starting with due to / which / including does not trim; kill the 3 surviving mutants and the 7 abbreviation-entry deletions) and the LLM_VS_CODE row 4 text (on T-109).
66:- 2026-11-02T11:25:01Z orchestrator: moved changes_requested -> blocked: awaiting AC2 live 3-runs on 63e18ed, then close with accepted debt (see note)
78:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; the D-054 trimmer is vocabulary-bound, so it misses some abbreviations (fresh probes: 12/43 faithful pairs over-trimm
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:46:42.413Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/upg129.py <<'EOF'\nimport sys, os\nroot, db, step = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfrom app.db import db as DB\nfrom app.backend import pipeline, present, review\ndef rec(date, src, ex): return f'Date: {date}\\nSource: {src}\\nExcerpt: \"{ex}\"'\ntext = \"FAX COVER SHEET\\nTo: Dr X\\n---\\n\" + \"\\n---\\n\".join([rec(\"2026-01-09\",\"Lakeside Clinic, intake\",\"Intake done.\"), rec(\"2026-03-20\",\"Lakeside Clinic, follow-up\",\"Neck pain improving.\")])\nconn = DB.connect(db)\nif step == \"old\":\n    cid = DB.create_case(conn, text, now=1.0, name=\"x\", source=\"paste\", backend=\"fixture\", demo_mode=0)\n    pipeline.ingest_case(conn, cid, text, 1.0)\n    gap = [f for f in DB.list_items(conn, cid, \"flag\") if f[\"type\"]==\"gap\"][0]\n    review.apply_review(conn, cid, gap[\"id\"], {\"action\": \"accept\"}, now=2.0)\n    print(\"old:\", cid, [(r[\"id\"], r[\"date_iso\"]) for r in present._recs_by_id(conn, cid).values()], [(f[\"id\"], f[\"review_status\"], f[\"computed\"].get(\"days\")) for f in DB.list_items(conn, cid, \"flag\")])\n    open(db + \".cid\", \"w\").write(cid)\nelse:\n    cid = open(db + \".cid\").read()\n    pipeline.ingest_case(conn, cid, text, 3.0)\n    print(\"new:\", [(r[\"id\"], r[\"date_iso\"]) for r in present._recs_by_id(conn, cid).values()], [(f[\"id\"], f[\"review_status\"], f[\"computed\"].get(\"days\"), f[\"computed\"].get(\"record_ids\") or f.get(\"record_ids\")) for f in DB.list_items(conn, cid, \"flag\")])\nEOF\nmkdir -p $S/upg; rm -f $S/upg/t.sqlite*; .venv/bin/python -I $S/scripts/upg129.py $S/parent $S/upg/t.sqlite old 2>&1 | tail -3; .venv/bin/python -I $S/scripts/upg129.py $S/repo $S/upg/t.sqlite new 2>&1 | tail -3",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T11:46:42.951Z

**tool result**
````
old: Kr6Fmiwykb4LqQ7bEPpbuw [('r1', None), ('r2', '2026-01-09'), ('r3', '2026-03-20')] [('f_gap_r2_r3', 'accepted', 70), ('f_date_r1', 'pending', None)]
new: [('r1', '2026-01-09'), ('r2', '2026-03-20'), ('r3', None)] [('f_gap_r2_r3', 'accepted', 70, ['r2', 'r3']), ('f_gap_r1_r2', 'pending', 70, ['r1', 'r2']), ('f_date_r3', 'pending', None, ['r3'])]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:46:53.741Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; mkdir -p artifacts/review-evidence/T-128-129-127-r1 && for f in probe_t128.py probe_t128b.py mut.py sweep.py rev.py ab.py ov129.py api129.py upg129.py probe127.py probe127b.py cmp_ingest.py; do cp $S/scripts/$f artifacts/review-evidence/T-128-129-127-r1/$f; done; ls artifacts/review-evidence/T-128-129-127-r1; ls reviews | grep -E \"T-12[789]\""
}
````

### User / tool · 2026-11-02T11:46:53.878Z

**tool result**
````
ab.py
api129.py
cmp_ingest.py
mut.py
ov129.py
probe127.py
probe127b.py
probe_t128.py
probe_t128b.py
rev.py
sweep.py
upg129.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:47:30.242Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-128-staff-engineer.md",
 "content": "# T-128 review, round 1 - staff-engineer-reviewer\n\nCard: summary trim must never leave a fragment (source findings: reviews/T-112-staff-engineer-r3.md finding 2 and 4). Commit 3d53ca5; HEAD at review time is 93de5f2 (`git log --oneline | head -3` shows 93de5f2, 3a74f75, 3d53ca5; `git diff 3d53ca5 HEAD --stat -- app/backend/summary_trim.py` is empty). I worked on `git archive 93de5f2` in my scratchpad (`T128_9_127_r1/repo`, plus a second archive `mut/` for mutants). Probe and mutation scripts are copied to `artifacts/review-evidence/T-128-129-127-r1/`.\n\n**Verdict: changes.** One major, two minors. The 7 fragments named in r3 are held and the three r3 mutants are now killed. The guard is still a closed word list, though: 10 of 31 fresh probes still leave a clear fragment and 3 more a borderline one.\n\n## 1. Deterministic checks\n- `tests/unit/test_summary_trim.py` in the archive: 259 passed (matches the handoff). Full `tests/unit` in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed (handoff says 3056 passed; the 4 skips account for the difference).\n- No model or network is involved: `summary_trim.py` is pure code.\n\n## 2. Fresh fragment probes (probe_t128.py, 31 summaries)\n`.venv/bin/python -I probe_t128.py <archive>`. 19 of 31 trimmed, 12 stayed whole (correct, whole summary goes to judge 1). Of the 19 trimmed outputs, 10 are clear fragments, 3 borderline, 6 fine:\n- Clear fragments: `Pain in the neck and lower back.` | `Lower back pain.` -> `Lower back.`; `Pain in the neck and right shoulder.` -> `Right shoulder.`; `Wrist fracture and surgery.` | `Surgery.` -> `Surgery.`; `MRI ordered, pending insurance approval.` -> `Pending insurance approval.`; `Knee surgery recommended, requiring six weeks of crutches.` -> `Requiring six weeks of crutches.`; `Ankle sprain, likely from the fall.` -> `Likely from the fall.`; `Back pain, worse with sitting.` -> `Worse with sitting.`; `Epidural injection given, after which pain eased.` -> `After which pain eased.`; `Shoulder surgery performed, leading to a sling.` -> `Leading to a sling.`; `Physical therapy started, plus home exercises.` -> `Plus home exercises.`\n- Borderline: `Again advised to rest.`, `Treated with ice.`, `No radiation.` (the last is a negation kept over a quote that says radiation to arm; judge 1 still sees it).\n- The guard works only for words in `_CONNECTOR` (summary_trim.py:389-392), the bare-body-part test (:445-447) and `_LEAD`. `pending`, `requiring`, `likely`, `worse`, `after`, `leading`, `plus`, `again` are not in any list, and a two-word noun phrase (`Lower back`) or a non-body bare noun (`Surgery`) passes the single-body-part test. This is the r3 finding-2 class with a different vocabulary.\n\n## 3. Unsupported clauses still trim (probe_t128b.py, 12 pairs)\n5 of 12 trim as intended (`Neck pain; surgery recommended.` -> `Neck pain.`; `Wrist pain; cast applied; discharged home.` -> `Wrist pain; discharged home.`; also the sling, splint and CT cases). 7 stay whole: 2 are right (`then physical therapy`, `Which was tolerated.` would be cut-loose clauses), 5 are over-guarded: `Neck pain. Surgery recommended. Also reports headaches.`, `Neck pain; MRI ordered. Was prescribed ibuprofen.`, `Back pain; injection given. Is improving.`, `Back pain; ultrasound done. Had a follow-up visit.` (each kept clause is its own sentence), and `Was seen at the ER; surgery recommended.` (nothing was removed before it; the summary opened that way itself). This fails safe (judge 1 sees the unsupported clause) but the brief's \"unsupported clauses still trim when no fragment would remain\" is not met for these.\n\n## 4. Mutation of the tests (mut.py, 14 mutants on summary_trim.py against test_summary_trim.py)\nKilled (9): connector rule off; drop the after-removed arm; with-join guard off; bare-body-part test off; widen it to any noun; delete `which`, `including`, `was`, `due` from `_CONNECTOR`. Survived (5): drop the \"no kept clause before it\" arm (259 passed; this arm only fires for the summary's own first clause, which is exactly the over-guard above); drop `len(...) > 1` (equivalent: a one-word summary cannot have had a clause removed); delete `also`, `however`, `consistent` from `_CONNECTOR`.\nAbbreviation-table sweep (sweep.py: each of the 30 `_ABBR`/`_ABBR_CASE` entries set to a dead word, then test_summary_trim.py): 26 killed, 4 survive: `IV`, `orif`, `hep`, `ekg`. The card's AC says each entry deletion is killed. `IV`, `hep`, `ekg` show no behavioural effect in any pair I tried. `orif` does, in the direction the tests do not cover (section 5).\n\n## 5. Reverse-direction abbreviation check (rev.py, 18 pairs: abbreviation in the summary, spelled out in the quote)\n2 of 18 over-trim to an empty text (to the could-not-verify tray): `ORIF wrist.` | `Open reduction internal fixation of wrist.` -> `''`; `RCR performed.` | `Rotator cuff repair performed.` -> `''`. The `orif` and `rcr` expansions (summary_trim.py:97-98) append the word `surgery`, which the quote does not contain, so the family check sees a new procedure. The other 16 stay whole. Pre-existing T-112 behaviour, not introduced here, but it is why the `orif` survivor matters.\n\n```json\n{\"card\": \"T-128\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 93de5f2 (summary_trim.py and test_summary_trim.py identical to 3d53ca5) in scratchpad T128_9_127_r1; app/backend/summary_trim.py, tests/unit/test_summary_trim.py, reviews/T-112-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-054; fixture/no backend, no network\",\n \"exercised\": [\n  \"python3 tools/board.py show T-128, T-129, T-127; read reviews/T-112-staff-engineer-r3.md in full; git diff 3d53ca5~1 3d53ca5\",\n  \".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed\",\n  \"tests/unit/test_summary_trim.py in the archive: 259 passed\",\n  \"probe_t128.py: 31 fresh fragment-prone summaries (19 trimmed, 10 clear and 3 borderline fragments among them)\",\n  \"probe_t128b.py: 12 positive-control pairs (5 trimmed, 2 rightly held, 5 over-guarded)\",\n  \"mut.py: 14 mutants of summary_trim.py (9 killed, 5 survived), 5 of ingest.py and 11 of present.py/review.py run for the sibling cards\",\n  \"sweep.py: 30 abbreviation-table entries set dead one at a time (26 killed, 4 survive: IV, orif, hep, ekg)\",\n  \"rev.py: 18 reverse-direction abbreviation pairs (2 over-trimmed)\",\n  \"grep of docs/LLM_VS_CODE.md and memory/ORCHESTRATOR_DECISIONS.md for 'fragment' and 'not yet committed'\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"deterministic_trim_is_code\": 5, \"fragment_safety\": 2, \"unsupported_removal_precision\": 3, \"faithful_paraphrase_survival\": 4, \"test_strength\": 3, \"doc_matches_code\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The fragment guard is a closed word list: 10 of 31 fresh probes still leave a clear fragment, 3 more a borderline one; D-054 still says 'never leaving a fragment'\",\n   \"evidence\": \"`.venv/bin/python -I artifacts/review-evidence/T-128-129-127-r1/probe_t128.py <archive>` (summary_trim.py:389-392 `_CONNECTOR`, :445-447 bare body part): 'Pain in the neck and lower back.' | 'Lower back pain.' -> 'Lower back.'; 'Pain in the neck and right shoulder.' -> 'Right shoulder.'; 'Wrist fracture and surgery.' | 'Surgery.' -> 'Surgery.'; 'MRI ordered, pending insurance approval.' | 'MRI approved.' -> 'Pending insurance approval.'; 'Knee surgery recommended, requiring six weeks of crutches.' -> 'Requiring six weeks of crutches.'; 'Ankle sprain, likely from the fall.' -> 'Likely from the fall.'; 'Back pain, worse with sitting.' -> 'Worse with sitting.'; 'Epidural injection given, after which pain eased.' -> 'After which pain eased.'; 'Shoulder surgery performed, leading to a sling.' -> 'Leading to a sling.'; 'Physical therapy started, plus home exercises.' -> 'Plus home exercises.'. Borderline: 'Again advised to rest.', 'Treated with ice.', 'No radiation.'. memory/ORCHESTRATOR_DECISIONS.md:62 (D-054) 'never leaving a fragment'.\",\n   \"why_it_matters\": \"This is r3 finding 2 again: the fix adds the r3 examples' words (due, which, including) and one-body-part rule, so the same defect class re-opens with the next connector. A fragment like 'Likely from the fall.' reaches judge 1 and the paralegal as the whole summary after one accept click; nothing is invented and the quote and trace stay, so it is not a blocker, but the card title and D-054 promise 'never' and the 7 tested probes were written from the review's own examples (they pass by construction).\",\n   \"fix\": \"Replace the lexical list with a structural test: after removal, a kept clause that does not contain a finite verb or a content-word head of its own, or whose first word is not a noun/adjective/determiner head of the original summary's subject, keeps the whole summary. Cheap version: when a clause is removed, keep the whole summary unless every kept clause begins with a word that also begins a kept clause in the ORIGINAL summary's first position (i.e. a word that could open a sentence), and extend the bare-noun rule to any single content word or a noun phrase with no verb. Or soften D-054 to name the guarded shapes.\",\n   \"acceptance_test\": \"tests/unit/test_summary_trim.py: the 10 clear fragments above (and the 3 borderline) return changed False; 'Pain in the neck and back.' over 'Neck pain.' still becomes 'Pain in the neck.'; a parametrized sweep takes every trimmed output of 100 recorded generator summaries and asserts each kept clause begins with the summary's own first-clause word class or a verb.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The guard over-fires: 5 of 12 positive controls that should trim stay whole, including a summary whose own first clause opens with a connector word\",\n   \"evidence\": \"`probe_t128b.py`: 'Neck pain; MRI ordered. Was prescribed ibuprofen.' | 'Neck pain. Ibuprofen prescribed.' -> unchanged; 'Neck pain. Surgery recommended. Also reports headaches.' -> unchanged; 'Back pain; injection given. Is improving.' -> unchanged; 'Back pain; ultrasound done. Had a follow-up visit.' -> unchanged; 'Was seen at the ER; surgery recommended.' | 'Seen at ER.' -> unchanged. summary_trim.py:443 `(after_removed or not any(not d for d in drop[:i])) and _connector_led(...)` does not look at the separator, so a new sentence after '.' counts as cut-loose. Mutant 'drop the no-kept-before arm' -> 259 passed.\",\n   \"why_it_matters\": \"I would have done it differently, not a spec violation: the failure is in the safe direction (judge 1 still sees the unsupported clause). But AC 1 says the trim 'still trims when no fragment would remain', and the handoff's own surprise ('a blanket rule broke Pain.') shows the guard was tuned by hand.\",\n   \"fix\": \"Apply the connector test only when the removed clause was joined to the kept one by ',' ';' or a conjunction, not when a '.' ends the removed clause; and drop the leading arm (a summary's own first clause is the model's wording, not something this trim cut loose).\",\n   \"acceptance_test\": \"The 4 two-sentence pairs and the 'Was seen at the ER' pair above trim (changed True, kept clause intact); 'Knee surgery recommended, due to torn meniscus.' over 'Torn meniscus.' still stays whole.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Mutant-killing tests are incomplete: 3 connector entries, the leading arm and 4 abbreviation entries (IV, orif, hep, ekg) survive; the orif entry shows a faithful over-trim in the reverse direction\",\n   \"evidence\": \"mut.py: deleting 'also', 'however' or 'consistent' from `_CONNECTOR` -> 259 passed each; dropping the leading arm -> 259 passed. sweep.py: 4 of 30 table entries survive (IV, orif, hep, ekg); AC 1 evidence names only tha/acdf/lle/rle/bue/rue/lue/u/s/UE. rev.py: 'ORIF wrist.' | 'Open reduction internal fixation of wrist.' -> '' and 'RCR performed.' | 'Rotator cuff repair performed.' -> '' (expansions at summary_trim.py:97-98 append 'surgery').\",\n   \"why_it_matters\": \"The card's second half is 'kill the surviving mutants'; 26 of 30 table deletions are killed, not all. The two reverse-direction over-trims send faithful entries to the tray, the T-112 r1/r2/r3 failure class (accepted as debt after round 3).\",\n   \"fix\": \"Add one test per surviving connector (also, however, consistent) and a faithful pair for orif/rcr in both directions; drop 'surgery' from the orif/rcr expansions or let a procedure word be covered by the abbreviation that produced it. Mark IV/hep/ekg as dead entries (remove or document).\",\n   \"acceptance_test\": \"The sweep.py run prints 'survivors: []' or lists only entries documented as inert; 'ORIF wrist.' over the spelled-out quote returns changed False.\"}\n ],\n \"whats_right\": [\n  \"The 7 fragments from the T-112 r3 review are held whole and the three r3 mutants (us/im case, label body vouch, quote negation) are now killed by named tests.\",\n  \"Trimming stays pure code with the original output kept: unsupported clauses with no fragment risk still trim to a whole clause ('Neck pain; surgery recommended.' -> 'Neck pain.').\",\n  \"Test file is deterministic and fast (259 tests in about 1 s), with a monkeypatch-based entry-deletion check built into the suite.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:47:30.416Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-128-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:47:58.361Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-129-staff-engineer.md",
 "content": "# T-129 review, round 1 - staff-engineer-reviewer\n\nCard: a non-library preamble must not become record 1 (reviews/T-123-paralegal.md minor; D-027: nothing is dropped). Commit 3a74f75; HEAD at review time is 93de5f2 (`git diff 3a74f75 HEAD --stat -- app/backend/ingest.py` is empty). I worked on `git archive 93de5f2` (`repo/`) and on `git archive 3a74f75~1` (`parent/`) in scratchpad `T128_9_127_r1`. Scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.\n\n**Verdict: changes.** One major, one minor. Numbering is stable and nothing is dropped, and all 5 ingest mutants I ran are killed. But the contract line that says the preamble \"has `preamble: true`\" is not true of what the API serves, so the card's second option (\"shown as a preamble\") is unreachable and the preamble is still counted and displayed as an unlabelled record 3.\n\n## 1. Deterministic checks\n- `tests/unit/test_ingest.py` is part of the full unit run in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed.\n- Old/new comparison over every `.txt` input under evals/, tests/, spec/, app/ (27 files, `cmp_ingest.py` loads the parent and HEAD `ingest.py` side by side): record numbers, sources and `unsplit` flags are identical for all 27. Golden and library packets and `unsplit_paste.txt` do not shift. The recorded-fixture suite passes, so no recorded call is keyed to a moved number.\n- Record numbering of the 9 shapes in `ab.py` (HEAD vs parent): with a preamble above (`---` separated, blank-line separated, no separator, `=== Record N ===` style, \"Re: Date:\" text, two preambles), real records are r1, r2 and the preamble(s) are r3 (r4), `unsplit: true`, `preamble: true`. A note between records and trailing text are numbered after the real records, `preamble: false`. Parent numbered the preamble r1 in all of those. `ov129.py`: no overlapping record spans in 6 shapes.\n\n## 2. What the API serves (api129.py, via `pipeline.ingest_case` and `present.record_view`)\n`record_view` keys: char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text. No `unsplit`, no `preamble`. HEAD: `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')` (unsplit and preamble print None). `GET /api/cases/{token}` returns `\"warnings\": []` (present.py case_view), so `UNSPLIT_TEXT` is only in the POST response. `grep -n \"UNSPLIT\\|unsplit\\|preamble\" app/frontend/*.js app/frontend/*.html` prints nothing. memory/contracts/api.md:76 says an unsplit record has `unsplit: true` and the one above the first real record `preamble: true`.\n\n## 3. Upgrade behaviour (upg129.py)\nA case created under the parent with a cover sheet, whose gap flag the paralegal accepted, then re-ingested by HEAD code on the same DB file:\n`old: [('f_gap_r2_r3', 'accepted', 70), ('f_date_r1', 'pending', None)]` then `new: records r1 2026-01-09, r2 2026-03-20, r3 None; flags [('f_gap_r2_r3', 'accepted', 70, ['r2','r3']), ('f_gap_r1_r2', 'pending', 70, ['r1','r2']), ('f_date_r3', 'pending', None, ['r3'])]`. `_persist` (pipeline.py:186-208) keeps the accepted row by id, and it now cites r3 = the cover sheet.\n\n```json\n{\"card\": \"T-129\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 93de5f2 (ingest.py identical to 3a74f75) and 3a74f75~1 in scratchpad T128_9_127_r1; app/backend/ingest.py, tests/unit/test_ingest.py, app/backend/present.py record_view, app/backend/pipeline.py _store_records/_persist, memory/contracts/api.md:76; fixture/no backend, no network\",\n \"exercised\": [\n  \"python3 tools/board.py show T-129; git diff 3a74f75~1 3a74f75; read app/backend/ingest.py in full\",\n  \".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed\",\n  \"cmp_ingest.py: parent vs HEAD ingest over 27 .txt inputs under evals/, tests/, spec/, app/ (0 differ in record numbers/sources/unsplit)\",\n  \"ab.py: 9 input shapes through parent and HEAD ingest (preamble with ---, blank line, no separator, header style; mid-note; trailing note; date-like preamble)\",\n  \"ov129.py: 6 preamble shapes checked for overlapping record spans (none)\",\n  \"api129.py: pipeline.ingest_case + present.record_view keys for a preamble case and a mid-note case (parent and HEAD)\",\n  \"upg129.py: case created and gap flag accepted under the parent, re-ingested under HEAD on the same sqlite file\",\n  \"mut.py: 5 mutants of ingest.py against tests/unit/test_ingest.py (sort off, preamble flag never set, preamble always true, first = block start, drop leftovers): all 5 killed\",\n  \"grep of app/frontend for UNSPLIT/unsplit/preamble; grep of callers of ingest/split_records/_store_records\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"numbering_stability\": 5, \"nothing_dropped_D027\": 5, \"api_exposes_preamble\": 2, \"contract_matches_code\": 2, \"test_strength\": 4, \"upgrade_safety\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The preamble is still a counted record 3 and nothing the API serves says it is a preamble: api.md:76 promises `unsplit`/`preamble` fields on the record that GET case and POST case do not return\",\n   \"evidence\": \"api129.py on HEAD: `record_view` keys are char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text; the cover sheet prints `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')`. present.py case_view returns `\\\"warnings\\\": []`; `grep -rn \\\"UNSPLIT\\\\|unsplit\\\\|preamble\\\" app/frontend` prints nothing. memory/contracts/api.md:76: 'text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: ... the one above the first real record also has `preamble: true`'. Card AC 1: 'is not counted as a record (or is shown as a preamble, not a record)'. Handoff: 'Left: frontend may label preamble records.'\",\n   \"why_it_matters\": \"The harm the paralegal reported (a cover sheet shifting 'record 1') is fixed. But AC 1 asks for one of two outcomes: the cover sheet is not counted (it is, as record 3, so a 2-record packet reports 3), or it is shown as a preamble (the UI cannot tell: the flag lives only in the in-memory ingest dict, which `_store_records` (pipeline.py:158) does not persist and `record_view` does not emit). The contract text is wrong for GET case, so a frontend following it finds no field. The stated 'frontend may label' follow-up cannot be built without a backend change.\",\n   \"fix\": \"Persist `unsplit` and `preamble` on the records row (or derive them in `record_view` from `source_label == '' and date_raw == ''` plus position) and add both to `record_view`; carry the `UNSPLIT_TEXT` warning into GET case or document that it is POST-only. Then update api.md:76 to say which responses carry the fields. Frontend card to label it 'cover text, not a record'.\",\n   \"acceptance_test\": \"tests/unit: create a case from a cover-sheet paste, then `GET /api/cases/{token}`: records[2] has `preamble: true` and `unsplit: true`, records[0..1] have both false, and a library packet (golden case_01) has all records false.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A case stored before this commit and re-ingested after it keeps its accepted review on the old record numbers, so the accepted gap flag now cites the cover sheet\",\n   \"evidence\": \"upg129.py: old (parent) `('f_gap_r2_r3', 'accepted', 70)`; after HEAD re-ingest on the same DB: `('f_gap_r2_r3', 'accepted', 70, ['r2','r3'])` alongside a new pending `('f_gap_r1_r2', 'pending', 70, ['r1','r2'])`, with r3 now the cover sheet. pipeline.py:150-166 (`_store_records` deletes and re-stores) and :186-208 (`_persist` keeps the old row's review_status by id; stale rows are removed only if pending).\",\n   \"why_it_matters\": \"A reviewed item stays bound to a number that now means a different record; the accepted gap would still be listed for export. Exposure is bounded (cases purge after 24 h, `DB.RETENTION_SECONDS`, and only pastes with unsplit text are affected), so it is minor, but it is the numbering-stability question the brief asked and the card has no note, no migration and no test.\",\n   \"fix\": \"Either re-run is allowed to drop a reviewed item whose record_ids no longer match the stored records, with a visible reset, or document in the card/DECISIONS that numbering changed and in-flight cases with unsplit text must be re-created (retention makes this a one-line note).\",\n   \"acceptance_test\": \"Unit test: store a case with a preamble using the old numbering (records r1 preamble, r2, r3, accepted f_gap_r2_r3), re-run ingest_case with the new code, assert no accepted flag cites a record whose date differs from the one it was computed on, or that the item is reset to pending.\"}\n ],\n \"whats_right\": [\n  \"Numbering is stable on real data: 27 golden/library/spec inputs produce identical record numbers before and after, and the preamble cases keep r1, r2 for the real records in 6 shapes.\",\n  \"D-027 is honoured: the preamble is kept verbatim as its own unsplit record, `UNSPLIT_TEXT` is raised for it, and no span overlaps another.\",\n  \"The tests pin the behaviour (6 parametrized preambles plus 2 more): all 5 mutants I ran against ingest.py (sort, flag, first-field, always-preamble, dropped leftovers) fail at least one test.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:47:58.516Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-129-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:48:16.094Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T128_9_127_r1; cat > $S/scripts/idx.py <<'EOF'\nimport sys; sys.path.insert(0, sys.argv[1])\nfrom app.backend import present\nev=[{\"action\":\"confirm_date\",\"after\":{\"gap_changes\":[{\"flag_id\":\"g\",\"change\":\"changed\",\"old_days\":42,\"new_days\":40,\"old_from\":\"2026-03-03\",\"old_to\":\"2026-04-14\",\"new_from\":\"2026-03-05\",\"new_to\":\"2026-04-14\",\"record_seq\":4,\"sentence\":\"s\"}]}}]\nprint(\"same days, shifted dates ->\", present.gap_change_index(ev, {\"g\": {\"days\": 40, \"from\": \"2026-03-10\", \"to\": \"2026-04-19\"}}))\nprint(\"same figures ->\", bool(present.gap_change_index(ev, {\"g\": {\"days\": 40, \"from\": \"2026-03-05\", \"to\": \"2026-04-14\"}})[0]))\nEOF\n.venv/bin/python -I $S/scripts/idx.py $S/repo; cp $S/scripts/idx.py artifacts/review-evidence/T-128-129-127-r1/idx.py; python3 - <<'EOF'\nimport subprocess\nEOF\nsed -n 79,80p /dev/null; grep -n \"from_date\\|\\\"from\\\"\" app/backend/present.py | head -5"
}
````

### User / tool · 2026-11-02T11:48:16.430Z

**tool result**
````
same days, shifted dates -> ({}, [])
same figures -> True
71:    if "from_date" in c:
72:        c.update({"from": c.pop("from_date"), "to": c.pop("to_date", None)})
126:        if cur and cur.get("days") == ch.get("new_days") and (ch.get("new_from") is None or cur.get("from") == ch["new_from"]) and (ch.get("new_to") is None or cur.get("to") == ch["new_to"]):
133:    cur = {f["id"]: {"days": f["computed"].get("days"), "from": f["computed"].get("from"), "to": f["computed"].get("to")} for f in flags if f["type"] == "gap"}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:48:43.626Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-127-staff-engineer.md",
 "content": "# T-127 review, round 1 - staff-engineer-reviewer\n\nCard: keep the gap-change record on the gap flag (GET case returns `gap_change` on a gap flag whose figures moved after a confirm_date, and `gap_changes_removed[]`). Commit 93de5f2, which is HEAD at review time (`git log -1 --format=%H` prints 93de5f2e47a18f3eeff9edf8e6bc7b34fbb02dfb). I worked on `git archive 93de5f2` in scratchpad `T128_9_127_r1` (`repo/` for runs, `mut/` for mutants). Scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.\n\n**Verdict: pass.** No blocker or major. The record is stored in the `confirm_date` review event, read back by code only, and survives a fresh app on the same DB file. Two minors are test gaps; one nit is a contract omission.\n\n## 1. Deterministic checks\n- `tests/unit/test_t127_gap_change_kept.py`: 4 passed in the archive (part of the full run: 3057 collected, 3053 passed, 4 skipped, 0 failed).\n- No model is called: `present.gap_change_index` is a loop over stored events; `review.py:353-359` fills `record_seq` and `sentence` from the recompute.\n\n## 2. What I exercised on the real API (probe127.py, fixture backend, library case lib09)\n- Before: `f_gap_r1_r2` 42 days, no `gap_change`. `POST .../records/r4/confirm_date {\"date\": \"2026-03-05\"}` returns `gap_changes [('f_gap_r4_r2', 'changed', 42, 40)]`. `GET case` then shows `('f_gap_r4_r2', 40, (42, 40, 4))` = old_days, new_days, record_seq, and `gap_changes_removed: []`.\n- Accept, then `reset` (the undo) on the gap flag: both 200; `gap_change` still present after the reset, as api.md says (\"stays through ... review actions\"). `GET /items/{id}` and the review response wrap the item as `{\"item\": ...}` and carry the same `gap_change` sentence.\n- Re-confirm of the same record: `422 invalid_edit` (a confirmed date is no longer ambiguous), no second event. There is no route that undoes a confirm_date, so there is no re-confirm path that could write a second change.\n- Determinism: two GETs of the case are byte-equal (sorted JSON), and a fresh `create_app` on the same sqlite file returns the same JSON. `list_events` orders by `at, rowid` (db.py:261).\n- The removed path end to end (probe127b.py, `pipeline.ingest_case` + `review.confirm_date` with no LLM, a 44-day gap split by an ambiguous 02/03/2026 record confirmed as 2026-02-03): `confirm_date` returns `removed f_gap_r1_r3`; `all_items` then lists `gap_changes_removed [('f_gap_r1_r3', 'A gap of 44 days no longer applies after you confirmed the date of record 2.')]`; the event holds `change: removed`.\n- Non-gap flags carry no `gap_change` key; the contract says `gap_change: null` \"otherwise\", which is true only for gap flags.\n\n## 3. Mutation of the tests (mut.py, 11 mutants of present.py/review.py against test_t127_gap_change_kept.py)\nKilled (6): `record_seq` not stored; `gap_changes` not written into the event; removed list ignores current gaps; first event wins instead of latest; `gap_changes_removed` dropped from case_view; `gap_change` never set. Survived (5): drop the `days ==` check (equivalent: from/to imply days); drop both from/to checks; drop only the `new_to` check; skip `gone.pop` on re-add; skip `latest.pop` on removal. The last two do not change an observable result because the `fid not in current` and `cur ==` tests already guard them (equivalent). The from/to survivor is real: `idx.py` shows the code returns `{}` for a gap with the same 40 days but shifted dates, and the mutant would return the old change; no test sends that case.\n\n```json\n{\"card\": \"T-127\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 93de5f2 (HEAD) in scratchpad T128_9_127_r1; app/backend/present.py (gap_change_index, _with_gap_changes, item_view, all_items, case_view), app/backend/review.py (confirm_date, _log_confirm_date, _recompute_gaps), app/db/db.py list_events, memory/contracts/api.md:268, tests/unit/test_t127_gap_change_kept.py; fixture backend, no network\",\n \"exercised\": [\n  \"python3 tools/board.py show T-127; git diff 93de5f2~1 93de5f2; read present.py, review.py:329-476, memory/contracts/api.md:262-270\",\n  \".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed\",\n  \"probe127.py on the real API (fixture backend): confirm_date, GET case, accept + reset on the gap flag, GET item, re-confirm (422), second GET equality, fresh create_app on the same DB file\",\n  \"probe127b.py: removed-gap path through pipeline.ingest_case + review.confirm_date + present.all_items (no LLM)\",\n  \"idx.py: direct gap_change_index call with same days and shifted dates\",\n  \"mut.py: 11 mutants of present.py/review.py against test_t127_gap_change_kept.py (6 killed, 5 survived, 4 of those equivalent)\",\n  \"grep of callers of _recompute_gaps (review.py:354 and :579) and gap_change in app/backend\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"stored_through_review_events\": 5, \"exposed_on_get_case\": 5, \"contract_matches_code\": 4, \"undo_and_reconfirm_paths\": 5, \"determinism\": 5, \"test_strength\": 3},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"No test pins the from/to comparison in gap_change_index; removing it survives the suite\",\n   \"evidence\": \"mut.py: replacing `(ch.get(\\\"new_from\\\") is None or cur.get(\\\"from\\\") == ch[\\\"new_from\\\"]) and (ch.get(\\\"new_to\\\") is None or cur.get(\\\"to\\\") == ch[\\\"new_to\\\"])` with nothing (present.py:126) -> 4 passed. idx.py: with an event new_days 40, new_from 2026-03-05, new_to 2026-04-14 and a current gap days 40 from 2026-03-10 to 2026-04-19, the code returns ({}, []); the mutant returns the stale change. The one `moved by something else` case in test_gap_change_goes_when_the_gaps_figures_move_again changes the days too (30), so the days check alone kills it.\",\n   \"why_it_matters\": \"The contract says the change goes when the gap's figures differ from the ones it produced. A recompute that shifts both endpoints but keeps the length (not_duplicate calls `_recompute_gaps` at review.py:579 without recording a change) would then show 'now 40 days (was 42) after you confirmed record 4' on figures that are no longer those. It is a stale claim shown as fact.\",\n   \"fix\": \"Add a case to test_gap_change_goes_when_the_gaps_figures_move_again with equal days and different from/to, asserting `changes == {}`.\",\n   \"acceptance_test\": \"The mutant that removes the from/to comparison fails test_t127_gap_change_kept.py.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The removed-gap path is tested only on hand-built events, never through confirm_date and GET case\",\n   \"evidence\": \"tests/unit/test_t127_gap_change_kept.py::test_a_gap_that_no_longer_applies_is_listed_with_its_sentence_until_it_comes_back calls `present.gap_change_index` with a dict; no test drives `confirm_date` to a removal and then reads `GET /api/cases/{token}`. Mutant 'gap_changes_removed not in case_view' is killed only because test 1 asserts `== []`.\",\n   \"why_it_matters\": \"I checked the path by hand (probe127b.py: 44-day gap, confirm, `gap_changes_removed` lists it with its sentence, and the event holds `change: removed`), and it works. Without a test, a later change to `_gap_changes` or the event shape could drop the removed list while every test stays green.\",\n   \"fix\": \"Add the probe127b scenario as a unit test through `review.confirm_date` and `present.all_items` (no LLM needed), asserting the sentence, then confirming a second record that recreates the gap and asserting the list empties.\",\n   \"acceptance_test\": \"Mutating `_log_confirm_date` to write `gap_changes: []` fails a removed-path test, not only the changed-path test.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"api.md names GET case only; GET item and the review response also carry gap_change, and non-gap flags have no key\",\n   \"evidence\": \"probe127.py: `GET /items/{id}` returns {'item': ...} with gap_change sentence 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'; present.py:149-157 item_view adds it for kind == 'flag' gaps; api.md:268 says 'a gap flag in `flags[]` ... otherwise `gap_change: null`' and 'Both are always present' while non-gap flags have no `gap_change` key.\",\n   \"why_it_matters\": \"A frontend reading the contract would not know the item and review responses are consistent with GET case, and 'always present' is true only for gap flags.\",\n   \"fix\": \"One sentence in api.md:268: 'On gap flags only; also in GET /items/{id} and the review response `item`.'\",\n   \"acceptance_test\": \"grep -n 'gap_change' memory/contracts/api.md shows the item/review mention.\"}\n ],\n \"whats_right\": [\n  \"The change is derived, not duplicated: stored once in the confirm_date audit event (no schema change) and shown only while the gap's current figures match, so a later move cannot leave a stale claim in the common case.\",\n  \"Deterministic and restart-safe: two GETs and a fresh app on the same sqlite file return identical JSON; accept and reset on the gap flag keep the change.\",\n  \"The removed-gap case works end to end with its sentence, and a second confirm of the same record is refused with 422 invalid_edit without writing a second event.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:48:43.784Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-127-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:48:46.872Z

**tool call — Bash**
````
{
 "command": "for t in T-128 T-129 T-127; do python3 - $t <<'EOF'\nimport sys,re,json\nt=sys.argv[1]; s=open(f\"reviews/{t}-staff-engineer.md\").read()\nblocks=re.findall(r\"```json\\n(.*?)\\n```\", s, re.S); assert len(blocks)==1\nj=json.loads(blocks[0]); print(t, j[\"verdict\"], [f[\"severity\"] for f in j[\"findings\"]], len(s.split(\"```json\")[0]))\nEOF\ndone; python3 tools/board.py validate 2>&1 | tail -3; ps aux | grep -E \"uvicorn|board_server\" | grep -v grep | head -2"
}
````

### User / tool · 2026-11-02T11:48:47.160Z

**tool result**
````
T-128 changes ['major', 'minor', 'minor'] 5166
T-129 changes ['major', 'minor'] 3141
T-127 pass ['minor', 'minor', 'nit'] 3494
ok (131 file(s))
arsis              824   0.1  0.1 435658416  58032   ??  S    19Oct26  24:22.80 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m uvicorn ofq.api.app:app --app-dir src --host 127.0.0.1 --port 8000
arsis            38450   0.0  0.1 435291024  50352 s002  S+    7:35PM   1:12.75 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python tools/board_server.py --port 7777
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:48:54.922Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t128_t129_t127_patterns.md",
 "content": "---\nname: project_t128_t129_t127_patterns\ndescription: r1 at HEAD 93de5f2 - T-128 changes (fragment guard still a closed word list, over-guard, 4 table survivors), T-129 changes (preamble flag not served by API, pre-upgrade accepted flag mis-bound), T-127 pass\nmetadata:\n  type: project\n---\n\n- T-128 3d53ca5 (changes: 1 major, 2 minor): fragment guard `_CONNECTOR` + bare-body-part rule is a closed list; 31 fresh probes left 10 clear fragments (pending/requiring/likely/worse/after which/leading/plus, 'Lower back.', 'Surgery.'). Over-guard: connector test ignores the '.' separator and the summary's own first clause (5/12 positives stay whole). Abbreviation sweep: 26/30 killed, survivors IV/orif/hep/ekg; orif/rcr expansions append 'surgery' so the abbreviation-in-summary direction over-trims.\n- T-129 3a74f75 (changes: 1 major, 1 minor): numbering stable on 27 inputs, 5/5 ingest mutants killed, but `unsplit`/`preamble` never reach record_view, GET case warnings is [] and the frontend never reads them, so api.md:76 is false for GET; pre-upgrade case re-ingest keeps an accepted gap flag bound to the old number (`_persist` keeps review_status by id).\n- T-127 93de5f2 (pass: 2 minor, 1 nit): from/to comparison in gap_change_index unpinned (equal days, shifted dates); removed path tested only on hand-built events.\n\n**Why:** the same classes recur: a closed-vocabulary guard re-opens with the next word; a field that exists in an in-memory dict is documented as API but never persisted or serialised.\n**How to apply:** on any \"contract says field X\" card, call present.record_view / the real route and list the keys, do not trust the ingest dict; on guard cards write 30 fresh probes from the guard's complement, not the review's examples; for the old/new comparison load parent and HEAD ingest side by side (scripts in artifacts/review-evidence/T-128-129-127-r1/).\n\nRelated: [[project_t112_trim_patterns]], [[project_wiring_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T11:48:55.019Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t128_t129_t127_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:48:56.224Z

**tool call — Bash**
````
{
 "command": "printf '%s\\n' '- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — r1 93de5f2: closed-list fragment guard, preamble flag never served by API, T-127 pass with unpinned from/to' >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md; tail -2 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-120"
}
````

### User / tool · 2026-11-02T11:48:56.321Z

**tool result**
````
- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction
- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — r1 93de5f2: closed-list fragment guard, preamble
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:00.703Z

T-128 and T-129 get `changes`, and T-127 gets `pass`. All three reviews are in `reviews/` (`T-128-staff-engineer.md`, `T-129-staff-engineer.md`, `T-127-staff-engineer.md`), and `board.py validate` says ok (131 files). I ran a `git archive 93de5f2` copy (HEAD): 3057 unit tests collected, 3053 passed, 4 skipped, 0 failed.

- **T-128 (changes: 1 major, 2 minor):** the fragment guard is still a closed word list. 10 of 31 fresh probes still leave a clear fragment, such as `Likely from the fall.`, `Pending insurance approval.` and `Lower back.`. The guard also blocks 5 of 12 trims that should fire, and 4 of the 30 abbreviation-table entries (IV, orif, hep, ekg) survive deletion.
- **T-129 (changes: 1 major, 1 minor):** record numbering is stable and all 5 ingest mutants are killed, but the API never serves `unsplit` or `preamble`, so `api.md:76` is wrong for GET case. A case stored before this commit and re-run keeps an accepted gap flag pointing at the old record numbers.
- **T-127 (pass: 2 minor, 1 nit):** the change is stored in the `confirm_date` review event, comes back on GET case, and is identical across two GETs and a fresh app on the same DB. Accept then reset keeps it, and re-confirming the same record returns 422. The minors are an untested from/to comparison and a removed-gap path tested only on hand-built events.

I stopped no PIDs. Probe and mutation scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.
