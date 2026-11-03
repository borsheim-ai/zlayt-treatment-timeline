# Subagent: Full-stack: T-179 gate UI round (Full-stack: T-179 gate UI round)

Source: `agent-a5f92561429208252.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T20:26:36.800Z

You are a frontend worker in /Users/arsis/zlayt-pm-project on T-179 (P0, M3 gate). Claim it with `python3 tools/board.py claim T-179 --agent frontend`. For D-066 only, you may also make the small review.py enforcement change in the backend.

Read:
- D-066 and D-067 in memory/ORCHESTRATOR_DECISIONS.md;
- reviews/GATE-M3-product-manager.md, GATE-M3-paralegal.md, GATE-M3-ux-designer.md and GATE-M3-accessibility.md.

**Build:**
1. **D-066.** Accepting an item whose judge verdict is disagree, unsupported or partially, or that carries JUDGE_DISAGREES, requires the "I compared it with the quote" confirm:
   - the backend returns 422 without it and stores it on the review event;
   - batch accept excludes such items;
   - the UI asks for the compare first, by mouse and by keyboard.
2. **D-067.** No page offers the drafted treatment paragraph, and the narrative never reaches the letter.
3. **UX and accessibility minors:**
   - an h1 on the case page;
   - the restored Undo row and its focus are never hidden under the sticky header;
   - Try again keeps focus;
   - the dismiss announcement is not overwritten;
   - a refused edit names the words to keep;
   - at 320px: Theme and Shortcuts are reachable, and the section nav doesn't clip Export.

**Constraints.** T-177 is in the badge, tags, trace and audit for provenance; T-178 is in pipeline.py, store.py and the review write path. Coordinate by keeping your review.py change minimal, and commit via a temp index. Never run `git checkout` on files.

**Tests and finish.**
- Write tests first: unit and e2e for D-066, and axe checks.
- Verify only from a `git archive HEAD` copy on your own port with E2E_REQUIRE_DB=1.
- Write the handoff, move the card to in_review, and restart the shared app.

Reply in 2 lines.

### User / tool · 2026-11-02T20:26:36.805Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:39.329Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-179 --agent frontend; python3 tools/board.py show T-179 | head -80; grep -n \"D-066\\|D-067\" memory/ORCHESTRATOR_DECISIONS.md | head"
}
````

### User / tool · 2026-11-02T20:26:39.534Z

**tool result**
````
T-179 claimed by frontend
---
id: "T-179"
title: "GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:26:28Z"
updated_at: "2026-11-02T20:26:39Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T20:26:39Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "accepting a disputed item without the confirm is 422 and the UI asks for the compare first (e2e, unit); no narrative control on any page and no narrative in the letter; each listed minor fixed with an e2e or axe check; axe 0 serious/critical and the h1 violation gone", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:26:30Z orchestrator: assigned: frontend
- 2026-11-02T20:26:39Z frontend: claimed

## Handoff (filled when moving to in_review)

74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75:| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:40.032Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/MEMORY.md"
}
````

### User / tool · 2026-11-02T20:26:40.050Z

**tool result**
````
1	- [T-043 panels conventions](project_t043_panels.md) — plug-in hooks, testid pitfalls, dev harness
2	- [Office 3D phone conventions](project_office3d_phone.md) — touch ownership, fit-to-box camera, kanban sheet, pitfalls
3	- [Stepper and AI-check panel](project_stepper_panels.md) — T-081/T-082 hooks, data-item-id pitfall, own-instance recipe
4	- [Side-by-side viewer](project_sidebyside.md) — T-046 pane hooks, sticky offset, test-id choices
5	- [Code-check refusals](project_code_check_refusals.md) — T-104 hooks: Change the quote, inline edit refusal, Why lead, picker pitfall
6	- [Suggestions and confidence](project_suggestions.md) — T-096 ZL.sg hooks, null-append pitfall, test recipe
7	- [T-060 enterprise polish](project_t060_polish.md) — tokens, keyboard scope, compact rows, one open-item definition and same-list focus advance (r5), test recipe, pitfalls
8	- [T-136 edit_to_check](project_t136_edit_to_check.md) — server flag, a-key prompt, Dismissed groups, ZLAYT_DB test recipe, open F1 residuals
9	- [Multi-case UI, conflicts skipped, held quote](project_multicase.md) — T-149/T-151/T-136 r3 hooks, routing, test recipe, pitfalls
10	- [Uncovered sentences list](project_uncovered.md) — T-144 hooks, refresh rule, lib09 test pitfalls
11	- [Verify from git archive](feedback_verify_from_archive.md) — temp-index commit recipe, no-console-errors test, confirm-dialog Escape race
12	- [T-166 MVP polish](project_t166_mvp_polish.md) — one-row header, More actions, dismiss ghost, a/n/x keys, discard confirm, reveal() in tests
13	- [T-174 MVP finish](project_t174_finish.md) — one first item, one count, section nav + --head-h, Back to review, preview discard, error actions, ghost focus
14	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:42.020Z

**tool call — Bash**
````
{
 "command": "for f in reviews/GATE-M3-product-manager.md reviews/GATE-M3-paralegal.md reviews/GATE-M3-ux-designer.md reviews/GATE-M3-accessibility.md; do echo \"=== $f\"; wc -c $f; done; cat .claude/agent-memory/frontend/feedback_verify_from_archive.md .claude/agent-memory/frontend/project_t174_finish.md"
}
````

### User / tool · 2026-11-02T20:26:42.121Z

**tool result**
````
=== reviews/GATE-M3-product-manager.md
   19564 reviews/GATE-M3-product-manager.md
=== reviews/GATE-M3-paralegal.md
   15833 reviews/GATE-M3-paralegal.md
=== reviews/GATE-M3-ux-designer.md
   18505 reviews/GATE-M3-ux-designer.md
=== reviews/GATE-M3-accessibility.md
   34224 reviews/GATE-M3-accessibility.md
---
name: verify-from-git-archive
description: Verify a frontend commit from a git archive of the commit tree, never the dirty tree; temp-index commit recipe and the confirm-dialog Escape race
metadata:
  type: feedback
---

Run e2e from `git archive <tree>` (tree from `GIT_INDEX_FILE=tmp git write-tree`) with `E2E_REQUIRE_DB=1`; a plain pytest there starts its own private server on a free port.

**Why:** T-154 r2 committed the a-key guard inside mountSection() (ReferenceError on every case load) while 12/12 passed on the dirty tree where other workers' hunks and the guard sat elsewhere. tests/e2e/test_no_console_errors.py now fails CI on any pageerror.

**How to apply:** build the commit with a temp index (`git read-tree HEAD`, `update-index --cacheinfo` for a file with others' hunks, `--add` for my own files); the check_stale_index hook blocks it if HEAD moved, so re-read-tree and recheck `git diff --stat OLD HEAD -- app/frontend tests/e2e`. The shared scratchpad has many dirs named arch/head0/etc; use a fresh name with mkdir -p.

Pitfall: ZL.confirmCharge (charges.js) must settle on the `cancel` event and ignore a stale `close` when the dialog is open again, else Escape then `a` is dropped (item still busy) or the reopened window is shut.
---
name: t174-mvp-finish
description: T-174 hooks and pitfalls: one first item (next_action), one count (progressOf + hitl), sticky section nav + --head-h, Back to review, preview discard, error actions, ghost focus
metadata:
  type: project
---
**One first item (F8):** the case overview box carries `data-do-first-item` (next_action). `RV.firstItemId()` reads it; `RV.focusFirstPending` (skip link, `n`, Start review fallback) calls `ZL.stepper.goto(id)` first, then falls back to the first decidable row.
**One count (F9):** `ZL.progressOf(c).needs` = server `hitl.needs_review_open` ONLY when the list summary matches the case on screen (same open total AND same `edits_to_check`), else counted from the case (state needs_review OR editToCheck). "Can export — N not reviewed" says `left` everywhere (`ZL.openLeft()` in the stepper, `p.left` in the case chip, `undecidedOf(s)` in the list), never the gate warning count (it leaves the edit to check out). The list filter is "Everything decided".
**Section nav (F13):** `sections.js` + `#section-nav` (index.html). Targets are headings: `#co-h`, `#h-timeline`, `#rv-flags-h`, `#rv-charges-h`, `#h-export`. Counts = undecided per section. `--head-h` (banner+header) is where the nav sticks; `--chrome-h` now includes the nav (app.js measureChrome, nav is observed). At <= 480 px "Overview" shows as "Top" so five buttons fit 360 px. `ZL.sections.back()` (Back to review, first control in Export) closes Export synchronously and `stepper.goto(lastItem)`.
**Preview (F14):** input.js `previewToken` = a sample preview not yet analyzed; a state subscriber deletes it when `s.token` changes (All cases, opening another case) and refreshes the list. `startRun` clears it.
**Errors (F15):** `showError(msg, {label, run})` renders `btn-error-action` inside `#input-error`; also overview open-error, export error, switcher msg, panel-error.
**Ghost focus (N3):** placeGhosts rebuilds the placeholder on every zl:panels; it refocuses the new Undo if focus was on one (tracked by a focusin listener, because the repaint may already have dropped focus to body). The old flake: spec measured before focus moved (one frame) and repaints lost it.
**Pitfalls:** `.cs > summary` never matched (summary is inside `.cs-details`): style `.cs-details > summary`. `appearance:none` on `select` removes its arrow: only on `input[type=search]`. The stub for "unrunnable paste" must route `**/api/cases/*/run` (the 409 is on run, not create). A gate that is blocked (nothing accepted) shows the notice, not the Export view: accept one item before testing Export/Can export chips. Another worker may have uncommitted hunks in charges.js: commit only yours.

**Round 2 (F15 demo paste, counted row, F14 reload):** input.js `demoRefusal()` (create AND run path) = plain sentence + `btn-error-action` "Open the sample" + `btn-error-library` (only when `#case-switcher` is visible, i.e. local mode; opens its details and focuses the first library button) + `error-live-note` (ENABLE_LIVE=1 line). Test it with a REAL non-sample paste: the e2e server is demo mode (no ENABLE_LIVE), so POST /api/cases itself returns 409 `demo_mode_unsupported_input`; never stub `/run` for this. charges.js `isOwnCount(a)` = kind charge + flag `separate_charge` -> neutral `charge-counted` line with chip `counted-by-you` (no chip--warn, no "flag" word; server `why` hidden once counted); Undo leaves a pending charge with the same flag -> `count-taken-back` chip (the real restore is backend card T-176). F14: input.js `pagehide` sends `DELETE` with `keepalive` for an un-analyzed preview and resets the hash; `pageshow` persisted reloads. Pitfall: the shared git index has others' staged deletions (sections.js shows `D` while the file exists): build commits and verification trees with a temp index (`/private/tmp/claude-501/scratch/f2/verify.sh`-style), never from the shared one.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:44.699Z

**tool call — Bash**
````
{
 "command": "sed -n 1,400p reviews/GATE-M3-ux-designer.md"
}
````

### User / tool · 2026-11-02T20:26:44.784Z

**tool result**
````
# GATE-M3 — ux-designer-reviewer (Priya Raman persona)

Model claude-opus-5-5. Date 2026-11-02. Baseline: reviews/MVP-ux-audit-r4.md (489f1bc, pass).

## Build and setup
- **Commit.** `git rev-parse --short HEAD` gave `d0b04bc`. `git merge-base --is-ancestor 489f1bc d0b04bc` gave `ancestor_ok`.
- **No app changes since r4.** `git diff --stat 489f1bc d0b04bc -- app` printed nothing. The 9 changed files are tests only.
- **Servers.** Both ran from a `git archive d0b04bc` copy in my scratchpad, each with its own scratch `ZLAYT_DB`.
  - 127.0.0.1:7991: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`. `/api/cases` returned `{"cases":[]}` at start.
  - 127.0.0.1:7992: the same, plus `LLM_FIXTURE_DIR` set to an empty directory. This gives a real model failure (fixture miss), not a stub.
  - I stopped both by PID (49978, 50285). Both ports then returned `000`.
- **Evidence.** `artifacts/review-evidence/gate-m3-ux/`: scripts `w0..w6*.py`, raw output `w*.out`, screenshots `NN-*.png`, and the exported letters as `.txt`.

## Deterministic check first
I ran `pytest tests/e2e/test_journey_modes.py tests/e2e/test_mvp_finish.py tests/e2e/test_adversarial_ui.py` from the archive copy. Each spec starts its own server. Result: `31 passed in 53.37s` (pytest-e2e.out).

## Verdict: **pass**
- 0 blockers, 0 majors, 8 minors, 3 nits.
- **Scores:** design quality 4, originality 3, craft 4, functionality 4.

## What I graded
**Hierarchy.**
- At 1440 the case top shows four things in order: one "Do this first" line, the needs-review and export-blocked chips, jump buttons with counts, then the timeline.
- Needs-review entries sort first. Each has an amber 3 px border, a "Needs review" chip and its one-sentence reason in the row. On lib11, e1, e2, e4 and e9 come before the verified rows.
- Verified rows use a grey border and a "Quote matches" chip. Unverified and verified are never styled alike.

**Review-not-trust affordances.**
- Every entry, flag and charge shows its verbatim excerpt inline, with the record label. Verifying an item takes 0 actions.
- Conflicts show each record's quote in the same card.
- The $185 rate sits under "Unclear — not totaled" with its reason.
- "Could not verify (2)" on lib11 is visible and says why each item was left out.
- The Why dialog lays out the validation ladder step by step.

**States.**
- **Empty input, 513,071 characters, and a refused paste.** Each shows a plain message beside the input with a next-step button. The text is kept every time (181 of 181 characters, 513,071 kept).
- **Model failure.** It keeps the 9 records and offers Try again.
- **Loading.** It shows a progress element and skeleton rows.
- **Overview.** Both the empty and the 17-case lists have counts, filters and per-case progress.

**Mobile.**
- At 390, scrollWidth equals 390 on every screen, in light and dark.
- Accept, Edit, Dismiss, Export, Copy and Analyze are 44 px tall.
- The sticky section nav reaches Timeline, Flags, Charges and Export in one tap.

**Export.**
- **Nothing accepted.** The export is blocked and says why.
- **Some items pending.** The letter shows only accepted items. The count line reads "4 entries, 0 charges in letter · … · 19 items pending (10 flags)". Copy and Download both ask "Copy the letter anyway?" with the pending counts.
- **Edits and dismissals.** An edited summary appears in its edited form. Dismissed entries are absent.
- **Pasted text.** The clipboard equals the letter. It has no HTML or UI labels, and each entry carries a `Source [Ex. __ / Bates __]` citation. A one-line layout is offered.

**Timing.**
- Keyboard-only sample journey, from the home screen to the letter: about 126 key presses and 0 pointer clicks, 52.6 s of script time.
- Mouse journey with "Accept all verified entries" and then per-item clicks: 18 clicks, 41.1 s.

## Findings (none blocks)
- **F1 minor.** After Undo on a dismissed entry, the restored row and its focused Accept button sit behind the sticky header (focus top 0, header bottom 124).
- **F2 minor.** An edit that drops "complained of" is refused with a message that names a category, not the words.
- **F3 minor.** The edit hint promises that the second AI check gates the letter. Under D-045(b) it does not.
- **F4 minor.** The model-failure notice says "finished items are saved" and, in the same box, that nothing was made.
- **F5 minor (opinion).** Every untouched case on the overview wears a red "✕ Export blocked (1)".
- **F6 minor, carried from r4 F1.** The counted-charge Why dialog still says "Flagged by the code" / "confirmed this flag".
- **F7 minor, carried from r4 F4.** The letter prints the ledger's statement date as the date of service.
- **F8 minor, carried.** The 73-day gap flag is at y 2,139 at 1440x900. A one-click "Show gap flag" at the top makes up for it. This improves on about 5,000 at bc12d44.
- **Nits.** "Starting……" shows a double ellipsis. At 390 the Export screen highlights "Charges" in the section nav. The refusal note names `ENABLE_LIVE=1`.

## r4 carry-overs at d0b04bc
- **F1 (Why wording).** Still present.
- **F3 (refusal off-screen).** Not reproduced: with 29 cases the box sat at y 748–850 of 900.
- **F4 (statement date).** Still present.
- **T-176 (Undo on a counted line).** The row now reads coherently: "Count taken back … Accept it to count this line again". No finding.

## What is right (keep)
- The excerpt is beside every entry, flag and charge. Needs-review items sort first with their reason in the row. Could-not-verify items have their own visible tray.
- The letter holds exactly the accepted set, including edits. The count line says what is in it. Copy and Download ask when items are pending. The pasted text is clean.
- Every error keeps her text or records, sits beside the input, and offers one next step, at both widths and in both themes.

```json
{"card": "GATE-M3", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive d0b04bc (HEAD d0b04bc; app unchanged since 489f1bc per git diff --stat 489f1bc d0b04bc -- app); app at 127.0.0.1:7991 (fixture curated, ZLAYT_MODE=local, scratch ZLAYT_DB) and 127.0.0.1:7992 (same, empty LLM_FIXTURE_DIR for a real model failure); sample case evals/golden/sample.txt and library case case_lib11_priors_and_ledger; 1440x900 and 390x844, light and dark",
 "exercised": [
  "pytest tests/e2e/test_journey_modes.py tests/e2e/test_mvp_finish.py tests/e2e/test_adversarial_ui.py from the archive copy: 31 passed in 53.37s",
  "w0: API inventory of the sample + 15 library cases (entry states, flag types, amounts, tray counts)",
  "w1, at 1440/390 x light/dark: empty overview; Analyze with empty input; 513,071-char paste; refused non-sample paste (case count 0 to 0, text kept); sample preview; loading (real /run and /status responses held 2.5 s); results top; model failure on :7992 (run_partial, 9 records kept, Try again)",
  "w2, at 1440/390 x light/dark: populated overview (17 cases); Start review / Do this first lands on a2 ($185, needs review); gap flag position and Show gap flag; flags panel; both conflict cards; charges + unclear tray; edit refused for a dropped qualifier; dismiss; accept; export with nothing accepted (blocked); all 23 decided; letter; Copy (clipboard == letter, no HTML)",
  "w3, at 1440 light and 390 dark: More > Why this status dialog; valid edit via Save and accept (original kept, Edited by you, in letter); dismiss then Undo; accept 3 then Export (count line, letter of 4, Copy anyway confirm)",
  "w4, at 1440/390 x light/dark: lib11 opened via Add a synthetic case (results in ~32 s, of which up to 15 s was my script waiting for an Analyze button the library flow does not show); needs-review rows first with reason and border colours; Could not verify tray (2 items); Count this charge on $250 with confirm; dismiss a gap flag",
  "w5, at 1440 light: keyboard-only sample journey from home to letter (0 pointer clicks, ~126 keys, 52.6 s script time); ? shortcuts dialog; j through all items (0 rows behind the sticky header); e edit, Esc; a then r undo; n/a/d through all; x Enter export; one-line layout; mouse journey with Accept all (18 clicks, 41.1 s)",
  "w6, at 1440 light: refusal position with 29 cases; counted-charge Why dialog wording; letter lines for counted $250/$180; Undo on a counted line",
  "read input.js (showError, demoRefusal, runningNode), review.js:527, review.py:336-364, trace.py:530-533, export.js:40-64; memory/ORCHESTRATOR_DECISIONS.md D-044, D-045, D-058",
  "stopped servers PID 49978 and 50285; both ports then returned 000"
 ],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "After Undo on a dismissed entry, the restored row and its focused Accept button are hidden behind the sticky header",
   "evidence": "w3.out 'AFTER UNDO e2: pending | focus {tid: btn-accept, item: e2, y: 0, h: 28}' at 1440 (sticky header bottom 124 per w5 sticky_bottom) and 'y: 0, h: 44' at 390; artifacts/review-evidence/gate-m3-ux/18b-undo-dismiss-light-1440.png and 18b-undo-dismiss-dark-390.png show neither e2 nor its focus. j/k stepping had 0 obscured rows (w5.out), so the problem is on the Undo path only",
   "why_it_matters": "She presses Undo in the Dismissed group, and the item jumps back up out of sight while focus goes under the header. She cannot see what she restored (visibility of system status; checklist 14). Accessibility severity (WCAG 2.4.11) is deferred to accessibility-reviewer.",
   "fix": "Give item rows scroll-margin-top equal to the sticky banner + header + section nav height, and scroll the restored row to the 'nearest' block after the reset.",
   "acceptance_test": "E2E at 1440x900 and 390x844: dismiss e2, press Undo in the Dismissed group; the e2 row's top and document.activeElement are both below the sticky nav's bottom edge and inside the viewport."},
  {"severity": "minor", "title": "An edit that drops 'complained of' is refused with a category, not the words to keep",
   "evidence": "artifacts/review-evidence/gate-m3-ux/17-after-edit-light-1440.png: 'The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.' The edit removed 'complained of' (quote 'C/O'). Source app/backend/review.py:336 (_QUALIFIER_WORDS self_report has no example) and :364. The number and word refusals at review.py:356-360 do quote the tokens. The edit hint app/frontend/review.js:527 lists only 'number, date and negation'",
   "why_it_matters": "Correction must be cheap. She is told something is missing but not what, so she must guess. Shortening a summary is the most common edit. NN/g: error messages should say precisely what is wrong.",
   "fix": "Quote the qualifier the code found and its summary form: 'The quote says “C/O” (complained of): keep “complained of” or “reports” in the summary.' Add 'hedges, approximations and whose account it is' to the edit hint.",
   "acceptance_test": "Edit sample e1 to drop 'complained of'; the refusal contains '“C/O”' and 'complained of'. The edit hint mentions whose account it is."},
  {"severity": "minor", "title": "The edit hint says the second AI check gates the letter, but an edited summary reaches the letter without it",
   "evidence": "app/frontend/review.js:527: 'When you save, the code checks every number, date and negation … then a second AI check reads it. Nothing is added to the letter until it passes.' After Save and accept the row says 'Compared by you with the quote. The second AI check did not run.' and the letter contains the edited text (w3.out 'partial letter has edited GOOD: True'). That behaviour is correct under D-045(b) (human-authored text is exempt from the judge); the copy is not",
   "why_it_matters": "The AI's role must be explained accurately where it acts (checklist 15). Calibrated trust breaks when the screen promises a check that does not gate the letter.",
   "fix": "'When you save, the code checks your wording against the quote; nothing is saved until it passes. A second AI check then reads it and may mark it for review.'",
   "acceptance_test": "Hint text has no 'until it passes' tied to the AI check, and matches the row copy after Save and accept when the judge did not run."},
  {"severity": "minor", "title": "The model-failure notice contradicts itself",
   "evidence": "artifacts/review-evidence/gate-m3-ux/08-model-failure-light-1440.png and 08-model-failure-dark-390.png: 'The analysis did not finish. Your records are kept and finished items are saved. The AI step failed for 20 items (finding the flags and the second check and writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9.' The static half is app/frontend/input.js:120. 'Try again' wraps to two lines at 1440",
   "why_it_matters": "Error states must be designed: one says items are saved, the next says nothing was made. The middle clause is in process words ('the second check'), not hers.",
   "fix": "When counts are zero, render 'Your 9 records are kept. Nothing was finished on this run.' and drop 'finished items are saved'; keep the server's record list; keep Try again on one line (white-space: nowrap).",
   "acceptance_test": "Fixture-miss sample run: run-error does not contain both 'finished items are saved' and 'No entry was made'; Try again is one line at 1440."},
  {"severity": "minor", "title": "Opinion, not a spec breach: every untouched case on the overview shows a red '✕ Export blocked (1)'",
   "evidence": "artifacts/review-evidence/gate-m3-ux/10-overview-cases-light-1440.png: 17 of 17 rows show the red chip with 'Nothing is accepted or edited yet, so the letter would be empty.'",
   "why_it_matters": "Red error styling for the normal starting state teaches her to ignore red. A case that is actually blocked (judge never ran, D-044) then looks the same as one she has not started.",
   "fix": "For the 'nothing accepted yet' reason, show a neutral 'Not started' chip; keep red '✕ Export blocked' for real blockers.",
   "acceptance_test": "Overview with a fresh case and a D-044-blocked case: only the second shows the red chip."},
  {"severity": "minor", "title": "Carried from r4 F1: the counted-charge Why dialog still says 'Flagged by the code' and 'confirmed this flag'",
   "evidence": "w6.out 'flag' words: 4 | 'Flagged by the code' present: True | 'confirmed this flag': True; artifacts/review-evidence/gate-m3-ux/51-counted-why-light-1440.png; app/backend/trace.py:530, :533",
   "why_it_matters": "The row reads 'Counted by you'. One click away, the same decision is called a code flag she confirmed.",
   "fix": "As r4: label the step 'Counted by you', with no 'flag' wording.",
   "acceptance_test": "After Count this charge, the Why dialog contains 'Counted by you' and no 'flag'."},
  {"severity": "minor", "title": "Carried from r4 F4: a counted ledger line prints the statement date as its date of service",
   "evidence": "w6.out letter lines: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00' and '… June 15, 2026: $180.00'; the row's own reason is 'The line states no date of service'",
   "why_it_matters": "The letter implies a date of service the record does not state (checklist 20).",
   "fix": "'itemized ledger (statement dated June 15, 2026; no service date stated): $250.00'.",
   "acceptance_test": "lib11 export with $250 counted contains 'statement dated' and no bare 'June 15, 2026: $250.00'."},
  {"severity": "minor", "title": "Carried (checklist 19): the 73-day gap flag is below the fold at 1440x900; a one-click link makes up for it",
   "evidence": "w2-light-1440.out 'GAP FLAG box at load (scroll 0): y 2139 … vh 900 | show-gap button: y 174'; one click on Show gap flag focuses it at y 387. Down from about 5,000 at bc12d44",
   "why_it_matters": "The most damaging fact in the sample is 2.4 screens down. The link is the accepted alternative but depends on her noticing a side-panel button.",
   "fix": "Put the gap flag (type and days) in the Case overview line beside 'Do this first'.",
   "acceptance_test": "At 1440x900, scroll 0, the text 'Gap of 73 days' is inside the viewport."},
  {"severity": "nit", "title": "Loading reads 'Starting……' (double ellipsis)",
   "evidence": "w1.out 'LOADING visible True stage: Starting……' at all four combos; artifacts/review-evidence/gate-m3-ux/06-loading-dark-1440.png; app/frontend/input.js:142 sets 'Starting…' and runningNode appends '…' when no step count",
   "why_it_matters": "Small craft slip on the first state after Analyze.",
   "fix": "Do not append the ellipsis when the label already ends with one.",
   "acceptance_test": "status-stage text right after Analyze is 'Starting…'."},
  {"severity": "nit", "title": "At 390 the Export screen highlights 'Charges' in the sticky section nav",
   "evidence": "artifacts/review-evidence/gate-m3-ux/22-export-letter-dark-390.png (Charges underlined, Export heading on screen); at 1440 22-export-letter-light-1440.png highlights Export correctly",
   "why_it_matters": "Wrong 'you are here' cue on the phone.",
   "fix": "Set the active tab from the view, not scroll position, when the Export view is open.",
   "acceptance_test": "At 390 on Export, the nav's aria-current item is Export."},
  {"severity": "nit", "title": "Carried from r4: the refusal note names an environment variable",
   "evidence": "w1.out refusal text '… start the app on your own computer with ENABLE_LIVE=1 and a model key.'; app/frontend/input.js:45",
   "why_it_matters": "Developer terms in her screen (checklist 18). Acceptable for a demo.",
   "fix": "Link to the README's Run live section instead.",
   "acceptance_test": "Refusal note has no 'ENABLE_LIVE'."}
 ],
 "whats_right": [
  "Every entry, flag and charge shows its verbatim excerpt inline with its record; needs-review items sort first with an amber border and the reason in the row; the Could not verify tray is visible.",
  "The letter holds exactly the accepted set (edits in, dismissed and pending out); the count line says what is in it; Copy and Download ask when items are pending; the pasted text is clean with citations.",
  "Empty, oversized, refused and model-failure states each keep her text or records, sit beside the input and offer one next step, with no sideways scroll at 390 in light or dark."
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:47.431Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p reviews/GATE-M3-accessibility.md | cut -c1-600"
}
````

### User / tool · 2026-11-02T20:26:47.517Z

**tool result**
````
# GATE-M3 accessibility review (WCAG 2.2 AA)

Reviewer: accessibility-reviewer (claude-sonnet-5-5). Date 2026-11-02. Review only; no product code changed.
Verdict: **pass**. 0 blockers, 0 majors, 9 minors, 6 nits. Every must-have action (accept, edit, dismiss, undo, count, export, copy, new case, rename, open case) is reachable and operable by keyboard alone, with no trap and visible focus. axe-core found 0 serious or critical violations in 50 scans. The minors are listed below with fixes.

## Scope and method

- Commit audited: `d0b04bc8274a10c8ae08fc55cd4f7693e17024b4` (`git rev-parse d0b04bc`), extracted with `git archive d0b04bc | tar -x` into a fresh scratchpad directory (not the working tree).
- Served on http://127.0.0.1:7931 (`ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, `ZLAYT_DB` in the scratchpad). Listener PID 52031 (`lsof -nP -t -iTCP:7931 -sTCP:LISTEN`), stopped by PID at the end of this run.
- axe-core 4.10.3, `axe.min.js` sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` (same file as passes 1 to 3). Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- Synthetic data only: the Appendix A sample (9 records, 23 items), library cases `case_lib11_priors_and_ledger` (ledger, Count this charge, unclear tray) and `case_lib06_lop_billed_vs_adjusted` (flagged-charge dialog, with the worker's own route stub), and a pasted copy of `evals/golden/sample.txt` typed by keyboard.
- Screen reader: not available. Announcements were checked by DOM inspection only (a MutationObserver on the live regions, `role`, text, node identity). I make no claim about what NVDA or VoiceOver say.
- Tab start point reset with `documentElement.focus()` before every walk (harness note).
- The tray in the brief is read as the "Unclear - not totaled" tray in Charges (`data-testid=unclear-tray`) and the could-not-verify tray; both exercised.
- Not exercised: the demo-mode refused-paste explanation (this server runs local mode, where a paste is accepted), 200% and 400% browser zoom (320 CSS px emulated by viewport instead), Windows forced-colors, PDF input, the excerpt editor and manual-entry forms.

## Deterministic checks first

Worker e2e files run from the `d0b04bc` copy against my server (`E2E_BASE_URL=http://127.0.0.1:7931`):

```
$ .venv/bin/python -m pytest tests/e2e/test_keyboard_mobile.py tests/e2e/test_polish_r3.py tests/e2e/test_count_charge.py -q -rs -p no:cacheprovider -x
..............................                                           [100%]
30 passed in 41.06s

$ .venv/bin/python -m pytest tests/e2e/test_mvp_finish.py tests/e2e/test_multicase.py -q -rf -p no:cacheprovider
FAILED tests/e2e/test_mvp_finish.py::test_a_paste_the_demo_does_not_run_is_explained_with_real_actions
FAILED tests/e2e/test_mvp_finish.py::test_the_refused_paste_offers_the_library_by_keyboard
FAILED tests/e2e/test_multicase.py::test_new_case_button_is_in_the_first_screen_and_puts_the_cursor_in_the_name_field
3 failed, 59 passed, 1 skipped in 150.41s (0:02:30)
```

The 3 failures are environment mismatches, not accessibility evidence: two test the demo-mode refused paste (my server is local mode) and one compares an aria snapshot of the overview with an empty case list (my DB held cases). I did not use them as evidence and did not investigate further. I tested the same behaviours by hand: New case moves focus to Case name (kb1/kb2 below).

## axe-core: 25 states x light and dark = 50 scans

