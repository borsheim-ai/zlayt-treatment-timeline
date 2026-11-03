# T-072 round 4: claims-adjuster-reviewer (commit 38a1efb)

**Verdict: changes.** No blocker. One major (a guard exemption that lets a non-verbatim "patient states" line through, so brief check 1 is not met on that line), two minors carried from r3, one nit.

Scope: commit 38a1efb, read through `git archive` into the scratchpad (`t072r4`). The live tree is dirty (uncommitted edits to board/, .claude/ and tests), so no result below comes from the live tree. No browser run.

## Brief checks

1. **No user-facing "self-report", "self report", "patient states" or "patient statement" in app/ (fail on one line).**
   - "self-report" / "self report": clean for user-facing text. The only hits are `review.css:27` and `review.js:293` (internal class `rv-selfreport`; the chip text is "Entered by reviewer"), a docstring at `narrative.py:4`, a comment at `grounding.py:58`, and lexicon.yaml comments and metadata (lines 26, 86, 90, 496, 764). No code reads the lexicon `rationale`, `false_positive` or `note` fields.
   - "patient statement": clean for user-facing text. Hits are a lexicon comment (`lexicon.yaml:84`) and model-facing prompts (`narrative_v1.md:7`, "Attribute patient statements to the patient.").
   - "patient states": one hit that is not verbatim record text, `app/frontend/mock.js:15` (F1). Every other hit is a verbatim Appendix A excerpt or a neutral template around one (see check 2).
2. **Verbatim exemption (partly fails).** The exemption is per file (`test_frontend_no_speaker_label.py:17` VERBATIM_FIXTURES, `:24` `check_states = rel not in VERBATIM_FIXTURES`), not per line. The lines I read in the four exempt files are verbatim or template-plus-verbatim: `mock-data.js:142`, `:415`, `:754`, `mock_flags.js:25`, `mock_sample.js:2` are record 9 text (`mock_sample.js:2` matches the Appendix A sentence exactly); `mock-data.js:749` and `mock_flags.js:24` are the neutral "Onset wording reported in ..." template around the quote; `mock-data.js:412` is "Summary:" plus a verbatim substring cut at "Jan". `mock.js:15` is not verbatim: the record says "Recommend cervical epidural steroid injection. Patient states ...", the mock says "Cervical epidural steroid injection recommended; patient states ...". The file-level exemption passes it (plant F8 below).
3. **Both guard tests pass (pass).** `11 passed` for the two files at 38a1efb. Full unit suite `996 passed`.
4. **Each guard fails on a planted string (pass, with F8 as the exception).** Results in the table below.

## Plant results (each a fresh copy of the 38a1efb archive; string appended with tee -a)

| Plant | File | Planted text | Result |
|---|---|---|---|
| base | none | none | 11 passed, exit 0 |
| B1 | app/backend/why.py | `PLANT_B1 = "an attribution such as patient states"` | FAIL (`why.py:71`), exit 1 |
| B2 | app/backend/narrative.py | `PLANT_B2 = "a patient statement"` | FAIL, exit 1 |
| B3 | app/backend/why.py | `PLANT_B3 = "Patient self-report"` | FAIL, exit 1 |
| B4 | app/backend/why.py | `PLANT_B4 = "self report"` | FAIL, exit 1 |
| F1 | app/frontend/review.js | `// PLANT_F1 an attribution such as patient states` | FAIL, exit 1 |
| F2 | app/frontend/review.js | `// PLANT_F2 a patient statement` | FAIL, exit 1 |
| F3 | app/frontend/mock_flags.js | `// PLANT_F3 Patient self-report` | FAIL, exit 1 |
| F4 | app/frontend/mock_flags.js | `// PLANT_F4 Patient states symptoms began after the January collision.` (verbatim) | PASS, exit 0 (expected) |
| F5 | app/frontend/timeline.js | `// PLANT_F5 self report` | FAIL, exit 1 |
| F6 | app/frontend/timeline.js | `// PLANT_F6 patient states` | FAIL, exit 1 |
| F7 | app/frontend/mock.js | `// PLANT_F7 patient statement` | FAIL, exit 1 |
| F8 | app/frontend/mock.js | `// PLANT_F8 Cervical epidural steroid injection recommended; patient states symptoms began.` (paraphrase) | **PASS, exit 0 (gap, F1)** |

## Closed since r3

- r3 F1 (blocker, reason text names the speaker): closed. `why.py:7` and `narrative.py:19` now say "an attribution phrase". No "patient states" in either file.
- r3 F2 (major, guard coverage): closed for the four banned phrases. The backend BAD pattern now includes `patient states`; the frontend scan covers `patient statement` and `patient self` everywhere and `patient states` outside the four exempt files. The remaining hole is the file-level exemption (F1).

