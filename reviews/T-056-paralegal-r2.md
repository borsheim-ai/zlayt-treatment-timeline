# T-056 round 2 review, paralegal-reviewer (Maria Delgado persona)

Commits under review: e83eb54 (backend r1), d796383 (frontend B1). Round 1 was `reviews/T-056-paralegal.md` (fail: B1, B2, M1, m1).
Verdict: **pass**. All three round-1 blockers and the major are resolved in what I ran. One new minor (the 422 message names the figure as "9", not "9/10").

## What I ran
- `.venv/bin/python -m pytest tests/unit/test_manual_and_split.py tests/unit/test_review_rules.py -q 2>&1 | tail -2` gave `45 passed in 2.14s` (run twice, same result).
- `artifacts/review-evidence/T-056-paralegal-r2-api.py` (output `T-056-paralegal-r2-api.out.txt`): TestClient on a temp app (LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch sqlite, temp library holding a synthetic two-record $310 case). Real routes only.
  - Manual entry on record 5, summary "Pain 9/10." against the quote "Pain 4/10, improving." gives **422 invalid_edit** with and without `confirm_warnings: true`. The letter does not contain "9/10".
  - Control, summary "Pain 4/10, improving.": 201, `review_status: pending`, `entered_by: reviewer`, `entered_by_reviewer: true`, `ai_drafted: false`, date 2026-02-20, provider "Capital PT, visit 8" (from the header). Pending notes line: `- Entry, record 5 (Capital PT, visit 8, February 20, 2026): "Pain 4/10, improving." [entered by reviewer]`. The pending entry is absent from the letter.
  - Split: `POST .../items/e1/not_duplicate {"record_id":"r2"}` gives 200. Before the split the total is $310.00 (a1, r1). After the split, before accepting, the total is still $310.00 and the notes list `- Amount $310 (charge), record 2 (Capital Imaging, March 2, 2026): "Charge: $310."` as pending. After accepting ax2_1 the total is **$620.00**. The rerun (`confirm_rerun: true`) keeps a1 and ax2_1 as accepted, and the total stays $620.00.
- Browser (Playwright, `artifacts/review-evidence/T-056-paralegal-r2-chip.py`, screenshot `T-056-paralegal-r2-chip.png`) against the live demo at http://localhost:7860. I clicked "Use the sample case" and "Analyze". I rewrote the case-view GET response in the browser so entry e5 carries `entered_by_reviewer: true`. The row shows the chip `Entered by reviewer` (one chip, `data-testid="entered-by"`). This checks the render path only. The demo cannot produce a rejected record, so the manual-entry control itself was not driven.
- `grep -rn -i "entered" app/frontend` gives one hit: `app/frontend/review.js:274-276` (`entered_by_reviewer || /reviewer/i.test(entered_by)` appends `<span class="rv-chip rv-selfreport" data-testid="entered-by">Entered by reviewer</span>`). `manual.js` is loaded by `index.html:58`.
- Read: `git show e83eb54` (review.py, amounts.py, export.py, pipeline.py, store.py, present.py), `git show d796383 --stat`, `memory/ORCHESTRATOR_DECISIONS.md` D-034, `tests/unit/test_manual_and_split.py`.
- Grounding probe (python, `grounding.new_tokens`): "Seen February 20, 2026." against the header date passes. "Seen March 6, 2026." and "Charge $310 for the visit." are flagged.
- Model: I ran as claude-haiku-5-5 (the dossier expects claude-opus-5-5; I report what I ran as).

## Round-1 status
- **B1 (label in UI and notes, not before accept): resolved.** Pending notes carry `[entered by reviewer]` (`export.py:497`). The API returns `entered_by`. The chip renders on the entry row (`review.js:274-276`, browser check above).
- **B2 (not-a-duplicate does not move the charge; rerun reattaches it): resolved.** `review.py:313` and `amounts.py:94-117` keep split records out of the cross-record merge and give them `ax<n>_<k>` ids. The probe shows a1 = [r1] and ax2_1 = [r2], total $620.00, and the rows survive the rerun. The unit test `test_duplicate_charge_moves_to_the_split_record_and_survives_rerun` now covers the identical-amount case.
- **Major (override let "Pain 9/10" into the letter): resolved.** D-034 hard 422 at `review.py:66-70`, with no override. The probe shows 422 with `confirm_warnings: true`. The non-numeric 409 path records `reviewer override: JUDGE_UNSUPPORTED` in notes (`export.py:478-479`). Covered by `test_manual_entry_label_in_pending_notes_and_override_is_recorded`, which passes.
- **m1 (test gaps): resolved.** The pending-label and identical-amount tests exist and pass.

## Findings

**m1 minor. The 422 message names the figure as "9", not "9/10".**
Evidence: `artifacts/review-evidence/T-056-paralegal-r2-api.out.txt`: `"message": "The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote."` with `"tokens": ["9"]`. The message is built at `app/backend/review.py:69-70` from bare tokens.
Why it matters: Maria has to know which figure tripped the check. "9" in "Pain 9/10." is ambiguous. The adjuster-facing risk is low, but this is the message she reads before she fixes the entry.
Fix: quote the matched span from the summary (for example "9/10"), not the bare token.
Acceptance test: `manual_entry` with summary "Pain 9/10." and quote "Pain 4/10, improving." raises a ReviewError whose message contains "9/10".

