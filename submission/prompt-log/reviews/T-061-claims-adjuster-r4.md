# T-061 round 4 (final): patient_report under D-037, claims-adjuster review (Gary Pruitt)

Verdict: **fail** (1 blocker, 3 minors). Reviewed object: commit 991dac4 (D-037 whole-excerpt chip), reviewed via `git archive 991dac4` extracted to `artifacts/review-evidence/T-061-r4-991` (HEAD is now b614b40; `git diff --stat 991dac4 HEAD` on the reviewed files is empty, so HEAD tests the same code). Judged against D-037 (memory/ORCHESTRATOR_DECISIONS.md:45): "the chip attaches only when the whole excerpt is a single patient-subject clause ... any further clause means no chip".

## Round-3 status (reviews/T-061-claims-adjuster-r3.md)

- **B1 (comma, "and", parenthesis family clause inside a patient-subject sentence): closed.** All seven r3 rows return `has_self_report` False and `source_kind` record through `flags._flag` (probe rows OK, group r3-B1). The comma/and/parenthesis forms no longer leak.
- **B2 (non-patient clause whose verb is outside the closed list): closed.** All four r3 rows return record (group r3-B2). The verb list is no longer consulted for mixed excerpts.
- **Major 3 (research gate measures a rule production no longer runs): closed in form.** `research/lexicon_selfcheck.py:162-166` `production_chip()` calls `app.backend.grounding.has_self_report`; the gate reports `[production chip] ... 18/18` and `RESULT: PASS`. Sub-acceptance not met: the r3 finding 1/2 rows were to go in `evals/lexicon_heldout.jsonl`; they sit in the selfcheck's closed `CHIP_NO` list instead (`research/lexicon_selfcheck.py:172`), and `grep` of the held-out file returns 0 rows. See minor 2.
- Carried minors: r3 minor 5 (verb set not named in D-037; partly narrowed, see minor 3), r3 minor 6 (no family/EMS patient-subject row in held-out, see minor 2). r3 minor 4 (stale text) is still open, routed (minor 3).

## Findings

1. **Blocker. D-037's "any further clause means no chip" is implemented as a four-separator list. Eleven mixed excerpts still carry the patient chip.** Evidence: `artifacts/review-evidence/T-061-r4-probe.txt` (run with `.venv/bin/python artifacts/review-evidence/T-061-r4-probe.py artifacts/review-evidence/T-061-r4-991`), MISS rows, all `chip=True source_kind=patient_report`:
   - Five new attacks (group r4-new):
     - `Patient states neck pain but his wife reports headaches.`
     - `Patient states neck pain: wife reports headaches.`
     - `Patient reports neck pain — EMS notes headaches.`
     - `Patient states neck pain with his wife reporting headaches.`
     - `Patient states neck pain while wife says he limps.`
   - Six extra variants of the same class (group r4-extra): `... neck pain & wife reports headaches.`, `... neck pain / wife reports headaches.`, `... neck pain [wife reports headaches].`, `... neck pain plus wife reports headaches.`, `... neck pain as wife reports headaches.`, `Patient reports neck pain per wife.`
   - Cause: `app/backend/grounding.py:187` `_FURTHER_CLAUSE = [;,(]|\band\b` only. `:196` returns the whole excerpt as the span whenever it is one unit and matches the patient subject. A colon, em dash, `&`, `/`, brackets, `plus`, `as`, `with`, `while` or `but` introduces a clause and is not in the list, so the function returns the chip. `:180-183` says "no further clause", which the code does not enforce. The mixed-case control `Patient states neck pain, but wife reports headaches.` is record (group r4-extra), so only the comma-less forms leak.
   - Why it matters: ten of the eleven rows put a wife, EMS or family clause under the claimant's "Patient self-report (not a physician's opinion)" label. That is the credibility error D-033 names (memory/ORCHESTRATOR_DECISIONS.md:41), and D-037's own headline says "a wrong chip mislabels the source". "per wife" (no clause, no verb) is the weakest row; the blocker stands on the ten clause rows without it. The gate is blind here: `research/lexicon_selfcheck.py` PASSes 18/18 on its closed row list at `:172-179`, and it has none of the eleven rows.
   - Fix: make the chip rule closed on grammar, not on speakers or verbs. Attach the chip only when the text after the patient subject and reporting verb contains (a) no clause-introducing punctuation other than the final period (`: ; , ( ) [ ] & + — –`, and `/` surrounded by spaces; `4/10` and `c/o` are exempt) and (b) no connector from a closed function-word set (`and, or, but, with, while, as, plus, per, whereas, though, although, because, which, who, when, if, until, then, nor, yet, than`). Put the same set in D-037 so the spec and the code agree. If Chris decides the four-separator list is the complete rule, the eleven rows become a documented residual instead of a defect (question 1); I did not downgrade them, because the brief states the headline rule.
   - Acceptance test: `artifacts/review-evidence/T-061-r4-probe.py` reports 33/33 with the eleven rows `chip=False source_kind=record`. Add the eleven rows to `NO_TAG` (`tests/unit/test_flags_pass.py:167`) and to `CHIP_NO` (`research/lexicon_selfcheck.py:172`); the selfcheck must go red on the pre-fix code and pass after. Keep chipped: `Patient states EMS noted a laceration.`, `Patient reports his wife said he was fine.`, `Patient states his wife drove him to the ER.`, `Pt reports neck pain 7/10.`, `The patient denies loss of consciousness.`, `Patient states neck pain.`. `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py` stays green after the test edits.

