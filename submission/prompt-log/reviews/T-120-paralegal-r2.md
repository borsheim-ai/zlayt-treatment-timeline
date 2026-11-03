# T-120 paralegal re-check (round 2)

**Verdict: fail.** One blocker, the same class as round 1. The colon forms from the r1 blocker now raise the prior flag again. But the skip still hides a prior condition in a history-source sentence whenever the sentence has no colon, no digit and no "of", for example "Hx obtained via patient's son, who reports neck pain." The pre-T-120 build flags that sentence. HEAD does not.

Scope: HEAD 433ac1c (contains 07dbd2b, the T-120 r2 commit) as a `git archive` copy in the session scratchpad, fixture backend, ZLAYT_MODE=local, port 7895, listener PID 17734 (stopped; port closed, curl returns 000). Baselines are also archive copies: 0c47356 (pre-T-120, the parent of 1cb8707) and 07dbd2b (r2). The paste route is refused on HEAD with 409 demo_mode_unsupported_input (demo_mode is true even with ZLAYT_MODE=local), so my own sentences went through the same engine the pipeline calls (flags.lexicon_flags, flags.py:80, which the pipeline calls at flags.py:249). Each sentence was put in lib09 record 1 with its excerpt replaced. The card's "record 2" is record 1.

## Re-test of the r1 blocker and the interpreter-only sentence

Full table: artifacts/review-evidence/T-120-r2-compare.txt. Labels S1 to S16 match the probe script.

| # | Probe sentence | Pre-T-120 | HEAD 433ac1c | Expected | OK |
|---|---|---|---|---|---|
| S1 | PHx obtained via patient's son: lumbar strain 2019. (r1 blocker) | flag | flag | flag | yes |
| S2 | Hx obtained via patient's son, who interpreted. (interpreter-only) | flag | none | none | yes |
| S3 | Hx obtained via interpreter: lumbar strain 2019. | flag | flag | flag | yes |
| S4 | Hx obtained via patient's son, who reports neck pain. | flag | none | flag | NO |
| S5 | Hx obtained via patient's son, who reports chronic neck pain. | flag | flag | flag | yes |
| S6 | Hx obtained via patient's son; neck pain and headaches. | flag | none | flag | NO |
| S7 | Hx per patient's son, who interpreted. | flag | none | none | yes |
| S8 | Hx via interpreter, who interpreted; prior neck injury. | flag | flag | flag | yes |
| S9 | Hx of lumbar strain obtained via patient's son. | flag | flag | flag | yes |
| S10 | Hx obtained via patient's son, who interpreted, lumbar strain 2019. | flag | flag | flag | yes |
| S11 | Hx obtained via EMS crew, who relayed lumbar strain. | flag | none | flag | NO |
| S12 | Hx obtained via patient's son, who interpreted. Lumbar strain was noted. | flag | none | none | yes |
| S13 | Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019. | flag | flag | flag | yes |
| S14 | Hx: lumbar strain 2019. (control, no source phrase) | flag | flag | flag | yes |
| S15 | Hx obtained via patient's son, who interpreted, and reports lumbar strain. | flag | none | flag | NO |
| S16 | Hx obtained via patient's son, who interpreted, denies neck pain. | flag | none | none | yes |

Live app (HEAD, library route, the only route that takes this sentence): case_lib09_spanish_interpreter_espalda is ready with no pre_existing flags, so the interpreter-only sentence in record 1 stays unflagged. Sample record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("Findings may represent degenerative change") still flag. lib02 and lib11 still flag their prior mentions. Evidence: artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json.

## Findings

### 1. blocker: the source-sentence skip still drops a prior condition that has no colon, digit or "of"

- Four of the 16 probes (S4, S6, S11, S15) raise a pre_existing flag before T-120 and raise none on HEAD. The raw lexicon hit on the pre-T-120 build is `hx_abbrev`; on HEAD the lexicon finds nothing at all for the same sentences (`lexicon_hit_ids` is empty).
- Cause: `app/backend/lexicon_scan.py:107-115` (`_is_source_sentence`) returns False only when the rest of the sentence contains a colon, a digit or the word "of" (line 115: `return not re.search(r":|\d|\bof\b", rest, re.I)`). Line 152 then drops the `hx_abbrev` hit for every other source sentence.
- The unit tests do not cover this shape. Every REAL row that must still flag carries a colon, a digit or "of" (`tests/unit/test_t120_history_source_sentence.py:14-17`). `pytest tests/unit/test_t120_history_source_sentence.py` on the HEAD archive: 28 passed.

Why it matters: checklist item 9 and card AC 1 require a real prior-condition mention to raise the flag. The r2 commit message says the skip applies only "when the sentence names no condition", but the check tests punctuation and one word, not the condition. A history line such as "who reports neck pain" gets no prior flag, and the adjuster reads that same line in the record. This is the r1 blocker for a different shape. The rule removes a guess (the source phrase is not a prior) and deletes the condition next to it. I am not downgrading it because the shape is less common than the colon form.

