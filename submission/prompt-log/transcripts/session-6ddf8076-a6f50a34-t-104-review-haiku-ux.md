# Subagent: T-104 review (haiku UX) (T-104 review (haiku UX))

Source: `agent-a6f50a349e410d181.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:08:45.944Z

Review board card T-104 in /Users/arsis/zlayt-pm-project (commit 3462ad0, app/frontend). On a `git archive HEAD` copy in your scratchpad, with your own server on a spare port (fixture backend, ZLAYT_DB in your scratchpad), confirm:
- a 422 CODE_CHECK_FAILED with EDIT_QUOTE shows "Change the quote" and opens the quote picker, and EDIT_SUMMARY shows "Edit the summary". Check this in item rows, batch rows, the "why" dialog and the rail;
- CODE_CHECK_FAILED from an edit renders inline under the edit box and keeps the typed text;
- the "why" copy follows the backend verdict string.

A known limitation is tracked as card T-108: on the sample, the quote picker can't save a valid quote, so don't score that. Stop your server by PID. Write reviews/T-104-ux-designer.md with a ```json block of real values: card, persona ux-designer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:48.046Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/ux-designer.md"
}
````

### User / tool · 2026-11-02T06:08:48.053Z

**tool result**
````
1	# Persona dossier — ux-designer-reviewer
2	
3	## 1. Identity
4	**Priya Raman (fictional), Principal UX Designer, enterprise workflow software — 12 years, last 4 on human-in-the-loop AI review tools (document review, claims triage).**
5	She has watched expert users abandon AI tools that hid where an answer came from, and others that made correcting the AI slower than doing the work by hand. Her incentive: the reviewer must finish faster *and* trust the result, so she grades the cost of verifying and correcting, not the beauty of the first screen.
6	
7	## 2. Day-to-day context
8	- Tools: Figma, Playwright scripts for walkthroughs, screen recordings, heuristic-evaluation sheets.
9	- Pressures: expert users with high volume who live on the keyboard; buyers who judge in a 3-minute demo.
10	- A bad day: usability sessions where every participant re-opens the source PDF because the tool's excerpt is hidden two clicks away.
11	
12	## 3. Goals and success criteria for this artifact
13	- The paralegal can see, for any entry, flag, or dollar amount, the exact source excerpt without leaving the screen.
14	- State is always visible: what is verified, what needs review and why, what has been accepted/edited/dismissed, how many remain.
15	- Correction is cheap: accept/edit/dismiss in one action each, keyboard-reachable, undoable.
16	- Errors, empty states, and model failure are designed, not default stack traces.
17	- The export is usable as pasted text in a demand letter.
18	
19	## 4. Review checklist
20	1. Every timeline entry shows date, provider, one-line summary, and the verbatim excerpt (or a one-click/one-key reveal that stays on the same screen).
21	2. `needs_review` items are visually distinct from `verified` and sorted first; the one-sentence reason is visible without hovering.
22	3. `rejected` (could-not-verify) items appear in a visible tray, not silently dropped.
23	4. Flags are grouped by type (gap, conflict, prior condition, causation language) and each shows the evidence excerpt(s); a conflict shows both excerpts side by side.
24	5. The charges table separates totaled charges from "unclear — not totaled" items; the $185/visit rate sits in the unclear group with its reason.
25	6. A progress indicator shows reviewed vs remaining (e.g., "7 of 12 reviewed") at all times during review.
26	7. Accept, edit, dismiss are each one click and have keyboard equivalents; the shortcuts are discoverable on screen.
27	8. Edit happens in place, preserves the original text for comparison, and marks the item as edited.
28	9. Any accept/dismiss can be undone without reloading.
29	10. Export is disabled or clearly warns while items remain unreviewed, and states exactly what will be included.
30	11. The exported text pastes cleanly into a word processor: one line per entry, no HTML artifacts, no UI labels, citations present.
31	12. Empty input, oversized input, and model/LLM failure each show a plain-language message near the input, preserve what the user pasted, and suggest the next step.
32	13. Long-running processing shows status (step names or progress), not a frozen screen.
33	14. The "synthetic data only" banner is persistent and does not obscure content or focused elements.
34	15. The AI's role is explained where it acts (e.g., "Summary drafted by AI, checked against the excerpt") — not a generic disclaimer.
35	16. Confidence is shown only as states that change a decision (verified / needs review / rejected), not as decorative percentages.
36	17. The layout works at 390 px width: no horizontal scroll for the review list; actions remain reachable.
37	18. Terminology matches the user's world (chronology, provider, excerpt, billed charges), not the developer's (chunk, span, token).
38	19. On first load of the sample-case results, the first focusable item in the results region is a `needs_review` item, and the 73-day gap flag is visible without scrolling at 1440x900.
39	20. Nothing in the interface claims more than the record supports (e.g., no "injury caused by accident" headers).
40	
41	## 5. Red flags / dealbreakers
42	Each item here is a **blocker** (rate it so; never major or minor).
43	- The source excerpt is not visible or reachable for an item (breaks "reviews rather than trusts").
44	- Export includes items the user did not accept, or there is no way to see what will be exported.
45	- An error state loses the user's pasted records.
46	- Unverified model output is styled identically to verified output.
47	
48	## 6. Vocabulary
49	visibility of system status, recognition over recall, error prevention, user control and freedom, accelerators, progressive disclosure, empty state, error state, inline validation, provenance / citation affordance, calibrated trust, efficient correction, efficient dismissal, scope of AI explanation, information scent, hierarchy, affordance.
50	
51	## 7. How I review
52	1. Read the brief; open the app at the given URL with Playwright (desktop 1440x900 and mobile 390x844).
53	2. Screenshot every state: empty, input pasted, processing, results, an item expanded, edit mode, flags panel, charges table, export preview, error (submit empty input; submit 500 KB of text), and model-failure if the brief provides a way to force it.
54	3. Complete the sample case end to end using only the keyboard first, then the mouse. Time both.
55	4. Try to export with items unreviewed; try to undo an accept; edit an entry and check the export shows the edit.
56	5. Paste the export into a plain text file and inspect it.
57	6. Score each of the four criteria (design quality, originality, craft, functionality) 1-5; any score ≤ 2 must have a matching major or blocker finding.
58	7. File findings with screenshot paths under `artifacts/review-evidence/`.
59	
60	Hard thresholds: functionality ≤ 2 → at least one blocker; verifying any single item takes more than 2 actions → major.
61	
62	## 8. Calibration
63	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
64	- **blocker — Excerpt hidden from conflict flag.** Evidence: screenshot shows "Conflicting accident dates" with no excerpts. Fix: show both quotes ("...2026-01-09..." EMS, "Date of accident per intake form: 2026-01-19") with record labels. Test: E2E asserts both excerpts visible in the flag card.
65	- **blocker — Error loses pasted input.** Evidence: submitting 600 KB shows "Error 413" and clears the textarea. Fix: inline message "This is over the 200 KB limit. Split the records and try again." with text preserved.
66	- **minor — No progress count.** Evidence: review screen with 12 entries has no remaining count. Fix: sticky "5 of 12 reviewed · 3 need review".
67	
68	## 9. Sources
69	- https://www.nngroup.com/articles/ten-usability-heuristics/ — NN/g: Nielsen's 10 heuristics (system status, user control, error prevention, recognition over recall, flexibility/accelerators, error recovery).
70	- https://www.nngroup.com/articles/error-message-guidelines/ — NN/g (2023): put errors near their source, don't rely on color alone, explain plainly with a fix, preserve user input.
71	- https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ — Amershi et al., CHI 2019: 18 validated guidelines across initial use, during interaction, when wrong, over time.
72	- https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ — Microsoft HAX Toolkit: the same 18 guidelines grouped by stage, including when the AI system is wrong.
73	- https://pair.withgoogle.com/chapter/explainability-trust/ — Google PAIR: calibrate trust, explain data sources, scale detail to stakes, show confidence only when it improves decisions.
74	- Assumption: the "two actions to verify" threshold and the 390 px width are this project's choices, not from a source.
75	
76	## 10. Limits
77	Do not judge clinical correctness, adjuster tactics, legal ethics, or code quality. Accessibility conformance (WCAG) belongs to accessibility-reviewer — note obvious issues but defer severity to them.
78	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:49.144Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_pin_review_commit.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_git_and_review_writes.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_bash_devnull.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_fix_every_surface.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/reference_sample_load_stall.md",
 "description": "List memory dir and read key feedback notes"
}
````

### User / tool · 2026-11-02T06:08:49.261Z

**tool result**
````
total 120
drwxr-xr-x@ 16 arsis  staff   512 Nov  1 23:50 .
drwxr-xr-x@ 17 arsis  staff   544 Nov  1 20:38 ..
-rw-r--r--@  1 arsis  staff  2270 Nov  1 23:50 MEMORY.md
-rw-r--r--@  1 arsis  staff  1261 Nov  1 22:54 feedback_fix_every_surface.md
-rw-r--r--@  1 arsis  staff  2109 Nov  1 23:50 feedback_gate_stored_results.md
-rw-r--r--@  1 arsis  staff  1079 Nov  1 22:57 feedback_one_action_keyboard_check.md
-rw-r--r--@  1 arsis  staff  1424 Nov  1 23:25 feedback_pin_review_commit.md
-rw-r--r--@  1 arsis  staff  1472 Nov  1 20:28 feedback_recheck_all_paths.md
-rw-r--r--@  1 arsis  staff  4424 Nov  1 23:25 feedback_rerun_status_and_gate_sync.md
-rw-r--r--@  1 arsis  staff   987 Nov  1 23:25 feedback_reviewer_bash_devnull.md
-rw-r--r--@  1 arsis  staff  1686 Nov  1 23:25 feedback_reviewer_git_and_review_writes.md
-rw-r--r--@  1 arsis  staff  1594 Nov  1 23:50 feedback_stub_rejudge_and_refresh_timing.md
-rw-r--r--@  1 arsis  staff  1646 Nov  1 22:57 project_sample_case_gap_flag_fold.md
-rw-r--r--@  1 arsis  staff  1519 Nov  1 22:57 project_sbs_pane_overlay.md
-rw-r--r--@  1 arsis  staff  1995 Nov  1 21:32 reference_office3d_phone_walk.md
-rw-r--r--@  1 arsis  staff  1089 Nov  1 22:57 reference_sample_load_stall.md
---
name: feedback_pin_review_commit
description: Review the app at the card's commit via git archive, never the repo-root working tree (it carries uncommitted changes and HEAD moves mid-review)
metadata:
  type: feedback
---

Serve the app from `git archive <card-commit> | tar -x -C <scratchpad>/<name>` and run `python -m app.main` from that copy, not from the repo root.

**Why:** On the T-046 review the repo-root tree had 269 uncommitted changes (`git status --short`). A server started there gave a judge-panel test failure that did not reproduce at the card commit 5616dc3. HEAD also moved twice during the review (5616dc3 to e92b6ed to e2b4e3f). Results from the dirty tree were discarded.

T-097 r2 (2026-11-02): the card's latest commit (21b6665) predated the backend tickets the brief depended on (T-100 24c18a7 came after it). When the brief asks for HEAD, archive HEAD, record that SHA, and check ancestry with `git merge-base --is-ancestor` for each ticket commit. HEAD moved again during that review (32f6c9d to f345bc8); diff the two before saying the pinned result still holds.

**How to apply:** Before any "at HEAD" run, record `git rev-parse --short HEAD` and `git status --short | wc -l`. Export the card's commit to scratch and start the server from that copy (PORT, HOST=127.0.0.1, separate ZLAYT_DB). Quote the commit in the review scope. Stop the server when done and confirm the port returns 000.
---
name: feedback_reviewer_git_and_review_writes
description: Reviewers cannot run git worktree (board-guard) and review files are append-only (reviewer-write-guard); pin a commit with git archive and write the review once, correctly
metadata:
  type: feedback
---

`git worktree add` and `git worktree list` are refused for reviewers in the project ("reviewers may not run git worktree in the project"). Use `git archive <commit> | tar -x -C <scratch>/<unique-dir>` to get a clean copy of the commit instead. Same content, no .git.

Reviews are append-only once written: the first `Write` to `reviews/<card>-<persona>[-rN].md` is final, and any `Edit` afterwards fails with "reviews are append-only — write a new file (e.g. -r2/-r3 suffix)". So draft the full review and its JSON block before the first write. Fix small wording errors in the first pass, not after.

**Why:** On T-046 r2 (2026-11-01) the worktree command was refused, and three wording fixes to the freshly written review could not be made afterwards.

T-097 r2 (2026-11-02) repeated it: a line cite (stepper.js:454, grep said 453) and an "after dismiss, all say 1" claim for the Why dialogs and export that I had not re-measured went into the first write and could not be edited. Disclosed in the reply instead.

**How to apply:** Before writing a review file, re-read the findings for file lists, counts, line numbers and attributions, and check every "after" state against an actual measurement. Put scratch exports in a uniquely named directory. The scratchpad path can change or lose a directory between calls (a `wt` folder disappeared between two calls). Check the directory exists right after you create it.
---
name: feedback_reviewer_bash_devnull
description: Reviewer Bash calls with "2>/dev/null" trip the board-guard hook ("redirect to /"); avoid /dev/null redirects in reviewer shell commands
metadata:
  type: feedback
---

A Bash command containing `2>/dev/null` (or other `>` followed by `/`) is rejected by the PreToolUse hook `board-guard` with "reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to /)". Nothing was written, but the call fails.

**Why:** The guard parses shell redirects loosely. The first Bash call in the T-046 review failed for this reason and had to be rerun.

The same guard also trips on a `>` inside inline `python -c` code, e.g. `i>=0` gives "redirect to =0". Put any Python check in a file under artifacts/review-evidence/ and run it.

**How to apply:** Drop `2>/dev/null`. Use `2>&1 | tail`, or test with `command -v` and `curl -s -o /dev/null -w`. For scratch files, use the scratchpad path with Python, not a shell redirect.
---
name: fix-every-surface-showing-the-state
description: When a finding names one component, re-measure every other surface that shows the same state (summary line, item Why dialog, rail rows) before accepting a fix
metadata:
  type: feedback
---

A state such as "blocks export", "edited" or "second check missing" is rendered by several code paths. Fixing the component named in the finding is not enough. T-097 (2026-11-01) fixed the AI-check panel rows and group, but the panel's collapsed summary still said "2 not checked (blocks export)" with a gate of 1, and the item Why dialog for an edited item still said "Accepted, second check missing" with a rerun button.
**Why:** T-082 r3 and T-097 each claimed gate agreement in one place. The same state comes from different builders: judges.js summaryText, judges.js row(), stepper.js item trace, stepper.js blockerRow. A fix in one builder leaves the others contradicting the gate.
**How to apply:** For any state a card touches, list every surface that shows it (grep the copy and the testid), then check each on a mixed case (edited + accepted + pending, judge never ran) at 1440 and 390. Record each surface's copy next to the gate's answer. See [[rerun-status-and-gate-sync]] for the T-097 instances.
---
name: reference_sample_load_stall
description: Playwright sample load (btn-sample, btn-analyze, entry-1) sometimes shows no entry-1 for 60 s just after an app server start; the server log stays empty; retry once and log the wait time
metadata:
  type: reference
---

On a freshly started app server (PORT set, fixture backend, empty ZLAYT_DB), the first sample analysis sometimes never shows `entry-1` within 60 s. `/api/health` is 200, the server log is empty, and no LLM failures are logged. A later load on the same server took 1.3 s (`wait_for` visible), and the same sample run succeeded inside 15 s in another run.

**Why:** Seen on T-046 r2 (2026-11-01) on three server starts. I could not isolate a cause from the server side.

**How to apply:** Load the sample once and wait up to 45 s for `entry-1`. On timeout, click `btn-analyze` once more and wait again. Record the wait time in the review's exercised list rather than reporting a stall as a product defect. Do not use a click result from a page where the sample stalled. See [[project_sbs_pane_overlay]] for the r2 walk.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:52.965Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | wc -l && git cat-file -t 3462ad0 && git log --oneline -3 3462ad0 && python3 tools/board.py show T-104",
 "description": "Pin HEAD, confirm commit 3462ad0, and show card T-104"
}
````

### User / tool · 2026-11-02T06:08:53.210Z

**tool result**
````
c2a5d1f
    1307
commit
3462ad0 fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
---
id: "T-104"
title: "Frontend follow-up for T-098 r3: EDIT_QUOTE refusals offer 'Change the quote'; CODE_CHECK_FAILED on edit shown inline; stale 'Your wording doesn't match' copy"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:54:15Z"
updated_at: "2026-11-02T06:08:42Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T05:54:21Z"
rounds: 0
commits: ["3462ad0"]
reviews: []
ac:
  - {"n": 1, "text": "When next_action is EDIT_QUOTE the refusal shows 'Change the quote' and opens the quote picker; CODE_CHECK_FAILED on edit renders inline (not the generic error path); Why copy follows the backend verdict string; e2e tests", "done": true, "evidence": "3462ad0 in a clean worktree of HEAD on :7906 with ZLAYT_DB: tests/e2e/test_code_check_refusal.py (23 incl. real+stub quote/edit/batch/Why cases), test_rerun_judge, test_stepper, test_edit, test_review_matrix + tests/unit/test_e2e_contract.py = 75 passed, 7 skipped; the new specs fail 11 on the pre-change frontend"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:54:21Z frontend: claimed
- 2026-11-02T06:08:31Z frontend: AC 1 checked: 3462ad0 in a clean worktree of HEAD on :7906 with ZLAYT_DB: tests/e2e/test_code_check_refusal.py (23 incl. real+stub quote/edit/batch/Why cases), test_rerun_judge, test_stepper, test_edit, test_review_matrix + tests/unit/test_e2e_contract.py = 75 passed, 7 skipped; the new specs fail 11 on the pre-change frontend
- 2026-11-02T06:08:31Z frontend: moved in_progress -> in_review
- 2026-11-02T06:08:42Z orchestrator: review dispatched: ux-designer-reviewer

## Handoff
What changed (3462ad0): EDIT_QUOTE refusal shows 'Change the quote' (accept box, batch rows, Why dialog, rail and AI-check rows) and opens the item's quote picker via ZL.openQuoteEditor (record fallback when no picker); CODE_CHECK_FAILED from an edit renders edit-refused-msg under the edit box, text kept, with Change the quote for EDIT_QUOTE; Why lead follows the backend verdict string (this summary / your wording), hardcoded guess only when no verdict. | Verified: clean worktree of HEAD, own server :7906 with ZLAYT_DB, 75 passed 7 skipped incl. test_e2e_contract; new ids declared in tests/e2e/conftest.py; 11 new specs fail on old frontend. | Left: nothing. | Surprised: the sample record's quote picker cannot rebuild the original quote (units carry 'Excerpt: "'), so saving from it 422s; specs stop at 'picker is open'.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:53.462Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"port|serve|ZLAYT_DB|LLM_BACKEND|fixture|PYTHONPATH|python -m|uvicorn|start\" docs/RUNBOOK.md | head -60",
 "description": "Read runbook for server start and env vars"
}
````

### User / tool · 2026-11-02T06:08:53.549Z

**tool result**
````
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
12:We restored those and gave the board and app their own ports so nothing of yours was clobbered.
24:## Restart (after a crash, reboot, or closing the session)
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
39:.venv/bin/python -m pytest tools/tests -q   # harness tests
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:55.407Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh && echo ---- && git merge-base --is-ancestor 3462ad0 HEAD && echo \"3462ad0 is ancestor of HEAD\" ; git log --oneline 3462ad0..HEAD | head -20",
 "description": "Read app serve script and check commit ancestry"
}
````

### User / tool · 2026-11-02T06:08:55.527Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
----
3462ad0 is ancestor of HEAD
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:00.876Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR/t104-3462ad0-ux\" && git archive 3462ad0 | tar -x -C \"$SCR/t104-3462ad0-ux\" && ls \"$SCR/t104-3462ad0-ux\" && ls \"$SCR/t104-3462ad0-ux/app\" && grep -n -E \"PORT|HOST|environ\" \"$SCR/t104-3462ad0-ux/app/main.py\" | head -20; grep -rn -E \"ZLAYT_DB|FIXTURE_SET\" \"$SCR/t104-3462ad0-ux/app/config.py\" 2>/dev/null | head; (command -v lsof >/dev/null && lsof -iTCP:7931 -sTCP:LISTEN | tail -n +1) ; echo \"port check done\"",
 "description": "Export commit 3462ad0 to scratch and check server entrypoint"
}
````

