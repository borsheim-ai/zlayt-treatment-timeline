# T-039 round 2 review - staff-engineer-reviewer (Marcus Lee lens)

Scope: HEAD b1803c0 (fix commit 11ab4fb is an ancestor). Working tree had uncommitted edits by other workers (M app/backend/pipeline.py, review.py, app/llm/audited.py, app/llm/record.py; untracked api.py, present.py, store.py, main.py). Test results below are for that tree. I wrote nothing under app/, tests/ or evals/; mutations ran on copies.

Model note: the dossier expects claude-sonnet-5-5, but this review ran as claude-haiku-5-5, which is the model field below. The round-1 record listed claude-sonnet-5-5.

## Round-1 majors

1. **Conftest contract incomplete: CLOSED.** The docstring now names data-review, data-state, role=alert, the input-name rule, tabindex, and the a/d/j/Enter keys (grep below). My script finds every test id, data-* attribute, role and key used by tests/e2e specs declared in the docstring (used but undeclared: []). test_e2e_contract.py: 3 passed.
2. **record_nos vs record_ids, case_01 IndexError: CLOSED.** `grep -c record_nos tests/unit/test_review_rules.py` gives 0. ent() keys on record_ids. seeded() passes `case` to which_record, and which_record maps all 8 case_01 records. The real pipeline (T-037, d67a82d) now runs under these tests, and test_confirm_date_non_candidate_is_422_date_invalid passes. The first run this session, before the pipeline landed, was 20 failed / 3 passed, and all 20 errors were `E   NotImplementedError` (none IndexError or KeyError).
3. **Letter isolation lacked positive assertions: CLOSED.** Accepts must return 200 (test_letter_isolation.py:11), the note edit must return 200 (:18), and the letter must start with TREATMENT CHRONOLOGY with 9 dated headings and an accepted quote (:20-21). The stub run (section Exercised) shows the spec now fails on a 409-everywhere server and on an empty letter.

## New finding

- **MAJOR: the judge exception path is unguarded.** app/backend/review.py:107-109 catches `Exception` and sets "unavailable". The only test of judge failure (test_review_rules.py:108-112) raises LLMFailed, which judges.py:33 converts before review.py sees it. So the review.py branch is never exercised. Mutating that branch to "supported" leaves the suite green (`[M-C ...] exit=0 :: 23 passed`, before the probe was added). A TimeoutError probe, which is the case dossier section 8 names, catches the same mutation (`[M-C ...] exit=1 :: 1 failed, 23 passed`). The current code is correct, so this is a test gap, not a live silent fallback. Required before the gate.

## Minors and nits (not blockers)

- F2 minor: the textContent injection assertion (test_source_record.py:22-23) runs only `if` the optional hook exists. A frontend without the hook passes.
- F3 minor, carried from r1: test_review_rules.py:127-130 accepts $185 twice and asserts only the total.
- F4 minor: test_e2e_contract.py:33-37 checks fixed substrings for roles, keys and tabindex. It does not parse `keyboard.press()` or `get_by_role()`, so a new undeclared key stays green.
- F5 minor: _fakes.py:37, `which_record(user, case="sample")` returns [] silently for other cases (repro in the checks output).
- F6 minor: test_edit.py:23-24 asserts count()==0 for the date/provider inputs without first asserting the edit form is open.
- F7 minor: tests/e2e/conftest.py:21-27, `_up()` catches all exceptions. An HTTP 500 on /api/health reads as "not running", so every spec skips and CI stays green.
- F8 nit, carried: tests/unit/test_provider_backends.py was bundled into commit 11ab4fb (34 insertions, 5 deletions), which is outside the T-039 AC.
- F9 nit, carried: tests/e2e/conftest.py:64-66 asserts before `yield`, so a failed readiness check leaves the case undeleted.

Carried r1 minors now closed: negative-only charge and rejected-tray checks now have positive existence checks (test_charges.py:26, test_review_matrix.py:25); `Items not reviewed: 1.` is asserted (test_export.py:150); the $1,2OO test asserts the total line (test_review_rules.py:122); the edit notes test asserts both texts (test_edit.py:34). Not re-checked this round: the r1 nits on test_keyboard_mobile browser leak, test_side_by_side `__import__`, and test_api docstring.

## Exercised

