# Subagent: T-119 r3 staff review (T-119 r3 staff review)

Source: `agent-a3cef1be9f4780850.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:22:18.620Z

This is the round-3 review of board card T-119 (commit c559ce2) in /Users/arsis/zlayt-pm-project. Read reviews/T-119-staff-engineer-r2.md and `python3 tools/board.py show T-119`.

Verify these on a `git archive HEAD` copy, on your own port:
- The new test, test_p_focuses_the_record_pane_only_from_an_item_row, fails when you apply mutB to app/frontend/sidebyside.js:102 in your copy, and passes on HEAD.
- The test_code_check_refusal.py vis() polling has no sleeps. Run that file 5 times.
- The minors are fixed.

Write reviews/T-119-staff-engineer-r3.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Stop only your own PIDs. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:20.660Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:22:20.681Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:20.886Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-119-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-02T11:22:20.894Z

**tool result**
````
1	# T-119 review, round 2: staff-engineer-reviewer
2	
3	**Verdict: changes.** No blocker. Of the two round-1 majors, the Tab/Enter/Space-only R-RV-4 test is fixed and kills its mutants. The row-only key test is mostly fixed: it kills four of five scratch mutants, but the `p` gate (`app/frontend/sidebyside.js:102`) is still untested. That was the round-1 mutB, whose acceptance test said the new E2E "fails on both mutants". Three round-1 minors are unchanged.
4	
5	## What I ran
6	
7	- Pinned to `git archive e1ce8dc` (HEAD when I started: `e1ce8dc620e6ec0778320456ac79a25f1832bfee`; card commit d9efc5c). Archive file count 1979 equals `git ls-tree -r HEAD`. HEAD later moved to c26ff04; `git diff --stat e1ce8dc HEAD -- app/frontend tests/e2e` shows only a two-line `tests/e2e/conftest.py` comment change (d56328a), so the pin still holds.
8	- Own fixture server on 127.0.0.1:7991 (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch>`). Both servers (7991, 7992) stopped by PID; ports verified closed.
9	- `tests/e2e/test_polish_r3.py`: **18 passed** in 23.6s.
10	- Full `tests/e2e`, run twice. Run 1: **1 failed, 190 passed, 1 skipped** in 253s; the failure was `test_code_check_refusal.py:110` (`vis(...)` "the reason must be on screen beside the button"). Run 2: **191 passed, 1 skipped** in 253s. The failing file then passed 3 of 3 isolated runs (23 passed each). The handoff's 176 passed + 16 skipped = 192 equals my 191 + 1 skipped = 192 collected; the 15 extra skips are the ZLAYT_DB gates, which I set.
11	- Mutants on a second scratch copy (own port 7992 and sqlite), control green (18 passed) before and after each swap:
12	  - A, `review.js` letter keys fall back to the first row (`const row = RV.itemRowOf(t) || document.querySelector("[data-item-id]")`): **killed**, `test_letter_keys_do_nothing_from_body_export_or_an_input` fails.
13	  - B, `sidebyside.js:102` `p` without `ZL.rv.itemRowOf(t)`: **survived 18 of 18, and survived 129 of 129** across all 8 e2e files that press keys (`test_code_check_refusal, test_keyboard_mobile, test_input, test_rerun_judge, test_suggestions, test_polish_r3, test_stepper, test_side_by_side`).
14	  - C, `batch.js` Shift+A without the row gate: **killed**, same test.
15	  - D, `review.js` `typing(t)` exemption removed: **killed**, same test (the `jadA` typed-not-run assertion).
16	  - E, `review.js` dialog-open swallow removed: **killed**, `test_letter_key_with_a_window_open_says_so`.
17	- Probe (scratch, `artifacts/review-evidence/T-119/r2-probe_p.py`): select an item so the pane is on, blur to body, press `p`. Unmutated HEAD: passes (focus stays). Mutant B: fails with `p moved focus from the body: BODY: -> DIV:sbs-body`. So B has a real effect that no committed test sees.
18	- Read `tests/e2e/test_polish_r3.py` in full, the `test_stepper.py:204` retry, `review.js:309-345`, `sidebyside.js:98-106`, `batch.js:124-128`. Greps for `sleep(`, `wait_for_timeout`, `keyboard.press("Tab")`, `inner_text()` after a parent wait, `pytest.skip`, and the stale tray copy in `conftest.py`.
19	- Evidence in `artifacts/review-evidence/T-119/`: `r2-e2e-full-run1.txt`, `r2-e2e-full-run2.txt`, `r2-mutants-polish.txt`, `r2-probe_p.py`, `r2-mut.py`.
20	
21	## Judgement of the new tests
22	
23	- **Negative key test** (`test_polish_r3.py:74-102`): asserts decision count, open dialogs and typed text (not implementation). It drives j, a, d, Shift+A and `?` from the body, from Export, from the edit textarea and from the sort control. The "active" field in `_snapshot` compares the snapshot to itself, so it proves nothing, but the next line (`closest('[data-item-id]')` is falsy) does check that focus did not enter a row. Real, mutation-tested for decision keys. Gap: `p` (and `k o e r` only through the shared gate, which mutant A covers) and the header; `p` has its own gate and is not pressed.
24	- **Dialog case** (`:105-111`): `o` then `a`, expects the "Press Escape" notice and zero accepted. Killed mutant E.
25	- **Tab/Enter/Space-only flow** (`:115-143`): no `.focus()` on the path; `tab_until` raises if the target is never reached, so a lost skip link, a lost tab stop or a swallowed Enter fails it. It asserts the real outcome (`data-review="dismissed"`, `export-letter` visible, `copy-confirm`, then `Copied the treatment section`). Setup accepts go through the API, which is fine for a keyboard test of one item plus export. It covers one item, not "the sample case", so R-RV-4 is met in kind, not in full; I rate that as a note, not a finding.
26	- **Determinism:** no `wait_for_timeout`. The one `time.sleep(.5)` (`:21`) is a bounded `/status` poll for the run to reach `ready` (150 s cap, asserts `ready`), the same helper pattern as `test_stepper.py:17`. Assertions after UI actions use `expect(...)` retries. No wall clock, no network beyond the local fixture server.
27	- **`test_stepper.py:204`:** now `expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(...))`, a retrying assert. Round-1 minor 4 is fixed. No `inner_text()` follows a parent `wait_for` for that testid.
28	
29	## Round-1 minors
30	
31	- Minor 3 (stale tray-flag copy): **not fixed.** `tests/e2e/conftest.py:45` still says "AI suggested a flag that the second check did not confirm; it is not in the letter."
32	- Minor 4 (`inner_text` at :204): **fixed**, see above.
33	- Minor 5 (the only skip hides ADR-005): **unchanged.** `tests/e2e/test_ladder_gate.py:37` still skips; it is the one skip in both full runs. Pre-existing and not in the T-119 diff.
34	- Docstring from round-1 finding 2: `tests/e2e/test_keyboard_mobile.py:9` still says "Tab to the first queue item" and `:10` calls `.focus()`. The Tab test now exists elsewhere, so this is a misleading comment only.
35	
36	## Findings
37	
38	1. **major: the `p` gate is untested; the new negative test does not fail on round-1 mutB.** Evidence: mutant B (`app/frontend/sidebyside.js:102`, `&& ZL.rv && ZL.rv.itemRowOf(t)` removed) gives 18 passed on `test_polish_r3.py` and 129 passed across the 8 keyboard files (`r2-mutants-polish.txt`); the probe fails on it with `p moved focus from the body: BODY: -> DIV:sbs-body`. The test presses only `j a d Shift+A ?` (`test_polish_r3.py:79,85,93,100`). Round-1 finding 1 asked for a d j k p o e r and its acceptance said it fails on both mutants. Why it matters: `p` is a single-character shortcut that acts from the page body and Export, which is the WCAG 2.1.4 rule T-060 made a blocker; it can regress without CI noticing. Fix: add `p` to the key lists in `test_letter_keys_do_nothing_from_body_export_or_an_input`, after first putting an item in the pane (focus a row, press `p`, Escape, then blur) so the pane is visible; assert focus stays on body or Export. Acceptance: the test passes on HEAD and fails on mutant B (`r2-probe_p.py` is the reference).
39	
40	2. **minor: full-suite flake in `test_code_check_refusal.py:110`.** Evidence: run 1 failed `test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action` with "the reason must be on screen beside the button, not below the fold"; run 2 passed; the file alone passed 3 of 3. `vis()` (`:93-95`) reads `bounding_box()` once, after `expect(...).to_be_visible()`, against the viewport. This is a one-shot layout read after a click. File is outside the T-119 diff, but the card's AC says "full e2e green". Fix: wait for scroll to settle before the check, e.g. `expect` on a stable box position, or poll `vis` with a retrying assertion. Acceptance: 5 consecutive full-suite runs without this failure.
41	
42	3. **minor: stale tray-flag copy still in the E2E contract (round-1 minor, unchanged).** Evidence: `tests/e2e/conftest.py:45`. Fix: use the T-060 sentence from `app/frontend/timeline.js:135`. Acceptance: `grep -n "did not confirm; it is not in the letter" tests/e2e/conftest.py` returns nothing.
43	
44	4. **nit: misleading docstring.** `tests/e2e/test_keyboard_mobile.py:9-10` says "Tab to the first queue item" while calling `.focus()`. Fix: reword to "focus the first item" or point to `test_polish_r3.py`.
45	
46	## What is right
47	
48	- The Tab/Enter/Space-only test is genuine keyboard reach with no `.focus()` and real end-state assertions.
49	- The negative key test kills four of five gate mutants, including the typing exemption and the dialog swallow.
50	- `test_stepper.py:204` now uses a retrying `expect`; the polish file has no fixed sleeps in UI waits.
51	
52	## Limits
53	
54	Outside my lens: UX wording of the shortcut sheet and notices. I did not run `tests/unit`; the card changes only `tests/e2e`.
55	
56	```json
57	{"card": "T-119", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
58	 "scope": "commit d9efc5c (tests/e2e/test_polish_r3.py, conftest.py) and the test_stepper.py:204 retry; pinned git archive of HEAD e1ce8dc (later HEAD c26ff04 changes only a two-line tests/e2e/conftest.py comment); own fixture servers 127.0.0.1:7991 and 7992 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB in scratch), both stopped by PID",
59	 "exercised": [
60	  "read personas/staff-engineer.md, board show T-119, reviews/T-119-staff-engineer.md, git show --stat d9efc5c, git diff --stat d9efc5c HEAD for app/frontend and tests/e2e",
61	  "git archive e1ce8dc into scratch T119_r2/archive (1979 files, equal to git ls-tree count)",
62	  "pytest tests/e2e/test_polish_r3.py: 18 passed",
63	  "pytest tests/e2e full, run 1: 1 failed (test_code_check_refusal.py:110 vis check), 190 passed, 1 skipped (test_ladder_gate.py:37); run 2: 191 passed, 1 skipped",
64	  "pytest tests/e2e/test_code_check_refusal.py alone x3: 23 passed each",
65	  "mutants A, B, C, D, E on a scratch copy with control green: polish file kills A, C, D, E; B survives 18/18",
66	  "mutant B across the 8 e2e files that press keys: 129 passed (survives)",
67	  "scratch probe r2-probe_p.py: passes on unmutated, fails on mutant B with 'p moved focus from the body: BODY: -> DIV:sbs-body'",
68	  "read review.js:309-345, sidebyside.js:98-106, batch.js:124-128, test_stepper.py:196-215, test_keyboard_mobile.py:1-20",
69	  "greps: sleep(, wait_for_timeout, keyboard.press(Tab), inner_text(), pytest.skip, conftest.py stale tray copy, xfail",
70	  "stopped scratch servers by PID (52563, 59175); ports 7991 and 7992 verified closed",
71	  "evidence copied to artifacts/review-evidence/T-119/ (r2-e2e-full-run1.txt, r2-e2e-full-run2.txt, r2-mutants-polish.txt, r2-probe_p.py, r2-mut.py)"
72	 ],
73	 "verdict": "changes",
74	 "scores": {"e2e_green_on_pinned_head": 4, "negative_key_rule_coverage": 3, "keyboard_reachability_coverage": 5, "flake_resistance": 4, "round1_minors_closed": 2},
75	 "findings": [
76	  {"severity": "major", "title": "The p gate is untested; the new negative key test does not fail on round-1 mutB",
77	   "evidence": "mutant B (app/frontend/sidebyside.js:102, '&& ZL.rv && ZL.rv.itemRowOf(t)' removed): test_polish_r3.py 18 passed, 8 keyboard files 129 passed (artifacts/review-evidence/T-119/r2-mutants-polish.txt); probe r2-probe_p.py fails with 'p moved focus from the body: BODY: -> DIV:sbs-body'; the test presses only j a d Shift+A ? (tests/e2e/test_polish_r3.py:79,85,93,100)",
78	   "why_it_matters": "p is a single-character shortcut that must act only from an item row (WCAG 2.1.4, T-060 blocker). It can regress with all 129 keyboard tests green. Round-1 finding 1 named p and its acceptance test required failing on both mutants.",
79	   "fix": "Add p to the key lists in test_letter_keys_do_nothing_from_body_export_or_an_input after putting an item in the pane (focus a row, press p, Escape, blur), and assert focus stays on the body or Export.",
80	   "acceptance_test": "The test passes on HEAD and fails on mutant B; artifacts/review-evidence/T-119/r2-probe_p.py is the reference."},
81	  {"severity": "minor", "title": "Full-suite flake: one-shot bounding-box read in test_code_check_refusal.py:110",
82	   "evidence": "run 1 of tests/e2e failed test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action 'the reason must be on screen beside the button, not below the fold' (r2-e2e-full-run1.txt); run 2 passed (r2-e2e-full-run2.txt); file alone 23 passed x3; vis() at test_code_check_refusal.py:93-95 reads bounding_box() once",
83	   "why_it_matters": "The card AC says full e2e green; a one-shot layout read after a click fails intermittently under a full run. Outside the T-119 diff.",
84	   "fix": "Retry the position check until the scroll settles (poll vis, or use a retrying expect on a stable position).",
85	   "acceptance_test": "5 consecutive full tests/e2e runs without this failure."},
86	  {"severity": "minor", "title": "Stale tray-flag copy still in the E2E data-testid contract (round-1 minor, unchanged)",
87	   "evidence": "tests/e2e/conftest.py:45 quotes 'AI suggested a flag that the second check did not confirm; it is not in the letter.'; the product (app/frontend/timeline.js:135) and test_suggestions.py use the T-060 sentence",
88	   "why_it_matters": "The conftest is the declared contract for the frontend hooks and contradicts the product and the test.",
89	   "fix": "Update conftest.py:45 to the T-060 sentence.",
90	   "acceptance_test": "grep -n 'did not confirm; it is not in the letter' tests/e2e/conftest.py returns nothing."},
91	  {"severity": "nit", "title": "Misleading docstring in test_keyboard_mobile.py",
92	   "evidence": "tests/e2e/test_keyboard_mobile.py:9 'Tab to the first queue item' with :10 calling .focus()",
93	   "why_it_matters": "The docstring claims keyboard reach the test does not exercise; the real Tab test now lives in test_polish_r3.py.",
94	   "fix": "Reword to 'focus the first item' or point to test_polish_r3.py.",
95	   "acceptance_test": "The docstring no longer says Tab."}
96	 ],
97	 "whats_right": [
98	  "The Tab/Enter/Space-only test has no .focus() on its path and asserts real end states (dismissed row, export visible, copy confirmed).",
99	  "The negative key test kills four of five gate mutants (body fallback, Shift+A, typing exemption, dialog swallow).",
100	  "test_stepper.py:204 is a retrying expect, and test_polish_r3.py has no fixed sleeps in UI waits (one bounded status poll)."
101	 ],
102	 "questions_for_chris": []}
103	```
104	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:21.193Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-119",
 "description": "Show board card T-119"
}
````

