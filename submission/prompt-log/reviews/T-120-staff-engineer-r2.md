# T-120 staff-engineer review, round 2 (fix commit 07dbd2b, archive of HEAD 433ac1c)

Verdict: changes. The r1 forms are fixed: `Hx per patient: lumbar strain 2019.`, `Hx obtained via interpreter: ...` and the `of`/year forms now flag, and lib09 record 1 stays quiet. The new guard is still a proxy. It skips whenever the rest of the sentence has no colon, no digit and no `of`, and that is not the same as "the sentence names no condition". Several ordinary wordings that name a condition are still suppressed, and some of them were flagged before T-120.

Exercised (archive of HEAD 433ac1c under the scratchpad, `.venv/bin/python -I`):
- `pytest tests/unit -q` on the archive: 3005 passed, 4 skipped.
- Probe `artifacts/review-evidence/t120r2_probe.py`: 32 history-source phrasings, 13 without a condition and 19 with one, run against HEAD and against the parent of the T-120 commit (1cb8707^). Output quoted below.
- Mutants `artifacts/review-evidence/t120r2_mutants.py` against `tests/unit/test_t120_history_source_sentence.py` (9 mutants).
- Read `git show 07dbd2b` in full. No LLM call, no float, no network, no clock; the guard is deterministic code in `lexicon_scan.py`.

Probe results (HEAD). Source-only sentences that stay quiet (correct): `Hx per patient's son.`, `PHx obtained via patient's son, who interpreted.`, `History provided by patient's wife.`, `Hx obtained via telephone interpreter.`, `Hx per EMS.`, `Hx per interpreter line.`, `History given by the patient's mother.`, `Hx relayed through language line interpreter.`, `PHx gathered from patient's friend.`, `History was obtained from patient's caregiver.`, `History obtained from chart review.`, `Hx obtained from Dr. Lee.`
Condition named, flag kept (correct): `Hx obtained via interpreter: lumbar strain 2019.`, `PHx obtained via patient's son: lumbar strain 2019.`, `Hx per patient's son, history of lumbar strain.`, `Hx per EMS - pt had previous knee surgery`, `PHx obtained via son; previous whiplash`, and the sentence-adjacent `Hx of lumbar strain 2019.` case.
Condition named, flag LOST (see finding 1): `Hx per patient's son, significant for diabetes.`, `History provided by wife, notable for lumbar strain.`, `History obtained from patient - lumbar strain.`, `PHx obtained via interpreter (lumbar strain).`, `Hx obtained via interpreter\nLumbar strain 2019`, `Hx per patient's son, who interpreted, a recurring back problem`, `Hx obtained from Dr. Lee: lumbar strain`, `Hx per patient's son; patient fractured her wrist before.`
Same eight against the parent 1cb8707^: the parent flags `Hx` in five of them (diabetes, parenthesis, newline, recurring, Dr. Lee colon), so those five are regressions that T-120 introduced. The other three (wife, dash, fractured) were not flagged by the parent either.

Mutants on the T-120 test file: drop the rest check (killed), drop digit (killed), drop `of` (killed), widen `via` (killed), never skip (killed), rest-to-end-of-text (killed), drop the VIA alternative (killed). SURVIVED: drop the colon from the rest check; newline no longer a sentence end.

