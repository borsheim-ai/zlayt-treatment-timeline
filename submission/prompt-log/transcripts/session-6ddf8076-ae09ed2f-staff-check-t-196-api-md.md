# Subagent: Staff check: T-196 api.md (Staff check: T-196 api.md)

Source: `agent-ae09ed2fbc6f10c05.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T22:30:16.628Z

Check T-196 in /Users/arsis/zlayt-pm-project as the staff engineer. This is a mechanical doc check, starting from a fresh context. Read the card (`python3 tools/board.py show T-196`), reviews/T-179-staff-engineer-r2.md (its minor on the compare stamp), and SCOPE_CUTS row 25 in memory/SCOPE_CUTS.md.

Verify that memory/contracts/api.md at HEAD (`git show HEAD:memory/contracts/api.md`) no longer claims a disputed item is never accepted without the compare on record. It should state the second-commit take-back and point to SCOPE_CUTS 25. Also confirm the claim matches app/backend/review.py. Write reviews/T-196-staff-engineer.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:18.866Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T22:30:18.875Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:19.407Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-196; echo \"---\"; ls reviews/ | head -100; echo \"---\"; cat reviews/T-179-staff-engineer-r2.md",
 "description": "Show T-196 card and read T-179 r2 review"
}
````

### User / tool · 2026-11-02T22:30:19.544Z

**tool result**
````
---
id: "T-196"
title: "api.md: D-066 compare stamp wording matches behaviour (not atomic; taken back on failure)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T22:25:53Z"
updated_at: "2026-11-02T22:30:13Z"
claimed_by: "backend"
claimed_at: "2026-11-02T22:26:13Z"
rounds: 0
commits: ["9b40445"]
reviews: []
ac:
  - {"n": 1, "text": "memory/contracts/api.md no longer claims 'never accepted without the compare on record'; states the take-back and SCOPE_CUTS 25", "done": true, "evidence": "memory/contracts/api.md D-066 paragraph: stamp not atomic, second commit taken back on failure, concurrent reader or kill can see accepted disputed item without stamp; SCOPE_CUTS row 25; commit 9b40445"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T22:26:04Z orchestrator: assigned: backend
- 2026-11-02T22:26:05Z orchestrator: Queued: the backend worker on T-177 r4 takes this after T-177 (message sent).
- 2026-11-02T22:26:13Z backend: claimed
- 2026-11-02T22:26:30Z backend: AC 1 checked: memory/contracts/api.md D-066 paragraph: stamp not atomic, second commit taken back on failure, concurrent reader or kill can see accepted disputed item without stamp; SCOPE_CUTS row 25; commit 9b40445
- 2026-11-02T22:26:30Z backend: moved in_progress -> in_review
- 2026-11-02T22:30:13Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: one sentence in api.md D-066 paragraph. How verified: read back; git show 9b40445 is 1 line. Left: none. Surprised: T-177 r4 edits sit in the same file, committed separately via temp index.

---
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
GATE-M2-claims-adjuster.md
GATE-M2-legal-nurse.md
GATE-M2-paralegal.md
GATE-M2-privacy-compliance.md
GATE-M2-qa.md
GATE-M2-r2-claims-adjuster.md
GATE-M2-r2-legal-nurse.md
GATE-M2-r2-paralegal.md
GATE-M2-r2-staff-engineer.md
GATE-M2-round1-triage.md
GATE-M2-staff-engineer.md
GATE-M2-summary.md
GATE-M3-accessibility.md
GATE-M3-chaos-tester.md
GATE-M3-paralegal.md
GATE-M3-product-manager.md
GATE-M3-round1-triage.md
GATE-M3-staff-engineer.md
GATE-M3-ux-designer.md
MVP-ux-audit-r2.md
MVP-ux-audit-r3.md
MVP-ux-audit-r4.md
MVP-ux-audit.md
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
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
T-026-ux-designer.md
T-027-legal-nurse.md
T-028-staff-engineer-r2.md
T-028-staff-engineer.md
T-029-staff-engineer-r2.md
T-029-staff-engineer.md
T-030-staff-engineer-r2.md
T-030-staff-engineer-r3.md
---
# T-179 staff-engineer review, round 2 (commit 619f283)

Verdict: pass (0 blockers, 0 majors, 3 minors).

The round-1 major is fixed and I proved it by mutation. The D-067 test now builds a stored, accepted two-sentence paragraph, has an `=1` control, and asserts with no if-guard. Forcing `narrative_in_letter()` to `return True` fails `test_an_accepted_paragraph_never_reaches_the_letter_the_notes_or_the_json` at test_d067_narrative_cut.py:58. The round-1 survivor M5 (amount `disagree` mapping removed) is now killed by two tests. The api.md order claims now match the code and are pinned by mutants.

Two things are not as the handoff and api.md state. The `compared` stamp is still a second commit after the accept commit. The "taken back" repair is a compensation, not a transaction. A concurrent reader sees the accepted item with no stamp. The api.md sentence "a disputed item is never accepted without the compare on record" is false for a reader in that window and for a process crash. The held-quote sleep from F5 is unchanged; the card said it was out of scope. All three are minors.

## What I ran (all from `git archive 619f283` in the scratchpad `T179_r2`, never the shared tree)
- `tests/unit`: 5830 passed, 8 skipped in 338.47s. This matches the handoff. Output: `artifacts/review-evidence/T-179-r2/unit_full.txt`.
- e2e with `E2E_REQUIRE_DB=1`, 29 spec files that touch accept, batch, review, charges, the letter or the stepper:
  - Group A (review_matrix, ladder_gate, charge_confirm, count_charge, edit_to_check, rerun_judge, code_check_refusal, held_quote_gate, letter_isolation, charges, api, edit): 130 passed in 211.77s.
  - Group B (stepper, suggestions, uncovered_ui, letter_matrix, mvp_finish, mvp_polish, polish_r3/r4/r5, keyboard_mobile, rerun_note, export_ui, change_the_quote, conflict_skipped, no_console_errors, multicase, journey_modes): 225 passed, 1 skipped in 323.14s. The skips in these files are data or mode dependent (`pytest.skip` for "library cases need ZLAYT_MODE=local" and "this backend verified the edit"); I did not identify which one fired.
  - Outputs: `e2e_a.txt`, `e2e_b.txt`. `test_held_quote_gate.py` passed inside group A, 1 run.
- Mutants on 12 archive copies, `artifacts/review-evidence/T-179-r2/mutants.py`, results in `mutants_out.txt`. Each mutant printed `occurrences=1 changed=True` before running.
  - Killed: M1 (D-067 gate forced on, 1 failed), M2 (gate on unless "0", 1 failed), M3 (compare check off, 6 failed), M4 (batch allows disputed, 1 failed), M5 (`v = v`, 2 failed), M6 (stamp written for an undisputed item, 1 failed), M7 (stamp never written, 6 failed), M8 (no take-back on stamp failure, 1 failed), M10 (compare before the code checks, 1 failed), M11 (confirm before compare, 1 failed), M12 (batch reason renamed, 1 failed).
  - **Survived**: M9 (`"edited": "edit"` removed from the take-back map), 14 passed.
  - My first M11 used the wrong key (`item.get("flag")`), so it was a no-op and survived; I fixed it to `ladder.confirm` and the rerun was killed. Both runs are in `mutants_out.txt`.
- `probe_window.py` (reader on a second connection inside the stamp call, stamp failure plus take-back failure, process kill between the two commits) and `probe_edited_takeback.py` (stamp failure on a disputed edited entry, with and without M9).
- Read: `git show 619f283` for review.py, api.md and both test files; `app/db/db.py:215-237` (`apply_review` commits at line 233); `review.py:260-282`, `:333-345`; `memory/ORCHESTRATOR_DECISIONS.md` D-066 and D-067.

## Round-1 findings, checked
- **F1 (major) D-067 test cannot fail: fixed.** The test drafts and accepts real sentences (`entry_id` e1 and e5), proves with `=1` that they are in the letter, then asserts absence from letter, notes and the export JSON with the env var removed. M1 and M2 both fail it.
- **F2 (minor) non-atomic stamp: improved, not fixed.** See finding 1 below.
- **F3 (minor) api.md order and "ignored": fixed.** The doc says code checks, then COMPARE_REQUIRED, then CONFIRM_REQUIRED; the stamp is written only for a disputed item. `test_a_disputed_flagged_charge_needs_both_statements_compare_first` pins the order (M11 killed) and `test_the_code_checks_refuse_before_the_compare` pins code-checks-first (M10 killed). The undisputed `compared:true` test (M6 killed) pins "no key written". The doc sentence about the stamp being "written together with the accept" is the part that is not true (finding 1).
- **F4 (minor) charge, amount and code-check tests: fixed.** The disputed amount with verdict `disagree` and no reasons returns 422 COMPARE_REQUIRED (M5 killed, M7 killed). The batch test now reads `rej == {"e2": "judge_disputed", "e3": "judge_disputed"}` with no `if`. M12 kills it.
- **F5 (minor) held-quote sleep: not addressed.** `tests/e2e/test_held_quote_gate.py:93` still has `page.wait_for_timeout(300)`, and the commit touches no e2e file. The handoff states this. Carried as finding 3.

## Findings
1. The compared stamp is a compensation, not a transaction, and the doc says otherwise (minor). `DB.apply_review` commits the accept at db.py:233, then `_record_compared` opens its own BEGIN/COMMIT (review.py:333-345). The probe shows what a second connection sees in between: `status accepted, events [('accept', None)]`. With the stamp failing and the take-back also failing: HTTP 500 and the item stays `accepted` with `[('accept', None)]`. With the process killed inside the stamp: exit 9, item `accepted`, no stamp, and nothing ever reconciles it. api.md:382 says "if the stamp cannot be written the accept is taken back ... so a disputed item is never accepted without the compare on record". That holds only for a stamp exception that is followed by a successful take-back.
2. The "edited" take-back path has no test (minor). M9 leaves 14 passed. The probe shows the difference: on a disputed edited entry with a failing stamp, HEAD returns the item to `edited` and M9 leaves it `accepted`. The `"edited": "edit"` entry is new in 619f283.
3. Held-quote e2e keeps a bare 300 ms sleep and an unrecorded flake (minor, carried from round 1). Still at test_held_quote_gate.py:93.

Separate "violates a constraint" from preference: findings 1 to 3 are not spec-constraint violations. D-066 says the confirm "is stored on the review event" and does not require a single transaction; round 1 named the take-back as an acceptable fix. Finding 1 is minor because the doc claims more than the code delivers and a real transaction is cheap. Findings 2 and 3 are test-proof gaps.

```json
{"card": "T-179", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 619f283 (app/backend/review.py, memory/contracts/api.md, tests/unit/test_d066_compare_confirm.py, tests/unit/test_d067_narrative_cut.py; app/db/db.py read for the transaction boundary); tests/unit full, 29 tests/e2e spec files; no app URL (private test servers); round-1 review reviews/T-179-staff-engineer.md",
 "exercised": [
  "python3 tools/board.py show T-179; read reviews/T-179-staff-engineer.md, the card handoff, the r1 memory notes, personas/staff-engineer.md, D-066 and D-067",
  "git show 619f283 -- app/backend/review.py memory/contracts/api.md tests/ (every changed line)",
  "git archive 619f283 into the scratchpad T179_r2; .venv/bin/python -m pytest tests/unit -q -> 5830 passed, 8 skipped in 338.47s (artifacts/review-evidence/T-179-r2/unit_full.txt)",
  "E2E_REQUIRE_DB=1 pytest from the archive: group A 12 files, 130 passed in 211.77s (e2e_a.txt); group B 17 files, 225 passed, 1 skipped in 323.14s (e2e_b.txt); test_held_quote_gate.py inside group A",
  "artifacts/review-evidence/T-179-r2/mutants.py: M1..M12 on archive copies, each mutant printed occurrences=1 changed=True; M1-M8, M10, M11 (second attempt), M12 killed, M9 survived; first M11 was a no-op and is recorded as such (mutants_out.txt)",
  "artifacts/review-evidence/T-179-r2/probe_window.py: second-connection snapshot between accept commit and stamp commit; stamp failure plus take-back failure; process kill inside the stamp",
  "artifacts/review-evidence/T-179-r2/probe_edited_takeback.py on the HEAD archive and on the M9 mutant copy",
  "read app/db/db.py:215-237 (apply_review commits at 233), review.py:260-282 and 333-345, api.md:382; grep wait_for_timeout in the archive's test_held_quote_gate.py"
 ],
 "verdict": "pass",
 "scores": {"d066_enforcement": 4, "d067_cut_in_code": 5, "d067_test_strength": 5, "audit_trail_atomicity": 3, "contract_doc_accuracy": 4, "changed_tests_not_weakened": 5},
 "findings": [
  {"severity": "minor", "title": "The compared stamp is a second commit with a compensating take-back, so the doc claim 'never accepted without the compare on record' is false for a concurrent reader and for a crash",
   "evidence": "app/db/db.py:233 apply_review COMMITs the accept; app/backend/review.py:260-265 then calls _record_compared (review.py:333-345, its own BEGIN/COMMIT) and _take_back on failure. probe_window.py A: a second connection inside the stamp call sees \"accepted\", events [('accept', None)]. B: stamp raises and the take-back's apply_review raises -> status 500, e3 review_status accepted, events [('accept', None)]. C: process killed inside the stamp (exit 9) -> e4 review_status accepted, events [('accept', None)], never reconciled. memory/contracts/api.md:382: 'if the stamp cannot be written the accept is taken back ... so a disputed item is never accepted without the compare on record'.",
   "why_it_matters": "D-066 puts the compare on the review event so the audit can show a human compared a disputed summary. In the window, and after a crash or a failed take-back, a disputed item sits accepted, countable and exportable, with no compare on record, and the doc tells a client that cannot happen. A compensating repair also fails exactly when the DB is failing, which is when it is needed.",
   "fix": "Write after.compared in the same transaction as the accept: let DB.apply_review take an optional dict that is merged into the after_json it already inserts (the single INSERT at db.py:231-232), so the status UPDATE and the stamp commit together. Then drop _record_compared and the take-back for compared. If that is not wanted, change the api.md sentence to say the stamp is written right after the accept and is repaired best-effort, and say what a reader can see in between.",
   "acceptance_test": "Unit test: patch the stamp path to raise and assert the item is pending and has zero accept events (with the stamp inside apply_review it cannot be accepted without it). A second-connection snapshot taken inside the call never sees an accepted disputed item whose accept event lacks compared. Re-run probe_window.py: A, B and C show no accepted item without a stamp."},
  {"severity": "minor", "title": "The edited-status take-back has no test: removing it leaves all 14 D-066/D-067 tests green",
   "evidence": "review.py:280 '{\"pending\": \"reset\", \"dismissed\": \"dismiss\", \"edited\": \"edit\"}'. Mutant M9 (drop the 'edited' entry) -> '14 passed' (mutants_out.txt). probe_edited_takeback.py: disputed edited entry, stamp raises -> HEAD 'http 500 after take-back: edited'; M9 'http 500 after take-back: accepted'.",
   "why_it_matters": "The 'edited' mapping is new in 619f283. Without a test, a refactor of _take_back can leave an edited disputed item accepted with no compare on record and nothing fails. test_a_failed_compared_stamp_takes_the_accept_back covers only the pending case.",
   "fix": "Parametrize test_a_failed_compared_stamp_takes_the_accept_back over the starting status: pending, dismissed, and edited (edit e2 to clean wording first, then dispute it, then accept with compared:true under the failing stamp) and assert the status returns to the starting one.",
   "acceptance_test": "Rerun mutants.py M9: a test fails."},
  {"severity": "minor", "title": "Round-1 F5 not addressed: test_held_quote_gate.py keeps a bare 300 ms sleep and the flake assertion is still unrecorded",
   "evidence": "tests/e2e/test_held_quote_gate.py:93 'panel.locator(\"summary\").first.click(); page.wait_for_timeout(300)' in the 619f283 archive. 'git diff --stat f17c991 619f283 -- tests/e2e' lists no changed file under tests/e2e other than the guided specs that belong to another card. The handoff says F5 is frontend or qa owned and not touched. The test passed in group A (130 passed).",
   "why_it_matters": "A fixed sleep on a UI toggle is the pattern that fails under load, and the card note still does not record which assertion timed out in the 430-test run, so the next red run is dismissed the same way. It is a test-owner item, not a backend regression.",
   "fix": "Replace the sleep with an expect on the panel content, set an explicit expect timeout on the case-rail waits, and open a qa card for it if it is not in this card's scope. Record the failing assertion and line next time it times out.",
   "acceptance_test": "grep -n 'wait_for_timeout' tests/e2e/test_held_quote_gate.py returns nothing and the file passes in the load recipe from reviews/T-179-staff-engineer.md."}
 ],
 "whats_right": [
  "The D-067 test now builds real accepted sentences, proves them present with a flag-on control, and fails under two different gate mutants (M1, M2).",
  "The new D-066 tests pin the refusal order from both sides: M10 (compare before code checks) and M11 (confirm before compare) are each killed, and M5 and the batch reason are now killed too.",
  "The compared stamp is written only for a real compare on a disputed item (M6 killed), so the audit no longer overstates what she was asked to do."
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:19.735Z

**tool call — Bash**
````
{
 "command": "sed -n '1,80p' memory/SCOPE_CUTS.md",
 "description": "Read top of SCOPE_CUTS to locate row 25"
}
````

### User / tool · 2026-11-02T22:30:19.812Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:26.338Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>&1; git log --oneline -5 2>&1; echo \"--- HEAD api.md D-066 region ---\"; git show HEAD:memory/contracts/api.md 2>&1 | grep -n -i \"D-066\\|compare\\|taken back\\|take-back\\|SCOPE_CUTS\\|compared\" ; echo \"--- SCOPE_CUTS row 25 ---\"; grep -n \"^| 25 \\|^| 25|\" memory/SCOPE_CUTS.md; grep -n \"| 25 \" memory/SCOPE_CUTS.md; echo \"--- 9b40445 ---\"; git show --stat 9b40445 2>&1 | head -20",
 "description": "Check git state, api.md D-066 text at HEAD, SCOPE_CUTS row 25, and commit 9b40445"
}
````

### User / tool · 2026-11-02T22:30:26.501Z

**tool result**
````
true
3feb096 test(backend): T-177 r4 e2e: golden notes normalize the prepared disclosure line; classic tag tooltip stays exempt until the frontend card
c27e7f1 fix(backend): T-177 r4 D-069 prepared wording from templates keyed by provenance (no swap table); malformed or empty prepared answer is a missing one; property test over fault-injected curated sets
9b40445 docs(backend): T-196 api.md D-066 compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)
a5deecc docs(release): README walkthrough matches the guided UI labels; OWNER URL explained (T-182)
c5caf61 test(qa): skip history-dependent provenance tests in a one-commit snapshot (T-194)
--- HEAD api.md D-066 region ---
107:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
139:**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags, **computed each time the case is read from the current record dates (not stored)**, so `confirm_date` refreshes them together with the accident-date flag: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them has injury, mechanism or accident wording of its own that is not history or negated, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."). The decision is by content (T-141 round 3, no "a record is dated that day" shortcut): a record dated before the stated date makes the accident-date conflict when any clause of it has injury, mechanism or accident vocabulary (collision, crash, MVA/MVC, rear-end, struck, "hit by", pedestrian, incident, accident, injury, whiplash, LOC, trauma, impact, fall, airbag, seatbelt and similar) unless that clause is negated within five words ("denies any accidents", "no recent injuries") or is plainly history (a history word right before the word: "prior accident", "history of MVA", not "prior to the collision"; "last year", "N years ago", a full date over a year before the stated date, a month and year more than two months before the record, a bare year before the record's year). A safe false positive beats a hidden conflict: the conflict then compares with the earliest such record. **A case with no stored run summary** (analysed before per-case checks were kept) reports all four types in `skipped` with `NOT_RUN` and `conflict_types: []` (nothing is claimed; the UI renders an empty list as "none checked", not as the default list). `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.
284:- Accident-date conflict: the earliest dated record of ANY kind sets the comparison. If every record on that earliest date looks like paperwork, the explanation never says "first recorded treatment" for it: title "Stated accident date is later than the earliest record"; "... is later than the earliest recorded date, January 12, 2026 (record 1: <header>), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: <header> is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: <header>), and the stated date is not later than it. Check when treatment actually began before relying on this comparison." (`also later` when it is; "there is no recorded visit to compare with." when no visit exists). `first_treatment_date` keeps the earliest recorded date. A visit on the earliest date keeps the plain wording.
370:**An edit that is still `needs_review` is not decided (T-134; D-045b, D-051; paralegal pass 4 M2).** Saving the edit stays as above (`review_status: "edited"`, `state: "needs_review"`), but until the paralegal says she compared it with the quote it is **open**, one rule in all places:
372:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
376:- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.", and the item `verdict` is `{code: "edit_to_check", label: "Edited; waiting for your check"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / "Accepted by you". A verified edit (state not `needs_review`) still reads "You edited this item and accepted it.". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).
380:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
382:**D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amount judge's `disagree`), or whose `reasons` hold `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_DISAGREES` (`unsure` / `unavailable` are not an objection). `POST .../items/{id}/review {action: "accept"}` on such an item, without `compared: true`, is `422 COMPARE_REQUIRED` and nothing is written: `error.detail = {item_id, reason_code: "COMPARE_REQUIRED", verdict, next_action: {code: "COMPARE_WITH_QUOTE", ...}}`, the message names which check objected. With `compared: true` it is accepted as before and the statement is kept on the accept event (`after.compared = {at}`; `GET .../audit` `events[]` carries `compared: {at}`, also in public mode). The order of refusals on one accept is: the code checks (D-051, so a failing code check stays `CODE_CHECK_FAILED`), then `COMPARE_REQUIRED`, then the charge confirm (D-059, `CONFIRM_REQUIRED`); a disputed flagged charge therefore needs `compared: true` and the named `confirm` together, and its accept event carries both. The statement is stored only when the item was disputed: `compared: true` on an item nobody disputed is accepted as before and writes no `compared` key. It is not atomic with the accept: the stamp is a second commit after the accept, and if it cannot be written the accept is taken back (item returns to its earlier status) and the call fails. A concurrent reader, or a process killed between the two commits, can therefore see an accepted disputed item without its stamp (SCOPE_CUTS row 25; making it one transaction is post-MVP). `compared` must be a boolean (else `422 invalid_edit`); it is ignored on dismiss, reset and edit. **Batch accept (`POST .../review/batch`)** never takes such an item: the whole batch is refused (all or nothing, like every other refusal) with the item listed as `{id, reason: "judge_disputed"}`; the client leaves disputed items out of "accept all verified". `count` clears the judge, so a counted charge is not disputed.
417:`POST .../items/{id}/review` with `{"action": "count", "confirm": "separate_charge"}` (an amount only; `400 bad_request` for an entry or flag, `409 item_rejected` for a rejected amount) counts a countable amount: it becomes class `charge` and is `accepted` in one step, so the letter total (R-EX-8) sums it like any accepted charge; no second AI check is asked (it is her decision with a named confirm: `judge_required_for_export: false`, `second_check_pending: false`, the trace's `judge_2` step is `skipped` with "you counted this line ... and confirmed it by name", `why` says so). Response: the review response shape (`item`, `totals`, `review`, `warnings`) plus `amount` (the case-view shape, `kind: "charge"`) and `reclassified: {from, to: "charge", counted: true, confirm: "separate_charge"}`. Errors, all `422` with `detail.reason_code` equal to the code and nothing changed: `NOT_COUNTABLE` (message "This amount cannot be counted. <not_counted_reason>"; `detail.not_counted_reason`; also for an amount that is already a charge: "This amount is already a charge. Accept it to count it."); `CONFIRM_REQUIRED` for a missing or wrong `confirm` (`detail: {flag: "separate_charge", name: "Counted as a separate charge", confirm_with: "separate_charge", message, not_counted_reason}`); `CONFIRM_REQUIRED` naming `likely_duplicate` or `likely_total` (send that flag as `confirm_flag`; `detail.flag`, `detail.confirm_with`, `detail.of` = the other amount's id): `likely_duplicate` when ANOTHER live amount of the case (any record, the same record too) that is an accepted or pending charge, or is itself countable, has the same amount and the same service and a compatible date; the service is normalized (round 3): codes meet, or the shorter description's words each have an equivalent in the other (word families and abbreviations: PT / physical therapy, pt / patient, xray / x-ray / radiograph, ther ex / therapeutic exercise, OV / office visit, e-stim, eval / exam), or a CPT code meets its description when the case itself states both on one line; a code the case never describes, against a described line at the same amount, is asked about (candidate, not decided). Over-flagging costs one more named confirm (a date is compared only when both lines state one; a line with no date of service may be the same visit as a dated one). `separate_charge` alone is never enough for a line that matches; both lines of a pair are flagged, and after one is counted the other matches an accepted charge. `likely_total` when the figure equals the sum of at least two other charges of its record. Every amount in `amounts[]` also carries `count_confirm`: `null`, or for a countable amount that would need such a flag `{flag, name, message, confirm_with, of}` (the same object the 422 `detail` carries), so the screen can show the warning before the click. A non-string `confirm` is `422 invalid_edit`. The charge then carries `flag: {flag: "separate_charge", name: "Counted as a separate charge", confirmed_at, ...}` (or the duplicate/total flag it was counted with); after a `reset` the next `accept` needs the flag's `confirm_with` again (`confirm_required: true`), a `dismiss` takes it out of the total, and a rerun keeps it. Audit (`GET .../audit`, also in public mode as metadata): two events for the item, in order: `action: "reclassify"` whose local-mode `after` is `{event: "count", kind: "charge", review_status: "accepted", confirm: {flag: "separate_charge", name, confirmed_at}, not_counted_reason, confirm_flag}` (`before: {kind, review_status, state}`) and, in `events[]`, `confirm: {flag: "separate_charge", name, confirmed_at}`; then the `accept` event, which carries the confirm of the flag the charge holds. `ladder.counted = {confirm, at, by: "reviewer", not_counted_reason}`; `ladder.code_checks.classified_by = "reviewer:counted"`. The internal notes' `AMOUNTS NOT TOTALED` list drops a counted amount. Balance wording (round 2): "Amount unpaid that the provider has a right to be paid: $2,660.00" says Balance (lib15 affidavit), not Payment. Checked on every library case, both by summing every countable amount and by counting each with only the named confirm: never exceeds the case's hand-verified `explicit_charges_total` (lib11: $3,260 + $250 + $180 + $2,310 = $6,000.00) and the adjuster's t140 ledgers (r1 to r3, restating labels) have no countable amount.
419:**`totals.possible_overlaps` (T-110, D-019; every response that carries `totals`).** Array, normally empty. One object per pair of a billing-statement line and a separately stated charge that name the same kind of service (closed family table in `app/backend/overlap.py`: consult, physical therapy, imaging, emergency, ambulance, injection, surgery, laboratory; English and Spanish) when the charge's record date is inside the statement's date range (two dates written in the statement text, else on or before the statement's own date). Fields: `code: "POSSIBLE_OVERLAP"`, `statement_amount_id`, `covered_amount_id`, `statement_record_id`, `covered_record_id`, `statement_text`, `covered_text` (the figures as written), `service`, `range: {from, to, stated}`, `date_known` (false when the charge's record date is not confirmed: it is listed, not ruled out), `both_charges` (both are class `charge`), `both_in_total` (both are accepted, so the accepted total currently contains both), `message` (one of three fixed sentences; never model text). Rates, estimates, damages, dismissed and unreadable figures are never parties, nor are statement balance/total/payment/adjustment lines or two figures of one record. **The warning never changes `totals.accepted`, `pending` or `detected_not_a_total`, and no figure is subtracted, merged or compared: the total still adds stated charges only.** The frontend shows each warning beside the total with both figures and the message; the paralegal dismisses one of the two if the statement line includes the other. **Export (T-110 r2):** when `possible_overlaps` is not empty, `internal_notes_text` gets a section `POSSIBLE OVERLAPS (check before relying on the charges total)` after `AMOUNTS NOT TOTALED`, one plain-words line per pair naming both records and both figures (and whether both are in the total); with none, the notes are byte-for-byte as before. The letter never mentions an overlap.
425:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the only change to the quote is whitespace (each run of spaces and line breaks becomes one space); a translated entry adds ` — English: <summary>` after the bracket, before the translation note; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
617:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the action is `POST /rejudge`), `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.
628:  "next_action": { "code": "COMPARE_BY_HAND", "text": "...", "target": {"item_id": "e4"} },
641:      "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
729:**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `hitl.needs_review_open` (T-157 r3) is the number of items still open in Needs review: `state: needs_review` and (`review_status: pending` or an unconfirmed edit, `edit_to_check`), i.e. exactly the set `next_action` picks from and the items of `GET /api/cases/{token}` that wait for the paralegal; a reworded entry counts, an accepted item that is still `needs_review` does not (so it is at most `needs_review`). `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
772:**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. **Figure fields on an extra line, `other_figures`, a running `balance`, and everything in `eob` are never summed or compared by a client.** `other_figures` (a list of `{text, cents, usd}`, empty when none) holds every OTHER money token printed on a rate, estimate or LOP/lien row, wherever a parser first put it: the running balance on a price row (a no-cents one such as `$315` keeps its text with `cents: null`), a second amount in an LOP or rate sentence (the first amount is the entry, the later ones are its other figures), a printed balance or total on that row. A token on such a row is never also a line of its own, with no exception: on a UB-04 room row the FL 44 figure is the rate entry and the FL 47 total (and any non-covered figure) is one of that entry's `other_figures` (T-103 r4, T-110 r2). No token is reachable only by reading the excerpt; each text sits inside the excerpt (`verify_citations`: `other_figure_not_in_excerpt`). The class is `unclear` because the code does not decide what such a figure means. A figure that is both an LOP amount and a printed balance is one line.
773:**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept). A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. **Nothing is merged or deduplicated across records or providers (T-103 r3):** two providers printing the same row are two lines, a re-sent statement is two lines (one per record, each citing only its own record, so `record_nos` has one entry), and a line is identified by its record and its position in it (`id` follows record order, then position). Only a byte-identical copy of a whole record is dropped, at ingest (`duplicate_of`). CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a `rate` and the `0001` line is a printed total. A fee-schedule or per-unit figure is a rate; a table row or a sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate; one shared test, `amounts.has_rate_cue`, also used by reclassify) is a rate even beside the word charge or billed, is listed once, and a `RATE` column's figures are rates too. A ledger-table figure with no cents (`$185`, `185`) under a money column stays on its row as `unclear` text (`LINE_UNCLEAR`); on a rate row it is a `rate` line with `cents: null`, and a no-cents balance on a rate row is that rate's `other_figures` entry. A blank DOS cell stays blank (`dos: null`, `NO_DATE_OF_SERVICE`); the posting date is never read as the service date. A figure with OCR letters, other than two decimals, or inside an injection-tagged record has `cents: null` / the record is in `skipped_records`. A billing-looking record in no known layout is a `skipped_records` entry `UNRECOGNISED_BILLING_FORM`. An EOB service row (date, service code, then one figure per header column: BILLED, DISCOUNT, ALLOWED, DEDUCT, COINS, PLAN PAID, YOU MAY OWE) is a line of form `eob`; it is never compared with the ledger, so a difference in billed or paid is simply two cited lines. A service code and the number in a reason code (`PR-1`, `CO-45`) are not money. Every cited excerpt anywhere in the response (lines, cites, unreconciled) is checked against the record's own text, and every figure text (including each `eob` figure) against its excerpt, by `verify_citations`, which the route runs on every call; failures are returned as `citation_failures` and make the status `citation_failed`.
--- SCOPE_CUTS row 25 ---
109:| 25 | Compare stamp atomic with the accept (T-179 r2 minor) | The D-066 compare stamp is a second commit after the accept with a take-back on failure; a concurrent reader or a process kill can see an accepted disputed item without its stamp. api.md must say "taken back if the stamp fails", not "never". | Move the stamp into DB.apply_review's transaction (app/db); ~0.5 day. | post-MVP |
109:| 25 | Compare stamp atomic with the accept (T-179 r2 minor) | The D-066 compare stamp is a second commit after the accept with a take-back on failure; a concurrent reader or a process kill can see an accepted disputed item without its stamp. api.md must say "taken back if the stamp fails", not "never". | Move the stamp into DB.apply_review's transaction (app/db); ~0.5 day. | post-MVP |
--- 9b40445 ---
commit 9b4044599be1384172dd6de0b02ff6013d8d96e4
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 16:26:26 2026 -0600

    docs(backend): T-196 api.md D-066 compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 memory/contracts/api.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:27.125Z

