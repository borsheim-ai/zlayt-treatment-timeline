# T-096 round 2 review: suggestions and confidence UI (ux-designer-reviewer)

**Verdict: pass.** The round-1 major (keyboard reach, 87 to 102 Tab presses) is fixed: Tab, Enter reaches the dates form and the dismissal suggestion at both widths. Of the 5 round-1 minors, 2 are fixed (Keep showing persisted, pointer near the top), 2 are fixed with a small residual (stale note, tray wording) and 1 is open (sentences_reason copy). No blocker, no major.

## Scope and how I ran it

- `git rev-parse --short HEAD` printed `e1ce8dc`; `git diff --stat 7d5a45f HEAD -- app/frontend` printed nothing. `git archive HEAD` into the scratchpad; server 127.0.0.1:7981 (fixture backend, ZLAYT_MODE=local, scratch DB), PID 49349, stopped with `kill 49349`, port returns 000.
- No stubs this time: the dismissal suggestion comes from the real route (`ux3-setup2.py` dismissed f_r7_2 in three sample cases through `POST .../items/f_r7_2/review`, then opened a fourth: `dismissal_suggestions` returned 'You dismissed this kind of flag 3 times. Hide similar ones in this case?'). The stale calibration is the real state at HEAD: `GET /api/calibration` returned `stale: True` with 'judge_conflict_v6.md is new' (the archive has no `.git`, but the route served a result).
- Playwright at 1440x900 and 390x844 touch (`ux3-walk7.py`, `ux3-walk10.py`): Tab sequences and Enter on lib09 (dates) and on the suggestion case; Keep showing then `reload()`; calibration line text and DOM order; the pointer button; the first-screen text scan.
- Not exercised: Hide similar's apply path (round 1 covered it; the frontend is unchanged there except the skip link), the overlap warning (unchanged), the no-sentences state beyond reading `app/frontend/manual.js:55` and `app/backend/present.py:188`: no corpus case reaches it (round 1 swept 24 files).

## Round-1 findings, one by one

| # | Round-1 finding | Status | Evidence |
|---|---|---|---|
| F1 (major) | 87 to 102 Tab presses to Confirm date and Hide similar | **Fixed** | lib09 at 1440 and 390: first Tab is 'Skip to dates to confirm' (`skip-dates`), Enter focuses the pre-selected date radio (`confirm-date`), one more Tab reaches Confirm. Suggestion case at both widths: first Tab is 'Skip to the dismissal suggestion', Enter focuses `btn-hide-similar` ('Hide similar (1)') (`ux3-walk7-results.json`, `ux3-90-1440-lib09-skip-dates.png`, `ux3-91-1440-sugg-skip.png`). Two key actions, as asked; Confirm date is a third (see N1) |
| F2 | Keep showing not remembered | **Fixed** | `after_keep` 0 then `after_keep_reload` 0 at 1440 and 390 (round 1: 1 after reload). suggestions.js:55 stores it in localStorage per case and key |
| F3 | Banner far below the fold | **Fixed** | First screen shows a button '1 dismissal suggestion waiting in Flags' in the Open decisions card (`todo-suggest`) at both widths; clicking it moves focus to `btn-hide-similar` (`ux3-walk10.py`). The banner itself is at y 2,084 (1440) and 4,243 (390) |
| F4 | Stale note repeats, shows a file name, sits after the number | **Fixed, residual nit (N2)** | `calibration-stale` is first in DOM order, before `calibration-verified`; visible text is one sentence 'These numbers come from an older version of the AI prompts.' (`ux3-92-1440-calibration.png`). Opening 'What changed' still prints 'judge_conflict_v6.md is new' and repeats 'older version' |
| F5 | Tray flag wording | **Fixed** | Tray lead: 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' then 'Nothing to accept here. Read what the AI suggested below; if it applies, open the record and check.' (`ux3-117-tray-lib06.png`). No 'code check' or 'phrase list' in the tray. The AI-check panel still uses 'phrase list' (see T-117 review) |
| F6 | sentences_reason copy repeats; no corpus case | **Open (minor)** | `app/frontend/manual.js:55` renders 'This record has no sentences to pick from.' + ' Why: ' + reason; the reason (`app/backend/present.py:188`) starts 'No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, ...'. 'no sentences' appears twice, 'could not be told apart' is a developer phrase, and no real case reaches the state |
| F7 (nit) | Precision line below the first screen | **Still true** | `calibration-line` at y 1,822 (1440) and 3,841 (390); was 2,098 and 3,665 |

## Findings

