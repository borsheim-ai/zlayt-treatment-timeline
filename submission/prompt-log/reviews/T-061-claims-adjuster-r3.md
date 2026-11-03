# T-061 round 3 (final): self-report label precision, claims-adjuster review (Gary Pruitt)

Verdict: **fail** (2 blockers, 1 major, 3 minors). Reviewed object: commit a27b358 (D-035 clause-level patient_report), reviewed via `git archive` (session scratchpad `r3-a27`). HEAD is now d0c9cdb, which adds only `tests/unit/test_grounding_may.py`; it is not the reviewed object, but I ran the brief's pytest command on it as well.

D-024 item 7 says no harness rounds after M0 r3 and residual findings become debt. This card is product attribution, not harness, so I did not treat it as covered by that rule and did not downgrade the blockers. See questions_for_chris.

## Round 2 status

- r2 finding 1 (colon, abbreviation and long-subject speakers): **closed.** All six r2 rows return record (r2 probe rows MISS now OK).
- r2 finding 2 (spouse clause in a patient-subject sentence): **open, same class.** The semicolon form `C/O neck pain; wife reports headaches.` is record now. The same class with a comma, "and" or parentheses still carries the patient chip. Blocker 1.
- r2 finding 3 (`EMS reports neck pain, patient states headaches.`): **closed** as the brief allows. Only the patient clause is spanned (`['patient states headaches.']`); excerpt chip absent.
- r2 finding 4 (girlfriend, co-worker, passenger, ambulance crew, triage nurse): **closed.** D-035's "any other or unknown speaker gets no tag" rule holds on all of them.
- r2 finding 5 (spec text still lexicon-driven): **open.** Minor 4.
- r2 finding 6 (held-out coverage): **open.** Minor 6.

## Brief script-checks (all through production: `flags._flag` -> `source_kind`, and `grounding.has_self_report`)

- `Pt reports neck pain.` -> patient_report, span `['Pt reports neck pain.']`. OK.
- `Girlfriend says he limps.` -> record. OK.
- `C/O neck pain; wife reports headaches.` -> record. OK.
- `EMS reports neck pain, patient states headaches.` -> record at excerpt level; span `['patient states headaches.']`. OK (brief allows the absent excerpt chip).

## Findings

1. **Blocker. A family or EMS clause after a comma, "and" or a parenthesis inside a patient-subject sentence inherits the patient chip.** Evidence: `artifacts/review-evidence/T-061-r3-probe.txt`, MISS rows (group r3-adv), all `source_kind = patient_report`:
   - `Patient states pain began after the collision, wife reports headaches.`
   - `Pt reports neck pain, EMS notes headaches.`
   - `Patient reports neck pain and his wife says he is in pain.`
   - `Patient reports neck pain, per his wife, headaches began at the scene.`
   - `Patient reports neck pain (per wife, headaches since the scene).`
   - `Patient reports pain 4/10, girlfriend says he limps.`
   - `Patient reports neck pain, Mrs. Ortiz reports headaches.`

   In each, the span from `patient_report_spans` (grounding.py:189-200) runs from the patient word to the next `;` or sentence end (`S.unit_spans`, sentences.py:29). The span therefore swallows the comma-joined family clause, and `_self_report` (grounding.py:205-213) only searches the text outside the span for a reporting word, so the family clause is never seen. The comment at grounding.py:190-191 says a clause "starts at a unit start or after a comma", but the span end ignores commas. The commit's own test pins the span to `;` (tests/unit/test_flags_pass.py:190-196), and no test covers a comma-joined family clause.

   Why it matters: the chip tells the reader the claimant said what the wife, girlfriend or EMS said. D-033 calls this exact error "a credibility error an adjuster would exploit" (memory/ORCHESTRATOR_DECISIONS.md:41). r2 finding 2 was this class and was a blocker. Under the architect's chosen rule (b) (grounding.py:206 "a mixed excerpt cannot carry one chip, so it carries none"), these excerpts must be record. D-035's default is "a missing chip is safe, a wrong chip is not" (ORCHESTRATOR_DECISIONS.md:44).

   Fix: either (i) end the patient span at the next comma, "and" or open parenthesis that begins another clause, so the family clause falls outside the span and rule (b) applies; or (ii) safer and simpler: attach the chip only when the patient clause is the whole excerpt, so any following clause makes the excerpt record. Under (ii) the pinned `Pt c/o neck pain; wife drove him in.` (test_flags_pass.py:195-196 area) becomes record, and that test must change with it.

   Acceptance test: all seven rows above return `has_self_report` False and `source_kind` record through `flags._flag`. `Patient states EMS noted a laceration.`, `Patient reports his wife said he was fine.` and `Patient states his wife drove him to the ER.` stay patient_report. `.venv/bin/python research/lexicon_selfcheck.py` still PASS. Add the seven rows to test_flags_pass.py.