### User / tool · 2026-11-02T11:22:21.383Z

**tool result**
````
---
id: "T-119"
title: "E2E updates for T-060: keyboard keys act only from an item row (tests pressed from body), tray-flag wording, case rail and judge panel tests"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:03:50Z"
updated_at: "2026-11-02T11:22:15Z"
claimed_by: "qa"
claimed_at: "2026-11-02T11:14:53Z"
rounds: 2
commits: ["6e880e6", "c559ce2"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-119-staff-engineer.md", "at": "2026-11-02T10:27:09Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-119-staff-engineer-r2.md", "at": "2026-11-02T11:14:46Z"}
ac:
  - {"n": 1, "text": "tests/e2e updated so keyboard tests focus an item row first; tray-flag wording tests match T-096/T-060 copy; test_case_rail_is_one_line and test_judge_panel_when_nothing_objected diagnosed (drift fixed, or product bug -> card + strict xfail); full e2e green on a clean HEAD", "done": true, "evidence": "r3: tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row fails on reviewer mutB (sidebyside.js:102 row gate removed: 'BODY: -> DIV:sbs-body', artifacts/t119-r3-mutB.txt) and passes on HEAD; full tests/e2e on git archive HEAD copy (port 7993): 192 passed, 1 skipped (artifacts/t119-r3-e2e-full.txt); vis() now polls per animation frame, no sleeps"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:04:06Z qa: claimed
- 2026-11-02T10:10:35Z qa: AC 1 checked: Fixes are in 6e880e6 (landed concurrently by another qa agent; same edits): test_p_moves focuses a row first, tray-flag LEAD matches T-060 copy + tray-why in closed details, judge-count assert retrying (drift: counts load after the panel). test_case_rail_is_one_line passes on a clean HEAD (b89b9d9 worktree, port 7947, killed by PID). Full tests/e2e on clean HEAD: 156 pass, 16 skip, 1 xfail (T-117), the 1 failure was the pre-fix judge assert, then test_stepper+side_by_side+suggestions rerun with 6e880e6: 50 pass, 1 xfail. No product bug, no new card.
- 2026-11-02T10:10:35Z qa: moved in_progress -> in_review
- 2026-11-02T10:10:41Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T10:27:09Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-119-staff-engineer.md; round 1; findings:
    - [major] No e2e test proves letter keys are inert outside an item row (WCAG 2.1.4 rule untested) — fix: Make the probe's body-key test permanent (e.g. in tests/e2e/test_keyboard_mobile.py): from body, Export, header and an open dialog, a d j k p o e r do nothing and focus stays put.
    - [major] No e2e reaches a row by Tab; spec R-RV-4 keyboard-only E2E is not implemented — fix: Add a Tab-only E2E from page load to the first item row (no .focus()), press a, and assert the accept. Correct the test_keyboard_mobile.py:9 docstring if it stays on focus().
    - [minor] Stale tray-flag copy in the E2E data-testid contract — fix: Update conftest.py:45 to the T-060 sentence.
    - [minor] One-shot inner_text() read after a parent wait remains (T-115 pattern, :204 not fixed) — fix: Replace with expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\d+ checked, \d+ agreed with the draft, 3 questioned')).
    - [minor] The only e2e skip hides the ADR-005 rejected-item 409 path — fix: Seed one rejected item in the curated fixture, or convert to a strict xfail that names a card.
- 2026-11-02T10:27:09Z qa: claimed
- 2026-11-02T10:27:09Z orchestrator: The 2 coverage majors (negative row-only key test; Tab-only R-RV-4 E2E) are being added by the T-060 round-3 worker; re-check T-119 after it lands.
- 2026-11-02T10:27:09Z orchestrator: assigned: qa
- 2026-11-02T10:55:22Z orchestrator: moved in_progress -> in_review
- 2026-11-02T10:55:22Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T11:14:46Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-119-staff-engineer-r2.md; round 2; findings:
    - [major] The p gate is untested; the new negative key test does not fail on round-1 mutB — fix: Add p to the key lists in test_letter_keys_do_nothing_from_body_export_or_an_input after putting an item in the pane (focus a row, press p, Escape, blur), and assert focus stays on the body or Export.
    - [minor] Full-suite flake: one-shot bounding-box read in test_code_check_refusal.py:110 — fix: Retry the position check until the scroll settles (poll vis, or use a retrying expect on a stable position).
    - [minor] Stale tray-flag copy still in the E2E data-testid contract (round-1 minor, unchanged) — fix: Update conftest.py:45 to the T-060 sentence.
- 2026-11-02T11:14:46Z orchestrator: Round 3: add a test that 'p' (side-by-side, sidebyside.js:102) does nothing from body (kills mutB); stabilize test_code_check_refusal.py:110 position check (wait on condition, no sleeps).
- 2026-11-02T11:14:46Z orchestrator: assigned: qa
- 2026-11-02T11:14:53Z qa: claimed
- 2026-11-02T11:17:36Z qa: r3: added test_p_focuses_the_record_pane_only_from_an_item_row (kills reviewer mutB: fails 'BODY: -> DIV:sbs-body'); vis() in test_code_check_refusal polls per animation frame; conftest tray copy + keyboard_mobile docstring fixed. Full e2e running on git archive HEAD copy, port 7993.
- 2026-11-02T11:22:10Z qa: AC 1 checked: r3: tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row fails on reviewer mutB (sidebyside.js:102 row gate removed: 'BODY: -> DIV:sbs-body', artifacts/t119-r3-mutB.txt) and passes on HEAD; full tests/e2e on git archive HEAD copy (port 7993): 192 passed, 1 skipped (artifacts/t119-r3-e2e-full.txt); vis() now polls per animation frame, no sleeps
- 2026-11-02T11:22:10Z qa: moved in_progress -> in_review
- 2026-11-02T11:22:15Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
r3 changes: (1) new e2e test p from body/Export/header/sort does nothing, from an item row focuses sbs-body; applied mutB on a scratch copy (port 7994): that test fails, other 18 pass. (2) test_code_check_refusal vis() polls bounding box per animation frame, no sleeps. (3) conftest tray copy now the T-060 sentence, test_keyboard_mobile docstring reworded. Verified: full e2e on git archive HEAD copy, 192 passed 1 skipped, one run (flake needs more runs to disprove). Surprised: conftest.py carried another worker's uncommitted round-4 hook docs; they went in with my commit (comment-only). Skip in test_ladder_gate.py:37 untouched (pre-existing).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:21.657Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git cat-file -t c559ce2 && git show --stat c559ce2 | head -40",
 "description": "Verify commit c559ce2 and its file list"
}
````

### User / tool · 2026-11-02T11:22:21.815Z

**tool result**
````
c559ce2 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
6d01774 feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
c26ff04 feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
commit
commit c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:22:03 2026 -0600

    test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 artifacts/t119-r3-e2e-full.txt       |  4 ++++
 artifacts/t119-r3-mutB.txt           |  8 ++++++++
 tests/e2e/test_code_check_refusal.py | 13 ++++++++++---
 tests/e2e/test_keyboard_mobile.py    |  2 +-
 tests/e2e/test_polish_r3.py          | 20 ++++++++++++++++++++
 5 files changed, 43 insertions(+), 4 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:27.223Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/project_t119_keyboard_coverage_patterns.md; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/feedback_exact_count_vs_presence.md",
 "description": "Read recurring review memory for T-119 and feedback"
}
````

