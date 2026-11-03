# T-039 review - staff-engineer-reviewer (Marcus Lee lens)

Scope: commit a3068ed (tests/unit/test_export.py, tests/unit/test_review_rules.py, tests/e2e/*, stubs app/backend/export.py and review.py). Working tree at review time already had uncommitted edits by other workers (HEAD a2fc95a), including app/backend/export.py; the unit run below still failed only with NotImplementedError.

Exercised:
- `python3 tools/board.py show T-039` (9 AC)
- `.venv/bin/python -m pytest tests/unit/test_export.py tests/unit/test_review_rules.py -q` -> `39 failed, 2 passed`; every `E` line is `NotImplementedError` (19 + 20). The 2 passes are `test_letter_builder_takes_no_flags_argument` (signature on stub) and `test_no_bulk_accept_exists`.
- `.venv/bin/python -m pytest tests/e2e -q -rs` -> `57 skipped`, each with reason "app server not running at http://localhost:7860 (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)". 13 files, matches AC4.
- Read all of both unit files, conftest.py and all 13 E2E specs; read golden `evals/golden/sample.export.expected.txt`, `memory/contracts/api.md`, `tests/unit/_fakes.py`, `_golden.py`.
- Scripted a testid cross-check (specs vs conftest docstring) and `which_record(G.raw('case_01_date_formats'))` -> `[]`.
- Mutation spot-check and CLI determinism run: not applicable (no implementation yet; tests-first card).

AC coverage verdict: golden byte-equal (R-EX-6), D-019 total line, case_07 $420, no `flags` parameter, 7-of-9 with 5 dismissed and 6 pending, EDITED ITEMS, 422/409 matrix, `date_invalid`, `$1,2OO` to notes, `$185` accept leaving 839000 are all encoded. The problems are in how three helpers/specs are wired and in contract completeness, not in missing AC rows. No blocker (no float money, no network, no secrets, no LLM in assembly).

```json
{"card": "T-039", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit a3068ed; tests/unit/test_export.py, tests/unit/test_review_rules.py, tests/e2e/*; HEAD a2fc95a with dirty tree; app not running (:7860 down); sample + case_01/03/07 goldens",
 "exercised": [
  "python3 tools/board.py show T-039",
  ".venv/bin/python -m pytest tests/unit/test_export.py tests/unit/test_review_rules.py -q -> 39 failed (all NotImplementedError), 2 passed",
  ".venv/bin/python -m pytest tests/e2e -q -rs -> 57 skipped with explicit :7860 reason",
  "read test_export.py, test_review_rules.py, e2e/conftest.py and all 13 e2e specs line by line",
  "read evals/golden/sample.export.expected.txt, memory/contracts/api.md, tests/unit/_fakes.py, tests/unit/_golden.py",
  "script: data-testid set used by specs vs conftest contract docstring; data-review/data-state/role/key hooks listed",
  ".venv/bin/python -c which_record(G.raw('case_01_date_formats')) -> []",
  "grep for record_nos/record_ids/raw across tests/unit to compare pipeline output shapes",
  "mutation spot-check and CLI determinism: not applicable, no implementation"],
 "verdict": "changes",
 "scores": {"ac_encoding": 4, "red_for_the_right_reason": 3, "test_strength": 3, "e2e_contract_completeness": 2, "determinism_and_isolation": 5},
 "findings": [
  {"severity": "major", "title": "E2E data-testid contract is incomplete: specs rely on undeclared hooks",
   "evidence": "tests/e2e/conftest.py docstring says specs use 'ONLY these test ids / roles' but specs also need: attribute data-review (pending|accepted|edited|dismissed) at test_review_matrix.py:10,15,20,21,31, test_edit.py:12,18, test_keyboard_mobile.py:10; attribute data-state at test_timeline.py:20; role=alert at test_input.py (pdf refusal); inputs named date/provider at test_edit.py (locator input[name=date], input[name=provider]); [tabindex] on queue rows at test_keyboard_mobile.py:9; keyboard shortcuts 'a' (test_keyboard_mobile.py:9), 'j' (test_side_by_side.py:17). Script output: set of data-* attrs used = {data-review, data-state, data-flag-type}; only data-flag-type is in the docstring. Conversely status-stage, flag-<id>, flag-evidence, review-ready, btn-copy-notes are declared but no spec uses them.",
   "why_it_matters": "The frontend cards (T-040..T-046) build to this docstring. A frontend that follows it literally fails about 12 specs for reasons nobody can see in the contract, and a vacuous negative (count()==0) will pass anyway. The point of tests-first is that the contract is the single source.",
   "fix": "Add to the conftest docstring: data-review and its four values on entry/amount/flag containers, data-state (verified|needs_review|rejected), role=alert for refusals, keyboard shortcuts a/d/j and Enter, [tabindex] on queue rows, input names date/provider (absent by design), the btn-source inside flag-<id>. Drop or justify the declared-but-unused ids, or add the specs that use them.",
   "acceptance_test": "A script that extracts every get_by_test_id/locator/get_by_role hook from tests/e2e/test_*.py and asserts each is named in the conftest docstring; run it in the unit suite."},
  {"severity": "major", "title": "Review-rule helpers are keyed to the wrong shapes; ~28 tests will fail for the wrong reason once the pipeline exists",
   "evidence": "tests/unit/test_review_rules.py: `def ent(out, n): return [e for e in out[\"entries\"] if e[\"record_nos\"] == [n]][0][\"id\"]` but tests/unit/_fakes.py items_for uses `record_ids` with 'r{n}' and memory/contracts/api.md entries carry `record_ids: [\"r2\"]` (no record_nos on entries). Also seeded(tmp_path, \"case_01_date_formats\") (test_confirm_date_non_candidate_is_422_date_invalid) wires the sample extract lambda: `which_record(G.raw('case_01_date_formats'))` returns [] so `sums[which_record(u)[0]]` raises IndexError inside the extract fake. Today all 28 seeded tests die at app/backend/pipeline.py:5 NotImplementedError, which masks both.",
   "why_it_matters": "Tests-first is red-then-green. These will go red with KeyError/IndexError after M2 lands, which looks like a backend bug and wastes the M3 backend worker's time or invites them to bend the pipeline output to the helper.",
   "fix": "Use `\"r%d\" % n in e[\"record_ids\"]` (or the _fakes.items_for helper) in ent(); for non-sample seeds use a case-aware extract (which_record(u, case)) or sample_script-style fake keyed on the case; add a smoke test that seeded() works on a stub pipeline output shape.",
   "acceptance_test": "Unit test that calls ent(out, 5) on a hand-built out dict shaped like api.md and returns the id, and a seeded('case_01_date_formats') run against a fake pipeline that does not IndexError."},
  {"severity": "major", "title": "Letter-isolation E2E can pass vacuously: accept calls unchecked, no positive assertion",
   "evidence": "tests/e2e/test_letter_isolation.py::test_letter_has_no_flag_or_note_content: the loops `api(\"POST\", .../review, {\"action\": \"accept\"})` and the note edit ignore the status code, and the only asserts are `assert b not in t` over BAD. If every accept returns 409/422 (for example item_rejected, or a wrong body) the letter is empty and the test is green.",
   "why_it_matters": "This is the R-EX-1 'letter has no flag content' proof at the system level. An empty letter satisfies it. Same class as tests that pass when the thing under test is stubbed out.",
   "fix": "Assert status 200 for accepts (skip rejected items explicitly), assert the note edit returned 200, and assert positives before the negatives: letter starts with TREATMENT CHRONOLOGY, has 9 dated headings and the total line.",
   "acceptance_test": "Run the spec against a server whose review endpoint always returns 409: the spec must fail."},
  {"severity": "minor", "title": "Edit E2E assertions would pass without the new text; 'edited' label not checked",
   "evidence": "tests/e2e/test_edit.py::test_notes_list_edited_item_with_both_texts asserts `\"EDITED ITEMS\" in n and \"daily headaches\" in n`; 'daily headaches' is in the ORIGINAL summary (golden: 'Persistent neck pain 6/10, daily headaches'), so it is satisfied by the original alone. AC6/T-044 requires original and new text. test_edit_summary_labelled_and_persists checks the data-review attribute, not a visible 'edited' label; its docstring also promises 'letter has no edited' but never reads the letter.",
   "why_it_matters": "AC6 ('edited summary and edited label persist; notes list original and new') is only proven at unit level.",
   "fix": "Assert the exact original sentence and the exact new sentence appear in the EDITED ITEMS section; assert a visible 'edited' label text; fetch export-letter and assert 'edited' absent.",
   "acceptance_test": "Mutate the notes builder to drop original_summary: the E2E spec must fail."},
  {"severity": "minor", "title": "Negative-only UI assertions pass when the element does not exist",
   "evidence": "tests/e2e/test_charges.py::test_rate_has_no_edit_path: `get_by_test_id(\"amount-$185\").get_by_test_id(\"btn-edit\").count() == 0` (true if the row is missing); tests/e2e/test_review_matrix.py::test_rejected_item_cannot_be_accepted `rejected-tray ... btn-accept count() == 0` (true if the tray is missing); test_source_record.py::test_record_text_is_inserted_as_text asserts no script/img/iframe in the modal, but the sample records contain no markup and demo mode (D-020) refuses unrecorded text, so the spec cannot fail on an innerHTML bug.",
   "why_it_matters": "R-CH-7 and the textContent invariant look covered but are not. (XSS depth belongs to security-reviewer; flagging only.)",
   "fix": "Precede each count()==0 with a positive existence check (row visible, accept button present on the sibling row); for the markup test use a recorded case or inject via a test-only fixture hook and assert the literal string appears as text.",
   "acceptance_test": "Remove the amount-$185 row from the DOM: test_rate_has_no_edit_path must fail."},
  {"severity": "minor", "title": "Export unit tests: pending count fixture inconsistent, total not asserted for $1,2OO case, narrow forbidden list",
   "evidence": "tests/unit/test_export.py::test_dismiss_5_pending_6_reconciliation_and_counts sets entry 6 'pending' but leaves case['pending_count']=0, so the AI line 'Items not reviewed: N' (golden notes line 4) is never checked as 1 in the dismissed/pending scenario. tests/unit/test_review_rules.py::test_accept_unclear_amount_goes_to_notes_not_letter docstring says 'not in the letter or total' but asserts only \"1,2OO\" absent and '$95.00' present, never the total line. test_export.py::test_letter_has_no_flag_content forbids 7 strings; the E2E list also forbids 'Prior condition', 'REVIEWER NOTE', 'supplemented', 'Pending items', 'of 9', and the unit case never gives a flag a reviewer note.",
   "why_it_matters": "These are the places a builder that leaks a note, a count or an unclear amount into the carrier letter would slip through.",
   "fix": "Derive or set pending_count=1 in the 5/6 scenario and assert 'Items not reviewed: 1'; assert 'Billed charges stated in these records: $95.00' in the case_03 test; share one BAD list between unit and E2E and set a reviewer note on a flag in the unit case.",
   "acceptance_test": "A builder that emits 'Items not reviewed: 0' regardless, or appends flag notes to the letter, makes a unit test fail."},
  {"severity": "minor", "title": "$185 accept test double-accepts and does not check the letter",
   "evidence": "tests/unit/test_review_rules.py::test_accept_rate_keeps_total_8390: loop accepts '$6,240','$2,150','$185', then accepts '$185' a second time and asserts only totals.accepted.cents == 839000 on the second response.",
   "why_it_matters": "A second accept's behaviour (idempotent 200 vs 409) is not specified anywhere, so the test can fail on that rather than on the total; it also never shows the rate is absent from the letter (covered only in test_export).",
   "fix": "Accept the rate once, assert the response total, then call build_export on the resulting state and assert the total line and that $185 is not in letter_text.",
   "acceptance_test": "A review module that adds 18500 on accepting a rate fails the test; one that 409s on re-accept does not."},
  {"severity": "nit", "title": "Out-of-scope file bundled into the T-039 commit; minor hygiene in specs",
   "evidence": "git show --stat a3068ed lists tests/unit/test_provider_backends.py (161 lines), not in T-039 AC. conftest sample_case fixture does not delete the case if its readiness assert fails; test_keyboard_mobile mobile test leaks the browser on assertion failure; test_side_by_side builds pytestmark with __import__('os'); test_api health docstring promises demo_mode true but asserts only backend.",
   "why_it_matters": "Traceability and leaked processes in CI; none block.",
   "fix": "Move test_provider_backends.py to its own card/commit; use try/finally or a fixture for the browser and for case cleanup.",
   "acceptance_test": "git show --stat for the follow-up commit lists only T-039 files."}],
 "whats_right": [
  "Golden byte-equality (R-EX-6), D-019 total line, case_07 $420 and the no-flags-parameter signature are encoded from checked-in goldens with no float money and no network.",
  "Unit suites go red only on NotImplementedError (39 of 39) and E2E skips all 57 with the :7860-down reason; AC4 file list of 13 files is exact.",
  "The 422/409 matrix, keep-my-wording resend, JUDGE_UNAVAILABLE save, date_invalid and the 7-of-9 reconciliation with record 5 dismissed and record 6 pending are asserted by state and output, not by implementation detail."],
 "questions_for_chris": []}
```
