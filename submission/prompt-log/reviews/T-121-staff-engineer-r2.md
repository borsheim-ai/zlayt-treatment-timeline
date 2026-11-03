# T-121 staff-engineer review, round 2 (fix commit 4c59fac, archive of HEAD 433ac1c)

Verdict: pass. Both r1 findings are fixed and pinned. The one-line style now carries ` — English: <summary>` on a translated entry before the note, the whitespace-only collapse is documented in the docstring and in api.md, and the standard style prints the note on its own bracket line under the quote. The default letter still equals the golden. Three minors and nits remain; none blocks.

Exercised (archive of HEAD 433ac1c, `.venv/bin/python -I`):
- `pytest tests/unit -q` on the archive: 3005 passed, 4 skipped. This includes the golden byte-equal test, `test_spanish_records` and `test_d050_never_verified`.
- `python -m evals.run --check-spec` on the archive: `{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}`.
- Mutants `artifacts/review-evidence/t121r2_mutants.py` (12) against test_t121_letter_styles, test_spanish_records, test_d050_never_verified and test_export.
- Probe `artifacts/review-evidence/t121r2_probe.py`: translated entry with empty, None and whitespace-only summary, and with a multi-line edited summary, in both styles.
- Read `git show 4c59fac` in full (export.py, api.md, the test file). No LLM call, no float, no network.

Mutant results: `_one_line` no-op KILLED (2 failed), `_one_line` collapsing spaces only KILLED, drop the English tail KILLED, English tail on every entry KILLED, summary not collapsed KILLED, standard style with the note back on the quote line KILLED, drop the note line in standard KILLED, tail placed after the note KILLED, note line with a leading space KILLED, one-line drops the note KILLED, one-line note only for one label KILLED. SURVIVED: provider label not collapsed in the one-line style (`{v.source(n)}` for `{_one_line(v.source(n))}`), 123 passed.

Probe, translated entry, one-line: summary '' gives `... [Ex. __ / Bates __] — English:  [AI translation of the Spanish original; check before sending]`; summary None gives `— English: None [...]`. Standard style with summary None raises `TypeError: sequence item 3: expected str instance, NoneType found` at export.py:285 (this crash predates T-121; the entry schema has a string summary).

```json
{"card": "T-121", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD 433ac1c (T-121 r2 commit 4c59fac): app/backend/export.py:245-270, memory/contracts/api.md:373 and :718, tests/unit/test_t121_letter_styles.py:80-146; no app URL",
 "exercised": ["pytest tests/unit -q on archive of HEAD: 3005 passed, 4 skipped", "python -m evals.run --check-spec: letter_equal true, internal_notes_equal true", "artifacts/review-evidence/t121r2_mutants.py: 12 mutants, 11 killed, 1 survived", "artifacts/review-evidence/t121r2_probe.py: empty/None summary and multi-line summary in both styles", "read git show 4c59fac in full"],
 "verdict": "pass",
 "scores": {"correctness": 4, "determinism": 5, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [
  {"severity": "minor",
   "title": "api.md still says the translation note 'ends the line in both styles', which is false for the standard style after r2",
   "evidence": "memory/contracts/api.md:373 ends with `The translation note ends the line in both styles.`; app/backend/export.py:248-250 and :269 now print the standard-style note as its own line (`*_translation_line(e)`), and api.md:718 says 'on its own line under the quote'. The two paragraphs of the same contract disagree.",
   "why_it_matters": "api.md is the contract the frontend and any later reviewer read; a reader of :373 would expect the note to share the quote's line and would write a UI or test against it.",
   "fix": "Change :373 to 'The translation note is its own bracket line under the quote in the standard style and ends the entry's line in the one-line style.'",
   "acceptance_test": "grep -n 'ends the line in both styles' memory/contracts/api.md returns nothing."},
  {"severity": "nit",
   "title": "Collapsing the provider label in the one-line style is not pinned by any test",
   "evidence": "t121r2_mutants.py: `SURVIVED H provider not collapsed in oneline | 123 passed`. export.py:269 calls `_one_line(v.source(n))`; no test gives a source label with a line break or a double space.",
   "why_it_matters": "Low: source labels come from a single header line. If a label ever carries a break, the 'one line per entry' promise breaks silently.",
   "fix": "Add a case with a source label containing a run of spaces and assert the entry line has one space.",
   "acceptance_test": "Mutant H is killed."},
  {"severity": "nit",
   "title": "A translated entry with an empty summary prints a dangling 'English:' in the one-line style",
   "evidence": "t121r2_probe.py: summary '' -> `[Ex. __ / Bates __] — English:  [AI translation of the Spanish original; check before sending]`. export.py:266 `tr = f\" — English: {_one_line(e['summary'])}\" if e.get(\"translation_label\") else \"\"`.",
   "why_it_matters": "Edits to an empty summary are most likely rejected upstream, so I could not reach this through the API; the pure builder still has no guard and the note would then point at nothing again.",
   "fix": "Build the tail only when the collapsed summary is non-empty, or raise in the builder.",
   "acceptance_test": "A unit test with summary '' asserts no 'English:' fragment on the line."}
 ],
 "whats_right": ["r1 major fixed at the right place: the translated summary sits on the one-line entry, in front of the note, with the multi-line case tested.", "The whitespace-only collapse is documented (export.py:253 docstring, api.md:373) and the no-op mutant that survived r1 is now killed.", "Default and style=standard letters stay byte-equal to evals/golden; build_export is still a pure function of accepted items and an unknown style fails with a ValueError / 422."],
 "questions_for_chris": []}
```
