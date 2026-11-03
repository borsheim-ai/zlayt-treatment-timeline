# T-036 LLM flag passes, round 2 (commit cd4bc60): claims-adjuster review (Gary Pruitt)

Verdict: **fail** (1 blocker, 2 major, 1 minor, 1 nit).

Round-1 items, status on cd4bc60:
- Blocker `objective_negative` title "No objective findings noted": **resolved.** `grep -n "No objective findings" app/backend/flag_templates.py` returned nothing (exit 1). New template at flag_templates.py:132 reads `"objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}.")`. An own-voice sweep over all 21 TYPE_OF categories with two quotes found no "objective", "subjective", "question", "suggest", "could be used", "another cause", "severe", "significant", "traumatic", "acute" or "herniation" outside the verbatim quote.
- Major, silent conflict-pass loss: **partly resolved.** The failure now yields a visible needs_review `record_warning` flag (flags.py:201, 203). The run-level signal the fix asked for does not exist (finding 2).
- Major, J3 fixture shape: **resolved.** A conflict without `excerpt_b` is rejected (flags.py, `or not m.excerpt_b`), and test_pipeline.py's J3 tests now pass.
- Major, intake date labelled patient self-report: **resolved for record 7, but the fix over-reaches.** Record 7's flag is now `record`. The lexicon self-report mechanism was removed for every entry, which breaks the spec (finding 1).

Findings:
1. **Blocker.** `source_kind` no longer comes from the lexicon `self_report` entries, which DECISIONS.md:286 requires. Lines that the lexicon itself marks as patient self-report now read as record statements. Flag-level probe: "Patient notes prior neck pain." gives `pre_existing`, `source_kind=record`, and a title with no self-report attribution. "Patient links her neck pain to the collision." gives `category=patient_report` with title "Patient self-report" but `source_kind=record`. The control "Patient reports prior neck pain." gives `patient_report`. No fact is invented, since the verbatim quote keeps "Patient notes", but the attribution the spec requires is lost.
2. **Major.** On a conflict-pass failure the run still reports `status=done` with no error or warning. flags.py:183 says "the pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial", but nothing reads `pipeline_warning`.
3. **Major.** The full unit suite is still red: `5 failed, 750 passed`, all in test_t037_backend.py. Round 1 reported 3.
4. **Minor.** The conflict-pass warning is attached to record 1 and its "why" text says record 1 has no AI entry. Record 1 has entry e1.
5. **Nit.** Every quote template still ends in `.”.`.

What is right:
- The objective_negative title is neutral, and the own-voice sweep over all 21 categories is clean.
- The record-7 intake date is `record`, and the conflict-pass failure path now produces a visible needs_review item for both LLMFailed and FixtureMiss.
- A single-quote conflict is rejected (`SCHEMA_INVALID`), and test_flags_pass.py covers it.

Outside my lens: the wording of the FIXTURE_MISS "why" ("The demo has no recorded AI answer...", why.py:16) is product copy. I did not rate it.

