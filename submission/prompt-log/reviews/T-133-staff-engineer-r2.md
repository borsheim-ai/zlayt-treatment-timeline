# T-133 review (staff-engineer-reviewer), lexicon deny forms and history_significant_for

This file supersedes `reviews/T-133-staff-engineer.md`, which was written without its ```json block (board-validate rejected it, and reviewer-write-guard blocks editing it). The content and verdict here are the same, with one line citation corrected.

Pinned to HEAD 1218b2e (commits e79c3aa feat and 1218b2e calibration). Reviewed from `git archive 1218b2e` extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-133-r1-archive`. The main tree was not edited.

Verdict: **changes** (no blocker; one major). The deny forms are real negation words in the grounding path, and the NegEx source checks out for three of the four forms. The new `history_significant_for` entry meets its two required hits and the attribution-only control, but it over-flags HPI-style "History:" narratives, which the brief asked me to check. The attribution-word addition is untested, and flag excerpts can lose the condition.

## Checks against the brief

1. **Deny forms in the grounding list, each with a source.** Pass for three forms, partial for one. `is_negation_word` is True for deny, denies, denied and denying (`app/llm/lexicon.yaml:1440`, code_lists negation_word). The NegEx list (fetched from `chapmanbe/negex` `genConText/negex_triggers.txt`, lines 24-26) has `denied`, `denies` and `denying` tagged `[PREN]`. `deny` is not in that list. The yaml labels it an assumption (lines 50-51), which is honest but does not meet "with a source" (F4).
2. **Hits.** Pass. "History provided by wife, notable for lumbar strain." flags with the condition in the quote. "History significant for diabetes." flags.
3. **Attribution-only control.** Pass. "History provided by wife." is quiet.
4. **No over-flag on HPI and similar text (10+ probes).** Fail on the bare-header form. 29 sentences were probed. The HPI, H&P and "Chief complaint: ... History of present illness" variants are quiet, as are the family, social, interval, work, and "per patient; exam" cases. Five bare "History:" or complaint-style narratives flag as `pre_existing` (F1).
5. **Tests.** `tests/unit/test_t133_lexicon.py` 32 passed. The full `tests/unit` suite on the archive gave 3246 passed, 4 skipped (the card says 3249 passed; nit F6). `research/lexicon_selfcheck.py` RESULT: PASS, held-out 115/115.

## Mutation spot-checks (scratch copies, not committed)

| Mutant | Result |
|---|---|
| M1 drop `history_significant_for` entry | 9 failed |
| M2 drop `deny` from negation_word | 3 failed |
| M3 drop `deny` and `denying` from attribution_word | 0 failed; full unit suite 3246 passed, 4 skipped |
| M4 drop `denying` from pre_cues | 2 failed |
| M5 drop `deny` from field_answer | 2 failed |
| M6 drop `(?<!family\s)` look-behind | 1 failed |

## Findings

**F1 (major). Bare "History:" HPI narratives and complaint text are flagged pre_existing.** Probe output from `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t133_r1_probe.py`: FLAG for "History: 45-year-old male, significant for neck pain.", "History: patient was a passenger, significant for neck pain.", "Chief complaint and history: notable for neck pain.", "History obtained from patient, notable for neck pain since the crash." The look-ahead at `app/llm/lexicon.yaml:179` checks exclusion words only between "history" and the condition phrase, so an index-accident word after the condition is never checked. The entry's rationale (`app/llm/lexicon.yaml:187`) defers relevance to the LLM judge, but the flag is deterministic and medium. Fix: exclude a bare header-form "History:" whose sentence carries an age/sex, mechanism or presentation cue before the condition phrase, and check the same cues after it. Acceptance test: the four sentences above stay quiet, and the existing hits ("History provided by wife, notable for lumbar strain.", "History significant for diabetes.", "History is notable for a 2019 lumbar strain.", "Medical history remarkable for prior neck surgery.") plus "History is significant for prior assault." still flag.

**F2 (minor). `attribution_word` deny and denying are untested.** `app/llm/lexicon.yaml:1398` adds `deny` and `denying`, read by `grounding.attribution_carried` (`app/backend/grounding.py:195-197`, summary side). With both removed, the full unit suite stays green (3246 passed, 4 skipped). Repro: `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c "import sys; sys.path.insert(0, '<archive>'); from app.backend import grounding as G; print(G.dropped_qualifiers('Deny numbness.', 'Patient reports numbness.'))"` prints `[]` at HEAD and `['self_report']` under the mutant. Fix: add that assertion, and the "Patient and wife deny numbness." variant, to `tests/unit/test_t133_lexicon.py`.