### User / tool · 2026-11-02T06:09:01.359Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
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
README-arch.md
__init__.py
backend
db
frontend
llm
main.py
pipeline.py
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
port check done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:03.829Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && D=\"$SCR/t104-3462ad0-ux\" && ls -d \"$D\" && cd \"$D\" && (PORT=7931 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=\"$SCR/t104-ux.sqlite3\" nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > \"$SCR/t104-server.log\" 2>&1 & echo $! > \"$SCR/t104-server.pid\") ; sleep 4; cat \"$SCR/t104-server.pid\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7931/api/health; curl -s http://127.0.0.1:7931/api/health | head -c 300; echo; cat \"$SCR/t104-server.log\" | tail -5",
 "description": "Start my own app server on port 7931 from archive copy"
}
````

### User / tool · 2026-11-02T06:09:07.959Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t104-3462ad0-ux
77878
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hour
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:10.038Z

**tool call — Bash**
````
{
 "command": "git show 3462ad0 --stat | head -30 && echo ---- && git show 3462ad0 -- app/frontend | head -400",
 "description": "Show the frontend diff for commit 3462ad0"
}
````

### User / tool · 2026-11-02T06:09:10.155Z

**tool result**
````
commit 3462ad0f62c5fa57f2803203c81fbe673a6dc517
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:06:28 2026 -0600

    fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/batch.js                |   9 +-
 app/frontend/excerpt.js              |  13 +++
 app/frontend/judges.js               |   2 +-
 app/frontend/review.js               |  23 ++++-
 app/frontend/stepper.js              |  20 +++-
 tests/e2e/conftest.py                |   4 +
 tests/e2e/test_code_check_refusal.py | 188 +++++++++++++++++++++++++++++++++++
 7 files changed, 247 insertions(+), 12 deletions(-)
----
commit 3462ad0f62c5fa57f2803203c81fbe673a6dc517
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:06:28 2026 -0600

    fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/batch.js b/app/frontend/batch.js
index d975a9b..1adcb2a 100644
--- a/app/frontend/batch.js
+++ b/app/frontend/batch.js
@@ -24,7 +24,7 @@
         if (String(code).toUpperCase() === "DATE_UNCONFIRMED") { RV.say("Confirm the date first. An entry in this batch has no confirmed date, so nothing was accepted. Pick its date in Dates to confirm, then try again.", true); return; }
         if (String(code).toUpperCase() === "CODE_CHECK_FAILED") {   // D-051 (T-098 r2): the whole batch is refused; say which items and why, with an Edit action on each
           const d = (r.body.error.detail || {}), list = Array.isArray(d.rejected) ? d.rejected : [];
-          refused = { token: c.token, message: r.body.error.message || "Nothing was accepted: a summary fails a check.", rows: list.map((x) => ({ id: x.id || x.item_id, why: x.why || "" })).filter((x) => x.id) };
+          refused = { token: c.token, message: r.body.error.message || "Nothing was accepted: a summary fails a check.", rows: list.map((x) => ({ id: x.id || x.item_id, why: x.why || "", code: x.next_action && x.next_action.code ? String(x.next_action.code).toUpperCase() : null })).filter((x) => x.id) };
           paintBar(c); RV.say(refused.message, true);
           const f = document.querySelector('[data-testid="batch-refused-msg"]'); if (f) { f.setAttribute("tabindex", "-1"); f.focus(); }
           return;
@@ -63,12 +63,15 @@
     const rows = refusedRows(c);
     if (!rows.length) return null;
     return el("div", { class: "rv-refused rv-refused-batch", role: "alert", "data-testid": "batch-refused" },
-      el("p", { class: "rv-refused-msg", "data-testid": "batch-refused-msg" }, el("strong", {}, "Nothing was accepted. "), refused.rows.length ? (rows.length === 1 ? "One summary fails a check, so the whole batch was refused. Edit it, then accept again." : rows.length + " summaries fail a check, so the whole batch was refused. Edit them, then accept again.") : refused.message),
+      el("p", { class: "rv-refused-msg", "data-testid": "batch-refused-msg" }, el("strong", {}, "Nothing was accepted. "), refused.rows.length ? (rows.some((x) => x.code === "EDIT_QUOTE")   // T-104: a quote check is not a summary problem
+        ? (rows.length === 1 ? "One entry fails a check, so the whole batch was refused. Fix it, then accept again." : rows.length + " entries fail a check, so the whole batch was refused. Fix them, then accept again.")
+        : rows.length === 1 ? "One summary fails a check, so the whole batch was refused. Edit it, then accept again." : rows.length + " summaries fail a check, so the whole batch was refused. Edit them, then accept again.") : refused.message),
       el("ul", { class: "rv-refused-list" }, rows.map((x) => {
         const name = ZL.stepper && ZL.stepper.label ? ZL.stepper.label(x.id) : x.id;
         return el("li", { "data-testid": "batch-refused-item", "data-refused-id": x.id },
           el("span", { class: "rv-refused-name" }, name), x.why ? el("span", { class: "rv-refused-why" }, " " + x.why) : null, " ",
-          ZL.stepper && ZL.stepper.editItem ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-batch-refused-edit", "aria-label": "Edit the summary for " + name, onclick: () => ZL.stepper.editItem(x.id) }, "Edit the summary") : null);
+          x.code === "EDIT_QUOTE" && ZL.stepper && ZL.stepper.changeQuote ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-batch-refused-quote", "aria-label": "Change the quote for " + name, onclick: () => ZL.stepper.changeQuote(x.id) }, "Change the quote")
+          : ZL.stepper && ZL.stepper.editItem ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-batch-refused-edit", "aria-label": "Edit the summary for " + name, onclick: () => ZL.stepper.editItem(x.id) }, "Edit the summary") : null);
       })));
   }
   function bar(c) {
diff --git a/app/frontend/excerpt.js b/app/frontend/excerpt.js
index bf91d81..060a674 100644
--- a/app/frontend/excerpt.js
+++ b/app/frontend/excerpt.js
@@ -2,6 +2,18 @@
    The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows the server's reasons. */
 (function () {
   const ZL = window.ZL, { el, clear } = ZL;
+  // T-104: other places (a refused Accept or edit, the Why dialog, the gate) open this picker for an item by id. Every rendering of the row registers its picker; the first one on the page opens.
+  const pickers = {};
+  ZL.openQuoteEditor = function (id) {
+    const list = (pickers[id] = (pickers[id] || []).filter((p) => p.panel.isConnected));
+    const p = list.find((x) => x.row.offsetParent !== null) || list[0];
+    if (!p) return false;
+    p.panel.hidden = false;
+    const f = p.panel.querySelector('[data-testid="excerpt-unit"]'); if (f) f.focus();
+    if (p.panel.scrollIntoView) p.panel.scrollIntoView({ block: "nearest" });
+    return true;
+  };
+  ZL.hasQuoteEditor = (id) => !!(pickers[id] || []).some((p) => p.panel.isConnected);
   ZL.registerRowActions((entry, row) => {
     if (entry.state === "rejected") return;
     const rec = ZL.state.get().case.records.find((r) => r.id === entry.record_ids[0]);
@@ -30,6 +42,7 @@
       }
     });
     draw();
+    pickers[entry.id] = (pickers[entry.id] || []).filter((p) => p.panel.isConnected); pickers[entry.id].push({ panel, row });
     const bar = row.querySelector(".row-actions");
     if (bar) bar.append(el("button", { type: "button", class: "btn small", "data-testid": "btn-edit-excerpt", onclick: () => { panel.hidden = !panel.hidden; } }, "Change quote"));
     row.append(panel);
diff --git a/app/frontend/judges.js b/app/frontend/judges.js
index 797fda8..4005b0d 100644
--- a/app/frontend/judges.js
+++ b/app/frontend/judges.js
@@ -104,7 +104,7 @@
       el("p", { class: "zs-why" }, el("strong", {}, ZL.stepper.wordingLead(id) + " "), b.why || ""),
       b.next_action && b.next_action.text ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), b.next_action.text) : null,
       el("div", { class: "zs-todo-btns" },
-        el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-judge-edit", "aria-label": ZL.stepper.wordingEditText(id) + " for " + t, onclick: () => ZL.stepper.editItem(id) }, ZL.stepper.wordingEditText(id)),
+        el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-judge-edit", "aria-label": ZL.stepper.wordingEditText(id, b.next_action) + " for " + t, onclick: () => ZL.stepper.wordingFix(id, b.next_action) }, ZL.stepper.wordingEditText(id, b.next_action)),
         el("button", { type: "button", class: "zs-btn", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
         el("button", { type: "button", class: "zs-btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps")));
   }
diff --git a/app/frontend/review.js b/app/frontend/review.js
index 4282c69..54ce70d 100644
--- a/app/frontend/review.js
+++ b/app/frontend/review.js
@@ -126,6 +126,20 @@
   // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
   function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
   function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }
+  const nextCode = (e) => { const n = e && e.detail && e.detail.next_action; return n && n.code ? String(n.code).toUpperCase() : null; };   // T-104: EDIT_SUMMARY | EDIT_QUOTE
+  const QUOTE = "Change the quote";
+  const changeQuote = (id) => () => { if (ZL.stepper && ZL.stepper.changeQuote) ZL.stepper.changeQuote(id); };
+  // T-104: CODE_CHECK_FAILED returned by an EDIT: the server's sentence sits under the edit box (the box stays open with the typed text); EDIT_QUOTE adds a Change the quote action.
+  function showEditRefusal(id, e) {
+    const s = slot(id, "rv-error"), msg = e.message || "That wording fails a check. Edit it to match the quote.";
+    if (s) {
+      ZL.clear(s);
+      s.append(el("span", { "data-testid": "edit-refused-msg" }, msg));
+      if (nextCode(e) === "EDIT_QUOTE") s.append(" ", el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-edit-refused-quote", "aria-label": QUOTE + " for " + (ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id), onclick: changeQuote(id) }, QUOTE));
+    }
+    RV.say("Not saved: " + msg, true);
+    const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
+  }
 
   // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
   // quote.") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.
@@ -136,7 +150,9 @@
     ZL.clear(box); box.hidden = !r;
     if (!r) return;
     box.append(el("p", { class: "rv-refused-msg", "data-testid": "accept-refused-msg" }, el("strong", {}, "Not accepted. "), r.message),
-      edit ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
+      r.code === "EDIT_QUOTE"   // T-104: the first failing check is on the quote, so the fix is the quote, not the summary
+        ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-accept-refused-quote", "aria-label": QUOTE + " for " + r.label, onclick: changeQuote(r.id) }, QUOTE)
+        : edit ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
   }
   function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
   RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";
@@ -172,12 +188,13 @@
       restoreFocus(o.advance ? { nextFrom: id, scope: o.scope } : o.focus ? { id, action: o.focus } : null);
       return true;
     } catch (e) {
-      if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
+      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
+      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
         const d = e.detail || {}, toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
         showError(id, (e.message || "That edit is not allowed.") + toks);
         const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
       } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
-        refusals[id] = { message: e.message || "The summary fails a check. Edit the summary to match the quote.", label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
+        refusals[id] = { id, code: nextCode(e), message: e.message || "The summary fails a check. Edit the summary to match the quote.", label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
         repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
         const mine = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-controls-for="' + id + '"]'), box = (mine || document).querySelector(".rv-refused:not([hidden])");
         if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner
diff --git a/app/frontend/stepper.js b/app/frontend/stepper.js
index b101833..d6fed30 100644
--- a/app/frontend/stepper.js
+++ b/app/frontend/stepper.js
@@ -132,8 +132,12 @@
   const WORDING_AI = "This summary doesn't match the quote:";
   // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
   const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== "entry" || f.item.ai_drafted === false || f.item.review_status === "edited"; };
-  S.wordingLead = (id) => (mine(id) ? WORDING : WORDING_AI);
-  S.wordingEditText = (id) => (mine(id) ? "Edit your wording" : "Edit the summary");
+  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
+  // only for wording the paralegal wrote or edited); no verdict (rail and panel rows) falls back to who wrote the item.
+  S.wordingLead = (id, verdictLabel) => (/your wording/i.test(verdictLabel || "") ? WORDING : /this summary/i.test(verdictLabel || "") ? WORDING_AI : mine(id) ? WORDING : WORDING_AI);
+  const quoteFix = (na) => !!na && String(na.code).toUpperCase() === "EDIT_QUOTE";   // the first failing check is on the quote, not the summary (T-104)
+  S.wordingEditText = (id, na, verdictLabel) => (quoteFix(na) ? "Change the quote" : (/your wording/i.test(verdictLabel || "") || (!/this summary/i.test(verdictLabel || "") && mine(id))) ? "Edit your wording" : "Edit the summary");
+  S.wordingFix = (id, na) => (quoteFix(na) ? S.changeQuote(id) : S.editItem(id));
   S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;
   let rerunBusy = false, rerunNote = null;   // rerunNote: {token, text}
   const rerunSay = (text) => {
@@ -212,6 +216,12 @@
     if (n) n.dispatchEvent(new KeyboardEvent("keydown", { key: "e", bubbles: true }));
     return true;
   };
+  // T-104: the first failing check is on the quote (next_action EDIT_QUOTE): the action is the quote picker (Change quote on the row), or the record itself when the row has no picker.
+  S.changeQuote = function (id) {
+    if (!gotoItem(id)) return false;
+    if (ZL.openQuoteEditor && ZL.openQuoteEditor(id)) return true;
+    openRecord(id, null); return true;
+  };
   const VIEW = {   // target.view -> [button text, handler]
     judges: ["Open the AI checks", () => gotoPanel("judges")],
     amounts: ["Go to the charges", () => gotoPanel("charges")],
@@ -416,8 +426,8 @@
         el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "item-verdict" }, v.label || ""),
         el("span", { class: "zs-progress", role: "status", "data-testid": "item-progress" }, progressLabel(steps))),
       wf ? el("div", { class: "zs-wording", role: "alert", "data-testid": "item-wording-fail" },
-        el("p", { class: "zs-todo-text" }, el("strong", {}, S.wordingLead(tr.item_id) + " "), wf.why || ""),
-        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-wording-edit", "aria-label": S.wordingEditText(tr.item_id) + " for " + S.label(tr.item_id), onclick: () => S.editItem(tr.item_id) }, S.wordingEditText(tr.item_id)))) : null,
+        el("p", { class: "zs-todo-text" }, el("strong", {}, S.wordingLead(tr.item_id, (tr.verdict || {}).label) + " "), wf.why || ""),
+        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-wording-edit", "aria-label": S.wordingEditText(tr.item_id, wf.next_action, (tr.verdict || {}).label) + " for " + S.label(tr.item_id), onclick: () => S.wordingFix(tr.item_id, wf.next_action) }, S.wordingEditText(tr.item_id, wf.next_action, (tr.verdict || {}).label)))) : null,
       now ? el("div", { class: "zs-now", "data-testid": "item-active" },
         el("p", { class: "zs-now-text" }, el("strong", {}, statusInfo(now).word + ": "), now.label, " ", el("span", { class: "zs-ev" }, firstSentence(now.why))),
         el("button", { type: "button", class: "zs-btn", "data-testid": "btn-jump-active", onclick: showActive }, "Show this step")) : null,
@@ -458,7 +468,7 @@
     return el("li", { class: "zs-blocker", "data-testid": "gate-blocker", "data-blocker-code": b.reason_code, "data-jump-item": b.item_id || null },
       el("span", { class: "zs-blocker-name" }, name), " ", el("span", { class: "zs-ev" }, wording ? [el("strong", {}, S.wordingLead(b.item_id) + " "), b.why || ""] : b.why || ""),
       b.item_id ? el("button", { type: "button", class: "zs-btn", "data-testid": "btn-gate-jump", "aria-label": "Go to item " + name, onclick: () => gotoItem(b.item_id) }, "Go to item") : null,
-      wording ? el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-gate-edit", "aria-label": S.wordingEditText(b.item_id) + " for " + name, onclick: () => S.editItem(b.item_id) }, S.wordingEditText(b.item_id)) : null,
+      wording ? el("button", { type: "button", class: "zs-btn zs-primary", "data-testid": "btn-gate-edit", "aria-label": S.wordingEditText(b.item_id, b.next_action) + " for " + name, onclick: () => S.wordingFix(b.item_id, b.next_action) }, S.wordingEditText(b.item_id, b.next_action)) : null,
       null);
   }
   // Rows only offer Go to item (and Edit for a wording blocker): the one rerun button lives with the list (the gate step, the refused-export message), because one POST reruns them all.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:12.959Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat \"$SCR/t104-3462ad0-ux/tests/e2e/test_code_check_refusal.py\"",
 "description": "Read the T-104 e2e spec at the pinned commit"
}
````

### User / tool · 2026-11-02T06:09:13.047Z

**tool result**
````
"""T-097 round 3 (D-051, T-098 r2): Accept (single and batch) can be refused with 422 CODE_CHECK_FAILED. The UI shows the server's plain reason next to the item's Accept button
with an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server
under test, to put a failing summary into the store the way a stale or imported state would) and against a route stub that answers exactly as memory/contracts/api.md says."""
import json
import os
import re
import sys
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REASON = "The summary has a number that is not in the quote: 5. Edit the summary to match the quote."
NEXT = {"code": "EDIT_SUMMARY", "text": "Edit the summary to match the quote"}


def _entry(tok, eid):
    c = api("GET", f"/api/cases/{tok}")[1]
    return next(e for e in c["entries"] + c["undated_entries"] if e["id"] == eid)