2. **Minor. Held-out set still has no patient-subject family or EMS row, and the gate's closed row list is why a PASS hides misses.** Evidence: `grep -n "Patient states EMS noted\|wife said he was fine\|Patient states his wife" evals/lexicon_heldout.jsonl` returns no output (0 rows). The r3 finding 1/2 rows are in `research/lexicon_selfcheck.py:172-179`, not in the held-out file the r3 acceptance named. Finding 1's eleven rows also fail production while the gate prints `RESULT: PASS` (`[production chip] ... 18/18`).
   - Why it matters: a PASS on a closed list is the failure r3 finding 3 named. The selfcheck now calls production, which is the fix; the coverage is still one list.
   - Fix: add the three keep rows and the r4-new rows to `evals/lexicon_heldout.jsonl` with `expected` patient_report or record, and have the gate read them.
   - Acceptance test: `grep -c "wife said he was fine" evals/lexicon_heldout.jsonl` is at least 1, and the gate's production-chip line reports the held-out rows, not only the in-script list.

3. **Minor (routed, not failing). Stale text still states superseded rules, and one note contradicts the pinned test.** Evidence, routed to owners:
   - `memory/DECISIONS.md:286` (architect): "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". Production reads no lexicon `self_report` entry (`app/backend/grounding.py:201-202`).
   - `app/llm/lexicon.yaml:25-26` (researcher): "code sets source_kind = "patient_report" from it (ADR-013)".
   - `app/llm/lexicon.yaml:84-93` (researcher): `self_report_scope` and `exclude_sentence` remain with examples. Production and the selfcheck no longer use them. Delete or mark as unread.
   - `app/llm/lexicon.yaml:764` (researcher): "`"C/O"` and `"complains of"` with no named speaker are read as the patient, which is the clinical convention." This contradicts D-037's "Bare `C/O` gets no chip" and the pinned no-chip row at `tests/unit/test_flags_pass.py:118`/`:175`.
   - Verb set (orchestrator, D-037 text): `_VERB` at `app/backend/grounding.py:184-185` includes stated, reported, noted, said, endorsed, denied, described. D-037 names no verbs; D-035 (memory/ORCHESTRATOR_DECISIONS.md:43) names states, reports, notes, says, endorses, complains of, c/o, denies. This is r3 minor 5, partly narrowed.
   - Acceptance test: `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` and `grep -n "read as the patient, which is the clinical convention" app/llm/lexicon.yaml` return nothing; D-037 names the verb set `_VERB` uses.

## What is not a finding

