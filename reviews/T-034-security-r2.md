# T-034 security review, round 2 (security-reviewer, claude-haiku-5-5)

Verdict: **pass**. No blockers, no majors. The round-1 major (red tests against FixtureMissing, the sleep seam and the hash-bearing miss log) is resolved and the three named files are green. All five round-1 minors are resolved or reduced to residual minors and nits; three residuals are recorded below.

Tree at review time: HEAD `250e7b6` (other cards committed during the review; the T-034 LLM code under `app/llm/` and the three test files are unchanged since `b1803c0`, the round-1 fix commit. Only four judge prompt `.md` files changed in the same range, which are outside this card and were not reviewed for content).

Pytest, quoted verbatim:
```
$ .venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3
........................................                                 [100%]
40 passed in 0.97s
```
Round 1 was `12 failed, 25 passed`. An earlier run in this round also gave `40 passed in 0.95s`.

## Major (round 1): resolved
- `FixtureMissing` exists and is exported. `app/llm/provider.py:15` re-exports it, `app/llm/_types.py:11` defines it, and `_types.py:19` keeps `FixtureMiss` as an alias.
- The `sleep` seam exists. `app/llm/audited.py:53` takes `sleep=None`, and `audited.py:86-87` calls `sleep(RETRY_DELAYS_S[attempt - 1])` only for non-final attempts. `tests/unit/test_provider_backends.py:184-190` checks that the naps are capped at 2 s and that `sleep` is injectable.
- The miss is logged with the prompt hash. `audited.py:83`: `log.warning("llm call failed call_id=%s step=%s attempt=%d%s", ..., f" prompt_hash={h}" if fixture_miss else "")`. A fixture miss is one attempt and one row, and it raises `LLMFailedFixtureMiss` (`audited.py:85`).
- The tests were tightened, not loosened. The `FixtureMiss` expectations became `FixtureMissing` plus `LLM_FAILED_AFTER_RETRIES` (`git diff 958c353 HEAD -- tests/unit/test_audited.py`). The test edits were committed in `f3da5b9` (T-048).

## Minor findings (round 1): status
1. Recorder guard. Largely resolved. `record_context` now requires a whole-file golden match. Residual is nit 3 below.
2. Schema validator. Resolved. Probes show `maxLength`, `maximum` and `anyOf` are enforced, and unknown keywords and types fail closed (see Exercised).
3. claude-cli child env. The env part is resolved. The gating and argv-prompt parts of the same round-1 finding remain open; see minor 2 below.
4. Audit error column. Resolved. Only codes are stored.

## Findings

**minor 1. The miss-log hash line has no test.** `audited.py:83` logs `prompt_hash=<sha256>` on a miss, and the probe shows it. But `grep -rn "prompt_hash=" tests/` returns nothing, and no test named `test_fixture_miss_logs_hash_not_text` exists (the round-1 acceptance name). `tests/unit/test_provider.py:41` `test_fixture_miss_reports_hash_not_text` checks the exception message and that the prompt text is absent from caplog. It does not check that the hash is in the log. A future edit could drop the suffix and every test would stay green.

**minor 2. claude-cli gating and argv prompt remain open.** `app/llm/provider.py:72-76` selects `claude-cli` on `LLM_BACKEND` alone, with no dev flag. `grep -rln ZLAYT_DEV` (code, md, Makefile) matches only `board/cards/T-034.md` and `reviews/T-034-security.md`, so no gate exists. `app/llm/backends/claude_cli.py:37-40` puts the user prompt in argv after `--` (the comment marks it as a qa-pinned contract), so the record text is visible in `ps` on a shared box. `ls Dockerfile*` returns "No such file or directory", so this is not exploitable in a public build yet. It is still checklist 16 and must close before the Docker card.

**nit 3. Recorder guard residual.** `app/llm/provider.py:36` sets `MIN_FRAGMENT = 20` and `provider.py:42-46` still accepts any 20-character substring of a golden file when `whole_file` is false. `record_context` (`provider.py:52`) is still public. Record writes are gated by the whole-file check, so this is not exploitable: the probe shows `record_context('a')` raises `ValueError`, and `record_context(<full golden text>)` is accepted. `app/llm/record.py:20` uses the fragment default as a pre-check only.

