# Subagent: T-100 review (haiku staff) (T-100 review (haiku staff))

Source: `agent-a1472eadd1e1dae7e.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:10:14.699Z

Review board card T-100 in /Users/arsis/zlayt-pm-project (commit 24c18a7), which implements D-047 from memory/ORCHESTRATOR_DECISIONS.md. A side, negation or qualifier token missing from the excerpt is a hard 422 on edit and manual entry, and the 409 "keep my wording" path is removed.

Check:
- no route can still store such an edit: try confirm_warnings, force flags and the batch path;
- the 422 reasons are in plain words;
- the T-098 gate tests still exercise the gate as a second line of defence, since they now write that state directly;
- the D-040 speaker-word string at review.py is reworded;
- api.md is updated.

The orchestrator's decision: a judge objection to a human-written edit saves as needs_review with a warning, not a 422. Check that's implemented consistently. Mutate the token check in a scratch copy to confirm a test fails. Test a `git archive HEAD` copy in your scratchpad, and run `.venv/bin/python -m pytest -q tests/unit -k "edit or manual or d047 or d034"`.

Write reviews/T-100-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:15.812Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T05:10:15.821Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:16.037Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T05:10:16.044Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad + r2 7df65fb (fail): audit prompt-id mismatch, 0.95 gate vs "every", arithmetic in controls, relabel basis
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263 + r2 8bc7f90 (fail): fix covers fixture shape not input class (no-decimal, dateless, unlabelled), unpinned elif-no-else gate, stated totals lost
24	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
25	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
26	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
27	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
28	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:16.627Z

**tool call — Bash**
````
{
 "command": "git show --stat 24c18a7 | head -60 && echo ---- && python3 tools/board.py show T-100 && echo ---- && grep -n \"D-047\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -60",
 "description": "Show commit stats, card T-100, and D-047 decision"
}
````

### User / tool · 2026-11-02T05:10:16.790Z

**tool result**
````
commit 24c18a757beaef62d42be592f85409187531e563
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:09:49 2026 -0600

    feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
    
    Judge objections no longer block a human-written edit: saved as needs_review with a warnings[] code.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/export.py               |  7 ++--
 app/backend/review.py               | 70 +++++++++++++++++--------------------
 app/backend/store.py                |  7 +---
 app/backend/trace.py                |  2 --
 memory/contracts/api.md             | 20 +++++------
 tests/unit/test_api_routes.py       | 24 ++++++++++++-
 tests/unit/test_export.py           |  5 ++-
 tests/unit/test_manual_and_split.py | 27 ++++++++++----
 tests/unit/test_ocr_invariant.py    |  2 +-
 tests/unit/test_review_rules.py     | 64 ++++++++++++++++++++++++++-------
 tests/unit/test_trace.py            | 20 +++++++----
 11 files changed, 156 insertions(+), 92 deletions(-)
----
---
id: "T-100"
title: "Implement D-047: side/negation/qualifier tokens missing from the excerpt are a hard 422 on edit and manual entry; remove the 409 keep-my-wording path"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:00:32Z"
updated_at: "2026-11-02T05:10:10Z"
claimed_by: "backend"
claimed_at: "2026-11-02T05:00:36Z"
rounds: 0
commits: ["24c18a7"]
reviews: []
ac:
  - {"n": 1, "text": "Edit and manual entry return 422 for any D-034/D-047 token not in the excerpt; no 409 confirm path remains (API + frontend copy); unit + e2e tests; api.md updated", "done": true, "evidence": "tests/unit/test_review_rules.py (side/negation/qualifier 422 x confirm flag, no event, no judge call, no confirm path), test_manual_and_split.py (manual entry 422), test_api_routes.py (route 422 shape, grep-no-409/confirm_warnings), test_trace.py T-098 gate tests adapted; tests/unit 1834 passed (1 skipped); api.md updated; frontend copy removal handed to T-097 note. e2e not run."}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:00:36Z backend: claimed
- 2026-11-02T05:10:01Z backend: AC 1 checked: tests/unit/test_review_rules.py (side/negation/qualifier 422 x confirm flag, no event, no judge call, no confirm path), test_manual_and_split.py (manual entry 422), test_api_routes.py (route 422 shape, grep-no-409/confirm_warnings), test_trace.py T-098 gate tests adapted; tests/unit 1834 passed (1 skipped); api.md updated; frontend copy removal handed to T-097 note. e2e not run.
- 2026-11-02T05:10:01Z backend: moved in_progress -> in_review
- 2026-11-02T05:10:10Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T05:10:10Z orchestrator: Orchestrator: keep the choice that a judge objection to a human-written edit saves as needs_review with a JUDGE_PARTIAL/UNSUPPORTED warning (D-045b exempts human text from the judge's veto; the warning keeps it visible).

## Handoff
What changed: review._check_summary now raises 422 invalid_edit (no override) for numbers (D-034), left/right/no/not/without missing from the quote (SUMMARY_TOKEN_NOT_IN_EXCERPT), a dropped quote qualifier (SUMMARY_DROPS_QUALIFIER), unlocatable quote (HIGHLIGHT_NOT_FOUND), before any judge call; 409 needs_confirm/confirm_warnings/keep_my_wording event + override_reasons/kept_my_wording/keep_wording fields removed from review, store, export, trace; api.md updated; T-097 note posted. | Verified: .venv/bin/python -m pytest -q tests/unit -> 1834 passed. | Assumption: a judge objection (partial/unsupported) can no longer 409, so it saves as needs_review + warnings[] (D-045b judge-exempt human wording); orchestrator may want 422 instead. | Left: app/db/db.py still lists the keep_my_wording action (db owner, harmless); qa e2e tests/e2e/test_rerun_judge.py and test_edit.py still send confirm_warnings (ignored) and were not run; frontend mock-review.js. | Surprised: T-098 gate tests built failing edits through the edit route, so they now write the legacy state directly (gate stays as second line of defence); real git index was stale, committed via temp index (24c18a7).

----
55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
56-| D-048 | Language routing fails safe (2026-11-02, after T-085 r2): a record or line runs as English only when it is **confidently English** (enough English function and clinical words, and no non-English evidence). Everything else is Spanish if confidently Spanish, otherwise LANGUAGE_UNCERTAIN: needs_review, labeled, and never passes on English token checks alone. On mixed lines, the English **and** Spanish token and qualifier checks both run (union), so a dropped 'posible' is caught whichever language leads. Routing gets a held-out measurement set. | Two rounds of heuristic detection let fresh Spanish and other-language lines through as unlabeled English. | T-085 legal-nurse r2 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:19.444Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 && git show 24c18a7 -- app/ memory/contracts/api.md",
 "description": "Show full product and API diff for commit 24c18a7"
}
````

### User / tool · 2026-11-02T05:10:19.654Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:20.794Z

**tool call — Bash**
````
{
 "command": "git show 24c18a7 -- app/backend/review.py app/backend/store.py app/backend/trace.py app/backend/export.py",
 "description": "Show product diff for review, store, trace, export"
}
````

### User / tool · 2026-11-02T05:10:20.888Z

**tool result**
````
commit 24c18a757beaef62d42be592f85409187531e563
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:09:49 2026 -0600

    feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
    
    Judge objections no longer block a human-written edit: saved as needs_review with a warnings[] code.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/export.py b/app/backend/export.py
index da080d7..bb851d3 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -5,7 +5,7 @@ Contract (ADR-009, D-001, D-012, D-017, D-019, LLM_VS_CODE rows 8 and 19; R-EX-1
 
 `case` is a plain dict (the route layer assembles it from the DB; tests build it from golden files):
     records: [{n, source, date_iso|None, excerpt, [could_not_process|status|reason]}]
-    entries: [{id, record_no, summary, excerpt, review_status, [translation_label], [date_iso], [original_summary], [original_excerpt], [keep_wording]}]
+    entries: [{id, record_no, summary, excerpt, review_status, [translation_label], [date_iso], [original_summary], [original_excerpt]}]
     amounts: [{id, record_no, cents|None, cls, raw, excerpt, review_status}]   cls: charge | rate | estimate | unclear | damages | ...
     flags:   [{id, type, subtype, evidence:[{record_no, field, excerpt}], review_status, [days, from_date, to_date], [note], [reason]}]
 review_status in (accepted, edited) is "in"; dismissed/rejected is "out"; anything else is pending.
@@ -118,7 +118,6 @@ class _View:
         self.amounts = sorted(case.get("amounts", []), key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
         self.flags = list(case.get("flags", []))
         self.narrative = case.get("narrative")
-        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
 
     def verbatim(self, item):
         """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
@@ -491,7 +490,7 @@ def _edited(v):
     for e in v.entries:
         if e.get("entered_by_reviewer") and _status(e) == "in":
             out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer (the AI did not draft this entry); summary "{e["summary"]}"'
-                       + (f'; paralegal confirmed keep my wording (reviewer override: {", ".join(e["override_reasons"])})' if e.get("override_reasons") else "") + ".")
+                       + ".")
         if not _was_edited(e):
             continue
         bits = []
@@ -499,8 +498,6 @@ def _edited(v):
             bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
         if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
             bits.append(f'excerpt was "{e["original_excerpt"]}", now "{e["excerpt"]}"')
-        if e.get("keep_wording") or e.get("id") in v.keep_wording:
-            bits.append("paralegal confirmed keep my wording" + (f" (reviewer override: {', '.join(e['override_reasons'])})" if e.get("override_reasons") else ""))
         out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + ".")
     return out or ["- none"]
 
diff --git a/app/backend/review.py b/app/backend/review.py
index 135d721..f7e212f 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -1,9 +1,11 @@
 """Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).
 
-Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
-Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
-and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
-that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
+Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
+Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
+no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
+invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
+(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
+JUDGE_UNAVAILABLE).
 """
 import time
 
@@ -118,39 +120,42 @@ _QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self
                     "laterality": "a side (left or right)", "approx": "an approximation (such as approximately)"}
 
 
-def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body, ocr_derived=False):
-    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
-    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
+def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False):
+    """Code checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
+    D-034/D-047: a number/date/$ figure, a side or negation word that is not in the quote, a qualifier the summary drops, or a highlight that
+    cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
+    The judge never blocks (D-045b): its objection is returned in `warnings` and the item is stored as needs_review."""
     code_reasons = []
     lang = language.record_lang(rec)                        # D-042: a Spanish record's English summary is checked against the Spanish quote
     g = spanish.module_for(lang)
     toks = g.new_tokens(new_sum, new_exc, label, date_iso)
     numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
-    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
+    if numeric:
         raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                    tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
-    blocking = []
     if toks:
-        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
-        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
-    if g.dropped_qualifiers(new_sum, new_exc):
-        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
+        words = ", ".join("\u201c" + t + "\u201d" for t in toks)
+        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
+    dropped = g.dropped_qualifiers(new_sum, new_exc)
+    if dropped:
+        what = "; ".join(_QUALIFIER_WORDS.get(k, k) for k in dropped)
+        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
     if span is None:
-        code_reasons.append("HIGHLIGHT_NOT_FOUND")
+        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
     verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
     if call is not None:
         verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
         ladder_verdict = judges.to_ladder("j1", verdict)
+    warnings = []
     if ladder_verdict in ("partially", "unsupported"):
         code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
-        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
-    if blocking and not bool(body.get("confirm_warnings")):
-        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
+        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
+    elif ladder_verdict == "unavailable":
+        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
     state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                               {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived})
-    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
-            "judge_error": judge_error,
-            "state": state, "reasons": reasons}
+    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
+            "judge_error": judge_error, "state": state, "reasons": reasons}
 
 
 # ---------------------------------------------------------------- edit
@@ -184,22 +189,18 @@ def _edit(conn, case_id, kind, item, body, call, t):
     span = grounding.locate(rec["excerpt"], new_exc)
     base = generator.body_offset(rec)
     label, date_iso = item["provider"] or "", item["date_iso"] or ""
-    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, body,
+    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call,
                          ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
-    toks, code_reasons, blocking, ladder_verdict, call_id, state, reasons = (
-        chk["toks"], chk["code_reasons"], chk["blocking"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
-    confirmed = bool(body.get("confirm_warnings"))
+    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
+        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
     edited = dict(prev)
-    edited.update(at=store.iso(t), kept_my_wording=bool(blocking and confirmed),
-                  override_reasons=[b["code"] for b in blocking] if blocking and confirmed else prev.get("override_reasons", []))
+    edited.update(at=store.iso(t))
     if "summary" in edits or "summary" in prev:
         edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
     if "excerpt" in edits or "excerpt" in prev:
         edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                       excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
     DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
-    if edited["kept_my_wording"]:
-        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
     lad = item.get("ladder") or {"item_id": item["id"]}
     lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                     "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
@@ -208,8 +209,7 @@ def _edit(conn, case_id, kind, item, body, call, t):
     lad["state"] = state
     DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
     enforce_ocr(conn, case_id, t)
-    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
-        if ladder_verdict == "unavailable" else []
+    return chk["warnings"]
 
 
 # ---------------------------------------------------------------- confirm_date
@@ -337,7 +337,7 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
         raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
     span = grounding.locate(rec["excerpt"], excerpt)
     eid = f"e{rec['seq']}_m"
-    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, body or {},
+    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
                          ocr_derived=record_id in ocr_record_ids(conn, case_id))
     base = generator.body_offset(rec)
     ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
@@ -349,21 +349,15 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
               "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
     if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
         ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
-    if chk["blocking"]:     # reached only with confirm_warnings: the override travels to the internal notes
-        ladder["override_reasons"] = [b["code"] for b in chk["blocking"]]
     DB.add_item(conn, case_id, "entry", {
         "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
         "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
         "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
     DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
-    if chk["blocking"]:
-        DB.apply_review(conn, eid, "keep_my_wording", now=t, case=case_id)
     enforce_ocr(conn, case_id, t)
     from app.backend import present
-    warns = [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the entry stays marked for review.", "item_id": eid}] \
-        if chk["ladder_verdict"] == "unavailable" else []
     return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
-            "review": present.review_view(conn, case_id), "warnings": warns}
+            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}
 
 
 # ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
diff --git a/app/backend/store.py b/app/backend/store.py
index 6a1327c..f2ffea2 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -49,16 +49,11 @@ def export_case(conn, case_id: str) -> dict:
             d["original_summary"] = ed.get("original_summary", e["summary"])
         if "excerpt" in ed:
             d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
-        if ed.get("kept_my_wording"):
-            d["keep_wording"] = True
         lad = e.get("ladder") or {}
         if lad.get("entered_by"):
             d["entered_by_reviewer"] = True
         if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
             d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
-        if ed.get("override_reasons") or lad.get("override_reasons"):
-            d["keep_wording"] = True
-            d["override_reasons"] = ed.get("override_reasons") or lad.get("override_reasons")
         ents.append(d)
     amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                  excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
@@ -69,7 +64,7 @@ def export_case(conn, case_id: str) -> dict:
                    excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
         fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                        days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
-    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
+    events = []     # D-047: no 'keep my wording' event exists any more
     pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
     pages = (case.get("config") or {}).get("pages")
     records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
diff --git a/app/backend/trace.py b/app/backend/trace.py
index 1ac9f43..3da1094 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -232,8 +232,6 @@ def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
         ev["at"] = store.iso(evs[-1]["at"])
     if rs == "edited":
         ed = row.get("edited") or {}
-        ev["kept_my_wording"] = bool(ed.get("kept_my_wording"))
-        ev["override_reasons"] = ed.get("override_reasons") or []
         if cx.full:
             ev["edited_text"] = ed.get("summary") or ed.get("note")
     if rs in ("accepted", "edited"):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:22.582Z

**tool call — Bash**
````
{
 "command": "git show 24c18a7 --stat >/dev/null && git show 24c18a7 -- tests/ | head -400",
 "description": "Show test diff for commit 24c18a7"
}
````

### User / tool · 2026-11-02T05:10:22.701Z

**tool result**
````
commit 24c18a757beaef62d42be592f85409187531e563
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:09:49 2026 -0600

    feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
    
    Judge objections no longer block a human-written edit: saved as needs_review with a warnings[] code.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index 8a1a141..18aeb9d 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -123,7 +123,7 @@ def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode(env):
     _, c = env
     tok = run_case(c)
     e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
-    r = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10 and improving, per the paralegal."}})
+    r = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10 and improving; patient reports missing 3 days of work, per the paralegal."}})
     j = r.json()
     assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
     assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]
@@ -349,3 +349,25 @@ def test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):
         assert TestClient(app, client=(peer, 5000)).get("/api/health").status_code == 403
     monkeypatch.delenv("ZLAYT_MODE")                                    # public build: no peer restriction
     assert TestClient(app, client=("192.168.1.5", 5000)).get("/api/health").status_code == 200
+
+
+def test_side_or_negation_edit_is_a_422_with_plain_reason_and_confirm_flag_changes_nothing_d047(env):
+    _, c = env
+    tok = run_case(c)
+    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]
+    before = c.get(f"/api/cases/{tok}").json()
+    for flag in ({}, {"confirm_warnings": True}):
+        r = c.post(f"/api/cases/{tok}/items/{e5['id']}/review", json={"action": "edit", "edits": {"summary": "Visit 8: left-sided pain 4/10, improving; no missed work."}, **flag})
+        err = r.json()["error"]
+        assert r.status_code == 422 and err["code"] == "invalid_edit" and err["detail"]["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT"
+        assert {"left", "no"} <= set(err["detail"]["tokens"]) and "quote" in err["message"]
+    assert c.get(f"/api/cases/{tok}").json()["entries"] == before["entries"]
+
+
+def test_no_409_confirm_path_for_edits_or_manual_entry_remains_d047():
+    """D-047: grep the backend. The only needs_confirm left is the re-run of a case that already has decisions (api.py); review.py has no confirm flag."""
+    import pathlib
+    root = pathlib.Path(__file__).resolve().parents[2] / "app" / "backend"
+    src = {p.name: p.read_text() for p in root.glob("*.py")}
+    assert "confirm_warnings" not in "".join(src.values()) and "keep_my_wording" not in "".join(src.values())
+    assert [n for n, t in src.items() if "needs_confirm" in t] == ["api.py"]
diff --git a/tests/unit/test_export.py b/tests/unit/test_export.py
index 7af086b..da9ed14 100644
--- a/tests/unit/test_export.py
+++ b/tests/unit/test_export.py
@@ -155,13 +155,12 @@ def test_dismiss_5_pending_6_reconciliation_and_counts():
     assert "7 of 9" not in out["letter_text"] + n
 
 def test_edited_items_section():
-    """R-RV-2, R-EX-4(10): entry 3 edited -> EDITED ITEMS lists original and new text and the keep-my-wording confirmation."""
+    """R-RV-2, R-EX-4(10): entry 3 edited -> EDITED ITEMS lists original and new text. D-047: no keep-my-wording confirmation exists any more."""
     c = build_case()
     c["entries"][2].update(review_status="edited", summary="Persistent neck pain 6/10; daily headaches.", original_summary="Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.")
-    c["events"] = [dict(type="keep_my_wording", item_id="e3")]
     n = X.build_export(c)["internal_notes_text"]
     sec = n.split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
-    assert "referred to physical therapy 2x/week" in sec and "Persistent neck pain 6/10; daily headaches." in sec and "keep my wording" in sec.lower()
+    assert "referred to physical therapy 2x/week" in sec and "Persistent neck pain 6/10; daily headaches." in sec and "keep my wording" not in sec.lower()
 
 
 def test_edited_then_accepted_entry_still_listed_in_edited_items():
diff --git a/tests/unit/test_manual_and_split.py b/tests/unit/test_manual_and_split.py
index a421d60..a2f3388 100644
--- a/tests/unit/test_manual_and_split.py
+++ b/tests/unit/test_manual_and_split.py
@@ -60,20 +60,35 @@ def test_manual_entry_summary_with_new_number_is_a_hard_422(tmp_path, confirm):
     assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]
 
 
-def test_manual_entry_label_in_pending_notes_and_override_is_recorded(tmp_path):
+@pytest.mark.parametrize("confirm", [False, True])
+@pytest.mark.parametrize("summary", ["No pain, improving.", "Left-sided pain, improving.", "Pain improving without medication.", "Pain not improving."])
+def test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047(tmp_path, summary, confirm):
+    """D-047: a side/negation word absent from the quote is refused with no override; nothing is stored, no judge call, no event."""
     conn, cid = sample_with_rejected_5(tmp_path)
-    body = {"summary": "Pain improving, treatment effective.", "excerpt": "Pain 4/10, improving."}
+    events = DB.list_events(conn, cid)
+    calls = []
+    def spy(*a, **k):
+        calls.append(1); return judge("supported")(*a, **k)
     with pytest.raises(RV.ReviewError) as e:
-        RV.manual_entry(conn, cid, "r5", body, call=judge("unsupported"))
-    assert e.value.code == "needs_confirm"                                           # non-numeric judge objection: the confirm path stays
-    r = RV.manual_entry(conn, cid, "r5", {**body, "confirm_warnings": True}, call=judge("unsupported"))
+        RV.manual_entry(conn, cid, "r5", {"summary": summary, "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=spy)
+    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and e.value.detail["tokens"]
+    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]
+    assert DB.list_events(conn, cid) == events and calls == []
+
+
+def test_manual_entry_judge_objection_saves_pending_with_warning_and_no_override_note(tmp_path):
+    conn, cid = sample_with_rejected_5(tmp_path)
+    body = {"summary": "Pain improving, treatment effective.", "excerpt": "Pain 4/10, improving."}
+    r = RV.manual_entry(conn, cid, "r5", body, call=judge("unsupported"))             # D-047: no 409; the judge never blocks a human-written entry
+    assert "JUDGE_UNSUPPORTED" in [w["code"] for w in r["warnings"]] and r["item"]["state"] == "needs_review"
+    assert not [x for x in DB.list_events(conn, cid) if x["action"] == "keep_my_wording"]
     assert r["item"]["entered_by"] == "reviewer"
     notes = X.build_export(store.export_case(conn, cid))["internal_notes_text"]
     pend = notes.split("PENDING ITEMS NOT INCLUDED")[1]
     assert "[entered by reviewer]" in pend                                            # label before accept
     RV.apply_review(conn, cid, "e5_m", {"action": "accept"})
     sec = X.build_export(store.export_case(conn, cid))["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
-    assert "entered by reviewer" in sec and "paralegal confirmed keep my wording (reviewer override: JUDGE_UNSUPPORTED)" in sec
+    assert "entered by reviewer" in sec and "keep my wording" not in sec and "override" not in sec
 
 
 def test_manual_entry_refused_when_record_has_a_live_entry(tmp_path):
diff --git a/tests/unit/test_ocr_invariant.py b/tests/unit/test_ocr_invariant.py
index b411ec2..e6eedf9 100644
--- a/tests/unit/test_ocr_invariant.py
+++ b/tests/unit/test_ocr_invariant.py
@@ -80,7 +80,7 @@ def test_manual_entry_on_an_ocr_record_is_needs_review_with_the_ocr_reason(tmp_p
     rec_id = e["record_ids"][0]
     rec = next(r for r in store.load_records(conn, cid) if r["id"] == rec_id)
     quote = e["excerpt"]
-    r = RV.manual_entry(conn, cid, rec_id, {"summary": "Visit documented.", "excerpt": quote}, call=FakeCall(SUPPORTED))
+    r = RV.manual_entry(conn, cid, rec_id, {"summary": quote, "excerpt": quote}, call=FakeCall(SUPPORTED))
     assert r["item"]["state"] == "needs_review" and "OCR_DERIVED" in r["item"]["reasons"], rec["excerpt"]
 
 
diff --git a/tests/unit/test_review_rules.py b/tests/unit/test_review_rules.py
index 43ef9bf..51f3955 100644
--- a/tests/unit/test_review_rules.py
+++ b/tests/unit/test_review_rules.py
@@ -92,23 +92,63 @@ def test_added_dollar_is_a_hard_422_even_with_confirm_and_saves_nothing(tmp_path
     assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["tokens"]
     assert DB.get_item(conn, eid) == before
 
-def test_seeded_herniation_judge_unsupported_needs_confirm(tmp_path):
-    """R-RV-3: 'herniation' passes the code check but judge #1 says unsupported -> 409 with JUDGE_UNSUPPORTED."""
+def test_seeded_herniation_judge_unsupported_saves_as_needs_review_with_warning(tmp_path):
+    """D-047/D-045b: 'herniation' passes the code check but judge #1 says unsupported -> no 409; saved as needs_review, warning JUDGE_UNSUPPORTED."""
     conn, cid, out = seeded(tmp_path)
-    with pytest.raises(RV.ReviewError) as e:
-        RV.apply_review(conn, cid, ent(out, 8), dict(action="edit", edits=dict(summary="Cervical MRI: C5-C6 disc herniation with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.")), call=judge("unsupported"))
-    assert e.value.code == "needs_confirm" and "JUDGE_UNSUPPORTED" in [w["code"] for w in e.value.detail["warnings"]]
+    r = RV.apply_review(conn, cid, ent(out, 8), dict(action="edit", edits=dict(summary="Cervical MRI: C5-C6 disc herniation with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.")), call=judge("unsupported"))
+    assert r["item"]["review_status"] == "edited" and r["item"]["state"] == "needs_review"
+    assert "JUDGE_UNSUPPORTED" in [w["code"] for w in r["warnings"]]
 
-def test_keep_my_wording_resend_saves_and_logs(tmp_path):
-    """R-RV-3: resend with confirm_warnings=true saves (review_status edited) and logs a keep_my_wording event."""
+def test_no_confirm_path_remains_confirm_warnings_is_ignored_and_no_event_is_logged(tmp_path):
+    """D-047: the 409 'keep my wording' path is gone. A judge objection saves without a confirm; `confirm_warnings` changes nothing and no keep_my_wording event or override field is ever written."""
     conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
     edits = dict(summary="Visit 8: pain 4/10, improving; the patient is recovering well.")
-    with pytest.raises(RV.ReviewError) as e:
-        RV.apply_review(conn, cid, eid, dict(action="edit", edits=edits), call=judge("unsupported"))
-    assert e.value.code == "needs_confirm"                                       # non-numeric judge objection keeps the confirm path
     r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=edits, confirm_warnings=True), call=judge("unsupported"))
-    assert r["item"]["review_status"] == "edited" and r["item"]["edited"]["kept_my_wording"] is True
-    assert r["item"]["edited"]["override_reasons"] == ["JUDGE_UNSUPPORTED"]
+    assert r["item"]["review_status"] == "edited" and "kept_my_wording" not in r["item"]["edited"] and "override_reasons" not in r["item"]["edited"]
+    assert not [x for x in DB.list_events(conn, cid) if x["action"] == "keep_my_wording"]
+    from app.backend import store
+    assert store.export_case(conn, cid)["events"] == []
+
+
+_EXC5 = "Pain 4/10, improving."
+
+
+@pytest.mark.parametrize("confirm", [False, True])
+@pytest.mark.parametrize("summary,reason,key", [
+    ("Visit 8: pain 4/10, improving; no radiating symptoms.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
+    ("Visit 8: pain 4/10, improving; not in distress.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
+    ("Visit 8: pain 4/10 improving without medication.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
+    ("Visit 8: left-sided pain 4/10, improving.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
+    ("Visit 8: right shoulder pain 4/10, improving.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
+])
+def test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047(tmp_path, summary, reason, key, confirm):
+    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
+    before, events = DB.get_item(conn, eid), DB.list_events(conn, cid)
+    with pytest.raises(RV.ReviewError) as e:
+        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary=summary), confirm_warnings=confirm), call=judge("supported"))
+    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == reason and e.value.detail[key]
+    assert e.value.message and "quote" in e.value.message
+    assert DB.get_item(conn, eid) == before and DB.list_events(conn, cid) == events
+
+
+def test_dropping_a_qualifier_of_the_quote_is_a_hard_422_d047(tmp_path):
+    conn, cid, out = seeded(tmp_path); eid = ent(out, 8)
+    before = DB.get_item(conn, eid)
+    with pytest.raises(RV.ReviewError) as e:
+        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Cervical MRI: C5-C6 disc herniation with foraminal narrowing."), confirm_warnings=True), call=judge("supported"))
+    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_DROPS_QUALIFIER" and "hedge" in e.value.detail["qualifiers"]
+    assert "leaves out" in e.value.message
+    assert DB.get_item(conn, eid) == before
+
+
+def test_judge_is_not_called_when_a_code_check_fails_d047(tmp_path):
+    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
+    calls = []
+    def spy(*a, **k):
+        calls.append(1); return judge("supported")(*a, **k)
+    with pytest.raises(RV.ReviewError):
+        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Visit 8: no pain, 4/10, improving.")), call=spy)
+    assert calls == []
 
 def test_judge_unavailable_saves_with_reason(tmp_path):
     """R-RV-3: code check passes, judge fails -> saved, state needs_review, reason JUDGE_UNAVAILABLE."""
diff --git a/tests/unit/test_trace.py b/tests/unit/test_trace.py
index ad630af..b74966e 100644
--- a/tests/unit/test_trace.py
+++ b/tests/unit/test_trace.py
@@ -1027,12 +1027,18 @@ def _edit_entry(c, tok, eid, summary):
     return r
 
 
-def _mixed(c, tok):
+def _mixed(c, tok, conn):
     """The reviewer's walk: accept one entry, edit another so it drops a qualifier, dismiss the first. Returns the edited id."""
     ents = c.get(f"/api/cases/{tok}").json()["entries"]
     acc, edt = ents[0]["id"], ents[1]["id"]
     assert c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"}).status_code == 200
-    _edit_entry(c, tok, edt, REVIEWER_EDIT)
+    r = c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "edit", "edits": {"summary": REVIEWER_EDIT}})
+    assert r.status_code == 422 and r.json()["error"]["detail"]["reason"] == "SUMMARY_DROPS_QUALIFIER"     # D-047: the route refuses it, so the gate case below is legacy/hand-written data
+    orig = DB.get_item(conn, edt, tok)
+    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)   # bypass the route: the gate is the second line of defence
+    lad = orig.get("ladder") or {"item_id": edt}
+    lad.setdefault("code_checks", {}).update(qualifier_carried=False)
+    DB.update_item(conn, edt, now=9e9, case=tok, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"], ladder=lad)
     c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "dismiss"})
     return edt
 
@@ -1043,7 +1049,7 @@ def _ccf(gate):
 
 def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
     c, conn, tok, _ = env
-    edt = _mixed(c, tok)
+    edt = _mixed(c, tok, conn)
     g = _gate(c, tok)
     got = _ccf(g)
     assert [b["item_id"] for b in got] == [edt] and got[0]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and got[0]["step_id"] == "summary_qualifier"
@@ -1060,7 +1066,7 @@ def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t0
 
 def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
     c, conn, tok, _ = env
-    edt = _mixed(c, tok)
+    edt = _mixed(c, tok, conn)
     t = c.get(f"/api/cases/{tok}/items/{edt}/trace").json()
     s = steps_of(t)
     q = s["summary_qualifier"]
@@ -1075,7 +1081,7 @@ def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
 
 def test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098(env):
     c, conn, tok, _ = env
-    edt = _mixed(c, tok)
+    edt = _mixed(c, tok, conn)
     assert c.get(f"/api/cases/{tok}/export").status_code == 422
     quote = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == edt)["excerpt"]
     _edit_entry(c, tok, edt, quote)      # the quote verbatim keeps every qualifier
@@ -1088,7 +1094,7 @@ def test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t
 
 def test_dismissing_the_failing_edited_item_clears_the_blocker_t098(env):
     c, conn, tok, _ = env
-    edt = _mixed(c, tok)
+    edt = _mixed(c, tok, conn)
     c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "dismiss"})
     assert _ccf(_gate(c, tok)) == []
 
@@ -1101,7 +1107,7 @@ def test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098(env):
 
 def test_gate_ready_equals_export_allowed_with_a_failing_edit_t098(env):
     c, conn, tok, _ = env
-    _mixed(c, tok)
+    _mixed(c, tok, conn)
     for name in ("failing edit", "failing edit and run failed"):
         if name.endswith("run failed"):
             DB.update_case(conn, tok, status="failed")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:24.934Z

**tool call — Bash**
````
{
 "command": "grep -n \"speaker\\|D-040\\|Speaker\" app/backend/*.py app/llm/*.py 2>/dev/null | head -40; echo ----; grep -rn \"confirm_warnings\\|keep_my_wording\\|keep_wording\\|needs_confirm\\|kept_my_wording\\|override_reasons\\|force\" app/ --include=*.py --include=*.js --include=*.html --include=*.jsx --include=*.ts --include=*.tsx --include=*.yaml --include=*.md 2>/dev/null | grep -v node_modules | head -60",
 "description": "Grep for speaker-word string and any remaining confirm/override references"
}
````

### User / tool · 2026-11-02T05:10:25.038Z

**tool result**
````
app/backend/grounding.py:185:    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
app/backend/flags.py:52:         "source_kind": "record",   # D-040: no code or model labels who is speaking
app/backend/speaker.py:1:"""Speaker attribution v2 (T-091, D-040 / D-042): who is the speaker of an excerpt? Deterministic, local, no model, no network.
app/backend/speaker.py:3:STATUS: DISABLED. D-040 stays in force; nothing in the UI, flags or export imports this module. `ENABLED` is the
app/backend/speaker.py:4:switch and it is False. See the T-091 handoff for the score on evals/adversarial/speaker_attribution.jsonl.
app/backend/speaker.py:7:    attribute(text) -> Attribution(label, speakers, reasons)
app/backend/speaker.py:13:      "unknown"  anything else: mixed speakers, no speaker, pronoun-only speaker ("He states"), bare "C/O", titles or
app/backend/speaker.py:21:    3. A segment is a HEAD only if it starts with a recognised speaker + speech verb ("wife reports"), a "per X" /
app/backend/speaker.py:24:       function words). An unknown word, a second speaker, a speech verb or a pronoun head all fall outside it, so the
app/backend/speaker.py:25:       result is unknown. There is no deny-list of speakers or verbs on the patient path: that is what let four review
app/backend/speaker.py:28:       "Patient states EMS noted a laceration." / "... his wife drove him to the ER." The patient is still the speaker.
app/backend/speaker.py:36:ENABLED = False   # D-040: the chip stays off. Flip only after the adversarial gate is 100% AND T-091 wiring is reviewed.
app/backend/speaker.py:44:    speakers: tuple = ()
app/backend/speaker.py:49:    """What the UI would ask for. None while ENABLED is False (D-040) and for every non-patient result."""
app/backend/speaker.py:75:# speech / documentation verbs. Used ONLY to recognise a head ("<speaker> <verb>"); never as a deny-list.
app/backend/speaker.py:173:# What a continuation / complement may contain, by current speaker.
app/backend/speaker.py:285:    """Classify one segment. -> (speaker, complement_tokens, kind) or None.
app/backend/speaker.py:286:    speaker: 'patient' | 'other'; kind: 'verb' | 'per' | 'label'."""
app/backend/speaker.py:323:def _complement_ok(comp, speaker, allow_embed):
app/backend/speaker.py:325:    vocab = _VOCAB_PATIENT if speaker == "patient" else _VOCAB_OTHER
app/backend/speaker.py:347:    speakers = set()
app/backend/speaker.py:369:                return None, speakers, ["unrecognised words or a pronoun/second speaker in: " + " ".join(toks)]
app/backend/speaker.py:371:        speaker, comp, kind = h
app/backend/speaker.py:373:            if kind != "per" or any(not _complement_ok(p, speaker, False) for p in pre):
app/backend/speaker.py:374:                return None, speakers, ["unattributed text before the first speaker"]
app/backend/speaker.py:376:        if not _complement_ok(comp, speaker, allow_embed=(speaker == "patient" and kind == "verb")):
app/backend/speaker.py:377:            return None, speakers, ["unrecognised words in the statement: " + " ".join(comp)]
app/backend/speaker.py:378:        cur = speaker
app/backend/speaker.py:379:        speakers.add(speaker)
app/backend/speaker.py:381:    if pre or not speakers:
app/backend/speaker.py:382:        return None, speakers, ["no explicit speaker"]
app/backend/speaker.py:383:    return speakers, speakers, reasons
app/backend/speaker.py:389:    # a newline starts a new segment only when the next line begins with a speaker head; otherwise it is a soft wrap
app/backend/speaker.py:417:    return Attribution("unknown", tuple(sorted(allspk)), ("mixed speakers",))
----
app/llm/lexicon.yaml:1272:  false_positive: '"Probable cause" in a legal sentence is also a hedge hit: harmless, it only forces that sentence to stay in the excerpt. Permission uses of "may" are not in this entry.'
app/llm/lexicon.yaml:1314:    consumer: 'ADR-008 / D-005: a hit tags the record INJECTION_SUSPECTED. Code creates a record_warning flag (category injection_suspected, evidence = the matched phrase). Everything derived from the record is forced to needs_review, its amounts cannot be charges, and it cannot suppress other records'' flags. The text stays verbatim and is never stripped.'
app/llm/backends/anthropic_api.py:1:"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
app/frontend/batch.js:1:/* Batch accept for verified entries only (T-055, D-031). Button + Shift+A; the server enforces "verified pending entries only" (422 otherwise).
app/frontend/review.js:126:  // The "keep my wording" confirmation below (409 needs_confirm) is the pre-D-047 path: dead once backend T-100 lands (the server never answers 409 for an edit then);
app/frontend/review.js:127:  // delete showConfirm and the needs_confirm branch in RV.act with that card.
app/frontend/review.js:137:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => RV.act(id, Object.assign({}, body, { confirm_warnings: true }), { focus: "edit" }) }, "Keep my wording"),
app/frontend/review.js:176:      } else if (e && e.code === "needs_confirm") showConfirm(id, e, body);
app/frontend/manual.js:3:   Server refusals (422, D-047: the reason is shown inline and the typed text stays) are shown in plain words. The 409 needs_confirm "keep my wording" branch below is dead once backend T-100 lands; delete it with that card. Text via ZL.el only. */
app/frontend/manual.js:45:      if (confirmWarnings) body.confirm_warnings = true;
app/frontend/manual.js:51:      if (r.status === 409 && err.code === "needs_confirm") {
app/frontend/excerpt.js:2:   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows the server's reasons. */
app/frontend/mock.js:188:        else if (a === "edit" && body.edits && typeof body.edits.summary === "string" && id[0] === "e") { it.edited = { summary: body.edits.summary, original_summary: it.summary, at: new Date().toISOString(), kept_my_wording: false }; it.summary = body.edits.summary; it.review_status = "edited"; }
app/backend/dismissal_patterns.py:11:bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.
app/backend/export.py:587:    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
app/backend/review.py:93:def enforce_ocr(conn, case_id: str, t) -> int:
app/backend/review.py:211:    enforce_ocr(conn, case_id, t)
app/backend/review.py:242:    enforce_ocr(conn, case_id, t)
app/backend/review.py:357:    enforce_ocr(conn, case_id, t)
app/backend/review.py:414:    enforce_ocr(conn, case_id, t)
app/backend/api.py:361:                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
app/backend/speaker.py:3:STATUS: DISABLED. D-040 stays in force; nothing in the UI, flags or export imports this module. `ENABLED` is the
app/db/db.py:20:           "confirm_date": None, "keep_my_wording": None,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:26.920Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/review.py | sed -n 1,140p",
 "description": "Read review.py top section with line numbers"
}
````

### User / tool · 2026-11-02T05:10:26.995Z

**tool result**
````
     1	"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).
     2	
     3	Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
     4	Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
     5	no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
     6	invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
     7	(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
     8	JUDGE_UNAVAILABLE).
     9	"""
    10	import time
    11	
    12	from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
    13	from app.db import db as DB
    14	
    15	ACTIONS = ("accept", "dismiss", "reset", "edit")
    16	_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|may|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
    17	_KIND = {"e": "entry", "a": "amount", "f": "flag"}
    18	
    19	
    20	class ReviewError(Exception):
    21	    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
    22	        super().__init__(code)
    23	        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")
    24	
    25	
    26	def _now(now):
    27	    return now() if callable(now) else (time.time() if now is None else now)
    28	
    29	
    30	def _item(conn, case_id, item_id):
    31	    try:
    32	        row = DB.get_item(conn, item_id, case_id)
    33	    except KeyError:
    34	        raise ReviewError(404, "not_found", message="No such item.") from None
    35	    if row["case_id"] != case_id:
    36	        raise ReviewError(404, "not_found", message="No such item.")
    37	    return _KIND[item_id[0]], row
    38	
    39	
    40	def _bad(msg, **detail):
    41	    return ReviewError(422, "invalid_edit", detail, msg)
    42	
    43	
    44	def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
    45	    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
    46	    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
    47	    if kind != "entry":
    48	        return False
    49	    if not item.get("date_iso"):
    50	        return True
    51	    rid = (item.get("record_ids") or [None])[0]
    52	    row = conn.execute("SELECT date_status FROM records WHERE id=? AND case_id=?", (rid, case_id)).fetchone()
    53	    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)
    54	
    55	
    56	def _date_unconfirmed_error():
    57	    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
    58	                       "cannot be accepted into the letter.")
    59	
    60	
    61	def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    62	    t = _now(now)
    63	    kind, item = _item(conn, case_id, item_id)
    64	    action = (body or {}).get("action")
    65	    if action not in ACTIONS:
    66	        raise _bad("That action is not allowed.")
    67	    if item["state"] == "rejected" and action in ("accept", "edit"):
    68	        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    69	    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
    70	        raise _date_unconfirmed_error()
    71	    warnings = []
    72	    if action in ("accept", "dismiss", "reset"):
    73	        DB.apply_review(conn, item_id, action, now=t, case=case_id)
    74	        if kind == "flag" and action == "dismiss" and body.get("note"):
    75	            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    76	    else:
    77	        warnings = _edit(conn, case_id, kind, item, body, call, t)
    78	    from app.backend import present
    79	    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
    80	            "review": present.review_view(conn, case_id), "warnings": warnings}
    81	
    82	
    83	def ocr_record_ids(conn, case_id: str) -> set:
    84	    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
    85	    from app.backend import pdf_checks
    86	    pages = (DB.get_case(conn, case_id).get("config") or {}).get("pages")
    87	    if not any(p.get("source") == "ocr" for p in pages or []):
    88	        return set()
    89	    return {r[0] for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=?", (case_id,))
    90	            if pdf_checks.is_ocr_span(pages, r[1], r[2])}
    91	
    92	
    93	def enforce_ocr(conn, case_id: str, t) -> int:
    94	    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
    95	    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
    96	    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
    97	    ids = ocr_record_ids(conn, case_id)
    98	    if not ids:
    99	        return 0
   100	    n = 0
   101	    for kind in ("entry", "amount", "flag"):
   102	        for it in DB.list_items(conn, case_id, kind):
   103	            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
   104	                continue
   105	            reasons = list(it.get("state_reasons") or [])
   106	            if it["state"] == "needs_review" and "OCR_DERIVED" in reasons:
   107	                continue
   108	            if "OCR_DERIVED" not in reasons:
   109	                reasons.append("OCR_DERIVED")
   110	            out = {"state": "needs_review", "state_reasons_json": reasons}
   111	            if isinstance(it.get("ladder"), dict):
   112	                out["ladder"] = {**it["ladder"], "state": "needs_review"}
   113	            DB.update_item(conn, it["id"], now=t, case=case_id, **out)
   114	            n += 1
   115	    return n
   116	
   117	
   118	_SIDE_NEG = {"left", "right", "no", "not", "without"}
   119	_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "an attribution phrase (such as complained of or reports)", "negation": "a negation (such as no, not or denies)",
   120	                    "laterality": "a side (left or right)", "approx": "an approximation (such as approximately)"}
   121	
   122	
   123	def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False):
   124	    """Code checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
   125	    D-034/D-047: a number/date/$ figure, a side or negation word that is not in the quote, a qualifier the summary drops, or a highlight that
   126	    cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
   127	    The judge never blocks (D-045b): its objection is returned in `warnings` and the item is stored as needs_review."""
   128	    code_reasons = []
   129	    lang = language.record_lang(rec)                        # D-042: a Spanish record's English summary is checked against the Spanish quote
   130	    g = spanish.module_for(lang)
   131	    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
   132	    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
   133	    if numeric:
   134	        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
   135	                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
   136	    if toks:
   137	        words = ", ".join("\u201c" + t + "\u201d" for t in toks)
   138	        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
   139	    dropped = g.dropped_qualifiers(new_sum, new_exc)
   140	    if dropped:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:10:28.138Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/review.py | sed -n 140,460p",
 "description": "Read rest of review.py with line numbers"
}
````

### User / tool · 2026-11-02T05:10:28.221Z

**tool result**
````
   140	    if dropped:
   141	        what = "; ".join(_QUALIFIER_WORDS.get(k, k) for k in dropped)
   142	        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
   143	    if span is None:
   144	        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
   145	    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
   146	    if call is not None:
   147	        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
   148	        ladder_verdict = judges.to_ladder("j1", verdict)
   149	    warnings = []
   150	    if ladder_verdict in ("partially", "unsupported"):
   151	        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
   152	        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
   153	    elif ladder_verdict == "unavailable":
   154	        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
   155	    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
   156	                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived})
   157	    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
   158	            "judge_error": judge_error, "state": state, "reasons": reasons}
   159	
   160	
   161	# ---------------------------------------------------------------- edit
   162	def _edit(conn, case_id, kind, item, body, call, t):
   163	    edits = body.get("edits")
   164	    if kind == "amount":
   165	        raise _bad("A charge can only be accepted or dismissed.")
   166	    if not isinstance(edits, dict) or not edits:
   167	        raise _bad("Nothing to edit.")
   168	    if kind == "flag":
   169	        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
   170	            raise _bad("Only a note can be added to a flag.")
   171	        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
   172	        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
   173	        return []
   174	    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
   175	        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
   176	    case = DB.get_case(conn, case_id)
   177	    recs = store.load_records(conn, case_id, case["raw_text"])
   178	    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
   179	    if rec is None:
   180	        raise _bad("The entry's source record is missing.")
   181	    prev = item.get("edited") or {}
   182	    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
   183	    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
   184	    span = None
   185	    if "excerpt" in edits:
   186	        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
   187	        if problems:
   188	            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
   189	    span = grounding.locate(rec["excerpt"], new_exc)
   190	    base = generator.body_offset(rec)
   191	    label, date_iso = item["provider"] or "", item["date_iso"] or ""
   192	    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call,
   193	                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
   194	    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
   195	        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
   196	    edited = dict(prev)
   197	    edited.update(at=store.iso(t))
   198	    if "summary" in edits or "summary" in prev:
   199	        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
   200	    if "excerpt" in edits or "excerpt" in prev:
   201	        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
   202	                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
   203	    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
   204	    lad = item.get("ladder") or {"item_id": item["id"]}
   205	    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
   206	                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
   207	    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
   208	                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
   209	    lad["state"] = state
   210	    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
   211	    enforce_ocr(conn, case_id, t)
   212	    return chk["warnings"]
   213	
   214	
   215	# ---------------------------------------------------------------- confirm_date
   216	def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
   217	    t = _now(now)
   218	    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
   219	    if row is None:
   220	        raise ReviewError(404, "not_found", message="No such record.")
   221	    rec = DB._decode(row)
   222	    if rec["date_status"] != "ambiguous":
   223	        raise _bad("Only a record whose date can be read two ways can be confirmed.")
   224	    if date_iso not in (rec["date_candidates"] or []):
   225	        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
   226	    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
   227	    moved, cleared = None, []
   228	    for e in DB.list_items(conn, case_id, "entry"):
   229	        if record_id in (e["record_ids"] or []):
   230	            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
   231	            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
   232	                cleared.append(e["id"])
   233	            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
   234	    for a in DB.list_items(conn, case_id, "amount"):
   235	        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
   236	            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
   237	            cleared.append(a["id"])
   238	    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
   239	    removed += _recompute_gaps(conn, case_id, t)
   240	    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
   241	    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
   242	    enforce_ocr(conn, case_id, t)
   243	    from app.backend import present
   244	    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
   245	            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
   246	            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
   247	
   248	
   249	def _without_date_doubt(item: dict) -> dict:
   250	    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
   251	    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
   252	    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
   253	    state = item["state"]
   254	    if state == "needs_review" and not reasons:
   255	        state = "verified"
   256	    out = {"state": state, "state_reasons_json": reasons}
   257	    if isinstance(item.get("ladder"), dict):
   258	        out["ladder"] = {**item["ladder"], "state": state}
   259	    return out
   260	
   261	
   262	def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
   263	    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
   264	             "cleared_date_ambiguous": cleared}
   265	    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
   266	    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
   267	                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
   268	
   269	
   270	def _drop(conn, case_id, flag_id):
   271	    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
   272	    return [flag_id] if cur.rowcount else []
   273	
   274	
   275	def _recompute_gaps(conn, case_id, t):
   276	    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
   277	    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
   278	    from app.backend import pipeline as PL
   279	    case = DB.get_case(conn, case_id)
   280	    recs = store.load_records(conn, case_id, case["raw_text"])
   281	    by_n = {r["n"]: r for r in recs}
   282	    backend = DB.get_case(conn, case_id).get("backend") or "code"
   283	    new = {}
   284	    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
   285	        nos = f["record_nos"]
   286	        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
   287	        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
   288	                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
   289	                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
   290	        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
   291	            if k in f:
   292	                item[k] = f[k]
   293	        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
   294	        new[item["id"]] = item
   295	    removed = []
   296	    for old in DB.list_items(conn, case_id, "flag"):
   297	        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
   298	            continue
   299	        item = new.get(old["id"])
   300	        if item is None:
   301	            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
   302	            removed.append(old["id"])
   303	            continue
   304	        oc = old.get("computed") or {}
   305	        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
   306	        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
   307	            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
   308	    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
   309	    for iid, item in new.items():
   310	        if iid not in have:
   311	            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
   312	    return removed
   313	
   314	
   315	# ---------------------------------------------------------------- manual entry (D-031, T-056)
   316	def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
   317	    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
   318	    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
   319	    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
   320	    t = _now(now)
   321	    case = DB.get_case(conn, case_id)
   322	    recs = store.load_records(conn, case_id, case["raw_text"])
   323	    rec = next((r for r in recs if r["id"] == record_id), None)
   324	    if rec is None:
   325	        raise ReviewError(404, "not_found", message="No such record.")
   326	    if rec.get("duplicate_of"):
   327	        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
   328	    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
   329	    if live:
   330	        raise _bad("This record already has an entry; edit that entry instead.")
   331	    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
   332	    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
   333	        raise _bad("Provide a summary and the quoted sentences.")
   334	    summary, excerpt = summary.strip(), excerpt.strip()
   335	    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
   336	    if problems:
   337	        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
   338	    span = grounding.locate(rec["excerpt"], excerpt)
   339	    eid = f"e{rec['seq']}_m"
   340	    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
   341	                         ocr_derived=record_id in ocr_record_ids(conn, case_id))
   342	    base = generator.body_offset(rec)
   343	    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
   344	              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
   345	                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
   346	              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
   347	                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
   348	                              "date_provider_from_header": True},
   349	              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
   350	    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
   351	        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
   352	    DB.add_item(conn, case_id, "entry", {
   353	        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
   354	        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
   355	        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
   356	    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
   357	    enforce_ocr(conn, case_id, t)
   358	    from app.backend import present
   359	    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
   360	            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}
   361	
   362	
   363	# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
   364	def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
   365	    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
   366	    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
   367	    `not_duplicate` event on the original entry."""
   368	    from app.backend import pipeline as PL
   369	    from app.llm import provider as P
   370	    t = _now(now)
   371	    kind, ent = _item(conn, case_id, entry_id)
   372	    if kind != "entry":
   373	        raise _bad("Only a merged entry can be split.")
   374	    ids = list(ent["record_ids"] or [])
   375	    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
   376	        raise _bad("That record is not one of the duplicates merged into this entry.")
   377	    case = DB.get_case(conn, case_id)
   378	    cfg = dict(case.get("config") or {})
   379	    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
   380	    DB.update_case(conn, case_id, config_json=cfg)
   381	    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
   382	    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
   383	    recs = store.load_records(conn, case_id, case["raw_text"])
   384	    by_n = {r["n"]: r for r in recs}
   385	    rec = next(r for r in recs if r["id"] == record_id)
   386	    warns = []
   387	    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
   388	    if call is not None:
   389	        e = generator.extract_one(rec, [rec["n"]], call=call, case_text=case["raw_text"])
   390	        if "failure" in e:
   391	            warns.append({"code": e["failure"], "message": "The record was split off, but the AI could not draft its entry; enter it by hand.", "item_id": None})
   392	        else:
   393	            if e["state"] != "rejected":
   394	                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
   395	            e["ladder"]["backend"] = P.backend_name()
   396	            e.pop("_stage", None)
   397	            _upsert(conn, case_id, "entry", PL._clean(e), t)
   398	    else:
   399	        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
   400	    # its amounts come back as their own items (new ids; existing amounts keep theirs and their review status)
   401	    sep = {int(str(i)[1:]) for i in cfg["not_duplicates"] if str(i)[1:].isdigit()}
   402	    rows = [a for a in AM.extract_amounts(recs, separate=sep) if a["record_no"] == rec["n"]]
   403	    new_items = [PL.amount_item(a, rec) for a in rows]
   404	    ing = {"records": recs, "text": case["raw_text"]}
   405	    for a in DB.list_items(conn, case_id, "amount"):
   406	        if record_id in (a["record_ids"] or []):
   407	            DB.update_item(conn, a["id"], now=t, case=case_id, record_ids_json=[i for i in a["record_ids"] if i != record_id], duplicate_note=None)
   408	    dollars = [a for a in new_items if a["cls"] != "damages"]
   409	    verdicts = judges_for(dollars, call, case["raw_text"])
   410	    for a in new_items:
   411	        _upsert(conn, case_id, "amount", PL._finish_amount(a, ing, verdicts.get(a["id"])), t)
   412	    _recompute_gaps(conn, case_id, t)
   413	    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
   414	    enforce_ocr(conn, case_id, t)
   415	    from app.backend import present
   416	    split_id = f"e{rec['n']}" if any(e["id"] == f"e{rec['n']}" for e in DB.list_items(conn, case_id, "entry")) else None
   417	    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
   418	            "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": warns}
   419	
   420	
   421	def _upsert(conn, case_id, kind, item, t):
   422	    """Add or refresh ONE item without PL._persist's removal of other pending rows."""
   423	    from app.backend import pipeline as PL
   424	    row = PL._row(kind, item)
   425	    if any(i["id"] == item["id"] for i in DB.list_items(conn, case_id, kind)):
   426	        DB.update_item(conn, item["id"], now=t, case=case_id, **row)
   427	    else:
   428	        DB.add_item(conn, case_id, kind, {"id": item["id"], **row}, now=t)
   429	
   430	
   431	def judges_for(dollars, call, case_text):
   432	    if call is None or not dollars:
   433	        return {}
   434	    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)
   435	
   436	
   437	def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
   438	    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
   439	    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
   440	    DB.apply_review(conn, item_id, action, now=now, case=case_id)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:04.941Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-040\\|D-045\\|D-047\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-600; echo ----; grep -n \"_SIDE_NEG\\|code_reasons\\|def new_tokens\\|def dropped_qualifiers\\|SELF_CARRIED\" app/backend/*.py | head -40; echo ----; grep -n \"review\\|batch\\|manual\\|edit\" app/backend/api.py | grep -n \"route\\|@\\|def \\|post\\|patch\" | head -60",
 "description": "Find D-040/D-045/D-047 text, unused symbols, and route definitions"
}
````

### User / tool · 2026-11-02T05:11:05.072Z

**tool result**
````
48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need r
53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
----
app/backend/confidence.py:42:_LADDER_KEYS = {"grounding_failures", "schema_valid", "code_reasons", "judge"}
app/backend/confidence.py:57:    for c in ladder.get("code_reasons", []) or []:
app/backend/generator.py:77:    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
app/backend/generator.py:79:        code_reasons.append("LANGUAGE_UNCERTAIN")
app/backend/generator.py:82:        code_reasons += g.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
app/backend/generator.py:84:            code_reasons.append("HIGHLIGHT_NOT_FOUND")
app/backend/generator.py:90:    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
app/backend/generator.py:91:              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
app/backend/generator.py:95:    return compose(e, record, grounding_failures=failures, code_reasons=list(dict.fromkeys(code_reasons)))
app/backend/generator.py:98:def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
app/backend/generator.py:104:    if code_reasons is not None:
app/backend/generator.py:105:        st["code_reasons"] = code_reasons
app/backend/generator.py:106:    st.setdefault("code_reasons", [])
app/backend/generator.py:113:        {"grounding_failures": st["grounding_failures"], "schema_valid": st["schema_valid"], "code_reasons": st["code_reasons"],
app/backend/flags.py:40:    ladder = {"grounding_failures": st["grounding_failures"], "schema_valid": True, "code_reasons": [], "judge": st.get("judge")}
app/backend/grounding.py:146:def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/grounding.py:169:_SELF_CARRIED = re.compile(r"\bc/o\b|\bcomplain(?:s|ed|ing|t)?\b|\b(?:patient|pt\.?|he|she|client)\s+(?:states?|stated|reports?|reported|endorses|admits|"
app/backend/grounding.py:180:def dropped_qualifiers(summary: str, excerpt: str) -> list:
app/backend/grounding.py:185:    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
app/backend/grounding.py:217:    for kind, rx in (("self_report", _SELF_CARRIED), ("negation", _NEG), ("laterality", _LATERAL), ("approx", _APPROX)):
app/backend/pipeline.py:44:                                     "code_reasons": []}, ctx)
app/backend/pipeline.py:78:        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
app/backend/pipeline.py:232:         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
app/backend/reclassify.py:130:    state, reasons = confidence.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": ladder_verdict},
app/backend/review.py:118:_SIDE_NEG = {"left", "right", "no", "not", "without"}
app/backend/review.py:128:    code_reasons = []
app/backend/review.py:155:    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
app/backend/review.py:157:    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
app/backend/review.py:194:    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
app/backend/review.py:195:        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
app/backend/review.py:208:                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
app/backend/review.py:347:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/spanish_text.py:189:def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/spanish_text.py:216:def dropped_qualifiers(summary: str, excerpt: str) -> list:
app/backend/spanish_text.py:232:    if (_cue_set(excerpt, _SELF_CUES, _SELF_PHRASES) or grounding._SELF_CARRIED.search(excerpt)) and not (
app/backend/spanish_text.py:233:            grounding._SELF_CARRIED.search(summary) or _EN_SELF.search(summary)):
----
1:1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
3:151:    @app.exception_handler(review.ReviewError)
4:152:    async def _review_error(_, e):
7:424:    async def manual_entry(token: str, rid: str, request: Request):
11:469:    @app.post("/api/cases/{token}/narrative/review")
12:470:    async def narrative_review(token: str, request: Request):
15:496:    @app.post("/api/cases/{token}/items/{item_id}/review")
16:497:    async def review_item(token: str, item_id: str, request: Request):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:07.461Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/grounding.py | sed -n 120,240p; echo ----; cat -n app/backend/spanish_text.py | sed -n 180,245p",
 "description": "Read token and qualifier checks in grounding and spanish_text"
}
````

### User / tool · 2026-11-02T05:11:07.567Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:19.577Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/api.py | sed -n 145,165p; echo ----; cat -n app/backend/api.py | sed -n 340,375p; echo ----; cat -n app/backend/api.py | sed -n 420,520p",
 "description": "Read API routes for manual entry, review, and rerun"
}
````

### User / tool · 2026-11-02T05:11:19.688Z

**tool result**
````
   145	
   146	    # -------------------------------------------------- errors / headers
   147	    @app.exception_handler(ApiError)
   148	    async def _api_error(_, e):
   149	        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
   150	
   151	    @app.exception_handler(review.ReviewError)
   152	    async def _review_error(_, e):
   153	        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
   154	
   155	    @app.exception_handler(StarletteHTTPException)
   156	    async def _http_error(_, e):
   157	        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
   158	        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)
   159	
   160	    @app.exception_handler(Exception)
   161	    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
   162	        log.error("unhandled %s", type(e).__name__)
   163	        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
   164	
   165	    @app.exception_handler(RequestValidationError)
----
   340	        except Exception as e:                                   # code only: no message text from the pipeline
   341	            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
   342	                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
   343	        finally:
   344	            c.close()
   345	            runs.pop(token, None)
   346	
   347	    @app.post("/api/cases/{token}/run", status_code=202)
   348	    async def run_case(token: str, request: Request):
   349	        b = await body_of(request)
   350	        c = conn()
   351	        try:
   352	            case = get_case(c, token)
   353	            if case["status"] == "running" or token in runs:
   354	                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
   355	            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
   356	                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
   357	            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
   358	                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
   359	            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
   360	            if decided and b.get("confirm_rerun") is not True:
   361	                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
   362	            now = time.time()
   363	            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
   364	            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
   365	            runs[token].start()
   366	            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
   367	        finally:
   368	            c.close()
   369	
   370	    @app.post("/api/cases/{token}/rejudge")
   371	    async def rejudge_case(token: str):
   372	        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
   373	        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
   374	        from app.backend import rejudge as RJ
   375	        c = conn()
----
   420	        finally:
   421	            c.close()
   422	
   423	    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
   424	    async def manual_entry(token: str, rid: str, request: Request):
   425	        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
   426	        b = await body_of(request)
   427	        c = conn()
   428	        try:
   429	            get_case(c, token)
   430	            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
   431	        finally:
   432	            c.close()
   433	
   434	    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
   435	    async def not_duplicate(token: str, item_id: str, request: Request):
   436	        """D-031: split one record back out of a merged entry. Body {record_id}."""
   437	        b = await body_of(request)
   438	        if not isinstance(b.get("record_id"), str):
   439	            raise ApiError(400, "bad_request", "Provide the record to split off.")
   440	        c = conn()
   441	        try:
   442	            get_case(c, token)
   443	            return review.not_duplicate(c, token, item_id, b["record_id"], call=make_call(c, token))
   444	        finally:
   445	            c.close()
   446	
   447	    @app.get("/api/cases/{token}/narrative")
   448	    def narrative_get(token: str):
   449	        c = conn()
   450	        try:
   451	            get_case(c, token)
   452	            return {"narrative": narrative.get(c, token)}
   453	        finally:
   454	            c.close()
   455	
   456	    @app.post("/api/cases/{token}/narrative")
   457	    def narrative_draft(token: str):
   458	        """D-031: draft the firm-voice paragraph from ACCEPTED entries (each sentence code-checked and judged; failures removed with a reason)."""
   459	        c = conn()
   460	        try:
   461	            get_case(c, token)
   462	            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
   463	            if nar.get("error") == "NO_ACCEPTED_ENTRIES":
   464	                raise ApiError(400, "bad_request", "Accept at least one entry first; the paragraph is written from accepted entries only.")
   465	            return {"narrative": nar}
   466	        finally:
   467	            c.close()
   468	
   469	    @app.post("/api/cases/{token}/narrative/review")
   470	    async def narrative_review(token: str, request: Request):
   471	        b = await body_of(request)
   472	        c = conn()
   473	        try:
   474	            get_case(c, token)
   475	            try:
   476	                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
   477	            except KeyError:
   478	                raise ApiError(404, "not_found", "No draft paragraph yet.") from None
   479	            except ValueError:
   480	                raise ApiError(422, "invalid_edit", "That action is not allowed.") from None
   481	        finally:
   482	            c.close()
   483	
   484	    @app.get("/api/cases/{token}/items/{item_id}")
   485	    def item(token: str, item_id: str):
   486	        c = conn()
   487	        try:
   488	            get_case(c, token)
   489	            try:
   490	                return present.why_view(c, token, item_id)
   491	            except (KeyError, IndexError):
   492	                raise ApiError(404, "not_found", "No such item.") from None
   493	        finally:
   494	            c.close()
   495	
   496	    @app.post("/api/cases/{token}/items/{item_id}/review")
   497	    async def review_item(token: str, item_id: str, request: Request):
   498	        b = await body_of(request)
   499	        c = conn()
   500	        try:
   501	            get_case(c, token)
   502	            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
   503	        finally:
   504	            c.close()
   505	
   506	    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
   507	    from app.backend import billing
   508	    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
   509	    from app.backend import pdf_routes
   510	    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
   511	    from app.backend import reclassify
   512	    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
   513	    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
   514	    from app.backend import calibration_route
   515	    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
   516	
   517	    @app.get("/api/cases/{token}/export")
   518	    def export(token: str):
   519	        from app.backend import export_routes as XR
   520	        c = conn()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:22.015Z

**tool call — Bash**
````
{
 "command": "grep -n \"apply_review(\\|update_item(\\|add_item(\" app/backend/*.py | grep -v \"def \" | cut -c1-220; echo ----; grep -n \"def apply_batch\" -A30 app/backend/case_extras.py | cut -c1-220 | head -50",
 "description": "Find all writers of review state and summary, and batch apply"
}
````

### User / tool · 2026-11-02T05:11:22.118Z

**tool result**
````
app/backend/api.py:502:            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
app/backend/dismissal_patterns.py:87:        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
app/backend/pipeline.py:196:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
app/backend/pipeline.py:198:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
app/backend/pipeline.py:202:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
app/backend/reclassify.py:139:    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/rejudge.py:79:            DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
app/backend/rejudge.py:87:        DB.update_item(conn, row["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/review.py:73:        DB.apply_review(conn, item_id, action, now=t, case=case_id)
app/backend/review.py:75:            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
app/backend/review.py:113:            DB.update_item(conn, it["id"], now=t, case=case_id, **out)
app/backend/review.py:171:        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
app/backend/review.py:172:        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
app/backend/review.py:203:    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
app/backend/review.py:210:    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/review.py:230:            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
app/backend/review.py:236:            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
app/backend/review.py:305:        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
app/backend/review.py:307:            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
app/backend/review.py:311:            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
app/backend/review.py:352:    DB.add_item(conn, case_id, "entry", {
app/backend/review.py:356:    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
app/backend/review.py:382:    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
app/backend/review.py:407:            DB.update_item(conn, a["id"], now=t, case=case_id, record_ids_json=[i for i in a["record_ids"] if i != record_id], duplicate_note=None)
app/backend/review.py:413:    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
app/backend/review.py:426:        DB.update_item(conn, item["id"], now=t, case=case_id, **row)
app/backend/review.py:428:        DB.add_item(conn, case_id, kind, {"id": item["id"], **row}, now=t)
app/backend/review.py:440:    DB.apply_review(conn, item_id, action, now=now, case=case_id)
----
44:def apply_batch(conn, case_id, body, now):
45-    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
46-    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
47-    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
48-            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
49-        raise ValueError("bad_request")
50-    with _LOCK:
51-        bad = _check(conn, case_id, ids, action)
52-        if bad:
53-            raise BatchRefused(bad)
54-        done = []
55-        try:
56-            for i in ids:
57-                review.batch_apply(conn, case_id, i, action, now)
58-                done.append(i)
59-        except Exception:
60-            for i in reversed(done):          # compensate: each undo is itself an audited event
61-                review.batch_apply(conn, case_id, i, "reset", now)
62-            raise
63-    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
64-    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}
65-
66-
67-# ------------------------------------------------------------------ export config
68-def validate_config(b):
69-    """Returns the normalised config or raises ValueError. All keys optional; unknown keys refused."""
70-    if not isinstance(b, dict) or set(b) - set(EXPORT_KEYS):
71-        raise ValueError("invalid_edit")
72-    out = {}
73-    for k in ("exhibit", "bates_prefix"):
74-        v = b.get(k)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:25.584Z

**tool call — Bash**
````
{
 "command": "grep -n \"def apply_review\" -A32 app/db/db.py | cut -c1-200; echo ----; sed -n 12,26p app/db/db.py | cut -c1-200",
 "description": "Read DB.apply_review and action table in db.py"
}
````

### User / tool · 2026-11-02T05:11:25.681Z

**tool result**
````
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
231-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
232-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
233-        conn.execute("COMMIT")
234-    except Exception:
235-        conn.execute("ROLLBACK")
236-        raise
237-    return get_item(conn, item_id, row["case_id"])
238-
239-
240-def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
241-    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
242-    if action not in AUDIT_ONLY_ACTIONS:
243-        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
244-    eid = _tok("v")
245-    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
246-                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
247-    return eid
----
import re
import secrets
import sqlite3
import time

RETENTION_SECONDS = 24 * 3600
REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
           "confirm_date": None, "keep_my_wording": None,
           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:28.256Z

**tool call — Bash**
````
{
 "command": "git show 24c18a7 -- memory/contracts/api.md; echo ----; grep -rn \"summary_qualifier\\|SUMMARY_DROPS_QUALIFIER\\|SUMMARY_TOKEN_NOT_IN_EXCERPT\\|SUMMARY_NUMBER\" app/ --include=*.py | cut -c1-220",
 "description": "Show api.md diff and gate-related references"
}
````

### User / tool · 2026-11-02T05:11:28.372Z

**tool result**
````
commit 24c18a757beaef62d42be592f85409187531e563
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:09:49 2026 -0600

    feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
    
    Judge objections no longer block a human-written edit: saved as needs_review with a warnings[] code.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 337f8bc..b0eb8e7 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -6,7 +6,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 - Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
 - `{token}` is the case id: a random 128-bit URL-safe string. It is the only credential. **There is no case-list endpoint.** An unknown token is `404 not_found`.
 - Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
-- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
+- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has decisions only; never an edit or manual entry, D-047), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
 - Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
 - `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
 - Untrusted strings (record text, excerpts, summaries) are plain text; clients must insert them with `textContent`.
