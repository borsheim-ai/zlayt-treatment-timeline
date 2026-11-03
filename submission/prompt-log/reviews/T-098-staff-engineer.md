# T-098 staff-engineer-reviewer: export gate for human-edited wording (commit e511778)

Verdict: **fail** (1 blocker, 1 major, 2 minor). The card's own AC holds: an accepted, human-edited summary that fails a code check is a gate blocker, GET /export returns 422 with the same list, and gate `ready` equals export allowed. The blocker is adjacent to the AC: AI drafts with a number not in the quote are still accepted and exported with no code check (finding 1). That is outside the card, the handoff lists it as an exclusion, and I have not downgraded it for that reason.

Pinning: I reviewed `git archive 196c985` (HEAD when I started; e511778 and 36a982b are its ancestors). HEAD moved during the review to e7a1987, then to f5ddec8. f5ddec8 contains T-100 (24c18a7, the D-047 follow-up) and the frontend change that removes the 409 dialog. I re-ran the two open items at f5ddec8 (finding 2 closed there; finding 1 still open).

Severity note: the brief expected the D-047 409 leftover to be a major. I kept it as a major. The outcome at the reviewed commit is fail-closed (the export is refused and no invented fact leaves), which is what D.2 uses to separate major from blocker. Finding 1 is a blocker because an invented number reaches the letter.

Counts: `pytest -q tests/unit/test_trace.py tests/unit/test_export.py` gives 88 passed at e511778 and at 196c985. The full `tests/unit` gives 1577 passed, 4 skipped at e511778 and 1600 passed, 4 skipped at 196c985. The card's "1614 passed" comes from a dirty shared tree and does not reproduce from the archives.

Carried hunks (T-094 in trace.py, T-099 contract in api.md): they do not break the suite. The T-094 conflict branch has no test (finding 3). The T-099 API section is documentation only and matches the route.

## Findings

**F1 (blocker). An AI draft with a number not in its quote reaches the export after one accept.** Outside the T-098 AC; found while testing the gate path. Probe at 196c985: code marks the AI wording `needs_review` (reason SUMMARY_TOKEN_NOT_IN_EXCERPT); the human edit of the same wording is refused with 422; accept returns 200; the gate is ready with no blockers; GET /export returns 200 and the letter contains the invented "5/10". Same result when the judge answer is unsupported or disagrees. Code: `app/backend/review.py:70-71` (accept applies no code check), `app/backend/trace.py:399-400` and `:750-751` (the gate only covers human wording), `memory/contracts/api.md:618` ("AI drafts are not covered by this blocker"). D-034 (`memory/ORCHESTRATOR_DECISIONS.md:42`) says a number not in the quote is never saved, with no override; CLAUDE.md non-negotiable 5 says the product may not invent facts. Rated blocker per D.2 (invents a fact that reaches the letter).

**F2 (major, closed at f5ddec8). The D-047 409 "keep my wording" path still existed at the reviewed commit.** `app/backend/review.py:107-108` raises 409 needs_confirm for token warnings; `:161` logs keep_my_wording; `app/frontend/review.js:135` and `app/frontend/manual.js:55` render the button. At 196c985, "on the left" returns 409 without confirm, saves with confirm, accepts, and the gate blocks it (export 422). D-047 says that state must not be reachable. At f5ddec8 (24c18a7 and f5ddec8) the edit returns 422 invalid_edit with and without confirm and there is no keep path. Open question: a hedge added to a quote without one ("Possibly ...") still saves with 200 and no warning.

**F3 (minor). The T-094 trace hunk carried in e511778 has no test.** `app/backend/trace.py:527-540` (the candidate_rule conflict branch) and `trace.py:607` (`_ocr_steps` now runs on every flag; before e511778 it ran only in the AI branch). `grep -rln 'candidate_rule\|paired_by_code' tests/` prints nothing at 196c985, e511778 and f5ddec8. Owned by T-094.

**F4 (minor). The reason filter in the new blocker is untested.** `app/backend/trace.py:435` filters failing steps by `_CODE_CHECK_REASONS`. Mutant M3 (filter removed) leaves 88 passed. A widened blocker would over-block and no test would notice.

