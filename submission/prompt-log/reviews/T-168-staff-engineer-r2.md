# T-168 round 2: staff-engineer-reviewer (commit 56004f0)

Verdict: pass. No blocker, no major. One nit. Run on `git archive 56004f0` (control `git archive 235e135`) with the repo `.venv/bin/python`. HEAD at review time was 8398bee; `git diff --stat 56004f0 HEAD -- app/llm tests/unit/test_t168_strict_judge_parse.py tests/unit/test_provider_backends.py` is empty, so the reviewed files are what is at HEAD.

**Major 1 (judge took a later "supported" object) is fixed.** `parse_json_reply` is strict by default (`app/llm/_types.py:59`). The closing-object read is opt-in through a contextvar (`_types.py:42`, default False) that `audited_call` turns on only for `LENIENT_JSON_STEPS = {"extract","extract_es"}` (`audited.py:17`, `audited.py:82`). The contextvar is set and reset in the same thread as the provider call (provider.py has no thread pool or executor), and `lenient leaked: False` after every step in my probe.
- Strict default, my 20 r1 shapes on the 56004f0 archive: every two-object, prose-before, prose-after, truncated-outer and trailing-fake-after-fence shape is INVALID_JSON. Only case 04 (braces inside strings) and case 18 (duplicate keys inside one object, last wins, pre-existing json.loads behaviour) parse. On the 235e135 control, 01, 03, 05, 06, 07, 08, 09, 10, 13, 16, 17 all parsed. Case 19 RecursionError is identical on both (pre-existing, not charged).
- Per step through `audited_call` with the claude-cli subprocess mocked, replies A (unsupported then supported) and B (supported then unsupported): j1, j2, j3, j4, judge_1, flags, conflicts, split, narrative all give `LLMFailed INVALID_JSON` in both orders (three attempts each). extract and extract_es parse the closing object (A gives supported, B gives unsupported, which is the intended last-object read for the generator).
- Truncated outer in lenient mode: `{"result": {...}` (08), the truncated array (09), a closing object cut mid-key, mid-string or after a comma (21-23), and a judge-like wrapper after a draft (26) are all INVALID_JSON.
- lib01 on the fixture backend at 56004f0: status done, errors `[]`, DB status ready.

**Tests.** `test_t168_strict_judge_parse.py` + `test_provider_backends.py` + `test_curated_fixtures.py`: 68 passed. `tests/unit` on the archive: 5321 passed, 2 failed, 8 skipped (253 s). The 2 failures are the known unrelated ones: `test_e2e_contract::test_every_test_id_is_declared` and `test_eval_runner::test_committed_calibration_header_names_backend_and_a_clean_source_commit` (asserts backend fixture, committed header says claude-cli). Mutation script `artifacts/review-evidence/T-168/mutants_r2.py`, 10 mutants on the T-168 tests plus test_provider_backends: M1 j1 made lenient (2 red), M2 default on (16), M3 EOF error continues scan (2), M5 never reset (8), M6 drop the end-of-reply check (12), M7 extract_es dropped (1), M8 never lenient (10), M9 inverted step test (14), M10 take first object (12) all red. M4 (resume scan inside a skipped complete object) stays green; it is an equivalent mutant, because an inner object of a complete outer cannot reach the end of the reply.

The r1 second major (boundary untested, docstring stale) and the r1 minor (truncated outer returns inner) are also closed: the docstring at `_types.py:60-64` now says STRICT by default, and the parametrized lists at test_t168_strict_judge_parse.py:95-122 pin prose-before, three objects, braces in strings, truncated outer, closing object cut off and prose after a fenced object.

