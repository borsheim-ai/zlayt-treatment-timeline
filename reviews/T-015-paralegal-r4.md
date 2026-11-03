# T-015 round 4: paralegal-reviewer mechanical re-check (after commit 0c03c4f, HEAD 65537a4)

**Verdict: changes** (0 blockers, 1 major, 1 minor).

The r3 blocker and the r3 span-key major are resolved on the output. The r3 AI-line major is only partly resolved. The golden AI line now matches REQUIREMENTS §6 byte for byte, but REQUIREMENTS R-EX-4(1), the normative text, still says something different. The r3 review also quoted an R-EX-4(1) string that is not in the spec file.

Resolved on the output:
- **r3 blocker (accident-date bullet).** Export line 55 quotes record 7's intake line and record 1's "rear-ended" sentence, and says "The tool does not choose between the dates." Deleting the record-1 quote makes check_golden.py exit 1 (mutation M2).
- **r3 major (self-report key).** All 10 self-report entries use `self_report_spans`. None use `spans`. An objective span under that key exits 1 (M1), and a renamed key exits 1 (M3).
- **r3 minor (K3 flag).** K3 now has `subtype: patient_reported_onset` and `source_kind: patient_report`. The `patient_self_report` string is gone from the golden.
- **r3 major (notes block), partial.** The golden notes block is byte-identical to REQUIREMENTS §6 block 2. The stale "Pending items: 0." line and the stray period are gone. The README "authority where REQUIREMENTS lags" sentence is gone. The AI-line mismatch with R-EX-4(1) remains (finding 1).

Probe script: `artifacts/review-evidence/T-015-r4-paralegal-recheck.py`. Output: `artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt`.

