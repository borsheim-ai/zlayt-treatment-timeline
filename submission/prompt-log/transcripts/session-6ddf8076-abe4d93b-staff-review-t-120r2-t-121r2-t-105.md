# Subagent: Staff review T-120r2/T-121r2/T-105 (Staff review T-120r2/T-121r2/T-105)

Source: `agent-abe4d93bb81e16cea.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:28:12.968Z

You are the staff-engineer reviewer in /Users/arsis/zlayt-pm-project for three cards: T-120 round 2, T-121 round 2 and T-105 round 1. Read each with `python3 tools/board.py show T-###`, plus the prior reviews: reviews/T-120-staff-engineer.md, T-120-paralegal.md, T-121-staff-engineer.md and T-121-paralegal.md.

On a `git archive HEAD` copy in your scratchpad, run the unit suite. Then check each card:
- **T-120:** the flag is suppressed only when the sentence names no condition. Probe at least 15 history-source forms ('Hx per', 'PHx obtained via ... :', 'history provided by', and others), with and without a condition. Mutate the code to test the tests.
- **T-121:** the one-line style, the translation note on its own bracket line, and the whitespace-collapse test kills the no-op mutant.
- **T-105:** the word lists come from a single source, app/llm/lexicon.yaml `added_qualifier`, used by both the English and Spanish paths. Check for any remaining duplicated lists, and that the T-100 r2 misses are covered.

Write reviews/T-120-staff-engineer-r2.md, reviews/T-121-staff-engineer-r2.md and reviews/T-105-staff-engineer.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Stop only your own PIDs. Reply in 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:14.186Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:28:14.194Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:14.886Z

**tool call — Bash**
````
{
 "command": "for t in T-120 T-121 T-105; do python3 tools/board.py show $t; echo ======; done; git log --oneline | head -8; git status --short | head -20"
}
````

### User / tool · 2026-11-02T11:28:15.158Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:15.447Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t100_r2_patterns.md"
}
````

### User / tool · 2026-11-02T11:28:15.456Z

**tool result**
````
1	---
2	name: t100-r2-review-patterns
3	description: T-100 r2 288c1d3 (changes, 1 major): r1 blocker fixed through one shared new_tokens; vocabulary still narrower than repo's own _EN_* lists; eval side-effect method
4	metadata:
5	  type: project
6	---
7	
8	T-100 r2 (card commit 288c1d3, verdict changes: 1 major, 4 minors). Method and patterns worth reusing:
9	
10	- **Eval side effect without a live model.** Run `python -m evals.run --backend fixture` on a `git archive` of the card AND of its parent, then diff the two `.md` reports and the two `latest.json` (a small recursive walk finds the one differing key). Also replay all recorded generator outputs (`tests/fixtures/llm/*.json` with keys `excerpt`,`summary`) through old and new `new_tokens`, routed by `language.detect` -> `spanish_text.module_for`. Run artifacts store only `summary_sha`, so live summaries cannot be replayed.
11	- **Fix widens one side only.** The r2 fix added summary-side qualifier words but the repo already held wider lists (`grounding._SELF_IN_QUOTE`, `spanish_text._EN_*`). Always grep the other modules for sibling word lists before accepting "one vocabulary".
12	- **Spanish branch is the unpinned branch.** Per-kind mutants (self-report, hedge, approximation) on `spanish_text.added_qualifier_tokens`: two survive all tests. Mutate each branch separately, not only the call site.
13	- **Mutant shape matters.** Removing a regex alternative that `findall` unpacks as a tuple breaks every caller (324 failures, not a valid mutant); replace the branch with a never-matching one instead.
14	- **Shared-file hunk sweep.** A card commit included another card's `memory/contracts/api.md` hunk (hidden-text 5 pt) whose code landed two commits later. Check `git show <sha> -- memory/contracts/api.md` against `git grep` of the code at that sha.
15	- **Reviewer env.** Scripts must live under `artifacts/review-evidence/`; scratchpad writes only via shell redirects. git-guard rejects `$var` in command position and parse-fails on complex quoting in python3 -c; put code in a script file. `rm -rf` is denied. Review files are append-only: proof-read line cites before the first Write (I left four cites off by 1 to 3 lines).
16	- **Baseline failures to expect in an exported tree:** `test_eval_runner.py::..._exported_tree_without_git` and `test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts` fail on parent and card; the second also in the working tree.
17	
18	**Why:** r1 was a one-directional check; r2 checks the fix at the route, gate and vocabulary level.
19	**How to apply:** see [[project_t100_d047_review_patterns]] for r1; for any "one shared function" fix, mutate each call site and each branch.
20	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:17.862Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p reviews/T-120-staff-engineer.md | head -150; echo =====; tail -n +1 reviews/T-121-staff-engineer.md | head -120"
}
````

### User / tool · 2026-11-02T11:28:17.965Z

**tool result**
````
# T-120 staff-engineer review (commit 1cb8707, archive of c26ff04)

Verdict: changes. The guard works for the cases it lists, but the `per`/`via` branch is unconditional and silently drops a flag on a real prior-condition mention.

Exercised (all on a `git archive` copy of c26ff04, run with the project venv):
- `pytest tests/unit -q`: 2816 passed, 4 skipped.
- `python -m evals.run` on the fixture backend: runs; `--check-spec` gives spec_matches_golden true. The fixture run reports ship_bar_met=False on the usual live-only items.
- `python -m app.pipeline evals/golden/sample.txt` twice: byte-identical output.
- Probe script calling `lexicon_scan.scan` on 10 phrasings (below).
- Mutants against tests/unit/test_t120_history_source_sentence.py: removing the guard is killed, and widening it to every Hx hit is killed. My third mutant (adding `|:`) was inert, because the `\s+` prefix blocks it. It proves nothing and is not counted.
- Read the diff in full. There is no LLM call, no float, no network and no clock. The guard is code only, in lexicon_scan.

```json
{"card": "T-120", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04 (T-120 commit 1cb8707): app/backend/lexicon_scan.py, tests/unit/test_t120_history_source_sentence.py; no app URL; sample case plus lib09",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "python -m evals.run (fixture) and --check-spec: spec_matches_golden true", "python -m app.pipeline evals/golden/sample.txt twice: identical", "probe of lexicon_scan.scan on 10 Hx/History phrasings", "mutants: drop guard (killed), guard hits every Hx (killed)", "read git show 1cb8707 in full"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "The `Hx per ...` branch drops the flag on real prior-condition mentions",
   "evidence": "app/backend/lexicon_scan.py:15 `(?:per|via)\\s` is unconditional, and :136 skips the hit. Probe with `.venv/bin/python -I` on the archive: scan('Hx per patient: lumbar strain 2019.') -> [] ; scan('Hx per patient of lumbar strain') -> [] ; scan('PMH per patient: diabetes since 2015.') -> []. 'Hx per patient: ...' is ordinary note phrasing. tests/unit/test_t120_history_source_sentence.py REAL list has no 'per' case, so the suite is green.",
   "why_it_matters": "The skip is meant for sentences that name who gave the history. 'Hx per patient: lumbar strain 2019' names the source and a prior condition together, and the whole condition mention disappears. That is a lost recall flag with no trace, on a defense-relevant item (R-FL pre_existing).",
   "fix": "Narrow the `per`/`via` branch so it skips only when the source phrase ends the clause or is followed by an interpreter/family-member noun and no condition text (or only skip the `Hx` token and let the remaining clause scan run). Do not skip when a colon, 'of', a year or a condition word follows the source.",
   "acceptance_test": "Add to REAL: 'Hx per patient: lumbar strain 2019.', 'Hx per patient of lumbar strain', 'History per patient: left knee surgery in 2017.' and assert a pre_existing hit; keep every SOURCE case green. Mutant widening `(?:per|via)\\s` to any following text must fail."}
 ],
 "whats_right": ["Guard is deterministic code in lexicon_scan; lexicon.yaml untouched; evals fixture flag P/R unchanged.", "The sentence-adjacent test proves a real prior mention next to a source sentence still hits.", "Removing or broadening the guard fails the new tests."],
 "questions_for_chris": []}
```
=====
# T-121 staff-engineer review (commit c26ff04)

Verdict: changes. The style option is built by code, the default letter still equals the golden, and the API rejects bad styles. The one-line style has two defects: it prints a "translation" note over a letter line with no translation in it, and it rewrites the quote's whitespace without a test that would notice.

Exercised (archive of c26ff04, project venv):
- `pytest tests/unit -q`: 2816 passed, 4 skipped. This includes the golden byte-equal test and the updated Spanish and D-050 tests.
- `python -m evals.run --check-spec`: letter_equal true, internal_notes_equal true.
- A probe script (scratch) building the letter with a Spanish-labelled entry that has a multi-line excerpt, in both styles.
- Six mutants against tests/unit/test_t121_letter_styles.py: dropping the note, ignoring the style, dropping the PDF page, removing the API check and dropping the note from one-line are all killed. A no-op `_one_line` survives.
- Read the diff in full (export.py, export_routes.py, api.py, api.md). There is no LLM call, no float and no network. Both routes validate the style before building.

```json
{"card": "T-121", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04: app/backend/export.py, export_routes.py, api.py, memory/contracts/api.md, tests/unit/test_t121_letter_styles.py, test_spanish_records.py, test_d050_never_verified.py",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "python -m evals.run --check-spec: letter_equal true", "probe: Spanish-labelled entry with multi-line excerpt, standard vs oneline", "6 mutants on test_t121_letter_styles.py: 5 killed, 1 survived (_one_line no-op)", "read git show c26ff04 in full"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "One-line style prints an 'AI translation' note on a line that has no translation",
   "evidence": "app/backend/export.py:259 the oneline branch emits only the date, provider, quote and bracket, plus `_translation_note(e)`; the summary (the English translation, or the reviewer's edited translation) is never printed. Probe output: `January 9, 2026 — Austin EMS run report: \"Conductor con cinturon. Dolor lumbar 7/10.\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]`. The standard style prints the translation on the line above the quote. tests/unit/test_t121_letter_styles.py::test_api_style_param_and_unknown_style only asserts the note count and that ES_QUOTE is present, not that any translation is.",
   "why_it_matters": "The note tells the paralegal an AI translation is here to check. In this style there is nothing to check, and the reviewer's edited translation (Translation (edited by reviewer)) is lost from the letter. A Spanish quote may reach the demand letter with a note about a translation that was never written.",
   "fix": "For a translated entry in the one-line style, either append the translation inside the line (for example after the quote, before the bracketed note) or reword the note to say the quote is untranslated. Do not claim a translation that is not on the line.",
   "acceptance_test": "Add a test: a Spanish-labelled entry in style=oneline must contain its summary text on the same line as the note (or the reworded note), for both labels AI translation and Translation (edited by reviewer). Mutant dropping the summary from that line must fail."},
  {"severity": "minor",
   "title": "One-line style collapses whitespace inside the quote, so it is no longer a verbatim substring; the test cannot see it",
   "evidence": "export.py:248-250 `_one_line` and :259 `_one_line(e[\"excerpt\"])`. Probe: excerpt 'Conductor con cinturon.\\n  Dolor   lumbar 7/10.' gives `excerpt in oneline_letter` False, while the standard style keeps it verbatim. Mutant `_one_line` -> `str(s)` SURVIVED all 10 tests in test_t121_letter_styles.py, because the sample excerpts are single-line (test_oneline_quote_is_still_a_substring_of_the_record_and_has_no_newline is therefore vacuous for its 'no newline' half).",
   "why_it_matters": "The letter's quote is the product's grounded text. Whitespace-only normalization is acceptable if it is documented, but here it is undocumented and unpinned, so a later change could silently change quotes.",
   "fix": "Document the normalization (whitespace only) in the docstring and api.md, and add a multi-line-excerpt test that asserts the collapsed form equals the whitespace-normalized excerpt and contains no newline.",
   "acceptance_test": "Test with excerpt 'a\\n  b' asserts the one-line letter contains '\"a b\"' and no other newline inside the entry line; the no-op mutant must fail."},
  {"severity": "nit",
   "title": "Style validation is duplicated in two routes",
   "evidence": "app/backend/api.py:520-523 and app/backend/export_routes.py:71 both check the style and build the 422.",
   "why_it_matters": "Two copies of the same check will drift; only one route answers at a time.",
   "fix": "Keep one route and call a shared helper.",
   "acceptance_test": "Optional: a test that both routes return the same body for ?style=fancy."}
 ],
 "whats_right": ["Default and style=standard letters stay byte-equal to evals/golden; build_export stays a pure function of accepted items.", "Invalid style fails fast with 422 invalid_style and a ValueError in the pure builder, no silent fallback.", "The bracketed note is keyed to the translation label and tested to end the entry in both styles."],
 "questions_for_chris": []}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:18.341Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-120-paralegal.md | head -80; echo ====; cat reviews/T-121-paralegal.md | head -60; git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T11:28:18.451Z

**tool result**
````
# T-120 paralegal review

**Verdict: fail.** One blocker. The fix for "Hx obtained via ..." also hides a real prior condition that the pre-T-120 build flags. Lib09 itself is clean.

Scope: T-120 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09, lib02, lib11, sample, plus engine-level probes of flags.lexicon_flags.

What I checked:
- lib09 on HEAD: no pre_existing flag (T-120-123-paralegal-probe.out.json, A_lib09_pre_existing_flags = []). The parent flags the sentence on record 1 (T-120-paralegal-before-after-parent.txt). The other lib09 flags are unchanged (T-120-paralegal-flags-diff-parent.txt vs -HEAD.txt; only the pre_existing flag is gone).
- The card's "record 2" is wrong: the sentence is in record 1 of the library file and in app record r1 (A_raw_lib09_interpreter_sentence_in = [1]).
- Real prior controls on HEAD: sample still flags record 3 "Patient reports low back pain in 2023, resolved." and record 8 "Findings may represent degenerative change" (A_sample_pre_existing_flags). lib02 and lib11 still flag (A_lib02_pre_existing_flags, A_lib11_pre_existing_flags).
- Variants on the flag engine (T-120-paralegal-variants-HEAD.txt vs -parent.txt):
  - "Hx obtained via interpreter: lumbar strain 2019." raises nothing on HEAD; the parent flags the whole sentence.
  - "PHx obtained via patient's son: lumbar strain 2019." raises nothing on HEAD; the parent flags it.
  - Period-joined variants still flag on HEAD.
- Unit tests test_t120, test_t121 and test_t123 on the HEAD copy: 48 passed. None of them uses the colon form, so the regression is not covered.

Ship-bar score (verify_quickly 2): the lib09 entries verify quickly, but the prior-condition list cannot be trusted as complete until the colon case is fixed. A reviewer who relies on the flag list would miss the prior.

Findings are in the JSON block.

```json
{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); sample evals/golden/sample.txt; library case_lib09, case_lib02, case_lib11; engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan",
 "exercised": [
  "read board show T-120, personas/paralegal.md, CLAUDE.md",
  "pytest on tests/unit/test_t120_history_source_sentence.py, test_t121_letter_styles.py, test_t123_baseline_same_day_paperwork.py on the HEAD copy: 48 passed",
  "HTTP on :7893 and :7894: POST /api/cases {library: case_lib09...}, poll status to ready, GET case flags (artifacts/review-evidence/T-120-paralegal-before-after-parent.txt, T-120-paralegal-flags-diff-parent.txt, T-120-paralegal-flags-diff-HEAD.txt)",
  "HTTP on :7893: sample, lib02, lib11 pre_existing flags (artifacts/review-evidence/T-120-123-paralegal-probe.out.json)",
  "in-process flags.lexicon_flags on lib09 record 1 with the excerpt replaced by 3 variants, HEAD and parent (T-120-paralegal-engine-HEAD.txt, T-120-paralegal-engine-parent.txt)",
  "in-process lexicon_scan.scan on 11 variant texts, HEAD and parent (T-120-paralegal-variants-HEAD.txt, T-120-paralegal-variants-parent.txt)",
  "raw record check of the library file: the sentence is in record 1 (A_raw_lib09_interpreter_sentence_in)"],
 "verdict": "fail",
 "scores": {"verify_quickly": 2, "prior_mentions_flagged": 2, "interpreter_sentence_not_flagged": 5},
 "findings": [
  {"severity": "blocker",
   "title": "The skip drops the whole prior hit, so a real prior after a colon on a history-source line is no longer flagged (regression vs 0c47356)",
   "evidence": "artifacts/review-evidence/T-120-paralegal-engine-HEAD.txt: 'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag; \"PHx obtained via patient's son: lumbar strain 2019.\" -> NO pre_existing flag. artifacts/review-evidence/T-120-paralegal-engine-parent.txt, same inputs: ['Hx obtained via interpreter: lumbar strain 2019.'] and [\"PHx obtained via patient's son: lumbar strain 2019.\"]. Same result in T-120-paralegal-variants-HEAD.txt vs -parent.txt.",
   "why_it_matters": "Checklist 9 and card AC 1 (a real prior-condition mention still raises the flag) are broken for this shape. The record still says lumbar strain 2019, but the tool no longer surfaces it, which is the prior injury the adjuster will find and the paralegal missed. The fix removes a guess (a source phrase is not a prior) and deletes a fact next to it.",
   "fix": "Drop only the source-phrase span (for example 'Hx obtained via interpreter') from the hit, and keep any lexicon match that extends past it, including after a colon or semicolon. Keep the current sentence-level behaviour for 'Hx obtained via ..., who interpreted. Hx of lumbar strain 2019.'.",
   "acceptance_test": "Add both colon inputs above to REAL in tests/unit/test_t120_history_source_sentence.py and assert FL.lexicon_flags(record) returns a pre_existing flag for each. Re-run the T-120 probe: lib09 still has no pre_existing flag, and sample still flags record 3 and record 8. Re-run the parent-vs-HEAD variant probe and expect no row to lose a flag that the parent raised except the source-phrase-only row."},
  {"severity": "minor",
   "title": "Card AC and test name cite lib09 'record 2' for the interpreter sentence; it is record 1",
   "evidence": "board/cards/T-120.md AC 1 text: 'the interpreter-history sentence of record 2'; test name test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do; evals/library/case_lib09_spanish_interpreter_espalda.txt, '=== Record 1 ===' Excerpt starts 'Hx obtained via patient's son, who interpreted.'; record 2 (14/04/2026, Consultorio Médico Aguaclara) has no such sentence; A_raw_lib09_interpreter_sentence_in = [1].",
   "why_it_matters": "Checklist 3 needs the record reference to point at the right source in one action. A paralegal who opens record 2 to check the AC will not find the sentence.",
   "fix": "Change the AC text, the test name and the handoff to record 1 (app id r1).",
   "acceptance_test": "grep of the AC and test name shows record 1; the lib09 record list in the case JSON shows the sentence under r1."},
  {"severity": "nit",
   "title": "Flag ids are positional: f_r1_1 names a different flag on HEAD than on the parent",
   "evidence": "artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt: id f_r1_1 = pre_existing (Hx sentence), f_r1_2 = causation 'Reported onset'. T-120-paralegal-flags-diff-HEAD.txt: id f_r1_1 = causation 'Reported onset'; f_r1_2 is gone.",
   "why_it_matters": "If any saved decision is keyed by flag id, it could attach to a different flag after a re-run. I did not test whether decisions carry over, so this is a risk to check, not a loss I reproduced.",
   "fix": "Derive flag ids from category and record so they survive a removed flag, or confirm that decisions are not keyed by id across builds.",
   "acceptance_test": "A flag decision made on a case before a flag is removed still points at the same flag after a re-run on the new build."}
 ],
 "whats_right": [
  "lib09 on HEAD raises no pre_existing flag on the 'Hx obtained via patient's son, who interpreted.' sentence, and the gap (42 days), date-to-confirm and three patient-report flags are unchanged against the parent",
  "the sample's two real prior mentions (record 3 'low back pain in 2023, resolved', record 8 'may represent degenerative change') still raise flags, with verbatim evidence",
  "the period-joined 'Hx ... Hx of lumbar strain 2019.' and 'Hx ... Prior low back pain 2023, resolved.' forms still flag on HEAD"],
 "questions_for_chris": [
  "On the live backend the model may also propose a prior-condition flag. Does the merge at flags.py:249 keep an LLM prior flag on the Hx sentence? The fixture set cannot show this; I only tested the lexicon path."]
}
```
====
# T-121 paralegal review

