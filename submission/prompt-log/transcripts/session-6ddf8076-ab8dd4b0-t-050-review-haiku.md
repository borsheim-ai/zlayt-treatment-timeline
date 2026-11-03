# Subagent: T-050 review (haiku) (T-050 review (haiku))

Source: `agent-ab8dd4b06d546f7ce.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:01:46.974Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-050 "Per-case ID namespacing" (AC: `python3 tools/board.py show T-050`). Run `.venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q 2>&1 | tail -2`. With a short script, run two different golden cases back to back into one temp sqlite DB via the code path the card names, confirm no collision, display ids stay short in API output, and delete_case removes only that case's rows. Quote outputs. Write reviews/T-050-staff-engineer.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:48.060Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:01:48.067Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:48.662Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-050",
 "description": "Show T-050 card from board"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:48.666Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:01:48.789Z

**tool result**
````
---
id: "T-050"
title: "Per-case ID namespacing (records/entries/amounts/flags) so multiple cases coexist in one DB"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:59:33Z"
updated_at: "2026-11-02T02:01:47Z"
claimed_by: "backend"
claimed_at: "2026-11-02T01:59:47Z"
rounds: 0
commits: ["6c3aeb1"]
reviews: []
ac:
  - {"n": 1, "text": "Two different golden cases run back to back in one DB file without collision; ids unique per case (e.g. <case_token_prefix>:r1) or composite keys; test in tests/unit/test_db.py and test_pipeline.py", "done": true, "evidence": "tests/unit/test_multicase.py (3 passed: two golden cases + two full pipeline runs in one file); db PK is now (case_id, id), ids stay short"}
  - {"n": 2, "text": "API responses keep short display ids (r1, e5) per memory/contracts/api.md while storage is unique", "done": true, "evidence": "test_api_routes::test_two_cases_coexist_with_short_display_ids (ids e1/r1, no suffix)"}
  - {"n": 3, "text": "delete_case removes only that case's rows (test)", "done": true, "evidence": "test_multicase::test_delete_case_removes_only_that_case"}
---
## Description
Defect found by backend-3 on T-040: pipeline and db use global ids (r1, e5); a second case in the same sqlite file collides. Fix in app/db + pipeline id generation.

## Notes (append-only, newest last)
- 2026-11-02T01:59:37Z orchestrator: assigned: backend-3
- 2026-11-02T01:59:47Z backend: claimed
- 2026-11-02T02:01:40Z backend: AC 1 checked: tests/unit/test_multicase.py (3 passed: two golden cases + two full pipeline runs in one file); db PK is now (case_id, id), ids stay short
- 2026-11-02T02:01:40Z backend: AC 2 checked: test_api_routes::test_two_cases_coexist_with_short_display_ids (ids e1/r1, no suffix)
- 2026-11-02T02:01:40Z backend: AC 3 checked: test_multicase::test_delete_case_removes_only_that_case
- 2026-11-02T02:01:40Z backend: moved in_progress -> in_review
- 2026-11-02T02:01:47Z orchestrator: review dispatched: haiku

## Handoff
What changed: schema.sql composite PK (case_id,id) for records/entries/amounts/flags; db.py _find/get_item/update_item/apply_review/set_review_status accept case=; review.py/present.py pass case; pipeline._persist passes case=cid (uncommitted, in backend-2's WIP file, see T-037 note). Verified: test_db, test_review_rules, test_api_routes (15), test_pipeline, test_multicase (3) = 93 passed. Left: backend-2 must commit the pipeline.py lines; delete old sqlite files.
````

### User / tool · 2026-11-02T02:01:48.794Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
5	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
6	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
7	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:51.412Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q 2>&1 | tail -2; echo \"---GIT---\"; git rev-parse --is-inside-work-tree 2>&1; git log --oneline -5 2>&1; echo \"---SHOW 6c3aeb1---\"; git show --stat 6c3aeb1 2>&1 | head -40; echo \"---STATUS---\"; git status --short 2>&1 | head -30",
 "description": "Run required pytest subset and inspect git state"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:51.668Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_db_review_patterns.md"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:51.883Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_wiring_review_patterns.md"
}
````

### User / tool · 2026-11-02T02:01:56.140Z

**tool result**
````
....................................                                     [100%]
36 passed in 4.27s
---GIT---
true
0691e84 fix(frontend): count undated needs-review entries in the timeline header (T-042 follow-up)
c8c7ba6 fix(evals): exactly-3-run gate, check-spec recomputes bar, no swallowed exceptions, per-bar mutation tests (T-038 r1)
6c3aeb1 fix(db): per-case id namespacing via composite primary key (T-050)
7b7c8a5 test(review): any judge exception on edit is JUDGE_UNAVAILABLE and needs_review (T-039 debt)
43b5e12 test(fixtures): curated golden-conformant fixture set + generator (T-051, D-029)
---SHOW 6c3aeb1---
commit 6c3aeb14d78df77fdf244532fd5105624fef22fe
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:01:40 2026 -0600

    fix(db): per-case id namespacing via composite primary key (T-050)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/present.py        |  2 +-
 app/backend/review.py         | 32 +++++++++++++-------------
 app/db/db.py                  | 41 +++++++++++++++++++--------------
 app/db/schema.sql             | 21 ++++++++++-------
 tests/unit/test_api_routes.py | 12 ++++++++++
 tests/unit/test_multicase.py  | 53 +++++++++++++++++++++++++++++++++++++++++++
 6 files changed, 119 insertions(+), 42 deletions(-)
---STATUS---
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M app/backend/pipeline.py
 M app/frontend/charges.js
 M app/frontend/flags.js
 M app/frontend/index.html
 M app/frontend/review.js
 M app/llm/backends/fixture.py
 M app/llm/record.py
 M board/activity.jsonl
 M board/cards/T-015.md
 M board/cards/T-027.md
 M board/cards/T-029.md
 M board/cards/T-030.md
````

### User / tool · 2026-11-02T02:01:56.147Z

**tool result**
````
1	---
2	name: wiring-review-patterns
3	description: T-030 r2 pattern: a round fix passes its unit tests at the function/table level but the producer path never calls it. Check callers and run the producer, not just pytest.
4	metadata:
5	  type: project
6	---
7	
8	Recurring pattern (T-030 r2, 2026-11-01): the round-1 major "compose_state ignores endpoint_unverified" was fixed in the
9	boolean table (confidence.py:64) and tested there, and `check_amount` was added with tests. But the only producer of
10	ENDPOINT_NOT_VERIFIED (app/backend/gaps.py:37) never calls compose_state, and gap flags carry reasons with no `state` key.
11	`check_amount` had no production caller at all. Pytest was green on both, so the green summary hid the gap.
12	
13	**Why:** a fix that is green only in its own unit test does not close the risk the original finding named (the gap flag
14	path). Same family as T-031 partial re-fixes (sibling writers), see [[project_db_review_patterns]].
15	
16	**How to apply:**
17	- For every function or table row a round adds or changes, grep non-test callers (`grep -rn name --include=*.py . | grep -v tests/`).
18	  Zero production hits = not wired, regardless of pytest.
19	- Run the producer on a repro (e.g. gaps.gap_flags on synthetic records) and check the output shape, not only the unit tests.
20	- Scratch-copy mutation of the function (return []) and of the table row shows whether the tests are load-bearing; it does not
21	  show whether production reaches them.
22	
23	Also: the dossier names claude-sonnet-5-5 as the expected model id, but the r2 run was executing as claude-haiku-5-5. Record
24	the model that actually ran in the JSON, and note the mismatch in the reply.
25	
````

### User / tool · 2026-11-02T02:01:56.148Z

**tool result**
````
1	---
2	name: db-review-patterns
3	description: T-031 (app/db) round-1/round-2 review patterns - partial re-fixes, regex guard blind spots, scratch-copy mutation method, hook gotchas for reviewers
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns from the T-031 review (app/db/db.py, tests/unit/test_db.py; reviews reviews/T-031-staff-engineer.md and -r2.md).
9	
10	- **A re-fix closes the named entry point, not the write class.** Round 2 locked `update_item` (db.py:137) but left `add_item` (db.py:90-101) accepting `edited_json` with no review event. When a finding says "X can be written with no event", grep every helper that reaches the same column (`grep -rn edited_json app`), not just the one named.
11	- **Source-regex guard tests have blind spots.** test_review_status_only_via_apply_review matches `review_status=?`, `SET review_status`, `review_status='...'`. It misses a multi-column `SET edited_json=?, review_status=:s`, and the test still passes while its docstring says the property holds. Probe such guards with an appended rogue line in a scratch copy before accepting them as proof.
12	- **"Raises on no payload" was true only for the fresh item.** `(edited or before["edited"])` lets a re-edit with no payload succeed and log an event. When a fix says "raises when X", probe the state variants (fresh, already-edited).
13	- **Mutation method that works:** copy app/ and tests/ to the scratchpad, `sed -i.bak` one guard, run `pytest tests/unit/test_db.py -q`, restore from .bak. Do not touch repo files.
14	
15	Reviewer environment gotchas (seen on this card):
16	- The Bash git-guard hook denies commands containing backticks inside a `python -c "..."` string ("could not parse command safely"). Put scripts in a file and run the file.
17	- reviewer-write-guard blocks Write to the scratchpad. Scripts and probes must go under artifacts/review-evidence/.
18	
19	Related: [[project_harness_review_patterns]], [[project_design_review_patterns]].
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:59.392Z

**tool call — Bash**
````
{
 "command": "git show 6c3aeb1 -- app/db/schema.sql app/db/db.py app/backend/present.py app/backend/review.py 2>&1",
 "description": "Show committed diff for schema, db, present, review"
}
````

### User / tool · 2026-11-02T02:01:59.488Z

**tool result**
````
commit 6c3aeb14d78df77fdf244532fd5105624fef22fe
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:01:40 2026 -0600

    fix(db): per-case id namespacing via composite primary key (T-050)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/present.py b/app/backend/present.py
index 2018b57..3f3ec86 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -85,7 +85,7 @@ def _recs_by_id(conn, case_id):
 
 
 def item_view(conn, case_id, item_id):
-    row = DB.get_item(conn, item_id)
+    row = DB.get_item(conn, item_id, case_id)
     kind = _ID_KIND[item_id[0]]
     v = _VIEW[kind](row, _recs_by_id(conn, case_id))
     v["kind"] = kind
diff --git a/app/backend/review.py b/app/backend/review.py
index fb3c00c..752fe2b 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -26,7 +26,7 @@ def _now(now):
 
 def _item(conn, case_id, item_id):
     try:
-        row = DB.get_item(conn, item_id)
+        row = DB.get_item(conn, item_id, case_id)
     except KeyError:
         raise ReviewError(404, "not_found", message="No such item.") from None
     if row["case_id"] != case_id:
@@ -48,9 +48,9 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
         raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
     warnings = []
     if action in ("accept", "dismiss", "reset"):
-        DB.apply_review(conn, item_id, action, now=t)
+        DB.apply_review(conn, item_id, action, now=t, case=case_id)
         if kind == "flag" and action == "dismiss" and body.get("note"):
-            DB.update_item(conn, item_id, now=t, reviewer_note=str(body["note"])[:2000])
+            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
     else:
         warnings = _edit(conn, case_id, kind, item, body, call, t)
     from app.backend import present
@@ -68,8 +68,8 @@ def _edit(conn, case_id, kind, item, body, call, t):
     if kind == "flag":
         if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
             raise _bad("Only a note can be added to a flag.")
-        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t)
-        DB.update_item(conn, item["id"], now=t, reviewer_note=edits["note"].strip()[:2000])
+        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
+        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
         return []
     if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
         raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
@@ -123,15 +123,15 @@ def _edit(conn, case_id, kind, item, body, call, t):
     if "excerpt" in edits or "excerpt" in prev:
         edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                       excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
-    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t)
+    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
     if edited["kept_my_wording"]:
-        DB.apply_review(conn, item["id"], "keep_my_wording", now=t)
+        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
     lad = item.get("ladder") or {"item_id": item["id"]}
     lad["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": call_id, "verdict": ladder_verdict}
     lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                               qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
     lad["state"] = state
-    DB.update_item(conn, item["id"], now=t, state=state, state_reasons_json=reasons, ladder=lad)
+    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
     return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
         if ladder_verdict == "unavailable" else []
 
@@ -147,25 +147,25 @@ def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None)
         raise _bad("Only a record whose date can be read two ways can be confirmed.")
     if date_iso not in (rec["date_candidates"] or []):
         raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
-    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=?", (date_iso, record_id))
+    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
     moved = None
     for e in DB.list_items(conn, case_id, "entry"):
         if record_id in (e["record_ids"] or []):
-            DB.update_item(conn, e["id"], now=t, date_iso=date_iso)
+            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso)
             moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
-    removed = _drop(conn, f"f_date_r{rec['seq']}")
+    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
     removed += _recompute_gaps(conn, case_id, t)
     log_id = moved["id"] if moved else None
     if log_id:
-        DB.apply_review(conn, log_id, "confirm_date", now=t)
+        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
     from app.backend import present
     return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
             "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
             "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
 
 
-def _drop(conn, flag_id):
-    cur = conn.execute("DELETE FROM flags WHERE id=?", (flag_id,))
+def _drop(conn, case_id, flag_id):
+    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
     return [flag_id] if cur.rowcount else []
 
 
@@ -199,9 +199,9 @@ def _recompute_gaps(conn, case_id, t):
             removed.append(old["id"])
             continue
         oc = old.get("computed") or {}
-        DB.update_item(conn, old["id"], now=t, **PL._row("flag", item))
+        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
         if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
-            DB.apply_review(conn, old["id"], "reset", now=t)
+            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
     have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
     for iid, item in new.items():
         if iid not in have:
diff --git a/app/db/db.py b/app/db/db.py
index 1156236..f557cbb 100644
--- a/app/db/db.py
+++ b/app/db/db.py
@@ -16,6 +16,7 @@ REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
 ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
            "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
 _ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
+_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
 _PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
 _CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
 _SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
@@ -100,15 +101,21 @@ def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> st
     return iid
 
 
-def _find(conn, item_id):
+def _find(conn, item_id, case=None):
+    """Item ids are unique per case (T-050). Pass `case` (the case id) whenever more than one case can share the file."""
     kind = _PREFIX_KIND.get(item_id[:1])
     if kind is None:
         raise KeyError(item_id)
-    table = _ITEM_TABLES[kind][0]
-    r = conn.execute(f"SELECT * FROM {table} WHERE id=?", (item_id,)).fetchone()
-    if r is None:
+    table = _ITEM_TABLE_OF[kind]
+    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
+    if case is not None:
+        q, a = q + " AND case_id=?", a + [case]
+    rows = conn.execute(q, a).fetchall()
+    if not rows:
         raise KeyError(item_id)
-    return table, r
+    if len(rows) > 1:
+        raise ValueError(f"item id {item_id!r} exists in several cases; pass case=")
+    return table, rows[0]
 
 
 def _decode(row) -> dict:
@@ -122,8 +129,8 @@ def _decode(row) -> dict:
     return out
 
 
-def get_item(conn, item_id: str) -> dict:
-    return _decode(_find(conn, item_id)[1])
+def get_item(conn, item_id: str, case: str = None) -> dict:
+    return _decode(_find(conn, item_id, case)[1])
 
 
 def list_items(conn, case_id: str, kind: str) -> list:
@@ -131,27 +138,27 @@ def list_items(conn, case_id: str, kind: str) -> list:
     return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
 
 
-def update_item(conn, item_id: str, now: float = 0, **fields) -> None:
+def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
     """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
     fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
     locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
     if locked & set(fields):
         raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
-    table, _ = _find(conn, item_id)
+    table, found = _find(conn, item_id, case)
     bad = set(fields) - _cols(conn, table)
     if bad:
         raise ValueError(f"unknown {table} fields {sorted(bad)}")
     fields["updated_at"] = now
     sets = ", ".join(f"{k}=?" for k in fields)
-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [item_id])
+    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
 
 
-def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0) -> dict:
+def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
     """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
     item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
     if action not in ACTIONS:
         raise ValueError(f"invalid review action {action!r}")
-    table, row = _find(conn, item_id)
+    table, row = _find(conn, item_id, case)
     before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
     status = ACTIONS[action] or row["review_status"]
     new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
@@ -160,22 +167,22 @@ def apply_review(conn, item_id: str, action: str, edited: dict = None, now: floa
     after = {"review_status": status, "edited": new_edited}
     conn.execute("BEGIN")
     try:
-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=?",
-                     (status, _enc(new_edited), now, item_id))
+        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
+                     (status, _enc(new_edited), now, item_id, row["case_id"]))
         conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                      (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
         conn.execute("COMMIT")
     except Exception:
         conn.execute("ROLLBACK")
         raise
-    return get_item(conn, item_id)
+    return get_item(conn, item_id, row["case_id"])
 
 
-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None) -> None:
+def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
     if status not in REVIEW_STATUSES:
         raise ValueError(f"invalid review_status {status!r}")
     action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
-    apply_review(conn, item_id, action, edited=edited, now=now)
+    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
 
 
 def list_events(conn, case_id: str, item_id: str = None) -> list:
diff --git a/app/db/schema.sql b/app/db/schema.sql
index 7d991f8..7e97b6f 100644
--- a/app/db/schema.sql
+++ b/app/db/schema.sql
@@ -1,3 +1,4 @@
+-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
 -- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
 -- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
 CREATE TABLE IF NOT EXISTS cases (
@@ -8,36 +9,40 @@ CREATE TABLE IF NOT EXISTS cases (
   injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
 );
 CREATE TABLE IF NOT EXISTS records (
-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
+  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
   date_header_start INTEGER, date_header_end INTEGER, source_header_start INTEGER, source_header_end INTEGER,
   source_label TEXT, date_raw TEXT, date_iso TEXT,
   date_status TEXT CHECK (date_status IN ('parsed','ambiguous','missing','confirmed')),
-  date_candidates_json TEXT, duplicate_of TEXT, injection_tag INTEGER DEFAULT 0, encounter INTEGER DEFAULT 1
+  date_candidates_json TEXT, duplicate_of TEXT, injection_tag INTEGER DEFAULT 0, encounter INTEGER DEFAULT 1,
+  PRIMARY KEY (case_id, id)
 );
 CREATE TABLE IF NOT EXISTS entries (
-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
+  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
   provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
   state TEXT, state_reasons_json TEXT,
   review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
-  edited_json TEXT, ladder_json TEXT, updated_at REAL
+  edited_json TEXT, ladder_json TEXT, updated_at REAL,
+  PRIMARY KEY (case_id, id)
 );
 CREATE TABLE IF NOT EXISTS amounts (
-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
+  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
   text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
   excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
   state TEXT, state_reasons_json TEXT,
   review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
-  edited_json TEXT, ladder_json TEXT, updated_at REAL
+  edited_json TEXT, ladder_json TEXT, updated_at REAL,
+  PRIMARY KEY (case_id, id)
 );
 CREATE TABLE IF NOT EXISTS flags (
-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id),
+  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
   type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
   category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
   title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
   origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
   state TEXT, state_reasons_json TEXT,
   review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
-  edited_json TEXT, ladder_json TEXT, updated_at REAL
+  edited_json TEXT, ladder_json TEXT, updated_at REAL,
+  PRIMARY KEY (case_id, id)
 );
 -- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
 CREATE TABLE IF NOT EXISTS llm_calls (
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:59.857Z

**tool call — Bash**
````
{
 "command": "git show 6c3aeb1 -- tests/ 2>&1; echo \"---PIPELINE DIFF vs HEAD---\"; git diff HEAD -- app/backend/pipeline.py 2>&1",
 "description": "Show test diffs and pipeline WIP diff"
}
````

### User / tool · 2026-11-02T02:01:59.970Z

**tool result**
````
commit 6c3aeb14d78df77fdf244532fd5105624fef22fe
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:01:40 2026 -0600

    fix(db): per-case id namespacing via composite primary key (T-050)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index 9c4f124..d127e11 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -195,3 +195,15 @@ def test_no_text_in_logs(env, caplog, capsys):
     run_case(c)
     out = capsys.readouterr()
     assert "Jordan Rivera" not in caplog.text + out.out + out.err
+
+
+def test_two_cases_coexist_with_short_display_ids(env):
+    """T-050: the same short ids (e1, r1, f_gap_r6_r7) exist in two cases; review on one does not touch the other; delete is per case."""
+    _, c = env
+    a, b = run_case(c), run_case(c)
+    ga, gb = c.get(f"/api/cases/{a}").json(), c.get(f"/api/cases/{b}").json()
+    assert [e["id"] for e in ga["entries"]] == [e["id"] for e in gb["entries"]] and ga["entries"][0]["id"].startswith("e") and "." not in ga["entries"][0]["id"]
+    eid = ga["entries"][0]["id"]
+    assert c.post(f"/api/cases/{a}/items/{eid}/review", json={"action": "accept"}).status_code == 200
+    assert c.get(f"/api/cases/{b}").json()["entries"][0]["review_status"] == "pending"
+    assert c.delete(f"/api/cases/{a}").status_code == 204 and len(c.get(f"/api/cases/{b}").json()["entries"]) == 9
diff --git a/tests/unit/test_multicase.py b/tests/unit/test_multicase.py
new file mode 100644
index 0000000..1b63ab8
--- /dev/null
+++ b/tests/unit/test_multicase.py
@@ -0,0 +1,53 @@
+"""T-050: many cases share one sqlite file; ids are short per case and never collide; delete_case touches only its own rows."""
+import pytest
+from app.backend import pipeline as PL
+from app.db import db as DB
+from tests.unit import _golden as G
+from tests.unit._fakes import FakeCall, golden_summaries, which_record
+
+
+def seeded(conn, case, text):
+    cid = DB.create_case(conn, text, now=1.0)
+    PL.ingest_case(conn, cid, text, 1.0)
+    return cid
+
+
+def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
+    conn = DB.connect(str(tmp_path / "m.sqlite"))
+    a = seeded(conn, "sample", G.raw("sample"))
+    b = seeded(conn, "case_01", G.raw("case_01_date_formats"))
+    c = seeded(conn, "sample again", G.raw("sample"))
+    ids = lambda cid: sorted(r["id"] for r in DB.list_items(conn, cid, "flag"))   # noqa: E731
+    assert ids(a) == ids(c) and ids(a)                                              # same short ids in two cases
+    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (a,)).fetchone()[0] == 9
+    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (b,)).fetchone()[0] >= 8
+
+
+def test_full_pipeline_twice_in_one_file(tmp_path):
+    sums = golden_summaries()
+    script = {"extract": lambda u: dict(summary=sums[which_record(u)[0]][0], excerpt=sums[which_record(u)[0]][1]),
+              "j1": {"verdict": "supported", "reason": "r"}, "j2": {"verdict": "agree", "reason": "r"}, "j3": {"verdict": "conflict", "reason": "r"},
+              "j4": {"verdict": "agree", "reason": "r"}, "conflicts": {"flags": []}, "flags": {"flags": []}}
+    conn = DB.connect(str(tmp_path / "m.sqlite"))
+    outs = []
+    for _ in range(2):
+        cid = DB.create_case(conn, G.raw("sample"), now=1.0)
+        outs.append((cid, PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script), now=lambda: 1.0)))
+    (a, oa), (b, ob) = outs
+    assert [e["id"] for e in oa["entries"]] == [e["id"] for e in ob["entries"]] and len(oa["entries"]) == 9
+    eid = oa["entries"][0]["id"]
+    with pytest.raises(ValueError):                      # a bare id is ambiguous once two cases hold it
+        DB.get_item(conn, eid)
+    assert DB.get_item(conn, eid, a)["case_id"] == a and DB.get_item(conn, eid, b)["case_id"] == b
+    DB.apply_review(conn, eid, "accept", now=2.0, case=a)
+    assert DB.get_item(conn, eid, a)["review_status"] == "accepted" and DB.get_item(conn, eid, b)["review_status"] == "pending"
+
+
+def test_delete_case_removes_only_that_case(tmp_path):
+    conn = DB.connect(str(tmp_path / "m.sqlite"))
+    a = seeded(conn, "a", G.raw("sample"))
+    b = seeded(conn, "b", G.raw("sample"))
+    before = DB.table_counts(conn, b)
+    DB.delete_case(conn, a)
+    assert DB.get_case(conn, a) is None and DB.table_counts(conn, a).get("records", 0) == 0
+    assert DB.table_counts(conn, b) == before and before["records"] == 9
---PIPELINE DIFF vs HEAD---
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index d5f97e2..4e047ed 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -11,8 +11,8 @@ import sys
 import time
 from concurrent.futures import ThreadPoolExecutor
 
-from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, grounding, ingest as IN,
-                         judges, sentences, totals as TT, why as WHY)
+from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
+                         judges, totals as TT, why as WHY)
 from app.db import db as DB
 from app.llm import audited as AU, provider as P
 
@@ -82,8 +82,6 @@ def run_ingest(raw_text: str) -> dict:
     for a in AM.extract_amounts(recs):
         r = by_n[a["record_no"]]
         body = r["excerpt"]
-        base = generator.body_offset(r)
-        s = next((x for x in sentences.stripped_spans(body) if x[0] <= a["start"] - (r["char_start"] + (r["text"].find(body)))), None) if False else None
         item = {"id": a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
                 "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
                 "excerpt": body, "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
@@ -138,11 +136,11 @@ def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
         if old is None:
             DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
             continue
-        DB.update_item(conn, it["id"], now=now, **row)
+        DB.update_item(conn, it["id"], now=now, case=cid, **row)
         if kind == "flag" and old["review_status"] != "pending":
             oc = old.get("computed") or {}
             if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
-                DB.apply_review(conn, it["id"], "reset", now=now)
+                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
             else:
                 it["review_status"] = old["review_status"]
         elif old["review_status"] != "pending":
@@ -167,8 +165,6 @@ def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
 def _finish_amount(a: dict, ing: dict, judged) -> dict:
     """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
     by_n = {r["n"]: r for r in ing["records"]}
-    r = by_n[a["record_nos"][0]]
-    base = generator.body_offset(r)
     a = dict(a)
     a.update(excerpt_start=a["start"], excerpt_end=a["end"])
     verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
@@ -243,7 +239,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     if guard("verify"):
         pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
     if guard("judge_entries") and entries:
-        judges_failed = generator.judge_entries(entries, by_n, call=call, case_text=text)
+        generator.judge_entries(entries, by_n, call=call, case_text=text)
     for e in entries + rejected:
         e["ladder"]["backend"] = P.backend_name()
         e.pop("_stage", None)
@@ -319,6 +315,79 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
                        "verified": sum(1 for i in all_items if i["state"] == "verified")}}
 
 
+# ------------------------------------------------------------------ eval / API view
+def case_view(out: dict) -> dict:
+    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
+    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
+    flags = []
+    for f in out["flags"] + out["tray"]:
+        if "summary" in f:
+            continue
+        g = dict(f)
+        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
+        if f["type"] == "gap":
+            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
+        flags.append(g)
+    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
+            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
+            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
+            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
+            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}
+
+
+class _Backend:
+    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""
+
+    def __init__(self, name):
+        self.name, self.old = name, None
+
+    def __enter__(self):
+        import os
+        self.old = os.environ.get("LLM_BACKEND")
+        if self.name:
+            os.environ["LLM_BACKEND"] = self.name
+
+    def __exit__(self, *a):
+        import os
+        if self.old is None:
+            os.environ.pop("LLM_BACKEND", None)
+        else:
+            os.environ["LLM_BACKEND"] = self.old
+
+
+def _scratch_call(tmp, text):
+    import os
+    conn = DB.connect(os.path.join(tmp, "scratch.sqlite"))
+    cid = DB.create_case(conn, text, now=0.0)
+    return conn, cid, AU.make_call(conn, cid)
+
+
+def run_case(text: str, backend: str = None) -> dict:
+    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
+    import contextlib
+    import tempfile
+    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
+        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
+        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
+            out = run_pipeline(conn, cid, text, call=call)
+        view = case_view(out)
+        conn.close()
+        return view
+
+
+def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
+    """Judge 1 on one (summary, excerpt, label): 'supported' | 'partially' | 'unsupported' | 'unavailable'. A missing fixture or a failed call
+    is 'unavailable', never a pass."""
+    import contextlib
+    import tempfile
+    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
+        conn, cid, call = _scratch_call(tmp, excerpt)
+        with (P.record_context(excerpt) if P._recording() else contextlib.nullcontext()):
+            v = judges.run_j1(summary, excerpt, label, call=call)
+        conn.close()
+        return v
+
+
 # ------------------------------------------------------------------ CLI
 def _usd(c):
     return TT.usd(c)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:14.673Z

**tool call — Bash**
````
{
 "command": "echo \"---DB.py full---\" && cat -n app/db/db.py && echo \"---schema head/tail---\" && sed -n '1,12p;50,80p' app/db/schema.sql",
 "description": "Read db.py and schema in full"
}
````

### User / tool · 2026-11-02T02:02:14.759Z

**tool result**
````
---DB.py full---
     1	"""SQLite persistence (ADR-002, ADR-006). Owner: db.
     2	
     3	- Times are epoch seconds passed in by the caller (`now=`); nothing here reads the clock, so tests inject a fake one.
     4	- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
     5	- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
     6	- delete_case() is the one deletion path; purge_expired() calls it. Never log record text or prompts.
     7	"""
     8	import hashlib
     9	import json
    10	import os
    11	import secrets
    12	import sqlite3
    13	
    14	RETENTION_SECONDS = 24 * 3600
    15	REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
    16	ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
    17	           "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
    18	_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
    19	_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
    20	_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
    21	_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
    22	_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
    23	
    24	
    25	def init(path: str = ":memory:"):
    26	    return connect(path)
    27	
    28	
    29	def connect(path: str):
    30	    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
    31	    conn.row_factory = sqlite3.Row
    32	    conn.execute("PRAGMA secure_delete=ON")
    33	    conn.execute("PRAGMA foreign_keys=ON")
    34	    with open(_SCHEMA, encoding="utf-8") as f:
    35	        conn.executescript(f.read())
    36	    return conn
    37	
    38	
    39	def _tok(prefix: str) -> str:
    40	    return prefix + secrets.token_hex(6)
    41	
    42	
    43	def _enc(v):
    44	    return json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v
    45	
    46	
    47	def _cols(conn, table):
    48	    return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
    49	
    50	
    51	def sha256(text: str) -> str:
    52	    return hashlib.sha256(text.encode("utf-8")).hexdigest()
    53	
    54	
    55	def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
    56	    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
    57	    row = {"id": cid, "name": name, "source": source, "raw_text": raw_text, "text_sha256": sha256(raw_text),
    58	           "created_at": now, **fields}
    59	    _insert(conn, "cases", row)
    60	    return cid
    61	
    62	
    63	def update_case(conn, case_id: str, **fields) -> None:
    64	    ok = _cols(conn, "cases") - {"id", "created_at", "raw_text"}
    65	    bad = set(fields) - ok
    66	    if bad:
    67	        raise ValueError(f"unknown case fields {sorted(bad)}")
    68	    sets = ", ".join(f"{k}=?" for k in fields)
    69	    conn.execute(f"UPDATE cases SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [case_id])
    70	
    71	
    72	def get_case(conn, case_id: str):
    73	    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    74	    return _decode(r) if r else None
    75	
    76	
    77	def _insert(conn, table, row):
    78	    bad = set(row) - _cols(conn, table)
    79	    if bad:
    80	        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    81	    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
    82	                 [_enc(v) for v in row.values()])
    83	
    84	
    85	def add_record(conn, case_id: str, **fields) -> str:
    86	    rid = fields.pop("id", None) or _tok("r")
    87	    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
    88	    return rid
    89	
    90	
    91	def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
    92	    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
    93	    if kind not in _ITEM_TABLES:
    94	        raise ValueError(f"unknown item kind {kind!r}")
    95	    table, prefix = _ITEM_TABLES[kind]
    96	    p = dict(payload)
    97	    if {"review_status", "edited_json", "edited"} & set(p):
    98	        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
    99	    iid = p.pop("id", None) or _tok(prefix)
   100	    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
   101	    return iid
   102	
   103	
   104	def _find(conn, item_id, case=None):
   105	    """Item ids are unique per case (T-050). Pass `case` (the case id) whenever more than one case can share the file."""
   106	    kind = _PREFIX_KIND.get(item_id[:1])
   107	    if kind is None:
   108	        raise KeyError(item_id)
   109	    table = _ITEM_TABLE_OF[kind]
   110	    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
   111	    if case is not None:
   112	        q, a = q + " AND case_id=?", a + [case]
   113	    rows = conn.execute(q, a).fetchall()
   114	    if not rows:
   115	        raise KeyError(item_id)
   116	    if len(rows) > 1:
   117	        raise ValueError(f"item id {item_id!r} exists in several cases; pass case=")
   118	    return table, rows[0]
   119	
   120	
   121	def _decode(row) -> dict:
   122	    out = {}
   123	    for k in row.keys():
   124	        v = row[k]
   125	        if k.endswith("_json"):
   126	            out[k[:-5]] = json.loads(v) if v else None
   127	        else:
   128	            out[k] = v
   129	    return out
   130	
   131	
   132	def get_item(conn, item_id: str, case: str = None) -> dict:
   133	    return _decode(_find(conn, item_id, case)[1])
   134	
   135	
   136	def list_items(conn, case_id: str, kind: str) -> list:
   137	    table = _ITEM_TABLES[kind][0]
   138	    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
   139	
   140	
   141	def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
   142	    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
   143	    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
   144	    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
   145	    if locked & set(fields):
   146	        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
   147	    table, found = _find(conn, item_id, case)
   148	    bad = set(fields) - _cols(conn, table)
   149	    if bad:
   150	        raise ValueError(f"unknown {table} fields {sorted(bad)}")
   151	    fields["updated_at"] = now
   152	    sets = ", ".join(f"{k}=?" for k in fields)
   153	    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
   154	
   155	
   156	def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
   157	    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
   158	    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
   159	    if action not in ACTIONS:
   160	        raise ValueError(f"invalid review action {action!r}")
   161	    table, row = _find(conn, item_id, case)
   162	    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
   163	    status = ACTIONS[action] or row["review_status"]
   164	    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
   165	    if action == "edit" and not new_edited:
   166	        raise ValueError("edit requires a non-empty edited payload")
   167	    after = {"review_status": status, "edited": new_edited}
   168	    conn.execute("BEGIN")
   169	    try:
   170	        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
   171	                     (status, _enc(new_edited), now, item_id, row["case_id"]))
   172	        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
   173	                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
   174	        conn.execute("COMMIT")
   175	    except Exception:
   176	        conn.execute("ROLLBACK")
   177	        raise
   178	    return get_item(conn, item_id, row["case_id"])
   179	
   180	
   181	def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
   182	    if status not in REVIEW_STATUSES:
   183	        raise ValueError(f"invalid review_status {status!r}")
   184	    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
   185	    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
   186	
   187	
   188	def list_events(conn, case_id: str, item_id: str = None) -> list:
   189	    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
   190	    if item_id:
   191	        q, a = q + " AND item_id=?", a + [item_id]
   192	    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
   193	
   194	
   195	def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
   196	    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
   197	    cid = fields.pop("id", None) or _tok("c")
   198	    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
   199	           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
   200	    _insert(conn, "llm_calls", row)
   201	    return cid
   202	
   203	
   204	def get_llm_call(conn, call_id: str):
   205	    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
   206	    return _decode(r) if r else None
   207	
   208	
   209	def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
   210	    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
   211	    if item_id:
   212	        q, a = q + " AND item_id=?", a + [item_id]
   213	    return [_decode(r) for r in conn.execute(q + " ORDER BY created_at, rowid", a)]
   214	
   215	
   216	def delete_case(conn, case_id: str) -> None:
   217	    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
   218	    conn.execute("BEGIN")
   219	    try:
   220	        for t in _CASE_TABLES:
   221	            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
   222	        conn.execute("COMMIT")
   223	    except Exception:
   224	        conn.execute("ROLLBACK")
   225	        raise
   226	
   227	
   228	def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
   229	    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
   230	    for cid in ids:
   231	        delete_case(conn, cid)
   232	    return len(ids)
   233	
   234	
   235	def table_counts(conn, case_id: str) -> dict:
   236	    return {t: conn.execute(f"SELECT COUNT(*) FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,)).fetchone()[0]
   237	            for t in _CASE_TABLES}
---schema head/tail---
-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
-- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
-- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
  raw_text TEXT NOT NULL, text_sha256 TEXT,
  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
);
CREATE TABLE IF NOT EXISTS records (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
  parsed_ok INTEGER, verdict TEXT, attempt INTEGER DEFAULT 1, latency_ms INTEGER, cost_usd REAL,
  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS review_events (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording')),
  before_json TEXT, after_json TEXT, at REAL
);
CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:15.933Z

**tool call — Bash**
````
{
 "command": "echo \"---callers of DB item fns (non-test)---\" && grep -rn \"get_item\\|update_item\\|apply_review\\|set_review_status\\|_find(\\|delete_case\\|_drop(\\|list_events\" --include=*.py app | grep -v \"def \" ; echo \"---raw SQL w/o case_id---\"; grep -rn \"WHERE id=\\|WHERE id =\\|FROM flags\\|FROM entries\\|FROM amounts\\|FROM records\" --include=*.py app | grep -v case_id; echo \"---routes---\"; ls app/backend app/ 2>/dev/null; grep -rln \"APIRouter\\|FastAPI\\|@app\\.\\(get\\|post\\|delete\\)\" --include=*.py app",
 "description": "Find production callers and unscoped SQL"
}
````

### User / tool · 2026-11-02T02:02:16.046Z

**tool result**
````
---callers of DB item fns (non-test)---
app/backend/store.py:64:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
app/backend/present.py:88:    row = DB.get_item(conn, item_id, case_id)
app/backend/present.py:176:    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
app/backend/present.py:198:                       for e in DB.list_events(conn, case_id)],
app/backend/api.py:155:                DB.delete_case(c, cid)
app/backend/api.py:182:            DB.delete_case(c, token)
app/backend/api.py:273:            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
app/backend/review.py:29:        row = DB.get_item(conn, item_id, case_id)
app/backend/review.py:51:        DB.apply_review(conn, item_id, action, now=t, case=case_id)
app/backend/review.py:53:            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
app/backend/review.py:71:        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
app/backend/review.py:72:        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
app/backend/review.py:126:    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
app/backend/review.py:128:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
app/backend/review.py:134:    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/review.py:154:            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso)
app/backend/review.py:156:    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
app/backend/review.py:160:        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
app/backend/review.py:202:        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
app/backend/review.py:204:            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
app/backend/pipeline.py:139:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
app/backend/pipeline.py:143:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
app/db/db.py:4:- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
app/db/db.py:5:- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
app/db/db.py:6:- delete_case() is the one deletion path; purge_expired() calls it. Never log record text or prompts.
app/db/db.py:98:        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
app/db/db.py:133:    return _decode(_find(conn, item_id, case)[1])
app/db/db.py:142:    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
app/db/db.py:146:        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
app/db/db.py:147:    table, found = _find(conn, item_id, case)
app/db/db.py:161:    table, row = _find(conn, item_id, case)
app/db/db.py:178:    return get_item(conn, item_id, row["case_id"])
app/db/db.py:185:    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
app/db/db.py:231:        delete_case(conn, cid)
---raw SQL w/o case_id---
app/db/db.py:110:    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
app/db/db.py:205:    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
---routes---
app/:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

app/backend:
__init__.py
__pycache__
amounts.py
api.py
confidence.py
conflicts.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
pipeline.py
present.py
review.py
schemas.py
sentences.py
store.py
totals.py
why.py
app/backend/api.py
app/backend/export_routes.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:20.036Z

**tool call — Bash**
````
{
 "command": "echo \"--- working tree _persist ---\" && sed -n '120,160p' app/backend/pipeline.py | cat -n; echo \"--- HEAD _persist ---\"; git show HEAD:app/backend/pipeline.py | sed -n '125,150p' | cat -n; echo \"--- HEAD grep for get_item/_find in pipeline ---\"; git show HEAD:app/backend/pipeline.py | grep -n \"DB\\.\\(get_item\\|update_item\\|apply_review\\|add_item\\|list_items\\)\" ; echo \"--- app/pipeline.py ---\"; cat -n app/pipeline.py | head -30",
 "description": "Compare _persist in working tree vs HEAD"
}
````

### User / tool · 2026-11-02T02:02:20.161Z

**tool result**
````
--- working tree _persist ---
     1	                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
     2	    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
     3	                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
     4	    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
     5	            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
     6	            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
     7	
     8	
     9	def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
    10	    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    11	    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
    12	    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    13	    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    14	    for it in items:
    15	        row = _row(kind, it)
    16	        old = existing.get(it["id"])
    17	        if old is None:
    18	            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
    19	            continue
    20	        DB.update_item(conn, it["id"], now=now, case=cid, **row)
    21	        if kind == "flag" and old["review_status"] != "pending":
    22	            oc = old.get("computed") or {}
    23	            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
    24	                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
    25	            else:
    26	                it["review_status"] = old["review_status"]
    27	        elif old["review_status"] != "pending":
    28	            it["review_status"] = old["review_status"]
    29	    keep = {i["id"] for i in items}
    30	    for oid, old in existing.items():
    31	        if oid not in keep and old["review_status"] == "pending":
    32	            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
    33	
    34	
    35	def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    36	    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    37	    ing = run_ingest(raw_text)
    38	    _store_records(conn, cid, ing)
    39	    _persist(conn, cid, "flag", ing["flags"], now)
    40	    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    41	    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
--- HEAD _persist ---
     1	    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
     2	            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
     3	            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
     4	
     5	
     6	def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
     7	    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
     8	    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
     9	    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    10	    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    11	    for it in items:
    12	        row = _row(kind, it)
    13	        old = existing.get(it["id"])
    14	        if old is None:
    15	            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
    16	            continue
    17	        DB.update_item(conn, it["id"], now=now, **row)
    18	        if kind == "flag" and old["review_status"] != "pending":
    19	            oc = old.get("computed") or {}
    20	            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
    21	                DB.apply_review(conn, it["id"], "reset", now=now)
    22	            else:
    23	                it["review_status"] = old["review_status"]
    24	        elif old["review_status"] != "pending":
    25	            it["review_status"] = old["review_status"]
    26	    keep = {i["id"] for i in items}
--- HEAD grep for get_item/_find in pipeline ---
134:    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
139:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
141:        DB.update_item(conn, it["id"], now=now, **row)
145:                DB.apply_review(conn, it["id"], "reset", now=now)
--- app/pipeline.py ---
     1	"""`python -m app.pipeline <file>` (CONTRACT M2 CLI). The implementation lives in app/backend/pipeline.py."""
     2	from app.backend.pipeline import *  # noqa: F401,F403
     3	from app.backend.pipeline import main
     4	
     5	if __name__ == "__main__":
     6	    raise SystemExit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:20.601Z

**tool call — Bash**
````
{
 "command": "sed -n '1,60p' tests/unit/test_api_routes.py; echo \"--- golden dir ---\"; ls evals/golden/ 2>/dev/null; echo \"--- _golden.py ---\"; sed -n '1,40p' tests/unit/_golden.py",
 "description": "Read API route test env and golden helper"
}
````

### User / tool · 2026-11-02T02:02:20.688Z

**tool result**
````
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def wait_ready(c, tok):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
--- golden dir ---
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
--- _golden.py ---
"""Helpers: load golden records/expected files from evals/golden (the only test data; synthetic)."""
import json, pathlib, re
G = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"

def case_names():
    return sorted(p.name[:-len(".expected.json")] for p in G.glob("*.expected.json"))

def expected(case):
    return json.loads((G / f"{case}.expected.json").read_text())

def raw(case):
    return (G / f"{case}.txt").read_text()

def records(case):
    """[{n, date_raw, source, excerpt}] parsed from the golden paste format."""
    out = []
    for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', raw(case)):
        out.append(dict(n=int(m.group(1)), date_raw=m.group(2), source=m.group(3), excerpt=m.group(4)))
    return out

def record(case, n):
    return next(r for r in records(case) if r["n"] == n)

def export_blocks():
    t = (G / "sample.export.expected.txt").read_text()
    letter, notes = t.split("=== INTERNAL_NOTES_TEXT")
    return letter.split("\n", 1)[1], notes.split("\n", 1)[1]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:34.584Z

**tool call — Bash**
````
{
 "command": "echo \"--- default db path ---\"; grep -rn \"sqlite\\|DB_PATH\\|db_path\\|DATABASE\" --include=*.py app | grep -v \"^app/db/db.py\" | head -20; echo \"--- sqlite files in repo (excl venv) ---\"; find . -name \"*.sqlite*\" -not -path \"./.venv/*\" -not -path \"./node_modules/*\" 2>/dev/null | head; echo \"--- conn.execute in app ---\"; grep -rn \"conn.execute\" --include=*.py app | grep -v \"app/db/db.py\" | head -40; echo \"--- test_db / test_pipeline mentions of case-scoped ids ---\"; ls tests/unit/ | head -60; grep -n \"case=\\|coexist\\|two cases\\|namespac\" tests/unit/test_db.py tests/unit/test_pipeline.py 2>/dev/null | head",
 "description": "Check DB path defaults, raw SQL and test locations"
}
````

### User / tool · 2026-11-02T02:02:34.735Z

**tool result**
````
--- default db path ---
app/llm/audited.py:16:_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
app/llm/record.py:32:        conn = DB.connect(os.path.join(d, "rec.sqlite"))
app/backend/api.py:44:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
app/backend/api.py:45:    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
app/backend/api.py:46:    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
app/backend/api.py:48:    app.state.db_path = db_path
app/backend/api.py:51:    DB.connect(db_path).close()
app/backend/api.py:67:        return DB.connect(app.state.db_path)
app/backend/pipeline.py:360:    conn = DB.connect(os.path.join(tmp, "scratch.sqlite"))
app/backend/pipeline.py:432:        conn = DB.connect(a.db or os.path.join(d, "cli.sqlite"))
--- sqlite files in repo (excl venv) ---
./artifacts/review-evidence/tmp13651ilh/sample-0.sqlite
./artifacts/review-evidence/tmp_7ds_ih3/sample-1.sqlite
./artifacts/review-evidence/tmpq8_383ll/case_07_prompt_injection-0.sqlite
./artifacts/review-evidence/tmpr0ep3lxh/sample-0.sqlite
./artifacts/review-evidence/tmpexbqevaz/sample-2.sqlite
--- conn.execute in app ---
app/backend/store.py:19:    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
app/backend/present.py:84:    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
app/backend/review.py:142:    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
app/backend/review.py:150:    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
app/backend/review.py:168:    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
app/backend/review.py:198:            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
app/backend/review.py:205:    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
app/backend/pipeline.py:151:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
--- test_db / test_pipeline mentions of case-scoped ids ---
__init__.py
_fakes.py
_golden.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_boundaries.py
test_confidence.py
test_conflicts.py
test_dates.py
test_db.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_gaps.py
test_generator.py
test_grounding.py
test_ingest.py
test_injection.py
test_judges.py
test_multicase.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_t033_backend.py
test_t037_backend.py
test_totals.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:45.167Z

**tool call — Bash**
````
{
 "command": "sed -n '1,60p' tests/unit/_fakes.py; echo \"--- api.py run/ingest/delete section ---\"; grep -n \"def \\|run_pipeline\\|ingest_case\\|create_case\\|delete_case\" app/backend/api.py | head -80; echo \"--- HEAD case= check ---\"; git show HEAD:app/backend/pipeline.py | grep -c \"case=cid\"; git log --oneline 6c3aeb1..HEAD -- app/backend/pipeline.py app/db | cat",
 "description": "Read test fakes, API route wiring and HEAD pipeline state"
}
````

### User / tool · 2026-11-02T02:02:45.303Z

**tool result**
````
"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]


def sample_script(**over):
    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
          "conflicts": {"flags": []}, "flags": {"flags": []}}
    sc.update(over)
    return sc

def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
    from app.backend import pipeline as PL
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
--- api.py run/ingest/delete section ---
39:    def __init__(self, status, code, message="", detail=None):
44:def digest(text: str) -> str:
48:def recorded_hashes() -> set:
52:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
65:    def backend():
68:    def live_enabled():
71:    def demo_mode():
74:    def models():
77:    def conn():
80:    def make_call(c, cid):
86:    def pipeline_mod():
92:    def get_case(c, token):
100:    async def _api_error(_, e):
104:    async def _review_error(_, e):
108:    async def _http_error(_, e):
113:    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
118:    async def _validation(_, e):
122:    async def _headers(request, call_next):
141:    async def body_of(request: Request) -> dict:
162:    def health():
168:    async def create_case(request: Request):
185:            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None, source="sample" if sample else "paste",
188:                ing = pipeline_mod().ingest_case(c, cid, text, now)
192:                DB.delete_case(c, cid)
207:    def get_case_view(token: str):
216:    def delete_case(token: str):
220:            DB.delete_case(c, token)
225:    def _run_thread(token, raw):
229:            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
240:    async def run_case(token: str, request: Request):
263:    def status(token: str):
282:    async def confirm_date(token: str, rid: str, request: Request):
294:    def item(token: str, item_id: str):
306:    async def review_item(token: str, item_id: str, request: Request):
316:    def export(token: str):
340:    def audit(token: str):
--- HEAD case= check ---
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:04.367Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-050/head_6c3aeb1 artifacts/review-evidence/T-050/pre_6c3aeb1p && git archive 6c3aeb1 | tar -x -C artifacts/review-evidence/T-050/head_6c3aeb1 && git archive 6c3aeb1^ | tar -x -C artifacts/review-evidence/T-050/pre_6c3aeb1p && echo \"HEAD archive pipeline case= count: $(grep -c 'case=cid' artifacts/review-evidence/T-050/head_6c3aeb1/app/backend/pipeline.py)\"; echo \"pre archive db.py has _find(conn, item_id): $(grep -c 'def _find(conn, item_id)' artifacts/review-evidence/T-050/pre_6c3aeb1p/app/db/db.py)\"; git rev-parse --short 6c3aeb1^ HEAD; grep -n \"def run_pipeline\" -A4 app/backend/pipeline.py | head -8; grep -n \"def make_call\" -A5 app/llm/audited.py | head -10",
 "description": "Extract committed T-050 and pre-T-050 trees into evidence dir"
}
````

### User / tool · 2026-11-02T02:03:04.673Z

**tool result**
````
HEAD archive pipeline case= count: 0
pre archive db.py has _find(conn, item_id): 1
fatal: Needed a single revision
201:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
202-    clock = now if callable(now) else (lambda: time.time() if now is None else now)
203-    t0 = clock()
204-    call = call or AU.make_call(conn, cid, now=clock)
205-    errors, stage_done = [], []
100:def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
101-    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
102-    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
103-    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
104-
105-    def call(step, system, user, schema, *, item_id=None, validate=None):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:17.138Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py",
 "content": "\"\"\"T-050 reviewer probe (staff-engineer-reviewer). Read-only on product code.\n\nUsage: .venv/bin/python artifacts/review-evidence/T-050/t050_check.py <repo_root> <outdir>\n\nRuns two different golden cases back to back into ONE sqlite file:\n  Part A: DB + pipeline code path (ingest_case, run_pipeline with the fixture backend via AU.make_call).\n  Part B: the HTTP API path (create_app -> POST /api/cases -> POST /run -> review -> DELETE).\nThen checks: no collision, display ids short, bare-id lookup behaviour, review isolation, delete_case isolation.\n\"\"\"\nimport os\nimport re\nimport sqlite3\nimport sys\nimport time\n\nROOT, OUT = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ROOT)\nos.chdir(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.makedirs(OUT, exist_ok=True)\n\nfrom app.db import db as DB            # noqa: E402\nfrom app.backend import pipeline as PL  # noqa: E402\nfrom app.llm import audited as AU       # noqa: E402\nfrom tests.unit import _golden as G     # noqa: E402\n\nCASES = [\"sample\", \"case_01_date_formats\"]\nSHORT = re.compile(r\"^[a-z]+[0-9]+(_[a-z0-9_]+)?$\")   # r1, e5, f_gap_r6_r7 style\nTABLES = [\"records\", \"entries\", \"amounts\", \"flags\", \"llm_calls\", \"review_events\", \"cases\"]\n\n\ndef fresh(path):\n    for suffix in (\"\", \"-wal\", \"-shm\", \"-journal\"):\n        if os.path.exists(path + suffix):\n            os.remove(path + suffix)\n    return path\n\n\ndef raw_counts(path):\n    c = sqlite3.connect(path)\n    out = {}\n    for t in TABLES:\n        col = \"id\" if t == \"cases\" else \"case_id\"\n        out[t] = dict(c.execute(f\"SELECT {col}, COUNT(*) FROM {t} GROUP BY {col}\").fetchall())\n    c.close()\n    return out\n\n\ndef part_a(dbpath):\n    print(\"== PART A: DB + pipeline code path ==\")\n    conn = DB.connect(fresh(dbpath))\n    cids = {}\n    for case in CASES:\n        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)\n        PL.ingest_case(conn, cid, G.raw(case), 1.0)\n        cids[case] = cid\n    for case in CASES:\n        out = PL.run_pipeline(conn, cids[case], G.raw(case), call=AU.make_call(conn, cids[case]), now=lambda: 1.0)\n        print(f\"run_pipeline {case}: status={out.get('status')} entries={len(out['entries'])} \"\n              f\"amounts={len(out['amounts'])} flags={len(out['flags'])} errors={[e.get('code') for e in out.get('errors', [])]}\")\n    a, b = cids[CASES[0]], cids[CASES[1]]\n    for kind in (\"entry\", \"flag\", \"amount\"):\n        ia = [i[\"id\"] for i in DB.list_items(conn, a, kind)]\n        ib = [i[\"id\"] for i in DB.list_items(conn, b, kind)]\n        bad = [i for i in ia + ib if not SHORT.match(i)]\n        print(f\"{kind}: caseA={len(ia)} {ia[:4]}... caseB={len(ib)} {ib[:4]}... shared_ids={len(set(ia)&set(ib))} non_short={bad}\")\n    rc = raw_counts(dbpath)\n    print(\"rows per case (records/entries/amounts/flags):\",\n          {c: [rc[t].get(x, 0) for t in (\"records\", \"entries\", \"amounts\", \"flags\")] for c, x in ((\"A\", a), (\"B\", b))})\n    print(\"PK check:\", conn.execute(\"SELECT sql FROM sqlite_master WHERE name='entries'\").fetchone()[0].split(\"\\n\")[-1].strip())\n    eid = DB.list_items(conn, a, \"entry\")[0][\"id\"]\n    try:\n        DB.get_item(conn, eid)\n        print(f\"bare get_item({eid}) -> returned (no ambiguity error)\")\n    except ValueError as e:\n        print(f\"bare get_item({eid}) -> ValueError: {e}\")\n    DB.apply_review(conn, eid, \"accept\", now=2.0, case=a)\n    print(\"after accept in A: A=\", DB.get_item(conn, eid, a)[\"review_status\"], \" B=\", DB.get_item(conn, eid, b)[\"review_status\"])\n    before = {c: DB.table_counts(conn, c) for c in (a, b)}\n    DB.delete_case(conn, a)\n    after_b = DB.table_counts(conn, b)\n    print(\"delete_case(A): A counts now\", DB.table_counts(conn, a), \"| B unchanged:\", after_b == before[b], after_b)\n    print(\"A case row gone:\", DB.get_case(conn, a) is None, \"| B case row present:\", DB.get_case(conn, b) is not None)\n    conn.close()\n\n\ndef part_b(dbpath):\n    from fastapi.testclient import TestClient\n    from app.backend.api import create_app\n    print(\"== PART B: HTTP API path, one sqlite file ==\")\n    static = os.path.join(OUT, \"static\")\n    os.makedirs(static, exist_ok=True)\n    c = TestClient(create_app(fresh(dbpath), static_dir=static))\n    toks = {}\n    for case in CASES:\n        r = c.post(\"/api/cases\", json={\"text\": G.raw(case)})\n        print(f\"POST /api/cases {case}: {r.status_code}\")\n        toks[case] = r.json()[\"token\"]\n    for case in CASES:\n        t = toks[case]\n        rr = c.post(f\"/api/cases/{t}/run\", json={})\n        st = None\n        for _ in range(400):\n            st = c.get(f\"/api/cases/{t}/status\").json()\n            if st[\"status\"] in (\"ready\", \"failed\"):\n                break\n            time.sleep(0.25)\n        print(f\"run {case}: POST={rr.status_code} final status={st.get('status')} stage={st.get('stage')} error={st.get('error')}\")\n    views = {k: c.get(f\"/api/cases/{v}\").json() for k, v in toks.items()}\n    for k, v in views.items():\n        ids = [x[\"id\"] for x in v.get(\"entries\", []) + v.get(\"flags\", []) + v.get(\"amounts\", []) + v.get(\"records\", [])]\n        print(f\"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} non_short={[i for i in ids if not SHORT.match(i)]}\")\n    ta, tb = toks[CASES[0]], toks[CASES[1]]\n    eid = views[CASES[0]][\"entries\"][0][\"id\"]\n    rv = c.post(f\"/api/cases/{ta}/items/{eid}/review\", json={\"action\": \"accept\"})\n    print(f\"POST review {eid} on A: {rv.status_code}; A status={c.get(f'/api/cases/{ta}').json()['entries'][0]['review_status']} \"\n          f\"B same-id status={c.get(f'/api/cases/{tb}').json()['entries'][0]['review_status']}\")\n    bids = [e[\"id\"] for e in c.get(f\"/api/cases/{tb}\").json()[\"entries\"]]\n    ids_a = [e[\"id\"] for e in c.get(f\"/api/cases/{ta}\").json()[\"entries\"]]\n    print(\"entry id lists identical across cases (short ids, no collision):\", ids_a == bids, ids_a[:5])\n    cnt = lambda: {t: 0 for t in []}  # placeholder, real counts from sqlite below\n    rc0 = raw_counts(dbpath)\n    d = c.delete(f\"/api/cases/{ta}\")\n    rc1 = raw_counts(dbpath)\n    print(f\"DELETE A: {d.status_code}; B rows unchanged across all tables:\",\n          all(rc1[t].get(tb, 0) == rc0[t].get(tb, 0) for t in TABLES),\n          \"| A rows left:\", {t: rc1[t].get(ta, 0) for t in TABLES})\n    print(\"B still served after A delete, entries:\", len(c.get(f\"/api/cases/{tb}\").json()[\"entries\"]))\n\n\nif __name__ == \"__main__\":\n    part_a(os.path.join(OUT, \"partA.sqlite\"))\n    part_b(os.path.join(OUT, \"partB.sqlite\"))\n"
}
````

### User / tool · 2026-11-02T02:03:17.234Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:18.542Z

**tool call — Bash**
````
{
 "command": "timeout 240 .venv/bin/python artifacts/review-evidence/T-050/t050_check.py /Users/arsis/zlayt-pm-project artifacts/review-evidence/T-050/worktree 2>&1 | tail -60",
 "description": "Run two-case probe against working tree",
 "timeout": 260000
}
````

### User / tool · 2026-11-02T02:03:18.622Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:20.231Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-050/t050_check.py /Users/arsis/zlayt-pm-project artifacts/review-evidence/T-050/worktree 2>&1 | tail -60",
 "description": "Run two-case probe against working tree",
 "timeout": 280000
}
````

### User / tool · 2026-11-02T02:03:21.515Z

**tool result**
````
llm call failed call_id=c3579bad7820d step=j1 attempt=1 prompt_hash=97c5477ae31d518466eb89335e224b86f8802be67c4c47df47c69b3b0bfc5346
llm call failed call_id=ca58a6b2b3afe step=j1 attempt=1 prompt_hash=4a67bc43647dbcca4719ede9547e025faa9435bb73a18186d797de279c302ee0
llm call failed call_id=c11c1e2d5b01d step=j2 attempt=1 prompt_hash=067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd
llm call failed call_id=c460b03601687 step=j4 attempt=1 prompt_hash=57cf618ce07cfa4ddfc12c278b60f8f458afa7f23a630bffe4ab07b201eb65e5
llm call failed call_id=ccfb644606cab step=j4 attempt=1 prompt_hash=60d2f600a71ab79faa3e48a93dde4d078ed9f4c370b48117662e893fa5da2a09
llm call failed call_id=c7b1d80498526 step=j1 attempt=1 prompt_hash=56e115e914a9dd3fc4cabf30d389f6c5c1f234bf487ab9fc8e24580dc19e0240
llm call failed call_id=c11626763cfb2 step=j1 attempt=1 prompt_hash=e52e60e1ed00713dbc3ea960404b10cfd5913ab988731c4bce782b0385363f98
llm call failed call_id=c1ab898d0cc2b step=j1 attempt=1 prompt_hash=d7294736d7aed62bf466fd10b0fa5006352e73613509ed8b7c5cbdec4ce41a5e
llm call failed call_id=cc39eddd3e437 step=j1 attempt=1 prompt_hash=6f6f6b3cd32ab2a827055d485be8e628585d46e5994fcab4c38e6c8dae4b73cb
llm call failed call_id=c4d349562df84 step=j1 attempt=1 prompt_hash=bcea6ba7d7b0914996ffd1e587988953107f3cae9d6dd3776912d959f44a9e26
llm call failed call_id=c3a2395fe9ef0 step=j1 attempt=1 prompt_hash=dbfd58f8dd566dfd0c83eb9cc838c37b8b845e9835e931aa1e22b9e23c444b6c
llm call failed call_id=c3cd61ebae25c step=j1 attempt=1 prompt_hash=c930c148e45f7e0a01a1c7d23b743c02b45b9b4c2c690f0aeca16618455cf97d
llm call failed call_id=c443ae0920260 step=j1 attempt=1 prompt_hash=78e9a6eb0aaea08b812e2a76b790366556359202a7544b9b638a3720cf48ae1c
llm call failed call_id=c15dfd560dd4c step=j1 attempt=1 prompt_hash=056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d
llm call failed call_id=c78b3b9a6d228 step=j2 attempt=1 prompt_hash=632a0e6302845a76592de8f53c07e4809ea08d9727f280e2e72b226c9faa5aa7
llm call failed call_id=c8d945fd32eee step=j2 attempt=1 prompt_hash=f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c
llm call failed call_id=c09c03ac0498b step=j2 attempt=1 prompt_hash=8258d36c1cdad8d5f84566c7d7ccb6f8cbdf043cc018ab771440220878c84c96
llm call failed call_id=c9dcf9804ff97 step=j3 attempt=1 prompt_hash=3787bdabbca433ea035220bcef2d7bc9c295375c65ba9617445d10a094d2515f
llm call failed call_id=cbdb5891ed306 step=j4 attempt=1 prompt_hash=9e3c8633aeea3fd87eb055c6d34203f7c33762b0fd3742d9ccee371ee7722f2b
llm call failed call_id=cb72f77f574ed step=j4 attempt=1 prompt_hash=f9e4dc3c09ef6fd906b6646bfc9a693611a8aa1f0f8e020cf9f104c0687862fa
llm call failed call_id=c028090d25810 step=j4 attempt=1 prompt_hash=d33f0f6bd5a79114deff14a84772c6ef2e30f9ed9c9591f366aaf53d58f27f70
llm call failed call_id=c200701b67df5 step=j4 attempt=1 prompt_hash=98c9ecc5fc199e17a2582926e896eae01b3c2a720f8c67ba84fe739fb4394f2f
llm call failed call_id=ce1c8a5ccf6d4 step=j4 attempt=1 prompt_hash=3ab32c7b388852f1fb66117225fd377dd8ea392d767c2664031a6a037df64caf
llm call failed call_id=ca321908f9f17 step=j4 attempt=1 prompt_hash=29ee418c79119a6311c1e2d6b9210fd3c4fd01f152f1dcef5a6acc0d5b917d58
llm call failed call_id=c93ea81b7c455 step=j4 attempt=1 prompt_hash=9391f6bf99db12e040f88843580adab24a5b2b06eab51ee982d85c36d2c761db
llm call failed call_id=c76a9e0ec4ca7 step=j4 attempt=1 prompt_hash=664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c
llm call failed call_id=c0e43312a335a step=j1 attempt=1 prompt_hash=37f588e1e562428cfaa109749b24600ce2fe250be9f99536047ef79e8dd79c78
llm call failed call_id=c0960cc59fa43 step=j1 attempt=1 prompt_hash=4d0039605f4eda08fc878c0b9559185e8df9b8a3ca732112d64abe5197f59f85
llm call failed call_id=c40e36fae3819 step=j1 attempt=1 prompt_hash=fc789ea36ae435903b9c77dc0a7163947534302b7cecd9cd078b5a9c915d3456
llm call failed call_id=c325b778aef44 step=j1 attempt=1 prompt_hash=ac6129be7b1a814113f8ad392c9fe34b267b7dccb7393531c513fb49fcab82f3
llm call failed call_id=ce38b70b0ba6c step=j1 attempt=1 prompt_hash=5ef978e652e30168fc71e2f22322219adb3fe1f8134c003d0652bedd9dfc0374
llm call failed call_id=c43bf778d0ce0 step=j1 attempt=1 prompt_hash=49667de16a2c245e1e6e54e5999fcb7566b5d578d27c9b09015781885e9b515a
llm call failed call_id=cec859462d4c5 step=j1 attempt=1 prompt_hash=97c5477ae31d518466eb89335e224b86f8802be67c4c47df47c69b3b0bfc5346
llm call failed call_id=c552f614cd601 step=j1 attempt=1 prompt_hash=4a67bc43647dbcca4719ede9547e025faa9435bb73a18186d797de279c302ee0
llm call failed call_id=cc207bb082a1d step=j2 attempt=1 prompt_hash=067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd
llm call failed call_id=c433059e40c28 step=j4 attempt=1 prompt_hash=57cf618ce07cfa4ddfc12c278b60f8f458afa7f23a630bffe4ab07b201eb65e5
llm call failed call_id=c18375028f172 step=j4 attempt=1 prompt_hash=60d2f600a71ab79faa3e48a93dde4d078ed9f4c370b48117662e893fa5da2a09
== PART A: DB + pipeline code path ==
run_pipeline sample: status=done entries=9 amounts=3 flags=11 errors=[]
run_pipeline case_01_date_formats: status=done entries=7 amounts=1 flags=3 errors=[]
entry: caseA=9 ['e1', 'e2', 'e3', 'e4']... caseB=8 ['e1', 'e2', 'e3', 'e4']... shared_ids=8 non_short=[]
flag: caseA=11 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1']... caseB=3 ['f_date_r8', 'f_r1_1', 'f_r7_1']... shared_ids=1 non_short=['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1', 'f_r8_1', 'f_r2_1', 'f_r6_1', 'f_r7_1', 'f_r7_2', 'f_r8_2', 'f_r9_1', 'f_date_r8', 'f_r1_1', 'f_r7_1']
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 9, 4, 11], 'B': [8, 8, 1, 3]}
PK check: )
bare get_item(e1) -> ValueError: item id 'e1' exists in several cases; pass case=
after accept in A: A= accepted  B= pending
delete_case(A): A counts now {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0} | B unchanged: True {'records': 8, 'entries': 8, 'amounts': 1, 'flags': 3, 'llm_calls': 28, 'review_events': 0, 'cases': 1}
A case row gone: True | B case row present: True
== PART B: HTTP API path, one sqlite file ==
POST /api/cases sample: 201
POST /api/cases case_01_date_formats: 201
run sample: POST=202 final status=ready stage=finalize error=None
run case_01_date_formats: POST=202 final status=ready stage=finalize error=None
API view sample: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=33 non_short=['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1', 'f_r8_1', 'f_r2_1', 'f_r6_1', 'f_r7_1', 'f_r7_2', 'f_r8_2', 'f_r9_1']
API view case_01_date_formats: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=19 non_short=['f_date_r8', 'f_r1_1', 'f_r7_1']
POST review e1 on A: 200; A status=accepted B same-id status=pending
entry id lists identical across cases (short ids, no collision): False ['e1', 'e2', 'e3', 'e4', 'e5']
DELETE A: 204; B rows unchanged across all tables: True | A rows left: {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0}
B still served after A delete, entries: 7
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:38.870Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050 && .venv/bin/python - <<'EOF' 2>/dev/null || true\nEOF\ncd /Users/arsis/zlayt-pm-project && python3 - <<'EOF'\nimport re\np = \"artifacts/review-evidence/T-050/t050_check.py\"\ns = open(p).read()\ns = s.replace('SHORT = re.compile(r\"^[a-z]+[0-9]+(_[a-z0-9_]+)?$\")   # r1, e5, f_gap_r6_r7 style',\n              'SHORT = re.compile(r\"^[a-z][a-z0-9_]{0,40}$\")   # r1, e5, f_gap_r6_r7 style: no case token, no random hex suffix\\nRANDOM_TOKEN = re.compile(r\"[0-9a-f]{12}\")                 # secrets.token_hex(6) would show up here')\ns = s.replace('bad = [i for i in ia + ib if not SHORT.match(i)]',\n              'bad = [i for i in ia + ib if not SHORT.match(i) or RANDOM_TOKEN.search(i)]')\ns = s.replace('non_short={[i for i in ids if not SHORT.match(i)]}', 'x')\ns = s.replace('''    print(\"PK check:\", conn.execute(\"SELECT sql FROM sqlite_master WHERE name='entries'\").fetchone()[0].split(\"\\\\n\")[-1].strip())''',\n'''    sql = conn.execute(\"SELECT sql FROM sqlite_master WHERE name='entries'\").fetchone()[0]\n    print(\"entries PK clause:\", re.findall(r\"PRIMARY KEY \\\\([^)]*\\\\)\", sql))\n    states = {c: conn.execute(\"SELECT state, COUNT(*) FROM entries WHERE case_id=? GROUP BY state\", (x,)).fetchall() for c, x in ((\"A\", a), (\"B\", b))}\n    print(\"entry states per case:\", {k: [tuple(r) for r in v] for k, v in states.items()})''')\ns = s.replace('''    for case in CASES:\n        out = PL.run_pipeline(conn, cids[case], G.raw(case), call=AU.make_call(conn, cids[case]), now=lambda: 1.0)\n        print(f\"run_pipeline {case}: status={out.get('status')} entries={len(out['entries'])} \"\n              f\"amounts={len(out['amounts'])} flags={len(out['flags'])} errors={[e.get('code') for e in out.get('errors', [])]}\")''',\n'''    for case in CASES:\n        try:\n            out = PL.run_pipeline(conn, cids[case], G.raw(case), call=AU.make_call(conn, cids[case]), now=lambda: 1.0)\n        except Exception as e:  # probe only: report the exception instead of crashing the probe\n            print(f\"run_pipeline {case}: RAISED {type(e).__name__}: {e}\")\n            continue\n        print(f\"run_pipeline {case}: status={out.get('status')} entries={len(out['entries'])} \"\n              f\"amounts={len(out['amounts'])} flags={len(out['flags'])} errors={[e.get('code') for e in out.get('errors', [])]}\")''')\ns = s.replace('''    ids_a = [e[\"id\"] for e in c.get(f\"/api/cases/{ta}\").json()[\"entries\"]]\n    print(\"entry id lists identical across cases (short ids, no collision):\", ids_a == bids, ids_a[:5])''',\n'''    ids_a = [e[\"id\"] for e in c.get(f\"/api/cases/{ta}\").json()[\"entries\"]]\n    print(\"API entry ids A:\", ids_a, \"| B:\", bids)\n    print(\"API shared entry ids A&B:\", sorted(set(ids_a) & set(bids)), \"| all short:\", all(SHORT.match(i) and not RANDOM_TOKEN.search(i) for i in ids_a + bids))''')\ns = s.replace('''    cnt = lambda: {t: 0 for t in []}  # placeholder, real counts from sqlite below\n''', \"\")\ns = s.replace('''        ids = [x[\"id\"] for x in v.get(\"entries\", []) + v.get(\"flags\", []) + v.get(\"amounts\", []) + v.get(\"records\", [])]\n        print(f\"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} non_short={[i for i in ids if not SHORT.match(i)]}\")''',\n'''        ids = [x[\"id\"] for x in v.get(\"entries\", []) + v.get(\"flags\", []) + v.get(\"amounts\", []) + v.get(\"records\", [])]\n        print(f\"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} \"\n              f\"non_short={[i for i in ids if not (SHORT.match(i) and not RANDOM_TOKEN.search(i))]}\")''')\nopen(p, \"w\").write(s)\nprint(\"ok\")\nEOF\ngrep -n \"SHORT\\|RANDOM_TOKEN\\|RAISED\\|PK clause\" artifacts/review-evidence/T-050/t050_check.py | head -20",
 "description": "Patch probe script regexes and reporting"
}
````

### User / tool · 2026-11-02T02:03:38.988Z

**tool result**
````
ok
30:SHORT = re.compile(r"^[a-z][a-z0-9_]{0,40}$")   # r1, e5, f_gap_r6_r7 style: no case token, no random hex suffix
31:RANDOM_TOKEN = re.compile(r"[0-9a-f]{12}")                 # secrets.token_hex(6) would show up here
64:            print(f"run_pipeline {case}: RAISED {type(e).__name__}: {e}")
72:        bad = [i for i in ia + ib if not SHORT.match(i) or RANDOM_TOKEN.search(i)]
78:    print("entries PK clause:", re.findall(r"PRIMARY KEY \([^)]*\)", sql))
131:    print("API shared entry ids A&B:", sorted(set(ids_a) & set(bids)), "| all short:", all(SHORT.match(i) and not RANDOM_TOKEN.search(i) for i in ids_a + bids))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:41.752Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-050/t050_check.py /Users/arsis/zlayt-pm-project artifacts/review-evidence/T-050/worktree > artifacts/review-evidence/T-050/worktree/stdout.txt 2> artifacts/review-evidence/T-050/worktree/stderr.txt; echo \"exit=$?\"; cat artifacts/review-evidence/T-050/worktree/stdout.txt; echo \"--- stderr lines: $(wc -l < artifacts/review-evidence/T-050/worktree/stderr.txt); distinct messages:\"; sed -E 's/call_id=[^ ]+//; s/prompt_hash=[^ ]+//' artifacts/review-evidence/T-050/worktree/stderr.txt | sort | uniq -c | head",
 "description": "Run probe on working tree, saving stdout and stderr"
}
````

### User / tool · 2026-11-02T02:03:43.044Z

**tool result**
````
exit=0
== PART A: DB + pipeline code path ==
run_pipeline sample: status=done entries=9 amounts=3 flags=11 errors=[]
run_pipeline case_01_date_formats: status=done entries=7 amounts=1 flags=3 errors=[]
entry: caseA=9 ['e1', 'e2', 'e3', 'e4']... caseB=8 ['e1', 'e2', 'e3', 'e4']... shared_ids=8 non_short=[]
flag: caseA=11 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1']... caseB=3 ['f_date_r8', 'f_r1_1', 'f_r7_1']... shared_ids=1 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 9, 4, 11], 'B': [8, 8, 1, 3]}
entries PK clause: ['PRIMARY KEY (case_id, id)']
entry states per case: {'A': [('needs_review', 9)], 'B': [('needs_review', 8)]}
bare get_item(e1) -> ValueError: item id 'e1' exists in several cases; pass case=
after accept in A: A= accepted  B= pending
delete_case(A): A counts now {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0} | B unchanged: True {'records': 8, 'entries': 8, 'amounts': 1, 'flags': 3, 'llm_calls': 28, 'review_events': 0, 'cases': 1}
A case row gone: True | B case row present: True
== PART B: HTTP API path, one sqlite file ==
POST /api/cases sample: 201
POST /api/cases case_01_date_formats: 201
run sample: POST=202 final status=ready stage=finalize error=None
run case_01_date_formats: POST=202 final status=ready stage=finalize error=None
API view sample: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=33 x
API view case_01_date_formats: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=19 x
POST review e1 on A: 200; A status=accepted B same-id status=pending
API entry ids A: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9'] | B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']
API shared entry ids A&B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7'] | all short: True
DELETE A: 204; B rows unchanged across all tables: True | A rows left: {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0}
B still served after A delete, entries: 7
--- stderr lines:       64; distinct messages:
  34 llm call failed  step=j1 attempt=1 
   8 llm call failed  step=j2 attempt=1 
   2 llm call failed  step=j3 attempt=1 
  20 llm call failed  step=j4 attempt=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:48.976Z

**tool call — Bash**
````
{
 "command": "grep -n \"API view\" -A2 artifacts/review-evidence/T-050/t050_check.py",
 "description": "Locate the API view print line in probe"
}
````

### User / tool · 2026-11-02T02:03:49.061Z

**tool result**
````
122:        print(f"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} x")
123-    ta, tb = toks[CASES[0]], toks[CASES[1]]
124-    eid = views[CASES[0]]["entries"][0]["id"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:50.665Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py",
 "old_string": "        print(f\"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} x\")",
 "new_string": "        bad = [i for i in ids if not (SHORT.match(i) and not RANDOM_TOKEN.search(i))]\n        print(f\"API view {k}: entries={[e['id'] for e in v.get('entries', [])][:5]} n_ids={len(ids)} non_short={bad}\")"
}
````

### User / tool · 2026-11-02T02:03:50.757Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:53.255Z

**tool call — Bash**
````
{
 "command": "W=artifacts/review-evidence/T-050/worktree; .venv/bin/python artifacts/review-evidence/T-050/t050_check.py /Users/arsis/zlayt-pm-project $W > $W/stdout.txt 2> $W/stderr.txt; echo \"exit=$?\"; grep \"API view\\|API entry\\|shared\" $W/stdout.txt; echo \"--- reason codes for one worktree entry ---\"; .venv/bin/python -c \"\nimport sqlite3,sys\nc=sqlite3.connect('$W/partA.sqlite')\nprint(c.execute('SELECT id, state, state_reasons_json FROM entries LIMIT 2').fetchall())\n\" ; echo \"--- HEAD (6c3aeb1) tree ---\"; H=artifacts/review-evidence/T-050/head_6c3aeb1; mkdir -p $H/out && .venv/bin/python artifacts/review-evidence/T-050/t050_check.py /Users/arsis/zlayt-pm-project $H/out > $H/stdout.txt 2> $H/stderr.txt; echo \"exit=$?\"; cat $H/stdout.txt | head -30",
 "description": "Rerun probe on working tree and HEAD archive"
}
````

### User / tool · 2026-11-02T02:03:55.787Z

**tool result**
````
exit=0
entry: caseA=9 ['e1', 'e2', 'e3', 'e4']... caseB=8 ['e1', 'e2', 'e3', 'e4']... shared_ids=8 non_short=[]
flag: caseA=11 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1']... caseB=3 ['f_date_r8', 'f_r1_1', 'f_r7_1']... shared_ids=1 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
API view sample: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=33 non_short=[]
API view case_01_date_formats: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=19 non_short=[]
API entry ids A: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9'] | B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']
API shared entry ids A&B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7'] | all short: True
--- reason codes for one worktree entry ---
[('e1', 'needs_review', '["JUDGE_UNAVAILABLE"]'), ('e2', 'needs_review', '["JUDGE_UNAVAILABLE"]')]
--- HEAD (6c3aeb1) tree ---
exit=0
== PART A: DB + pipeline code path ==
run_pipeline sample: status=done entries=9 amounts=3 flags=11 errors=[]
run_pipeline case_01_date_formats: status=done entries=7 amounts=1 flags=3 errors=[]
entry: caseA=9 ['e1', 'e2', 'e3', 'e4']... caseB=8 ['e1', 'e2', 'e3', 'e4']... shared_ids=8 non_short=[]
flag: caseA=11 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1']... caseB=3 ['f_date_r8', 'f_r1_1', 'f_r7_1']... shared_ids=1 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 9, 4, 11], 'B': [8, 8, 1, 3]}
entries PK clause: ['PRIMARY KEY (case_id, id)']
entry states per case: {'A': [('needs_review', 9)], 'B': [('needs_review', 8)]}
bare get_item(e1) -> ValueError: item id 'e1' exists in several cases; pass case=
after accept in A: A= accepted  B= pending
delete_case(A): A counts now {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0} | B unchanged: True {'records': 8, 'entries': 8, 'amounts': 1, 'flags': 3, 'llm_calls': 28, 'review_events': 0, 'cases': 1}
A case row gone: True | B case row present: True
== PART B: HTTP API path, one sqlite file ==
POST /api/cases sample: 201
POST /api/cases case_01_date_formats: 201
run sample: POST=202 final status=ready stage=finalize error=None
run case_01_date_formats: POST=202 final status=ready stage=finalize error=None
API view sample: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=33 non_short=[]
API view case_01_date_formats: entries=['e1', 'e2', 'e3', 'e4', 'e5'] n_ids=19 non_short=[]
POST review e1 on A: 200; A status=accepted B same-id status=pending
API entry ids A: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9'] | B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']
API shared entry ids A&B: ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7'] | all short: True
DELETE A: 204; B rows unchanged across all tables: True | A rows left: {'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0, 'cases': 0}
B still served after A delete, entries: 7
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:00.614Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050; H=$R/head_6c3aeb1; rm -rf $H/out; mkdir -p $H/out; .venv/bin/python $R/t050_check.py $H $H/out > $H/stdout.txt 2> $H/stderr.txt; echo \"HEAD exit=$?\"; cat $H/stdout.txt; echo \"--- HEAD stderr non-judge lines ---\"; grep -v \"llm call failed\" $H/stderr.txt | head -30; echo \"--- pre-T050 (6c3aeb1^) ---\"; P=$R/pre_6c3aeb1p; rm -rf $P/out; mkdir -p $P/out; .venv/bin/python $R/t050_check.py $P $P/out > $P/stdout.txt 2> $P/stderr.txt; echo \"PRE exit=$?\"; cat $P/stdout.txt | head -30; echo \"--- PRE stderr non-judge lines ---\"; grep -v \"llm call failed\" $P/stderr.txt | tail -15",
 "description": "Run probe against HEAD archive and pre-T-050 archive"
}
````

### User / tool · 2026-11-02T02:04:01.316Z

**tool result**
````
HEAD exit=1
== PART A: DB + pipeline code path ==
run_pipeline sample: RAISED ValueError: item id 'a1' exists in several cases; pass case=
run_pipeline case_01_date_formats: RAISED ValueError: item id 'a1' exists in several cases; pass case=
entry: caseA=0 []... caseB=0 []... shared_ids=0 non_short=[]
flag: caseA=2 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7']... caseB=1 ['f_date_r8']... shared_ids=0 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 0, 4, 2], 'B': [8, 0, 1, 1]}
entries PK clause: ['PRIMARY KEY (case_id, id)']
entry states per case: {'A': [], 'B': []}
--- HEAD stderr non-judge lines ---
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 143, in <module>
    part_a(os.path.join(OUT, "partA.sqlite"))
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 81, in part_a
    eid = DB.list_items(conn, a, "entry")[0]["id"]
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
--- pre-T050 (6c3aeb1^) ---
PRE exit=1
== PART A: DB + pipeline code path ==
--- PRE stderr non-judge lines ---
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 143, in <module>
    part_a(os.path.join(OUT, "partA.sqlite"))
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 58, in part_a
    PL.ingest_case(conn, cid, G.raw(case), 1.0)
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p/app/backend/pipeline.py", line 159, in ingest_case
    _store_records(conn, cid, ing)
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p/app/backend/pipeline.py", line 106, in _store_records
    DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p/app/db/db.py", line 86, in add_record
    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p/app/db/db.py", line 80, in _insert
    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
sqlite3.IntegrityError: UNIQUE constraint failed: records.id
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:09.308Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np = \"artifacts/review-evidence/T-050/t050_check.py\"\ns = open(p).read()\nold = '''    for case in CASES:\n        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)\n        PL.ingest_case(conn, cid, G.raw(case), 1.0)\n        cids[case] = cid'''\nnew = '''    for case in CASES:\n        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)\n        cids[case] = cid\n        try:\n            PL.ingest_case(conn, cid, G.raw(case), 1.0)\n        except Exception as e:  # probe only: report instead of crashing\n            print(f\"ingest_case {case}: RAISED {type(e).__name__}: {e}\")'''\nassert old in s; s = s.replace(old, new)\nold2 = '''    eid = DB.list_items(conn, a, \"entry\")[0][\"id\"]\n    try:'''\nnew2 = '''    if not DB.list_items(conn, a, \"entry\"):\n        print(\"no entries in case A: skipping bare-id and review checks\")\n        conn.close()\n        return\n    eid = DB.list_items(conn, a, \"entry\")[0][\"id\"]\n    try:'''\nassert old2 in s; s = s.replace(old2, new2)\nopen(p, \"w\").write(s); print(\"patched\")\nEOF\nR=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050; for v in head_6c3aeb1 pre_6c3aeb1p; do D=$R/$v; rm -rf $D/out; mkdir -p $D/out; .venv/bin/python $R/t050_check.py $D $D/out > $D/stdout.txt 2> $D/stderr.txt; echo \"== $v exit=$?\"; cat $D/stdout.txt; echo \"-- non-judge stderr (tail):\"; grep -v \"llm call failed\" $D/stderr.txt | tail -4; done",
 "description": "Patch probe and rerun HEAD and pre-T-050 archives"
}
````

### User / tool · 2026-11-02T02:04:09.361Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion (/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/$v/out) is blocked | command: python3 - <<'EOF'
p = "artifacts/review-evidence/T-050/t050_check.py"
s = open(p).read()
old = '''    for case in CASES:
        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)
        PL.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:11.580Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py",
 "old_string": "    for case in CASES:\n        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)\n        PL.ingest_case(conn, cid, G.raw(case), 1.0)\n        cids[case] = cid",
 "new_string": "    for case in CASES:\n        cid = DB.create_case(conn, G.raw(case), now=1.0, name=case)\n        cids[case] = cid\n        try:\n            PL.ingest_case(conn, cid, G.raw(case), 1.0)\n        except Exception as e:  # probe only: report instead of crashing\n            print(f\"ingest_case {case}: RAISED {type(e).__name__}: {e}\")"
}
````

### User / tool · 2026-11-02T02:04:11.675Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:12.312Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py",
 "old_string": "    eid = DB.list_items(conn, a, \"entry\")[0][\"id\"]\n    try:",
 "new_string": "    if not DB.list_items(conn, a, \"entry\"):\n        print(\"no entries in case A: skipping bare-id and review checks\")\n        conn.close()\n        return\n    eid = DB.list_items(conn, a, \"entry\")[0][\"id\"]\n    try:"
}
````

### User / tool · 2026-11-02T02:04:12.408Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:13.919Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050; rm -rf $R/head_6c3aeb1/out $R/pre_6c3aeb1p/out; mkdir -p $R/head_6c3aeb1/out $R/pre_6c3aeb1p/out; .venv/bin/python $R/t050_check.py $R/head_6c3aeb1 $R/head_6c3aeb1/out > $R/head_6c3aeb1/stdout.txt 2> $R/head_6c3aeb1/stderr.txt; echo \"== HEAD exit=$?\"; cat $R/head_6c3aeb1/stdout.txt; echo \"-- HEAD non-judge stderr:\"; grep -v \"llm call failed\" $R/head_6c3aeb1/stderr.txt | tail -6; .venv/bin/python $R/t050_check.py $R/pre_6c3aeb1p $R/pre_6c3aeb1p/out > $R/pre_6c3aeb1p/stdout.txt 2> $R/pre_6c3aeb1p/stderr.txt; echo \"== PRE exit=$?\"; cat $R/pre_6c3aeb1p/stdout.txt; echo \"-- PRE non-judge stderr (tail):\"; grep -v \"llm call failed\" $R/pre_6c3aeb1p/stderr.txt | tail -3",
 "description": "Rerun probe on HEAD and pre-T-050 archives with literal paths"
}
````

### User / tool · 2026-11-02T02:04:15.637Z

**tool result**
````
== HEAD exit=1
== PART A: DB + pipeline code path ==
run_pipeline sample: RAISED ValueError: item id 'a1' exists in several cases; pass case=
run_pipeline case_01_date_formats: RAISED ValueError: item id 'a1' exists in several cases; pass case=
entry: caseA=0 []... caseB=0 []... shared_ids=0 non_short=[]
flag: caseA=2 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7']... caseB=1 ['f_date_r8']... shared_ids=0 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=1 ['a1']... shared_ids=1 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 0, 4, 2], 'B': [8, 0, 1, 1]}
entries PK clause: ['PRIMARY KEY (case_id, id)']
entry states per case: {'A': [], 'B': []}
no entries in case A: skipping bare-id and review checks
== PART B: HTTP API path, one sqlite file ==
POST /api/cases sample: 201
POST /api/cases case_01_date_formats: 201
run sample: POST=202 final status=failed stage=finalize error={'code': 'run_failed', 'message': 'The run stopped; finished items are kept.'}
run case_01_date_formats: POST=202 final status=failed stage=finalize error={'code': 'run_failed', 'message': 'The run stopped; finished items are kept.'}
API view sample: entries=[] n_ids=15 non_short=[]
API view case_01_date_formats: entries=[] n_ids=10 non_short=[]
-- HEAD non-judge stderr:
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 151, in <module>
    part_b(os.path.join(OUT, "partB.sqlite"))
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/t050_check.py", line 132, in part_b
    eid = views[CASES[0]]["entries"][0]["id"]
          ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
== PRE exit=1
== PART A: DB + pipeline code path ==
ingest_case case_01_date_formats: RAISED IntegrityError: UNIQUE constraint failed: records.id
run_pipeline sample: status=done_with_errors entries=0 amounts=3 flags=10 errors=['LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES', 'LLM_FAILED_AFTER_RETRIES']
run_pipeline case_01_date_formats: RAISED IntegrityError: UNIQUE constraint failed: records.id
entry: caseA=0 []... caseB=0 []... shared_ids=0 non_short=[]
flag: caseA=10 ['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_r3_1', 'f_r8_1']... caseB=0 []... shared_ids=0 non_short=[]
amount: caseA=4 ['a1', 'a2', 'a4', 'a3']... caseB=0 []... shared_ids=0 non_short=[]
rows per case (records/entries/amounts/flags): {'A': [9, 0, 4, 10], 'B': [0, 0, 0, 0]}
entries PK clause: []
entry states per case: {'A': [], 'B': []}
no entries in case A: skipping bare-id and review checks
== PART B: HTTP API path, one sqlite file ==
POST /api/cases sample: 201
-- PRE non-judge stderr (tail):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p/app/db/db.py", line 80, in _insert
    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
sqlite3.IntegrityError: UNIQUE constraint failed: records.id
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:28.113Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/head_6c3aeb1 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_api_routes.py tests/unit/test_db.py tests/unit/test_pipeline.py -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -40",
 "description": "Run T-050 tests against the committed 6c3aeb1 tree"
}
````

### User / tool · 2026-11-02T02:04:33.858Z

**tool result**
````
    def test_two_cases_coexist_with_short_display_ids(env):
        """T-050: the same short ids (e1, r1, f_gap_r6_r7) exist in two cases; review on one does not touch the other; delete is per case."""
        _, c = env
>       a, b = run_case(c), run_case(c)
                            ^^^^^^^^^^^

tests/unit/test_api_routes.py:203: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/unit/test_api_routes.py:37: in run_case
    wait_ready(c, tok)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

c = <starlette.testclient.TestClient object at 0x10a330e30>
tok = 'JVTXRyuF-RBHtAYiCXu4cg'

    def wait_ready(c, tok):
        for _ in range(160):
            s = c.get(f"/api/cases/{tok}/status").json()
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.25)
>       assert s["status"] == "ready", s
E       AssertionError: {'token': 'JVTXRyuF-RBHtAYiCXu4cg', 'status': 'failed', 'stage': 'finalize', 'stages': ['ingest', 'extract', 'verify', 'judge_entries', 'amounts', 'conflicts', ...], ...}
E       assert 'failed' == 'ready'
E         
E         - ready
E         + failed

tests/unit/test_api_routes.py:30: AssertionError
------------------------------ Captured log call -------------------------------
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_whole_case_after_run_matches_contract
FAILED tests/unit/test_api_routes.py::test_why_returns_ladder_backend_and_calls
FAILED tests/unit/test_api_routes.py::test_review_http_matrix_and_decisions_survive_restart
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
FAILED tests/unit/test_api_routes.py::test_confirm_date_case_01 - assert False
FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted
FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
7 failed, 59 passed in 5.35s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:42.256Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/head_6c3aeb1 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_api_routes.py::test_whole_case_after_run_matches_contract -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | grep -n \"Error\\|error\\|Traceback\\|raise\\|pipeline.py\\|db.py\" | head -20; echo \"--- HEAD single-case direct run ---\"; cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/single_case_probe.py <<'EOF'\n\"\"\"Single-case probe: ingest + run one golden case into a fresh DB, report exception or status. Usage: probe <root> <case>.\"\"\"\nimport os, sys, tempfile\nroot, case = sys.argv[1], sys.argv[2]\nsys.path.insert(0, root); os.chdir(root)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfrom app.db import db as DB\nfrom app.backend import pipeline as PL\nfrom app.llm import audited as AU\nfrom tests.unit import _golden as G\nconn = DB.connect(os.path.join(tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(__file__))), \"one.sqlite\"))\ncid = DB.create_case(conn, G.raw(case), now=1.0)\nPL.ingest_case(conn, cid, G.raw(case), 1.0)\ntry:\n    out = PL.run_pipeline(conn, cid, G.raw(case), call=AU.make_call(conn, cid), now=lambda: 1.0)\n    print(case, \"single-case run status:\", out[\"status\"], \"entries:\", len(out[\"entries\"]))\nexcept Exception as e:\n    import traceback; print(case, \"RAISED\", type(e).__name__, e); traceback.print_exc(limit=-3)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/single_case_probe.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/head_6c3aeb1 sample 2>/dev/null; echo \"exit=$?\"",
 "description": "Inspect HEAD single-case failure cause"
}
````

### User / tool · 2026-11-02T02:04:43.793Z

**tool result**
````
15:tests/unit/test_api_routes.py:81: AssertionError
--- HEAD single-case direct run ---
sample single-case run status: done_with_errors entries: 0
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:51.416Z

**tool call — Bash**
````
{
 "command": "git diff --stat HEAD -- app tests evals | tail -30; echo \"--- untracked under app/tests ---\"; git status --short -- app tests | grep \"^??\" | head",
 "description": "List uncommitted app and test changes vs HEAD"
}
````

### User / tool · 2026-11-02T02:04:51.532Z

**tool result**
````
 app/backend/pipeline.py | 87 ++++++++++++++++++++++++++++++++++++++++++++-----
 app/llm/provider.py     | 18 ++++++++++
 app/llm/record.py       | 47 +++++++++++++++++++++++++-
 3 files changed, 142 insertions(+), 10 deletions(-)
--- untracked under app/tests ---
?? tests/fixtures/llm/051431244b8754ecac0333514244f37930768de97ec3b4f639b97047e0ada328.json
?? tests/fixtures/llm/06ba451c413e5628f554f915316d53a63820f262b930020da1cd2ecb147c5fea.json
?? tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
?? tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
?? tests/fixtures/llm/0a7eff512ada0b23f5a97cb0617eb0eecc95c4a443273eaa7f2f8c60676fba86.json
?? tests/fixtures/llm/0cebc40f6b66a32cc8f395fde98789b2409fca08b175e1fcfba2581706f657d5.json
?? tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
?? tests/fixtures/llm/0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
?? tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
?? tests/fixtures/llm/1018ad182d2235434136054be56b867ff27dbf962da13fd09c077fc8085431a4.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:59.820Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-050 && echo \"untracked llm fixtures: $(git status --short tests/fixtures | grep -c '^??')\"; echo \"tracked llm fixtures at HEAD: $(git ls-files tests/fixtures/llm | wc -l)\"; echo \"fixture files in head archive: $(ls $R/head_6c3aeb1/tests/fixtures/llm 2>/dev/null | wc -l)\"; cp -R $R/head_6c3aeb1 $R/h1_head_plus_fixtures && cp tests/fixtures/llm/*.json $R/h1_head_plus_fixtures/tests/fixtures/llm/ && cp -R $R/h1_head_plus_fixtures $R/h2_head_plus_fixtures_plus_wt_pipeline && cp app/backend/pipeline.py $R/h2_head_plus_fixtures_plus_wt_pipeline/app/backend/pipeline.py && echo \"fixture files now in h1: $(ls $R/h1_head_plus_fixtures/tests/fixtures/llm | wc -l)\"; for d in h1_head_plus_fixtures h2_head_plus_fixtures_plus_wt_pipeline; do echo \"== $d\"; (cd $R/$d && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_api_routes.py tests/unit/test_db.py tests/unit/test_pipeline.py -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -12); done",
 "description": "Isolate T-050 commit by overlaying missing fixtures and WIP pipeline"
}
````

### User / tool · 2026-11-02T02:05:11.586Z

**tool result**
````
untracked llm fixtures: 251
tracked llm fixtures at HEAD:       38
fixture files in head archive:        1
fixture files now in h1:      252
== h1_head_plus_fixtures
>       assert s["status"] == "ready", s
E       AssertionError: {'token': 'IxSYtXxu5zLeeXfjZg4tjg', 'status': 'failed', 'stage': 'finalize', 'stages': ['ingest', 'extract', 'verify', 'judge_entries', 'amounts', 'conflicts', ...], ...}
E       assert 'failed' == 'ready'
E         
E         - ready
E         + failed

tests/unit/test_api_routes.py:30: AssertionError
------------------------------ Captured log call -------------------------------
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
1 failed, 65 passed in 5.44s
== h2_head_plus_fixtures_plus_wt_pipeline
..................................................................       [100%]
66 passed in 5.19s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:37.830Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/mutate.py",
 "content": "\"\"\"T-050 mutation spot-check (staff-engineer-reviewer). Copies app/, tests/, evals/ from the WORKING TREE into scratch\ndirs under artifacts/review-evidence/T-050/mut/, applies one mutation each, runs the T-050 test files, prints the summary.\nThe repo itself is never modified.\n\nUsage: .venv/bin/python artifacts/review-evidence/T-050/mutate.py\n\"\"\"\nimport os\nimport shutil\nimport subprocess\nimport sys\n\nREPO = \"/Users/arsis/zlayt-pm-project\"\nBASE = os.path.join(REPO, \"artifacts\", \"review-evidence\", \"T-050\", \"mut\")\nPY = os.path.join(REPO, \".venv\", \"bin\", \"python\")\nTESTS = [\"tests/unit/test_multicase.py\", \"tests/unit/test_api_routes.py\", \"tests/unit/test_db.py\"]\n\nMUTANTS = {\n    \"M1_find_not_case_scoped\": (\"app/db/db.py\",\n        '    if case is not None:\\n        q, a = q + \" AND case_id=?\", a + [case]',\n        '    if False:\\n        q, a = q + \" AND case_id=?\", a + [case]'),\n    \"M2_schema_pk_global_id\": (\"app/db/schema.sql\",\n        \"PRIMARY KEY (case_id, id)\",\n        \"PRIMARY KEY (id)\"),\n    \"M3_delete_case_skips_llm_calls\": (\"app/db/db.py\",\n        '_CASE_TABLES = (\"records\", \"entries\", \"amounts\", \"flags\", \"llm_calls\", \"review_events\", \"cases\")',\n        '_CASE_TABLES = (\"records\", \"entries\", \"amounts\", \"flags\", \"review_events\", \"cases\")'),\n    \"M4_apply_review_update_not_case_scoped\": (\"app/db/db.py\",\n        '''WHERE id=? AND case_id=?\",\n                     (status, _enc(new_edited), now, item_id, row[\"case_id\"]))''',\n        '''WHERE id=?\",\n                     (status, _enc(new_edited), now, item_id))'''),\n}\n\n\ndef main():\n    os.makedirs(BASE, exist_ok=True)\n    ignore = shutil.ignore_patterns(\"__pycache__\", \".pytest_cache\", \"*.sqlite\")\n    for name, (rel, old, new) in MUTANTS.items():\n        d = os.path.join(BASE, name)\n        if os.path.exists(d):\n            shutil.rmtree(d)\n        os.makedirs(d)\n        for top in (\"app\", \"tests\", \"evals\"):\n            shutil.copytree(os.path.join(REPO, top), os.path.join(d, top), ignore=ignore)\n        path = os.path.join(d, rel)\n        text = open(path, encoding=\"utf-8\").read()\n        n = text.count(old)\n        if n == 0:\n            print(f\"{name}: PATTERN NOT FOUND in {rel}; mutation not applied\")\n            continue\n        open(path, \"w\", encoding=\"utf-8\").write(text.replace(old, new))\n        r = subprocess.run([PY, \"-m\", \"pytest\", *TESTS, \"-q\", \"-p\", \"no:cacheprovider\"], cwd=d,\n                           capture_output=True, text=True)\n        lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]\n        summary = lines[-1] if lines else \"\"\n        failed = [l for l in lines if l.startswith(\"FAILED\")]\n        print(f\"{name} (sites={n}): exit={r.returncode} | {summary}\")\n        for f in failed[:8]:\n            print(\"   \", f)\n    return 0\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
}
````

### User / tool · 2026-11-02T02:05:37.937Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/mutate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:39.171Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-050/mutate.py 2>&1 | grep -v \"llm call failed\" | tail -60",
 "description": "Run four mutation spot-checks in scratch copies"
}
````

### User / tool · 2026-11-02T02:05:58.196Z

**tool result**
````
M1_find_not_case_scoped (sites=1): exit=1 | 2 failed, 42 passed in 4.22s
    FAILED tests/unit/test_multicase.py::test_full_pipeline_twice_in_one_file - V...
    FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
M2_schema_pk_global_id (sites=4): exit=1 | 4 failed, 40 passed in 4.24s
    FAILED tests/unit/test_multicase.py::test_two_golden_cases_back_to_back_in_one_file
    FAILED tests/unit/test_multicase.py::test_full_pipeline_twice_in_one_file - s...
    FAILED tests/unit/test_multicase.py::test_delete_case_removes_only_that_case
    FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
M3_delete_case_skips_llm_calls (sites=1): exit=1 | 6 failed, 38 passed in 4.30s
    FAILED tests/unit/test_api_routes.py::test_delete_removes_everything - Assert...
    FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
    FAILED tests/unit/test_db.py::test_delete_case_empties_every_table_including_prompts
    FAILED tests/unit/test_db.py::test_llm_calls_table_is_among_the_deleted - Ass...
    FAILED tests/unit/test_db.py::test_purge_after_24h_with_injectable_now - sqli...
    FAILED tests/unit/test_db.py::test_purge_uses_the_same_deletion_path - sqlite...
M4_apply_review_update_not_case_scoped (sites=1): exit=1 | 3 failed, 41 passed in 4.60s
    FAILED tests/unit/test_multicase.py::test_full_pipeline_twice_in_one_file - A...
    FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
    FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:05.178Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-050/legacy_probe.py <<'EOF'\n\"\"\"Upgrade hazard probe: a DB file created by pre-T-050 code, then opened by the current code.\nUsage: legacy_probe.py <pre_root> <new_root> <dbpath>\"\"\"\nimport os, re, sys\npre, new, dbp = sys.argv[1], sys.argv[2], sys.argv[3]\nfor suffix in (\"\", \"-wal\", \"-shm\", \"-journal\"):\n    if os.path.exists(dbp + suffix):\n        os.remove(dbp + suffix)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\n# step 1: pre-T-050 code writes sample into the file (run in a subprocess so module names do not clash)\nimport subprocess\ncode = (\n    \"import sys,os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]);\"\n    \"from app.db import db as DB; from app.backend import pipeline as PL; from tests.unit import _golden as G;\"\n    \"c=DB.connect(sys.argv[2]); cid=DB.create_case(c, G.raw('sample'), now=1.0); PL.ingest_case(c, cid, G.raw('sample'), 1.0);\"\n    \"print('pre-code ingest sample ok, records=', c.execute('select count(*) from records').fetchone()[0])\"\n)\nr = subprocess.run([sys.executable, \"-c\", code, pre, dbp], capture_output=True, text=True, env=dict(os.environ))\nprint(\"STEP1 exit\", r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1])\n# step 2: current code opens the same file and ingests a second case\ncode2 = (\n    \"import sys,os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]);\"\n    \"from app.db import db as DB; from app.backend import pipeline as PL; from tests.unit import _golden as G;\"\n    \"c=DB.connect(sys.argv[2]);\"\n    \"print('entries PK clause now:', __import__('re').findall(r'CREATE TABLE IF NOT EXISTS entries \\\\(\\\\n  id [^,]*', c.execute(\\\"select sql from sqlite_master where name='entries'\\\").fetchone()[0]));\"\n    \"cid=DB.create_case(c, G.raw('case_01_date_formats'), now=1.0); PL.ingest_case(c, cid, G.raw('case_01_date_formats'), 1.0);\"\n    \"print('second case ingest ok')\"\n)\nr2 = subprocess.run([sys.executable, \"-c\", code2, new, dbp], capture_output=True, text=True, env=dict(os.environ))\nprint(\"STEP2 exit\", r2.returncode, (r2.stdout + r2.stderr).strip().splitlines()[-3:])\nEOF\nR=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050; .venv/bin/python $R/legacy_probe.py $R/pre_6c3aeb1p /Users/arsis/zlayt-pm-project $R/legacy.sqlite 2>&1 | grep -v \"llm call failed\"",
 "description": "Probe legacy DB file opened by new schema code"
}
````

### User / tool · 2026-11-02T02:06:05.717Z

**tool result**
````
STEP1 exit 0 pre-code ingest sample ok, records= 9
STEP2 exit 1 ['  File "/Users/arsis/zlayt-pm-project/app/db/db.py", line 81, in _insert', '    conn.execute(f"INSERT INTO {table} ({\',\'.join(row)}) VALUES ({\',\'.join(\'?\' * len(row))})",', 'sqlite3.IntegrityError: UNIQUE constraint failed: records.id']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:16.271Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q 2>&1 | tail -2; echo \"--- T-050 tests in working tree (verbose names) ---\"; .venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -2; echo \"--- full tests/unit (working tree) ---\"; .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -4; echo \"--- T-050 test names in test_db/test_pipeline ---\"; grep -c \"case=\" tests/unit/test_db.py tests/unit/test_pipeline.py; grep -n \"def test_\" tests/unit/test_db.py | grep -i \"case\\|coexist\\|namesp\" ",
 "description": "Run brief pytest command, T-050 tests, and full unit suite",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T02:06:33.537Z

**tool result**
````
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 40 passed in 4.34s
--- T-050 tests in working tree (verbose names) ---
....                                                                     [100%]
4 passed in 1.23s
--- full tests/unit (working tree) ---
------------------------------ Captured log call -------------------------------
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 762 passed in 10.38s
--- T-050 test names in test_db/test_pipeline ---
tests/unit/test_pipeline.py:0
tests/unit/test_db.py:0
17:def test_delete_case_empties_every_table_including_prompts(conn):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:36.896Z

**tool call — Bash**
````
{
 "command": "for i in 1 2 3; do .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode -q -p no:cacheprovider 2>&1 | tail -1; done; echo \"--- failure detail ---\"; .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | grep -B3 -A12 \"^E \" | head -40; echo \"--- files changed recently in app/ tests/ ---\"; find app tests -newer artifacts/review-evidence/T-050/t050_check.py -name \"*.py\" 2>/dev/null | head; git status --short -- app tests | grep -v \"^??\" ; git log --oneline -1 | cat",
 "description": "Re-run flaky-looking test and inspect failure and recent edits"
}
````

### User / tool · 2026-11-02T02:06:41.218Z

**tool result**
````
1 failed in 0.80s
1 failed in 0.74s
1 failed in 0.74s
--- failure detail ---
        assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
>       assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]
               ^^^^^^^^^^^^^^^^
E       IndexError: list index out of range

tests/unit/test_api_routes.py:129: IndexError
------------------------------ Captured log call -------------------------------
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed in 0.73s
--- files changed recently in app/ tests/ ---
app/backend/why.py
app/backend/confidence.py
app/backend/flags.py
app/backend/flag_templates.py
app/backend/grounding.py
tests/unit/test_flags_pass.py
tests/fixtures/make_curated.py
tests/unit/test_t037_backend.py
 M app/backend/confidence.py
 M app/backend/flag_templates.py
 M app/backend/flags.py
 M app/backend/grounding.py
 M app/backend/pipeline.py
 M app/backend/why.py
 M app/llm/provider.py
 M app/llm/record.py
 M tests/unit/test_flags_pass.py
 M tests/unit/test_t037_backend.py
4e8f43d test(fixtures): curated set r2 - golden flag spans (D-030), accept all pending, byte-equal export (T-051)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:49.212Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 | cat; echo \"--- 6c3aeb1 still in history: $(git merge-base --is-ancestor 6c3aeb1 HEAD && echo yes)\"; echo \"--- commits touching pipeline.py/db since 6c3aeb1 ---\"; git log --oneline 6c3aeb1..HEAD -- app/backend/pipeline.py app/db app/backend/review.py app/backend/present.py | cat; echo \"--- HEAD pipeline case=cid count: $(git show HEAD:app/backend/pipeline.py | grep -c 'case=cid')\"; echo \"--- HEAD stat ---\"; git show --stat HEAD | head -20 | cat; echo \"--- current brief command ---\"; .venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q 2>&1 | tail -2",
 "description": "Check current git history and whether pipeline fix landed"
}
````

### User / tool · 2026-11-02T02:06:54.080Z

**tool result**
````
4e8f43d test(fixtures): curated set r2 - golden flag spans (D-030), accept all pending, byte-equal export (T-051)
2ad53e7 chore(app): serve_app.sh; app live on :7860 (tailnet); runbook
5490ab9 feat(backend): flag evidence is the model's verbatim phrase span when model and lexicon agree (D-030)
5542dfd fix(harness): AC evidence must be >= 10 chars; D-030 flag evidence spans
c9f272a fix(backend): export maps pipeline output to golden (amount sentence, PT plan label, self-report marker, record-1 quote); FIXTURE_SET support
077e294 fix(backend): clean create failure, JSON 500, CSP, body cap, lazy purge, live cap guard (T-040 r1)
e771ed3 feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)
239e2d3 fix(frontend): T-043 review minors, mock flags overlay
--- 6c3aeb1 still in history: yes
--- commits touching pipeline.py/db since 6c3aeb1 ---
--- HEAD pipeline case=cid count: 0
--- HEAD stat ---
commit 4e8f43d037acde52ed0fe0fac77c0995f8ce20db
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:06:08 2026 -0600

    test(fixtures): curated set r2 - golden flag spans (D-030), accept all pending, byte-equal export (T-051)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 ...6af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json |  2 +-
 ...7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json |  2 +-
 ...0ebda1d3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json |  2 +-
 ...764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json |  2 +-
 ...c5e00a8732ecddb694b45c2637be29b83e3bfa35576123f24.json |  2 +-
 ...72348f390212b959eebee7313b76f0edf051977846aacbc56.json |  2 +-
 ...d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json |  2 +-
 ...a035220bcef2d7bc9c295375c65ba9617445d10a094d2515f.json |  2 +-
 ...0482345adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json |  2 +-
 ...9bd60ceabdf7b697fe630c4f949d830b08ddc815cb9e1252.json} |  2 +-
 ...b7093d23904905e4e400ef4c6eb8499806d234f247dd75262.json |  2 +-
 ...6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json |  2 +-
--- current brief command ---
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 40 passed in 4.37s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:58.487Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-050 && mkdir -p $R/head_4e8f43d && git archive HEAD | tar -x -C $R/head_4e8f43d && echo \"untracked fixtures now: $(git status --short tests/fixtures | grep -c '^??')\"; cd $R/head_4e8f43d && echo \"== HEAD 4e8f43d as committed:\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -3; cp -n /Users/arsis/zlayt-pm-project/tests/fixtures/llm/*.json tests/fixtures/llm/ 2>/dev/null; echo \"== HEAD 4e8f43d + untracked fixture overlay:\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q -p no:cacheprovider 2>&1 | grep -v \"llm call failed\" | tail -3",
 "description": "Test committed HEAD tree with and without untracked fixtures"
}
````

### User / tool · 2026-11-02T02:07:08.228Z

**tool result**
````
untracked fixtures now: 0
== HEAD 4e8f43d as committed:
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 40 passed in 4.43s
== HEAD 4e8f43d + untracked fixture overlay:
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 40 passed in 4.43s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:12.965Z

**tool call — Bash**
````
{
 "command": "grep -n \"def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode\" -A14 tests/unit/test_api_routes.py | cat -n | head -24; echo \"--- what the T-050 commit touched in that test file ---\"; git log --oneline -3 -- tests/unit/test_api_routes.py | cat; echo \"--- does 6c3aeb1 tree fail that test? (committed fixtures of that time) ---\"; R=artifacts/review-evidence/T-050; cd $R/head_6c3aeb1 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode -q -p no:cacheprovider 2>&1 | tail -1",
 "description": "Inspect the newly failing judge-unavailable test and its history"
}
````

### User / tool · 2026-11-02T02:07:14.051Z

**tool result**
````
     1	122:def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode(env):
     2	123-    _, c = env
     3	124-    tok = run_case(c)
     4	125-    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
     5	126-    r = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10 and improving."}})
     6	127-    j = r.json()
     7	128-    assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
     8	129-    assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]
     9	130-
    10	131-
    11	132-def test_charge_cannot_be_edited_and_rerun_needs_confirm(env):
    12	133-    _, c = env
    13	134-    tok = run_case(c)
    14	135-    a = c.get(f"/api/cases/{tok}").json()["amounts"][0]["id"]
    15	136-    assert c.post(f"/api/cases/{tok}/items/{a}/review", json={"action": "edit", "edits": {"value": 1}}).status_code == 422
--- what the T-050 commit touched in that test file ---
077e294 fix(backend): clean create failure, JSON 500, CSP, body cap, lazy purge, live cap guard (T-040 r1)
6c3aeb1 fix(db): per-case id namespacing via composite primary key (T-050)
a7df086 feat(backend): FastAPI routes, demo gate, review/edit/confirm_date with re-check (T-040)
--- does 6c3aeb1 tree fail that test? (committed fixtures of that time) ---
1 failed in 0.70s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:37.599Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/pipeline.py | grep -n 'DB.update_item(conn, it\\[\"id\"\\], now=now, \\*\\*row)\\|DB.apply_review(conn, it\\[\"id\"\\], \"reset\", now=now)\\|DB.add_item(conn, cid, kind' ; git show HEAD:app/db/db.py | grep -n \"def _find\\|def delete_case\\|exists in several cases\\|_CASE_TABLES = \"; git show HEAD:tests/unit/test_api_routes.py | grep -n \"def test_two_cases_coexist\"; git show HEAD:tests/unit/test_multicase.py | grep -n \"^def test_\"; grep -n \"def test_\" tests/unit/test_multicase.py | head -5; git show HEAD:app/db/schema.sql | grep -n \"PRIMARY KEY (case_id, id)\" | head; sed -n '1,3p' /dev/null; ls reviews 2>/dev/null | head -20; ls -d .claude/agent-memory/staff-engineer-reviewer",
 "description": "Confirm line numbers for cited evidence at HEAD"
}
````

### User / tool · 2026-11-02T02:07:37.790Z

**tool result**
````
137:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
21:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
104:def _find(conn, item_id, case=None):
117:        raise ValueError(f"item id {item_id!r} exists in several cases; pass case=")
216:def delete_case(conn, case_id: str) -> None:
200:def test_two_cases_coexist_with_short_display_ids(env):
15:def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
26:def test_full_pipeline_twice_in_one_file(tmp_path):
46:def test_delete_case_removes_only_that_case(tmp_path):
15:def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
26:def test_full_pipeline_twice_in_one_file(tmp_path):
46:def test_delete_case_removes_only_that_case(tmp_path):
17:  PRIMARY KEY (case_id, id)
25:  PRIMARY KEY (case_id, id)
34:  PRIMARY KEY (case_id, id)
45:  PRIMARY KEY (case_id, id)
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
.claude/agent-memory/staff-engineer-reviewer
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:42.350Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep -i \"T-050\\|T-031\\|T-039\" | head; f=$(ls reviews/T-031-staff-engineer*.md 2>/dev/null | tail -1); echo \"--- sample: $f\"; head -c 1500 \"$f\"; echo; echo \"--- validator usage ---\"; python3 tools/board.py --help 2>&1 | head -20",
 "description": "Inspect an existing staff review format and board tool usage"
}
````

### User / tool · 2026-11-02T02:07:42.496Z

**tool result**
````
T-031-staff-engineer-r2.md
T-031-staff-engineer.md
T-039-staff-engineer-r2.md
T-039-staff-engineer.md
--- sample: reviews/T-031-staff-engineer.md
# T-031 review: staff-engineer (Marcus Lee lens)

Verdict: **changes**. Behaviour the AC names mostly works: I proved ladder round-trip, delete_case, 24h purge, secure_delete, originals kept and persistence myself (artifacts/review-evidence/T-031-ac_check.py and its .out). Three gaps: `update_item` is an unlogged side door around `apply_review`, `apply_review("edit")` accepts an empty edit, and the AC-named proof tests don't exist or don't prove what the AC says.

Labels: the three majors violate an AC or spec constraint (row 20 audit, honest failure, "proved by" tests). The minors are "I would do it differently".

```json
{"card": "T-031", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 39e458a: app/db/db.py, app/db/schema.sql; tests/unit/test_db.py; no app URL (library card); sample case n/a",
 "exercised": [
  "python3 tools/board.py show T-031",
  ".venv/bin/python -m pytest tests/unit/test_db.py -q -> 9 passed in 0.09s",
  "read app/db/db.py (227 lines), schema.sql (60 lines), tests/unit/test_db.py in full",
  ".venv/bin/python artifacts/review-evidence/T-031-ac_check.py (output in T-031-ac_check.out): ladder D.4+backend round trip on a new connection, llm_calls fields, secure_delete PRAGMA on two connections, raw-file byte check after delete_case, delete_case across all tables, purge at 24h-1 / 24h / 24h+1 with injected now, purge of a case with children under FK ON, apply_review before/after events, originals kept, SQL-injection pr
--- validator usage ---
usage: board.py [-h]
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
                ...

Zlayt PM project board CLI

positional arguments:
  {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}

options:
  -h, --help            show this help message and exit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:08:37.550Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer.md",
 "content": "# T-050 review: staff-engineer (Marcus Lee lens)\n\nVerdict: **fail**. The namespacing design is right (composite key, every writer in `app/db/db.py` takes `case=`, ambiguous bare ids raise). The committed change is not runnable for a second case: commit `6c3aeb1` leaves `app/backend/pipeline.py` `_persist` unscoped, so the card's own AC2 test fails at that commit. The three `case=cid` lines exist only as uncommitted working-tree WIP (mixed in with unrelated backend-2 edits). Blocker: F1. Major: F2 (no migration for DB files made before T-050). Minors: F3, F4.\n\nLabels: F1 violates AC1/AC2 (two cases coexist; \"done\" evidence fails at the commit), so it is a blocker. F2 is a persistence-upgrade hazard, rated major. F3 and F4 are \"the AC names the wrong place / the AC test is weaker than the AC\" and are minor.\n\nTree note: HEAD moved during this review (6c3aeb1 → 4e8f43d by other commits; pipeline.py still has no `case=cid` at 4e8f43d). The first brief-command run gave `36 passed`; a later run gave `1 failed, 40 passed` on a test unrelated to T-050 (see \"Outside this card\").\n\nModel note: this review ran as `claude-haiku-5-5`. The dossier expects `claude-sonnet-5-5`; the record uses the model that ran.\n\n```json\n{\"card\": \"T-050\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 6c3aeb1 (card commits) plus the working tree at review time (uncommitted app/backend/pipeline.py WIP); HEAD 4e8f43d checked at the end (pipeline.py unchanged since 6c3aeb1). No live app URL used: the HTTP API was exercised in-process with fastapi TestClient. Sample case and case_01_date_formats.\",\n \"exercised\": [\n  \"python3 tools/board.py show T-050 (AC read; commit list 6c3aeb1; ac evidence strings)\",\n  \".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q -> '36 passed in 4.27s' (first run); same command later -> '1 failed, 40 passed in 4.37s' (FAILED test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode; tree had moved to HEAD 4e8f43d)\",\n  \".venv/bin/python -m pytest tests/unit -q (working tree) -> '1 failed, 762 passed in 10.38s' (same unrelated test)\",\n  \"git show 6c3aeb1 (full diff of app/db/db.py, app/db/schema.sql, app/backend/review.py, app/backend/present.py, tests/unit/test_api_routes.py, tests/unit/test_multicase.py) read in full\",\n  \"git show HEAD:app/backend/pipeline.py | grep -n: lines 137 (add_item), 141 (update_item without case=), 145 (apply_review without case=); git show HEAD:app/backend/pipeline.py | grep -c 'case=cid' -> 0\",\n  \"git diff HEAD -- app/backend/pipeline.py: adds case=cid at the same _persist calls (uncommitted), plus unrelated removals of sentences/body_offset/judges_failed\",\n  \"artifacts/review-evidence/T-050/t050_check.py run on the working tree (outputs in artifacts/review-evidence/T-050/worktree/stdout.txt): two golden cases into one sqlite file via ingest_case + run_pipeline (Part A) and via POST /api/cases, POST /run, review, DELETE (Part B)\",\n  \"same script on git archive 6c3aeb1 (artifacts/review-evidence/T-050/head_6c3aeb1/stdout.txt): RAISED ValueError 'item id a1 exists in several cases; pass case='; API run status=failed, error run_failed for both cases\",\n  \"same script on git archive 6c3aeb1^ (artifacts/review-evidence/T-050/pre_6c3aeb1p/stdout.txt): baseline collision reproduced: 'ingest_case case_01_date_formats: RAISED IntegrityError: UNIQUE constraint failed: records.id'\",\n  \"artifacts/review-evidence/T-050/legacy_probe.py: pre-T-050 code writes sample into a file, current code opens the same file and ingests case_01 -> 'STEP1 exit 0 ... records= 9', 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'\",\n  \"artifacts/review-evidence/T-050/single_case_probe.py on the archives (single-case run; used only to rule out the single-case path)\",\n  \"pytest on the 6c3aeb1 archive with the untracked LLM fixtures copied in (artifacts/review-evidence/T-050/h1_head_plus_fixtures): 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'; with the working-tree pipeline.py also copied in (h2_head_plus_fixtures_plus_wt_pipeline): '66 passed in 5.19s'\",\n  \"pytest on the 4e8f43d archive (artifacts/review-evidence/T-050/head_4e8f43d): '1 failed, 40 passed' (test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode, IndexError at tests/unit/test_api_routes.py:129)\",\n  \"artifacts/review-evidence/T-050/mutate.py (scratch copies under artifacts/review-evidence/T-050/mut/, repo not modified): M1 _find not case-scoped -> 2 failed (test_multicase::test_full_pipeline_twice_in_one_file, test_api_routes::test_two_cases_coexist_with_short_display_ids); M2 schema PK (id) only -> 4 failed; M3 llm_calls dropped from _CASE_TABLES -> 6 failed, NOT including test_multicase::test_delete_case_removes_only_that_case; M4 apply_review UPDATE not case-scoped -> 3 failed\",\n  \"grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0\",\n  \"app/db/db.py read in full (_find 104-118, update_item 141-153, apply_review 156-178, delete_case 216-225); app/db/schema.sql read (four PRIMARY KEY (case_id, id) clauses); grep of every DB item call site in app/ (review.py, present.py, pipeline.py, api.py): all pass case=; raw SQL scoped by case_id except llm_calls by random call id\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"composite_pk_and_writers\": 4, \"committed_state_consistency\": 1, \"short_display_ids\": 5, \"delete_case_isolation\": 4, \"test_adequacy_for_ac\": 2, \"upgrade_safety\": 2, \"failure_visibility\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Committed T-050 change leaves pipeline._persist unscoped: a second case's run fails, and the card's own AC2 test fails at 6c3aeb1\",\n   \"evidence\": \"git show HEAD:app/backend/pipeline.py: line 141 'DB.update_item(conn, it[\\\"id\\\"], now=now, **row)' and line 145 'DB.apply_review(conn, it[\\\"id\\\"], \\\"reset\\\", now=now)' carry no case=; 'git show HEAD:app/backend/pipeline.py | grep -c case=cid' -> 0 at 4e8f43d too. The fix exists only as uncommitted diff (git diff HEAD -- app/backend/pipeline.py, lines 139 and 143 in the working tree). Repro 1: git archive 6c3aeb1 into artifacts/review-evidence/T-050/head_6c3aeb1, copy tests/fixtures/llm/*.json in, run .venv/bin/python -m pytest tests/unit/test_api_routes.py tests/unit/test_multicase.py tests/unit/test_db.py tests/unit/test_pipeline.py -q -> 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'. Repro 2: same tree with the working-tree pipeline.py copied in -> '66 passed in 5.19s'. Repro 3: artifacts/review-evidence/T-050/t050_check.py on head_6c3aeb1 -> 'run_pipeline sample: RAISED ValueError: item id 'a1' exists in several cases; pass case=' and 'run sample: POST=202 final status=failed ... error={'code': 'run_failed'...}' for both cases.\",\n   \"why_it_matters\": \"AC1 and AC2 require two cases to coexist in one file. At the committed revision the second case's run fails, and that is the exact sequence the API performs (create, then run). The card is marked done and AC2 cites a test that fails at the commit. The green tests hide it: test_multicase::test_full_pipeline_twice_in_one_file calls run_pipeline on fresh case ids without ingest_case, so it never reaches the update path. Same pattern as T-030 r2: the fix is green in a unit test while the producer path is not wired.\",\n   \"fix\": \"Commit the case=cid argument on the three _persist calls (pipeline.py:141 and :145 at HEAD; :139 and :143 in the working tree) in a commit that does not carry the unrelated backend-2 WIP, or in the same commit as db.py. Add a test to tests/unit/test_multicase.py that does ingest_case for case B after case A has run, then run_pipeline for case B (the API order).\",\n   \"acceptance_test\": \"From the fix commit: git archive <fix> | tar -x -C <dir>; cd <dir> && .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids tests/unit/test_multicase.py -q passes; artifacts/review-evidence/T-050/t050_check.py <dir> <out> Part B reports 'final status=ready' for both cases.\"},\n  {\"severity\": \"major\",\n   \"title\": \"No migration for sqlite files created before T-050: the new composite key is silently not applied to an existing file\",\n   \"evidence\": \"artifacts/review-evidence/T-050/legacy_probe.py output: 'STEP1 exit 0 pre-code ingest sample ok, records= 9' then 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'. Cause: app/db/db.py:34-35 executes schema.sql, which uses CREATE TABLE IF NOT EXISTS, so the old global-PK tables are kept; there is no PRAGMA user_version check. The default DB path is app/backend/api.py:45 (data/zlayt.sqlite). The handoff's 'delete old sqlite files' is a manual step, not in the AC or in code.\",\n   \"why_it_matters\": \"Any machine with a pre-upgrade DB file gets a raw IntegrityError on the second case, and the first case's data stays under the old schema. This is the persistence failure the dossier warns about: a schema change that does not reach existing data without a visible signal.\",\n   \"fix\": \"Read PRAGMA user_version in connect(). On an old schema, either migrate (rebuild the four item tables with PRIMARY KEY (case_id, id), copying rows) or raise a named error that tells the user which file to remove. Bump the version in schema.sql.\",\n   \"acceptance_test\": \"Create a file with the pre-T-050 tree (git archive 6c3aeb1^), then open it with the fix tree and ingest a second case. Either the rows migrate and the second case ingests, or connect() raises a named error. artifacts/review-evidence/T-050/legacy_probe.py must no longer end in IntegrityError.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"AC1 names tests/unit/test_db.py and test_pipeline.py; neither file has a case-scoped test\",\n   \"evidence\": \"grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0. AC1 evidence cites tests/unit/test_multicase.py (a new file).\",\n   \"why_it_matters\": \"The AC says where the proof lives. A reader following the card will not find it in the named files.\",\n   \"fix\": \"Add one case-scoped test to test_db.py (get_item/apply_review with case=, ambiguous bare id raises ValueError) and one to test_pipeline.py, or amend the AC text to name test_multicase.py.\",\n   \"acceptance_test\": \"grep -l 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py lists both files, and pytest on those two files passes.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"AC3 delete test asserts only the records count for case A\",\n   \"evidence\": \"tests/unit/test_multicase.py:46-53: 'assert DB.get_case(conn, a) is None and DB.table_counts(conn, a).get(\\\"records\\\", 0) == 0'. Mutant M3 (llm_calls removed from _CASE_TABLES, app/db/db.py:21) leaves this test green; it is caught only by test_db.py (4 tests) and test_api_routes.py (2 tests) in mutate.py.\",\n   \"why_it_matters\": \"ADR-006 requires prompts (llm_calls) to be deleted with the case. The AC3 test as written would stay green if prompts survived. The protection comes from older tests, not from the test the card cites.\",\n   \"fix\": \"Assert every table in _CASE_TABLES has zero rows for case A and unchanged counts for case B.\",\n   \"acceptance_test\": \"Apply mutation M3 (drop llm_calls from _CASE_TABLES) in a scratch copy; tests/unit/test_multicase.py::test_delete_case_removes_only_that_case must fail.\"}\n ],\n \"whats_right\": [\n  \"Composite PK (case_id, id) on records, entries, amounts and flags, and every db.py/review.py writer takes case= and scopes its UPDATE/DELETE by case_id; an ambiguous bare id raises ValueError (app/db/db.py:116-117) instead of picking a row.\",\n  \"Display ids stay short in API JSON (e1, a1, f_gap_r6_r7, no random suffix) and identical across cases, as the AC2 text requires; delete_case leaves the other case's rows unchanged in every table on both code paths.\",\n  \"Four injected defects in scratch copies (unscoped _find, global PK, skipped llm_calls delete, unscoped apply_review UPDATE) were each caught by at least one test.\"\n ],\n \"questions_for_chris\": [\n  \"Is a DB file created before T-050 a state the demo or paralegal machines can be in? If yes, F2 must be fixed before the gate. If no, a documented 'remove data/zlayt.sqlite on upgrade' step is acceptable and F2 drops to a note.\"\n ]}\n```\n\n## Outside this card (observed, not T-050 findings)\n\n- `tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode` fails at HEAD 4e8f43d (`IndexError` at line 129: `warnings` is empty, so the judge did not report JUDGE_UNAVAILABLE). It passed on the 6c3aeb1 tree in my run. Not caused by the T-050 diff as far as I can tell. Flagging for the orchestrator to route.\n- In the probe, the fixture backend's judge steps (j1 to j4) raised 64 `llm call failed` lines on the working tree, and every probe entry ended `needs_review` with `[\"JUDGE_UNAVAILABLE\"]`. That is an honest visible state, but it means the probe proves id and isolation behaviour, not verified output.\n- At my review start, 251 LLM fixture files under `tests/fixtures/llm/` were untracked, so a clean checkout of 6c3aeb1 could not reproduce the suite. At 4e8f43d `git status` shows 0 untracked fixtures, so this is resolved.\n\nNot exercised: live app at http://localhost:7860, the eval runner, the `python -m app.pipeline evals/golden/sample.txt` CLI run-twice determinism check, export.\n"
}
````

### User / tool · 2026-11-02T02:08:37.705Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:08:40.326Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json,re\ns=open(\"reviews/T-050-staff-engineer.md\",encoding=\"utf-8\").read()\nblocks=re.findall(r\"```json\\n(.*?)\\n```\", s, re.S)\nprint(\"json blocks:\", len(blocks))\nj=json.loads(blocks[0])\nsev=[f[\"severity\"] for f in j[\"findings\"]]\nprint(\"verdict:\", j[\"verdict\"], \"| severities:\", sev, \"| model:\", j[\"model\"], \"| whats_right:\", len(j[\"whats_right\"]))\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule expects:\", exp, \"OK\" if exp==j[\"verdict\"] else \"MISMATCH\")\nEOF\npython3 tools/board.py validate 2>&1 | tail -8",
 "description": "Parse review JSON, check verdict rule, run board validate"
}
````

