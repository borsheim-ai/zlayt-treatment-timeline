# T-034 security review (security-reviewer, claude-sonnet-5-5)

Verdict: **changes**. No blockers. The security-relevant design is sound: SDK `max_retries=0` with a 120 s timeout, a claude-cli argv with no tools/MCP/hooks that runs outside the project, the API key read only inside `anthropic_api.py`, no record text in logs, a fixture miss mapped to `LLM_FAILED_AFTER_RETRIES` with one row per attempt, and no shell. One major: the requested pytest command is red on the current tree.

The command `.venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q` gives `12 failed, 25 passed`.
- 4 failures are `AttributeError: module 'app.llm.provider' has no attribute 'FixtureMissing'`.
- 8 failures are `TypeError: audited_call() got an unexpected keyword argument 'sleep'`.
- `tests/unit/test_provider.py` and `tests/unit/test_audited.py` have uncommitted edits (`git status`: ` M`). A `git archive 958c353` export of the committed tree gives `30 passed`.
- So the commit passes its own tests, but the card's AC8 wording (`FixtureMissing`, "logged with the prompt hash") and the tightened tests are not met by the implementation.

Probes run (script `/private/tmp/claude-501/.../scratchpad/p.py`):
- An argv built with record text `x'; rm -rf ~ ; \`id\` $(id)\n--dangerously-skip-permissions --tools Bash --mcp-config evil.json` keeps the whole string as one element after `--`. The flag section is unchanged.
- `assert_recordable("a")`, `("the")` and `("2019")` all pass.
- `validate_schema` accepts `maxLength`, `maximum` and `anyOf` violations.

## Checks against the brief
- The SDK client is built with `max_retries=0, timeout=120.0` (`anthropic_api.py:15`). Pass.
- The claude-cli argv has a pinned `--model`, `--tools ""`, `--strict-mcp-config`, `disableAllHooks`, `--no-session-persistence` and the prompt after `--`. It runs with `cwd=mkdtemp`, `timeout=120`, a `BoundedSemaphore(3)`, a list argv (no `shell=True`) and `stdin=DEVNULL`. Pass.
- JSON from the model is parsed and then checked by `validate_schema` in code. Pass, with finding 3.
- `ANTHROPIC_API_KEY` appears only in `anthropic_api.py:15,20` and as a strip in `claude_cli.py:36`. Pass.
- Logs: `audited.py:73` logs only call_id, step and attempt. Backend errors carry class or code only. `test_no_text_in_logs` passes on the commit. Pass, except that the hash is not logged (finding 1).
- The default is `LLM_BACKEND=fixture`, and an unknown value raises `UNKNOWN_BACKEND` instead of going live. This is fail-closed.
- A `FixtureMiss` is a single attempt, writes one row, and raises `LLMFailedFixtureMiss` (code `LLM_FAILED_AFTER_RETRIES`). The other failures write one row per attempt, three at most.

Outside my lens: whether `error` and prompt storage in `llm_calls` meets retention rules (privacy-compliance-reviewer). Docker and CLI exclusion (checklist 15 and 16) cannot be checked yet because there is no Dockerfile.

