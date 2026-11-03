# Subagent: Release: T-182 Docker + README (Release: T-182 Docker + README)

Source: `agent-a30e35d65cc445095.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:00:21.710Z

You are the release worker in /Users/arsis/zlayt-pm-project. Claim T-182 (P0, M4) with `python3 tools/board.py claim T-182 --agent release`. Read the M4 section of docs/CONTRACT.md, CLAUDE.md and docs/RUNBOOK.md.

Build:
1. **Dockerfile** on port 7860. It serves the app in demo mode with no key, from the committed fixtures. The image must contain no secrets.
2. **Verify** with `docker build` and `docker run`. If Docker isn't available on this host, say so and verify the same run command without Docker.
3. **Hosting instructions.** Write Hugging Face Spaces instructions (Docker SDK, app_port 7860, secrets via Space settings) and Replit instructions. Check the current HF docs with a web fetch, and cite them.
4. **README.md:** what this is, run-from-clone in under 5 minutes, demo vs live mode, and where the evals and the submission live.
5. **.env.example**, plus a Makefile or run.sh.

Time the README path yourself from a fresh `git clone` into your scratchpad, and record the time.

Rules:
- Never print .env, and never put a key anywhere.
- Commit with a pathspec.
- Write the handoff and move the card to in_review.
- Stop only your own PIDs; never touch ports 7860, 8787 or 4173.

Reply in 3 lines.

### User / tool · 2026-11-02T21:00:21.715Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:24.829Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-182 --agent release; python3 tools/board.py show T-182; grep -n -i \"M4\" docs/CONTRACT.md | head -30; ls; cat docs/RUNBOOK.md | head -60; which docker"
}
````

### User / tool · 2026-11-02T21:00:25.043Z

**tool result**
````
T-182 claimed by release
---
id: "T-182"
title: "M4 release: Dockerfile (port 7860) with docker run verified; Hugging Face Spaces (Docker SDK, app_port 7860, secrets via Space settings) and Replit instructions (check current HF docs); README.md timed run-from-clone (<5 min); .env.example; Makefile/run.sh"
milestone: "M4"
role: "release"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:00:24Z"
claimed_by: "release"
claimed_at: "2026-11-02T21:00:24Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "docker build + docker run serve the guided UI at :7860 in demo mode with no key; README path timed from a clean clone under 5 minutes; HF/Replit instructions cite current docs; no secrets in image or repo", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: release
- 2026-11-02T21:00:24Z release: claimed

## Handoff (filled when moving to in_review)

312:### M4 — Hardening, deployment, demo assets (≤ 2 h)
316:Gate panel: security, privacy-compliance, installer-reviewer (clones into a clean temp directory and times the README path; must be under 5 minutes), qa, release self-check against the HF/Replit requirements. Exit: tag `m4`.
415:- `tools/install_test.sh` — clean-clone timed run (installer-reviewer runs it; qa runs it at M4 and M5).
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
# RUNBOOK (for Chris)

## URLs
| What | URL | Notes |
|---|---|---|
| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |

Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
We restored those and gave the board and app their own ports so nothing of yours was clobbered.

## Steer
- **Inbox:** Board → Inbox → type a note → Send. It lands in `board/inbox/` and the orchestrator acts on it next cycle.
- **Direct:** type into this Claude session (Remote Control / Desktop). Treated exactly like an inbox note.
- **Your items:** `submission/NEEDS_CHRIS.md` and the `needs_chris` column. Nothing there blocks the team.

## Stop
- Board → Inbox → **STOP** (type STOP to confirm) → creates `board/STOP`. The orchestrator finishes its current handoff and stops.
- Or on the Mac: `touch ~/zlayt-pm-project/board/STOP`.
- **Resume after STOP:** from the phone, type into this Claude session (Remote Control): "Delete board/STOP and continue the loop." On the Mac: `rm ~/zlayt-pm-project/board/STOP`, then continue the session.

## Restart (after a crash, reboot, or closing the session)
1. `cd ~/zlayt-pm-project`
2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
3. Session — either:
   - Desktop app: reopen this session from the sidebar (it keeps bypass-permissions mode), or
   - Terminal: `claude --continue --dangerously-skip-permissions --remote-control` (without the first flag the run stalls on permission prompts nobody answers; the second lets you steer and resume from your phone).
4. Say:
   > Re-read CLAUDE.md, memory/STATE.md and `python3 tools/board.py status`. Re-spawn the worker agents (general-purpose subagents whose first step is `python3 tools/agent_prompt.py <role>` unless native agent types are available), recreate the heartbeat cron (text in memory/STATE.md), continue the loop.
5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.

## Useful commands
```
python3 tools/board.py status          # where are we
python3 tools/board.py list --status in_review
tail -f board/activity.jsonl           # raw event log
.venv/bin/python -m pytest tools/tests -q   # harness tests
```
/opt/homebrew/bin/docker
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:25.404Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/release/MEMORY.md"
}
````

### User / tool · 2026-11-02T21:00:25.410Z

**tool result (error)**
````
File does not exist. Note: your current working directory is /Users/arsis/zlayt-pm-project.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:28.262Z

**tool call — Bash**
````
{
 "command": "sed -n 305,320p docs/CONTRACT.md; ls app app/* deploy tools | head -80; cat requirements.txt; cat tools/serve_app.sh; cat app/config.py 2>/dev/null | head -50; git status --short | head; git log --oneline | head -5; docker info 2>&1 | head -5; ls data"
}
````

### User / tool · 2026-11-02T21:00:28.533Z

**tool result**
````
### M3 — Review UI, export, E2E (≤ 3.5 h)

Cards (frontend, backend, qa): paste/upload input; timeline view with date, provider, summary, exact excerpt, confidence state, and "Why?"; flags panel grouped by type with evidence; charges table with running total and the "unclear" tray; accept / edit / dismiss per entry and per flag with keyboard-friendly review flow; export (copy-ready demand-letter treatment section containing only accepted items, with source citations in a format a paralegal would use); the chosen stretch item if still inside budget; mobile-usable; Playwright E2E for the full paralegal journey (paste sample → review → export equals accepted set).

Gate panel: ux-designer (drives the app via Playwright and screenshots every state), paralegal (completes the full job on the sample case as a user and reports where she distrusted the tool), accessibility, staff-engineer, chaos-tester (adversarial inputs: empty, huge, non-English, injection record, pasted PDF text with page headers), product-manager. Exit: E2E green, gate passed, tag `m3`.

### M4 — Hardening, deployment, demo assets (≤ 2 h)

Cards (release, qa, backend, security): Dockerfile (port 7860) + `docker run` verified locally; Hugging Face Spaces (Docker SDK, `app_port: 7860`, secrets via Space settings) and Replit run instructions — verify the current HF docs before writing; `README.md` with a *timed* run-from-clone path; `.env.example`; server-side API key with per-session rate limit and spend cap, **demo mode** that serves cached results for the sample case when no key is configured (so the public link works without Chris's key being abused), optional bring-your-own-key; input size limits; error states; a visible "synthetic data only — never paste real records" banner; annotated screenshots of every state (`artifacts/screenshots/`, with captions in `artifacts/CAPTIONS.md`); a ≤ 3-minute Playwright-recorded walkthrough video (`artifacts/demo.webm`, plus a narration script Chris can read over it).

Gate panel: security, privacy-compliance, installer-reviewer (clones into a clean temp directory and times the README path; must be under 5 minutes), qa, release self-check against the HF/Replit requirements. Exit: tag `m4`.

### M5 — Submission package (≤ 2 h)

Cards (writer, qa, orchestrator):
app/README-arch.md
app/__init__.py
app/main.py
app/pipeline.py

app:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

app/__pycache__:
__init__.cpython-312.pyc
main.cpython-312.pyc
pipeline.cpython-312.pyc

app/backend:
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
count_charge.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
money.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
spanish.py
spanish_text.py
speaker.py
split_llm.py
store.py
summary_trim.py
totals.py
trace.py
uncovered.py
why.py

app/db:
# Runtime dependencies, exact versions from the working .venv (pip freeze minus test tools). Python 3.12.
# Test/dev tools are in requirements-dev.txt. Release adopts these pins; re-run pip-audit when they change.
annotated-doc==0.0.5
annotated-types==0.8.0
anthropic==2.3.0
anyio==4.16.0
certifi==2026.10.23
click==8.5.0
docstring_parser==0.18.0
fastapi==0.162.0
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.0
httptools==0.9.0
httpx==0.28.1
httpx2==2.16.0
idna==3.20
jiter==0.18.0
opentelemetry-api==1.45.2
packaging==26.3
pydantic==2.14.2
pydantic_core==2.50.2
pypdf==6.21.4
pypdfium2==5.14.0
python-dotenv==1.2.4
python-multipart==0.0.33
PyYAML==6.0.3
sniffio==1.3.1
starlette==1.10.0
truststore==0.10.5
typing-inspection==0.4.4
typing_extensions==4.16.0
uvicorn==0.54.0
uvloop==0.23.0
watchfiles==1.3.0
websockets==17.4
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
b824a6c fix(evals): T-045 r3: --record-latest refuses non-live backends and recomputes the ship bar from the report body and per-run directory; records sha256 and source commit
a56f189 fix(backend): T-178 GATE-M3 chaos: interrupted runs recovered at startup, stale-tab 409 stale_item, invisible characters stripped and lone surrogates replaced (no 500)
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
Client: Docker Engine - Community
 Version:    29.9.2
 Context:    default
 Debug Mode: false

zlayt.sqlite
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:30.540Z

**tool call — Bash**
````
{
 "command": "cat app/main.py; ls deploy app/llm app/frontend evals data | head -80; grep -rn \"os.environ\\|getenv\" app --include=*.py | grep -v __pycache__ | head -50; cat .gitignore; ls .dockerignore 2>&1; python3 --version; ls -a | head -30"
}
````

### User / tool · 2026-11-02T21:00:30.658Z

**tool result**
````
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/frontend:
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
guided
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
overview.css
overview.js
review.css
review.js
sections.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
suggestions.js
switcher.js
timeline.js
tokens.css
uncovered.css
uncovered.js

app/llm:
__init__.py
__pycache__
_types.py
audited.py
backends
lexicon.yaml
promptlib.py
prompts
provider.py
record.py

data:
zlayt.sqlite

deploy:

evals:
__init__.py
__pycache__
adversarial
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py
app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
app/llm/provider.py:28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
app/llm/provider.py:89:    return os.environ.get("RECORD_FIXTURES") == "1" or os.environ.get("LLM_FIXTURE_RECORD") == "1"
app/llm/audited.py:148:    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
app/llm/backends/fixture.py:14:    if os.environ.get("LLM_FIXTURE_DIR"):
app/llm/backends/fixture.py:15:        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
app/llm/backends/fixture.py:23:    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
app/llm/backends/anthropic_api.py:15:    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"), max_retries=0, timeout=TIMEOUT_S)
app/llm/backends/anthropic_api.py:20:        if not os.environ.get("ANTHROPIC_API_KEY"):
app/llm/backends/claude_cli.py:27:    return {k: os.environ[k] for k in ENV_ALLOW if k in os.environ}
app/llm/backends/claude_cli.py:37:    return [os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude", "-p", "--model", model,
app/backend/store.py:71:    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
app/backend/pdf_ocr.py:42:    return {**{k: os.environ[k] for k in _ENV_KEEP if k in os.environ}, "OMP_THREAD_LIMIT": "1"}
app/backend/api.py:82:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:96:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
app/backend/api.py:111:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/backend/api.py:113:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:136:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/api.py:439:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:465:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:665:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/backend/judges.py:17:    return os.environ.get("GENERATOR_MODEL") or DEFAULT_GENERATOR_MODEL
app/backend/judges.py:21:    return os.environ.get("JUDGE_MODEL") or DEFAULT_JUDGE_MODEL
app/backend/pipeline.py:693:        self.old = os.environ.get("LLM_BACKEND")
app/backend/pipeline.py:695:            os.environ["LLM_BACKEND"] = self.name
app/backend/pipeline.py:700:            os.environ.pop("LLM_BACKEND", None)
app/backend/pipeline.py:702:            os.environ["LLM_BACKEND"] = self.old
app/backend/pdf_hidden.py:556:        env = {k: os.environ[k] for k in _CHILD_ENV_KEEP if k in os.environ}
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
.pytest_cache/
node_modules/
.claude/agent-memory-local/
.claude/settings.local.json
artifacts/tmp/
board/.locks/
board/.stop_guard_state
board/.hook_debug.log
board/.server.log
app/db/*.sqlite3
*.sqlite3
.DS_Store
board/.hook_input_keys.log
board/.state.json
*.pem
*.key
id_rsa*
.envrc
*.env
.ruff_cache/
.coverage
*.log
.claude/scheduled_tasks.lock
ls: .dockerignore: No such file or directory
Python 3.12.2
.
..
.claude
.env
.git
.gitignore
.pytest_cache
.scratch
.venv
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:32.812Z

**tool call — Bash**
````
{
 "command": "sed -n 60,160p app/backend/api.py; sed -n 15,100p app/llm/provider.py; cat app/llm/backends/fixture.py | head -50; grep -n \"def demo_mode\" -A8 app/backend/*.py; ls app/llm/backends; git check-ignore data/zlayt.sqlite; git ls-files data app/llm | head -30"
}
````

### User / tool · 2026-11-02T21:00:32.952Z

**tool result**
````
def recorded_hashes() -> set:
    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}


def library_cases() -> list:
    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
    evals/golden until the library exists. [{id, name, description, path}]"""
    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
    out = []
    for p in sorted(base.glob("*.txt")):
        meta = {}
        ej = p.with_name(p.stem + ".expected.json")
        if ej.exists():
            try:
                meta = json.loads(ej.read_text())
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    _boot = DB.connect(db_path)
    try:
        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
    finally:
        _boot.close()
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
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def answers():
        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
        if live_enabled():
            return "live"
        from app.llm.backends import fixture
        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"

    def config_models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def models():
        """The models /health shows. T-177 r2: on the prepared (curated) set no model drafts an answer, so none is named as the drafter. Per-case payloads use present.models_for (from the case's own calls)."""
        base = config_models()
        prepared = answers() == "prepared"
        return dict(base, generator=present.PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)

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

    def get_case(c, token):
        case = DB.get_case(c, token)
from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
from app.llm.backends import fixture as _fixture

GOLDEN_DIR = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"
LIBRARY_DIR = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"    # committed SYNTHETIC packets (D-031, T-052)
_record_ok = False


def backend_name() -> str:
    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
        return "fixture"
    return name


def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


MIN_FRAGMENT = 20


def assert_recordable(text: str, *, whole_file: bool = False) -> None:
    """ValueError unless `text` (whitespace-normalised) is a golden file's full text (whole_file) or a fragment of at least
    MIN_FRAGMENT characters inside one. No other text may be recorded."""
    t = _norm(text or "")
    if len(t) >= (1 if whole_file else MIN_FRAGMENT):
        for p in sorted(GOLDEN_DIR.glob("*.txt")) + sorted(LIBRARY_DIR.glob("*.txt")):
            g = _norm(p.read_text())
            if t == g or (not whole_file and t in g):
                return
        if not whole_file:       # synthetic seeded-hallucination lines (their record_text) are golden input too
            import json as _json
            for p in sorted(GOLDEN_DIR.glob("hallucinations*.jsonl")):
                for line in p.read_text().splitlines():
                    if line.strip() and t in _norm(_json.loads(line).get("record_text", "")):
                        return
    raise ValueError("text is not an evals/golden input; refusing to record")


@contextlib.contextmanager
def record_context(source_text: str):
    """Used by record.py only: allow record-mode writes while the pipeline runs over a COMPLETE golden input."""
    global _record_ok
    assert_recordable(source_text, whole_file=True)
    prev, _record_ok = _record_ok, True
    try:
        yield
    finally:
        _record_ok = prev


@contextlib.contextmanager
def record_fragment_context(fragment: str):
    """Judge-line recording: allow record-mode writes for a judge call whose record text is a fragment (>= MIN_FRAGMENT chars) of a golden file."""
    global _record_ok
    assert_recordable(fragment)
    prev, _record_ok = _record_ok, True
    try:
        yield
    finally:
        _record_ok = prev


def _recording() -> bool:
    return os.environ.get("RECORD_FIXTURES") == "1" or os.environ.get("LLM_FIXTURE_RECORD") == "1"


def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
    name = backend_name()
    key = prompt_hash(model, system, user, json_schema)
    if name == "fixture":
        res = _fixture.call(model, system, user, json_schema, key=key)
    elif name in ("claude-cli", "anthropic-api"):
        if _recording() and not _record_ok:
            raise ValueError("record mode needs record_context() over text from evals/golden")
        if name == "claude-cli":
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p


def answer_source() -> str:
    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
    return "prepared" if fixture_dir().name == "curated" else "recorded"
app/backend/api.py:125:    def demo_mode():
app/backend/api.py-126-        return not live_enabled()
app/backend/api.py-127-
app/backend/api.py-128-    def answers():
app/backend/api.py-129-        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
app/backend/api.py-130-        if live_enabled():
app/backend/api.py-131-            return "live"
app/backend/api.py-132-        from app.llm.backends import fixture
app/backend/api.py-133-        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
__init__.py
__pycache__
anthropic_api.py
claude_cli.py
fixture.py
app/llm/__init__.py
app/llm/_types.py
app/llm/audited.py
app/llm/backends/__init__.py
app/llm/backends/anthropic_api.py
app/llm/backends/claude_cli.py
app/llm/backends/fixture.py
app/llm/lexicon.yaml
app/llm/promptlib.py
app/llm/prompts/extract_es_v1.md
app/llm/prompts/extract_v1.md
app/llm/prompts/flags_v1.md
app/llm/prompts/judge_amount_class_v1.md
app/llm/prompts/judge_conflict_v1.md
app/llm/prompts/judge_conflict_v2.md
app/llm/prompts/judge_conflict_v4.md
app/llm/prompts/judge_conflict_v5.md
app/llm/prompts/judge_conflict_v6.md
app/llm/prompts/judge_faithfulness_es_v1.md
app/llm/prompts/judge_faithfulness_v1.md
app/llm/prompts/judge_flag_v1.md
app/llm/prompts/judge_flag_v2.md
app/llm/prompts/judge_flag_v3.md
app/llm/prompts/narrative_v1.md
app/llm/prompts/split_v1.md
app/llm/provider.py
app/llm/record.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:36.470Z

**tool call — Bash**
````
{
 "command": "ls tests/fixtures/llm | head -5; ls tests/fixtures/llm | wc -l; ls tests/fixtures/llm/curated | wc -l; du -sh tests/fixtures/llm evals/golden evals/library app/frontend; git ls-files tests/fixtures/llm | wc -l; git ls-files evals/library | wc -l; sed -n 60,90p app/backend/store.py; grep -n \"^ROOT\\|^GOLDEN\\|^LIBRARY\\|FRONTEND\\|frontend\" app/backend/api.py | head; grep -rn \"ZLAYT_DEMO\\|RATE\\|rate_limit\\|SPEND\" app/backend/api.py | head; cat requirements-dev.txt | head; grep -rn \"tesseract\\|ocrmypdf\\|pdftoppm\\|subprocess\" app/backend/pdf_ocr.py | head -8; cat tools/install_test.sh 2>&1 | head -5; cat Makefile 2>&1|head -3"
}
````

### User / tool · 2026-11-02T21:00:36.659Z

**tool result**
````
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
00e8d38a3d50d7d1d7a9b7431c6c2c1970b32930a2583c8a3acd58fdced43d2f.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
    1211
      19
4.9M	tests/fixtures/llm
348K	evals/golden
344K	evals/library
656K	app/frontend
    1213
      30
    now = time.time() if now is None else now
    if case and case["status"] == "running" and not is_live_run(case["id"]) and case.get("run_started_at") and now - case["run_started_at"] > RUN_STALE_AFTER_S:
        if interrupt_run(conn, case["id"], now):
            return DB.get_case(conn, case["id"])
    return case


def live_enabled() -> bool:
    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
    Read per call so a test can change the environment."""
    from app.llm import provider
    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))


def live_model_available() -> bool:
    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
    from app.llm import provider
    return provider.backend_name() != "fixture" and live_enabled()


def iso(t) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_records(conn, case_id: str, raw: str = None) -> list:
    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
    if raw is None:
        raw = DB.get_case(conn, case_id)["raw_text"]
    out = []
    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
28:# index.html has one inline onclick (dialog Close); allowed by hash until the frontend moves it to a listener.
31:ROOT = pathlib.Path(__file__).resolve().parents[2]
32:GOLDEN = ROOT / "evals" / "golden"
33:LIBRARY = ROOT / "evals" / "library"
669:    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
676:            app.mount("/", StaticFiles(directory=str(guided), html=True), name="frontend")
678:            app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
-r requirements.txt
# test and browser-check tools (not shipped in the image)
greenlet==3.5.6
iniconfig==2.3.1
playwright==1.64.1
pluggy==1.7.0
pyee==14.0.0
Pygments==2.21.0
pytest==9.2.0
app/backend/pdf_ocr.py:1:"""Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text
app/backend/pdf_ocr.py:17:import subprocess
app/backend/pdf_ocr.py:35:INSTALL_HINT = "Install Tesseract: macOS `brew install tesseract`; Debian/Ubuntu `sudo apt-get install tesseract-ocr`."
app/backend/pdf_ocr.py:41:    """The environment tesseract runs with: an allow-list taken from the server's at call time, plus one thread (T-086 round 2)."""
app/backend/pdf_ocr.py:59:    return shutil.which("tesseract") or ""
app/backend/pdf_ocr.py:69:        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_env())
app/backend/pdf_ocr.py:73:        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_env())
app/backend/pdf_ocr.py:75:    except (OSError, subprocess.SubprocessError):
cat: tools/install_test.sh: No such file or directory
cat: Makefile: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:44.887Z

**tool call — ToolSearch**
````
{
 "query": "select:WebFetch",
 "max_results": 1
}
````

### User / tool · 2026-11-02T21:00:44.892Z

**tool result**
````
[tool_reference]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:53.696Z

**tool call — WebFetch**
````
{
 "url": "https://huggingface.co/docs/hub/spaces-sdks-docker",
 "prompt": "Extract exact requirements for Docker Spaces: README.md YAML front matter (sdk, app_port), port default, user/permissions (uid 1000), secrets and variables handling (build-time vs runtime), persistent storage, any caveats. Quote key lines."
}
````

### User / tool · 2026-11-02T21:00:53.962Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:54.447Z

**tool call — WebFetch**
````
{
 "url": "https://huggingface.co/docs/hub/spaces-config-reference",
 "prompt": "List the Space README YAML front matter fields: title, emoji, colorFrom, colorTo, sdk, app_port, short_description, pinned, etc. Quote exact wording for sdk docker and app_port."
}
````

### User / tool · 2026-11-02T21:00:54.518Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:00:55.353Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/replit-workspace/configuring-repl",
 "prompt": "Explain the .replit file: run command, modules, [[ports]] localPort/externalPort, deployment section, and nix config for python. Quote exact snippets."
}
````

### User / tool · 2026-11-02T21:01:02.850Z

**tool result**
````
## `.replit` file overview

The `.replit` file uses TOML and controls how your Replit App behaves. Its default Python version includes:

```toml
entrypoint = "main.py"
modules = ["python-3.10:v18-20230807-322e88b"]
```

## Run command

The `run` key sets what happens when you press Run. The page describes it as "Specify the command that executes when the Run button is selected." It accepts a string or an array:

- `run = "python -m app & npm run start & wait"` runs multiple processes at once.
- `run = ["echo", "Hello, Replit!"]` passes each argument explicitly.

For more complex apps, the page recommends Workflows instead.

## Modules

`modules` pins language versions and other major dependencies. The page says it "Defines specific versions of programming languages or other major dependencies supported by Replit." The Python default is `["python-3.10:v18-20230807-322e88b"]`.

## Ports: `[[ports]]`, `localPort`, `externalPort`

The double brackets define an array of port mappings:

```toml
[[ports]]
localPort = 3000
externalPort = 80
```

- `localPort` is described as the "Port that Replit binds to an external port."
- `externalPort` is the "Publicly accessible port linked to the `localPort`."

## Deployment section

The `[deployment]` table configures the live environment. The Python default is:

```toml
[deployment]
run = ["python3", "main.py"]
deploymentTarget = "cloudrun"
```

- `run` is the "Command executed to start the application during deployment."
- `deploymentTarget` specifies the platform hosting the app. The default is `cloudrun`.

The page also lists `build`, which runs before a deployment starts, and `ignorePorts`, which skips the open-port check when set to `true`.

## Nix config for Python

The default Python file includes:

```toml
[nix]
channel = "stable-23_05"
```

The `channel` key sets the Nix channel, which "affects the versions of system dependencies available." The `packages` key can install Nix packages directly, and the page notes that `replit.nix` offers "more fine-grained control."

The page's `replit.nix` example uses Node.js packages, not Python. To add Python-related packages, list them in the `deps` array with the `pkgs.` prefix. The page doesn't include a Python-specific example.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:07.984Z

**tool call — Bash**
````
{
 "command": "grep -rhn \"^from evals\\|^import evals\\|from tools\\|ROOT / \\\"[a-z]*\\\"\" app --include=*.py | sort | uniq | head -20; grep -rn \"parents\\[\" app --include=*.py | grep -v \"parents\\[[23]\\] / \\\"\\(evals\\|tests\\)\" | head; grep -n \"healthz\\|\\\"/health\\|/api/health\" app/backend/api.py | head -3; git ls-files evals/golden | head -3; git ls-files | grep -c \"^tests/fixtures/llm/curated\""
}
````

### User / tool · 2026-11-02T21:01:08.126Z

**tool result**
````
26:REPORT = ROOT / "evals" / "reports" / "calibration.json"
32:GOLDEN = ROOT / "evals" / "golden"
33:LIBRARY = ROOT / "evals" / "library"
669:    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
96:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
app/backend/calibration_route.py:25:ROOT = pathlib.Path(__file__).resolve().parents[2]
app/backend/api.py:31:ROOT = pathlib.Path(__file__).resolve().parents[2]
app/backend/lexicon.py:8:LEXICON_PATH = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"
app/backend/grounding.py:12:_LEXICON = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"
261:    @app.get("/api/health")
322:        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
evals/golden/README.md
evals/golden/case_01_date_formats.expected.json
evals/golden/case_01_date_formats.txt
19
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:09.743Z

**tool call — Bash**
````
{
 "command": "ls evals/reports | head -20; du -sh evals/reports; sed -n 20,40p app/backend/calibration_route.py; curl -s localhost:7860/api/health | head -c 600"
}
````

### User / tool · 2026-11-02T21:01:09.875Z

**tool result**
````
20261102T020824Z.md
20261102T020933Z.md
20261102T021029Z.md
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T023155Z.md
20261102T023203Z.md
20261102T023204Z.md
20261102T023208Z.md
20261102T023603Z.md
20261102T023911Z.md
20261102T023916Z.md
20261102T024348Z.md
20261102T024355Z.md
20261102T024653Z.md
20261102T024822Z.md
20261102T025055Z.md
20261102T025219Z.md
4.0M	evals/reports
import hashlib
import json
import logging
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "evals" / "reports" / "calibration.json"
SCHEMA = "evals.calibration/1"
TYPES = ("entry", "amount", "flag")
STATES = ("verified", "needs_review")
SMALL_N = 30  # evals/run.py CAL_SMALL_N: fewer cases, or items in a state, than this is a small sample
SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
PROMPT_DIR = "app/llm/prompts"  # the same inputs evals/run.py hashes(): every prompt *.md and the lexicon
LEXICON = "app/llm/lexicon.yaml"
MISSING = "No calibration has been measured yet, so no accuracy line is shown."
INVALID = "The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run."
UNCHECKED = "The current prompts could not be read, so these numbers cannot be checked against them."
log = logging.getLogger("zlayt.calibration")


def _count(x) -> bool:
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:27.947Z

**tool call — Bash**
````
{
 "command": "cat > app/config.py <<'EOF'\n\"\"\"Runtime configuration, read-only. One place that says which mode the process is in and why; never returns or prints a secret.\n\n`python -m app.config` prints the resolved settings (a key is reported only as set / not set). The Dockerfile, run.sh and the Makefile\nuse it as a startup self-check. The rules themselves live where they are enforced (app.llm.provider.backend_name, app.backend.store.live_enabled);\nthis module calls those so there is one definition of \"live\".\n\"\"\"\nimport json\nimport os\n\nDEFAULTS = {\"HOST\": \"127.0.0.1\", \"PORT\": \"7860\", \"LLM_BACKEND\": \"fixture\", \"FIXTURE_SET\": \"curated\"}\n\n\ndef resolved() -> dict:\n    from app.backend import store\n    from app.llm import provider\n    live = store.live_enabled()\n    key_set = bool(os.environ.get(\"ANTHROPIC_API_KEY\"))\n    backend = provider.backend_name()\n    warnings = []\n    if os.environ.get(\"ENABLE_LIVE\") == \"1\" and not live:\n        warnings.append(\"ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.\")\n    if os.environ.get(\"LLM_BACKEND\") not in (None, \"\", \"fixture\") and os.environ.get(\"ENABLE_LIVE\") != \"1\":\n        warnings.append(\"LLM_BACKEND is set but ENABLE_LIVE is not 1: the fixture backend is used (no model call is possible).\")\n    if live and backend == \"anthropic-api\" and os.environ.get(\"PROVIDER_CAP_CONFIRMED\") != \"1\":\n        warnings.append(\"Live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a spend limit at the provider first); the server will refuse to start.\")\n    return {\n        \"mode\": \"live\" if live else \"demo\",\n        \"backend\": backend,\n        \"fixture_set\": os.environ.get(\"FIXTURE_SET\", DEFAULTS[\"FIXTURE_SET\"]) if backend == \"fixture\" else None,\n        \"host\": os.environ.get(\"HOST\", DEFAULTS[\"HOST\"]),\n        \"port\": int(os.environ.get(\"PORT\", DEFAULTS[\"PORT\"])),\n        \"anthropic_api_key\": \"set\" if key_set else \"not set\",\n        \"local_mode\": os.environ.get(\"ZLAYT_MODE\") == \"local\",\n        \"warnings\": warnings,\n    }\n\n\nif __name__ == \"__main__\":\n    print(json.dumps(resolved(), indent=2))\nEOF\ncat > .dockerignore <<'EOF'\n# Allow-list build context: only what the demo image runs. No .env, no .git, no board, no memory, no reviews, no databases.\n*\n!requirements.txt\n!app/**\n!evals/golden/**\n!evals/library/**\n!evals/reports/calibration.json\n!tests/fixtures/llm/**\n**/__pycache__\n**/*.pyc\n**/*.sqlite\n**/*.sqlite3\n**/.env\n**/.env.*\nEOF\ncat > Dockerfile <<'EOF'\n# Zlayt treatment timeline: demo-mode image. Serves the guided UI on :7860 from committed fixtures. No key, no network, no secrets in the image.\n# Hugging Face Spaces (Docker SDK) runs the container as uid 1000 and expects app_port 7860: both are set here.\nFROM python:3.12-slim\n\n# uid 1000 = the user Hugging Face runs Docker Spaces as; harmless anywhere else.\nRUN useradd -m -u 1000 user\nUSER user\nENV HOME=/home/user PATH=/home/user/.local/bin:$PATH \\\n    PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1\nWORKDIR $HOME/app\n\nCOPY --chown=user requirements.txt .\nRUN pip install -r requirements.txt\n\n# Context is allow-listed by .dockerignore: app/, the synthetic eval inputs, the recorded + curated LLM fixtures, the calibration file.\nCOPY --chown=user app ./app\nCOPY --chown=user evals ./evals\nCOPY --chown=user tests/fixtures/llm ./tests/fixtures/llm\n\n# Demo mode: fixture backend replays the team-prepared (curated) answers; nothing can call a model. Live mode is opt-in at `docker run -e` time (see README).\nENV HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=/home/user/data\nRUN mkdir -p $DATA_DIR\nEXPOSE 7860\n\nHEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \\\n  CMD python -c \"import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:7860/api/health', timeout=4).status == 200 else 1)\"\n\nCMD [\"python\", \"-m\", \"app.main\"]\nEOF\n(time docker build -t zlayt-demo:test . ) 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T21:01:28.054Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:32.851Z

**tool call — Bash**
````
{
 "command": "docker context ls 2>&1; ls /Applications | grep -i -E \"docker|orbstack|colima|podman\"; which colima orbstack podman limactl 2>&1 | head; ls <home-path> <home-path> 2>&1 | head; docker buildx version 2>&1 | head -2"
}
````

### User / tool · 2026-11-02T21:01:32.981Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:44.424Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/cloud-services/deployments/about-deployments",
 "prompt": "Deployment types (Autoscale, Reserved VM, Static, Scheduled), the requirement to bind 0.0.0.0, port configuration, which ports are exposed publicly, and how Secrets are available in deployments. Quote key lines."
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:45.294Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/replit-workspace/workspace-features/secrets",
 "prompt": "How to add Secrets in a Replit app (Secrets tool), availability as environment variables, and whether they carry into deployments. Quote key lines."
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:45.987Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/updates/2025/09/05/changelog",
 "prompt": "Is there any mention of python version modules (python-3.12), or changes to .replit / replit.nix? If not, say so briefly."
}
````

### User / tool · 2026-11-02T21:01:47.601Z

**tool result**
````
No. The page doesn't mention Python 3.12, Python modules, `.replit`, or `replit.nix`. It does say General Agent works with "any codebase in any language or framework that runs on NixOS," but it doesn't describe any configuration file changes.
````

### User / tool · 2026-11-02T21:01:48.685Z

**tool result**
````
The page describes the four deployment types but doesn't cover the other topics you asked about.

**Deployment types**
- **Autoscale:** "Automatically adjusts resources based on your app's usage."
- **Static:** "Provides an affordable way to host websites that don't change based on user input."
- **Reserved VM:** "Provides a consistent amount of computing resources for your app to run continuously."
- **Scheduled:** "Runs your app at scheduled times that you choose."

**Not covered in this content**
- **Binding to 0.0.0.0:** No requirement is stated.
- **Port configuration and publicly exposed ports:** Not addressed.
- **Secrets in deployments:** Not addressed.

The page does say that published apps get isolated compute, secrets, and storage, but it doesn't explain how secrets are made available to the app. The detailed deployment-types page it links to (docs.replit.com/features/publishing/deployment-types.md) may cover these topics.
````

### User / tool · 2026-11-02T21:01:50.232Z

**tool result**
````
**Adding secrets:** Open your project, select **Tools**, then find **Secrets** under **Setup**. Select **New Secret**, enter a **Key** and **Value**, and select **Add Secret**. You can also edit secrets in bulk through the **Secrets** header menu using **Edit as JSON** or **Edit as .env**. Be careful with bulk edits: "Review the full list before saving: bulk editing replaces the project's existing secrets."

**Access in code:** The tool "automatically encrypts the data and makes it available to your Replit project as an environment variable." Your code can read secrets like any other environment variable, so you don't need to hard-code them. To see all variables, run `printenv` in the Shell.

**Deployments:** The docs state that "Secrets are available for all deployment types except Static Deployments." For published apps, go to **Publishing**, select **Adjust settings**, and check **Production app secrets**. The docs recommend reviewing these values, especially if your testing and production credentials differ.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:52.260Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/features/publishing/deployment-types",
 "prompt": "Port configuration for deployments, binding to 0.0.0.0, how many ports exposed, the run command for deployments, Autoscale vs Reserved VM differences (state/filesystem). Quote key lines."
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:01:53.166Z

**tool call — WebFetch**
````
{
 "url": "https://docs.replit.com/replit-workspace/configuring-repl",
 "prompt": "Does the page mention python-3.12 module or listing available modules, and 'onBoot', '[env]' section, '[nix]'? Quote any [env] example and python module versions."
}
````

### User / tool · 2026-11-02T21:01:57.226Z

**tool result**
````
The provided page doesn't cover most of what you asked. It doesn't mention port configuration, binding to 0.0.0.0, how many ports can be exposed, or the state and filesystem differences between Autoscale and Reserved VM.

**What it does say:**

- **Ports and run command:** For Reserved VM, configuration includes "port mappings, and whether the app runs as a web server or a background worker." It also lists "build and run commands" for Reserved VM and Scheduled deployments, but gives no details on the run command's format.
- **Autoscale vs. Reserved VM:** Autoscale servers scale with traffic. "When it's idle, the count drops to as low as zero." Reserved VM is "a dedicated virtual machine that never sleeps." The page doesn't say how either handles state or the filesystem.
- **Static:** Configuration includes "the public directory to serve and an optional build command." Static deployments have no backend server.

For port binding, exposed-port limits, and state or filesystem behavior, check the machine configuration page linked from the article or the full Replit deployment documentation.
````

### User / tool · 2026-11-02T21:01:58.362Z

**tool result**
````
- **python-3.12:** Not mentioned. The only Python module version shown is in the default Python config: "modules = ["python-3.10:v18-20230807-322e88b"]".
- **Listing available modules:** No list of modules is provided. The page describes the `modules` key as "Defines specific versions of programming languages or other major dependencies supported by Replit."
- **onBoot:** Yes. The advanced configuration table gives the example `onBoot = "npm install"` and describes it as "Command that executes when the Replit App boots up."
- **[env] section:** No dedicated `[env]` section appears. The closest match is `[run.env]`, shown in this example:

```toml
[run.env]
NAME="Replit"
```

- **[nix]:** Yes. The default Python configuration includes a `[nix]` section with `channel = "stable-23_05"`. The page describes it as settings for using Nix to manage system dependencies.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:02.585Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p evals/run.py | head -50; ls tests | head -20; grep -n \"pytest\\|testpaths\" -r pytest.ini pyproject.toml setup.cfg 2>/dev/null | head; ls evals/reports | tail -5; ls submission artifacts | head -40; head -30 evals/golden/README.md; cat tools/serve_app.sh >/dev/null; sed -n 1,30p app/frontend/guided/index.html 2>/dev/null | head -5; ls app/frontend/guided | head"
}
````

### User / tool · 2026-11-02T21:02:02.703Z

**tool result**
````
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
    python -m evals.run --write-calibration
                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
    python -m evals.run --record-latest evals/reports/<ts>.md
                                         no run: point latest.json at an existing dated report, values parsed from it, provenance recorded (T-045 r2).
                                         A fixture run never replaces a live ship_bar_met latest.json (it writes latest.fixture.json).

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
artifacts:
m0-smoke
mockups
review-evidence
screenshots
t119-r3-e2e-full.txt
t119-r3-mutB.txt
tmp

submission:
NEEDS_CHRIS.md
prompt-log
# Golden set — expected-output schema (`golden/1`) and hand arithmetic

Owner: qa. Written by hand **before any product code exists**; expected outputs are never produced by running the product or an LLM. This set defines "good enough to ship" (CONTRACT §8.2, REQUIREMENTS §7). Self-check: `python3 evals/golden/check_golden.py` (deterministic).

## Files

| File | What |
|---|---|
| `sample.txt` / `sample.expected.json` | Appendix A records, verbatim (extracted from `spec/SPEC.md` by script), truths from Appendix C |
| `sample.export.expected.txt` | Byte-exact expected export for the sample, extracted by script from REQUIREMENTS §6 (R-EX-6; re-extract if §6 changes). Two blocks split by delimiter lines `=== LETTER_TEXT ... ===` and `=== INTERNAL_NOTES_TEXT ... ===`. `letter_text` = lines between the first and second delimiter; `internal_notes_text` = lines after the second. Trailing newline of each block is not part of the block. |
| `case_NN_<slug>.txt` / `.expected.json` | 9 synthetic cases; line 1 of each `.txt` is `SYNTHETIC — invented for evaluation; not real patient data`. All provider and physician names are obviously fictional. |
| `hallucinations.jsonl` | 40 seeded unsupported summaries `{id, synthetic, category, record_text, candidate_summary, why_unsupported}` for judge recall (ship bar ≥ 95%); 13 come from synthetic cases; includes `temporal_to_causal` (patient's "began after" upgraded to "caused"), `approximation_dropped`, `abbreviation_misexpanded` |
| `hallucinations_controls.jsonl` | 10 supported summaries (5 near-verbatim, 5 paraphrases) `{..., supported: true}`; the judge must NOT reject them (precision guard) |
| `check_golden.py` | validator for all of the above |

## Input format (`*.txt`)

```
=== Record 7 ===
Date: 2026-05-18
Source: Hill Country Pain Management, new patient
Excerpt: "New onset pain ... Date of accident per intake form: 2026-01-19."
```
`Date:` is verbatim as pasted (formats vary on purpose). Record number = ordinal in the file. **The date of service is the header `Date:`**; dates inside an excerpt are evidence for conflict checks only (R-TL-3).

## Expected-output schema (`*.expected.json`)

```jsonc
{
  "schema_version": "golden/1", "case_id", "synthetic": true, "input_file", "description", "stress_types": [...],
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
app.js
core.js
home.js
index.html
step1.js
step2.js
step3.js
step4.js
styles.css
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:06.439Z

**tool call — Bash**
````
{
 "command": "git ls-files evals/reports | grep -v \"^evals/reports/2026\\|runs/\" | head; git ls-files app | grep -c .; git ls-files app | grep -E \"sqlite|\\.env\" ; ls submission/prompt-log | head -3; ls docs"
}
````

### User / tool · 2026-11-02T21:02:06.573Z

**tool result**
````
evals/reports/calibration.json
evals/reports/controls-20261102T042306Z.json
evals/reports/controls-20261102T042306Z.md
evals/reports/controls-20261102T063331Z.json
evals/reports/controls-20261102T063331Z.md
evals/reports/controls-20261102T075238Z.json
evals/reports/controls-20261102T075238Z.md
evals/reports/controls-20261102T090925Z.json
evals/reports/controls-20261102T090925Z.md
evals/reports/controls-20261102T102626Z.json
130
transcripts
CONTRACT.md
GUIDED_UI_SPEC.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md
UI_DESIGN_BRIEF.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:07.433Z

Now run.sh, Makefile, .env.example.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:19.290Z

**tool call — Bash**
````
{
 "command": "cat > .env.example <<'EOF'\n# Copy to .env only if you want live mode. Demo mode (the default) needs NO .env and NO key.\n# .env is git-ignored and never baked into the Docker image. Never commit a real value.\n# Names only here; the values below are placeholders.\n\n# --- Server -----------------------------------------------------------------------------------\n# HOST=127.0.0.1        # the Docker image sets 0.0.0.0; keep 127.0.0.1 on a laptop\n# PORT=7860             # Hugging Face Spaces expects 7860 (app_port)\n\n# --- Demo mode (default) ----------------------------------------------------------------------\n# LLM_BACKEND=fixture   # replays recorded/prepared answers; no model call is possible\n# FIXTURE_SET=curated   # the hand-checked sample set the public demo serves\n\n# --- Live mode (opt-in; leave all of these unset for the public demo) -------------------------\n# Live needs ALL of: ENABLE_LIVE=1, a backend, and (for anthropic-api) a key and a provider-side spend limit.\n# ENABLE_LIVE=1\n# LLM_BACKEND=anthropic-api   # or claude-cli (local dev only: uses your logged-in `claude` CLI, no key)\n# ANTHROPIC_API_KEY=<redacted> PROVIDER_CAP_CONFIRMED=1    # you set a monthly spend limit in the Anthropic console first; the server refuses to start live without this\n# GENERATOR_MODEL=claude-sonnet-5-5\n# JUDGE_MODEL=claude-haiku-5-5\n\n# --- Storage ----------------------------------------------------------------------------------\n# DATA_DIR=./data       # SQLite file lives here (zlayt.sqlite). On a Space the disk is wiped on restart: that is fine for a demo.\nEOF\ncat > run.sh <<'EOF'\n#!/bin/sh\n# One command from a fresh clone to the guided UI in demo mode (no key, no network after the one-time install).\n#   ./run.sh                 demo mode on http://127.0.0.1:7860   (PORT=7870 ./run.sh to change the port)\n#   ./run.sh test            run the unit tests (installs requirements-dev.txt first)\n# Live mode is opt-in: see README.md and .env.example. This script never reads or prints .env.\nset -eu\ncd \"$(dirname \"$0\")\"\n\nPY=\"${PYTHON:-python3}\"\nif ! \"$PY\" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then\n  echo \"Python 3.12+ is required (found: $(\"$PY\" --version 2>&1)). Install it, or set PYTHON=/path/to/python3.12.\" >&2\n  exit 1\nfi\n\nif [ ! -x .venv/bin/python ]; then\n  echo \"Creating .venv and installing requirements (one time, about a minute)...\"\n  \"$PY\" -m venv .venv\nfi\n# Reinstall only when requirements.txt changed since the last successful install.\nif [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then\n  .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt\n  touch .venv/.installed\nfi\n\ncase \"${1:-serve}\" in\n  test)\n    .venv/bin/pip install --quiet --disable-pip-version-check -r requirements-dev.txt\n    exec .venv/bin/python -m pytest tests/unit -q ;;\n  serve)\n    # Demo defaults; a value you already exported wins.\n    export LLM_BACKEND=\"${LLM_BACKEND:-fixture}\" FIXTURE_SET=\"${FIXTURE_SET:-curated}\" HOST=\"${HOST:-127.0.0.1}\" PORT=\"${PORT:-7860}\"\n    .venv/bin/python -m app.config\n    echo \"Serving on http://$HOST:$PORT  (Ctrl-C to stop)\"\n    exec .venv/bin/python -m app.main ;;\n  *)\n    echo \"usage: ./run.sh [serve|test]\" >&2; exit 2 ;;\nesac\nEOF\nchmod +x run.sh\ncat > Makefile <<'EOF'\n# make run | test | evals | docker | docker-run | config      (PORT=7870 make run to change the port)\nPORT ?= 7860\nIMAGE ?= zlayt-demo\n\n.PHONY: run test evals docker docker-run config\n\nrun:            ## demo mode, no key: http://127.0.0.1:$(PORT)\n\tPORT=$(PORT) ./run.sh\n\ntest:           ## unit tests\n\t./run.sh test\n\nevals:          ## golden-set eval on the fixture backend (writes evals/reports/<ts>.md; does not touch calibration.json)\n\t./run.sh >/dev/null 2>&1 & true\n\t@echo \"use: .venv/bin/python -m evals.run   (after ./run.sh has created .venv)\"\n\nconfig:         ## print the resolved mode (never prints a key)\n\t.venv/bin/python -m app.config\n\ndocker:         ## build the demo image\n\tdocker build -t $(IMAGE) .\n\ndocker-run:     ## run the demo image on host port $(PORT)\n\tdocker run --rm -p $(PORT):7860 $(IMAGE)\nEOF\n"
}
````

### User / tool · 2026-11-02T21:02:19.394Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:24.463Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='run.sh'; s=open(p).read()\ns=s.replace(\"#   ./run.sh test \",\"#   ./run.sh setup           create .venv and install requirements only\\n#   ./run.sh test \")\ns=s.replace(\"  test)\\n\",\"  setup)\\n    echo \\\"Ready: .venv installed.\\\" ;;\\n  test)\\n\",1)\ns=s.replace(\"[serve|test]\",\"[serve|setup|test]\")\nopen(p,'w').write(s)\nm=open('Makefile').read()\nm=m.replace(\"\"\"evals:          ## golden-set eval on the fixture backend (writes evals/reports/<ts>.md; does not touch calibration.json)\n\t./run.sh >/dev/null 2>&1 & true\n\t@echo \"use: .venv/bin/python -m evals.run   (after ./run.sh has created .venv)\"\n\"\"\",\"\"\"evals:          ## golden-set eval on the fixture backend (writes evals/reports/<ts>.md; does not touch calibration.json)\n\t./run.sh setup\n\t.venv/bin/python -m evals.run\n\"\"\")\nm=m.replace(\"config:         ## print the resolved mode (never prints a key)\\n\\t.venv\",\"config:         ## print the resolved mode (never prints a key)\\n\\t./run.sh setup\\n\\t.venv\")\nopen('Makefile','w').write(m)\nEOF\nsh -n run.sh && echo ok; head -20 evals/reports/latest.json; "
}
````

