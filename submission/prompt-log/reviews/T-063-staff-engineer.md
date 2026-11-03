# T-063 review: staff-engineer-reviewer

Scope: commit 473ac2a (docs/LLM_VS_CODE.md row 1 and the "Added in the second build wave (D-031 to D-035)" section; memory/DECISIONS.md ADR-018). Code verified at 473ac2a via `git archive`, not the working tree. HEAD moved to 636a042 during the review; every check below is pinned to 473ac2a.

Verdict: **fail**. One blocker and six majors. The doc describes several behaviours the code does not have, and the D-033 mismatch is an attribution error that the doc says must not happen.

Rating note: the brief said to file mismatches as majors. I rated the D-033 mismatch a blocker because CONTRACT D.2 (persona section 8) defines a violated spec constraint as a blocker, and D-033 is an explicit constraint ("family ... statements are not patient self-report"). The code labels a mother's statement as the patient's self-report. If Chris or the orchestrator disagrees, that is their call to make, not mine to take.

## What I checked, in order

1. Row 1 (docs/LLM_VS_CODE.md:29) against `ingest.validate_split` (app/backend/ingest.py:149-165), the split trigger (ingest.py:262-270), the SPLIT_* warnings (ingest.py:284-289), split_llm.py, and the schema (schemas.py:59-66). Result: validator clauses match the doc; the SPLIT_REJECTED claim and the "one unsplit block" trigger do not.
2. Manual entry (review.py:226-272), 422 rules (review.py:68-70, 241, 246-248), not_duplicate (review.py:276-329), batch accept (case_extras.py:24-63, review.py:348-351, app/frontend/batch.js:11-19). Result: the doc says manual entry and not_duplicate are code only; both call a model.
3. Narrative (narrative.py:50-111, schemas.py:69-76, export.py:136-139, 520-526). Result: the doc says code splits the paragraph into sentences; the model returns the sentences.
4. D-032 to D-035 in flags.py (lines 12-15, 46, 78, 107, 125, 139) and grounding.py (188-230), against lexicon.yaml. Results: D-034 holds; D-032 and D-033 do not match the doc's description.
5. Tests at the pinned sha: clean `git archive` gives 9 failed, 874 passed. Three failures are in the test file the AC names (test_split_llm.py), because the split replay fixture was deleted in b365af3 and not restored.

## Exercised (what I ran)

- `python3 tools/board.py show T-063`; `git show --stat 473ac2a`; `git show 473ac2a -- docs/LLM_VS_CODE.md memory/DECISIONS.md`; `git diff --stat b365af3 473ac2a` (docs and memory only).
- `git grep` at 473ac2a for validate_split, LLM_SPLIT, SPLIT_REJECTED, SPLIT_AMBIGUOUS, D-031 to D-035.
- Read at 473ac2a: app/backend/ingest.py, split_llm.py, schemas.py, pipeline.py (run_ingest, run_pipeline, ingest_case), review.py, case_extras.py, narrative.py, flags.py, grounding.py, export.py, app/llm/lexicon.yaml (self_report_scope, patient_reports_generic, objective and scene entries), app/frontend/batch.js, tests/unit/test_split_llm.py.
- `git ls-tree -r --name-only {099732b,b365af3,473ac2a} | grep -c 'fixtures/llm/split/'` gave 1, 0, 0.
- Clean run: `git archive 473ac2a | tar -x -C artifacts/review-evidence/T-063-staff-engineer/clean-473ac2a`, then `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -rf`: **9 failed, 874 passed**, saved to artifacts/review-evidence/T-063-staff-engineer/pytest_473ac2a_clean.txt.
- Control run in artifacts/review-evidence/T-063-staff-engineer/tree-473ac2a (pinned archive plus working-tree LLM fixtures copied in, so not clean): with `tests/fixtures/llm/split` restored, test_split_llm.py passes in full. Remaining with all LLM fixtures copied: **5 failed, 878 passed** (test_t037_backend x3 with judge-step j1 fixture misses, test_narrative replay returning LLM_FAILED_AFTER_RETRIES, test_case_extras batch accept x1).
- Mutation spot-check, in a scratch copy of tree-473ac2a (restored and diffed against 473ac2a afterwards): dropping the line-start check, the record cap, contiguity, or coverage in validate_split each made test_split_llm.py fail (1, 1, 2, 1 failures).
- Probe script artifacts/review-evidence/T-063-staff-engineer/probe_t063.py, run with `.venv/bin/python`, sections 1 to 6 (outputs quoted below).
- CLI: `.venv/bin/python -m app.pipeline evals/golden/sample.txt` run twice in the clean archive: exit 0 both, outputs byte-identical (cli_sample_run1.txt, cli_sample_run2.txt). Status done, records 9, entries 9, flags 10, amounts 3. Judge j4 calls miss fixtures on the clean tree, so the sample shows needs_review throughout; that is the pre-existing fixture gap, not this commit.
- Not run: eval runner, browser UI, an end-to-end not_duplicate on a merged entry, an HTTP call to the 422 routes, ADR-005 and ADR-015 supersession text.
- Housekeeping: I wrote one scratch copy of ingest.py to /tmp and deleted it, which breaks the scratch-directory rule. The probe's temp DB lives in the system temp dir. Nothing persists outside artifacts/review-evidence.

