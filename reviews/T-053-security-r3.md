# T-053 security review, round 3 (security-reviewer, Tomas Rivas lens)

Pinned code: `git archive 8ec0b25` extracted to `artifacts/review-evidence/T-053-r3/head_8ec0b25`. HEAD was 08764e7 at my first check, 8ec0b25 at the pin (docs only, one line in `memory/ORCHESTRATOR_DECISIONS.md`), and 38421cc when I wrote this (`memory/SCOPE_CUTS.md` only). `git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py requirements.txt` printed nothing (exit 0), so the fix commit and everything after it leave the gate files unchanged.

Model note: the brief expected `claude-sonnet-5-5`. This session runs as Haiku 5.5 (model id `claude-haiku-5-5`), so that id is recorded.

Verdict: **changes**. Both round-2 majors are closed as written.

- F1 (uvicorn `--host 0.0.0.0` with `HOST` unset) is closed. A LAN peer gets 403 on every path, a loopback peer gets 200, and the server opened no outbound connections. Spoofed forwarding headers from the LAN are ignored.
- F2 (library texts in local demo mode, no amendment) is closed on paper. D-036 amends D-020 and R-CO-4 cites it. The basis question is in `questions_for_chris`.

The peer-address rule does not give loopback-only behaviour once a loopback reverse proxy is in front of the app. The project's own tailnet exposure is a proxy shape. That is a new **major** (finding 1). It becomes a blocker if local mode is started behind a proxy before the fix lands. Findings 2 to 4 are round-2 minors, still open, not re-graded to major.

## Checks

1. Round-2 F1 reproduction (`uvicorn app.main:create --factory --host 0.0.0.0`, `ZLAYT_MODE=local`, HOST unset, dummy key, `ENABLE_LIVE` unset, port 7981, stopped afterwards). From the LAN address 192.168.199.106: GET /api/cases, /api/health, /, POST /api/cases, and GET /api/cases with `X-Forwarded-For`/`X-Real-IP`/`Forwarded: for=127.0.0.1` all returned 403 `forbidden`. From 127.0.0.1: GET /api/cases 200 `['cases']`. Server outbound TCP lines after the requests: 0. Listener count after stop: 0. Verbatim: `LAN GET /api/cases  src=192.168.199.106 -> 403 error.code=forbidden`.
2. Round-2 F2 (D-036). `memory/ORCHESTRATOR_DECISIONS.md:44` reads "Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash ... Local mode must refuse any non-loopback client by peer address". `spec/REQUIREMENTS.md:138` (R-CO-4) cites "(D-036)". D-020 at line 28 is unchanged. No ruling on this exact point is in `submission/NEEDS_CHRIS.md` or `board/inbox/`.
3. Unit tests. The brief's `python3 -m pytest -q tests/unit/test_api_routes.py` does not run here: system `python3` has no pytest (`No module named pytest`, exit 1). The project venv runs it: `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py` gives `31 passed in 5.63s`, and the same in the pinned archive gives `31 passed in 5.58s`.
4. Carried round-2 minors (findings 2 to 4): gate files unchanged since e83eb54 (`git diff --quiet e83eb54 8ec0b25 -- app/llm/provider.py app/llm/backends/anthropic_api.py requirements.txt` exit 0). The round-2 evidence for these stands. I re-checked the SDK signature only.
5. Proxy shape (new finding 1). Probe Part B: app bound to 127.0.0.1 with `ZLAYT_MODE=local`, a plain TCP relay on 0.0.0.0:7984 and a header-adding relay on 0.0.0.0:7985. Output verbatim: `direct LAN GET to app port (no proxy): connect refused/failed (ConnectionRefusedError)`; `LAN GET via plain loopback relay :7984 (no header added) src=192.168.199.106 -> 200 ['cases']`; `LAN GET via loopback relay adding X-Forwarded-For=192.168.199.106 :7985 ... -> 403 error.code=forbidden`.
6. Startup refusal (`python -m app.main`, `HOST=0.0.0.0`, `ZLAYT_MODE=local`): exit 1, stderr last line `RuntimeError: ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost`, no listener.
7. Secrets: `git check-ignore -v .env` gives `.gitignore:25:*.env	.env`; `git ls-files .env | wc -l` gives `0`. The app does not load `.env` (no dotenv reference in `app/` or `tools/`). I did not read the `.env` contents.