Suggested direction (the fix owner decides the exact rule): skip only when the words after the source phrase are the attribution and nothing else, from a closed list such as "who interpreted", "who translated" or "who relayed", followed by the end of the clause. Any other word after the source phrase keeps the hit. The colon, digit and "of" cases already pass and should stay as they are.

Acceptance test: add S4, S6, S11 and S15 (verbatim, as in the table) to REAL and assert `flags.lexicon_flags` returns a pre_existing flag for each. Keep S2 and S7 in SOURCE (no flag). Re-run `artifacts/review-evidence/T-120-r2-paralegal-probe.py engine` on the fixed archive and `T-120-r2-paralegal-compare.py`: every row must match its Expected column. Re-run `http` mode: lib09 record 1 pre_existing stays empty, and sample r3 and r8 still flag.

### 2. minor: card AC 1 still cites "record 2" and a test name that no longer exists (carried from r1)

- `python3 tools/board.py show T-120` prints AC 1 as "the interpreter-history sentence of record 2", and its evidence as "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes".
- HEAD has `def test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do` at `tests/unit/test_t120_history_source_sentence.py:44`. The sentence is in lib09 record 1 (`lib09_record_numbers_with_source_sentence = [1]`).
- Why it matters: checklist item 3. A paralegal who opens record 2 will not find the sentence. The r2 handoff says the AC text "cannot be edited by hand", so the correction goes through the board, not a hand edit.
- Acceptance test: `board.py show T-120` shows "record 1" in AC 1, and its evidence names `test_lib09_record_1_...`.

## Not re-tested this round

- The r1 nit on positional flag ids (`f_r1_1` changed meaning). I did not check whether decisions carry over, so I make no claim either way.
- The live LLM merge path (flags.py:249). Fixture mode cannot run unseen text, and the paste route is refused at HEAD. The probe covers the lexicon path only.

## What I exercised

- Read `personas/paralegal.md` in full, `reviews/T-120-paralegal.md`, `python3 tools/board.py show T-120`, and my memory notes on T-120/T-123 and reviewer tooling.
- `git rev-parse HEAD` gave 433ac1c. Extracted `git archive --prefix=zlayt-head/ HEAD`, plus 07dbd2b and 0c47356, into the session scratchpad with `git archive ... | tar -x`.
- Started the app from the HEAD archive with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, PORT=7895. Listener PID 17734 (`python -m app.main`). Log: artifacts/review-evidence/T-120-r2-paralegal-server.log.
- HTTP (`T-120-r2-paralegal-probe.py http`): `/api/health`; paste POST with a history sentence (409 demo_mode_unsupported_input); library cases lib09, lib02, lib11 and the sample, each run to ready and read back through GET.
- Engine (`T-120-r2-paralegal-probe.py engine`, `-I`) on HEAD, 07dbd2b and 0c47356: 16 sentences through `flags.lexicon_flags` and `lexicon_scan.scan`. Compare output: artifacts/review-evidence/T-120-r2-compare.txt.
- `pytest tests/unit/test_t120_history_source_sentence.py` on the HEAD archive: 28 passed.
- Stopped the server: `kill 17734`, then `lsof` on 7895 returned nothing, `curl` returned 000, and `ps` showed no PID 17734.