## Checks against the brief
- Retries are capped at 3 and the timeout is 120 s (`audited.py:14`, `claude_cli.py:12`). Pass.
- `ANTHROPIC_*` and cloud credentials are absent from the CLI child env. Pass.
- Audit error column holds codes only (`audited.py:36-42`, `:67-68`). Pass.
- The LLM prompt-injection record cannot change the schema (`_types.py:54-55`, `:76-82`). Pass.

Outside my lens: whether the `llm_calls` retention and prompt storage meet the rules (privacy-compliance-reviewer).

```json
{"card": "T-034", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 250e7b6 working tree; LLM code app/llm/{provider,audited,_types,record}.py and backends/{claude_cli,anthropic_api,fixture}.py unchanged since b1803c0; tests/unit/test_provider.py, test_audited.py, test_provider_backends.py at HEAD; no app URL (library card)",
 "exercised": [
  "git rev-parse --short HEAD -> 250e7b6; git log -1 -> 'fix(backend): generator tests, D-028 judge reason_code, label in nonce block (T-035 r2)'",
  "git merge-base --is-ancestor b1803c0 HEAD -> ancestor; git diff --stat b1803c0 HEAD -- app/llm tests/unit/test_provider*.py tests/unit/test_audited.py -> only 4 judge prompt .md files differ",
  ".venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3 -> '40 passed in 0.97s' (run twice; 40 passed in 0.95s on the earlier run)",
  "git status --short on the three test files and app/llm -> empty (clean)",
  "git diff 958c353 HEAD -- tests/unit/test_audited.py tests/unit/test_provider.py (read in full) to confirm the tightening, not loosening",
  "grep -n on app/llm for FixtureMissing, FixtureMiss, sleep, prompt_hash, maxLength, maximum, anyOf, _KEYWORDS, child_env, ENV_ALLOW, _CODE, log.warning; grep -rn in tests/ for sleep, caplog, prompt_hash=, test_fixture_miss_logs_hash_not_text",
  "grep -rln ZLAYT_DEV across repo (code, md, Makefile); ls Dockerfile* -> no such file",
  "read provider.py, audited.py, _types.py (validator 50-150), claude_cli.py (1-75), record.py (15-36) in full",
  "probe via .venv/bin/python heredoc (no file written): assert_recordable('a'|'the'|'2019') -> ValueError; record_context('a') -> ValueError; record_context(full golden) -> accepted; validate_schema maxLength 3 on 10 chars -> SCHEMA_INVALID too long; maximum 10 on 99999 -> SCHEMA_INVALID above maximum; anyOf non-match -> SCHEMA_INVALID matches no anyOf branch; unknown keyword 'pattern' -> SCHEMA_UNSUPPORTED keyword; unknown type 'foo' -> SCHEMA_UNSUPPORTED type foo; extra key -> SCHEMA_INVALID unexpected key",
  "probe child_env() with ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY, AWS_SECRET_ACCESS_KEY set -> keys ['HOME','LOGNAME','PATH','TMPDIR','USER']; no ANTHROPIC/AWS key",
  "probe audited_call with schema-invalid output containing key '<img src=x onerror=alert(1)>' -> error column ['SCHEMA_INVALID' x3]; injected string in any row: False",
  "probe audited_call with FixtureMissing and sleep=naps.append -> LLMFailedFixtureMiss LLM_FAILED_AFTER_RETRIES; warning line 'llm call failed ... attempt=1 prompt_hash=a3a128eb...'; prompt text in log: False; sleep calls: []; rows: 1"
 ],
 "verdict": "pass",
 "scores": {"retry_timeout_caps": 5, "claude_cli_isolation": 4, "key_handling": 5, "log_hygiene": 5, "fixture_recorder_guard": 4, "output_schema_validation": 5, "audit_error_column": 5, "ac_conformance": 4},
 "findings": [
  {"severity": "minor", "title": "The miss-log hash line (prompt_hash=) is not pinned by any test",
   "evidence": "app/llm/audited.py:83 log.warning(... prompt_hash={h} if fixture_miss); grep -rn 'prompt_hash=' tests/ returns nothing; tests/unit/test_provider.py:41 test_fixture_miss_reports_hash_not_text checks only str(e.value) and absence of prompt text in caplog; round-1 acceptance name test_fixture_miss_logs_hash_not_text does not exist",
   "why_it_matters": "The hash in the miss log is the audit trail that makes a silent fixture miss visible (LLM09). Nothing fails if the suffix is removed from audited.py:83.",
   "fix": "In tests/unit/test_audited.py add a test that runs audited_call with a FixtureMissing carrying a known hash under caplog at WARNING, and asserts 'prompt_hash=' + that hash is in caplog.text and the prompt text is not.",
   "acceptance_test": "pytest tests/unit/test_audited.py -q passes with the new test, and fails when the prompt_hash suffix at app/llm/audited.py:83 is removed."},
  {"severity": "minor", "title": "claude-cli is selectable with one env var and puts the prompt on argv (round-1 finding 4, remainder)",
   "evidence": "app/llm/provider.py:72-76 selects claude-cli on LLM_BACKEND alone; no ZLAYT_DEV gate in code (grep -rln ZLAYT_DEV hits only board/cards/T-034.md and reviews/T-034-security.md); app/llm/backends/claude_cli.py:37-40 build_argv ends with '--', user (prompt on argv, comment: qa-pinned contract); ls Dockerfile* -> No such file or directory",
   "why_it_matters": "Checklist 16 requires the dev-only claude-cli backend to be impossible to enable in the container or public config. Today it is one env var away. Pasted record text in argv is visible to other local users via ps. Not exploitable yet because no Dockerfile exists.",
   "fix": "Raise BACKEND_UNAVAILABLE for claude-cli unless ZLAYT_DEV=1 is set. When the Docker card lands, exclude app/llm/backends/claude_cli.py from the image and fail startup if LLM_BACKEND=claude-cli. Move the prompt to stdin if the CLI supports it, or record the qa-pinned argv exception in the card.",
   "acceptance_test": "with ZLAYT_DEV unset and LLM_BACKEND=claude-cli, provider.complete raises LLMError starting BACKEND_UNAVAILABLE; with ZLAYT_DEV=1 it proceeds to the subprocess call."},
  {"severity": "nit", "title": "Recorder guard: fragment path and public record_context remain",
   "evidence": "app/llm/provider.py:36 MIN_FRAGMENT = 20; provider.py:42-46 'if t == g or (not whole_file and t in g)'; provider.py:52 def record_context (public); app/llm/record.py:20 P.assert_recordable(raw) uses the fragment default",
   "why_it_matters": "Record writes are still gated by whole-file record_context (record.py:34; probe: record_context('a') raises ValueError, full golden text accepted), so this is not exploitable. Keeping a 20-character substring path and a public context manager leaves an easy way to widen the gate later.",
   "fix": "Make record_context private to record.py, and call assert_recordable(raw, whole_file=True) in record.py:20.",
   "acceptance_test": "P.record_context('2019') and P.record_context('x'*25) raise ValueError; record.py calls the whole-file check; full golden text is accepted."}
 ],
 "whats_right": [
  "The schema validator now fails closed: probes show maxLength, maximum and anyOf are enforced, and unknown keywords and types raise SCHEMA_UNSUPPORTED instead of passing.",
  "claude-cli child env is an allowlist (app/llm/backends/claude_cli.py:25-27); ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL and cloud keys are absent from the child env in the probe.",
  "The audit error column stores only codes; the injected key '<img src=x onerror=alert(1)>' appears in no llm_calls row, and a fixture-miss row carries the hash, not the prompt text."],
 "questions_for_chris": ["Should the T-034 card's acceptance-test name (test_fixture_miss_logs_hash_not_text) be updated to match the existing test_fixture_miss_reports_hash_not_text, or should minor 1 add the log-line test under the card's name?"]}
```
