# Subagent: T-155 test-change review (T-155 test-change review)

Source: `agent-ae9ea60ccf18ae271.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:40:33.792Z

Review board card T-155 (commit 20b3a42, tests only) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-155` and its triage table.

For each changed test, judge whether the change follows a recorded decision (D-058, D-059, T-134 r2, T-144), or whether it weakens what the test protects. The T-144 row-height change now measures the row without the collapsed list; is that still a real constraint?

Confirm that T-158 holds the real regression: the 390px refusal box below the fold. On a clean HEAD worktree, on your own port with E2E_REQUIRE_DB=1, run the changed e2e files.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-155-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Stop only your own PIDs. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:35.332Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T14:40:35.343Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:35.626Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-155",
 "description": "Show board card T-155"
}
````

### User / tool · 2026-11-02T14:40:35.754Z

**tool result**
````
---
id: "T-155"
title: "E2E red at HEAD: 7-8 deterministic failures (test_polish_r5, test_rerun_judge x2, test_stepper x4, ...) after backend changes T-134/T-139/T-145/T-146; triage each to stale test vs real regression and fix or file"
milestone: "M2"
role: "qa"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:16:07Z"
updated_at: "2026-11-02T14:40:30Z"
claimed_by: "qa"
claimed_at: "2026-11-02T14:16:16Z"
rounds: 0
commits: ["20b3a42"]
reviews: []
ac:
  - {"n": 1, "text": "full tests/e2e green on a clean HEAD worktree (E2E_REQUIRE_DB=1); each failure explained on the card: test updated with reason, or a backend/frontend card filed for a real regression", "done": true, "evidence": "full tests/e2e on clean HEAD 078c5ae worktree + 3 test files updated (20b3a42), own server :7955, E2E_REQUIRE_DB=1: 281 passed, 2 skipped, 1 failed (test_code_check_refusal mobile, flaky ~50%: real frontend layout bug filed as T-158, not masked). Triage in handoff"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:16:09Z orchestrator: assigned: qa
- 2026-11-02T14:16:16Z qa: claimed
- 2026-11-02T14:39:00Z orchestrator: Known e2e reds to triage: test_polish_r3 first entry y=552 (>520) from the T-149 overview block (T-149 r2 is moving the first entry above the fold - coordinate, don't loosen first); test_rerun_judge x2 expect 'Edited by you, not AI-checked' but get 'Edited; waiting for your check' (T-134 wording change, D-058 - stale test).
- 2026-11-02T14:40:22Z qa: AC 1 checked: full tests/e2e on clean HEAD 078c5ae worktree + 3 test files updated (20b3a42), own server :7955, E2E_REQUIRE_DB=1: 281 passed, 2 skipped, 1 failed (test_code_check_refusal mobile, flaky ~50%: real frontend layout bug filed as T-158, not masked). Triage in handoff
- 2026-11-02T14:40:22Z qa: moved in_progress -> in_review
- 2026-11-02T14:40:30Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: 3 e2e files updated (20b3a42), tests only. Triage of the 9 failures in my HEAD 078c5ae run (plus 3 flakes): STALE test_stepper x4 (judged_case L6 now has 4 judge objections, not 3: D-059 marks 'Amount due $1,150' unclear and the recorded second check disagrees; const L6_OBJECTIONS=4) · STALE test_rerun_judge x2 (Why-dialog verdict of an unaccepted edit is 'Edited; waiting for your check', T-134 r2 edit_to_check, api.md Item trace; D-045b wording kept in panel/step) · STALE test_polish_r3 density x2 (T-144 collapsed 'Also in this record' list adds 30-57px; budgets now measure the row without it, so row growth is still caught) · FLAKE test_polish_r3 shortcut sheet (focus restore race after Escape; fixed by waiting for btn-shortcuts focus) · REAL FLAKE test_code_check_refusal mobile 390x844 fails ~50% (3 of 6): accept-refused box ends below fold, scrollY varies; filed T-158 (frontend) with repro, test unchanged · LOAD FLAKE test_rerun_judge refused-export 1440 ('Running the second check…' without count, trace cache not loaded; 5/5 pass idle), in T-158 note. test_polish_r5 and T-097 judge tests passed this run; T-145/T-146/T-139 caused no e2e failure at HEAD. How verified: full run 1 (before edits) 9 failed 272 passed; the 3 files 61 passed; full run 2 after edits: 281 passed 2 skipped 1 failed (the T-158 mobile flake). Left: T-158 for frontend; conftest silent fallback to :7860 (T-136 r2 major 2) not touched, not in this card. Surprised: the review's 7 failures had shrunk to 3 files; logs in scratchpad t155/e2e1.txt, e2e2.txt.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:35.979Z

**tool call — Bash**
````
{
 "command": "git show --stat 20b3a42 && git log --oneline -5 && git rev-parse HEAD",
 "description": "Show commit 20b3a42 stat and recent log"
}
````

### User / tool · 2026-11-02T14:40:36.097Z

**tool result**
````
commit 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:40:12 2026 -0600

    test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 tests/e2e/test_polish_r3.py   | 12 ++++++++++--
 tests/e2e/test_rerun_judge.py |  9 +++++++--
 tests/e2e/test_stepper.py     | 19 ++++++++++++-------
 3 files changed, 29 insertions(+), 11 deletions(-)
20b3a42 test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
bf53087 fix(backend): T-146 r3 a re-run never lowers or replaces a decided item: it is kept whole with a visible note and the case reads run_partial (flag step down, summary check failed, extract down, judge down, nothing to keep)
93a2ffc fix(backend): T-141 r4 accident-date: a pre-accident record is info-only only when its accident wording is negated or explicitly prior generic history; a negator or history word no longer reaches across the, prepositions, verbs or label colons (33 reviewer variants pinned)
d34182b docs(frontend): memory notes for T-144 and T-154
25f585c fix(frontend): T-136 r3 e2e private server that fails to start stops the run with its log; never falls back to :7860
20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:38.573Z

**tool call — Bash**
````
{
 "command": "git show 20b3a42 -- tests/ | cat",
 "description": "Show full test diff for commit 20b3a42"
}
````

### User / tool · 2026-11-02T14:40:38.666Z

**tool result**
````
commit 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:40:12 2026 -0600

    test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/test_polish_r3.py b/tests/e2e/test_polish_r3.py
index 95306c8..20c71ae 100644
--- a/tests/e2e/test_polish_r3.py
+++ b/tests/e2e/test_polish_r3.py
@@ -56,6 +56,7 @@ def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
     txt = dlg.inner_text()
     assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
     page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
+    page.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('data-testid') === 'btn-shortcuts'")   # the dialog hands focus back to its opener first; focusing the row before that raced it (flaky at HEAD 078c5ae)
     # '?' from an item row opens the same sheet
     page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()
 
@@ -164,12 +165,19 @@ def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_c
 
 
 # ---- 4. density
+# T-144 (stale-test update): every entry row may now carry a collapsed "Also in this record, not in an entry (n)" list (uncovered-list, ~30-57 px with its margins). The row-height
+# budgets below (150 / 170 px at 1440, 420 px at 390) were set before it existed and still guard the row itself, so the measured height leaves that deliberate list out.
+ROW_BOXES_JS = """els => els.map(e => { const r = e.getBoundingClientRect(), u = e.querySelector('[data-testid=uncovered-list]');
+    let extra = 0; if (u) { const c = getComputedStyle(u); extra = u.getBoundingClientRect().height + parseFloat(c.marginTop) + parseFloat(c.marginBottom); }
+    return [r.top + scrollY, r.height - extra, e.getAttribute('data-state')]; })"""
+
+
 def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
     try:
         rows = pg.locator('[data-testid=queue] > article')
         assert rows.count() >= 5
-        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
+        boxes = rows.evaluate_all(ROW_BOXES_JS)
         assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
         first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
         assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
@@ -192,7 +200,7 @@ def test_row_opens_with_more_and_closes_with_less(page, sample_case):
 def test_390_needs_review_row_is_at_most_420(pw, lib09):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
     try:
-        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
+        hs = [bx[1] for bx in pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all(ROW_BOXES_JS)]
         assert hs and max(hs) <= 420, hs
         assert pg.evaluate("document.documentElement.scrollWidth") <= 391
     finally:
diff --git a/tests/e2e/test_rerun_judge.py b/tests/e2e/test_rerun_judge.py
index 36b825c..0ad04b6 100644
--- a/tests/e2e/test_rerun_judge.py
+++ b/tests/e2e/test_rerun_judge.py
@@ -261,6 +261,9 @@ def test_judge_panel_follows_the_gate_for_an_edited_item(page, sample_case):
 # ---- T-097 round 2 (D-045 b, T-098, D-047): the summary and the Why dialog read the gate and the item trace; a failing code check on an edited summary is a named blocker.
 # Since T-100 the edit route refuses wording that fails a code check, so that gate state is produced by the WordingFails route stub (conftest); everything else is the real backend.
 WORDING = "Your wording doesn't match the quote:"
+# T-134 r2 (stale-test update): an edit that passes the code checks but that she has not yet compared with the quote and accepted is `edit_to_check`; the item trace words the verdict
+# "Edited; waiting for your check" (memory/contracts/api.md, Item trace), not "Edited by you, not AI-checked" (that wording stays in the AI-check panel row and the judge step).
+EDIT_WAITING = "Edited; waiting for your check"
 
 
 def _edit(tok, i, summary):
@@ -303,6 +306,7 @@ def test_failing_edit_is_a_named_blocker_in_the_panel_summary_and_row(page, mixe
 
 
 def test_passing_edit_says_edited_by_you_not_ai_checked_everywhere(page, mixed):
+    """D-045(b) wording in the panel and the judge step; T-134 r2: the Why dialog verdict of an edit she has not yet accepted is EDIT_WAITING (edit_to_check)."""
     t = mixed
     open_case(page, t["tok"]); jp = open_judges(page)
     row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["ok"]["id"]}"]')
@@ -311,7 +315,7 @@ def test_passing_edit_says_edited_by_you_not_ai_checked_everywhere(page, mixed):
     assert jp.get_by_test_id("judge-summary-counts").inner_text().count("blocks export") == 1, "only the failing edit blocks"
     page.locator(f'[data-testid="queue"] [data-item-id="{t["ok"]["id"]}"]').get_by_test_id("entry-why").click()
     st = page.get_by_test_id("item-stepper"); st.wait_for()
-    assert st.get_by_test_id("item-verdict").inner_text() == "Edited by you, not AI-checked"
+    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING
     j = st.locator('[data-step-id="judge_1"]')
     assert j.get_by_test_id("step-status").inner_text() == "Not needed" and j.get_by_test_id("btn-rerun-judge").count() == 0
     assert "said:" not in j.inner_text() and "Unavailable" not in j.inner_text(), "T-097 r3 m-new-1: a Not-needed step prints no second-check verdict"
@@ -345,6 +349,7 @@ def test_rail_blocker_row_names_the_wording_problem_with_an_edit_button(page, mi
 
 
 def test_fixing_the_wording_clears_panel_dialog_and_rail(page, mixed):
+    """T-134 r2: once the failing wording is replaced, the Why dialog reads EDIT_WAITING (edited, not yet accepted by her), not a failure."""
     t = mixed
     _edit(t["tok"], t["bad"]["id"], t["bad"]["summary"].rstrip(".") + " as recorded.")   # any new wording ends the stub's failure, as a passing edit ends the real one
     open_case(page, t["tok"]); page.reload(); page.get_by_test_id("timeline").wait_for(); jp = open_judges(page)
@@ -353,7 +358,7 @@ def test_fixing_the_wording_clears_panel_dialog_and_rail(page, mixed):
     assert "Ready to export" in open_rail(page).get_by_test_id("case-summary-gate").inner_text()
     page.locator(f'[data-testid="queue"] [data-item-id="{t["bad"]["id"]}"]').get_by_test_id("entry-why").click()
     st = page.get_by_test_id("item-stepper"); st.wait_for()
-    assert st.get_by_test_id("item-verdict").inner_text() == "Edited by you, not AI-checked" and st.get_by_test_id("item-wording-fail").count() == 0
+    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING and st.get_by_test_id("item-wording-fail").count() == 0
 
 
 @pytest.mark.parametrize("typed,shown", [("Visit 8: pain 4/10, improving; billed $9,000.", "$9,000"), ("Pain 4/10, improving in the left arm.", "left"), ("Pain 4/10, improving.", None)])
diff --git a/tests/e2e/test_stepper.py b/tests/e2e/test_stepper.py
index c1bd50e..bd7e98e 100644
--- a/tests/e2e/test_stepper.py
+++ b/tests/e2e/test_stepper.py
@@ -18,9 +18,14 @@ def _run(tok):
     assert s["status"] == "ready"
 
 
+# D-059 (T-140 r2): code now marks "Amount due: $1,150" (record 5) as an unclear amount, and the recorded second check disagrees on it (SHOULD_BE_CHARGE), so L6 has FOUR judge
+# objections (three amounts a3, a4, a7, one flag f_r5_1), not three.
+L6_OBJECTIONS = 4
+
+
 @pytest.fixture
 def judged_case():
-    """Library L6: three judge objections (two amounts, one flag) and several code-vs-AI disagreements. Local mode only."""
+    """Library L6: four judge objections (three amounts, one flag; D-059 made the "Amount due" figure the third amount) and several code-vs-AI disagreements. Local mode only."""
     st, c = api("POST", "/api/cases", {"library": "case_lib06_lop_billed_vs_adjusted"})
     if st not in (200, 201):
         pytest.skip("library cases need ZLAYT_MODE=local")
@@ -172,7 +177,7 @@ def test_case_steps_that_need_you_have_a_working_action(page, judged_case):
         if not page.get_by_test_id("case-stepper").locator("details.zs-case-det").evaluate("d => d.open"):
             page.get_by_test_id("case-stepper").get_by_test_id("case-summary").click()
     judges = page.get_by_test_id("case-stepper").locator('[data-step-id="judges"]')
-    assert "3 items the AI objected to" in judges.get_by_test_id("step-action").inner_text()
+    assert f"{L6_OBJECTIONS} items the AI objected to" in judges.get_by_test_id("step-action").inner_text()
     assert page.locator("details.zj-det").evaluate("d => d.open")      # the jump opened the collapsed panel
 
 
@@ -182,10 +187,10 @@ def test_case_stepper_marks_failed_judges_and_links_to_panel(page, judged_case):
     j = cs.locator('[data-step-id="judges"]')
     expect(j).to_have_attribute("data-status", "fail")
     assert j.get_by_test_id("step-status").inner_text() == "Needs your decision"
-    assert "AI objected 3" in j.get_by_test_id("step-counts").inner_text()
+    assert f"AI objected {L6_OBJECTIONS}" in j.get_by_test_id("step-counts").inner_text()
     j.get_by_test_id("btn-step-action").click()
     expect(page.get_by_test_id("judge-panel").get_by_test_id("judge-totals")).to_be_visible()
-    assert page.get_by_test_id("judge-rejection").count() == 3
+    assert page.get_by_test_id("judge-rejection").count() == L6_OBJECTIONS
 
 
 def test_case_rail_has_no_developer_vocabulary(page, sample_case):
@@ -201,7 +206,7 @@ def test_judge_panel_collapsed_summary_and_labels(page, judged_case):
     open_case(page, judged_case)
     jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
     assert jp.locator("details.zj-det").evaluate("d => d.open") is False and jp.bounding_box()["height"] < 120
-    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"\d+ checked, \d+ agreed with the draft, 3 questioned"))   # counts load after the row (retrying assert, not a snapshot)
+    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(rf"\d+ checked, \d+ agreed with the draft, {L6_OBJECTIONS} questioned"))   # counts load after the row (retrying assert, not a snapshot)
     jp = open_judges(page)
     label = jp.get_by_test_id("judge-label").inner_text()
     assert "AI quality checks" in label and "not a verdict" in label
@@ -223,14 +228,14 @@ def test_judge_panel_one_row_per_item_with_record_cue(page, judged_case):
     rows = jp.locator("[data-target-item]")
     ids = rows.evaluate_all("els => els.map(e => e.getAttribute('data-target-item'))")
     assert len(ids) == len(set(ids)) and len(ids) >= 4
-    assert jp.get_by_test_id("judge-rejection").count() == 3
+    assert jp.get_by_test_id("judge-rejection").count() == L6_OBJECTIONS
     titles = jp.get_by_test_id("judge-row-title").evaluate_all("els => els.map(e => e.innerText)")
     assert len(titles) == len(set(titles)), titles
     assert all(re.search(r"Records? \d", t) for t in titles), titles
     assert any(t.startswith("Attorney referral") for t in titles)
     j = api("GET", f"/api/cases/{judged_case}/judges")[1]
     assert len(ids) == len({r["item_id"] for k in ("rejections", "unresolved", "disagreements") for r in j[k]})
-    assert "(3 items)" in jp.get_by_test_id("judge-rejections").locator("h3").inner_text()
+    assert f"({L6_OBJECTIONS} items)" in jp.get_by_test_id("judge-rejections").locator("h3").inner_text()
     rej = jp.get_by_test_id("judge-rejection").first
     assert "What you need to do" in rej.inner_text()
     assert "primary" in (rej.get_by_test_id("btn-judge-goto").get_attribute("class") or "")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:39.060Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"D-058|D-059|D-045|T-144|T-134\" memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md 2>/dev/null | head -60",
 "description": "Find decisions D-058, D-059, T-144 references"
}
````

### User / tool · 2026-11-02T14:40:39.142Z

**tool result**
````
memory/ORCHESTRATOR_DECISIONS.md:53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
memory/ORCHESTRATOR_DECISIONS.md:59:| D-051 | Code checks bind accept for **every** item (2026-11-02, T-098 review blocker): an item whose current summary fails any D-034/D-047/D-022 code check (e.g. an AI draft 'Pain 5/10' over a quote without 5/10) cannot be accepted, single or batch (422 with the reason; the paralegal must edit it to match the quote), and the export gate blocks it if such a state exists anyway. Only the judge step is exempt for human wording (D-045b); the code rung never is. | A one-click accept exported an invented number. | T-098 staff r1 F1 |
memory/ORCHESTRATOR_DECISIONS.md:66:| D-058 | A re-picked quote does not make the AI summary human-authored (2026-11-02, T-134 r3 / T-136 F-2). When she picks a different quote but keeps the AI summary, the summary is still LLM-made and its judge ran on the old quote, so D-044 still applies: the new summary–quote pair needs judge 1, and her "I compared it with the quote" does not replace it. If the judge cannot answer, the item stays out of the letter and the UI says so and names the way out (write the summary herself, which makes it human text under D-045). | The ladder rule: nothing LLM-made reaches the export without code check, independent judge and human. | T-134 r3 backend question |
memory/ORCHESTRATOR_DECISIONS.md:67:| D-059 | The letter total is built only from charges a human accepted one at a time (2026-11-02, T-140 adjuster fail). (1) Charges are never batch-accepted. (2) Code marks an amount `unclear` (not totaled, listed in internal notes with its reason) when its line or column label says total/subtotal/balance/balance forward/previous statement/year-to-date/amount due/paid/payment/adjustment/write-off/credit, when it carries a CR suffix or a negative sign, or when it comes from an insurer document (EOB/remittance) restating a provider charge. (3) Code flags a likely duplicate (same date, description and amount on two statements) and a likely total (equals the sum of other charges); such a charge can be accepted only through a confirm step that names the flag. The total line stays (R-EX-8) and sums exactly the accepted charges. | Totals from ledgers failed adversarial rounds whenever accept-all could include restated amounts; one-at-a-time acceptance plus code flags keeps the human as the final check without removing the total paralegals need. | T-140 claims-adjuster r1 |
memory/ORCHESTRATOR_DECISIONS.md:68:| D-060 | Amends D-059 (2026-11-02, T-140 adjuster r2): charge candidates are **default-deny**. An amount can be class `charge` only when it sits on an itemized service line: a date of service, a service description (CPT/HCPCS/revenue code or a service noun) and the amount on the same line or table row, in a provider bill or ledger. Every other amount (statement-level labels, account summaries, 'last statement', year-to-date, payment history, insurer documents, unlabeled figures) is `unclear` with its reason. Duplicates are matched on normalized date of service + service + amount (any date format). A charge cites its own line by offset, never by text search. | Deny-lists of total/balance wording lost every adversarial round; listing what a charge must look like cannot be outworded. | T-140 claims-adjuster r2 |
memory/DECISIONS.md:154:  - **Edit re-check order (R-RV-3, D-006):** (1) structure, else 422. (2) Code token check (ADR-012, widened by D-047 to sides, negations and qualifiers). A miss is a hard `422 invalid_edit`; nothing is saved; there is no confirm or `keep_my_wording` path (ADR-019). (3) Judge 1 re-runs against the edited text. If it objects (`partially`/`unsupported`): the edit is saved as `needs_review` with a warning; the judge never blocks a human-written edit (D-045b, ADR-019). If the judge fails (error, timeout) or there is no recorded fixture for the edit (always the case in demo mode): the edit is saved and the item becomes `needs_review` with `JUDGE_UNAVAILABLE`, shown to her; the code check already passed. The judge never blocks the edit and never lets an unchecked edit look verified.
memory/DECISIONS.md:350:  3. **Edits and manual entry (D-034, D-047).** Side (left/right), negation (no/not/without) and qualifier tokens that the quote does not carry are a hard `422 invalid_edit`, the same as numbers. The `409 needs_confirm` / `keep_my_wording` path is removed (no such event is written). A judge objection never blocks a human-written edit (D-045b): it is a warning and the item stays `needs_review`.
memory/DECISIONS.md:351:  4. **Code checks bind accept (D-051).** Every accept, single or batch, recomputes the code checks on the wording it would leave. A failure is `422 CODE_CHECK_FAILED` and nothing is written. The judge is not re-run for human wording (D-045b); the code rung always runs.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:41.590Z

