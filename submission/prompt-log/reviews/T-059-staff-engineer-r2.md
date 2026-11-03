# T-059 round 2 review: firm-voice treatment paragraph (commit 06eb84b), staff-engineer-reviewer

Verdict: **pass**. Both round-1 majors are closed, the failed re-draft minor is closed, and `SEVERITY_NOT_QUOTED` exists and covers the prompt's four banned adjectives. One round-1 minor is partly open: the prompt's diagnosis and opinion wording has no code check. I rate that residual minor, not a blocker, for the reasons in the finding.

Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Pinning

- HEAD at review start: `373f8b1`. Commit under review: `06eb84b`, an ancestor of HEAD.
- Reviewed code: `git archive 06eb84b` at `artifacts/review-evidence/T-059-staff-engineer-r2/head_06eb84b`.
- `git diff --stat 06eb84b HEAD -- app/backend/narrative.py app/backend/export.py app/backend/store.py app/backend/api.py app/backend/judges.py tests/unit/test_narrative.py` is empty. The narrative code and tests are unchanged since 06eb84b.
- Known, not counted: in the live working tree, `tests/unit/test_narrative.py::test_recorded_sample_paragraph_replays_with_every_sentence_supported` fails with a fixture miss on step `narrative` while another worker re-records narrative fixtures. Per the brief it is treated as known. It passes in the pinned archive (see below).

## Round-1 findings: status

- **Major 1, seeded-hallucination test does not pin any check: closed.** `tests/unit/test_narrative.py` now runs `test_each_code_check_removes_a_seeded_sentence_with_its_own_reason` over 12 cases. Each asserts the exact `reasons` list, `r["reason"] == reasons[0]`, the matching `message`, and no `j1` call. The always-true clause from r1 is gone. Mutant N3 (the D-006 token check disabled, `narrative.py:59` set to `if False:`) fails 5 tests: four `e5` number/side/negation/date rows and the `e1` row. Output: `artifacts/review-evidence/T-059-staff-engineer-r2/mutants.out.txt`.
- **Major 2, stale-basis rule not tested: closed.** `test_entry_edited_after_the_draft_drops_its_sentence_from_the_letter` drafts, accepts, edits `e5` (summary change), exports, and asserts: the `e5` sentence is absent from `letter_text`, the `e1` sentence is still present (control), and the internal notes carry the `[NOT in the letter: the cited entry changed or is no longer accepted]` tag on the `e5` line only. Mutant N11 (the basis clause removed from `export.py` `narrative_sentences`) fails this test.
- **Minor 2, failed re-draft overwrites an accepted paragraph: closed.** `narrative.py:122-127` (`_keep_or_save`) returns the stored paragraph with `error` alongside and writes nothing when the stored paragraph has sentences or removed items. `test_failed_redraft_keeps_the_accepted_paragraph` runs four failure modes (`AU.LLMFailed`, `P.FixtureMiss`, schema-invalid, `None` output) and asserts the stored paragraph is unchanged and the `e5` sentence is still in the letter. Mutant N12 (`_keep_or_save` replaced by `_save(..., base)`) fails all 4 cases. Routes: `test_narrative_routes_before_any_draft` and `test_narrative_review_route_refuses_a_bad_action_and_an_empty_accept` exist.
- **Minor 1, banned wording has no code check: partly closed.** `SEVERITY_NOT_QUOTED` exists: it is in `REASONS` (`narrative.py:21`), raised in `check_sentence` (`narrative.py:70-71`, `_SEVERITY` at `:33-34`), and documented in `memory/contracts/api.md`. `_SEVERITY` covers the prompt's four banned adjectives (`narrative_v1.md:10`: serious, severe, significant, ongoing). The four round-1 probe sentences are now removed by code before judge 1 (probe output lines 1-4; mutant N13 fails 4 tests). See finding 1 for what remains.
- **Minor 3, reviewed commit not green on a clean checkout: closed.** `git archive 06eb84b` + `pytest tests/unit -q`: 928 passed (`clean_archive_full_unit.out.txt`). The archive run includes the recorded replay, which passes there.

## Findings