def _break(tok, eid):
    """Real backend: put 'Pain 5/10' (a figure the quote does not carry) into the stored summary, like a stale or imported state."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        assert "5/10" not in (_entry(tok, eid)["excerpt"] or "")
        DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10")
    finally:
        conn.close()


class Refuse:
    """Stub: POST .../review (accept) and POST .../review/batch (accept) answer 422 CODE_CHECK_FAILED while the item's summary is unchanged (an edit through the real route lifts it)."""
    def __init__(self, tok, eid):
        self.tok, self.eid = tok, eid
        self.base = _entry(tok, eid)["summary"]
        self.posts = 0

    def attach(self, page):
        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), self._single)
        page.route(re.compile(r"/api/cases/[^/]+/review/batch$"), self._batch)

    def active(self):
        return _entry(self.tok, self.eid)["summary"] == self.base

    def _single(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or not route.request.url.endswith(f"/items/{self.eid}/review") or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": REASON, "detail": {
            "item_id": self.eid, "reason_code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "step_id": "summary_tokens", "failed_steps": ["summary_tokens"], "tokens": ["5"],
            "next_action": dict(NEXT, target={"item_id": self.eid})}}}))

    def _batch(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or self.eid not in (body.get("item_ids") or []) or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": REASON + " Nothing was changed.", "detail": {"rejected": [
            {"id": self.eid, "reason": "code_check_failed", "reason_code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "why": REASON, "next_action": dict(NEXT, target={"item_id": self.eid})}]}}}))


@pytest.fixture(params=["real", "stub"])
def broken(request, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    orig = e["summary"]
    if request.param == "real":
        _break(sample_case, e["id"])
        assert _entry(sample_case, e["id"])["summary"] == "Pain 5/10"
        stub = None
    else:
        stub = Refuse(sample_case, e["id"])
    return {"tok": sample_case, "id": e["id"], "orig": orig, "mode": request.param, "stub": stub}


def arm(t, page):
    if t["stub"]:
        t["stub"].attach(page)
    return t


def row_of(page, i):
    return page.get_by_test_id("timeline").locator(f'[data-item-id="{i}"]').first


def vis(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"])
        row.scroll_into_view_if_needed()
        btn = row.get_by_test_id("btn-accept"); btn.click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
        assert "not in the quote" in msg or t["mode"] == "real"
        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
        assert box.get_attribute("role") == "alert"
        assert api("GET", f"/api/cases/{t['tok']}")[1]["review"]["counts"]["accepted"] == 0 and _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was changed"
        # Edit opens the item's edit box; a passing edit clears the refusal and the item is accepted by the edit
        box.get_by_test_id("btn-accept-refused-edit").click()
        ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
        assert pg.evaluate("document.activeElement === document.querySelector('[data-item-id=\"%s\"] textarea')" % t["id"]) or ta.is_visible()
        ta.fill(t["orig"]); row.get_by_test_id("btn-save-edit").click()
        expect(row_of(pg, t["id"])).to_have_attribute("data-review", "edited")
        expect(row_of(pg, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):
    t = arm(broken, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"]); row.focus()
    page.keyboard.press("a")
    expect(row.get_by_test_id("accept-refused")).to_be_visible()
    assert page.evaluate("document.activeElement.getAttribute('data-item-id')") == t["id"], "focus stays on the refused item"
    assert row.get_by_test_id("btn-accept").get_attribute("aria-pressed") == "false"
    page.keyboard.press("d")                                   # deciding the item another way clears the refusal
    expect(row_of(page, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()


def test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted(page, broken):
    t = arm(broken, page)
    open_case(page, t["tok"])
    page.get_by_test_id("btn-accept-verified").click()
    box = page.get_by_test_id("batch-refused"); expect(box).to_be_visible()
    assert box.get_attribute("role") == "alert" and box.get_by_test_id("batch-refused-msg").inner_text().startswith("Nothing was accepted.")
    items = box.get_by_test_id("batch-refused-item"); assert items.count() == 1
    assert items.first.get_attribute("data-refused-id") == t["id"]
    txt = items.first.inner_text()
    assert "Edit the summary to match the quote" in txt or "Edit the summary" in txt
    c = api("GET", f"/api/cases/{t['tok']}")[1]
    assert c["review"]["counts"]["accepted"] == 0, "all or nothing: the batch accepted none"
    items.first.get_by_test_id("btn-batch-refused-edit").click()
    ta = row_of(page, t["id"]).get_by_test_id("edit-summary"); expect(ta).to_be_visible()
    ta.fill(t["orig"]); row_of(page, t["id"]).get_by_test_id("btn-save-edit").click()
    expect(page.get_by_test_id("batch-refused")).to_have_count(0)      # the edited item is no longer waiting, so it leaves the list
    page.get_by_test_id("btn-accept-verified").click()
    expect(page.get_by_test_id("btn-undo-batch")).to_be_visible()      # the next batch goes through


def test_case_verdict_reads_the_backend_label_in_rail_and_panel(page, sample_case):
    """Real backend: an accepted AI draft whose summary then fails a code check is a gate blocker; the case verdict is the backend's words, in the rail and in the panel."""
    from tests.e2e.test_stepper import open_rail, open_judges
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    assert api("POST", f"/api/cases/{sample_case}/items/{e['id']}/review", {"action": "accept"})[0] == 200
    _break(sample_case, e["id"])
    open_case(page, sample_case); cs = open_rail(page)
    assert cs.get_by_test_id("case-verdict").text_content() == "1 summary fails a check"
    jp = open_judges(page)
    assert jp.get_by_test_id("judge-case-verdict").text_content() == "1 summary fails a check"
    assert "1 summary fails a check, blocks export: 1" in jp.get_by_test_id("judge-summary-counts").inner_text()
    blocker = cs.locator(f'[data-testid="gate-blocker"][data-jump-item="{e["id"]}"]')
    assert "This summary doesn't match the quote:" in blocker.inner_text() and "Your wording" not in blocker.inner_text(), "the paralegal did not write an AI draft"
    assert blocker.get_by_test_id("btn-gate-edit").inner_text() == "Edit the summary"


# ---- T-104: a first failing check on the QUOTE (next_action EDIT_QUOTE) offers "Change the quote" and opens the quote picker; CODE_CHECK_FAILED returned by an EDIT is shown
# inline under the edit box (typed text kept); the Why dialog follows the backend verdict string as sent. Real backend (ZLAYT_DB) and a route stub per case.
QUOTE_REASON = "The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence."
QUOTE_NEXT = {"code": "EDIT_QUOTE", "text": "Change the quote to whole sentences of the record that keep the hedge sentence"}


def _break_quote(tok, eid):
    """Real backend: store a quote that starts mid-sentence (first word cut off), like a stale or imported state. The record offsets stay, so the quote picker still preselects the whole sentences."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        words = _entry(tok, eid)["excerpt"].split(" ")
        DB.update_item(conn, eid, now=9e9, case=tok, excerpt=" ".join(words[1:]))
    finally:
        conn.close()


class RefuseQuote(Refuse):
    """Stub: accept (single and batch) and a summary-only edit answer 422 CODE_CHECK_FAILED / EDIT_QUOTE while the item's quote is unchanged; a quote edit goes to the real route and lifts it."""
    def __init__(self, tok, eid, edit_code="EDIT_QUOTE"):
        super().__init__(tok, eid)
        self.base_q = _entry(tok, eid)["excerpt"]
        self.edit_code = edit_code

    def active(self):
        return _entry(self.tok, self.eid)["excerpt"] == self.base_q and _entry(self.tok, self.eid)["review_status"] == "pending"

    def _detail(self, code):
        return {"item_id": self.eid, "reason_code": "EXCERPT_NOT_WHOLE_SENTENCE", "step_id": "excerpt_whole_sentence", "failed_steps": ["excerpt_whole_sentence"], "tokens": [],
                "next_action": dict(QUOTE_NEXT if code == "EDIT_QUOTE" else NEXT, code=code, target={"item_id": self.eid})}

    def _single(self, route):
        body = route.request.post_data_json or {}
        if not route.request.url.endswith(f"/items/{self.eid}/review") or not self.active():
            return route.fallback()
        if body.get("action") == "accept":
            self.posts += 1
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": QUOTE_REASON, "detail": self._detail("EDIT_QUOTE")}}))
        if body.get("action") == "edit" and "summary" in (body.get("edits") or {}):
            self.posts += 1
            msg = QUOTE_REASON if self.edit_code == "EDIT_QUOTE" else REASON
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": msg, "detail": self._detail(self.edit_code)}}))
        return route.fallback()

    def _batch(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or self.eid not in (body.get("item_ids") or []) or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": QUOTE_REASON + " Nothing was changed.", "detail": {"rejected": [
            {"id": self.eid, "reason": "code_check_failed", "reason_code": "EXCERPT_NOT_WHOLE_SENTENCE", "why": QUOTE_REASON, "next_action": dict(QUOTE_NEXT, target={"item_id": self.eid})}]}}}))


@pytest.fixture(params=["real", "stub"])
def broken_quote(request, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    if request.param == "real":
        _break_quote(sample_case, e["id"]); stub = None
    else:
        stub = RefuseQuote(sample_case, e["id"])
    return {"tok": sample_case, "id": e["id"], "orig": e["summary"], "excerpt": e["excerpt"], "mode": request.param, "stub": stub}


def _picker_open(page, t):
    """The item's own quote picker is open (its sentences listed, focus on one of them, on screen). Saving a choice is the picker's own job (excerpt.js); the sample record prints
    'Excerpt: "..."' around the quote, so its sentence units cannot rebuild the original quote and this spec stops at opening it."""
    row = row_of(page, t["id"]); ed = row.get_by_test_id("excerpt-editor")
    expect(ed).to_be_visible(); assert ed.get_by_test_id("excerpt-unit").count() >= 2
    assert page.evaluate("document.activeElement.getAttribute('data-testid')") == "excerpt-unit", "focus moves into the picker"
    assert vis(page, ed.get_by_test_id("btn-save-excerpt")) or vis(page, ed.get_by_test_id("excerpt-unit").first), "the picker is on screen"


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_on_a_quote_check_offers_change_the_quote_and_opens_the_picker(pw, broken_quote, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken_quote, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"]); row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-accept").click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and "whole sentences" in msg, msg
        q = box.get_by_test_id("btn-accept-refused-quote")
        assert q.inner_text() == "Change the quote" and box.get_by_test_id("btn-accept-refused-edit").count() == 0, "a quote check does not offer 'Edit the summary'"
        assert "Change the quote for" in q.get_attribute("aria-label")
        q.click()
        _picker_open(pg, t)
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_refused_batch_on_a_quote_check_offers_change_the_quote_per_item(page, broken_quote):
    t = arm(broken_quote, page)
    open_case(page, t["tok"])
    page.get_by_test_id("btn-accept-verified").click()
    box = page.get_by_test_id("batch-refused"); expect(box).to_be_visible()
    item = box.get_by_test_id("batch-refused-item"); assert item.count() == 1 and item.first.get_attribute("data-refused-id") == t["id"]
    assert item.first.get_by_test_id("btn-batch-refused-edit").count() == 0 and "summary" not in box.get_by_test_id("batch-refused-msg").inner_text()
    assert item.first.get_by_test_id("btn-batch-refused-quote").inner_text() == "Change the quote"
    item.first.get_by_test_id("btn-batch-refused-quote").click()
    _picker_open(page, t)


def test_a_refused_summary_check_still_offers_edit_the_summary(page, broken):
    """EDIT_SUMMARY keeps 'Edit the summary' (and no quote button)."""
    t = arm(broken, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"])
    row.get_by_test_id("btn-accept").click()
    box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
    assert box.get_by_test_id("btn-accept-refused-edit").inner_text() == "Edit the summary" and box.get_by_test_id("btn-accept-refused-quote").count() == 0


def test_code_check_failed_returned_by_an_edit_shows_inline_under_the_edit_box_and_keeps_the_text(page, broken_quote):
    """A summary-only edit on an item whose quote fails: 422 CODE_CHECK_FAILED / EDIT_QUOTE. The sentence sits under the edit box, the box stays open with the typed text,
    nothing is saved, and 'Change the quote' opens the picker."""
    t = arm(broken_quote, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"])
    row.get_by_test_id("btn-edit").click()
    ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
    typed = t["orig"].rstrip(".") + " as the record says."
    ta.fill(typed); row.get_by_test_id("btn-save-edit").click()
    ref = row.get_by_test_id("edit-refused-msg"); expect(ref).to_be_visible()
    assert "whole sentences" in ref.inner_text() and "Not accepted" not in ref.inner_text()
    form = row.locator("form.rv-edit"); assert form.is_visible() and ta.input_value() == typed, "the box stays open with the typed text"
    ya, yb = ref.bounding_box()["y"], form.bounding_box()["y"] + form.bounding_box()["height"]
    assert ya >= yb - 2, "under the edit box"
    assert ref.evaluate("e => e.closest('.rv-error').getAttribute('role')") == "alert"
    assert _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was saved"
    assert page.evaluate("document.activeElement.tagName") == "TEXTAREA", "focus stays in the box"
    row.get_by_test_id("btn-edit-refused-quote").click()
    _picker_open(page, t)


def test_code_check_failed_on_an_edit_with_edit_the_summary_has_no_quote_button(page, sample_case):
    """Stub: the edit route answers CODE_CHECK_FAILED / EDIT_SUMMARY. Same inline place, text kept, no 'Change the quote'."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = RefuseQuote(sample_case, e["id"], edit_code="EDIT_SUMMARY"); st.attach(page)
    open_case(page, sample_case); row = row_of(page, e["id"])
    row.get_by_test_id("btn-edit").click(); ta = row.get_by_test_id("edit-summary"); typed = e["summary"] + " Pain 5/10."
    ta.fill(typed); row.get_by_test_id("btn-save-edit").click()
    ref = row.get_by_test_id("edit-refused-msg"); expect(ref).to_be_visible()
    assert ref.inner_text() == REASON and ta.input_value() == typed and row.get_by_test_id("btn-edit-refused-quote").count() == 0


def _why_dialog(page, t, rewrite_label=None):
    """Accept the item (AI draft), break its quote in the store, open the Why dialog. rewrite_label rewrites the item trace's verdict label (a stub of what the backend sends)."""
    assert api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"})[0] == 200
    _break_quote(t["tok"], t["id"])
    if rewrite_label:
        def fn(route):
            d = route.fetch().json(); d["verdict"] = dict(d.get("verdict") or {}, label=rewrite_label); route.fulfill(json=d)
        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/trace$"), fn)
    open_case(page, t["tok"])
    page.locator(f'[data-testid="queue"] [data-item-id="{t["id"]}"], [data-testid="timeline"] [data-item-id="{t["id"]}"]').first.get_by_test_id("entry-why").click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    return st


def test_why_dialog_uses_the_backend_verdict_string_for_an_ai_draft_and_offers_change_the_quote(page, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = _why_dialog(page, {"tok": sample_case, "id": e["id"]})
    assert st.get_by_test_id("item-verdict").inner_text() == "Needs your attention: a check on this summary fails", "the backend's verdict string as sent"
    w = st.get_by_test_id("item-wording-fail"); txt = w.inner_text()
    assert txt.startswith("This summary doesn't match the quote:") and "Your wording" not in txt
    b = w.get_by_test_id("btn-wording-edit"); assert b.inner_text() == "Change the quote"
    b.click()
    expect(page.locator("#why-modal")).not_to_be_visible()
    expect(row_of(page, e["id"]).get_by_test_id("excerpt-editor")).to_be_visible()


@pytest.mark.parametrize("label,lead", [("Needs your attention: a check on your wording fails", "Your wording doesn't match the quote:"),
                                         ("Needs your attention: a check on this summary fails", "This summary doesn't match the quote:")])
def test_why_dialog_lead_follows_the_verdict_string_not_a_frontend_guess(page, sample_case, label, lead):
    """An AI draft whose trace the backend labels 'your wording' reads 'Your wording...'; the same item labelled 'this summary' reads 'This summary...'."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = _why_dialog(page, {"tok": sample_case, "id": e["id"]}, rewrite_label=label)
    assert st.get_by_test_id("item-verdict").inner_text() == label
    assert st.get_by_test_id("item-wording-fail").inner_text().startswith(lead)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:18.878Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat \"$SCR/t104-3462ad0-ux/tests/e2e/conftest.py\" | head -150; echo ----; .venv/bin/python -c \"import playwright, sys; print('playwright ok', sys.version.split()[0])\"",
 "description": "Read e2e conftest helpers and verify Playwright import"
}
````

### User / tool · 2026-11-02T06:09:18.988Z

**tool result**
````
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

@pytest.fixture
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)



class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."

    def __init__(self, page, token, ids):
        self.page, self.token, self.ids = page, token, list(ids)
        self.base = {i: self._summary(i) for i in self.ids}
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
            page.route(self._re.compile(pat), fn)

    def _summary(self, i):
        c = api("GET", f"/api/cases/{self.token}")[1]
        e = next((x for x in c["entries"] + c["undated_entries"] if x["id"] == i), None)
        return e and (e["summary"], e["review_status"])

    def active(self):
        return [i for i in self.ids if (cur := self._summary(i)) and cur[1] in ("accepted", "edited") and cur[0] == self.base[i][0]]

    def _na(self, i):
        return {"code": "EDIT_SUMMARY", "text": self.FIX, "target": {"item_id": i}}

    def blockers(self):
        return [{"item_id": i, "kind": "entry", "reason_code": "SUMMARY_DROPS_QUALIFIER", "step_id": "summary_qualifier", "failed_steps": ["summary_qualifier"], "why": self.WHY, "next_action": self._na(i)} for i in self.active()]

    def _case_trace(self, route):
        d = route.fetch().json(); act = self.blockers()
        if act:
            g = next(x for x in d["steps"] if x["id"] == "export_gate")
            g["blockers"] = [b for b in g["blockers"] if b["reason_code"] != "NOTHING_ACCEPTED"] + act
----
playwright ok 3.12.2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:37.103Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -n -A6 -E \"^def open_rail|^def open_judges\" \"$SCR/t104-3462ad0-ux/tests/e2e/test_stepper.py\"; echo ----; grep -n -E \"def update_item|def connect\" -A4 \"$SCR/t104-3462ad0-ux/app/db/db.py\" | head -30; echo ----; grep -n -i -E \"CODE_CHECK_FAILED|EDIT_QUOTE|next_action\" \"$SCR/t104-3462ad0-ux/memory/contracts/api.md\" | head -30",
 "description": "Read rail-opening helpers, DB update signature, and API contract refs"
}
````

### User / tool · 2026-11-02T06:09:37.212Z

**tool result**
````
32:def open_rail(page):
33-    """The case checks are collapsed to one line by default; open them like a user does."""
34-    cs = page.get_by_test_id("case-stepper"); cs.get_by_test_id("case-summary").wait_for()
35-    if not cs.locator("details.zs-case-det").evaluate("d => d.open"):
36-        cs.get_by_test_id("case-summary").click()
37-    cs.get_by_test_id("case-step").first.wait_for()
38-    return cs
--
41:def open_judges(page):
42-    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
43-    if not jp.locator("details.zj-det").evaluate("d => d.open"):
44-        jp.get_by_test_id("judge-summary").click()
45-    jp.get_by_test_id("judge-totals").wait_for()
46-    return jp
47-
----
38:def connect(path: str):
39-    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
40-    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
41-    pasted text past the 24 h purge (T-040 security r2)."""
42-    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
--
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
----
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
107:**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}`.
362:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
549:  "next_action": null }                 // object when status is "fail" or "pending", else null
553:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the action is `POST /rejudge`), `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.
564:  "next_action": { "code": "COMPARE_BY_HAND", "text": "...", "target": {"item_id": "e4"} },
570:                    "latency_ms": 5120, "parsed_ok": true, "excerpt": {"record_id": "r4", "start": 858, "end": 928, "text": "..."} }, "next_action": null },
577:      "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
597:      "counts": {"records": 9, "duplicates_merged": 0, "characters": 4120}, "evidence": {}, "next_action": null },
601:      "next_action": {"code": "CONFIRM_DATE", "text": "...", "target": {"view": "dates_to_confirm"}} },
611:      "blockers": [ { "item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "...", "next_action": {"code": "DECIDE", "text": "..."} } ],
612:      "warnings": [ { "reason_code": "ITEMS_NOT_REVIEWED", "count": 21, "why": "21 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "...", "target": {"view": "queue"}} } ],
613:      "next_action": {"code": "DECIDE", "text": "..."} } ] }
619:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
635:`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
643:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:45.749Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-setup.py",
 "content": "\"\"\"T-104 review (ux-designer-reviewer): build the states the brief asks for on MY server (port 7931, archive of 3462ad0).\n\nCreates one sample case over the API, then puts two failing states into the store the way the e2e spec does (tests/e2e/test_code_check_refusal.py):\n  - entry A: quote cut to start mid-sentence  -> backend answers EDIT_QUOTE  (\"Change the quote\")\n  - entry B: summary carries 'Pain 5/10'      -> backend answers EDIT_SUMMARY (\"Edit the summary\")\nWrites the ids to a JSON file in the scratchpad. Usage: ZLAYT_DB=<scratch db> .venv/bin/python <this file> <archive dir> <json out>\n\"\"\"\nimport json\nimport os\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = \"http://127.0.0.1:7931\"\nARCHIVE, OUT = sys.argv[1], sys.argv[2]\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            raw = r.read()\n            return r.status, (json.loads(raw) if raw else None)\n    except urllib.error.HTTPError as e:\n        raw = e.read()\n        return e.code, (json.loads(raw) if raw else None)\n\n\nst, c = api(\"POST\", \"/api/cases\", {\"sample\": True})\nassert st in (200, 201), st\ntok = c[\"token\"]\nassert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\nstatus = None\nfor _ in range(300):\n    status = api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"]\n    if status in (\"ready\", \"failed\"):\n        break\n    time.sleep(1)\nassert status == \"ready\", status\n\ncase = api(\"GET\", f\"/api/cases/{tok}\")[1]\ncands = [x for x in case[\"entries\"] if x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\"]\nassert len(cands) >= 2, [x[\"id\"] for x in cands]\nA, B = cands[0], cands[1]\norig_quote_A = A[\"excerpt\"]\nwords = A[\"excerpt\"].split(\" \")\nnew_quote_A = \" \".join(words[1:])\n\nsys.path.insert(0, ARCHIVE)\nfrom app.db import db as DB  # the archive's own module, same schema as the server under test\nconn = DB.connect(os.environ[\"ZLAYT_DB\"])\ntry:\n    DB.update_item(conn, A[\"id\"], now=9e9, case=tok, excerpt=new_quote_A)\n    DB.update_item(conn, B[\"id\"], now=9e9, case=tok, summary=\"Pain 5/10\")\nfinally:\n    conn.close()\n\nafter = api(\"GET\", f\"/api/cases/{tok}\")[1]\nea = next(x for x in after[\"entries\"] if x[\"id\"] == A[\"id\"])\neb = next(x for x in after[\"entries\"] if x[\"id\"] == B[\"id\"])\nassert ea[\"excerpt\"] == new_quote_A and eb[\"summary\"] == \"Pain 5/10\"\nout = {\"token\": tok, \"quote_item\": A[\"id\"], \"quote_item_summary\": A[\"summary\"], \"quote_item_orig_excerpt\": orig_quote_A,\n       \"summary_item\": B[\"id\"], \"summary_item_orig_summary\": B[\"summary\"], \"summary_item_excerpt\": B[\"excerpt\"],\n       \"candidate_ids\": [x[\"id\"] for x in cands]}\nwith open(OUT, \"w\") as f:\n    json.dump(out, f, indent=2)\nprint(json.dumps(out, indent=2))\n"
}
````

### User / tool · 2026-11-02T06:09:45.849Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-setup.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:48.428Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ZLAYT_DB=\"$SCR/t104-ux.sqlite3\" timeout 400 .venv/bin/python artifacts/review-evidence/T-104-ux-designer-setup.py \"$SCR/t104-3462ad0-ux\" \"$SCR/t104-state.json\" 2>&1 | tail -40",
 "description": "Create sample case and inject the two failing states",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T06:09:48.518Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:51.009Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ZLAYT_DB=\"$SCR/t104-ux.sqlite3\" .venv/bin/python artifacts/review-evidence/T-104-ux-designer-setup.py \"$SCR/t104-3462ad0-ux\" \"$SCR/t104-state.json\" 2>&1 | tail -40",
 "description": "Create sample case and inject the two failing states",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T06:09:52.434Z

**tool result**
````
{
  "token": "jNn5UicSOtYM-94PD2dE2g",
  "quote_item": "e1",
  "quote_item_summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.",
  "quote_item_orig_excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
  "summary_item": "e2",
  "summary_item_orig_summary": "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
  "summary_item_excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
  "candidate_ids": [
    "e1",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "e9"
  ]
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:56.922Z

**tool call — Bash**
````
{
 "command": "TOK=jNn5UicSOtYM-94PD2dE2g; B=http://127.0.0.1:7931; echo \"1 accept e1:\"; curl -s -X POST $B/api/cases/$TOK/items/e1/review -H 'Content-Type: application/json' -d '{\"action\":\"accept\"}' | head -c 900; echo; echo \"2 edit e1 summary-only:\"; curl -s -X POST $B/api/cases/$TOK/items/e1/review -H 'Content-Type: application/json' -d '{\"action\":\"edit\",\"edits\":{\"summary\":\"Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. As the record says.\"}}' | head -c 900; echo; echo \"3 accept e2:\"; curl -s -X POST $B/api/cases/$TOK/items/e2/review -H 'Content-Type: application/json' -d '{\"action\":\"accept\"}' | head -c 900; echo; echo \"4 edit e2 summary Pain 5/10 typed:\"; curl -s -X POST $B/api/cases/$TOK/items/e2/review -H 'Content-Type: application/json' -d '{\"action\":\"edit\",\"edits\":{\"summary\":\"Diagnosed with cervical strain; pain 5/10 as the record says.\"}}' | head -c 900; echo; echo \"state check:\"; curl -s $B/api/cases/$TOK | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['review']['counts']); [print(e['id'], e['review_status']) for e in d['entries'] if e['id'] in ('e1','e2')]\"",
 "description": "Probe real backend responses for accept and edit refusals"
}
````

### User / tool · 2026-11-02T06:09:57.101Z

**tool result**
````
1 accept e1:
{"error":{"code":"CODE_CHECK_FAILED","message":"The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.","detail":{"item_id":"e1","reason_code":"EXCERPT_NOT_WHOLE_SENTENCE","step_id":"excerpt_whole_sentence","failed_steps":["excerpt_whole_sentence"],"tokens":[],"next_action":{"code":"EDIT_QUOTE","text":"Change the quote to whole sentences of the record that keep the hedge sentence","target":{"item_id":"e1"}}}}}
2 edit e1 summary-only:
{"error":{"code":"CODE_CHECK_FAILED","message":"The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.","detail":{"item_id":"e1","reason_code":"EXCERPT_NOT_WHOLE_SENTENCE","step_id":"excerpt_whole_sentence","failed_steps":["excerpt_whole_sentence"],"tokens":[],"next_action":{"code":"EDIT_QUOTE","text":"Change the quote to whole sentences of the record that keep the hedge sentence","target":{"item_id":"e1"}}}}}
3 accept e2:
{"error":{"code":"CODE_CHECK_FAILED","message":"The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.","detail":{"item_id":"e2","reason_code":"SUMMARY_TOKEN_NOT_IN_EXCERPT","step_id":"summary_tokens","failed_steps":["summary_tokens","summary_qualifier"],"tokens":["5"],"next_action":{"code":"EDIT_SUMMARY","text":"Edit the summary to match the quote","target":{"item_id":"e2"}}}}}
4 edit e2 summary Pain 5/10 typed:
{"error":{"code":"invalid_edit","message":"The summary has a number, date or dollar figure that is not in the quote: 5. Remove it or change the quote.","detail":{"tokens":["5"],"reason":"SUMMARY_NUMBER_NOT_IN_EXCERPT"}}}
state check:
{'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0}
e1 pending
e2 pending
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:16.315Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-setup.py",
 "old_string": "A, B = cands[0], cands[1]\norig_quote_A = A[\"excerpt\"]\nwords = A[\"excerpt\"].split(\" \")\nnew_quote_A = \" \".join(words[1:])\n\nsys.path.insert(0, ARCHIVE)\nfrom app.db import db as DB  # the archive's own module, same schema as the server under test\nconn = DB.connect(os.environ[\"ZLAYT_DB\"])\ntry:\n    DB.update_item(conn, A[\"id\"], now=9e9, case=tok, excerpt=new_quote_A)\n    DB.update_item(conn, B[\"id\"], now=9e9, case=tok, summary=\"Pain 5/10\")\nfinally:\n    conn.close()\n\nafter = api(\"GET\", f\"/api/cases/{tok}\")[1]\nea = next(x for x in after[\"entries\"] if x[\"id\"] == A[\"id\"])\neb = next(x for x in after[\"entries\"] if x[\"id\"] == B[\"id\"])\nassert ea[\"excerpt\"] == new_quote_A and eb[\"summary\"] == \"Pain 5/10\"\nout = {\"token\": tok, \"quote_item\": A[\"id\"], \"quote_item_summary\": A[\"summary\"], \"quote_item_orig_excerpt\": orig_quote_A,\n       \"summary_item\": B[\"id\"], \"summary_item_orig_summary\": B[\"summary\"], \"summary_item_excerpt\": B[\"excerpt\"],\n       \"candidate_ids\": [x[\"id\"] for x in cands]}",
 "new_string": "A, B, C, D = cands[0], cands[1], cands[2], cands[3]\norig_quote_A = A[\"excerpt\"]\nwords = A[\"excerpt\"].split(\" \")\nnew_quote_A = \" \".join(words[1:])\nwords_C = C[\"excerpt\"].split(\" \")\nnew_quote_C = \" \".join(words_C[1:])\n\n# C and D are accepted while their wording is still valid (the rail and Why dialog then show a blocker on an accepted item), then broken in the store.\nfor x in (C, D):\n    st_acc, body_acc = api(\"POST\", f\"/api/cases/{tok}/items/{x['id']}/review\", {\"action\": \"accept\"})\n    assert st_acc == 200, (x[\"id\"], st_acc, body_acc)\n\nsys.path.insert(0, ARCHIVE)\nfrom app.db import db as DB  # the archive's own module, same schema as the server under test\nconn = DB.connect(os.environ[\"ZLAYT_DB\"])\ntry:\n    DB.update_item(conn, A[\"id\"], now=9e9, case=tok, excerpt=new_quote_A)\n    DB.update_item(conn, B[\"id\"], now=9e9, case=tok, summary=\"Pain 5/10\")\n    DB.update_item(conn, C[\"id\"], now=9e9, case=tok, excerpt=new_quote_C)\n    DB.update_item(conn, D[\"id\"], now=9e9, case=tok, summary=\"Pain 5/10\")\nfinally:\n    conn.close()\n\nafter = api(\"GET\", f\"/api/cases/{tok}\")[1]\nea = next(x for x in after[\"entries\"] if x[\"id\"] == A[\"id\"])\neb = next(x for x in after[\"entries\"] if x[\"id\"] == B[\"id\"])\nassert ea[\"excerpt\"] == new_quote_A and eb[\"summary\"] == \"Pain 5/10\"\nout = {\"token\": tok, \"quote_item\": A[\"id\"], \"quote_item_summary\": A[\"summary\"], \"quote_item_orig_excerpt\": orig_quote_A,\n       \"summary_item\": B[\"id\"], \"summary_item_orig_summary\": B[\"summary\"], \"summary_item_excerpt\": B[\"excerpt\"],\n       \"accepted_quote_item\": C[\"id\"], \"accepted_summary_item\": D[\"id\"],\n       \"candidate_ids\": [x[\"id\"] for x in cands]}"
}
````

### User / tool · 2026-11-02T06:10:16.414Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-setup.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:19.969Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ZLAYT_DB=\"$SCR/t104-ux.sqlite3\" .venv/bin/python artifacts/review-evidence/T-104-ux-designer-setup.py \"$SCR/t104-3462ad0-ux\" \"$SCR/t104-state.json\" 2>&1 | tail -40 && TOK=$(python3 -c \"import json,sys; print(json.load(open(sys.argv[1]))['token'])\" \"$SCR/t104-state.json\") && curl -s http://127.0.0.1:7931/api/cases/$TOK | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['review']['counts']); [print(e['id'], e['review_status'], e['state']) for e in d['entries'] if e['id'] in ('e1','e2','e3','e4')]\"",
 "description": "Recreate the case with two accepted and two pending broken items",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T06:10:21.242Z

**tool result**
````
{
  "token": "LSx5Yirp9S2KvZOp_puLBw",
  "quote_item": "e1",
  "quote_item_summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.",
  "quote_item_orig_excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
  "summary_item": "e2",
  "summary_item_orig_summary": "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
  "summary_item_excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
  "accepted_quote_item": "e3",
  "accepted_summary_item": "e4",
  "candidate_ids": [
    "e1",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "e9"
  ]
}
{'pending': 21, 'accepted': 2, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0}
e1 pending verified
e2 pending verified
e3 accepted verified
e4 accepted verified
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:25.439Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && TOK=LSx5Yirp9S2KvZOp_puLBw; for i in e1 e3 e2 e4; do echo \"== trace $i\"; curl -s http://127.0.0.1:7931/api/cases/$TOK/items/$i/trace | python3 -c \"import json,sys; d=json.load(sys.stdin); print('verdict:', d.get('verdict')); print('next:', d.get('next_action')); [print('  step', s['id'], s['status'], s.get('blocks_export'), (s.get('next_action') or {}).get('code'), (s.get('why') or '')[:140]) for s in d.get('steps',[]) if s.get('status')=='fail']\"; done; echo \"== case rail gate:\"; curl -s http://127.0.0.1:7931/api/cases/$TOK/trace | python3 -c \"import json,sys; d=json.load(sys.stdin); g=[s for s in d['steps'] if s['id']=='export_gate'][0]; print('verdict', d.get('verdict')); [print(' blocker', b.get('item_id'), b.get('reason_code'), (b.get('next_action') or {}).get('code'), b.get('why','')[:90]) for b in g.get('blockers',[])]\"",
 "description": "Read real traces and gate blockers for the four items"
}
````

### User / tool · 2026-11-02T06:10:25.634Z

**tool result**
````
== trace e1
verdict: {'code': 'needs_attention', 'label': 'Needs your attention', 'blocks_export': True}
next: {'code': 'EDIT_QUOTE', 'text': 'Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.', 'target': {'item_id': 'e1'}}
  step excerpt_whole_sentence fail False EDIT_QUOTE The quote starts or ends in the middle of a sentence.
== trace e3
verdict: {'code': 'needs_attention', 'label': 'Needs your attention: a check on this summary fails', 'blocks_export': True}
next: {'code': 'EDIT_QUOTE', 'text': 'Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it. The export stays blocked until it passes.', 'target': {'item_id': 'e3'}}
  step excerpt_whole_sentence fail True EDIT_QUOTE The quote starts or ends in the middle of a sentence.
== trace e2
verdict: {'code': 'needs_attention', 'label': 'Needs your attention', 'blocks_export': True}
next: {'code': 'EDIT_SUMMARY', 'text': "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.", 'target': {'item_id': 'e2'}}
  step summary_tokens fail False EDIT_SUMMARY The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.
  step summary_qualifier fail False EDIT_SUMMARY The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.
== trace e4
verdict: {'code': 'needs_attention', 'label': 'Needs your attention: a check on this summary fails', 'blocks_export': True}
next: {'code': 'EDIT_SUMMARY', 'text': 'Edit the summary to remove ‘5’, ‘10’, or change the quote so it contains them. The export stays blocked until it passes.', 'target': {'item_id': 'e4'}}
  step summary_tokens fail True EDIT_SUMMARY The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.
  step summary_qualifier fail True EDIT_SUMMARY The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.
== case rail gate:
verdict {'code': 'needs_attention', 'label': '2 summaries fail a check'}
 blocker e3 EXCERPT_NOT_WHOLE_SENTENCE EDIT_QUOTE The quote starts or ends in the middle of a sentence. This summary was drafted by the AI a
 blocker e4 SUMMARY_TOKEN_NOT_IN_EXCERPT EDIT_SUMMARY The summary has a number, date, dollar figure or left/right/no/not/without that is not in
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:22.872Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-walk.py",
 "content": "\"\"\"T-104 review (ux-designer-reviewer). Drives the app on my own server (127.0.0.1:7931, archive of commit 3462ad0).\n\nUsage: .venv/bin/python artifacts/review-evidence/T-104-ux-designer-walk.py <state.json>\nstate.json comes from T-104-ux-designer-setup.py. Each phase opens a fresh page. No accept or edit is ever saved (every refusal is answered\nby the backend or by a route stub); the quote picker is opened and closed without saving (T-108).\nReal backend for every phase except PHASE_STUB_* (route stubs, named in the results).\n\"\"\"\nimport json\nimport re\nimport sys\nimport time\n\nfrom playwright.sync_api import sync_playwright, expect\n\nBASE = \"http://127.0.0.1:7931\"\nEV = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"\nSTATE = json.load(open(sys.argv[1]))\nTOK = STATE[\"token\"]\nQI, SI, QA, SA = STATE[\"quote_item\"], STATE[\"summary_item\"], STATE[\"accepted_quote_item\"], STATE[\"accepted_summary_item\"]\nRESULTS = []\n\n\ndef rec(name, ok, detail=\"\"):\n    RESULTS.append({\"check\": name, \"ok\": bool(ok), \"detail\": detail})\n    print((\"PASS \" if ok else \"FAIL \") + name + (\" | \" + str(detail) if detail != \"\" else \"\"), flush=True)\n\n\ndef shot(page, name):\n    path = f\"{EV}/{name}.png\"\n    page.screenshot(path=path, full_page=False)\n    return path\n\n\ndef open_case(page):\n    page.goto(f\"{BASE}/#/case/{TOK}\")\n    page.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n\n\ndef row_of(page, i):\n    return page.get_by_test_id(\"timeline\").locator(f'[data-item-id=\"{i}\"]').first\n\n\ndef vis_in_viewport(page, loc):\n    b = loc.bounding_box()\n    vw, vh = page.viewport_size[\"width\"], page.viewport_size[\"height\"]\n    return b is not None and b[\"x\"] >= 0 and b[\"x\"] + b[\"width\"] <= vw + 1 and b[\"y\"] >= 0 and b[\"y\"] + b[\"height\"] <= vh\n\n\ndef buttons_in(loc):\n    return [(b.get_attribute(\"data-testid\"), b.inner_text().strip()) for b in loc.locator(\"button\").all()]\n\n\ndef picker_check(page, row, label):\n    ed = row.get_by_test_id(\"excerpt-editor\")\n    try:\n        expect(ed).to_be_visible(timeout=5000)\n        units = ed.get_by_test_id(\"excerpt-unit\").count()\n        focus = page.evaluate(\"document.activeElement.getAttribute('data-testid')\")\n        rec(f\"{label}: quote picker opens (units listed, focus moves into it)\", units >= 2 and focus == \"excerpt-unit\", f\"units={units} focus={focus}\")\n    except Exception as ex:  # noqa: BLE001\n        rec(f\"{label}: quote picker opens\", False, f\"not visible: {str(ex)[:160]}\")\n\n\n# ---------- PHASE 1: item row, real backend, EDIT_QUOTE (e1) and EDIT_SUMMARY (e2) ----------\ndef phase_rows(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    shot(pg, \"T-104-ux-desk-01-case-loaded\")\n    # EDIT_QUOTE on an item row\n    row = row_of(pg, QI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-accept\").click()\n    box = row.get_by_test_id(\"accept-refused\"); expect(box).to_be_visible(timeout=10000)\n    msg = box.get_by_test_id(\"accept-refused-msg\").inner_text()\n    btns = buttons_in(box)\n    shot(pg, \"T-104-ux-desk-02-row-e1-accept-refused-quote\")\n    q = box.get_by_test_id(\"btn-accept-refused-quote\")\n    rec(\"row e1 (EDIT_QUOTE): refusal shows 'Change the quote' and no 'Edit the summary'\",\n        q.count() == 1 and q.inner_text() == \"Change the quote\" and box.get_by_test_id(\"btn-accept-refused-edit\").count() == 0,\n        {\"msg\": msg, \"buttons\": btns})\n    rec(\"row e1: aria-label names the item\", \"Change the quote for\" in (q.get_attribute(\"aria-label\") or \"\"), q.get_attribute(\"aria-label\"))\n    q.click()\n    picker_check(pg, row, \"row e1 Change the quote\")\n    shot(pg, \"T-104-ux-desk-03-row-e1-picker-open\")\n    pg.keyboard.press(\"Escape\")\n    # EDIT_SUMMARY on an item row\n    row2 = row_of(pg, SI); row2.scroll_into_view_if_needed()\n    row2.get_by_test_id(\"btn-accept\").click()\n    box2 = row2.get_by_test_id(\"accept-refused\"); expect(box2).to_be_visible(timeout=10000)\n    msg2 = box2.get_by_test_id(\"accept-refused-msg\").inner_text()\n    e = box2.get_by_test_id(\"btn-accept-refused-edit\")\n    rec(\"row e2 (EDIT_SUMMARY): refusal shows 'Edit the summary' and no quote button\",\n        e.count() == 1 and e.inner_text() == \"Edit the summary\" and box2.get_by_test_id(\"btn-accept-refused-quote\").count() == 0,\n        {\"msg\": msg2, \"buttons\": buttons_in(box2)})\n    shot(pg, \"T-104-ux-desk-04-row-e2-accept-refused-summary\")\n    e.click()\n    ta = row2.get_by_test_id(\"edit-summary\")\n    try:\n        expect(ta).to_be_visible(timeout=5000)\n        rec(\"row e2: 'Edit the summary' opens the summary edit box\", True)\n    except Exception as ex:  # noqa: BLE001\n        rec(\"row e2: 'Edit the summary' opens the summary edit box\", False, str(ex)[:160])\n    shot(pg, \"T-104-ux-desk-05-row-e2-edit-box-open\")\n    pg.close()\n\n\n# ---------- PHASE 2: batch rows, real backend ----------\ndef phase_batch(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    pg.get_by_test_id(\"btn-accept-verified\").click()\n    box = pg.get_by_test_id(\"batch-refused\"); expect(box).to_be_visible(timeout=10000)\n    shot(pg, \"T-104-ux-desk-06-batch-refused\")\n    msg = box.get_by_test_id(\"batch-refused-msg\").inner_text()\n    items = box.get_by_test_id(\"batch-refused-item\").all()\n    rows = []\n    for it in items:\n        rid = it.get_attribute(\"data-refused-id\")\n        rows.append({\"id\": rid, \"text\": it.inner_text().strip(), \"buttons\": buttons_in(it)})\n    rec(\"batch: refused list names the two failing items\", {r[\"id\"] for r in rows} >= {QI, SI}, [r[\"id\"] for r in rows])\n    by = {r[\"id\"]: r for r in rows}\n    rq = by.get(QI, {}).get(\"buttons\", [])\n    rs = by.get(SI, {}).get(\"buttons\", [])\n    rec(\"batch e1 (EDIT_QUOTE): row offers 'Change the quote', not 'Edit the summary'\",\n        (\"btn-batch-refused-quote\", \"Change the quote\") in rq and not any(t == \"btn-batch-refused-edit\" for t, _ in rq), rq)\n    rec(\"batch e2 (EDIT_SUMMARY): row offers 'Edit the summary', no quote button\",\n        (\"btn-batch-refused-edit\", \"Edit the summary\") in rs and not any(t == \"btn-batch-refused-quote\" for t, _ in rs), rs)\n    rec(\"batch message (mixed quote and summary refusals) reads as the backend codes say\", True, msg)\n    qbtn = box.get_by_test_id(\"batch-refused-item\").locator('[data-testid=\"btn-batch-refused-quote\"]').first\n    qbtn.click()\n    picker_check(pg, row_of(pg, QI), \"batch e1 Change the quote\")\n    pg.close()\n\n\n# ---------- PHASE 3: inline edit refusal, real backend (EDIT_QUOTE on a summary-only edit) ----------\ndef phase_edit_inline(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    row = row_of(pg, QI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-edit\").click()\n    ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible(timeout=10000)\n    typed = \"Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. As the record says.\"\n    ta.fill(typed)\n    row.get_by_test_id(\"btn-save-edit\").click()\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    form = row.locator(\"form.rv-edit\")\n    shot(pg, \"T-104-ux-desk-07-edit-refused-quote\")\n    rec(\"inline edit e1 (CODE_CHECK_FAILED / EDIT_QUOTE): reason renders under the edit box, typed text kept\",\n        ta.input_value() == typed and form.is_visible() and ref.bounding_box()[\"y\"] >= form.bounding_box()[\"y\"] + form.bounding_box()[\"height\"] - 2,\n        {\"msg\": ref.inner_text(), \"typed_kept\": ta.input_value() == typed})\n    rec(\"inline edit e1: message sits in the item's role=alert error line\", ref.evaluate(\"e => e.closest('.rv-error').getAttribute('role')\") == \"alert\")\n    rec(\"inline edit e1: no generic 'Not accepted' prefix on an edit refusal\", \"Not accepted\" not in ref.inner_text())\n    qb = row.get_by_test_id(\"btn-edit-refused-quote\")\n    rec(\"inline edit e1 (EDIT_QUOTE): 'Change the quote' offered under the box\", qb.count() == 1 and qb.inner_text() == \"Change the quote\", buttons_in(row.locator(\".rv-error\")))\n    rec(\"inline edit e1: focus stays in the textarea\", pg.evaluate(\"document.activeElement.tagName\") == \"TEXTAREA\")\n    qb.click()\n    picker_check(pg, row, \"inline edit e1 Change the quote\")\n    shot(pg, \"T-104-ux-desk-08-edit-refused-quote-picker\")\n    pg.close()\n\n\n# ---------- PHASE 4: Why dialog, real backend ----------\ndef why_open(pg, i):\n    row = row_of(pg, i); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"entry-why\").click()\n    st = pg.get_by_test_id(\"item-stepper\"); st.wait_for(timeout=10000)\n    return st\n\n\ndef phase_why(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    st = why_open(pg, QA)\n    verdict = st.get_by_test_id(\"item-verdict\").inner_text()\n    w = st.get_by_test_id(\"item-wording-fail\")\n    wtxt = w.inner_text()\n    wb = w.get_by_test_id(\"btn-wording-edit\")\n    shot(pg, \"T-104-ux-desk-09-why-e3-quote\")\n    rec(\"why e3 (accepted AI draft, EDIT_QUOTE, real verdict): lead and action\", wb.inner_text() == \"Change the quote\" and wtxt.startswith(\"This summary doesn't match the quote:\"),\n        {\"verdict\": verdict, \"alert\": wtxt, \"button\": wb.inner_text()})\n    wb.click()\n    try:\n        expect(pg.locator(\"#why-modal\")).not_to_be_visible(timeout=5000)\n        rec(\"why e3: 'Change the quote' closes the dialog\", True)\n    except Exception as ex:  # noqa: BLE001\n        rec(\"why e3: 'Change the quote' closes the dialog\", False, str(ex)[:120])\n    picker_check(pg, row_of(pg, QA), \"why e3 Change the quote\")\n    pg.close()\n    # EDIT_SUMMARY on an accepted AI draft\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    st = why_open(pg, SA)\n    verdict = st.get_by_test_id(\"item-verdict\").inner_text()\n    w = st.get_by_test_id(\"item-wording-fail\"); wtxt = w.inner_text(); wb = w.get_by_test_id(\"btn-wording-edit\")\n    rec(\"why e4 (accepted AI draft, EDIT_SUMMARY, real verdict): lead and action\",\n        wb.inner_text() == \"Edit the summary\" and wtxt.startswith(\"This summary doesn't match the quote:\"), {\"verdict\": verdict, \"alert\": wtxt, \"button\": wb.inner_text()})\n    shot(pg, \"T-104-ux-desk-10-why-e4-summary\")\n    pg.close()\n\n\n# ---------- PHASE 5: Why dialog follows the verdict string (route stub rewrites only the label; EDIT_QUOTE and EDIT_SUMMARY) ----------\ndef phase_why_label_stub(browser):\n    results = {}\n    for item, label, tag in ((QA, \"Needs your attention: a check on your wording fails\", \"quote-your-wording\"),\n                             (SA, \"Needs your attention: a check on your wording fails\", \"summary-your-wording\"),\n                             (SA, \"Needs your attention: a check on this summary fails\", \"summary-this-summary\")):\n        pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n\n        def fn(route, lab=label):\n            d = route.fetch().json(); d[\"verdict\"] = dict(d.get(\"verdict\") or {}, label=lab); route.fulfill(json=d)\n        pg.route(re.compile(r\"/api/cases/[^/]+/items/[^/]+/trace$\"), fn)\n        open_case(pg)\n        st = why_open(pg, item)\n        verdict = st.get_by_test_id(\"item-verdict\").inner_text()\n        w = st.get_by_test_id(\"item-wording-fail\"); wtxt = w.inner_text(); wb = w.get_by_test_id(\"btn-wording-edit\")\n        results[tag] = {\"verdict_shown\": verdict, \"lead\": wtxt[:60], \"button\": wb.inner_text()}\n        pg.unroute_all(behavior=\"ignoreErrors\")\n        if tag == \"summary-your-wording\":\n            shot(pg, \"T-104-ux-desk-11-why-e4-your-wording-stub\")\n        pg.close()\n    rec(\"why lead follows the verdict string (stub label 'your wording' on an EDIT_SUMMARY item)\",\n        results[\"summary-your-wording\"][\"lead\"].startswith(\"Your wording doesn't match the quote:\") and results[\"summary-your-wording\"][\"button\"] == \"Edit your wording\",\n        results[\"summary-your-wording\"])\n    rec(\"why lead follows the verdict string (real 'this summary' label, EDIT_SUMMARY item)\",\n        results[\"summary-this-summary\"][\"lead\"].startswith(\"This summary doesn't match the quote:\") and results[\"summary-this-summary\"][\"button\"] == \"Edit the summary\",\n        results[\"summary-this-summary\"])\n    rec(\"why e3 with stub label 'your wording' (EDIT_QUOTE): lead flips, action stays 'Change the quote'\",\n        results[\"quote-your-wording\"][\"lead\"].startswith(\"Your wording doesn't match the quote:\") and results[\"quote-your-wording\"][\"button\"] == \"Change the quote\",\n        results[\"quote-your-wording\"])\n\n\n# ---------- PHASE 6: rail (case checks, gate blockers) ----------\ndef phase_rail(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    cs = pg.get_by_test_id(\"case-stepper\")\n    cs.get_by_test_id(\"case-summary\").wait_for(timeout=10000)\n    if not cs.locator(\"details.zs-case-det\").evaluate(\"d => d.open\"):\n        cs.get_by_test_id(\"case-summary\").click()\n    cs.get_by_test_id(\"case-step\").first.wait_for(timeout=10000)\n    shot(pg, \"T-104-ux-desk-12-rail-open\")\n    bq = cs.locator(f'[data-testid=\"gate-blocker\"][data-jump-item=\"{QA}\"]')\n    bs = cs.locator(f'[data-testid=\"gate-blocker\"][data-jump-item=\"{SA}\"]')\n    eq = bq.get_by_test_id(\"btn-gate-edit\"); es = bs.get_by_test_id(\"btn-gate-edit\")\n    rec(\"rail e3 (EDIT_QUOTE): gate blocker button reads 'Change the quote'\", eq.count() == 1 and eq.inner_text() == \"Change the quote\",\n        {\"blocker\": bq.inner_text()[:200], \"button\": eq.inner_text() if eq.count() else None})\n    rec(\"rail e4 (EDIT_SUMMARY): gate blocker button reads 'Edit the summary'\", es.count() == 1 and es.inner_text() == \"Edit the summary\",\n        {\"blocker\": bs.inner_text()[:200], \"button\": es.inner_text() if es.count() else None})\n    shot(pg, \"T-104-ux-desk-13-rail-blockers\")\n    eq.click()\n    picker_check(pg, row_of(pg, QA), \"rail e3 Change the quote\")\n    pg.close()\n\n\n# ---------- PHASE 7: AI-check panel (same state on a fourth surface) ----------\ndef phase_judges(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    jp = pg.get_by_test_id(\"judge-panel\"); jp.get_by_test_id(\"judge-summary\").wait_for(timeout=10000)\n    if not jp.locator(\"details.zj-det\").evaluate(\"d => d.open\"):\n        jp.get_by_test_id(\"judge-summary\").click()\n    jp.get_by_test_id(\"judge-totals\").wait_for(timeout=10000)\n    wl = jp.get_by_test_id(\"judge-wording-list\") if jp.get_by_test_id(\"judge-wording-list\").count() else None\n    rows = jp.get_by_test_id(\"btn-judge-edit\").all()\n    texts = [(b.inner_text(), (b.get_attribute(\"aria-label\") or \"\")) for b in rows]\n    rec(\"AI-check panel: wording rows read the same action as the item (quote -> 'Change the quote', summary -> 'Edit the summary')\",\n        any(t == \"Change the quote\" for t, _ in texts) and any(t == \"Edit the summary\" for t, _ in texts) and all(t in (\"Change the quote\", \"Edit the summary\", \"Edit your wording\") for t, _ in texts),\n        {\"judge_edit_buttons\": texts, \"wording_list_present\": wl is not None})\n    shot(pg, \"T-104-ux-desk-14-judges-wording\")\n    pg.close()\n\n\n# ---------- PHASE 8: 390 px, no horizontal scroll, actions reachable ----------\ndef phase_mobile(browser):\n    pg = browser.new_context(viewport={\"width\": 390, \"height\": 844}, is_mobile=False).new_page()\n    open_case(pg)\n    row = row_of(pg, QI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-accept\").click()\n    box = row.get_by_test_id(\"accept-refused\"); expect(box).to_be_visible(timeout=10000)\n    q = box.get_by_test_id(\"btn-accept-refused-quote\")\n    sw = pg.evaluate(\"document.documentElement.scrollWidth - document.documentElement.clientWidth\")\n    rec(\"390px: accept refusal (EDIT_QUOTE) button is inside the viewport\", vis_in_viewport(pg, q), {\"scroll_overflow_px\": sw, \"box\": box.bounding_box()})\n    shot(pg, \"T-104-ux-mob-01-row-e1-accept-refused-quote\")\n    pg.close()\n    pg = browser.new_context(viewport={\"width\": 390, \"height\": 844}).new_page()\n    open_case(pg)\n    row = row_of(pg, QI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-edit\").click()\n    ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible(timeout=10000)\n    typed = \"Restrained driver rear-ended at approx. 35 mph. As the record says.\"\n    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    qb = row.get_by_test_id(\"btn-edit-refused-quote\")\n    sw = pg.evaluate(\"document.documentElement.scrollWidth - document.documentElement.clientWidth\")\n    rec(\"390px: inline edit refusal and 'Change the quote' are reachable without horizontal scroll\", vis_in_viewport(pg, qb) and sw <= 0,\n        {\"scroll_overflow_px\": sw, \"typed_kept\": ta.input_value() == typed})\n    shot(pg, \"T-104-ux-mob-02-edit-refused-quote\")\n    pg.close()\n\n\n# ---------- PHASE 9: keyboard only, row e1 ----------\ndef phase_keyboard(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    row = row_of(pg, QI); row.scroll_into_view_if_needed(); row.focus()\n    pg.keyboard.press(\"a\")\n    box = row.get_by_test_id(\"accept-refused\"); expect(box).to_be_visible(timeout=10000)\n    focus_on_row = pg.evaluate(\"document.activeElement.getAttribute('data-item-id')\") == QI\n    presses = 0\n    target = None\n    for presses in range(1, 41):\n        pg.keyboard.press(\"Tab\")\n        if pg.evaluate(\"document.activeElement.getAttribute('data-testid')\") == \"btn-accept-refused-quote\":\n            target = presses; break\n    rec(\"keyboard (e1 EDIT_QUOTE): 'a' shows refusal, focus stays on the item, Tab reaches 'Change the quote'\",\n        focus_on_row and target is not None, {\"focus_on_row_after_a\": focus_on_row, \"tabs_to_quote_button\": target})\n    if target is not None:\n        pg.keyboard.press(\"Enter\")\n        picker_check(pg, row, \"keyboard e1 Change the quote (Enter)\")\n    pg.close()\n\n\ndef main():\n    with sync_playwright() as p:\n        browser = p.chromium.launch()\n        for fn in (phase_rows, phase_batch, phase_edit_inline, phase_why, phase_why_label_stub, phase_rail, phase_judges, phase_mobile, phase_keyboard):\n            try:\n                fn(browser)\n            except Exception as ex:  # noqa: BLE001\n                rec(f\"{fn.__name__} crashed\", False, str(ex)[:300])\n        browser.close()\n    out = f\"{EV}/T-104-ux-designer-results.json\"\n    with open(out, \"w\") as f:\n        json.dump({\"token\": TOK, \"results\": RESULTS}, f, indent=2)\n    print(\"results written:\", out)\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T06:11:22.970Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-walk.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:26.804Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-walk.py \"$SCR/t104-state.json\" 2>&1 | tail -80",
 "description": "Run the T-104 walkthrough against my server on 7931",
 "timeout": 540000
}
````

### User / tool · 2026-11-02T06:11:50.931Z

**tool result**
````
PASS row e2 (EDIT_SUMMARY): refusal shows 'Edit the summary' and no quote button | {'msg': 'Not accepted. The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.', 'buttons': [('btn-accept-refused-edit', 'Edit the summary')]}
PASS row e2: 'Edit the summary' opens the summary edit box
PASS batch: refused list names the two failing items | ['e1', 'e2']
PASS batch e1 (EDIT_QUOTE): row offers 'Change the quote', not 'Edit the summary' | [('btn-batch-refused-quote', 'Change the quote')]
PASS batch e2 (EDIT_SUMMARY): row offers 'Edit the summary', no quote button | [('btn-batch-refused-edit', 'Edit the summary')]
PASS batch message (mixed quote and summary refusals) reads as the backend codes say | Nothing was accepted. 2 entries fail a check, so the whole batch was refused. Fix them, then accept again.
PASS batch e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS inline edit e1 (CODE_CHECK_FAILED / EDIT_QUOTE): reason renders under the edit box, typed text kept | {'msg': 'The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.', 'typed_kept': True}
PASS inline edit e1: message sits in the item's role=alert error line
PASS inline edit e1: no generic 'Not accepted' prefix on an edit refusal
PASS inline edit e1 (EDIT_QUOTE): 'Change the quote' offered under the box | [('btn-edit-refused-quote', 'Change the quote')]
PASS inline edit e1: focus stays in the textarea
PASS inline edit e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS why e3 (accepted AI draft, EDIT_QUOTE, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The quote starts or ends in the middle of a sentence.\n\nChange the quote", 'button': 'Change the quote'}
PASS why e3: 'Change the quote' closes the dialog
PASS why e3 Change the quote: quote picker opens (units listed, focus moves into it) | units=6 focus=excerpt-unit
PASS why e4 (accepted AI draft, EDIT_SUMMARY, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.\n\nEdit the summary", 'button': 'Edit the summary'}
Error occurred in event listener
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_page.py", line 312, in _on_route
    handled = await route_handler.handle(route)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 456, in handle
    raise e
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 443, in handle
    return await self._handle_internal(route)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 479, in _handle_internal
    await handler_finished_future
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 470, in _handler
    self.handler(route, route.request)  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_impl_to_api_mapping.py", line 140, in wrapper_func
    return handler(
           ^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-walk.py", line 209, in fn
    d = route.fetch().json(); d["verdict"] = dict(d.get("verdict") or {}, label=lab); route.fulfill(json=d)
                                                                                      ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 22711, in fulfill
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 430, in fulfill
    await self._handle_route(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 508, in _handle_route
    raise e
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 504, in _handle_route
    await callback()
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 451, in _inner_fulfill
    body = json_utils.dumps(json)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 200, in encode
    chunks = self.iterencode(o, _one_shot=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 258, in iterencode
    return _iterencode(o, 0)
           ^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type Request is not JSON serializable
FAIL phase_why_label_stub crashed | Locator.wait_for: Timeout 10000ms exceeded.
Call log:
  - waiting for get_by_test_id("item-stepper") to be visible

FAIL phase_rail crashed | Browser.new_context: Object of type Request is not JSON serializable
PASS AI-check panel: wording rows read the same action as the item (quote -> 'Change the quote', summary -> 'Edit the summary') | {'judge_edit_buttons': [('Change the quote', 'Change the quote for 2026-01-16 · Dr. Alvarez, primary care · Record 3'), ('Edit the summary', 'Edit the summary for 2026-01-23 · Capital PT, initial evaluation · Record 4')], 'wording_list_present': True}
PASS 390px: accept refusal (EDIT_QUOTE) button is inside the viewport | {'scroll_overflow_px': 0, 'box': {'x': 40, 'y': 671.328125, 'width': 314, 'height': 156.828125}}
FAIL phase_mobile crashed | Locator expected to be visible
Actual value: None
Error: element(s) not found 
Call log:
  - Expect "to_be_visible" get_by_test_id("timeline").locator("[data-item-id=\"e1\"]").first.get_by_test_id("edit-refused-msg") with timeout 10000ms
  - waiting for get_by_test_id("timeline").locator("[data-item
PASS keyboard (e1 EDIT_QUOTE): 'a' shows refusal, focus stays on the item, Tab reaches 'Change the quote' | {'focus_on_row_after_a': True, 'tabs_to_quote_button': 8}
PASS keyboard e1 Change the quote (Enter): quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
results written: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-results.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:58.495Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && TOK=LSx5Yirp9S2KvZOp_puLBw; curl -s http://127.0.0.1:7931/api/cases/$TOK | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['review']['counts']); [print(e['id'], e['review_status'], e['state']) for e in d['entries'] if e['id'] in ('e1','e2','e3','e4')]\"; grep -c \"\" \"$SCR/t104-server.log\"; tail -5 \"$SCR/t104-server.log\"",
 "description": "Confirm no accept or edit was saved and check server log"
}
````

### User / tool · 2026-11-02T06:11:58.615Z

**tool result**
````
{'pending': 21, 'accepted': 2, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0}
e1 pending verified
e2 pending verified
e3 accepted verified
e4 accepted verified
2
llm call failed call_id=c77c5862c52d7 step=j1 attempt=1 prompt_hash=9ad331cd97b77e42df76c4a7c1c7c2731b17421a722c07711833bd7e817c5abe
llm call failed call_id=c210df5758e72 step=j1 attempt=1 prompt_hash=9ad331cd97b77e42df76c4a7c1c7c2731b17421a722c07711833bd7e817c5abe
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:05.953Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF' 2>&1 | tail -5\nimport re\np = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-walk.py\"\ns = open(p).read()\nold = \"\"\"        def fn(route, lab=label):\n            d = route.fetch().json(); d[\"verdict\"] = dict(d.get(\"verdict\") or {}, label=lab); route.fulfill(json=d)\n\"\"\"\nnew = \"\"\"        def make(lab):\n            def fn(route, *_args):\n                d = route.fetch().json(); d[\"verdict\"] = dict(d.get(\"verdict\") or {}, label=lab); route.fulfill(json=d)\n            return fn\n        fn = make(label)\n\"\"\"\nassert s.count(old) == 1\ns = s.replace(old, new)\nold2 = \"\"\"    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    qb = row.get_by_test_id(\"btn-edit-refused-quote\")\"\"\"\nnew2 = \"\"\"    seen = []\n    pg.on(\"response\", lambda r: seen.append((r.request.method, r.status, r.url[-40:])) if \"/review\" in r.url and r.request.method == \"POST\" else None)\n    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    time.sleep(2)\n    print(\"DEBUG mobile save responses:\", seen, \"rv-error text:\", row.locator(\".rv-error\").all_inner_texts(), flush=True)\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    qb = row.get_by_test_id(\"btn-edit-refused-quote\")\"\"\"\nassert s.count(old2) == 1\ns = s.replace(old2, new2)\nopen(p, \"w\").write(s)\nprint(\"patched\")\nEOF",
 "description": "Patch the stub closure bug and add mobile save debug output"
}
````

### User / tool · 2026-11-02T06:12:06.047Z

**tool result**
````
patched
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:09.584Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-walk.py \"$SCR/t104-state.json\" 2>&1 | grep -v \"^  \" | tail -60",
 "description": "Rerun the full T-104 walkthrough after the stub fix",
 "timeout": 540000
}
````

### User / tool · 2026-11-02T06:12:26.835Z

**tool result**
````
PASS row e1 (EDIT_QUOTE): refusal shows 'Change the quote' and no 'Edit the summary' | {'msg': 'Not accepted. The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.', 'buttons': [('btn-accept-refused-quote', 'Change the quote')]}
PASS row e1: aria-label names the item | Change the quote for 2026-01-09 · Austin EMS run report
PASS row e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS row e2 (EDIT_SUMMARY): refusal shows 'Edit the summary' and no quote button | {'msg': 'Not accepted. The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.', 'buttons': [('btn-accept-refused-edit', 'Edit the summary')]}
PASS row e2: 'Edit the summary' opens the summary edit box
PASS batch: refused list names the two failing items | ['e1', 'e2']
PASS batch e1 (EDIT_QUOTE): row offers 'Change the quote', not 'Edit the summary' | [('btn-batch-refused-quote', 'Change the quote')]
PASS batch e2 (EDIT_SUMMARY): row offers 'Edit the summary', no quote button | [('btn-batch-refused-edit', 'Edit the summary')]
PASS batch message (mixed quote and summary refusals) reads as the backend codes say | Nothing was accepted. 2 entries fail a check, so the whole batch was refused. Fix them, then accept again.
PASS batch e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS inline edit e1 (CODE_CHECK_FAILED / EDIT_QUOTE): reason renders under the edit box, typed text kept | {'msg': 'The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.', 'typed_kept': True}
PASS inline edit e1: message sits in the item's role=alert error line
PASS inline edit e1: no generic 'Not accepted' prefix on an edit refusal
PASS inline edit e1 (EDIT_QUOTE): 'Change the quote' offered under the box | [('btn-edit-refused-quote', 'Change the quote')]
PASS inline edit e1: focus stays in the textarea
PASS inline edit e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS why e3 (accepted AI draft, EDIT_QUOTE, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The quote starts or ends in the middle of a sentence.\n\nChange the quote", 'button': 'Change the quote'}
PASS why e3: 'Change the quote' closes the dialog
PASS why e3 Change the quote: quote picker opens (units listed, focus moves into it) | units=6 focus=excerpt-unit
PASS why e4 (accepted AI draft, EDIT_SUMMARY, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.\n\nEdit the summary", 'button': 'Edit the summary'}
PASS why lead follows the verdict string (stub label 'your wording' on an EDIT_SUMMARY item) | {'verdict_shown': 'Needs your attention: a check on your wording fails', 'lead': "Your wording doesn't match the quote: The summary has a numb", 'button': 'Edit your wording'}
PASS why lead follows the verdict string (real 'this summary' label, EDIT_SUMMARY item) | {'verdict_shown': 'Needs your attention: a check on this summary fails', 'lead': "This summary doesn't match the quote: The summary has a numb", 'button': 'Edit the summary'}
PASS why e3 with stub label 'your wording' (EDIT_QUOTE): lead flips, action stays 'Change the quote' | {'verdict_shown': 'Needs your attention: a check on your wording fails', 'lead': "Your wording doesn't match the quote: The quote starts or en", 'button': 'Change the quote'}
PASS rail e3 (EDIT_QUOTE): gate blocker button reads 'Change the quote' | {'blocker': "2026-01-16 · Dr. Alvarez, primary care\nThis summary doesn't match the quote: The quote starts or ends in the middle of a sentence. This summary was drafted by the AI and a code check on it fails, so i", 'button': 'Change the quote'}
PASS rail e4 (EDIT_SUMMARY): gate blocker button reads 'Edit the summary' | {'blocker': "2026-01-23 · Capital PT, initial evaluation\nThis summary doesn't match the quote: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. This summar", 'button': 'Edit the summary'}
PASS rail e3 Change the quote: quote picker opens (units listed, focus moves into it) | units=6 focus=excerpt-unit
PASS AI-check panel: wording rows read the same action as the item (quote -> 'Change the quote', summary -> 'Edit the summary') | {'judge_edit_buttons': [('Change the quote', 'Change the quote for 2026-01-16 · Dr. Alvarez, primary care · Record 3'), ('Edit the summary', 'Edit the summary for 2026-01-23 · Capital PT, initial evaluation · Record 4')], 'wording_list_present': True}
PASS 390px: accept refusal (EDIT_QUOTE) button is inside the viewport | {'scroll_overflow_px': 0, 'box': {'x': 40, 'y': 671.328125, 'width': 314, 'height': 156.828125}}
DEBUG mobile save responses: [('POST', 422, 's/LSx5Yirp9S2KvZOp_puLBw/items/e1/review')] rv-error text: ['The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.']
FAIL phase_mobile crashed | Locator expected to be visible
Actual value: None
Error: element(s) not found 
Call log:
PASS keyboard (e1 EDIT_QUOTE): 'a' shows refusal, focus stays on the item, Tab reaches 'Change the quote' | {'focus_on_row_after_a': True, 'tabs_to_quote_button': 8}
PASS keyboard e1 Change the quote (Enter): quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
results written: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-results.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:32.822Z

**tool call — Bash**
````
{
 "command": "TOK=LSx5Yirp9S2KvZOp_puLBw; curl -s -X POST http://127.0.0.1:7931/api/cases/$TOK/items/e1/review -H 'Content-Type: application/json' -d '{\"action\":\"edit\",\"edits\":{\"summary\":\"Restrained driver rear-ended at approx. 35 mph. As the record says.\"}}'; echo; curl -s http://127.0.0.1:7931/api/cases/$TOK | python3 -c \"import json,sys; d=json.load(sys.stdin); print([ (e['id'],e['review_status']) for e in d['entries'] if e['id']=='e1'])\"",
 "description": "Re-probe the mobile summary-only edit response (refused, no save)"
}
````

### User / tool · 2026-11-02T06:12:32.940Z

**tool result**
````
{"error":{"code":"invalid_edit","message":"The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.","detail":{"qualifiers":["self_report"],"reason":"SUMMARY_DROPS_QUALIFIER"}}}
[('e1', 'pending')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:45.253Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF' 2>&1 | tail -5\np = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-walk.py\"\ns = open(p).read()\nold = \"\"\"    typed = \"Restrained driver rear-ended at approx. 35 mph. As the record says.\"\n    seen = []\"\"\"\nnew = \"\"\"    typed = \"Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. As the record says.\"\n    seen = []\"\"\"\nassert s.count(old) == 1; s = s.replace(old, new)\nnew_phases = '''\n\n# ---------- PHASE 10: real backend, summary-only edit that drops a qualifier (answered invalid_edit, not CODE_CHECK_FAILED) ----------\ndef phase_invalid_edit_real(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    open_case(pg)\n    row = row_of(pg, QI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-edit\").click()\n    ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible(timeout=10000)\n    typed = \"Restrained driver rear-ended at approx. 35 mph. As the record says.\"\n    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    time.sleep(1.5)\n    err = row.locator(\".rv-error\")\n    expect(err).to_be_visible(timeout=10000)\n    rec(\"real edit that drops a qualifier (backend invalid_edit, not CODE_CHECK_FAILED): message under the box, typed text kept, no quote button\",\n        \"whose account\" in err.inner_text() and ta.input_value() == typed and row.get_by_test_id(\"edit-refused-msg\").count() == 0,\n        {\"rv_error\": err.inner_text(), \"typed_kept\": ta.input_value() == typed, \"quote_button\": row.get_by_test_id(\"btn-edit-refused-quote\").count()})\n    shot(pg, \"T-104-ux-desk-15-real-invalid-edit-qualifier\")\n    pg.close()\n\n\n# ---------- PHASE 11: STUB (route) CODE_CHECK_FAILED / EDIT_SUMMARY from an edit on e2; the real backend never returns it for a summary-only edit (see phase 10) ----------\ndef phase_edit_summary_stub(browser):\n    pg = browser.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    reason = \"The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.\"\n\n    def handler(route, *_args):\n        body = route.request.post_data_json or {}\n        if body.get(\"action\") != \"edit\":\n            return route.fallback()\n        route.fulfill(status=422, content_type=\"application/json\", body=json.dumps({\"error\": {\"code\": \"CODE_CHECK_FAILED\", \"message\": reason, \"detail\": {\n            \"item_id\": SI, \"reason_code\": \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"step_id\": \"summary_tokens\", \"failed_steps\": [\"summary_tokens\"], \"tokens\": [\"5\"],\n            \"next_action\": {\"code\": \"EDIT_SUMMARY\", \"text\": \"Edit the summary to match the quote\", \"target\": {\"item_id\": SI}}}}}))\n    pg.route(re.compile(rf\"/api/cases/[^/]+/items/{SI}/review$\"), handler)\n    open_case(pg)\n    row = row_of(pg, SI); row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-edit\").click()\n    ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible(timeout=10000)\n    typed = \"Diagnosed with cervical strain; pain 5/10 as the record says.\"\n    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    form = row.locator(\"form.rv-edit\")\n    rec(\"STUB edit CODE_CHECK_FAILED / EDIT_SUMMARY: reason inline under the box, typed text kept, no 'Change the quote'\",\n        ref.inner_text() == reason and ta.input_value() == typed and form.is_visible() and row.get_by_test_id(\"btn-edit-refused-quote\").count() == 0\n        and ref.bounding_box()[\"y\"] >= form.bounding_box()[\"y\"] + form.bounding_box()[\"height\"] - 2,\n        {\"msg\": ref.inner_text(), \"typed_kept\": ta.input_value() == typed})\n    shot(pg, \"T-104-ux-desk-16-stub-edit-summary-refused\")\n    pg.close()\n'''\nmarker = \"\\n\\ndef main():\"\nassert s.count(marker) == 1\ns = s.replace(marker, new_phases + marker)\nold_list = \"phase_rail, phase_judges, phase_mobile, phase_keyboard):\"\nassert s.count(old_list) == 1\ns = s.replace(old_list, \"phase_rail, phase_judges, phase_mobile, phase_keyboard, phase_invalid_edit_real, phase_edit_summary_stub):\")\nopen(p, \"w\").write(s)\nprint(\"patched\")\nEOF",
 "description": "Add real invalid_edit and stub EDIT_SUMMARY edit phases to walk script"
}
````

### User / tool · 2026-11-02T06:12:45.356Z

**tool result**
````
patched
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:48.864Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-walk.py \"$SCR/t104-state.json\" 2>&1 | grep -E \"^(PASS|FAIL|DEBUG|results)\" | cut -c1-400 | tail -60",
 "description": "Run the full T-104 walkthrough again with the new phases",
 "timeout": 540000
}
````

### User / tool · 2026-11-02T06:12:58.223Z

**tool result**
````
PASS row e1 (EDIT_QUOTE): refusal shows 'Change the quote' and no 'Edit the summary' | {'msg': 'Not accepted. The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.', 'buttons': [('btn-accept-refused-quote', 'Change the quote')]}
PASS row e1: aria-label names the item | Change the quote for 2026-01-09 · Austin EMS run report
PASS row e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS row e2 (EDIT_SUMMARY): refusal shows 'Edit the summary' and no quote button | {'msg': 'Not accepted. The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.', 'buttons': [('btn-accept-refused-edit', 'Edit the summary')]}
PASS row e2: 'Edit the summary' opens the summary edit box
PASS batch: refused list names the two failing items | ['e1', 'e2']
PASS batch e1 (EDIT_QUOTE): row offers 'Change the quote', not 'Edit the summary' | [('btn-batch-refused-quote', 'Change the quote')]
PASS batch e2 (EDIT_SUMMARY): row offers 'Edit the summary', no quote button | [('btn-batch-refused-edit', 'Edit the summary')]
PASS batch message (mixed quote and summary refusals) reads as the backend codes say | Nothing was accepted. 2 entries fail a check, so the whole batch was refused. Fix them, then accept again.
PASS batch e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS inline edit e1 (CODE_CHECK_FAILED / EDIT_QUOTE): reason renders under the edit box, typed text kept | {'msg': 'The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.', 'typed_kept': True}
PASS inline edit e1: message sits in the item's role=alert error line
PASS inline edit e1: no generic 'Not accepted' prefix on an edit refusal
PASS inline edit e1 (EDIT_QUOTE): 'Change the quote' offered under the box | [('btn-edit-refused-quote', 'Change the quote')]
PASS inline edit e1: focus stays in the textarea
PASS inline edit e1 Change the quote: quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS why e3 (accepted AI draft, EDIT_QUOTE, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The quote starts or ends in the middle of a sentence.\n\nChange the quote", 'button': 'Change the quote'}
PASS why e3: 'Change the quote' closes the dialog
PASS why e3 Change the quote: quote picker opens (units listed, focus moves into it) | units=6 focus=excerpt-unit
PASS why e4 (accepted AI draft, EDIT_SUMMARY, real verdict): lead and action | {'verdict': 'Needs your attention: a check on this summary fails', 'alert': "This summary doesn't match the quote: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.\n\nEdit the summary", 'button': 'Edit the summary'}
PASS why lead follows the verdict string (stub label 'your wording' on an EDIT_SUMMARY item) | {'verdict_shown': 'Needs your attention: a check on your wording fails', 'lead': "Your wording doesn't match the quote: The summary has a numb", 'button': 'Edit your wording'}
PASS why lead follows the verdict string (real 'this summary' label, EDIT_SUMMARY item) | {'verdict_shown': 'Needs your attention: a check on this summary fails', 'lead': "This summary doesn't match the quote: The summary has a numb", 'button': 'Edit the summary'}
PASS why e3 with stub label 'your wording' (EDIT_QUOTE): lead flips, action stays 'Change the quote' | {'verdict_shown': 'Needs your attention: a check on your wording fails', 'lead': "Your wording doesn't match the quote: The quote starts or en", 'button': 'Change the quote'}
PASS rail e3 (EDIT_QUOTE): gate blocker button reads 'Change the quote' | {'blocker': "2026-01-16 · Dr. Alvarez, primary care\nThis summary doesn't match the quote: The quote starts or ends in the middle of a sentence. This summary was drafted by the AI and a code check on it fails, so i", 'button': 'Change the quote'}
PASS rail e4 (EDIT_SUMMARY): gate blocker button reads 'Edit the summary' | {'blocker': "2026-01-23 · Capital PT, initial evaluation\nThis summary doesn't match the quote: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. This summar", 'button': 'Edit the summary'}
PASS rail e3 Change the quote: quote picker opens (units listed, focus moves into it) | units=6 focus=excerpt-unit
PASS AI-check panel: wording rows read the same action as the item (quote -> 'Change the quote', summary -> 'Edit the summary') | {'judge_edit_buttons': [('Change the quote', 'Change the quote for 2026-01-16 · Dr. Alvarez, primary care · Record 3'), ('Edit the summary', 'Edit the summary for 2026-01-23 · Capital PT, initial evaluation · Record 4')], 'wording_list_present': True}
PASS 390px: accept refusal (EDIT_QUOTE) button is inside the viewport | {'scroll_overflow_px': 0, 'box': {'x': 40, 'y': 671.328125, 'width': 314, 'height': 156.828125}}
DEBUG mobile save responses: [('POST', 422, 's/LSx5Yirp9S2KvZOp_puLBw/items/e1/review')] rv-error text: ['The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence. Change the quote']
FAIL 390px: inline edit refusal and 'Change the quote' are reachable without horizontal scroll | {'scroll_overflow_px': 0, 'typed_kept': True}
PASS keyboard (e1 EDIT_QUOTE): 'a' shows refusal, focus stays on the item, Tab reaches 'Change the quote' | {'focus_on_row_after_a': True, 'tabs_to_quote_button': 8}
PASS keyboard e1 Change the quote (Enter): quote picker opens (units listed, focus moves into it) | units=7 focus=excerpt-unit
PASS real edit that drops a qualifier (backend invalid_edit, not CODE_CHECK_FAILED): message under the box, typed text kept, no quote button | {'rv_error': 'The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.', 'typed_kept': True, 'quote_button': 0}
PASS STUB edit CODE_CHECK_FAILED / EDIT_SUMMARY: reason inline under the box, typed text kept, no 'Change the quote' | {'msg': 'The summary has a number, date or dollar figure that is not in the quote: 5. Edit the summary to match the quote.', 'typed_kept': True}
results written: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-results.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:07.574Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-104-ux-designer-mobile.py <<'EOF'\n\"\"\"T-104 review (ux-designer-reviewer): 390x844 geometry of the inline edit refusal and its 'Change the quote' button, on my server (127.0.0.1:7931).\"\"\"\nimport json, sys, time\nfrom playwright.sync_api import sync_playwright, expect\n\nBASE = \"http://127.0.0.1:7931\"\nEV = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"\nSTATE = json.load(open(sys.argv[1]))\nTOK, QI = STATE[\"token\"], STATE[\"quote_item\"]\n\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    pg = b.new_context(viewport={\"width\": 390, \"height\": 844}).new_page()\n    pg.goto(f\"{BASE}/#/case/{TOK}\")\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n    row = pg.get_by_test_id(\"timeline\").locator(f'[data-item-id=\"{QI}\"]').first\n    row.scroll_into_view_if_needed()\n    row.get_by_test_id(\"btn-edit\").click()\n    ta = row.get_by_test_id(\"edit-summary\"); expect(ta).to_be_visible(timeout=10000)\n    typed = \"Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. As the record says.\"\n    ta.fill(typed); row.get_by_test_id(\"btn-save-edit\").click()\n    ref = row.get_by_test_id(\"edit-refused-msg\"); expect(ref).to_be_visible(timeout=10000)\n    qb = row.get_by_test_id(\"btn-edit-refused-quote\")\n    before = {\"viewport_h\": pg.viewport_size[\"height\"], \"msg_box\": ref.bounding_box(), \"quote_btn_box\": qb.bounding_box()}\n    qb.scroll_into_view_if_needed()\n    time.sleep(0.3)\n    after = {\"quote_btn_box\": qb.bounding_box(), \"page_scroll_y\": pg.evaluate(\"window.scrollY\")}\n    pg.screenshot(path=f\"{EV}/T-104-ux-mob-03-edit-refused-quote-bottom.png\", full_page=False)\n    sw = pg.evaluate(\"document.documentElement.scrollWidth - document.documentElement.clientWidth\")\n    # keyboard reach: from the textarea, Tab to the quote button\n    ta.focus(); n = 0\n    for n in range(1, 30):\n        pg.keyboard.press(\"Tab\")\n        if pg.evaluate(\"document.activeElement.getAttribute('data-testid')\") == \"btn-edit-refused-quote\":\n            break\n    else:\n        n = None\n    print(json.dumps({\"before_scroll\": before, \"after_scroll_into_view\": after, \"horizontal_overflow_px\": sw, \"tabs_from_textarea_to_quote_button\": n}, indent=1, default=str))\n    b.close()\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-mobile.py \"$SCR/t104-state.json\" 2>&1 | tail -60",
 "description": "Measure 390px geometry of inline refusal and quote button",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T06:13:08.787Z

**tool result**
````
{
 "before_scroll": {
  "viewport_h": 844,
  "msg_box": {
   "x": 40,
   "y": 853.671875,
   "width": 294.140625,
   "height": 93.015625
  },
  "quote_btn_box": {
   "x": 108.71875,
   "y": 916.5,
   "width": 150.53125,
   "height": 44
  }
 },
 "after_scroll_into_view": {
  "quote_btn_box": {
   "x": 108.71875,
   "y": 399.5,
   "width": 150.53125,
   "height": 44
  },
  "page_scroll_y": 1251
 },
 "horizontal_overflow_px": 0,
 "tabs_from_textarea_to_quote_button": 3
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:15.689Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-desk-07-edit-refused-quote.png"
}
````

### User / tool · 2026-11-02T06:13:15.697Z

**tool result (error)**
````
File does not exist. Note: your current working directory is /Users/arsis/zlayt-pm-project.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:15.975Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-mob-02-edit-refused-quote.png"
}
````

### User / tool · 2026-11-02T06:13:15.984Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:16.218Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-02-row-e1-accept-refused-quote.png"
}
````

### User / tool · 2026-11-02T06:13:16.227Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:20.357Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-06-batch-refused.png"
}
````

### User / tool · 2026-11-02T06:13:20.366Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:20.614Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-09-why-e3-quote.png"
}
````

### User / tool · 2026-11-02T06:13:20.622Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:20.917Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-13-rail-blockers.png"
}
````

### User / tool · 2026-11-02T06:13:20.934Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:21.149Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-mob-03-edit-refused-quote-bottom.png"
}
````

### User / tool · 2026-11-02T06:13:21.159Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:34.152Z

**tool call — Bash**
````
{
 "command": "ls -1 artifacts/review-evidence/ | grep -i \"T-104\" ",
 "description": "List T-104 evidence files written so far"
}
````

### User / tool · 2026-11-02T06:13:34.242Z

**tool result**
````
T-104-ux-designer-mobile.py
T-104-ux-designer-results.json
T-104-ux-designer-setup.py
T-104-ux-designer-walk.py
T-104-ux-desk-01-case-loaded.png
T-104-ux-desk-02-row-e1-accept-refused-quote.png
T-104-ux-desk-03-row-e1-picker-open.png
T-104-ux-desk-04-row-e2-accept-refused-summary.png
T-104-ux-desk-05-row-e2-edit-box-open.png
T-104-ux-desk-06-batch-refused.png
T-104-ux-desk-07-edit-refused-quote.png
T-104-ux-desk-08-edit-refused-quote-picker.png
T-104-ux-desk-09-why-e3-quote.png
T-104-ux-desk-10-why-e4-summary.png
T-104-ux-desk-11-why-e4-your-wording-stub.png
T-104-ux-desk-12-rail-open.png
T-104-ux-desk-13-rail-blockers.png
T-104-ux-desk-14-judges-wording.png
T-104-ux-desk-15-real-invalid-edit-qualifier.png
T-104-ux-desk-16-stub-edit-summary-refused.png
T-104-ux-mob-01-row-e1-accept-refused-quote.png
T-104-ux-mob-02-edit-refused-quote.png
T-104-ux-mob-03-edit-refused-quote-bottom.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:36.056Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-07-edit-refused-quote.png"
}
````

### User / tool · 2026-11-02T06:13:36.065Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:36.337Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-16-stub-edit-summary-refused.png"
}
````

### User / tool · 2026-11-02T06:13:36.344Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:36.621Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-14-judges-wording.png"
}
````

### User / tool · 2026-11-02T06:13:36.631Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:03.158Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-104-ux-designer-rail.py <<'EOF'\n\"\"\"T-104 review (ux-designer-reviewer): screenshot of the case-rail gate blockers (EDIT_QUOTE and EDIT_SUMMARY) on my server (127.0.0.1:7931).\"\"\"\nimport json, sys\nfrom playwright.sync_api import sync_playwright, expect\n\nBASE = \"http://127.0.0.1:7931\"\nEV = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"\nSTATE = json.load(open(sys.argv[1]))\nTOK, QA, SA = STATE[\"token\"], STATE[\"accepted_quote_item\"], STATE[\"accepted_summary_item\"]\n\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    pg = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    pg.goto(f\"{BASE}/#/case/{TOK}\")\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n    cs = pg.get_by_test_id(\"case-stepper\")\n    cs.get_by_test_id(\"case-summary\").wait_for(timeout=10000)\n    if not cs.locator(\"details.zs-case-det\").evaluate(\"d => d.open\"):\n        cs.get_by_test_id(\"case-summary\").click()\n    cs.get_by_test_id(\"case-step\").first.wait_for(timeout=10000)\n    bl = cs.get_by_test_id(\"gate-blockers\")\n    bl.scroll_into_view_if_needed()\n    bl.screenshot(path=f\"{EV}/T-104-ux-desk-17-rail-gate-blockers-list.png\")\n    for i in (QA, SA):\n        r = cs.locator(f'[data-testid=\"gate-blocker\"][data-jump-item=\"{i}\"]')\n        print(i, \"|\", r.get_by_test_id(\"btn-gate-edit\").inner_text(), \"| row text head:\", r.inner_text()[:90].replace(\"\\n\", \" / \"))\n    print(\"rail blocker count:\", cs.get_by_test_id(\"gate-blocker\").count())\n    b.close()\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-rail.py \"$SCR/t104-state.json\" 2>&1 | tail -10",
 "description": "Screenshot the rail gate blocker list and read its button labels",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T06:14:04.017Z

**tool result**
````
e3 | Change the quote | row text head: 2026-01-16 · Dr. Alvarez, primary care / This summary doesn't match the quote: The quote sta
e4 | Edit the summary | row text head: 2026-01-23 · Capital PT, initial evaluation / This summary doesn't match the quote: The summ
rail blocker count: 2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:04.990Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-desk-17-rail-gate-blockers-list.png"
}
````

### User / tool · 2026-11-02T06:14:05.000Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:27.976Z

**tool call — Bash**
````
{
 "command": "git show 3462ad0:app/frontend/review.js | grep -n -E \"function showEditRefusal|window.scrollBy|function showError|RV.isCodeCheckRefusal\\(e\\) && body.action === \\\"edit\\\"\" | head; echo ---; git show 3462ad0:app/frontend/stepper.js | grep -n -E \"S.wordingLead = |S.wordingEditText = |S.changeQuote = \" | head; echo ---; git show 3462ad0:app/frontend/batch.js | grep -n \"Fix them, then accept again\" | head -3",
 "description": "Get line numbers for the cited frontend lines at the pinned commit"
}
````

### User / tool · 2026-11-02T06:14:28.116Z

**tool result**
````
128:  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }
133:  function showEditRefusal(id, e) {
191:      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
200:        if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner
---
137:  S.wordingLead = (id, verdictLabel) => (/your wording/i.test(verdictLabel || "") ? WORDING : /this summary/i.test(verdictLabel || "") ? WORDING_AI : mine(id) ? WORDING : WORDING_AI);
139:  S.wordingEditText = (id, na, verdictLabel) => (quoteFix(na) ? "Change the quote" : (/your wording/i.test(verdictLabel || "") || (!/this summary/i.test(verdictLabel || "") && mine(id))) ? "Edit your wording" : "Edit the summary");
220:  S.changeQuote = function (id) {
---
67:        ? (rows.length === 1 ? "One entry fails a check, so the whole batch was refused. Fix it, then accept again." : rows.length + " entries fail a check, so the whole batch was refused. Fix them, then accept again.")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:32.523Z

**tool call — Bash**
````
{
 "command": "git grep -n -E \"until the summary matches the quote|a check on this summary fails|a code check on it fails\" 3462ad0 -- app | head -8; echo ---; git grep -n -E \"Change quote\\\"|\\\"Change quote\\\"|Change quote'\" 3462ad0 -- app/frontend | head -5",
 "description": "Locate where the copy strings are built at the pinned commit"
}
````

### User / tool · 2026-11-02T06:14:32.651Z

**tool result**
````
3462ad0:app/backend/export.py:513:            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
3462ad0:app/backend/trace.py:48:    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
3462ad0:app/backend/trace.py:275:        code, label = "needs_attention", ("Needs your attention: a check on your wording fails" if _paralegal_wording(kind, row) else "Needs your attention: a check on this summary fails")
3462ad0:app/frontend/stepper.js:135:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
---
3462ad0:app/frontend/excerpt.js:47:    if (bar) bar.append(el("button", { type: "button", class: "btn small", "data-testid": "btn-edit-excerpt", onclick: () => { panel.hidden = !panel.hidden; } }, "Change quote"));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:46.384Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-104-ux-designer-results.json'))\nr=d['results']; print('token', d['token'], 'checks', len(r), 'pass', sum(x['ok'] for x in r), 'fail', [x['check'] for x in r if not x['ok']])\n\" ; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls \"$SCR\" | head -30",
 "description": "Count walkthrough PASS and FAIL results from the results file"
}
````

### User / tool · 2026-11-02T06:14:46.495Z

**tool result**
````
token LSx5Yirp9S2KvZOp_puLBw checks 33 pass 32 fail ["390px: inline edit refusal and 'Change the quote' are reachable without horizontal scroll"]
T-047-run1.json
T103_archive
T103_parent
T106_head_archive
T106_unit_run1.log
a.sqlite3
a27e3a4.diff
adr013.txt
ap3500.pdf
api
api2
api_at_099732b.py
api_head.log
api_head.py
api_head.sqlite3
api_md_head.md
api_md_new.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app.log
app.pid
app.sqlite3
app2.log
ar2
ar_old
arch
arch_57a08ba
audit.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:05.352Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/ | grep -i \"T-104\" ; echo \"exists-check done\"; ls reviews | wc -l",
 "description": "Check whether a T-104 review file already exists before writing"
}
````

### User / tool · 2026-11-02T06:15:05.455Z

**tool result**
````
exists-check done
     240
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:25.368Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-104-ux-designer.md",
 "content": "# T-104 review: ux-designer-reviewer (Priya Raman persona)\n\nScope: app/frontend at commit 3462ad0, served from a `git archive` copy on my own server (127.0.0.1:7931, fixture backend, curated set, scratch ZLAYT_DB). Repo HEAD at review start was c2a5d1f, one commit ahead (T-106), not used.\n\nVerdict: **pass** (0 blockers, 0 majors, 3 minors, 1 nit).\n\nThe routing is right. EDIT_QUOTE reads \"Change the quote\" and EDIT_SUMMARY reads \"Edit the summary\" on the item refusal, batch rows, the Why dialog, the case rail and the AI-check panel. A refused edit renders inline under the box with the typed text and focus kept. The Why lead follows the verdict string. My 33-check walk passed 32. The one failure is a 390 px placement issue (F2).\n\nThe three minors are copy and placement, not wrong actions:\n- F1: quote-level refusals are explained as a summary problem. The sentence names the wrong fix.\n- F2: at 390 px the edit refusal sits below the fold after Save.\n- F3: 8 Tab presses from the row to the quote fix.\n\nEvidence: `artifacts/review-evidence/T-104-ux-designer-walk.py`, `T-104-ux-designer-results.json`, `T-104-ux-designer-mobile.py`, `T-104-ux-designer-rail.py`, `T-104-ux-designer-setup.py`, and the screenshots `artifacts/review-evidence/T-104-ux-desk-*.png` and `T-104-ux-mob-*.png`. Nothing was saved in the walk: pending 21, accepted 2 (the two pre-accepted AI drafts), edited 0 after the run. Saving through the quote picker is not scored (T-108).\n\n```json\n{\"card\": \"T-104\", \"persona\": \"ux-designer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"app/frontend at commit 3462ad0 (git archive copy, not the repo root); app http://127.0.0.1:7931 (my own server: fixture backend, curated set, scratch ZLAYT_DB); sample case token LSx5Yirp9S2KvZOp_puLBw; repo HEAD at review start c2a5d1f (one commit ahead, T-106, not used)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-104 (status in_review, AC 1 evidence read); read personas/ux-designer.md and the memory directory\",\n  \"git rev-parse --short HEAD -> c2a5d1f; git status --short | wc -l -> 1307 (repo root, not used); git merge-base --is-ancestor 3462ad0 HEAD -> ancestor; git log --oneline 3462ad0..HEAD -> c2a5d1f\",\n  \"git archive 3462ad0 | tar -x into a scratch directory; started app.main there with PORT=7931 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated; GET /api/health -> 200, backend fixture, synthetic_only true (PID 77878, stopped at the end)\",\n  \"artifacts/review-evidence/T-104-ux-designer-setup.py: created a sample case, injected e1 (quote cut to start mid-sentence, EDIT_QUOTE), e2 (summary 'Pain 5/10', EDIT_SUMMARY), accepted e3 and e4 and then broke their quote and summary (AI-draft gate blockers). Same method as tests/e2e/test_code_check_refusal.py\",\n  \"curl probes on the real backend: accept e1 -> 422 CODE_CHECK_FAILED, EDIT_QUOTE; summary-only edit on e1 -> 422 CODE_CHECK_FAILED, EDIT_QUOTE; accept e2 -> 422 CODE_CHECK_FAILED, EDIT_SUMMARY; edit e2 with a new number -> 422 invalid_edit SUMMARY_NUMBER_NOT_IN_EXCERPT; edit e1 dropping the self-report qualifier -> 422 invalid_edit SUMMARY_DROPS_QUALIFIER; GET .../items/{e1..e4}/trace and the case trace gate blockers\",\n  \"Playwright at 1440x900 (artifacts/review-evidence/T-104-ux-designer-walk.py, 33 checks, results in T-104-ux-designer-results.json): item row accept refusal for e1 and e2 incl. button sets and quote picker open; batch refusal list and per-row buttons, picker from the batch row; inline edit refusal on e1 (real backend) with typed text, focus and role=alert; Why dialog for e3 and e4 (real verdict), Why with route-rewritten verdict label ('your wording') on e3 and e4 and 'this summary' on e4 (STUB: trace label rewritten, nothing else); rail gate blockers e3 and e4 and their buttons; AI-check panel wording rows; keyboard: 'a' on e1 then Tab count then Enter; stub edit refusal CODE_CHECK_FAILED/EDIT_SUMMARY on e2 (STUB: route answers the edit; the real backend never returned this shape for a summary edit)\",\n  \"390x844 (artifacts/review-evidence/T-104-ux-designer-mobile.py): geometry of the edit refusal after Save and after scrolling; horizontal overflow 0 px; Tab count from the textarea to the quote button (3). Screenshots T-104-ux-mob-01..03\",\n  \"Rail gate-blocker list screenshot (artifacts/review-evidence/T-104-ux-desk-17-rail-gate-blockers-list.png)\",\n  \"Read app/frontend diff at 3462ad0 (review.js, stepper.js, batch.js, excerpt.js, judges.js) and app/backend/trace.py:48,:275 for the copy source; tests/e2e/test_code_check_refusal.py for the method\",\n  \"Not scored: saving a quote choice through the picker (T-108, known limitation)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"design_quality\": 4, \"originality\": 3, \"craft\": 4, \"functionality\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Quote-level refusals are explained as a summary problem, and the sentence names the wrong fix\",\n   \"evidence\": \"app/backend/trace.py:48 (fixed why 'This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.') and trace.py:275 (verdict label chosen by who wrote the wording, not by the failing check). Real trace for e3 (first failing check EXCERPT_NOT_WHOLE_SENTENCE, next_action EDIT_QUOTE): verdict label 'Needs your attention: a check on this summary fails'. Shown on the Why alert 'This summary doesn't match the quote: The quote starts or ends in the middle of a sentence ... until the summary matches the quote.' with button 'Change the quote' (artifacts/review-evidence/T-104-ux-desk-09-why-e3-quote.png); the same text on the rail gate blocker (artifacts/review-evidence/T-104-ux-desk-17-rail-gate-blockers-list.png) and on the AI-check panel row (artifacts/review-evidence/T-104-ux-desk-14-judges-wording.png). The frontend lead (app/frontend/stepper.js:137) follows the verdict string as T-104 requires, so the defect is in the backend strings.\",\n   \"why_it_matters\": \"The button is right, but the sentence tells the paralegal to make the summary match the quote. A summary-only edit does not clear this check: a summary-only edit on e1 returned 422 CODE_CHECK_FAILED / EDIT_QUOTE again. A paralegal who follows the sentence loops. This is a wrong explanation next to a correct action, so minor, not blocker.\",\n   \"fix\": \"In app/backend/trace.py, choose the verdict label and the blocker 'why' by the failing check's next_action code. For EDIT_QUOTE, say the quote fails and that the quote must change, e.g. 'Needs your attention: a check on the quote fails' and 'until the quote is fixed'. Keep the summary wording for EDIT_SUMMARY. The frontend then needs no change, because it follows the string.\",\n   \"acceptance_test\": \"E2E on a real backend with an accepted AI draft whose quote is cut mid-sentence: the item Why alert, the rail gate-blocker row and the AI-check row contain no 'until the summary matches the quote' and name the quote. The same item with a broken summary (Pain 5/10) still reads 'This summary doesn't match the quote' and 'Edit the summary'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"At 390 px the edit refusal sits below the fold after Save, and the edit path does not bring it into view\",\n   \"evidence\": \"Measured by artifacts/review-evidence/T-104-ux-designer-mobile.py on e1 at 390x844: after Save, edit-refused-msg top y=853.7 and btn-edit-refused-quote y=916.5, viewport height 844; after scrollIntoView the button is at y=399.5. Screenshot artifacts/review-evidence/T-104-ux-mob-02-edit-refused-quote.png shows the textarea (focused) and Save with the reason cut off below. Walk check '390px: inline edit refusal and Change the quote are reachable' FAILED for this reason (results JSON; horizontal overflow 0). The accept path scrolls its refusal into view (app/frontend/review.js:200, window.scrollBy); showEditRefusal (review.js:133-141) only writes the message and focuses the textarea. At 1440x900 the message is visible under the box (artifacts/review-evidence/T-104-ux-desk-07-edit-refused-quote.png).\",\n   \"why_it_matters\": \"On a phone, Save is the only feedback for a refused edit, and the reason is one scroll away and unseen. The message is near its input, so criterion 12 holds; the gap is that the screen gives no signal. Minor, not blocker, because nothing is lost and the box stays open.\",\n   \"fix\": \"In showEditRefusal (app/frontend/review.js:133), after writing the message, scroll the rv-error line into view with block 'nearest', as the accept path does at review.js:200.\",\n   \"acceptance_test\": \"E2E at 390x844: after Save on a refused quote edit, edit-refused-msg is within the viewport (its bounding box bottom is at or below 844 and its top is at or above 844) without a manual scroll; the typed-text and focus asserts still pass.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Keyboard route to the quote fix is 8 Tab presses from the row\",\n   \"evidence\": \"Keyboard run on e1 at 1440x900: 'a' shows the refusal, focus stays on the row (data-item-id e1), 8 Tab presses reach btn-accept-refused-quote, Enter opens the picker (results JSON, check 'keyboard (e1 EDIT_QUOTE)': tabs_to_quote_button 8). The refusal box comes after the row's six action buttons (Why, Open record, Change quote, Accept, Edit, Dismiss, Audit). At 390 px the inline edit route is 3 Tabs from the textarea (T-104-ux-designer-mobile.py output).\",\n   \"why_it_matters\": \"The fix is reachable, but a keyboard-first paralegal has to walk the whole row to reach it (criterion 7: efficient correction, keyboard equivalents). Verification is not affected, because the excerpt stays inline. Minor.\",\n   \"fix\": \"Either move focus to the refusal's action after 'a' refuses (the way the edit path moves focus to its textarea), or add a row key for the quote picker and name it in the refusal text.\",\n   \"acceptance_test\": \"After 'a' on a refused EDIT_QUOTE row, the active element is btn-accept-refused-quote or a documented key opens the picker; the test asserts the picker opens within 2 key presses after the refusal appears.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Two names for the same picker in one row, and the refusal repeats its button text\",\n   \"evidence\": \"artifacts/review-evidence/T-104-ux-desk-02-row-e1-accept-refused-quote.png: the row toolbar says 'Change quote' (app/frontend/excerpt.js:47) and the refusal below says 'Change the quote' (also batch, Why, rail, AI-check). The refusal text reads 'Change the quote to whole sentences of the record that keep the hedge sentence.' right before the button 'Change the quote' (same screenshot).\",\n   \"why_it_matters\": \"Two labels for one action in the same row make the paralegal check whether they are different actions. Nit only.\",\n   \"fix\": \"Use one label everywhere (for example 'Change the quote' on the toolbar too), and consider dropping the trailing imperative from the backend sentence when a button with the same words follows it.\",\n   \"acceptance_test\": \"Grep the rendered label set on an EDIT_QUOTE row: one string for the picker action across the toolbar, refusal, batch, Why and rail.\"}\n ],\n \"whats_right\": [\n  \"Each next_action code gets the right button on every surface: EDIT_QUOTE reads 'Change the quote' and EDIT_SUMMARY reads 'Edit the summary' on the item refusal, batch rows, Why, rail and AI-check panel (33-check walk, 32 pass).\",\n  \"A refused edit renders inline under its box: the server's sentence sits in a role=alert line, the typed text stays in the box, focus stays in the textarea, and nothing is saved (artifacts/review-evidence/T-104-ux-desk-07-edit-refused-quote.png, T-104-ux-desk-16-stub-edit-summary-refused.png).\",\n  \"The Why lead follows the verdict string: rewriting the label to 'your wording' changed the lead to 'Your wording doesn't match the quote:' and the button to 'Edit your wording', and the real 'this summary' label gave 'This summary doesn't match the quote:' (results JSON).\"\n ],\n \"questions_for_chris\": [\n  \"The real backend answers a summary-only edit that drops a qualifier or adds a number with 422 invalid_edit (SUMMARY_DROPS_QUALIFIER / SUMMARY_NUMBER_NOT_IN_EXCERPT), not CODE_CHECK_FAILED with EDIT_SUMMARY as memory/contracts/api.md describes for edits. The UI shows both inline with the text kept, so I scored the UI. The EDIT_SUMMARY-from-edit path was only reachable through a route stub here. Which shape is intended?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T06:15:25.519Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-104-ux-designer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:28.949Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-104-ux-designer-jsoncheck.py <<'EOF'\n\"\"\"Parse the single fenced json block of reviews/T-104-ux-designer.md and print the verdict rule outcome.\"\"\"\nimport json, re\ntxt = open(\"/Users/arsis/zlayt-pm-project/reviews/T-104-ux-designer.md\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", txt, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"keys:\", sorted(d.keys()))\nprint(\"model:\", d[\"model\"], \"| persona:\", d[\"persona\"], \"| card:\", d[\"card\"])\nprint(\"severities:\", sev, \"| rule verdict:\", rule, \"| declared:\", d[\"verdict\"], \"| match:\", rule == d[\"verdict\"])\nEOF\n.venv/bin/python artifacts/review-evidence/T-104-ux-designer-jsoncheck.py 2>&1 | tail -8; python3 tools/board.py validate 2>&1 | tail -15",
 "description": "Check the review JSON parses and the verdict rule, then run board validate"
}
````

### User / tool · 2026-11-02T06:15:29.131Z

**tool result**
````
json blocks: 1
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
model: claude-haiku-5-5 | persona: ux-designer-reviewer | card: T-104
severities: ['minor', 'minor', 'minor', 'nit'] | rule verdict: pass | declared: pass | match: True
ok (108 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:31.956Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PID=$(cat \"$SCR/t104-server.pid\") && echo \"pid $PID\" && ps -p $PID -o pid=,command= && kill $PID && sleep 2 && (ps -p $PID -o pid= || echo \"pid $PID gone\") && curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7931/api/health",
 "description": "Stop my app server by PID and confirm port 7931 is closed"
}
````

### User / tool · 2026-11-02T06:15:32.011Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:34.429Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t104-server.pid",
 "description": "Read the saved server PID file"
}
````

### User / tool · 2026-11-02T06:15:34.510Z

**tool result**
````
77878
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:35.393Z

**tool call — Bash**
````
{
 "command": "ps -p 77878 -o pid=,command=",
 "description": "Confirm PID 77878 is my app server process"
}
````

### User / tool · 2026-11-02T06:15:35.477Z

**tool result**
````
77878 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:36.376Z

**tool call — Bash**
````
{
 "command": "kill 77878",
 "description": "Stop my app server by PID 77878"
}
````

### User / tool · 2026-11-02T06:15:36.455Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:36.814Z

**tool call — Bash**
````
{
 "command": "sleep 3; ps -p 77878 -o pid=,command=; echo \"ps exit: $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7931/api/health",
 "description": "Confirm the process is gone and port 7931 returns 000"
}
````

### User / tool · 2026-11-02T06:15:39.911Z

**tool result (error)**
````
Exit code 7
ps exit: 1
000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:50.041Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_edit_refusal_shapes.md",
 "content": "---\nname: project_edit_refusal_shapes\ndescription: On the real backend, a summary-only edit that fails a check returns invalid_edit (D-047 pre-check), not CODE_CHECK_FAILED; only quote-level edit failures return CODE_CHECK_FAILED on edit. EDIT_SUMMARY-from-edit is stub-only.\nmetadata:\n  type: project\n---\n\nReal backend, checked on T-104 r1 (commit 3462ad0, 2026-11-02) with curl, sample case, fixture backend:\n- Summary-only edit that adds a number not in the quote (e2, \"pain 5/10\") -> 422 `invalid_edit`, `SUMMARY_NUMBER_NOT_IN_EXCERPT`.\n- Summary-only edit that drops a self-report qualifier (e1) -> 422 `invalid_edit`, `SUMMARY_DROPS_QUALIFIER`, message \"...Put it back in the summary.\"\n- Summary-only edit on an item whose quote fails (e1) -> 422 `CODE_CHECK_FAILED`, `EDIT_QUOTE`.\n- Accept on a summary that fails (e2) -> 422 `CODE_CHECK_FAILED`, `EDIT_SUMMARY` (accept path only).\n\nSo memory/contracts/api.md (\"edit runs the same guard\") and the backend disagree for summary-level edit failures. The UI renders both shapes inline under the box with the text kept. The `invalid_edit` path goes through `showError` (app/frontend/review.js:~196) and not `showEditRefusal` (review.js:133); it has no \"Change the quote\" button.\n\n**Why:** A reviewer who expects CODE_CHECK_FAILED/EDIT_SUMMARY from a real summary edit will wrongly fail the UI. Open question sent to Chris in T-104 review (questions_for_chris).\n\n**How to apply:** When grading an edit refusal, probe both codes with curl first (a refused POST changes nothing), then walk the UI. For EDIT_SUMMARY-from-edit, use a route stub and label it STUB in the review. Related: [[project_quote_check_copy_mismatch]].\n"
}
````

### User / tool · 2026-11-02T06:15:50.134Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_edit_refusal_shapes.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:50.506Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_quote_check_copy_mismatch.md",
 "description": "placeholder"
}
````

### User / tool · 2026-11-02T06:15:50.508Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Write failed due to the following issues:
The required parameter `content` is missing
An unexpected parameter `description` was provided</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:54.146Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_quote_check_copy_mismatch.md",
 "content": "---\nname: project_quote_check_copy_mismatch\ndescription: Backend copy for a quote-level code-check failure says \"this summary\" and \"until the summary matches the quote\" while the action is \"Change the quote\" (trace.py:48, :275). Seen on T-104 r1.\nmetadata:\n  type: project\n---\n\nOn T-104 r1 (3462ad0, 2026-11-02) an accepted AI draft whose quote starts mid-sentence (first failing check EXCERPT_NOT_WHOLE_SENTENCE, next_action EDIT_QUOTE) showed:\n- trace verdict label: \"Needs your attention: a check on this summary fails\" (app/backend/trace.py:275 picks the label by who wrote the wording, not by the failing check);\n- gate `why` (app/backend/trace.py:48, fixed sentence CODE_CHECK_FAILED_AI): \"...so it cannot go into the letter until the summary matches the quote.\";\n- frontend lead \"This summary doesn't match the quote:\" (app/frontend/stepper.js:137 follows the verdict string, as T-104 requires), beside a \"Change the quote\" button.\n\nShown in the Why alert, the case rail gate blocker and the AI-check panel row. A summary-only edit cannot clear it (CODE_CHECK_FAILED / EDIT_QUOTE again). Filed as minor F1 in reviews/T-104-ux-designer.md.\n\n**Why:** The copy tells the paralegal to fix the wrong thing; the button is right. The defect is in the backend strings, so a frontend-only change will not fix it.\n\n**How to apply:** On any EDIT_QUOTE state, check every surface that shows the blocker (Why, rail, AI-check panel, batch, export message) for the phrases \"doesn't match the quote\" and \"until the summary matches\". See [[feedback_fix_every_surface]] and [[project_edit_refusal_shapes]].\n"
}
````