## Findings

- **F1 major. A non-verbatim summary with "patient states" passes because its whole file is exempt.** `app/frontend/mock.js:15` at 38a1efb: `9: "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.",`. It is shown as the entry summary in mock mode (`mock.js:80`, `:87`: `summary = sm`). Record 9 verbatim is `Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.` (`mock_sample.js:2`). Plant F8 passes; the same phrase in `timeline.js` (F6) fails. The card's AC says "patient states outside verbatim mock files"; mock.js is not verbatim-only. A regression in mock.js would not fail CI. The same wording is also the product's designed output: `grounding.py:185` (D-022 carry, comment "D-040: nothing labels who is speaking") makes an entry `needs_review` when the summary drops "states" from a quote that has it. The golden letter carries it at `evals/golden/sample.export.expected.txt:37`. The backend guard does not scan model output, so mock.js is the only place this literal rule is tested. Whether D-040 reaches summary text is a spec question (see questions_for_chris); I am not treating the attribution itself as an invented fact. My reading from the adjuster's side: "patient states" is the record's own marker and is accurate.
- **F2 minor (carried, r3 F3, r2 F4). The golden flag K3 summary still carries the cut label.** `evals/golden/sample.expected.json:625` at 38a1efb: `"summary": "Causation rests on patient self-report, not a physician's causation opinion."`. It is qa-owned and not rendered, and it is outside the brief's app/ grep. The must_not at `:990` is a legitimate use of the term.
- **F3 minor (carried, r3 F4, r1 F2, r2 F5). The internal id `patient_report` is in the public flag payload.** `app/backend/present.py:74` (`"category": row["category"]`) and `app/frontend/flags.js:65` (`"data-category": f.category`). Text renders `f.title` (`flags.js:66`), so this is not a wording violation. The card note says "the id is never shown to users"; that is inaccurate for the payload and the DOM attribute. Unchanged in 38a1efb.
- **F4 nit. The frontend guard's ALLOWED test is dead code.** `test_frontend_no_speaker_label.py:16` and `:28`: the BAD match can only be "self-report" / "selfreport" / "patient statement" / "patient self", so `m.group(0).lower() in ALLOWED` never fires. The adjacency check on the next clause does the real work, and it is correct. Harmless; simplify when the test is next touched.

## Reproduction

```
git rev-parse --short HEAD -> (dirty tree; reviewed commit is 38a1efb)
git show --stat 38a1efb    -> 5 files: grounding.py, narrative.py, why.py, test_backend_no_speaker_label.py, test_frontend_no_speaker_label.py
git archive 38a1efb | tar -x -C <scratchpad>/t072r4
cd <scratchpad>/t072r4 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_backend_no_speaker_label.py tests/unit/test_frontend_no_speaker_label.py
  -> 11 passed in 0.12s, exit 0
  ... tests/unit -> 996 passed in 20.49s
git grep -n -i -E 'self[- ]?report' 38a1efb -- app/        -> hits as listed in check 1
git grep -n -F 'patient states' 38a1efb -- app/frontend    -> mock-data.js:142,412,415,749,754; mock.js:15; mock_flags.js:24,25; mock_sample.js:2
git grep -n -F 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.' 38a1efb -- app/  -> app/frontend/mock.js:15 only
plants B1-B4, F1-F8 in <scratchpad>/t072r4_plants/<name> (cp -R of the archive, then tee -a); both guard tests run in each
```

## Not run

- Browser render of `?api=mock` (the Why? modal and the mock.js summary path).
- `evals.run` (writes evals/reports, outside my write paths).
- Live-tree plants (the live tree is dirty).