**tool call — Bash**
````
{
 "command": "git show HEAD:memory/contracts/api.md | grep -n \"never accepted without\" ; echo \"rc=$?\"; echo \"--- full D-066 paragraph at HEAD ---\"; git show HEAD:memory/contracts/api.md | awk '/D-066/{f=1} f{print NR\": \"$0} /D-067/{if(f)exit}' | head -60",
 "description": "Grep for the disputed-accept claim and print the D-066 paragraph at HEAD"
}
````

### User / tool · 2026-11-02T22:30:27.240Z

**tool result**
````
rc=1
--- full D-066 paragraph at HEAD ---
382: **D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amount judge's `disagree`), or whose `reasons` hold `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_DISAGREES` (`unsure` / `unavailable` are not an objection). `POST .../items/{id}/review {action: "accept"}` on such an item, without `compared: true`, is `422 COMPARE_REQUIRED` and nothing is written: `error.detail = {item_id, reason_code: "COMPARE_REQUIRED", verdict, next_action: {code: "COMPARE_WITH_QUOTE", ...}}`, the message names which check objected. With `compared: true` it is accepted as before and the statement is kept on the accept event (`after.compared = {at}`; `GET .../audit` `events[]` carries `compared: {at}`, also in public mode). The order of refusals on one accept is: the code checks (D-051, so a failing code check stays `CODE_CHECK_FAILED`), then `COMPARE_REQUIRED`, then the charge confirm (D-059, `CONFIRM_REQUIRED`); a disputed flagged charge therefore needs `compared: true` and the named `confirm` together, and its accept event carries both. The statement is stored only when the item was disputed: `compared: true` on an item nobody disputed is accepted as before and writes no `compared` key. It is not atomic with the accept: the stamp is a second commit after the accept, and if it cannot be written the accept is taken back (item returns to its earlier status) and the call fails. A concurrent reader, or a process killed between the two commits, can therefore see an accepted disputed item without its stamp (SCOPE_CUTS row 25; making it one transaction is post-MVP). `compared` must be a boolean (else `422 invalid_edit`); it is ignored on dismiss, reset and edit. **Batch accept (`POST .../review/batch`)** never takes such an item: the whole batch is refused (all or nothing, like every other refusal) with the item listed as `{id, reason: "judge_disputed"}`; the client leaves disputed items out of "accept all verified". `count` clears the judge, so a counted charge is not disputed.
383: 
384: **D-067 (T-179): the drafted treatment paragraph is out of the MVP.** The `/narrative` routes stay, but the export never carries it: `letter_text` has no `TREATMENT SUMMARY` and `internal_notes_text` no paragraph lines, whatever the paragraph's status, unless the server runs with `NARRATIVE_IN_LETTER=1` (for the narrative's own tests and its future eval). The classic page offers no panel or Draft button.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:31.317Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/review.py | grep -n \"compared\\|_take_back\\|_record_compared\\|COMPARE_REQUIRED\\|def \\|apply_review\\|judge_disputed\\|invalid_edit\" | head -120",
 "description": "Locate compare, take-back and accept functions in review.py at HEAD"
}
````

