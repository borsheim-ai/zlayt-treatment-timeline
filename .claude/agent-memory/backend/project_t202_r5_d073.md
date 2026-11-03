---
name: t202-r5-d073
description: T-202 r5 / D-073 conservative fallback - two date sources only, encounter_types.json is document-type words, prose never read, leader mask in amounts.py, corpus diff, mutant runner pitfalls
metadata:
  type: project
---

**Rule (r5, D-073):** `service_date.resolve` reads a charge date from (1) the date cell of the figure's own table row (>= 2 cells) under a heading matching `_H_SVC` (a bare From/To cell under a line naming service, e.g. `24A DATE(S) OF SERVICE`, takes that line's words in `_header_cells`; From+To cells pair into a period in `_from_to`, equal days = one day), or on a UB-04 coded line the `statement (covers) period` span; (2) the record's own date when `record_kind == "encounter"` AND every date unit in the figure's own segment (`AM._segments`) equals the record date AND `_MULTI` (plural visits/sessions, "to date", "visits 1-9", "N x") does not match. Everything else = blank. No prose label code remains (`_SVC_*`, `_LBL`, `_mark` deleted), so the staff r4b guard-word mutants cannot exist.

**encounter_types.json** now lists only document-type phrases (visit, note, progress note, ER/ED record, discharge summary, run report, operative report, evaluation, exam, consult, new patient, follow-up, mri ...). Provider/specialty words (clinic, ED, ER, urgent care, imaging, orthopedics, therapy, EMS, primary care) are NOT there; `encounter_abbreviations` key is gone. `record_kind` still lets financial/administrative words in source or excerpt opening veto. The 19 corpus lines on provider-only labels (Thornbury Regional ED, Quillfeather Urgent Care, Cobblestone Imaging ...) now print the blank; plus case_09 'visit of' and lib14 'run of' (3 lines). 22 of 37 distinct accepted charge lines changed; lib10 UB-04 period kept.

**Leaders:** `amounts.mask_leaders` + `@_masked` decorator on non_charge_reason/charge_basis/classify/charge_line/not_totaled_reason/not_counted; `_label` strips trailing middle dots (else "ER charges ......" never ends in "charges"). `service_date._mask_leaders` is the same helper.

**Pitfalls**
- Tests that pass the whole excerpt as the letter quote make letter_check see other sentences' dates; the real letter quotes the figure's sentence (`quote_of` in test_t202_r5_d073.py). A figure without cents ("$6,240") never matches letter_check's header regex: pass `_money`.
- Table fixtures need rec_date after the row date (a service cannot follow its statement): default 2026-06-15 blanked a 06/17 row.
- AS_WRITTEN (r3) written-date reasons now only come from DOS table cells; prose gives `non_service_date`.
- Mutant runner (scratchpad mut.py): rsync copy minus .git/.venv/artifacts/submission/reviews, run with the repo .venv python and cwd = copy; M-numbers in the handoff.
