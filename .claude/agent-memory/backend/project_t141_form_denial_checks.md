---
name: t141-form-denial-and-checks
description: T-141 form-field denials ("Prior accidents? Yes [ ] No [X]"), accident-date corroboration rule, GET case `checks` (T-142)
metadata:
  type: project
---

- `conflict_candidates._denial_units`: besides the `_DENIAL` phrases, a stem unit ("Prior accidents?") plus the next unit ("Yes [ ] No [X].", OCR "No IX]") is one contiguous quote; splitter cuts after '?'. Yes-checked / no box / stem alone is not a denial. A form stem about accidents pairs only with accident sentences (`_ACCIDENT_STEM`), not problem-list lines.
- Prior accident named only by year ("car accidents in 2019 and 2022") counts when year < the denial record's year (`_earlier_year_accident`; no date on the denial record = not counted). The lexicon scan (not mine) fires pre_existing even on "Rear-end collision in 2026." when no case context, so don't test absence with it.
- `conflicts.accident_date_conflicts`: a single stated date later than the first record is NOT a conflict when another record is dated that day AND no earlier record describes a collision/accident that is not history (`_corroborated`). Two different stated dates still conflict.
- `conflict_candidates.checks()` -> present.case_view `checks`; documented in memory/contracts/api.md. Row 11 of LLM_VS_CODE (architect) and SCOPE_CUTS need a matching sentence from their owners.
- Candidate set diff across golden+library packets before/after: only lib11 gained pairs, so no existing J3 control text changed (no live re-run needed). Compare with `git show HEAD:...conflict_candidates.py` loaded as a scratch module.
