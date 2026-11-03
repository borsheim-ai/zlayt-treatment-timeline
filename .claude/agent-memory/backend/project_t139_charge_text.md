---
name: t139-charge-text
description: T-139 CHARGE_TEXT_IN_ENTRY rule: where the check lives, how entries are held out, why tests had to be reshaped, shared-file commit pitfall
metadata:
  type: project
---

`app/backend/charge_text.py` (pure): `currency_strings`, `check(summary, excerpt)`, `trim_summary` (D-054 suffix rule, uses `summary_trim.split_clauses`/`content_words`). Wired in: `generator.verify` adds code reason `CHARGE_TEXT_IN_ENTRY` (state needs_review, NOT rejected); `review.set_review` -> `charge_text_error` (422 CODE_CHECK_FAILED, same shape as D-051); `review._check_summary` (edit + manual entry, placed AFTER the number/side/qualifier checks so `SUMMARY_NUMBER_NOT_IN_EXCERPT` still wins); `review._edit` auto-trims the AI summary when the new quote is clean (warning `CHARGE_CLAUSE_REMOVED`); `export._View.in_entries` drops any entry with an amount (defence in depth) and `_amount_quote` narrows a charge line's quote to the clause with its own figure; `_bills` skips providers with a dismissed charge. Eval: `evals/letter_check.py` (+ row/blocker in evals/run.py).

**Why:** GATE-M2 claims-adjuster blocker: recorded model output quotes 'Charge per visit $140' / 'ED charge: $3,915.' into the carrier letter (extract_v1.md line 12 asks for "charge" sentences). Rule: amounts only in the BILLED CHARGES section (accepted charges + total line) and internal notes.

**Pitfalls:** (1) NOT trimming at generation time on purpose: a changed summary changes the J1 prompt hash, ~49 fixture entries would miss (fill-missing needs a live LLM). Trim happens only in the edit path. (2) 49 golden/library entries are now needs_review: the recorded sample's e2/e4 are held, so tests that accepted them were reshaped (test_trace `_without_amount_entries`, narrative fixture re-recorded over the other 7 entries with claude-cli, api_routes/lib09 expectations). (3) committed `evals/reports/calibration.json` counts by state are now stale (verified -> needs_review): regenerate with `--write-calibration` on a clean tree (not done, tree dirty). (4) comma-split on thousands separators (`$1,100`) broke the clause regex; use `,(?=\d)`. (5) The shared working tree has other workers' uncommitted hunks in review.py/evals/run.py/pipeline.py: check `git diff <file>` is only yours before a pathspec commit.