**tool call — Bash**
````
{
 "command": "grep -rn -E \"T-144|uncovered-list|Also in this record\" memory/ docs/ spec/ app/frontend 2>/dev/null | head -40; echo ---; grep -n -E \"edit_to_check|waiting for your check|Edited by you\" memory/contracts/api.md app/backend/*.py 2>/dev/null | head -30; echo ---; python3 tools/board.py show T-158 2>&1 | head -60; echo ---; python3 tools/board.py show T-144 2>&1 | head -40",
 "description": "Grep T-144, uncovered-list, verdict wording and cards T-158/T-144"
}
````

### User / tool · 2026-11-02T14:40:41.809Z

**tool result**
````
memory/PROGRESS.md:43:- 2026-11-02T13:03:50Z orchestrator: GATE-M2 round 1 failed (adjuster + paralegal blockers on billing in letter/totals; nurse + qa majors). Fix cards T-139..T-144 in flight; re-gate after fixes + confirming live 3-run.
memory/PROGRESS.md:46:- 2026-11-02T14:14:33Z heartbeat: 86.9%, inbox empty, 0 stalled, reviews dispatched; M2 re-gate waits on T-139 r2, T-140 r2 reviews, T-141 r3, T-144, T-152, T-154 + confirming live run; T-149 multi-case UI finishing.
memory/contracts/api.md:138:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
app/frontend/uncovered.css:1:/* T-144: the collapsed "Also in this record, not in an entry (n)" list under an entry. Tokens only. */
app/frontend/uncovered.js:1:/* T-144: "Also in this record, not in an entry (n)" under each entry. Shows records[].uncovered[] (T-143: every sentence of the record that no live entry quote overlaps, computed by code),
app/frontend/uncovered.js:19:    const full = `Also in this record, not in an entry (${n})`;
app/frontend/uncovered.js:21:    const panel = el("section", { class: "unc", id, hidden: !opened.has(entry.id) || null, "data-testid": "uncovered-list", "data-record-count": String(n), "aria-label": full + ": " + who },
---
memory/contracts/api.md:365:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
memory/contracts/api.md:366:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
memory/contracts/api.md:370:- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.", and the item `verdict` is `{code: "edit_to_check", label: "Edited; waiting for your check"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / "Accepted by you". A verified edit (state not `needs_review`) still reads "You edited this item and accepted it.". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).
memory/contracts/api.md:372:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summary (`edit_to_check` with no second-check answer) the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning (and the passing gate headline that repeats it) and the case `review` step all use one clause: "... accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words." It is conditional on purpose: before she accepts, the gate passes and nothing is blocked (the entry is only left out); D-044 blocks only after accept. After `POST /rejudge` leaves an accepted item unavailable, its `JUDGE_NOT_RUN` blocker carries `rerun_no_answer: true` and a `why` that says the check ran again and gave no answer; the 422 `judge_not_run` message then says what clears it instead of repeating "Run the second check again"; the failing `export_gate` headline is the same sentence as that 422 message (one function, `trace.judge_not_run_message`). **T-134 r4:** `rerun_no_answer` describes the CURRENT wording and quote: any edit that replaces the second-check result (`ladder.judge`) also drops `ladder.rejudge` (the attempts belonged to the old quote), and an undo restores the attempts the old wording had, so a re-picked quote reads "Run the second check again" until that check has been run on it. **`second_check_pending` (bool, every entry, amount and flag view, in `GET /api/cases/{token}` and every review response `item`):** true when the item is live (not rejected, not dismissed), AI-made (not a manual entry or a summary she wrote, D-045b), its second check has no answer, and it is not a rate (accepting a rate only acknowledges it). It is the same list the `JUDGE_NOT_RUN` gate reads, whether or not she has accepted it yet; it is false after the check answers. The UI uses this field instead of inferring it from `ladder.judge` or `reasons`. Show `why` as given.
memory/contracts/api.md:374:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
memory/contracts/api.md:705:**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
app/backend/case_list.py:159:            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "edits_to_check": counts["edit_to_check"],
app/backend/present.py:58:            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter
app/backend/present.py:230:    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
app/backend/present.py:235:            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
app/backend/trace.py:289:        code, label = "edit_to_check", "Edited; waiting for your check"
app/backend/trace.py:1097:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
app/backend/trace.py:1101:    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
app/backend/trace.py:1102:        n = rc["edit_to_check"]
app/backend/trace.py:1115:    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
app/backend/trace.py:1180:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
---
---
id: "T-158"
title: "Flaky ~50% at 390x844: after a refused Accept the reason box (accept-refused) sometimes ends below the fold (T-119 r3 promise); tests/e2e/test_code_check_refusal.py mobile cases"
milestone: "M2"
role: "frontend"
status: "ready"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:39:57Z"
updated_at: "2026-11-02T14:40:30Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "after a refused Accept at 390x844 the accept-refused box is fully inside the viewport after layout settles, 10 consecutive runs of tests/e2e/test_code_check_refusal.py 0 failed (E2E_REQUIRE_DB=1)", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:40:08Z qa: Repro: E2E_REQUIRE_DB=1 pytest tests/e2e/test_code_check_refusal.py (private server, HEAD 078c5ae) fails 3 of 6 runs on [real|stub]-390-844 'the reason must be on screen beside the button, not below the fold'. Probe: open sample case at 390x844, scroll first verified pending entry into view, click Accept (route-stubbed 422): final scrollY varies run to run (690..851) and accept-refused spans y=805..937 > 844 in half the runs; nothing scrolls after layout settles. Also seen once under load: test_rerun_judge.py::test_rerun_pressed_in_the_refused_export_message_answers_beside_the_button[1440-900] got 'Running the second check…' without the count (stepper.js S.rejudge: n from jnrBlockers(gateOf(cache)) was 0 because the trace cache was not loaded when the button was pressed); 5 of 5 pass on an idle machine.
- 2026-11-02T14:40:30Z orchestrator: assigned: frontend

## Handoff (filled when moving to in_review)

---
---
id: "T-144"
title: "UI: show record.uncovered[] as 'Also in this record, not in an entry' under each entry's source, one click to the sentence (legal-nurse GATE-M2 major 2 UI half)"
milestone: "M2"
role: "frontend"
status: "done"
priority: "P1"
depends_on: ["T-143"]
created_by: "orchestrator"
created_at: "2026-11-02T13:03:14Z"
updated_at: "2026-11-02T14:38:44Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T13:58:12Z"
rounds: 0
commits: ["ded5ca4", "f262223"]
reviews:
  - {"persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5", "verdict": "pass", "file": "reviews/T-144-legal-nurse.md", "at": "2026-11-02T14:38:44Z"}
ac:
  - {"n": 1, "text": "each entry with uncovered clinical sentences shows a collapsed list with the verbatim sentences and a jump to the highlighted source; e2e on lib09", "done": true, "evidence": "tests/e2e/test_uncovered_ui.py 7/7 on lib09 (+ sample for letter/copy); polish_r3 row-height specs pass"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:03:19Z orchestrator: assigned: frontend
- 2026-11-02T13:58:12Z frontend: claimed
- 2026-11-02T14:05:18Z frontend: uncovered.js/css built; tests/e2e/test_uncovered_ui.py 7/7 on lib09 + sample on own server; full e2e + unit running.
- 2026-11-02T14:30:53Z frontend: AC 1 checked: tests/e2e/test_uncovered_ui.py 7/7 on lib09 (+ sample for letter/copy); polish_r3 row-height specs pass
- 2026-11-02T14:30:53Z frontend: moved in_progress -> in_review
- 2026-11-02T14:30:56Z orchestrator: review dispatched: legal-nurse-reviewer
- 2026-11-02T14:38:44Z orchestrator: review legal-nurse-reviewer (claude-sonnet-5-5): pass — reviews/T-144-legal-nurse.md
- 2026-11-02T14:38:44Z orchestrator: moved in_review -> done

## Handoff
What changed: app/frontend/uncovered.js + uncovered.css; a registerRowActions hook adds a 'Not in an entry (n)' link in the entry head that opens 'Also in this record, not in an entry (n)': verbatim sentences from records[].uncovered[], 'Show in record' opens the source modal on that sentence (ZL.openSource by API offsets). Never in letter/notes/copy. List re-read from GET case when an entry's quote or state changes. Closed by default; kinds never used. · Verified: tests/e2e/test_uncovered_ui.py 7/7 (lib09: count, verbatim, jump+highlight, keyboard, 390px, quote change refresh, sample letter+clipboard); full e2e on own port: only failures are others' (polish_r3 first-entry y 552>520 from T-149 overview block; rerun_judge 2x 'Edited; waiting for your check'). · Left: none. · Surprised: a link in the row's link bar or a <details> line broke T-060's compact-row height specs, so the link lives in the head line; port 7961 was another worker's server (mine silently died).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:03.532Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat feedback_verify_pid_before_kill.md feedback_shared_scratchpad.md project_round2_snapshot_review_patterns.md project_t136_r2_patterns.md project_t145_t146_patterns.md project_t134_r4_t138_r2_patterns.md feedback_frontend_text_coupling.md 2>&1 | head -220",
 "description": "Read relevant recorded memory patterns"
}
````

### User / tool · 2026-11-02T14:41:03.621Z

**tool result**
````
---
name: feedback_verify_pid_before_kill
description: a PID captured with $! from a subshell can be a wrapper, not the server; run ps -p and lsof on the port before kill, and kill the listener, not the recorded number
metadata:
  type: feedback
---

Before killing a server, check the PID you recorded with `ps -o pid,ppid,command -p <pid>` and check the listener with `lsof -iTCP:<port> -sTCP:LISTEN -n -P`. Kill the listener and confirm the port is closed.

**Why:** T-119 r3 (this session): I wrote `echo $!` from a subshell that started `nohup python -m app.main &`. The recorded PID (6353) was a bash wrapper, not the server. I killed it without checking. The real server (6354) stayed up and had to be stopped by its listener PID. The ports were closed only after that second kill.

**How to apply:** when a review starts its own servers, record the listener PID with lsof after the health check, not `$!`. Stop only PIDs whose command line shows the app, and verify both ports closed afterwards. If a wrong PID was killed, say so in the review's exercised list.

Related: [[project_t119_keyboard_coverage_patterns]], [[feedback_shared_scratchpad]].
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
---
name: round2-snapshot-review-patterns
description: T-040 r2 and T-043 r2 (2026-11-01): HEAD moves mid-review, git archive needs untracked fixtures, mutation method, guard traps, overwritten review file
metadata:
  type: project
---

Round-2 reviews of T-040 (security) and T-043 (paralegal) ran while other agents committed to the same branch. HEAD moved about six times in one session (5542dfd -> 700ca9a -> 7364096 -> 7a450a1 -> 5216d06 -> 099732b -> dd545e3 -> c61e84f).

**Why:** A test result or live check is only valid for the hash it ran against. Quote the hash in every review, and re-run the required command at the end of the review.

**How to apply:**
- Snapshot the reviewed commit with `git archive <sha> | tar -x -C <scratch>`, then copy untracked files in (`git ls-files --others --exclude-standard`, through a small Python copier because BSD `cp` has no `--parents`). `.gitattributes` has no export-ignore, but a commit can lack files that a later commit adds. 077e294 lacks `tests/fixtures/llm/*.json` (added by 0d040d3), so `FIXTURE_MISS` fails 7 tests. Overlaying HEAD's fixtures isolates the code question from the fixture-ordering question.
- Mutation checks run in a scratch copy via a Python driver (`mutate_api.py` pattern in artifacts/review-evidence/T-040-r2-mutate_api.py). Result shape: drop the delete_case line, drop the CSP line, disable the Content-Length precheck. A test that still passes with the control removed is a finding (here the body-cap test).
- Live checks: start uvicorn from the snapshot with DATA_DIR in scratch, get listener PIDs with `lsof -nP -iTCP:<port> -sTCP:LISTEN`, and kill those PIDs by number. A PID file from `nohup ... &` in a subshell can point at a dead parent.
- Guard traps (board-guard / git-guard in this repo): `kill $(cat ...)` is denied (command substitution in command position); `rm -rf "$VAR/..."` is denied; `awk` with `>` or `NR>1` is read as a redirect into a product path; `grep "<style"` is read as redirect; a `2>&1 | tail` inside an echo string is denied. Put shell logic in a scratch .py file and run it with `.venv/bin/python -I`.
- Overwrite hazard: `Write` on an existing reviews/ file replaces it silently. Before writing `reviews/<card>-<persona>-r2.md`, check for an existing file and the card's reviews list (`board show <card>`). An earlier round-2 review for T-040 existed (verdict changes, 02:17:03Z) and was overwritten; it was untracked, so it could not be restored from git.
- Fixes can land between a review's findings and its re-check: at c61e84f the PDF route moved to a threadpool with a 10 s cap and a demo refusal before parse. Re-measure any performance claim on the current HEAD before rating it.
---
name: t136-r2-patterns
description: T-136 r2 (HEAD 07c7558): private-server fallback to :7860, red e2e suite predating the card, flaky mobile and open_rail tests, client copy of a server gate rule
metadata:
  type: project
---

T-136 r2 review (reviews/T-136-staff-engineer-r2.md, verdict changes: 0 blockers, 2 majors, 2 minors).

- **Fall-through in a start-your-own-server harness.** tests/e2e/conftest.py pytest_configure returned silently when its private server failed to start or did not answer in 80 tries, leaving BASE at localhost:7860. A plain run then ran against the shared dev app and reported green with skips. Repro: prepend sys.exit(3) to app/main.py in a scratch copy. Check any "start my own server" helper for paths that keep the default URL.
- **Attribution run was invalid at first.** Archiving an older commit (d19ae46) with the old conftest hit the shared :7860 app and skipped 30 DB specs. Re-run old commits against your own server with E2E_REQUIRE_DB=1, and check which server the run actually hits before attributing failures.
- **Red suite that predates the card.** Seven deterministic e2e failures (polish_r5 row reasons, rerun_judge x2, stepper x4) fail on d19ae46 too, so the card's frontend diff is not the cause. The card still cannot claim a pass on a red suite.
- **Flakes.** Mobile refusal test (code_check_refusal 390x844) failed in 2 of 3 plain runs on the same commit. The card's own gate-warning test failed once in 5 runs; open_rail does a read-then-click on details.open (test_stepper.py:35-36).
- **Duplicated gate rule.** dom.js:55 decides "export stays blocked" from reasons containing JUDGE_UNAVAILABLE; trace.py:807 ai_summary_unchecked decides it on the server. They differ on judge verdict None or "".

**Why:** these four patterns (fall-through, invalid attribution, red-before-card, read-then-click) recur across cards; check for them first.
**How to apply:** when a card claims "N fail identically at HEAD", archive its parent and run the same files against your own server before accepting the attribution; run the same file twice before calling a test deterministic.

Related: [[project_e2e_contract_review_patterns]], [[project_harness_review_patterns]].
---
name: t145-t146-patterns
description: T-145 b604ff2 pass, T-146 7d3ca35 changes - shared reason sentence labels two cases, "failed re-run" AC covers only the timeout path, snapshot tests compare state only
metadata:
  type: project
---

T-145 (deadline leaves entries verified) pass: `_mark_judge_not_run` call-site patch; 6/6 mutants killed. Minor: the "JUDGE_NOT_RUN:" prefix sits on the shared JUDGE_UNAVAILABLE sentence, so a judge that ran and failed (ladder reason NONE, model set) prints it too. compose_state still treats judge None as clean.
T-146 (timed-out re-run) changes: `_persist(additive=timed_out)` is right for timeouts, but a done_with_errors re-run (extract LLMFailed) still replaces accepted entries with summary=None stubs and the case stays `ready`, error None (`done_with_errors` is never stored). Tests snapshot only (review_status, state, reasons) and never the message; summary-null and old-message mutants survive.

**How to apply:** for "keeps earlier results" fixes, probe every non-happy re-run status (timeout, done_with_errors, judge-down), not just the one named; compare full rows, and mutate the message text. Files: reviews/T-145-staff-engineer.md, reviews/T-146-staff-engineer.md. Errata: the T-146 file cites pipeline.py:244-247 for the replace path; it is :250 (write-once, not edited).
---
name: project_t134_r4_t138_r2_patterns
description: T-134 r4 4f416a4 and T-138 r2 b7a7ead (scoped 7.4 checks): backend wording fixed but UI regex keeps the old 'stays blocked' sentence; "second pick" test re-saves identical text; alias and leak controls; HEAD moved mid-review
metadata:
  type: project
---

T-134 r4 (4f416a4, changes) and T-138 r2 (b7a7ead, pass), scoped 7.4 check on `git archive`.

- Backend wording for the open re-picked quote now matches D-058 in every surface I probed (review step, gate headline == 422 message, item step, EDIT_NOT_CONFIRMED warning). The UI did not follow: `app/frontend/review.js:191` swaps in the server's `why` only if it matches `/export stays blocked/`, so the r4 rewording silently left the fallback `AI_HELD` (review.js:182, "export stays blocked") on the card while the gate passes. A backend-only fix passed every backend test. Lesson: when a backend sentence changes, grep the frontend for the old phrase AND for regexes over it (see [[feedback_frontend_text_coupling]]).
- The "second pick" test used `QUOTE_ONLY.strip()`, which equals the AI's own excerpt after the server's strip, so it re-saved identical text. On the sample with the AI summary kept, the other candidates fail the number or attribution check (only the first two sentences pass; the second sentence alone was not run). Mutant P1 (drop `ladder.rejudge` on edit removed) died, so the behaviour is protected; the test's description was wrong. Check that a "re-pick" changes the stored text before calling it one.
- Rerun claim currency works: identical re-save drops `ladder.rejudge` and the claim; a new rerun brings it back.
- T-138 alias fixed with `copy.deepcopy`. Control on the parent 68b8685 shows `RESTORED False`, HEAD shows True: the probe discriminates. Leak scan: 48 GET + 3 review responses clean at HEAD, `pre_edit` present on the parent control.
- Mutants on the same 7 modules: N18, N19 (anchor moved; the r3 N19 anchor now SKIPs), N21, N22, H2, P1, A1, T3, T9, L1 all killed.
- Pre-existing red test on HEAD: `tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted` (`['e2','e4'] == []`), from the T-139 hold-out (5f7ef96, 184cbb7). Same at 68b8685. Not this card's; reported as out of scope.
- HEAD moved (4f416a4 to 2db6ad2) during the review. `present._why` and `_common` changed upstream; re-ran the card tests, probe and leak scan on the new archive, same results.
- Reviews are write-once: I wrote the r4 and r2 files, then found errors (a pin claim that present.py was not touched, a "no other valid quote" overclaim, and an empty nit entry). Edit was refused by reviewer-write-guard, so corrections went into `-r4b` and `-r2b` files. Proof-read every "I did not touch X" claim with `git diff --stat` before the first Write.
- Method: the bash cwd can be the repo root, so a `mkdir "$PWD/..."` hit board-guard. Use absolute scratchpad paths. The mutant runner can use `--deselect` for a known red test; without it every mutant reports KILLED.

**Why:** the card round was a bounded fix-up, the verdict depends on whether the fix reached the UI, and the orchestrator's acceptance text named the exact sentence.
**How to apply:** for any D-058-style wording card, probe the item step, the gate, the 422 AND the frontend constants; for any "re-pick" test, assert the stored text changed.

See [[project_t134_unconfirmed_edit_patterns]], [[project_t134_r3_t138_patterns]], [[feedback_review_write_once]].
---
name: feedback_frontend_text_coupling
description: when a backend changes a user-facing sentence, grep app/frontend for the old phrase and for regexes over it; a server-text swap keyed to old wording silently keeps the frontend fallback
metadata:
  type: feedback
---

When a card rewords a sentence the UI shows, check the frontend for (a) the old literal phrase in fallback constants and (b) any regex or `includes` that decides whether to swap in the server's text. A backend-only test passes while the screen keeps the old fallback.

**Why:** T-134 r4 (4f416a4): the backend reworded the held-edit sentence to a conditional and dropped "stays blocked". `app/frontend/review.js:191` only swapped in the server's text when `/export stays blocked/` matched, so the fallback `AI_HELD` (review.js:182) that says "the export stays blocked" stayed on the card while the gate passed. The backend unit tests were green.

**How to apply:** `grep -rn "<old phrase>" app/frontend app/backend` and `grep -rn "test(" app/frontend | grep -i <phrase>` before accepting a wording fix. Probe the item's JSON for the same state and run the frontend regex over it (python `re` gives the same answer for these literals). Prefer an explicit server flag over a regex on text (the T-134 r4 `second_check_pending` field exists for this; the UI does not read it yet).

Related: [[project_t134_r4_t138_r2_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:04.195Z

**tool call — Bash**
````
{
 "command": "git status --short | head -40; echo \"---ignored-relevant\"; git status --ignored --short | head -40; echo \"---conftest\"; ls tests/e2e | head -80; echo; sed -n 1,200p tests/e2e/conftest.py",
 "description": "Check working tree state and e2e conftest"
}
````

### User / tool · 2026-11-02T14:41:04.888Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:07.387Z

**tool call — Bash**
````
{
 "command": "ls tests/e2e; echo ---; sed -n 1,140p tests/e2e/conftest.py",
 "description": "List e2e directory and read conftest"
}
````

### User / tool · 2026-11-02T14:41:07.470Z

**tool result**
````
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charge_confirm.py
test_charges.py
test_code_check_refusal.py
test_conflict_coverage.py
test_conflict_skipped.py
test_edit.py
test_edit_to_check.py
test_export_ui.py
test_flags_panel.py
test_held_quote_gate.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_multicase.py
test_polish_r3.py
test_polish_r4.py
test_polish_r5.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
test_uncovered_ui.py
---
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
T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
T-136 r3 (tests/e2e/test_held_quote_gate.py): btn-write-summary-case ('Write the summary' on the case-level places: the 'Ready to export?' and 'Second AI check' steps of the case rail and the 'How the AI was checked' rows; opens the entry's summary box like the blocker row's btn-gate-write-summary). A held re-picked quote offers btn-rerun-judge only until a rerun gave no answer (the blocker's rerun_no_answer).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
  edit-check-hint (a reworded entry that is still marked Needs review: its btn-accept reads 'I compared it with the quote'; the row carries data-edit-check; it counts as open in the header, todo-list ('1 edit to check') and the copy-confirm),
  letter-style (fieldset in the export panel) with letter-style-standard / letter-style-oneline radios (T-121: ?style=oneline), tray-filtered (collapsed <details> 'Filtered by rule (n)', D-057) with tray-filtered-summary,
  tray-filtered-rule (one per rule, data-rule) and tray-filtered-item; data-group = the list a row sits in (flag kind on the flag sections, 'charges' / 'unclear-amounts' on the amount tables): a / d move only inside it.
  T-136: btn-edit-excerpt ('Change quote' on an entry row; opens excerpt-editor), btn-copy-cancel ('Go back' in copy-confirm), edit-compare-prompt (a visible line under the edit-check hint after the a key was pressed on an edit that still waits for her comparison: 'Not recorded yet ...'; a never records it, the btn-accept 'I compared it with the quote' does),
  dismissed-group-flags / dismissed-group-amounts (a <details> at the end of the Flags / Charges panel, 'Dismissed (n)', rows keep Undo; opens for the item just dismissed) with dismissed-summary-flags / dismissed-summary-amounts, dismissed-flags (rows) and dismissed-amounts (table).
  A dismissed flag / amount / entry has NO btn-accept and no btn-edit (state word 'Dismissed' + btn-reset 'Undo'); entry-date is a <time datetime="YYYY-MM-DD"> showing the long date.
T-144: uncovered-summary (a link 'Not in an entry (n)' in an entry row's link bar; aria-expanded), uncovered-list (the list 'Also in this record, not in an entry (n)', hidden until opened; data-record-count), uncovered-heading (its full wording), uncovered-item (one <li> per sentence, data-record-id), uncovered-text (the verbatim sentence, read-only), btn-uncovered-jump ('Show in record': opens the source record with that sentence highlighted). Never in the letter, the notes or the copy text. data-entry-id = the entry id on an entry row (specs find a row by it); data-flag = the flag key (likely_duplicate | likely_total) on charge-flag; T-144's data-record-count is the number of sentences in uncovered-list.
T-154 (tests/e2e/test_charge_confirm.py): charge-flag (the flag name + the server's sentence in a charge row's Status cell), charge-confirm (the confirm <dialog> before a flagged charge is accepted; role dialog, Cancel focused), charge-confirm-flag (the flag's name inside it), charge-confirm-msg (the server's sentence), btn-charge-confirm ('Confirm <flag> and accept'), btn-charge-cancel, batch-charges-note (batch bar: 'Charges are accepted one at a time').
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_PRIVATE = {}


def pytest_configure(config):
    """T-136 r2 (staff review F1): a plain `pytest tests/e2e` must RUN the specs that write to the server's SQLite file (ZLAYT_DB: test_edit_to_check, test_code_check_refusal, test_change_the_quote,
    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
    global BASE
    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
        return
    import atexit, shutil, socket, subprocess, sys, tempfile, time
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"

    def fail(why):
        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
        if proc.poll() is None:
            proc.kill()
        log.close()
        try:
            tail = open(os.path.join(tmp, "server.log")).read()[-2000:]
        except OSError:
            tail = ""
        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)

    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            if proc.poll() is not None:
                fail(f"exited with code {proc.returncode} before it answered")
            time.sleep(0.5)
    else:
        fail("did not answer /api/health within 40 seconds")
    if proc.poll() is not None:
        fail(f"exited with code {proc.returncode} right after it answered")
    _PRIVATE.update(proc=proc, tmp=tmp)
    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
    def stop():
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close(); shutil.rmtree(tmp, ignore_errors=True)
    atexit.register(stop)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:08.230Z

**tool call — Bash**
````
{
 "command": "git ls-files --others --exclude-standard | grep -v '^\\.claude/' | grep -v '^board/' | head -60; echo \"--- count:\"; git ls-files --others --exclude-standard | wc -l; echo \"--- HEAD sha:\"; git rev-parse HEAD; echo \"--- lsof 7860:\"; lsof -nP -iTCP:7860 -sTCP:LISTEN 2>/dev/null | head -5",
 "description": "List untracked files, HEAD sha, and check port 7860 listener"
}
````

### User / tool · 2026-11-02T14:41:09.248Z

**tool result**
````
artifacts/review-evidence/GATE-M2-paralegal/draft.md
artifacts/review-evidence/GATE-M2-paralegal/g1-analyzed-full.png
artifacts/review-evidence/GATE-M2-paralegal/g1-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g1-landing.png
artifacts/review-evidence/GATE-M2-paralegal/g1.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g1.py
artifacts/review-evidence/GATE-M2-paralegal/g2-shortcuts.png
artifacts/review-evidence/GATE-M2-paralegal/g2.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g2.py
artifacts/review-evidence/GATE-M2-paralegal/g3-after-entries.png
artifacts/review-evidence/GATE-M2-paralegal/g3-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g3-edit-open.png
artifacts/review-evidence/GATE-M2-paralegal/g3-edit-saved.png
artifacts/review-evidence/GATE-M2-paralegal/g3-start.png
artifacts/review-evidence/GATE-M2-paralegal/g3.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g3.py
artifacts/review-evidence/GATE-M2-paralegal/g4.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g4.py
artifacts/review-evidence/GATE-M2-paralegal/g4b.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g5-change-quote-e3.png
artifacts/review-evidence/GATE-M2-paralegal/g5-open-record-e3.png
artifacts/review-evidence/GATE-M2-paralegal/g5.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g5.py
artifacts/review-evidence/GATE-M2-paralegal/g6-after-reload.png
artifacts/review-evidence/GATE-M2-paralegal/g6-after-review.png
artifacts/review-evidence/GATE-M2-paralegal/g6-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g6-e3-edited.png
artifacts/review-evidence/GATE-M2-paralegal/g6-reload-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g6.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g6.py
artifacts/review-evidence/GATE-M2-paralegal/g7-A-unconfirmed-edit-export.png
artifacts/review-evidence/GATE-M2-paralegal/g7-A-unconfirmed-edit-letter.txt
artifacts/review-evidence/GATE-M2-paralegal/g7-A-unconfirmed-edit-notes.txt
artifacts/review-evidence/GATE-M2-paralegal/g7.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g7.py
artifacts/review-evidence/GATE-M2-paralegal/g8-clipboard.txt
artifacts/review-evidence/GATE-M2-paralegal/g8-export-final.png
artifacts/review-evidence/GATE-M2-paralegal/g8-letter.txt
artifacts/review-evidence/GATE-M2-paralegal/g8-notes.txt
artifacts/review-evidence/GATE-M2-paralegal/g8.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g8.py
artifacts/review-evidence/GATE-M2-paralegal/g9-letter.txt
artifacts/review-evidence/GATE-M2-paralegal/g9.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g9.py
artifacts/review-evidence/GATE-M2-paralegal/gh.py
artifacts/review-evidence/GATE-M2-paralegal/l1-body.txt
artifacts/review-evidence/GATE-M2-paralegal/l1-lib11-full.png
artifacts/review-evidence/GATE-M2-paralegal/l1.out.txt
artifacts/review-evidence/GATE-M2-paralegal/l1.py
artifacts/review-evidence/GATE-M2-paralegal/l2-order.txt
artifacts/review-evidence/GATE-M2-paralegal/l2.out.txt
artifacts/review-evidence/GATE-M2-paralegal/l2.py
artifacts/review-evidence/GATE-M2-paralegal/l3-after-review.png
artifacts/review-evidence/GATE-M2-paralegal/l3-body.txt
artifacts/review-evidence/GATE-M2-paralegal/l3.out.txt
artifacts/review-evidence/GATE-M2-paralegal/l3.py
artifacts/review-evidence/GATE-M2-paralegal/l4-export-all6.png
artifacts/review-evidence/GATE-M2-paralegal/l4-letter-all6.txt
artifacts/review-evidence/GATE-M2-paralegal/l4-notes-all6.txt
artifacts/review-evidence/GATE-M2-paralegal/l4.out.txt
--- count:
  109424
--- HEAD sha:
20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
--- lsof 7860:
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  20423 arsis    9u  IPv4 0xe79fb86e4f7049c5      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:19.760Z

**tool call — Bash**
````
{
 "command": "git ls-files --others --exclude-standard -- app tests evals tools docs spec memory/contracts | head -30; echo \"--- ignored under app/tests/evals:\"; git ls-files --others --ignored --exclude-standard -- app tests evals | head -20; echo \"--- venv:\"; ls -la .venv/bin/python 2>&1; .venv/bin/python -c \"import playwright, pytest, fastapi; print('ok')\" 2>&1 | tail -1; echo \"--- archive dir:\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la \"$S\" 2>&1 | head -20",
 "description": "Check untracked product files, venv, and scratchpad state"
}
````

### User / tool · 2026-11-02T14:41:20.248Z

**tool result**
````
evals/reports/20261102T023155Z.md
evals/reports/20261102T023203Z.md
evals/reports/20261102T023204Z.md
evals/reports/20261102T023208Z.md
evals/reports/20261102T023603Z.md
evals/reports/20261102T023911Z.md
evals/reports/20261102T023916Z.md
evals/reports/20261102T024348Z.md
evals/reports/20261102T024355Z.md
evals/reports/20261102T024653Z.md
evals/reports/20261102T024822Z.md
evals/reports/20261102T025055Z.md
evals/reports/20261102T025526Z.md
evals/reports/20261102T030405Z.md
evals/reports/20261102T031209Z.md
evals/reports/20261102T032024Z.md
evals/reports/20261102T043845Z.md
evals/reports/20261102T051136Z.md
evals/reports/20261102T052638Z.md
evals/reports/20261102T052716Z.md
evals/reports/20261102T060623Z.md
evals/reports/20261102T062420Z.md
evals/reports/20261102T063158Z.md
evals/reports/20261102T090501Z.md
evals/reports/20261102T090958Z.md
evals/reports/20261102T093020Z.md
evals/reports/20261102T093441Z.md
evals/reports/20261102T094757Z.md
evals/reports/20261102T094902Z.md
evals/reports/20261102T095147Z.md
--- ignored under app/tests/evals:
app/__pycache__/__init__.cpython-312.pyc
app/__pycache__/main.cpython-312.pyc
app/__pycache__/pipeline.cpython-312.pyc
app/backend/__pycache__/__init__.cpython-312.pyc
app/backend/__pycache__/amounts.cpython-312.pyc
app/backend/__pycache__/api.cpython-312.pyc
app/backend/__pycache__/billing.cpython-312.pyc
app/backend/__pycache__/calibration_route.cpython-312.pyc
app/backend/__pycache__/case_extras.cpython-312.pyc
app/backend/__pycache__/case_list.cpython-312.pyc
app/backend/__pycache__/charge_text.cpython-312.pyc
app/backend/__pycache__/confidence.cpython-312.pyc
app/backend/__pycache__/conflict_candidates.cpython-312.pyc
app/backend/__pycache__/conflicts.cpython-312.pyc
app/backend/__pycache__/credibility.cpython-312.pyc
app/backend/__pycache__/date_convention.cpython-312.pyc
app/backend/__pycache__/dates.cpython-312.pyc
app/backend/__pycache__/dismissal_patterns.cpython-312.pyc
app/backend/__pycache__/export.cpython-312.pyc
app/backend/__pycache__/export_routes.cpython-312.pyc
--- venv:
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
ok
--- archive dir:
total 343808
drwx------@ 1411 arsis  wheel    45152 Nov  2 08:40 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
drwxr-xr-x@    6 arsis  wheel      192 Nov  2 08:00 .pytest_cache
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
-rw-r--r--@    1 arsis  wheel     6786 Nov  2 07:36 CLAUDE.md
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
-rw-r--r--@    1 arsis  wheel    83742 Nov  2 07:36 MASTER_PROMPT.md
-rw-r--r--@    1 arsis  wheel     2046 Nov  1 19:21 T-047-run1.json
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 04:04 T-060-pass2-head
drwxr-xr-x@   23 arsis  wheel      736 Nov  2 00:41 T-093-r3-2ab7896
-rw-r--r--@    1 arsis  wheel    74715 Nov  2 00:41 T-093-r3-run.py.orig
drwxr-xr-x@    3 arsis  wheel       96 Nov  2 00:41 T-093-r3-scripts
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:13 T-093-r4-3223e50
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:25.579Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/T155_r1/head\" && cd /Users/arsis/zlayt-pm-project && git archive -o \"$S/T155_r1/head.tar\" 20b3a42 && tar -xf \"$S/T155_r1/head.tar\" -C \"$S/T155_r1/head\" && rm \"$S/T155_r1/head.tar\" && cd \"$S/T155_r1/head\" && ls && echo \"--- untracked product-needed check:\" && cd /Users/arsis/zlayt-pm-project && git ls-files --others --exclude-standard -- app tests spec docs memory/contracts evals/golden tools | head; echo \"--- diff snapshot vs HEAD tracked files count:\"; git -C /Users/arsis/zlayt-pm-project ls-tree -r --name-only 20b3a42 | wc -l; find \"$S/T155_r1/head\" -type f | wc -l",
 "description": "Archive clean HEAD 20b3a42 into my scratch dir"
}
````

### User / tool · 2026-11-02T14:41:26.563Z

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
--- untracked product-needed check:
tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
tests/fixtures/llm/0cda4d86d157a3de853406a613c709da25988add2f9978c0c6daf9533cb39d52.json
tests/fixtures/llm/0d6d2c00c56c049235405220c600effe905ad5155138aaeecb6ef264da4bf225.json
tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
tests/fixtures/llm/23a42e78f6f5e66dfaeda880459bbbbf14d34b4945c40aca56c2d0bd19babf84.json
tests/fixtures/llm/249e2de6179c20db35f047d07665f84dcea759a937141dbc2f80ca48a96692f4.json
tests/fixtures/llm/25db65a09efeefb47595b11beb77327aa1ca9791fb56d3dc437314de1f6368ec.json
tests/fixtures/llm/273599fd2c6ed0efea9a55146c9a266e3f2d89910b609e4ab99c1048e57fc8d3.json
tests/fixtures/llm/2f120fa442d8cefb9b20af17f126a8b6e373a772aa7fbbc2f48ec0a6a3c84aa1.json
--- diff snapshot vs HEAD tracked files count:
    2217
    2217
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:31.648Z

**tool call — Bash**
````
{
 "command": "echo \"untracked fixtures:\"; git ls-files --others --exclude-standard -- tests/fixtures | wc -l; git ls-files --others --exclude-standard -- tests/fixtures | sed 's#/[^/]*$##' | sort | uniq -c; echo \"--- tracked fixture dirs in HEAD:\"; git ls-tree -r --name-only 20b3a42 -- tests/fixtures | sed 's#/[^/]*$##' | sort | uniq -c; echo \"--- is any untracked fixture named by a tracked file (sample):\"; grep -rl \"FIXTURE_MISS\" app | head -3; echo \"--- snapshot untracked-fixture count vs tests/fixtures/llm in HEAD:\"; ls \"$(echo $PWD)\" >/dev/null; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1/head/tests/fixtures/llm | wc -l",
 "description": "Count untracked fixture files and compare with HEAD fixtures"
}
````

### User / tool · 2026-11-02T14:41:31.821Z

**tool result**
````
untracked fixtures:
      51
   3 tests/fixtures
  48 tests/fixtures/llm
--- tracked fixture dirs in HEAD:
   1 tests/fixtures
1158 tests/fixtures/llm
  19 tests/fixtures/llm/curated
  25 tests/fixtures/llm/narrative
   1 tests/fixtures/llm/split
--- is any untracked fixture named by a tracked file (sample):
app/llm/_types.py
app/llm/audited.py
app/frontend/timeline.js
--- snapshot untracked-fixture count vs tests/fixtures/llm in HEAD:
    1161
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:40.340Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && env PORT=7955 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=\"$S/e2e.sqlite3\" nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > \"$S/server7955.log\" 2>&1 &\necho \"launched pid $!\"; cat > \"$S/wait_health.py\" <<'EOF'\nimport time, urllib.request, sys\nfor _ in range(60):\n    try:\n        print(urllib.request.urlopen(\"http://127.0.0.1:7955/api/health\", timeout=2).read().decode()[:200]); sys.exit(0)\n    except Exception as e:\n        time.sleep(0.5)\nprint(\"no health\", file=sys.stderr); sys.exit(1)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/wait_health.py\"; echo \"--- listener:\"; lsof -nP -iTCP:7955 -sTCP:LISTEN; echo \"--- ps:\"; ps -o pid,ppid,command -p $(lsof -nP -t -iTCP:7955 -sTCP:LISTEN | head -1)",
 "description": "Start my own HEAD app server on port 7955 and check health"
}
````

### User / tool · 2026-11-02T14:41:41.187Z

**tool result**
````
launched pid 64258
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-son
--- listener:
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  64260 arsis    9u  IPv4 0xc114fcbccb2573bb      0t0  TCP 127.0.0.1:7955 (LISTEN)
--- ps:
  PID  PPID COMMAND
64260 64258 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:46.191Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_code_check_refusal.py -q -rfEs -p no:cacheprovider > \"$S/run1_changed4.txt\" 2>&1; echo \"exit=$?\"; tail -40 \"$S/run1_changed4.txt\"",
 "description": "Run the changed e2e files plus T-158 file on my HEAD server",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:43:55.172Z

**tool result**
````
exit=1
......F................................................................. [ 85%]
............                                                             [100%]
=================================== FAILURES ===================================
_____________ test_first_screen_shows_entries_and_rows_are_compact _____________

pw = <playwright._impl._playwright.Playwright object at 0x106c94cb0>
sample_case = '8WYmgB8bfsirQTIlawGeUg'

    def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
        b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
        try:
            rows = pg.locator('[data-testid=queue] > article')
            assert rows.count() >= 5
            boxes = rows.evaluate_all(ROW_BOXES_JS)
>           assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]
E           assert 552 < 520

tests/e2e/test_polish_r3.py:181: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_first_screen_shows_entries_and_rows_are_compact
1 failed, 83 passed in 128.70s (0:02:08)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:44:04.862Z

**tool call — Bash**
````
{
 "command": "git log --oneline 078c5ae -1 && git merge-base --is-ancestor 078c5ae 20b3a42 && echo \"078c5ae is ancestor of 20b3a42\" ; echo \"--- commits after 078c5ae up to HEAD:\"; git log --oneline 078c5ae..20b3a42; echo \"--- product files changed 078c5ae..20b3a42:\"; git diff --stat 078c5ae 20b3a42 -- app | tail -3; echo \"--- git blame line of first-entry assertion:\"; git blame -L 180,181 20b3a42 -- tests/e2e/test_polish_r3.py; echo \"--- T-149 overview commits:\"; git log --oneline -3 -- app/frontend/overview.js; echo \"--- status of overview.js (working tree vs HEAD):\"; git diff --stat 20b3a42 -- app/frontend/overview.js; echo \"--- ps for my PIDs:\"; ps -o pid,ppid,command -p 64258,64260",
 "description": "Check commit ancestry and the T-149 overview history"
}
````

### User / tool · 2026-11-02T14:44:05.264Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:44:12.726Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"390|below the fold|accept-refused|scroll|def test_\" tests/e2e/test_code_check_refusal.py | head -60",
 "description": "Inspect the mobile refusal test assertions"
}
````

### User / tool · 2026-11-02T14:44:12.818Z

**tool result**
````
94:    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
95:    so a single bounding_box() read can land mid-scroll."""
105:@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
106:def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
111:        row.scroll_into_view_if_needed()
113:        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
114:        msg = box.get_by_test_id("accept-refused-msg").inner_text()
117:        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
122:        box.get_by_test_id("btn-accept-refused-edit").click()
127:        expect(row_of(pg, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
132:def test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):
136:    expect(row.get_by_test_id("accept-refused")).to_be_visible()
140:    expect(row_of(page, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
143:def test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted(page, broken):
163:def test_case_verdict_reads_the_backend_label_in_rail_and_panel(page, sample_case):
257:@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
258:def test_refused_accept_on_a_quote_check_offers_change_the_quote_and_opens_the_picker(pw, broken_quote, w, h):
262:        open_case(pg, t["tok"]); row = row_of(pg, t["id"]); row.scroll_into_view_if_needed()
264:        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
265:        msg = box.get_by_test_id("accept-refused-msg").inner_text()
267:        q = box.get_by_test_id("btn-accept-refused-quote")
268:        assert q.inner_text() == "Change the quote" and box.get_by_test_id("btn-accept-refused-edit").count() == 0, "a quote check does not offer 'Edit the summary'"
276:def test_refused_batch_on_a_quote_check_offers_change_the_quote_per_item(page, broken_quote):
288:def test_a_refused_summary_check_still_offers_edit_the_summary(page, broken):
293:    box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
294:    assert box.get_by_test_id("btn-accept-refused-edit").inner_text() == "Edit the summary" and box.get_by_test_id("btn-accept-refused-quote").count() == 0
297:def test_code_check_failed_returned_by_an_edit_shows_inline_under_the_edit_box_and_keeps_the_text(page, broken_quote):
318:def test_code_check_failed_on_an_edit_with_edit_the_summary_has_no_quote_button(page, sample_case):
344:def test_why_dialog_uses_the_backend_verdict_string_for_an_ai_draft_and_offers_change_the_quote(page, sample_case):
359:def test_why_dialog_lead_follows_the_verdict_string_not_a_frontend_guess(page, sample_case, label, lead):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:44:14.234Z

**tool call — Bash**
````
{
 "command": "sed -n 88,130p tests/e2e/test_code_check_refusal.py",
 "description": "Read the visibility helper and mobile refusal test body"
}
````

### User / tool · 2026-11-02T14:44:14.317Z

**tool result**
````
def row_of(page, i):
    return page.get_by_test_id("timeline").locator(f'[data-item-id="{i}"]').first


def vis(page, loc, frames=120):
    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
    so a single bounding_box() read can land mid-scroll."""
    vh = page.viewport_size["height"]
    for _ in range(frames):
        bb = loc.bounding_box()
        if bb is not None and bb["y"] >= 0 and bb["y"] + bb["height"] <= vh:
            return True
        page.evaluate("() => new Promise(r => requestAnimationFrame(() => r(true)))")
    return False


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"])
        row.scroll_into_view_if_needed()
        btn = row.get_by_test_id("btn-accept"); btn.click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
        assert "not in the quote" in msg or t["mode"] == "real"
        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
        assert box.get_attribute("role") == "alert"
        assert api("GET", f"/api/cases/{t['tok']}")[1]["review"]["counts"]["accepted"] == 0 and _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was changed"
        # Edit opens the item's edit box; a passing edit clears the refusal and the item is accepted by the edit
        box.get_by_test_id("btn-accept-refused-edit").click()
        ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
        assert pg.evaluate("document.activeElement === document.querySelector('[data-item-id=\"%s\"] textarea')" % t["id"]) or ta.is_visible()
        ta.fill(t["orig"]); row.get_by_test_id("btn-save-edit").click()
        expect(row_of(pg, t["id"])).to_have_attribute("data-review", "edited")
        expect(row_of(pg, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:44:20.374Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && for i in 1 2 3 4 5 6 7 8; do E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -k \"390\" -q -p no:cacheprovider 2>&1 | tail -1 | sed \"s/^/run$i: /\"; done 2>&1 | tee \"$S/t158_mobile_repeat.txt\"",
 "description": "Repeat the 390px refusal e2e cases eight times on my server",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:45:17.998Z

**tool result**
````
run1: 4 passed, 19 deselected in 7.05s
run2: 4 passed, 19 deselected in 6.92s
run3: 4 passed, 19 deselected in 6.81s
run4: 4 passed, 19 deselected in 7.18s
run5: 4 passed, 19 deselected in 6.92s
run6: 4 passed, 19 deselected in 7.10s
run7: 4 passed, 19 deselected in 6.75s
run8: 4 passed, 19 deselected in 6.78s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:45:30.277Z

**tool call — Bash**
````
{
 "command": "sed -n 1,87p tests/e2e/test_code_check_refusal.py; echo \"--- load:\"; uptime; ps -axo pid,etime,command | grep -E \"pytest|app.main|playwright|chrom\" | grep -v grep | head -20",
 "description": "Read refusal test fixtures and check machine load"
}
````

### User / tool · 2026-11-02T14:45:30.420Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:45:39.500Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"^def |^@pytest.fixture|BASE = |def open_case|def api\" tests/e2e/conftest.py | head -60; echo ---; grep -n -A12 \"def sample_case\" tests/e2e/conftest.py | head -30",
 "description": "Locate e2e helper functions and sample_case fixture"
}
````

### User / tool · 2026-11-02T14:45:39.594Z

**tool result**
````
89:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
95:def pytest_configure(config):
135:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
144:def needs_db():
155:def _up():
162:def pytest_collection_modifyitems(config, items):
170:def api(method, path, body=None):
180:def golden_text(name):
183:@pytest.fixture
184:def base_url():
187:@pytest.fixture
188:def sample_case():
202:@pytest.fixture(scope="session")
203:def pw():
208:@pytest.fixture
209:def page(pw):
218:def open_case(page, tok):
---
188:def sample_case():
189-    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
190-    import time
191-    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
192-    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
193-    for _ in range(300):
194-        s = api("GET", f"/api/cases/{tok}/status")[1]
195-        if s["status"] in ("ready", "failed"):
196-            break
197-        time.sleep(1)
198-    assert s["status"] == "ready"
199-    yield tok
200-    api("DELETE", f"/api/cases/{tok}")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:45:48.782Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; mkdir -p \"$S/probe\" && cat > \"$S/probe/probe_t158.py\" <<'EOF'\nimport os, sys, json, time\nSNAP = sys.argv[1]; N = int(sys.argv[2]); MODE = sys.argv[3]\nsys.path.insert(0, SNAP)\nos.environ[\"E2E_BASE_URL\"] = \"http://127.0.0.1:7955\"\nfrom playwright.sync_api import sync_playwright\nfrom tests.e2e import conftest as C\nfrom tests.e2e import test_code_check_refusal as R\n\ndef make_case():\n    st, c = C.api(\"POST\", \"/api/cases\", {\"sample\": True}); tok = c[\"token\"]\n    C.api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(300):\n        s = C.api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"): break\n        time.sleep(0.5)\n    c = C.api(\"GET\", f\"/api/cases/{tok}\")[1]\n    e = next(x for x in c[\"entries\"] if x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\")\n    return tok, e\n\nout = []\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for i in range(N):\n        tok, e = make_case()\n        if MODE == \"real\":\n            R._break(tok, e[\"id\"]); stub = None\n        else:\n            stub = R.Refuse(tok, e[\"id\"])\n        ctx = b.new_context(viewport={\"width\": 390, \"height\": 844}); pg = ctx.new_page()\n        if stub: stub.attach(pg)\n        C.open_case(pg, tok)\n        row = R.row_of(pg, e[\"id\"]); row.scroll_into_view_if_needed()\n        btn = row.get_by_test_id(\"btn-accept\")\n        btn.click()\n        box = row.get_by_test_id(\"accept-refused\")\n        box.wait_for(state=\"visible\", timeout=10000)\n        # sample the geometry a few frames later, as the test's vis() does\n        time.sleep(0.6)\n        bb = box.bounding_box(); bt = btn.bounding_box()\n        sy = pg.evaluate(\"scrollY\")\n        out.append({\"i\": i, \"mode\": MODE, \"scrollY\": sy, \"box_y\": round(bb[\"y\"],1), \"box_bottom\": round(bb[\"y\"]+bb[\"height\"],1), \"btn_y\": round(bt[\"y\"],1), \"vh\": 844, \"below_fold\": bb[\"y\"]+bb[\"height\"] > 844})\n        ctx.close()\n        C.api(\"DELETE\", f\"/api/cases/{tok}\")\n    b.close()\nfor r in out: print(json.dumps(r))\nprint(\"below_fold_count\", sum(r[\"below_fold\"] for r in out), \"of\", len(out))\nEOF\ncd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_t158.py\" \"$S/head\" 6 stub 2>&1 | tail -12",
 "description": "Probe refusal box geometry at 390x844 in stub mode",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T14:45:48.872Z

**tool result**
````
/bin/bash: line 96: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:45:51.713Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_t158.py\" \"$S/head\" 6 stub > \"$S/probe/stub6.txt\" 2>&1; echo \"exit=$?\"; tail -12 \"$S/probe/stub6.txt\"",
 "description": "Run geometry probe in stub mode, six iterations",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T14:46:01.806Z

**tool result**
````
exit=0
{"i": 0, "mode": "stub", "scrollY": 895, "box_y": 644, "box_bottom": 776, "btn_y": 512, "vh": 844, "below_fold": false}
{"i": 1, "mode": "stub", "scrollY": 843, "box_y": 696, "box_bottom": 828, "btn_y": 564, "vh": 844, "below_fold": false}
{"i": 2, "mode": "stub", "scrollY": 895, "box_y": 644, "box_bottom": 776, "btn_y": 512, "vh": 844, "below_fold": false}
{"i": 3, "mode": "stub", "scrollY": 734, "box_y": 805, "box_bottom": 937, "btn_y": 673, "vh": 844, "below_fold": true}
{"i": 4, "mode": "stub", "scrollY": 895, "box_y": 644, "box_bottom": 776, "btn_y": 512, "vh": 844, "below_fold": false}
{"i": 5, "mode": "stub", "scrollY": 895, "box_y": 644, "box_bottom": 776, "btn_y": 512, "vh": 844, "below_fold": false}
below_fold_count 1 of 6
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:46:10.913Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_t158.py\" \"$S/head\" 10 stub > \"$S/probe/stub10.txt\" 2>&1; echo \"exit=$?\"; tail -1 \"$S/probe/stub10.txt\"; E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_t158.py\" \"$S/head\" 8 real > \"$S/probe/real8.txt\" 2>&1; echo \"exit=$?\"; tail -1 \"$S/probe/real8.txt\"; grep -h -o '\"scrollY\": [0-9]*, \"box_y\": [0-9.]*, \"box_bottom\": [0-9.]*, \"btn_y\": [0-9.]*' \"$S/probe/stub10.txt\" \"$S/probe/real8.txt\" | sort | uniq -c",
 "description": "Run geometry probe ten stub and eight real iterations",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T14:46:40.096Z

**tool result**
````
exit=0
below_fold_count 0 of 10
exit=0
below_fold_count 0 of 8
   1 "scrollY": 843, "box_y": 696, "box_bottom": 828, "btn_y": 564
   8 "scrollY": 875, "box_y": 624, "box_bottom": 756, "btn_y": 492
   9 "scrollY": 895, "box_y": 644, "box_bottom": 776, "btn_y": 512
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:46:46.997Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/uncovered.css; echo ---; sed -n 1,60p app/frontend/uncovered.js",
 "description": "Read the uncovered list JS and CSS at HEAD"
}
````

### User / tool · 2026-11-02T14:46:47.112Z

**tool result**
````
/* T-144: the collapsed "Also in this record, not in an entry (n)" list under an entry. Tokens only. */
.entry[data-entry-id] > .unc { order: 7; grid-column: 1 / -1; }   /* after the decision buttons and the link bar */
.unc { margin-top: var(--s-2); border-top: 1px dashed var(--border); padding-top: var(--s-1); }
.unc[hidden] { display: none; }
.unc-h { margin: 0; font-size: var(--t-sm); line-height: var(--lh-sm); font-weight: var(--w-strong); color: var(--text); }
.unc-note { margin: var(--s-1) 0 var(--s-2); }
.unc-list { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--s-2); }
.unc-item { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--s-3); padding: var(--s-2) var(--s-3); background: var(--sunken); border-radius: var(--r-1, var(--r-2)); }
.unc-text { flex: 1 1 auto; min-width: 0; overflow-wrap: anywhere; font-size: var(--t-read); line-height: var(--lh-read); color: var(--text); }
.unc-jump { flex: 0 0 auto; white-space: nowrap; }
@media (max-width: 768px) {
  .unc-item { flex-direction: column; gap: var(--s-1); }
  .unc-jump { align-self: flex-start; min-height: 2.25rem; padding-left: 0; }
}
---
/* T-144: "Also in this record, not in an entry (n)" under each entry. Shows records[].uncovered[] (T-143: every sentence of the record that no live entry quote overlaps, computed by code),
   each sentence verbatim, in a list that starts closed (a "Not in an entry (n)" link in the row's head line opens it). "Show in record" opens the source record with that sentence highlighted (ZL.openSource, by the API's offsets).
   Review aid only: it is never in the letter, the notes or the copy text, and `kinds` is a hint the UI does not use (nothing is filtered here). Plugs in through ZL.registerRowActions. */
