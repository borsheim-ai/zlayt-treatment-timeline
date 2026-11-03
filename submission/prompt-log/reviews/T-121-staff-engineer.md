# T-121 staff-engineer review (commit c26ff04)

Verdict: changes. The style option is built by code, the default letter still equals the golden, and the API rejects bad styles. The one-line style has two defects: it prints a "translation" note over a letter line with no translation in it, and it rewrites the quote's whitespace without a test that would notice.

Exercised (archive of c26ff04, project venv):
- `pytest tests/unit -q`: 2816 passed, 4 skipped. This includes the golden byte-equal test and the updated Spanish and D-050 tests.
- `python -m evals.run --check-spec`: letter_equal true, internal_notes_equal true.
- A probe script (scratch) building the letter with a Spanish-labelled entry that has a multi-line excerpt, in both styles.
- Six mutants against tests/unit/test_t121_letter_styles.py: dropping the note, ignoring the style, dropping the PDF page, removing the API check and dropping the note from one-line are all killed. A no-op `_one_line` survives.
- Read the diff in full (export.py, export_routes.py, api.py, api.md). There is no LLM call, no float and no network. Both routes validate the style before building.

```json
{"card": "T-121", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04: app/backend/export.py, export_routes.py, api.py, memory/contracts/api.md, tests/unit/test_t121_letter_styles.py, test_spanish_records.py, test_d050_never_verified.py",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "python -m evals.run --check-spec: letter_equal true", "probe: Spanish-labelled entry with multi-line excerpt, standard vs oneline", "6 mutants on test_t121_letter_styles.py: 5 killed, 1 survived (_one_line no-op)", "read git show c26ff04 in full"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "One-line style prints an 'AI translation' note on a line that has no translation",
   "evidence": "app/backend/export.py:259 the oneline branch emits only the date, provider, quote and bracket, plus `_translation_note(e)`; the summary (the English translation, or the reviewer's edited translation) is never printed. Probe output: `January 9, 2026 — Austin EMS run report: \"Conductor con cinturon. Dolor lumbar 7/10.\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]`. The standard style prints the translation on the line above the quote. tests/unit/test_t121_letter_styles.py::test_api_style_param_and_unknown_style only asserts the note count and that ES_QUOTE is present, not that any translation is.",
   "why_it_matters": "The note tells the paralegal an AI translation is here to check. In this style there is nothing to check, and the reviewer's edited translation (Translation (edited by reviewer)) is lost from the letter. A Spanish quote may reach the demand letter with a note about a translation that was never written.",
   "fix": "For a translated entry in the one-line style, either append the translation inside the line (for example after the quote, before the bracketed note) or reword the note to say the quote is untranslated. Do not claim a translation that is not on the line.",
   "acceptance_test": "Add a test: a Spanish-labelled entry in style=oneline must contain its summary text on the same line as the note (or the reworded note), for both labels AI translation and Translation (edited by reviewer). Mutant dropping the summary from that line must fail."},
  {"severity": "minor",
   "title": "One-line style collapses whitespace inside the quote, so it is no longer a verbatim substring; the test cannot see it",
   "evidence": "export.py:248-250 `_one_line` and :259 `_one_line(e[\"excerpt\"])`. Probe: excerpt 'Conductor con cinturon.\\n  Dolor   lumbar 7/10.' gives `excerpt in oneline_letter` False, while the standard style keeps it verbatim. Mutant `_one_line` -> `str(s)` SURVIVED all 10 tests in test_t121_letter_styles.py, because the sample excerpts are single-line (test_oneline_quote_is_still_a_substring_of_the_record_and_has_no_newline is therefore vacuous for its 'no newline' half).",
   "why_it_matters": "The letter's quote is the product's grounded text. Whitespace-only normalization is acceptable if it is documented, but here it is undocumented and unpinned, so a later change could silently change quotes.",
   "fix": "Document the normalization (whitespace only) in the docstring and api.md, and add a multi-line-excerpt test that asserts the collapsed form equals the whitespace-normalized excerpt and contains no newline.",
   "acceptance_test": "Test with excerpt 'a\\n  b' asserts the one-line letter contains '\"a b\"' and no other newline inside the entry line; the no-op mutant must fail."},
  {"severity": "nit",
   "title": "Style validation is duplicated in two routes",
   "evidence": "app/backend/api.py:520-523 and app/backend/export_routes.py:71 both check the style and build the 422.",
   "why_it_matters": "Two copies of the same check will drift; only one route answers at a time.",
   "fix": "Keep one route and call a shared helper.",
   "acceptance_test": "Optional: a test that both routes return the same body for ?style=fancy."}
 ],
 "whats_right": ["Default and style=standard letters stay byte-equal to evals/golden; build_export stays a pure function of accepted items.", "Invalid style fails fast with 422 invalid_style and a ValueError in the pure builder, no silent fallback.", "The bracketed note is keyed to the translation label and tested to end the entry in both styles."],
 "questions_for_chris": []}
```
