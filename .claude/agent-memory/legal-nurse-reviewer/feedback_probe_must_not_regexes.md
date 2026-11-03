---
name: probe-must-not-regexes
description: When reviewing golden/eval must_not regexes, probe them with faithful AND violating clinical phrasings plus chart abbreviations; also check good_examples are clinically faithful to the case record
metadata:
  type: feedback
---

Always run every clinical must_not regex against a fixture of faithful paraphrases (no/w/o/denies LOC, "could represent", adjuster-argument flag text) and real violations (lost consciousness, +LOC, DDD, "likely degenerative", "collision-related", left/right, other spinal level, mild->severe). Add chart abbreviations too (ESI, HNP, mTBI, s/p, "LOC x").

**Why:** T-015 r1 (2026-11-01): M6 was inverted and M2/M3 failed correct flag prose (both blockers). r2: the author's examples all passed, yet 30 of 50 of my new phrasings leaked. A regex good_example ("Patient states her neck pain is due to the collision") was itself unfaithful to the record ("began after"; the patient is 41M). An unless_context hedge window crossed commas, so an unrelated "could" exempted DDD.

**How to apply:** Reuse artifacts/review-evidence/T-015-r2-nurse-probe.py (`python3 -I`, check_golden semantics). Read every good_example against the actual case record, not just against the regex. Bash writes to the memory dir are blocked by board-guard; use the Write tool. Related: [[golden-entries-lack-summary-requirements]]
