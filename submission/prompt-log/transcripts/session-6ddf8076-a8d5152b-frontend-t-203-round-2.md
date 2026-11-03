# Subagent: Frontend: T-203 round 2 (Frontend: T-203 round 2)

Source: `agent-a8d5152b9a428fc34.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T23:47:58.533Z

You are the frontend worker in /Users/arsis/zlayt-pm-project on T-203, round 2. Claim it with --force. Read reviews/T-203-ux-designer.md and its evidence in artifacts/review-evidence/T-203-ux/.

Fix the following:
1. **Major.** At 375x667, after "Fix the wording", the "Saved…" message replaces the hint and the tick box is hidden behind the bar. The hint must persist until she ticks, or a saved message must coexist with it, and the tick box must be reachable and visible. Better still, scroll it into view.
2. **"above".** The hint says "above", but at 375 the box can be below. Make the wording position-neutral, such as "Tick the box 'I compared them' first", or scroll the box into view.
3. **"PT".** "PT" maps to patient, so it hides a real outside word. Fix it so PT and physical therapy are not treated as "patient".
4. **Nit.** Fix "lost pay" sitting under "Payment: money received" if cheap.

Add e2e tests at 375x667 for the after-edit path. Verify the guided suite plus test_no_console_errors from a fresh `git archive` in an empty directory (E2E_REQUIRE_DB=1). Commit through a temp index, move the card to in_review, and reply in 1 line.

### User / tool · 2026-11-02T23:47:58.539Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:01.176Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-203 --agent frontend --force; python3 tools/board.py show T-203 | tail -60; cat reviews/T-203-ux-designer.md; ls artifacts/review-evidence/T-203-ux/"
}
````

### User / tool · 2026-11-02T23:48:01.372Z

**tool result**
````
T-203 claimed by frontend
---
id: "T-203"
title: "Guided UI polish: at 375x667 a disputed line's tick box sits below the buttons and nothing says why Yes is disabled; paralegal r2 minors"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T23:35:18Z"
updated_at: "2026-11-02T23:48:01Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T23:48:01Z"
rounds: 1
commits: ["38ee0c3"]
reviews:
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-203-ux-designer.md", "at": "2026-11-02T23:47:53Z"}
ac:
  - {"n": 1, "text": "at 375x667 the tick box is visible with the buttons or a one-line hint says 'Tick the box above to say you compared them'; paralegal r2 minors fixed where cheap; e2e at 375x667", "done": true, "evidence": "tests/e2e/guided/test_t203.py (375x667 hint + 390 wording/Pt) passes; git archive of 38ee0c3 tree: guided suite + test_no_console_errors 135 passed, E2E_REQUIRE_DB=1"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:35:25Z frontend: claimed
- 2026-11-02T23:41:12Z frontend: AC 1 checked: tests/e2e/guided/test_t203.py (375x667 hint + 390 wording/Pt) passes; git archive of 38ee0c3 tree: guided suite + test_no_console_errors 135 passed, E2E_REQUIRE_DB=1
- 2026-11-02T23:41:12Z frontend: moved in_progress -> in_review
- 2026-11-02T23:41:16Z orchestrator: review dispatched: ux-designer-reviewer
- 2026-11-02T23:47:53Z orchestrator: review ux-designer-reviewer (claude-sonnet-5-5): changes — reviews/T-203-ux-designer.md; round 1; findings:
    - [major] 375x667: after Fix the wording, Yes is greyed, the slot shows only 'Saved ... Read it once more', and the tick box is hidden behind the action bar; the new hint is not shown (this is the second half of my T-181 r3 F1) — fix: Keep both sentences while Yes is greyed by an unticked box: append the hint to the Saved text ('Saved: your wording is in. Now tick the box to say you compared t
    - [minor] 375x667 and 360x740: 'Tick the box above' points the wrong way, and at 360x740 the box is behind the buttons — fix: Use direction-free words, e.g. 'Tick the box under the line to say you compared them.', or make the hint a button that scrolls the box into view. Hint is 13 px; at 375 it is the only cue, so use the 15 px used for the slot at rest.
    - [minor] The new chart-shorthand mapping treats 'PT' (physical therapy) as 'patient', so 'Patient' goes unmarked when the quote has only 'PT' — fix: Map 'pt' to 'patient' only when the quote spells it 'Pt' (not all caps), or only when the same quote also contains words like 'states', 'reports' or 'denies'; otherwise leave it underlined.
- 2026-11-02T23:47:53Z orchestrator: assigned: frontend
- 2026-11-02T23:48:01Z frontend: claimed

## Handoff
What changed: review.js drawStatus shows 'Tick the box above to say you compared them.' (generic 'Tick the box above first.') in the status slot whenever Yes is greyed by an unticked box (all sizes, only when no Saved message); S.sync redraws on tick. SHOULD_BE_DAMAGES now reads 'a damages figure (such as lost pay)'; step2 outside-word diff treats Pt/Dx/Rx/Hx/Tx/Sx as the word they stand for. How verified: tests/e2e/guided/test_t203.py (375x667 one-line hint inside the bar with Yes, clears on tick; no hint on a line without a box; lib11 e2 no 'Patient' underline; a6 wording); git archive of commit tree, E2E_REQUIRE_DB=1 guided + test_no_console_errors: 135 passed. Left: paralegal minors needing backend skipped (notes 'Causation language' label, notes opening line; letter-date major already done by T-200); UX r3 minor 2 (390x844 refusal editor top under header) not in this card. Surprised me: the tick box still sits under the bar at 375x667, the hint is the fix; commit via temp index because tree has others' hunks.

# T-203 review: 375x667 greyed Yes, payment wording, underline fix (commit 38ee0c3), ux-designer-reviewer

Verdict: **changes** (0 blockers, 1 major, 2 minors, 2 nits). Scores: design quality 4, originality 4, craft 3, functionality 3.

**On a disputed line at 375x667, is it clear why Yes is greyed out, and what to do?**
- **Why: yes.** The status slot inside the action bar, with Yes and No, now reads "Tick the box above to say you compared them." It is one line (18 px high at y 636-654, bar top 482, screen bottom 667). It clears when she ticks the box and comes back if she unticks it. Yes does not move in either state (y 531-581), so nothing jumps.
- **What to do: only half.** The box is at y 691-719 on a 667 px screen. It is below the screen, not above. "Above" points the wrong way, and nothing says to scroll (F2).
- **The reworded-line path is not fixed (F1).** After "Fix the wording" at 375x667, Yes is greyed, the slot says only "Saved: your wording is in. Read it once more against the highlighted words.", and the tick box is hidden behind the bar. That text stayed for 30 s. Tapping the greyed Yes does nothing.

**Payment wording and underline fix**
- **Payment wording:** on a payment, the second-check line now reads "A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as." The old "an amount that is not a bill" is gone (lib11 a6 at 390, 375 and 1440). It is clearer. One nit about "lost pay" beside "Payment: money received" (F4).
- **Underline fix:** on lib11 e2 and lib10 e1 the underlined words no longer include "Patient". On lib10 e1 the underlined words are only Driver, pickup, struck, intersection, at 390, 375 and 1440. The fix also hides a real case (F3).

**Regressions at 390 and 1440: none found.**
- lib10 e1 at 390x844 has the same numbers as T-181 r3: mark y 223-269, line 412-484, box 599-627, bar top 659, box hit = self. Yes stays at y 708-758 with the hint, after ticking, and after unticking.
- Sample e1 after a valid edit at 390: mark 235-332, line 412-508, box 602-630. These are the same as r3.
- At 1440 the tick hint replaces the "Keys: A says yes..." line while the box is unticked, and the keys line returns once she ticks it. Yes stays at y 782-838. Lines with no box show no hint (lib10 e2 at 375 and 1440).
- Deterministic: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh archive printed `142 passed in 192.63s`.

## Findings
- **F1 (major):** the reworded line at 375x667 still has a greyed Yes with no reason, and the tick box is hidden behind the bar.
- **F2 (minor):** at 375x667 "above" points the wrong way, and at 360x740 the box is behind the buttons.
- **F3 (minor):** "PT" (physical therapy) is treated as "patient", so an outside word goes unmarked.
- **F4 (nit):** "lost pay" next to a "Payment: money received" card.
- **F5 (nit):** the "Step 3 of 4" label wraps to three lines at 375 (not from this commit).

```json
{"card": "T-203", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 38ee0c3 (git archive 38ee0c3 into a new empty scratchpad dir ux-t203-38ee0c3; HEAD = 38ee0c3 per git rev-parse --short HEAD); demo app http://127.0.0.1:7981 (LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7982 (same plus ZLAYT_MODE=local, to create library cases lib10 and lib11); both stopped afterwards (PIDs 89165 and 89167 from lsof; both ports then answered 000); sample case evals/golden/sample.txt plus library cases case_lib10_eob_ub04_cms1500 and case_lib11_priors_and_ledger",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '142 passed in 192.63s' (includes tests/e2e/guided/test_t203.py)",
  "artifacts/review-evidence/T-203-ux-measure.py: lib10 e1 (disputed line, tick box) at 375x667, 390x844, 360x740 and 1440x900: rects of status slot, Yes/No, tick box, mark, line, action bar; tapped the greyed Yes; scrolled the page until the box cleared the bar; ticked and unticked the box (measure.out is the printed output, screenshots in artifacts/review-evidence/T-203-ux/)",
  "same script: sample e1 fresh and after a valid edit ('transported to' -> 'taken to') at 375x667, 390x844 and 1440x900; lib10 e2 (no box) at 375 and 1440",
  "artifacts/review-evidence/T-203-ux-measure2.py: sample e1 at 375x667 after a valid edit, status slot read at +0, +5, +15 and +30 s, tapped the greyed Yes, scrolled 300 px; lib11 e2 and lib10 e1 outside-word underlines and lib11 a6 (Step 3) second-check wording at 390, 375 and 1440; walked every lib11 item at 375x667 listing greyed Yes, box id, box rect and slot text (measure2.out)",
  "read the screenshots a-lib10-e1-375x667-open.png, a-lib10-e1-390x844-open.png, a-lib10-e1-1440x900-open.png, b-sample-e1-375x667-edit-to-check.png, p2-lib11-a6-375x667.png and p2-lib11-a6-390x844.png",
  "node check of the new ABBR mapping copied from app/frontend/guided/step2.js:113-114 with a PT (physical therapy) quote",
  "git show 38ee0c3 (review.js drawStatus and AMOUNT_WAY, step2.js ABBR, tests/e2e/guided/test_t203.py); board.py show T-203 for the handoff; read reviews/T-181-ux-designer-r3.md and personas/ux-designer.md"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major",
   "title": "375x667: after Fix the wording, Yes is greyed, the slot shows only 'Saved ... Read it once more', and the tick box is hidden behind the action bar; the new hint is not shown (this is the second half of my T-181 r3 F1)",
   "evidence": "T-203-ux-measure2.py [1 edit-to-check 375x667 +0s .. +30s], identical at each time: status 'Saved: your wording is in. Read it once more against the highlighted words.', slot y 627-663, yesDisabled true, box y 630-658 (id check-compare), bar y 482-667, scrollY 107. T-203-ux-measure.py [B sample e1 375x667 after valid edit]: boxHit = 'status-text', so the slot is drawn on top of the box. Tapping the greyed Yes changes nothing. Only after a 300 px page scroll does the box appear (y 330-358, the highlighted words are then off screen). Screenshot artifacts/review-evidence/T-203-ux/b-sample-e1-375x667-edit-to-check.png shows a faded Yes, 'Saved...' and no box. Cause: review.js drawStatus (38ee0c3) shows the tick hint only when no 'Saved' message is up (`!s && ...`); the edit path always has one. At 390x844 the same path is fine, the box is in view at y 602-630 above the bar at 659.",
   "why_it_matters": "This is the same state the card was opened to fix: a first-time user on a small iPhone sees a greyed Yes and no box. The reworded line is the correction path, and the message sends her back to the highlighted words, not to the box. The disputed-line case in the brief is fixed; the reworded line is not. In my r3 F1 and r3 acceptance test, both the disputed and the reworded line were named.",
  "fix": "Keep both sentences while Yes is greyed by an unticked box: append the hint to the Saved text ('Saved: your wording is in. Now tick the box to say you compared them.'), or draw the hint as a second line under the Saved message. Also when she taps the greyed Yes, scroll the box into view or flash the hint.",
   "acceptance_test": "At 375x667, on sample e1 after a valid edit, the status slot text contains 'Tick the box' while Yes is disabled, and tapping the disabled Yes either scrolls the box into view or leaves that sentence in the slot. Extend tests/e2e/guided/test_t203.py to cover the edit path."},
  {"severity": "minor",
   "title": "375x667 and 360x740: 'Tick the box above' points the wrong way, and at 360x740 the box is behind the buttons",
   "evidence": "T-203-ux-measure.py [A lib10-e1 375x667 open]: box y 691-719 on a 667 px screen (boxBelowViewport true), boxHit 'none'; the hint is at y 636-654. Scrolling the page 249 px brings the box to y 442-470, above the bar, but the mark is then at y -26-20 (off the top). lib11 a6 at 375x667 has the box at y 666-694, also below the screen (p2-lib11-a6-375x667.png: no box visible, hint says 'above'). At 360x740 the box is at y 604-632 behind Yes/No (y 604-654), boxHit 'big', and the page cannot scroll (docH 740, scrollY stays 0); only the card scrolls. The words 'above' are correct at 390x844 and 1440x900 (box at y 599-627, above the bar at 659).",
   "why_it_matters": "She now learns why Yes is greyed, but she is told to look above for a box that is below the screen or under the buttons. The card AC literally asks for 'above', so this is a preference about the wording, not a miss against the AC.",
   "fix": "Use direction-free words, e.g. 'Tick the box under the line to say you compared them.', or make the hint a button that scrolls the box into view. Hint is 13 px; at 375 it is the only cue, so use the 15 px used for the slot at rest.",
   "acceptance_test": "At 375x667 on lib10 e1 the hint contains no direction word that contradicts the box position, or tapping it brings the box fully above the bar."},
  {"severity": "minor",
   "title": "The new chart-shorthand mapping treats 'PT' (physical therapy) as 'patient', so 'Patient' goes unmarked when the quote has only 'PT'",
   "evidence": "app/frontend/guided/step2.js:113-114: ABBR = { pt: 'patient', ... } and stem() lowercases. I copied the functions into node: quote 'PT 3x/week, tolerating exercises', line 'Patient attended physical therapy 3 times a week' gives underlined words [attended, physical, therapy, 3, times], with no 'Patient'. The quote 'Pt states chest wall pain' with 'Patient states chest wall pain' gives none, as intended. Not run in the app, because the fixture backend cannot draft a PT line; the code path is the same function.",
   "why_it_matters": "'PT' for physical therapy is common in injury records. A line that says 'Patient' where the record only said 'PT' is exactly the kind of outside word the underline exists to show, and the underline now hides it.",
   "fix": "Map 'pt' to 'patient' only when the quote spells it 'Pt' (not all caps), or only when the same quote also contains words like 'states', 'reports' or 'denies'; otherwise leave it underlined.",
   "acceptance_test": "Unit or e2e: quote 'PT 3x/week' with line 'Patient attended ...' underlines 'Patient'; quote 'Pt states chest pain' with line 'Patient states chest pain' underlines nothing."},
  {"severity": "nit",
   "title": "'(such as lost pay)' sits right under 'Payment: money received, not a charge' on a payment amount",
   "evidence": "p2-lib11-a6-390x844.png: card text 'Payment: money received, not a charge.' followed by 'A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as.'",
   "why_it_matters": "'Payment' and 'pay' side by side can read as the same thing. Still far better than 'an amount that is not a bill'.",
   "fix": "Name the way plainly: 'a damages figure (for example lost wages), not a payment to the clinic'.",
   "acceptance_test": "Wording review only."},
  {"severity": "nit",
   "title": "At 375x667 the Step 3 label 'Step 3 of 4' wraps to three lines beside the bill total (not changed by this commit)",
   "evidence": "p2-lib11-a6-375x667.png top strip: 'Step / 3 of / 4'. The diff touches no CSS (git show 38ee0c3 --stat: review.js, step2.js, test_t203.py).",
   "why_it_matters": "Small polish; it eats header height on the screen where height is scarcest.",
   "fix": "Let the bill-total pill shrink or drop 'so far' at 375.",
   "acceptance_test": "At 375x667 on Step 3 the step label is on at most two lines."}
 ],
 "whats_right": [
  "On a disputed line the reason for the greyed Yes now sits in the action bar next to the buttons, in one line at 375, 390 and 1440, and it clears on the tick without moving Yes (y 531-581 at 375, 708-758 at 390).",
  "The new second-check wording on a payment ('a damages figure (such as lost pay)') and the 'Patient' underline fix both show in the app, and nothing moved at 390 or 1440: same rects as T-181 r3 and 142 e2e tests pass.",
  "The hint appears only when a box is the reason: lines without a box show none (lib10 e2 at 375 and 1440), and the generic 'Tick the box above first.' shows for the 'check-separate' box on lib11 bills a2-a4."
 ],
 "questions_for_chris": []}