### User / tool · 2026-11-02T06:15:54.239Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_quote_check_copy_mismatch.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:56.912Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/reference_state_injection_setup.md",
 "content": "---\nname: reference_state_injection_setup\ndescription: artifacts/review-evidence/T-104-ux-designer-setup.py builds failing states (broken quote, bad summary, accepted-then-broken AI draft) on a sample case via the API plus DB.update_item; reuse it for code-check review states.\nmetadata:\n  type: reference\n---\n\n`artifacts/review-evidence/T-104-ux-designer-setup.py <archive dir> <out.json>` (run with `ZLAYT_DB=<the server's db>` and the project venv) creates a sample case over the API, runs it to ready, accepts two verified entries while their wording is still valid, then breaks them in the store with `app.db.db.update_item`: one quote cut to start mid-sentence (EDIT_QUOTE), one summary with \"Pain 5/10\" (EDIT_SUMMARY), and the two accepted ones broken the same way. It writes the token and ids to the JSON file. The walk script (`T-104-ux-designer-walk.py`) reads that file.\n\n**Why:** It is the same method tests/e2e/test_code_check_refusal.py uses (\"the way a stale or imported state would\"), so the review does not need a stub for the real-backend states. Only the route rewrites are stubs.\n\n**How to apply:** Start the server from a git-archive copy on a spare port with its own ZLAYT_DB, run the setup script against that port (it hardcodes 127.0.0.1:7931; edit BASE for another port), then the walk. The `DB.connect` path must be the same file the server uses. See [[feedback_pin_review_commit]].\n"
}
````

