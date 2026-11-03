# T-178 chaos-tester recheck (chaos-tester-reviewer, commit a56f189)

**Verdict: pass (0 blockers, 0 majors, 2 minors).** All four GATE-M3 findings (B1, M1, M2, M3) are fixed at the API level.

Setup: `git archive a56f189` copy in my scratchpad, fixture backend, `ZLAYT_MODE=local`, own SQLite files, spare ports 7881-7884. Servers 7882 (demo) and 7883 (fixture backend plus `ENABLE_LIVE=1` and a dummy key, so arbitrary text reaches ingest with no network) were stopped by PID at the end. 7881 was killed by the interrupt script itself. 7884 was the old d0b04bc copy, used for one before/after comparison. `lsof` shows no listener left on 7881-7884. All inputs are SYNTHETIC. Scripts and outputs are in `artifacts/review-evidence/T-178-chaos-*`.

## What I re-checked

**B1 interrupted run: fixed.** `T-178-chaos-interrupt.py`, run on a fresh DB.
- Scenario A (first run). SIGKILL straight after the 202. The DB showed `('running','extract')` at kill time. After restart the case reads `failed`, `error.code run_partial`, `interrupted: true`. The message is: "The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry." `POST /run` returned 202, then the case went `ready`.
- Scenario B (re-run with e1, e4, e5 accepted). `/run` without confirm returned 409 `needs_confirm`. With `confirm_rerun` it returned 202 and I killed the server again; the DB showed `running` at kill time. After restart:
  - Status was `failed` with `interrupted: true`. The decisions on e1, e4 and e5 were unchanged.
  - Export returned 422 `RUN_FAILED` with next action `CONFIRM_RERUN`. That is the contract (the export is blocked until the run is repeated), and the message is plain.
  - I could still accept e6 while the case was interrupted.
  - The re-run with confirm returned 202, then `ready`. Decisions were e1, e4, e5, e6, and export returned 200 with items 1, 4, 5, 6, exactly the accepted set. The review events were exactly four accepts.
- Scenario C (mid-review, two restarts in a row). The case stayed `ready`, e1 stayed accepted and export returned 200.

**M1 stale write (API only): fixed, UI not yet.** `T-178-chaos-stale.py` printed 29 PASS lines and no FAIL.
- Tab 1 dismissed e4 (version 1793651878.27 became .53). Tab 2 then posted an accept with the old version. It returned 409 `stale_item` with the message "This item changed in another tab; reload to see it." and the detail showed the current state (dismissed). No review event was written (1 event before, 1 after) and e4 stayed dismissed.
- Version-only and expected_status-only stale writes both return 409. Stale `edit` and `reset` also return 409.
- ABA case: tab 1 reset the item to pending, so the status looks the same as tab 2's view. The stale version still returns 409, so `version` closes a hole that `expected_status` alone leaves open.
- A fresh write succeeds. A post with neither field is unchecked, as documented. A stale repeat of the same decision (dismiss on an already dismissed item) returns 200, as documented.
- Amounts and flags are covered too (a1 and f_gap_r6_r7 stale accept return 409).
- Bad values (string, boolean, list, bogus or non-string `expected_status`) return 422 with a plain message, never 5xx.
- `T-178-chaos-stale2.py`: ten accepts and ten dismisses racing on one item with the same version. Exactly one side won each round (10x200 and 10x409) and the final state matched. The end-to-end two-tab case stays open until the UI sends the version.

**M2 zero-width paste: fixed.** `T-178-chaos-pastes.py` on the live-looking fixture server.
- Pastes made only of U+200B, 200C, 200D, 2060, FEFF, 200E, 202E, 00AD, 180E, E0041 or 2066, or of a mix with spaces, tabs, newlines and NBSP, all return 400 "Input is empty." The `(llm_calls, cases)` counts stayed at (0,0) before and after every probe. A 50,000-character zero-width paste returns the same 400.
- Zero-width characters inside real text: the case is created, the stored text has no format characters, and a run makes 3 model calls as expected.
- 60,000 visible characters plus 5,000 zero-width are accepted, so invisible characters do not count toward the limit.

