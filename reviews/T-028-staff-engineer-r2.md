# Review T-028 round 2 (staff-engineer-reviewer): ADR consistency pass

Verdict: **changes** (0 blockers, 1 major, 3 minors carried or new, 2 nits). Commit reviewed: 10cffcd (architect r2), on top of 3ff15cd (spec R-EX-4(1) AI line) and HEAD 1e675ea. The four in-scope docs are clean in git status (only the agent-memory and board files show as modified).

Round 1 status:
- **Blocker (AI line) is closed.** The three places that carried the disputed line now carry the golden wording, byte for byte, as C1 shows. The spec change came in 3ff15cd; DECISIONS:204 already carried the golden text in de749c2. My round-1 blocker is stale, as the orchestrator triage said.
- **Major (api.md mg. split) is closed.** api.md:91 is one unit [477,532) and matches the R-TL-2 splitter and sample.txt offsets exactly.
- **Major (per-category templates) is closed at design level.** ADR-013 has a template row for all 13 lexicon v2 categories, plus the conflict, gap and record_warning codes. Two new minors come out of the table itself (F2, F3).
- **Major (spec §8 row 1 vs the export example) is re-filed as F1.** The row was rewritten to a filename grep; the content check it now relies on does not exist.
- **Minors carried, still open:** F4 (README-arch v1 names), F5 (confirm_date warning vs golden), F6 (unreproducible "14/14, 17/17" count). Nit F7 (D-id wording) was not re-checked this round.

Correction to my round-1 evidence: `artifacts/review-evidence/T-028-review-checks.py` had two defects. AC4b compared api.md against a hand-typed constant `[(477,532)]` while its span filter also caught the 533-552 unit, so it could not pass; the splitter and api.md agreed. AC5 searched for the pre-3ff15cd R-EX-4(1) wording. I retract those two FAIL lines. The corrected checks are in `artifacts/review-evidence/T-028-r2-checks.py`.

Mechanical results: `artifacts/review-evidence/T-028-r2-checks.py` prints 7/12 PASS. The five FAILs are F2 (C2c, C2d), F4 (C6), F5 (C7), F6 (C8). F1 is not a script FAIL because the spec row passes its own weakened check (C5); that is the problem.

Evidence excerpts:

```
$ grep -n "drafted with AI assistance" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt
spec/REQUIREMENTS.md:122:... (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." ...
spec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
memory/DECISIONS.md:204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); ...
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
EXIT=0

$ grep -n "sample.export.expected.txt" memory/contracts/api.md
267:Built by code from items ... **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** ...
272:  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries ... full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges stated in these records: $8,390.00",
EXIT=0

$ .venv/bin/python -I -c "...sample[477:532]..." (run on evals/golden/sample.txt)
sample[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'
api unit text present: True | sample span equals unit: True | old split present in api.md: False

$ .venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py
PASS C1 AI line: same canonical sentence in spec, DECISIONS, LLM_VS_CODE and golden; no old variant
PASS C2a every lexicon v2 category has a template-table row in ADR-013
    lexicon categories: 13; rows in table: 21
    lexicon categories whose explanation is blank or n/a: ['recovery_context']
PASS C2b every conflict, gap and record_warning code named in ADR-013 has a row
FAIL C2c every placeholder in the template table is declared in the slot legend
    used but not declared: ['date A', 'date B', 'provider A', 'provider B', 'quote A', 'quote B', 'raw', 'stated']
FAIL C2d the example template under the table uses the same slot names as the table
    example slots: ['date', 'excerpt', 'source']
PASS C3a api.md record 2 sentences equal the R-TL-2 splitter output on sample record 2
PASS C3b each api.md sentence text equals sample.txt[start:end] exactly
PASS C4 api.md references evals/golden/sample.export.expected.txt (grep count >= 1)
PASS C5 spec section 8 row 1 check is 'expect >= 1' (not 'expect none') and api.md satisfies it
FAIL C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys
    names on that line not in lexicon v2 categories or code_lists keys: ['causation_weakening', 'compliance', 'hedge']
FAIL C7 api.md confirm_date removed_flag_ids (f_warn_date_r8) has a matching golden expectation
    golden case_01 record_warnings for record 8: []
FAIL C8 card AC3 evidence '14/14 blocks, 17/17 offsets' appears in a checked-in script or doc
    matches for 14/14 or 17/17 in the four docs: 0
SUMMARY: 7/12 checks passed
EXIT=1
```