```json
{"card": "T-034", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 958c353 (app/llm/{provider,audited,record,_types}.py, backends/*) plus uncommitted tests/unit/test_provider.py and test_audited.py edits in the working tree; no app URL (library card)",
 "exercised": [
  "python3 tools/board.py show T-034",
  ".venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q -> 12 failed, 25 passed (working tree)",
  "LLM_BACKEND=fixture pytest of the same three files -> 12 failed, 25 passed",
  "git archive 958c353 exported to scratchpad, same pytest command -> 30 passed",
  "git status / git diff of tests/unit/test_provider.py to see the uncommitted test changes",
  "read provider.py, audited.py, _types.py, record.py, backends/{claude_cli,anthropic_api,fixture}.py in full",
  "grep for ANTHROPIC_API_KEY, subprocess, shell=True, Popen, os.system, logging and print under app/ and tools/",
  "probe script: injection-laden record text through claude_cli.build_argv; assert_recordable on 'a', 'the', '2019'; validate_schema with maxLength, maximum and anyOf violations",
  "claude --help flag check for --tools, --strict-mcp-config, --settings, --system-prompt, --no-session-persistence, --bare",
  "python3 tools/check_secrets.py -> 'check_secrets: ok (305 file(s) scanned)'",
  "git check-ignore .env; ls Dockerfile* (none exists)"],
 "verdict": "changes",
 "scores": {"retry_timeout_caps": 5, "claude_cli_isolation": 4, "key_handling": 5, "log_hygiene": 4, "fixture_recorder_guard": 2, "output_schema_validation": 3, "ac_conformance": 2},
 "findings": [
  {"severity": "major", "title": "AC8 and the current T-034 tests are not met: FixtureMissing name, hash logging, and the sleep seam are missing; 12 tests red",
   "evidence": "pytest on the working tree: 12 failed. 'AttributeError: module app.llm.provider has no attribute FixtureMissing. Did you mean: FixtureMiss?' (tests/unit/test_provider.py:32). 'TypeError: audited_call() got an unexpected keyword argument sleep' (tests/unit/test_audited.py:27, 8 tests). audited.py:73 logs 'llm call failed call_id=%s step=%s attempt=%d' with no prompt hash, while AC8 and test_fixture_miss_logs_hash_not_text require the miss to be logged with the prompt hash. The hash is only in the DB row error field. The implementation names the class FixtureMiss (_types.py:11) and has no sleep parameter. Passing at 958c353 (30 passed) but red against the uncommitted test edits.",
   "why_it_matters": "The audited retry loop is the OWASP LLM10 control for this card, and the fixture-miss audit trail is what makes a silent default answer detectable (LLM09). The card cannot be accepted while its named tests fail. Neither the AC nor the tests are ambiguous: AC8 says FixtureMissing and logged with the prompt hash.",
   "fix": "Export FixtureMissing from provider (rename FixtureMiss or alias it) and log the miss with the 64-hex prompt hash and no text. Add the sleep seam to audited_call (a short capped backoff, never user-controlled) if the tightened tests are the intended contract. Re-run the three files with no key. If the test edits are wrong instead, have QA revert them and amend AC8.",
   "acceptance_test": ".venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q reports 0 failed on a clean tree; test_fixture_miss_logs_hash_not_text asserts the hash is in the log and the prompt text is not."},
  {"severity": "minor", "title": "Recorder guard is a substring test; record_context accepts any fragment of golden text",
   "evidence": "provider.py:44 'if t in _norm(p.read_text())'. Probe: assert_recordable('a'), ('the') and ('2019') all return without error. record_context() is a public context manager that sets the process-global _record_ok (provider.py:49-56), so any code can open it with a one-character string and then run a live backend over non-golden text with RECORD_FIXTURES=1. record_file() itself is safe because it requires a .txt under evals/golden after resolve().",
   "why_it_matters": "'Recorder refuses non-golden text' is only enforced on the CLI path. The guard does not tie the text being sent to the model to the text that was validated. Fixtures store model output, which can quote record text, into a committed directory.",
   "fix": "Require a whole-file match, or a minimum length plus whole-line containment. Better, derive the allow-list from the case text actually passed to the pipeline. Make record_context private to record.py.",
   "acceptance_test": "test: P.record_context('a') and P.record_context('2019') raise ValueError; record_context(<full golden file text>) is accepted."},
  {"severity": "minor", "title": "Mini JSON-Schema validator fails open on unsupported keywords",
   "evidence": "_types.py:50-90 handles only type, enum, required, properties, additionalProperties:false and items. Probe: validate_schema({'s':'x'*10000,'n':99999}, {... 'maxLength':5 ... 'maximum':10 ...}) returned without error ('maxLength/maximum NOT enforced'); anyOf with a non-matching enum also passed ('anyOf NOT enforced'). Unknown type names raise KeyError (_TYPES[x]), not LLMError.",
   "why_it_matters": "Deterministic schema validation in code is the LLM01 mitigation. Any constraint a later prompt schema (T-035 and following) writes with a keyword outside this subset is silently not applied, and the author gets a false sense of enforcement. No current schema uses these keywords, so this is not yet exploitable.",
   "fix": "Raise on any schema keyword outside the supported set (fail closed), and map unknown types to LLMError. Or add jsonschema to the pinned requirements and use it.",
   "acceptance_test": "unit test: validate_schema(..., {'type':'string','maxLength':3}) either enforces maxLength or raises on the unsupported keyword; never passes silently."},
  {"severity": "minor", "title": "claude-cli child gets the full environment and the record text on argv; nothing blocks claude-cli in a public config",
   "evidence": "claude_cli.py:36 env = {k: v for k, v in os.environ.items() if k != 'ANTHROPIC_API_KEY'} passes ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, cloud credentials and anything else to the child. claude_cli.py:28-31 puts the user prompt on argv (stdin=DEVNULL), which is visible in ps to other local users. provider.py:67-73 selects claude-cli whenever LLM_BACKEND=claude-cli, with no check for a container or public flag. No Dockerfile exists yet.",
   "why_it_matters": "Checklist 16 requires that the dev-only claude-cli backend cannot be enabled in the public config. Today it takes only one env var. Passing the full environment and putting pasted record text in argv widen the exposure on a shared dev box.",
   "fix": "Build the child env from an allowlist (PATH, HOME, LANG, TMPDIR, CLAUDE_BIN), drop all ANTHROPIC_* variables, and send the prompt on stdin if the CLI supports it. Refuse claude-cli unless an explicit dev flag is set (for example ZLAYT_DEV=1). Make the Docker build exclude the module and fail startup if LLM_BACKEND=claude-cli.",
   "acceptance_test": "test: with ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL set, they are absent from the env passed to subprocess.run; with ZLAYT_DEV unset, LLM_BACKEND=claude-cli raises BACKEND_UNAVAILABLE."},
  {"severity": "nit", "title": "Audit error column can store model-controlled text",
   "evidence": "audited.py:~46 stores str(e)[:200] for LLMError and ValueError. _types.py:76 builds 'SCHEMA_INVALID $: unexpected [<keys from model output>]'. A validate callback that raises ValueError with an excerpt would also land in the row.",
   "why_it_matters": "Rows are removed with the case and are never logged, so the exposure is small. Model-chosen strings in a DB field that may later be shown in a debug view are a stored-XSS vector if rendered with innerHTML.",
   "fix": "Keep the error code and the path only. Do not echo output keys or values. Render audit rows with textContent.",
   "acceptance_test": "test: schema-invalid output with an extra key '<img src=x onerror=alert(1)>' leaves a row error that does not contain that string."}
 ],
 "whats_right": [
  "Retries are owned only by audited.py, with a hard cap of 3 attempts, the SDK set to max_retries=0 with timeout=120, and the CLI set to timeout=120 with a 3-way semaphore.",
  "The claude-cli argv is a list with `--` before the user prompt, so prompt-injection text cannot add flags, tools or MCP config (probe confirmed). The ANTHROPIC_API_KEY read is confined to anthropic_api.py and stripped from the child env.",
  "Fail-closed defaults: LLM_BACKEND defaults to fixture, an unknown backend raises, a miss is never retried and never answered with a default, and backend exceptions are reduced to a class name so the SDK cannot echo record text."],
 "questions_for_chris": ["Is the intended contract the uncommitted QA tests (FixtureMissing, sleep backoff, miss logged with hash) or the 958c353 behaviour? The card AC8 text says FixtureMissing and logged with the hash, so I have treated the tests as authoritative."]}
```