## Probe output (verbatim, from probe_t063.py)

```
== 1. no splitter: warning codes
split_method ambiguous split_failure None codes ['SPLIT_AMBIGUOUS', 'DATE_EXCLUDED_FROM_GAPS']
invalid proposal: split_failure SPLIT_NOT_COVERING codes ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'DATE_EXCLUDED_FROM_GAPS']
== 2. splitter call condition
A date+source label, no excerpt (recognised block): splitter called=False
B no labels at all (unsplit): splitter called=True
C date + excerpt label, no source (recognised, incomplete): splitter called=True
== 3. has_self_report (D-033)
has_self_report=True   'Complains of neck pain since the collision.'
has_self_report=True   'She reports the pain started after the accident.'
has_self_report=True   'Dr. Pell notes patient states pain 7/10.'
has_self_report=True   'Mother: c/o neck pain.'
has_self_report=False  'EMS reports neck pain 7/10.'
has_self_report=False  'Wife complains of neck pain.'
has_self_report=False  'Per his wife, headaches began at the scene.'
== 4. lexicon_flags
0 flag(s)  'Subjective complaints out of proportion to exam findings.'
0 flag(s)  'Waddell signs positive 3/5.'
0 flag(s)  'Patient exhibits symptom magnification and secondary gain.'
0 flag(s)  'Full cervical ROM.'
0 flag(s)  'CT head negative.'
0 flag(s)  'Cyclist struck by a car at low speed.'
1 flag(s) [('scene_facts', 'causation')]  'Ambulatory at scene, refused transport.'
2 flag(s) [('scene_facts', 'causation'), ('scene_facts', 'causation')]  'Minimal damage to vehicle; airbags did not deploy.'
== 5. manual entry model calls (doc says none)
manual_entry ok; item state needs_review warnings ['JUDGE_UNAVAILABLE']
model steps invoked by manual_entry: ['j1']
== 6. D-034 numeric override (manual entry, confirm_warnings=True)
refused: 422 invalid_edit | reason: SUMMARY_NUMBER_NOT_IN_EXCERPT | tokens: ['7'] | ...
```

(Section 3 lines for "Patient states ...", "Pt c/o ..." and "C/O neck pain 7/10." returned True and are not quoted; the probe prints them in full.)

## Mismatches and findings

