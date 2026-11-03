# T-114 review: paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 1 major, 1 minor, 1 nit). The three asks hold on the running backend. The rate row is acknowledge-only, never blocks export, never reaches the total, and every acceptable item on all 15 library packets exports without JUDGE_NOT_RUN. confirm_date reports the lib09 gap as 42 to 40 days. What is still open is the part of T-060 F4 that is a UI job: the new figure appears with no notice in HEAD.

## What I ran

Deterministic first.

- `git rev-parse HEAD` printed `b5fb35c743dced9cad3f3dc700e853dc42f4da8e`. I extracted `git archive HEAD` into `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/unit/test_t114_rates_and_demo_judges.py -q -p no:cacheprovider` on that copy printed `20 passed in 7.82s`.
- Server from the copy: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, `ZLAYT_DB` in my scratchpad, `HOST=127.0.0.1 PORT=7881`. Started twice (PID 32148, then PID 41378). Both stopped by PID. `curl` to 7881 returns 000 afterwards. The team app on 7860 was not touched (still 200).

Live checks (scripts in `artifacts/review-evidence/`):

- `T-114-paralegal-api-checks.py` (stdlib, run `.venv/bin/python -I`), output `T-114-paralegal-api-checks.out.json`, log `T-114-api-checks-run.log`. Covers the rate accept, the 15 packets in two date variants (dates confirmed to the first candidate; left unconfirmed), and confirm_date on lib09 record 4.
- `T-114-paralegal-gate-before.py`: lib09 gate before any accept shows `NOTHING_ACCEPTED` (status fail, blocking 1). That explains the "Export blocked by 1" the UI shows before any accept. After accepting only a3 the gate is `pass` with `blocking 0` and `judge_not_run 0`. Printed to terminal, not saved.
- `T-114-paralegal-ui-rates.py` (Playwright, Chromium, 1440x900): opened the lib09 case, accepted both rate rows, read the rows and the summary bar. Screenshots `T-114-ui-1-rates-before-accept.png` and `T-114-ui-2-rates-after-accept.png`; output `T-114-paralegal-ui-rates.out.json`.
- Code read at HEAD: `app/backend/trace.py:505, 792-801`; `app/backend/present.py:57-66`; `app/backend/review.py:330-363, 400-429`; `evals/library/case_lib09_spanish_interpreter_espalda.expected.json:219-222, 479-483`; `evals/golden/check_golden.py:250-260`.
- Grep at HEAD: `grep -rn gap_changes app/frontend/` returns nothing. `git show b5fb35c:app/frontend/timeline.js` has no `gap_changes`. The working tree does have a consumer at `app/frontend/timeline.js:50-56`, but it is uncommitted and not in b5fb35c. I did not review it.

Results against the three asks:

1. **lib09 rate row.** Accepting a3 and a6 returns 200 each, with `review_status` accepted, `accept_effect` acknowledge, `judge_required_for_export` false. Accepted total stays 0 cents. Gate after both rates: `ready` true, JUDGE_NOT_RUN list empty, export 200. After also accepting the two verified charges (a1 $2,940 and a4 $2,150), the letter total line is `Billed charges stated in these records: $5,090.00`. The two $400.00 rates appear only in `internal_notes_text`. In the UI the accepted row shows the chips "Needs review" and "Accepted", and the sentence "Noted for the internal notes only; not in the letter or the total." (see finding 2).
2. **Every acceptable item on the demo packets.** 15 packets x 2 variants = 30 exports. All 30 gates `ready`, JUDGE_NOT_RUN empty, no other blocker code, export 200. Accepted items: 271 per variant. Seven server refusals in total, all with plain messages and none a judge block: `CODE_CHECK_FAILED` on lib02 e4 and lib06 e5 (summary word not in the quote); `DATE_UNCONFIRMED` on lib14 e5 (both variants) and lib09 e4 (unconfirmed variant only).
3. **confirm_date gap_changes.** Confirming lib09 record 4 as 2026-03-05 returns `gap_changes` with one entry: `change` changed, `old_days` 42, `new_days` 40, `old_from` 2026-03-03, `new_from` 2026-03-05, both `to` 2026-04-14, and `sentence` "Gap recalculated after you confirmed record 4: now 40 days (was 42)." The flag id moves to `f_gap_r4_r2` with `record_nos` [2, 4].

Not exercised: whether the UI offers Accept on the seven refused items; the blank-judge path on the live server (covered only by the unit test, which passed); the rest of the T-060 list.

## Findings

### Major: the 42 to 40 change is reported by the API only; HEAD's UI shows the new figure with no notice

Evidence: `artifacts/review-evidence/T-114-paralegal-api-checks.out.json` (C_gap). `grep -rn gap_changes app/frontend/` on b5fb35c returns nothing. The uncommitted consumer in the working tree is not part of this card.

