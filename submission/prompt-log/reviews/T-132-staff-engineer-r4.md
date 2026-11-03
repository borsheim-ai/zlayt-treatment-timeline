# T-132 staff-engineer review, round 4 (fix-up after §7.4), commit fc60471

Verdict: changes. One major, three minors, one nit, no blockers.

The five §7.4 items are in place and work as directed: overlapping attribution flags join (V1, V3-V7, V9, V10 give one flag with the condition), any `Label:` line and bullet ends the extension (L1-L10), `scan()` on a 24k-character chain takes 0.17 s, the family-noun list is parametrised and pinned, and the title wrap is no longer a fragment (D1-D5, X1, X2). Quotes are verbatim and contiguous (0 violations in 20,000 fuzz texts, 0 partial overlaps in 18,000 fuzz2 texts). The three linearised functions give the same output as round 3 on 86,856 windows each.

The major is a side effect of item 2 that I could not accept as a stated trade-off. Because any capitalised phrase followed by a colon at a line start counts as a label, a condition line such as `Left wrist swollen: since Monday.` now stops the extension. Round 3 showed that condition in the flag; HEAD shows it in no flag. This is the same shape as the round-3 major (a flag whose quote drops the condition), reintroduced by this round. The fix keeps the orchestrator's decision for real section labels (Dx:, Rx:, Plan:) and removes the false stop.

## What I exercised

Archives (no `.git`, `git archive` output): HEAD fc60471 at `artifacts/review-evidence/T-132-r4/arc`; round-3 control 5d7074e at `artifacts/review-evidence/T-132-r4/ctl`. Both are copies of the repository's tracked files; the in-scope files equal the working tree (`diff -q` clean for lexicon_scan.py, flags.py, the T-132 test).

- `pytest tests/unit/test_t132_attribution_unit.py tests/unit/test_summary_trim.py -q -p no:cacheprovider` (archive): 474 passed.
- `pytest tests/unit -q -p no:cacheprovider` (archive): 3540 passed, 1 skipped, 1 failed in 260.18 s. The failure is `test_committed_calibration_regenerates_exactly_from_its_source_commit`. It is a placement artifact, not a T-132 defect: `git archive <sha>` run in a subdirectory of the repository exports only that subtree, so the archive under `artifacts/review-evidence/` gets an empty tar (`T-132-r4-calib-debug.py`: `git archive rc 0 bytes 10240`, `src top []`). The same test passes in the live project root (`pytest tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit -q`: `1 passed`). The live tree has other agents' uncommitted tests, so I did not use it for the full-suite count.
- Round-3 fuzz oracle, `artifacts/review-evidence/T-132-128-r3/T-132-r3-fuzz2.py` (partial overlap and phrase-end on scan hits): HEAD 6,000 texts seed 1 = 0 failing; HEAD 12,000 texts seed 7 = 0 failing; control 5d7074e 6,000 seed 1 = 76 failing (the oracle discriminates). Outputs in `T-132-r4/fuzz2-*.txt`.
- Round-3 fuzz, `T-132-r3-fuzz.py` 20,000 seed 1: HEAD 0 not-verbatim, 0 blank-line quote, 0 overlap, 69 "ends inside phrase" (control 434 = 166 + 268). The 69 are verbatim fragments; see finding 5.
- Item probes, both archives: `T-132-r3-regress.py` (V1-V10), `T-132-r3-title.py` (D1-D8), `T-132-r4-items.py` (L1-L10, C1-C5), `T-132-r4-title-extra.py` (X1-X6), `T-132-r4-msrow.py` (Y1-Y4), `T-132-r4-lost.py` (K1-K3).
- `T-132-r4-perf.py` (archive and control): `scan` 24,010 chars 0.17 s (control 49.36 s); `lexicon_flags` 11.00 s (the flags._hedge_run cost, T-147, not charged here; card status ready).
- `T-132-r4-equiv.py`: round-3 (5d7074e) and HEAD definitions of `negated`, `_sentence_bounds`, `_is_source_sentence` on 1,500 fuzz texts plus 27 corpus files: 86,856 / 86,856 / 86,871 calls, 0 differences.
- `T-132-r4-mutants.py`, one mutant per item against the T-132 test file: base 156 passed; M1 no join 62 failed; M2 label not a hard break 12 failed; M3 `cousin` removed 2 failed; M4 `Dr.` as sentence end 3 failed. All four killed.
- `T-132-r4-dump.py` + `T-132-r4-hidden-cmp.py`: flag spans for 20,000 generated texts, HEAD vs control. Known conditions shown by control and in no HEAD flag: 28 occurrences in 26 texts; shown by HEAD only: 5.
- `T-132-r4-items.py`, `-title-extra.py`, `-msrow.py`, `-lost.py` run on both archives (outputs saved beside them).
- Read: `T-132-staff-engineer-r3.md` (findings 1-5 and their acceptance tests), `git show fc60471 -- app/backend/lexicon_scan.py`, `tests/unit/test_t132_attribution_unit.py` lines 338-402 and the test names.
- Not exercised: browser or API view; `flags.merge` live path; the evals runner (the CLI `python -m app.pipeline` was not re-run in this round; the lexicon diff is confined to scan-side functions and the equivalence check covers them).