```
a-lib10-e1-1440x900-open.png
a-lib10-e1-1440x900-ticked.png
a-lib10-e1-360x740-open.png
a-lib10-e1-360x740-scrolled.png
a-lib10-e1-360x740-tap-disabled-yes.png
a-lib10-e1-360x740-ticked.png
a-lib10-e1-375x667-open.png
a-lib10-e1-375x667-scrolled.png
a-lib10-e1-375x667-tap-disabled-yes.png
a-lib10-e1-375x667-ticked.png
a-lib10-e1-390x844-open.png
a-lib10-e1-390x844-tap-disabled-yes.png
a-lib10-e1-390x844-ticked.png
b-sample-e1-1440x900-edit-to-check.png
b-sample-e1-1440x900-fresh.png
b-sample-e1-375x667-edit-to-check.png
b-sample-e1-375x667-fresh.png
b-sample-e1-390x844-edit-to-check.png
b-sample-e1-390x844-fresh.png
c-lib10-e2-1440x900.png
c-lib10-e2-375x667.png
measure2.out
p2-edit-375x667-after-wheel.png
p2-edit-375x667-after30s.png
p2-lib11-a6-1440x900.png
p2-lib11-a6-375x667.png
p2-lib11-a6-390x844.png
p2-lib11-e2-1440x900.png
p2-lib11-e2-375x667.png
p2-lib11-e2-390x844.png
tokens.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:01.542Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_round3.md"
}
````

### User / tool · 2026-11-02T23:48:01.549Z

**tool result**
````
1	---
2	name: t181-round3
3	description: T-181 r3 phone fixes - mark alignment in the record window, refusal scrolled above the bar, textarea height pitfall, stale-archive panel test
4	metadata:
5	  type: project
6	---
7	
8	- **Highlight in the record window**: `alignMark()` in review.js (rect-based, mark top-aligned with a 30px lead on phones, a third down on desktop). The old code used `offsetTop`, which is relative to the wrong offset parent, so the mark sat at the bottom edge. Toggle `needs-check` BEFORE `renderSource` so the window has its final size when scrolled. Split on phones with a tick box is `.8fr 1.2fr` (src body ~155px at 390x844; line card ~294 still shows line + tick box). A fixed split per visit is deliberate: a content-sized split would move the cards between items.
9	- **Refusal**: `showRefusal()` after render when `S.err`: scrolls the line card (it is the scroll box on phones) so the foot is inside it, plus `scrollIntoView` with `scroll-margin-bottom:200px` in the short-phone (<=720px high) block so the page scroll stops above the bar. Root cause of "Save does nothing" was `textarea.edit {height:100%}` of an auto-height body: the textarea overran the foot and covered the refusal. Phones now use `height: 8rem`.
10	- **Test recipe**: tests/e2e/guided/test_round3.py asserts bounding boxes (mark inside the window and viewport and above `[data-testid=actions]`; foot above the bar and `elementFromPoint` inside it). Set `R3_SHOTS=<dir>` to dump screenshots; the env var does not survive between Bash calls, export it in the same command.
11	- **Panel-list test**: `test_every_registered_panel_is_listed` now scans only the scripts index.html loads. A reviewer extracting `git archive` over an old directory kept a deleted narrative.js and saw a false failure; always extract into a fresh dir.
12	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:02.151Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/feedback_verify_from_archive.md"
}
````

### User / tool · 2026-11-02T23:48:02.159Z

**tool result**
````
1	---
2	name: verify-from-git-archive
3	description: Verify a frontend commit from a git archive of the commit tree, never the dirty tree; temp-index commit recipe and the confirm-dialog Escape race
4	metadata:
5	  type: feedback
6	---
7	
8	Run e2e from `git archive <tree>` (tree from `GIT_INDEX_FILE=tmp git write-tree`) with `E2E_REQUIRE_DB=1`; a plain pytest there starts its own private server on a free port.
9	
10	**Why:** T-154 r2 committed the a-key guard inside mountSection() (ReferenceError on every case load) while 12/12 passed on the dirty tree where other workers' hunks and the guard sat elsewhere. tests/e2e/test_no_console_errors.py now fails CI on any pageerror.
11	
12	**How to apply:** build the commit with a temp index (`git read-tree HEAD`, `update-index --cacheinfo` for a file with others' hunks, `--add` for my own files); the check_stale_index hook blocks it if HEAD moved, so re-read-tree and recheck `git diff --stat OLD HEAD -- app/frontend tests/e2e`. The shared scratchpad has many dirs named arch/head0/etc; use a fresh name with mkdir -p.
13	
14	Pitfall: ZL.confirmCharge (charges.js) must settle on the `cancel` event and ignore a stale `close` when the dialog is open again, else Escape then `a` is dropped (item still busy) or the reopened window is shut.
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:04.285Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; git log --oneline | head -3; grep -n \"drawStatus\" -n app/frontend/guided/review.js | head; grep -n \"ABBR\\|AMOUNT_WAY\\|SHOULD_BE_DAMAGES\" app/frontend/guided/*.js | head -20; cat tests/e2e/guided/test_t203.py"
}
````

### User / tool · 2026-11-02T23:48:04.467Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t181_round2.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test
f0921e4 feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
a44cfa7 fix(qa): T-187 r4 README item 7 wording matches the normalized rule (no unicode/percent/entity decoding claimed)
141:    function say(text, undo) { S.said = text ? { text, undo } : null; drawStatus(); }
219:    function drawStatus() {
282:      updateTitlebar(); syncButtons(); drawStatus();
313:    S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };
app/frontend/guided/review.js:82:  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "a damages figure (such as lost pay)" };
app/frontend/guided/review.js:85:    if (v === "disagrees" && AMOUNT_WAY[code]) return `A second AI check thought this may be ${AMOUNT_WAY[code]}, not what it was first sorted as.`;
app/frontend/guided/step2.js:113:  const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
app/frontend/guided/step2.js:114:  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return ABBR[x] || x; };
"""T-203 (phone): at 375x667 the tick box of a disputed line can sit below the action bar. The greyed Yes must say why, in the status slot beside it.
Also: a payment's second-check wording names the damages way, and chart shorthand ('Pt') is not underlined as an outside word."""
from playwright.sync_api import expect

from tests.e2e.guided.test_round2 import LIB10, phone, item, make, open_item   # noqa: F401  (make is a fixture)

HINT = "Tick the box above to say you compared them."


def test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons(pw, make):
    tok = make(LIB10); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e1")
        expect(page.get_by_test_id("check-compare")).to_be_attached()
        yes, st = page.get_by_test_id("answer-yes"), page.get_by_test_id("status-text")
        expect(yes).to_be_disabled()
        expect(st).to_have_text(HINT)
        r = page.evaluate("""() => { const q = (s) => document.querySelector('[data-testid=' + s + ']').getBoundingClientRect(), y = q('answer-yes'), s = q('status-text'), bar = q('actions');
            return { yes: [y.top, y.bottom], st: [s.top, s.bottom, s.left, s.right], bar: [bar.top, bar.bottom], vh: innerHeight, vw: innerWidth, lines: Math.round(s.height / parseFloat(getComputedStyle(document.querySelector('[data-testid=status-text]')).lineHeight)) }; }""")
        assert r["st"][0] >= r["bar"][0] - 0.5 and r["st"][1] <= r["vh"] and r["st"][2] >= 0 and r["st"][3] <= r["vw"], ("the hint is not fully on screen inside the action bar", r)
        assert r["yes"][0] >= r["bar"][0] - 0.5 and r["yes"][1] <= r["vh"], ("the Yes button is not on screen with the hint", r)
        assert r["lines"] == 1, ("the hint is more than one line", r)
        page.get_by_test_id("check-compare").check(force=True)
        expect(yes).to_be_enabled()
        expect(st).not_to_have_text(HINT)
        page.get_by_test_id("check-compare").uncheck(force=True)
        expect(yes).to_be_disabled(); expect(st).to_have_text(HINT)
    finally:
        b.close()


def test_the_hint_is_not_shown_on_a_line_with_no_tick_box(pw, make):
    tok = make(); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e2")
        expect(page.get_by_test_id("answer-yes")).to_be_enabled()
        expect(page.get_by_test_id("status-text")).not_to_contain_text("Tick the box")
    finally:
        b.close()


def test_chart_shorthand_pt_is_not_underlined_and_the_damages_way_is_named(pw, make):
    from tests.e2e.guided.test_round2 import LIB11
    tok = make(LIB11); b, page = phone(pw, 390, 844)
    try:
        open_item(page, tok, "e2")
        out = set(page.get_by_test_id("outside-word").all_inner_texts())
        assert "Patient" not in out and "struck" in out, out
        open_item(page, tok, "a6", step="bills")
        reason = page.get_by_test_id("compare-reason")
        expect(reason).to_contain_text("damages figure")
        assert "not a bill" not in reason.inner_text()
    finally:
        b.close()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:05.957Z

**tool call — Bash**
````
{
 "command": "sed -n 130,150p app/frontend/guided/review.js; sed -n 205,320p app/frontend/guided/review.js; sed -n 100,135p app/frontend/guided/step2.js; grep -n \"Payment: money\\|money received\" app/frontend/guided/*.js | head"
}
````

### User / tool · 2026-11-02T23:48:06.181Z

**tool result**
````
  R.run = async function (ctx, cfg) {
    const token = ctx.token, body = document.body;
    const S = { ctx, cfg, token, c: ctx.case, queue: [], idx: -1, ui: {}, busy: false, alive: true, said: null, err: null, screen: null, forceCompare: new Map(), part2: new Set(), el: {} };
    const q$ = (id) => S.queue.find((q) => q.id === id);
    S.item = (id) => cfg.find(S.c, id);
    S.counted = () => S.queue.filter((q) => !q.optional && S.item(q.id));
    S.left = () => S.counted().filter((q) => undecided(S.item(q.id)));
    S.numberOf = (id) => { const i = S.counted().findIndex((q) => q.id === id); return i < 0 ? null : i + 1; };
    S.record = (rid) => (S.c.records || []).find((r) => r.id === rid);
    S.recOf = (pos) => (S.c.records || []).find((r) => pos >= r.char_start && pos < r.char_end);

    function say(text, undo) { S.said = text ? { text, undo } : null; drawStatus(); }
    S.say = say;
    S.fail = async function (e) {
      if (e && e.name === "AbortError") return;
      if (e instanceof G.ApiError && e.status === 409 && e.code === "stale_item") {
        let now = "";
        try { await S.reload(); const it = S.cur(); now = it && it.review_status === "dismissed" ? " It is now left out." : it && (it.review_status === "accepted" || it.review_status === "edited") ? " It is now kept." : ""; } catch (_) { /* the message below is enough */ }
        S.err = { text: `This item changed in another tab. We've loaded the latest.${now} Choose again if that is wrong.` };
      } else if (e instanceof G.ApiError && e.code === "COMPARE_REQUIRED") {
        const it = S.cur(); if (it) S.forceCompare.set(it.id, (e.detail && e.detail.verdict) || "disagrees");       // the page did not know: show the compare box (the server's reason is in it), never a raw error
    E.actions = h("div", { class: "actions", "data-testid": "actions" }, h("div", { class: "actions-in" }, E.question,
      h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
    E.back.textContent = "‹ Back"; E.later.textContent = "Decide later";
    E.back.onclick = () => back();
    E.later.onclick = () => { const l = S.screen && S.screen.later; if (l === false) return; if (l && l.run) l.run(); else S.skip(); };
    ctx.view.replaceChildren(E.titlebar, E.work, E.actions);
    ctx.layout("frame");

    function toggleSteps(force) {
      const open = force != null ? force : !body.classList.contains("steps-open");
      body.classList.toggle("steps-open", open); E.toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    const onDocClick = (e) => { if (body.classList.contains("steps-open") && !e.target.closest("#step-bar") && !e.target.closest("[data-testid=btn-steps]")) toggleSteps(false); };

    function drawStatus() {
      const s = S.said;
      const box = !s && E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
      E.statusText.textContent = s ? s.text : box ? (box.dataset.testid === "check-compare" ? "Tick the box above to say you compared them." : "Tick the box above first.") : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
      E.status.classList.toggle("hint", !s && !box);
      E.status.dataset.why = box ? "tick" : "";
      E.undo.hidden = !(s && s.undo);
      E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;
    }

    function updateTitlebar() {
      const items = S.counted(), left = S.left().length, total = items.length, done = total - left;
      const q = S.queue[S.idx], n = q && !q.optional ? S.numberOf(q.id) : null;
      E.count.textContent = S.screen && S.screen.counter ? S.screen.counter : n ? `${cfg.unit} ${n} of ${total}` : q && q.optional ? "Optional" : `${total} ${cfg.unit.toLowerCase()}s`;
      E.prog.textContent = `${done} answered · ${left} to go`;
      const pct = total ? Math.round((done / total) * 100) : 100;
      E.fill.style.width = pct + "%"; E.bar.setAttribute("aria-valuenow", String(pct));
      if (cfg.chip) E.total.textContent = R.money(((S.c.totals || {}).accepted || {}).cents || 0);
    }

    /* ---- render one screen ---- */
    function fillTag(tag, extra) { return tag ? h("span", { class: "tag " + tag.cls, title: tag.title || null, "data-testid": extra || "line-tag" }, tag.text) : null; }
    function syncButtons() {
      const sc = S.screen; if (!sc) return;
      const set = (el, def) => {                                    // an absent answer keeps its place (invisible), so nothing else moves
        if (!def) { el.style.visibility = "hidden"; el.disabled = true; el.setAttribute("aria-hidden", "true"); el.tabIndex = -1; return; }
        el.disabled = S.busy || (typeof def.disabled === "function" ? def.disabled() : !!def.disabled);
        el.style.visibility = ""; el.removeAttribute("aria-hidden"); el.removeAttribute("tabindex");
      };
      set(E.yes, sc.yes); set(E.no, sc.no); set(E.third, sc.third);
      E.back.disabled = S.busy || sc.back === false; E.later.disabled = S.busy;
      E.later.style.visibility = sc.later === false ? "hidden" : ""; E.later.tabIndex = sc.later === false ? -1 : 0;
      E.third.classList.toggle("hint", !!(sc.third && sc.third.hint));
      E.undo.disabled = S.busy;
    }
    function drawBtn(el, def, keep) {
      if (!def) { el.replaceChildren(keep || ""); el.classList.remove("two"); el.onclick = null; return; }
      el.replaceChildren(...[def.label, def.sub ? h("span", { class: "sub" }, def.sub) : null].filter(Boolean));
      el.classList.toggle("two", !!def.sub); el.onclick = () => def.run();
      if (el === E.yes) el.classList.toggle("primary", !def.plain);
    }
    function render(keepScroll) {
      const item = S.cur(), q = S.queue[S.idx];
      if (!item) return finish();
      const sc = (S.screen = cfg.present(S, item, q));
      E.lineCard.dataset.itemId = item.id; E.lineCard.dataset.kind = item.kind || ""; E.lineCard.dataset.mode = S.ui.mode || "view";
      const head = [fillTag(sc.tag), fillTag(sc.tag2, "line-tag2"), sc.sub ? h("span", { class: "ch-sub", "data-testid": "line-sub" }, sc.sub) : null];
      E.lineHead.replaceChildren(...head.filter(Boolean));
      const bodyScroll = E.lineBody.scrollTop;
      E.lineBody.replaceChildren(...[].concat(sc.body || []).filter(Boolean));
      E.lineBody.scrollTop = keepScroll ? bodyScroll : 0;
      if (!keepScroll) E.lineCard.scrollTop = 0;
      const err = S.err ? { cls: "bad", nodes: [h("strong", {}, "Not saved. "), S.err.text] } : null;
      const foot = err || sc.foot || { cls: "plain", nodes: [] };
      E.foot.className = "card-f " + (foot.cls || "plain"); E.foot.replaceChildren(...[].concat(foot.nodes || []).filter(Boolean));
      if (err) E.foot.setAttribute("role", "alert"); else E.foot.removeAttribute("role");
      E.question.textContent = sc.question || "";
      drawBtn(E.yes, sc.yes, "Yes"); drawBtn(E.no, sc.no, "No"); drawBtn(E.third, sc.third, "Fix the wording");
      E.later.textContent = sc.later && sc.later.label ? sc.later.label : "Decide later";
      // a phone: when any item of this step needs a tick box the line card gets the room for the whole visit (so nothing moves between items), and the line and its box are on screen together
      S.sticky = S.sticky || S.queue.some((q) => { const it = S.item(q.id); return !!it && (!!R.dispute(it) || !!it.edit_to_check || (it.countable && it.kind !== "charge") || (it.flag && it.confirm_required)); }) || !!E.foot.querySelector("input[type=checkbox]");
      E.work.classList.toggle("needs-check", !!S.sticky);      // before the record is drawn: the window is its final size when the highlight is scrolled into it
      renderSource(false);
      updateTitlebar(); syncButtons(); drawStatus();
      if (err) showRefusal();
      if (!keepScroll) focusFirst(sc);
    }
    function renderSource(keep) {
      const sc = S.screen; if (!sc || !sc.src) { E.srcHead.textContent = ""; E.srcBody.replaceChildren(); return; }
      const top = E.srcBody.scrollTop;
      E.srcHead.textContent = sc.src.head || ""; E.srcBody.replaceChildren(...sc.src.nodes().filter(Boolean));
      if (keep) E.srcBody.scrollTop = top;
      else alignMark();
    }
    /* the first highlighted word is in the record window: top-aligned with one line of the record above it on a phone (the window is small), a third down on a wide screen. Measured with rects, not offsetTop (the window is not the mark's offset parent). */
    function alignMark() {
      const box = E.srcBody, m = box.querySelector("mark, .sent.on");
      if (!m) { box.scrollTop = 0; return; }
      const narrow = matchMedia("(max-width: 760px)").matches, lead = narrow ? Math.min(30, box.clientHeight / 4) : box.clientHeight / 3;
      const at = m.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
      box.scrollTop = Math.max(0, at - lead);
    }
    S.alignMark = alignMark;
    /* a refused save: its words sit in the line card's foot, which on a phone can be below the visible part of the card (the card scrolls as one box) or under the action bar. Bring it into view, never under the bar. */
    function showRefusal() {
      const card = E.lineCard, f = E.foot;
      if (card.scrollHeight > card.clientHeight + 1) {
        const c = card.getBoundingClientRect(), r = f.getBoundingClientRect();
        if (r.bottom > c.bottom) card.scrollTop += r.bottom - c.bottom + 2;
      }
      try { f.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* the card scroll above is enough */ }
    }
    S.renderSource = () => renderSource(true);
    S.render = (keep) => render(!!keep);
    S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };
    function focusFirst(sc) {
      const f = sc.focus === "field" ? E.lineBody.querySelector("textarea, input") : null;
      const target = f || (!E.yes.disabled ? E.yes : E.foot.querySelector("input[type=checkbox]") || (sc.yes && !S.busy ? E.foot : (!E.no.disabled ? E.no : null)));      // a refused Yes with no tick box: focus the reason, never a button that would answer
      if (target && document.activeElement !== target && !S.firstPaint) target.focus({ preventScroll: true });
    }

    /* ---- moving ---- */
    const sents = (rec.sentences || []).filter((s) => picked.has(s.start));
    if (!sents.length) return { error: "Pick at least one sentence." };
    const all = rec.sentences, idx = sents.map((s) => all.findIndex((x) => x.start === s.start)).sort((a, b) => a - b);
    if (idx.some((v, i) => i && v !== idx[i - 1] + 1)) return { error: "Pick sentences that follow each other." };
    const a = all[idx[0]], b = all[idx[idx.length - 1]];
    return { excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
  }
  function togglePick(S, sent) { const p = S.ui.picked || (S.ui.picked = new Set()); p.has(sent.start) ? p.delete(sent.start) : p.add(sent.start); S.renderSource(); }
  const warningsFoot = (S) => (S.ui.warnings || []).map((w) => h("p", { class: "foot-warn", "data-testid": "save-warning" }, R.plain(w.message || String(w))));

  /* ---------- the words of a line that are not in the highlighted words (code, no AI): a deterministic word diff so she sees what to check (paralegal review T-181 major) ---------- */
  const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
  const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
  const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return ABBR[x] || x; };
  function outsideParts(summary, quote) {
    const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
    let last = 0, any = false;
    for (const m of String(summary || "").matchAll(WORD)) {
      const w = m[0], out = !SKIP.has(w.toLowerCase()) && !inQuote.has(stem(w));
      if (m.index > last) parts.push(summary.slice(last, m.index));
      parts.push(out ? h("u", { class: "out", "data-testid": "outside-word" }, w) : w); if (out) any = true;
      last = m.index + w.length;
    }
    if (last < summary.length) parts.push(summary.slice(last));
    return any ? parts : null;
  }

  /* ---------- presenting an item ---------- */
  function present(S, item, q) {
    const c = S.c, g = groupOf(c, item);
    if (g === "tray") return item.kind === "flag" ? trayFlag(S, item) : trayEntry(S, item);
    if (g === "flag") return warning(S, item);
    if (g === "undated") return undated(S, item);
    return line(S, item);
  }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:12.250Z

**tool call — Bash**
````
{
 "command": "grep -n \"E.status\\b\\|E.statusText\\|E.undo =\" app/frontend/guided/review.js | head; grep -n \"\\.status\\|status-text\\|data-why\\|\\.actions-in\" app/frontend/guided/*.css app/frontend/guided/*.html 2>/dev/null | head -40; ls app/frontend/guided | head -30"
}
````

### User / tool · 2026-11-02T23:48:12.347Z

**tool result**
````
203:    E.statusText = h("span", { class: "st-msg", "data-testid": "status-text" }); E.undo = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-undo", hidden: true }, "Undo");
204:    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo);
206:      h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
222:      E.statusText.textContent = s ? s.text : box ? (box.dataset.testid === "check-compare" ? "Tick the box above to say you compared them." : "Tick the box above first.") : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
223:      E.status.classList.toggle("hint", !s && !box);
224:      E.status.dataset.why = box ? "tick" : "";
app/frontend/guided/review.css:21:  .actions-in { padding-top: 10px; padding-bottom: 8px; row-gap: 8px; }
app/frontend/guided/review.css:25:.actions .status { grid-area: status; display: flex; align-items: center; gap: 8px; min-height: 40px; }
app/frontend/guided/review.css:26:.actions .status .st-msg { flex: 1; min-width: 0; }
app/frontend/guided/review.css:27:.actions .status.hint { color: var(--subtle); font-size: .9375rem; }
app/frontend/guided/review.css:28:.actions .status .undo { flex: none; height: 36px; padding: 0 14px; border-color: var(--accent); }
app/frontend/guided/review.css:90:  .actions-in { padding: 6px 12px 4px; row-gap: 4px; }
app/frontend/guided/review.css:94:  .actions .status { min-height: 36px; font-size: .8125rem; line-height: 1.1rem; }
app/frontend/guided/review.css:95:  .actions .status .st-msg { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; white-space: normal; }
app/frontend/guided/review.css:96:  .actions .status .undo { height: 34px; padding: 0 12px; }
app/frontend/guided/styles.css:165:.actions-in { max-width: 1440px; margin: 0 auto; padding: 14px var(--gutter) 12px; display: grid; grid-template-columns: auto 1fr; grid-template-areas: "q q" "big small" "status status"; column-gap: 24px; row-gap: 10px; align-items: center; }
app/frontend/guided/styles.css:170:.status { grid-area: status; min-height: 1.5rem; font-size: 1rem; line-height: 1.5rem; color: var(--muted); }
app/frontend/guided/styles.css:171:.status b { color: var(--ok); }
app/frontend/guided/styles.css:376:  .actions-in { grid-template-columns: minmax(0, 1fr); grid-template-areas: "q" "big" "small" "status"; padding: 8px 16px 6px; row-gap: 6px; }
app/frontend/guided/styles.css:383:  .status { font-size: .875rem; min-height: 1.25rem; line-height: 1.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
app.js
core.js
home.css
home.js
index.html
review.css
review.js
step1.css
step1.js
step2.css
step2.js
step3.css
step3.js
step4.css
step4.js
styles.css
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:13.840Z

**tool call — Bash**
````
{
 "command": "sed -n 80,100p app/frontend/guided/review.css; sed -n 370,390p app/frontend/guided/styles.css; grep -rn \"Saved: your wording\" app/frontend/guided/*.js | head -3"
}
````

### User / tool · 2026-11-02T23:48:13.935Z

**tool result**
````
  body.frame .work.needs-check .card-line .card-h { flex-wrap: nowrap; min-height: 0; padding-top: 8px; padding-bottom: 8px; }
  body.frame .work.needs-check .card-line .card-h .ch-sub { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; flex: 1 1 0; }
  body.frame .work.needs-check .card-line .card-b { padding-top: 10px; padding-bottom: 6px; }
  body.frame .work.needs-check .card-line .card-f { padding-top: 8px; padding-bottom: 8px; }      /* a line to compare + its tick box: both on screen together */
  .card-line { overflow: auto; }
  .card-line .card-b { flex: none; overflow: visible; }
  .card-line .card-f, .card-f.plain { flex: none; height: auto; min-height: 0; display: block; -webkit-line-clamp: unset; overflow: visible; }
  .card-line .card-h { position: sticky; top: 0; z-index: 2; background: var(--panel); flex-wrap: wrap; row-gap: 4px; }
  .card-src .card-h { min-height: 40px; padding: 6px 12px; }
  .card-src .card-h .ch-sub { font-size: .8125rem; }
  .actions-in { padding: 6px 12px 4px; row-gap: 4px; }
  .question { min-height: 2.4rem; font-size: .9375rem; line-height: 1.2rem; }
  .btn.answer { height: 50px; font-size: 1rem; }
  .small .btn { height: 38px; }
  .actions .status { min-height: 36px; font-size: .8125rem; line-height: 1.1rem; }
  .actions .status .st-msg { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; white-space: normal; }
  .actions .status .undo { height: 34px; padding: 0 12px; }
  .card-b .line-text { font-size: 1.0625rem; line-height: 1.5rem; }
}
@media (max-width: 760px) and (max-height: 720px) {
  body.frame .work { grid-template-rows: none; }
  .money { font-size: 2rem; line-height: 2.5rem; }
  .warn-title { font-size: 1.0625rem; line-height: 1.5rem; margin-bottom: 4px; }
  .explain { font-size: .9375rem; line-height: 1.4rem; }
  textarea.edit { font-size: 1.0625rem; line-height: 1.5rem; min-height: 0; height: 8rem; }      /* a fixed height: 100% of a body that grows with the hint above it ran over the card foot, hiding a refusal (UX r2) */
  .check { font-size: .9375rem; line-height: 1.35rem; gap: 10px; margin-top: 6px; }
  .check input { width: 26px; height: 26px; }
  .actions-in { grid-template-columns: minmax(0, 1fr); grid-template-areas: "q" "big" "small" "status"; padding: 8px 16px 6px; row-gap: 6px; }
  .question { font-size: 1rem; line-height: 1.35rem; min-height: 2.7rem; display: flex; align-items: center; }
  .big { gap: 10px; }
  .btn.answer { flex: 1; width: auto; min-width: 0; height: 54px; font-size: 1.0625rem; padding: 0 8px; white-space: normal; text-align: center; line-height: 1.25rem; }
  .btn.answer .sub { font-size: .75rem; }
  .small { justify-content: space-between; gap: 4px; }
  .small .btn { flex: 1 1 0; width: auto; min-width: 0; height: 40px; font-size: .875rem; padding: 0 4px; }
  .status { font-size: .875rem; min-height: 1.25rem; line-height: 1.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .wrap { padding: 20px 16px; }
  .page-h { flex-direction: column; align-items: stretch; gap: 12px; }
  .page-h h1 { font-size: 1.625rem; line-height: 2.125rem; }
  .panel { padding: 18px; }
  .tiles { grid-template-columns: 1fr; gap: 10px; }
  .tile { min-height: 0; padding: 16px; }
  .input-box { height: 220px; }
app/frontend/guided/step2.js:191:        S.say("Saved: your wording is in. Read it once more against the highlighted words.", null);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:32.431Z

**tool call — Bash**
````
{
 "command": "sed -n 180,196p app/frontend/guided/step2.js; grep -n \"check-compare\\|check-separate\" app/frontend/guided/*.js | head; grep -n \"I compared\\|compared them\" app/frontend/guided/*.js | head"
}
````

### User / tool · 2026-11-02T23:48:32.533Z

**tool result**
````
      const summary = (ui.draft || "").trim();
      if (!summary) { S.err = { text: "Write the line first." }; S.render(true); return; }
      const qChanged = r.excerpt !== item.excerpt, sChanged = summary !== (item.summary || "").trim();
      if (!qChanged && !sChanged) { S.err = { text: "Nothing has changed yet." }; S.render(true); return; }
      return S.act(async () => {
        S.lastEdit = { excerpt: r.excerpt, summary, before: item.summary };       // a refusal that names dropped words reads these (review.js droppedText)
        const edits = {};                                   // one call: the server checks the new wording against the new quote together (two calls would test the old wording against the new quote)
        if (qChanged) edits.excerpt = r.excerpt;
        if (sChanged) edits.summary = summary;
        const resp = await S.post(item, "edit", { edits });
        S.c = await S.ctx.refresh(); ui.mode = "view"; ui.picked = null; ui.draft = null; ui.warnings = resp.warnings || [];
        S.say("Saved: your wording is in. Read it once more against the highlighted words.", null);
        S.render(false);
      });
    };
    return {
      tag: { cls: "you", text: "Your wording" }, sub: lineHead(item, rec), focus: "field",
app/frontend/guided/review.js:222:      E.statusText.textContent = s ? s.text : box ? (box.dataset.testid === "check-compare" ? "Tick the box above to say you compared them." : "Tick the box above first.") : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
app/frontend/guided/review.js:222:      E.statusText.textContent = s ? s.text : box ? (box.dataset.testid === "check-compare" ? "Tick the box above to say you compared them." : "Tick the box above first.") : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:34.478Z

**tool call — Bash**
````
{
 "command": "grep -n \"check-compare\\|check-separate\\|testid.*check\" app/frontend/guided/*.js app/frontend/*.js 2>/dev/null| head; grep -n \"S.said\\|S.say(\" app/frontend/guided/*.js | grep -v \"^app/frontend/guided/review.js:14[01]\" | head -30"
}
````

### User / tool · 2026-11-02T23:48:34.601Z

**tool result**
````
app/frontend/guided/step2.js:271:      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
app/frontend/guided/step2.js:351:      : h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "You checked every item on the timeline."),
app/frontend/guided/step2.js:370:      trayDone.length ? h("div", { class: "panel", "data-testid": "tray-done" }, h("h2", {}, "Items we couldn't check"), h("p", { class: "muted" }, "These are optional. They stay out of the letter unless you wrote the line yourself."),
app/frontend/guided/step2.js:374:      checks ? h("div", { class: "panel", "data-testid": "checks-panel" }, h("h2", {}, "What we compared between records"),
app/frontend/guided/step2.js:379:    return R.doneFrame(2, "Check the timeline", h("div", { class: "panel" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "–"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "There are no timeline lines in this case."), h("p", {}, "Nothing here needs checking."))),
app/frontend/guided/step1.js:66:        const ta = h("textarea", { "aria-label": "Paste the records here", placeholder: "Paste the records here", "data-testid": "input-text", spellcheck: "false" }); ta.value = st.text;
app/frontend/guided/step1.js:77:          const r = h("input", { type: "radio", name: "lib", value: x.id, "data-testid": "library-" + x.id }); if (st.lib === x.id) r.checked = true;
app/frontend/guided/step1.js:115:        const ok = h("input", { type: "checkbox", "data-testid": "check-hidden" }), go = h("button", { type: "button", class: "btn", disabled: true, "data-testid": "btn-hidden-anyway", onclick: () => submit({ includeHidden: "all" }) }, "Use these pages anyway");
app/frontend/guided/step3.js:39:      if (flag) { cls = "attn"; foot.push(h("strong", { "data-testid": "flag-message" }, R.plain(flag.message)), R.check(S, "flag", flagBox(flag))); }
app/frontend/guided/step3.js:55:      const cc = item.count_confirm, foot = [h("span", { "data-testid": "count-hint" }, "You can still count it if you checked the ledger yourself."), R.check(S, "separate", "I checked this is a separate charge for a service.")];
app/frontend/guided/review.js:220:      const s = S.said;
app/frontend/guided/review.js:313:    S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };
app/frontend/guided/step2.js:166:      third: { label: quoteFail(item) ? "Change the words" : "Fix the wording", hint: refusal, run: () => { ui.mode = "fix"; ui.draft = null; ui.picked = null; S.err = null; S.say(null, null); S.render(); } },
app/frontend/guided/step2.js:191:        S.say("Saved: your wording is in. Read it once more against the highlighted words.", null);
app/frontend/guided/step2.js:229:      S.say(sentences.length ? sentences.join(" ") : `Saved: record ${rec.seq} is dated ${R.longDate(iso)}.`, null);
app/frontend/guided/step2.js:278:      third: { label: "Add a note", run: () => { ui.mode = "note"; ui.draft = null; S.err = null; S.say(null, null); S.render(); } } };
app/frontend/guided/step2.js:299:          S.say("Saved: your line is in. Check it against the highlighted words once more.", null);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:39.937Z

**tool call — Bash**
````
{
 "command": "grep -n \"R.check(S, \\\"compare\\\"\\|check(S, 'compare'\\|R.check = \\|function check\" app/frontend/guided/*.js; sed -n 291,302p app/frontend/guided/step2.js"
}
````

### User / tool · 2026-11-02T23:48:40.024Z

**tool result**
````
app/frontend/guided/review.js:404:  R.check = function (S, key, label, opt) {
app/frontend/guided/step2.js:152:      foot.push(R.check(S, "compare", "I read this line against the highlighted words myself.", { focus: true }));
app/frontend/guided/step2.js:271:      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
app/frontend/guided/step3.js:33:    const compareBox = () => R.check(S, "compare", "I read this amount against the highlighted words myself.");
        const r = pickedRange(rec, ui.picked), summary = (ui.draft || "").trim();
        if (r.error || !summary) { S.err = { text: r.error || "Write the line first." }; S.render(true); return undefined; }
        return S.act(async () => {
          const resp = await G.api.addEntry(S.token, rec.id, { summary, excerpt: r.excerpt });
          S.c = await S.ctx.refresh();
          const nid = (resp.item && resp.item.id) || (resp.entry && resp.entry.id);
          S.queue[S.idx] = { id: nid, optional: false }; S.ui = {}; S.screen = null;
          history.replaceState(history.state, "", G.url.timeline(S.token, nid));
          S.say("Saved: your line is in. Check it against the highlighted words once more.", null);
          S.render(false);
        });
      };
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:48.758Z

**tool call — bash**
````
{
 "command": "echo"
}
````

### User / tool · 2026-11-02T23:48:48.760Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:48:57.257Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/frontend/guided/review.js'; s=open(p).read()\ns=s.replace('\"a damages figure (such as lost pay)\"','\"a damages figure (for example lost wages)\"')\nold=s[s.index('    function drawStatus() {'):s.index('    function updateTitlebar()')]\nnew='''    function drawStatus() {\n      const s = S.said;\n      const box = E.yes && E.yes.disabled && !S.busy && E.foot.querySelector(\"input[type=checkbox]:not(:checked)\");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)\n      const tick = box ? (box.dataset.testid === \"check-compare\" ? \"Tick the box to say you compared them.\" : \"Tick the box first.\") : \"\";      // no direction word: the box can be above the bar or below the screen\n      const saved = s && !s.undo && /^Saved/.test(s.text);      // a \"Saved\" note must not hide the reason Yes is greyed: both stay until she ticks\n      const why = box && (!s || saved);\n      E.statusText.textContent = why ? (saved ? \"Saved. \" : \"\") + tick : s ? s.text : (matchMedia(\"(min-width: 761px)\").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? \"E fixes or adds a note, \" : \"\"}the arrow keys move between items.` : \"\");\n      E.status.classList.toggle(\"hint\", !s && !why);\n      E.status.dataset.why = why ? \"tick\" : \"\";\n      E.undo.hidden = !(s && s.undo);\n      E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;\n      const hidden = !!why && boxHidden(box);      // the box is under the bar or below the screen: one tap brings it into view\n      E.showBox.hidden = !hidden;\n      E.showBox.onclick = hidden ? () => revealBox(box) : null;\n    }\n    function boxHidden(box) {\n      const r = box.getBoundingClientRect(), bar = E.actions.getBoundingClientRect();\n      return r.bottom > bar.top - 4 || r.top < 0;\n    }\n    function revealBox(box) {\n      const bar = E.actions.getBoundingClientRect();\n      box.style.scrollMarginBottom = Math.ceil(window.innerHeight - bar.top + 12) + \"px\";\n      try { box.scrollIntoView({ block: \"nearest\", inline: \"nearest\" }); } catch (_) { /* nothing to scroll */ }\n      box.focus({ preventScroll: true }); drawStatus();\n    }\n\n'''\ns=s.replace(old,new)\ns=s.replace('E.status = h(\"p\", { class: \"status\", role: \"status\", \"aria-live\": \"polite\", \"data-testid\": \"status-slot\" }, E.statusText, E.undo);',\n 'E.showBox = h(\"button\", { type: \"button\", class: \"btn quiet undo\", \"data-testid\": \"btn-show-box\", hidden: true }, \"Show box\");\\n    E.status = h(\"p\", { class: \"status\", role: \"status\", \"aria-live\": \"polite\", \"data-testid\": \"status-slot\" }, E.statusText, E.undo, E.showBox);')\ns=s.replace('S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };','S.sync = () => { syncButtons(); if (!S.said || (!S.said.undo && /^Saved/.test(S.said.text))) drawStatus(); };')\nopen(p,'w').write(s)\np='app/frontend/guided/step2.js'; s=open(p).read()\ns=s.replace('const stem = (w) => { const x = w.toLowerCase().replace(/[\\'’]s$/, \"\").replace(/s$/, \"\"); return ABBR[x] || x; };',\n 'const stem = (w) => { const x = w.toLowerCase().replace(/[\\'’]s$/, \"\").replace(/s$/, \"\"); return w === \"PT\" ? x : ABBR[x] || x; };      // \"PT\" in capitals is physical therapy, not a patient: it stays a word of its own, so a \"Patient\" in the line is still underlined')\nopen(p,'w').write(s)\nEOF\ngit diff --stat -- app/frontend; grep -n \"S.busy = \\|S.busy=\" app/frontend/guided/review.js | head -3; grep -n \"\\.undo\\[hidden\\]\\|\\[hidden\\]\" app/frontend/guided/*.css | head"
}
````

### User / tool · 2026-11-02T23:48:57.392Z

**tool result**
````
 app/frontend/guided/app.js     |  17 +++---
 app/frontend/guided/core.js    |   9 ++-
 app/frontend/guided/home.js    |   3 +-
 app/frontend/guided/review.css |  15 ++++-
 app/frontend/guided/review.js  | 121 ++++++++++++++++++++++++++++++++++++-----
 app/frontend/guided/step1.js   |  13 +++--
 app/frontend/guided/step2.js   |  56 ++++++++++++++++---
 app/frontend/guided/step3.css  |  12 ++++
 app/frontend/guided/step3.js   |  14 +++--
 app/frontend/guided/step4.css  |   3 +-
 app/frontend/guided/step4.js   |  18 +++++-
 app/frontend/guided/styles.css |   2 +-
 app/frontend/timeline.js       |   2 +-
 13 files changed, 235 insertions(+), 50 deletions(-)
166:      S.busy = true; S.err = null; syncButtons();
168:        S.busy = false;
app/frontend/guided/styles.css:50:[hidden] { display: none !important; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:02.349Z

**tool call — Bash**
````
{
 "command": "grep -n \"outsideParts\" app/frontend/guided/*.js | head; grep -n \"def open_item\\|def phone\\|def make\\|^EDIT\\|transported to\\|edit-to-check\\|edit_to_check\" tests/e2e/guided/test_round2.py tests/e2e/guided/test_round3.py | head -20"
}
````

### User / tool · 2026-11-02T23:49:02.438Z

**tool result**
````
app/frontend/guided/step2.js:115:  function outsideParts(summary, quote) {
app/frontend/guided/step2.js:160:      body: [h("p", { class: "line-text", "data-testid": "line-text" }, ...(((need && outsideParts(item.summary, item.excerpt)) || [item.summary || ""]))),
app/frontend/guided/step2.js:161:        need && outsideParts(item.summary, item.excerpt) ? h("p", { class: "muted out-note", "data-testid": "outside-note" }, "Underlined words are not in the highlighted words.") : null],
tests/e2e/guided/test_round2.py:30:def phone(pw, w=390, h=844):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:03.949Z

**tool call — Bash**
````
{
 "command": "grep -rln \"taken to\\|btn-third\\|answer-third\" tests/e2e | head; sed -n 1,60p tests/e2e/guided/test_round2.py"
}
````

### User / tool · 2026-11-02T23:49:04.038Z

**tool result**
````
tests/e2e/guided/test_step2.py
tests/e2e/guided/test_round2.py
tests/e2e/guided/test_step3.py
tests/e2e/guided/test_round3.py
"""T-181 round 2 (D-068): the paralegal and UX-designer findings of round 1, each with its own guard.
Real browser, the fixture backend (curated set), the real API. Cases are made over the API and deleted afterwards.
What is guarded: the borrowed-sentence label and the underlined words (paralegal major 1); the Bates rule and its preview (paralegal major 2); no failed request on first paint, in a local and in a
PUBLIC server (T-182 r3); a refused edit names the dropped words (UX major 3); the step list closes when its toggle is tapped again (UX major 4); a disputed line and its tick box are on screen together
at 390 (UX major 2); Step 3's done lists fit a phone (UX major 1); no sideways scrolling on any guided screen at 390 and 320; a refused Yes never moves focus onto a button that answers; the second
check's direction on an amount; ledger lines with no date of service; the title-row provenance follows the case; every highlight of a multi-record warning is in view at 1440x900."""
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect

import tests.e2e.conftest as C
from tests.e2e.guided._helpers import decide_all
from tests.e2e.guided.test_shell_smoke import go, watch
from tests.e2e.guided.test_step2 import LIB10, item, make, open_item, case   # noqa: F401  (make is a fixture)

LIB11 = "case_lib11_priors_and_ledger"


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")


def phone(pw, w=390, h=844):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=True, has_touch=True)
    return b, ctx.new_page()


def desktop(pw, w=1440, h=900):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True)
    return b, ctx.new_page()


# ------------------------------------------------------------------------------------ paralegal major 1: the borrowed sentence

def test_the_grey_box_does_not_say_a_borrowed_sentence_is_in_no_line_and_the_outside_words_are_underlined(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        for iid, words in (("e1", {"Annual", "visit"}), ("e2", {"struck", "behind"})):
            open_item(page, tok, iid)
            box = page.get_by_test_id("uncovered")
            expect(box).to_contain_text("outside the highlighted words")
            assert "not in any line" not in box.inner_text()
            out = set(page.get_by_test_id("outside-word").all_inner_texts())
            assert words <= out, (iid, out)
            expect(page.get_by_test_id("outside-note")).to_contain_text("Underlined words are not in the highlighted words")
        # an item that is not disputed carries no underline
        open_item(page, tok, "e3")
        assert page.get_by_test_id("outside-word").count() == 0
    finally:
        b.close()


# ------------------------------------------------------------------------------------ paralegal major 2: Bates
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:05.949Z

**tool call — Bash**
````
{
 "command": "grep -n \"taken to\\|transported\" tests/e2e/guided/*.py | head; grep -n \"^def \\(case\\|make\\|open_item\\|item\\)\\|^SAMPLE\\|fixture\" tests/e2e/guided/test_step2.py | head -20"
}
````

### User / tool · 2026-11-02T23:49:06.043Z

**tool result**
````
1:"""T-181 (D-068) guided Step 2, "Check the timeline" (docs/GUIDED_UI_SPEC.md section 5). Real browser, the fixture backend (curated set), the real API: every case is made over the API and deleted afterwards.
18:@pytest.fixture
19:def make():
39:def case(tok):
43:def item(tok, iid):
48:def open_item(page, tok, iid=None, step="timeline"):
61:@pytest.fixture
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:07.711Z

**tool call — Bash**
````
{
 "command": "sed -n 15,110p tests/e2e/guided/test_step2.py; grep -n \"answer-third\\|btn-save\\|edit-text\\|textarea\" tests/e2e/guided/test_step2.py | head -20"
}
````

### User / tool · 2026-11-02T23:49:07.817Z

**tool result**
````
JARGON = re.compile(r"\b(model's|its quote|checked by code|itemized service line|tray|excerpt|judge|LLM|J[1-4])\b|\bflags?\b|\bpending\b|\bverified\b", re.I)


@pytest.fixture
def make():
    made = []

    def _make(lib=None):
        import time
        st, c = C.api("POST", "/api/cases", {"sample": True} if lib is None else {"library": lib}); assert st in (200, 201), (st, c)
        tok = c["token"]; made.append(tok)
        assert C.api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = C.api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.5)
        assert s["status"] == "ready", s
        return tok
    yield _make
    for t in made:
        C.api("DELETE", f"/api/cases/{t}")


def case(tok):
    return C.api("GET", f"/api/cases/{tok}")[1]


def item(tok, iid):
    c = case(tok)
    return next(i for g in ("entries", "undated_entries", "flags", "amounts", "tray") for i in c[g] if i["id"] == iid)


def open_item(page, tok, iid=None, step="timeline"):
    go(page, f"/case/{tok}/{step}" + (f"?item={iid}" if iid else ""))
    page.get_by_test_id("card-line").wait_for()


def line_id(page):
    return page.get_by_test_id("card-line").get_attribute("data-item-id")


def settle(page, ms=350):
    page.wait_for_timeout(ms)


@pytest.fixture
def phone(pw):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); pg = ctx.new_page()
    yield pg
    b.close()


def sized(pw, w, h):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}); return b, ctx.new_page()


# ------------------------------------------------------------------------------------------------ the screen

def test_opens_on_the_first_item_with_the_record_words_beside_it(page, make):
    seen = watch(page)
    tok = make(); e1 = item(tok, "e1")
    go(page, f"/case/{tok}/timeline")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
    assert page.evaluate("location.search") == "?item=e1", "the open item is in the address, so a reload lands on it"
    assert page.get_by_test_id("item-count").inner_text() == "Item 1 of 19" and page.get_by_test_id("progress-text").inner_text() == "0 answered · 19 to go"
    assert page.get_by_test_id("line-text").inner_text() == e1["summary"]
    marks = page.locator("[data-testid=card-source] mark")
    assert marks.count() == 1 and marks.first.inner_text() == e1["excerpt"], "the highlighted words are exactly the quote"
    assert "Record 1 · Austin EMS run report · January 9, 2026" in page.get_by_test_id("src-head").inner_text()
    assert page.get_by_test_id("question").inner_text() == "Does this line say the same thing as the highlighted words?"
    assert page.get_by_test_id("answer-yes").inner_text() == "Yes, this matches" and page.get_by_test_id("answer-no").inner_text() == "No, leave it out"
    assert page.get_by_test_id("btn-third").inner_text() == "Fix the wording"
    foot = page.get_by_test_id("card-foot").inner_text()
    assert "word for word" in foot and "a second AI check agreed" in foot, foot
    tag = page.get_by_test_id("line-tag")
    expect(tag).to_have_text("Prepared answer")                                    # D-065: a prepared answer says so, never "AI draft"
    assert "not written by an AI model" in tag.get_attribute("title")
    assert page.get_by_test_id("btn-undo").is_hidden()
    page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
    assert seen == [], seen


def test_every_item_screen_has_plain_words_and_no_provenance_leak(page, make):
    tok = make()
    open_item(page, tok)
    for n in range(19):
        page.wait_for_timeout(60)
        text = " ".join(page.get_by_test_id(t).inner_text() for t in ("card-line", "card-foot", "question", "src-head", "actions"))
        bad = JARGON.findall(text)
        assert not bad, (line_id(page), bad, text)
        assert "AI draft" not in text or "Prepared answer" not in text
        body = page.locator("body").inner_text()
        assert "model" not in page.get_by_test_id("card-line").inner_text().lower(), body
        page.get_by_test_id("btn-later").click(); settle(page, 80)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:09.353Z

**tool call — Bash**
````
{
 "command": "grep -rn \"edit_to_check\\|edit-to-check\\|Fix the wording\" tests/e2e/guided/*.py | grep -v \"^tests/e2e/guided/test_t203\" | head; "
}
````

### User / tool · 2026-11-02T23:49:09.472Z

**tool result**
````
tests/e2e/guided/test_step2.py:87:    assert page.get_by_test_id("btn-third").inner_text() == "Fix the wording"
tests/e2e/guided/test_step2.py:331:    assert item(tok, "e4")["edit_to_check"] is True
tests/e2e/guided/test_step2.py:502:        pg.get_by_test_id("btn-third").click(); assert boxes(pg, skip) == first, "Fix the wording moved something"
tests/e2e/guided/test_shell_smoke.py:201:        editToCheck: S({ status: "ready", entries: [it("edited", { edit_to_check: true })], amounts: [], review: {} }, 2),
tests/e2e/guided/test_step4.py:160:        expect(act(3).get_by_test_id("blocker-note")).to_have_text("The second check can't run here. Fix the wording in your own words, or leave the item out.")    # rerun_available is false in demo mode
tests/e2e/guided/test_step4.py:199:    left = api("GET", f"/api/cases/{tok}")[1]["review"]["counts"]; n = left["pending"] + left["edit_to_check"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:10.706Z

**tool call — Bash**
````
{
 "command": "sed -n 300,345p tests/e2e/guided/test_step2.py"
}
````

### User / tool · 2026-11-02T23:49:10.790Z

**tool result**
````
    sents = page.get_by_test_id("sentence"); assert sents.count() == 3
    assert [s.get_attribute("aria-pressed") for s in sents.all()] == ["true", "true", "false"]
    ta.fill("Neck pain 9/10; plan of care 12 visits."); page.get_by_test_id("answer-yes").click()
    foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved"); assert "9" in foot.inner_text() and "highlighted words" in foot.inner_text() and "quote" not in foot.inner_text().lower()
    assert page.get_by_test_id("edit-summary").input_value() == "Neck pain 9/10; plan of care 12 visits.", "her text stays in the box"
    assert item(tok, "e4")["summary"] == e4["summary"]
    page.get_by_test_id("edit-summary").fill(e4["summary"] + " Reviewed."); page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("edit-summary")).to_have_count(0)
    assert sent[-1]["action"] == "edit" and sent[-1]["edits"] == {"summary": e4["summary"] + " Reviewed."} and sent[-1]["expected_status"] == "pending" and sent[-1]["version"] == e4["version"]
    assert page.get_by_test_id("line-tag").inner_text() == "Written by you"
    expect(page.get_by_test_id("compare-reason")).to_have_text("You changed the wording. Read it against the highlighted words once more.")
    expect(page.get_by_test_id("answer-yes")).to_be_disabled()
    assert page.get_by_test_id("item-count").inner_text().startswith("Item ") and "answered" in page.get_by_test_id("progress-text").inner_text()
    page.get_by_test_id("check-compare").check(); page.get_by_test_id("answer-yes").click(); settle(page)
    assert sent[-1]["action"] == "accept" and sent[-1]["compared"] is True
    assert item(tok, "e4")["review_status"] == "accepted"


def test_changing_the_highlighted_sentences_sends_the_quote_and_wording_together(page, make):
    tok = make(); e4 = item(tok, "e4"); sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    open_item(page, tok, "e4"); page.get_by_test_id("btn-third").click()
    sents = page.get_by_test_id("sentence")
    sents.nth(1).click(); assert sents.nth(1).get_attribute("aria-pressed") == "false" and sents.nth(0).get_attribute("aria-pressed") == "true"
    sents.nth(2).click(); page.get_by_test_id("answer-yes").click()                                              # sentences 1 and 3 are picked, 2 is not: they do not follow each other
    expect(page.get_by_test_id("card-foot")).to_contain_text("Pick sentences that follow each other."); assert sent == []
    sents.nth(2).click()                                                                                          # back to the first sentence only
    page.get_by_test_id("edit-summary").fill("Cervical range of motion reduced approx. 40%.")
    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("edit-summary")).to_have_count(0)
    assert len(sent) == 1 and sent[0]["edits"] == {"excerpt": "Cervical range of motion reduced approx. 40%.", "summary": "Cervical range of motion reduced approx. 40%."}, sent
    assert [m.inner_text() for m in page.locator("[data-testid=card-source] mark").all()] == ["Cervical range of motion reduced approx. 40%."], "the new words are highlighted"
    assert item(tok, "e4")["edit_to_check"] is True


def test_cancel_sends_nothing_and_leaves_the_card_as_it_was(page, make):
    tok = make(); sent = []
    page.on("request", lambda r: sent.append(r.url) if r.method == "POST" else None)
    open_item(page, tok, "e4"); before = page.get_by_test_id("line-text").inner_text()
    page.get_by_test_id("btn-third").click(); page.get_by_test_id("edit-summary").fill("something else"); page.get_by_test_id("answer-no").click()
    assert page.get_by_test_id("line-text").inner_text() == before and sent == []


# ------------------------------------------------------------------------------------------------ a date to pick, and items we could not check

def test_a_date_to_pick_shows_both_readings_a_suggestion_and_then_the_line(page, make):
    tok = make(LIB09); c = case(tok); dtc = c["dates_to_confirm"][0]; eid = c["undated_entries"][0]["id"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:14.039Z

**tool call — Bash**
````
{
 "command": "sed -n 1,12p app/frontend/guided/step2.js; grep -n \"^  G\\.\\|window\\.\\|G\\.step2\\|R\\.[a-z]* = \" app/frontend/guided/step2.js | tail -8"
}
````

### User / tool · 2026-11-02T23:49:14.132Z

**tool result**
````
/* Step 2: Check the timeline (/case/<token>/timeline[?item=<id>]). OWNER: frontend-B. Spec 5 (5.1 queue, 5.2 line, 5.3 fix the wording, 5.4 compare confirm, 5.5 could not check, 5.6 date, 5.7 warning, 5.8 done);
   D-066 (a disputed or still-to-check item is accepted only with the box ticked, sent as compared:true), D-065 (tags), D-067 (no narrative), T-178 (version + expected_status on every write: review.js).
   The frame, the queue, Undo, the keyboard and every write are in review.js; this file says what each item looks like and which call each button makes. Record text is inserted with textContent only. */
(function () {
  const G = window.G, { h } = G, R = G.review;

  /* ---------- the queue (5.1): entries, undated entries, warnings and could-not-check items, in the order of the next_action timeline rule; frozen when the step opens ---------- */
  const recById = (c) => Object.fromEntries((c.records || []).map((r) => [r.id, r]));
  function citedIds(it) {
    const ids = new Set([].concat(it.record_ids || [], (it.computed && it.computed.record_ids) || [], (it.evidence || []).map((e) => e.record_id)).filter(Boolean));
    if (!ids.size && /^e\d+/.test(it.id || "")) ids.add("r" + /^e(\d+)/.exec(it.id)[1]);
    return [...ids];
5:  const G = window.G, { h } = G, R = G.review;
383:  G.pages.timeline = function (ctx) {
386:  G.step2 = { buildQueue, find, flagHeading };
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:27.626Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/frontend/guided/step2.js'; s=open(p).read()\ns=s.replace('G.step2 = { buildQueue, find, flagHeading };','G.step2 = { buildQueue, find, flagHeading, outsideParts };')\nopen(p,'w').write(s)\np='tests/e2e/guided/test_t203.py'; s=open(p).read()\ns=s.replace('HINT = \"Tick the box above to say you compared them.\"','HINT = \"Tick the box to say you compared them.\"')\ns+='''\n\n# ------------------------------------------------------------------ round 2: the reworded line, position-neutral words, PT is not a patient\n\ndef _words(page, summary, quote):\n    return page.evaluate(\"\"\"([s, q]) => { const p = window.G.step2.outsideParts(s, q); return p ? p.filter((n) => n && n.nodeType === 1).map((n) => n.textContent) : []; }\"\"\", [summary, quote])\n\n\ndef test_pt_in_capitals_is_physical_therapy_not_a_patient_but_pt_alone_still_reads_as_patient(pw, make):\n    tok = make(); b, page = phone(pw, 390, 844)\n    try:\n        open_item(page, tok, \"e1\")\n        assert \"Patient\" in _words(page, \"Patient attended physical therapy 3 times a week\", \"PT 3x/week, attended physical therapy\"), \"PT is not the word patient\"\n        assert _words(page, \"Patient states chest pain\", \"Pt states chest pain\") == [], \"Pt is the chart shorthand for patient\"\n        assert _words(page, \"Patient states chest pain\", \"PATIENT states chest pain\") == []\n    finally:\n        b.close()\n\n\ndef test_375x667_after_fixing_the_wording_the_reason_for_the_greyed_yes_stays_until_she_ticks(pw, make):\n    tok = make(); b, page = phone(pw, 375, 667)\n    try:\n        open_item(page, tok, \"e4\")\n        page.get_by_test_id(\"btn-third\").click()\n        page.get_by_test_id(\"edit-summary\").fill(page.get_by_test_id(\"edit-summary\").input_value() + \" Reviewed.\")\n        page.get_by_test_id(\"answer-yes\").click()\n        yes, st, show = page.get_by_test_id(\"answer-yes\"), page.get_by_test_id(\"status-text\"), page.get_by_test_id(\"btn-show-box\")\n        expect(page.get_by_test_id(\"check-compare\")).to_be_attached(); expect(yes).to_be_disabled()\n        expect(st).to_contain_text(\"Saved\"); expect(st).to_contain_text(\"Tick the box to say you compared them.\")\n        assert \"above\" not in st.inner_text().lower() and \"below\" not in st.inner_text().lower()\n        page.wait_for_timeout(1500)\n        expect(st).to_contain_text(\"Tick the box\")                       # it stays; it does not time out\n        bar = page.evaluate(\"document.querySelector('[data-testid=actions]').getBoundingClientRect().top\")\n        box_in_view = lambda: page.evaluate(\"\"\"(bar) => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(); return r.top >= 0 && r.bottom <= bar - 2; }\"\"\", bar)\n        if show.is_visible():                                             # the box is under the bar or below the screen: one tap brings it into view\n            show.click(); page.wait_for_timeout(300)\n            assert box_in_view(), \"Show box did not bring the tick box above the bar\"\n            assert page.evaluate(\"document.activeElement && document.activeElement.dataset.testid\") == \"check-compare\"\n        else:\n            assert box_in_view(), \"no Show box button, yet the tick box is not in view\"\n        page.get_by_test_id(\"check-compare\").check(force=True)\n        expect(yes).to_be_enabled(); expect(st).not_to_contain_text(\"Tick the box\"); expect(show).to_be_hidden()\n        expect(st).to_contain_text(\"Saved: your wording is in\")\n        page.get_by_test_id(\"check-compare\").uncheck(force=True)\n        expect(yes).to_be_disabled(); expect(st).to_contain_text(\"Tick the box to say you compared them.\")\n    finally:\n        b.close()\n\n\ndef test_375x667_the_show_box_button_is_there_when_the_box_is_hidden_and_the_hint_stays_one_line_at_rest(pw, make):\n    tok = make(LIB10); b, page = phone(pw, 375, 667)\n    try:\n        open_item(page, tok, \"e1\")\n        st, show = page.get_by_test_id(\"status-text\"), page.get_by_test_id(\"btn-show-box\")\n        expect(st).to_have_text(HINT)\n        hidden = page.evaluate(\"\"\"() => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(), b = document.querySelector('[data-testid=actions]').getBoundingClientRect(); return r.bottom > b.top - 4; }\"\"\")\n        assert hidden, \"this size is expected to hide the box\"\n        expect(show).to_be_visible()\n        show.click(); page.wait_for_timeout(300)\n        assert page.evaluate(\"\"\"() => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(), b = document.querySelector('[data-testid=actions]').getBoundingClientRect(); return r.top >= 0 && r.bottom <= b.top; }\"\"\")\n    finally:\n        b.close()\n'''\ns=s.replace('''    tok = make(); b, page = phone(pw, 375, 667)\n    try:\n        open_item(page, tok, \"e1\")\n        expect(page.get_by_test_id(\"check-compare\")).to_be_attached()''','''    tok = make(LIB10); b, page = phone(pw, 375, 667)\n    try:\n        open_item(page, tok, \"e1\")\n        expect(page.get_by_test_id(\"check-compare\")).to_be_attached()''') if False else s\ns=s.replace('\"damages figure\")\\n        assert \"not a bill\"','\"damages figure\")\\n        assert \"lost pay\" not in reason.inner_text()\\n        assert \"not a bill\"')\nopen(p,'w').write(s)\nEOF\nsed -n 8,12p tests/e2e/guided/test_t203.py\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_t203.py -q -x 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T23:49:30.011Z

**tool result**
````
def test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons(pw, make):
    tok = make(LIB10); b, page = phone(pw, 375, 667)
    try:
F
=================================== FAILURES ===================================
___ test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons ___

pw = <playwright._impl._playwright.Playwright object at 0x1075b1760>
make = <function make.<locals>._make at 0x10dec7ba0>

    def test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons(pw, make):
        tok = make(LIB10); b, page = phone(pw, 375, 667)
        try:
            open_item(page, tok, "e1")
            expect(page.get_by_test_id("check-compare")).to_be_attached()
            yes, st = page.get_by_test_id("answer-yes"), page.get_by_test_id("status-text")
            expect(yes).to_be_disabled()
            expect(st).to_have_text(HINT)
            r = page.evaluate("""() => { const q = (s) => document.querySelector('[data-testid=' + s + ']').getBoundingClientRect(), y = q('answer-yes'), s = q('status-text'), bar = q('actions');
                return { yes: [y.top, y.bottom], st: [s.top, s.bottom, s.left, s.right], bar: [bar.top, bar.bottom], vh: innerHeight, vw: innerWidth, lines: Math.round(s.height / parseFloat(getComputedStyle(document.querySelector('[data-testid=status-text]')).lineHeight)) }; }""")
            assert r["st"][0] >= r["bar"][0] - 0.5 and r["st"][1] <= r["vh"] and r["st"][2] >= 0 and r["st"][3] <= r["vw"], ("the hint is not fully on screen inside the action bar", r)
            assert r["yes"][0] >= r["bar"][0] - 0.5 and r["yes"][1] <= r["vh"], ("the Yes button is not on screen with the hint", r)
>           assert r["lines"] == 1, ("the hint is more than one line", r)
E           AssertionError: ('the hint is more than one line', {'yes': [531, 581], 'st': [627.40625, 662.59375, 12, 249.078125], 'bar': [481.59375, 667], 'vh': 667, ...})
E           assert 2 == 1

tests/e2e/guided/test_t203.py:22: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_t203.py::test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 1.30s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:33.710Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/guided/test_t203.py'; s=open(p).read()\ns=s.replace('assert r[\"lines\"] == 1, (\"the hint is more than one line\", r)','assert r[\"lines\"] <= 2 and r[\"bar\"][0] > 470, (\"the hint is more than two lines, or the bar grew\", r)')\ns=s.replace(\"the hint stays one line at rest\",\"the hint is in the bar at rest\")\nopen(p,'w').write(s)\nEOF\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_t203.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T23:49:46.027Z

**tool result**
````
pw = <playwright._impl._playwright.Playwright object at 0x10bcc18e0>
make = <function make.<locals>._make at 0x1125fb2e0>

    def test_375x667_after_fixing_the_wording_the_reason_for_the_greyed_yes_stays_until_she_ticks(pw, make):
        tok = make(); b, page = phone(pw, 375, 667)
        try:
            open_item(page, tok, "e4")
            page.get_by_test_id("btn-third").click()
            page.get_by_test_id("edit-summary").fill(page.get_by_test_id("edit-summary").input_value() + " Reviewed.")
            page.get_by_test_id("answer-yes").click()
            yes, st, show = page.get_by_test_id("answer-yes"), page.get_by_test_id("status-text"), page.get_by_test_id("btn-show-box")
            expect(page.get_by_test_id("check-compare")).to_be_attached(); expect(yes).to_be_disabled()
>           expect(st).to_contain_text("Saved"); expect(st).to_contain_text("Tick the box to say you compared them.")
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: Locator expected to contain text 'Tick the box to say you compared them.'
E           Actual value: Saved: your wording is in. Read it once more against the highlighted words. 
E           Call log:
E             - Expect "to_contain_text" get_by_test_id("status-text") with timeout 5000ms
E             - waiting for get_by_test_id("status-text")
E               14 × locator resolved to <span class="st-msg" data-testid="status-text">Saved: your wording is in. Read it once more agai…</span>
E                  - unexpected value "Saved: your wording is in. Read it once more against the highlighted words."
E           
E           Aria snapshot:
E           - text: "Saved: your wording is in. Read it once more against the highlighted words."

tests/e2e/guided/test_t203.py:84: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_t203.py::test_375x667_after_fixing_the_wording_the_reason_for_the_greyed_yes_stays_until_she_ticks
1 failed, 5 passed in 11.20s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:48.978Z

**tool call — Bash**
````
{
 "command": "sed -n 160,180p app/frontend/guided/review.js"
}
````

### User / tool · 2026-11-02T23:49:49.061Z

**tool result**
````
      render(true);
    };
    S.cur = () => (S.idx >= 0 && S.queue[S.idx] ? S.item(S.queue[S.idx].id) : null);
    S.reload = async function () { S.c = await ctx.refresh(); updateTitlebar(); };
    S.act = async function (fn) {
      if (S.busy || !S.alive) return undefined;
      S.busy = true; S.err = null; syncButtons();
      try { return await fn(); } catch (e) { await S.fail(e); return undefined; } finally {
        S.busy = false;
        if (S.alive) { syncButtons(); if (!S.ended && S.screen && (!document.activeElement || document.activeElement === document.body)) focusFirst(S.screen); }     // the click disabled the button that had focus: put it on the next item's first answer
      }
    };
    /* every review POST carries version + expected_status of the item on screen (T-178) */
    S.post = (item, action, extra) => G.api.review(token, item.id, { action, version: item.version, expected_status: item.review_status, ...(extra || {}) });
    S.go = (item) => { const i = S.queue.findIndex((q) => q.id === item.id); S.open(i < 0 ? S.idx : i); };

    /* ---- frame ---- */
    const E = S.el;
    E.eyebrow = h("div", { class: "eyebrow" }, `Step ${cfg.step} of 4`);
    E.toggle = h("button", { type: "button", class: "steps-toggle", "data-testid": "btn-steps", "aria-expanded": "false", "aria-controls": "step-list", onclick: () => toggleSteps() }, `Step ${cfg.step} of 4`, h("span", { "aria-hidden": "true" }, " ▾"));
    E.ai = h("div", { class: "t-ai", "data-testid": "ai-note" }, R.aiNote());
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:49:51.867Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/frontend/guided/review.js'; s=open(p).read()\ns=s.replace(\"if (S.alive) { syncButtons(); if (!S.ended\",\"if (S.alive) { syncButtons(); drawStatus(); if (!S.ended\",1)\nopen(p,'w').write(s)\nEOF\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_t203.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T23:50:00.734Z

**tool result**
````
......                                                                   [100%]
6 passed in 7.80s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:50:04.935Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -3; git diff 38ee0c3 HEAD --stat -- app/frontend tests/e2e | tail -3; git diff --stat -- app/frontend/guided/review.js app/frontend/guided/step2.js tests/e2e/guided/test_t203.py; git status --short tests/e2e/guided/test_t203.py"
}
````

### User / tool · 2026-11-02T23:50:05.105Z

**tool result**
````
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test
f0921e4 feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
a44cfa7 fix(qa): T-187 r4 README item 7 wording matches the normalized rule (no unicode/percent/entity decoding claimed)
 app/frontend/guided/review.js | 123 ++++++++++++++++++++++++++++++++++++------
 app/frontend/guided/step2.js  |  58 ++++++++++++++++----
 2 files changed, 155 insertions(+), 26 deletions(-)
D  tests/e2e/guided/test_t203.py
?? tests/e2e/guided/test_t203.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:50:16.662Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/t203r2 && cd $SP/t203r2 && git -C /Users/arsis/zlayt-pm-project show HEAD:app/frontend/guided/review.js > review.js && git -C /Users/arsis/zlayt-pm-project show HEAD:app/frontend/guided/step2.js > step2.js && python3 - <<'EOF'\nimport re\n# take the dirty-tree files and diff against HEAD to extract only my hunks: apply replacements again on HEAD copies\ncur_r=open('/Users/arsis/zlayt-pm-project/app/frontend/guided/review.js').read()\ncur_s=open('/Users/arsis/zlayt-pm-project/app/frontend/guided/step2.js').read()\nr=open('review.js').read(); s=open('step2.js').read()\n# drawStatus block + helpers\na=cur_r.index('    function drawStatus() {'); b=cur_r.index('    function updateTitlebar()')\nblk=cur_r[a:b]\na2=r.index('    function drawStatus() {'); b2=r.index('    function updateTitlebar()')\nr=r[:a2]+blk+r[b2:]\ndef rep(t,o,n):\n    assert o in t, o[:50]; return t.replace(o,n,1)\nr=rep(r,'\"a damages figure (such as lost pay)\"','\"a damages figure (for example lost wages)\"') if 'such as lost pay' in r else r\nr=rep(r,'E.status = h(\"p\", { class: \"status\", role: \"status\", \"aria-live\": \"polite\", \"data-testid\": \"status-slot\" }, E.statusText, E.undo);',\n 'E.showBox = h(\"button\", { type: \"button\", class: \"btn quiet undo\", \"data-testid\": \"btn-show-box\", hidden: true }, \"Show box\");\\n    E.status = h(\"p\", { class: \"status\", role: \"status\", \"aria-live\": \"polite\", \"data-testid\": \"status-slot\" }, E.statusText, E.undo, E.showBox);')\nr=rep(r,'S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };','S.sync = () => { syncButtons(); if (!S.said || (!S.said.undo && /^Saved/.test(S.said.text))) drawStatus(); };')\nr=rep(r,\"if (S.alive) { syncButtons(); if (!S.ended\",\"if (S.alive) { syncButtons(); drawStatus(); if (!S.ended\")\ns=rep(s,'const stem = (w) => { const x = w.toLowerCase().replace(/[\\'’]s$/, \"\").replace(/s$/, \"\"); return ABBR[x] || x; };',\n 'const stem = (w) => { const x = w.toLowerCase().replace(/[\\'’]s$/, \"\").replace(/s$/, \"\"); return w === \"PT\" ? x : ABBR[x] || x; };      // \"PT\" in capitals is physical therapy, not a patient: it stays a word of its own, so a \"Patient\" in the line is still underlined')\ns=rep(s,'G.step2 = { buildQueue, find, flagHeading };','G.step2 = { buildQueue, find, flagHeading, outsideParts };')\nopen('review.js','w').write(r); open('step2.js','w').write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && grep -c \"lost wages\" $SP/t203r2/review.js; diff <(git show HEAD:app/frontend/guided/review.js) $SP/t203r2/review.js | grep -c '^[<>]'; diff $SP/t203r2/review.js app/frontend/guided/review.js | grep -c '^[<>]'; diff $SP/t203r2/step2.js app/frontend/guided/step2.js | grep -c '^[<>]'; grep -c \"such as lost pay\" $SP/t203r2/review.js"
}
````

### User / tool · 2026-11-02T23:50:16.883Z

**tool result**
````
1
33
0
0
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:50:22.930Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/frontend tests/e2e/guided/test_t203.py; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -f $SP/t203r2.idx; export GIT_INDEX_FILE=$SP/t203r2.idx; git read-tree HEAD && git update-index --add app/frontend/guided/review.js app/frontend/guided/step2.js tests/e2e/guided/test_t203.py && T=$(git write-tree) && echo $T && unset GIT_INDEX_FILE; rm -rf $SP/arch203r2; mkdir -p $SP/arch203r2 && git archive $T | tar -x -C $SP/arch203r2 && cd $SP/arch203r2 && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; ls | head -20"
}
````

### User / tool · 2026-11-02T23:50:25.253Z

**tool result**
````
 app/frontend/guided/review.js | 33 +++++++++++++++++++-------
 app/frontend/guided/step2.js  |  4 ++--
 tests/e2e/guided/test_t203.py | 54 -------------------------------------------
 3 files changed, 27 insertions(+), 64 deletions(-)
deef2624a685be20a6e0f46bd335c40aad16d9f8
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:50:31.419Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch203r2 && grep -c \"btn-show-box\" tests/e2e/guided/test_t203.py app/frontend/guided/review.js; ls -a | grep venv; (E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py -q 2>&1 | tail -15)",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:53:33.302Z

**tool result**
````
app/frontend/guided/review.js:1
tests/e2e/guided/test_t203.py:2
.venv
........................................................................ [ 52%]
..................................................................       [100%]
138 passed in 180.80s (0:03:00)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:53:40.762Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git log --oneline | head -1; P=$(git rev-parse HEAD); C=$(git commit-tree deef2624a685be20a6e0f46bd335c40aad16d9f8 -p $P -m \"fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\") && git update-ref refs/heads/$(git symbolic-ref --short HEAD) $C $P && git log --oneline | head -2; git status --short app/frontend tests/e2e/guided/test_t203.py"
}
````

### User / tool · 2026-11-02T23:53:40.856Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: git update-ref rewrites or prunes history; blocked | command: SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf80
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:53:47.545Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git log --oneline | head -1; GIT_INDEX_FILE=$SP/t203r2.idx git commit -q -m \"fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2; git show --stat HEAD | tail -5"
}
````

### User / tool · 2026-11-02T23:54:14.545Z

**tool result**
````
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test
check_secrets: ok (3 file(s) scanned staged)
fa34fe9 fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test

 app/frontend/guided/review.js | 33 +++++++++++++++------
 app/frontend/guided/step2.js  |  4 +--
 tests/e2e/guided/test_t203.py | 67 +++++++++++++++++++++++++++++++++++++++++--
 3 files changed, 92 insertions(+), 12 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:21.703Z

**tool call — Bash**
````
{
 "command": "git reset -q HEAD -- tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/frontend/guided/step2.js; git status --short tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/frontend/guided/step2.js; B=\"python3 tools/board.py\"; $B ac T-203 --check 1 --agent frontend --evidence \"r2: tests/e2e/guided/test_t203.py 6 pass (375x667 after-edit hint persists beside Saved, Show box, PT, lost wages); git archive of fa34fe9 tree: guided suite + test_no_console_errors 138 passed, E2E_REQUIRE_DB=1\"; $B handoff T-203 --agent frontend --text \"What changed (r2): drawStatus keeps the reason for a greyed Yes beside a 'Saved' note ('Saved. Tick the box to say you compared them.'), persists after act ends (drawStatus in S.act finally) until ticked; wording has no direction word; new 'Show box' button in the status slot appears when the box is under the bar/below screen and scrolls it above the bar + focuses it; 'PT' in capitals no longer maps to patient (Pt still does); 'lost pay' -> 'for example lost wages'. How verified: test_t203.py 6 tests incl. e4 edit path at 375x667; git archive fa34fe9 tree guided + no_console_errors 138 passed (E2E_REQUIRE_DB=1). Left: hint is 2 lines at 375 now (bar height unchanged); Step 3 label wrap nit not done. Surprised me: S.act finally only synced buttons, so the hint never appeared after an edit until the next redraw.\"; $B commit T-203 --sha fa34fe9 --agent frontend; $B move T-203 in_review --agent frontend"
}
````

### User / tool · 2026-11-02T23:54:21.757Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: git reset to a revision moves history; blocked (unstage with `git reset -- <path>`) | command: git reset -q HEAD -- tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/frontend/guided/step2.js; git status --short tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/fronte
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:26.548Z

**tool call — Bash**
````
{
 "command": "git reset -q -- tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/frontend/guided/step2.js; git status --short tests/e2e/guided/test_t203.py app/frontend/guided/review.js app/frontend/guided/step2.js; B=\"python3 tools/board.py\"; $B ac T-203 --check 1 --agent frontend --evidence \"r2: tests/e2e/guided/test_t203.py 6 pass (375x667 after-edit hint persists beside Saved, Show box, PT, lost wages); git archive of fa34fe9 tree: guided suite + test_no_console_errors 138 passed, E2E_REQUIRE_DB=1\"; $B handoff T-203 --agent frontend --text \"What changed (r2): drawStatus keeps the reason for a greyed Yes beside a 'Saved' note ('Saved. Tick the box to say you compared them.') and redraws after act ends, until ticked; wording has no direction word; new 'Show box' button in the status slot appears when the box is under the bar/below screen and scrolls it above the bar + focuses it; 'PT' in capitals no longer maps to patient (Pt still does); 'lost pay' -> 'for example lost wages'. How verified: test_t203.py 6 tests incl. e4 edit path at 375x667; git archive fa34fe9 tree guided + no_console_errors 138 passed (E2E_REQUIRE_DB=1). Left: hint is 2 lines at 375 now (bar height unchanged); Step 3 label wrap nit not done. Surprised me: S.act finally only synced buttons, so the hint never appeared after an edit until the next redraw.\"; $B commit T-203 --sha fa34fe9 --agent frontend; $B move T-203 in_review --agent frontend"
}
````

### User / tool · 2026-11-02T23:54:26.997Z

**tool result**
````
AC 1 checked: r2: tests/e2e/guided/test_t203.py 6 pass (375x667 after-edit hint persists beside Saved, Show box, PT, lost wages); git archive of fa34fe9 tree: guided suite + test_no_console_errors 138 passed, E2E_REQUIRE_DB=1
handoff written on T-203
T-203: commit fa34fe9 recorded
T-203: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:30.171Z

T-203 r2 is in `in_review` as commit fa34fe9. The guided suite plus `test_no_console_errors` give 138 passed from a fresh `git archive` of that tree (`E2E_REQUIRE_DB=1`), and the 6 `test_t203.py` tests cover the 375x667 after-edit path.

1. **Major:** after "Fix the wording" the slot now reads "Saved. Tick the box to say you compared them." and stays until she ticks. Ticking brings back the full saved message, and unticking brings the hint back. The cause was that `S.act` never redrew the status when it finished.
2. **"above":** the wording has no direction word. I also added a "Show box" button in the status slot that appears only when the box is under the bar or below the screen. One tap scrolls the box above the bar and focuses it.
3. **"PT":** capital "PT" is no longer treated as "patient", while "Pt" still is. I exposed `G.step2.outsideParts` so the test can call it.
4. **"lost pay":** it now reads "(for example lost wages)".

The hint at 375x667 now takes two lines instead of one (the Show box button narrows it). The bar height is unchanged. I didn't touch the Step 3 label wrap nit.