(function () {
  const ZL = window.ZL, { el } = ZL;
  const opened = new Set();   // entry ids whose list she opened; the rows repaint on every decision, and a list she is reading must stay open

  const recordsOf = (entry) => {
    const c = ZL.state.get().case; if (!c) return [];
    return entry.record_ids.map((rid) => c.records.find((r) => r.id === rid)).filter((r) => r && r.uncovered && r.uncovered.length);
  };

  ZL.registerRowActions((entry, row) => {
    const recs = recordsOf(entry);
    const items = recs.flatMap((r) => r.uncovered.map((u) => ({ rec: r, u })));
    if (!items.length) return;
    const many = recs.length > 1, n = items.length, id = "unc-" + entry.id;
    const who = entry.provider + (entry.date ? ", " + ZL.fmtDate(entry.date) : "");
    const full = `Also in this record, not in an entry (${n})`;
    // The row budget is tight (T-060: a compact row), so the collapsed state costs no height: a short link in the row's head line opens the list below the row. The full wording heads the list.
    const panel = el("section", { class: "unc", id, hidden: !opened.has(entry.id) || null, "data-testid": "uncovered-list", "data-record-count": String(n), "aria-label": full + ": " + who },
      el("h4", { class: "unc-h", "data-testid": "uncovered-heading" }, full),
      el("p", { class: "muted small unc-note" }, "Sentences from this record that no entry quotes. They are not in the letter. To use one, add it by hand or change the quote."),
      el("ul", { class: "unc-list" }, items.map(({ rec, u }) => el("li", { class: "unc-item", "data-testid": "uncovered-item", "data-record-id": rec.id },
        el("span", { class: "unc-text", "data-testid": "uncovered-text" }, u.text),
        el("button", { type: "button", class: "btn btn--link unc-jump", "data-testid": "btn-uncovered-jump",
          "aria-label": `Show in record ${rec.seq}: ${u.text.length > 80 ? u.text.slice(0, 80) + "..." : u.text}`,
          onclick: () => ZL.openSource([{ record_id: rec.id, start: u.start, end: u.end }], `Record ${rec.seq}: ${rec.source_label || who}`) }, many ? `Show in record ${rec.seq}` : "Show in record")))));
    const toggle = el("button", { type: "button", class: "btn btn--link unc-toggle", "data-testid": "uncovered-summary", "aria-expanded": String(opened.has(entry.id)), "aria-controls": id, "aria-label": full + ": " + who,
      onclick: () => { const open = panel.hidden; panel.hidden = !open; toggle.setAttribute("aria-expanded", String(open)); if (open) opened.add(entry.id); else opened.delete(entry.id); } }, `Not in an entry (${n})`);
    const head = row.querySelector(":scope > .entry-head");   // the head line has room on a wide screen; the link bar wraps to a second line when one more link joins it
    if (head) head.append(toggle); else row.append(toggle);
    row.append(panel);
  });

  // The list is computed by the server from the entries' quotes and states, so it changes when a quote is changed or an entry stops being live. The review responses do not carry it:
  // when any entry's quote or state differs from the last paint, read the case again and take only the records' `uncovered` from it.
  let lastToken = null, lastSig = null, seq = 0;
  const sigOf = (c) => (c.entries || []).concat(c.undated_entries || []).map((e) => [e.id, e.state, e.excerpt_start, e.excerpt_end].join(":")).join("|");
  ZL.state.subscribe((s) => {
    const c = s.case; if (!c || !s.token) { lastToken = lastSig = null; return; }
    const sig = sigOf(c);
    if (s.token !== lastToken) { lastToken = s.token; lastSig = sig; return; }
    if (sig === lastSig) return;
    lastSig = sig;
    const mine = ++seq, token = s.token;
    ZL.api.getCase(token).then((fresh) => {
      const cur = ZL.state.get();
      if (mine !== seq || cur.token !== token || !cur.case || !fresh || !fresh.records) return;
      let changed = false;
      cur.case.records.forEach((r) => {
        const f = fresh.records.find((x) => x.id === r.id);
        if (f && f.uncovered && JSON.stringify(f.uncovered) !== JSON.stringify(r.uncovered)) { r.uncovered = f.uncovered; changed = true; }
      });
      if (changed) ZL.state.set({ case: cur.case });
    }).catch(() => {});   // the list stays as it was; nothing she decided depends on it
  });
})();
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:01.311Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd /Users/arsis/zlayt-pm-project && git show 20b3a42^:tests/e2e/test_polish_r3.py > \"$S/head/tests/e2e/test_polish_r3_pre_t155.py\" && git show 20b3a42^:tests/e2e/test_rerun_judge.py > /dev/null && cd \"$S/head\" && E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3_pre_t155.py -k \"density or compact or 390 or first_screen\" -q -p no:cacheprovider -rf > \"$S/probe/pre_density.txt\" 2>&1; echo \"exit=$?\"; tail -15 \"$S/probe/pre_density.txt\"; echo \"--- current file, same selection:\"; E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py -k \"density or compact or 390 or first_screen\" -q -p no:cacheprovider -rf > \"$S/probe/cur_density.txt\" 2>&1; echo \"exit=$?\"; tail -6 \"$S/probe/cur_density.txt\"; echo \"--- tokens:\"; grep -rn -- \"--s-2:\" /Users/arsis/zlayt-pm-project/app/frontend/*.css | head -3",
 "description": "Run density tests with the pre-change test file on HEAD",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:47:07.149Z