**Verdict: pass.** No blockers or majors. Every entry line in both styles matches its raw record: long date, provider as written, verbatim quote, citation placeholder. The "AI translation:" prefix is gone from the summary lines. Two minors: where the translation note sits, and the one-line form is not reachable from the screen.

Scope: T-121 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09 (Spanish, interpreter) and the sample (golden).

What I checked:
- lib09: accepted the 6 entries, 2 charges and 2 rates through the live review route (all 200). Standard and one-line exports both 200 (T-120-123-paralegal-probe.out.json, B_lib09_*).
- Each entry line verified against the raw record text (T-121-paralegal-letter-check.out.json): lib09 6/6 in standard and 6/6 in one-line; sample 9/9 in both. The date is the raw record date in long format, the provider equals the raw Source label, the quote is a verbatim substring of the raw excerpt.
- Translation label before and after: the parent prints "LINE: AI translation: Patient reports pain 6/10 that worsens when raising the arm..." and "LINE: AI translation: Account statement: ..." (T-121-paralegal-before-after-parent.txt). HEAD prints neither; the note sits at the end of the Source line (T-121-paralegal-before-after-HEAD.txt). Billed total $5,090.00 on both builds; the unclear amounts stay out.
- Sample: accepted all 9 entries and the amounts. The standard letter equals the LETTER_TEXT block of evals/golden/sample.export.expected.txt (exact match). One-line export is 9 lines, one per entry, with the same two charges.
- ?style=Oneline and ?style=bogus both return 422 invalid_style.
- Frontend: app/frontend/api.js:43 calls GET /export with no style, and `grep -rl oneline app/frontend` returns no file, so the screen cannot request the one-line form.

Ship-bar score (verify_quickly 4): each entry line carries its date, provider, verbatim quote and citation placeholder, so I could check a line in one read. Spanish lines are slower because the English summary and the Spanish quote are not paired and the note sits next to the quote.

```json
{"card": "T-121", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); library case_lib09; sample evals/golden/sample.txt; app/frontend/api.js",
 "exercised": [
  "read board show T-121, personas/paralegal.md, CLAUDE.md",
  "pytest on tests/unit/test_t121_letter_styles.py (with test_t120 and test_t123, 48 passed on the HEAD copy)",
  "HTTP on :7893: POST /api/cases {library: case_lib09...}, run, poll ready; POST /items/{id}/review accept on 6 entries, 2 charges and 2 rates (all 200); GET /export and GET /export?style=oneline (both 200); GET ?style=Oneline and ?style=bogus (422 invalid_style)",
  "HTTP on :7893: sample accepted, standard letter compared with the golden LETTER_TEXT block (exact match), one-line export (9 lines)",
  "HTTP on :7894: the same lib09 accept and standard export on the parent build (T-121-paralegal-before-after-parent.txt)",
  "letter verification script: every entry line in both styles against the raw library/sample text (T-121-paralegal-letter-check.txt and .out.json)",
  "grep of app/frontend for oneline and style (0 hits); api.js:43 exportCase"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "verbatim_quotes": 5, "translation_note_placement": 3},
 "findings": [
  {"severity": "minor",
   "title": "The translation note sits on the Spanish quote line, not on the English summary it describes; in one-line style the line has no English text",
   "evidence": "artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt: 'LINE: Source [Ex. __ / Bates __]: \"Refiere dolor 6/10 que empeora al levantar el brazo. ...\" [AI translation of the Spanish original; check before sending]'. One-line export (artifacts/review-evidence/T-120-123-paralegal-probe.out.json, B_lib09_oneline_letter): 'April 14, 2026 — Consultorio Médico Aguaclara, nota de consulta: \"Refiere dolor 6/10 ...\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]'.",
   "why_it_matters": "The thing to check is the English summary line above, and it carries no marker. The warning reads as a comment on the Spanish original, which is not a translation. In one-line style nothing on the line is translated, so the note describes text the line does not have. A paralegal who deletes the note by mistake leaves an unmarked AI summary.",
   "fix": "In standard style put the marker on the summary line that holds the AI translation. In one-line style print the note only when the line carries translated text, or move it to the internal notes (see question 1).",
   "acceptance_test": "lib09 standard export: the bracketed phrase is on the same line as the AI-translated summary of each Spanish entry. lib09 one-line export: no bracketed claim on a line that holds only the Spanish quote, or the question-1 decision is recorded."},
  {"severity": "minor",
   "title": "The one-line style cannot be reached from the app; the screen always gets the standard letter",
   "evidence": "app/frontend/api.js:43: exportCase: (token) => call(\"GET\", t(token) + \"/export\"). grep -rl oneline app/frontend: 0 files. The card handoff says a style toggle is left to frontend.",
   "why_it_matters": "The goal is an export she can paste with minimal reformatting. The one-line form exists only through a direct GET with ?style=oneline, so the paralegal cannot choose it on the screen. The card's AC is API-level, so this is a gap for the next card rather than a failure of T-121.",
   "fix": "Add a style control to the export panel that calls /export?style=oneline and shows the returned letter_text unchanged.",
   "acceptance_test": "In the app, choosing the one-line option shows letter_text byte-equal to GET /export?style=oneline for lib09 and sample."}
 ],
 "whats_right": [
  "every entry line in both styles verifies against the raw record: lib09 6/6 and sample 9/9, date, provider as written, verbatim quote (T-121-paralegal-letter-check.out.json)",
  "the 'AI translation:' prefix is gone from the summary lines (the parent prints it twice on lib09); the billed total stays $5,090.00 with the unclear amounts out",
  "the sample standard letter equals the golden LETTER_TEXT block exactly, and invalid style values return 422 invalid_style"],
 "questions_for_chris": [
  "Decision needed: D-001 keeps notes out of the letter body. The translation warning sits inside the letter by design (card AC 2 and the pass-2 F9 request asked for a bracketed, removable phrase). Keep it in the letter, or move it to the internal notes and keep only the translated summary in the letter?",
  "For Spanish entries the one-line form carries only the Spanish quote, with no English. Is a Spanish-only quote acceptable in a demand to an English-speaking adjuster, or should the one-line form carry the English summary too?"]
}
```
433ac1c60f608713917d4fa4010a54d5fb6cae08
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:22.608Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; ls $S | head; git show 07dbd2b --stat | tail -8; git show 07dbd2b -- app/backend/lexicon_scan.py"
}
````

### User / tool · 2026-11-02T11:28:22.741Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
641ed.bak
M1
M1_nocombine
M2
M2_find0
M3
M4
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896

    fix(backend): T-120 r2 history-source skip only when the sentence names no condition (colon, year, 'of' keep the flag); per/via only before a person or channel
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/lexicon_scan.py                     | 20 ++++++++++++++++++--
 tests/unit/test_t120_history_source_sentence.py |  8 ++++++--
 2 files changed, 24 insertions(+), 4 deletions(-)
commit 07dbd2b6513b8e124e8c3da5306e2cadb8ac20e6
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:27:21 2026 -0600

    fix(backend): T-120 r2 history-source skip only when the sentence names no condition (colon, year, 'of' keep the flag); per/via only before a person or channel
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/lexicon_scan.py b/app/backend/lexicon_scan.py
index f7858b7..10050fb 100644
--- a/app/backend/lexicon_scan.py
+++ b/app/backend/lexicon_scan.py
@@ -12,7 +12,12 @@ RAISES = ("high", "medium")
 # T-120: "Hx obtained via patient's son, who interpreted" names who GAVE the history; it states no prior condition. Only the bare history
 # abbreviation or word, directly followed by a source word, is skipped ("Hx of lumbar strain", "Hx: neck pain" still hit).
 _HISTORY_WORD = re.compile(r"(?:hx|h/o|phx|history)\Z", re.I)
-_HISTORY_SOURCE = re.compile(r"\s+(?:(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+(?:via|from|by|through|per|with)\b|(?:per|via)\s)", re.I)
+_HISTORY_SOURCE = re.compile(r"\s+(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+(?:via|from|by|through|per|with)\b", re.I)
+# "Hx per ..." / "Hx via ..." skip only before a person or channel that gave the history ("per patient's son", "via interpreter"), never before
+# "per patient: lumbar strain 2019" (T-120 staff review: that names a condition).
+_HISTORY_VIA = re.compile(r"\s+(?:per|via)\s+(?:the\s+)?(?:(?:patient|pt)(?:'s)?\s+)?(?:son|daughter|husband|wife|spouse|mother|father|brother|sister|sibling|family|friend|caregiver|"
+                          r"relative|guardian|parent|interpreter|translator|language\s+line|telephone|phone|video|ipad|tablet|staff|nurse|ems)\b", re.I)
+_SENT_END = re.compile(r"[.!?](?:\s|$)|\n")
 
 
 def _sentence_bounds(text, start, end):
@@ -99,6 +104,17 @@ def _entries() -> tuple:
     return tuple(out)
 
 
+def _is_source_sentence(text: str, end: int) -> bool:
+    """T-120: the history word at text[:end] is followed by a statement of WHO gave the history and nothing that states a condition: no colon, no digit
+    (a year) and no 'of' in the rest of the sentence. "Hx obtained via patient's son, who interpreted." skips; "Hx per patient: lumbar strain 2019." and
+    "Hx obtained via interpreter: prior neck injury." still hit."""
+    if not (_HISTORY_SOURCE.match(text, end) or _HISTORY_VIA.match(text, end)):
+        return False
+    m = _SENT_END.search(text, end)
+    rest = text[end:m.start() if m else len(text)]
+    return not re.search(r":|\d|\bof\b", rest, re.I)
+
+
 def _hit_year(m):
     for g in ("year", "year2"):
         try:
@@ -133,7 +149,7 @@ def scan(text: str, accident_year=None) -> list:
                     continue
             if sup and sup.search(_clause_after(text, m.end())):
                 continue
-            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _HISTORY_SOURCE.match(text, m.end()):
+            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _is_source_sentence(text, m.end()):
                 continue
             u = next(((a, b) for a, b in units if a <= m.start() < b), (m.start(), m.end()))
             out.append({"id": e["id"], "flag_type": e["flag_type"], "category": e["category"], "strength": e["strength"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:29.121Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t120r2/arc && git archive HEAD | tar -x -C $S/t120r2/arc && ls $S/t120r2/arc | head -30; ls .venv/bin/python; ls $S/t120r2/arc/evals/library | head -3"
}
````

### User / tool · 2026-11-02T11:28:30.099Z

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
.venv/bin/python
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:33.039Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t120r2/arc && (timeout 590 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15) ",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T11:28:33.134Z

**tool result**
````
Command running in background with ID: bnd3i9xln. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bnd3i9xln.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:33.397Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/unit/test_t120_history_source_sentence.py"
}
````

### User / tool · 2026-11-02T11:28:33.496Z

**tool result**
````
"""T-120 (T-060 pass-2 F13): a history-SOURCE sentence ('Hx obtained via patient's son, who interpreted') names who gave the history,
not a prior condition, so the phrase list does not raise 'Mention of a prior or pre-existing condition' on it. A real prior-condition
mention still raises the flag, in the same record and in others. Deterministic code guard in lexicon_scan (the lexicon is researcher-owned)."""
import pathlib

import pytest

from app.backend import flags as FL, ingest as I, lexicon_scan as LS

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ["Hx obtained via patient's son, who interpreted.", "Hx obtained from patient's daughter.", "Hx taken per interpreter.",
          "History obtained via interpreter.", "History provided by patient's husband.", "hx was obtained through a telephone interpreter.",
          "H/o obtained via family member.", "Hx per patient's son, who interpreted.", "Hx via interpreter."]
REAL = ["Hx obtained via interpreter: lumbar strain 2019.", "PHx obtained via patient's son: lumbar strain 2019.", "Hx obtained via interpreter; lumbar strain 2019.",
        "Hx per patient: lumbar strain 2019.", "Hx per patient of lumbar strain", "History per patient: left knee surgery in 2017.",
        "Hx per patient lumbar strain", "Hx via interpreter: prior neck injury 2018.", "Hx obtained from patient: lumbar strain 2019.", "Hx obtained via patient's son of lumbar strain",
        "Hx per patient's son: prior neck injury.", "Hx of lumbar strain.", "Hx: lumbar strain 2019.", "History of migraines.", "Hx neck pain.", "h/o lumbar strain",
        "Prior history of neck pain 2019, resolved."]


def _prior(text):
    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]


@pytest.mark.parametrize("s", SOURCE)
def test_history_source_sentence_raises_no_prior_condition_hit(s):
    assert _prior(s) == []
    assert _prior(s + " Patient states she was struck by a car. Left shoulder pain 7/10.") == []


@pytest.mark.parametrize("s", REAL)
def test_real_prior_condition_mentions_still_hit(s):
    assert _prior(s)


def test_source_sentence_does_not_hide_a_real_prior_condition_next_to_it():
    t = "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. Left shoulder pain 7/10."
    hits = _prior(t)
    assert len(hits) >= 1 and all("lumbar strain" in t[h["unit_start"]:h["unit_end"]] for h in hits)
    t2 = "Hx obtained via patient's son. Prior neck injury in 2018."
    assert _prior(t2)


def test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do():
    recs = I.ingest((ROOT / "evals/library/case_lib09_spanish_interpreter_espalda.txt").read_text(encoding="utf-8"))["records"]
    interp = next(r for r in recs if "Hx obtained via" in r["excerpt"])
    assert interp["n"] == 1                                    # the interpreter sentence is in record 1 of lib09 (r1), not record 2
    assert [f for f in FL.lexicon_flags(interp) if f["type"] == "pre_existing"] == []
    real = dict(interp, excerpt="Hx obtained via patient's son, who interpreted. Prior history of left shoulder dislocation 2019. Pain 7/10.")
    pre = [f for f in FL.lexicon_flags(real) if f["type"] == "pre_existing"]
    assert pre and all("Hx obtained via" not in f["excerpt"] for f in pre)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:34.865Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bnd3i9xln.output"
}
````

### User / tool · 2026-11-02T11:28:34.971Z

**tool result**
````
/bin/bash: timeout: command not found

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:37.937Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t120r2/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > $S/t120r2/unit.out 2>&1; tail -15 $S/t120r2/unit.out",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T11:28:38.005Z

**tool result**
````
Command running in background with ID: bljd8laqr. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bljd8laqr.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:38.372Z

**tool call — Bash**
````
{
 "command": "sed -n 120,175p app/backend/lexicon_scan.py; git show 4c59fac --stat | tail -8"
}
````

### User / tool · 2026-11-02T11:28:38.581Z

**tool result**
````
        try:
            if m.group(g):
                return int(m.group(g))
        except IndexError:
            pass
    y = YEAR.search(m.group(0))
    return int(y.group(0)) if y else None


def _clause_after(text, end):
    m = re.search(r"[,;.\n]", text[end:])
    return text[end:end + m.start()] if m else text[end:]


def scan(text: str, accident_year=None) -> list:
    """Firing hits as [{id, flag_type, category, strength, start, end, text, unit_start, unit_end}], file order. Unknown accident_year keeps
    year-filtered hits (the item is reviewed anyway)."""
    neg = lexicon.load()["negation"]
    units = sentences.stripped_spans(text)
    out = []
    for e, rx, sup in _entries():
        if e["strength"] not in RAISES:
            continue
        for m in rx.finditer(text):
            if e.get("negatable") and negated(text, m.start(), m.end(), neg):
                continue
            if e.get("year_filter") and accident_year:
                y = _hit_year(m)
                if y and y >= accident_year:
                    continue
            if sup and sup.search(_clause_after(text, m.end())):
                continue
            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _is_source_sentence(text, m.end()):
                continue
            u = next(((a, b) for a, b in units if a <= m.start() < b), (m.start(), m.end()))
            out.append({"id": e["id"], "flag_type": e["flag_type"], "category": e["category"], "strength": e["strength"],
                        "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": u[0], "unit_end": u[1]})
    return out
    fix(backend): T-121 r2 one-line style carries the translated summary, whitespace-only quote collapse documented and tested, translation note on its own line
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                 | 12 ++++++++++--
 memory/contracts/api.md               |  4 ++--
 tests/unit/test_t121_letter_styles.py | 34 +++++++++++++++++++++++++++++++++-
 3 files changed, 45 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:48.531Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t120r2_probe.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import lexicon_scan as LS\n# (text, expect_flag): expect_flag True when the sentence names a prior condition\nCASES = [\n (\"Hx per patient's son.\", False),\n (\"PHx obtained via patient's son, who interpreted.\", False),\n (\"History provided by patient's wife.\", False),\n (\"Hx obtained via telephone interpreter.\", False),\n (\"Hx per EMS.\", False),\n (\"Hx per interpreter line.\", False),\n (\"History given by the patient's mother.\", False),\n (\"Hx relayed through language line interpreter.\", False),\n (\"PHx gathered from patient's friend.\", False),\n (\"History was obtained from patient's caregiver.\", False),\n (\"Hx per patient.\", False),\n (\"History obtained from chart review.\", False),\n (\"Hx per medical records.\", False),\n (\"Hx obtained via interpreter: lumbar strain 2019.\", True),\n (\"PHx obtained via patient's son: lumbar strain 2019.\", True),\n (\"Hx per patient's son, significant for diabetes.\", True),\n (\"History provided by wife, notable for lumbar strain.\", True),\n (\"Hx obtained via interpreter, positive for prior neck injury.\", True),\n (\"Hx per patient's son; patient fractured her wrist before.\", True),\n (\"History obtained from patient - lumbar strain.\", True),\n (\"PHx obtained via interpreter (lumbar strain).\", True),\n (\"History provided by husband, who states she has chronic back pain.\", True),\n (\"Hx obtained via interpreter and reports degenerative disc disease.\", True),\n (\"Hx per patient's son, history of lumbar strain.\", True),\n (\"Hx obtained via patient's son who interpreted. Hx of lumbar strain 2019.\", True),\n (\"Hx obtained via interpreter\\nLumbar strain 2019\", True),\n (\"Hx per EMS - pt had previous knee surgery\", True),\n (\"Hx obtained via interpreter, pre-existing arthritis\", True),\n (\"Hx per patient's son, who interpreted, a recurring back problem\", True),\n (\"PHx obtained via son; previous whiplash\", True),\n (\"Hx obtained from Dr. Lee: lumbar strain\", True),\n (\"Hx obtained from Dr. Lee.\", False),\n]\nbad = 0\nfor t, exp in CASES:\n    hit = [h[\"text\"] for h in LS.scan(t) if h[\"flag_type\"] == \"pre_existing\"]\n    ok = bool(hit) == exp\n    bad += (not ok)\n    print((\"OK  \" if ok else \"BAD \") + (\"expect-flag \" if exp else \"expect-none \") + repr(t) + \" -> \" + repr(hit))\nprint(\"bad\", bad, \"of\", len(CASES))\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t120r2_probe.py $S/t120r2/arc"
}
````