Why it matters: T-060 F4 asked that a figure that changes after a decision say so. The backend AC is met, and the handoff says the frontend note stays on T-060. In the build as committed, a paralegal who confirms record 4 sees "Gap of 40 days" with no reason, ending at an intake form. The adjuster counts days between treatment encounters, and she needs to know why the number moved.

Fix: frontend (under T-060): render `gap_changes[].sentence` beside the gap flag and in the flags tray after confirm_date. The open question of whether an intake form should ever be an endpoint is in questions_for_chris.

Acceptance test: Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05. The gap flag card shows "Gap recalculated after you confirmed record 4: now 40 days (was 42)." and names the 2026-03-05 start.

### Minor: an accepted rate row still reads "Needs review" and keeps a primary "Accept as noted" button

Evidence: `artifacts/review-evidence/T-114-ui-2-rates-after-accept.png` (the $400.00 Rate rows show chips "Needs review" and "Accepted"; primary button "Accept as noted"). `T-114-paralegal-ui-rates.out.json` after_rates.a3: `data_review` accepted, `data_state` needs_review.

Why it matters: the money side is right; the rate is out of the total and does not block export. But an accepted row that still says "Needs review" and invites a second Accept looks unfinished, the same pattern as T-060 F6 and F7. The code says "acknowledge", the row says "Accepted", the sentence says "Noted". Pick one.

Fix: after acknowledge, the state chip reads something like "Noted, not in letter" and the primary control becomes Undo or Reset. Keep the internal-notes sentence.

Acceptance test: lib09 after accepting a3: the row has no "Needs review" chip and its primary control is not "Accept as noted".

### Nit: the lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped

Evidence: scratch DB on the first server, `SELECT ... FROM llm_calls WHERE error LIKE 'FIXTURE_MISS%'` returns 4 rows: step extract, attempt 1, parsed_ok 0, error "FIXTURE_MISS 83bcee077841...", all on cases named "case lib01 er only then gap" (status ready). The lib01 case stored 6 records and 6 entries. `grep -c "^=== Record" evals/library/case_lib01_er_only_then_gap.txt` returns 6. I did not trace which path produced the lib01 extraction.

Why it matters: nothing is lost here, but the demo leans on a logged miss for lib01, which is the kind of demo dead end T-114 set out to close.

Fix: record the lib01 extract response in `tests/fixtures/llm/` (curated set), or note the fallback on the card.

Acceptance test: a fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls.

## Right already

- Accepting a rate is acknowledge-only at every layer I checked. The API says so (`accept_effect` acknowledge, `judge_required_for_export` false). The gate agrees. The letter total excludes it. The UI says it is in the internal notes only.
- Every acceptable item on the 15 demo packets exports with no JUDGE_NOT_RUN, in both date variants, and every refusal names the next step.
- The confirm_date response carries old and new endpoints, old and new days, and a plain sentence. The backend side of gap_changes is complete.

