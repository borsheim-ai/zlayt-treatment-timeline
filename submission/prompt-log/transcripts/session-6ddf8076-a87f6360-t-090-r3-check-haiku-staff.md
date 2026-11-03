# Subagent: T-090 r3 check (haiku staff) (T-090 r3 check (haiku staff))

Source: `agent-a87f63607361876b0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:49:08.663Z

Round-3 check of board card T-090 in /Users/arsis/zlayt-pm-project (commits b85fc1b and 172028c). Read reviews/T-090-staff-engineer-r2.md, and confirm:
- the r2 code and tests are in HEAD;
- a forged or non-ancestor source_commit fails the tests and isn't skipped (try it in a scratch copy);
- calibration.json regenerates exactly from its recorded commit: use a `git archive <commit>` copy in your scratchpad, since reviewers can't use worktree;
- source_tree is checked against git;
- the served field has moved to T-096, with its shape noted there.

Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Write reviews/T-090-staff-engineer-r3.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:11.209Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:49:11.217Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:11.435Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-02T04:49:11.444Z

**tool result**
````
1	# T-090 round 2 review: calibrated confidence, provenance and majors (commits 823b718, 02ff244)
2	
3	**Verdict: fail.** The file itself reproduces exactly from its source commit 823b718, and the r1 majors are mostly fixed in the commit. But a later commit, 2fca530 (T-087/T-086, sits between 823b718 and 02ff244), deleted the r2 code and its 11 tests, so HEAD (865b186) has neither. That re-opens the r1 blocker at HEAD. Two more majors and two minors remain.
4	
5	Method notes. The brief named `git worktree add`, which board-guard blocks in the project tree, so I used a scratch clone of the project with `git checkout --detach 823b718` (same result: a clean tree at 823b718). Scratch evidence is in `artifacts/review-evidence/T-090-staff-r2/` (`mutation-and-command-log.txt`, regenerated `calibration.json` copies). Regeneration used `python -I` with the scratch clone on `sys.path`, fixture backend, `LLM_BACKEND` and `ENABLE_LIVE` unset.
6	
7	## What reproduces
8	
9	| Check | Result |
10	|---|---|
11	| Regenerate at 823b718, run 1 vs committed file (generated_at removed) | equal |
12	| Regenerate at 823b718, run 2 vs run 1 | byte-identical except generated_at |
13	| Counts | verified 83/84, needs_review 10/10 (same as committed) |
14	| Header | `source_commit` 823b718817cacf6d38cf179724fd374ad09dffdf, `source_tree_clean` true, `backend` fixture, 12 hashes (11 prompts + lexicon), `models` generator claude-sonnet-5-5 / judge claude-haiku-5-5 |
15	| Percent signs in calibration.json and in the sentence builder | 0 |
16	| `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` in the project tree | 84 passed, 1284 deselected, 0 skipped |
17	| Same selector at 823b718 code with the 02ff244 file (scratch clone) | 84 passed, 0 skipped |
18	| Same selector at 02ff244 (file commit, code as left by 2fca530) | 71 passed |
19	
20	## Finding 1 (blocker): the r2 fix is not in HEAD
21	
22	`git show 2fca530 -- evals/run.py` removes `git_source` and reverts the `unscored`/candidate-state changes. `git show 2fca530 -- tests/unit/test_eval_runner.py` removes 11 `^-def test_` lines, including `test_committed_calibration_regenerates_exactly_from_its_source_commit`. `git show 02ff244:evals/run.py | grep -c 'def git_source'` is 0. `git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py` exits 0, so HEAD carries the reverted code. The 84 passed in the project tree comes from uncommitted edits (`git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py`: 383 insertions, and the working-tree `evals/run.py` also differs from 823b718 at line 505). The card's AC evidence therefore cannot be reproduced from HEAD.
23	
24	The consequence is the r1 blocker again. Running `python -m evals.run` at 02ff244 code overwrites calibration.json without `hashes`, `not_scored`, `source_commit` and `source_tree_clean`, and the sentences change (`artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json`). The committed header still names 823b718, and nothing in HEAD can check it.
25	
26	Why blocker and not major: the shipped provenance guard (the traceability the card exists for) is absent from the committed code, so a rerun at HEAD does not produce the file it ships. I cannot downgrade this because the fix lives in another card's commit.
27	
28	## Finding 2 (major): a forged source_commit passes by skipping
29	
30	`tests/unit/test_eval_runner.py:635-638` skips the ancestor test when `cat-file -e <source_commit>^{commit}` fails, labelled "no git history here". `:642-647` skips the regeneration test with "source commit not available in this checkout". So a hand-edited header naming a commit that does not exist passes, with 2 skips. Mutant M-C (`source_commit` = `"1"*40`, 823b718 code, 02ff244 file): `82 passed, 2 skipped`. The brief asked that hand-edits fail the tests. This one does not.
31	
32	## Finding 3 (major): the served field has no owner
33	
34	Card AC 1 (board/cards/T-090.md) now reads "served field and UI line are carried by T-096 (frontend)". `python3 tools/board.py show T-096` shows its AC 1 covers only the "Verified items matched the record N/M times in testing" line "(T-090)". No backend route is in any AC. `grep -rln calibration app/` returns nothing (exit 1). The r1 fix asked that the served field be linked to a backend card; the narrowing removed the link rather than adding one.
35	
36	## Finding 4 (minor): check-fresh passes an edited sentence
37	
38	The card says check-fresh validates calibration.json. `evals/run.py:962` (`check_calibration`) checks only that by_state equals the sum of by_type and that hashes match the files. With the sentence changed from 83/84 to 84/84 and counts untouched, `R.check_fresh` returns 0 (log item 5). The regeneration test catches it, but only under pytest with git history.
39	
40	## Finding 5 (minor): the clean flag is not checked by the regeneration test
41	
42	`tests/unit/test_eval_runner.py:660` sets `fresh["source_tree_clean"] = c["source_tree_clean"]`, copying the file's own value into the comparison. Only the header test (`:629-633`) pins it to true. A file generated from a dirty tree that forges `true` passes both tests. This is minor because the committed file's commit is clean, but the header field is not verified.
43	
44	## Majors from r1: status
45	
46	- Blocker (not reproducible): fixed in 823b718/02ff244 (regeneration reproduces); reopened at HEAD by Finding 1.
47	- Major 2 (AC 1 closed with UI unbuilt): narrowed to the eval side; the UI is claimed by T-096, but the served field is not (Finding 3).
48	- Major 3 (amount class not tested): fixed. Mutant C1 (drop class term) turns `test_amount_class_is_part_of_the_match` red.
49	- Major 4 (sentences name no backend): fixed. Mutant C2 (drop backend from caveat) turns 3 parametrized sentence tests red. The fixture sentence reads "on the fixture backend (recorded replies, 10 golden cases, small sample)".
50	- Minors: 29/30 boundary (C3 killed), tolerated flag (C4 killed), not-scored disclosure (C5 killed), record_warning alignment (C6, candidate state dropped, killed broadly), check-fresh covers calibration.json (partly; Finding 4).
51	
52	Hand-edit mutants on the 823b718 code with the 02ff244 file: count in by_state (killed, 2 tests), sentence text (killed), count in by_type only (killed, 2 tests), stale hash (killed), clean flag false (killed). Only the forged source_commit survives (Finding 2).
53	
54	## Outside my lens
55	
56	The ship bar is not met on the fixture run (`4_no_invented_facts`, determinism and judge controls not measured). Those are existing ship-bar items, not T-090. I did not judge the frontend wording.
57	
58	```json
59	{"card": "T-090", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
60	 "scope": "commits 823b718 (evals/run.py, tests/unit/test_eval_runner.py) and 02ff244 (evals/reports/calibration.json); HEAD 865b186 checked for the code; scratch clone of the project at detached 823b718 and 02ff244 (git worktree blocked by board-guard); no app URL (no calibration route or UI exists: grep -rln calibration app/ returns nothing); sample case = fixture backend over the 10 golden cases",
61	 "exercised": [
62	  "read personas/staff-engineer.md, reviews/T-090-staff-engineer.md (r1), board/cards/T-090.md, board/cards/T-096.md via board.py show",
63	  "git show --stat 823b718, 02ff244, 2fca530; git show 823b718 -- evals/run.py and -- tests/unit/test_eval_runner.py; git show 2fca530 -- evals/run.py and -- tests/unit/test_eval_runner.py (11 removed test defs, git_source removed)",
64	  "git clone of the project into scratchpad t090r2/clone, git checkout --detach 823b718; regenerated twice: python -I -c runpy evals.run --out <scratch>/out1 and out2 (fixture); out1 and out2 equal to each other and to evals/reports/calibration.json ignoring generated_at (dict compare True, cmp of lines without generated_at byte-identical)",
65	  "header check on committed calibration.json: backend fixture, source_commit 823b718817cacf6d38cf179724fd374ad09dffdf, source_tree_clean true, 12 hashes, models; grep -c '%' calibration.json = 0; percent in build_calibration section of 823b718 = 0",
66	  ".venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' in the project tree: 84 passed, 1284 deselected, 0 skipped",
67	  "same selector at 823b718 code with the 02ff244 calibration.json in the scratch clone: 84 passed; at 02ff244 (clone detached): 71 passed; at 823b718 with its own pre-r2 file: 3 failed, 81 passed (stale file, not recorded further)",
68	  "regeneration at 02ff244 code (scratch clone): keys missing vs committed = hashes, not_scored, source_commit, source_tree_clean; by_state equal; sentences differ (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json)",
69	  "git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exit 0; git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py: 383 insertions; cmp working-tree evals/run.py vs 823b718: differ at line 505; cmp working-tree test_eval_runner.py vs 823b718: identical",
70	  "hand-edit mutants in scratch clone (823b718 code, 02ff244 file): by_state count +1 -> 2 failed; sentence text -> 1 failed; by_type count -> 2 failed; stale hash -> 1 failed; source_tree_clean false -> 1 failed; source_commit = 1*40 -> 82 passed, 2 skipped (test_eval_runner.py:638, :647)",
71	  "code mutants in scratch clone evals/run.py (restored from saved pristine copy): drop class term line 271 -> 1 failed; drop backend in caveat line 317 -> 4 failed; CAL_SMALL_N 30->5 line 243 -> 1 failed; drop tolerated term line 279 -> 1 failed; drop Not-scored sentence line 327 -> 1 failed; drop candidate state in to_candidates -> 35 failed, 5 errors",
72	  "check_fresh(latest.json) with edited sentence, python -I on scratch clone: returned 0",
73	  "board.py show T-096 (AC 1 text, status ready); grep -rln calibration app/ (no output, exit 1)",
74	  "full log: artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt"
75	 ],
76	 "verdict": "fail",
77	 "scores": {"counts_reproduce_from_commit": 5, "header_provenance_at_commit": 4, "provenance_guard_at_HEAD": 1, "hand_edit_detected": 3, "r1_majors_fixed": 3, "ac_closed_honestly": 2, "no_bare_percent": 5, "mutants_killed": 4},
78	 "findings": [
79	  {"severity": "blocker",
80	   "title": "The r2 provenance fix and its tests are reverted at HEAD by commit 2fca530; the card's test evidence is not reproducible from HEAD",
81	   "evidence": "git show 2fca530 -- tests/unit/test_eval_runner.py removes 11 test defs (grep -c '^-def test_' = 11), including test_committed_calibration_regenerates_exactly_from_its_source_commit; git show 2fca530 -- evals/run.py removes def git_source (git show 02ff244:evals/run.py | grep -c 'def git_source' = 0). git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exits 0, so HEAD has the reverted code. Selector at 02ff244: 71 passed (no r2 tests). Project-tree 84 passed comes from uncommitted edits (git diff --stat HEAD: evals/run.py and tests/unit/test_eval_runner.py, 383 insertions). Regeneration at 02ff244 code omits hashes, not_scored, source_commit, source_tree_clean (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json).",
82	   "why_it_matters": "This is the r1 blocker again. The served calibration.json names a source commit whose provenance guard is no longer in the shipped code, so a rerun of python -m evals.run at HEAD overwrites the file with one that has no provenance. The tests that were supposed to fail on a hand edit do not exist at HEAD, so the card's '84 passed' cannot be reproduced from the commits it lists. The 823b718 and 02ff244 commits themselves are correct; the loss happened after them.",
83	   "fix": "Restore the 823b718 versions of evals/run.py and tests/unit/test_eval_runner.py in a new commit that stages those two paths explicitly (git show 823b718:evals/run.py and :tests/unit/test_eval_runner.py are the reference). Do not hand-merge the uncommitted working-tree edits, which differ from 823b718 in evals/run.py (first difference at line 505). Ask the author of 2fca530 to stage by explicit path; the commit staged a stale evals/run.py and test file.",
84	   "acceptance_test": "git show HEAD:evals/run.py | grep -c 'def git_source' is at least 1; at the new HEAD, .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' reports 84 passed with 0 skipped from a clean tree; a regeneration at HEAD (fixture, --out) equals evals/reports/calibration.json ignoring generated_at."},
85	  {"severity": "major",
86	   "title": "A forged source_commit that names no existing commit passes the two provenance tests by skipping",
87	   "evidence": "tests/unit/test_eval_runner.py:635-638 (skip 'no git history here (shallow or exported tree)' when cat-file -e <source_commit>^{commit} fails) and :642-647 (skip 'source commit not available in this checkout'). Mutant on scratch clone (823b718 code, 02ff244 file, source_commit set to '1'*40): .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 82 passed, 2 skipped.",
88	   "why_it_matters": "The brief requires the tests to fail when the file is hand-edited. A header that cites a commit which does not exist is the provenance lie the card was opened to stop, and it is reported green. The skip conflates 'no git at all' (a legitimate export) with 'the cited commit is missing' (a fabricated header).",
89	   "fix": "Skip only when there is no git repository (git rev-parse --git-dir fails). When a repository exists and the cited commit is missing, or the commit is not an ancestor of HEAD, fail with the commit name.",
90	   "acceptance_test": "Set source_commit to '1'*40 in calibration.json; the selector reports at least one failed test and no skip for the provenance tests."},
91	  {"severity": "major",
92	   "title": "The served calibration field has no owner after AC 1 was narrowed",
93	   "evidence": "board/cards/T-090.md AC 1 evidence: 'served field and UI line are carried by T-096 (frontend)'. python3 tools/board.py show T-096 shows AC 1: 'Dates-to-confirm row ... Verified items matched the record N/M times in testing line with small-sample note (T-090); e2e tests', done false, status ready. No AC names a backend route or a read of evals/reports/calibration.json. grep -rln calibration app/ returns no files (exit 1).",
94	   "why_it_matters": "The r1 major asked for the served field to be linked to a backend card. The narrowing moved the UI line to T-096 but left the backend route with no card and no AC, so the sentence the paralegal reads has no path to the screen. The card's AC is narrower and honest about the UI, but the handoff to the backend is unowned.",
95	   "fix": "Add an explicit backend AC (route that returns the calibration.json fields, or null when the file is absent, read-only) to an existing backend card or a new one, and name it in T-090 AC 1 or the T-096 AC.",
96	   "acceptance_test": "board.py show <owning card> lists the route AC; grep -rn calibration app/backend finds the route; curl of the route returns the sentences.overall.verified string from evals/reports/calibration.json verbatim."},
97	  {"severity": "minor",
98	   "title": "check-fresh exits 0 for an edited sentence; it validates sums and hashes only",
99	   "evidence": "evals/run.py:962 check_calibration checks by_state vs sum of by_type and hashes vs files. Scratch-clone repro (python -I, R.check_fresh on a tmp dir with latest.json and the edited calibration.json, verified sentence changed to '84/84 ...'): returned 0.",
100	   "why_it_matters": "The card says check-fresh validates calibration.json. A hand-edited sentence, which the UI renders verbatim, passes the freshness command. Only the pytest regeneration test catches it, and that test needs git history.",
101	   "fix": "Add the calibration.json sentences and not_scored to check_calibration, or regenerate the sentences inside check_calibration from by_state and by_type and compare.",
102	   "acceptance_test": "Edit sentences.overall.verified in a copy of calibration.json; R.check_fresh returns 1."},
103	  {"severity": "minor",
104	   "title": "The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes",
105	   "evidence": "tests/unit/test_eval_runner.py:660 fresh[\"source_tree_clean\"] = c[\"source_tree_clean\"] (823b718 numbering). Only the header test (:629-633) asserts the value is True.",
106	   "why_it_matters": "The clean flag is the only evidence the counts came from an unmodified tree. The regeneration test cannot check it, so a file produced from a dirty tree that says true is indistinguishable from a clean one.",
107	   "fix": "Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.",
108	   "acceptance_test": "A calibration.json whose recorded tree hash differs from the source commit's tree fails the regeneration test."}
109	 ],
110	 "whats_right": [
111	  "calibration.json regenerates exactly from its source commit 823b718 (two runs identical except generated_at; counts 83/84 and 10/10), and the header records source_commit, source_tree_clean true, backend fixture and 12 prompt/lexicon hashes.",
112	  "Hand edits to by_state counts, by_type counts, the sentence text, the hashes and the clean flag each turn at least one test red at 823b718 (mutants M-A, M-B, M-D, M-E, M-G).",
113	  "Sentences name the backend and '(recorded replies, N golden cases)' for the fixture, no percent sign appears anywhere, and the r1 amount-class, tolerated, 29/30 boundary and not-scored mutants are each killed."
114	 ],
115	 "questions_for_chris": [
116	  "Which card should own the backend route that serves calibration.json: a new backend card, or an AC added to T-096?"
117	 ]}
118	```
119	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:12.067Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 8 && echo \"---\" && git rev-parse HEAD && echo \"---\" && git show --stat b85fc1b 172028c | head -80",
 "description": "Show recent commits and stats for the two round-2 fix commits"
}
````

### User / tool · 2026-11-02T04:49:12.194Z

**tool result**
````
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
8bc7f90 fix(backend): billing never totals per-visit rate rows, lists unparsed CMS-1500/ledger rows as unreconciled, verifier runs on the route, unreadable provider is not $0 (T-083 r2)
31b7ceb docs: revert audit for 328428f..bc12d44
0e30623 fix(frontend): scroll the rerun status line into view beside the pressed button (T-097)
c7ba1f1 fix: restore T-075/T-057 work reverted by 865b186 (prompt-version map: j3 judge_conflict_v2 and the conflicts step; T-085 commit had swept in an uncommitted audited.py edit)
d0b5fd8 test(e2e): declare sbs-flags and sbs-show-flag in the hook contract (T-097)
94edf56 fix(frontend): rerun answer shows beside the pressed button, AI-check panel follows the export gate, edited items shown as not AI-checked (T-097, D-045)
---
172028cfcff1750fec094d9e567e9d870a8f7b8e
---
commit b85fc1b56386aa0d37460186b5840eec0e578642
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:48:24 2026 -0600

    fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/run.py                   | 65 ++++++++++++++++++++++++------------------
 tests/unit/test_eval_runner.py | 61 ++++++++++++++++++++++++++++++---------
 2 files changed, 85 insertions(+), 41 deletions(-)

commit 172028cfcff1750fec094d9e567e9d870a8f7b8e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:48:52 2026 -0600

    chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/reports/calibration.json | 7 +++++--
 1 file changed, 5 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:12.631Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md",
 "description": "List reviewer memory dir and read T-090 calibration memory"
}
````

### User / tool · 2026-11-02T04:49:12.713Z

**tool result**
````
MEMORY.md
feedback_review_write_once.md
feedback_severity_vs_brief.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_r2_fix_verification_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_t065_batch_fallback_review_patterns.md
project_t066_no_model_reason_patterns.md
project_t067_r6_d043_patterns.md
project_t070_t067_review_patterns.md
project_t073_t084_review_patterns.md
project_t075_determinism_review_patterns.md
project_t080_trace_review_patterns.md
project_t083_billing_review_patterns.md
project_t088_t089_review_patterns.md
project_t090_calibration_review_patterns.md
project_t093_signature_controls_patterns.md
project_t095_head_revert_patterns.md
project_wiring_review_patterns.md
---
name: t090-calibration-review-patterns
description: T-090 r1 d0aee83 calibrated-confidence review: committed artifact not reproducible from its commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive, fixture-miss log noise from score_unsplit
metadata:
  type: project
---

T-090 r1 (commit d0aee83, calibrated confidence as N/M counts, D-042) written to reviews/T-090-staff-engineer.md: fail, 1 blocker, 3 majors, 4 minors, 1 nit.

- **Committed artifact must be regenerated, not trusted.** evals/reports/calibration.json said 82/83 and 11/13, but `git archive d0aee83` + `evals.run --out` (fixture) gives 83/84 and 10/10 twice, and HEAD ec33bf0 gives the same. No `*T041847Z.md` report existed for its generated_at. Method: pin with git archive, regenerate with --out, diff counts ignoring generated_at, then hand-check two cells from a dump of the raw items.
- **Hand-check cells from raw items, not from the counters.** A dump script (run.py's golden_cases + pipeline.run_case, fixture) lets you tally verified amounts (9/9) and needs-review flags (2/2) by reading golden against live. Found the file's flag cell (3/5) unreproducible.
- **"llm call failed ... FIXTURE_MISS" lines on the eval CLI come from score_unsplit**, not from the golden cases (checked: score_unsplit alone prints 7). Do not read them as calibration misses.
- **Working tree evals/run.py was modified mid-review (uncommitted).** Working-tree counts (84/85, 9/9) differ from the commit's. Use archives for every count you cite.
- **Mutants that survive a green suite here:** dropping the class term in amount matching (test gap; golden counts identical, so the rate-vs-charge blind spot is real), dropping the tolerated term, lowering CAL_SMALL_N to 5 (the boundary test uses 30 names, never 29), and dropping the record_warning filter before zip (positional alignment, untested).
- **AC closed with an unbuilt clause.** Card AC 1 said "UI shows ..." and was done:true with "UI line pending frontend". Check for any route/UI reference (grep app/) before accepting an AC that names the UI.
- **Sentence without provenance.** The generated sentence the UI would show verbatim named N/M and a case count, not the backend. A fixture replay read as live precision. Check the rendered sentence, not only the file's top-level fields.

**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.

T-090 r2 (commits 823b718 code, 02ff244 file; review reviews/T-090-staff-engineer-r2.md): fail, 1 blocker, 2 majors, 2 minors.
- **A later commit reverted the fix.** 2fca530 (another card, committed 15 s after 823b718, before 02ff244) deleted git_source and the 11 r2 tests. HEAD evals/ and test file == 02ff244. Project-tree "84 passed" was uncommitted. Always check `git diff --quiet <fix> HEAD -- <files>` and `git log --oneline <fix>..HEAD -- <files>` before accepting a fix commit as shipped.
- **Skip is a silent pass for a forged header.** Provenance tests skip on "no git history" and on "commit not available", so a source_commit naming a non-existent commit reports 2 skipped and no failure. Skips must be scoped to "no .git"; a missing cited commit must fail.
- **check-fresh validates sums and hashes only.** An edited served sentence returns 0 from check_fresh; only the pytest regeneration test catches it.
- **Scratch method that worked:** clone, detached checkout of the commit, regenerate with `python -I` plus sys.path insert and runpy, compare ignoring generated_at, then mutate the clone's file and run the selector per mutant. Restore by copying a saved pristine file (not git checkout).
- Narrowing an AC to "UI is under T-096" left the backend serve route with no AC anywhere (grep for the route name in the owning card).

Related: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:16.146Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD=$(git rev-parse HEAD)\" && git rev-parse --is-inside-work-tree && for c in 823b718 02ff244 2fca530 865b186 b85fc1b 172028c; do printf \"%s ancestor_of_HEAD=\" $c; git merge-base --is-ancestor $c HEAD && echo yes || echo no; done && echo \"--- log of r2 files since 02ff244\" && git log --oneline 02ff244..HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json && echo \"--- diff r2 code vs HEAD for evals/run.py and test file\" && git diff --stat 823b718 HEAD -- evals/run.py tests/unit/test_eval_runner.py && echo \"--- 02ff244 file vs HEAD\" && git diff --stat 02ff244 HEAD -- evals/reports/calibration.json; echo \"--- worktree status\"; git status --short | head -30",
 "description": "Check ancestry of fix commits and diff r2 code against HEAD"
}
````

### User / tool · 2026-11-02T04:49:16.458Z

**tool result**
````
HEAD=172028cfcff1750fec094d9e567e9d870a8f7b8e
true
823b718 ancestor_of_HEAD=yes
02ff244 ancestor_of_HEAD=yes
2fca530 ancestor_of_HEAD=yes
865b186 ancestor_of_HEAD=yes
b85fc1b ancestor_of_HEAD=yes
172028c ancestor_of_HEAD=yes
--- log of r2 files since 02ff244
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
a850be0 fix: restore T-090 work reverted by 2fca530
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
--- diff r2 code vs HEAD for evals/run.py and test file
 evals/run.py                   | 189 ++++++++++++++++++++++++++++++-----------
 tests/unit/test_eval_runner.py |  61 ++++++++++---
 2 files changed, 186 insertions(+), 64 deletions(-)
--- 02ff244 file vs HEAD
 evals/reports/calibration.json | 7 +++++--
 1 file changed, 5 insertions(+), 2 deletions(-)
--- worktree status
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
MM .claude/agent-memory/qa/MEMORY.md
D  .claude/agent-memory/qa/project_judge_controls.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/confidence.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/backend/reclassify.py
MM app/backend/rejudge.py
 M app/backend/review.py
 M app/backend/trace.py
MM app/db/db.py
MM app/db/schema.sql
MM app/llm/audited.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:19.023Z

**tool call — Bash**
````
{
 "command": "git show b85fc1b -- evals/run.py tests/unit/test_eval_runner.py",
 "description": "Show full diff of the r3 code commit"
}
````

### User / tool · 2026-11-02T04:49:19.124Z

**tool result**
````
commit b85fc1b56386aa0d37460186b5840eec0e578642
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:48:24 2026 -0600

    fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index 981b70b..47b0807 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -71,9 +71,10 @@ def git_source(root=ROOT):
     try:
         head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
         dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
-        return {"commit": head, "clean": not dirty}
+        tree = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
+        return {"commit": head, "clean": not dirty, "tree": tree}
     except Exception:
-        return {"commit": None, "clean": None}
+        return {"commit": None, "clean": None, "tree": None}
 
 
 def sha256_file(p):
@@ -283,33 +284,11 @@ def score_calibration(exp, out, unscored=None):
     return tally
 
 
-def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
-    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
-    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
-    names = list(results)
-    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
-    for n, r in results.items():
-        for t in CAL_TYPES:
-            for s in CAL_STATES:
-                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
-                c = cells[t][s]
-                c["matched"] += m
-                c["total"] += tot
-                if tot:
-                    c["by_case"][n] = [m, tot]
-    by_state = {}
-    for s in CAL_STATES:
-        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
-        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
-        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
-        by_state[s] = {"matched": m, "total": tot, "cases": cs}
-    small_cases = len(names) < CAL_SMALL_N
-    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
-    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)
-
+def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
+    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
     def caveat(total):
         """Names the backend and what was run, so the sentence cannot be read as live-model precision when it is a replay (T-090 r2)."""
-        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{len(names)} golden cases"]
+        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
         if small_cases:
             parts.append("small sample")
         elif total < CAL_SMALL_N:
@@ -333,9 +312,37 @@ def build_calibration(results, backend, models=None, generated_at=None, source=N
             sentences["by_type"][t][s] = (f"{('Verified' if s == 'verified' else 'Needs-review')} {noun[t]} matched the record {c['matched']}/{c['total']} "
                                           f"times in testing{caveat(c['total'])}." if c["total"] else
                                           f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
+    return sentences
+
+
+def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
+    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
+    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
+    names = list(results)
+    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
+    for n, r in results.items():
+        for t in CAL_TYPES:
+            for s in CAL_STATES:
+                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
+                c = cells[t][s]
+                c["matched"] += m
+                c["total"] += tot
+                if tot:
+                    c["by_case"][n] = [m, tot]
+    by_state = {}
+    for s in CAL_STATES:
+        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
+        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
+        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
+        by_state[s] = {"matched": m, "total": tot, "cases": cs}
+    small_cases = len(names) < CAL_SMALL_N
+    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
+    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)
+
+    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
     return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
             "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
-            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "hashes": hashes_ or {},
+            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
             "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
                           "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
                           "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
@@ -1031,6 +1038,8 @@ def check_calibration(path, root=ROOT):
         for k in ("matched", "total"):
             if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                 bad.append(f"by_state.{s}.{k} is not the sum of by_type")
+    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
+        bad.append("sentences do not match the counts they are built from")
     old = c.get("hashes") or {}
     now = hashes(root)
     bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index ebc9d1a..d21a423 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -626,25 +626,49 @@ def _committed():
     return json.loads(CAL.read_text())
 
 
+def _has_git():
+    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0
+
+
+def _require_source_commit(c):
+    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
+    if not _has_git():
+        pytest.skip("no git repository here (exported tree)")
+    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
+    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"
+
+
 def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
     c = _committed()
     assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
-    assert c["source_tree_clean"] is True and c["hashes"]
+    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")
 
 
-def test_committed_calibration_source_commit_is_an_ancestor_of_head():
+def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
     c = _committed()
-    if _git("rev-parse", "--git-dir").returncode or _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode:
-        pytest.skip("no git history here (shallow or exported tree)")
-    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0
+    _require_source_commit(c)
+    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
+    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"
+
+
+def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
+    c = _committed()
+    c["source_commit"] = "1" * 40
+    forged = tmp_path / "calibration.json"
+    forged.write_text(json.dumps(c))
+    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
+    if not _has_git():
+        pytest.skip("no git repository here")
+    with pytest.raises(AssertionError, match="does not exist"):
+        _require_source_commit(_committed())
 
 
 def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
     """T-090 r2 blocker: the shipped counts must come from the code of the commit named in the header. Export that commit
-    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at."""
+    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at and the git-derived fields
+    (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
     c = _committed()
-    if _git("rev-parse", "--git-dir").returncode or _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode:
-        pytest.skip("source commit not available in this checkout")
+    _require_source_commit(c)
     src = tmp_path / "src"
     src.mkdir()
     tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
@@ -655,11 +679,10 @@ def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_pa
     r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
     assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
     fresh = json.loads((out / "calibration.json").read_text())
-    for d in (fresh, c):
-        d.pop("generated_at")
-    fresh["source_tree_clean"] = c["source_tree_clean"]                        # the export has no .git, so it cannot attest cleanliness itself
+    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
     assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
-    assert {k: v for k, v in fresh.items() if k != "source_commit"} == {k: v for k, v in c.items() if k != "source_commit"}
+    assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
+    assert c["source_tree_clean"] is True
 
 
 def test_git_source_reports_commit_and_dirtiness(tmp_path):
@@ -674,7 +697,8 @@ def test_git_source_reports_commit_and_dirtiness(tmp_path):
     assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
     (tmp_path / "f").write_text("b")
     assert R.git_source(tmp_path)["clean"] is False
-    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None}
+    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
+    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None}
 
 
 def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
@@ -693,3 +717,14 @@ def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(
     cal["hashes"][k] = "0" * 64
     (tmp_path / "calibration.json").write_text(json.dumps(cal))
     assert R.check_fresh(rep) == 1
+
+
+def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
+    rep = tmp_path / "latest.json"
+    rep.write_text(json.dumps({"hashes": R.hashes()}))
+    cal = _committed()
+    cal["hashes"] = R.hashes()
+    cal["sentences"]["overall"]["verified"] = cal["sentences"]["overall"]["verified"].replace(
+        f"{cal['by_state']['verified']['matched']}/", f"{cal['by_state']['verified']['total']}/", 1)
+    (tmp_path / "calibration.json").write_text(json.dumps(cal))
+    assert R.check_fresh(rep) == 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:19.710Z

**tool call — Bash**
````
{
 "command": "git show 172028c && echo \"=== a850be0 stat\" && git show --stat a850be0 | head -20 && echo \"=== 2fca530 stat\" && git show --stat 2fca530 | head -20",
 "description": "Show the calibration regeneration commit and the restore commit stats"
}
````

### User / tool · 2026-11-02T04:49:19.861Z

**tool result**
````
commit 172028cfcff1750fec094d9e567e9d870a8f7b8e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:48:52 2026 -0600

    chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/reports/calibration.json b/evals/reports/calibration.json
index 0d3ffea..d1bdb36 100644
--- a/evals/reports/calibration.json
+++ b/evals/reports/calibration.json
@@ -210,15 +210,17 @@
   "case_08_diagnosis_temptation",
   "case_09_nonvisit_hides_gap"
  ],
- "generated_at": "2026-11-02T04:31:09Z",
+ "generated_at": "2026-11-02T04:48:31Z",
  "hashes": {
   "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
   "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca",
+  "app/llm/prompts/extract_es_v1.md": "985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb",
   "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
   "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
   "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
   "app/llm/prompts/judge_conflict_v1.md": "10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa",
   "app/llm/prompts/judge_conflict_v2.md": "6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6",
+  "app/llm/prompts/judge_faithfulness_es_v1.md": "d51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898",
   "app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b",
   "app/llm/prompts/judge_flag_v1.md": "97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432",
   "app/llm/prompts/judge_flag_v2.md": "7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe",
@@ -259,6 +261,7 @@
  },
  "small_sample": true,
  "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
- "source_commit": "823b718817cacf6d38cf179724fd374ad09dffdf",
+ "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642",
+ "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f",
  "source_tree_clean": true
 }
=== a850be0 stat
commit a850be05b5fafe1c5e95e8a4294508403aa77438
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:42:02 2026 -0600

    fix: restore T-090 work reverted by 2fca530
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/run.py                   |  88 ++++++++++++++++-----
 tests/unit/test_eval_runner.py | 170 ++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 237 insertions(+), 21 deletions(-)
=== 2fca530 stat
commit 2fca530363a43f5e886a441234ba2cfc7a6725ea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:03 2026 -0600

    feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
    
    Hidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page
    (pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd
    locally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at
    needs_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py                   |  26 +++--
 app/backend/confidence.py            |   2 +-
 app/backend/pdf_checks.py            | 125 +++++++++++++++++++++++
 app/backend/pdf_hidden.py            | 188 +++++++++++++++++++++++++++++++++++
 app/backend/pdf_ocr.py               | 178 +++++++++++++++++++++++++++++++++
 app/backend/pdf_routes.py            |  25 +++++
 app/backend/pdf_text.py              |  41 ++++++--
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:48.527Z

**tool call — Bash**
````
{
 "command": "echo \"== project-tree diff vs HEAD for the two files\" && git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json; echo \"exit=$?\"; echo \"== HEAD greps\" && git show HEAD:evals/run.py | grep -n \"def git_source\\|def calibration_sentences\\|def check_calibration\\|def check_fresh\\|source_tree\\|not_scored\\[\" ; echo \"== HEAD test greps\" && git show HEAD:tests/unit/test_eval_runner.py | grep -n \"^def \\|skip(\" | sed -n '1,200p' | grep -n \"calib\\|git\\|forged\\|skip\\|regen\\|fresh\"; echo \"== trees\"; git rev-parse b85fc1b^{tree} 172028c^{tree}; echo \"== committed header\"; python3 -c \"import json;c=json.load(open('evals/reports/calibration.json'));print({k:c[k] for k in ['backend','source_commit','source_tree','source_tree_clean','generated_at','case_count','small_sample'] if k in c}); print(c['sentences'])\"",
 "description": "Check HEAD contents, tree hashes and committed calibration header"
}
````

### User / tool · 2026-11-02T04:49:48.734Z

**tool result**
````
== project-tree diff vs HEAD for the two files
exit=0
== HEAD greps
67:def git_source(root=ROOT):
287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
305:        if b["total"] and not_scored["total"]:
306:            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
340:    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)
345:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
1013:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1029:def check_calibration(path, root=ROOT):
== HEAD test greps
26:272:def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
42:444:def test_score_calibration_counts_matched_over_seen_per_state_and_type():
43:459:def test_score_calibration_ignores_rejected_items_and_items_without_a_state():
44:469:def test_flag_calibration_follows_flag_precision():
45:480:def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
46:495:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
55:606:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
56:621:def _git(*a, cwd=None):
58:629:def _has_git():
60:636:        pytest.skip("no git repository here (exported tree)")
61:641:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
62:647:def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
63:654:def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
64:661:        pytest.skip("no git repository here")
65:666:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
66:688:def test_git_source_reports_commit_and_dirtiness(tmp_path):
67:690:        pytest.skip("git missing")
68:704:def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
69:722:def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
== trees
3f014d4b5d84f8731ff464d4548e18dfce3fbd4f
a208c48b85483f09b28b7f8d918baac18f56378b
== committed header
{'backend': 'fixture', 'source_commit': 'b85fc1b56386aa0d37460186b5840eec0e578642', 'source_tree': '3f014d4b5d84f8731ff464d4548e18dfce3fbd4f', 'source_tree_clean': True, 'generated_at': '2026-11-02T04:48:31Z', 'case_count': 10, 'small_sample': True}
{'by_type': {'amount': {'needs_review': 'Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}, 'entry': {'needs_review': 'Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}, 'flag': {'needs_review': 'Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}}, 'overall': {'needs_review': 'Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:49.176Z

**tool call — Bash**
````
{
 "command": "ls .venv/bin/python && .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -25",
 "description": "Run the brief's calibration and eval_runner pytest selector in project tree",
 "timeout": 900000
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:49.847Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-090 2>&1 | head -80; echo \"=========== T-096\"; python3 tools/board.py show T-096 2>&1 | head -80; echo \"=========== grep app\"; grep -rln calibration app/ ; echo \"grep exit=$?\"",
 "description": "Show T-090 and T-096 cards and grep app for calibration route"
}
````

### User / tool · 2026-11-02T04:49:57.041Z

**tool result**
````
.venv/bin/python
........................................................................ [ 83%]
..............                                                           [100%]
86 passed, 1372 deselected in 7.39s
````

### User / tool · 2026-11-02T04:49:57.243Z

**tool result**
````
---
id: "T-090"
title: "Calibrated confidence: measured precision per state from evals"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:49:05Z"
claimed_by: "qa"
claimed_at: "2026-11-02T04:39:56Z"
rounds: 2
commits: ["d0aee83", "02ff244", "823b718", "b85fc1b", "172028c"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-090-staff-engineer.md", "at": "2026-11-02T04:27:39Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-090-staff-engineer-r2.md", "at": "2026-11-02T04:39:56Z"}
ac:
  - {"n": 1, "text": "evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)", "done": true, "evidence": "calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z qa: claimed
- 2026-11-02T04:19:52Z qa: AC 1 checked: evals/run.py score_calibration/build_calibration; evals/reports/calibration.json (fixture backend: verified 82/83, needs_review 11/13, 10 golden cases, small-sample caveat); tests/unit/test_eval_runner.py 6 new tests incl. no-percent check; eval-suite tests 126 pass. UI line pending frontend (note).
- 2026-11-02T04:19:52Z qa: FOR BACKEND: serve evals/reports/calibration.json (regenerated by every full 'python -m evals.run'; keys: backend, case_count, small_sample, by_state{verified,needs_review:{matched,total,cases}}, by_type{entry|amount|flag:{state:{matched,total,by_case}}}, sentences{overall,by_type}) as a read-only 'calibration' field (e.g. GET /api/meta or /api/calibration; null when the file is absent). FOR FRONTEND: render sentences.overall.verified verbatim (it reads 'Verified items matched the record N/M times in testing (small sample: 10 cases).'); never compute or show a %. Show backend name (fixture = recorded model replies) beside it. Numbers shipped now are from the FIXTURE backend; a live run overwrites the file with its own backend field.
- 2026-11-02T04:19:52Z qa: moved in_progress -> in_review
- 2026-11-02T04:19:58Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:27:39Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-090-staff-engineer.md; round 1; findings:
    - [blocker] Committed calibration.json does not reproduce from the commit and has no traceable run — fix: Regenerate calibration.json with a full python -m evals.run at the commit being shipped (fixture backend) and commit it with its report .md and latest.json in the same commit. Do not hand-place or copy the file. Update the card evidence to the regenerated counts (83/84 and 10/10 at d0aee83
    - [major] AC 1 is marked done while its UI clause is unbuilt — fix: Set AC 1 to done: false, or split it: AC 1a (eval counts, done) and AC 1b (served read-only calibration field and UI line rendered verbatim, no percent), with 1b linked to the frontend and backend cards that will build it.
    - [major] Amount matching ignores class in no test; mutant survives and golden counts do not change — fix: Keep the class term and add a unit test in tests/unit/test_eval_runner.py: in the sample, change the kind of one verified amount (for example $6,240 charge to rate) and assert that the verified amount count falls from 2/2 to 1/2 for the sample.
    - [major] The sentence the UI will render verbatim names no backend and no provenance — fix: Put the backend and the golden-set basis into the sentence, for example 'Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases).' Build it in build_calibration so the UI cannot drop it.
    - [minor] Small-sample threshold boundary at 29 cases is not tested; lowering CAL_SMALL_N to 5 survives — fix: Add the 29-case assertion beside the 30-case one: at 29 cases the overall sentence carries 'small sample'; at 30 it does not.
    - [minor] Tolerated-flag and record_warning alignment mutants survive — fix: Add a test with one tolerated candidate (expect it counted as matched) and one case with a record_warning placed before a flag (expect the states to stay aligned). Prefer matching by candidate identity over zip position.
    - [minor] Items are dropped from the denominator silently — fix: Count the excluded items per cell and print them beside the sentence ('N items not scored'); or state in the sentence that the count covers produced items only.
    - [minor] calibration.json is outside the freshness check and embeds a wall-clock timestamp — fix: Add the calibration.json hash to the check-fresh comparison, and either drop generated_at from the served file or exclude it from the hash.
- 2026-11-02T04:27:39Z qa: claimed
- 2026-11-02T04:31:37Z qa: AC 1 edited: evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)
- 2026-11-02T04:31:37Z qa: AC 1 checked: evals/reports/calibration.json generated from a clean worktree of 823b718 (source_commit, source_tree_clean=true, backend=fixture in header): verified 83/84, needs_review 10/10; tests/unit/test_eval_runner.py regenerates it from git archive of source_commit and compares; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed
- 2026-11-02T04:31:37Z qa: r2: commits 823b718 (code, tests) and 02ff244 (calibration.json from clean worktree 823b718, worktree removed). Blocker: header has source_commit, source_tree_clean, backend, hashes; tests: ancestor-of-HEAD, regenerate-from-source-commit equality, check-fresh fails on edited count/changed hashes. Major 2: AC 1 narrowed to the eval side, served field + UI line is T-096. Major 3: amount class test. Major 4: sentences name backend + golden set (+ 'recorded replies' for fixture). Minors: 29/30 boundary, tolerated flag, record_warning alignment (state now travels with the candidate, no zip), not_scored counts, check-fresh covers calibration.json. Nit: 7 tests originally, not 6; selector now gives 84. generated_at kept in file (test ignores it). Not done: latest.json/.md not regenerated (latest.json is the live claude-cli report). FOR FRONTEND T-096: sentences now end with backend+basis already, render verbatim.
- 2026-11-02T04:31:37Z qa: moved in_progress -> in_review
- 2026-11-02T04:31:43Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:39:56Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-090-staff-engineer-r2.md; round 2; findings:
    - [blocker] The r2 provenance fix and its tests are reverted at HEAD by commit 2fca530; the card's test evidence is not reproducible from HEAD — fix: Restore the 823b718 versions of evals/run.py and tests/unit/test_eval_runner.py in a new commit that stages those two paths explicitly (git show 823b718:evals/run.py and :tests/unit/test_eval_runner.py are the reference). Do not hand-merge the un
    - [major] A forged source_commit that names no existing commit passes the two provenance tests by skipping — fix: Skip only when there is no git repository (git rev-parse --git-dir fails). When a repository exists and the cited commit is missing, or the commit is not an ancestor of HEAD, fail with the commit name.
    - [major] The served calibration field has no owner after AC 1 was narrowed — fix: Add an explicit backend AC (route that returns the calibration.json fields, or null when the file is absent, read-only) to an existing backend card or a new one, and name it in T-090 AC 1 or the T-096 AC.
    - [minor] check-fresh exits 0 for an edited sentence; it validates sums and hashes only — fix: Add the calibration.json sentences and not_scored to check_calibration, or regenerate the sentences inside check_calibration from by_state and by_type and compare.
    - [minor] The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes — fix: Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.
- 2026-11-02T04:39:56Z qa: claimed
- 2026-11-02T04:39:56Z orchestrator: r2 blocker (code reverted by 2fca530) is being restored by the revert audit; r3 then fixes the forged source_commit skip and moves the served field to T-096 (backend serve + UI).
- 2026-11-02T04:39:56Z orchestrator: assigned: qa
- 2026-11-02T04:46:29Z backend: Round-2 work reverted by 2fca530 (evals/run.py, test_eval_runner.py) restored in a850be0. See artifacts/review-evidence/revert-audit.md
- 2026-11-02T04:48:59Z qa: AC 1 checked: calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)
- 2026-11-02T04:48:59Z qa: moved in_progress -> in_review
- 2026-11-02T04:49:05Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
r3. Changed: r2 code confirmed in HEAD (a850be0); provenance tests now fail (not skip) on a missing or non-ancestor source_commit when a git repo exists, skip only with no repo; source_tree recorded and checked against git (replaces copying the clean flag); check_calibration rebuilds sentences from counts (calibration_sentences) so edited sentences fail check-fresh; calibration.json regenerated from a clean worktree of b85fc1b (83/84, 10/10), worktree removed. Verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; forged source_commit mutant fails 2 tests. Left: served field + UI line on T-096 (note with field shape posted). Surprise: shared tree's calibration.json had been overwritten by another run without provenance.

=========== T-096
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
updated_at: "2026-11-02T04:48:59Z"
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
- 2026-11-02T04:48:59Z qa: From T-090 (qa): serve evals/reports/calibration.json read-only as a 'calibration' field (backend: e.g. in GET /api/meta; null when the file is absent). Shape: {schema:'evals.calibration/1', backend:'fixture'|..., case_count:int, small_sample:bool, source_commit:str, by_state:{verified|needs_review:{matched:int,total:int,cases:[str]}}, by_type:{entry|amount|flag:{verified|needs_review:{matched,total,by_case:{case:[m,t]}}}}, not_scored:{entry,amount,flag,total}, sentences:{overall:{verified:str,needs_review:str}, by_type:{entry|amount|flag:{verified:str,needs_review:str}}}}. Frontend: render sentences.overall.verified verbatim (it already names backend and basis, e.g. 'Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'); never compute or show a percentage. Backend AC needed: route returns those fields, null if file absent, no write path; test it. Frontend AC: line shown, hidden when null.

## Handoff (filled when moving to in_review)

=========== grep app
grep exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:16.848Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/unit/test_eval_runner.py | sed -n '1,30p' | grep -n \"import\\|^R\\|CAL\\|ROOT\" ; echo ---; git show HEAD:tests/unit/test_eval_runner.py | sed -n '621,700p'; echo \"--- run.py 1013-1050\"; git show HEAD:evals/run.py | sed -n '1013,1050p'; echo \"--- run.py ROOT/CAL\"; git show HEAD:evals/run.py | grep -n \"^ROOT\\|^REPORTS\\|^CAL_SMALL_N\\|^def hashes\" ",
 "description": "Read HEAD test helpers, regeneration test, and check_fresh code"
}
````

### User / tool · 2026-11-02T04:50:17.017Z

**tool result**
````
3:import copy, json, re
4:import pytest
5:from evals import run as R
6:from tests.unit import _golden as G
12:REC = re.compile(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n')
---
def _git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)


def _committed():
    return json.loads(CAL.read_text())


def _has_git():
    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0


def _require_source_commit(c):
    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
    if not _has_git():
        pytest.skip("no git repository here (exported tree)")
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    c = _committed()
    assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")


def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
    c = _committed()
    _require_source_commit(c)
    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"


def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
    c = _committed()
    c["source_commit"] = "1" * 40
    forged = tmp_path / "calibration.json"
    forged.write_text(json.dumps(c))
    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
    if not _has_git():
        pytest.skip("no git repository here")
    with pytest.raises(AssertionError, match="does not exist"):
        _require_source_commit(_committed())


def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
    """T-090 r2 blocker: the shipped counts must come from the code of the commit named in the header. Export that commit
    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at and the git-derived fields
    (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
    c = _committed()
    _require_source_commit(c)
    src = tmp_path / "src"
    src.mkdir()
    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
    assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
    fresh = json.loads((out / "calibration.json").read_text())
    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
    assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
    assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
    assert c["source_tree_clean"] is True


def test_git_source_reports_commit_and_dirtiness(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git missing")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "f").write_text("a")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
    a = R.git_source(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
    (tmp_path / "f").write_text("b")
    assert R.git_source(tmp_path)["clean"] is False
    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
--- run.py 1013-1050
def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
    p = pathlib.Path(latest_path)
    if not p.exists():
        print("check-fresh: no latest.json", file=sys.stderr)
        return 1
    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
    for k in diff:
        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
    bad = check_calibration(p.parent / "calibration.json", root)
    for m in bad:
        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
    return 1 if diff or bad else 0


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad


def load_pipeline():
    from app import pipeline
--- run.py ROOT/CAL
28:ROOT = pathlib.Path(__file__).resolve().parents[1]
30:REPORTS = ROOT / "evals" / "reports"
84:def hashes(root=ROOT):
244:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:17.700Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json\nc=json.load(open('evals/reports/calibration.json'))\nprint(\"top keys:\", sorted(c.keys()))\nprint(\"by_state:\", json.dumps(c['by_state'])[:400])\nprint(\"by_type entry verified:\", json.dumps(c['by_type']['entry']['verified']))\nprint(\"not_scored:\", c['not_scored'])\nprint(\"case_count:\", c['case_count'], \"small_sample:\", c['small_sample'])\nEOF",
 "description": "Dump calibration.json top-level keys and served shape"
}
````

### User / tool · 2026-11-02T04:50:17.799Z

**tool result**
````
top keys: ['backend', 'by_state', 'by_type', 'case_count', 'cases', 'generated_at', 'hashes', 'match_rule', 'models', 'not_scored', 'schema', 'sentences', 'small_sample', 'source', 'source_commit', 'source_tree', 'source_tree_clean']
by_state: {"needs_review": {"cases": ["case_01_date_formats", "case_03_rate_and_ocr", "case_06_subtle_pre_existing", "case_07_prompt_injection", "sample"], "matched": 10, "total": 10}, "verified": {"cases": ["case_01_date_formats", "case_02_gap_boundaries", "case_03_rate_and_ocr", "case_04_duplicates_no_amounts", "case_05_provider_conflict", "case_06_subtle_pre_existing", "case_07_prompt_injection", "case_0
by_type entry verified: {"by_case": {"case_01_date_formats": [7, 7], "case_02_gap_boundaries": [8, 8], "case_03_rate_and_ocr": [5, 5], "case_04_duplicates_no_amounts": [4, 4], "case_05_provider_conflict": [5, 5], "case_06_subtle_pre_existing": [4, 5], "case_07_prompt_injection": [3, 3], "case_08_diagnosis_temptation": [4, 4], "case_09_nonvisit_hides_gap": [5, 5], "sample": [9, 9]}, "matched": 54, "total": 55}
not_scored: {'amount': 0, 'entry': 0, 'flag': 0, 'total': 0}
case_count: 10 small_sample: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:32.374Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nmkdir -p \"$S/t090r3\" && cd \"$S/t090r3\" && rm -rf clone archive-b85 && git clone -q --no-hardlinks /Users/arsis/zlayt-pm-project clone && git -C clone checkout -q --detach 172028cfcff1750fec094d9e567e9d870a8f7b8e && echo \"clone HEAD=$(git -C clone rev-parse HEAD)\" && mkdir archive-b85 && git -C /Users/arsis/zlayt-pm-project archive b85fc1b | tar -x -C archive-b85 && echo \"archive files: $(find archive-b85 -type f | wc -l)\" && ls -la archive-b85 | head -5 && cd clone && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import evals.run as R, sys; print('R.ROOT=', R.ROOT)\" && ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -5",
 "description": "Create scratch clone at HEAD and git archive of b85fc1b, run selector in clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:50:41.813Z

**tool result**
````
clone HEAD=172028cfcff1750fec094d9e567e9d870a8f7b8e
archive files:     1794
total 208
drwxr-xr-x@  21 arsis  wheel    672 Nov  1 22:50 .
drwxr-xr-x@   4 arsis  wheel    128 Nov  1 22:50 ..
drwxr-xr-x@   7 arsis  wheel    224 Nov  1 22:48 .claude
-rw-r--r--@   1 arsis  wheel    403 Nov  1 22:48 .gitignore
R.ROOT= /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3/clone
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
........................................................................ [ 83%]
..............                                                           [100%]
86 passed, 1346 deselected in 7.04s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:48.126Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\ncd \"$S\" && for run in 1 2; do rm -rf \"$S/t090r3/out$run\"; env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=\"$HOME\" \"$PY\" -I -c \"import sys,runpy; sys.path.insert(0,'$S/t090r3/archive-b85'); sys.argv=['evals.run','--out','$S/t090r3/out$run']; import os; os.chdir('$S/t090r3/archive-b85'); runpy.run_module('evals.run', run_name='__main__')\" > \"$S/t090r3/regen$run.log\" 2>&1; echo \"run$run exit=$?\"; done\nls \"$S/t090r3/out1\" \"$S/t090r3/out2\"\necho \"== compare committed vs regen (ignoring generated_at, source_commit, source_tree_clean, source_tree)\"\n\"$PY\" -I - \"$S/t090r3\" <<'EOF'\nimport json, sys, pathlib\nbase = pathlib.Path(sys.argv[1])\ncommitted = json.load(open('/Users/arsis/zlayt-pm-project/evals/reports/calibration.json'))\ngit_fields = (\"generated_at\",\"source_commit\",\"source_tree_clean\",\"source_tree\")\nfor run in (1,2):\n    f = json.load(open(base/f'out{run}'/'calibration.json'))\n    print(f\"run{run}: keys_equal={sorted(f)==sorted(committed)}\")\n    print(f\"run{run}: by_state==, by_type==, sentences== :\", f['by_state']==committed['by_state'], f['by_type']==committed['by_type'], f['sentences']==committed['sentences'])\n    print(f\"run{run}: hashes==\", f['hashes']==committed['hashes'], \" not_scored==\", f['not_scored']==committed['not_scored'])\n    a={k:v for k,v in f.items() if k not in git_fields}; b={k:v for k,v in committed.items() if k not in git_fields}\n    print(f\"run{run}: all non-git fields equal:\", a==b)\n    print(f\"run{run}: regen source_commit={f['source_commit']} source_tree={f['source_tree']} clean={f['source_tree_clean']}\")\n    print(f\"run{run}: sentences overall verified:\", f['sentences']['overall']['verified'])\n    print(f\"run{run}: committed generated_at={committed['generated_at']} regen generated_at={f['generated_at']}\")\nEOF\necho \"== byte compare regen1 vs regen2 ignoring generated_at\"\ndiff <(grep -v generated_at \"$S/t090r3/out1/calibration.json\") <(grep -v generated_at \"$S/t090r3/out2/calibration.json\") && echo \"run1 == run2 byte-identical except generated_at\"\necho \"== byte compare committed vs regen1 ignoring generated_at, source_commit, source_tree, source_tree_clean\"\ndiff <(grep -v 'generated_at\\|source_commit\\|source_tree\\|\"source_tree_clean\"' /Users/arsis/zlayt-pm-project/evals/reports/calibration.json) <(grep -v 'generated_at\\|source_commit\\|source_tree\\|\"source_tree_clean\"' \"$S/t090r3/out1/calibration.json\") && echo \"committed == regen1 except git fields\"\necho \"== regen log tail\"; tail -3 \"$S/t090r3/regen1.log\"",
 "description": "Regenerate calibration.json from git archive of b85fc1b twice and compare",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:50:48.244Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:51.936Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nls \"$B\"\ncd \"$B\" && env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=\"$HOME\" \"$PY\" -I -c \"import sys,runpy,os; sys.path.insert(0,'$B/archive-b85'); os.chdir('$B/archive-b85'); sys.argv=['evals.run','--out','$B/out1']; runpy.run_module('evals.run', run_name='__main__')\" > \"$B/regen1.log\" 2>&1; echo \"run1 exit=$?\"\nenv -i PATH=/usr/bin:/bin:/usr/local/bin HOME=\"$HOME\" \"$PY\" -I -c \"import sys,runpy,os; sys.path.insert(0,'$B/archive-b85'); os.chdir('$B/archive-b85'); sys.argv=['evals.run','--out','$B/out2']; runpy.run_module('evals.run', run_name='__main__')\" > \"$B/regen2.log\" 2>&1; echo \"run2 exit=$?\"\nls \"$B/out1\" \"$B/out2\"; tail -3 \"$B/regen1.log\"",
 "description": "Regenerate calibration.json from git archive of b85fc1b twice",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:50:54.279Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:59.428Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\n\"$PY\" -I - \"$B\" <<'EOF'\nimport json, sys, pathlib\nbase = pathlib.Path(sys.argv[1])\ncommitted = json.load(open('/Users/arsis/zlayt-pm-project/evals/reports/calibration.json'))\ngit_fields = (\"generated_at\",\"source_commit\",\"source_tree_clean\",\"source_tree\")\nfor run in (1,2):\n    f = json.load(open(base/f'out{run}'/'calibration.json'))\n    print(f\"run{run}: keys_equal={sorted(f)==sorted(committed)}\")\n    print(f\"run{run}: by_state==, by_type==, sentences==:\", f['by_state']==committed['by_state'], f['by_type']==committed['by_type'], f['sentences']==committed['sentences'])\n    print(f\"run{run}: hashes==\", f['hashes']==committed['hashes'], \" not_scored==\", f['not_scored']==committed['not_scored'])\n    a={k:v for k,v in f.items() if k not in git_fields}; b={k:v for k,v in committed.items() if k not in git_fields}\n    print(f\"run{run}: all non-git fields equal:\", a==b)\n    print(f\"run{run}: regen source_commit={f['source_commit']} source_tree={f['source_tree']} clean={f['source_tree_clean']}\")\n    print(f\"run{run}: committed generated_at={committed['generated_at']} regen generated_at={f['generated_at']}\")\nprint(\"regen overall verified:\", json.load(open(base/'out1'/'calibration.json'))['sentences']['overall']['verified'])\nEOF\necho \"== run1 vs run2 ignoring generated_at\"\ndiff <(grep -v generated_at \"$B/out1/calibration.json\") <(grep -v generated_at \"$B/out2/calibration.json\") && echo \"IDENTICAL\"\necho \"== committed vs regen1 ignoring git fields\"\ndiff <(grep -v 'generated_at\\|\"source_commit\"\\|\"source_tree\"\\|\"source_tree_clean\"' /Users/arsis/zlayt-pm-project/evals/reports/calibration.json) <(grep -v 'generated_at\\|\"source_commit\"\\|\"source_tree\"\\|\"source_tree_clean\"' \"$B/out1/calibration.json\") && echo \"IDENTICAL except git fields\"\necho \"== percent signs in committed\"; grep -c '%' /Users/arsis/zlayt-pm-project/evals/reports/calibration.json\necho \"== tree hash of b85fc1b vs header\"; git -C /Users/arsis/zlayt-pm-project rev-parse b85fc1b^{tree}",
 "description": "Compare regenerated calibration.json with committed file"
}
````

### User / tool · 2026-11-02T04:50:59.590Z

**tool result**
````
run1: keys_equal=True
run1: by_state==, by_type==, sentences==: True True True
run1: hashes== True  not_scored== True
run1: all non-git fields equal: True
run1: regen source_commit=None source_tree=None clean=None
run1: committed generated_at=2026-11-02T04:48:31Z regen generated_at=2026-11-02T04:50:53Z
run2: keys_equal=True
run2: by_state==, by_type==, sentences==: True True True
run2: hashes== True  not_scored== True
run2: all non-git fields equal: True
run2: regen source_commit=None source_tree=None clean=None
run2: committed generated_at=2026-11-02T04:48:31Z regen generated_at=2026-11-02T04:50:54Z
regen overall verified: Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).
== run1 vs run2 ignoring generated_at
IDENTICAL
== committed vs regen1 ignoring git fields
IDENTICAL except git fields
== percent signs in committed
0
== tree hash of b85fc1b vs header
3f014d4b5d84f8731ff464d4548e18dfce3fbd4f
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:07.994Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nC=$B/clone\nmkdir -p \"$B/pristine\" && cp \"$C/evals/reports/calibration.json\" \"$B/pristine/calibration.json\" && cp \"$C/evals/run.py\" \"$B/pristine/run.py\" && cp \"$C/tests/unit/test_eval_runner.py\" \"$B/pristine/test_eval_runner.py\"\nNEWC=$(git -C \"$C\" commit-tree \"$(git -C \"$C\" rev-parse HEAD^{tree})\" -m \"orphan side commit, not an ancestor of HEAD\")\necho \"non-ancestor commit: $NEWC  is_ancestor=$(git -C \"$C\" merge-base --is-ancestor $NEWC HEAD && echo yes || echo no)\"\ncat > \"$B/mutate_cal.py\" <<'EOF'\nimport json, sys\npath, field, value = sys.argv[1], sys.argv[2], sys.argv[3]\nc = json.load(open(path))\nc[field] = value\njson.dump(c, open(path, \"w\"), indent=1)\nEOF\ncd \"$C\"\nrun() { echo \"== $1\"; \"$PY\" -m pytest -q -rs tests/unit -k \"calibration or eval_runner\" 2>&1 | grep -E \"passed|failed|SKIPPED|^FAILED\" | tail -8; cp \"$B/pristine/calibration.json\" \"$C/evals/reports/calibration.json\"; }\n\"$PY\" -I \"$B/mutate_cal.py\" \"$C/evals/reports/calibration.json\" source_commit \"$(printf '1%.0s' $(seq 40))\"; run \"M1 forged source_commit 1*40\"\n\"$PY\" -I \"$B/mutate_cal.py\" \"$C/evals/reports/calibration.json\" source_commit \"$NEWC\"; run \"M2 source_commit = unreferenced non-ancestor commit\"\n\"$PY\" -I \"$B/mutate_cal.py\" \"$C/evals/reports/calibration.json\" source_tree \"$(printf '0%.0s' $(seq 40))\"; run \"M3 source_tree forged 0*40\"\n\"$PY\" -I \"$B/mutate_cal.py\" \"$C/evals/reports/calibration.json\" source_commit \"$(printf '1%.0s' $(seq 40))\"; cp \"$B/pristine/calibration.json\" \"$C/evals/reports/calibration.json\"; cmp \"$C/evals/reports/calibration.json\" \"$B/pristine/calibration.json\" && echo \"restored pristine OK\"\necho \"== pristine selector again\"; \"$PY\" -m pytest -q -rs tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -2",
 "description": "Run forged and non-ancestor source_commit mutants in scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:51:08.064Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf807
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:12.291Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nmkdir -p \"$B/pristine\"\ncp \"$B/clone/evals/reports/calibration.json\" \"$B/pristine/calibration.json\"\ncp \"$B/clone/evals/run.py\" \"$B/pristine/run.py\"\ncp \"$B/clone/tests/unit/test_eval_runner.py\" \"$B/pristine/test_eval_runner.py\"\ncmp \"$B/clone/evals/run.py\" \"$B/pristine/run.py\" && echo \"pristine saved\"\nls \"$B/pristine\"",
 "description": "Save pristine copies of clone files for restore"
}
````

### User / tool · 2026-11-02T04:51:12.501Z

**tool result**
````
pristine saved
calibration.json
run.py
test_eval_runner.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:17.204Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\ncat > \"$B/mutants_cal.py\" <<'EOF'\nimport json, subprocess, shutil, sys, pathlib\nB = pathlib.Path(sys.argv[1]); C = B / \"clone\"; PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = C / \"evals/reports/calibration.json\"\nPRIST = B / \"pristine/calibration.json\"\ndef git(*a): return subprocess.run([\"git\", \"-C\", str(C), *a], capture_output=True, text=True)\norphan = git(\"commit-tree\", git(\"rev-parse\", \"HEAD^{tree}\").stdout.strip(), \"-m\", \"orphan, not an ancestor\").stdout.strip()\nprint(\"non-ancestor commit:\", orphan, \"is_ancestor_of_HEAD:\", git(\"merge-base\", \"--is-ancestor\", orphan, \"HEAD\").returncode == 0)\ndef pytest_run():\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rs\", \"tests/unit\", \"-k\", \"calibration or eval_runner\"], cwd=C, capture_output=True, text=True)\n    lines = [l for l in r.stdout.splitlines() if l.startswith((\"FAILED\", \"SKIPPED\")) or \" passed\" in l or \" failed\" in l]\n    return \"\\n      \".join(lines)\ndef mutate(name, field, value):\n    c = json.loads(PRIST.read_text()); c[field] = value\n    CAL.write_text(json.dumps(c, indent=1))\n    print(\"== \" + name)\n    print(\"      \" + pytest_run())\n    shutil.copyfile(PRIST, CAL)\nmutate(\"M1 forged source_commit 1*40\", \"source_commit\", \"1\" * 40)\nmutate(\"M2 source_commit = non-ancestor commit\", \"source_commit\", orphan)\nmutate(\"M3 source_tree forged 0*40\", \"source_tree\", \"0\" * 40)\nmutate(\"M4 source_commit = nonexistent but well-formed then restored\", \"source_commit\", \"2\" * 40)\nshutil.copyfile(PRIST, CAL)\nprint(\"== restored pristine:\", subprocess.run([\"cmp\", str(CAL), str(PRIST)]).returncode == 0)\nprint(\"== pristine selector:\", pytest_run())\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$B/mutants_cal.py\" \"$B\"",
 "description": "Run source_commit and source_tree forgery mutants in scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:51:52.850Z

**tool result**
````
non-ancestor commit: 2095c6de26596d6355dcb1c4452582f4ec74beb1 is_ancestor_of_HEAD: False
== M1 forged source_commit 1*40
      2 failed, 84 passed, 1346 deselected in 5.50s
== M2 source_commit = non-ancestor commit
      1 failed, 85 passed, 1346 deselected in 7.22s
== M3 source_tree forged 0*40
      1 failed, 85 passed, 1346 deselected in 7.45s
== M4 source_commit = nonexistent but well-formed then restored
      2 failed, 84 passed, 1346 deselected in 5.91s
== restored pristine: True
== pristine selector: 86 passed, 1346 deselected in 7.53s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:04.647Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\ncat > \"$B/mutants_code.py\" <<'EOF'\nimport json, subprocess, shutil, sys, pathlib\nB = pathlib.Path(sys.argv[1]); C = B / \"clone\"; PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = C / \"evals/reports/calibration.json\"; PRIST_CAL = B / \"pristine/calibration.json\"\nRUN = C / \"evals/run.py\"; PRIST_RUN = B / \"pristine/run.py\"\nTST = C / \"tests/unit/test_eval_runner.py\"; PRIST_TST = B / \"pristine/test_eval_runner.py\"\ndef pytest_run(extra=()):\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rfs\", \"tests/unit\", \"-k\", \"calibration or eval_runner\", *extra], cwd=C, capture_output=True, text=True)\n    return [l for l in r.stdout.splitlines() if l.startswith((\"FAILED\", \"SKIPPED\")) or l.strip().endswith((\"passed\", \"failed\", \"passed.\")) or \" passed\" in l][-12:]\ndef restore():\n    shutil.copyfile(PRIST_CAL, CAL); shutil.copyfile(PRIST_RUN, RUN); shutil.copyfile(PRIST_TST, TST)\n# M5: drop the sentence rebuild check from check_calibration\nsrc = PRIST_RUN.read_text()\nneedle = 'if c.get(\"sentences\") != calibration_sentences('\nassert src.count(needle) == 1, src.count(needle)\ni = src.index(needle); j = src.index(\"\\n\", i)\nRUN.write_text(src[:i] + \"if False:\" + src[i + len(needle):j].split(\")\", 0)[0][:0] + src[i:j].split(\"bad.append\")[0][len(needle)-0:][:0] + src[i:j] .replace(needle, \"if False and (\" , 1) + \"\\n\" + src[j+1:])\nprint(\"== M5 check_calibration sentence rebuild disabled (run.py)\")\n# rewrite cleanly instead: replace the whole line with a no-op\nRUN.write_text(src.replace(src[i:j], \"    pass  # M5 mutant: sentence rebuild removed\"))\nprint(\"   \", [l for l in RUN.read_text().splitlines() if \"M5 mutant\" in l][0].strip())\nprint(\"    pytest:\", pytest_run())\nrestore()\n# M5b: an edited served sentence with no code mutation: check_fresh must return 1 (data mutant)\nimport importlib.util\nc = json.loads(PRIST_CAL.read_text())\nc[\"sentences\"][\"overall\"][\"verified\"] = c[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"84/84\", 1)\nCAL.write_text(json.dumps(c, indent=1))\nprint(\"== M5b edited sentence 83/84 -> 84/84, check_fresh via run.py (pristine code):\")\nr = subprocess.run([PY, \"-I\", \"-c\", f\"import sys; sys.path.insert(0,{str(C)!r}); from evals import run as R; import pathlib; rc=R.check_fresh(pathlib.Path({str(C / 'evals/reports/latest.json')!r})); print('check_fresh returned', rc)\"], capture_output=True, text=True, cwd=C)\nprint(\"   \", r.stdout.strip(), \"|\", \" \".join(r.stderr.split(\"\\n\")[:3])[:300])\nrestore()\n# M8: restore the r2 skip-on-missing logic in _require_source_commit\ntsrc = PRIST_TST.read_text()\nold = 'if not _has_git():\\n        pytest.skip(\"no git repository here (exported tree)\")'\nassert tsrc.count(old) == 1\nTST.write_text(tsrc.replace(old, 'if _git(\"rev-parse\", \"--git-dir\").returncode or _git(\"cat-file\", \"-e\", c[\"source_commit\"] + \"^{commit}\").returncode:\\n        pytest.skip(\"no git history here\")'))\nCAL.write_text(json.dumps({**json.loads(PRIST_CAL.read_text()), \"source_commit\": \"1\" * 40}, indent=1))\nprint(\"== M8 old skip logic restored in test + forged source_commit 1*40\")\nprint(\"    pytest:\", pytest_run([\"-rs\"]))\nrestore()\nprint(\"== restored; pristine selector:\", pytest_run())\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$B/mutants_code.py\" \"$B\"; echo \"exit=$?\"; cmp \"$B/clone/evals/run.py\" \"$B/pristine/run.py\" && cmp \"$B/clone/tests/unit/test_eval_runner.py\" \"$B/pristine/test_eval_runner.py\" && cmp \"$B/clone/evals/reports/calibration.json\" \"$B/pristine/calibration.json\" && echo \"clone restored to pristine (run.py, test, calibration.json)\"",
 "description": "Run code and data mutants for sentence check and skip regression",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:52:25.752Z

**tool result**
````
== M5 check_calibration sentence rebuild disabled (run.py)
    pass  # M5 mutant: sentence rebuild removed
    pytest: ['FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes', '1 failed, 85 passed, 1346 deselected in 7.37s']
== M5b edited sentence 83/84 -> 84/84, check_fresh via run.py (pristine code):
    check_fresh returned 1 | check-fresh: app/llm/prompts/extract_es_v1.md changed since the report check-fresh: app/llm/prompts/judge_faithfulness_es_v1.md changed since the report check-fresh: calibration.json sentences do not match the counts they are built from
== M8 old skip logic restored in test + forged source_commit 1*40
    pytest: ['SKIPPED [3] tests/unit/test_eval_runner.py:636: no git history here', '83 passed, 3 skipped, 1346 deselected in 5.49s']
== restored; pristine selector: ['86 passed, 1346 deselected in 7.00s']
exit=0
clone restored to pristine (run.py, test, calibration.json)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:37.808Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\ncat > \"$B/mutant_m5.py\" <<'EOF'\nimport json, subprocess, shutil, sys, pathlib\nB = pathlib.Path(sys.argv[1]); C = B / \"clone\"; PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = C / \"evals/reports/calibration.json\"; PRIST_CAL = B / \"pristine/calibration.json\"\nRUN = C / \"evals/run.py\"; PRIST_RUN = B / \"pristine/run.py\"\nblock = ('    if c.get(\"sentences\") != calibration_sentences(c[\"by_state\"], c[\"by_type\"], c[\"backend\"], c[\"case_count\"], c.get(\"not_scored\") or {\"total\": 0}, c[\"case_count\"] < CAL_SMALL_N):\\n'\n         '        bad.append(\"sentences do not match the counts they are built from\")\\n')\nsrc = PRIST_RUN.read_text()\nassert src.count(block) == 1\nRUN.write_text(src.replace(block, \"    pass  # M5 mutant: sentence rebuild removed\\n\"))\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rf\", \"tests/unit\", \"-k\", \"calibration or eval_runner\"], cwd=C, capture_output=True, text=True)\nprint(\"== M5 sentence rebuild removed from check_calibration (two-line block replaced)\")\nprint(\"\\n\".join(l for l in r.stdout.splitlines() if l.startswith(\"FAILED\") or \" passed\" in l or \" failed\" in l))\nshutil.copyfile(PRIST_RUN, RUN)\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rf\", \"tests/unit\", \"-k\", \"calibration or eval_runner\"], cwd=C, capture_output=True, text=True)\nprint(\"== restored:\", r.stdout.strip().splitlines()[-1])\n# M1 failing test names\nCAL.write_text(json.dumps({**json.loads(PRIST_CAL.read_text()), \"source_commit\": \"1\" * 40}, indent=1))\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rf\", \"tests/unit\", \"-k\", \"calibration or eval_runner\"], cwd=C, capture_output=True, text=True)\nprint(\"== M1 forged source_commit 1*40, new logic: failing tests\")\nprint(\"\\n\".join(l for l in r.stdout.splitlines() if l.startswith(\"FAILED\") or \" passed\" in l or \" failed\" in l))\nshutil.copyfile(PRIST_CAL, CAL)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$B/mutant_m5.py\" \"$B\"; cmp \"$B/clone/evals/run.py\" \"$B/pristine/run.py\" && cmp \"$B/clone/evals/reports/calibration.json\" \"$B/pristine/calibration.json\" && echo \"clone restored\"",
 "description": "Redo sentence-check removal mutant and name failing tests for forged header",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:52:58.781Z

**tool result**
````
== M5 sentence rebuild removed from check_calibration (two-line block replaced)
FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_an_edited_calibration_sentence
1 failed, 85 passed, 1346 deselected in 6.99s
== restored: 86 passed, 1346 deselected in 7.04s
== M1 forged source_commit 1*40, new logic: failing tests
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 84 passed, 1346 deselected in 5.78s
clone restored
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:53:04.991Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\nmkdir -p \"$B/archive-head\" && git -C /Users/arsis/zlayt-pm-project archive 172028cfcff1750fec094d9e567e9d870a8f7b8e | tar -x -C \"$B/archive-head\"\ncat > \"$B/mutant_nogit.py\" <<'EOF'\nimport json, subprocess, shutil, sys, pathlib\nB = pathlib.Path(sys.argv[1]); A = B / \"archive-head\"; PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = A / \"evals/reports/calibration.json\"\nprint(\"archive has .git:\", (A / \".git\").exists(), \"| git sees a repo here:\", subprocess.run([\"git\", \"-C\", str(A), \"rev-parse\", \"--git-dir\"], capture_output=True).returncode == 0)\ndef run(label):\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-rs\", \"tests/unit\", \"-k\", \"calibration or eval_runner\"], cwd=A, capture_output=True, text=True)\n    print(\"==\", label)\n    print(\"\\n\".join(l for l in r.stdout.splitlines() if l.startswith((\"SKIPPED\", \"FAILED\")) or \" passed\" in l or \" failed\" in l))\nrun(\"archive of 172028c, unmodified calibration.json\")\norig = CAL.read_text()\nCAL.write_text(json.dumps({**json.loads(orig), \"source_commit\": \"1\" * 40}, indent=1))\nrun(\"archive of 172028c, forged source_commit 1*40\")\nCAL.write_text(orig)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$B/mutant_nogit.py\" \"$B\"",
 "description": "Run selector on git-less export with and without forged header",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:53:15.035Z

**tool result**
````
archive has .git: False | git sees a repo here: False
== archive of 172028c, unmodified calibration.json
SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)
SKIPPED [1] tests/unit/test_eval_runner.py:661: no git repository here
83 passed, 3 skipped, 1346 deselected in 4.40s
== archive of 172028c, forged source_commit 1*40
SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)
SKIPPED [1] tests/unit/test_eval_runner.py:661: no git repository here
83 passed, 3 skipped, 1346 deselected in 4.50s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:53:30.019Z

**tool call — Bash**
````
{
 "command": "echo \"== r2 (823b718) test defs missing at HEAD:\" && diff <(git show 823b718:tests/unit/test_eval_runner.py | grep -o \"^def test_[a-z0-9_]*\" | sort) <(git show HEAD:tests/unit/test_eval_runner.py | grep -o \"^def test_[a-z0-9_]*\" | sort); echo \"== r2 helper names at HEAD\"; git show HEAD:tests/unit/test_eval_runner.py | grep -n \"_require_source_commit\\|_has_git\\|test_committed_calibration_regenerates_exactly_from_its_source_commit\\|test_forged_source_commit\"; echo \"== git_source at 823b718 vs HEAD\"; git show 823b718:evals/run.py | grep -c \"def git_source\"; git show HEAD:evals/run.py | grep -c \"def git_source\"; echo \"== except lines in b85fc1b added/removed\"; git show b85fc1b | grep \"^[+-].*except\" ; echo \"(none if empty)\"; echo \"== skip( in HEAD eval tests around calibration\"; git show HEAD:tests/unit/test_eval_runner.py | grep -n \"skip(\"; echo \"== tree of HEAD for source_tree check\"; git rev-parse HEAD~0:evals/run.py >/dev/null && echo ok; echo \"== board validate (read-only)\"; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Check r2 tests survive at HEAD, skip sites, and board validate"
}
````

### User / tool · 2026-11-02T04:53:30.294Z

**tool result**
````
== r2 (823b718) test defs missing at HEAD:
8a9
> def test_check_fresh_fails_on_an_edited_calibration_sentence
13c14
< def test_committed_calibration_source_commit_is_an_ancestor_of_head
---
> def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head
22a24
> def test_forged_source_commit_fails_instead_of_skipping
== r2 helper names at HEAD
629:def _has_git():
633:def _require_source_commit(c):
635:    if not _has_git():
649:    _require_source_commit(c)
654:def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
660:    if not _has_git():
663:        _require_source_commit(_committed())
666:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
671:    _require_source_commit(c)
== git_source at 823b718 vs HEAD
1
1
== except lines in b85fc1b added/removed
(none if empty)
== skip( in HEAD eval tests around calibration
636:        pytest.skip("no git repository here (exported tree)")
661:        pytest.skip("no git repository here")
690:        pytest.skip("git missing")
== tree of HEAD for source_tree check
ok
== board validate (read-only)
ok (97 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:53:33.007Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/ | grep T-090; echo \"---\"; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md; echo \"---\"; cat .claude/agent-memory/staff-engineer-reviewer/feedback_severity_vs_brief.md | head -20; echo \"--- git-guard blocked? check T-090 r2 file present in HEAD\"; git log --oneline -1 -- reviews/T-090-staff-engineer-r2.md",
 "description": "Check existing review files and reviewer write rules in memory"
}
````

### User / tool · 2026-11-02T04:53:33.149Z

**tool result**
````
-rw-r--r--@   1 arsis  staff  17622 Nov  1 22:38 T-090-staff-engineer-r2.md
-rw-r--r--@   1 arsis  staff  18880 Nov  1 22:27 T-090-staff-engineer.md
---
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
---
---
name: severity-vs-brief
description: When the dispatch brief sets a default severity that conflicts with CONTRACT D.2 (for example "list mismatches as major"), rate per D.2 and state the deviation in the review
metadata:
  type: feedback
---

When the brief says to file a class of finding as a major, but the finding violates a spec constraint, rate it a blocker per CONTRACT D.2 (persona section 8) and say so in the review summary and in why_it_matters.

**Why:** T-063 brief said "list any mismatch as a major". The D-033 mismatch labelled a family member's statement as the patient's own self-report, which D-033 explicitly forbids. D.2 defines a spec-constraint violation as a blocker. I rated it a blocker, stated the deviation at the top of the review, and left the override to the orchestrator.

**How to apply:** for each finding, check the D.2 definition first; a brief's default is a starting point, not a cap. Put any deviation in the review's first paragraph so the orchestrator sees it without reading the JSON. Do not downgrade a finding to match a brief.

See also [[project_t063_doc_vs_code_review_patterns]].
--- git-guard blocked? check T-090 r2 file present in HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:54:03.054Z

**tool call — Bash**
````
{
 "command": "git show HEAD:evals/run.py | grep -n \"except Exception\\|return {\\\"commit\\\": None\\|if c.get(\\\"sentences\\\")\\|bad.append(\\\"sentences\\|def calibration_sentences\\|def check_calibration\\|def check_fresh\" ; echo \"--- test\"; git show HEAD:tests/unit/test_eval_runner.py | grep -n \"def _require_source_commit\\|def test_committed_calibration_source_commit_exists\\|def test_forged\\|def test_committed_calibration_regenerates\\|def test_check_fresh_fails_on_an_edited_calibration_sentence\\|_git(\\\"merge-base\\\"\\|source_tree is not\\|source_commit\\\"\\] + \\\"^{commit}\\\").returncode == 0\\|pytest.skip(\\\"no git repository here (exported tree)\\\")\\|pytest.skip(\\\"no git repository here\\\")\"; echo \"--- T-096 AC line in card\"; grep -n \"^  - {\\\"n\\\": 1\" board/cards/T-096.md | cut -c1-120; echo \"--- T-090 card AC carried by T-096\"; grep -n \"carried by T-096\" board/cards/T-090.md | cut -c1-80; echo \"--- grep app (exit)\"; grep -rln calibration app/ ; echo \"exit=$?\"",
 "description": "Collect exact line numbers for review citations"
}
````

### User / tool · 2026-11-02T04:54:03.217Z

**tool result**
````
76:    except Exception:
77:        return {"commit": None, "clean": None, "tree": None}
287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
1013:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1029:def check_calibration(path, root=ROOT):
1041:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
1042:        bad.append("sentences do not match the counts they are built from")
--- test
633:def _require_source_commit(c):
636:        pytest.skip("no git repository here (exported tree)")
647:def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
650:    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
651:    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"
654:def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
661:        pytest.skip("no git repository here")
666:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
722:def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
--- T-096 AC line in card
18:  - {"n": 1, "text": "Dates-to-confirm row pre-selects the suggested convention with its reason and still requires on
--- T-090 card AC carried by T-096
20:  - {"n": 1, "text": "evals report matched/seen counts for verified / needs_r
41:- 2026-11-02T04:31:37Z qa: AC 1 edited: evals report matched/seen counts for 
--- grep app (exit)
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:54:05.424Z

**tool call — Bash**
````
{
 "command": "sed -n '18p' board/cards/T-096.md | grep -o -i \"route\\|backend\\|serve[a-z]*\\|calibration\" ; echo \"matches-in-AC-line exit=$? (1 = none)\"; grep -n \"Backend AC needed\" board/cards/T-096.md | cut -c1-60; echo \"--- T-096 depends/status\"; grep -n \"^status\\|^depends_on\" board/cards/T-096.md",
 "description": "Confirm T-096 AC names no backend route"
}
````

### User / tool · 2026-11-02T04:54:05.557Z

**tool result**
````
matches-in-AC-line exit=1 (1 = none)
26:- 2026-11-02T04:48:59Z qa: From T-090 (qa): serve evals/r
--- T-096 depends/status
6:status: "ready"
8:depends_on: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:54:31.130Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-090-staff-r3 && cp /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3/out1/calibration.json artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json && ls -la artifacts/review-evidence/T-090-staff-r3/ && git status --short artifacts/review-evidence/T-090-staff-r3/",
 "description": "Create review evidence folder and copy regenerated calibration.json"
}
````

### User / tool · 2026-11-02T04:54:31.294Z

**tool result**
````
total 16
drwxr-xr-x@   3 arsis  staff     96 Nov  1 22:54 .
drwxr-xr-x@ 855 arsis  staff  27360 Nov  1 22:54 ..
-rw-r--r--@   1 arsis  staff   6953 Nov  1 22:54 regen-b85fc1b-run1-calibration.json
?? artifacts/review-evidence/T-090-staff-r3/
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:54:39.818Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt",
 "content": "T-090 r3 staff-engineer-reviewer evidence log (HEAD 172028c; code commit b85fc1b; r2 code restored by a850be0)\n\n1. Project tree selector (read-only use of the project tree)\n   $ .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"\n   86 passed, 1372 deselected in 7.39s            (0 skipped)\n   $ git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json\n   (empty: the three files equal HEAD)\n\n2. Ancestry and trees\n   $ git merge-base --is-ancestor <c> HEAD   for 823b718, 02ff244, 2fca530, 865b186, b85fc1b, 172028c -> all yes\n   $ git rev-parse b85fc1b^{tree}  -> 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f  (= header source_tree)\n   $ git show HEAD:evals/run.py | grep -c \"def git_source\"  -> 1\n   r2 test defs (823b718) vs HEAD: all present except test_committed_calibration_source_commit_is_an_ancestor_of_head,\n   renamed to test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head.\n\n3. Scratch clone: git clone --no-hardlinks, git checkout --detach 172028c\n   $ .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"   (in clone)\n   86 passed, 1346 deselected in 7.04s            (0 skipped)\n\n4. Regeneration from git archive b85fc1b (no .git), python -I, env -i, fixture (no LLM_BACKEND/ENABLE_LIVE)\n   run1 and run2 written to scratch out1/ out2/ (exit 1 both: ship bar unmet, expected; file written)\n   run1 vs run2 (generated_at excluded): IDENTICAL\n   committed vs run1, excluding generated_at, source_commit, source_tree, source_tree_clean: IDENTICAL\n   by_state, by_type, sentences, hashes, not_scored: equal to committed (True)\n   regen header on archive: source_commit None, source_tree None, clean None (no .git; test ignores git fields by design)\n   copy: artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json\n   $ grep -c \"%\" evals/reports/calibration.json -> 0\n\n5. Mutants in the scratch clone (pristine copies restored after each; final selector 86 passed)\n   M1 source_commit = \"1\"*40                   -> 2 failed, 84 passed, 0 skipped\n        FAILED test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head\n        FAILED test_committed_calibration_regenerates_exactly_from_its_source_commit\n   M2 source_commit = unreferenced commit made by git commit-tree of HEAD^{tree} (is-ancestor: no)\n                                               -> 1 failed, 85 passed\n   M3 source_tree = \"0\"*40                     -> 1 failed, 85 passed\n   M4 source_commit = \"2\"*40                   -> 2 failed, 84 passed\n   M5 check_calibration sentence rebuild (evals/run.py:1041-1042) removed\n                                               -> 1 failed: test_check_fresh_fails_on_an_edited_calibration_sentence\n   M5b calibration.json sentences.overall.verified 83/84 -> 84/84, check_fresh (clone, pristine code)\n        -> returns 1; stderr \"check-fresh: calibration.json sentences do not match the counts they are built from\"\n   M8 r2 skip logic restored in _require_source_commit (test file) + source_commit \"1\"*40\n        -> 83 passed, 3 skipped, 0 failed   (silent green: the reason the r3 change exists)\n\n6. Git-less export: git archive 172028c into scratch (no .git)\n   unmodified calibration.json : 83 passed, 3 skipped (SKIPPED [2] test_eval_runner.py:636; SKIPPED [1] :661)\n   source_commit = \"1\"*40      : 83 passed, 3 skipped   (forged header passes with skips)\n\n7. Served field owner\n   $ grep -rln calibration app/        -> (no output), exit 1\n   $ sed -n 18p board/cards/T-096.md | grep -o -i \"route|backend|serve|calibration\"  -> no output, exit 1\n   T-096 AC 1 text: \"Dates-to-confirm row ... 'Verified items matched the record N/M times in testing' line ... (T-090); e2e tests\"\n   T-096 note 2026-11-02T04:48:59Z qa: \"Backend AC needed: route returns those fields, null if file absent, no write path; test it.\"\n   T-096 shape (note) vs calibration.json keys: by_state, by_type, not_scored, sentences, case_count, small_sample,\n   backend, source_commit match; omitted: cases, hashes, models, source, match_rule, generated_at, source_tree, source_tree_clean.\n\n8. Board (read-only)\n   $ python3 tools/board.py validate  -> ok (97 file(s))\n   $ python3 tools/board.py show T-090 / show T-096 (status, ac, notes)\n"
}
````

### User / tool · 2026-11-02T04:54:39.935Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:54:58.142Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\ncat > \"$B/review_json_draft.json\" <<'EOF'\n{\"card\": \"T-090\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commits b85fc1b (evals/run.py, tests/unit/test_eval_runner.py: r3 code), 172028c (evals/reports/calibration.json: regenerated), a850be0 (restores r2 code reverted by 2fca530); HEAD 172028c. No app URL (no calibration route exists: grep -rln calibration app/ returns nothing). Sample case = fixture backend over the 10 golden cases.\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-090-staff-engineer-r2.md, memory project_t090_calibration_review_patterns.md, board/cards/T-090.md and T-096.md via tools/board.py show, python3 tools/board.py validate (ok, 97 files)\",\n  \"git show b85fc1b (full diff of evals/run.py and tests/unit/test_eval_runner.py) and git show 172028c (calibration.json diff); git show --stat a850be0, 2fca530\",\n  \"git merge-base --is-ancestor for 823b718, 02ff244, 2fca530, 865b186, b85fc1b, 172028c: all yes; git rev-parse b85fc1b^{tree} = 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f (equals header source_tree)\",\n  \"git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json: empty; git show HEAD:evals/run.py | grep -c 'def git_source' = 1; test def list of 823b718 vs HEAD: all present except one rename (test_committed_calibration_source_commit_is_an_ancestor_of_head)\",\n  \"project tree: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 86 passed, 1372 deselected, 0 skipped\",\n  \"scratch clone (git clone --no-hardlinks, detached 172028c): same selector -> 86 passed, 1346 deselected, 0 skipped; R.ROOT confirmed inside the clone\",\n  \"git archive b85fc1b into scratchpad (no .git); regenerated twice with python -I, env -i, fixture (python -I -c runpy evals.run --out); run1 vs run2 identical except generated_at; committed vs regenerated identical except generated_at, source_commit, source_tree, source_tree_clean; by_state, by_type, sentences, hashes, not_scored equal. Copy at artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json\",\n  \"mutants in the scratch clone (pristine copies restored after each): M1 source_commit 1*40 -> 2 failed, 0 skipped; M2 unreferenced non-ancestor commit -> 1 failed; M3 source_tree 0*40 -> 1 failed; M4 source_commit 2*40 -> 2 failed; M5 sentence rebuild removed from check_calibration -> 1 failed (test_check_fresh_fails_on_an_edited_calibration_sentence); M5b edited sentence 83/84->84/84, check_fresh returns 1; M8 r2 skip logic restored + forged 1*40 -> 83 passed, 3 skipped, 0 failed\",\n  \"git archive 172028c into scratchpad (no .git): selector unmodified -> 83 passed, 3 skipped; with source_commit 1*40 -> 83 passed, 3 skipped (forged header passes with skips)\",\n  \"grep -rln calibration app/ (no output, exit 1); sed -n 18p board/cards/T-096.md | grep route/backend/serve/calibration (no output); grep -c '%' evals/reports/calibration.json = 0; python dump of calibration.json keys against the served shape in the T-096 note\",\n  \"full log: artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"r2_blocker_closed_at_head\": 5, \"forged_header_fails_in_git_checkout\": 5, \"forged_header_fails_without_git\": 2, \"regeneration_from_source_commit\": 5, \"source_tree_checked_against_git\": 5, \"check_fresh_catches_sentence_edit\": 5, \"served_field_owned_with_ac\": 2, \"no_silent_skip_or_fallback\": 3, \"mutants_killed\": 5},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The served calibration field still has no backend route in any acceptance criterion; T-090 AC 1 closes on an owner that does not carry it\",\n   \"evidence\": \"board/cards/T-090.md:20 AC 1 done:true, text 'served field and UI line are carried by T-096 (frontend)'. board/cards/T-096.md:18 AC 1 (done:false, status ready) names no route, backend or serve term: sed -n 18p board/cards/T-096.md | grep -o -i 'route|backend|serve|calibration' prints nothing. board/cards/T-096.md:26 note 2026-11-02T04:48:59Z: 'Backend AC needed: route returns those fields, null if file absent, no write path; test it.' No card holds that AC. grep -rln calibration app/ prints nothing, exit 1.\",\n   \"why_it_matters\": \"The served sentence is the only path from the measured counts to the paralegal's screen. A note that says 'Backend AC needed' is a request, not a criterion, so the route can ship absent and the T-090 AC stays green. This is r2 finding 3 unchanged: the r3 change moved the UI line and the shape to T-096 but left the backend route with no AC. Not a blocker because no UI renders an unsupported number today; it must be fixed before the milestone gate.\",\n   \"fix\": \"Add an AC to T-096 (or to a named backend card) for a read-only route that returns the calibration.json fields in the T-096 note (schema evals.calibration/1), with null when evals/reports/calibration.json is absent and no write path; name that card id in T-090 AC 1.\",\n   \"acceptance_test\": \"python3 tools/board.py show <owner> lists the route AC; grep -rn calibration app/backend finds the route handler; a test reads the route against a temp calibration.json and asserts the response equals the file's sentences.overall.verified verbatim, and returns null when the file is absent.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A copy without .git skips both provenance tests, so a forged source_commit passes with 3 skips\",\n   \"evidence\": \"tests/unit/test_eval_runner.py:636 pytest.skip('no git repository here (exported tree)') and :661 pytest.skip('no git repository here'). Repro: git -C /Users/arsis/zlayt-pm-project archive 172028c | tar -x -C <scratch>/archive-head; set archive calibration.json source_commit to '1'*40; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 83 passed, 3 skipped (SKIPPED [2] :636, SKIPPED [1] :661). The unforged archive gives the same 83 passed, 3 skipped.\",\n   \"why_it_matters\": \"The r2 fix as specified (skip only when there is no repository) is implemented, and in a git checkout a forged header now fails (M1: 2 failed, 0 skipped). But any shipped copy without .git reports green with the provenance guard off, and the skip is only visible as a count. Minor because the skip is explicit and the normal submission has history; the question is whether a .git-less copy is ever what gets graded.\",\n   \"fix\": \"When there is no repository, fail unless an explicit opt-out variable is set by the export step (for example CALIBRATION_EXPORT_NO_GIT=1), so an export that is meant to be checked cannot skip the guard silently.\",\n   \"acceptance_test\": \"In a git-less copy with source_commit = '1'*40 and no opt-out variable, the selector reports at least one failed test and no skipped provenance tests.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"git_source's catch-all discards the reason git failed\",\n   \"evidence\": \"evals/run.py:76-77 'except Exception: return {\\\"commit\\\": None, \\\"clean\\\": None, \\\"tree\\\": None}' (the except line predates r3; r3 added the tree key to the same return). The None state is explicit and the header test fails on it, so this is not silent.\",\n   \"why_it_matters\": \"A missing git binary, a timeout and a non-repository all look the same in the header. Not a blocker; it hides the cause when the header comes out None.\",\n   \"fix\": \"Catch subprocess.CalledProcessError, FileNotFoundError and subprocess.TimeoutExpired, and print the reason to stderr.\",\n   \"acceptance_test\": \"git_source on a directory with no repository prints a reason to stderr and still returns the None state.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"The served shape in the T-096 note omits the provenance keys\",\n   \"evidence\": \"board/cards/T-096.md:26 note lists by_state, by_type, not_scored, sentences, case_count, small_sample, backend, source_commit. evals/reports/calibration.json also has source_tree_clean, source_tree, hashes, generated_at, cases, models, source, match_rule (python3 dump of the file's keys).\",\n   \"why_it_matters\": \"The UI cannot show that the counts came from a clean tree of the named commit. Not a spec requirement; noted so the frontend does not assume the field carries it.\",\n   \"fix\": \"If the UI should show provenance, add source_tree_clean to the served field and to the T-096 note. Otherwise say in the note that the served field is a subset.\",\n   \"acceptance_test\": \"The served route's response includes or explicitly excludes source_tree_clean, and the T-096 note matches the route's keys.\"}\n ],\n \"whats_right\": [\n  \"The r2 provenance code and its tests are back in HEAD (a850be0): git show HEAD:evals/run.py has def git_source, and every test def of 823b718 is present at HEAD except one rename.\",\n  \"A forged or unreferenced source_commit now fails in a git checkout (M1 2 failed, M2 1 failed, 0 skipped), a forged source_tree fails (M3), and an edited served sentence makes check-fresh return 1 (M5b).\",\n  \"calibration.json regenerates from git archive b85fc1b: two runs identical except generated_at, and the committed file equals the regeneration except the four git-derived fields; source_tree 3f014d4b... equals git rev-parse b85fc1b^{tree}.\"\n ],\n \"questions_for_chris\": [\n  \"Which card owns the backend route that serves calibration.json: an AC added to T-096, or a new backend card? The T-096 note asks for a backend AC that no card holds; this is the same question as r2.\",\n  \"Is a copy without .git ever what gets graded or shipped? If yes, the provenance guard skips there (finding 2) and needs another check.\",\n  \"Model record: I am running as claude-haiku-5-5 and recorded that id as the brief asked. CLAUDE.md section 6 and the persona expect Sonnet for engineering reviewers. Should reviewer records show the id actually run, or the expected one?\"\n ]}\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import json,sys; d=json.load(open(sys.argv[1])); print('parsed OK; verdict', d['verdict'], '; findings', [f['severity'] for f in d['findings']], '; whats_right', len(d['whats_right']))\" \"$B/review_json_draft.json\"",
 "description": "Draft the review JSON in scratch and parse it to validate"
}
````

### User / tool · 2026-11-02T04:54:58.256Z

**tool result**
````
parsed OK; verdict changes ; findings ['major', 'minor', 'nit', 'nit'] ; whats_right 3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:25.445Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r3.md",
 "content": "# T-090 round 3 review: forged-header skip, source_tree, sentence check, served field (commits b85fc1b, 172028c)\n\n**Verdict: changes.** No blocker. The r2 blocker is closed at HEAD: the r2 provenance code and its tests are back (a850be0), and `evals/reports/calibration.json` regenerates exactly from `git archive b85fc1b`. The r2 forged-header skip and the check-fresh sentence gap are fixed, and each mutant I ran is killed in a git checkout. One major stays open, the same as r2 finding 3: the served calibration field has no backend route in any acceptance criterion. T-090 AC 1 says the field is \"carried by T-096\", but T-096 does not carry it.\n\nMethod: the project-tree selector gives 86 passed, 0 skipped. The three files equal HEAD (`git diff --stat HEAD -- ...` empty), so that count is HEAD's. Mutants ran in a `git clone` detached at 172028c, which has `.git`, so the provenance tests run. The regeneration ran from `git archive b85fc1b`, which has no `.git`, as the brief asked. Full log: `artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt`.\n\n## r2 status\n\n| r2 finding | r3 status |\n|---|---|\n| 1 blocker: r2 fix reverted at HEAD by 2fca530 | Closed. a850be0 restores it; `git show HEAD:evals/run.py \\| grep -c \"def git_source\"` = 1; every r2 test def is at HEAD except one rename |\n| 2 major: forged source_commit passes by skipping | Closed in a git checkout (M1: 2 failed, 0 skipped). Residual in a git-less copy: finding 2 |\n| 3 major: served field has no owner | Open: finding 1 |\n| 4 minor: check-fresh passes an edited sentence | Closed: M5 kills the new test; M5b makes check_fresh return 1 |\n| 5 minor: clean flag copied into the comparison | Closed: the flag is no longer copied. `source_tree` is checked against git (test_eval_runner.py:651) and `source_tree_clean` is pinned True |\n\n## Mutants (scratch clone at 172028c, pristine files restored after each)\n\n| Mutant | Result |\n|---|---|\n| M1: `source_commit` = \"1\"*40 | 2 failed, 84 passed, 0 skipped (ancestor test and regeneration test) |\n| M2: `source_commit` = unreferenced commit, not an ancestor of HEAD | 1 failed (ancestor test) |\n| M3: `source_tree` = \"0\"*40 | 1 failed (ancestor test) |\n| M5: sentence rebuild removed from `check_calibration` (evals/run.py:1041-1042) | 1 failed: `test_check_fresh_fails_on_an_edited_calibration_sentence` |\n| M5b: `sentences.overall.verified` 83/84 changed to 84/84, pristine code | `check_fresh` returns 1; stderr \"calibration.json sentences do not match the counts they are built from\" |\n| M8: r2 skip-on-missing logic restored in `_require_source_commit`, header = \"1\"*40 | 83 passed, 3 skipped, 0 failed: a silent green, which is what r3 is meant to stop |\n\n## Findings\n\n### 1. major: the served calibration field still has no backend AC (r2 finding 3, open)\n\nEvidence: `board/cards/T-090.md:20` AC 1 is `done: true` and says \"served field and UI line are carried by T-096 (frontend)\". `board/cards/T-096.md:18` AC 1 (`done: false`, status ready) contains no route, backend or serve term: `sed -n 18p board/cards/T-096.md | grep -o -i \"route\\|backend\\|serve\\|calibration\"` prints nothing. `board/cards/T-096.md:26` is a note that says \"Backend AC needed: route returns those fields, null if file absent, no write path; test it.\" No card holds that AC. `grep -rln calibration app/` prints nothing and exits 1.\n\nWhy it matters: the served sentence is the only path from the measured counts to the paralegal's screen. A note that says \"Backend AC needed\" is a request, not a criterion, so the route can ship absent while T-090 AC 1 stays done. The r3 change moved the UI line and the field shape to T-096 but left the backend route with no AC. This is not a blocker: no UI renders the number today. It must be fixed before the milestone gate.\n\nFix: add an AC to T-096, or to a named backend card, for a read-only route that returns the `calibration.json` fields listed in the T-096 note (schema `evals.calibration/1`). It returns null when `evals/reports/calibration.json` is absent and has no write path. Name that card id in T-090 AC 1.\n\nAcceptance test: `python3 tools/board.py show <owner>` lists the route AC; `grep -rn calibration app/backend` finds the handler; a test reads the route against a temp file and asserts the response equals `sentences.overall.verified` verbatim, and returns null when the file is absent.\n\n### 2. minor: a copy without `.git` skips both provenance tests, so a forged header passes with 3 skips\n\nEvidence: `tests/unit/test_eval_runner.py:636` `pytest.skip(\"no git repository here (exported tree)\")` and `:661` `pytest.skip(\"no git repository here\")`. Repro: `git -C /Users/arsis/zlayt-pm-project archive 172028c | tar -x -C <scratch>/archive-head`, then set that copy's `source_commit` to \"1\"*40 and run `.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"`. Result: `83 passed, 3 skipped` (SKIPPED [2] at :636, SKIPPED [1] at :661). The unforged copy gives the same `83 passed, 3 skipped`.\n\nWhy it matters: the r2 fix as specified (skip only when there is no repository) is implemented, and in a git checkout a forged header now fails. But a shipped copy without `.git` reports green with the provenance guard off, and the skip shows only as a count. Minor because the skip is explicit and the normal submission has history. The open question is whether a `.git`-less copy is ever what gets graded (see questions).\n\nFix: when there is no repository, fail unless an explicit opt-out variable is set by the export step (for example `CALIBRATION_EXPORT_NO_GIT=1`).\n\nAcceptance test: in a git-less copy with `source_commit` = \"1\"*40 and no opt-out variable, the selector reports at least one failed test and no skipped provenance tests.\n\n### 3. nit: `git_source` catch-all discards the reason git failed\n\nEvidence: `evals/run.py:76-77` `except Exception:` / `return {\"commit\": None, \"clean\": None, \"tree\": None}`. The except line predates r3; r3 added the `tree` key to the same return. The None state is explicit, and the header test fails on it, so this is not silent.\n\nWhy it matters: a missing git binary, a timeout and a non-repository all look the same in the header. Not a blocker.\n\nFix: catch `subprocess.CalledProcessError`, `FileNotFoundError` and `subprocess.TimeoutExpired`, and print the reason to stderr.\n\n### 4. nit: the served shape in the T-096 note omits the provenance keys\n\nEvidence: `board/cards/T-096.md:26` lists by_state, by_type, not_scored, sentences, case_count, small_sample, backend and source_commit. `evals/reports/calibration.json` also carries `source_tree_clean`, `source_tree`, `hashes`, `generated_at`, `cases`, `models`, `source` and `match_rule` (key dump in the evidence log, section 7).\n\nWhy it matters: the UI cannot show that the counts came from a clean tree of the named commit. Not a spec requirement; noted so the frontend does not assume the field carries it.\n\nFix: if the UI should show provenance, add `source_tree_clean` to the served field and to the note. Otherwise say in the note that the served field is a subset.\n\n## Reproduced\n\n- `.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"` in the project tree: 86 passed, 1372 deselected, 0 skipped. In the scratch clone at 172028c: 86 passed, 1346 deselected.\n- Regeneration from `git archive b85fc1b` with `python -I`, `env -i`, fixture backend, run twice: run1 and run2 are identical except `generated_at`. The committed file and the regeneration are identical except the four git-derived fields (`generated_at`, `source_commit`, `source_tree`, `source_tree_clean`). Copy at `artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json`.\n- `git rev-parse b85fc1b^{tree}` = 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f, equal to the header `source_tree`.\n- `grep -c \"%\" evals/reports/calibration.json` = 0.\n- `python3 tools/board.py validate`: ok (97 files).\n\n## Outside my lens\n\nThe ship bar on the fixture run is still unmet (`4_no_invented_facts`, determinism and judge controls not measured); `evals.run` exits 1 for that reason in each regeneration. Those are not T-090 AC items. I did not judge frontend wording.\n\n```json\n{\"card\": \"T-090\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commits b85fc1b (evals/run.py, tests/unit/test_eval_runner.py: r3 code), 172028c (evals/reports/calibration.json: regenerated), a850be0 (restores r2 code reverted by 2fca530); HEAD 172028c. No app URL (no calibration route exists: grep -rln calibration app/ returns nothing). Sample case = fixture backend over the 10 golden cases.\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-090-staff-engineer-r2.md, memory project_t090_calibration_review_patterns.md, board/cards/T-090.md and T-096.md via tools/board.py show, python3 tools/board.py validate (ok, 97 files)\",\n  \"git show b85fc1b (full diff of evals/run.py and tests/unit/test_eval_runner.py) and git show 172028c (calibration.json diff); git show --stat a850be0, 2fca530\",\n  \"git merge-base --is-ancestor for 823b718, 02ff244, 2fca530, 865b186, b85fc1b, 172028c: all yes; git rev-parse b85fc1b^{tree} = 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f (equals header source_tree)\",\n  \"git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json: empty; git show HEAD:evals/run.py | grep -c 'def git_source' = 1; test def list of 823b718 vs HEAD: all present except one rename (test_committed_calibration_source_commit_is_an_ancestor_of_head)\",\n  \"project tree: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 86 passed, 1372 deselected, 0 skipped\",\n  \"scratch clone (git clone --no-hardlinks, detached 172028c): same selector -> 86 passed, 1346 deselected, 0 skipped; R.ROOT confirmed inside the clone\",\n  \"git archive b85fc1b into scratchpad (no .git); regenerated twice with python -I, env -i, fixture (python -I -c runpy evals.run --out); run1 vs run2 identical except generated_at; committed vs regenerated identical except generated_at, source_commit, source_tree, source_tree_clean; by_state, by_type, sentences, hashes, not_scored equal. Copy at artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json\",\n  \"mutants in the scratch clone (pristine copies restored after each): M1 source_commit 1*40 -> 2 failed, 0 skipped; M2 unreferenced non-ancestor commit -> 1 failed; M3 source_tree 0*40 -> 1 failed; M4 source_commit 2*40 -> 2 failed; M5 sentence rebuild removed from check_calibration -> 1 failed (test_check_fresh_fails_on_an_edited_calibration_sentence); M5b edited sentence 83/84->84/84, check_fresh returns 1; M8 r2 skip logic restored + forged 1*40 -> 83 passed, 3 skipped, 0 failed\",\n  \"git archive 172028c into scratchpad (no .git): selector unmodified -> 83 passed, 3 skipped; with source_commit 1*40 -> 83 passed, 3 skipped (forged header passes with skips)\",\n  \"grep -rln calibration app/ (no output, exit 1); sed -n 18p board/cards/T-096.md | grep route/backend/serve/calibration (no output); grep -c '%' evals/reports/calibration.json = 0; python dump of calibration.json keys against the served shape in the T-096 note\",\n  \"full log: artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"r2_blocker_closed_at_head\": 5, \"forged_header_fails_in_git_checkout\": 5, \"forged_header_fails_without_git\": 2, \"regeneration_from_source_commit\": 5, \"source_tree_checked_against_git\": 5, \"check_fresh_catches_sentence_edit\": 5, \"served_field_owned_with_ac\": 2, \"no_silent_skip_or_fallback\": 3, \"mutants_killed\": 5},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The served calibration field still has no backend route in any acceptance criterion; T-090 AC 1 closes on an owner that does not carry it\",\n   \"evidence\": \"board/cards/T-090.md:20 AC 1 done:true, text 'served field and UI line are carried by T-096 (frontend)'. board/cards/T-096.md:18 AC 1 (done:false, status ready) names no route, backend or serve term: sed -n 18p board/cards/T-096.md | grep -o -i 'route|backend|serve|calibration' prints nothing. board/cards/T-096.md:26 note 2026-11-02T04:48:59Z: 'Backend AC needed: route returns those fields, null if file absent, no write path; test it.' No card holds that AC. grep -rln calibration app/ prints nothing, exit 1.\",\n   \"why_it_matters\": \"The served sentence is the only path from the measured counts to the paralegal's screen. A note that says 'Backend AC needed' is a request, not a criterion, so the route can ship absent while the T-090 AC stays done. This is r2 finding 3 unchanged: r3 moved the UI line and the shape to T-096 but left the backend route with no AC. Not a blocker because no UI renders an unsupported number today; it must be fixed before the milestone gate.\",\n   \"fix\": \"Add an AC to T-096 (or to a named backend card) for a read-only route that returns the calibration.json fields in the T-096 note (schema evals.calibration/1), with null when evals/reports/calibration.json is absent and no write path; name that card id in T-090 AC 1.\",\n   \"acceptance_test\": \"python3 tools/board.py show <owner> lists the route AC; grep -rn calibration app/backend finds the route handler; a test reads the route against a temp calibration.json and asserts the response equals the file's sentences.overall.verified verbatim, and returns null when the file is absent.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A copy without .git skips both provenance tests, so a forged source_commit passes with 3 skips\",\n   \"evidence\": \"tests/unit/test_eval_runner.py:636 pytest.skip('no git repository here (exported tree)') and :661 pytest.skip('no git repository here'). Repro: git -C /Users/arsis/zlayt-pm-project archive 172028c | tar -x -C <scratch>/archive-head; set that copy's source_commit to '1'*40; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 83 passed, 3 skipped (SKIPPED [2] at :636, SKIPPED [1] at :661). The unforged copy gives the same 83 passed, 3 skipped.\",\n   \"why_it_matters\": \"The r2 fix as specified (skip only when there is no repository) is implemented, and in a git checkout a forged header now fails (M1: 2 failed, 0 skipped). But a shipped copy without .git reports green with the provenance guard off, and the skip shows only as a count. Minor because the skip is explicit and the normal submission has history; the open question is whether a .git-less copy is ever what gets graded.\",\n   \"fix\": \"When there is no repository, fail unless an explicit opt-out variable is set by the export step (for example CALIBRATION_EXPORT_NO_GIT=1), so an export that is meant to be checked cannot skip the guard silently.\",\n   \"acceptance_test\": \"In a git-less copy with source_commit = '1'*40 and no opt-out variable, the selector reports at least one failed test and no skipped provenance tests.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"git_source's catch-all discards the reason git failed\",\n   \"evidence\": \"evals/run.py:76-77 'except Exception: return {\\\"commit\\\": None, \\\"clean\\\": None, \\\"tree\\\": None}' (the except line predates r3; r3 added the tree key to the same return). The None state is explicit and the header test fails on it, so this is not silent.\",\n   \"why_it_matters\": \"A missing git binary, a timeout and a non-repository all look the same in the header. Not a blocker; it hides the cause when the header comes out None.\",\n   \"fix\": \"Catch subprocess.CalledProcessError, FileNotFoundError and subprocess.TimeoutExpired, and print the reason to stderr.\",\n   \"acceptance_test\": \"git_source on a directory with no repository prints a reason to stderr and still returns the None state.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"The served shape in the T-096 note omits the provenance keys\",\n   \"evidence\": \"board/cards/T-096.md:26 note lists by_state, by_type, not_scored, sentences, case_count, small_sample, backend and source_commit. evals/reports/calibration.json also carries source_tree_clean, source_tree, hashes, generated_at, cases, models, source and match_rule (key dump in the evidence log, section 7).\",\n   \"why_it_matters\": \"The UI cannot show that the counts came from a clean tree of the named commit. Not a spec requirement; noted so the frontend does not assume the field carries it.\",\n   \"fix\": \"If the UI should show provenance, add source_tree_clean to the served field and to the T-096 note. Otherwise say in the note that the served field is a subset.\",\n   \"acceptance_test\": \"The served route's response includes or explicitly excludes source_tree_clean, and the T-096 note matches the route's keys.\"}\n ],\n \"whats_right\": [\n  \"The r2 provenance code and its tests are back in HEAD (a850be0): git show HEAD:evals/run.py has def git_source, and every test def of 823b718 is present at HEAD except one rename.\",\n  \"A forged or unreferenced source_commit now fails in a git checkout (M1 2 failed, M2 1 failed, 0 skipped), a forged source_tree fails (M3), and an edited served sentence makes check-fresh return 1 (M5b).\",\n  \"calibration.json regenerates from git archive b85fc1b: two runs identical except generated_at, and the committed file equals the regeneration except the four git-derived fields; source_tree 3f014d4b... equals git rev-parse b85fc1b^{tree}.\"\n ],\n \"questions_for_chris\": [\n  \"Which card owns the backend route that serves calibration.json: an AC added to T-096, or a new backend card? The T-096 note asks for a backend AC that no card holds; this is the same question as r2.\",\n  \"Is a copy without .git ever what gets graded or shipped? If yes, the provenance guard skips there (finding 2) and needs another check.\",\n  \"Model record: I am running as claude-haiku-5-5 and recorded that id as the brief asked. CLAUDE.md section 6 and the persona expect Sonnet for engineering reviewers. Should reviewer records show the id actually run, or the expected one?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T04:55:25.607Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:28.390Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport re,json,sys\nt=open(sys.argv[1]).read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json fences:', len(blocks), '| total fences:', t.count('\\`\\`\\`'))\nd=json.loads(blocks[0]); print('parsed; verdict', d['verdict'], '; blockers', sum(f['severity']=='blocker' for f in d['findings']), '; majors', sum(f['severity']=='major' for f in d['findings']))\n\" reviews/T-090-staff-engineer-r3.md && python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Parse the review JSON block and run read-only board validate"
}
````

### User / tool · 2026-11-02T04:55:28.450Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:32.061Z

**tool call — Bash**
````
{
 "command": "B=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r3\ncat > \"$B/check_review.py\" <<'EOF'\nimport re, json, sys\nt = open(sys.argv[1]).read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, t, re.S)\nprint(\"json fences:\", len(blocks), \"| total fences:\", t.count(fence))\nd = json.loads(blocks[0])\nprint(\"parsed; verdict\", d[\"verdict\"], \"; blockers\", sum(f[\"severity\"] == \"blocker\" for f in d[\"findings\"]), \"; majors\", sum(f[\"severity\"] == \"major\" for f in d[\"findings\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$B/check_review.py\" /Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r3.md",
 "description": "Parse the review file JSON block with a scratch checker script"
}
````

### User / tool · 2026-11-02T04:55:32.173Z

**tool result**
````
json fences: 1 | total fences: 2
parsed; verdict changes ; blockers 0 ; majors 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:33.394Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3; echo \"exit=$?\"",
 "description": "Run read-only board validate on the board"
}
````

