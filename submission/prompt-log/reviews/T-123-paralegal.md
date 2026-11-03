# T-123 paralegal review

**Verdict: pass.** No blockers or majors. A same-day paperwork record or a bare questionnaire or authorization header is now named as paperwork in the accident-date flag, in both record orders. The visits-only control keeps its old wording. The conflict is still not resolved by the tool. One minor, found while probing, is not from this change: a non-library preamble line makes ingest count a phantom record 1, which shifts every record number.

Scope: T-123 at HEAD 63e18ed (git archive copy, fixture backend, port 7893, listener PID 87376). The pre-T-123 build is 0c47356^ (d56328a), extracted to the scratchpad and run in-process. The live server refuses synthetic pastes in demo mode, so the synthetic probes ran in-process through the same functions the pipeline calls.

What I checked:
- Library and sample through the live server: 16 cases (sample plus 15 library), accident-date flags only on the sample and lib11, and neither has paperwork on the earliest date (T-123-paralegal-survey.out.json). So the library gives no paperwork-branch case, and the synthetic probes are the only evidence for it.
- Same-day probes, labelled SYNTHETIC, run through IN.ingest, language.annotate and CF.accident_date_conflicts (T-123-paralegal-baseline-HEAD.txt and -pre-T123.txt):
  - P1, intake form then initial evaluation on 2026-01-09: HEAD names record 1 (intake form) as paperwork and gives record 2 as the first visit. Pre-T-123 said "first recorded treatment, January 9, 2026 (Lakeside Clinic, intake form; Lakeside Clinic, initial evaluation)".
  - P2, the same two records in reverse order: HEAD names record 2 as paperwork and record 1 as the first visit.
  - P3, a bare "Patient questionnaire" alone on 2026-01-09: named as paperwork; first visit on 2026-01-16.
  - P4, a bare "Authorization request" alone on 2026-01-09: named as paperwork; first visit on 2026-01-16.
  - P5, visits only: the old wording, "later than the first recorded treatment, January 9, 2026 (Central ER, discharge summary)".
- Sample and lib11 accident sentences are identical before and after (T-123-paralegal-sample-compare-pre.jsonl vs -HEAD.jsonl).
- Unit tests test_t123, test_t120 and test_t121 on the HEAD copy: 48 passed.

Ship-bar score (verify_quickly 4): each paperwork sentence names the record number, the date and the alternative visit, so I could check it against the record in one read. The phantom-record minor lowers my confidence in the numbers on any paste with a preamble.

```json
{"card": "T-123", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); pre-T-123 0c47356^ (d56328a) extracted and run in-process; library cases and sample via the live server; SYNTHETIC probes in-process through app.backend.ingest, language.annotate and conflicts.accident_date_conflicts",
 "exercised": [
  "read board show T-123, personas/paralegal.md, CLAUDE.md",
  "pytest on tests/unit/test_t123_baseline_same_day_paperwork.py, test_t120 and test_t121 on the HEAD copy: 48 passed",
  "HTTP on :7893: GET /api/library, POST /api/cases for the sample and all 15 library cases, poll to ready, read accident-date flags (artifacts/review-evidence/T-123-paralegal-survey.out.json)",
  "in-process baseline probes P1 to P5 on HEAD and on d56328a (artifacts/review-evidence/T-123-paralegal-baseline-HEAD.txt, T-123-paralegal-baseline-pre-T123.txt, T-123-paralegal-baseline.out.json)",
  "in-process sample and lib11 accident sentence, HEAD and d56328a (artifacts/review-evidence/T-123-paralegal-sample-compare-HEAD.jsonl, -pre.jsonl)",
  "record numbering probe with three preamble wordings (artifacts/review-evidence/T-123-paralegal-preamble.txt)",
  "a POST /api/cases with pasted text returned 409 demo_mode_unsupported_input on :7893 (api.py:288), which is why the synthetic probes are in-process"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "accident_baseline_wording": 5},
 "findings": [
  {"severity": "minor",
   "title": "Outside T-123's change, pre-existing: a preamble line that is not the library wording makes ingest count a phantom record 1",
   "evidence": "artifacts/review-evidence/T-123-paralegal-preamble.txt: 'SYNTHETIC — invented for a review probe;' -> [(1, ''), (2, 'Lakeside Clinic, intake form')]; the same record with the library wording 'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]; with no preamble -> [(1, 'Lakeside Clinic, intake form')].",
   "why_it_matters": "Every record number the paralegal cites, and every flag that names a record, shifts by one when the paste starts with a header line that is not the library wording. Checklist 3 needs the citation to open the right record in one action. I did not test real fax or cover-sheet text, so the reach of this is unknown.",
   "fix": "Text before the first '=== Record' header, or a block with no Date and no Source, is not a record. Numbering starts at the first real record.",
   "acceptance_test": "Three preamble wordings (library header, free text, fax cover sheet) each give the first real record number 1, with no undated empty-source record, and the flag record numbers in the T-123 probe match the pasted headers."}
 ],
 "whats_right": [
  "a same-day intake form is named as paperwork in both record orders (P1, P2), and a bare questionnaire or authorization request alone on the first date is named as paperwork (P3, P4); pre-T-123 called the same records the first recorded treatment",
  "the visits-only control keeps its old wording, and the sample and lib11 accident sentences are identical before and after",
  "the tool does not choose between the two dates: 'The records disagree; the tool does not choose between them.' and 'Check when treatment actually began before relying on this comparison.'"],
 "questions_for_chris": [
  "In local mode with the fixture backend, a paste that is not a library or recorded case is refused (409 demo_mode_unsupported_input, api.py:288). So the paralegal can only run the sample and the 15 library cases without ENABLE_LIVE. Is that intended for the local build?"]
}
```
