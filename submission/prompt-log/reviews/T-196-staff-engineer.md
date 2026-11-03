# T-196 staff-engineer review (doc check, HEAD 3feb096, card commit 9b40445)

Verdict: pass (0 blockers, 0 majors, 1 nit).

The T-179 r2 minor is closed in the doc. `memory/contracts/api.md` at HEAD no longer says a disputed item is "never accepted without the compare on record". The D-066 paragraph (line 382) now says the stamp is a second commit, that a failed stamp takes the accept back and the call fails, that a concurrent reader or a process killed between the two commits can see an accepted disputed item without its stamp, and it points at SCOPE_CUTS row 25 (line 109, post-MVP). Every mechanism the paragraph names matches `app/backend/review.py` and `app/db/db.py` at HEAD. The one gap is in what the take-back covers, not in what the doc says.

Model note: the brief expects claude-sonnet-5-5, but this review was run by claude-haiku-5-5, so the JSON records that id.

## What I ran (read-only; the shared tree was not written)
- `python3 tools/board.py show T-196`: status in_review, AC 1 done, commits [9b40445], rounds 0. Quoted in the card note: "AC 1 checked: ... SCOPE_CUTS row 25; commit 9b40445".
- Read `reviews/T-179-staff-engineer-r2.md`: minor finding 1 (the compared stamp is a compensation, and the api.md sentence "never accepted without the compare on record" is false in the window). Also minor finding 2 (edited take-back untested).
- Read `memory/SCOPE_CUTS.md` line 109: `| 25 | Compare stamp atomic with the accept (T-179 r2 minor) | ... api.md must say "taken back if the stamp fails", not "never". | Move the stamp into DB.apply_review's transaction (app/db); ~0.5 day. | post-MVP |`
- `git show HEAD:memory/contracts/api.md | grep -n "never accepted without"`: no match, exit 1. `git show HEAD:memory/contracts/api.md | grep -c "compare on record"`: 0.
- `git show HEAD:memory/contracts/api.md | awk` over the D-066 block: line 382 reads "**D-066 (T-179): a disputed item is accepted only with her compare.** ... if it cannot be written the accept is taken back (item returns to its earlier status) and the call fails. A concurrent reader, or a process killed between the two commits, can therefore see an accepted disputed item without its stamp (SCOPE_CUTS row 25; making it one transaction is post-MVP)."
- `git show 9b40445 -- memory/contracts/api.md`: one line changed (`-` old sentence, `+` new sentence), commit message "...compare stamp is a second commit taken back on failure, not atomic (SCOPE_CUTS 25)". `git diff --stat 9b40445 HEAD -- memory/contracts/api.md` shows later edits (c27e7f1, 3feb096, T-177 r4) elsewhere in the file; I read the HEAD D-066 paragraph itself, which contains the new text.
- `git diff --stat HEAD -- memory/contracts/api.md app/backend/review.py app/db/db.py`: no output (no working-tree drift from HEAD).
- Claim-to-code check at HEAD (read with `git show HEAD:<path>`):
  - `app/backend/review.py:238-276` `set_review`: code checks (247-252), then `compare_error` (253, refuses before any write), then the charge confirm (255-260). Order matches the paragraph: code checks, COMPARE_REQUIRED, CONFIRM_REQUIRED.
  - `review.py:261` `DB.apply_review` (the accept commit), `:262` `if action == "accept" and compared is True and judge_dispute(item)`, `:264` `_record_compared`, `:266-267` `_take_back` then `raise`. The stamp is written only for a disputed item with `compared: true`; that matches "The statement is stored only when the item was disputed".
  - `review.py:279-283` `_take_back`: map `{"pending": "reset", "dismissed": "dismiss", "edited": "edit"}`, then `DB.apply_review`. Matches "item returns to its earlier status" for those three statuses.
  - `review.py:326-337` `compare_error`: returns None when `compared is True` or `review_status == "accepted"`; otherwise 422 COMPARE_REQUIRED with `reason_code`, `verdict`, `next_action.code` COMPARE_WITH_QUOTE. Matches the paragraph.
  - `review.py:340-349` `_record_compared`: its own `BEGIN` (345) and `COMMIT` (348), updating the latest accept event's `after` with `compared: {at}`. Separate from the accept transaction.
  - `review.py:348-349` and `:354-376` (`apply_review` route): `compared` must be a bool, else `_bad` (422 invalid_edit, `review.py:44-45`). Matches "else 422 invalid_edit". `compared` is read only for accept, dismiss and reset (`:373`); the edit branch goes to `_edit`. Matches "ignored on dismiss, reset and edit".
  - `app/db/db.py:215-233` `apply_review`: `BEGIN` at 227, `COMMIT` at 233, one transaction for the status UPDATE and the event INSERT. The stamp is not inside it. Matches "a second commit after the accept".
  - `app/db/db.py:19` `ACTIONS` maps `edit` to `edited`, which the `_take_back` map relies on.
  - `app/backend/present.py:565`: `audit_view` exposes `compared` in each `events[]` entry in metadata mode, so "GET .../audit events[] carries compared: {at}, also in public mode" holds.
- `git archive HEAD | tar -x -C <scratchpad>/T196`, then from that copy `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q -p no:cacheprovider`: "11 passed in 3.99s". Covers the COMPARE_REQUIRED order and the take-back test at `test_d066_compare_confirm.py:123`.

