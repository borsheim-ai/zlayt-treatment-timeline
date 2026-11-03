---
name: spec-review-patterns
description: Recurring defects found in Zlayt PM requirements/spec reviews (T-013 r1-r3) — rules/claims contradicted by the doc's own example, names that don't exist, unreconciled newer D-IDs
metadata:
  type: feedback
---

Before grading a requirements doc, mechanically check (1) every absolute claim against the doc's OWN worked example, and (2) every named artifact it keys on (lexicon category, R-ID, golden file, reason code) actually exists.

**Why:** T-013 r2: R-EX-1 said "No flag text of any kind" in the letter, yet 8 of 10 golden flag evidence strings sat verbatim in its §6 letter example; its test only listed strings that happened to pass. R-TL-8 keyed on a lexicon `hedge` category that doesn't exist (lexicon flag_types are pre_existing/causation_weakening/compliance). r1 had R-TL-4 citing a nonexistent R-QA-2. Writers fix the reviewer's wording and leave the test narrower than the claim.

T-013 r3 (b4f3924) showed the same pattern again. The R-EX-4(4) rule computed records {1,4,6,7,8,9}, but the example, the test and the golden file said {4,6,7,8,9}. Two more checks would have caught issues sooner:
- Check the doc's header list of binding decisions against the latest D-ID. It cited D-001..D-015, while D-016..D-018 existed and D-017 went unreconciled.
- Run my OWN previous acceptance tests literally. The r2 money regex fails on verbatim "$6,240." quotes.

Golden export files are copied from the spec example, so any contradiction in the example gets frozen into the golden file.

**How to apply:** Implement each stated rule in the walk script and compare its output with the example (don't just check the example's strings). Write a script under artifacts/review-evidence/ that extracts the example blocks and compares them with evals/golden/sample.expected.json (flag evidence, quotes, providers, dates); grep each referenced name. Also judge the export as a demand-letter paste: tool-authored text in the carrier block (e.g. "visit count not stated") is adjuster ammunition even when the reviewer asked for the disclosure. See [[reviewer-tooling-quirks]].
