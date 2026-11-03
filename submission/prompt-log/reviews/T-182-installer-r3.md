# T-182 installer review, round 3: README run-from-clone after the guided UI landed

Verdict: **changes**. The r2 blocker is closed: from a fresh clone of HEAD 52e115a, `/` now offers "Open the sample case", and a first-time installer reaches the sample case, finishes all four steps and downloads the letter in about 28 s from `git clone` (2 s clone, healthy server at 12 s, sample case 0.2 s after page load, letter 15.9 s after that), well inside 5 minutes. What is left is that the README's golden-path sentence describes the old screen: its button names and counts match nothing on the new one. That is a major (the README is the artifact under review), not a blocker, because the correct buttons are the only buttons on screen and the path is not blocked.

Timing (local path clone into an empty temp dir, `env -i HOME PATH PORT=7883 ./run.sh`, no `.env`, no key; 7860 is held by another process and was left alone):
- clone 2 s; `/api/health` ok at 12 s from T0 with a cold venv and pip install; `demo_mode: true`, `backend: fixture`, synthetic banner shown.
- Sample case visible ("We found 9 records") 0.2 s after page load. Letter downloaded (`sample-case-letter.txt`, 2746 bytes) 15.9 s after page load, scripted. A human clicking 19 + 4 decisions will take longer, but that is user decision time, not setup time.
- Limits: local clone rather than a network clone; headless Chromium via the repo's dev venv (a clean machine does not carry Playwright); elapsed time excludes my tool-call gaps. Log: `artifacts/review-evidence/T-182-installer-r3-log.txt`.

Re-checks you asked for:
- **F1 holds.** `ENABLE_LIVE=1 LLM_BACKEND=anthropic-api` with no cap: exit 1, one line `error: live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 ...`, 0 tracebacks, and the contradictory "serving demo mode" warning is gone (85bcd22).
- **F3 holds.** `make evals` on the clone: make exit 2, three `blocker:` lines, the Makefile "EXPECTED" line, 8 s, `git status --short` empty afterwards.
- **Q2 holds.** `.dockerignore` still has `*`, `!app/**`, then `app/llm/backends/claude_cli.py` (right order). `git diff 18bfa69..HEAD` over Dockerfile, .dockerignore, app/llm/backends, run.sh, Makefile, requirements.txt, .env.example touches only `app/config.py`, so the r2 emulation still stands.
- **Other:** port 7860 busy gives one line plus the `PORT=7870` hint, exit 3. A second run on the same clone is healthy in 1 s.
- **Not graded:** F2 is documented debt (no Docker daemon: `docker info` fails on `/var/run/docker.sock`), kept as the same major with the same conditions as r2; F4 and F11.