### User / tool · 2026-11-02T21:02:24.588Z

**tool result**
````
ok
{
 "backend": "claude-cli",
 "blockers": [],
 "generated_at": "2026-11-02T16:40:38Z",
 "hashes": {
  "app/llm/lexicon.yaml": "fbefe801fb3d582c48e93bfbe54ccb1e34e9640a5b6cbf800e42a5aa7f612a8b",
  "app/llm/prompts/extract_es_v1.md": "985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb",
  "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
  "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
  "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
  "app/llm/prompts/judge_conflict_v1.md": "10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa",
  "app/llm/prompts/judge_conflict_v2.md": "6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6",
  "app/llm/prompts/judge_conflict_v4.md": "15df87e8655a014111bbcddb2fee769d01e28149072ceea76f3f9d51fcae4649",
  "app/llm/prompts/judge_conflict_v5.md": "90deea934564aa0fda0ad34dc38477104e371c0267259c38c61f58635819dffd",
  "app/llm/prompts/judge_conflict_v6.md": "8a09702a5c12a9f08a162cad574374827d3a367cbcca7080e1331c76406318b5",
  "app/llm/prompts/judge_faithfulness_es_v1.md": "d51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898",
  "app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b",
  "app/llm/prompts/judge_flag_v1.md": "97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432",
  "app/llm/prompts/judge_flag_v2.md": "7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe",
  "app/llm/prompts/judge_flag_v3.md": "64d65c0182360d4ef84b5f4b62e19a6707ee3f508d975aec4ea6e527c9a5a664",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:32.221Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo $SP > /dev/null && IMG=$SP/image-emu && rm -rf $IMG && mkdir -p $IMG/app_root && \n# emulate COPY layers per .dockerignore allow-list from tracked files only\ngit ls-files -z requirements.txt app evals/golden evals/library evals/reports/calibration.json tests/fixtures/llm | (cd . && xargs -0 -I{} cp --parents {} $IMG/app_root 2>/dev/null || tar -cf - --null -T - | tar -xf - -C $IMG/app_root) ; ls $IMG/app_root"
}
````

### User / tool · 2026-11-02T21:02:34.794Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:40.449Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; IMG=$SP/image-emu; rm -rf $IMG; mkdir -p $IMG/app\ngit ls-files -z requirements.txt app evals/golden evals/library evals/reports/calibration.json tests/fixtures/llm | tar -cf - --null -T - | tar -xf - -C $IMG/app\nls $IMG/app; du -sh $IMG/app\ncd $IMG && time (python3.12 -m venv venv && ./venv/bin/pip install -q --disable-pip-version-check -r app/requirements.txt) 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T21:02:49.512Z

**tool result**
````
tar: app/frontend/narrative.js: Cannot stat: No such file or directory
tar: Error exit delayed from previous errors.
app
evals
requirements.txt
tests
7.3M	/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/image-emu/app

real	0m7.797s
user	0m5.094s
sys	0m1.588s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:02:57.108Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/image-emu/app && mkdir -p ../data && cp /Users/arsis/zlayt-pm-project/app/config.py app/config.py && \nenv -i PATH=/usr/bin:/bin HOME=$PWD/.. HOST=0.0.0.0 PORT=7871 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=$PWD/../data PYTHONUNBUFFERED=1 ../venv/bin/python -m app.config\nenv -i PATH=/usr/bin:/bin HOME=$PWD/.. HOST=0.0.0.0 PORT=7871 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=$PWD/../data ../venv/bin/python -m app.main > ../server.log 2>&1 &\necho $! > ../server.pid; sleep 4; curl -s localhost:7871/api/health | head -c 300; echo; curl -s -o /dev/null -w \"ui %{http_code}\\n\" localhost:7871/; cat ../server.log | head"
}
````