@@ -23,7 +23,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 | POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
 | GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
 | POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
-| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
+| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
 | POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
 | GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
 | POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
@@ -313,19 +313,17 @@ All single-item human decisions. Request body (one of these per call; shown as a
   { "action": "reset" },
   { "action": "edit", "edits": { "summary": "Discharged from physical therapy after two missed appointments; pain 3/10." } },
   { "action": "edit", "edits": { "excerpt": "Discharged from PT after two missed appointments. Pain 3/10." } },
-  { "action": "edit", "edits": { "note": "Ask client about the 2023 episode." }, "confirm_warnings": false }
+  { "action": "edit", "edits": { "note": "Ask client about the 2023 episode." } }
 ]
 ```
 Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
 
-**Edit re-check order (R-RV-3, ADR-005).** (1) Structure, else 422. (2) Code token check (ADR-012) and (3) judge 1 re-run. If the code check finds a number, date, dollar figure or left/right/no/not/without that is not in the quote, or the judge says `partially`/`unsupported`, nothing is saved and the response is 409:
-```json
-{ "error": { "code": "needs_confirm", "message": "This edit adds a number or fact that is not in the quote.",
-    "detail": { "warnings": [
-      {"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "“$9,000” is not in the quote.", "item_id": "e3"},
-      {"code": "JUDGE_UNSUPPORTED", "message": "The second check could not support “herniation” from the quote.", "item_id": "e3"} ] } } }
-```
-The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.
+**Edit re-check order (R-RV-3, ADR-005; D-034, D-047).** (1) Structure, else 422. (2) Code checks (ADR-012). Any of these is a **hard `422 invalid_edit`**: nothing is saved, no judge call is made, no event is logged, and there is **no confirm or override** (the `409 needs_confirm` / `confirm_warnings` / `keep_my_wording` path is removed; a `confirm_warnings` field in a body is ignored):
+- a number, date or $ figure in the summary that is not in the quote, its source label or the parsed date: `detail.reason "SUMMARY_NUMBER_NOT_IN_EXCERPT"`, `detail.tokens`;
+- a side or negation word (`left`, `right`, `no`, `not`, `without`) in the summary that the quote does not have: `detail.reason "SUMMARY_TOKEN_NOT_IN_EXCERPT"`, `detail.tokens`;
+- a qualifier the quote carries that the summary leaves out (hedge, attribution phrase, negation, side, approximation): `detail.reason "SUMMARY_DROPS_QUALIFIER"`, `detail.qualifiers[]` (`hedge`, `self_report`, `negation`, `laterality`, `approx`);
+- a quote that cannot be located in the record: `detail.reason "HIGHLIGHT_NOT_FOUND"`.
+`message` is a plain sentence naming the words, e.g. `The summary says “left”, which the quote does not say. Remove it or change the quote.` These are the same checks the export gate (T-098) runs, so an edit the route stores can never be an export blocker for a code reason. The same rule applies to `POST .../records/{rid}/entry`. (3) Judge 1 re-run: it never blocks a human-written edit (D-045b). If it says `partially`/`unsupported`, errors, times out, or has no recorded fixture (always the case in demo mode), the edit is saved, the item becomes `needs_review` (reason `JUDGE_UNAVAILABLE` when it did not answer) and `warnings[]` carries `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_UNAVAILABLE`; no 409, because nothing the code can verify is wrong. The judge never lets an unchecked edit look verified.
 
 Response 200:
 ```json
----
app/backend/why.py:6:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
app/backend/why.py:7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
app/backend/trace.py:69:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
app/backend/trace.py:76:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
app/backend/trace.py:353:    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
app/backend/trace.py:355:              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
app/backend/trace.py:356:    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
app/backend/trace.py:357:              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
app/backend/trace.py:412:    if code == "SUMMARY_DROPS_QUALIFIER":
app/backend/trace.py:416:    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
app/backend/spanish_text.py:7:gets SUMMARY_TOKEN_NOT_IN_EXCERPT / SUMMARY_DROPS_QUALIFIER, which route it to the paralegal (fail toward flagging).
app/backend/spanish_text.py:253:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/spanish_text.py:255:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/confidence.py:7:    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
app/backend/narrative.py:18:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, an attribution phrase or a negation that the cited quote has.",
app/backend/narrative.py:60:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/narrative.py:62:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:135:                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
app/backend/review.py:138:        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/review.py:142:        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:208:                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
app/backend/review.py:347:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/generator.py:91:              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
app/backend/grounding.py:229:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/grounding.py:231:        reasons.append("SUMMARY_DROPS_QUALIFIER")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:32.358Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/trace.py | sed -n 330,362p; echo ----; cat -n app/backend/trace.py | sed -n 405,425p; echo ----; grep -n \"def gate\\|def export_gate\\|export_blockers\\|def _ccf\\|blockers\" app/backend/*.py | cut -c1-200 | head -30",
 "description": "Read trace code-check steps and find the export gate"
}
````