## Nit (not a spec violation, does not change the verdict)
The take-back map at `review.py:281` has no key for `accepted`. `compare_error` (`review.py:329`) returns None for an already-accepted item, so a re-accept with `compared: true` of an item that a later judge run disputed reaches the stamp at 262-267. If that stamp fails, `_take_back` does nothing, the call returns 500, and the item stays accepted with no stamp. The doc sentence "item returns to its earlier status" is true for that item (it is still accepted), but the doc does not say what happens in this case, and `test_a_failed_compared_stamp_takes_the_accept_back` (line 123) covers pending only. I did not reproduce it: I did not drive a judge rerun that disputes an accepted item, so reachability is from code reading only. Outside the T-196 AC.

## Scores
- The old overclaim is gone and the doc states the second commit, the take-back and SCOPE_CUTS 25.
- The paragraph's mechanisms match review.py, db.py and present.py at HEAD (table above).
- SCOPE_CUTS row 25 exists with matching wording and a cost line.
- Take-back coverage of the cases the doc implies: pending, dismissed and edited mapped in code; accepted not mapped and not tested.

```json
{"card": "T-196", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 3feb096 (card commit 9b40445): memory/contracts/api.md D-066 paragraph line 382; app/backend/review.py (set_review, compare_error, _record_compared, _take_back); app/db/db.py apply_review; app/backend/present.py audit_view; memory/SCOPE_CUTS.md row 25 line 109; tests/unit/test_d066_compare_confirm.py. Doc and unit check; no app URL.",
 "exercised": [
  "python3 tools/board.py show T-196: in_review, AC 1 done, commits [9b40445]",
  "read reviews/T-179-staff-engineer-r2.md findings 1-3 and memory/SCOPE_CUTS.md row 25 (line 109)",
  "git show HEAD:memory/contracts/api.md | grep -n 'never accepted without': no match (exit 1); grep -c 'compare on record': 0",
  "git show HEAD:memory/contracts/api.md D-066 paragraph read in full (line 382): second commit, take-back on failure, concurrent reader or kill window, SCOPE_CUTS row 25, post-MVP",
  "git show 9b40445 -- memory/contracts/api.md: one-line change in the D-066 paragraph; git diff --stat 9b40445 HEAD on api.md shows later T-177 r4 edits outside it",
  "git diff --stat HEAD on api.md, review.py, db.py: no output (no working-tree drift)",
  "git show HEAD:app/backend/review.py read at set_review 238-276, compare_error 326-337, _record_compared 340-349, _take_back 279-283, apply_review route 354-376, judge_dispute 314-323",
  "git show HEAD:app/db/db.py read at apply_review 215-233 (BEGIN 227, COMMIT 233) and ACTIONS line 19",
  "git show HEAD:app/backend/present.py audit_view line 565: compared exposed in events[] metadata",
  "git archive HEAD into the session scratchpad T196; .venv/bin/python -I -m pytest tests/unit/test_d066_compare_confirm.py -q: 11 passed in 3.99s"
 ],
 "verdict": "pass",
 "scores": {"old_overclaim_removed": 5, "doc_matches_review_py": 4, "scope_cuts_25_link": 5, "take_back_coverage_of_doc_cases": 3},
 "findings": [
  {"severity": "nit", "title": "Take-back has no branch for an item already accepted when a re-accept's stamp fails; the doc does not say what happens there",
   "evidence": "app/backend/review.py:281 back = {\"pending\": \"reset\", \"dismissed\": \"dismiss\", \"edited\": \"edit\"}.get(item.get(\"review_status\")) has no accepted key; review.py:329 compare_error returns None when review_status is accepted, so a re-accept with compared:true reaches the stamp at review.py:262-267; a failed stamp then runs _take_back (no-op) and raises. tests/unit/test_d066_compare_confirm.py:123 test_a_failed_compared_stamp_takes_the_accept_back covers pending only. Not reproduced: no judge rerun that disputes an accepted item was driven.",
   "why_it_matters": "api.md:382 says the accept is taken back and the item returns to its earlier status. For an already-accepted item the status is unchanged and the call fails, which the doc does not describe. The sentence is not false as written, and the case is outside the one-sentence T-196 AC.",
   "fix": "Either state in api.md that a failed re-stamp on an already-accepted item leaves the item accepted and the call fails, or add a defined take-back target for accepted and test it.",
   "acceptance_test": "Parametrize test_a_failed_compared_stamp_takes_the_accept_back over pending, dismissed, edited and accepted (accept, then dispute with the _dispute helper, then re-accept with compared:true under a failing _record_compared) and assert the status the doc names."}
 ],
 "whats_right": [
  "api.md at HEAD replaces the 'never accepted without the compare on record' sentence with the second-commit take-back and a pointer to SCOPE_CUTS 25; grep for the old wording returns nothing.",
  "The refusal order (code checks, COMPARE_REQUIRED, confirm), the bool check for compared, the stamp-only-when-disputed rule and the take-back for pending, dismissed and edited all match review.py at HEAD line for line.",
  "SCOPE_CUTS row 25 carries the matching wording (api.md must say taken back, not never) with a cost line and post-MVP; the D-066 unit file passes 11/11 on a HEAD archive."
 ],
 "questions_for_chris": []}
```
