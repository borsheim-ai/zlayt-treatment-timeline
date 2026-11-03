# T-157 review: staff-engineer-reviewer (commit 926bf37)

Verdict: **changes** (0 blockers, 3 majors, 3 minors, 2 nits). Verdict rule: no blocker, so not fail; majors present, so changes.

Scope: commit 926bf37 (HEAD at review time). Reviewed on a `git archive 926bf37` copy in my scratchpad. Untracked `artifacts/review-evidence` (1576 files) was overlaid with no-clobber because `tests/unit` reads it. Fixture backend, in-process TestClient, no live app URL.

What holds: the code implements the four brief items. Title create, PATCH rename and the derived default work, and the default is never "Untitled case". `rerun_available` is false in demo/fixture mode and after a no-answer rerun. `next_action` is code-only, with blockers ahead of needs-review items and a total sort key that ends in the item id. The 13 `test_case_list.py` tests pass, and the full `tests/unit` run has no failures on this copy.

What does not hold: the brief asks for HTML validation of titles, and there is none. Two `next_action` rules (blockers first, first-in-timeline pick) have no test that fails when they break. Two mutants survive, so the tests do not prove the AC.

Findings (detail in the JSON block):
1. major: titles are stored and returned with markup unchanged. Not exploitable in the shipped UI, because the frontend writes text nodes.
2. major: blockers-first rule is untested. Mutant `first = None` leaves all 13 tests green.
3. major: first-in-timeline pick is untested. Mutant `waiting[-1]` leaves all 13 tests green.
4. minor: the card's full-suite evidence (4387 passed, 2 failed) does not reproduce at 926bf37. My run gave 4286 passed, 8 skipped, 0 failed.

