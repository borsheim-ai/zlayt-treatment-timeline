# T-128 staff-engineer review, round 4 (scoped fix-up), commit eef92a7

Verdict: pass. One nit, no blockers, no majors. The fix-up does what the orchestrator scoped: `' with '` no longer splits a clause, `Neck pain consistent with sprain.` stays one clause, the "never a fragment by construction" claim is gone from the `summary_trim.py` docstring and from `memory/contracts/api.md`, and a single unsupported clause goes to the could-not-verify tray (`text == ''`, the clause named in `removed`). I checked only that, as asked.

Scope: `git archive HEAD` (HEAD = eef92a7; `git diff --quiet HEAD -- app/backend/summary_trim.py tests/unit/test_summary_trim.py` was clean). Control: `git archive eef92a7^` (the round-3 code). Archives are `T132r3_arc`, `T132r3_mut`, `T128r4_prev` in my scratchpad. Python is `.venv/bin/python -I`. Scripts and outputs: `artifacts/review-evidence/T-132-128-r3/` (`T-128-r4-*`).

## What I exercised

- `python3 tools/board.py show T-128`; `git show eef92a7 -- app/backend/summary_trim.py memory/contracts/api.md` in full; the test diff.
- `pytest tests/unit -q` on the HEAD archive: `3359 passed, 4 skipped in 184.92s`; `test_summary_trim.py` alone is part of the 397 passed with the t132 file (`test_summary_trim.py`: 318 tests, as the handoff says).
- My round-3 probe tables re-run on HEAD: `T-128-r3-with.py` (`T-128-r4-with-out.txt`, 19 pairs) and `T-128-r3-with2.py` (`T-128-r4-with2-out.txt`, 14 pairs), plus `T-128-r3-edge.py` (`T-128-r4-edge-out.txt`, 18 pairs). All the reviewer's `' with '` tails (`consistent with sprain`, `treated with injection`, `managed with ibuprofen`, `immobilized with a splint`, `relieved with ibuprofen`, ...) now give `text == ''` with the whole clause in `removed`, never `'Neck pain consistent.'`. The old script `T-128-r3-probe.py` needs a second argument and exited 1 (`T-128-r4-probe-out.txt`, IndexError); I replaced it by the fuzz below.
- `T-128-r4-fuzz.py`: 20,000 random summaries built from `' with '`, `' and '`, `,`, `;`, `.`, `' due to '`, `' followed by '` joins, with three oracles: (A) a changed result is a prefix of whole clauses of the summary, (B) the kept text is never followed, in the original, by `' with '`, (C) `split_clauses` never makes a clause that starts with `with`. HEAD: 0 / 0 / 0. Control (`eef92a7^`): B violated 1,888 times, for example `'Neck pain with surgery recommended.'` -> `'Neck pain.'` and `'Headaches and Seen at ER with Back pain.'` -> `'Headaches and Seen at ER.'` (`T-128-r4-fuzz-prev.txt`). The oracle fails on the old code and passes on the new.
- `T-128-r4-mutants.py`: 11 mutants of `summary_trim.py` (the 12th, a comma-split edit, did not match its pattern and was not run) against `tests/unit/test_summary_trim.py`; `T-128-r4-mutants-out.txt`: 10 killed. `' with '` splitting again (Q01), `' and '` not splitting (Q02), suffix rule off (Q03), prefix threshold 1 or 3 (Q05, Q06), tray rule off (Q07), notes dropped (Q08), tray `any` -> `all` (Q09), final period dropped (Q11), `changed` forced False (Q12) are all killed. Q04 (the explicit first-clause return) survives; it is redundant with the suffix rule plus the empty-result rule, which I already noted in round 3 as a nit.
- `grep -rniE 'by construction|never (leav|a fragment)|fragment'` over `app`, `docs`, `memory`, `tests/unit/test_summary_trim.py`, `submission`, `spec` in the archive, for the stale-claim check.
- Not exercised: the pipeline end to end for trimmed summaries and the live judge path (outside the scoped check); no server started.

## The four scoped checks

| Check | Result |
|---|---|
| `' with '` no longer splits | `_SPLIT = re.compile(r";\|,(?!\d)\|(?<!\d),\|\s+and\s+\|\.(?=\s\|$)", re.IGNORECASE)` at `app/backend/summary_trim.py:82`; mutant Q01 (put `with` back) fails 1 test; fuzz oracle C: 0 violations; `T.split_clauses("Wrist pain with numbness; neck pain consistent with sprain.")` has 2 clauses (`tests/unit/test_summary_trim.py:388`). |
| `Neck pain consistent with sprain.` stays whole | `T-128-r4-with2-out.txt`: `'Neck pain consistent with sprain.' | 'Neck pain.' -> '' ['Neck pain consistent with sprain']`: one clause, removed whole. Pinned at `tests/unit/test_summary_trim.py:402` (MIDDLE/with list). Oracle B on 20,000 random summaries: 0 violations. |
| The by-construction claim is gone | The docstring rule 3 now says it does NOT guarantee the kept text reads as a finished sentence and lists only three guarantees (suffix only, first clause kept, 2 content words); `memory/contracts/api.md:742` says "Code does not promise that the kept text reads as a finished sentence". Neither file contains "by construction" or "never a fragment" any more (grep). Leftovers outside the two files: finding 1. |
| A single unsupported clause goes to the tray | `T.trim("Laceration repaired with sutures.", "Sutures placed in the clinic.")` -> `text == ""`, `removed == ["Laceration repaired with sutures"]` (`tests/unit/test_summary_trim.py:385-386`); `'Neck pain consistent with sprain.'` over `'Neck pain.'` gives `''` (above). The cost is that a summary whose only clause carries one unsupported word goes to the tray instead of judge 1 whole (the handoff says so); it is the safe direction (nothing unsupported is shown) and Q07 shows the tray is pinned. |