**B1 (blocker) D-033: the self-report label goes to family and pronoun statements.** Doc (docs/LLM_VS_CODE.md:97) says the label is attached "only to a clause that starts with an explicit patient subject plus a reporting verb". The code sets `source_kind = patient_report` for any sentence where a lexicon pattern matches and the sentence does not start with a named non-patient speaker (grounding.py:188-198; lexicon.yaml:754-759 `patient_reports_generic`; exclusion scope at lexicon.yaml:88-89). The exclusion needs whitespace after the speaker name, so "Mother: c/o neck pain." passes. Bare "Complains of", and "She reports", match with no explicit patient subject. flags.py:46 and :125 write the label from this function. Reproduce: probe section 3 (True for "Mother: c/o neck pain.", "She reports ...", "Complains of neck pain ..."). Caveat: I showed this at function level. I did not run an end-to-end case where a flag quotes such a sentence, though the label is written on any flag whose excerpt matches.

**M1 (major) SPLIT_REJECTED with no model.** Doc row 1 (docs/LLM_VS_CODE.md:29) says: "If validation fails, or no model is available, the whole paste is one record flagged SPLIT_AMBIGUOUS with a SPLIT_REJECTED reason." ADR-018 (memory/DECISIONS.md:341) says "(SPLIT_REJECTED otherwise)". Code emits SPLIT_REJECTED only when `split_failure` is set (ingest.py:288-289), which needs a splitter that ran. `ingest_case` passes no call (pipeline.py:166-168), so the creation path emits SPLIT_AMBIGUOUS only. Reproduce: probe section 1, first line. Fix: emit SPLIT_REJECTED with reason NO_MODEL when an ambiguous single block is not sent to a model, or correct the doc. Acceptance test: `IN.ingest(TEXT)` contains a SPLIT_REJECTED warning whose message names the reason.

**M2 (major) Manual entry is "code only, no model" but runs judge 1.** Doc says at docs/LLM_VS_CODE.md:94 "(code only) ... no model is involved". Code: review.py:251 passes `call` into `_check_summary`, which runs `judges.run_j1_meta` when `call` is set (review.py:79-82). api.py:383 always passes `make_call`. Reproduce: probe section 5 prints `model steps invoked by manual_entry: ['j1']`. Judge 1 is the right design for a human-written summary, so I would fix the doc, not the code. Acceptance test: a recording call on manual_entry asserts steps == ['j1'], and the doc names judge 1 for manual entry.

**M3 (major) "Not a duplicate" is "code only, logged" but calls the generator and two judges.** Doc row 1 (docs/LLM_VS_CODE.md:29) says "A reviewer can mark two merged amounts 'not a duplicate' (code only, logged)"; ADR-018 (memory/DECISIONS.md:341) repeats "code-only". Code: review.py:300-306 calls `generator.extract_one` and `judge_entries`; review.py:320-321 calls `judges_for` -> `judges.judge_amounts`; api.py:396 passes `make_call`. The action also works on an entry and a record (review.py:276-288), not on "two merged amounts". Read from code only; I did not run it end to end. Fix: correct the doc and ADR (the entry is grounded and judged, which is the safe behaviour) or remove the calls. Acceptance test: split a two-record merged entry with a recording call and assert the steps match the doc.

**M4 (major) Narrative: "code splits it into sentences" is not what happens.** Doc (docs/LLM_VS_CODE.md:95) says "Code splits it into sentences and checks every sentence". The model returns the sentence list with entry ids (schemas.py:69-76); narrative.py:82 reads `NarrativeOutput.sentences` directly, with no splitter in narrative.py. Code still checks each returned sentence (narrative.py:87-108), so the risk is contained, but the doc describes a different segmentation owner. Fix: either split the paragraph in code, or change the doc to "the model returns sentences; code checks each one". Acceptance test: a model reply with one sentence citing e1 and containing a figure that only appears in e2 is removed with SUMMARY_TOKEN_NOT_IN_EXCERPT.

