# T-132 staff-engineer review, round 2 (commit c759213)

Verdict: changes. One major, three minors, no blockers. Round 1's four findings are fixed in the shapes I named: a wrapped attribution phrase now gives one flag with the condition, plain chained clauses give one flag, the extension stops at a sentence end, a blank line and a 3+ letter uppercase header, and mutants M8-M10 are killed. Three gaps remain. First, a wrap inside a chained clause still yields a fragment quote, overlapping flags, or no condition at all. Second, the chain recognition is narrower than the phrase regex. Third, two-letter labels such as `BP:` do not stop the extension, and the brief asks for them.

Scope: `git archive HEAD` (HEAD at start b348221, at the end 5f1a7e2). `git diff --stat b348221 HEAD -- app/backend/lexicon_scan.py app/backend/summary_trim.py tests/unit/test_summary_trim.py tests/unit/test_t132_attribution_unit.py app/llm/lexicon.yaml` printed nothing, so HEAD's code is the code of c759213. Archives are in `rv_T132_T128_r2r3/` (`head`, `c_f4d68bb`, `c_parent`) of my session scratchpad. Python is `.venv/bin/python -I`. Probe scripts and outputs are in `artifacts/review-evidence/T-132-128-r2/`.

## What I exercised

- `python3 tools/board.py show T-132` and `T-128`; reviews/T-132-staff-engineer.md; reviews/T-128-staff-engineer-r2.md; `git show c759213 -- app/backend/lexicon_scan.py` in full; the 59 added test lines.
- `pytest tests/unit -q` on the HEAD archive: `3289 passed, 4 skipped in 181.14s`. The handoff says 3292; the working tree holds other agents' uncommitted tests, which the archive does not have. `test_t132_attribution_unit.py` plus `test_t120_history_source_sentence.py`: 141 passed.
- Probe `T-132-r2-probe.py`: 77 sentences through `flags.lexicon_flags` (37 from round 1, 40 new: wraps in every position, chains of 2 to 6, blank lines, headers, drug names, vitals, `!` and `?` ends, CRLF, NBSP). Probe `T-132-r2-probe2.py`: 26 more (wraps inside a chained clause, title-case headers, 2-letter labels, `TYLENOL #3:`, `IBUPROFEN:`). That is 103 sentences, run on HEAD, on f4d68bb and on the parent (`T-132-r2-probe-HEAD.txt`, `-f4d68bb.txt`, `T-132-r2-probe2-HEAD.txt`, `-f4d68bb.txt`). Every quote is a contiguous substring of its record; for the 26 in probe2, `text[span[0]:span[1]] == quote` as well.
- Mutants `T-132-r2-mutants.py`: 19 mutants of `lexicon_scan.py` against the t132 and t120 test files (`T-132-r2-mutants-out.txt`). The 4 survivors that I could separate were re-run by hand in `T-132-r2-mutant-behaviour.py` (`-out.txt`).
- `python -m app.pipeline evals/golden/sample.txt` twice with `LLM_BACKEND=fixture` on the HEAD archive: exit 0 both, `cmp` identical, 45 lines.
- `python -m evals.run --backend fixture` on HEAD and on a control (HEAD with f4d68bb's `lexicon_scan.py` and 2790918's `summary_trim.py`): flattened `latest.json`, 773 leaves each, 2 differences, both `generated_at` timestamps. Both exit 1 (`ship_bar_met` false: determinism_3run and judge_controls need a live backend), as in round 1. My first attempt used `timeout`, which does not exist on this machine, exit 127; I discarded that run and re-ran.
- Not exercised: a browser or API view (round 1 showed the flag text comes straight from the quote; the code path is unchanged), and the live-LLM merge path in `flags.merge`.
- Stopped PIDs: I killed my own first pytest (PID 17827, cwd my scratch archive, checked with `lsof`) before restarting in a clean directory, because the first directory name collided with another agent's old extract. No server was started.