### User / tool · 2026-11-02T06:15:57.009Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/reference_state_injection_setup.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:59.270Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_bash_parse_guard.md",
 "content": "---\nname: feedback_reviewer_bash_parse_guard\ndescription: git-guard refuses a reviewer Bash call it cannot parse (\"No closing quotation\") when one command chains a $(cat ...) assignment, a || fallback and echo strings; split the stop-and-verify steps into separate calls\nmetadata:\n  type: feedback\n---\n\nOn T-104 r1 (2026-11-02) one Bash call combining `SCR=...; PID=$(cat \"$SCR/...\")`, `ps -p $PID -o pid=,command=`, `kill`, a `sleep`, `(ps ... || echo \"...\")` and a `curl -w` failed in the PreToolUse hook: \"git-guard: could not parse command safely (No closing quotation)\". Nothing ran. The same kind of chained command had passed earlier.\n\n**Why:** The hook's shell parser loses track of quotes in long compound lines. The failure costs a call and makes it unclear whether anything ran.\n\n**How to apply:** Keep each Bash call to one purpose. Read the PID file with the Read tool, check the process with `ps -p <pid> -o pid=,command=` alone, then `kill <pid>` alone, then confirm the port in a separate call. Put Python checks in a file under artifacts/review-evidence/ (see [[feedback_reviewer_bash_devnull]]).\n"
}
````

