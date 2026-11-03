# Subagent: Release: T-182 round 3 fixes (Release: T-182 round 3 fixes)

Source: `agent-a4603f0d5db439b82.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:38:04.630Z

You are the release worker in /Users/arsis/zlayt-pm-project. Your card is T-182, round 3. Claim it with --force. Read reviews/T-182-installer-r2.md and the orchestrator's newest note on the card.

Fix two things only:
- the literal `<owner>` in the first README command: use a real clone instruction or a clear note;
- the "serving demo mode" warning that prints before the live-config error. Print only the error line.

The r2 blocker (`/` showing the unfinished guided UI) belongs to T-181, not you, so don't touch app/frontend or api.py. Verify from a fresh clone, commit only your paths through a temp index, and move the card to in_review. The orchestrator will re-run the installer walk after T-181 lands. Reply in 1 line.

### User / tool · 2026-11-02T21:38:04.635Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:08.110Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B claim T-182 --agent release --force; $B show T-182 | tail -40; cat reviews/T-182-installer-r2.md | head -80; cat .claude/agent-memory/release/project_release_conventions.md"
}
````

### User / tool · 2026-11-02T21:38:08.300Z

**tool result**
````
T-182 claimed by release
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: release
- 2026-11-02T21:00:24Z release: claimed
- 2026-11-02T21:03:21Z release: Dockerfile, .dockerignore, run.sh, Makefile, .env.example, app/config.py written. Docker daemon is NOT running on this host (client only, no buildx/colima/orbstack): docker build/run cannot be executed here. Verified the same image recipe by emulation: allow-listed tracked files, fresh py3.12 venv from requirements.txt (8s), Dockerfile ENV, python -m app.main on :7871 -> /api/health demo_mode true, sample case run -> ready, 9 entries, 10 flags. HF + Replit docs fetched; next: deploy docs, README, clone timing.
- 2026-11-02T21:06:03Z release: moved in_progress -> in_review: AC1 left unchecked: docker build/run not executed because no Docker daemon on this host; verified by emulation (see handoff, deploy/TIMING.md). All other AC1 parts met with evidence.
- 2026-11-02T21:06:15Z orchestrator: review dispatched: installer-reviewer
- 2026-11-02T21:25:55Z orchestrator: review installer-reviewer (claude-sonnet-5-5): changes — reviews/T-182-installer.md; round 1; findings:
    - [major] Live-mode misconfiguration prints a Python traceback at startup (opt-in path, no key, no spend-cap flag) — fix: In create_app (app/backend/api.py:112 area) or in app/main.py, catch the live-config RuntimeError and print one line naming the missing variable (PROVIDER_CAP_CONFIRMED=1), then exit non-zero without a traceback. Keep the README sentence that the server refuses to start.
    - [major] Docker path not executed: docker build and docker run are unverified (card AC1 still open) — fix: On a host with a Docker daemon, run make docker and make docker-run (or the two README commands) from a fresh clone. Save the build and run output to artifacts/review-evidence/ and record curl -fsS http://127.0.0.1:7860/api/health with demo_mode true.
    - [major] make evals, a documented command, exits 2 on a clean clone; the README does not say so — fix: Either (a) README.md:57 states that the fixture run cannot meet the ship bar by design, names the report it writes, and gives the expected exit status and what it means; or (b) the fixture run exits 0 and labels its result as not a ship measurement. The ship bar itself stays unchanged.
    - [minor] First Analyze click after a server starts is ignored (no POST /run); a second click works — fix: Frontend: keep Analyze disabled until the POST that creates the sample case resolves, or re-bind the handler after the preview is re-rendered (input.js around line 100 and the preview render). Owner: frontend.
    - [minor] README does not name the buttons for the sample case — fix: Replace the README sentence with: Click Use the sample case, then Analyze. You should see 9 records found, then 9 entries to decide.
    - [minor] No troubleshooting section; run.sh prints Serving on before the bind fails — fix: Print the Serving on line only after the bind succeeds, or print a neutral line. Add a short Troubleshooting section: port in use -> PORT=7870 ./run.sh; no Docker daemon -> start Docker Desktop or skip Docker; Python below 3.12 -> the run.sh message and PYTHON=/path/to/python3.12.
    - [minor] Placeholders without example values in copy-paste commands; Replit prerequisites incomplete — fix: Give example values (for example git clone https://github.com/<owner>/zlayt zlayt, with the real URL once it exists). List a GitHub account as a Replit prerequisite.
    - [minor] Normal use leaves untracked runtime files that .gitignore does not cover — fix: Add data/, *.sqlite and the evals fixture report outputs to .gitignore, or write them to an ignored directory. Decide explicitly which evals reports are committed.
    - [minor] Replit: HOST binding for the published run is not shown to be inherited; python module name unconfirmed — fix: Set the bind address where the deployment definitely reads it, or default HOST to 0.0.0.0 when REPL_ID is set. Confirm the module name against the current Replit page or the UI.
    - [minor] Dockerfile: floating base tag and a HEALTHCHECK hard-coded to port 7860 — fix: Pin the base image by digest and record the digest in the Dockerfile comment. Read PORT inside the HEALTHCHECK command.
- 2026-11-02T21:26:00Z orchestrator: Round 2 (release): F1 live-config error -> one line naming the missing variable, exit 1, no traceback (smallest hook in app/main.py or create_app; coordinate with the backend workers in api.py); F3 README states that the fixture make evals cannot meet the ship bar by design, with the exit status and report path; Q2 .dockerignore excludes app/llm/backends/claude_cli.py and the image still boots (CONTRACT §10); minors where cheap. F2 Docker: no daemon on this host -> stays on NEEDS_CHRIS (Chris runs make docker); accept as documented debt if nothing else is open. Q3: D-065 governs the label.
- 2026-11-02T21:26:00Z orchestrator: assigned: release
- 2026-11-02T21:26:08Z release: claimed
- 2026-11-02T21:30:54Z release: r2 fixed: F1 (app/main.py preflight + RuntimeError catch -> one 'error:' line, exit 1; fresh clone: 0 Traceback), F3 (README Tests and evals: runner exit 1, make exit 2, 3 blockers by design; Makefile prints the same; make evals now writes to data/evals so git status stays clean), Q2 (.dockerignore + hf_push.sh drop claude_cli.py; emulated allow-listed ctx + fresh venv: imports ok, demo_mode true, sample 9 entries/10 flags; live claude-cli in that tree -> one-line error), F5-F10, F12, F13. F4 (frontend first click) and F11 (404s) are not mine: need a frontend card. F2 Docker stays NEEDS_CHRIS (no daemon). Replit python-3.12 module name still unconfirmed in docs.
- 2026-11-02T21:30:56Z release: moved in_progress -> in_review: AC1 left unchecked: docker build/run not executed, no Docker daemon on this host (F2 stays on NEEDS_CHRIS); everything else in AC1 is met, verified by emulation, see handoff
- 2026-11-02T21:31:13Z orchestrator: review dispatched: installer-reviewer
- 2026-11-02T21:37:42Z orchestrator: review installer-reviewer (claude-sonnet-5-5): fail — reviews/T-182-installer-r2.md; round 2; findings:
    - [blocker] README golden path does not reach the sample case on committed HEAD: / is the unfinished guided scaffold and the buttons the README names are gone — fix: Before the M4 gate: (a) T-181 ships a guided Home / Step 1 that works in demo (non-local) mode without GET /api/cases and shows a start or Open the sample case control, then release updates README.md:22 to the exact guided labels 
    - [major] Docker path still not executed: docker build and docker run unverified (card AC1 open; Dockerfile changed in r2) — fix: On a host with a Docker daemon run make docker and make docker-run from a fresh clone; save output to artifacts/review-evidence/ and record curl -fsS http://127.0.0.1:7860/api/health with demo_mode true. Until then keep AC1 unchecked and the NEEDS_CHRIS entry.
    - [minor] First command in the README still contains a literal <owner> and a trailing comment, so it cannot be pasted as written — fix: Fill in the real repo URL when the public snapshot exists (T-194), or put the placeholder explanation in prose above the block and show one runnable line.
- 2026-11-02T21:37:42Z orchestrator: r2 blocker is the unfinished T-181 at / plus the T-177 /classic redirect (orchestrator instruction), not a release defect. Round 3 = re-run the installer walk after T-181 lands. Release meanwhile: replace the literal <owner> in the first README command with the real clone path or a clear note; silence the 'serving demo mode' line before the live-config error. F2 Docker = documented debt (AC1 unchecked, NEEDS_CHRIS open).
- 2026-11-02T21:38:01Z orchestrator: assigned: release
- 2026-11-02T21:38:08Z release: claimed

## Handoff
Changed: app/main.py (preflight + one-line errors, port-in-use exit 3, Serving line after bind), app/config.py (preflight, port_in_use), run.sh (HOST 0.0.0.0 on Replit), Makefile (evals to data/evals + expected-failure line), .dockerignore/hf_push.sh (claude_cli.py out of image), Dockerfile (base digest pin, PORT-aware healthcheck), .gitignore (/data, *.sqlite, latest.fixture.json), README (buttons, Tests and evals, Troubleshooting, example placeholders, heading), deploy docs. Commits c031483 fb48dda 18bfa69.
Verified from fresh git clone (cold venv): live opt-in w/o cap -> one error line, exit 1, 0 Traceback; ENABLE_LIVE=1 alone -> demo_mode true; port busy -> one line, exit 3, no Serving line; REPL_ID -> binds 0.0.0.0; make evals -> runner 1 / make 2, git status clean; emulated image (allow-list, no claude_cli.py): imports ok, demo true, sample 9/10.
Left: F2 docker build/run (no daemon; NEEDS_CHRIS: make docker docker-run); F4 first Analyze click and F11 404s need a frontend card; Replit module name unconfirmed.
Surprised: make evals runner exit is 1 (make exit 2), not 2 as the round-1 review said; a str.replace on .gitignore hit two lines.

# T-182 installer review, round 2: README run-from-clone, demo mode, Docker recipe, deploy docs

Verdict: **fail**. One new blocker: following the README on committed HEAD, the sample case cannot be reached, because `/` now serves the unfinished guided-UI scaffold. The round-1 fixes themselves check out (F1, F3, Q2, and the minors). F2 (Docker not executed) remains a major.

Cause of the blocker, to be fair to the card: the commits that broke the golden path are T-181 (f3d42a2, a placeholder guided UI at `/`) and T-177 r3 (2e58e18, `/classic` now redirects to `/`). T-182 r2 made it visible by rewriting the README to name buttons ("Use the sample case", "Analyze") that exist only on the old screen. That is still a defect on the install path at HEAD, and the rule is that I grade what a first-time installer experiences.

Timing (fresh `git clone` of HEAD 18bfa69 into an empty temp dir, `env -i`, spare port 7881):
- clone: 2 s; `./run.sh` cold venv + pip: server healthy within 10 s of the run.sh start (about 12 s server-side total). The healthy server reports `demo_mode: true`, `backend: fixture`, and the synthetic banner shows.
- Sample case visible: **never**. After the README's step 3 there is no "Use the sample case" button on the page (log section 2).
- Limits: local clone, not a network clone; headless Chromium. Elapsed wall time includes my tool-call gaps.

What I checked from your list:
- **F1 fixed.** `ENABLE_LIVE=1 LLM_BACKEND=anthropic-api`, no cap, no key: one line, `error: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 ...`, exit 1, 0 occurrences of "Traceback". `ENABLE_LIVE=1` with the cap set serves demo. Nit: the config JSON that prints just before the error carries a warning saying "serving demo mode", which contradicts the exit that follows.
- **F3 fixed.** `make evals` on the clone: runner exit 1, `make` exit 2, three `blocker:` lines, the Makefile line "the failure (runner exit 1) is EXPECTED", and README.md:29 says exactly this. 10 s. `git status --short` is empty afterwards.
- **Q2 holds.** Allow-list context from the clone has 0 `claude_cli.py` files; `app/llm/backends/` holds `__init__.py`, `anthropic_api.py`, `fixture.py`. Under the Dockerfile ENV the app boots, `demo_mode` true, sample run reaches 9 entries and 10 flags. `ENABLE_LIVE=1 LLM_BACKEND=claude-cli` there prints one line naming CONTRACT section 10, exit 1. `.dockerignore` line 5 comes after `!app/**`, so the rule order is right (not run through a real Docker engine).
- **F2 judgment.** Still a major. `docker info` fails with no daemon, so `docker build` and `docker run` are unverified, and the Dockerfile changed in r2 (digest pin, PORT-aware healthcheck). I checked the digest against Docker Hub: it is the current `python:3.12-slim` index and resolves. That reduces risk but does not replace a build. Acceptable as documented debt at the gate only on these conditions: AC1 stays unchecked, `submission/NEEDS_CHRIS.md` keeps the "Docker verification (T-182)" entry (it does, line 40), and the README's primary path (`./run.sh`) does not depend on Docker (it does not). The worker cannot fix it on this host, so it is a verification gap rather than a defect to rework.
- **Minors.** Port busy: one line plus `PORT=7870` hint, exit 3, no "Serving on" line (fixed). Python 3.9: clear message, exit 1. Troubleshooting section present. `.gitignore` covers `*.sqlite`, `/data/`, the fixture report. `run.sh:35` sets HOST 0.0.0.0 on `REPL_ID`. REPLIT.md names a GitHub account. Heading and make test duration fixed. Still open: README.md:14 keeps a literal `<owner>` in the first command (finding 3); the Replit module name is still unconfirmed, and honestly disclosed.

F4 and F11 not graded, as instructed. The 404 on `/api/cases` appears in the blocker's evidence only as the mechanism for the empty home screen.

```json
{"card": "T-182", "persona": "installer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git HEAD 18bfa69 of /Users/arsis/zlayt-pm-project (fresh clone into a temp dir; fix commits c031483, fb48dda, 18bfa69). App on http://127.0.0.1:7881 (spare port; 7860 is held by another process and left alone). Sample case: README says Use the sample case, then Analyze. No ANTHROPIC_API_KEY, no .env.",
 "exercised": [
  "git clone of HEAD into a mktemp dir; read README.md in full; read .dockerignore, Dockerfile, run.sh, deploy/REPLIT.md, deploy/replit/.replit, deploy/TIMING.md, submission/NEEDS_CHRIS.md, .gitignore",
  "env -i HOME PATH PORT=7881 ./run.sh from the fresh clone: healthy within 10 s of run.sh start (clone 2 s); /api/health demo_mode true (log section 1)",
  "Playwright headless Chromium against http://127.0.0.1:7881/: page shows Your cases / No cases yet, no sample button; console 404 on /api/cases; GET /new shows 'This step is not built yet'; /classic 307-redirects to / (log section 2; screenshots T-182-installer-r2-landing.png, T-182-installer-r2-new.png)",
  "read app/backend/api.py:272 (GET /api/cases is 404 outside local mode) and the committed guided home.js header ('PLACEHOLDER from the T-181 scaffold')",
  "F1: ENABLE_LIVE=1 LLM_BACKEND=anthropic-api with no cap and no key: one error line, exit 1, grep -c -i traceback = 0; with PROVIDER_CAP_CONFIRMED=1 and no key: serves demo (log section 3)",
  "F3: make evals in the clone: runner exit 1, make exit 2, three blocker lines, expected-failure line printed, 10 s; git status --short empty afterwards (log section 4)",
  "port busy on 7881 and on the literal default 7860: one-line error, exit 3, no Serving line; PYTHON=/usr/bin/python3 (3.9.6): clear message, exit 1 (log section 5)",
  "Q2: Dockerfile recipe emulated without a daemon (git archive allow-list context, claude_cli.py dropped per .dockerignore line 5, clone venv from requirements.txt, Dockerfile ENV): imports ok, /api/health demo_mode true, POST /api/cases sample then run: ready, 9 entries, 10 flags; live claude-cli in that tree: one-line error exit 1 (log section 6)",
  "docker info: no daemon (failed to connect to /var/run/docker.sock); docker build and docker run NOT executed. Checked the Dockerfile base digest against Docker Hub: matches the current python:3.12-slim index, manifest by digest HTTP 200 (log section 7)",
  "minors read in the clone: .gitignore lines 18-20, run.sh:35 REPL_ID host, REPLIT.md:14 GitHub prerequisite, README.md:14 placeholder (log section 8)",
  "stopped only my own PIDs (99085, 1981, 3641); lsof afterwards shows only PID 86899 on 7860 (not mine)"
 ],
 "verdict": "fail",
 "scores": {
  "readme_first_screen_and_fastest_path": 3,
  "prerequisites_explicit_with_versions": 5,
  "copy_pasteable_commands": 4,
  "clean_clone_commands_in_order": 4,
  "time_to_first_success_under_5_min": 1,
  "demo_mode_without_key_no_crash": 5,
  "env_example_and_no_secrets": 5,
  "url_port_and_expected_output_stated": 2,
  "one_step_sample_case_load_documented": 1,
  "docker_path_builds_and_runs": 2,
  "nondocker_path_pinned_and_reproducible": 5,
  "errors_and_troubleshooting": 5,
  "public_link_opens_with_banner": 3,
  "tests_and_evals_commands_work": 5,
  "no_undocumented_global_installs_or_accounts": 4,
  "rerun_works": 5
 },
 "findings": [
  {"severity": "blocker",
   "title": "README golden path does not reach the sample case on committed HEAD: / is the unfinished guided scaffold and the buttons the README names are gone",
   "evidence": "artifacts/review-evidence/T-182-installer-r2-log.txt section 2. Fresh clone of 18bfa69, ./run.sh, open http://127.0.0.1:7881/: body 'Your cases | No cases yet.', footer 'null'; buttons on the page are only 'Skip to the main content', 'Treatment Timeline', 'Dark mode'. Playwright: Locator.click: Timeout 30000ms exceeded waiting for get_by_text('Use the sample case'). GET /new body: 'Add your records ... This step is not built yet.' GET /classic -> 307 to /. Console: 404 http://127.0.0.1:7881/api/cases (app/backend/api.py:272 returns 404 when not local_mode, by design, so the home screen has no list to draw and shows no start or sample button). Committed app/frontend/guided/home.js line 1: 'PLACEHOLDER from the T-181 scaffold'. README.md:22 says: click Use the sample case, then Analyze; you should see '9 records found', then '9 entries to decide'. Screenshots T-182-installer-r2-landing.png and T-182-installer-r2-new.png.",
   "why_it_matters": "Persona section 5 dealbreakers: time to first success on the documented primary path cannot be reached, and the README's golden-path step 3 describes UI that is not on screen. A reviewer following the README sees an empty page with no way forward within the 5-minute budget. Server startup, demo mode and the banner are fine; the failure is what the browser shows. Cause is outside the release files (T-181 in progress, T-177 r3 /classic redirect), but the README is the artifact under review and it is wrong at HEAD.",
   "fix": "Before the M4 gate: (a) T-181 ships a guided Home / Step 1 that works in demo (non-local) mode without GET /api/cases and shows a start or Open the sample case control, then release updates README.md:22 to the exact guided labels and strings; or (b) until then, keep a working sample path reachable from the README (for example /classic served in demo mode) and say so. Release owns the README wording; frontend owns the page. Re-run this review from a fresh clone after T-181 is committed.",
   "acceptance_test": "Fresh clone, env -i, ./run.sh, open http://127.0.0.1:PORT/: a Playwright script reaches the sample case results using only the labels the README names, within 60 s of the server being healthy, with no 4xx on page load; README.md names those labels and the expected counts verbatim."},
  {"severity": "major",
   "title": "Docker path still not executed: docker build and docker run unverified (card AC1 open; Dockerfile changed in r2)",
   "evidence": "docker info: failed to connect to the docker API at unix:///var/run/docker.sock ... no such file or directory (log section 7). Card T-182 AC1 done=false. deploy/TIMING.md Docker sections: docker build and docker run NOT executed. Emulation passes (log section 6: 1486 context files, 0 claude_cli.py, demo_mode true, sample 9 entries / 10 flags). Base digest sha256:b18b261e... is the current python:3.12-slim index on Docker Hub (HTTP 200). submission/NEEDS_CHRIS.md:40 'Docker verification (T-182)' tracks it.",
   "why_it_matters": "Checklist item 10 and card AC1 require a real docker build and docker run serving :7860 in demo mode. The emulation is strong evidence but the digest pin, the PORT-aware HEALTHCHECK and the allow-list were not exercised by a build. Judgment on the debt: a verification gap the worker cannot close on this host, so it can stay as documented debt at the gate with AC1 unchecked and the NEEDS_CHRIS entry open. It is not downgraded, because nobody has evidence yet that the image builds.",
   "fix": "On a host with a Docker daemon run make docker and make docker-run from a fresh clone; save output to artifacts/review-evidence/ and record curl -fsS http://127.0.0.1:7860/api/health with demo_mode true. Until then keep AC1 unchecked and the NEEDS_CHRIS entry.",
   "acceptance_test": "docker build -t zlayt-demo . exits 0; docker run --rm -p 7860:7860 zlayt-demo serves /api/health demo_mode true and docker inspect reports healthy; with -e PORT=7870 -p 7870:7870 it also reports healthy."},
  {"severity": "minor",
   "title": "First command in the README still contains a literal <owner> and a trailing comment, so it cannot be pasted as written",
   "evidence": "README.md:14: git clone https://github.com/<owner>/zlayt.git zlayt && cd zlayt     # <owner> = the GitHub account that hosts this repo; a local path works too: ... The shell treats <owner> as a redirect, so the command errors before cloning.",
   "why_it_matters": "Checklist 3: every command copy-pasteable. The reader's very first step fails, and the only workaround is in a comment on the same line.",
   "fix": "Fill in the real repo URL when the public snapshot exists (T-194), or put the placeholder explanation in prose above the block and show one runnable line.",
   "acceptance_test": "Paste the first README command block into a clean shell: it clones and enters the directory with no edits."},
  {"severity": "nit",
   "title": "Startup prints 'serving demo mode' warning right before a live-config error that exits",
   "evidence": "Log section 3: config JSON ends with warning 'ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.' followed by 'error: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 ...' and exit 1.",
   "why_it_matters": "The first message says the server will serve demo; the next says it refuses to start. A first-time reader may not know which to believe.",
   "fix": "Run the live-config check before printing the resolved-config warnings, or drop the demo warning when the next step is an error exit.",
   "acceptance_test": "Same env as section 3: output contains the one error line and no 'serving demo mode' warning."},
---
name: release-conventions-and-pitfalls
description: Release worker codepaths, env vars, and pitfalls found building T-182 (Docker/README/HF/Replit)
metadata:
  type: project
---

Paths: Dockerfile, .dockerignore (allow-list), run.sh, Makefile, .env.example, app/config.py, deploy/{HUGGINGFACE,REPLIT,TIMING}.md, deploy/hf_push.sh, deploy/replit/.replit.

Demo mode = no ENABLE_LIVE=1 -> provider.backend_name() is always 'fixture' (D-020). Image env: HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR. App needs at runtime: app/, evals/golden, evals/library, evals/reports/calibration.json, tests/fixtures/llm.

**Pitfalls**
- Docker daemon was NOT running on the dev Mac (client only): docker build/run could not be verified; emulate with a venv and say so. Dev app owns :7860, board :7777/:8787/:4173: use other ports for tests.
- tools/check_secrets.py flags even a placeholder `sk-ant-...` in .env.example; leave the value empty.
- git-guard hook rejects `git add && git commit` in one Bash call (and blocks the whole command, so earlier parts of it do not run): add, then commit with a pathspec in separate calls.
- macOS cp has no --parents; use git ls-files -z | tar --null -T -.
- Replit python module name and deployment port rules are not in the fetched docs; flagged as unverified.
- git-guard also rejects `git commit` chained with ANY other command (`;` or `&&`) and dislikes complex quoting/`$(...)` in long one-liners: one command per call, helper scripts in the scratchpad. pkill by pattern is blocked: use `kill $!`.
- Startup errors live in app/main.py (preflight + `except RuntimeError` -> `error: ...` one line, exit 1; port busy exit 3; `ZLAYT_DEBUG=1` gives the traceback); helpers in app/config.py. Do not touch api.py (backend owns it).
- `.dockerignore` excludes app/llm/backends/claude_cli.py (CONTRACT §10); hf_push.sh rm's it too; provider imports it lazily so demo works; config.preflight gives a one-line error if live claude-cli is asked for without it.
- `make evals`: runner exits 1, make exits 2; it is expected on fixture. Output goes to data/evals (git-ignored) so a clean clone stays clean. Emulate the image with a .dockerignore matcher script (last match wins) over `git ls-files` of a fresh clone + fresh venv.
- Replit: REPL_ID is documented; python-3.12 module name and PORT/host rules for deployments still unconfirmed in docs.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:11.405Z

**tool call — Bash**
````
{
 "command": "sed -n 5,30p README.md; grep -n \"demo mode\\|serving demo\" app/config.py app/main.py; git remote -v; git log --oneline | head -3; git status --short | head"
}
````

### User / tool · 2026-11-02T21:38:11.711Z

**tool result**
````
**Synthetic data only.** The app shows a banner and refuses text it has not seen in demo mode. Never paste real patient or client records.

How the work is split: language and judgment (summaries, "is this supported by the quote?") are LLM steps; dates, gap arithmetic, substring checks, currency totals, dedupe and export are plain code. Each LLM output passes a code check, then an independent judge, then a human accept / edit / dismiss. The table is in [`docs/LLM_VS_CODE.md`](docs/LLM_VS_CODE.md).

## Run it from a clone (under a minute on a fast network, no key)

Needs Python 3.12+ and git. Docker is optional.

```
git clone https://github.com/<owner>/zlayt.git zlayt && cd zlayt     # <owner> = the GitHub account that hosts this repo; a local path works too: git clone /path/to/zlayt zlayt
./run.sh
```

Open <http://127.0.0.1:7860>. The first run creates `.venv` and installs `requirements.txt` (the only slow step); later runs start in seconds. Use another port with `PORT=7870 ./run.sh`.

Timed 2026-11-02 from a fresh `git clone` into an empty directory: 17 s to a healthy server with a cold pip download (Apple-silicon Mac, Python 3.12.2, fast network; details in [`deploy/TIMING.md`](deploy/TIMING.md)). Budget a few minutes on a slow network.

Then: click **Use the sample case**, then **Analyze**. You should see "9 records found", then "9 entries to decide". Each timeline entry shows its exact excerpt; flags (gaps, conflicts, unclear charges) show their evidence; Accept / Edit / Dismiss decides what the export contains.

Equivalent commands: `make run`, `make test`, `make evals`, `make config` (prints the resolved mode; never prints a key).

### Tests and evals

- `make test` runs the unit tests (several minutes; about 6 on a shared laptop). Exit 0 means all passed.
- `make evals` scores the golden set on the **fixture backend** and writes `data/evals/<timestamp>.md` (git-ignored; the committed `evals/reports/` are left alone). **It fails on a clean clone, and that is expected, not a defect** (the runner exits 1, so `make` prints `Error 1` and exits 2; the last lines name three `blocker:` items): the ship bar includes metrics that need live model runs (3-run determinism, the judge's seeded-error controls), and a fixture run cannot measure them, so the report says `ship_bar_met=False` and lists those as blockers by design. The Makefile prints a line saying so. Read the report's table for the numbers the fixture run can check (dates, gaps, totals, grounding); the ship-bar result comes from a live run, recorded in `evals/reports/latest.json`.

app/config.py:23:        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
app/config.py:46:                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
6904b41 feat(release): T-194 deploy/make_public_snapshot.sh builds a redacted single-commit public snapshot from git archive HEAD
6d6dc45 fix(submission): T-185/T-186 r3 library numbers cite only library-latest.md; counts computed at 18bfa69 with re-run commands; D-065 wording, CHRIS marker, card refs
18bfa69 docs(release): T-182 r2 timing note for the claude_cli-excluded image emulation
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:13.667Z

No remote exists, so I'll make the first command a runnable local-path clone with a clear note in prose. Next, the config/main code.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:14.146Z

**tool call — Bash**
````
{
 "command": "sed -n 1,70p app/config.py; grep -n \"warn\\|preflight\\|config\" app/main.py"
}
````

### User / tool · 2026-11-02T21:38:14.230Z

**tool result**
````
"""Runtime configuration, read-only. One place that says which mode the process is in and why; never returns or prints a secret.

`python -m app.config` prints the resolved settings (a key is reported only as set / not set). The Dockerfile, run.sh and the Makefile
use it as a startup self-check. The rules themselves live where they are enforced (app.llm.provider.backend_name, app.backend.store.live_enabled);
this module calls those so there is one definition of "live".
"""
import importlib.util
import json
import os
import socket

DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}


def resolved() -> dict:
    from app.backend import store
    from app.llm import provider
    live = store.live_enabled()
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    backend = provider.backend_name()
    warnings = []
    if os.environ.get("ENABLE_LIVE") == "1" and not live:
        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
        warnings.append("LLM_BACKEND is set but ENABLE_LIVE is not 1: the fixture backend is used (no model call is possible).")
    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        warnings.append("Live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a spend limit at the provider first); the server will refuse to start.")
    return {
        "mode": "live" if live else "demo",
        "backend": backend,
        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
        "anthropic_api_key": "set" if key_set else "not set",
        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
        "warnings": warnings,
    }


def preflight() -> str | None:
    """One-line reason the server cannot start in the configured mode, or None. Called by app.main before create_app so a misconfigured
    live opt-in prints one line naming the variable instead of a traceback. The cap/host rules themselves stay in create_app (it still raises)."""
    from app.llm import provider
    if provider.backend_name() == "claude-cli" and importlib.util.find_spec("app.llm.backends.claude_cli") is None:
        return ("LLM_BACKEND=claude-cli is not available in this build (the Docker image does not ship the CLI backend, CONTRACT section 10): "
                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
    return None


def port_in_use(host: str, port: int) -> bool:
    """True when something is already listening on host:port (same SO_REUSEADDR setting uvicorn binds with)."""
    with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
        except OSError:
            return True
    return False


if __name__ == "__main__":
    print(json.dumps(resolved(), indent=2))
3:A startup misconfiguration (live opt-in without PROVIDER_CAP_CONFIRMED=1, a port already in use, ...) prints one line naming the
24:    from app import config
26:    why = config.preflight()
31:    except RuntimeError as e:                         # create_app's configuration refusals (cap flag, local-mode host); each message names the variable
35:    if config.port_in_use(host, port):
38:    uvicorn.run(app, host=host, port=port, access_log=False, log_level="warning")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:19.661Z

**tool call — Bash**
````
{
 "command": "cat run.sh; sed -n 15,45p app/main.py"
}
````

### User / tool · 2026-11-02T21:38:19.751Z

**tool result**
````
#!/bin/sh
# One command from a fresh clone to the guided UI in demo mode (no key, no network after the one-time install).
#   ./run.sh                 demo mode on http://127.0.0.1:7860   (PORT=7870 ./run.sh to change the port)
#   ./run.sh setup           create .venv and install requirements only
#   ./run.sh test            run the unit tests (installs requirements-dev.txt first)
# Live mode is opt-in: see README.md and .env.example. This script never reads or prints .env.
set -eu
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
  echo "Python 3.12+ is required (found: $("$PY" --version 2>&1)). Install it, or set PYTHON=/path/to/python3.12." >&2
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "Creating .venv and installing requirements (one time, about a minute)..."
  "$PY" -m venv .venv
fi
# Reinstall only when requirements.txt changed since the last successful install.
if [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then
  .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt
  touch .venv/.installed
fi

case "${1:-serve}" in
  setup)
    echo "Ready: .venv installed." ;;
  test)
    .venv/bin/pip install --quiet --disable-pip-version-check -r requirements-dev.txt
    exec .venv/bin/python -m pytest tests/unit -q ;;
  serve)
    # Demo defaults; a value you already exported wins.
    # On Replit (REPL_ID is set) the preview/published URL only reaches a process bound to 0.0.0.0.
    if [ -z "${HOST:-}" ] && [ -n "${REPL_ID:-}" ]; then HOST=0.0.0.0; fi
    export LLM_BACKEND="${LLM_BACKEND:-fixture}" FIXTURE_SET="${FIXTURE_SET:-curated}" HOST="${HOST:-127.0.0.1}" PORT="${PORT:-7860}"
    .venv/bin/python -m app.config
    # app.main prints "Serving on ..." once the port is free; a startup error is one line, not a traceback.
    exec .venv/bin/python -m app.main ;;
  *)
    echo "usage: ./run.sh [serve|setup|test]" >&2; exit 2 ;;
esac
    return create_app()


def _fail(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def main():
    from app import config
    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
    why = config.preflight()
    if why:
        _fail(why)
    try:
        app = create()
    except RuntimeError as e:                         # create_app's configuration refusals (cap flag, local-mode host); each message names the variable
        if os.environ.get("ZLAYT_DEBUG") == "1":
            raise
        _fail(str(e))
    if config.port_in_use(host, port):
        _fail(f"port {port} on {host} is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).", 3)
    print(f"Serving on http://{host}:{port}  (Ctrl-C to stop)", flush=True)
    uvicorn.run(app, host=host, port=port, access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:23.285Z

**tool call — Bash**
````
{
 "command": "env ENABLE_LIVE=1 LLM_BACKEND=anthropic-api PORT=7899 .venv/bin/python -m app.config | tail -8; env ENABLE_LIVE=1 LLM_BACKEND=anthropic-api PORT=7899 .venv/bin/python -m app.main; echo exit $?; grep -n \"PROVIDER_CAP\" -B6 app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T21:38:23.886Z

**tool result**
````
  "host": "127.0.0.1",
  "port": 7899,
  "anthropic_api_key": "not set",
  "local_mode": false,
  "warnings": [
    "ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode."
  ]
}
error: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)
exit 1
107-    rejudging = set()
108-    _boot = DB.connect(db_path)
109-    try:
110-        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
111-    finally:
112-        _boot.close()
113:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
114:        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:34.945Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && python3 - <<'EOF'\np='app/config.py'\ns=open(p).read()\ns=s.replace('''    from app.llm import provider\n    if provider.backend_name() == \"claude-cli\"''','''    from app.llm import provider\n    if os.environ.get(\"LLM_BACKEND\") == \"anthropic-api\" and os.environ.get(\"ENABLE_LIVE\") == \"1\" and os.environ.get(\"PROVIDER_CAP_CONFIRMED\") != \"1\":\n        return \"live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)\"\n    if provider.backend_name() == \"claude-cli\"''')\ns=s.replace('''if __name__ == \"__main__\":\n    print(json.dumps(resolved(), indent=2))''','''if __name__ == \"__main__\":\n    import sys\n    why = preflight()\n    if why:                                           # same refusal app.main makes: print only the error line, not a config dump with a contradicting warning\n        print(f\"error: {why}\", file=sys.stderr)\n        sys.exit(1)\n    print(json.dumps(resolved(), indent=2))''')\nopen(p,'w').write(s)\np='README.md'\ns=open(p).read()\nold=[l for l in s.split('\\n') if l.startswith('git clone https://github.com/<owner>')][0]\nnew='git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'\ns=s.replace('```\\n'+old+'\\n./run.sh\\n```','''Replace `OWNER` with the GitHub account that hosts the repo (the public link is in the submission email), or clone from the folder you were given: `git clone /path/to/zlayt zlayt`.\n\n```\ngit clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt\n./run.sh\n```''')\nopen(p,'w').write(s)\nEOF\ngit diff --stat -- README.md app/config.py; sed -n 10,20p README.md"
}
````

### User / tool · 2026-11-02T21:38:34.947Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:42.607Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/config.py'\ns=open(p).read()\ns=s.replace('''    from app.llm import provider\n    if provider.backend_name() == \"claude-cli\"''','''    from app.llm import provider\n    if os.environ.get(\"LLM_BACKEND\") == \"anthropic-api\" and os.environ.get(\"ENABLE_LIVE\") == \"1\" and os.environ.get(\"PROVIDER_CAP_CONFIRMED\") != \"1\":\n        return \"live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)\"\n    if provider.backend_name() == \"claude-cli\"''')\ns=s.replace('''if __name__ == \"__main__\":\n    print(json.dumps(resolved(), indent=2))''','''if __name__ == \"__main__\":\n    import sys\n    why = preflight()\n    if why:                                           # same refusal app.main makes: print only the error line, not a config dump with a contradicting warning\n        print(f\"error: {why}\", file=sys.stderr)\n        sys.exit(1)\n    print(json.dumps(resolved(), indent=2))''')\nopen(p,'w').write(s)\np='README.md'\ns=open(p).read()\nold=[l for l in s.split('\\n') if l.startswith('git clone https://github.com/<owner>')][0]\ns=s.replace('```\\n'+old+'\\n./run.sh\\n```','''Replace `OWNER` with the GitHub account that hosts the repo (the link is in the submission email), or clone from the folder you were given with `git clone /path/to/zlayt zlayt`.\n\n```\ngit clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt\n./run.sh\n```''')\nopen(p,'w').write(s)\nEOF\ngit diff --stat -- README.md app/config.py; sed -n 10,20p README.md; grep -n \"<owner>\" README.md deploy/*.md"
}
````

### User / tool · 2026-11-02T21:38:42.749Z

**tool result**
````
 README.md     | 4 +++-
 app/config.py | 7 +++++++
 2 files changed, 10 insertions(+), 1 deletion(-)

Needs Python 3.12+ and git. Docker is optional.

Replace `OWNER` with the GitHub account that hosts the repo (the link is in the submission email), or clone from the folder you were given with `git clone /path/to/zlayt zlayt`.

```
git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt
./run.sh
```

Open <http://127.0.0.1:7860>. The first run creates `.venv` and installs `requirements.txt` (the only slow step); later runs start in seconds. Use another port with `PORT=7870 ./run.sh`.
deploy/REPLIT.md:14:1. Replit -> **Create App** -> **Import from GitHub** -> paste this repo's URL (for example `https://github.com/<owner>/zlayt`; needs a Replit account and a GitHub account that can see the repo).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:45.857Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXX) && git read-tree HEAD && git add README.md app/config.py && git diff --cached --name-only && python3 tools/check_secrets.py --staged; git commit -q -m \"fix(release): T-182 r3 README first command has no angle-bracket placeholder; live-config error prints one line with no demo-mode warning\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- README.md app/config.py; git log --oneline | head -1; git show --stat HEAD | tail -4"
}
````

### User / tool · 2026-11-02T21:38:45.940Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXX) && git read-tree HEAD && git add README.md app/config.py && git diff --cached --name-only && python3 tools/check_secrets.py --staged
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:47.589Z

Separate commands via a helper script in the scratchpad.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:50.037Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo $S/idx > $S/idxpath && rm -f $S/idx && GIT_INDEX_FILE=$S/idx git read-tree HEAD && GIT_INDEX_FILE=$S/idx git add README.md app/config.py && GIT_INDEX_FILE=$S/idx git diff --cached --name-only"
}
````

### User / tool · 2026-11-02T21:38:51.218Z

**tool result**
````
README.md
app/config.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:52.323Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && GIT_INDEX_FILE=$S/idx python3 tools/check_secrets.py --staged"
}
````

### User / tool · 2026-11-02T21:38:52.480Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:56.182Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && GIT_INDEX_FILE=$S/idx git commit -q -m \"fix(release): T-182 r3 README first command has no angle-bracket placeholder; live-config error prints one line with no demo-mode warning\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- README.md app/config.py; git log --oneline | head -1; git show --stat HEAD | tail -4"
}
````

### User / tool · 2026-11-02T21:39:02.995Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
85bcd22 fix(release): T-182 r3 README first command has no angle-bracket placeholder; live-config error prints one line with no demo-mode warning

 README.md     | 4 +++-
 app/config.py | 7 +++++++
 2 files changed, 10 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:06.797Z

Verify from a fresh clone.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:08.115Z

**tool call — Bash**
````
{
 "command": "D=$(mktemp -d) && git clone -q . $D/zlayt && cd $D/zlayt && git log --oneline | head -1 && (ENABLE_LIVE=1 LLM_BACKEND=anthropic-api PORT=7899 timeout 120 ./run.sh >out.txt 2>&1; echo exit $?; cat out.txt; grep -ci \"traceback\\|serving demo\" out.txt); (PORT=7898 timeout 8 ./run.sh 2>&1 | tail -3; true)"
}
````

### User / tool · 2026-11-02T21:39:10.503Z

**tool result**
````
85bcd22 fix(release): T-182 r3 README first command has no angle-bracket placeholder; live-config error prints one line with no demo-mode warning
exit 127
/bin/bash: timeout: command not found
0
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:13.127Z

**tool call — Bash**
````
{
 "command": "D=$(ls -dt /var/folders/*/*/T/tmp.*/zlayt /tmp/tmp.*/zlayt 2>/dev/null | head -1); echo $D; cd $D && (ENABLE_LIVE=1 LLM_BACKEND=anthropic-api PORT=7899 ./run.sh >out.txt 2>&1; echo exit $?; cat out.txt; grep -ci \"traceback\\|serving demo\" out.txt); (PORT=7898 ./run.sh >ok.txt 2>&1 & P=$!; sleep 6; curl -fsS http://127.0.0.1:7898/api/health; echo; kill $P; head -3 ok.txt)"
}
````

