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
  {"severity": "nit",
   "title": "Replit python module name still unconfirmed against Replit docs",
   "evidence": "deploy/replit/.replit:3-4: 'The python module name is NOT listed on that page ... pick Python 3.12 in the Replit UI if this line is rejected.' modules = [\"python-3.12\"]. Disclosed, not tested (no Replit account).",
   "why_it_matters": "A wrong module name makes the import step on Replit fail. The text already tells the reader the fallback, so this is low risk.",
   "fix": "Confirm the module string in the Replit UI once, or leave the disclosure as is.",
   "acceptance_test": "An import of the repo into Replit with the shipped .replit starts ./run.sh without an editor error."}
 ],
 "whats_right": [
  "Round-1 fixes verified from a clean clone: one-line live-config error (exit 1, 0 tracebacks), port-in-use one-liner (exit 3, no Serving line), make evals expected failure documented and printed, git status clean afterwards.",
  "The image recipe without claude_cli.py boots in demo mode and refuses live claude-cli with a one-line CONTRACT section 10 message; the base digest is the real current python:3.12-slim index.",
  "Cold-clone server start is about 12 s with no key and no .env; Python 3.9 gets a clear message; secrets stay out of the repo and the build context."
 ],
 "questions_for_chris": [
  "Do you want README.md:22 (golden-path step) held to the committed guided UI at each gate, or is the README allowed to lag T-181 while the guided home is a placeholder? As written, a fresh clone of HEAD cannot reach the sample case.",
  "Is /classic meant to stay reachable in demo mode until the guided UI is complete? T-177 r3 (2e58e18) redirects it to /, which removes the only working sample path."
 ]}
```