**M3 surrogate 500: fixed.** A lone high or low surrogate, a reversed pair and 20,000 surrogates in the text, plus surrogates in the title, an unknown field, a library id and the URL path, all return 201, 400 or 404. Never 500. A valid pair is kept. The title is stored with U+FFFD. Running the cleaned text gives a visible `failed` state, not a 5xx.

**Other odd inputs, no 500 except one (minor 2).** NUL bytes, control and C1 characters, private-use characters and non-characters are accepted as text. Invalid UTF-8 and random binary bodies return 400. A number, list or null in `text`, a JSON array body, a huge number, form-encoded bodies and an empty body all return 400. A UTF-16 body is accepted as text. A 1 MB text gets 413 and a 5 MB text gets 413 with curl. Sample x200 gets 413. 60k RTL Arabic gets 400 `unsupported_language`. The 413s mean no model call, no case and no 500. Python's urllib sees a broken pipe on the 2 MB+ bodies because the server answers before reading the body. That is a client-side artifact, and curl gets the 413.

**Suite.** `tests/unit/test_t178_chaos.py` on the archive: 68 passed (`T-178-chaos-unit.out.txt`).

## Minors
**m1. A `version` of NaN bypasses the stale check.** `POST .../items/e2/review {"action":"accept","version":NaN}` on a stale item returned 200 and accepted an item that was dismissed. The check at `review.py:287` computes `abs(float(ver) - ...) > 1e-6`, which is False for NaN. `Infinity` and `-Infinity` correctly give 409. A browser cannot send NaN (`JSON.stringify` turns it into null), so this is a hand-built or non-standard client. It matters for the "stale write returns 409" guarantee, so I filed it. Repro: `T-178-chaos-stale2.py`, output in `T-178-chaos-stale2.out.txt`.

**m2. A deeply nested JSON body returns 500.** `{"text":"...","k":[[[...1500 levels...]]]}` returns 500 `internal` ("Something went wrong."). The log shows `unhandled RecursionError` at `api.py:225` (the `json.loads` call) in the old build and `api.py:247` in the new one. I confirmed the old d0b04bc gives the same result (1500, 5000 and 100,000 levels all 500; 900 levels is 201), so this is not a regression. It is not reachable from the paste box. Fix: catch `RecursionError` with `ValueError` in `body_of` and return 400 "Request body is not valid JSON."