### User / tool · 2026-11-02T11:22:27.346Z

**tool result**
````
---
name: t119-keyboard-coverage-patterns
description: T-119 r1 (6e880e6, changes): focus() replaces the keyboard route, no negative test for the WCAG 2.1.4 row-only gate (two mutants survive 87 passing tests), no Tab-only E2E against R-RV-4, stale conftest tray copy, one-shot inner_text left at :204
metadata:
  type: project
---

Recurring patterns from the T-119 review (reviews/T-119-staff-engineer.md, 2026-11-02, pinned to 288affc, card commit 6e880e6).

- **A green keyboard suite can hide a dropped negative rule.** T-060 made letter keys act only from an item row (review.js:307-311, sidebyside.js:102). The T-119 rewrite made each test start with a programmatic `.focus()`, and no test asserts that a/d/j/p from the body do nothing. Mutants that let keys act from the body survived 87 passing tests in six keyboard files. **How to apply:** when a card narrows a key or focus rule, ask for a negative test (focus on body, Export, header, dialog) and run a mutant of the gate before accepting "tests pass".
- **Programmatic focus is not keyboard reach.** The old test_p_moves reached the row with a `j` keypress; the new one uses `.focus()`. No e2e in tests/e2e presses Tab to reach a row, so R-RV-4 ("E2E completes the sample case by keyboard only", spec/REQUIREMENTS.md:95) is unproven. test_keyboard_mobile.py:9 says "Tab" but calls `.focus()`. **How to apply:** grep `keyboard.press("Tab")` before accepting any keyboard-only claim, and read the docstring against the code.
- **Contract docstring drift.** conftest.py:45 kept the old tray-flag sentence while :51 and the product use the new one; test_e2e_contract.py is a needle check and passed. **How to apply:** grep the copy string in conftest.py and in the frontend together.
- **Same race, one fix.** T-115 flagged the one-shot inner_text at test_stepper.py:204 and :257; T-119 fixed only :257. Five repeat runs did not reproduce it, so it is minor. **How to apply:** after any race fix, grep the sibling reads in the same file.
- **Skip reconciliation.** Card counts 156 pass / 16 skip / 1 xfail plus one pre-fix failure = 174 collected. Full run with ZLAYT_DB exported: 172 / 1 skip (test_ladder_gate.py:37, runtime pytest.skip) / 1 xfail. The 15 extra skips are ZLAYT_DB gates (test_code_check_refusal.py:26,183 and test_change_the_quote.py). **How to apply:** reconcile the total with collected count before quoting skips.

Environment notes (this card): the board-guard denies `chmod`, and git-guard fails closed on escaped backticks inside `python -c`; put checkers in a heredoc file under scratch and run with `python -I`. Killing the `nohup` wrapper PID leaves the uvicorn listener alive; find the listener with `lsof -iTCP:<port> -sTCP:LISTEN` and kill that PID, then check the port. Mutants were scratch copies of the archive, each on its own port and sqlite file.

See also [[project_e2e_contract_review_patterns]], [[project_t115_e2e_curated_patterns]], [[project_t065_batch_fallback_review_patterns]].
----
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
----
---
name: feedback_exact_count_vs_presence
description: A presence oracle (each token appears somewhere) cannot see a dropped or doubled occurrence; run the test module's own random generator with exact per-record counts before passing a "nothing silently missing" claim
metadata:
  type: feedback
---

When a card claims "every money token is placed", check multiplicity, not presence. A presence oracle passes when a second printed copy of the same figure is dropped, because the first copy still satisfies it. T-103 r3: the test oracle (`unaccounted`) was presence-only, the exact count ran only over a fixed PROBES dict, and 31 of 600 generated draws differed per record (10 dropped occurrences, 2 doubled, 18 bare counts listed as figures).

**Why:** the handoff said "per-record count in==out for every probe" and the suite was green, but a fixed probe set cannot find an equal-text collision in a shape nobody wrote down. The fix was claimed for one collision (210.00) and a different collision class (130.00 twice in one excerpt) was still lost.

T-103 r4 confirmed the method: 41 seeds x 600 draws with exact counts, 0 failures, and the same harness on the r3 commit gives the r3 count (31/600). Always run the harness on the previous commit first as a positive control; a harness that prints 0 may simply not see the failure.

**How to apply:**
1. Import the test module's generator (`tests/unit/test_billing.py` `_BASES`, `_TOKENS`, `_insert`) and run the same draws with exact per-record Counters, outside pytest, with `-I` against a git-archive copy. Count mismatches by class (drop, double, bare over-list).
2. Any suppression keyed by text (count of (record, excerpt, text)) is suspect: two equal figures in one excerpt cannot be told apart.
3. Mutate a suppression to "always suppress" and a drop-only mutant to confirm the exact count goes red, not just the presence oracle.

