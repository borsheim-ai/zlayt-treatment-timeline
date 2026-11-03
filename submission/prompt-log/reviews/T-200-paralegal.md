# T-200 undated ledger charge label (bd72d5b): paralegal review (Maria Delgado, senior PI paralegal)

**Verdict: pass** (0 blockers, 0 majors, 2 minors, 1 nit).

**Scope.** I extracted `git archive bd72d5b` to the session scratchpad. I ran it on port 7963 with the fixture backend (`/api/health`: `"demo_mode":true,"local_mode":true`). Local mode is needed because `/api/library` is local-only. I stopped listener PID 66842 afterwards: `lsof` returned exit 1 and `curl` returned 000. Dated charge lines (D-071) are out of scope and not graded here.

**Deterministic checks first (from the archive):**
- `pytest tests/unit/test_t200_undated_charge_label.py` gave `6 passed in 1.93s` (pytest-t200.out).
- `python -m evals.letter_check` gave `{"value": 0, "cases": 25, ...}` (letter_check.out).

## What I did on lib11

1. Drafted lib11. Accepted Step 2, and dismissed the refused ledger entry e9.
2. In Step 3, counted the three undated ledger lines. For each I ticked "I checked this is a separate charge for a service" and the compare box.
3. Downloaded the letter and notes. The on-screen letter text is byte-identical to the download.

The BILLED CHARGES section now reads (lib11-letter.txt:37-46):

```
Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.00
```

## Does it work in a demand letter? Yes.

My r2 major (T-181-paralegal-r2) is fixed:
- **No bare date.** The old line was "itemized ledger, June 15, 2026: $250.00". An adjuster would have read June 15 as a visit that has no treatment note. Now the date is labelled as the statement's.
- **The date is faithful.** "statement dated June 15, 2026" is an unambiguous reformat of the record's own words, "statement date 06/15/2026" (case_lib11 record 9).
- **The adjuster can still use it.** The date lets the adjuster tie each line to the ledger page.
- **Screen and letter agree.** Step 3 shows "No date of service (statement dated June 15, 2026)" (p01.out:406-408).
- **Clean paste.** The charge lines are plain ASCII, so they paste into Word cleanly.
- **The ED line is unchanged.** It still carries its date of service.
- **The total is right.** It is $6,000.00.

"Service date not stated" is blunt. An adjuster will ask for a dated bill (CMS-1500) either way, and the blunt wording is better than any date the reader would take as a visit. Whether the attorney wants that admission in the demand is a strategy call, so it is outside my lens (litigation-lead).

## What is still thin (minors)

1. **The internal notes do not mention these three charges.** `grep -c "service date\|date of service" lib11-notes.txt` gives 0. The attorney reads the notes before the letter goes out. Nothing there says three counted Fennimoor charges have no date of service, or suggests requesting a dated itemized bill. R-EX-4 section 5 covers only amounts that are not totaled, so this is a "should", not a spec violation.
2. **No eval guards a counted undated line.** The card AC says "golden letters and evals/letter_check updated". `git show --stat bd72d5b` lists no `evals/` file. The handoff says letter_check walks accept only, not count. A regression on this line would be caught only by the new unit test.

**Nit.** The Step 3 card header still reads "Fennimoor Spine Clinic, itemized ledger · June 15, 2026", with the date bare (p01.out:348). The reason line under it does explain it. It is screen only, not in the letter.

