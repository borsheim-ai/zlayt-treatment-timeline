# T-059 review: firm-voice treatment paragraph, staff-engineer-reviewer

Commit under review: 20d866f (narrative.py, export.py, store.py, schemas.py, narrative_v1.md, tests/unit/test_narrative.py, 9 narrative fixtures). `narrative.py`, `export.py` (narrative parts) and the tests are unchanged at HEAD 08764e7, so mutants were run on a clean `git archive HEAD`.
AC3 (live 3-run, 0 unsupported) is deferred to the gate: not a finding.
Verdict: **changes**. No blockers, two majors, three minors.

What I checked against the brief:
- Built from accepted entries only: yes. `accepted_entries` uses `export._View.in_entries`; mutant N1 (use all entries) fails 2 tests.
- Every sentence cites an accepted entry and goes through code checks then judge 1: yes. An unknown or non-accepted `entry_id` is removed as `NOT_AN_ACCEPTED_ENTRY` (N9 fails a test); judge verdicts partial, unsupported and unavailable all remove the sentence with a reason (N7 fails 3 tests). There is no silent fallback to "supported".
- Seeded hallucinations are removed with a reason: yes, but the test is looser than it looks (major 1).
- No flag content, no unquoted causation: tested and mutants N5 and N6 fail a test each. Adverse facts that add no number, side, negation, date, cause word or lexicon term are left to judge 1 only (minor 1).
- Internal draft until accepted: pending, dismissed and accepted-with-changed-entry paragraphs stay out of the letter (N10, N12 fail a test). The edited-entry path is not pinned (major 2).