### User / tool · 2026-11-02T22:30:31.410Z

**tool result**
````
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
4:Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
6:invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
25:    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
30:def _now(now):
34:def _item(conn, case_id, item_id):
44:def _bad(msg, **detail):
45:    return ReviewError(422, "invalid_edit", detail, msg)
48:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
60:def _date_unconfirmed_error():
79:def current_text(item: dict):
84:def edit_unconfirmed(kind: str, item: dict) -> bool:
86:    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
93:def code_check_failures(rec, item: dict) -> dict:
118:def code_check_message(fails: dict) -> str:
143:def code_check_detail(item_id: str, fails: dict) -> dict:
151:def code_check_error(item_id: str, rec, item: dict):
159:def bill_state_for(conn, case_id: str, record_ids) -> str:
165:def charge_text_error(item_id: str, item: dict, state_fn=None):
180:def hold_hints(conn, case_id: str, entry_views: list) -> None:
195:def entry_record(item: dict, recs: list):
200:def confirm_error(item_id: str, item: dict, confirm):
213:def confirmed_accept(item: dict) -> bool:
219:def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
238:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None, compared=None) -> dict:
239:    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
253:    if action == "accept" and (err := compare_error(item_id, item, compared, conn, case_id)):      # D-066: after the code checks (they refuse first), before any write
261:    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
262:    if action == "accept" and compared is True and judge_dispute(item):
264:            _record_compared(conn, case_id, item_id, now)       # D-066 r2: only a real compare is stamped; a failed stamp takes the accept back, so nothing disputed is accepted without it on record
266:            _take_back(conn, case_id, item_id, item, now)
273:            _take_back(conn, case_id, item_id, item, now)      # T-159 r2: take the accept back, so no charge counts without its confirm on record
279:def _take_back(conn, case_id: str, item_id: str, item: dict, now) -> None:
283:        DB.apply_review(conn, item_id, back, now=now, case=case_id)
290:def check_fresh(item: dict, body: dict, action: str) -> None:
314:def judge_dispute(item: dict):
326:def compare_error(item_id: str, item: dict, compared, conn=None, case_id=None):
327:    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
329:    if not v or compared is True or item.get("review_status") == "accepted":
335:    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
336:                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
337:                       (_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v] + " Read it against the quote, then say you compared it before you accept it.")
340:def _record_compared(conn, case_id: str, item_id: str, t) -> None:
341:    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
347:            conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "compared": {"at": store.iso(t)}}), ev["id"]))
354:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
373:        compared = body.get("compared")
374:        if compared is not None and not isinstance(compared, bool):
375:            raise _bad("The compared flag must be true or false.")
376:        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm, compared=compared)
388:def ocr_record_ids(conn, case_id: str) -> set:
398:def enforce_ocr(conn, case_id: str, t) -> int:
401:    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
427:def _quoted_words(toks) -> str:
432:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False, bill_state=None):
435:    cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
475:def _edit(conn, case_id, kind, item, body, call, t):
548:def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
578:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
606:    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
616:def _without_date_doubt(item: dict) -> dict:
631:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
639:def _drop(conn, case_id, flag_id):
644:def _gap_figures(flag: dict) -> dict:
649:def _gap_changes(old: dict, new: dict) -> list:
672:def _gap_change_sentence(ch: dict, seq) -> str:
681:def _recompute_gaps(conn, case_id, t, changes=None):
714:            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
725:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
727:    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
765:    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
775:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
831:    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
839:def _upsert(conn, case_id, kind, item, t):
849:def judges_for(dollars, call, case_text):
855:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
857:    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:31.765Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/db/db.py | sed -n '205,245p'",
 "description": "Read DB.apply_review transaction boundary at HEAD"
}
````