**M5 (major, question for Chris) D-032 scope is wider in code than in the doc.** Doc (docs/LLM_VS_CODE.md:97) says "Normal or negative findings ('negative for fracture', 'full ROM') are context only". Code drops the whole objective_negative category (flags.py:14, :78, :107). That category also holds credibility-attack phrases: "out of proportion" and "no objective findings" (lexicon.yaml:852-858), "Waddell", "malingering", "exaggerat", "secondary gain" (lexicon.yaml:1159-1166). Probe section 4 shows zero flags for "Waddell signs positive 3/5." and "...symptom magnification and secondary gain." D-018 made those causation flags. D-032 (memory/ORCHESTRATOR_DECISIONS.md:40) names the category objective_negative, so the code follows the literal decision. Either the doc is wrong or the code suppresses flags the decision did not intend to suppress. Fix: decide which, then make doc and code agree. Acceptance test: the chosen behaviour asserted for "Waddell signs positive 3/5." and for "Full cervical ROM.".

**M6 (major) The test file the AC names is red at the pinned sha.** The AC names tests/unit/test_split_llm.py. At 473ac2a, `git ls-tree` shows zero `tests/fixtures/llm/split/` files; 099732b had one, and b365af3 deleted it. Clean run: `.venv/bin/python -m pytest tests/unit/test_split_llm.py` reports three failures (test_golden_unsplit_paste_replays_recorded_split_through_audited, test_run_pipeline_replaces_the_single_stored_record, test_split_audit_row_has_prompt_version_and_flag_resolves_to_call). Full clean suite: 9 failed, 874 passed (pytest_473ac2a_clean.txt). Six of the nine are in other files and are pre-existing judge-replay misses (t037 x3, narrative replay, batch accept x2). The diff since the parent is docs and memory only, so these results are the parent's too. This commit did not create the red tests, but the doc points at them as evidence. Fix: restore a re-recorded split fixture under tests/fixtures/llm/split and re-run the clean archive. Acceptance test: `git archive 473ac2a | tar -x` then `pytest tests/unit/test_split_llm.py -q` reports 0 failures.

**M7 (major, latent) Batch accept: the UI fallback skips the server's verified-only check.** The batch route refuses any id that is not a verified entry before writing (case_extras.py:24-51). The per-item accept route only blocks rejected items (review.py:48-49). app/frontend/batch.js:17-19 switches to one per-item accept call per eligible id on a 404 or 405, with no message to the user. The route is registered (api.py:459), so the fallback is not reachable on this server, which is why I rate it major and latent. Under persona section 5, a reachable silent fallback that changes the verified-only guard would be a blocker. Fix: delete the fallback, or show an error and accept nothing. Acceptance test: stub a 404 on the batch route and assert nothing is accepted and the user sees an error.

**m1 (minor) The model is called for one recognised but incomplete block.** Doc says "only when the code split finds one unsplit block". Code calls the model when the single record is unsplit or lacks a date or source label (ingest.py:262). Probe section 2, case C (a block with Date and Excerpt labels, no Source) calls the splitter; case A does not. Fix: align the doc with the condition, or change the condition. Acceptance test: one case per branch.

**m2 (minor) Swallowed judge exception in the shared edit path.** review.py:83-84 `except Exception:` turns any error into `unavailable`. The state is visible (JUDGE_UNAVAILABLE), so this is not silent, but the error class and call id are lost. The new manual-entry path inherits this. Fix: catch the provider errors the judge can raise and let anything else propagate. Acceptance test: a non-provider exception from the judge propagates.

**m3 (minor) Narrative wording.** Doc says a number must "come from an accepted entry" (docs/LLM_VS_CODE.md:95). Code checks the cited entry's quote (narrative.py:54), which is stricter and correct. Doc says a failing sentence is "marked"; code moves it to `removed` (narrative.py:96-97). Fix the wording.

**n1 (nit).** Doc (docs/LLM_VS_CODE.md:96) says batch accept happens "after she confirms the count". The button shows the count (batch.js bar); there is no confirm step.

## Right (keep these)

