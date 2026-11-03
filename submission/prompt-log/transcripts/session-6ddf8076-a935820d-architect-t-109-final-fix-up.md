# Subagent: Architect: T-109 final fix-up (Architect: T-109 final fix-up)

Source: `agent-a935820d1c89bd13d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T12:25:37.568Z

You are the architect in /Users/arsis/zlayt-pm-project. This is the T-109 final fix-up after review round 3; read reviews/T-109-staff-engineer-r3.md. The orchestrator has already marked D-004, D-031 and SCOPE_CUTS row 15 as superseded.

Fix in docs/LLM_VS_CODE.md:
1. **Major:** row 11 claims J3 controls include dosage and laterality pairs. They were removed in T-093 r4 (822ff38). State what evals/j3_controls.py actually contains now, with the correct citation.
2. **Row 4 and ADR-020 item 5 (memory/DECISIONS.md):** describe the suffix-only trim from b348221. Only trailing clauses are removed, the kept text is a prefix of whole clauses, and it needs at least 2 content words. Fix the cited line range.

Minor 7 (the test name and docstring rename) is not yours; I'll file it.

Verify every claim against HEAD code. Commit with a pathspec: run `git add <paths>`, then `git commit -m msg -- <paths>` as a separate command. Write the handoff and move T-109 to in_review (claim it again with --force if needed). Reply in 2 lines.

### User / tool · 2026-11-02T12:25:37.574Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:40.422Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -5; cat reviews/T-109-staff-engineer-r3.md | head -80; grep -n \"J3\\|j3\" docs/LLM_VS_CODE.md | head -20; grep -n \"trim\\|suffix\\|prefix\" docs/LLM_VS_CODE.md memory/DECISIONS.md | head -20"
}
````

### User / tool · 2026-11-02T12:25:40.549Z

**tool result**
````
bd8c50e docs(orchestrator): mark D-004, D-031 and scope cut 15 superseded by D-042/D-052 (T-109 r3)
b348221 fix(backend): T-128 r3 trim only a suffix, n't contraction and quote-side tests
c759213 fix(backend): T-132 r2 wrapped attribution phrase, chained attribution clauses, no extension across blank line or section header
b612176 feat(frontend): T-060 r5 + T-131 - dismissed items keep no Accept, edited-needs-review counts as open, focus stays in one list, one need-review count, plain reasons, long dates, Filtered by rule, one-line letter control
1218b2e chore(evals): regenerate calibration.json from a clean worktree of e79c3aa (fixture; lexicon.yaml T-133)
# T-109 round-3 review (staff-engineer-reviewer), docs commits f8bb674 and a27e1d7

Scope: `docs/LLM_VS_CODE.md` rows 4, 11, 12, 13 (header D-057), `memory/DECISIONS.md` ADR-015, 019, 020, and the six round-2 minors. Code read through `git archive` of two pins: `94a135b` (HEAD when I started; scratchpad `t109r3_pin`) and `b348221` (HEAD at the end; scratchpad `t109r3_head`). HEAD moved twice during the review: `dab3037` (docs only, D-053 text) and `b348221` (T-128 r3, trim is suffix-only; also T-132 r2 `lexicon_scan.py` and T-131 frontend). The doc file itself is identical at 94a135b and b348221 (`git diff --stat 94a135b HEAD -- docs/LLM_VS_CODE.md` is empty). Backend files cited by rows 11, 12 and 13 are unchanged between the two pins except `lexicon_scan.py`; I re-ran the probes on the b348221 archive.

Verdict: changes. No blocker. The round-2 blocker (model-proposed conflict dropped in `run_flag_pass`) is closed in code, and rows 11, 12 and 13 match the tray routes line by line. One major remains: row 11 tells the reader the J3 eval controls measure dosage and laterality pairs, and they do not (they were removed in T-093 r4). Row 4 matched the trim at 94a135b and now needs a sync to T-128 r3 (flagged as a sync item, not the reason for this verdict).

Round-2 status:
- Blocker (model conflicts dropped): closed. `flags.py:252-254` splits proposed flags into per-record types and conflicts; `flags.py:265` adds `_model_conflicts(...)`; probe through the producer `run_flag_pass` returns one conflict, state `rejected`, reasons `['LLM_ONLY']`. Tests go through `run_flag_pass` (`tests/unit/test_flags_pass.py:370`, `:387`). Mutant A (route removed) fails 5 tests.
- Minor 2 (D-053 wider than ADR-020): closed. `memory/ORCHESTRATOR_DECISIONS.md:61` (dab3037) now says "a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020)"; ADR-020 item 2 mirrors it.
- Minor 3 (balance due, Spanish wording): closed. ADR-020 item 3 says the balance cue always refuses "balance due" and lists cargo, cargos, honorarios, consultas (`reclassify.py:29`, `amounts.py:43-46`).
- Minor 4 ('not yet committed', SUMMARY_NOT_IN_QUOTE): closed. No "not yet committed" in docs or DECISIONS; `why.py:33` has the template.
- Minor 5 (uncommitted reports): closed. `git cat-file -e HEAD:evals/reports/20261102T083252Z.md` and `...T085207Z.md` succeed, each has `ship_bar_met: True`.
- Minor 6 (stale cut text): half closed. ADR-015 status and consequences are amended. D-004, D-031 and SCOPE_CUTS row 15 still carry the old sentence with no mark (finding 3).
- Minor 7 (test name, docstring): still open, third round (finding 4).

Key evidence (reproducible with `/Users/arsis/zlayt-pm-project/.venv/bin/python -I` on the scratch archives):
- Routing probe (`run_flag_pass` then `judge_flags`, fake call), identical on both pins: model conflict gives rejected/LLM_ONLY; model-only causation with J4 disagree gives rejected `['JUDGE_DISAGREES','LLM_ONLY']`, unsure gives needs_review `JUDGE_UNSURE`, agree gives needs_review `LLM_ONLY`, fixture miss gives needs_review `JUDGE_UNAVAILABLE`; phrase-list-plus-model flag with J4 disagree stays needs_review `JUDGE_DISAGREES` (origin both); lexicon-only has no judge; `objective_negative` proposal gives rejected `FILTERED_BY_RULE`; model-only `scene_facts` gives rejected `LLM_ONLY`. All match rows 11, 12, 13.
- Candidate probe (b348221): "twice-weekly for six weeks" gives arithmetic 12 visits; intake-form plan ignored; intake-form denial still compared; relative's sentence and the neighbouring semicolon clause not paired.
- Trim probes: all structural claims in row 4 hold at 94a135b. At b348221 `'Wrist pain 6/10; splint fitted; patient tolerated well.'` is returned unchanged (at 94a135b it became `'Wrist pain 6/10; patient tolerated well.'`).
- Mutants on the 94a135b copy over test_summary_trim, test_conflict_candidates, test_t126_filtered_by_rule, test_flags_pass, test_pipeline (411 tests, all pass unmutated): A model-conflict route off, 5 failed; B filtered-by-rule branch off, 8 failed; C J3 benign-to-tray off, 4 failed; D denial `_other_person` off, 1 failed; E paperwork test off, 1 failed; F `store.py:69` tray-flag exclusion off, 2 failed; H kept-prefix rule off, 3 failed; I comma/and/with rule off, 2 failed; J empty-trim-to-tray off, 4 failed. G (`if drop[0]` off) passed all 411: equivalent, see nit.
- Unit suite at b348221: 3289 passed, 4 skipped.

```json
{"card": "T-109", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "docs/LLM_VS_CODE.md rows 4, 11, 12, 13 and memory/DECISIONS.md ADR-015/019/020 at f8bb674 and a27e1d7, checked against code at 94a135b (git archive, t109r3_pin) and b348221 (git archive, t109r3_head; HEAD moved via dab3037 docs-only and b348221 T-128 r3 during the review); docs/LLM_VS_CODE.md identical at both; no app URL (docs review); sample case not run through the CLI (outside this card's rows)",
 "exercised": [
  "python3 tools/board.py show T-109; git rev-parse HEAD, git log, git diff --stat 94a135b dab3037 b348221 (HEAD moved 94a135b -> dab3037 -> b348221)",
  "git archive 94a135b and b348221 into scratchpad t109r3_pin and t109r3_head; read docs/LLM_VS_CODE.md lines 1-50 in full; memory/ORCHESTRATOR_DECISIONS.md D-004, D-031, D-042, D-053 to D-057; memory/DECISIONS.md ADR-015 and 019/020 (lines 303-306, 356-368); memory/SCOPE_CUTS.md rows 13 and 15; reviews/T-109-staff-engineer-r2.md",
  "read code at the pins: app/backend/summary_trim.py (1-40, 100-125, 205-275, 315-440); generator.py 40-95 and 141-155; why.py 28-38; flags.py 100-385 (merge, _model_conflicts, run_flag_pass, run_conflict_pass, _judge_one, _to_tray, judge_flags); conflict_candidates.py 1-185; present.py 262-345; store.py 60-75; judges.py 40-66; schemas.py 41-57; flag_templates.py 219-226; reclassify.py 1-31; amounts.py 40-48; language.py EN_CONFIDENT/EN_DOMINANT/is_translated; trace.py summary_trim notes; evals/j3_controls.py 1-20 and the control rows; evals/golden/judge_controls.CHANGELOG.md; app/llm/prompts/judge_conflict_v6.md rule 2",
  "opened every file:line cited in rows 4, 11, 12, 13 and ADR-020 items 1, 2, 3, 5, 6 and compared with the code (summary_trim.py:108, 212-267, 269, 325-356, 338-342, 391, 414-424; generator.py:70-79, 75-77; why.py:33; conflict_candidates.py:73-83, 98, 101, 133-148, 138, 151-175, 155, 166, 169; judges.py:59, 64; flags.py:126-131, 173-174, 176-180, 187-212, 265, 349-352, 381-383; present.py:290-300, 298-307; store.py:69; flag_templates.py:219; test names in test_summary_trim.py, test_conflict_candidates.py, test_t126_filtered_by_rule.py)",
  ".venv/bin/python -I probes (stdin or scratch files): summary_trim.trim on 16 summary/excerpt pairs at both pins; run_flag_pass plus judge_flags routing probe (11 cases) at both pins; conflict_candidates.candidates on a 5-record set at b348221",
  "pytest (scratch archives, -p no:cacheprovider): test_summary_trim, test_conflict_candidates, test_t126_filtered_by_rule, test_flags_pass, test_pipeline: 411 passed at 94a135b, 435 passed at b348221; tests/unit full at b348221: 3289 passed, 4 skipped (180s)",
  "mutants A, B, C, D, E, F, G, H, I, J on scratch copies of the 94a135b archive (script t109r3_mutate.py): 5, 8, 4, 1, 1, 2, 0, 3, 2, 4 failures",
  "git cat-file -e HEAD:evals/reports/20261102T083252Z.md, ...T085207Z.md (present), ...T060623Z.md, ...T062420Z.md (absent, no longer cited); grep -c 'ship_bar_met: True' on the two reports; grep for 'rate can never become', 'rate must never become', 'not yet committed', 'dosage and laterality' across docs and memory; git grep for the test name and docstring 'agree' at HEAD; board list grep for a card owning the rename"],
 "verdict": "changes",
 "scores": {"claims_match_code": 4, "decisions_consistency": 4, "tests_backing_claims": 4, "fail_safe_and_binding": 5, "honest_limits_disclosed": 3},
 "findings": [
  {"severity": "major",
   "title": "Row 11 says the J3 eval controls include dosage and laterality pairs; they do not, and the cited test file has none",
   "evidence": "docs/LLM_VS_CODE.md:39 (row 11): 'The J3 eval controls include dosage and laterality pairs (`tests/unit/test_t093_eval_signature.py`), so the model's answer on them is measured; no code rule proposes them.' Counter-evidence at 94a135b and b348221: evals/j3_controls.py:3-4 'The first J3 controls were hand-written pairs (laterality, dates, doses, pain scores). conflict_candidates.candidates() never proposes those, so the gate measured a path the product does not have.'; evals/golden/judge_controls.CHANGELOG.md:27 'Removed (not relabelled), because the generator does not propose them ... Laterality, date, dose and pain conflicts are not flagged by the product at all (memory/SCOPE_CUTS.md), so a judge gate on them would test a path that does not exist.'; commit 822ff38 (T-093 r4, after the 4bdf366 version of the row). Repro: grep -n -i 'dose\\|dosage\\|laterality' tests/unit/test_t093_eval_signature.py returns nothing; grep -n -i 'mg\\|left.*right\\|right.*left' evals/j3_controls.py returns nothing; the two left/right-looking controls (J3V7, H3V9) are denial-vs-different-body-part pairs, not laterality conflicts.",
   "why_it_matters": "The graded table claims a measurement that is not made. A reader who checks the cited file finds nothing, and the claim reverses the eval history (the dosage and laterality controls were removed because they tested an unreachable path). Dosage and laterality are not raised by the product and not measured by the eval; the row should say that, which is the honest limit.",
   "fix": "Architect: replace the sentence in row 11 with: 'Dosage and laterality pairs are neither proposed by code nor measured: the J3 controls are built only from pairs the code proposes (evals/j3_controls.py, T-093 r4), and the earlier dose and laterality controls were removed for that reason.' Cite evals/j3_controls.py instead of the unit test.",
   "acceptance_test": "grep -n 'include dosage and laterality pairs' docs/LLM_VS_CODE.md returns nothing; row 11 names evals/j3_controls.py and says dosage and laterality are not measured; every file path cited in the sentence contains the claimed content (grep for it)."},
  {"severity": "minor",
   "title": "Row 4 and ADR-020 item 5 describe the trim before T-128 r3; at b348221 the trim is suffix-only (SYNC NEEDED, not a failure of this card)",
   "evidence": "docs/LLM_VS_CODE.md:32 (row 4): 'the first clause is never removed ...; the kept prefix, the clauses before the first removal, needs at least 2 content words; a clause joined to a removed one by a comma, 'and' or 'with' is not left behind (`:414-424`)'; memory/DECISIONS.md:367 (ADR-020 item 5) says the same. Code at b348221 (commit b348221, summary_trim.py docstring line 26 and code 417-422): '(1) trim only a SUFFIX (T-128 r3): ... a clause is removed only when every clause after it is removed too'; the comma/and/with arm was deleted. Probe: trim('Wrist pain 6/10; splint fitted; patient tolerated well.', 'Wrist pain 6/10.') returns the summary unchanged at b348221 and 'Wrist pain 6/10; patient tolerated well.' at 94a135b. At 94a135b every row 4 claim held (probes, mutants H and I fail 3 and 2 tests; cited test names exist at b348221 as well: tests/unit/test_summary_trim.py:162, 635, 646, and a renamed special case at :656). The other row 4 cites are unchanged at b348221 (summary_trim.py:108, 212-267, 269, 325-356, 338-342, 391, 414).",
   "why_it_matters": "At HEAD the table no longer says that a middle clause is never cut: the rule that governs what the paralegal sees in the summary changed, and the doc and ADR still describe the old rule. This is expected drift from a card that landed after the doc commit, so I do not hold T-109 on it, but the next doc edit must carry it.",
   "fix": "Architect (after T-128 r3 is accepted): in row 4 and ADR-020 item 5 replace the comma/'and'/'with' sentence with 'code trims only a suffix: a clause is removed only when every clause after it is also removed (T-128 r3); otherwise the summary goes to judge 1 unchanged', keep the first-clause and two-content-word rules, and update the line range (the structural block is now 417-422).",
   "acceptance_test": "grep -n 'not left behind' docs/LLM_VS_CODE.md memory/DECISIONS.md returns nothing; row 4 contains the word 'suffix'; the cited range 417-422 (or the then-current range) contains the first-clause, suffix and prefix checks."},
  {"severity": "minor",
   "title": "Carry-over from round 2 (half done): D-004, D-031 and SCOPE_CUTS row 15 still say a rate can never become a charge / reclassification is cut, with no superseded mark",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:12 D-004 'a rate can never become a charge'; :39 D-031 'Still cut, with reason: charge reclassification (a rate must never become a charge — safety)'; memory/SCOPE_CUTS.md:19 row 15 'A rate must never become a totaled charge; accept/dismiss is enough.'. D-042 (ORCHESTRATOR_DECISIONS.md:50) reinstates it as guarded reclassification. grep -n 'superseded' memory/ORCHESTRATOR_DECISIONS.md returns nothing. ADR-015 is fixed (status line 304 and consequences line 306).",
   "why_it_matters": "A reader starting from D-004, D-031 or the scope-cut list gets the claim that row 7 no longer makes. These files are orchestrator-owned, so the architect could not close this part.",
   "fix": "Orchestrator: append 'superseded by D-042 (guarded reclassification; ADR-020)' to D-004 and D-031 and to SCOPE_CUTS row 15 (or move row 15 to the reinstated list).",
   "acceptance_test": "grep -n 'rate can never become\\|rate must never become\\|Still cut, with reason: charge reclassification' memory/*.md returns only lines that also carry 'superseded'."},
  {"severity": "minor",
   "title": "Carry-over (third round): test name and docstring still say plans 'agree', no card owns the rename",
   "evidence": "git grep at HEAD b348221: tests/unit/test_conflict_candidates.py:33 'def test_frequency_times_duration_is_arithmetic_and_agrees_with_the_visit_count'; app/backend/conflict_candidates.py:8 'so it agrees with \"Plan of care: 12 visits\" and is never a conflict. Plans that agree make one plan (the explicit visit count is quoted).' Row 11 says correctly that no numeric comparison is made. python3 tools/board.py list shows no card for the rename (open cards T-113 in_review, T-134 in_progress are unrelated). The architect note says it is 'not architect-owned; still open for backend/qa'.",
   "why_it_matters": "The name and docstring claim an agreement check that does not exist; row 11 had to carry a sentence to contradict them. Left unowned it will survive a fourth round.",
   "fix": "Orchestrator: open a card for backend (code docstring) and qa (test name), or fold it into T-113 r2. Rename to '..._is_arithmetic_and_makes_one_plan_quoting_the_visit_count' and reword the docstring to 'the explicit visit count is the plan quoted; nothing is compared'.",
   "acceptance_test": "git grep -n 'agrees_with_the_visit_count\\|Plans that agree' returns nothing; the renamed test still passes."},
  {"severity": "nit",
   "title": "Line cites in row 11 are slightly wider than the code; one arm of the first-clause rule is unreachable on its own",
   "evidence": "docs/LLM_VS_CODE.md:39 cites `_model_conflicts` as flags.py:187-212; the function is 187-209 (line 212 is `def ground`). It cites `judge_flags` :381-383 beside `_model_conflicts` as if both were routes, but run_flag_pass already moves the item to the tray and judge_flags skips rejected items at :379, so :381-383 is a backstop for a conflict handed in directly (the only caller is the test at tests/unit/test_pipeline.py:248). Mutant G (summary_trim.py `if drop[0]:` disabled) passes all 411 tests: with the first clause removed the kept prefix is empty and the 2-content-word rule returns the summary unchanged anyway, so the first-clause rule is behaviourally true but redundant.",
   "why_it_matters": "Cosmetic, but a reader tracing the tray route will look for a second route that the pipeline does not use.",
   "fix": "Architect: write 'flags.py:187-209' and 'backstop in judge_flags, :381-383'. Optionally state that the first-clause rule is implied by the prefix rule.",
   "acceptance_test": "The cited ranges contain exactly the named functions."}
 ],
 "whats_right": [
  "The round-2 blocker is fixed at the producer: run_flag_pass sends a model conflict to the tray (rejected, LLM_ONLY), two tests drive it through run_flag_pass and the case payload, and removing the route fails 5 tests",
  "Rows 12 and 13 match the tray and filter routes exactly (J4 disagree to tray only for model-only flags, both-origin stays needs_review, objective_negative listed under Filtered by rule, tray flags excluded from counts, gate and export); mutants B and F fail 8 and 2 tests",
  "Row 4's structural claims were each probed true at 94a135b and the cited tests exist; row 11's candidate drop rules (different person, semicolon clause, intake form as plan or outcome, intake denial still compared) match conflict_candidates.py and a fresh probe"
 ],
 "questions_for_chris": []}