**tool result**
````
exit=1
    def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
        b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
        try:
            rows = pg.locator('[data-testid=queue] > article')
            assert rows.count() >= 5
            boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
>           assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: [[631, 138, 'verified'], [777, 138, 'verified']]
E           assert 631 < 520

tests/e2e/test_polish_r3_pre_t155.py:173: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3_pre_t155.py::test_first_screen_shows_entries_and_rows_are_compact
1 failed, 1 passed, 17 deselected in 2.57s
--- current file, same selection:
exit=1
E           assert 552 < 520

tests/e2e/test_polish_r3.py:181: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_first_screen_shows_entries_and_rows_are_compact
1 failed, 1 passed, 17 deselected in 2.59s
--- tokens:
/Users/arsis/zlayt-pm-project/app/frontend/tokens.css:43:  --s-1: 0.25rem; --s-2: 0.5rem; --s-3: 0.75rem; --s-4: 1rem; --s-5: 1.5rem; --s-6: 2rem; --s-7: 3rem;
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:17.502Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cat > \"$S/probe/probe_rows.py\" <<'EOF'\nimport os, sys, json, time\nSNAP = sys.argv[1]; sys.path.insert(0, SNAP)\nos.environ[\"E2E_BASE_URL\"] = \"http://127.0.0.1:7955\"\nfrom playwright.sync_api import sync_playwright\nfrom tests.e2e import conftest as C\nst, c = C.api(\"POST\", \"/api/cases\", {\"sample\": True}); tok = c[\"token\"]\nC.api(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(300):\n    s = C.api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n    if s[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.5)\nncases = len(C.api(\"GET\", \"/api/cases\")[1].get(\"cases\", C.api(\"GET\", \"/api/cases\")[1]) if isinstance(C.api(\"GET\", \"/api/cases\")[1], dict) else C.api(\"GET\", \"/api/cases\")[1])\nJS_OLD = \"els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state'), !!e.querySelector('[data-testid=uncovered-list]'), e.querySelector('[data-testid=uncovered-list]') ? getComputedStyle(e.querySelector('[data-testid=uncovered-list]')).display : null, e.querySelector('[data-testid=uncovered-list]') ? e.querySelector('[data-testid=uncovered-list]').getBoundingClientRect().height : 0, e.querySelector('[data-testid=uncovered-list]') ? getComputedStyle(e.querySelector('[data-testid=uncovered-list]')).marginTop : null]; })\"\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for (w, h) in [(1440, 900), (390, 800)]:\n        pg = b.new_context(viewport={\"width\": w, \"height\": h}).new_page()\n        C.open_case(pg, tok)\n        rows = pg.locator('[data-testid=queue] > article')\n        rows.first.wait_for()\n        res = rows.evaluate_all(JS_OLD)\n        print(json.dumps({\"viewport\": [w, h], \"cases_in_db\": ncases, \"rows\": res[:6], \"row_count\": len(res),\n                          \"rows_with_list\": sum(1 for r in res if r[3])}))\n        pg.context.close()\n    b.close()\nC.api(\"DELETE\", f\"/api/cases/{tok}\")\nEOF\ncd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_rows.py\" \"$S/head\" 2>&1 | tail -6; echo \"--- cases listing shape:\"; curl -s http://127.0.0.1:7955/api/cases | head -c 300; echo",
 "description": "Measure row heights and collapsed uncovered list on HEAD",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:47:19.261Z