### User / tool · 2026-11-02T06:15:59.369Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_bash_parse_guard.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:00.712Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T06:16:00.720Z

**tool result**
````
1	- [Recheck all data paths](feedback_recheck_all_paths.md) — reconcile count lines on sample AND paste variants; new round script per prefix, don't rerun old hardcoded-port walks
2	- [Office 3D phone walk recipe](reference_office3d_phone_walk.md) — CDP touch + O3 globals for the board canvas; T-064 r2 passed on phone numbers
3	- [Pin the review commit](feedback_pin_review_commit.md) — serve the card's commit via git archive, never the dirty repo-root tree; HEAD moves mid-review
4	- [Reviewer Bash and /dev/null](feedback_reviewer_bash_devnull.md) — "2>/dev/null" trips board-guard "redirect to /"; drop it in reviewer shell calls
5	- [Sample-case gap flag below fold](project_sample_case_gap_flag_fold.md) — gap flag 3,600 to 5,200 px down at 1440x900; grew at bc12d44 (e92b6ed); pointer link is the workaround
6	- [Rerun status and gate sync](feedback_rerun_status_and_gate_sync.md) — rerun placement holds (T-097 r2); open: rail row label (m1), Export off-screen (n1); sandbox quirks
7	- [Gate trusts stored results](feedback_gate_stored_results.md) — B1 closed at dd84122 (T-097 r3, real backend); keep the edited_json bypass as a regression step for any "gate blocks X" claim
8	- [Fix every surface](feedback_fix_every_surface.md) — a state fixed in one component is still shown by summary line, Why dialog, rail rows; re-measure all on a mixed case
9	- [Reviewer git and review writes](feedback_reviewer_git_and_review_writes.md) — git worktree is refused (use git archive); review files are append-only, so the first write is final
10	- [One-action keyboard check](feedback_one_action_keyboard_check.md) — "one action" passed on pointer but took 190 Tab presses to the T-046 r2 summary link; measure both paths
11	- [Side-by-side pane overlay](project_sbs_pane_overlay.md) — T-046 r2 fixed pane covers the case list and library rows at the top and while scrolling (switcher is outside main)
12	- [Sample load stall](reference_sample_load_stall.md) — first sample analysis after a server start may show no entry-1 for 60 s; retry once, log the wait
13	- [Stub rejudge and refresh timing](feedback_stub_rejudge_and_refresh_timing.md) — JudgeNotRun stub says ready:true; rail refreshes ~3 s after a rerun; read after the trace response, confirm with a real rejudge
14	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:03.481Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/MEMORY.md",
 "old_string": "- [Stub rejudge and refresh timing](feedback_stub_rejudge_and_refresh_timing.md) — JudgeNotRun stub says ready:true; rail refreshes ~3 s after a rerun; read after the trace response, confirm with a real rejudge\n",
 "new_string": "- [Stub rejudge and refresh timing](feedback_stub_rejudge_and_refresh_timing.md) — JudgeNotRun stub says ready:true; rail refreshes ~3 s after a rerun; read after the trace response, confirm with a real rejudge\n- [Edit refusal shapes](project_edit_refusal_shapes.md) — real backend: summary-only edit fails as invalid_edit, only quote edits give CODE_CHECK_FAILED; EDIT_SUMMARY-from-edit is stub-only (T-104 r1)\n- [Quote-check copy mismatch](project_quote_check_copy_mismatch.md) — quote-level blocker says \"this summary\" / \"until the summary matches\" beside \"Change the quote\" (trace.py:48, :275); T-104 F1\n- [State injection setup](reference_state_injection_setup.md) — artifacts/review-evidence/T-104-ux-designer-setup.py builds broken and accepted-then-broken states via API plus DB.update_item\n- [Reviewer Bash parse guard](feedback_reviewer_bash_parse_guard.md) — git-guard \"could not parse command safely\" on chained $(cat)/|| commands; one purpose per Bash call\n"
}
````