```json
{"card": "T-200", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive bd72d5b extracted to the session scratchpad (t200/); fixture backend FIXTURE_SET=curated, demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, http://127.0.0.1:7963, listener PID 66842 stopped (lsof exit 1, curl 000). Library case case_lib11_priors_and_ledger. Dated charge lines (D-071) not graded. Evidence dir artifacts/review-evidence/T-200-paralegal/ (lib-step4.png was taken after revisiting Step 3, so it shows Step 3; the Step 4 letter is in lib11-letter-onscreen.txt).",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-181-paralegal-r2.md, board.py show T-200 (AC, notes, handoff), git show bd72d5b (export.py charge_when, store.charge_dos_stated, amounts.py, api.md), D-064 and D-071 in memory/ORCHESTRATOR_DECISIONS.md, R-EX-4 in spec/REQUIREMENTS.md",
  "From the archive: pytest tests/unit/test_t200_undated_charge_label.py: '6 passed in 1.93s' (pytest-t200.out); python -m evals.letter_check: value 0, 25 cases (letter_check.out)",
  "Playwright p01_lib11.py (p01.out): New case > library lib11 > Read > Draft (2.6 s) > Step 2 accept all, dismiss refused e9 > Step 3 count the three undated ledger lines (check-separate + check-compare) > Step 4 download letter and notes, read on-screen letter (identical to download) > revisit Step 3 (date column 'No date of service (statement dated June 15, 2026)')",
  "Read lib11-letter.txt BILLED CHARGES lines 37-46 against evals/library/case_lib11_priors_and_ledger.txt record 9 ('statement date 06/15/2026'); non-ASCII grep on the letter (charge lines ASCII); grep of lib11-notes.txt for service-date wording (0)"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "undated_charge_line_reads_right_for_adjuster": 4},
 "findings": [
  {"severity": "minor", "title": "Internal notes say nothing about the three counted charges that have no date of service",
   "evidence": "artifacts/review-evidence/T-200-paralegal/lib11-notes.txt: grep -c 'service date\\|date of service' = 0; the BILLS TO REQUEST line names only 'Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.'",
   "why_it_matters": "The attorney reads the notes before the demand goes out. The adjuster will ask for a dated itemized bill for $2,740 of Fennimoor charges, so the records request should be queued now, not after the response letter.",
   "fix": "Add one notes line per provider: 'Counted without a stated date of service: record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) $250.00, $180.00, $2,310.00; request dated itemized bill.' Keep the letter wording unchanged (D-071).",
   "acceptance_test": "Unit test on lib11 with the three ledger lines counted: internal_notes_text names each counted undated charge and contains 'request dated itemized bill'; letter_text unchanged."},
  {"severity": "minor", "title": "No eval or golden covers a counted undated ledger line (AC says letter_check and goldens updated)",
   "evidence": "Card AC 1: 'golden letters and evals/letter_check updated'; git show --stat bd72d5b lists only app/backend/amounts.py, export.py, store.py, memory/contracts/api.md and tests/unit/test_t200_undated_charge_label.py; handoff: 'letter_check walks accept only, not count'.",
   "why_it_matters": "The only guard against the old 'itemized ledger, June 15, 2026: $250.00' line coming back is one unit test. The eval that walks every letter never produces this line.",
   "fix": "Give evals/letter_check (qa) a count walk for D-064 'Count this charge' items. Assert that no charge line whose quote has no date shows a bare long date before the amount.",
   "acceptance_test": "python -m evals.letter_check exits 1 when charge_when is reverted to f'{src}, {_long_date(rd)}' (mutation test)."},
  {"severity": "nit", "title": "Step 3 card header still shows the statement date bare",
   "evidence": "p01.out:348 'Fennimoor Spine Clinic, itemized ledger · June 15, 2026 / ... / The line states no date of service'",
   "why_it_matters": "On screen only. The reason line below explains it, but the header reads like a date of service at a glance.",
   "fix": "Header 'itemized ledger · statement dated June 15, 2026' for billing records.",
   "acceptance_test": "E2E on lib11 Step 3: the card header for a2 contains 'statement dated'."}
 ],
 "whats_right": [
  "The counted ledger line names its date as the statement's and says the service date is not stated. Nothing reads as a visit date (lib11-letter.txt:39-43).",
  "Step 3 ('No date of service (statement dated June 15, 2026)') and the letter now agree.",
  "The ED line keeps its date of service, and the total is $6,000.00; letter_check is value 0 over 25 cases."
 ],
 "questions_for_chris": []}
```
