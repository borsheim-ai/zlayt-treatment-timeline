# T-182 installer review: README run-from-clone, demo mode, Docker recipe, HF/Replit instructions

Verdict: **changes**. No blockers. Three majors: a live-mode startup traceback, the Docker path not executed (no daemon on this host), and `make evals` exiting 2 on a documented command.

Timing (fresh `git clone` into an empty temp dir, `env -i` clean environment, README path on spare port 7871):
- clone: 1 s (local path)
- `./run.sh` creates `.venv`, installs pins, server healthy: **12 s** from clone start
- Sample case visible in the browser (9 entries, 10 flags, 2 charges, 2 unclear amounts): **17 s** from clone start, including one lost first click that cost about 3 s
- Limits: local clone, not a network clone; headless Chromium driven by Playwright, so a human would add reading time. Well under the 5-minute bar.

Demo mode with no key and no `.env` works: `/api/health` reports `demo_mode: true`, the synthetic banner shows, and the sample case runs. The Docker half is not verified on a real daemon (finding 2).

Findings in order: F1 major live-mode traceback; F2 major Docker not executed; F3 major `make evals` exit 2 undocumented; F4 to F10 minor; F11 to F13 nit. Each has its evidence in `artifacts/review-evidence/T-182-installer-log.txt` (section numbers below) or the screenshots in `artifacts/review-evidence/T-182-installer-0*.png`.

Scope note for F1: the §8 calibration test for the crash-without-key blocker (empty environment reaches the sample case) passes, and the traceback needs an explicit live opt-in with the spend-cap flag missing. I rated it major, not blocker. If the orchestrator reads §5 literally it becomes a blocker; see questions_for_chris.

Out of my lens: the Docker image ships `app/llm/backends/claude_cli.py`, which is inert in fixture mode, while CONTRACT §10 says the image never includes the CLI backend. I did not grade that.

What I exercised (details in the JSON `exercised` list): clean clone and README read; `run.sh` run, re-run, and literal default-port run; Python 3.9 guard; `make config`; live-mode startup with three env combinations; Playwright walk of the sample case with screenshots; Dockerfile emulation (allow-listed context, fresh py3.12 venv, Dockerfile ENV, health and sample walk); `make test`; `make evals`; `git status` after the runs; `.gitignore`; deploy/ docs and scripts; HF and Replit docs fetched and checked.