```json
{"card": "T-114", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD = b5fb35c, extracted to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, stopped by PID); sample case: library case_lib09_spanish_interpreter_espalda plus all 15 library packets in two date variants",
 "exercised": [
  "git rev-parse HEAD and git cat-file -t b5fb35c (board show T-114 handoff read)",
  "pytest tests/unit/test_t114_rates_and_demo_judges.py on the archive copy: 20 passed in 7.82s",
  "API: lib09 accept a3 and a6 (200, acknowledge, total 0 cents), gate after rates (ready, no JUDGE_NOT_RUN), export letter total with a1 and a4 accepted ($5,090.00), internal notes with the rate lines",
  "API: all 15 library packets, two variants (dates confirmed, dates unconfirmed): 30 gates ready, 0 JUDGE_NOT_RUN, 30 exports 200, 7 plain 422 refusals recorded",
  "API: lib09 confirm_date r4 to 2026-03-05: gap_changes 42 to 40 with sentence; gap flag endpoints before and after; records encounter and date_status",
  "Playwright on lib09 (1440x900): accepted both rate rows in the UI; read the row text and the summary bar; two screenshots",
  "Gate before and after one rate accept (NOTHING_ACCEPTED explains the pre-accept 'Export blocked by 1')",
  "Scratch DB llm_calls query for FIXTURE_MISS rows; lib01 record count versus packet headers",
  "Read app/backend/trace.py, present.py, review.py, evals/golden/check_golden.py, the lib09 expected.json; grep for gap_changes in HEAD frontend (none)"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "rate_row_clarity": 3, "export_jnr_free_demo_packets": 5, "rate_never_in_total": 5, "gap_change_reported_by_api": 5, "gap_change_visible_in_head_ui": 1},
 "findings": [
  {"severity": "major", "title": "The lib09 gap change (42 to 40 days) is returned by the API, but HEAD's UI shows the new figure with no notice",
   "evidence": "artifacts/review-evidence/T-114-paralegal-api-checks.out.json C_gap.gap_changes[0].sentence = Gap recalculated after you confirmed record 4: now 40 days (was 42).; C_gap.after = f_gap_r4_r2, days 40, from 2026-03-05, record_nos [2,4]. grep -rn gap_changes app/frontend/ on b5fb35c returns nothing. Working-tree consumer app/frontend/timeline.js:50-56 is uncommitted and not in b5fb35c (not reviewed).",
   "why_it_matters": "T-060 F4 asked that a figure which changes after a decision say so. The backend AC is met, but in the committed build a paralegal who confirms record 4 sees Gap of 40 days with no reason, ending at an intake form. The adjuster counts days between treatment encounters and needs to see why the figure moved.",
   "fix": "Frontend, under T-060: render gap_changes[].sentence beside the gap flag and in the flags tray after confirm_date. Whether an intake form should ever be a gap endpoint is a decision for Chris (questions_for_chris 1).",
   "acceptance_test": "Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05; the gap flag card shows Gap recalculated after you confirmed record 4: now 40 days (was 42). and names 2026-03-05 as the start."},
  {"severity": "minor", "title": "An accepted rate row still reads Needs review and keeps a primary Accept as noted button",
   "evidence": "artifacts/review-evidence/T-114-ui-2-rates-after-accept.png (chips Needs review and Accepted; primary button Accept as noted; text Noted for the internal notes only; not in the letter or the total.). artifacts/review-evidence/T-114-paralegal-ui-rates.out.json after_rates.a3: data_review accepted, data_state needs_review. app/backend/present.py:57-66 (accept_effect acknowledge).",
   "why_it_matters": "The money side is right: the rate is out of the total and does not block export. An accepted row that still says Needs review and invites a second Accept looks unfinished (T-060 F6/F7 pattern). The code says acknowledge, the chip says Accepted, the sentence says Noted.",
   "fix": "After acknowledge, the state chip reads something like Noted, not in letter, and the primary control becomes Undo or Reset. Keep the internal-notes sentence.",
   "acceptance_test": "lib09 after accepting a3: the row has no Needs review chip and its primary control is not Accept as noted."},
  {"severity": "nit", "title": "The lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped",
   "evidence": "Scratch DB (first server) query on llm_calls WHERE error LIKE FIXTURE_MISS%: 4 rows, step extract, attempt 1, parsed_ok 0, error FIXTURE_MISS 83bcee077841..., all on case lib01 er only then gap (status ready). Stored 6 records and 6 entries; grep -c ^=== Record evals/library/case_lib01_er_only_then_gap.txt returns 6.",
   "why_it_matters": "Nothing is lost, but the lib01 demo depends on a logged fixture miss, the kind of demo dead end T-114 set out to close. I did not trace which path produced the lib01 extraction.",
   "fix": "Record the lib01 extract response in tests/fixtures/llm (curated set), or note the fallback on the card.",
   "acceptance_test": "Fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls."}
 ],
 "whats_right": [
  "Accepting a rate is acknowledge-only at every layer checked: API accept_effect acknowledge with judge_required_for_export false, gate agrees, letter total excludes it, UI says it is in the internal notes only.",
  "All 15 library packets export with no JUDGE_NOT_RUN in both date variants (30 of 30 gates ready), and every refusal names the next step.",
  "confirm_date returns old and new endpoints, old and new days, and a plain sentence; the backend side of gap_changes is complete."
 ],
 "questions_for_chris": [
  "Should a dated admission or intake form ever be a gap endpoint? evals/library/case_lib09_spanish_interpreter_espalda.expected.json records entry 4 has kind encounter with date null, and must_not_flag N1 excludes it only as an ambiguous-date intake. Once confirmed, the product counts it (encounter true), so the lib09 figure goes 42 to 40. T-060 F4 says an intake form must never be an endpoint. This changes the number the adjuster sees, so it needs a decision. Whether the gap goes in the demand is litigation-lead's call, outside my lens.",
  "A rate whose second check disagrees (for example SHOULD_BE_CHARGE) still gets acknowledge-only treatment: acknowledge_only() is kind-based (app/backend/trace.py:792-795) and does not read the judge verdict. Should a disagreeing check on a rate force a decision before Accept?",
  "Seven refusals on the demo packets (lib02 e4 and lib06 e5 CODE_CHECK_FAILED; lib14 e5 and lib09 e4 DATE_UNCONFIRMED in one variant). The server messages name the next step. I did not check whether the UI offers Accept on them. Does the T-060 F3 rule (offer only what can be accepted) cover them?"
 ]}
```