### User / tool · 2026-11-02T04:55:33.564Z

**tool result**
````
ok (98 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:35.815Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:55:35.830Z

**tool result**
````
1	---
2	name: t090-calibration-review-patterns
3	description: T-090 r1 d0aee83 calibrated-confidence review: committed artifact not reproducible from its commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive, fixture-miss log noise from score_unsplit
4	metadata:
5	  type: project
6	---
7	
8	T-090 r1 (commit d0aee83, calibrated confidence as N/M counts, D-042) written to reviews/T-090-staff-engineer.md: fail, 1 blocker, 3 majors, 4 minors, 1 nit.
9	
10	- **Committed artifact must be regenerated, not trusted.** evals/reports/calibration.json said 82/83 and 11/13, but `git archive d0aee83` + `evals.run --out` (fixture) gives 83/84 and 10/10 twice, and HEAD ec33bf0 gives the same. No `*T041847Z.md` report existed for its generated_at. Method: pin with git archive, regenerate with --out, diff counts ignoring generated_at, then hand-check two cells from a dump of the raw items.
11	- **Hand-check cells from raw items, not from the counters.** A dump script (run.py's golden_cases + pipeline.run_case, fixture) lets you tally verified amounts (9/9) and needs-review flags (2/2) by reading golden against live. Found the file's flag cell (3/5) unreproducible.
12	- **"llm call failed ... FIXTURE_MISS" lines on the eval CLI come from score_unsplit**, not from the golden cases (checked: score_unsplit alone prints 7). Do not read them as calibration misses.
13	- **Working tree evals/run.py was modified mid-review (uncommitted).** Working-tree counts (84/85, 9/9) differ from the commit's. Use archives for every count you cite.
14	- **Mutants that survive a green suite here:** dropping the class term in amount matching (test gap; golden counts identical, so the rate-vs-charge blind spot is real), dropping the tolerated term, lowering CAL_SMALL_N to 5 (the boundary test uses 30 names, never 29), and dropping the record_warning filter before zip (positional alignment, untested).
15	- **AC closed with an unbuilt clause.** Card AC 1 said "UI shows ..." and was done:true with "UI line pending frontend". Check for any route/UI reference (grep app/) before accepting an AC that names the UI.
16	- **Sentence without provenance.** The generated sentence the UI would show verbatim named N/M and a case count, not the backend. A fixture replay read as live precision. Check the rendered sentence, not only the file's top-level fields.
17	
18	**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.
19	
20	T-090 r2 (commits 823b718 code, 02ff244 file; review reviews/T-090-staff-engineer-r2.md): fail, 1 blocker, 2 majors, 2 minors.
21	- **A later commit reverted the fix.** 2fca530 (another card, committed 15 s after 823b718, before 02ff244) deleted git_source and the 11 r2 tests. HEAD evals/ and test file == 02ff244. Project-tree "84 passed" was uncommitted. Always check `git diff --quiet <fix> HEAD -- <files>` and `git log --oneline <fix>..HEAD -- <files>` before accepting a fix commit as shipped.
22	- **Skip is a silent pass for a forged header.** Provenance tests skip on "no git history" and on "commit not available", so a source_commit naming a non-existent commit reports 2 skipped and no failure. Skips must be scoped to "no .git"; a missing cited commit must fail.
23	- **check-fresh validates sums and hashes only.** An edited served sentence returns 0 from check_fresh; only the pytest regeneration test catches it.
24	- **Scratch method that worked:** clone, detached checkout of the commit, regenerate with `python -I` plus sys.path insert and runpy, compare ignoring generated_at, then mutate the clone's file and run the selector per mutant. Restore by copying a saved pristine file (not git checkout).
25	- Narrowing an AC to "UI is under T-096" left the backend serve route with no AC anywhere (grep for the route name in the owning card).
26	
27	Related: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps).
28	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:40.556Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md",
 "old_string": "Related: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps).",
 "new_string": "T-090 r3 (commits b85fc1b code, 172028c file, a850be0 restores r2; review reviews/T-090-staff-engineer-r3.md): changes, 0 blockers, 1 major, 1 minor, 2 nits.\n- **Fix verified at HEAD, then the residual moved.** r2 blocker closed (a850be0 restored git_source and 11 tests). Forged source_commit now fails in a git clone (2 failed, 0 skipped). But a .git-less copy (git archive) skips both provenance tests, so the forged header passes with 3 skipped. Test for \"fails not skips\" in a clone AND in an archive, not only in one.\n- **Served field owner still missing.** T-090 AC 1 says \"carried by T-096\"; T-096 AC 1 names no route, and its note says \"Backend AC needed\". Check the owning card's AC text for the route term, not the note.\n- **Sentence rebuild in check_calibration is real.** Removing the 2-line block (not just the `if` line) kills test_check_fresh_fails_on_an_edited_calibration_sentence; check_fresh returns 1 on an edited 83/84 -> 84/84.\n- **Mutants to run for the header/tree pattern:** source_commit 1*40 (expect fail), commit-tree orphan commit (non-ancestor, expect 1 fail), source_tree 0*40 (expect 1 fail), r2 skip logic restored (expect 3 skipped, the silent green).\n- **Regeneration from git archive matches exactly** except the git-derived fields: run twice, byte-identical except generated_at. Archive copies report source_commit None (expected; test ignores git fields).\n\nRelated: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps), [[project_harness_review_patterns]] (git-guard quirks in scratch runs)."
}
````

