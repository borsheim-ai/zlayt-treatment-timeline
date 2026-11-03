# T-025 Spec reconciliation, round 2: product-manager-reviewer

**Verdict: changes.** 0 blockers, 4 majors, 1 minor. Judged on spec/REQUIREMENTS.md only (qa and architect edits still landing).

r1 status:
- Fixed: authority is stated as golden-wins and no row asks qa to change the golden (REQUIREMENTS:365); `date_invalid` now agrees across REQUIREMENTS:93, :371 and api.md:9,:212; ship bar 4 no longer promises a CONTRACT edit (:329, row 6 closed); R-TL-10(a) cites the ADR-012 token set; rows 1-3 are marked T-028.
- Not fixed: the must-never gate in R-FL-4 still reads M1-M14 (golden has 17); A-106 still contradicts R-EX-4; row 5 is owned by a card that is done and has no AC for it; and the claim that §6 block 2 equals the golden is false at HEAD (the golden export was rewritten 01:04:26Z, after REQUIREMENTS at 01:03:57Z).

Evidence: `artifacts/review-evidence/T-025-pm-r2-probe.py` and `.out.txt`, plus the greps under `exercised`.

```json
{"card": "T-025", "persona": "product-manager-reviewer", "model": "claude-sonnet-5-5",
 "scope": "spec/REQUIREMENTS.md at HEAD (mtime 19:03:57 local = 01:03:57Z), cross-checked against evals/golden/sample.export.expected.txt (01:04:26Z) and sample.expected.json (01:04:46Z), memory/contracts/api.md, memory/DECISIONS.md, memory/ASSUMPTIONS.md, board cards T-014/T-015/T-016/T-028. Round 2 (D-024). No app (M1). Prior review: reviews/T-025-product-manager.md.",
 "exercised": [
  "python3 tools/board.py show T-025 / T-028 / T-014 / T-015 / T-016 (statuses, ACs, handoffs): T-014 done, T-016 done, T-015 in_review, T-028 in_review",
  "grep -n 'authority|golden is|golden wins' spec/REQUIREMENTS.md -> :4 and :365 'Authority rule: evals/golden/* is the authority ... the writer asks qa for no golden changes'",
  "Read spec/REQUIREMENTS.md:336-380 (§8 in full): rows 1-6 and 'Already aligned' paragraph",
  "grep -n 'M1[–-]M\\|must_not' spec/REQUIREMENTS.md -> :68 R-FL-4 'Golden must_not M1–M14 all pass'; :137 R-CO-3 'every must_not item in evals/golden holds (no fixed range)'; grep -n 'M1[–-]M1[0-9]' -> only :68",
  "python3 json load of evals/golden/sample.expected.json -> must_not has 17 ids (M1..M17)",
  "grep -n 'date_invalid|invalid_edit' REQUIREMENTS.md api.md -> REQ:93 and api.md:9,:212 both 422 date_invalid for a non-candidate date",
  "grep -n 'A-106' REQUIREMENTS.md ASSUMPTIONS.md -> REQ:352 'internal notes cite provider + date, not record numbers'; ASSUMPTIONS.md:20 'Internal notes cite record N (provider, date) per REQUIREMENTS R-EX-4'; REQ:376 'A-106 matches R-EX-4 (... record numbers appear only in the internal notes)'; REQ:122 R-EX-4 'record N (<provider as written>, <Month D, YYYY>)'",
  ".venv/bin/python artifacts/review-evidence/T-025-pm-r2-probe.py -> block 0 == golden LETTER_TEXT True; block 1 == golden INTERNAL_NOTES_TEXT False, 3 hunks (AI line, accident-date line, K5 trailing period)",
  "grep -n 'AI assistance|Pending items|Items not reviewed' REQUIREMENTS.md golden export DECISIONS.md api.md -> REQ:273-274 'AI assistance: ... reviewed by the paralegal before export.' + 'Pending items: 0.'; golden :51 and DECISIONS.md:204 'This chronology was drafted with AI assistance; every item ... accepted ... Items not reviewed: 0.'",
  "ls -l mtimes: REQUIREMENTS.md 19:03:57, golden export 19:04:26, sample.expected.json 19:04:46 (local, UTC-6)",
  "grep -c verify_quickly .claude/agents/paralegal-reviewer.md -> 0; board show T-016 -> status done; grep of T-016 card for verify_quickly -> only a reviewer line, no AC",
  "grep -c 'patient_self_report|summary+excerpt' evals/golden/README.md -> 0 (row 4 check already returns 0); grep -c SUMMARY_DROPS_QUALIFIER api.md -> 1 (row 2 check already passes)",
  "grep -n 'D-02[5-9]' memory/ORCHESTRATOR_DECISIONS.md -> no entry beyond D-024, so row 4's 'orchestrator (D-entry)' has no entry yet",
  "grep -n 'R-TL-10' and ship bar 4 (:329) -> ADR-012 token set cited; '(orchestrator to align the wording)' gone; row 6 'closed'"
 ],
 "verdict": "changes",
 "scores": {"ac_met": 3, "reconciliation_accuracy": 3, "scope_discipline": 5, "handoff_clarity": 3, "ship_bar_testability": 4},
 "findings": [
  {"severity": "major",
   "title": "R-FL-4 still gates on a fixed must-never range M1–M14; golden has 17",
   "evidence": "spec/REQUIREMENTS.md:68 (R-FL-4): 'Golden `must_not` M1–M14 all pass (no \"herniation\", ...)'. R-CO-3 at :137 was fixed ('every `must_not` item in `evals/golden` holds (no fixed range)'), so the two rows now disagree. sample.expected.json must_not has 17 ids; M15 (DDD escalation), M16 (swapped laterality) and M17 (non-compliant) are outside M1–M14. `grep -n 'M1[–-]M1[0-9]' spec/REQUIREMENTS.md` returns only :68. The handoff says 'R-FL-4/R-CO-3 gate on every must_not item'; only R-CO-3 does.",
   "why_it_matters": "This was r1 major 3. Read literally, the E2E for R-FL-4 skips the three newest must-nevers, which are the failures that embarrass a paralegal in front of an adjuster. The handoff claims a fix that is only half done.",
   "fix": "R-FL-4: 'every item in the golden `must_not` list passes (no fixed range)'. Keep the parenthetical examples if wanted, marked as examples.",
   "acceptance_test": "`grep -n 'M1[–-]M1[0-9]' spec/REQUIREMENTS.md` returns nothing, and R-FL-4 and R-CO-3 use the same wording."},
  {"severity": "major",
   "title": "A-106 row still says 'not record numbers' while R-EX-4 requires them, and §8 says they match",
   "evidence": "REQUIREMENTS.md:352 (A-106): 'internal notes cite provider + date, not record numbers (matches `memory/ASSUMPTIONS.md`)'. REQUIREMENTS.md:122 (R-EX-4): 'Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`'; the §6 notes use 'record 6 (Capital PT, visit 9, ...)'. ASSUMPTIONS.md:20 was updated to 'Internal notes cite `record N (provider, date)` per REQUIREMENTS R-EX-4', so the parenthetical '(matches ASSUMPTIONS.md)' is now false as well. REQUIREMENTS.md:376 says 'A-106 matches R-EX-4 ... record numbers appear only in the internal notes'. The file contradicts itself between :352 and :122/:376.",
   "why_it_matters": "This was r1 major 1(b). A test writer who reads the assumptions table builds a notes check that forbids `record N`; the R-EX-4 UT requires it. An 'aligned' claim that fails its own grep is the failure AC6 exists to catch.",
   "fix": "Reword :352 to match ASSUMPTIONS.md:20: 'the export cites provider + date; the internal notes cite `record N (provider, date)` (R-EX-4)'. Keep :376 only after `grep -n 'not record numbers' spec/REQUIREMENTS.md` returns nothing.",
   "acceptance_test": "`grep -n 'not record numbers' spec/REQUIREMENTS.md` returns nothing; the A-106 row text and ASSUMPTIONS.md:20 both mention `record N` in the internal notes."},
  {"severity": "major",
   "title": "§8 row 5 is owned by T-016, which is done and has no AC for verify_quickly (AC6 requires an open card)",
   "evidence": "REQUIREMENTS.md:373 row 5: owner 'T-016 (orchestrator)'. `python3 tools/board.py show T-016` -> status \"done\"; a grep of the T-016 card finds no verify_quickly AC. `grep -c verify_quickly .claude/agents/paralegal-reviewer.md` -> 0, so ship bar 5 still can't be read mechanically from the paralegal's output. Row 4 is owned by 'orchestrator (D-entry)' but ORCHESTRATOR_DECISIONS.md ends at D-024, so no entry exists; its own check (`grep patient_self_report|summary+excerpt` on the golden README) already returns 0, so the row is stale and nothing says so.",
   "why_it_matters": "This was r1 major 2, second half. A row with a closed owner and no AC never gets done, and T-017 plans M2/M3 cards from §8. A resolved row left open also hides which differences are real.",
   "fix": "Row 5: name an open card (create one, or add the AC to a card still open), or mark it 'orchestrator, will edit the brief, no card' with a due point. Row 4: mark closed (grep returns 0) or name the D-entry id once written. Mark rows 2 and 3 closed if T-028 passes review (their checks already return the expected results).",
   "acceptance_test": "Every §8 row either names a card whose status is not done and which lists the work as an AC, or is marked closed with a passing grep. `grep -c verify_quickly .claude/agents/paralegal-reviewer.md` is 1 or more before row 5 is closed."},
  {"severity": "major",
   "title": "'§6 block 2 equals the golden notes block' is false at HEAD, and the AI line is on three different texts",
   "evidence": "REQUIREMENTS.md:365: '§6 block 2 equals the golden `INTERNAL_NOTES_TEXT` block'. Probe at HEAD: block 1 == golden notes -> False, 3 hunks. (1) REQ:273-274 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' + 'Pending items: 0.' vs golden export :51 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.' (2) the accident-date bullet: REQ lists records 1 and 2 as 'show treatment on that date' then the record 7 line; golden quotes record 7's line, then record 1's 'rear-ended' sentence, then record 2's header date, 'The tool does not choose between the dates'. (3) a trailing '.' after the K5 quote in REQ. The golden export was written at 19:04:26 local, after REQUIREMENTS (19:03:57). memory/DECISIONS.md:204 quotes the golden wording while calling it 'the fixed text of R-EX-4(1)'; R-EX-4(1) at :122 has the other wording.",
   "why_it_matters": "R-EX-6 requires byte equality with the golden. By §8's own rule the golden wins, so REQUIREMENTS has to change; today the three files carry two AI texts, and the D-017 both-sides quote (the accident-date fix the paralegal asked for) is in the golden but not in the spec the M3 E2E is written from. The cause is qa landing edits after the writer finished, but §8 states an equality as fact and nothing checks it.",
   "fix": "After T-015 lands, re-extract §6 block 2 from the golden and update R-EX-4(1), then add a §8 row: 'diff of §6 blocks against evals/golden/sample.export.expected.txt (expect none)', owner T-025 until clean. Change :365 from 'equals' to 'must equal (row N checks it)'. The orchestrator picks which AI line wins in a D-entry if qa and architect disagree.",
   "acceptance_test": "`.venv/bin/python artifacts/review-evidence/T-025-pm-r2-probe.py` prints '== notes True' for block 1; `grep -n 'AI assistance' spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt` shows one wording."},
  {"severity": "minor",
   "title": "Ship bar 4 and R-TL-4 keep 'today 34' while the file has 40",
   "evidence": "REQUIREMENTS.md:51 and :329 '(today 34, so at least 33)'; `wc -l evals/golden/hallucinations.jsonl` -> 40 (95% of 40 is 38). The rule itself is a rate, so this is illustrative, but r1 asked to drop or mark these parentheticals and they are neither.",
   "why_it_matters": "A reader of the product note will quote '33 of 34' against a report that shows 40 items.",
   "fix": "Replace with '(illustrative: 95% of 34 is 33)' or drop the number.",
   "acceptance_test": "`grep -n 'today 3[0-9]' spec/REQUIREMENTS.md` returns nothing."}
 ],
 "whats_right": [
  "§8 now states one authority rule (golden wins, writer asks qa for nothing), which ends the circular hand-off from r1.",
  "confirm_date uses one code, `date_invalid`, in REQUIREMENTS:93 and api.md:9,:212, and R-RV-3 keeps 409 `needs_confirm` separate from 422.",
  "R-CO-3 and ship bar 4 are rates and 'every item', and the §6 letter block is byte-equal to the golden LETTER_TEXT."
 ],
 "questions_for_chris": []}
```