## What I exercised

- `git rev-parse HEAD` (196c985641d7...), `git show --stat e511778`, `git show 36a982b` (docs only), `git show --stat 196c985`, `git show --stat 24c18a7 f5ddec8`, `git log --oneline -n 4`.
- `git archive` of e511778, 196c985 and f5ddec8 into the scratchpad; `.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py` on each (88 passed).
- Full `tests/unit` on e511778 and 196c985 (1577 and 1600 passed, 4 skipped).
- Probes, all through the real FastAPI app with the fixture backend and a scratch DB: `artifacts/review-evidence/T-098-staff-engineer-probe1.py` (non-token edit, gate and export), `artifacts/review-evidence/T-098-staff-engineer-probe2.py` (409 path, AI draft), `artifacts/review-evidence/T-098-staff-engineer-probe3-verdicts.py` (judge verdict variants). The AI-draft state comes from the real `generator.verify`; the judge verdict and the DB row were then set in the scratch copy.
- Results: `artifacts/review-evidence/T-098-staff-engineer-results.txt` (196c985) and `artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt` (f5ddec8).
- Mutants on a scratch copy: `artifacts/review-evidence/T-098-staff-engineer-mutants.py` (M1 3 failed, M2 4 failed, M3 88 passed, M4 1 failed).
- Read: `reviews/T-097-ux-designer.md` (B1 case), `memory/ORCHESTRATOR_DECISIONS.md` D-022, D-034, D-044, D-045, D-047, `memory/contracts/api.md` export section, `git show e511778` in full for the four files in scope.
- Grep: `409`, `needs_confirm`, `keep_my_wording`, `btn-keep-wording` across app and tests; `candidate_rule` across tests.
- Not exercised: UX (Why dialog, panel copy), outside my lens; the browser was not driven.