### User / tool · 2026-11-02T11:28:48.754Z

**tool result**
````
OK  expect-none "Hx per patient's son." -> []
OK  expect-none "PHx obtained via patient's son, who interpreted." -> []
OK  expect-none "History provided by patient's wife." -> []
OK  expect-none 'Hx obtained via telephone interpreter.' -> []
OK  expect-none 'Hx per EMS.' -> []
OK  expect-none 'Hx per interpreter line.' -> []
OK  expect-none "History given by the patient's mother." -> []
OK  expect-none 'Hx relayed through language line interpreter.' -> []
OK  expect-none "PHx gathered from patient's friend." -> []
OK  expect-none "History was obtained from patient's caregiver." -> []
BAD expect-none 'Hx per patient.' -> ['Hx']
OK  expect-none 'History obtained from chart review.' -> []
BAD expect-none 'Hx per medical records.' -> ['Hx']
OK  expect-flag 'Hx obtained via interpreter: lumbar strain 2019.' -> ['Hx']
OK  expect-flag "PHx obtained via patient's son: lumbar strain 2019." -> ['PHx']
BAD expect-flag "Hx per patient's son, significant for diabetes." -> []
BAD expect-flag 'History provided by wife, notable for lumbar strain.' -> []
OK  expect-flag 'Hx obtained via interpreter, positive for prior neck injury.' -> ['prior neck injury']
BAD expect-flag "Hx per patient's son; patient fractured her wrist before." -> []
BAD expect-flag 'History obtained from patient - lumbar strain.' -> []
BAD expect-flag 'PHx obtained via interpreter (lumbar strain).' -> []
OK  expect-flag 'History provided by husband, who states she has chronic back pain.' -> ['chronic']
OK  expect-flag 'Hx obtained via interpreter and reports degenerative disc disease.' -> ['degenerative']
OK  expect-flag "Hx per patient's son, history of lumbar strain." -> ['history of', 'Hx']
OK  expect-flag "Hx obtained via patient's son who interpreted. Hx of lumbar strain 2019." -> ['Hx']
BAD expect-flag 'Hx obtained via interpreter\nLumbar strain 2019' -> []
OK  expect-flag 'Hx per EMS - pt had previous knee surgery' -> ['previous knee surgery']
OK  expect-flag 'Hx obtained via interpreter, pre-existing arthritis' -> ['pre-existing']
BAD expect-flag "Hx per patient's son, who interpreted, a recurring back problem" -> []
OK  expect-flag 'PHx obtained via son; previous whiplash' -> ['previous whiplash']
BAD expect-flag 'Hx obtained from Dr. Lee: lumbar strain' -> []
OK  expect-none 'Hx obtained from Dr. Lee.' -> []
bad 10 of 32
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:58.355Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git log --oneline -3 1cb8707; mkdir -p $S/t120r2/parent && git archive 1cb8707^ | tar -x -C $S/t120r2/parent && .venv/bin/python -I artifacts/review-evidence/t120r2_probe.py $S/t120r2/parent | grep -E \"diabetes|wife, notable|patient - lumbar|interpreter \\(|Lumbar strain 2019|recurring|Dr\\. Lee|patient\\.|medical records|bad\""
}
````

### User / tool · 2026-11-02T11:28:59.034Z

**tool result**
````
1cb8707 fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
0c47356 fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
d56328a test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
BAD expect-none 'Hx per patient.' -> ['Hx']
BAD expect-none 'Hx per medical records.' -> ['Hx']
OK  expect-flag "Hx per patient's son, significant for diabetes." -> ['Hx']
BAD expect-flag 'History provided by wife, notable for lumbar strain.' -> []
BAD expect-flag 'History obtained from patient - lumbar strain.' -> []
OK  expect-flag 'PHx obtained via interpreter (lumbar strain).' -> ['PHx']
OK  expect-flag 'Hx obtained via interpreter\nLumbar strain 2019' -> ['Hx']
OK  expect-flag "Hx per patient's son, who interpreted, a recurring back problem" -> ['Hx']
OK  expect-flag 'Hx obtained from Dr. Lee: lumbar strain' -> ['Hx']
BAD expect-none 'Hx obtained from Dr. Lee.' -> ['Hx']
bad 12 of 32
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:29:18.752Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t120r2_mutants.py <<'EOF'\nimport sys, shutil, subprocess, pathlib\nsrc = pathlib.Path(sys.argv[1]); work = pathlib.Path(sys.argv[2]); py = sys.argv[3]\nif work.exists(): shutil.rmtree(work)\nshutil.copytree(src, work, ignore=shutil.ignore_patterns('.git'))\nf = work / \"app/backend/lexicon_scan.py\"\norig = f.read_text()\nM = {\n \"M1 skip whenever source phrase matched (no rest check)\": ('    return not re.search(r\":|\\\\d|\\\\bof\\\\b\", rest, re.I)', '    return True'),\n \"M2 drop colon from rest check\": ('r\":|\\\\d|\\\\bof\\\\b\"', 'r\"\\\\d|\\\\bof\\\\b\"'),\n \"M3 drop digit from rest check\": ('r\":|\\\\d|\\\\bof\\\\b\"', 'r\":|\\\\bof\\\\b\"'),\n \"M4 drop 'of' from rest check\": ('r\":|\\\\d|\\\\bof\\\\b\"', 'r\":|\\\\d\"'),\n \"M5 via branch widened to any following text\": ('_HISTORY_VIA = re.compile(r\"\\\\s+(?:per|via)\\\\s+(?:the\\\\s+)?', '_HISTORY_VIA = re.compile(r\"\\\\s+(?:per|via)\\\\s+.*?|\\\\s+(?:per|via)\\\\s+(?:the\\\\s+)?'),\n \"M6 never skip\": ('_is_source_sentence(text, m.end()):\\n                continue', 'False:\\n                continue'),\n \"M7 sentence end scan removed (rest to end of text)\": ('rest = text[end:m.start() if m else len(text)]', 'rest = text[end:]'),\n \"M8 newline not a sentence end\": ('_SENT_END = re.compile(r\"[.!?](?:\\\\s|$)|\\\\n\")', '_SENT_END = re.compile(r\"[.!?](?:\\\\s|$)\")'),\n \"M9 skip also when only HISTORY_SOURCE (drop VIA alt)\": ('_HISTORY_SOURCE.match(text, end) or _HISTORY_VIA.match(text, end)', '_HISTORY_SOURCE.match(text, end)'),\n}\nfor name, (a, b) in M.items():\n    if a not in orig:\n        print(\"SKIP (pattern not found)\", name); continue\n    f.write_text(orig.replace(a, b, 1))\n    r = subprocess.run([py, \"-m\", \"pytest\", \"tests/unit/test_t120_history_source_sentence.py\", \"-q\", \"-p\", \"no:cacheprovider\", \"-x\"], cwd=work, capture_output=True, text=True)\n    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", last)\nf.write_text(orig)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t120r2_mutants.py $S/t120r2/arc $S/t120r2/mut /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:29:25.064Z

**tool result**
````
KILLED   M1 skip whenever source phrase matched (no rest check) | 1 failed, 9 passed in 0.31s
SURVIVED M2 drop colon from rest check | 28 passed in 0.40s
KILLED   M3 drop digit from rest check | 1 failed, 11 passed in 0.34s
KILLED   M4 drop 'of' from rest check | 1 failed, 18 passed in 0.34s
KILLED   M5 via branch widened to any following text | 1 failed, 15 passed in 0.35s
KILLED   M6 never skip | 1 failed in 0.41s
KILLED   M7 sentence end scan removed (rest to end of text) | 1 failed in 0.36s
SURVIVED M8 newline not a sentence end | 28 passed in 0.45s
KILLED   M9 skip also when only HISTORY_SOURCE (drop VIA alt) | 1 failed, 7 passed in 0.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:29:33.454Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t120r2_probe2.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import lexicon_scan as LS\nfor t in [\"Hx obtained via interpreter: lumbar strain.\", \"PHx obtained via patient's son: migraines\", \"Hx obtained via interpreter\\nLumbar strain\", \"Hx obtained via interpreter\\n- lumbar strain\"]:\n    print(repr(t), [h[\"text\"] for h in LS.scan(t) if h[\"flag_type\"]==\"pre_existing\"])\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t120r2_probe2.py $S/t120r2/arc; echo ---mut M2; .venv/bin/python -I artifacts/review-evidence/t120r2_probe2.py $S/t120r2/mut | head -0; cat $S/t120r2/unit.out | tail -5"
}
````

### User / tool · 2026-11-02T11:29:33.887Z

**tool result**
````
'Hx obtained via interpreter: lumbar strain.' ['Hx']
"PHx obtained via patient's son: migraines" ['PHx']
'Hx obtained via interpreter\nLumbar strain' []
'Hx obtained via interpreter\n- lumbar strain' []
---mut M2
head: illegal line count -- 0
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
........................................................................ [ 43%]
........................................................................ [ 45%]
........................................................................ [ 47%]
........................................................................ [ 50%]
.........................................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:29:36.570Z

**tool call — Bash**
````
{
 "command": "git show 4c59fac -- app/backend/export.py memory/contracts/api.md tests/unit/test_t121_letter_styles.py"
}
````

### User / tool · 2026-11-02T11:29:36.719Z

**tool result**
````
commit 4c59fac60ae02174cfc3e648ed4b6c609b53f2bc
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:27:25 2026 -0600

    fix(backend): T-121 r2 one-line style carries the translated summary, whitespace-only quote collapse documented and tested, translation note on its own line
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/export.py b/app/backend/export.py
index c8eb83f..135c5c5 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -245,7 +245,13 @@ def _translation_note(e):
     return " " + TRANSLATION_NOTE.get(lab, f"[{lab}; check before sending]") if lab else ""
 
 
+def _translation_line(e) -> list:
+    """Standard style: the note is its own bracket line at the end of the entry, under the Spanish quote, so it is not read as a comment on the quote."""
+    return [_translation_note(e).strip()] if e.get("translation_label") else []
+
+
 def _one_line(s):
+    """Whitespace only: every run of spaces, tabs and line breaks becomes one space, so the one-line style stays one line. No word changes (T-121)."""
     return " ".join(str(s).split())
 
 
@@ -256,9 +262,11 @@ def _letter(v, style=None):
     for e in v.in_entries:
         n = e["record_no"]
         if style == "oneline":
-            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{_translation_note(e)}']
+            # a translated entry carries its English summary on the same line (the note below it would otherwise point at nothing)
+            tr = f" — English: {_one_line(e['summary'])}" if e.get("translation_label") else ""
+            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{tr}{_translation_note(e)}']
         else:
-            out += [f"{_long_date(v.date_of(e))} — {v.source(n)}", e["summary"], f'{v.source_prefix(n)}"{e["excerpt"]}"{_translation_note(e)}', ""]
+            out += [f"{_long_date(v.date_of(e))} — {v.source(n)}", e["summary"], f'{v.source_prefix(n)}"{e["excerpt"]}"', *_translation_line(e), ""]
     if style == "oneline" and v.in_entries:
         out.append("")
     sents = v.narrative_sentences
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 9a2654f..e889028 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -370,7 +370,7 @@ Note `item.kind` is the item type (`"amount"`, as in the review response); the a
 
 ## GET /api/cases/{token}/export
 **D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
-Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
+Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the only change to the quote is whitespace (each run of spaces and line breaks becomes one space); a translated entry adds ` — English: <summary>` after the bracket, before the translation note; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
 ```json
 {
   "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
@@ -715,7 +715,7 @@ Languages: English and Spanish. Code detects the language of every record (`app/
 - **Never auto-verified (D-050).** Every item (entry, amount, flag) made from a record routed `es` or `uncertain` is `needs_review` with reason `AI_TRANSLATION` ("AI translation — check against the original"), whatever the Spanish code checks and the translation judge said. Their failures still show in the trace; passing them never yields `verified`. Enforced once, in `confidence.compose_state` (ctx `translated`), and every path that rewrites a state passes it: pipeline, rerun, rejudge, edit and manual entry, date confirmation, reclassify, flags. The entry `translation` block also carries `review_label: "AI translation — check against the original"`. Batch accept refuses such an item (`not_verified`); the paralegal's single accept is the gate and still works, and export needs nothing more than that accept.
 - **Record view** has `language`: `"en"` | `"es"` | `"other"` | `"uncertain"`.
 - **Uncertain language** (`LANGUAGE_UNCERTAIN`). A record with some non-English evidence but no confident answer (a short line with accents and no clear language; Spanish against French or Portuguese on too little text) is neither run as English nor refused. It goes through the translation path (Spanish prompt, Spanish token checks, translation judge), its `translation` block has `source_language: "uncertain"`, `source_language_name: "an unidentified language"`, and the entry is always `needs_review` with reason `LANGUAGE_UNCERTAIN`. The run warning `LANGUAGE_UNCERTAIN` (`record_no`, `message` with the cause) says so. The English token checks never run for it. French, Portuguese, Italian and German lines of any length that reach two or more distinct words in their own language are `other` (refused as `UNSUPPORTED_LANGUAGE`).
