# T-159 staff-engineer review (D-059 audit trail for a flagged charge)

Reviewed commit 9fc579c as contained in HEAD 83f1afd, on a `git archive 83f1afd` copy (HEAD later moved to ba21b4b; `git diff 83f1afd ba21b4b --stat` touches only conflicts.py, SCOPE_CUTS.md and a T-141 test, none of this card's files).

Verdict: **changes**. No blocker. One major: AC1 is only partly delivered (the card says so itself: `internal_notes_text` does not list confirmed-flag charges). The rest of the audit trail works end to end through the API and is well pinned.

What I exercised (all on the archive copy, `.venv/bin/python`):
- `pytest tests/unit -q` at 83f1afd: 4613 passed, 8 skipped (252 s).
- API probe (TestClient, live-mode env as in `test_amounts_d059_api.make_env`) for a likely_total charge (extraction-time flag, ledger text) and a promoted likely_duplicate charge:
  - 422 CONFIRM_REQUIRED carries `detail.message` = the flag's own sentence (no token, no `a<n>`); the top-level `message` still has the "(likely_total)" token, as the AC allows.
  - Accept with the named confirm gives 200; GET /audit then shows `events[].confirm = {flag, name, confirmed_at}` in public mode (no before/after). The DB row `after_json` carries the same confirm.
  - Item trace: `charge_flag` step "Flagged by the code: Likely total", pending with `next_action.code == CONFIRM_FLAG` and "needs your named confirm", then pass with `evidence.values {flag, name, confirmed_at}`; human step says "You accepted this item and confirmed the flag "Likely total" by name."
  - Three repeat accepts (no confirm) return 200, `confirmed_at` unchanged, totals unchanged, still exactly one accept event in /audit.
  - dismiss then accept without confirm gives 422; confirm, dismiss, accept without confirm gives 422 (the no-op does not outlive a status change).
  - The duplicate sentence reads: `This looks like the same charge as “04/16/2026 manual therapy invoiced $150.00.” in record 1: $150.00 on 2026-04-16. Counting both would count one service twice.` (no id).
- Mutation run of 13 mutants against `test_t159_flag_audit.py` + `test_amounts_d059_api.py`: 11 killed, 2 survived (findings 2 and 3). Killed: dropping the no-op, dropping the event write, dropping the review_status check, dropping the charge_flag step, pending-when-confirmed, dismissed-not-skipped, detail message dropped, plain human step, audit_view dropping confirm, id back in the sentence, wrong flag name stamped.
- Failure-injection probe: made the event write in `_record_confirm` raise after the accept committed (finding 3).
- Read `git show 9fc579c` for amounts.py, present.py, reclassify.py, review.py, trace.py, api.md in full, and `git diff HEAD` to see uncommitted state.

Separation of labels: findings 1 is a card AC that is unmet (must fix before the gate). Findings 2 to 4 are test and robustness gaps I would want fixed (minor). Finding 5 is housekeeping (nit).

```json
{"card": "T-159", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 9fc579c within HEAD 83f1afd (git archive copy); app/backend/{review,trace,present,amounts,reclassify}.py, tests/unit/test_t159_flag_audit.py, memory/contracts/api.md; synthetic NOTE and ledger text; no app server",
 "exercised": ["python3 tools/board.py show T-159 and T-161; read memory/contracts/api.md D-059 paragraph", "git archive 83f1afd copy: pytest tests/unit -q -> 4613 passed, 8 skipped", "API probe via TestClient: likely_total (extraction-time) and promoted likely_duplicate: 422 CONFIRM_REQUIRED detail.message, accept with confirm, GET /audit events[].confirm in public mode, item trace charge_flag pending then pass, human step text, three repeat accepts (200, one event, totals unchanged), dismiss/reset then accept needs confirm again", "13 mutants of review.py, trace.py, present.py, amounts.py against test_t159_flag_audit.py + test_amounts_d059_api.py: 11 killed, 2 survived", "failure injection: json.loads raising inside _record_confirm after apply_review committed", "git show 9fc579c (all hunks) and git diff HEAD (found an uncommitted trace.py hunk)"],
 "verdict": "changes",
 "scores": {"audit_event_confirm": 4, "trace_flag_step": 5, "repeat_accept_noop": 5, "plain_sentence": 5, "ac_completeness": 2, "test_strength": 4, "atomicity": 3},
 "findings": [
  {"severity": "major", "title": "AC1 is not met: internal_notes_text does not list confirmed-flag charges",
   "evidence": "board T-159 AC1 text: 'internal_notes_text lists confirmed-flag charges, the letter is unchanged'; AC1 done:false; handoff note 2026-11-02T15:06:37Z 'AC1 part not done: internal_notes_text listing ... needs export.py'. `git show --stat 9fc579c` touches no export file; grep -n confirmed_at app/backend/export.py at 83f1afd finds nothing for a flag confirm.",
   "why_it_matters": "The audit trail of a D-059 confirm is meant to reach the one artifact the paralegal keeps: the internal notes. Today the confirm lives in /audit and the trace only. The card is in_review with a stated gap, so it cannot be done as written.",
   "fix": "Either add the internal-notes line (service/amount/date/record, flag name, confirmed_at) in export.py via a card for its owner or with the orchestrator's go-ahead, with the letter text byte-identical, or split AC1 into a new card with an explicit SCOPE_CUTS row and amend this card's AC.",
   "acceptance_test": "Accept a flagged charge with its confirm, call GET /api/cases/{tok}/export: internal_notes_text names the charge and the flag 'Likely duplicate' with the confirm date; letter_text equals the letter exported when the same charge was accepted without a flag change; dismissed flagged charges are not listed."},
  {"severity": "minor", "title": "Mutant survives: the confirm is stamped on the wrong accept event after reset and re-accept",
   "evidence": "mutate app/backend/review.py:228 query 'ORDER BY at DESC, rowid DESC LIMIT 1' to 'ORDER BY at ASC, rowid ASC LIMIT 1' -> 23 passed (test_t159_flag_audit.py + test_amounts_d059_api.py + test_t159 duplicate file). tests/unit/test_t159_flag_audit.py:92 test_accept_again_after_a_reset_needs_the_confirm_again asserts only len(accept_events) == 2.",
   "why_it_matters": "A flagged charge accepted, reset and accepted again has two accept events. With the mutant the second confirm overwrites the first event and the second event shows no confirm: the audit trail would be wrong exactly in the path the AC calls out.",
   "fix": "Assert in that test that both accept events carry a confirm and that their confirmed_at values differ or match the item at each step.",
   "acceptance_test": "After accept(confirm) -> reset -> accept(confirm), GET /audit shows two accept events for the item and each has its own confirm {flag, name, confirmed_at}; the ASC mutant fails."},
  {"severity": "minor", "title": "Mutant survives: repeat-accept no-op does not require confirmed_at",
   "evidence": "delete 'and bool(f.get(\"confirmed_at\"))' in review.py:212-215 confirmed_accept -> 23 passed. No test builds an accepted, flagged charge with no confirmed_at.",
   "why_it_matters": "The only way to get that state is a partial write (see next finding) or an older run; the intended behaviour (a charge with an unconfirmed flag asks for the confirm again) is unpinned.",
   "fix": "Add a unit test with an accepted flagged item whose ladder.confirm has no confirmed_at: a repeat accept without confirm is 422 CONFIRM_REQUIRED.",
   "acceptance_test": "That test passes at HEAD and fails with the confirmed_at clause removed."},
  {"severity": "minor", "title": "The confirm is written in three separate autocommit statements; a failure leaves the item confirmed and the event not, and the no-op then makes it permanent",
   "evidence": "app/backend/review.py:252-254 (apply_review, then _record_confirm) and :225-228 (DB.update_item, then a raw conn.execute UPDATE review_events outside any transaction; connection is isolation_level=None, app/db/db.py:54). Repro: patch app.backend.review.json with a loads that raises, POST accept with confirm=likely_duplicate -> 500; GET case shows review_status accepted, flag.confirmed_at set, totals.accepted 15000; /audit accept event has no confirm; a second POST accept without confirm -> 200 (no-op), so the event never gets its confirm.",
   "why_it_matters": "It is visible (a 500), not silent, but the audit event is the artifact this card exists to make reliable, and the new no-op removes the retry that would have repaired it.",
   "fix": "Write status, item confirm and event confirm in one transaction (give DB.apply_review an optional extra for after_json), or have the repeat-accept path repair an accepted event whose confirm is missing.",
   "acceptance_test": "Inject a failure into the event write: either nothing is accepted (status pending, no confirm anywhere) or a retry leaves the event with its confirm."},
  {"severity": "nit", "title": "Working tree holds an uncommitted trace.py hunk in this card's area",
   "evidence": "git diff HEAD -- app/backend/trace.py shows `_human_step` events gaining `**({\"confirm\": e[\"after\"][\"confirm\"]} ...)` at line 244; the HEAD archive trace shows human evidence.events with only action and at (probe output, TRACE-DONE).",
   "why_it_matters": "I reviewed committed HEAD; the committed human step names the confirm in its text, so AC1's wording holds, but the machine-readable confirm in the trace events is not in any commit or test yet.",
   "fix": "Commit it with a test in the T-159 file or drop it.",
   "acceptance_test": "GET /items/{id}/trace human evidence.events[0].confirm equals the /audit event confirm."}
 ],
 "whats_right": ["repeat accept is a true no-op: one event, same confirmed_at, same totals, and it does not survive dismiss or reset (probe and tests agree)", "charge_flag trace step is a code step with pending/pass/skipped states, CONFIRM_FLAG next_action and evidence.values; 7 of 7 trace mutants killed", "the flag sentence names the other charge by its own line (service, amount, date, record) with no internal id and no token"],
 "questions_for_chris": []}
```