### User / tool · 2026-11-02T21:03:01.774Z

**tool result**
````
{
  "mode": "demo",
  "backend": "fixture",
  "fixture_set": "curated",
  "host": "0.0.0.0",
  "port": 7871,
  "anthropic_api_key": "not set",
  "local_mode": false,
  "warnings": []
}
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max
ui 200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:03:05.867Z

**tool call — Bash**
````
{
 "command": "grep -n \"sample\\|POST /api/cases\" memory/contracts/api.md | head -15"
}
````

### User / tool · 2026-11-02T21:03:06.068Z

**tool result**
````
3:Status: drafted by the architect (T-014, round 2). From M2 the backend worker is the sole writer; changes after that go through a card. Frontend may start against the examples below. They use the Appendix A sample case (Jordan Rivera, SYNTHETIC) as stored in `evals/golden/sample.txt`; **every `start`/`end` is an absolute character offset into the case's raw text, and `raw_text[start:end]` equals the quoted string** (verified by a script run for the T-014 handoff). Design rationale: `memory/DECISIONS.md` ADR-002, 005, 006, 007, 009 to 017. Orchestrator decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001..D-024). Requirements: `spec/REQUIREMENTS.md`; the conflicts it lists in §8 are resolved in ADR-017.
18:| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
55:  "sample_available": true }
57:`answers` (T-177, D-065): whose answers the app shows. `prepared` = the curated fixture set (`FIXTURE_SET=curated`): hand-checked by the team, NOT model output; `recorded` = a replay of real model answers (the default fixture dir); `live` = a model answering now. The UI badge follows it: `prepared` -> "Demo: sample answers prepared by our team" (tooltip "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."; T-177 r2: the report does not hold the answers, so the old pointer was cut), `recorded` -> "Demo: recorded AI answers". With `prepared`, `ai_banner` reads "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item".
62:## POST /api/cases
63:Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). A title is plain text (T-157 r2): control, zero-width and bidi-override characters are removed, line breaks and tabs become spaces, runs of white space collapse; blank means no name. A `title` with a `<` or `>` in it, or longer than 120 characters, is refused: `422 invalid_title` with a plain `message` that never repeats the text, and no case is created (the same for the `title` query of `POST /api/cases/pdf`, checked before the PDF is read). The older `name` field is held to the markup rule too, but a `name` longer than 120 characters (a long file name) is cut, not refused. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
65:{ "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
67:Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
69:{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ingested", "source": "paste",
80:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
82:## POST /api/cases/pdf (D-031)
83:Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
87:Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server. A page larger than 40 inches on a side is refused (`ocr_page_too_large`, `detail.page`); a larger one under that is rendered smaller than 150 dpi (longest side at most 3500 px, area at most 8 million px); all page images of one upload together are capped at 12 MB (`ocr_images_too_large`). Tesseract runs with a scrubbed environment (no API key or token reaches it). One deadline (10 s, or 165 s with OCR) covers text reading, the hidden-text scan and OCR; when it passes the work stops and the response is `400 bad_request` with `detail.reason: "pdf_timeout"`.
110:## POST /api/cases/{token}/review/batch (D-031)
117:## POST /api/cases/{token}/run
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:03:09.605Z

**tool call — Bash**
````
{
 "command": "cd /tmp && T=$(curl -s -X POST localhost:7871/api/cases -H 'content-type: application/json' -d '{\"sample\":true}' | python3 -c \"import sys,json; print(json.load(sys.stdin)['token'])\"); echo token ok; curl -s -X POST localhost:7871/api/cases/$T/run -H 'content-type: application/json' -d '{}' -w \"\\nrun %{http_code}\\n\" | head -c 300; sleep 5; curl -s localhost:7871/api/cases/$T | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d.get('status'), len(d.get('entries',[])), 'entries', len(d.get('flags',[])), 'flags', d.get('backend'))\""
}
````

### User / tool · 2026-11-02T21:03:14.847Z

**tool result**
````
token ok
{"token":"13PGuXQUMHtLwNoEZ11vIA","status":"running","stage":"extract","started_at":"2026-11-02T21:03:09Z"}
run 202
ready 9 entries 10 flags fixture
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:03:20.071Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/image-emu && kill $(cat server.pid); sleep 1; curl -s -m 2 localhost:7871/ >/dev/null && echo still up || echo stopped; cd /Users/arsis/zlayt-pm-project; python3 tools/board.py note T-182 --agent release --text \"Dockerfile, .dockerignore, run.sh, Makefile, .env.example, app/config.py written. Docker daemon is NOT running on this host (client only, no buildx/colima/orbstack): docker build/run cannot be executed here. Verified the same image recipe by emulation: allow-listed tracked files, fresh py3.12 venv from requirements.txt (8s), Dockerfile ENV, python -m app.main on :7871 -> /api/health demo_mode true, sample case run -> ready, 9 entries, 10 flags. HF + Replit docs fetched; next: deploy docs, README, clone timing.\""
}
````

### User / tool · 2026-11-02T21:03:21.229Z

**tool result**
````
stopped
noted on T-182
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:03:51.494Z

**tool call — Bash**
````
{
 "command": "mkdir -p deploy/replit && cat > deploy/hf_space_frontmatter.yml <<'EOF'\n---\ntitle: Treatment Timeline (synthetic demo)\nemoji: 🗂️\ncolorFrom: blue\ncolorTo: gray\nsdk: docker\napp_port: 7860\nshort_description: Medical records to a verified treatment chronology. Synthetic data only.\npinned: false\n---\n\nEOF\ncat > deploy/hf_push.sh <<'EOF'\n#!/bin/sh\n# Publish the demo to a Hugging Face Docker Space as a clean one-commit snapshot (no board, memory, reviews, .claude or history).\n#   deploy/hf_push.sh <hf-username>/<space-name>\n# Prerequisites: the Space already exists (SDK: Docker) and git can authenticate to huggingface.co\n# (username + a write-scoped access token as the password, or `hf auth login` / a git credential helper).\n# This script never reads, takes or prints a token. It force-pushes the snapshot to the Space's main branch.\nset -eu\n[ $# -eq 1 ] || { echo \"usage: deploy/hf_push.sh <hf-username>/<space-name>\" >&2; exit 2; }\nSPACE=\"$1\"\ncd \"$(dirname \"$0\")/..\"\ngit diff --quiet HEAD -- Dockerfile .dockerignore README.md requirements.txt app evals tests/fixtures/llm || { echo \"Uncommitted changes in shipped paths; commit first (the snapshot is taken from HEAD).\" >&2; exit 1; }\n\nTMP=\"$(mktemp -d)\"\ntrap 'rm -rf \"$TMP\"' EXIT\n# Same allow-list as .dockerignore, taken from HEAD so untracked/ignored files (.env, databases) can never ride along.\ngit archive HEAD Dockerfile .dockerignore requirements.txt app evals/golden evals/library evals/reports/calibration.json tests/fixtures/llm | tar -x -C \"$TMP\"\ncat deploy/hf_space_frontmatter.yml README.md > \"$TMP/README.md\"\n\n# Refuse to publish if anything key-shaped slipped in.\nif grep -rIlE 'sk-ant-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{30,}' \"$TMP\" >/dev/null 2>&1; then\n  echo \"Refusing to push: a key-shaped string is in the snapshot.\" >&2; exit 1\nfi\n\ncd \"$TMP\"\ngit init -q -b main\ngit add -A\ngit -c user.name=\"release\" -c user.email=\"release@example.invalid\" commit -q -m \"Deploy demo snapshot\"\ngit remote add space \"https://huggingface.co/spaces/$SPACE\"\ngit push --force space main\necho \"Pushed. Build logs: https://huggingface.co/spaces/$SPACE (Logs tab). Live at https://huggingface.co/spaces/$SPACE\"\nEOF\nchmod +x deploy/hf_push.sh\ncat > deploy/HUGGINGFACE.md <<'EOF'\n# Deploy to Hugging Face Spaces (Docker SDK)\n\nThe demo image needs no key and no secrets: it serves the guided UI on port 7860 in demo mode from committed fixtures.\n\nSources checked 2026-11-02:\n- Docker Spaces: <https://huggingface.co/docs/hub/spaces-sdks-docker> (sdk, app_port, permissions, secrets, persistence)\n- Config reference: <https://huggingface.co/docs/hub/spaces-config-reference> (`sdk`, `app_port`, `short_description`, `startup_duration_timeout`)\n\n## What the docs require, and where we meet it\n\n| HF requirement (from the docs above) | How this repo meets it |\n|---|---|\n| README.md YAML block at the repo root with `sdk: docker` | `deploy/hf_space_frontmatter.yml` is prepended to README.md by `deploy/hf_push.sh` (the repo README stays clean for GitHub) |\n| \"change the default exposed port 7860 by setting `app_port: 7860`\" | `app_port: 7860` in the front matter; the Dockerfile `EXPOSE`s and listens on 7860 (`PORT=7860`, `HOST=0.0.0.0`) |\n| \"The container runs with user ID 1000\" | Dockerfile creates `user` (uid 1000), `WORKDIR /home/user/app`, `COPY --chown=user` |\n| Data on disk is lost on restart | Fine for a demo: cases are 24 h-retained scratch data in `/home/user/data`; nothing needs to persist |\n| Secrets are runtime env vars; build-time access only via `--mount=type=secret` | The image uses no build-time secret. Live mode (optional) reads `ANTHROPIC_API_KEY` at runtime |\n\n## Steps (about 10 minutes, mostly the first build)\n\n1. Create the Space: <https://huggingface.co/new-space> -> SDK **Docker** (Blank template) -> hardware **CPU basic** -> **Public**. Note the id `<username>/<space-name>`.\n2. Authenticate git to huggingface.co (username + a **write** access token as the password, or a credential helper). Do not paste the token into any file in this repo.\n3. From a clean checkout of this repo (everything committed):\n   ```\n   deploy/hf_push.sh <username>/<space-name>\n   ```\n   It builds a one-commit snapshot of the allow-listed paths only (see `.dockerignore`), prepends the YAML block, scans it for key-shaped strings, and force-pushes it to the Space.\n4. Open the Space's **Logs** tab. The build takes a few minutes; when the status turns **Running**, open the Space URL. You should see the guided UI with the \"Synthetic data only\" banner and \"Demo: sample answers prepared by our team\".\n5. Smoke test: `curl https://<username>-<space-name>.hf.space/api/health` returns `\"demo_mode\":true`.\n\n## Live mode on a Space (optional, off by default)\n\nThe public link should stay in demo mode: a visitor can only run the sample and golden cases, and no code path can call a model. To enable live calls you accept responsibility for spend:\n\n1. Set a monthly spend limit for the key in the Anthropic console first.\n2. Space -> **Settings** -> **Variables and secrets**:\n   - Secret `ANTHROPIC_API_KEY` (the key; Secrets are not shown after saving and are injected at runtime)\n   - Variables `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api`, `PROVIDER_CAP_CONFIRMED=1`\n3. Restart the Space. `/api/health` should now report `\"demo_mode\":false`.\n4. To go back: delete `ENABLE_LIVE` (demo mode wins whatever else is set).\n\nPer-session rate limits and a server-side spend cap are tracked in separate M4 backend cards; until they land, do not leave a live key on a public Space.\n\n## Troubleshooting\n\n- Build fails at `pip install`: check the Logs tab; the pins in `requirements.txt` target Python 3.12 (the Dockerfile base is `python:3.12-slim`).\n- \"Application startup failed ... PROVIDER_CAP_CONFIRMED\": you enabled live `anthropic-api` without the spend-limit acknowledgement (by design).\n- Space shows \"Building\" for a long time: `startup_duration_timeout` defaults to 30 minutes; the demo starts in seconds once built.\n- Scanned-PDF OCR needs Tesseract, which the slim image does not include; the PDF text-layer path works without it.\nEOF\ncat > deploy/replit/.replit <<'EOF'\n# Copy this file to the repo root as `.replit` after importing the repo into Replit (see deploy/REPLIT.md).\n# Format per https://docs.replit.com/replit-workspace/configuring-repl (run, modules, [[ports]], [deployment]).\n# The python module name is NOT listed on that page (its example is python-3.10): pick Python 3.12 in the Replit UI if this line is rejected.\nmodules = [\"python-3.12\"]\nrun = \"./run.sh\"\n\n[run.env]\nHOST = \"0.0.0.0\"\nPORT = \"7860\"\nLLM_BACKEND = \"fixture\"\nFIXTURE_SET = \"curated\"\n\n[[ports]]\nlocalPort = 7860\nexternalPort = 80\n\n[deployment]\nbuild = [\"./run.sh\", \"setup\"]\nrun = [\"./run.sh\"]\ndeploymentTarget = \"cloudrun\"\nEOF\ncat > deploy/REPLIT.md <<'EOF'\n# Run on Replit (alternate host)\n\nHugging Face Spaces is the primary host (`deploy/HUGGINGFACE.md`). Replit works too because the app is one Python process with no external services.\n\nSources checked 2026-11-02:\n- `.replit` file: <https://docs.replit.com/replit-workspace/configuring-repl> (`run`, `modules`, `[[ports]]` with `localPort`/`externalPort`, `[deployment]` with `build`/`run`/`deploymentTarget`, `[run.env]`)\n- Secrets: <https://docs.replit.com/replit-workspace/workspace-features/secrets> (\"available for all deployment types except Static Deployments\"; add under Tools -> Secrets)\n- Deployment types: <https://docs.replit.com/features/publishing/deployment-types> (Autoscale, Reserved VM, Static, Scheduled)\n\nNot confirmed from the docs fetched: the exact Python 3.12 module name (the docs page shows only `python-3.10`), and the port-binding rules for deployments. `deploy/replit/.replit` uses `python-3.12` and binds `0.0.0.0:7860`; if Replit rejects the module line, choose Python 3.12 in the Replit UI and let it rewrite that line.\n\n## Steps\n\n1. Replit -> **Create App** -> **Import from GitHub** -> paste this repo's URL.\n2. In the Shell: `cp deploy/replit/.replit .replit` (Replit reads `.replit` only from the repo root).\n3. Press **Run**. The first run creates `.venv` and installs `requirements.txt` (about a minute), then serves on 7860; the webview opens it.\n4. To publish: **Publish** -> **Autoscale** (or Reserved VM) -> keep the run command `./run.sh`. No secrets are needed for demo mode.\n\n## Live mode on Replit (optional)\n\nTools -> **Secrets**: add `ANTHROPIC_API_KEY`. Then add `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api`, `PROVIDER_CAP_CONFIRMED=1` (also under Secrets or in `[run.env]`; not the key). For a published app, Publishing -> Adjust settings -> **Production app secrets** must include them. Set a provider-side spend limit first. Delete `ENABLE_LIVE` to return to demo mode.\nEOF\n"
}
````

### User / tool · 2026-11-02T21:03:51.615Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:10.631Z

**tool call — Bash**
````
{
 "command": "cat > README.md <<'EOF'\n# Treatment timeline: medical records to a verified chronology\n\nA prototype for a personal-injury paralegal. Paste (or upload) medical records and get a dated treatment chronology where **every statement is tied to a verbatim excerpt of the record**, every date and total is computed by code, gaps and conflicts are flagged with their evidence, and nothing reaches the demand-letter export until a human accepts it.\n\n**Synthetic data only.** The app shows a banner and refuses text it has not seen in demo mode. Never paste real patient or client records.\n\nHow the work is split: language and judgment (summaries, \"is this supported by the quote?\") are LLM steps; dates, gap arithmetic, substring checks, currency totals, dedupe and export are plain code. Each LLM output passes a code check, then an independent judge, then a human accept / edit / dismiss. The table is in [`docs/LLM_VS_CODE.md`](docs/LLM_VS_CODE.md).\n\n## Run it from a clone (about 3 minutes, no key)\n\nNeeds Python 3.12+ and git. Docker is optional.\n\n```\ngit clone <this repo> zlayt && cd zlayt\n./run.sh\n```\n\nOpen <http://127.0.0.1:7860>. The first run creates `.venv` and installs `requirements.txt` (the only slow step); later runs start in seconds. Use another port with `PORT=7870 ./run.sh`.\n\nTimed on 2026-11-02 from a fresh `git clone` into an empty directory on an Apple-silicon Mac (Python 3.12.2, warm pip download cache is **not** assumed; figures are in `deploy/TIMING.md`).\n\nThen: click the sample case, run it, and review the entries. Each timeline entry shows its exact excerpt; flags (gaps, conflicts, unclear charges) show their evidence; Accept / Edit / Dismiss decides what the export contains.\n\nEquivalent commands: `make run`, `make test`, `make evals`, `make config` (prints the resolved mode; never prints a key).\n\n### With Docker\n\n```\ndocker build -t zlayt-demo .\ndocker run --rm -p 7860:7860 zlayt-demo        # http://127.0.0.1:7860\n```\n\nThe image contains the app, the synthetic eval inputs and the committed LLM fixtures, and nothing else (`.dockerignore` is an allow-list; there is no `.env`, key or database in it). It runs as uid 1000, listens on `0.0.0.0:7860`, and has a health check on `/api/health`.\n\n## Demo mode vs live mode\n\n| | Demo mode (default) | Live mode (opt-in) |\n|---|---|---|\n| Needs | nothing | `ENABLE_LIVE=1` and a model to call |\n| Model calls | none possible: the fixture backend replays answers | yes: `LLM_BACKEND=claude-cli` (local, your logged-in `claude` CLI) or `anthropic-api` (key) |\n| Accepted input | the sample and the committed golden/library cases only (others get `409 demo_mode_unsupported_input`) | any pasted text or PDF, within size limits |\n| Answers shown as | \"prepared by our team\" (curated set, hand-checked, then checked by code) | produced by the model now |\n\nDemo wins whatever else is set: without `ENABLE_LIVE=1` the backend is `fixture` even if `LLM_BACKEND` or a key is present. Live `anthropic-api` also needs `PROVIDER_CAP_CONFIRMED=1` (you set a provider-side spend limit first) or the server refuses to start.\n\nTo go live locally: `cp .env.example .env`, uncomment the live block, put your key in `.env` (git-ignored), then load it into the shell yourself (for example `set -a; . ./.env; set +a; ./run.sh`). `.env.example` lists every variable; the repo never contains a key. Check what you got with `make config`.\n\n## Deploy\n\n- Hugging Face Spaces (primary, Docker SDK, port 7860, secrets in Space settings): [`deploy/HUGGINGFACE.md`](deploy/HUGGINGFACE.md), one command `deploy/hf_push.sh <user>/<space>`.\n- Replit (alternate): [`deploy/REPLIT.md`](deploy/REPLIT.md).\n\n## Where things are\n\n| Looking for | Path |\n|---|---|\n| Evals: golden set, runner, reports | `evals/golden/` (hand-written expected outputs), `evals/run.py`, `evals/reports/latest.json` and dated `*.md` reports. Run `make evals` (fixture backend; does not overwrite the committed `calibration.json`) |\n| Tests | `tests/unit`, `tests/e2e` (Playwright, needs `requirements-dev.txt`) |\n| Submission package (product note, Part 2 process doc, prompt log, checklist) | `submission/` |\n| Requirements, spec, API contract | `spec/REQUIREMENTS.md`, `spec/SPEC.md`, `memory/contracts/api.md` |\n| Architecture and decisions | `app/README-arch.md`, `memory/DECISIONS.md`, `docs/LLM_VS_CODE.md` |\n| Screenshots and demo video | `artifacts/screenshots/`, `artifacts/demo.webm` (M4) |\n| How the AI team worked (board, reviews) | `board/`, `reviews/`, `memory/LESSONS.md` |\n\n## Layout\n\n`app/backend` (API, pipeline, deterministic checks), `app/llm` (prompts, backends, fixtures replay), `app/db` (SQLite), `app/frontend` (guided UI, no build step), `app/config.py` (resolved mode).\nEOF\nprintf '# Timing: README run-from-clone path\\n\\n(filled in below by the release worker)\\n' > deploy/TIMING.md; sed -n 1,15p docs/LLM_VS_CODE.md | head -3; ls spec memory | head -20"
}
````

### User / tool · 2026-11-02T21:04:10.733Z

**tool result**
````
# Where the AI works and where plain code works

*Treatment Timeline prototype. For the hiring panel, reviewers and the developers who maintain it. Decisions behind this page: `memory/DECISIONS.md` ADR-003, 004, 005, 008, 010 to 020; cross-cutting decisions D-001 to D-057 in `memory/ORCHESTRATOR_DECISIONS.md`. Requirements it serves: `spec/REQUIREMENTS.md`.*
memory:
ASSUMPTIONS.md
DECISIONS.md
ENVIRONMENT.md
GLOSSARY.md
LESSONS.md
ORCHESTRATOR_DECISIONS.md
PROGRESS.md
SCOPE_CUTS.md
STATE.md
contracts

spec:
REQUIREMENTS.md
SAMPLE_CASE_TRUTHS.md
SPEC.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:14.410Z

**tool call — Bash**
````
{
 "command": "F=\"Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy\" && git add $F && git commit -q -m \"feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- $F && git log --oneline -1 && git show --stat HEAD | tail -15"
}
````

### User / tool · 2026-11-02T21:04:14.473Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: F="Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy" && git add $F && git commit -q -m "feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/M
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:17.833Z

**tool call — Bash**
````
{
 "command": "git add Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy && git status --short Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy"
}
````

### User / tool · 2026-11-02T21:04:17.963Z

**tool result**
````
A  .dockerignore
A  .env.example
A  Dockerfile
A  Makefile
A  README.md
A  app/config.py
A  deploy/HUGGINGFACE.md
A  deploy/REPLIT.md
A  deploy/TIMING.md
A  deploy/hf_push.sh
A  deploy/hf_space_frontmatter.yml
A  deploy/replit/.replit
A  run.sh
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:19.965Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy && git log --oneline -1"
}
````