Related: [[t103-listing-review-patterns]], [[project_t083_billing_review_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:28.091Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git merge-base --is-ancestor c559ce2 HEAD && echo ANCESTOR_OK; git log --oneline c559ce2..HEAD | head; echo ---; git show c559ce2 -- tests/e2e/test_polish_r3.py tests/e2e/test_code_check_refusal.py tests/e2e/test_keyboard_mobile.py | head -150",
 "description": "Check HEAD, ancestry of c559ce2, and the commit diff"
}
````

### User / tool · 2026-11-02T11:22:28.253Z

**tool result**
````
c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7
ANCESTOR_OK
---
commit c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:22:03 2026 -0600

    test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/test_code_check_refusal.py b/tests/e2e/test_code_check_refusal.py
index 2ba40a1..209f4fe 100644
--- a/tests/e2e/test_code_check_refusal.py
+++ b/tests/e2e/test_code_check_refusal.py
@@ -90,9 +90,16 @@ def row_of(page, i):
     return page.get_by_test_id("timeline").locator(f'[data-item-id="{i}"]').first
 
 
-def vis(page, loc):
-    b = loc.bounding_box(); vh = page.viewport_size["height"]
-    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh
+def vis(page, loc, frames=120):
+    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
+    so a single bounding_box() read can land mid-scroll."""
+    vh = page.viewport_size["height"]
+    for _ in range(frames):
+        bb = loc.bounding_box()
+        if bb is not None and bb["y"] >= 0 and bb["y"] + bb["height"] <= vh:
+            return True
+        page.evaluate("() => new Promise(r => requestAnimationFrame(() => r(true)))")
+    return False
 
 
 @pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
diff --git a/tests/e2e/test_keyboard_mobile.py b/tests/e2e/test_keyboard_mobile.py
index d6fa8e0..98f4e06 100644
--- a/tests/e2e/test_keyboard_mobile.py
+++ b/tests/e2e/test_keyboard_mobile.py
@@ -6,7 +6,7 @@ from tests.e2e.conftest import api, open_case, golden_text, BASE
 
 
 def test_keyboard_only_accept_flow(page, sample_case):
-    """R-RV-8: Tab to the first queue item, Enter opens, 'a' accepts, 'd' dismisses (documented shortcuts)."""
+    """R-RV-8: with the first queue item focused (the Tab-only path is test_polish_r3.py), 'a' accepts, 'd' dismisses (documented shortcuts)."""
     open_case(page, sample_case); page.get_by_test_id("queue").locator("[data-item-id]").first.focus(); page.keyboard.press("a")
     expect(page.locator("[data-review=accepted]")).to_have_count(1)
 
diff --git a/tests/e2e/test_polish_r3.py b/tests/e2e/test_polish_r3.py
index 4ce3a24..5fc400a 100644
--- a/tests/e2e/test_polish_r3.py
+++ b/tests/e2e/test_polish_r3.py
@@ -102,6 +102,26 @@ def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
     assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0
 
 
+def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
+    """WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing."""
+    open_case(page, sample_case)
+    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()
+    page.keyboard.press("p")
+    expect(page.get_by_test_id("sbs-body")).to_be_focused()           # from an item row it works, and the pane now shows an item
+    page.keyboard.press("Escape")
+    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')"), "Escape should return focus to the item row"
+    focus = lambda: page.evaluate("(() => { const a = document.activeElement; return (a.tagName || '') + ':' + (a.getAttribute('data-testid') || a.id || ''); })()")
+    page.evaluate("document.activeElement.blur()")
+    before = focus()
+    page.keyboard.press("p")
+    assert focus() == before, f"p moved focus from the page body: {before} -> {focus()}"
+    for tid in ("btn-export", "btn-shortcuts", "sort"):
+        page.get_by_test_id(tid).focus(); here = focus()
+        page.keyboard.press("p")
+        assert focus() == here, f"p moved focus from {tid}: {here} -> {focus()}"
+    assert not page.get_by_test_id("sbs-body").evaluate("e => e === document.activeElement")
+
+
 def test_letter_key_with_a_window_open_says_so(page, sample_case):
     """paralegal F11: o then a used to do nothing, silently."""
     open_case(page, sample_case)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:35.521Z

**tool call — Bash**
````
{
 "command": "SCRATCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la \"$SCRATCH\" 2>&1 | head -30; echo ---; grep -n \"BASE\\|ZLAYT_DB\\|environ\\|8000\\|78\" tests/e2e/conftest.py | head -40; echo ---; ls .venv/bin/python && .venv/bin/python -c \"import playwright, pytest; print('ok')\"",
 "description": "Inspect scratchpad, e2e conftest base URL, venv"
}
````

### User / tool · 2026-11-02T11:22:35.872Z

**tool result**
````
total 256904
drwx------@ 1042 arsis  wheel    33344 Nov  2 05:22 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M3
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M4
-rw-r--r--@    1 arsis  wheel     2046 Nov  1 19:21 T-047-run1.json
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 04:04 T-060-pass2-head
drwxr-xr-x@   23 arsis  wheel      736 Nov  2 00:41 T-093-r3-2ab7896
-rw-r--r--@    1 arsis  wheel    74715 Nov  2 00:41 T-093-r3-run.py.orig
drwxr-xr-x@    3 arsis  wheel       96 Nov  2 00:41 T-093-r3-scripts
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:13 T-093-r4-3223e50
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:15 T-093-r4-mutA
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:15 T-093-r4-mutB
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 00:42 T-109-probe
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:36 T-109-r1-card
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:36 T-109-r1-head
-rw-r--r--@    1 arsis  wheel     2531 Nov  2 00:40 T-109-unit-head.txt
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-head
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-mut2
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-parent
drwxr-xr-x@   10 arsis  wheel      320 Nov  2 03:17 T102_staff_r1
drwxr-xr-x@   15 arsis  wheel      480 Nov  2 03:26 T102_staff_r2
drwxr-xr-x@   21 arsis  wheel      672 Nov  1 23:51 T103_archive
drwxr-xr-x@   21 arsis  wheel      672 Nov  1 23:53 T103_parent
---
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
67:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
72:        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
80:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
86:    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
100:    return BASE
134:    page.goto(f"{BASE}/#/case/{tok}")
---
.venv/bin/python
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:40.211Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir \"$S/T119_r3\" && mkdir \"$S/T119_r3/head\" && git archive HEAD | tar -x -C \"$S/T119_r3/head\" && cd \"$S/T119_r3/head\" && find . -type f | wc -l && cd /Users/arsis/zlayt-pm-project && git ls-tree -r HEAD | wc -l; echo ---; grep -n \"uvicorn\\|app.backend\\|8000\\|7860\" Makefile run.sh 2>/dev/null | head; grep -rn \"uvicorn\" docs/RUNBOOK.md | head -5; echo ---; sed -n 95,106p app/frontend/sidebyside.js; echo ---; sed -n 1,30p tests/e2e/test_polish_r3.py | head -40",
 "description": "Create git archive of HEAD in scratch and inspect run and gate lines"
}
````

### User / tool · 2026-11-02T11:22:40.915Z

**tool result**
````
    2038
    2038
---
---
    const t = ev.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    if (ev.key === "Enter" && t && t.hasAttribute && t.hasAttribute("data-item-id") && !t.closest("dialog") && !t.closest(".sbs-pane")) {
      show(t.getAttribute("data-item-id"));   // Enter on a focused row (re)selects it into the pane; buttons inside the row keep their own Enter
    } else if (ev.key === "Escape" && t && t.closest && t.closest(".sbs-pane") && current) {
      const row = document.querySelector('[data-testid="queue"] [data-item-id="' + current.id + '"]') || document.querySelector('[data-item-id="' + current.id + '"]');
      if (row) { ev.preventDefault(); if (!row.hasAttribute("tabindex")) row.setAttribute("tabindex", "0"); row.focus(); }
    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
      if (document.querySelector("dialog[open]")) return;
      ev.preventDefault(); body.focus();
    }
  });
---
"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:45.694Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat artifacts/t119-r3-mutB.txt; echo ---; cat artifacts/t119-r3-e2e-full.txt; echo ---; ls Makefile run.sh 2>&1; grep -n \"run:\" -A3 Makefile 2>/dev/null | head; grep -rln \"uvicorn\" --include=*.py --include=*.sh --include=*.md . 2>/dev/null | grep -v node_modules | grep -v \"^./.venv\" | head -10; echo ---; grep -n \"7991\\|uvicorn\\|nohup\" docs/RUNBOOK.md | head",
 "description": "Read qa mutB artifact and find server launch command"
}
````

### User / tool · 2026-11-02T11:22:47.096Z

**tool result**
````
E         
E         - BODY:
E         + DIV:sbs-body

tests/e2e/test_polish_r3.py:117: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row
1 failed, 18 passed in 24.92s
---
........................................................................ [ 37%]
......s................................................................. [ 74%]
.................................................                        [100%]
192 passed, 1 skipped in 255.42s (0:04:15)
---
ls: Makefile: No such file or directory
ls: run.sh: No such file or directory
artifacts/review-evidence/T-053-r2-probe.py
artifacts/review-evidence/T-040-r2-boom_final.py
artifacts/review-evidence/T-053-r3-probe.py
artifacts/review-evidence/T-054-security-probe4.py
artifacts/review-evidence/T-055-security-r2/head_670ed09/app/backend/api.py
artifacts/review-evidence/T-055-security-r2/head_670ed09/app/README-arch.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/app/main.py
artifacts/review-evidence/T-055-security-r2/head_670ed09/memory/DECISIONS.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/memory/ENVIRONMENT.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_api_routes.py
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:50.259Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls \"$S/T119_r3/head\"; ls \"$S/T119_r3/head/app\" | head -30; grep -n \"ZLAYT_DB\\|environ\" \"$S/T119_r3/head/app/main.py\" \"$S/T119_r3/head/app/config.py\" 2>/dev/null | head -20; .venv/bin/python -c \"import uvicorn; print(uvicorn.__version__)\"; grep -n \"ZLAYT_DB\\|FIXTURE_SET\\|ZLAYT_MODE\" tests/e2e/conftest.py | head",
 "description": "Inspect archive layout, config env vars, and uvicorn presence"
}
````

### User / tool · 2026-11-02T11:22:50.511Z

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
README-arch.md
__init__.py
backend
db
frontend
llm
main.py
pipeline.py
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
0.54.0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:53.050Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat \"$S/T119_r3/head/app/main.py\"; echo ---; grep -rn \"ZLAYT_DB\\|ZLAYT_MODE\" \"$S/T119_r3/head/app\" | head -8; echo ---; grep -n \"ZLAYT_DB\" tests/e2e/*.py | head -5; echo; sed -n 1,20p \"$S/T119_r3/head/tests/e2e/conftest.py\" | head -5; grep -n \"def sample_case\" -A6 \"$S/T119_r3/head/tests/e2e/conftest.py\"",
 "description": "Read app entrypoint and DB env var usage"
}
````

### User / tool · 2026-11-02T11:22:53.201Z

**tool result**
````
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/frontend/mock_extra.js:1:/* Mock-only overlay (T-055 / T-058): export_config and audit for ?api=mock. ?local=1 adds prompt/response text to the audit like ZLAYT_MODE=local. */
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/trace.py:7:Visibility is the /audit split (D-020/D-036): full=False (public/demo) returns metadata only; full=True (ZLAYT_MODE=local) adds the model's raw
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/dismissal_patterns.py:5:ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/api.py:94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/api.py:550:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/backend/api.py:584:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
---
tests/e2e/test_change_the_quote.py:1:"""T-108: "Change the quote" completes end to end on the sample, against the REAL backend (needs ZLAYT_DB, the SQLite file of the server under test, to put
tests/e2e/test_code_check_refusal.py:2:with an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server
tests/e2e/test_code_check_refusal.py:24:    path = os.environ.get("ZLAYT_DB")
tests/e2e/test_code_check_refusal.py:26:        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
tests/e2e/test_code_check_refusal.py:181:# inline under the edit box (typed text kept); the Why dialog follows the backend verdict string as sent. Real backend (ZLAYT_DB) and a route stub per case.

"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
103:def sample_case():
104-    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
105-    import time
106-    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
107-    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
108-    for _ in range(300):
109-        s = api("GET", f"/api/cases/{tok}/status")[1]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:00.307Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/T119_r3/head\"; grep -rn \"FIXTURE_SET\" \"$A/app\" | head -3; echo ---; sed -n 40,50p \"$A/tests/e2e/conftest.py\"; echo ---; mkdir -p \"$S/T119_r3/db\" && cd \"$A\" && (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=\"$S/T119_r3/db/head.sqlite\" HOST=127.0.0.1 PORT=7995 nohup \"/Users/arsis/zlayt-pm-project/.venv/bin/python\" -m app.main > \"$S/T119_r3/db/head-server.log\" 2>&1 & echo $! > \"$S/T119_r3/db/head.pid\"); cat \"$S/T119_r3/db/head.pid\"; curl -s --retry 20 --retry-delay 1 --retry-connrefused http://127.0.0.1:7995/api/health; echo; lsof -iTCP:7995 -sTCP:LISTEN -n -P | tail -2",
 "description": "Start HEAD fixture server on port 7995 and confirm health"
}
````

### User / tool · 2026-11-02T11:23:01.525Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
---
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
---
5290
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
COMMAND  PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  5290 arsis    9u  IPv4 0xebeecf9f3a19a184      0t0  TCP 127.0.0.1:7995 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:07.608Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/T119_r3/head\"; cd \"$A\" && E2E_BASE_URL=http://127.0.0.1:7995 ZLAYT_DB=\"$S/T119_r3/db/head.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row -q 2>&1 | tail -15; echo \"=== grep ===\"; grep -n \"did not confirm; it is not in the letter\" tests/e2e/conftest.py; echo \"exit-grep=$?\"; grep -n \"not in the letter\\|left out of the letter\" tests/e2e/conftest.py app/frontend/timeline.js | head; echo \"=== docstring ===\"; sed -n 9,10p tests/e2e/test_keyboard_mobile.py",
 "description": "Run new p-key test on HEAD archive and check stale copy and docstring"
}
````

### User / tool · 2026-11-02T11:23:09.763Z

**tool result**
````
.                                                                        [100%]
1 passed in 1.77s
=== grep ===
exit-grep=1
tests/e2e/conftest.py:47:  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
tests/e2e/conftest.py:53:  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
app/frontend/timeline.js:191:  const FLAG_NOT_CONFIRMED = "The AI suggested this flag. The checks did not support it, so it is left out of the letter.";
=== docstring ===
    """R-RV-8: with the first queue item focused (the Tab-only path is test_polish_r3.py), 'a' accepts, 'd' dismisses (documented shortcuts)."""
    open_case(page, sample_case); page.get_by_test_id("queue").locator("[data-item-id]").first.focus(); page.keyboard.press("a")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:20.149Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/T119_r3/scripts\" && cat > \"$S/T119_r3/scripts/mutB.py\" <<'EOF'\nimport sys\npath = sys.argv[1]\nsrc = open(path, encoding=\"utf-8\").read()\nold = 'ev.key.toLowerCase() === \"p\" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {'\nnew = 'ev.key.toLowerCase() === \"p\" && !pane.hidden && body) {'\nassert src.count(old) == 1, src.count(old)\nopen(path, \"w\", encoding=\"utf-8\").write(src.replace(old, new))\nprint(\"mutB applied to\", path)\nEOF\ncp -R \"$S/T119_r3/head\" \"$S/T119_r3/mutB\" && \"/Users/arsis/zlayt-pm-project/.venv/bin/python\" -I \"$S/T119_r3/scripts/mutB.py\" \"$S/T119_r3/mutB/app/frontend/sidebyside.js\" && diff -u \"$S/T119_r3/head/app/frontend/sidebyside.js\" \"$S/T119_r3/mutB/app/frontend/sidebyside.js\"; echo \"diff-exit=$?\"; diff -rq \"$S/T119_r3/head\" \"$S/T119_r3/mutB\" ; echo \"--- cmp count\"; cd \"$S/T119_r3/head\" && git -C /Users/arsis/zlayt-pm-project show HEAD:app/frontend/sidebyside.js | diff - app/frontend/sidebyside.js && echo \"head sidebyside matches HEAD blob\"",
 "description": "Create mutB scratch copy and apply the row-gate removal at sidebyside.js:102"
}
````