## Checks asked for

| Check | Result |
|---|---|
| Wrapped attribution never yields a fragment | First-clause wraps: B1-B4, B28, C14 give one flag with the condition (round 1 gave `'Hx obtained'`). **Fails** when the wrap is inside a chained clause (finding 1). |
| Chained attribution gives one flag | A19, A35, B5, B6, B32, B33, C13: one flag, condition inside, no overlap. **Fails** for a wrapped chained clause (finding 1), a chain of 5 or more (B7, B40) and `who interpreted for the patient` (finding 2). |
| Stops at a sentence end | A10-A12, B22-B25, C11: pass. `Hx per EMS; who interpreted. Prior neck injury.` (B22) gives `'Hx per EMS; who interpreted.'` plus `'Prior neck injury.'`: two flags, no overlap. |
| Stops at a blank line | B8, B9, B26, B28-B30, A25, C25 pass (a whitespace-only line counts). |
| Stops at a section header | `PLAN:`, `MEDICATIONS:`, `CHIEF COMPLAINT:`, `NSAID:`, `MRI:`, `X-RAY:`, `DISPOSITION:`, `PMH:`, `L4-5:`, `SEE PLAN:` stop (B10-B14, B39, C16, C19, C20, C23). **Fails** for `BP:`, `HR:`, `RR:`, `PE:`, `Dx:`, title-case `Plan:`, `Medications:` and `TYLENOL #3:` (finding 3). |
| Uppercase drug name plus colon | `Hx per EMS;\nTYLENOL: taken 2019 for back pain.` (B19) and `IBUPROFEN: 400 mg for neck pain` (C18) stop, so the quote is `'Hx per EMS;'`, the parent's quote. A drug name cannot be told from a header without a list, so I count this as the accepted cost of the structural rule, not a finding. |
| Every quote verbatim, contiguous | All 103 rows `verbatim`; span check ok on 26. |
| No LLM, no clock, no float, no except | The diff adds regex and span code only (read in full). |

## Findings

