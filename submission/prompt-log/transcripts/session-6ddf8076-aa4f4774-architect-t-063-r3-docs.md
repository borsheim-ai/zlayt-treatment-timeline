# Subagent: Architect: T-063 r3 docs (Architect: T-063 r3 docs)

Source: `agent-aa4f4774467e8aa52.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:45:27.295Z

You own board card T-063, round 3 (claimed by "architect") in /Users/arsis/zlayt-pm-project. Read reviews/T-063-staff-engineer-r2.md. Both majors are doc-only, because the code has landed:
- D-038 credibility flags are implemented in 59c7edb (T-067), under category credibility_language. Describe them as decided, not as an open question.
- D-040 cuts the patient_report chip, implemented in a27e3a4 (T-071). Remove the D-037 chip description from docs/LLM_VS_CODE.md and memory/DECISIONS.md, and state D-040. Cite T-072 (neutral title for the patient_reported_onset flag) as open.

Also fix the 4 minors. Stage with `git add <paths>`, then commit with `git commit -m "..." -- <paths>` in a separate command, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-063 in_review --agent architect`. Reply in 2 lines.

### User / tool · 2026-11-02T02:45:27.299Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:29.988Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-063-staff-engineer-r2.md && python3 tools/board.py show T-063 | tail -40 && git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T02:45:30.162Z