```
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only classifies.** `app/backend/conflict_candidates.py` pairs two whole sentences by two fixed rules: **plan vs early end** (a stated plan, as a visit count or frequency × duration, against a LATER record showing a missed, no-show, cancelled, self-discharged or discontinued course; `plan_vs_outcome`, `:133-148`) and **denial vs prior history** (a sentence denying prior problems, against a sentence in another record that the phrase list marks as a prior condition or prior surgery, or that names an earlier accident or claim; `history_denials`, `:151-175`). **The rules drop pairs before any model sees them:** (1) *different person:* a sentence whose subject is a relative or another party from a closed list (the other driver, a witness, mother, husband, "family history") and that does not name the patient is never half of a candidate, on either side (`_other_person`, `:73-76`, applied at `:101`, `:138`, `:155`, `:166`, `:169`); a person the list does not name still reaches the judge, whose prompt is the backstop. (2) *across a semicolon:* the subject is read inside the sentence's own semicolon clause (the splitter cuts at ';'), so a relative named in the neighbouring clause neither hides the patient's own history nor is paired with it (`tests/unit/test_conflict_candidates.py::test_the_subject_is_read_inside_its_own_semicolon_clause`). (3) *intake forms:* a paperwork record (intake form, bill, affidavit, by the header test `gaps.admin_label`) is never the plan or the outcome of a course (`:79-83`, `:98`, `:138`; `::test_an_intake_form_is_never_the_plan_or_the_outcome_of_a_course`); a denial written on an intake form is still the patient's own statement and is compared. Code multiplies frequency × duration into visits ("2x/week for 6 weeks" = 12) and carries that arithmetic on the flag. An explicit visit count is the plan quoted when one exists. No numeric comparison is made between a count and a frequency plan, so the two are not checked against each other. Candidates come in a fixed order, so the set cannot vary between runs: there is no open-ended model search (`conflicts_v1` is retired). The model is `judge_conflict_v6` (J3; `judges.py:59`), and it only classifies each candidate as `conflict`, `benign` or `unsure`, with a fixed reason code and no prose. It never proposes a pair, a quote or a number. **Nothing the model produces is silently dropped (D-053):** a code-proposed pair that J3 calls `benign` goes to the could-not-verify tray (tray kind `flag`, reason `JUDGE_DISAGREES`, with the judge's fixed reason); a model-only flag that the flag judge (J4, `judge_flag_v3`, `judges.py:64`) calls `disagree` goes to the tray the same way (`flags.py:349-352`; `present.py:290-300`); a conflict the model proposed in the per-record pass, which no code candidate made, goes to the tray with `LLM_ONLY` and is not judged (`_model_conflicts`, `flags.py:187-212`, called at `:265`; `judge_flags`, `:381-383`). The tray-on-no-candidate rule is for conflicts only: a model-only flag that J4 does not reject stays `needs_review` (`LLM_ONLY`), and a flag the phrase list also found stays `needs_review` even if J4 disagrees. Tray items are never flags and never reach the letter. A J3 or J4 `unsure` answer, or a judge that did not answer, keeps the flag visible as `needs_review`. **Candidate rules** also cover number-word visit counts with a plan cue, frequency × duration in weeks (including "twice-weekly for six weeks"), lost to follow-up, stopped or left care, negation- and completion-aware, and denials of earlier accidents or claims. **Not built as candidates:** dosage and laterality pairs (laterality is checked only within one summary, row 15), and month durations (`memory/SCOPE_CUTS.md`, row 13). The J3 eval controls include dosage and laterality pairs (`tests/unit/test_t093_eval_signature.py`), so the model's answer on them is measured; no code rule proposes them. | Reading comprehension is needed only for one yes or no per pair. An open-ended search let the model call "2x/week for 6 weeks" against "12 visits" a conflict (T-094, live run 2). The arithmetic and the choice of pairs are code's. | **Rung 1:** both quotes are whole sentences cut from the record text, and grounding still checks them. **Rung 2, J3:** `conflict` gives a flag (verified only when the other checks hold); `unsure` keeps it `needs_review`; `benign` on a code-proposed pair moves it to the could-not-verify tray, never exported. A denial is judged one candidate at a time, in record order, and the first confirmed conflict stands. **Rung 3:** human accept or dismiss. |
docs/LLM_VS_CODE.md:32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:414-424`): the first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix, the clauses before the first removal, needs at least 2 content words; a clause joined to a removed one by a comma, 'and' or 'with' is not left behind. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
memory/DECISIONS.md:99:  - Item ids are case-scoped strings with a type prefix: `e…` entries, `a…` amounts, `f…` flags, `r…` records. Gap flags have deterministic ids `f_gap_<recA>_<recB>`.
memory/DECISIONS.md:100:  - **All offsets are absolute character offsets into `cases.raw_text`**, which is the pasted text after newline normalisation (CRLF and CR become LF and trailing whitespace is trimmed; nothing else is changed, offsets are unaffected, and the normalised text is what is hashed and stored). The grounding matcher compares whitespace-normalised text but builds a normalised-to-raw index map and returns raw offsets. If a verified excerpt cannot be mapped back, the item becomes `needs_review` with `HIGHLIGHT_NOT_FOUND` (R-ST-2, R-RV-9). The UI derives record-relative offsets by subtracting `records.char_start`.
memory/DECISIONS.md:165:  - **Demo gate (D-020).** `POST /api/cases` normalises the text (CRLF to LF, trimmed), computes its sha256 and accepts it only if the hash is in the recorded set: the sha256 of the normalised `evals/golden/*.txt`, computed at start-up (those files ship in the image). Any other text returns `409 demo_mode_unsupported_input` before anything is written ("Demo mode can only process the recorded sample cases."). `sample: true` works. `/run` re-checks the hash and returns the same 409 before any LLM call. Nothing a visitor pastes is ever stored by the public Space.
memory/DECISIONS.md:361:- Context: T-094 r2 (789cb39) landed the code-proposed conflict candidates with `judge_conflict_v5`; T-113 moved the judge to `judge_conflict_v6` and added the candidate drop rules. D-053 then ruled that nothing the model proposes is dropped, which replaced the suppression of ADR-019 item 2. D-042 reinstated guarded charge reclassification, which ADR-005, 011, 015 and 017 cut. D-054 (T-112, shipped; amended in T-112 r2) has code trim summary clauses that add salient new content. T-110 added the could-not-verify placeholder for a record with no output and the `totals.possible_overlaps` warning. The staff-engineer review of T-109 round 1 (`reviews/T-109-staff-engineer.md`) found that rows 7 and 103 still said a rate can never become a charge.
memory/DECISIONS.md:367:  5. **Summary trim (D-054 as amended by T-112 r2; shipped).** Before judging, code removes a summary clause only when it adds salient new content its excerpt lacks (a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term, matched by word family with abbreviations expanded; `app/backend/summary_trim.py:325-356`). Negation and side words come from the lexicon. A structural no-fragment rule applies: the first clause is never removed, the kept prefix has at least 2 content words, and a clause joined to a removed one by a comma, "and" or "with" is not left behind (`:414-424`). Each removal is shown in the trace. If nothing remains, the item goes to the tray with `SUMMARY_NOT_IN_QUOTE` (`generator.py:75-77`, `why.py:33`). The trim runs only on English-routed records. There is no prompt change.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:42.979Z