2. **Blocker. A non-patient clause whose reporting verb is outside the closed list inherits the chip.** Evidence: `artifacts/review-evidence/T-061-r3-probe.txt`, MISS rows (group r3-adv2), all `source_kind = patient_report`:
   - `Patient states neck pain; wife thinks he is faking.` (semicolon form: the span does end at the `;`, but "thinks" is not in `_VERB`, grounding.py:183-184)
   - `Patient reports neck pain, wife thinks he is faking.`
   - `Patient states neck pain; his wife told the ER he was fine.`
   - `Patient states neck pain, EMS notes headaches, wife reports nausea.`

   Cause: `_self_report` decides "no other speech" by searching the leftover text for the closed `_REPORT_WORD` list (grounding.py:186, 213). Any non-patient clause with a verb outside that list ("thinks", "told", "insists", "mentions") passes as "no other report". The lexicon's exclude list has `thinks?` and `links?` (lexicon.yaml:89), but production no longer reads it (see finding 3).

   Why it matters: the excerpt quotes a spouse's or family member's opinion or account under the claimant's "Patient self-report" chip. This is the r2 finding 2 class again, reached through a different door. D-035 says "any other or unknown speaker ... gets no tag" (ORCHESTRATOR_DECISIONS.md:44). A closed verb list cannot satisfy an "any speaker" rule.

   Fix: the mixed-excerpt test must not depend on a verb list. Under rule (b), an excerpt that contains any clause after the patient clause is record. Under (ii) in finding 1 this is the same change. Do not add verbs to the list as the fix; that just moves the hole.

   Acceptance test: the four rows above return record. Add them to `test_d035_mixed_excerpt_carries_no_chip` (test_flags_pass.py:199-202). Then `Pt c/o neck pain; wife drove him in.` decides under the chosen rule; the test must say which.

3. **Major. The research gate PASS measures a rule production no longer runs.** Evidence: `.venv/bin/python research/lexicon_selfcheck.py` on the a27b358 archive gives `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115` and `RESULT: PASS`, exit 0. The selfcheck applies its own `is_patient_statement` (research/lexicon_selfcheck.py:165, called at :179) to lexicon `self_report` entries. Production does not: grounding.py:73-76 still loads `self_report` and `self_report_exclude`, and `_self_report` (grounding.py:205-213) reads neither. `grep -rn "exclude_sentence\|self_report_scope" app tests` finds only the lexicon and the loader (grounding.py:75).

   Why it matters: a PASS on the research gate says nothing about what the flag layer emits. The probe rows in finding 1 and 2 are exactly the cases the gate cannot see. The persona rule is that a self-check PASS does not prove the product path.

   Fix: the selfcheck should call `grounding.has_self_report` (the production function) on the golden, held-out and adversarial rows, or the lexicon self_report entries and `self_report_scope` should be deleted once D-035 is the only rule.

   Acceptance test: `research/lexicon_selfcheck.py` imports and calls `app.backend.grounding.has_self_report` for the patient-attribution rows, and the seven finding-1 and four finding-2 rows are in the held-out set with expected record.

4. **Minor. Spec and lexicon text still state the superseded rule, and one lexicon note contradicts D-035 and the pinned test.** Evidence: `memory/DECISIONS.md:286` still reads "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". `app/llm/lexicon.yaml:25-26` says the same. `app/llm/lexicon.yaml:764` reads `"C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.` That contradicts the commit's pinned no-tag for bare "C/O neck pain 7/10 and headache." (test_flags_pass.py:184-188 area).
   Fix: amend DECISIONS.md:286 and lexicon.yaml:25-26 to D-035's rule. Rewrite lexicon.yaml:764 to say bare C/O gets no chip.
   Acceptance test: `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` returns nothing; `grep -n "read as the patient, which is the clinical convention" app/llm/lexicon.yaml` returns nothing.