## Not verified in this round (limits, not findings)
- The manual-entry control in `app/frontend/manual.js` was not driven in a browser. The demo cannot produce a rejected record. The label and chip were checked with a rewritten case-view response, so they show the render path only.
- The split's UI rows were not checked in a browser. The split was checked through the HTTP routes.
- Outside my lens: `manual.js` 422/409 wording, and the code-level judge behaviour for non-numeric objections (other than the notes trace).

## What holds
- The D-034 hard 422 holds with and without `confirm_warnings`. The letter never gets a figure the quote lacks.
- Manual entries stay pending until accepted. The pending notes carry the label, and the letter carries no pending text.
- The split-off charge is listed in internal notes before it is accepted. The total moves from $310.00 to $620.00 only after the charge is accepted, and the rerun keeps it.

Ship-bar score (D-015, `scores.verify_quickly`): 4. Each manual entry, its header date and provider, the split charge, and the total can be checked against a record cite in one step. The 422 wording is the one place I had to guess which figure was meant.

```json
{"card": "T-056", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits e83eb54 (backend r1) and d796383 (frontend B1) on top of d548ccd; working tree with other workers' uncommitted edits; sample case evals/golden/sample.txt and synthetic two-record $310 case via temp library; live demo http://localhost:7860 (fixture, demo mode)",
 "exercised": [
  "read personas/paralegal.md in full; read reviews/T-056-paralegal.md (round 1); read memory/ORCHESTRATOR_DECISIONS.md D-034",
  "read .claude/agent-memory/paralegal-reviewer/manual-entry-split-review-patterns.md",
  ".venv/bin/python -m pytest tests/unit/test_manual_and_split.py tests/unit/test_review_rules.py -q 2>&1 | tail -2 -> 45 passed in 2.14s",
  "artifacts/review-evidence/T-056-paralegal-r2-api.py via TestClient on a temp app -> T-056-paralegal-r2-api.out.txt: manual 'Pain 9/10.' vs quote 'Pain 4/10, improving.' -> 422 invalid_edit (also with confirm_warnings true); control 4/10 -> 201 pending, entered_by reviewer, header date 2026-02-20 and provider 'Capital PT, visit 8'; pending notes line carries '[entered by reviewer]'; split of r2 via POST /items/e1/not_duplicate -> 200; total $310.00 before accept, pending notes list the $310 charge for record 2, total $620.00 after accept; rerun keeps a1 and ax2_1 accepted, total $620.00",
  "artifacts/review-evidence/T-056-paralegal-r2-dom.py and T-056-paralegal-r2-chip.py (Playwright, live demo): sample -> Analyze; case-view response rewritten to flag e5 as entered_by_reviewer; one 'Entered by reviewer' chip on the e5 row -> T-056-paralegal-r2-chip.png",
  "grep -rn -i 'entered' app/frontend -> review.js:274-276 only; index.html:58 loads manual.js",
  "git show e83eb54 (review.py, amounts.py, export.py, pipeline.py, store.py, present.py); git show d796383 --stat",
  "grounding.new_tokens probe: header date passes, other dates and $ figures flagged",
  "read app/backend/review.py:62-70, 134, 227-267, 276-313; app/backend/amounts.py:94-117; app/backend/export.py:477-497"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "manual_entry_verbatim_gate": 5, "never_auto_accepted_or_in_letter": 5, "entry_labelling_ui_and_notes": 4, "split_entries_event_rerun": 5, "split_amounts_totals": 5, "override_traceability": 4},
 "findings": [
  {"severity": "minor", "title": "The 422 message names the figure as '9', not '9/10'",
   "evidence": "artifacts/review-evidence/T-056-paralegal-r2-api.out.txt: \"message\": \"The summary has a number, date or dollar figure that is not in the quote: 9. Remove it or change the quote.\", \"tokens\": [\"9\"]; message built from bare tokens at app/backend/review.py:69-70",
   "why_it_matters": "The paralegal needs to know which figure tripped the check before she fixes the entry; a bare '9' from '9/10' is ambiguous. Not a fact-invention issue: the letter stays clean.",
   "fix": "Quote the matched span from the summary (for example '9/10') in the message, not the bare token.",
   "acceptance_test": "manual_entry with summary 'Pain 9/10.' and quote 'Pain 4/10, improving.' raises ReviewError (422, invalid_edit) whose message contains '9/10'."}
 ],
 "whats_right": [
  "D-034 hard 422 holds: 'Pain 9/10.' against 'Pain 4/10, improving.' is refused with and without confirm_warnings; the letter never carries 9/10.",
  "Split moves the duplicate's $310 to ax2_1 for record 2; total is $310.00 while pending (pending charge listed in notes) and $620.00 once accepted; the rerun keeps both.",
  "The manual entry is labelled '[entered by reviewer]' on its pending notes line before accept, and the 'Entered by reviewer' chip renders on the entry row."
 ],
 "questions_for_chris": [
  "The live demo cannot produce a rejected record, so the manual-entry control (manual.js) was not driven end to end. Should the demo or a library case give one rejected record, so the review can drive the control in a browser next round?"
 ]}
```
