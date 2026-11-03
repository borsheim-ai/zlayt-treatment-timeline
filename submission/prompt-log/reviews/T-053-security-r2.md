# T-053 security review, round 2 (security-reviewer, Tomas Rivas lens)

Pinned code: HEAD e83eb54, extracted with `git archive` to `artifacts/review-evidence/T-053-r2/head_e83eb54`. HEAD moved during the review (02f9939 when the card went to review, then 709397e, f5444a8, e83eb54, d796383, d0c9cdb). The gate files `app/llm/provider.py`, `app/llm/backends/anthropic_api.py`, `app/main.py` and `app/backend/api.py` are byte-identical from 02f9939 through d0c9cdb (`git diff --quiet 02f9939 d0c9cdb -- ...` not run on d0c9cdb; checked 02f9939..e83eb54 exit 0, and e83eb54..d0c9cdb touches only `pipeline.py`, `audited.py` and `split_v1.md`). Everything below was run on e83eb54.

Verdict: **changes**. The round-1 blocker (demo mode sends live SDK calls) is closed on every path I could reach. Two majors remain: the local-mode loopback refusal is bypassed by the uvicorn CLI, and the library-in-local-demo admission still has no written amendment of D-020 / R-CO-4. No new blocker.

Checks requested by the brief:
1. Demo mode with `LLM_BACKEND=anthropic-api`, `ANTHROPIC_API_KEY=<redacted> `ENABLE_LIVE` unset selects the fixture backend. The SDK constructor and `messages.create` were counted and blocked: 0 events and 0 socket attempts, for `provider.complete`, the claude-cli selection, and a full API sample run. PASS.
2. `ZLAYT_MODE=local HOST=0.0.0.0` refuses to start under `python -m app.main`: exit 1, no listener. PASS for that entry point. FAIL for `uvicorn app.main:create --factory --host 0.0.0.0` with HOST unset (finding 1).
3. Library texts are admitted only in local mode: public 404 / 409, local 201. PASS for the code. The spec conflict is open (finding 2).

Probe scripts: `artifacts/review-evidence/T-053-r2-probe.py` (parts 1, 2, 2b, 3, 3b) and `artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C). Outputs: `artifacts/review-evidence/T-053-r2/out_parts_1_2_2b.txt`, `out_part3.txt`, `out_part3b.txt`, `out_probe2.txt`.

Exercised (all on e83eb54 unless noted):
- `python3 tools/board.py show T-053`; read `personas/security.md`, my memory dir, `reviews/T-053-security.md`.
- `git log --oneline -n 8`, `git show --stat 02f9939`, `git diff --stat 02f9939 709397e -- app tests`, `git diff --quiet` on the gate files between each HEAD pair listed above.
- `git archive e83eb54 | tar -x -C artifacts/review-evidence/T-053-r2/head_e83eb54` (and the same for 709397e and 02f9939 during the review).
- `.venv/bin/python -m pytest -p no:cacheprovider` in the pinned copy, with the six new or changed round-1 tests named by the card note: `test_demo_never_reaches_a_live_backend[claude-cli]`, `[anthropic-api]`, `test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set`, `test_local_mode_refuses_non_loopback_host` (5 hosts), `test_library_texts_are_admitted_only_in_local_mode`, `test_case_list_and_library_exist_only_in_local_mode`, `test_cases_do_not_leak_decisions_between_each_other`: `11 passed in 1.87s`.
- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_provider_backends.py tests/unit/test_api_routes.py tests/e2e/test_api.py -q`: `57 passed in 8.14s`.
- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q` (full unit suite): `6 failed, 867 passed in 17.34s` (see outside-lens note).
- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 1 2 2b`: output in `out_parts_1_2_2b.txt`.
- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 3` and `3b`: outputs in `out_part3.txt` and `out_part3b.txt`. Part 3b started uvicorn on port 7972 for about 5 seconds, made one HTTP GET to the machine's LAN address, and killed it. Logged output shows `uvicorn stopped`.
- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C): output in `out_probe2.txt`.
- Manual uvicorn start on port 7973 with `--host 0.0.0.0` and `ZLAYT_MODE=local` for a debug check (killed afterwards via `lsof -ti tcp:7973 | xargs kill`; listener count 0 after).
- `.venv/bin/python -c "inspect.signature(anthropic.resources.Messages.create)"`: `anthropic 2.3.0`, `temperature in Messages.create signature: False`.
- `ls requirements*.txt pyproject.toml Makefile Dockerfile` in the pinned copy: `requirements-dev.txt`, `requirements.txt` present; no pyproject, Makefile or Dockerfile. `.venv/bin/pip-audit`: `No such file or directory`.
- `.venv/bin/python tools/check_secrets.py` on the working tree at d0c9cdb: `check_secrets: ok (740 file(s) scanned)`. Key-shaped grep (`sk-ant-|sk-proj-`) over `app` and `tests` in the pinned copy: 0 hits.
- `grep` of D-020 in `memory/ORCHESTRATOR_DECISIONS.md` at e83eb54 (line 28, unchanged from 02f9939) and R-CO-4 in `spec/REQUIREMENTS.md:138`.
- `app/backend/api.py` `BANNER` at e83eb54: `Synthetic data only — never paste real records`.