**tool call — Bash**
````
{
 "command": "git status --short | head; sed -n 1,25p evals/j3_controls.py; sed -n 20,32p app/backend/summary_trim.py; grep -n \"\" app/backend/summary_trim.py | sed -n 395,440p; sed -n 20,30p evals/golden/judge_controls.CHANGELOG.md; grep -n \"def trim\\|MIN_\\|first clause\\|drop\\[0\\]\" app/backend/summary_trim.py"
}
````

### User / tool · 2026-11-02T12:25:43.127Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
"""J3 seeded controls, built from pairs the shipped code actually proposes (T-093 r4, staff-engineer r3 major 1).

The first J3 controls were hand-written pairs (laterality, dates, doses, pain scores). conflict_candidates.candidates() never proposes those, so the
gate measured a path the product does not have. Here every J3 control input IS a candidate: the generator is run over the golden and library packets
(origin "packet": the real candidates) and over deliberately crafted variants of those real candidates (origin "variant": one quote replaced, the
other kept). A variant is only written if the generator proposes exactly that pair; the quotes in the file are the generator's own output.

Labels are LOCKED in SPEC below, with a rationale per item, before any live run (D-046): a failing item is a finding, never a relabel. `python -m
evals.j3_controls` regenerates the J3 rows of judge_controls.jsonl / judge_controls_heldout.jsonl and leaves the J4 rows byte for byte as they are.
`python -m evals.j3_controls --check` verifies the committed files equal the build (no live model, no network).

Row fields beyond the J4 rows: rule (the code rule that proposes it), origin, packet + packet_record_nos (real candidates), derived_from (variants),
records (the record texts the generator was run on, so a test can re-derive the pair)."""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GOLD = ROOT / "evals" / "golden"
PACKET_DIRS = ("evals/golden", "evals/library")
PLAN_OUT = ("2026-01-23", "2026-03-06")        # the dates of the real sample plan (record 4) and outcome (record 6)
DENIAL = ("2026-09-14", "2026-09-21")          # the dates of the real case_06 denial (record 1) and a later history record

