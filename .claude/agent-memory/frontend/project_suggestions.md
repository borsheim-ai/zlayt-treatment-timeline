---
name: suggestions-and-confidence
description: T-096 hooks (date suggestion form, dismissal banner, calibration line, overlap box, flag tray wording) and the pitfalls hit
metadata:
  type: project
---
app/frontend/suggestions.js = ZL.sg {usableSuggestion, dateForm, dismissalBox, calibration, overlapBox}; suggestions.css; api.js dismissalSuggestions/applyDismissal/calibration.
- dateForm is shared by timeline.js (only when suggestion.iso is usable; otherwise the old one-click `confirm-date` buttons + a hint) and flags.js dateControl. Radios carry testid confirm-date + data-date; Confirm is btn-confirm-date. Existing specs click it via `_confirm()` in test_input.py.
- dismissal banner lives at the top of the flags panel; module cache keyed by token; flags re-render on every state.set so errors are kept in `errs` (a repaint after a failed apply detached the first version of the error line).
- calibration line is mounted in timeline.js under the toolbar; fetched once, a failed fetch retries on the next paint.
**Pitfall:** native `Element.append(null)` writes the text "null" (screenshot showed it); only ZL.el filters null. Use `.append(...[..].filter(Boolean))` outside el().
**Pitfall:** `reasons` of a flag tray item is `['JUDGE_DISAGREES','LLM_ONLY']` on real data; use reasons[0] for the wording.
**Test recipe:** real backend gives state for case_01 (date suggestion), lib06 (flag tray), lib09 (overlap), lib01 (entry tray); dismissal counts depend on the machine's history, so stub GET/POST dismissal_suggestions (the POST stub really dismisses through the review route).
**Clean worktree:** `git worktree add <scratch>/wt96 HEAD`, rsync app/frontend into it, start with ZLAYT_DB in scratch, kill by PID, `git worktree remove --force`.
