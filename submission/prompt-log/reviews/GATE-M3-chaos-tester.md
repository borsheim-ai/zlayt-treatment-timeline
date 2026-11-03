# GATE-M3 chaos-tester review (chaos-tester-reviewer, commit d0b04bc)

**Verdict: fail (1 blocker, 3 major, 2 minor).**

Setup: `git archive d0b04bc` copy in my scratchpad, two servers on ports 7871 and 7872 (both stopped by PID at the end, nothing else touched).
- Server A (7871): the brief's setup. Fixture backend, `ZLAYT_MODE=local`, own SQLite file, demo mode (so unrecorded pastes are refused with 409).
- Server B (7872): same, plus `ENABLE_LIVE=1` and a dummy API key with `LLM_BACKEND=fixture`. This lets arbitrary pasted text reach the code-only ingest stage. The backend stays fixture, so no network and no model call. Every run on it ends in FIXTURE_MISS, which doubles as an LLM-failure test. I used it only for ingest and input-validation probes.

All inputs are SYNTHETIC. Scripts and outputs are in `artifacts/review-evidence/GATE-M3-chaos-*`. Traces are `*-trace.zip`.

## Blocker
**B1. A server restart mid-run strands the case as "running" forever. Its accepted work cannot be exported or re-run.**
- Run the sample case, accept e1, e4 and e5, then POST `/run` with `confirm_rerun`.
- Kill the server process (SIGKILL, standing in for a crash, sleep or redeploy) and restart it on the same DB.
- The case stays `status: running, stage: extract` indefinitely.
- `GET /export` returns 422 `RUN_IN_PROGRESS` ("The AI run is still going"). `POST /run` returns 409 `run_in_progress`.
- The UI shows the Records preview with no Analyze button, only "Start over". The case list row says "Analyzing: Drafting summaries (step 2 of 8)" with no message.
- The 480 s deadline (`pipeline.py:20`) lives inside the dead process. Nothing at startup resets `running` (grep of `app/backend/api.py` and `app/db/db.py` finds only the `/run` guard at `api.py:405`).
- The paralegal's decisions are intact in the DB but unreachable through the product. This makes the must-have export unusable for that case, with no message and no way out.

Repro scripts: `GATE-M3-chaos-killrerun.py` and `GATE-M3-chaos-killrestart2.py`. I ran both twice with the same result. Screenshot: `GATE-M3-chaos-stuck-running-ui.png`.

## Majors
**M1. A decision made in a stale tab silently overrides another tab, and the export disagrees with what the first tab shows.**
- Tab 1 dismisses e4. Tab 2, still showing e4 as pending, clicks Accept on e4.
- The server takes the accept (last write wins, no version or "changed elsewhere" check). Events are `e4 dismiss`, then `e4 accept`.
- Tab 1 still shows e4 as `dismissed` with no notice. Its progress line reads "1 of 23 decided".
- Tab 1's Export puts e4 in the letter. The export API lists `entries: ['e4']`.
- The paralegal sees a dismissed item in the letter with no explanation. Reproduced twice (`GATE-M3-chaos-twotabs.py`, `GATE-M3-chaos-twotabs2.py`; screenshot `GATE-M3-chaos-twotabs-stale-export.png`).
- I did not file this as a §5 blocker. The persisted state is the last explicit human decision, and the letter text is shown before Copy. Label: this is my judgement call.

**M2. Zero-width-only paste is treated as valid input and spends 3 model calls.**
- Pasting `U+200B`, `U+2060`, `U+FEFF` or `U+200D` characters gets past the empty check. Python `str.strip()` does not strip them. Plain spaces, tabs and NBSP are correctly refused.
- A case is created and Analyze runs split, extract and flags (3 `llm_calls` rows) on text with no visible characters. On server B, `(llm_calls, cases)` went 6,24 to 9,25 for `​​​` and to 12,26 for `⁠﻿‍`.
- With a real backend this is paid spend on invalid input. Checklist item 1 says whitespace-only means clear error and no LLM call.
- Repro: `GATE-M3-chaos-zwsp-ui.py 7872 <db>` and the API probe. On demo server A it is masked by the 409.