### User / tool · 2026-11-02T22:30:31.856Z

**tool result**
````
        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
    table, found = _find(conn, item_id, case)
    bad = set(fields) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    fields["updated_at"] = now
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])


def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
    if action not in ACTIONS:
        raise ValueError(f"invalid review action {action!r}")
    table, row = _find(conn, item_id, case)
    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
    status = ACTIONS[action] or row["review_status"]
    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
    if action == "edit" and not new_edited:
        raise ValueError("edit requires a non-empty edited payload")
    after = {"review_status": status, "edited": new_edited}
    conn.execute("BEGIN")
    try:
        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return get_item(conn, item_id, row["case_id"])


def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
    if action not in AUDIT_ONLY_ACTIONS:
        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
    eid = _tok("v")
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:33.518Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/review.py | sed -n '238,290p'; echo \"-----\"; git show HEAD:app/backend/review.py | sed -n '314,352p'; echo \"----- apply_review call site -----\"; git show HEAD:app/backend/review.py | sed -n '354,387p'",
 "description": "Read set_review, take-back, compare checks and apply_review call site at HEAD"
}
````

### User / tool · 2026-11-02T22:30:33.666Z

**tool result**
````
def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None, compared=None) -> dict:
    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
    if kind is None or item is None:
        kind, item = _item(conn, case_id, item_id)
    if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):
        cand = dict(item)
        if edited is not None:
            cand["edited"] = edited
            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand) or charge_text_error(item_id, cand, lambda: bill_state_for(conn, case_id, item.get("record_ids")))
        if err:
            raise err
    if action == "accept" and (err := compare_error(item_id, item, compared, conn, case_id)):      # D-066: after the code checks (they refuse first), before any write
        raise err
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        if confirmed_accept(item):
            return item                                     # T-159: already accepted with its flag confirmed; a repeat accept writes no second decision
        err = confirm_error(item_id, item, confirm)         # D-059
        if err:
            raise err
    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
    if action == "accept" and compared is True and judge_dispute(item):
        try:
            _record_compared(conn, case_id, item_id, now)       # D-066 r2: only a real compare is stamped; a failed stamp takes the accept back, so nothing disputed is accepted without it on record
        except Exception:
            _take_back(conn, case_id, item_id, item, now)
            raise
        out = DB.get_item(conn, item_id, case_id)
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        try:
            _record_confirm(conn, case_id, item_id, item, now)
        except Exception:
            _take_back(conn, case_id, item_id, item, now)      # T-159 r2: take the accept back, so no charge counts without its confirm on record
            raise
        out = DB.get_item(conn, item_id, case_id)
    return out


