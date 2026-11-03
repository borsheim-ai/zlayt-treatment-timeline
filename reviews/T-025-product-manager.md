# T-025 Spec reconciliation: product-manager-reviewer

**Verdict: changes.** 0 blockers, 3 majors, 2 minors.

AC1-AC5 hold on the content. I checked each one with a grep or a probe. Scope stayed mechanical: there were 62 R-IDs before and 62 after, and every new rule traces to D-016..D-022, an ADR, or a T-013 r3 / T-015 r2 finding.

AC6 does not hold. The "Checked and aligned" paragraph in §8 says four things are aligned that are not:
- the confirm_date error code;
- A-106 against R-EX-4;
- the ADR's "single agreed AI line";
- the api.md gap example for a phone note.

The hand-off for the notes block is also circular. REQUIREMENTS names the golden as the authority and asks T-015 to change it. T-015's r3 handoff names REQUIREMENTS as the file that lags and hands it back to T-025. Finally, the must-never gate is still a fixed range, M1–M14. One minute after this commit the golden grew to M1–M17.

Evidence: `artifacts/review-evidence/T-025-pm-probe.py` and its `.out.txt`, plus the commands listed under `exercised`.

```json
{"card": "T-025", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md at 2e92535 (diff b4f3924..2e92535), cross-checked against memory/contracts/api.md and memory/DECISIONS.md (388d5b2), evals/golden at 2e92535 and at HEAD f8c1948, memory/ASSUMPTIONS.md, memory/SCOPE_CUTS.md, memory/ORCHESTRATOR_DECISIONS.md D-016..D-024, board cards T-014/T-015/T-016. No app (M1).",
 "exercised": [
  "python3 tools/board.py show T-025 (AC 1-6 checked, commit 2e92535); show T-014/T-015/T-016/T-017 -> T-014, T-015, T-016 in_review; T-017 ready and depends on T-025",
  "git diff b4f3924..2e92535 -- spec/REQUIREMENTS.md (read in full); git show -s: 388d5b2 18:54:01, 2e92535 18:56:02, f8c1948 18:57:06",
  "AC1: grep -n '19 of the 20\\|19 of 20' spec/REQUIREMENTS.md -> no output; wc -l evals/golden/hallucinations*.jsonl -> 40 and 10 at HEAD; git show 2e92535:evals/golden/hallucinations.jsonl | wc -l -> 34",
  "AC2: sample.expected.json flags -> K1..K5 all level 'must' (at 2e92535 and at HEAD); golden README.md:74 one-to-one plus overlapping evidence matches R-FL-4",
  "AC3: grep -c 'to be supplemented' spec/REQUIREMENTS.md -> 0; probe [1]: the §6 letter block contains none of excludes/supplement/visit count/rate",
  "AC5: grep -o 'D-0[12][0-9]' REQ | uniq -c -> D-016 1, D-017 2, D-018 2, D-019 1, D-020 1, D-021 3, D-022 6; lexicon hedge:true ids via .venv yaml walk -> the same 7 that R-TL-8 lists; DECISIONS.md:119 'Total attempts = 1 + 2 retries' matches R-CO-9",
  "Scope: git show b4f3924:spec/REQUIREMENTS.md R-ID rows -> 62; probe [3] -> 62 defined, only R-RV-7 (withdrawn) cited without a row; non-goal renumbering 12/13/19 matches SCOPE_CUTS.md rows 12, 13 and 19, and no other file references the old numbers (grep)",
  "§8 greps at HEAD: row1 'Pending items: 0' still at golden export :52; row2 api.md count 1; row3 'Known spec mismatches' gone and 'one-to-one' present (resolved by f8c1948); row4 sample.expected.json:638 'patient_self_report'; row5 SUMMARY_DROPS_QUALIFIER in api.md -> 0; row6 verify_quickly in the paralegal agent and persona -> 0",
  "Probe: §6 block 1 == golden LETTER_TEXT -> True; §6 block 2 == golden INTERNAL_NOTES_TEXT -> False (3 hunks: AI line, accident-date conflict line, trailing '.' on the K5 causation quote)",
  "grep date_invalid in api.md -> none (at e442626 it was :208); api.md:212 '422 invalid_edit when ... the date is not one of its candidates'",
  "ASSUMPTIONS.md:20 A-106; DECISIONS.md:204 'single agreed AI line'; reviews/T-013-paralegal-r3.md:77-82 (source of the new AI line)",
  "case_01_date_formats.txt record 8 = 'Dr. Orla Pennywhistle, phone note'; case_01 expected gap_excluded_records [8] vs api.md:205-210 confirm_date example",
  "board/cards/T-015.md:71 handoff; grep of T-014.md/T-016.md for SUMMARY_DROPS/verify_quickly/Pending items/T-025 -> no hits"
 ],
 "verdict": "changes",
 "scores": {"ac_met": 3, "reconciliation_accuracy": 2, "scope_discipline": 5, "handoff_clarity": 2, "ship_bar_testability": 4},
 "findings": [
  {"severity": "major",
   "title": "§8 'Checked and aligned' claims four alignments that the files contradict, so AC6 is not met",
   "evidence": "(a) REQ R-RV-2: 'a date that is not one of the code-proposed readings → 422 `date_invalid`'. §8 says 'api.md ... uses ... `422 date_invalid` for a non-candidate date'. But api.md:212 (last changed 388d5b2, 2 min before 2e92535) says '`422 invalid_edit` when the record's date is not ambiguous, or the date is not one of its candidates', and grep date_invalid api.md finds nothing. The two files have swapped sides since T-013 r3. (b) ASSUMPTIONS.md:20 and REQ's own A-106 row say 'Internal notes cite provider + date, not record numbers'. R-EX-4 says 'Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`', and §6 uses 'record 6 (Capital PT, visit 9, ...)'. §8 says 'A-106 matches R-EX-4'. (c) DECISIONS.md:204 fixes 'the single agreed AI line `AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.`'. R-EX-4(1) replaces it. §8 rows 1-2 list the golden and api.md, not the ADR. (d) api.md:205-210: the confirm_date example on case_01 record 8 returns a new gap flag `f_gap_r7_r8` of 40 days. Record 8 is a phone note (case_01 .txt:40; gap_excluded_records [8]), and R-IN-5 says 'The gap table is unchanged'. This is not in §8.",
   "why_it_matters": "§8 is the contract that T-017 uses to plan M2/M3 cards. An item marked aligned gets no owner, so a backend worker who follows api.md and a test writer who follows REQ will build confirm_date errors, note citations and the AI line two different ways. A claim that a check was done when it wasn't is worse than leaving the row open.",
   "fix": "Re-run the greps at the current api.md/DECISIONS commit. Move (a)-(d) into the §8 table with a grep and an owner: (a) and (d) to T-014 r3; (c) to T-014 r3, or to a D-entry if the new line wins. For (b), either reword A-106 to 'provider + date, with a record number in the internal notes' or drop record numbers from R-EX-4, and record which one in a D-entry. Delete each claim from 'Checked and aligned' until its grep proves it.",
   "acceptance_test": "Each sentence in 'Checked and aligned' has a grep that returns the stated result at the cited commit. `grep -n date_invalid memory/contracts/api.md spec/REQUIREMENTS.md` shows the same code in both files, or §8 lists the difference. A-106 and R-EX-4 no longer contradict each other on record numbers."},
  {"severity": "major",
   "title": "The internal-notes reconciliation is circular, and the named owner cards don't carry the work",
   "evidence": "REQ:3: 'Authority: golden outputs are `evals/golden/` (qa, T-015)'. §8 row 1: the golden must re-extract §6 block 2, owner 'T-015 r3 (qa)'. board/cards/T-015.md:71 (T-015 r3 handoff, f8c1948): 'Left: REQUIREMENTS lag is writer T-025 (golden is authority).' At HEAD the probe still shows §6 block 2 != golden INTERNAL_NOTES_TEXT, with 3 hunks: the AI line, the accident-date conflict line (golden still describes records 1 and 2 in tool wording instead of quoting both sides per D-017), and a trailing '.' after the K5 quote. Rows 2, 5 and 6 name T-014 r3 and T-016, but a grep of T-014.md and T-016.md for SUMMARY_DROPS / verify_quickly / 'Pending items' / T-025 finds nothing, and T-016's AC 1-2 are already checked.",
   "why_it_matters": "Each side says the other is the authority, so neither one moves. R-EX-6 requires byte equality with the golden notes block, which means the M3 E2E fails whichever text the code follows. D-017's both-sides quote, the accident-date fix the paralegal asked for, exists only in REQ. Ship-bar item 5 can't be read mechanically until verify_quickly reaches the paralegal brief, and the card named for that has no AC for it.",
   "fix": "Orchestrator: record one D-entry that decides the notes block (REQ §6 block 2 wins, per T-013 paralegal r3 and D-017), and change REQ:3 to say that §6 is authoritative for the export text. Then add each open §8 row as an AC on its owner card (T-014: rows 2 and 5; T-015: rows 1 and 4; T-016: row 6) so that the card can't close without it.",
   "acceptance_test": "`python3 tools/board.py show T-014|T-015|T-016` each lists the §8 row(s) as an AC. A D-entry names which file wins for the notes block. After the owner cards close, the probe reports §6 block 2 == golden INTERNAL_NOTES_TEXT."},
  {"severity": "major",
   "title": "The must-never gate is still a fixed range (M1–M14) that the golden has already outgrown",
   "evidence": "R-FL-4: 'Golden `must_not` M1–M14 all pass'. R-CO-3: 'the golden `must_not` list M1–M14 holds'. REQ: 'Pass/fail wording is literal.' Golden sample.expected.json at f8c1948 (64 s after 2e92535) has M1–M17. The three new items are M15 'Escalates degenerative change into a disease or diagnosis (DDD)', M16 'Swaps laterality' and M17 'Labels the patient non-compliant'. R-TL-4 and ship bar 4 also still read 'today 34, so at least 33', but the file now has 40.",
   "why_it_matters": "AC1 fixed this exact pattern for hallucinations by turning the count into a rate. The must-never list is the most important gate, and it kept a range. Read literally, the M3 gate skips the three new must-nevers, and those are the ways this tool would embarrass a paralegal in front of an adjuster (DDD from a hedge, a wrong-side arm, 'non-compliant').",
   "fix": "R-FL-4 and R-CO-3: 'every item in the golden `must_not` list (today M1–M17) passes'. Drop the 'today N' parentheticals or mark them illustrative only, so the rule doesn't depend on keeping them current.",
   "acceptance_test": "`grep -n 'M1–M1[0-9]' spec/REQUIREMENTS.md` returns only lines that also say 'every item'. The gate text names no upper bound."},
  {"severity": "minor",
   "title": "§8 row 7 has no card, and ship bar 4 contradicts it",
   "evidence": "§8 row 7: owner 'orchestrator', check 'none (noted only)', 'CONTRACT is never edited'. Ship bar 4: 'CONTRACT §5 M2 still says \"qa injects 20\"; the rate governs (orchestrator to align the wording)'. The brief requires every open row to name an open card.",
   "why_it_matters": "One line promises an alignment and the other rules it out. A reader of the product note can't tell whether 20 or the rate is the bar.",
   "fix": "Mark row 7 as 'closed: permanent; the product note quotes the rate' and remove '(orchestrator to align the wording)' from ship bar 4.",
   "acceptance_test": "Every §8 row either names an open card id or is marked closed with a reason. Ship bar 4 no longer promises a CONTRACT edit."},
  {"severity": "minor",
   "title": "R-TL-10(a) defines a smaller token set than the ADR it reconciles to",
   "evidence": "REQ R-TL-10(a): 'the word left, right, no, not or without'. DECISIONS.md:241: 'numerals and number words (normalised: \"two\" = 2), percentages, scores like 6/10 ... (left, right, bilateral, no, not, without, negative)'.",
   "why_it_matters": "There are now two definitions of one code check. A UT written from REQ won't cover 'bilateral', 'negative' or 'two', so a summary that turns 'two missed appointments' into 'three' passes the REQ test.",
   "fix": "R-TL-10(a): 'the tokens of `grounding.new_tokens` (ADR, DECISIONS.md:241)', with the closed list copied in or cited.",
   "acceptance_test": "The R-TL-10 UT includes a number-word case and a 'bilateral' or 'negative' case."}
 ],
 "whats_right": [
  "Ship bar 4 and R-TL-4 are now rates over the whole file, so the bar can't weaken as the golden grows.",
  "K1–K5 are all 'must', with one-to-one matching on overlapping evidence, and the golden README:74 agrees, so a single record-7 flag can't hide the wrong intake date.",
  "Scope stayed mechanical: 62 R-IDs before and after, non-goals renumbered to match SCOPE_CUTS 1:1, and the letter block is byte-equal to the golden."
 ],
 "questions_for_chris": []}
```
