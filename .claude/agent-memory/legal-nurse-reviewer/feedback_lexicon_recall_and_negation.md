---
name: lexicon-recall-and-negation
description: Lexicon/phrase-list reviews — selfchecks only test the sample and author examples; authors absorb reviewer probes into examples, so always add held-out probes (spinal levels, 'may be' hedges, 'attributes … to', since-year, post-accident follow-up wording)
metadata:
  type: feedback
---

When reviewing app/llm/lexicon.yaml (or any clinical phrase list), the author's selfcheck only proves the sample case and the author's own examples. Real-chart recall and negation-scope bugs show up only with independent probes.

**Why:** In T-009 r1 (commit f419c3b) the selfcheck passed, yet my probes found no hit for hx, s/p, PMH or prior surgery, and the negation guard crossed commas (two blockers). In T-009 r2 (commit 2fee2df) the author fixed exactly the probe sentences: 115 of the 140 round-1 probes became verbatim `examples`, and the selfcheck reported FP 0. On 40 held-out probes the lexicon scored 11/40. Causes:
- `(?:\w+\s+)` slots fail on spinal levels ("Prior C5-6 fusion").
- No "since 2019" branch.
- The hedge set lacks "may be degenerative".
- `attributes|relates` without a "to" connector.
- High-strength hits on "Previously seen on 01/16/2026" and "Chronic … secondary to the MVA".

The selfcheck also grades FIRE at any strength, so a low-only hit (which never raises a flag) passes.

**How to apply:**
- Reuse artifacts/review-evidence/T-009-r2-nurse-probe.py. It imports the selfcheck's scan(), so negation, year_filter and suppressors are included.
- Always write NEW held-out probes and grade them strictly (high/medium = raise).
- Count how many probe sentences appear in `examples`.
- Check categories against the ADR-013 closed list.
- Guard gaps with no observed wrong output are rated major (calibration). Golden must misses were the r1 blocker basis.
- Bash `sed -i` on review-evidence is blocked by board-guard. Use Edit.

Related: [[probe-must-not-regexes]]