### F6 (minor): the no-sentences message still says the same thing twice and speaks in layout terms
Evidence: `app/frontend/manual.js:55`; `app/backend/present.py:188`. Composed message: 'This record has no sentences to pick from. Why: No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, so a quote cut from it could not be checked against the record. Read the record text instead.'
Why it matters: a paralegal reads the same fact twice and then a sentence about line layout; the one useful instruction, 'Read the record text instead', is last.
Fix: drop the frontend lead and the 'Why:' prefix and show one sentence: 'No sentence can be picked from this record because its Date and Source lines were not recognised. Read the record text instead.' Add a fixture case so the real path is exercised.
Acceptance test: a non-stubbed case with a record without Date and Source lines shows `manual-no-sentences` with one sentence and no repeated 'no sentences'.

### N1 (nit): the date skip link lands on the radio, so Confirm is the third key action
Tab, Enter focuses the pre-selected radio; Tab reaches 'Confirm date'; Enter confirms: four key presses against one click. Landing on the radio lets the reviewer see which reading is chosen, which I prefer to landing on Confirm; if the suggestion's reason is read first, the cost is fine. Optional: after Enter on the skip link, announce the chosen date and reason.

### N2 (nit): the stale reason prints a file name and repeats 'older version'
Opening 'What changed' shows 'The prompts have changed since these numbers were measured: judge_conflict_v6.md is new. The numbers describe an older version of the prompts.' The default view is clean; the disclosure is for the curious. Text is the backend's (`calibration_route.py`).

## What is right

- Tab, Enter reaches the dates form and the dismissal suggestion in two key actions at both widths, and the skip links only appear when the target exists.
- The dismissal banner never hides by itself and its first-screen pointer button takes focus straight to Hide similar.
- The stale warning now comes before the numbers, once, in plain words.

```json
{"card": "T-096", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "frontend at HEAD e1ce8dc (frontend identical to 7d5a45f); app at http://127.0.0.1:7981 (git archive HEAD, fixture backend, ZLAYT_MODE=local); lib09 (dates), a sample case with a real dismissal suggestion, lib06 tray; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (e1ce8dc); git diff --stat 7d5a45f HEAD -- app/frontend (empty); git archive HEAD into scratchpad; server PID 49349 stopped with kill, port returns 000",
  "ux3-setup2.py: three dismissals of f_r7_2 through the real review route, fourth case returns a real dismissal suggestion (no stub)",
  "ux3-walk7.py at 1440 and 390: Tab and Enter on lib09 and on the suggestion case, Keep showing then reload, calibration line text and DOM order, first-screen scan for the pointer",
  "ux3-walk10.py: stale 'What changed' text, pointer button click and focus",
  "GET /api/calibration at HEAD: status ok, stale true, reason 'judge_conflict_v6.md is new'",
  "read app/frontend/manual.js:55, app/backend/present.py:188, app/frontend/suggestions.js:55-59",
  "not exercised: Hide similar apply path, overlap warning, a real sentenceless record (none exists in the corpus)"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "F6. The no-sentences message states the same fact twice and uses layout terms",
   "evidence": "app/frontend/manual.js:55 ('This record has no sentences to pick from.' + ' Why: ' + reason); app/backend/present.py:188 (reason starts 'No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text')",
   "why_it_matters": "The reviewer reads 'no sentences' twice, then a developer phrase; the one instruction ('Read the record text instead') comes last. No real case reaches the state.",
   "fix": "One sentence without the 'Why:' prefix: 'No sentence can be picked from this record because its Date and Source lines were not recognised. Read the record text instead.' Add a fixture case for the real path.",
   "acceptance_test": "A non-stubbed case with a record without Date and Source lines shows manual-no-sentences with one sentence and no repeated 'no sentences'."},
  {"severity": "nit", "title": "N1. The date skip link lands on the radio, so Confirm date is the third key action",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-walk7-results.json: 1440_lib09_after_enter ['INPUT','confirm-date'], same at 390",
   "why_it_matters": "Four key presses against one click; landing on the chosen reading is defensible, so this is optional.",
   "fix": "Optionally announce the chosen date and its reason when the skip link lands.",
   "acceptance_test": "After Tab, Enter the live region names the selected date."},
  {"severity": "nit", "title": "N2. The stale reason prints a file name and repeats 'older version'",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-walk10.py output: 'The prompts have changed since these numbers were measured: judge_conflict_v6.md is new. The numbers describe an older version of the prompts.'",
   "why_it_matters": "Developer vocabulary behind a disclosure; the default view is clean.",
   "fix": "Backend wording: 'The detection prompt changed after these numbers were measured.'",
   "acceptance_test": "The 'What changed' text contains no '.md' and 'older version' at most once."}
 ],
 "whats_right": [
  "Tab, Enter reaches the dates form and the dismissal suggestion in two key actions at both widths",
  "A first-screen pointer button takes focus straight to Hide similar; the banner never hides by itself",
  "The stale warning is one sentence and comes before the numbers"
 ],
 "questions_for_chris": []}
```