## Findings

**F1 (major, new this round): the spec §8 row 1 check is a filename grep, and the content test it now relies on does not exist.** The orchestrator rewrote row 1 from "diff against golden, expect none" to a grep (`grep -n "sample.export.expected.txt" memory/contracts/api.md`, expect ≥ 1). That makes the row pass whether or not the export's notes block equals the golden block. The api.md:267 sentence says "a pytest compares real output with it", but no such pytest exists: `.venv/bin/python -m pytest tests/unit -q` prints "no tests ran in 0.00s" and exits 5, and `grep -rl "sample.export.expected" tests app | wc -l` prints 0. Round-1 fix option A asked for the row to name the test; the row names a grep instead. The golden is the authority (spec §8), and nothing checks it.

**F2 (minor, new): slot names in the ADR-013 template table do not match the slot legend or the example.** DECISIONS.md:258 declares `{date}`, `{provider}`, `{quote}`, `{days}`, `{a}`/`{b}`. The rows use `{date A}`, `{provider A}`, `{quote A}`, `{date B}`, `{provider B}`, `{quote B}` (lines 262 onward), `{stated}` (263) and `{raw}` (281). The example at DECISIONS.md:285 uses `{source}`, `{date}`, `{excerpt}`. A renderer built from the legend would raise on the table's keys, or the implementer would pick one set and the other would drift. Design text only, nothing built yet, so minor.

**F3 (minor, new): recovery_context has no explanation template, but the text says every category has one.** DECISIONS.md:279 `| recovery_context | (context only, never raises a flag) | n/a |`, against DECISIONS.md:285 "a unit test asserts every category has one". As written, the test either fails on recovery_context or needs an unstated exception. State the exception: categories with strength `low` are never rendered and have no explanation template; the test asserts a template for every other category.

**F4 (minor, carried from r1, open): README-arch lexicon line lists v1 names.** app/README-arch.md:36 reads `lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection`. Lexicon v2 has none of `causation_weakening`, `compliance` or `hedge` as categories (C6 output above). Fix: rewrite the line as the 13 v2 names plus the 4 code_lists keys, with a pointer to ADR-013.

**F5 (minor, carried from r1, open): confirm_date example removes a warning the golden does not expect.** api.md:209 `"removed_flag_ids": ["f_warn_date_r8"]`. Golden case_01 record 8 (`{"record_no": 8, "raw_date": "04/05/2026", "date": null, "kind": "phone_note", ...}` at line 65) has `"record_warnings": []` at line 315, and the golden description says the ambiguous date "must be marked ambiguous ... and surfaced for review", which no expected value checks. Either the golden lacks the expectation or the example names a flag the pipeline is not required to create. The gap example itself (`gap_flags: []`) is correct. Fix as r1: qa adds the date_ambiguous expectation, or the architect writes `removed_flag_ids: []` and records which wins.

**F6 (minor, carried from r1, open): the AC3 evidence count is not reproducible.** Card T-028 AC3 evidence and the Handoff both say "check script 14/14 blocks, 17/17 offsets". `grep -rn '14/14\|17/17' memory/ docs/ app/ evals/ tools/` returns nothing (C8: 0). Check the script into artifacts/review-evidence/ and quote its output.

**F7 (nit, carried from r1, not re-checked): card AC4 "D-001..D-024 in all three docs" overstates the citations.** The r1 counts stand; every cited id resolves.

**F8 (nit, new): spec §8 row 1 has six cells under a five-column header.** spec/REQUIREMENTS.md row 1 ends `| T-028 | resolved |` after the Owner column. Move the status into the Difference cell or add a column.

## Exercised

