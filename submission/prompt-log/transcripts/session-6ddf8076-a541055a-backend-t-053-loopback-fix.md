# Subagent: Backend: T-053 loopback fix (Backend: T-053 loopback fix)

Source: `agent-a541055a161285c40.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:32:14.472Z

You own board card T-053, round 3 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-053-security-r2.md, finding 1, and memory/ORCHESTRATOR_DECISIONS.md D-036. Finding 2 is resolved by D-036, so don't change library admission.

Fix: with ZLAYT_MODE=local, the app must refuse any request whose peer address (request.client.host) is not loopback (127.0.0.0/8, ::1). That holds however the server was started, including `uvicorn app.main:create --factory --host 0.0.0.0`. Return 403 with a short JSON error. Keep the existing HOST startup check. Note that tailscale serve proxies from localhost, so loopback peers must keep working.

Add a test in tests/unit/test_api_routes.py that uses a non-loopback client address (for example, Starlette TestClient(client=("192.168.1.5", 5000)) or an ASGI scope override) and asserts 403 on /api/cases in local mode and 200 for loopback.

Run `python3 -m pytest -q tests/unit`. Commit with `git add <paths>` then `git commit` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Check the AC with `board.py ac`, add a note naming the commit, do the handoff, and run `board.py move T-053 in_review --agent backend`. Then restart the app with `tools/serve_app.sh`. Reply in 3 lines max.

### User / tool · 2026-11-02T02:32:14.478Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:18.589Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-036\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; grep -n \"inding 1\" -B2 -A15 reviews/T-053-security-r2.md | head -50; grep -n \"ZLAYT_MODE\\|HOST\" -r app/backend/*.py | head -30; cat tools/serve_app.sh | head -30"
}
````

### User / tool · 2026-11-02T02:32:18.710Z

**tool result**
````
44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
7-Checks requested by the brief:
8-1. Demo mode with `LLM_BACKEND=anthropic-api`, `ANTHROPIC_API_KEY=<redacted> `ENABLE_LIVE` unset selects the fixture backend. The SDK constructor and `messages.create` were counted and blocked: 0 events and 0 socket attempts, for `provider.complete`, the claude-cli selection, and a full API sample run. PASS.
9:2. `ZLAYT_MODE=local HOST=0.0.0.0` refuses to start under `python -m app.main`: exit 1, no listener. PASS for that entry point. FAIL for `uvicorn app.main:create --factory --host 0.0.0.0` with HOST unset (finding 1).
10-3. Library texts are admitted only in local mode: public 404 / 409, local 201. PASS for the code. The spec conflict is open (finding 2).
11-
12-Probe scripts: `artifacts/review-evidence/T-053-r2-probe.py` (parts 1, 2, 2b, 3, 3b) and `artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C). Outputs: `artifacts/review-evidence/T-053-r2/out_parts_1_2_2b.txt`, `out_part3.txt`, `out_part3b.txt`, `out_probe2.txt`.
13-
14-Exercised (all on e83eb54 unless noted):
15-- `python3 tools/board.py show T-053`; read `personas/security.md`, my memory dir, `reviews/T-053-security.md`.
16-- `git log --oneline -n 8`, `git show --stat 02f9939`, `git diff --stat 02f9939 709397e -- app tests`, `git diff --quiet` on the gate files between each HEAD pair listed above.
17-- `git archive e83eb54 | tar -x -C artifacts/review-evidence/T-053-r2/head_e83eb54` (and the same for 709397e and 02f9939 during the review).
18-- `.venv/bin/python -m pytest -p no:cacheprovider` in the pinned copy, with the six new or changed round-1 tests named by the card note: `test_demo_never_reaches_a_live_backend[claude-cli]`, `[anthropic-api]`, `test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set`, `test_local_mode_refuses_non_loopback_host` (5 hosts), `test_library_texts_are_admitted_only_in_local_mode`, `test_case_list_and_library_exist_only_in_local_mode`, `test_cases_do_not_leak_decisions_between_each_other`: `11 passed in 1.87s`.
19-- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_provider_backends.py tests/unit/test_api_routes.py tests/e2e/test_api.py -q`: `57 passed in 8.14s`.
20-- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q` (full unit suite): `6 failed, 867 passed in 17.34s` (see outside-lens note).
21-- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 1 2 2b`: output in `out_parts_1_2_2b.txt`.
22-- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 3` and `3b`: outputs in `out_part3.txt` and `out_part3b.txt`. Part 3b started uvicorn on port 7972 for about 5 seconds, made one HTTP GET to the machine's LAN address, and killed it. Logged output shows `uvicorn stopped`.
23-- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C): output in `out_probe2.txt`.
24-- Manual uvicorn start on port 7973 with `--host 0.0.0.0` and `ZLAYT_MODE=local` for a debug check (killed afterwards via `lsof -ti tcp:7973 | xargs kill`; listener count 0 after).
--
31-Findings detail:
32-
33:Finding 1 (major, new in round 2). The round-1 loopback rule reads the `HOST` environment variable, not the address uvicorn binds. `uvicorn app.main:create --factory --host 0.0.0.0` with `ZLAYT_MODE=local` and `HOST` unset starts, and the case list is served to the LAN. Verbatim from `out_part3b.txt`: `GET http://LAN-address:7972/api/cases -> 200 body keys: ['cases']` and `Python 73551 arsis 9u IPv4 ... TCP *:7972 (LISTEN)`. The gate at `app/backend/api.py:93-94` reads `os.environ.get("HOST", "127.0.0.1")`; `app/main.py:9` documents `uvicorn app.main:create --factory` as a launch line. The probe uses `--host` only, so `HOST` is never set. This is a partial fix of the round-1 major and the card decision (2): the refusal covers `python -m app.main` only.
34-
35-Finding 2 (major, carried from round 1, not closed). Library texts are admitted in local demo mode, and nothing in `memory/ORCHESTRATOR_DECISIONS.md` amends D-020 for this. Verbatim D-020 (line 28, unchanged): `in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and not stored`. R-CO-4 (`spec/REQUIREMENTS.md:138`) says the same. In local mode `demo_mode()` is true whenever `ENABLE_LIVE` is unset (`app/backend/api.py:103-106`), so the spec text applies. Observed: `POST {text: library text} -> 201` in local mode and `-> 409` in public mode. The card decision (3) is a reasonable call, but it is not an amendment. Per D.2 a spec conflict is a blocker; I am holding it at major because the path is local-only and the data is synthetic. If the amendment is not written before the milestone gate, re-rate to blocker.
36-
37-Finding 3 (minor). With `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api` and no key, the server reports the live backend while demo mode is on, and every run fails. Verbatim from `out_probe2.txt` check A: `/api/health: backend=anthropic-api demo_mode=True live_enabled=False` and `llm_calls (backend, error[:60], n): [('anthropic-api', 'BACKEND_UNAVAILABLE', 66)]`, with `SDK ctor/create events: 0`. No live call happens (the key check runs before the client is built), so this fails closed. It does break card decision (1), "demo mode ALWAYS uses the fixture backend", and the sample demo cannot run in this configuration. Cause: `app/llm/provider.py:27-29` returns the live name whenever `ENABLE_LIVE=1`, without the key check that `live_enabled()` applies (`app/backend/api.py:103`).
38-
39-Finding 4 (minor). `RECORD_FIXTURES=1` alone opens live SDK calls on the dev eval path. Verbatim from `out_probe2.txt` check B: `backend_name() outside any context = fixture`, `run_case returned`, `[B] SDK ctor/create events: 132`. The mechanism is `app/backend/pipeline.py:392-393` and `:406`, which call `P.record_context` / `record_fragment_context` when `P._recording()` is true (`provider.py:88-89`), and those contexts set `_record_ok`, which bypasses the ENABLE_LIVE check in `provider.py:27-29`. The server does not reach this: `run_case` has no caller in `app/backend/api.py`, and `judge_summary` is called only from `app/llm/record.py:60,66`. With `RECORD_FIXTURES=1` the API sample run made `0` SDK events (`out_parts_1_2_2b.txt`, `[API run, RECORD_FIXTURES=1]`). The docstring at `provider.py:24-26` ("ALWAYS 'fixture'") is therefore true for the server and false for the dev tools. Fix: require ENABLE_LIVE=1 in addition to record mode before `_record_ok` can be set, or narrow the docstring.
40-
41-Finding 5 (minor, carried from round 1, partly addressed). Pins now exist: `requirements.txt` has `anthropic==2.3.0` at line 5, with `==` pins throughout. But the pinned SDK does not accept the kwarg the backend passes: `temperature in Messages.create signature: False`, while `app/llm/backends/anthropic_api.py:26` passes `temperature=0`. So the live path cannot work with the pinned version. `pip-audit` is not installed (`.venv/bin/pip-audit: No such file or directory`), and there is no Makefile, so the round-1 request to add `pip-audit` to `make test` has no target.
42-
43-Outside my lens (reported, not graded):
44-- Six unit tests fail at e83eb54: `test_case_extras.py` x2, `test_narrative.py` x1, `test_t037_backend.py` x3. They fail on fixture misses (judge and extract steps, `FIXTURE_MISS` rows), not on the gate. `LLM_BACKEND=fixture` resolves to `fixture` before and after round 1, so the gate change does not touch them. The card note says 865 passed; the current run is 867 passed, 6 failed.
45-- With the default fixture directory, the sample demo run has 18 `FIXTURE_MISS` rows out of 37 calls. With `FIXTURE_SET=curated` (`out_probe2.txt` check C) it has 38 rows and 0 errors. The public deploy needs `FIXTURE_SET=curated`, and nothing in the repo sets it (no Dockerfile or config file).
46-
47-What is right:
48-- Demo mode cannot reach the SDK or the network: with the dummy key, `ENABLE_LIVE` unset, `LLM_BACKEND` set to anthropic-api or claude-cli, the provider call, the API sample run and the RECORD_FIXTURES=1 API run each showed `SDK constructor/create calls: 0 | socket attempts: 0`.
--
109- "questions_for_chris": [
110-  "Does local demo mode admit unrecorded library texts (card decision 3)? If yes, please record the amendment to D-020 and R-CO-4 for ZLAYT_MODE=local; if no, library texts stay recorded-only until T-052 lands (finding 2).",
111:  "Should local mode refuse non-loopback peers outright (finding 1), or is a LAN override wanted? Round-1 question 3 is still open."
112- ]}
113-```
app/backend/api.py:77:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:93:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:94:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:490:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/backend/present.py:195:    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:20.472Z

**tool call — Bash**
````
{
 "command": "sed -n 70,125p app/backend/api.py; grep -n \"def create\\|add_middleware\\|@app.middleware\\|FastAPI(\" app/backend/api.py app/main.py; grep -n \"TestClient\\|^def client\\|fixture\" tests/unit/test_api_routes.py | head -20; git status --short | head"
}
````

### User / tool · 2026-11-02T02:32:20.610Z

**tool result**
````
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL

app/main.py:8:def create():
app/backend/api.py:80:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
app/backend/api.py:83:    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
app/backend/api.py:155:    @app.middleware("http")
app/backend/api.py:218:    async def create_case(request: Request):
app/backend/api.py:234:    async def create_case_from_pdf(request: Request, name: str = None):
7:from fastapi.testclient import TestClient
15:@pytest.fixture
17:    monkeypatch.setenv("LLM_BACKEND", "fixture")
21:    return db, TestClient(create_app(db, static_dir=str(tmp_path)))
43:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
85:    assert g["review"]["queue"] and g["tray"] == [] and g["backend"] == "fixture"
101:    assert w["item"]["ladder"]["backend"] == "fixture" and w["calls"] and w["source"][0]["highlight_start"] is not None
118:    c2 = TestClient(create_app(db, static_dir=str(tmp_path)))           # restart: the decision is still there
168:    assert ex["internal_notes_text"]    # golden byte-equality runs on the curated fixture set (D-029, qa T-051)
169:    assert ex["totals"]["charges_cents"] == 839000 and ex["provenance"]["backend"] == "fixture" and "counts" in ex
221:    monkeypatch.setenv("LLM_BACKEND", "fixture")
223:    c = TestClient(create_app(db, static_dir=str(tmp_path), pipeline=_Boom), raise_server_exceptions=False)
306:def test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set(env, monkeypatch):
309:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:22.520Z

**tool call — Bash**
````
{
 "command": "sed -n 150,175p app/backend/api.py; sed -n 1,25p tests/unit/test_api_routes.py; sed -n 285,330p tests/unit/test_api_routes.py; grep -n \"^import\\|^from\" app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T02:32:22.620Z

**tool result**
````
    @app.exception_handler(RequestValidationError)
    async def _validation(_, e):
        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)

    @app.middleware("http")
    async def _headers(request, call_next):
        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
            purged["at"] = time.time()
            c = conn()
            try:
                DB.purge_expired(c, time.time())
            finally:
                c.close()
        try:
            resp = await call_next(request)
        except Exception as e:                                                          # last line of defence: standard JSON, no detail
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp

    async def body_of(request: Request) -> dict:
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def wait_ready(c, tok):
    for _ in range(160):
    monkeypatch.setenv("ZLAYT_MODE", "local")
    lib = c.get("/api/library").json()["cases"]
    assert lib and "path" not in lib[0] and {"id", "name", "description"} <= set(lib[0])
    r = c.post("/api/cases", json={"library": lib[0]["id"]})
    assert r.status_code == 201 and r.json()["token"] != tok
    listed = c.get("/api/cases").json()["cases"]
    assert [x["token"] for x in listed][:2] == [r.json()["token"], tok] and {"name", "status", "record_count", "counts", "created_at"} <= set(listed[0])
    assert "text" not in listed[0] and c.post("/api/cases", json={"library": "nope"}).status_code == 404


def test_cases_do_not_leak_decisions_between_each_other(env, monkeypatch):
    """T-053 AC3 (API half): decisions on one case never show on the other."""
    _, c = env
    monkeypatch.setenv("ZLAYT_MODE", "local")
    a, b = run_case(c), run_case(c, G.raw("case_01_date_formats"))
    ea = c.get(f"/api/cases/{a}").json()["entries"][0]["id"]
    assert c.post(f"/api/cases/{a}/items/{ea}/review", json={"action": "accept"}).status_code == 200
    la = {x["token"]: x["counts"] for x in c.get("/api/cases").json()["cases"]}
    assert la[a]["accepted"] == 1 and la[b]["accepted"] == 0


def test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set(env, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False


@pytest.mark.parametrize("host,ok", [("127.0.0.1", True), ("::1", True), ("localhost", True), ("0.0.0.0", False), ("192.168.1.20", False)])
def test_local_mode_refuses_non_loopback_host(tmp_path, monkeypatch, host, ok):
    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", host)
    if ok:
        create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path))
    else:
        with pytest.raises(RuntimeError):
            create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path))
    monkeypatch.delenv("ZLAYT_MODE")
    monkeypatch.setenv("HOST", "0.0.0.0")
    create_app(str(tmp_path / "h2.sqlite"), static_dir=str(tmp_path))          # public demo may bind anywhere


def test_library_texts_are_admitted_only_in_local_mode(env, tmp_path, monkeypatch):
    import app.backend.api as A
    lib = tmp_path / "lib"; lib.mkdir()
    (lib / "lib_case.txt").write_text(G.raw("sample").replace("Jordan Rivera", "Library Person"))
    monkeypatch.setattr(A, "LIBRARY", lib)
    text = (lib / "lib_case.txt").read_text()
6:import hashlib
7:import asyncio
8:import json
9:import logging
10:import os
11:import pathlib
12:import threading
13:import time
15:from fastapi import FastAPI, Request
16:from fastapi.exceptions import RequestValidationError
17:from fastapi.responses import JSONResponse, Response
18:from starlette.exceptions import HTTPException as StarletteHTTPException
20:from starlette.concurrency import run_in_threadpool
22:from app.backend import case_extras, ingest, narrative, pdf_text, present, review, store
23:from app.db import db as DB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:31.107Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\ns=s.replace('''def local_mode() -> bool:\n    return os.environ.get(\"ZLAYT_MODE\") == \"local\"\n''','''def local_mode() -> bool:\n    return os.environ.get(\"ZLAYT_MODE\") == \"local\"\n\n\ndef is_loopback_peer(request) -> bool:\n    \"\"\"True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback.\"\"\"\n    host = request.client.host if request.client else None\n    try:\n        ip = ipaddress.ip_address(host)\n    except (TypeError, ValueError):\n        return False\n    return (ip.ipv4_mapped or ip).is_loopback\n''',1)\ns=s.replace(\"import hashlib\\n\",\"import hashlib\\nimport ipaddress\\n\",1)\ns=s.replace('''        try:\n            resp = await call_next(request)\n        except Exception as e:                                                          # last line''','''        try:\n            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound\n                resp = JSONResponse({\"error\": {\"code\": \"forbidden\", \"message\": \"Local mode accepts loopback clients only.\", \"detail\": {}}}, status_code=403)\n            else:\n                resp = await call_next(request)\n        except Exception as e:                                                          # last line''',1)\nopen(p,'w').write(s)\nEOF\ncat >> tests/unit/test_api_routes.py <<'EOF'\n\n\ndef test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):\n    \"\"\"D-036: peer address, not the HOST env var, gates local mode (covers `uvicorn --host 0.0.0.0`).\"\"\"\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\"); monkeypatch.setenv(\"ZLAYT_MODE\", \"local\"); monkeypatch.delenv(\"HOST\", raising=False)\n    app = create_app(str(tmp_path / \"p.sqlite\"), static_dir=str(tmp_path))\n    for peer in (\"127.0.0.1\", \"127.0.0.5\", \"::1\", \"::ffff:127.0.0.1\"):\n        assert TestClient(app, client=(peer, 5000)).get(\"/api/cases\").status_code == 200, peer\n    for peer in (\"192.168.1.5\", \"10.0.0.2\", \"<redacted-private>\", \"0.0.0.0\", \"testclient\"):\n        r = TestClient(app, client=(peer, 5000)).get(\"/api/cases\")\n        assert r.status_code == 403 and r.json()[\"error\"][\"code\"] == \"forbidden\", peer\n        assert TestClient(app, client=(peer, 5000)).get(\"/api/health\").status_code == 403\n    monkeypatch.delenv(\"ZLAYT_MODE\")                                    # public build: no peer restriction\n    assert TestClient(app, client=(\"192.168.1.5\", 5000)).get(\"/api/health\").status_code == 200\nEOF\npython3 -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:32:31.241Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:32.375Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:32:50.055Z

**tool result**
````
E            +  where 500 = <Response [500 Internal Server Error]>.status_code
E            +    where <Response [500 Internal Server Error]> = get('/api/cases')
E            +      where get = <starlette.testclient.TestClient object at 0x10854bc20>.get
E            +        where <starlette.testclient.TestClient object at 0x10854bc20> = TestClient(<fastapi.applications.FastAPI object at 0x10854b680>, client=('127.0.0.1', 5000))

tests/unit/test_api_routes.py:345: AssertionError
------------------------------ Captured log call -------------------------------
ERROR    zlayt.api:api.py:181 unhandled AttributeError
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_audit_is_metadata_only_unless_local_mode
FAILED tests/unit/test_api_routes.py::test_case_list_and_library_exist_only_in_local_mode
FAILED tests/unit/test_api_routes.py::test_cases_do_not_leak_decisions_between_each_other
FAILED tests/unit/test_api_routes.py::test_library_texts_are_admitted_only_in_local_mode
FAILED tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address
5 failed, 891 passed in 16.90s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:52.761Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\ns=s.replace(\"    return (ip.ipv4_mapped or ip).is_loopback\",\"    return (getattr(ip, \\\"ipv4_mapped\\\", None) or ip).is_loopback\")\nopen(p,'w').write(s)\np='tests/unit/test_api_routes.py'\ns=open(p).read()\ns=s.replace(\"return db, TestClient(create_app(db, static_dir=str(tmp_path)))\",\"return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=(\\\"127.0.0.1\\\", 50000))   # real loopback peer: local mode checks it (D-036)\",1)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8; grep -rln \"ZLAYT_MODE\" tests | head"
}
````

### User / tool · 2026-11-02T02:33:11.009Z

**tool result**
````
........................................................................ [ 56%]
........................................................................ [ 64%]
........................................................................ [ 72%]
........................................................................ [ 80%]
........................................................................ [ 88%]
........................................................................ [ 96%]
................................                                         [100%]
896 passed in 17.47s
tests/unit/test_api_routes.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:13.093Z

**tool call — Bash**
````
{
 "command": "git add app/backend/api.py tests/unit/test_api_routes.py && git commit -q -m \"fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && SHA=$(git rev-parse --short HEAD) && echo $SHA\nB=\"python3 tools/board.py\"; $B show T-053 | grep -n \"\\[.\\]\" | head -12"
}
````

### User / tool · 2026-11-02T02:33:13.161Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git add app/backend/api.py tests/unit/test_api_routes.py && git commit -q -m "fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)

Co-Authored-By: Claude Opus 5.5 <noreply
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:14.242Z

**tool call — Bash**
````
{
 "command": "git add app/backend/api.py tests/unit/test_api_routes.py"
}
````

### User / tool · 2026-11-02T02:33:14.338Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:14.614Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-053 | grep -n \"^- \\[\" | head -12"
}
````

### User / tool · 2026-11-02T02:33:14.742Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:16.209Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"; git rev-parse --short HEAD; python3 tools/board.py show T-053 | grep -in \"acceptance\\|\\[ \\]\\|\\[x\\]\" | head"
}
````

### User / tool · 2026-11-02T02:33:16.547Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
08764e7
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:17.643Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-053 | head -40"
}
````

### User / tool · 2026-11-02T02:33:17.771Z

**tool result**
````
---
id: "T-053"
title: "Multi-case: case list + switcher (local/dev mode only), library loader"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: ["T-040", "T-041"]
created_by: "orchestrator"
created_at: "2026-11-02T02:06:39Z"
updated_at: "2026-11-02T02:32:08Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:32:08Z"
rounds: 2
commits: ["2c2eb1f", "996f9b4", "02f9939"]
reviews:
  - {"persona": "security-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-053-security.md", "at": "2026-11-02T02:21:00Z"}
  - {"persona": "security-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-053-security-r2.md", "at": "2026-11-02T02:31:45Z"}
ac:
  - {"n": 1, "text": "GET /api/cases lists cases only in local mode; 404 in demo/public mode (test)", "done": true, "evidence": "test_api_routes::test_case_list_and_library_exist_only_in_local_mode (404 in demo, list+library+library load in local)"}
  - {"n": 2, "text": "UI case switcher in local mode; library cases loadable in one click; cases isolated (T-050)", "done": true, "evidence": "Playwright vs local-mode server (ZLAYT_MODE=local, port 7871): switcher hidden on demo server (GET /api/cases 404), shown in local mode; library case loads and runs with one keyboard Enter; list opens cases; accepted flag in case 1 not present in case 2 and restored on switching back; 375 px no horizontal scroll; no console errors. Note: fixture backend has no recordings for library texts so their entries land in the could-not-verify tray (flags and amounts still show)"}
  - {"n": 3, "text": "E2E: two cases reviewed side by side, decisions do not leak between cases", "done": true, "evidence": "moved to T-045 AC (two library cases side by side, no leakage E2E); API-level isolation test in tests/unit/test_api_routes.py"}
---
## Description
D-031 + D-008: case list exists only when ZLAYT_MODE=local; public demo stays token-only. Loader seeds evals/library cases.

## Notes (append-only, newest last)
- 2026-11-02T02:11:17Z orchestrator: assigned: backend-3
- 2026-11-02T02:11:36Z backend: claimed
- 2026-11-02T02:12:32Z backend: AC 1 checked: test_api_routes::test_case_list_and_library_exist_only_in_local_mode (404 in demo, list+library+library load in local)
- 2026-11-02T02:12:33Z backend: API done: GET /api/cases, GET /api/library, POST /api/cases {library:id} (all ZLAYT_MODE=local only; 404 otherwise); library loader reads evals/library/*.txt (+ .expected.json name/description), falls back to evals/golden until T-052 lands. In local mode library texts pass the demo gate. AC2 (UI switcher) is frontend: needs a card; AC3 browser E2E is qa. api.md updated (audit both shapes + these routes). NB: another agent is editing api.py concurrently (PDF upload make_case); I merged around it.
- 2026-11-02T02:12:39Z backend: moved in_progress -> in_review: AC2 UI switcher is frontend, AC3 browser E2E is qa; API halves checked
- 2026-11-02T02:12:46Z orchestrator: review dispatched: security (haiku)
- 2026-11-02T02:14:58Z frontend: AC 2 checked: Playwright vs local-mode server (ZLAYT_MODE=local, port 7871): switcher hidden on demo server (GET /api/cases 404), shown in local mode; library case loads and runs with one keyboard Enter; list opens cases; accepted flag in case 1 not present in case 2 and restored on switching back; 375 px no horizontal scroll; no console errors. Note: fixture backend has no recordings for library texts so their entries land in the could-not-verify tray (flags and amounts still show)
- 2026-11-02T02:14:58Z frontend: AC2 UI done: app/frontend/switcher.js (+ .cs-* styles in review.css, script tag in index.html). Local mode detected by GET /api/cases 200 vs 404; lists cases and /api/library; one click POST /cases {library:id} then run. textContent only, buttons keyboard reachable. AC3 (two cases side by side E2E) still qa.
- 2026-11-02T02:15:28Z orchestrator: AC 3 checked: moved to T-045 AC (two library cases side by side, no leakage E2E); API-level isolation test in tests/unit/test_api_routes.py
- 2026-11-02T02:15:28Z orchestrator: Follow-up after T-052 review: record claude-cli fixtures for evals/library packets (python -m app.llm.record) so library cases verify in fixture mode.
- 2026-11-02T02:21:00Z orchestrator: review security-reviewer (claude-haiku-5-5): fail — reviews/T-053-security.md; round 1; findings:
    - [blocker] Demo mode sends live Anthropic SDK calls when LLM_BACKEND=anthropic-api and a key is set, with ENABLE_LIVE unset (pre-existing gate hole; T-053 library route reaches it too) — fix: In app/llm/provider.py complete_with_meta, refuse claude-cli and anthropic-api unless ENABLE_LIVE=1 and the key (or claude CLI) is present, raising LLMError('BACKEND_UNAVAILABLE live not enabled') before
    - [major] Local demo mode now admits seven unrecorded library texts through the demo gate; this conflicts with D-020/R-CO-4 wording and needs a ruling — fix: Chris rules on whether D-031 amends D-020 for local mode. If yes, amend D-020 in writing and require that library texts run only on recorded fixtures and never on a live backend (finding 1). If no, admit only texts whose hash is in app.st
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:22.075Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-053 --check 1 --agent backend --evidence \"tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address: 403 for 192.168.1.5/10.x/<redacted-private>x/0.0.0.0, 200 for 127.x, ::1, ::ffff:127.0.0.1; unit suite 896 passed\" ; $B note T-053 --agent backend --text \"Round 3 fix for security r2 F1 (D-036): app/backend/api.py middleware returns 403 {error.code=forbidden} when ZLAYT_MODE=local and request.client.host is not loopback; HOST startup check kept. Test env fixture now uses a loopback client. Commit 08764e7. Unit suite: 896 passed. F2 resolved by D-036 (no change).\"; $B commit T-053 --sha 08764e7 --agent backend; $B handoff T-053 --agent backend --text \"What changed: local mode now gates by peer address (api.py middleware + is_loopback_peer), 403 JSON for non-loopback, works behind tailscale serve (loopback peer). How verified: tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address; python -m pytest tests/unit 896 passed. Left: nothing for F1; F2 closed by D-036. Surprised: TestClient default peer is 'testclient', so local-mode tests needed an explicit loopback client.\"; $B move T-053 in_review --agent backend; tools/serve_app.sh"
}
````

### User / tool · 2026-11-02T02:33:24.495Z

**tool result**
````
AC 1 checked: tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address: 403 for 192.168.1.5/10.x/<redacted-private>x/0.0.0.0, 200 for 127.x, ::1, ::ffff:127.0.0.1; unit suite 896 passed
noted on T-053
T-053: commit 08764e7 recorded
handoff written on T-053
T-053: in_progress -> in_review
app http 200 on :7860
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:27.031Z

T-053 round 3 is fixed and moved to `in_review`. With `ZLAYT_MODE=local`, a middleware in `app/backend/api.py` now returns 403 `{error.code: forbidden}` for any non-loopback `request.client.host`, whatever address uvicorn bound to. The `HOST` startup check stays, and loopback peers (including `::ffff:127.0.0.1`) still get 200.

The new test `test_local_mode_refuses_non_loopback_peer_by_address` passes with the rest of the unit suite (896 passed). The shared `env` test fixture in `tests/unit/test_api_routes.py` now uses a loopback client, because TestClient's default peer is `"testclient"` and the middleware would otherwise 403 it.

The AC is checked and the commit is `08764e7`, which is recorded on the card with the handoff note. The app was restarted with `tools/serve_app.sh` and answers 200 on :7860.