def _take_back(conn, case_id: str, item_id: str, item: dict, now) -> None:
    """Undo an accept whose stamp (compare or confirm) could not be written: back to the status the item had before."""
    back = {"pending": "reset", "dismissed": "dismiss", "edited": "edit"}.get(item.get("review_status"))
    if back:
        DB.apply_review(conn, item_id, back, now=now, case=case_id)


STALE_MESSAGE = "This item changed in another tab; reload to see it."
_TARGET_STATUS = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}


def check_fresh(item: dict, body: dict, action: str) -> None:
-----
def judge_dispute(item: dict):
    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only."""
    j = (item.get("ladder") or {}).get("judge")
    v = j.get("verdict") if isinstance(j, dict) else None
    v = "disagrees" if v == "disagree" else v        # the amount-class judge says "disagree"
    if v in _DISPUTED:
        return v
    reasons = item.get("state_reasons") or []
    return next((k for k, code in _DISPUTED.items() if code in reasons), None)


def compare_error(item_id: str, item: dict, compared, conn=None, case_id=None):
    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
    v = judge_dispute(item)
    if not v or compared is True or item.get("review_status") == "accepted":
        return None
    prep = False
    if conn is not None:
        from app.backend import present          # lazy: present imports review
        prep = present.Prov(conn, case_id).prepared(item)      # D-069: the sentence follows the item's provenance
    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
                       (_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v] + " Read it against the quote, then say you compared it before you accept it.")


def _record_compared(conn, case_id: str, item_id: str, t) -> None:
    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
    ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
    if ev:
        after = json.loads(ev["after_json"]) if ev["after_json"] else {}
        conn.execute("BEGIN")
        try:
            conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "compared": {"at": store.iso(t)}}), ev["id"]))
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

----- apply_review call site -----
def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    check_fresh(item, body, action)
    if action == "count":
        from app.backend import count_charge          # lazy: count_charge imports review
        return count_charge.count(conn, case_id, item_id, body, now=t)
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        confirm = body.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise _bad("The confirm must be the name of the flag.")
        compared = body.get("compared")
        if compared is not None and not isinstance(compared, bool):
            raise _bad("The compared flag must be true or false.")
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm, compared=compared)
        if action == "reset":
            restore_pre_edit(conn, case_id, item_id, kind, item, t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:30:56.784Z

**tool call — Bash**
````
{
 "command": "echo \"--- compare on record anywhere in api.md at HEAD ---\"; git show HEAD:memory/contracts/api.md | grep -n -i \"compare on record\\|never accepted\"; echo \"rc=$?\"; echo \"--- api.md diff 9b40445 -> HEAD ---\"; git diff --stat 9b40445 HEAD -- memory/contracts/api.md; echo \"--- 9b40445 api.md change ---\"; git show 9b40445 -- memory/contracts/api.md | grep \"^[-+]\" | cut -c1-400; echo \"--- working tree vs HEAD ---\"; git diff --stat HEAD -- memory/contracts/api.md app/backend/review.py; echo \"--- _take_back callers / accepted mapping / compared read in _edit ---\"; git show HEAD:app/backend/review.py | grep -n \"_take_back\\|\\\"accepted\\\"\" ; git show HEAD:app/backend/review.py | grep -n \"compared\" ; echo \"--- rejudge can change verdict on accepted item? ---\"; git grep -n \"def rejudge\\|rejudge(\" HEAD -- app/backend | head -10; echo \"--- tests on take-back ---\"; git grep -n \"takes_the_accept_back\\|_take_back\\|compare on record\\|COMPARE_REQUIRED\" HEAD -- tests/unit | head -20",
 "description": "Check api.md for residual claim, diff since 9b40445, take-back mapping, rejudge path and related tests"
}
````

### User / tool · 2026-11-02T22:30:56.857Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  HEAD ---)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:00.746Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/feedback_guard_blocks_shell_expansions.md 2>/dev/null | head -30; echo ---; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md 2>/dev/null | head -30; echo ---; cat .claude/agent-memory/staff-engineer-reviewer/feedback_reviewer_scratch_writes.md 2>/dev/null | head -30",
 "description": "Read memory notes on guard behaviour and review write-once"
}
````

### User / tool · 2026-11-02T22:31:00.837Z

**tool result**
````
---
name: feedback_guard_blocks_shell_expansions
description: git-guard and board-guard refuse shell parameter expansion in command position, and board.py commands with 2> redirects; do citation loops in a python -I script under artifacts/review-evidence
metadata:
  type: feedback
---

A bash `for` loop with `${spec%%:*}` expansions was blocked by git-guard ("unresolved variable or substitution in command position"), and a
`cd ... && python3 tools/board.py ... 2>&1` line was blocked by board-guard ("`2>` is not allowed" for reviewers, which may only run
validate/show/list/status read-only). Whole blocked commands do not run, so a helper script written in the same command is never created.

**Why:** T-173 r1 (this session): the first citation loop and the first check script both failed silently at the hook, and I only found
out from a later "No such file" error.

**How to apply:** for citation checks and output parsing, write the script with the Write tool under artifacts/review-evidence/<card>-r<n>/
and run it with `.venv/bin/python -I`. Use plain `python3 tools/board.py validate` without redirects. Do not use `$var` expansions in a
shell loop.

Related: [[feedback_review_write_once]] (proof-read citations before the first Write).

**T-175 r2 addendum:** board-guard denied `git branch` for reviewers in the project ("allowed only in scratch repos under /tmp"). `git merge-base --is-ancestor <sha> HEAD` and `git log -S <string> -- <paths>` both ran. A plain `python3 -c "import time; time.sleep(100)"` in the foreground ran without a block, but it is a poor habit: check the background task instead.
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

**T-141 r5 addendum:** the first Write carried one control claim I had not yet run ("V10 and W10 print info on 93a2ffc"). It was true, but the guard then refused an Edit to fix a muddled sentence about it. Run every "X prints Y on the control archive" claim before the first Write, and proof-read the evidence sentence, not only the JSON. Accurate-but-clumsy wording can stay, but it cannot be corrected in place. See [[project_t141_r5_patterns]].

**T-173 r2 addendum:** the first Write had one clumsy sentence and one citation range one line too wide (conftest.py:208-211 for a guard at 208-210). Both stayed, because Edit was refused on the new file, and I did not work around the guard. Proof-read the body the same way as the JSON block before the Write, and read each cited range with `git show <sha>:<path> | sed -n` first. A shell line with a backtick inside a `python -c` string was denied by git-guard ("could not parse command safely"); put any fence or regex with backticks in a script file.

**T-045 r3 addendum:** three function line ranges in the exercised list were written from memory of grep output (ship_bar 913-960 should be 913-955; render_md 1058-1092 should be 1093; check_fresh 1294-1313 should be 1315). The findings' own citations were grepped and correct. I did not work around the guard; the slip stays in the record. Run `grep -n "^def "` and `sed -n` on each range before the first Write, and list each range as you verified it. See [[project_t045_r3_record_latest_patterns]].

**T-155 r2 / T-164 addendum:** two wrong body facts went out in first Writes: a file name (test_multicase.py for test_rerun_note.py) and "the card names X" when the card does not. Both were caught only after the Write. Before the first Write, grep each file name and each "the card says" phrase against `board.py show` output. The corrected records are `-r2b` and `-r1` files, and each names the file it corrects. See [[project_t155_r2_t164_patterns]].
---
---
name: reviewer-scratch-writes
description: Reviewer Write tool is blocked outside reviews/ and artifacts/review-evidence/ (scratchpad refused); keep helper scripts and sweep outputs there; shell lines with backticks or triple backticks trip the board guard
metadata:
  type: feedback
---

Write tool calls to the session scratchpad were refused by reviewer-write-guard. Shell `cp` and `cat >` into the scratchpad still worked. Keep reviewer helper scripts and copied evidence in artifacts/review-evidence/<card>-rN/ so the Write tool is allowed.

**Why:** the write guard allows only reviews/, artifacts/review-evidence/ and the agent memory dir. The scratchpad is outside that list for Write, and the error came back on the first Write.

**How to apply:** put sweep scripts, mutants and copied outputs under artifacts/review-evidence/. Do not put backticks or triple backticks inside a shell command line; the git-guard board-guard denies unparseable commands. Write a small .py file instead and run it with python -I.

**T-169 r2 addendum:** `git clone` plus `git checkout --detach <sha>` was denied by board-guard when the clone sat under artifacts/review-evidence/ ("reviewers may not run git checkout in the project"). The same two commands worked in a clone under the session scratchpad (/private/tmp/...), so put pinned clones in the scratchpad and evidence in artifacts/review-evidence/. A python -c line containing backtick-escaped fences was also denied; use a .py file.

Related: [[project_t167_plain_wording_patterns]], [[feedback_bind_to_named_reference]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:03.293Z

**tool call — Bash**
````
{
 "command": "git show HEAD:memory/contracts/api.md > /private/tmp/claude-501/api_head.md 2>/dev/null; git show HEAD:memory/contracts/api.md | grep -c \"compare on record\"",
 "description": "Count residual compare-on-record wording in api.md at HEAD"
}
````

### User / tool · 2026-11-02T22:31:03.415Z

**tool result**
````
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:03.988Z

**tool call — Bash**
````
{
 "command": "git diff --stat 9b40445 HEAD -- memory/contracts/api.md; git diff --stat HEAD -- memory/contracts/api.md app/backend/review.py app/db/db.py; git log --oneline -3 -- memory/contracts/api.md",
 "description": "Check api.md changes since 9b40445 and working-tree drift"
}
````

### User / tool · 2026-11-02T22:31:04.117Z

**tool result**
````
 memory/contracts/api.md | 7 ++++---
 1 file changed, 4 insertions(+), 3 deletions(-)
c27e7f1 fix(backend): T-177 r4 D-069 prepared wording from templates keyed by provenance (no swap table); malformed or empty prepared answer is a missing one; property test over fault-injected curated sets
9b40445 docs(backend): T-196 api.md D-066 compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)
619f283 fix(backend): T-179 r2 compared stamped only for a disputed item and taken back if the stamp fails; D-067 default-off test now asserts (killed by forcing the gate on); direct tests for disputed amount, flagged charge, code-check-first; api.md order corrected
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:04.504Z

**tool call — Bash**
````
{
 "command": "git show 9b40445 -- memory/contracts/api.md | grep \"^[-+][^-+]\" | cut -c1-200",
 "description": "Show the exact one-line api.md change in commit 9b40445"
}
````

### User / tool · 2026-11-02T22:31:04.598Z

**tool result**
````
-**D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amoun
+**D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amoun
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:07.525Z

**tool call — Bash**
````
{
 "command": "git grep -n \"rejudge\" HEAD -- app/backend/review.py app/backend/server.py app/backend/judge.py 2>/dev/null | head -15",
 "description": "Find rejudge path that could change a judge verdict on an accepted item"
}
````

### User / tool · 2026-11-02T22:31:07.623Z

**tool result**
````
HEAD:app/backend/review.py:530:        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
HEAD:app/backend/review.py:532:    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
HEAD:app/backend/review.py:550:    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
HEAD:app/backend/review.py:562:    if snap.get("rejudge"):
HEAD:app/backend/review.py:563:        lad["rejudge"] = snap["rejudge"]
HEAD:app/backend/review.py:565:        lad.pop("rejudge", None)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:08.198Z

**tool call — Bash**
````
{
 "command": "git grep -n \"takes_the_accept_back\\|test_a_disputed_flagged_charge\\|COMPARE_REQUIRED\" HEAD -- tests/unit | head -12",
 "description": "Locate unit tests covering compare refusal and take-back"
}
````

### User / tool · 2026-11-02T22:31:08.301Z

**tool result**
````
HEAD:tests/unit/test_d066_compare_confirm.py:2:JUDGE_DISAGREES reason) needs the explicit `compared: true` statement ("I compared it with the quote"). Without it: 422 COMPARE_REQUIRED, nothing written.
HEAD:tests/unit/test_d066_compare_confirm.py:56:    assert "COMPARE_REQUIRED" in blob and "compared" in blob and verdict in blob
HEAD:tests/unit/test_d066_compare_confirm.py:123:def test_a_failed_compared_stamp_takes_the_accept_back(env, monkeypatch):
HEAD:tests/unit/test_d066_compare_confirm.py:150:        assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED", r.text         # not COMPARE_REQUIRED
HEAD:tests/unit/test_d066_compare_confirm.py:175:    assert r.status_code == 422 and r.json()["error"]["code"] == "COMPARE_REQUIRED" and r.json()["error"]["detail"]["verdict"] == "disagrees", r.text
HEAD:tests/unit/test_d066_compare_confirm.py:183:def test_a_disputed_flagged_charge_needs_both_statements_compare_first(tmp_path, monkeypatch):
HEAD:tests/unit/test_d066_compare_confirm.py:193:    assert code(_post(c, tok, f["id"])) == "COMPARE_REQUIRED"                                  # compare first (documented order)
HEAD:tests/unit/test_d066_compare_confirm.py:194:    assert code(_post(c, tok, f["id"], confirm="likely_duplicate")) == "COMPARE_REQUIRED"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:09.998Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/unit/test_d066_compare_confirm.py | sed -n '123,145p'",
 "description": "Read the take-back unit test at HEAD"
}
````

### User / tool · 2026-11-02T22:31:10.104Z

**tool result**
````
def test_a_failed_compared_stamp_takes_the_accept_back(env, monkeypatch):
    db, c = env
    tok = run_case(c)
    _dispute(db, tok, "e2", "disagrees", "JUDGE_DISAGREES")

    def boom(*a, **k):
        raise RuntimeError("stamp write failed")
    monkeypatch.setattr(RV, "_record_compared", boom)
    assert _post(c, tok, "e2", compared=True).status_code == 500
    assert _status(db, tok, "e2") == "pending"                  # never left accepted without the compare on record
    monkeypatch.undo()
    ok = _post(c, tok, "e2", compared=True)
    assert ok.status_code == 200 and _status(db, tok, "e2") == "accepted"
    acc = [e for e in _events(db, tok, "e2") if e["action"] == "accept"][-1]
    assert acc["after"]["compared"]["at"]


def test_the_code_checks_refuse_before_the_compare(env):
    db, c = env
    tok = run_case(c)
    conn = DB.connect(db)
    ed = dict(DB.get_item(conn, "e3", tok)["edited"] or {}, summary="Persistent neck pain 9/10 with daily headaches noted.")      # a figure the quote does not carry
    DB.apply_review(conn, "e3", "edit", edited=ed, now=1.0, case=tok)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:25.271Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && cd /Users/arsis/zlayt-pm-project && git archive HEAD | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && git rev-parse HEAD && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 | head -30",
 "description": "Extract HEAD into a scratchpad copy for running the D-066 tests"
}
````

### User / tool · 2026-11-02T22:31:26.361Z

**tool result**
````
3feb096208e835cf9bf4cba9e59f6fa05c8f705f
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:28.958Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && timeout 600 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q -p no:cacheprovider 2>&1 | tail -15",
 "description": "Run the D-066 compare unit tests against the HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T22:31:29.118Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:31.171Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q -p no:cacheprovider 2>&1 | tail -15",
 "description": "Run the D-066 compare unit tests against the HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T22:31:35.475Z

**tool result**
````
...........                                                              [100%]
11 passed in 3.99s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:38.804Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && grep -rn \"compared\" app/backend --include=*.py | grep -v \"^app/backend/review.py\" | head -8; grep -n \"compared\" app/backend/review.py | head -12; sed -n '40,46p' app/backend/review.py; sed -n '279,284p' app/backend/review.py",
 "description": "Check audit exposure of compared stamp and line refs in the archive"
}
````

### User / tool · 2026-11-02T22:31:38.908Z

**tool result**
````
app/backend/trace.py:744:        st.append(step("computed", "Dates compared by code" if ftype == "gap" else "Stated and recorded dates compared by code", "code", PASS,
app/backend/trace.py:1231:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and {pick('the AI', 'the prepared answers')}.", rule="row 9", counts=fc))
app/backend/spanish_text.py:4:The D-034 token checks need the English summary compared with a SPANISH quote, so this module maps the Spanish
app/backend/billing.py:43:    "Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.",
app/backend/billing.py:357:    as printed, compared with nothing."""
app/backend/billing.py:583:# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
app/backend/billing.py:780:    shown once. Positions decide all of this; no figure text is compared."""
app/backend/present.py:96:    """D-064 r2: the case's other lines a countable line is compared with (amounts.count_flag): every live charge and every countable amount, read once per list and only when a
86:    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
238:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None, compared=None) -> dict:
253:    if action == "accept" and (err := compare_error(item_id, item, compared, conn, case_id)):      # D-066: after the code checks (they refuse first), before any write
262:    if action == "accept" and compared is True and judge_dispute(item):
264:            _record_compared(conn, case_id, item_id, now)       # D-066 r2: only a real compare is stamped; a failed stamp takes the accept back, so nothing disputed is accepted without it on record
326:def compare_error(item_id: str, item: dict, compared, conn=None, case_id=None):
327:    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
329:    if not v or compared is True or item.get("review_status") == "accepted":
336:                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
337:                       (_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v] + " Read it against the quote, then say you compared it before you accept it.")
340:def _record_compared(conn, case_id: str, item_id: str, t) -> None:
341:    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
        raise ReviewError(404, "not_found", message="No such item.")
    return _KIND[item_id[0]], row