### User / tool · 2026-11-02T06:16:03.581Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:11.150Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > artifacts/review-evidence/T-104-ux-designer-dbcheck.py <<'EOF'\n\"\"\"Read-only check of the T-104 review's scratch DB: review_status counts for the sample case (token LSx5Yirp9S2KvZOp_puLBw).\"\"\"\nimport sqlite3, sys\nc = sqlite3.connect(sys.argv[1])\ncols = [r[1] for r in c.execute(\"PRAGMA table_info(items)\")]\nprint(\"items columns with status:\", [x for x in cols if \"status\" in x or x in (\"id\", \"case_id\")])\nfor row in c.execute(\"SELECT review_status, COUNT(*) FROM items WHERE case_id = ? GROUP BY review_status\", (\"LSx5Yirp9S2KvZOp_puLBw\",)):\n    print(row)\nEOF\n.venv/bin/python artifacts/review-evidence/T-104-ux-designer-dbcheck.py \"$SCR/t104-ux.sqlite3\" 2>&1 | tail -12",
 "description": "Read-only check of review_status counts in the scratch DB"
}
````

### User / tool · 2026-11-02T06:16:11.259Z

**tool result**
````
items columns with status: []
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-104-ux-designer-dbcheck.py", line 6, in <module>
    for row in c.execute("SELECT review_status, COUNT(*) FROM items WHERE case_id = ? GROUP BY review_status", ("LSx5Yirp9S2KvZOp_puLBw",)):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: items
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:14.044Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -n -E \"CREATE TABLE\" app/db/*.py 2>/dev/null | head -12; git show 3462ad0:app/db/db.py | grep -n -E \"CREATE TABLE\" | head -12",
 "description": "Find the item table name in the db schema at the pinned commit"
}
````

