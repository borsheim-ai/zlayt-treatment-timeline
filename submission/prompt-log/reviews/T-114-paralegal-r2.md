# T-114 r2 review: paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 1 major, 1 minor, 2 nits). The gap-change notice now appears when a date is confirmed and names both numbers, but it is held only in page memory. After Got it or a reload the gap card reads "Gap of 40 days" with no reason, so the round-1 major is still open. The round-1 minor is partly fixed: the "Accept as noted" button is gone, but an accepted rate row still shows a "Needs review" chip. The round-1 nit (lib01 fixture miss) is still there.

The scope is HEAD, not b5fb35c. HEAD is e1ce8dc, which includes the T-060 r3 frontend commits (c8e36fb, 5d975ed), so the round-1 "no UI consumer" finding had to be re-tested on the committed code.

## Round-1 items

| Round-1 item | Status at e1ce8dc | Evidence |
|---|---|---|
| Major: gap change must show in the UI | Partly. Banner at confirm: yes. Gap card and after reload: no. | artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json |
| Minor: accepted rate row reads unfinished | Partly. "Accept as noted" gone; "Needs review" chip still on the row. | artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png |
| Nit: lib01 extract misses its fixture | Still open. One FIXTURE_MISS row for case lib01. | sqlite3 query output in the exercised list |

## What I ran

Deterministic first.

- `git rev-parse HEAD` printed `e1ce8dc620e6ec0778320456ac79a25f1832bfee`. `git merge-base --is-ancestor c8e36fb HEAD` and the same for `5d975ed` both succeeded.
- `git archive HEAD` extracted to the session scratchpad `t114r2/archive`. `grep -rln gap_changes app/frontend app/backend` returned `app/frontend/timeline.js` and `app/backend/review.py`.
- Server from the archive: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local HOST=127.0.0.1 PORT=7881`, ZLAYT_DB in the scratchpad, PID 51899. `GET /` returned 200. Stopped by PID at the end. The team app on 7860 was not touched.

Live checks. Scripts are in `artifacts/review-evidence/`, run with `.venv/bin/python` (`-I` for the JSON check).

- `T-114-r2-paralegal-probe.py`: lib09 has one date to confirm (record 4, "03/05/2026"), candidates 2026-03-05 and 2026-05-03, suggested 2026-05-03. The gap is 42 days, record 1 to record 2.
- `T-114-r2-paralegal-sweep.py` (out: `T-114-r2-paralegal-sweep.out.json`): all 15 library packets, fresh cases. Two confirm attempts in total, both lib09 record 4. Confirming 2026-03-05 returns `gap_changes` 42 to 40 (new start 2026-03-05). Confirming 2026-05-03 returns none.
- `T-114-r2-paralegal-ui-gap.py` (Playwright, Chromium, 1440x900; out: `T-114-r2-paralegal-ui-gap.out.json`): confirmed record 4 as 2026-03-05 in the Dates to confirm form, read the banner text and position, scrolled to top, clicked Got it, reloaded, then accepted rate a3 on a second load.
- `T-114-r2-paralegal-checks2.py` (out: `T-114-r2-paralegal-checks2.out.json`): full gap-card text after confirm and after reload, rate a3 chips and the Kept in notes control, FIXTURE_MISS rows.
- `sqlite3` on the scratch DB: `SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name;` printed `case lib01 er only then gap|1`. The same query without the join printed `1`.
- `T-114-r2-paralegal-jsoncheck.py` on the draft JSON: `findings {'blocker': 0, 'major': 1, 'minor': 1, 'nit': 2} verdict changes`, `errors none`, `paperwork sentence count in reloaded gap card: 2`, `'was 42' or 'recalculated' in reloaded gap card: False`.

Code read at HEAD: `app/frontend/timeline.js:73, 77, 95, 97`; `app/frontend/review.js:233`; `app/frontend/charges.js:77`; `app/backend/review.py:353-364, 400`.

Not exercised: I did not click "Kept in notes" or Undo on the rate row. I did not walk the 30 exports or the 7 refusals again (round 1 covered them, and this round's scope is the notice and the minors). The working tree has uncommitted changes (for example `app/backend/api.py` and `app/backend/pipeline.py` in `git status --short`), so this review covers the HEAD archive only.

## Findings

### Major: the gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed

Evidence: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.after_confirm.note_text is "A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it". steps.after_dismiss.note_count is 0. steps.after_reload.note_count is 0, body_has_recalc is false and body_has_was_42 is false. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload begins "Gap of 40 days Needs review Gap of 40 days between March 5, 2026", and the check reports no "was 42" or "recalculated" on the card. The only 42 on the card is in the paperwork sentence: "the gap would be 42 days (March 3, 2026 to April 14, 2026)". Source: `app/frontend/timeline.js:73` (`let gapNote = null`) and `timeline.js:97` (Got it clears it). Screenshots: `artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png` and `artifacts/review-evidence/T-114-r2-ui-4-after-reload.png`.

Why it matters: round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray. Its acceptance test was that the gap flag card shows "Gap recalculated after you confirmed record 4: now 40 days (was 42)." At e1ce8dc the notice is clear at the moment of confirm, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The adjuster counts days between encounters and asks why a number changed. The round-1 acceptance test is not met.

Fix: show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory. One line under the title, for example "Changed after you confirmed record 4: now 40 days (was 42)." It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.

Acceptance test: lib09, confirm record 4 as 2026-03-05, then reload. The element `flag-f_gap_r4_r2` contains "now 40 days (was 42)" and "March 5, 2026". Repeat after clicking Got it on the banner.

### Minor: an accepted rate row still shows a "Needs review" chip beside "Accepted"

Evidence: `artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png`. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` rate_a3_chips is ["Needs review", "Accepted"], and rate_a3_needs_review_text_count is 1. Fixed part: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.rate_a3_after.has_accept_as_noted is 0. The control is now "Kept in notes" (`app/frontend/review.js:233`) with Undo, and the text reads "Kept in the internal notes only; not in the letter or the total." (`app/frontend/charges.js:77`).