- **minor (open, residual of round-1 minor 1), diagnosis and opinion wording is not checked in code.** Evidence: `artifacts/review-evidence/T-059-staff-engineer-r2/probe_banned_wording.out.txt` lines 5-6: `PASSES CODE CHECKS (judge 1 only) <- ... with mild right foraminal narrowing, diagnosed as a herniation.` and `... a clear sign of nerve injury.` The quote is `C5-C6 disc protrusion with mild right foraminal narrowing.` (e8 shape), so "herniation" and "nerve injury" are not in the quote. The prompt bans them: `app/llm/prompts/narrative_v1.md:8` ("Never add a diagnosis, severity, prognosis, opinion or cause"). `_SEVERITY` (`narrative.py:33-34`) has no diagnosis or opinion terms. Why it matters: a sentence that adds a diagnosis reaches judge 1 alone; the judge is stubbed in the tests and its catch rate on this paragraph is unmeasured until the AC3 live run. It is rated minor, not blocker, because judge 1 still runs on every sentence, the paragraph is internal until the paralegal accepts it, and the round-1 rating stands. Fix: add a deterministic backstop for diagnosis and opinion wording (for example, a content-word check against the cited quote, which the round-1 review proposed as `WORD_NOT_IN_QUOTE`), or at minimum a diagnosis and opinion term list next to `_SEVERITY`. Acceptance: the two probe sentences return a reason code, and `call.steps()` shows no `j1` for them; `test_recorded_sample_paragraph_replays_with_every_sentence_supported` and `test_quoted_severity_and_recommendation_words_are_allowed` still pass.

## What this review does not cover

- AC3 (live 3-run eval, 0 unsupported sentences): card status `done: false`, deferred to the gate by the coordinator. Not a finding in this round.
- Judge 1 on a live backend (not exercised; tests stub it).
- The frontend panel (`app/frontend/narrative.js`, commit 636a042, a later commit).

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- Read `personas/staff-engineer.md` in full and `reviews/T-059-staff-engineer.md` in full (round-1 majors and minors).
- `.venv/bin/python tools/board.py show T-059`: `status: "in_review"`, `commits: ["20d866f", "06eb84b"]`, AC1 and AC2 `done: true`, AC3 `done: false`.
- `git show --stat 06eb84b` (3 files: `narrative.py`, `memory/contracts/api.md`, `tests/unit/test_narrative.py`); `git show 06eb84b -- app/backend/narrative.py` read; `git diff --stat 06eb84b HEAD` over the narrative, export, store, api, judges and test files: empty.
- `git archive 06eb84b | tar -x -C artifacts/review-evidence/T-059-staff-engineer-r2/head_06eb84b`.
- `.venv/bin/python -m pytest tests/unit/test_narrative.py -q -p no:cacheprovider` in the archive: 36 passed.
- `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` in the archive: 928 passed (`clean_archive_full_unit.out.txt`).
- `.venv/bin/python -m pytest tests/unit/test_narrative.py -q -p no:cacheprovider` in the live working tree: 1 failed, 35 passed. The failure is `test_recorded_sample_paragraph_replays_with_every_sentence_supported` (`FixtureMiss`, step `narrative`), the known fixture re-record, not counted.
- Mutants on scratch copies (`mutate_t059.py`, output `mutants.out.txt`): N3 D-006 token check off, 5 failed; N11 stale-basis clause off, 1 failed; N12 failed re-draft overwrites, 4 failed; N13 `SEVERITY_NOT_QUOTED` off, 4 failed.
- `.venv/bin/python probe_banned_wording.py` in the archive: 6 sentences through `narrative.check_sentence`, output in `probe_banned_wording.out.txt`.
- Read `app/llm/prompts/narrative_v1.md:8-10` and the `_SEVERITY` pattern (`narrative.py:33-34`) for the banned-wording comparison.

Not exercised: live claude-cli or API backend; the 3-run eval; the frontend panel.

## Machine-readable record

