# T-058 round 2 security review: export_config trailing newline (commit 991dac4)

Verdict: **pass**. The round-1 blocker is closed. No open blocker or major. One nit.

Lens: this review applies `personas/security.md` (security-reviewer) at the orchestrator's request, as the brief asks. The reviewer identity in this file is security-reviewer. Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Pinning

- HEAD at review start: `373f8b1`. Commit under review: `991dac4`, an ancestor of HEAD.
- `git diff --stat 991dac4 HEAD -- app/backend/case_extras.py app/backend/amounts.py app/backend/dates.py app/llm/_types.py app/backend/api.py app/backend/grounding.py app/backend/present.py app/backend/export.py memory/contracts/api.md` shows only `case_extras.py` (1 line removed: the unused `before` variable) and `memory/contracts/api.md` (documentation). No validator file changed after 991dac4.
- Reviewed code: `git archive 991dac4` at `artifacts/review-evidence/T-058-security-r2/head_991dac4`. The import check `.venv/bin/python -c "import app"` resolves to that archive. Working-tree fixtures were not copied in; the archive ran with its tracked fixtures.

## Round-1 blocker: closed

Round 1 found `_LABEL = re.compile(r"^[A-Za-z0-9 ._-]{1,20}$")` with `.match`, so `"7\n"` passed (`app/backend/case_extras.py:13` and `:76` at d796383). At 991dac4:

- `app/backend/case_extras.py:13` is `_LABEL = re.compile(r"[A-Za-z0-9 ._-]{1,20}")`, and `:75` is `_LABEL.fullmatch(v)`.
- Probe through the real route (`PUT /api/cases/{token}/export_config`, in-process TestClient, fixture backend, no network). Output: `artifacts/review-evidence/T-058-security-r2/probe_put_newline.out.txt`.

| PUT body | Status | Stored config changed |
|---|---|---|
| `{"exhibit": "7"}` (control) | 200 | yes (expected) |
| `{"exhibit": "7\n"}` | 422 `invalid_edit` | no |
| `{"bates_prefix": "RIV-\n"}` | 422 `invalid_edit` | no |
| `{"exhibit": "\n7"}` | 422 `invalid_edit` | no |
| `{"exhibit": "7\r\n"}` | 422 `invalid_edit` | no |
| `{"exhibit": "7\n\n"}` | 422 `invalid_edit` | no |
| `{"exhibit": "7\u2028"}` | 422 `invalid_edit` | no |
| `{"exhibit": "ab\n", "bates_prefix": "RIV-"}` | 422 `invalid_edit` | no |

After the valid config, the export (9 accepted entries) carries `[Ex. 7 / Bates RIV-0001]`, `[Ex. 7 / Bates RIV-0002]`, `[Ex. 7 / Bates RIV-0003]`, and no citation contains a newline. Stored values with a newline after any 200: 0.

Test evidence at 991dac4: `tests/unit/test_case_extras.py` 11 passed (the five newline cases and `test_no_backend_validator_accepts_a_trailing_newline` pass). Full `tests/unit` in the archive: 902 passed.

Mutation check (scratch copies, not committed; output `artifacts/review-evidence/T-058-security-r2/mutants.out.txt`):

- M1, round-1 regex restored (`^...$` with `.match`): 2 failed (`[bad0]`, `[bad1]`), which are exactly the two round-1 cases.
- M2, `dates._ISO` back to `$`: 1 failed (`test_no_backend_validator_accepts_a_trailing_newline`).
- M3, `amounts._VALID` back to `$`: 1 failed (same test).
- M4, `_types._FENCE` back to `$`: 1 failed (same test).

## Grep for remaining `$`-anchored validators

Commands (run in the pinned archive):

```
grep -rn --include=*.py -E '\$([|)"'"'"'/\]}\\]|$)' app/backend app/llm
grep -rn --include=*.py '\\Z' app/backend app/llm
```

Every `$` anchor in `app/backend` and `app/llm` is one of these:

- Value validators: none left. `dates.py:13-16`, `amounts.py:11`, `llm/_types.py:35` and `case_extras.py:13` all end in `\Z` or use `fullmatch`.
- Line-oriented parsers with `re.MULTILINE` (`ingest.py:15-19`, `promptlib.py:9`): `$` means end of line by design. Not value validators.
- Parser and context regexes applied to slices or labels (`record.py:44`, `amounts.py:19` used by `_CHARGE_END.search(label)`, `sentences.py:14`, `export.py:90`, `lexicon_scan.py:9`): the trailing `\s*` absorbs any newline, or the `$` is a lookahead. Not validator gaps.
- `review.py:14` `_NUMERIC_TOKEN = ... ^(?:january|...|december)$` (used at `review.py:67` with `.search`): the one remaining validator-style `$`. Its only effect is to match more (over-refuse), never to accept what should be refused. Tokens come from `grounding.new_tokens` (`grounding.py:146-160`), which returns only regex captures (digit runs, `left|right|no|not|without`, month names), so no token can contain a newline. See finding 1.

## Findings

- **nit, `app/backend/review.py:14` still has a `$` anchor.** Evidence: the grep above, line 14. `_NUMERIC_TOKEN.search(t)` runs on tokens that cannot contain a newline (`grounding.py:146-160`). Why it matters: no current input reaches the bug, but a future token source with a trailing newline would be classified as numeric and refused, and the pattern is inconsistent with the rest of the file. Fix: change to `...|december)\Z` (or `fullmatch`). Acceptance: the grep above returns no `$` validators in `app/backend` and `app/llm`.

## AC status (r1 evidence, not re-run this round)