### User / tool · 2026-11-02T11:23:21.767Z

**tool result**
````
mutB applied to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/mutB/app/frontend/sidebyside.js
--- /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/frontend/sidebyside.js	2026-11-02 05:22:03
+++ /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/mutB/app/frontend/sidebyside.js	2026-11-02 05:23:21
@@ -99,7 +99,7 @@
     } else if (ev.key === "Escape" && t && t.closest && t.closest(".sbs-pane") && current) {
       const row = document.querySelector('[data-testid="queue"] [data-item-id="' + current.id + '"]') || document.querySelector('[data-item-id="' + current.id + '"]');
       if (row) { ev.preventDefault(); if (!row.hasAttribute("tabindex")) row.setAttribute("tabindex", "0"); row.focus(); }
-    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
+    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
       if (document.querySelector("dialog[open]")) return;
       ev.preventDefault(); body.focus();
     }
diff-exit=1
Files /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/app/frontend/sidebyside.js and /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/mutB/app/frontend/sidebyside.js differ
--- cmp count
head sidebyside matches HEAD blob
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:26.337Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=\"$S/T119_r3/mutB\"; (cd \"$M\" && LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=\"$S/T119_r3/db/mutB.sqlite\" HOST=127.0.0.1 PORT=7996 nohup \"/Users/arsis/zlayt-pm-project/.venv/bin/python\" -m app.main > \"$S/T119_r3/db/mutB-server.log\" 2>&1 & echo $! > \"$S/T119_r3/db/mutB.pid\"); cat \"$S/T119_r3/db/mutB.pid\"; curl -s --retry 20 --retry-delay 1 --retry-connrefused http://127.0.0.1:7996/api/health | head -c 80; echo; cd \"$M\" && E2E_BASE_URL=http://127.0.0.1:7996 ZLAYT_DB=\"$S/T119_r3/db/mutB.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/test_polish_r3.py -q 2>&1 | tail -25",
 "description": "Start mutB server on port 7996 and run polish file against it"
}
````

### User / tool · 2026-11-02T11:23:52.117Z

**tool result**
````
6353
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only
sample_case = 'JS5oopbNNR6X2DaFOFgNgQ'

    def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
        """WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing."""
        open_case(page, sample_case)
        page.get_by_test_id("queue").locator("[data-item-id]").first.focus()
        page.keyboard.press("p")
        expect(page.get_by_test_id("sbs-body")).to_be_focused()           # from an item row it works, and the pane now shows an item
        page.keyboard.press("Escape")
        assert page.evaluate("!!document.activeElement.closest('[data-item-id]')"), "Escape should return focus to the item row"
        focus = lambda: page.evaluate("(() => { const a = document.activeElement; return (a.tagName || '') + ':' + (a.getAttribute('data-testid') || a.id || ''); })()")
        page.evaluate("document.activeElement.blur()")
        before = focus()
        page.keyboard.press("p")
>       assert focus() == before, f"p moved focus from the page body: {before} -> {focus()}"
E       AssertionError: p moved focus from the page body: BODY: -> DIV:sbs-body
E       assert 'DIV:sbs-body' == 'BODY:'
E         
E         - BODY:
E         + DIV:sbs-body

tests/e2e/test_polish_r3.py:117: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row
1 failed, 18 passed in 24.43s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:02.128Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/T119_r3/head\"; grep -n \"vis(\" \"$A/tests/e2e/test_code_check_refusal.py\"; echo ---; sed -n 86,125p \"$A/tests/e2e/test_code_check_refusal.py\"; echo ---; grep -rn \"timeout\\|sleep\" \"$A/tests/e2e/test_code_check_refusal.py\" | head; echo ---; ls \"$A\"/pytest.ini \"$A\"/pyproject.toml \"$A\"/setup.cfg \"$A\"/tox.ini 2>/dev/null; grep -n \"timeout\" \"$A\"/pytest.ini \"$A\"/pyproject.toml \"$A\"/setup.cfg 2>/dev/null | head -3",
 "description": "Inspect vis() call sites and timeout configuration"
}
````

### User / tool · 2026-11-02T11:24:02.314Z

**tool result**
````
93:def vis(page, loc, frames=120):
117:        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
254:    assert vis(page, ed.get_by_test_id("btn-save-excerpt")) or vis(page, ed.get_by_test_id("excerpt-unit").first), "the picker is on screen"
---
    return t


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
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T119_r3/head/tests/e2e/test_code_check_refusal.py:94:    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:16.169Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/T119_r3/head\"; cd \"$A\" && for i in 1 2 3 4 5; do E2E_BASE_URL=http://127.0.0.1:7995 ZLAYT_DB=\"$S/T119_r3/db/head.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/test_code_check_refusal.py -q > \"$S/T119_r3/refusal-run$i.txt\" 2>&1; echo \"run $i exit=$? $(tail -1 \"$S/T119_r3/refusal-run$i.txt\")\"; done",
 "description": "Run test_code_check_refusal.py five times against HEAD archive server",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:27:11.581Z

**tool result**
````
run 1 exit=0 23 passed in 36.07s
run 2 exit=0 23 passed in 34.75s
run 3 exit=0 23 passed in 34.19s
run 4 exit=0 23 passed in 35.19s
run 5 exit=0 23 passed in 34.04s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:27:16.246Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T119_r3/head\" && E2E_BASE_URL=http://127.0.0.1:7995 ZLAYT_DB=\"$S/T119_r3/db/head.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/test_polish_r3.py -q 2>&1 | tail -3; echo \"=== mutB full polish with row gate test name listing ===\"; cd \"$S/T119_r3/mutB\" && E2E_BASE_URL=http://127.0.0.1:7996 ZLAYT_DB=\"$S/T119_r3/db/mutB.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/test_polish_r3.py -q -rf 2>&1 | tail -3",
 "description": "Run polish file on HEAD and mutB for the summary counts",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:28:04.702Z

**tool result**
````
...................                                                      [100%]
19 passed in 23.91s
=== mutB full polish with row gate test name listing ===
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row
1 failed, 18 passed in 24.09s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:28:10.062Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T119_r3/head\" && E2E_BASE_URL=http://127.0.0.1:7995 ZLAYT_DB=\"$S/T119_r3/db/head.sqlite\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e -q -rs > \"$S/T119_r3/full-head-run1.txt\" 2>&1; echo \"exit=$?\"; tail -8 \"$S/T119_r3/full-head-run1.txt\"",
 "description": "Run full tests/e2e once against HEAD archive server",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:32:49.632Z

**tool result**
````
exit=0
........................................................................ [ 34%]
......s................................................................. [ 69%]
...............................................................          [100%]
=========================== short test summary info ============================
SKIPPED [1] tests/e2e/test_ladder_gate.py:37: no rejected item in the sample fixture run
206 passed, 1 skipped in 279.26s (0:04:39)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:32:58.614Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T119_r3/head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e --collect-only -q 2>/dev/null | tail -1; ZLAYT_DB= /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e --collect-only -q 2>/dev/null | tail -1; echo ---; grep -c \"\" /Users/arsis/zlayt-pm-project/artifacts/t119-r3-e2e-full.txt; cat /Users/arsis/zlayt-pm-project/artifacts/t119-r3-e2e-full.txt | head -3; echo ---; grep -n \"ZLAYT_DB\" /Users/arsis/zlayt-pm-project/memory/ENVIRONMENT.md 2>/dev/null | head -3",
 "description": "Collect e2e test counts with and without ZLAYT_DB to reconcile"
}
````

### User / tool · 2026-11-02T11:32:59.673Z

**tool result**
````
207 tests collected in 0.28s
207 tests collected in 0.27s
---
4
........................................................................ [ 37%]
......s................................................................. [ 74%]
.................................................                        [100%]
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:33:07.026Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ad %s' --date=iso -6 | cut -c1-120; echo ---; git log --format='%h %ad' --date=iso -3 -- tests/e2e | head -3; echo ---; for c in e293daa 6d01774 63e18ed c26ff04; do echo \"$c: $(git show --stat --format= $c -- tests/e2e | tail -1)\"; done; echo ---; git rev-list --count HEAD -- tests/e2e; git show e293daa:tests/e2e/ 2>/dev/null | head -0; echo \"e2e test defs at e293daa: $(git grep -h '^def test_' e293daa -- tests/e2e | wc -l)\"; echo \"e2e test defs at HEAD: $(git grep -h '^def test_' HEAD -- tests/e2e | wc -l)\"",
 "description": "Compare e2e test definition counts across recent commits"
}
````

### User / tool · 2026-11-02T11:33:07.080Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($c:) | command: git log --format='%h %ad %s' --date=iso -6 | cut -c1-120; echo ---; git log --format='%h %ad' --date=iso -3 -- tests/e2e | head -3; echo ---; for c in e293daa 6d01774 63e18ed c26ff04; do echo "$c: $(g
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:33:09.125Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ad %s' --date=iso -6 | cut -c1-120; echo ---; git log --format='%h %ad' --date=iso -3 -- tests/e2e | head -3; echo ---; git show --stat --format= e293daa -- tests/e2e | tail -1; git show --stat --format= 6d01774 -- tests/e2e | tail -1; git show --stat --format= 63e18ed -- tests/e2e | tail -1; git show --stat --format= c26ff04 -- tests/e2e | tail -1; echo ---; echo \"e2e defs at e293daa: $(git grep -h '^def test_' e293daa -- tests/e2e | wc -l)\"; echo \"e2e defs at HEAD: $(git grep -h '^def test_' HEAD -- tests/e2e | wc -l)\"",
 "description": "Compare recent commit history and e2e test definitions"
}
````

### User / tool · 2026-11-02T11:33:09.464Z