1. **major: a line wrap inside a chained attribution clause still yields a fragment quote, overlapping flags, or no condition.** `"Hx per EMS; Hx obtained\nvia son; neck pain."` gives two overlapping flags, `'Hx per EMS; Hx obtained'` and `'Hx obtained\nvia son; neck pain.'` (C1; C2 and C4 the same). `"Hx per EMS; who\ninterpreted; neck pain."` gives one flag, `'Hx per EMS; who'`, and the condition is in no flag (C3; `neck pain` has no lexicon hit of its own). B31 gives `'Hx per EMS; who'` plus a separate `'prior neck injury.'`. Cause: `_attribution_only(text, nxt)` (lexicon_scan.py:133-141) tests one newline-split unit at a time, so the first piece of a wrapped second phrase (`Hx obtained`) is not attribution-only, the loop at :163-169 stops there, and the wrap fix of step (a) is applied to the first clause only. Both checks I was asked for fail in this shape: a wrapped attribution yields a fragment, and a chain does not give one flag. Round 1's major was the wrap alone; this is the same defect for text copied from a fixed-width source, one chained clause later. Rated major for the same reason as round 1 (a rare input shape, but the criterion says never, and the condition can be lost). None of the 46 tests has a wrapped chain row.
2. **minor: the chain recognition is narrower than the phrase regex, so a long or differently worded chain gives a flag with no condition.** (a) The loop is capped at `range(4)` (lexicon_scan.py:163): `"Hx per EMS; Hx per son; Hx per wife; Hx per aunt; Hx per uncle; neck pain."` gives `'Hx per EMS; Hx per son; Hx per wife; Hx per aunt;'` and `'Hx per uncle;'` (B7); B40 and C12 end the same way. (b) `_WHO_CLAUSE` (line 130) lacks the `for (the) patient|her|him|them` tail that `_WHO_INTERPRETED` accepts, so `"Hx per EMS; who interpreted for the patient; cervical strain; headaches."` gives `['Hx per EMS; who interpreted for the patient;']` (`T-132-r2-mutant-behaviour-out.txt`, section none). The parent gave `'Hx per EMS;'` for these, so nothing is worse than before; the stated aim (the condition is shown) is not met.
3. **minor: the section-header rule needs 3 or more characters, so two-letter labels, title-case labels and `#` labels do not stop the extension.** Pattern: `[A-Z][A-Z0-9 /&-]{2,}:` (lexicon_scan.py:128). `"Hx per EMS;\nBP: 120/80"` gives one flag whose quote is the whole text (B16); `"Hx per EMS; BP: 120/80."` (B15); `"Hx per EMS;\nHR: 88, BP: 120/80"` (B17); `PE: normal.` (C7); `RR: 16, HR: 88` (C9); `Plan: follow up in 2 weeks.` (C5); `Medications: ibuprofen 400 mg` (C6); `Dx: sprain.` (C8); `TYLENOL #3: prn` (C17). The vitals or medication line is then quoted inside a prior-condition flag. The brief names `BP: 120/80` as a tricky case and `BP:` is an uppercase label with a colon; this is round 1 finding 3, fixed for 3+ letter headers only. Safe direction (no fact lost), so minor.
4. **minor: 6 of 19 mutants survive the new tests.** Killed 13. `C6` (`_attribution_only` ignores text after the phrase): `"Hx per EMS; Hx per son: lumbar strain 2019; headaches."` changes from `'...lumbar strain 2019;'` to `'...lumbar strain 2019; headaches.'`. `C7` (same for the who-clause): `"...who interpreted for the patient; cervical strain; headaches."` gains `cervical strain;`. `S6` (blank-line regex `\n\n` instead of `\n[ \t]*\n`): `"Hx per EMS;\n \nneck pain."` goes from `'Hx per EMS;'` to the whole text, although the code comment and the test names promise whitespace-only lines stop it. `S3` (`{2,}` to `{0,}`): `"Hx per EMS;\nA: neck pain."` changes from the whole text to `'Hx per EMS;'`. `S7` (`.match` to `.search`) and `S8` (`nxt[0] + 1` to `nxt[0]`) survive too; I found no input that separates them and do not claim they are real gaps. Fix: add rows for C6, C7, S6, S3 to `tests/unit/test_t132_attribution_unit.py`.

## Questions answered with evidence

- Is the whole round-1 set closed? Findings 1, 2 and 3 of round 1: wrap and chain are fixed in the plain forms (B1-B6, A19, A35); the header and blank-line stops work for 3+ letter headers. Finding 4 (M8, M9, M10): killed (`W1`-`W3` and the new tests).
- Does the change alter eval metrics? No: head and control differ only in timestamps.

