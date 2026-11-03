# Subagent: Release: README clone wording (Release: README clone wording)

Source: `agent-ac9505cef00ef9ffd.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T14:59:40.392Z

You are the release worker in /Users/arsis/zlayt-pm-project on T-212 (tiny fix, D-075). Read reviews/T-212-gate-M3M4.md.

README.md:16 clones `https://github.com/OWNER/zlayt.git`, which doesn't exist. Replace the step with one that is true however Chris hands it over: "Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder." Remove the OWNER URL and any paragraph about an unpublished snapshot. Keep everything else.

Commit README.md only, staging with a temp index (`GIT_INDEX_FILE=<tmp> git read-tree HEAD`, then `git add`) and committing with `git commit`. Move T-212 to in_review if the board allows (cycle through in_progress first), and reply in 1 line.

### User / tool · 2026-11-03T14:59:40.400Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:42.902Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-212-gate-M3M4.md"
}
````

### User / tool · 2026-11-03T14:59:42.911Z

**tool result**
````
1	# T-212 review, combined M3+M4 gate (D-075), staff-engineer-reviewer
2	
3	Verdict: **changes**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.
4	
5	README front door. The install and the walk work on a fresh clone (installer and verify pass), the `make evals` blocker is fixed, and all 58 README links resolve. The installer panel's major is still open at HEAD: the first command is a placeholder. The README discloses it and gives a zip path, and it cannot be closed until the repo is published, but it is open, so the verdict is changes.
6	
7	Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).
8	
9	## Findings
10	1. **major** The first README command cannot run as written: it clones https://github.com/OWNER/zlayt.git. Evidence: README.md:13 'The repo URL below does not exist yet ... OWNER is a placeholder'; README.md:16 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'. GATE-M3M4-installer.md major 1: 'First README command is a placeholder that fails'. verify-staff did not re-rate it; row 29 of SCOPE_CUTS accepts it as debt.
11	2. **minor** Docker build and run were never executed and the README says so (accepted, NEEDS_CHRIS). Evidence: GATE-M3M4-installer.md 'Not exercised': docker build, docker run, make test, deploy/; SCOPE_CUTS debt row for T-182.
12	
13	```json
14	{
15	 "card": "T-212",
16	 "persona": "staff-engineer-reviewer",
17	 "model": "claude-sonnet-5-5",
18	 "scope": "git archive a932fc9: README.md, run.sh, Makefile; installer panel at f6d5c19; verify pass at 43ce6eb",
19	 "exercised": [
20	  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
21	  "python3 tools/board.py show <card> for the AC of this card",
22	  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
23	  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
24	  "grep -n OWNER README.md at a932fc9: line 13 explains the placeholder, line 16 is 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'",
25	  "link checker: README.md 58 relative links, 0 dead",
26	  "verify-staff: fresh clone under env -i, ./run.sh healthy, Playwright walk of README steps 1-5 reaches $8,390.00 and a letter, zero page errors; make evals exits 2 and names exactly three blocker lines",
27	  "grep -n -i 'date of service' README.md: line 43 now describes the blank (installer minor fixed)",
28	  "git show HEAD:memory/SCOPE_CUTS.md row 29 lists 'Installer: README OWNER placeholder until Chris publishes' as accepted debt",
29	  "git show HEAD:submission/NEEDS_CHRIS.md rows 2-4: publish only the snapshot (T-195), byline and links (T-190), demo link (T-022); grep OWNER in NEEDS_CHRIS.md finds nothing, so no row says to replace the README placeholder"
30	 ],
31	 "verdict": "changes",
32	 "scores": {
33	  "fresh_clone_path_works": 5,
34	  "claims_true": 5,
35	  "first_command_runs_as_written": 2
36	 },
37	 "findings": [
38	  {
39	   "severity": "major",
40	   "title": "The first README command cannot run as written: it clones https://github.com/OWNER/zlayt.git",
41	   "evidence": "README.md:13 'The repo URL below does not exist yet ... OWNER is a placeholder'; README.md:16 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'. GATE-M3M4-installer.md major 1: 'First README command is a placeholder that fails'. verify-staff did not re-rate it; row 29 of SCOPE_CUTS accepts it as debt.",
42	   "why_it_matters": "The T-212 AC is 'a fresh-clone reader following only README reaches the sample case and the letter'. Today that works only through the zip path the README mentions in one sentence. The placeholder is disclosed, so it does not mislead, but a reviewer who copies the first command gets 'repository not found'.",
43	   "fix": "At publish time (T-194/T-195) replace OWNER with the real account in the snapshot's README, or name the actual path in the first code block (unzip, then ./run.sh) until a URL exists. This needs Chris's account name, so it is a publish-step item, not a worker fix today.",
44	   "acceptance_test": "grep -c OWNER README.md in the published snapshot returns 0 and `git clone <that url>` works from an empty directory; or the first code block is the zip path and runs."
45	  },
46	  {
47	   "severity": "minor",
48	   "title": "Docker build and run were never executed and the README says so (accepted, NEEDS_CHRIS)",
49	   "evidence": "GATE-M3M4-installer.md 'Not exercised': docker build, docker run, make test, deploy/; SCOPE_CUTS debt row for T-182.",
50	   "why_it_matters": "Reader-facing Docker instructions are unproven; the README does not hide that.",
51	   "fix": "Chris runs `make docker docker-run` once with Docker Desktop.",
52	   "acceptance_test": "a note on NEEDS_CHRIS says it ran."
53	  }
54	 ],
55	 "whats_right": [
56	  "A fresh clone under env -i reaches a healthy server, the sample case and a downloadable letter with zero page errors.",
57	  "The 'make evals' description now matches reality (three blocker lines, exit 2) and the README names the date blank in the walk."
58	 ],
59	 "questions_for_chris": [
60	  "Which GitHub account and repo name will host the public snapshot, so README.md:16 can be filled in at publish (T-194/T-195)?"
61	 ]
62	}
63	```
64	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:43.127Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/README.md",
 "limit": 40
}
````