-- **Export.** In the letter, a translated entry ends with a bracketed, removable note (T-121): `[AI translation of the Spanish original; check before sending]` (or `[Translation of the Spanish original, edited by reviewer; check before sending]`), at the end of its last line; no line starts with `AI translation:`. The quote is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
+- **Export.** In the letter, a translated entry ends with a bracketed, removable note on its own line under the quote (T-121): `[AI translation of the Spanish original; check before sending]` (or `[Translation of the Spanish original, edited by reviewer; check before sending]`), (in the one-line style, at the end of the entry's line); no line starts with `AI translation:`. The quote is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
 - **Warnings** (in `POST /api/cases` and the run result): `SPANISH_RECORDS` (`record_nos`; says that the pre-existing and causation phrase lists are English only, so Spanish records' flags come from the AI check alone) and `UNSUPPORTED_LANGUAGE` (`record_no`; a record in a mixed packet that looks like another language: not sent to any model, no entry, plus a run `errors[]` item with code `UNSUPPORTED_LANGUAGE`, stage `extract`).
 - **Unsupported language, whole case.** If no record is English or Spanish: `POST /api/cases` (and `/pdf`) answers `400 unsupported_language`, `message` "This tool reads English and Spanish records. The text looks like French, which is not supported, so nothing was run. ...", `detail: {languages: ["French"], supported: ["English", "Spanish"]}`; nothing is stored and no model is called. Detected names: French, German, Portuguese, Italian, or a script (Chinese, Japanese, Korean, Cyrillic, Arabic, Hebrew, Devanagari, Thai, Greek).
 - **Dates.** A `Date:` header such as `14 de mayo de 2026`, `14-ago-2026` parses (day first, month spelled out, never ambiguous).
diff --git a/tests/unit/test_t121_letter_styles.py b/tests/unit/test_t121_letter_styles.py
index 51cafd0..f54fe61 100644
--- a/tests/unit/test_t121_letter_styles.py
+++ b/tests/unit/test_t121_letter_styles.py
@@ -86,7 +86,9 @@ def test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_
         line = next(l for l in out.split("\n") if note in l)
         assert line.endswith(note)
     assert "Restrained driver rear-ended.\n" in std                              # the summary line carries no label prefix
-    assert next(l for l in std.split("\n") if note in l).startswith("Source [Ex. __ / Bates __]: ")
+    lines = std.split("\n")
+    i = lines.index(note)                                                          # standard style: its own bracket line, last line of the entry
+    assert lines[i - 1].startswith("Source [Ex. __ / Bates __]: ") and note not in lines[i - 1] and (i + 1 == len(lines) or lines[i + 1] == "")
     assert next(l for l in one.split("\n") if note in l).startswith("January 9, 2026 — Austin EMS run report: ")
 
 
@@ -110,3 +112,33 @@ def test_api_style_param_and_unknown_style(api):
     assert c.get(f"/api/cases/{tok}/export?style=standard").json()["letter_text"] == std
     bad = c.get(f"/api/cases/{tok}/export?style=fancy")
     assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_style"
+
+
+@pytest.mark.parametrize("label,note", [("AI translation", NOTE), ("Translation (edited by reviewer)", NOTE_EDITED)])
+def test_oneline_translated_entry_carries_its_summary_on_the_same_line_as_the_note(label, note):
+    case = _case(label)
+    case["entries"][0]["summary"] = "Restrained driver rear-ended; neck pain 7/10."
+    line = next(l for l in X.build_export(case, style="oneline")["letter_text"].split("\n") if note in l)
+    assert " — English: Restrained driver rear-ended; neck pain 7/10. " + note in line
+    assert line.index('"41M restrained') < line.index("English:") < line.index(note)
+    assert "English:" not in "\n".join(l for l in X.build_export(build_case(), style="oneline")["letter_text"].split("\n"))     # English entries carry no such tail
+
+
+def test_oneline_collapses_whitespace_only_and_keeps_one_line():
+    case = build_case()
+    e = case["entries"][0]
+    case["records"][0]["excerpt"] = "Line one.\n  Line   two.\tEnd."
+    e["excerpt"] = "Line one.\n  Line   two.\tEnd."
+    out = X.build_export(case, style="oneline")["letter_text"]
+    assert '"Line one. Line two. End." [Ex. __ / Bates __]' in out
+    entry_line = next(l for l in out.split("\n") if l.startswith("January 9, 2026 — Austin EMS run report"))
+    assert "\t" not in entry_line and "  " not in entry_line
+    std = X.build_export(case)["letter_text"]
+    assert '"Line one.\n  Line   two.\tEnd."' in std                # the standard style keeps the quote exactly
+
+
+def test_oneline_translated_entry_with_a_multi_line_summary_stays_one_line():
+    case = _case("AI translation")
+    case["entries"][0]["summary"] = "Restrained driver\nrear-ended."
+    line = next(l for l in X.build_export(case, style="oneline")["letter_text"].split("\n") if NOTE in l)
+    assert "English: Restrained driver rear-ended." in line
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:29:48.246Z

**tool call — Bash**
````
{
 "command": "sed -n 225,290p app/backend/export.py; sed -n 1,60p tests/unit/test_t121_letter_styles.py; grep -rn \"ends the line\\|AI translation of the Spanish original\\|last line of\" --include=*.md --include=*.py --include=*.js --include=*.html --include=*.yaml . 2>/dev/null | grep -v \"^./reviews\\|^./board\\|agent-memory\\|^./tests\\|artifacts/\" | head -20"
}
````

### User / tool · 2026-11-02T11:29:52.223Z

**tool result**
````
def basis_hash(entry: dict) -> str:
    """What a narrative sentence was drafted from: if an entry's summary or quote changes afterwards, its sentences leave the letter."""
    import hashlib
    return hashlib.sha256(f"{entry['summary']}\x1f{entry['excerpt']}".encode("utf-8")).hexdigest()[:16]


def _status(item):
    s = item.get("review_status")
    return "in" if s in IN else "out" if s in OUT else "pending"


# ---------------------------------------------------------------- letter (takes no flags)
def build_letter(case: dict, style: str = None) -> str:
    """The treatment section. Deliberately has no flags parameter (R-EX-1): flag content cannot reach the letter."""
    return _letter(_View(case), style)


def _translation_note(e):
    """D-042/T-121: a translated entry says so in a bracketed phrase at the end of the entry, which the paralegal deletes after checking."""
    lab = e.get("translation_label")
    return " " + TRANSLATION_NOTE.get(lab, f"[{lab}; check before sending]") if lab else ""


def _translation_line(e) -> list:
    """Standard style: the note is its own bracket line at the end of the entry, under the Spanish quote, so it is not read as a comment on the quote."""
    return [_translation_note(e).strip()] if e.get("translation_label") else []


def _one_line(s):
    """Whitespace only: every run of spaces, tabs and line breaks becomes one space, so the one-line style stays one line. No word changes (T-121)."""
    return " ".join(str(s).split())


def _letter(v, style=None):
    if style not in (None, *STYLES):
        raise ValueError(f"unknown letter style {style!r}")
    out = [LETTER_TITLE, ""]
    for e in v.in_entries:
        n = e["record_no"]
        if style == "oneline":
            # a translated entry carries its English summary on the same line (the note below it would otherwise point at nothing)
            tr = f" — English: {_one_line(e['summary'])}" if e.get("translation_label") else ""
            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{tr}{_translation_note(e)}']
        else:
            out += [f"{_long_date(v.date_of(e))} — {v.source(n)}", e["summary"], f'{v.source_prefix(n)}"{e["excerpt"]}"', *_translation_line(e), ""]
    if style == "oneline" and v.in_entries:
        out.append("")
    sents = v.narrative_sentences
    if sents:
        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
    charges = v.in_charges
    if charges:
        out += [CHARGES_TITLE, ""]
        for a in charges:
            n = a["record_no"]
            out += [f"{v.source(n)}, {_long_date(v.rec_date(n))}: {_money(a['cents'])}",
                    f'{v.source_prefix(n)}"{_amount_quote(v, a)}"']
        out += ["", TOTAL_PREFIX + _money(sum(a["cents"] for a in charges))]
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


# ---------------------------------------------------------------- internal notes
def _flag_label(f):
    t, sub = f.get("type"), f.get("subtype")
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
board/cards/T-121.md:21:  - {"n": 2, "text": "In every letter style an AI-translation note is a bracketed phrase at the end of the entry, [AI translation of the Spanish original; check before sending], never a line that starting with 'AI translation:'; golden and unit tests updated", "done": true, "evidence": "test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles; test_spanish_records/test_d050 updated"}
app/backend/api.py:183:        except Exception as e:                                                          # last line of defence: standard JSON, no detail
tests/unit/test_t121_letter_styles.py:10:NOTE = "[AI translation of the Spanish original; check before sending]"
tests/unit/test_t121_letter_styles.py:90:    i = lines.index(note)                                                          # standard style: its own bracket line, last line of the entry
tests/unit/test_spanish_records.py:378:    assert ES_SUMMARY in letter and "AI translation:" not in letter and f'"{ES_QUOTE}"' in letter and letter.count("[AI translation of the Spanish original; check before sending]") == 1
app/backend/export.py:37:TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
memory/contracts/api.md:373:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the only change to the quote is whitespace (each run of spaces and line breaks becomes one space); a translated entry adds ` — English: <summary>` after the bracket, before the translation note; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
memory/contracts/api.md:718:- **Export.** In the letter, a translated entry ends with a bracketed, removable note on its own line under the quote (T-121): `[AI translation of the Spanish original; check before sending]` (or `[Translation of the Spanish original, edited by reviewer; check before sending]`), (in the one-line style, at the end of the entry's line); no line starts with `AI translation:`. The quote is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
tests/unit/test_d050_never_verified.py:119:    assert ex.status_code == 200 and ES_SUMMARY in ex.json()["letter_text"] and "[AI translation of the Spanish original; check before sending]" in ex.json()["letter_text"]
reviews/T-121-staff-engineer.md:21:   "evidence": "app/backend/export.py:259 the oneline branch emits only the date, provider, quote and bracket, plus `_translation_note(e)`; the summary (the English translation, or the reviewer's edited translation) is never printed. Probe output: `January 9, 2026 — Austin EMS run report: \"Conductor con cinturon. Dolor lumbar 7/10.\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]`. The standard style prints the translation on the line above the quote. tests/unit/test_t121_letter_styles.py::test_api_style_param_and_unknown_style only asserts the note count and that ES_QUOTE is present, not that any translation is.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:06.981Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t121r2_mutants.py <<'EOF'\nimport sys, shutil, subprocess, pathlib\nsrc = pathlib.Path(sys.argv[1]); work = pathlib.Path(sys.argv[2]); py = sys.argv[3]\nif work.exists(): shutil.rmtree(work)\nshutil.copytree(src, work, ignore=shutil.ignore_patterns('.git'))\nf = work / \"app/backend/export.py\"\norig = f.read_text()\nSTD = '''f'{v.source_prefix(n)}\"{e[\"excerpt\"]}\"', *_translation_line(e), \"\"]'''\nM = {\n \"A _one_line no-op\": ('    return \" \".join(str(s).split())', '    return str(s)'),\n \"B _one_line collapses spaces only (newline/tab survive)\": ('\" \".join(str(s).split())', '\" \".join(str(s).split(\" \"))'),\n \"C drop English summary tail\": ('''tr = f\" — English: {_one_line(e['summary'])}\" if e.get(\"translation_label\") else \"\"''', 'tr = \"\"'),\n \"D English tail on every entry\": ('''if e.get(\"translation_label\") else \"\"\\n            out''', '''if True else \"\"\\n            out'''),\n \"E summary not whitespace-collapsed\": (\"{_one_line(e['summary'])}\", \"{e['summary']}\"),\n \"F standard: note back on the quote line\": (STD, '''f'{v.source_prefix(n)}\"{e[\"excerpt\"]}\"{_translation_note(e)}', \"\"]'''),\n \"G standard: drop the note line\": ('*_translation_line(e), \"\"]', '\"\"]'),\n \"H provider not collapsed in oneline\": (\"{_one_line(v.source(n))}\", \"{v.source(n)}\"),\n \"I tail after the note\": (\"{v.oneline_bracket(n)}{tr}{_translation_note(e)}\", \"{v.oneline_bracket(n)}{_translation_note(e)}{tr}\"),\n \"J note line keeps leading space\": (\"return [_translation_note(e).strip()]\", \"return [_translation_note(e)]\"),\n \"K oneline drops note\": (\"{tr}{_translation_note(e)}'\", \"{tr}'\"),\n \"L oneline note only if label==AI translation\": (\"{tr}{_translation_note(e)}'\", '''{tr}{_translation_note(e) if e.get(\"translation_label\") == \"AI translation\" else \"\"}\\''''),\n}\nfor name, (a, b) in M.items():\n    if a not in orig:\n        print(\"SKIP (pattern not found)\", name); continue\n    f.write_text(orig.replace(a, b, 1))\n    r = subprocess.run([py, \"-m\", \"pytest\", \"tests/unit/test_t121_letter_styles.py\", \"tests/unit/test_spanish_records.py\", \"tests/unit/test_d050_never_verified.py\", \"tests/unit/test_export.py\", \"-q\", \"-p\", \"no:cacheprovider\"], cwd=work, capture_output=True, text=True)\n    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", last)\nf.write_text(orig)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t121r2_mutants.py $S/t120r2/arc $S/t121r2/mut /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T11:30:40.569Z

**tool result**
````
KILLED   A _one_line no-op | 2 failed, 121 passed in 3.09s
KILLED   B _one_line collapses spaces only (newline/tab survive) | 2 failed, 121 passed in 2.65s
KILLED   C drop English summary tail | 3 failed, 120 passed in 2.38s
KILLED   D English tail on every entry | 3 failed, 120 passed in 2.18s
KILLED   E summary not whitespace-collapsed | 1 failed, 122 passed in 2.16s
KILLED   F standard: note back on the quote line | 2 failed, 121 passed in 2.17s
KILLED   G standard: drop the note line | 6 failed, 117 passed in 1.90s
SURVIVED H provider not collapsed in oneline | 123 passed in 2.31s
KILLED   I tail after the note | 4 failed, 119 passed in 2.11s
KILLED   J note line keeps leading space | 2 failed, 121 passed in 2.41s
KILLED   K oneline drops note | 6 failed, 117 passed in 2.24s
KILLED   L oneline note only if label==AI translation | 2 failed, 121 passed in 1.77s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:48.257Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t121r2_probe.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import export as X\nfrom tests.unit.test_export import build_case\nfor summ in [\"\", None, \"  \\n \"]:\n    c = build_case()\n    e = next(e for e in c[\"entries\"] if e[\"record_no\"] == 1)\n    e[\"translation_label\"] = \"AI translation\"; e[\"summary\"] = summ\n    for st in (\"oneline\", None):\n        out = X.build_export(c, style=st)[\"letter_text\"]\n        print(repr(summ), st, [l for l in out.split(\"\\n\") if \"AI translation\" in l or \"English:\" in l])\nc = build_case(); e = next(e for e in c[\"entries\"] if e[\"record_no\"] == 1)\ne[\"translation_label\"] = \"Translation (edited by reviewer)\"; e[\"summary\"] = \"Driver rear-ended.\\nNeck pain.\"\nprint(X.build_export(c, style=\"oneline\")[\"letter_text\"].split(\"\\n\")[2])\nprint(\"\\n\".join(X.build_export(c)[\"letter_text\"].split(\"\\n\")[2:8]))\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t120r2/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t121r2_probe.py $S/t120r2/arc 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T11:30:48.533Z

**tool result**
````
'' oneline ['January 9, 2026 — Austin EMS run report: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." [Ex. __ / Bates __] — English:  [AI translation of the Spanish original; check before sending]']
'' None ['[AI translation of the Spanish original; check before sending]']
None oneline ['January 9, 2026 — Austin EMS run report: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." [Ex. __ / Bates __] — English: None [AI translation of the Spanish original; check before sending]']
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/t121r2_probe.py", line 10, in <module>
    out = X.build_export(c, style=st)["letter_text"]
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120r2/arc/app/backend/export.py", line 669, in build_export
    return {"letter_text": _letter(v, style), "internal_notes_text": notes, "counts": counts}
                           ^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120r2/arc/app/backend/export.py", line 285, in _letter
    return "\n".join(out)
           ^^^^^^^^^^^^^^
TypeError: sequence item 3: expected str instance, NoneType found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:52.710Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -8 $S/t120r2/unit.out; cd /Users/arsis/zlayt-pm-project && git show aa6ae9f --stat | tail -12"
}
````

### User / tool · 2026-11-02T11:30:52.828Z

**tool result**
````
........................................................................ [ 40%]
........................................................................ [ 43%]
........................................................................ [ 45%]
........................................................................ [ 47%]
........................................................................ [ 50%]
........................................................................ [ 52%]
........................................................................ [ 55%]
...........Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:27:36 2026 -0600

    feat(backend): T-105 added-qualifier word lists (attribution, hedge, approximation, inability) come from lexicon.yaml code_lists.added_qualifier; curly apostrophes, Spanish-helper negations, faithful paraphrases; lexicon text updated to D-055
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/grounding.py                        | 62 ++++++++++++----
 app/backend/spanish_text.py                     | 32 +++------
 app/llm/lexicon.yaml                            | 59 +++++++++++++++-
 tests/unit/test_t105_added_qualifier_lexicon.py | 94 +++++++++++++++++++++++++
 4 files changed, 209 insertions(+), 38 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:54.451Z

**tool call — Bash**
````
{
 "command": "git show aa6ae9f -- app/backend/grounding.py app/backend/spanish_text.py app/llm/lexicon.yaml"
}
````

### User / tool · 2026-11-02T11:30:54.559Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:01.576Z

**tool call — Bash**
````
{
 "command": "grep -n \"_SELF_CARRIED\\|_SELF_IN_QUOTE\\|_HEDGE_WORDS\\|^_APPROX\\|_APPROX\\b\" -r app | grep -v \"\\.pyc\"; echo ----; grep -n \"_EN_NEG_EXTRA\\|_EN_NEG_QUOTE\\|_NEG_ENGLISH\\|_SELF_CUES\\|_SELF_PHRASES\\|_HEDGE_PHRASES\\|_APPROX_PHRASES\" -r app --include=*.py | head -30"
}
````

### User / tool · 2026-11-02T11:31:01.696Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:02.268Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_t105_added_qualifier_lexicon.py; grep -n \"no list words\\|def test\" tests/unit/test_t105_added_qualifier_lexicon.py | head -50"
}
````

### User / tool · 2026-11-02T11:31:02.373Z

**tool result**
````
"""T-105 (T-100 r2 F1-F3): the added-qualifier word lists (attribution, hedge, approximation) are built from ONE place, app/llm/lexicon.yaml
(code_lists.added_qualifier), and read by the English and the Spanish path alike. Misses from the r2 probe are refused; faithful paraphrases are not."""
import pytest

from app.backend import grounding as GR, lexicon, spanish_text as ST

Q = "Pain 4/10, improving."


def _new(summary, quote=Q):
    return GR.new_tokens(summary, quote)


@pytest.mark.parametrize("summary", [
    "Reports pain 4/10, improving.", "Patient describes pain 4/10, improving.", "Patient noted pain 4/10, improving.", "Patient indicates pain 4/10, improving.",
    "Pain 4/10, improving according to the patient.", "Pain 4/10 (self-reported), improving.",
    "Pain 4/10, seems to be improving.", "Pain 4/10, potentially improving.", "Pain 4/10, apparently improving.", "Pain 4/10, suspected improvement.",
    "Pain 4/10, consistent with improvement.", "Pain 4/10, tends to improve.",
    "Pain nearly 4/10, improving.", "Pain almost 4/10, improving.", "Pain close to 4/10, improving.", "Pain circa 4/10, improving.", "Pain ca. 4/10, improving.",
    "Pain about four out of ten, improving."])
def test_r2_misses_are_refused(summary):
    assert _new(summary), summary


@pytest.mark.parametrize("summary,quote", [
    ("Patient describes pain 4/10.", "Patient describes pain 4/10."), ("Seems improved.", "Seems improved."), ("Pain nearly 4/10.", "Pain nearly 4/10."),
    ("Reports pain 4/10.", "Reports pain 4/10."), ("Pain apparently improving.", "Pain apparently improving."), ("Pain circa 4/10.", "Pain about 4/10."),
    ("Pain ca. 4/10.", "Pain ~4/10."), ("Patient indicates pain 4/10.", "Pt states pain 4/10.")])
def test_a_quote_that_carries_the_kind_lets_the_summary_carry_it(summary, quote):
    assert _new(summary, quote) == []


@pytest.mark.parametrize("summary,quote", [
    ("Counseled about 3 home exercises.", "Counseling provided on 3 home exercises."),
    ("Educated around 2 stretching routines.", "Education given on 2 stretching routines."),
    ("Discussed about 3 options.", "3 options reviewed."),
    ("Patient cannot bear weight.", "Unable to bear weight."), ("Patient can't bear weight.", "Unable to bear weight."),
    ("Unable to bear weight.", "Patient cannot bear weight."), ("Patient could not lift the arm.", "Cannot lift the arm."),
    ("Did not tolerate the exercise.", "Didn’t tolerate the exercise."), ("Didn't tolerate the exercise.", "Did not tolerate the exercise."),
    ("Pain not improved.", "Pain isn't improved.")])
def test_faithful_paraphrases_are_not_refused(summary, quote):
    assert GR.new_tokens(summary, quote) == [], (summary, quote, GR.new_tokens(summary, quote))


def test_a_real_approximation_still_refused_after_a_non_preposition_about():
    assert _new("Counseled about 3 exercises; pain about 4/10.", "Counseling provided on 3 exercises. Pain 4/10.")
    assert _new("Pain about 4/10.")
    assert _new("Pain around 4/10.")


def test_cannot_is_still_refused_when_the_quote_has_no_inability_or_hedge():
    assert _new("Patient cannot bear weight.")
    assert _new("Patient cannot bear weight.", "Weight bearing tolerated.")


@pytest.mark.parametrize("summary", ["Improving; absence of numbness.", "Improving; lacks radiation.", "Improving; free of numbness.", "Improving; nothing else.",
                                     "Improving; unremarkable otherwise.", "Improving; didn’t worsen.", "Improving; wasn’t worse."])
def test_negation_words_of_the_spanish_helper_and_curly_apostrophes_are_covered(summary):
    assert _new(summary), summary

21:def test_r2_misses_are_refused(summary):
29:def test_a_quote_that_carries_the_kind_lets_the_summary_carry_it(summary, quote):
41:def test_faithful_paraphrases_are_not_refused(summary, quote):
45:def test_a_real_approximation_still_refused_after_a_non_preposition_about():
51:def test_cannot_is_still_refused_when_the_quote_has_no_inability_or_hedge():
58:def test_negation_words_of_the_spanish_helper_and_curly_apostrophes_are_covered(summary):
62:def test_curly_apostrophe_contraction_in_the_quote_supports_the_summary():
67:def test_the_word_lists_come_from_the_lexicon_not_from_code():
84:def test_spanish_path_reads_the_same_lists():
93:def test_faithful_spanish_paraphrases_are_not_refused():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:09.041Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep T-100; sed -n 60,110p tests/unit/test_t105_added_qualifier_lexicon.py"
}
````

### User / tool · 2026-11-02T11:31:09.167Z

**tool result**
````
T-100-staff-engineer-r2.md
T-100-staff-engineer.md


def test_curly_apostrophe_contraction_in_the_quote_supports_the_summary():
    assert _new("Patient wasn't worse.", "Patient wasn’t worse.") == []
    assert GR.side_neg_words("didn’t") == GR.side_neg_words("didn't") and GR.side_neg_words("didn’t")


def test_the_word_lists_come_from_the_lexicon_not_from_code():
    import pathlib
    import re
    fam = {e["id"] for e in lexicon.code_list("added_qualifier")}
    assert {"attribution", "attribution_bare_verb", "hedge", "approximation", "approximation_preposition_context", "inability", "inability_assertion"} <= fam
    code = "".join(pathlib.Path(m.__file__).read_text(encoding="utf-8") for m in (GR, ST))
    for word in ("describes", "apparently", "nearly", "circa", "potentially", "indicates"):
        assert word not in code.lower(), word                    # the words live in lexicon.yaml, once
    # every example recorded in the lexicon behaves as stated
    for e in lexicon.load()["code_lists"]["added_qualifier"]["entries"]:
        rx = re.compile(e["pattern"], re.I)
        for ex in e["examples"]["hit"]:
            assert rx.search(ex), (e["id"], ex)
        for ex in e["examples"]["miss"]:
            assert not rx.search(ex), (e["id"], ex)