## Per-item status

1. Overlap join: done (V1, V3-V7, V9, V10 one flag each; V8 unchanged).
2. `Label:` and bullet stop: done as directed (L1-L7, L10, bullets). Side effect: finding 1.
3. Linear scan: done (scan 0.17 s at 24k, call-count test, equivalence of the three functions). T-147 noted, not charged.
4. Family nouns: done (24 nouns parametrised and pinned; M3 killed).
5. Title wrap: done for the fragment (D1-D5, X1, X2). Two residual shapes, finding 3 and finding 4.

## Findings

See the JSON block. Finding 1 is the one that blocks the pass.

```json
{"card": "T-132", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD fc60471 (artifacts/review-evidence/T-132-r4/arc) vs round-3 control 5d7074e (artifacts/review-evidence/T-132-r4/ctl); app/backend/lexicon_scan.py (fc60471 diff), tests/unit/test_t132_attribution_unit.py; fixture-only, no network, no server; sample case not re-run in this round",
 "exercised": [
  "personas/staff-engineer.md read in full; reviews/T-132-staff-engineer-r3.md read; board show T-132 and T-147 read; git show fc60471 -- app/backend/lexicon_scan.py read in full",
  "git archive HEAD and 5d7074e into artifacts/review-evidence/T-132-r4/arc and ctl; diff -q of lexicon_scan.py, flags.py, the T-132 test: archive equals working tree",
  "pytest tests/unit/test_t132_attribution_unit.py tests/unit/test_summary_trim.py -q on arc: 474 passed",
  "pytest tests/unit -q on arc: 3540 passed, 1 skipped, 1 failed (test_committed_calibration_regenerates_exactly_from_its_source_commit); failure traced to git archive from a subdirectory giving an empty tar (T-132-r4-calib-debug.py); same test passes in the live root (1 passed)",
  "T-132-r3-fuzz2.py on arc: 6000 seed 1 = 0 failing, 12000 seed 7 = 0 failing; on ctl 6000 seed 1 = 76 failing (oracle discriminates)",
  "T-132-r3-fuzz.py on arc 20000 seed 1: 0 not-verbatim, 0 blank-line quote, 0 overlap, 69 ends-inside-phrase; ctl 434 (166 ends-inside + 268 overlap)",
  "T-132-r3-regress.py and T-132-r3-title.py on arc: V1-V10 one flag each with the condition except V8 (unchanged); D1-D5, D7, D8 one flag; D6 two flags (first without condition)",
  "T-132-r4-items.py on arc and ctl: L1-L10 stop at Label:/bullet/SOAP A:/S:/BP:/PLAN:, L8 inline colon extends, L9 time is not a label; C1 one flag, C2 one flag, C4 stops at sentence end, C5 two flags",
  "T-132-r4-title-extra.py on arc and ctl: X1/X2 initials one unit, two flags (first without condition); X3 sentence-final Dr. now joins into one flag; X4 one-line named who-clause also gives two flags (cause is the who-clause vocabulary, not the wrap)",
  "T-132-r4-lost.py on arc and ctl: K1 'Hx obtained via patient's son;\\nLeft wrist swollen: since Monday.' ctl one flag with the condition; arc attribution-only flag, condition in no flag; K3 Dx: stops as intended",
  "T-132-r4-msrow.py on arc and ctl: Y1 'Hx per MS' fragment flag exists on ctl too (not new); Y4 'Hx per EMS: neck pain.' line-start stop",
  "T-132-r4-perf.py on arc and ctl: scan 24,010 chars 0.17 s (ctl 49.36 s); lexicon_flags 11.00 s (T-147)",
  "T-132-r4-equiv.py: negated, _sentence_bounds, _is_source_sentence round-3 vs HEAD on 86,856 / 86,856 / 86,871 calls: 0 differences",
  "T-132-r4-mutants.py: base 156 passed; M1 join removed 62 failed; M2 label not hard 12 failed; M3 cousin removed 2 failed; M4 Dr. sentence end 3 failed",
  "T-132-r4-dump.py + T-132-r4-hidden-cmp.py: 20000 texts, HEAD vs ctl; condition shown by ctl and in no HEAD flag: 28 occurrences in 26 texts; shown by HEAD only: 5",
  "Not exercised: browser/API view; flags.merge live path; evals runner; python -m app.pipeline re-run in this round"],
 "verdict": "changes",
 "scores": {"correctness": 3, "determinism": 4, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [
  {"severity": "major",
   "title": "A capitalised condition line ending in a colon ('Left wrist swollen:') is read as a section label, so the attribution flag drops a condition that round 3 showed in the same sentence",
   "evidence": "Repro: `.venv/bin/python -I artifacts/review-evidence/T-132-r4/T-132-r4-lost.py artifacts/review-evidence/T-132-r4/arc` gives flags [(pre_existing, \"Hx obtained via patient's son;\")] for K1 \"Hx obtained via patient's son;\\nLeft wrist swollen: since Monday.\"; the same command on .../ctl gives one flag \"Hx obtained via patient's son;\\nLeft wrist swollen: since Monday.\" (T-132-r4-lost-arc.txt, T-132-r4-lost-ctl.txt). Cause: app/backend/lexicon_scan.py `_LINE_LABEL` (line ~133) matches any 1-4 word capitalised phrase followed by a colon and space, and `_soft_wraps` makes that newline hard. Corpus: T-132-r4-hidden-cmp-out.txt, 28 occurrences in 26 of 20,000 generated texts shown by ctl and in no HEAD flag, e.g. 'Hx obtained via\\npatient's son: Hx from\\nthe patient's wife\\nLeft wrist swollen: who\\ninterpreted: History obtained from Dr.\\nSmith;' (ctl quote includes 'Left wrist swollen'; HEAD quote stops before it). Also 'Hx per EMS: denies fever' and 'Hx per EMS: neck pain' lines stop the attribution in T-132-r4-msrow-arc.txt.",
   "why_it_matters": "AC1 of the card says the flag's quote extends over the following clause of the same sentence 'so the condition is shown'. A line that is one clause of the same sentence (K1 has no sentence end between ';' and '.') now drops the condition from every flag. Nothing is invented and the record is intact, but the paralegal sees an attribution with no condition, which is the round-1 and round-3 failure shape. It is a regression from the round-3 code, introduced by this round. The regex cannot tell a section label from condition text; only the word list can. Labelled: this violates AC1 as written for these shapes, so it is not a judgement call.",
   "fix": "Keep the orchestrator's decision for record section labels: stop at a `Label:` line only when the label is a closed section name (Plan, Medications, Meds, Rx, Dx, Assessment, Allergies, Disposition, Discharge instructions, Vitals, Exam, SOAP letters S/O/A/P) or an all-capitals header, held in app/llm/lexicon.yaml as the project does for other lists. Title-case or capitalised condition lines ('Left wrist swollen:', 'Neck pain:', 'Hx per EMS:') keep extending, as they do inside a line.",
   "acceptance_test": "K1 gives one pre_existing flag whose quote contains 'Left wrist swollen'; K3 ('Hx per EMS;\\nDx: sprain, lumbar strain 2019.') still stops at 'Hx per EMS;'; L1, L2, L5, L6, L7, L10 unchanged; add a row for 'Hx per EMS;\\nNeck pain: onset 2019.' expecting the whole text; T-132-r4-hidden-cmp.py on the fixed build shows 0 occurrences shown by ctl and in no HEAD flag for conditions in the list."},
  {"severity": "minor",
   "title": "The 24k linear-time test asserts a wall-clock bound",
   "evidence": "tests/unit/test_t132_attribution_unit.py:348 `assert dt < 2.0, dt` inside test_item3_a_24k_character_chain_scans_in_linear_time (time.perf_counter around LS.scan). The call-count test at :351-357 is the exact check.",
   "why_it_matters": "Persona section 4.14 forbids tests that depend on wall-clock time. The bound has a 20x margin (0.17 s measured) but will flake on a loaded CI runner.",
   "fix": "Remove the time bound and keep the call-count assertion (`len(calls) <= 3 * n`) plus the same-flag assertion; if a time guard is wanted, put it in a perf script under artifacts/, not in unit tests.",
   "acceptance_test": "test_item3_* passes with the time bound removed; monkeypatching _attribution_only back to a quadratic walk (per-hit rescan of the chain) still fails the call-count test at n = 600."},
  {"severity": "minor",
   "title": "Named-person and initialled who-clauses still give two flags, the first without the condition (round-3 finding 3 acceptance for D6 not met)",
   "evidence": "T-132-r4-items-arc.txt C5 'Hx per EMS; who interpreted for Dr.\\nSmith; prior neck injury.' -> ['Hx per EMS; who interpreted for Dr.\\nSmith;', 'prior neck injury.']; T-132-r4-title-extra-arc.txt X4 one line 'Hx per EMS; who interpreted for Dr. Smith; prior neck injury.' -> the same two flags (so the wrap is not the cause); X1 'Hx per EMS; Hx per J.\\nSmith; prior neck injury.' -> ['Hx per EMS; Hx per J.\\nSmith;', 'prior neck injury.']. The phrase vocabulary (_WHO_INTERPRETED, _HISTORY_VIA) accepts 'for the patient' but not a titled or initialled name. X5 'who interpreted for the patient' stays one flag.",
   "why_it_matters": "The first flag reads as prior-condition evidence with no condition in it. Nothing is invented; the second flag shows the condition. This is the round-2 minor 2 narrowness, now seen for names; the wrap fix itself is complete.",
   "fix": "Let the who-clause and the source phrase accept a title plus name (`(dr|mr|mrs|ms)\\.?\\s+[\\w'-]+`) and a bare initial (`[A-Z]\\.`), reusing the sentences module's _ALWAYS_ABBREV; or record the narrowness as a SCOPE_CUTS row with the X1/X4 examples.",
   "acceptance_test": "D6 ('Hx per EMS; who interpreted for Dr.\\nSmith; prior neck injury.') and X4 give one pre_existing flag containing 'prior neck injury'; X1 likewise; X5 unchanged."},
  {"severity": "minor",
   "title": "A sentence-final 'Dr.' followed by a new line is now a soft wrap, so one flag crosses a sentence end",
   "evidence": "T-132-r4-title-extra-arc.txt X3 'Hx per EMS; seen by Dr.\\nPrior neck injury.' -> ['Hx per EMS; seen by Dr.\\nPrior neck injury.']; the same row on T-132-r4-title-extra-ctl.txt gives ['Hx per EMS; seen by Dr.', 'Prior neck injury.']. Cause: app/backend/lexicon_scan.py `_soft_wraps` (abbreviation check on the '.' before the newline).",
   "why_it_matters": "This is the trade-off of item 5 (Dr. is not a sentence end). The condition is still shown, but the quote now runs across a real sentence boundary, which the extension otherwise never does. Labelled as a judgement cost of the orchestrator's direction, not a spec violation.",
   "fix": "Either accept and record it in SCOPE_CUTS with X3 as the example, or narrow the rule to a title followed by a capitalised name on the next line and a lower-case or name-shaped continuation.",
   "acceptance_test": "X3 either gives two flags (Dr. ends the sentence when no name follows the title on the next line) or a SCOPE_CUTS row cites X3."},
  {"severity": "minor",
   "title": "The round-3 fuzz phrase oracle still reports 69 verbatim fragment quotes; the card's evidence line cites 'reviewer fuzz oracle 0 failing' without naming which oracle",
   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-132-128-r3/T-132-r3-fuzz.py artifacts/review-evidence/T-132-r4/arc 20000 1` -> 69 ends-inside-phrase, 0 not-verbatim, 0 blank-line, 0 overlap (T-132-r4/fuzz-HEAD-20000-s1.txt). Example: 'prior\\nneck injury\\n\\napprox. 2 yrs ago\\n\\nHx per MS history Hx\\nvia interpreter' -> flag 'Hx per MS history Hx' (T-132-r4/ends-inside-probe-HEAD.txt). The phrase after 'Hx' is suppressed as an attribution-only sentence, and the physical-line unit is kept because no source phrase matches at the hit's end, so the extension never runs.",
   "why_it_matters": "The quote is verbatim and contiguous, so the card's stated invariant holds. The fragments are a display defect of the kind round 1 ruled out. The count fell from 434 (ctl) to 69, so the fix is not a regression, but the card should say which oracle is at zero.",
   "fix": "When a history hit has no source phrase at its end, still walk the soft-wrapped unit to its chain end if the next soft-wrapped clause starts a history phrase; or name the 69 shapes in SCOPE_CUTS. In the card's AC evidence, cite fuzz2 by name and report the fuzz phrase count beside it.",
   "acceptance_test": "fuzz.py on the fixed build: 0 ends-inside-phrase at seed 1, or the residual shapes are listed in SCOPE_CUTS and each has a unit row."},
  {"severity": "nit",
   "title": "Tracked performance debt on the flag path (not charged to T-132): lexicon_flags takes 11.0 s on a 24k chain while scan takes 0.17 s",
   "evidence": "T-132-r4-perf-arc.txt: 'chain2000 ... scan 0.17s ... lexicon_flags 11.00s'; board show T-147 status ready.",
   "why_it_matters": "A 60,000-character record can still hold a request for minutes in deterministic code with no timeout. Tracked as T-147; noted here so the gate sees it.",
   "fix": "T-147 (per-unit memo in flags.lexicon_flags).",
   "acceptance_test": "T-147 acceptance."}
 ],
 "whats_right": [
  "The five §7.4 items are in place: V1, V3-V7, V9, V10 give one flag with the condition; L1-L10 stop as directed; scan on 24k characters 0.17 s (control 49 s); family nouns pinned and each killed by a mutant; Dr. wrap fragments gone.",
  "Quotes stay verbatim and contiguous: 0 not-verbatim and 0 blank-line quotes in 20,000 fuzz texts, 0 partial overlaps in 18,000 fuzz2 texts (the round-3 control fails 76 of 6,000), and negated, _sentence_bounds and _is_source_sentence give identical output to round 3 on 86,856 windows each.",
  "Tests are mutation-sensitive: four one-line mutants (join, label stop, a family noun, Dr. sentence end) each fail 2-62 tests, and the CLI-level probes match the worker's stated rows."],
 "questions_for_chris": ["Should a capitalised condition line such as 'Left wrist swollen:' end a prior-condition quote, or only a closed list of record section labels? The orchestrator's decision 2 reads as any 'Label:' line; finding 1 assumes section labels only."]
}
```