### User / tool · 2026-11-03T14:59:43.134Z

**tool result**
````
1	# Treatment timeline: medical records to a verified chronology
2	
3	A prototype for a personal-injury paralegal: paste or upload medical records and get a dated treatment chronology, plus the treatment section of a demand letter, where **every statement is tied to a verbatim excerpt of the record**. Dates, gaps and bill totals are computed by code, a second, independent AI check double-checks each model answer, and **nothing reaches the letter until a person accepts it**.
4	
5	**Synthetic data only.** The app shows a banner and refuses text it has not seen in demo mode. Never paste real patient or client records.
6	
7	Ten minutes? Run it (below), do the 3-minute walk, then read "How the AI is checked".
8	
9	## Run it
10	
11	Needs **Python 3.12+** and git. No API key, no account, no network after the one-time install.
12	
13	The repo URL below does not exist yet: it will once Chris publishes the public snapshot, and the link will be in the submission email. Until then `OWNER` is a placeholder for the GitHub account that hosts it. If you were given the project as a zipped folder, skip the clone: unzip it, `cd` into the unzipped folder, and run `./run.sh` from there.
14	
15	```
16	git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt
17	./run.sh
18	```
19	
20	Open <http://127.0.0.1:7860>. The first run creates `.venv` and installs `requirements.txt` (the only slow step); later runs start in seconds. Stop it with Ctrl-C. Use another port with `PORT=7870 ./run.sh`.
21	
22	Timed 2026-11-02 from a fresh `git clone` into an empty directory: 17 s to a healthy server with a cold pip download (Apple-silicon Mac, Python 3.12.2, fast network; details in [`deploy/TIMING.md`](deploy/TIMING.md)). Budget a few minutes on a slow network.
23	
24	If `python3` on your machine is older than 3.12 (the macOS system Python is 3.9), `./run.sh` says so and stops. Point it at a newer one: `PYTHON=python3.12 ./run.sh`.
25	
26	**Docker (optional, not verified by us).** The `./run.sh` path above is the one we tested. The Dockerfile exists, but the team's machine had no running Docker daemon, so `docker build` and `docker run` have never been executed; we emulated the image's file list and environment instead. If you want to try it and it fails, use `./run.sh`. The open item is recorded in [`submission/NEEDS_CHRIS.md`](submission/NEEDS_CHRIS.md) ("Docker verification").
27	
28	```
29	docker build -t zlayt-demo .
30	docker run --rm -p 7860:7860 zlayt-demo        # http://127.0.0.1:7860
31	```
32	
33	The image is meant to hold the app, the synthetic eval inputs and the committed LLM fixtures, and nothing else (`.dockerignore` is an allow-list; no `.env`, key or database). It runs as uid 1000, listens on `0.0.0.0:7860`, and has a health check on `/api/health`.
34	
35	## The 3-minute walk (sample case)
36	
37	The page opens on **Your cases**. Every screen after it shows four steps across the top: **Add records, Check the timeline, Check the bills, Get your letter**. These labels were checked against the running app on a fresh clone.
38	
39	1. **Your cases.** With no cases yet, click **Open the sample case**.
40	2. **Step 1 of 4, "We found 9 records".** The nine synthetic records are listed with the dates the code read from them. Click **Draft the timeline**. When it finishes you should see "19 timeline items and 4 bill amounts are ready for you to check." (The badge "Prepared by our team" is demo mode; see below.) Click **Go to step 2: Check the timeline**.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:43.505Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-212 && git rev-parse --is-inside-work-tree && git status --short README.md",
 "description": "Show card T-212 and check git state of README"
}
````