## Findings

**1 (major, new in r3): the peer-address gate is not loopback-only behind a loopback proxy.** F1 is closed as written, and the peer check is right for direct access. But `is_loopback_peer` (`app/backend/api.py:81-88`) sees the proxy's address, not the client's. Every client a loopback proxy forwards passes the gate. The project's documented tailnet exposure is a proxy in front of the app port (`docs/RUNBOOK.md:8`, tailnet URL on :7860). The card handoff says the design "works behind tailscale serve (loopback peer)" (`board/cards/T-053.md`, Handoff). That is the failing shape. It is dormant today: `tools/serve_app.sh` does not set `ZLAYT_MODE`, so the tailnet app runs demo mode and `/api/cases` is 404. The data is synthetic, which limits the impact. I did not run `tailscale serve`, because it would change Chris's tailnet mapping, so I cannot say which headers it adds. A relay that adds `X-Forwarded-For` fails closed (uvicorn honours it from a loopback peer), so the tailnet outcome depends on what Tailscale sends.

**2 (minor, carried from r2 F3, still open): `ENABLE_LIVE=1` without a key reports the live backend.** `app/llm/provider.py:28` checks only `ENABLE_LIVE`, while `live_enabled()` (`app/backend/api.py:103`) also needs a key. No live call happens (fail closed). The health label and the audit rows are wrong, and card decision (1) is not met as written. Source unchanged since e83eb54. Round-2 evidence: `out_probe2.txt` check A.

**3 (minor, carried from r2 F4, still open): `RECORD_FIXTURES=1` alone opens live SDK calls on the dev path.** `provider.py:65-85` (`record_context`, `record_fragment_context`) set `_record_ok`, which bypasses the `ENABLE_LIVE` check at `provider.py:28`. The server path does not reach it (no caller in `app/backend/api.py`). Round-2 evidence: 132 SDK events in check B. Source unchanged since e83eb54.

**4 (minor, carried from r2 F5, still open): pinned SDK cannot accept the `temperature` kwarg; `pip-audit` not run.** Re-checked this round: `inspect.signature(anthropic.resources.Messages.create).parameters` contains `'temperature'`: False, with `anthropic 2.3.0`. `requirements.txt:5` pins `anthropic==2.3.0`. `app/llm/backends/anthropic_api.py:26` passes `temperature=0`, so the live path raises `TypeError`. `.venv/bin/pip-audit` is absent (`No such file or directory`), and I did not re-run an audit this round.

## What is right

- F1 closed: the peer gate returns 403 for every LAN path with `uvicorn --host 0.0.0.0` and HOST unset, and 200 for loopback (out_probe.txt Part A).
- Forwarding headers from a LAN peer are ignored (`LAN GET /api/cases + XFF/XRI/Forwarded=127.0.0.1 -> 403`).
- D-036 is written and cited: `memory/ORCHESTRATOR_DECISIONS.md:44`, `spec/REQUIREMENTS.md:138`.

## Exercised

