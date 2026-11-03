# T-063 round 2: staff-engineer-reviewer

Scope: docs/LLM_VS_CODE.md and memory/DECISIONS.md at commit 1855b76 (round-1 fixes), checked against code pinned to git archive 373f8b1. HEAD moved to f201e3b0 during the review; the delta was checked and touches none of the cited claims except the D-039 re-run freeze, which the doc does not describe.

Verdict: **changes**. No blockers. Two majors, four minors. The round-1 blocker (D-033) is resolved and the code matches the doc on every round-1 item except the stale statements listed below.

## Round-1 findings, status at HEAD

| R1 | Severity in R1 | Status at HEAD | Evidence |
|---|---|---|---|
| B1 D-033 self-report label | blocker | Resolved. Doc now states D-037; code matches every doc-cited case. Superseded by D-040 (see F2). | probe section 3: 18/18 rows match the documented rule |
| M1 SPLIT_REJECTED with no model | major | Code fixed (T-066, e7c1912). Doc text is stale (F3). | probe section 1 |
| M2 manual entry runs judge 1 | major | Resolved. Doc matches. | probe 6b steps ['j1']; review.py:79-82, 251 |
| M3 not-a-duplicate calls models | major | Resolved in substance. Warning wording does not match the doc (F5). | review.py:300-321; probe 6a |
| M4 narrative sentences from model | major | Resolved. Doc matches. | narrative.py:90, 102-119; probe 5 |
| M5 D-032 scope | major, question for Chris | Doc matches code, but D-038 answered the question (F1). | D-038 at ORCHESTRATOR_DECISIONS.md:46 |
| M6 split test red at pinned sha | major | Resolved. Fixture present; test_split_llm.py 31 passed at 373f8b1. | `git ls-tree` count 1; pytest run |
| M7 batch UI fallback | major, latent | Code fixed (T-065, 5900040). Doc still calls it a live defect (F4). | batch.js:17-19 |
| m1 splitter trigger | minor | Resolved. Doc matches. | probe section 2, cases A to D |
| m2 broad except review.py:83-84 | minor | Open. Code unchanged, no doc claim, no card (F6). | review.py:83-84 |
| m3 narrative wording | minor | Resolved. Doc matches. | narrative.py:55-119 |
| n1 "confirms the count" | nit | Resolved. Doc says count on button, no confirm step. | batch.js:42-49 |

## Findings

- **F1 (major).** Doc and ADR still present the credibility-phrase suppression as an open question. D-038 (memory/ORCHESTRATOR_DECISIONS.md:46) says those phrases raise a flag. Card T-067 is ready and open. The code gap (flags.py:14, 78, 107) belongs to T-067 and is not charged to T-063.
- **F2 (major).** D-040 (memory/ORCHESTRATOR_DECISIONS.md:48 at f201e3b0, commit 8b2001e, after 1855b76) cuts the patient self-report chip and supersedes D-037. The doc (lines 41 and 100), ADR-018 and DECISIONS.md:286 still describe the D-037 label as current. The code still sets it (flags.py:46, 125; present.py:46; flags.js:63 renders it). No card implements D-040. The code removal is not charged to T-063.
- **F3 (minor).** Row 1 says a no-model paste emits only SPLIT_AMBIGUOUS. HEAD emits SPLIT_REJECTED with reason NO_MODEL (ingest.py:263-264, 294-296).
- **F4 (minor).** Doc says the batch-accept 404/405 fallback exists and is a known defect. batch.js:17-19 no longer loops per item; it shows an error and accepts nothing (T-065).
- **F5 (minor).** Doc says the LLM_UNAVAILABLE warning tells her to enter the entry by hand. review.py:311 says only that the entry has not been drafted.
- **F6 (minor, carried).** review.py:83-84 still has `except Exception:` in the shared judge path. The state is visible (JUDGE_UNAVAILABLE), so it is not silent, but the error class and call id are lost. No card exists.

## Exercised