Commands and outputs (verbatim):
- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered` EXIT=0
- `grep -n "Conflict, accident date" evals/golden/sample.export.expected.txt` → line 55 contains `"Date of accident per intake form: 2026-01-19."` and `"41M restrained driver, rear-ended at approx. 35 mph."` and `The tool does not choose between the dates.` (record 1 source: sample.txt:6, record 7 source: sample.txt:36)
- `grep -rn "self_report_spans\|patient_self_report\|patient_report" evals/golden | head` → 10 `self_report_spans` hits (case_01:175, case_06:74/120/157, sample:109/272, plus check_golden and README); `patient_self_report` no hit; `sample.expected.json:638-639` = `patient_reported_onset` / `patient_report`. `grep -rhoE '"[a-z_]*spans"' evals/golden` → `10 "self_report_spans"`, no other key.
- `grep -n "Pending items" evals/golden/sample.export.expected.txt` → no match (rc=1)
- `grep -n "Items not reviewed: 0\." evals/golden/sample.export.expected.txt` → `51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.`
- `grep -n "Items not reviewed" spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt` → `spec/REQUIREMENTS.md:273:` (identical sentence) and `evals/golden/sample.export.expected.txt:51:` (identical). The §6 line equals the golden AI line.
- Probe Part A: `notes (block 2): identical=True`. `letter (block 1)`: body identical; the only differences are the golden's `=== LETTER_TEXT ===` and `=== INTERNAL_NOTES_TEXT ===` delimiter lines.
- Probe Part A: `R-EX-4(1) fixed text present verbatim in REQUIREMENTS: True`; `golden AI line equals R-EX-4(1) fixed text: False`. `spec/REQUIREMENTS.md:122` R-EX-4(1) reads `AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.` followed by `Pending items: N.`. R-EX-4(11) reads `Pending items not included.`
- Probe Part B (scratch copy, real files untouched): base exit=0; M1 objective span under self_report_spans exit=1 (`E1: self_report span: objective/assessment content: Alert and oriented`); M2 drop record-1 quote exit=1; M3 renamed key exit=1 (`unknown entry keys ['spans']`); M4 `Pending items: 0.` in notes exit=1.
- `git status --porcelain evals/golden spec` → empty. `git log --oneline -3` → `65537a4`, `0c03c4f`, `4cc0f81`.
- `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md evals/golden/sample.expected.json` → no match (rc=1).
- `grep -n "no physician" evals/golden/sample.expected.json` → line 1014 only.

Not re-run this round: the r3 K4/K5 matcher probe and the r3 nurse probe. Their r3 minors are not re-tested here.

Model note: this review was run as claude-haiku-5-5. The dossier's expected id (claude-opus-5-5) does not match the runtime model, so the id is recorded as observed.

```json
{"card": "T-015", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 4 re-check after commit 0c03c4f (HEAD 65537a4). Files: evals/golden/check_golden.py, sample.export.expected.txt, sample.expected.json, case_01 and case_06 expected.json, README.md; spec/REQUIREMENTS.md R-EX-4(1), R-EX-4(11), section 6 blocks 1-2, section 8 row 4. No app (pre-code eval data). Sample case evals/golden/sample.txt. Prior rounds: reviews/T-015-paralegal-r3.md, reviews/T-015-legal-nurse-r3.md.",
 "exercised": [
  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
  "grep accident-date bullet in sample.export.expected.txt (line 55 quotes intake line and record 1 'rear-ended at approx. 35 mph'; 'does not choose' present); record sources sample.txt:6 and :36",
  "grep -rn self_report_spans|patient_self_report|patient_report evals/golden; grep -rhoE '\"[a-z_]*spans\"' evals/golden -> 10 self_report_spans, 0 spans, 0 patient_self_report",
  "grep 'Pending items' export -> absent; grep 'Items not reviewed' spec/REQUIREMENTS.md and export -> identical line at REQUIREMENTS.md:273 and export:51",
  "grep -n 'AI assistance' R-EX-4(1) at spec/REQUIREMENTS.md:122 and R-EX-4(11)",
  "artifacts/review-evidence/T-015-r4-paralegal-recheck.py (.out.txt): byte diff of golden blocks 1-2 vs REQUIREMENTS section 6; R-EX-4(1) comparison; mutations M1-M4 on a scratch copy of evals/golden (base exit 0; M1, M2, M3, M4 each exit 1)",
  "grep 'patient_self_report|summary+excerpt' README.md sample.expected.json -> no match; grep 'no physician' sample.expected.json -> line 1014",
  "git status --porcelain evals/golden spec -> empty; git log --oneline -3 -> 65537a4, 0c03c4f, 4cc0f81"
 ],
 "verdict": "changes",
 "scores": {"accident_conflict_both_sides": 5, "self_report_key_integrity": 5, "notes_block_matches_s6": 4, "ai_line_spec_consistency": 2, "tool_commentary_out_of_good_examples": 3},
 "findings": [
  {"severity": "major", "title": "AI-assistance line: golden and REQUIREMENTS section 6 agree, but normative R-EX-4(1) still has different text and a Pending items line that contradicts R-EX-4(11). The r3 finding's quoted R-EX-4(1) string is not in the spec.",
   "evidence": "evals/golden/sample.export.expected.txt:51 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.' ; spec/REQUIREMENTS.md:273 same sentence (identical). spec/REQUIREMENTS.md:122 R-EX-4(1): 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' followed by 'Pending items: N.' R-EX-4(11) at :122: 'Pending items not included.' Probe Part A: 'R-EX-4(1) fixed text present verbatim in REQUIREMENTS: True; golden AI line equals R-EX-4(1) fixed text: False' (artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt). grep for the r3 quoted string 'every item in the treatment section was accepted by the paralegal. Items not reviewed: N' in spec/REQUIREMENTS.md -> rc=1.",
   "why_it_matters": "R-EX-6 makes the export golden the byte-exact E2E target. An implementer who follows R-EX-4(1) fails the golden. An implementer who follows the golden contradicts R-EX-4(1). The spec also contradicts itself on pending items. The line says every item was reviewed, which overstates what the tool tracks. The count line is the one I check before export (checklist 17). Severity is held at major because the r3 finding was major and the residual is the same defect, not a new one.",
   "fix": "Spec owner (architect or qa) picks one AI-line text and makes R-EX-4(1), REQUIREMENTS section 6 block 2 and the golden identical. Remove 'Pending items: N.' from R-EX-4(1) so it agrees with R-EX-4(11). Change the check_golden.py AI-line error text, which currently says 'the R-EX-4(1) text' while it checks the section 6 text, so it names the section that actually holds the text.",
   "acceptance_test": "grep -n 'drafted with AI assistance' spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt shows the same sentence in both files. grep -n 'Pending items: N' spec/REQUIREMENTS.md matches nothing. The r4 probe Part A prints 'golden AI line equals R-EX-4(1) fixed text: True'. check_golden.py exits 0."},
  {"severity": "minor", "title": "Carry-forward of the r3 minor: tool-authored commentary on what no physician said remains as a good example, now under M10",
   "evidence": "evals/golden/sample.expected.json:1014 good_examples: 'Per the patient, symptoms started after the January collision; the note records no physician opinion on cause.' (grep 'no physician' returns only this line; the M2 examples the r3 finding named are gone.)",
   "why_it_matters": "This sentence judges what the record set lacks. It is not the record's words, and R-EX-1 keeps that kind of tool commentary out of the letter. Golden good examples read as house style, so this example teaches the wrong style.",
   "fix": "Replace with a record-words example, e.g. 'Per the patient, symptoms started after the January collision.'",
   "acceptance_test": "grep -n 'no physician' evals/golden/sample.expected.json returns nothing. check_golden.py exits 0."}
 ],
 "whats_right": [
  "Export line 55 quotes both sides verbatim and says the tool does not choose between the dates. Deleting the record-1 quote from that bullet makes check_golden.py exit 1 (probe M2).",
  "Self-report spans use one key everywhere (self_report_spans, 10 uses, 0 spans). An objective span under that key exits 1 (M1), and a renamed key exits 1 through the ENTRY_KEYS guard (M3).",
  "The export notes block is byte-identical to REQUIREMENTS section 6 block 2. The stale Pending items line and the stray period are gone, and 'Items not reviewed: 0.' matches section 6 line 273."
 ],
 "questions_for_chris": [
  "Which AI-assistance text is authoritative: R-EX-4(1) ('AI assistance: ... before export.' followed by 'Pending items: N.') or REQUIREMENTS section 6 block 2 and the golden ('This chronology was drafted with AI assistance; ... Items not reviewed: 0.')? R-EX-4(1) also contradicts R-EX-4(11) ('Pending items not included.'). I am read-only on spec, so I have not edited it."
 ]}
```