- `python3 tools/board.py show T-053`; read `personas/security.md`, `reviews/T-053-security-r2.md`, my memory dir (project_config_gate_patterns, feedback_round2_review_workflow, project_demo_live_gate).
- `git rev-parse --short HEAD` (08764e7, then 8ec0b25, then 38421cc); `git log --oneline 08764e7..HEAD`; `git show --stat 08764e7`, `fa8a36e`, `8ec0b25`; `git show 08764e7 -- app/backend/api.py tests/unit/test_api_routes.py`; gate-file diffs listed above.
- `git archive 8ec0b25` into `artifacts/review-evidence/T-053-r3/head_8ec0b25`.
- `grep` of D-020 (line 28), D-036 (line 44), R-CO-4 (`spec/REQUIREMENTS.md:138`); read `app/backend/api.py` 77-106 and 170-190; `docs/RUNBOOK.md` 8-9 and 32; `tools/serve_app.sh`; `board/cards/T-053.md` Handoff; `grep` of `submission/NEEDS_CHRIS.md` and `board/inbox/` for library or D-036 rulings (none).
- `python3 -m pytest -q tests/unit/test_api_routes.py` (system python3: exit 1, no pytest); `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py` in the repo and in the pinned archive: 31 passed both times.
- `.venv/bin/python -I artifacts/review-evidence/T-053-r3-probe.py A B C` (output `artifacts/review-evidence/T-053-r3/out_probe.txt`): uvicorn CLI with `--host 0.0.0.0` on 7981 (killed; listener count 0); loopback relay on 7984/7985 with app on 7982 (all stopped, counts 0); `python -m app.main` with HOST=0.0.0.0 on 7983 (exit 1, no listener). Dummy key only.
- `lsof` listener counts on 7981 to 7985 before and after.
- `inspect.signature` check of `anthropic.resources.Messages.create` under `.venv` (anthropic 2.3.0).
- Not run: `tailscale serve` (would change Chris's tailnet mapping), full unit suite, `pip-audit` (not installed), `tools/check_secrets.py` and gitleaks (not part of this round's brief).

