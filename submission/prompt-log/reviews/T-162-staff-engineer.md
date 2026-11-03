# T-162 review (staff-engineer-reviewer), commit 70af4a7

Verdict: **fail**. The card's own e2e spec fails at its commit (0 of 2 pass), and the cause is a corrupted `mountSection` in `app/frontend/review.js` that makes every registered side panel throw. The charges panel does not render at HEAD. The stray block came from 6379c0b (T-154 r2), not from this card's diff, but the card's acceptance evidence ("2/2", "12/12") does not reproduce on the reviewed commit or on HEAD.

Evidence sha: reviewed 70af4a7. HEAD moved to c8022fa during the review; `git diff --stat 70af4a7 c8022fa` shows only `tools/check_index_imports.py`, so the findings hold for HEAD too. Both were run from `git archive` copies in my scratch directory, on my own ports (7891 for HEAD, 7892 for a control copy), and both servers were stopped.

What was checked:
- `tests/e2e/test_rerun_note.py` on archived HEAD: 2 failed (both wait 30 s for `charges-panel [data-item-id="a1"]`).
- `test_charge_confirm.py` plus `test_rerun_note.py` on archived HEAD: 13 failed, 1 passed.
- Root cause: `ZL.hooks.panels` calls throw `ReferenceError: key is not defined` at `review.js:479`. Removing only those four lines (control copy) turns the same two files into 13 passed, 1 failed.
- Mutants on the control copy: dropping the row line in `review.js` or the trace line in `stepper.js` each makes the row/trace assertion fail.
- Dismissed-group probe on the control copy: the dismissed entry's note is in the DOM and invisible while the group is closed; it is visible once the group opens. The dismissed amount's note is visible in the opened Dismissed group, and its trace dialog shows the note.
- `conftest.py` parses at 70af4a7 and HEAD (the acad4f6 fix holds; acad4f6^ fails at line 89).