```json
{"card": "T-072", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 4; commit 38a1efb read via git archive into the scratchpad (t072r4); plants in the scratchpad (t072r4_plants); app/ grep via git grep at 38a1efb; live tree dirty and not used for results; Appendix A sample case (record 9 text, golden K3, golden export line 37); no browser run",
 "exercised": [
  "read personas/claims-adjuster.md in full; read reviews/T-072-claims-adjuster-r3.md in full; read .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md and project_d040_label_cut_residue.md",
  "git rev-parse --short HEAD; git cat-file -t 38a1efb (commit); git show --stat 38a1efb; git merge-base --is-ancestor 38a1efb HEAD (ancestor); git status --short (dirty tree, not used)",
  "python3 tools/board.py show T-072 (status in_review, rounds 3, commits include 38a1efb; notes 2026-11-02T02:47:25Z and 03:05:56Z)",
  "git archive 38a1efb | tar -x -C <scratchpad>/t072r4; git show 38a1efb -- app tests (full diff read)",
  "read tests/unit/test_backend_no_speaker_label.py (88 lines) and tests/unit/test_frontend_no_speaker_label.py (full) at 38a1efb",
  "cd archive && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_backend_no_speaker_label.py tests/unit/test_frontend_no_speaker_label.py -> 11 passed, exit 0",
  "cd archive && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -> 996 passed in 20.49s",
  "git grep -n -i -E 'self[- ]?report' 38a1efb -- app/; git grep -n -i -E 'patient[ -]statement' 38a1efb -- app/; git grep -n -i -E 'patient[ \\t]+states' 38a1efb -- app/; git grep -n -i -E 'patient[ -]self' 38a1efb -- app/",
  "git grep -n -i -E 'patient[ -](report|reports|reported|says|said|own)|own statement' 38a1efb -- app/frontend app/backend; git grep -n -i 'patient' 38a1efb -- app/backend app/frontend/*.js (non-mock)",
  "git grep -n -F 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.' 38a1efb -- app/ (mock.js:15 only); git grep -c -F of the record 9 sentence in app/frontend/mock_sample.js (1)",
  "git show 38a1efb:app/frontend/mock.js lines 78-87 (SAMPLE_SUMMARIES feeds summary = sm at :87)",
  "git show 38a1efb:app/backend/grounding.py lines 168-185 (_SELF_CARRIED at :169; dropped_qualifiers self_report check at :185)",
  "git show 38a1efb:memory/ORCHESTRATOR_DECISIONS.md D-022 (line 30) and D-040 (line 48) read in full",
  "git grep -n 'rationale|false_positive|note' 38a1efb -- 'app/*.py' (no hits; no code reads lexicon metadata); app/backend/present.py:74 and app/frontend/flags.js:65 read",
  "git grep -n for 'patient self-report' and 'patient states' in evals/golden (sample.expected.json:625, :990; sample.export.expected.txt:37, :38, :58, :69; check_golden.py:491, :543)",
  "plants in scratch copies (cp -R of the archive, then tee -a of one line): B1 why.py 'an attribution such as patient states' FAIL; B2 narrative.py 'a patient statement' FAIL; B3 why.py 'Patient self-report' FAIL; B4 why.py 'self report' FAIL; F1 review.js 'an attribution such as patient states' FAIL; F2 review.js 'a patient statement' FAIL; F3 mock_flags.js 'Patient self-report' FAIL; F4 mock_flags.js verbatim 'Patient states symptoms began after the January collision.' PASS; F5 timeline.js 'self report' FAIL; F6 timeline.js 'patient states' FAIL; F7 mock.js 'patient statement' FAIL; F8 mock.js paraphrase 'Cervical epidural steroid injection recommended; patient states symptoms began.' PASS (gap)"
 ],
 "verdict": "changes",
 "scores": {"d040_reason_strings_no_speaker": 5, "d040_user_facing_grep_clean": 3, "guard_coverage_matches_wording": 3, "export_golden_fidelity": 3, "no_invented_facts_or_severity": 5, "tests_green_at_commit": 5},
 "findings": [
  {"severity": "major",
   "title": "mock.js:15 carries a non-verbatim summary with 'patient states' that the file-level exemption passes; brief check 1 is not met on that line",
   "evidence": "app/frontend/mock.js:15 at 38a1efb: 9: \"Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.\" Record 9 verbatim (app/frontend/mock_sample.js:2, exact sentence count 1): 'Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.' Shown as the entry summary in mock mode: app/frontend/mock.js:80, :87 (summary = sm). tests/unit/test_frontend_no_speaker_label.py:17 VERBATIM_FIXTURES and :24 check_states = rel not in VERBATIM_FIXTURES. Repro: plant F8 ('// PLANT_F8 Cervical epidural steroid injection recommended; patient states symptoms began.') appended to app/frontend/mock.js: both guards PASS (11 passed, exit 0). Same phrase in app/frontend/timeline.js (F6): FAIL.",
   "why_it_matters": "The exemption was written for verbatim record text (card AC: 'patient states outside verbatim mock files'). It is per file, so any non-verbatim line in the four exempt files passes, and mock.js:15 is a paraphrase. The card's claim is false for this file, and a regression in mock.js would not fail CI. The same wording is the product's designed output: grounding.py:185 (D-022 carry; comment 'D-040: nothing labels who is speaking') makes an entry needs_review when the summary drops 'states'; the golden letter carries it at evals/golden/sample.export.expected.txt:37. The backend guard does not scan model output, so mock.js is the only place the literal rule is tested. Whether D-040 reaches summary text is a spec question (questions_for_chris). The attribution itself is the record's own marker and is accurate; I am not calling it an invented fact.",
   "fix": "Frontend and qa (tests/**): (a) make the exemption line-level: a 'patient states' line in an exempt file passes only if it contains an exact Appendix A excerpt (the test reads the excerpt from mock_sample.js or spec/SAMPLE_CASE_TRUTHS.md); mock.js:15 then fails unless its summary is reworded. (b) If Chris rules that summaries may keep the record's attribution, say so in the guard docstring, remove mock.js from VERBATIM_FIXTURES, and add a named allowance for SAMPLE_SUMMARIES only. Either way, record the decision in memory/ORCHESTRATOR_DECISIONS.md and correct the card AC wording.",
   "acceptance_test": "In a scratch copy of 38a1efb, appending '// PLANT_F8 Cervical epidural steroid injection recommended; patient states symptoms began.' to app/frontend/mock.js makes tests/unit/test_frontend_no_speaker_label.py fail. mock-data.js:415, :754, mock_flags.js:25 and mock_sample.js:2 still pass. git grep -n -F 'patient states' <commit> -- app/frontend returns only verbatim Appendix A lines (or a documented allowance)."},
  {"severity": "minor",
   "title": "Golden flag K3 summary still carries the cut label 'patient self-report' (carried from r3 F3 and r2 F4)",
   "evidence": "evals/golden/sample.expected.json:625 at 38a1efb: \"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\"",
   "why_it_matters": "It is the expected-output authority for the flag and still states the label D-040 cut. It is not rendered, and it is outside the brief's app/ grep, so minor. The must_not at sample.expected.json:990 is a legitimate use of the term.",
   "fix": "qa (evals/**): replace the summary with a neutral line that quotes record 9 verbatim, for example 'Causation language: record 9 verbatim \"Patient states symptoms began after the January collision.\"', consistent with whatever Chris rules on the question below. Re-run the evals before merging.",
   "acceptance_test": "git grep -n -i 'self-report' <commit> -- evals/golden/sample.expected.json returns only the :990 must_not line, or nothing."},
  {"severity": "minor",
   "title": "The internal id 'patient_report' is in the public flag payload; the card says it is never shown to users (carried from r3 F4, r1 F2, r2 F5)",
   "evidence": "app/backend/present.py:74 at 38a1efb: \"category\": row[\"category\"] in flag_view. app/frontend/flags.js:65: \"data-category\": f.category. Text renders f.title (flags.js:66). Card T-072 note 2026-11-02T02:47:25Z: 'the id is never shown to users'. app/llm/prompts/flags_v1.md:13 defines the id as 'the patient's own statement' (model-facing).",
   "why_it_matters": "Not rendered as text, so not a wording violation. But an adjuster who opens the payload or the DOM attribute sees the speaker id, and the card and decision note overstate it. Unchanged in 38a1efb.",
   "fix": "Backend: correct the card and decision note to 'not rendered as text; present in API JSON and data-category', or map to a neutral public id at present.py:74 and flags.js:65.",
   "acceptance_test": "Option (a): card and decision note state the exposure. Option (b): a GET of a sample case flags payload has no category or data-category value containing 'patient'."},
  {"severity": "nit",
   "title": "Frontend guard ALLOWED membership test can never fire",
   "evidence": "tests/unit/test_frontend_no_speaker_label.py:16 ALLOWED = {\"rv-selfreport\"} and :28 m.group(0).lower() in ALLOWED. BAD (line 14) can only match 'self-report', 'selfreport', 'patient statement' or 'patient self', never 'rv-selfreport'.",
   "why_it_matters": "Harmless: the adjacency check on the next clause (rv-selfreport in the 3-character window) is what allows the CSS class. It misleads the next reader about how the allowance works.",
   "fix": "QA: delete the dead ALLOWED membership test or comment that the window check is the allowance.",
   "acceptance_test": "Both guard tests still pass; planting 'Patient self-report' in review.js still fails."}
 ],
 "whats_right": [
  "why.py:7 and narrative.py:19 no longer name the speaker ('an attribution phrase'); the r3 F1 blocker is closed.",
  "Both guard scans fail on each banned phrase planted outside the four mock files (B1-B4, F1-F3, F5-F7), and the backend scan is AST-based so docstrings and comments do not trip it.",
  "Both guard tests pass at 38a1efb (11 passed) and the full unit suite passes (996 passed)."
 ],
 "questions_for_chris": [
  "D-022 requires a summary to keep the record's attribution when the excerpt has it (grounding.py:169 and :185, with the comment 'D-040: nothing labels who is speaking'). D-040 says 'No code or model labels who is speaking.' Does D-040 reach attribution carried inside a model or code summary (the letter line 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.', sample.export.expected.txt:37), or only chips, reason text and excerpt labels? If it reaches summaries, the grounding.py:185 carry rule must change and this review becomes fail (F1 becomes a blocker). If it does not, take fix (a) for F1."
 ]}
```
