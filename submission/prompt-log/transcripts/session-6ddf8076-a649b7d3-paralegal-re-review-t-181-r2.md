# Subagent: Paralegal re-review: T-181 r2 (Paralegal re-review: T-181 r2)

Source: `agent-a649b7d3a918e435a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T22:51:36.683Z

Re-review T-181, round 2 of the guided UI, in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The fix commit is 9ab8cae. Read reviews/T-181-paralegal.md (your round 1) and the card handoff, which includes one backend wording gap, the letter's undated-ledger line, that the worker left.

Run a `git archive 9ab8cae` copy in demo mode on your own port, and stop only your PID afterward.
- Verify both majors: the disputed-line label and the Bates fill-in wording.
- Re-run the sample case end to end, timed.
- Judge whether the undated-ledger letter line is a problem for a demand letter.

Put screenshots in artifacts/review-evidence/T-181-paralegal-r2/. Write reviews/T-181-paralegal-r2.md in D.2 format, applying the verdict rule. Reply in 2 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:39.295Z

**tool call — Bash**
````
{
 "command": "cat personas/paralegal.md | head -c 200 && echo && cat .claude/agent-memory/paralegal-reviewer/t181-guided-ui-patterns.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md",
 "description": "Read persona header and relevant memories"
}
````

### User / tool · 2026-11-02T22:51:39.390Z

**tool result**
````
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.
---
name: t181-guided-ui-patterns
description: T-181 guided 4-step UI (26287b9) paralegal review: changes (2 majors: disputed-item grey box says borrowed sentence "not in any line"; Bates helper one-number-per-record unstated); selectors, demo vs local library, keyboard traps
metadata:
  type: project
---

T-181 review (reviews/T-181-paralegal.md, commit 26287b9). Verdict: changes, with 2 majors, 7 minors and 2 nits. Sample truths are all correct. verify_quickly is 4.

**Majors**
- On lib11 e1, e2 and e4 (JUDGE_PARTIAL), the line borrows a sentence from outside the quote. The grey box (step2.js:66) lists that same sentence under "Also in this record, not in any line". The dispute text never says which words.
- The Bates helper (step4.js:148) numbers first number + record number - 1 (api.md:115) and does not say so on screen.

**Minors to re-check next round**
- e9 refusal says "none of them is in Billed charges", but Step 3 can count the ledger lines.
- A on a refused item moves focus to answer-no, so A then Space dismisses.
- lib11 title row says "not written by an AI model" while the cards say "AI draft" (review.js:45 uses health).
- Undated ledger lines show the statement date under "Date".
- The Step 3 dispute line has no direction.
- The conflict record-7 highlight is below the fold.
- Public /new promises "our test cases".

**Mechanics**
- Public demo mode (ZLAYT_MODE unset):
  - GET /api/cases 404 is by design (it causes a console error on every page).
  - The home list is localStorage, so use a Playwright persistent profile (launch_persistent_context) to keep cases between runs.
  - /api/library is local-only. Run a second ZLAYT_MODE=local copy for library cases.
- Selectors:
  - Home and new case: `btn-continue` is an A, not a button; `case-card[data-title=...]`, `btn-new-case`, `tile-library`, `library-<id>`, `btn-read`, `btn-draft`.
  - Review frame: `answer-yes`/`answer-no`/`btn-third`/`btn-later`/`btn-back`; `check-compare`, `check-separate`; `edit-summary`, `edit-note`.
  - Step 4: `letter-text`, `notes-text`, `btn-download-letter`/`btn-download-notes`/`btn-copy-letter`, `cfg-exhibit`/`cfg-bates-prefix`/`cfg-bates-start`/`btn-save-cfg`; `step-1..4`.
  - Page regions: `.titlebar`, `.work .card`, `.actions`.
- Keys: A, D and E are document-level and work after a reload with focus on BODY. There is no save shortcut in a textarea, so Tab to Save and press Enter. On a disabled Yes, A focuses the unticked checkbox; Space ticks it; A accepts.
- The guided e2e suite runs from the archive: E2E_REQUIRE_DB=1 pytest tests/e2e/guided gave 100 passed in about 2.5 min.
- board-guard reads `->` inside a grep pattern as a redirect. Avoid ">" in patterns.
- Don't put a URL in a screenshot file name: it creates `http:` directories.

**Why:** these took a full run to learn. Next round, check the two majors first.
**How to apply:** reuse artifacts/review-evidence/T-181-paralegal/h.py (T181_BASE env var) and the s05, s13 and s14 scripts. Related: [[gate-m3-patterns]], [[reviewer-run-pitfalls-pass4]], [[feedback_reviewer_tooling_quirks]].
---
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.
- T-118 (2026-11-02): the Write tool is refused for the session scratchpad (reviewer-write-guard), and board-guard refuses `mkdir` there. A Bash `git archive | tar -x` into the scratchpad still worked. Put scripts and output dirs under artifacts/review-evidence/ and run archive copies from the scratchpad. Run them with `.venv/bin/python -I` and a runner that puts the archive root first on sys.path.

**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
---
name: reviewer-tooling-quirks
description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
metadata:
  type: feedback
---

Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.

**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.

**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].

## T-077/T-078 r2 additions (2026-11-01)
- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep ("exceeds complexity limits"). Strip tags and search in a python script under artifacts/review-evidence/.
- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.
- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.
- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.
- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.

## T-077 r3 additions (2026-11-01)
- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused ("reviews are append-only"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.
- A bash `python3 -c` with `\`\`\`` and `\d` escapes was denied by git-guard ("could not parse command safely (No escaped character)"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.

## T-114 additions (2026-11-02)
- board-guard reads a redirect target written as `$VAR/file` inside the same command as "writes outside reviews/"; the same redirect with a literal absolute path passes. Use literal paths for `> file` redirects, and put server start/stop in their own calls.
- git-guard rejected a `kill $(cat pidfile)` chain with echo quotes ("No closing quotation"). Use the PID number directly.
- `timeout` is not installed (already noted); `python3 tools/board.py validate reviews/<file>` works and printed "ok (1 file(s))".

## T-116 r2 additions (2026-11-02)
- `reviewer-write-guard` also refuses Write to the session scratchpad ("reviewers write only under reviews/ or artifacts/review-evidence/").
  Put probe copies, extracted archives and JSON checkers under artifacts/review-evidence/ (run with `.venv/bin/python -I`). `git archive`
  extraction into the scratchpad via Bash worked.
- The review file was refused a second write once it existed, so a wrong body sentence (I wrote "a scratchpad archive path that no longer
  exists" without checking it, and mislabeled a record) could not be fixed. Before the single Write: `ls` every path and grep every record
  label you quote.
- `bash python3 -c "... \`\`\` ..."` was denied again by git-guard. The JSON check now lives in artifacts/review-evidence/<card>-paralegal-r2-jsoncheck.py.

## T-114 r2 additions (2026-11-02)
- `nohup .venv/bin/python -m app.main ... &` then `kill $!` left the listener alive: the launcher PID exited, and the server
  (a child, re-parented to launchd, ppid 1) kept 7881 open and returned 200. Always `lsof -iTCP:<port> -sTCP:LISTEN -nP` after a
  kill, kill the listener PID too, and confirm `curl` returns 000. Name both PIDs in the review scope.
- reviewer-write-guard refused an Edit on reviews/T-114-paralegal-r2.md (append-only). A wrong scope PID could not be fixed; it went into the final reply.
  Before the single Write, check every PID, path and count with a command, not from memory.
- The board validator only checks files under reviews/. Pre-check a draft JSON with a script in artifacts/review-evidence/ (T-114-r2-paralegal-jsoncheck.py).

## T-116 r3 additions (2026-11-02)
- The r3 review was written once and then contained one wrong claim (a grep "returns 1 from the H3V5 line only" that was actually the line-29
  orchestrator note). Edit on the existing review was refused by `reviewer-write-guard`, so the erratum went into the final reply instead.
  Rule: before the single Write, run the exact grep again and quote its line numbers; do not describe a match you have not printed.
- `python3 -c` with `\`\`\`json` in the string was denied by git-guard again (parse error). The JSON check is `artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py`
  run with `.venv/bin/python -I <script> <review>`; it works for any review path.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider` keeps the dirty project tree free of new .pytest_cache and .pyc writes.

## T-120 r4 additions (2026-11-02)
- git-guard denies `git show "$c:$f"` and any git call with a shell variable in the subcommand or a `for` loop with `${var%%:*}` ("dynamic git subcommand is not allowed", "unresolved variable in command position"). Use literal git commands, or a script under artifacts/review-evidence/ run with `.venv/bin/python -I` (T-120-r4-archive-check.py does this).
- The Write tool and board-guard accept a `cp` of a finished draft from artifacts/review-evidence/ to reviews/<new file>; that let me proof a draft JSON with the jsoncheck and then publish the identical text in one step.
- `kill` by PID, then `lsof -iTCP:<port> -sTCP:LISTEN -nP` (exit 1 = closed) and `curl` 000, worked for four server pairs.

## T-120 r2 additions (2026-11-02)
- The guard refused Edit on reviews/T-120-paralegal-r2.md right after the single Write (the name has no -rN suffix, so it is treated as existing and append-only). Two wording slips were found after the Write: "lib02 and lib11 keep their prior flags" (I had not compared them to the pre-T-120 build) and "r2 handoff" (the line is the r2 backend note). They could not be fixed in the file; they went into the one-line reply.
- Before the Write, check each "keeps / still / unchanged" claim against a run you have actually done, not against memory of the build.

## T-060 pass 5 additions (2026-11-02)
- Playwright `new_page` with a fresh browser context is a fresh visit, not a reload; a same-page `pg.reload()` does restore the case. Probe a reload in the same page.
- Letter keys do nothing until an item is selected: after opening a case, click Start review (or a row edge) before j, a, d.
- Probe scripts that walk with j/a can stop early because `a` auto-advances within a kind; check the focus item after every key and reach skipped items with k or j, not by assumption.
- A ```json regex that captures a trailing colon in an evidence path reports a false "missing path"; the file exists. Strip `:` in the checker.
- Write the draft under artifacts/review-evidence/<card>-paralegal-pass5/, run the jsoncheck, then `cp` to reviews/ in one Bash call; board.py validate returned "ok (1 file(s))".
---
name: reviewer-run-pitfalls-pass4
description: T-060/T-114 pass-4 run pitfalls: HEAD moves mid-review (pin by hash, run both if brief says HEAD and card names a commit); venv path relative from subdirs (exit 127); sed -i blocked again; Playwright selectors for case list, disclosure, confirm-date radios; reload restores the case
metadata:
  type: reference
---

- HEAD moved during the review: 433ac1c became f7829c1 while I worked (other agents commit). Record the hash you archived with `git rev-parse --short HEAD` at the start AND `git archive <hash>`. When the brief says HEAD and the card names a commit (e293daa), run both and say which commit each finding applies to. Check `git diff --stat <card-commit> HEAD -- app/frontend` (empty = same UI).
- Server launch: `env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=<p> HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/<card>-paralegal-pass4-serve.py <archive_root>` (runpy, puts the archive root first on sys.path). Background launch: the launcher task exits 0 while the listener lives; get the listener PID with `lsof -iTCP:<p> -sTCP:LISTEN -nP`, kill by number, confirm curl = 000. Port 7860 is the live dev app; never touch it.
- `.venv/bin/python` is relative: from artifacts/review-evidence/<card>/ it exits 127. Run from repo root.
- `sed -i` is refused by board-guard again (pass 4). Use the Edit tool on scripts and memory; check `grep -c` after.
- Playwright selectors (e293daa/HEAD): case list buttons are `[data-testid=case-<token>]`; library entries `[data-testid=library-case_lib09_spanish_interpreter_espalda]` sit inside a collapsed disclosure: click `summary:has-text('synthetic library')` first. The lib09 names repeat ("Spanish-language records, back pain") and differ only by token: never pick by name. Date step: `button:has-text('1 date to confirm')`; radios via `get_by_label("March 5, 2026")`; confirm `get_by_role("button", name="Confirm date")`; there is NO `form[data-testid=confirm-date]` in this build. Gap notice `[data-testid=gap-change-note]`; dismiss it `[data-testid=btn-dismiss-gap-note]`. Dismissed entries group `[data-testid=dismissed-summary]`. Export `[data-testid=btn-export]`, letter `[data-testid=export-letter]` (a PRE, read innerText not value), copy `[data-testid=btn-copy-letter]`, download `[data-testid=btn-download-letter]`.
- Keyboard: `a` on a flag or amount acts on it; `d` on a flag dismisses without a reason prompt; `e` opens the textarea only when focus is on the row, and Ctrl+Enter saves.
- Reload restores the last case view (no paste page), so a probe that expects the paste box after reload will time out. Use the case list or continue on the restored case.
- Output discipline: write every probe's output with `> file` in the same call; console-only numbers do not count as evidence when the review quotes them.
- Review files are write-once: proofread every line reference with grep before the single Write (api.md:341 D-045b checked; the erratum route is the final reply).

Why: all of these cost a probe rerun or an unfixable review line during the T-060/T-114 pass-4 run.
How to apply: start each Playwright run with `curl` on the port, confirm the archive hash, and keep one helper module per card. Related: [[reviewer-tooling-quirks]], [[reviewer-api-shape-gotchas]], [[t060-pass4-state-patterns]], [[t114-r3-gap-change-persistence]].
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:41.330Z

**tool call — Bash**
````
{
 "command": "cat personas/paralegal.md | sed -n '1,400p' | wc -l && diff <(sed -n '1,500p' personas/paralegal.md) /dev/null | head -0; git rev-parse --short HEAD; git log --oneline -5; python3 tools/board.py show T-181 | tail -60",
 "description": "Check persona length, git state, card"
}
````

### User / tool · 2026-11-02T22:51:41.502Z

**tool result**
````
      84
head: illegal line count -- 0
9ab8cae
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
dfd9b11 docs(submission): NEEDS_CHRIS publish-from-snapshot item, T-193, row 8 to P2
3feb096 test(backend): T-177 r4 e2e: golden notes normalize the prepared disclosure line; classic tag tooltip stays exempt until the frontend card
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: ["T-180"]
created_by: "orchestrator"
created_at: "2026-11-02T20:32:49Z"
updated_at: "2026-11-02T22:51:29Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T22:25:37Z"
rounds: 1
commits: ["f3d42a2", "848bbad", "3944cc2", "26287b9", "9ab8cae"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-181-paralegal.md", "at": "2026-11-02T22:25:17Z"}
  - {"persona": "ux-designer-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-181-ux-designer.md", "at": "2026-11-02T22:30:00Z"}
ac:
  - {"n": 1, "text": "every screen in docs/GUIDED_UI_SPEC.md built; a first-time user finishes the sample case to a downloaded letter with no instructions; old /classic e2e still green; new tests/e2e/guided/ suite green; screenshots", "done": true, "evidence": "r2 commit 9ab8cae from git archive of the commit tree, E2E_REQUIRE_DB=1: tests/e2e/guided + test_no_console_errors + test_demo_provenance 134 passed (incl. test_round2.py, public-server first-paint test now a hard assertion after T-197)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:32:52Z orchestrator: assigned: frontend
- 2026-11-02T20:33:17Z frontend: claimed
- 2026-11-02T20:34:27Z orchestrator: Guided UI must send version + expected_status on every review POST (T-178 stale-tab 409, see api.md) and show the 409 message with a reload of the item; carry D-066 (disputed accept needs the compare confirm) and D-067 (no narrative).
- 2026-11-02T21:04:53Z orchestrator: Guided UI provenance: read models.generator_prepared / item.prepared and use the D-065 badge + tooltip and 'Prepared answer' tag (T-177 r2, 4fcf9cd).
- 2026-11-02T21:05:43Z orchestrator: Build must fix the T-180 review majors (reviews/T-180-ux-designer.md): primary action of every step above the fold at 1440x900 (Read the records, Draft the timeline, Copy/Download letter) - use a sticky action bar; 390px: show enough of the record (collapsible header, not a 122px window) and Undo fully visible; build the paste/upload screen with plain errors, and in demo mode do not offer Paste/Upload as if they work (explain + Open the sample / Choose a library case); no jargon on decision screens ('second check' -> 'a second AI check', no 'model's quote', no 'itemized service line'). Also fold the 7 minors.
- 2026-11-02T21:26:32Z frontend: SCAFFOLD COMMITTED f3d42a2, ready for the two step builders. Verified from git archive with E2E_REQUIRE_DB=1: full tests/e2e 431 passed 1 skipped (classic at /classic + 12 guided shell tests); the committed tree also passed the pre-commit smoke. SERVING: / = app/frontend/guided (real paths, history.pushState; server answers index.html for any extension-less non-file path via GuidedFiles in api.py; /api and /classic never fall through); /classic = old screen, unchanged. e2e conftest: SERVER (root, API) and BASE = SERVER+'/classic' (classic specs unchanged). FILE BOUNDARIES (one file per step, none shared except review.js): Builder A (Home + Step 1 + Step 4): home.js/.css, step1.js/.css (registers G.pages.new AND G.pages.records), step4.js/.css (G.pages.letter). Builder B (Step 2 + Step 3): step2.js/.css (G.pages.timeline), step3.js/.css (G.pages.bills), review.js/.css (shared frame helpers, B only). Nobody edits index.html, core.js, app.js or styles.css except to fix the shell (tell frontend). styles.css = the mockup guided.css verbatim plus shell additions, so every mockup class (.card, .actions-in, .btn.answer, .tile, .ccard ...) already exists. PAGE CONTRACT (header of app.js): G.pages.<home|new|records|timeline|bills|letter> = async (ctx) => cleanup?; render into ctx.view (display:contents, children become body children: frame pages append .titlebar/.work/.actions, page pages append one main.wrap); resolve after first paint (shell then sets data-ready on [data-testid=view]); ctx = {route, token, step, query, case (GET case, loaded by the shell), health, signal, view, layout('frame'|'page') (done screens call ctx.layout('page')), go(path,{replace}), refresh() (re-GET case; redraws step bar + header), setStepStatus(n,text,state?), setCaseTitle, setTitle}. SHELL PROVIDES: banner + demo pill + footer (D-065 amended wording, G.provenance() gives {kind,label,note,hours}), header, step bar with live statuses from G.steps.states (spec 9.1/9.2; also accepts a /api/cases row, so Home reuses it), theme, G.api (plain-message ApiError: 0 offline, 404, 413, 429, 5xx never show raw text), G.store, G.url.records/timeline/bills/letter/step, G.h (no innerHTML), G.errorBlock. Throws become the plain error block + Try again. RULES: textContent only; no inline style attributes (CSP style-src 'self'): size things with el.style.width=... from code; CSP otherwise unchanged. TESTS: tests/e2e/guided/test_shell_smoke.py has helpers watch(page) (console/page/http/requestfailed errors), go(page,path) (waits for data-ready), rect, chrome; put each builder's specs in their own tests/e2e/guided/test_<name>.py. Test ids set by the shell: banner-synthetic, app-header, demo-badge, btn-theme, step-bar, step-1..4 (aria-current=step; locked step is a span aria-disabled), view (data-route, data-ready), footer-note, case-title, btn-your-cases, page-error, btn-retry, link-home. NOTES: (1) real paths replaced the hash routes I was first told to build, because spec section 1 requires them. (2) D-065 was amended after the spec: prepared pill tooltip and footer use 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' not the spec 2.3 sentence about the evaluation report. (3) Step 4 status 'Ready' comes from review.ready_to_export (row export_ready); a page that knows the blocker count can override with ctx.setStepStatus(4,'1 problem','attn'). (4) The worktree api.py now holds another worker's uncommitted ClassicFiles/limits hunks; my commit contains only the GuidedFiles hunk, so whoever commits those must keep the /classic mount lines. (5) Changed tests/e2e/test_count_duplicate.py (goto adds /classic) and tools/check_index_imports.py (smoke list = no_console_errors + guided shell smoke).
- 2026-11-02T21:31:13Z orchestrator: From T-182 installer: F4 first Analyze/Read click lost on cold load and F11 404s on page load (reviews/T-182-installer.md) - guided UI must not repeat these; the first-time verification checks them.
- 2026-11-02T21:33:37Z frontend: frontend-B started: step2/step3/review (js+css) + tests/e2e/guided/test_step2.py, test_step3.py. Plan: review.js holds the shared one-item engine (G.review.run); phones collapse the step bar behind a 'Step N of 4' toggle in the title row (review.css only, overlay so no layout shift). Shell-change requests will be listed in notes.
- 2026-11-02T21:37:48Z orchestrator: Builder A: add tests/e2e/guided/test_golden_path.py::test_demo_sample_reachable_from_root (demo mode: / -> Open the sample -> Step 2 shows entries). The orchestrator will add it to the pre-commit FRONTEND_SMOKE so / can never again ship unreachable (T-182 r2 lesson).
- 2026-11-02T21:39:12Z frontend: frontend-A: Home + Open the sample landed in the working tree (home.js/css, step1.js/css incl. records page, step4.js/css); test_golden_path.py::test_demo_sample_reachable_from_root and test_home.py pass (public-mode stub: empty list -> Open the sample case -> records -> Draft -> Step 2). SHELL BUG for the shell owner: app.js drawBanner does f.replaceChildren(span, p.hours ? span : null) -> the footer shows the text 'null' (replaceChildren stringifies null); filter nulls. Committing after step1/step4 specs.
- 2026-11-02T21:52:27Z frontend: frontend-A: COMMITTED 848bbad (Home + Step 1 + Step 4, 4 specs). Verified from a git archive of the commit tree with E2E_REQUIRE_DB=1: test_home + test_step1 + test_step4 + test_shell_smoke + test_no_console_errors = 51 passed. test_golden_path::test_demo_sample_reachable_from_root passes in the working tree with Builder B's step 2 but needs it (HEAD still has the stub). Notes for the shell owner: (1) app.js drawBanner footer shows the text 'null' (replaceChildren(null) stringifies); (2) test_shell_smoke::test_links_route... clicks btn-next on the bills page, which is Builder B's page now. Screenshots at 1440/390 in artifacts/screenshots/guided/ (home, home-empty, new-demo, step1-*, step4-*). Shared: G.sbar (sticky action bar, step1.js, CSS in step1.css), G.cases (home.js), G.longDate.
- 2026-11-02T21:56:03Z frontend: frontend (shell owner): 3944cc2 footer 'null' fixed in app.js (filter before replaceChildren) + test_footer_and_chrome_never_print_the_word_null in test_shell_smoke; verified from a git archive: smoke + test_home + test_no_console_errors 25 passed. btn-next bills test left to Builder B.
- 2026-11-02T22:07:43Z frontend: frontend-B COMMIT 26287b9: Step 2 + Step 3 + review.js/css (+ test_step2.py 28, test_step3.py 23, screenshots artifacts/screenshots/guided/step2-*, step3-* at 1440 and 390). Verified from a git archive of the commit tree with E2E_REQUIRE_DB=1: tests/e2e/guided + test_no_console_errors 104 passed (incl. test_golden_path). Notes: (1) shell-smoke test_links_route clicked btn-next on bills; changed to the step-4 link (one line, tests/e2e/guided/test_shell_smoke.py). (2) D-066: compare box sends compared:true; an unexpected 422 COMPARE_REQUIRED re-renders with the compare box (verdict from detail.verdict), never a raw error; tests for entries, flags, amounts. (3) Accept-all: the guided UI has NO batch/accept-all by design (spec 11; D-059 charges are never batched), so there is nothing to skip; test_there_is_no_accept_all asserts no control exists and that the server refuses a batch with a disputed item and a charge. Tell me if you want an accept-all added instead. (4) Edit with both a new quote and new wording is ONE call {edits:{excerpt,summary}}: two calls (quote first) fail when the old wording has a number missing from the new quote (spec 5.3 said two calls; api.md should say one call works). (5) Phones (<=760px): the step bar folds behind a 'Step N of 4' toggle in the title row (overlay, no layout shift); the line card scrolls as one box. Shell change suggested: none required. Residual: 1366x768 line-card body is ~110px (scrolls); the D-065 amended footer sentence says 'against its quote' (shell text, shown in the title row).
- 2026-11-02T22:08:53Z frontend: moved in_progress -> in_review: AC1 first-time-user finish is what this review verifies; e2e and screenshots done
- 2026-11-02T22:08:53Z orchestrator: review dispatched: ux-designer-reviewer, paralegal-reviewer
- 2026-11-02T22:15:32Z orchestrator: From T-182 r3: every guided page load logs a 404 on /api/cases (README walk, demo mode). Fix before close: no failed request on first paint.
- 2026-11-02T22:25:17Z orchestrator: review paralegal-reviewer (claude-opus-5-5): changes — reviews/T-181-paralegal.md; round 1; findings:
    - [major] Disputed-item screen doesn't say what is disputed, and its grey box says the borrowed sentence is 'not in any line' when the line uses it — fix: Relabel the grey box 'In this record but not in the highlighted words'. On a disputed or edited item, mark (underline) the words in the line that are not in the highlighted quote, using a deterministic word diff, with a caption such as 'Thes
    - [major] Bates helper numbers one page per record in record order, and the screen never says so — fix: On the panel, state the rule and preview it before Save, for example: 'Each record gets one number, in order: record 1 = RIVERA0001 ... record 9 = RIVERA0009. Use this only if each record is one Bates page in this order; otherwise leave it blank and fill the cites in Word.' Better still, acc
    - [minor] Step 2 tells me no ledger amount will be in billed charges; Step 3 then lets me count three of them — fix: In the guided UI, replace the reason's last clause with 'Its amounts are decided in step 3, Check the bills.' Fix 'a highlighted words'.
    - [minor] Pressing A on a refused line moves focus to 'No, leave it out', so the next Space or Enter leaves the line out — fix: When Yes is refused and there is no checkbox, keep focus where it was (or on the refusal message) and say 'Yes is not available for this line: <reason>'. Don't move focus onto a decision button.
    - [minor] lib11 screens say the answers were 'not written by an AI model' while each card says 'AI draft' — fix: Build the title-row note from the case (models.generator_prepared / item.prepared), not from health. In the legend, say a second check read each line 'unless the line says it was not double-checked'.
    - [minor] Undated ledger lines are listed under a 'Date' column with the statement date — fix: For a counted line with no date of service, show 'no date of service (statement June 15, 2026)' in the Step 3 table, and use 'statement dated June 15, 2026' in the letter line.
    - [minor] Step 3 dispute line doesn't say what the second check disagreed about — fix: Name the direction from the judge verdict. For example: 'A second AI check thought this may not be a separate charge.' or '... thought this may be a charge, not a total.'
    - [minor] On the conflict warning, the record-7 sentence that makes the conflict is below the fold of the record pane — fix: For multi-record warnings, show only each record's highlighted sentence (with 'show whole record'), or scroll the pane so every highlight is in view.
    - [minor] Public demo says it can read 'our test cases' but offers none — fix: In public mode, drop 'and our test cases' (or expose the library read-only if Chris wants it in the demo).
- 2026-11-02T22:25:29Z orchestrator: Round 2 (frontend): paralegal majors (disputed-line grey box mislabels the outside-quote sentence as 'not in any line'; Bates fill-in must say it is one number per record) + the /api/cases 404 on every page load (T-182 r3) + paralegal minors where cheap. UX designer findings will be appended to this round when they land.
- 2026-11-02T22:25:29Z orchestrator: assigned: frontend
- 2026-11-02T22:25:37Z frontend: claimed
- 2026-11-02T22:30:00Z orchestrator: review ux-designer-reviewer (claude-opus-5-5): changes — reviews/T-181-ux-designer.md
- 2026-11-02T22:43:16Z frontend: r2 in progress: all fixes coded + tests/e2e/guided/test_round2.py (22 tests); verifying from a git archive of a temp-index tree. 404 root cause: public mode answers 404 on GET /api/cases (Home) and /api/library (/new) by design and health had no mode field; T-197 adds health.local_mode, frontend (G.healthNow) skips both probes when false.
- 2026-11-02T22:51:23Z frontend: AC 1 checked: r2 commit 9ab8cae from git archive of the commit tree, E2E_REQUIRE_DB=1: tests/e2e/guided + test_no_console_errors + test_demo_provenance 134 passed (incl. test_round2.py, public-server first-paint test now a hard assertion after T-197)
- 2026-11-02T22:51:23Z frontend: moved in_progress -> in_review
- 2026-11-02T22:51:29Z orchestrator: review dispatched: ux-designer-reviewer, paralegal-reviewer

## Handoff
R2 9ab8cae. What changed: (1) grey box now 'outside the highlighted words' and disputed/edited lines underline the words not in the quote (code diff); (2) Bates panel states one number per record, shows a live preview (record 1..N) and what it does to the letter; (3) no first-paint 404: Home and /new read health.local_mode (T-197) and skip /api/cases and /api/library in public mode, e2e starts a real public server; (4) UX majors: Step 3 done lists are cards on phones (no sideways scroll), disputed line and tick box on screen together at 390, refused edit names the dropped words with correct grammar, step toggle closes on a second tap; plus paralegal minors (amount dispute direction, ledger statement date, ledger reason points to step 3, refused-Yes focus stays off No, provenance follows the case, multi-record highlight window, stale 409 says what it is now, no E hint on Step 3, 404 page primary) and classic tooltip per D-065 (exemption removed). How verified: git archive of commit tree, E2E_REQUIRE_DB=1, guided + no_console_errors + demo_provenance 134 passed. Left: letter line for undated ledger counts still says the statement date without the word 'statement' (backend text; Step 3 table fixed); minors not done: locked steps all say 'After step 1', Step 4/new paste box vs sticky bar, 'Was:' line, case copy link, D-065 wording 'quote' (needs Chris). Surprised: on a phone the record shrinks to ~3 lines when a tick box is present (test_step3 floor lowered 200 to 80).
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:43.359Z

**tool call — Bash**
````
{
 "command": "sed -n '1,84p' personas/paralegal.md | diff - <(echo) >/dev/null; sed -n '60,84p' personas/paralegal.md; echo ----; cat reviews/T-181-paralegal.md | head -80; ls artifacts/review-evidence/T-181-paralegal/",
 "description": "Read persona tail and round-1 review"
}
````

### User / tool · 2026-11-02T22:51:43.463Z

**tool result**
````
5. Check the charges table and the total; try to find where the $185 went.
6. Review the whole case keyboard-first: accept most, edit one summary (record 3), dismiss one flag. Time the full review.
7. Export; paste into a plain-text file under `artifacts/review-evidence/`; confirm the dismissed item is absent and my edit is present.
8. Refresh mid-review once and confirm my decisions persist (or note that they don't).
9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).

## 8. Calibration
Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
- **blocker — PT total invented.** Evidence: charges table row "Capital PT — $2,220 (12 × $185)". Fix: list "$185 per visit — rate, visit count not stated; needs review"; total stays $8,390. Test: eval asserts no PT total and total = 8390.
- **major — Export has no citations.** Evidence: export line "Patient treated at Capital PT for neck pain." Fix: `January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]`. Test: E2E asserts every letter line contains a date of service, the provider as written, a verbatim quote, and the citation placeholder.
- **minor — No remaining count.** Evidence: review screen of 9 entries + 8 flags has no counter. Fix: sticky "11 of 17 reviewed".

## 9. Sources
- https://www.evenuplaw.com/guides/how-to-prepare-medical-chronology — EvenUp (vendor): chronology columns are source page, DOS, provider/facility, encounter, complaint, diagnoses, treatment, referrals; ends with a review checklist.
- https://www.evenuplaw.com/guides/what-is-a-medical-chronology/ — EvenUp: paralegal drafts, attorney reviews; demand medical facts must match the chronology; a bill without a matching note is a gap to flag.
- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor, 2026): common errors are entry-timestamp vs visit dates, copy-forward duplication, missing page/Bates cites, unflagged conflicting onset histories.
- https://davislaw.betterteam.com/personal-injury-litigation-paralegal-3 — Davis Law Firm (San Antonio) posting: PI paralegals summarize records, bills, and wage loss and build demand packages; Filevine preferred.
- https://www.builtinaustin.com/job/litigation-paralegal/11851661 — Brown Sims (Houston) posting: medical and billing chronologies are a core paralegal duty on the defense side too.
- https://nala.org/events/2025-11-24/?ical=1 — NALA CLE (Nov 2025): PI discovery guide for paralegals; organizing records for attorney and expert use.
- https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ — RMD Law (PI firm, 2026): no carrier publishes a gap threshold; delay-to-first-care, mid-treatment gaps, and early stopping are distinct.
- https://www.blackchapman.com/?p=396 — Black Chapman (PI firm) on Colossus: documented diagnoses per body part and objective findings drive valuation.
- Assumptions: Texas setting and Filevine are from the postings; the `[Ex. __ / Bates __]` placeholder (D-002) is used because Appendix A records have no Bates numbers. Vendor and plaintiff-firm sources are advocacy, not neutral.

## 10. Limits
Do not opine on legal strategy (whether to disclose a gap in the demand — litigation-lead), clinical interpretation beyond reading the words (legal-nurse), code quality, or security. Do not judge visual design except where it slows verification.
----
# T-181 guided 4-step UI (D-068): paralegal review (Maria Delgado, senior PI paralegal)

**Verdict: changes** (0 blockers, 2 majors, 7 minors, 2 nits). Scope: `git archive 26287b9` run in demo mode (fixture backend, curated set, no live calls).
- Public demo copy: port 7931, listener PID 49893.
- Library run: the same archive with `ZLAYT_MODE=local`, port 7932, PID 57169. The library is local-only by design (api.py:282).
- Both servers were stopped afterwards (`lsof` returned nothing, `curl` returned 000).

I took the sample case from **Your cases** to a downloaded letter using only what the screen said. Then I opened lib11 (priors and ledger) and did Step 2 and Step 3. The guided suite run from the archive: `100 passed in 148.47s`.

**Timing for the sample case:**
- Wall clock was about 5 min 10 s, from "Open the sample case" (16:10:21) to the downloaded letter (about 16:15:30). That includes reading all 23 items against the raw records.
- Drafting took about 1.5 s.
- The decision pass was 34 key actions and 5 clicks: Continue on Your cases ×3 (I resumed between script runs), one deliberate Undo, and Go to step 4. Before that came Open the sample case and Draft the timeline. The scripted keys took 17.5 s.
- At a human reading pace I'd expect about 8 to 10 minutes for this case.

**What I would tell my attorney:**
- I would use this letter. Every Appendix A truth is right:
  - 9 lines, with EMS and ER both on 01-09.
  - The 73-day gap is flagged and the 28-day interval is not.
  - The 01-09 / 01-19 conflict is flagged with both quotes, and the tool does not pick one.
  - 12 planned PT visits vs. discharge after two missed appointments.
  - Both prior-condition mentions.
  - $6,240 + $2,150 = **$8,390.00**.
  - $185 is never counted ("Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger." appears in the notes only).
  - Lost work appears under DAMAGES MENTIONS, not as a charge.
- My edit to record 3 reached the letter. The original wording is kept under EDITED ITEMS. My dismissed flag appears only under FLAGS DISMISSED. Decisions survived a reload. With undecided items, Copy and Download stay disabled until "Copy it anyway" is ticked.

**What I would fix before the gate (majors):**
1. **The disputed-item screen doesn't show what is disputed, and the grey box contradicts the line.** On lib11 e1, e2 and e4, the line uses a sentence from outside the highlighted quote. The grey box lists that same sentence under "Also in this record, not in any line:".
2. **The Bates helper assumes one page per record without saying so.** It numbers one Bates page per record in record order, but the screen never says that. The letter then carries specific page cites that nothing in the records supports.

**Grades asked for:**
- verify_quickly **4**: every item puts the full record, the highlighted verbatim quote and the line side by side, and the check is explained in one sentence.
- Keyboard **4**: A, D and E plus Space and Tab handle everything. The arrows move between items. Reload keeps working. No key moves between steps.
- Charges **4**: counting matches D-059 to D-062 and D-064, and lib11 comes to $6,000 with each ledger line cited. Undated ledger lines carry the statement date in a "Date" column.
- Compare confirm **3**: the box is deliberate and never pre-ticked, but it doesn't say which words are in dispute.
- Letter **4**: I'd paste it, but I'd leave the Bates helper empty.
- Where you are **5**: the step bar, "Item N of M · X answered · Y to go", the done screens and "Finished. Your letter is ready." on home were right every time.

```json
{"card": "T-181", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 26287b9 (guided UI: f3d42a2, 848bbad, 3944cc2, 26287b9) extracted to the session scratchpad. Public demo mode (LLM_BACKEND=fixture FIXTURE_SET=curated, ZLAYT_MODE unset) at http://127.0.0.1:7931 (listener PID 49893). Library run: the same archive with ZLAYT_MODE=local at http://127.0.0.1:7932 (PID 57169), because /api/library is local-only (app/backend/api.py:282). Both were stopped with kill; lsof found no listener and curl returned 000 on both ports. Sample case: evals/golden/sample.txt via 'Open the sample case'. Library: case_lib11_priors_and_ledger via Start a new case > Choose a test case. Viewport 1440x900.",
 "exercised": [
  "Read personas/paralegal.md, the T-181 card notes, D-059 to D-068 in memory/ORCHESTRATOR_DECISIONS.md, and docs/GUIDED_UI_SPEC.md sections 3 to 7 and 9",
  "Guided e2e suite from the archive: E2E_REQUIRE_DB=1 pytest tests/e2e/guided -q gave '100 passed in 148.47s'",
  "Sample case, Playwright with a persistent profile. Steps:",
  "  Opened the empty Your cases page and clicked Open the sample case: Step 1 showed 'We found 9 records'",
  "  Clicked Draft the timeline (about 1.5 s), saw 'All set', then went to Step 2",
  "  Paged through all 19 Step 2 items with ArrowRight without deciding, and compared each date, provider, line and highlighted quote with sample.txt (s05_catalogue.out)",
  "  Timed keyboard pass: A on most items; E on record 3, retyped the line, Tab to Save my wording; the compare box showed; A moved focus to the checkbox, Space ticked it, A accepted",
  "  Reloaded the page mid-review: position and decisions were kept",
  "  E on the gap flag: typed a note, saved it with Tab and Enter (the flag was accepted with the note)",
  "  D on the accident-date-source flag; A on the new-onset flag, clicked Undo, then A again; reached the Step 2 done screen",
  "  Step 3: catalogued the 4 amounts, then A on each; the total chip showed $6,240.00 then $8,390.00; done screen",
  "  Step 4: read the letter and the notes; Download letter and Download notes; Copy letter (clipboard text equals the download); clean-text check (check_letter.py)",
  "  Filled Exhibit 3 / Bates prefix RIVERA / First number 1, saved, and reloaded",
  "  Home shows 'Finished. Your letter is ready.' with an 'Open letter' button",
  "Second sample case: decided 2 items, jumped to Step 4. Copy and Download were disabled until 'Copy it anyway, without 21 items'; the preview held only the 2 accepted lines",
  "Public demo Start a new case: only the sample tile is offered; GET /api/library returned 404",
  "lib11 on port 7932: picked the test case, Read the records, Draft (1.5 s)",
  "lib11 Step 2: worked all 21 items. Compare confirm on the disputed lines e1, e2 and e4. The ledger line e9 was refused (CHARGE_TEXT_IN_ENTRY)",
  "lib11 Step 3: all 8 amounts. Counted ED $3,260; counted ledger lines $250, $180 and $2,310 with the 'separate charge' and compare boxes; listed the total, payment, adjustment and balance; done screen showed $6,000.00",
  "API reads (api_e1.py, curl): item e1/e2/e4/e9 why, reasons and ladder.judge; the lib11 export letter_text"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "keyboard_speed": 4, "charges_trust": 4, "compare_confirm_clarity": 3, "letter_usable": 4, "where_am_i": 5},
 "findings": [
  {"severity": "major", "title": "Disputed-item screen doesn't say what is disputed, and its grey box says the borrowed sentence is 'not in any line' when the line uses it",
   "evidence": "artifacts/review-evidence/T-181-paralegal/28-lib-s2-00-e1.png: the line reads 'Annual visit; history per patient of car accidents in 2019 and 2022...', the highlighted quote starts at 'History per patient', and the grey box reads 'Also in this record, not in any line: “Annual visit.”'. The same pattern is in 28-lib-s2-05-e2.png ('...after passenger vehicle was struck from behind' vs 'not in any line: “Passenger vehicle struck from behind.”') and 28-lib-s2-08-e4.png ('Law firm letter of protection to Fennimoor Spine Clinic...' vs 'not in any line: “Letter of protection to Fennimoor Spine Clinic.”'). The dispute box only says 'A second AI check found this only partly supported by the highlighted words.' The API has no more detail: why 'A second AI check found the summary only partly supported by the quoted text.', ladder.judge reason_code 'OTHER_UNSUPPORTED', and code_checks.summary_tokens_not_in_excerpt [] (api_e1.out). The label comes from app/frontend/guided/step2.js:66.",
   "why_it_matters": "D-066 asks me to compare deliberately, and this is the screen where I do it. The screen has the exact words the line borrowed from outside the quote, but it tells me they are in no line, which contradicts the line beside it. If I tick 'I read this line...' on trust, the letter carries 'Annual visit' and 'after ... struck from behind' with a Source quote that does not contain them. The adjuster can quote that back at us.",
   "fix": "Relabel the grey box 'In this record but not in the highlighted words'. On a disputed or edited item, mark (underline) the words in the line that are not in the highlighted quote, using a deterministic word diff, with a caption such as 'These words are not in the highlighted quote'. Keep the checkbox as it is.",
   "acceptance_test": "Guided e2e on lib11 e1: the grey box heading does not contain 'not in any line', and the line card marks 'Annual visit' as outside the quote. Same check on e2 for 'struck from behind'."},
  {"severity": "major", "title": "Bates helper numbers one page per record in record order, and the screen never says so",
   "evidence": "Step 4 panel text: 'Exhibit and page numbers (optional) / Fill these in to replace “[Ex. __ / Bates __]” in every source line.' (app/frontend/guided/step4.js:148). With Exhibit 3, prefix RIVERA and first number 1, letter-with-bates.txt reads line 5 'Source [Ex. 3 / Bates RIVERA0001]' (record 1), line 33 '[Ex. 3 / Bates RIVERA0008]' (MRI, record 8) and line 42 '[Ex. 3 / Bates RIVERA0002]' (the ER charge). The rule is memory/contracts/api.md:115 'NNNN = first number + record number - 1'. The backend has worked this way since T-058 (dbb2c66). T-181 puts it on the new Step 4 screen without the rule. Screenshot 22-step4-bates-filled.png.",
   "why_it_matters": "Real records run many pages each, so record 8 is almost never page 8. The letter would then send the adjuster specific Bates cites that nothing in the records supports, and these are exactly the cites they check first. The screen reads as if the tool knows the pages. The default with the panel blank is safe.",
   "fix": "On the panel, state the rule and preview it before Save, for example: 'Each record gets one number, in order: record 1 = RIVERA0001 ... record 9 = RIVERA0009. Use this only if each record is one Bates page in this order; otherwise leave it blank and fill the cites in Word.' Better still, accept a starting Bates number per record.",
   "acceptance_test": "Guided e2e test_step4: the cfg panel text names the one-number-per-record rule. After the prefix and first number are typed, a preview shows record 1 and the last record's cite before Save."},
  {"severity": "minor", "title": "Step 2 tells me no ledger amount will be in billed charges; Step 3 then lets me count three of them",
   "evidence": "lib11 e9 card (28-lib-s2-19-e9.png, s13.out): '...Its amounts were read but not totaled (the notes for the attorney say why), so none of them is in Billed charges; dismiss this line unless it states treatment.' It also says 'pick a highlighted words without the amount'. Step 3 for the same ledger (s14.out) offers 'You can still count it if you checked the ledger yourself'. After counting, Step 3 done reads 'Billed charges accepted from these records: $6,000.00' with $250, $180 and $2,310 counted.",
   "why_it_matters": "On the charges question the two steps contradict each other. A paralegal who believes Step 2 would leave real ledger charges out of the specials.",
01-home-empty.png
02-step1-after-open.png
03-home-one-case.png
04-step1-drafting.png
05-after-draft.png
06-step2-first-item.png
07-cat-00-e1.png
07-cat-01-f_accident_date_after_treatment_1_2_7.png
07-cat-02-e2.png
07-cat-03-e3.png
07-cat-04-f_r3_1.png
07-cat-05-e4.png
07-cat-06-f_cx1.png
07-cat-07-e5.png
07-cat-08-e6.png
07-cat-09-f_gap_r6_r7.png
07-cat-10-f_r6_1.png
07-cat-11-e7.png
07-cat-12-f_r7_1.png
07-cat-13-f_r7_2.png
07-cat-14-e8.png
07-cat-15-f_r8_1.png
07-cat-16-f_r8_2.png
07-cat-17-e9.png
07-cat-18-f_r9_1.png
08-step2-fix-wording.png
09-step2-after-edit-compare.png
10-step2-compare-ticked.png
11-step2-after-reload.png
12-step2-gap-note.png
13-step2-after-gap-note.png
14-home-mid-review.png
15-step2-after-dismiss.png
16-step2-done.png
17-bills-00-a1.png
17-bills-01-a4.png
17-bills-02-a2.png
17-bills-03-a3.png
18-bills-after-first-charge.png
19-step3-done.png
20-step4-letter.png
20b-step4-letter-full.png
21-home-finished.png
22-step4-bates-filled.png
23-new-case.png
24-lib-new-case.png
25-lib-choose.png
26-lib-records.png
27-lib-after-draft.png
28-lib-s2-00-e1.png
28-lib-s2-05-e2.png
28-lib-s2-08-e4.png
28-lib-s2-19-e9.png
29-lib-s2-00-e1-ticked.png
29-lib-s2-05-e2-ticked.png
29-lib-s2-08-e4-ticked.png
29-lib-s2-19-e9-ticked.png
30-lib-step2-done.png
31-lib-s3-00-a1.png
31-lib-s3-01-a2.png
31-lib-s3-02-a3.png
31-lib-s3-03-a4.png
31-lib-s3-04-a5.png
31-lib-s3-05-a6.png
31-lib-s3-06-a7.png
31-lib-s3-07-a8.png
32-lib-step3-done.png
33-step4-pending.png
api_e1.out
api_e1.py
check_letter.out
check_letter.py
draft-T-181-paralegal.md
h.py
letter-clipboard.txt
letter-download.txt
letter-with-bates.txt
notes-download.txt
profile
run.log
s01_home.py
s02_open_sample.py
s03_draft.py
s04_step2_first.py
s05_catalogue.out
s05_catalogue.py
s06.out
s06_counts.json
s06_step2_pass.py
s07.out
s07_counts.json
s07_step2_finish.py
s08.out
s08_step3_catalogue.py
s09.out
s09_counts.json
s09_step3_pass_and_letter.py
s10.out
s10_export.py
s11.out
s11_new_case.py
s12.out
s12_lib_open.py
s13.out
s13_lib_step2.py
s14.out
s14_lib_step3.py
s15.out
s15_pending_letter.py
timing.json
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:45.547Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-181-paralegal/h.py; head -30 artifacts/review-evidence/T-181-paralegal/run.log; ls artifacts/review-evidence/ | grep -i serve | head",
 "description": "Read helper and run log from round 1"
}
````

### User / tool · 2026-11-02T22:51:45.652Z

**tool result**
````
"""T-181 paralegal review helper: persistent Chromium profile on the archive app (26287b9, demo mode, port 7931).

Usage: .venv/bin/python -I artifacts/review-evidence/T-181-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7931")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PROFILE = os.path.join(OUT, "profile")
LOG = os.path.join(OUT, "run.log")


def main(script):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900})
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        pg.on("response", lambda r: errors.append(f"http {r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
        logf = open(LOG, "a")

        def log(*a):
            s = " ".join(str(x) for x in a)
            print(s)
            logf.write(s + "\n")
            logf.flush()

        def shot(name, full=False):
            path = os.path.join(OUT, name + ".png")
            pg.screenshot(path=path, full_page=full)
            log("[shot]", path)

        def dump(label=""):
            pg.wait_for_timeout(250)
            t = pg.evaluate("() => document.body.innerText")
            log(f"===== {label} url={pg.url}")
            log(t)
            log("=====")
            return t

        g = {"pg": pg, "shot": shot, "dump": dump, "log": log, "BASE": BASE, "OUT": OUT, "time": time, "ctx": ctx}
        log(f"### run {os.path.basename(script)} at {time.strftime('%H:%M:%S')}")
        try:
            exec(compile(open(script).read(), script, "exec"), g)
        finally:
            if errors:
                log("ERRORS:\n  " + "\n  ".join(errors))
            ctx.close()
            logf.close()


if __name__ == "__main__":
    main(sys.argv[1])
### run s01_home.py at 16:10:02
===== home first visit url=http://127.0.0.1:7931/
Skip to the main content
Synthetic data only — never paste real records
TT
Treatment Timeline
Demo: sample answers prepared by our team
Dark mode
Your cases

Each case goes through 4 steps. Pick up where you left off.

These are the cases started in this browser. Keep the case link to open it elsewhere.

+
You don't have any cases yet.

A case is one client's medical records. We'll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter.

+ Start a new case
Open the sample case

Demo: sample answers prepared by our team. Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal/01-home-empty.png
buttons: ['Skip to the main content', 'TT\nTreatment Timeline', 'Dark mode', '+ Start a new case', 'Open the sample case']
### run s01_home.py at 16:10:06
===== home first visit url=http://127.0.0.1:7931/
Skip to the main content
Synthetic data only — never paste real records
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:48.261Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py; grep -n -i \"demo\\|ZLAYT_MODE\\|PORT\" docs/RUNBOOK.md | head -20",
 "description": "Read serve script and runbook mode notes"
}
````

### User / tool · 2026-11-02T22:51:48.364Z

**tool result**
````
"""Start the app from a git-archive copy (commit e293daa) for the paralegal pass-4 / T-114 r3 review.

Usage (env vars set by the caller: LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=7897 HOST=127.0.0.1):
    .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py <archive_root>
Runs under -I (isolated), so the archive root is put first on sys.path explicitly.
"""
import os
import runpy
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
runpy.run_module("app.main", run_name="__main__")
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
12:We restored those and gave the board and app their own ports so nothing of yours was clobbered.
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:53.944Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && cd /Users/arsis/zlayt-pm-project && git archive 9ab8cae | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab",
 "description": "Extract archive of 9ab8cae to scratchpad"
}
````

### User / tool · 2026-11-02T22:51:55.116Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:51:59.485Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && grep -rn \"environ.get\\|getenv\" app/config.py app/main.py 2>/dev/null | head -20; lsof -iTCP:7941 -sTCP:LISTEN -nP; lsof -iTCP:7942 -sTCP:LISTEN -nP; echo free",
 "description": "Check env vars and port availability"
}
````

### User / tool · 2026-11-02T22:51:59.779Z

**tool result**
````
app/config.py:19:    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
app/config.py:22:    if os.environ.get("ENABLE_LIVE") == "1" and not live:
app/config.py:24:    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
app/config.py:26:    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/config.py:31:        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
app/config.py:32:        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
app/config.py:33:        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
app/config.py:35:        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
app/config.py:44:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/main.py:25:    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
app/main.py:32:        if os.environ.get("ZLAYT_DEBUG") == "1":
free
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:02.645Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && grep -rn \"ZLAYT_DB\\|DB_PATH\" app/db/*.py app/backend/*.py | head -5",
 "description": "Find DB path env var"
}
````

### User / tool · 2026-11-02T22:52:02.739Z

**tool result**
````
app/backend/api.py:98:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:09.942Z

**tool call — Bash**
````
{
 "command": "env LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7941 HOST=127.0.0.1 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/demo.sqlite .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/demo.log 2>&1",
 "description": "Start demo-mode server on port 7941",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T22:52:10.018Z

**tool result**
````
Command running in background with ID: bg4zpdl47. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bg4zpdl47.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:15.975Z

**tool call — Bash**
````
{
 "command": "env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local PORT=7942 HOST=127.0.0.1 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/local.sqlite .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/local.log 2>&1",
 "description": "Start local-mode server on port 7942",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T22:52:16.066Z

**tool result**
````
Command running in background with ID: bc0633pok. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bc0633pok.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:17.632Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7941/api/health; echo; curl -s http://127.0.0.1:7942/api/health; echo; lsof -iTCP:7941 -sTCP:LISTEN -nP; lsof -iTCP:7942 -sTCP:LISTEN -nP",
 "description": "Check both servers healthy and get PIDs"
}
````

### User / tool · 2026-11-02T22:52:17.916Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":false,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND   PID  USER   FD   TYPE            DEVICE SIZE/OFF NODE NAME
Python  14948 arsis    9u  IPv4 0xf563babbd4d1f02      0t0  TCP 127.0.0.1:7941 (LISTEN)
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  15071 arsis    9u  IPv4 0xc872ad9ef808077a      0t0  TCP 127.0.0.1:7942 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:20.488Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal && for f in s02_open_sample.py s03_draft.py s06_step2_pass.py s07_step2_finish.py; do echo \"##### $f\"; cat $f; done",
 "description": "Read round-1 step scripts"
}
````

### User / tool · 2026-11-02T22:52:20.579Z

**tool result**
````
##### s02_open_sample.py
T0 = time.time()
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.get_by_role("button", name="Open the sample case").click()
pg.wait_for_timeout(1500)
log("t after open click", round(time.time() - T0, 2))
dump("after Open the sample case")
shot("02-step1-after-open")
log("buttons:", [b.inner_text() for b in pg.query_selector_all("button, a") if b.is_visible()])
##### s03_draft.py
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
dump("home with one case")
shot("03-home-one-case")
pg.click("[data-testid=btn-continue]")
pg.wait_for_selector("[data-testid=view][data-ready]")
T0 = time.time()
pg.get_by_role("button", name="Draft the timeline").click()
seen = set()
for i in range(120):
    pg.wait_for_timeout(500)
    t = pg.evaluate("() => document.querySelector('main') ? document.querySelector('main').innerText : document.body.innerText")
    key = t[:300]
    if key not in seen:
        seen.add(key)
        log(f"--- t={round(time.time()-T0,1)}s url={pg.url}")
        log(t[:900])
        if len(seen) == 2:
            shot("04-step1-drafting")
    if "/timeline" in pg.url or "timeline is ready" in t.lower() or "Check the timeline" in [b.inner_text() for b in pg.query_selector_all("main button")]:
        break
log("draft finished at", round(time.time() - T0, 1), "s; url", pg.url)
pg.wait_for_timeout(800)
dump("after draft")
shot("05-after-draft")
log("buttons:", [b.inner_text() for b in pg.query_selector_all("button, a") if b.is_visible()])
##### s06_step2_pass.py
import re, json
T0 = time.time()
MOUSE = 0
KEYS = 0
open(OUT + "/timing.json", "w").write(json.dumps({"start": T0}))

def st(label=""):
    pg.wait_for_timeout(350)
    m = re.search(r"item=([^&]+)", pg.url)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    acts = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")
    ae = pg.evaluate("() => { const a = document.activeElement; return a ? a.tagName + '[' + (a.getAttribute('data-testid')||'') + '] ' + (a.innerText||a.value||'').slice(0,30) : null }")
    log(f"[{round(time.time()-T0,1)}s] {label} item={m.group(1) if m else '-'} | {title[-40:]} | ACT: {acts[:260]} | focus: {ae}")

def key(k, label=None):
    global KEYS
    KEYS += 1
    pg.keyboard.press(k)
    st(label or k)

pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=btn-continue]"); MOUSE += 1
pg.wait_for_selector("[data-testid=view][data-ready]")
st("opened step 2")
key("a", "a e1")
key("a", "a conflict flag")
key("a", "a e2")
# item 4 = e3: fix the wording
key("e", "e on e3")
shot("08-step2-fix-wording")
dump("fix wording screen")
ta = pg.locator("textarea").first
log("textarea value:", ta.input_value())
pg.keyboard.press("Meta+A"); KEYS += 1
pg.keyboard.type("Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks."); KEYS += 1
for i in range(6):
    pg.keyboard.press("Tab"); KEYS += 1
    ae = pg.evaluate("() => (document.activeElement.innerText||'').trim()")
    log("tab ->", ae)
    if ae.startswith("Save"):
        break
pg.keyboard.press("Enter"); KEYS += 1
st("after save wording")
shot("09-step2-after-edit-compare")
dump("after edit save")
# compare confirm: try 'a' (should focus the checkbox), space ticks, 'a' accepts
key("a", "a on edited (expect focus checkbox)")
key("Space", "space tick")
shot("10-step2-compare-ticked")
key("a", "a accept edited")
key("a", "a prior-condition flag")
key("a", "a e4")
key("a", "a plan-vs-actual flag")
key("a", "a e5")
# refresh mid-review
pg.reload()
pg.wait_for_selector("[data-testid=view][data-ready]")
st("after reload")
dump("after reload")
shot("11-step2-after-reload")
key("a", "a e6")
# gap: add a note
key("e", "e on gap (add a note)")
shot("12-step2-gap-note")
pg.keyboard.type("Ask client about March-May 2026: any care elsewhere? Records request if so."); KEYS += 1
for i in range(6):
    pg.keyboard.press("Tab"); KEYS += 1
    ae = pg.evaluate("() => (document.activeElement.innerText||'').trim()")
    log("tab ->", ae)
    if ae.startswith("Save"):
        break
pg.keyboard.press("Enter"); KEYS += 1
st("after save note")
dump("after gap note save")
shot("13-step2-after-gap-note")
open(OUT + "/s06_counts.json", "w").write(json.dumps({"mouse": MOUSE, "keys": KEYS, "elapsed": time.time() - T0}))
##### s07_step2_finish.py
import re, json
T0 = time.time()
KEYS = 0
MOUSE = 0
def st(label=""):
    pg.wait_for_timeout(350)
    m = re.search(r"item=([^&]+)", pg.url)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    acts = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")
    log(f"[{round(time.time()-T0,1)}s] {label} item={m.group(1) if m else '-'} | {title[-40:]} | ACT: {acts[:200]}")
def key(k, label=None):
    global KEYS
    KEYS += 1
    pg.keyboard.press(k)
    st(label or k)

pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
dump("home mid-review")
shot("14-home-mid-review")
pg.click("[data-testid=btn-continue]"); MOUSE += 1
pg.wait_for_selector("[data-testid=view][data-ready]")
st("continue lands on")
key("a", "a missed-care flag")
key("a", "a e7")
key("d", "d accident-date-source flag (dismiss)")
shot("15-step2-after-dismiss")
key("a", "a new-onset flag")
# Undo test on the new-onset flag
pg.get_by_role("button", name="Undo").click(); MOUSE += 1
st("after Undo click")
key("a", "a new-onset flag again")
key("a", "a e8")
key("a", "a degenerative flag")
key("a", "a hedged flag")
key("a", "a e9")
key("a", "a patient-report flag")
pg.wait_for_timeout(500)
dump("step2 done screen")
shot("16-step2-done", full=True)
open(OUT + "/s07_counts.json", "w").write(json.dumps({"mouse": MOUSE, "keys": KEYS, "elapsed": time.time() - T0}))
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:23.757Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal && for f in s09_step3_pass_and_letter.py s10_export.py s12_lib_open.py s13_lib_step2.py; do echo \"##### $f\"; cat $f; done",
 "description": "Read round-1 step 3/4 and lib scripts"
}
````

### User / tool · 2026-11-02T22:52:23.854Z

**tool result**
````
##### s09_step3_pass_and_letter.py
import re, json
T0 = time.time()
KEYS = 0
MOUSE = 0
def st(label=""):
    pg.wait_for_timeout(350)
    m = re.search(r"item=([^&]+)", pg.url)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    acts = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")
    log(f"[{round(time.time()-T0,1)}s] {label} item={m.group(1) if m else '-'} | {title[-70:]} | ACT: {acts[:200]}")
def key(k, label=None):
    global KEYS
    KEYS += 1
    pg.keyboard.press(k)
    st(label or k)

pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=btn-continue]"); MOUSE += 1
pg.wait_for_selector("[data-testid=view][data-ready]")
st("bills opened")
key("a", "a ER charge")
shot("18-bills-after-first-charge")
key("a", "a MRI charge")
key("a", "a list rate")
key("a", "a list lost-work mention")
pg.wait_for_timeout(400)
dump("step3 done")
shot("19-step3-done", full=True)
log("buttons:", [b.inner_text() for b in pg.query_selector_all("main button, main a") if b.is_visible()])
# go to step 4 with the primary button (keyboard: is it focused?)
log("focus:", pg.evaluate("() => (document.activeElement.innerText||document.activeElement.tagName).slice(0,60)"))
pg.get_by_text("Go to step 4: Get your letter").first.click(); MOUSE += 1
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(800)
dump("step4 letter page")
shot("20-step4-letter")
shot("20b-step4-letter-full", full=True)
log("testids:", pg.evaluate("() => Array.from(document.querySelectorAll('[data-testid]')).map(e => e.getAttribute('data-testid')).filter(t => !t.startsWith('step-'))"))
open(OUT + "/s09_counts.json", "w").write(json.dumps({"mouse": MOUSE, "keys": KEYS, "elapsed": time.time() - T0}))
##### s10_export.py
import json
ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=BASE)
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
dump("home after finishing")
shot("21-home-finished")
log("continue button text:", pg.inner_text("[data-testid=btn-continue]"))
pg.click("[data-testid=btn-continue]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(600)
log("url:", pg.url)
with pg.expect_download() as d:
    pg.click("[data-testid=btn-download-letter]")
d.value.save_as(OUT + "/letter-download.txt")
log("letter download name:", d.value.suggested_filename)
with pg.expect_download() as d2:
    pg.click("[data-testid=btn-download-notes]")
d2.value.save_as(OUT + "/notes-download.txt")
log("notes download name:", d2.value.suggested_filename)
pg.click("[data-testid=btn-copy-letter]")
pg.wait_for_timeout(400)
clip = pg.evaluate("() => navigator.clipboard.readText()")
open(OUT + "/letter-clipboard.txt", "w").write(clip)
log("bar msg after copy:", pg.inner_text("[data-testid=bar-msg]"))
log("clipboard == download:", clip == open(OUT + "/letter-download.txt").read())
# exhibit / Bates fill-in
pg.fill("[data-testid=cfg-exhibit]", "3")
pg.fill("[data-testid=cfg-bates-prefix]", "RIVERA")
pg.fill("[data-testid=cfg-bates-start]", "1")
pg.click("[data-testid=btn-save-cfg]")
pg.wait_for_timeout(800)
log("cfg-error:", pg.inner_text("[data-testid=cfg-error]"))
txt = pg.inner_text("[data-testid=letter-text]")
open(OUT + "/letter-with-bates.txt", "w").write(txt)
log("letter with bates first 900:\n" + txt[:900])
shot("22-step4-bates-filled")
pg.reload()
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(600)
log("after reload letter has RIVERA:", "RIVERA" in pg.inner_text("[data-testid=letter-text]"))
##### s12_lib_open.py
import re
pg.goto(BASE + "/new")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
dump("new case page (local mode)")
shot("24-lib-new-case")
pg.click("[data-testid=tile-library]")
pg.wait_for_timeout(300)
shot("25-lib-choose")
log("library radios:", [r.get_attribute("data-testid") for r in pg.query_selector_all("[data-testid^=library-]")])
pg.check("[data-testid=library-case_lib11_priors_and_ledger]")
pg.click("[data-testid=btn-read]")
pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
pg.wait_for_timeout(400)
dump("lib11 records found")
shot("26-lib-records")
T0 = time.time()
pg.click("[data-testid=btn-draft]")
for i in range(60):
    pg.wait_for_timeout(500)
    if pg.query_selector("text=Go to step 2") or pg.query_selector("text=Stopped") or pg.query_selector("text=Drafting stopped"):
        break
log("draft took", round(time.time() - T0, 1), "s")
dump("lib11 after draft")
shot("27-lib-after-draft")
##### s13_lib_step2.py
import re
T0 = time.time()
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=btn-continue]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
n = 0
for step in range(40):
    m = re.search(r"item=([^&]+)", pg.url)
    if not m:
        break
    iid = m.group(1)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    srcHead = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[0].innerText.split('\\n').slice(0,2).join(' | ') : '' }")
    q = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").split("\n")[0]
    marks = pg.evaluate("() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)")
    yes = pg.query_selector("[data-testid=answer-yes]")
    yes_dis = yes.is_disabled() if yes else None
    cmp_box = pg.query_selector("[data-testid=check-compare]")
    log(f"######## {n} item={iid} | {title.split('|')[-2:]} | Q: {q} | yes_disabled={yes_dis} compare_box={bool(cmp_box)}")
    log("SRC:", srcHead)
    log("CARD:", right.replace("\n", " / "))
    log("MARKS:", marks)
    if cmp_box or yes_dis or "couldn't" in right.lower() or "could not" in right.lower():
        shot(f"28-lib-s2-{n:02d}-{iid}")
    n += 1
    if cmp_box or yes_dis:
        pg.keyboard.press("a")
        pg.wait_for_timeout(250)
        log("  after a on disabled: focus", pg.evaluate("() => document.activeElement.getAttribute('data-testid')"))
        pg.keyboard.press("Space")
        pg.wait_for_timeout(250)
        shot(f"29-lib-s2-{n-1:02d}-{iid}-ticked")
        pg.keyboard.press("a")
    elif "write this line yourself" in q.lower() or "can't go in the notes" in q.lower():
        pg.keyboard.press("d")
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
    log("  status:", pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").split("\n")[-2:])
log("step2 lib done in", round(time.time() - T0, 1), "s")
dump("lib step2 done")
shot("30-lib-step2-done", full=True)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:29.218Z

**tool call — Bash**
````
{
 "command": "git diff --stat 26287b9 9ab8cae -- app/ ; git diff 26287b9 9ab8cae -- app/frontend/guided/step2.js | head -150",
 "description": "Show r2 diff stat and step2 changes"
}
````

### User / tool · 2026-11-02T22:52:29.364Z

**tool result**
````
 app/backend/api.py             |   2 +-
 app/backend/export.py          |  15 ++--
 app/backend/export_routes.py   |   2 +-
 app/backend/flag_templates.py  |   9 ++
 app/backend/flags.py           |   2 +-
 app/backend/generator.py       |   2 +-
 app/backend/ingest.py          |  11 +--
 app/backend/language.py        |   6 +-
 app/backend/pipeline.py        |  17 ++--
 app/backend/present.py         | 118 ++++++++++++++++----------
 app/backend/reclassify.py      |   9 +-
 app/backend/review.py          |  18 ++--
 app/backend/spanish_text.py    |  11 ++-
 app/backend/store.py           |   6 +-
 app/backend/trace.py           | 185 ++++++++++++++++++++++++++---------------
 app/backend/why.py             |  87 +++++++++----------
 app/frontend/guided/app.js     |  17 ++--
 app/frontend/guided/core.js    |   9 +-
 app/frontend/guided/home.js    |   3 +-
 app/frontend/guided/review.css |  14 +++-
 app/frontend/guided/review.js  |  74 ++++++++++++++---
 app/frontend/guided/step1.js   |  13 +--
 app/frontend/guided/step2.js   |  55 ++++++++++--
 app/frontend/guided/step3.css  |  12 +++
 app/frontend/guided/step3.js   |  14 +++-
 app/frontend/guided/step4.css  |   3 +-
 app/frontend/guided/step4.js   |  18 +++-
 app/frontend/timeline.js       |   2 +-
 app/llm/audited.py             |  16 +++-
 29 files changed, 508 insertions(+), 242 deletions(-)
diff --git a/app/frontend/guided/step2.js b/app/frontend/guided/step2.js
index 101dbdd..7f53838 100644
--- a/app/frontend/guided/step2.js
+++ b/app/frontend/guided/step2.js
@@ -63,14 +63,32 @@
     const rows = [];
     recs.forEach((r) => (r.uncovered || []).forEach((u) => { if (!marks.some(([a, b]) => u.start >= a && u.end <= b)) rows.push(u.text); }));
     if (!rows.length) return [];
-    return [h("div", { class: "also", "data-testid": "uncovered" }, h("b", {}, "Also in this record, not in any line:"), ...rows.map((t) => h("div", {}, h("q", {}, t))))];
+    return [h("div", { class: "also", "data-testid": "uncovered" }, h("b", {}, "Also in this record, outside the highlighted words:"), ...rows.map((t) => h("div", {}, h("q", {}, t))))];
+  }
+  /* the part of a record to show when several records share the card: the highlighted words with about 80 characters of the record on each side, cut at a space or line end */
+  function windowOf(rec, marks) {
+    const t = rec.text || "", a = Math.min(...marks.map((m) => m[0])) - rec.char_start, b = Math.max(...marks.map((m) => m[1])) - rec.char_start;
+    let from = Math.max(t.lastIndexOf("\n", Math.max(0, a - 1)) + 1, a - 80), to = b + 80;
+    if (from > 0 && t[from - 1] !== "\n") { const sp = t.indexOf(" ", from); if (sp >= 0 && sp < a) from = sp + 1; }
+    const nl = t.indexOf("\n", b); if (nl >= 0 && nl < to) to = nl;
+    if (to < t.length && t[to] !== "\n") { const sp = t.lastIndexOf(" ", to); if (sp > b) to = sp; }
+    to = Math.min(t.length, to);
+    return from <= 0 && to >= t.length ? null : [Math.max(0, from), to];
   }
   function sourceFor(S, recs, marks, opt) {
     opt = opt || {};
+    S.whole = S.whole || new Set();
     return () => {
       const many = recs.length > 1, nodes = [];
       if (opt.hint) nodes.push(h("p", { class: "muted src-hint" }, opt.hint));
-      recs.forEach((r) => nodes.push(...R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r) : null, sentences: opt.sentencesOf === r.id ? r.sentences : null, picked: opt.picked, onPick: opt.onPick })));
+      recs.forEach((r) => {
+        const mine = marks.filter(([a]) => a >= r.char_start && a < r.char_end), win = many && mine.length && !opt.sentencesOf && !S.whole.has(r.id) ? windowOf(r, mine) : null;
+        nodes.push(...R.recBlock(r, { marks: mine, win, head: many ? recLabel(r) : null, sentences: opt.sentencesOf === r.id ? r.sentences : null, picked: opt.picked, onPick: opt.onPick }));
+        if (many && mine.length && !opt.sentencesOf && (win || S.whole.has(r.id))) {          // several records: each shows its highlighted sentence, so every highlight is on screen without scrolling
+          nodes.push(h("button", { type: "button", class: "btn quiet src-toggle", "data-testid": "btn-whole-record", "aria-expanded": win ? "false" : "true",
+            onclick: () => { win ? S.whole.add(r.id) : S.whole.delete(r.id); S.renderSource(); } }, win ? `Show the whole of record ${r.seq}` : `Show only the highlighted part of record ${r.seq}`));
+        }
+      });
       if (!opt.sentencesOf && opt.uncovered !== false) nodes.push(...uncoveredNote(recs, marks));
       return nodes;
     };
@@ -89,6 +107,23 @@
   function togglePick(S, sent) { const p = S.ui.picked || (S.ui.picked = new Set()); p.has(sent.start) ? p.delete(sent.start) : p.add(sent.start); S.renderSource(); }
   const warningsFoot = (S) => (S.ui.warnings || []).map((w) => h("p", { class: "foot-warn", "data-testid": "save-warning" }, R.plain(w.message || String(w))));
 
+  /* ---------- the words of a line that are not in the highlighted words (code, no AI): a deterministic word diff so she sees what to check (paralegal review T-181 major) ---------- */
+  const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
+  const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
+  const stem = (w) => w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, "");
+  function outsideParts(summary, quote) {
+    const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
+    let last = 0, any = false;
+    for (const m of String(summary || "").matchAll(WORD)) {
+      const w = m[0], out = !SKIP.has(w.toLowerCase()) && !inQuote.has(stem(w));
+      if (m.index > last) parts.push(summary.slice(last, m.index));
+      parts.push(out ? h("u", { class: "out", "data-testid": "outside-word" }, w) : w); if (out) any = true;
+      last = m.index + w.length;
+    }
+    if (last < summary.length) parts.push(summary.slice(last));
+    return any ? parts : null;
+  }
+
   /* ---------- presenting an item ---------- */
   function present(S, item, q) {
     const c = S.c, g = groupOf(c, item);
@@ -111,7 +146,7 @@
     if (refusal) { cls = "attn"; foot.push(h("strong", { "data-testid": "refusal" }, R.plain(item.why))); }
     else if (need) {
       cls = "attn";
-      foot.push(h("strong", { "data-testid": "compare-reason" }, edited ? "You changed the wording. Read it against the highlighted words once more." : R.disputeText(disp)));
+      foot.push(h("strong", { "data-testid": "compare-reason" }, edited ? "You changed the wording. Read it against the highlighted words once more." : R.disputeText(disp, item)));
       if (!edited) foot.push(" Read it against the highlighted words before you say yes.");
       foot.push(R.check(S, "compare", "I read this line against the highlighted words myself.", { focus: true }));
     } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "left out of the letter." : "kept in the letter.", " You can change it."); }
@@ -121,12 +156,13 @@
     foot.push(...warningsFoot(S));
     return {
       tag: R.tagFor(item), sub: lineHead(item, main),
-      body: [h("p", { class: "line-text", "data-testid": "line-text" }, item.summary || "")],
+      body: [h("p", { class: "line-text", "data-testid": "line-text" }, ...(((need && outsideParts(item.summary, item.excerpt)) || [item.summary || ""]))),
+        need && outsideParts(item.summary, item.excerpt) ? h("p", { class: "muted out-note", "data-testid": "outside-note" }, "Underlined words are not in the highlighted words.") : null],
       foot: { cls, nodes: foot },
       question: "Does this line say the same thing as the highlighted words?",
-      yes: { label: "Yes, this matches", disabled: () => refusal || (need && !R.ticked(S, "compare")), run: () => S.decide(item, "accept", need && R.ticked(S, "compare") ? { compared: true } : undefined) },
+      yes: { label: "Yes, this matches", why: refusal ? R.plain(item.why) : "", disabled: () => refusal || (need && !R.ticked(S, "compare")), run: () => S.decide(item, "accept", need && R.ticked(S, "compare") ? { compared: true } : undefined) },
       no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") },
-      third: { label: quoteFail(item) ? "Change the words" : "Fix the wording", hint: refusal, run: () => { ui.mode = "fix"; ui.draft = null; ui.picked = null; S.err = null; S.render(); } },
+      third: { label: quoteFail(item) ? "Change the words" : "Fix the wording", hint: refusal, run: () => { ui.mode = "fix"; ui.draft = null; ui.picked = null; S.err = null; S.say(null, null); S.render(); } },
       src: { head: headFor(srcRecs), nodes: sourceFor(S, srcRecs, marks) },
     };
   }
@@ -145,6 +181,7 @@
       const qChanged = r.excerpt !== item.excerpt, sChanged = summary !== (item.summary || "").trim();
       if (!qChanged && !sChanged) { S.err = { text: "Nothing has changed yet." }; S.render(true); return; }
       return S.act(async () => {
+        S.lastEdit = { excerpt: r.excerpt, summary, before: item.summary };       // a refusal that names dropped words reads these (review.js droppedText)
         const edits = {};                                   // one call: the server checks the new wording against the new quote together (two calls would test the old wording against the new quote)
         if (qChanged) edits.excerpt = r.excerpt;
         if (sChanged) edits.summary = summary;
@@ -230,14 +267,14 @@
     const foot = [];
     let cls = "plain";
     if (disp) {
-      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
+      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
     } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not needed. It is listed as ruled out in the notes." : "the attorney will be told.", " You can change it."); }
     else foot.push("Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.");
     return { ...tags, sub: "", body, foot: { cls, nodes: foot },
       question: "Should the attorney be told about this?",
       yes: { label: "Yes, tell the attorney", disabled: () => !!disp && !R.ticked(S, "compare"), run: () => S.decide(item, "accept", disp && R.ticked(S, "compare") ? { compared: true } : undefined) },
       no: { label: "No, not needed", run: () => S.decide(item, "dismiss") },
-      third: { label: "Add a note", run: () => { ui.mode = "note"; ui.draft = null; S.err = null; S.render(); } } };
+      third: { label: "Add a note", run: () => { ui.mode = "note"; ui.draft = null; S.err = null; S.say(null, null); S.render(); } } };
   }
 
   /* 5.5 could not check */
@@ -328,7 +365,7 @@
         first ? h("a", { class: "btn primary lg", href: G.url.timeline(S.token, first.q.id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
         h("a", { class: "btn lg " + (first ? "" : "primary"), href: nextHref, "data-testid": "btn-next-step" }, nextLabel))),
       h("div", { class: "panel" }, h("h2", {}, "Your answers"), h("p", { class: "muted" }, "Every item in the order you saw it. Change any answer here."), h("ol", { class: "answers", "data-testid": "answers-list" }, rows),
-        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. “AI draft” means an AI wrote it. “Written by you” means you did. A second AI check read each one against the record.")),
+        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. “AI draft” means an AI wrote it. “Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
       trayDone.length ? h("div", { class: "panel", "data-testid": "tray-done" }, h("h2", {}, "Items we couldn't check"), h("p", { class: "muted" }, "These are optional. They stay out of the letter unless you wrote the line yourself."),
         h("ul", { class: "plain-list" }, trayDone.map((t) => h("li", {}, h("a", { href: G.url.timeline(S.token, t.id) }, t.kind === "flag" ? "A suggested warning we couldn't confirm" : "A record with no line"), t.review_status === "dismissed" ? " (skipped)" : "")))) : null,
       filtered ? h("div", { class: "panel", "data-testid": "filtered-rules" }, h("h2", {}, "Suggestions a rule ruled out (nothing to do)"),
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:33.270Z

**tool call — Bash**
````
{
 "command": "git diff 26287b9 9ab8cae -- app/frontend/guided/step4.js app/backend/export.py; git log --oneline 26287b9..9ab8cae | cat",
 "description": "Show step4 and export diffs, commit range"
}
````

### User / tool · 2026-11-02T22:52:33.390Z

**tool result**
````
diff --git a/app/backend/export.py b/app/backend/export.py
index 8776c50..499636c 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -36,6 +36,8 @@ SOURCE_PREFIX = "Source [Ex. __ / Bates __]: "
 TOTAL_PREFIX = "Billed charges accepted from these records: "  # D-019: nothing may follow the amount, ever
 AI_LINE = ("This chronology was drafted with AI assistance; every item in the treatment section was accepted "
            "by the paralegal. Items not reviewed: {n}.")
+AI_LINE_PREPARED = ("This chronology was built from answers the team prepared for this demo and checked by a second check; every item in the treatment section was accepted "
+                    "by the paralegal. Items not reviewed: {n}.")      # D-069: the notes of a prepared case never say an AI drafted it
 FLAGGED_HEADING = ("FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or "
                    "dismiss the entry to remove it; hedge sentences cannot be removed)")
 
@@ -43,6 +45,7 @@ IN = ("accepted", "edited")
 STYLES = ("standard", "oneline")      # T-121: "standard" (default) is the golden layout; "oneline" gives one line per entry
 # T-121: the translation note is a bracketed, removable phrase at the end of the entry, keyed by the item's translation label (never a line prefix).
 TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
+                    "Prepared translation": "[Prepared translation of the Spanish original; check before sending]",
                     "Translation (edited by reviewer)": "[Translation of the Spanish original, edited by reviewer; check before sending]"}
 NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
 OUT = ("dismissed", "rejected")
@@ -134,6 +137,7 @@ class _View:
         self.flags = list(case.get("flags", []))
         self.narrative = case.get("narrative") if narrative_in_letter() else None      # D-067: the drafted paragraph is cut from the MVP; it never reaches the letter (or the notes) unless NARRATIVE_IN_LETTER=1
         self.overlaps = list(case.get("possible_overlaps") or [])
+        self.prepared = bool(case.get("prepared"))      # D-069: the case's answers are the team's prepared ones, so no sentence of the notes says an AI drafted them
 
     def verbatim(self, item):
         """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
@@ -660,14 +664,14 @@ def _edited(v):
     out = []
     for e in v.entries:
         if e.get("entered_by_reviewer") and _status(e) == "in":
-            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer (the AI did not draft this entry); summary "{e["summary"]}"'
+            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer' + ("" if v.prepared else " (the AI did not draft this entry)") + f'; summary "{e["summary"]}"'
                        + ".")
         if not _was_edited(e):
             continue
         bits = []
         if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
             if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
-                bits.append(f'summary was AI wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
+                bits.append(f'summary was {"prepared" if v.prepared else "AI"} wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
             else:
                 bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
         if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
@@ -714,7 +718,8 @@ def _draft_paragraph(v):
         return []
     live = {e["id"]: e for e in v.in_entries}
     st = n.get("status", "pending")
-    lines = ["", "DRAFT TREATMENT PARAGRAPH (AI-drafted from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
+    prep = getattr(v, "prepared", False)
+    lines = ["", f"DRAFT TREATMENT PARAGRAPH ({'drafted' if prep else 'AI-drafted'} from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
     lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
                   "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
     for s in n.get("sentences", []):
@@ -724,7 +729,7 @@ def _draft_paragraph(v):
         lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
     for r in n.get("removed", []):
         if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
-            lines.append(f'- AI wording removed (failed a check: {_removed_why(r)}) ({r["entry_id"]}).')
+            lines.append(f'- {"Prepared" if prep else "AI"} wording removed (failed a check: {_removed_why(r)}) ({r["entry_id"]}).')
         elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
             lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}).')
         else:
@@ -738,7 +743,7 @@ def _notes(v):
     pending = _pending(v)
     sec = [
         NOTES_TITLE, "",
-        AI_LINE.format(n=len(pending)), "",
+        (AI_LINE_PREPARED if v.prepared else AI_LINE).format(n=len(pending)), "",
         "FLAGS ACCEPTED", *_flag_block(v, accepted), "",
         "FLAGS DISMISSED", *_flag_block(v, dismissed), "",
         FLAGGED_HEADING, *_flagged_language(v, v.flags), "",
diff --git a/app/frontend/guided/step4.js b/app/frontend/guided/step4.js
index 4566197..b2c6706 100644
--- a/app/frontend/guided/step4.js
+++ b/app/frontend/guided/step4.js
@@ -16,7 +16,7 @@
     ctx.view.append(main);
 
     const head = () => h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, "Step 4 of 4"), h("h1", { "data-testid": "page-title", tabindex: "-1" }, "Get your letter"),
-      h("p", {}, "Copy the treatment section into your demand letter, or download it. The notes on the right are for the attorney only.")));
+      h("p", {}, "Copy the treatment section into your demand letter, or download it. The notes for the attorney are separate and are for the attorney only.")));
 
     /* ---- load ---- */
     async function load() {
@@ -145,8 +145,20 @@
         catch (e) { if (e.name === "AbortError") return; err.textContent = e.message; }
         finally { save.disabled = false; }
       });
-      return h("div", { class: "panel cfg-panel" }, h("h2", {}, "Exhibit and page numbers (optional)"), h("p", { class: "muted" }, "Fill these in to replace “[Ex. __ / Bates __]” in every source line."),
-        h("div", { class: "cfg" }, ex.f, bp.f, bs.f, save), err);
+      /* one Bates number per RECORD (the server counts record 1, record 2 ... in the order the records were read), and nothing in the records says how many pages each one is */
+      const nRec = ((c && c.records) || []).length, pad = (n) => String(n).padStart(4, "0");
+      const cite = (n) => { const st = val(bs) === "" || !/^\d{1,8}$/.test(val(bs)) ? 1 : Number(val(bs)); return `[Ex. ${val(ex) || "__"} / Bates ${val(bp) || val(bs) ? (val(bp) + pad(st + n - 1)) : "__"}]`; };
+      const preview = h("p", { class: "cfg-preview", "data-testid": "cfg-preview", "aria-live": "polite" });
+      const drawPreview = () => {
+        if (!val(ex) && !val(bp) && !val(bs)) { preview.textContent = "Nothing filled in: every source line keeps “[Ex. __ / Bates __]” for you to fill in."; return; }
+        preview.textContent = nRec > 1 ? `In your letter: record 1 reads ${cite(1)}, record 2 reads ${cite(2)}, and record ${nRec} reads ${cite(nRec)}.` : `In your letter: record 1 reads ${cite(1)}.`;
+      };
+      [ex, bp, bs].forEach((x) => x.f.querySelector("input").addEventListener("input", drawPreview));
+      queueMicrotask(drawPreview);
+      return h("div", { class: "panel cfg-panel", "data-testid": "cfg-panel" }, h("h2", {}, "Exhibit and Bates numbers (optional)"),
+        h("p", { "data-testid": "cfg-rule" }, h("b", {}, "One Bates number per record, not per page. "), `Record 1 gets the first number you type, record 2 gets the next number, and so on in the order the records were read (${nRec} record${nRec === 1 ? "" : "s"} here). Use this only if each of your records is one Bates page in that order.`),
+        h("p", { class: "muted" }, "If your records are longer, or in a different order, leave these blank and fill in the page numbers in Word. Filled in, the numbers replace “[Ex. __ / Bates __]” in every source line of the letter, and the letter then cites those pages."),
+        h("div", { class: "cfg" }, ex.f, bp.f, bs.f, save), preview, err);
     }
 
     function showError(e) {
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
dfd9b11 docs(submission): NEEDS_CHRIS publish-from-snapshot item, T-193, row 8 to P2
3feb096 test(backend): T-177 r4 e2e: golden notes normalize the prepared disclosure line; classic tag tooltip stays exempt until the frontend card
c27e7f1 fix(backend): T-177 r4 D-069 prepared wording from templates keyed by provenance (no swap table); malformed or empty prepared answer is a missing one; property test over fault-injected curated sets
9b40445 docs(backend): T-196 api.md D-066 compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)
a5deecc docs(release): README walkthrough matches the guided UI labels; OWNER URL explained (T-182)
c5caf61 test(qa): skip history-dependent provenance tests in a one-commit snapshot (T-194)
aca9827 chore: ignore deploy/.private_patterns (T-194)
ef5d588 docs(release): T-194 r2 SNAPSHOT.md: allow-list, local patterns file, run log, make test result and the 3 history-dependent tests
52e115a chore(tools): pre-commit frontend smoke includes the guided golden path (T-182 r2 lesson)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:52:38.460Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && sed -e 's/26287b9, demo mode, port 7931/9ab8cae r2, demo mode, port 7941/' -e 's#127.0.0.1:7931#127.0.0.1:7941#' -e 's#os.path.join(OUT, \"profile\")#os.path.join(OUT, os.environ.get(\"T181_PROFILE\", \"profile\"))#' /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal/h.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/h.py && grep -n \"BASE =\\|PROFILE =\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/h.py",
 "description": "Create r2 evidence dir and adapted helper"
}
````

### User / tool · 2026-11-02T22:52:38.582Z

**tool result**
````
11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7941")
13:PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:11.474Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r01_sample_e2e.py",
 "content": "\"\"\"T-181 r2: sample case end to end, timed, keyboard-first. Home -> Open the sample -> Draft -> Step 2 -> Step 3 -> Step 4 -> downloads.\nRun: T181_BASE=http://127.0.0.1:7941 .venv/bin/python -I artifacts/review-evidence/T-181-paralegal-r2/h.py artifacts/review-evidence/T-181-paralegal-r2/r01_sample_e2e.py\n\"\"\"\nimport re, json\nT0 = time.time()\nC = {\"keys\": 0, \"clicks\": 0}\nctx.grant_permissions([\"clipboard-read\", \"clipboard-write\"], origin=BASE)\n\ndef T():\n    return round(time.time() - T0, 1)\n\ndef item_id():\n    m = re.search(r\"item=([^&]+)\", pg.url)\n    return m.group(1) if m else None\n\ndef info(label):\n    pg.wait_for_timeout(300)\n    title = pg.evaluate(\"() => (document.querySelector('.titlebar') || {innerText:''}).innerText\").replace(\"\\n\", \" | \")\n    acts = pg.evaluate(\"() => (document.querySelector('.actions') || {innerText:''}).innerText\").replace(\"\\n\", \" | \")\n    ae = pg.evaluate(\"() => { const a = document.activeElement; return a ? a.tagName + '[' + (a.getAttribute('data-testid')||'') + ']' : null }\")\n    log(f\"[{T()}s] {label} item={item_id()} | {title[-60:]} | ACT: {acts[:220]} | focus {ae}\")\n\ndef card(n):\n    iid = item_id()\n    right = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }\")\n    src = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[0].innerText.split('\\\\n').slice(0,2).join(' | ') : '' }\")\n    marks = pg.evaluate(\"() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)\")\n    outs = pg.evaluate(\"() => Array.from(document.querySelectorAll('[data-testid=outside-word]')).map(m => m.innerText)\")\n    unc = pg.evaluate(\"() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText : null }\")\n    log(f\"######## {n} item={iid} t={T()}s\")\n    log(\"SRC:\", src)\n    log(\"CARD:\", right.replace(\"\\n\", \" / \"))\n    log(\"MARKS:\", marks)\n    log(\"OUTSIDE-WORDS:\", outs, \"| UNCOVERED:\", unc)\n    shot(f\"s2-{n:02d}-{iid}\")\n\ndef key(k, label=None):\n    C[\"keys\"] += 1\n    pg.keyboard.press(k)\n    info(label or k)\n\ndef tab_to(prefix):\n    for i in range(8):\n        pg.keyboard.press(\"Tab\"); C[\"keys\"] += 1\n        ae = pg.evaluate(\"() => (document.activeElement.innerText||'').trim()\")\n        if ae.startswith(prefix):\n            return True\n    log(\"could not tab to\", prefix)\n    return False\n\n# ---- Home -> Open the sample case\npg.goto(BASE + \"/\")\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\ndump(\"home first visit\")\nshot(\"01-home\")\npg.get_by_role(\"button\", name=\"Open the sample case\").click(); C[\"clicks\"] += 1\npg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)\npg.wait_for_timeout(300)\nlog(f\"[{T()}s] step 1 shown\")\ndump(\"step 1 records\")\nshot(\"02-step1\")\nTD = time.time()\npg.click(\"[data-testid=btn-draft]\"); C[\"clicks\"] += 1\nfor i in range(120):\n    pg.wait_for_timeout(250)\n    if pg.query_selector(\"text=Go to step 2\") or \"/timeline\" in pg.url:\n        break\nlog(f\"[{T()}s] draft took {round(time.time()-TD,1)}s\")\ndump(\"after draft\")\nshot(\"03-after-draft\")\nif \"/timeline\" not in pg.url:\n    pg.get_by_text(\"Go to step 2\").first.click(); C[\"clicks\"] += 1\n    pg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.wait_for_timeout(400)\nif not item_id():\n    btn = pg.query_selector(\"text=Start\") or pg.query_selector(\"[data-testid=btn-first-undecided]\")\n    if btn:\n        btn.click(); C[\"clicks\"] += 1\n        pg.wait_for_timeout(400)\ninfo(\"step 2 first item\")\n\n# ---- Step 2\nn = 0\nreloaded = False\nseen = []\nfor step in range(40):\n    iid = item_id()\n    if not iid or \"/timeline\" not in pg.url:\n        break\n    seen.append(iid)\n    card(n)\n    n += 1\n    if iid == \"e3\":\n        key(\"e\", \"E on record 3 (fix wording)\")\n        ta = pg.locator(\"[data-testid=edit-summary]\")\n        log(\"textarea before:\", ta.input_value())\n        pg.keyboard.press(\"Meta+A\"); C[\"keys\"] += 1\n        pg.keyboard.type(\"Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks.\"); C[\"keys\"] += 1\n        tab_to(\"Save\")\n        pg.keyboard.press(\"Enter\"); C[\"keys\"] += 1\n        info(\"after save wording\")\n        card(99)\n        shot(\"s2-e3-edited-compare\")\n        key(\"a\", \"a (expect focus to compare box)\")\n        key(\"Space\", \"Space ticks compare\")\n        shot(\"s2-e3-ticked\")\n        key(\"a\", \"a accepts edited e3\")\n    elif iid.startswith(\"f_gap\"):\n        key(\"e\", \"E on gap: add a note\")\n        pg.keyboard.type(\"Ask client about March-May 2026: any care elsewhere? Records request if so.\"); C[\"keys\"] += 1\n        tab_to(\"Save\")\n        pg.keyboard.press(\"Enter\"); C[\"keys\"] += 1\n        info(\"after gap note save\")\n        shot(\"s2-gap-after-note\")\n        if item_id() == iid:\n            key(\"a\", \"a on gap after note\")\n    elif iid == \"f_r7_1\":\n        key(\"d\", \"D dismiss accident-date-source flag\")\n    else:\n        yes = pg.query_selector(\"[data-testid=answer-yes]\")\n        if (yes and yes.is_disabled()) and pg.query_selector(\"[data-testid=check-compare]\"):\n            key(\"a\", \"a (compare)\"); key(\"Space\", \"tick\"); key(\"a\", \"a accept\")\n        else:\n            key(\"a\", f\"a {iid}\")\n    if iid == \"e5\" and not reloaded:\n        reloaded = True\n        pg.reload()\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        info(\"after reload mid-review\")\n        shot(\"s2-after-reload\")\nlog(f\"[{T()}s] step 2 items seen in order: {seen}\")\npg.wait_for_timeout(500)\ndump(\"step 2 done screen\")\nshot(\"04-step2-done\", full=True)\n\n# ---- Step 3\nnxt = pg.query_selector(\"[data-testid=btn-next-step]\")\nlog(\"step2 next label:\", nxt.inner_text() if nxt else None)\nnxt.click(); C[\"clicks\"] += 1\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.wait_for_timeout(500)\nif not item_id():\n    dump(\"step 3 landing\")\n    b = pg.query_selector(\"[data-testid=btn-first-undecided]\") or pg.query_selector(\"text=Start\")\n    if b:\n        b.click(); C[\"clicks\"] += 1\n        pg.wait_for_timeout(400)\nm = 0\nfor step in range(20):\n    iid = item_id()\n    if not iid or \"/bills\" not in pg.url:\n        break\n    right = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }\")\n    acts = pg.evaluate(\"() => (document.querySelector('.actions') || {innerText:''}).innerText\").replace(\"\\n\", \" | \")\n    log(f\"######## bills {m} item={iid} t={T()}s\")\n    log(\"CARD:\", right.replace(\"\\n\", \" / \"))\n    log(\"ACT:\", acts)\n    shot(f\"s3-{m:02d}-{iid}\")\n    m += 1\n    yes = pg.query_selector(\"[data-testid=answer-yes]\")\n    if yes and yes.is_disabled():\n        key(\"a\", \"a (box)\"); key(\"Space\", \"tick\"); key(\"a\", \"a\")\n    else:\n        key(\"a\", f\"a {iid}\")\npg.wait_for_timeout(500)\ndump(\"step 3 done\")\nshot(\"05-step3-done\", full=True)\n\n# ---- Step 4\npg.get_by_text(\"Go to step 4\").first.click(); C[\"clicks\"] += 1\npg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\npg.wait_for_timeout(600)\nlog(f\"[{T()}s] step 4 shown\")\nwith pg.expect_download() as d:\n    pg.click(\"[data-testid=btn-download-letter]\"); C[\"clicks\"] += 1\nd.value.save_as(OUT + \"/letter-download.txt\")\nTL = time.time() - T0\nlog(f\"[{round(TL,1)}s] LETTER DOWNLOADED as {d.value.suggested_filename}\")\nwith pg.expect_download() as d2:\n    pg.click(\"[data-testid=btn-download-notes]\")\nd2.value.save_as(OUT + \"/notes-download.txt\")\npg.click(\"[data-testid=btn-copy-letter]\")\npg.wait_for_timeout(300)\nclip = pg.evaluate(\"() => navigator.clipboard.readText()\")\nopen(OUT + \"/letter-clipboard.txt\", \"w\").write(clip)\nlog(\"clipboard == download:\", clip == open(OUT + \"/letter-download.txt\").read())\ndump(\"step 4 page\")\nshot(\"06-step4\", full=True)\nopen(OUT + \"/r01_counts.json\", \"w\").write(json.dumps({\"keys\": C[\"keys\"], \"clicks\": C[\"clicks\"], \"to_letter_s\": round(TL, 1), \"step2_items\": seen}))\n"
}
````

### User / tool · 2026-11-02T22:53:11.588Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r01_sample_e2e.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:14.402Z

**tool call — Bash**
````
{
 "command": "T181_BASE=http://127.0.0.1:7941 .venv/bin/python -I artifacts/review-evidence/T-181-paralegal-r2/h.py artifacts/review-evidence/T-181-paralegal-r2/r01_sample_e2e.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r01.out 2>&1; echo exit $?; grep -n \"^\\[\\|LETTER\\|draft took\\|clipboard\\|ERRORS\\|http \\|Traceback\\|Error\" artifacts/review-evidence/T-181-paralegal-r2/r01.out | head -80",
 "description": "Run timed sample end-to-end script",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T22:53:32.532Z

**tool result**
````
exit 0
25:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/01-home.png
26:[0.9s] step 1 shown
92:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/02-step1.png
93:[2.5s] draft took 1.3s
166:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/03-after-draft.png
167:[3.5s] step 2 first item item=e1 | er against its quote. | Item 1 of 19 | 0 answered · 19 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Keys: A says yes, D says no, E fixes or adds a note, the arrow keys mov | focus BUTTON[answer-yes]
173:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-00-e1.png
174:[3.9s] a e1 item=f_accident_date_after_treatment_1_2_7 | er against its quote. | Item 2 of 19 | 1 answered · 18 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 1 kept in the letter. | Undo | focus BUTTON[answer-yes]
181:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-01-f_accident_date_after_treatment_1_2_7.png
182:[4.2s] a f_accident_date_after_treatment_1_2_7 item=e2 | er against its quote. | Item 3 of 19 | 2 answered · 17 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 2 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
188:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-02-e2.png
189:[4.6s] a e2 item=e3 | er against its quote. | Item 4 of 19 | 3 answered · 16 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 3 kept in the letter. | Undo | focus BUTTON[answer-yes]
196:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-03-e3.png
197:[4.9s] E on record 3 (fix wording) item=e3 | er against its quote. | Item 4 of 19 | 3 answered · 16 to go | ACT: Change the line, then save it. |  | Save my wording | Cancel | ‹ Back | Decide later |  | Keys: A says yes, D says no, the arrow keys move between items. | focus TEXTAREA[edit-summary]
199:[5.3s] after save wording item=e3 | er against its quote. | Item 4 of 19 | 3 answered · 16 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: your wording is in. Read it once more against the highlighted wo | focus INPUT[check-compare]
206:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-99-e3.png
207:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-e3-edited-compare.png
208:[5.7s] a (expect focus to compare box) item=e3 | er against its quote. | Item 4 of 19 | 3 answered · 16 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: your wording is in. Read it once more against the highlighted wo | focus INPUT[check-compare]
209:[6.0s] Space ticks compare item=e3 | er against its quote. | Item 4 of 19 | 3 answered · 16 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: your wording is in. Read it once more against the highlighted wo | focus INPUT[check-compare]
210:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-e3-ticked.png
211:[6.4s] a accepts edited e3 item=f_r3_1 | er against its quote. | Item 5 of 19 | 4 answered · 15 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 4 kept in the letter. | Undo | focus BUTTON[answer-yes]
217:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-04-f_r3_1.png
218:[6.7s] a f_r3_1 item=e4 | er against its quote. | Item 6 of 19 | 5 answered · 14 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 5 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
224:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-05-e4.png
225:[7.0s] a e4 item=f_cx1 | er against its quote. | Item 7 of 19 | 6 answered · 13 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 6 kept in the letter. | Undo | focus BUTTON[answer-yes]
231:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-06-f_cx1.png
232:[7.4s] a f_cx1 item=e5 | er against its quote. | Item 8 of 19 | 7 answered · 12 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 7 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
239:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-07-e5.png
240:[7.7s] a e5 item=e6 | er against its quote. | Item 9 of 19 | 8 answered · 11 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 8 kept in the letter. | Undo | focus BUTTON[answer-yes]
241:[8.1s] after reload mid-review item=e6 | er against its quote. | Item 9 of 19 | 8 answered · 11 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Keys: A says yes, D says no, E fixes or adds a note, the arrow keys mov | focus BODY[]
242:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-after-reload.png
248:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-08-e6.png
249:[8.5s] a e6 item=f_gap_r6_r7 | r against its quote. | Item 10 of 19 | 9 answered · 10 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 9 kept in the letter. | Undo | focus BUTTON[answer-yes]
256:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-09-f_gap_r6_r7.png
257:[8.8s] E on gap: add a note item=f_gap_r6_r7 | r against its quote. | Item 10 of 19 | 9 answered · 10 to go | ACT: Write your note, then save it. |  | Save note | Cancel | ‹ Back | Decide later |  | Keys: A says yes, D says no, the arrow keys move between items. | focus TEXTAREA[edit-note]
258:[9.2s] after gap note save item=f_r6_1 | r against its quote. | Item 11 of 19 | 10 answered · 9 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 10 will go in the notes for the attorney, with your note. | Undo | focus BUTTON[answer-yes]
259:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-gap-after-note.png
265:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-10-f_r6_1.png
266:[9.6s] a f_r6_1 item=e7 | r against its quote. | Item 12 of 19 | 11 answered · 8 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 11 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
273:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-11-e7.png
274:[9.9s] a e7 item=f_r7_1 | r against its quote. | Item 13 of 19 | 12 answered · 7 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 12 kept in the letter. | Undo | focus BUTTON[answer-yes]
280:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-12-f_r7_1.png
281:[10.3s] D dismiss accident-date-source flag item=f_r7_2 | r against its quote. | Item 14 of 19 | 13 answered · 6 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 13 marked not needed. | Undo | focus BUTTON[answer-yes]
288:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-13-f_r7_2.png
289:[10.6s] a f_r7_2 item=e8 | r against its quote. | Item 15 of 19 | 14 answered · 5 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 14 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
295:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-14-e8.png
296:[11.0s] a e8 item=f_r8_1 | r against its quote. | Item 16 of 19 | 15 answered · 4 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 15 kept in the letter. | Undo | focus BUTTON[answer-yes]
302:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-15-f_r8_1.png
303:[11.3s] a f_r8_1 item=f_r8_2 | r against its quote. | Item 17 of 19 | 16 answered · 3 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 16 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
309:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-16-f_r8_2.png
310:[11.6s] a f_r8_2 item=e9 | r against its quote. | Item 18 of 19 | 17 answered · 2 to go | ACT: Does this line say the same thing as the highlighted words? |  | Yes, this matches | No, leave it out | ‹ Back | Fix the wording | Decide later |  | Saved: item 17 will go in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
316:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-17-e9.png
317:[12.0s] a e9 item=f_r9_1 | r against its quote. | Item 19 of 19 | 18 answered · 1 to go | ACT: Should the attorney be told about this? |  | Yes, tell the attorney | No, not needed | ‹ Back | Add a note | Decide later |  | Saved: item 18 kept in the letter. | Undo | focus BUTTON[answer-yes]
323:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-18-f_r9_1.png
324:[12.3s] a f_r9_1 item=None |  | ACT:  | focus H1[page-title]
325:[12.3s] step 2 items seen in order: ['e1', 'f_accident_date_after_treatment_1_2_7', 'e2', 'e3', 'f_r3_1', 'e4', 'f_cx1', 'e5', 'e6', 'f_gap_r6_r7', 'f_r6_1', 'e7', 'f_r7_1', 'f_r7_2', 'e8', 'f_r8_1', 'f_r8_2', 'e9', 'f_r9_1']
469:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/04-step2-done.png
474:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s3-00-a1.png
475:[14.2s] a a1 item=a4 | al so far | $6,240.00 | Amount 2 of 4 | 1 answered · 3 to go | ACT: Should this charge count toward the bill total? |  | Yes, count it | No, don't count it | ‹ Back | Decide later |  | Saved: amount 1 $6,240.00 counted in the bill total. | Undo | focus BUTTON[answer-yes]
479:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s3-01-a4.png
480:[14.5s] a a4 item=a2 | al so far | $8,390.00 | Amount 3 of 4 | 2 answered · 2 to go | ACT: This amount is never added to the total. List it in the notes for the attorney? |  | Yes, list it | No, leave it out | ‹ Back | Decide later |  | Saved: amount 2 $2,150.00 counted in the bill total. | Undo | focus BUTTON[answer-yes]
484:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s3-02-a2.png
485:[14.9s] a a2 item=a3 | al so far | $8,390.00 | Amount 4 of 4 | 3 answered · 1 to go | ACT: This amount is never added to the total. List it in the notes for the attorney? |  | Yes, list it | No, leave it out | ‹ Back | Decide later |  | Saved: amount 3 $185.00 listed in the notes for the attorney. | Undo | focus BUTTON[answer-yes]
489:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s3-03-a3.png
490:[15.2s] a a3 item=None |  | ACT:  | focus H1[page-title]
543:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/05-step3-done.png
544:[16.8s] step 4 shown
545:[16.9s] LETTER DOWNLOADED as sample-case-letter.txt
546:clipboard == download: True
646:FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
695:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/06-step4.png
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:34.885Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && grep -n \"^CARD:\\|^SRC:\\|^MARKS:\\|^OUTSIDE\" r01.out | cut -c1-700",
 "description": "Show every Step 2 card text from the run"
}
````

### User / tool · 2026-11-02T22:53:35.032Z

**tool result**
````
169:SRC: From the record | Record 1 · Austin EMS run report · January 9, 2026
170:CARD: Prepared answer / January 9, 2026 · Austin EMS run report /  / Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
171:MARKS: ['41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.']
172:OUTSIDE-WORDS: [] | UNCOVERED: None
176:SRC: From the record | Records 1, 2 and 7
177:CARD: Warning for the attorney /  / The records disagree about the accident date /  / Stated accident date is later than recorded treatment /  / Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
178:MARKS: ['Date: 2026-01-09', 'Date: 2026-01-09', 'Date of accident per intake form: 2026-01-19']
179:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
184:SRC: From the record | Record 2 · Central ER discharge summary · January 9, 2026
185:CARD: Prepared answer / January 9, 2026 · Central ER discharge summary /  / Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
186:MARKS: ['Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.']
187:OUTSIDE-WORDS: [] | UNCOVERED: None
191:SRC: From the record | Record 3 · Dr. Alvarez, primary care · January 16, 2026
192:CARD: Prepared answer / January 16, 2026 · Dr. Alvarez, primary care /  / Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
193:MARKS: ['Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.']
194:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
201:SRC: From the record | Record 3 · Dr. Alvarez, primary care · January 16, 2026
202:CARD: Written by you / January 16, 2026 · Dr. Alvarez, primary care /  / Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks. /  / You changed the wording. Read it against the highlighted words once more. / I read this line against the highlighted words myself. /  / A second AI check is not available in this demo, so this item has not been double-checked. Compare the line with the highlighted words yourself; if they match, accept it. Until you do, the item stays marked for review.
203:MARKS: ['Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.']
204:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
213:SRC: From the record | Record 3 · Dr. Alvarez, primary care · January 16, 2026
214:CARD: Warning for the attorney / Prepared answer /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
215:MARKS: ['Patient reports low back pain in 2023, resolved.']
216:OUTSIDE-WORDS: [] | UNCOVERED: None
220:SRC: From the record | Record 4 · Capital PT, initial evaluation · January 23, 2026
221:CARD: Prepared answer / January 23, 2026 · Capital PT, initial evaluation /  / Cervical range of motion reduced approx. 40%; plan of care 12 visits. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
222:MARKS: ['Cervical range of motion reduced approx. 40%. Plan of care: 12 visits.']
223:OUTSIDE-WORDS: [] | UNCOVERED: None
227:SRC: From the record | Records 4 and 6
228:CARD: Warning for the attorney /  / The plan and what happened differ /  / Treatment plan and what followed differ /  / Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
229:MARKS: ['Plan of care: 12 visits.', 'Discharged from PT after two missed appointments.']
230:OUTSIDE-WORDS: [] | UNCOVERED: None
234:SRC: From the record | Record 5 · Capital PT, visit 8 · February 20, 2026
235:CARD: Prepared answer / February 20, 2026 · Capital PT, visit 8 /  / Pain 4/10, improving. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
236:MARKS: ['Pain 4/10, improving.']
237:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
244:SRC: From the record | Record 6 · Capital PT, visit 9 · March 6, 2026
245:CARD: Prepared answer / March 6, 2026 · Capital PT, visit 9 /  / Discharged from physical therapy after two missed appointments; pain 3/10. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
246:MARKS: ['Discharged from PT after two missed appointments. Pain 3/10.']
247:OUTSIDE-WORDS: [] | UNCOVERED: None
251:SRC: From the record | Records 6 and 7
252:CARD: Warning for the attorney /  / A break in treatment /  / Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient). /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
253:MARKS: ['Date: 2026-03-06', 'Source: Capital PT, visit 9', 'Date: 2026-05-18', 'Source: Hill Country Pain Management, new patient']
254:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
261:SRC: From the record | Record 6 · Capital PT, visit 9 · March 6, 2026
262:CARD: Warning for the attorney / Prepared answer /  / Missed or ended treatment /  / Missed or ended care /  / Wording about missed appointments or ending care in Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
263:MARKS: ['Discharged from PT after two missed appointments.']
264:OUTSIDE-WORDS: [] | UNCOVERED: None
268:SRC: From the record | Record 7 · Hill Country Pain Management, new patient · May 18, 2026
269:CARD: Prepared answer / May 18, 2026 · Hill Country Pain Management, new patient /  / New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
270:MARKS: ['New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.']
271:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
276:SRC: From the record | Record 7 · Hill Country Pain Management, new patient · May 18, 2026
277:CARD: Warning for the attorney / Prepared answer /  / Where the accident date comes from /  / Accident date source /  / Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): “Date of accident per intake form: 2026-01-19.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
278:MARKS: ['Date of accident per intake form: 2026-01-19.']
279:OUTSIDE-WORDS: [] | UNCOVERED: None
283:SRC: From the record | Record 7 · Hill Country Pain Management, new patient · May 18, 2026
284:CARD: Warning for the attorney / Prepared answer /  / Wording about a new problem /  / New-onset wording in Hill Country Pain Management, new patient (May 18, 2026): “New onset pain”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
285:MARKS: ['New onset pain']
286:OUTSIDE-WORDS: [] | UNCOVERED: Also in this record, outside the highlighted words:
291:SRC: From the record | Record 8 · Austin Imaging, cervical MRI · May 29, 2026
292:CARD: Prepared answer / May 29, 2026 · Austin Imaging, cervical MRI /  / C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
293:MARKS: ['C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.']
294:OUTSIDE-WORDS: [] | UNCOVERED: None
298:SRC: From the record | Record 8 · Austin Imaging, cervical MRI · May 29, 2026
299:CARD: Warning for the attorney / Prepared answer /  / Wording about wear and tear /  / Degenerative wording /  / Austin Imaging, cervical MRI (May 29, 2026) uses degenerative wording: “Findings may represent degenerative change”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
300:MARKS: ['Findings may represent degenerative change']
301:OUTSIDE-WORDS: [] | UNCOVERED: None
305:SRC: From the record | Record 8 · Austin Imaging, cervical MRI · May 29, 2026
306:CARD: Warning for the attorney / Prepared answer /  / Hedged wording (“may”, “possible”) /  / Hedged wording in Austin Imaging, cervical MRI (May 29, 2026): “may represent degenerative change; correlate clinically”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
307:MARKS: ['may represent degenerative change; correlate clinically']
308:OUTSIDE-WORDS: [] | UNCOVERED: None
312:SRC: From the record | Record 9 · Hill Country Pain Management, follow-up · June 12, 2026
313:CARD: Prepared answer / June 12, 2026 · Hill Country Pain Management, follow-up /  / Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
314:MARKS: ['Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.']
315:OUTSIDE-WORDS: [] | UNCOVERED: None
319:SRC: From the record | Record 9 · Hill Country Pain Management, follow-up · June 12, 2026
320:CARD: Warning for the attorney / Prepared answer /  / The patient, not a doctor, says what caused it /  / Reported onset /  / Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
321:MARKS: ['Patient states symptoms began after the January collision.']
322:OUTSIDE-WORDS: [] | UNCOVERED: None
472:CARD: Charge / Central ER discharge summary · January 9, 2026 /  / $6,240.00 /  / Written in the record as $6,240. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
477:CARD: Charge / Austin Imaging, cervical MRI · May 29, 2026 /  / $2,150.00 /  / Written in the record as $2,150. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
482:CARD: Never counted / Capital PT, initial evaluation · January 23, 2026 /  / $185 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
487:CARD: Never counted / Capital PT, visit 8 · February 20, 2026 /  / Not a money amount: missing 3 days of work /  / This figure is not a bill (for example a damages or settlement figure), so it is not added to the total. /  / Either way, it is never added to the bill total.
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:38.624Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && cat -n letter-download.txt; echo =====; cat -n notes-download.txt | head -90",
 "description": "Read downloaded letter and notes"
}
````

### User / tool · 2026-11-02T22:53:38.719Z

**tool result**
````
     1	TREATMENT CHRONOLOGY
     2	
     3	January 9, 2026 — Austin EMS run report
     4	Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
     5	Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
     6	
     7	January 9, 2026 — Central ER discharge summary
     8	Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
     9	Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
    10	
    11	January 16, 2026 — Dr. Alvarez, primary care
    12	Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks.
    13	Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
    14	
    15	January 23, 2026 — Capital PT, initial evaluation
    16	Cervical range of motion reduced approx. 40%; plan of care 12 visits.
    17	Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
    18	
    19	February 20, 2026 — Capital PT, visit 8
    20	Pain 4/10, improving.
    21	Source [Ex. __ / Bates __]: "Pain 4/10, improving."
    22	
    23	March 6, 2026 — Capital PT, visit 9
    24	Discharged from physical therapy after two missed appointments; pain 3/10.
    25	Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."
    26	
    27	May 18, 2026 — Hill Country Pain Management, new patient
    28	New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
    29	Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
    30	
    31	May 29, 2026 — Austin Imaging, cervical MRI
    32	C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
    33	Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
    34	
    35	June 12, 2026 — Hill Country Pain Management, follow-up
    36	Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
    37	Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
    38	
    39	BILLED CHARGES
    40	
    41	Central ER discharge summary, January 9, 2026: $6,240.00
    42	Source [Ex. __ / Bates __]: "ER charges: $6,240."
    43	Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
    44	Source [Ex. __ / Bates __]: "Charge: $2,150."
    45	
    46	Billed charges accepted from these records: $8,390.00=====
     1	INTERNAL REVIEW NOTES — DO NOT SEND
     2	
     3	This chronology was built from answers the team prepared for this demo and checked by a second check; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
     4	
     5	FLAGS ACCEPTED
     6	- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026). Reviewer note: Ask client about March-May 2026: any care elsewhere? Records request if so.
     7	- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
     8	- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
     9	- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
    10	- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain".
    11	
    12	FLAGS DISMISSED
    13	- Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
    14	
    15	FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
    16	- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
    17	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
    18	- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
    19	- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
    20	- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
    21	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
    22	
    23	AMOUNTS NOT TOTALED
    24	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
    25	
    26	DAMAGES MENTIONS (not charges)
    27	- Record 5 (Capital PT, visit 8, February 20, 2026): "Patient reports missing 3 days of work."
    28	
    29	FUTURE TREATMENT RECOMMENDED (no cost stated)
    30	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.
    31	
    32	BILLS TO REQUEST (entry in the letter, no accepted charge)
    33	- Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.
    34	
    35	RECORDS NOT IN THE TREATMENT SECTION
    36	- none (9 of 9 records included)
    37	
    38	EDITED ITEMS
    39	- Record 3 (Dr. Alvarez, primary care, January 16, 2026): summary was "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.", now "Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks.". (accepted by the paralegal after comparing it with the quote; second check not available)
    40	
    41	PENDING ITEMS NOT INCLUDED
    42	- none
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:46.235Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && grep -n \"DISMISSED\" -A2 T-181-paralegal/notes-download.txt; grep -n \"second check\" T-181-paralegal/notes-download.txt | head -3",
 "description": "Compare r1 notes dismissed label"
}
````

### User / tool · 2026-11-02T22:53:46.336Z

**tool result**
````
12:FLAGS DISMISSED
13-- Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
14-
39:- Record 3 (Dr. Alvarez, primary care, January 16, 2026): summary was "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.", now "Persistent neck pain 6/10 with daily headaches; physical therapy 2x/week for 6 weeks.". (accepted by the paralegal after comparing it with the quote; second check not available)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:56.982Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py",
 "content": "\"\"\"T-181 r2: Step 4 Bates panel wording, live preview, save, letter cites, reload. Sample case (the one finished by r01).\"\"\"\nimport re\npg.goto(BASE + \"/\")\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.click(\"[data-testid=btn-continue]\")\npg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\npg.wait_for_timeout(600)\npanel = pg.locator(\"[data-testid=cfg-panel]\")\npanel.scroll_into_view_if_needed()\nlog(\"PANEL (blank):\\n\" + panel.inner_text())\nshot(\"07-bates-blank\")\npg.click(\"[data-testid=cfg-exhibit]\")\npg.keyboard.type(\"3\")\nlog(\"PREVIEW after exhibit only:\", pg.inner_text(\"[data-testid=cfg-preview]\"))\npg.click(\"[data-testid=cfg-bates-prefix]\")\npg.keyboard.type(\"RIVERA\")\nlog(\"PREVIEW after prefix:\", pg.inner_text(\"[data-testid=cfg-preview]\"))\npg.click(\"[data-testid=cfg-bates-start]\")\npg.keyboard.type(\"101\")\nlog(\"PREVIEW after start 101:\", pg.inner_text(\"[data-testid=cfg-preview]\"))\npanel.scroll_into_view_if_needed()\nshot(\"08-bates-typed-preview\")\npg.click(\"[data-testid=btn-save-cfg]\")\npg.wait_for_timeout(900)\nlog(\"cfg-error:\", pg.inner_text(\"[data-testid=cfg-error]\") if pg.query_selector(\"[data-testid=cfg-error]\") else None)\ntxt = pg.inner_text(\"[data-testid=letter-text]\")\nopen(OUT + \"/letter-with-bates.txt\", \"w\").write(txt)\nfor ln in txt.split(\"\\n\"):\n    if \"Bates\" in ln or re.match(r\"^[A-Z][a-z]+ \\d\", ln):\n        log(\"LETTER:\", ln[:140])\npanel.scroll_into_view_if_needed()\nshot(\"09-bates-saved\")\npg.reload()\npg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\npg.wait_for_timeout(600)\nlog(\"after reload has RIVERA0101:\", \"RIVERA0101\" in pg.inner_text(\"[data-testid=letter-text]\"))\nlog(\"after reload PREVIEW:\", pg.inner_text(\"[data-testid=cfg-preview]\"))\n# put it back to blank so the letter is the default again\nfor t in (\"cfg-exhibit\", \"cfg-bates-prefix\", \"cfg-bates-start\"):\n    pg.fill(f\"[data-testid={t}]\", \"\")\npg.click(\"[data-testid=btn-save-cfg]\")\npg.wait_for_timeout(900)\nlog(\"after clearing: letter has [Ex. __ / Bates __]:\", \"[Ex. __ / Bates __]\" in pg.inner_text(\"[data-testid=letter-text]\"), \"| PREVIEW:\", pg.inner_text(\"[data-testid=cfg-preview]\"))\n"
}
````

### User / tool · 2026-11-02T22:53:57.101Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:53:59.613Z

**tool call — Bash**
````
{
 "command": "T181_BASE=http://127.0.0.1:7941 .venv/bin/python -I artifacts/review-evidence/T-181-paralegal-r2/h.py artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r02.out 2>&1; echo exit $?; grep -v \"^\\[shot\\]\" artifacts/review-evidence/T-181-paralegal-r2/r02.out",
 "description": "Run Bates panel probe",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T22:54:04.308Z

**tool result**
````
exit 0
### run r02_bates.py at 16:54:00
PANEL (blank):
Exhibit and Bates numbers (optional)

One Bates number per record, not per page. Record 1 gets the first number you type, record 2 gets the next number, and so on in the order the records were read (9 records here). Use this only if each of your records is one Bates page in that order.

If your records are longer, or in a different order, leave these blank and fill in the page numbers in Word. Filled in, the numbers replace “[Ex. __ / Bates __]” in every source line of the letter, and the letter then cites those pages.

Exhibit
Bates prefix
First number
Save numbers

Nothing filled in: every source line keeps “[Ex. __ / Bates __]” for you to fill in.
PREVIEW after exhibit only: In your letter: record 1 reads [Ex. 3 / Bates __], record 2 reads [Ex. 3 / Bates __], and record 9 reads [Ex. 3 / Bates __].
PREVIEW after prefix: In your letter: record 1 reads [Ex. 3 / Bates RIVERA0001], record 2 reads [Ex. 3 / Bates RIVERA0002], and record 9 reads [Ex. 3 / Bates RIVERA0009].
PREVIEW after start 101: In your letter: record 1 reads [Ex. 3 / Bates RIVERA0101], record 2 reads [Ex. 3 / Bates RIVERA0102], and record 9 reads [Ex. 3 / Bates RIVERA0109].
cfg-error: 
LETTER: January 9, 2026 — Austin EMS run report
LETTER: Source [Ex. 3 / Bates RIVERA0101]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented
LETTER: January 9, 2026 — Central ER discharge summary
LETTER: Source [Ex. 3 / Bates RIVERA0102]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 m
LETTER: January 16, 2026 — Dr. Alvarez, primary care
LETTER: Source [Ex. 3 / Bates RIVERA0103]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
LETTER: January 23, 2026 — Capital PT, initial evaluation
LETTER: Source [Ex. 3 / Bates RIVERA0104]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
LETTER: February 20, 2026 — Capital PT, visit 8
LETTER: Pain 4/10, improving.
LETTER: Source [Ex. 3 / Bates RIVERA0105]: "Pain 4/10, improving."
LETTER: March 6, 2026 — Capital PT, visit 9
LETTER: Source [Ex. 3 / Bates RIVERA0106]: "Discharged from PT after two missed appointments. Pain 3/10."
LETTER: May 18, 2026 — Hill Country Pain Management, new patient
LETTER: Source [Ex. 3 / Bates RIVERA0107]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
LETTER: May 29, 2026 — Austin Imaging, cervical MRI
LETTER: Source [Ex. 3 / Bates RIVERA0108]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; c
LETTER: June 12, 2026 — Hill Country Pain Management, follow-up
LETTER: Source [Ex. 3 / Bates RIVERA0109]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision
LETTER: Source [Ex. 3 / Bates RIVERA0102]: "ER charges: $6,240."
LETTER: Source [Ex. 3 / Bates RIVERA0108]: "Charge: $2,150."
after reload has RIVERA0101: True
after reload PREVIEW: In your letter: record 1 reads [Ex. 3 / Bates RIVERA0101], record 2 reads [Ex. 3 / Bates RIVERA0102], and record 9 reads [Ex. 3 / Bates RIVERA0109].
after clearing: letter has [Ex. __ / Bates __]: True | PREVIEW: Nothing filled in: every source line keeps “[Ex. __ / Bates __]” for you to fill in.
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:54:08.656Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal && cat s14_lib_step3.py; grep -n \"statement\\|June 15\" s14.out | head -20",
 "description": "Read round-1 lib11 step 3 script"
}
````

### User / tool · 2026-11-02T22:54:08.812Z

**tool result**
````
import re
T0 = time.time()
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
cards = pg.query_selector_all("[data-testid=case-card]")
log("cards:", [c.get_attribute("data-title") for c in cards])
# open the lib11 case card's Continue
pg.click("[data-testid=case-card][data-title='Priors and ledger'] [data-testid=btn-continue]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
log("landed:", pg.url)
n = 0
for step in range(15):
    m = re.search(r"item=([^&]+)", pg.url)
    if not m:
        break
    iid = m.group(1)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    acts = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")
    marks = pg.evaluate("() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)")
    boxes = [(b.get_attribute("data-testid"), pg.evaluate("(e) => (e.closest('label') || e.parentElement).innerText", b)) for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
    yes = pg.query_selector("[data-testid=answer-yes]")
    log(f"######## {n} item={iid} | {' | '.join(title.split(' | ')[-4:])}")
    log("CARD:", right.replace("\n", " / "))
    log("ACT:", acts)
    log("MARKS:", marks, "| BOXES:", boxes, "| yes_disabled:", yes.is_disabled() if yes else None)
    shot(f"31-lib-s3-{n:02d}-{iid}")
    n += 1
    if boxes:
        pg.keyboard.press("a")  # should focus the first unticked box
        pg.wait_for_timeout(200)
        for _ in boxes:
            log("  focus:", pg.evaluate("() => document.activeElement.getAttribute('data-testid')"))
            pg.keyboard.press("Space")
            pg.wait_for_timeout(200)
            pg.keyboard.press("a")
            pg.wait_for_timeout(300)
            if re.search(r"item=" + re.escape(iid) + r"(&|$)", pg.url) is None:
                break
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
    log("  after:", pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").split("\n")[-2:], "| total chip:", pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")[-80:])
log("lib step3 took", round(time.time() - T0, 1), "s")
dump("lib step3 done")
shot("32-lib-step3-done", full=True)
11:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $250.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check disagreed with the first result for this item. / I read this amount against the highlighted words myself.
18:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $180.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check disagreed with the first result for this item. / I read this amount against the highlighted words myself.
25:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,310.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check disagreed with the first result for this item. / I read this amount against the highlighted words myself.
32:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,740.00 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check disagreed with the first result for this item. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
39:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $300.00 /  / Payment: money received, not a charge. /  / A second AI check disagreed with the first result for this item. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
46:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $274.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
52:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,166.00 /  / Balance or amount due: worked out from charges, payments and adjustments, not a charge. /  / A second AI check disagreed with the first result for this item. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
97:$250.00	Fennimoor Spine Clinic, itemized ledger	June 15, 2026	Change
98:$180.00	Fennimoor Spine Clinic, itemized ledger	June 15, 2026	Change
99:$2,310.00	Fennimoor Spine Clinic, itemized ledger	June 15, 2026	Change
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:54:09.803Z

Now the lib11 run on the local copy (port 7942), with a separate profile.

### Assistant · claude-opus-5-5 · 2026-11-02T22:54:24.999Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py",
 "content": "\"\"\"T-181 r2: lib11 (priors and ledger) on the local-mode copy. Step 2 disputed lines (grey box label, underlined outside words),\nStep 3 ledger lines (dispute direction, date column), Step 4 letter lines for the counted undated ledger amounts.\nRun: T181_BASE=http://127.0.0.1:7942 T181_PROFILE=profile-local .venv/bin/python -I .../h.py .../r03_lib11.py\n\"\"\"\nimport re\nT0 = time.time()\npg.goto(BASE + \"/new\")\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.click(\"[data-testid=tile-library]\")\npg.wait_for_timeout(300)\npg.check(\"[data-testid=library-case_lib11_priors_and_ledger]\")\npg.click(\"[data-testid=btn-read]\")\npg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)\npg.wait_for_timeout(300)\ndump(\"lib11 records\")\npg.click(\"[data-testid=btn-draft]\")\nfor i in range(80):\n    pg.wait_for_timeout(250)\n    if pg.query_selector(\"text=Go to step 2\") or \"/timeline\" in pg.url:\n        break\nlog(\"draft took\", round(time.time() - T0, 1), \"s\")\nif \"/timeline\" not in pg.url:\n    pg.get_by_text(\"Go to step 2\").first.click()\n    pg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.wait_for_timeout(500)\n\ndef iid():\n    m = re.search(r\"item=([^&]+)\", pg.url)\n    return m.group(1) if m else None\n\nn = 0\nfor step in range(40):\n    i = iid()\n    if not i or \"/timeline\" not in pg.url:\n        break\n    right = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }\")\n    marks = pg.evaluate(\"() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)\")\n    outs = pg.evaluate(\"() => Array.from(document.querySelectorAll('[data-testid=outside-word]')).map(m => m.innerText)\")\n    note = pg.evaluate(\"() => { const u = document.querySelector('[data-testid=outside-note]'); return u ? u.innerText : null }\")\n    unc = pg.evaluate(\"() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText.replace(/\\\\n/g, ' / ') : null }\")\n    yes = pg.query_selector(\"[data-testid=answer-yes]\")\n    yd = yes.is_disabled() if yes else None\n    cmp_box = pg.query_selector(\"[data-testid=check-compare]\")\n    log(f\"######## {n} item={i} yes_disabled={yd} compare_box={bool(cmp_box)}\")\n    log(\"CARD:\", right.replace(\"\\n\", \" / \"))\n    log(\"MARKS:\", marks)\n    log(\"OUTSIDE-WORDS:\", outs, \"| NOTE:\", note)\n    log(\"UNCOVERED:\", unc)\n    if cmp_box or yd:\n        shot(f\"lib-s2-{n:02d}-{i}\")\n    n += 1\n    if cmp_box:\n        pg.keyboard.press(\"a\"); pg.wait_for_timeout(200)\n        pg.keyboard.press(\"Space\"); pg.wait_for_timeout(200)\n        pg.keyboard.press(\"a\")\n    elif yd:\n        pg.keyboard.press(\"a\"); pg.wait_for_timeout(250)\n        log(\"  after A on refused: focus\", pg.evaluate(\"() => document.activeElement.getAttribute('data-testid') || document.activeElement.tagName\"),\n            \"| msg:\", pg.evaluate(\"() => (document.querySelector('.actions') || {innerText:''}).innerText\").replace(\"\\n\", \" | \")[-200:])\n        pg.keyboard.press(\"d\")\n    else:\n        pg.keyboard.press(\"a\")\n    pg.wait_for_timeout(450)\ndump(\"lib11 step 2 done\")\nshot(\"lib-step2-done\", full=True)\n\npg.click(\"[data-testid=btn-next-step]\")\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.wait_for_timeout(500)\nn = 0\nfor step in range(15):\n    i = iid()\n    if not i or \"/bills\" not in pg.url:\n        break\n    right = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }\")\n    boxes = [b.get_attribute(\"data-testid\") for b in pg.query_selector_all(\"input[type=checkbox]\") if b.is_visible()]\n    log(f\"######## bills {n} item={i} boxes={boxes}\")\n    log(\"CARD:\", right.replace(\"\\n\", \" / \"))\n    shot(f\"lib-s3-{n:02d}-{i}\")\n    n += 1\n    if boxes:\n        pg.keyboard.press(\"a\"); pg.wait_for_timeout(200)\n        for _ in boxes:\n            pg.keyboard.press(\"Space\"); pg.wait_for_timeout(200)\n            pg.keyboard.press(\"a\"); pg.wait_for_timeout(300)\n            if iid() != i:\n                break\n    else:\n        pg.keyboard.press(\"a\")\n    pg.wait_for_timeout(450)\ndump(\"lib11 step 3 done\")\nshot(\"lib-step3-done\", full=True)\n\npg.get_by_text(\"Go to step 4\").first.click()\npg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\npg.wait_for_timeout(600)\nwith pg.expect_download() as d:\n    pg.click(\"[data-testid=btn-download-letter]\")\nd.value.save_as(OUT + \"/lib11-letter.txt\")\nwith pg.expect_download() as d2:\n    pg.click(\"[data-testid=btn-download-notes]\")\nd2.value.save_as(OUT + \"/lib11-notes.txt\")\nshot(\"lib-step4\", full=True)\nlog(\"lib11 done in\", round(time.time() - T0, 1), \"s\")\n"
}
````

### User / tool · 2026-11-02T22:54:25.102Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:54:28.056Z

**tool call — Bash**
````
{
 "command": "T181_BASE=http://127.0.0.1:7942 T181_PROFILE=profile-local .venv/bin/python -I artifacts/review-evidence/T-181-paralegal-r2/h.py artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/r03.out 2>&1; echo exit $?; grep -n \"^######\\|^CARD\\|^OUTSIDE\\|^UNCOVERED\\|after A on\\|draft took\\|done in\\|ERRORS\\|Traceback\\|http \" artifacts/review-evidence/T-181-paralegal-r2/r03.out | cut -c1-900",
 "description": "Run lib11 probe on local copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T22:54:53.773Z

**tool result**
````
exit 0
67:draft took 2.6 s
68:######## 0 item=e1 yes_disabled=True compare_box=True
69:CARD: AI draft / March 4, 2026 · Dr. Hesper Alderton, primary care /  / Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. /  / Underlined words are not in the highlighted words. /  / A second AI check found this only partly supported by the highlighted words. Read it against the highlighted words before you say yes. / I read this line against the highlighted words myself.
71:OUTSIDE-WORDS: ['Annual', 'visit'] | NOTE: Underlined words are not in the highlighted words.
72:UNCOVERED: Also in this record, outside the highlighted words: / Annual visit. / Problem list: hypertension, type 2 diabetes, chronic low back pain. / Low back pain 3/10 today.
74:######## 1 item=f_cx1 yes_disabled=False compare_box=False
75:CARD: Warning for the attorney /  / The records disagree /  / Records differ on a fact /  / Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior accidents? Yes [ ] No [X].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
77:OUTSIDE-WORDS: [] | NOTE: None
78:UNCOVERED: Also in this record, outside the highlighted words: / Annual visit. / Problem list: hypertension, type 2 diabetes, chronic low back pain. / Low back pain 3/10 today. / Date of injury: 3/l8/26.
79:######## 2 item=f_cx2 yes_disabled=False compare_box=False
80:CARD: Warning for the attorney /  / The records disagree /  / Records differ on a fact /  / Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior injuries? Yes [ ] No IX].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
82:OUTSIDE-WORDS: [] | NOTE: None
83:UNCOVERED: Also in this record, outside the highlighted words: / Annual visit. / Problem list: hypertension, type 2 diabetes, chronic low back pain. / Low back pain 3/10 today. / Date of injury: 3/l8/26.
84:######## 3 item=f_r1_1 yes_disabled=False compare_box=False
85:CARD: Warning for the attorney / AI draft /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Dr. Hesper Alderton, primary care (March 4, 2026) mentions a prior or pre-existing condition: “Problem list: hypertension, type 2 diabetes, chronic low back pain.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
87:OUTSIDE-WORDS: [] | NOTE: None
88:UNCOVERED: Also in this record, outside the highlighted words: / Annual visit. / Low back pain 3/10 today.
89:######## 4 item=f_r1_2 yes_disabled=False compare_box=False
90:CARD: Warning for the attorney / AI draft /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Dr. Hesper Alderton, primary care (March 4, 2026) mentions a prior or pre-existing condition: “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
92:OUTSIDE-WORDS: [] | NOTE: None
93:UNCOVERED: Also in this record, outside the highlighted words: / Annual visit. / Problem list: hypertension, type 2 diabetes, chronic low back pain. / Low back pain 3/10 today.
94:######## 5 item=e2 yes_disabled=True compare_box=True
95:CARD: AI draft / March 18, 2026 · Ashgrove Fire-Rescue run report /  / Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED. /  / Underlined words are not in the highlighted words. /  / A second AI check found this only partly supported by the highlighted words. Read it against the highlighted words before you say yes. / I read this line against the highlighted words myself.
97:OUTSIDE-WORDS: ['Patient', 'after', 'passenger', 'vehicle', 'struck', 'from', 'behind'] | NOTE: Underlined words are not in the highlighted words.
98:UNCOVERED: Also in this record, outside the highlighted words: / Passenger vehicle struck from behind.
100:######## 6 item=f_r2_1 yes_disabled=False compare_box=False
101:CARD: Warning for the attorney / AI draft /  / Wording the other side could use /  / Scene facts recorded by Ashgrove Fire-Rescue run report (March 18, 2026): “Ambulatory at scene.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
103:OUTSIDE-WORDS: [] | NOTE: None
104:UNCOVERED: Also in this record, outside the highlighted words: / Passenger vehicle struck from behind.
105:######## 7 item=e3 yes_disabled=False compare_box=False
106:CARD: AI draft / March 18, 2026 · Wexcombe Memorial ED /  / Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
108:OUTSIDE-WORDS: [] | NOTE: None
109:UNCOVERED: None
110:######## 8 item=e4 yes_disabled=True compare_box=True
111:CARD: AI draft / March 26, 2026 · Pellingham and Rook PLLC, correspondence (letter of protection) /  / Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending. /  / Underlined words are not in the highlighted words. /  / A second AI check found this only partly supported by the highlighted words. Read it against the highlighted words before you say yes. / I read this line against the highlighted words myself.
113:OUTSIDE-WORDS: ['Law', 'letter', 'protection', 'Fennimoor', 'Spine', 'Clinic', 'states', 'clinic'] | NOTE: Underlined words are not in the highlighted words.
114:UNCOVERED: Also in this record, outside the highlighted words: / Letter of protection to Fennimoor Spine Clinic. / Please send complete records and an itemized statement.
116:######## 9 item=f_r4_1 yes_disabled=False compare_box=False
117:CARD: Warning for the attorney / AI draft /  / Wording the other side could use /  / Attorney referral /  / Referral wording in Pellingham and Rook PLLC, correspondence (letter of protection) (March 26, 2026): “Letter of protection to Fennimoor Spine Clinic.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
119:OUTSIDE-WORDS: [] | NOTE: None
120:UNCOVERED: Also in this record, outside the highlighted words: / Please send complete records and an itemized statement.
121:######## 10 item=e5 yes_disabled=False compare_box=False
122:CARD: AI draft / March 27, 2026 · Fennimoor Spine Clinic, new patient /  / Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
124:OUTSIDE-WORDS: [] | NOTE: None
125:UNCOVERED: Also in this record, outside the highlighted words: / Patient referred by attorney.
126:######## 11 item=f_r5_1 yes_disabled=False compare_box=False
127:CARD: Warning for the attorney / AI draft /  / Wording the other side could use /  / Attorney referral /  / Referral wording in Fennimoor Spine Clinic, new patient (March 27, 2026): “Patient referred by attorney.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
129:OUTSIDE-WORDS: [] | NOTE: None
130:UNCOVERED: None
131:######## 12 item=f_r5_2 yes_disabled=False compare_box=False
132:CARD: Warning for the attorney / AI draft /  / Wording the other side could use /  / Attorney referral /  / Referral wording in Fennimoor Spine Clinic, new patient (March 27, 2026): “Treating under a letter of protection.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
134:OUTSIDE-WORDS: [] | NOTE: None
135:UNCOVERED: Also in this record, outside the highlighted words: / Patient referred by attorney.
136:######## 13 item=e6 yes_disabled=False compare_box=False
137:CARD: AI draft / March 27, 2026 · Fennimoor Spine Clinic, new patient intake form (OCR text) /  / Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
139:OUTSIDE-WORDS: [] | NOTE: None
140:UNCOVERED: Also in this record, outside the highlighted words: / Date of injury: 3/l8/26.
141:######## 14 item=f_r6_1 yes_disabled=False compare_box=False
142:CARD: Warning for the attorney / AI draft /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026) mentions a prior or pre-existing condition: “Prior accidents?”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
144:OUTSIDE-WORDS: [] | NOTE: None
145:UNCOVERED: Also in this record, outside the highlighted words: / Date of injury: 3/l8/26.
146:######## 15 item=f_r6_2 yes_disabled=False compare_box=False
147:CARD: Warning for the attorney / AI draft /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026) mentions a prior or pre-existing condition: “Prior injuries?”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
149:OUTSIDE-WORDS: [] | NOTE: None
150:UNCOVERED: Also in this record, outside the highlighted words: / Date of injury: 3/l8/26.
151:######## 16 item=e7 yes_disabled=False compare_box=False
152:CARD: AI draft / April 24, 2026 · Fennimoor Spine Clinic, visit 8 /  / Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
154:OUTSIDE-WORDS: [] | NOTE: None
155:UNCOVERED: None
156:######## 17 item=f_gap_r7_r8 yes_disabled=False compare_box=False
157:CARD: Warning for the attorney /  / A break in treatment /  / Gap of 35 days between April 24, 2026 (Fennimoor Spine Clinic, visit 8) and May 29, 2026 (Fennimoor Spine Clinic, visit 14). /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
159:OUTSIDE-WORDS: [] | NOTE: None
160:UNCOVERED: None
161:######## 18 item=e8 yes_disabled=False compare_box=False
162:CARD: AI draft / May 29, 2026 · Fennimoor Spine Clinic, visit 14 /  / Neck pain 4/10, low back pain 5/10. Care continues. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
164:OUTSIDE-WORDS: [] | NOTE: None
165:UNCOVERED: None
166:######## 19 item=e9 yes_disabled=True compare_box=False
167:CARD: AI draft / June 15, 2026 · Fennimoor Spine Clinic, itemized ledger /  / Itemized ledger lists new patient exam charge $250.00, x-ray charge $180.00, treatment visits 1 through 14 charge $2,310.00, and total charges $2,740.00. /  / The line or highlighted words states a dollar amount, which goes only in the notes for the attorney, so this line is held out of the letter. Dismiss it, or pick highlighted words without the amount and edit the line to match. Its amounts were read but not totaled. You decide in step 3, Check the bills, whether to count them. Dismiss this line unless it states treatment.
169:OUTSIDE-WORDS: [] | NOTE: None
170:UNCOVERED: Also in this record, outside the highlighted words: / Account held under letter of protection.
172:  after A on refused: focus card-foot | msg:  words without the amount and edit the line to match. Its amounts were read but not totaled. You decide in step 3, Check the bills, whether to count them. Dismiss this line unless it states treatment.
173:######## 20 item=f_r9_1 yes_disabled=False compare_box=False
174:CARD: Warning for the attorney / AI draft /  / Wording the other side could use /  / Attorney referral /  / Referral wording in Fennimoor Spine Clinic, itemized ledger (June 15, 2026): “Account held under letter of protection.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.
176:OUTSIDE-WORDS: [] | NOTE: None
177:UNCOVERED: None
344:######## bills 0 item=a1 boxes=[]
345:CARD: Charge / Wexcombe Memorial ED · March 18, 2026 /  / $3,260.00 /  / Written in the record as $3,260. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
347:######## bills 1 item=a2 boxes=['check-separate', 'check-compare']
348:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $250.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this may be a billed charge, not what it was first sorted as. / I read this amount against the highlighted words myself.
350:######## bills 2 item=a3 boxes=['check-separate', 'check-compare']
351:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $180.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this may be a billed charge, not what it was first sorted as. / I read this amount against the highlighted words myself.
353:######## bills 3 item=a4 boxes=['check-separate', 'check-compare']
354:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,310.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this may be a billed charge, not what it was first sorted as. / I read this amount against the highlighted words myself.
356:######## bills 4 item=a5 boxes=['check-compare']
357:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,740.00 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
359:######## bills 5 item=a6 boxes=['check-compare']
360:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $300.00 /  / Payment: money received, not a charge. /  / A second AI check thought this may be an amount that is not a bill, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
362:######## bills 6 item=a7 boxes=[]
363:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $274.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
365:######## bills 7 item=a8 boxes=['check-compare']
366:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,166.00 /  / Balance or amount due: worked out from charges, payments and adjustments, not a charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
426:lib11 done in 25.2 s
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:03.699Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && sed -n 94,99p r03.out | cut -c1-600; sed -n 110,115p r03.out | cut -c1-600; echo ====; cat -n lib11-letter.txt; echo ====; grep -n -i \"ledger\\|statement\\|June 15\" lib11-notes.txt | cut -c1-400; grep -n \"June 15\\|no date\" r03.out | sed -n 1,40p | cut -c1-300 | grep -v \"^1[0-9][0-9]:CARD\"",
 "description": "Inspect lib11 marks, letter and ledger wording"
}
````

### User / tool · 2026-11-02T22:55:03.808Z

**tool result**
````
######## 5 item=e2 yes_disabled=True compare_box=True
CARD: AI draft / March 18, 2026 · Ashgrove Fire-Rescue run report /  / Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED. /  / Underlined words are not in the highlighted words. /  / A second AI check found this only partly supported by the highlighted words. Read it against the highlighted words before you say yes. / I read this line against the highlighted words myself.
MARKS: ['Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.']
OUTSIDE-WORDS: ['Patient', 'after', 'passenger', 'vehicle', 'struck', 'from', 'behind'] | NOTE: Underlined words are not in the highlighted words.
UNCOVERED: Also in this record, outside the highlighted words: / Passenger vehicle struck from behind.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/lib-s2-05-e2.png
######## 8 item=e4 yes_disabled=True compare_box=True
CARD: AI draft / March 26, 2026 · Pellingham and Rook PLLC, correspondence (letter of protection) /  / Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending. /  / Underlined words are not in the highlighted words. /  / A second AI check found this only partly supported by the highlighted words. Read it against the highlighted words before you say yes. / I read this line against the highlighted words myself.
MARKS: ['This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending.']
OUTSIDE-WORDS: ['Law', 'letter', 'protection', 'Fennimoor', 'Spine', 'Clinic', 'states', 'clinic'] | NOTE: Underlined words are not in the highlighted words.
UNCOVERED: Also in this record, outside the highlighted words: / Letter of protection to Fennimoor Spine Clinic. / Please send complete records and an itemized statement.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/lib-s2-08-e4.png
====
     1	TREATMENT CHRONOLOGY
     2	
     3	March 4, 2026 — Dr. Hesper Alderton, primary care
     4	Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
     5	Source [Ex. __ / Bates __]: "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
     6	
     7	March 18, 2026 — Ashgrove Fire-Rescue run report
     8	Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED.
     9	Source [Ex. __ / Bates __]: "Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."
    10	
    11	March 18, 2026 — Wexcombe Memorial ED
    12	Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture.
    13	Source [Ex. __ / Bates __]: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture."
    14	
    15	March 26, 2026 — Pellingham and Rook PLLC, correspondence (letter of protection)
    16	Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending.
    17	Source [Ex. __ / Bates __]: "This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending."
    18	
    19	March 27, 2026 — Fennimoor Spine Clinic, new patient
    20	Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.
    21	Source [Ex. __ / Bates __]: "Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."
    22	
    23	March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)
    24	Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7.
    25	Source [Ex. __ / Bates __]: "How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7."
    26	
    27	April 24, 2026 — Fennimoor Spine Clinic, visit 8
    28	Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
    29	Source [Ex. __ / Bates __]: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
    30	
    31	May 29, 2026 — Fennimoor Spine Clinic, visit 14
    32	Neck pain 4/10, low back pain 5/10. Care continues.
    33	Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."
    34	
    35	BILLED CHARGES
    36	
    37	Wexcombe Memorial ED, March 18, 2026: $3,260.00
    38	Source [Ex. __ / Bates __]: "ED charge: $3,260."
    39	Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00
    40	Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
    41	Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00
    42	Source [Ex. __ / Bates __]: "x-ray charge $180.00"
    43	Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $2,310.00
    44	Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"
    45	
    46	Billed charges accepted from these records: $6,000.00====
10:- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 2
24:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00." Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
25:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00." Not totaled ($300.00): Payment: money received, not a charge.
26:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
27:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00." Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
39:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — dismissed
58:June 15, 2026
348:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $250.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge f
351:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $180.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge f
354:CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,310.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge
357:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,740.00 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the
360:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $300.00 /  / Payment: money received, not a charge. /  / A second AI check thought this may be an amount that is not a bill, not what it was first sorted as. Read it against the highlighted words before you decid
363:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $274.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
366:CARD: Never counted / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $2,166.00 /  / Balance or amount due: worked out from charges, payments and adjustments, not a charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against 
406:$250.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
407:$180.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
408:$2,310.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:24.585Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && ls evals/library 2>/dev/null | grep lib11; grep -rln \"itemized ledger\" evals/ | head -5",
 "description": "Locate lib11 case source"
}
````

### User / tool · 2026-11-02T22:55:24.675Z

**tool result**
````
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
evals/library_build_v2.py
evals/letter_check.py
evals/golden/sample.export.expected.txt
evals/golden/check_golden.py
evals/library/case_lib11_priors_and_ledger.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:29.657Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && grep -n -B2 -A12 \"itemized ledger\" evals/library/case_lib11_priors_and_ledger.txt | head -30; grep -n \"_charge_line\\|def _charges\\|: \\${\\|amount_fmt\\|, {.*date\" app/backend/export.py | head -20",
 "description": "Read lib11 ledger record and export charge line code"
}
````

### User / tool · 2026-11-02T22:55:29.758Z

**tool result**
````
43-=== Record 9 ===
44-Date: 2026-06-15
45:Source: Fennimoor Spine Clinic, itemized ledger
46-Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
210:        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
339:            out += [f"{v.source(n)}, {_long_date(v.rec_date(n))}: {_money(a['cents'])}",
377:        span = f"{days} days, {_long_date(f.get('from_date'))} to {_long_date(f.get('to_date'))}"
706:    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:36.209Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && grep -n \"ERRORS\" -A8 r01.out r02.out r03.out | head -30; sed -n 335,342p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab/app/backend/export.py",
 "description": "Check console/http errors and export line"
}
````

### User / tool · 2026-11-02T22:55:36.298Z

**tool result**
````
    if charges:
        out += [CHARGES_TITLE, ""]
        for a in charges:
            n = a["record_no"]
            out += [f"{v.source(n)}, {_long_date(v.rec_date(n))}: {_money(a['cents'])}",
                    f'{v.source_prefix(n)}"{_amount_quote(v, a)}"']
        out += ["", TOTAL_PREFIX + _money(sum(a["cents"] for a in charges))]
    while out and out[-1] == "":
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:40.201Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && cat r01_counts.json; echo; ls *.png | wc -l",
 "description": "Show counts and screenshot count"
}
````

### User / tool · 2026-11-02T22:55:40.311Z

**tool result**
````
{"keys": 33, "clicks": 6, "to_letter_s": 16.9, "step2_items": ["e1", "f_accident_date_after_treatment_1_2_7", "e2", "e3", "f_r3_1", "e4", "f_cx1", "e5", "e6", "f_gap_r6_r7", "f_r6_1", "e7", "f_r7_1", "f_r7_2", "e8", "f_r8_1", "f_r8_2", "e9", "f_r9_1"]}
      52
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:41.046Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/lib-s2-05-e2.png"
}
````

### User / tool · 2026-11-02T22:55:41.055Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:43.306Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/08-bates-typed-preview.png"
}
````

### User / tool · 2026-11-02T22:55:43.315Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:45.918Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/09-bates-saved.png"
}
````

### User / tool · 2026-11-02T22:55:45.929Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:55:53.091Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && E2E_REQUIRE_DB=1 PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/e2e/guided tests/e2e/test_no_console_errors.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/pytest-guided.out 2>&1; tail -5 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/pytest-guided.out",
 "description": "Run guided e2e suite from the archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T22:58:47.684Z

**tool result**
````
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 173.39s (0:02:53)
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:58:52.848Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/s2-01-f_accident_date_after_treatment_1_2_7.png"
}
````

### User / tool · 2026-11-02T22:58:52.860Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:58:55.733Z

**tool call — Bash**
````
{
 "command": "kill 14948 15071; sleep 1; lsof -iTCP:7941 -sTCP:LISTEN -nP; echo \"lsof7941=$?\"; lsof -iTCP:7942 -sTCP:LISTEN -nP; echo \"lsof7942=$?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7941/api/health; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7942/api/health",
 "description": "Stop my two server PIDs and confirm closed"
}
````

### User / tool · 2026-11-02T22:58:56.997Z

**tool result (error)**
````
Exit code 7
lsof7941=1
lsof7942=1
000
000
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:59:17.922Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && grep -n \"outside the highlighted words:\\|Underlined words are not\\|One Bates number per record\" app/frontend/guided/step2.js app/frontend/guided/step4.js | cut -c1-120; grep -n \"AI_LINE_PREPARED = \\|an amount that is not a bill\\|may be a billed charge\" app/backend/export.py app/frontend/guided/*.js | cut -c1-160; grep -n \"Causation language\" app/backend/export.py | head -5; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py",
 "description": "Get line refs for cited code"
}
````

### User / tool · 2026-11-02T22:59:18.149Z

**tool result**
````
app/frontend/guided/step2.js:66:    return [h("div", { class: "also", "data-testid": "uncovered" }, h("b", {}, "Also in 
app/frontend/guided/step2.js:160:        need && outsideParts(item.summary, item.excerpt) ? h("p", { class: "muted out-n
app/frontend/guided/step4.js:159:        h("p", { "data-testid": "cfg-rule" }, h("b", {}, "One Bates number per record, 
app/frontend/guided/review.js:82:  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD
app/backend/export.py:39:AI_LINE_PREPARED = ("This chronology was built from answers the team prepared for this demo and checked by a second check; every item i
357:        return "Causation language"
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T22:59:22.499Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a9ab && sed -n 80,86p app/frontend/guided/review.js | cut -c1-400; sed -n 350,358p app/backend/export.py",
 "description": "Read dispute-direction map and flag label code"
}
````

### User / tool · 2026-11-02T22:59:22.592Z

**tool result**
````
  };
  /* An amount's second check names the way it disagreed (judge reason_code): say which way, so the tick is not a formality (paralegal review T-181 minor). */
  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "an amount that is not a bill" };
  R.disputeText = function (v, item) {
    const code = item && item.ladder && item.ladder.judge && item.ladder.judge.reason_code;
    if (v === "disagrees" && AMOUNT_WAY[code]) return `A second AI check thought this may be ${AMOUNT_WAY[code]}, not what it was first sorted as.`;
    if (v === "disagrees" && (code === "SHOULD_BE_UNCLEAR" || code === "TEXT_AMBIGUOUS")) return "A second AI check could not read this figure with confidence.";
    if t == "gap":
        return "Gap"
    if t == "conflict":
        return "Conflict, " + _CONFLICT_SUB.get(sub, (sub or "other").replace("_", " "))
    if t == "pre_existing":
        return "Prior condition"
    if t == "causation":
        return "Causation language"
    if t == "record_warning":
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:15.025Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/draft-T-181-paralegal-r2.md",
 "content": "# T-181 guided 4-step UI, round 2 (9ab8cae): paralegal re-review (Maria Delgado, senior PI paralegal)\n\n**Verdict: changes** (0 blockers, 1 major, 3 minors, 1 nit).\n\n**Scope.** `git archive 9ab8cae` was extracted to the session scratchpad and run with the fixture backend (curated set, no live calls):\n- Public demo mode (ZLAYT_MODE unset): port 7941, listener PID 14948.\n- Local copy for the lib11 library case: port 7942, PID 15071.\n- I stopped both by PID afterwards. `lsof` returned 1 on both ports and `curl` returned 000.\n\n**Deterministic check first.** From the archive, `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py` gave `127 passed in 173.39s` (pytest-guided.out).\n\n## Both round-1 majors are fixed\n\n1. **Disputed-line label: fixed.**\n   - The grey box now reads \"Also in this record, outside the highlighted words:\" (step2.js:66).\n   - Disputed lines underline the words that are not in the quote, with the caption \"Underlined words are not in the highlighted words.\"\n   - lib11 e1 underlines `Annual`, `visit`. e2 underlines `Patient`, `after`, `passenger`, `vehicle`, `struck`, `from`, `behind`. e4 underlines `Law`, `letter`, `protection`, `Fennimoor`, `Spine`, `Clinic`, `states`, `clinic` (r03.out, lib-s2-00-e1.png, lib-s2-05-e2.png, lib-s2-08-e4.png).\n   - This is exactly what I need in order to tick the compare box honestly.\n2. **Bates fill-in wording: fixed.**\n   - The panel now says \"One Bates number per record, not per page. ... Use this only if each of your records is one Bates page in that order.\" It also tells me to leave the fields blank and fill the cites in Word otherwise.\n   - A live preview showed \"record 1 reads [Ex. 3 / Bates RIVERA0101], record 2 reads [Ex. 3 / Bates RIVERA0102], and record 9 reads [Ex. 3 / Bates RIVERA0109]\". The saved letter matched it exactly (0101 to 0109; the ER charge is 0102 and the MRI charge is 0108).\n   - The numbers survived a reload, and clearing the fields restored `[Ex. __ / Bates __]` (r02.out, 08-bates-typed-preview.png, 09-bates-saved.png).\n\n## Sample case end to end, timed\n\nFrom Home, \"Open the sample case\" to the downloaded letter took **16.9 s scripted**: 33 key presses and 6 clicks, with drafting at 1.3 s (r01.out, r01_counts.json). At a human reading pace I still estimate 8 to 10 minutes.\n\nEvery Appendix A truth held:\n- 9 lines, with EMS and ER both on January 9.\n- The 73-day gap is flagged and the 28-day interval is not.\n- The 01-09 vs 01-19 conflict shows all three highlights on screen. The multi-record window fix works (s2-01-...png).\n- 12 planned PT visits vs discharge at visit 9.\n- Both prior-condition mentions are flagged.\n- The total is $6,240 + $2,150 = $8,390.00.\n- The $185 rate goes to the notes only. Lost work is listed under DAMAGES MENTIONS.\n\nMy edits and decisions held:\n- My record-3 edit is in the letter, and the original wording is under EDITED ITEMS.\n- The dismissed flag appears only under FLAGS DISMISSED.\n- A reload mid-review kept my place.\n- The copied letter matched the downloaded letter.\n- No console or HTTP errors in any run (the first-paint 404 is gone).\n\n## The undated-ledger letter line: yes, it is a problem for a demand letter (major)\n\nOn lib11 I counted the three ledger lines after ticking \"I checked this is a separate charge\". The letter's BILLED CHARGES section then reads:\n- `Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00`\n- `Source ...: \"New patient exam charge $250.00\"`\n\nThe ledger line for $180 and the line for $2,310 follow the same pattern (lib11-letter.txt:39-44).\n\nJune 15 is the *statement date*: the record says \"statement date 06/15/2026\". In the same section, `Wexcombe Memorial ED, March 18, 2026: $3,260.00` uses a date of service, so any reader takes June 15 as the date of service. The chronology above it puts the new-patient visit on March 27, 2026 (lib11-letter.txt:19).\n\nThe adjuster will say the exam was billed on a day with no treatment record, after the last visit on May 29. That is checklist item 1: a line dated by something other than the date of service. Step 3 now shows the right label (\"No date of service (statement dated June 15, 2026)\", r03.out:406-408), so the screen and the letter disagree.\n\nIt is backend text (app/backend/export.py:339). I am grading it on the letter this UI produces. I rated it minor in round 1, when it was bundled with the Step 3 table. On its own, the letter line is the half that goes to the adjuster, so it is major. The sample letter is not affected.\n\n## Round-1 minors\n\nThese are fixed:\n- The e9 refusal now points to Step 3.\n- A on a refused line leaves focus off \"No\".\n- lib11 provenance now follows the case (\"Demo: recorded AI answers\" with \"AI draft\" cards).\n- The Step 3 table shows the statement date correctly.\n- Step 3 disputes now name a direction.\n\nI did not re-exercise the public `/new` \"our test cases\" copy.\n\n```json\n{\"card\": \"T-181\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"git archive 9ab8cae (T-181 r2 fix) extracted to the session scratchpad; fixture backend, FIXTURE_SET=curated. Public demo mode (ZLAYT_MODE unset) at http://127.0.0.1:7941 (listener PID 14948); local copy (ZLAYT_MODE=local) at http://127.0.0.1:7942 (PID 15071) for library case lib11, since /api/library is local-only. Both stopped by PID; lsof exit 1 and curl 000 on both ports. Sample case: evals/golden/sample.txt via 'Open the sample case'. Library: case_lib11_priors_and_ledger. Viewport 1440x900. Evidence dir artifacts/review-evidence/T-181-paralegal-r2/.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, reviews/T-181-paralegal.md (round 1), the T-181 card notes and handoff, git diff 26287b9 9ab8cae for step2.js, step4.js and export.py\",\n  \"From the archive: E2E_REQUIRE_DB=1 pytest -q tests/e2e/guided tests/e2e/test_no_console_errors.py: '127 passed in 173.39s' (pytest-guided.out)\",\n  \"Sample case, timed, one Playwright run (r01_sample_e2e.py, r01.out): Home > Open the sample case > Draft the timeline (1.3 s) > all 19 Step 2 items with each card, highlight and outside-word list logged > E on record 3, retyped the line, Tab to Save, A focused the compare box, Space, A > reload after e5 > E on the gap flag with a note > D on the accident-date-source flag > Step 3: A on the 4 amounts (total chip $6,240.00 then $8,390.00) > Step 4 > Download letter at 16.9 s; Download notes; Copy letter (clipboard equals download)\",\n  \"Read letter-download.txt and notes-download.txt against Appendix A truths\",\n  \"Step 4 Bates panel (r02_bates.py, r02.out): read the panel text blank; typed Exhibit 3, prefix RIVERA, first number 101 and read the live preview after each; saved; compared letter cites to the preview; reloaded; cleared and saved (letter back to [Ex. __ / Bates __])\",\n  \"lib11 on the local copy (r03_lib11.py, r03.out): picked the test case, Read, Draft (2.6 s); all 21 Step 2 items with outside-word lists and grey-box text; compare confirm on e1, e2 and e4; A then D on the refused ledger line e9 (focus stayed on card-foot); Step 3 all 8 amounts, ticking 'separate charge' and compare on the three ledger lines; Step 4 letter and notes downloaded (lib11-letter.txt, lib11-notes.txt)\",\n  \"Read evals/library/case_lib11_priors_and_ledger.txt record 9 and app/backend/export.py:339 in the archive\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 4, \"keyboard_speed\": 4, \"charges_trust\": 4, \"compare_confirm_clarity\": 5, \"letter_usable\": 3, \"where_am_i\": 5},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Letter dates counted undated ledger charges by the statement date, in the same format as a date of service\",\n   \"evidence\": \"artifacts/review-evidence/T-181-paralegal-r2/lib11-letter.txt:39-44: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00' / 'Source [Ex. __ / Bates __]: \\\"New patient exam charge $250.00\\\"', and the same pattern for $180.00 and $2,310.00. Record 9 (evals/library/case_lib11_priors_and_ledger.txt:46) says 'Itemized ledger, statement date 06/15/2026'. The same letter dates the new-patient visit March 27, 2026 (lib11-letter.txt:19), and the ED charge line above uses a date of service ('Wexcombe Memorial ED, March 18, 2026: $3,260.00', line 37). Step 3 now labels these 'No date of service (statement dated June 15, 2026)' (r03.out:406-408), but the letter drops that label. Code: app/backend/export.py:339 prints v.rec_date(n) for every charge. The worker's handoff left this line on purpose.\",\n   \"why_it_matters\": \"The letter is what goes to the adjuster. A $250 new-patient exam dated June 15, after the last visit on May 29 and months after the March 27 exam in the same letter, is a date that matches no date of service. The adjuster will quote it back. That breaks checklist item 1 (nothing dated other than by date of service), and the screen and the letter now disagree.\",\n   \"fix\": \"In export.py, for a counted charge whose line states no date of service, print 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; no date of service stated): $250.00'. Keep the date-of-service format only for charges whose own line carries the date. This is backend-owned and can be split to its own card.\",\n   \"acceptance_test\": \"Export test on lib11 with a1-a4 counted: each ledger charge line contains 'statement dated June 15, 2026' and no charge line matches the bare pattern '<source>, June 15, 2026: $'; the ED line is unchanged.\"},\n  {\"severity\": \"minor\", \"title\": \"Step 3 dispute direction on the payment says 'may be an amount that is not a bill', which is what a payment already is\",\n   \"evidence\": \"r03.out:360 (lib11 a6): 'Payment: money received, not a charge. / A second AI check thought this may be an amount that is not a bill, not what it was first sorted as.' Source: app/frontend/guided/review.js:82 maps SHOULD_BE_DAMAGES to 'an amount that is not a bill'.\",\n   \"why_it_matters\": \"The direction was added so the tick is not a formality, but here it reads as agreement. I can't tell what the second check actually disputes (damages vs payment), so I'd tick on trust.\",\n   \"fix\": \"Map SHOULD_BE_DAMAGES to 'a damages figure (lost wages or similar), not a payment or bill' or name the first sort: 'thought this may be a damages figure rather than a payment'.\",\n   \"acceptance_test\": \"Guided e2e on lib11 a6: the compare-reason text names 'damages' and does not contain 'an amount that is not a bill'.\"},\n  {\"severity\": \"minor\", \"title\": \"Notes list the dismissed accident-date-source flag as 'Causation language' (pre-existing; missed in round 1)\",\n   \"evidence\": \"artifacts/review-evidence/T-181-paralegal-r2/notes-download.txt:13 '- Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) \\\"Date of accident per intake form: 2026-01-19.\\\"'. The screen called the same flag 'Where the accident date comes from / Accident date source' (r01.out:277). The round-1 notes have the same line (artifacts/review-evidence/T-181-paralegal/notes-download.txt:13). The label comes from app/backend/export.py:357 (type causation).\",\n   \"why_it_matters\": \"The attorney reads 'Causation language' over an accident-date quote and has to work out why. The screen and the notes name the same item differently.\",\n   \"fix\": \"Label flags in the notes with the same title the guided screen used (e.g. 'Accident date source'), or add a subtype label for accident-date-source causation flags.\",\n   \"acceptance_test\": \"Export test on the sample with f_r7_1 dismissed: FLAGS DISMISSED line starts 'Accident date source'.\"},\n  {\"severity\": \"minor\", \"title\": \"Notes opening line says every answer was checked by a second check, while my edited record-3 line was not\",\n   \"evidence\": \"notes-download.txt:3 'This chronology was built from answers the team prepared for this demo and checked by a second check; ...' versus notes-download.txt:39 '(accepted by the paralegal after comparing it with the quote; second check not available)'. Text from app/backend/export.py:39 (AI_LINE_PREPARED, T-177 D-069).\",\n   \"why_it_matters\": \"The notes are my record of how each line was verified. The opening sentence overstates it and repeats itself ('checked by a second check').\",\n   \"fix\": \"'...prepared for this demo; a second AI check read each prepared answer (lines you rewrote were compared by you, see EDITED ITEMS).'\",\n   \"acceptance_test\": \"Export test: AI_LINE_PREPARED does not contain 'checked by a second check'; with an edited item, line 3 does not claim every item was second-checked.\"},\n  {\"severity\": \"nit\", \"title\": \"Outside-word underline flags 'Patient' where the quote says 'Pt'\",\n   \"evidence\": \"lib-s2-05-e2.png and r03.out: OUTSIDE-WORDS includes 'Patient'; the highlight reads 'Pt states neck and low back pain 7/10.'\",\n   \"why_it_matters\": \"Conservative and harmless, but one false mark per abbreviation trains me to skim the underlines.\",\n   \"fix\": \"Optional: treat a small list of chart abbreviations (Pt/patient, Dx/diagnosed, Rx/prescribed, C/O/complained) as matches in the word diff.\",\n   \"acceptance_test\": \"lib11 e2 underlines do not include 'Patient'.\"}\n ],\n \"whats_right\": [\n  \"Underlined outside words plus the 'outside the highlighted words' grey box make the D-066 compare tick an actual check.\",\n  \"Bates panel states the one-number-per-record rule and previews record 1, 2 and N; the saved letter matched the preview.\",\n  \"Sample case: every Appendix A truth, $8,390.00 total, $185 only in the notes, and edits/dismissals/reload all held.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T23:00:15.114Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/draft-T-181-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:23.640Z

**tool call — Bash**
````
{
 "command": "sed -n 46p evals/library/case_lib11_priors_and_ledger.txt | cut -c1-80; grep -c \"ERRORS\" artifacts/review-evidence/T-181-paralegal-r2/r01.out artifacts/review-evidence/T-181-paralegal-r2/r02.out artifacts/review-evidence/T-181-paralegal-r2/r03.out; ls artifacts/review-evidence/T-181-paralegal-r2/lib-s2-00-e1.png artifacts/review-evidence/T-181-paralegal-r2/lib-s2-08-e4.png artifacts/review-evidence/T-181-paralegal-r2/pytest-guided.out; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-181-paralegal-r2/draft-T-181-paralegal-r2.md",
 "description": "Verify cited paths and validate review JSON"
}
````

### User / tool · 2026-11-02T23:00:23.767Z

**tool result**
````
Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $2
artifacts/review-evidence/T-181-paralegal-r2/r01.out:0
artifacts/review-evidence/T-181-paralegal-r2/r02.out:0
artifacts/review-evidence/T-181-paralegal-r2/r03.out:0
artifacts/review-evidence/T-181-paralegal-r2/lib-s2-00-e1.png
artifacts/review-evidence/T-181-paralegal-r2/lib-s2-08-e4.png
artifacts/review-evidence/T-181-paralegal-r2/pytest-guided.out
json blocks: 1
verdict: changes | severities: ['major', 'minor', 'minor', 'minor', 'nit']
verdict rule expects: changes | matches: True
model: claude-opus-5-5 | card: T-181 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:25.782Z

**tool call — Bash**
````
{
 "command": "cp artifacts/review-evidence/T-181-paralegal-r2/draft-T-181-paralegal-r2.md reviews/T-181-paralegal-r2.md && python3 tools/board.py validate reviews/T-181-paralegal-r2.md",
 "description": "Publish review and validate with board"
}
````

### User / tool · 2026-11-02T23:00:25.920Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:26.515Z

Now I'll update memory.

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:34.496Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t181-r2-patterns.md",
 "content": "---\nname: t181-r2-patterns\ndescription: T-181 r2 (9ab8cae) paralegal re-review: changes; both r1 majors fixed (outside-word underline, Bates rule+preview); new major = letter dates counted undated ledger charges by statement date (export.py:339, backend)\nmetadata:\n  type: project\n---\n\nT-181 r2 review (reviews/T-181-paralegal-r2.md, commit 9ab8cae). Verdict: changes, with 1 major, 3 minors and 1 nit.\n\n**Fixed in r2**\n- The grey box now says \"outside the highlighted words\".\n- The `[data-testid=outside-word]` underlines and the `outside-note` caption show on disputed or edited lines.\n- The Bates panel has `cfg-rule` and a `cfg-preview`, and the letter matches the preview.\n- No first-paint 404 in demo mode.\n\n**Major (backend, export.py:339)**\n- When the paralegal counts undated ledger charges, the BILLED CHARGES line prints the statement date in the date-of-service format: \"itemized ledger, June 15, 2026: $250.00\".\n- Step 3 labels the same line \"No date of service (statement dated ...)\".\n- I raised this from minor (r1) to major because the letter is the half that goes to the adjuster.\n\n**Minors**\n- The SHOULD_BE_DAMAGES direction on a payment reads \"an amount that is not a bill\" (review.js:82).\n- The notes label the accident-date-source flag \"Causation language\" (export.py:357). This is pre-existing and I missed it in r1.\n- AI_LINE_PREPARED says \"checked by a second check\" even when an edited line was not second-checked.\n\n**Mechanics that worked**\n- h.py takes the T181_PROFILE env var, so the local and demo profiles stay separate.\n- One timed end-to-end script (r01_sample_e2e.py) loops by `item=` in the URL. The full sample run took 16.9 s scripted.\n- The guided e2e from the archive took about 3 min: 127 passed.\n\n**Why:** next round, check that the export line names the statement date. Check the Step 3 wording for the payment direction.\n**How to apply:** reuse the scripts in artifacts/review-evidence/T-181-paralegal-r2/. Related: [[t181-guided-ui-patterns]], [[reviewer-run-pitfalls-pass4]].\n"
}
````

### User / tool · 2026-11-02T23:00:34.589Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t181-r2-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:36.276Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [GATE-M2 r2 patterns]",
 "new_string": "- [T-181 r2 patterns](t181-r2-patterns.md) — 9ab8cae changes: r1 majors fixed; letter dates undated ledger charges by statement date (export.py:339)\n- [GATE-M2 r2 patterns]"
}
````

### User / tool · 2026-11-02T23:00:36.421Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:00:40.234Z

Verdict **changes** (1 major, 3 minors, 1 nit): both round-1 majors are fixed — disputed lines now underline the words not in the quote, and the Bates panel states the one-number-per-record rule with a preview the saved letter matched; the sample case still meets every Appendix A item, Open-sample to downloaded letter took 16.9 s scripted, and the guided e2e suite from the archive passed (127).
Major: the undated-ledger line is a demand-letter problem — counted lib11 charges print as `itemized ledger, June 15, 2026: $250.00`, giving the statement date as if it were the service date and contradicting the same letter's March 27 visit (backend `export.py:339`; can be split to its own card); review at /Users/arsis/zlayt-pm-project/reviews/T-181-paralegal-r2.md, screenshots in /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2/, both my servers (PIDs 14948 and 15071) stopped.