- `.venv/bin/python -m pytest tests/unit/test_review_rules.py -q 2>&1 | tail -3`: first run gave 20 failed / 3 passed, all NotImplementedError. Later run, after d67a82d: `23 passed in 1.13s` (repeated, `23 passed in 1.23s` on the last run).
- `.venv/bin/python -m pytest tests/unit/test_export.py -q`: 19 passed. `tests/unit/test_e2e_contract.py`: 3 passed. `tests/e2e --collect-only`: 57 collected. `tests/e2e -q -rs` with no server: 57 skipped with the :7860 reason.
- `grep -n "data-review\|data-state\|role=alert\|input named\|tabindex\|a = accept" tests/e2e/conftest.py` returned:
  - 9: `Attributes (on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected`
  - 11: `Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).`
  - 12: `Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).`
- `grep -n "record_ids\|record_nos" tests/unit/test_review_rules.py` returned line 25 `... if f"r{n}" in e["record_ids"] ...`, plus lines 24, 138 and 139. The count of record_nos is 0.
- `.venv/bin/python artifacts/review-evidence/T-039-r2-checks.py` (output in artifacts/review-evidence/T-039-r2-checks.txt): hook cross-check (used but undeclared: []; data-* missing: []); golden letter block versus the BAD list (0 hits each), 9 headings, the accepted quote and the $8,390 total line present; which_record per case (case_01 8/8). The default-arg repro is `which_record(raw('case_01_date_formats')) with default case = []`.
- `.venv/bin/python artifacts/review-evidence/T-039-r2-letter-stub.py` (output in artifacts/review-evidence/T-039-r2-letter-stub.txt): ran tests/e2e/test_letter_isolation.py against an in-process stub of the API on a free port. Results: control (golden letter served) had 2 passed; `test_letter_is_subset_of_accepted` failed with `9 == 2` only because the stub does not filter by accepted items (stub artifact, not a spec defect). r409 had 3 failed (`AssertionError: ('e1', 409)` at :11). empty had 3 failed (:20, :28, :35).
- `.venv/bin/python artifacts/review-evidence/T-039-r2-mutation.py` (output in artifacts/review-evidence/T-039-r2-mutation.txt), on copies only:
  - CONTROL with probe: 24 passed.
  - M-A judge-unavailable mapped to supported (judges.py): 2 failed, including test_judge_unavailable_saves_with_reason.
  - M-B immutable-field guard removed (review.py): 4 failed (test_entry_immutable_fields_are_422 edits0-3).
  - M-C review.py except-branch to supported: 1 failed (the timeout probe). The unit suite alone stays green.
- Read in full: tests/unit/test_review_rules.py, tests/e2e/conftest.py, test_letter_isolation.py, test_edit.py, test_e2e_contract.py, tests/unit/_fakes.py, _golden.py; grep of the other e2e specs for hooks; git show --stat 11ab4fb.
- Not run: any E2E spec against a live app (no server on :7860), CLI determinism (pipeline CLI not in scope of this card).