PLAN, TREAT, OTHER = "plan_vs_outcome", "treatment_plan_vs_actual", "other_fact_mismatch"
    A capitalized word inside a clause is a name ('Fennimoor Spine Clinic'), not a body part.
    Clinical abbreviations are spelled out on both sides first (expand_abbreviations: lac, DJD, ESI, BLE, US, IM, C-collar ...), so 'Chin lac.' supports 'Laceration to the chin'.
    Terms (d-f) are matched by word FAMILY (lexicon below): the quote supports a term when it has a word of the same family (Tylenol~acetaminophen, cervical~neck,
    fingers~digits, prescription~prescribed) or of a family that covers it (a bare 'scan' is covered by MRI or CT; 'spine' by neck or back).
 3. A clause with no salient new content STAYS, whatever its other words ('Dizziness reported.' over 'Pt dizzy since crash.'; 'Walks with a cane' over 'Patient ambulating
    with cane'); the judge checks it. Whole clauses only: a kept clause is never edited. The kept text is never a fragment, by CONSTRUCTION and with no word list (T-128 r2/r3, D-054):
      (1) trim only a SUFFIX (T-128 r3): the kept text is always a prefix of whole clauses, and a clause is removed only when every clause after it is removed too,
          so no kept clause can follow (and depend on) a removed one ('Shoulder pain; surgery performed; due to torn labrum.' keeps both or drops the tail);
      (2) the FIRST clause is never removed: when it is unsupported nothing is trimmed and the whole summary goes to judge 1 (unless every clause is unsupported: rule 4);
      (3) the kept prefix has at least 2 content words.
    When a rule says no, the summary is returned unchanged. A lone participle before a removed ' with ' clause ('diagnosed' in 'diagnosed with diabetes') is that clause's
    head word and is removed with it.
 4. If every clause is removed, or the clauses left have no content word at all (stopwords and numbers only), `text` is '' and the caller sends the item to the
395:    why_removed = [new_salient(text, quote) for text, _ in clauses]
396:    drop = [bool(w) for w in why_removed]
397:    unchanged = {"text": summary, "removed": [], "kept": [c[0] for c in clauses], "supported": bool(summary), "notes": [], "changed": False}
398:    if not any(drop):
399:        return unchanged
400:    # 'diagnosed with diabetes': the lone participle left of a removed ' with ' clause is its head word, not a clause of its own: it goes with it (one removal, one note).
401:    merged = {}
402:    for i in range(len(clauses) - 1):
403:        if not drop[i] and drop[i + 1] and _joined_by_with(clauses[i][1]) and _PARTICIPLE.match(_single_word(clauses[i][0])):
404:            drop[i] = True
405:            merged[i] = i + 1
406:    removed = []
407:    for i, (c, d) in enumerate(zip(clauses, drop)):
408:        if not d or i - 1 in merged:
409:            continue
410:        text = c[0].rstrip(" .;,")
411:        removed.append(f"{text} with {clauses[i + 1][0].rstrip(' .;,')}" if i in merged else text)
412:    notes = [NOTE.format(r) for r in removed]
413:    left = [c[0] for c, d in zip(clauses, drop) if not d]
414:    if not left or not any(content_words(c) for c in left):
415:        return {"text": "", "removed": removed, "kept": [], "supported": False, "notes": notes, "changed": True}
416:    # T-128 r2/r3 (D-054 'never leave a fragment'), structural, no word list:
417:    if drop[0]:                                      # (2) the first clause is never removed: an unsupported first clause means the whole summary goes to judge 1
418:        return unchanged
419:    first_cut = drop.index(True)
420:    if not all(drop[first_cut:]):                    # (1) SUFFIX ONLY (T-128 r3): a clause is removed only when every clause after it is removed too, so no kept clause can depend on a removed one
421:        return unchanged
422:    if len(content_words(" ".join(c[0] for c in clauses[:first_cut]))) < 2:       # (3) the kept prefix must carry at least 2 content words ('Pain.' alone is not a summary)
423:        return unchanged
424:    out, last_kept = "", None
425:    for i, ((text, sep), d) in enumerate(zip(clauses, drop)):
426:        if d:
427:            continue
428:        piece = text.rstrip(" .;,")
429:        if last_kept is None:
430:            out = piece
431:        else:
432:            prev_sep = clauses[last_kept][1]
433:            use = prev_sep if i - 1 == last_kept else max((clauses[j][1] for j in range(last_kept, i)), key=_strength)
434:            out = _join(out, use, piece)
435:        last_kept = i
436:    out = out[:1].upper() + out[1:]
437:    if summary.rstrip().endswith("."):
438:        out += "."
439:    return {"text": out, "removed": removed, "kept": left, "supported": True, "notes": notes, "changed": True}
- The gate is now EVERY wrong item (wrong_caught == wrong_total, no false agree), not the 0.95 hallucination bar; a test fails if the threshold is read again (D-046).
- J3W11 (plan 12 visits vs completed all 12, discharged, benign) is unchanged and was never relabelled: it failed under judge_conflict_v2/v3 rule 1 and the fix was the prompt (v4), not the label.
- Counts after this change: in-sample 43 (J3 23, J4 20), held-out 13 (J3 6, J4 7); J3 wrong items 17 (14 in-sample, 3 held-out).

## 2026-11-02 round 4 (T-093, staff-engineer r3 major 1): J3 controls rebuilt from pairs the code proposes
- Why. `conflict_candidates.candidates()` proposes only two kinds of pair: a stated plan against a later early end (`plan_vs_outcome`) and a denial of prior problems against a prior-condition sentence (`history_denial`). The round 2/3 J3 set (laterality, dates, doses, pain scores, unrelated topics, "completed all 12 visits; discharged") was hand-written; 23 of its 29 rows were NOT PROPOSED by the generator (r3 review, reproduced), so "17/17 wrong caught" measured 2 wrong items on the production path.
- What. Every J3 row is now a candidate. `evals/j3_controls.py` runs the generator over every golden and library packet (4 real candidates exist: the sample plan against the discharge after missed appointments, and three case_06 denials: chiropractic history, baseline stiffness, the old shoulder problem) and over crafted variants of them (one quote replaced, the rule kept; held-out variants change both quotes). The script refuses to write a row the generator does not propose, and the quotes in the file are the generator's own output (including its clause cut at a semicolon: the judge sees "Cancelled the Tuesday appointment;", not the rest of the sentence). Counts: in-sample J3 17 (10 wrong, 7 correct), held-out J3 15 (7 wrong, 8 correct); J4 unchanged (12 wrong, 15 correct).
- Removed (not relabelled), because the generator does not propose them and the shipped path never sends them to the judge: J3C1 to J3C5, J3C7 to J3C10, J3W1 to J3W5, J3W11 to J3W19 (the old J3 ids), H3W2 to H3W4, H3C2 to H3C4 (the old held-out J3 ids). Their histories stay on this page: J3C10 / J3W1 (undated pain scores; run 20261102T035750Z gave FACT_MISMATCH; the J3C10 label and policy basis were confirmed by the second agent in round 3) and J3W11 (completed plan and discharge, benign; fixed in the prompt, never relabelled). Laterality, date, dose and pain conflicts are not flagged by the product at all (memory/SCOPE_CUTS.md), so a judge gate on them would test a path that does not exist. J3W11's case survives in spirit as J3V3 ("Therapy stopped after visit 12 as planned."); the discharge wording is not matched by the code's early-end pattern, so it cannot be a control.
- Labels were locked before the first live run of this set: they are in `evals/j3_controls.py` with a rationale per row, mirrored in `LOCKED` in tests/unit/test_t093_j3_controls_reachable.py, and committed before the run. A failing item is a finding, not a relabel (D-046). The matched-pair rule is now: every wrong item has a correct twin on the same first quote (a plan against a stop that is not the course ending vs one that is; a denial of the neck against a knee injury vs a cervical strain).
- Tests: `test_every_j3_control_input_is_producible_by_the_candidate_generator` (red if a code rule is removed: `test_the_reachability_check_goes_red_when_a_candidate_rule_is_removed`), and the real-candidate test fails when a golden or library packet gains or loses a candidate. J4 rows, including J4W7 (missed_care, disagree), are untouched.
- Findings seen while building (for T-094, not fixed here): the generator quotes only the clause that matched, cut at a semicolon, so the judge never sees "; attended all 12 visits"; `discontinued`, `no longer attends` and `dropped out` fire on a medicine, smoking or the gym; "Appointment cancelled by the clinic and moved to Friday." and "Treatment stopped after the final authorized session." are not proposed.
391:def trim(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> dict:
417:    if drop[0]:                                      # (2) the first clause is never removed: an unsupported first clause means the whole summary goes to judge 1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:47.140Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport json,collections\nfor f in [\"evals/golden/judge_controls.jsonl\",\"evals/golden/judge_controls_heldout.jsonl\"]:\n    rows=[json.loads(l) for l in open(f) if l.strip()]\n    j3=[r for r in rows if str(r.get(\"id\",\"\")).startswith((\"J3\",\"H3\"))]\n    print(f,len(rows),len(j3),collections.Counter(r.get(\"origin\") for r in j3),collections.Counter(r.get(\"rule\") for r in j3))\nE\ngrep -n \"def test_every_j3\\|def test_the_reachability\" tests/unit/*.py; grep -n \"dosage\\|laterality\\|dose\" docs/LLM_VS_CODE.md | cut -c1-120; sed -n 360,368p memory/DECISIONS.md | cut -c1-80; python3 tools/board.py show T-109 | tail -15"
}
````

### User / tool · 2026-11-02T12:25:47.320Z

**tool result**
````
evals/golden/judge_controls.jsonl 37 17 Counter({'variant': 13, 'packet': 4}) Counter({'history_denial': 9, 'plan_vs_outcome': 8})
evals/golden/judge_controls_heldout.jsonl 22 15 Counter({'variant': 15}) Counter({'history_denial': 9, 'plan_vs_outcome': 6})
tests/unit/test_t093_j3_controls_reachable.py:30:def test_every_j3_control_input_is_producible_by_the_candidate_generator():
tests/unit/test_t093_j3_controls_reachable.py:38:def test_the_reachability_check_goes_red_when_a_candidate_rule_is_removed():
34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is li
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems 
- Status: accepted (T-109 round 2, 2026-11-02; items 1, 2 and 5 updated in round
- Context: T-094 r2 (789cb39) landed the code-proposed conflict candidates with 
- Decision:
  1. **Conflict judge.** J3 is `judge_conflict_v6` (`judges.run_j3_meta`, `app/b
  2. **Nothing is suppressed (D-053).** There is no `suppressed_flags` output. A
  3. **Guarded reclassification (D-042, T-084; `app/backend/reclassify.py`).** A
  4. **Billing is a listing (D-052, T-083).** Unchanged from ADR-019 item 7: no 
  5. **Summary trim (D-054 as amended by T-112 r2; shipped).** Before judging, c
  6. **No-output records (T-110).** A record with no usable extract output (`LLM
- 2026-11-02T11:02:26Z orchestrator: Also update row 4 to the T-112 r2 trim rule (salient new content only; see D-054 as amended and the app/backend/summary_trim.py docstring) and drop 'not yet committed' (reviews/T-112-staff-engineer-r2.md major 2).
- 2026-11-02T11:45:38Z backend: From T-126 r2 (staff review minor 5): docs/LLM_VS_CODE.md rows 11/12 describe D-053 only. Please add one sentence for D-057: a model flag that a fixed code rule filters out (today D-032 objective_negative) is listed in a collapsed, counted 'Filtered by rule' group (case payload tray_filtered), never a flag, never in counts, the gate or the export; the rule filter is code, the model only proposed it. Also true now: every tray flag (judge-rejected, not word for word, rule-filtered) stays out of export pending counts and notes. Behaviour is in memory/contracts/api.md (FILTERED_BY_RULE row).
- 2026-11-02T12:13:37Z architect: AC 1 checked: commits f8bb674 (docs/LLM_VS_CODE.md) and the DECISIONS.md commit: row 4 = T-112 r2 trim (summary_trim.py:325-356, :414-424 no-fragment, lexicon negation/side :269, generator.py:70-79, 'not yet committed' dropped); row 11 = candidate drop rules (conflict_candidates.py:73-83, :98, :138), judge_conflict_v6 (judges.py:59), tray routes (flags.py:187-212, :349-352, :381-383); row 13/12 = D-057 (flags.py:126-131, :176-180; present.py:298-307; store.py:69); pytest test_summary_trim + test_conflict_candidates + test_t126_filtered_by_rule: 340 passed
- 2026-11-02T12:13:37Z architect: Round 3: r2 minors 2-6 done (D-053 conflicts-only scope, balance due/Spanish wording, 'not yet committed', ADR-019 reports 083252Z/085207Z, ADR-015 consequences) in ADR-015/019/020 + doc. Minor 7 (test name test_conflict_candidates.py:33, docstring conflict_candidates.py:8 'agree') not architect-owned; still open for backend/qa. D-053 text itself (ORCHESTRATOR_DECISIONS.md:61) still reads broader than ADR-020 item 2: orchestrator to add the 'conflicts only' scope.
- 2026-11-02T12:13:37Z architect: moved in_progress -> in_review
- 2026-11-02T12:13:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T12:25:25Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-109-staff-engineer-r3.md; round 3; findings:
    - [major] Row 11 says the J3 eval controls include dosage and laterality pairs; they do not, and the cited test file has none — fix: Architect: replace the sentence in row 11 with: 'Dosage and laterality pairs are neither proposed by code nor measured: the J3 controls are built only from pairs the code proposes (evals/j3_controls.py, T-093 r4), and the earlier dose and laterality controls were
    - [minor] Row 4 and ADR-020 item 5 describe the trim before T-128 r3; at b348221 the trim is suffix-only (SYNC NEEDED, not a failure of this card) — fix: Architect (after T-128 r3 is accepted): in row 4 and ADR-020 item 5 replace the comma/'and'/'with' sentence with 'code trims only a suffix: a clause is removed only when every clause after it is also removed (T-128 r3); otherwise the summary 
    - [minor] Carry-over from round 2 (half done): D-004, D-031 and SCOPE_CUTS row 15 still say a rate can never become a charge / reclassification is cut, with no superseded mark — fix: Orchestrator: append 'superseded by D-042 (guarded reclassification; ADR-020)' to D-004 and D-031 and to SCOPE_CUTS row 15 (or move row 15 to the reinstated list).
    - [minor] Carry-over (third round): test name and docstring still say plans 'agree', no card owns the rename — fix: Orchestrator: open a card for backend (code docstring) and qa (test name), or fold it into T-113 r2. Rename to '..._is_arithmetic_and_makes_one_plan_quoting_the_visit_count' and reword the docstring to 'the explicit visit count is the plan quoted; nothing is compared'.

## Handoff
What changed (f8bb674 + DECISIONS commit): row 4 = T-112 r2 trim (salient new content by word family, abbreviation expansion, lexicon negation/side words, structural no-fragment rule, tray SUMMARY_NOT_IN_QUOTE), 'not yet committed' removed; row 11 = judge_conflict_v6, candidate drop rules (different person, semicolon clause, intake forms), tray routes with file:line; rows 12/13 = D-057 Filtered by rule group; header D-057. ADR-015/019/020 updated for r2 minors 2-6. How verified: every claim read against HEAD code; pytest test_summary_trim, test_conflict_candidates, test_t126_filtered_by_rule 340 passed. Left: minor 7 (test name/docstring 'agree') is backend/qa; D-053 text needs the conflicts-only sentence (orchestrator). Surprised: intake forms are dropped only as plan/outcome, not as the denial side (history_denials has no paperwork test), so the doc says so.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:49.515Z

**tool call — Bash**
````
{
 "command": "sed -n 185,190p app/backend/flags.py | cut -c1-90; sed -n 207,213p app/backend/flags.py | cut -c1-70; grep -n \"def test_a_trim_never_leaves\\|def test_the_first_clause\\|def test_a_kept_prefix\\|def test_.*suffix\" tests/unit/test_summary_trim.py; sed -n 376,384p app/backend/flags.py | cut -c1-110"
}
````

### User / tool · 2026-11-02T12:25:49.629Z

**tool result**
````
def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:
    """A conflict the model proposed in the per-record pass (T-113, D-053; T-109 r2): only
    model's is a could-not-verify tray item (LLM_ONLY) with its own quotes and the fixed t
    out, seen = [], set()
        f["_tray"] = "LLM_ONLY"
        out.append(f)
    return out


def ground(flags: list, record: dict) -> list:
    """Rung 1 on model flags: quote must be verbatim in its record (el
162:def test_a_trim_never_leaves_a_fragment():
592:def test_a_trim_never_leaves_a_fragment_the_whole_summary_goes_to_the_judge(summary, excerpt):
635:def test_the_first_clause_is_never_removed():
646:def test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed():
656:def test_a_clause_joined_to_a_removed_one_by_comma_and_or_with_is_not_left_behind():      # still true, now a special case of the suffix rule
    phrase-list and model leaves it needs_review (JUDGE_DISAGREES); a model-only flag J4 rejects goes to the t
    A model-proposed CONFLICT is never a flag: only a code candidate (run_conflict_pass) can make one, so the 
    for i, f in enumerate(flags):
        if f["type"] == "record_warning" or f["state"] == "rejected":
            continue
        if f["type"] == "conflict" and f.get("origin") == "llm":
            _to_tray(f, "LLM_ONLY")
            continue
        _judge_one(f, i, call=call, case_text=case_text)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:50.670Z

Now edit.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:25:58.219Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np=\"docs/LLM_VS_CODE.md\"; s=open(p).read()\nold_r4=\"A **structural no-fragment rule** (no word list; `:414-424`): the first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix, the clauses before the first removal, needs at least 2 content words; a clause joined to a removed one by a comma, 'and' or 'with' is not left behind. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`).\"\nnew_r4=\"A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`).\"\nassert old_r4 in s; s=s.replace(old_r4,new_r4)\nold=\"(`summary_trim.py:414-415`; `generator.py:75-77`\"\nassert old in s; s=s.replace(old,\"(`summary_trim.py:414-415`; `generator.py:75-77`\")\nold11=\"The J3 eval controls include dosage and laterality pairs (`tests/unit/test_t093_eval_signature.py`), so the model's answer on them is measured; no code rule proposes them.\"\nnew11=\"Dosage and laterality pairs are neither proposed by code nor measured: every J3 control is a pair the candidate generator proposes (real packet candidates and variants of them, `evals/j3_controls.py`, checked by `tests/unit/test_t093_j3_controls_reachable.py::test_every_j3_control_input_is_producible_by_the_candidate_generator`), and the earlier dose, laterality, date and pain-score controls were removed for that reason (T-093 r4, 822ff38; `evals/golden/judge_controls.CHANGELOG.md`).\"\nassert old11 in s; s=s.replace(old11,new11)\ns=s.replace(\"`_model_conflicts`, `flags.py:187-212`, called at `:265`; `judge_flags`, `:381-383`)\",\"`_model_conflicts`, `flags.py:185-209`, called at `:265`; backstop in `judge_flags`, `:381-383`, for a conflict handed in directly)\")\nopen(p,\"w\").write(s)\np=\"memory/DECISIONS.md\"; s=open(p).read()\nold5=\"A structural no-fragment rule applies: the first clause is never removed, the kept prefix has at least 2 content words, and a clause joined to a removed one by a comma, \\\"and\\\" or \\\"with\\\" is not left behind (`:414-424`).\"\nnew5=\"A structural no-fragment rule applies (T-128 r3, `:417-423`): code trims only a suffix, so a clause is removed only when every clause after it is removed too and the kept text is a prefix of whole clauses; the first clause is never removed; the kept prefix has at least 2 content words; otherwise the summary goes to judge 1 unchanged.\"\nassert old5 in s; s=s.replace(old5,new5); open(p,\"w\").write(s)\nE\ngrep -n \"187-212\\|not left behind\\|:414-424\" docs/LLM_VS_CODE.md memory/DECISIONS.md | cut -c1-60; sed -n 185p app/backend/flags.py | head -1; grep -n \"def _model_conflicts\" -A25 app/backend/flags.py | grep -n \"return out\" "
}
````

### User / tool · 2026-11-02T12:25:58.355Z

**tool result**
````
memory/DECISIONS.md:364:  2. **Nothing is suppressed (D-053)

23:209-    return out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:26:01.135Z

**tool call — Bash**
````
{
 "command": "sed -i '364s/187-212/185-209/' memory/DECISIONS.md && grep -c \"185-209\" memory/DECISIONS.md docs/LLM_VS_CODE.md; sed -n 364p memory/DECISIONS.md | grep -o \".\\{60\\}185-209.\\{60\\}\"\nB=\"python3 tools/board.py\"\ngit add docs/LLM_VS_CODE.md memory/DECISIONS.md"
}
````

### User / tool · 2026-11-02T12:26:01.267Z

**tool result**
````
sed: 1: "memory/DECISIONS.md
": invalid command code m
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:26:01.973Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"docs(architect): T-109 r3 row 11 J3 controls (no dosage/laterality), row 4 and ADR-020 item 5 suffix-only trim (T-128 r3)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md memory/DECISIONS.md && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T12:26:02.366Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
5f1a7e2
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:26:04.996Z

**tool call — Bash**
````
{
 "command": "sed -i '' '364s/187-212/185-209/' memory/DECISIONS.md && grep -c \"185-209\" memory/DECISIONS.md && grep -n \"187-212\" docs/LLM_VS_CODE.md memory/DECISIONS.md | cut -c1-40; git add memory/DECISIONS.md"
}
````

### User / tool · 2026-11-02T12:26:05.123Z

**tool result**
````
1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:26:09.340Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"docs(architect): T-109 r3 ADR-020 item 2 cite _model_conflicts at flags.py:185-209\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- memory/DECISIONS.md && SHA=$(git rev-parse --short HEAD) && echo $SHA\nB=\"python3 tools/board.py\"\n$B claim T-109 --agent architect --force 2>&1 | tail -2\n$B ac T-109 --check 1 --agent architect --evidence \"r3 fixes: row 11 now names evals/j3_controls.py (no dosage/laterality; grep 'include dosage and laterality' empty); row 4 + ADR-020 item 5 describe suffix-only trim at summary_trim.py:417-423 (grep 'not left behind' empty); cites checked at HEAD\" 2>&1 | tail -1\n$B commit T-109 --sha $SHA --agent architect 2>&1 | tail -1\n$B handoff T-109 --agent architect --text \"Round 3 fixes (5f1a7e2, $SHA). Row 11: replaced the false 'J3 controls include dosage and laterality pairs' with the truth: neither proposed nor measured; all J3 controls are generator-proposed pairs (evals/j3_controls.py, reachability test, T-093 r4 822ff38, CHANGELOG). Row 4 and ADR-020 item 5: suffix-only trim (T-128 r3, summary_trim.py:417-423), prefix of whole clauses, first clause kept, >=2 content words; comma/and/with sentence removed. Also fixed _model_conflicts cite to flags.py:185-209 and judge_flags :381-383 as backstop. Verified by reading HEAD summary_trim.py/flags.py/j3_controls.py and grep of the old phrases (none left). Left: minor 7 test rename (orchestrator filing). Surprised: first-clause rule is implied by the prefix rule (reviewer mutant G).\" 2>&1 | tail -1\n$B move T-109 in_review --agent architect 2>&1 | tail -1"
}
````

### User / tool · 2026-11-02T12:26:09.966Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
425095f
T-109 claimed by architect
AC 1 checked: r3 fixes: row 11 now names evals/j3_controls.py (no dosage/laterality; grep 'include dosage and laterality' empty); row 4 + ADR-020 item 5 describe suffix-only trim at summary_trim.py:417-423 (grep 'not left behind' empty); cites checked at HEAD
T-109: commit 425095f recorded
handoff written on T-109
T-109: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:26:12.545Z

T-109 is back in `in_review`, with the commits recorded as 5f1a7e2 and 425095f. I checked each claim by reading HEAD code and grepping for the old phrases, which are gone; I did not re-run the tests.

- **Row 11:** it now says dosage and laterality pairs are neither proposed by code nor measured. Every J3 control is a pair the generator proposes (`evals/j3_controls.py`, T-093 r4 822ff38), and the earlier dose, laterality, date and pain controls were removed.
- **Row 4 and ADR-020 item 5:** both now describe the suffix-only trim from b348221 at `summary_trim.py:417-423`. I also fixed the `_model_conflicts` line range to `flags.py:185-209` in row 11 and ADR-020 item 2, which the review hadn't asked for.