Findings detail:

Finding 1 (major, new in round 2). The round-1 loopback rule reads the `HOST` environment variable, not the address uvicorn binds. `uvicorn app.main:create --factory --host 0.0.0.0` with `ZLAYT_MODE=local` and `HOST` unset starts, and the case list is served to the LAN. Verbatim from `out_part3b.txt`: `GET http://LAN-address:7972/api/cases -> 200 body keys: ['cases']` and `Python 73551 arsis 9u IPv4 ... TCP *:7972 (LISTEN)`. The gate at `app/backend/api.py:93-94` reads `os.environ.get("HOST", "127.0.0.1")`; `app/main.py:9` documents `uvicorn app.main:create --factory` as a launch line. The probe uses `--host` only, so `HOST` is never set. This is a partial fix of the round-1 major and the card decision (2): the refusal covers `python -m app.main` only.

Finding 2 (major, carried from round 1, not closed). Library texts are admitted in local demo mode, and nothing in `memory/ORCHESTRATOR_DECISIONS.md` amends D-020 for this. Verbatim D-020 (line 28, unchanged): `in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and not stored`. R-CO-4 (`spec/REQUIREMENTS.md:138`) says the same. In local mode `demo_mode()` is true whenever `ENABLE_LIVE` is unset (`app/backend/api.py:103-106`), so the spec text applies. Observed: `POST {text: library text} -> 201` in local mode and `-> 409` in public mode. The card decision (3) is a reasonable call, but it is not an amendment. Per D.2 a spec conflict is a blocker; I am holding it at major because the path is local-only and the data is synthetic. If the amendment is not written before the milestone gate, re-rate to blocker.

Finding 3 (minor). With `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api` and no key, the server reports the live backend while demo mode is on, and every run fails. Verbatim from `out_probe2.txt` check A: `/api/health: backend=anthropic-api demo_mode=True live_enabled=False` and `llm_calls (backend, error[:60], n): [('anthropic-api', 'BACKEND_UNAVAILABLE', 66)]`, with `SDK ctor/create events: 0`. No live call happens (the key check runs before the client is built), so this fails closed. It does break card decision (1), "demo mode ALWAYS uses the fixture backend", and the sample demo cannot run in this configuration. Cause: `app/llm/provider.py:27-29` returns the live name whenever `ENABLE_LIVE=1`, without the key check that `live_enabled()` applies (`app/backend/api.py:103`).

Finding 4 (minor). `RECORD_FIXTURES=1` alone opens live SDK calls on the dev eval path. Verbatim from `out_probe2.txt` check B: `backend_name() outside any context = fixture`, `run_case returned`, `[B] SDK ctor/create events: 132`. The mechanism is `app/backend/pipeline.py:392-393` and `:406`, which call `P.record_context` / `record_fragment_context` when `P._recording()` is true (`provider.py:88-89`), and those contexts set `_record_ok`, which bypasses the ENABLE_LIVE check in `provider.py:27-29`. The server does not reach this: `run_case` has no caller in `app/backend/api.py`, and `judge_summary` is called only from `app/llm/record.py:60,66`. With `RECORD_FIXTURES=1` the API sample run made `0` SDK events (`out_parts_1_2_2b.txt`, `[API run, RECORD_FIXTURES=1]`). The docstring at `provider.py:24-26` ("ALWAYS 'fixture'") is therefore true for the server and false for the dev tools. Fix: require ENABLE_LIVE=1 in addition to record mode before `_record_ok` can be set, or narrow the docstring.