```json
{"card": "T-132", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD (code identical to c759213 in lexicon_scan.py, summary_trim.py and both test files; HEAD b348221 at start, 5f1a7e2 at end); app/backend/lexicon_scan.py:127-170; tests/unit/test_t132_attribution_unit.py; round-1 control f4d68bb and f4d68bb^; fixture backend, no network, no server",
 "exercised": [
  "python3 tools/board.py show T-132 and T-128; read reviews/T-132-staff-engineer.md and reviews/T-128-staff-engineer-r2.md; git show c759213 -- app/backend/lexicon_scan.py; read the added tests",
  "pytest tests/unit -q on a clean git archive HEAD: 3289 passed, 4 skipped in 181.14s; t132 + t120 test files: 141 passed",
  "artifacts/review-evidence/T-132-128-r2/T-132-r2-probe.py: 77 sentences (37 from round 1, 40 new) via flags.lexicon_flags on HEAD, f4d68bb and the parent; all quotes contiguous substrings",
  "T-132-r2-probe2.py: 26 more sentences (wrap inside a chained clause, title-case and 2-letter labels, drug names with a colon, TYLENOL #3:, NBSP); span == quote on all",
  "T-132-r2-mutants.py: 19 mutants of lexicon_scan.py against the t132 + t120 tests, 13 killed, 6 survived; T-132-r2-mutant-behaviour.py re-ran C6, C7, S3, S6 by hand",
  "python -m app.pipeline evals/golden/sample.txt twice (fixture): exit 0, cmp identical",
  "python -m evals.run --backend fixture on HEAD and on a control with the round-1 lexicon_scan.py and round-2 summary_trim.py: 773 leaves, 2 differences (timestamps); first attempt with timeout failed with exit 127 and was discarded",
  "git diff --stat b348221 HEAD for the in-scope files and lexicon.yaml: empty",
  "killed my own first pytest PID 17827 (lsof cwd checked) before restarting in a clean directory; no server started"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "A line wrap inside a chained attribution clause still gives a fragment quote, overlapping flags, or no condition (step (b) tests one newline-split unit at a time)",
   "evidence": "artifacts/review-evidence/T-132-128-r2/T-132-r2-probe2-HEAD.txt: C1 \"Hx per EMS; Hx obtained\\nvia son; neck pain.\" -> ['Hx per EMS; Hx obtained', 'Hx obtained\\nvia son; neck pain.'] (overlapping); C2 'Hx per EMS; Hx per\\nson; neck pain.' -> ['Hx per EMS; Hx per', 'Hx per\\nson; neck pain.']; C3 'Hx per EMS; who\\ninterpreted; neck pain.' -> ['Hx per EMS; who'] (condition in no flag); C4 the same with three newlines. T-132-r2-probe-HEAD.txt B31 -> ['Hx per EMS; who', 'prior neck injury.']. app/backend/lexicon_scan.py:133-141 _attribution_only works on one unit; :163-169 the loop breaks on the first unit that is not attribution-only. Re-run: .venv/bin/python -I artifacts/review-evidence/T-132-128-r2/T-132-r2-probe2.py <archive>.",
   "why_it_matters": "The card's criteria are that a wrapped attribution never yields a fragment and that a chain gives one flag. Both fail here, and in C3 the condition after the semicolon is in no flag, which is the T-120 r3 paralegal blocker. Hard-wrapped pasted text is the input that makes the round-1 wrap fix necessary, and a second attribution clause in a row is the input that makes the chain fix necessary.",
   "fix": "In step (b), apply the step (a) merge to the next clause as well: when the clause starts with a history word or 'who', match the full phrase regex from there and extend the clause to the end of the match before testing whether it is attribution-only. Alternatively compute _attribution_only on the text from nxt[0] to the end of the phrase match instead of on one unit.",
   "acceptance_test": "Rows in tests/unit/test_t132_attribution_unit.py for C1-C4 and B31: exactly one pre_existing flag whose quote contains 'neck pain' (or 'prior neck injury'), and no two pre_existing spans overlap."},
  {"severity": "minor",
   "title": "Chain recognition is narrower than the phrase regex: loop cap of 4, and 'who interpreted for the patient' is not attribution-only in a chained clause",
   "evidence": "lexicon_scan.py:163 `for _ in range(4)`; :130 _WHO_CLAUSE lacks the `for (the) patient|her|him|them` tail that _WHO_INTERPRETED has. T-132-r2-probe-HEAD.txt B7 -> ['Hx per EMS; Hx per son; Hx per wife; Hx per aunt;', 'Hx per uncle;']; B40 and T-132-r2-probe2-HEAD.txt C12 end without the condition. T-132-r2-mutant-behaviour-out.txt (section none): 'Hx per EMS; who interpreted for the patient; cervical strain; headaches.' -> ['Hx per EMS; who interpreted for the patient;'].",
   "why_it_matters": "The flag shows who gave the history and not what the condition was; the parent behaved the same, so this is not a regression, but the card's purpose (the quote shows the condition) is not met for these inputs.",
   "fix": "Loop until the sentence end or a content clause instead of a fixed count (the sentence, blank-line and header guards already bound it); share one who-tail pattern between _WHO_CLAUSE and _WHO_INTERPRETED.",
   "acceptance_test": "A 6-clause chain and the 'for the patient' form each give one flag with the condition in its quote."},
  {"severity": "minor",
   "title": "The section-header rule needs 3+ characters; BP:, HR:, RR:, PE:, Dx:, Plan:, Medications: and 'TYLENOL #3:' do not stop the extension",
   "evidence": "lexicon_scan.py:128 `[A-Z][A-Z0-9 /&-]{2,}:`. T-132-r2-probe-HEAD.txt B15 'Hx per EMS; BP: 120/80.' -> one flag with the vitals; B16 'Hx per EMS;\\nBP: 120/80' -> one flag with the whole text; B17 with HR and BP. T-132-r2-probe2-HEAD.txt C5 'Plan: follow up in 2 weeks.', C6 'Medications: ibuprofen 400 mg', C7 'PE: normal.', C8 'Dx: sprain.', C9 'RR: 16, HR: 88', C17 'TYLENOL #3: prn' all bundled into the quote. Mutant S3 ({2,} to {0,}) survives all 141 tests.",
   "why_it_matters": "Round 1 finding 3 (a prior-condition quote that bundles vitals, medications or plan text) is fixed for 3+ letter uppercase headers only. The brief names 'BP: 120/80'.",
   "fix": "Allow 2 uppercase letters (`[A-Z][A-Z0-9 /&#-]{1,}:`) and decide title-case labels explicitly (for example a capitalised word of 4+ letters followed by a colon at a line start), or state the limit in the docstring and tests so it is a decision, not a gap.",
   "acceptance_test": "'Hx per EMS;\\nBP: 120/80' and 'Hx per EMS;\\nPE: normal.' keep the quote 'Hx per EMS;'; 'Hx per EMS;\\nA: neck pain.' is pinned either way."},
  {"severity": "minor",
   "title": "Six of 19 mutants survive the new tests (C6, C7, S3, S6 shown to change output; S7, S8 not separated)",
   "evidence": "artifacts/review-evidence/T-132-128-r2/T-132-r2-mutants-out.txt: `SURVIVED C6 ... 141 passed`, `SURVIVED C7`, `SURVIVED S3`, `SURVIVED S6`, `SURVIVED S7`, `SURVIVED S8`. T-132-r2-mutant-behaviour-out.txt: C6 'Hx per EMS; Hx per son: lumbar strain 2019; headaches.' quote gains ' headaches.'; C7 gains 'cervical strain;'; S6 'Hx per EMS;\\n \\nneck pain.' becomes the whole text; S3 'Hx per EMS;\\nA: neck pain.' becomes 'Hx per EMS;'.",
   "why_it_matters": "One-token edits change the quote the paralegal reads and no test notices; S6 breaks a behaviour the code comment promises (blank line with whitespace).",
   "fix": "Add rows for the four shown inputs to test_t132_attribution_unit.py.",
   "acceptance_test": "Re-run T-132-r2-mutants.py: C6, C7, S3, S6 print KILLED."}
 ],
 "whats_right": [
  "A wrapped phrase in the first clause (B1-B4, B28, C14) now gives one flag with the condition in a contiguous quote, and the plain chained forms (A19, A35, B5, B6, B32, B33) give one flag with no overlap.",
  "The blank-line and 3+ letter header stops are structural (no section-name list) and work across 20 probes, including whitespace-only lines, CRLF and mixed punctuation; evals are identical to the control and the CLI output is byte-stable.",
  "The 8 new mutants plus M8-M10 are killed by named tests (13 of 19 killed in my set), and the extended quote is always a verbatim contiguous slice of its record (103 of 103)."],
 "questions_for_chris": []}
```