### User / tool · 2026-11-02T05:11:32.464Z

**tool result**
````
   330	                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
   331	
   332	    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
   333	        if stop:
   334	            st.append(_skipped(sid, label, "code", stop, rule))
   335	        elif failed if failed is not None else code in R:
   336	            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
   337	        else:
   338	            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
   339	    # 2 grounding substring
   340	    if schema_fail:
   341	        st.append(_skipped("excerpt_verbatim", "Quote is word for word in the record", "code", "SCHEMA_INVALID", "row 4"))
   342	    elif verbatim_fail:
   343	        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text("GROUNDING_EXCERPT_NOT_VERBATIM"),
   344	                       reason="GROUNDING_EXCERPT_NOT_VERBATIM", rule="row 4", evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
   345	    else:
   346	        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.",
   347	                       rule="row 4", evidence={"excerpt": exc}))
   348	    code_step("excerpt_whole_sentence", "Quote is made of whole sentences", "EXCERPT_NOT_WHOLE_SENTENCE", "The quote starts and ends on whole sentences.", "row 4",
   349	              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False)
   350	    code_step("excerpt_hedge", "Quote keeps the hedge sentence that qualifies it", "EXCERPT_OMITS_QUALIFIER", "No hedge sentence that qualifies the quote is left out.", "row 4",
   351	              na("EDIT_QUOTE", {"item_id": row["id"]}))
   352	    toks = cc.get("summary_tokens_not_in_excerpt") or []
   353	    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
   354	              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
   355	              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
   356	    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
   357	              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
   358	    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
   359	              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False)
   360	    # date confirmed (D-041)
   361	    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
   362	    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