`artifacts/review-evidence/GATE-M3-accessibility-audit-results.json`. Script `GATE-M3-accessibility-audit.py`.

States: overview empty, overview empty after Analyze with no text (error), overview with 2 cases, overview with a `status_error` row (route stub, as the worker's own e2e), case top, rename open, edit open, source dialog, row More open, Why dialog, audit drawer, Case checks and AI-check disclosures open, flags, charges, shortcut sheet, batch confirm, dismiss placeholder, export blocked, export, copy confirm (granted and not granted), Copy anyway blocked, side-by-side, lib11 charges with the unclear tray, Count this charge dialog. Each state was reached with fresh cases per theme so one theme's 

- Serious or critical: **0** in all 50 scans.
- Violations: `page-has-heading-one` (moderate, best-practice) in 32 scans (every case-view state, both themes). Nothing else.
- Needs-review ("incomplete"): `color-contrast` in 26 scans (dialogs, empty states, charges). My own computed contrast found 0 failures in the same scans, so these are not contrast failures.
- Computed contrast (own script, same scans): 29,684 visible text nodes checked, 0 below threshold; 204 form-control boundaries checked, 0 below 3:1. Progress track border 4.30:1 light and 4.73:1 dark against the card (the track fill itself is 1.15:1, but a numeric "n of m" label sits next to every bar, so the bar is not the only carrier).
- The flagged-charge dialog (worker's route stub on lib06) scanned separately in both themes: 0 violations (`GATE-M3-accessibility-kb7.json`).

## Keyboard-only job (no mouse, no click calls)

Scripts `GATE-M3-accessibility-kb1..kb12.py`, JSON next to them. The whole job completed:

1. Overview: Tab from the top reaches Theme, New case, 3 filters, Search, Sort, each case link, Case name, Records textarea, Analyze, Upload (label ring), Use the sample case, Add a synthetic case. The filters expose `aria-pressed` (true/false).
2. New case by keyboard: Enter on New case puts focus in "Case name"; typed a name; Tab to the Records textarea (visible label); inserted the sample; Tab to Analyze; Enter. The run finished and the case opened. Progress was announced as "9 records found", "Starting...", "Drafting summaries (step 2 of 8)".
3. Case: first Tab is the skip link "Skip to the first item to review"; all four skip hrefs resolve; Enter moves focus to the item named by "Do this first".
4. Accept by Enter on a charge ("Keep in notes: $185") announces "Accepted: $185. 22 left to review." and moves focus to the next needs-review row.
5. Dismiss by Enter leaves an Undo placeholder ("Dismissed: Austin EMS run report, January 9, 2026 Undo"); the button is named "Undo dismissing Austin EMS run report, January 9, 2026" (visible "Undo" is inside the name). One Shift+Tab reaches it. When the six seconds end with focus on that Undo, focus moves to the next row, not to the page body. The item stays in the open Dismissed (1) group with its own Undo.
6. Edit: Enter opens the textarea with focus; Tab runs Save and accept, Save, Cancel, Open record; Escape closes. No trap. Save announces "Saved edit to: ...". Undo on an edited item asks first (`role=group` "Confirm undo", Keep focused, Escape returns to Undo).
7. Rename: Rename this case, Enter, input named "Case name", Save returns focus to Rename. An empty name shows "Type a name for the case." as `role=alert` with focus kept in the input.
8. Section nav: `<nav aria-label="Sections of this case">`, buttons "Timeline, 9 items open" etc., `aria-current="location"` on the current one. It is `visibility: hidden` and 0 px tall at scrollY 0 (so it is not in the Tab walk from the top) and appears, tabbable, once scrolled (Tab from the header Export reaches "Overview"). Enter on Flags moves focus to the Flags heading with a 2 px ring; Enter on Export lands on "Why the export is blocked" or the Export heading.
9. Count this charge (lib11): 3 buttons named "Count this charge: $250.00", "...: $180.00", "...: $2,310.00" (visible "Count this charge" inside each). Enter opens a modal dialog labelled "Count this charge?" with focus on Cancel; Tab cycles Confirm, Cancel (browser chrome between, as with any showModal); Escape returns focus to the button; the named confirm ("I checked this is a separate charge for a service: count $250.00") announces "Counted $250.00 as a separate charge. Accepted charges now $250.00." and focus lands on the row. The flagged-charge dialog behaves the same ("Count this flagge
10. Export: Enter on Export puts focus on the Export heading with a 2 px ring (pass-3 nit P3-4 is fixed); the next Tab is "Back to review", then the letter-style radios, then Copy letter. Copy letter with unreviewed items shows `role=alert` text and focus moves to "Copy anyway"; Enter there copies, focus returns to Copy letter, `role=status` says "Copied the treatment section." and the clipboard holds "TREATMENT CHRONOLOGY". Back to review returns focus to the first entry. All cases returns to the overview with focus on the first case link; Enter on a case link opens it with focus on the case 
11. Dialogs (shortcut sheet, source record, Why, batch confirm by Shift+A, count, flagged charge): modal, labelled, Escape returns focus to the opener, no trap.

## Focus order and visible focus

`GATE-M3-accessibility-walk.json`, script `GATE-M3-accessibility-walk.py`. One full Tab cycle from the top of lib11 (12 flags, 8 amounts):

| Run | Stops | Entirely hidden (SC 2.4.11) | Partly hidden | No indicator | Unnamed | Min ring contrast |
|---|---|---|---|---|---|---|
| light 1280 | 213 | 0 | 0 | 0 | 0 | 5.51:1 |
| dark 1280 | 213 | 0 | 0 | 0 | 0 | 6.85:1 |
| light 320 | 205 | 0 | 1 ("Records differ on a fact", 6 of 9 sample points visible) | 0 | 0 | 5.55:1 |
| overview 1280 | 28 | 0 (the visually hidden file input; the "Upload .txt" label draws the ring: solid 2px rgb(11, 87, 208)) | 0 | 0 | 0 | 6.39:1 |

All rings are 2 px solid. The tab order follows the visual order.

## 320 CSS px reflow and target size

`GATE-M3-accessibility-reflow.json`, script `GATE-M3-accessibility-reflow.py`. At 320, 375 and 1280 across overview, case top (Case checks and AI-check disclosures opened first), row More open, edit, scrolled with the section nav showing, flags, charges, source dialog, export, lib11 charges and the Count dialog: `scrollWidth` equals the viewport in every state (no two-dimensional scroll). Visible controls checked 26 to 279 per state: 0 below 24 x 24 CSS px at 320, 375 and 1280. Two clipped items at 320 are listed as findings R-1 and R-2.

## Pass-3 items on this build
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:47.845Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"narrative\\|D-066\\|compare\\|disagree\\|batch\" reviews/GATE-M3-product-manager.md reviews/GATE-M3-paralegal.md | cut -c1-500 | head -50"
}
````

### User / tool · 2026-11-02T20:26:47.932Z

**tool result**
````
reviews/GATE-M3-paralegal.md:21:1. **Major.** The accepted "TREATMENT SUMMARY" paragraph goes into the letter with short cites only: `(Austin EMS run report, January 9, 2026)`. It has no verbatim quote and no `[Ex. __ / Bates __]`, which D-002 rules out ("No short-cite mode"). It also restates the chronology in different words ("Discharged from PT" vs "Discharged from physical therapy"), and an adjuster will compare the two.
reviews/GATE-M3-paralegal.md:38:  "Unit tests in the archive: pytest tests/unit -k 'export or letter or narrative' -> 276 passed (artifacts/review-evidence/GATE-M3-paralegal/unit-export.out.txt)",
reviews/GATE-M3-paralegal.md:41:  "p3: full keyboard review of 23 items (26 keys, 23.4 s): a on entries/flags/charges, e + Ctrl+Enter edit of record 3 summary, compare prompt via a+Enter, d on New-onset flag, reload at step 8 (7 of 23 persisted), ends 23 of 23 decided",
reviews/GATE-M3-paralegal.md:44:  "p6/p7: second sample case: batch accept verified entries, draft paragraph, accept $2,150 then dismiss entry 8, accept paragraph, export letter + notes with 13 pending items",
reviews/GATE-M3-paralegal.md:45:  "p8: lib08 added from the case overview 'Add a synthetic case' (1.3 s); compared to evals/library/case_lib08_second_crash_mri_after.txt and .expected.json",
reviews/GATE-M3-paralegal.md:47:  "Read personas/paralegal.md, CONTRACT M3 section, T-045 AC7, D-002, D-015, D-019, D-031, D-062, REQUIREMENTS non-goals, api.md narrative routes"
reviews/GATE-M3-paralegal.md:53:   "evidence": "artifacts/review-evidence/GATE-M3-paralegal/p7-letter.txt:35 'TREATMENT SUMMARY', :37 'On January 9, 2026, Austin EMS run report: Restrained driver rear-ended ... (Austin EMS run report, January 9, 2026)'; :42 'Discharged from PT after two missed appointments' vs chronology :24 'Discharged from physical therapy after two missed appointments'; tests/unit/test_narrative.py:120 asserts the '(Capital PT, visit 8, February 20, 2026)' form; memory/ORCHES
reviews/GATE-M3-paralegal.md:56:   "acceptance_test": "Unit + E2E: after narrative accept, every non-heading line of letter_text contains '[Ex. __ / Bates __]' or the configured Bates, and every TREATMENT SUMMARY sentence's entry excerpt appears verbatim in its line; test_narrative.py:120 updated."},
reviews/GATE-M3-paralegal.md:73:   "evidence": "p5-narrative.txt:7 'The model could not draft the paragraph after three tries.' and :15 'Draft written. Read each sentence before you accept it.'; p5-narrative.png; server.log 'llm call failed ... step=narrative'",
reviews/GATE-M3-product-manager.md:59:  "POST /narrative + /narrative/review accept on the sample; the letter then gains a 'TREATMENT SUMMARY' block (sample-narrative-structure.out)",
reviews/GATE-M3-product-manager.md:60:  "GET /items/e1/trace and /audit on the sample (sample-e1-trace.out): generator step says 'The AI read this record...' model claude-sonnet-5-5; audit counts 9 extract_v1 + 9 flags_v1 + 1 narrative_v1 calls as claude-sonnet-5-5",
reviews/GATE-M3-product-manager.md:71:   "evidence": "tests/fixtures/llm/curated/*.json (19 files, 9 extract + 9 flags + 1 narrative): CURATED 'hand-checked response written by qa from evals/golden ... Not a model output', recorded_from.model 'hand-checked (qa)'. app/frontend/app.js:13-14 badge 'Demo: recorded AI answers', tooltip 'This demo replays recorded AI answers for its sample cases.' 04-sample-top.png shows the badge and an 'AI draft' tag on every sample entry. sample-e1-trace.out: 'AI d
reviews/GATE-M3-product-manager.md:81:   "evidence": "memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues agai
reviews/GATE-M3-product-manager.md:86:   "evidence": "board.py show T-059: status blocked, AC3 'eval: 0 unsupported sentences across 3 runs on the sample (live backend)' done:false. grep -c narrative evals/run.py prints 0. After POST /narrative + accept, sample-narrative-structure.out shows the letter gains 'TREATMENT SUMMARY' (lines 38-48): 9 sentences 'On January 9, 2026, Austin EMS run report: <same summary> (<same citation>)', restating the chronology above it.",
reviews/GATE-M3-product-manager.md:88:   "fix": "Default it off (config flag) in the M3/M4 build until T-059 AC3 passes and evals.run reports a narrative unsupported count; or remove it and list it as a cut with the reason.",
reviews/GATE-M3-product-manager.md:89:   "acceptance_test": "With default config, GET /narrative returns 404 or the panel is absent (no btn-draft-narrative). With the flag on, the eval report has a narrative metric with a value."},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:50.646Z

**tool call — Bash**
````
{
 "command": "sed -n 80,400p reviews/GATE-M3-accessibility.md | cut -c1-900"
}
````

### User / tool · 2026-11-02T20:26:50.736Z

**tool result**
````
## Pass-3 items on this build

| Pass-3 id | Status now | Evidence |
|---|---|---|
| P3-1 More/Less name | fixed in substance | collapsed name "More actions: Austin EMS run report, January 9, 2026" contains the visible "More"; expanded "Less actions: ..." contains "Less" (`GATE-M3-accessibility-prior.json`). The name still changes with state (nit N-1) |
| P3-2 timeline `aria-labelledby` with no role | fixed | container is `role="group"` with `aria-labelledby="h-timeline"`; no `aria-prohibited-attr` in any of the 50 scans |
| N-8 Export-view skip hrefs | fixed | axe `skip-link` absent in export, copy-confirm and copy-blocked scans, both themes |
| P3-4 Export heading focus ring | fixed | ring 2 px solid on the heading |
| N-9 row Tab model | open (minor, F-1) | 9 of 9 rows `tabindex=0`; 213 stops |
| P3-5 decided Accept `aria-pressed` | open (nit N-2) | decided Accept: `aria-pressed="true"`, name "Accepted: ..." |
| N-12 two polite regions | open (nit N-3) | "Accepted: $185. 22 left to review." and "1 of 23 decided" both change |
| N-14 twelve "Technical details" | open (nit N-4) | `tech_details` count 12 |

## Findings

### Minor

**F-1 (carried N-9). Each timeline row is a Tab stop and holds 8 buttons.** One lib11 walk is 213 stops; a dismiss on a charge in the tray took 134 Tab presses from the entry above it (`GATE-M3-accessibility-kb3.json`). All actions stay reachable and the skip links and "Do this first" shortcut reduce the cost, hence minor.

**F-2. The case page has no level-one heading.** axe `page-has-heading-one` (moderate) in 32 of 50 scans. `h1.brand` "Treatment timeline" has `display: none` in the case view; the case name is a `<span>` (`h1_case`: `['Treatment timeline', 'none', 0]`, `case_name_markup`: SPAN). SC 1.3.1 and 2.4.6.

**F-3. The section nav "Overview" button shows "Top" under about 480 px but is named "Overview".** At 480, 375 and 320 px the visible text is "Top" and `aria-label` is "Overview" (`nav_overview_label_480`: `['Top', 'Overview', ...]`). SC 2.5.3 Label in Name (Level A): a voice-control user saying "click Top" gets nothing.

**F-4. The overview's j and k keys act when nothing has focus.** With focus on BODY, `j` moved focus to the first case link (`GATE-M3-accessibility-keys.json` `j_from_body` -> `('a','Sample case','cases-open')`). From a header button, a filter, the sort select and the search box they do nothing, so the gating is partial. In the case view the same keys do nothing from BODY (`GATE-M3-accessibility-keys2.json`, 11 keys, 0 changes). SC 2.1.4 and checklist item 8 want a shortcut active only when its component has focus, or a way to turn it off. Impact is small (focus moves; nothing is changed or opened), so minor; this is the one a stricter reader could call major.

**F-5. "Try again" on a status-error case row drops focus to the page.** Enter on `cases-status-retry` repainted the row; `document.activeElement` became BODY (`GATE-M3-accessibility-kb10.json` `after_retry_focus`). The whole-list "Try again" (`cases-retry`) moves focus to the Cases heading, so the two retries disagree. The announcement is only "Showing 14 of 14 cases". The button is named just "Try again" with no case name (`retry_name`: `[None, 'Try again', None]`). SC 2.4.3 and 4.1.2.

**F-6. A step-complete message overwrites "Dismissed: ..." 8 ms later in the same polite region.** Dismissing the last needs-review amount: `rv-live` text went '' (t=1933), "Dismissed: missing 3 days of work. 21 left to review." (t=1955), "Unclear amounts done. Next: Timeline, Austin EMS run report, January 9, 2026. 21 items are still open." (t=1963) (`GATE-M3-accessibility-kb4.json`). A screen reader may speak only the last message, so the user may not hear what was dismissed. DOM only; not checked in a screen reader. SC 4.1.3.

**F-7. At 320 px the Theme and Shortcuts controls are removed.** `display: none` at 640 px and below (`nav_overview_label_640`: Theme 'none', Shortcuts 'none'; `probe320`: both display none). A keyboard user at 400% zoom (320 CSS px) cannot open the shortcut sheet or switch theme; the review actions themselves are unaffected. SC 1.4.10 asks for no loss of functionality.

**F-8. At 320 px the case name is cut to "Sam..." / "Prior..." and the full name is not on screen.** `case-name` scrollWidth exceeds clientWidth at 320 (`nav_overview_label_320` last value true); the case heading is "Case overview" and carries the name only in its `aria-label`; the full name is only in a `title` tooltip (`case_name_markup`: title 'Sample case'). SC 1.4.10 (information loss). Screenshot `GATE-M3-accessibility-320-top.png`.

**F-9. The section nav clips its Export tab at 320 px with two-digit counts.** lib11: `button[nav-export] l=290 r=343` in a 320 px viewport; the strip scrolls sideways (`GATE-M3-accessibility-reflow.json`, `reflow lib11-charges|320`; screenshot `GATE-M3-accessibility-reflow-charges-320.png` shows "Exp"). Export is also in the header and the skip links, and keyboard focus scrolls the strip, so this is minor.

### Nit

**N-1.** The More toggle's name changes with state ("More actions: X" / "Less actions: X"). `aria-expanded` already carries the state; "Less actions" reads oddly.
**N-2 (carried P3-5).** A decided Accept keeps `aria-pressed="true"` while a second press does nothing.
**N-3 (carried N-12).** Two polite regions update on each decision (`rv-live` and `progress-text`).
**N-4 (carried N-14).** Twelve "Technical details" summaries share one name.
**N-5.** After Analyze finishes, focus goes to `nav#skip-nav` ("Skip links"), which has `outline: none` and 0 of 9 visible sample points (`GATE-M3-accessibility-kb2.json` step C; kb10 `focus_after_run`). A sighted keyboard user sees no focus until the next Tab.
**N-6.** Rename's empty-name error is `role=alert` but the input has no `aria-describedby` or `aria-invalid` (`rename_empty_error`). Also, during a case load the polite region repeats "Loading the case checks..." four times and "Loading the AI checks..." three times, and the first run message reads "Starting......" (`kb10 run_live_history`).

## Checks that passed

- Keyboard operability of every action in the journey; modal dialogs close with Escape and return focus; no trap anywhere (checklist 1, 2).
- Focus ring: 2 px solid everywhere, at least 5.51:1 (checklist 4); no focus entirely hidden by the sticky banner, header or nav at 1280 or 320 (checklist 5).
- Accept, dismiss, undo, count, edit, copy and batch each announce through `role=status` or `role=alert` (checklist 11); decided rows expose state by text and `aria-pressed` (checklist 10, 15).
- Names: New case ("New case"), Count this charge ("Count this charge: $250.00"), section nav ("Flags, 10 items open"), Undo placeholders ("Undo dismissing ..."), Try again ("Try again"), Rename ("Rename this case"), all dialogs labelled. Roles: filters are toggle buttons, the nav is `<nav>`, dialogs are modal `<dialog>`, `aria-current="location"` on the active section.
- Light and dark contrast, target size, 320 px reflow (apart from F-7 to F-9), reduced-motion not re-tested this gate.

## What is right

- Undo placeholders are real buttons with item-specific names, keep focus through a repaint, and fall back to the next row, never the page body, when they expire.
- Every modal dialog is labelled, opens on its safe answer, and returns focus to its opener on Escape; the Count and flagged-charge dialogs announce the result.
- Contrast, ring, target-size and reflow numbers held across 50 axe scans, 213-stop walks and 3 widths with the new overview, section nav and tray.

## Questions for Chris

- Should the overview's j and k keys also require focus inside the case list (F-4), or is body-level j/k on the overview intended?