### User / tool · 2026-11-02T21:04:21.158Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: secret check failed on staged files:
check_secrets: BLOCKED
.env.example:17: Anthropic key (value redacted)
.env.example:17: ANTHROPIC_API_KEY with a value (value redacted) | command: git commit -q -m "feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:25.459Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/^# ANTHROPIC_API_KEY=<redacted> ANTHROPIC_API_KEY=                 <redacted> paste your key here in .env only/' .env.example && python3 tools/check_secrets.py --help 2>&1 | head -3; git add .env.example && python3 tools/check_secrets.py --staged; echo rc=$?"
}
````

### User / tool · 2026-11-02T21:04:28.019Z

**tool result**
````
check_secrets: ok (2382 file(s) scanned)
check_secrets: ok (63 file(s) scanned staged)
rc=0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:31.578Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- Dockerfile .dockerignore README.md .env.example Makefile run.sh app/config.py deploy && git log --oneline -1 && git show --stat HEAD --format= | tail -16"
}
````

### User / tool · 2026-11-02T21:04:35.777Z

**tool result**
````
check_secrets: ok (13 file(s) scanned staged)
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
 .dockerignore                   | 14 +++++++++
 .env.example                    | 23 ++++++++++++++
 Dockerfile                      | 28 +++++++++++++++++
 Makefile                        | 25 +++++++++++++++
 README.md                       | 67 +++++++++++++++++++++++++++++++++++++++++
 app/config.py                   | 39 ++++++++++++++++++++++++
 deploy/HUGGINGFACE.md           | 49 ++++++++++++++++++++++++++++++
 deploy/REPLIT.md                | 21 +++++++++++++
 deploy/TIMING.md                |  3 ++
 deploy/hf_push.sh               | 30 ++++++++++++++++++
 deploy/hf_space_frontmatter.yml | 11 +++++++
 deploy/replit/.replit           | 20 ++++++++++++
 run.sh                          | 40 ++++++++++++++++++++++++
 13 files changed, 370 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:04:47.566Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $SP/clone-run && mkdir $SP/clone-run && cd $SP/clone-run\nS=$(date +%s)\ngit clone -q /Users/arsis/zlayt-pm-project zlayt && cd zlayt; C=$(date +%s); echo \"clone: $((C-S))s\"\nPIP_NO_CACHE_DIR=1 PORT=7872 ./run.sh > ../run.log 2>&1 &\necho $! > ../run.pid\nfor i in $(seq 1 120); do if curl -s -m 1 localhost:7872/api/health | grep -q '\"ok\":true'; then break; fi; sleep 1; done\nE=$(date +%s); echo \"clone+install+first health: $((E-S))s (run.sh part: $((E-C))s)\"\ncurl -s localhost:7872/api/health | head -c 200; echo; cat ../run.log | head -20\n# sample flow\nT=$(curl -s -X POST localhost:7872/api/cases -H 'content-type: application/json' -d '{\"sample\":true}' | python3 -c \"import sys,json; print(json.load(sys.stdin)['token'])\"); curl -s -o /dev/null -X POST localhost:7872/api/cases/$T/run -H 'content-type: application/json' -d '{}'; sleep 4; curl -s localhost:7872/api/cases/$T | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d['status'], len(d['entries']), len(d['flags']))\"\necho \"total incl. sample run: $(( $(date +%s)-S ))s\""
}
````