### User / tool · 2026-11-02T04:55:40.660Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:43.010Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md",
 "old_string": "description: T-090 r1 d0aee83 calibrated-confidence review: committed artifact not reproducible from its commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive, fixture-miss log noise from score_unsplit",
 "new_string": "description: T-090 calibrated-confidence r1-r3: committed counts not reproducible, reverted fix at HEAD, forged source_commit skip (git-less copies still skip), served field owner missing, sentence check mutant"
}
````

### User / tool · 2026-11-02T04:55:43.102Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:44.094Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:55:44.103Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:46.838Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- (T-083 r2, 2026-11-01) board-guard denied a Bash call that made a `mkdir` under `$HOME`",
 "new_string": "- (T-090 r3, 2026-11-01) git-guard denied `rm` with a variable path that expanded to a doubled dir (a mistyped `$S/t090r3/t090r3/...`); board-guard failed closed on a `python3 -c` with backslash-escaped backticks (grep for a fence). Keep scratch paths in one variable set to the scratchpad root, use `cp` not `rm`, and drive mutants from a `.py` file run with `-I` that takes the scratch dir as argv. `mkdir -p` and `cp` into `artifacts/review-evidence/<card>-r3/` worked. `git clone --no-hardlinks <project> <scratch>/clone` plus `checkout --detach` worked for a .git-carrying copy.\n- (T-083 r2, 2026-11-01) board-guard denied a Bash call that made a `mkdir` under `$HOME`"
}
````

### User / tool · 2026-11-02T04:55:46.952Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:47.962Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T04:55:47.973Z

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
24	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible; r2 823b718/02ff244: fix reverted at HEAD by 2fca530, forged source_commit skips
25	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
26	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
27	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass, rate phrase; r2 c8a9874 fails its own tree (closed 6feb2ff), class-only restore untested, gate vs classifier gap
28	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:49.878Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible; r2 823b718/02ff244: fix reverted at HEAD by 2fca530, forged source_commit skips",
 "new_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned"
}
````

### User / tool · 2026-11-02T04:55:49.986Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:55:51.889Z

T-090 r3 verdict: changes (0 blockers, 1 major: the served calibration route still has no backend AC in T-096; 1 minor: a copy without `.git` skips the provenance tests). Review: /Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r3.md