----
   405	
   406	
   407	def _fix_action(row, stp) -> dict:
   408	    """The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure)."""
   409	    code, summ, exc = stp["reason_code"], *_current_text(row)
   410	    target = {"item_id": row["id"]}
   411	    tail = " The export stays blocked until it passes."
   412	    if code == "SUMMARY_DROPS_QUALIFIER":
   413	        terms = grounding.missing_qualifier_terms(summ, exc)
   414	        what = ", ".join(f"\u2018{t}\u2019" for t in terms) if terms else "the quote's hedge, attribution, negation, side or approximation"
   415	        return na("EDIT_SUMMARY", target, text=f"Edit the summary to keep {what}; the quote says it and your summary leaves it out." + tail)
   416	    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
   417	        toks = (stp.get("evidence") or {}).get("tokens") or []
   418	        what = ", ".join(f"\u2018{t}\u2019" for t in toks) if toks else "the words that are not in the quote"
   419	        return na("EDIT_SUMMARY", target, text=f"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}." + tail)
   420	    if code in ("EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER"):
   421	        return na("EDIT_QUOTE", target, text=_NEXT["EDIT_QUOTE"] + tail)
   422	    return na("READ_RECORD", {"record_id": (row.get("record_ids") or [None])[0]}, text="Read the record yourself, then fix the quote or dismiss this item." + tail)
   423	
   424	
   425	def code_check_blockers(conn, case_id: str, cx=None) -> list:
----
app/backend/api.py:526:            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
app/backend/api.py:527:                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
app/backend/export.py:568:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:569:    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""
app/backend/export.py:587:    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
app/backend/export_routes.py:28:    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
app/backend/export_routes.py:29:        raise export.ExportBlocked(case["export_blockers"])
app/backend/export_routes.py:69:    except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
app/backend/export_routes.py:71:                                                                "detail": {"blockers": e.items}}})
app/backend/rejudge.py:92:            "export_gate": {"ready": gate["ready"], "status": gate["status"], "blockers": gate["blockers"]}}
app/backend/store.py:75:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/store.py:76:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/trace.py:425:def code_check_blockers(conn, case_id: str, cx=None) -> list:
app/backend/trace.py:426:    """Export blockers (D-045(b)): accepted or edited entries whose wording the paralegal wrote or edited and whose current summary or quote fails a code check.
app/backend/trace.py:768:def judge_not_run_blockers(conn, case_id: str) -> list:
app/backend/trace.py:769:    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one."""
app/backend/trace.py:970:    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
app/backend/trace.py:971:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/trace.py:972:    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
app/backend/trace.py:976:    ready = not blockers
app/backend/trace.py:977:    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
app/backend/trace.py:986:        first = blockers[0]
app/backend/trace.py:991:    gate.update(ready=ready, blockers=blockers, warnings=warnings)
app/backend/trace.py:1005:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
app/backend/trace.py:1015:    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
app/backend/trace.py:1017:        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:11:33.912Z

**tool call — Bash**
````
{
 "command": "cat -n app/backend/trace.py | sed -n 425,470p; echo ----; grep -n \"def _current_text\" -A12 app/backend/trace.py | cut -c1-220",
 "description": "Read the code-check export blocker logic and current-text helper"
}
````

### User / tool · 2026-11-02T05:11:34.021Z

**tool result**
````
   425	def code_check_blockers(conn, case_id: str, cx=None) -> list:
   426	    """Export blockers (D-045(b)): accepted or edited entries whose wording the paralegal wrote or edited and whose current summary or quote fails a code check.
   427	    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
   428	    cx = cx or _Cx(conn, case_id, False)
   429	    out = []
   430	    for row in DB.list_items(conn, case_id, "entry"):
   431	        if not _code_check_gated(row):
   432	            continue
   433	        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
   434	        if not fails:
   435	            continue
   436	        f = fails[0]
   437	        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
   438	                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED"], "next_action": _fix_action(row, f)})
   439	    return out
   440	
   441	
   442	# ------------------------------------------------------------------ amounts
   443	def _amount_steps(cx, row):
   444	    R = set(row.get("state_reasons") or [])
   445	    lad = row.get("ladder") or {}
   446	    cc = lad.get("code_checks") or {}
   447	    rid = (row.get("record_ids") or [None])[0]
   448	    rec = cx.recs.get(rid, {})
   449	    kind = row["kind"]
   450	    vals = {"text": row["text"], "value_cents": row["value_cents"], "kind": kind, "classified_by": cc.get("classified_by")}
   451	    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
   452	    gfail = "GROUNDING_AMOUNT_NOT_IN_TEXT" in R or cc.get("amount_in_text") is False
   453	    st = []
   454	    if gfail:
   455	        st.append(step("found_in_text", "Dollar figure is in the record text", "code", FAIL, reason_text("GROUNDING_AMOUNT_NOT_IN_TEXT"), reason="GROUNDING_AMOUNT_NOT_IN_TEXT",
   456	                       rule="row 6", evidence={"excerpt": exc, "values": vals}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"])))
   457	        st.append(_skipped("amount_class", "Rule says what the figure is", "code", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
   458	    else:
   459	        st.append(step("found_in_text", "Dollar figure is in the record text", "code", PASS, "Code found this figure in the record by pattern; it is not a model's claim.",
   460	                       rule="row 6", evidence={"excerpt": exc, "values": vals}))
   461	        if kind == "charge":
   462	            st.append(step("amount_class", "Rule says what the figure is", "code", PASS,
   463	                           "A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it.", rule="row 7", evidence={"values": vals}))
   464	        elif kind == "unclear":
   465	            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
   466	                           evidence={"values": vals}, next_action=na("READ_RECORD", {"record_id": rid})))
   467	        else:
   468	            code = _AMOUNT_CODE[kind]
   469	            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
   470	    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
----
402:def _current_text(row):
403-    ed = row.get("edited") or {}
404-    return ed.get("summary", row.get("summary") or ""), ed.get("excerpt", row.get("excerpt") or "")
405-
406-
407-def _fix_action(row, stp) -> dict:
408-    """The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure)."""
409-    code, summ, exc = stp["reason_code"], *_current_text(row)
410-    target = {"item_id": row["id"]}
411-    tail = " The export stays blocked until it passes."
412-    if code == "SUMMARY_DROPS_QUALIFIER":
413-        terms = grounding.missing_qualifier_terms(summ, exc)
414-        what = ", ".join(f"\u2018{t}\u2019" for t in terms) if terms else "the quote's hedge, attribution, negation, side or approximation"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:19.152Z

**tool call — Bash**
````
{
 "command": "ls -d .venv 2>/dev/null && .venv/bin/python --version; echo ----; sed -n 1,40p tests/unit/test_review_rules.py | cut -c1-220; echo ----; grep -n \"batch\" app/backend/case_extras.py | grep -n \"add_routes\\|post\\|@app\" | head; grep -n \"@app.post\" app/backend/case_extras.py | head -20; echo ----; grep -n \"def _check\\b\" -A18 app/backend/case_extras.py | cut -c1-200 | head -30",
 "description": "Check venv, test helpers, and batch route definition"
}
````

### User / tool · 2026-11-02T05:12:19.296Z

**tool result**
````
.venv
Python 3.12.2
----
"""Review/edit rules (backend/review.py). R-RV-2 (D-010, D-012), R-RV-3, R-CH-5, R-CH-7, ADR-005 edit re-check order; fake judge only."""
import pytest
from app.backend import pipeline as PL, review as RV, export as X
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record

def seeded(tmp_path, case="sample"):
    """Seeds a case through the pipeline with a case-aware fake (extract returns the first sentence unit of the cited record)."""
    from tests.unit._fakes import sample_script, which_record as wr
    if case == "sample":
        call = FakeCall(sample_script())
    else:
        def extract(u):
            n = wr(u, case)[0]; ex = G.record(case, n)["excerpt"]
            return dict(summary=ex.split(". ")[0].rstrip(".") + ".", excerpt=ex.split(". ")[0].rstrip(".") + ".")
        call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / f"rv-{case}.sqlite")); cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), call=call, now=lambda: 1.0)
    return conn, cid, out

def ent(out, n):
    """Entry id citing record n (api.md: entries carry record_ids like 'r5')."""
    return [e for e in out["entries"] + out.get("undated_entries", []) if f"r{n}" in e["record_ids"]][0]["id"]
def amt(out, raw): return [a for a in out["amounts"] if a["raw"] == raw][0]["id"]
def judge(v): return FakeCall({"j1": {"verdict": v, "reason_code": "NONE"}})

@pytest.mark.parametrize("edits", [{"date": "2026-01-01"}, {"provider": "Someone Else"}, {"record": "r2"}, {"summary": "ok", "date": "2026-01-01"}])
def test_entry_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: editing an entry's date, provider or record -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

@pytest.mark.parametrize("edits", [{"evidence": "x"}, {"type": "causation"}, {"title": "New title"}])
def test_flag_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: flag evidence, type and title are not editable (only a note)."""
    conn, cid, out = seeded(tmp_path)
----
7:107:    @app.post("/api/cases/{token}/review/batch")
107:    @app.post("/api/cases/{token}/review/batch")
----
24:def _check(conn, case_id, ids, action):
25-    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
26-    bad = []
27-    for i in ids:
28-        try:
29-            kind, row = review._item(conn, case_id, i)
30-        except review.ReviewError:
31-            bad.append({"id": i, "reason": "not_found"})
32-            continue
33-        if kind != "entry":
34-            bad.append({"id": i, "reason": "not_an_entry"})
35-        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
36-            bad.append({"id": i, "reason": "date_unconfirmed"})
37-        elif action == "accept" and row["state"] != "verified":
38-            bad.append({"id": i, "reason": "not_verified"})
39-        elif action == "accept" and row["review_status"] != "pending":
40-            bad.append({"id": i, "reason": "not_pending"})
41-    return bad
42-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:21.348Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -20; echo ----; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k \"edit or manual or d047 or d034\" 2>&1 | tail -15",
 "description": "Confirm HEAD sha, working tree state, and run the brief's pytest selection",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:12:28.794Z

**tool result**
````
f5ddec825e5287124d268ddf16d06a299b957fda
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/billing.py
D  app/backend/calibration_route.py
 M app/backend/flags.py
----
........................................................................ [ 69%]
...............................                                          [100%]
103 passed, 1732 deselected in 6.89s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:31.437Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && echo ---- && git merge-base --is-ancestor 24c18a7 HEAD && echo \"24c18a7 is ancestor of HEAD\" ; echo ----; git diff --stat 24c18a7 HEAD -- app/backend/review.py app/backend/trace.py tests/unit/test_review_rules.py tests/unit/test_trace.py memory/contracts/api.md | tail -8; echo ----; git diff --stat 24c18a7 HEAD | tail -3",
 "description": "Check HEAD movement and whether card commit is an ancestor"
}
````

### User / tool · 2026-11-02T05:12:31.596Z

**tool result**
````
f5ddec8 fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
24c18a7 feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
e7a1987 fix(backend): language routing fails safe (D-048): English only when confidently English, mixed lines run the union of checks, Spanish cue words, 206-line routing set (T-085 r3)
21b6665 fix(frontend): AI-check summary and Why dialog read the gate and trace; failing edited wording is a named blocker with an Edit action; 422 edit reason inline (T-097 r2)
950d4a5 fix(backend): OCR_DERIVED survives edits; OCR render pixel caps and scrubbed tesseract env; hidden-text differential render, fail-closed scan, deadline that stops the worker (T-086 r2, T-087 r2)
db08276 fix(backend): billing lists every amount-bearing row or marks the provider incomplete; pins the prose charge gate (T-083 r3)
----
24c18a7 is ancestor of HEAD
----
----
 tests/e2e/conftest.py         |  2 +-
 tests/e2e/test_rerun_judge.py | 12 +++++-------
 5 files changed, 15 insertions(+), 41 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:35.226Z

**tool call — Bash**
````
{
 "command": "git show --stat f5ddec8 | tail -12; echo ----; git diff 24c18a7 HEAD --stat -- app/backend tests/unit memory/contracts; echo \"backend/unit diff exit: $?\"; echo ----; git diff 24c18a7 HEAD -- app/backend/review.py | head -5; echo ---; git show 24c18a7:app/backend/review.py | grep -n \"self_report\\|reports\" | head; echo ----; git show 24c18a7:tests/e2e/test_edit.py 2>/dev/null | grep -n \"confirm_warnings\\|409\\|needs_confirm\" | head; git grep -n \"confirm_warnings\\|needs_confirm\\|keep_my\\|keep-my\" 24c18a7 -- tests/e2e | head",
 "description": "Inspect the follow-up commit and e2e references at card commit"
}
````

### User / tool · 2026-11-02T05:12:35.471Z

**tool result**
````
Date:   Sun Nov 1 23:10:53 2026 -0600

    fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/manual.js        | 20 +++++---------------
 app/frontend/review.css       |  3 +--
 app/frontend/review.js        | 19 +++----------------
 tests/e2e/conftest.py         |  2 +-
 tests/e2e/test_rerun_judge.py | 12 +++++-------
 5 files changed, 15 insertions(+), 41 deletions(-)
