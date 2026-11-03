---
name: golden-set-recurring-findings
description: Patterns found reviewing evals/golden (T-015, 2026-11-01) to re-check on any later golden/eval change — must/should downgrades, leaky must_not regexes, missing tolerated flags
metadata:
  type: project
---

Recurring golden-set weaknesses found in the T-015 review (commit 47520a8, verdict fail):
- Appendix C "Expected flags (at minimum)" items got downgraded to `should` (K4 new onset after the 73-day gap, K5 wrong intake accident date). Under README scoring, `should` never counts as a miss, and cross-type credit isn't implemented. Re-check levels whenever golden files change.
- Explicit prior-condition mentions marked `should` (case_06 P2/P3), while the sample's different-region prior (P1) is `must`. Check that levels are consistent across cases.
- A credible adjuster attack with no golden or tolerated entry gets scored as a false positive (case_06 "denies prior neck problems" vs chiropractor history). Ask "what would the adjuster's letter quote?" and confirm each answer is must, should or tolerated.
- must_not regexes are only tested negatively (they must not match the input). Probe them with known-bad phrasings: the sample M9 regex missed "full recovery", and M2 missed "caused by the January collision" and "Degenerative findings".

Round 2 (commit 3c5eb7c) added these patterns:
- A level fix isn't enough. If two `must` flags share type and cite (K4/K5: causation, record 7) and matching is type+cite only, one candidate satisfies both. Simulate the README matching rule literally, and require evidence overlap plus one-to-one assignment.
- The byte-exact export golden (extracted from REQUIREMENTS §6) can drift from the golden JSON: a missing must-flag line, and evidence changes such as C1 "rear-ended" that should add a "flagged language" row. Rebuild each notes section from the JSON plus the R-EX-4 rules, and diff.
- Spec text (R-FL-4) can lag behind a golden change. Grep REQUIREMENTS for the old rule.

Round 3 (commit f8c1948, verdict fail) added these patterns:
- Schema key drift can silently disable a check. The JSON used `spans` while README and check_golden read `self_report_spans`, so the D-022 checks ran on empty lists and the validator stayed green. Count keys across all JSON files, and mutation-test every new assertion on a scratchpad copy (break the data, and the checker must exit 1).
- The writer fixes the line the reviewer named (the K5 line) and leaves the sibling lines that REQUIREMENTS §8 also listed (the C1 conflict bullet quoting both sides, the AI line). Byte-diff the golden against REQUIREMENTS §6 every round, and run the §8 reconciliation greps literally.
- Either-way substring overlap in the reference matcher lets a whole-record excerpt satisfy every golden flag on that record. Probe with whole-record and one-word candidates.

Round 4 (commit 0c03c4f, HEAD 65537a4, verdict changes) added these patterns:
- A fixed text can match one spec section and still break another. The golden AI line was made to match REQUIREMENTS section 6, but normative R-EX-4(1) keeps different text, and R-EX-4(1) contradicts R-EX-4(11). Diff the golden against every spec location that quotes the same text, not only the one the finding named.
- A prior review's quoted "spec text" can be wrong. The r3 paralegal quoted an R-EX-4(1) string that grep does not find in REQUIREMENTS.md. Grep every quoted spec string before relying on it.
- Key renames fix the data but can leave the checker's guard code stale. Mutation-test with the renamed key and with an objective span. The guard for unknown entry keys (ENTRY_KEYS in check_golden.py) is what makes the rename safe.

**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility.
**How to apply:** on any re-review of evals/golden or evals.run, re-run a probe like artifacts/review-evidence/T-015-paralegal-regex-probe.py and re-check the level of every Appendix C item. Related: [[reviewer-hook-constraints]]