**tool result**
````
{"viewport": [1440, 900], "cases_in_db": 1, "rows": [[552, 138, "verified", false, null, 0, null], [698, 138, "verified", false, null, 0, null], [844, 138, "verified", true, "none", 0, "8px"], [990, 134, "verified", false, null, 0, null], [1132, 114, "verified", true, "none", 0, "8px"], [1254, 118, "verified", false, null, 0, null]], "row_count": 9, "rows_with_list": 3}
{"viewport": [390, 800], "cases_in_db": 1, "rows": [[1013, 310, "verified", false, null, 0, null], [1331, 308, "verified", false, null, 0, null], [1647, 330, "verified", true, "none", 0, "8px"], [1985, 288, "verified", false, null, 0, null], [2281, 268, "verified", true, "none", 0, "8px"], [2557, 290, "verified", false, null, 0, null]], "row_count": 9, "rows_with_list": 3}
--- cases listing shape:
{"cases":[]}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:41.849Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cat > \"$S/probe/probe_l6.py\" <<'EOF'\nimport os, sys, json, time\nSNAP = sys.argv[1]; sys.path.insert(0, SNAP)\nos.environ[\"E2E_BASE_URL\"] = \"http://127.0.0.1:7955\"\nfrom tests.e2e import conftest as C\nst, c = C.api(\"POST\", \"/api/cases\", {\"library\": \"case_lib06_lop_billed_vs_adjusted\"}); print(\"create\", st)\ntok = c[\"token\"]; print(\"run\", C.api(\"POST\", f\"/api/cases/{tok}/run\", {})[0])\nfor _ in range(300):\n    s = C.api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n    if s[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.5)\nprint(\"status\", s[\"status\"])\nj = C.api(\"GET\", f\"/api/cases/{tok}/judges\")[1]\nprint(\"totals\", json.dumps(j.get(\"totals\"), sort_keys=True)[:600])\nfor k in (\"rejections\", \"unresolved\", \"disagreements\"):\n    for r in j.get(k, []):\n        print(k, r.get(\"item_id\"), r.get(\"target_kind\", r.get(\"kind\")), (r.get(\"summary\") or r.get(\"reason\") or r.get(\"text\") or \"\")[:140])\nc2 = C.api(\"GET\", f\"/api/cases/{tok}\")[1]\nfor a in c2.get(\"amounts\", [])[:0]: pass\nprint(\"amount rows with kind:\", [(a.get(\"raw\"), a.get(\"kind\"), a.get(\"reason\") or a.get(\"unclear_reason\")) for a in c2.get(\"amounts\", [])][:12])\nC.api(\"DELETE\", f\"/api/cases/{tok}\")\nEOF\ncd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_l6.py\" \"$S/head\" 2>&1 | tail -30",
 "description": "Inspect the L6 judge objections on my HEAD server",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:47:42.639Z

