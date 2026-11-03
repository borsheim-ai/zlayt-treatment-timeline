# T-154 round 2 — claims-adjuster-reviewer (Gary Pruitt)

Verdict: fail (one blocker, one minor).

Commit 6379c0b does not run. The new `a`-key guard was committed inside `mountSection()` in `app/frontend/review.js` (lines 474-477), not inside the keydown handler. That function has no `key` or `f`, so every call throws `ReferenceError: key is not defined`. Every case load stops on "The analysis did not finish ... key is not defined", and the charges panel never renders. I could not run any of my round-1 attacks on the commit. A paralegal cannot even reach a charge row.

Tree tested: `git archive 6379c0b` into the scratchpad, app on 127.0.0.1:7873 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB). The ledger from round 1 was copied into that copy's `evals/golden/` so demo mode accepts the paste. The working tree has the block in the right place (uncommitted, plus other workers' edits), so the worker's "12/12" must have been run on that tree, not on the commit.

Proof on the commit:
- lib10 on 7873: pageerror `ReferenceError: key is not defined at mountSection (review.js:474:5) at review.js:481:83 at timeline.js:341:37 at ZL.renderReview`; `charges-panel count: 0`; run-error text "The analysis did not finish. Your records are kept and finished items are saved. key is not defined".
- The pasted ledger shows the same banner and "Entries None".
- `E2E_BASE_URL=http://127.0.0.1:7873 .venv/bin/python -m pytest tests/e2e/test_charge_confirm.py -p no:cacheprovider -q` gave `11 failed, 1 passed in 317.95s`. The panel never appears (`waiting for get_by_test_id("charges-panel").locator("[data-item-id=\"a1\"]")`).

Because the commit is unusable, I also ran a simulated fix, clearly not the commit: a second scratch copy (port 7874) where I moved the same four lines into the key handler, before the `askCompare` line. I report it so the worker knows what else holds once the guard is in the right place. It is not a pass for the commit.
- `a` on an accepted, confirmed flagged charge (a4 Likely total): no dialog, no POST, live region "Accepted already. Use Undo to change it." Two more `a` presses: still nothing. POSTs for the whole run were `a5 {"action":"accept"}` and `a4 {"action":"accept","confirm":"likely_total"}` only. The Accept button on the row reads "Accepted" and sends nothing.
- Audit panel for a4: "Your decisions | Likely total The code flagged this charge: likely total. You confirmed that flag by name at 2026-11-02T15:01:11Z, so the charge is counted. | accept, confirmed Likely total | 2026-11-02T15:01:11Z". "How this was checked" for a4 opens with the same flag step. a5 (no flag) shows a single plain `accept`.
- No lowercase-underscore flag token (likely_total, CONFIRM_REQUIRED and so on) in the dialog, audit, trace or page body. (The fixture run shows `JUDGE_NOT_RUN` and `FIXTURE_MISS` in the trace; that is the fixture backend and outside this card.)
- On this ledger the same-service 04/09 line merges into one amount, so there is no flagged duplicate to click. At 6379c0b `likely_duplicate` comes only from promoting a figure to a charge (`promotion_flag`, reclassify.py), which needs a judge call. I could not reach it with the fixture backend, so I tested the duplicate wording by answering the accept POST with the backend's own 422 text (r2dup.py). See the minor finding.
- Backend audit fields (T-159): the audit and trace lines here are built by the page from `flag.confirmed_at`. I noted this and did not count it.

