# T-121 paralegal review

**Verdict: pass.** No blockers or majors. Every entry line in both styles matches its raw record: long date, provider as written, verbatim quote, citation placeholder. The "AI translation:" prefix is gone from the summary lines. Two minors: where the translation note sits, and the one-line form is not reachable from the screen.

Scope: T-121 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09 (Spanish, interpreter) and the sample (golden).

What I checked:
- lib09: accepted the 6 entries, 2 charges and 2 rates through the live review route (all 200). Standard and one-line exports both 200 (T-120-123-paralegal-probe.out.json, B_lib09_*).
- Each entry line verified against the raw record text (T-121-paralegal-letter-check.out.json): lib09 6/6 in standard and 6/6 in one-line; sample 9/9 in both. The date is the raw record date in long format, the provider equals the raw Source label, the quote is a verbatim substring of the raw excerpt.
- Translation label before and after: the parent prints "LINE: AI translation: Patient reports pain 6/10 that worsens when raising the arm..." and "LINE: AI translation: Account statement: ..." (T-121-paralegal-before-after-parent.txt). HEAD prints neither; the note sits at the end of the Source line (T-121-paralegal-before-after-HEAD.txt). Billed total $5,090.00 on both builds; the unclear amounts stay out.
- Sample: accepted all 9 entries and the amounts. The standard letter equals the LETTER_TEXT block of evals/golden/sample.export.expected.txt (exact match). One-line export is 9 lines, one per entry, with the same two charges.
- ?style=Oneline and ?style=bogus both return 422 invalid_style.
- Frontend: app/frontend/api.js:43 calls GET /export with no style, and `grep -rl oneline app/frontend` returns no file, so the screen cannot request the one-line form.

Ship-bar score (verify_quickly 4): each entry line carries its date, provider, verbatim quote and citation placeholder, so I could check a line in one read. Spanish lines are slower because the English summary and the Spanish quote are not paired and the note sits next to the quote.

```json
{"card": "T-121", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); library case_lib09; sample evals/golden/sample.txt; app/frontend/api.js",
 "exercised": [
  "read board show T-121, personas/paralegal.md, CLAUDE.md",
  "pytest on tests/unit/test_t121_letter_styles.py (with test_t120 and test_t123, 48 passed on the HEAD copy)",
  "HTTP on :7893: POST /api/cases {library: case_lib09...}, run, poll ready; POST /items/{id}/review accept on 6 entries, 2 charges and 2 rates (all 200); GET /export and GET /export?style=oneline (both 200); GET ?style=Oneline and ?style=bogus (422 invalid_style)",
  "HTTP on :7893: sample accepted, standard letter compared with the golden LETTER_TEXT block (exact match), one-line export (9 lines)",
  "HTTP on :7894: the same lib09 accept and standard export on the parent build (T-121-paralegal-before-after-parent.txt)",
  "letter verification script: every entry line in both styles against the raw library/sample text (T-121-paralegal-letter-check.txt and .out.json)",
  "grep of app/frontend for oneline and style (0 hits); api.js:43 exportCase"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "verbatim_quotes": 5, "translation_note_placement": 3},
 "findings": [
  {"severity": "minor",
   "title": "The translation note sits on the Spanish quote line, not on the English summary it describes; in one-line style the line has no English text",
   "evidence": "artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt: 'LINE: Source [Ex. __ / Bates __]: \"Refiere dolor 6/10 que empeora al levantar el brazo. ...\" [AI translation of the Spanish original; check before sending]'. One-line export (artifacts/review-evidence/T-120-123-paralegal-probe.out.json, B_lib09_oneline_letter): 'April 14, 2026 — Consultorio Médico Aguaclara, nota de consulta: \"Refiere dolor 6/10 ...\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]'.",
   "why_it_matters": "The thing to check is the English summary line above, and it carries no marker. The warning reads as a comment on the Spanish original, which is not a translation. In one-line style nothing on the line is translated, so the note describes text the line does not have. A paralegal who deletes the note by mistake leaves an unmarked AI summary.",
   "fix": "In standard style put the marker on the summary line that holds the AI translation. In one-line style print the note only when the line carries translated text, or move it to the internal notes (see question 1).",
   "acceptance_test": "lib09 standard export: the bracketed phrase is on the same line as the AI-translated summary of each Spanish entry. lib09 one-line export: no bracketed claim on a line that holds only the Spanish quote, or the question-1 decision is recorded."},
  {"severity": "minor",
   "title": "The one-line style cannot be reached from the app; the screen always gets the standard letter",
   "evidence": "app/frontend/api.js:43: exportCase: (token) => call(\"GET\", t(token) + \"/export\"). grep -rl oneline app/frontend: 0 files. The card handoff says a style toggle is left to frontend.",
   "why_it_matters": "The goal is an export she can paste with minimal reformatting. The one-line form exists only through a direct GET with ?style=oneline, so the paralegal cannot choose it on the screen. The card's AC is API-level, so this is a gap for the next card rather than a failure of T-121.",
   "fix": "Add a style control to the export panel that calls /export?style=oneline and shows the returned letter_text unchanged.",
   "acceptance_test": "In the app, choosing the one-line option shows letter_text byte-equal to GET /export?style=oneline for lib09 and sample."}
 ],
 "whats_right": [
  "every entry line in both styles verifies against the raw record: lib09 6/6 and sample 9/9, date, provider as written, verbatim quote (T-121-paralegal-letter-check.out.json)",
  "the 'AI translation:' prefix is gone from the summary lines (the parent prints it twice on lib09); the billed total stays $5,090.00 with the unclear amounts out",
  "the sample standard letter equals the golden LETTER_TEXT block exactly, and invalid style values return 422 invalid_style"],
 "questions_for_chris": [
  "Decision needed: D-001 keeps notes out of the letter body. The translation warning sits inside the letter by design (card AC 2 and the pass-2 F9 request asked for a bracketed, removable phrase). Keep it in the letter, or move it to the internal notes and keep only the translated summary in the letter?",
  "For Spanish entries the one-line form carries only the Spanish quote, with no English. Is a Spanish-only quote acceptable in a demand to an English-speaking adjuster, or should the one-line form carry the English summary too?"]
}
```
