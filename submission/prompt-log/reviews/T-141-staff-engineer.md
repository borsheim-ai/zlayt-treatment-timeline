# T-141 staff-engineer review (c4bb4da), Marcus Lee persona, with the paralegal view

Verdict: **changes** (0 blockers, 2 major, 3 minor, 1 nit). The target works: on lib11 (fixture backend, ZLAYT_MODE=local) the app shows two conflict cards, "Prior accidents? Yes [ ] No [X]." and "Prior injuries? Yes [ ] No IX]." against the PCP's "car accidents in 2019 and 2022", and no accident-date conflict. All 3600 unit tests pass on the commit archive. The two majors are about what the new code can hide: the accident-date skip can drop a true date conflict (five of six plausible variants), and the new `checks` field says the same thing on every case, including Spanish cases where the pair rules cannot fire.

## Answers to the five questions
1. **Intake denials.** 25 pairs, pre vs HEAD. New and correct: checked No [X], OCR No IX], reversed box order, "Prior accidents: No.", "Prior injuries: None." pair with accident sentences; Yes checked, both boxes empty, both boxes checked, a bare question, an accident in the denial's own year, a husband's or other driver's accident do not pair. Wrong pairs (minor finding 3): a topic-free stem ("Previous employer: None.", "Prior authorization ... No [X]", "Previous visits to this clinic: None.") pairs with any prior-condition sentence; a negated history ("No car accidents in 2019 or 2022") counts as a prior event; a scoped question ("in the last year") pairs with a 2019 accident. "No prior accidents since 2010" vs a 2005 accident pairs on both builds (inherited from T-094). The roommate pair reaches the judge on purpose (J3V20). One live J3 run rejected every wrong pair I tried and confirmed the lib11 pair, so the judge held; no control covers these shapes.
2. **Accident-date skip.** It can hide a true conflict (major finding 1): five variants flagged before the commit return nothing now.
3. **Controls.** Labels were fixed in the same commit, before any run, with a rationale per row and a locked table in the test; the reachability test passes. The live 3x run is not required to accept this card (AC 1 does not ask for it and "controls unaffected" is verified by the 27-packet diff), but it is required before the M2 gate (D-046) and nobody owns it (minor finding 4).
4. **lib11 expected.** Three additive edits, each with a written reason: C1 summary suffix (nit), N2 must_not (false accident-date conflict; red on the old code, green on HEAD), T1 tolerated (second form field against the problem-list sentence). Nothing was loosened.
5. **checks.conflict_types.** Present and correct for English; the four types match the code paths and the not_checked list is honest about what is absent. It is a constant, so it overclaims for Spanish and skipped stages (major finding 2).

## Paralegal view (lib11 in the app, Maria's reading)
- The conflict is easy to see: "Conflicts between records (2)" with each card quoting the intake form line with the answer ("Prior accidents? Yes [ ] No [X].") next to the PCP line, record numbers and dates, "Open records 6 and 1". No "records disagree" accident-date card, no "No conflicts found" text.
- The OCR quote "No IX]" is shown as scanned; a paralegal can read it, but it is the one line that asks for a second look.
- Two cards cite the same PCP sentence, and two label-only "mentions a prior or pre-existing condition: Prior accidents?" flags remain (minor finding 6).
- The `checks` list is not shown in the UI yet (T-142 in progress), so the empty-state wording was not testable here.
- Still wrong on lib11 and outside this card: the ledger total and balance due count as charges (M1 in the library report); not counted against T-141.

Server stopped by PID 82002. Evidence and scripts: `artifacts/review-evidence/T-141/`.