```json
{"card": "T-098", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e511778 (T-098) with 36a982b (D-047 docs); pinned git archive 196c985 (HEAD at review start); re-check of open items at git archive f5ddec8 (live HEAD during review, includes T-100 24c18a7 and frontend f5ddec8); no app URL (FastAPI TestClient, fixture backend, scratch DB); sample case entry e9 and the synthetic probes",
 "exercised": [
  "git rev-parse HEAD -> 196c985641d72aa699e295223fed8961db0b0c2a; git show --stat e511778, 3ecb8b1, 36a982b, 196c985, 24c18a7, f5ddec8",
  "git archive 196c985 | tar -x (scratch t098-head); git archive e511778 (t098-e511778); git archive f5ddec8 (t098-f5ddec8)",
  ".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py -> 88 passed at e511778 and at 196c985 (artifacts/review-evidence/T-098-staff-engineer-results.txt)",
  ".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -> 1577 passed, 4 skipped at e511778; 1600 passed, 4 skipped at 196c985",
  "artifacts/review-evidence/T-098-staff-engineer-probe1.py: edit 'significantly' (no token), accept, gate and export; D-047 candidates 'on the left', 'not', 'possibly' -> 409, 409, 200 at 196c985 and 422, 422, 200 at f5ddec8",
  "artifacts/review-evidence/T-098-staff-engineer-probe2.py: edit 'on the left' without and with confirm_warnings -> 409 then 200; accept 200; gate ready False with SUMMARY_TOKEN_NOT_IN_EXCERPT; GET /export 422 export_blocked; ready == (export 200) True. At f5ddec8: 422 both times",
  "artifacts/review-evidence/T-098-staff-engineer-probe2.py (p3): generator.verify on 'Pain 5/10' over a quote without it -> needs_review, SUMMARY_TOKEN_NOT_IN_EXCERPT; human edit same wording -> 422 invalid_edit; AI accept -> 200; gate ready True, blockers []; export 200 contains 5/10. Same at f5ddec8",
  "artifacts/review-evidence/T-098-staff-engineer-probe3-verdicts.py: judge verdict unsupported and disagrees -> accept 200, export 200 with the invented figure, at 196c985 and f5ddec8",
  "artifacts/review-evidence/T-098-staff-engineer-mutants.py on the 196c985 copy: M1 drop code_check_blockers -> 3 failed; M2 _code_check_gated False -> 4 failed; M3 drop reason filter -> 88 passed (survives); M4 blocks_export not set -> 1 failed; restored -> 88 passed",
  "read reviews/T-097-ux-designer.md (B1 and walk2 evidence); memory/ORCHESTRATOR_DECISIONS.md lines 30, 42, 53, 55; memory/contracts/api.md line 618; app/backend/review.py 59-175, app/backend/trace.py 390-441 and 527-607, app/backend/generator.py 71-100, app/frontend/review.js 125-137, app/frontend/manual.js 45-56",
  "grep -rn '409\\|keep my wording\\|needs_confirm\\|keep_my_wording\\|btn-keep-wording' app tests memory/contracts (at 196c985 and f5ddec8); grep -rln 'candidate_rule\\|paired_by_code' tests (empty at 196c985, e511778, f5ddec8)",
  "git show e511778 -- app/backend/trace.py app/backend/grounding.py tests/unit/test_trace.py tests/unit/test_export.py memory/contracts/api.md (full diff read)"],
 "verdict": "fail",
 "scores": {"gate_export_agreement": 4, "human_wording_code_check_gate": 4, "ai_draft_path": 1, "d047_followup": 2, "test_pins_behaviour": 3},
 "findings": [
  {"severity": "blocker", "title": "An AI draft with a number not in its quote reaches the export after one accept (outside the T-098 AC, found on the gate path)",
   "evidence": "artifacts/review-evidence/T-098-staff-engineer-results.txt (probe2 p3 at 196c985): 'P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: [SUMMARY_TOKEN_NOT_IN_EXCERPT]', 'P3 human edit with same wording -> (422, invalid_edit)', 'P3 accept AI draft -> 200', 'P3 gate ready True | blockers []', 'P3 export 200 | letter contains invented 5/10: True'. Same with judge verdict unsupported or disagrees (probe3 block) and at f5ddec8 (artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt). Code: app/backend/review.py:70-71 (accept applies no code check); app/backend/trace.py:399-400 and 750-751 (gate covers only human wording); memory/contracts/api.md:618 'AI drafts are not covered by this blocker'; memory/ORCHESTRATOR_DECISIONS.md:42 (D-034: a number not in the quote is never saved, no override).",
   "why_it_matters": "D-034 names this failure ('Pain 9/10' against a 4/10 quote reached the letter). The paralegal typing the same number is refused with 422, but an AI draft with it is saved as needs_review and one accept sends it to the letter; a judge objection does not stop it. CLAUDE.md non-negotiable 5 (no invented facts) is violated on the export path. Rated blocker per D.2 (invents a fact that reaches the letter). The card's AC covers human wording only and the handoff lists AI drafts as an exclusion; that is not a reason to downgrade.",
   "fix": "Decide and record the rule for AI drafts whose D-034 tokens (numbers, dates, dollar figures, left/right/no/not/without) fail the code check: either the generator refuses the draft as it refuses GROUNDING_* failures (app/backend/generator.py:71 verify, REJECTED_CODES in app/backend/confidence.py), or accept returns 422 with EDIT_SUMMARY and the gate lists it as a blocker. Apply the same rule whatever the judge says.",
   "acceptance_test": "Unit: generator.verify on 'Pain 5/10' over an excerpt without 5/10 must not yield a state that accept can send to the export; accept returns 422 or GET /export returns 422. Run with judge verdicts supported, unsupported and disagrees; the export never contains '5/10'. Mutation: removing the new check makes the test fail."},
  {"severity": "major", "title": "D-047 409 keep-my-wording path still existed at the reviewed commit (T-098 follow-up; closed at f5ddec8 by T-100 24c18a7 and frontend f5ddec8)",
   "evidence": "app/backend/review.py:107-108 (raise ReviewError 409 needs_confirm for token warnings), :161 (keep_my_wording event), app/frontend/review.js:135 and app/frontend/manual.js:55 (btn-keep-wording). At 196c985, artifacts/review-evidence/T-098-staff-engineer-results.txt (probe2 P1): 'on the left no confirm -> (409, needs_confirm)', 'confirm_warnings=true -> (200, None)', 'accept -> 200', 'gate ready False | blockers [(e9, SUMMARY_TOKEN_NOT_IN_EXCERPT)]', 'export 422 export_blocked'. At f5ddec8 (artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt): 'on the left' -> (422, invalid_edit) with and without confirm; 'not' -> 422.",
   "why_it_matters": "D-047 says the 409 path is removed so that no item can be confirmed into an unexportable state. At the reviewed commit a paralegal could confirm one: it saved, accepted, and the gate then refused the export. The outcome is fail-closed and no invented fact leaves, so I rate major (the brief's default), not blocker. Closed at f5ddec8.",
   "fix": "Already done in 24c18a7 and f5ddec8. Keep the regression: side, negation and qualifier tokens refused with 422 at edit and manual entry, with no keep path in the API or the UI.",
   "acceptance_test": "E2E and unit: edit 'Neck pain ... on the left.' with and without confirm_warnings returns 422 invalid_edit, the item is unchanged, and no btn-keep-wording exists in the DOM. Mutation: restoring the 409 branch in review.py:107-108 makes the test fail."},
  {"severity": "minor", "title": "The T-094 trace hunk carried in e511778 has no test and no card review",
   "evidence": "app/backend/trace.py:527-540 (candidate_rule conflict branch: paired_by_code, spans_match, judge_conflict) and app/backend/trace.py:607 (_ocr_steps now on every flag; in e511778 it moved out of the AI-only branch). 'grep -rln candidate_rule\\|paired_by_code tests' prints nothing at 196c985, e511778 and f5ddec8.",
   "why_it_matters": "The brief asked whether the carried hunks break anything. The suite passes (88 at e511778 and 196c985), but no test runs the new code-origin conflict branch, and the OCR-step move changes what lexicon-only flags show. Behaviour owned by T-094 is untested.",
   "fix": "T-094 adds its own tests and goes through its own review before it closes, or the hunk is split out of the T-098 commit.",
   "acceptance_test": "tests/unit/test_trace.py: a conflict with candidate_rule plan_vs_outcome gives paired_by_code pass, spans_match pass (verbatim) or fail (not verbatim), and a judge_conflict step; a lexicon-only flag on an OCR record shows the OCR step. Mutation: deleting the trace.py:527 branch makes the test fail."},
  {"severity": "minor", "title": "The reason filter in the new blocker is untested",
   "evidence": "app/backend/trace.py:435 (fails = steps with reason_code in _CODE_CHECK_REASONS). Mutant with the filter removed: 88 passed (artifacts/review-evidence/T-098-staff-engineer-results.txt, M3).",
   "why_it_matters": "A widened blocker would block on any failing code step of a paralegal entry (over-blocking) and no test would notice. It does not under-block, so minor.",
   "fix": "Add a test: an accepted paralegal entry with a failing non-summary code step is not listed as a code-check blocker (or state the intended behaviour and test it).",
   "acceptance_test": "Mutant M3 makes the new test fail."}
 ],
 "whats_right": [
  "Gate and export share one list: at 196c985 a refused edit gives gate ready False and GET /export 422 with the identical blocker; ready == (export 200) held in every probed state (probe2 P1 and probe1 P1 in the results file).",
  "The blocker is pinned by tests: removing the call from export_blockers (M1) fails 3 tests, the gating predicate (M2) fails 4, and the blocks_export flag (M4) fails 1.",
  "The T-097 B1 case now gates: the test test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 passes, and the item trace names summary_qualifier with an EDIT_SUMMARY action."],
 "questions_for_chris": [
  "F1: should an AI draft whose number, date or dollar figure is not in its quote be refused at generation or at accept (D-034 says never saved), or may the paralegal accept it? D-022 says needs_review for qualifiers; the numeric case is the open question.",
  "D-047: does a hedge added to a quote without one ('Possibly ...') count as a qualifier token? At f5ddec8 it saves with 200 and no warning.",
  "T-100 made judge objections on a human-written edit non-blocking (saved as needs_review). D-045(b) exempts human wording from the judge. Confirm this is intended."]}
```