Finding 5 (minor, carried from round 1, partly addressed). Pins now exist: `requirements.txt` has `anthropic==2.3.0` at line 5, with `==` pins throughout. But the pinned SDK does not accept the kwarg the backend passes: `temperature in Messages.create signature: False`, while `app/llm/backends/anthropic_api.py:26` passes `temperature=0`. So the live path cannot work with the pinned version. `pip-audit` is not installed (`.venv/bin/pip-audit: No such file or directory`), and there is no Makefile, so the round-1 request to add `pip-audit` to `make test` has no target.

Outside my lens (reported, not graded):
- Six unit tests fail at e83eb54: `test_case_extras.py` x2, `test_narrative.py` x1, `test_t037_backend.py` x3. They fail on fixture misses (judge and extract steps, `FIXTURE_MISS` rows), not on the gate. `LLM_BACKEND=fixture` resolves to `fixture` before and after round 1, so the gate change does not touch them. The card note says 865 passed; the current run is 867 passed, 6 failed.
- With the default fixture directory, the sample demo run has 18 `FIXTURE_MISS` rows out of 37 calls. With `FIXTURE_SET=curated` (`out_probe2.txt` check C) it has 38 rows and 0 errors. The public deploy needs `FIXTURE_SET=curated`, and nothing in the repo sets it (no Dockerfile or config file).

What is right:
- Demo mode cannot reach the SDK or the network: with the dummy key, `ENABLE_LIVE` unset, `LLM_BACKEND` set to anthropic-api or claude-cli, the provider call, the API sample run and the RECORD_FIXTURES=1 API run each showed `SDK constructor/create calls: 0 | socket attempts: 0`.
- The `python -m app.main` refusal is clean: `python -m app.main exit code: 1`, `stderr last line: RuntimeError: ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost`, and `listener on 7971 after refusal: none`.
- Public route gating holds with `ZLAYT_MODE` unset: `GET /api/cases -> 404 | GET /api/library -> 404`, `POST {library} -> 404`, `POST {text: library text} -> 409`.