```json
{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit cd4bc60 (app/backend/flag_templates.py, flags.py, grounding.py, tests/unit/test_flags_pass.py) against 199785f; app/llm/lexicon.yaml, memory/DECISIONS.md:286 as the source_kind spec; sample case via fixture pipeline (no live app URL; LLM is scripted FakeCall)",
 "exercised": [
  "Read personas/claims-adjuster.md in full",
  "grep -n 'No objective findings' app/backend/flag_templates.py -> no output, exit=1",
  "grep -n 'objective_negative' -A6 app/backend/flag_templates.py -> lines 37 and 132 (new template quoted in the summary)",
  "grep -rn 'CONFLICT_PASS_INCOMPLETE|analysis_incomplete' app/ -> flag_templates.py:38,136; flags.py:184-188",
  "grep -rn 'pipeline_warning|CONFLICT_PASS_INCOMPLETE' app/ tests/ -> only flags.py:183,188 (no reader in pipeline.py)",
  "grep -n 'patient_report' app/backend/flags.py -> flags.py:42 source_kind = patient_report if grounding.has_self_report(excerpt)",
  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2 -> 48 passed in 0.27s",
  ".venv/bin/python -m pytest tests/unit/test_pipeline.py tests/unit/test_flags_pass.py tests/unit/test_conflicts.py -q -> 45 passed",
  ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6 -> 5 failed, 750 passed (test_t037_backend.py: test_replay_has_no_fixture_miss[case_02_gap_boundaries], [case_08_diagnosis_temptation], [case_09_nonvisit_hides_gap], test_judge_lines_replay, test_fixtures_come_only_from_golden_text)",
  ".venv/bin/python -m pytest tests/unit/test_t037_backend.py -q (failure messages read)",
  "git show --stat cd4bc60; git show cd4bc60 -- app/backend/flag_templates.py app/backend/flags.py app/backend/grounding.py tests/unit/test_flags_pass.py",
  "grep -n 'self_report' app/llm/lexicon.yaml; parsed lexicon.yaml: 4 entries with self_report: true (self_reported_prior, patient_attributes_causation, patient_reports_generic, intake_form_accident_date)",
  "sed -n 22,28p app/llm/lexicon.yaml (header: code sets source_kind from self_report)",
  "grep -n 'source_kind' memory/DECISIONS.md -> line 286 (source_kind set by code from the lexicon self_report entries)",
  "app/frontend/flags.js:63 (chip logic: source_kind patient_report and title not 'Patient self-report')",
  "artifacts/review-evidence/T-036-r2-probe.py -> T-036-r2-probe.txt (template sweep over 21 categories x 2 quotes; conflict-pass failure paths LLMFailed/FixtureMiss on the sample; has_self_report vs lexicon self_report hits on 13 lines)",
  "artifacts/review-evidence/T-036-r2-probe4.py -> T-036-r2-probe4.txt (record-1 entries, f_cx1 record_ids, run status on LLMFailed)",
  "artifacts/review-evidence/T-036-r2-probe5.py -> T-036-r2-probe5.txt (lexicon_flags source_kind on 4 lines)",
  "python3 tools/board.py show T-036 (card AC, notes; AC2 defers full fixture run to T-037)"
 ],
 "verdict": "fail",
 "scores": {"surfaces_every_attack_item_on_sample": 4, "no_invented_or_overstated_text": 3, "patient_attribution_label": 2, "visible_conflict_failure": 3, "template_neutrality": 5, "test_honesty": 2},
 "findings": [
  {"severity": "blocker",
   "title": "source_kind no longer comes from lexicon self_report entries (spec DECISIONS.md:286); self-reported prior and causation lines lose patient attribution",
   "evidence": "app/backend/grounding.py:174-176 `def _self_report(text): return bool(_SELF.search(text))` (round-2 diff deleted `or any(rx.search(text) for rx in _lexicon()['self_report'].values())`). Spec memory/DECISIONS.md:286: 'source_kind = \"patient_report\" is set by code from the lexicon self_report entries on the excerpt'. app/llm/lexicon.yaml:25-26 header: 'code sets source_kind = \"patient_report\" from it (ADR-013)'. Flag-level output artifacts/review-evidence/T-036-r2-probe5.txt: `'Patient notes prior neck pain.' type=pre_existing category=pre_existing source_kind=record title='Mention of a prior or pre-existing condition'` (lexicon self_reported_prior hit); `'Patient links her neck pain to the collision.' type=causation category=patient_report source_kind=record title='Patient self-report'`; control `'Patient reports prior neck pain.' ... source_kind=patient_report`. Sweep T-036-r2-probe.txt section 3: 'Subjective: neck pain 7/10.', 'Patient describes neck pain since the collision.', 'Patient-reported neck pain 7/10.' are lexicon hits with has_self_report=False.",
   "why_it_matters": "The spec says the lexicon's self_report entries drive source_kind. The round-2 change removed that for every entry, not only the intake-form entry round 1 named. A patient's pre-existing or causation statement now reads as a record statement in the structured field, and for the pre-existing line the title carries no self-report attribution (checklist 9, 10). The verbatim quote still says 'Patient notes', so nothing is invented, but the attribution the spec requires is lost.",
   "fix": "Restore the lexicon contribution in grounding._self_report (regex OR any lexicon self_report entry on the excerpt). Set self_report: false on intake_form_accident_date (lexicon.yaml:759-764) so the record-7 date stays 'record'. Remove EMS, witness, wife, husband, family and friend from patient_reports_generic (lexicon.yaml:743-746), because an EMS report is not a patient statement. If the narrowing was intended, amend DECISIONS.md:286 and lexicon.yaml:25-26 in the same commit (see questions_for_chris).",
   "acceptance_test": "tests/unit/test_flags_pass.py: lexicon_flags on 'Patient notes prior neck pain.' and 'Patient links her neck pain to the collision.' give source_kind == 'patient_report'; 'Date of accident per intake form: 2026-01-19.' gives 'record'; grounding.has_self_report('EMS reports neck pain 7/10.') is False; the existing record-9 and record-7 tests still pass."},
  {"severity": "major",
   "title": "Conflict-pass failure is visible on the flag, but the run still reports status done with no warning or error",
   "evidence": "artifacts/review-evidence/T-036-r2-probe.txt section 2: 'conflicts LLMFailed: status=done errors=[] warnings=[]' and 'conflicts FixtureMiss: status=done errors=[] warnings=[]'. artifacts/review-evidence/T-036-r2-probe4.txt: 'status: done errors: [] warnings: []'. app/backend/flags.py:183 docstring: 'pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial'. grep -rn 'pipeline_warning' app/ returns only flags.py:183 and flags.py:188 (the flag key); app/backend/pipeline.py:304 `status = 'done_with_errors' if errors else 'done'` never reads it.",
   "why_it_matters": "Round 1 asked for a visible item and a pipeline warning. The item exists, so the attorney sees 'Cross-record check did not finish' in the flags list. The run-level signal is missing, and the docstring claims it exists, so a reader is told the run is partial when the status says done. That is the silent-pass concern in another form. Major, not blocker, because the visible needs_review flag does reach the reviewer.",
   "fix": "In pipeline.py, read the conflict-stage flag's pipeline_warning and append a warning {code: 'CONFLICT_PASS_INCOMPLETE', stage: 'conflicts'} to out['warnings'], and set status to 'done_with_errors' or a partial marker. Or correct the docstring and the handoff if the run-level status is out of scope.",
   "acceptance_test": "test_pipeline.py: run_sample(..., conflicts=AU.LLMFailed('down')) -> 'CONFLICT_PASS_INCOMPLETE' in [w['code'] for w in out['warnings']] and out['status'] != 'done'; the same for P.FixtureMiss."},
  {"severity": "major",
   "title": "Full unit suite is still red: 5 failures in test_t037_backend.py (round 1 reported 3, all now in a different file)",
   "evidence": ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6 -> '5 failed, 750 passed in 10.12s'. Failures: test_t037_backend.py::test_replay_has_no_fixture_miss[case_02_gap_boundaries] (view errors: LLM_FAILED_AFTER_RETRIES at extract, record 1, cause FIXTURE_MISS; line 36), [case_08_diagnosis_temptation] (flag 'Clinical correlation recommended.' has reasons incl. FIXTURE_MISS; line 38), [case_09_nonvisit_hides_gap] (line 36), test_judge_lines_replay (H01: judge_summary returns 'unavailable'; line 52), test_fixtures_come_only_from_golden_text (message 'text is not an evals/golden input; refusing to record' vs expected 'not in evals/golden'; line 62). The round-1 test_pipeline.py J3 failures now pass: .venv/bin/python -m pytest tests/unit/test_pipeline.py tests/unit/test_flags_pass.py tests/unit/test_conflicts.py -q -> 45 passed.",
   "why_it_matters": "A green unit suite is the gate the handoff relies on. Five red tests with no owner named keep the 'verified' claim unsupported. Scope note: board AC2 says the full fixture run waits for T-037, so these may belong to T-037. I did not check out HEAD~1 to prove cd4bc60 is not the cause, and I did not downgrade for that.",
   "fix": "Either fix the golden fixtures for case_02, case_08 and case_09 and the judge line, or name the owning card for each failure in the handoff and make the suite count explicit.",
   "acceptance_test": ".venv/bin/python -m pytest tests/unit -q reports 0 failed, or the handoff lists each failing test with its owning card and the board shows that card in progress."},
  {"severity": "minor",
   "title": "Case-wide conflict-pass warning is attached to record 1, and its why text says record 1 has no AI entry",
   "evidence": "artifacts/review-evidence/T-036-r2-probe4.txt: 'f_cx1 record_warning ['r1'] needs_review' and 'entries with record 1: [('e1', ['r1'])]'. app/backend/flags.py:186-187 sets record_no=records[0]['n']. Why text from app/backend/why.py:28 'The AI step failed on all three attempts, so this record has no AI-made entry.' (LLM path); why.py:16 'The demo has no recorded AI answer for this step...' (FixtureMiss path).",
   "why_it_matters": "The warning concerns the conflict check across all records, but it is pinned to record 1 and says record 1 has no AI entry. Record 1 does have entry e1. A paralegal could read it as record 1 being left out of review. The explanation text ('conflicts between records may be missing') is accurate; the attribution and the why are not.",
   "fix": "Leave record_ids empty for the case-level warning, or attach it to every distinct record. Give it a conflict-specific why code instead of the per-record LLM_FAILED_AFTER_RETRIES text.",
   "acceptance_test": "run_sample with conflicts=AU.LLMFailed: the f_cx record_warning has no single record_id, and its why does not contain 'has no AI-made entry'."},
  {"severity": "nit",
   "title": "Every quote template still ends in a double period, '.”.'",
   "evidence": "artifacts/review-evidence/T-036-r2-probe.txt section 1: 'Capital PT (January 23, 2026) mentions a prior or pre-existing condition: “Cervical ROM full, no spasm noted.”.' Same pattern in all quote templates (flag_templates.py _quote usage).",
   "why_it_matters": "A quote that already ends in a period followed by a second one reads as careless in a document that goes to counsel. Carried from round 1; not changed.",
   "fix": "Omit the template period after a closing quote, or strip the quote's trailing period.",
   "acceptance_test": "No rendered explanation in flag_templates.TEMPLATES contains the sequence '.”.'."}
 ],
 "whats_right": [
  "The objective_negative title is neutral: 'Normal or absent findings wording'. No 'objective' or 'subjective' appears in any rendered title or explanation outside the verbatim quote, across 21 categories.",
  "Record 7's intake-form date is source_kind 'record' (probe5), and a conflict-pass failure (LLMFailed or FixtureMiss) now yields a visible needs_review item instead of an empty list.",
  "A single-quote conflict is rejected as SCHEMA_INVALID (test_flags_pass.py::test_single_quote_conflict_is_rejected passes), so the round-1 garbled 'the record.' rendering cannot reach the review."
 ],
 "questions_for_chris": [
  "Was narrowing grounding._self_report to regex-only an intended decision? If yes, DECISIONS.md:286 and lexicon.yaml:25-26 are stale and need amending; if no, finding 1 stands as written.",
  "Is the 5-test red set in test_t037_backend.py owned by T-037 (board AC2 defers the full fixture run to T-037)? If so, should T-036 be allowed to hand off with the unit suite red?"
 ]}
```
