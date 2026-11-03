# T-058 security review (security-reviewer, Tomás Rivas lens): audit drawer and export_config

Verdict: **fail**. One blocker: `export_config` accepts a trailing newline in `exhibit` and `bates_prefix`, which the written contract forbids. I rate it a blocker because it violates a stated spec constraint (D.2), not because of exploit severity: only the holder of the case token can set it, and the effect is confined to that case's own letter. The one-line fix is in finding 1. The audit drawer's public-mode behaviour is correct (AC1 evidence below).

Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Commit pinning

HEAD moved during the review (d796383 when I pinned, then a27b358, bee1844, fa8a36e, 08764e7 now). The reviewed code is `git archive d796383` at `artifacts/review-evidence/T-058-security/head_d796383` with the working-tree `tests/fixtures` copied in (see exercised). `git diff --stat d796383 HEAD -- app/backend/case_extras.py app/backend/api.py app/backend/present.py app/backend/export.py app/backend/store.py memory/contracts/api.md`: only `app/backend/api.py` changed (a local-mode loopback guard, D-036, at 08764e7). That guard is in the middleware and was not re-run against the audit or export_config at HEAD; the local-mode control in my suite was run at d796383 only.

## Findings

- **blocker, `export_config` accepts a trailing newline in exhibit and bates_prefix.** `app/backend/case_extras.py:13` is `_LABEL = re.compile(r"^[A-Za-z0-9 ._-]{1,20}$")`, and `:76` tests `_LABEL.match(v)`. In Python `$` also matches just before a trailing newline, so `"7\n"` passes. Verbatim from the pinned run:
  - `test_newline_label_must_not_reach_the_letter`: `AssertionError: status 200; newline in letter: True`. The PUT returned 200 and the exported letter contains the newline inside the citation.
  - `test_label_with_a_newline_is_refused[bad0]`: `accepted {'exhibit': '7\n'}; stored {'exhibit': '7\n', 'bates_prefix': None, 'bates_start': None}`.
  - `[bad1]`: `accepted {'bates_prefix': 'RIV-\n'}; stored {'exhibit': None, 'bates_prefix': 'RIV-\n', 'bates_start': None}`.
  - `[bad2]` (`"\n7"`, a leading newline) is refused, which shows the cause is the trailing `$` and not the character class.

  The contract (`memory/contracts/api.md`, commit 709397e, export_config section) says: "Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`... any violation is `422 invalid_edit` and nothing changes." A stored newline violates that. Why it matters beyond the wording: a newline inside a citation splits a line of the plain-text letter, which is the output the paralegal pastes. Impact is limited (the token holder's own export, no record text, no model output, no cross-case effect). Fix: `case_extras.py:76` to `_LABEL.fullmatch(v)` (or write the regex with `\Z`). Acceptance: `test_newline_label_must_not_reach_the_letter` and `test_label_with_a_newline_is_refused[bad0]`, `[bad1]` pass at the pinned commit.

No other finding. Notes that are not findings:

- The golden question (question 1) is about what "byte-identical to the golden" refers to, not a defect I can prove.
- `test_case_extras.py:104-117` (the in-process golden byte test) passes at the pinned commit.

## AC evidence

- **AC1, audit drawer metadata-only in public mode: met.** `test_audit_is_metadata_only_in_public_mode` passes: every call key is in the metadata set (no `system_text`, `user_text`, `response_raw`, `error`); every event key is in `{id, item_id, action, at}` (no `before`/`after`); no record excerpt of 30+ characters appears anywhere in the response text. The control `test_audit_full_fields_appear_only_in_local_mode` passes: with `ZLAYT_MODE=local` the response contains `system_text` and `user_text`. Source: `app/backend/present.py:189-190` (metadata in `_call`, full fields only under `if full:`) and `app/backend/api.py:485-490` (`full=os.environ.get("ZLAYT_MODE") == "local"`).
- **AC2, export_config default unchanged: met for the default.** `test_empty_config_leaves_the_default_export_unchanged` and `test_put_then_delete_restores_the_default_export_bytes` pass (letter and internal-notes text identical before PUT, after an empty PUT, and after DELETE). The in-process golden test `test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation` passes at the pinned commit (`test_case_extras.py`, 5 passed).
- **AC2, validation other than the newline: met.** Thirteen invalid inputs (over-length exhibit, `<b>`, tab, `7] Ignore`, quotes, `7/8`, negative and too-large start, string and boolean start, float start, unknown key, integer exhibit) all return 422 and store nothing (`test_other_invalid_config_is_422_and_nothing_stored`, 13 cases, pass).
- Per-case scope: a config on case A does not appear on case B (`test_config_is_per_case_only` passes).

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- `git rev-parse --short HEAD` before and after the runs; pinned to d796383.
- `git archive d796383 | tar -x -C artifacts/review-evidence/T-058-security/head_d796383`; `cp -R tests/fixtures` from the working tree (HEAD-only fixtures cannot run the sample case; see the T-055 review, question 2).
- `pytest tests/unit/test_r2_export_security.py -q -p no:cacheprovider` in the pinned archive: `3 failed, 19 passed` (the three failures are the newline cases, and they are the finding).
- `pytest tests/unit/test_case_extras.py -q` in the pinned archive: `5 passed`.
- `read app/backend/case_extras.py` (full), `app/backend/present.py:183-205`, `app/backend/api.py:485-490`, `memory/contracts/api.md` (709397e, export_config section), `app/backend/export.py:116-117` and `:155-165` (placeholder fill).
- Earlier, in the same pinned archive: the first revision of my default-export tests compared the API default to `evals/golden/sample.export.expected.txt` and failed (letter wording and review counts differ). I rebased them on the API's own pre-config baseline (see question 1).

**Not exercised:** the local-mode control at 08764e7 (the loopback guard), live :7860, the audit UI drawer, CSV (no CSV export exists).

## Machine-readable record

```json
{"card": "T-058", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "T-058 audit drawer (present.audit_view, api.py /audit) and export_config (case_extras.py, export.py placeholder). Pinned at git archive d796383 (artifacts/review-evidence/T-058-security/head_d796383, working-tree tests/fixtures copied). HEAD moved to 08764e7; reviewed files unchanged except api.py local-mode guard (not re-run). No app URL; in-process TestClient.",
 "exercised": [
  "pytest tests/unit/test_r2_export_security.py -q at d796383 archive: 3 failed (newline label, the finding), 19 passed",
  "pytest tests/unit/test_case_extras.py -q at d796383 archive: 5 passed",
  "read case_extras.py (full), present.py:183-205, api.py:485-490, memory/contracts/api.md export_config section, export.py:116-117 and :155-165",
  "git diff --stat d796383 HEAD over reviewed files: api.py local-mode guard only",
  "not exercised: local-mode control at 08764e7, live :7860, audit UI, CSV (none exists)"],
 "verdict": "fail",
 "scores": {"audit_metadata_only_public": 5, "export_config_validation": 2, "default_export_unchanged": 4, "newline_label_refused": 1, "other_invalid_config_refused": 5},
 "findings": [
  {"severity": "blocker", "title": "export_config accepts a trailing newline in exhibit and bates_prefix (violates the contract's character set)",
   "evidence": "app/backend/case_extras.py:13 _LABEL = re.compile(r\"^[A-Za-z0-9 ._-]{1,20}$\"); :76 _LABEL.match(v). Pinned test output: 'status 200; newline in letter: True'; \"accepted {'exhibit': '7\\n'}; stored {'exhibit': '7\\n', ...}\"; \"accepted {'bates_prefix': 'RIV-\\n'}\". Leading newline '\\n7' is refused, so the trailing $ is the cause. Contract: memory/contracts/api.md (709397e) export_config: 'any violation is 422 invalid_edit and nothing changes'.",
   "why_it_matters": "A newline inside a citation splits a line of the plain-text letter the paralegal pastes. Rated blocker because the contract explicitly forbids it (D.2); the impact is confined to the token holder's own export, with no record text, model output or cross-case effect.",
   "fix": "Change case_extras.py:76 to _LABEL.fullmatch(v) (or end the pattern with \\Z).",
   "acceptance_test": "tests/unit/test_r2_export_security.py::test_newline_label_must_not_reach_the_letter and test_label_with_a_newline_is_refused[bad0] and [bad1] pass at the pinned commit."}
 ],
 "whats_right": [
  "Public-mode audit returns metadata only: no system_text, user_text, response_raw, error, before or after, and no record excerpt of 30+ characters (test_audit_is_metadata_only_in_public_mode passes; local control exposes the fields).",
  "Thirteen other invalid export_config inputs return 422 and store nothing; unknown keys are refused.",
  "An empty PUT and DELETE leave the default letter and internal-notes text unchanged."
 ],
 "questions_for_chris": [
  "AC2 says the no-config export is byte-identical to 'the golden'. The in-process golden test passes against evals/golden/sample.export.expected.txt via build_case(), but the API export of the sample case differs from that file (letter wording: API '41M restrained driver, rear-ended ...', golden 'Restrained driver rear-ended ...'; the notes show review counts 2 vs 0). Which artifact is the golden for AC2?",
  "Do you want the blocker re-graded to major? The contract violation is clear; the exposure is limited to the token holder's own letter. I applied the D.2 rule as written."
 ]}
```