----
backend/unit diff exit: 0
----
---
119:_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "an attribution phrase (such as complained of or reports)", "negation": "a negation (such as no, not or denies)",
----
19:    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
24c18a7:tests/e2e/test_edit.py:19:    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
24c18a7:tests/e2e/test_rerun_judge.py:240:    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}, "confirm_warnings": True})
24c18a7:tests/e2e/test_rerun_judge.py:269:        st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}, "confirm_warnings": True})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:40.626Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; mkdir -p \"$S/t100-card\" && git archive 24c18a7 | tar -x -C \"$S/t100-card\" && ls \"$S/t100-card\" | head -30 && ls \"$S/t100-card/tests/unit\" | wc -l; ls -la \"$S/t100-card/app/llm/\" | head -5; git -C /Users/arsis/zlayt-pm-project status --short -- app/llm evals/golden | head -3",
 "description": "Extract the card commit into a scratchpad copy via git archive"
}
````

### User / tool · 2026-11-02T05:12:41.079Z

**tool result**
````
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
      72
total 256
drwxr-xr-x@ 11 arsis  wheel    352 Nov  1 23:09 .
drwxr-xr-x@ 10 arsis  wheel    320 Nov  1 23:09 ..
-rw-r--r--@  1 arsis  wheel      0 Nov  1 23:09 __init__.py
-rw-r--r--@  1 arsis  wheel   5704 Nov  1 23:09 _types.py
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
?? app/llm/prompts/judge_conflict_v4.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:48.054Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/runner && cat > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/runner/run_pytest.py <<'EOF'\nimport os, sys\nROOT = sys.argv[1]\nargs = sys.argv[2:]\nos.chdir(ROOT)\nsys.path.append(ROOT)          # appended, never prepended: stdlib names cannot be shadowed by the archive\nimport pytest\nraise SystemExit(pytest.main(args))\nEOF\ncd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$PWD/t100-card\" -q -p no:cacheprovider tests/unit -k \"edit or manual or d047 or d034\" 2>&1 | tail -15",
 "description": "Run the brief's pytest selection against the card-commit archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:12:48.174Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/runner/run_pytest.py", line 4, in <module>
    os.chdir(ROOT)
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/t100-card'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:50.772Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$B/scratchpad/t100-card\" -q -p no:cacheprovider tests/unit -k \"edit or manual or d047 or d034\" 2>&1 | tail -15",
 "description": "Run the brief's pytest selection against the card-commit archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:12:58.189Z

**tool result**
````
........................................................................ [ 69%]
...............................                                          [100%]
103 passed, 1715 deselected in 6.91s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:13:00.596Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$B/scratchpad/t100-card\" -q -p no:cacheprovider tests/unit 2>&1 | tail -4",
 "description": "Run full unit suite against the card-commit archive copy",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:13:57.765Z

**tool result**
````
........................................................................ [ 95%]
........................................................................ [ 99%]
..................                                                       [100%]
1814 passed, 4 skipped in 55.86s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:14:01.140Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$B/scratchpad/t100-card\" -q -p no:cacheprovider tests/unit -rs 2>&1 | grep -i \"skip\" | tail -8; echo ----; cd /Users/arsis/zlayt-pm-project && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -rs 2>&1 | tail -4",
 "description": "List skipped tests and run full suite in the working tree for comparison",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:15:50.846Z

**tool result**
````
SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)
SKIPPED [1] tests/unit/test_eval_runner.py:661: no git repository here
SKIPPED [1] tests/unit/test_spanish_failsafe.py:223: live judge eval: run with SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1 LLM_BACKEND=claude-cli (about 55 model calls)
1814 passed, 4 skipped in 52.31s
----
tests/unit/test_eval_runner.py:683: AssertionError
=========================== short test summary info ============================
SKIPPED [1] tests/unit/test_spanish_failsafe.py:223: live judge eval: run with SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1 LLM_BACKEND=claude-cli (about 55 model calls)
2 failed, 1832 passed, 1 skipped in 55.25s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:15:57.669Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | grep -E \"^FAILED|failed|passed\" | tail -4; echo ----; B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$B/scratchpad/t100-card\" -q -p no:cacheprovider tests/unit/test_review_rules.py tests/unit/test_manual_and_split.py tests/unit/test_api_routes.py tests/unit/test_trace.py tests/unit/test_export.py tests/unit/test_ocr_invariant.py 2>&1 | tail -2",
 "description": "Identify failing tests in working tree and count changed-file tests on archive",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:17:04.758Z

**tool result**
````
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 1832 passed, 1 skipped in 52.93s
----
..................................................                       [100%]
194 passed in 12.50s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:11.116Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && for m in tok qual gate; do rm -rf scratchpad/mut-$m; cp -R scratchpad/t100-card scratchpad/mut-$m; done && cat > runner/mutate.py <<'EOF'\nimport sys\npath, old, new = sys.argv[1], sys.argv[2], sys.argv[3]\nsrc = open(path, encoding=\"utf-8\").read()\nn = src.count(old)\nassert n == 1, f\"expected exactly one match, found {n}\"\nopen(path, \"w\", encoding=\"utf-8\").write(src.replace(old, new))\nprint(\"mutated\", path)\nEOF\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python; S=$B/scratchpad\nPYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-tok/app/backend/review.py \"    if toks:\n        words\" \"    if False and toks:\n        words\" && PYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-qual/app/backend/review.py \"    if dropped:\n        what\" \"    if False and dropped:\n        what\" && PYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-gate/app/backend/trace.py \"def code_check_blockers(conn, case_id: str, cx=None) -> list:\n    \\\"\\\"\\\"Export blockers (D-045(b))\" \"def code_check_blockers(conn, case_id: str, cx=None) -> list:\n    return []\n    \\\"\\\"\\\"Export blockers (D-045(b))\" && diff -u $S/t100-card/app/backend/review.py $S/mut-tok/app/backend/review.py | head -20",
 "description": "Create three scratch mutants of the card commit (token, qualifier, gate)"
}
````

### User / tool · 2026-11-02T05:17:11.200Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion (scratchpad/mut-$m) is blocked | command: B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf807
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:15.142Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; cd $B && cp -R scratchpad/t100-card scratchpad/mut-tok && cp -R scratchpad/t100-card scratchpad/mut-qual && cp -R scratchpad/t100-card scratchpad/mut-gate && ls scratchpad && cat > runner/mutate.py <<'EOF'\nimport sys\npath, old, new = sys.argv[1], sys.argv[2], sys.argv[3]\nsrc = open(path, encoding=\"utf-8\").read()\nn = src.count(old)\nassert n == 1, f\"expected exactly one match, found {n}\"\nopen(path, \"w\", encoding=\"utf-8\").write(src.replace(old, new))\nprint(\"mutated\", path)\nEOF\necho written",
 "description": "Copy the card archive into three scratch mutant directories"
}
````

### User / tool · 2026-11-02T05:17:17.099Z

**tool result**
````
T-047-run1.json
a.sqlite3
a27e3a4.diff
adr013.txt
api
api2
api_at_099732b.py
api_head.log
api_head.py
api_head.sqlite3
api_md_head.md
api_md_new.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app.log
app.pid
app.sqlite3
app2.log
arch
arch_57a08ba
audit.py
base
billing.orig
blank.py
boom_final.py
boom_server.py
build_set.py
build_set.py.bak
build_t099_blobs.py
c
c8a9874
ca.sh
cal.bak
cases.txt
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
chk.py
chk_mut.py
cli1.err
cli1.out
cli1.txt
cli2.err
cli2.out
cli2.txt
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
collapsed.png
commitcases.txt
copy
copy_untracked.py
corpus.py
cr.sh
cred_b05.py
cred_orig.py
cs.sh
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
dbg.png
dbg.py
dbg97.py
de1.txt
demo
demo.log
diag.py
dl
dos
drive.py
e1.py
e1400d4
e2.py
env97
es1.txt
ev.json
ev.sh
evalout
evalout2
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
final-data
first.png
fr_r2.txt
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.log
full.patch
fxbak
gen_controls.py
guardprobe.py
guardprobe.py.bak
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head2.py
head_950d4a5
head_9c1af01
head_clean
head_clean.log
head_clean.sqlite3
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
heldout.py
hookcopy
ing.bak
ingest.orig
jcheck.py
judge_live.py
judges.png
leak.py
lib_app.sqlite
link
live-demo
live-demo.log
live-local
live-local.log
local
local.log
m1
m2
m3
m4
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
mine.diff
mine.patch
mine.txt
miss.py
mk.py
mkd.py
mkfix.py
mkpdf.py
mkreview.py
mkreviews.py
msg.txt
mut
mut-A
mut-B
mut-C
mut-D
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut2
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_dedupe
mut_flagsdeadline
mut_rmfixture
mut_rmjudgefixture
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutate.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
narr.py
neg
neg2
nucc
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old
out
overlay-head
p.py
p2.py
p3.py
p_be
p_fe
pa
page.txt
parent
parent-server.log
parent.sqlite3
pathspec.txt
pdf_time.py
pdfs
pdfs_head
pid
pid2
pin-8bc7f90
pin-db08276
pin-f218263
pl.bak
pre_t095_schema.sql
probe
probe.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_failed.py
probe_head
probe_head_out.txt
probe_nojudge.py
probe_rej.py
probe_run.py
probe_t067.py
probe_timeout.py
probe_work_head
probe_work_head2
probes
pub.log
pub2.log
r2
r2-cases.out
r2.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2d.sqlite3
r2demo
r2demo.log
r2local
r2local.log
r2o
r2src
r3
r3-a27
r3-parent
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3copy
r3probe.py
r3run
r3scripts
r3src
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4probe_on_0f58181.txt
rail.png
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_sample.log
recon.py
replay.py
repo
repro_stale
req_mut.md
rerec.log
rerec.sh
review_headplus.py
run.base.py
run.head.py
run.try.py
run_mutants_r3.py
run_ro.py
run_t070_orig.py
scan.py
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
selfcheck-r2.txt
server.log
server.pid
server2.log
server7867.log
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap2
snap3
src
srv.KdvV
srv.log
srv.out
srvdir
strip.py
sync.py
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t093.base.py
t095.patch
t095r2_head
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099.index
t099_msg.txt
t1.xXug
t100-card
t2.q4VB
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tail.md
tests_b05.py
tmpindex
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
ub
ui-demo
ui-local
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux3
v
view.json
walk.py
walk2.py
wprobe.py
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
xc.py
xss.py
written
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:23.838Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; mkdir -p $S/t100-fresh && cd /Users/arsis/zlayt-pm-project && git archive 24c18a7 | tar -x -C $S/t100-fresh && diff -rq $S/t100-fresh $S/t100-card && echo \"t100-card identical to fresh 24c18a7 archive\"; cd $B && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; PYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-tok/app/backend/review.py \"    if toks:\n        words\" \"    if False and toks:\n        words\" && PYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-qual/app/backend/review.py \"    if dropped:\n        what\" \"    if False and dropped:\n        what\" && PYTHONDONTWRITEBYTECODE=1 $PY -I runner/mutate.py $S/mut-gate/app/backend/trace.py \"def code_check_blockers(conn, case_id: str, cx=None) -> list:\n    \\\"\\\"\\\"Export blockers (D-045(b))\" \"def code_check_blockers(conn, case_id: str, cx=None) -> list:\n    return []\n    \\\"\\\"\\\"Export blockers (D-045(b))\"; diff $S/t100-card/app/backend/review.py $S/mut-tok/app/backend/review.py; diff $S/t100-card/app/backend/review.py $S/mut-qual/app/backend/review.py; diff $S/t100-card/app/backend/trace.py $S/mut-gate/app/backend/trace.py",
 "description": "Verify scratch archive matches commit and apply three exact-string mutations"
}
````

### User / tool · 2026-11-02T05:17:24.457Z

**tool result**
````
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/app: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/app/backend: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/app/db: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/app/llm: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/app/llm/backends: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/evals: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/research: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/tests: __pycache__
Only in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card/tests/unit: __pycache__
mutated /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut-tok/app/backend/review.py
mutated /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut-qual/app/backend/review.py
mutated /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut-gate/app/backend/trace.py
136c136
<     if toks:
---
>     if False and toks:
140c140
<     if dropped:
---
>     if False and dropped:
425a426
>     return []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:29.646Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cd $B && for m in tok qual gate; do echo \"=== mutant: $m\"; PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I runner/run_pytest.py \"$S/mut-$m\" -q -p no:cacheprovider tests/unit 2>&1 | grep -E \"^FAILED|passed|failed\" | sed 's/ - .*//' | head -40; done",
 "description": "Run full unit suite against each of the three mutants",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:20:13.422Z

**tool result**
````
=== mutant: tok
FAILED tests/unit/test_api_routes.py::test_side_or_negation_edit_is_a_422_with_plain_reason_and_confirm_flag_changes_nothing_d047
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[No pain, improving.-False]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[No pain, improving.-True]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Left-sided pain, improving.-False]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Left-sided pain, improving.-True]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Pain improving without medication.-False]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Pain improving without medication.-True]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Pain not improving.-False]
FAILED tests/unit/test_manual_and_split.py::test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047[Pain not improving.-True]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10, improving; no radiating symptoms.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-False]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10, improving; no radiating symptoms.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-True]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10, improving; not in distress.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-False]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10, improving; not in distress.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-True]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10 improving without medication.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-False]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: pain 4/10 improving without medication.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-True]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: left-sided pain 4/10, improving.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-False]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: left-sided pain 4/10, improving.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-True]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: right shoulder pain 4/10, improving.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-False]
FAILED tests/unit/test_review_rules.py::test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047[Visit 8: right shoulder pain 4/10, improving.-SUMMARY_TOKEN_NOT_IN_EXCERPT-tokens-True]
FAILED tests/unit/test_review_rules.py::test_judge_is_not_called_when_a_code_check_fails_d047
20 failed, 1794 passed, 4 skipped in 52.59s
=== mutant: qual
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=cab0f28e5538b step=j1 attempt=1 prompt_hash=52614d4ce981c69b903da75470c2f4ebb0cc2e05102855d25872d0155a4c2458
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c256309ce014a step=j1 attempt=1 prompt_hash=52614d4ce981c69b903da75470c2f4ebb0cc2e05102855d25872d0155a4c2458
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=ca17e00aa3654 step=j1 attempt=1 prompt_hash=52614d4ce981c69b903da75470c2f4ebb0cc2e05102855d25872d0155a4c2458
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c19efa7987b64 step=j1 attempt=1 prompt_hash=52614d4ce981c69b903da75470c2f4ebb0cc2e05102855d25872d0155a4c2458
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c7daf8240bdb4 step=j1 attempt=1 prompt_hash=52614d4ce981c69b903da75470c2f4ebb0cc2e05102855d25872d0155a4c2458
FAILED tests/unit/test_review_rules.py::test_dropping_a_qualifier_of_the_quote_is_a_hard_422_d047
FAILED tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098
FAILED tests/unit/test_trace.py::test_item_trace_shows_the_failing_code_step_with_the_next_action_t098
FAILED tests/unit/test_trace.py::test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098
FAILED tests/unit/test_trace.py::test_dismissing_the_failing_edited_item_clears_the_blocker_t098
FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_with_a_failing_edit_t098
6 failed, 1808 passed, 4 skipped in 53.73s
=== mutant: gate
        for name in ("failing edit", "failing edit and run failed"):
            if name.endswith("run failed"):
                DB.update_case(conn, tok, status="failed")
FAILED tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098
FAILED tests/unit/test_trace.py::test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098
FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_with_a_failing_edit_t098
3 failed, 1811 passed, 4 skipped in 53.68s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:28.696Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; mkdir -p $S/probes-t100 && cat > $S/probes-t100/probe_gap.py <<'EOF'\n\"\"\"Scratch probe (not committed): does the route store negation/side words D-047 is about, and does the export gate catch them?\nRun from a copy of the card commit with its tests/ tree on the path.\"\"\"\nimport sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nfrom tests.unit.test_review_rules import seeded, ent, judge\nfrom app.backend import review as RV, trace\nfrom app.db import db as DB\n\nCASES = [\n    \"Visit 8: pain 4/10, improving; denies radiating symptoms.\",\n    \"Visit 8: pain 4/10, never worse.\",\n    \"Visit 8: pain 4/10, none reported.\",\n    \"Visit 8: bilateral pain 4/10, improving.\",\n    \"Visit 8: negative for distress; pain 4/10, improving.\",\n    \"Visit 8: pain 4/10, improving; absent distress.\",\n    \"Visit 8: pain 4/10, improving; neither worse nor better.\",\n]\nfor mode in (\"judge_unavailable\", \"judge_supported\"):\n    for summ in CASES:\n        d = pathlib.Path(tempfile.mkdtemp(dir=ROOT + \"/../probe-db\"))\n        conn, cid, out = seeded(d)\n        eid = ent(out, 5)\n        call = None if mode == \"judge_unavailable\" else judge(\"supported\")\n        try:\n            r = RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=summ)), call=call)\n            item = DB.get_item(conn, eid, cid)\n            blockers = trace.export_blockers(conn, cid)\n            print(f\"[{mode}] SAVED  state={item['state']} reasons={item['state_reasons']} warnings={[w['code'] for w in r['warnings']]} \"\n                  f\"gate_blockers={[b['reason_code'] for b in blockers if b['item_id']==eid]} | {summ}\")\n        except RV.ReviewError as e:\n            print(f\"[{mode}] {e.status} {e.code} reason={e.detail.get('reason')} | {summ}\")\nEOF\nmkdir -p $S/probe-db && cd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_gap.py').read())\n\" 2>&1 | grep -v WARNING | tail -40",
 "description": "Probe which negation and side words the card-commit route stores and whether the gate blocks them",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:20:29.915Z