5. **Minor. D-035 narrows the chip without saying so, and the code's verb set is wider than D-035's list.** Evidence: probe rows, `Patient-reported neck pain 7/10.` -> record; `Patient links her neck pain to the collision.` -> record; `C/O neck pain 7/10 and headache.` -> record. All three were patient_report in r1 and r2. The commit moved them to the no-list (test diff: `git show a27b358 -- tests/unit/test_flags_pass.py`). Separately, `_VERB` (grounding.py:183-184) includes describes, admits, recalls, claims, believes, feels, relates and attributes, which D-035's parenthetical (ORCHESTRATOR_DECISIONS.md:44) does not name.
   Why it matters: a missing chip is safe under D-035, so this is not a blocker. But the team's spec and the code should agree on what counts as an explicit patient attribution, and "C/O" is the adjuster's most common patient-voice marker.
   Fix: name the verb set in D-035 (or trim `_VERB` to it). Decide on bare C/O (question 3).
   Acceptance test: D-035 lists the verb set used by `_VERB`, and the three rows above are either tagged or listed as deliberate no-tag in D-035.

6. **Minor. Held-out set still has no patient-subject sentence naming a family or EMS member (r2 finding 6, carried forward).** Evidence: `grep -n "Patient states EMS noted\|wife said he was fine\|Patient states his wife" evals/lexicon_heldout.jsonl` returns nothing. The only family-named row is H-109, `Per his wife, headaches began at the scene.`
   Fix: add `Patient states EMS noted a laceration.` and `Patient reports his wife said he was fine.` with expected patient_report.
   Acceptance test: both appear in evals/lexicon_heldout.jsonl and the research gate checks them (finding 3).

## What is not a finding

- `Patient-reported` and bare `C/O` losing the chip: a deliberate D-035 narrowing with a pinned test. Reported as finding 5 and question 3, not as a blocker.
- `Per EMS, pt. c/o neck pain.` and `EMS noted pt. reports neck pain 7/10.`: record, as in r2.
- `Date of accident per intake form: 2026-01-19.`: record, so the intake date is not an attribution.
- The `test_split_llm.py` failure on the archive (below): outside my lens.

## Outside my lens

`tests/unit/test_split_llm.py::test_split_audit_row_has_prompt_version_and_flag_resolves_to_call` fails on the a27b358 archive and on the parent 473ac2a archive, so it is not caused by this commit. The `-k "flag or ..."` filter matches it by name. The live tree passes it. I did not triage why the archive fails.

## Exercised

- Read `personas/claims-adjuster.md` in full; `memory/ORCHESTRATOR_DECISIONS.md` (D-024 line 32, D-033 line 41, D-035 line 44); `reviews/T-061-claims-adjuster.md` (r1, full); `reviews/T-061-claims-adjuster-r2.md` (full); my memory files `feedback_review_commit_not_worktree.md`, `project_t061_r2_speaker_scope.md`, `feedback_lexicon_review_method.md`.
- `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon or self_report" 2>&1 | tail -2` on the live tree (HEAD d0c9cdb) gave `123 passed, 770 deselected in 2.23s`. A second run gave `123 passed, 772 deselected in 2.07s`; the count moved because the tree moved.
- `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm`: `M app/llm/record.py` and evals reports only. None of the reviewed files has a diff. `git merge-base --is-ancestor a27b358 d0c9cdb` says the commit is in HEAD. `git show --stat d0c9cdb` gives `tests/unit/test_grounding_may.py` only.
- `git archive a27b358` extracted to the session scratchpad `r3-a27`. `cd r3-a27 && .venv/bin/python -m pytest tests/unit -q -k "flag or lexicon or self_report" -p no:cacheprovider 2>&1 | tail -2` gave `1 failed, 122 passed, 760 deselected`. The failure is the `test_split_llm.py` case above. The same command on `git archive 473ac2a` (parent) gave `1 failed, 122 passed, 760 deselected`.
- `artifacts/review-evidence/T-061-r3-probe.py` (new, read-only) run against the a27b358 archive: `.venv/bin/python artifacts/review-evidence/T-061-r3-probe.py <r3-a27>`. Output saved to `artifacts/review-evidence/T-061-r3-probe.txt`: 70 rows (r1 probe, r2 probe, the brief sentences, and r3 variants); `SUMMARY rows=70 misses=11 superseded=3`. The probe calls `flags._flag` (flags.py:46 constructor) and `grounding.has_self_report` and `grounding.patient_report_spans`. The module path printed was the archive's grounding.py.
- `research/lexicon_selfcheck.py` run from the archive: `RESULT: PASS`, exit 0 (finding 3).
- `grep -n "exclude_sentence\|self_report_scope" app/ tests/` in the archive: lexicon.yaml:88-89 and grounding.py:75 (loader only); `sed -n 68,84p` and `grep -n` on grounding.py for `_self_report`, `_lexicon()`, `self_report_exclude`.
- `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` gave line 286. `grep -n "clinical convention"` on the archive's lexicon.yaml gave line 764.
- `grep` of `evals/lexicon_heldout.jsonl` for the two patient-subject family/EMS sentences: no output (finding 6).
- `git show a27b358 -- app/backend/grounding.py` and `git show a27b358 -- tests/unit/test_flags_pass.py` (full diffs read).
- Probe rows reproduced by hand through `flags._flag` in the probe output (the file above).