```json
{"card": "T-157", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 926bf37 (HEAD at review time): app/backend/api.py, case_list.py, present.py, store.py, memory/contracts/api.md, tests/unit/test_case_list.py. Reviewed on a git archive copy of 926bf37 with untracked artifacts/review-evidence overlaid (tests read it). Fixture backend, in-process TestClient, no app URL. Case under test: evals/library case_lib01_er_only_then_gap (plus a pasted-and-named case and a library-created title case).",
 "exercised": [
  "python3 tools/board.py show T-157 (card AC, handoff, rounds 0, commits 926bf37)",
  "cat memory/contracts/api.md; sections read: conventions line 46 (untrusted strings are plain text), POST /api/cases (line 60, title), PATCH row (line 54), GET case rerun_available (line 132), next_action (line 705), Case titles (line 703)",
  "git show --stat 926bf37; git show 926bf37 -- app/backend/api.py app/backend/case_list.py app/backend/present.py app/backend/store.py memory/contracts/api.md tests/unit/test_case_list.py (full diff read)",
  "git archive 926bf37 | tar -x into the scratchpad archive dir; overlaid artifacts/review-evidence with cp -Rn (1576 untracked files)",
  ".venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '13 passed in 8.00s'",
  ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider on the archive: '4286 passed, 8 skipped in 275.41s (0:04:35)', 0 failed (full output at the scratchpad full-unit.out file)",
  "mutant A: case_list.py:136 'w = waiting[0]' -> 'waiting[-1]'; pytest test_case_list.py: '13 passed in 6.33s' (survived)",
  "mutant B: case_list.py:131 'first = next(...)' -> 'first = None'; pytest test_case_list.py: '13 passed in 7.64s' (survived)",
  "mutant C: case_list.py:117 sort key with rank before date; pytest: '1 failed, 12 passed' (killed by test_next_action_orders_by_record_date_not_by_kind_or_id)",
  "mutant D: present.py:40 drops the no-answer clause; pytest: '1 failed, 12 passed' (killed by test_rerun_available_follows_live_mode_and_the_last_rerun)",
  "mutant E: case_list.py:23 MAX_TITLE 120 -> 200; pytest: '1 failed, 12 passed' (killed by test_title_on_create_and_patch)",
  "every mutant file restored from 'git show 926bf37:<path>' and confirmed identical with diff -q",
  "HTML probe (scratchpad t157-html-probe.py, run with python -I, fixture env): POST /api/cases library + title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH title '<script>x</script>\\u0007Acme' -> 200 title '<script>x</script> Acme'; GET case returns the same string",
  "PATCH body probe (scratchpad t157-probe2.py): body JSON string '\"title\"' -> 400 bad_request; body '[\"title\"]' -> 400 bad_request; {\"title\": 5} -> 400 bad_request",
  "review response for a dismiss carries item.rerun_available = false (fixture); GET case tray item has no rerun_available key",
  "readable_title probe: 'case_01_' -> 'Records added Nov 1'; '.txt' -> same; 'case_lib01_' -> same; '  ' -> same",
  "read app/backend/api.py:116-119 (live_enabled, demo_mode = not live_enabled) against app/backend/store.py:11-16 (live_model_available)",
  "read app/backend/rejudge.py:64-80 and review.py:385 (rejudge attempts stored with verdict; edit pops ladder.rejudge)",
  "grep for 'Untitled' in app tests tools evals; grep for case name/title readers in app (none reach a prompt, the letter or the export)",
  "frontend sinks: app/frontend/dom.js:5-17 (ZL.el writes text nodes), app/frontend/overview.js:51 and 76-84 (title passed to el as text); grep for innerHTML on title paths (none)",
  "grep for bare except / except: pass in the diff (none added; only try/finally in get_case_view)"
 ],
 "verdict": "changes",
 "scores": {"card_acs_implemented": 4, "tests_prove_acs": 2, "title_input_validation": 2, "rerun_available_correct": 4, "next_action_determinism": 4, "contract_consistency": 3, "honest_failure": 4},
 "findings": [
  {"severity": "major",
   "title": "Case titles are not validated for HTML (brief check fails); markup is stored and returned verbatim",
   "evidence": "Probe output (scratchpad t157-html-probe.py, python -I): create with title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH '<script>x</script>\\u0007Acme' -> 200 '<script>x</script> Acme'; GET case same. Code: app/backend/case_list.py:23-29 clean_title only maps control characters and collapses whitespace, then truncates to 120; no markup check. Derived default copies record text: case_list.py:32-47 derived_title uses clean_title(r['source_label']) on the Source header of a record, which api.md line 46 treats as untrusted. The contract's plain-text rule (api.md:46) lists record text, excerpts and summaries but not titles.",
   "why_it_matters": "The brief requires titles validated for length and HTML. Length is validated (120, test_case_list.py:185-186); HTML is not. Not a live XSS today: app/frontend/dom.js:5-17 writes text nodes and overview.js:76-84 passes the title to el() as text. But the value is untrusted record text in a field the contract does not cover, so the first innerHTML sink added later becomes stored XSS. Rated major (not blocker) because no current sink renders markup; this is a missed required check, not an unsafe shipped path.",
   "fix": "Decide the rule and enforce it in clean_title. Either reject typed titles containing < or > with 400 bad_request (detail.reason 'title_markup'), and strip tags from derived titles (source label becomes plain text), or document titles as plain text in api.md line 46 and keep the derived text escaped. Add both to the api.md title paragraph (line 703).",
   "acceptance_test": "Unit: clean_title('<img src=x onerror=alert(1)>Rivera') contains no '<' (or the typed path returns 400 bad_request). Integration: POST /api/cases with title '<script>x</script>' returns 400 bad_request, and PATCH with the same returns 400 and leaves the stored name unchanged. Derived title for a record with Source '<b>Clinic</b>' contains no '<'."},
  {"severity": "major",
   "title": "next_action blockers-first rule has no test that fails when it breaks (mutant survives)",
   "evidence": "app/backend/case_list.py:131 'first = next((b for b in blockers if b[\"reason_code\"] != \"NOTHING_ACCEPTED\"), None)' mutated to 'first = None' (scratch archive only). '.venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider' -> '13 passed in 7.64s'. The only blocker assertion is tests/unit/test_case_list.py:248-251 and it runs only for a library case that has an item blocker; under the mutant that assertion would fail, so no case in the suite reaches it. api.md:705 says 'tests/unit/test_case_list.py ... checks the order rules'.",
   "why_it_matters": "T-157 AC says next_action must be blockers first. A regression that surfaces a waiting item ahead of an export blocker (for example a JUDGE_NOT_RUN accept) would pass CI, and the paralegal would be sent to the wrong item. This is the determinism rule the card exists for.",
   "fix": "Add a case where an accepted AI-made item has no second-check answer (JUDGE_NOT_RUN) or a code-check failure on an accepted edit, while other items still wait. Assert next_action equals the blocker, and assert the scenario was actually built (no silent skip). Also add an assertion that next_action is None-free when a blocker exists.",
   "acceptance_test": "Scratch mutant 'first = None' in case_list.py:131 must turn the new test red. Test asserts next_action == {item_id, kind, reason} of the export-gate blocker, with a needs-review item present in the same case."},
  {"severity": "major",
   "title": "next_action timeline pick is untested (mutant survives); test only checks the sort of its own helper",
   "evidence": "app/backend/case_list.py:136 'w = waiting[0]' mutated to 'w = waiting[-1]' (scratch archive only); pytest tests/unit/test_case_list.py -> '13 passed in 6.33s'. tests/unit/test_case_list.py:253-256 only asserts that next_action names some needs-review item. tests/unit/test_case_list.py:272-283 asserts that needs_review_order's own output is sorted by the same key the code uses (order == sorted(order, key=...)), which does not test the pick.",
   "why_it_matters": "The AC says the single first thing is the first needs-review item in timeline order. Nothing proves the field is that item, so a change to the index or to the review order would pass. The api.md line 703 claim that the tests 'check the order rules' overstates the coverage.",
   "fix": "For each library case with a waiting item and no blocker, assert next_action['item_id'] == case_list.needs_review_order(conn, tok)[0]['id'], and assert the chosen item's cited record date is the earliest of the waiting set. Include a case where kind order and date order disagree, so the test cannot pass on id or kind alone.",
   "acceptance_test": "Scratch mutant 'waiting[-1]' at case_list.py:136 must turn the test red. Test: for every library case with waiting items and no blocker, next_action.item_id equals the earliest-dated waiting item."},
  {"severity": "minor",
   "title": "Card evidence for the full unit suite does not reproduce at 926bf37",
   "evidence": "board/cards/T-157.md AC evidence: 'full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend)'. My run on the 926bf37 archive (with review-evidence overlay): '4286 passed, 8 skipped in 275.41s', 0 failed. .venv/bin/python -m pytest tests/test_e2e_contract.py --co reports 'no tests collected', and the file is not under tests/unit.",
   "why_it_matters": "Evidence that cannot be reproduced cannot support the verdict. The worker may have run a dirty working tree (git status shows uncommitted product files from other cards). Not a code defect in T-157, but the card cites a file outside the suite it names.",
   "fix": "Rerun 'python3 -m pytest tests/unit -q' from a clean archive of the commit, paste the exact command and tail into the card AC evidence, and drop the test_e2e_contract line unless it is reproduced in tests/unit.",
   "acceptance_test": "Card AC evidence includes the command and the pytest summary line, and it matches a fresh git archive run."},
  {"severity": "minor",
   "title": "rerun_available re-derives the demo/live rule instead of using the one that defines demo mode",
   "evidence": "app/backend/store.py:11-16 live_model_available() = name != 'fixture' and ENABLE_LIVE == '1' and (claude-cli or ANTHROPIC_API_KEY). app/backend/api.py:116-119 live_enabled() = ENABLE_LIVE == '1' and (backend() == 'claude-cli' or key); demo_mode() = not live_enabled(). The two agree by reading today, but two definitions of 'live' can drift, and the spec says demo mode is the gate.",
   "why_it_matters": "If the two drift, the item could say a rerun can answer in demo mode, which is the failure the AC forbids. Nothing in the suite asserts they agree.",
   "fix": "Have present.rerun_available use the same demo_mode/live function as the API (move the definition to one module), and add a parametrized test over LLM_BACKEND, ENABLE_LIVE and ANTHROPIC_API_KEY asserting rerun_available is False whenever demo_mode() is True.",
   "acceptance_test": "Parametrized test: for each env combination, rerun_available == (not demo_mode()) for a fixture item."},
  {"severity": "minor",
   "title": "The anthropic-api-without-key assertion is conditional and can pass without checking anything",
   "evidence": "tests/unit/test_case_list.py:227-229: 'other = [...][:1]' then 'if other: assert other[0][\"rerun_available\"] is False'.",
   "why_it_matters": "If the library case has no flags or amounts, the no-key branch asserts nothing, and a regression would pass silently.",
   "fix": "Name a specific item id from the case and assert on it unconditionally.",
   "acceptance_test": "Test asserts rerun_available is False for a named flag or amount with LLM_BACKEND=anthropic-api and no key, without an if-guard."},
  {"severity": "minor",
   "title": "PDF title query parameter is untested",
   "evidence": "app/backend/api.py:252 create_case_from_pdf(..., title: str = None) and the make_case call passing 'title if title is not None else name'. No test in tests/unit/test_case_list.py posts to /api/cases/pdf with title. api.md line 60 documents the parameter.",
   "why_it_matters": "A documented input path with no test can regress (for example the name would be dropped), and nothing would fail.",
   "fix": "Add one test posting an existing synthetic PDF fixture with ?title= and asserting the returned title and GET case title.",
   "acceptance_test": "POST /api/cases/pdf?title=Rivera%20intake returns 201 and title 'Rivera intake'. (Not run by me.)"},
  {"severity": "nit",
   "title": "A stored name that is empty after cleanup skips the record-header default",
   "evidence": "Probe: readable_title('case_01_', 'paste', ...) -> 'Records added Nov 1'; '.txt' and 'case_lib01_' give the same. app/backend/case_list.py:61-65 case_title uses readable_title whenever name is non-blank, so the header default (api.md:703 rule 2) is never reached for such names.",
   "why_it_matters": "Still never 'Untitled case', so no contract breach. The title is less useful than the first record header and differs from the documented order.",
   "fix": "Treat an empty readable name as no name and fall through to derived_title.",
   "acceptance_test": "case_title for a case named 'case_01_' returns the derived header title when a record has a Source line."},
  {"severity": "nit",
   "title": "Frontend still carries an Untitled case fallback (outside this commit)",
   "evidence": "app/frontend/overview.js:51 titleOf: '... || \"Untitled case\"'. Unreachable today because the backend always sends a non-empty title.",
   "why_it_matters": "Dead text, but it is the string the AC bans, and a future backend null would show it.",
   "fix": "Route to the frontend card: drop the fallback and fall back to the backend title only.",
   "acceptance_test": "grep -rn 'Untitled case' app/frontend returns nothing."}
 ],
 "whats_right": [
  "next_action and needs_review_order are code-only and deterministic: the sort key ends in the item id (case_list.py:117) and the no-model-call test passes.",
  "rerun_available is false in fixture/demo mode and after a no-answer rerun; the review response carries it and tray items omit it, as api.md requires (mutant D killed).",
  "PATCH rejects non-object bodies, non-text titles and unknown tokens with explicit 400/404, and the 120-character cap is enforced by test (mutant E killed)."
 ],
 "questions_for_chris": [
  "For typed titles that contain < or >, do you want a 400 (reject) or stored-as-text with escaping at the sink? The answer decides the fix for finding 1."
 ]}
```