```json
{"card": "T-168", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 56004f0 (control 235e135; HEAD 8398bee has no change to app/llm or the T-168 tests): app/llm/_types.py, app/llm/audited.py, app/llm/backends/claude_cli.py, tests/unit/test_t168_strict_judge_parse.py, tests/unit/test_provider_backends.py; lib01 on the fixture backend; no live app",
 "exercised": [
  "read reviews/T-168-staff-engineer.md (r1) and git show 56004f0 (all five files, full diff)",
  "git archive 56004f0 and 235e135 into scratch dirs; re-ran artifacts/review-evidence/T-168/probe_parse_json_reply.py on both: strict default now INVALID_JSON for cases 01-03, 05-13, 15-17, 20; 04 and 18 parse (single object); 19 RecursionError same on both",
  "wrote and ran artifacts/review-evidence/T-168/probe_r2_lenient_and_steps.py on the 56004f0 archive: Part A strict vs lenient on 13 shapes incl. truncated closing objects (21-23); Part B audited_call over j1, j2, j3, j4, judge_1, flags, conflicts, split, narrative, extract, extract_es with two-object replies in both orders (claude-cli subprocess mocked): all non-extract steps LLMFailed INVALID_JSON, extract and extract_es read the closing object, lenient flag False afterwards",
  "grep parse_json_reply, lenient_json and _closing_object across app/: one caller (backends/claude_cli.py:67), one opt-in site (audited.py:82); grep for threads/executors in provider.py, backends and audited.py: none, so the contextvar reaches the parser",
  "pytest test_t168_strict_judge_parse.py + test_provider_backends.py + test_curated_fixtures.py on the archive: 68 passed",
  "pytest tests/unit on the 56004f0 archive: 5321 passed, 2 failed (test_every_test_id_is_declared; test_committed_calibration_header_names_backend_and_a_clean_source_commit), 8 skipped",
  "mutants_r2.py: 10 one-line mutants, 9 red, M4 equivalent and green",
  "ran lib01_fixture_run.py on the 56004f0 archive: status done, errors [], DBSTATUS ready; git diff --stat 56004f0 HEAD -- app/llm and the T-168 tests: empty"],
 "verdict": "pass",
 "scores": {"parser_safety": 5, "recordings_integrity": 4, "lib01_outcome": 5, "tests": 4, "determinism": 5},
 "findings": [
  {"severity": "nit", "title": "Lenient (extract-only) scan resumes at inner braces after a malformed, non-truncated outer, so a malformed reply can still resolve to an inner object that ends the reply",
   "evidence": "probe_r2_lenient_and_steps.py Part A lenient: case 24 '{\"summary\":\"x {\"summary\":\"c\",\"excerpt\":\"d\"}' -> PARSED {\"summary\": \"c\", \"excerpt\": \"d\"}; case 25 '{\"summary\":\"a\",\"excerpt\":\"b\"} Wait {\"note\": oops {\"summary\":\"c\",\"excerpt\":\"d\"}' -> PARSED {\"summary\": \"c\", \"excerpt\": \"d\"}. app/llm/_types.py:94-97: only an EOF decode error (e.pos >= len(t)) stops the scan; any other decode error moves to the next '{'. This is the documented 'stray brace in prose is skipped' rule, and true truncation (EOF) is correctly refused, so it does not contradict the r1 fix. Also, lenient mode accepts a bare object after a fenced block (case 13) and a prose-then-object reply (case 17) with no test pinning either.",
   "why_it_matters": "Extract only, and the output still goes through schema validation, the excerpt substring check and judge 1, so a wrong object cannot reach the export without the ladder. It is noted because a malformed outer is read as its inner fragment with no state saying the outer was discarded.",
   "fix": "Optional: add the two shapes to the lenient parametrize list so the intended behaviour (accept or reject) is written down; if reject is wanted, stop the scan on any decode error whose position is inside a '{'-started object that is not followed by prose.",
   "acceptance_test": "Cases 24 and 25 are pinned in test_t168_strict_judge_parse.py as either accepted or INVALID_JSON, and a mutant that flips the choice turns a test red."}
 ],
 "whats_right": [
  "Strictness is the default and leniency is a scoped, per-context opt-in for exactly extract and extract_es; every judge and every other step fails visibly with INVALID_JSON on two objects in either order.",
  "The new test file pins both orders for j1-j4, the no-leak and reset-on-raise cases, and the lenient boundary; 9 of 10 mutants go red and the survivor is equivalent.",
  "lib01 still reads ready on the fixture backend (done, errors [], ready) and the recordings and curated files are untouched."],
 "questions_for_chris": []}
```