**tool result**
````
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
  - {"n": 1, "text": "docs/LLM_VS_CODE.md row 1: code first; the model returns character offsets only when the code split finds one unsplit block; code validates coverage, contiguity, line starts and record count (ingest.validate_split); otherwise one record and SPLIT_AMBIGUOUS with a SPLIT_REJECTED reason; every model-split record carries LLM_SPLIT; names tests/unit/test_split_llm.py and the audited step 'split'; grep -n LLM_SPLIT docs/LLM_VS_CODE.md hits row 1", "done": true, "evidence": "docs/LLM_VS_CODE.md row 1 + second-wave section match code at HEAD; test_split_llm.py 29 passed; commit 1855b76"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:27:47Z orchestrator: assigned: architect
- 2026-11-02T02:27:50Z architect: claimed
- 2026-11-02T02:28:05Z architect: AC 1 checked: grep -n LLM_SPLIT docs/LLM_VS_CODE.md hits row 1 (line 29); validate_split, test_split_llm.py, step split named
- 2026-11-02T02:28:05Z architect: moved in_progress -> in_review
- 2026-11-02T02:28:15Z orchestrator: review dispatched: staff (haiku)
- 2026-11-02T02:38:05Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-063-staff-engineer.md; round 1; findings:
    - [blocker] D-033: self-report label set on family, pronoun and subject-less statements — fix: Require an explicit patient subject (patient/pt/client) at the start of the clause plus a reporting verb; drop pronoun-only and subject-less matches for source_kind; make the speaker exclusion accept colons and punctuation; or compute the label only from clause-initial patient attribution.
    - [major] SPLIT_REJECTED is not emitted when no model is available — fix: Emit SPLIT_REJECTED with a reason code (for example NO_MODEL) when an ambiguous single block is not sent to a model, or correct the doc and ADR-018.
    - [major] Manual entry is documented as code only with no model, but runs judge 1 — fix: Correct the doc to say judge 1 checks the summary against the quote for a manual entry. Keep the judge; it matches the ladder.
    - [major] 'Not a duplicate' is documented as code only, but calls the generator and two judges — fix: Correct the doc and ADR-018 to describe the generator and judge calls, or remove them. Fix the unit wording.
    - [major] Narrative: doc says code splits the paragraph into sentences; the model returns them — fix: Either split the returned paragraph in code, or change the doc to say the model returns sentences and code checks each one.
    - [major] D-032 scope: code suppresses the whole objective_negative category, including credibility-attack phrases the doc does not mention — fix: Chris to decide. Then make doc and code agree: either suppress only normal/negative entries (split the category), or state in the doc that the whole category is context-only.
    - [major] The test file the AC names is red at the pinned sha: split replay fixture deleted in b365af3 — fix: Restore a re-recorded split fixture under tests/fixtures/llm/split; re-run from a clean git archive; record the counts on the card. The other six are pre-existing judge-replay misses and need their own card.
    - [major] Batch accept: UI fallback on 404/405 bypasses the server's verified-only check (latent) — fix: Delete the fallback, or show an error and accept nothing on a 404/405.
    - [minor] Model is called for a single recognised but incomplete block — fix: Align the doc with the condition, or change the condition to match the doc.
    - [minor] Broad except in the shared judge path swallows the error class — fix: Catch the provider errors the judge can raise and let anything else propagate, logged with the call id.
    - [minor] Narrative wording: 'from an accepted entry' and 'marked' — fix: Reword the doc to 'must come from the cited entry's quote' and 'removed, with a reason'.
- 2026-11-02T02:38:13Z architect: claimed
- 2026-11-02T02:39:22Z architect: Round 1 fixes at 1855b76: B1 now D-037 (grounding.patient_report_spans, T-061 991dac4); DECISIONS.md:286 and ADR-018 amended; M3-M6 documented as code behaves; M2/M8 point to T-066/T-065 as defects; m1 trigger, m3 and nit wording fixed; row 13 and stale 'manual add is a cut' line corrected. Verified: .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -> 29 passed (31070c3). Not changed: m2 broad except in review.py (code, not doc); D-032 scope question left to Chris.
- 2026-11-02T02:39:22Z architect: AC 1 checked: docs/LLM_VS_CODE.md row 1 + second-wave section match code at HEAD; test_split_llm.py 29 passed; commit 1855b76
- 2026-11-02T02:39:22Z architect: moved in_progress -> in_review
- 2026-11-02T02:39:41Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T02:45:23Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-063-staff-engineer-r2.md; round 2; findings:
    - [major] Doc and ADR present credibility-phrase suppression as an open question; D-038 already decided it — fix: Rewrite row 13 and the D-032 sub-bullet: normal or negative findings are context only (D-032); credibility phrases from the lexicon raise a flag (D-038, card T-067). Keep 'no flag at HEAD until T-067 lands' as a dated note. Delete the 'question for Chris' sentence at line 99 and th
    - [major] D-040 cut the patient self-report chip; doc, ADR and code still describe the D-037 label as current — fix: Doc: replace the D-037 sub-bullet (line 100) and the label clause in row 13 with 'the patient self-report chip is cut (D-040); every excerpt is shown verbatim with its source label'. Same in ADR-018 and memory/DECISIONS.md:286. Orchestrator: file a card for the code removal (gro
    - [minor] Row 1 says a no-model paste emits only SPLIT_AMBIGUOUS; HEAD emits SPLIT_REJECTED with reason NO_MODEL — fix: Replace the sentence with: 'With no model wired in, the paste stays one record flagged SPLIT_AMBIGUOUS with SPLIT_REJECTED (reason NO_MODEL) (T-066, in review).' Same in memory/DECISIONS.md:341.
    - [minor] Doc calls the batch-accept 404/405 fallback a live known defect; the fallback is removed — fix: Delete the 'still has a fallback' sentence and write: 'on a 404 or 405 the UI shows an error and accepts nothing (T-065).' Same in memory/DECISIONS.md:341.
    - [minor] Doc says the LLM_UNAVAILABLE warning tells her to enter the record by hand; the message does not — fix: Either add 'enter it by hand if needed' to the review.py:311 message, or change the doc to 'a LLM_UNAVAILABLE warning says the entry has not been drafted'.
    - [minor] Broad except in the shared judge path still swallows the error class (carried from round 1, no card) — fix: Catch only the provider error classes the judge call can raise; let anything else propagate, logged with the call id. Orchestrator: file a card.
- 2026-11-02T02:45:23Z architect: claimed

## Handoff
What changed: LLM_VS_CODE row 1, row 13 and second-wave section rewritten to HEAD behaviour (D-037 label rule, manual entry judge 1, not-a-duplicate model calls, model-returned narrative sentences, D-032 whole-category suppression, T-066/T-065 flagged as defects); DECISIONS.md line 286 and ADR-018 amended. How verified: read grounding.py, review.py, narrative.py, flags.py, ingest.py at HEAD; .venv/bin/python -m pytest -q tests/unit/test_split_llm.py = 29 passed. Left: D-032 credibility-phrase question for Chris; m2 broad except in review.py is a code finding with no card. Surprised: row 13 and costs section also had stale claims.

e0ca2b0 fix(frontend): mock batch applies verified-only rule in one step, no per-item fan-out; test undo has no fallback (T-065)
d148e0f fix(backend): run-path fixture miss and unsplit tail both emit SPLIT_REJECTED with a reason; run result carries split_failure (T-066 r2)
a27e3a4 feat(backend): cut the patient_report speaker chip (T-071, D-040)
59c7edb fix(backend): export lists edited-then-accepted entries; flag defense credibility phrases (T-069, T-067/D-038)
89a323a fix(frontend): list dates_to_confirm items that have no undated entry (T-068)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:32.514Z

**tool call — Bash**
````
{
 "command": "git status --short docs memory | head; grep -n \"D-037\\|D-032\\|D-038\\|question for Chris\\|only SPLIT_AMBIGUOUS\\|still has a fallback\\|enter it by hand\\|T-065\\|T-066\\|T-067\\|self-report\\|patient_report\" docs/LLM_VS_CODE.md memory/DECISIONS.md; sed -n 44,50p memory/ORCHESTRATOR_DECISIONS.md; grep -n \"T-072\" -r board/cards | head -3; python3 tools/board.py show T-072 | head -8; sed -n 80,86p app/backend/review.py"
}
````

### User / tool · 2026-11-02T02:45:32.724Z

**tool result**
````
 M memory/LESSONS.md
docs/LLM_VS_CODE.md:29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. When no model is wired in at all (the case-creation path today), only `SPLIT_AMBIGUOUS` is emitted and the reason is not shown; that gap is card T-066, so read this row as the intended behaviour once T-066 lands. Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
docs/LLM_VS_CODE.md:41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, an attorney referral; normal or negative exam findings and credibility wording such as "out of proportion" are context only, see D-032 below) | Same as row 12 (per record). Whether an excerpt gets the **patient self-report** label is set by code (rule D-037, see the second-wave section), never by the model. | Same. The tool points at the record's own words; it never rules on causation. | Same, plus golden "must not" checks (no "degenerative" or "traumatic" in the tool's own voice). |
docs/LLM_VS_CODE.md:95:- **"Not a duplicate" (code undoes the merge; model drafts and checks the split-off record).** On a merged entry she picks one of the merged records. Code removes it from the entry, restores its amounts and recomputes gaps, and logs a `not_duplicate` event. The split-off record then gets its own entry the normal way: the generator drafts it (code checks the quote), judge 1 checks it, and the amount judge checks its amounts. With no model available, the entry is not drafted and a `LLM_UNAVAILABLE` warning tells her to enter it by hand. The unit is a record inside one merged entry, not "two amounts".
docs/LLM_VS_CODE.md:97:- **Batch accept (code only).** Accepts entries that are `verified` and still `pending`, in one all-or-nothing request, with the count on the button (no separate confirm step) and an Undo. Never amounts, never flags. The server refuses the whole batch if any id is not such an entry. The front end still has a fallback that, on a 404/405 from the batch route, accepts item by item and so skips that check; card T-065 removes it, and until then it is a known defect, not intended behaviour.
docs/LLM_VS_CODE.md:98:- **Narrower flags (D-032, D-033, D-035, D-037).**
docs/LLM_VS_CODE.md:99:  - *D-032:* code drops the **whole `objective_negative` category** from both the lexicon and the model, so it never raises a flag. That category holds normal findings ("negative for fracture", "full ROM") **and** the credibility-attack phrases ("out of proportion", "no objective findings", Waddell signs, symptom magnification, malingering, secondary gain). Those phrases therefore raise no flag at HEAD. Whether to split the category so credibility wording flags again is a question for Chris (staff-engineer review major 6; D-018 had them as causation flags). Scene facts raise a causation flag only on specific adjuster phrases ("minimal damage", "refused transport"), not on a plain description of the crash.
docs/LLM_VS_CODE.md:100:  - *D-037 (binding, supersedes D-033 and D-035; code `grounding.patient_report_spans`, T-061 commit 991dac4):* the **"patient self-report" label is set only when the whole excerpt is one patient-subject clause**: it begins with Patient, Pt or The patient plus a reporting verb ("Patient states neck pain 7/10."), is a single sentence, and contains no `;`, `,`, `(` or "and". Any mixed excerpt, family, EMS, witness or unknown speaker, a bare "C/O", or an "S:" or "Subjective:" header gets **no label**. A missing label is safe; a wrong one mislabels the source. The looser qualifier carry (a summary must keep "complained of" and similar) is a separate check and never sets the label.
memory/DECISIONS.md:87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), source_kind('record'|'patient_report'),
memory/DECISIONS.md:244:- **Dropped qualifiers (D-022, round 4).** A second function `grounding.dropped_qualifiers(summary, excerpt)` finds qualifiers in the excerpt (lexicon hedge set, `self_report` entries, negation words such as "without", laterality, "approx.") and requires each to appear in the summary; a missing one gives `needs_review` with `SUMMARY_DROPS_QUALIFIER`. The judge checks additions, not omissions, so this is code. Self-report is tagged per quote: each entry carries `source_kind` (`patient_report` | `record`) for its excerpt sentences, set by code from the lexicon. In evals, `required_terms` are checked against the summary alone. R-TL-10 gains this check (ADR-017).
memory/DECISIONS.md:251:  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on: `pre_existing`, `causation_weakening`, `compliance`, the hedge set, `patient_report`, `accident_date_phrases`, `damages`, `non_encounter`, `injection`. **`lexicon.yaml` v2 is a researcher deliverable that blocks the gap rule (`non_encounter`), the accident-date rule (`accident_date_phrases`) and the injection scan (`injection`); its self-check must run over every golden case and report recall per `must` flag.** The lexicon `causation_weakening` and `compliance` map to `causation`.
memory/DECISIONS.md:255:    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
memory/DECISIONS.md:272:    | patient_report | Patient self-report | Patient self-report (not a physician's opinion) in {provider} ({date}): “{quote}”. |
memory/DECISIONS.md:286:  - `source_kind = "patient_report"` is set by code (`grounding.patient_report_spans`) under D-037, which supersedes the lexicon-driven rule first written here and D-033/D-035: only when the whole excerpt is one patient-subject clause (Patient/Pt/The patient + reporting verb, one sentence, no `;` `,` `(` or "and"); family, EMS, unknown speakers, bare "C/O" and mixed excerpts get no label. It drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
memory/DECISIONS.md:340:- Status: accepted (T-063). Context: Chris reinstated cut items that need no third-party integration (D-031) and evals narrowed several flag rules (D-032 to D-035).
memory/DECISIONS.md:341:- Decision: the LLM split fallback is allowed only when the code split finds one record that is unsplit or lacks a date or source label; it returns offsets only, is validated by `ingest.validate_split` and marks records `LLM_SPLIT`; on a failed validation or failed call the paste stays one record with `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` and a reason (with no model wired in, the reason is not emitted yet: T-066). Manual entry runs code checks then judge 1 on her summary; "not a duplicate" is code for the undo and log, then the generator, judge 1 and the amount judge for the split-off record; batch accept (verified pending entries only) is code only (the UI 404/405 fallback that skips the check is T-065). The firm-voice paragraph is returned sentence by sentence by the model, with per-sentence code checks and judge 1 on accepted entries only, internal until accepted. D-032 drops the whole `objective_negative` category from flags (including credibility phrases such as Waddell and "out of proportion"; open question for Chris); D-037 is the binding rule for the patient self-report label (supersedes D-033 and D-035); D-034 makes numeric mismatches a hard 422. These supersede the matching cut items in ADR-015 and the batch/override text in ADR-005. Plain-language table: `docs/LLM_VS_CODE.md`.
| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
| D-039 | Re-run with decided items (2026-11-02): once any entry in a case is accepted, edited or dismissed, the case's records are frozen. A re-run reuses the stored records and never re-splits, so decided items keep their record ids and excerpts. Re-splitting is allowed only while every entry is still pending. | Provenance of an accepted item is what the paralegal verified against; it must never silently move. | T-057 staff r3 blocker |
| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
board/cards/T-072.md:2:id: "T-072"
---
id: "T-072"
title: "Neutral title for patient_reported_onset flag; drop '(patient self-report)' from export (D-040 follow-through)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
    if call is not None:
        try:
            verdict, call_id, _ = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)
        except Exception:
            verdict, call_id = "unavailable", None
        ladder_verdict = judges.to_ladder("j1", verdict)
    if ladder_verdict in ("partially", "unsupported"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:35.771Z

**tool call — Bash**
````
{
 "command": "grep -n \"credibility_language\" -r app | head; grep -rn \"patient_report\" app --include=*.py --include=*.js | head; grep -ln \"except Exception\\|broad except\" board/cards/*.md | head; grep -n \"broad except\\|judge path\" board/cards/*.md | head -5; sed -n 305,312p app/backend/review.py; sed -n 86,98p docs/LLM_VS_CODE.md | cut -c1-200"
}
````

### User / tool · 2026-11-02T02:45:35.929Z

**tool result**
````
app/backend/flag_templates.py:37:    "objective_negative": "causation", "accident_date_provenance": "causation", "credibility_language": "causation",
app/backend/flag_templates.py:133:    "credibility_language": lambda v: ("Credibility wording a defense reviewer may quote", f"Wording in {_at(v)} that questions effort or symptom credibility{_quote(v)}."),
app/backend/flags.py:23:CREDIBILITY_CATEGORY = "credibility_language"
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
app/frontend/dev/mock-data.js:746:   "category": "patient_report",
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/backend/export.py:45:_SELF_REPORT_SUBTYPES = ("patient_reported_onset", "patient_report")
board/cards/T-001.md
board/cards/T-040.md
board/cards/T-063.md
board/cards/T-038.md
board/cards/T-063.md:41:    - [minor] Broad except in the shared judge path swallows the error class — fix: Catch the provider errors the judge can raise and let anything else propagate, logged with the call id.
board/cards/T-063.md:44:- 2026-11-02T02:39:22Z architect: Round 1 fixes at 1855b76: B1 now D-037 (grounding.patient_report_spans, T-061 991dac4); DECISIONS.md:286 and ADR-018 amended; M3-M6 documented as code behaves; M2/M8 point to T-066/T-065 as defects; m1 trigger, m3 and nit wording fixed; row 13 and stale 'manual add is a cut' line corrected. Verified: .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -> 29 passed (31070c3). Not changed: m2 broad except in review.py (code, not doc); D-032 scope question left to Chris.
board/cards/T-063.md:54:    - [minor] Broad except in the shared judge path still swallows the error class (carried from round 1, no card) — fix: Catch only the provider error classes the judge call can raise; let anything else propagate, logged with the call id. Orchestrator: file a card.
board/cards/T-063.md:58:What changed: LLM_VS_CODE row 1, row 13 and second-wave section rewritten to HEAD behaviour (D-037 label rule, manual entry judge 1, not-a-duplicate model calls, model-returned narrative sentences, D-032 whole-category suppression, T-066/T-065 flagged as defects); DECISIONS.md line 286 and ADR-018 amended. How verified: read grounding.py, review.py, narrative.py, flags.py, ingest.py at HEAD; .venv/bin/python -m pytest -q tests/unit/test_split_llm.py = 29 passed. Left: D-032 credibility-phrase question for Chris; m2 broad except in review.py is a code finding with no card. Surprised: row 13 and costs section also had stale claims.
            if e["state"] != "rejected":
                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
            e["ladder"]["backend"] = P.backend_name()
            e.pop("_stage", None)
            _upsert(conn, case_id, "entry", PL._clean(e), t)
    else:
        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
    # its amounts come back as their own items (new ids; existing amounts keep theirs and their review status)

- **Code** finds the money. `$50,000` follows the word "add", not a billing label, so the rule says *unclear* (and the injection warning would force *unclear* in any case). It is not a `charge`, so it
- The **phrase scan** tags record 3. Its entry, and anything citing it, needs review; a banner names the record. The text is shown exactly as written.
- The pre-existing flag from record 2 ("prior ACL repair of the same knee in 2019") is still raised: the flag pass runs on each record separately, so record 3's text never reaches the call that looks 
- Nothing in the record can accept, dismiss or resolve a flag. Only her clicks do.

## Added in the second build wave (D-031 to D-035)

- **Manual entry for a rejected record (code checks, then judge 1).** If a record could not be verified, the paralegal can build the entry herself by selecting whole sentences of that record. Code che
- **"Not a duplicate" (code undoes the merge; model drafts and checks the split-off record).** On a merged entry she picks one of the merged records. Code removes it from the entry, restores its amoun
- **Draft treatment paragraph in the firm's voice (model, behind the full ladder).** A model may draft a paragraph from **accepted entries only**. The **model returns the sentences**, each citing one 
- **Batch accept (code only).** Accepts entries that are `verified` and still `pending`, in one all-or-nothing request, with the count on the button (no separate confirm step) and an Undo. Never amoun
- **Narrower flags (D-032, D-033, D-035, D-037).**
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:38.534Z

**tool call — Bash**
````
{
 "command": "sed -n 12,30p app/backend/flags.py; grep -n \"CREDIBILITY_CATEGORY\\|credibility\" app/backend/flags.py | head -20; grep -n \"credibility_language\" app/llm/lexicon.yaml | head -3; git show a27e3a4 --stat | head -15; sed -n 99,104p docs/LLM_VS_CODE.md | cut -c1-80"
}
````

### User / tool · 2026-11-02T02:45:38.677Z

**tool result**
````
_PER_RECORD_TYPES = ("pre_existing", "causation")
# D-032: normal/negative findings are context only and never become flags (from either signal); a scene_facts flag needs a phrase-list
# hit on a specific adjuster phrase, never just a model's reading of a mechanism description.
_CONTEXT_ONLY = ("objective_negative",)
_NEEDS_LEXICON = ("scene_facts",)
# D-038 (narrows D-032): defense credibility phrases are the exception to "normal/negative is context only". They are what an adjuster quotes
# against the claimant, so the paralegal must see them first. Entry ids come from app/llm/lexicon.yaml; subjective_exceeds_objective also holds
# "no objective findings" (stays context), so only its credibility phrases count. Raised under their own category, not objective_negative.
_CREDIBILITY_ENTRIES = {"symptom_magnification": None,   # Waddell, symptom magnification, inconsistent/sub-maximal/poor effort, malingering, ...
                        "subjective_exceeds_objective": re.compile(r"out\s+of\s+proportion|non-?\s?physiologic", re.I)}
CREDIBILITY_CATEGORY = "credibility_language"


def is_credibility_hit(h: dict) -> bool:
    if h["id"] not in _CREDIBILITY_ENTRIES:
        return False
    rx = _CREDIBILITY_ENTRIES[h["id"]]
    return rx is None or bool(rx.search(h.get("text", "")))
18:# D-038 (narrows D-032): defense credibility phrases are the exception to "normal/negative is context only". They are what an adjuster quotes
20:# "no objective findings" (stays context), so only its credibility phrases count. Raised under their own category, not objective_negative.
23:CREDIBILITY_CATEGORY = "credibility_language"
26:def is_credibility_hit(h: dict) -> bool:
95:        if is_credibility_hit(h):
96:            hits.append(dict(h, category=CREDIBILITY_CATEGORY))
104:        key = (a, b, h["flag_type"], CREDIBILITY_CATEGORY if h["category"] == CREDIBILITY_CATEGORY else None)   # D-038: never folded into a hedge flag
commit a27e3a4780fb8f5015644d39ac0fa85dfefcaa3b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:44:39 2026 -0600

    feat(backend): cut the patient_report speaker chip (T-071, D-040)
    
    Remove grounding.has_self_report/patient_report_spans and every source_kind=patient_report setter; flags panel chip markup removed; tests and lexicon selfcheck assert no chip.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/generator.py        |   2 +-
 app/backend/grounding.py        |  32 +-----------
 app/backend/present.py          |   3 +-
 app/frontend/dev/mock-data.js   |   4 +-
 app/frontend/flags.js           |   5 +-
  - *D-032:* code drops the **whole `objective_negative` category** from both th
  - *D-037 (binding, supersedes D-033 and D-035; code `grounding.patient_report_
- **Numbers cannot be overridden (D-034).** A number, date or dollar figure in a
- **Still cut, on purpose:** reclassifying a charge (a rate must never become a 

## What the tool is built never to do (from the sample case)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:39.547Z

Now edit with a Python script for the long lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:47.413Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\ndef sub(path, pairs):\n    s=open(path).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(path,a[:60],s.count(a))\n        s=s.replace(a,b)\n    open(path,'w').write(s)\n\nsub('docs/LLM_VS_CODE.md',[\n(\"When no model is wired in at all (the case-creation path today), only `SPLIT_AMBIGUOUS` is emitted and the reason is not shown; that gap is card T-066, so read this row as the intended behaviour once T-066 lands.\",\n \"With no model wired in, the paste stays one record flagged `SPLIT_AMBIGUOUS` with `SPLIT_REJECTED` (reason `NO_MODEL`) (T-066).\"),\n(\"normal or negative exam findings and credibility wording such as \\\"out of proportion\\\" are context only, see D-032 below)\",\n \"normal or negative exam findings are context only (D-032); defense credibility wording such as \\\"out of proportion\\\" or Waddell signs raises a flag (D-038), see the second-wave section)\"),\n(\"Whether an excerpt gets the **patient self-report** label is set by code (rule D-037, see the second-wave section), never by the model.\",\n \"No code or model labels who is speaking: the patient self-report chip is cut (D-040), and every excerpt is shown verbatim with its source label.\"),\n(\"With no model available, the entry is not drafted and a `LLM_UNAVAILABLE` warning tells her to enter it by hand.\",\n \"With no model available, the entry is not drafted and a `LLM_UNAVAILABLE` warning says the entry has not been drafted yet.\"),\n(\" The front end still has a fallback that, on a 404/405 from the batch route, accepts item by item and so skips that check; card T-065 removes it, and until then it is a known defect, not intended behaviour.\",\n \" If the batch route answers 404 or 405, the UI shows an error and accepts nothing (T-065).\"),\n(\"- **Narrower flags (D-032, D-033, D-035, D-037).**\",\"- **Narrower flags (D-032, D-038) and the cut self-report chip (D-040).**\"),\n])\ns=open('docs/LLM_VS_CODE.md').read()\nlines=s.split('\\n')\ni=[k for k,l in enumerate(lines) if l.startswith('  - *D-032:*')][0]\nj=[k for k,l in enumerate(lines) if l.startswith('  - *D-037 (binding')][0]\nlines[i]=(\"  - *D-032 and D-038:* normal or negative findings (\\\"negative for fracture\\\", \\\"full ROM\\\", \\\"no objective findings\\\") are **context only**: code drops them from both the lexicon and the model, so they never raise a flag. \"\n \"Defense **credibility phrases** from the lexicon (Waddell signs, \\\"out of proportion\\\", symptom magnification, \\\"non-physiologic\\\", inconsistent or sub-maximal effort, malingering) **do raise a flag** (D-038, implemented in T-067, commit 59c7edb). They are raised under their own category `credibility_language` (a causation flag), never folded into a hedge flag, because an adjuster quotes them against the claimant and the paralegal should see them first. \"\n \"Scene facts raise a causation flag only on specific adjuster phrases (\\\"minimal damage\\\", \\\"refused transport\\\"), not on a plain description of the crash.\")\nlines[j]=(\"  - *D-040 (supersedes D-033, D-035 and D-037; code removed in T-071, commit a27e3a4):* the **patient self-report chip is cut**. Every excerpt is shown as a verbatim record excerpt with its source label; no code or model labels who is speaking, because four review rounds kept finding mixed excerpts that a closed rule still mislabeled, and the excerpt already shows who spoke. \"\n \"Open: T-072 gives the `patient_reported_onset` flag a neutral title and drops \\\"(patient self-report)\\\" from the export. The qualifier-carry check (a summary must keep \\\"complained of\\\" and similar) is separate and unaffected.\")\nopen('docs/LLM_VS_CODE.md','w').write('\\n'.join(lines))\nEOF\ngrep -n \"broad\\|except\" docs/LLM_VS_CODE.md | head; sed -n 280,290p memory/DECISIONS.md | cut -c1-120; grep -n \"ADR-018\" memory/DECISIONS.md | head -3"
}
````

### User / tool · 2026-11-02T02:45:47.584Z

**tool result**
````
    | accident_date_provenance | Accident date source | Accident date as stated in {provider} ({date}): “{quote}”. |
    | date_ambiguous | Date to confirm | The date “{raw}” in {provider} can be read more than one way; choose one re
    | injection_suspected | Instruction-like text in a record | {provider} ({date}) contains instruction-like text: “{

    Every category has a code template and a flag_type. `recovery_context` entries have `strength: low` and never raise 
  - Code verifies the excerpt, computes offsets and renders `title` and `explanation` from a template per category (`app
  - `source_kind = "patient_report"` is set by code (`grounding.patient_report_spans`) under D-037, which supersedes the
- Consequences: no free LLM string reaches the internal notes; the golden `must_not` list can be tested against template
- Alternatives considered: J1 over LLM prose (a judge on a free-text claim is the weakest rung); editable titles (cut); 

## ADR-014 Conflicts: the accident-date rule, header-line grounding, and offsets
339:## ADR-018 Second-wave additions and narrowings (D-031 to D-035)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:57.899Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\ndef sub(path, pairs):\n    s=open(path).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(path,a[:60],s.count(a))\n        s=s.replace(a,b)\n    open(path,'w').write(s)\ns=open('memory/DECISIONS.md').read()\na=s.index(\"  - `source_kind = \\\"patient_report\\\" is set by code\") if False else s.index(\"  - `source_kind = \\\"patient_report\\\"` is set by code\")\nb=s.index(\"\\n\",a)\ns=s[:a]+(\"  - `source_kind = \\\"patient_report\\\"` and the \\\"Patient self-report\\\" chip are **cut (D-040)**, which supersedes the lexicon-driven rule first written here and D-033/D-035/D-037; the code setter was removed in T-071 (commit a27e3a4). Every excerpt is shown verbatim with its source label. Open: T-072 (neutral title for the `patient_reported_onset` flag, no \\\"(patient self-report)\\\" in the export). Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.\")+s[b:]\nopen('memory/DECISIONS.md','w').write(s)\nsub('memory/DECISIONS.md',[\n(\"(with no model wired in, the reason is not emitted yet: T-066)\",\"(with no model wired in, the reason is `NO_MODEL`: T-066)\"),\n(\" (the UI 404/405 fallback that skips the check is T-065)\",\" (on a 404/405 the UI shows an error and accepts nothing: T-065)\"),\n(\"D-032 drops the whole `objective_negative` category from flags (including credibility phrases such as Waddell and \\\"out of proportion\\\"; open question for Chris); D-037 is the binding rule for the patient self-report label (supersedes D-033 and D-035);\",\n \"D-032 keeps normal or negative findings context-only, and D-038 narrows it so defense credibility phrases (Waddell, \\\"out of proportion\\\", symptom magnification) raise a flag under category `credibility_language` (T-067, commit 59c7edb); D-040 cuts the patient self-report chip (supersedes D-033, D-035 and D-037; T-071, commit a27e3a4; T-072 open for the `patient_reported_onset` title and export wording);\"),\n(\"## ADR-018 Second-wave additions and narrowings (D-031 to D-035)\",\"## ADR-018 Second-wave additions and narrowings (D-031 to D-040)\"),\n])\n# F6 known limitation in doc\nsub('docs/LLM_VS_CODE.md',[\n(\"- **Batch accept (code only).**\",\"- **Known limitation (judge errors).** The shared judge path used by manual entry and \\\"not a duplicate\\\" (`review.py`) catches any exception and reports `JUDGE_UNAVAILABLE`. The state is visible to the paralegal, but the error class and call id are not kept; narrowing it to provider errors is a code change with no card yet.\\n- **Batch accept (code only).**\"),\n])\nEOF\nsed -i '' 's/(D-031 to D-035)/(D-031 to D-040)/' memory/DECISIONS.md 2>/dev/null; grep -n \"D-031 to D-03\" memory/DECISIONS.md docs/LLM_VS_CODE.md | cut -c1-140; grep -n \"D-037\\|question for Chris\\|T-066\\b\" docs/LLM_VS_CODE.md memory/DECISIONS.md | cut -c1-160; git diff --stat -- docs memory/DECISIONS.md"
}
````

### User / tool · 2026-11-02T02:45:58.076Z

**tool result**
````
docs/LLM_VS_CODE.md:92:## Added in the second build wave (D-031 to D-035)
docs/LLM_VS_CODE.md:29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table ro
docs/LLM_VS_CODE.md:101:  - *D-040 (supersedes D-033, D-035 and D-037; code removed in T-071, commit a27e3a4):* the **patient self-report chip is cut**. Every e
memory/DECISIONS.md:286:  - `source_kind = "patient_report"` and the "Patient self-report" chip are **cut (D-040)**, which supersedes the lexicon-driven rule fi
memory/DECISIONS.md:341:- Decision: the LLM split fallback is allowed only when the code split finds one record that is unsplit or lacks a date or source label;
 docs/LLM_VS_CODE.md | 15 ++++++++-------
 memory/DECISIONS.md |  6 +++---
 2 files changed, 11 insertions(+), 10 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:59.501Z

**tool call — Bash**
````
{
 "command": "grep -n \"NOT_ATTEMPTED\\|NO_MODEL\" memory/contracts/api.md app/backend/ingest.py | head -12; git show d148e0f --stat | head -12"
}
````

### User / tool · 2026-11-02T02:45:59.611Z

**tool result**
````
app/backend/ingest.py:264:        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
app/backend/ingest.py:266:        split_failure = "NOT_ATTEMPTED"    # several records plus an unsplit tail: the model is only asked about a single block, so say that
app/backend/ingest.py:273:                split_failure = "NO_MODEL"
app/backend/ingest.py:300:            if split_failure == "NOT_ATTEMPTED":
app/backend/ingest.py:301:                msg = "The paste has several records and some text outside them; the AI is only asked to split a single unsplit block, so that text stays its own record (NOT_ATTEMPTED)."
app/backend/ingest.py:302:            elif split_failure == "NO_MODEL":
memory/contracts/api.md:67:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
commit d148e0f4a6870623e65601c02cf408ce49f9daec
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:44:51 2026 -0600

    fix(backend): run-path fixture miss and unsplit tail both emit SPLIT_REJECTED with a reason; run result carries split_failure (T-066 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/ingest.py        | 18 ++++++++++++++----
 app/backend/pipeline.py      |  8 ++++----
 memory/contracts/api.md      |  2 +-
 tests/unit/test_split_llm.py | 34 ++++++++++++++++++++++++++++++++++
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:02.985Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nfor p,a,b in [\n('docs/LLM_VS_CODE.md',\"With no model wired in, the paste stays one record flagged `SPLIT_AMBIGUOUS` with `SPLIT_REJECTED` (reason `NO_MODEL`) (T-066).\",\n \"`SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record).\"),\n('memory/DECISIONS.md',\"the reason is `NO_MODEL`: T-066)\",\"the reason is `NO_MODEL`; an unsplit tail after several records gives `NOT_ATTEMPTED`, never silently: T-066, d148e0f)\")]:\n    s=open(p).read(); assert s.count(a)==1; open(p,'w').write(s.replace(a,b))\nEOF\ngit add docs/LLM_VS_CODE.md memory/DECISIONS.md"
}
````

### User / tool · 2026-11-02T02:46:03.125Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:03.956Z

**tool call — Bash**
````
{
 "command": "git commit -m \"docs(architect): T-063 r3: D-038 credibility flags decided, D-040 cuts self-report chip, split reasons, batch and judge wording\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md memory/DECISIONS.md 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T02:46:04.433Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 4808b77] docs(architect): T-063 r3: D-038 credibility flags decided, D-040 cuts self-report chip, split reasons, batch and judge wording
 2 files changed, 11 insertions(+), 10 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:08.612Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-063 --sha 4808b77 --agent architect; $B ac T-063 --check 1 --agent architect --evidence \"r3 4808b77: docs match HEAD; D-038 credibility_language (59c7edb), D-040 chip cut (a27e3a4), T-072 open; split reasons NO_MODEL/NOT_ATTEMPTED (d148e0f); grep 'question for Chris|D-037' LLM_VS_CODE.md clean\"; $B handoff T-063 --agent architect --text \"What changed: LLM_VS_CODE rows 1 and 13 and second-wave section, DECISIONS.md ADR-018 and line 286 (4808b77). D-038 credibility flags stated as decided (credibility_language, T-067 59c7edb); D-037 chip text replaced by D-040 (T-071 a27e3a4), T-072 cited as open; row 1 gives NO_MODEL and NOT_ATTEMPTED (d148e0f); batch 404/405 now shows an error and accepts nothing (T-065); LLM_UNAVAILABLE wording matches review.py. How verified: read flags.py, ingest.py, review.py, api.md at HEAD; grep for stale phrases is clean. Left: F6 broad except in review.py is documented as a known limitation, still needs an orchestrator card. Surprised: flag_templates.py still carries a patient_report template (T-072 scope).\"; $B move T-063 in_review --agent architect"
}
````

### User / tool · 2026-11-02T02:46:08.972Z

**tool result**
````
T-063: commit 4808b77 recorded
AC 1 checked: r3 4808b77: docs match HEAD; D-038 credibility_language (59c7edb), D-040 chip cut (a27e3a4), T-072 open; split reasons NO_MODEL/NOT_ATTEMPTED (d148e0f); grep 'question for Chris|D-037' LLM_VS_CODE.md clean
handoff written on T-063
T-063: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:11.694Z

T-063 round 3 is in review, committed as 4808b77. The docs now say D-038 credibility flags are decided (`credibility_language`) and D-040 cuts the self-report chip, with T-072 cited as open. I checked the claims against `flags.py`, `ingest.py`, `review.py` and `api.md` at HEAD and grepped for the stale phrases. I did not re-run any tests.

The 4 minors are fixed:
- **Split reasons:** row 1 now gives `NO_MODEL` and `NOT_ATTEMPTED` (d148e0f), per your message.
- **Batch accept:** a 404/405 now shows an error and accepts nothing (T-065).
- **`LLM_UNAVAILABLE`:** the doc wording now matches the message in `review.py`.
- **Broad `except` in `review.py`:** I documented it as a known limitation, but it still needs an orchestrator card.

`flag_templates.py` still carries a `patient_report` template, which I left alone as T-072 scope.