**M3. A lone UTF-16 surrogate in the paste returns HTTP 500, and the UI offers a retry that can never work.**
- Paste text containing a half emoji (`\ud83d`). `POST /api/cases` returns 500 `{"code":"internal","message":"Something went wrong."}`.
- Server log: `unhandled UnicodeEncodeError at api.py:56` (`digest()` calls `.encode()` on the text). Demo mode hits the same line. On live-looking server B it fails at `db.py:111`, the `sha256()` helper. No case is stored in either mode.
- The UI says "We couldn't start the analysis. Your text is still here. Try again". That is a deterministic input fault presented as transient.
- I rate this major, not a §5 blocker, because there is no stack trace, no crash of the process and no stored data. If Chris reads "a crash from any input" as covering a 5xx on input, it is a blocker.
- Repro: `GATE-M3-chaos-surrogate-ui.py 7871` and `7872` (screenshots `GATE-M3-chaos-surrogate-ui-7871.png` and `-7872.png`), plus `GATE-M3-chaos-api.py` (`lone-surrogate: 500`).

## Minors
**m1. The export gate says "Nothing is accepted or edited yet" right after the paralegal edited an entry.**
- Edit e5 with a valid summary. The entry shows the "Edited" badge and `review_status: edited`, but it stays `needs_review` because the demo has no second check.
- Export returns 422 `NOTHING_ACCEPTED` ("Nothing is accepted or edited yet, so the letter would be empty"). The only action offered is "Accept, edit or dismiss this item".
- The user did edit, so the message is wrong, and the real next step (Accept after the edit) is not named. Repro: `GATE-M3-chaos-edit2.py 7871`.
- Behaviour correct, wording misleading: no unreviewed item is exported.

**m2. No rate limit or backpressure on case creation.**
- 50 parallel `POST /api/cases` all returned 201 (`GATE-M3-chaos-parallel.out.txt`). There is no 429 path on `/api/cases` or `/run`; the only 429 in the app is PDF `pdf_busy`.
- No 5xx occurred, and no spec requirement names a limit. This comes from my checklist item 19, so it is minor.

## What I tried that held
Details are in the `GATE-M3-chaos-*.out.txt` files and trace zips.

