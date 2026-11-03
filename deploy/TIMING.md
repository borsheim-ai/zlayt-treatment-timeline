# Timing: README run-from-clone path

Measured 2026-11-02 by the release worker (T-182), following README.md literally: `git clone` into an empty directory, then `./run.sh` (PORT=7872 only to avoid the dev server on 7860).

| Step | Time |
|---|---|
| `git clone` (local path) | 5 s |
| `./run.sh`: create `.venv`, `pip install -r requirements.txt` with `PIP_NO_CACHE_DIR=1` (wheels downloaded, not cached), start server, first `/api/health` ok | 12 s |
| Clone to a healthy server | 17 s |
| Plus: create the sample case, run it, read 9 entries / 10 flags back over the API | 21 s total |

Host: Apple-silicon Mac, Python 3.12.2, fast network. A slower network can add a minute or two; the README bar is under 5 minutes.
The clone was of the local repository, not a remote; clone time over the network is not included.

## Docker

The Docker daemon was not running on the host this was built on (docker client 29.9.2 present; no daemon, no buildx, no Colima/OrbStack), so `docker build` and `docker run` were NOT executed. The same recipe was run without Docker: the `.dockerignore` allow-list taken from tracked files, a fresh Python 3.12 venv from `requirements.txt`, the Dockerfile's `ENV` (`HOST=0.0.0.0 LLM_BACKEND=fixture FIXTURE_SET=curated`), `python -m app.main` -> `/api/health` `demo_mode: true`, sample case ran to `ready`. Run `make docker docker-run` on a machine with Docker to close this gap; the installer-reviewer can do it at the M4 gate.

## Round 2 emulation (T-182 r2, 2026-11-02): claude_cli.py excluded

Still no Docker daemon. The `.dockerignore` rules were applied to the tracked files of a fresh `git clone` (1425 files; `app/llm/backends/claude_cli.py` absent; only `anthropic_api.py`, `fixture.py` remain), a fresh Python 3.12.2 venv from `requirements.txt`, the Dockerfile's `ENV`: `import app.main, app.backend.api, app.llm.provider` ok; `python -m app.main` -> `/api/health` `demo_mode: true`, `backend: fixture`; sample case -> ready, 9 entries, 10 flags. `ENABLE_LIVE=1 LLM_BACKEND=claude-cli` in that tree exits 1 with one line (`error: LLM_BACKEND=claude-cli is not available in this build ...`), no traceback. `make docker docker-run` on a Docker host is still the open step (NEEDS_CHRIS).