### User / tool · 2026-11-03T14:59:43.667Z

**tool result**
````
---
id: "T-212"
title: "README front door for a repo-only reviewer (D-074): what it is, 2-command setup from a fresh clone, 3-minute demo walk, where the LLM judge and HITL live, links to the packet"
milestone: "M4"
role: "release"
status: "changes_requested"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T04:33:55Z"
updated_at: "2026-11-03T14:59:36Z"
claimed_by: "release"
claimed_at: "2026-11-03T04:34:21Z"
rounds: 1
commits: ["6be191fa295feaa7674e99205a0a4c2236cb85f6"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-212-gate-M3M4.md", "at": "2026-11-03T14:59:36Z"}
ac:
  - {"n": 1, "text": "a fresh-clone reader following only README reaches the sample case and the letter; a section 'How the AI is checked' explains code check -> LLM judge -> human with links to the prompts, judge code, evals/calibration and docs/LLM_VS_CODE.md and the ladder svg; links to submission/ files; installer re-walk passes", "done": true, "evidence": "README.md @6be191f: fresh git clone + env -i + ./run.sh on spare ports 7893/7894 healthy; sample walk clicked through in the browser (labels match); links checked; board status runs in the clone. Open: submission/SUBMISSION_CHECKLIST.md and email-draft.md are linked but untracked (writer)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T04:34:21Z release: claimed
- 2026-11-03T04:41:02Z release: AC 1 checked: README.md @6be191f: fresh git clone + env -i + ./run.sh on spare ports 7893/7894 healthy; sample walk clicked through in the browser (labels match); links checked; board status runs in the clone. Open: submission/SUBMISSION_CHECKLIST.md and email-draft.md are linked but untracked (writer)
- 2026-11-03T04:41:02Z release: moved in_progress -> in_review
- 2026-11-03T13:13:36Z orchestrator: review dispatched: product-manager-reviewer + installer-reviewer (queued: the D-074 double-check after T-202 fallback and T-211 land)
- 2026-11-03T14:51:23Z orchestrator: review dispatched: staff-engineer-reviewer (per-card record from the GATE-M3M4 panel, running)
- 2026-11-03T14:59:36Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-212-gate-M3M4.md; round 1; findings:
    - [major] The first README command cannot run as written: it clones https://github.com/OWNER/zlayt.git — fix: At publish time (T-194/T-195) replace OWNER with the real account in the snapshot's README, or name the actual path in the first code block (unzip, then ./run.sh) until a URL exists. This needs Chris's account name, so it is a publish-step item, not a worker fix today.
    - [minor] Docker build and run were never executed and the README says so (accepted, NEEDS_CHRIS) — fix: Chris runs `make docker docker-run` once with Docker Desktop.

## Handoff
What changed: README.md restructured per D-074 (what it is, run, 3-min walk with on-screen labels, How the AI is checked with ladder svg + prompts/judge code/evals/calibration/LLM_VS_CODE + demo vs live (D-056/D-065), what's where, limits->SCOPE_CUTS); Docker marked optional/unverified (NEEDS_CHRIS); make evals note and OWNER note kept. Verified: clone of HEAD 6be191f into temp dir, env -i, PORT 7893/7894, walked sample case to letter in browser (found: bill step uses 'Yes, list it/No, leave it out' for rate and non-money lines; macOS system python is 3.9 so README says PYTHON=python3.12). Servers stopped. Left: SUBMISSION_CHECKLIST.md and email-draft.md are linked but not yet committed (writer must commit or the links 404 in a clone); once T-211 ships, add one line in 'How the AI is checked' pointing at the 'How each answer is checked' page. Surprised: another agent's app already held :7871 (not mine; untouched).

true
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:55.772Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Move T-212 back to in_progress on the board",
   "status": "in_progress"
  },
  {
   "content": "Replace README run step (lines 13-18)",
   "status": "pending"
  },
  {
   "content": "Verify no OWNER or snapshot paragraph remains",
   "status": "pending"
  },
  {
   "content": "Commit README.md only via temp index",
   "status": "pending"
  },
  {
   "content": "Record commit, handoff, move T-212 to in_review",
   "status": "pending"
  }
 ],
 "scope": "continuation"
}
````

