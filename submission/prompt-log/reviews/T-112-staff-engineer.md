# T-112 review — staff-engineer-reviewer (round 1)

Card: D-054, code removes unsupported summary clauses before judging. Card commit afcde06; HEAD at review time 6e880e6 (app/backend/summary_trim.py, generator.py and tests/unit/test_summary_trim.py are byte-identical between the two). I worked on `git archive` copies of afcde06 and HEAD in my scratchpad (`T112_r1/a`, `T112_r1/h`).

**Verdict: changes.** Two majors, no blocker. The wiring is sound: each mutant I tried was killed (judge sees the untrimmed summary, empty not routed to the tray, translated records trimmed, trace step removed). Human edits are never trimmed. The weakness is the trimming rule itself and one unwired caller.

## What passes
- Judge sees the trimmed text: pipeline probe, 0 of 9 `j1` prompts contained the removed words ("splint", "cast"); mutant `summary = o.summary` fails `test_judge_sees_the_trimmed_summary...`.
- Each removal shows in the trace: step `summary_trimmed` (kind code, rule D-054) sits directly after `extracted` with `removed from the summary: not in the quote: 'splint fitted' ... 'cast applied'`; read back from the DB through `trace.item_trace`.
- Empty result goes to the tray: `rejected`, reasons `['SUMMARY_NOT_IN_QUOTE']`, no `errors[]` entry, the unsupported summary never reached the judge, accept returns 409 `item_rejected`.
- Human-written summaries: a human edit that adds "; splint fitted." persisted untrimmed (`summary_trim` is referenced only from generator.py and trace.py).
- Unit suite at HEAD archive: 2585 passed, 4 skipped. At afcde06: 2462 passed, 2 failed (see minor 5).

## Probe results (50 summaries, `T112_r1_scripts/probe.py`, `probe2.py`, `probe3.py`)
- 30 mixed cases: 27 as expected. Unsupported clauses were removed in 9 of 9 (MRI ordered, surgery recommended, cast applied, referred to neurosurgeon, hospitalized overnight, ...). Faithful paraphrases survived 15 of 17; the 2 that did not are finding 1; 1 modality swap (CT vs MRI scan) was kept for the judge.
- 20 further faithful pairs: 8 over-trimmed, 4 of them whole entries to the tray (finding 1).
- 5 partially overlapping hallucinations (finding 7): all kept.
- Offline sweep over the 188 recorded generator outputs in tests/fixtures/llm: trim fires on 8; the 3 English ones are correct ("Initial consult", "Annual visit", "Driver of a pickup ..."); the 5 Spanish ones are excluded in production by `is_translated`.

## AC 2: did T-112 fix its own cause?
Yes for the cause it set out to fix; the ship bar stays red for T-113's reason. All three reports (`evals/reports/20261102T093020Z.md`, `094902Z.md`, `100811Z.md`) name `Source commit afcde0628cd9637a2d09b190271650220d27d314, tree clean`; the extract_v1 and judge_faithfulness_v1 prompt hashes in the report match the afcde06 archive. In all three: hallucination 40/40, controls judged unsupported 0 of 10, `unsupported_count_3run` 0, determinism 1.0, `golden_must_not_hits` 0, unsplit_paste True, case_07_total_420 True. The "Blockers: 4_no_invented_facts; judge_controls" line is one failure: `evals/run.py:907-912` makes bar 4 end with `controls_ok(judge_controls)`, and J3 caught 15/17, 14/17, 13/17. So `ship_bar_met` False is attributable to J3 (T-113), not summary trimming.
Caveats: (a) case_02 is not fully clean in report 093020Z (finding 4); (b) the reports do not record how often the trim fired, and three clean 3-runs against a ~1-in-3 flap rate is only about 0.3 probable by luck, so the fix is evidenced but not proven (finding 4); (c) the rule only removes clauses sharing no content word (finding 7).

