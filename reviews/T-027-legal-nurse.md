# T-027 legal-nurse review (Linda Chen, RN) — Lexicon generalization, commit 8b7dc17

Verdict: **pass** (minors only). Fresh 25 reviewer probes (written after reading only the first 5 held-out rows; none are in the worker's file): **21/25 = 84%** under strict grading (high/medium raises), above the 80% bar. Golden MUST 11/11, SHOULD 1/1, must_not 0. Worker's own held-out 90/90, no leak. All 5 post-accident false-alarm traps and the negation trap stayed quiet; the no-hedge MRI impression raised no hedge.

Fresh misses (evidence file: artifacts/review-evidence/T-027-nurse-fresh.txt; script T-027-nurse-fresh-probe.py):
- "Patient states the pain started when the other vehicle struck her from behind." -> only patient_reports_generic[low]; "when ... struck" is not an attribution connector.
- "Patient feels her symptoms are a result of the collision." -> no hit at all.
- "Patient was treated for neck pain by a chiropractor from 2019 to 2020." -> no hit.
- "Remote T11-12 vertebroplasty; no current complaints." -> no hit.
These are recall gaps, not wrong output (nothing was inferred or upgraded), so minor. Attribution scored 2/4 fresh versus 12/12 on the worker's tuned set, so the worker's group figures overstate recall.

Label note: ADR-013 category `objective_negative` is the tool's own "objective" word. It is acceptable as an internal key, but it must not reach the UI or export (persona checklist item 7).
Scope: lexicon recall only. Prompts, UI and summaries are outside this card.

```json
{"card": "T-027", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 8b7dc17: app/llm/lexicon.yaml, research/lexicon_selfcheck.py, evals/lexicon_heldout.jsonl; 25 fresh reviewer probes; golden cases",
 "exercised": [
  ".venv/bin/python research/lexicon_selfcheck.py -> golden MUST 11/11, SHOULD 1/1, must_not 0, probes FP 0 FN 1 of 140, held-out 90/90, RESULT: PASS",
  "python3 tools/board.py show T-027 (AC and handoff read)",
  ".venv/bin/python -I artifacts/review-evidence/T-027-nurse-fresh-probe.py: 25 fresh probes scored with selfcheck scan() -> 21/25 = 84% (PRE 8/10, HEDGE 5/5, ATTR 2/4, QUIET_PRE 5/5, QUIET_HEDGE 1/1); output at artifacts/review-evidence/T-027-nurse-fresh.txt",
  "read research/lexicon_selfcheck.py header, held-out runner and leak check; read lexicon entries prior_treatment_terms, pmh_psh_spine, patient_attributes_causation; read memory/DECISIONS.md:250-258 ADR-013 category list"
 ],
 "verdict": "pass",
 "scores": {"held_out_recall_fresh": 4, "golden_must_flags": 5, "post_accident_false_alarms": 5, "hedge_preservation": 5, "patient_attribution_recall": 3, "category_names_adr013": 4},
 "findings": [
  {"severity": "minor",
   "title": "Patient-attributed causation recall is 2/4 on fresh phrasings",
   "evidence": "T-027-nurse-fresh.txt: 'Patient states the pain started when the other vehicle struck her from behind.' -> patient_reports_generic[low/causation] only; 'Patient feels her symptoms are a result of the collision.' -> '-'. Worker group result: attribution 12/12 (tuned set).",
   "why_it_matters": "Checklist item 8: patient-stated causation must be surfaced as self-report, not silently dropped. A miss means the attorney is not told the causation claim is the patient's.",
   "fix": "Widen the connector set in patient_attributes_causation to include 'when ... struck/hit/rear-ended', 'result of', 'secondary to', 'ever since'; keep the self_report flag so it stays attributed to the patient.",
   "acceptance_test": "Both sentences above raise patient_attributes_causation at high/medium; the quiet post-accident probes still raise no pre_existing."},
  {"severity": "minor",
   "title": "Prior treatment given as a year range, and 'Remote <level> <procedure>' with no year, are not flagged",
   "evidence": "T-027-nurse-fresh.txt: 'Patient was treated for neck pain by a chiropractor from 2019 to 2020.' -> '-'; 'Remote T11-12 vertebroplasty; no current complaints.' -> '-'.",
   "why_it_matters": "Checklist item 9: prior history must be flagged as prior history. These forms are common in intake notes.",
   "fix": "Add a 'treated ... (for|by) ... from <year> to <year>' branch (year-filtered like the others) and let remote/past/old precede a spinal level plus a spine procedure noun (vertebroplasty, kyphoplasty, fusion, laminectomy).",
   "acceptance_test": "Both sentences raise pre_existing at high/medium; 'Chiropractic care from 03/20/2026 to 05/01/2026' stays quiet."},
  {"severity": "minor",
   "title": "ADR-013 category 'objective_negative' puts the tool's own 'objective' label in a user-reachable vocabulary",
   "evidence": "memory/DECISIONS.md:255 'objective_negative (no objective findings, normal exam, WNL/full ROM)'; worker handoff says names are used as written.",
   "why_it_matters": "Checklist item 7 and dealbreaker 3: the tool must not add its own subjective/objective labels. As an internal key this is fine; displayed text would not be.",
   "fix": "Confirm the category key is never rendered, and that UI and export use the template text and the verbatim quote only. Alternatively rename it to `normal_exam_language`.",
   "acceptance_test": "grep of UI templates and export for 'objective' and 'subjective' returns no tool-authored label."}
 ],
 "whats_right": [
  "Post-accident wording ('sustained in the 03/14/2026 collision', 'Previous MRI of 05/29/2026', 'Prior to today's visit') stayed quiet 5/5 via the year filter; the negation trap also stayed quiet.",
  "Hedges ('cannot exclude', 'possibly ... versus', 'indeterminate', 'likely age-related') were caught 5/5 on unseen phrasings, and a plain MRI impression raised no hedge.",
  "Selfcheck now fails on example/held-out overlap, grades strictly, and golden MUST is 11/11."
 ],
 "questions_for_chris": []}
```