```json
{"card": "T-162", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 70af4a7 (reviewed): app/frontend/review.js, app/frontend/stepper.js, tests/e2e/test_rerun_note.py, tests/e2e/conftest.py. HEAD c8022fa archived (70af4a7..HEAD changes only tools/check_index_imports.py). Own servers: 127.0.0.1:7891 (archived HEAD) and 127.0.0.1:7892 (archived HEAD with review.js lines 479-482 removed, control). Sample case: case_lib06_lop_billed_vs_adjusted (library fixture, ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated).",
 "exercised": [
  "read personas/staff-engineer.md; python3 tools/board.py show T-162 (AC 1 done, evidence: 'tests/e2e/test_rerun_note.py 2/2 ... test_charge_confirm 12/12 and unit contract 3/3 still pass'); git show 70af4a7 (full diff of 4 files)",
  "git rev-parse HEAD -> c8022fa; git rev-list --count 70af4a7..HEAD -> 1; git diff --stat 70af4a7 HEAD -> tools/check_index_imports.py only",
  "git archive c8022fa | tar -x into <scratchpad>/T162_r1/head; server: PORT=7891 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch>/data/e2e.sqlite3 python -m app.main; lsof listener PID 25517 (verified by ps)",
  "E2E_BASE_URL=http://127.0.0.1:7891 ZLAYT_DB=<scratch>/data/e2e.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_rerun_note.py -v -> 2 failed in 62.58s; both: Locator.scroll_into_view_if_needed timeout waiting for get_by_test_id('charges-panel').locator('[data-item-id=\"a1\"]')",
  "same env, pytest tests/e2e/test_charge_confirm.py tests/e2e/test_rerun_note.py -> 13 failed, 1 passed in 379.61s (test_charge_confirm 1 of 12 passes)",
  "Playwright probe (scratch script) on :7891 for the case: charges-panel count 0; #side-panels children = [flags] only; console and pageerror lists empty; window.ZL.hooks.panels.forEach(fn => fn(c, side)) gives 'ReferenceError: key is not defined ... at mountSection (review.js:479:5)' for all 7 registered panels",
  "cmp of served charges.js, review.js, stepper.js, index.html against archive copies: identical",
  "git log --oneline -S 'if (key === \"a\" && /^(accepted|edited)' -- app/frontend/review.js -> 6379c0b only; git show 6379c0b -- app/frontend/review.js: the 4-line keydown guard was added inside mountSection (hunk @@ -471,6 +471,10 @@)",
  "control copy (git archive c8022fa, review.js lines 479-482 removed, nothing else): tests/e2e/test_rerun_note.py + test_charge_confirm.py on :7892 -> 13 passed, 1 failed (test_the_a_key_on_an_accepted_confirmed_flagged_charge_says_so_and_sends_nothing) in 21.23s",
  "mutant M1 on control: deleted review.js row line 'if (item.rerun_note) root.append(RV.rerunNote(item));' -> test_a_decided_item... FAILED, test_an_item_without_a_note PASSED; file restored (cmp checked)",
  "mutant M2 on control: deleted stepper.js rn insertion (rv().rerunNoteFor) -> test_a FAILED on the trace assertion; file restored (cmp checked)",
  "dismissed probe on control (accepted a1 charge, dismissed entry e1, dismissed amount a2; rerun_note stubbed on all three as the spec does): [data-testid=timeline] [data-item-id=e1] count 1 (spec selector), [data-testid=queue] count 0, [data-testid=dismissed-queue] count 1; rerun-note in DOM 3, e1 note is_visible False while dismissed-group is closed; after opening dismissed-group e1 note visible with text 'Re-run: The re-run gave a different result...'; dismissed-queue e1 buttons: btn-dismiss, btn-reset, btn-source, entry-why, btn-audit, entry-toggle (no btn-trace); after opening dismissed-group-amounts a2 note visible; a2 btn-trace opens #why-modal with rerun-note visible",
  "pytest tests/unit/test_e2e_contract.py -q on archived HEAD -> 3 passed",
  "pytest tests/unit -q on archived HEAD -> 1 failed, 4925 passed, 1 skipped in 382.44s; failure: tests/unit/test_t146_r2_failed_rerun_keeps_items.py::test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial (outside T-162 scope)",
  "git diff -- app/frontend/review.js (working tree, uncommitted, another agent's edits): not evaluated; grep of the working tree finds no stray keydown line in mountSection, so the fix may be in progress but is not committed",
  "grep at 70af4a7: rerunNote used only in review.js:332-333, 367 and stepper.js:472; 0 hits in timeline.js (entry Why dialog)",
  "servers stopped: PIDs 25517 (:7891) and 62877 (:7892), verified with ps and lsof before kill; both ports closed afterwards"
 ],
 "verdict": "fail",
 "scores": {"ac_reproduces_at_commit": 1, "test_strength_dismissed_and_entry": 2, "honest_failure_ui": 2, "backend_to_ui_wiring": 4, "conftest_contract_parse": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Every registered side panel throws at HEAD: a keydown guard was pasted into mountSection (charges panel does not render)",
   "evidence": "app/frontend/review.js:479-482 at 70af4a7 (inside function mountSection, review.js:476): 'if (key === \"a\" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) {' then 'RV.say(...)', 'return;', '}'. 'key' and 'f' are not in scope there. Introduced by 6379c0b (T-154 r2), not by 70af4a7 (git log -S). Repro: git archive c8022fa; run on a port; open #/case/<tok> of case_lib06 after run; document.querySelector('[data-testid=charges-panel]') is null; ZL.hooks.panels.forEach(fn => fn(c, side)) throws 'key is not defined' at review.js:479:5. Spec evidence: test_charge_confirm.py + test_rerun_note.py -> 13 failed, 1 passed (archived HEAD). No error reached the page or the console (pageerror and console lists empty).",
   "why_it_matters": "The charges panel is where a paralegal accepts a charge and sees Accepted charges (charges.js:156-162). At HEAD it does not render, so the must-have charge review is unusable (CONTRACT D.2 blocker). The T-154 r2 guard ('a on a decided item says so and sends nothing') was meant for the keydown handler (review.js:463 at 70af4a7) and is absent there, so the a-key shortcut on an accepted flagged charge is not guarded (test_the_a_key_on_an_accepted_confirmed_flagged_charge fails on the control copy once the panel renders). The failure is silent.",
   "fix": "Delete review.js:479-482 from mountSection. Add the same guard inside the keydown handler beside the dismissed check (review.js:463 at 70af4a7), using that handler's own key and f. Owner: frontend, with the T-154 card; this card's commit cannot be green without it.",
   "acceptance_test": "On a git archive of the fixed commit with E2E_REQUIRE_DB=1: tests/e2e/test_charge_confirm.py 12/12 and tests/e2e/test_rerun_note.py 2/2. Add a spec that fails on any page error during open_case, so a ReferenceError inside a panel cannot pass silently."},
  {"severity": "blocker",
   "title": "T-162 acceptance evidence does not reproduce at the reviewed commit",
   "evidence": "Board AC 1 evidence: 'tests/e2e/test_rerun_note.py 2/2 ... test_charge_confirm 12/12 and unit contract 3/3 still pass'. Reproduced on git archive 70af4a7 / c8022fa: test_rerun_note.py 0/2 (2 failed in 62.58s); test_charge_confirm.py 1/12 (11 failed). Unit contract tests/unit/test_e2e_contract.py 3/3 does pass. The evidence line names no commit sha.",
   "why_it_matters": "The card's only acceptance check is the e2e spec, and it is red on the commit that carries the card. Recording 2/2 without a sha means the claim cannot be audited (feedback_evidence_sha_vs_commit). The card cannot move to done on this evidence.",
   "fix": "Re-run the two specs on a git archive of the commit that will be marked done, record the sha in the AC evidence, and fix finding 1 first. If the 2/2 run used the dirty working tree, say so and drop it.",
   "acceptance_test": "board AC 1 evidence cites the sha, and tests/e2e/test_rerun_note.py passes 2/2 from git archive of that sha with E2E_REQUIRE_DB=1 and E2E_BASE_URL set to a server started from that archive."},
  {"severity": "major",
   "title": "Entry-row assertion passes while the dismissed note is hidden, and it is conditional",
   "evidence": "tests/e2e/test_rerun_note.py:56-58: 'erow = page.locator(f'[data-testid=\"timeline\"] [data-item-id=\"{entry}\"]').first' then 'if erow.count():' then 'expect(erow.get_by_test_id(\"rerun-note\").first).to_contain_text(NOTE)'. Probe on control: that selector matches the dismissed entry inside the closed <details data-testid=\"dismissed-group\"> (dismissed-queue count 1); rerun-note is in the DOM with is_visible False. to_contain_text does not check visibility, so the assertion passes with the note hidden.",
   "why_it_matters": "The AC is 'a decided item with rerun_note shows the note in its row'. A dismissed item is decided, and its note is never proven visible. The 'if erow.count()' branch also turns the check into a no-op if the row is ever absent. The worker's handoff says the dismissed row is 'not asserted'; the code asserts DOM text only, which is weaker than either reading.",
   "fix": "In the test, open the dismissed group first (click [data-testid=dismissed-summary]) and assert the dismissed entry's rerun-note with to_be_visible(). Remove the conditional so a missing row fails. Also add a dismissed amount case: open [data-testid=dismissed-group-amounts] and assert the note on that row is visible.",
   "acceptance_test": "Mutant: add display:none to .rv-rerun-note inside [data-testid=dismissed-queue] (or delete the note line for dismissed rows); the spec must fail. Spec passes on the control copy with the frontend fix in finding 1 applied."},
  {"severity": "minor",
   "title": "Note helpers are defined as a side effect inside RV.controls; the trace guard drops the note silently",
   "evidence": "app/frontend/review.js:332-333 at 70af4a7: 'RV.rerunNote = ...' and 'RV.rerunNoteFor = ...' sit inside the body of RV.controls (review.js:320-). app/frontend/stepper.js:472: 'const rn = rv() && rv().rerunNoteFor ? rv().rerunNoteFor(id) : null; if (rn) n.firstChild.after(rn);' - if RV.controls has not run, the note is dropped without any message.",
   "why_it_matters": "A trace opened before any row controls render loses the note with no error. Today the path is covered because the charge row exists first, but the coupling is hidden and the fallback is silent (the same class as the frontend text-coupling pattern in memory).",
   "fix": "Move RV.rerunNote and RV.rerunNoteFor to module scope before RV.controls, with the same 4-space indentation as the rest of the file, and have stepper.js call them directly.",
   "acceptance_test": "A unit or e2e check that calls the trace path for a decided charge on a fresh page, before any row render, shows rerun-note in #why-modal."},
  {"severity": "minor",
   "title": "Entry rows have no 'How this was checked'; the entry Why dialog does not show the note (product question)",
   "evidence": "Probe on control: buttons in the dismissed entry row are btn-dismiss, btn-reset, btn-save-excerpt, entry-why, btn-source, btn-audit, btn-edit-excerpt, entry-toggle; no btn-trace. grep at 70af4a7: rerunNote appears 0 times in app/frontend/timeline.js (the entry 'entry-why' dialog is timeline.js:241).",
   "why_it_matters": "The card's wording says 'row and trace'. For entries, the trace does not exist, so the note shows only in the row. Whether the entry Why dialog should also carry it is a product call (see questions).",
   "fix": "Decide with Chris (question below). If yes, add the note to the entry Why dialog from timeline.js:241 and add an assertion; if no, say so in the card so the AC matches the product.",
   "acceptance_test": "The AC text names which surfaces show the note for entries, and the spec asserts exactly those."},
  {"severity": "minor",
   "title": "The decided-fixture skip is not governed by E2E_REQUIRE_DB",
   "evidence": "tests/e2e/test_rerun_note.py:19: 'if st not in (200, 201): pytest.skip(\"library cases need ZLAYT_MODE=local\")'. The fixture has no needs_db() guard (conftest.py:145-155), so with E2E_REQUIRE_DB=1 a run against a non-local server reports skipped, not failed.",
   "why_it_matters": "A green-with-skips run can read as a pass on the AC. The rule in conftest is that a skipped DB spec must fail when E2E_REQUIRE_DB=1.",
   "fix": "Use the needs_db() helper (or fail when E2E_REQUIRE_DB=1) in the decided fixture.",
   "acceptance_test": "E2E_REQUIRE_DB=1 against a server started without ZLAYT_MODE=local: the spec errors, it does not skip."},
  {"severity": "minor",
   "title": "Unit suite is red at HEAD in a test outside this card (routing note)",
   "evidence": "pytest tests/unit -q on git archive c8022fa -> 1 failed, 4925 passed, 1 skipped. Failing test: tests/unit/test_t146_r2_failed_rerun_keeps_items.py::test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial (assert {'code': 'run_partial', ...} is None).",
   "why_it_matters": "Not charged to T-162. It is the same rerun area (T-146), so the owner should see it before the gate. The card's review cannot claim a green unit suite at HEAD.",
   "fix": "Route to the T-146 backend owner: either fix the behaviour or update the test with a recorded decision.",
   "acceptance_test": "pytest tests/unit -q green at the fixed commit."}
 ],
 "whats_right": [
  "The backend source is right: present.py:47 maps ladder.rerun_note.message to item rerun_note, and tests/unit/test_t146_r3_decided_items_never_lowered.py:67 asserts it on item_view.",
  "The two-sided check is sound: deleting either the row line (review.js:367) or the trace line (stepper.js:472) makes the note spec fail on the control copy, and the no-note test passes both times.",
  "conftest.py parses at 70af4a7 and HEAD, so the acad4f6 repair holds, and tests/unit/test_e2e_contract.py passes 3/3."],
 "questions_for_chris": [
  "Should a decided entry's note also show in its Why? dialog (timeline.js:241), or is the row enough? Entries have no 'How this was checked' button at HEAD (only charges and flags do)."
 ]}
```
