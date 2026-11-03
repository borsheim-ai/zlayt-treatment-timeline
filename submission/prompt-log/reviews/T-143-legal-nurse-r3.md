# T-143 round 3 review (legal-nurse-reviewer)

**Verdict: pass.** No blocker, no major, two minors.

I tested on a `git archive` of 255b001 (scratchpad copy `t143r3`).

**My r2 major is fixed.** I probed `is_administrative` with the exact r2 cases. Every one is now LISTED:
- `Adjustment to C5-6 performed.` and `Adjustment of C4-5 and C5-6.`
- `Date of onset: 01/16/2026.`, `Date of prior surgery: 2019.`, `Date of surgery: 05/02/2026.` and `Date of MRI: 05/29/2026.`
- `Source of history: patient's son.`, `Name of interpreter: Maria L.` and `Account of accident: rear-ended at a red light.`
- `Letter of protection issued; patient states neck pain began after collision.` and `Under letter of protection, patient reports neck pain 5.`
- `Dictated by Dr. Ortiz, cervical strain with radiating pain to arm.` and `Signed: patient reports neck pain improving.`
- `Source: patient report, neck pain 7/10.`, `Fax: patient denies numbness.`, `Splinted.`, and `Date of accident per intake form: 2026-01-19.` (the sample r7 line is now listed).

Still skipped, as they should be: `Date of service: 03/01/2026.`, `Fax: 555-0100.`, `Electronically signed by J. Smith, MD`, `Signed 3/27/2G.`, `Page 2 of 5`, `Adjustment (courtesy discount) -$274.00.`, `Total charges: $4,500.`, `Balance due: $0.00.`, `Letter of protection requested.`, `CPT 97110, 4 units.` and `ED charge: $2,940.`.

**The worker's charge-line deviation.** The relaxation: a line that ends in a currency amount and has a charge cue ignores procedure, body-part and number words.
- Corpus: I scanned 63 shipped text files. 230 sentences are skipped. 13 of them carry a hint kind, and all 13 pass only through this relaxation. All 13 are pure billing labels, for example `MRI charge: $2,150.`, `x-ray charge $180.00;` and `Costo por sesión de terapia física: $400.00.`. None holds a pain score, a patient statement or a hedge.
- The relaxation keeps pain scores, negations, patient statements and mechanisms listed. Examples listed: `Back pain 6/10 charge: $90.`, `Patient denies charge: $90.`, `Collision charge: $100.`, `Concussion without loss of consciousness, charge $2,940.`, and `Cervical range of motion reduced approx. 40%, charge $75.`.
- Residual risk: a single sentence that mixes a recommendation, a plan-of-care count or a performed-procedure date with an amount is skipped. The amounts engine takes the whole record excerpt and the amount. It does not repeat these words as separate items. See finding 1.
- Judgment: safe on the shipped corpus and narrow. It is not safe for mixed one-sentence lines. That is a minor. It is not a blocker, because it needs a charge cue plus a trailing amount and none exists in the corpus.

**List quality (sample and 15 library cases).** The list is useful and small.
- Sample 2 items; lib01 3; lib03 0; lib09 8; lib11 9; lib14 7; lib15 13.
- It surfaces `Pain 5/10.` (lib09 r6), the Spanish chief complaint, `Prognosis: guarded.`, and the lib15 r6 conclusory sentence `The collision of 2026-10-04 caused all of the injuries and treatment described in this letter.`.
- The noise is small and errs toward showing a line, for example `Annual visit.`, `OCR of scanned CMS-1500.`, `Account held under letter of protection.`

**Letter and notes.**
- I accepted everything on six cases and exported them.
- No listed sentence is in the letter, with one correct exception: lib15 r2 `Neck pain 4/10.` is identical to the text the r5 entry quotes. This is the same exception as in r2.
- Some listed sentences appear in the notes because an accepted flag quotes them as its own evidence. Examples: sample r3, sample r7 and lib09 r1. The test exempts exactly that case.

**Tests.**
- `tests/unit/test_uncovered.py`: 133 passed.
- Full `tests/unit` on the 255b001 archive: 1 failed, 3850 passed, 8 skipped.
- The failure is `test_api_routes.py::test_export_equals_golden_when_everything_accepted` (`['e2','e4'] == []`). It fails identically on the parent 4f416a4, so it is not caused by T-143.