### User / tool · 2026-11-02T21:05:08.935Z

**tool result**
````
clone: 5s
clone+install+first health: 17s (run.sh part: 12s)
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{
Creating .venv and installing requirements (one time, about a minute)...
{
  "mode": "demo",
  "backend": "fixture",
  "fixture_set": "curated",
  "host": "127.0.0.1",
  "port": 7872,
  "anthropic_api_key": "not set",
  "local_mode": false,
  "warnings": []
}
Serving on http://127.0.0.1:7872  (Ctrl-C to stop)
ready 9 10
total incl. sample run: 21s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:12.069Z

**tool call — Bash**
````
{
 "command": "git diff --cached --name-only | grep -E \"^(\\.env\\.example|Dockerfile|README\\.md|Makefile|run\\.sh|deploy/|app/config\\.py|\\.dockerignore)\" ; echo \"staged-of-mine: none above\"; git status --short .env.example; grep -n \"ANTHROPIC_API_KEY\" .env.example; python3 tools/check_secrets.py; git log --oneline -1 -- .env.example"
}
````

### User / tool · 2026-11-02T21:05:13.528Z

**tool result**
````
staged-of-mine: none above
17:# ANTHROPIC_API_KEY=                 <redacted> paste your key here in .env only
check_secrets: ok (2382 file(s) scanned)
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:27.261Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; kill $(cat $SP/clone-run/run.pid) 2>/dev/null; sleep 1; curl -s -m 2 localhost:7872/ >/dev/null && echo up || echo stopped\ncd /Users/arsis/zlayt-pm-project && cat > deploy/TIMING.md <<'EOF'\n# Timing: README run-from-clone path\n\nMeasured 2026-11-02 by the release worker (T-182), following README.md literally: `git clone` into an empty directory, then `./run.sh` (PORT=7872 only to avoid the dev server on 7860).\n\n| Step | Time |\n|---|---|\n| `git clone` (local path) | 5 s |\n| `./run.sh`: create `.venv`, `pip install -r requirements.txt` with `PIP_NO_CACHE_DIR=1` (wheels downloaded, not cached), start server, first `/api/health` ok | 12 s |\n| Clone to a healthy server | 17 s |\n| Plus: create the sample case, run it, read 9 entries / 10 flags back over the API | 21 s total |\n\nHost: Apple-silicon Mac, Python 3.12.2, fast network. A slower network or a first-ever pip download of pypdfium2/uvloop wheels can add a minute or two; the README bar is under 5 minutes.\nThe clone was of the local repository, not a remote; clone time over the network is not included.\n\n## Docker\n\nThe Docker daemon was not running on the host this was built on (docker client 29.9.2 present; no daemon, no buildx, no Colima/OrbStack), so `docker build` and `docker run` were NOT executed. The same recipe was run without Docker: the `.dockerignore` allow-list taken from tracked files, a fresh Python 3.12 venv from `requirements.txt`, the Dockerfile's `ENV` (`HOST=0.0.0.0 LLM_BACKEND=fixture FIXTURE_SET=curated`), `python -m app.main` -> `/api/health` `demo_mode: true`, sample case ran to `ready`. Run `make docker docker-run` on a machine with Docker to close this gap; the installer-reviewer can do it at the M4 gate.\nEOF\npython3 - <<'EOF'\np='README.md'; s=open(p).read()\na=s.index(\"Timed on 2026-11-02\"); b=s.index(\"Then: click\")\ns=s[:a]+\"Timed 2026-11-02 from a fresh `git clone` into an empty directory: 17 s to a healthy server with a cold pip download (Apple-silicon Mac, Python 3.12.2, fast network; details in [`deploy/TIMING.md`](deploy/TIMING.md)). Budget a few minutes on a slow network.\\n\\n\"+s[b:]\nopen(p,'w').write(s)\nEOF\ngit add README.md deploy/TIMING.md && git commit -q -m \"docs(release): T-182 record timed clone path (17s) and Docker-daemon caveat\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- README.md deploy/TIMING.md; git log --oneline -1"
}
````