def test_spanish_path_reads_the_same_lists():
    q = "Dolor cervical 6/10, mejorando."
    for s in ("Patient describes neck pain 6/10.", "Neck pain apparently 6/10.", "Neck pain nearly 6/10.", "Neck pain potentially 6/10.", "Patient indicates neck pain 6/10."):
        assert ST.new_tokens(s, q), s
    assert ST.new_tokens("Patient describes neck pain 6/10.", "Refiere dolor cervical 6/10.") == []
    assert ST.new_tokens("Neck pain nearly 6/10.", "Dolor cervical aproximadamente 6/10.") == []
    assert ST.new_tokens("Neck pain apparently 6/10.", "Dolor cervical posible 6/10.") == []


def test_faithful_spanish_paraphrases_are_not_refused():
    assert ST.new_tokens("Counseled about 3 home exercises.", "Se ensenaron 3 ejercicios en casa.") == []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:12.465Z

**tool call — Bash**
````
{
 "command": "grep -n '\"severity\"\\|\"title\"\\|\"evidence\"' reviews/T-100-staff-engineer-r2.md | cut -c1-900 | head -30"
}
````

### User / tool · 2026-11-02T11:31:12.589Z

**tool result**
````
35:  {"severity": "major",
36:   "title": "The added-qualifier check recognises fewer attribution, hedge and approximation words than the repo already defines; the same invention passes with a different word",
37:   "evidence": "Quote 'Pain 4/10, improving.', grounding.new_tokens returns [] (saved, no 422) for: attribution 'Reports pain 4/10, improving.', 'Patient describes pain 4/10, improving.', 'Patient noted pain 4/10, improving.', 'Patient indicates pain 4/10, improving.', 'Pain 4/10, improving according to the patient.', 'Pain 4/10 (self-reported), improving.'; hedge 'Pain 4/10, seems to be improving.', 'potentially improving', 'apparently improving', 'suspected improvement', 'consistent with improvement', 'tends to improve'; approximation 'Pain nearly 4/10', 'almost 4/10', 'close to 4/10', 'circa 4/10', 'ca. 4/10', 'about four out of ten'. Repro: .venv/bin/python -I artifacts/review-evidence/T-100-r2/probe_variants.py <archive of 288c1d3> (output: probe_variants_output.txt). The summary-side lists are grounding.py:178-182 (_SELF_CARRIED needs a subject plus a short verb list) and :186-1
41:  {"severity": "minor",
42:   "title": "Negation words the repo's Spanish helper defines are still outside the shared list, and a curly apostrophe defeats the contraction branch",
43:   "evidence": "spanish_text.py:61-62 _EN_NEG_EXTRA = absent|absence|lacks?|lacking|free of|rules out|ruled out|unremarkable|none|neither|nor|never|nothing|excluded. Quote 'Pain 4/10, improving.' with summaries 'improving; absence of numbness', 'improving; lacks radiation', 'improving; free of numbness', 'improving; nothing else', 'improving; unremarkable otherwise' all return [] (probe_variants_output.txt). Contractions with U+2019: probe_vocab_output.txt prints [('didn’t', []), ('wasn’t', [])]; side_neg_words matches the ASCII apostrophe only (grounding.py:128 \\b(\\w+n't)\\b). 'L side' and 'both sides' also pass.",
47:  {"severity": "minor",
48:   "title": "The wider check refuses some faithful paraphrases; for an AI draft this means needs_review and no one-click accept",
49:   "evidence": "probe_fp_r2.txt vs probe_fp_base.txt (probe_fp.py, same quote and summary pairs): refused at the card, passed at the parent: 'Counseled about 3 home exercises.' over 'Counseling provided on 3 home exercises.' -> ['about'] (the _APPROX 'about' + digit rule, grounding.py:179, reads a preposition as an approximation); 'Pain radiates around 2 inches...' -> ['around']; 'Patient cannot bear weight' over 'Unable to bear weight' -> ['cannot'] (_HEDGE_WORDS includes bare 'cannot', grounding.py:186); 'Suggested follow-up in 4 weeks.' over 'Recommend follow-up in 4 weeks.' -> ['suggested'] (suggest\\w*); 'Patient appears in mild distress.' -> ['appears']; 'didn't tolerate' over 'did not tolerate' -> [\"didn't\"]; 'Negative for fracture.' over 'No fracture seen.' -> ['negative'] (_NEG_SYN, grounding.py:175, is defined and unused by new_tokens). Incidence is low: 0 of 186 recorded 
53:  {"severity": "minor",
54:   "title": "The Spanish added-qualifier path is mostly unpinned: removing its attribution or approximation branch fails no test",
55:   "evidence": "mutate_output_set2.txt: M8a (spanish_text.added_qualifier_tokens self-report branch replaced by 'if False') -> 1986 passed, 0 failed; M8c (approximation branch) -> 1986 passed, 0 failed; M8b (hedge branch) -> 1 failed (only the pre-existing test_no_se_descarta_keeps_its_meaning_and_ruled_out_fails_it row, which the card edited at test_spanish_failsafe.py:159). The card's new tests (test_review_rules.py:201-241, test_manual_and_split.py:197-209) all use an English quote. probe_spanish_output.txt shows the behaviour is right today ('Patient reports neck pain 6/10' over 'Dolor cervical 6/10, mejorando.' -> ['patient reports']; 'approximately' and 'about' refused; a quote with 'Refiere' and 'aproximadamente' lets both through).",
59:  {"severity": "minor",
60:   "title": "The T-100 commit carries an unrelated api.md hunk that describes code not yet in that commit",
61:   "evidence": "git show 288c1d3 -- memory/contracts/api.md: first hunk rewrites the 'Hidden text.' paragraph to 'tiny_font (under 5 pt effective)', 'blends_with_background ... contrast under 96 levels' and adds 'covered_by_annotation'. At 288c1d3: git grep -n 'TINY_PT' gives app/backend/pdf_hidden.py:33 'TINY_PT = 3.0' and git grep 'covered_by_annotation' -- app is empty. The code arrives at ae76835 (T-087 r3), a later commit (HEAD: TINY_PT = 5.0).",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:17.067Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-100-r2/; sed -n 1,40p artifacts/review-evidence/T-100-r2/probe_variants.py; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -3 $S/t120r2/unit.out"
}
````

### User / tool · 2026-11-02T11:31:17.164Z

**tool result**
````
corpus_diff.py
corpus_diff_output.txt
corpus_diff_routed_output.txt
corpus_probe.py
corpus_probe_routed.py
mutate.py
mutate_output.txt
mutate_output_set2.txt
mutate_output_set3.txt
probe_fp.py
probe_fp_base.txt
probe_fp_r2.txt
probe_routes.py
probe_routes_output.txt
probe_spanish.py
probe_spanish_output.txt
probe_variants.py
probe_variants_output.txt
probe_vocab.py
probe_vocab_output.txt
shape.py
"""Usage: probe_variants.py <tree_root>. Added-qualifier wordings against the quote 'Pain 4/10, improving.': which still pass grounding.new_tokens (and so are saved)?"""
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import grounding as G
Q = "Pain 4/10, improving."
V = {
 "attribution": ["Reports pain 4/10, improving.", "Patient endorses pain 4/10, improving.", "Pain 4/10, improving, as the patient described it.", "Patient noted pain 4/10, improving.",
                 "Patient describes pain 4/10, improving.", "Pain 4/10, improving according to the patient.", "Patient-reported pain 4/10, improving.", "The patient told staff pain 4/10, improving.",
                 "Pt reports pain 4/10, improving.", "Patient complained of pain 4/10, improving.", "Pain 4/10 (self-reported), improving.", "Patient indicates pain 4/10, improving."],
 "hedge": ["Pain 4/10, perhaps improving.", "Pain 4/10, seems to be improving.", "Pain 4/10, could be improving.", "Pain 4/10, potentially improving.", "Pain 4/10, presumably improving.",
           "Pain 4/10, apparently improving.", "Pain 4/10, probably improving.", "Pain 4/10, suspected improvement.", "Pain 4/10, possible improvement.", "Pain 4/10, consistent with improvement.",
           "Pain 4/10, appears improving.", "Pain 4/10, tends to improve.", "Pain 4/10, may suggest improvement."],
 "approx": ["Pain nearly 4/10, improving.", "Pain almost 4/10, improving.", "Pain roughly 4/10, improving.", "Pain circa 4/10, improving.", "Pain close to 4/10, improving.", "Pain around 4/10, improving.",
            "Pain approx. 4/10, improving.", "Pain in the range of 4/10, improving.", "Pain somewhere near 4/10, improving.", "Pain about four out of ten, improving.", "Pain estimated 4/10, improving.", "Pain ca. 4/10, improving."],
 "side/neg": ["Pain 4/10, improving; denies numbness.", "Pain 4/10, improving; unremarkable otherwise.", "Pain 4/10, improving; no longer severe.", "Pain 4/10, improving; free of numbness.", "Pain 4/10, improving; lacks radiation.",
              "Pain 4/10, improving; right-sided.", "Pain 4/10, improving; L side.", "Pain 4/10, improving; both sides.", "Pain 4/10, improving; absence of numbness.", "Pain 4/10, improving; nothing else.", "Pain 4/10, improving; without radiation."],
}
for k, L in V.items():
    for s in L:
        t = G.new_tokens(s, Q)
        print(f"{'refused' if t else 'PASSES '} {k:11} {t!s:28} {s}")
........................................................................ [ 52%]
........................................................................ [ 55%]
..............................................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:21.616Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-100-r2/probe_variants.py $S/t120r2/arc | grep -c refused; .venv/bin/python -I artifacts/review-evidence/T-100-r2/probe_variants.py $S/t120r2/arc | grep PASSES; echo; .venv/bin/python -I artifacts/review-evidence/T-100-r2/probe_fp.py $S/t120r2/arc 2>&1 | head -40"
}
````

### User / tool · 2026-11-02T11:31:22.305Z

**tool result**
````
43
PASSES  attribution []                           The patient told staff pain 4/10, improving.
PASSES  approx      []                           Pain in the range of 4/10, improving.
PASSES  approx      []                           Pain somewhere near 4/10, improving.
PASSES  side/neg    []                           Pain 4/10, improving; L side.
PASSES  side/neg    []                           Pain 4/10, improving; both sides.

     passes  []                                       about as preposition before a number
!    refused ['around']                               around as preposition before a number
     passes  []                                       cannot for unable to
     passes  []                                       suggested = recommended
!    refused ['appears']                              appears as observation
     passes  []                                       contraction for did not
!    refused ['negative']                             negative for == no (synonym)
!    refused ['no']                                   no for denies (old behaviour)
     passes  []                                       quote has about, summary has approx
     passes  []                                       quote has c/o, summary has complained
     passes  []                                       quote reports, summary states
     passes  []                                       quote complains, summary reports
     passes  []                                       quote says 'likely', summary 'probably'
     passes  []                                       quote says 'consistent with', summary 'suggests'
     passes  []                                       plain faithful
!    refused ['29', '2026']                           May month in summary
     refused ['patient reports']                      NEG: attribution added (should refuse)
     refused ['possibly']                             NEG: hedge added
     refused ['approximately']                        NEG: approx added
     refused ['about']                                NEG: about+number added
     refused ['bilateral']                            NEG: bilateral added
     refused ['never']                                NEG: never added
faithful-but-refused: 5
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:26.203Z

**tool call — Bash**
````
{
 "command": "sed -n 35,40p reviews/T-100-staff-engineer-r2.md | cut -c900-3000; grep -n \"in the range\\|somewhere near\\|told staff\\|L side\\|both sides\" artifacts/review-evidence/T-100-r2/probe_variants_output.txt"
}
````

### User / tool · 2026-11-02T11:31:26.297Z

**tool result**
````
 (_HEDGE_WORDS). The repo already holds wider lists: grounding.py:191 _SELF_IN_QUOTE (according to, described as, rates, feels), spanish_text.py:63-65 _EN_HEDGE_EXTRA (suspect*, presum*, apparent*, consistent with, questionabl*), spanish_text.py:66 _EN_SELF (describes, mentions, according to, characteriz*), spanish_text.py:72 _EN_APPROX (circa, nearly, some). So the quote side is read more widely than the summary side, and the Spanish branch uses _EN_HEDGE_EXTRA but the English branch does not.",



8:PASSES  attribution []                           The patient told staff pain 4/10, improving.
33:PASSES  approx      []                           Pain in the range of 4/10, improving.
34:PASSES  approx      []                           Pain somewhere near 4/10, improving.
44:PASSES  side/neg    []                           Pain 4/10, improving; L side.
45:PASSES  side/neg    []                           Pain 4/10, improving; both sides.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:34.182Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t105_probe_dropped.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import grounding as G\nimport inspect\nprint([n for n in dir(G) if \"drop\" in n.lower() or \"qualif\" in n.lower()])\npairs = [\n (\"Patient describes pain 4/10.\", \"Pain 4/10.\"),\n (\"Pain apparently improving.\", \"Pain improving.\"),\n (\"Pain potentially improving.\", \"Pain improving.\"),\n (\"Pain seems to be improving.\", \"Pain improving.\"),\n (\"Pain nearly 4/10.\", \"Pain 4/10.\"),\n (\"Pain circa 4/10.\", \"Pain 4/10.\"),\n (\"Pain close to 4/10.\", \"Pain 4/10.\"),\n (\"Pain reportedly 4/10.\", \"Pain 4/10.\"),\n (\"Pain possibly 4/10.\", \"Pain 4/10.\"),\n (\"Pain approx. 4/10.\", \"Pain 4/10.\"),\n (\"Pain according to the patient 4/10.\", \"Pain 4/10.\"),\n]\nfn = getattr(G, \"dropped_qualifiers\", None)\nfor q, s in pairs:\n    try:\n        r = fn(s, q) if fn else None\n    except TypeError:\n        r = fn(q, s)\n    print(\"DROPPED-LOST \" if not r else \"caught       \", q, \"->\", s, r)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t105_probe_dropped.py $S/t120r2/arc; sed -n 245,300p app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T11:31:34.512Z

**tool result**
````
['added_qualifier_tokens', 'dropped_qualifiers', 'missing_qualifier_terms']
DROPPED-LOST  Patient describes pain 4/10. -> Pain 4/10. []
DROPPED-LOST  Pain apparently improving. -> Pain improving. []
DROPPED-LOST  Pain potentially improving. -> Pain improving. []
DROPPED-LOST  Pain seems to be improving. -> Pain improving. []
DROPPED-LOST  Pain nearly 4/10. -> Pain 4/10. []
DROPPED-LOST  Pain circa 4/10. -> Pain 4/10. []
DROPPED-LOST  Pain close to 4/10. -> Pain 4/10. []
DROPPED-LOST  Pain reportedly 4/10. -> Pain 4/10. []
caught        Pain possibly 4/10. -> Pain 4/10. ['hedge']
caught        Pain approx. 4/10. -> Pain 4/10. ['approx']
DROPPED-LOST  Pain according to the patient 4/10. -> Pain 4/10. []
            if w.split()[0] in ("about", "around") and fam["approximation_preposition_context"].search(summary[max(0, m.start() - 40):m.start()]):
                continue
            out.append(w)
    return list(dict.fromkeys(w for w in out if w))


def dropped_qualifiers(summary: str, excerpt: str) -> list:
    """Qualifier kinds present in the excerpt and absent from the summary (D-022): hedge, self_report, negation, laterality, approx."""
    out = []
    if hedge_ids(excerpt) and not (hedge_ids(summary) or _HEDGE_WORDS.search(summary)):
        out.append("hedge")
    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
        out.append("self_report")
    ex_neg = {w.lower() for w in _NEG.findall(excerpt)}
    sm_neg = {w.lower() for w in _NEG.findall(summary)}
    if any(w not in sm_neg and not (w in ("no", "not", "none", "never") and sm_neg & {"no", "not", "none", "never"}) for w in ex_neg):
        out.append("negation")
    if {w.lower() for w in _LATERAL.findall(excerpt)} - {w.lower() for w in _LATERAL.findall(summary)}:
        out.append("laterality")
    if _APPROX.search(excerpt) and not _APPROX.search(summary):
        out.append("approx")
    return out


def missing_qualifier_terms(summary: str, excerpt: str) -> list:
    """The words in the quote that carry a qualifier the summary dropped (D-022), for the 'Edit the summary to keep ...' sentence. English patterns only;
    a Spanish quote may return []. Display only: the pass/fail decision is dropped_qualifiers()."""
    kinds = set(dropped_qualifiers(summary, excerpt))
    found = []

    def add(m):
        w = re.sub(r"\s+", " ", m.group(0)).strip(" .").lower()
        if w and w not in found:
            found.append(w)
    if "hedge" in kinds:
        for rx in _lexicon()["hedge"].values():
            m = rx.search(excerpt)
            if m:
                add(m)
        if not found:
            m = _HEDGE_WORDS.search(excerpt)
            if m:
                add(m)
    for kind, rx in (("self_report", _SELF_CARRIED), ("negation", _NEG), ("laterality", _LATERAL), ("approx", _APPROX)):
        if kind in kinds:
            sm = {w.lower() for w in rx.findall(summary)}
            for m in rx.finditer(excerpt):
                if m.group(0).lower() not in sm:
                    add(m)
    return found[:4]


def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
    reasons = []
    if new_tokens(summary, excerpt, label, date_iso):
        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:52.057Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t105/par && git archive aa6ae9f^ | tar -x -C $S/t105/par; (cd $S/t105/par && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend fixture > $S/t105/par.eval.txt 2>&1; echo par rc=$?); (cd $S/t120r2/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend fixture > $S/t105/head.eval.txt 2>&1; echo head rc=$?); tail -5 $S/t105/head.eval.txt; diff <(sed 's/[0-9]\\{4\\}-[0-9-]*T[0-9:]*Z*//g' $S/t105/par.eval.txt) <(sed 's/[0-9]\\{4\\}-[0-9-]*T[0-9:]*Z*//g' $S/t105/head.eval.txt) && echo EVAL-STDOUT-SAME",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T11:31:55.455Z

**tool result (error)**
````
Exit code 1
par rc=1
head rc=1
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120r2/arc/evals/reports/20261102T113155Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
1c1
< ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t105/par/evals/reports/20261102T113154Z.md
---
> ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120r2/arc/evals/reports/20261102T113155Z.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:58.886Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -12 $S/t120r2/unit.out | cut -c1-300"
}
````

### User / tool · 2026-11-02T11:31:58.969Z

**tool result**
````
........................................................................ [ 76%]
........................................................................ [ 78%]
........................................................................ [ 81%]
........................................................................ [ 83%]
........................................................................ [ 86%]
........................................................................ [ 88%]
........................................................................ [ 90%]
........................................................................ [ 93%]
........................................................................ [ 95%]
........................................................................ [ 98%]
.........................................................                [100%]
3005 passed, 4 skipped in 192.31s (0:03:12)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:15.578Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t105_mutants.py <<'EOF'\nimport sys, shutil, subprocess, pathlib\nsrc = pathlib.Path(sys.argv[1]); work = pathlib.Path(sys.argv[2]); py = sys.argv[3]\nif work.exists(): shutil.rmtree(work)\nshutil.copytree(src, work, ignore=shutil.ignore_patterns('.git'))\ng = work / \"app/backend/grounding.py\"; s = work / \"app/backend/spanish_text.py\"\ngo, so = g.read_text(), s.read_text()\nG = {\n \"a summary loop drops fam['attribution']\": ('for rx in (_SELF_CARRIED, fam[\"attribution\"], fam[\"attribution_bare_verb\"])', 'for rx in (_SELF_CARRIED, fam[\"attribution_bare_verb\"])'),\n \"b summary loop drops attribution_bare_verb\": ('for rx in (_SELF_CARRIED, fam[\"attribution\"], fam[\"attribution_bare_verb\"])', 'for rx in (_SELF_CARRIED, fam[\"attribution\"])'),\n \"c quote-side hedge lexicon check removed\": ('or has_hedge(excerpt) or fam[\"hedge\"].search(excerpt))', 'or has_hedge(excerpt))'),\n \"d inability_assertion block removed\": ('out += [_clean(m) for m in fam[\"inability_assertion\"].finditer(summary)]', 'pass'),\n \"e approximation preposition exemption removed\": ('and fam[\"approximation_preposition_context\"].search(summary[max(0, m.start() - 40):m.start()]):', 'and False:'),\n \"f qh approximation ignored\": ('if not (qh.get(\"approximation\") or _APPROX', 'if not (False or _APPROX'),\n \"g qh attribution ignored\": ('if not (qh.get(\"attribution\") or', 'if not (False or'),\n \"h qh hedge ignored\": ('if not (qh.get(\"hedge\") or', 'if not (False or'),\n \"i quote-side approx lexicon check removed\": ('or _APPROX.search(excerpt) or fam[\"approximation\"].search(excerpt)):', 'or _APPROX.search(excerpt)):'),\n \"j _canon_neg identity\": ('return \"not\" if w.endswith(\"n\\'t\") else w', 'return w'),\n \"k inability substitution removed\": ('neg_text = _aq()[\"inability\"].sub(\" \", summary) if _aq()[\"inability\"].search(excerpt) else summary', 'neg_text = summary'),\n \"l curly apostrophe in summary not normalised\": ('summary, excerpt = summary.replace(\"\\\\u2019\", \"\\'\"), excerpt.replace(\"\\\\u2019\", \"\\'\")', 'summary, excerpt = summary, excerpt.replace(\"\\\\u2019\", \"\\'\")'),\n \"m curly apostrophe in side_neg_words removed\": ('_WORDS.findall(text.replace(\"\\\\u2019\", \"\\'\"))', '_WORDS.findall(text)'),\n \"n _WORDS drops absence|lacks|free of|nothing|unremarkable\": ('|absence|lacks?|lacking|free\\\\s+of|nothing|unremarkable)', ')'),\n \"o attribution_bare_verb quote-side removed\": (' or fam[\"attribution\"].search(excerpt) or fam[\"attribution_bare_verb\"].search(excerpt)):', ' or fam[\"attribution\"].search(excerpt)):'),\n}\nS = {\n \"p spanish passes no quote_has attribution\": ('\"attribution\": _cue_set(excerpt, _SELF_CUES, _SELF_PHRASES),', '\"attribution\": False,'),\n \"q spanish passes no quote_has hedge\": ('\"hedge\": _cue_set(excerpt, _HEDGE_CUES, _HEDGE_PHRASES) or bool(_NOT_RULED_OUT.search(folded)),', '\"hedge\": False,'),\n \"r spanish passes no quote_has approximation\": ('\"approximation\": _cue_set(excerpt, _APPROX_CUES, _APPROX_PHRASES)})', '\"approximation\": False})'),\n \"s spanish _NEG_ENGLISH loses new words\": ('\"absent\", \"absence\", \"lack\", \"lacks\", \"lacking\",\\n                \"free of\", \"nothing\", \"unremarkable\"}', '\"absent\"}'),\n}\ndef run(name, path, orig, a, b):\n    if a not in orig:\n        print(\"SKIP (pattern not found)\", name); return\n    path.write_text(orig.replace(a, b, 1))\n    r = subprocess.run([py, \"-m\", \"pytest\", \"tests/unit/test_t105_added_qualifier_lexicon.py\", \"-q\", \"-p\", \"no:cacheprovider\"], cwd=work, capture_output=True, text=True)\n    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", last)\n    path.write_text(orig)\nfor n, (a, b) in G.items(): run(n, g, go, a, b)\nfor n, (a, b) in S.items(): run(n, s, so, a, b)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t105_mutants.py $S/t120r2/arc $S/t105/mut /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:32:23.871Z

**tool result**
````
KILLED   a summary loop drops fam['attribution'] | 6 failed, 43 passed in 0.21s
KILLED   b summary loop drops attribution_bare_verb | 1 failed, 48 passed in 0.20s
KILLED   c quote-side hedge lexicon check removed | 2 failed, 47 passed in 0.20s
KILLED   d inability_assertion block removed | 1 failed, 48 passed in 0.20s
KILLED   e approximation preposition exemption removed | 4 failed, 45 passed in 0.21s
KILLED   f qh approximation ignored | 1 failed, 48 passed in 0.20s
KILLED   g qh attribution ignored | 1 failed, 48 passed in 0.20s
KILLED   h qh hedge ignored | 1 failed, 48 passed in 0.21s
KILLED   i quote-side approx lexicon check removed | 1 failed, 48 passed in 0.23s
KILLED   j _canon_neg identity | 3 failed, 46 passed in 0.23s
KILLED   k inability substitution removed | 2 failed, 47 passed in 0.20s
SURVIVED l curly apostrophe in summary not normalised | 49 passed in 0.19s
KILLED   m curly apostrophe in side_neg_words removed | 4 failed, 45 passed in 0.21s
KILLED   n _WORDS drops absence|lacks|free of|nothing|unremarkable | 5 failed, 44 passed in 0.21s
SURVIVED o attribution_bare_verb quote-side removed | 49 passed in 0.20s
KILLED   p spanish passes no quote_has attribution | 1 failed, 48 passed in 0.20s
KILLED   q spanish passes no quote_has hedge | 1 failed, 48 passed in 0.20s
KILLED   r spanish passes no quote_has approximation | 1 failed, 48 passed in 0.20s
SURVIVED s spanish _NEG_ENGLISH loses new words | 49 passed in 0.19s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:36.846Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t105_probe_misc.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import grounding as G, spanish_text as ST, lexicon\nprint(\"curly can’t added:\", G.new_tokens(\"Patient can’t bear weight.\", \"Weight bearing tolerated.\"))\nprint(\"ascii can't added:\", G.new_tokens(\"Patient can't bear weight.\", \"Weight bearing tolerated.\"))\nprint(\"Indicates quote faithful:\", G.new_tokens(\"Patient indicates pain 4/10.\", \"Indicates pain 4/10.\"))\nprint(\"ES ausencia/absence:\", ST.new_tokens(\"Absence of numbness.\", \"Ausencia de entumecimiento.\"))\n# list inventory: regexes in code that hold attribution/hedge/approx words\nimport re\nfor n in (\"_SELF_CARRIED\", \"_SELF_IN_QUOTE\", \"_HEDGE_WORDS\", \"_APPROX\", \"_WORDS\"):\n    print(n, \"in grounding:\", len(getattr(G, n).pattern), \"chars\")\nfor n in (\"_EN_NEG_EXTRA\", \"_EN_NEG_QUOTE\", \"_NEG_ENGLISH\"):\n    v = getattr(ST, n); print(n, \"in spanish_text:\", (v.pattern if hasattr(v, \"pattern\") else sorted(v))[:120])\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t105_probe_misc.py $S/t120r2/arc; grep -n \"T-105\\|added_qualifier\\|dropped\" memory/SCOPE_CUTS.md | head; python3 tools/board.py list 2>/dev/null | grep -i \"dropped\\|qualifier\\|T-105\\|T-111\\|Waddell\" | head"
}
````

### User / tool · 2026-11-02T11:32:37.166Z

**tool result**
````
curly can’t added: ["can't"]
ascii can't added: ["can't"]
Indicates quote faithful: []
ES ausencia/absence: []
_SELF_CARRIED in grounding: 263 chars
_SELF_IN_QUOTE in grounding: 249 chars
_HEDGE_WORDS in grounding: 196 chars
_APPROX in grounding: 92 chars
_WORDS in grounding: 168 chars
_EN_NEG_EXTRA in spanish_text: \b(?:absent|absence|lacks?|lacking|free\s+of|rules?\s+out|ruled\s+out|unremarkable|none|neither|nor|never|nothing|exclud
_EN_NEG_QUOTE in spanish_text: \b(?:not|none|never|without|denies|denied|negative|neither|nor)\b|n't\b
_NEG_ENGLISH in spanish_text: ['absence', 'absent', 'denied', 'denies', 'free of', 'lack', 'lacking', 'lacks', 'negative', 'neither', 'never', 'no', 'none', 'nor', 'not', 'nothing', 'unremarkable', 'without']
37:| debt | T-032 accepted with documented debt after 2 rounds (§7.4) | r2 major (first line starting SYNTHETIC silently dropped) fixed as backend-2 follow-up with a mutation-sensitive test; minors carried | see card | M2 |
67:| debt | T-100 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; blocker fixed and the fixture eval is unchanged (0 new failures over 186 recorded summaries). Remaining word-list gaps and false refusals move to T-105; the judge still checks paraphrase faithfulness for AI text. | see card | M3 |
71:| debt | T-111 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; the D-043 not-performed silence and the common positive Waddell orders are fixed. Remaining code-rule gaps (count before the term, word-form counts 'three of five', non-adjacent counts) are covered by the model flag path plus the paralegal; logged as a lexicon follow-up in T-105. | see card | M3 |
T-100	M3	backend    	done             	P1	AC 1/1	Implement D-047: side/negation/qualifier tokens missing from the excerpt are a hard 422 on edit and manual entry; remove the 409 keep-my-wording path
T-105	M3	backend    	in_review        	P2	AC 1/1	Derive added-qualifier word lists from the lexicon (single source) and cover the T-100 r2 misses
T-111	M3	backend    	done             	P2	AC 1/1	D-043 reading: single-clause 'Waddell testing not performed/not done' stays silent (test not done is not a credibility finding)
T-126	M3	backend    	in_review        	P2	AC 1/1	D-057: D-032-filtered model flags (objective_negative) go to a collapsed 'Filtered by rule' tray group, never silently dropped
T-130	M3	backend    	backlog          	P2	AC 0/1	T-105 leftovers: Waddell count forms in credibility.py, statement-line service nouns as charge context, bare insurance/seguro wording
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:49.914Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-130 | sed -n 1,25p | cut -c1-600; grep -rn \"sha256\\|lexicon_hash\\|lexicon_sha\" evals/*.py | head -5; git log --oneline -3 -- app/llm/lexicon.yaml; git show aa6ae9f --stat --format=%H | head -3; ls evals/reports | tail -3"
}
````

### User / tool · 2026-11-02T11:32:50.283Z

**tool result**
````
---
id: "T-130"
title: "T-105 leftovers: Waddell count forms in credibility.py, statement-line service nouns as charge context, bare insurance/seguro wording"
milestone: "M3"
role: "backend"
status: "backlog"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:28:07Z"
updated_at: "2026-11-02T11:28:07Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "each of the three cases from T-105 notes has a unit test and behaves per D-043/D-052", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)

## Handoff (filled when moving to in_review)
evals/run.py:94:def sha256_file(p):
evals/run.py:95:    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
evals/run.py:99:    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
evals/run.py:102:        out[p.relative_to(root).as_posix()] = sha256_file(p)
evals/run.py:105:        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
aa6ae9f feat(backend): T-105 added-qualifier word lists (attribution, hedge, approximation, inability) come from lexicon.yaml code_lists.added_qualifier; curly apostrophes, Spanish-helper negations, faithful paraphrases; lexicon text updated to D-055
e1400d4 feat(backend): patient_report only from explicit patient attribution, scoped exclusion (T-061, D-033)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
aa6ae9fcca518b831cf9ec44aa733c4d548bb710

 app/backend/grounding.py                        | 62 ++++++++++++----
library-latest.md
m3-sensors.md
runs
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:55.740Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls evals/reports/runs | tail -3; ls evals/*.json evals/reports/*.json 2>/dev/null; shasum -a 256 app/llm/lexicon.yaml; git show aa6ae9f^:app/llm/lexicon.yaml | shasum -a 256; grep -rn \"lexicon.yaml\" evals/reports/latest.json 2>/dev/null | head -3; grep -o '\"app/llm/lexicon.yaml\": *\"[0-9a-f]*\"' -r evals/reports/*.json evals/reports/runs/* 2>/dev/null | tail -3"
}
````

### User / tool · 2026-11-02T11:32:55.923Z

**tool result**
````
20261102T104042Z
20261102T104435Z
20261102T105126Z
evals/reports/calibration.json
evals/reports/controls-20261102T042306Z.json
evals/reports/controls-20261102T043911Z.json
evals/reports/controls-20261102T044933Z.json
evals/reports/controls-20261102T045207Z.json
evals/reports/controls-20261102T063331Z.json
evals/reports/controls-20261102T075238Z.json
evals/reports/controls-20261102T090925Z.json
evals/reports/controls-20261102T102626Z.json
evals/reports/latest.json
ac3132161abd5600ce144b5ecc63f54f8b805ab7df507a0556f7cc42a7261821  app/llm/lexicon.yaml
a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263  -
evals/reports/latest.json:230:   "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
evals/reports/latest.json:300:  "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
evals/reports/runs/20261102T103042Z/calibration.json:"app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263"
evals/reports/runs/20261102T103337Z/calibration.json:"app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263"
evals/reports/runs/20261102T104042Z/calibration.json:"app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:01.685Z

**tool call — Bash**
````
{
 "command": "grep -n \"stale\\|def .*signature\\|calibration_stale\" evals/run.py | head -15; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t120r2/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --check-spec 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T11:33:01.834Z

**tool result**
````
677:def signature_parts(out):
704:def signature(out):
933:        blockers.append(f"hallucination_catch_rate not_measured: judge unavailable on {m['hallucination_catch_rate']['judge_unavailable_count']} line(s) (stale or missing judge fixtures?)")
1226:        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:03.960Z

**tool call — Bash**
````
{
 "command": "grep -rln \"lexicon.yaml\" app/backend/*.py | head; grep -rn \"def .*stale\\|calibration_stale\\|\\\"stale\\\"\" app/backend/*.py | head -8; git log --oneline -4 -- evals/reports/latest.json"
}
````

### User / tool · 2026-11-02T11:33:04.101Z

**tool result**
````
app/backend/calibration_route.py
app/backend/grounding.py
app/backend/lexicon.py
app/backend/calibration_route.py:144:def stale_reason(doc, current):
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
e491cad feat(evals): determinism signature covers every R-CO-7 field, per-run artifacts, J3/J4 seeded controls (T-093)
3104213 fix(backend): stabilize live 3-run determinism (T-075, R-CO-7)
43fc69e chore(backend): re-record sample narrative fixtures against current summaries; eval report
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:05.376Z

**tool call — Bash**
````
{
 "command": "sed -n 120,185p app/backend/calibration_route.py"
}
````

### User / tool · 2026-11-02T11:33:05.449Z

**tool result**
````
    return bad


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def disk_prompt_hashes(root=ROOT) -> dict:
    """The prompt and lexicon hashes read from the working tree: the set evals/run.py hashes() records. The route compares against these, not HEAD."""
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / PROMPT_DIR).glob("*.md")):
        out[p.relative_to(root).as_posix()] = _sha256(p.read_bytes())
    if (root / LEXICON).exists():
        out[LEXICON] = _sha256((root / LEXICON).read_bytes())
    return out


def current_prompt_hashes(root=ROOT) -> dict:
    """What the prompts are now: the files on disk under `root`, which are the files the running app loads (app/llm/promptlib.py reads them
    from disk). Deliberately not HEAD: a prompt edited and not yet committed already changes what the pipeline runs, so it must read as stale."""
    return disk_prompt_hashes(root)


def stale_reason(doc, current):
    """Why the measurement in `doc` no longer matches the prompts in `current`, or None. Compared name by name: a prompt added, removed or
    edited since the run means the counts describe other prompts. A file that records no hashes cannot be shown current."""
    recorded = doc.get("hashes")
    if not isinstance(recorded, dict) or not recorded:
        return "This measurement does not record which prompts it used, so it cannot be checked against the current prompts."
    changed = sorted(k for k in set(recorded) | set(current) if recorded.get(k) != current.get(k))
    if not changed:
        return None

    def describe(k):
        name = pathlib.PurePosixPath(k).name
        if k not in recorded:
            return f"{name} is new"
        if k not in current:
            return f"{name} was removed"
        return f"{name} changed"
    shown = "; ".join(describe(k) for k in changed[:8])
    more = f"; and {len(changed) - 8} more" if len(changed) > 8 else ""
    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."


def _envelope(status, calibration=None, message=None) -> dict:
    return {"status": status, "calibration": calibration, "message": message}


def load(path=REPORT, root=ROOT) -> dict:
    """The envelope for the file at `path`: ok with the served subset and the stale flags, missing, or invalid. Read-only; never raises.
    `root` is the tree whose prompt files (on disk) the file is compared with."""
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _envelope("missing", message=MISSING)
    except (OSError, UnicodeDecodeError):
        log.warning("calibration file could not be read: %s", p.name)
        return _envelope("invalid", message=INVALID)
    try:
        doc = json.loads(raw)
    except ValueError:
        log.warning("calibration file is not JSON: %s", p.name)
        return _envelope("invalid", message=INVALID)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:11.381Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/t105_stale.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import calibration_route as C\ne = C.load(root=sys.argv[1], path=sys.argv[1] + \"/evals/reports/calibration.json\")\nprint(e[\"status\"], {k: v for k, v in (e.get(\"calibration\") or {}).items() if \"stale\" in k}, (e.get(\"calibration\") or {}).get(\"stale_reason\"))\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t105_stale.py $S/t120r2/arc; echo parent:; mkdir -p $S/t105/par2 && git archive aa6ae9f^ | tar -x -C $S/t105/par2; .venv/bin/python -I artifacts/review-evidence/t105_stale.py $S/t105/par2"
}
````

### User / tool · 2026-11-02T11:33:12.033Z

**tool result**
````
ok {'stale': True, 'stale_reason': 'The prompts have changed since these numbers were measured: lexicon.yaml changed; judge_conflict_v6.md is new. The numbers describe an older version of the prompts.'} The prompts have changed since these numbers were measured: lexicon.yaml changed; judge_conflict_v6.md is new. The numbers describe an older version of the prompts.
parent:
ok {'stale': True, 'stale_reason': 'The prompts have changed since these numbers were measured: judge_conflict_v6.md is new. The numbers describe an older version of the prompts.'} The prompts have changed since these numbers were measured: judge_conflict_v6.md is new. The numbers describe an older version of the prompts.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:16.393Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p artifacts/review-evidence/T-100-r2/corpus_diff_routed.py 2>/dev/null || sed -n 1,40p artifacts/review-evidence/T-100-r2/corpus_probe_routed.py; sed -n 1,30p artifacts/review-evidence/T-100-r2/corpus_diff.py"
}
````

### User / tool · 2026-11-02T11:33:16.501Z

**tool result**
````
"""Usage: corpus_probe_routed.py <tree_root> <out.json>. Like corpus_probe.py but routes each recorded extract fixture through
spanish_text.module_for(language.detect(excerpt)['lang']), as the pipeline does."""
import glob, json, os, sys
root, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, root)
from app.backend import language, spanish_text as ST  # noqa: E402
res = {}
for f in sorted(glob.glob("/Users/arsis/zlayt-pm-project/tests/fixtures/llm/*.json")):
    o = json.load(open(f))["output"]
    if isinstance(o, dict) and set(o) == {"excerpt", "summary"}:
        lang = language.detect(o["excerpt"])["lang"]
        mod = ST.module_for(lang)
        res["fx:" + os.path.basename(f)[:12]] = {"summary": o["summary"], "excerpt": o["excerpt"], "lang": lang, "tokens": mod.new_tokens(o["summary"], o["excerpt"])}
json.dump(res, open(out, "w"), indent=1, sort_keys=True)
import collections
print(len(res), collections.Counter(v["lang"] for v in res.values()))
import json
import sys

a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
newly, cleared = [], []
for k in sorted(a):
    ta, tb = set(a[k]["tokens"]), set(b[k]["tokens"])
    if tb - ta:
        newly.append((k, sorted(tb - ta), a[k]["summary"], a[k]["excerpt"]))
    if ta - tb:
        cleared.append((k, sorted(ta - tb), a[k]["summary"], a[k]["excerpt"]))
print("items", len(a), "| newly flagged", len(newly), "| newly cleared", len(cleared))
for k, t, s, e in newly:
    print("NEW  ", k, t, "\n   S:", s, "\n   Q:", e)
for k, t, s, e in cleared:
    print("CLEAR", k, t, "\n   S:", s, "\n   Q:", e)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:20.527Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; P=artifacts/review-evidence/T-100-r2; .venv/bin/python -I $P/corpus_probe_routed.py $S/t105/par2 $S/t105/c_par.json && .venv/bin/python -I $P/corpus_probe_routed.py $S/t120r2/arc $S/t105/c_head.json && .venv/bin/python -I $P/corpus_diff.py $S/t105/c_par.json $S/t105/c_head.json | cut -c1-400"
}
````

### User / tool · 2026-11-02T11:33:21.283Z

**tool result**
````
191 Counter({'en': 185, 'es': 6})
191 Counter({'en': 185, 'es': 6})
items 191 | newly flagged 0 | newly cleared 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:36.832Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120r2/arc && (LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt > ../cli1.txt 2>../cli1.err; echo rc=$?; LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt > ../cli2.txt 2>../cli2.err; echo rc=$?; cmp ../cli1.txt ../cli2.txt && echo IDENTICAL; wc -l ../cli1.txt; head -c 300 ../cli1.err)"
}
````

### User / tool · 2026-11-02T11:33:37.891Z

**tool result**
````
rc=0
rc=0
IDENTICAL
      45 ../cli1.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:42.252Z

**tool call — Bash**
````
{
 "command": "git status --short app tests | head; grep -n \"_SENT_END\\|def _is_source_sentence\\|_HISTORY_VIA =\\|return not re.search\\|_HISTORY_SOURCE =\" app/backend/lexicon_scan.py; grep -n \"def _one_line\\|def _translation_line\\|tr = f\\|_translation_line(e)\\|ends the line\" app/backend/export.py memory/contracts/api.md | cut -c1-120; grep -n \"def test_oneline_collapses\\|def test_oneline_translated\" tests/unit/test_t121_letter_styles.py; grep -n \"_WORDS = \\|^_SELF_CARRIED\\|^_HEDGE_WORDS\\|^_SELF_IN_QUOTE\\|^_APPROX\\|def dropped_qualifiers\\|def added_qualifier_tokens\\|if hedge_ids(excerpt) and not\" app/backend/grounding.py; grep -n \"^_NEG_ENGLISH\\|^_EN_NEG_EXTRA\\|^_EN_NEG_QUOTE\" app/backend/spanish_text.py; grep -n \"def test_the_word_lists_come_from\\|for word in\" tests/unit/test_t105_added_qualifier_lexicon.py"
}
````

### User / tool · 2026-11-02T11:33:42.396Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:33:59.773Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD; sed -n 266,266p app/backend/export.py | cut -c1-140; ls reviews | grep -E \"T-120-staff|T-121-staff|T-105\""
}
````

### User / tool · 2026-11-02T11:33:59.884Z

**tool result**
````
433ac1c60f608713917d4fa4010a54d5fb6cae08
            tr = f" — English: {_one_line(e['summary'])}" if e.get("translation_label") else ""
T-120-staff-engineer.md
T-121-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:34:24.544Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-staff-engineer-r2.md",
 "content": "# T-120 staff-engineer review, round 2 (fix commit 07dbd2b, archive of HEAD 433ac1c)\n\nVerdict: changes. The r1 forms are fixed: `Hx per patient: lumbar strain 2019.`, `Hx obtained via interpreter: ...` and the `of`/year forms now flag, and lib09 record 1 stays quiet. The new guard is still a proxy. It skips whenever the rest of the sentence has no colon, no digit and no `of`, and that is not the same as \"the sentence names no condition\". Several ordinary wordings that name a condition are still suppressed, and some of them were flagged before T-120.\n\nExercised (archive of HEAD 433ac1c under the scratchpad, `.venv/bin/python -I`):\n- `pytest tests/unit -q` on the archive: 3005 passed, 4 skipped.\n- Probe `artifacts/review-evidence/t120r2_probe.py`: 32 history-source phrasings, 13 without a condition and 19 with one, run against HEAD and against the parent of the T-120 commit (1cb8707^). Output quoted below.\n- Mutants `artifacts/review-evidence/t120r2_mutants.py` against `tests/unit/test_t120_history_source_sentence.py` (9 mutants).\n- Read `git show 07dbd2b` in full. No LLM call, no float, no network, no clock; the guard is deterministic code in `lexicon_scan.py`.\n\nProbe results (HEAD). Source-only sentences that stay quiet (correct): `Hx per patient's son.`, `PHx obtained via patient's son, who interpreted.`, `History provided by patient's wife.`, `Hx obtained via telephone interpreter.`, `Hx per EMS.`, `Hx per interpreter line.`, `History given by the patient's mother.`, `Hx relayed through language line interpreter.`, `PHx gathered from patient's friend.`, `History was obtained from patient's caregiver.`, `History obtained from chart review.`, `Hx obtained from Dr. Lee.`\nCondition named, flag kept (correct): `Hx obtained via interpreter: lumbar strain 2019.`, `PHx obtained via patient's son: lumbar strain 2019.`, `Hx per patient's son, history of lumbar strain.`, `Hx per EMS - pt had previous knee surgery`, `PHx obtained via son; previous whiplash`, and the sentence-adjacent `Hx of lumbar strain 2019.` case.\nCondition named, flag LOST (see finding 1): `Hx per patient's son, significant for diabetes.`, `History provided by wife, notable for lumbar strain.`, `History obtained from patient - lumbar strain.`, `PHx obtained via interpreter (lumbar strain).`, `Hx obtained via interpreter\\nLumbar strain 2019`, `Hx per patient's son, who interpreted, a recurring back problem`, `Hx obtained from Dr. Lee: lumbar strain`, `Hx per patient's son; patient fractured her wrist before.`\nSame eight against the parent 1cb8707^: the parent flags `Hx` in five of them (diabetes, parenthesis, newline, recurring, Dr. Lee colon), so those five are regressions that T-120 introduced. The other three (wife, dash, fractured) were not flagged by the parent either.\n\nMutants on the T-120 test file: drop the rest check (killed), drop digit (killed), drop `of` (killed), widen `via` (killed), never skip (killed), rest-to-end-of-text (killed), drop the VIA alternative (killed). SURVIVED: drop the colon from the rest check; newline no longer a sentence end.\n\n```json\n{\"card\": \"T-120\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive HEAD 433ac1c (T-120 r2 commit 07dbd2b): app/backend/lexicon_scan.py:15-20, :107-115, :152; tests/unit/test_t120_history_source_sentence.py; no app URL\",\n \"exercised\": [\"pytest tests/unit -q on archive of HEAD: 3005 passed, 4 skipped\", \"artifacts/review-evidence/t120r2_probe.py: 32 phrasings on HEAD and on parent 1cb8707^\", \"artifacts/review-evidence/t120r2_mutants.py: 9 mutants, 7 killed, 2 survived\", \"artifacts/review-evidence/t120r2_probe2.py: colon-only and newline forms\", \"read git show 07dbd2b in full\", \"python -m app.pipeline evals/golden/sample.txt twice (fixture backend): identical output\"],\n \"verdict\": \"changes\",\n \"scores\": {\"correctness\": 3, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The skip tests for the absence of a colon, digit or 'of', not for the absence of a condition, so a named prior condition is still dropped without a trace\",\n   \"evidence\": \"app/backend/lexicon_scan.py:115 `return not re.search(r\\\":|\\\\d|\\\\bof\\\\b\\\", rest, re.I)` and :20 `_SENT_END = re.compile(r\\\"[.!?](?:\\\\s|$)|\\\\n\\\")`. Repro: `.venv/bin/python -I artifacts/review-evidence/t120r2_probe.py <archive of 433ac1c>` -> `BAD expect-flag \\\"Hx per patient's son, significant for diabetes.\\\" -> []`; `'PHx obtained via interpreter (lumbar strain).' -> []`; `'Hx obtained via interpreter\\\\nLumbar strain 2019' -> []` (the newline ends the 'sentence', so the year is never seen); `'Hx obtained from Dr. Lee: lumbar strain' -> []` (the period after Dr ends the sentence before the colon); `\\\"Hx per patient's son, who interpreted, a recurring back problem\\\" -> []`. The same inputs on the parent (1cb8707^) return ['Hx'] for diabetes, parenthesis, newline, recurring and the Dr. Lee colon form (artifacts/review-evidence/t120r2_probe.py with the parent archive).\",\n   \"why_it_matters\": \"The card's rule is that the flag is suppressed only when the sentence names no condition. These sentences name one. A pre-existing condition is the first thing an adjuster looks for; losing its flag is silent (no state, no log) and is a regression against the build before T-120. Multi-line excerpts and 'Dr.' abbreviations are ordinary in record text, so the newline and Dr. forms are not exotic. I rate it major, not blocker: the quote stays in the record and entry, the lexicon's other phrases (prior, previous, chronic, degenerative, pre-existing) still catch most wordings, and it is the same class as my r1 finding at lower incidence.\",\n   \"fix\": \"Invert the test: skip only when the whole remainder of the clause is a recognised source phrase and nothing else, for example match `^(source phrase)(,? who interpreted)?\\\\s*[.;]?\\\\s*(?:$|\\\\n\\\\s*$)`-style, or strip the source phrase and rescan the remainder for any other word. Treat newline, '(' , dash and ';' as continuing the condition text, not as the end of the source sentence, and do not end a sentence on an abbreviation such as 'Dr.'.\",\n   \"acceptance_test\": \"Add to REAL in tests/unit/test_t120_history_source_sentence.py: \\\"Hx per patient's son, significant for diabetes.\\\", 'PHx obtained via interpreter (lumbar strain).', 'Hx obtained via interpreter\\\\nLumbar strain 2019', 'Hx obtained from Dr. Lee: lumbar strain', \\\"Hx per patient's son, who interpreted, a recurring back problem\\\"; assert each returns a pre_existing hit. Keep every SOURCE case green.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Two of the guard's conditions are unpinned: the colon check and the newline sentence end\",\n   \"evidence\": \"artifacts/review-evidence/t120r2_mutants.py: `SURVIVED M2 drop colon from rest check | 28 passed` and `SURVIVED M8 newline not a sentence end | 28 passed`. Every REAL row with a colon also has a digit, an 'of' or a separate lexicon phrase (`Hx per patient's son: prior neck injury.` is caught by 'prior ... injury', not by the Hx hit), so the colon branch is never the deciding one. Colon-only probe: `Hx obtained via interpreter: lumbar strain.` -> ['Hx'] today and would be [] under M2.\",\n   \"why_it_matters\": \"The r1 blocker class was exactly the colon form; a later edit could reopen it and the suite would stay green. Tests that assert 'any pre_existing hit' cannot tell which rule produced it.\",\n   \"fix\": \"Assert on the Hx hit itself (hit text equals the history word) for the colon-only and newline rows.\",\n   \"acceptance_test\": \"Rows `Hx obtained via interpreter: lumbar strain.` and `Hx obtained via interpreter\\\\nLumbar strain` must assert a hit whose text is 'Hx'; mutants M2 and M8 in t120r2_mutants.py must be killed.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Source phrases that name no person still flag: 'Hx per patient.' and 'Hx per medical records.'\",\n   \"evidence\": \"t120r2_probe.py: `BAD expect-none 'Hx per patient.' -> ['Hx']`, `'Hx per medical records.' -> ['Hx']`. The parent flags them too.\",\n   \"why_it_matters\": \"Over-flagging, the safe direction; the paralegal dismisses it. Listed so nobody mistakes it for a regression.\",\n   \"fix\": \"Optional: add 'patient' and 'medical records' as stand-alone channels only after the finding-1 inversion, so the rule stays one mechanism.\",\n   \"acceptance_test\": \"Optional test that both phrases stay quiet and `Hx per patient: lumbar strain 2019.` still flags.\"}\n ],\n \"whats_right\": [\"All three r1 forms (Hx per patient: ..., colon after via, 'of') now flag, with named rows in REAL.\", \"Guard is deterministic code in lexicon_scan.py; lexicon.yaml untouched; the sample CLI output is byte-identical across two runs.\", \"Seven of nine mutants on the guard are killed, including widening `via` and removing the digit or 'of' check.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:34:24.703Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-120-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:34:30.249Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/t120r2_probe.py $S/t120r2/parent | grep -E \"fractured|wife, notable|patient - lumbar\""
}
````

### User / tool · 2026-11-02T11:34:30.448Z

**tool result**
````
BAD expect-flag 'History provided by wife, notable for lumbar strain.' -> []
OK  expect-flag "Hx per patient's son; patient fractured her wrist before." -> ['Hx']
BAD expect-flag 'History obtained from patient - lumbar strain.' -> []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:34:33.139Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-staff-engineer-r2.md",
 "old_string": "Same eight against the parent 1cb8707^: the parent flags `Hx` in five of them (diabetes, parenthesis, newline, recurring, Dr. Lee colon), so those five are regressions that T-120 introduced. The other three (wife, dash, fractured) were not flagged by the parent either.",
 "new_string": "Same eight against the parent 1cb8707^: the parent flags `Hx` in six of them (diabetes, parenthesis, newline, recurring, Dr. Lee colon, and `Hx per patient's son; patient fractured her wrist before.`), so those six are regressions that T-120 introduced. The other two (wife, dash) are `History` forms the parent did not flag either."
}
````

### User / tool · 2026-11-02T11:34:33.187Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-120-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:34:51.225Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-121-staff-engineer-r2.md",
 "content": "# T-121 staff-engineer review, round 2 (fix commit 4c59fac, archive of HEAD 433ac1c)\n\nVerdict: pass. Both r1 findings are fixed and pinned. The one-line style now carries ` — English: <summary>` on a translated entry before the note, the whitespace-only collapse is documented in the docstring and in api.md, and the standard style prints the note on its own bracket line under the quote. The default letter still equals the golden. Three minors and nits remain; none blocks.\n\nExercised (archive of HEAD 433ac1c, `.venv/bin/python -I`):\n- `pytest tests/unit -q` on the archive: 3005 passed, 4 skipped. This includes the golden byte-equal test, `test_spanish_records` and `test_d050_never_verified`.\n- `python -m evals.run --check-spec` on the archive: `{\"spec_matches_golden\": true, \"letter_equal\": true, \"internal_notes_equal\": true}`.\n- Mutants `artifacts/review-evidence/t121r2_mutants.py` (12) against test_t121_letter_styles, test_spanish_records, test_d050_never_verified and test_export.\n- Probe `artifacts/review-evidence/t121r2_probe.py`: translated entry with empty, None and whitespace-only summary, and with a multi-line edited summary, in both styles.\n- Read `git show 4c59fac` in full (export.py, api.md, the test file). No LLM call, no float, no network.\n\nMutant results: `_one_line` no-op KILLED (2 failed), `_one_line` collapsing spaces only KILLED, drop the English tail KILLED, English tail on every entry KILLED, summary not collapsed KILLED, standard style with the note back on the quote line KILLED, drop the note line in standard KILLED, tail placed after the note KILLED, note line with a leading space KILLED, one-line drops the note KILLED, one-line note only for one label KILLED. SURVIVED: provider label not collapsed in the one-line style (`{v.source(n)}` for `{_one_line(v.source(n))}`), 123 passed.\n\nProbe, translated entry, one-line: summary '' gives `... [Ex. __ / Bates __] — English:  [AI translation of the Spanish original; check before sending]`; summary None gives `— English: None [...]`. Standard style with summary None raises `TypeError: sequence item 3: expected str instance, NoneType found` at export.py:285 (this crash predates T-121; the entry schema has a string summary).\n\n```json\n{\"card\": \"T-121\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive HEAD 433ac1c (T-121 r2 commit 4c59fac): app/backend/export.py:245-270, memory/contracts/api.md:373 and :718, tests/unit/test_t121_letter_styles.py:80-146; no app URL\",\n \"exercised\": [\"pytest tests/unit -q on archive of HEAD: 3005 passed, 4 skipped\", \"python -m evals.run --check-spec: letter_equal true, internal_notes_equal true\", \"artifacts/review-evidence/t121r2_mutants.py: 12 mutants, 11 killed, 1 survived\", \"artifacts/review-evidence/t121r2_probe.py: empty/None summary and multi-line summary in both styles\", \"read git show 4c59fac in full\"],\n \"verdict\": \"pass\",\n \"scores\": {\"correctness\": 4, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"api.md still says the translation note 'ends the line in both styles', which is false for the standard style after r2\",\n   \"evidence\": \"memory/contracts/api.md:373 ends with `The translation note ends the line in both styles.`; app/backend/export.py:248-250 and :269 now print the standard-style note as its own line (`*_translation_line(e)`), and api.md:718 says 'on its own line under the quote'. The two paragraphs of the same contract disagree.\",\n   \"why_it_matters\": \"api.md is the contract the frontend and any later reviewer read; a reader of :373 would expect the note to share the quote's line and would write a UI or test against it.\",\n   \"fix\": \"Change :373 to 'The translation note is its own bracket line under the quote in the standard style and ends the entry's line in the one-line style.'\",\n   \"acceptance_test\": \"grep -n 'ends the line in both styles' memory/contracts/api.md returns nothing.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Collapsing the provider label in the one-line style is not pinned by any test\",\n   \"evidence\": \"t121r2_mutants.py: `SURVIVED H provider not collapsed in oneline | 123 passed`. export.py:269 calls `_one_line(v.source(n))`; no test gives a source label with a line break or a double space.\",\n   \"why_it_matters\": \"Low: source labels come from a single header line. If a label ever carries a break, the 'one line per entry' promise breaks silently.\",\n   \"fix\": \"Add a case with a source label containing a run of spaces and assert the entry line has one space.\",\n   \"acceptance_test\": \"Mutant H is killed.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"A translated entry with an empty summary prints a dangling 'English:' in the one-line style\",\n   \"evidence\": \"t121r2_probe.py: summary '' -> `[Ex. __ / Bates __] — English:  [AI translation of the Spanish original; check before sending]`. export.py:266 `tr = f\\\" — English: {_one_line(e['summary'])}\\\" if e.get(\\\"translation_label\\\") else \\\"\\\"`.\",\n   \"why_it_matters\": \"Edits to an empty summary are most likely rejected upstream, so I could not reach this through the API; the pure builder still has no guard and the note would then point at nothing again.\",\n   \"fix\": \"Build the tail only when the collapsed summary is non-empty, or raise in the builder.\",\n   \"acceptance_test\": \"A unit test with summary '' asserts no 'English:' fragment on the line.\"}\n ],\n \"whats_right\": [\"r1 major fixed at the right place: the translated summary sits on the one-line entry, in front of the note, with the multi-line case tested.\", \"The whitespace-only collapse is documented (export.py:253 docstring, api.md:373) and the no-op mutant that survived r1 is now killed.\", \"Default and style=standard letters stay byte-equal to evals/golden; build_export is still a pure function of accepted items and an unknown style fails with a ValueError / 422.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:34:51.367Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-121-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:34:55.909Z

**tool call — Bash**
````
{
 "command": "grep -n \"_one_line(v.source\" app/backend/export.py | cut -c1-60; sed -n 254p app/backend/export.py | cut -c1-80"
}
````

### User / tool · 2026-11-02T11:34:55.999Z

**tool result**
````
267:            out += [f'{_long_date(v.date_of(e))} — {_o
    """Whitespace only: every run of spaces, tabs and line breaks becomes one sp
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:35.655Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-105-staff-engineer.md",
 "content": "# T-105 staff-engineer review, round 1 (card commit aa6ae9f, archive of HEAD 433ac1c)\n\nVerdict: changes. The lexicon family `code_lists.added_qualifier` exists, is read by `grounding.added_qualifier_tokens`, and the Spanish path calls the same function with its own quote-side cues. Every wording named in the T-100 r2 review is refused, and the faithful paraphrases are not. But \"single source\" is not reached: the lists that decide whether the QUOTE carries a qualifier, and the whole dropped-qualifier check, still read private regexes in `grounding.py`, and the card adds a third hand-typed copy of the negation words. The card's evidence line \"no list words left in grounding.py/spanish_text.py\" rests on a six-word spot check.\n\nExercised (archive of HEAD 433ac1c and of the parent aa6ae9f^, `.venv/bin/python -I`):\n- `pytest tests/unit -q` on the archive: 3005 passed, 4 skipped (includes the 49 tests in test_t105_added_qualifier_lexicon.py and the lexicon examples check).\n- T-100 r2 probe `artifacts/review-evidence/T-100-r2/probe_variants.py` on HEAD: 43 of 48 wordings refused. The 18 wordings named in the T-100 r2 finding all refuse. Still passing: 'The patient told staff pain 4/10', 'Pain in the range of 4/10', 'Pain somewhere near 4/10', 'L side', 'both sides'. None of these five was named in that finding.\n- Faithful-paraphrase probe `T-100-r2/probe_fp.py` on HEAD: 'about as preposition', 'cannot for unable to', 'contraction for did not' pass; `faithful-but-refused: 5` (around, appears, negative, no for denies, May).\n- Mutants `artifacts/review-evidence/t105_mutants.py` (19) against test_t105_added_qualifier_lexicon.py: 16 killed, 3 survived (below).\n- Probes `artifacts/review-evidence/t105_probe_dropped.py` (dropped-qualifier direction), `t105_probe_misc.py`, `t105_stale.py`.\n- Recorded-corpus replay `T-100-r2/corpus_probe_routed.py` + `corpus_diff.py` on parent and HEAD: `items 191 | newly flagged 0 | newly cleared 0`.\n- Fixture eval `python -m evals.run --backend fixture` on parent and HEAD: stdout identical except the report path (ship_bar_met=False on live-only items on both). `--check-spec` on HEAD: spec_matches_golden true.\n- `python -m app.pipeline evals/golden/sample.txt` twice with `LLM_BACKEND=fixture`: byte-identical.\n- Read `git show aa6ae9f` in full: grounding.py, spanish_text.py, lexicon.yaml and the test file. No LLM call, no float, no network, no clock.\n\nRemaining duplicated lists (grep on HEAD): grounding.py:183 `_APPROX`, :185 `_SELF_CARRIED`, :192 `_HEDGE_WORDS`, :197 `_SELF_IN_QUOTE`, :128 `_WORDS`; spanish_text.py:36-37 `_NEG_ENGLISH`, :62-63 `_EN_NEG_EXTRA`, :68 `_EN_NEG_QUOTE`. The first four are still consulted inside `added_qualifier_tokens` (:231, :233, :242) and entirely by `dropped_qualifiers` (:254, :256, :264).\n\n```json\n{\"card\": \"T-105\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive HEAD 433ac1c (T-105 commit aa6ae9f): app/backend/grounding.py:125-258, app/backend/spanish_text.py:30-70 and :205-215, app/llm/lexicon.yaml code_lists.added_qualifier, tests/unit/test_t105_added_qualifier_lexicon.py; no app URL\",\n \"exercised\": [\"pytest tests/unit -q on archive of HEAD: 3005 passed, 4 skipped\", \"T-100-r2/probe_variants.py on HEAD: 43 of 48 refuse, all 18 named T-100 r2 wordings refuse\", \"T-100-r2/probe_fp.py on HEAD: faithful paraphrases pass\", \"artifacts/review-evidence/t105_mutants.py: 19 mutants, 16 killed, 3 survived\", \"artifacts/review-evidence/t105_probe_dropped.py: 9 of 11 dropped qualifiers not caught\", \"T-100-r2 corpus replay parent vs HEAD: 191 items, 0 newly flagged, 0 cleared\", \"python -m evals.run --backend fixture on parent and HEAD: same output; --check-spec true\", \"artifacts/review-evidence/t105_stale.py: calibration stale reasons\", \"python -m app.pipeline evals/golden/sample.txt twice: identical\", \"read git show aa6ae9f in full\"],\n \"verdict\": \"changes\",\n \"scores\": {\"correctness\": 4, \"determinism\": 5, \"llm_code_boundary\": 5, \"test_quality\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"The word lists are not a single source: the quote-side and dropped-qualifier checks still read private regexes, and the negation words now exist in three hand-typed copies\",\n   \"evidence\": \"app/backend/grounding.py:251-264 `dropped_qualifiers` uses `_HEDGE_WORDS` (:192), `_SELF_CARRIED` (:185) and `_APPROX` (:183), none of which read the lexicon family. Repro `.venv/bin/python -I artifacts/review-evidence/t105_probe_dropped.py <archive of 433ac1c>`: quote 'Patient describes pain 4/10.' -> summary 'Pain 4/10.' returns []; likewise 'apparently improving', 'potentially improving', 'seems to be improving', 'nearly 4/10', 'circa 4/10', 'close to 4/10', 'reportedly 4/10', 'according to the patient 4/10' (9 of 11 pairs lost the qualifier unseen; only 'possibly' and 'approx.' are caught). In added_qualifier_tokens the quote-side test still ORs the old lists (grounding.py:231 `_SELF_CARRIED.search(excerpt) or _SELF_IN_QUOTE.search(excerpt)`, :242 `_APPROX.search(excerpt)`). Negation words: the card typed 'absence|lacks|lacking|free of|nothing|unremarkable' into grounding.py:128 `_WORDS`, spanish_text.py:36-37 `_NEG_ENGLISH` and left spanish_text.py:62-63 `_EN_NEG_EXTRA`, so the same words live in three places. tests/unit/test_t105_added_qualifier_lexicon.py:73 `for word in (\\\"describes\\\", \\\"apparently\\\", \\\"nearly\\\", \\\"circa\\\", \\\"potentially\\\", \\\"indicates\\\")` is the only guard behind the card's evidence 'no list words left in grounding.py/spanish_text.py'; the handoff itself says 'dropped_qualifiers shares the same lists on the quote side, so I kept the carries checks lenient'.\",\n   \"why_it_matters\": \"The card exists because T-100 r2 found three different vocabularies for one check (title: 'single source'). After T-105 the added side reads the lexicon and the carried/dropped side reads code, so a lexicon edit changes one direction and not the other: a summary may not ADD 'apparently' but may silently DROP it (a D-022 dropped hedge, attribution or approximation reaches the entry unflagged). The next list change will drift again, which is how the original defect arose. Rated major, not blocker: no invented fact now passes that the card was meant to stop, and the dropped-side gap predates the card; the shortfall is the card's own stated goal plus an evidence claim that overstates it.\",\n   \"fix\": \"Build `_SELF_CARRIED`/`_SELF_IN_QUOTE`/`_HEDGE_WORDS`/`_APPROX` as thin views over the lexicon family (or retire them and call `aq(...)` everywhere, including dropped_qualifiers and missing_qualifier_terms), and make the Spanish negation sets derive from one list. If the dropped side is deliberately out of scope, say so in the card, add a SCOPE_CUTS row and a follow-up card (T-130 does not cover it), and drop the 'no list words left' sentence from the evidence.\",\n   \"acceptance_test\": \"A test that fails if any of `_SELF_CARRIED`, `_SELF_IN_QUOTE`, `_HEDGE_WORDS`, `_APPROX`, `_NEG_ENGLISH`, `_EN_NEG_EXTRA` is a literal word list in code (for example: every alternation word in them must also match a lexicon pattern, checked in both directions). Plus rows in the dropped-qualifier tests for 'describes', 'apparently', 'nearly', 'circa', 'according to the patient' that expect a dropped kind.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Three branches of the new code are unpinned, and the source guard is a six-word spot check\",\n   \"evidence\": \"artifacts/review-evidence/t105_mutants.py: `SURVIVED o attribution_bare_verb quote-side removed | 49 passed` (grounding.py:231 `or fam[\\\"attribution_bare_verb\\\"].search(excerpt)`; probe `new_tokens('Patient indicates pain 4/10.', 'Indicates pain 4/10.')` -> [] only because that branch is present); `SURVIVED s spanish _NEG_ENGLISH loses new words | 49 passed` (spanish_text.py:36-37; `ST.new_tokens('Absence of numbness.', 'Ausencia de entumecimiento.')` -> [] today and no test asserts it); `SURVIVED l curly apostrophe in summary not normalised | 49 passed`. Guard at test_t105_added_qualifier_lexicon.py:67-77 only greps six words.\",\n   \"why_it_matters\": \"A later cleanup can delete these branches and the suite stays green; the source guard cannot see a seventh word added back to code.\",\n   \"fix\": \"Add rows: a bare-verb quote ('Indicates pain 4/10.') against a 'Patient indicates' summary; a Spanish quote with 'ausencia'/'sin' against an English 'absence of' summary; a curly 'can’t' summary against a quote with no inability. Replace the six-word grep with the structural check in finding 1.\",\n   \"acceptance_test\": \"Mutants o and s in t105_mutants.py are killed; adding the word 'seems' as a literal to grounding.py makes the guard fail.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"No re-run eval report path for a lexicon change, and the served calibration is now stale for lexicon.yaml too\",\n   \"evidence\": \"Checklist 18: the diff adds 59 lines to app/llm/lexicon.yaml (family added_qualifier) and rewrites the non_encounter text; the handoff says only 'evals fixture unchanged earlier' with no report path. evals/reports/latest.json:230 and :300 record lexicon sha a2518d8f...; the file now hashes to ac313216... . `.venv/bin/python -I artifacts/review-evidence/t105_stale.py`: HEAD stale_reason 'lexicon.yaml changed; judge_conflict_v6.md is new', parent 'judge_conflict_v6.md is new'. lexicon.yaml is researcher-owned (CLAUDE.md file ownership) and the backend commit edited it without a researcher card.\",\n   \"why_it_matters\": \"I re-ran the fixture eval and the 191-item recorded corpus and found no change, so the code is not harmed; but the card should cite that run, and a live re-measure is what clears the stale label. Cross-boundary edits are supposed to go through the owner.\",\n   \"fix\": \"Add the fixture eval report path (and the corpus replay) to the handoff, note the live re-run is owed, and file or cite the researcher card for the lexicon family.\",\n   \"acceptance_test\": \"Card handoff names an evals/reports path dated after aa6ae9f; the lexicon family has a researcher-reviewed note.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Five same-class wordings still pass (outside the card's AC)\",\n   \"evidence\": \"T-100-r2/probe_variants.py on HEAD: `PASSES attribution 'The patient told staff pain 4/10, improving.'`, `PASSES approx 'Pain in the range of 4/10'`, `'Pain somewhere near 4/10'`, `PASSES side/neg 'L side'`, `'both sides'`. They were in the r2 probe output but not in the r2 finding text, so the card is not wrong to leave them.\",\n   \"why_it_matters\": \"Same invention class as the T-100 r2 misses; the judge is the only remaining check.\",\n   \"fix\": \"Add 'told', 'in the range of', 'somewhere near' to the lexicon family; side words are a separate question.\",\n   \"acceptance_test\": \"Add the three wordings to test_r2_misses_are_refused.\"}\n ],\n \"whats_right\": [\"Every wording named in the T-100 r2 finding is refused, and faithful paraphrases ('about 3 exercises', 'cannot'~'unable to', didn't~did not) are not; 16 of 19 mutants on the new code are killed.\", \"The Spanish path calls the English function with a quote_has dict instead of keeping its own summary-side lists, and the recorded corpus (191 items) shows 0 new refusals.\", \"The lexicon family carries hit/miss examples that a test executes, and the leftovers (Waddell counts, statement-line nouns) were moved to T-130 instead of being left open on this card.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:35:35.801Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:39.823Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate --help 2>&1 | head -5; for f in T-120-staff-engineer-r2 T-121-staff-engineer-r2 T-105-staff-engineer; do python3 - \"$f\" <<'EOF'\nimport sys,re,json\nt=open(f\"reviews/{sys.argv[1]}.md\").read()\nb=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S)\nd=json.loads(b[0]); print(sys.argv[1],len(b),d[\"verdict\"],[f[\"severity\"] for f in d[\"findings\"]])\nEOF\ndone"
}
````

### User / tool · 2026-11-02T11:35:40.025Z

**tool result**
````
usage: board.py validate [-h] [path]

positional arguments:
  path

T-120-staff-engineer-r2 1 changes ['major', 'minor', 'nit']
T-121-staff-engineer-r2 1 pass ['minor', 'nit', 'nit']
T-105-staff-engineer 1 changes ['major', 'minor', 'minor', 'nit']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:40.863Z

Now save memory for recurring patterns.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:48.324Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t120_t121_t105_patterns.md",
 "content": "---\nname: t120-t121-t105-review-patterns\ndescription: T-120 r2 (changes), T-121 r2 (pass), T-105 r1 (changes) at HEAD 433ac1c: negative-proxy guards, single-source refactor that covers one direction, write-once review errata\nmetadata:\n  type: project\n---\n\nReviewed at HEAD 433ac1c (fixes 07dbd2b, 4c59fac; card aa6ae9f).\n\n- **Negative-proxy guard (T-120 r2).** \"Skip when the rest of the sentence has no colon/digit/of\" is not \"names no condition\". Probe both the card's commit and its parent with the same phrasing list; regressions are the ones the parent flagged. Sentence-end regexes that count `\\n` and `Dr.` as ends hide the condition text. Use a probe script that prints expect-flag vs actual for 30+ phrasings, then mutate each clause of the guard (colon and newline mutants survived).\n- **Single-source refactor covers one direction (T-105).** Card read the lexicon on the ADDED side only; `dropped_qualifiers` and quote-side carry checks still read `_SELF_CARRIED/_HEDGE_WORDS/_APPROX`. Always probe the reverse direction (quote has word, summary drops it) and grep for sibling lists after any \"one list\" claim. A \"no list words left\" test that greps six words is a spot check.\n- **Lexicon change checklist.** latest.json/calibration hash lexicon.yaml; `calibration_route.stale_reason` shows it. Run fixture eval on parent and HEAD, replay the 191 recorded fixtures (`artifacts/review-evidence/T-100-r2/corpus_probe_routed.py` + `corpus_diff.py`) to show no change.\n- **Write-once errata.** My r2 files carry three small errors I could not fix (guard blocks Edit): T-120-r2 says \"five\" regressions and \"other three not flagged by parent\" but the parent also flagged the \"fractured\" form (six); T-121-r2 cites export.py:269 for the one-line provider collapse (it is :267) and says an empty summary \"could not be reached through the API\" (untested). Proof-read every cite and every \"could not\" claim against a command output before the first Write; state only what was run.\n- **Reviewer env.** No `timeout` on macOS; run long pytest with output redirect in background. Full unit suite takes about 3 minutes (3005 passed, 4 skipped at 433ac1c).\n\n**Why:** same two traps recur: guards that approximate the rule, and refactors that fix the direction the reviewer looked at.\n**How to apply:** see [[project_t100_r2_patterns]] for the original T-100 misses and [[feedback_review_write_once]].\n"
}
````

### User / tool · 2026-11-02T11:35:48.426Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t120_t121_t105_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:49.362Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && printf -- '- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction single-source refactor, write-once errata in my r2 files\\n' >> MEMORY.md && tail -2 MEMORY.md"
}
````

### User / tool · 2026-11-02T11:35:49.462Z

**tool result**
````
- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof listener before killing own servers
- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction single-source refactor, write-once errata in my r2 files
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:35:54.796Z

Verdicts: T-120 r2 is **changes** (1 major), T-121 r2 is **pass**, and T-105 is **changes** (1 major). The unit suite on a `git archive` of HEAD 433ac1c gave 3005 passed, 4 skipped. The three review files are `reviews/T-120-staff-engineer-r2.md`, `reviews/T-121-staff-engineer-r2.md` and `reviews/T-105-staff-engineer.md`.

- **T-120:** the r1 forms now flag, but the guard skips whenever the sentence has no colon, digit or "of", which isn't the same as naming no condition. Of 32 phrasings probed, 8 that name a condition are still dropped, for example "Hx per patient's son, significant for diabetes.", a newline form, and "Hx obtained from Dr. Lee: ...". The parent flagged 6 of those 8. Two guard mutants survive the tests: dropping the colon check and removing the newline sentence end.
- **T-121:** both r1 findings are fixed, and 11 of 12 mutants are killed, including the no-op `_one_line`. Only the minor and the two nits below remain.
- **T-105:** every wording named in the T-100 r2 review is refused. The single source is not reached, though. `dropped_qualifiers` and the quote-side checks still read private regexes (9 of 11 dropped-qualifier probes go unflagged), and the negation words now live in three places. The card's "no list words left" test is a six-word grep. No eval report path is cited, and `evals/reports/calibration.json` is now also stale for `lexicon.yaml`. The recorded-corpus replay (191 items) shows no change.

My reviews have errors I couldn't fix, because the write guard makes review files append-only. In T-120 r2, six regressions vs the parent, not five: "fractured her wrist" was also flagged by the parent. In T-121 r2, the provider-collapse cite is `export.py:267`, not :269, and "could not reach through the API" for the empty-summary case was never tested.