## Findings

One nit: stale overclaims in a test header, a test name and an ADR line.

```json
{"card": "T-128", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD (eef92a7; app/backend/summary_trim.py and tests/unit/test_summary_trim.py identical to the working tree); control git archive eef92a7^; scoped fix-up check only: ' with ' split, 'Neck pain consistent with sprain.', removal of the by-construction claim in the docstring and memory/contracts/api.md, single unsupported clause to the tray; fixture backend, no network, no server",
 "exercised": [
  "python3 tools/board.py show T-128; git show eef92a7 -- app/backend/summary_trim.py memory/contracts/api.md; the test diff",
  "pytest tests/unit -q on the HEAD archive: 3359 passed, 4 skipped in 184.92s; test_summary_trim.py (318 tests) and the t132 test file together: 397 passed",
  "artifacts/review-evidence/T-132-128-r3/T-128-r4-with-out.txt (19 pairs), T-128-r4-with2-out.txt (14 pairs), T-128-r4-edge-out.txt (18 pairs): the round-3 probe tables re-run on HEAD; every ' with ' tail gives '' (tray) with the whole clause in removed",
  "T-128-r4-fuzz.py: 20000 random summaries, oracles A (prefix of whole clauses), B (kept text not followed by ' with '), C (no clause starts with 'with'): HEAD 0/0/0, control eef92a7^ B=1888",
  "T-128-r4-mutants.py: 11 mutants of summary_trim.py against test_summary_trim.py, 10 killed, 1 survived (Q04, explicit first-clause return, redundant); a 12th mutant did not match and was not run",
  "grep for 'by construction', 'never a fragment', 'fragment' over app, docs, memory, tests/unit/test_summary_trim.py, submission, spec in the HEAD archive",
  "T-128-r3-probe.py needs a second argument and exited 1 (IndexError); not used"],
 "verdict": "pass",
 "scores": {"correctness": 5, "determinism": 5, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [
  {"severity": "nit",
   "title": "Stale overclaims remain in a test header, a test name and an ADR line (outside the two files the fix-up scoped)",
   "evidence": "tests/unit/test_summary_trim.py:590 header '# ---- T-128 round 2 ...: fragments are impossible by construction, not by a word list' with rule (3) at :593 still describing the round-2 ' with ' / ',' / ' and ' behaviour; tests/unit/test_summary_trim.py:162 `def test_a_trim_never_leaves_a_fragment` asserts over a fixed UNSUPPORTED list only; memory/DECISIONS.md:367 'A structural no-fragment rule applies (T-128 r3, ...)'; app/backend/summary_trim.py:393 comment \"(D-054 'never leave a fragment')\". Checked with grep -rniE 'by construction|never (leav|a fragment)|fragment' on the HEAD archive.",
   "why_it_matters": "The orchestrator asked that the by-construction claim be removed unless a test proves it over the fuzz set. The docstring and api.md are clean, but the test file still says fragments are impossible by construction and a test is named 'never leaves a fragment'; the next reader takes the header as a guarantee. memory/DECISIONS.md is architect-owned.",
   "fix": "Backend: reword the header at tests/unit/test_summary_trim.py:590-593 to the three guarantees and rename test_a_trim_never_leaves_a_fragment to something like test_a_with_phrase_is_removed_whole_or_kept_whole. Architect (separate card): change 'no-fragment rule' at memory/DECISIONS.md:367 to 'suffix-only rule'.",
   "acceptance_test": "grep -rniE 'by construction|never leaves a fragment|no-fragment' app/backend/summary_trim.py memory/contracts/api.md memory/DECISIONS.md tests/unit/test_summary_trim.py prints nothing."}
 ],
 "whats_right": [
  "Removing the ' with ' split deletes the participle-merge code (_PARTICIPLE, _single_word, _joined_by_with) instead of patching it: 20,000 random summaries show 0 oracle-B violations against 1,888 on the previous commit.",
  "The docstring and api.md now state only what the code guarantees (whole clauses, suffix only, first clause kept, 2 content words) and say outright that the kept text may not read as a finished sentence.",
  "The new tests pin the right shapes: the 9 ' with ' tails go to the tray, 'diagnosed with diabetes' is removed whole, and mutant Q01 (' with ' splitting again) fails."],
 "questions_for_chris": []}
```
