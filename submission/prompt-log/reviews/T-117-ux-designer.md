# T-117 review: AI-check panel row for a could-not-verify tray flag (ux-designer-reviewer)

**Verdict: pass.** The row is titled with the flag's name and a record cue, like every other row; no raw id appears in the panel on any of the five library cases at 1440 or 390. One minor (copy contradicts the tray) and no blocker or major.

## Scope and how I ran it

- `git rev-parse --short HEAD` printed `e1ce8dc`; `git diff --stat 7d5a45f HEAD -- app/frontend` printed nothing; the card's commit is c8e36fb, an ancestor of HEAD. `git archive HEAD` into the scratchpad, server on 127.0.0.1:7981 (fixture backend, ZLAYT_MODE=local, scratch DB), PID 49349, stopped with `kill 49349`, port returns 000.
- Playwright at 1440x900 and 390x844 on lib01, lib06, lib09, lib11, lib14: opened the AI-check panel and scanned its text for `f_...` ids (`ux3-walk5.py`); on lib06 (the card's case) read the tray, opened the panel, pressed 'Go to item' on the 'Degenerative wording' row and read where focus landed (`ux3-walk6.py`).
- Not exercised: the e2e test itself (T-115/qa's), other tray item kinds beyond the lib06 flag.

## Card checks

1. **Tray flag row titled with a name and a record cue: PASS.** lib06 row reads 'Degenerative wording · Record 5' with a 'Flag' chip (`ux3-117-judge-panel-lib06.png`, `ux3-walk5-results.json`). The tray item it belongs to is 'Record 5: Larchmont Ridge Imaging, right shoulder MRI · Flag not confirmed' with 'Degenerative wording — "Mild supraspinatus tendinosis; no full-thickness tear."' (`ux3-117-tray-lib06.png`), so the title and the tray agree.
2. **No raw id anywhere in the panel: PASS.** `raw_ids` is empty for all ten runs (five cases, two widths); rows for entries read 'date · provider · Record n', amounts '$450 (unclear) · Record 4'.
3. **Row navigates to the item: PASS.** 'Go to item' on the tray flag row moves focus to `[data-testid=tray-item]` inside the tray (`after_go_active`: ARTICLE tray-item, 'in tray'), page scrolled to y 2,817.

## Findings

### F1 (minor): the panel row tells the reviewer to accept an item the tray says cannot be accepted
Evidence: `ux3-117-judge-panel-lib06.png` shows 'Your decision: Not reviewed' and 'What you need to do: Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.' for 'Degenerative wording · Record 5'. `ux3-117-tray-lib06.png` for the same item says 'Nothing to accept here ... it is left out of the letter.' The row also keeps 'See the steps', 'Technical details', 'Code said' and 'The phrase list did not find it', internal wording that the pass-2 text scan did not catch because the panel was closed.
Why it matters: two surfaces give opposite instructions for the same item; a paralegal who follows the panel looks for an Accept button that is not there.
Fix: for tray items show 'Left out of the letter' in place of the decision line and the action sentence; one label ('Why this status') for the steps.
Acceptance test: the judge row for a `[data-tray-kind=flag]` item has no 'accept' and no 'Your decision' text.

## What is right

- The title comes from the AI's own summary ('Degenerative wording'), so the row names what was attempted, not an id.
- The record cue ('· Record 5') is on every row type, which makes the panel scannable against the record list.
- 'Go to item' lands inside the tray, not at the top of the page.

```json
{"card": "T-117", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "frontend at HEAD e1ce8dc (card commit c8e36fb; frontend identical to 7d5a45f); app at http://127.0.0.1:7981 (git archive HEAD, fixture backend, ZLAYT_MODE=local); lib01, lib06, lib09, lib11, lib14; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (e1ce8dc); git diff --stat 7d5a45f HEAD -- app/frontend (empty); git archive HEAD into scratchpad; server PID 49349 stopped with kill, port returns 000",
  "ux3-walk5.py: AI-check panel opened and scanned for raw f_ ids on five library cases at 1440 and 390 (raw_ids empty in all ten)",
  "ux3-walk6.py: lib06 tray read, panel row for 'Degenerative wording' opened, 'Go to item' pressed, focus landed in tray-item",
  "screenshots ux3-117-judge-panel-lib06.png, ux3-117-judge-panel-lib06-390.png, ux3-117-tray-lib06.png, ux3-117-after-go-to-item.png",
  "not exercised: the e2e test, tray item kinds other than the lib06 flag"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "AI-check panel row for a could-not-verify flag says to accept or dismiss it; the tray says nothing can be accepted",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-117-judge-panel-lib06.png ('Your decision: Not reviewed'; 'Edit it, accept it if you agree with it, or dismiss it') vs artifacts/review-evidence/T-060-pass3/ux3-117-tray-lib06.png ('Nothing to accept here')",
   "why_it_matters": "Opposite instructions for the same item on two surfaces; internal terms ('Code said', 'phrase list', 'See the steps', 'Technical details') remain in the opened panel.",
   "fix": "For tray items show 'Left out of the letter' instead of the decision line and action sentence; use 'Why this status' as the one label for the steps.",
   "acceptance_test": "The judge row for a [data-tray-kind=flag] item contains no 'accept' and no 'Your decision'."}
 ],
 "whats_right": [
  "The row title is the AI's own summary plus 'Record 5', and it matches the tray item it belongs to",
  "No raw id in the panel on any of five cases at two widths",
  "'Go to item' moves focus into the tray item"
 ],
 "questions_for_chris": []}
```