```json
{"card": "T-039", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2; fix commit 11ab4fb (ancestor of HEAD b1803c0); tests/unit/test_review_rules.py, tests/unit/test_e2e_contract.py, tests/unit/_fakes.py, tests/e2e/conftest.py, test_letter_isolation.py, test_edit.py, test_source_record.py; working tree has uncommitted app/backend/pipeline.py, review.py and untracked api.py; app not running at :7860; stub API for E2E in-process",
 "exercised": [
  "pytest tests/unit/test_review_rules.py -q: 20 failed/3 passed (NotImplementedError only) before pipeline landed; 23 passed after d67a82d",
  "pytest tests/unit/test_export.py -q: 19 passed; tests/unit/test_e2e_contract.py: 3 passed; tests/e2e --collect-only: 57; tests/e2e -q -rs (no server): 57 skipped",
  "grep conftest.py for data-review/data-state/role=alert/input named/tabindex/a = accept: lines 9, 11, 12",
  "grep -c record_nos tests/unit/test_review_rules.py: 0; record_ids at lines 24-25, 138-139",
  "artifacts/review-evidence/T-039-r2-checks.py: hook cross-check (undeclared: []), golden letter vs BAD list (0 hits), 9 headings, which_record per case, default-arg footgun repro",
  "artifacts/review-evidence/T-039-r2-letter-stub.py: letter-isolation spec vs stub in control/r409/empty modes (r409: 3 failed; empty: 3 failed)",
  "artifacts/review-evidence/T-039-r2-mutation.py on copies: M-A judges.py to_ladder unavailable->supported (2 failed); M-B immutable guard removed (4 failed); M-C review.py except-branch->supported (suite 23 passed without probe; 1 failed with timeout probe)",
  "read in full: test_review_rules.py, e2e/conftest.py, test_letter_isolation.py, test_edit.py, test_e2e_contract.py, _fakes.py, _golden.py; grep of other e2e specs; git show --stat 11ab4fb"],
 "verdict": "changes",
 "scores": {"ac_encoding": 4, "red_for_the_right_reason": 4, "test_strength": 3, "e2e_contract_completeness": 4, "determinism_and_isolation": 4},
 "findings": [
  {"severity": "major", "title": "Judge exception path (review.py except-branch) has no test; silent fallback to supported passes the suite",
   "evidence": "app/backend/review.py:107-109 `except Exception:` then `verdict, call_id = \"unavailable\", None`; test_review_rules.py:108-112 raises AU.LLMFailed, which judges.py:33 converts before review.py sees it, so the branch is not exercised. artifacts/review-evidence/T-039-r2-mutation.txt: mutated branch to \"supported\" -> `[M-C review-except-branch-as-supported] exit=0 :: 23 passed` (before probe); with TimeoutError probe -> `exit=1 :: 1 failed, 23 passed` (test_r2_judge_timeout_saves_with_reason). Control with probe: `24 passed`.",
   "why_it_matters": "T-039 AC3 requires judge unavailable -> JUDGE_UNAVAILABLE and dossier section 8 requires a test that a timeout yields needs_review. A regression to 'supported' on this path would pass CI. The broad except also reports any programming error in the judge call as 'judge unavailable', which is visible but misattributed. Current code is correct; this is a guard gap.",
   "fix": "Add the probe to tests/unit/test_review_rules.py: FakeCall({\"j1\": TimeoutError(\"slow\")}) on an entry edit must return review_status edited, state needs_review, reasons containing JUDGE_UNAVAILABLE. In the backend card, narrow review.py:107 to the provider's timeout/failure types instead of Exception.",
   "acceptance_test": "pytest tests/unit/test_review_rules.py -q passes on HEAD and fails when review.py:109 is mutated to \"supported\" (artifacts/review-evidence/T-039-r2-mutation.py, M-C)."},
  {"severity": "minor", "title": "textContent injection proof is conditional on an optional hook",
   "evidence": "tests/e2e/test_source_record.py:22-23: `if page.evaluate(\"typeof window.__debugInjectRecordHtml === 'function'\"):` then the img/onerror assertion; tests/e2e/conftest.py docstring line 14 says \"Optional test hook\".",
   "why_it_matters": "A frontend that omits the hook passes; the invariant that untrusted text uses textContent then has no required proof (sample records contain no markup, so the static assertions cannot fail on innerHTML). Carried from r1 and only partly fixed.",
   "fix": "Make the hook required in the conftest contract and drop the `if`; assert the literal '<img src=x' appears as text and no img element exists.",
   "acceptance_test": "Remove the hook from a copy of the frontend: test_record_text_is_inserted_as_text must fail (needs a live server, not run this round)."},
  {"severity": "minor", "title": "Charge-rate double accept: test does not check the letter or a single-accept state (carried from r1, unfixed)",
   "evidence": "tests/unit/test_review_rules.py:127-130: loop accepts \"$6,240\",\"$2,150\",\"$185\" then accepts \"$185\" a second time and asserts only totals.accepted.cents == 839000.",
   "why_it_matters": "Second-accept behaviour is unspecified, so the test can fail for the wrong reason; the letter exclusion of the rate is not asserted here.",
   "fix": "Accept the rate once, assert the response total, then build_export on the state and assert the total line and that \"$185\" is not in letter_text.",
   "acceptance_test": "A review module that adds 18500 when a rate is accepted fails the test."},
  {"severity": "minor", "title": "Contract test enforces only fixed substrings for roles, keys and tabindex",
   "evidence": "tests/unit/test_e2e_contract.py:33-37 asserts `needle in c` for six literal strings. Specs use keyboard.press(\"a\") and (\"j\") (test_keyboard_mobile.py:9, test_side_by_side.py:18), get_by_role(\"alert\") (test_input.py:20), get_by_role(\"button\", ...) (test_review_matrix.py:15), which the test does not parse.",
   "why_it_matters": "The docstring is complete today (checks output: used but undeclared = []), but a spec that adds press(\"x\") or a new role stays green. The r1 acceptance test asked for extraction of every hook, not needle presence.",
   "fix": "Extract keyboard.press() keys and get_by_role() names from tests/e2e/test_*.py and assert each is in the contract docstring.",
   "acceptance_test": "Add page.keyboard.press(\"x\") to a copy of a spec: the contract test must fail (checked by reading; not run)."},
  {"severity": "minor", "title": "which_record() silently returns [] for non-sample cases with its default argument",
   "evidence": "tests/unit/_fakes.py:37 `def which_record(user, case=\"sample\"):`. Repro: `.venv/bin/python artifacts/review-evidence/T-039-r2-checks.py` prints `default-arg footgun: which_record(raw('case_01_date_formats')) with default case = []`.",
   "why_it_matters": "seeded() passes case today (test_review_rules.py:16-17), so there is no live failure. Any future caller that omits case gets [], and extract then fails with IndexError or cites the wrong record, which is the exact r1 failure mode.",
   "fix": "Make case a required argument, or raise ValueError when no record matches.",
   "acceptance_test": "which_record(G.raw('case_01_date_formats')) raises instead of returning []."},
  {"severity": "minor", "title": "Negative-only assertion for date/provider inputs without proving the edit form is open",
   "evidence": "tests/e2e/test_edit.py:23-24: `e.get_by_test_id(\"btn-edit\").click()` then `assert e.locator(\"input[name=date], input[name=provider]\").count() == 0`; no positive check on edit-summary first.",
   "why_it_matters": "If the edit form never opens, count()==0 holds and the test is green. Same class as the r1 negative-only minor.",
   "fix": "Assert e.get_by_test_id(\"edit-summary\").count() == 1 (or is_visible) before the negative.",
   "acceptance_test": "A build with no edit form fails test_date_and_provider_not_editable (needs a live server; not run)."},
  {"severity": "minor", "title": "_up() treats any exception as 'server not running', so an unhealthy server skips every E2E spec green",
   "evidence": "tests/e2e/conftest.py:21-27: `def _up():` ... `except Exception: return False`; pytest_collection_modifyitems then skips with reason \"app server not running at ...\". urllib raises HTTPError (a URLError, so an Exception) for a 5xx on /api/health (read, not run).",
   "why_it_matters": "A server that is up but broken yields 57 skips with the wrong reason, and CI reports success. Failures must be visible, and a skip is not a failure.",
   "fix": "Catch only connection errors (URLError whose reason is refusal or timeout) as not-running; any HTTP status other than 200 from /api/health should fail collection.",
   "acceptance_test": "Stub /api/health returning 500: the e2e run errors instead of skipping (stub method in artifacts/review-evidence/T-039-r2-letter-stub.py can serve it)."},
  {"severity": "nit", "title": "Out-of-scope file bundled in the T-039 fix commit (carried from r1)",
   "evidence": "`git show --stat 11ab4fb`: tests/unit/test_provider_backends.py, 34 insertions, 5 deletions; not in any T-039 AC.",
   "why_it_matters": "Traceability only; it is not a blocker.",
   "fix": "Move it to its own card or commit.",
   "acceptance_test": "git show --stat for the T-039 commit lists only T-039 files."},
  {"severity": "nit", "title": "sample_case fixture does not delete the case when readiness fails (carried from r1)",
   "evidence": "tests/e2e/conftest.py:64-66: `assert s[\"status\"] == \"ready\"`, then `yield tok`, then `api(\"DELETE\", ...)` with no try/finally.",
   "why_it_matters": "Leaked cases accumulate on a failing run.",
   "fix": "Wrap the yield in try/finally so the DELETE always runs.",
   "acceptance_test": "A forced readiness failure leaves no case behind (needs a live server)."}],
 "whats_right": [
  "Letter isolation now asserts positives and fails on both a 409-everywhere server and an empty letter (artifacts/review-evidence/T-039-r2-letter-stub.txt).",
  "The conftest docstring now declares every test id, data attribute, role and key that the specs use (artifacts/review-evidence/T-039-r2-checks.txt, section 2).",
  "The M-A and M-B mutations of the review rules are caught by named tests, and the case_01 path runs through the real pipeline and passes."],
 "questions_for_chris": ["Is the window.__debugInjectRecordHtml hook meant to stay optional? If it is, the textContent invariant has no required proof (F2)."]}
```