**tool result**
````
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; denies radiating symptoms.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, never worse.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, none reported.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: bilateral pain 4/10, improving.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: negative for distress; pain 4/10, improving.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; absent distress.
[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; neither worse nor better.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; denies radiating symptoms.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, never worse.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, none reported.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: bilateral pain 4/10, improving.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: negative for distress; pain 4/10, improving.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; absent distress.
[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; neither worse nor better.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:42.055Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cd $B && cat > $S/probes-t100/probe_gate_alone.py <<'EOF'\nimport sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nfrom tests.unit.test_review_rules import seeded, ent, judge\nfrom app.backend import review as RV, trace, export as X, store\nfrom app.db import db as DB\nd = pathlib.Path(tempfile.mkdtemp(dir=ROOT + \"/../probe-db\"))\nconn, cid, out = seeded(d)\neid = ent(out, 5)\n# route with the token check disabled (mutant): does the gate catch the stored edit on its own?\nr = RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=\"Visit 8: left-sided pain 4/10, improving.\")), call=judge(\"supported\"))\nRV.apply_review(conn, cid, eid, dict(action=\"accept\"))\nit = DB.get_item(conn, eid, cid)\nprint(\"stored state:\", it[\"state\"], it[\"state_reasons\"], \"| review:\", it[\"review_status\"], \"| summary:\", it[\"edited\"][\"summary\"])\nprint(\"gate blockers for item:\", [b[\"reason_code\"] for b in trace.export_blockers(conn, cid) if b[\"item_id\"] == eid])\ntry:\n    X.build_export(store.export_case(conn, cid))\n    print(\"export built: summary 'left-sided' in letter/notes:\", \"left-sided\" in str(X.build_export(store.export_case(conn, cid))))\nexcept Exception as e:\n    print(\"export refused:\", type(e).__name__, getattr(e, \"items\", None) or str(e)[:120])\nEOF\nPYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/mut-tok'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_gate_alone.py').read())\n\" 2>&1 | grep -v WARNING | tail -12",
 "description": "Probe whether the export gate blocks a stored side-word edit without the route check",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:20:42.662Z

**tool result**
````
stored state: verified [] | review: accepted | summary: Visit 8: left-sided pain 4/10, improving.
gate blockers for item: []
export built: summary 'left-sided' in letter/notes: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:48.037Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; sed -n 1,60p $S/t100-card/tests/unit/test_api_routes.py | cut -c1-220; echo ----; sed -n 100,120p $S/t100-card/app/backend/case_extras.py | cut -c1-200",
 "description": "Read API test fixture and batch route definition in the card copy"
}
````

### User / tool · 2026-11-02T05:20:48.133Z

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
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


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
----
        config.pop("export", None)
    else:
        config["export"] = cfg
    DB.update_case(conn, case_id, config_json=config or None)


def add_routes(app, *, conn, get_case, body_of, ApiError, now):
    @app.post("/api/cases/{token}/review/batch")
    async def review_batch(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply_batch(c, token, b, now())
            except ValueError:
                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
            except BatchRefused as e:
                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:02.049Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cat > $S/probes-t100/probe_http.py <<'EOF'\n\"\"\"Scratch HTTP probe against the card-commit copy (not committed). Argument 1: copy root.\"\"\"\nimport os, sys, tempfile, pathlib, json\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\"):\n    os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit.test_api_routes import run_case\nd = tempfile.mkdtemp(dir=ROOT + \"/../probe-db\")\ndbp = str(pathlib.Path(d) / \"api.sqlite\")\nc = TestClient(create_app(dbp, static_dir=d), client=(\"127.0.0.1\", 50000))\ntok = run_case(c)\nents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\ne5 = [e for e in ents if e[\"provider\"].startswith(\"Capital PT, visit 8\")][0]\nbefore = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\ndef show(label, r):\n    j = r.json()\n    err = j.get(\"error\")\n    print(f\"{label}: HTTP {r.status_code} code={err['code'] if err else 'ok'} reason={(err or {}).get('detail', {}).get('reason')} msg={(err or {}).get('message')!r}\")\nurl = f\"/api/cases/{tok}/items/{e5['id']}/review\"\nL = \"Visit 8: left-sided pain 4/10, improving; no missed work.\"\nfor label, body in [\n    (\"edit plain\", {\"action\": \"edit\", \"edits\": {\"summary\": L}}),\n    (\"edit confirm_warnings\", {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"confirm_warnings\": True}),\n    (\"edit force\", {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"force\": True}),\n    (\"edit override+keep_my_wording+confirm\", {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"override\": True, \"keep_my_wording\": True, \"confirm\": True}),\n    (\"edit confirm_warnings str 'true'\", {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"confirm_warnings\": \"true\"}),\n    (\"accept carrying edits payload\", {\"action\": \"accept\", \"edits\": {\"summary\": L}}),\n]:\n    show(label, c.post(url, json=body))\nshow(\"batch action=edit\", c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"edit\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}, \"confirm_warnings\": True}))\nshow(\"batch action=accept\", c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}, \"force\": True}))\nafter = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\nprint(\"entries unchanged after every refused route:\", before == after or [x for x in after if x[\"id\"] == e5[\"id\"]][0].get(\"summary\") == e5[\"summary\"] and [x for x in after if x[\"id\"] == e5[\"id\"]][0].get(\"review_status\") == e5.get(\"review_status\"))\nprint(\"e5 review_status now:\", [x for x in after if x[\"id\"] == e5[\"id\"]][0][\"review_status\"], \"| summary now:\", [x for x in after if x[\"id\"] == e5[\"id\"]][0][\"summary\"][:70])\n# 422 reasons for every D-047 class\nfor label, s in [\n    (\"number\", \"Visit 8: pain 9/10, improving.\"),\n    (\"side\", \"Visit 8: right-sided pain 4/10, improving.\"),\n    (\"negation\", \"Visit 8: pain 4/10, not improving.\"),\n    (\"qualifier drop\", \"Cervical MRI: no; pain 4/10, improving.\"),\n]:\n    show(f\"edit {label}\", c.post(url, json={\"action\": \"edit\", \"edits\": {\"summary\": s}, \"confirm_warnings\": True}))\n# manual entry: make record 5 rejected so the route accepts a manual entry\nconn = DB.connect(dbp)\nrec5 = [r for r in DB.list_items(conn, tok, \"entry\") if r[\"id\"] == e5[\"id\"]][0]\nconn.execute(\"UPDATE entries SET state='rejected' WHERE id=? AND case_id=?\", (e5[\"id\"], tok)); conn.commit()\nrid = e5[\"record_ids\"][0]\nq = \"Pain 4/10, improving.\"\nmu = f\"/api/cases/{tok}/records/{rid}/entry\"\nshow(\"manual side+confirm\", c.post(mu, json={\"summary\": \"Left-sided pain 4/10, improving.\", \"excerpt\": q, \"confirm_warnings\": True}))\nshow(\"manual negation+force\", c.post(mu, json={\"summary\": \"Pain 4/10, not improving.\", \"excerpt\": q, \"force\": True}))\nshow(\"manual number+confirm\", c.post(mu, json={\"summary\": \"Pain 9/10, improving.\", \"excerpt\": q, \"confirm_warnings\": True}))\nEOF\ncd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_http.py').read())\n\" 2>&1 | grep -v \"WARNING\\|INFO\" | tail -40",
 "description": "Probe edit, batch and manual routes over HTTP on the card-commit copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:21:03.054Z

**tool result**
````
edit plain: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
edit confirm_warnings: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
edit force: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
edit override+keep_my_wording+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
edit confirm_warnings str 'true': HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
accept carrying edits payload: HTTP 200 code=ok reason=None msg=None
batch action=edit: HTTP 400 code=bad_request reason=None msg='Send an action (accept or reset) and a list of entry ids.'
batch action=accept: HTTP 422 code=invalid_batch reason=None msg='Only verified entries can be accepted together; nothing was changed.'
entries unchanged after every refused route: False
e5 review_status now: accepted | summary now: Pain 4/10, improving. Patient reports missing 3 days of work.
edit number: HTTP 422 code=invalid_edit reason=SUMMARY_NUMBER_NOT_IN_EXCERPT msg='The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote.'
edit side: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “right”, which the quote does not say. Remove it or change the quote.'
edit negation: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “not”, which the quote does not say. Remove it or change the quote.'
edit qualifier drop: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “no”, which the quote does not say. Remove it or change the quote.'
manual side+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, which the quote does not say. Remove it or change the quote.'
manual negation+force: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “not”, which the quote does not say. Remove it or change the quote.'
manual number+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_NUMBER_NOT_IN_EXCERPT msg='The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote.'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:11.737Z

**tool call — Bash**
````
{
 "command": "git show 24c18a7:tests/e2e/test_edit.py | sed -n 1,40p | cut -c1-240; echo ----; git show 24c18a7:tests/e2e/test_rerun_judge.py | sed -n 230,275p | cut -c1-240",
 "description": "Read the e2e edit tests at the card commit that still send confirm_warnings"
}
````

### User / tool · 2026-11-02T05:21:11.876Z

**tool result**
````
"""Edit flow. R-RV-2, R-RV-3, R-EX-4(10)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_edit_summary_labelled_and_persists(page, sample_case):
    """R-RV-2: edit entry 3 summary -> 'edited' label; reload keeps summary and label; letter has no 'edited'."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 and daily headaches."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    page.reload(); page.get_by_test_id("timeline").wait_for()
    e = page.get_by_test_id("entry-3"); assert e.get_attribute("data-review") == "edited" and "edited" in e.inner_text().lower() and "daily headaches" in e.get_by_test_id("entry-summary").inner_text()

def test_added_dollar_is_a_hard_422_no_override(page, sample_case):
    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
    c = api("GET", f"/api/cases/{sample_case}")[1]; eid = [e for e in c["entries"] if "r5" in e["record_ids"]][0]["id"]
    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
    assert st == 422
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Visit 8: pain 4/10, improving; billed $9,000."); e.get_by_test_id("btn-save-edit").click()
    expect(page.get_by_role("alert").or_(page.get_by_test_id("warning-list")).first).to_contain_text("9000")
    assert e.get_attribute("data-review") != "edited" and page.get_by_test_id("btn-keep-wording").count() == 0

def test_date_and_provider_not_editable(page, sample_case):
    """R-RV-2: no input exists for date or provider."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    assert e.locator("input[name=date], input[name=provider]").count() == 0

def test_notes_list_edited_item_with_both_texts(page, sample_case):
    """R-EX-4(10): after editing entry 3 and exporting, EDITED ITEMS holds the exact original and new sentences; the letter has no 'edited'."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3")
    original = "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks."; new = "Persistent neck pain 6/10 with daily headaches noted."
    e.get_by_test_id("btn-edit").click(); e.get_by_test_id("edit-summary").fill(new); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited"); expect(e.get_by_test_id("entry-summary")).to_contain_text("daily headaches noted")
    e.get_by_test_id("btn-accept").click(); page.get_by_test_id("btn-export").click()
    sec = page.get_by_test_id("export-notes").inner_text().split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
    assert original in sec and new in sec and "edited" not in page.get_by_test_id("export-letter").inner_text().lower()

----
        assert jp.get_by_test_id("judge-unresolved").count() == 3 and "blocks export" in jp.get_by_test_id("judge-summary-counts").inner_text()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_judge_panel_follows_the_gate_for_an_edited_item(page, sample_case):
    """D-045(b): the gate lists only the accepted AI-made items; the edited one is ready, so the panel must not say it blocks and must not offer a rerun for it."""
    ids = _accept(sample_case, 3)
    c = api("GET", f"/api/cases/{sample_case}")[1]
    edited = next(e for e in c["entries"] if e["state"] != "rejected" and e["date"] and e["id"] not in ids)
    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}, "confirm_warnings": True})
    assert st == 200
    JudgeNotRun(page, sample_case, ids, exempt=[edited["id"]])
    open_case(page, sample_case); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert summ.count("blocks export") == 1 and "blocks export: 3" in summ, "the summary counts the gate's 3 blockers, not the edited item"
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{edited["id"]}"]')
    expect(row).to_have_count(1)
    t = row.inner_text()
    assert "Edited by you, not AI-checked" in t and "Blocks the export" not in t and "can't go in the letter" not in t
    assert row.get_by_test_id("btn-rerun-judge").count() == 0
    assert jp.get_by_test_id("judge-rerun-group").inner_text().count("these 3") == 1
    blocked_rows = jp.locator('[data-testid="judge-unresolved"]:has-text("Blocks the export")')
    assert blocked_rows.count() == 3


# ---- T-097 round 2 (D-045 b, T-098): the summary and the Why dialog read the gate and the item trace; a failing code check on an edited summary is a named blocker
DROPS = "C5-C6 disc protrusion with foraminal narrowing."   # drops 'mild', 'right', 'may represent', 'correlate clinically' from the quote (code check summary_qualifier)
WORDING = "Your wording doesn't match the quote:"


def _entry_with(tok, text):
    c = api("GET", f"/api/cases/{tok}")[1]
    return next(e for e in c["entries"] if text in e["excerpt"] and e["date"])


def _edit(tok, i, summary):
    st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
    if st == 409:   # pre-D-047 server: the 'keep my wording' confirm; once T-100 lands this branch is never taken
        st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}, "confirm_warnings": True})
    assert st == 200, r
    return r


@pytest.fixture
def mixed(page, sample_case):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:19.545Z

**tool call — Bash**
````
{
 "command": "git show f5ddec8 -- tests/e2e/test_rerun_judge.py tests/e2e/conftest.py | cut -c1-260 | head -70; echo ----; git show 24c18a7:tests/e2e/test_rerun_judge.py | grep -n \"def _edit\" -A6 | cut -c1-200",
 "description": "Show the e2e repair in the follow-up commit and the card-commit helper"
}
````

### User / tool · 2026-11-02T05:21:19.664Z

**tool result**
````
commit f5ddec825e5287124d268ddf16d06a299b957fda
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:10:53 2026 -0600

    fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/conftest.py b/tests/e2e/conftest.py
index 9e56630..56654f0 100644
--- a/tests/e2e/conftest.py
+++ b/tests/e2e/conftest.py
@@ -26,7 +26,7 @@ T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit
   (an edited item is 'Edited by you, not AI-checked', no rerun).
 T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the ite
   item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes s
-  The 409 'keep my wording' confirm (btn-keep-wording, warning-list, btn-cancel-confirm) is dead under D-047: a refused edit is a 422 shown in the rv-error line under the edit box.
+  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
 T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equa
 Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
 """
diff --git a/tests/e2e/test_rerun_judge.py b/tests/e2e/test_rerun_judge.py
index c68061c..dada312 100644
--- a/tests/e2e/test_rerun_judge.py
+++ b/tests/e2e/test_rerun_judge.py
@@ -237,7 +237,7 @@ def test_judge_panel_follows_the_gate_for_an_edited_item(page, sample_case):
     ids = _accept(sample_case, 3)
     c = api("GET", f"/api/cases/{sample_case}")[1]
     edited = next(e for e in c["entries"] if e["state"] != "rejected" and e["date"] and e["id"] not in ids)
-    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}, "confirm_warnings": True})
+    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}})
     assert st == 200
     JudgeNotRun(page, sample_case, ids, exempt=[edited["id"]])
     open_case(page, sample_case); jp = open_judges(page)
@@ -265,8 +265,6 @@ def _entry_with(tok, text):
 
 def _edit(tok, i, summary):
     st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
-    if st == 409:   # pre-D-047 server: the 'keep my wording' confirm; once T-100 lands this branch is never taken
-        st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}, "confirm_warnings": True})
     assert st == 200, r
     return r
 
@@ -353,12 +351,12 @@ def test_fixing_the_wording_clears_panel_dialog_and_rail(page, mixed):
     assert st.get_by_test_id("item-verdict").inner_text() == "Edited by you, not AI-checked" and st.get_by_test_id("item-wording-fail").count() == 0
 
 
-def test_refused_edit_shows_the_reason_inline_and_keeps_the_typed_text_no_confirm_dialog(page, sample_case):
-    """D-047: a number (or side/negation) that is not in the quote is a hard 422: the reason sits under the edit box, the text stays, there is no 'keep my wording' choice."""
+@pytest.mark.parametrize("typed,shown", [("Visit 8: pain 4/10, improving; billed $9,000.", "9000"), ("Pain 4/10, improving in the left arm.", "left")])
+def test_refused_edit_shows_the_reason_inline_and_keeps_the_typed_text_no_confirm_dialog(page, sample_case, typed, shown):
+    """D-047: a number, side or negation that is not in the quote is a hard 422: the reason sits under the edit box, the text stays, there is no 'keep my wording' choice."""
     open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
-    typed = "Visit 8: pain 4/10, improving; billed $9,000."
     e.get_by_test_id("edit-summary").fill(typed); e.get_by_test_id("btn-save-edit").click()
-    err = e.locator(".rv-error"); expect(err).to_contain_text("9000"); expect(err).to_contain_text("not in the quote")
+    err = e.locator(".rv-error"); expect(err).to_contain_text(shown); expect(err).to_contain_text("not in the quote")
     assert e.get_by_test_id("edit-summary").input_value() == typed and e.get_by_test_id("edit-summary").is_visible()
     assert e.get_attribute("data-review") != "edited"
     assert page.get_by_test_id("btn-keep-wording").count() == 0 and page.get_by_test_id("warning-list").count() == 0
----
266:def _edit(tok, i, summary):
267-    st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
268-    if st == 409:   # pre-D-047 server: the 'keep my wording' confirm; once T-100 lands this branch is never taken
269-        st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}, "confirm_warnings": True})
270-    assert st == 200, r
271-    return r
272-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:24.020Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/test_rerun_judge.py | grep -n \"DROPS\\|_edit(\\|def mixed\" -A0 | cut -c1-220 | head -30; echo ----; git show HEAD:tests/e2e/test_rerun_judge.py | sed -n 278,300p | cut -c1-260",
 "description": "Check whether the e2e mixed fixture at HEAD still asserts 200 on a refused edit"
}
````

### User / tool · 2026-11-02T05:21:24.176Z

**tool result**
````
261:def _edit(tok, i, summary):
268:def mixed(page, sample_case):
273:    _edit(sample_case, bad["id"], bad["summary"].rstrip(".") + " per the record.")
274:    _edit(sample_case, ok["id"], ok["summary"].rstrip(".") + " per the record.")
339:    _edit(t["tok"], t["bad"]["id"], t["bad"]["summary"].rstrip(".") + " as recorded.")   # any new wording ends the stub's failure, as a passing edit ends the real one
----

def test_failing_edit_is_a_named_blocker_in_the_panel_summary_and_row(page, mixed):
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert "1 edit does not match its quote, blocks export: 1" in summ
    assert "Export blocked by 1" in open_rail(page).get_by_test_id("case-summary-gate").inner_text(), "the rail and the panel summary agree"
    row = jp.locator(f'[data-testid="judge-wording"][data-target-item="{t["bad"]["id"]}"]')
    expect(row).to_have_count(1)
    txt = row.inner_text()
    assert WORDING in txt and "qualifier" in txt and "Blocks the export" in txt and "Edited by you, not AI-checked" not in txt
    assert "The export stays blocked until it passes" in txt, "the server's fix sentence is shown as the next step"
    assert jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["bad"]["id"]}"]').count() == 0, "one row per item"
    row.get_by_test_id("btn-judge-edit").click()
    ta = page.locator(f'[data-item-id="{t["bad"]["id"]}"]').first.get_by_test_id("edit-summary")
    expect(ta).to_be_visible(); assert active_in(page, f'[data-item-id="{t["bad"]["id"]}"]')


def test_passing_edit_says_edited_by_you_not_ai_checked_everywhere(page, mixed):
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["ok"]["id"]}"]')
    if row.count():   # the report lists the edited item as unchecked; the row follows the gate, which does not hold it
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:25.593Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/test_rerun_judge.py | sed -n 258,280p | cut -c1-260",
 "description": "Read the HEAD e2e mixed fixture that edits a dropped-qualifier summary"
}
````

### User / tool · 2026-11-02T05:21:25.693Z

**tool result**
````
WORDING = "Your wording doesn't match the quote:"


def _edit(tok, i, summary):
    st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
    assert st == 200, r
    return r


@pytest.fixture
def mixed(page, sample_case):
    """One accepted AI item; one edited summary the gate holds (stub: fails a code check); one edited summary that passes."""
    ids = _accept(sample_case, 1)
    pend = [e for e in api("GET", f"/api/cases/{sample_case}")[1]["entries"] if e["id"] not in ids and e["state"] != "rejected" and e["date"] and e["review_status"] == "pending"]
    bad, ok = pend[0], pend[1]
    _edit(sample_case, bad["id"], bad["summary"].rstrip(".") + " per the record.")
    _edit(sample_case, ok["id"], ok["summary"].rstrip(".") + " per the record.")
    stub = WordingFails(page, sample_case, [bad["id"]])
    return {"tok": sample_case, "bad": bad, "ok": ok, "accepted": ids[0], "stub": stub}


def test_failing_edit_is_a_named_blocker_in_the_panel_summary_and_row(page, mixed):
    t = mixed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:54.969Z

**tool call — Bash**
````
{
 "command": "git show 24c18a7:tests/unit/test_review_rules.py > /dev/null; B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-card; grep -rn \"partially\" $B/tests/unit/test_review_rules.py $B/tests/unit/test_manual_and_split.py $B/tests/unit/test_api_routes.py | cut -c1-160 | head; echo ----; grep -n \"def to_ladder\" -A8 $B/app/backend/judges.py | cut -c1-180; echo ----; grep -n \"def compose_state\" -A14 $B/app/backend/confidence.py | cut -c1-200 | head -24; echo ----; grep -n \"JUDGE_UNSUPPORTED\\|JUDGE_PARTIAL\" $B/app/backend/trace.py | cut -c1-200 | head -8",
 "description": "Check judge-partial test coverage, ladder mapping, state composition, and trace judge wording"
}
````

### User / tool · 2026-11-02T05:21:55.119Z

**tool result**
````
----
92:def to_ladder(step: str, verdict: str) -> str:
93-    """Map a judge's own enum to the compose_state vocabulary. Only the positive verdict becomes 'supported';
94-    unknown values become 'unsure' and 'unavailable' stays 'unavailable' (never positive by accident)."""
95-    if verdict == "unavailable":
96-        return "unavailable"
97-    return _TO_LADDER[step].get(verdict, "unsure")
98-
99-
100-def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
----
47:def compose_state(ladder: dict, context: dict = None):
48-    ctx = context or {}
49-    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
50-    if bad:      # a misspelled key must not fail open to 'verified'
51-        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
52-    rejected, doubts = [], []
53-    for c in ladder.get("grounding_failures", []) or []:
54-        rejected.append(_known(c))
55-    if ladder.get("schema_valid", True) is False:
56-        rejected.append("SCHEMA_INVALID")
57-    for c in ladder.get("code_reasons", []) or []:
58-        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
59-    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
60-    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
61-    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
----
32:_OBJECTION = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}
937:                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:02.795Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cd $S/t100-card && grep -n \"_TO_LADDER\" -A6 app/backend/judges.py | cut -c1-200 | head -12; cat > $S/probes-t100/probe_verdicts.py <<'EOF'\nimport sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nfrom tests.unit.test_review_rules import seeded, ent, judge\nfrom app.backend import review as RV\nfrom app.db import db as DB\nfor v in (\"supported\", \"partially\", \"unsupported\", \"unsure\", \"disagrees\", \"unavailable_raise\"):\n    d = pathlib.Path(tempfile.mkdtemp(dir=ROOT + \"/../probe-db\"))\n    conn, cid, out = seeded(d)\n    eid = ent(out, 5)\n    call = None if v == \"unavailable_raise\" else judge(v)\n    r = RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=\"Visit 8: pain 4/10, improving; the patient is recovering well.\")), call=call)\n    it = DB.get_item(conn, eid, cid)\n    print(f\"judge={v:18s} -> review_status={it['review_status']} state={it['state']} reasons={it['state_reasons']} warnings={[w['code'] for w in r['warnings']]}\")\nEOF\nPYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_verdicts.py').read())\n\" 2>&1 | grep -v WARNING | tail -12",
 "description": "Probe the warning returned for each judge verdict on a human-written edit",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:22:03.581Z

**tool result**
````
84:_TO_LADDER = {
85-    "j1": {"supported": "supported", "partially": "partially", "unsupported": "unsupported"},
86-    "j2": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
87-    "j3": {"conflict": "supported", "benign": "disagrees", "unsure": "unsure"},
88-    "j4": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
89-}
90-
--
97:    return _TO_LADDER[step].get(verdict, "unsure")
98-
99-
100-def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
judge=supported          -> review_status=edited state=verified reasons=[] warnings=[]
judge=partially          -> review_status=edited state=needs_review reasons=['JUDGE_PARTIAL'] warnings=['JUDGE_PARTIAL']
judge=unsupported        -> review_status=edited state=needs_review reasons=['JUDGE_UNSUPPORTED'] warnings=['JUDGE_UNSUPPORTED']
judge=unsure             -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
judge=disagrees          -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
judge=unavailable_raise  -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:20.960Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cat > $S/probes-t100/probe_http_clean.py <<'EOF'\nimport os, sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\"):\n    os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom tests.unit.test_api_routes import run_case\nd = tempfile.mkdtemp(dir=ROOT + \"/../probe-db\")\nc = TestClient(create_app(str(pathlib.Path(d) / \"api.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\ntok = run_case(c)\nsnap = lambda: c.get(f\"/api/cases/{tok}\").json()\ne5 = [e for e in snap()[\"entries\"] if e[\"provider\"].startswith(\"Capital PT, visit 8\")][0]\nbefore = snap()\nurl = f\"/api/cases/{tok}/items/{e5['id']}/review\"\nL = \"Visit 8: left-sided pain 4/10, improving; no missed work.\"\ncodes = []\nfor body in [{\"action\": \"edit\", \"edits\": {\"summary\": L}},\n             {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"confirm_warnings\": True},\n             {\"action\": \"edit\", \"edits\": {\"summary\": L}, \"force\": True, \"confirm_warnings\": True, \"override\": True},\n             {\"action\": \"edit\", \"edits\": {\"summary\": L, \"excerpt\": e5[\"excerpt\"]}, \"confirm\": True}]:\n    codes.append(c.post(url, json=body).status_code)\ncodes.append(c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"edit\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}, \"confirm_warnings\": True}).status_code)\ncodes.append(c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}}).status_code)\nafter = snap()\nprint(\"statuses:\", codes)\nprint(\"case JSON identical before/after refused calls:\", before == after)\nEOF\nPYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_http_clean.py').read())\n\" 2>&1 | grep -v \"WARNING\\|INFO\" | tail -5",
 "description": "Confirm refused edit and batch calls leave the case JSON unchanged",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:22:21.878Z

**tool result**
````
statuses: [422, 422, 422, 422, 400, 200]
case JSON identical before/after refused calls: False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:27.304Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cd $S/probes-t100 && python3 - <<'EOF'\nimport re\np = \"probe_http_clean.py\"\ns = open(p).read()\ns = s.replace('codes.append(c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}}).status_code)\\nafter = snap()',\n 'after = snap()\\nprint(\"refused edit + batch-edit calls only -> case JSON identical:\", before == after)\\ncodes.append(c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [e5[\"id\"]], \"edits\": {\"summary\": L}}).status_code)\\nacc = snap()\\nprint(\"batch accept with an edits payload: status\", codes[-1], \"| stored summary unchanged by the payload:\", [x for x in acc[\"entries\"] if x[\"id\"] == e5[\"id\"]][0][\"summary\"] == e5[\"summary\"])')\nopen(p, \"w\").write(s)\nEOF\ncd $B && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_http_clean.py').read())\n\" 2>&1 | grep -v \"WARNING\\|INFO\" | tail -5",
 "description": "Re-run the clean HTTP probe isolating refused edits from the batch accept",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:22:28.337Z

**tool result**
````
refused edit + batch-edit calls only -> case JSON identical: True
batch accept with an edits payload: status 200 | stored summary unchanged by the payload: True
statuses: [422, 422, 422, 422, 400, 200]
case JSON identical before/after refused calls: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:22:49.470Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cat > $S/probes-t100/probe_added_qual.py <<'EOF'\nimport sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nfrom tests.unit.test_review_rules import seeded, ent, judge\nfrom app.backend import review as RV\nfrom app.db import db as DB\nfor summ in [\"Visit 8: patient reports pain 4/10, improving.\",\n             \"Visit 8: pain 4/10, possibly improving.\",\n             \"Visit 8: pain approximately 4/10, improving.\",\n             \"Visit 8: bilateral pain 4/10, improving.\"]:\n    d = pathlib.Path(tempfile.mkdtemp(dir=ROOT + \"/../probe-db\"))\n    conn, cid, out = seeded(d)\n    eid = ent(out, 5)\n    try:\n        r = RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=summ)), call=None)\n        it = DB.get_item(conn, eid, cid)\n        print(f\"SAVED state={it['state']} warnings={[w['code'] for w in r['warnings']]} | {summ}\")\n    except RV.ReviewError as e:\n        print(f\"{e.status} {e.code} reason={e.detail.get('reason')} | {summ}\")\nEOF\nPYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_added_qual.py').read())\n\" 2>&1 | grep -v \"WARNING\" | tail -6; cd $S/t100-card && grep -n \"Pain 4/10\\|Visit 8\" tests/unit/_golden.py 2>/dev/null | head -3; ls tests/unit | grep -i golden | head; grep -rn \"Pain 4/10, improving\" tests/unit/*.py | head -3 | cut -c1-200",
 "description": "Probe summaries that add a self-report, hedge or approximation absent from the quote",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:22:50.252Z

**tool result**
````
SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: patient reports pain 4/10, improving.
SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: pain 4/10, possibly improving.
SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: pain approximately 4/10, improving.
SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: bilateral pain 4/10, improving.
_golden.py
tests/unit/test_generator.py:60:        return dict(summary="Pain 3/10, improving.", excerpt="Pain 4/10, improving.") if n == 5 else extract_ok(u)
tests/unit/test_grounding.py:45:    assert GR.check_excerpt(G.record("sample", 5)["excerpt"], "Pain 4/10, improving.") == []
tests/unit/test_grounding.py:89:    assert codes("Visit 8: pain 4/10, improving.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20") == []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:06.444Z

**tool call — Bash**
````
{
 "command": "git grep -n \"JUDGE_PARTIAL\\|partially\" 24c18a7 -- tests/unit | cut -c1-200 | head -8; echo ----; git grep -n \"_SIDE_NEG\" 24c18a7 -- app | cut -c1-160; echo ----; git show 24c18a7:app/backend/review.py | sed -n 119p; git show HEAD:app/backend/review.py | sed -n 119p; echo ----; git grep -n \"frontend\\|review.js\\|manual.js\" 24c18a7 -- memory/contracts/api.md | head -3",
 "description": "Confirm JUDGE_PARTIAL test coverage, dead constant, and the D-040 string at both commits"
}
````

### User / tool · 2026-11-02T05:23:06.752Z

**tool result**
````
24c18a7:tests/unit/test_confidence.py:3:Ladder:  {"grounding_failures": [codes], "schema_valid": bool, "code_reasons": [codes], "judge": None|"supported"|"partially"|
24c18a7:tests/unit/test_confidence.py:50:    (L(judge="partially"), X(), "JUDGE_PARTIAL"),
24c18a7:tests/unit/test_confidence.py:89:    st, rs = C.compose_state(L(judge="partially", code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(injection=True, date_status="ambiguous"))
24c18a7:tests/unit/test_confidence.py:91:    assert sorted(rs) == sorted(["JUDGE_PARTIAL", "SUMMARY_DROPS_QUALIFIER", "INJECTION_SUSPECTED", "DATE_AMBIGUOUS"])
24c18a7:tests/unit/test_confidence.py:95:    l, c = L(judge="partially"), X(injection=True)
24c18a7:tests/unit/test_confidence.py:137:    assert W.why("JUDGE_PARTIAL") == W.why("JUDGE_PARTIAL")
24c18a7:tests/unit/test_eval_runner.py:316:    """Integrity: hallucination_catch_rate counts only real catches (code reason or judge partially/unsupported); 'unavailable' is reported as judge_unavaila
24c18a7:tests/unit/test_generator.py:96:@pytest.mark.parametrize("verdict,code", [("partially", "JUDGE_PARTIAL"), ("unsupported", "JUDGE_UNSUPPORTED")])
----
24c18a7:app/backend/review.py:118:_SIDE_NEG = {"left", "right", "no", "not", "without"}
----
_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "an attribution phrase (such as complained of or reports)", "negation": "a negation (such as no, not or denies)",
_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "an attribution phrase (such as complained of or reports)", "negation": "a negation (such as no, not or denies)",
----
24c18a7:memory/contracts/api.md:8:- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
24c18a7:memory/contracts/api.md:337:The frontend does not need to refetch the case.
24c18a7:memory/contracts/api.md:534:**Visibility (same split as `/audit`, D-020/D-036).** Public/demo = **metadata only**. `ZLAYT_MODE=local` = **full**. Both modes return `"mode": "metadata" | "full"`. Metadata mode returns: model id, backend, prompt version and hash, call id, verdict, latency, closed reason codes and their fixed sentences, counts, the item's own excerpt spans and text (the case view already shows them), and the action and time of each human event. **Full mode adds, per step:** `evidence.response_raw` (the model's raw answer for an LLM step), and for the human step `evidence.events[].before/after` and `evidence.edited_text`. Prompt text (`system_text`/`user_text`) is **never** in a trace; use `/audit` in local mode. The frontend must not assume the full-only keys exist.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:10.468Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i \"T-100\" ; echo \"exit $?\"; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md | head -30; echo ----; python3 tools/board.py show T-100 | sed -n 1,5p >/dev/null; python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Check for an existing T-100 review file and read the write-once memory note"
}
````

