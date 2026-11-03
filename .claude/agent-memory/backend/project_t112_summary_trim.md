---
name: t112-summary-trim
description: D-054 summary clause trimming (app/backend/summary_trim.py): rule, threshold, where it is wired, pitfalls found on real fixtures
metadata:
  type: project
---

`summary_trim.trim(summary, excerpt)` is called only from `generator.extract_one` (AI summaries, English records, quote verbatim in the record). A clause is removed only when it has content words and NONE has a stem / abbreviation-group match in the quote. Sides, negations, numbers, hedges and reporting words are stopwords (never support). Emptied -> `{"failure": "SUMMARY_NOT_IN_QUOTE", "detail": ...}` -> `failure_entry` tray placeholder (no pipeline error). Removal record: `ladder.summary_trim`; trace step `summary_trimmed`.

**Why:** case_02 live flap (model summarized past its own excerpt). **How to apply:** do not widen to human summaries (D-047 refuses those) or Spanish (stems cannot match a translation).

Pitfalls found by replaying all 181 fixture items: (1) abbreviations ('Denies LOC per patient' vs 'loss of consciousness') trimmed a faithful denial, so there is a negation guard (keep a clause with a negation word when the quote has one) and a generous synonym/abbreviation group table; add groups there, not exceptions. (2) Filler words ('now', 'seen', 'rated') must be stopwords or they make a clause look unsupported. (3) A trimmed summary changes the J1 prompt, so its fixture misses: run `python -m app.llm.record --fill-missing evals/library/<packet>.txt` for the packets where `ladder.summary_trim` appears in a fixture replay (2 of 181 items did). (4) HEAD can move during a full unit run (qa commits eval controls), producing transient test_t093_eval_signature failures; rerun.

**Round 2 (2026-11-02) replaced the rule.** The round-1 rule ("no content word matches the quote -> remove") over-trimmed faithful paraphrases (dizzy~dizziness, ambulating~walks) and left fragments. Now a clause is removed only when it adds SALIENT new content the quote lacks: a number/month, side, negation, or a word of a lexicon family (procedure/device/drug, body part, diagnosis noun; `_FAMILIES` in summary_trim.py, with `covered_by` for generic words like scan/meds/spine). Neutral clauses ('Initial consult') stay; the judge checks them. Capitalized mid-clause words are names (Fennimoor Spine Clinic), not body parts. The record label vouches for body part, side and imaging modality only (never treatment words). trim() takes label and date_iso. A fragment-making trim (kept clause starting with an article/preposition) is skipped entirely. Add a family, not an exception, when a faithful pair trims; tests: FAITHFUL (50 pairs) and UNSUPPORTED (28) in tests/unit/test_summary_trim.py.

Also in r2: review.not_duplicate now makes a failure_entry tray item for any extract failure (it used to drop the record with a false 'AI could not draft' warning); trace._entry_steps stops at the placeholder's failure code (no false 'not word for word'); evals/run.py reports `summary_trim_fired`. The `evals/` edit was explicitly authorized by the orchestrator for this card.
