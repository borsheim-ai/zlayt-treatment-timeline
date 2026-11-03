# T-139 — claims-adjuster-reviewer (BI adjuster / defense adversary), round 0

**Verdict: fail** (2 blockers, 1 major, 1 minor, 1 nit).

Scope: HEAD `ba82071` (card commits 5f7ef96, 184cbb7, ba82071). I ran `git archive HEAD` into the session scratchpad (`t139tree/`) and started the app on spare port 7874
with `ZLAYT_MODE=local LLM_BACKEND=fixture` and a scratch `ZLAYT_DB`. `/api/health` returned `"backend":"fixture","demo_mode":true`.

**The committed tree cannot run a case.** The sample, lib01 (both runs) and lib03 each ended `status failed`, `entries: 0`, and export returned 422 RUN_FAILED.
I reproduced the run in-process to get the traceback: `generator.py:169 e["why"] = why.join(...)` raised `AttributeError: module 'app.backend.why' has no attribute 'join'`.
`git show HEAD:app/backend/why.py | grep "def join"` finds nothing. The function exists only in the uncommitted working copy (`app/backend/why.py:62`, git status `M`).
On HEAD the card's own tests (`test_t139_narrow.py`, `test_t139_charge_text.py`, `test_t139_letter_eval.py`) give `17 failed, 44 passed, 9 errors`, and `python -m evals.letter_check` crashes with the same AttributeError.
The card's evidence was produced on a dirty working tree.

**To still answer the brief**, I built a second tree: HEAD plus only the working-copy `why.py` (sha1 92d540a…, identical to the worktree file). I ran the same server on 7874 against it
and repeated the brief on the sample, lib01 and lib03 (accept every item, dismiss the lib01 $3,915 ED charge on a second lib01 run, export default/oneline/standard).
I added lib11 (plaintiff-firm check) and lib10/lib14 (claim forms). Every finding below about letter content comes from that overlay tree, so it shows the T-139 logic as the worker meant it to ship.
Server PIDs 51517 (HEAD) and 57748 (overlay) were stopped with kill. Afterwards `lsof -iTCP:7874 -sTCP:LISTEN` returned nothing and curl exited 7.

Answers to the three questions:
1. **Rates, estimates or dismissed amounts outside the total and accepted-charge lines.** On sample, lib01 and lib03: none. `$140`, `$120` and `$185` are gone. Each letter's only `$` lines are the accepted charges, their source quotes and the R-EX-8 total.
   The lib01 letter with the dismissed charge has 0 `$` and keeps the ED clinical entry. **But on CMS-1500 claim forms (lib10, lib14) charge and paid figures written without `$` reach the treatment chronology.**
   Examples: "total charge 49100; amount paid 0 00" and "24F 25500 … Item 28 TOTAL CHARGE 33000". letter_check still scores this 0 because it uses the same detector it is meant to audit.
2. **"Bills to request".** It no longer names the dismissed provider: lib01 now lists "Dunmarrow Fire-Rescue run report; Plumtree Physical Therapy (itemized ledger)". **It still names the plaintiff's own firm on lib11:** "Dr. Hesper Alderton; Ashgrove Fire-Rescue run report; Pellingham and Rook PLLC."
3. **Held-out entries.** Partly explained. The tray, the notes and the 422 response all say why the entry is held. But the stated remedy "or edit the summary to remove it" is refused by the server. A quote-only change is refused too. Only a combined quote+summary edit goes through, and it leaves a hollow "Itemized ledger, statement date 06/15/2026." line in the treatment chronology.
   Nothing tells her the bill's charges are already in BILLED CHARGES, so she could simply dismiss the entry.

Deterministic checks run first: the T-139 pytest files and `evals.letter_check` on HEAD (both broken, above). On the overlay, `evals.letter_check` returned `{"value": 0, "cases": 25, "held_out_entries": 9}`.
I also ran a currency-recall sweep over the evals input text (`artifacts/review-evidence/t139_adjuster/currency_sweep.txt`).