- Read personas/staff-engineer.md, reviews/T-063-staff-engineer.md, memory/ORCHESTRATOR_DECISIONS.md (D-032 to D-040), memory/DECISIONS.md:286 and :339-341, and docs/LLM_VS_CODE.md lines 29, 41, 94-100.
- `git show 1855b76 -- docs/LLM_VS_CODE.md memory/DECISIONS.md` (the round-1 fix diff); `git show 6707a12 --stat`; `git show 8b2001e --stat`.
- `git merge-base --is-ancestor` for 1855b76, 5900040, e7c1912, 991dac4, 31070c3, 6707a12 against HEAD: all yes.
- `git ls-tree -r --name-only` for the split fixture at 1855b76 and HEAD: 1 file each.
- `python3 tools/board.py show T-063`, `show T-065`, `show T-066`, `show T-067`.
- `git archive 373f8b1 | tar -x` into artifacts/review-evidence/T-063-staff-engineer-r2/head-373f8b1de2a8553738eed2f0f390a15a016e2ac7; `.venv/bin/python -m pytest tests/unit/test_split_llm.py -q` gave 31 passed.
- probe artifacts/review-evidence/T-063-staff-engineer-r2/probe_t063_r2.py (sections 1 to 5, 6b), output in probe_t063_r2_output.txt; probe_t063_r2_nd.py (section 6a, not_duplicate), output in probe_t063_r2_nd_output.txt.
- Code read at 373f8b1: grounding.py:180-234; ingest.py:254-296; pipeline.py:177-184; review.py:62-97, 226-331, 342-347; case_extras.py:17-62; narrative.py:41-119; flags.py:12-15, 78, 107; batch.js:1-62; lexicon.yaml:852-858, 1159-1168.
- HEAD delta: `git log --oneline 373f8b1..f201e3b0`; `git diff --stat 373f8b1 f201e3b0 -- app docs memory`; `git diff 373f8b1 f201e3b0 -- app/backend/pipeline.py`; `git grep -n 'self-report\|patient_report' f201e3b0 -- app/frontend app/backend/flags.py app/backend/present.py`.
- Not run: eval runner, CLI, browser UI, HTTP routes, full unit suite. The doc does not describe the D-039 freeze; not checked, because the brief did not ask for it.