```json
{"card": "T-059", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 20d866f: app/backend/narrative.py, export.py, store.py, schemas.py, app/llm/prompts/narrative_v1.md, memory/contracts/api.md, tests/unit/test_narrative.py, tests/fixtures/llm/narrative/*. Clean archives of 20d866f and of HEAD (08764e7) under artifacts/review-evidence/T-059-staff-engineer/. Sample case (tests/_golden sample). No app URL exercised.",
 "exercised": [
  "read personas/staff-engineer.md in full; read reviewer memory MEMORY.md and project_split_llm_review_patterns.md",
  "python3 tools/board.py show T-059 -> status in_review, commits [20d866f], AC1 and AC2 done, AC3 not done (deferred to gate by coordinator)",
  "git show 20d866f -- app/ memory/ read in full; tests/unit/test_narrative.py read in full (git show 20d866f:tests/unit/test_narrative.py)",
  ".venv/bin/python -m pytest tests/unit/test_narrative.py -q (working tree) -> 17 passed; pytest tests/unit -q -k narrative -> 17 passed, 879 deselected; full tests/unit (working tree) -> 895 passed in 17.46s",
  "git diff --stat 20d866f HEAD -- narrative.py export.py store.py schemas.py narrative_v1.md judges.py grounding.py test_narrative.py -> export.py (+/-7), grounding.py (53), store.py (6) differ; narrative.py, schemas.py, prompt and test_narrative.py identical",
  "git archive 20d866f into artifacts/review-evidence/T-059-staff-engineer/tree, pytest tests/unit -q -> 6 failed, 860 passed (test_case_extras x2, test_narrative recorded replay, test_t037_backend x3: failed j1/j2/j3/j4 fixture calls); after copying untracked/modified fixtures from the working tree -> 5 failed; git archive HEAD (tree2) -> 895 passed. The failing j1..j4 fixtures were re-recorded later in 31070c3 ('re-record fixtures for D-028 prompts'). At the parent dbb2c66 the archive printed no pass/fail line, so there is no clean parent control",
  "probe artifacts/review-evidence/T-059-staff-engineer/probe_checks.py (working tree): check_sentence on 9 candidate sentences against e1/e5 quotes: 'herniated disc' -> ['SUMMARY_DROPS_QUALIFIER']; 'ongoing since the crash' -> ['SUMMARY_DROPS_QUALIFIER']; 'significant pain 4/10' / 'severe pain 4/10' / 'and recommended surgery' / 'worsening pain 4/10' (e5) -> PASSES CODE CHECKS (judge 1 only); 'could not work' -> ['SUMMARY_TOKEN_NOT_IN_EXCERPT']; 'seriously injured' -> ['SUMMARY_DROPS_QUALIFIER']",
  "mutants on a clean archive of HEAD, pytest tests/unit/test_narrative.py, baseline 17 passed: N1 all entries not only accepted -> 2 failed; N2 skip all code checks -> 5 failed; N3 drop D-006 new_tokens check -> 17 passed (SURVIVES); N4 drop dropped_qualifiers -> 2 failed; N5 drop causation/adverse -> 1 failed; N6 drop flag-content -> 1 failed; N7 judge verdict not enforced -> 3 failed; N9 no accepted-entry gate -> 1 failed; N10 pending paragraph in letter -> 1 failed; N11 drop stale-basis check in letter -> 17 passed (SURVIVES); N12 dismissed paragraph in letter -> 1 failed (script artifacts/review-evidence/T-059-staff-engineer/mutants.py)",
  "grep: tests referencing /narrative routes -> none; grep LLM_FAILED_AFTER_RETRIES tests/unit/test_narrative.py -> no hits; narrative.py has no float(, sleep( or bare except (one specific except tuple at line 83)",
  "api.py:400-435 read (GET/POST narrative, narrative/review); judges.py run_j1_meta read (judge gets the quote and the candidate sentence only)",
  "Not exercised: live claude-cli or API backend; frontend panel (636a042, later commit); the AC3 3-run"
 ],
 "verdict": "changes",
 "scores": {"accepted_only_input": 5, "per_sentence_citation_and_judge": 4, "code_check_coverage_vs_prompt_rules": 3, "test_strength_on_ac1_ac2": 3, "internal_until_accepted": 4, "failure_visibility": 3, "commit_self_containedness": 2},
 "findings": [
  {"severity": "major",
   "title": "The seeded-hallucination test does not pin any one check: removing the D-006 token check leaves all 17 tests green",
   "evidence": "tests/unit/test_narrative.py:62 'assert rem and rem[0][\"reason\"] in (reason, \"SUMMARY_DROPS_QUALIFIER\", \"CAUSATION_NOT_QUOTED\", \"FLAG_CONTENT\", \"SUMMARY_TOKEN_NOT_IN_EXCERPT\")' accepts any code reason, and line 60 '... == [\"e1\"] or bad[\"entry_id\"] == \"e1\"' is always true for the e1 cases. Mutant N3 (narrative.py:54 'if grounding.new_tokens(...)' replaced by 'if False') -> '17 passed'. The invented-number case (e1, 'herniated disc at C6-C7 and neck pain 9/10') is still removed, but by SUMMARY_DROPS_QUALIFIER because the e1 quote has 'C/O' and the sentence drops it (probe_checks.py: e1 'herniated disc' -> ['SUMMARY_DROPS_QUALIFIER']). Every e1 case is caught by that incidental check.",
   "why_it_matters": "AC1 says each sentence must pass D-006. That clause has no test that fails when it is removed (checklist 13: tests must fail when the code breaks). The card's '5 cases' evidence looks like five different checks but one check does the work for all e1 rows.",
   "fix": "Parametrize with the exact expected reason code and assert equality, using a quote with no hedge or self-report marker (e5 'Pain 4/10, improving.') so only the named check can fire: an invented number (4/10 changed to 9/10), an invented side, an invented negation, a date not in the label. Remove the always-true clause on line 60.",
   "acceptance_test": "Mutant N3 (and each of dropped_qualifiers, causation, flag-content on its own) makes at least one test fail; each case asserts removed[0]['reason'] == the named code."},
  {"severity": "major",
   "title": "The 'drops out if its entry is edited' rule is not tested: removing the basis-hash check leaves all 17 tests green",
   "evidence": "app/backend/export.py:139 (HEAD, same logic as 20d866f): 'narrative_sentences' keeps a sentence only when 'basis.get(entry_id) == basis_hash(live[entry_id])'. Mutant N11 (replace that clause with nothing) -> '17 passed'. test_dismissed_and_stale_sentences_stay_out_of_the_letter only dismisses e5 (the 'entry_id in live' branch); no test edits an accepted entry's summary or quote after the draft. memory/contracts/api.md (T-059 row) promises 'a sentence drops out again if its entry is dismissed or edited'.",
   "why_it_matters": "This is the guard that keeps an accepted paragraph from putting a sentence into the letter that no longer matches its entry. It is the last code control between the paralegal's accept and the export, and nothing would notice if it broke.",
   "fix": "Add a test: draft, accept the paragraph, apply_review edit on e5 (summary or quote change), export, and assert the e5 sentence is absent from letter_text and that the internal notes carry the '[NOT in the letter: the cited entry changed ...]' tag. Add the inverse: an unchanged entry keeps its sentence.",
   "acceptance_test": "Mutant N11 makes the new test fail; the e5 sentence is not in letter_text after the edit and is in internal_notes_text with the tag."},
  {"severity": "minor",
   "title": "The prompt's banned wording (severity adjectives, added outcomes) has no code check; such sentences reach judge 1 alone",
   "evidence": "narrative_v1.md rule: 'Use no adjectives of your own (\"serious\", \"severe\", \"significant\", \"ongoing\")' and 'Never add a diagnosis, severity, prognosis'. probe_checks.py (e5 quote 'Pain 4/10, improving.'): 'recorded significant pain 4/10, improving', 'recorded severe pain 4/10, improving', 'recorded pain 4/10, improving, and recommended surgery', 'recorded worsening pain 4/10' all print 'PASSES CODE CHECKS (judge 1 only)'. check_sentence (narrative.py:50-65) only tests new numbers/sides/negations/dates, dropped hedges, causation/lexicon words and flag words.",
   "why_it_matters": "AC2 says no adverse facts that are not in the accepted entries. The code layer would let an unnumbered severity or outcome word through; judge 1 is then the only control, and the tests stub judge 1, so its catch rate on this paragraph is unmeasured until the AC3 live run. That is within the D-031 design (D-006 plus judge 1), so this is a gap in defence, not a spec violation.",
   "fix": "Add a deterministic backstop: every content word of the sentence (after removing the provider label, date phrase and stop words) must appear in the cited summary or quote, or the sentence is removed with a new reason code (for example WORD_NOT_IN_QUOTE). At minimum, enforce the prompt's own banned list in code.",
   "acceptance_test": "The four probe sentences above are removed before the judge call (call.steps() shows no j1 for them) with a reason code; the 8 recorded sample sentences still pass."},
  {"severity": "minor",
   "title": "A failed re-draft overwrites an accepted paragraph, and neither the failure path nor the routes are tested",
   "evidence": "narrative.py:73-85 and :114-118: draft() builds a fresh 'base' (status 'pending', sentences []) and calls _save on the LLM failure path (line 85 'base[\"error\"] = \"LLM_FAILED_AFTER_RETRIES\"; return _save(...)'), replacing config['narrative'] even when the stored paragraph was accepted. api.py:409-419 returns 200 with the error inside the narrative (only NO_ACCEPTED_ENTRIES maps to 400). grep for 'LLM_FAILED_AFTER_RETRIES' in tests/unit/test_narrative.py -> no hits; grep for '/narrative' under tests -> no files.",
   "why_it_matters": "A transient model error wipes the paralegal's accept and the sentences from the letter. The error is visible in the response, so this is not silent, but the loss is avoidable and untested, and the 404/422/400 route branches have no test.",
   "fix": "On failure, keep the existing narrative and return the error separately (or store it under narrative.error without clearing sentences/status). Add tests: failure path (stub raising AU.LLMFailed, and an invalid schema), and route tests for GET before draft, POST with no accepted entries (400), review before draft (404) and a bad action (422).",
   "acceptance_test": "Accept a paragraph, then run a failing re-draft: GET narrative still returns the accepted sentences and a separate error field; the route tests above pass."},
  {"severity": "minor",
   "title": "The reviewed commit is not green on a clean checkout: the AC1 recorded-replay test and five others fail at 20d866f",
   "evidence": "git archive 20d866f + pytest tests/unit -q -> '6 failed, 860 passed': test_narrative.py::test_recorded_sample_paragraph_replays_with_every_sentence_supported, test_case_extras.py x2, test_t037_backend.py x3 (log: 'llm call failed ... step=j1 ... prompt_hash=...', 'sample: 20 failed calls, steps [j1, j2, j3, j4]'). git archive HEAD (08764e7) -> '895 passed'. 31070c3 'chore(backend): re-record fixtures for D-028 prompts' is the later commit that makes the fixtures match the prompts.",
   "why_it_matters": "The card cites the recorded replay as AC1 evidence, but at its own commit that test depends on j1 fixtures that do not match the committed prompts. The cause is outside this card (D-028 prompt changes), and HEAD is green, so this is resolved; recorded so the evidence is not read as a green snapshot of 20d866f.",
   "fix": "None needed at HEAD. Run a clean `git archive` of the last card commit before in_review.",
   "acceptance_test": "git archive <card commit> + pytest tests/unit -q -k narrative -> 0 failed."}
 ],
 "whats_right": [
  "Accepted-only input is enforced in code and pinned: the prompt contains only accepted entries (no flags, gaps or conflicts), and removing the filter fails tests.",
  "Judge 1 failure modes are not silent: partial, unsupported and unavailable all remove the sentence with a reason code, and no path marks a sentence supported by default.",
  "The export is a pure function of the stored narrative and accepted entries: pending or dismissed paragraphs stay in the internal notes, an accepted one adds TREATMENT SUMMARY, and each sentence is followed by the provider and date from its entry."
 ],
 "questions_for_chris": []}
```
