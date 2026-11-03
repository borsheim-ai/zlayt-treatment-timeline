# T-133 review (staff-engineer-reviewer), lexicon deny forms and history_significant_for

Pinned to HEAD 1218b2e (commits e79c3aa feat and 1218b2e calibration). Reviewed from `git archive 1218b2e` extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-133-r1-archive`. The main tree was not edited.

Verdict: **changes** (no blocker; one major). The deny forms are real negation words in the grounding path and the NegEx source checks out for three of the four forms. The new `history_significant_for` entry meets its two required hits and the attribution-only control, but it over-flags HPI-style "History:" narratives, which the brief asked me to check. The attribution-word addition is untested, and flag excerpts can lose the condition.

## Checks against the brief

1. **Deny forms in the grounding list, each with a source.** Pass for three forms, partial for one. `is_negation_word` is True for deny, denies, denied and denying (`app/llm/lexicon.yaml` code_lists negation_word, line 1440; probe output below). The NegEx list (fetched from `chapmanbe/negex` `genConText/negex_triggers.txt`, lines 24-26) has `denied`, `denies` and `denying` tagged `[PREN]`. `deny` is not in that list. The yaml labels it an assumption (lines 50-51), which is honest but does not meet "with a source" (finding 4).
2. **Hits.** Pass. "History provided by wife, notable for lumbar strain." flags with the condition in the quote. "History significant for diabetes." flags.
3. **Attribution-only control.** Pass. "History provided by wife." is quiet.
4. **No over-flag on HPI and similar text (10+ probes).** Fail on the bare-header form. 29 sentences were probed. The 7 `History of present illness` / `History and physical` / `Chief complaint: ... History of present illness` variants are quiet, as are the family, social, interval, work, and "per patient; exam" cases. Five bare "History:" or complaint-style narratives flag as `pre_existing` (finding 1).
5. **Tests.** `tests/unit/test_t133_lexicon.py` 32 passed. The full `tests/unit` suite on the archive gave 3246 passed, 4 skipped (card says 3249 passed; nit). `research/lexicon_selfcheck.py` RESULT: PASS, held-out 115/115.

## Mutation spot-checks (scratch copies, not committed)

| Mutant | Result |
|---|---|
| M1 drop `history_significant_for` entry | 9 failed |
| M2 drop `deny` from negation_word | 3 failed |
| M3 drop `deny` and `denying` from attribution_word | 0 failed in the full unit suite (3246 passed, 4 skipped) |
| M4 drop `denying` from pre_cues | 2 failed |
| M5 drop `deny` from field_answer | 2 failed |
| M6 drop `(?<!family\s)` look-behind | 1 failed |

## Findings

**F1 (major). Bare "History:" HPI narratives and complaint text are flagged pre_existing.** Evidence in the probe output of `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t133_r1_probe.py`. Flagged: "History: 45-year-old male, significant for neck pain.", "History: patient was a passenger, significant for neck pain.", "Chief complaint and history: notable for neck pain.", "History obtained from patient, notable for neck pain since the crash." The look-ahead at `app/llm/lexicon.yaml:179` checks exclusion words only between "history" and the condition phrase, so an index-accident word after the condition is never checked. The entry's rationale (line 188) defers this to the LLM judge, but the flag is deterministic and medium. Fix: exclude a bare header-form "History:" whose sentence carries an age/sex, mechanism or presentation cue before the condition phrase, and add the same cues to a check after it. Acceptance test: the five sentences above stay quiet, and the four existing hits plus "History is significant for prior assault." still flag.

**F2 (minor). `attribution_word` deny/denying is untested.** `app/llm/lexicon.yaml:1398` adds `deny` and `denying`, read by `grounding.attribution_carried` (`app/backend/grounding.py:195-197`). With both removed, the full unit suite stays green (3246 passed, 4 skipped). Repro: `.venv/bin/python -I -c "from app.backend import grounding as G; print(G.dropped_qualifiers('Deny numbness.', 'Patient reports numbness.'))"` gives `[]` at HEAD and `['self_report']` under M3. Fix: add that assertion (and the 'Patient and wife deny numbness.' variant) to `tests/unit/test_t133_lexicon.py`.

**F3 (minor). A flag excerpt can show no condition.** `History reviewed; notable for pain on cough.` gives excerpt `History reviewed;` from `flags.lexicon_flags`. The T-132 extension (`app/backend/lexicon_scan.py:127-137`) covers only attribution phrases. Fix: extend the unit for a bare history hit whose unit ends at `;` so the excerpt carries the condition. Acceptance test: the excerpt contains "notable for pain on cough".

**F4 (minor). `deny` has no source.** The AC says "with a source". `app/llm/lexicon.yaml:50-53` names "NegEx trigger list" without a path, and labels `deny` an assumption. `grep -n deny memory/ASSUMPTIONS.md` returns nothing. Fix: put the NegEx path (`genConText/negex_triggers.txt`, lines 24-26) in the yaml comment, and record `deny` as a numbered assumption. Acceptance test: grep finds both.

**F5 (minor). Eval evidence is fixture-only.** `evals/reports/20261102T121612Z.md` header reads "ship_bar_met: False  backend `fixture`" and says determinism_3run and unsupported_count_3run need a live backend. Criterion 18 is met because a path exists, and the card records the live re-measure as owed. Fix: run the live claude-cli re-measure and cite the report path before the M3 gate.

**F6 (nit). Unit count does not match the card.** Card AC1 says "unit 3249 passed" in a clean worktree. My run on the archive: `3246 passed, 4 skipped in 178.73s`. Fix: correct the count in the card note.

## Probe output (verbatim, from the probe script)

- `AC-wife FLAG ids=['history_significant_for'] quote=['History provided by wife, notable for lumbar strain.']`
- `AC-diabetes FLAG ids=['history_significant_for'] quote=['History significant for diabetes.']`
- `AC-attr-only quiet ids=[] quote=[]  <= 'History provided by wife.'`
- `[HDR] FLAG ... quote=['History: 45-year-old male, significant for neck pain.']`
- `[HDR] FLAG ... quote=['History reviewed;']  <= 'History reviewed; notable for pain on cough.'`
- `dropped deny->none: ['negation']`; `negation_words: ['deny', 'denying']`; `declined is negation? False False`

## Exercised

- `python3 tools/board.py show T-133` (card and notes read)
- `git show e79c3aa -- app/llm/lexicon.yaml` and `-- tests/unit/test_t133_lexicon.py`; `git show 1218b2e --stat`
- `git archive 1218b2e | tar -x -C <scratchpad>/T-133-r1-archive`
- `.venv/bin/python -I -m pytest tests/unit/test_t133_lexicon.py -q` on the archive: 32 passed
- `.venv/bin/python -I -m pytest tests/unit -q` on the archive: 3246 passed, 4 skipped
- `.venv/bin/python -I research/lexicon_selfcheck.py` on the archive: RESULT: PASS, held-out 115/115
- Probe script `t133_r1_probe.py` in the same scratchpad: 29 sentences through `lexicon_scan.scan` and `flags.lexicon_flags`, plus grounding probes
- Mutant script `t133_r1_mutate.py` and a follow-up on the family look-behind; M3 rerun on the full unit suite (`t133_r1_m3_full.py`)
- `curl` of `raw.githubusercontent.com/chapmanbe/negex/master/genConText/negex_triggers.txt` (HTTP 200); grep of lines 22-26
- `shasum -a 256` of `git show 1218b2e:app/llm/lexicon.yaml` = 30f5c65f...def7, equal to the hash recorded in `evals/reports/calibration.json`
- Read `evals/reports/20261102T121612Z.md` header
- Not run: the `python -m app.pipeline` CLI on the sample (out of this card's brief; lexicon-only change). Outside my lens: whether a "pre_existing" flag is clinically right.

## Right

- Mutants M1, M2, M4, M5 and M6 are each caught by 1 to 9 tests, and the family look-behind is pinned.
- `declined` is kept out of the negation cues and the scene_facts flag still fires (`test_declined_is_not_a_negation_cue`).
- Attribution-only "History provided by wife." and the family, social, interval, work and H&P histories stay quiet.