def _bad(msg, **detail):
    return ReviewError(422, "invalid_edit", detail, msg)

def _take_back(conn, case_id: str, item_id: str, item: dict, now) -> None:
    """Undo an accept whose stamp (compare or confirm) could not be written: back to the status the item had before."""
    back = {"pending": "reset", "dismissed": "dismiss", "edited": "edit"}.get(item.get("review_status"))
    if back:
        DB.apply_review(conn, item_id, back, now=now, case=case_id)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:41.618Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && grep -rn \"def audit\\|\\\"events\\\"\" app/backend/*.py | head -6",
 "description": "Locate the audit builder that emits events[]"
}
````

### User / tool · 2026-11-02T22:31:41.698Z

**tool result**
````
app/backend/api.py:670:    def audit(token: str):
app/backend/present.py:540:    return {"item": item, "source": src, "calls": calls, "events": events}
app/backend/present.py:556:def audit_view(conn, case_id, full=False):
app/backend/present.py:563:            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
app/backend/trace.py:320:          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:43.683Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && sed -n '556,572p' app/backend/present.py",
 "description": "Read audit_view event fields to confirm compared is exposed"
}
````

### User / tool · 2026-11-02T22:31:43.765Z

**tool result**
````
def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
                        **({"compared": e["after"]["compared"]} if (e.get("after") or {}).get("compared") else {}),      # T-179 / D-066: she said she compared it with the quote
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                        "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}