```json
{"card": "T-120", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD 433ac1c (T-120 r2 commit 07dbd2b): app/backend/lexicon_scan.py:15-20, :107-115, :152; tests/unit/test_t120_history_source_sentence.py; no app URL",
 "exercised": ["pytest tests/unit -q on archive of HEAD: 3005 passed, 4 skipped", "artifacts/review-evidence/t120r2_probe.py: 32 phrasings on HEAD and on parent 1cb8707^", "artifacts/review-evidence/t120r2_mutants.py: 9 mutants, 7 killed, 2 survived", "artifacts/review-evidence/t120r2_probe2.py: colon-only and newline forms", "read git show 07dbd2b in full", "python -m app.pipeline evals/golden/sample.txt twice (fixture backend): identical output"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "The skip tests for the absence of a colon, digit or 'of', not for the absence of a condition, so a named prior condition is still dropped without a trace",
   "evidence": "app/backend/lexicon_scan.py:115 `return not re.search(r\":|\\d|\\bof\\b\", rest, re.I)` and :20 `_SENT_END = re.compile(r\"[.!?](?:\\s|$)|\\n\")`. Repro: `.venv/bin/python -I artifacts/review-evidence/t120r2_probe.py <archive of 433ac1c>` -> `BAD expect-flag \"Hx per patient's son, significant for diabetes.\" -> []`; `'PHx obtained via interpreter (lumbar strain).' -> []`; `'Hx obtained via interpreter\\nLumbar strain 2019' -> []` (the newline ends the 'sentence', so the year is never seen); `'Hx obtained from Dr. Lee: lumbar strain' -> []` (the period after Dr ends the sentence before the colon); `\"Hx per patient's son, who interpreted, a recurring back problem\" -> []`. The same inputs on the parent (1cb8707^) return ['Hx'] for diabetes, parenthesis, newline, recurring and the Dr. Lee colon form (artifacts/review-evidence/t120r2_probe.py with the parent archive).",
   "why_it_matters": "The card's rule is that the flag is suppressed only when the sentence names no condition. These sentences name one. A pre-existing condition is the first thing an adjuster looks for; losing its flag is silent (no state, no log) and is a regression against the build before T-120. Multi-line excerpts and 'Dr.' abbreviations are ordinary in record text, so the newline and Dr. forms are not exotic. I rate it major, not blocker: the quote stays in the record and entry, the lexicon's other phrases (prior, previous, chronic, degenerative, pre-existing) still catch most wordings, and it is the same class as my r1 finding at lower incidence.",
   "fix": "Invert the test: skip only when the whole remainder of the clause is a recognised source phrase and nothing else, for example match `^(source phrase)(,? who interpreted)?\\s*[.;]?\\s*(?:$|\\n\\s*$)`-style, or strip the source phrase and rescan the remainder for any other word. Treat newline, '(' , dash and ';' as continuing the condition text, not as the end of the source sentence, and do not end a sentence on an abbreviation such as 'Dr.'.",
   "acceptance_test": "Add to REAL in tests/unit/test_t120_history_source_sentence.py: \"Hx per patient's son, significant for diabetes.\", 'PHx obtained via interpreter (lumbar strain).', 'Hx obtained via interpreter\\nLumbar strain 2019', 'Hx obtained from Dr. Lee: lumbar strain', \"Hx per patient's son, who interpreted, a recurring back problem\"; assert each returns a pre_existing hit. Keep every SOURCE case green."},
  {"severity": "minor",
   "title": "Two of the guard's conditions are unpinned: the colon check and the newline sentence end",
   "evidence": "artifacts/review-evidence/t120r2_mutants.py: `SURVIVED M2 drop colon from rest check | 28 passed` and `SURVIVED M8 newline not a sentence end | 28 passed`. Every REAL row with a colon also has a digit, an 'of' or a separate lexicon phrase (`Hx per patient's son: prior neck injury.` is caught by 'prior ... injury', not by the Hx hit), so the colon branch is never the deciding one. Colon-only probe: `Hx obtained via interpreter: lumbar strain.` -> ['Hx'] today and would be [] under M2.",
   "why_it_matters": "The r1 blocker class was exactly the colon form; a later edit could reopen it and the suite would stay green. Tests that assert 'any pre_existing hit' cannot tell which rule produced it.",
   "fix": "Assert on the Hx hit itself (hit text equals the history word) for the colon-only and newline rows.",
   "acceptance_test": "Rows `Hx obtained via interpreter: lumbar strain.` and `Hx obtained via interpreter\\nLumbar strain` must assert a hit whose text is 'Hx'; mutants M2 and M8 in t120r2_mutants.py must be killed."},
  {"severity": "nit",
   "title": "Source phrases that name no person still flag: 'Hx per patient.' and 'Hx per medical records.'",
   "evidence": "t120r2_probe.py: `BAD expect-none 'Hx per patient.' -> ['Hx']`, `'Hx per medical records.' -> ['Hx']`. The parent flags them too.",
   "why_it_matters": "Over-flagging, the safe direction; the paralegal dismisses it. Listed so nobody mistakes it for a regression.",
   "fix": "Optional: add 'patient' and 'medical records' as stand-alone channels only after the finding-1 inversion, so the rule stays one mechanism.",
   "acceptance_test": "Optional test that both phrases stay quiet and `Hx per patient: lumbar strain 2019.` still flags."}
 ],
 "whats_right": ["All three r1 forms (Hx per patient: ..., colon after via, 'of') now flag, with named rows in REAL.", "Guard is deterministic code in lexicon_scan.py; lexicon.yaml untouched; the sample CLI output is byte-identical across two runs.", "Seven of nine mutants on the guard are killed, including widening `via` and removing the digit or 'of' check."],
 "questions_for_chris": []}
```