```json
{
 "card": "T-141",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git c4bb4da (and c4bb4da~1 for differential); app from a git archive copy, http://127.0.0.1:7921 (PID 82002, stopped), fixture backend, ZLAYT_MODE=local; lib11 (evals/library/case_lib11_priors_and_ledger.txt) as the paralegal view; sample case not exercised in the UI",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/GATE-M2-paralegal.md, `python3 tools/board.py show T-141`, D-046/D-053/D-057 in memory/ORCHESTRATOR_DECISIONS.md, git show c4bb4da in full (conflict_candidates.py, conflicts.py, j3_controls.py, judge_controls.jsonl, expected.json, tests)",
  "git archive c4bb4da and c4bb4da~1 into separate scratchpad directories (T141_head, T141_pre); all probes ran on those, never on the working tree",
  "Conflict suites on the HEAD archive: pytest tests/unit/test_conflict_candidates.py test_conflicts.py test_t093_j3_controls_reachable.py -> 116 passed; full pytest tests/unit -> 3600 passed, 8 skipped, 0 failed (the unit failures the brief mentions are from the dirty working tree, not the commit)",
  "25 intake/history candidate probes on both archives (probe1.py), 12 accident-date scenarios on both archives (probe2.py), Spanish probe (probe3.py), candidates + accident-date diff over all 27 golden and library packets pre vs HEAD (diff_packets.py: only lib11 changes)",
  "11 mutants on a scratch copy (mutate.py): 9 killed; survivors M4 (guard in _earlier_year_accident, covered by callers) and M9 (len(distinct)<2 inside the skip, equivalent because two distinct dates take the other branch)",
  "evals.library_report on c4bb4da~1, c4bb4da, and c4bb4da~1 with the new expected file: lib11 must flags 3/4 -> 4/4; must_not_flag hits for the new N2: 1 on the old code, 0 on HEAD (N2 discriminates); remaining M1 hit (ledger charges) is the separate GATE-M2 blocker",
  "Live J3 (claude-cli, ENABLE_LIVE=1, one run each, exploratory): 6 false pairs benign, real lib11 pair conflict (live_j3.py)",
  "App from the HEAD archive: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, port 7921, listener PID 82002 verified by lsof and ps before kill; stopped by PID (lsof empty, curl 000); port 7860 (PID 66274) untouched. Loaded lib11 from the synthetic library by Playwright (ui_lib11.py), read the full page text, screenshotted the conflict cards, fetched GET case JSON (case.json), POSTed the Spanish library packet and read its checks",
  "Read memory/contracts/api.md:133 and checked checks.conflict_types, labels and not_checked against code; checked the latest controls report for the new ids"
 ],
 "verdict": "changes",
 "scores": {
  "determinism": 5,
  "honest_failure": 3,
  "tests_assert_behaviour": 4,
  "llm_code_boundary": 4,
  "controls_discipline": 4
 },
 "findings": [
  {
   "severity": "major",
   "title": "Accident-date corroboration skip silently drops a true date conflict when the earliest record words the collision in a way its word list misses",
   "evidence": "app/backend/conflicts.py:14-15 (_EVENT, _HISTORICAL), :19-28 (_describes_event: a sentence counts only if it has no prior/history word and no 4-digit year earlier than the stated year), :31-36 (_corroborated), :76 (later = ...). Repro on a git archive of c4bb4da: `.venv/bin/python -I artifacts/review-evidence/T-141/probe2.py <archive>` (same script on c4bb4da~1 flags all of them). Each case is ER on the collision date, a PT follow-up on the date the intake states, intake 'Date of accident per intake form: <follow-up date>'. HEAD returns [] (no conflict, no tray item, no note) for: B ER 'Restrained driver, vehicle hit from behind at a stoplight. Neck pain.' (2026-01-09 vs stated 2026-01-19); C ER 'MVA 12/30/2025, neck pain.' with stated 2026-01-05 (previous year's digits make the sentence 'historical'); D ER 'Rear-end collision, no history of loss of consciousness.' ('history' makes the sentence 'historical'); F ER 'Pt in car when another vehicle hit them.'; G ER 'Rear-end collision, driver of a 2019 Honda Civic.' (model year < stated year). Only the plain 'Rear-end collision. Neck pain.' (E) still conflicts. The new tests (tests/unit/test_conflicts.py::test_t141_a_stated_date_still_conflicts_when_an_earlier_record_describes_the_collision) use exactly that plain wording, so none of B, C, D, F, G is pinned.",
   "why_it_matters": "R-FL-2 makes the accident-date conflict a must for the sample, and the 'accident_date' check is advertised in GET case checks. The skip turns a deterministic check into a word-list guess and its failure is invisible: the paralegal sees neither a conflict nor a could-not-verify item, so a real discrepancy between the stated accident date and the first treatment disappears. Before c4bb4da all five cases were flagged. The sample and all 27 golden/library packets are unchanged (diff of conflicts and candidates pre vs HEAD: only lib11), which is why the existing suites stay green. Not a blocker only because it needs the stated date to coincide with another record's date and a collision wording outside the list; it is a lost conflict (rate by D.2 'loses facts' if Chris disagrees).",
   "fix": "Do not drop. Either (a) widen _EVENT (hit, struck by, vehicle, motor vehicle, car, airbag, T-boned, side-swiped) and apply the _HISTORICAL / earlier-year exclusion to the clause that names the accident, not to the whole sentence, and treat a year equal to the stated year minus 0 or 1 with a month as possibly the index event; or (b) when the skip would apply and an earlier record is not provably a pre-accident visit, keep the flag but state the other reading (the stated date matches record N) so the paralegal decides, as D-055 does for paperwork.",
   "acceptance_test": "tests/unit/test_conflicts.py: the five variants B, C, D, F, G each return one accident_date_after_treatment conflict; the lib11 shape (annual PCP visit 2026-03-04 listing 2019 and 2022 accidents, EMS 2026-03-18 'struck from behind', intake 2026-03-18) still returns []."
  },
  {
   "severity": "major",
   "title": "GET case `checks` is the same on every case, so a Spanish case, or a run whose conflicts stage was skipped, is still told 'checked for denial vs history' and 'plan vs early end'",
   "evidence": "app/backend/conflict_candidates.py:244-247 (checks() takes no argument), app/backend/present.py:317 (\"checks\": conflict_candidates.checks()), memory/contracts/api.md:133 ('always present, the same on every case'). The candidate rules are English regexes (_DENIAL, _FORM_STEM, _ENDED, _EN_*): `artifacts/review-evidence/T-141/probe3.py` on the HEAD archive, records lang='es': 'La paciente niega lesiones previas en el cuello.' vs 'Historial de accidente de tráfico en 2019...' -> False; 'Accidentes previos: No.' -> False; a Spanish plan/outcome pair -> []. Live API on the HEAD copy: POST the Spanish library packet evals/library/case_lib09_spanish_interpreter_espalda.txt, then GET case -> checks.conflict_types = ['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] and not_checked has no language entry. pipeline.py:360-362 also lets `guard(\"conflicts\")` skip the whole conflict pass (deadline), with checks unchanged.",
   "why_it_matters": "T-142 exists to stop the UI overclaiming ('No conflicts found'). It now gets a list that says what was checked on this case, but the list is a constant, so on a Spanish case or a timed-out run the UI can say 'Checked for: a denial of prior problems...' when nothing could have fired. Same failure family as the empty-state overclaim, moved one layer down, and it is in the new field this card adds.",
   "fix": "Make checks a function of the case: add `skipped: [{type, reason}]` (or move a type into not_checked) when records are lang 'es' for the two English-rule checks, when the conflicts stage was skipped or errored, and when no record has a parsed date for accident_date. Keep the constant lists for the default.",
   "acceptance_test": "tests/unit/test_api_routes.py: GET case for a Spanish packet has denial_vs_history and plan_vs_early_end under not_checked (or skipped) with a language reason; an English case is unchanged; a case whose conflicts stage was guarded off lists all pair-rule types as skipped."
  },
  {
   "severity": "minor",
   "title": "The new denial rule has no topic restriction on its stem, and the year-named accident route has no negation or scope guard; the judge is the only filter and the controls do not cover those shapes",
   "evidence": "app/backend/conflict_candidates.py:49 and :53 (_FORM_STEM / _FORM_ONE accept any 'Prior|Previous|Pre-existing|Earlier + letters' stem answered No/None), :55 + :106-111 (_earlier_year_accident: accident word within 40 characters of 'in <year>' < denial year, no negation check beyond _DENIAL). `artifacts/review-evidence/T-141/probe1.py` (25 pairs, run on c4bb4da~1 and c4bb4da): HEAD now pairs 'Previous employer: None.', 'Prior authorization required? Yes [ ] No [X].', 'Previous visits to this clinic: None.' with 'History of lumbar strain in 2022.'; pairs 'Prior accidents? Yes [ ] No [X].' with 'No car accidents in 2019 or 2022.', 'Patient denies accidents in 2019 and 2022.', 'Records show no motor vehicle accident in 2019.' (the prior side is itself a negation); pairs a scoped question 'Prior accidents in the last year? ... No [X].' with 'Car accident in 2019'; and 'Rear-end collision at Main St, patient first seen here in 2019.' (index collision plus an unrelated year). Correct as designed: Yes checked, both boxes empty, both boxes checked, a bare question, an accident in the denial's own year, husband and other driver (P04, P06, P07, P17, P19, P23). Roommate (P05) pairs on purpose (J3V20). 'No prior accidents since 2010' vs 'Car accident in 2005' (P08, P25) pairs on both builds (T-094 inherited, not new). Live check, one run each, claude-cli with ENABLE_LIVE=1 (exploratory, not the 3x controls): J3 answered benign CAN_BOTH_BE_TRUE on P13, P14, P15, P09, P10, P08 and conflict FACT_MISMATCH on the real lib11 pair; script artifacts/review-evidence/T-141/live_j3.py. judge_conflict_v6 rule 2(c) answers conflict for 'the denial is general' and has no time-scope, negated-history or topic rule.",
   "why_it_matters": "Candidate generation is the first rung of the ladder; a wrong candidate costs a judge call and, if the judge is unavailable or answers unsure, shows the paralegal a needs_review conflict about an employer or a prior authorization (flags.py: judge unavailable keeps the flag). The single live run held, but J3 is a model and no control covers these shapes. Labelled 'I would tighten it' rather than a spec violation: the ladder as designed puts the judge behind the rule.",
   "fix": "Restrict _FORM_STEM/_FORM_ONE nouns to a closed list (accident, collision, injury, injuries, surgery, surgeries, condition, treatment, claim, back/neck problems); skip a prior sentence that is negated ('no', 'denies', 'never' before the accident word); skip a denial stem containing 'in the last|past|since'. Add wrong controls (J3V21..) for a topic stem, a negated history and a scoped question.",
   "acceptance_test": "tests/unit/test_conflict_candidates.py: history_denials returns [] for P09, P10, P11, P12, P13, P14, P15; the lib11 pair and 'Prior injuries: None.' vs 'History of lumbar strain in 2022.' still pair."
  },
  {
   "severity": "minor",
   "title": "The live 3x controls run for J3R5, J3R6, J3R7 and J3V20 is owed and no card or owner exists; the changelog has no entry for the new rows",
   "evidence": "Latest committed report evals/reports/controls-20261102T123937Z.json (source_commit bea3984, controls_ok True) has 64 rows and none of J3R5, J3R6, J3R7, J3V20 (checked: set intersection empty). Its `hashes` block does not include judge_controls.jsonl, so nothing marks the report stale. `python3 tools/board.py list | grep -i control` shows no open card for the run; the handoff text says 'qa/orchestrator: python -m evals.run --controls on a clean tree'. evals/golden/judge_controls.CHANGELOG.md has no round for this change (last entry is T-093 round 4). Labels themselves are fine: locked in evals/j3_controls.py with a rationale per row and in LOCKED in tests/unit/test_t093_j3_controls_reachable.py in the same commit as the rows, committed before any run of them (git show c4bb4da), and the reachability test passes (116 passed on the three conflict/controls modules).",
   "why_it_matters": "Answer to the brief: the live run is not required for acceptance of this card (AC 1 asks for unit tests, expected update and 'controls unaffected', and I verified that: candidates and accident-date output over all 27 golden and library packets are identical pre vs HEAD except lib11). It is required before the M2 gate: D-046 makes J3 'catch every seeded wrong item, 0 false agrees' a ship-bar condition, J3V20 is a new wrong item with no result, and a fixture run will report not_measured for it. Without an owner it will surface at the gate.",
   "fix": "Open a qa card for `LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --controls` (3 repeats) on a clean tree after the F-findings above land, so the rows for any new wrong controls run once; add the round entry to judge_controls.CHANGELOG.md with the four labels and reasons.",
   "acceptance_test": "A controls report newer than c4bb4da whose rows include J3R5, J3R6, J3R7 and J3V20 with 3 verdicts each; the changelog names them."
  },
  {
   "severity": "minor",
   "title": "A prior commit calls conflict_candidates.checks() before it exists: GET case raised AttributeError from T-143 until this commit",
   "evidence": "`git show 225e666:app/backend/present.py | grep -c 'conflict_candidates.checks()'` -> 1 and `git show 225e666:app/backend/conflict_candidates.py | grep -c 'def checks'` -> 0 (T-143 swept this hunk of T-141/T-142's work into its commit through the shared index). On the c4bb4da~1 archive: `.venv/bin/python -m pytest tests/unit/test_api_routes.py -q -x` -> `ERROR zlayt.api:api.py:184 unhandled AttributeError`, 1 failed (test_whole_case_after_run_matches_contract). Fixed at c4bb4da.",
   "why_it_matters": "Five commits (225e666 to e25098d) have a broken case endpoint; bisect lands on the wrong commit, and any reviewer pinned to one of them sees a 500 on every case.",
   "fix": "No code change needed now. Stage with pathspec per file-ownership rule; if a hunk of another card is in the index, commit them together or leave it unstaged.",
   "acceptance_test": "Each commit on main passes tests/unit/test_api_routes.py (a pre-push loop over the range)."
  },
  {
   "severity": "minor",
   "title": "lib11 still shows two 'mentions a prior or pre-existing condition' flags whose quotes are only the form labels, beside the new conflicts (paralegal view)",
   "evidence": "artifacts/review-evidence/T-141/lib11-body.txt:333 'Fennimoor Spine Clinic ... mentions a prior or pre-existing condition: “Prior accidents?”.' and :349 same for 'Prior injuries?'; screenshot artifacts/review-evidence/T-141/lib11-conflicts.png shows the two conflict cards. The flags carry the question without the answer (No), so they read as the form admitting a prior accident; the conflict cards beside them quote the answer. Two conflict cards also cite the same PCP sentence (accidents, injuries), so the paralegal decides the same fact twice. The GATE-M2 paralegal report listed the label-only flags as evidence; this card did not change them.",
   "why_it_matters": "A paralegal skimming 'mentions a prior or pre-existing condition: Prior accidents?' can quote it as an admission. The correct reading is in the conflict card, not in these.",
   "fix": "Suppress the lexicon pre_existing flag when the matched unit is a form stem answered No (the same _FORM_STEM + _FORM_NO test), or extend the quote to include the answer; show the two denial conflicts as one card with both quotes.",
   "acceptance_test": "lib11 case JSON: no pre_existing flag whose excerpt is 'Prior accidents?' or 'Prior injuries?'."
  },
  {
   "severity": "nit",
   "title": "Implementation notes written into the golden C1 summary",
   "evidence": "evals/library/case_lib11_priors_and_ledger.expected.json (C1 summary) now ends 'T-141: the code reads a checked No [X] (OCR No IX]) as the denial ... so this pair is now proposed and sent to the judge.'",
   "why_it_matters": "An expected file describes what the records say, not how the code finds it; the sentence will go stale with the next rule change.",
   "fix": "Keep the T-141 reason in the changelog or the card, not in the expected summary.",
   "acceptance_test": "C1 summary states only the record facts."
  }
 ],
 "whats_right": [
  "Intake form denials now read as a conflict with the answer quoted (No [X] and OCR No IX]), and the 27-packet differential shows only lib11 changed, so the existing J3 control text is untouched.",
  "N2 discriminates: the false accident-date conflict is red against the old code and green on HEAD; 9 of 11 mutants on the new rules are killed.",
  "Control labels were locked in code and in the test table in the same commit as the rows, before any run, with a reason per row."
 ],
 "questions_for_chris": [
  "Is the accident-date skip worth its recall cost? The alternative is to keep the conflict and print the other reading (the stated date matches record N), as D-055 does for paperwork."
 ]
}
```

Erratum: the summary line above says 3 minor; the JSON block lists 4 minor findings (3, 4, 5, 6) and is authoritative.