```json
{"card": "T-143", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 255b001 (r3): app/backend/uncovered.py, tests/unit/test_uncovered.py; git archive copy in the scratchpad (t143r3); TestClient on LLM_BACKEND=fixture; sample and case_lib01/03/09/11/14/15; evals/library, evals/golden and sample text corpus (63 files)",
 "exercised": ["git archive 255b001; tests/unit/test_uncovered.py (133 passed)", "full tests/unit on the 255b001 archive: 1 failed, 3850 passed, 8 skipped; the one failure test_export_equals_golden_when_everything_accepted fails identically on parent 4f416a4", "is_administrative probe of 60 lines: all r2 major cases (Adjustment to C5-6, Date of onset/surgery/MRI, Source of history, Name of interpreter, LOP with patient statement, Dictated by/Signed with clinical tail) listed; billing, signature, header, stamp lines skipped", "second probe of 17 charge-line mixed sentences (recommended, planned visits, dose, performed date) and for_record splitter check", "corpus scan of 230 skipped sentences across 63 files; 13 skipped through the charge relaxation, all pure billing labels", "TestClient GET case, accept-all, export on the sample and lib01/03/09/11/14/15: listed sentences vs letter and internal notes vs flag-quoted evidence", "amounts.extract_amounts read: it works from the record excerpt, not per sentence", "board.py show T-143, r2 review, personas/legal-nurse.md"],
 "verdict": "pass",
 "scores": {"r2_major_fixed": 5, "recall_of_clinical_sentences": 5, "charge_line_relaxation_safety": 4, "noise_and_billing_exclusion": 4, "letter_notes_isolation": 5, "usefulness_as_nurse_view": 5, "test_strength": 4},
 "findings": [
  {"severity": "minor", "title": "Charge-line relaxation skips a mixed sentence that also carries a recommendation, a plan-of-care count, a dose or a performed-procedure date",
   "evidence": "is_administrative returns True (skipped) for: 'Discharged after 9 of 12 planned visits, total $1,665.', 'Total 9 visits, $1,665.', 'Cervical epidural steroid injection recommended, estimated cost $3,200.', 'Surgery recommended, total $38,500.', 'Surgery performed 05/02/2026, charge: $38,500.', 'Ibuprofen 800 mg, due $12.', 'Rx cyclobenzaprine 10 mg billed $12.', 'Neck pain, charge: $90.', 'Copay $40 each visit, neck pain.'. Cause: uncovered.py is_administrative drops body_part, term and number kinds when _CHARGE_LINE and _CHARGE_CUE match, and _CHARGE_CUE includes generic words (per, each, total, due, paid, balance). amounts.extract_amounts works from the record excerpt and the amount, so the recommendation, the visit count and the dose are not repeated anywhere. The shipped corpus has no such sentence: the 13 relaxed lines are pure labels (MRI charge: $2,150.; Estimated surgical cost $38,500. in lib13 r7 follows a separate 'Recommend microdiscectomy.' sentence). Also a deviation from the round-3 direction, which counted number and diagnosis/procedure as clinical kinds; the worker disclosed it in the handoff.",
   "why_it_matters": "'Recommend injection' (checklist 11), '9 of 12 planned visits' (checklist 15) and a drug dose (checklist 12) can sit in the same sentence as a charge. Skipped without a trace, the list says the record never stated them. This is the original failure mode through a narrow door. I rate it minor because it needs a charge cue and a trailing amount, and nothing in the corpus triggers it.",
   "fix": "Keep the relaxation only for a short label-plus-amount line. Do not relax when the sentence has an action or plan word (recommend*, order*, perform*, plan*, discharg*, estimated, \\d+ of \\d+) or a number-of-visits phrase. Alternatively relax only for the exact shapes '<label> charge|cost|fee: $N.'. Drop the generic cue words (per, each, total, due, balance) from _CHARGE_CUE.",
   "acceptance_test": "Listed: 'Discharged after 9 of 12 planned visits, total $1,665.', 'Cervical epidural steroid injection recommended, estimated cost $3,200.', 'Surgery performed 05/02/2026, charge: $38,500.'. Still skipped: 'MRI charge: $2,150.', 'x-ray charge $180.00;', 'ED charge: $2,940.', 'Total charges: $4,500.'."},
  {"severity": "minor", "title": "Tests do not pin the charge-line relaxation's limits or the full-suite state",
   "evidence": "tests/unit/test_uncovered.py has charge cases only for plain labels (lines 77-78, 113, 174-175, 188). No case lists a charge-cue sentence with a recommendation, a count or a dose. The full tests/unit run on the archive shows 1 failure (test_export_equals_golden_when_everything_accepted), also present on parent 4f416a4. The handoff reports 5 failures in files it does not own, so the suite is not green on HEAD.",
   "why_it_matters": "The relaxation is the one place that sentences can still vanish. Unpinned, a later change can widen it silently.",
   "fix": "Add the finding-1 listed and skipped cases to test_uncovered.py. Route the unrelated golden-export failure to its owner.",
   "acceptance_test": "The finding-1 acceptance cases pass, and a mutant that widens _CHARGE_CUE to any sentence ending in a dollar amount is killed."}
 ],
 "whats_right": ["My r2 major is fixed: Adjustment to C5-6, Date of onset, Source of history and the LOP sentence with a patient statement are all listed, while real billing, signature and header lines are still skipped.", "Whole-line fullmatch plus a no-clinical-kind veto makes the rule predictable; pain scores, negations, patient statements and mechanisms always keep a line listed, even on a charge line.", "The list is short and useful (0 to 13 items per case) and letter and notes isolation holds by sentence across six accepted-everything exports."],
 "questions_for_chris": []}
```