```json
{"card": "T-182", "persona": "installer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git HEAD 52e115a of /Users/arsis/zlayt-pm-project (includes 26287b9 guided UI, 85bcd22 README/config fix). Fresh clone into a temp dir; app on http://127.0.0.1:7883 (7860 held by another process). Sample case via the guided UI; no ANTHROPIC_API_KEY, no .env.",
 "exercised": [
  "git clone /Users/arsis/zlayt-pm-project into a mktemp dir, README.md lines 1-60 read in full, timer from T0: clone 2 s, healthy at 12 s (artifacts/review-evidence/T-182-installer-r3-start.sh, log section 1)",
  "env -i HOME PATH PORT=7883 ./run.sh: /api/health demo_mode true, backend fixture, synthetic banner",
  "Playwright headless Chromium: GET / shows 'Open the sample case' and 'Start a new case'; Open the sample case -> 'We found 9 records' -> Draft the timeline -> '19 timeline items and 4 bill amounts' -> 19 timeline decisions -> 4 bill decisions -> '$8,390.00' -> Step 4 -> Download letter (.txt) saved as sample-case-letter.txt (T-182-installer-r3-full.py; screenshots T-182-installer-r3-01..09)",
  "console and network capture on every page: 404 on /api/cases at each load; no pageerror",
  "F1: ENABLE_LIVE=1 LLM_BACKEND=anthropic-api, no cap, no key: one line, exit 1, grep -c traceback 0, grep -c 'serving demo' 0 (log section 3)",
  "F3: make evals in the clone: exit 2, 3 blocker lines, EXPECTED line, 8 s, git status empty (T-182-installer-r3-checks.out)",
  "Q2: .dockerignore order read, ls app/llm/backends, git diff --stat 18bfa69..HEAD for the Docker-affecting files",
  "literal README first command: git clone https://github.com/OWNER/zlayt.git -> 'Repository not found' (checks.out)",
  "port 7860 busy: exit 3 one-liner; second run on same clone healthy in 1 s; docker info: no daemon",
  "stopped only my own PIDs (49823 on 7883, the 7885 rerun); lsof afterwards shows 7860 (PID 48223) and 7871 (PID 90987) untouched, neither mine"
 ],
 "verdict": "changes",
 "scores": {
  "readme_first_screen_and_fastest_path": 4,
  "prerequisites_explicit_with_versions": 5,
  "copy_pasteable_commands": 3,
  "clean_clone_commands_in_order": 4,
  "time_to_first_success_under_5_min": 5,
  "demo_mode_without_key_no_crash": 5,
  "env_example_and_no_secrets": 5,
  "url_port_and_expected_output_stated": 2,
  "one_step_sample_case_load_documented": 3,
  "docker_path_builds_and_runs": 2,
  "nondocker_path_pinned_and_reproducible": 5,
  "errors_and_troubleshooting": 5,
  "public_link_opens_with_banner": 3,
  "tests_and_evals_commands_work": 5,
  "no_undocumented_global_installs_or_accounts": 4,
  "rerun_works": 5
 },
 "findings": [
  {"severity": "major",
   "title": "README golden-path sentence names buttons and counts that are not in the guided UI",
   "evidence": "README.md:24 (golden-path line after the URL): 'click Use the sample case, then Analyze. You should see \"9 records found\", then \"9 entries to decide\". ... Accept / Edit / Dismiss decides what the export contains.' Actual screens at 52e115a (log section 2): home buttons are 'Start a new case' and 'Open the sample case'; then 'We found 9 records' and 'Draft the timeline'; then 'All set. 19 timeline items and 4 bill amounts are ready for you to check.'; decisions are 'Yes, this matches' / 'No, leave it out' / 'Fix the wording' / 'Decide later'; the path ends at Step 4 'Download letter (.txt)'. 'Use the sample case', 'Analyze', '9 records found', '9 entries to decide', 'Accept' and 'Dismiss' appear nowhere. The README never mentions the four steps or the letter download.",
   "why_it_matters": "Checklist 8 and 9: the README must say what you should see when it works and how to load the sample case. A reviewer comparing the page to the README sees different words and different numbers (19 items, not 9 entries) and has no way to tell whether the build is right. In r2 this same sentence was a blocker because no path existed; now the path works and only the wording is stale, so it is a major. The README is release-owned, so this is release rework, not a frontend defect.",
   "fix": "Rewrite README.md:24 to the guided labels: Open the sample case, then 'We found 9 records', Draft the timeline, then 'Go to step 2' and answer with Yes / No / Fix the wording, Step 3 bills ending '$8,390.00', Step 4 'Download letter (.txt)'. State the 19 timeline items and 4 bill amounts as the expected counts. Add a pointer to the guided pathway or a one-line 'the demo walk takes about 30 s of clicking plus your decisions'.",
   "acceptance_test": "A script that reads every quoted label and number from the README golden-path paragraph and asserts each appears on the matching screen of a fresh-clone run (grep the quoted strings against the Playwright page text); zero mismatches."},
  {"severity": "major",
   "title": "Docker path still not executed: docker build and docker run unverified (card AC1 open)",
   "evidence": "`docker info`: 'failed to connect to the docker API at unix:///var/run/docker.sock ... no such file or directory'. Card T-182 AC1 done=false. submission/NEEDS_CHRIS.md keeps 'Docker verification (T-182)'. Dockerfile, .dockerignore and requirements unchanged since r2 (`git diff --stat 18bfa69..HEAD` shows only app/config.py); the r2 emulation (allow-listed context, claude_cli.py dropped, Dockerfile ENV) therefore still applies.",
   "why_it_matters": "Checklist 10 requires a real docker build and docker run -p 7860:7860. Carried forward unchanged from r2 as documented debt: acceptable at the gate only with AC1 unchecked, the NEEDS_CHRIS entry open, and the README primary path not depending on Docker (it does not). The worker cannot close it on a host without a daemon.",
   "fix": "On a host with a Docker daemon run make docker and make docker-run from a fresh clone; save output to artifacts/review-evidence/ and record curl -fsS http://127.0.0.1:7860/api/health with demo_mode true. Until then keep AC1 unchecked and the NEEDS_CHRIS entry.",
   "acceptance_test": "docker build -t zlayt-demo . exits 0; docker run --rm -p 7860:7860 zlayt-demo serves /api/health with demo_mode true and docker inspect reports healthy; with -e PORT=7870 -p 7870:7870 it also reports healthy."},
  {"severity": "minor",
   "title": "README first command still contains the placeholder OWNER, so it cannot be pasted as written",
   "evidence": "README.md:13-16 (OWNER explained in prose at line 13, block shows `git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt`). Run as written: 'remote: Repository not found. fatal: repository https://github.com/OWNER/zlayt.git/ not found'. The r2 problem (angle brackets read as a shell redirect) is fixed; the command is now safe to paste but still points at no repository. A real URL depends on the public snapshot (T-194).",
   "why_it_matters": "Checklist 3: no placeholders without an example value. The reader's first step fails until they edit it, though the prose above says how.",
   "fix": "Put the real repository URL in the block once T-194 publishes it, or lead with the local-path form in the block as the runnable example.",
   "acceptance_test": "Paste the first README command block into a clean shell: it clones and enters the directory with no edits."},
  {"severity": "minor",
   "title": "Every page load logs a 404 on /api/cases in the browser console",
   "evidence": "Playwright capture on each load of GET / (log section 2): [http 404 http://127.0.0.1:7883/api/cases] and console 'Failed to load resource: the server responded with a status of 404 (Not Found)'. The r2 acceptance test for the guided home asked for 'no 4xx on page load'. The page itself is fine (shows Start a new case / Open the sample case, 'You don't have any cases yet.').",
   "why_it_matters": "A reviewer who opens devtools in the first minute sees a red error on the landing page. Not visible in the UI, and the cause is the backend returning 404 on that route outside local mode, which is by design for the case list, but the guided home still requests it.",
   "fix": "Frontend: do not request /api/cases when the server is not in local mode (check demo_mode in /api/health first) or have the endpoint return an empty list in demo mode.",
   "acceptance_test": "Fresh clone, ./run.sh, Playwright load of / with response and console listeners: zero responses with status >= 400 and zero console errors."},
  {"severity": "nit",
   "title": "Replit python module name still unconfirmed against Replit docs",
   "evidence": "deploy/replit/.replit lines 3-4: 'The python module name is NOT listed on that page ... pick Python 3.12 in the Replit UI if this line is rejected.' Disclosed, not tested (no Replit account).",
   "why_it_matters": "A wrong module name would make the Replit import fail. The text already gives the fallback, so risk is low.",
   "fix": "Confirm the module string once in the Replit UI, or leave the disclosure.",
   "acceptance_test": "Importing the repo into Replit with the shipped .replit starts ./run.sh without an editor error."}
 ],
 "whats_right": [
  "Golden path from a fresh clone works end to end with no key: clone 2 s, healthy 12 s, 9 records visible instantly, letter downloaded 16 s after page load.",
  "Round-1 and round-2 fixes hold on a fresh clone: one-line live-config error (no demo warning now), port-in-use exit 3, make evals expected failure printed and documented, git status clean afterwards.",
  "The guided home gives one obvious control per goal ('Open the sample case'), and the synthetic banner and demo badge are present from the first paint."
 ],
 "questions_for_chris": [
  "Do you want the README golden-path paragraph checked against the UI text automatically (a grep of its quoted strings against the Playwright page text) as a pre-commit or gate check, so a UI rewrite cannot leave it stale again?"
 ]}
```