### User / tool · 2026-11-02T02:08:40.485Z

**tool result**
````
json blocks: 1
verdict: fail | severities: ['blocker', 'major', 'minor', 'minor'] | model: claude-haiku-5-5 | whats_right: 3
verdict rule expects: fail OK
ok (60 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:08:50.913Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t050_namespacing_review_patterns.md",
 "content": "---\nname: t050-namespacing-review-patterns\ndescription: T-050 (per-case id namespacing, commit 6c3aeb1) round-1 review - committed fix missing producer lines, no DB migration, delete test checks records only; how to reproduce a commit without the working tree\nmetadata:\n  type: project\n---\n\nRecurring pattern from the T-050 review (reviews/T-050-staff-engineer.md, verdict fail, 2026-11-01).\n\n- **A commit can be green in its own unit tests and still not run.** 6c3aeb1 changed db.py to require `case=` for ambiguous ids,\n  but the producer `_persist` in app/backend/pipeline.py (HEAD lines 141, 145) still called update_item/apply_review without it.\n  The fix lived only as uncommitted working-tree diff, mixed with unrelated backend WIP. test_multicase passed at HEAD because it\n  calls run_pipeline on fresh case ids and never does the API order (ingest_case for B, then run B). Same family as\n  [[project_wiring_review_patterns]].\n- **Reproduce a committed state without the working tree:** `git archive <sha> | tar -x -C artifacts/review-evidence/<card>/<dir>`,\n  then run pytest there. Before reading any red, check untracked fixtures: at review time 251 files under tests/fixtures/llm/\n  were untracked, so a clean archive fails 7 API tests for reasons unrelated to the card. Compare three trees: the commit, the commit plus\n  the untracked fixtures, and the commit plus the working-tree file in question.\n- **Schema change with CREATE TABLE IF NOT EXISTS is not a migration.** An existing file keeps the old global PRIMARY KEY, and the\n  second case dies with `IntegrityError: UNIQUE constraint failed: records.id`. Probe with the pre-change tree (git archive <sha>^)\n  writing the file, then the new tree opening it. The handoff's \"delete old sqlite files\" is not a fix.\n- **Delete-isolation tests can check one table.** test_delete_case_removes_only_that_case checked only `records`, so dropping llm_calls\n  (ADR-006 prompts) from _CASE_TABLES left it green. Other tests caught it. Check the mutant against the card's own test, not the suite.\n- **Mutation method that worked:** copy app/, tests/, evals/ from the working tree into artifacts/review-evidence/<card>/mut/<name>/,\n  assert the pattern occurs once, apply one replacement, run the card's test files. Never edit the repo.\n\nReviewer environment gotchas (this card):\n- `timeout` is not installed on this macOS shell; do not use it.\n- The git-guard hook blocks `rm -rf $var/...` when the variable is unresolved. Use literal paths.\n- HEAD moved during the review (other agents committed). Record `git rev-parse --short HEAD` at start and at each test run; a test\n  that passed at the start can fail at the end (test_judge_unavailable_edit... went red on HEAD 4e8f43d).\n\nRelated: [[project_db_review_patterns]], [[project_wiring_review_patterns]], [[project_harness_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T02:08:51.007Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t050_namespacing_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:08:52.027Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E",
 "new_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E\n- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1: commit missing producer case= lines, no DB migration, git-archive reproduction method"
}
````

### User / tool · 2026-11-02T02:08:52.121Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:08:53.854Z

T-050 verdict: fail (claude-haiku-5-5, not the expected sonnet). Blocker: commit 6c3aeb1 leaves `pipeline._persist` without `case=`, so a second case's run fails and the card's own AC2 test fails at that commit. Major: no migration for pre-T-050 DB files. Review: /Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer.md