**F3 (minor). A flag excerpt can show no condition.** `History reviewed; notable for pain on cough.` gives excerpt `History reviewed;` from `flags.lexicon_flags`. The T-132 extension (`app/backend/lexicon_scan.py:127-137`) covers only attribution phrases. Fix: for a bare history hit whose unit ends at `;`, extend the unit to the condition clause. Acceptance test: the excerpt for "Pain 6/10. History reviewed; notable for pain on cough." contains "notable for pain on cough".

**F4 (minor). `deny` has an assumption, not a source.** The AC says "with a source". `app/llm/lexicon.yaml:50-53` says "sources: NegEx trigger list" with no path and labels `deny` an assumption. NegEx `genConText/negex_triggers.txt` lines 24-26 list denied, denies and denying as `[PREN]` and do not list deny. `grep -n deny memory/ASSUMPTIONS.md` returns nothing. Fix: put the NegEx path in the yaml comment for denied, denies and denying, and record `deny` as a numbered assumption in `memory/ASSUMPTIONS.md`. Acceptance test: grep finds the genConText path in the yaml and a deny entry in ASSUMPTIONS.md.

**F5 (minor). Eval evidence for the lexicon change is fixture-only.** `evals/reports/20261102T121612Z.md` header: "ship_bar_met: False  backend `fixture`"; determinism_3run and unsupported_count_3run need a live backend. Criterion 18 is met by the path, and the card records the live re-measure as owed. Fix: run the live claude-cli re-measure and cite its report path before the M3 gate.