```json
{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit a27b358 (T-061 r3, D-035 clause-level patient_report: app/backend/grounding.py, tests/unit/test_flags_pass.py), reviewed via git archive in the session scratchpad (r3-a27); HEAD d0c9cdb (adds test_grounding_may.py only) ran for the brief pytest command; specs memory/ORCHESTRATOR_DECISIONS.md D-033 (line 41), D-035 (line 44), D-024 (line 32), memory/DECISIONS.md:286; no app URL (flag and attribution layer, no UI in scope); probe artifacts/review-evidence/T-061-r3-probe.py -> T-061-r3-probe.txt.",
 "exercised": [
  "Read personas/claims-adjuster.md in full; ORCHESTRATOR_DECISIONS.md D-024, D-033, D-035; reviews/T-061-claims-adjuster.md (r1) and reviews/T-061-claims-adjuster-r2.md (full); my memory files",
  ".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon or self_report' 2>&1 | tail -2 -> 123 passed, 770 deselected (live, d0c9cdb); second run 123 passed, 772 deselected",
  "git status --short on reviewed paths (only app/llm/record.py and evals reports, none reviewed); git merge-base --is-ancestor a27b358 d0c9cdb; git show --stat d0c9cdb",
  "git archive a27b358 -> scratchpad r3-a27; pytest -k 'flag or lexicon or self_report' there -> 1 failed, 122 passed (test_split_llm.py::test_split_audit_row_has_prompt_version_and_flag_resolves_to_call, same failure on parent 473ac2a archive; outside scope)",
  "artifacts/review-evidence/T-061-r3-probe.py against the a27b358 archive -> artifacts/review-evidence/T-061-r3-probe.txt: 70 rows, misses 11 (r3-adv 7, r3-adv2 4), superseded 3; brief script-checks 4/4, r1 19/19, r2 colon/abbrev/long-subject 11/11, r2 adv2 6/6, r2 mixed 2/2",
  "research/lexicon_selfcheck.py on the archive -> SUMMARY golden MUST 11/11, held-out 115/115; RESULT: PASS; exit 0",
  "sed -n 68,84p and grep -n on app/backend/grounding.py (lines 73-76, 183-186, 189-200, 205-213, 243-245): production reads no lexicon self_report entry and no self_report_exclude",
  "grep -rn exclude_sentence|self_report_scope app/ tests/ on archive -> lexicon.yaml:88-89, grounding.py:75 only",
  "grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md -> 286; grep 'clinical convention' lexicon.yaml -> 764",
  "grep -n 'Patient states EMS noted|wife said he was fine|Patient states his wife' evals/lexicon_heldout.jsonl -> no output; only H-109 names a family member",
  "git show a27b358 -- app/backend/grounding.py and -- tests/unit/test_flags_pass.py (full diffs read); grep -n on test_flags_pass.py for test_d035_* line numbers"
 ],
 "verdict": "fail",
 "scores": {"attribution_precision_production": 2, "clause_scope_logic": 2, "ac2_flags_wiring": 4, "prior_findings_closed": 3, "test_honesty": 3, "spec_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A family or EMS clause after a comma, 'and' or a parenthesis inside a patient-subject sentence inherits the patient chip",
   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt MISS rows r3-adv: 'Patient states pain began after the collision, wife reports headaches.', 'Pt reports neck pain, EMS notes headaches.', 'Patient reports neck pain and his wife says he is in pain.', 'Patient reports neck pain, per his wife, headaches began at the scene.', 'Patient reports neck pain (per wife, headaches since the scene).', 'Patient reports pain 4/10, girlfriend says he limps.', 'Patient reports neck pain, Mrs. Ortiz reports headaches.' all give source_kind patient_report; span is the whole sentence. Cause: app/backend/grounding.py:189-200 patient_report_spans runs the span to the next ';' or sentence end (S.unit_spans, app/backend/sentences.py:29); grounding.py:205-213 _self_report searches only the text outside the span, so the comma-joined family clause is never checked. Comment at grounding.py:190-191 says a clause starts after a comma but the span end ignores commas. tests/unit/test_flags_pass.py test_d035_tag_spans_the_patient_clause_only (line 190) pins the ';' span; no comma-joined case is tested.",
   "why_it_matters": "The chip tells the reader the claimant said what a wife, girlfriend, EMS or family member said. D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) names this exact error as a credibility error an adjuster would exploit. This is the r2 finding 2 class, which was a blocker; the semicolon form now passes but the comma, 'and' and parenthesis forms do not. Under the chosen rule (b) (grounding.py:206) these excerpts must be record. D-035 (ORCHESTRATOR_DECISIONS.md:44): a missing chip is safe, a wrong chip is not.",
   "fix": "(i) End the patient span at the next comma, 'and' or open parenthesis that begins another clause, so rule (b) applies to the family clause; or (ii) attach the chip only when the patient clause is the whole excerpt (safer, simpler). Under (ii) the pinned 'Pt c/o neck pain; wife drove him in.' changes to record and its test changes with it.",
   "acceptance_test": "The seven r3-adv rows return has_self_report False and source_kind record via flags._flag. 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.' stay patient_report. research/lexicon_selfcheck.py still PASS. The seven rows are added to tests/unit/test_flags_pass.py."},
  {"severity": "blocker",
   "title": "A non-patient clause whose reporting verb is outside the closed list inherits the chip",
   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt MISS rows r3-adv2 (all source_kind patient_report): 'Patient states neck pain; wife thinks he is faking.', 'Patient reports neck pain, wife thinks he is faking.', 'Patient states neck pain; his wife told the ER he was fine.', 'Patient states neck pain, EMS notes headaches, wife reports nausea.'. Cause: app/backend/grounding.py:186 _REPORT_WORD and :183-184 _VERB are closed lists; _self_report (grounding.py:205-213) decides 'no other speech' by searching the leftover text for them. 'thinks', 'told', 'insists' are not in the list.",
   "why_it_matters": "The excerpt quotes a spouse's or family member's opinion or account under the claimant's 'Patient self-report' chip. D-035 says any other or unknown speaker gets no tag (ORCHESTRATOR_DECISIONS.md:44); a closed verb list cannot satisfy an any-speaker rule. Same credibility error as D-033 (line 41).",
   "fix": "Make the mixed-excerpt test independent of the verb list: under rule (b), any clause after the patient clause makes the excerpt record. Do not fix by adding verbs; that moves the hole.",
   "acceptance_test": "The four r3-adv2 rows return record. They are added to test_d035_mixed_excerpt_carries_no_chip (tests/unit/test_flags_pass.py:199). The pinned 'Pt c/o neck pain; wife drove him in.' is decided under the chosen rule and the test says which."},
  {"severity": "major",
   "title": "The research gate PASS measures a rule production no longer runs",
   "evidence": "research/lexicon_selfcheck.py on archive a27b358: 'SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115', 'RESULT: PASS', exit 0. The selfcheck applies its own is_patient_statement (research/lexicon_selfcheck.py:165, called at :179) to lexicon self_report entries. Production: app/backend/grounding.py:73-76 loads self_report and self_report_exclude; _self_report (grounding.py:205-213) reads neither. grep -rn exclude_sentence|self_report_scope app/ tests/ finds only app/llm/lexicon.yaml:88-89 and grounding.py:75 (loader).",
   "why_it_matters": "A PASS on the research gate says nothing about what flags.py:46 and :125 emit. The cases in findings 1 and 2 are exactly what the gate cannot see. A self-check that tests a rule production does not run gives false comfort.",
   "fix": "Make the selfcheck call grounding.has_self_report (the production function) for the patient-attribution rows, or delete the lexicon self_report entries and self_report_scope once D-035 is the only rule.",
   "acceptance_test": "research/lexicon_selfcheck.py imports app.backend.grounding.has_self_report and reports its result for the attribution rows; the finding 1 and finding 2 rows are in evals/lexicon_heldout.jsonl with expected record; selfcheck PASS."},
  {"severity": "minor",
   "title": "Spec and lexicon text still state the superseded rule; one lexicon note contradicts D-035 and the pinned test",
   "evidence": "memory/DECISIONS.md:286: '`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26 says the same. app/llm/lexicon.yaml:764: '\"C/O\" and \"complains of\" with no named speaker are read as the patient, which is the clinical convention.' The pinned no-tag for bare 'C/O neck pain 7/10 and headache.' is in tests/unit/test_flags_pass.py (no-list, around line 184).",
   "why_it_matters": "A future reader gets two rules, and the lexicon note tells the reader the opposite of what the code does for bare C/O.",
   "fix": "Amend DECISIONS.md:286 and lexicon.yaml:25-26 to D-035's rule. Rewrite lexicon.yaml:764 to say bare C/O gets no chip.",
   "acceptance_test": "grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md returns nothing; grep -n 'read as the patient, which is the clinical convention' app/llm/lexicon.yaml returns nothing."},
  {"severity": "minor",
   "title": "D-035 narrows the chip without saying so, and the code's verb set is wider than D-035's list",
   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt: 'Patient-reported neck pain 7/10.' -> record; 'Patient links her neck pain to the collision.' -> record; 'C/O neck pain 7/10 and headache.' -> record. All three were patient_report in r1 and r2; the commit moved them to the no-list (git show a27b358 -- tests/unit/test_flags_pass.py). _VERB (app/backend/grounding.py:183-184) includes describes, admits, recalls, claims, believes, feels, relates, attributes, which D-035's parenthetical (ORCHESTRATOR_DECISIONS.md:44) does not name.",
   "why_it_matters": "A missing chip is safe under D-035, so this is not a blocker. The spec and the code should agree on what counts as explicit patient attribution, and bare C/O is the most common patient-voice marker in clinical notes.",
   "fix": "Name the verb set in D-035 or trim _VERB to it. Decide on bare C/O (question 3).",
   "acceptance_test": "D-035 lists the verb set used by _VERB; the three rows are either tagged or recorded as deliberate no-tag in D-035."},
  {"severity": "minor",
   "title": "Held-out set has no patient-subject sentence naming a family or EMS member (r2 finding 6, carried forward)",
   "evidence": "grep -n 'Patient states EMS noted|wife said he was fine|Patient states his wife' evals/lexicon_heldout.jsonl: no output. The only family-named row is H-109 'Per his wife, headaches began at the scene.' (evals/lexicon_heldout.jsonl:109).",
   "why_it_matters": "The research gate cannot show a regression on the patient-subject-plus-family case, which is the over-exclusion class from r1 finding 3.",
   "fix": "Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' with expected patient_report.",
   "acceptance_test": "Both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report and the research gate checks them."}
 ],
 "whats_right": [
  "The r2 colon, abbreviation and long-subject forms and the third-party speakers (girlfriend, co-worker, passenger, ambulance crew, triage nurse) are record now: 11/11 r2 adv and 6/6 r2 adv2 rows match, and the default-no-tag design of D-035 is the right shape.",
  "The semicolon mixed case is fixed: 'C/O neck pain; wife reports headaches.' is record, and 'EMS reports neck pain, patient states headaches.' spans only 'patient states headaches.' (brief allowed the absent excerpt chip).",
  "All four brief script-checks hold through the production constructor: 'Pt reports neck pain.' tagged; 'Girlfriend says he limps.' and 'C/O neck pain; wife reports headaches.' none; and the round-1 EMS, witness, wife, family and intake-date rows are record."
 ],
 "questions_for_chris": [
  "Does a clause end at a comma? D-035 says the tag spans to the next ';' or sentence end, which is what makes finding 1 possible. My recommendation is option (ii) in finding 1 (chip only when the patient clause is the whole excerpt), because a missing chip is safe and a wrong one is not. Confirm (i) or (ii).",
  "Is the chip meant to cover a non-patient clause that has no speech verb, such as 'Pt c/o neck pain; wife drove him in.' (pinned by test_flags_pass.py)? Under rule (b) it should be record; the pinned test says patient_report. Which one?",
  "Bare 'C/O neck pain 7/10' and 'Patient-reported neck pain' now have no chip (pinned). The lexicon note at lexicon.yaml:764 calls C/O the clinical convention for the patient. Is the no-chip outcome deliberate, and should D-035 say so?",
  "D-024 item 7 says no harness rounds after M0 r3, residual findings become debt. T-061 is product attribution, not harness. I did not downgrade the two blockers on that basis. Is T-061 under that rule, or does it need a fix before the gate?",
  "The persona file expects model claude-opus-5-5 in the review record. I ran as claude-haiku-5-5 and wrote that id, as in rounds 1 and 2. Confirm acceptable for the gate."
 ]}
```