```json
{"card": "T-154", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 6379c0b (T-154 r2) extracted to scratchpad; app on http://127.0.0.1:7873, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB; UI only (Playwright); lib10 and pasted SYNTHETIC ledger artifacts/review-evidence/t154/ledger.txt (copied into the scratch copy's evals/golden); plus one simulated-fix copy on 7874 that is NOT the commit",
 "exercised": [
  "python3 tools/board.py show T-154; reviews/T-154-claims-adjuster.md; git show 6379c0b -- app/frontend/review.js; git diff 6379c0b -- app/frontend/review.js (working tree has the block moved into the key handler, uncommitted)",
  "git archive 6379c0b into the scratchpad; app started on 7873; health check ok; stopped by PID 11525, port confirmed down",
  "UI on 7873: lib10 load (r2err.py) -> pageerror 'key is not defined' at mountSection review.js:474, charges-panel count 0, run-error banner; pasted ledger load (r2peek.py) -> same banner",
  "tests/e2e/test_charge_confirm.py against 7873: 11 failed, 1 passed (charges panel never renders)",
  "simulated fix on a second scratch copy (guard moved into the key handler), port 7874, stopped by PID 16845: r2p.py ran a on accepted+confirmed a4 and a5 (no dialog, zero POSTs, 'Accepted already. Use Undo to change it.'), Accept button on accepted row, Audit panel and 'How this was checked' for a4 and a5, raw-token scan of dialog/audit/trace/body, Undo then Accept; same e2e file against 7874: 11 passed, 1 failed (test_the_a_key_asks_first_and_escape_cancels, line 116, not investigated further because it is a simulation)",
  "r2dup.py on 7874: accept POST answered with the backend's own CONFIRM_REQUIRED sentence (amounts.py:517, review.py:206) for of=a3 and of=ax2_1; read the dialog text",
  "read app/backend/amounts.py (confirm_info, promotion_flag), app/backend/reclassify.py (_promotion_flag), app/backend/review.py (confirm_error), app/frontend/charges.js plain()"
 ],
 "verdict": "fail",
 "scores": {"app_runs_at_commit": 1, "a_key_on_confirmed_flagged_charge": 1, "audit_and_trace_name_the_confirm": 4, "no_raw_tokens": 4, "duplicate_named_by_its_line": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Commit 6379c0b throws ReferenceError on every case load: the a-key guard was committed inside mountSection(), so no panel renders and the round-1 major is not fixed at the commit",
   "evidence": "app/frontend/review.js at 6379c0b, lines 471-478: `function mountSection(mountEl, name) { let s = ...; if (!s) { ... } if (key === \"a\" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) { RV.say(...); return; } return s; }`. `key` and `f` exist only in the keydown handler (lines 446 and 455). Browser result on lib10 at port 7873: `PAGEERROR: key is not defined | ReferenceError: key is not defined / at mountSection (http://127.0.0.1:7873/review.js:474:5) / at http://127.0.0.1:7873/review.js:481:83 / at http://127.0.0.1:7873/timeline.js:341:37 / at ZL.renderReview`; `charges-panel count: 0 | run-error: The analysis did not finish. Your records are kept and finished items are saved. key is not defined`. Pasted ledger: same banner, 'Entries None', 'Amounts 0 of 5'. `E2E_BASE_URL=http://127.0.0.1:7873 .venv/bin/python -m pytest tests/e2e/test_charge_confirm.py -p no:cacheprovider -q` -> `11 failed, 1 passed in 317.95s`. The handler's own `a` branch at that commit (review.js:463-464) is unchanged: `if (key === \"a\") RV.act(id, { action: \"accept\" }, { advance: true });`, so a key press on a confirmed flagged charge would still go to the server. Screenshot: artifacts/review-evidence/t154/r2_lib10_broken.png. Evidence scripts: r2err.py, r2peek.py, r2.py.",
   "why_it_matters": "The whole review screen is unusable: no charge, flag or confirm can be reached. This is a must-have made unusable, and the worker's handoff ('12/12 ... a-key test fails without the guard') does not describe the commit it names. A tree run that passes while the commit fails is a process gap, not a fluke: the temp-index commit took the hunk to the wrong place.",
   "fix": "Move the four-line guard from mountSection() to the keydown handler, after the dismissed check and before the editToCheck/askCompare line (the uncommitted working tree already has it there). Restore mountSection() to `return s;` only. Run the e2e from a `git archive HEAD` of the new commit, not from the dirty tree.",
   "acceptance_test": "From `git archive` of the fix commit: load lib10 and the pasted ledger with zero pageerror events and charges-panel visible; tests/e2e/test_charge_confirm.py passes 12/12; confirm a flagged charge, focus its row, press a: no charge-confirm dialog, no review POST, live region says it is already accepted, Audit shows one accept."},
  {"severity": "minor",
   "title": "Duplicate sentence can still show an internal id (ids with an underscore), and the real backend text carries no service name although the code comment and the e2e test say it does",
   "evidence": "charges.js plain() replaces only `/(same charge as) [a-z]\\d+(?=[:,.]|\\s)/i`. Answering the accept POST with the backend's own CONFIRM_REQUIRED text and of='ax2_1' (the id form amounts.py gives records the paralegal marked separate) the dialog reads: 'This looks like the same charge as ax2_1: $150.00 on 2026-04-09, already listed from record 2. Counting both would count one service twice.' With of='a3' it reads 'same charge as this earlier line: $150.00 on 2026-04-09, already listed from record 2.' amounts.py:623 builds the detail as `f\"{_usd(target['cents'])} on {b['dos']}, already listed from record {o['record_no']}. \"` with no service. tests/e2e/test_charge_confirm.py:262 asserts 'therapeutic exercise $150.00 on 2026-04-09' only because its stub message contains the service; the comment at charges.js:63 says 'told by its service, amount, date and record'. Screenshots: r2_dup_a3.png, r2_dup_ax2_1.png (7874, simulated-fix copy; the sentence code is the same as the commit).",
   "why_it_matters": "She is meant to find the other line by what it says. Date, amount and record find it; the service is missing, so two same-day same-amount lines in one record could not be told apart. An id like ax2_1 on screen is a machine word. The stub-only assertion means the test would keep passing if the real wording stayed as is.",
   "fix": "Widen the id match to the full id form (`[a-z]+\\d+(?:_\\d+)?`). Ask the backend (T-159 covers the sentence) to put the service in the detail, and make the e2e use the backend's real string.",
   "acceptance_test": "Unit check on plain(): with of in {a3, ax2_1, ax10_12} no /\\ba[a-z]*\\d+(_\\d+)?\\b/ remains in the output; the duplicate e2e stub text equals the string produced by amounts.promotion_flag for the same case."}
 ],
 "whats_right": [
  "On a copy where the guard sits in the key handler: a on an accepted, confirmed flagged charge opens nothing, sends nothing and says 'Accepted already. Use Undo to change it.'",
  "The Audit panel and 'How this was checked' name the flag and the named confirm with the time ('accept, confirmed Likely total'), and no raw flag token reaches the dialog, audit, trace or page body.",
  "Batch, named confirm and Cancel/Escape paths from round 1 are untouched by the change; the plain Accept on an unflagged charge (a5) is a single 200 with no dialog."
 ],
 "questions_for_chris": [
  "The fixture backend cannot produce a flagged likely_duplicate on a pasted ledger any more (promotion only, needs a judge call). Is a library case with a promoted duplicate planned so this path can be clicked on the real server without a stub?"
 ]}
```
