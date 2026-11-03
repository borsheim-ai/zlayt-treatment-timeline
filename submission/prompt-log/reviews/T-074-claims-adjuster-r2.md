# T-074 round 2: claims-adjuster-reviewer (spec sync to D-040, commit 312ed92)

**Verdict: pass** (no blocker, no major). The round-1 major is closed: R-FL-7 in `spec/REQUIREMENTS.md:71` now states D-040, and `test_eval_spec_check` passes. Four minors from round 1 are still open in other spec and golden files; they are listed below as carried.

Model: claude-haiku-5-5 (the running model; the dossier's expected id does not match what is running).
Scope note: HEAD moved during the review (b9d3ead, then 43fc69e). I checked commit 312ed92 with `git show` and `git archive` into the scratchpad.

## What I checked

- **R-FL-7 closed (pass).** `spec/REQUIREMENTS.md:71` at 312ed92 reads "**No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion." Its acceptance cell is "No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes." The title matches `app/backend/flag_templates.py:126`.
- **Spec-check test (pass).** `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py` at the 312ed92 archive: 3 passed, exit 0.
- **Lines 280 and 291 still match the golden (pass).** `diff` of `sed -n 280p spec/REQUIREMENTS.md` against `sed -n 58p evals/golden/sample.export.expected.txt`, and 291 against 69, both identical at 312ed92.
- **Residue in spec, contracts, docs, golden (fails; carried minors).** See F1 to F3.
- **Cross-reference, not a T-074 finding.** R-FL-7's own acceptance cell ("No user-facing text contains self-report") is false at cab0068 because of `app/backend/narrative.py:19`. That is the T-072 r2 blocker, not a spec defect.

## Findings

- **F1 minor (carried from r1 F2). The case truth sheet still labels the record 9 quote.** `spec/SAMPLE_CASE_TRUTHS.md:9`: "(9 — patient self-report, not a physician's causation opinion)". Not rendered; it is the reference the team grades against. Owner: writer or orchestrator.
- **F2 minor (carried from r1 F3). Deviation row 4 is stale.** `spec/REQUIREMENTS.md:371` says the golden uses `source_kind: patient_self_report`. Its evidence command `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` returns nothing at 312ed92 (exit 1). A row that no longer reproduces misleads the next reviewer. Owner: orchestrator; close the row with a pointer to D-040.
- **F3 minor (carried from r1 F4). Contract example, design brief and golden K3 still show the cut label.** `memory/contracts/api.md:185-186` (title "Patient self-report", explanation "Patient self-report (not a physician's opinion) ..."), which contradicts that file's own D-040 note at line 212. `docs/UI_DESIGN_BRIEF.md:132` still lists a "Patient self-report" chip row. `evals/golden/sample.expected.json:625` (K3 summary) still says "Causation rests on patient self-report". Owners: backend (api.md), orchestrator (design brief), qa (golden).

## Reproduction

```
git show 312ed92 --stat                                     -> spec/REQUIREMENTS.md, 1 insertion, 1 deletion
git show 312ed92:spec/REQUIREMENTS.md | grep -n 'No speaker label (D-040'   -> 71
diff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 280p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 58p)  -> identical
diff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 291p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 69p)  -> identical
git archive 312ed92 | tar -x -C <scratchpad>/t074 && cd <scratchpad>/t074 && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py  -> 3 passed, exit 0
git grep -n -i 'self-report|patient_self_report' 312ed92 -- spec/ memory/contracts docs/ evals/golden -> residue at SAMPLE_CASE_TRUTHS.md:9, REQUIREMENTS.md:371, api.md:185-186, UI_DESIGN_BRIEF.md:132, sample.expected.json:625
```

## Not run

`evals.run` (writes `evals/reports`, outside my write paths), so the golden M10 check named in R-FL-7's acceptance cell was not re-run. `docs/CONTRACT.md:617` also carries "patient self-report"; CLAUDE.md marks that file as never edited, so it is listed as a question, not a finding.

```json
{"card": "T-074", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2; commit 312ed92 (spec/REQUIREMENTS.md R-FL-7) checked with git show and git archive into the scratchpad (t074); live HEAD moved during review (b9d3ead, then 43fc69e) and was not the verdict basis; sample case Appendix A",
 "exercised": [
  "read personas/claims-adjuster.md in full; reviews/T-074-claims-adjuster.md (r1); memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48)",
  "git show 312ed92 --stat; git show 312ed92 -- spec/REQUIREMENTS.md (1 insertion, 1 deletion, R-FL-7 only); git show 312ed92:spec/REQUIREMENTS.md | grep -n 'No speaker label (D-040' -> line 71",
  "diff of 312ed92 spec line 280 vs golden sample.export.expected.txt line 58, and line 291 vs line 69 -> both identical",
  "git archive 312ed92 | tar -x -C <scratchpad>/t074; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py -> 3 passed, exit 0",
  "git grep -n -i -E 'self-report|patient_self_report' 312ed92 -- spec/ memory/contracts docs/ evals/golden; git show 312ed92:spec/SAMPLE_CASE_TRUTHS.md (line 9); git show 312ed92:spec/REQUIREMENTS.md (line 371); git show 312ed92:memory/contracts/api.md (lines 185-186); git show 312ed92:docs/UI_DESIGN_BRIEF.md (line 132); git show 312ed92:evals/golden/sample.expected.json (line 625)",
  "git show 312ed92:evals/golden/README.md | grep -n 'patient_self_report|summary+excerpt' -> no output, exit 1",
  "read app/backend/flag_templates.py:126 (title 'Reported onset') to match R-FL-7 text",
  "not run: evals.run (writes evals/reports, outside write paths); golden M10 not re-run"
 ],
 "verdict": "pass",
 "scores": {"r_fl_7_states_d040": 5, "spec_lines_match_golden": 5, "spec_check_test_green": 5, "decision_residue_cleanup_spec_docs_golden": 2},
 "findings": [
  {"severity": "minor",
   "title": "Case truth sheet still labels the record 9 quote 'patient self-report' (carried from r1 F2)",
   "evidence": "spec/SAMPLE_CASE_TRUTHS.md:9 at 312ed92: \"Patient states symptoms began after the January collision\" (9 — patient self-report, not a physician's causation opinion)",
   "why_it_matters": "The truth sheet is the case reference the team grades against. It still records the speaker label D-040 cut. Not rendered anywhere.",
   "fix": "Writer or orchestrator: replace the parenthetical with the verbatim marker, e.g. (9 — verbatim 'Patient states ...').",
   "acceptance_test": "grep -n -i 'self-report' spec/SAMPLE_CASE_TRUTHS.md returns nothing."},
  {"severity": "minor",
   "title": "Deviation row 4 is stale: its evidence command returns nothing (carried from r1 F3)",
   "evidence": "spec/REQUIREMENTS.md:371 at 312ed92: | 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` ... | `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md` | orchestrator (D-entry) |. The command returns no output at 312ed92 (exit 1).",
   "why_it_matters": "A deviation row that no longer reproduces misleads the next reviewer about what is still open.",
   "fix": "Orchestrator: close the row with a pointer to D-040, or update it to the current golden state.",
   "acceptance_test": "The row's evidence command matches a current line, or the row is marked closed."},
  {"severity": "minor",
   "title": "Contract example, design brief and golden K3 still show the cut label (carried from r1 F4)",
   "evidence": "memory/contracts/api.md:185-186 at 312ed92 (title \"Patient self-report\"; explanation \"Patient self-report (not a physician's opinion) ...\"), while api.md's own D-040 note is at line 212. docs/UI_DESIGN_BRIEF.md:132: | `Patient self-report` | speech bubble | ... evals/golden/sample.expected.json:625: \"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\"",
   "why_it_matters": "Builders following these documents would rebuild the cut chip and the cut speaker wording. api.md contradicts its own decision note.",
   "fix": "Backend: update api.md:185-186 to the neutral title and explanation. Orchestrator: mark the design-brief row as cut under D-040. QA: replace the K3 summary with a neutral verbatim line.",
   "acceptance_test": "grep -rn 'Patient self-report' memory/contracts docs/ evals/golden returns no hits outside decision history and the M10 must_not statement."}
 ],
 "whats_right": [
  "R-FL-7 at spec/REQUIREMENTS.md:71 now states the D-040 rule, names the neutral 'Reported onset' title that flag_templates.py:126 produces, and keeps the M10 must_not check.",
  "Spec lines 280 and 291 are byte-identical to golden lines 58 and 69 at 312ed92, and test_eval_spec_check passes (3 passed).",
  "The commit is one line in one file, so the spec change is reviewable on its own."
 ],
 "questions_for_chris": [
  "docs/CONTRACT.md:617 carries 'patient self-report' in the case truth copy, and CLAUDE.md says that file is never edited. Should the team record that copy as a known residue in SCOPE_CUTS, or is there a sanctioned way to correct it?"
 ]}
```