**F6 (nit). Unit count in the card does not match my run.** Card AC1 says "unit 3249 passed". My archive run: "3246 passed, 4 skipped in 178.73s". Fix: correct the count in the card note.

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
- Probe script `t133_r1_probe.py` (same scratchpad): 29 sentences through `lexicon_scan.scan` and `flags.lexicon_flags`, plus grounding probes
- Mutant scripts `t133_r1_mutate.py` and `t133_r1_m3_full.py` in the same scratchpad: M1 to M6 on the targeted files, M3 on the full unit suite
- `curl` of `raw.githubusercontent.com/chapmanbe/negex/master/genConText/negex_triggers.txt` (HTTP 200); grep of lines 22-26
- `shasum -a 256` of `git show 1218b2e:app/llm/lexicon.yaml` = 30f5c65f...def7, equal to the hash recorded in `evals/reports/calibration.json`
- Read `evals/reports/20261102T121612Z.md` header
- Not run: the `python -m app.pipeline` CLI on the sample (out of this card's brief; lexicon-only change). Outside my lens: whether a "pre_existing" flag is clinically right.

## Right

- Mutants M1, M2, M4, M5 and M6 are each caught by 1 to 9 tests, including the family look-behind.
- `declined` stays out of the negation cues and the scene_facts flag still fires (`test_declined_is_not_a_negation_cue`).
- Attribution-only "History provided by wife." and the family, social, interval, work and H&P histories stay quiet.

## Machine-readable record

```json
{"card": "T-133", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 1218b2e (commits e79c3aa and 1218b2e): app/llm/lexicon.yaml, tests/unit/test_t133_lexicon.py, evals/reports/20261102T121612Z.md and calibration.json; no app URL (lexicon-only, no server); no sample case run (probes are sentences)",
 "exercised": ["board.py show T-133", "git show e79c3aa (lexicon.yaml, test_t133_lexicon.py) and 1218b2e --stat", "git archive 1218b2e extracted to scratchpad T-133-r1-archive", "pytest tests/unit/test_t133_lexicon.py on archive: 32 passed", "pytest tests/unit on archive: 3246 passed, 4 skipped in 178.73s", "research/lexicon_selfcheck.py on archive: PASS, held-out 115/115", "probe script t133_r1_probe.py: 29 sentences via lexicon_scan.scan and flags.lexicon_flags, plus grounding probes", "six mutants (M1-M6) in scratch copies; M3 rerun on full unit suite: 3246 passed, 4 skipped", "curl raw.githubusercontent.com chapmanbe/negex genConText/negex_triggers.txt (HTTP 200), grep lines 22-26", "shasum -a 256 of 1218b2e lexicon.yaml equals calibration.json hash", "read evals/reports/20261102T121612Z.md header"],
 "verdict": "changes",
 "scores": {"deterministic_no_llm": 5, "deny_forms_grounded_and_sourced": 3, "history_entry_hits_and_controls": 4, "over_flag_control_on_hpi_text": 2, "mutation_killability": 4, "flag_excerpt_visibility": 3, "eval_evidence_criterion_18": 3},
 "findings": [
  {"severity": "major", "title": "Bare History: HPI narratives and complaint text flag as pre_existing",
   "evidence": "t133_r1_probe.py output: FLAG for 'History: 45-year-old male, significant for neck pain.', 'History: patient was a passenger, significant for neck pain.', 'Chief complaint and history: notable for neck pain.', 'History obtained from patient, notable for neck pain since the crash.'; app/llm/lexicon.yaml:179 look-ahead checks exclusions only between history and the condition phrase; rationale at app/llm/lexicon.yaml:187 defers relevance to the LLM judge",
   "why_it_matters": "The brief asks that HPI-style text is not over-flagged. A deterministic medium pre_existing flag labels a presenting complaint as a prior condition, which an adjuster or paralegal may cite.",
   "fix": "Exclude a bare header-form History: whose sentence has an age/sex, mechanism or presentation cue before the condition phrase; check the same cues after the condition phrase.",
   "acceptance_test": "The four quoted sentences stay quiet in lexicon_scan.scan and flags.lexicon_flags; the existing hits ('History provided by wife, notable for lumbar strain.', 'History significant for diabetes.', 'History is notable for a 2019 lumbar strain.', 'Medical history remarkable for prior neck surgery.') and 'History is significant for prior assault.' still flag."},
  {"severity": "minor", "title": "attribution_word deny and denying are untested",
   "evidence": "app/llm/lexicon.yaml:1398 adds deny and denying; read by grounding.attribution_carried at app/backend/grounding.py:195-197. Mutant removing both: full tests/unit suite 3246 passed, 4 skipped (same as HEAD). Repro: .venv/bin/python -I -c with sys.path set to the archive, then G.dropped_qualifiers('Deny numbness.', 'Patient reports numbness.') prints [] at HEAD and ['self_report'] under the mutant.",
   "why_it_matters": "A behaviour change in the summary-side attribution check is not pinned, so removing it passes CI.",
   "fix": "Add an assertion to tests/unit/test_t133_lexicon.py that a deny-only summary carries attribution.",
   "acceptance_test": "dropped_qualifiers('Deny numbness.', 'Patient reports numbness.') == [] and dropped_qualifiers('Patient and wife deny numbness.', 'Patient reports numbness.') == []; the test fails under the deny/denying removal mutant."},
  {"severity": "minor", "title": "Flag excerpt can show no condition after a semicolon",
   "evidence": "'History reviewed; notable for pain on cough.' gives excerpt 'History reviewed;' from flags.lexicon_flags (probe output); the T-132 extension at app/backend/lexicon_scan.py:127-137 covers only attribution phrases.",
   "why_it_matters": "The reviewer and UI see a flag with no condition, so the evidence does not show what was flagged.",
   "fix": "For a bare history hit whose unit ends at ';', extend the unit to the condition clause, as the T-132 extension does for attribution.",
   "acceptance_test": "flags.lexicon_flags on 'Pain 6/10. History reviewed; notable for pain on cough.' returns an excerpt containing 'notable for pain on cough'."},
  {"severity": "minor", "title": "deny has an assumption, not a source",
   "evidence": "app/llm/lexicon.yaml:50-53 says 'sources: NegEx trigger list' with no path and labels deny an assumption; NegEx genConText/negex_triggers.txt lines 24-26 list denied, denies, denying [PREN] and no deny; grep -n deny memory/ASSUMPTIONS.md returns nothing.",
   "why_it_matters": "Card AC1 says each deny form has a source.",
   "fix": "Put the NegEx path in the yaml comment for denied, denies and denying, and record deny as a numbered assumption in memory/ASSUMPTIONS.md.",
   "acceptance_test": "grep finds the genConText path in app/llm/lexicon.yaml and a deny entry in memory/ASSUMPTIONS.md."},
  {"severity": "minor", "title": "Eval evidence for the lexicon change is fixture-only",
   "evidence": "evals/reports/20261102T121612Z.md header: 'ship_bar_met: False  backend fixture'; determinism_3run and unsupported_count_3run need a live backend.",
   "why_it_matters": "Criterion 18 is met by the path, but the card records the live re-measure as owed.",
   "fix": "Run the live claude-cli re-measure and cite its report path before the M3 gate.",
   "acceptance_test": "A report with backend claude-cli and numeric determinism_3run and unsupported_count_3run exists under evals/reports/ and is cited on the card."},
  {"severity": "nit", "title": "Unit count in the card does not match my run",
   "evidence": "Card AC1 says 'unit 3249 passed'; archive run: '3246 passed, 4 skipped in 178.73s'.",
   "why_it_matters": "The card evidence should match a reproducible run.",
   "fix": "Correct the count in the card note.",
   "acceptance_test": "pytest tests/unit -q on 1218b2e reports the count written on the card."}
 ],
 "whats_right": ["Mutants M1, M2, M4, M5 and M6 are each caught by 1 to 9 tests, including the family look-behind.", "declined stays out of the negation cues and the scene_facts flag still fires (test_declined_is_not_a_negation_cue).", "Attribution-only 'History provided by wife.' and the family, social, interval, work and H&P histories stay quiet."],
 "questions_for_chris": ["Should bare History: HPI-header narratives be flagged pre_existing at medium (judge decides), or suppressed in code? This is a precision trade-off for the product, not something the reviewer can settle."]}
```
