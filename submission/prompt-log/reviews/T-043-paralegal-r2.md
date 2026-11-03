# T-043 round 2 review: paralegal-reviewer (Maria Delgado)

Verdict: pass (0 blockers, 0 majors, 1 minor). All five round-1 items are closed in the mock build at 239e2d3. Nothing here was checked against the live API; the card still defers that to T-045.

What I exercised, in short: the 239e2d3 frontend served from a git-archive snapshot on :7868 (killed after), `?api=mock` with the sample case at 1280 px, the charges and flags panels, keyboard a/d on flag and charge cards, the dismiss-with-reason flow, and a 375 px width check. The frontend at HEAD is byte-identical to 239e2d3 for `app/frontend` (`git diff --stat 239e2d3 HEAD -- app/frontend` printed nothing), so this covers current HEAD's frontend too.

Round-1 items, checked:
- Major (ACs ticked done on specs not run): the evidence text is now "verified on mock (Playwright); E2E pending T-045" on every AC row. The card is still `in_review`. Closed, with the minor below.
- Minor (a/d throws focus to the timeline): closed. After `a` on the gap flag, focus moved to the next pending card inside `flags-panel`; after `d` on a flag, the same; after `a` on a charge card, focus stayed in `charges`. Scroll moved by 178 px and 176 px on flags and did not move on the charge.
- Minor ($185 row lacks plan context): closed. Tray text: "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review". No PT total appears.
- Minor (dismiss reason not shown): closed. After dismiss-with-reason "Not relevant", the card shows "Dismissed because: Not relevant" (screenshot 1280-03).
- Minor (needs-review not first in group): closed for flags. Conflicts: [needs_review, verified]; pre-existing: [needs_review, verified]. Charges table order not checked.

New checks this round:
- Four flag groups plus Record warnings render on `?api=mock`: "Treatment gaps (1)", "Conflicts between records (2)", "Pre-existing conditions (2)", "Causation language (1)", "Record warnings (0)".
- Accident-date conflict card shows "Date of accident per intake form: 2026-01-19." and "the tool does not choose between them". The word "resolved" appears only in the pre-existing card f_pre_3, where it quotes record 3 ("low back pain in 2023, resolved"); it is not in the conflict card.
- Charges at load: "Accepted charges: $0", "Detected, not yet accepted: $8,390 (not a total)".
- Console errors: none. 375 px scrollWidth: 375.

Minor left open:
- The AC rows still say `done: true` and still read "proved by tests/e2e/...". That is the wording round 1 asked me to fix, so I am not blocking, but a T-045 reader may take the card as closed. Hold done=false until the live run.

Evidence: `artifacts/review-evidence/T-043-r2-probe.py`, `artifacts/review-evidence/T-043-r2-probe2.py`, and screenshots `artifacts/review-evidence/T-043-r2-1280-01-flags-charges.png`, `T-043-r2-1280-02-after-a-on-flag.png`, `T-043-r2-1280-03-dismissed-with-reason.png`, `T-043-r2-1280-04-after-d-on-flag.png`, `T-043-r2-1280-05-after-a-on-charge.png`, `T-043-r2-375-01-flags.png`.

Not exercised: the live backend on :7860 and the server E2E specs (deferred to T-045 by the card); the post-accept totals ($8,390 to $2,150) in this round; reload persistence; `e` and `r` keys; the charges table ordering.

```json
{"card": "T-043", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 239e2d3 (app/frontend/{charges,flags,index.html,mock_flags.js,review}.js); served from git archive of 239e2d3 at http://127.0.0.1:7868 (killed after); app/frontend identical at HEAD dd545e3; index.html?api=mock, sample case, 1280 and 375 px; live backend not run (E2E deferred to T-045)",
 "exercised": [
  ".venv/bin/python tools/board.py show T-043 (AC 1-7, round-1 notes read)",
  "git diff --stat 239e2d3 HEAD -- app/frontend (empty)",
  "git archive 239e2d3 app/frontend | tar -x -C <scratch>; .venv/bin/python -m http.server 7868 --bind 127.0.0.1 --directory <scratch>/app/frontend (pid 47676, killed)",
  "artifacts/review-evidence/T-043-r2-probe.py (Playwright chromium, 1280 px): flag_headings = ['Flags','Treatment gaps (1)','Conflicts between records (2)','Pre-existing conditions (2)','Causation language (1)','Record warnings (0)']",
  "same probe: state_order_by_type conflict=[needs_review,verified], pre_existing=[needs_review,verified]; rate line 'rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review'; 'Accepted charges: $0'; 'Detected, not yet accepted: $8,390 (not a total)'",
  "same probe: a on f_gap_r6_r7 -> scrollY 2758 -> 2936, activeElement inside [data-testid=flags-panel] on f_plan_4_6, not in queue",
  "same probe: btn-dismiss-reason, fill 'Not relevant', btn-dismiss-confirm on f_plan_4_6 -> data-review=dismissed, card text 'Dismissed because: Not relevant'",
  "artifacts/review-evidence/T-043-r2-probe2.py: accident conflict card text contains 'Date of accident per intake form: 2026-01-19.' and 'the tool does not choose between them'; 'resolved' appears only in f_pre_3 (record 3 quote), verified by a per-card search",
  "probe2: d on f_acc_1 -> scrollY 3629 -> 3805, focus inside flags-panel on f_pre_3; a on charge a1 -> scrollY 5235 unchanged, focus inside [data-panel=charges]",
  "probe2: 375 px scrollWidth 375; console errors none (probe1)",
  "screenshots T-043-r2-1280-01..05 and T-043-r2-375-01-flags.png read; 1280-03 shows 'Dismissed because: Not relevant'"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "flags_visible_and_sourced": 5, "charges_total_integrity": 5, "keyboard_flow": 4, "mobile_375": 5},
 "findings": [
  {"severity": "minor",
   "title": "AC 1-5 still read done:true and 'proved by tests/e2e/...' beside the mock-only evidence",
   "evidence": "board show T-043: AC 1 text '...proved by tests/e2e/test_flags_panel.py', 'done': true, evidence 'verified on mock (Playwright); E2E pending T-045 ...'. AC 2-5 have the same pattern. Card status in_review.",
   "why_it_matters": "The round-1 remedy was to mark AC 1-5 as mock-verified; the evidence now says that, so I am not blocking. But done:true with a 'proved by' clause reads as closed to T-045 and to a later reviewer. The four flag groups and the $185 text come from the mock overlay (app/frontend/mock_flags.js), so the live API shape is still unproven.",
   "fix": "Set done:false on AC 1-5 (or add a status 'mock-verified') until a live run of tests/e2e/test_flags_panel.py, test_charges.py, test_review_matrix.py, test_keyboard_mobile.py and test_source_record.py::test_gap_flag_two_records passes; keep the 'E2E pending T-045' wording.",
   "acceptance_test": "board validate passes; card shows AC 1-5 not done until the live E2E output is attached to the card."}
 ],
 "whats_right": [
  "The accident-date conflict card keeps both dates side by side and says the tool does not choose between them; no 'resolved' or 'correct date' appears in that card.",
  "Charges never add on the client: pending is labelled '(not a total)', the $185 row has no PT total and now carries the 12-planned / discharged-at-visit-9 context, and accepted totals come from the API.",
  "Dismiss with reason shows 'Dismissed because:' on the card, and keyboard a/d keep focus inside the panel the user is working in."
 ],
 "questions_for_chris": ["Should AC 1-5 stay done:false until the T-045 live run, or is mock-verified plus the E2E-pending note enough to close them? I have assumed held open is the stricter reading."]}
```