```json
{"card": "T-059", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round 2 of T-059 at commit 06eb84b: app/backend/narrative.py (check_sentence, _keep_or_save, REASONS incl. SEVERITY_NOT_QUOTED), tests/unit/test_narrative.py, memory/contracts/api.md. Pinned at git archive 06eb84b (artifacts/review-evidence/T-059-staff-engineer-r2/head_06eb84b). export.py narrative_sentences read at 06eb84b (unchanged since). HEAD 373f8b1: no change to these files since 06eb84b. Live working tree had one known fixture-miss failure (not counted).",
 "exercised": [
  "read personas/staff-engineer.md and reviews/T-059-staff-engineer.md in full",
  "board.py show T-059 (in_review; commits 20d866f, 06eb84b; AC1, AC2 done; AC3 not done)",
  "git show --stat 06eb84b; git show 06eb84b -- app/backend/narrative.py; git diff --stat 06eb84b HEAD over narrative/export/store/api/judges/tests: empty",
  "git archive 06eb84b extracted to artifacts/review-evidence/T-059-staff-engineer-r2/head_06eb84b",
  "pytest tests/unit/test_narrative.py -q in the archive: 36 passed",
  "pytest tests/unit -q in the archive: 928 passed (clean checkout, round-1 minor 3 resolved)",
  "pytest tests/unit/test_narrative.py -q in the live working tree: 1 failed (known fixture miss, not counted), 35 passed",
  "mutants N3 (D-006 token check off) 5 failed; N11 (stale-basis clause off) 1 failed; N12 (failed re-draft overwrites) 4 failed; N13 (SEVERITY_NOT_QUOTED off) 4 failed (mutants.out.txt)",
  "probe_banned_wording.py through narrative.check_sentence: 4 round-1 severity sentences removed by SEVERITY_NOT_QUOTED; 2 diagnosis/opinion sentences pass code checks (probe_banned_wording.out.txt)",
  "read app/llm/prompts/narrative_v1.md:8-10 and narrative.py:16-72, 75-134",
  "not exercised: live claude-cli/API judge, AC3 3-run eval, frontend panel"],
 "verdict": "pass",
 "scores": {"d006_token_check_pinned": 5, "stale_basis_pinned": 5, "failed_redraft_keeps_paragraph": 5, "severity_backstop_present": 4, "banned_wording_backstop_complete": 3, "clean_checkout_green": 5},
 "findings": [
  {"severity": "minor", "title": "Diagnosis and opinion wording the prompt bans has no code check; such sentences reach judge 1 alone (residual of round-1 minor 1)",
   "evidence": "artifacts/review-evidence/T-059-staff-engineer-r2/probe_banned_wording.out.txt lines 5-6: 'PASSES CODE CHECKS (judge 1 only)' for '... mild right foraminal narrowing, diagnosed as a herniation.' and '... a clear sign of nerve injury.' against the quote 'C5-C6 disc protrusion with mild right foraminal narrowing.' Prompt: app/llm/prompts/narrative_v1.md:8 'Never add a diagnosis, severity, prognosis, opinion or cause.' _SEVERITY (app/backend/narrative.py:33-34) has no diagnosis or opinion terms.",
   "why_it_matters": "A sentence that adds a diagnosis is an invented fact, and only judge 1 stands between it and the internal draft. Judge 1 is stubbed in the tests and not measured live (AC3 deferred). Rated minor, not blocker: judge 1 still runs on every sentence, the paragraph is internal until the paralegal accepts it, and round 1 rated the same gap minor.",
   "fix": "Add a deterministic backstop for diagnosis and opinion wording: every content word of the sentence (after the provider label, date phrase and stop words) must appear in the cited quote or summary, or the sentence is removed with a reason code (for example WORD_NOT_IN_QUOTE). Minimum: a diagnosis and opinion term list next to _SEVERITY.",
   "acceptance_test": "probe_banned_wording.py: the two diagnosis and opinion sentences return a reason code, and call.steps() has no j1 for them; test_recorded_sample_paragraph_replays_with_every_sentence_supported and test_quoted_severity_and_recommendation_words_are_allowed still pass."}
 ],
 "whats_right": [
  "Round-1 major 1 closed: the seeded-hallucination test asserts exact reason lists; disabling the D-006 token check fails 5 tests (mutants.out.txt N3).",
  "Round-1 major 2 and minor 2 closed: an edit to an accepted entry drops its sentence from the letter with the NOT-in-the-letter tag, and a failed re-draft keeps the accepted paragraph (N11 fails 1 test; N12 fails 4).",
  "Round-1 minor 3 closed: a clean git archive of 06eb84b passes all 928 unit tests; SEVERITY_NOT_QUOTED covers the prompt's four banned adjectives (N13 fails 4 tests)."
 ],
 "questions_for_chris": [
  "Under CONTRACT D.2, does 'invents or loses facts' cover a diagnosis word that passes the code layer and reaches judge 1, which would make it a blocker? I rated it minor, consistent with round 1, because judge 1 is the designated control and the paragraph is internal until accepted."
 ]}
```