- The four validate_split clauses each have a test that fails when the clause is removed (mutation spot-check above).
- D-034 holds: a summary number absent from the quote returns 422 invalid_edit even with confirm_warnings=True (probe section 6).
- Batch accept on the server refuses non-entries and non-verified entries before any write (case_extras.py:24-51), and the split audit row records prompt_version split_v1 (test_split_llm.py:228).

## Not verified

- ADR-005 and ADR-015 supersession text (the brief did not ask for it).
- Eval report paths: none named in the commit, which changes no prompt, model, lexicon or schema. The commit does touch the doc that describes them, so CONTRACT 8.3 does not apply directly.

```json
{"card": "T-063", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 473ac2a (docs/LLM_VS_CODE.md row 1 and D-031..D-035 section; memory/DECISIONS.md ADR-018); code read and run at 473ac2a via git archive (HEAD moved to 636a042 during review, not used); no app URL; CLI on evals/golden/sample.txt",
 "exercised": [
  "python3 tools/board.py show T-063",
  "git show --stat 473ac2a; git show 473ac2a -- docs/LLM_VS_CODE.md memory/DECISIONS.md; git diff --stat b365af3 473ac2a",
  "git grep at 473ac2a: validate_split, LLM_SPLIT, SPLIT_REJECTED, SPLIT_AMBIGUOUS, D-031..D-035",
  "read at 473ac2a: app/backend/ingest.py, split_llm.py, schemas.py, pipeline.py, review.py, case_extras.py, narrative.py, flags.py, grounding.py, export.py, app/llm/lexicon.yaml, app/frontend/batch.js, tests/unit/test_split_llm.py",
  "git ls-tree -r --name-only {099732b,b365af3,473ac2a} | grep -c 'fixtures/llm/split/' -> 1, 0, 0",
  "clean git archive of 473ac2a; .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -rf -> 9 failed, 874 passed (artifacts/review-evidence/T-063-staff-engineer/pytest_473ac2a_clean.txt)",
  "control: pinned archive plus working-tree LLM fixtures copied in -> 5 failed, 878 passed; test_split_llm.py fully green with the split fixture restored",
  "mutation spot-check in scratch copy: drop line-start / record cap / contiguity / coverage in validate_split -> test_split_llm.py fails 1, 1, 2, 1; tree restored and diffed identical to 473ac2a",
  "artifacts/review-evidence/T-063-staff-engineer/probe_t063.py sections 1-6 (validator warnings, splitter call condition, has_self_report, lexicon_flags, manual_entry model steps, D-034 422)",
  "CLI: .venv/bin/python -m app.pipeline evals/golden/sample.txt twice in clean archive: exit 0 both, byte-identical (cli_sample_run1.txt, cli_sample_run2.txt)"
 ],
 "verdict": "fail",
 "scores": {"row1_doc_matches_code": 3, "new_section_doc_matches_code": 2, "llm_code_boundary_as_documented": 2, "split_validator_and_tests": 4, "failures_visible": 3, "tests_reproducible_at_pinned_sha": 2},
 "findings": [
  {"severity": "blocker", "title": "D-033: self-report label set on family, pronoun and subject-less statements",
   "evidence": "app/backend/grounding.py:188-198 (_self_report matches any sentence unless the exclusion regex hits); app/llm/lexicon.yaml:754-759 (patient_reports_generic); lexicon.yaml:88-89 (exclusion needs whitespace after speaker, so 'Mother: c/o neck pain.' is not excluded); flags.py:46,125 write source_kind from it. Repro: .venv/bin/python artifacts/review-evidence/T-063-staff-engineer/probe_t063.py (section 3): has_self_report=True for 'Mother: c/o neck pain.', 'She reports the pain started after the accident.', 'Complains of neck pain since the collision.'. Doc docs/LLM_VS_CODE.md:97 says label only for 'a clause that starts with an explicit patient subject plus a reporting verb'.",
   "why_it_matters": "D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) forbids labelling family, EMS or unknown statements as patient self-report; the label drives the 'Patient self-report' chip, which attributes a statement to the patient that the patient did not make. This invents attribution. Function-level repro; end-to-end path needs a flag whose excerpt matches, not run.",
   "fix": "Require an explicit patient subject (patient/pt/client) at the start of the clause plus a reporting verb; drop pronoun-only and subject-less matches for source_kind; make the speaker exclusion accept colons and punctuation; or compute the label only from clause-initial patient attribution.",
   "acceptance_test": "has_self_report is False for 'Mother: c/o neck pain.', 'She reports the pain started after the accident.', 'Complains of neck pain since the collision.'; True for 'Patient states symptoms began after the collision.' and 'Pt c/o neck pain.'. Add next to tests/unit/test_flags_pass.py:163."},
  {"severity": "major", "title": "SPLIT_REJECTED is not emitted when no model is available",
   "evidence": "docs/LLM_VS_CODE.md:29 ('If validation fails, or no model is available, ... with a SPLIT_REJECTED reason'); memory/DECISIONS.md:341 ('SPLIT_REJECTED otherwise'); app/backend/ingest.py:286-289 (SPLIT_REJECTED only when split_failure is set); app/backend/pipeline.py:166-168 (ingest_case passes no call). Repro: probe section 1: codes ['SPLIT_AMBIGUOUS', 'DATE_EXCLUDED_FROM_GAPS'] with no splitter.",
   "why_it_matters": "The doc tells an adjuster-facing reader that a missing model leaves a visible reason; the creation path leaves no reason code at all. Silent loss of the why.",
   "fix": "Emit SPLIT_REJECTED with a reason code (for example NO_MODEL) when an ambiguous single block is not sent to a model, or correct the doc and ADR-018.",
   "acceptance_test": "IN.ingest(TEXT) with no splitter returns a SPLIT_REJECTED warning carrying a reason; a test in tests/unit/test_split_llm.py asserts it."},
  {"severity": "major", "title": "Manual entry is documented as code only with no model, but runs judge 1",
   "evidence": "docs/LLM_VS_CODE.md:94 ('(code only) ... no model is involved'); app/backend/review.py:251 (_check_summary receives call); review.py:79-82 (judges.run_j1_meta when call is not None); app/backend/api.py:383 (call=make_call). Repro: probe section 5: 'model steps invoked by manual_entry: ['j1']'.",
   "why_it_matters": "The doc is the reviewer-facing contract for which steps are model steps. A paralegal or auditor reading row 1 and the D-031..D-035 section would believe no model touched a manual entry. The judge run is audited, so the record exists; the doc is wrong.",
   "fix": "Correct the doc to say judge 1 checks the summary against the quote for a manual entry. Keep the judge; it matches the ladder.",
   "acceptance_test": "A recording call passed to review.manual_entry records steps == ['j1']; docs/LLM_VS_CODE.md line 94 names judge 1."},
  {"severity": "major", "title": "'Not a duplicate' is documented as code only, but calls the generator and two judges",
   "evidence": "docs/LLM_VS_CODE.md:29 ('A reviewer can mark two merged amounts 'not a duplicate' (code only, logged)'); memory/DECISIONS.md:341 ('not a duplicate ... are code-only'); app/backend/review.py:300-306 (generator.extract_one and judge_entries when call is set); review.py:320-321 (judges_for -> judges.judge_amounts); api.py:396 (call=make_call). Read from code; not run end to end.",
   "why_it_matters": "Same as the manual-entry finding: the documented LLM boundary is wrong for a user action. The action also works on an entry and record (review.py:276-288), not on 'two merged amounts', so the doc describes a different unit.",
   "fix": "Correct the doc and ADR-018 to describe the generator and judge calls, or remove them. Fix the unit wording.",
   "acceptance_test": "Split a two-record merged entry with a recording call; the steps recorded match the doc's list."},
  {"severity": "major", "title": "Narrative: doc says code splits the paragraph into sentences; the model returns them",
   "evidence": "docs/LLM_VS_CODE.md:95 ('Code splits it into sentences and checks every sentence'); app/backend/schemas.py:69-76 (NarrativeOutput.sentences with entry_id per sentence); app/backend/narrative.py:82 (sents read from model output; no splitter in narrative.py); narrative.py:87-108 (per-sentence checks do run).",
   "why_it_matters": "Who decides sentence boundaries changes what the per-sentence check protects. The checks still run on each returned sentence, so the exposure is contained, but the doc describes a different design than the code.",
   "fix": "Either split the returned paragraph in code, or change the doc to say the model returns sentences and code checks each one.",
   "acceptance_test": "A model reply with one sentence citing entry e1 that contains a figure appearing only in e2 is removed with SUMMARY_TOKEN_NOT_IN_EXCERPT (narrative.py:55)."},
  {"severity": "major", "title": "D-032 scope: code suppresses the whole objective_negative category, including credibility-attack phrases the doc does not mention",
   "evidence": "docs/LLM_VS_CODE.md:97 ('Normal or negative findings ... are context only'); app/backend/flags.py:14, :78, :107 (drops every objective_negative hit); app/llm/lexicon.yaml:852-858 ('out of proportion', 'no objective findings') and :1159-1166 (symptom_magnification: Waddell, malingering, exaggerat, secondary gain). Repro: probe section 4: 0 flags for 'Waddell signs positive 3/5.' and 'Patient exhibits symptom magnification and secondary gain.'. memory/ORCHESTRATOR_DECISIONS.md:40 names the category objective_negative.",
   "why_it_matters": "Either the doc understates what D-032 suppresses or the code suppresses flags D-018 meant to keep. Silent suppression of a credibility flag is a quiet loss of a finding the adjuster may need.",
   "fix": "Chris to decide. Then make doc and code agree: either suppress only normal/negative entries (split the category), or state in the doc that the whole category is context-only.",
   "acceptance_test": "The chosen behaviour is asserted for 'Waddell signs positive 3/5.' and 'Full cervical ROM.' in tests/unit/test_flags_pass.py."},
  {"severity": "major", "title": "The test file the AC names is red at the pinned sha: split replay fixture deleted in b365af3",
   "evidence": "git ls-tree -r --name-only 099732b | grep -c 'fixtures/llm/split/' = 1; b365af3 = 0; 473ac2a = 0; git show --stat b365af3 -- tests/fixtures/llm/split deletes one file. Clean run: artifacts/review-evidence/T-063-staff-engineer/pytest_473ac2a_clean.txt: 9 failed, 874 passed. Failing in tests/unit/test_split_llm.py: test_golden_unsplit_paste_replays_recorded_split_through_audited, test_run_pipeline_replaces_the_single_stored_record, test_split_audit_row_has_prompt_version_and_flag_resolves_to_call. Other six: test_t037_backend.py x3, test_narrative.py replay, test_case_extras.py batch x2.",
   "why_it_matters": "The AC and row 1 name test_split_llm.py as evidence for accepted and rejected splits, and three of its tests cannot run on the commit. The doc diff added no code, so the red tests predate this commit, but T-063 cites them. Pass counts must be reproducible from a clean checkout.",
   "fix": "Restore a re-recorded split fixture under tests/fixtures/llm/split; re-run from a clean git archive; record the counts on the card. The other six are pre-existing judge-replay misses and need their own card.",
   "acceptance_test": "git archive 473ac2a | tar -x -C <dir>; cd <dir>; .venv/bin/python -m pytest tests/unit/test_split_llm.py -q reports 0 failures (after the fixture is restored on the branch under review)."},
  {"severity": "major", "title": "Batch accept: UI fallback on 404/405 bypasses the server's verified-only check (latent)",
   "evidence": "app/frontend/batch.js:17-19 (on 404/405 runs one per-item accept per eligible id; no message); app/backend/case_extras.py:24-51 (verified-only check exists only on the batch route); app/backend/review.py:48-49 (per-item accept blocks only rejected items); app/backend/api.py:459 (route registered, so the fallback is not reachable on this server).",
   "why_it_matters": "A silent fallback that changes which guard runs is the persona's section 5 pattern. Not reachable today, so major rather than blocker; it becomes a blocker the moment the route is missing in a deployment.",
   "fix": "Delete the fallback, or show an error and accept nothing on a 404/405.",
   "acceptance_test": "A stub 404 on /review/batch leaves every entry unchanged and shows an error to the user."},
  {"severity": "minor", "title": "Model is called for a single recognised but incomplete block",
   "evidence": "docs/LLM_VS_CODE.md:94-95 and row 1 ('only when the code split leaves one unsplit block'); app/backend/ingest.py:262 (condition is single record AND (unsplit OR missing date or source)). Repro: probe section 2 case C: splitter called=True; case A: False.",
   "why_it_matters": "The doc's trigger is narrower than the code's; a reader auditing model use would be wrong about when it runs.",
   "fix": "Align the doc with the condition, or change the condition to match the doc.",
   "acceptance_test": "One ingest case per branch (unsplit, incomplete with source, incomplete without source) asserts whether the splitter ran."},
  {"severity": "minor", "title": "Broad except in the shared judge path swallows the error class",
   "evidence": "app/backend/review.py:83-84 (except Exception: verdict = 'unavailable').",
   "why_it_matters": "The state is visible (JUDGE_UNAVAILABLE), so this is not a silent fallback. The error class and call id are lost, and the new manual-entry path inherits it.",
   "fix": "Catch the provider errors the judge can raise and let anything else propagate, logged with the call id.",
   "acceptance_test": "A non-provider exception raised by the judge propagates out of review.manual_entry."},
  {"severity": "minor", "title": "Narrative wording: 'from an accepted entry' and 'marked'",
   "evidence": "docs/LLM_VS_CODE.md:95 ('each number ... must come from an accepted entry'; 'is marked and cannot be accepted'); app/backend/narrative.py:54 (checks the cited entry's quote, which is stricter and correct); narrative.py:96-97 (failing sentences move to removed[]).",
   "why_it_matters": "The doc understates the check and misnames the outcome. Code is correct; the doc should match it.",
   "fix": "Reword the doc to 'must come from the cited entry's quote' and 'removed, with a reason'.",
   "acceptance_test": "Doc review only; the existing narrative tests cover the behaviour."},
  {"severity": "nit", "title": "Batch accept: 'after she confirms the count' describes a step the UI does not have",
   "evidence": "docs/LLM_VS_CODE.md:96; app/frontend/batch.js (button label carries the count; a single click calls acceptAll; no confirm step).",
   "why_it_matters": "Wording only; the count is shown on the button.",
   "fix": "Reword, or add the confirm step if Chris wants one.",
   "acceptance_test": "None needed."}
 ],
 "whats_right": [
  "validate_split's four clauses (coverage, contiguity, line starts, record cap) each fail a test when removed (mutation spot-check on a scratch copy of 473ac2a)",
  "D-034 holds: a summary figure absent from the quote returns 422 invalid_edit even with confirm_warnings=True (probe section 6)",
  "Batch accept on the server refuses non-entries and non-verified entries before any write (case_extras.py:24-51), and the split audit row records prompt_version split_v1"
 ],
 "questions_for_chris": [
  "D-032 scope: should symptom magnification, Waddell, malingering and 'out of proportion' (lexicon objective_negative, lexicon.yaml:852 and :1159) stay suppressed as context-only, or go back to causation flags as D-018 had them? The doc and the code disagree on this.",
  "Manual entry (judge 1) and not-a-duplicate (generator and judges) both call a model. I recommend keeping the calls and correcting the doc. Confirm, or tell me the calls should be removed.",
  "D-033 lists 'Pt c/o' as explicit patient attribution. Should a bare 'C/O neck pain' with no subject also get the label? I did not flag it, because it is ambiguous."
 ]}
```