- `personas/staff-engineer.md` read in full; `reviews/T-028-staff-engineer.md` (r1) read in full; `.claude/agent-memory/staff-engineer-reviewer/MEMORY.md` read.
- `git log --oneline -5`; `git show --stat 10cffcd`; `git show 10cffcd -- memory/DECISIONS.md memory/contracts/api.md` (full diff read); `git log --oneline de749c2..HEAD -- <four docs, spec, golden>`.
- `grep -n "drafted with AI assistance" ...` and `grep -n "AI assistance" ...` over spec, DECISIONS, LLM_VS_CODE, api.md, golden (outputs quoted above).
- `.venv/bin/python -I` lexicon load: version 2, 66 entries, 13 distinct categories; code_lists keys `accident_date_phrases, damages, injection, non_encounter`.
- DECISIONS.md ADR-013 lines 246-296 read; template table counted: 21 rows; 13 of 13 lexicon categories have a row.
- api.md:86-92 record 2 sentences; `sample.txt[477:532]` literal check; `grep -n "sample.export.expected.txt" memory/contracts/api.md` (lines 267, 272); `grep -n "removed_flag_ids"` (209); `grep -n "internal_notes_text"` (273).
- spec/REQUIREMENTS.md section 8 rows 1-5 (current text).
- `artifacts/review-evidence/T-028-review-checks.py` (round 1, now with two known defects) and `artifacts/review-evidence/T-028-r2-checks.py` (new, 12 checks, 7/12).
- `evals/golden/check_golden.py` → "golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered", exit 0.
- `evals/golden/case_01_date_formats.expected.json`: top-level keys, record 8 (line 65), `record_warnings` (line 315).
- `.venv/bin/python -m pytest tests/unit -q` → "no tests ran in 0.00s", exit 5. `grep -rl sample.export.expected tests app` → 0 files.
- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` → "No module named app.pipeline", exit 1. Not runnable at this commit; no app URL exists (`ls -A app/backend` empty).
- `python3 tools/board.py show T-028` (in_review, 4 ACs, notes, handoff) and `python3 tools/board.py validate` → "ok (28 file(s))", exit 0 (before this file was written).
- `app/README-arch.md:36` read.

## What is right

- The mg. sentence is one unit in api.md:91 (477-532), equal to the R-TL-2 splitter output and to sample.txt[477:532] (C3a, C3b).
- ADR-013 has one template row per lexicon v2 category plus each conflict, gap and record_warning code, and the text is code-rendered with no model text in it (C2a, C2b).
- The AI disclosure sentence is identical in spec R-EX-4(1) and §6, DECISIONS:204, LLM_VS_CODE:103 and the golden file (C1); the round-1 blocker is closed.

```json
{"card": "T-028", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git 10cffcd (architect r2) on HEAD 1e675ea; four docs memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; spec/REQUIREMENTS.md (3ff15cd, section 8 row 1 rewritten by orchestrator) and evals/golden at HEAD; no app URL (app/backend empty, no app.pipeline); sample case evals/golden/sample.txt",
 "exercised": [
   "read personas/staff-engineer.md in full; read reviews/T-028-staff-engineer.md (round 1) and the agent memory index",
   "git show --stat 10cffcd; git show 10cffcd -- memory/DECISIONS.md memory/contracts/api.md (full diff); git log --oneline de749c2..HEAD over the in-scope files",
   "grep -n \"drafted with AI assistance\" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt -> spec:122, spec:273, DECISIONS:204, golden:51, all the same sentence (N or 0 for the count), EXIT=0",
   "grep -n \"AI assistance\" across spec, DECISIONS, LLM_VS_CODE, api.md, golden -> one canonical line each; no R-EX-4(1) old variant anywhere",
   ".venv/bin/python -I lexicon load: version 2, 66 entries, 13 distinct categories; code_lists keys accident_date_phrases, damages, injection, non_encounter",
   "read memory/DECISIONS.md ADR-013 (lines 246-296): template table has 21 rows; all 13 lexicon categories have a row; recovery_context explanation is n/a",
   "api.md:86-92 record 2 sentences vs sample.txt[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.' ; artifacts/review-evidence/T-028-r2-checks.py C3a/C3b PASS",
   "grep -n \"sample.export.expected.txt\" memory/contracts/api.md -> lines 267, 272",
   "read spec/REQUIREMENTS.md section 8 rows 1-5 (row 1 now 'grep ... expect >= 1')",
   "artifacts/review-evidence/T-028-review-checks.py (round 1) rerun: 8/12; two round-1 defects identified and retracted (AC4b constant, AC5 stale wording)",
   "artifacts/review-evidence/T-028-r2-checks.py (new): 7/12 PASS; FAILs C2c, C2d, C6, C7, C8",
   "evals/golden/check_golden.py -> golden OK, exit 0",
   "evals/golden/case_01_date_formats.expected.json: record 8 (line 65, raw_date 04/05/2026, date null, phone_note), record_warnings [] (line 315), gap_excluded_records [8]",
   ".venv/bin/python -m pytest tests/unit -q -> 'no tests ran in 0.00s', exit 5; grep -rl sample.export.expected tests app -> 0 files",
   ".venv/bin/python -m app.pipeline evals/golden/sample.txt -> 'No module named app.pipeline', exit 1; ls -A app/backend -> empty",
   "grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches (C8: 0)",
   "app/README-arch.md:36 read; lexicon v2 names compared (causation_weakening, compliance, hedge not categories)",
   "python3 tools/board.py show T-028 -> in_review, 4 ACs, notes and handoff read (claims not trusted)",
   "python3 tools/board.py validate -> ok (28 file(s)), exit 0"
 ],
 "verdict": "changes",
 "scores": {"AI_line_matches_R-EX-4_1": 5, "mg_unit_matches_splitter_and_D-021": 5, "ADR013_template_per_lexicon_category": 4, "ADR013_slot_keys_consistent": 2, "spec_section8_row1_testable": 2, "golden_vs_confirm_date_example": 2, "evidence_reproducible": 2, "evidence_honesty": 3},
 "findings": [
  {"severity": "major",
   "title": "spec section 8 row 1 is checked by a filename grep; the golden-equality test it depends on does not exist",
   "evidence": "spec/REQUIREMENTS.md section 8 row 1: `grep -n \"sample.export.expected.txt\" memory/contracts/api.md` (expect ≥ 1). memory/contracts/api.md:267: 'a pytest compares real output with it'. Repro: `.venv/bin/python -m pytest tests/unit -q` -> 'no tests ran in 0.00s', exit 5; `grep -rl sample.export.expected tests app | wc -l` -> 0.",
   "why_it_matters": "The golden notes and letter blocks are the authority (spec section 8). With this row, the spec check passes whether or not the export's internal_notes_text equals the golden block, so the disclosure text and the flag lists in the notes could drift from the golden with no failing check. The round-1 fix asked for the row to name a test; the row now names a grep.",
   "fix": "Build the export golden test on the export card (the one that assembles letter_text and internal_notes_text). Point spec section 8 row 1 at that test id, not at a grep for a filename. Keep the api.md pointer.",
   "acceptance_test": "A pytest (proposed id tests/unit/test_export_golden.py::test_blocks_equal_golden) builds the export from the sample accepted set and asserts both blocks equal evals/golden/sample.export.expected.txt byte for byte; spec row 1 check names that id; mutating one line of the notes block in the export code makes the test fail."},
  {"severity": "minor",
   "title": "ADR-013 template table uses slot names that the slot legend and the example do not declare",
   "evidence": "memory/DECISIONS.md:258 legend: `{date}`, `{provider}`, `{quote}`, `{days}`, `{a}`/`{b}`. Rows use {date A}, {provider A}, {quote A}, {date B}, {provider B}, {quote B} (from line 262), {stated} (line 263), {raw} (line 281). Example at memory/DECISIONS.md:285 uses {source}, {date}, {excerpt}. Repro: `.venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py` -> C2c FAIL, C2d FAIL.",
   "why_it_matters": "The table is the code-rendered template set the flag rule depends on (LLM_VS_CODE row 14). If the legend and the rows disagree, the renderer and its unit test will disagree on keys, and a template could emit literal braces in a flag the paralegal reads.",
   "fix": "Pick one slot set. Declare every slot used in the table, including stated and raw, in the legend; rename the example's slots to match. Add the slot list as a column or a line per row.",
   "acceptance_test": "The unit test that asserts one template per category also asserts every placeholder in each template is in the declared slot set; the r2 script C2c and C2d PASS."},
  {"severity": "minor",
   "title": "recovery_context has no explanation template, but the ADR says every category has one and a unit test asserts it",
   "evidence": "memory/DECISIONS.md:279: `| recovery_context | (context only, never raises a flag) | n/a |`. memory/DECISIONS.md:285: 'a unit test asserts every category has one'.",
   "why_it_matters": "As written, the stated test either fails on recovery_context or needs an exception nobody has written down. An implementer will pick one of these silently.",
   "fix": "State the exception in ADR-013: categories with strength low are never rendered and have no explanation template; the unit test asserts a template for every other category.",
   "acceptance_test": "The unit test lists the strength-low categories explicitly and asserts a template for every other category in the lexicon v2 list."},
  {"severity": "minor",
   "title": "README-arch lexicon line lists category names that lexicon v2 does not contain (carried from r1)",
   "evidence": "app/README-arch.md:36: 'lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection'. Repro: `.venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py` -> C6 FAIL: causation_weakening, compliance, hedge.",
   "why_it_matters": "A backend worker reading the architecture map would look for categories that do not exist in app/llm/lexicon.yaml.",
   "fix": "Rewrite README-arch.md:36 as the 13 lexicon v2 category names and the 4 code_lists keys, with a pointer to ADR-013.",
   "acceptance_test": "C6 PASS: every name on the README-arch lexicon line is a lexicon v2 category or a code_lists key."},
  {"severity": "minor",
   "title": "confirm_date example removes a date_ambiguous warning the golden does not expect (carried from r1)",
   "evidence": "memory/contracts/api.md:209: `\"removed_flag_ids\": [\"f_warn_date_r8\"]`. evals/golden/case_01_date_formats.expected.json:315 `\"record_warnings\": []`; record 8 at line 65 (`\"raw_date\": \"04/05/2026\", \"date\": null`). Golden description: 'Ambiguous date must be marked ambiguous, excluded from gap math, and surfaced for review'; only the exclusion is expected. Repro: C7 FAIL.",
   "why_it_matters": "The golden is the stated authority for expected outputs. Either the golden is missing the date_ambiguous expectation the description states, or the example names a warning the pipeline is not required to create. The gap example is correct; this one id is the problem.",
   "fix": "qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden; or the architect writes `removed_flag_ids: []` and records which of the two wins.",
   "acceptance_test": "check_golden.py asserts the record 8 warning if qa adds it, or the api example removes the id and C7 is retired."},
  {"severity": "minor",
   "title": "the AC3 evidence count '14/14 blocks, 17/17 offsets' is not produced by any checked-in script (carried from r1)",
   "evidence": "Card T-028 AC3 evidence and Handoff: 'check script 14/14 blocks, 17/17 offsets'. Repro: `grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/` -> no matches (C8: 0 matches in the four docs).",
   "why_it_matters": "The card's evidence cannot be re-run by the next reviewer, so the claim rests on a hand count.",
   "fix": "Check the offset and block script into artifacts/review-evidence/ and quote its output in the card.",
   "acceptance_test": "`.venv/bin/python -I artifacts/review-evidence/<script>.py` exits 0 and prints the counts quoted in the card."},
  {"severity": "nit",
   "title": "spec section 8 row 1 has six cells under a five-column header (new)",
   "evidence": "spec/REQUIREMENTS.md section 8, row 1: `| 1 | ... | T-028 | resolved |` after the Owner column.",
   "why_it_matters": "Markdown renders the status as a stray cell; the next editor may read it as an owner.",
   "fix": "Move 'resolved' into the Difference cell or add a Status column to the table.",
   "acceptance_test": "Each row of the section 8 table has five cells."},
  {"severity": "nit",
   "title": "card AC4 evidence 'D-001..D-024 in all three docs' overstates the citations (carried from r1, not re-checked this round)",
   "evidence": "Card T-028 AC4 evidence. Round-1 count: DECISIONS.md 22 distinct D-ids, api.md 8, LLM_VS_CODE.md 2; every cited id resolves.",
   "why_it_matters": "The substance passes; the evidence sentence does not describe the files.",
   "fix": "Restate as 'every D-id cited in the four docs resolves to a row in ORCHESTRATOR_DECISIONS (D-001..D-024)'.",
   "acceptance_test": "The r1 AC8 check (every cited D-id defined) continues to pass."}
 ],
 "whats_right": [
   "The mg. sentence is one unit in api.md:91 (477-532), equal to the R-TL-2 splitter output and to sample.txt[477:532] (C3a, C3b).",
   "ADR-013 has one template row for each of the 13 lexicon v2 categories and for each conflict, gap and record_warning code; the text is code-rendered.",
   "The AI disclosure sentence is identical in spec R-EX-4(1), spec section 6, DECISIONS.md:204, LLM_VS_CODE.md:103 and the golden file (C1); the round-1 blocker is closed."
 ],
 "questions_for_chris": [
   "Is the golden wording the canonical AI line? After 3ff15cd, spec R-EX-4(1), section 6, DECISIONS:204, LLM_VS_CODE:103 and golden:51 all carry it, which closes the round-1 blocker on that reading. Confirm, or name the other wording.",
   "D-024 puts Tier-1 card reviews on sonnet. This review ran as claude-haiku-5-5, as in round 1. Accept haiku for doc-only consistency passes, or re-run on sonnet before the gate?",
   "Should the golden export test (F1) be assigned to a card now? tests/unit is empty at M1, so the spec row has nothing to point at until one exists."
 ]}
```