### User / tool · 2026-11-02T21:05:27.327Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf80
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:35.884Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; kill $(cat $SP/clone-run/run.pid) 2>/dev/null; sleep 1; curl -s -m 2 localhost:7872/ >/dev/null && echo up || echo stopped\ncd /Users/arsis/zlayt-pm-project && cat > deploy/TIMING.md <<'EOF'\n# Timing: README run-from-clone path\n\nMeasured 2026-11-02 by the release worker (T-182), following README.md literally: `git clone` into an empty directory, then `./run.sh` (PORT=7872 only to avoid the dev server on 7860).\n\n| Step | Time |\n|---|---|\n| `git clone` (local path) | 5 s |\n| `./run.sh`: create `.venv`, `pip install -r requirements.txt` with `PIP_NO_CACHE_DIR=1` (wheels downloaded, not cached), start server, first `/api/health` ok | 12 s |\n| Clone to a healthy server | 17 s |\n| Plus: create the sample case, run it, read 9 entries / 10 flags back over the API | 21 s total |\n\nHost: Apple-silicon Mac, Python 3.12.2, fast network. A slower network can add a minute or two; the README bar is under 5 minutes.\nThe clone was of the local repository, not a remote; clone time over the network is not included.\n\n## Docker\n\nThe Docker daemon was not running on the host this was built on (docker client 29.9.2 present; no daemon, no buildx, no Colima/OrbStack), so `docker build` and `docker run` were NOT executed. The same recipe was run without Docker: the `.dockerignore` allow-list taken from tracked files, a fresh Python 3.12 venv from `requirements.txt`, the Dockerfile's `ENV` (`HOST=0.0.0.0 LLM_BACKEND=fixture FIXTURE_SET=curated`), `python -m app.main` -> `/api/health` `demo_mode: true`, sample case ran to `ready`. Run `make docker docker-run` on a machine with Docker to close this gap; the installer-reviewer can do it at the M4 gate.\nEOF\npython3 - <<'EOF'\np='README.md'; s=open(p).read()\na=s.index(\"Timed on 2026-11-02\"); b=s.index(\"Then: click\")\ns=s[:a]+\"Timed 2026-11-02 from a fresh `git clone` into an empty directory: 17 s to a healthy server with a cold pip download (Apple-silicon Mac, Python 3.12.2, fast network; details in [`deploy/TIMING.md`](deploy/TIMING.md)). Budget a few minutes on a slow network.\\n\\n\"+s[b:]\nopen(p,'w').write(s)\nEOF\ngit add README.md deploy/TIMING.md"
}
````