Why it matters: the Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.

Fix: after acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false). I did not click it; if it does nothing, it should not look like a button.

Acceptance test: lib09, accept rate a3. The row contains no "Needs review" text (count 0), and its status reads Accepted or Noted only.

### Nit: the lib01 extract step still misses its demo fixture on every run

Evidence: the sqlite3 query in the exercised list printed `case lib01 er only then gap|1`. The row is step extract, attempt 1, parsed_ok 0, error "FIXTURE_MISS 83bcee077841...". Round 1 saw four such rows across its lib01 runs.

Why it matters: nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.

Fix: record the lib01 extract response under `tests/fixtures/llm/` (curated set), or note the fallback on the card.

Acceptance test: a fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls.

### Nit: the paperwork sentence appears twice in the lib09 gap card

Evidence: `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload. "which looks like paperwork, not a visit" occurs twice (the jsoncheck count is 2). Each occurrence is followed by "If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)", with the "Needs review: AI translation" text between them.

Why it matters: the gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It sits on the card this card touches, so I flag it here.

Fix: render the paperwork note once in the gap card.

Acceptance test: lib09 gap card after confirming record 4: the text "looks like paperwork" occurs once.

## Right already

- The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers ("now 40 days (was 42)"), and is announced in the status region.
- The accepted rate row has no Accept as noted button and says "Kept in the internal notes only; not in the letter or the total."
- The backend figure holds at e1ce8dc: confirming 2026-03-05 on lib09 returns gap_changes 42 to 40 with new start 2026-03-05. The suggested 2026-05-03 reading changes no gap (`artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json`).

## Questions for Chris

Still open from round 1: the lib09 gap card now says record 4 "looks like paperwork, not a visit", and the 40-day figure still starts there. T-060 F4 says an intake form is never an endpoint. Should an intake form ever be a gap endpoint? The number the adjuster sees depends on the answer. Whether the gap goes in the demand is litigation-lead's call.

```json
{"card": "T-114", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD = e1ce8dc620e6ec0778320456ac79a25f1832bfee (T-060 r3 commits c8e36fb and 5d975ed are ancestors), extracted to the session scratchpad t114r2/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, PID 51899, stopped at the end); sample case: library case_lib09_spanish_interpreter_espalda, plus the 15 library packets for the confirm-date sweep",
 "exercised": [
  "git rev-parse HEAD printed e1ce8dc620e6ec0778320456ac79a25f1832bfee; git merge-base --is-ancestor c8e36fb HEAD and 5d975ed HEAD both printed as ancestors",
  "git archive HEAD into the scratchpad; grep gap_changes in the archive: app/frontend/timeline.js and app/backend/review.py",
  "server from the archive on 127.0.0.1:7881 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB in scratchpad); GET / returned 200",
  "artifacts/review-evidence/T-114-r2-paralegal-probe.py: lib09 dates_to_confirm r4 candidates 2026-03-05 and 2026-05-03 (suggested 2026-05-03); gap flag 42 days r1 to r2",
  "artifacts/review-evidence/T-114-r2-paralegal-sweep.py: all 15 library packets; 2 confirm attempts (both lib09 r4); 2026-03-05 returns gap_changes 42 to 40, 2026-05-03 returns none",
  "artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py (Playwright, Chromium, 1440x900): confirm r4 as 2026-03-05 in the Dates to confirm form; read the gap-change notice text and its viewport position; scroll to top; Got it; reload; accept rate a3 on a second load",
  "artifacts/review-evidence/T-114-r2-paralegal-checks2.py: full gap card text after confirm and after reload; rate a3 chips and Kept in notes control; FIXTURE_MISS rows in the scratch DB",
  "sqlite3 on the scratch DB: SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'",
  "read app/frontend/timeline.js:73, 77, 95, 97 (gapNote in memory; Got it clears it); app/frontend/review.js:233; app/frontend/charges.js:77; app/backend/review.py:353-364 and 400"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "gap_change_notice_at_confirm": 4, "gap_change_on_card_after_reload": 2, "rate_row_clarity": 3},
 "findings": [
  {"severity": "major", "title": "The gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed",
   "evidence": "artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.after_confirm.note_text = 'A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it'; steps.after_dismiss.note_count 0; steps.after_reload.note_count 0 with body_has_recalc false and body_has_was_42 false. artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload begins 'Gap of 40 days Needs review Gap of 40 days between March 5, 2026' and card_has_was_or_recalc_after_reload is false; the only 42 on the card is 'the gap would be 42 days (March 3, 2026 to April 14, 2026)' in the paperwork sentence. app/frontend/timeline.js:73 (let gapNote = null), timeline.js:97 (Got it sets gapNote = null and removes the node). Screenshots: artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png, artifacts/review-evidence/T-114-r2-ui-4-after-reload.png.",
   "why_it_matters": "Round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray (acceptance test: the gap flag card shows 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'). At e1ce8dc the notice appears at the moment of confirm and is clear, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The card's only 42 means something else (what the gap would be if record 4 is paperwork). The adjuster counts days between encounters and asks why a number changed; the paralegal needs the answer after the banner is gone. The round-1 acceptance test is not met.",
   "fix": "Show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory: one line under the title such as 'Changed after you confirmed record 4: now 40 days (was 42).' It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.",
   "acceptance_test": "lib09: confirm record 4 as 2026-03-05, then reload the page. The element flag-f_gap_r4_r2 contains 'now 40 days (was 42)' and 'March 5, 2026'. Repeat after clicking Got it on the banner."},
  {"severity": "minor", "title": "An accepted rate row still shows a Needs review chip beside Accepted",
   "evidence": "artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json rate_a3_chips ['Needs review', 'Accepted'] and rate_a3_needs_review_text_count 1. Fixed part: artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.rate_a3_after.has_accept_as_noted 0; the control is now 'Kept in notes' (app/frontend/review.js:233) with Undo, and the text 'Kept in the internal notes only; not in the letter or the total.' (app/frontend/charges.js:77).",
   "why_it_matters": "The Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.",
   "fix": "After acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false); I did not click it. If it does nothing, it should not look like a button.",
   "acceptance_test": "lib09, accept rate a3: the row contains no 'Needs review' text (count 0) and its status reads Accepted or Noted only."},
  {"severity": "nit", "title": "The lib01 extract step still misses its demo fixture on every run",
   "evidence": "sqlite3 on the scratch DB, SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'. Row: step extract, attempt 1, parsed_ok 0, error 'FIXTURE_MISS 83bcee077841...'. Round 1 saw four such rows across its lib01 runs.",
   "why_it_matters": "Nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.",
   "fix": "Record the lib01 extract response under tests/fixtures/llm/ (curated set), or note the fallback on the card.",
   "acceptance_test": "A fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls."},
  {"severity": "nit", "title": "The paperwork sentence appears twice in the lib09 gap card",
   "evidence": "artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload: 'which looks like paperwork, not a visit' occurs twice; each occurrence is followed by the 'If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)' sentence, with the 'Needs review: AI translation' text between them.",
   "why_it_matters": "The gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It is on the card this card touches, so I flag it here.",
   "fix": "Render the paperwork note once in the gap card.",
   "acceptance_test": "lib09 gap card after confirm of record 4: the text 'looks like paperwork' occurs once."}
 ],
 "whats_right": [
  "The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers ('now 40 days (was 42)'), and is announced in the status region.",
  "The accepted rate row has no Accept as noted button and says 'Kept in the internal notes only; not in the letter or the total.'",
  "The backend figure holds at e1ce8dc: confirming 2026-03-05 on lib09 returns gap_changes 42 to 40 with new start 2026-03-05; the suggested 2026-05-03 reading changes no gap (artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json)."
 ],
 "questions_for_chris": [
  "Still open from round 1: the lib09 gap card now says record 4 'looks like paperwork, not a visit', and the 40-day figure still starts there. T-060 F4 says an intake form is never an endpoint. Should an intake form ever be a gap endpoint? The number the adjuster sees depends on the answer. Whether the gap goes in the demand is litigation-lead's call."
 ]}
```