```json
{"card": "T-053", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 8ec0b25 pinned (git archive at artifacts/review-evidence/T-053-r3/head_8ec0b25; fix commit 08764e7 is an ancestor; HEAD 38421cc at write time, gate files unchanged 08764e7..HEAD); local app and relays on 127.0.0.1 and the LAN address, ports 7981-7985, all stopped; dummy key only, ENABLE_LIVE unset; sample case not run (access checks only)",
 "exercised": [
  "python3 tools/board.py show T-053; read personas/security.md, reviews/T-053-security-r2.md, memory dir",
  "git rev-parse --short HEAD (08764e7, 8ec0b25, 38421cc); git log --oneline 08764e7..HEAD; git show --stat 08764e7, fa8a36e, 8ec0b25; git show 08764e7 -- app/backend/api.py tests/unit/test_api_routes.py",
  "git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py requirements.txt: empty, exit 0; git diff --quiet e83eb54 8ec0b25 -- provider.py anthropic_api.py requirements.txt: exit 0",
  "git archive 8ec0b25 into artifacts/review-evidence/T-053-r3/head_8ec0b25",
  "grep ORCHESTRATOR_DECISIONS.md line 28 (D-020) and line 44 (D-036); spec/REQUIREMENTS.md:138 (R-CO-4 cites D-036); grep NEEDS_CHRIS.md and board/inbox for library ruling: none",
  "read app/backend/api.py 77-106 and 170-190; docs/RUNBOOK.md 8-9, 32; tools/serve_app.sh; board/cards/T-053.md Handoff",
  "python3 -m pytest -q tests/unit/test_api_routes.py: system python3 has no pytest (exit 1); .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py: 31 passed (repo and pinned archive)",
  "artifacts/review-evidence/T-053-r3-probe.py parts A, B, C with .venv/bin/python -I: output artifacts/review-evidence/T-053-r3/out_probe.txt",
  "lsof listener counts on 7981-7985 before and after; server outbound TCP lines after requests: 0",
  "inspect.signature(anthropic.resources.Messages.create) under .venv: anthropic 2.3.0, 'temperature' False",
  "git check-ignore -v .env: .gitignore:25; git ls-files .env: 0 lines"
 ],
 "verdict": "changes",
 "scores": {"live-call gating in demo mode (checklist 4)": 4, "local-mode exposure and bind address, peer and proxy (checklist 18, r2 F1)": 3, "library admission vs D-020 and R-CO-4 (r2 F2)": 4, "secrets and key handling (checklist 10-11)": 4, "dependency pinning and audit (checklist 13)": 2},
 "findings": [
  {"severity": "major",
   "title": "Local mode admits clients behind a loopback reverse proxy: the peer-address gate is not loopback-only (new in r3; r2 F1 closed as written)",
   "evidence": "artifacts/review-evidence/T-053-r3/out_probe.txt PART B: 'direct LAN GET to app port (no proxy): connect refused/failed (ConnectionRefusedError)'; 'LAN GET via plain loopback relay :7984 (no header added) src=192.168.199.106 -> 200 ['cases']'; 'LAN GET via loopback relay adding X-Forwarded-For=192.168.199.106 :7985 ... -> 403 error.code=forbidden'. app/backend/api.py:81-88 (is_loopback_peer reads request.client.host) and :176 (gate). docs/RUNBOOK.md:8 (App tailnet URL on :7860). board/cards/T-053.md Handoff: 'works behind tailscale serve (loopback peer)'.",
   "why_it_matters": "D-036 (memory/ORCHESTRATOR_DECISIONS.md:44) says local mode refuses any non-loopback client by peer address, and R-CO-4 (spec/REQUIREMENTS.md:138) says local mode is loopback only. A reverse proxy on 127.0.0.1 makes every client it forwards look like a loopback peer, so /api/cases and every case token reach any client that can reach the proxy. The project's documented tailnet exposure is a proxy in front of the app port (RUNBOOK.md:8). Dormant today: tools/serve_app.sh does not set ZLAYT_MODE, so the tailnet app runs demo mode. Data is synthetic, which limits impact. Re-rate to blocker if local mode is started behind tailscale serve or any proxy before the fix lands. A relay that adds X-Forwarded-For fails closed, so the tailscale serve outcome depends on the headers it sends; not verified (tailscale serve not run, it would change Chris's tailnet mapping).",
   "fix": "In local mode, fail closed on the request as well as the socket peer: (a) refuse any request whose Host header is not localhost, 127.0.0.1 or [::1] with an optional port (DNS-rebinding style allowlist); (b) refuse any request carrying Forwarded, X-Forwarded-For, X-Real-IP or Tailscale-* headers. Keep is_loopback_peer. Document that local mode is for direct loopback access only and must not be served through tailscale serve or any proxy. Update the test client default (TestClient uses Host testserver) to a localhost Host.",
   "acceptance_test": "tests/unit/test_api_routes.py: with ZLAYT_MODE=local and client=('127.0.0.1',5000): Host '192.168.199.106:7984' returns 403; Host 'localhost:7860' returns 200; a request with X-Forwarded-For returns 403; a request with Host 'localhost:7860' and no forwarding headers returns 200. Probe: rerun artifacts/review-evidence/T-053-r3-probe.py B; the plain-relay line must read 403."},
  {"severity": "minor",
   "title": "ENABLE_LIVE=1 without a key: health reports anthropic-api while demo_mode is true; every run fails BACKEND_UNAVAILABLE (carried from r2 F3, still open)",
   "evidence": "app/llm/provider.py:28 (backend_name checks ENABLE_LIVE only); app/backend/api.py:103 (live_enabled also needs ANTHROPIC_API_KEY). Source unchanged since e83eb54 (git diff --quiet exit 0). Round-2 evidence: artifacts/review-evidence/T-053-r2/out_probe2.txt check A.",
   "why_it_matters": "No live call happens, so this fails closed. It contradicts card decision (1) ('demo mode ALWAYS uses the fixture backend') and mislabels the audit rows. Not re-probed this round.",
   "fix": "In provider.backend_name, return 'fixture' unless ENABLE_LIVE=1 and the backend's credential is present (ANTHROPIC_API_KEY for anthropic-api; claude CLI for claude-cli), matching live_enabled().",
   "acceptance_test": "tests/unit/test_provider_backends.py: ENABLE_LIVE=1, LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY unset: backend_name() == 'fixture'; /api/health backend == 'fixture'."},
  {"severity": "minor",
   "title": "RECORD_FIXTURES=1 alone opens live SDK calls on the dev eval path (carried from r2 F4, still open)",
   "evidence": "app/llm/provider.py:65-85 (record_context and record_fragment_context set _record_ok) and :28 (ENABLE_LIVE check bypassed when _record_ok). Source unchanged since e83eb54. Round-2 evidence: out_probe2.txt check B, 132 SDK events.",
   "why_it_matters": "Not reachable from the server today (run_case and judge_summary have no caller in app/backend/api.py). A second env var that opens live calls is a configuration trap if the dev tools run on the public host.",
   "fix": "Require ENABLE_LIVE=1 before record_context or record_fragment_context can set _record_ok, or narrow the docstring at provider.py:6 and :24-26 to name the entry points that may record.",
   "acceptance_test": "tests/unit/test_provider_backends.py: RECORD_FIXTURES=1, LLM_BACKEND=anthropic-api, key set, ENABLE_LIVE unset: pipeline.run_case(golden sample) makes 0 SDK calls (SDK constructor patched to count)."},
  {"severity": "minor",
   "title": "Pinned anthropic SDK 2.3.0 cannot accept the temperature kwarg the live backend passes; pip-audit not installed (carried from r2 F5, still open)",
   "evidence": "requirements.txt:5 'anthropic==2.3.0'. inspect.signature(anthropic.resources.Messages.create).parameters: 'temperature' in it: False (anthropic 2.3.0, .venv). app/llm/backends/anthropic_api.py:26 passes temperature=0. '.venv/bin/pip-audit: No such file or directory'.",
   "why_it_matters": "The live path raises TypeError with the pinned SDK, and no dependency audit is recorded. Checklist 13 stays partly met.",
   "fix": "Pin an SDK release whose Messages.create accepts temperature, verify the live path with a stub, install pip-audit and record 'pip-audit -r requirements.txt' output (or triage each finding), and add a check command.",
   "acceptance_test": "A unit test asserts 'temperature' in inspect.signature(anthropic.resources.Messages.create).parameters for the pinned version; pip-audit -r requirements.txt exits 0 or each finding is triaged in the review."}
 ],
 "whats_right": [
  "F1 closed: with uvicorn --host 0.0.0.0 and HOST unset, every LAN request gets 403 and loopback gets 200; zero outbound connections from the server (out_probe.txt Part A).",
  "Forwarding headers sent by a LAN peer (X-Forwarded-For, X-Real-IP, Forwarded) are ignored: the request is still 403.",
  "D-036 is written and cited: memory/ORCHESTRATOR_DECISIONS.md:44 amends D-020 and spec/REQUIREMENTS.md:138 (R-CO-4) cites it."
 ],
 "questions_for_chris": [
  "D-036 rests on D-031 (multi-case scope). Is that your ruling that library texts may pass the demo gate in local mode? No ruling on this exact point is in NEEDS_CHRIS.md or board/inbox. If you did not intend it, say so and the amendment is reversed.",
  "Do you want local mode reachable from your tailnet (phone)? If yes, the rule must change (peer address cannot give loopback-only behind a proxy). If no, keep local mode off the tailnet app URL and apply the Host and forwarding-header fix (finding 1)."
 ]}
```

---

Correction, appended after the JSON block (the record above stands otherwise): in finding 2 the `live_enabled()` reference is `app/backend/api.py:113`, not `:103`. I checked line numbers with grep after writing the record. No other line reference is affected.