**tool result**
````
433ac1c 2026-11-02 05:27:41 -0600 test(backend): T-123 pin which record is named as paperwork in either order (kills the
aa6ae9f 2026-11-02 05:27:36 -0600 feat(backend): T-105 added-qualifier word lists (attribution, hedge, approximation, in
4c59fac 2026-11-02 05:27:25 -0600 fix(backend): T-121 r2 one-line style carries the translated summary, whitespace-only 
07dbd2b 2026-11-02 05:27:21 -0600 fix(backend): T-120 r2 history-source skip only when the sentence names no condition (
1a0106b 2026-11-02 05:25:06 -0600 docs(orchestrator): T-112 accepted-debt row (§7.4 after round 3)
c559ce2 2026-11-02 05:22:03 -0600 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray c
---
c559ce2 2026-11-02 05:22:03 -0600
e293daa 2026-11-02 05:21:50 -0600
d56328a 2026-11-02 05:06:22 -0600
---
 5 files changed, 247 insertions(+), 4 deletions(-)
---
e2e defs at e293daa:      184
e2e defs at HEAD:      185
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:33:18.537Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir \"$S/T119_r3/pin_c559\" && git archive c559ce2 | tar -x -C \"$S/T119_r3/pin_c559\" && diff -rq \"$S/T119_r3/pin_c559\" \"$S/T119_r3/head\" && echo \"PIN_MATCH_c559ce2\"; mkdir \"$S/T119_r3/pre_e293\" && git archive d56328a | tar -x -C \"$S/T119_r3/pre_e293\" && cd \"$S/T119_r3/pre_e293\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e --collect-only -q 2>/dev/null | tail -1",
 "description": "Verify c559ce2 archive matches pin and collect the pre-e293daa tree count",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:33:20.825Z

**tool result**
````
PIN_MATCH_c559ce2
192 tests collected in 0.28s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:33:33.037Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ad %s' --date=iso -S\"did not confirm; it is not in the letter\" -- tests/e2e/conftest.py | cut -c1-110; echo ---; git show c559ce2:tests/e2e/conftest.py | grep -c \"did not confirm; it is not in the letter\"; echo ---; git show c559ce2:tests/e2e/test_keyboard_mobile.py | sed -n 9p | cut -c1-80; echo ---; git show c559ce2:tests/e2e/test_ladder_gate.py | sed -n 35,38p; echo ---; git show c559ce2:tests/e2e/test_stepper.py | grep -n \"inner_text\" | head -5",
 "description": "Trace stale-copy fix commit and check remaining minors at the pinned commit"
}
````

### User / tool · 2026-11-02T11:33:33.479Z

**tool result**
````
e293daa 2026-11-02 05:21:50 -0600 feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed 
36ceb38 2026-11-02 03:27:49 -0600 feat(frontend): T-096 pre-selected date suggestion, dismissal banner, measur
---
0
---
    """R-RV-8: with the first queue item focused (the Tab-only path is test_poli
---
    c = api("GET", f"/api/cases/{sample_case}")[1]
    rej = [i for i in c["entries"] if i["state"] == "rejected"]
    if not rej: pytest.skip("no rejected item in the sample fixture run")
    assert api("POST", f"/api/cases/{sample_case}/items/{rej[0]['id']}/review", {"action": "accept"})[0] == 409
---
66:    kinds = {steps.nth(i).get_by_test_id("step-kind").inner_text() for i in range(steps.count())}
71:        assert s.get_by_test_id("step-why").inner_text().strip()
72:        assert s.get_by_test_id("step-status").inner_text().strip() in ("Passed", "Failed", "Skipped", "Not done yet", "Needs your decision", "Blocked")
73:        assert s.get_by_test_id("step-marker").inner_text().strip() in ("✓", "✕", "–", "○")   # glyph plus word, never colour alone
83:    assert "What you need to do" in human.get_by_test_id("step-action").inner_text()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:33:36.630Z

**tool call — Bash**
````
{
 "command": "git show c559ce2:tests/e2e/test_stepper.py | grep -n \"judge-summary-counts\" ; echo ---; git show c559ce2:tests/e2e/test_polish_r3.py | grep -n \"sleep(\\|wait_for_timeout\" ; git show c559ce2:tests/e2e/test_code_check_refusal.py | grep -n \"sleep(\\|wait_for_timeout\"; echo \"sleep-grep-exit=$?\"; echo ---; git show c559ce2:tests/e2e/test_polish_r3.py | grep -n \"keyboard.press(\\\"Tab\\\")\" | head -3; echo ---; git show c559ce2:tests/e2e/test_keyboard_mobile.py | grep -n \"xfail\\|skip\" | head",
 "description": "Check remaining sleep/inner_text/skip sites at the pinned commit"
}
````

### User / tool · 2026-11-02T11:33:36.800Z

**tool result**
````
204:    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"\d+ checked, \d+ agreed with the draft, 3 questioned"))   # counts load after the row (retrying assert, not a snapshot)
256:    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"checked \d+, all agreed"))   # counts load after the panel (retrying assert, not a snapshot)
---
21:        time.sleep(.5)
sleep-grep-exit=1
---
41:        page.keyboard.press("Tab")
249:    page.keyboard.press("Shift+Tab"); page.keyboard.press("Tab")
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:34:00.223Z

**tool call — Bash**
````
{
 "command": "git show c559ce2:tests/e2e/test_code_check_refusal.py | sed -n '93,102p;117p' | cat -n | head -20; echo ---; git show c559ce2:tests/e2e/test_polish_r3.py | grep -n \"def test_p_focuses\\|for tid in\\|sort\\\"\\|assert not page.get_by_test_id(\\\"sbs-body\\\")\\|an input\" ; echo ---; git show c559ce2:app/frontend/sidebyside.js | grep -n \"INPUT|TEXTAREA|SELECT\\|\\\"p\\\" && !pane.hidden\"; echo ---; git show c559ce2:tests/e2e/test_ladder_gate.py | grep -n \"pytest.skip\"; echo ---; git show c559ce2:tests/e2e/test_polish_r3.py | grep -n \"time.sleep\"",
 "description": "Pin exact line numbers for the findings at c559ce2"
}
````

### User / tool · 2026-11-02T11:34:00.424Z

**tool result**
````
     1	def vis(page, loc, frames=120):
     2	    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
     3	    so a single bounding_box() read can land mid-scroll."""
     4	    vh = page.viewport_size["height"]
     5	    for _ in range(frames):
     6	        bb = loc.bounding_box()
     7	        if bb is not None and bb["y"] >= 0 and bb["y"] + bb["height"] <= vh:
     8	            return True
     9	        page.evaluate("() => new Promise(r => requestAnimationFrame(() => r(true)))")
    10	    return False
    11	        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
---
68:# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
89:    # from an input: the edit box of an item, and the sort control
99:    page.get_by_test_id("sort").focus()
105:def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
106:    """WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing."""
118:    for tid in ("btn-export", "btn-shortcuts", "sort"):
122:    assert not page.get_by_test_id("sbs-body").evaluate("e => e === document.activeElement")
---
96:    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
102:    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
---
37:    if not rej: pytest.skip("no rejected item in the sample fixture run")
---
21:        time.sleep(.5)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:34:06.034Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for p in 5290 6353; do ps -o pid=,command= -p $p | cut -c1-120; done; kill 5290 6353; sleep 2; for port in 7995 7996; do echo \"port $port listeners: [$(lsof -iTCP:$port -sTCP:LISTEN -t 2>/dev/null)]\"; done; cat \"$S/T119_r3/db/head.pid\" \"$S/T119_r3/db/mutB.pid\"",
 "description": "Stop my own two fixture servers by PID and verify ports closed"
}
````

### User / tool · 2026-11-02T11:34:08.323Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:34:15.971Z

**tool call — Bash**
````
{
 "command": "ps -o pid=,ppid=,command= -p 6354 | cut -c1-200; echo ---; lsof -iTCP:7996 -sTCP:LISTEN -n -P | tail -1",
 "description": "Identify the surviving mutB server listener before stopping it"
}
````

### User / tool · 2026-11-02T11:34:16.130Z

**tool result**
````
 6354     1 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
---
Python  6354 arsis    9u  IPv4 0x33b43ec9523bcd6d      0t0  TCP 127.0.0.1:7996 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:34:17.767Z

**tool call — Bash**
````
{
 "command": "kill 6354; sleep 2; lsof -iTCP:7996 -sTCP:LISTEN -n -P | tail -1; echo \"7996 listeners after stop: [$(lsof -iTCP:7996 -sTCP:LISTEN -t 2>/dev/null)]\"; echo \"7995 listeners: [$(lsof -iTCP:7995 -sTCP:LISTEN -t 2>/dev/null)]\"; ps -o pid=,command= -p 6354 5290 | cut -c1-100",
 "description": "Stop the mutB server PID 6354 and confirm both ports closed"
}
````

### User / tool · 2026-11-02T11:34:20.165Z

**tool result**
````
7996 listeners after stop: []
7995 listeners: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:34:42.427Z

**tool call — Bash**
````
{
 "command": "git show c559ce2:tests/e2e/test_code_check_refusal.py | grep -n \"abs(box\\|assert vis(pg, box)\\|def vis\\|return True\\|return False\\|requestAnimationFrame\" ; echo ---; git show c559ce2:tests/e2e/test_polish_r3.py | grep -n \"def test_p_focuses\\|assert focus() == before\\|for tid\\|sort\\\").focus\\|sbs-body\\\").to_be_focused\\|time.sleep\" ; echo ---; git show c559ce2:app/frontend/sidebyside.js | grep -n \"let p\\|const t = ev.target\\|INPUT|TEXTAREA\\|toLowerCase() === \\\"p\\\"\" ; echo ---; git show c559ce2:tests/e2e/conftest.py | grep -n \"tray-flag-lead\\|left out of the letter\" | cut -c1-60; echo ---; git show c559ce2:tests/e2e/test_ladder_gate.py | grep -n \"pytest.skip\"; echo ---; git show c559ce2:tests/e2e/test_keyboard_mobile.py | grep -n \"R-RV-8\" | cut -c1-70; echo ---; git show c559ce2:tests/e2e/test_stepper.py | sed -n 204p | cut -c1-90; echo ---; git rev-parse --short c559ce2",
 "description": "Proof-read every cited line number against the pinned commit"
}
````

### User / tool · 2026-11-02T11:34:42.680Z

**tool result**
````
93:def vis(page, loc, frames=120):
100:            return True
101:        page.evaluate("() => new Promise(r => requestAnimationFrame(() => r(true)))")
102:    return False
117:        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
118:        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
---
21:        time.sleep(.5)
99:    page.get_by_test_id("sort").focus()
105:def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
117:    assert focus() == before, f"p moved focus from the page body: {before} -> {focus()}"
118:    for tid in ("btn-export", "btn-shortcuts", "sort"):
---
9:  let pane, body, titleEl, flagsBar, current = null, lastToken = null;   // current = {id}
85:    const t = ev.target; if (!t || !t.closest || t.closest("dialog") || t.closest(".sbs-pane")) return;
95:    const t = ev.target;
96:    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
102:    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
---
47:  tray-item (one per could-not-verify item, data-item-id)
53:  Wording: the row's 'Why?' button reads 'Why this status
---
37:    if not rej: pytest.skip("no rejected item in the sample fixture run")
---
1:"""Keyboard and mobile. R-RV-8, R-ST-1, a11y."""
9:    """R-RV-8: with the first queue item focused (the Tab-only path 
---
    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"\d+ checke
---
c559ce2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:14.550Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-119-staff-engineer-r3.md",
 "content": "# T-119 review, round 3: staff-engineer-reviewer\n\n**Verdict: pass.** No blocker, no major. The round-2 major is closed: `test_p_focuses_the_record_pane_only_from_an_item_row` fails on mutant B (`sidebyside.js:102` row gate removed) and passes on HEAD. The round-2 flake fix is partial: `vis()` now exits at the first frame the box is in the viewport, not at a settled position, and the card's five-run full-suite acceptance is not evidenced. Three minors and two nits remain (below). Pinned to `c559ce2`; HEAD has moved since (now `433ac1c`), and I did not review the later commits.\n\n## What I ran\n\nPin: `git rev-parse HEAD` returned `c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7` when I started; `git merge-base --is-ancestor c559ce2 HEAD` succeeded. Archive `git archive c559ce2` into scratch `T119_r3/head`: 2038 files, equal to `git ls-tree -r c559ce2 | wc -l` (2038). A second archive `T119_r3/pin_c559` is `diff -rq`-identical to it.\n\n- Mutant B (scratch copy `T119_r3/mutB`, script `T119_r3/scripts/mutB.py` run with `-I`): replaces `&& ZL.rv && ZL.rv.itemRowOf(t)` on `app/frontend/sidebyside.js:102` with nothing. `diff -u` shows that one-line change only.\n- New test on HEAD (port 7995): `1 passed in 1.77s`.\n- New test on mutB (port 7996): `FAILED test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row`, `AssertionError: p moved focus from the page body: BODY: -> DIV:sbs-body`, at `test_polish_r3.py:117`. Result for the file: `1 failed, 18 passed`.\n- `tests/e2e/test_polish_r3.py` on HEAD: `19 passed in 23.91s`.\n- `tests/e2e/test_code_check_refusal.py` run five times on HEAD: `23 passed in 36.07s`, `34.75s`, `34.19s`, `35.19s`, `34.04s` (exit 0 each; logs in `T119_r3/refusal-run{1..5}.txt`).\n- Full `tests/e2e` on HEAD, one run: `206 passed, 1 skipped in 279.26s`; the skip is `test_ladder_gate.py:37`. `--collect-only` gives 207.\n- Reconciling the card artifact: `artifacts/t119-r3-e2e-full.txt` reports `192 passed, 1 skipped` and records no commit. `git archive d56328a` collects 192, so the artifact probably came from an older tree. It does not reproduce on `c559ce2`.\n- Greps at `c559ce2`: `time.sleep` appears only at `test_polish_r3.py:21` (a capped `/status` poll, pre-existing); no `sleep(` or `wait_for_timeout` in `test_code_check_refusal.py`; `git show c559ce2:tests/e2e/conftest.py | grep -c \"did not confirm; it is not in the letter\"` returns 0. `git log -S` puts that removal in `e293daa`, not in `c559ce2` as the handoff says.\n- Read at `c559ce2`: `test_code_check_refusal.py:93-102` (vis) and `:117-118` (call site and the 140 px check); `test_polish_r3.py:105-122`; `sidebyside.js:96` (early return for INPUT, TEXTAREA, SELECT) and `:102`; `test_keyboard_mobile.py:9`; `test_stepper.py:204`; `test_ladder_gate.py:37`; `conftest.py:47,53`.\n- Ports: my fixture servers were PID 5290 (7995) and 6354 (7996). I first killed PID 6353, which is the PID I had recorded for the 7996 server. It turned out to be a bash wrapper, not the server, and I killed it in error. The listener, 6354, is the `Python -m app.main` process; I then stopped it. `lsof -iTCP:7995 -sTCP:LISTEN` and `lsof -iTCP:7996 -sTCP:LISTEN` both return nothing.\n\nEvidence is under the scratch directory `T119_r3/` (`refusal-run*.txt`, `full-head-run1.txt`, `scripts/mutB.py`). Copies are not in `artifacts/review-evidence/` because I did not change the repo.\n\n## Round-2 status\n\n- r2 major, p gate untested: **closed.** The new test kills mutB and passes on HEAD. The shape differs from the r2 suggestion (a separate test, not an added key in the list), which is fine because the acceptance is met.\n- r2 minor, vis flake: **partly closed.** Finding 1.\n- r2 minor, stale tray copy: **closed at HEAD** (`e293daa`). The handoff's attribution to `c559ce2` is wrong, which is a note, not a finding.\n- r2 nit, `test_keyboard_mobile.py:9` docstring: **closed.**\n- r1 minor 4, `inner_text` at `test_stepper.py:204`: **closed.** It is now a retrying `expect`.\n- r1 minor 5, the only skip hides the ADR-005 path: **open.** Finding 3.\n\n## Findings\n\n1. **minor: `vis()` stops at the first in-viewport frame, and the flake acceptance is not evidenced.** Evidence: `test_code_check_refusal.py:100` returns True on the first frame where the box is inside the viewport; `:101` polls rAF; `:102` returns False after 120 frames. The call at `:117` is the only positive assertion that uses it. The round-2 fix asked for a wait \"until the scroll settles\". This returns as soon as the box is in the viewport once, so the assertion means \"visible at some frame within about 2 s\", not \"on screen at rest\". The one-shot check at `:118` still reads boxes after the poll. A permanently off-screen box still fails after the loop exhausts, so regression coverage holds for that case. The round-2 flake was seen once in two full runs; this review has one full run (206 passed), so the five-run acceptance is not met. Why it matters: a box that enters and leaves the viewport now passes, and the card's \"full e2e green\" claim rests on one run. Fix: return True only after two consecutive frames with the same box inside the viewport. Acceptance: five consecutive full `tests/e2e` runs on the pinned tree are green, and a mutant that pushes the reason box below the fold still fails at `:117`.\n\n2. **minor: the card's full-run artifact cannot be tied to a commit and does not reproduce.** Evidence: `artifacts/t119-r3-e2e-full.txt` shows `192 passed, 1 skipped in 255.42s` and 193 progress marks, with no sha. On the archive of `c559ce2`, `pytest tests/e2e --collect-only -q` gives `207 tests collected`, and the full run gives `206 passed, 1 skipped in 279.26s`. The nearest tree I checked, `d56328a`, collects 192. Why it matters: the AC cites this file as proof, and a reviewer cannot reproduce its count. Fix: regenerate the file from a stated sha and include the collected count. Acceptance: the file names `c559ce2` and its numbers match a fresh `--collect-only` and run on that sha.\n\n3. **minor (carried from r1): the only e2e skip hides the ADR-005 rejected-item path.** Evidence: `tests/e2e/test_ladder_gate.py:37`, `if not rej: pytest.skip(\"no rejected item in the sample fixture run\")`; the full run prints `SKIPPED [1] tests/e2e/test_ladder_gate.py:37`. Why it matters: the 409 path never runs in the suite. Fix: seed one rejected item in the curated fixture, or convert to a strict xfail that names a card. Acceptance: the full run reports zero skips, or the xfail names a card.\n\n4. **nit: the p test's docstring says \"an input\", but its loop presses btn-export, btn-shortcuts and sort.** Evidence: `test_polish_r3.py:106` (docstring), `:118` (loop). `sort` is a SELECT, and `sidebyside.js:96` returns early for SELECT, so that step never reaches the p gate. Fix: reword to \"a select\" or add a text field. Acceptance: docstring matches the presses.\n\n5. **nit: `vis()` has no timeout on its rAF evaluate.** Evidence: `test_code_check_refusal.py:101`. The archive root has no `pytest.ini`, `pyproject.toml`, `setup.cfg` or `tox.ini`, so no timeout applies. If rAF never fires, the test hangs rather than fails. Fix: use `page.wait_for_function` with a timeout, or add an explicit deadline. Acceptance: a test with rAF stopped fails within the timeout.\n\n## What is right\n\n- The new p test names the focus move in its failure message, so a regression reads as `BODY: -> DIV:sbs-body`, and it passes on HEAD (19/19 in the polish file).\n- `vis()` has no wall-clock sleep and a fixed frame budget, and both call sites are positive assertions, so a box that never comes into view still fails.\n- The stale tray copy and the keyboard docstring are fixed at HEAD, and `test_code_check_refusal.py` passed 23/23 on each of five runs.\n\n## Limits\n\nOutside my lens: the wording of the shortcut sheet and the notices. I did not run `tests/unit`; the card changes only `tests/e2e`.\n\n```json\n{\"card\": \"T-119\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit c559ce2 (tests/e2e/test_polish_r3.py, tests/e2e/test_code_check_refusal.py, tests/e2e/test_keyboard_mobile.py, artifacts/t119-r3-e2e-full.txt, artifacts/t119-r3-mutB.txt); pinned git archive of c559ce2 (2038 files, identical to a second archive); fixture servers 127.0.0.1:7995 (HEAD archive) and 127.0.0.1:7996 (mutB archive), both stopped; HEAD has since moved to 433ac1c and was not reviewed\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-119-staff-engineer-r2.md, board show T-119, memory project_t119_keyboard_coverage_patterns.md\",\n  \"git rev-parse HEAD (c559ce2 at pin time), git merge-base --is-ancestor c559ce2 HEAD, git show --stat and git show c559ce2 for the five changed files\",\n  \"git archive c559ce2 into scratch T119_r3/head (2038 files = git ls-tree count); second archive T119_r3/pin_c559, diff -rq identical\",\n  \"mutB: scratch copy T119_r3/mutB, scripts/mutB.py (run with -I) removes ' && ZL.rv && ZL.rv.itemRowOf(t)' at app/frontend/sidebyside.js:102; diff -u shows the one-line change\",\n  \"pytest tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row on HEAD: 1 passed in 1.77s\",\n  \"same test on mutB: FAILED at test_polish_r3.py:117 'p moved focus from the page body: BODY: -> DIV:sbs-body'\",\n  \"pytest tests/e2e/test_polish_r3.py on HEAD: 19 passed in 23.91s; on mutB: 1 failed, 18 passed in 24.09s\",\n  \"pytest tests/e2e/test_code_check_refusal.py five times on HEAD: 23 passed each (36.07s, 34.75s, 34.19s, 35.19s, 34.04s); logs in T119_r3/refusal-run1..5.txt\",\n  \"pytest tests/e2e full on HEAD, one run: 206 passed, 1 skipped in 279.26s (skip at test_ladder_gate.py:37); --collect-only 207\",\n  \"pytest tests/e2e --collect-only on git archive d56328a: 192 collected (to reconcile artifacts/t119-r3-e2e-full.txt, which reports 192 passed, 1 skipped)\",\n  \"greps at c559ce2: time.sleep only at test_polish_r3.py:21; no sleep( or wait_for_timeout in test_code_check_refusal.py; git show c559ce2:tests/e2e/conftest.py | grep -c old tray sentence = 0; git log -S shows the removal in e293daa\",\n  \"read at c559ce2: test_code_check_refusal.py:93-102 and :117-118; test_polish_r3.py:105-122; sidebyside.js:96 and :102; test_keyboard_mobile.py:9; test_stepper.py:204; test_ladder_gate.py:37; conftest.py:47 and :53\",\n  \"stopped my own servers: PID 5290 (7995) and PID 6354 (7996 listener); PID 6353 (a recorded wrapper, not the server) was killed in error first; lsof shows ports 7995 and 7996 closed\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"e2e_green_on_pinned_head\": 4, \"negative_key_rule_coverage\": 5, \"keyboard_reachability_coverage\": 5, \"flake_resistance\": 4, \"round1_minors_closed\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"vis() stops at the first in-viewport frame; the flake fix and its five-run acceptance are not evidenced\",\n   \"evidence\": \"tests/e2e/test_code_check_refusal.py:100 (return True on first in-viewport frame), :101 (rAF poll), :102 (return False after 120 frames), :117 (positive call), :118 (one-shot 140 px read after the poll); r2 flake observed once in two full runs (r2-e2e-full-run1.txt); this review: one full run 206 passed\",\n   \"why_it_matters\": \"A box that enters and leaves the viewport now passes, so the assertion means visible at some frame, not on screen at rest. The card's full-e2e-green claim rests on one run here and the round-2 acceptance asked for five.\",\n   \"fix\": \"Return True only after two consecutive frames with the same box fully inside the viewport, then keep the 140 px check.\",\n   \"acceptance_test\": \"Five consecutive full tests/e2e runs on the pinned tree are green, and a mutant that pushes the accept-refused box below the fold still fails at test_code_check_refusal.py:117.\"},\n  {\"severity\": \"minor\", \"title\": \"artifacts/t119-r3-e2e-full.txt records no commit and does not reproduce on c559ce2\",\n   \"evidence\": \"artifacts/t119-r3-e2e-full.txt: '192 passed, 1 skipped in 255.42s' with 193 progress marks and no sha; on the c559ce2 archive, --collect-only gives 207 and the full run gives '206 passed, 1 skipped in 279.26s'; git archive d56328a collects 192\",\n   \"why_it_matters\": \"The AC cites this file as proof of full e2e green on a clean HEAD, and a reviewer cannot tie its count to a tree.\",\n   \"fix\": \"Regenerate the file from a stated sha with the collected count in it.\",\n   \"acceptance_test\": \"The artifact names c559ce2 (or its successor) and its numbers match a fresh --collect-only and full run on that sha.\"},\n  {\"severity\": \"minor\", \"title\": \"The only e2e skip hides the ADR-005 rejected-item 409 path (carried from r1)\",\n   \"evidence\": \"tests/e2e/test_ladder_gate.py:37: if not rej: pytest.skip('no rejected item in the sample fixture run'); full run prints SKIPPED [1] tests/e2e/test_ladder_gate.py:37\",\n   \"why_it_matters\": \"The 409 path for a rejected item never runs in the suite, so a regression there passes CI.\",\n   \"fix\": \"Seed one rejected item in the curated fixture, or convert to a strict xfail that names a card.\",\n   \"acceptance_test\": \"The full run reports zero skips, or the xfail names a card and fails loudly if the path starts to work.\"},\n  {\"severity\": \"nit\", \"title\": \"The p test docstring says 'an input' but the loop presses btn-export, btn-shortcuts and sort (a SELECT)\",\n   \"evidence\": \"tests/e2e/test_polish_r3.py:106 (docstring), :118 (for tid in ('btn-export', 'btn-shortcuts', 'sort')); app/frontend/sidebyside.js:96 returns early for SELECT, so the sort step never reaches the p gate\",\n   \"why_it_matters\": \"The docstring overstates what the test covers; the p gate itself is exercised by the body step and the Export and shortcuts steps.\",\n   \"fix\": \"Reword to 'a select', or add a text field to the loop.\",\n   \"acceptance_test\": \"The docstring matches the controls pressed.\"},\n  {\"severity\": \"nit\", \"title\": \"vis() waits on requestAnimationFrame with no timeout\",\n   \"evidence\": \"tests/e2e/test_code_check_refusal.py:101; no pytest.ini, pyproject.toml, setup.cfg or tox.ini at the archive root\",\n   \"why_it_matters\": \"If rAF never fires (for example a hidden page), the test hangs instead of failing.\",\n   \"fix\": \"Use page.wait_for_function with a timeout, or add an explicit deadline.\",\n   \"acceptance_test\": \"A test with rAF stopped fails within the timeout instead of hanging.\"}\n ],\n \"whats_right\": [\n  \"The new p test names the focus move in its failure message and passes on HEAD (19/19 in test_polish_r3.py); mutB fails it at test_polish_r3.py:117.\",\n  \"vis() has no wall-clock sleep and a fixed frame budget, and both call sites are positive assertions, so a box that never comes into view still fails.\",\n  \"The stale tray copy and the keyboard docstring are fixed at HEAD, and test_code_check_refusal.py passed 23/23 on each of five runs.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:35:14.720Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-119-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:19.698Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T119_r3/scripts/check_r3.py\" <<'EOF'\nimport json, re, sys\ntext = open(sys.argv[1], encoding=\"utf-8\").read()\nblocks = re.findall(r\"```json\\n(.*?)```\", text, re.S)\nprint(\"json fences:\", len(blocks), \"| all fences:\", text.count(\"```\"))\ndata = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in data[\"findings\"]]\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", data[\"card\"], \"| persona\", data[\"persona\"], \"| model\", data[\"model\"])\nprint(\"severities\", sev, \"| rule verdict\", rule, \"| written verdict\", data[\"verdict\"], \"| match\", rule == data[\"verdict\"])\nprint(\"whats_right\", len(data[\"whats_right\"]), \"| exercised\", len(data[\"exercised\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T119_r3/scripts/check_r3.py\" /Users/arsis/zlayt-pm-project/reviews/T-119-staff-engineer-r3.md; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Parse the review JSON block and check the verdict rule and fence count"
}
````

### User / tool · 2026-11-02T11:35:19.882Z

**tool result**
````
json fences: 1 | all fences: 2
card T-119 | persona staff-engineer-reviewer | model claude-haiku-5-5
severities ['minor', 'minor', 'minor', 'nit', 'nit'] | rule verdict pass | written verdict pass | match True
whats_right 3 | exercised 13
ok (130 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:27.180Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t119_keyboard_coverage_patterns.md",
 "content": "---\nname: t119-keyboard-coverage-patterns\ndescription: T-119 r1 (6e880e6, changes), r2 (d9efc5c/e1ce8dc, changes), r3 (c559ce2, pass): row-gate negative test, p-gate mutB now killed, vis() exits at first in-viewport frame, count artifact without sha\nmetadata:\n  type: project\n---\n\nRecurring patterns from the T-119 reviews (reviews/T-119-staff-engineer.md r1, -r2.md, -r3.md; card commits 6e880e6, d9efc5c, c559ce2).\n\n- **A green keyboard suite can hide a dropped negative rule.** T-060 made letter keys act only from an item row (sidebyside.js:102 for p, review.js:307-311 for the rest). Round 1 found that no test asserted a/d/j/p from the body does nothing, and the p gate survived 129 passing tests in r2 (mutB). r3 added a p-specific negative test (test_polish_r3.py:105-122), which kills mutB at :117. **How to apply:** for every single-key gate, run a mutant of that gate and check the key is in a test.\n- **Programmatic focus is not keyboard reach.** The Tab-only test (test_polish_r3.py:41, Tab presses) is the R-RV-4 proof; test_keyboard_mobile.py:9 now says it is the focus-first path. **How to apply:** grep `keyboard.press(\"Tab\")` before accepting any keyboard-only claim.\n- **Contract docstring drift.** conftest.py tray copy was fixed in e293daa (not c559ce2 as the handoff said); grep the old sentence in the archive at the pinned sha, not in the working tree.\n- **Retry-to-first-pass is a weaker assertion.** vis() (test_code_check_refusal.py:93-102) returns True on the first frame the box is in the viewport, where the one-shot read it replaced asserted a single position. A box that enters and leaves passes. A permanently off-screen box still fails. **How to apply:** when a one-shot read becomes a poll, require the position to hold for two frames, or assert at rest.\n- **Artifacts without a sha do not reproduce.** artifacts/t119-r3-e2e-full.txt says 192 passed; c559ce2 collects 207 and runs 206 passed, 1 skipped. The nearest tree checked (d56328a) collects 192. **How to apply:** before accepting a count in an artifact, run --collect-only on the stated sha; reject any artifact with no sha.\n- **Skip reconciliation.** ZLAYT_DB gates add 15 skips when unset (test_code_check_refusal.py:26,183, test_change_the_quote.py); with ZLAYT_DB set they run. The only remaining skip is test_ladder_gate.py:37 (ADR-005, still open since r1). **How to apply:** reconcile the total with collected count before quoting skips.\n\nEnvironment notes: the git-guard hook refuses `$(...)` inside `for` loops and `echo` lines with unresolved variables; write checkers in a heredoc under scratch and run with `python -I`. Record the server PID with `$!` only after checking it with `ps -p` (see [[feedback_verify_pid_before_kill]]). Mutants were scratch copies of the archive, each on its own port and sqlite file.\n\nSee also [[project_e2e_contract_review_patterns]], [[project_t115_e2e_curated_patterns]], [[project_t065_batch_fallback_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T11:35:27.269Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t119_keyboard_coverage_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:30.363Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_verify_pid_before_kill.md",
 "content": "---\nname: feedback_verify_pid_before_kill\ndescription: a PID captured with $! from a subshell can be a wrapper, not the server; run ps -p and lsof on the port before kill, and kill the listener, not the recorded number\nmetadata:\n  type: feedback\n---\n\nBefore killing a server, check the PID you recorded with `ps -o pid,ppid,command -p <pid>` and check the listener with `lsof -iTCP:<port> -sTCP:LISTEN -n -P`. Kill the listener and confirm the port is closed.\n\n**Why:** T-119 r3 (this session): I wrote `echo $!` from a subshell that started `nohup python -m app.main &`. The recorded PID (6353) was a bash wrapper, not the server. I killed it without checking. The real server (6354) stayed up and had to be stopped by its listener PID. The ports were closed only after that second kill.\n\n**How to apply:** when a review starts its own servers, record the listener PID with lsof after the health check, not `$!`. Stop only PIDs whose command line shows the app, and verify both ports closed afterwards. If a wrong PID was killed, say so in the review's exercised list.\n\nRelated: [[project_t119_keyboard_coverage_patterns]], [[feedback_shared_scratchpad]].\n"
}
````

### User / tool · 2026-11-02T11:35:30.476Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_verify_pid_before_kill.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:31.862Z

**tool call — Bash**
````
{
 "command": "grep -n \"T-119\\|verify_pid\" .claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "description": "Find the existing T-119 index line in memory"
}
````

### User / tool · 2026-11-02T11:35:31.944Z

**tool result**
````
46:- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes: focus() replaces key route, no WCAG 2.1.4 negative test (mutants survive), no Tab E2E, stale conftest copy
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:34.023Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes: focus() replaces key route, no WCAG 2.1.4 negative test (mutants survive), no Tab E2E, stale conftest copy",
 "new_string": "- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes; r2 changes (p gate); r3 c559ce2 pass: vis() first-frame poll, count artifact without sha\n- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof listener before killing own servers"
}
````

### User / tool · 2026-11-02T11:35:34.132Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:35:35.676Z

Verdict pass (no blocker, no major): the new p-key test kills mutB at test_polish_r3.py:117 and passes on HEAD, but the five-run acceptance for the vis() flake is unmet and the card's full-run artifact does not reproduce. Review is at /Users/arsis/zlayt-pm-project/reviews/T-119-staff-engineer-r3.md.