```json
{"card": "T-063", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "docs/LLM_VS_CODE.md and memory/DECISIONS.md at 1855b76 (round-1 fixes); code at git archive 373f8b1; HEAD moved to f201e3b0 during review (delta checked, no cited claim changed except D-039 re-run freeze, not described in doc); no app URL; no CLI run",
 "exercised": [
  "read personas/staff-engineer.md; reviews/T-063-staff-engineer.md; memory/ORCHESTRATOR_DECISIONS.md D-032..D-040; memory/DECISIONS.md:286, 339-341; docs/LLM_VS_CODE.md lines 29, 41, 94-100",
  "git show 1855b76 -- docs/LLM_VS_CODE.md memory/DECISIONS.md; git show 6707a12 --stat; git show 8b2001e --stat",
  "git merge-base --is-ancestor 1855b76|5900040|e7c1912|991dac4|31070c3|6707a12 HEAD -> all yes",
  "git ls-tree -r --name-only 1855b76|HEAD | grep -c fixtures/llm/split/ -> 1, 1",
  "python3 tools/board.py show T-063; show T-065; show T-066; show T-067",
  "git archive 373f8b1 | tar -x -C artifacts/review-evidence/T-063-staff-engineer-r2/head-373f8b1de2a8553738eed2f0f390a15a016e2ac7; .venv/bin/python -m pytest tests/unit/test_split_llm.py -q -> 31 passed",
  "artifacts/review-evidence/T-063-staff-engineer-r2/probe_t063_r2.py sections 1-5 and 6b (probe_t063_r2_output.txt)",
  "artifacts/review-evidence/T-063-staff-engineer-r2/probe_t063_r2_nd.py section 6a not_duplicate (probe_t063_r2_nd_output.txt)",
  "code read at 373f8b1: grounding.py:180-234; ingest.py:254-296; pipeline.py:177-184; review.py:62-97, 226-331, 342-347; case_extras.py:17-62; narrative.py:41-119; flags.py:12-15, 78, 107; app/frontend/batch.js:1-62; app/llm/lexicon.yaml:852-858, 1159-1168",
  "HEAD delta: git log --oneline 373f8b1..f201e3b0; git diff --stat 373f8b1 f201e3b0 -- app docs memory; git diff 373f8b1 f201e3b0 -- app/backend/pipeline.py; git grep -n 'self-report|patient_report' f201e3b0 -- app/frontend app/backend/flags.py app/backend/present.py",
  "not run: eval runner, CLI, browser UI, HTTP routes, full unit suite"
 ],
 "verdict": "changes",
 "scores": {"round1_blocker_resolved": 5, "doc_matches_code_at_head": 3, "doc_reflects_binding_decisions": 2, "failures_visible_in_doc": 4, "tests_reproducible_at_pinned_sha": 5},
 "findings": [
  {"severity": "major", "title": "Doc and ADR present credibility-phrase suppression as an open question; D-038 already decided it",
   "evidence": "docs/LLM_VS_CODE.md:41 ('credibility wording such as \"out of proportion\" are context only, see D-032 below'); docs/LLM_VS_CODE.md:99 ('Whether to split the category so credibility wording flags again is a question for Chris'); memory/DECISIONS.md:341 ('open question for Chris'); memory/ORCHESTRATOR_DECISIONS.md:46 (D-038: credibility phrases 'raise a flag'); probe_t063_r2_output.txt section 4: 0 flags for 'Waddell signs positive 3/5.', 'Subjective complaints out of proportion to exam findings.', 'No objective findings.', 'Patient exhibits symptom magnification and secondary gain.', 'Inconsistent effort noted on grip testing.'; 0 for 'Full cervical ROM.' and 'Negative for fracture.' (correct under D-032). Code gap: app/backend/flags.py:14, 78, 107 drop the whole objective_negative category; card T-067 is ready and unclaimed.",
   "why_it_matters": "The doc is the reader's contract for what is flagged. It presents a decided rule as an open question and states a suppression as design that D-038 reverses. The 'no flag at HEAD' sentence is true today and will be false after T-067 lands unless the doc is updated. The code gap is T-067's scope and is not charged to T-063; if T-067 is not landed before the M3 gate, the suppression becomes a D.2 blocker against the code.",
   "fix": "Rewrite row 13 and the D-032 sub-bullet: normal or negative findings are context only (D-032); credibility phrases from the lexicon raise a flag (D-038, card T-067). Keep 'no flag at HEAD until T-067 lands' as a dated note. Delete the 'question for Chris' sentence at line 99 and the matching text at memory/DECISIONS.md:341.",
   "acceptance_test": "After T-067 lands: probe_t063_r2.py section 4 prints at least one flag for 'Waddell signs positive 3/5.' and for 'Subjective complaints out of proportion to exam findings.', and 0 for 'Full cervical ROM.'; grep -n 'question for Chris' docs/LLM_VS_CODE.md returns no line about credibility wording."},
  {"severity": "major", "title": "D-040 cut the patient self-report chip; doc, ADR and code still describe the D-037 label as current",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:48 at f201e3b0 (D-040: 'Cut the patient_report self-report chip (supersedes D-033/D-035/D-037, 2026-11-02)... No code or model labels who is speaking'), committed in 8b2001e after 1855b76. docs/LLM_VS_CODE.md:41 ('Whether an excerpt gets the patient self-report label is set by code (rule D-037...)') and :100 (D-037 'binding' sub-bullet). memory/DECISIONS.md:286 and :341 ('D-037 is the binding rule'). Code unchanged at f201e3b0: app/backend/flags.py:46, 125; app/backend/present.py:46; app/backend/grounding.py:190 (patient_report_spans); app/frontend/flags.js:63 renders 'Patient self-report'. No board card implements D-040.",
   "why_it_matters": "The brief names D-037 as binding; D-040 is a later decision that supersedes it. The doc now states a speaker-labelling rule that the orchestrator has cut, and the code still applies it, with no card that owns the removal. This card's doc is the wrong side of that divergence; the code removal is not charged to T-063.",
   "fix": "Doc: replace the D-037 sub-bullet (line 100) and the label clause in row 13 with 'the patient self-report chip is cut (D-040); every excerpt is shown verbatim with its source label'. Same in ADR-018 and memory/DECISIONS.md:286. Orchestrator: file a card for the code removal (grounding.patient_report_spans, flags.py:46 and 125, present.py:46, flags.js:63, and the tests that assert the label) and link it from T-063.",
   "acceptance_test": "docs/LLM_VS_CODE.md has no sentence saying a label is set by code; the card for the code removal exists on the board; after it lands, git grep -n 'patient_report' over app/ returns no producer."},
  {"severity": "minor", "title": "Row 1 says a no-model paste emits only SPLIT_AMBIGUOUS; HEAD emits SPLIT_REJECTED with reason NO_MODEL",
   "evidence": "docs/LLM_VS_CODE.md:29 ('When no model is wired in at all (the case-creation path today), only SPLIT_AMBIGUOUS is emitted and the reason is not shown; that gap is card T-066'); memory/DECISIONS.md:341 (same). app/backend/ingest.py:263-264 (split_failure = 'NO_MODEL'), :294-296 (SPLIT_REJECTED 'No model was available to propose record boundaries'); app/backend/pipeline.py:177-179 (ingest_case passes no call). probe_t063_r2_output.txt section 1: codes SPLIT_AMBIGUOUS, SPLIT_REJECTED, DATE_EXCLUDED_FROM_GAPS. T-066 (e7c1912) is an ancestor of HEAD.",
   "why_it_matters": "The doc states as current a gap the code no longer has. Naming an open card is acceptable; saying the reason is 'not shown' is false at HEAD. It understates shipped behaviour; no reader is misled about a model step or an attribution.",
   "fix": "Replace the sentence with: 'With no model wired in, the paste stays one record flagged SPLIT_AMBIGUOUS with SPLIT_REJECTED (reason NO_MODEL) (T-066, in review).' Same in memory/DECISIONS.md:341.",
   "acceptance_test": "probe_t063_r2.py section 1 prints SPLIT_REJECTED with NO_MODEL; grep -n 'only SPLIT_AMBIGUOUS is emitted' docs/LLM_VS_CODE.md returns nothing."},
  {"severity": "minor", "title": "Doc calls the batch-accept 404/405 fallback a live known defect; the fallback is removed",
   "evidence": "docs/LLM_VS_CODE.md:97 ('The front end still has a fallback that, on a 404/405 from the batch route, accepts item by item ... card T-065 removes it, and until then it is a known defect'); memory/DECISIONS.md:341 ('the UI 404/405 fallback that skips the check is T-065'). app/frontend/batch.js:17-19 at 373f8b1: on 404/405 it shows 'Accept all could not run on this server, so nothing was accepted' and returns; no per-item loop. T-065 (5900040) is an ancestor of HEAD.",
   "why_it_matters": "Same pattern as F3: the doc describes a bypass the code now refuses. A reader auditing the batch path would look for a defect that is closed.",
   "fix": "Delete the 'still has a fallback' sentence and write: 'on a 404 or 405 the UI shows an error and accepts nothing (T-065).' Same in memory/DECISIONS.md:341.",
   "acceptance_test": "tests/e2e/test_edit.py::test_batch_accept_route_missing_accepts_nothing passes at HEAD (card evidence; not re-run here); grep -n 'still has a fallback' docs/LLM_VS_CODE.md returns nothing."},
  {"severity": "minor", "title": "Doc says the LLM_UNAVAILABLE warning tells her to enter the record by hand; the message does not",
   "evidence": "docs/LLM_VS_CODE.md:95 ('With no model available, the entry is not drafted and a LLM_UNAVAILABLE warning tells her to enter it by hand'). app/backend/review.py:311 (message 'The record was split off; its entry has not been drafted yet.'). probe_t063_r2_nd_output.txt: 'warning LLM_UNAVAILABLE | The record was split off; its entry has not been drafted yet.' (the 'enter it by hand' text is only on the generator-failure branch, review.py:307-308).",
   "why_it_matters": "The doc promises an instruction the paralegal does not receive. Wording only; the manual entry route exists.",
   "fix": "Either add 'enter it by hand if needed' to the review.py:311 message, or change the doc to 'a LLM_UNAVAILABLE warning says the entry has not been drafted'.",
   "acceptance_test": "probe_t063_r2_nd.py output contains the chosen wording and matches the doc sentence."},
  {"severity": "minor", "title": "Broad except in the shared judge path still swallows the error class (carried from round 1, no card)",
   "evidence": "app/backend/review.py:83-84 at 373f8b1: 'except Exception:' then 'verdict, call_id = \"unavailable\", None'. Doc makes no claim about it.",
   "why_it_matters": "The state is visible (JUDGE_UNAVAILABLE), so this is not a silent fallback. The error class and call id are lost on the path that manual entry and not-a-duplicate use. Not a doc mismatch; listed so it is not dropped, because no card exists.",
   "fix": "Catch only the provider error classes the judge call can raise; let anything else propagate, logged with the call id. Orchestrator: file a card.",
   "acceptance_test": "A non-provider exception raised by the judge call propagates out of review.manual_entry (unit test to add under tests/unit)."}
 ],
 "whats_right": [
  "Split trigger text matches ingest.py: the splitter runs for a single unsplit or incomplete block and not for a block with both labels (probe section 2, cases A to D)",
  "Narrative text matches narrative.py: the model returns sentences, code checks each against the cited entry's quote, and failing sentences are removed with a reason (probe section 5)",
  "Batch accept text matches batch.js and case_extras.py: all-or-nothing, verified pending entries only, count on the button, no confirm step, Undo"
 ],
 "questions_for_chris": [
  "D-040 (8b2001e) cuts the self-report chip and supersedes D-037. This review treats D-040 as binding for the doc. Confirm that it removes the chip entirely and does not keep the label for a narrower case.",
  "Should the LLM_UNAVAILABLE warning say 'enter it by hand' (F5), or is the doc sentence simply to be reworded? Wording only; either choice is acceptable."
 ]}
```