### User / tool · 2026-11-03T14:59:55.775Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:56.063Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py move T-212 in_progress --agent release",
 "description": "Move T-212 from changes_requested to in_progress"
}
````

### User / tool · 2026-11-03T14:59:56.199Z

**tool result**
````
T-212: changes_requested -> in_progress
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:58.736Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/README.md",
 "old_string": "The repo URL below does not exist yet: it will once Chris publishes the public snapshot, and the link will be in the submission email. Until then `OWNER` is a placeholder for the GitHub account that hosts it. If you were given the project as a zipped folder, skip the clone: unzip it, `cd` into the unzipped folder, and run `./run.sh` from there.\n\n```\ngit clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt\n./run.sh\n```",
 "new_string": "Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder.\n\n```\n./run.sh\n```"
}
````

### User / tool · 2026-11-03T14:59:58.788Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/README.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:59.290Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"OWNER|snapshot|unpublished|does not exist\" README.md; echo \"---diff---\"; git diff --stat -- README.md; git diff -- README.md | head -60",
 "description": "Check for leftover OWNER or snapshot text and review README diff"
}
````

### User / tool · 2026-11-03T14:59:59.406Z

**tool result**
````
---diff---
 README.md | 3 +--
 1 file changed, 1 insertion(+), 2 deletions(-)
diff --git a/README.md b/README.md
index 9b56421..174fc0c 100644
--- a/README.md
+++ b/README.md
@@ -10,10 +10,9 @@ Ten minutes? Run it (below), do the 3-minute walk, then read "How the AI is chec
 
 Needs **Python 3.12+** and git. No API key, no account, no network after the one-time install.
 
-The repo URL below does not exist yet: it will once Chris publishes the public snapshot, and the link will be in the submission email. Until then `OWNER` is a placeholder for the GitHub account that hosts it. If you were given the project as a zipped folder, skip the clone: unzip it, `cd` into the unzipped folder, and run `./run.sh` from there.
+Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder.
 
 ```
-git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt
 ./run.sh
 ```
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:05.525Z