### User / tool · 2026-11-02T05:23:10.693Z

**tool result**
````
exit 1
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it ("review must contain a ```json block"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
----
ok (101 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:18.281Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t100-fresh; cd $B && grep -n \"_WORDS = \\|^_NEG = \\|^_LATERAL\\|^def dropped_qualifiers\\|if _SELF_CARRIED.search(excerpt)\\|^def new_tokens\\|^_SELF_CARRIED\" app/backend/grounding.py; echo ---; grep -n \"_SIDE_NEG\\|^_QUALIFIER_WORDS\\|if toks:\\|if dropped:\\|if span is None:\\|code_reasons = \\[\\]\\|return {\\\"toks\\\"\\|summary_tokens_not_in_excerpt=toks\\|def _check_summary\\|ladder_verdict in (\\\"partially\\\"\" app/backend/review.py; echo ---; grep -n \"def code_check_blockers\\|cc.get(\\\"summary_tokens_not_in_excerpt\\\")\\|failed=\\\"SUMMARY_TOKEN_NOT_IN_EXCERPT\\\" in R\\|failed=\\\"SUMMARY_DROPS_QUALIFIER\\\" in R\" app/backend/trace.py; echo ---; grep -n \"Edit re-check order\\|records/{rid}/entry\\` | D-031\" memory/contracts/api.md | cut -c1-120; echo ---; grep -n \"def test_side_or_negation_edit\\|def test_no_409_confirm\\|def test_judge_is_not_called\" tests/unit/test_api_routes.py tests/unit/test_review_rules.py | cut -c1-140; grep -n \"def test_side_negation_token\\|def test_dropping_a_qualifier\\|def test_seeded_herniation\\|def test_no_confirm_path\" tests/unit/test_review_rules.py | cut -c1-140; grep -n \"def test_manual_entry_side_or_negation\\|def test_manual_entry_judge_objection\" tests/unit/test_manual_and_split.py | cut -c1-140; grep -n \"def _mixed\\|bypass the route\" tests/unit/test_trace.py | cut -c1-120; echo ---; grep -n \"needs_confirm\\|keep-wording\\|keep_wording\\|override\\|confirm_warnings\" app/frontend/review.js app/frontend/manual.js app/frontend/mock.js | cut -c1-120 | head -12",
 "description": "Collect exact line numbers at the card commit for the findings"
}
````

### User / tool · 2026-11-02T05:23:18.446Z

**tool result**
````
126:_WORDS = re.compile(r"\b(left|right|no|not|without)\b", re.IGNORECASE)
146:def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
163:_NEG = re.compile(r"\b(no|not|none|never|without|denies|denied|negative|neither|nor)\b|n't\b", re.IGNORECASE)
166:_LATERAL = re.compile(r"\b(left|right|bilateral(?:ly)?)\b", re.IGNORECASE)
169:_SELF_CARRIED = re.compile(r"\bc/o\b|\bcomplain(?:s|ed|ing|t)?\b|\b(?:patient|pt\.?|he|she|client)\s+(?:states?|stated|reports?|reported|endorses|admits|"
176:_HEDGE_WORDS = re.compile(r"\b(" + _MODAL_MAY + r"|might|possibl[ey]|likely|probabl[ey]|suggest\w*|correlate|appears?|cannot|unclear|"
180:def dropped_qualifiers(summary: str, excerpt: str) -> list:
185:    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
---
118:_SIDE_NEG = {"left", "right", "no", "not", "without"}
119:_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "an attribution phrase (such as complained of or reports)", "negation": "a negation (such as no, not or denies)",
123:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False):
128:    code_reasons = []
136:    if toks:
140:    if dropped:
143:    if span is None:
150:    if ladder_verdict in ("partially", "unsupported"):
157:    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
207:    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
---
352:    toks = cc.get("summary_tokens_not_in_excerpt") or []
355:              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
357:              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
425:def code_check_blockers(conn, case_id: str, cx=None) -> list:
---
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{su
321:**Edit re-check order (R-RV-3, ADR-005; D-034, D-047).** (1) Structure, else 422. (2) Code checks (ADR-012). Any of 
---
tests/unit/test_review_rules.py:144:def test_judge_is_not_called_when_a_code_check_fails_d047(tmp_path):
tests/unit/test_api_routes.py:354:def test_side_or_negation_edit_is_a_422_with_plain_reason_and_confirm_flag_changes_nothing_d047(env):
tests/unit/test_api_routes.py:367:def test_no_409_confirm_path_for_edits_or_manual_entry_remains_d047():
95:def test_seeded_herniation_judge_unsupported_saves_as_needs_review_with_warning(tmp_path):
102:def test_no_confirm_path_remains_confirm_warnings_is_ignored_and_no_event_is_logged(tmp_path):
124:def test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047(tmp_path, summary, reason, key, confirm):
134:def test_dropping_a_qualifier_of_the_quote_is_a_hard_422_d047(tmp_path):
65:def test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047(tmp_path, summary, confirm):
79:def test_manual_entry_judge_objection_saves_pending_with_warning_and_no_override_note(tmp_path):
1030:def _mixed(c, tok, conn):
1038:    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at":
---
app/frontend/manual.js:3:   Server refusals (422, D-047: the reason is shown inline and the typed text stays) are shown 
app/frontend/manual.js:45:      if (confirmWarnings) body.confirm_warnings = true;
app/frontend/manual.js:51:      if (r.status === 409 && err.code === "needs_confirm") {
app/frontend/manual.js:55:          el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn", "
app/frontend/review.js:126:  // The "keep my wording" confirmation below (409 needs_confirm) is the pre-D-047 path: dead
app/frontend/review.js:127:  // delete showConfirm and the needs_confirm branch in RV.act with that card.
app/frontend/review.js:137:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", on
app/frontend/review.js:176:      } else if (e && e.code === "needs_confirm") showConfirm(id, e, body);
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:23:45.946Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; cat > $S/probes-t100/probe_msg.py <<'EOF'\nimport sys, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.append(ROOT)\nfrom tests.unit.test_review_rules import seeded, ent, judge\nfrom app.backend import review as RV\nd = pathlib.Path(tempfile.mkdtemp(dir=ROOT + \"/../probe-db\"))\nconn, cid, out = seeded(d)\neid = ent(out, 5)\nfrom app.db import db as DB\nprint(\"quote:\", DB.get_item(conn, eid, cid)[\"excerpt\"])\ntry:\n    RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=\"Visit 8: pain 4/10, improving.\")), call=judge(\"supported\"))\n    print(\"saved\")\nexcept RV.ReviewError as e:\n    print(e.status, e.code, e.detail, \"|\", e.message)\nEOF\nPYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; ROOT='$S/t100-card'; sys.argv=['x', ROOT]\nexec(open('$S/probes-t100/probe_msg.py').read())\n\" 2>&1 | grep -v WARNING | tail -4",
 "description": "Capture the exact 422 message for a dropped attribution phrase",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:23:46.562Z

**tool result**
````
quote: Pain 4/10, improving.
saved
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:20.879Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD frontend hits:\"; git grep -n \"needs_confirm\\|btn-keep-wording\\|confirm_warnings\" HEAD -- app/frontend | cut -c1-140; echo \"card frontend hits:\"; git grep -n \"needs_confirm\\|btn-keep-wording\\|confirm_warnings\" 24c18a7 -- app/frontend | cut -c1-140; echo ----; git show --stat 24c18a7 -- tests/e2e | tail -1; echo \"(e2e files changed by card commit: none if empty above)\"; mkdir -p artifacts/review-evidence/T-100 2>/dev/null; ls -d artifacts/review-evidence/T-100",
 "description": "Confirm frontend 409 references at card commit and HEAD, and e2e changes"
}
````

### User / tool · 2026-11-02T05:24:21.050Z

**tool result**
````
HEAD frontend hits:
HEAD:app/frontend/excerpt.js:2:   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows 
card frontend hits:
24c18a7:app/frontend/excerpt.js:2:   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and sho
24c18a7:app/frontend/manual.js:3:   Server refusals (422, D-047: the reason is shown inline and the typed text stays) are shown in plain wor
24c18a7:app/frontend/manual.js:45:      if (confirmWarnings) body.confirm_warnings = true;
24c18a7:app/frontend/manual.js:51:      if (r.status === 409 && err.code === "needs_confirm") {
24c18a7:app/frontend/manual.js:55:          el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn", "data-testid"
24c18a7:app/frontend/review.js:126:  // The "keep my wording" confirmation below (409 needs_confirm) is the pre-D-047 path: dead once backen
24c18a7:app/frontend/review.js:127:  // delete showConfirm and the needs_confirm branch in RV.act with that card.
24c18a7:app/frontend/review.js:137:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () =>
24c18a7:app/frontend/review.js:176:      } else if (e && e.code === "needs_confirm") showConfirm(id, e, body);
----
(e2e files changed by card commit: none if empty above)
artifacts/review-evidence/T-100
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:28.968Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8; S=$B/scratchpad; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100; cp $S/probes-t100/*.py $E/ && cd $E && export PYTHONDONTWRITEBYTECODE=1 && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && { echo \"# T-100 probe outputs (card commit 24c18a7 archive copy unless noted). Scratch copies: $S\"; echo \"## probe_http_clean.py (t100-card)\"; $PY -I probe_http_clean.py $S/t100-card 2>&1 | grep -v \"WARNING\\|INFO\"; echo \"## probe_http.py (t100-card)\"; $PY -I probe_http.py $S/t100-card 2>&1 | grep -v \"WARNING\\|INFO\"; echo \"## probe_gap.py (t100-card, judge unavailable / supported)\"; $PY -I probe_gap.py $S/t100-card 2>&1 | grep -v WARNING; echo \"## probe_added_qual.py (t100-card, judge unavailable)\"; $PY -I probe_added_qual.py $S/t100-card 2>&1 | grep -v WARNING; echo \"## probe_verdicts.py (t100-card)\"; $PY -I probe_verdicts.py $S/t100-card 2>&1 | grep -v WARNING; echo \"## probe_gate_alone.py (mut-tok: route token check disabled)\"; $PY -I probe_gate_alone.py $S/mut-tok 2>&1 | grep -v WARNING; } > $E/probe_outputs.txt 2>&1; wc -l $E/probe_outputs.txt; grep -c \"SAVED\\|422\\|identical\\|export built\\|gate blockers\" $E/probe_outputs.txt",
 "description": "Copy probe scripts into review evidence and capture their outputs",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:24:33.690Z

**tool result**
````
      55 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/probe_outputs.txt
36
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:24:35.400Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/probe_outputs.txt"
}
````

### User / tool · 2026-11-02T05:24:35.417Z

**tool result**
````
1	# T-100 probe outputs (card commit 24c18a7 archive copy unless noted). Scratch copies: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
2	## probe_http_clean.py (t100-card)
3	refused edit + batch-edit calls only -> case JSON identical: True
4	batch accept with an edits payload: status 200 | stored summary unchanged by the payload: True
5	statuses: [422, 422, 422, 422, 400, 200]
6	case JSON identical before/after refused calls: True
7	## probe_http.py (t100-card)
8	edit plain: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
9	edit confirm_warnings: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
10	edit force: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
11	edit override+keep_my_wording+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
12	edit confirm_warnings str 'true': HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, “no”, which the quote does not say. Remove it or change the quote.'
13	accept carrying edits payload: HTTP 200 code=ok reason=None msg=None
14	batch action=edit: HTTP 400 code=bad_request reason=None msg='Send an action (accept or reset) and a list of entry ids.'
15	batch action=accept: HTTP 422 code=invalid_batch reason=None msg='Only verified entries can be accepted together; nothing was changed.'
16	entries unchanged after every refused route: False
17	e5 review_status now: accepted | summary now: Pain 4/10, improving. Patient reports missing 3 days of work.
18	edit number: HTTP 422 code=invalid_edit reason=SUMMARY_NUMBER_NOT_IN_EXCERPT msg='The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote.'
19	edit side: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “right”, which the quote does not say. Remove it or change the quote.'
20	edit negation: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “not”, which the quote does not say. Remove it or change the quote.'
21	edit qualifier drop: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “no”, which the quote does not say. Remove it or change the quote.'
22	manual side+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “left”, which the quote does not say. Remove it or change the quote.'
23	manual negation+force: HTTP 422 code=invalid_edit reason=SUMMARY_TOKEN_NOT_IN_EXCERPT msg='The summary says “not”, which the quote does not say. Remove it or change the quote.'
24	manual number+confirm: HTTP 422 code=invalid_edit reason=SUMMARY_NUMBER_NOT_IN_EXCERPT msg='The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote.'
25	## probe_gap.py (t100-card, judge unavailable / supported)
26	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; denies radiating symptoms.
27	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, never worse.
28	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, none reported.
29	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: bilateral pain 4/10, improving.
30	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: negative for distress; pain 4/10, improving.
31	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; absent distress.
32	[judge_unavailable] SAVED  state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE'] gate_blockers=[] | Visit 8: pain 4/10, improving; neither worse nor better.
33	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; denies radiating symptoms.
34	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, never worse.
35	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, none reported.
36	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: bilateral pain 4/10, improving.
37	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: negative for distress; pain 4/10, improving.
38	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; absent distress.
39	[judge_supported] SAVED  state=verified reasons=[] warnings=[] gate_blockers=[] | Visit 8: pain 4/10, improving; neither worse nor better.
40	## probe_added_qual.py (t100-card, judge unavailable)
41	SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: patient reports pain 4/10, improving.
42	SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: pain 4/10, possibly improving.
43	SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: pain approximately 4/10, improving.
44	SAVED state=needs_review warnings=['JUDGE_UNAVAILABLE'] | Visit 8: bilateral pain 4/10, improving.
45	## probe_verdicts.py (t100-card)
46	judge=supported          -> review_status=edited state=verified reasons=[] warnings=[]
47	judge=partially          -> review_status=edited state=needs_review reasons=['JUDGE_PARTIAL'] warnings=['JUDGE_PARTIAL']
48	judge=unsupported        -> review_status=edited state=needs_review reasons=['JUDGE_UNSUPPORTED'] warnings=['JUDGE_UNSUPPORTED']
49	judge=unsure             -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
50	judge=disagrees          -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
51	judge=unavailable_raise  -> review_status=edited state=needs_review reasons=['JUDGE_UNAVAILABLE'] warnings=['JUDGE_UNAVAILABLE']
52	## probe_gate_alone.py (mut-tok: route token check disabled)
53	stored state: verified [] | review: accepted | summary: Visit 8: left-sided pain 4/10, improving.
54	gate blockers for item: []
55	export built: summary 'left-sided' in letter/notes: True
56	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:28.472Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-100-staff-engineer.md",
 "content": "# T-100 review (D-047), staff-engineer-reviewer\n\nReviewed commit 24c18a7 (card T-100). HEAD has moved to f5ddec8 (frontend and e2e only; app/backend and tests/unit are byte-identical to 24c18a7). Verdict: **fail**.\n\n**Blocker.** The route still stores an edit that adds an attribution, hedge or approximation the quote does not have (\"patient reports pain 4/10\", \"possibly improving\", \"approximately 4/10\"). D-047 says qualifier tokens missing from the excerpt are a hard 422; only the reverse direction (qualifier dropped from the summary) is enforced.\n\n**Majors.** (a) The export gate is not an independent second line: it reads stored reasons and never re-runs the checks, so a route that stores no reason passes the gate and the letter exports \"left-sided\". (b) The negation and side word list is narrower than the module's own list (denies, never, none, negative, absent, neither, bilateral all save). (c) AC 1 is checked done, but at 24c18a7 the frontend 409 branch and the e2e half were not done.\n\n**Checked as asked.**\n- No route stores a side or negation edit: confirm_warnings, force, override, confirm, string 'true', manual entry and batch all refuse. Batch edit returns 400; batch accept ignores the edits payload. Refused calls leave the case JSON identical. Holds.\n- 422 reasons in plain words: mostly yes. Grammar nit in the two-word case. The qualifier message still uses the speech verbs (minor, below).\n- T-098 gate tests: they now write state directly. Removing the gate fails 3 of them, so they exercise the gate's reading of stored state. They do not show the gate as a backstop for the route (major, below).\n- D-040 speaker-word string at review.py:119: not reworded at 24c18a7 or at HEAD.\n- api.md: updated for the 422 shape and the no-409 rule. Two statements are inaccurate (line 321: \"the same checks the export gate runs\"; the HIGHLIGHT_NOT_FOUND 422 is outside D-047).\n- Judge objection to a human edit saves as needs_review with a warning, and this is consistent across edit (review.py:212) and manual entry (review.py:360).\n- Mutation: token check disabled (review.py:136) fails 20 tests. Qualifier-drop check disabled fails 6. Gate disabled fails 3.\n- Card-commit archive: the requested selection gives 103 passed. Full tests/unit gives 1814 passed and 4 skipped, not the 1834 the handoff claims (minor, below).\n\n**Exercised.** See the `exercised` list in the JSON. Probe outputs and scripts are in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/` (probe_outputs.txt, probe_*.py). probe_http.py has two mislabelled lines (its \"entries unchanged\" line is wrong because its accept ran first; its \"qualifier drop\" row is a \"no\" token case). probe_http_clean.py is the authoritative route check.\n\n```json\n{\"card\": \"T-100\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Commit 24c18a7 (D-047): app/backend/review.py, store.py, export.py, trace.py; tests/unit (test_review_rules.py, test_manual_and_split.py, test_api_routes.py, test_trace.py, test_export.py, test_ocr_invariant.py); memory/contracts/api.md. HEAD at review time f5ddec8 (backend unchanged since 24c18a7; frontend and tests/e2e changed). Synthetic sample case (golden sample record 5 and record 8 via tests/unit fixtures). HTTP probes ran in-process via FastAPI TestClient against the archive copy; no running app URL was used.\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md, memory/ORCHESTRATOR_DECISIONS.md (D-040, D-045, D-047), board.py show T-100, git show --stat and the full app/tests/api.md diff of 24c18a7.\",\n  \"git log --oneline -3; git merge-base --is-ancestor 24c18a7 HEAD (ancestor); git diff 24c18a7 HEAD -- app/backend tests/unit memory/contracts (empty); git show --stat f5ddec8.\",\n  \"Working tree (HEAD f5ddec8 plus uncommitted changes from other cards): .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k 'edit or manual or d047 or d034' gave 103 passed; full tests/unit gave 2 failed (test_eval_runner.py calibration header tests, outside T-100), 1832 passed, 1 skipped.\",\n  \"git archive 24c18a7 extracted into a scratchpad copy (diff -rq against a second fresh extract: identical except __pycache__). Run with .venv/bin/python -I and the copy appended to sys.path: the same selection gave 103 passed; full tests/unit gave 1814 passed, 4 skipped (3 need a git repository, 1 is the live judge eval).\",\n  \"Mutants of the archive copy, full tests/unit each: review.py:136 'if False and toks' gave 20 failed; review.py:140 'if False and dropped' gave 6 failed (5 of them T-098 tests failing at the route assertion); trace.py:425 code_check_blockers returning [] gave 3 failed (T-098 gate tests).\",\n  \"HTTP probes (TestClient on the archive): POST items/{id}/review with edit + confirm_warnings, force, override+keep_my_wording+confirm, confirm_warnings='true'; POST records/{rid}/entry with confirm_warnings and force; POST review/batch with action edit and accept. Case JSON identical before/after the refused calls (probe_http_clean.py).\",\n  \"Service-level probes (seeded() from tests/unit/test_review_rules.py): side, negation, qualifier-add and approximation summaries with judge unavailable and judge supported; judge verdicts supported/partially/unsupported/unsure/disagrees/unavailable; gate-alone probe on the token-check-disabled mutant (export built with 'left-sided').\",\n  \"Read review.py (full), grounding.py 120-232, spanish_text.py 189-245, trace.py 330-440, case_extras.py 24-64 and 107-120, api.py 347-361, 423-432, 496-506, db.py 215-237, api.md line 321 and line 26, tests/e2e/test_edit.py and test_rerun_judge.py (24c18a7 and HEAD), app/frontend/review.js and manual.js at 24c18a7 and HEAD (git grep for needs_confirm, btn-keep-wording, confirm_warnings).\",\n  \"Evidence: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/probe_outputs.txt and the probe_*.py scripts beside it.\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"d047_refusal_routes\": 3, \"d047_token_vocabulary\": 2, \"gate_as_second_line\": 2, \"judge_objection_consistency\": 4, \"plain_422_reasons\": 3, \"d040_wording\": 2, \"api_md_accuracy\": 3, \"tests_mutation_and_behaviour\": 4, \"llm_code_boundary\": 5, \"ac_honesty\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"D-047 qualifier tokens missing from the quote are saved, not refused (attribution, hedge, approximation added to the summary)\",\n   \"evidence\": \"app/backend/review.py:136-142 runs only grounding.new_tokens (side and negation words, grounding.py:126 and :146-160) and dropped_qualifiers. dropped_qualifiers (grounding.py:180-195) tests quote-to-summary only, e.g. grounding.py:185 'if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary)'. Repro: probe_added_qual.py (artifacts/review-evidence/T-100/) on the 24c18a7 copy, quote 'Pain 4/10, improving.' (record 5). probe_outputs.txt lines 41-44: 'Visit 8: patient reports pain 4/10, improving.' SAVED state=needs_review; 'Visit 8: pain 4/10, possibly improving.' SAVED; 'Visit 8: pain approximately 4/10, improving.' SAVED; each with judge unavailable and no 422.\",\n   \"why_it_matters\": \"Spec constraint: D-047 (memory/ORCHESTRATOR_DECISIONS.md:55) says 'side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a hard 422'; the brief says the same. The code enforces the reverse direction only. 'Patient reports' attributes a statement the record does not attribute, so this invents a fact. Under D-045(b) a human edit is exempt from the judge veto, and the gate reads only stored code reasons (trace.py:352-357), so the item exports with a warning on the item only.\",\n   \"fix\": \"In _check_summary (review.py:136-142), add the reverse check before the judge call, shared by edit and manual entry: for each qualifier kind present in the new summary (self_report via grounding._SELF_CARRIED, hedge via grounding._HEDGE_WORDS, approx via grounding._APPROX) with no matching kind in the new quote, raise _bad(...) with a reason code (SUMMARY_TOKEN_NOT_IN_EXCERPT or a new named code). Keep the existing drop check.\",\n   \"acceptance_test\": \"test_review_rules.py: parametrize summaries 'Visit 8: patient reports pain 4/10, improving.', 'Visit 8: pain 4/10, possibly improving.', 'Visit 8: pain approximately 4/10, improving.' against quote 'Pain 4/10, improving.'; assert 422 invalid_edit, nothing saved, no event, judge spy never called, for confirm_warnings False and True. Same three through test_manual_and_split.py manual_entry. Existing qualifier-drop test (test_review_rules.py:134) must still pass.\"},\n  {\"severity\": \"major\",\n   \"title\": \"The export gate is not an independent second line; it trusts stored reasons that the route alone writes\",\n   \"evidence\": \"app/backend/trace.py:352-357 reads cc.get('summary_tokens_not_in_excerpt') from the stored ladder and 'SUMMARY_DROPS_QUALIFIER' in R from stored state reasons. code_check_blockers (trace.py:425-439) uses those step results only; no call to grounding.new_tokens or dropped_qualifiers on the current text. Repro: probe_gate_alone.py on a scratch copy with the route token check disabled (review.py:136). probe_outputs.txt lines 53-55: 'stored state: verified []', 'gate blockers for item: []', 'export built: summary left-sided in letter/notes: True'. memory/contracts/api.md:321 says 'These are the same checks the export gate (T-098) runs, so an edit the route stores can never be an export blocker for a code reason.' The T-098 tests (test_trace.py:1030-1040, _mixed) write the state directly, so they exercise the reading path only.\",\n   \"why_it_matters\": \"D-047's rationale is that the gate and the route agree so no item can be confirmed into an unexportable state. A backstop that reads the field it backstops does not catch a route regression that stores no reason. No live bypass exists at 24c18a7 (every route tried refused), so this is major, not blocker. The api.md sentence is inaccurate as written.\",\n   \"fix\": \"Make the gate recompute the two pure checks from the current summary and quote for each entry it scopes (human-written, edited or accepted), in addition to the stored reasons, using the same helper the route uses. Correct api.md:321 to say what the gate actually reads.\",\n   \"acceptance_test\": \"A test that writes an edit with 'Visit 8: left-sided pain 4/10, improving.' through DB.apply_review with no stored reasons (judge supported), then asserts trace.export_blockers lists the item with reason_code SUMMARY_TOKEN_NOT_IN_EXCERPT and that export_routes raises ExportBlocked. Removing the recompute must fail it.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Negation and side words are narrower than the module's own vocabulary; D-047 'negation' is not settled as the enumerated list\",\n   \"evidence\": \"app/backend/grounding.py:126 _WORDS = left|right|no|not|without; grounding.py:163 _NEG also has none|never|denies|denied|negative|neither|nor; grounding.py:166 _LATERAL also has bilateral(ly); app/backend/review.py:118 _SIDE_NEG (same five words as _WORDS) is defined and never used. Repro: probe_gap.py. probe_outputs.txt lines 26-32 (judge unavailable): 'denies radiating symptoms', 'never worse', 'none reported', 'bilateral pain', 'negative for distress', 'absent distress', 'neither worse nor better' all SAVED state=needs_review, no gate blocker. Lines 33-39 (judge supported): all SAVED state=verified.\",\n   \"why_it_matters\": \"The enumerated D-047 list (memory/ORCHESTRATOR_DECISIONS.md:55) is met as written, so this is not a blocker by its letter. The card, the brief and the rationale say 'side, negation or qualifier token', and a 'denies' or 'never' the record does not state is the same risk D-047 describes. The module already defines the wider class, so the two lists disagree. See question 1.\",\n   \"fix\": \"Take the side and negation token set from the same _NEG and _LATERAL definitions that dropped_qualifiers uses, and delete or use _SIDE_NEG so only one list exists. If Chris confirms the enumerated list is intended, record that in D-047 and move this to a note.\",\n   \"acceptance_test\": \"test_review_rules.py: parametrize 'denies radiating symptoms', 'never worse', 'none reported', 'bilateral pain' against quote 'Pain 4/10, improving.'; assert 422 with the same reason as no/not, nothing saved, judge not called.\"},\n  {\"severity\": \"major\",\n   \"title\": \"AC 1 is checked done, but at 24c18a7 the frontend 409 branch and the e2e half were not done\",\n   \"evidence\": \"board.py show T-100: AC 1 text 'no 409 confirm path remains (API + frontend copy)' with done: true, evidence 'e2e not run ... frontend copy removal handed to T-097 note'. At 24c18a7: app/frontend/review.js:126-137 and :176 (showConfirm, btn-keep-wording, needs_confirm branch); app/frontend/manual.js:45-55 (confirm_warnings, needs_confirm, retry button). 'git show --stat 24c18a7 -- tests/e2e' is empty. At HEAD f5ddec8 'git grep -n needs_confirm|btn-keep-wording|confirm_warnings HEAD -- app/frontend' shows only a comment in excerpt.js:2.\",\n   \"why_it_matters\": \"A checked box says the frontend and e2e halves are done when the card's own handoff says they are not. The gap is closed at HEAD by f5ddec8 (another card, T-097 r2). I read those changes but did not run the e2e specs (Playwright and a live server are needed), so the e2e half is not verified.\",\n   \"fix\": \"Keep AC 1 open for the frontend and e2e clauses, or split them to T-097 and cite f5ddec8 as their evidence. Run tests/e2e/test_edit.py and test_rerun_judge.py on a live server before closing.\",\n   \"acceptance_test\": \"git grep -n 'needs_confirm|btn-keep-wording|confirm_warnings' -- app/frontend returns no product match at the commit that closes AC 1; the e2e specs above pass against a live server.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The D-040 speaker-word string is still in the user-facing 422 message\",\n   \"evidence\": \"app/backend/review.py:119 '\\\"self_report\\\": \\\"an attribution phrase (such as complained of or reports)\\\"', rendered by review.py:141-142 for SUMMARY_DROPS_QUALIFIER. Byte-identical at 24c18a7 and HEAD ('git show 24c18a7:app/backend/review.py | sed -n 119p' equals 'git show HEAD:app/backend/review.py | sed -n 119p'). D-040 (memory/ORCHESTRATOR_DECISIONS.md:48): no code or model labels who is speaking.\",\n   \"why_it_matters\": \"The brief asked for this string to be reworded and it was not. The message does not label a speaker, so it does not breach D-040 by its letter, but it puts the speech verbs D-040 retired into user-facing text.\",\n   \"fix\": \"Name the kind without speech verbs, e.g. 'a word that says whose account the quote gives', and keep the example verbs out of the 422 text.\",\n   \"acceptance_test\": \"A test that drops the self-report kind asserts the message contains neither 'reports' nor 'complained', and still says the qualifier is missing from the summary.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"HIGHLIGHT_NOT_FOUND is now a hard 422, which D-047 does not cover\",\n   \"evidence\": \"app/backend/review.py:143-144 raises _bad('The quoted sentences cannot be found in the record...', reason='HIGHLIGHT_NOT_FOUND') before the judge. At 24c18a7 this path appended a code reason and saved as needs_review (see the removed lines in the 24c18a7 diff of review.py). memory/contracts/api.md:321 lists it among the 422 causes.\",\n   \"why_it_matters\": \"D-047 covers side, negation and qualifier tokens. A summary-only edit on an item whose quote cannot be located is now refused rather than saved for review. That is a behaviour change nobody decided.\",\n   \"fix\": \"Either restore the needs_review path, or record the decision in ORCHESTRATOR_DECISIONS.md and keep the api.md line.\",\n   \"acceptance_test\": \"Whichever is chosen, a test pins it: summary-only edit on an item with an unlocatable quote returns the decided result.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The handoff test count is not reproducible from the commit\",\n   \"evidence\": \"Handoff: 'tests/unit 1834 passed (1 skipped)'. On the git archive of 24c18a7 the same command gives 1814 passed, 4 skipped (3 'no git repository here (exported tree)' skips plus the live judge eval). In the working tree at f5ddec8 with other cards' changes: 2 failed, 1832 passed, 1 skipped. The T-100 selection gives 103 passed in both trees.\",\n   \"why_it_matters\": \"Evidence must reproduce from the cited commit. The 1834 figure matches neither tree.\",\n   \"fix\": \"Record the commit sha and the exact command with its output in the card evidence, run from a clean archive.\",\n   \"acceptance_test\": \"Re-running the stated command on git archive 24c18a7 gives the number written on the card.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"No test pins the JUDGE_PARTIAL warning for a human-written edit\",\n   \"evidence\": \"git grep -n 'partially' 24c18a7 -- tests/unit/test_review_rules.py tests/unit/test_manual_and_split.py tests/unit/test_api_routes.py is empty. Human-edit judge tests cover 'unsupported' and 'unavailable' only. The branch is review.py:150-151. probe_verdicts.py gives partially -> needs_review, warning JUDGE_PARTIAL, consistent with the code.\",\n   \"why_it_matters\": \"The orchestrator's judge-objection rule has one untested branch. It works today, but nothing stops it regressing.\",\n   \"fix\": \"Parametrize the existing judge-objection tests over 'partially' and 'unsupported'.\",\n   \"acceptance_test\": \"test_seeded_herniation_judge_unsupported_saves_as_needs_review_with_warning passes for judge partially as well, asserting warning JUDGE_PARTIAL.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Dead or always-empty fields left behind by the change\",\n   \"evidence\": \"app/backend/review.py:118 _SIDE_NEG is never used. review.py:128, :155 and :157 keep code_reasons and 'toks' that are now always empty. review.py:207 stores summary_tokens_not_in_excerpt, which is always []; trace.py:352 reads it.\",\n   \"why_it_matters\": \"The stored field looks like a check result but is always empty, which is misleading to the next reader of the trace.\",\n   \"fix\": \"Delete the dead constant and the always-empty fields, or make them mean something.\",\n   \"acceptance_test\": \"No behaviour change: tests/unit passes unchanged after removal.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Wording and test-style nits\",\n   \"evidence\": \"review.py:138 renders 'The summary says “left”, “no”, which the quote does not say.' (two words read as a list). test_api_routes.py:367-374 greps source text for confirm_warnings and keep_my_wording rather than testing behaviour (persona item 13). app/db/db.py:20 still lists keep_my_wording as a writable DB action; no route can reach it (review.py:15 ACTIONS excludes it).\",\n   \"why_it_matters\": \"Small clarity issues; the DB action is harmless today but is the second place the removed path could come back.\",\n   \"fix\": \"Say 'and' between two words; keep the behavioural test and drop the source grep; remove keep_my_wording from db.py ACTIONS when that file's owner next touches it.\",\n   \"acceptance_test\": \"tests/unit still passes; the message for two words contains 'and'.\"}\n ],\n \"whats_right\": [\n  \"Every refusal route tried (confirm_warnings, force, override+keep_my_wording+confirm, string 'true', manual entry, batch edit) returns 422 or 400 and leaves the case JSON identical; batch accept ignores the edits payload (probe_outputs.txt lines 3-6).\",\n  \"A judge objection to a human edit is consistent: edit and manual entry both return chk['warnings'] (review.py:212 and :360), and the warning code equals the state reason for partially, unsupported and unavailable (probe_outputs.txt lines 46-51).\",\n  \"The token check runs before any judge call and is pinned: disabling it fails 20 tests across test_review_rules.py, test_manual_and_split.py and test_api_routes.py.\"\n ],\n \"questions_for_chris\": [\n  \"D-047 'negation': is it the enumerated list (no, not, without) or the class (denies, never, none, negative, absent, neither, nor)? Blocker if class; major if the list. Same question for side words (bilateral).\",\n  \"Is the HIGHLIGHT_NOT_FOUND hard 422 (review.py:143-144) intended, or should it stay a needs_review warning as before 24c18a7?\",\n  \"Pre-D-047 overrides: export.py at 24c18a7 no longer prints 'paralegal confirmed keep my wording (reviewer override: ...)' in internal notes for old items. review_events rows remain in the DB. Should the notes still disclose legacy overrides?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T05:25:28.628Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-100-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:31.710Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json, re\nt = open(\"reviews/T-100-staff-engineer.md\", encoding=\"utf-8\").read()\nfences = re.findall(r\"```(\\w*)\", t)\nprint(\"fence tags:\", fences)\nblk = re.search(r\"```json\\n(.*?)\\n```\", t, re.S).group(1)\nd = json.loads(blk)\nprint(\"card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"severities\", sev)\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"rule verdict:\", rule, \"matches:\", rule == d[\"verdict\"])\nprint(\"whats_right count:\", len(d[\"whats_right\"]), \"| scores:\", len(d[\"scores\"]))\nEOF\npython3 tools/board.py validate 2>&1 | tail -3",
 "description": "Parse the review JSON block, check the verdict rule, and run board validate"
}
````

### User / tool · 2026-11-02T05:25:31.883Z

**tool result**
````
fence tags: ['json', '']
card T-100 | persona staff-engineer-reviewer | model claude-haiku-5-5 | verdict fail
severities ['blocker', 'major', 'major', 'major', 'minor', 'minor', 'minor', 'minor', 'nit', 'nit']
rule verdict: fail matches: True
whats_right count: 3 | scores: 10
ok (101 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:39.199Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t100_d047_review_patterns.md",
 "content": "---\nname: t100-d047-review-patterns\ndescription: T-100 (D-047 hard 422 for side/negation/qualifier tokens) r1 24c18a7 fail: one-directional qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved\nmetadata:\n  type: project\n---\n\nT-100 r1 (card commit 24c18a7, verdict fail: 1 blocker, 3 majors). Patterns that will recur on any \"refuse this at the route\" card:\n\n- **One-directional check.** The route checked \"qualifier dropped from the summary\" but not \"qualifier added to the summary that the quote lacks\", while the decision text said \"tokens missing from the excerpt\". Read the decision's direction word literally and probe both directions (added and dropped).\n- **Gate reads what the route writes.** The T-098 gate used stored reasons and stored ladder fields (trace.py:352-357, code_check_blockers trace.py:425). Test it as a backstop: write an edit straight to the DB with no reasons and see whether the gate or export catches it. The gate tests that set state directly exercise the reading path, not the backstop.\n- **Enumerated list vs class.** The decision enumerated \"no/not/without\" while the module's own `_NEG` and `_LATERAL` define a wider class. Report as major, and put \"is it the class?\" in questions_for_chris, rather than guessing.\n- **HEAD moves after the card commit.** At review time HEAD was f5ddec8, one commit past 24c18a7, and the working tree was dirty. Review the card's sha with `git archive <sha>`, and check the backend is unchanged between the sha and HEAD with `git diff <sha> HEAD -- app/backend tests/unit`.\n- **Handoff counts do not reproduce.** The card claimed 1834 passed; the archive gave 1814 passed, 4 skipped (git-dependent skips in an exported tree). Always re-run the counts on the archive.\n\n**Why:** Chris's D-047 was an orchestrator decision, and the reviewer had to decide literal-spec blocker vs. class-scope major.\n**How to apply:** For future token/refusal cards, probe added and dropped tokens both ways, and probe the gate with the route check disabled. Link [[project_t080_trace_review_patterns]] (gate vs export agreement) and [[project_t098_gate_second_line]] if written later.\n"
}
````

### User / tool · 2026-11-02T05:25:39.300Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t100_d047_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:41.433Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t100_d047_review_patterns.md",
 "old_string": "Link [[project_t080_trace_review_patterns]] (gate vs export agreement) and [[project_t098_gate_second_line]] if written later.",
 "new_string": "See also [[project_t080_trace_review_patterns]] (gate vs export agreement)."
}
````

### User / tool · 2026-11-02T05:25:41.534Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t100_d047_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:43.719Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change",
 "new_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change\n- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card"
}
````

### User / tool · 2026-11-02T05:25:43.826Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:46.106Z

T-100 (24c18a7): fail, 1 blocker and 3 majors (added attribution/hedge tokens still save, the gate trusts stored reasons, the negation list is narrow, AC 1 was checked done early); see /Users/arsis/zlayt-pm-project/reviews/T-100-staff-engineer.md.