```json
{"card": "T-112", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive afcde06 and HEAD 6e880e6 in scratchpad T112_r1; app/backend/summary_trim.py, generator.py:44-78, trace.py:320-350, review.py:524-555; tests/unit/test_summary_trim.py; evals/reports/20261102T093020Z.md, 094902Z.md, 100811Z.md; sample case and case_04 via fake backend, no network",
 "exercised": [
  "read app/backend/summary_trim.py in full, git show afcde06 for generator.py, pipeline.py, trace.py, confidence.py, why.py, api.md, and tests/unit/test_summary_trim.py in full",
  "D-054 in memory/ORCHESTRATOR_DECISIONS.md and board show T-112",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit on git archive HEAD: 2585 passed, 4 skipped",
  "same on git archive afcde06: 2462 passed, 2 failed (tests/unit/test_provider.py::test_single_call_path, tests/unit/test_provider_backends.py::test_single_call_path), 4 skipped",
  ".venv/bin/python -m pytest -q tests/unit in the working tree (dirty, other agents' edits): 2643 passed, 1 failed (test_t114_rates_and_demo_judges lib07), 1 skipped; outside T-112",
  "probe.py, probe2.py, probe3.py: 50 summary/quote pairs through summary_trim.trim",
  "sweep.py: summary_trim.trim over every generator output in tests/fixtures/llm (188, fired on 8)",
  "wiring.py: full run_pipeline with a fake call on the sample case: trimmed entry, trace steps, judge prompts, human edit after trim, emptied summary to tray, accept on the tray item",
  "notdup.py: review.not_duplicate on case_04 with a fake extract whose summary is unsupported",
  "4 mutants of the afcde06 archive against test_summary_trim.py (judge sees untrimmed, empty not tray, translated trimmed, trace step off): each killed",
  "read evals/reports/20261102T093020Z.md, 094902Z.md, 100811Z.md headers, metric tables, Misses and prompt hashes; read evals/run.py ship_bar; shasum of the two prompts in the afcde06 archive; git status on evals/reports"
 ],
 "verdict": "changes",
 "scores": {"deterministic_trim_is_code": 5, "unsupported_removal_precision": 4, "faithful_paraphrase_survival": 2, "trace_visibility": 4, "empty_to_tray_all_paths": 2, "human_summaries_untouched": 4, "judge_sees_trimmed": 5, "test_strength": 3, "evidence_and_reports": 3},
 "findings": [
  {"severity": "major",
   "title": "Faithful paraphrases are over-trimmed: valid clauses removed, fragments left, whole entries sent to the tray",
   "evidence": "app/backend/summary_trim.py:65-66,109-120. `.venv/bin/python -I probe2.py` (afcde06 and HEAD identical): trim('Dizziness reported.', 'Pt dizzy since crash.') -> '' (tray); trim('Dizziness and blurred vision.', 'Dizzy, vision blurry.') -> 'Blurred vision.' removed ['Dizziness']; trim('Patient ambulating with a cane.', 'Walks with cane.') -> 'A cane.' (the ' with ' split removes 'Patient ambulating' and leaves a fragment); trim('Patient is anxious and tearful.', 'Anxiety, crying at exam.') -> '' ; trim('Numbness and tingling in fingers.', 'Paresthesias in digits.') -> ''; trim('Patient vomited twice.', 'Emesis x2.') -> ''; trim('Sleeping poorly.', 'Insomnia due to pain.') -> ''; trim('Taking Tylenol.', 'Acetaminophen PRN.') -> ''. 8 of 20 harder faithful pairs changed. Two are plain morphology (dizzy/dizziness: stem 'dizzi' vs 'dizzy' share 4 letters, the `_match` thresholds are 3-letter prefix with at most 3 extra letters or 5 shared letters), the others are vocabulary the abbreviation groups lack. The unit test `test_faithful_paraphrases_are_not_trimmed` has 11 pairs, all chosen to pass.",
   "why_it_matters": "Checked in this round: 'faithful paraphrases survive' is the card's own acceptance bar (AC 1 and D-054: only unsupported clauses are removed). A faithful clause dropped means the entry the paralegal sees is shorter than what the record says ('Dizziness' lost), and the ' with ' split can leave a meaningless summary ('A cane.') that the judge can still rate supported and a reviewer can accept into the letter. When every clause is a synonym, a valid entry is lost to the tray and entry_recall falls. Not a blocker: nothing is invented, the verbatim quote stays, the removal is shown in the trace and a human gate follows. Rated major, not minor, because a P0 rule that rewrites court-bound text must not mangle faithful input.",
   "fix": "(1) Normalize y/i before stem comparison (dizzy/dizziness, anxious/anxiety, bruise/bruising). (2) Do not remove a clause when removal would leave a kept clause that starts with an article or has fewer than two content words, or stop splitting on ' with ' unless both sides carry a content word of their own. (3) When a clause is the whole summary, require the stricter check or send to the judge rather than the tray. (4) Widen the groups (emesis/vomit, paresthesia/numbness/tingling, insomnia/sleep, anxious/anxiety, crying/tearful, walks/ambulat, brand/generic names), and replace the 11-pair test with a corpus of at least 40 faithful pairs drawn from the golden and library packets.",
   "acceptance_test": "tests/unit: trim('Dizziness reported.', 'Pt dizzy since crash.')['changed'] is False; trim('Patient ambulating with a cane.', 'Walks with cane.')['text'] is not 'A cane.' (either unchanged or a full clause); and a parametrized corpus of at least 40 faithful pairs asserts changed is False."},
  {"severity": "major",
   "title": "'Not a duplicate' split drops a SUMMARY_NOT_IN_QUOTE record: no entry, no tray item, and a message that says the AI failed",
   "evidence": "app/backend/review.py:549-553 calls generator.extract_one and on `\"failure\" in e` only appends a warning; pipeline.py is the only caller that builds generator.failure_entry. Repro (`.venv/bin/python -I notdup.py <HEAD archive>`, case_04, fake extract with summary 'Orthodontic braces tightened.'): warnings = [{'code': 'SUMMARY_NOT_IN_QUOTE', 'message': 'The record was split off, but the AI could not draft its entry; enter it by hand.', 'item_id': None}]; entries after split = e1, e3, e5, e6; items for r2 other than the merged entry = [].",
   "why_it_matters": "D-054 and AC 1 say an emptied summary goes to the could-not-verify tray and 'never vanishes' (generator.failure_entry docstring). On this path the record r2 is neither an entry nor a tray item, the only trace is a transient warning, and the warning text is false (the AI did draft; code removed it). The same gap already existed for LLM_FAILED_AFTER_RETRIES, but T-112 added a new failure code through the same door and its test covers only run_pipeline.",
   "fix": "In review.not_duplicate, when extract_one returns a failure, build `generator.failure_entry(rec, [rec['n']], e['failure'], e.get('detail'))`, upsert it as a rejected tray item, and choose the warning message by code (for SUMMARY_NOT_IN_QUOTE: 'code removed every part of the AI summary that the quote does not support'). Add the same handling to any other single-record re-extract caller.",
   "acceptance_test": "tests/unit/test_manual_and_split.py: seeded_case4 then RV.not_duplicate with an extract that returns an unsupported summary; assert DB.list_items(... 'entry') contains a rejected item for r2 with reasons ['SUMMARY_NOT_IN_QUOTE'] and the warning message does not say the AI could not draft the entry."},
  {"severity": "minor",
   "title": "Trace of a SUMMARY_NOT_IN_QUOTE tray item says the quote is not word for word, which is false",
   "evidence": "app/backend/trace.py:320-322 (`verbatim_fail` is true when the placeholder's excerpt is empty). Repro wiring.py case C: item trace steps for the tray item: `extracted fail | removed from the summary: not in the quote: 'Orthodontic braces tightened' ...` then `excerpt_verbatim fail | The quoted text is not word for word in the record, so this item was rejected and cannot be used.` and `judge_1 skipped | Not run: the quote did not pass the word-for-word check.` (also excerpt_whole_sentence, excerpt_hedge, summary_tokens, summary_qualifier, highlight). Trimming only runs after `grounding.locate` succeeds (generator.py:70), so the quote did pass.",
   "why_it_matters": "The audit trail contradicts itself: the first step gives the true cause, six later steps give a false one. A paralegal or the debugging engineer cannot tell which to believe. The LLM_FAILED placeholder shares the wording (existing), so this is a wart the new code inherited without fixing.",
   "fix": "In the placeholder branch of `_entry_steps`, set `stop` to the failure code (SUMMARY_NOT_IN_QUOTE, LLM_FAILED_AFTER_RETRIES) so the later steps read 'Not run: <reason>' and excerpt_verbatim is not asserted as failed.",
   "acceptance_test": "tests/unit/test_summary_trim.py pipeline test: for the emptied-summary tray item assert no step with id excerpt_verbatim and status fail, and every skipped step's why names the summary, not the word-for-word check."},
  {"severity": "minor",
   "title": "Live-report evidence is thinner than the handoff says: case_02 not clean in report 1, trim firing not recorded",
   "evidence": "evals/reports/20261102T093020Z.md:112: `entry misses: {\"case_02_gap_boundaries\": [{\"entry\": \"E1\", \"why\": \"excerpt misses must_contain_excerpt\"}], \"case_06_subtle_pre_existing\": ...}` (entry_recall 0.965); reports 094902Z and 100811Z list only case_06. `grep -in trim` over all three reports and the run artifacts evals/reports/runs/20261102T091115Z, T093020Z, T094902Z returns nothing: the per-run JSON keeps summary_sha only, so there is no count of trims fired.",
   "why_it_matters": "The case_02 unsupported-summary cause is clean in all three (0 unsupported, hallucination 40/40), but the E1 miss is on the record the fix targets, and with entry_recall 0.965 against a 0.95 bar one more miss fails recall. Without a trim counter nobody can show that the three clean runs came from the trim rather than from luck (about 0.3 chance of three clean 3-runs at a 1-in-3 flap rate).",
   "fix": "Add `summary_trim` counts (items trimmed, clauses removed, tray placeholders) to evals/run.py output and the report; note the case_02 E1 miss in the handoff.",
   "acceptance_test": "The next report has a metric row 'summary clauses removed by code' with a per-case count, and case_02 is clean in it or the miss is explained."},
  {"severity": "minor",
   "title": "Card commit afcde06 is not green and the cited count does not reproduce",
   "evidence": "AC 1 evidence says `unit suite 2453 passed`. `git archive afcde06` then `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit`: `2 failed, 2462 passed, 4 skipped`; failures `tests/unit/test_provider.py::test_single_call_path` and `tests/unit/test_provider_backends.py::test_single_call_path` (assert bad == [] -> `backend/cal...ion_route.py`). Cause is app/backend/calibration_route.py from T-102 276991b, fixed by 03206ca. `git archive HEAD`: `2585 passed, 4 skipped`.",
   "why_it_matters": "Not a T-112 defect, but the claim 'suite passed at the commit' only held in a working tree with later edits. A reviewer or a bisect at afcde06 sees red.",
   "fix": "State the run against the committed tree (clean checkout) in the handoff; no code change for T-112.",
   "acceptance_test": "Handoff quotes `git archive <sha> | tar -x; pytest -q tests/unit` counts for the sha under review."},
  {"severity": "minor",
   "title": "Human-summary guarantee is tested by grepping four file names",
   "evidence": "tests/unit/test_summary_trim.py:177-183 reads review.py, rejudge.py, export.py, narrative.py with `if p.exists()` and asserts the text 'summary_trim' is absent. api.py, store.py and pipeline.py are not covered, and nothing runs an edit. My behavioral probe (wiring.py B: apply_review edit adding '; splint fitted.') persisted the summary untrimmed, so the behavior is right today; no test would fail if a path started trimming.",
   "why_it_matters": "A source-text grep is an implementation test; the claim is a behavior ('human text is never trimmed').",
   "fix": "Replace with a behavioral test: run the pipeline, apply_review(edit) with a summary carrying an unsupported clause, assert the stored summary equals the edit and no ladder.summary_trim was added by the edit.",
   "acceptance_test": "A mutant that calls summary_trim.trim inside review._edit or manual_entry fails the new test."},
  {"severity": "minor",
   "title": "Design limit (not a spec violation): one shared content word keeps an invented clause",
   "evidence": "probe3.py on quote 'Patient reports left wrist pain 6/10.': 'Left wrist pain 6/10; splint fitted to the wrist.' -> unchanged; 'Left wrist fracture noted.' -> unchanged; 'Left wrist pain 6/10; wrist splint applied.' -> unchanged; 'Left wrist pain 6/10; patient referred to surgeon for wrist.' -> unchanged. Same for the group-generosity cases: 'Pain, splint fitted.' over 'Fell on back.' keeps 'Pain' (lbp group {low, back, pain}); 'CT scan ordered.' over 'MRI scan of brain.' is kept (scan group).",
   "why_it_matters": "This matches D-054 as written ('no content-word support'), so I label it 'I would have done it differently', not a violation. The residual risk is that the case_02 flap returns with a phrasing that shares one noun with the quote, because judge 1 still sees the clause.",
   "fix": "Consider counting only non-anatomical, non-side content words as support, or require two supported words for clauses of four or more content words; keep the current rule if the next three live runs show no case_02 unsupported item.",
   "acceptance_test": "trim('Left wrist pain 6/10; splint fitted to the wrist.', 'Patient reports left wrist pain 6/10.')['removed'] == ['splint fitted to the wrist'] while the faithful corpus from the first finding still shows changed False."},
  {"severity": "nit",
   "title": "The three cited live reports are untracked files",
   "evidence": "`git status --short evals/reports` lists `?? evals/reports/20261102T0...Z.md` entries; `git ls-files --error-unmatch evals/reports/20261102T093020Z.md` -> `error: pathspec ... did not match any file(s) known to git`.",
   "why_it_matters": "The evidence for AC 2 is only on one disk; the commit does not carry it.",
   "fix": "Commit the three reports (or copy them under artifacts/) with the card's closing commit.",
   "acceptance_test": "git ls-files lists the three report paths."}
 ],
 "whats_right": [
  "Trimming is pure, deterministic code with no LLM or network import, and keeps the model's original output in ladder.generator.output next to ladder.summary_trim for audit.",
  "Wiring is guarded and mutant-tested: trim runs only after the quote is located in the record, skips translated records, feeds the trimmed text to the judge and the D-034 token checks, and an empty result is a rejected tray item with no errors[] entry.",
  "Reports name afcde06 with a clean tree, prompt hashes match the commit, and the only red part of bar 4 is controls_ok (J3), so the AC 2 reading is clean about T-113 ownership."
 ],
 "questions_for_chris": []}
```