def case_list(conn):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:31:51.852Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && grep -n \"^ACTIONS\" app/db/db.py; ls /Users/arsis/zlayt-pm-project/reviews/ | grep \"T-196\"; echo \"exit=$?\"",
 "description": "Confirm the ACTIONS map used by the take-back and that no T-196 review exists yet"
}
````

### User / tool · 2026-11-02T22:31:51.944Z

**tool result**
````
19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:05.094Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T196 && grep -n \"def apply_review\\|conn.execute(\\\"BEGIN\\\")\\|conn.execute(\\\"COMMIT\\\")\" app/db/db.py | head; grep -n \"compared\" app/backend/present.py | head -3; grep -n \"def _record_compared\" -A 12 app/backend/review.py | grep -n \"BEGIN\\|COMMIT\" ; grep -n \"_record_compared\" app/backend/review.py",
 "description": "Get exact line numbers for DB transaction boundaries and audit exposure"
}
````

### User / tool · 2026-11-02T22:32:05.311Z

**tool result**
````
92:        conn.execute("COMMIT")
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
227:    conn.execute("BEGIN")
233:        conn.execute("COMMIT")
287:    conn.execute("BEGIN")
291:        conn.execute("COMMIT")
96:    """D-064 r2: the case's other lines a countable line is compared with (amounts.count_flag): every live charge and every countable amount, read once per list and only when a
565:                        **({"compared": e["after"]["compared"]} if (e.get("after") or {}).get("compared") else {}),      # T-179 / D-066: she said she compared it with the quote
6:345-        conn.execute("BEGIN")
9:348-            conn.execute("COMMIT")
264:            _record_compared(conn, case_id, item_id, now)       # D-066 r2: only a real compare is stamped; a failed stamp takes the accept back, so nothing disputed is accepted without it on record
340:def _record_compared(conn, case_id: str, item_id: str, t) -> None:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:34.027Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-196-staff-engineer.md",
 "content": "# T-196 staff-engineer review (doc check, HEAD 3feb096, card commit 9b40445)\n\nVerdict: pass (0 blockers, 0 majors, 1 nit).\n\nThe T-179 r2 minor is closed in the doc. `memory/contracts/api.md` at HEAD no longer says a disputed item is \"never accepted without the compare on record\". The D-066 paragraph (line 382) now says the stamp is a second commit, that a failed stamp takes the accept back and the call fails, that a concurrent reader or a process killed between the two commits can see an accepted disputed item without its stamp, and it points at SCOPE_CUTS row 25 (line 109, post-MVP). Every mechanism the paragraph names matches `app/backend/review.py` and `app/db/db.py` at HEAD. The one gap is in what the take-back covers, not in what the doc says.\n\nModel note: the brief expects claude-sonnet-5-5, but this review was run by claude-haiku-5-5, so the JSON records that id.\n\n## What I ran (read-only; the shared tree was not written)\n- `python3 tools/board.py show T-196`: status in_review, AC 1 done, commits [9b40445], rounds 0. Quoted in the card note: \"AC 1 checked: ... SCOPE_CUTS row 25; commit 9b40445\".\n- Read `reviews/T-179-staff-engineer-r2.md`: minor finding 1 (the compared stamp is a compensation, and the api.md sentence \"never accepted without the compare on record\" is false in the window). Also minor finding 2 (edited take-back untested).\n- Read `memory/SCOPE_CUTS.md` line 109: `| 25 | Compare stamp atomic with the accept (T-179 r2 minor) | ... api.md must say \"taken back if the stamp fails\", not \"never\". | Move the stamp into DB.apply_review's transaction (app/db); ~0.5 day. | post-MVP |`\n- `git show HEAD:memory/contracts/api.md | grep -n \"never accepted without\"`: no match, exit 1. `git show HEAD:memory/contracts/api.md | grep -c \"compare on record\"`: 0.\n- `git show HEAD:memory/contracts/api.md | awk` over the D-066 block: line 382 reads \"**D-066 (T-179): a disputed item is accepted only with her compare.** ... if it cannot be written the accept is taken back (item returns to its earlier status) and the call fails. A concurrent reader, or a process killed between the two commits, can therefore see an accepted disputed item without its stamp (SCOPE_CUTS row 25; making it one transaction is post-MVP).\"\n- `git show 9b40445 -- memory/contracts/api.md`: one line changed (`-` old sentence, `+` new sentence), commit message \"...compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)\". `git diff --stat 9b40445 HEAD -- memory/contracts/api.md` shows later edits (c27e7f1, 3feb096, T-177 r4) elsewhere in the file; I read the HEAD D-066 paragraph itself, which contains the new text.\n- `git diff --stat HEAD -- memory/contracts/api.md app/backend/review.py app/db/db.py`: no output (no working-tree drift from HEAD).\n- Claim-to-code check at HEAD (read with `git show HEAD:<path>`):\n  - `app/backend/review.py:238-276` `set_review`: code checks (247-252), then `compare_error` (253, refuses before any write), then the charge confirm (255-260). Order matches the paragraph: code checks, COMPARE_REQUIRED, CONFIRM_REQUIRED.\n  - `review.py:261` `DB.apply_review` (the accept commit), `:262` `if action == \"accept\" and compared is True and judge_dispute(item)`, `:264` `_record_compared`, `:266-267` `_take_back` then `raise`. The stamp is written only for a disputed item with `compared: true`; that matches \"The statement is stored only when the item was disputed\".\n  - `review.py:279-283` `_take_back`: map `{\"pending\": \"reset\", \"dismissed\": \"dismiss\", \"edited\": \"edit\"}`, then `DB.apply_review`. Matches \"item returns to its earlier status\" for those three statuses.\n  - `review.py:326-337` `compare_error`: returns None when `compared is True` or `review_status == \"accepted\"`; otherwise 422 COMPARE_REQUIRED with `reason_code`, `verdict`, `next_action.code` COMPARE_WITH_QUOTE. Matches the paragraph.\n  - `review.py:340-349` `_record_compared`: its own `BEGIN` (345) and `COMMIT` (348), updating the latest accept event's `after` with `compared: {at}`. Separate from the accept transaction.\n  - `review.py:348-349` and `:354-376` (`apply_review` route): `compared` must be a bool, else `_bad` (422 invalid_edit, `review.py:44-45`). Matches \"else 422 invalid_edit\". `compared` is read only for accept, dismiss and reset (`:373`); the edit branch goes to `_edit`. Matches \"ignored on dismiss, reset and edit\".\n  - `app/db/db.py:215-233` `apply_review`: `BEGIN` at 227, `COMMIT` at 233, one transaction for the status UPDATE and the event INSERT. The stamp is not inside it. Matches \"a second commit after the accept\".\n  - `app/db/db.py:19` `ACTIONS` maps `edit` to `edited`, which the `_take_back` map relies on.\n  - `app/backend/present.py:565`: `audit_view` exposes `compared` in each `events[]` entry in metadata mode, so \"GET .../audit events[] carries compared: {at}, also in public mode\" holds.\n- `git archive HEAD | tar -x -C <scratchpad>/T196`, then from that copy `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q -p no:cacheprovider`: \"11 passed in 3.99s\". Covers the COMPARE_REQUIRED order and the take-back test at `test_d066_compare_confirm.py:123`.\n\n## Nit (not a spec violation, does not change the verdict)\nThe take-back map at `review.py:281` has no key for `accepted`. `compare_error` (`review.py:329`) returns None for an already-accepted item, so a re-accept with `compared: true` of an item that a later judge run disputed reaches the stamp at 262-267. If that stamp fails, `_take_back` does nothing, the call returns 500, and the item stays accepted with no stamp. The doc sentence \"item returns to its earlier status\" is true for that item (it is still accepted), but the doc does not say what happens in this case, and `test_a_failed_compared_stamp_takes_the_accept_back` (line 123) covers pending only. I did not reproduce it: I did not drive a judge rerun that disputes an accepted item, so reachability is from code reading only. Outside the T-196 AC.\n\n## Scores\n- The old overclaim is gone and the doc states the second commit, the take-back and SCOPE_CUTS 25.\n- The paragraph's mechanisms match review.py, db.py and present.py at HEAD (table above).\n- SCOPE_CUTS row 25 exists with matching wording and a cost line.\n- Take-back coverage of the cases the doc implies: pending, dismissed and edited mapped in code; accepted not mapped and not tested.\n\n```json\n{\"card\": \"T-196\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git HEAD 3feb096 (card commit 9b40445): memory/contracts/api.md D-066 paragraph line 382; app/backend/review.py (set_review, compare_error, _record_compared, _take_back); app/db/db.py apply_review; app/backend/present.py audit_view; memory/SCOPE_CUTS.md row 25 line 109; tests/unit/test_d066_compare_confirm.py. Doc and unit check; no app URL.\",\n \"exercised\": [\n  \"python3 tools/board.py show T-196: in_review, AC 1 done, commits [9b40445]\",\n  \"read reviews/T-179-staff-engineer-r2.md findings 1-3 and memory/SCOPE_CUTS.md row 25 (line 109)\",\n  \"git show HEAD:memory/contracts/api.md | grep -n 'never accepted without': no match (exit 1); grep -c 'compare on record': 0\",\n  \"git show HEAD:memory/contracts/api.md D-066 paragraph read in full (line 382): second commit, take-back on failure, concurrent reader or kill window, SCOPE_CUTS row 25, post-MVP\",\n  \"git show 9b40445 -- memory/contracts/api.md: one-line change in the D-066 paragraph; git diff --stat 9b40445 HEAD on api.md shows later T-177 r4 edits outside it\",\n  \"git diff --stat HEAD on api.md, review.py, db.py: no output (no working-tree drift)\",\n  \"git show HEAD:app/backend/review.py read at set_review 238-276, compare_error 326-337, _record_compared 340-349, _take_back 279-283, apply_review route 354-376, judge_dispute 314-323\",\n  \"git show HEAD:app/db/db.py read at apply_review 215-233 (BEGIN 227, COMMIT 233) and ACTIONS line 19\",\n  \"git show HEAD:app/backend/present.py audit_view line 565: compared exposed in events[] metadata\",\n  \"git archive HEAD into the session scratchpad T196; .venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q: 11 passed in 3.99s\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"old_overclaim_removed\": 5, \"doc_matches_review_py\": 4, \"scope_cuts_25_link\": 5, \"take_back_coverage_of_doc_cases\": 3},\n \"findings\": [\n  {\"severity\": \"nit\", \"title\": \"Take-back has no branch for an item already accepted when a re-accept's stamp fails; the doc does not say what happens there\",\n   \"evidence\": \"app/backend/review.py:281 back = {\\\"pending\\\": \\\"reset\\\", \\\"dismissed\\\": \\\"dismiss\\\", \\\"edited\\\": \\\"edit\\\"}.get(item.get(\\\"review_status\\\")) has no accepted key; review.py:329 compare_error returns None when review_status is accepted, so a re-accept with compared:true reaches the stamp at review.py:262-267; a failed stamp then runs _take_back (no-op) and raises. tests/unit/test_d066_compare_confirm.py:123 test_a_failed_compared_stamp_takes_the_accept_back covers pending only. Not reproduced: no judge rerun that disputes an accepted item was driven.\",\n   \"why_it_matters\": \"api.md:382 says the accept is taken back and the item returns to its earlier status. For an already-accepted item the status is unchanged and the call fails, which the doc does not describe. The sentence is not false as written, and the case is outside the one-sentence T-196 AC.\",\n   \"fix\": \"Either state in api.md that a failed re-stamp on an already-accepted item leaves the item accepted and the call fails, or add a defined take-back target for accepted and test it.\",\n   \"acceptance_test\": \"Parametrize test_a_failed_compared_stamp_takes_the_accept_back over pending, dismissed, edited and accepted (accept, then dispute with the _dispute helper, then re-accept with compared:true under a failing _record_compared) and assert the status the doc names.\"}\n ],\n \"whats_right\": [\n  \"api.md at HEAD replaces the 'never accepted without the compare on record' sentence with the second-commit take-back and a pointer to SCOPE_CUTS 25; grep for the old wording returns nothing.\",\n  \"The refusal order (code checks, COMPARE_REQUIRED, confirm), the bool check for compared, the stamp-only-when-disputed rule and the take-back for pending, dismissed and edited all match review.py at HEAD line for line.\",\n  \"SCOPE_CUTS row 25 carries the matching wording (api.md must say taken back, not never) with a cost line and post-MVP; the D-066 unit file passes 11/11 on a HEAD archive.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T22:32:34.188Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-196-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:43.549Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-196-staff-engineer.md",
 "old_string": "  - `review.py:348-349` and `:354-376` (`apply_review` route): `compared` must be a bool, else `_bad` (422 invalid_edit, `review.py:44-45`). Matches \"else 422 invalid_edit\". `compared` is read only for accept, dismiss and reset (`:373`); the edit branch goes to `_edit`. Matches \"ignored on dismiss, reset and edit\".",
 "new_string": "  - `review.py:373-375` (inside the `apply_review` route, 354-376): `compared` must be a bool, else `_bad` (422 invalid_edit, `review.py:44-45`). Matches \"else 422 invalid_edit\". `compared` is read only for accept, dismiss and reset; the edit branch goes to `_edit`. Matches \"ignored on dismiss, reset and edit\"."
}
````

### User / tool · 2026-11-02T22:32:43.597Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-196-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:48.358Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -15",
 "description": "Run board validator read-only to check the review file"
}
````

### User / tool · 2026-11-02T22:32:48.527Z

**tool result**
````
ok (196 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:52.210Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && wc -l MEMORY.md && tail -3 MEMORY.md && ls | grep -c \"\\.md$\"",
 "description": "Check memory index length before adding an entry"
}
````

### User / tool · 2026-11-02T22:32:52.324Z

**tool result**
````
     113 MEMORY.md
- [Consistent forgery probe](feedback_consistent_forgery_probe.md) — recompute-from-document checks: probe header+body+pointer together, not only header flips
- [T-179 D-066/D-067 patterns](project_t179_d066_d067_patterns.md) — conditional-branch test never runs, regex misses heading, stamp outside txn
- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested
114
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:57.004Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t196_doc_claim_patterns.md",
 "content": "---\nname: t196-doc-claim-patterns\ndescription: T-196 doc-only check: api.md take-back claim vs review.py map keys; accepted pre-state unmapped; append-only file blocked a line-range fix\nmetadata:\n  type: project\n---\n\nT-196 (api.md D-066 compare stamp wording, HEAD 3feb096) passed with 1 nit. Recurring shapes for doc-only cards that describe a compensation path:\n\n- **Check the compensation map keys, not just the prose.** `_take_back` (review.py:279-283) maps only pending, dismissed and edited. The doc says \"item returns to its earlier status\"; an item already accepted has no key and no take-back. Grep the map for every status the doc's \"earlier status\" could be.\n- **Test coverage for the path can be one status.** test_a_failed_compared_stamp_takes_the_accept_back covers pending only (line 123).\n- **Confirm the refusal order in code, not in the doc.** set_review (review.py:238-276): code checks, compare_error, confirm.\n- **Shell expansions and `2>` in one command trip board-guard.** Split greps into separate calls; no `$?` echo chains with pipes into grep alternations.\n- **Reviews are append-only after the first Write.** A wrong line range in the body (review.py:348-349 written for the bool check; it is 373-375) could not be fixed with Edit; the guard refused it. Proof-read cites with sed before the first Write.\n\n**Why:** T-196 was a one-sentence doc change whose claim depended on a compensation mapping; the nit and the mis-cite both came from not checking each cited range before writing.\n\n**How to apply:** for any doc sentence that says \"X is taken back / returns to Y\", grep the code's map or mapping dict for every status the sentence could cover, and cite each line with sed -n before the first Write.\n\nRelated: [[project_t179_d066_d067_patterns]], [[feedback_review_write_once]], [[feedback_guard_blocks_shell_expansions]].\n"
}
````

### User / tool · 2026-11-02T22:32:57.104Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t196_doc_claim_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:32:58.539Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && tail -c 1 MEMORY.md | od -c | head -2",
 "description": "Check trailing newline in memory index before appending"
}
````

### User / tool · 2026-11-02T22:32:58.622Z

**tool result**
````
0000000   \n                                                            
0000001
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:33:00.300Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 111,
 "limit": 3
}
````

### User / tool · 2026-11-02T22:33:00.313Z

**tool result**
````
111	- [Consistent forgery probe](feedback_consistent_forgery_probe.md) — recompute-from-document checks: probe header+body+pointer together, not only header flips
112	- [T-179 D-066/D-067 patterns](project_t179_d066_d067_patterns.md) — conditional-branch test never runs, regex misses heading, stamp outside txn
113	- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:33:02.330Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested",
 "new_string": "- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested\n- [T-196 doc-claim patterns](project_t196_doc_claim_patterns.md) — take-back map lacks accepted; append-only file kept a wrong cite range"
}
````

### User / tool · 2026-11-02T22:33:02.440Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:33:04.345Z

T-196 passes (0 blockers, 0 majors, 1 nit): api.md at HEAD now states the second-commit take-back and cites SCOPE_CUTS 25, and it matches review.py. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-196-staff-engineer.md` (validator ok, 196 files); the nit is that a re-accept of an already-accepted disputed item has no take-back branch (review.py:281), which the doc doesn't cover. The body cites review.py:348-349 for the bool check where it should be 373-375; the file is append-only so I left it, and the record shows model claude-haiku-5-5 rather than the expected Sonnet id.