**tool call — Bash**
````
{
 "command": "IDX=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T212.index && rm -f \"$IDX\" && GIT_INDEX_FILE=\"$IDX\" git read-tree HEAD && GIT_INDEX_FILE=\"$IDX\" git add README.md && GIT_INDEX_FILE=\"$IDX\" git diff --cached --stat && GIT_INDEX_FILE=\"$IDX\" git commit -m \"docs(release): drop OWNER placeholder clone step from README (T-212)\n\nReplace the git clone line that pointed at https://github.com/OWNER/zlayt.git\nand the unpublished-snapshot paragraph with one step that holds however the\nproject is handed over: clone the link you were given or unzip the download,\nthen cd into the folder. ./run.sh is unchanged.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log -1 --format=%H && git show --stat HEAD | tail -3",
 "description": "Stage README.md in temp index and commit only it"
}
````

### User / tool · 2026-11-03T15:00:05.610Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: IDX=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:08.478Z

**tool call — Bash**
````
{
 "command": "IDX=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T212.index && rm -f \"$IDX\" && GIT_INDEX_FILE=\"$IDX\" git read-tree HEAD && GIT_INDEX_FILE=\"$IDX\" git add README.md && GIT_INDEX_FILE=\"$IDX\" git diff --cached --stat",
 "description": "Build temp index from HEAD and stage README.md"
}
````

### User / tool · 2026-11-03T15:00:08.697Z

**tool result**
````
 README.md | 3 +--
 1 file changed, 1 insertion(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:12.364Z

**tool call — Bash**
````
{
 "command": "IDX=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T212.index && GIT_INDEX_FILE=\"$IDX\" git commit -m \"docs(release): drop OWNER placeholder clone step from README (T-212)\n\nReplace the git clone line that pointed at https://github.com/OWNER/zlayt.git\nand the unpublished-snapshot paragraph with one step that holds however the\nproject is handed over: clone the link you were given or unzip the download,\nthen cd into the folder. ./run.sh is unchanged.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log -1 --format=%H && git show --stat HEAD | tail -3",
 "description": "Commit staged README.md and show resulting SHA"
}
````

### User / tool · 2026-11-03T15:00:13.424Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
[main be257c9] docs(release): drop OWNER placeholder clone step from README (T-212)
 1 file changed, 1 insertion(+), 2 deletions(-)
be257c9209f78512e742b4a571f8a0dec0022c26

 README.md | 3 +--
 1 file changed, 1 insertion(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:17.019Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-212 --sha be257c9209f78512e742b4a571f8a0dec0022c26 --agent release && python3 tools/board.py note T-212 --agent release --text \"Fixed review finding 1 (major): removed the OWNER clone line and the unpublished-snapshot paragraph; first step is now 'Get the code: clone the repository link you were given (or unzip the download), then cd into its folder.' Only README.md changed.\" && python3 tools/board.py handoff T-212 --agent release --text \"What changed: README.md run step (be257c9) only. How verified: grep OWNER/snapshot in README returns nothing; diff is 1 insertion, 2 deletions; commit staged via temp index. What's left: the Docker minor finding stays accepted under NEEDS_CHRIS. What surprised me: git-guard rejects stage and commit in one command, so they run as two.\" && python3 tools/board.py move T-212 in_review --agent release",
 "description": "Record commit, note, handoff and move T-212 to in_review"
}
````

### User / tool · 2026-11-03T15:00:17.302Z

**tool result**
````
T-212: commit be257c9209f78512e742b4a571f8a0dec0022c26 recorded
noted on T-212
handoff written on T-212
T-212: in_progress -> in_review
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:18.673Z

T-212 is in_review: README's first step is now "Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder," with the OWNER clone line and snapshot paragraph removed; committed as be257c9 (README.md only, via temp index).