```json
{"card": "T-178", "persona": "chaos-tester-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive a56f189 copy; fixture backend, ZLAYT_MODE=local, own SQLite DBs; ports 7881 (interrupt script), 7882 (demo, stale writes), 7883 (ENABLE_LIVE=1 with dummy key, fixture backend, pastes), 7884 (old d0b04bc, one comparison); sample case; API only, the UI does not send version yet; all inputs SYNTHETIC",
 "exercised": [
  "tests/unit/test_t178_chaos.py on the archive: 68 passed",
  "T-178-chaos-interrupt.py: SIGKILL of my own server mid first run and mid re-run with 3 accepted items (DB confirmed running at kill time), restart on the same DB, status/error/interrupted, decisions unchanged, export blocked with RUN_FAILED while interrupted, accept while interrupted, re-run with and without confirm, export 200 with exactly items 1,4,5,6 after the re-run, mid-review double restart",
  "T-178-chaos-stale.py: two-tab stale accept/edit/reset, version-only and expected_status-only, ABA, fresh and no-version writes, repeat dismiss, bad version/status values, amount and flag items, event count unchanged after 409, export",
  "T-178-chaos-stale2.py: NaN/Infinity version literals and 10 accept vs 10 dismiss racing with one version, 3 rounds",
  "T-178-chaos-pastes.py: 11 kinds of format-character-only pastes plus whitespace mixes, 50k and 100k zero-width, zero-width inside text, 60,000 visible plus 5,000 zero-width, 60,001, lone and reversed surrogates in text/title/unknown field/library id/path, 20k surrogates, NUL/control/C1/private-use, invalid UTF-8, binary and UTF-16 bodies, wrong JSON types, nested JSON, 1 to 25 MB bodies, sample x200, Zalgo, Arabic; llm_calls and case counts read from the DB around every probe; runs on cleaned text",
  "Extra probes in python and curl: nesting depth 500 to 100,000 on old d0b04bc versus a56f189, 1/2/5 MB bodies with curl",
  "Read review.py check_fresh, api.py body_of/_clean_strings and memory/contracts/api.md T-178 section to explain behaviour; every finding was reproduced against a running server",
  "Stopped 7882, 7883 and 7884 by PID after confirming each listened on its own port; 7881 was killed by the script; lsof shows no listeners on 7881-7884"],
 "verdict": "pass",
 "scores": {"interruption_recovery": 5, "stale_write_protection_api": 4, "input_handling": 4, "export_equals_accepted_set": 5, "error_messages": 5},
 "findings": [
  {"severity": "minor",
   "title": "A review POST with version NaN passes the stale check and overrides a newer decision",
   "evidence": "T-178-chaos-stale2.out.txt: after e2 was dismissed (so the earlier version is stale), POST /review {\"action\":\"accept\",\"version\":NaN} returned 200 and e2 became accepted ('stale item, version=NaN -> 200 ... status now: accepted'). Infinity and -Infinity returned 409. review.py:287 uses abs(float(ver) - float(updated_at)) > 1e-6, which is False for NaN.",
   "why_it_matters": "The 409 guarantee has a hole for a non-finite number. A browser cannot send NaN, so only a hand-built or non-standard client reaches it, but a stale write silently wins and the item shown as dismissed ends up in the export.",
   "fix": "In check_fresh, reject non-finite versions with 422 (math.isfinite) and treat any comparison that cannot be shown to be equal as stale.",
   "acceptance_test": "Unit test: a stale item with version NaN, Infinity or -Infinity returns 422 or 409, writes no review event, and leaves the review_status unchanged."},
  {"severity": "minor",
   "title": "A deeply nested JSON body returns HTTP 500 (RecursionError)",
   "evidence": "T-178-chaos-pastes.out.txt 'deeply nested JSON (100k) | http 500'; probe with {\"text\":\"Visit 03/17/2026 ok\",\"k\":[[[...]]]}: depth 900 gives 201, depths 1500, 5000 and 100000 give 500 {\"error\":{\"code\":\"internal\",\"message\":\"Something went wrong.\"}} on both d0b04bc and a56f189 (log: 'unhandled RecursionError at api.py:225' old, ':247' new). Not reachable from the paste box. The process survives and no case is stored.",
   "why_it_matters": "AC 1 says no 500 for any paste. A paste cannot produce this, but an API client can get a 5xx from a malformed body. Not a regression.",
   "fix": "Catch RecursionError together with ValueError around json.loads in body_of and return 400 'Request body is not valid JSON.'; make _clean_strings iterative or depth-capped.",
   "acceptance_test": "API test: a body nested 5,000 levels returns 400 with the plain message, no 'unhandled' log line, and the next request is served normally."}
 ],
 "whats_right": [
  "Startup recovery is exact: the case reads failed with interrupted true and a plain message, every accepted item is kept, and a confirmed re-run yields an export of exactly the accepted ids.",
  "The stale check refuses with 409 before any write (no review event), the version closes the ABA hole, and 20 racing posts on one item resolved cleanly.",
  "Cleaning happens before the empty check and the limits: eleven kinds of invisible-character pastes cost zero model calls and create no case, and no lone surrogate returned a 5xx."],
 "questions_for_chris": []}
```