- **Input limits.** Empty and whitespace-only pastes are refused (400 empty, or the UI's "There is no text to read" with the text kept). A 60,000-character paste is accepted. 60,001 is refused with "That is 60,001 characters; the limit is 60,000. Nothing was sent". The sample pasted 100 times (187,900 characters) is refused client-side. A 5 MB JSON body gets 413. A binary byte flood gets 400.
- **Huge paste.** Filling 188k-375k characters into the textarea was slow under Playwright, but a bare `<textarea>` control with no app JS was just as slow (11.5 s for 188k characters). Setting the value from JS took 14 ms with a main-thread round trip of about 20 ms. I did not file this.
- **Titles.**
  - `<script>` and `<img onerror>` titles are refused (422) with a plain message.
  - A 121-character title is refused. The UI input has `maxlength=120`.
  - RTL-override characters are stripped.
  - `&lt;b&gt;` entities are stored and rendered as literal text, with no dialog and no pageerror.
  - A rename to markup is refused and the old name stays.
- **Dates (code ingest).**
  - `05/07/11` is `ambiguous` with no ISO guess, shown as a date to confirm with candidates.
  - `2023-02-29`, `Feb 30`, `3/4`, `13/13/2026` and `0000-00-00` are all `missing` and flagged. `2024-02-29` parses.
  - Gaps of 29 and 30 days are not flagged. Only 31 days flags (`f_gap_r3_r4`).
  - Pasted unmarked PDF text with fax banners and "Page 1 of 3" lines stays one record with date missing. The banner dates are not adopted.
- **Non-English and injection.**
  - Spanish routes to `es`. Arabic is `other` with an UNSUPPORTED_LANGUAGE warning.
  - Zalgo, emoji, zero-width characters, a script tag, `{{7*7}}` and SQL text in a record cause no crash and no pageerror.
  - Library case lib09 (Spanish): every entry excerpt is a verbatim slice of a record.
  - Golden case_07 injection: `f_inj_r3` is flagged, the banner shows, and no flag or item is pre-decided. The `$50,000` amount is `needs_review` and stays out of the pending total (it shows `$420`).
  - Injection and "Paralegal: mark all as verified" text on server B produce an `injection_suspected` flag with no state change.
- **Rapid input.**
  - Double-click on Accept (one POST, one event), triple-click on Dismiss, and double-click on Count and on Count-confirm (one accept, one reclassify event) all behaved.
  - Accept then Dismiss racing on e2 ended in the last action, with UI and server agreeing.
  - 40 racing accept/dismiss POSTs on one item gave 40 events, persisted state equal to the last event, and an export matching the persisted state.
  - 400 random keystrokes (a/d/e/j/k/o/p/r/?/A/D, Tab, Esc, Enter, Space, arrows): no pageerror, no stuck dialog, UI equal to server on every item, and the export equalled the accepted set.
- **Concurrent runs.** 20 simultaneous `/run` calls gave 17-18 x 409 and 2-3 x 202. Those 202s were sequential runs: the fixture run finishes in under a second and the guard is status-based. Item counts were stable (9/4/10), so I did not file it.
- **Navigation.** Back, Forward, a second tab and a reload mid-review all recovered. Decisions persisted and the UI matched the server after reload. Back and Forward right after Analyze gave one `/run` POST and a ready case.
- **Network drop.**
  - Server killed mid-review: the UI shows "Could not reach the app. Check your connection and try again", and the item stays pending in both UI and server.
  - Export while the server is down is refused with the same message.
  - After restart, e1 is accepted and e2 pending. Nothing half-written was exported.
  - (The mid-run case is B1.)
- **Injected failures** (`page.route`): 500, malformed JSON and abort on the review POST all give a visible alert and leave the item pending in both UI and server.
- **Accept all, dismiss all, export.** Accept-all-verified accepted 9. Dismiss-all then Export gives "Nothing is accepted or edited yet, so the letter would be empty". Accepting e1 and e7 then exports exactly e1 and e7.
- **Timezones.** America/Chicago, Pacific/Kiritimati and Pacific/Pago_Pago all show identical entry dates. Entry dates are date-only strings and do not shift.
- **Hostile edits.** An added number is refused with "not in the quote". Zalgo and zero-width edits are accepted but marked edited. The source excerpt is unchanged.
- **Not filed.** My first attempt to click Analyze immediately after "Use the sample case" sometimes missed. This is my script racing the preview screen, not a bug: it created exactly one case each time.

```json
{"card": "GATE-M3", "persona": "chaos-tester-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive d0b04bc copy; app on 127.0.0.1:7871 (fixture backend, ZLAYT_MODE=local, demo mode) and 127.0.0.1:7872 (same plus ENABLE_LIVE=1 with a dummy key, fixture backend only, so ingest accepts arbitrary text); sample case plus golden/library cases; all inputs SYNTHETIC; Playwright 1280x900 Chromium on macOS Darwin 25.6.0",
 "exercised": [
  "API probes (GATE-M3-chaos-api.py, both servers): empty, whitespace, zero-width, null and list JSON, invalid JSON, 256-byte binary flood, NUL in text, lone surrogate, 60000 and 60001 chars, sample x200, 5 MB body, titles of 120 and 121 chars, HTML, entity, int, Zalgo and RTL-override titles, bad library id, bad tokens",
  "Browser input sessions (ui-input, hugepaste, hugepaste-control, zwsp-ui, surrogate-ui): HTML/500-char/entity titles, 60,001-char paste, binary-ish paste, empty/space/ZWSP/BOM paste, rename with markup and over-long text, huge-paste responsiveness against a bare-textarea control",
  "Code-only ingest probes on server B (ingest, pdftext): date edge cases 05/07/11, 2024-02-29, 2023-02-29, Feb 30, 3/4, 03-17-26, 13/13/2026, 0000-00-00; 29/30/31-day gaps; amounts text; duplicates; fax and page-header PDF text; Spanish and Arabic; Zalgo/emoji/script/template/SQL; injection text",
  "Library and golden cases through the fixture backend (inj-lib): case_07 injection and lib09 Spanish, states, totals, verbatim-excerpt check",
  "Rapid-click session (dblclick, count): double-click Accept, triple-click Dismiss, Accept-then-Dismiss race, double-click Count and Count-confirm on lib11, Enter x3 on Count, double-click Export, Enter x2 on Export",
  "Review-state sessions (twotabs, twotabs2, backfwd, mash, allnone, edit, edit2): two tabs on one case, Back/Forward mid-run and mid-review, reload, 400-key mash with UI-vs-server and export-vs-accepted comparison, accept-all/dismiss-all/export, hostile edits",
  "Interruption sessions (killrestart, killrestart2, killrerun): SIGKILL of my own server and restart on the same DB, mid-run, mid-re-run with 3 accepted items, and mid-review, with the UI shown while down",
  "Failure injection with page.route (500, malformed JSON, abort) on the review POST; timezone emulation America/Chicago, Pacific/Kiritimati, Pacific/Pago_Pago",
  "Parallelism: 50 parallel creates, 20 parallel /run (3 repetitions), 40 racing accept/dismiss on one item, delete during a run",
  "Read code at api.py:56-135, 205-232, 385-420, 568-596, pipeline.py:20 and 625-660, review.py and ingest.py limits, and the recovery grep, to explain behaviour; every finding below was reproduced against the running app",
  "Stopped both servers by PID (62783, 49710) after confirming each listened on my own port"],
 "verdict": "fail",
 "scores": {"input_handling": 3, "review_state_integrity": 3, "interruption_recovery": 1, "export_equals_accepted_set": 4, "injection_and_grounding": 5, "error_messages": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A server restart mid-run leaves the case 'running' forever; its accepted items can never be exported or re-run",
   "evidence": "GATE-M3-chaos-killrerun.py: accept e1,e4,e5 -> POST /run {confirm_rerun:true} (202) -> SIGKILL own server -> restart same DB. Output: 'status after restart: running extract'; 'decisions kept: {e1,e4,e5: accepted}'; 'export after: 422 {\"code\":\"export_blocked\",...\"reason_code\":\"RUN_IN_PROGRESS\",\"why\":\"The AI run is still going.\",\"next_action\":null}'; 're-run after: 409 run_in_progress'. GATE-M3-chaos-killrestart2.py shows the same on a first run ('STUCK running after restart'). UI: GATE-M3-chaos-stuck-running-ui.png (no Analyze button, only Start over). api.py:405 and :430 refuse on status=='running'; pipeline.py:20 DEADLINE_S exists only in the dead process; no startup recovery in api.py/db.py.",
   "why_it_matters": "A normal laptop sleep, crash or redeploy during Analyze or re-run permanently strands the case. The paralegal's decisions are in the DB but the product offers no way to export or re-run, with no message. It makes the export must-have unusable for that case, and recovery needs a delete or database surgery.",
   "fix": "On startup (create_app) and in GET status, treat status=running with no live run for that token (not in runs) as failed with error run_interrupted ('The run was interrupted; finished items and your decisions are kept. Run it again.'), so the case shows Run again and the export gate shows RUN_FAILED. Also let /run proceed when status is running but the token is not in `runs` and the started_at is older than DEADLINE_S.",
   "acceptance_test": "E2E: start a run, SIGKILL and restart the server on the same DB, then assert GET status is failed/run_interrupted, the UI shows a visible retry, POST /run with confirm_rerun returns 202, the earlier accepted ids are unchanged, and export is allowed after the re-run. Repeat with 3 accepted items present."},
  {"severity": "major",
   "title": "Decision from a stale second tab silently overrides the first tab's dismissal; the first tab then exports an item it displays as dismissed",
   "evidence": "GATE-M3-chaos-twotabs2.py: tab1 Dismiss e4; tab2 (stale, still pending) Accept e4. Output: 'after t2 (stale) accept: server accepted | t1 UI still shows: dismissed'; events e4 dismiss, e4 accept; 't1 shows e4: dismissed | progress: 1 of 23 decided'; letter from tab 1 contains the e4 quote (January 23, 2026 Capital PT); 'e4 row still dismissed in t1 after export'. Screenshot GATE-M3-chaos-twotabs-stale-export.png. Reproduced twice (twotabs.py). api.md has no version or expected-status check on /review (grep for stale/etag/expected_status found nothing).",
   "why_it_matters": "Checklist 15: decisions must not be reverted silently. A paralegal who dismissed an item and sees it Dismissed on screen can export a letter that contains it, with no warning. Persisted state is arguably the last human action, but the screen contradicts it.",
   "fix": "Send the client's last-seen review_status (or an updated_at/version) with each review POST and return 409 stale_decision with the current state when it differs; the UI then refreshes that item and says 'This item was changed in another tab.' Also refetch the case when a tab regains focus, and before building the export view.",
   "acceptance_test": "Playwright two-tab test: tab1 dismiss e4, tab2 (loaded before) accept e4 -> tab2 shows the 'changed elsewhere' message and e4 stays dismissed; tab1 export excludes e4; the server events show exactly one e4 decision."},
  {"severity": "major",
   "title": "Zero-width-only paste passes the empty check, creates a case and runs 3 model calls",
   "evidence": "GATE-M3-chaos-zwsp-ui.py 7872: spaces-only -> 'There is no text to read'; zero-width-only (U+200B x3) -> case created; after Analyze (llm_calls,cases) goes 6,24 -> 9,25; U+2060/U+FEFF/U+200D -> 9,25 -> 12,26; screen 'Record 1: no readable date ... The analysis did not finish'. Rows: llm_calls steps split, extract, flags. ingest.normalize_text/check_limits (ingest.py:30-42) use str.strip(), which keeps format characters. On demo server A the same paste is masked by the 409 (GATE-M3-chaos-api-7871.out.txt).",
   "why_it_matters": "Checklist 1 / R-CO-5: invalid input must cost no model call. With a live backend this is paid spend on an input with no visible characters; a paste of only invisible characters is realistic from copy/paste of a blank PDF page.",
   "fix": "In check_limits, treat text with no characters outside Unicode categories Z*, Cc and Cf (zero-width, BOM, word joiner, bidi marks) as empty (400 bad_request 'Input is empty.'); apply the same test client-side.",
   "acceptance_test": "Unit and E2E: texts of only U+200B, U+200D, U+2060, U+FEFF, U+200E and mixtures with whitespace each get 400/empty message and leave llm_calls and cases counts unchanged (extend tests/e2e/test_adversarial_ui.py's whitespace parametrisation)."},
  {"severity": "major",
   "title": "A lone UTF-16 surrogate in pasted text returns HTTP 500; the UI shows a retry message that can never succeed",
   "evidence": "GATE-M3-chaos-surrogate-ui.py 7871 and 7872: textarea holds '\\ud83d'; POST /api/cases -> 500; UI error 'We couldn't start the analysis. Your text is still here. Try again'. GATE-M3-chaos-api.py 'lone-surrogate: 500 {\"error\":{\"code\":\"internal\",\"message\":\"Something went wrong.\"}}'. Server log: 'unhandled UnicodeEncodeError at api.py:56' (demo, digest()) and 'at db.py:111' (live-looking server, sha256()). No case stored. Screenshots GATE-M3-chaos-surrogate-ui-7871.png/-7872.png.",
   "why_it_matters": "A 5xx from user text; the paralegal is told to retry something that will fail every time and gets no hint that the text is the problem. I rated it major because there is no stack trace, the process survives and nothing is stored; if §5 'crash from any input' is read to cover a 5xx it is a blocker (my judgement, stated openly).",
   "fix": "Validate text in check_limits: try text.encode('utf-8') and on UnicodeEncodeError raise IngestError('bad_request') with a specific message ('The text has a broken character; copy it again from the source.'). Same for title.",
   "acceptance_test": "API and Playwright test: a body with '\\ud83d' in text or title returns 400 with that message, the UI error names the problem and keeps the paste, no 500 is logged, and the case/llm_calls counts do not change."},
  {"severity": "minor",
   "title": "Export gate says 'Nothing is accepted or edited yet' right after the paralegal edited an entry",
   "evidence": "GATE-M3-chaos-edit2.py 7871: edit e5 -> 200, entry shows 'Needs review | Edited'; GET /export -> 422 NOTHING_ACCEPTED 'Nothing is accepted or edited yet, so the letter would be empty.' next_action 'Accept, edit or dismiss this item.' The UI export-blocked box repeats it (screenshot GATE-M3-chaos-edit-export.png).",
   "why_it_matters": "The message contradicts what the user just did and does not name the real next step (accept the edit once the check can confirm it). Behaviour is safe: no unconfirmed item is exported.",
   "fix": "When any entry is edited but unconfirmed, give a specific blocker/next action: 'You edited N entries, but an edited entry also needs Accept before it goes in the letter.'",
   "acceptance_test": "E2E: edit one entry in demo mode, press Export; the message names the edited entry and says to Accept it; accepting it makes the export list exactly that entry."},
  {"severity": "minor",
   "title": "No rate limit or backpressure on case creation or runs",
   "evidence": "GATE-M3-chaos-parallel.out.txt: '50 creates: Counter({201: 50})'; 20 simultaneous /run all 202/409 with no 429 (GATE-M3-chaos-parallelrun.out.txt). The only 429 in the app is pdf_busy (api.py PDF route). Checklist item 19 is a persona item, not a spec constraint.",
   "why_it_matters": "With a live backend each Analyze spends model calls; one client can start unbounded cases and runs. No 5xx was seen.",
   "fix": "A small per-client limit on POST /api/cases and /run (for example N per minute) returning 429 'Too many requests, wait a moment', plus a global cap on concurrent pipelines.",
   "acceptance_test": "Test: 50 parallel POST /api/cases from one client returns some 429 with a plain message and no 5xx; the app stays responsive; normal single use is unaffected."}
 ],
 "whats_right": [
  "The export is always derived from persisted state: across the 400-key mash, 40 racing accept/dismiss posts, Back/Forward, reloads and dismiss-all then accept-some, export ids equalled the accepted set every time.",
  "Ambiguous or invalid dates (05/07/11, 2023-02-29, Feb 30, 3/4) are flagged for confirmation and never guessed, and only a 31-day gap flags.",
  "Injected instructions change nothing (case_07 flag and banner, $50,000 stays out of the total), and every network or 500 failure leaves item state unchanged with a visible message."],
 "questions_for_chris": [
  "Is a 5xx on malformed input (the lone surrogate, finding 4) a 'crash from any input' blocker in your reading of the persona §5, or a major? I filed major."
 ]}
```