```json
{"card": "T-053", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD e83eb54 (pinned archive artifacts/review-evidence/T-053-r2/head_e83eb54); fix commit 02f9939 and HEAD d0c9cdb checked for gate-file drift; local app runs on 127.0.0.1 (7971 refusal, 7972 and 7973 bypass checks, stopped); sample case and library case lib01 (case_lib01_er_only_then_gap); dummy key only",
 "exercised": [
  "python3 tools/board.py show T-053; read personas/security.md, memory dir, reviews/T-053-security.md",
  "git log --oneline; git show --stat 02f9939; git diff --stat 02f9939 709397e -- app tests; git diff --quiet on app/llm/provider.py, app/llm/backends/anthropic_api.py, app/main.py, app/backend/api.py between each HEAD pair (exit 0 through e83eb54 and d0c9cdb)",
  "git archive e83eb54 into artifacts/review-evidence/T-053-r2/head_e83eb54 (also 709397e and 02f9939 during the review)",
  "pytest -p no:cacheprovider on the 7 round-1 tests named in the card note: 11 passed in 1.87s",
  "pytest tests/unit/test_provider_backends.py tests/unit/test_api_routes.py tests/e2e/test_api.py -q: 57 passed in 8.14s",
  "pytest tests/unit -q: 6 failed, 867 passed in 17.34s (failures are fixture misses outside the gate)",
  "artifacts/review-evidence/T-053-r2-probe.py parts 1, 2, 2b, 3, 3b with SDK constructor and socket counting: out_parts_1_2_2b.txt, out_part3.txt, out_part3b.txt",
  "artifacts/review-evidence/T-053-r2-probe2.py checks A (ENABLE_LIVE=1 no key), B (RECORD_FIXTURES=1 dev eval path), C (FIXTURE_SET=curated sample run): out_probe2.txt",
  "manual uvicorn app.main:create --factory --host 0.0.0.0 on port 7973 with ZLAYT_MODE=local; killed afterwards",
  "inspect.signature(anthropic.resources.Messages.create) under .venv: anthropic 2.3.0, temperature not in signature",
  "ls requirements*.txt pyproject.toml Makefile Dockerfile; .venv/bin/pip-audit absent; requirements.txt line 5 anthropic==2.3.0",
  "tools/check_secrets.py on the working tree: check_secrets: ok (740 file(s) scanned); key-shaped grep over app and tests in the pinned copy: 0 hits",
  "grep memory/ORCHESTRATOR_DECISIONS.md:28 (D-020) and spec/REQUIREMENTS.md:138 (R-CO-4); api.py BANNER line 33"
 ],
 "verdict": "changes",
 "scores": {"live-call gating in demo mode (checklist 4)": 4, "local-mode exposure and bind address (checklist 18, round-1 major 2)": 2, "library admission scope vs D-020 and R-CO-4": 3, "secrets and key handling (checklist 10-11)": 4, "dependency pinning and audit (checklist 13)": 2},
 "findings": [
  {"severity": "major",
   "title": "Local-mode loopback refusal reads the HOST env var, not the bind address: uvicorn --host 0.0.0.0 exposes the case list",
   "evidence": "out_part3b.txt: 'server started (process alive): True' ; 'GET http://LAN-address:7972/api/cases -> 200 body keys: ['cases']' ; lsof 'Python 73551 ... TCP *:7972 (LISTEN)'. Gate app/backend/api.py:93-94 reads os.environ.get('HOST', '127.0.0.1'); app/main.py:9 documents 'uvicorn app.main:create --factory'. Probe launched with --host 0.0.0.0 and HOST unset under ZLAYT_MODE=local.",
   "why_it_matters": "Local mode has no authentication. GET /api/cases returns every case token, and each token is the only capability for that case. The data is synthetic (BANNER at app/backend/api.py:33), which limits the impact. The round-1 decision (2) was that local mode refuses to start unless HOST is loopback; the implemented refusal covers python -m app.main only.",
   "fix": "Enforce the rule on the peer, not the configured host: in local mode, return 404 for any /api request whose request.client.host is not a loopback address (127.0.0.1, ::1). Keep the startup check as well. Document that local mode is launched with python -m app.main.",
   "acceptance_test": "tests/unit/test_api_routes.py: TestClient(create_app(...), client=('192.168.1.20', 50000)) with ZLAYT_MODE=local returns 404 on GET /api/cases; with client=('127.0.0.1', 50000) returns 200. Probe: uvicorn --host 0.0.0.0 with ZLAYT_MODE=local: GET from the LAN address returns non-200."},
  {"severity": "major",
   "title": "Library texts admitted in local demo mode with no written amendment of D-020 / R-CO-4 (carried from round 1)",
   "evidence": "out_parts_1_2_2b.txt PART2b: public 'POST {text: library text} -> 409'; local (ZLAYT_MODE=local, HOST=127.0.0.1) 'POST {text: library text} -> 201'. memory/ORCHESTRATOR_DECISIONS.md:28 (D-020) at e83eb54: 'in demo mode accepts only text whose normalized hash ... equals a recorded fixture; anything else is rejected and not stored'. spec/REQUIREMENTS.md:138 (R-CO-4) same. app/backend/api.py:88 and :260 admit library hashes; demo_mode() true in local mode without ENABLE_LIVE (api.py:103-106).",
   "why_it_matters": "The spec says demo mode accepts only recorded text. The card decision (3) admits unrecorded library texts in local demo mode, and the decision is not written as an amendment, so the code and the spec disagree. Public build is unaffected (409). If the amendment is not recorded before the gate, this is a blocker under D.2.",
   "fix": "Chris rules. If yes, add a dated amendment to D-020 and R-CO-4 scoped to ZLAYT_MODE=local, and keep library texts on recorded fixtures only. If no, admit only texts whose hash is in app.state.recorded until T-052 records library fixtures.",
   "acceptance_test": "Either memory/ORCHESTRATOR_DECISIONS.md carries a dated D-0xx that amends D-020 for ZLAYT_MODE=local and R-CO-4 cites it, or tests/unit/test_api_routes.py asserts 409 for an unrecorded library text in local mode."},
  {"severity": "minor",
   "title": "ENABLE_LIVE=1 without a key: health reports anthropic-api while demo_mode is true; every run fails with BACKEND_UNAVAILABLE",
   "evidence": "out_probe2.txt check A: '/api/health: backend=anthropic-api demo_mode=True live_enabled=False'; \"llm_calls (backend, error[:60], n): [('anthropic-api', 'BACKEND_UNAVAILABLE', 66)]\"; 'SDK ctor/create events: 0'. Cause app/llm/provider.py:27-29 (backend_name returns the live name whenever ENABLE_LIVE=1), versus app/backend/api.py:103 (live_enabled also needs a key).",
   "why_it_matters": "No live call happens, so this fails closed. It does contradict card decision (1), 'demo mode ALWAYS uses the fixture backend', and it means the sample demo cannot run under this configuration, with the audit rows labelled as the live backend.",
   "fix": "In provider.backend_name, return 'fixture' unless ENABLE_LIVE=1 and the backend has its credential (ANTHROPIC_API_KEY for anthropic-api; claude CLI present for claude-cli), matching live_enabled().",
   "acceptance_test": "tests/unit/test_provider_backends.py: ENABLE_LIVE=1, LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY unset: backend_name() == 'fixture'; /api/health backend == 'fixture'; a sample run writes no llm_calls row with backend 'anthropic-api'."},
  {"severity": "minor",
   "title": "RECORD_FIXTURES=1 alone opens live SDK calls on the dev eval path (not reachable from the server)",
   "evidence": "out_probe2.txt check B: 'backend_name() outside any context = fixture'; 'run_case returned'; '[B] SDK ctor/create events: 132'. Mechanism: app/backend/pipeline.py:392-393 and :406 call P.record_context / record_fragment_context when P._recording() (provider.py:88-89), and those set _record_ok, which bypasses provider.py:27-29. Server path: out_parts_1_2_2b.txt '[API run, RECORD_FIXTURES=1] SDK constructor/create calls: 0'. run_case has no caller in app/backend/api.py; judge_summary is called only from app/llm/record.py:60,66.",
   "why_it_matters": "provider.py:24-26 says live calls need ENABLE_LIVE=1 'or an explicit record_context() (dev recording)', and says demo is ALWAYS fixture. The docstring is true for the server and false for the dev tools. A second env var that opens live calls is a configuration trap if the dev tools ever run on the public host.",
   "fix": "In record_context and record_fragment_context, require ENABLE_LIVE=1 before setting _record_ok (record mode then needs both env vars), or narrow the docstring to say which entry points can record.",
   "acceptance_test": "tests/unit/test_provider_backends.py: RECORD_FIXTURES=1, LLM_BACKEND=anthropic-api, key set, ENABLE_LIVE unset: pipeline.run_case(golden sample) makes 0 SDK calls (SDK constructor patched to count)."},
  {"severity": "minor",
   "title": "Pinned anthropic SDK (2.3.0) cannot accept the temperature kwarg the live backend passes; pip-audit not run; no make target",
   "evidence": "requirements.txt:5 'anthropic==2.3.0'. Under .venv: inspect.signature(anthropic.resources.Messages.create) has 'temperature' False. app/llm/backends/anthropic_api.py:26 passes temperature=0. '.venv/bin/pip-audit: No such file or directory'. ls: no Makefile, pyproject.toml or Dockerfile.",
   "why_it_matters": "The round-1 minor asked for pins plus pip-audit. Pins now exist, but the pinned SDK makes the live path fail with TypeError, and no audit is run. Checklist 13 is only partly met.",
   "fix": "Pin an SDK release whose Messages.create accepts temperature, verify the live path with a stub, install pip-audit into the venv and record 'pip-audit -r requirements.txt' output, and add a Makefile test target or a documented check command.",
   "acceptance_test": "A test asserts 'temperature' in inspect.signature(anthropic.resources.Messages.create).parameters for the pinned version; pip-audit -r requirements.txt exits 0 or each finding is triaged."}
 ],
 "whats_right": [
  "Demo mode makes no SDK or socket call: with LLM_BACKEND=anthropic-api, a dummy key and ENABLE_LIVE unset, the provider call, the API sample run and the RECORD_FIXTURES=1 API run each showed 0 SDK constructor/create calls and 0 socket attempts (out_parts_1_2_2b.txt).",
  "The python -m app.main refusal is clean: exit code 1 with the RuntimeError message, and no listener on the refused port (out_part3.txt).",
  "Public routes are gated with ZLAYT_MODE unset: GET /api/cases and GET /api/library return 404, POST {library} returns 404, and an unrecorded text returns 409 (out_parts_1_2_2b.txt PART2b)."
 ],
 "questions_for_chris": [
  "Does local demo mode admit unrecorded library texts (card decision 3)? If yes, please record the amendment to D-020 and R-CO-4 for ZLAYT_MODE=local; if no, library texts stay recorded-only until T-052 lands (finding 2).",
  "Should local mode refuse non-loopback peers outright (finding 1), or is a LAN override wanted? Round-1 question 3 is still open."
 ]}
```