```json
{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 433ac1c (includes 07dbd2b, T-120 r2) as a git archive copy in the session scratchpad; app on http://127.0.0.1:7895 (fixture backend, ZLAYT_MODE=local, listener PID 17734, stopped); paste route refused 409 (demo_mode true); engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan on lib09 record 1 with the excerpt replaced; baselines 0c47356 (pre-T-120) and 07dbd2b (r2) as git archive copies; library cases lib09, lib02, lib11 and sample evals/golden/sample.txt",
 "exercised": [
  "read personas/paralegal.md, reviews/T-120-paralegal.md, board show T-120, memory notes t120-123-patterns and reviewer tooling",
  "git archive --prefix=zlayt-head/ HEAD | tar -x (433ac1c), plus zlayt-r2 (07dbd2b) and zlayt-base (0c47356) in the session scratchpad",
  "started python -m app.main from the HEAD archive on PORT=7895 with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture; log artifacts/review-evidence/T-120-r2-paralegal-server.log",
  "HTTP probe artifacts/review-evidence/T-120-r2-paralegal-probe.py http: /api/health (demo_mode true), paste POST returned 409 demo_mode_unsupported_input, library lib09/lib02/lib11 and sample run to ready and read via GET; output artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json",
  "engine probe artifacts/review-evidence/T-120-r2-paralegal-probe.py engine (python -I) on HEAD, 07dbd2b and 0c47356: 16 sentences (S1 to S16) through flags.lexicon_flags and lexicon_scan.scan; outputs artifacts/review-evidence/T-120-r2-engine-*.json",
  "artifacts/review-evidence/T-120-r2-paralegal-compare.py > artifacts/review-evidence/T-120-r2-compare.txt: per-sentence table, all three builds",
  "pytest tests/unit/test_t120_history_source_sentence.py on the HEAD archive: 28 passed",
  "python3 tools/board.py show T-120 (AC 1 wording and evidence string)",
  "grep of lexicon_scan.py (lines 107, 115, 152) and test file (REAL rows 14-17, test_lib09_record_1 at line 44) on the HEAD archive",
  "kill 17734; lsof on 7895 empty; curl returned 000; ps showed no PID 17734"],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "prior_mentions_flagged": 3, "interpreter_sentence_not_flagged": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Source-sentence skip still drops a prior condition named without a colon, digit or 'of' (S4, S6, S11, S15: flagged before T-120, not flagged on HEAD)",
   "evidence": "artifacts/review-evidence/T-120-r2-compare.txt rows S4, S6, S11, S15: pre-T-120 True, HEAD False, expected flag. Pre-T-120 raw hit on each is hx_abbrev (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json). On HEAD lexicon_hit_ids is empty for the same four (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json). Cause: app/backend/lexicon_scan.py:107-115 _is_source_sentence returns False only when the rest of the sentence contains a colon, a digit or the word of (line 115: return not re.search(r':|\\d|\\bof\\b', rest, re.I)); line 152 drops the hx_abbrev hit otherwise. Probe sentences, verbatim: 'Hx obtained via patient's son, who reports neck pain.' ; 'Hx obtained via patient's son; neck pain and headaches.' ; 'Hx obtained via EMS crew, who relayed lumbar strain.' ; 'Hx obtained via patient's son, who interpreted, and reports lumbar strain.' Unit tests miss this shape: REAL rows tests/unit/test_t120_history_source_sentence.py:14-17 all carry a colon, a digit or of; 28 passed on the HEAD archive.",
   "why_it_matters": "Checklist item 9 and card AC 1 require a real prior-condition mention to raise the flag. The r2 commit message says the skip applies only when the sentence names no condition, but the check tests punctuation and one word, not the condition. A history line such as 'who reports neck pain' gets no prior flag, and the adjuster reads the same line in the record. This is the r1 blocker for a different shape: the rule removes a guess (the source phrase is not a prior) and deletes the condition next to it. Not downgraded because the shape is less common than the colon form.",
   "fix": "Skip only when the words after the source phrase are the attribution and nothing else: a closed list such as 'who interpreted', 'who translated', 'who relayed', then the end of the clause. Any other word after the source phrase keeps the hit. Keep the colon, digit and of cases as they are. The fix owner decides the exact rule.",
   "acceptance_test": "Add the four sentences above verbatim to REAL in tests/unit/test_t120_history_source_sentence.py and assert flags.lexicon_flags returns a pre_existing flag for each. Keep 'Hx obtained via patient's son, who interpreted.' and 'Hx per patient's son, who interpreted.' in SOURCE (no flag). Re-run artifacts/review-evidence/T-120-r2-paralegal-probe.py engine on the fixed archive and T-120-r2-paralegal-compare.py: every row must match its expect column. Re-run http mode: lib09 record 1 pre_existing stays empty; sample records 3 and 8 still flag."},
  {"severity": "minor",
   "title": "Card AC 1 still cites lib09 record 2 and a test name that no longer exists (carried from r1; r2 renamed the test to record_1)",
   "evidence": "python3 tools/board.py show T-120 AC 1: 'the interpreter-history sentence of record 2'; evidence 'tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes'. HEAD defines test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do at tests/unit/test_t120_history_source_sentence.py:44. The sentence is in lib09 record 1 (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json: lib09_record_numbers_with_source_sentence = [1]).",
   "why_it_matters": "Checklist item 3: a paralegal who opens record 2 will not find the sentence, and the card's evidence names a test that no longer exists. The r2 handoff says the AC text cannot be edited by hand, so the correction goes through the board.",
   "fix": "Correct AC 1 text and its evidence string to record 1 and test_lib09_record_1_... through the board (orchestrator to choose the route).",
   "acceptance_test": "python3 tools/board.py show T-120 shows 'record 1' in AC 1, and the evidence names test_lib09_record_1_...; the test exists at tests/unit/test_t120_history_source_sentence.py:44."}
 ],
 "whats_right": [
  "The r1 blocker shapes now flag on HEAD: 'PHx obtained via patient's son: lumbar strain 2019.' and 'Hx obtained via interpreter: lumbar strain 2019.' (compare rows S1, S3)",
  "The interpreter-only sentence stays unflagged, in the engine ('Hx obtained via patient's son, who interpreted.', S2) and on the live lib09 case (pre_existing list empty)",
  "Live sample and library priors still flag: sample record 3 'Patient reports low back pain in 2023, resolved.' and record 8 'Findings may represent degenerative change'; lib02 and lib11 keep their prior flags"],
 "questions_for_chris": [
  "Should the history-source skip be a closed list of attribution phrases (my suggested direction), or should the Hx hit be dropped only when the whole sentence is the attribution? Your call on the rule; I only need every condition-naming history line to keep its flag.",
  "The live LLM merge path (flags.py:249) is still untested: fixture mode cannot run unseen text and the paste route returns 409 at HEAD. Can the model raise a prior flag on the Hx sentence in the live backend?"]
}
```
