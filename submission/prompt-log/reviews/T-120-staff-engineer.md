# T-120 staff-engineer review (commit 1cb8707, archive of c26ff04)

Verdict: changes. The guard works for the cases it lists, but the `per`/`via` branch is unconditional and silently drops a flag on a real prior-condition mention.

Exercised (all on a `git archive` copy of c26ff04, run with the project venv):
- `pytest tests/unit -q`: 2816 passed, 4 skipped.
- `python -m evals.run` on the fixture backend: runs; `--check-spec` gives spec_matches_golden true. The fixture run reports ship_bar_met=False on the usual live-only items.
- `python -m app.pipeline evals/golden/sample.txt` twice: byte-identical output.
- Probe script calling `lexicon_scan.scan` on 10 phrasings (below).
- Mutants against tests/unit/test_t120_history_source_sentence.py: removing the guard is killed, and widening it to every Hx hit is killed. My third mutant (adding `|:`) was inert, because the `\s+` prefix blocks it. It proves nothing and is not counted.
- Read the diff in full. There is no LLM call, no float, no network and no clock. The guard is code only, in lexicon_scan.

```json
{"card": "T-120", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04 (T-120 commit 1cb8707): app/backend/lexicon_scan.py, tests/unit/test_t120_history_source_sentence.py; no app URL; sample case plus lib09",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "python -m evals.run (fixture) and --check-spec: spec_matches_golden true", "python -m app.pipeline evals/golden/sample.txt twice: identical", "probe of lexicon_scan.scan on 10 Hx/History phrasings", "mutants: drop guard (killed), guard hits every Hx (killed)", "read git show 1cb8707 in full"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 5, "llm_code_boundary": 5, "test_quality": 3},
 "findings": [
  {"severity": "major",
   "title": "The `Hx per ...` branch drops the flag on real prior-condition mentions",
   "evidence": "app/backend/lexicon_scan.py:15 `(?:per|via)\\s` is unconditional, and :136 skips the hit. Probe with `.venv/bin/python -I` on the archive: scan('Hx per patient: lumbar strain 2019.') -> [] ; scan('Hx per patient of lumbar strain') -> [] ; scan('PMH per patient: diabetes since 2015.') -> []. 'Hx per patient: ...' is ordinary note phrasing. tests/unit/test_t120_history_source_sentence.py REAL list has no 'per' case, so the suite is green.",
   "why_it_matters": "The skip is meant for sentences that name who gave the history. 'Hx per patient: lumbar strain 2019' names the source and a prior condition together, and the whole condition mention disappears. That is a lost recall flag with no trace, on a defense-relevant item (R-FL pre_existing).",
   "fix": "Narrow the `per`/`via` branch so it skips only when the source phrase ends the clause or is followed by an interpreter/family-member noun and no condition text (or only skip the `Hx` token and let the remaining clause scan run). Do not skip when a colon, 'of', a year or a condition word follows the source.",
   "acceptance_test": "Add to REAL: 'Hx per patient: lumbar strain 2019.', 'Hx per patient of lumbar strain', 'History per patient: left knee surgery in 2017.' and assert a pre_existing hit; keep every SOURCE case green. Mutant widening `(?:per|via)\\s` to any following text must fail."}
 ],
 "whats_right": ["Guard is deterministic code in lexicon_scan; lexicon.yaml untouched; evals fixture flag P/R unchanged.", "The sentence-adjacent test proves a real prior mention next to a source sentence still hits.", "Removing or broadening the guard fails the new tests."],
 "questions_for_chris": []}
```