- `Patient reports low back pain in 2023, resolved.` and `Patient reports neck pain and headache.` now have no chip because of the comma or "and". D-037 accepts a missing chip ("a missing chip is safe"). The `pre_existing` flag itself is unaffected; only `source_kind` changes. Not a finding.
- `Patient-reported neck pain 7/10.`, `Patient links her neck pain to the collision.` and bare `C/O neck pain 7/10 and headache.`: no chip, as D-037 and the pinned tests say. Not a finding.
- `Pt c/o neck pain; wife drove him in.` is record, as the r3 Q2 question asked; the pinned test at `tests/unit/test_flags_pass.py:204` says so. Not a finding.
- `Patient states neck pain. Wife reports headaches.` and `Patient states headaches. Patient reports neck pain.` are record (two units). Control rows OK.

## Outside my lens

Schema, export ordering and the qualifier-carry logic in `dropped_qualifiers` are not in my lens. The `test_split_llm.py` archive failure noted in r3 was not rerun.

## Exercised

- Read `personas/claims-adjuster.md` in full; `reviews/T-061-claims-adjuster-r3.md` in full; `memory/ORCHESTRATOR_DECISIONS.md` (D-033 :41, D-035 :43, D-037 :45); my memory files (`feedback_review_commit_not_worktree.md`, `feedback_reviews_write_once.md`, `feedback_lexicon_review_method.md`, `project_t061_r3_clause_span_holes.md`).
- `git show --stat 991dac4`; `git show 991dac4 -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py` (full diff read).
- `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm`: `M app/llm/backends/fixture.py`, `M evals/reports/latest.json`, and untracked `evals/reports/2026110*.md`. None of the reviewed files has a diff.
- `git diff --stat 991dac4 HEAD -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py` (empty); `git rev-parse --short HEAD` gives `b614b40`; `git merge-base --is-ancestor 991dac4 HEAD` says 991dac4 is in HEAD.
- `git archive 991dac4 | tar -x -C artifacts/review-evidence/T-061-r4-991` (reviewed object).
- `python3 -m pytest -q tests/unit/test_flags_pass.py` (the brief's literal command) gave `No module named pytest` on the system `python3` (`/opt/homebrew/opt/python@3.12/bin/python3.12`); the project venv is the runner.
- `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider`: live tree `21 passed in 0.36s`; archive `21 passed in 0.36s`.
- `.venv/bin/python research/lexicon_selfcheck.py` in the archive: `[production chip] grounding.has_self_report on 13 no-chip + 5 chip rows: 18/18`; `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115`; `RESULT: PASS`; exit 0.
- `artifacts/review-evidence/T-061-r4-probe.py` in the archive, saved to `artifacts/review-evidence/T-061-r4-probe.txt`: `SUMMARY rows=33 ok=22 miss=11`. The probe calls `grounding.has_self_report` directly (`chip=`) and `flags._flag` (`source_kind=`); both agree on every row.
- `grep -c "wife reports headaches\|wife thinks he is faking\|per wife, headaches since" evals/lexicon_heldout.jsonl` gave 0; `grep -n "Patient states EMS noted\|wife said he was fine\|Patient states his wife" evals/lexicon_heldout.jsonl` gave no output.
- `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` gave 286; `grep -n "set by code from the lexicon" app/llm/lexicon.yaml` gave no hit (the text is at lines 25-26 in the form "code sets source_kind = ..."); `grep -n "read as the patient, which is the clinical convention" app/llm/lexicon.yaml` gave 764; `grep -n "self_report_scope\|exclude_sentence"` gave 85-89.
- `grep -n` on `app/backend/grounding.py` (`_VERB`, `_PATIENT_CLAUSE`, `_FURTHER_CLAUSE`, `patient_report_spans`, `_self_report`, `has_self_report`) and `tests/unit/test_flags_pass.py` (`NO_TAG`, `YES_TAG`, `test_d037_*`) to check every cited line before this write.

```json
{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 991dac4 (T-061 r4, D-037 whole-excerpt patient_report chip: app/backend/grounding.py, tests/unit/test_flags_pass.py, research/lexicon_selfcheck.py), reviewed via git archive at artifacts/review-evidence/T-061-r4-991; HEAD b614b40 has no diff on the reviewed files; specs memory/ORCHESTRATOR_DECISIONS.md D-033 (:41), D-035 (:43), D-037 (:45); no app URL (flag and attribution layer, no UI in scope); probe artifacts/review-evidence/T-061-r4-probe.py -> T-061-r4-probe.txt.",
 "exercised": [
  "Read personas/claims-adjuster.md in full; reviews/T-061-claims-adjuster-r3.md in full; memory/ORCHESTRATOR_DECISIONS.md D-033, D-035, D-037; my memory files",
  "git show --stat 991dac4; git show 991dac4 -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py (full diff)",
  "git status --short on reviewed paths (no diff on reviewed files; fixture.py and evals reports only); git diff --stat 991dac4 HEAD on reviewed files (empty); git rev-parse --short HEAD -> b614b40; git merge-base --is-ancestor 991dac4 HEAD (in HEAD)",
  "git archive 991dac4 extracted to artifacts/review-evidence/T-061-r4-991",
  "python3 -m pytest -q tests/unit/test_flags_pass.py -> No module named pytest (system python3); .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider -> 21 passed (live and archive)",
  ".venv/bin/python research/lexicon_selfcheck.py (archive) -> [production chip] 18/18; held-out 115/115; RESULT: PASS; exit 0",
  "artifacts/review-evidence/T-061-r4-probe.py against the archive -> artifacts/review-evidence/T-061-r4-probe.txt: 33 rows, 22 ok, 11 miss (all 11 chip=True); r3 B1 7/7 and B2 4/4 record; pinned and keep rows as expected",
  "grep of evals/lexicon_heldout.jsonl for family/EMS patient-subject rows -> no output; grep of DECISIONS.md:286 and lexicon.yaml:25-26, 84-93, 764 (stale text)"
 ],
 "verdict": "fail",
 "scores": {"attribution_precision_production": 2, "clause_scope_logic": 2, "b1_b2_closure": 4, "research_gate_measures_production": 3, "test_honesty": 3, "spec_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "D-037 'any further clause means no chip' is implemented as a four-separator list; eleven mixed excerpts still carry the patient chip",
   "evidence": "artifacts/review-evidence/T-061-r4-probe.txt MISS rows: 'Patient states neck pain but his wife reports headaches.', 'Patient states neck pain: wife reports headaches.', 'Patient reports neck pain — EMS notes headaches.', 'Patient states neck pain with his wife reporting headaches.', 'Patient states neck pain while wife says he limps.', 'Patient states neck pain & wife reports headaches.', 'Patient states neck pain / wife reports headaches.', 'Patient states neck pain [wife reports headaches].', 'Patient states neck pain plus wife reports headaches.', 'Patient states neck pain as wife reports headaches.', 'Patient reports neck pain per wife.' all chip=True source_kind=patient_report. Cause: app/backend/grounding.py:187 _FURTHER_CLAUSE = [;,(]|\\band\\b; :196 returns the whole excerpt as the span when it is one unit and matches the patient subject. Control 'Patient states neck pain, but wife reports headaches.' is record.",
   "why_it_matters": "Ten of the eleven rows put a wife, EMS or family clause under the claimant's 'Patient self-report' label. D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) names this a credibility error an adjuster would exploit; D-037 headline says a wrong chip mislabels the source. The research gate PASSes 18/18 on a closed list (research/lexicon_selfcheck.py:172-179) that contains none of these rows, so the PASS does not cover them.",
   "fix": "Closed-grammar rule, not a speaker or verb list: chip only when the text after the patient subject and reporting verb has no clause-introducing punctuation other than the final period (: ; , ( ) [ ] & + em/en dash, and '/' with spaces on both sides; 4/10 and c/o exempt) and no connector from a closed function-word set (and, or, but, with, while, as, plus, per, whereas, though, although, because, which, who, when, if, until, then, nor, yet, than). Write the same set into D-037. If Chris rules the four-separator list complete, record the eleven rows as a documented residual instead.",
   "acceptance_test": "artifacts/review-evidence/T-061-r4-probe.py reports the eleven rows chip=False source_kind=record. The eleven rows are in NO_TAG (tests/unit/test_flags_pass.py:167) and CHIP_NO (research/lexicon_selfcheck.py:172); the selfcheck fails on the pre-fix code and passes after. Kept chipped: 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.', 'Pt reports neck pain 7/10.', 'The patient denies loss of consciousness.', 'Patient states neck pain.' pytest tests/unit/test_flags_pass.py stays green."},
  {"severity": "minor",
   "title": "Held-out set has no patient-subject family or EMS row; the gate's closed row list is why a PASS hides misses (r3 major 3 sub-acceptance and r3 minor 6 carried)",
   "evidence": "grep -n 'Patient states EMS noted\\|wife said he was fine\\|Patient states his wife' evals/lexicon_heldout.jsonl: no output. The r3 finding 1/2 rows sit in research/lexicon_selfcheck.py:172-179 (CHIP_NO/CHIP_YES), not in the held-out file the r3 acceptance named. Gate prints '[production chip] ... 18/18' and RESULT: PASS with eleven probe rows still chipped.",
   "why_it_matters": "A gate PASS on a closed list is the failure r3 finding 3 named. The production call is now in place; the coverage is still one list, and held-out is where a regression would show.",
   "fix": "Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' (expected patient_report) and the r4-new rows (expected record) to evals/lexicon_heldout.jsonl; have the gate check them.",
   "acceptance_test": "grep -c 'wife said he was fine' evals/lexicon_heldout.jsonl >= 1; the gate's production-chip line covers held-out rows, not only the in-script list."},
  {"severity": "minor",
   "title": "Stale text states superseded rules (routed: DECISIONS.md to architect; lexicon.yaml to researcher; D-037 verb set to orchestrator); not failing",
   "evidence": "memory/DECISIONS.md:286 '`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt'; app/llm/lexicon.yaml:25-26 'code sets source_kind = \"patient_report\" from it'; app/llm/lexicon.yaml:84-93 self_report_scope and exclude_sentence still present and unread by production (grounding.py:201-202); app/llm/lexicon.yaml:764 '\"C/O\" and \"complains of\" with no named speaker are read as the patient, which is the clinical convention.' contradicts D-037 'Bare C/O gets no chip' and the no-chip row in tests/unit/test_flags_pass.py:167. _VERB (grounding.py:184-185) includes stated, reported, noted, said, endorsed, denied, described; D-037 names no verbs.",
   "why_it_matters": "A future reader gets two rules, and the lexicon note tells the reader the opposite of what the code does for bare C/O. Not failing, per the round brief.",
   "fix": "Architect amends DECISIONS.md:286; researcher amends lexicon.yaml:25-26 and 764 and removes or marks self_report_scope; orchestrator names the verb set in D-037 or trims _VERB to it.",
   "acceptance_test": "grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md returns nothing; grep -n 'read as the patient, which is the clinical convention' app/llm/lexicon.yaml returns nothing; D-037 lists the verb set used by _VERB."}
 ],
 "whats_right": [
  "The r3 B1 (7/7) and B2 (4/4) rows now return record through the production function, and the pinned 'Pt c/o neck pain; wife drove him in.' is decided record with the test saying so.",
  "The three keep rows (EMS laceration, wife said, wife drove him to the ER) and 'Pt reports neck pain 7/10.' still carry the chip, and the separate-sentence controls fail closed.",
  "research/lexicon_selfcheck.py:162-166 calls app.backend.grounding.has_self_report, so the research gate now measures the production function and no longer reads lexicon self_report entries."
 ],
 "questions_for_chris": [
  "Is D-037's four-separator list (';', ',', 'and', '(') the complete rule, or the examples for 'any further clause'? If complete, the eleven rows are a spec gap to record as residual; I judged against the headline the brief states.",
  "Is 'Patient reports neck pain per wife.' a further clause under D-037? It has no clause and no verb; I count it as a phrase attribution and it is the weakest of the eleven.",
  "This is round 4, past the three-round cap in §7.4 ('max 3 rounds, then decide'). Do you accept the blocker as residual debt with a documented limitation, or does T-061 hold until the closed-grammar fix lands? D-024 item 7 covers harness rounds, not product attribution, so I did not apply it.",
  "Do you accept the closed-grammar connector set (fail-closed on punctuation, closed function words, no speaker or verb list) as the D-037 mechanism, or do you want a different mechanism?"
 ]}
```