### User / tool · 2026-11-02T21:05:37.032Z

**tool result**
````
stopped
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:39.971Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"docs(release): T-182 record timed clone path (17s) and Docker-daemon caveat\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- README.md deploy/TIMING.md && git log --oneline -1 && git log --format=%h -2 | tr '\\n' ' '"
}
````

### User / tool · 2026-11-02T21:05:41.324Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
f547db4 docs(release): T-182 record timed clone path (17s) and Docker-daemon caveat
f547db4 4671eee
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:50.995Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B handoff T-182 --agent release --text \"Changed: Dockerfile (python:3.12-slim, uid 1000, 0.0.0.0:7860, demo env, healthcheck), .dockerignore allow-list, run.sh, Makefile, .env.example (no values), app/config.py (python -m app.config prints mode, never a key), deploy/HUGGINGFACE.md + hf_push.sh + hf_space_frontmatter.yml, deploy/REPLIT.md + replit/.replit, README.md, deploy/TIMING.md. Commits ac678bc, f547db4.\nVerified: fresh git clone + ./run.sh (cold pip) = 17s to healthy, 21s incl. sample run (9 entries, 10 flags); check_secrets ok; HF docs (spaces-sdks-docker, spaces-config-reference) and Replit docs (configuring-repl, secrets, deployment-types) fetched and cited.\nNOT verified: docker build/run. The Docker daemon is not running on this host (client only, no buildx/colima/orbstack). The same recipe was run without Docker (allow-listed tree, fresh py3.12 venv, Dockerfile ENV, :7871: demo_mode true, sample ready). AC1 left unchecked for that reason; run make docker docker-run on a Docker host.\nLeft: Replit python-3.12 module name and deployment port rules are not in the fetched docs (flagged in REPLIT.md); live-mode rate limit/spend cap belongs to backend cards; Tesseract OCR not in the slim image; nothing pushed to HF (needs Chris's token).\nSurprised: check_secrets flags a placeholder sk-ant-... in .env.example (fixed: empty value); git-guard rejects add+commit in one command.\"\n$B move T-182 in_review --agent release; $B commit T-182 --sha f547db4 --agent release; $B commit T-182 --sha ac678bc --agent release"
}
````

