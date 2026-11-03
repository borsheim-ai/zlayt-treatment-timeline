# T-072 round 2: claims-adjuster-reviewer (D-040 follow-through, commit cab0068)

**Verdict: fail** (two blockers, one major, two minors). The round-1 blocker is closed: the mock overlays now say "Reported onset" and the frontend guard test passes. The D-040 rule still fails in two backend strings the card did not touch, and the guard test does not scan the backend, so it cannot catch them.

Model: claude-haiku-5-5 (the running model; the dossier's expected id does not match what is running).
Scope note: HEAD moved during the review (b9d3ead, then 43fc69e). I reviewed cab0068 via `git archive` into the scratchpad, not the live tree.

## What I checked

- **Round-1 blocker closed (pass).** `app/frontend/mock_flags.js:24` now reads `mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, ...")`. `app/frontend/dev/mock-data.js:748-749` reads `"title": "Reported onset"` and `"explanation": "Onset wording reported in ..."`. `grep -c -i 'self-report' app/frontend/dev/mock-data.js` returns 0.
- **Frontend grep (pass).** `grep -rn -i -P 'self[-\s]?report' app/frontend` at cab0068 returns only `app/frontend/review.css:27` and `app/frontend/review.js:276`, both the internal class `rv-selfreport`. Those are allowed.
- **Guard test (passes; scope too narrow).** `tests/unit/test_frontend_no_speaker_label.py` passes at cab0068 and on the live tree. It fails on a planted string in `app/frontend` (finding 3 below), but it only walks `app/frontend` (line 8).
- **Backend user-facing text (fails).** See findings 1 and 2.
- **Export and golden (pass, unchanged from r1).** The record 9 quote stays verbatim: "Patient states symptoms began after the January collision."

## Findings

- **F1 blocker. The Why? text for a dropped qualifier names the speaker.** `app/backend/why.py:7` says "The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out." It is user-facing: `app/frontend/timeline.js:119` renders `it.why` as `data-testid="why-text"` in the Why? modal (opened by the button at `timeline.js:31`). Entry `why` is built from it at `app/backend/generator.py:108` and `app/backend/pipeline.py:66`. The reason fires when an edit or a summary drops the quote's qualifier (`app/backend/review.py:76`). D-040: "No code or model labels who is speaking." This sentence tells the paralegal the quoted text is a patient statement. It is the same speaker label in another string. I did not render it in a browser. The default sample outputs do not carry it; it appears on the edit and live path.
- **F2 blocker. The literal "self-report" is still in user-facing text, so the brief's own grep check fails.** `app/backend/narrative.py:19` says "The sentence drops a hedge, self-report marker or negation that the cited quote has." It is rendered at `app/frontend/narrative.js:55` (`r.message || r.reason`), with the message set at `app/backend/narrative.py:118` (`r["message"] = REASONS.get(...)`). The grep at cab0068 returns this line; the other backend hits are comments (`narrative.py:4`, `grounding.py:58`), which are not user-facing. R-FL-7 (`spec/REQUIREMENTS.md:71`) acceptance says "No user-facing text contains 'self-report'". At cab0068 the product fails that cell.
- **F3 major. The guard test does not scan the backend, where F1 and F2 sit.** `tests/unit/test_frontend_no_speaker_label.py:8` sets `FRONTEND = ... / "app" / "frontend"`. Mutation check in a scratch copy: appending `PLANT_TEXT = "Patient self-report"` to `app/backend/why.py` gives `1 passed in 0.02s`, exit 0. The same string appended to `app/frontend/mock_flags.js` gives `1 failed`, `D-040 violation: mock_flags.js:58`, exit 1. A regression of the round-1 blocker in the backend would pass CI.
- **F4 minor (carried from r1 F3). Golden flag K3 summary still carries the cut label.** `evals/golden/sample.expected.json:625`: `"summary": "Causation rests on patient self-report, not a physician's causation opinion."` It is qa-owned and not user-facing text, but the expected output still says it.
- **F5 minor (carried from r1 F2). The internal id is public API data.** `app/backend/present.py:74` returns `"category": row["category"]` in every flag payload, and `app/frontend/flags.js:65` writes `"data-category": f.category`. Not rendered as text, so not a blocker, but "never shown to users" in the card overstates it.

## Reproduction

```
git archive cab0068 | tar -x -C <scratchpad>/t072
cd <scratchpad>/t072 && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py   -> 1 passed, exit 0
(plant in app/frontend/mock_flags.js, scratch copy)                                                                 -> 1 failed, exit 1
(plant in app/backend/why.py, scratch copy)                                                                        -> 1 passed, exit 0
.venv/bin/python -c 'import sys; sys.path.insert(0, "app/backend"); import why; print(why.why("SUMMARY_DROPS_QUALIFIER"))'
  -> The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.
```

## Not run

No browser render of `?api=mock`. The "Reported onset" check is the served source text (`app/frontend/index.html:45` loads `mock_flags.js` on every page; `mock_flags.js:24`). The live tree was not used for the verdict.

```json
{"card": "T-072", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2; commit cab0068 (parent 312ed92) via git archive into the scratchpad (t072); live HEAD moved during review (b9d3ead, then 43fc69e) and was not the verdict basis; no browser run; sample case Appendix A records 1-9",
 "exercised": [
  "read personas/claims-adjuster.md in full; reviews/T-072-claims-adjuster.md (r1); reviews/T-074-claims-adjuster.md; memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48)",
  "git log --oneline -5; git merge-base --is-ancestor cab0068 HEAD (ancestor); git show --stat cab0068; git show cab0068 -- app/",
  "git archive cab0068 | tar -x -C <scratchpad>/t072",
  "grep -rn -i -P 'self[-\\s]?report' app/ at cab0068 archive (backend hits: narrative.py:4, narrative.py:19, grounding.py:58; frontend hits: review.js:276, review.css:27 only)",
  "grep -c -i 'self-report' app/frontend/dev/mock-data.js -> 0; sed -n 745,752p mock-data.js; grep -n 'f_pat_9' app/frontend/mock_flags.js -> line 24",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py at cab0068 archive -> 1 passed, exit 0; same on live tree -> 1 passed, exit 0",
  "plant 'Patient self-report' in scratch copy app/frontend/mock_flags.js -> 1 failed (D-040 violation: mock_flags.js:58), exit 1",
  "plant 'Patient self-report' in scratch copy app/backend/why.py -> 1 passed, exit 0 (scope gap)",
  "read app/backend/why.py:7; app/backend/narrative.py:19, :62, :118; app/frontend/narrative.js:55; app/frontend/timeline.js:31, :119; app/backend/review.py:76; app/backend/generator.py:108; app/backend/pipeline.py:66; app/frontend/flags.js:65, :68; app/backend/present.py:74; app/frontend/index.html:45",
  ".venv/bin/python -c 'import why; print(why.why(\"SUMMARY_DROPS_QUALIFIER\"))' in the archive app/backend -> prints the patient-statement sentence",
  "grep -rln 'carries a qualifier|SUMMARY_DROPS_QUALIFIER' tests/fixtures evals/golden app/frontend -> only evals/golden/README.md (no fixture carries the why text)",
  "not run: browser ?api=mock render; evals.run (writes evals/reports, outside write paths)"
 ],
 "verdict": "fail",
 "scores": {"d040_user_facing_text_mock_overlays": 5, "d040_user_facing_text_backend_reason_strings": 1, "guard_test_scope_covers_backend": 2, "export_golden_fidelity": 5, "no_invented_facts_or_severity": 5, "tests_green_at_commit": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Backend Why? text names the speaker ('a patient statement') in user-facing text (D-040)",
   "evidence": "app/backend/why.py:7: \"SUMMARY_DROPS_QUALIFIER\": \"The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.\" Rendered: app/frontend/timeline.js:119 (data-testid why-text, Why? modal opened by timeline.js:31) from entry.why at app/backend/generator.py:108 and app/backend/pipeline.py:66. Triggered by app/backend/review.py:76 when an edit or summary drops the quote's qualifier. Not in any sample fixture (grep).",
   "why_it_matters": "memory/ORCHESTRATOR_DECISIONS.md D-040: 'No code or model labels who is speaking.' The sentence tells the paralegal the quoted text is a patient statement. It is the cut speaker label in a different string, so the round-1 fix did not finish the decision. Blocker by the same rule as r1 F1.",
   "fix": "Backend owner: rewrite why.py:7 without a speaker word, e.g. 'The quoted text carries a qualifier (a hedge, a negation, a side or an approximation) that the summary leaves out.' Keep the qualifier check (app/backend/grounding.py:186) unchanged; change only the text.",
   "acceptance_test": "grep -rn -i -P 'patient statement|self[-\\s]?report' app/backend app/frontend returns no user-facing hits; a unit test asserts why.why('SUMMARY_DROPS_QUALIFIER') contains no 'patient' or 'self' word."},
  {"severity": "blocker",
   "title": "Literal 'self-report' remains in user-facing reason text; the brief's grep check fails",
   "evidence": "app/backend/narrative.py:19: \"SUMMARY_DROPS_QUALIFIER\": \"The sentence drops a hedge, self-report marker or negation that the cited quote has.\" Rendered at app/frontend/narrative.js:55 (r.message || r.reason); message set at app/backend/narrative.py:118 (r[\"message\"] = REASONS.get(r[\"reason\"], r[\"reason\"])). grep -rn -i -P 'self[-\\s]?report' app/ at cab0068 returns this line; the other backend hits are comments (narrative.py:4, grounding.py:58) and the allowed CSS class (review.js:276, review.css:27).",
   "why_it_matters": "The round-2 brief allows only the internal CSS class to remain. R-FL-7 (spec/REQUIREMENTS.md:71) acceptance cell says 'No user-facing text contains self-report', so at cab0068 the product fails the spec row it is meant to satisfy.",
   "fix": "Backend owner: change narrative.py:19 to 'The sentence drops a hedge, a marker or a negation that the cited quote has.' (no speaker word). Leave the comments alone; they are not user-facing.",
   "acceptance_test": "grep -rn -i -P 'self[-\\s]?report' app/backend app/frontend returns only rv-selfreport (review.js:276, review.css:27) and comment lines; REASONS['SUMMARY_DROPS_QUALIFIER'] contains no 'self' word."},
  {"severity": "major",
   "title": "The guard test scans app/frontend only, so the backend regression passes",
   "evidence": "tests/unit/test_frontend_no_speaker_label.py:8: FRONTEND = Path(...) / \"app\" / \"frontend\"; :9 BAD = re.compile(r\"self[-\\s]?report\", re.I). Scratch mutation: 'PLANT_TEXT = \"Patient self-report\"' appended to app/backend/why.py -> '1 passed in 0.02s', exit 0. Same string in app/frontend/mock_flags.js -> '1 failed', 'D-040 violation: mock_flags.js:58', exit 1.",
   "why_it_matters": "The round-1 blocker came back in app/backend (F1, F2) and nothing failed. A guard that only watches the place the last fix touched is not a guard for the rule.",
   "fix": "QA owner (tests/**): scan app/backend and app/frontend with the same allowlist, and add the patient-speaker words (patient statement, patient self) to the pattern. Keep the rv-selfreport allowance.",
   "acceptance_test": "In a scratch copy, pytest fails when 'Patient self-report' is planted in app/backend/why.py and when 'a patient statement' is planted in app/backend/narrative.py; passes on cab0068 after F1 and F2 are fixed."},
  {"severity": "minor",
   "title": "Golden flag K3 summary still carries the cut label (carried from r1 F3)",
   "evidence": "evals/golden/sample.expected.json:625 (at cab0068 and 312ed92): \"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\"",
   "why_it_matters": "The golden JSON is the expected-output authority. It still states the speaker label D-040 cut. Not rendered, so minor.",
   "fix": "QA owner (evals/**): replace the summary with a neutral line that quotes record 9 verbatim, e.g. 'Causation language: record 9 verbatim \"Patient states symptoms began after the January collision.\"'. Re-run the evals before merging.",
   "acceptance_test": "grep -n -i 'self-report' evals/golden/sample.expected.json returns only the M10 must_not statement (line 990) or nothing; eval gates unchanged."},
  {"severity": "minor",
   "title": "The internal id 'patient_report' is public API data (carried from r1 F2)",
   "evidence": "app/backend/present.py:74: \"category\": row[\"category\"]; app/frontend/flags.js:65: \"data-category\": f.category. Text rendering uses f.title (flags.js:66).",
   "why_it_matters": "Not text, so not a D-040 violation of user-facing wording. But 'never shown to users' in the card is inaccurate; an adjuster inspecting the payload sees the id.",
   "fix": "Backend owner: either correct the card and decision log to 'not rendered as text; present in API JSON and data-category', or map to a neutral public id in present.py:74 and flags.js:65.",
   "acceptance_test": "Option (a): card and decision note state the exposure. Option (b): GET a sample case's flags and assert no category or data-* value contains 'patient'."}
 ],
 "whats_right": [
  "The round-1 blocker lines are closed: app/frontend/mock_flags.js:24 and app/frontend/dev/mock-data.js:748-749 read 'Reported onset'; grep -c -i 'self-report' app/frontend/dev/mock-data.js is 0.",
  "The frontend guard test passes at cab0068 and fails when 'Patient self-report' is planted in app/frontend (exit 1), with the allowlist limited to the rv-selfreport class.",
  "The record 9 quote stays verbatim in the flag text (mock_flags.js:24, mock-data.js:749) with no added physician or speaker wording."
 ],
 "questions_for_chris": [
  "Is the Why? qualifier text (why.py:7) inside D-040's scope? I read D-040 as covering it. If you read D-040 as chip-only, F1 drops to major and the verdict to changes."
 ]}
```
