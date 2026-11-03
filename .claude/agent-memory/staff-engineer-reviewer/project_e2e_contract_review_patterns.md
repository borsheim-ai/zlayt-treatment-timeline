---
name: e2e-contract-review-patterns
description: T-039 round 1-2 (tests-first unit + E2E specs) patterns - contract docstring vs spec hooks, vacuous negatives, optional hooks, judge-path mutation, stub-server E2E method
metadata:
  type: project
---

Recurring patterns from the T-039 review (tests/unit/test_review_rules.py, tests/e2e/*, conftest contract docstring; reviews/T-039-staff-engineer.md and -r2.md).

- **Check the path a test actually reaches before calling a mutation "uncaught".** The first judge mutation (review.py except-branch) passed the suite, but the existing test never reaches that branch: judges.py:33 converts LLMFailed to "unavailable" first. A mutation on the reached path (judges.py to_ladder) was caught. Map which layer raises before mutating.
- **Stub-server E2E run without the app.** Serve /api/health, /api/cases, /run, /status, GET case, /review, /export in-process on a free port and point E2E_BASE_URL at it. Modes: control (golden letter), review-409, empty letter. Script: artifacts/review-evidence/T-039-r2-letter-stub.py. Useful for any E2E spec with a fixture-only dependency.
- **A contract docstring can be complete while enforcement stays needle-presence.** tests/unit/test_e2e_contract.py checks fixed substrings for roles/keys/tabindex; it does not parse keyboard.press() or get_by_role(). Re-check any "declared" claim by extracting hooks from the specs, not by grep of needles.
- **Optional hooks make proofs conditional.** `if page.evaluate("typeof window.__debugInjectRecordHtml === 'function'")` (test_source_record.py) means the textContent proof runs only when the frontend opts in. Require the hook in the contract.
- **Broad except in a health probe hides broken servers as skips.** tests/e2e/conftest.py `_up()` catches Exception; an HTTP 500 on /api/health becomes 57 green skips.
- **Red evidence goes stale.** T-039 r1 saw 39 failed / NotImplementedError; r2 saw 23 passed after the T-037 pipeline commit (d67a82d) landed. Re-run before quoting a red state; quote the run with its date and HEAD.
- **Default-argument footgun in fakes.** which_record(user, case="sample") returns [] silently for other cases; the r1 IndexError came from exactly this.

**Why:** these produced the T-039 r1 majors (contract incomplete, record_nos/IndexError, vacuous letter) and the r2 major (judge except-branch unguarded).
**How to apply:** on any E2E or tests-first card, extract hooks from specs, run a stub-server mode with a 409 and an empty output, mutate the path the test reaches, and grep for optional-hook `if` guards.

Environment notes (seen this card): board-guard denies shell redirects outside reviews/ and artifacts/review-evidence, including `> $(dirname $0)/...`. git-guard "could not parse command safely" on long for-loops with quotes and em-dashes; put the check in a file under artifacts/review-evidence and run it. Use `-p no:cacheprovider` for pytest runs from the reviewer. `timeout` is not on this macOS shell; use the tool timeout parameter.

Related: [[project_db_review_patterns]], [[project_design_review_patterns]], [[project_harness_review_patterns]].