**tool result**
````
create 201
run 202
status ready
totals {"human_overrides": 0, "items_judged": 16, "supported": 12, "unavailable": 0, "unsupported": 4, "unsure": 0}
rejections a3 amount 
rejections a4 amount 
rejections a7 amount 
rejections f_r5_1 flag 
disagreements e5 entry 
disagreements a3 amount 
disagreements a4 amount 
disagreements a7 amount 
disagreements f_r5_1 flag 
disagreements f_r3_2 flag 
disagreements f_r4_1 flag 
disagreements f_r5_1 flag 
amount rows with kind: [(None, 'charge', None), (None, 'charge', None), (None, 'unclear', None), (None, 'unclear', None), (None, 'charge', None), (None, 'unclear', None), (None, 'unclear', None)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:48.748Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cat > \"$S/probe/probe_l6b.py\" <<'EOF'\nimport os, sys, json, time\nSNAP = sys.argv[1]; sys.path.insert(0, SNAP)\nos.environ[\"E2E_BASE_URL\"] = \"http://127.0.0.1:7955\"\nfrom tests.e2e import conftest as C\nst, c = C.api(\"POST\", \"/api/cases\", {\"library\": \"case_lib06_lop_billed_vs_adjusted\"}); tok = c[\"token\"]\nC.api(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(300):\n    s = C.api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n    if s[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.5)\nc2 = C.api(\"GET\", f\"/api/cases/{tok}\")[1]\nprint(\"amount keys:\", sorted(c2[\"amounts\"][0].keys()) if c2.get(\"amounts\") else \"none\")\nfor a in c2.get(\"amounts\", []):\n    print(a.get(\"id\"), a.get(\"kind\"), a.get(\"amount_text\") or a.get(\"raw\") or a.get(\"text\") or a.get(\"label\"), a.get(\"cents\"), a.get(\"unclear_reason\") or a.get(\"reason\"))\nC.api(\"DELETE\", f\"/api/cases/{tok}\")\nEOF\ncd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_l6b.py\" \"$S/head\" 2>&1 | tail -12",
 "description": "Map L6 judge amount ids to their printed amounts",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:47:49.548Z

**tool result**
````
amount keys: ['accept_effect', 'confirm_required', 'duplicate_note', 'edited', 'entry_id', 'excerpt', 'excerpt_end', 'excerpt_start', 'flag', 'id', 'judge_required_for_export', 'kind', 'ladder', 'reasons', 'record_ids', 'rerun_note', 'review_status', 'second_check_pending', 'state', 'text', 'value_cents', 'why']
a1 charge $2,880 None None
a2 charge $1,100 None None
a3 unclear $450 None None
a4 unclear $1,550 None None
a5 charge $2,400 None None
a6 unclear $1,250 None None
a7 unclear $1,150 None None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:58.104Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cat > \"$S/probe/make_variant.py\" <<'EOF'\nimport sys\nsrc, dst = sys.argv[1], sys.argv[2]\nlines = open(src, encoding=\"utf-8\").read().split(\"\\n\")\nout = [l for l in lines if \"assert boxes[0][0] < 520\" not in l]\nassert len(lines) - len(out) == 1, len(lines) - len(out)\nopen(dst, \"w\", encoding=\"utf-8\").write(\"\\n\".join(out))\nprint(\"removed the first-entry assertion only\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/make_variant.py\" \"$S/head/tests/e2e/test_polish_r3_pre_t155.py\" \"$S/head/tests/e2e/test_polish_r3_pre_noentry.py\" && cd \"$S/head\" && E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3_pre_noentry.py -k \"first_screen or 390\" -q -p no:cacheprovider -rf 2>&1 | tail -4; echo \"--- current file variant:\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/make_variant.py\" /Users/arsis/zlayt-pm-project/tests/e2e/test_polish_r3.py \"$S/head/tests/e2e/test_polish_r3_cur_noentry.py\" && cd \"$S/head\" && E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3_cur_noentry.py -k \"first_screen or 390\" -q -p no:cacheprovider -rf 2>&1 | tail -4",
 "description": "Run density budgets with only the first-entry line removed",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:48:03.878Z

**tool result**
````
removed the first-entry assertion only
..                                                                       [100%]
2 passed, 17 deselected in 2.59s
--- current file variant:
removed the first-entry assertion only
..                                                                       [100%]
2 passed, 17 deselected in 2.54s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:26.412Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cd \"$S/head\" && for i in 1 2 3; do E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=\"$S/e2e.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py -k first_screen -q -p no:cacheprovider 2>&1 | grep -E \"AssertionError|passed|failed\" | head -2 | sed \"s/^/run$i: /\"; done; echo \"--- focus restore on shortcut close:\"; cd /Users/arsis/zlayt-pm-project && grep -n -E \"btn-shortcuts|shortcuts-modal|focus\\(\\)|returnFocus|restoreFocus|opener\" app/frontend/*.js | grep -i -E \"short|opener|restore|return\" | head -12",
 "description": "Repeat the first-screen test three times and grep focus restore",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:48:32.958Z

**tool result**
````
run1: E           AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]
run1: tests/e2e/test_polish_r3.py:181: AssertionError
run2: E           AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]
run2: tests/e2e/test_polish_r3.py:181: AssertionError
run3: E           AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]
run3: tests/e2e/test_polish_r3.py:181: AssertionError
--- focus restore on shortcut close:
app/frontend/app.js:30:    $("#case-progress").hidden = !ready; $("#btn-export").hidden = !ready; $("#btn-shortcuts").hidden = !ready;
app/frontend/app.js:127:    $("#btn-shortcuts").addEventListener("click", () => ZL.rv && ZL.rv.openShortcuts());
app/frontend/review.js:138:  function restoreFocus(pf) {
app/frontend/review.js:294:      restoreFocus(o.advance ? { nextFrom: id, plan } : o.focus ? { id, action: o.focus } : null);
app/frontend/review.js:418:    let d = document.querySelector('[data-testid="shortcuts-modal"]');
app/frontend/review.js:420:      d = el("dialog", { class: "dlg dlg--md", "data-testid": "shortcuts-modal", "aria-labelledby": "kb-title" },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:35.826Z

**tool call — Bash**
````
{
 "command": "sed -n 414,440p app/frontend/review.js | cut -c1-260",
 "description": "Read the shortcut sheet open and close focus code"
}
````

### User / tool · 2026-11-02T14:48:35.933Z

**tool result**
````
  const KEYS = [["j / k", "Next / previous item (dates to confirm, then entries, flags, charges)"], ["a", "Accept the selected item, then move to the next one that needs a decision (a flagged charge asks first)"], ["d", "Dismiss the selected item, then move on
    ["e", "Edit the wording of the selected item"], ["r", "Reset a decided item"], ["o", "Open the source record in a dialog"], ["p", "Move focus to the source record beside the list (Esc returns)"],
    ["Shift+A", "Accept all verified entries (asks first, with the count)"], ["?", "This list"]];
  RV.openShortcuts = function () {
    let d = document.querySelector('[data-testid="shortcuts-modal"]');
    if (!d) {
      d = el("dialog", { class: "dlg dlg--md", "data-testid": "shortcuts-modal", "aria-labelledby": "kb-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "kb-title" }, "Keyboard shortcuts"), el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-close-shortcuts", onclick: () => d.close() }, "Close")),
        el("div", { class: "dlg-body" },
          el("p", { class: "muted" }, "Letter keys work only while an item is selected: use Start review, or press Tab and then Enter on the first skip link. They never act from Export, the header or a text box."),
          el("dl", { class: "kv kv--keys", "data-testid": "shortcuts-list" }, KEYS.flatMap(([k, v]) => [el("dt", {}, el("kbd", {}, k)), el("dd", {}, v)]))));
      document.body.append(d);
    }
    const back = document.activeElement;
    d.addEventListener("close", () => { if (back && back.isConnected) back.focus(); }, { once: true });
    if (!d.open) d.showModal();
  };

  // ---- keyboard flow (R-RV-4, WCAG 2.1.4 / T-060 blocker). Single-key shortcuts act ONLY while focus is on an item row or on something inside one.
  // From Export, the header, a dialog, a text field or the page body they do nothing, so a stray key can never change a decision.
  const typing = (t) => !!t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (typing(t)) return;
    if (document.querySelector("dialog[open]")) {   // a dialog swallows the letter keys; say so instead of doing nothing (T-060 r3, paralegal F11)
      if (ev.key.length === 1 && "jkadero".includes(ev.key.toLowerCase()) && !ev.shiftKey && ZL.state.get().case) RV.say("A window is open. Press Escape to close it first, then use the key again.");
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:40.811Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"ROW_BOXES_JS|150|170|420|first entry above|uncovered\" tests/e2e/test_polish_r3.py | cut -c1-220; echo ---; grep -n -E \"def test_refused|vis\\(pg, box\\)|abs\\(box\" tests/e2e/test_code_check_refusal.py | head -5; echo ---; grep -n -E \"Edited by you, not AI-checked|EDIT_WAITING|everywhere\" tests/e2e/test_rerun_judge.py | cut -c1-200",
 "description": "Cite exact lines for density budgets and edited-wording assertions"
}
````

### User / tool · 2026-11-02T14:48:40.993Z

**tool result**
````
168:# T-144 (stale-test update): every entry row may now carry a collapsed "Also in this record, not in an entry (n)" list (uncovered-list, ~30-57 px with its margins). The row-height
169:# budgets below (150 / 170 px at 1440, 420 px at 390) were set before it existed and still guard the row itself, so the measured height leaves that deliberate list out.
170:ROW_BOXES_JS = """els => els.map(e => { const r = e.getBoundingClientRect(), u = e.querySelector('[data-testid=uncovered-list]');
180:        boxes = rows.evaluate_all(ROW_BOXES_JS)
181:        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
187:            assert h <= (170 if state == "needs_review" else 150), boxes
200:def test_390_needs_review_row_is_at_most_420(pw, lib09):
203:        hs = [bx[1] for bx in pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all(ROW_BOXES_JS)]
204:        assert hs and max(hs) <= 420, hs
---
106:def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
117:        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
118:        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
132:def test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):
143:def test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted(page, broken):
---
254:    assert "Edited by you, not AI-checked" in t and "Blocks the export" not in t and "can't go in the letter" not in t
265:# "Edited; waiting for your check" (memory/contracts/api.md, Item trace), not "Edited by you, not AI-checked" (that wording stays in the AI-check panel row and the judge step).
266:EDIT_WAITING = "Edited; waiting for your check"
300:    assert WORDING in txt and "qualifier" in txt and "Blocks the export" in txt and "Edited by you, not AI-checked" not in txt
308:def test_passing_edit_says_edited_by_you_not_ai_checked_everywhere(page, mixed):
309:    """D-045(b) wording in the panel and the judge step; T-134 r2: the Why dialog verdict of an edit she has not yet accepted is EDIT_WAITING (edit_to_check)."""
314:        assert "Edited by you, not AI-checked" in row.inner_text() and "Blocks the export" not in row.inner_text() and row.get_by_test_id("btn-rerun-judge").count() == 0
318:    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING
333:    assert st.get_by_test_id("item-verdict").inner_text() != "Edited by you, not AI-checked"
352:    """T-134 r2: once the failing wording is replaced, the Why dialog reads EDIT_WAITING (edited, not yet accepted by her), not a failure."""
361:    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING and st.get_by_test_id("item-wording-fail").count() == 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:19.093Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; mkdir -p \"$S/prev078\" && cd /Users/arsis/zlayt-pm-project && git archive -o \"$S/prev078.tar\" 078c5ae && tar -xf \"$S/prev078.tar\" -C \"$S/prev078\" && rm \"$S/prev078.tar\" && cd \"$S/prev078\" && env PORT=7956 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=\"$S/prev078.sqlite3\" nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > \"$S/server7956.log\" 2>&1 &\nsleep 0 ; cat > \"$S/probe/wait7956.py\" <<'EOF'\nimport time, urllib.request, sys\nfor _ in range(60):\n    try:\n        urllib.request.urlopen(\"http://127.0.0.1:7956/api/health\", timeout=2).read(); print(\"up\"); sys.exit(0)\n    except Exception:\n        time.sleep(0.5)\nprint(\"no health\"); sys.exit(1)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/wait7956.py\"; lsof -nP -iTCP:7956 -sTCP:LISTEN; cd \"$S/prev078\" && git -C /Users/arsis/zlayt-pm-project show 078c5ae:tests/e2e/test_polish_r3.py > tests/e2e/test_polish_r3_at078.py && E2E_BASE_URL=http://127.0.0.1:7956 ZLAYT_DB=\"$S/prev078.sqlite3\" E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3_at078.py -k \"density or first_screen or 390 or compact\" -q -p no:cacheprovider -rf > \"$S/probe/at078_density.txt\" 2>&1; echo \"exit=$?\"; grep -E \"^E  |passed|failed\" \"$S/probe/at078_density.txt\" | head -12",
 "description": "Archive 078c5ae and run density tests on its own server port 7956",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T14:49:24.216Z

**tool result**
````
up
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  86463 arsis    9u  IPv4 0x29a6af38a9d9d9a2      0t0  TCP 127.0.0.1:7956 (LISTEN)
exit=1
E               AssertionError: [[518, 138, 'verified'], [664, 138, 'verified'], [810, 179, 'verified'], [997, 134, 'verified'], [1139, 155, 'verified'], [1302, 118, 'verified'], ...]
E               assert 179 <= 150
E           AssertionError: [430.09375, 389.09375]
E           assert ([430.09375, 389.09375] and 430.09375 <= 420)
E            +  where 430.09375 = max([430.09375, 389.09375])
2 failed, 17 deselected in 2.83s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:37.326Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-155; mkdir -p \"$E\" && cd \"$S/head\" && E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_rows.py\" \"$S/head\" > \"$S/probe/rows_head.txt\" 2>&1; E2E_REQUIRE_DB=1 ZLAYT_DB=\"$S/e2e.sqlite3\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/probe/probe_l6.py\" \"$S/head\" > \"$S/probe/l6_head.txt\" 2>&1; cp \"$S/run1_changed4.txt\" \"$S/probe/stub6.txt\" \"$S/probe/stub10.txt\" \"$S/probe/real8.txt\" \"$S/probe/t158_mobile_repeat.txt\" \"$S/probe/pre_density.txt\" \"$S/probe/cur_density.txt\" \"$S/probe/at078_density.txt\" \"$S/probe/rows_head.txt\" \"$S/probe/l6_head.txt\" \"$S/probe/probe_t158.py\" \"$S/probe/probe_rows.py\" \"$S/probe/probe_l6.py\" \"$S/probe/make_variant.py\" \"$E/\" 2>&1; cp \"$S/t158_mobile_repeat.txt\" \"$E/t158_mobile_repeat_top.txt\" 2>/dev/null; ls \"$E\"; echo \"--- rows_head:\"; cat \"$S/probe/rows_head.txt\" | cut -c1-400; echo \"--- l6:\"; grep -E \"rejections|totals|status\" \"$S/probe/l6_head.txt\"",
 "description": "Save probe outputs as review evidence and recheck HEAD row geometry",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:49:39.741Z

**tool result**
````
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1/probe/t158_mobile_repeat.txt: No such file or directory
at078_density.txt
cur_density.txt
l6_head.txt
make_variant.py
pre_density.txt
probe_l6.py
probe_rows.py
probe_t158.py
real8.txt
rows_head.txt
run1_changed4.txt
stub10.txt
stub6.txt
t158_mobile_repeat_top.txt
--- rows_head:
{"viewport": [1440, 900], "cases_in_db": 1, "rows": [[552, 138, "verified", false, null, 0, null], [698, 138, "verified", false, null, 0, null], [844, 138, "verified", true, "none", 0, "8px"], [990, 134, "verified", false, null, 0, null], [1132, 114, "verified", true, "none", 0, "8px"], [1254, 118, "verified", false, null, 0, null]], "row_count": 9, "rows_with_list": 3}
{"viewport": [390, 800], "cases_in_db": 1, "rows": [[1005, 310, "verified", false, null, 0, null], [1323, 308, "verified", false, null, 0, null], [1639, 330, "verified", true, "none", 0, "8px"], [1977, 288, "verified", false, null, 0, null], [2273, 268, "verified", true, "none", 0, "8px"], [2549, 290, "verified", false, null, 0, null]], "row_count": 9, "rows_with_list": 3}
--- l6:
status ready
totals {"human_overrides": 0, "items_judged": 16, "supported": 12, "unavailable": 0, "unsupported": 4, "unsure": 0}
rejections a3 amount 
rejections a4 amount 
rejections a7 amount 
rejections f_r5_1 flag
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:45.093Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1; cp \"$S/t158_mobile_repeat.txt\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-155/t158_mobile_repeat.txt; echo \"--- listeners:\"; lsof -nP -iTCP:7955 -sTCP:LISTEN; lsof -nP -iTCP:7956 -sTCP:LISTEN; echo \"--- my PIDs:\"; ps -o pid,ppid,command -p 64258,64260,86463 | cut -c1-160; echo \"parent of 86463:\"; ps -o pid,ppid,command -p $(ps -o ppid= -p 86463) | cut -c1-160; echo \"cwd of 64260 / 86463:\"; lsof -a -p 64260 -d cwd -Fn | tail -1; lsof -a -p 86463 -d cwd -Fn | tail -1",
 "description": "Verify my server listener PIDs and their cwd before stopping"
}
````

### User / tool · 2026-11-02T14:49:45.605Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:48.399Z

**tool call — Bash**
````
{
 "command": "kill 64260 86463; sleep 2; kill 64258 86406 2>/dev/null; sleep 1; echo \"--- after kill:\"; lsof -nP -iTCP:7955 -sTCP:LISTEN; lsof -nP -iTCP:7956 -sTCP:LISTEN; ps -o pid,command -p 64258,64260,86406,86463 2>/dev/null | cut -c1-80; echo \"--- 7860 (not mine, untouched):\"; lsof -nP -iTCP:7860 -sTCP:LISTEN | tail -1",
 "description": "Stop only my two test servers and verify ports closed"
}
````

### User / tool · 2026-11-02T14:49:51.795Z

**tool result**
````
--- after kill:
  PID COMMAND
--- 7860 (not mine, untouched):
Python  20423 arsis    9u  IPv4 0xe79fb86e4f7049c5      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:50:24.303Z

**tool call — Bash**
````
{
 "command": "grep -n \"L6_OBJECTIONS = 4\" tests/e2e/test_stepper.py; grep -n \"wait_for_function\" tests/e2e/test_polish_r3.py | cut -c1-80; sed -n 170,172p tests/e2e/test_polish_r3.py | cut -c1-60; python3 tools/board.py --help 2>&1 | head -5; ls reviews | grep -i \"T-155\" ; echo \"exists-check done\"",
 "description": "Confirm exact line numbers for citations and existing review files"
}
````

### User / tool · 2026-11-02T14:50:24.604Z

**tool result**
````
23:L6_OBJECTIONS = 4
59:    page.wait_for_function("() => document.activeElement && document.activeEl
ROW_BOXES_JS = """els => els.map(e => { const r = e.getBound
    let extra = 0; if (u) { const c = getComputedStyle(u); e
    return [r.top + scrollY, r.height - extra, e.getAttribut
usage: board.py [-h]
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
                ...

Zlayt PM project board CLI
exists-check done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:16.178Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md",
 "content": "# T-155 review (staff-engineer-reviewer): e2e triage, commit 20b3a42 (tests only)\n\n**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at HEAD 20b3a42 (`git rev-parse HEAD`), tree from `git archive 20b3a42`.\n\n## What I checked\n\n- **Decisions.** D-059 (ORCHESTRATOR_DECISIONS.md:67) explains the L6 count change, and the count matches the live judge output. The T-134 r2 `edit_to_check` wording matches memory/contracts/api.md:370 and app/backend/trace.py:289. D-058 has no assertion in this diff, so it is not applicable here. The T-144 row-height edit does not follow any decision. Its stated premise is false at HEAD (see F2).\n- **Red at the reviewed commit.** `test_first_screen_shows_entries_and_rows_are_compact` fails 3 of 3 runs at 20b3a42 (`552 < 520`, tests/e2e/test_polish_r3.py:181). The card's green evidence cites 078c5ae, which is 11 commits behind HEAD (F1).\n- **Density edit.** At 078c5ae the original density budgets really fail (`179 <= 150`, `430 <= 420`). f262223 fixed that upstream. At HEAD the original budgets pass, and the collapsed list costs 0 px. The T-155 edit therefore removes a measure that was not needed and discounts 8 px on list rows (F2).\n- **T-158.** The 390px refusal box really can end below the fold. The mechanism is that the box sits 132 px under the Accept button, so it is out of a 844 px viewport whenever the button is lower than y=580. One of 24 probe samples hit that (scrollY 734, box bottom 937). The \"about 50%\" rate on the card was not reproduced. T-158 is the right owner for the product fix (F3).\n- **L6 count and EDIT_WAITING.** Both follow the recorded decisions. The count assertion is weak on identity (F4), and one test name is stale (F5).\n\nEvidence files: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-155/` (probe scripts and outputs). Scratch snapshot: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1/`.\n\n## Findings\n\n**F1 (major). The card's green claim cites 078c5ae, not the reviewed commit. The first-screen test is red at 20b3a42 and is not triaged.**\nRepro: `E2E_BASE_URL=http://127.0.0.1:7955 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -k first_screen` on the 20b3a42 archive prints `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` at tests/e2e/test_polish_r3.py:181. It failed in 3 of 3 runs. At 078c5ae the same line read `[[518, ...` (artifacts/review-evidence/T-155/at078_density.txt), so the red came in after that sha. The orchestrator note at 14:39 names it. The handoff triage does not.\n\n**F2 (major). The T-144 row-height edit weakens the compact-row budget on a false premise. The density reds it calls stale were real.**\n- The density reds at 078c5ae were real: `assert 179 <= 150` and `assert 430.09375 <= 420` (at078_density.txt). f262223 (\"the uncovered list opens from a short link in the entry head so compact rows keep their height\") is in 078c5ae..20b3a42 and is the fix.\n- At 20b3a42 the original measure passes. I removed only line 181 from the pre-change file (`git show 20b3a42^:tests/e2e/test_polish_r3.py`). Then `pytest -k \"first_screen or 390\"` gave `2 passed`. The current file with the same single-line removal also gave `2 passed`.\n- The collapsed list costs 0 px at HEAD. `app/frontend/uncovered.js:21` sets `hidden: !opened.has(entry.id) || null`, and `app/frontend/uncovered.css:4` is `.unc[hidden] { display: none; }`. On the sample at 1440x900 and 390x800, the list is `display: none` with height 0 and computed `margin-top: 8px` on 3 of 9 rows (artifacts/review-evidence/T-155/rows_head.txt).\n- The edit at tests/e2e/test_polish_r3.py:168-172 says \"~30-57 px with its margins\". The ROW_BOXES_JS function subtracts that margin from every row that carries a list, and it is used at :180 and :203. So those rows read 8 px short of the rendered height.\n- The constraint itself is real. The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen. The edit does not make that constraint go away, but it does make the measure wrong.\n\n**F3 (minor). T-158 holds the real regression. The \"about 50%\" rate is not reproduced.**\n- Mechanism: the box is `btn_y + 132` at every sample. It is below 844 whenever btn_y is greater than 580. One sample hit it: `{\"scrollY\": 734, \"box_y\": 805, \"box_bottom\": 937, \"btn_y\": 673, \"below_fold\": true}` (artifacts/review-evidence/T-155/stub6.txt).\n- Rate: 1 of 6 (stub), 0 of 10 (stub), 0 of 8 (real), so 1 of 24 in total (stub6.txt, stub10.txt, real8.txt). In pytest, `test_code_check_refusal.py -k 390` passed in 9 runs, 36 cases in total (t158_mobile_repeat.txt). Load averages were 21 to 24 during these runs (`uptime`). I cannot say what the card's machine was doing.\n- The test is correct and stays unchanged. The T-158 note should cite the geometry measurement, not the 3-of-6 rate.\n\n**F4 (minor). The L6 count change asserts a count, not which item moved.**\n- `L6_OBJECTIONS = 4` (tests/e2e/test_stepper.py:23). The four rejections on /judges are a3 (unclear $450), a4 (unclear $1,550), a7 (unclear $1,150) and flag f_r5_1 (artifacts/review-evidence/T-155/l6_head.txt).\n- The count follows D-059. Whether a7 is correct billing is outside my lens.\n- Because the test checks only the count, another item could replace a7 and the test would still pass.\n\n**F5 (nit). A test name overstates what it asserts.**\n- tests/e2e/test_rerun_judge.py:308 `test_passing_edit_says_edited_by_you_not_ai_checked_everywhere` now asserts `EDIT_WAITING` for the Why dialog (:318). The D-045(b) wording is still asserted in the panel row (:314). The name should say panel and judge step.\n\n## Notes on what I did not run\n\n- The full tests/e2e suite and tests/unit were not run. The brief asked for the changed files and T-158.\n- No mutation check was run on the edited files. Acceptance tests for F2 and F4 are written as proposals and have not been run.\n- I did not run `board.py review`.\n\n```json\n{\"card\": \"T-155\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 20b3a42 (tests only: tests/e2e/test_polish_r3.py, tests/e2e/test_rerun_judge.py, tests/e2e/test_stepper.py); reviewed at HEAD 20b3a42 from git archive in a scratch snapshot; own server 127.0.0.1:7955 (fixture backend, ZLAYT_MODE=local, E2E_REQUIRE_DB=1); comparison server 127.0.0.1:7956 from archive 078c5ae; library case case_lib06_lop_billed_vs_adjusted and the sample case\",\n \"exercised\": [\n   \"python3 tools/board.py show T-155; read personas/staff-engineer.md\",\n   \"git show --stat 20b3a42; git show 20b3a42 -- tests/ (full test diff); git rev-parse HEAD -> 20b3a42\",\n   \"git log --oneline 078c5ae..20b3a42 (11 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files)\",\n   \"read memory/ORCHESTRATOR_DECISIONS.md D-058 (line 66), D-059 (67), D-060 (68); memory/contracts/api.md lines 365-374; app/backend/trace.py:289; app/frontend/uncovered.js:21; app/frontend/uncovered.css:4; app/frontend/tokens.css:43; commit f262223 subject\",\n   \"git archive 20b3a42 extracted to scratch T155_r1/head (2217 files); 48 untracked tests/fixtures/llm files in the working tree not copied; no FIXTURE_MISS occurred\",\n   \"E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=<scratch>/e2e.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_code_check_refusal.py -q -rfEs -> 1 failed, 83 passed, 128.70s; failure test_polish_r3.py::test_first_screen_shows_entries_and_rows_are_compact at :181 (552 < 520)\",\n   \"3 repeats of test_polish_r3.py -k first_screen on 20b3a42: 552 each run\",\n   \"pytest test_code_check_refusal.py -k 390 x8 on 20b3a42: 4 passed each run (artifacts/review-evidence/T-155/t158_mobile_repeat.txt)\",\n   \"probe_t158.py (Playwright 390x844, stub 6 and 10, real 8 samples): 1 of 24 below the fold (stub6.txt, stub10.txt, real8.txt)\",\n   \"probe_rows.py on 20b3a42: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows at 1440x900 and 390x800 (rows_head.txt)\",\n   \"pre-change test file (git show 20b3a42^) and current file, each with only line 181 removed: pytest -k 'first_screen or 390' -> 2 passed each\",\n   \"server 127.0.0.1:7956 from archive 078c5ae: density budgets fail 179 <= 150 and 430.09 <= 420; first-entry y 518 (at078_density.txt)\",\n   \"probe_l6.py and probe_l6b on 20b3a42: judge rejections a3, a4, a7, f_r5_1; a3 unclear $450, a4 unclear $1,550, a7 unclear $1,150 (l6_head.txt)\",\n   \"uptime: load average 21 to 24 during the runs\",\n   \"stopped only my PIDs (listeners 64260 and 86463 and their bash wrappers 64258 and 86406), verified via lsof and cwd; ports 7955 and 7956 closed; shared :7860 untouched\",\n   \"not run: full tests/e2e, tests/unit, evals, mutation checks; board.py review not run\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"test_integrity\": 2, \"triage_accuracy\": 2, \"evidence_matches_reviewed_commit\": 2, \"decision_traceability\": 4, \"determinism\": 4},\n \"findings\": [\n   {\"severity\": \"major\",\n    \"title\": \"Green claim cites 078c5ae, not the reviewed commit; first-screen test red at 20b3a42 and not triaged\",\n    \"evidence\": \"tests/e2e/test_polish_r3.py:181 `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` on git archive 20b3a42, 3 of 3 runs; at078_density.txt shows 518 at 078c5ae; git log --oneline 078c5ae..20b3a42 lists 11 commits; card AC evidence says 'clean HEAD 078c5ae ... 281 passed, 2 skipped, 1 failed'\",\n    \"why_it_matters\": \"The AC requires a green clean-HEAD run with each failure explained on the card. The commit under review is red for a test the card neither fixes nor explains, and the cited evidence describes another tree. A gate reviewer reproducing the card gets a different result.\",\n    \"fix\": \"Re-run the full tests/e2e on git archive 20b3a42 with E2E_REQUIRE_DB=1, cite that sha and the counts in the AC evidence, and record on the card the owner of the first-screen failure (T-149 r2) or file a card. Do not loosen line 181 inside this card.\",\n    \"acceptance_test\": \"Full tests/e2e on the 20b3a42 archive: every failure has a card note naming its owner or a passing result; the AC evidence cites 20b3a42.\"},\n   {\"severity\": \"major\",\n    \"title\": \"T-144 row-height edit weakens the compact-row budget on a false premise; the density reds it calls stale were real\",\n    \"evidence\": \"at078_density.txt: `assert 179 <= 150` and `assert 430.09375 <= 420` at 078c5ae; f262223 fixed it in 078c5ae..20b3a42. At 20b3a42 the original measure passes: pre-change file with line 181 removed, `-k 'first_screen or 390'` -> 2 passed. rows_head.txt: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows. app/frontend/uncovered.js:21 `hidden: !opened.has(entry.id) || null`; app/frontend/uncovered.css:4 `.unc[hidden] { display: none; }`. tests/e2e/test_polish_r3.py:168-172 comment '~30-57 px with its margins' and ROW_BOXES_JS subtracting extra; used at :180 and :203.\",\n    \"why_it_matters\": \"The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen and is still a real constraint. The edit removes a term that is zero at HEAD, the stated reason is false, and it discounts 8 px of an unrendered margin on list rows, so the budget reads short. Any future visible collapsed element would be hidden from the budget under the same comment.\",\n    \"fix\": \"Revert ROW_BOXES_JS to the pre-20b3a42 measure (r.height) at tests/e2e/test_polish_r3.py:170-172, :180 and :203, and remove the T-144 comment at :168-169. Leave line 181 as it is (see F1).\",\n    \"acceptance_test\": \"On the reverted file, `pytest tests/e2e/test_polish_r3.py -k 'density or 390'` passes at 20b3a42. Mutation in a scratch copy: `.unc[hidden]{display:block}`; the 390 or 1440 budget test must fail. If it does not, the card must say the budget does not guard the list area.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"T-158 holds the real regression, but the about-50% rate on the card is not reproduced\",\n    \"evidence\": \"probe_t158.py: stub 1 of 6 (stub6.txt, `{\\\"scrollY\\\": 734, \\\"box_y\\\": 805, \\\"box_bottom\\\": 937, \\\"btn_y\\\": 673, \\\"below_fold\\\": true}`), stub 0 of 10 (stub10.txt), real 0 of 8 (real8.txt); box_y = btn_y + 132 in every sample; pytest -k 390 passed 36 cases in 9 runs (t158_mobile_repeat.txt); uptime load 21-24\",\n    \"why_it_matters\": \"The mechanism is real and T-158 (frontend) is the right owner, so leaving test_code_check_refusal.py unchanged is correct. The 3-of-6 rate is not reproduced, and a repro should rest on measured geometry, not a rate.\",\n    \"fix\": \"On T-158, replace the about-50% claim with the geometry measurement (btn_y, scrollY, box bottom) and keep the test unchanged.\",\n    \"acceptance_test\": \"T-158 AC adds a probe with at least 30 samples at 390x844 showing the accept-refused box inside the viewport for every sampled scrollY, plus the existing 10 consecutive green runs.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"L6 count change asserts a count, not which item moved\",\n    \"evidence\": \"tests/e2e/test_stepper.py:23 `L6_OBJECTIONS = 4`; judge rejections a3 ($450), a4 ($1,550), a7 ($1,150), f_r5_1 (l6_head.txt); D-059 at memory/ORCHESTRATOR_DECISIONS.md:67\",\n    \"why_it_matters\": \"The count follows D-059, so the update is right. But a count of 4 still passes if a different item replaces a7, so the test does not protect the item the decision is about.\",\n    \"fix\": \"Keep the count and add a presence check that the record-5 'Amount due' amount (a7) is in the judge rejections for the case.\",\n    \"acceptance_test\": \"Mutation: classify 'Amount due' as charge in a scratch copy; the stepper judge tests fail on the presence check, not only on the count.\"},\n   {\"severity\": \"nit\",\n    \"title\": \"Test name says 'everywhere' but the Why dialog now asserts EDIT_WAITING\",\n    \"evidence\": \"tests/e2e/test_rerun_judge.py:308 test_passing_edit_says_edited_by_you_not_ai_checked_everywhere; :318 asserts EDIT_WAITING; :314 keeps the D-045(b) panel wording\",\n    \"why_it_matters\": \"A reader would think the D-045(b) wording is asserted in the Why dialog. It is not.\",\n    \"fix\": \"Rename to match the assertions (for example ..._in_the_panel_and_judge_step); keep the docstring.\",\n    \"acceptance_test\": \"The renamed test passes unchanged in assertions.\"}\n ],\n \"whats_right\": [\n   \"L6 count 4 follows D-059: a3 $450, a4 $1,550 and a7 $1,150 are class unclear and flag f_r5_1 is a rejection on /judges (probe_l6.py, l6_head.txt)\",\n   \"EDIT_WAITING matches memory/contracts/api.md:370 and app/backend/trace.py:289; the D-045(b) panel assertion at test_rerun_judge.py:314 still stands\",\n   \"The shortcut-sheet change waits on a condition (test_polish_r3.py:59, focus back on btn-shortcuts) instead of sleeping, and fails loudly on timeout\"\n ],\n \"questions_for_chris\": [\n   \"After T-149 added the case overview block, the first entry sits at y=552 at 1440x900 (518 at 078c5ae). Is the 520 px 'first entry above the fold' rule (test_polish_r3.py:181) still the product rule, or should the overview block give way? The first Accept is still on screen (y+h < 900).\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T14:51:16.364Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:20.734Z

**tool call — Bash**
````
{
 "command": "git rev-list --count 078c5ae..20b3a42; git rev-list --count 078c5ae..HEAD; git rev-parse --short HEAD",
 "description": "Count commits between 078c5ae and HEAD"
}
````

### User / tool · 2026-11-02T14:51:20.905Z

**tool result**
````
12
15
35d8280
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:23.909Z

**tool call — Bash**
````
{
 "command": "git log --oneline 20b3a42..HEAD; echo \"--- files touched after 20b3a42:\"; git diff --stat 20b3a42 HEAD -- tests/e2e app/frontend/uncovered.js app/frontend/uncovered.css app/frontend/overview.js | tail -8; echo \"--- T-155 card state:\"; python3 tools/board.py show T-155 | sed -n 1,12p | grep -E \"status|commits|rounds\"",
 "description": "Check commits made since 20b3a42 and their effect on reviewed files"
}
````

### User / tool · 2026-11-02T14:51:24.165Z

**tool result**
````
35d8280 feat(backend): D-060 default-deny charges, same-service merge, cites by offset, promoted-charge flags (T-140 r3)
926bf37 feat(backend): T-157 case titles (title on create, PATCH rename, default from first record header), item.rerun_available, next_action on case list and GET case
52ac285 fix(backend): T-141 r5 date distance never exempts a mechanism word; injury prevention is not an event
--- files touched after 20b3a42:
--- T-155 card state:
status: "in_review"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:29.234Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"11 commit|36 cases|9 runs|Reviewed at HEAD|pytest -k 390\" reviews/T-155-staff-engineer.md | cut -c1-220",
 "description": "Locate the lines to correct in the review file"
}
````

### User / tool · 2026-11-02T14:51:29.378Z

**tool result**
````
3:**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at HEAD 20b3a42 (`git rev-parse HEAD`), tree from `git archive 20b3a42`.
8:- **Red at the reviewed commit.** `test_first_screen_shows_entries_and_rows_are_compact` fails 3 of 3 runs at 20b3a42 (`552 < 520`, tests/e2e/test_polish_r3.py:181). The card's green evidence cites 078c5ae, which is 11
29:- Rate: 1 of 6 (stub), 0 of 10 (stub), 0 of 8 (real), so 1 of 24 in total (stub6.txt, stub10.txt, real8.txt). In pytest, `test_code_check_refusal.py -k 390` passed in 9 runs, 36 cases in total (t158_mobile_repeat.txt)
52:   "git log --oneline 078c5ae..20b3a42 (11 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files)",
72:    "evidence": "tests/e2e/test_polish_r3.py:181 `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` on git archive 20b3a42, 3 of 3 runs; at078_density.txt shows 518 at 078c5ae; git log --oneline 078c5a
84:    "evidence": "probe_t158.py: stub 1 of 6 (stub6.txt, `{\"scrollY\": 734, \"box_y\": 805, \"box_bottom\": 937, \"btn_y\": 673, \"below_fold\": true}`), stub 0 of 10 (stub10.txt), real 0 of 8 (real8.txt); box_y = btn
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:31.657Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md",
 "old_string": "**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at HEAD 20b3a42 (`git rev-parse HEAD`), tree from `git archive 20b3a42`.",
 "new_string": "**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at commit 20b3a42 (HEAD was 20b3a42 when I started; `git archive 20b3a42`). HEAD then moved to 35d8280 (`git log --oneline 20b3a42..HEAD`: 52ac285, 926bf37, 35d8280, all backend). None of them touches tests/e2e, app/frontend/uncovered.js, uncovered.css or overview.js. I did not re-run at 35d8280."
}
````

### User / tool · 2026-11-02T14:51:31.741Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-155-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:32.169Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md",
 "old_string": "The card's green evidence cites 078c5ae, which is 11 commits behind HEAD",
 "new_string": "The card's green evidence cites 078c5ae, which is 12 commits behind 20b3a42"
}
````

### User / tool · 2026-11-02T14:51:32.237Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-155-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:32.826Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md",
 "old_string": "In pytest, `test_code_check_refusal.py -k 390` passed in 9 runs, 36 cases in total (t158_mobile_repeat.txt)",
 "new_string": "In pytest, `test_code_check_refusal.py -k 390` passed in 8 runs, 32 cases in total (t158_mobile_repeat.txt)"
}
````

### User / tool · 2026-11-02T14:51:32.910Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-155-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:33.611Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md",
 "old_string": "   \"git log --oneline 078c5ae..20b3a42 (11 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files)\",",
 "new_string": "   \"git log --oneline 078c5ae..20b3a42 (12 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files); git log --oneline 20b3a42..HEAD (HEAD moved to 35d8280, 3 backend commits)\","
}
````