```json
{"card": "T-139", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD ba82071 (commits 5f7ef96, 184cbb7, ba82071) via git archive into session scratchpad; second tree = HEAD + working-copy app/backend/why.py only; app at http://127.0.0.1:7874 (fixture backend, ZLAYT_MODE=local, scratch ZLAYT_DB); sample, case_lib01_er_only_then_gap (x2, one with $3,915 dismissed), case_lib03_truck_rear_end_chiro, plus case_lib11_priors_and_ledger, case_lib10_eob_ub04_cms1500, case_lib14_handwritten_chiro_scans",
 "exercised": [
  "python3 tools/board.py show T-139; git log --oneline -5; git status --short; read reviews/GATE-M2-claims-adjuster.md and personas/claims-adjuster.md",
  "git archive HEAD into scratchpad t139tree; started app (PORT 7874, LLM_BACKEND=fixture, ZLAYT_MODE=local); GET /api/health",
  "artifacts/review-evidence/t139_adjuster_probe.py on HEAD: sample, lib01, lib01 with a1 dismissed, lib03 -> every run status failed, entries 0, export 422 RUN_FAILED",
  "artifacts/review-evidence/t139_adjuster_trace.py (TestClient, in-process) on HEAD lib01 and sample -> AttributeError why.join at generator.py:169 (saved head_ba82071_sample_run_traceback.txt)",
  "git show HEAD:app/backend/why.py | grep 'def join' (no match) vs worktree app/backend/why.py:62; git show 184cbb7 -- app/backend/generator.py (hunk swapping why.why for why.join)",
  "HEAD: pytest tests/unit/test_t139_narrow.py test_t139_charge_text.py test_t139_letter_eval.py -> 17 failed, 44 passed, 9 errors; python -m evals.letter_check -> AttributeError",
  "Overlay tree (HEAD + worktree why.py): restarted on 7874; probe on sample (9 entries/4 amounts/11 flags), lib01, lib01 dismissing the $3,915 charge a1, lib03, lib11, lib10, lib14: accepted every item one by one, exported default/oneline/standard",
  "grep of every letter for '$', 'per visit', '/visit', '140', '120', 'estimat', 'cost', '3,915' outside BILLED CHARGES / Source / total lines",
  "Read BILLS TO REQUEST, RECORDS NOT IN THE TREATMENT SECTION and PENDING ITEMS in each internal_notes_text",
  "lib11 e9 fix attempts via /items/e9/review: summary-only edit (422), quote-only edit (422), quote+summary edit (200) -> probe_lib11_e9_fix.txt",
  "Listed ladder.excerpt_narrowed dropped sentences per case (narrowed_dropped.txt)",
  "artifacts/review-evidence/t139_adjuster_currency_sweep.py: 20 hand variants + all evals/library and golden input sentences with a money word and a digit",
  "Overlay: python -m evals.letter_check -> value 0, cases 25, held_out_entries 9",
  "Stopped server PIDs 51517 and 57748 with kill; lsof on 7874 empty, curl exit 7"
 ],
 "verdict": "fail",
 "scores": {"no_invented_facts": 4, "weaknesses_surfaced": 4, "billing_accuracy": 3, "letter_neutrality": 2, "source_cites": 5},
 "findings": [
  {"severity": "blocker",
   "title": "The committed card cannot run any case: generator calls why.join, which exists only in the uncommitted working copy",
   "evidence": "HEAD ba82071, git archive: sample/lib01/lib03 runs -> status failed, entries 0, export 422 RUN_FAILED. Traceback: 'app/backend/generator.py, line 169, in compose: e[\"why\"] = why.join(reasons, lad.get(\"judge\")) ... AttributeError: module app.backend.why has no attribute join' (artifacts/review-evidence/t139_adjuster/head_ba82071_sample_run_traceback.txt). `git show HEAD:app/backend/why.py | grep -n 'def join'` -> no output; worktree app/backend/why.py:62 'def join(reasons, judge=None)' (git status ' M app/backend/why.py'). HEAD T-139 tests: '17 failed, 44 passed, 9 errors' (head_ba82071_t139_pytest.txt). HEAD evals.letter_check -> same AttributeError.",
   "why_it_matters": "What is committed produces no chronology and no letter, so nothing reaches my desk. The AC evidence ('3887 pass', 'letter_check 0 over 25 cases') could not have come from this commit. It came from a working tree that includes another card's unstaged edits.",
   "fix": "Commit the why.join/why(code, judge) change together with the generator hunk that needs it, or revert that hunk out of 184cbb7. Then re-run the T-139 tests and letter_check from a clean `git archive HEAD`.",
   "acceptance_test": "From `git archive HEAD` in an empty dir: the three tests/unit/test_t139_*.py files pass; POST /api/cases {sample:true} + /run reaches status ready with 9 entries; `python -m evals.letter_check` exits with value 0 and no traceback."},
  {"severity": "blocker",
   "title": "Claim-form charge and paid figures without '$' reach the treatment chronology (lib10, lib14); letter_check is blind to them",
   "evidence": "Overlay tree, all items accepted. lib10_letter_text.txt:32-33: 'Claim lists CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units; total charge 49100; amount paid 0 00.' / Source: '... Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00.' lib14_letter_text.txt:24-25: '... CPT 98941, 24F 25500, 24G 3. Line 2: ... CPT 97014, 24F 7500, 24G 3. Item 28 total charge 33000.' lib10_letter_oneline.txt:10 carries the same quote. currency_sweep.txt: MISS for 'Charge per visit: 140.00', 'Charges: 3,915.00', 'Cost estimate 4,500', 'Fee 140/visit'; corpus misses include 'Item 28 TOTAL CHARGE 49100.' and 'Item 29 AMOUNT PAID 0 00.' evals/letter_check.py:39-45 audits with charge_text.currency_strings, the detector under test; it reports value 0 over 25 cases including lib10/lib14.",
   "why_it_matters": "AC1 says no dollar amount appears in the letter except the total (and accepted charge) lines. The carrier letter now prints a charge total the BILLED CHARGES section leaves out ($491.00 for Wardlaw) and an 'amount paid 0' figure. I will use that to argue the specials are inconsistent, and to open paid-versus-incurred. This is the same defect class as the GATE-M2 blocker (amounts reach the letter through entry quotes), on a record type the fix did not cover. The eval meant to guard it uses the same detector it is checking, so it cannot catch this.",
   "fix": "Hold out (or narrow) any entry whose quote or summary has a money field even without '$': CMS-1500 24F / Item 28 TOTAL CHARGE / Item 29 AMOUNT PAID / Item 30, UB-04 FL47, and a money word (charge|charges|fee|cost|paid|balance|billed|rate|estimate) followed by a number. Make letter_check use a detector independent of charge_text, for example money word + digit in the chronology section.",
   "acceptance_test": "lib10 and lib14 with every item accepted: the letter_text chronology contains none of 'TOTAL CHARGE', 'AMOUNT PAID', '24F', '49100', '33000'; letter_check fails on the current lib10/lib14 letters (mutation test) and passes after the fix; unit cases for 'Charges: 3,915.00' and 'Charge per visit: 140.00'."},
  {"severity": "major",
   "title": "'Bills to request' still lists the plaintiff's own law firm (lib11)",
   "evidence": "Overlay lib11_internal_notes_text.txt:35-36: 'BILLS TO REQUEST (entry in the letter, no accepted charge)' / '- Dr. Hesper Alderton; Ashgrove Fire-Rescue run report; Pellingham and Rook PLLC.' Record 4 source 'Pellingham and Rook PLLC, correspondence (letter of protection)': 'This firm represents the client...'. Card note 2026-11-02T13:03:01Z (orchestrator): \"'Bills to request' must not list the plaintiff's own law firm (lib11); only treating providers/facilities.\" export.py _bills (HEAD) excludes paid and dismissed providers only.",
   "why_it_matters": "This was added to this card's scope and it is not done. A request list that includes the firm itself makes the work product look unchecked. The carrier does not see it because it is internal, so this is not a blocker.",
   "fix": "_bills lists only providers whose entry is clinical (exclude correspondence/LOP/attorney sources, e.g. by record kind or a closed source pattern list); add the lib11 test.",
   "acceptance_test": "UT/E2E lib11 all accepted: BILLS TO REQUEST line does not contain 'Pellingham' or 'PLLC'; lists Dr. Hesper Alderton and Ashgrove Fire-Rescue."},
  {"severity": "minor",
   "title": "Held-out billing-statement entries: the stated remedy 'or edit the summary' is refused, and the clean path (dismiss; charges already in BILLED CHARGES) is not offered",
   "evidence": "why.py:10 (HEAD): '...held out of the letter until you pick a quote without the amount (or edit the summary to remove it).' export.py:539 (HEAD) notes: 'states a dollar amount, not exported (pick a quote that does not state it, or edit the summary)'. probe_lib11_e9_fix.txt: summary-only edit -> 422 'The quote states a dollar amount ($250.00, $180.00, $2,310.00, $2,740.00)...'; quote-only edit -> 422 SUMMARY_NUMBER_NOT_IN_EXCERPT; quote+summary 'Itemized ledger, statement date 06/15/2026.' -> 200. lib11 BILLED CHARGES already lists $250.00, $180.00, $2,310.00 from the same record 9.",
   "why_it_matters": "The paralegal follows the text she is given, and it fails. The only edit that works puts a contentless 'Itemized ledger' line in the treatment chronology, which reads as padding to me. The record's charges are already in the bill section, so the right move is to dismiss the entry. The tool never says so.",
   "fix": "For a held-out entry whose record's amounts are all charges/totals, say: 'This record is a bill; its charges are listed under Billed charges. Dismiss this entry unless it states treatment.' Change '(or edit the summary)' to 'and edit the summary' when the quote states the amount.",
   "acceptance_test": "lib11 e9 why/notes text names the BILLED CHARGES lines and offers dismiss; no remedy text is offered that the server then 422s (UT: apply each suggested remedy alone and assert 200)."},
  {"severity": "nit",
   "title": "CHARGE_TEXT_IN_ENTRY 422 detail lists every amount twice",
   "evidence": "lib11 e9 accept 422 detail.amounts: ['$250.00', '$180.00', '$2,310.00', '$2,740.00', '$250.00', '$180.00', '$2,310.00', '$2,740.00']; lib14 e8 the same pattern ('$1,380.00', '$21.50', '$187.05', '$1,567.05' x2).",
   "why_it_matters": "Cosmetic; a UI that renders the list shows each figure twice.",
   "fix": "De-duplicate excerpt+summary amounts in review.charge_text_error.",
   "acceptance_test": "UT: detail.amounts has no repeats."}
 ],
 "whats_right": [
  "Sample, lib01 and lib03 letters no longer print $185, $140 or $120 or 'per visit'; the only '$' lines are the accepted charges, their source quotes and the R-EX-8 total ($8,390.00 / $3,915.00 / $7,500.00).",
  "Dismissing lib01's $3,915 removes the figure from the whole letter (0 '$'), keeps the ED clinical entry, and drops Marrowgate General ED from Bills to request.",
  "Narrowing drops only the money sentence(s): 'Plan of care: 8/12 visits', 'Radiology: findings likely chronic' and 'This is not a bill.' survive (narrowed_dropped.txt)."
 ],
 "questions_for_chris": []}
```