```json
{"card": "GATE-M3", "persona": "accessibility-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git d0b04bc8274a10c8ae08fc55cd4f7693e17024b4 via git archive into the scratchpad (not the working tree); app http://127.0.0.1:7931 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated, DB in scratchpad); synthetic sample case (9 records, 23 items), library cases lib11 and lib06 (flagged-charge dialog via the worker's route stub); overview, case, tray, dialogs, export, section nav, Undo placeholders, Try again; demo-mode refused paste not exercised",
 "exercised": [
  "git rev-parse d0b04bc -> d0b04bc8274a10c8ae08fc55cd4f7693e17024b4; git archive d0b04bc | tar -x into a fresh scratchpad dir; server started with env -i ... ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated HOST=127.0.0.1 PORT=7931, listener PID 52031",
  "pytest tests/e2e/test_keyboard_mobile.py test_polish_r3.py test_count_charge.py against my server: 30 passed in 41.06s; test_mvp_finish.py + test_multicase.py: 59 passed, 3 failed, 1 skipped (the 3 failures are demo-mode and empty-DB environment mismatches with my local-mode populated server, not used as evidence)",
  "axe-core 4.10.3 (sha256 880970c0...) with wcag2a/aa/21a/21aa/22aa + best-practice on 25 states x light and dark = 50 scans (overview empty, empty error, overview with cases, status_error row stub, case top, rename, edit, source dialog, row More, Why dialog, audit drawer, disclosures open, flags, charges, shortcut sheet, batch confirm, dismiss placeholder, export blocked, export, copy confirm, Copy anyway blocked, side-by-side, lib11 charges + tray, Count dialog): 0 serious or critical; page-has-heading-one moderate in 32 scans (artifacts/review-evidence/GATE-M3-accessibility-audit-results.json)",
  "flagged-charge confirm dialog (lib06 with the worker's route stub) axe light and dark: 0 violations, keyboard path Accept -> Cancel focused -> Tab -> Confirm -> 'Accepted: $2,880. 18 left to review.' (GATE-M3-accessibility-kb7.json)",
  "computed contrast over 29,684 visible text nodes and 204 control boundaries in the 50 scans: 0 failing; progress track border 4.30 light and 4.73 dark (GATE-M3-accessibility-audit-results.json, GATE-M3-accessibility-prior.json)",
  "keyboard-only job: overview Tab walk, New case (focus to Case name), typed name and pasted sample by keyboard, Analyze by Enter, skip link, Accept, Dismiss, Undo placeholder (Shift+Tab to Undo, expiry while focused), Edit and Escape, Rename (save, empty error, Escape), section nav (hidden at scrollY 0, tabbable when scrolled; Enter and Space), Count this charge dialog, Export, Back to review, Copy letter, Copy anyway, All cases, open a case row (GATE-M3-accessibility-kb1..kb12.json)",
  "dialogs by keyboard: shortcut sheet, source record, Why, batch confirm (Shift+A), Count this charge, flagged charge, Undo-on-edited discard confirm: labelled, modal, Escape returns focus, no trap (kb6, kb7, kb12)",
  "full Tab walk from the top, lib11: 213 stops light 1280, 213 dark 1280, 205 light 320, 28 on the overview; 0 entirely hidden, 1 partly hidden at 320, min ring contrast 5.51 light and 6.85 dark, all 2 px solid (GATE-M3-accessibility-walk.json)",
  "320, 375 and 1280 px reflow and target size across overview, case top with disclosures open, row More, edit, scrolled nav, flags, charges, source dialog, export, lib11 charges and Count dialog: scrollWidth equals viewport everywhere, 0 controls under 24x24 (GATE-M3-accessibility-reflow.json)",
  "single-key shortcuts: overview j/k from body, header button, filter, sort, search, row link; case-view letters from BODY, nav, theme, all cases, rename, export (GATE-M3-accessibility-keys.json, keys2.json)",
  "live-region DOM history with a MutationObserver: Accept, Dismiss, last-in-step dismiss (two messages 8 ms apart), Count, flagged confirm, Copy letter/Copy anyway, run progress, status-error retry, load-error retry (kb2, kb4, kb6, kb9, kb10, kb11)",
  "names and states of the new controls: New case, Count this charge, section nav buttons and aria-current, Undo placeholders, Try again (row and list), filter aria-pressed, Rename input, More/Less toggles, decided Accept aria-pressed, timeline container role (kb1, kb3, kb5, kb6, prior.json)",
  "section nav label-in-name at 1280, 900, 640, 480, 375, 320 px and header Theme/Shortcuts display at each width (keys.json); h1 presence (keys.json h1_case)"],
 "verdict": "pass",
 "scores": {"keyboard_operability": 4, "focus_order_and_visibility": 5, "names_roles_states": 4, "status_announcements": 4, "contrast_light": 5, "contrast_dark": 5, "target_size": 5, "reflow_320": 4, "landmarks_headings": 3, "axe_serious_critical": 5},
 "findings": [
  {"severity": "minor", "title": "F-1 (carried N-9): each timeline row is a Tab stop followed by 8 buttons; 213 stops per page",
   "evidence": "GATE-M3-accessibility-walk.json lib11|light|1280 stops=213; prior.json row_tabindex [9, 9]; kb3.json 'tabs to tray Dismiss' 134 presses from the entry above",
   "why_it_matters": "APG composite pattern: a row that is both a stop and a container of stops gives a mixed model and a long walk. Every action stays reachable, and the skip links and Do this first shortcut cut the cost.",
   "fix": "Choose one model: roving tabindex across the rows with j and k as the arrows, or no row tab stop (buttons only).",
   "acceptance_test": "One documented Tab model; the Tab count from the first row to Export drops from the current value and every action stays reachable."},
  {"severity": "minor", "title": "F-2: the case page has no level-one heading (axe page-has-heading-one, 32 of 50 scans)",
   "evidence": "GATE-M3-accessibility-audit-results.json 10-case-top|light violations page-has-heading-one moderate, targets ['html']; keys.json h1_case [['Treatment timeline', 'none', 0, False]]; case_name_markup ['SPAN', 'Sample case', 'Sample case']",
   "why_it_matters": "SC 1.3.1 and 2.4.6: heading navigation in the case view starts at h2, and nothing names the page or the case as the top heading.",
   "fix": "Keep the h1 in the case view (visually hidden if the brand is hidden) or make the case name the h1.",
   "acceptance_test": "axe page-has-heading-one reports 0 in every case-view state; exactly one visible-to-AT h1 per view."},
  {"severity": "minor", "title": "F-3: section nav Overview button shows 'Top' under about 480 px but is named 'Overview' (SC 2.5.3)",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_480 ['Top', 'Overview', 'none', 'none', False]; the same at 375 and 320; nav-short span is aria-hidden in the markup",
   "why_it_matters": "Label in Name is Level A: voice control users say the visible word 'Top' and the button has no such name.",
   "fix": "Make the accessible name contain the visible text at every width (for example aria-label 'Top, Overview' or show 'Overview' and drop the short form).",
   "acceptance_test": "At 320, 375 and 1280 px, the accessible name of nav-overview contains its visible text."},
  {"severity": "minor", "title": "F-4: the overview's j and k keys act with nothing focused (SC 2.1.4)",
   "evidence": "GATE-M3-accessibility-keys.json j_from_body ('a', 'Sample case', 'cases-open'); j_from_new_case_btn, k_from_filter, j_from_sort, j_from_theme: no change; keys2.json: case view from BODY, 11 keys, 0 changes",
   "why_it_matters": "A single-character shortcut must be off-able, remappable or active only when its component has focus. j/k only move focus (no data change, no dialog), so this is minor, but it is the same class as pass-1 B1 and a stricter reader could rate it higher.",
   "fix": "Act on j/k only when focus is inside the case list, as the case view already does for item rows; or add a Keys on/off control.",
   "acceptance_test": "On the overview with focus on BODY, j and k change nothing; with focus on a case link they move to the next or previous link."},
  {"severity": "minor", "title": "F-5: Try again on a status-error row drops focus to the page, and its name does not say which case",
   "evidence": "GATE-M3-accessibility-kb10.json after_retry_focus {'tag': 'BODY'}; retry_name [None, 'Try again', None]; retry_live [['cases-count','status','Showing 14 of 14 cases']]. The list-level retry moves focus to the Cases heading (after_load_retry_focus h2 'Cases').",
   "why_it_matters": "SC 2.4.3: activating the control removes it and focus goes to the document. SC 4.1.2: two rows in error would expose two identical 'Try again' buttons.",
   "fix": "After the repaint, focus the retried row's link or its next control; name the button 'Try again: <case name>'.",
   "acceptance_test": "Enter on the row's Try again leaves focus on a control in that row or on the list; the button name includes the case name."},
  {"severity": "minor", "title": "F-6: the step-complete announcement replaces 'Dismissed: ...' within 8 ms in the same polite region",
   "evidence": "GATE-M3-accessibility-kb4.json live history: [1933, ''], [1955, 'Dismissed: missing 3 days of work. 21 left to review.'], [1963, 'Unclear amounts done. Next: Timeline, Austin EMS run report, January 9, 2026. 21 items are still open.']. DOM only; no screen reader.",
   "why_it_matters": "SC 4.1.3: a screen reader may speak only the last message, so the user may not hear what was dismissed.",
   "fix": "Write one combined message ('Dismissed: X. Unclear amounts done. Next: ...') or delay the second message until the first has been spoken.",
   "acceptance_test": "Dismissing the last needs-review item of a step produces one rv-live update that names the dismissed item and the next step."},
  {"severity": "minor", "title": "F-7: Theme and Shortcuts controls are removed at 640 px and below (loss of functionality at 320 px)",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_640 ['Overview','Overview','none','none',False] (columns 3 and 4 are Theme and Shortcuts display); probe320 output: btn-theme display none, btn-shortcuts display none; Tab walk at 320 has no Theme or Shortcuts stop (kb5.json w320 tab_walk_top)",
   "why_it_matters": "SC 1.4.10 expects content and functionality to survive reflow. A keyboard user at 400% zoom (320 CSS px) cannot open the shortcut sheet or change the theme. The review actions themselves are unaffected.",
   "fix": "Move both into an overflow menu or the Records disclosure at narrow widths instead of display: none.",
   "acceptance_test": "At 320 px, Theme and Shortcuts are reachable by Tab and operable."},
  {"severity": "minor", "title": "F-8: the case name is truncated at 320 px and the full name is not otherwise on screen",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_320 last value true (case-name scrollWidth > clientWidth); case_name_markup title 'Sample case'; screenshot artifacts/review-evidence/GATE-M3-accessibility-320-top.png shows 'Sam...'; reflow-charges-320.png shows 'Prior...'",
   "why_it_matters": "SC 1.4.10 information loss: a title attribute is not available to touch or keyboard users, and the heading 'Case overview' carries the name only in its aria-label.",
   "fix": "Let the name wrap on its own line at narrow widths, or show it in the case overview heading.",
   "acceptance_test": "At 320 px a 34-character case name is fully readable without hover."},
  {"severity": "minor", "title": "F-9: the section nav strip clips its Export tab at 320 px when counts are two digits",
   "evidence": "GATE-M3-accessibility-reflow.json reflow lib11-charges|320 offenders ['button[nav-export] l=290 r=343']; screenshot GATE-M3-accessibility-reflow-charges-320.png shows 'Exp' cut off; scrollWidth stays 320 because the strip scrolls inside itself",
   "why_it_matters": "SC 1.4.10: a sideways-scrolling strip is a second scroll direction. Export is also in the header and the skip links, and focus scrolls the strip, so minor.",
   "fix": "Wrap the nav at narrow widths, or shorten the labels so five tabs fit in 320 px.",
   "acceptance_test": "At 320 px with lib11 counts, all five nav buttons lie inside the viewport."},
  {"severity": "nit", "title": "N-1: the More toggle's name changes with its state ('More actions: X' / 'Less actions: X')",
   "evidence": "GATE-M3-accessibility-prior.json toggle_collapsed and toggle_expanded: ['entry-toggle','More actions: Austin EMS run report, January 9, 2026','More','false'] then 'Less actions: ...','Less','true'",
   "why_it_matters": "aria-expanded already carries the state; 'Less actions' reads oddly. The visible text is now inside the name, so SC 2.5.3 passes.",
   "fix": "Use one stable name such as 'More actions: X' with aria-expanded as the only state signal.",
   "acceptance_test": "The toggle's accessible name is identical collapsed and expanded."},
  {"severity": "nit", "title": "N-2 (carried P3-5): a decided Accept keeps aria-pressed='true' while a second press does nothing",
   "evidence": "GATE-M3-accessibility-prior.json decided_accept ['true', 'Accepted: Austin EMS run report, 2026-01-09', 'Accepted', 'Undo: Austin EMS run report, 2026-01-09']",
   "why_it_matters": "aria-pressed means a toggle; the way back is the separate Undo button.",
   "fix": "Drop aria-pressed on a decided Accept or make it a real toggle.",
   "acceptance_test": "A decided Accept has no aria-pressed or pressing it changes the value."},
  {"severity": "nit", "title": "N-3 (carried N-12): two polite regions change on each decision",
   "evidence": "GATE-M3-accessibility-kb2.json E2: rv-live 'Accepted: $185. 22 left to review.' and progress-text '1 of 23 decided · 2 to review' both role=status",
   "why_it_matters": "A screen reader may read both for one action.",
   "fix": "Keep one polite announcement per decision.",
   "acceptance_test": "One decision, one polite announcement."},
  {"severity": "nit", "title": "N-4 (carried N-14): twelve 'Technical details' summaries share one name",
   "evidence": "GATE-M3-accessibility-prior.json tech_details {'Technical details': 12, ...}",
   "why_it_matters": "SC 2.4.6 weak; each sits under its item.",
   "fix": "Name each with its item, or leave.",
   "acceptance_test": "Optional."},
  {"severity": "nit", "title": "N-5: after Analyze finishes, focus is on the invisible 'Skip links' nav with no focus indicator",
   "evidence": "GATE-M3-accessibility-kb2.json step C: tag nav, name 'Skip links', outlineStyle none, visible_points 0 (covered by #banner-synthetic); kb10.json focus_after_run: same",
   "why_it_matters": "The next Tab lands on the first skip link, which is the intent, but a sighted keyboard user sees no focus until then (SC 2.4.7 on a programmatic target).",
   "fix": "Move focus to the visible case heading, or show the skip links while the nav has focus.",
   "acceptance_test": "After Analyze, the focused element shows a 2 px ring or the skip links are visible."},
  {"severity": "nit", "title": "N-6: rename empty-name error is not tied to the input; run messages repeat and one reads 'Starting......'",
   "evidence": "GATE-M3-accessibility-kb9.json rename_empty_error {'text': 'Type a name for the case.', 'role': 'alert', 'inputDescribedby': None, 'invalid': None}; kb10.json run_live_history: 'Loading the case checks…' x4, 'Loading the AI checks…' x3, 'Starting……'",
   "why_it_matters": "SC 3.3.1 association is by role=alert and kept focus only; repeated polite text may be spoken more than once.",
   "fix": "Add aria-describedby and aria-invalid on the rename input; update the loading message once; fix the double ellipsis.",
   "acceptance_test": "The input references the error id; one loading message per phase."}
 ],
 "whats_right": [
  "Undo placeholders are real buttons named for their item, keep focus through a repaint, and fall back to the next row when they expire, never to the page body.",
  "Every modal dialog is labelled, opens on its safe answer and returns focus to its opener on Escape; the Count and flagged-charge dialogs announce the result.",
  "Contrast, focus ring, target size and 320 px reflow held across 50 axe scans (0 serious or critical), 213-stop walks and three widths with the new overview, section nav and unclear tray."
 ],
 "questions_for_chris": [
  "Should the overview's j and k keys also require focus inside the case list (F-4), or is body-level j/k on the overview intended?"
 ]}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:50.844Z

**tool call — Bash**
````
{
 "command": "sed -n 60,100p reviews/GATE-M3-product-manager.md | cut -c1-1500; git status --short | head -30; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T20:26:50.981Z

**tool result**
````
  "GET /items/e1/trace and /audit on the sample (sample-e1-trace.out): generator step says 'The AI read this record...' model claude-sonnet-5-5; audit counts 9 extract_v1 + 9 flags_v1 + 1 narrative_v1 calls as claude-sonnet-5-5",
  "curated_provenance.py: tests/fixtures/llm/curated has 19 files, each with CURATED 'hand-checked response written by qa ... Not a model output', recorded_from model 'hand-checked (qa)'",
  "In the d0b04bc copy: evals.run --check-spec exit 0; evals.letter_check value 0 over 25 cases; evals.run fixture (fixture-eval-d0b04bc.md: grounding 1.000, entry_recall 0.982, all flag P/R 1.000, hallucination 40/40, must_not 0; ship_bar False by design on fixture)",
  "evals.library_report regenerated at d0b04bc (library-d0b04bc.md); lib_missed.py lists missed must-flags for lib08/09/10/13/15",
  "git log 312efe6..d0b04bc -- app/llm/prompts app/llm/lexicon.yaml: empty (regression discipline holds); committed evals/reports/latest.json: 2026-11-02T14:39:59Z fixture ship_bar_met False",
  "board.py status/list/show: T-045 in_review; T-059, T-167 (P0), T-170 blocked; paralegal verify_quickly 4 in GATE-M2-r2 and T-149-r2"
 ],
 "verdict": "fail",
 "scores": {"solves_paralegal_job": 4, "no_over_claiming": 2, "scope_cut_honesty": 2, "decisions_defensible": 4, "ai_judgment_ship_bar": 3, "workflow_fit": 3},
 "findings": [
  {"severity": "blocker", "title": "The demo shows hand-written QA answers as AI output: badge, 'AI draft' tags, Why trace and audit all name the model",
   "evidence": "tests/fixtures/llm/curated/*.json (19 files, 9 extract + 9 flags + 1 narrative): CURATED 'hand-checked response written by qa from evals/golden ... Not a model output', recorded_from.model 'hand-checked (qa)'. app/frontend/app.js:13-14 badge 'Demo: recorded AI answers', tooltip 'This demo replays recorded AI answers for its sample cases.' 04-sample-top.png shows the badge and an 'AI draft' tag on every sample entry. sample-e1-trace.out: 'AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | model claude-sonnet-5-5'. /audit counts ('fixture','claude-sonnet-5-5','extract_v1') x9. D-029 (binding): 'the UI labels it cached demo (curated responses) ... honesty needs the label'; no decision supersedes it (T-166 F7 removed the wording as jargon)",
   "why_it_matters": "The public demo and the video are built on this sample. A panel that opens a fixture file will find that the output it saw labeled as the AI's was written by the team to match the golden file. The real model picks different excerpts (D-029 says so). This is the over-claim that ends trust, and the audit trail, which is a product feature, states something false.",
   "fix": "Put back an honest label in plain words, e.g. badge 'Demo: sample answers prepared by our team'; tooltip 'The AI's own answers on this case are in the eval report'. Curated items get a 'prepared answer' tag, not 'AI draft'. The trace step for a curated response reads 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'. The audit stores model 'hand-checked (qa)' from recorded_from. Alternatively, point the demo at the recorded live set and change the R-EX-6 byte test to structure only. Record whichever is chosen as a D-entry that amends D-029.",
   "acceptance_test": "E2E on FIXTURE_SET=curated: no element contains 'AI draft' or 'recorded AI answers' for a curated item; /items/e1/trace generator step evidence.model.id is not claude-sonnet-5-5 and its why names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'. With the recorded set, labels say AI."},
  {"severity": "major", "title": "Biggest product risk: a one-click Accept puts a summary the second check disputed into the carrier letter, and nobody is told which words are unsupported",
   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
   "why_it_matters": "Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.",
   "fix": "For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.",
   "acceptance_test": "lib11 e2 accept without confirm or edit returns 422 with a plain reason; with the confirm it is 200 and internal_notes_text names record 2 under the objection section; the new eval metric appears in the report."},
  {"severity": "major", "title": "The cut list and the spec no longer describe the product (R-CO-8 fails): 'cut' items are built, all four stretch items ship, and R-CH-7 is contradicted",
   "evidence": "memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues against PDF upload and the firm-voice paragraph; §5 non-goals 1, 2, 9-14, 16, 19 contradict the build. R-CH-7 (:84) says 'no path turns a rate, estimate or unreadable amount into a totaled charge', but SCOPE_CUTS 7g says 'Proposed'/'Quoted' charge lines are still countable (D-064). Appendix A: 'Stretch (pick at most one ...)'.",
   "why_it_matters": "Appendix A grades 'cut scope on purpose and tell us what you cut'. Right now the written reasons argue against features the panel will see working. That reads as either not knowing the product or not cutting at all. An estimate counted into 'Billed charges accepted' is a false statement in the letter that the spec still forbids.",
   "fix": "Rewrite SCOPE_CUTS as the current truth: one table with status cut / built (D-031/D-042) / held (D-063), each with its reason. Amend REQUIREMENTS §4/§5 and R-CH-3/R-CH-7 by ADR, or make 'Proposed'/'Quoted'/estimate lines not countable (class a). Get Chris's answer on presenting four stretch items (questions_for_chris) and write that reason into the note draft.",
   "acceptance_test": "Script: every REQUIREMENTS §5 non-goal maps to a SCOPE_CUTS row whose status matches the running app (route or testid present = built). R-CH-7 text agrees with count_charge.py; a 'Proposed charge $X' line is NOT_COUNTABLE, or the spec says why it is countable."},
  {"severity": "major", "title": "The draft paragraph (stretch, T-059 held with its eval unmet) is live and writes a second copy of the chronology into the letter",
   "evidence": "board.py show T-059: status blocked, AC3 'eval: 0 unsupported sentences across 3 runs on the sample (live backend)' done:false. grep -c narrative evals/run.py prints 0. After POST /narrative + accept, sample-narrative-structure.out shows the letter gains 'TREATMENT SUMMARY' (lines 38-48): 9 sentences 'On January 9, 2026, Austin EMS run report: <same summary> (<same citation>)', restating the chronology above it.",
   "why_it_matters": "This is an LLM output that reaches the carrier letter with no ship-bar number. It is the firm-voice stretch that REQUIREMENTS said 'would need its own verification', and it repeats the chronology without adding anything. It weakens the builder-mindset story and adds risk with no user value shown.",
   "fix": "Default it off (config flag) in the M3/M4 build until T-059 AC3 passes and evals.run reports a narrative unsupported count; or remove it and list it as a cut with the reason.",
   "acceptance_test": "With default config, GET /narrative returns 404 or the panel is absent (no btn-draft-narrative). With the flag on, the eval report has a narrative metric with a value."},
  {"severity": "major", "title": "The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale",
   "evidence": "library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).",
   "why_it_matters": "The product note will quote 'flag precision/recall 1.000'. Those numbers come from 10 cases written alongside the rules. Without the library number beside them, the claim goes beyond what the evidence supports, and the canonical pointer a panel opens says False.",
   "fix": "qa commits a library report regenerated at the gate commit and the live latest.json. The product note reports golden and library side by side, naming the conflict categories not covered (SCOPE_CUTS 13).",
   "acceptance_test": "evals/reports/library-latest.md source commit equals the gate tag; evals/reports/latest.json ship_bar_met True with backend claude-cli; the note draft cites both numbers."},
  {"severity": "minor", "title": "lib10: the internal notes drop the gap's paperwork caveat, and the flag is 'verified' although its start point is a claim form",
   "evidence": "journey-lib10.out notes: '- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 ...)'. The UI explanation adds 'looks like paperwork ... the gap would be 49 days'; the flag state is 'verified'. D-062 already identifies CMS-1500 as a billing header.",
   "why_it_matters": "The attorney reads the notes, not the UI. They show an understated gap with no warning.",
   "fix": "The notes line carries the same caveat and the 49-day alternative. An endpoint that looks like paperwork makes the gap needs_review.",
   "acceptance_test": "lib10 export notes contain '49 days' and 'paperwork'; f_gap_r8_r9 state is needs_review."},
  {"severity": "minor", "title": "A counted ledger line prints the statement date where every other line puts the date of service (UX F4, carried, no card)",
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
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/case_list.py
 M app/backend/ingest.py
 M app/backend/pdf_text.py
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
ee62967 docs(orchestrator): D-066 disputed accept needs a compare confirm; D-067 cut the drafted paragraph from the MVP UI; scope cuts 22-23
04ea2bf feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
d7ea327 test(qa): T-045 r2: real 375 px overflow check, rejected-item guard (unit + e2e), evals --record-latest points latest.json at the live run; fixture runs no longer replace a live latest.json
0c4284f docs(orchestrator): D-065 honest demo provenance (amends D-029)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:54.293Z

**tool call — Bash**
````
{
 "command": "git status --short app tests | head -40; wc -l app/frontend/*.js app/backend/review.py app/backend/api.py; grep -n \"confirm\\|compared\\|JUDGE_DISAGREES\\|edit_to_check\\|unconfirmed\" app/backend/review.py | head -80"
}
````

### User / tool · 2026-11-02T20:26:54.412Z

**tool result**
````
MM app/backend/api.py
MM app/backend/case_list.py
 M app/backend/ingest.py
 M app/backend/pdf_text.py
MM app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/store.py
MM app/backend/trace.py
MM app/frontend/api.js
MM app/frontend/app.js
MM app/frontend/audit.js
MM app/frontend/charges.js
MM app/frontend/export.js
MM app/frontend/flags.js
MM app/frontend/index.html
MM app/frontend/input.js
MM app/frontend/judges.js
MM app/frontend/overview.css
MM app/frontend/overview.js
MM app/frontend/review.css
MM app/frontend/review.js
D  app/frontend/sections.js
MM app/frontend/sidebyside.css
MM app/frontend/state.js
MM app/frontend/stepper.js
MM app/frontend/styles.css
MM app/frontend/suggestions.css
MM app/frontend/suggestions.js
MM app/frontend/switcher.js
MM app/frontend/timeline.js
MM app/frontend/tokens.css
MM app/frontend/uncovered.css
MM app/frontend/uncovered.js
MM app/llm/audited.py
MM app/llm/backends/fixture.py
MM tests/e2e/conftest.py
MM tests/e2e/test_charge_confirm.py
MM tests/e2e/test_code_check_refusal.py
D  tests/e2e/test_demo_provenance.py
MM tests/e2e/test_edit_to_check.py
      50 app/frontend/api.js
     162 app/frontend/app.js
      60 app/frontend/audit.js
     140 app/frontend/batch.js
     284 app/frontend/charges.js
      63 app/frontend/dom.js
      50 app/frontend/excerpt.js
      87 app/frontend/export.js
      51 app/frontend/exportcfg.js
     156 app/frontend/flags.js
     156 app/frontend/input.js
     223 app/frontend/judges.js
      93 app/frontend/manual.js
     218 app/frontend/mock.js
      29 app/frontend/mock_extra.js
      55 app/frontend/mock_flags.js
       2 app/frontend/mock_sample.js
      75 app/frontend/narrative.js
     401 app/frontend/overview.js
     652 app/frontend/review.js
      73 app/frontend/sections.js
     119 app/frontend/sidebyside.js
      37 app/frontend/source.js
      40 app/frontend/state.js
     696 app/frontend/stepper.js
     185 app/frontend/suggestions.js
      70 app/frontend/switcher.js
     373 app/frontend/timeline.js
      59 app/frontend/uncovered.js
     770 app/backend/review.py
     666 app/backend/api.py
    6095 total
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
6:invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
47:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
48:    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
49:    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
56:    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)
59:def _date_unconfirmed_error():
60:    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
83:def edit_unconfirmed(kind: str, item: dict) -> bool:
85:    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
199:def confirm_error(item_id: str, item: dict, confirm):
200:    """D-059: a charge that carries a likely_duplicate or likely_total flag is accepted only when the call names that flag (`confirm`). A 422 CONFIRM_REQUIRED
202:    f = (item.get("ladder") or {}).get("confirm")
203:    if item.get("kind") != "charge" or not f or confirm == f["confirm_with"]:
205:    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
206:              "message": f["message"],      # T-159: the flag's own sentence, without the "confirm by name" tail, so a client never strips the token out of the error message
208:    wrong = "" if confirm is None else " The confirm you sent does not name this flag."
209:    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")
212:def confirmed_accept(item: dict) -> bool:
213:    """T-159: a charge that is accepted and whose flag has been confirmed by name. A repeat accept of it changes nothing, so it writes nothing."""
214:    f = (item.get("ladder") or {}).get("confirm")
215:    return item.get("kind") == "charge" and bool(f) and bool(f.get("confirmed_at")) and item.get("review_status") == "accepted"      # item["kind"] = the amount's class
218:def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
219:    """The named confirm is kept on the item (ladder.confirm.confirmed_at) and in the accept event that carried it (after.confirm = {flag, name, confirmed_at}),
220:    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059). Both writes are ONE transaction: a failure on either leaves neither."""
221:    f = (item.get("ladder") or {}).get("confirm")
223:        stamp = {"flag": f["flag"], "name": f["name"], "confirmed_at": store.iso(t)}
226:            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
230:                conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
237:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
253:        if confirmed_accept(item):
254:            return item                                     # T-159: already accepted with its flag confirmed; a repeat accept writes no second decision
255:        err = confirm_error(item_id, item, confirm)         # D-059
261:            _record_confirm(conn, case_id, item_id, item, now)
263:            back = {"pending": "reset", "dismissed": "dismiss"}.get(item.get("review_status"))      # T-159 r2: take the accept back, so no charge counts without its confirm on record
282:    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
283:        raise _date_unconfirmed_error()
286:        confirm = body.get("confirm")
287:        if confirm is not None and not isinstance(confirm, str):
288:            raise _bad("The confirm must be the name of the flag.")
289:        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
312:    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
314:    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
348:    cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
463:    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
490:# ---------------------------------------------------------------- confirm_date
491:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
498:        raise _bad("Only a record whose date can be read two ways can be confirmed.")
501:    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
520:    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
523:    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
526:            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
530:    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
533:    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
544:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
549:                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
588:        return f"A gap of {ch['old_days']} days no longer applies after you confirmed the date of record {seq}."
590:        return f"A gap of {ch['new_days']} days now applies after you confirmed the date of record {seq}."
591:    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:58.501Z

**tool call — Bash**
````
{
 "command": "sed -n 1,20p app/backend/review.py; sed -n 76,130p app/backend/review.py; sed -n 195,310p app/backend/review.py"
}
````

### User / tool · 2026-11-02T20:26:58.589Z

**tool result**
````
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
JUDGE_UNAVAILABLE).
"""
import copy
import json
import time

from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store, why
from app.db import db as DB

ACTIONS = ("accept", "dismiss", "reset", "edit", "count")      # count (D-064): an amount held back for a missing detail becomes an accepted charge, see count_charge.py
# "may" is not here: grounding never reports the month May as a token, so a "may" token is the hedge word
_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
_KIND = {"e": "entry", "a": "amount", "f": "flag"}


def current_text(item: dict):
    ed = item.get("edited") or {}
    return ed.get("summary", item.get("summary") or ""), ed.get("excerpt", item.get("excerpt") or "")


def edit_unconfirmed(kind: str, item: dict) -> bool:
    """T-134 (D-045b, D-051): an ENTRY the paralegal reworded or re-quoted whose state is still needs_review (the second check did not run or did not agree, or another
    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
    not in the letter, not counted as accepted, and the notes do not say she accepted it. Her explicit accept (review_status accepted) ends it; that accept is bound
    by the code checks (set_review). One source for the item view, the review counts, the export and the gate."""
    return (kind == "entry" and item.get("review_status") == "edited" and item.get("state") == "needs_review"
            and any(k in (item.get("edited") or {}) for k in ("summary", "excerpt")))


def code_check_failures(rec, item: dict) -> dict:
    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
    out = {}
    summ, exc = current_text(item)
    if rec is not None:
        g = spanish.module_for(language.record_lang(rec))
        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
        if toks:
            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
        dropped = g.dropped_qualifiers(summ, exc)
        if dropped:
            out["SUMMARY_DROPS_QUALIFIER"] = {"qualifiers": list(dropped)}
        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE"):
                out[c] = {}
        if grounding.locate(rec["excerpt"], exc) is None and "GROUNDING_EXCERPT_NOT_VERBATIM" not in out:
            out["HIGHLIGHT_NOT_FOUND"] = {}
    for c in item.get("state_reasons") or []:
        if c in CODE_CHECK_REASONS:
            out.setdefault(c, {})
    return {c: out[c] for c in CODE_CHECK_REASONS if c in out}


def code_check_message(fails: dict) -> str:
    """Plain words for the first failing check, then the next step."""
    c = next(iter(fails))
    d = fails[c]
    if c == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and d.get("tokens"):
        toks = d["tokens"]
        if any(_NUMERIC_TOKEN.search(t) for t in toks):
            what = "The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(toks) + "."
        else:
            what = "The summary says " + _quoted_words(toks) + ", which the quote does not say."
    elif c == "SUMMARY_DROPS_QUALIFIER" and d.get("qualifiers"):
        what = "The quote carries " + "; ".join(_QUALIFIER_WORDS.get(k, k) for k in d["qualifiers"]) + " that the summary leaves out."
    elif c == "GROUNDING_EXCERPT_NOT_VERBATIM":
        what = "The quote is not word for word in the record."
    rid = (item.get("record_ids") or [None])[0]
    return next((r for r in recs if r["id"] == rid), None)


def confirm_error(item_id: str, item: dict, confirm):
    """D-059: a charge that carries a likely_duplicate or likely_total flag is accepted only when the call names that flag (`confirm`). A 422 CONFIRM_REQUIRED
    with the flag and the exact word to send, else None. Code only: the flag was set by amounts.py, not by a model, and a judge answer does not clear it."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") != "charge" or not f or confirm == f["confirm_with"]:
        return None
    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
              "message": f["message"],      # T-159: the flag's own sentence, without the "confirm by name" tail, so a client never strips the token out of the error message
              "next_action": {"code": "CONFIRM_FLAG", "text": "Confirm the flag by name, or dismiss the charge", "target": {"item_id": item_id}}}
    wrong = "" if confirm is None else " The confirm you sent does not name this flag."
    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")


def confirmed_accept(item: dict) -> bool:
    """T-159: a charge that is accepted and whose flag has been confirmed by name. A repeat accept of it changes nothing, so it writes nothing."""
    f = (item.get("ladder") or {}).get("confirm")
    return item.get("kind") == "charge" and bool(f) and bool(f.get("confirmed_at")) and item.get("review_status") == "accepted"      # item["kind"] = the amount's class


def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
    """The named confirm is kept on the item (ladder.confirm.confirmed_at) and in the accept event that carried it (after.confirm = {flag, name, confirmed_at}),
    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059). Both writes are ONE transaction: a failure on either leaves neither."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") == "charge" and f:
        stamp = {"flag": f["flag"], "name": f["name"], "confirmed_at": store.iso(t)}
        conn.execute("BEGIN")
        try:
            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
            ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
            if ev:
                after = json.loads(ev["after_json"]) if ev["after_json"] else {}
                conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
    if kind is None or item is None:
        kind, item = _item(conn, case_id, item_id)
    if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):
        cand = dict(item)
        if edited is not None:
            cand["edited"] = edited
            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand) or charge_text_error(item_id, cand, lambda: bill_state_for(conn, case_id, item.get("record_ids")))
        if err:
            raise err
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        if confirmed_accept(item):
            return item                                     # T-159: already accepted with its flag confirmed; a repeat accept writes no second decision
        err = confirm_error(item_id, item, confirm)         # D-059
        if err:
            raise err
    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        try:
            _record_confirm(conn, case_id, item_id, item, now)
        except Exception:
            back = {"pending": "reset", "dismissed": "dismiss"}.get(item.get("review_status"))      # T-159 r2: take the accept back, so no charge counts without its confirm on record
            if back:
                DB.apply_review(conn, item_id, back, now=now, case=case_id)
            raise
        out = DB.get_item(conn, item_id, case_id)
    return out


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if action == "count":
        from app.backend import count_charge          # lazy: count_charge imports review
        return count_charge.count(conn, case_id, item_id, body, now=t)
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        confirm = body.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise _bad("The confirm must be the name of the flag.")
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
        if action == "reset":
            restore_pre_edit(conn, case_id, item_id, kind, item, t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def ocr_record_ids(conn, case_id: str) -> set:
    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
    from app.backend import pdf_checks
    pages = (DB.get_case(conn, case_id).get("config") or {}).get("pages")
    if not any(p.get("source") == "ocr" for p in pages or []):
        return set()
    return {r[0] for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=?", (case_id,))
            if pdf_checks.is_ocr_span(pages, r[1], r[2])}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:00.728Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"compared it\\|i compared\\|edit_to_check\\|editToCheck\" app/frontend/*.js app/backend/*.py | cut -c1-220 | head -60"
}
````

### User / tool · 2026-11-02T20:27:00.818Z

**tool result**
````
app/frontend/app.js:30:    const all = itemsOf(c), open = all.filter(ZL.undecided), mine = open.filter((i) => i.state === "needs_review" || ZL.editToCheck(i)).length;   // an edit still to compare is Needs review by defi
app/frontend/dom.js:46:  // letter, but she has not yet compared it with the quote). A dismissed item is decided and is never counted as needing review.
app/frontend/dom.js:47:  ZL.undecided = (i) => { const rs = (i && i.review_status) || "pending"; return rs === "pending" || ZL.editToCheck(i); };
app/frontend/dom.js:49:  ZL.editToCheck = (i) => !!i && i.edit_to_check === true;   // T-136: the server's own flag (T-134): reworded summary OR quote, still Needs review, not yet accepted by her
app/frontend/dom.js:51:  ZL.editCount = (c) => { const n = c && c.review && c.review.counts && c.review.counts.edit_to_check; return n != null ? n : [].concat(c.entries || [], c.undated_entries || []).filter(ZL.editToChe
app/frontend/dom.js:59:  ZL.comparedEdit = (i) => !!i && i.review_status === "accepted" && i.state === "needs_review" && !!i.edited && !ZL.editToCheck(i);
app/frontend/export.js:29:    const open = (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).map((e) => { const r = (cs.records || []).find((x) => x.id === (e.record_ids || [])[0]); return (r ? "
app/frontend/mock.js:133:      edit_to_check: n((i) => i.edit_to_check === true) }, ready_to_export: false };
app/frontend/mock.js:192:        if (id[0] === "e") it.edit_to_check = it.review_status === "edited" && it.state === "needs_review";   // the server's flag (T-134)
app/frontend/stepper.js:281:        const n = c.pending || 0, ed = c.edit_to_check || 0;
app/frontend/stepper.js:282:        if (!n && ed) return { text: "Compare " + plural(ed, "edit", "edits") + " with the quote, then click \u201cI compared it with the quote\u201d on " + (ed === 1 ? "it" : "each") + ". Unt
app/frontend/review.js:266:  // T-136 (paralegal pass 5 F1): the confirmation "I compared it with the quote" is a statement by the paralegal. The a key (and Start review, which lands on this row) must not make it for her
app/frontend/review.js:269:  const COMPARE_PROMPT = "Not recorded yet. Read the quote against your edit. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
app/frontend/review.js:465:    const toCheck = ZL.editToCheck(item);
app/frontend/review.js:473:    const acceptText = toCheck ? "I compared it with the quote" : accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
app/frontend/review.js:613:    if (key === "a" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) {   // as the Accept button: a decided item is not decided twice (T-154: a confirmed flagged 
app/frontend/review.js:617:    if (key === "a" && ZL.editToCheck(f.item)) { askCompare(id); return; }   // T-136 (paralegal F1): one key press never records "I compared it with the quote"; the button (click, or Enter on 
app/frontend/review.js:641:      if (ZL.editToCheck(entry)) rowEl.setAttribute("data-edit-check", ""); else rowEl.removeAttribute("data-edit-check");
app/backend/case_list.py:202:            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "needs_review_open": len(needs_review_order(conn, case_id)), "edits_to_check": counts["edit_to_check
app/backend/present.py:59:            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter
app/backend/present.py:339:    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
app/backend/present.py:344:            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
app/backend/trace.py:298:        code, label = "edit_to_check", "Edited; waiting for your check"
app/backend/trace.py:1137:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
app/backend/trace.py:1141:    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
app/backend/trace.py:1142:        n = rc["edit_to_check"]
app/backend/trace.py:1156:    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
app/backend/trace.py:1227:    if rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0) > 0:
app/backend/trace.py:1231:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
app/backend/review.py:85:    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:05.620Z

**tool call — Bash**
````
{
 "command": "sed -n 255,330p app/frontend/review.js; sed -n 455,520p app/frontend/review.js"
}
````

### User / tool · 2026-11-02T20:27:05.723Z

**tool result**
````
    (tokens || []).forEach((tok) => {
      if (!/^\d[\d.]*$/.test(String(tok))) return;
      const re = /\$?\s?\d[\d,]*(?:\.\d+)?/g; let m, typed = null;
      while ((m = re.exec(text || "")) && !typed) { const bare = m[0].replace(/[$,\s]/g, ""); if (bare === tok || bare.replace(/\.0+$/, "") === tok) typed = m[0].trim(); }
      if (!typed || typed === tok) return;
      out = out.replace(new RegExp("(^|[^\\d$,.])" + String(tok).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![\\d,]|\\.\\d)"), (_, pre) => pre + typed);
    });
    return out;
  };
  // What happened to an edit, in plain words, kept on the row until the next decision: the code re-checks the wording against the quote on every save, then a second AI check reads it.
  const rechecks = {};   // id -> sentence
  // T-136 (paralegal pass 5 F1): the confirmation "I compared it with the quote" is a statement by the paralegal. The a key (and Start review, which lands on this row) must not make it for her:
  // a asks, in a visible line, and puts focus on the button; she records it by clicking the button or pressing Enter on it.
  const comparePrompt = new Set();
  const COMPARE_PROMPT = "Not recorded yet. Read the quote against your edit. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
  // T-136 r2 / D-058 (paralegal F-2): a re-picked quote keeps the AI's summary, and its second check has no answer on the new quote. Accepting alone does not put it in the letter. The words are the
  // server's (item trace "human" step, case trace blocker); the sentences below are only what shows until they arrive or when they cannot be loaded, and say the same thing.
  // Conditional on purpose (T-134 r4b, staff review): before she accepts the gate PASSES and nothing is blocked; D-044 blocks only after she accepts. The server's sentence replaces this one as soon as it arrives.
  const AI_HELD = "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers or you edit the summary in your own words.";
  const ACCEPTED_HELD = "Compared by you. The second AI check still has no answer on the new quote, so the export stays blocked until it answers or you write the summary in your own words.";
  const serverText = new Map();   // "item:<id>" | "blocker:<id>" -> the server's sentence for this page load
  function withServerText(node, key, load, prefix) {   // paint the fallback now; swap in the server's sentence when it arrives
    const set = (t) => { node.textContent = (prefix || "") + t; };
    if (serverText.has(key) && !key.startsWith("blocker:")) { set(serverText.get(key)); return node; }   // a blocker sentence changes with each rerun: ask again
    load().then((t) => { if (t) { serverText.set(key, t); if (node.isConnected) set(t); } }).catch(() => {});
    return node;
  }
  const loadItemWhy = (id) => () => ZL.api.trace(ZL.state.get().token, id).then((tr) => { const h = ((tr && tr.steps) || []).find((x) => x.id === "human"); return h && h.why ? h.why : null; });   // as given: whatever the server says about this item (no pattern test on its words)
  const loadBlockerWhy = (id) => () => ZL.api.caseTrace(ZL.state.get().token).then((tr) => { const g = ((tr && tr.steps) || []).find((x) => x.id === "export_gate"), b = ((g && g.blockers) || []).find((x) => x.item_id === id && x.reason_code === "JUDGE_NOT_RUN"); return b && b.why ? "Compared by you. " + b.why : null; });
  const comparePromptNode = (item) => {
    const p = el("p", { class: "rv-help rv-compare-prompt", "data-testid": "edit-compare-prompt" }, COMPARE_PROMPT + (ZL.secondCheckPending(item) ? " " + AI_HELD : ""));
    if (ZL.secondCheckPending(item)) withServerText(p, "item:" + item.id, loadItemWhy(item.id), COMPARE_PROMPT + " ");
    return p;
  };
  function askCompare(id) {
    comparePrompt.add(id);
    const root = document.querySelector('[data-controls-for="' + id + '"]'); if (!root) return;
    const f = RV.find(RV.caseNow(), id);
    let p = root.querySelector('[data-testid="edit-compare-prompt"]');
    if (!p) { p = comparePromptNode(f.item); const h = root.querySelector('[data-testid="edit-check-hint"]'); if (h) h.after(p); else root.append(p); }
    const b = root.querySelector('[data-testid="btn-accept"]'); if (b) b.focus();
    RV.say(p.textContent);
  }
  function recheckSentence(resp) {
    const w = (resp && resp.warnings) || [], st = resp && resp.item && resp.item.state;
    const lead = "Saved and re-checked. The code compared every number, date and negation in your wording with the quote and found no difference.";
    if (w.length) return lead + " " + w.map((x) => x.message).filter(Boolean).join(" ") + " Compare it with the quote yourself.";
    return lead + (st === "needs_review" ? " The entry still needs your review." : " The second AI check agreed.");
  }

  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  // m2: a refused edit is tied to its field (aria-invalid + aria-describedby) as well as announced
  function markInvalid(id, s) { const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (!ta || !s) return; s.id = s.id || "rv-err-" + id; ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", s.id); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) { s.textContent = msg; markInvalid(id, s); } RV.say(msg, true); }
  const nextCode = (e) => { const n = e && e.detail && e.detail.next_action; return n && n.code ? String(n.code).toUpperCase() : null; };   // T-104: EDIT_SUMMARY | EDIT_QUOTE
  const QUOTE = "Change the quote";
  const changeQuote = (id) => () => { if (ZL.stepper && ZL.stepper.changeQuote) ZL.stepper.changeQuote(id); };
  // T-104: CODE_CHECK_FAILED returned by an EDIT: the server's sentence sits under the edit box (the box stays open with the typed text); EDIT_QUOTE adds a Change the quote action.
  function showEditRefusal(id, e) {
    const ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea');
    const s = slot(id, "rv-error"), msg = RV.asTyped(e.message || "That wording fails a check. Edit it to match the quote.", e.detail && e.detail.tokens, ta0 ? ta0.value : "");
    if (s) {
      ZL.clear(s);
      s.append(el("span", { "data-testid": "edit-refused-msg" }, msg));
      if (nextCode(e) === "EDIT_QUOTE") s.append(" ", el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-edit-refused-quote", "aria-label": QUOTE + " for " + (ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id), onclick: changeQuote(id) }, QUOTE));
    }
    markInvalid(id, s);
    RV.say("Not saved: " + msg, true);
    const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
  }

  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
  // quote.") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.
  const refusals = {};       // id -> {message}
    const id = item.id, st = item.review_status || "pending";
    const isFlag = kind === "flag", canEdit = kind === "entry" || isFlag;
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    const dismissed = st === "dismissed";
    // T-060 r5 (paralegal M2): a reworded entry that is still marked Needs review is not settled. Its one next step is to compare it with the quote and say so (an Accept on her own wording).
    const toCheck = ZL.editToCheck(item);
    const accepted = (st === "accepted" || st === "edited") && !toCheck;

    // T-060 r3: a decided row shows its state, not the action it already took. Primary (filled) is for an undecided item only; Accepted / Dismissed read as quiet state words, Undo is the way back.
    const VARIANT = { accept: st === "pending" || toCheck ? (noted ? "" : "btn--primary") : st === "dismissed" ? "" : "rv-decided", edit: "", dismiss: st === "dismissed" ? "rv-decided rv-decided--muted" : "btn--ghost", reset: "btn--link", audit: "btn--link", "dismiss-reason": "btn--link" };
    const btn = (action, text, tid, extra, name) => el("button", Object.assign({ type: "button", class: ("btn " + (VARIANT[action] || "") + " rv-" + action).replace("  ", " "), "data-testid": tid, "data-action": action, "aria-label": (name || text).replace("…", "") + ": " + lbl }, extra || {}), text);
    const bar = el("div", { class: "rv-actions", role: "group", "aria-label": "Review actions" });
    const blocked = RV.needsDate(item, kind) && st !== "accepted";
    const acceptText = toCheck ? "I compared it with the quote" : accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
    // a dismissed item keeps only its state word, Undo and Audit: no Accept, Keep in notes or Edit (the paralegal's M1: one key must not reverse a dismissal)
    if (!dismissed) bar.append(btn("accept", acceptText, "btn-accept", { "data-icon": accepted ? "check" : null, "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null,
      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, { action: "accept" }, ev.detail === 0 ? { advance: true } : { focus: "accept" }); } }));
    let form;
    if (canEdit && !dismissed) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true), disabled: blocked }));
    bar.append(btn("dismiss", st === "dismissed" ? "Dismissed" : "Dismiss", "btn-dismiss", { "data-icon": st === "dismissed" ? "dash" : null, "aria-pressed": String(st === "dismissed"),
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.reasonOpen)); if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.reset(id) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    if (item.rerun_note) root.append(RV.rerunNote(item));
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (toCheck && !rechecks[id]) {
      const held = ZL.secondCheckPending(item), base = "Still marked Needs review. " + (ZL.wordingEdited(item) ? "Compare your wording with the quote" : "Compare the new quote with the record") + ", then press the button to say you did. Until then it is not in the letter and counts as open.";
      const h = el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, base + (held ? " " + AI_HELD : ""));
      root.append(held ? withServerText(h, "item:" + id, loadItemWhy(id), base + " ") : h);
    }
    if (toCheck && comparePrompt.has(id)) root.append(comparePromptNode(item));
    if (ZL.comparedEdit(item) && ZL.secondCheckPending(item)) {   // D-058: the action that matches the gate is writing the summary, not a rerun that cannot clear it
      const t = el("p", {}, ACCEPTED_HELD);
      root.append(el("div", { class: "rv-help rv-export-note", "data-testid": "compare-export-note" }, withServerText(t, "blocker:" + id, loadBlockerWhy(id)),
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-write-summary", "aria-label": "Write the summary: " + lbl, onclick: () => { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); } }, "Write the summary")));
    }
    if (rechecks[id] && st === "edited") root.append(el("p", { class: "rv-recheck", "data-testid": "edit-recheck-note" }, rechecks[id]));
    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
      el("button", { type: "button", class: "btn btn--link", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));

    // dismiss reason (flags only; optional - R-RV-5)
    const reasonIn = el("input", { type: "text", id: "dr-" + id, class: "rv-input", maxlength: "300", "aria-label": "Reason for dismissing (optional)", "data-testid": "dismiss-reason", value: d.reason || "" });
    reasonIn.addEventListener("input", () => { d.reason = reasonIn.value; });
    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const r = reasonIn.value.trim(); RV.act(id, r ? { action: "dismiss", note: r } : { action: "dismiss" }, { focus: "dismiss" }); } },
      reasonIn, el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-dismiss-confirm" }, "Dismiss"));
    if (isFlag) root.append(reasonRow);

    if (canEdit && !dismissed) {
      const hint = isFlag ? "Your note (internal notes only, never in the letter)" : "Summary wording (the quoted excerpt, date and provider cannot be changed)";
      const ta = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: isFlag ? "note" : "summary", "data-testid": isFlag ? "flag-note" : "edit-summary" });   // named by its visible label (WCAG 2.5.3)
      ta.value = d.text;
      ta.addEventListener("input", () => { d.text = ta.value; ta.removeAttribute("aria-invalid"); });
      form = el("form", { class: "rv-edit", hidden: !d.open, onsubmit: (ev) => {
        ev.preventDefault(); const v = ta.value.trim();
        if (!v) { showError(id, isFlag ? "Write a note first, or cancel." : "The summary can't be empty."); return; }
        const h = form.querySelector(".rv-recheck-hint"), was = h ? h.textContent : "";
        if (h) h.textContent = "Checking your wording against the quote…";
        // T-166 F4: "Save and accept" is her statement that the wording matches the quote beside it, made by clicking that button; the code's check of every number, date and negation still runs on save, and a refusal stops it.
        const both = !isFlag && !!(ev.submitter && ev.submitter.getAttribute("data-testid") === "btn-save-accept");
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:14.034Z

**tool call — Bash**
````
{
 "command": "grep -n \"JUDGE_DISAGREES\\|JUDGE_PARTIAL\\|JUDGE_UNSUPPORTED\" app/backend/*.py | cut -c1-200 | head -40; grep -n \"judge\" app/backend/present.py | head -30"
}
````

### User / tool · 2026-11-02T20:27:14.131Z

**tool result**
````
app/backend/confidence.py:10:    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
app/backend/confidence.py:19:_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
app/backend/export.py:637:                       "JUDGE_PARTIAL": "the second check only partly supported it", "JUDGE_UNSUPPORTED": "the second check did not support it",
app/backend/export.py:638:                       "JUDGE_UNSURE": "the second check was unsure", "JUDGE_DISAGREES": "the second check disagreed"}      # T-167: plain words, never the reason code
app/backend/flags.py:305:    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
app/backend/flags.py:352:        _to_tray(f, "JUDGE_DISAGREES", reason)
app/backend/flags.py:378:    phrase-list and model leaves it needs_review (JUDGE_DISAGREES); a model-only flag J4 rejects goes to the tray (D-053, see _judge_one).
app/backend/narrative.py:23:    "JUDGE_PARTIAL": "The second check found the sentence only partly supported by the cited quote.",
app/backend/narrative.py:24:    "JUDGE_UNSUPPORTED": "The second check found the sentence not supported by the cited quote.",
app/backend/narrative.py:113:            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
app/backend/reclassify.py:39:    "JUDGE_DISAGREES": "A second AI check read this figure as something other than a charge, so it stays as it is.",
app/backend/reclassify.py:221:        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
app/backend/rejudge.py:17:_JUDGE_REASONS = {"JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE", "FIXTURE_MISS"}
app/backend/review.py:7:(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
app/backend/review.py:398:        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
app/backend/trace.py:32:_OBJECTION = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}
app/backend/trace.py:648:        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
app/backend/trace.py:1111:                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})
app/backend/why.py:12:    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
app/backend/why.py:13:    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
app/backend/why.py:14:    "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
13:def _why(reasons, judge=None):
17:            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
40:    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
45:    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
146:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate" and not counted,
293:    return {u["item_id"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u["kind"], u["row"])}
430:    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
434:                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:14.653Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend app/frontend | tail -50; grep -n \"batch\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T20:27:14.779Z

**tool result**
````
 app/backend/api.py       | 22 +++++++++++++--
 app/backend/ingest.py    | 19 +++++++++++--
 app/backend/pdf_text.py  |  2 ++
 app/backend/present.py   |  2 +-
 app/backend/review.py    | 22 +++++++++++++++
 app/backend/store.py     | 56 +++++++++++++++++++++++++++++++++++++
 app/frontend/sections.js | 73 ------------------------------------------------
 7 files changed, 117 insertions(+), 79 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:17.679Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- app/backend/review.py app/backend/api.py app/backend/present.py | head -150; git diff HEAD --stat -- app/frontend tests | tail"
}
````

### User / tool · 2026-11-02T20:27:17.804Z

**tool result**
````
diff --git a/app/backend/api.py b/app/backend/api.py
index 5a4f4d4..64183fa 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -103,7 +103,11 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
     runs = {}
     rejudging = set()
-    DB.connect(db_path).close()
+    _boot = DB.connect(db_path)
+    try:
+        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
+    finally:
+        _boot.close()
     if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
         raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
     if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
@@ -150,7 +154,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         case = DB.get_case(c, token)
         if case is None:
             raise ApiError(404, "not_found", "No such case.")
-        return case
+        return store.settle_stale_run(c, case)           # T-178: an orphaned "running" case reads failed on every route, not only after a restart
 
     # -------------------------------------------------- errors / headers
     @app.exception_handler(ApiError)
@@ -218,6 +222,16 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
         return resp
 
+    def _clean_strings(v):
+        """T-178: a lone UTF-16 surrogate in any text of a request body (a title, an edit, a note) becomes U+FFFD before a route sees it: it cannot be encoded, so it was a 500."""
+        if isinstance(v, str):
+            return ingest.replace_lone_surrogates(v)
+        if isinstance(v, list):
+            return [_clean_strings(x) for x in v]
+        if isinstance(v, dict):
+            return {_clean_strings(k): _clean_strings(x) for k, x in v.items()}
+        return v
+
     async def body_of(request: Request) -> dict:
         cl = request.headers.get("content-length")
         if cl and cl.isdigit() and int(cl) > MAX_BODY_BYTES:
@@ -235,7 +249,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
         if not isinstance(b, dict):
             raise ApiError(400, "bad_request", "Request body must be a JSON object.")
-        return b
+        return _clean_strings(b)
 
     # -------------------------------------------------- routes
     @app.get("/api/health")
@@ -404,6 +418,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         finally:
             c.close()
             runs.pop(token, None)
+            store.run_ended(token)
 
     @app.post("/api/cases/{token}/run", status_code=202)
     async def run_case(token: str, request: Request):
@@ -421,6 +436,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             if decided and b.get("confirm_rerun") is not True:
                 raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
             now = time.time()
+            store.run_started(token)
             DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
             runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
             runs[token].start()
diff --git a/app/backend/present.py b/app/backend/present.py
index f0e6380..3138e1c 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -43,7 +43,7 @@ def rerun_available(row) -> bool:
 
 def _common(row):
     return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
-            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
+            "review_status": row["review_status"], "version": row.get("updated_at"), "edited": row.get("edited"), "ladder": _ladder(row),
             "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
             "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item
 
diff --git a/app/backend/review.py b/app/backend/review.py
index 3678f66..3bfb5a7 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -268,12 +268,34 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
     return out
 
 
+STALE_MESSAGE = "This item changed in another tab; reload to see it."
+_TARGET_STATUS = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}
+
+
+def check_fresh(item: dict, body: dict, action: str) -> None:
+    """T-178 (GATE-M3 chaos): a decision made from a stale screen must not silently override a newer one. The client sends what it last saw of the item: `version` (the item's
+    `version` field, its last-change time) and/or `expected_status` (its `review_status`). If either differs from the stored row the write is refused with 409 `stale_item`
+    and nothing changes. Neither sent = no check (older clients). A re-assertion that would leave the item exactly as it is (accept on an accepted item, dismiss on a
+    dismissed one, reset on a pending one) is harmless and is let through."""
+    ver, exp = body.get("version"), body.get("expected_status")
+    if ver is None and exp is None:
+        return
+    if exp is not None and exp not in ("pending", "accepted", "edited", "dismissed"):
+        raise _bad("The expected_status must be one of pending, accepted, edited or dismissed.")
+    if ver is not None and (isinstance(ver, bool) or not isinstance(ver, (int, float))):
+        raise _bad("The version must be the number the item was last shown with.")
+    stale = (exp is not None and exp != item["review_status"]) or (ver is not None and abs(float(ver) - float(item.get("updated_at") or 0)) > 1e-6)
+    if stale and _TARGET_STATUS.get(action) != item["review_status"]:
+        raise ReviewError(409, "stale_item", {"item_id": item["id"], "review_status": item["review_status"], "version": item.get("updated_at")}, STALE_MESSAGE)
+
+
 def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
     t = _now(now)
     kind, item = _item(conn, case_id, item_id)
     action = (body or {}).get("action")
     if action not in ACTIONS:
         raise _bad("That action is not allowed.")
+    check_fresh(item, body, action)
     if action == "count":
         from app.backend import count_charge          # lazy: count_charge imports review
         return count_charge.count(conn, case_id, item_id, body, now=t)
 app/frontend/sections.js                           |  73 ----
 tests/e2e/test_demo_provenance.py                  | 149 -------
 tests/e2e/test_mvp_finish.py                       | 474 ---------------------
 tests/e2e/test_mvp_polish.py                       | 351 ---------------
 ...ec211dca19fd26207433389d8e62ea61a4c97c7557.json |  11 -
 ...c0a17b50480b0491795555fdc4bccfe6bac45e9a00.json |  11 -
 tests/unit/test_prepared_provenance.py             | 120 ------
 7 files changed, 1189 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:24.664Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p app/backend/present.py | cut -c1-260; sed -n 1,40p app/backend/confidence.py | cut -c1-240; grep -n \"def apply_review\" -A60 app/db/db.py | head -110"
}
````

### User / tool · 2026-11-02T20:27:24.794Z

**tool result**
````
"""Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
import json
import re

from app.backend import amounts as AM, conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB
from app.llm import audited as AU

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons, judge=None):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
    return lad


def rerun_available(row) -> bool:
    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
            "review_status": row["review_status"], "version": row.get("updated_at"), "edited": row.get("edited"), "ladder": _ladder(row),
            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
            "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item


def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row),
            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter

"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.

Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
D-050: ctx["translated"] (the item comes from a record routed Spanish or LANGUAGE_UNCERTAIN) always adds AI_TRANSLATION, so such an item
can never be `verified`, whatever its code checks and judge said; the paralegal's accept is the gate. Every caller that has the record passes it. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
"""
REASON_CODES = (
    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE", "CHARGE_TEXT_IN_ENTRY",
)
REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}

_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}


def sort_key(state: str) -> int:
    """needs_review first, then verified, then rejected."""
    return STATE_ORDER[state]


def _known(code: str) -> str:
    if code not in REASON_CODES:
        raise ValueError(f"unknown reason code: {code}")
    return code


def _lookup(table: dict, value, none_ok=()):
    if value is None or value in none_ok:
        return None
    if value not in table:
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
231-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
232-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
233-        conn.execute("COMMIT")
234-    except Exception:
235-        conn.execute("ROLLBACK")
236-        raise
237-    return get_item(conn, item_id, row["case_id"])
238-
239-
240-def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
241-    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
242-    if action not in AUDIT_ONLY_ACTIONS:
243-        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
244-    eid = _tok("v")
245-    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
246-                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
247-    return eid
248-
249-
250-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
251-    if status not in REVIEW_STATUSES:
252-        raise ValueError(f"invalid review_status {status!r}")
253-    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
254-    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
255-
256-
257-def list_events(conn, case_id: str, item_id: str = None) -> list:
258-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
259-    if item_id:
260-        q, a = q + " AND item_id=?", a + [item_id]
261-    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
262-
263-
264-def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
265-    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
266-    cid = fields.pop("id", None) or _tok("c")
267-    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
268-           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
269-    _insert(conn, "llm_calls", row)
270-    return cid
271-
272-
273-def get_llm_call(conn, call_id: str):
274-    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
275-    return _decode(r) if r else None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:29.978Z

**tool call — Bash**
````
{
 "command": "grep -n \"ladder_verdict\\|\\\"verdict\\\"\\|\\['verdict'\\]\" app/backend/review.py app/backend/judge_guard.py app/backend/pipeline.py | head -30; grep -rn \"ladder\\[.judge.\\]\\|\\\"judge\\\":\" app/backend/pipeline.py app/backend/judges.py app/backend/flags.py | head"
}
````

### User / tool · 2026-11-02T20:27:30.080Z

**tool result**
````
app/backend/pipeline.py:235:        if e["state"] == "rejected" or (e["ladder"].get("judge") or {}).get("verdict"):
app/backend/pipeline.py:237:        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
app/backend/pipeline.py:254:    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None
app/backend/pipeline.py:266:    return cause if ((old.get("ladder") or {}).get("judge") or {}).get("verdict") not in (None, "unavailable") else None
app/backend/pipeline.py:283:    ov, nv = (ol.get("judge") or {}).get("verdict"), (nl.get("judge") or {}).get("verdict")
app/backend/pipeline.py:426:                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None),
app/backend/review.py:392:    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
app/backend/review.py:395:        ladder_verdict = judges.to_ladder("j1", verdict)
app/backend/review.py:397:    if ladder_verdict in ("partially", "unsupported"):
app/backend/review.py:398:        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
app/backend/review.py:400:    elif ladder_verdict == "unavailable":
app/backend/review.py:401:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}) + " Until you do, the item stays marked for review.", "item_id": item_id})
app/backend/review.py:402:    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
app/backend/review.py:405:    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
app/backend/review.py:449:    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
app/backend/review.py:450:        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
app/backend/review.py:468:    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
app/backend/review.py:688:              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
app/backend/flags.py:41:    ladder = {"grounding_failures": st["grounding_failures"], "schema_valid": True, "code_reasons": [], "judge": st.get("judge")}
app/backend/flags.py:56:         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
app/backend/flags.py:59:                    "judge": "unavailable" if origin != "lexicon" else None}}
app/backend/flags.py:238:            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}
app/backend/flags.py:290:         "ladder": {"item_id": None, "generator": None, "judge": None,
app/backend/flags.py:293:         "_stage": {"grounding_failures": fail, "injection": any_tagged, "agreement": None, "judge": "unavailable",
app/backend/pipeline.py:31:    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
app/backend/pipeline.py:421:         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
app/backend/pipeline.py:425:                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
app/backend/pipeline.py:682:            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:40.485Z

**tool call — Bash**
````
{
 "command": "grep -n \"action: \\\"accept\\\"\\|'accept'\\|\\\"accept\\\"\" app/frontend/*.js | cut -c1-230; grep -n \"batch\" app/backend/api.py app/backend/review.py app/backend/*.py | grep -v \"^app/backend/api.py.*#\" | cut -c1-200 | head -20"
}
````

### User / tool · 2026-11-02T20:27:40.581Z

**tool result**
````
app/frontend/audit.js:51:    const lastAccept = {}; events.forEach((e) => { if (e.action === "accept") lastAccept[e.item_id] = e; });   // her latest accept is the one the confirm belongs to
app/frontend/batch.js:24:      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "accept", item_ids: ids });
app/frontend/mock.js:188:        if (a === "accept") it.review_status = "accepted"; else if (a === "dismiss") it.review_status = "dismissed"; else if (a === "reset") { it.review_status = "pending"; it.edited = null; }
app/frontend/mock.js:198:        if (!["accept", "reset"].includes(act) || !ids.length) return err(400, "bad_request", "A batch needs an action and item ids.");
app/frontend/mock.js:200:        if (act === "accept") found.forEach((e) => { if (e && (e.state !== "verified" || e.review_status !== "pending")) bad.push({ id: e.id, reason: "only verified, not-yet-reviewed entries can be accepte
app/frontend/mock.js:202:        found.forEach((e) => { if (act === "accept") e.review_status = "accepted"; else { e.review_status = "pending"; e.edited = null; } });
app/frontend/judges.js:49:  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "accept".
app/frontend/narrative.js:67:        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-accept-narrative", "aria-pressed": String(nar.status === "accepted"), disabled: !(nar.sentences || []).length, oncl
app/frontend/mock_flags.js:37:        if (a === "accept") f.review_status = "accepted";
app/frontend/review.js:375:    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
app/frontend/review.js:376:    if (body.action === "accept" && !body.confirm && found && found.kind === "amount" && found.item.confirm_required && found.item.flag && ZL.confirmCharge) {   // D-059 (T-154): a flagged charge is coun
app/frontend/review.js:408:      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
app/frontend/review.js:412:      } else if (e && String(e.code).toUpperCase() === "CONFIRM_REQUIRED" && body.action === "accept" && !body.confirm && ZL.confirmCharge) {   // D-059: the page did not know the charge was flagged; the
app/frontend/review.js:475:    if (!dismissed) bar.append(btn("accept", acceptText, "btn-accept", { "data-icon": accepted ? "check" : null, "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked 
app/frontend/review.js:476:      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, { action: "accept" }, ev.detail === 0 ? { advance: true } : { focus: "accept" }); } 
app/frontend/review.js:522:          .then((ok) => (ok && both ? RV.act(id, { action: "accept" }, { focus: "accept" }) : null))
app/frontend/review.js:618:    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
app/frontend/timeline.js:162:      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
app/backend/review.py:238:    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
app/backend/review.py:789:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
app/backend/review.py:790:    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
app/backend/case_extras.py:17:# ------------------------------------------------------------------ batch review
app/backend/case_extras.py:20:        super().__init__("invalid_batch")
app/backend/case_extras.py:34:    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
app/backend/case_extras.py:42:        if kind == "amount" and row["kind"] == "charge":      # D-059: a charge is accepted one at a time, never in a batch
app/backend/case_extras.py:43:            bad.append({"id": i, "reason": "charge_in_batch"})
app/backend/case_extras.py:57:def apply_batch(conn, case_id, body, now):
app/backend/case_extras.py:71:                review.batch_apply(conn, case_id, i, action, now, recs)
app/backend/case_extras.py:75:                review.batch_apply(conn, case_id, i, "reset", now)
app/backend/case_extras.py:121:    @app.post("/api/cases/{token}/review/batch")
app/backend/case_extras.py:122:    async def review_batch(token: str, request: Request):
app/backend/case_extras.py:128:                return apply_batch(c, token, b, now())
app/backend/case_extras.py:132:                if any(r["reason"] == "charge_in_batch" for r in e.rejected):      # D-059
app/backend/case_extras.py:133:                    raise ApiError(422, "CHARGES_NOT_BATCHED", "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review
app/backend/case_extras.py:140:                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
app/backend/count_charge.py:83:            review.batch_apply(conn, case_id, item_id, "reset", t)
app/backend/reclassify.py:160:        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
app/backend/pipeline.py:232:    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) re
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:56.471Z

**tool call — Bash**
````
{
 "command": "sed -n 785,800p app/backend/review.py; sed -n 28,80p app/backend/case_extras.py; grep -n \"class ReviewError\" -A8 app/backend/review.py; grep -n \"set_review(\" app/backend/*.py"
}
````

### User / tool · 2026-11-02T20:27:56.569Z

**tool result**
````
        return {}
    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)


def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
    set_review(conn, case_id, item_id, action, now=now, recs=recs)
    if not err:
        return None
    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad, cache = [], {}
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind == "amount" and row["kind"] == "charge":      # D-059: a charge is accepted one at a time, never in a batch
            bad.append({"id": i, "reason": "charge_in_batch"})
        elif kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
            bad.append(err)
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad


def apply_batch(conn, case_id, body, now):
    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("bad_request")
    with _LOCK:
        bad = _check(conn, case_id, ids, action)
        if bad:
            raise BatchRefused(bad)
        done = []
        recs = store.load_records(conn, case_id) if action == "accept" else None
        try:
            for i in ids:
                review.batch_apply(conn, case_id, i, action, now, recs)
                done.append(i)
        except Exception:
            for i in reversed(done):          # compensate: each undo is itself an audited event
                review.batch_apply(conn, case_id, i, "reset", now)
            raise
    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}


23:class ReviewError(Exception):
24-    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
25-        super().__init__(code)
26-        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")
27-
28-
29-def _now(now):
30-    return now() if callable(now) else (time.time() if now is None else now)
31-
app/backend/count_charge.py:86:        review.set_review(conn, case_id, item_id, "accept", now=t, kind="amount", item=DB.get_item(conn, item_id, case_id), confirm=lad["confirm"]["confirm_with"])
app/backend/review.py:237:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
app/backend/review.py:311:        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
app/backend/review.py:419:        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
app/backend/review.py:462:    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
app/backend/review.py:792:    set_review(conn, case_id, item_id, action, now=now, recs=recs)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:04.993Z

**tool call — Bash**
````
{
 "command": "sed -n 40,60p app/frontend/audit.js | cut -c1-400; grep -n \"confirm\" app/backend/trace.py | cut -c1-200 | head; grep -n \"review/batch\\|\\\"/api/cases/{token}/items/{item_id}/review\\\"\" -B2 -A25 app/backend/api.py | head -80"
}
````

### User / tool · 2026-11-02T20:28:05.110Z

**tool result**
````
    clear(body);
    if (r.status !== 200) { body.append(el("p", { class: "rv-error", role: "alert" }, RV.errMsg(r, "The audit could not be loaded."))); return; }
    const a = r.body, calls = (a.calls || []).filter((x) => !itemId || x.item_id === itemId), events = (a.events || []).filter((x) => !itemId || x.item_id === itemId);
    const s = a.summary || {};
    body.append(el("p", { class: "rv-help", "data-testid": "audit-summary" }, itemId ? `${calls.length} model call${calls.length === 1 ? "" : "s"} for this item.` :
      `${s.calls != null ? s.calls : calls.length} model calls, ${s.latency_ms_total != null ? s.latency_ms_total + " ms total latency" : ""}${s.cost_usd != null ? ", $" + s.cost_usd : ""}${s.by_backend ? ", by backend: " + Object.keys(s.by_backend).map((k) => k + " " + s.by_backend[k]).join(", ") : ""}.`));
    body.append(el("h3", {}, "Model calls"));
    if (calls.length) body.append(el("ol", { class: "au-list" }, calls.map(callRow)));
    else body.append(el("p", { class: "rv-empty" }, itemId ? "No model call was made for this item: code computed it." : "No model calls recorded."));
    body.append(el("h3", {}, "Your decisions"));
    const fn = itemId && ZL.chargeFlagNote ? ZL.chargeFlagNote(itemId, "audit-charge-flag") : null; if (fn) body.append(fn);
    const lastAccept = {}; events.forEach((e) => { if (e.action === "accept") lastAccept[e.item_id] = e; });   // her latest accept is the one the confirm belongs to
    if (events.length) body.append(el("ol", { class: "au-list" }, events.map((e) => eventRow(e, ZL.chargeConfirmWord && lastAccept[e.item_id] === e ? ZL.chargeConfirmWord(e.item_id) : null)))); else body.append(el("p", { class: "rv-empty" }, "No decisions recorded yet."));
  };

  RV.registerPanel("audit", (root, c) => {
    ZL.clear(root);
    root.append(el("h2", {}, "Audit"), el("p", { class: "rv-help" }, "Every model call behind this case, and every decision you made."),
      el("button", { type: "button", class: "btn", "data-testid": "btn-audit-case", onclick: () => RV.openAudit(null) }, "Open full audit"));
  });
})();
42:    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
61:    "CONFIRM_DATE": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.",
70:    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
71:    "CONFIRM_FLAG": "Confirm the flag by name, or dismiss the charge",       # same words as the 422 CONFIRM_REQUIRED next_action (review.confirm_error)
76:    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
77:    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
249:          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
257:    if review.edit_unconfirmed(kind, row):      # T-134 r2: her edit is saved but she has not accepted it; the trail must not say she did (same rule as the gate, the export and the notes)
261:        cf = (row.get("ladder") or {}).get("confirm") if kind == "amount" and rs == "accepted" else None
262:        said = f"You accepted this item and confirmed the flag \u201c{cf['name']}\u201d by name." if cf and cf.get("confirmed_at") else "You accepted this item."      # T-159
570-            c.close()
571-
572:    @app.post("/api/cases/{token}/items/{item_id}/review")
573-    async def review_item(token: str, item_id: str, request: Request):
574-        b = await body_of(request)
575-        c = conn()
576-        try:
577-            get_case(c, token)
578-            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
579-        finally:
580-            c.close()
581-
582-    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
583-    from app.backend import billing
584-    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
585-    from app.backend import pdf_routes
586-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
587-    from app.backend import reclassify
588-    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
589-    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
590-    from app.backend import calibration_route
591-    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
592-
593-    @app.get("/api/cases/{token}/export")
594-    def export(token: str, style: str = None):
595-        from app.backend import export_routes as XR
596-        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
597-            raise ApiError(422, "invalid_style", XR.invalid_style_message())
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:20.217Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\nold='''def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:\n    t = _now(now)\n'''\nnew='''_DISPUTED = {\"partially\": \"JUDGE_PARTIAL\", \"unsupported\": \"JUDGE_UNSUPPORTED\", \"disagrees\": \"JUDGE_DISAGREES\"}\n_DISPUTE_SENTENCE = {\"partially\": \"The second AI check found this only partly supported by the quote.\", \"unsupported\": \"The second AI check found this not supported by the quote.\",\n                     \"disagrees\": \"The second AI check disagreed with the first result for this item.\"}\n\n\ndef judge_dispute(item: dict):\n    \"\"\"D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the\n    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only.\"\"\"\n    j = (item.get(\"ladder\") or {}).get(\"judge\")\n    v = j.get(\"verdict\") if isinstance(j, dict) else None\n    if v in _DISPUTED:\n        return v\n    reasons = item.get(\"state_reasons\") or []\n    return next((k for k, code in _DISPUTED.items() if code in reasons), None)\n\n\ndef compare_error(item_id: str, item: dict, compared):\n    \"\"\"D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it.\"\"\"\n    v = judge_dispute(item)\n    if not v or compared is True or item.get(\"review_status\") == \"accepted\":\n        return None\n    return ReviewError(422, \"COMPARE_REQUIRED\", {\"item_id\": item_id, \"reason_code\": \"COMPARE_REQUIRED\", \"verdict\": v,\n                       \"next_action\": {\"code\": \"COMPARE_WITH_QUOTE\", \"text\": \"Read it against the quote, then say you compared it\", \"target\": {\"item_id\": item_id}}},\n                       _DISPUTE_SENTENCE[v] + \" Read it against the quote, then say you compared it before you accept it.\")\n\n\ndef _record_compared(conn, case_id: str, item_id: str, t) -> None:\n    \"\"\"D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it.\"\"\"\n    ev = conn.execute(\"SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1\", (case_id, item_id)).fetchone()\n    if ev:\n        after = json.loads(ev[\"after_json\"]) if ev[\"after_json\"] else {}\n        conn.execute(\"UPDATE review_events SET after_json=? WHERE id=?\", (DB._enc({**after, \"compared\": {\"at\": store.iso(t)}}), ev[\"id\"]))\n\n\ndef apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:\n    t = _now(now)\n'''\nassert old in s\ns=s.replace(old,new,1)\nold2='''        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)\n        if action == \"reset\":'''\nnew2='''        compared = body.get(\"compared\")\n        if compared is not None and not isinstance(compared, bool):\n            raise _bad(\"The compared flag must be true or false.\")\n        if action == \"accept\" and (err := compare_error(item_id, item, compared)):      # D-066; before any write\n            raise err\n        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)\n        if action == \"accept\" and compared is True:\n            _record_compared(conn, case_id, item_id, t)\n        if action == \"reset\":'''\nassert old2 in s\ns=s.replace(old2,new2,1)\nopen(p,'w').write(s)\n\np='app/backend/case_extras.py'\ns=open(p).read()\nold='''        elif action == \"accept\" and review.date_unconfirmed(conn, case_id, kind, row):'''\nnew='''        elif action == \"accept\" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare\n            bad.append({\"id\": i, \"reason\": \"judge_disputed\"})\n        elif action == \"accept\" and review.date_unconfirmed(conn, case_id, kind, row):'''\nassert old in s\nopen(p,'w').write(s.replace(old,new,1))\nEOF\ngit diff HEAD --stat -- app/backend/case_extras.py; grep -n \"def _bad\" -A3 app/backend/review.py | head; grep -n \"ReviewError\" app/backend/api.py | head -5"
}
````

### User / tool · 2026-11-02T20:28:20.384Z

**tool result**
````
 app/backend/case_extras.py | 2 ++
 1 file changed, 2 insertions(+)
43:def _bad(msg, **detail):
44-    return ReviewError(422, "invalid_edit", detail, msg)
45-
46-
164:    @app.exception_handler(review.ReviewError)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:27.529Z

**tool call — Bash**
````
{
 "command": "ls tests/unit | grep -i \"review\\|batch\\|confirm\\|accept\" ; grep -ln \"JUDGE_PARTIAL\\|partially\" tests/unit/*.py | head; ls tests/e2e | head -80"
}
````

### User / tool · 2026-11-02T20:28:27.640Z

**tool result**
````
test_date_unconfirmed.py
test_review_rules.py
test_t134_unconfirmed_edit.py
tests/unit/test_confidence.py
tests/unit/test_d050_never_verified.py
tests/unit/test_eval_runner.py
tests/unit/test_generator.py
tests/unit/test_judges.py
tests/unit/test_narrative.py
tests/unit/test_pipeline.py
tests/unit/test_schemas.py
tests/unit/test_spanish_records.py
tests/unit/test_t134_unconfirmed_edit.py
__init__.py
__pycache__
_scripted_server.py
conftest.py
test_adversarial.py
test_adversarial_ui.py
test_api.py
test_change_the_quote.py
test_charge_confirm.py
test_charges.py
test_code_check_refusal.py
test_conflict_coverage.py
test_conflict_skipped.py
test_count_charge.py
test_count_duplicate.py
test_demo_provenance.py
test_edit.py
test_edit_to_check.py
test_export_ui.py
test_flags_panel.py
test_held_quote_gate.py
test_input.py
test_journey_modes.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_letter_matrix.py
test_local_mode.py
test_multicase.py
test_mvp_finish.py
test_mvp_polish.py
test_no_console_errors.py
test_polish_r3.py
test_polish_r4.py
test_polish_r5.py
test_rerun_judge.py
test_rerun_note.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
test_two_cases_side_by_side.py
test_uncovered_ui.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:29.675Z

**tool call — Bash**
````
{
 "command": "sed -n 1,70p tests/unit/test_t134_unconfirmed_edit.py"
}
````

### User / tool · 2026-11-02T20:28:29.764Z

**tool result**
````
"""T-134 (paralegal pass 4 M2; D-045b, D-051): an edited entry that is still needs_review has not been decided.
It is not in the letter, not counted as accepted, listed by the gate as EDIT_NOT_CONFIRMED (a warning: it is not in the letter, so it blocks nothing),
and the notes never say the paralegal accepted it. Her explicit Accept (after comparing with the quote) is still bound by the code checks (422)."""
import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "t134.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _gate(c, tok):
    return next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "export_gate")


def _setup(c, accept=("e1",)):
    tok = run_case(c)
    for i in accept:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "edited" and r.json()["item"]["state"] == "needs_review"
    return tok, r.json()


def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted(env):
    _, c = env
    tok, r = _setup(c)
    assert r["item"]["edit_to_check"] is True
    assert r["review"]["counts"]["edit_to_check"] == 1
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200
    j = ex.json()
    assert EDIT not in j["letter_text"] and "daily headaches" not in j["letter_text"]
    assert "e3" not in [e["id"] for e in j["items"]["entries"]]
    assert j["counts"]["entries"] == 1 and j["counts"]["pending"] >= 1
    assert j["excluded"]["edit_not_confirmed"] == 1
    assert j["provenance"]["edited_count"] == 0
    notes = j["internal_notes_text"]
    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" not in notes      # T-167: the code stays in the API fields, not the notes
    assert "not yet confirmed" in notes
    before_edited = notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
    assert "not in the letter" in before_edited and EDIT in before_edited
    assert "Items not reviewed: 0" not in notes


def test_gate_names_the_unconfirmed_edit_as_a_warning_and_agrees_with_the_export(env):
    _, c = env
    tok, _ = _setup(c)
    g = _gate(c, tok)
    assert g["ready"] is True and g["blockers"] == []          # not in the letter, so it does not block (the same rule as a pending item, D-045a)
    w = {x["reason_code"]: x for x in g["warnings"]}
    assert w["EDIT_NOT_CONFIRMED"]["count"] == 1 and "second check" in w["EDIT_NOT_CONFIRMED"]["why"]
    assert g["counts"]["edit_not_confirmed"] == 1 and g["counts"]["accepted"] == 1
    assert c.get(f"/api/cases/{tok}/export").status_code == 200       # ready == export allowed


def test_only_an_unconfirmed_edit_accepted_means_nothing_accepted(env):
    _, c = env
    tok, r = _setup(c, accept=())
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:30.022Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/e2e/test_edit_to_check.py; sed -n 1,80p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T20:28:30.105Z

**tool result**
````
"""T-136 (frontend; backend T-134, D-045b, D-051): the UI reads the item's own `edit_to_check` and the review's `counts.edit_to_check`, not a summary-only guess.
An edit made with the quote picker (excerpt only, no edited summary) on an entry that is still Needs review is open: its Accept reads "I compared it with the quote", the header,
the Open-decisions strip and the copy-confirm count it, the export stepper shows the gate warning EDIT_NOT_CONFIRMED in its plain reason, and the Accept clears all of it.
Real backend; needs ZLAYT_DB (the SQLite file of the server under test) to put the entry into Needs review the way a missing second check does (the fixture set verifies every entry).
No new test ids: btn-edit-excerpt, excerpt-unit, btn-save-excerpt, btn-accept, edit-check-hint, todo-list, need-review-count, case-next-action, copy-confirm, gate-warning,
btn-gate-warning-jump (all declared in conftest). New (declared in conftest): edit-compare-prompt, dismissed-group-flags / dismissed-group-amounts, dismissed-summary-flags / dismissed-summary-amounts,
dismissed-flags, dismissed-amounts."""
import os
import re
import sys
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, needs_db, reveal
from tests.e2e.test_stepper import open_rail

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")


def _case(tok):
    return api("GET", f"/api/cases/{tok}")[1]


def _needs_review_entry_with_picker(tok):
    """Put a dated, pending entry whose record has several sentences into Needs review (store write, like a missing second check) and return it."""
    path = needs_db()
    c = _case(tok); recs = {r["id"]: r for r in c["records"]}
    e = next(x for x in c["entries"] if x["id"] != "e1" and x["state"] == "verified" and x["date"] and x["review_status"] == "pending" and len(x["record_ids"]) == 1
             and len([s for s in recs[x["record_ids"][0]]["sentences"] if s["start"] >= x["excerpt_start"] and s["end"] <= x["excerpt_end"]]) >= 2)
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        DB.update_item(conn, e["id"], now=9e9, case=tok, state="needs_review")
    finally:
        conn.close()
    return e


def _progress(page):
    t = page.locator("#progress-text").inner_text()
    m = re.match(r"(\d+) of (\d+) decided", t)
    assert m, t
    pt = page.locator("#progress-text")   # T-166 F2: the visible line is short ('4 of 23 decided · 3 to review'); the counts are data attributes
    return int(m.group(1)), int(m.group(2)), int(pt.get_attribute("data-needs") or 0), int(pt.get_attribute("data-edits") or 0)


def _row(page, eid):
    return page.locator(f'[data-testid=queue] [data-item-id="{eid}"], [data-testid=timeline] [data-item-id="{eid}"]').first


def _quote_edit(row):
    """Use the quote picker the way a paralegal does: Change quote, drop the last chosen sentence, Use these sentences. No summary is edited."""
    reveal(row.get_by_test_id("btn-edit-excerpt")).click()
    ed = row.get_by_test_id("excerpt-editor"); expect(ed).to_be_visible()
    units = ed.get_by_test_id("excerpt-unit")
    last = max(i for i in range(units.count()) if units.nth(i).is_checked())
    units.nth(last).click()
    ed.get_by_test_id("btn-save-excerpt").click()


@pytest.fixture
def edited_quote(page, sample_case):
    e = _needs_review_entry_with_picker(sample_case)
    open_case(page, sample_case)
    row = _row(page, e["id"]); row.scroll_into_view_if_needed()
    before = _progress(page)
    _quote_edit(row)
    expect(row).to_have_attribute("data-review", "edited")
    return {"tok": sample_case, "id": e["id"], "before": before, "orig": e["excerpt"]}


def _accept_something_else(t):
    assert api("POST", f"/api/cases/{t['tok']}/items/e1/review", {"action": "accept"})[0] == 200      # the letter has one entry, so the gate is ready with a warning


def test_a_quote_only_edit_is_open_and_offers_the_compare_accept(page, edited_quote):
    t = edited_quote; row = _row(page, t["id"])
    got = next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])
    assert got["excerpt"] != t["orig"] and got["edit_to_check"] is True and not (got.get("edited") or {}).get("summary"), "the setup is a quote-only edit"
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
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
T-136 round 2: compare-export-note (D-058: a note on an accepted, compared quote-only edit under the AI's summary whose second AI check has no answer: the server's blocker sentence; holds btn-write-summary 'Write the summary', which opens the edit box; NO rerun button), data-blocker-code (the reason code on a gate-blocker row, e.g. JUDGE_NOT_RUN), btn-gate-write-summary (the same action on that item's JUDGE_NOT_RUN gate-blocker row); the row's entry-state chip of a compared edit reads
  'Compared by you' (not 'Needs review') with entry-reasons 'Compared by you with the quote; the second AI check ...'; edited-note of a quote-only edit reads 'Quote changed by you' and shows the original excerpt.
T-142: conflict-empty (the Conflicts group's empty state: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.'), conflict-coverage (details in the Conflicts group: open when empty, collapsed when conflicts are listed; words from GET case `checks`
  {conflict_types, labels, not_checked}, a fixed fallback without it) holding conflict-checked-item, conflict-not-checked-item and, in the fallback only, conflict-coverage-note.
T-149 (multi-case, tests/e2e/test_multicase.py): cases-overview (the home section, local mode only), cases-row (one per case, data-token), cases-open (the link that opens it), cases-title, cases-dates (<time> elements), cases-stage, cases-progress-<kind> (a <progress>, kind = entries | flags | amounts)
  with cases-progress-text-<kind> ('2 of 5'), call-out chips cases-chip-needs-review, cases-chip-edits, cases-chip-tray, cases-chip-blocked ('Export blocked (n)') with cases-blocker-reason (one per distinct reason, first two), cases-chip-ready; cases-filter-all / cases-filter-attention / cases-filter-ready (aria-pressed),
  cases-sort (select: attention, recent, least_done, title), cases-count, cases-empty. Detail: case-overview (first block of the timeline), co-progress-<kind> / co-progress-text-<kind>, co-chip-needs-review / co-chip-edits / co-chip-tray / co-chip-blocked / co-chip-ready, co-blocker-reason,
  co-gate-steps (<details>) with co-gate-toggle (its summary), co-gate-verdict, co-gate-step (one per step of GET trace; data-step-id, data-step-status) holding co-gate-word and co-gate-why; btn-all-cases (header: back to the overview).
  Literal forms used by specs: cases-progress-entries, cases-progress-<seq>, cases-progress-text-entries, cases-progress-text-<seq>, co-progress-entries, co-progress-<seq>, co-progress-text-entries, co-progress-text-<seq> (<seq> = flags | amounts).
T-149 round 2 (tests/e2e/test_multicase.py): the overview block is ONE block: it holds todo-strip and checks-card (case-stepper, judge-panel) in its .co-slot; co-gate-* are gone (the Case checks rail is the one place for the steps). need-review-count is now the block's
  needs-review chip (open items only), co-chip-edits, co-chip-tray (quiet), cases-chip-can-export and co-chip-can-export ('Can export \u2014 N not reviewed (they stay out of the letter)', amber), co-chip-ready ('Everything decided', green, only when nothing is undecided), co-chip-blocked; the same chip ids with the cases- prefix on a row.
  Row: cases-decided ('n of N decided'), cases-next (the one call-out of a not-analyzed or failed row), cases-search (title), cases-list (data-ready="true" after the first settled paint), cases-loading, cases-load-error with cases-retry, cases-open-error, filter cases-filter-ready is now 'Ready to send'.
  Detail: case-heading (the h2, tabindex -1, focused when a case opens from the list, aria-label names the case), do-first with btn-do-first (one line from next_action {item_id, kind, reason}), btn-rename-case, case-rename-input, btn-save-rename, case-rename-error, todo-more (phone: the jump list behind one line),
  data-do-first (attribute on the overview block while the line is shown), LiveRerun and JudgeNotRun (stubs that make GET case say rerun_available true), rerun-unavailable (the sentence that replaces the rerun button when no item says rerun_available), input-title (the case name field beside Analyze).
T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
T-136 r3 (tests/e2e/test_held_quote_gate.py): btn-write-summary-case ('Write the summary' on the case-level places: the 'Ready to export?' and 'Second AI check' steps of the case rail and the 'How the AI was checked' rows; opens the entry's summary box like the blocker row's btn-gate-write-summary). A held re-picked quote offers btn-rerun-judge only until a rerun gave no answer (the blocker's rerun_no_answer).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:35.022Z

**tool call — Bash**
````
{
 "command": "grep -n \"def run_case\" -A22 tests/unit/test_api_routes.py; grep -n \"def update_item\" -A12 app/db/db.py | head -30"
}
````

### User / tool · 2026-11-02T20:28:35.143Z

**tool result**
````
34:def run_case(c, text=None):
35-    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
36-    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
37-    wait_ready(c, tok)
38-    return tok
39-
40-
41-def test_health_shape(env):
42-    h = env[1].get("/api/health").json()
43-    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
44-    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)
45-
46-
47-def test_create_sample_is_code_only_with_gap_flag(env):
48-    _, c = env
49-    r = c.post("/api/cases", json={"sample": True})
50-    b = r.json()
51-    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
52-    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
53-    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest
54-
55-
56-def test_error_format_and_unknown_token(env):
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
205-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
206-    table, found = _find(conn, item_id, case)
207-    bad = set(fields) - _cols(conn, table)
208-    if bad:
209-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
210-    fields["updated_at"] = now
211-    sets = ", ".join(f"{k}=?" for k in fields)
212-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:48.936Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_d066_compare_confirm.py",
 "content": "\"\"\"T-179 / D-066 (GATE-M3 product-manager major): accepting an item the second check disputed (judge verdict disagrees, unsupported or partially, or a\nJUDGE_DISAGREES reason) needs the explicit `compared: true` statement (\"I compared it with the quote\"). Without it: 422 COMPARE_REQUIRED, nothing written.\nWith it: 200, and the statement is kept in the accept event. Batch accept never includes such an item. An item nobody disputed accepts as before.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit.test_api_routes import run_case\n\nCASES = [(\"partially\", \"JUDGE_PARTIAL\"), (\"unsupported\", \"JUDGE_UNSUPPORTED\"), (\"disagrees\", \"JUDGE_DISAGREES\")]\n\n\n@pytest.fixture\ndef env(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    db = str(tmp_path / \"d066.sqlite\")\n    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef _dispute(db, tok, item_id, verdict, code, *, reasons=True):\n    conn = DB.connect(db)\n    try:\n        it = DB.get_item(conn, item_id, tok)\n        lad = {**(it.get(\"ladder\") or {}), \"judge\": {\"model\": \"m\", \"prompt_version\": \"j1\", \"call_id\": None, \"verdict\": verdict, \"reason_code\": None}}\n        DB.update_item(conn, item_id, now=9e9, case=tok, state=\"needs_review\", state_reasons=[code] if reasons else [], ladder=lad)\n    finally:\n        conn.close()\n\n\ndef _events(db, tok, item_id):\n    conn = DB.connect(db)\n    try:\n        return DB.list_events(conn, tok, item_id)\n    finally:\n        conn.close()\n\n\ndef _post(c, tok, item_id, **body):\n    return c.post(f\"/api/cases/{tok}/items/{item_id}/review\", json={\"action\": \"accept\", **body})\n\n\n@pytest.mark.parametrize(\"verdict,code\", CASES)\ndef test_accept_of_a_disputed_entry_needs_the_compare(env, verdict, code):\n    db, c = env\n    tok = run_case(c)\n    _dispute(db, tok, \"e2\", verdict, code)\n    r = _post(c, tok, \"e2\")\n    assert r.status_code == 422, r.text\n    err = r.json()[\"error\"] if \"error\" in r.json() else r.json()\n    blob = r.text\n    assert \"COMPARE_REQUIRED\" in blob and \"compared\" in blob and verdict in blob\n    assert DB.get_item(DB.connect(db), \"e2\", tok)[\"review_status\"] == \"pending\"      # nothing written\n    assert [e for e in _events(db, tok, \"e2\") if e[\"action\"] == \"accept\"] == []\n    assert _post(c, tok, \"e2\", compared=False).status_code == 422\n    ok = _post(c, tok, \"e2\", compared=True)\n    assert ok.status_code == 200 and ok.json()[\"item\"][\"review_status\"] == \"accepted\"\n    acc = [e for e in _events(db, tok, \"e2\") if e[\"action\"] == \"accept\"]\n    assert len(acc) == 1 and acc[0][\"after\"][\"compared\"][\"at\"], acc          # kept on the review event\n\n\ndef test_the_verdict_alone_or_the_reason_alone_counts(env):\n    db, c = env\n    tok = run_case(c)\n    conn = DB.connect(db)\n    DB.update_item(conn, \"e3\", now=9e9, case=tok, state=\"needs_review\", state_reasons=[\"JUDGE_DISAGREES\"])      # reason only\n    _dispute(db, tok, \"e4\", \"unsupported\", \"JUDGE_UNSUPPORTED\", reasons=False)                                     # verdict only\n    conn.close()\n    assert _post(c, tok, \"e3\").status_code == 422\n    assert _post(c, tok, \"e4\").status_code == 422\n    assert _post(c, tok, \"e3\", compared=True).status_code == 200\n\n\ndef test_an_undisputed_item_accepts_as_before_and_a_bad_compared_is_refused(env):\n    db, c = env\n    tok = run_case(c)\n    assert _post(c, tok, \"e1\").status_code == 200\n    assert not [e for e in _events(db, tok, \"e1\") if e[\"action\"] == \"accept\" and \"compared\" in (e[\"after\"] or {})]       # nothing to compare: nothing recorded\n    assert _post(c, tok, \"e5\", compared=\"yes\").status_code == 422\n    # unsure / unavailable are not an objection\n    _dispute(db, tok, \"e6\", \"unsure\", \"JUDGE_UNSURE\")\n    assert _post(c, tok, \"e6\").status_code == 200\n\n\ndef test_dismiss_and_reset_need_no_compare(env):\n    db, c = env\n    tok = run_case(c)\n    _dispute(db, tok, \"e2\", \"partially\", \"JUDGE_PARTIAL\")\n    assert c.post(f\"/api/cases/{tok}/items/e2/review\", json={\"action\": \"dismiss\"}).status_code == 200\n    assert c.post(f\"/api/cases/{tok}/items/e2/review\", json={\"action\": \"reset\"}).status_code == 200\n\n\ndef test_batch_accept_excludes_a_disputed_item(env):\n    db, c = env\n    tok = run_case(c)\n    _dispute(db, tok, \"e2\", \"partially\", \"JUDGE_PARTIAL\")\n    conn = DB.connect(db)\n    DB.update_item(conn, \"e3\", now=9e9, case=tok, state=\"verified\", state_reasons=[], ladder={**DB.get_item(conn, \"e3\", tok)[\"ladder\"], \"judge\": {\"verdict\": \"disagrees\"}})      # even a \"verified\" row with the verdict is out\n    conn.close()\n    r = c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [\"e1\", \"e2\", \"e3\"]})\n    assert r.status_code == 422 and \"judge_disputed\" in r.text\n    rej = {x[\"id\"]: x[\"reason\"] for x in r.json()[\"error\"][\"detail\"][\"rejected\"]} if \"error\" in r.json() else {}\n    if rej:\n        assert rej.get(\"e2\") == \"judge_disputed\" and rej.get(\"e3\") == \"judge_disputed\" and \"e1\" not in rej\n    assert DB.get_item(DB.connect(db), \"e1\", tok)[\"review_status\"] == \"pending\"      # all or nothing\n    assert c.post(f\"/api/cases/{tok}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [\"e1\"]}).status_code == 200\n"
}
````

### User / tool · 2026-11-02T20:28:48.987Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_d066_compare_confirm.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:50.299Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_d066_compare_confirm.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T20:28:51.548Z

**tool result**
````
        tok = run_case(c)
>       _dispute(db, tok, "e2", verdict, code)

tests/unit/test_d066_compare_confirm.py:49: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/unit/test_d066_compare_confirm.py:28: in _dispute
    DB.update_item(conn, item_id, now=9e9, case=tok, state="needs_review", state_reasons=[code] if reasons else [], ladder=lad)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

conn = <sqlite3.Connection object at 0x1090246d0>, item_id = 'e2'
now = 9000000000.0, case = 'XPaoOzCrYRVGikx4yGphOA'
fields = {'state': 'needs_review', 'state_reasons': ['JUDGE_PARTIAL'], 'ladder_json': {'backend': 'fixture', 'code_checks': {'d...benzaprine 10 mg prescribed; follow up with PCP in 1 week; ER charges $6,240.'}, 'prompt_version': 'extract_v1'}, ...}}

    def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
        """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
        fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
        locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
        if locked & set(fields):
            raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
        table, found = _find(conn, item_id, case)
        bad = set(fields) - _cols(conn, table)
        if bad:
>           raise ValueError(f"unknown {table} fields {sorted(bad)}")
E           ValueError: unknown entries fields ['state_reasons']

app/db/db.py:209: ValueError
=========================== short test summary info ============================
FAILED tests/unit/test_d066_compare_confirm.py::test_accept_of_a_disputed_entry_needs_the_compare[partially-JUDGE_PARTIAL]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 0.90s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:54.096Z

**tool call — Bash**
````
{
 "command": "sed -i 's/state_reasons=\\[code\\] if reasons else \\[\\]/reasons=[code] if reasons else []/; s/state_reasons=\\[\"JUDGE_DISAGREES\"\\]/reasons=[\"JUDGE_DISAGREES\"]/; s/state_reasons=\\[\\], ladder/reasons=[], ladder/' tests/unit/test_d066_compare_confirm.py && grep -n \"reasons\" app/db/db.py | head -5; .venv/bin/python -m pytest tests/unit/test_d066_compare_confirm.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T20:28:55.550Z

**tool result**
````
sed: 2: "tests/unit/test_d066_co ...": undefined label 'ests/unit/test_d066_compare_confirm.py'
        tok = run_case(c)
>       _dispute(db, tok, "e2", verdict, code)

tests/unit/test_d066_compare_confirm.py:49: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/unit/test_d066_compare_confirm.py:28: in _dispute
    DB.update_item(conn, item_id, now=9e9, case=tok, state="needs_review", state_reasons=[code] if reasons else [], ladder=lad)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

conn = <sqlite3.Connection object at 0x10ae309a0>, item_id = 'e2'
now = 9000000000.0, case = 'bsKwVeunNT8DYT6r5EKKzg'
fields = {'state': 'needs_review', 'state_reasons': ['JUDGE_PARTIAL'], 'ladder_json': {'backend': 'fixture', 'code_checks': {'d...benzaprine 10 mg prescribed; follow up with PCP in 1 week; ER charges $6,240.'}, 'prompt_version': 'extract_v1'}, ...}}

    def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
        """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
        fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
        locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
        if locked & set(fields):
            raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
        table, found = _find(conn, item_id, case)
        bad = set(fields) - _cols(conn, table)
        if bad:
>           raise ValueError(f"unknown {table} fields {sorted(bad)}")
E           ValueError: unknown entries fields ['state_reasons']

app/db/db.py:209: ValueError
=========================== short test summary info ============================
FAILED tests/unit/test_d066_compare_confirm.py::test_accept_of_a_disputed_entry_needs_the_compare[partially-JUDGE_PARTIAL]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 1.07s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:58.442Z

**tool call — Bash**
````
{
 "command": "grep -n \"reasons\" app/db/*.py | head -8"
}
````

### User / tool · 2026-11-02T20:28:58.526Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:01.783Z

**tool call — Bash**
````
{
 "command": "ls app/db; grep -rn \"state_reasons\" app/db | head -5; grep -n \"state_reasons\" app/backend/store.py | head -5"
}
````

### User / tool · 2026-11-02T20:29:01.887Z

**tool result**
````
__init__.py
__pycache__
db.py
schema.sql
app/db/schema.sql:22:  state TEXT, state_reasons_json TEXT,
app/db/schema.sql:31:  state TEXT, state_reasons_json TEXT,
app/db/schema.sql:42:  state TEXT, state_reasons_json TEXT,
134:            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
145:            d["edit_state_reasons"] = list(e.get("state_reasons") or [])          # T-134: why her edit is still marked for review; the notes keep it after she accepts
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:07.806Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/state_reasons=\\[code\\] if reasons else \\[\\]/state_reasons_json=[code] if reasons else []/; s/reasons=\\[\"JUDGE_DISAGREES\"\\]/state_reasons_json=[\"JUDGE_DISAGREES\"]/; s/reasons=\\[\\], ladder/state_reasons_json=[], ladder/' tests/unit/test_d066_compare_confirm.py && sed -i '' 's/state_state_reasons_json/state_reasons_json/g; s/state_state/state_/g' tests/unit/test_d066_compare_confirm.py; grep -n \"reasons\" tests/unit/test_d066_compare_confirm.py; .venv/bin/python -m pytest tests/unit/test_d066_compare_confirm.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T20:29:11.004Z

**tool result**
````
23:def _dispute(db, tok, item_id, verdict, code, *, reasons=True):
28:        DB.update_item(conn, item_id, now=9e9, case=tok, state="needs_review", state_reasons_json=[code] if reasons else [], ladder=lad)
68:    DB.update_item(conn, "e3", now=9e9, case=tok, state="needs_review", state_reasons_json=["JUDGE_DISAGREES"])      # reason only
69:    _dispute(db, tok, "e4", "unsupported", "JUDGE_UNSUPPORTED", reasons=False)                                     # verdict only
100:    DB.update_item(conn, "e3", now=9e9, case=tok, state="verified", state_reasons_json=[], ladder={**DB.get_item(conn, "e3", tok)["ladder"], "judge": {"verdict": "disagrees"}})      # even a "verified" row with the verdict is out
.......                                                                  [100%]
7 passed in 2.82s
[This command modified 1 file you've previously read: tests/unit/test_d066_compare_confirm.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:24.910Z

**tool call — Bash**
````
{
 "command": "sed -n 330,454p app/frontend/review.js | cut -c1-420"
}
````

### User / tool · 2026-11-02T20:29:24.995Z

**tool result**
````
  const refusals = {};       // id -> {message}
  function paintRefusal(root, id, edit) {
    const r = refusals[id], box = root.querySelector(".rv-refused");
    if (!box) return;
    ZL.clear(box); box.hidden = !r;
    if (!r) return;
    box.append(el("p", { class: "rv-refused-msg", "data-testid": "accept-refused-msg" }, el("strong", {}, "Not accepted. "), r.message),
      r.code === "EDIT_QUOTE"   // T-104: the first failing check is on the quote, so the fix is the quote, not the summary
        ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-quote", "aria-label": QUOTE + " for " + r.label, onclick: changeQuote(r.id) }, QUOTE)
        : edit ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
  }
  // T-158: the refused-Accept box must end up fully on screen, clear of the sticky header. The layout is still moving right after the click (the case trace and the panels repaint, the sticky
  // header can change height, the list re-renders and the box node is rebuilt), so one scroll at click time is not enough: scroll now, again on the next two frames, and once more after the
  // repaints have settled. Each pass looks the box up again by item id and does nothing when it is already inside the viewport.
  function showRefusalInView(id) {
    const pass = () => {
      const row = document.querySelector('[data-controls-for="' + id + '"]'), box = row && row.querySelector(".rv-refused:not([hidden])");
      if (!box) return;
      const hdr = document.querySelector('[data-testid="app-header"]'), top = hdr ? Math.max(hdr.getBoundingClientRect().bottom, 0) + 8 : 60, r = box.getBoundingClientRect();
      if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16);
      else if (r.top < top) window.scrollBy(0, r.top - top);
    };
    pass(); requestAnimationFrame(() => { pass(); requestAnimationFrame(pass); }); setTimeout(pass, 250); setTimeout(pass, 700);
  }
  RV.clearRefusal = (id) => { if (refusals[id]) { delete refusals[id]; repaintRefusal(id); } };   // T-108: a saved quote change ends the refused-Accept box at once
  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
  const DATE_FIRST = "Confirm the date first.", DATE_WHY = "This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.";
  RV.needsDate = (item, kind) => kind === "entry" && !item.date;
  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
    const row = document.querySelector('[data-testid="dates-to-confirm"] [data-entry-id="' + id + '"]');
    const t = row && (row.querySelector('[data-testid="confirm-date"]:checked') || row.querySelector('[data-testid="confirm-date"]') || row);
    const box = document.querySelector('[data-testid="dates-to-confirm"]');
    const f = t || box; if (!f) return;
    if (!f.hasAttribute("tabindex") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1");
    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: "center" });
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    if (body.action === "accept" && !body.confirm && found && found.kind === "amount" && found.item.confirm_required && found.item.flag && ZL.confirmCharge) {   // D-059 (T-154): a flagged charge is counted only after she names the flag
      busy.add(id); const ok = await ZL.confirmCharge(found.item.flag, found.item); busy.delete(id);
      if (!ok) return false;
      body = Object.assign({}, body, { confirm: found.item.flag.confirm_with });
    }
    busy.add(id);
    const plan = o.advance ? RV.planAdvance(id) : null;   // the list she is working in, read before the repaint
    const slot = body.action === "dismiss" ? slotOf(id) : null;   // T-166 F5: where the row sits now, for its placeholder
    try {
      const resp = await ZL.api.review(c.token, id, body);
      comparePrompt.delete(id);
      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      if (body.action === "edit" && found && found.kind === "entry") rechecks[id] = recheckSentence(resp); else delete rechecks[id];
      if (body.action === "dismiss" && found && found.kind === "entry") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo
      else if (body.action === "dismiss" && found) ZL.dismissedOpenBy[found.kind === "amount" ? "amounts" : "flags"] = true;   // a flag or amount does the same in its own panel
      if (body.action === "dismiss" && found) addGhost(id, found.item, slot); else if (body.action === "reset") dropGhost(id, false);
      ZL.state.applyReview(resp);
      if (rechecks[id]) RV.say(rechecks[id]);
      const left = ZL.progressOf(RV.caseNow() || c).left;   // T-166 F9: the one open count (the same number as the header: undecided items, including an edit still to check)
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, plan } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea'), typed = ta0 ? ta0.value : "";
        const toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, RV.asTyped((e.message || "That edit is not allowed.") + toks, d.tokens, typed));
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
        refusals[id] = { id, code: nextCode(e), message: RV.asTyped(e.message || "The summary fails a check. Edit the summary to match the quote.", e.detail && e.detail.tokens, (found && found.item && ((found.item.edited && found.item.edited.summary) || found.item.summary)) || ""), label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
        showRefusalInView(id);
      } else if (e && String(e.code).toUpperCase() === "CONFIRM_REQUIRED" && body.action === "accept" && !body.confirm && ZL.confirmCharge) {   // D-059: the page did not know the charge was flagged; the server's flag opens the same confirm
        const d = e.detail || {}; busy.delete(id);
        const ok = await ZL.confirmCharge({ flag: d.flag, name: d.name, message: d.message || e.message, confirm_with: d.confirm_with }, found && found.item);
        if (ok) return RV.act(id, Object.assign({}, body, { confirm: d.confirm_with }), o);
        return false;
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
    } finally { busy.delete(id); }
  };

  // T-162 (T-146): a re-run that disagreed with or failed on a decided item kept it as it was and left a note; the server's sentence is shown beside the item and in its trace.
  RV.rerunNote = (item) => el("p", { class: "rv-reason-line rv-rerun-note", role: "note", "data-testid": "rerun-note" }, el("strong", {}, "Re-run: "), item.rerun_note);
  RV.rerunNoteFor = (id) => { const c = RV.caseNow(), f = c && RV.find(c, id); return f && f.item.rerun_note ? RV.rerunNote(f.item) : null; };

  // T-166 F12: Undo (or r) on an item she edited would throw her wording away with no way back. It asks first, inline, with Keep as the focused answer; nothing is sent until she says Discard.
  const discardOpen = new Set();
  const wordsOf = (item) => (item.edited && item.edited.original_excerpt != null && item.edited.original_summary == null ? "your change to the quote" : "your wording");
  function discardBox(id, item) {
    const keep = () => { discardOpen.delete(id); const root = document.querySelector('[data-controls-for="' + id + '"]'), b = root && root.querySelector('[data-testid="discard-confirm"]'); if (b) b.remove(); const r = root && root.querySelector('[data-action="reset"]'); if (r) r.focus(); RV.say("Kept " + wordsOf(item) + "."); };
    const w = wordsOf(item), box = el("div", { class: "rv-help rv-discard", role: "group", "aria-label": "Confirm undo", "data-testid": "discard-confirm" },
      el("p", {}, "Undo will throw away " + w + " and bring back the original. Discard " + w + "?"),
      el("div", { class: "rv-actions" },
        el("button", { type: "button", class: "btn", "data-testid": "btn-discard-edit", onclick: () => { discardOpen.delete(id); RV.act(id, { action: "reset" }, { focus: "reset" }); } }, "Discard " + w),
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-keep-edit", onclick: keep }, "Keep " + w)));
    box.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.stopPropagation(); keep(); } });
    return box;
  }
  RV.reset = function (id) {   // the one way back for a decided item (the Undo button and the r key)
    const c = RV.caseNow(), f = c && RV.find(c, id);
    if (f && f.item.edited && !discardOpen.has(id)) {
      discardOpen.add(id);
      const root = document.querySelector('[data-controls-for="' + id + '"]'); if (!root) return RV.act(id, { action: "reset" }, { focus: "reset" });
      const b = discardBox(id, f.item); root.append(b); const k = b.querySelector('[data-testid="btn-keep-edit"]'); k.focus({ preventScroll: true }); k.scrollIntoView({ block: "nearest" });
      RV.say("Undo will throw away " + wordsOf(f.item) + ". Press Keep to cancel, or Discard to go on.");
      return Promise.resolve(false);
    }
    if (f && f.item.edited && discardOpen.has(id)) { const k = document.querySelector('[data-controls-for="' + id + '"] [data-testid="btn-keep-edit"]'); if (k) k.focus(); return Promise.resolve(false); }
    return RV.act(id, { action: "reset" }, { focus: "reset" });
  };

  // ---- controls
  RV.controls = function (item, kind) {
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:28.607Z

**tool call — Bash**
````
{
 "command": "sed -n 520,540p app/frontend/review.js | cut -c1-500; sed -n 596,652p app/frontend/review.js | cut -c1-360; sed -n 1,140p app/frontend/batch.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T20:29:28.716Z

**tool result**
````
        const both = !isFlag && !!(ev.submitter && ev.submitter.getAttribute("data-testid") === "btn-save-accept");
        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: both ? null : "edit" })
          .then((ok) => (ok && both ? RV.act(id, { action: "accept" }, { focus: "accept" }) : null))
          .finally(() => { if (h && h.isConnected) h.textContent = was; });
      } },
        !isFlag && item.edited && item.edited.original_summary ? el("p", { class: "rv-original muted small", "data-testid": "edit-original" }, el("strong", {}, "Original wording: "), item.edited.original_summary) : null,
        el("label", { class: "rv-label" }, hint, ta),
        isFlag ? null : el("p", { class: "rv-help rv-recheck-hint", "data-testid": "edit-recheck-hint" }, "When you save, the code checks every number, date and negation in your wording against the quote, then a second AI check reads it. Nothing is added to the letter until it passes."),
        el("div", { class: "rv-actions" },
          isFlag ? null : el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-accept", title: "Saves your wording and accepts it, saying it matches the quote beside it" }, "Save and accept"),
          el("button", { type: "submit", class: "btn" + (isFlag ? " btn--primary" : ""), "data-testid": "btn-save-edit" }, "Save"),
          el("button", { type: "button", class: "btn", "data-testid": "btn-cancel-edit", onclick: () => toggleEdit(false) }, "Cancel")));
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
      });
      root.append(form);
      var toggleEdit = function (open) {
        d.open = open; form.hidden = !open;
        if (open) ta.focus(); else { const b = bar.querySelector('[data-action="edit"]'); if (b) b.focus(); }
      };
    }
    if (key === "n" || key === "x") {   // T-166 F6: n = the first item that still needs a decision, from any row; x = Export. Both only while an item row has focus (WCAG 2.1.4), like every letter key
      ev.preventDefault();
      if (key === "x") { focusExport("Export. Press Enter to open it."); return; }
      const left = ZL.progressOf(c).left;
      if (!left) { focusExport("Nothing left to decide. Export is next."); return; }
      if (RV.focusFirstPending()) { const at = document.activeElement, f = at && at.getAttribute && RV.find(c, at.getAttribute("data-item-id")), g = at && at.closest && at.closest(GROUP);
        RV.say("First open item: " + (g ? groupName(g) + ", " : "") + (f ? RV.ghostLabel(f.item) : "") + ". " + left + (left === 1 ? " item is" : " items are") + " open."); }
      return;
    }
    if (ev.key.length !== 1 || !"aedro".includes(key)) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    if ((key === "a" || key === "d" || key === "e") && f.item.review_status === "dismissed") {   // T-060 r5 (paralegal M1): one key never undoes a dismissal; only Undo (or r) does
      RV.say("This item is dismissed. Press r or Undo to bring it back first.");
      return;
    }
    if (key === "a" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) {   // as the Accept button: a decided item is not decided twice (T-154: a confirmed flagged charge must not reopen "not counted" or write a second accept)
      RV.say((f.kind === "amount" && f.item.kind !== "charge" ? "Kept in notes" : f.item.review_status === "edited" ? "Edited" : "Accepted") + " already. Use Undo to change it.");
      return;
    }
    if (key === "a" && ZL.editToCheck(f.item)) { askCompare(id); return; }   // T-136 (paralegal F1): one key press never records "I compared it with the quote"; the button (click, or Enter on it) does
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.reset(id); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (!c || !mountEl) return; const sec = mountSection(mountEl, name); try { render(sec, c); } catch (err) { ZL.panelFailed(sec, name, err); } });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
      rowEl.setAttribute("data-item-id", entry.id); rowEl.setAttribute("data-review", entry.review_status || "pending");
      if (ZL.editToCheck(entry)) rowEl.setAttribute("data-edit-check", ""); else rowEl.removeAttribute("data-edit-check");
      if (!rowEl.hasAttribute("tabindex")) rowEl.setAttribute("tabindex", "0");
      const ctrl = RV.controls(entry, "entry"); rowEl.append(ctrl);
      const au = ctrl.querySelector(".rv-audit"), links = rowEl.querySelector(".row-actions");
      if (au && links) links.append(au);   // Why? / Open record / Change quote / Audit are one group of links on the right of the row
      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
        const head = rowEl.querySelector(".entry-head") || rowEl;
        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
      }
    });
  }
})();
/* Batch accept for verified entries only (T-055, D-031). Button + Shift+A; the server enforces "verified pending entries only" (422 otherwise).
   Never touches amounts or flags. Undo resets exactly the entries this batch accepted. Any error (including 404/405) shows a plain message and accepts nothing: no per-item fallback, so the server's verified-only check cannot be bypassed (T-065). */
(function () {
  const ZL = window.ZL, RV = ZL.rv, el = ZL.el;
  let last = null;      // {token, ids} of the most recent batch, for Undo
  let busy = false;
  let refused = null;   // {token, message, rows:[{id, why}]}: the last batch the server refused for a failing code check (D-051); nothing was accepted
  const eligible = (c) => (c.entries || []).filter((e) => e.date && e.state === "verified" && (e.review_status || "pending") === "pending");
  // D-041: entries still without a confirmed date are never part of a batch; say how many were left out.
  const skippedUndated = (c) => (c.undated_entries || []).concat((c.entries || []).filter((e) => !e.date)).filter((e) => (e.review_status || "pending") === "pending").length;
  // D-059 (T-154): charges are never part of a batch (the server refuses a batch that names one); say so beside the button while any charge still waits.
  const pendingCharges = (c) => (c.amounts || []).filter((a) => a.kind === "charge" && (a.review_status || "pending") === "pending").length;
  const chargesText = (n) => (n === 1 ? "1 charge is" : n + " charges are") + " not part of this: charges are accepted one at a time, in the Charges panel.";
  const skipText = (n) => n + (n === 1 ? " undated entry was" : " undated entries were") + " skipped: confirm the date first (Dates to confirm).";

  async function refresh(token) { ZL.state.set({ case: await ZL.api.getCase(token) }); }

  async function acceptAll() {
    const c = RV.caseNow(); if (!c || busy) return;
    const ids = eligible(c).map((e) => e.id), skipped = skippedUndated(c);
    if (!ids.length) { if (skipped) RV.say("Nothing to accept. " + skipText(skipped)); return; }
    busy = true;
    try {
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "accept", item_ids: ids });
      if (r.status >= 400) {
        const code = r.body && r.body.error && r.body.error.code;
        if (String(code).toUpperCase() === "DATE_UNCONFIRMED") { RV.say("Confirm the date first. An entry in this batch has no confirmed date, so nothing was accepted. Pick its date in Dates to confirm, then try again.", true); return; }
        if (String(code).toUpperCase() === "CODE_CHECK_FAILED") {   // D-051 (T-098 r2): the whole batch is refused; say which items and why, with an Edit action on each
          const d = (r.body.error.detail || {}), list = Array.isArray(d.rejected) ? d.rejected : [];
          refused = { token: c.token, message: r.body.error.message || "Nothing was accepted: a summary fails a check.", rows: list.map((x) => ({ id: x.id || x.item_id, why: x.why || "", code: x.next_action && x.next_action.code ? String(x.next_action.code).to
          paintBar(c); RV.say(refused.message, true);
          const f = document.querySelector('[data-testid="batch-refused-msg"]'); if (f) { f.setAttribute("tabindex", "-1"); f.focus(); }
          return;
        }
        if (String(code).toUpperCase() === "CHARGES_NOT_BATCHED") { RV.say((r.body.error.message || "Charges are accepted one at a time, so a charge cannot be part of a batch.") + " Nothing was accepted.", true); return; }
        const plain = (r.status === 404 || r.status === 405) ? "Accept all could not run on this server, so nothing was accepted. Accept entries one at a time instead." : null;
        RV.say(plain || RV.errMsg(r, "The batch was refused; nothing was accepted."), true); return;
      }
      refused = null;
      last = { token: c.token, ids };
      await refresh(c.token);
      RV.say("Accepted " + ids.length + " verified " + (ids.length === 1 ? "entry" : "entries") + ". Undo is available." + (skipped ? " " + skipText(skipped) : ""));
      const u = document.querySelector('[data-testid="btn-undo-batch"]'); if (u) u.focus();
    } catch (e) { RV.say((e && e.message) || "The batch did not finish.", true); try { await refresh(c.token); } catch (_) { /* keep state */ } }
    finally { busy = false; }
  }
  async function undo() {
    const c = RV.caseNow(); if (!c || !last || last.token !== c.token || busy) return;
    const ids = last.ids.filter((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
    busy = true;
    try {
      if (ids.length) {
        const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/review/batch", { action: "reset", item_ids: ids });
        if (r.status >= 400) { RV.say(RV.errMsg(r, "Undo was refused."), true); return; }
      }
      const n = ids.length; last = null; await refresh(c.token);
      RV.say("Undone: " + n + " " + (n === 1 ? "entry" : "entries") + " back to not reviewed.");
    } catch (e) { RV.say((e && e.message) || "Undo did not finish.", true); } finally { busy = false; }
  }

  // Items the server named that are still waiting (an item the paralegal has since edited, accepted or dismissed drops out of the list).
  function refusedRows(c) {
    if (!refused || refused.token !== c.token) return [];
    return refused.rows.filter((x) => { const f = RV.find(c, x.id); return f && (f.item.review_status || "pending") === "pending"; });
  }
  function refusedBox(c) {
    const rows = refusedRows(c);
    if (!rows.length) return null;
    return el("div", { class: "rv-refused rv-refused-batch", role: "alert", "data-testid": "batch-refused" },
      el("p", { class: "rv-refused-msg", "data-testid": "batch-refused-msg" }, el("strong", {}, "Nothing was accepted. "), refused.rows.length ? (rows.some((x) => x.code === "EDIT_QUOTE")   // T-104: a quote check is not a summary problem
        ? (rows.length === 1 ? "One entry fails a check, so the whole batch was refused. Fix it, then accept again." : rows.length + " entries fail a check, so the whole batch was refused. Fix them, then accept again.")
        : rows.length === 1 ? "One summary fails a check, so the whole batch was refused. Edit it, then accept again." : rows.length + " summaries fail a check, so the whole batch was refused. Edit them, then accept again.") : refused.message),
      el("ul", { class: "rv-refused-list" }, rows.map((x) => {
        const name = ZL.stepper && ZL.stepper.label ? ZL.stepper.label(x.id) : x.id;
        return el("li", { "data-testid": "batch-refused-item", "data-refused-id": x.id },
          el("span", { class: "rv-refused-name" }, name), x.why ? el("span", { class: "rv-refused-why" }, " " + x.why) : null, " ",
          x.code === "EDIT_QUOTE" && ZL.stepper && ZL.stepper.changeQuote ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-batch-refused-quote", "aria-label": "Change the quote for " + name, onclick: () => ZL.stepper.changeQuo
          : ZL.stepper && ZL.stepper.editItem ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-batch-refused-edit", "aria-label": "Edit the summary for " + name, onclick: () => ZL.stepper.editItem(x.id) }, "Edit the summary") 
      })));
  }
  const HELP = "Entries only. Charges are accepted one at a time; flags and anything marked needs review always need your own decision.";
  function bar(c) {
    const n = eligible(c).length, sk = skippedUndated(c), pc = pendingCharges(c);
    const undoable = last && last.token === c.token && last.ids.some((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
    return el("div", { class: "rv-batchbar", "data-testid": "batch-bar" },
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-accept-verified", disabled: n === 0, "aria-describedby": "batch-help", title: HELP, onclick: acceptAll }, "Accept all verified entries (" + n + ")"),
      undoable ? el("button", { type: "button", class: "btn", "data-testid": "btn-undo-batch", onclick: undo }, "Undo last batch (" + last.ids.length + ")") : null,
      sk ? el("span", { class: "rv-help rv-blocked", "data-testid": "batch-skipped-note" }, skipText(sk)) : null,
      pc ? el("span", { class: "rv-help rv-blocked", "data-testid": "batch-charges-note" }, chargesText(pc)) : null,
      el("span", { class: "rv-sr", id: "batch-help" }, HELP),
      refusedBox(c));
  }
  function paintBar(c) {
    const wrap = document.querySelector('[data-testid="timeline"]'), old = wrap && wrap.querySelector(".toolbar > .rv-batchbar");
    if (old) old.replaceWith(bar(c));
  }
  RV.registerPanel("batch", (root, c) => {
    ZL.clear(root); root.className = "rv-batchhost";
    const wrap = root.closest('[data-testid="timeline"]'), tb = wrap && wrap.querySelector(".toolbar");
    const b = bar(c);
    if (tb) { const old = tb.querySelector(":scope > .rv-batchbar"); if (old) old.remove(); tb.insertBefore(b, tb.querySelector(".toolbar-sort")); } else root.append(b);   // the button sits in the Timeline toolbar (T-060 r3)
  });
  // Shift+A (WCAG 2.1.4, T-060 blocker): only while focus is on an item row, and never straight away. It opens a confirmation that names the count;
  // the Accept all button is a deliberate click on a labelled control and keeps its one-step behaviour.
  let dlg = null;
  function askFirst(n) {
    if (!dlg) {
      dlg = el("dialog", { class: "dlg dlg--sm", "data-testid": "batch-confirm", "aria-labelledby": "bc-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "bc-title" })),
        el("div", { class: "dlg-body" }, el("p", { id: "bc-text" }), el("p", { class: "muted" }, "Charges (accepted one at a time), flags and anything marked needs review are not part of this. You can undo it straight afterwards.")),
        el("div", { class: "dlg-foot" },
          el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-batch-confirm", id: "bc-ok" }),
          el("button", { type: "button", class: "btn", "data-testid": "btn-batch-cancel", id: "bc-cancel" }, "Cancel")));
      document.body.append(dlg);
    }
    const word = n === 1 ? "entry" : "entries";
    dlg.querySelector("#bc-title").textContent = "Accept " + n + " verified " + word + "?";
    dlg.querySelector("#bc-text").textContent = "The code and the second AI check found support for " + (n === 1 ? "this entry" : "these " + n + " entries") + ", but you have not decided on " + (n === 1 ? "it" : "them") + " one by one. Accepting puts " + (n ==
    dlg.querySelector("#bc-ok").textContent = "Accept " + n + " " + word;
    const back = document.activeElement;
    return new Promise((resolve) => {
      const done = (v) => { dlg.removeEventListener("close", onClose); dlg.querySelector("#bc-ok").onclick = dlg.querySelector("#bc-cancel").onclick = null; if (dlg.open) dlg.close(); if (back && back.isConnected) back.focus(); resolve(v); };
      const onClose = () => done(false);
      dlg.addEventListener("close", onClose);
      dlg.querySelector("#bc-ok").onclick = () => done(true);
      dlg.querySelector("#bc-cancel").onclick = () => done(false);
      dlg.showModal(); dlg.querySelector("#bc-cancel").focus();   // the safe answer has focus; Enter alone never accepts
    });
  }
  document.addEventListener("keydown", async (ev) => {
    if (ev.key !== "A" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target; if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    if (document.querySelector("dialog[open]") || !RV.itemRowOf(t)) return;   // not from Export, the header, a dialog or the page body
    ev.preventDefault();
    const c = RV.caseNow(); if (!c) return;
    const n = eligible(c).length;
    if (!n) { acceptAll(); return; }   // says why nothing happened (undated entries) without asking
    if (await askFirst(n)) acceptAll();
  });
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:32.335Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"accept\" app/frontend/stepper.js | cut -c1-240 | head -30; grep -n -i \"\\\"accept\\|data-action=\\\"accept\\|btn-accept\" app/frontend/charges.js app/frontend/flags.js app/frontend/timeline.js app/frontend/judges.js app/frontend/sidebyside.js | cut -c1-200 | head"
}
````

### User / tool · 2026-11-02T20:29:32.433Z

**tool result**
````
142:  // ---- "Run the second check again" (D-044): POST /rejudge for the accepted items whose second AI check never ran. One handler for every place that offers it
150:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
269:        if (obj) bits.push("Review the " + plural(obj, "item", "items") + " the AI objected to. Compare each one with its quote, then accept, edit or dismiss it.");
272:        if (unRerun) bits.push("The second AI check did not run on " + plural(unRerun, "item", "items") + ". Run it again; accepted items it never checked cannot go in the letter.");
278:        return { text: "Decide the " + plural(n, "detected charge", "detected charges") + ": accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.", label: "Go to the totals", go: () => gotoP
283:        return { text: "Decide the " + plural(n, "pending item", "pending items") + ": accept, edit or dismiss each one.", label: "Go to the first pending item", go: () => gotoFirstPending() };
289:        if (!b && !jnr.length && !held.length) return null;     // only whole-case blockers (nothing accepted, run state): the step's own action (go to the queue) says it
291:        if (jnr.length) parts.push(plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check again; if it still cannot answer, dismiss " + (jnr.length === 1 ?
442:    const decided = tr.review_status === "accepted" || tr.review_status === "edited";
452:    if (v.code === "accepted" && !wf) {
453:      if (notAIChecked) v.label = (tr.review_status === "edited" ? "Edited" : "Accepted") + " by you, not AI-checked";
454:      else if (skippedJudge) { v.code = "needs_attention"; v.label = "Accepted, second check missing"; }   // the gate (or an unloaded gate) holds it: not a green "Accepted by you"
456:    if (v.code === "accepted" && tr.review_status === "edited" && /^Accepted by you/.test(v.label || "")) v.label = v.label.replace(/^Accepted by you/, "Edited by you");   // an item the paralegal wrote reads "Edited", not "Accepted"
522:  S.HELD_NO_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary. The second AI check ran again and gave no answer on the new quote."
523:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed. The second AI check ran again and gave no answer on the new quotes.") + " Write the summary in your own words" + (n === 1 ?
524:  S.HELD_CAN_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote."
525:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed, and the second AI check has no answer on the new quotes.") + " Run the second check again, or write the summary in your own
677:    if (gate.ready || !(gate.blockers || []).length) blocked = { token: blocked.token, cleared: true, message: "Every accepted item now has its second check. Click Export again.", blockers: [] };
app/frontend/charges.js:77:  const isDone = (a) => a.review_status === "accepted" && !!(a.flag && a.flag.confirmed_at);
app/frontend/charges.js:235:      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Kept in the internal notes only; not in the letter or the total.") : null,
app/frontend/charges.js:265:        el("p", { class: "rv-total rv-total-main", "data-testid": "accepted-total", "aria-live": "polite" }, el("span", { class: "rv-total-label" }, "Accepted charges: "), 
app/frontend/judges.js:17:  const RS = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
app/frontend/judges.js:49:  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "ac
app/frontend/judges.js:183:        nBlock ? plural(nBlock, "accepted item", "accepted items") + " cannot go in the letter until the second AI check has run on " + (nBlock === 1 ? "it" : "them") + "."
app/frontend/timeline.js:7:  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
app/frontend/timeline.js:29:    const cmp = ZL.comparedEdit(e);   // T-136 r2 (paralegal F-1): she compared the edit with the quote and accepted it; "Needs review" beside "Accepted" would contradict h
app/frontend/timeline.js:162:      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:42.615Z

**tool call — Bash**
````
{
 "command": "grep -n \"api.review\\|RV.act(\" app/frontend/*.js | grep -v \"^app/frontend/review.js\" | cut -c1-220; grep -n \"RV.act(\" app/frontend/review.js | cut -c1-140; sed -n 40,62p app/frontend/dom.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T20:29:42.734Z

**tool result**
````
app/frontend/excerpt.js:39:      try { const resp = await ZL.api.review(ZL.state.get().token, entry.id, { action: "edit", edits: { excerpt: text } }); ZL.state.applyReview(resp); if (ZL.rv && ZL.rv.clearRefusal) ZL.rv.cl
app/frontend/charges.js:184:        try { resp = await ZL.api.review(c.token, id, body); }
207:    const undo = el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-undo-dismiss", "aria-label": "Undo dismissin
415:        if (ok) return RV.act(id, Object.assign({}, body, { confirm: d.confirm_with }), o);
435:        el("button", { type: "button", class: "btn", "data-testid": "btn-discard-edit", onclick: () => { discardOpen.delete(id); RV.act(
444:      const root = document.querySelector('[data-controls-for="' + id + '"]'); if (!root) return RV.act(id, { action: "reset" }, { focus
450:    return RV.act(id, { action: "reset" }, { focus: "reset" });
476:      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, { action: "accept
480:      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "
505:    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const
521:        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: both ? null : "edit" })
522:          .then((ok) => (ok && both ? RV.act(id, { action: "accept" }, { focus: "accept" }) : null))
618:    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
619:    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
    if (LIB_TITLE[+m[1]]) return LIB_TITLE[+m[1]];
    const t = m[2].replace(/_/g, " ").trim();
    return t ? t.charAt(0).toUpperCase() + t.slice(1) : name;
  };
  // ---- T-060 r5: ONE definition of "still waiting on the paralegal", used by the header, the Open-decisions strip, the Timeline chip, the keyboard flow and the export question.
  // An item is undecided when it is pending, or when she reworded it and it is still marked Needs review (the second check did not agree or did not run: her wording is in the
  // letter, but she has not yet compared it with the quote). A dismissed item is decided and is never counted as needing review.
  ZL.undecided = (i) => { const rs = (i && i.review_status) || "pending"; return rs === "pending" || ZL.editToCheck(i); };
  ZL.needsReview = (i) => !!i && i.state === "needs_review" && ZL.undecided(i);
  ZL.editToCheck = (i) => !!i && i.edit_to_check === true;   // T-136: the server's own flag (T-134): reworded summary OR quote, still Needs review, not yet accepted by her
  // How many edits are waiting for her comparison: the review's own count when the server sent it, else a count of the items that say so (the mock API).
  ZL.editCount = (c) => { const n = c && c.review && c.review.counts && c.review.counts.edit_to_check; return n != null ? n : [].concat(c.entries || [], c.undated_entries || []).filter(ZL.editToCheck).length; };
  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
  // the export gate (D-044) blocks it as soon as she accepts, until the check runs. One place for the rule, so a server flag can replace it.
  ZL.wordingEdited = (i) => !!i && !!i.edited && i.edited.summary != null;
  // T-136 r3 (T-134 r4): the server's own `second_check_pending` (live, AI-made, no second-check answer, not a rate) is what the page reads. The inference below is only for a server
  // (the mock API) that does not send the field.
  ZL.secondCheckPending = (i) => !!i && (i.second_check_pending !== undefined ? i.second_check_pending === true : i.ai_drafted === true && !ZL.wordingEdited(i) && (i.reasons || []).includes("JUDGE_UNAVAILABLE"));
  // She compared the edit with the quote and accepted it: the row says that, not "Needs review" (which would contradict her decision).
  ZL.comparedEdit = (i) => !!i && i.review_status === "accepted" && i.state === "needs_review" && !!i.edited && !ZL.editToCheck(i);
  // A date for a row: <time datetime="2026-01-09">January 9, 2026</time>. The machine date stays in the attribute (tests and assistive tech read it); the person reads the long form.
  ZL.timeEl = (iso, attrs) => ZL.el("time", Object.assign({ datetime: iso }, attrs || {}), ZL.fmtDate(iso));
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:00.633Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/frontend/dom.js'\ns=open(p).read()\nanchor=\"  // She compared the edit with the quote and accepted it:\"\nadd='''  // T-179 / D-066: the second check disputed this item (verdict partially | unsupported | disagrees, or a JUDGE_PARTIAL / JUDGE_UNSUPPORTED / JUDGE_DISAGREES reason). Accepting it needs her explicit\n  // \"I compared it with the quote\" (the server answers 422 COMPARE_REQUIRED without it). ZL.judgeDispute returns the verdict word or null; ZL.needsCompare is true while the item is still open.\n  const DISPUTE_REASON = { JUDGE_PARTIAL: \"partially\", JUDGE_UNSUPPORTED: \"unsupported\", JUDGE_DISAGREES: \"disagrees\" };\n  ZL.judgeDispute = (i) => {\n    const j = i && i.ladder && i.ladder.judge, v = j && typeof j === \"object\" ? j.verdict : null;\n    if (v === \"partially\" || v === \"unsupported\" || v === \"disagrees\") return v;\n    const hit = ((i && i.reasons) || []).find((r) => DISPUTE_REASON[r]);\n    return hit ? DISPUTE_REASON[hit] : null;\n  };\n  ZL.needsCompare = (i) => !!i && ((i.review_status || \"pending\") === \"pending\") && i.state !== \"rejected\" && !!ZL.judgeDispute(i);\n  ZL.DISPUTE_SENTENCE = { partially: \"The second AI check found this only partly supported by the quote.\", unsupported: \"The second AI check found this not supported by the quote.\", disagrees: \"The second AI check disagreed with the first result for this item.\" };\n'''\nassert anchor in s\ns=s.replace(anchor, add+anchor,1)\nopen(p,'w').write(s)\n\np='app/frontend/batch.js'\ns=open(p).read()\nold='e.date && e.state === \"verified\" && (e.review_status || \"pending\") === \"pending\");'\nnew='e.date && e.state === \"verified\" && (e.review_status || \"pending\") === \"pending\" && !ZL.judgeDispute(e));   // D-066: an item the second check disputed is accepted alone, with her compare'\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\n\np='app/frontend/review.js'\ns=open(p).read()\n# prompt text\nold='''  const COMPARE_PROMPT = \"Not recorded yet. Read the quote against your edit. Then click \\\\u201cI compared it with the quote\\\\u201d, or press Enter on it, to say you did.\";'''\nnew='''  const COMPARE_PROMPT = \"Not recorded yet. Read the quote against your edit. Then click \\\\u201cI compared it with the quote\\\\u201d, or press Enter on it, to say you did.\";\n  // T-179 / D-066: the same statement for an item the second AI check disputed. Nothing is sent by the a key; the button says it, and the server refuses an accept without it.\n  const DISPUTE_PROMPT = \"Not recorded yet. Read the quote against the summary. Then click \\\\u201cI compared it with the quote\\\\u201d, or press Enter on it, to say you did.\";\n  const disputeHint = (item) => (ZL.DISPUTE_SENTENCE[ZL.judgeDispute(item)] || \"The second AI check did not agree.\") + \" Read it against the quote, then press \\\\u201cI compared it with the quote\\\\u201d to say you did. Until then it stays open.\";'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''    const p = el(\"p\", { class: \"rv-help rv-compare-prompt\", \"data-testid\": \"edit-compare-prompt\" }, COMPARE_PROMPT + (ZL.secondCheckPending(item) ? \" \" + AI_HELD : \"\"));\n    if (ZL.secondCheckPending(item)) withServerText(p, \"item:\" + item.id, loadItemWhy(item.id), COMPARE_PROMPT + \" \");\n    return p;'''\nnew='''    const base = ZL.editToCheck(item) ? COMPARE_PROMPT : DISPUTE_PROMPT;\n    const p = el(\"p\", { class: \"rv-help rv-compare-prompt\", \"data-testid\": \"edit-compare-prompt\" }, base + (ZL.editToCheck(item) && ZL.secondCheckPending(item) ? \" \" + AI_HELD : \"\"));\n    if (ZL.editToCheck(item) && ZL.secondCheckPending(item)) withServerText(p, \"item:\" + item.id, loadItemWhy(item.id), base + \" \");\n    return p;'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''    let p = root.querySelector('[data-testid=\"edit-compare-prompt\"]');\n    if (!p) { p = comparePromptNode(f.item); const h = root.querySelector('[data-testid=\"edit-check-hint\"]'); if (h) h.after(p); else root.append(p); }'''\nnew='''    let p = root.querySelector('[data-testid=\"edit-compare-prompt\"]');\n    if (!p) { p = comparePromptNode(f.item); const h = root.querySelector('[data-testid=\"edit-check-hint\"], [data-testid=\"dispute-compare-hint\"]'); if (h) h.after(p); else root.append(p); }'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''    const toCheck = ZL.editToCheck(item);\n    const accepted = (st === \"accepted\" || st === \"edited\") && !toCheck;'''\nnew='''    const toCheck = ZL.editToCheck(item);\n    const mustCompare = !toCheck && ZL.needsCompare(item);      // T-179 / D-066: the second check disputed it, so Accept is her statement that she compared it with the quote\n    const compare = toCheck || mustCompare;\n    const accepted = (st === \"accepted\" || st === \"edited\") && !toCheck;'''\nassert old in s\ns=s.replace(old,new,1)\n\ns=s.replace('''const VARIANT = { accept: st === \"pending\" || toCheck ? (noted ? \"\" : \"btn--primary\")''','''const VARIANT = { accept: st === \"pending\" || toCheck ? (noted && !mustCompare ? \"\" : \"btn--primary\")''',1)\nold='''const acceptText = toCheck ? \"I compared it with the quote\" : accepted ?'''\nnew='''const acceptText = compare ? \"I compared it with the quote\" : accepted ?'''\nassert old in s\ns=s.replace(old,new,1)\nold='''RV.act(id, { action: \"accept\" }, ev.detail === 0 ? { advance: true } : { focus: \"accept\" }); } }));\n    let form;'''\nnew='''RV.act(id, compare ? { action: \"accept\", compared: true } : { action: \"accept\" }, ev.detail === 0 ? { advance: true } : { focus: \"accept\" }); } }));\n    let form;'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''    if (toCheck && comparePrompt.has(id)) root.append(comparePromptNode(item));'''\nnew='''    if (mustCompare) root.append(el(\"p\", { class: \"rv-help rv-recheck rv-dispute\", \"data-testid\": \"dispute-compare-hint\" }, disputeHint(item)));\n    if (compare && comparePrompt.has(id)) root.append(comparePromptNode(item));'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''.then((ok) => (ok && both ? RV.act(id, { action: \"accept\" }, { focus: \"accept\" }) : null))'''\nnew='''.then((ok) => (ok && both ? RV.act(id, { action: \"accept\", compared: true }, { focus: \"accept\" }) : null))      // Save and accept is her statement that the wording matches the quote beside it (D-066)'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''    if (key === \"a\" && ZL.editToCheck(f.item)) { askCompare(id); return; }'''\nnew='''    if (key === \"a\" && (ZL.editToCheck(f.item) || ZL.needsCompare(f.item))) { askCompare(id); return; }      // D-066 too: an item the second check disputed'''\nassert old in s\ns=s.replace(old,new,1)\n\nold='''      } else if (e && String(e.code).toUpperCase() === \"DATE_UNCONFIRMED\") showError'''\nnew='''      } else if (e && String(e.code).toUpperCase() === \"COMPARE_REQUIRED\" && body.action === \"accept\" && !body.compared) {   // D-066: the page did not know the second check disputed it; ask for the compare, record nothing\n        comparePrompt.add(id); showError(id, e.message || \"Compare it with the quote first.\"); const b = document.querySelector('[data-controls-for=\"' + id + '\"] [data-testid=\"btn-accept\"]'); if (b) b.focus();\n      } else if (e && String(e.code).toUpperCase() === \"DATE_UNCONFIRMED\") showError'''\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"else if (e && String(e.code).toUpperCase() === \\\"DATE_UNCONFIRMED\\\")\" app/frontend/review.js | head"
}
````

### User / tool · 2026-11-02T20:30:00.748Z

**tool result**
````
423:      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:04.548Z

**tool call — Bash**
````
{
 "command": "sed -n 244,254p app/backend/trace.py | cut -c1-400; sed -n 20,38p app/frontend/audit.js | cut -c1-300; git diff HEAD --stat -- app/backend/trace.py"
}
````

### User / tool · 2026-11-02T20:30:04.722Z

**tool result**
````
def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
    """The paralegal's rung. pending (live item) blocks export; rejected can only be dismissed; dismissed is skipped."""
    rs, rejected = row["review_status"], row["state"] == "rejected"
    evs = cx.events.get(row["id"], [])
    ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
                      **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
    if evs:
        ev["at"] = store.iso(evs[-1]["at"])
    if rs == "edited":
        ed = row.get("edited") or {}
  function callRow(c) {
    const rf = c.prepared ? " (prepared answer, not model output)" : c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
    return el("li", { class: "au-call", "data-testid": "audit-call" },
      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.prepared ? el("span", { class: "rv-chip", "data-testid": "audit-prepared" }, "Prepared answer") : null, c.verdict ? el("span", { class: "rv-chi
      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prompt_version), kv("hash", c.prompt_sha256 ? String(c.prompt_sha256).slice(0, 12) : null),
        kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
      pre("System prompt (local mode)", c.system_text), pre("Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
  }
  function eventRow(e, confirmed) {   // a flagged charge's accept names the flag she confirmed (the event's own `confirm` when the server sends it)
    const named = e.confirm ? "confirmed " + (e.confirm.name || e.confirm.flag) : confirmed;
    return el("li", { class: "au-call", "data-testid": "audit-event" }, el("div", { class: "au-line" }, el("strong", {}, e.action + (named ? ", " + named : "")), el("span", { class: "au-k" }, e.at || "")),
      e.before || e.after ? pre("Before and after (local mode)", { before: e.before, after: e.after }) : null);
  }

  RV.openAudit = async function (itemId, label) {
    ensure(); const c = RV.caseNow(); if (!c) return;
    title.textContent = itemId ? "Audit: " + (label || itemId) : "Audit: whole case";
    clear(body); body.append(el("p", { role: "status" }, "Loading…"));
    if (!dlg.open) dlg.showModal();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:09.745Z

**tool call — Bash**
````
{
 "command": "grep -n \"def audit\" -A25 app/backend/*.py | grep -n \"events\\|confirm\" | head"
}
````

### User / tool · 2026-11-02T20:30:09.832Z

**tool result**
````
21:app/backend/present.py-497-            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
22:app/backend/present.py-498-                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
24:app/backend/present.py-500-                       for e in DB.list_events(conn, case_id)],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:15.168Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/present.py'\ns=open(p).read()\nold='''                        **({\"confirm\": e[\"after\"][\"confirm\"]} if (e.get(\"after\") or {}).get(\"confirm\") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)\n'''\nnew=old+'''                        **({\"compared\": e[\"after\"][\"compared\"]} if (e.get(\"after\") or {}).get(\"compared\") else {}),      # T-179 / D-066: she said she compared it with the quote\n'''\nassert old in s\nopen(p,'w').write(s.replace(old,new,1))\np='app/frontend/audit.js'\ns=open(p).read()\nold='''    const named = e.confirm ? \"confirmed \" + (e.confirm.name || e.confirm.flag) : confirmed;'''\nnew='''    const named = [e.confirm ? \"confirmed \" + (e.confirm.name || e.confirm.flag) : confirmed, e.compared ? \"said she compared it with the quote\" : null].filter(Boolean).join(\", \");   // D-066'''\nassert old in s\nopen(p,'w').write(s.replace(old,new,1))\nEOF\nsed -n 490,502p app/backend/present.py | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:30:15.278Z

**tool result**
````
def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
                        **({"compared": e["after"]["compared"]} if (e.get("after") or {}).get("compared") else {}),      # T-179 / D-066: she said she compared it with the quote
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:20.182Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"narrative\" app/backend/export.py app/backend/export_routes.py app/backend/api.py app/backend/trace.py app/backend/present.py | cut -c1-200 | head -40; grep -n -i \"narrative\" app/frontend/*.js app/frontend/index.html | grep -v \"^app/frontend/narrative.js\" | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:30:20.289Z

**tool result**
````
app/backend/export.py:39:NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
app/backend/export.py:127:        self.narrative = case.get("narrative")
app/backend/export.py:148:    def narrative_sentences(self):
app/backend/export.py:150:        n = self.narrative
app/backend/export.py:273:    """What a narrative sentence was drafted from: if an entry's summary or quote changes afterwards, its sentences leave the letter."""
app/backend/export.py:319:    sents = v.narrative_sentences
app/backend/export.py:698:    """T-167: the plain sentence for a removed narrative sentence; the reason code is in the API field, not in the notes."""
app/backend/export.py:704:    n = v.narrative
app/backend/export.py:718:        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
app/backend/export.py:790:    blocker naming the line, whatever put it there (an AI summary, a quote, a paralegal's edit, a narrative sentence). Round 5: the BILLED CHARGES section is scanned too. A
app/backend/api.py:24:from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
app/backend/api.py:523:    @app.get("/api/cases/{token}/narrative")
app/backend/api.py:524:    def narrative_get(token: str):
app/backend/api.py:528:            return {"narrative": present.narrative_view(c, token, narrative.get(c, token))}
app/backend/api.py:532:    @app.post("/api/cases/{token}/narrative")
app/backend/api.py:533:    def narrative_draft(token: str):
app/backend/api.py:538:            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
app/backend/api.py:541:            return {"narrative": present.narrative_view(c, token, nar)}
app/backend/api.py:545:    @app.post("/api/cases/{token}/narrative/review")
app/backend/api.py:546:    async def narrative_review(token: str, request: Request):
app/backend/api.py:552:                return {"narrative": present.narrative_view(c, token, narrative.review(c, token, b.get("action"), now=time.time()))}
app/backend/trace.py:3:item_trace(conn, case_id, item_id, full)  one item (entry, amount, flag, narrative sentence): extracted, each code check by name, judge, human.
app/backend/trace.py:13:from app.backend import flag_templates as FT, generator, grounding, narrative, present, review, store, why
app/backend/trace.py:39:# Trace-only reason codes (case level and narrative); item reason codes come from confidence.REASON_CODES / why.py.
app/backend/trace.py:54:    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
app/backend/trace.py:55:    "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
app/backend/trace.py:56:    "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
app/backend/trace.py:57:    "FLAG_CONTENT": narrative.REASONS["FLAG_CONTENT"],
app/backend/trace.py:740:# ------------------------------------------------------------------ narrative sentences
app/backend/trace.py:742:    return narrative.REASONS.get(code) or reason_text(code)
app/backend/trace.py:745:def _narrative_trace(cx, item_id):
app/backend/trace.py:746:    nar = narrative.get(cx.conn, cx.case_id) or {}
app/backend/trace.py:757:    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
app/backend/trace.py:789:            ev["rationale"] = detail or narrative.REASONS[reason]
app/backend/trace.py:790:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", FAIL, (narrative.REASONS.get(reason, "") + " " + detail).strip(),
app/backend/trace.py:793:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAIL
app/backend/trace.py:806:                       next_action=na("DECIDE", {"view": "narrative"}, ["accept", "dismiss"])))
app/backend/trace.py:809:    return {"token": cx.case_id, "item_id": item_id, "kind": "narrative_sentence", "mode": "full" if cx.full else "metadata", "state": None,
app/backend/trace.py:820:    """UnknownItem for an id that is not in the case. Entry, amount, flag or narrative sentence (ns...). Any other error is a bug and propagates."""
app/backend/trace.py:823:        return _narrative_trace(cx, item_id)
app/frontend/dom.js:36:    11: "Prior conditions and charge ledger", 12: "Records review, credibility wording", 13: "Copied-forward notes across providers", 14: "Handwritten chiropractic scans", 15: "
app/frontend/stepper.js:50:  const extraLabels = {};   // narrative sentences register their own label ("ns1" -> first words of the sentence)
app/frontend/stepper.js:239:    return /^ns\d/.test(String(id)) ? gotoPanel("narrative") : gotoFirstPending();
app/frontend/stepper.js:259:    narrative: ["Go to the draft paragraph", () => gotoPanel("narrative")],
app/frontend/stepper.js:343:      case "SENTENCE_REMOVED": btn("Go to the draft paragraph", () => gotoPanel("narrative")); break;
app/frontend/index.html:87:<script src="narrative.js"></script>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:28.412Z

**tool call — Bash**
````
{
 "command": "sed -n 120,160p app/backend/export.py | cut -c1-220; git diff HEAD --stat -- app/backend/export.py; grep -rn \"narrative\" tests/unit/*.py tests/e2e/*.py -l"
}
````

### User / tool · 2026-11-02T20:30:28.537Z

**tool result**
````
    def __init__(self, case):
        self.records = {r["n"]: r for r in case.get("records", [])}
        cfg = case.get("export_config") or {}
        self.export_config = cfg if any(cfg.get(k) is not None for k in ("exhibit", "bates_prefix", "bates_start")) else None
        self.entries = sorted(case.get("entries", []), key=lambda e: (self._date(e), e["record_no"], str(e.get("id"))))
        self.amounts = sorted(case.get("amounts", []), key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
        self.flags = list(case.get("flags", []))
        self.narrative = case.get("narrative")
        self.overlaps = list(case.get("possible_overlaps") or [])

    def verbatim(self, item):
        """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
        return _norm(item.get("excerpt")) in _norm(self.text(item["record_no"]))

    @staticmethod
    def states_amount(e):
        """T-139 (D-019, R-CH-7, R-EX-8): the entry's summary or quote states money (the one shared detector, app/backend/money.py). It is used for the notes' hold reason; the letter
        itself is checked as text by the export gate (letter_money_blockers)."""
        return money.has_money(e.get("summary")) or money.has_money(e.get("excerpt"))

    @property
    def in_entries(self):
        """D-041: an entry with no confirmed date never reaches the letter, even if it was accepted before this rule (it is listed in the
        internal notes as 'date not confirmed'). T-139 r4: an accepted entry whose summary or quote states money is NOT dropped silently; it stays in the letter text, where the
        export gate (letter_money_blockers) finds the money and blocks the export, naming the line."""
        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e) and self.date_of(e)]

    @property
    def narrative_sentences(self):
        """Sentences of an ACCEPTED draft paragraph whose cited entry is still in the letter and unchanged since the draft."""
        n = self.narrative
        if not n or n.get("status") != "accepted":
            return []
        live = {e["id"]: e for e in self.in_entries}
        return [s for s in n.get("sentences", []) if s["entry_id"] in live and (n.get("basis") or {}).get(s["entry_id"]) == basis_hash(live[s["entry_id"]])
                and not charge_text.has_currency(s.get("text"))]

    @property
    def in_charges(self):
        return [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None
                and _status(a) == "in" and self.verbatim(a)]
tests/unit/test_backend_no_speaker_label.py
tests/unit/test_case_list_race.py
tests/unit/test_curated_fixtures.py
tests/unit/test_narrative.py
tests/unit/test_frontend_no_speaker_label.py
tests/unit/test_t116_gap_endpoints.py
tests/unit/test_t139_charge_text.py
tests/unit/test_spanish_records.py
tests/unit/test_t033_backend.py
tests/unit/test_t167_plain_wording.py
tests/unit/test_trace.py
tests/e2e/conftest.py
tests/unit/test_t133_lexicon.py
tests/unit/test_t168_strict_judge_parse.py
tests/e2e/test_no_console_errors.py
tests/e2e/test_stepper.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:33.396Z

**tool call — Bash**
````
{
 "command": "grep -rln \"TREATMENT SUMMARY\\|narrative/review\" tests | head; grep -n \"TREATMENT SUMMARY\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T20:30:33.548Z

**tool result**
````
tests/unit/test_narrative.py
app/backend/export.py:25:SUMMARY_TITLE = "TREATMENT SUMMARY"
app/backend/export.py:711:                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:39.339Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/export.py'\ns=open(p).read()\nold='''        self.narrative = case.get(\"narrative\")\n'''\nnew='''        self.narrative = case.get(\"narrative\") if narrative_in_letter() else None      # D-067: the drafted paragraph is cut from the MVP; it never reaches the letter (or the notes) unless NARRATIVE_IN_LETTER=1\n'''\nassert old in s\ns=s.replace(old,new,1)\nold='SUMMARY_TITLE = \"TREATMENT SUMMARY\"\\n'\nnew=old+'''\n\ndef narrative_in_letter() -> bool:\n    \"\"\"D-067: off by default. The paragraph needs its own eval and a verbatim quote plus [Ex. __ / Bates __] on each sentence (D-002) before it may reach a letter.\"\"\"\n    return __import__(\"os\").environ.get(\"NARRATIVE_IN_LETTER\") == \"1\"\n'''\nassert old in s\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nEOF\nsed -n 1,40p tests/unit/test_narrative.py"
}
````

### User / tool · 2026-11-02T20:30:39.461Z

**tool result**
````
"""T-059 (D-031): firm-voice treatment paragraph from ACCEPTED entries only; every sentence code-checked and judged; seeded hallucinations are removed."""
import pytest
from app.backend import export as X, narrative as N, pipeline as PL, review as RV, store
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script


def accepted_sample(tmp_path, accept=lambda n: True):
    conn = DB.connect(str(tmp_path / "n.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["state"] != "rejected" and accept(int(e["id"][1:])):
            RV.apply_review(conn, cid, e["id"], {"action": "accept"}, call=FakeCall(sample_script()))
    return conn, cid


GOOD = [{"entry_id": "e1", "text": "On January 9, 2026, Austin EMS documented a restrained driver rear-ended at approx. 35 mph who complained of neck pain 7/10 and headache."},
        {"entry_id": "e5", "text": "On February 20, 2026, Capital PT recorded pain 4/10, improving."}]


def narr(sentences, judge="supported"):
    return FakeCall({"narrative": {"sentences": sentences}, "j1": {"verdict": judge, "reason_code": "NONE"}})


def test_good_sentences_kept_with_citations(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    n = N.draft(conn, cid, call=narr(GOOD), now=2.0)
    assert [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"] and not n["removed"] and n["status"] == "pending"
    assert all(s["cite"].startswith("record ") and s["judge"]["verdict"] == "supported" for s in n["sentences"])


def test_only_accepted_entries_are_sent_to_the_model(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: n in (1, 5))
    call = narr(GOOD)
    N.draft(conn, cid, call=call, now=2.0)
    user = call.prompts("narrative")[0]
    assert "ENTRY e1" in user and "ENTRY e5" in user and "ENTRY e2 " not in user and "ENTRY e7" not in user
    for flagword in ("73 days", "gap", "Conflict", "FLAGS"):
        assert flagword.lower() not in user.lower().replace("approx", "")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:48.728Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_narrative.py'\ns=open(p).read()\nold='''def accepted_sample(tmp_path'''\nnew='''@pytest.fixture(autouse=True)\ndef _narrative_on(monkeypatch):\n    monkeypatch.setenv(\"NARRATIVE_IN_LETTER\", \"1\")      # D-067: off by default; these tests exercise the flagged-on path (test_d067_narrative_cut.py covers the default)\n\n\ndef accepted_sample(tmp_path'''\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nEOF\ncat > tests/unit/test_d067_narrative_cut.py <<'EOF'\n\"\"\"T-179 / D-067 (GATE-M3 product-manager + paralegal majors): the drafted treatment paragraph is cut from the MVP. No page offers it and it never reaches the letter.\nThe backend routes stay. With NARRATIVE_IN_LETTER unset, an ACCEPTED paragraph adds nothing to the letter or the notes.\"\"\"\nimport re\nfrom pathlib import Path\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import narrative as N\nfrom app.backend.api import create_app\nfrom tests.unit.test_api_routes import run_case\n\nFRONTEND = Path(__file__).resolve().parents[2] / \"app\" / \"frontend\"\n\n\n@pytest.fixture\ndef env(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"FIXTURE_SET\", \"curated\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    monkeypatch.delenv(\"NARRATIVE_IN_LETTER\", raising=False)\n    return TestClient(create_app(str(tmp_path / \"d067.sqlite\"), static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef test_the_page_loads_no_narrative_script_and_has_no_narrative_control():\n    html = (FRONTEND / \"index.html\").read_text()\n    assert \"narrative.js\" not in html\n    for f in FRONTEND.glob(\"*.js\"):\n        if f.name == \"narrative.js\":\n            continue\n        t = f.read_text()\n        assert \"btn-draft-narrative\" not in t and \"btn-accept-narrative\" not in t, f.name\n    assert \"Draft treatment paragraph\" not in html\n\n\ndef test_an_accepted_paragraph_never_reaches_the_letter_or_the_notes(env):\n    c = env\n    tok = run_case(c)\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"accept\"}).status_code == 200\n    d = c.post(f\"/api/cases/{tok}/narrative\")\n    if d.status_code == 200 and d.json()[\"narrative\"].get(\"sentences\"):\n        c.post(f\"/api/cases/{tok}/narrative/review\", json={\"action\": \"accept\"})\n    ex = c.get(f\"/api/cases/{tok}/export\").json()\n    assert \"TREATMENT SUMMARY\" not in ex[\"letter_text\"] and \"TREATMENT SUMMARY\" not in ex[\"internal_notes_text\"]\n    assert not re.search(r\"draft paragraph\", ex[\"internal_notes_text\"], re.I)\nEOF\n.venv/bin/python -m pytest tests/unit/test_d067_narrative_cut.py tests/unit/test_narrative.py tests/unit/test_d066_compare_confirm.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T20:30:56.474Z

**tool result**
````
E       assert 'narrative.js' not in '<!doctype h...>\n</html>\n'
E         
E         'narrative.js' is contained here:
E           ript src="narrative.js"></script>
E         ?           ++++++++++++
E           <script src="exportcfg.js"></script>
E           <script src="excerpt.js"></script>
E           <script src="uncovered.js"></script>...
E         
E         ...Full output truncated, use '-vv' to show

tests/unit/test_d067_narrative_cut.py:28: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_d067_narrative_cut.py::test_the_page_loads_no_narrative_script_and_has_no_narrative_control
1 failed, 45 passed in 7.30s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:02.515Z

**tool call — Bash**
````
{
 "command": "sed -i '' '/<script src=\"narrative.js\"><\\/script>/d' app/frontend/index.html && grep -n \"narrative\" tests/e2e/test_no_console_errors.py tests/e2e/test_stepper.py | cut -c1-200; grep -n \"narrative\" tests/e2e/conftest.py | cut -c1-120 | head -5; grep -n \"narrative\" app/frontend/stepper.js app/frontend/judges.js | head; sed -n 1,30p app/frontend/narrative.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:31:02.650Z

**tool result**
````
tests/e2e/test_stepper.py:270:# ---- item dialog and narrative
tests/e2e/test_stepper.py:289:def test_narrative_sentence_has_a_stepper(page, sample_case):
tests/e2e/test_stepper.py:290:    """Round 2: each drafted narrative sentence has 'How this sentence was checked'; it opens the ns trace ending in the human step."""
tests/e2e/test_stepper.py:295:    st, n = api("POST", f"/api/cases/{sample_case}/narrative", {})
tests/e2e/test_stepper.py:296:    if st != 200 or not n["narrative"].get("sentences"):
tests/e2e/test_stepper.py:297:        pytest.skip("this backend did not draft a narrative")
tests/e2e/test_stepper.py:299:    panel = page.get_by_test_id("narrative-panel"); panel.wait_for()
tests/e2e/test_stepper.py:300:    sents = panel.get_by_test_id("narrative-sentence")
tests/e2e/test_stepper.py:310:    assert active_in(page, '[data-panel="narrative"]')
tests/e2e/test_no_console_errors.py:15:# data-panel names, one per ZL.registerPanel/RV.registerPanel call in app/frontend (batch, audit, charges, export-settings, flags, manual, narrative). tests/unit
tests/e2e/test_no_console_errors.py:17:PANELS = ("batch", "audit", "charges", "export-settings", "flags", "manual", "narrative")
21:  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence wa
app/frontend/stepper.js:50:  const extraLabels = {};   // narrative sentences register their own label ("ns1" -> first words of the sentence)
app/frontend/stepper.js:239:    return /^ns\d/.test(String(id)) ? gotoPanel("narrative") : gotoFirstPending();
app/frontend/stepper.js:259:    narrative: ["Go to the draft paragraph", () => gotoPanel("narrative")],
app/frontend/stepper.js:343:      case "SENTENCE_REMOVED": btn("Go to the draft paragraph", () => gotoPanel("narrative")); break;
/* Draft treatment paragraph (T-059, D-031): drafted by the server from ACCEPTED entries only, every sentence cited and checked. Shown with the
   internal notes; it enters the letter only after the paralegal accepts it. GET/POST /narrative, POST /narrative/review. Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  const cache = {};   // token -> {nar|null} | {loading:true}
  let hostRef = null, msgText = "", msgErr = false, busy = false;
  const base = (t) => "/cases/" + encodeURIComponent(t) + "/narrative";
  const STATUS = {
    pending: ["Draft — not in letter until accepted", "chip--warn"],
    accepted: ["Accepted — goes into the letter as TREATMENT SUMMARY", "chip--ok"],
    dismissed: ["Dismissed — not in the letter", "chip--muted"],
  };

  const ERROR = {
    LLM_FAILED_AFTER_RETRIES: "The model could not draft the paragraph after three tries. Nothing was made up; press Draft again, or write it yourself from the accepted entries.",
    NO_ACCEPTED_ENTRIES: "Accept at least one entry first; the paragraph is written from accepted entries only.",
  };
  async function load(token) {
    cache[token] = { loading: true };
    try { const r = await RV.http("GET", base(token)); cache[token] = r.status === 200 ? { nar: (r.body && r.body.narrative) || null } : { na: true }; }
    catch (_) { cache[token] = { na: true }; }
    const c = RV.caseNow(); if (hostRef && c && c.token === token) draw(hostRef, c);
  }
  async function call(c, path, body, okMsg) {
    if (busy) return; busy = true; msgText = ""; msgErr = false;
    try {
      const r = await RV.http("POST", base(c.token) + path, body);
      if (r.status >= 400) { msgText = RV.errMsg(r, "That did not work."); msgErr = true; RV.say(msgText, true); }
      else { cache[c.token] = { nar: (r.body && r.body.narrative) || null }; msgText = okMsg; RV.say(okMsg); }
    } catch (e) { msgText = (e && e.message) || "That did not work."; msgErr = true; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:04.957Z

**tool call — Bash**
````
{
 "command": "sed -n 10,40p tests/e2e/test_no_console_errors.py; grep -rn \"registerPanel\" tests/unit/*.py | head -3"
}
````

### User / tool · 2026-11-02T20:31:05.065Z

**tool result**
````
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import BASE, api, open_case

# data-panel names, one per ZL.registerPanel/RV.registerPanel call in app/frontend (batch, audit, charges, export-settings, flags, manual, narrative). tests/unit/test_e2e_contract.py
# does not know this list, so test_every_registered_panel_is_listed greps the frontend for the registrations and fails if one is missing here.
PANELS = ("batch", "audit", "charges", "export-settings", "flags", "manual", "narrative")
LIB = "case_lib06_lop_billed_vs_adjusted"

HOOK = """
window.__zlErrors = [];
window.addEventListener("error", (e) => window.__zlErrors.push("window.onerror: " + (e.message || e.error)));
window.addEventListener("unhandledrejection", (e) => window.__zlErrors.push("unhandledrejection: " + (e.reason && e.reason.message || e.reason)));
"""


def _watch(page):
    """pageerror + console.error from Playwright, and window.onerror / unhandledrejection from a hook installed before any app script runs (read with _hooked)."""
    seen = []
    page.add_init_script(HOOK)
    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    return seen


def _hooked(page):
    return page.evaluate("window.__zlErrors || []")


@pytest.fixture
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:08.133Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && grep -n \"PANELS\\|data-panel\" tests/e2e/test_no_console_errors.py | head -20"
}
````

### User / tool · 2026-11-02T20:31:08.135Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:16.546Z

**tool call — Bash**
````
{
 "command": "grep -n \"PANELS\\|data-panel\" tests/e2e/test_no_console_errors.py | head -20"
}
````

### User / tool · 2026-11-02T20:31:16.630Z

**tool result**
````
3:- every registered side panel (ZL.registerPanel callers in app/frontend) must mount its root element `[data-panel=<name>]` and draw content, on the sample case and on one library case;
15:# data-panel names, one per ZL.registerPanel/RV.registerPanel call in app/frontend (batch, audit, charges, export-settings, flags, manual, narrative). tests/unit/test_e2e_contract.py
17:PANELS = ("batch", "audit", "charges", "export-settings", "flags", "manual", "narrative")
64:    for name in PANELS:
65:        panel = page.locator(f'[data-panel="{name}"]')
87:    """A new panel must be added to PANELS, or this smoke stays blind to it (the T-162 r2 finding: 4 of 7 panels were unwatched)."""
93:    assert registered == set(PANELS), f"registered panels {sorted(registered)} differ from PANELS {sorted(PANELS)}"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:21.966Z

**tool call — Bash**
````
{
 "command": "rm app/frontend/narrative.js && sed -i '' 's/, \"manual\", \"narrative\")/, \"manual\")/; s/flags, manual, narrative)/flags, manual)/' tests/e2e/test_no_console_errors.py && sed -n 268,315p tests/e2e/test_stepper.py"
}
````

### User / tool · 2026-11-02T20:31:22.066Z

**tool result**
````
# ---- item dialog and narrative
def test_why_dialog_opens_on_the_step_that_needs_you(pw, judged_case):
    """Round 2: at 390 px the Why dialog shows the step that needs the human and its button without scrolling, and focus is on that step."""
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 844}).new_page(); open_case(pg, judged_case)
    row = pg.locator('[data-testid="queue"] [data-item-id][data-state="needs_review"]').first
    reveal(row.get_by_test_id("entry-why")).click(); pg.get_by_test_id("item-stepper").wait_for()
    pg.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('aria-current') === 'step'")
    st = pg.get_by_test_id("item-stepper")
    assert "Needs your decision" in st.get_by_test_id("item-active").inner_text() or "Failed" in st.get_by_test_id("item-active").inner_text()
    btn = st.locator('[aria-current="step"]').get_by_test_id("btn-step-action").first
    box = btn.bounding_box()
    assert box and 0 <= box["y"] and box["y"] + box["height"] <= 844, box
    prog = st.get_by_test_id("item-progress").inner_text()
    assert "passed" in prog and "settled" not in prog
    st.get_by_test_id("btn-jump-active").click()
    assert pg.evaluate("document.activeElement.getAttribute('aria-current')") == "step"
    b.close()


def test_narrative_sentence_has_a_stepper(page, sample_case):
    """Round 2: each drafted narrative sentence has 'How this sentence was checked'; it opens the ns trace ending in the human step."""
    case = api("GET", f"/api/cases/{sample_case}")[1]
    for e in case["entries"]:
        if e["state"] == "verified":
            assert api("POST", f"/api/cases/{sample_case}/items/{e['id']}/review", {"action": "accept"})[0] == 200
    st, n = api("POST", f"/api/cases/{sample_case}/narrative", {})
    if st != 200 or not n["narrative"].get("sentences"):
        pytest.skip("this backend did not draft a narrative")
    open_case(page, sample_case)
    panel = page.get_by_test_id("narrative-panel"); panel.wait_for()
    sents = panel.get_by_test_id("narrative-sentence")
    assert sents.count() >= 1
    for i in range(sents.count()):
        assert sents.nth(i).get_by_test_id("btn-trace").inner_text() == "How this sentence was checked"
    sents.first.get_by_test_id("btn-trace").click()
    stp = page.get_by_test_id("item-stepper"); stp.wait_for()
    ids = stp.get_by_test_id("step").evaluate_all("els => els.map(e => e.getAttribute('data-step-id'))")
    assert ids[0] == "extracted" and ids[-1] == "human" and "sentence_checks" in ids
    assert page.locator("#why-title").inner_text().startswith("How this was checked: ")
    stp.locator('[data-step-id="human"]').get_by_test_id("btn-step-action").click()
    assert active_in(page, '[data-panel="narrative"]')


# ---- mobile
def test_steppers_usable_at_390(pw, sample_case):
    """At 390 px the case stepper, the item stepper and their buttons fit without horizontal scroll; buttons are touch-sized."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:25.118Z

Replace that test with a D-067 check.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:27.657Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_stepper.py'\ns=open(p).read()\na=s.index(\"def test_narrative_sentence_has_a_stepper\")\nb=s.index(\"# ---- mobile\")\nnew='''def test_no_page_offers_the_drafted_paragraph(page, sample_case):\n    \"\"\"T-179 / D-067: the drafted treatment paragraph is cut from the MVP UI. Even with an accepted entry there is no panel, no Draft button and no TREATMENT SUMMARY.\"\"\"\n    assert api(\"POST\", f\"/api/cases/{sample_case}/items/e1/review\", {\"action\": \"accept\"})[0] == 200\n    open_case(page, sample_case)\n    for tid in (\"narrative-panel\", \"btn-draft-narrative\", \"btn-accept-narrative\", \"narrative-sentence\"):\n        assert page.get_by_test_id(tid).count() == 0, tid\n    assert page.locator('[data-panel=\"narrative\"]').count() == 0\n    assert \"Draft treatment paragraph\" not in page.locator(\"body\").inner_text()\n\n\n'''\nopen(p,'w').write(s[:a]+new+s[b:])\nEOF\ngrep -n \"active_in\" tests/e2e/test_stepper.py | head -3"
}
````

### User / tool · 2026-11-02T20:31:27.775Z

**tool result**
````
54:def active_in(page, css):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:30.180Z

**tool call — Bash**
````
{
 "command": "sed -n 1,70p app/frontend/index.html | cut -c1-260; grep -n \"brand\\|case-name\\|btn-theme\\|btn-shortcuts\" app/frontend/*.css app/frontend/app.js app/frontend/switcher.js app/frontend/overview.js | cut -c1-220 | head -50"
}
````

### User / tool · 2026-11-02T20:31:30.273Z

**tool result**
````
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="review.css">
<link rel="stylesheet" href="stepper.css">
<link rel="stylesheet" href="sidebyside.css">
<link rel="stylesheet" href="suggestions.css">
<link rel="stylesheet" href="overview.css">
<link rel="stylesheet" href="uncovered.css">
</head>
<body>
<nav id="skip-nav" class="skip-nav" aria-label="Skip links" data-testid="skip-nav"></nav>
<div id="banner-synthetic" class="banner synth" data-testid="banner-synthetic" role="region" aria-label="Synthetic data notice">Synthetic data only — never paste real records</div>
<header class="app-header" data-testid="app-header">
  <div class="app-header-row">
    <button type="button" id="btn-all-cases" class="btn btn--sm" data-testid="btn-all-cases" hidden>All cases</button>
    <h1 class="brand">Treatment timeline</h1>
    <span id="case-name" class="case-name" data-testid="case-name" hidden></span>
    <div id="case-progress" class="case-progress" data-testid="case-progress-bar" hidden>
      <span id="progress-text" data-testid="progress-text" role="status"></span>
      <progress id="progress-bar" max="1" value="0" aria-label="Items decided"></progress>
    </div>
    <span class="spacer"></span>
    <div class="header-tools">
      <span id="badge" class="chip chip--muted" hidden></span>
      <span id="retention" class="muted small" hidden></span>
      <button type="button" id="delete-now" class="btn btn--sm" hidden>Delete now</button>
      <button type="button" id="btn-shortcuts" class="btn btn--sm" data-testid="btn-shortcuts" aria-haspopup="dialog" hidden>Shortcuts</button>
      <button type="button" id="btn-theme" class="btn btn--sm" data-testid="btn-theme" aria-label="Theme: auto. Press to change it.">Theme: auto</button>
      <button type="button" id="btn-export" class="btn btn--primary" data-testid="btn-export" hidden>Export</button>
    </div>
  </div>
</header>
<nav id="section-nav" class="section-nav" data-testid="section-nav" aria-label="Sections of this case" hidden><div class="section-nav-bar"><div id="section-nav-row" class="section-nav-row"></div></div></nav>
<div id="banner-ai" class="banner ai" data-testid="banner-ai" role="region" aria-label="AI notice" hidden></div>
<main id="main">
  <section id="view-cases" class="card cv" data-testid="cases-overview" aria-labelledby="cv-h" hidden>
    <div id="cases-body"></div>
  </section>
  <section id="view-input" class="card" aria-labelledby="h-input">
    <h2 id="h-input">Records</h2>
    <div id="input-body"></div>
  </section>
  <section id="view-review" aria-labelledby="h-review" hidden>
    <h2 id="h-review" class="sr">Review</h2>
    <div id="review-body"></div>
  </section>
  <section id="view-export" class="card" aria-labelledby="h-export" hidden>
    <h2 id="h-export">Export</h2>
    <div id="export-body"></div>
  </section>
</main>
<dialog id="source-modal" data-testid="record-modal" aria-labelledby="source-title">
  <div class="dlg-head"><h2 id="source-title">Source record</h2><button type="button" id="source-close" class="btn btn--sm" data-testid="btn-close-modal">Close</button></div>
  <div id="source-body"></div>
</dialog>
<dialog id="why-modal" data-testid="why-modal" aria-labelledby="why-title">
  <div class="dlg-head"><h2 id="why-title">Why?</h2><button type="button" class="btn btn--sm" data-testid="why-close" onclick="this.closest('dialog').close()">Close</button></div>
  <div id="why-body"></div>
</dialog>
<!-- load order matters; mock files are only used when API_MODE is "mock" -->
<script src="dom.js"></script>
<script src="mock_sample.js"></script>
<script src="mock.js"></script>
<script src="mock_flags.js"></script>
app/frontend/overview.css:61:.app-header-row:has(#btn-all-cases:not([hidden])) .brand { display: none; }   /* the button takes the brand's place while a case is open: one header row */
app/frontend/styles.css:35:.brand { white-space: nowrap; }
app/frontend/styles.css:36:.case-name { font-size: var(--t-lg); line-height: var(--lh-lg); font-weight: var(--w-strong); min-width: 0; overflow-wrap: anywhere; }
app/frontend/styles.css:43:  .case-name { flex: 0 1 auto; min-width: 16ch; max-width: 28ch; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
app/frontend/styles.css:226:@media (max-width: 480px) { .case-name { font-size: var(--t-md); } }
app/frontend/styles.css:247:  .app-header-row:has(#case-name:not([hidden])) .brand, #btn-shortcuts, #btn-theme, #badge, #retention { display: none; }
app/frontend/styles.css:248:  .case-name { flex: 1 1 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
app/frontend/app.js:40:    $("#case-name").hidden = !c; if (c) { const nm = nameOf(s) || "Case"; $("#case-name").textContent = nm; $("#case-name").title = nm; }   // T-166 F2: the header is one row, so a long name ends i
app/frontend/app.js:42:    $("#case-progress").hidden = !ready; $("#btn-export").hidden = !ready; $("#btn-shortcuts").hidden = !ready;
app/frontend/app.js:57:    const b = $("#btn-theme"); if (b) { b.textContent = "Theme: " + t; b.setAttribute("data-theme-choice", t); b.setAttribute("aria-label", "Theme: " + t + ". Press to change it."); }   // the name
app/frontend/app.js:154:    $("#btn-shortcuts").addEventListener("click", () => ZL.rv && ZL.rv.openShortcuts());
app/frontend/app.js:157:    $("#btn-theme").addEventListener("click", () => setTheme(THEMES[(THEMES.indexOf($("#btn-theme").getAttribute("data-theme-choice")) + 1) % THEMES.length]));
app/frontend/overview.js:320:    caseNameEl = ZL.$("#case-name"); if (!caseNameEl) return;
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:32.209Z

**tool call — Bash**
````
{
 "command": "sed -n 28,60p app/frontend/styles.css | cut -c1-260; sed -n 225,262p app/frontend/styles.css | cut -c1-300; sed -n 30,60p app/frontend/app.js | cut -c1-420"
}
````

### User / tool · 2026-11-02T20:31:32.306Z

**tool result**
````
.banner.synth::before { content: "i"; display: inline-flex; align-items: center; justify-content: center; width: 1rem; height: 1rem; border: 1.5px solid currentColor; border-radius: 50%; font-size: var(--t-xs); line-height: 1; font-style: italic; flex: none; }
.banner.ai { background: var(--info-bg); color: var(--info); border-bottom: 1px solid var(--border); font-size: var(--t-sm); line-height: var(--lh-sm); text-align: center; padding-top: var(--s-1); padding-bottom: var(--s-1); }
.skip-nav { position: absolute; left: var(--s-2); top: var(--s-2); z-index: 60; display: flex; flex-wrap: wrap; gap: var(--s-2); }
.skip-nav a { position: absolute; left: -10000px; top: 0; white-space: nowrap; padding: var(--s-2) var(--s-3); background: var(--panel); color: var(--accent); border: 2px solid var(--accent); border-radius: var(--r-1); font-weight: var(--w-strong); text-decora
.skip-nav a:focus { position: static; }
.app-header { position: sticky; top: var(--banner-h); z-index: 20; min-height: var(--header-h); display: flex; align-items: center; background: var(--panel); border-bottom: 1px solid var(--border); box-shadow: var(--elev-1); }
.app-header-row { width: 100%; margin: 0 auto; padding: var(--s-2) var(--gutter); display: flex; align-items: center; flex-wrap: wrap; gap: var(--s-2) var(--s-3); }
.brand { white-space: nowrap; }
.case-name { font-size: var(--t-lg); line-height: var(--lh-lg); font-weight: var(--w-strong); min-width: 0; overflow-wrap: anywhere; }
.case-progress { display: flex; align-items: center; gap: var(--s-3); min-width: 0; font-variant-numeric: tabular-nums; font-weight: var(--w-strong); }
.spacer { flex: 1 1 0; }
.header-tools { display: flex; align-items: center; gap: var(--s-2); flex-wrap: wrap; }
/* T-166 F2: on a wide screen the case header is ONE row. The name gives way first (ellipsis, full name in its title); the progress line is short and never wraps; the tools sit together at the right. */
@media (min-width: 1100px) {
  .app-header-row { flex-wrap: nowrap; }
  .case-name { flex: 0 1 auto; min-width: 16ch; max-width: 28ch; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .case-progress { flex: 0 0 auto; white-space: nowrap; }
  .spacer { flex: 1 1 0; min-width: 0; }
  .header-tools { flex-wrap: nowrap; flex: none; }
  .header-tools .btn { white-space: nowrap; }
}
@media (min-width: 1100px) and (max-width: 1279px) { .case-progress progress { display: none; } }   /* the words carry the progress when the bar has no room */
progress { appearance: none; -webkit-appearance: none; box-sizing: border-box; width: 6rem; height: var(--s-2); border: 1px solid var(--border-strong); border-radius: var(--r-1); background: var(--sunken); overflow: hidden; vertical-align: middle; }   /* T-174
progress::-webkit-progress-bar { background: var(--sunken); border-radius: var(--r-1); }
progress::-webkit-progress-value { background: var(--accent); border-radius: var(--r-1); }
progress::-moz-progress-bar { background: var(--accent); }
main { max-width: 1040px; margin: 0 auto; padding: var(--s-4) var(--gutter) var(--s-7); }
.top { display: none; }

/* ---- 3 buttons and controls ------------------------------------------------------------------------------------------------ */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: var(--s-2); min-height: var(--control-h); padding: 0 var(--s-3); border: 1px solid var(--border-strong); border-radius: var(--r-1);
  background: var(--panel); color: var(--text); font: var(--w-strong) var(--t-md)/var(--lh-md) var(--font); text-align: center; cursor: pointer; text-decoration: none;
  transition: background-color var(--motion), border-color var(--motion), color var(--motion); }
}
@media (max-width: 480px) { .case-name { font-size: var(--t-md); } }
@media print { .banner.synth, .app-header { position: static; } }

/* processing state */
.run-state { margin-top: var(--s-3); display: grid; gap: var(--s-2); }
.skeletons { display: grid; gap: var(--s-2); margin-top: var(--s-2); }
.skeleton { height: 4rem; border-radius: var(--r-2); background: linear-gradient(90deg, var(--sunken), var(--border), var(--sunken)); background-size: 200% 100%; }
@media (prefers-reduced-motion: no-preference) { .skeleton { animation: shimmer 1.4s linear infinite; } @keyframes shimmer { to { background-position: -200% 0; } } }

/* a finished run: the records card is one row (count, list, start over) */
.input-done { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-1) var(--s-4); }
.input-done .found { font-size: var(--t-lg); line-height: var(--lh-lg); }
.input-done .row { margin-top: 0; margin-left: auto; }
.input-done .reclist-wrap { margin: 0; }
.input-done .reclist-wrap[open] { flex: 1 1 100%; order: 5; }
#view-input:has(.input-done) { padding: var(--s-1) var(--s-4); margin-bottom: 0; }
#view-input:has(.input-done) > h2 { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.summary .tag { margin-left: var(--s-2); vertical-align: baseline; min-height: 0; line-height: var(--lh-xs); }
@media (max-width: 768px) {
  /* phone header: case name and Export on one row, progress under it; the rest is on the desktop header */
  .app-header-row { gap: var(--s-1) var(--s-3); padding-top: var(--s-2); padding-bottom: var(--s-2); }
  .app-header-row:has(#case-name:not([hidden])) .brand, #btn-shortcuts, #btn-theme, #badge, #retention { display: none; }
  .case-name { flex: 1 1 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .spacer { display: none; }
  .case-progress { order: 3; flex: 1 1 100%; }
  .header-tools { margin-left: auto; }
  .case-progress progress { flex: 1 1 auto; width: auto; }
}

/* decided rows: the state, not the action (T-060 r3). Filled primary is for an undecided item only. */
.btn.rv-decided, .btn[aria-pressed="true"].rv-decided { border-color: transparent; background: transparent; color: var(--ok); font-weight: var(--w-strong); cursor: default; }
.btn.rv-decided:hover { background: transparent; }
.btn.rv-decided--muted, .btn[aria-pressed="true"].rv-decided--muted { color: var(--text-muted); }
.btn.rv-decided[data-icon]::before { content: "\2713"; }
.btn.rv-decided--muted[data-icon]::before { content: "\2296"; }
.entry .rv-actions .btn, .entry .row-actions .btn { min-height: var(--control-h-sm); }
.rv-actions .btn--link.rv-reset { font-size: var(--t-sm); }
    const all = itemsOf(c), open = all.filter(ZL.undecided), mine = open.filter((i) => i.state === "needs_review" || ZL.editToCheck(i)).length;   // an edit still to compare is Needs review by definition (the server counts it; its response may lag the item's state)
    const sm = ZL.cases && ZL.cases.summary ? ZL.cases.summary(c.token) : null, h = sm && sm.hitl;
    const same = h && h.needs_review_open != null && (h.pending || 0) + (h.edits_to_check || 0) === open.length && (h.edits_to_check || 0) === ZL.editCount(c);
    return { total: all.length, decided: all.length - open.length, left: open.length, needs: same ? h.needs_review_open : mine, edits: ZL.editCount(c) };
  };
  // The open total (undecided items, an edit still to compare included) of the case on screen, or null. "Can export \u2014 N not reviewed" says this N everywhere.
  ZL.openLeft = function () { const c = ZL.state.get().case; return c && c.status === "ready" ? ZL.progressOf(c).left : null; };
  const nameOf = (s) => (s.case && ((ZL.titleOf && ZL.titleOf(s.case)) || (ZL.caseTitles || {})[s.token] || ZL.niceName(s.case.name))) || "";   // T-157: the same title the overview shows (typed name, else the first record header; library cases keep their plain titles)
  function renderHeader(s) {
    const c = s.case, ready = !!(c && c.status === "ready");
    $("#case-name").hidden = !c; if (c) { const nm = nameOf(s) || "Case"; $("#case-name").textContent = nm; $("#case-name").title = nm; }   // T-166 F2: the header is one row, so a long name ends in an ellipsis and the full name is its tooltip
    document.title = c && c.name ? "Treatment timeline · " + nameOf(s) : "Treatment timeline";
    $("#case-progress").hidden = !ready; $("#btn-export").hidden = !ready; $("#btn-shortcuts").hidden = !ready;
    if (!ready) return;
    const p = ZL.progressOf(c), bar = $("#progress-bar");
    // T-166 F2/F9: a short line that fits the one-row header. The full sentence is the tooltip and the screen-reader text; the edits to check are in data-edits.
    const full = p.decided + " of " + p.total + " decided" + (p.needs ? " · " + p.needs + (p.needs === 1 ? " item needs" : " items need") + " review" + (p.edits ? ", including " + p.edits + (p.edits === 1 ? " edit" : " edits") + " to check" : "") : "");
    const pt = $("#progress-text"); pt.textContent = p.decided + " of " + p.total + " decided" + (p.needs ? " · " + p.needs + " to review" : "");
    pt.title = full; pt.setAttribute("aria-label", full); pt.setAttribute("data-edits", String(p.edits || 0)); pt.setAttribute("data-needs", String(p.needs || 0));
    bar.max = Math.max(p.total, 1); bar.value = p.decided;
    bar.setAttribute("aria-valuetext", p.decided + " of " + p.total + " items decided");
  }
  // ---- theme: auto (follow the OS), light or dark. Remembered in localStorage when it is available; the page works without it.
  const THEMES = ["auto", "light", "dark"];
  function setTheme(t) {
    const root = document.documentElement;
    if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
    const b = $("#btn-theme"); if (b) { b.textContent = "Theme: " + t; b.setAttribute("data-theme-choice", t); b.setAttribute("aria-label", "Theme: " + t + ". Press to change it."); }   // the name contains the visible text and says the current value
    try { localStorage.setItem("zlayt.theme", t); } catch (_) { /* not remembered */ }
  }
  // ---- skip links: the first focusable things on the page. They land on the work, most blocking first: the dates form, the dismissal suggestion, the first item to decide, flags, charges, Export. With one of those present it is Tab, Enter.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:42.303Z

**tool call — Bash**
````
{
 "command": "grep -n \"^\\.sr\\b\\|\\.sr {\" app/frontend/*.css | head -3; sed -n 55,66p app/frontend/overview.css | cut -c1-250"
}
````

### User / tool · 2026-11-02T20:31:42.403Z

**tool result**
````
app/frontend/styles.css:16:.sr, .rv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.co-slot > * { border: 0; border-top: 1px solid var(--border); border-radius: 0; margin: 0; }
.co-slot .todo-strip { padding: var(--s-2) var(--s-4); background: transparent; border-left: 0; }
.co-slot .checks { background: transparent; }
.co[data-do-first] .zs-nextline { display: none; }       /* the block already says what to do first; the case checks do not say it a second time, in other words */

#btn-all-cases { flex: none; }
.app-header-row:has(#btn-all-cases:not([hidden])) .brand { display: none; }   /* the button takes the brand's place while a case is open: one header row */
@media (max-width: 768px) {
  .cv { padding: var(--s-3); }
  .cv-row { grid-template-columns: minmax(0, 1fr); padding: var(--s-3); gap: var(--s-2); }
  .cv-filters .btn { flex: 1 1 auto; }
  .cv-sort { width: 100%; } .cv-sort select { flex: 1 1 auto; min-width: 0; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:46.346Z

**tool call — Bash**
````
{
 "command": "grep -n \"scroll-margin\\|scroll-padding\\|--chrome-h\" app/frontend/*.css app/frontend/*.js | cut -c1-200 | head -30; grep -n \"function restoreFocus\" -A30 app/frontend/review.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T20:31:46.453Z

**tool result**
````
app/frontend/overview.css:138:#view-input { scroll-margin-top: 7rem; }
app/frontend/overview.css:141:/* ---- T-174 F13: the sticky section nav under the case header (Overview, Timeline, Flags, Charges, Export). It sits at --head-h, and app.js adds its height to --chrome-
app/frontend/sidebyside.css:7:  body.sbs-on .sbs-pane:not([hidden]) { display: flex; flex-direction: column; position: fixed; top: calc(var(--chrome-h) + var(--s-3)); right: var(--s-4); width: var(--s
app/frontend/styles.css:21:.entry, .rv-card, [data-item-id], [data-testid="btn-export"], h2[tabindex], section[tabindex] { scroll-margin-top: var(--sticky); }
app/frontend/app.js:119:    document.documentElement.style.setProperty("--chrome-h", (b.offsetHeight + h.offsetHeight + nh) + "px");
app/frontend/tokens.css:63:  --chrome-h: calc(var(--banner-h) + var(--header-h));   /* the sticky banner plus the sticky header; app.js writes the measured height here, so a header that grows never co
app/frontend/tokens.css:64:  --sticky: calc(var(--chrome-h) + var(--s-2));   /* what a scrolled-to item must clear */
app/frontend/stepper.js:89:    // a target taller than 60% of the screen lands with its heading at the top (the sticky banner is cleared by scroll-margin-top); short rows are centred
149:  function restoreFocus(pf) {
150-    if (!pf) return;
151-    requestAnimationFrame(() => {
152-      if (pf.nextFrom) {
153-        const plan = pf.plan || { key: null, ids: [], id: pf.nextFrom }, g = plan.key && document.querySelector(plan.key);
154-        const now = new Map((g ? rowsIn(g) : []).map((n) => [n.getAttribute("data-item-id"), n]));
155-        const at = plan.ids.indexOf(plan.id), order = plan.ids.slice(at + 1).concat(plan.ids.slice(0, Math.max(at, 0)));
156-        const t = order.map((i) => now.get(i)).filter(Boolean).find(decidable);
157-        if (t) { focusNode(t); return; }
158-        const c = RV.caseNow(), left = c ? ZL.progressOf(c).left : 0;
159-        if (!left) { focusExport("Nothing left to decide. Export is next."); return; }   // the last decision: the next control is the one that finishes the job, not the top of the page
160-        // this list is finished but others are not: T-166 F6 moves focus on to the first open item of the NEXT list (page order, wrapping at the end) and says so. It never decides that item:
161-        // a or d on it is a new press. "The next item anywhere" (Start review, n) is the same move from any row.
162-        const g0 = plan.key && document.querySelector(plan.key), all = RV.domItems().filter((n) => decidable(n) && !(g0 && g0.contains(n)));
163-        const after = g0 ? all.filter((n) => g0.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING) : all, nx = after[0] || all[0];
164-        if (nx) {
165-          focusNode(nx);
166-          const f = RV.find(RV.caseNow(), nx.getAttribute("data-item-id")), ng = nx.closest(GROUP);
167-          RV.say((g0 ? groupName(g0) + " done. " : "") + "Next: " + (ng ? groupName(ng) + ", " : "") + (f ? RV.ghostLabel(f.item) : "the next item") + ". " + left + (left === 1 ? " item is" : " items are") + " still open.");
168-          return;
169-        }
170-        const stay = now.get(plan.id) || order.map((i) => now.get(i)).filter(Boolean)[0];
171-        if (stay) focusNode(stay); else { const s = document.querySelector('[data-testid="btn-start-review"]'); if (s) s.focus(); }
172-        RV.say("Nothing more to decide here. " + left + (left === 1 ? " item is" : " items are") + " still open, but each needs something other than a plain decision (a date, a check of your wording).");
173-        return;
174-      }
175-      if (pf.action === "dismiss") {   // T-166 F5: the dismissed row is now a placeholder in its slot; focus its Undo (never the row's old buttons, which moved to the Dismissed group, often off screen)
176-        const u = document.querySelector('[data-ghost-for="' + pf.id + '"] button');
177-        if (u) { u.focus({ preventScroll: true }); u.scrollIntoView({ block: "nearest" }); return; }
178-      }
179-      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:48.281Z

**tool call — Bash**
````
{
 "command": "sed -n 179,200p app/frontend/review.js | cut -c1-300; grep -n \"function focusNode\" -A10 app/frontend/review.js | cut -c1-260; sed -n 110,125p app/frontend/app.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T20:31:48.432Z

**tool result**
````
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) { t.focus({ preventScroll: true }); t.scrollIntoView({ block: "nearest" }); } else focusItem(pf.id);
    });
  }

  // T-166 F11/F7: a row keeps the four things she does most (Accept, Edit, Dismiss, Open record); the rest (Why this status, Change quote, Audit, Dismiss with a reason) wait behind one "More" button.
  // Returns {btn, panel}: put btn where the link row ends and panel right after it (the panel's buttons then follow it in Tab order and flow in the same line when it is open).
  RV.moreActions = function (items, name, o) {
    const opt = o || {}, panel = el("div", { class: "rv-more-panel", hidden: !opt.open, "data-testid": opt.panelTestid || "more-panel" }, items.filter(Boolean));
    const btn = el("button", { type: "button", class: "btn btn--link rv-more-btn", "data-testid": opt.testid || "btn-more", "aria-expanded": String(!!opt.open), "aria-label": "More actions: " + name,
      onclick: () => { const on = panel.hidden; panel.hidden = !on; btn.setAttribute("aria-expanded", String(on)); btn.textContent = on ? "Less" : "More"; btn.setAttribute("aria-label", (on ? "Less actions: " : "More actions: ") + name); if (opt.onToggle) opt.onToggle(on); } }, opt.open ? "Less" : "
    return { btn, panel };
  };

  // T-166 F5: a dismissed row leaves a placeholder in its own slot for six seconds ("Dismissed: Capital PT, visit 8. Undo"), so the click has a visible result where she clicked and the way back is right there.
  // Then it collapses into the Dismissed (n) group. The page repaints on every change, so each placeholder is re-inserted after every paint (zl:panels) at the position it was captured at:
  // before the row that followed it (or after the row that preceded it, or first in its list).
  const GHOST_MS = 6000, ghosts = new Map();   // id -> {id, label, key, nextId, prevId, tr, timer}
  RV.ghostLabel = (item) => (item.provider ? item.provider + (item.date ? ", " + ZL.fmtDate(item.date) : "") : RV.label(item));
  function slotOf(id) {
    const ae = document.activeElement, mine = ae && ae.closest && ae.closest("[data-item-id]");
130:  function focusNode(t) {
131-    if (!t) return false;
132-    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
133-    t.focus({ preventScroll: true }); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
134-    return true;
135-  }
136-  function focusItem(id) {
137-    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
138-    return focusNode(q || document.querySelector('[data-item-id="' + id + '"]'));
139-  }
140-  // T-174 F8: "the first item" is ONE item. The case overview names it (case.next_action, the line "Do this first", data-do-first-item); the skip link, Start review and the n key all go there. Only when
    ZL.renderSkips();
    resetTabStart(s);
  }
  ZL.state.subscribe(render);
  // T-166 F2: what sits under the sticky banner and header (the side-by-side pane, scroll margins) reads the measured height, so a header that grows can never cover it.
  function measureChrome() {
    const b = $("#banner-synthetic"), h = document.querySelector(".app-header"); if (!b || !h) return;
    const n = document.querySelector("#section-nav .section-nav-bar"), nh = n && !n.closest("#section-nav").hidden ? n.offsetHeight : 0;   // T-174 F13: the section nav sits under the header and is part of what a scrolled-to item must clear
    document.documentElement.style.setProperty("--head-h", (b.offsetHeight + h.offsetHeight) + "px");
    document.documentElement.style.setProperty("--chrome-h", (b.offsetHeight + h.offsetHeight + nh) + "px");
  }
  ZL.measureChrome = measureChrome;
  document.addEventListener("DOMContentLoaded", () => {
    measureChrome(); window.addEventListener("resize", measureChrome);
    if (window.ResizeObserver) { const ro = new ResizeObserver(measureChrome); ro.observe($("#banner-synthetic")); ro.observe(document.querySelector(".app-header")); const n = document.querySelector("#section-nav .section-nav-bar"); if (n) ro.observe(n); }
  });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:59.340Z

**tool call — Bash**
````
{
 "command": "grep -n \"status-retry\\|cases-retry\\|retry\" app/frontend/overview.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T20:31:59.454Z

**tool result**
````
54:  let newBtn = null, toolsEl = null, skelEl = null, retryFocus = false, headEl = null;
98:      el("button", { type: "button", class: "btn btn--sm", "data-testid": "cases-status-retry", onclick: (ev) => { ev.stopPropagation(); load(); } }, "Try again")));
144:      el("span", { class: "cv-err-text" }), " ", el("button", { type: "button", class: "btn btn--sm", "data-testid": "cases-retry", onclick: () => { retryFocus = true; loadErr = ""; paint(); load(); } }, "Try again"));
218:    if (retryFocus && settled) { retryFocus = false; if (!loadErr && headEl && host.closest("section") && !host.closest("section").hidden) headEl.focus({ preventScroll: true }); }
````

### User / tool · 2026-11-02T20:32:00.898Z

[Request interrupted by user]
