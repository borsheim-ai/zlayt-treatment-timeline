# T-132 staff-engineer review, round 1 (commit f4d68bb)

Verdict: changes. One major, three minors, no blockers. The AC forms work: the semicolon and newline forms of "attribution only" now give ONE flag whose quote carries the condition, `Hx per MS history.` flags, and titled persons still count as a source. The same defect survives when the attribution phrase itself wraps across a line break, and three of fourteen mutants survive the new tests.

Scope: `git archive f4d68bb` (parent `f4d68bb^` as control) in the session scratchpad (`T132r1/arch`, `T132r1p/arch`). HEAD is now 2790918; `git diff --stat f4d68bb HEAD -- app/backend/lexicon_scan.py app/backend/sentences.py` printed nothing, so the code under review is HEAD's. Python is `.venv/bin/python`.

## What I exercised

- `python3 tools/board.py show T-132`; reviews/T-120-paralegal-r3.md; reviews/T-120-staff-engineer-r3.md; `git show f4d68bb -- app/backend/lexicon_scan.py` in full; the new test file in full; flags.py `lexicon_flags` and `merge`.
- `pytest tests/unit -q` on the archive: 3213 passed, 4 skipped, 187.70 s. `pytest tests/unit/test_t132_attribution_unit.py tests/unit/test_t120_history_source_sentence.py`: 122 passed.
- Probe `artifacts/review-evidence/T-132-probe.py`: 37 sentences through `flags.lexicon_flags` (the real quote path), on f4d68bb and on the parent. Output `T-132-probe-HEAD-f4d68bb.txt` and `T-132-probe-parent.txt` (`grep -c '^\['` gives 37 each). Each row checks that every quote is a contiguous substring of the record text, and whether two flags overlap.
- Wrap probe `T-132-wrap-probe.py` (5 hard-wrapped variants), and a 5-row probe of edge forms (no-space, `Hx\nper EMS`, blank line).
- Mutants `T-132-mutants.py`: 14 mutants of `lexicon_scan.py` against t132 + t120 test files; then M8, M9, M10 re-run by hand in separate copies to show behaviour.
- `python -m app.pipeline evals/golden/sample.txt` twice (fixture): exit 0 both, `cmp` identical. `python -m evals.run --backend fixture` on f4d68bb and parent: `evals/reports/latest.json` flattened, 508 leaves, 0 differences outside timestamps (pre_existing precision and recall 1.0 on both). The run exits 1 on `ship_bar_met=False` from fixture-backend blockers (determinism_3run needs a live backend), same on the parent.
- Paralegal view (below): live app on 127.0.0.1:7947, PID 96204.
- Note: my first start on port 7931 hit a listener (PID 88327, cwd another agent's `wt_r5`) that was not mine. My POST of one library case created a case on it before I noticed; I did not touch its process. I moved to 7947.

## Checks asked for

| Check | Result |
|---|---|
| Attribution-only unit ending at `;` or newline extends one clause, same sentence | A1-A6, A20, A24, A30-A33, A37 extend; A5 `Hx per interpreter; neck pain; headaches.` stops at `neck pain;` |
| No duplicate flags | A1-A3: one flag, both lexicon ids (parent gave two). **Fails** for chains (finding 2) |
| `Hx per MS history.` flags | A13 yes, A14 `Hx per patient, MS diagnosis.` yes (parent: none) |
| Titled names still a source | A16 `Dr Lee`, A17 `Ms. Alvarez`, A18 `Mr Smith`: no flag, as the parent |
| Must NOT extend: next clause in another sentence | A10, A11, A12: no extension (A10, A12 raise nothing; A11 flags only `Prior neck pain and headaches.`) |
| Must NOT extend: unit not attribution-only | A21, A22, A23, A27: quote stays the unit that already names the condition |
| Quotes verbatim and contiguous | all 37 rows `verbatim`; the quote is `text[a:b]` of one record |
| No LLM call, no clock | `git show f4d68bb` adds only regex and span code; grep of the diff for `except`, `float(`, `sleep(`, `retry`: none |

## Findings

1. **major: a hard-wrapped attribution phrase still yields a fragment quote with no condition.** `"Hx obtained\nvia patient's son; neck pain and headaches."` flags `'Hx obtained'`; `"Hx obtained via\npatient's son; ..."` flags `'Hx obtained via'`; `"Hx\nper EMS; neck pain."` flags `'Hx'` (`T-132-wrap-probe.py`; parent identical). Cause: `lexicon_scan.py:133` returns the unit unchanged when `m.end() > unit[1]` (the attribution regex spans the newline, past the unit's end). This is the T-120 r3 paralegal blocker (the condition is in no flag) for text copied from a fixed-width source, a shape the card does not name, so I rate it major and not blocker; that is a scope judgement, not a defect-class judgement. Mutant M10 (drop the guard) survives all 122 tests and changes the output to `'Hx\nper EMS;'`, still without the condition.
2. **minor: chained attribution clauses give overlapping flags, the first without a condition.** `"Hx per EMS; Hx per son; neck pain."` -> two flags, `'Hx per EMS; Hx per son;'` and `'Hx per son; neck pain.'` (A19, `OVERLAP`). `"Hx per EMS; who interpreted; prior neck injury."` -> `'Hx per EMS; who interpreted;'` plus `'prior neck injury.'` (A35). The "one clause only" rule is met, but the first flag shows no condition and the overlap is the duplicate the card says it removes.
3. **minor: the extension crosses a section break and bundles unrelated text into a prior-condition quote.** `"Hx per EMS\n\nPLAN: follow up in 2 weeks."` -> one flag, quote includes the blank line and `PLAN:` (A25); `"Hx per interpreter\nMEDICATIONS: ibuprofen 400 mg"` (A7); `"Hx per EMS; patient states symptoms began after the collision."` (A26, the causation sentence is quoted inside a prior-condition flag). The parent flagged the same attribution (an over-flag in the safe direction) with a short quote; now the quote is longer and names nothing prior. By the code's own rule a newline does not end the sentence (`_SENT_END`, lexicon_scan.py:28), and test row 6 pins that; the cost is this bundling.
4. **minor: three mutants survive the new tests.** M8 (extend for any pre_existing hit, dropping the history-word guard): `"Chronic per EMS; headaches."` becomes `'Chronic per EMS; headaches.'` (HEAD `'Chronic per EMS;'`). M9 (`a > unit[1]`): `"Hx per EMS;neck pain."` loses the condition (`'Hx per EMS;'`). M10 as in finding 1. Result: 11 of 14 killed. Add rows for these three inputs to `tests/unit/test_t132_attribution_unit.py`.

Not findings (stated so they are not re-raised): the denial over-flag (S16) and bare `History` without a lexicon entry were left open by T-120 and are unchanged; `Hx obtained from Dr. Lee; no complaints.` flags, as the parent did.

## Paralegal-view check

Setup: `git archive f4d68bb` copy (`app_arch`), library case `case_lib09_spanish_interpreter_espalda.txt` edited in the scratch copy only, record 1 now `Hx obtained via patient's son; neck pain and headaches. Patient states ...`. Server: `.venv/bin/python -m app.main` from that copy, `ZLAYT_MODE=local`, `ZLAYT_DB` in the scratchpad, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, `HOST=127.0.0.1 PORT=7947`. `lsof -p 96204 -a -d cwd` showed the copy.

- Pasting the text through `POST /api/cases {"text": ...}` returns 409 `demo_mode_unsupported_input` (fixture mode only runs recorded and library cases), the same as the T-120 r3 run. So I loaded the edited library case by id (`{"library": ...}`), then `POST /run`; status reached `ready`.
- `GET /api/cases/{token}`: one pre_existing flag, `f_r1_1`, origin `lexicon`, state `needs_review` (reason FIXTURE_MISS: no recorded AI answer, so nothing is claimed as checked). Title "Mention of a prior or pre-existing condition". The explanation the reviewer reads (the UI prints `f.explanation`, app/frontend/flags.js:71): `Quillmere Regional ED (March 3, 2026) mentions a prior or pre-existing condition: “Hx obtained via patient's son; neck pain and headaches.”`. Evidence excerpt is the same string, start 134, end 189; `raw_text[134:189]` equals it (checked against the library file).
- Result: the flag shown to the reviewer includes the condition ("neck pain and headaches"), and there is one flag, not two. In the T-120 r3 build the same input showed only `Hx obtained via patient's son;`.
- Stopped the server by PID: `kill 96204`; `lsof -iTCP:7947 -sTCP:LISTEN` printed nothing (exit 1); curl returned 000; `ps -p 96204` empty. PID 88327 (not mine) and the 7860 app (PID 23532) were left running.
- Not exercised: a browser render of the card (the explanation text and evidence come from the API response the page prints); the live LLM merge path, where a model flag that overlaps the lexicon span replaces the quote with the model's span (flags.py:merge, D-030).

```json
{"card": "T-132", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive f4d68bb (code unchanged to HEAD 2790918 in lexicon_scan.py and sentences.py); parent f4d68bb^ as control; app/backend/lexicon_scan.py:17-24,127-136,170-186; tests/unit/test_t132_attribution_unit.py; app on 127.0.0.1:7947 (fixture backend, ZLAYT_MODE=local, PID 96204, stopped); lib09 record 1 edited in a scratch copy",
 "exercised": [
  "python3 tools/board.py show T-132; read reviews/T-120-paralegal-r3.md and reviews/T-120-staff-engineer-r3.md; git show f4d68bb -- app/backend/lexicon_scan.py; read the new test file and flags.py lexicon_flags/merge",
  "pytest tests/unit -q on the archive: 3213 passed, 4 skipped in 187.70s; t132 + t120 test files: 122 passed",
  "artifacts/review-evidence/T-132-probe.py: 37 sentences via flags.lexicon_flags on f4d68bb and parent (outputs T-132-probe-HEAD-f4d68bb.txt, T-132-probe-parent.txt); all quotes contiguous substrings of the record",
  "artifacts/review-evidence/T-132-wrap-probe.py: 5 hard-wrapped variants on f4d68bb and parent; plus a 5-row edge probe (no-space, Hx newline per, blank line)",
  "artifacts/review-evidence/T-132-mutants.py: 14 mutants of lexicon_scan.py, 11 killed, 3 survived (M8, M9, M10), the survivors re-run by hand in separate copies",
  "python -m app.pipeline evals/golden/sample.txt twice (fixture): exit 0, cmp identical",
  "python -m evals.run --backend fixture on f4d68bb and parent: latest.json 508 leaves, 0 differences outside timestamps; ship_bar_met=False on both (fixture backend)",
  "app from the archive copy on 127.0.0.1:7947 (ZLAYT_MODE=local, fixture, ZLAYT_DB in scratchpad): paste POST returned 409; library case with the Hx semicolon sentence reached ready; read the pre_existing flag explanation and evidence; checked evidence offsets against the library file",
  "kill 96204; lsof -iTCP:7947 -sTCP:LISTEN printed nothing; curl 000; the foreign listener on 7931 (PID 88327) and the 7860 app were not touched",
  "grep of the diff for except, float(, sleep(, retry, network: none"],
 "verdict": "changes",
 "scores": {"correctness": 4, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "Hard-wrapped attribution phrase: the quote is a fragment and the condition is in no flag (guard m.end() > unit[1])",
   "evidence": "app/backend/lexicon_scan.py:133 `if not m or m.end() > unit[1] or ...: return unit`. Probe on f4d68bb (artifacts/review-evidence/T-132-wrap-probe.py): \"Hx obtained\\nvia patient's son; neck pain and headaches.\" -> ['Hx obtained']; \"Hx obtained via\\npatient's son; neck pain and headaches.\" -> ['Hx obtained via']; \"Hx obtained via patient's\\nson; neck pain and headaches.\" -> [\"Hx obtained via patient's\"]; \"Hx\\nper EMS; neck pain.\" -> ['Hx']. The parent gives the same output. Mutant M10 (delete `m.end() > unit[1] or`) survives 122 tests and gives 'Hx\\nper EMS;' for the last input.",
   "why_it_matters": "This is the T-120 r3 paralegal blocker (the condition after the semicolon is in no flag excerpt) for text with a line break inside the attribution phrase, which is what pasted fixed-width or PDF text looks like. ingest.py does not unwrap lines (it only normalises CRLF, ingest.py:33). The card names the ';' and newline ends, not a wrapped phrase, so I rate major, not blocker; that is a scope call, not a view that the loss is harmless.",
   "fix": "Decide the extension on the unit that holds the END of the attribution phrase: when m.end() lies past the unit end, merge the units up to m.end() first, then apply the same only-punctuation test and the one-clause extension. Or state in the card that a wrapped phrase is out of scope and record it in SCOPE_CUTS.",
   "acceptance_test": "Rows in tests/unit/test_t132_attribution_unit.py: \"Hx obtained\\nvia patient's son; neck pain and headaches.\" and \"Hx\\nper EMS; neck pain.\" give one pre_existing flag whose quote contains 'neck pain'; mutant M10 is then killed."},
  {"severity": "minor",
   "title": "Chained attribution clauses give overlapping flags and the first shows no condition",
   "evidence": "artifacts/review-evidence/T-132-probe-HEAD-f4d68bb.txt A19: \"Hx per EMS; Hx per son; neck pain.\" -> ['Hx per EMS; Hx per son;', 'Hx per son; neck pain.'] with OVERLAP. A35: \"Hx per EMS; who interpreted; prior neck injury.\" -> ['Hx per EMS; who interpreted;', 'prior neck injury.'] (first flag has no condition). The join loop at lexicon_scan.py:180-185 only merges hits whose unit lies inside another extended unit; a second extended unit is not contained.",
   "why_it_matters": "The card removes the duplicate fragment flag; here a paralegal sees two flags over the same words, one with no condition. Same class as the original defect, in a rarer shape (two attribution clauses in a row).",
   "fix": "Either let the extension skip following attribution-only clauses until it reaches one clause with content (still within the sentence), or fold the overlapping extended units into one flag.",
   "acceptance_test": "A19 and A35 give no flag whose quote lacks the condition and no two pre_existing flags with overlapping spans."},
  {"severity": "minor",
   "title": "The extended quote crosses a blank line or section header and bundles unrelated text into a prior-condition quote",
   "evidence": "T-132-probe-HEAD-f4d68bb.txt A25: \"Hx per EMS\\n\\nPLAN: follow up in 2 weeks.\" -> ['Hx per EMS\\n\\nPLAN: follow up in 2 weeks.']; A7: \"Hx per interpreter\\nMEDICATIONS: ibuprofen 400 mg\" -> quote includes the MEDICATIONS line; A26: \"Hx per EMS; patient states symptoms began after the collision.\" -> quote includes the causation sentence (which also has its own causation flag). Parent quotes: 'Hx per EMS', 'Hx per interpreter', 'Hx per EMS;'. Cause: _SENT_END (lexicon_scan.py:28) does not end a sentence at a newline, and T-132 row 6 pins that.",
   "why_it_matters": "The flag still says a prior condition is mentioned while the quote names none, and the paralegal now reads a longer, unrelated quote. The flag itself was already an over-flag on the parent; the extension makes it more misleading. Safe direction (no fact lost), so minor.",
   "fix": "Stop the extension at a blank line (two newlines) or at a header-like line (UPPERCASE word + colon), or extend only when the next clause is not a different flag type's own quote.",
   "acceptance_test": "A25 and A7 keep the short quote; row 6 (`Hx per interpreter\\nLumbar strain 2019`) still extends."},
  {"severity": "minor",
   "title": "Three mutants survive the new tests: M8 (history-word guard on the extension), M9 (a > unit[1], no-space next clause), M10",
   "evidence": "artifacts/review-evidence/T-132-mutants.py output: `SURVIVED M8 extend for any pre_existing hit (drop history-word) | 122 passed`, `SURVIVED M9 a > unit[1] (no-space next unit) | 122 passed`, `SURVIVED M10 drop m.end()>unit[1] guard | 122 passed`; 11 of 14 killed. Behaviour: M8 makes \"Chronic per EMS; headaches.\" quote 'Chronic per EMS; headaches.' (HEAD 'Chronic per EMS;'); M9 makes \"Hx per EMS;neck pain.\" quote 'Hx per EMS;' (HEAD 'Hx per EMS;neck pain.').",
   "why_it_matters": "Each is a one-token edit that changes the quote shown to the reviewer and no test notices; same class as T-120 r3 mutant F.",
   "fix": "Add rows: \"Chronic per EMS; headaches.\" expects 'Chronic per EMS;'; \"Hx per EMS;neck pain.\" expects the whole text; the wrapped rows from finding 1 for M10.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-132-mutants.py: 14 of 14 killed."}
 ],
 "whats_right": [
  "The T-120 r3 blocker forms S6, S8 and N2 now give one flag with the condition in the quote and both lexicon ids; the quote is a verbatim contiguous slice and the API offsets (134:189) match the library file.",
  "The extension is gated tightly: it never crosses a period, never fires for a non-history word or a unit that already names the condition, and a different flag type does not join (A10-A12, A21-A23, A27, test_only_hits_of_the_same_flag_type_join_the_extended_quote).",
  "The MS fix is precise: `Hx per MS history.` and `Hx per patient, MS diagnosis.` flag while Dr Lee, Ms. Alvarez and Mr Smith stay a source; eval metrics are identical to the parent (508 leaves, 0 differences)."],
 "questions_for_chris": []}
```