The audit drawer (r1 AC1) and the default-export golden were not re-exercised in this round, which covers the r1 blocker only. The default-export golden test passes in the archive (`tests/unit/test_case_extras.py`, part of the 11 passed).

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- Read `personas/security.md` in full and `reviews/T-058-security.md` in full (round-1 finding and acceptance tests).
- `.venv/bin/python tools/board.py show T-058`: `status: "in_review"`, `rounds: 1`, `commits: ["a79358c", "dbb2c66", "991dac4"]`.
- `git log --oneline -n 12`; `git show --stat 991dac4` (8 files, includes `app/backend/case_extras.py` and `tests/unit/test_case_extras.py`); `git show 991dac4 -- app/backend/case_extras.py` (regex and `.match` to `.fullmatch`).
- `git diff 991dac4 HEAD -- app/backend/case_extras.py memory/contracts/api.md`: one `before` line removed; one contract line changed.
- `git archive 991dac4 | tar -x -C artifacts/review-evidence/T-058-security-r2/head_991dac4`.
- `.venv/bin/python -m pytest tests/unit/test_case_extras.py -q -p no:cacheprovider` in the archive: 11 passed.
- `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` in the archive: 902 passed (`full_unit_991dac4.out.txt`).
- `.venv/bin/python probe_put_newline.py` in the archive: 8 PUT bodies, output in `probe_put_newline.out.txt`.
- Mutants M1 to M4 on scratch copies (`mutate_t058.py`, `mutants.out.txt`).
- The two greps above, plus reading `review.py:14`, `:67`, `grounding.py:146-160`, `amounts.py:19`, `record.py:44`.

Not exercised: live :7860 (no app URL in scope for this round); the audit drawer UI; the local-mode loopback guard (`api.py` is unchanged from 991dac4 to HEAD).

## Machine-readable record

```json
{"card": "T-058", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round 2 of T-058 at commit 991dac4 (export_config label: case_extras.py fullmatch; \\Z in amounts.py, dates.py, llm/_types.py). Pinned at git archive 991dac4 (artifacts/review-evidence/T-058-security-r2/head_991dac4), tracked fixtures only. HEAD 373f8b1: validator files unchanged since 991dac4 except one unused-variable removal. In-process TestClient, fixture backend; no app URL.",
 "exercised": [
  "read personas/security.md and reviews/T-058-security.md in full",
  "board.py show T-058 (in_review, rounds 1, commits a79358c dbb2c66 991dac4)",
  "git show --stat 991dac4; git show 991dac4 -- app/backend/case_extras.py; git diff 991dac4 HEAD over validator files and memory/contracts/api.md",
  "git archive 991dac4 extracted to artifacts/review-evidence/T-058-security-r2/head_991dac4; import app resolves to the archive",
  "pytest tests/unit/test_case_extras.py -q in the archive: 11 passed",
  "pytest tests/unit -q in the archive: 902 passed",
  "probe_put_newline.py through the real export_config route: PUT 7-newline, RIV-newline, leading newline, CRLF, double newline, U+2028, mixed body all 422 invalid_edit, stored config unchanged; control 200; export citations clean (probe_put_newline.out.txt)",
  "mutants M1 (round-1 regex), M2 (dates _ISO $), M3 (amounts _VALID $), M4 (_types _FENCE $) on scratch copies: M1 2 failed, M2-M4 1 failed each (mutants.out.txt)",
  "grep -rn for $-anchored patterns and \\Z in app/backend and app/llm; read review.py:14, :67, grounding.py:146-160, amounts.py:19, record.py:44",
  "not exercised: live :7860, audit drawer UI, local-mode loopback guard (unchanged since 991dac4)"],
 "verdict": "pass",
 "scores": {"export_config_newline_refused": 5, "other_validators_end_anchored": 5, "export_citation_clean": 5, "round1_regression_tests_fail_on_revert": 5},
 "findings": [
  {"severity": "nit", "title": "review.py:14 still has a $ anchor in _NUMERIC_TOKEN (not reachable with a newline today)",
   "evidence": "app/backend/review.py:14 `_NUMERIC_TOKEN = ... r\"\\d|^(?:january|...|december)$\"`, used at review.py:67 with .search. grounding.new_tokens (grounding.py:146-160) yields only regex captures (digit runs, left/right/no/not/without, month names): no token can contain a newline. Command: grep -rn --include=*.py -E '\\$([|)\"'\"'\"'/\\]}\\\\]|$)' app/backend app/llm",
   "why_it_matters": "No accept path is affected: the $ can only over-match. Still inconsistent with the rest of the validators, and a future token source could carry a newline and be refused as numeric.",
   "fix": "Change review.py:14 to end the alternative with \\Z (or use fullmatch).",
   "acceptance_test": "The grep above returns no $-anchored validator in app/backend or app/llm; tests/unit/test_case_extras.py::test_no_backend_validator_accepts_a_trailing_newline still passes."}
 ],
 "whats_right": [
  "PUT export_config with 7-newline, RIV-newline, leading newline, CRLF, double newline, U+2028 and a mixed body all return 422 invalid_edit, and the stored config does not change (probe_put_newline.out.txt).",
  "The round-1 regex restored in a scratch copy fails exactly the two round-1 cases; each reverted $ validator (dates, amounts, fence) fails test_no_backend_validator_accepts_a_trailing_newline.",
  "A valid config fills the citation with no newline: [Ex. 7 / Bates RIV-0001] to RIV-0003 on the sample export with 9 accepted entries."
 ],
 "questions_for_chris": []}
```