### User / tool · 2026-11-02T14:51:33.680Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-155-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:51:48.694Z

**tool call — Bash**
````
{
 "command": "grep -n \"unc\\[hidden\\]\" app/frontend/uncovered.css; grep -n \"hidden: !opened\" app/frontend/uncovered.js | cut -c1-60; ls reviews | grep T-155",
 "description": "Verify CSS and JS line citations and existing T-155 review files"
}
````

### User / tool · 2026-11-02T14:51:48.882Z

**tool result**
````
4:.unc[hidden] { display: none; }
21:    const panel = el("section", { class: "unc", id, hidde
T-155-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:11.658Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer-r1b.md",
 "content": "# T-155 review (staff-engineer-reviewer), corrected record r1b\n\nThis file is the corrected version of `reviews/T-155-staff-engineer.md`, which the reviewer write guard now keeps as written. Use this file for the board record. Three corrections against the first file: (1) the commit count between 078c5ae and 20b3a42 is 12, not 11; (2) the pytest `-k 390` repeat is 8 runs and 32 cases, not 9 runs and 36 cases; (3) HEAD moved to 35d8280 during the review, and this file says so. The verdict and every finding are unchanged.\n\n**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at commit 20b3a42 (HEAD was 20b3a42 when I started; tree from `git archive 20b3a42`). HEAD then moved to 35d8280 (`git log --oneline 20b3a42..HEAD`: 52ac285, 926bf37, 35d8280, all backend). None of them touches tests/e2e, app/frontend/uncovered.js, uncovered.css or overview.js. I did not re-run at 35d8280.\n\n## What I checked\n\n- **Decisions.** D-059 (ORCHESTRATOR_DECISIONS.md:67) explains the L6 count change, and the count matches the live judge output. The T-134 r2 `edit_to_check` wording matches memory/contracts/api.md:370 and app/backend/trace.py:289. D-058 has no assertion in this diff, so it is not applicable here. The T-144 row-height edit does not follow any decision. Its stated premise is false at HEAD (see F2).\n- **Red at the reviewed commit.** `test_first_screen_shows_entries_and_rows_are_compact` fails 3 of 3 runs at 20b3a42 (`552 < 520`, tests/e2e/test_polish_r3.py:181). The card's green evidence cites 078c5ae, which is 12 commits behind 20b3a42 (F1).\n- **Density edit.** At 078c5ae the original density budgets really fail (`179 <= 150`, `430 <= 420`). f262223 fixed that upstream. At HEAD the original budgets pass, and the collapsed list costs 0 px. The T-155 edit therefore removes a measure that was not needed and discounts 8 px on list rows (F2).\n- **T-158.** The 390px refusal box really can end below the fold. The box sits 132 px under the Accept button, so it is out of an 844 px viewport whenever the button is lower than y=580. One of 24 probe samples hit that (scrollY 734, box bottom 937). The \"about 50%\" rate on the card was not reproduced. T-158 is the right owner for the product fix (F3).\n- **L6 count and EDIT_WAITING.** Both follow the recorded decisions. The count assertion is weak on identity (F4), and one test name is stale (F5).\n\nEvidence files: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-155/` (probe scripts and outputs). Scratch snapshot: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1/`.\n\n## Findings\n\n**F1 (major). The card's green claim cites 078c5ae, not the reviewed commit. The first-screen test is red at 20b3a42 and is not triaged.**\nRepro: `E2E_BASE_URL=http://127.0.0.1:7955 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -k first_screen` on the 20b3a42 archive prints `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` at tests/e2e/test_polish_r3.py:181. It failed in 3 of 3 runs. At 078c5ae the same line read `[[518, ...` (artifacts/review-evidence/T-155/at078_density.txt), so the red came in after that sha. The orchestrator note at 14:39 names it. The handoff triage does not.\n\n**F2 (major). The T-144 row-height edit weakens the compact-row budget on a false premise. The density reds it calls stale were real.**\n- The density reds at 078c5ae were real: `assert 179 <= 150` and `assert 430.09375 <= 420` (at078_density.txt). f262223 (\"the uncovered list opens from a short link in the entry head so compact rows keep their height\") is in 078c5ae..20b3a42 and is the fix.\n- At 20b3a42 the original measure passes. I removed only line 181 from the pre-change file (`git show 20b3a42^:tests/e2e/test_polish_r3.py`). Then `pytest -k \"first_screen or 390\"` gave `2 passed`. That run includes the line-182 Accept-on-first-screen check, so that check passes too. The current file with the same single-line removal also gave `2 passed`.\n- The collapsed list costs 0 px at HEAD. `app/frontend/uncovered.js:21` sets `hidden: !opened.has(entry.id) || null`, and `app/frontend/uncovered.css:4` is `.unc[hidden] { display: none; }`. On the sample at 1440x900 and 390x800, the list is `display: none` with height 0 and computed `margin-top: 8px` on 3 of 9 rows (artifacts/review-evidence/T-155/rows_head.txt).\n- The edit at tests/e2e/test_polish_r3.py:168-172 says \"~30-57 px with its margins\". The ROW_BOXES_JS function subtracts that margin from every row that carries a list, and it is used at :180 and :203. So those rows read 8 px short of the rendered height.\n- The constraint itself is real. The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen. The edit does not make that constraint go away, but it does make the measure wrong.\n\n**F3 (minor). T-158 holds the real regression. The \"about 50%\" rate on the card is not reproduced.**\n- Mechanism: the box is `btn_y + 132` at every sample. It is below 844 whenever btn_y is greater than 580. One sample hit it: `{\"scrollY\": 734, \"box_y\": 805, \"box_bottom\": 937, \"btn_y\": 673, \"below_fold\": true}` (artifacts/review-evidence/T-155/stub6.txt).\n- Rate: 1 of 6 (stub), 0 of 10 (stub), 0 of 8 (real), so 1 of 24 in total (stub6.txt, stub10.txt, real8.txt). In pytest, `test_code_check_refusal.py -k 390` passed in 8 runs, 32 cases in total (artifacts/review-evidence/T-155/t158_mobile_repeat.txt). Load averages were 21 to 24 during these runs (`uptime`). I cannot say what the card's machine was doing.\n- The test is correct and stays unchanged. The T-158 note should cite the geometry measurement, not the 3-of-6 rate.\n\n**F4 (minor). The L6 count change asserts a count, not which item moved.**\n- `L6_OBJECTIONS = 4` (tests/e2e/test_stepper.py:23). The four rejections on /judges are a3 (unclear $450), a4 (unclear $1,550), a7 (unclear $1,150) and flag f_r5_1 (artifacts/review-evidence/T-155/l6_head.txt lists the rejection ids). The amount values come from a probe run whose output I did not save as an artifact (`probe_l6b.py` in the scratch folder).\n- The count follows D-059. Whether a7 is correct billing is outside my lens.\n- Because the test checks only the count, another item could replace a7 and the test would still pass.\n\n**F5 (nit). A test name overstates what it asserts.**\n- tests/e2e/test_rerun_judge.py:308 `test_passing_edit_says_edited_by_you_not_ai_checked_everywhere` now asserts `EDIT_WAITING` for the Why dialog (:318). The D-045(b) wording is still asserted in the panel row (:314). The name should say panel and judge step.\n\n## Notes on what I did not run\n\n- The full tests/e2e suite and tests/unit were not run. The brief asked for the changed files and T-158.\n- No mutation check was run on the edited files. Acceptance tests for F2 and F4 are written as proposals and have not been run.\n- I did not run `board.py review`.\n- My two test servers (127.0.0.1:7955 and 127.0.0.1:7956) were stopped; their listener PIDs were 64260 and 86463, with bash wrappers 64258 and 86406. Ports closed. The shared :7860 app was not touched.\n\n```json\n{\"card\": \"T-155\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 20b3a42 (tests only: tests/e2e/test_polish_r3.py, tests/e2e/test_rerun_judge.py, tests/e2e/test_stepper.py); reviewed at 20b3a42 from git archive in a scratch snapshot; own server 127.0.0.1:7955 (fixture backend, ZLAYT_MODE=local, E2E_REQUIRE_DB=1); comparison server 127.0.0.1:7956 from archive 078c5ae; library case case_lib06_lop_billed_vs_adjusted and the sample case; HEAD moved to 35d8280 after my start (backend only, not re-run)\",\n \"exercised\": [\n   \"python3 tools/board.py show T-155; read personas/staff-engineer.md\",\n   \"git show --stat 20b3a42; git show 20b3a42 -- tests/ (full test diff); git rev-parse HEAD -> 20b3a42 at start\",\n   \"git log --oneline 078c5ae..20b3a42 (12 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files); git log --oneline 20b3a42..HEAD (35d8280 now HEAD; 3 backend commits)\",\n   \"read memory/ORCHESTRATOR_DECISIONS.md D-058 (line 66), D-059 (67), D-060 (68); memory/contracts/api.md lines 365-374; app/backend/trace.py:289; app/frontend/uncovered.js:21; app/frontend/uncovered.css:4; app/frontend/tokens.css:43; commit f262223 subject\",\n   \"git archive 20b3a42 extracted to scratch T155_r1/head (2217 files); 48 untracked tests/fixtures/llm files in the working tree not copied; no FIXTURE_MISS occurred\",\n   \"E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=<scratch>/e2e.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_code_check_refusal.py -q -rfEs -> 1 failed, 83 passed, 128.70s; failure test_polish_r3.py::test_first_screen_shows_entries_and_rows_are_compact at :181 (552 < 520)\",\n   \"3 repeats of test_polish_r3.py -k first_screen on 20b3a42: 552 each run\",\n   \"pytest test_code_check_refusal.py -k 390 x8 on 20b3a42: 4 passed each run, 32 cases (artifacts/review-evidence/T-155/t158_mobile_repeat.txt)\",\n   \"probe_t158.py (Playwright 390x844, stub 6 and 10, real 8 samples): 1 of 24 below the fold (stub6.txt, stub10.txt, real8.txt)\",\n   \"probe_rows.py on 20b3a42: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows at 1440x900 and 390x800 (rows_head.txt)\",\n   \"pre-change test file (git show 20b3a42^) and current file, each with only line 181 removed: pytest -k 'first_screen or 390' -> 2 passed each\",\n   \"server 127.0.0.1:7956 from archive 078c5ae: density budgets fail 179 <= 150 and 430.09 <= 420; first-entry y 518 (at078_density.txt)\",\n   \"probe_l6.py on 20b3a42: judge rejections a3, a4, a7, f_r5_1 (l6_head.txt); amount values from probe_l6b.py (output not saved)\",\n   \"uptime: load average 21 to 24 during the runs\",\n   \"stopped only my PIDs (listeners 64260 and 86463 and their bash wrappers 64258 and 86406), verified via lsof and cwd; ports 7955 and 7956 closed; shared :7860 untouched\",\n   \"not run: full tests/e2e, tests/unit, evals, mutation checks; board.py review not run\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"test_integrity\": 2, \"triage_accuracy\": 2, \"evidence_matches_reviewed_commit\": 2, \"decision_traceability\": 4, \"determinism\": 4},\n \"findings\": [\n   {\"severity\": \"major\",\n    \"title\": \"Green claim cites 078c5ae, not the reviewed commit; first-screen test red at 20b3a42 and not triaged\",\n    \"evidence\": \"tests/e2e/test_polish_r3.py:181 `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` on git archive 20b3a42, 3 of 3 runs; at078_density.txt shows 518 at 078c5ae; git log --oneline 078c5ae..20b3a42 lists 12 commits; card AC evidence says 'clean HEAD 078c5ae ... 281 passed, 2 skipped, 1 failed'\",\n    \"why_it_matters\": \"The AC requires a green clean-HEAD run with each failure explained on the card. The commit under review is red for a test the card neither fixes nor explains, and the cited evidence describes another tree. A gate reviewer reproducing the card gets a different result.\",\n    \"fix\": \"Re-run the full tests/e2e on git archive 20b3a42 with E2E_REQUIRE_DB=1, cite that sha and the counts in the AC evidence, and record on the card the owner of the first-screen failure (T-149 r2) or file a card. Do not loosen line 181 inside this card.\",\n    \"acceptance_test\": \"Full tests/e2e on the 20b3a42 archive: every failure has a card note naming its owner or a passing result; the AC evidence cites 20b3a42.\"},\n   {\"severity\": \"major\",\n    \"title\": \"T-144 row-height edit weakens the compact-row budget on a false premise; the density reds it calls stale were real\",\n    \"evidence\": \"at078_density.txt: `assert 179 <= 150` and `assert 430.09375 <= 420` at 078c5ae; f262223 fixed it in 078c5ae..20b3a42. At 20b3a42 the original measure passes: pre-change file with line 181 removed, `-k 'first_screen or 390'` -> 2 passed. rows_head.txt: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows. app/frontend/uncovered.js:21 `hidden: !opened.has(entry.id) || null`; app/frontend/uncovered.css:4 `.unc[hidden] { display: none; }`. tests/e2e/test_polish_r3.py:168-172 comment '~30-57 px with its margins' and ROW_BOXES_JS subtracting extra; used at :180 and :203.\",\n    \"why_it_matters\": \"The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen and is still a real constraint. The edit removes a term that is zero at HEAD, the stated reason is false, and it discounts 8 px of an unrendered margin on list rows, so the budget reads short. Any future visible collapsed element would be hidden from the budget under the same comment.\",\n    \"fix\": \"Revert ROW_BOXES_JS to the pre-20b3a42 measure (r.height) at tests/e2e/test_polish_r3.py:170-172, :180 and :203, and remove the T-144 comment at :168-169. Leave line 181 as it is (see F1).\",\n    \"acceptance_test\": \"On the reverted file, `pytest tests/e2e/test_polish_r3.py -k 'density or 390'` passes at 20b3a42. Mutation in a scratch copy: `.unc[hidden]{display:block}`; the 390 or 1440 budget test must fail. If it does not, the card must say the budget does not guard the list area.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"T-158 holds the real regression, but the about-50% rate on the card is not reproduced\",\n    \"evidence\": \"probe_t158.py: stub 1 of 6 (stub6.txt, `{\\\"scrollY\\\": 734, \\\"box_y\\\": 805, \\\"box_bottom\\\": 937, \\\"btn_y\\\": 673, \\\"below_fold\\\": true}`), stub 0 of 10 (stub10.txt), real 0 of 8 (real8.txt); box_y = btn_y + 132 in every sample; pytest -k 390 passed 32 cases in 8 runs (t158_mobile_repeat.txt); uptime load 21-24\",\n    \"why_it_matters\": \"The mechanism is real and T-158 (frontend) is the right owner, so leaving test_code_check_refusal.py unchanged is correct. The 3-of-6 rate is not reproduced, and a repro should rest on measured geometry, not a rate.\",\n    \"fix\": \"On T-158, replace the about-50% claim with the geometry measurement (btn_y, scrollY, box bottom) and keep the test unchanged.\",\n    \"acceptance_test\": \"T-158 AC adds a probe with at least 30 samples at 390x844 showing the accept-refused box inside the viewport for every sampled scrollY, plus the existing 10 consecutive green runs.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"L6 count change asserts a count, not which item moved\",\n    \"evidence\": \"tests/e2e/test_stepper.py:23 `L6_OBJECTIONS = 4`; judge rejections a3 ($450), a4 ($1,550), a7 ($1,150), f_r5_1 (l6_head.txt lists the ids; amounts from probe_l6b.py, output not saved); D-059 at memory/ORCHESTRATOR_DECISIONS.md:67\",\n    \"why_it_matters\": \"The count follows D-059, so the update is right. But a count of 4 still passes if a different item replaces a7, so the test does not protect the item the decision is about.\",\n    \"fix\": \"Keep the count and add a presence check that the record-5 'Amount due' amount (a7) is in the judge rejections for the case.\",\n    \"acceptance_test\": \"Mutation: classify 'Amount due' as charge in a scratch copy; the stepper judge tests fail on the presence check, not only on the count.\"},\n   {\"severity\": \"nit\",\n    \"title\": \"Test name says 'everywhere' but the Why dialog now asserts EDIT_WAITING\",\n    \"evidence\": \"tests/e2e/test_rerun_judge.py:308 test_passing_edit_says_edited_by_you_not_ai_checked_everywhere; :318 asserts EDIT_WAITING; :314 keeps the D-045(b) panel wording\",\n    \"why_it_matters\": \"A reader would think the D-045(b) wording is asserted in the Why dialog. It is not.\",\n    \"fix\": \"Rename to match the assertions (for example ..._in_the_panel_and_judge_step); keep the docstring.\",\n    \"acceptance_test\": \"The renamed test passes unchanged in assertions.\"}\n ],\n \"whats_right\": [\n   \"L6 count 4 follows D-059: a3 $450, a4 $1,550 and a7 $1,150 are class unclear and flag f_r5_1 is a rejection on /judges (probe_l6.py, l6_head.txt)\",\n   \"EDIT_WAITING matches memory/contracts/api.md:370 and app/backend/trace.py:289; the D-045(b) panel assertion at test_rerun_judge.py:314 still stands\",\n   \"The shortcut-sheet change waits on a condition (test_polish_r3.py:59, focus back on btn-shortcuts) instead of sleeping, and fails loudly on timeout\"\n ],\n \"questions_for_chris\": [\n   \"After T-149 added the case overview block, the first entry sits at y=552 at 1440x900 (518 at 078c5ae). Is the 520 px 'first entry above the fold' rule (test_polish_r3.py:181) still the product rule, or should the overview block give way? The first Accept is on screen (its y+h < 900 check passes in the variant run).\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T14:52:11.861Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer-r1b.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:14.442Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate --help 2>&1 | head -8; echo \"---\"; python3 tools/board.py validate 2>&1 | tail -15",
 "description": "Run the read-only board validator"
}
````

### User / tool · 2026-11-02T14:52:14.808Z

**tool result**
````
usage: board.py validate [-h] [path]

positional arguments:
  path

options:
  -h, --help  show this help message and exit
---
ok (159 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:16.445Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-155-staff-engineer-r1b.md 2>&1 | tail -5; python3 tools/board.py validate reviews/T-155-staff-engineer.md 2>&1 | tail -3",
 "description": "Validate both T-155 review files with the read-only validator"
}
````

### User / tool · 2026-11-02T14:52:16.680Z

**tool result**
````
ok (1 file(s))
ok (1 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:26.421Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t155_e2e_triage_patterns.md",
 "content": "---\nname: t155-e2e-triage-patterns\ndescription: T-155 r1 (20b3a42, changes): green claim cited an older sha, \"stale\" density reds were real at 078c5ae, hidden collapsed list measures 0 px with an 8px margin, refusal box sits btn_y+132\nmetadata:\n  type: project\n---\n\nT-155 (test-only triage of 9 e2e reds) reviewed at 20b3a42. Verdict changes: 0 blockers, 2 majors, 2 minors, 1 nit. Review: reviews/T-155-staff-engineer-r1b.md (corrected record; the first file is write-once and has two count errors).\n\n- **Green claim on an older sha.** The card's AC evidence was a run at 078c5ae; 20b3a42 has 12 more commits. At 20b3a42 test_polish_r3.py:181 (first entry y<520) fails 3 of 3 (y=552, the T-149 overview block). It was not triaged on the card.\n- **\"Stale test\" was the wrong direction.** At 078c5ae the original density budgets really failed (179 > 150, 430 > 420). f262223 fixed it upstream. At 20b3a42 the original measure passes, so the T-144 edit to ROW_BOXES_JS was unnecessary.\n- **Hidden list.** The T-144 list is `display:none` when closed (uncovered.css:4, uncovered.js:21). It has height 0 but its computed margin-top is 8px, so the edit's subtraction under-measures list rows by 8px. The \"30-57 px\" comment is false at HEAD.\n- **Refusal box geometry (T-158).** The accept-refused box sits at btn_y + 132 and is below an 844px fold when btn_y > 580. One of 24 samples hit it (scrollY 734). The card's \"about 50%\" rate did not reproduce. Mechanism real, rate overstated.\n- **Load.** uptime load averages were 21 to 24 during these runs. Flake rates measured on this machine may not match a loaded one.\n\n**Why:** a \"stale test\" triage is a claim about history. It has to be tested at the sha the red was seen on, not inferred from the diff.\n**How to apply:** for any e2e triage, run the pre-change test file at the card's cited sha and at HEAD. Count commits between them. For any layout budget, check the DOM state (display, height, computed margin) of anything the test excludes.\n\nRelated: [[feedback_evidence_sha_vs_commit]], [[project_t136_r2_patterns]], [[project_t158_mobile_geometry]], [[feedback_review_write_once]].\n"
}
````

### User / tool · 2026-11-02T14:52:26.548Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t155_e2e_triage_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:29.032Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_evidence_sha_vs_commit.md",
 "content": "---\nname: feedback_evidence_sha_vs_commit\ndescription: a card's green run and its \"stale test\" triage can cite an older sha; run the cited test at that sha and at the reviewed commit before accepting either, and count the commits between them\nmetadata:\n  type: feedback\n---\n\nBefore accepting \"full suite green at clean HEAD\" or \"this red is a stale test\", check which sha the evidence ran on. Run `git rev-list --count <evidence-sha>..<commit>` and run the disputed test file at both shas. If the file at the evidence sha fails the same way the card says it is stale, the triage is backwards.\n\n**Why:** T-155 r1 (20b3a42): the AC evidence was a run at 078c5ae, 12 commits behind. At 078c5ae the density budgets really failed (179 > 150); a later frontend fix (f262223) cured them. The card called them stale and loosened the budget with a false comment. A first-screen red at the reviewed commit was not on the card.\n\n**How to apply:** in any e2e review, record the evidence sha and the reviewed sha on the first line of the exercised list. Use an archive per sha (git archive | tar -x into a unique scratch dir, own port, E2E_REQUIRE_DB=1). If HEAD moves during the review, say so and state which sha the findings are for.\n\nRelated: [[project_t155_e2e_triage_patterns]], [[project_round2_snapshot_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T14:52:29.188Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_evidence_sha_vs_commit.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:32.353Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T14:52:32.364Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E; T-124 d56328a pass: one-way and substring id check
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
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1-r2 (fail) and r4 3223e50 (changes): H3V5 label contradicts judge rule 1, reachability mutants red, relabel second-agent test
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263, r2 8bc7f90, r3 db08276 (all fail): bare figures vanish in prose/CMS/balance-forward, second balance-forward overwrites, counter blind to bare numbers, mutant label checks
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4 6bca71e (fail): repeated statement totals overwritten while counted as placed, skipped billing records leave complete true, stray bare-number definition gap
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untested); T-099 r2 f345bc8 pass: case_count clause untested, F2 debt needs SCOPE_CUTS row
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — r5 690a0e3 fail: ledger+CMS totals share a [-1] slot, bare charge beyond TOL=8 dropped, complete ignores reconciliation checks
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — r1 4c5f9bf changes; r2 fdc2506 pass: guard tested for golden only, recheck test passes via backstop, latest.json blocks run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — dd84122 fail: summary-only edit bypasses accept guard, gate recomputes 2 of 5 checks, notes print AI wording
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — r1 fail; r2b fail; r3 changes; r4 8a2b934 changes: UB-04 room total vs other_figures, offset comparisons open on Q1, redundant holder branches
35	- [Exact count vs presence](feedback_exact_count_vs_presence.md) — presence oracles miss a dropped second copy; run the test module's random generator with exact per-record counts
36	- [T-100 r2 patterns](project_t100_r2_patterns.md) — r2 288c1d3 changes: shared new_tokens, vocabulary narrower than _EN_* lists, fixture eval diff method, Spanish branches unpinned
37	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — 1335f21 pass: choke point verified by grep+probe; unchecked removed narrative text still printed; 4 unrelated unit failures
38	- [T-106 patterns](project_t106_review_patterns.md) — c2a5d1f changes: pdf_hidden regex bypass via from-subprocess-import, notes-only fix leaves narrative panel printing, loose fixture filter
39	- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — r1 d3e127c changes; r2 a271014 pass: masked route checks, sentences_reason unrendered, store.py broad except, clone for .git count
40	- [Shared scratchpad](feedback_shared_scratchpad.md) — scratchpad is shared with other agents: unique card-round subdirs, diff -rq archive checks, no backgrounded setup chains
41	- [T-109 doc-vs-code patterns](project_t109_doc_vs_code_patterns.md) — r1 changes; r2 4bdf366 fail (model conflicts dropped); r3 changes; r4 425095f pass: cite range off by blank lines, scan a-side keys, fix-up scope
42	- [T-106 r2 audit patterns](project_t106_r2_audit_patterns.md) — r2 e3a62fa changes: AST audit misses os alias/ctypes/asyncio, ps argv tail unpinned, rest-of-app still regex
43	- [T-102 stale-calibration patterns](project_t102_stale_calibration_patterns.md) — r1 276991b fail; r2 03206ca changes: stale fix verified via clone (archive can't discriminate), T-096 owner still missing, wrong-dir guard is a literal pin
44	- [T-115 e2e/curated patterns](project_t115_e2e_curated_patterns.md) — r1 400a8c0 changes: evidence cites older commit than HEAD, regen re-keys prompts with scripted answers, ZLAYT_DB skips, inner_text race
45	- [T-112 trim patterns](project_t112_trim_patterns.md) — r1 afcde06, r2 1b93582 changes: stems then abbreviations over-trim, doc/D-054 on old rule, unpinned counter
46	- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes; r2 changes (p gate); r3 c559ce2 pass: vis() first-frame poll, count artifact without sha
47	- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof listener before killing own servers
48	- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction single-source refactor, write-once errata in my r2 files
49	- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — r1 93de5f2: closed-list fragment guard, preamble flag never served by API, T-127 pass with unpinned from/to
50	- [T-120 r3 patterns](project_t120_r3_patterns.md) — f7829c1 pass: strip-then-scan verified, MS honorific collision, unpinned gate mutant, count errata in r3 file
51	- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — T-128 r2 changes: structural rule leaves dependent tail clauses, deny gap; T-129 r2 pass: tests flag-only, relative sweep path false-kills
52	- [T-133 lexicon patterns](project_t133_lexicon_review_patterns.md) — r1 e79c3aa/1218b2e changes: bare 'History:' HPI over-flag, attribution deny untested, ';' truncates excerpt, deny has no source
53	- [T-113/T-122 patterns](project_t113_t122_patterns.md) — 5dfba88: held-out control written with the prompt naming its noun, closed-list word mutants, vacuous order test; T-122 regression created by T-113 commit
54	- [T-132 r2 / T-128 r3 patterns](project_t132_t128_r2r3_patterns.md) — both changes: wrap inside chained clause, 2-letter header labels, participle before removed with-tail, prefix-oracle fuzz with old-code control
55	- [T-133 r3 patterns](project_t133_r3_patterns.md) — 4065ef2 changes: r2 header guard dropped Past/Medical/Surgical history flags, ';' suppression recall gap, live eval owed
56	- [T-133 r4 patterns](project_t133_r4_patterns.md) — 128942d changes (final): \s matches newline so line-start bare History: flags, parity tests blind to gains, 13d "before T-133" premise false
57	- [T-133 r5 patterns](project_t133_r5_patterns.md) — 15be212 pass: prior-ending x separator grid, CR-only kills \s but CRLF/blank cannot, eval grep must read header line, 13d PMH overstated
58	- [Regex multiline probe](feedback_regex_multiline_probe.md) — probe \s and line-break variants of "line start" guards; \s matches newline under re.M on raw text
59	- [Differential probe vs prior build](feedback_differential_probe_prior_build.md) — run the probe set on pre-fix and HEAD archives; FLAG-to-quiet flips reveal regressions the acceptance list misses
60	- [T-134 unconfirmed-edit patterns](project_t134_unconfirmed_edit_patterns.md) — r1 5fb338d changes; r2 db1d8d5 changes: judge_report human_overrides counts open edit, N3/N5 mutants survive
61	- [GATE-M2 patterns](project_gate_m2_patterns.md) — 0c24f5f fail: deadline skips judge_entries so entries compose verified, timed-out rerun deletes pending, no live ship-bar report at HEAD
62	- [T-113 r2 patterns](project_t113_r2_patterns.md) — bea3984 changes: git-derived held-out audit checked with throwaway repos, count/real-data unpinned (7 of 14 mutants green), in-place edit blind spot, 13c history side only
63	- [T-132 r4 patterns](project_t132_r4_patterns.md) — fc60471 changes: 'Label:' regex drops condition lines ('Left wrist swollen:'), git archive from a subdir exports empty tree, control-vs-HEAD visibility diff, equivalence of linearised helpers
64	- [T-132 r5 patterns](project_t132_r5_patterns.md) — ed45b4a/5de16d3 pass: closed-list stop leaves ALL-CAPS condition lines dropped (minor), AC count off by one, control-first probe expectations, hook denies rm with expansion
65	- [T-134 r3 / T-138 patterns](project_t134_r3_t138_patterns.md) — both changes: text fix missed review step + gate headline, stale rejudge claim, snapshot aliases mutated dict, HEAD broken by sibling commit
66	- [T-145/T-146 patterns](project_t145_t146_patterns.md) — T-145 pass: shared JUDGE_NOT_RUN sentence mislabels real failure; T-146 changes: failed (done_with_errors) re-run wipes accepted entries, state-only snapshot
67	- [T-141 r2 patterns](project_t141_r2_patterns.md) — 68b8685 changes: clause word list still loses conflicts (prior to/no history of), stored run summary stale after confirm_date, sibling test hunk red at commit
68	- [T-134 r4 / T-138 r2 patterns](project_t134_r4_t138_r2_patterns.md) — 4f416a4 changes, b7a7ead pass: backend D-058 wording fixed but UI regex keeps old stays-blocked sentence, identical-text re-pick test, alias and leak controls
69	- [Frontend text coupling](feedback_frontend_text_coupling.md) — when a backend sentence changes, grep app/frontend for the old phrase and regexes over it (server-text swap silently falls back)
70	- [T-136 r2 patterns](project_t136_r2_patterns.md) — 07c7558 changes: private-server fallback to :7860, red e2e predating the card, flaky mobile and open_rail tests, client copy of gate rule
71	- [T-146 r2 patterns](project_t146_r2_patterns.md) — 2db6ad2 changes: keep-whole rule keyed on judge/stub only; flags-down downgrades corroborated flag, SUMMARY_NOT_IN_QUOTE overwrites
72	- [T-140 r2 patterns](project_t140_r2_patterns.md) — a0e2639 changes: tests read untracked reviewer file (clean pytest aborts), after-figure position gap, reclassify skips duplicate/total flags
73	- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed
74	- [T-141 r4 patterns](project_t141_r4_patterns.md) — 93a2ffc changes: month-year two-month cut-off hides 'Rear-ended in October 2025' while bare-year fix flipped; pinned variant contradicts r3 acceptance
75	- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — r1 changes: untracked ledger read at import breaks clean collection, golden-named test without golden compare, git show not working tree, HEAD moved 3x
76	- [T-146 r3 patterns](project_t146_r3_patterns.md) — bf53087 changes: equal-rank check worsening replaces decided item silently, reword fails case, rerun_note no UI consumer
77	- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned
78	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:34.807Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned\n",
 "new_string": "- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned\n- [T-155 e2e triage patterns](project_t155_e2e_triage_patterns.md) — 20b3a42 changes (r1b): green claim on older sha, \"stale\" density reds were real, hidden list 0 px + 8px margin, refusal box btn_y+132\n- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a \"stale test\" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between\n"
}
````

### User / tool · 2026-11-02T14:52:34.918Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:52:38.344Z

T-155 verdict is changes (0 blockers, 2 majors): `/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer-r1b.md` is the corrected record, because the write guard kept the first file `/Users/arsis/zlayt-pm-project/reviews/T-155-staff-engineer.md` with two count errors.