```json
{"card": "T-182", "persona": "installer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 9199b72 of /Users/arsis/zlayt-pm-project (fresh clone into a temp dir; card commits f547db4, ac678bc). App on http://127.0.0.1:7871 (spare port; 7860 is held by a non-reviewer process, left alone). Sample case: Use the sample case, then Analyze. No ANTHROPIC_API_KEY, no .env.",
 "exercised": [
  "git clone of HEAD into a scratchpad temp dir; read README.md in full, then run.sh, Makefile, requirements.txt, .env.example, Dockerfile, .dockerignore, run.sh-referenced files, app/config.py via make config",
  "fresh clone, env -i (HOME, PATH only), PORT=7871 ./run.sh: healthy after 12 s from clone start (artifacts/review-evidence/T-182-installer-log.txt section 1-3)",
  "Playwright headless Chromium walk: landing, Use the sample case, Analyze, Accept/Edit/Dismiss visible, counts 9 entries / 10 flags / 2 charges / 2 unclear amounts; sample visible at 17 s from clone start (section 4; screenshot T-182-installer-02-sample-results-clean-clone.png)",
  "re-run in the same clone (kill own listener only, run ./run.sh again): healthy in 1 s, no .venv re-creation (section 5)",
  "literal README run on default port 7860 while another process holds it: bind error captured, exit 3, own child only stopped (section 6)",
  "PYTHON=/usr/bin/python3 ./run.sh (Python 3.9.6): clear message, exit 1 (section 7)",
  "make config (README command): mode demo, key not set (section 8)",
  "live opt-in with no spend-cap flag and no key: RuntimeError traceback at startup, exit 1 (section 9); cap set and no key: demo served with a message (section 10); ENABLE_LIVE=1 alone: demo_mode true (section 11)",
  "Dockerfile recipe emulated without a daemon: git archive of the .dockerignore allow-list (1411 files, 0 forbidden), cold pip install into a fresh py3.12 venv (11 s), HOST=0.0.0.0 PORT=7873 LLM_BACKEND=fixture FIXTURE_SET=curated, /api/health demo_mode true, sample case walked (section 12)",
  "docker info: daemon not running (failed to connect to /var/run/docker.sock); docker build and docker run NOT executed",
  "make test: 5801 passed, 2 skipped in 386.90 s on a shared host (section 13)",
  "make evals: exit 2, ship_bar_met=False, three blocker lines, make Error 1 (section 14)",
  "git status in the clone after README path, make test and make evals: untracked data/zlayt.sqlite and evals/reports outputs (section 15); .gitignore lines 16-17 read",
  "static checks: tracked .env files (only .env.example), key-shaped strings in tracked files (none), deploy/HUGGINGFACE.md, deploy/hf_push.sh, deploy/hf_space_frontmatter.yml, deploy/REPLIT.md, deploy/replit/.replit, deploy/TIMING.md read",
  "HF docs fetched (spaces-config-reference, spaces-sdks-docker): app_port default 7860 for docker SDK, sdk docker, container runs as user ID 1000, all match deploy/ text. Replit docs fetched (configuring-repl, deployment-types): localPort/externalPort and deployment run/deploymentTarget match; [run.env] documented for the Run command only; python-3.12 module name not confirmed (section 16)",
  "console and network check on load and after Use the sample case: GET /api/cases and GET /api/library return 404, favicon.ico 404 (section 17)",
  "first-click check: on 5 of 5 first walks on a newly started server, the first Analyze click produced no POST /run within 3 s; a second click worked; 0 of 13 later walks on a warm server needed a retry (screenshot T-182-installer-03-first-analyze-click-lost.png; section 4)"
 ],
 "verdict": "changes",
 "scores": {
  "readme_first_screen_and_fastest_path": 4,
  "prerequisites_explicit_with_versions": 4,
  "copy_pasteable_commands": 3,
  "clean_clone_commands_in_order": 5,
  "time_to_first_success_under_5_min": 5,
  "demo_mode_without_key_no_crash": 5,
  "env_example_and_no_secrets": 4,
  "url_port_and_expected_output_stated": 3,
  "one_step_sample_case_load_documented": 4,
  "docker_path_builds_and_runs": 2,
  "nondocker_path_pinned_and_reproducible": 5,
  "errors_and_troubleshooting": 2,
  "public_link_opens_with_banner": 3,
  "tests_and_evals_commands_work": 2,
  "no_undocumented_global_installs_or_accounts": 3,
  "rerun_works": 5
 },
 "findings": [
  {"severity": "major",
   "title": "Live-mode misconfiguration prints a Python traceback at startup (opt-in path, no key, no spend-cap flag)",
   "evidence": "artifacts/review-evidence/T-182-installer-log.txt section 9: ENABLE_LIVE=1 LLM_BACKEND=anthropic-api, no key, PROVIDER_CAP_CONFIRMED unset; output ends with RuntimeError: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020) raised from app/backend/api.py:112 under a full traceback; exit 1. Clean behaviour for comparison: section 10 (cap set, no key: demo served with a one-line message) and section 11 (ENABLE_LIVE=1 alone: demo wins).",
   "why_it_matters": "deploy/HUGGINGFACE.md:46-47 and deploy/REPLIT.md tell an operator to set these live variables on a Space or Replit. A wrong variable then shows a traceback in the logs instead of one line naming the missing setting. The demo path itself is clean. Scope: opt-in only, see the scope note above.",
   "fix": "In create_app (app/backend/api.py:112 area) or in app/main.py, catch the live-config RuntimeError and print one line naming the missing variable (PROVIDER_CAP_CONFIRMED=1), then exit non-zero without a traceback. Keep the README sentence that the server refuses to start.",
   "acceptance_test": "env -i HOME=$HOME PATH=$PATH ENABLE_LIVE=1 LLM_BACKEND=anthropic-api PORT=7875 ./run.sh exits non-zero; stdout/stderr contains one line naming PROVIDER_CAP_CONFIRMED; no line starts with Traceback. ENABLE_LIVE=1 alone still serves demo_mode true."},
  {"severity": "major",
   "title": "Docker path not executed: docker build and docker run are unverified (card AC1 still open)",
   "evidence": "`docker info` returns: failed to connect to the docker API at unix:///var/run/docker.sock: connect: no such file or directory. Card T-182 AC1 done=false. deploy/TIMING.md (Docker section): docker build and docker run were NOT executed. Emulated recipe passes (section 12): ctx_files=1411, forbidden=0, healthy in 2 s, demo_mode true, sample walked.",
   "why_it_matters": "Persona checklist 10 and card AC1 both require docker build and docker run to serve :7860 in demo mode with no key. Until a daemon runs the image, the Docker half of the golden path is ungraded. The emulation is strong evidence, not a substitute for the build.",
   "fix": "On a host with a Docker daemon, run make docker and make docker-run (or the two README commands) from a fresh clone. Save the build and run output to artifacts/review-evidence/ and record curl -fsS http://127.0.0.1:7860/api/health with demo_mode true.",
   "acceptance_test": "docker build -t zlayt-demo . exits 0; docker run --rm -p 7860:7860 zlayt-demo serves /api/health with demo_mode true, and the sample case reaches 9 entries with no key and no .env."},
  {"severity": "major",
   "title": "make evals, a documented command, exits 2 on a clean clone; the README does not say so",
   "evidence": "artifacts/review-evidence/T-182-installer-log.txt section 14, verbatim: ship_bar_met=False backend=fixture report=.../evals/reports/20261102T212248Z.md / blocker: 4_no_invented_facts / blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7) ... / blocker: judge_controls (J3/J4 seeded wrong items): not measured / make: *** [evals] Error 1. README.md:57 lists make evals with no mention of the exit status.",
   "why_it_matters": "Criterion 14 requires the documented eval command to work. A first-time reader gets a red failure with the word blocker and cannot tell whether the product is broken or the fixture run is expected to fail.",
   "fix": "Either (a) README.md:57 states that the fixture run cannot meet the ship bar by design, names the report it writes, and gives the expected exit status and what it means; or (b) the fixture run exits 0 and labels its result as not a ship measurement. The ship bar itself stays unchanged.",
   "acceptance_test": "On a clean clone with no key: make evals; echo $? gives the exit status the README documents, and the README sentence explaining it exists. A reader can tell from the README alone whether a non-zero result is expected."},
  {"severity": "minor",
   "title": "First Analyze click after a server starts is ignored (no POST /run); a second click works",
   "evidence": "Screenshot artifacts/review-evidence/T-182-installer-03-first-analyze-click-lost.png: the preview (9 records found, Analyze, Start over) is still on screen 60 s after the click. Walk output, section 4: analyze_clicked, then no POST /run after 3s; re-clicking Analyze, then SAMPLE_RESULTS_VISIBLE. Observed on 5 of 5 first walks against a newly started server; 0 of 13 later walks on a warm server needed a retry. Mechanism not established.",
   "why_it_matters": "A first-time reviewer sees Analyze do nothing and may conclude the app is broken. It costs about 3 s when they click again, but it is a timing defect on the golden path.",
   "fix": "Frontend: keep Analyze disabled until the POST that creates the sample case resolves, or re-bind the handler after the preview is re-rendered (input.js around line 100 and the preview render). Owner: frontend.",
   "acceptance_test": "On 5 fresh server starts, Playwright: click Use the sample case, then click Analyze as soon as it is visible; POST /api/cases/{token}/run appears within 2 s every time, with no second click."},
  {"severity": "minor",
   "title": "README does not name the buttons for the sample case",
   "evidence": "README.md:22: 'click the sample case, run it, and review the entries'. The button is labelled Use the sample case (app/frontend/input.js:100; screenshot artifacts/review-evidence/T-182-installer-01-landing.png), and the next step is Analyze. Section 4 shows the two-step flow.",
   "why_it_matters": "Checklist 9 wants a one-step load documented. The control exists, but a first-time reader has to guess the label and the two-click sequence.",
   "fix": "Replace the README sentence with: Click Use the sample case, then Analyze. You should see 9 records found, then 9 entries to decide.",
   "acceptance_test": "README contains the exact labels Use the sample case and Analyze, and the expected strings 9 records found and 9 entries to decide."},
  {"severity": "minor",
   "title": "No troubleshooting section; run.sh prints Serving on before the bind fails",
   "evidence": "Section 6 (verbatim tail): Serving on http://127.0.0.1:7860 (run.sh:36) then ERROR: [Errno 48] error while attempting to bind on address ('127.0.0.1', 7860): address already in use, exit 3. README.md has no Troubleshooting heading (full read). The uvicorn message is understandable; the success line before it is not.",
   "why_it_matters": "Checklist 12. Port in use is the most likely first failure on a shared machine. The printed success line tells the reader the server is up when it is not.",
   "fix": "Print the Serving on line only after the bind succeeds, or print a neutral line. Add a short Troubleshooting section: port in use -> PORT=7870 ./run.sh; no Docker daemon -> start Docker Desktop or skip Docker; Python below 3.12 -> the run.sh message and PYTHON=/path/to/python3.12.",
   "acceptance_test": "With the port occupied, ./run.sh prints one line naming the port and the PORT override, and no Serving on line. README has a Troubleshooting section that covers those three cases."},
  {"severity": "minor",
   "title": "Placeholders without example values in copy-paste commands; Replit prerequisites incomplete",
   "evidence": "README.md:14 git clone <this repo> zlayt; deploy/HUGGINGFACE.md:29 curl https://<username>-<space-name>.hf.space/api/health; deploy/REPLIT.md:14 Import from GitHub, paste this repo's URL (a GitHub account and a GitHub copy of the repo are not listed as prerequisites).",
   "why_it_matters": "Checklist 3 and 15. A reader cannot paste these as written.",
   "fix": "Give example values (for example git clone https://github.com/<owner>/zlayt zlayt, with the real URL once it exists). List a GitHub account as a Replit prerequisite.",
   "acceptance_test": "Every command block in README.md and deploy/*.md either has a real value or an example value next to each placeholder, and Replit prerequisites list GitHub."},
  {"severity": "minor",
   "title": "Normal use leaves untracked runtime files that .gitignore does not cover",
   "evidence": "Section 15 (git status after README path, make test and make evals): ?? data/ (data/zlayt.sqlite, 806912 bytes), ?? evals/reports/20261102T212248Z.md, ?? evals/reports/latest.fixture.json, ?? evals/reports/runs/20261102T212238Z/. .gitignore:16-17 covers app/db/*.sqlite3 and *.sqlite3 but not *.sqlite or data/.",
   "why_it_matters": "git add -A would stage a SQLite database of case records. hf_push.sh (git archive HEAD) and .dockerignore keep these out of the shipped artifacts, so this is repo hygiene, not a leak in the published demo.",
   "fix": "Add data/, *.sqlite and the evals fixture report outputs to .gitignore, or write them to an ignored directory. Decide explicitly which evals reports are committed.",
   "acceptance_test": "On a clean clone, run the README path, make test and make evals, then git status --short prints nothing."},
  {"severity": "minor",
   "title": "Replit: HOST binding for the published run is not shown to be inherited; python module name unconfirmed",
   "evidence": "deploy/replit/.replit:7-9 sets HOST=0.0.0.0 under [run.env]. The fetched Replit configuring-repl page documents [run.env] in the context of the Run command; the [deployment] block documents only run and deploymentTarget (cloudrun). run.sh:34 defaults HOST to 127.0.0.1, so a published ./run.sh may bind loopback only. deploy/replit/.replit:4 modules = [python-3.12] is unconfirmed; the docs example uses the python-3.10:v18-... form, and deploy/REPLIT.md:10 says so. Not tested: no Replit account here.",
   "why_it_matters": "Replit is the alternate host. If the published app binds loopback, the publish step in REPLIT.md:17 fails and the reader sees an unreachable app.",
   "fix": "Set the bind address where the deployment definitely reads it, or default HOST to 0.0.0.0 when REPL_ID is set. Confirm the module name against the current Replit page or the UI.",
   "acceptance_test": "Published Replit URL returns /api/health with demo_mode true (screenshot or curl output saved to artifacts/review-evidence/)."},
  {"severity": "minor",
   "title": "Dockerfile: floating base tag and a HEALTHCHECK hard-coded to port 7860",
   "evidence": "Dockerfile:3 FROM python:3.12-slim (tag, not digest). Dockerfile:21 ENV PORT=7860 is the default, but Dockerfile:26 HEALTHCHECK calls http://127.0.0.1:7860/api/health regardless of PORT.",
   "why_it_matters": "A rebuild can pull a different base image without warning. With docker run -e PORT=7870 -p 7870:7870 the container would be reported unhealthy while serving normally. Not tested: no daemon.",
   "fix": "Pin the base image by digest and record the digest in the Dockerfile comment. Read PORT inside the HEALTHCHECK command.",
   "acceptance_test": "docker inspect --format {{.State.Health.Status}} reports healthy with a PORT override, and the base image line includes a digest."},
  {"severity": "nit",
   "title": "Browser console shows 404s on load (/api/cases, /api/library, favicon.ico)",
   "evidence": "Section 17: 404 http://127.0.0.1:7871/api/cases (twice), 404 http://127.0.0.1:7871/api/library, favicon.ico 404.",
   "why_it_matters": "Does not block anything. A reviewer who opens devtools sees red errors on first load.",
   "fix": "Avoid the requests in demo mode, or add a favicon.",
   "acceptance_test": "Page load in demo mode produces no 4xx responses in the Playwright response listener."},
  {"severity": "nit",
   "title": "README heading says about 3 minutes; the measured time is 12 to 17 s",
   "evidence": "README.md:9 heading 'Run it from a clone (about 3 minutes, no key)' vs README.md:20 'Timed ... 17 s'. Section 1: 12 s to healthy, 17 s to sample visible.",
   "why_it_matters": "Mismatched numbers make the reader doubt the rest of the timing claims.",
   "fix": "Change the heading to match the timed figure, for example under a minute on a fast network, a few minutes on a slow one.",
   "acceptance_test": "The heading and the timed sentence give the same order of magnitude."},
  {"severity": "nit",
   "title": "make test duration is not stated",
   "evidence": "Section 13: 5801 passed, 2 skipped in 386.90s (0:06:26) on a shared host. README gives no expected duration.",
   "why_it_matters": "A reader who expects seconds may assume the run has hung.",
   "fix": "Add an expected duration, for example several minutes, next to the make test line.",
   "acceptance_test": "README states an expected duration for make test."}
 ],
 "whats_right": [
  "Demo path from a clean clone needs no key and no .env: healthy in 12 s, sample case visible in 17 s, demo_mode true and the synthetic banner shown (sections 1-4).",
  "run.sh rejects Python below 3.12 with a clear message, and a re-run reuses .venv: healthy in 1 s with no reinstall (sections 5 and 7).",
  "No secrets in the repo or in the Docker context: only .env.example is tracked, no key-shaped strings, and the .dockerignore allow-list keeps .env and sqlite files out (sections 12 and 16)."
 ],
 "questions_for_chris": [
  "Does the section 5 blocker 'the app crashes or shows a stack trace without an API key' cover an explicit live opt-in with the spend-cap flag missing (finding 1)? I rated it major because the section 8 test (empty environment reaches the sample case) passes. A literal reading makes it a blocker and the verdict fail.",
  "CONTRACT section 10 says the Docker image never includes the CLI backend, but the build context ships app/llm/backends/claude_cli.py (inert in fixture mode). Does shipping the code satisfy section 10? Outside my lens (security and release); flagged only.",
  "CONTRACT section 10 says the demo label reads cached demo. D-065 amends it to Demo: sample answers prepared by our team, which is what the app shows. I assumed D-065 governs and did not grade the label."
 ]}
```