### User / tool · 2026-11-02T21:05:51.292Z

**tool result**
````
handoff written on T-182
board.py: error: AC [1] unchecked; check them with evidence or give --note explaining
T-182: commit f547db4 recorded
T-182: commit ac678bc recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:55.168Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/release/project_release_conventions.md",
 "content": "---\nname: release-conventions-and-pitfalls\ndescription: Release worker codepaths, env vars, and pitfalls found building T-182 (Docker/README/HF/Replit)\nmetadata:\n  type: project\n---\n\nPaths: Dockerfile, .dockerignore (allow-list), run.sh, Makefile, .env.example, app/config.py, deploy/{HUGGINGFACE,REPLIT,TIMING}.md, deploy/hf_push.sh, deploy/replit/.replit.\n\nDemo mode = no ENABLE_LIVE=1 -> provider.backend_name() is always 'fixture' (D-020). Image env: HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR. App needs at runtime: app/, evals/golden, evals/library, evals/reports/calibration.json, tests/fixtures/llm.\n\n**Pitfalls**\n- Docker daemon was NOT running on the dev Mac (client only): docker build/run could not be verified; emulate with a venv and say so. Dev app owns :7860, board :7777/:8787/:4173: use other ports for tests.\n- tools/check_secrets.py flags even a placeholder `sk-ant-...` in .env.example; leave the value empty.\n- git-guard hook rejects `git add && git commit` in one Bash call (and blocks the whole command, so earlier parts of it do not run): add, then commit with a pathspec in separate calls.\n- macOS cp has no --parents; use git ls-files -z | tar --null -T -.\n- Replit python module name and deployment port rules are not in the fetched docs; flagged as unverified.\n"
}
````

### User / tool · 2026-11-02T21:05:55.217Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/release/project_release_conventions.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:05:56.067Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/release/MEMORY.md",
 "content": "- [Release conventions and pitfalls](project_release_conventions.md) — paths, demo-mode env, Docker-daemon gap, secret-scan and git-guard gotchas\n"
}
````

### User / tool · 2026-11-02T21:05:56.133Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/release/MEMORY.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:06:00.057Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py move --help 2>&1 | head -8"
}
````

### User / tool · 2026-11-02T21:06:00.183Z

**tool result**
````
usage: board.py move [-h] --agent AGENT [--note NOTE]
                     [--accept-debt ACCEPT_DEBT]
                     id status

positional arguments:
  id
  status
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:06:03.738Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py move T-182 in_review --agent release --note \"AC1 left unchecked: docker build/run not executed because no Docker daemon on this host; verified by emulation (see handoff, deploy/TIMING.md). All other AC1 parts met with evidence.\""
}
````

### User / tool · 2026-11-02T21:06:03.870Z

**tool result**
````
T-182: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:06:07.768Z

T-182 is in `in_review`, but `docker build` and `docker run` never ran. This host has only the Docker client and no daemon, so AC1 is left unchecked. I ran the same recipe without Docker instead: fresh Python 3.12 venv, the Dockerfile's environment, `/api/health` reporting demo mode, and the sample case reaching `ready`.

- **README path, timed:** a fresh `git clone` plus `./run.sh` took 17 s to a healthy server (21 s with the sample run), using a cold pip download. The timing is in `/Users/arsis/zlayt-pm-project/deploy/TIMING.md`.
- **Hosting docs:** I fetched and cited the current Hugging Face and Replit docs. The Replit `python-3.12` module name and its port rules aren't in those docs, so `deploy/REPLIT.md` marks them as unverified.
- **`.env.example`:** the secret-scan warning is fixed, and nothing is left staged. Commits are `ac678bc` and `f547db4`.

I also added `.dockerignore`, `Makefile`, `run.sh`, `app/config.py`, `deploy/hf_push.sh` and the Replit config. The remaining gap is running `make docker docker-run` on a host with Docker.