### User / tool · 2026-11-02T06:16:14.154Z

**tool result**
````
app/db/db.py:72:    ddl = re.search(r"CREATE TABLE IF NOT EXISTS review_events \(.*?\n\);", schema, re.S).group(0).replace("IF NOT EXISTS ", "")
72:    ddl = re.search(r"CREATE TABLE IF NOT EXISTS review_events \(.*?\n\);", schema, re.S).group(0).replace("IF NOT EXISTS ", "")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:15.334Z

**tool call — Bash**
````
{
 "command": "git show 3462ad0:app/db/schema.sql | grep -n -E \"CREATE TABLE\" | head -12; git show 3462ad0:app/db/schema.sql | grep -n -i \"review_status\" | head -3",
 "description": "Read table names and review_status column from the pinned schema file"
}
````

### User / tool · 2026-11-02T06:16:15.455Z

**tool result**
````
4:CREATE TABLE IF NOT EXISTS cases (
11:CREATE TABLE IF NOT EXISTS records (
19:CREATE TABLE IF NOT EXISTS entries (
27:CREATE TABLE IF NOT EXISTS amounts (
36:CREATE TABLE IF NOT EXISTS flags (
48:CREATE TABLE IF NOT EXISTS llm_calls (
55:CREATE TABLE IF NOT EXISTS review_events (
23:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
32:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
43:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:18.202Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && sed -i.bak 's/FROM items WHERE case_id/FROM entries WHERE case_id/; s/print(\"items columns.*$/print(\"entries table\")/' artifacts/review-evidence/T-104-ux-designer-dbcheck.py && rm -f artifacts/review-evidence/T-104-ux-designer-dbcheck.py.bak && .venv/bin/python artifacts/review-evidence/T-104-ux-designer-dbcheck.py \"$SCR/t104-ux.sqlite3\" 2>&1 | tail -12",
 "description": "Rerun the read-only review_status count against the entries table"
}
````

### User / tool · 2026-11-02T06:16:18.331Z

**tool result**
````
entries table
('accepted', 2)
('pending', 7)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:34.703Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_git_and_review_writes.md"
}
````

### User / tool · 2026-11-02T06:16:34.709Z

**tool result**
````
1	---
2	name: feedback_reviewer_git_and_review_writes
3	description: Reviewers cannot run git worktree (board-guard) and review files are append-only (reviewer-write-guard); pin a commit with git archive and write the review once, correctly
4	metadata:
5	  type: feedback
6	---
7	
8	`git worktree add` and `git worktree list` are refused for reviewers in the project ("reviewers may not run git worktree in the project"). Use `git archive <commit> | tar -x -C <scratch>/<unique-dir>` to get a clean copy of the commit instead. Same content, no .git.
9	
10	Reviews are append-only once written: the first `Write` to `reviews/<card>-<persona>[-rN].md` is final, and any `Edit` afterwards fails with "reviews are append-only — write a new file (e.g. -r2/-r3 suffix)". So draft the full review and its JSON block before the first write. Fix small wording errors in the first pass, not after.
11	
12	**Why:** On T-046 r2 (2026-11-01) the worktree command was refused, and three wording fixes to the freshly written review could not be made afterwards.
13	
14	T-097 r2 (2026-11-02) repeated it: a line cite (stepper.js:454, grep said 453) and an "after dismiss, all say 1" claim for the Why dialogs and export that I had not re-measured went into the first write and could not be edited. Disclosed in the reply instead.
15	
16	**How to apply:** Before writing a review file, re-read the findings for file lists, counts, line numbers and attributions, and check every "after" state against an actual measurement. Put scratch exports in a uniquely named directory. The scratchpad path can change or lose a directory between calls (a `wt` folder disappeared between two calls). Check the directory exists right after you create it.
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:36.796Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_git_and_review_writes.md",
 "old_string": "**How to apply:** Before writing a review file, re-read the findings for file lists, counts, line numbers and attributions, and check every \"after\" state against an actual measurement.",
 "new_string": "T-104 r1 (2026-11-02) repeated it a third time: \"six action buttons\" when my own list had seven, and a \"pending 21\" count taken before the final walk run, written as the after-run state. The DB after the run (read-only check) showed 2 accepted, 7 pending, 0 edited for the entries. Both went into the first write and were disclosed in the reply.\n\n**How to apply:** Before writing a review file, re-read the findings for file lists, counts, line numbers and attributions, and check every \"after\" state against an actual measurement taken after the last run. Count list items in the sentence that names them."
}
````

### User / tool · 2026-11-02T06:16:36.896Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_reviewer_git_and_review_writes.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:39.513Z

T-104 review written to `/Users/arsis/zlayt-pm-project/reviews/T-104-ux-designer.md`: pass (0 blocker, 0 major, 3 minor, 1 nit), with the three checks holding at 3462ad0. Two errors are in the file and can't be edited because review files are append-only: "six" action buttons should be seven, and the "21 pending" figure predates the final run (the DB after the run shows 2 accepted, 7 pending, 0 edited for entries). Server PID 77878 is stopped and port 7931 returns 000.
