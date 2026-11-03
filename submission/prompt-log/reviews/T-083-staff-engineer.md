# T-083 review (r1): billing analysis on itemized ledgers (staff-engineer-reviewer)

**Verdict: fail.** Three blockers, three majors, three minors.

Notes for the orchestrator, before the findings:
- **Model.** This review is by claude-haiku-5-5, as the brief states and as this session runs. CLAUDE.md section 6 and D-024 call for Sonnet on engineering reviewers, and the persona file expects claude-sonnet-5-5. The dispatch needs a check.
- **F1 is a repo-state defect, not a defect in f218263.** It was caused by another card's commit (ec33bf0, T-084). I rated it blocker under D.2 ("makes the must-have unusable"), because on HEAD the D-042 billing route does not exist. F2 and F3 are code defects that stand on their own.
- **Brief checks.** Verbatim excerpts: pass (independent check, zero violations). Hand recompute of the Larkspur ledger: matches the code. Rate guard mutation in a scratch copy: UB-04 and table-ledger rate guards are caught; the prose rate guard is not (F4), and table-row rates are not guarded at all (F2). CMS-1500 implied cents: handled and tested (mutant M5 caught).

## What I exercised

- Read: `personas/staff-engineer.md`, `board/cards/T-083.md`, `memory/ORCHESTRATOR_DECISIONS.md` (D-019 line 27, D-042 line 50), `research/record-formats.md` (sections 1.1, 1.2, 8, 9, 16 and the fee-schedule trap at line 489), `app/backend/billing.py` (642 lines, full), `tests/unit/test_billing.py` (330 lines, full), `app/backend/amounts.py` (`find_amounts` line 33, `classify` 51-70).
- Pinned f218263 with `git archive f218263` into the session scratchpad (`pin-f218263`). Working-tree `billing.py` and `test_billing.py` are byte-identical to the f218263 blobs (`git show f218263:... | diff -q`).
- `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: **27 passed** on the working tree, **27 passed** on the pinned copy, **27 passed** on a second run (determinism).
- Repo state at HEAD (`git ls-tree`, `git show --stat ec33bf0`, `git show HEAD:app/backend/api.py | grep -c billing`): evidence in `artifacts/review-evidence/T-083-r1/head_state.txt`.
- Mutation runner `artifacts/review-evidence/T-083-r1/run_mutants.py` on scratch copies (log `artifacts/review-evidence/T-083-r1/mutants.log`): nine mutants, results in F4 and F5.
- Probes (python against the pinned copy and mutant copies): prose rate sentences; table rows with per-visit wording, with and without `$`; unnamed RATE column; RATE column with no charge; ambulance invoice (research section 16 specimen); CMS-1500 variants (printed decimal, slash dates, no Item 28); `box_amount` values; ledger rows with blank DOS and with no date.
- Independent verbatim check: every `excerpt`, `cite`, `cites[]`, and figure text in the five billing output shapes (ledger+EOB, CMS clean, CMS OCR, UB-04, prose+LOP) checked as a substring of the record's own `text` field. 0 violations across 31 excerpts, 15 cites and 14 line figures, not using `verify_citations`.
- Hand recompute of the Larkspur ledger (tests/unit/test_billing.py `LEDGER`): lines 210.00, 130.00, 70.00, 35.00, (70.00) VOID, 70.00, ADJ 45.00 credit. Billed = 210+130+70+35-70+70 = 445.00 (44500 cents). Adjustment = 45.00. Balance = 445.00 - 0.00 - 45.00 = 400.00 (40000). Code output matches on all three, and on every running-balance step.
- Red-flag greps on `billing.py` and `test_billing.py`: no `except` (count 0), no `float(`/`round(`, no multiplication of a rate by a count, no `sleep`, `retry` or network call. `test_billing.py:330` checks that `app.llm` is absent from the source text (a string check, not an import check).
- Route read: `billing.py:634-641`; `grep -c verify_citations app/backend/api.py` returns 0.
- Not exercised: a live server (no app URL), the evals/sample case (`evals/golden/sample.txt`), the frontend. The billing route is exercised only through the TestClient test.

## Findings

**F1 blocker. The card's code and route are absent from HEAD.** T-084's commit ec33bf0 deletes `app/backend/billing.py` (642 lines) and `tests/unit/test_billing.py` (330 lines), and replaces the billing hook in `app/backend/api.py` with the reclassify hook. Both commits are one second apart (22:25:02 and 22:25:03), which is consistent with a shared-index race. I did not verify the cause. At HEAD 02ff244 (checked after HEAD moved), `git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py` prints nothing and `grep -c billing` on `HEAD:app/backend/api.py` gives 0. The only copies are untracked working-tree files. Card T-083 cites commit f218263, which no longer reaches the branch's content.

**F2 blocker. Per-visit rate rows in an itemized table are totaled as charges; a rate with `$` is also listed as an excluded rate.** Probe on the pinned copy, table with a CHARGES column and the row `06/10/26  06/11/26  99213  Charge per visit  185.00  185.00`: line 99213 has kind `charge` and billed 18500; `totals.billed` = $315.00 (31500); `excluded` = []. Same row with `$185.00`: billed 31500 and `excluded` lists `(18500, rate)` twice. The code path: `billing.py:465-468` appends table lines with no rate check; `billing.py:489` only classifies figures returned by `find_amounts`, and `amounts.py:33` says it finds only `$` figures. RULES line 30 says a per-visit rate is never a charge, and research section 1.2 agrees. This is the persona's red flag ("a total that includes the $185 rate").

**F3 blocker. Service lines that do not match a strict pattern are dropped silently; the output still says complete.**
- CMS-1500, printed decimal in 24F, no Item 28 line: lines `060126 060126 11 98941 AB 85.00 1`, `060226 060226 11 98941 AB 85 | 00 1`, `060326 060326 11 97014 A 90 | 00 3`. Output: billed 17500 (expected 26000), 2 lines, `complete` True, `checks` [], `status` analyzed. Cause: `billing.py:242` (`_AMT` accepts no `.`), and `billing.py:282-288` lets a non-matching line fall through with no record of it. The same happens with slash dates (`06/01/26`).
- Ledger table, row with no date (`97014 E-stim unattended 35.00 165.00` under a DOS-less line): billed 20000, `complete` True. The stated total flags only an aggregate (`LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`) that does not name the row. Cause: `billing.py:148-150` (`if not m: continue`).
- Under D.2, "loses facts" is a blocker. D-027 ("text outside recognised blocks is never dropped") is the same principle.

**F4 major. No test pins the prose rate guard; a mutant that lets a rate become a charge passes all 27 tests.** Mutant M3 changes `billing.py:228` from `== "charge"` to `!= "estimate"`. `mutants.log`: `M3_prose_rate_gate_open: 27 passed`. Probe sentence: `Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.` Mutant: billed 43500 with a line for the $185 rate, `checks` []. Pinned f218263: billed 25000, `checks` [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH]. The stated total was written to include the rate, so the mutant passes every check. `grep -n -F "per visit" tests/unit/test_billing.py` finds nothing; the only rate wording is the table's `Fee schedule ... per unit` at line 24, which runs through the table path.

**F5 major. The grounding verifier cannot fail on real output, and the route never calls it.**
- `billing.py:612` says "Run in tests and by the API before a response leaves: a line that fails is dropped from the response". The route (`billing.py:634-641`) calls only `get_case` and `for_case`. `grep -c verify_citations app/backend/api.py` gives 0. The docstring is false.
- `billing.py:613` builds the reference as `text + "\n" + excerpt`, so any cite that is a substring of its own excerpt passes. The fail-closed check at `billing.py:485-487` cannot fire: every line excerpt is sliced from `body`, and `text` contains `body`.
- Mutants: M7 (fail-closed block disabled) `27 passed`; M8 (reference = record text only) `27 passed`; M9 (verifier returns []) fails one test. The verifier is only caught when it is stubbed to return [], not when its reference is weakened.
- `verify_citations` also does not cover `payer_reports[].lines[].excerpt`, `line_flags[].excerpt`, `checks[].cites`, or the `stated_totals[].cite` fields.
- The verbatim property holds today (independent check, zero violations), but nothing enforces it.

**F6 major. The grand total treats an unreadable provider as $0.00.** `billing.py:603-605` uses `sum(p["billed"]["cents"] or 0 ...)`. Probe: a provider whose only line has an unreadable figure gives `providers[0].billed` = None and `totals.billed` = `{"cents": 0, "usd": "$0.00"}`, status `partial_unclear`. A default value is shown as a total; the spec says unreadable figures are kept out of totals, not reported as zero.

**F7 minor. A blank DOS cell takes the POSTED date as date of service.** Probe: row `          06/11/26  97014  E-stim unattended  35.00  165.00` gives `dos` = `06/11/26`, `posted` = None. `billing.py:148-157` treats the first date in the row as DOS. Research section 1.1 names the posting-versus-service trap. No totals change, but EOB matching (`billing.py:576-577`) can pair on the wrong date.

**F8 minor. A billing record that matches no form is absent, with no notice.** Probe with the research section 16 ambulance invoice (no `$` sign, no balance column): `status` none_found, `providers` [], `skipped_records` []. `form_of` (`billing.py:93-108`) returns None and `analyze` has no branch for it (`billing.py:465-483`). The case reports "none found" for a case with a bill. Ambulance invoices are outside the card's named forms, so this is minor.

**F9 minor. A rate in an unnamed RATE column is listed as unclear, not as an excluded rate.** Probe: header `UNITS  RATE  CHARGES`, row `2  65.00  130.00`. Output: billed 13000 (correct), line `unclear` ['65.00'], `complete` False, `excluded` []. `billing.py:46-47` (`_COLS`) has no RATE entry. Not totaled, so this is conservative, but the rate is not shown under "Rates and excluded".

**What is right (not to break):**
- Money is integer cents throughout; no floats; no rate is multiplied by a count; the Larkspur ledger hand recompute matches (44500 / 4500 / 40000).
- UB-04: the FL 44 rate is excluded, the 0001 total is compared and not added (9,165.75); mutants M1, M4 and M6 each fail the UB-04 test.
- CMS-1500 implied cents: `85 | 00`, `85 00` and `8500` read as $85.00; OCR letters (`45 OO`) are listed unclear, not guessed; mutant M5 fails the OCR test.

## Mutation results (scratch copies of f218263, `mutants.log`)

| Mutant | Change | Result |
|---|---|---|
| M1 | UB-04 rate branch disabled (`billing.py:325`) | fails 1 (UB-04 test) |
| M2 | ledger rate exclusion disabled (`billing.py:490`) | fails 1 (fee-schedule test) |
| M3 | prose rate gate opened (`billing.py:228`) | **passes 27 (F4)** |
| M4 | UB-04 rates not listed (`billing.py:480`) | fails 1 |
| M5 | CMS-1500 raw digits not implied cents (`billing.py:262`) | fails 1 (OCR test) |
| M6 | UB-04 rate header not found (`billing.py:302`) | fails 1 |
| M7 | fail-closed block disabled (`billing.py:485`) | **passes 27 (F5)** |
| M8 | verifier reference = record text only (`billing.py:613`) | **passes 27 (F5)** |
| M9 | verifier returns [] (`billing.py:613`) | fails 1 |

## Process

- Verdict by the D.2 rule: blocker present, so fail. The first-round count of blockers does not change if F1 is resolved by restoring the files, because F2 and F3 are independent.
- No finding rests on a claim I did not run. Where a claim depends on HEAD, the commands and outputs are in `artifacts/review-evidence/T-083-r1/head_state.txt`.

```json
{"card": "T-083", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f218263 (app/backend/billing.py, app/backend/api.py +2 lines, tests/unit/test_billing.py, memory/contracts/api.md +37), pinned by git archive to the session scratchpad (pin-f218263); HEAD checked at 02ff244; no app URL exercised (route exercised via TestClient in tests/unit/test_billing.py); sample case: synthetic fixtures LEDGER, EOB, CMS_CLEAN, CMS_OCR, UB_ROOM, PROSE, LOP from tests/unit/test_billing.py",
 "exercised": [
  "read personas/staff-engineer.md, board/cards/T-083.md, memory/ORCHESTRATOR_DECISIONS.md D-019 and D-042, research/record-formats.md sections 1.1, 1.2, 8, 9, 16 and line 489, app/backend/billing.py (full), tests/unit/test_billing.py (full), app/backend/amounts.py find_amounts and classify",
  ".venv/bin/python -m pytest -q tests/unit/test_billing.py: 27 passed (working tree), 27 passed (pinned f218263 copy), 27 passed (second run)",
  "git archive f218263 to scratchpad pin-f218263; git show f218263:app/backend/billing.py | diff -q against working tree: identical; test file identical",
  "git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py: empty at 02ff244; git show --stat ec33bf0 shows billing.py 642 deletions and test_billing.py 330 deletions; git show HEAD:app/backend/api.py | grep -c billing: 0 (artifacts/review-evidence/T-083-r1/head_state.txt)",
  "mutation runner artifacts/review-evidence/T-083-r1/run_mutants.py on scratch copies, log artifacts/review-evidence/T-083-r1/mutants.log: M1-M9 results",
  "probes against pinned copy: prose rate sentences; table rows with per-visit wording with and without $; unnamed RATE column; RATE column without charge; ambulance invoice specimen; CMS-1500 printed decimal, slash dates, missing Item 28; box_amount values; ledger rows with blank DOS and no date",
  "independent verbatim check of every excerpt, cite, cites[] and figure text in five output shapes against record text: 0 violations (31 excerpts, 15 cites, 14 line figures)",
  "hand recompute of the Larkspur ledger: billed 445.00, adjustment 45.00, balance 400.00 = 445.00 - 0.00 - 45.00; matches code output and running-balance steps",
  "grep for except, float(, round(, sleep, retry, network calls in billing.py and test_billing.py: none; grep -n -F per visit in test_billing.py: no match; grep -c verify_citations app/backend/api.py: 0; route read at billing.py:634-641"
 ],
 "verdict": "fail",
 "scores": {"delivered_on_branch": 1, "integer_cents_no_llm": 5, "rate_guard": 2, "grounding_verifier": 2, "honest_failure_visible": 2, "test_quality": 3, "determinism_and_reproducibility": 4},
 "findings": [
  {"severity": "blocker", "title": "Card code and route absent from HEAD: T-084 commit ec33bf0 deletes billing.py, test_billing.py and the billing hook",
   "evidence": "artifacts/review-evidence/T-083-r1/head_state.txt | git show --stat ec33bf0: 'app/backend/billing.py | 642 ----', 'tests/unit/test_billing.py | 330 ----'; git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py prints nothing at 02ff244; git show HEAD:app/backend/api.py | grep -c billing prints 0; git status shows '?? app/backend/billing.py' and '?? tests/unit/test_billing.py'",
   "why_it_matters": "The D-042 billing route GET /api/cases/{token}/billing is not served by any committed code and its tests exist only as untracked files. Card T-083 cites f218263, which no longer reaches the branch. Rated blocker under D.2 (must-have unusable). Commits ec33bf0 and f218263 are one second apart, consistent with a shared-index race; cause not verified.",
   "fix": "Backend or orchestrator: restore app/backend/billing.py and tests/unit/test_billing.py from f218263 and re-add the billing.add_routes call beside reclassify.add_routes in app/backend/api.py, so both routes are wired. Commit with explicit git add paths. Do not revert T-084.",
   "acceptance_test": "git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py lists both paths; .venv/bin/python -m pytest -q tests/unit/test_billing.py passes at HEAD; test_billing_route_for_a_pasted_case passes; the reclassify route still resolves"},
  {"severity": "blocker", "title": "Per-visit rate rows in an itemized table are totaled as charges; a rate with $ is also listed as an excluded rate",
   "evidence": "Probe on pinned f218263. Table row '06/10/26  06/11/26  99213  Charge per visit  185.00  185.00' (CHARGES column): line 99213 kind=charge billed=18500, totals.billed=31500, excluded=[]. Same row with '$185.00': billed 31500 and excluded=[(18500,rate),(18500,rate)]. billing.py:465-468 appends table lines with no rate check; billing.py:489 classifies only find_amounts results; app/backend/amounts.py:33 says find_amounts finds only '$' figures.",
   "why_it_matters": "billing.py:30 (RULES) says a per-visit rate is never a charge; D-042 and research/record-formats.md section 1.2 agree. The $185 per-visit price enters the billed total: the persona red flag 'a total that includes the $185 rate'. The $-form lists the same figure as both a charge and a rate, so the output contradicts itself. A stated total that includes the rate hides the error from the total check.",
   "fix": "Apply A.classify to each table figure with its row label (the rule the prose path already uses at billing.py:228) before assigning to billed. A rate-classified figure goes to excluded only, never to billed. Run the exclusion over every money figure in table rows, not only '$' figures, and never list one figure as both charge and rate.",
   "acceptance_test": "New tests in tests/unit/test_billing.py: (a) table row 'Charge per visit 185.00' in the CHARGES column gives billed excluding 18500 and excluded listing it exactly once; (b) the same row with '$185.00' gives the same result; (c) a statement whose stated total excludes the rate gives checks == []. Mutant: remove the new guard, and the test fails."},
  {"severity": "blocker", "title": "Unmatched service lines are dropped silently: complete=true, no unclear entry, no check when no stated total exists",
   "evidence": "Probe on pinned f218263: CMS-1500 with lines '060126 060126 11 98941 AB 85.00 1 SYN-NPI-0001' (printed decimal), '060226 060226 11 98941 AB 85 | 00 1', '060326 060326 11 97014 A 90 | 00 3', no Item 28: billed 17500 (expected 26000), lines 2, complete True, checks [], status analyzed. Slash dates '06/01/26' also dropped. Ledger row with no date: billed 20000, complete True, checks [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH] (aggregate only). Causes: billing.py:242 (_AMT accepts no '.'); billing.py:282-288 non-matching lines fall through with no record; billing.py:148-150 ('if not m: continue').",
   "why_it_matters": "A billed fact disappears while the provider reports complete. D.2 'loses facts' is a blocker. D-027 ('text outside recognised blocks is never dropped') is the same principle. When the aggregate mismatch does fire, it does not say which row was lost.",
   "fix": "Any CMS-1500 or ledger-table line that is not parsed but carries a money figure or a date-like token is emitted as a line with unclear=[figure text], LINE_UNCLEAR, and complete=false. Either parse a printed decimal in 24F as a stated amount or list it unclear; the silent drop is the defect. Add an unparsed-line count to each provider.",
   "acceptance_test": "Tests: the CMS fixture with a '85.00' line and no Item 28 gives an unclear line with its excerpt, complete False, and billed excluding it; a ledger row with no date is listed unclear and complete False; a slash-dated CMS line is listed, not dropped."},
  {"severity": "major", "title": "No test pins the prose rate guard; mutant M3 passes all 27 tests and lets a $185 rate become a charge",
   "evidence": "mutants.log: 'M3_prose_rate_gate_open: 27 passed'. Mutant changes billing.py:228 '== \"charge\"' to '!= \"estimate\"'. Sentence: 'Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00.' Mutant: billed 43500 with a line for the $185 rate, checks []. Pinned f218263: billed 25000, checks [LEDGER_TOTAL_MISMATCH, LEDGER_BALANCE_MISMATCH]. grep -n -F 'per visit' tests/unit/test_billing.py: no match; the only rate wording is 'per unit' at line 24, which runs through the table path.",
   "why_it_matters": "The prose-path rate guard is the only thing keeping a rate out of totals on prose ledgers. The stated-total check hides the error when the statement's own total was computed the same way. The brief asks that the rate guard be proven by tests, and this one is not.",
   "fix": "Add a prose-ledger test with 'Charge per visit $185.00' and a stated total that excludes it; assert the rate is excluded once and checks == [].",
   "acceptance_test": "The new prose test passes on f218263 and fails on mutant M3 (billed becomes 43500)."},
  {"severity": "major", "title": "The grounding verifier cannot fail on real output and the route never calls it",
   "evidence": "billing.py:612 docstring: 'Run in tests and by the API before a response leaves: a line that fails is dropped'. billing.py:634-641 route calls only get_case and for_case; grep -c verify_citations app/backend/api.py: 0. billing.py:613 text_of = text + excerpt, so any cite that is a substring of its own excerpt passes. Fail-closed check at billing.py:485-487 cannot fire (excerpts are slices of body; text contains body). Mutants: M7 (fail-closed off) 27 passed; M8 (reference = record text only) 27 passed; M9 (verifier returns []) 1 failed.",
   "why_it_matters": "Persona checklist items 4 and 13: the verifier must check each excerpt against its own record and fail visibly. Here the docstring claims an API gate that does not exist, and the in-analysis guard is unreachable. The verbatim property holds today (independent check: 0 violations), but nothing enforces it. verify_citations also skips payer_reports excerpts, line_flags excerpts, checks[].cites and stated_totals cite fields.",
   "fix": "Call verify_citations in billing_get and return a visible citation_failures list when it is non-empty. Build the reference from the record text only, normalised as documented. Extend the check to every cite-bearing field. Delete the dead fail-closed block or turn it into a checked assertion.",
   "acceptance_test": "A record with text 'A' and excerpt 'B $10.00' makes verify_citations non-empty; mutant M8 and M7 each fail a test; a route test with a patched non-verbatim cite shows a citation_failures entry."},
  {"severity": "major", "title": "Grand total treats an unreadable provider as $0.00",
   "evidence": "billing.py:603-605: sum(p['billed']['cents'] or 0 for p in providers). Probe: RATE column row with no charge gives providers[0].billed None and totals.billed {'cents': 0, 'usd': '$0.00'} with status partial_unclear.",
   "why_it_matters": "A default value is shown as a total. The spec says unreadable figures are kept out of totals, not reported as zero. A paralegal who reads 'Billed $0.00' is misled.",
   "fix": "Set totals.billed.cents to None when any provider's billed is None, or add totals.complete=false and totals.unreadable_providers.",
   "acceptance_test": "The probe fixture gives totals.billed.cents None (or totals.complete False); a test in tests/unit/test_billing.py asserts it."},
  {"severity": "minor", "title": "A blank DOS cell takes the POSTED date as the date of service",
   "evidence": "Probe: row '          06/11/26  97014  E-stim unattended  35.00  165.00' gives dos '06/11/26', posted None. billing.py:148-157 treats the first date in the row as DOS.",
   "why_it_matters": "A service date is attributed to a row whose DOS cell is blank (research/record-formats.md section 1.1 posting-versus-service trap). No totals change, but EOB matching at billing.py:576-577 can pair on the wrong date.",
   "fix": "Assign dates by column position when the header has separate DOS and POSTED columns; flag a row with an empty DOS cell as NO_DATE_OF_SERVICE.",
   "acceptance_test": "A blank-DOS row gives dos None, posted kept, and the flag."},
  {"severity": "minor", "title": "A billing record that matches no form is absent with no notice",
   "evidence": "Probe with the research/record-formats.md section 16 ambulance invoice (no $ sign, no balance column): status none_found, providers [], skipped_records []. form_of at billing.py:93-108 returns None; analyze has no branch for it (billing.py:465-483).",
   "why_it_matters": "A case with a bill reports 'none found'. Ambulance invoices are outside the card's named forms, so this is minor; D-027's principle applies.",
   "fix": "Record form None on a billing-looking source or with money figures as skipped_records with reason_code UNRECOGNISED_BILLING_FORM, shown to the paralegal.",
   "acceptance_test": "The ambulance specimen appears in skipped_records and status is not none_found."},
  {"severity": "minor", "title": "A rate in an unnamed RATE column is listed as unclear, not as an excluded rate",
   "evidence": "Probe: header 'UNITS  RATE  CHARGES' and row '2  65.00  130.00': billed 13000 (correct), line unclear ['65.00'], complete False, excluded []. billing.py:46-47 (_COLS) has no RATE entry.",
   "why_it_matters": "The rate is not totaled, which is conservative. But it is not shown under 'Rates and excluded', and the provider is marked incomplete for a figure its own column calls a rate.",
   "fix": "Add a RATE column kind to _COLS and route its figures to excluded with kind 'rate'.",
   "acceptance_test": "A RATE-column table gives excluded containing 6500 with kind rate, and complete True."}
 ],
 "whats_right": [
  "Money is integer cents with no floats or rate-times-count arithmetic; the Larkspur ledger hand recompute matches the code (44500 billed, 4500 adjustment, 40000 balance = 44500 - 0 - 4500).",
  "UB-04: the FL 44 rate is excluded, the 0001 total is compared and not added (916575 cents); mutants M1, M4 and M6 each fail the UB-04 test.",
  "CMS-1500 implied cents: '85 | 00', '85 00' and '8500' read as $85.00; OCR letters ('45 OO') are listed unclear, not guessed; mutant M5 fails the OCR test."
 ],
 "questions_for_chris": [
  "Was the deletion of app/backend/billing.py and tests/unit/test_billing.py in T-084 commit ec33bf0 intended? If intended, T-083 should be cancelled, not reviewed as done.",
  "A dated ledger row whose description says 'per visit' but whose amount sits in the CHARGES column: my reading of D-042 and RULES line 30 is that it is a rate and must not be totaled. Confirm, or tell me the judge re-check path you intend for it."
 ]}
```
