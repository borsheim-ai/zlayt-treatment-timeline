---
name: design-review-patterns
description: Recurring design-level defects found reviewing the Zlayt treatment-timeline architecture (T-014 rounds 1-2); check these first on later cards
metadata:
  type: project
---

Round 1 (2026-11-01, fail): defects, all resolved in round 2 but re-check them in M2 code reviews.
- Flag/gap logic keyed on LLM entries instead of code-parsed record dates (r5 dropped -> false 42-day gap). In M2 test that gaps use `records.date_iso`.
- Export default omitted verbatim excerpt (cite=short) vs ship bar 1 / R-EX-2.
- Judge #2 skipped on code-classified amounts; summary numerals not code-checked; retry count wording inconsistent.
- Illustrative JSON in api.md had wrong offsets and a `{...}` block. Re-run `artifacts/review-evidence/T-014-json-check.py` and `T-014-r2-offset-check.py` after any api.md edit.

Round 2 (changes, 4 majors) - new pattern: the architect's docs drift from REQUIREMENTS revision N because writer and architect edit in parallel.
- Export format restated in ADR-009, api.md and the golden file differ from REQUIREMENTS sec 6 (dot leaders, Source line, total-line parenthetical). Check byte-equality test target first.
- ADR-011 amount rules: simulate them on all `evals/golden/*.txt` (`T-014-r2-amount-sim.py`); case_09 `$275` billing-statement amount fell to `unclear`. Charges are accept/dismiss only, so a missed rule is unrecoverable for the user.
- Anything that calls a judge at request time (edit re-check) needs a stated judge-failure / FixtureMiss path; demo mode makes every edit a fixture miss.
- ADR-016 over-applied D-012 (forced inclusion of lexicon sentences; `mg.` abbreviation) vs R-TL-8 hedge-only.
- D-018 landed after the architect started; always check the newest D-xx against ADR category lists.

**Why:** these made T-014 fail round 1 (2026-11-01) and require changes in round 2.
**How to apply:** on M2 backend review, run the golden amount simulation against the real `amounts.py`, check export equals golden file, and grep for a defined judge-unavailable path.

Round 3 (2026-11-01, changes, 5 majors): same parallel-edit drift, now against lexicon v2, D-021/D-022 and the golden file.
- Check ADR category lists against the real `app/llm/lexicon.yaml` category values (6 lexicon categories were missing from ADR-013; P1 floor flag had no template).
- A binding D-xx can land during the architect's round (D-022 SUMMARY_DROPS_QUALIFIER was missed); grep new reason codes in api.md appendix.
- Embedded copies of files others own (api.md export vs golden) drift within the hour; recommend pointer + test, not a copy. Working tree can hold other agents' uncommitted edits: compare with `git show <rev>:path`.
- api.md examples that claim golden provenance: verify against the golden `gap_excluded_records` (confirm_date example put a phone note into gap math).
- Cut-line items can silently undo a structural control (per-record flag pass): read the cut line against ADR-008.
- Evidence: `artifacts/review-evidence/T-014-r3-amount-sim.py` / `-amount-demo.py` (real lexicon, ADR-011 r3 rules; 14/14 dollar amounts).

Round 4 = T-028 consistency pass (2026-11-01, fail: 1 blocker, 3 majors). Evidence: `artifacts/review-evidence/T-028-review-checks.py`.
- Fix claims drift from the file: the architect's "mg. one unit" evidence is contradicted by api.md:91 (two units). T-014 r3 M4 came back after DECISIONS was fixed; ADR text and illustrative JSON are separate places to fix. Re-run the R-TL-2 splitter on sample record 2 after any api.md sentence edit.
- "Fixed text of R-EX-4(1)" label on a string that is not R-EX-4(1). The spec itself had two AI lines (R-EX-4(1) vs section 6 / golden). Architect followed the golden-authority rule silently. When the spec disagrees with itself, the card must say so, not claim alignment.
- A spec reconciliation check ("diff of the example against golden, expect none") cannot pass once the example is a pointer. Amend the check row or the example; never leave them disagreeing.
- "Each with a template" in an ADR is a generic assertion; count per-category template text, not the word "template".
- Evidence counts with no script in the repo ("14/14 blocks, 17/17 offsets") are not reproducible; ask for the script in artifacts/review-evidence.

Round 2 of T-028 (2026-11-01, changes: 1 major, 3 minors carried or new, 2 nits; 0 blockers). Evidence: `artifacts/review-evidence/T-028-r2-checks.py`.
- Stale blockers: the round-1 AI-line blocker was closed by a spec-side commit (3ff15cd) while the review still quoted the old wording. Re-grep every disputed string before re-filing.
- Check weakened to pass: the spec row 1 diff check was rewritten to a grep for a filename ("expect >= 1"), and the golden equality it implied has no test (tests/unit is empty). A check that passes without the content it is meant to verify is a finding even when the doc now agrees.
- Template tables: 21 rows cover 13 of 13 lexicon categories, but slot names differ between legend, rows and example (`{a}` vs `{date A}`, `{source}` vs `{provider}`), and recovery_context is `n/a` while the text says every category has one.
- My own round-1 script had a hand-typed constant in AC4b (span filter caught a second unit) and searched for stale wording in AC5. Compare computed to computed, never to a literal, and retire checks whose target text moved.
- Carried, still open: README-arch lexicon line (v1 names), confirm_date `f_warn_date_r8` vs golden (no record 8 warning), "14/14, 17/17" count with no script.

**Why:** these were the open T-014 r3 items closed by T-028; closure claims were partly false, and round 2 showed the fixes can also weaken the checks.
**How to apply:** on any ADR or api.md consistency card, grep the claimed string in every file it names, run the splitter/offset check and compare computed values, and check that any spec check row still tests content, not a filename, before accepting "aligned".