### User / tool · 2026-11-02T21:39:28.242Z

**tool result**
````
/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/tmp.MvlkpZ6AGz/zlayt
exit 1
Creating .venv and installing requirements (one time, about a minute)...
error: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)
0
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
{
  "mode": "demo",
  "backend": "fixture",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:32.461Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B note T-182 --agent release --text \"r3: README first command now a runnable line (OWNER placeholder explained in prose above; no repo remote exists yet, T-194 fills the URL); config preflight shared so 'python -m app.config' prints only the 'error:' line (no demo-mode warning, no JSON) for the live opt-in without PROVIDER_CAP_CONFIRMED. Fresh clone of 85bcd22: exit 1, 0 traceback, 0 'serving demo' lines; plain ./run.sh healthy demo_mode true. Not touched: T-181 / frontend / api.py. F2 Docker stays NEEDS_CHRIS.\" ; $B commit T-182 --sha 85bcd22 --agent release; $B handoff T-182 --agent release --text \"r3 changed: README.md first clone command (OWNER placeholder explained in prose), app/config.py (preflight shared with the cap rule; python -m app.config prints only the error line). Verified from fresh clone of 85bcd22: live opt-in w/o cap -> one error line, exit 1, 0 traceback/'serving demo'; plain run.sh healthy demo_mode true. Left: re-run installer walk after T-181 lands; README sample-case labels may need updating then; F2 Docker (NEEDS_CHRIS). Surprised: the demo warning came from run.sh's separate config dump, not app.main.\"; $B move T-182 in_review --agent release"
}
````

### User / tool · 2026-11-02T21:39:32.757Z

**tool result (error)**
````
Exit code 2
noted on T-182
T-182: commit 85bcd22 recorded
handoff written on T-182
board.py: error: AC [1] unchecked; check them with evidence or give --note explaining
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:35.918Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py move T-182 in_review --agent release --note \"AC1 unchecked: docker build/run not executed, no Docker daemon on this host (F2 stays on NEEDS_CHRIS); rest met, see handoff\""
}
````

### User / tool · 2026-11-02T21:39:36.055Z

**tool result**
````
T-182: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:42.173Z

T-182 r3 is in_review (commit 85bcd22): the README's first command is now a runnable `git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt` with the `OWNER` note in prose above it, and the live-config failure prints only the `error:` line (exit 1). From a fresh clone it shows 0 tracebacks and 0 "serving demo" lines, and plain `./run.sh` still serves `demo_mode: true`. No repo remote exists yet, so `OWNER` stays a placeholder until T-194 gives a real URL. I didn't touch the frontend or api.py. AC1 (Docker build/run) stays unchecked and open on NEEDS_CHRIS because this host has no Docker daemon.
