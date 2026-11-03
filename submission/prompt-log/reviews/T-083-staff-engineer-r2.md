# T-083 r2 review: billing analysis on itemized ledgers (staff-engineer-reviewer)

**Verdict: fail.** One blocker stands: blocker 3 from r1 is not closed.

Brief checks, one line each:
- **Blocker 1 (files and hook in HEAD): closed.** `git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py` prints both paths. `git show HEAD:app/backend/api.py` lines 509-510 wire `billing.add_routes`.
- **Blocker 2 (per-visit rates never totaled; cues win beside charge or billed): closed for the cases asked.** `Charge per visit $185.00.` and `Charge per visit $185.` are excluded once, and billed stays 25000 (prose). `Billed $150.00 per visit.` and `Billed $150 per visit.` are excluded once (prose). The table row `Charge per visit` with CHARGES `185.00` or `$185.00` gives billed 13000 and one excluded rate of 18500. Scratch mutants that remove a cue fail tests (M01, M03, M04, M06, M07, M08). The no-decimal form (`185`, `$185`) is not closed; see finding 1.
- **Blocker 3 (unmatched CMS-1500 and ledger rows listed as unreconciled, never dropped): NOT closed.** Four drop paths remain with `complete: true` and no unreconciled entry (finding 1).
- **Majors from r1:** F4 (prose rate guard test) closed; F5 (verifier on the route, record-text reference) closed except one minor (finding 3); F6 (unreadable provider is not $0.00) closed; F7 (blank DOS), F8 (UNRECOGNISED_BILLING_FORM) and F9 (RATE column) closed. One new major: the prose charge gate is unpinned (finding 2).
- **api.md billing section:** closed. At HEAD the billing section is at line 651, `## DELETE /api/cases/{token}` is at line 707 and its body (`204`. Removes the case...) is intact at line 708.

Evidence: probe log `artifacts/review-evidence/T-083-r2/probes.log`, mutant log `artifacts/review-evidence/T-083-r2/mutants.log`, runners `artifacts/review-evidence/T-083-r2/probes_r2.py` and `artifacts/review-evidence/T-083-r2/run_mutants.py`. The pin is `git archive 8bc7f90` into the reviewer scratchpad. Mutants ran on scratch copies only: 23 mutants, 21 caught, 2 survived (M05, M20). `.venv/bin/python -m pytest -q tests/unit/test_billing.py` gives 56 passed on every run (4 runs).

```json
{"card": "T-083", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 8bc7f90 (T-083 r2; card commits f218263 and 8bc7f90, restore in e2b4e3f): app/backend/billing.py, app/backend/amounts.py, app/backend/reclassify.py, app/backend/api.py (2 lines), tests/unit/test_billing.py, memory/contracts/api.md billing section. Pinned with git archive 8bc7f90 into the reviewer scratchpad (pin-8bc7f90). No app URL; the billing route is exercised by TestClient tests and by direct analyze() probes. Sample case: not on this path (billing is not in the sample CLI). Probe fixtures are synthetic.",
 "exercised": [
  "board.py show T-083 (status in_review, commits [f218263, 8bc7f90], round-2 notes); read reviews/T-083-staff-engineer.md (r1, 9 findings); read personas/staff-engineer.md; read the T-083 patterns memory file",
  "git log --oneline -12; git cat-file -t e2b4e3f (commit); git show --stat 8bc7f90 (amounts.py, billing.py, reclassify.py, api.md, test_billing.py)",
  "git ls-tree --name-only HEAD app/backend/billing.py tests/unit/test_billing.py: both paths printed. git show HEAD:app/backend/api.py | grep -n -i billing: line 509 from billing import, line 510 billing.add_routes(app, conn=conn, get_case=get_case)",
  "git show HEAD:memory/contracts/api.md | grep -n '^#': '## GET /api/cases/{token}/billing' at 651, '## DELETE /api/cases/{token}' at 707, body at 708. Billing rules paragraph (line 689) read in full",
  "git archive 8bc7f90 into the scratchpad pin; .venv/bin/python -m pytest -q tests/unit/test_billing.py: '56 passed' on four runs",
  "read the pinned app/backend/billing.py (757 lines), app/backend/amounts.py (171 lines) and tests/unit/test_billing.py (572 lines) in full",
  "red-flag greps on the three files: no float( in money code, no except, no sleep, no retry. The only round( hit is the name _line_around; time.time() in tests is an injected timestamp, not a sleep",
  "artifacts/review-evidence/T-083-r2/probes_r2.py run as .venv/bin/python -I probes_r2.py <PIN> with modes brief, table, prose, cms, noisy; output in artifacts/review-evidence/T-083-r2/probes.log. verify_citations returned 0 failures on every probe case",
  "artifacts/review-evidence/T-083-r2/run_mutants.py on scratch copies of the pin (never the repo): 23 mutants; log artifacts/review-evidence/T-083-r2/mutants.log: 21 CAUGHT, 2 SURVIVED (M05, M20), 0 NOT APPLIED",
  "not exercised: a live server or app URL, the sample CLI (python -m app.pipeline evals/golden/sample.txt), the frontend billing panel (not built yet per the r2 handoff)"
 ],
 "verdict": "fail",
 "scores": {"delivered_on_branch": 5, "integer_cents_no_llm": 5, "rate_guard": 4, "grounding_verifier": 4, "honest_failure_visible": 2, "test_quality": 3, "determinism_and_reproducibility": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Blocker 3 not closed: unparsed ledger and CMS-1500 rows are still dropped while complete is true",
   "evidence": "artifacts/review-evidence/T-083-r2/probes.log. Case A and B (table, CHARGES '$185' and '185', description 'Office visit'): billed 13000, complete True, unparsed 0, excluded [], unreconciled [], line b2 billed None kind balance_only; A also raises LEDGER_TOTAL_MISMATCH without naming the row. Case H (table, 'Charge per visit', CHARGES '185'): excluded [] and no unreconciled entry. Case C (prose 'Office visit $250.00. Total charges $250.00. Balance due $250.00.') and J ('Balance due $250.00.' alone): status none_found, totals.billed null, excluded [], unreconciled []. Case I (prose 'Physical therapy $2O0.00.'): none_found. Case E (CMS-1500 service line '    11     98941              AB     85.00         1      SYN-NPI-0001' with no date): billed 17500, complete True, unreconciled []. Code: billing.py:41 _FIG requires a decimal point; billing.py:42 _NUM; billing.py:165 figs = list(_NUM.finditer(ln)) with no figure gives a line with no unclear and no unparsed flag; billing.py:246-248 if a[\"cents\"] is None: continue; billing.py:264-265 elif cls == \"charge\" with no else; billing.py:327-329 the CMS tail requires a date token; billing.py:576 and :662 build providers and found from emitted lines only, so stated totals are discarded. Contract, memory/contracts/api.md:689: 'A row that carries a figure or a date but fits no column (CMS-1500 or ledger) becomes a `kind: unclear`, `unparsed: true` line with `ROW_NOT_PARSED`, makes the provider `complete: false`, and is listed in `unreconciled`'. Repro: git archive 8bc7f90 into a scratch dir, then .venv/bin/python -I artifacts/review-evidence/T-083-r2/probes_r2.py <PIN> table (and modes prose, cms, noisy).",
   "why_it_matters": "A figure the record prints disappears from the output while the provider reads complete. That is 'loses facts' under D.2, and it is the same defect as r1 F3. The r2 fix covers only rows whose figure has two decimals, and real ledgers print '$185' and '185'. The contract at api.md:689 says these rows go to unreconciled. Brief check 3 fails, and so do the prose and dateless-CMS cases.",
   "fix": "(a) Accept a figure with no decimals in ledger and CMS rows as a token; when it does not read to two decimals, keep its text as unclear, never leave the row empty. (b) A dated table row with an empty figure list but a money-like token in its tail goes to unparsed with ROW_NOT_PARSED. (c) In _ledger_text (billing.py:246-265) a figure whose cents is None or whose class is unclear is emitted as an unparsed line, and a statement that has stated totals but no emitted line reports partial_unclear with those totals kept. (d) In _cms1500 (billing.py:327-329) the rest check must not require a date token; a service-shaped line with figures and no date goes to unparsed. Each of these sets complete false for its provider.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-083-r2/probes_r2.py against the new HEAD in modes table, prose, cms, noisy: cases A, B, C, E, H, I and J must each show an unreconciled entry or an excluded entry with the row excerpt, and complete false where a row was lost. Add tests to tests/unit/test_billing.py for the '$185' and '185' table rows, the prose 'Office visit $250.00' line, and the dateless CMS-1500 line. Add a mutant for each new branch (the existing M10 and M12 only cover dated rows) and confirm a test fails."},
  {"severity": "major",
   "title": "Prose charge gate is unpinned: a figure the classifier cannot place is totaled and all 56 tests still pass",
   "evidence": "artifacts/review-evidence/T-083-r2/mutants.log: 'M05 prose cls!=estimate gate (unclear becomes charge): SURVIVED | 56 passed'. Mutant: billing.py:264 elif cls == \"charge\": changed to elif cls != \"estimate\": in a scratch copy. The rate branch above it still catches rates, so this mutant tests the unlabelled-figure path only.",
   "why_it_matters": "On the prose path this gate is the only thing that keeps a figure with no recognised label out of billed. The r1 F4 finding had the same shape and was rated major. Rate cases are now pinned (M04 and M23 are caught), but nothing says 'unclassified means not totaled'. A rate worded without a cue word, such as 'Standard fee $185.00.', would enter billed on regression with no test failing.",
   "fix": "Add a prose-ledger test with one unlabelled figure next to a stated total, asserting the figure is not in billed. After the finding 1 fix, also assert it appears in unreconciled or excluded.",
   "acceptance_test": "The new test passes on HEAD and fails on mutant M05 (billed includes the unlabelled figure)."},
  {"severity": "minor",
   "title": "A stated-total figure is not checked against its own cite; the mutant survives",
   "evidence": "artifacts/review-evidence/T-083-r2/mutants.log: 'M20 verifier stated-total cite check off: SURVIVED | 56 passed'. Check at billing.py:720-721 (if _figure_like(d) and isinstance(d.get(\"cite\"), dict) and not _in(d[\"text\"], d[\"cite\"].get(\"excerpt\", \"\"))). The only test that touches stated cites, tests/unit/test_billing.py:549, breaks the cite excerpt itself, which the verbatim check at billing.py:713-714 catches first, so this branch never decides a test.",
   "why_it_matters": "The persona checklist (item 4) requires each amount to appear in its cited text. A stated total cited to a line that does not carry that figure would pass every test.",
   "fix": "Add an assertion that changes only stated_totals.billed.text to a figure absent from its cite, and expects a citation failure with reason stated_figure_not_in_cite.",
   "acceptance_test": "Mutant M20 is caught by a test in tests/unit/test_billing.py."},
  {"severity": "minor",
   "title": "The unreconciled CMS-1500 row lists the whole line tail as its figure",
   "evidence": "artifacts/review-evidence/T-083-r2/probes.log, case F: unreconciled [('ROW_NOT_PARSED', ['11     98941              AB     85.00      SYN-NPI-0001'])]. Code: billing.py:329 unclear=[rest.group(1).strip()]. The test at tests/unit/test_billing.py:462 asserts '$85.00' in u['figures'][0], which passes on the whole tail.",
   "why_it_matters": "The paralegal sees the NPI and the procedure code next to the money, and the r1 F3 fix asked for the figure text. The membership assertion let the defect through.",
   "fix": "Put only the money tokens in figures (for example ['85.00']) and assert equality, not membership.",
   "acceptance_test": "A test for the no-units CMS line asserts u['figures'] == ['85.00'] (or the agreed text), and fails when the tail is listed instead."},
  {"severity": "minor",
   "title": "Broad except in store.load_records falls back silently to the whole record block (pre-existing, outside the 8bc7f90 diff)",
   "evidence": "git show HEAD:app/backend/store.py, lines 22-25: 'try:' / 'body = ingest.split_records(block)[0][\"excerpt\"]' / 'except Exception:' / 'body = block'. Not in the 8bc7f90 stat, so not introduced by T-083. billing reads its excerpts through this path.",
   "why_it_matters": "Persona section 5 and checklist item 12: no broad except that falls back silently. A split failure changes which text is cited and verified, with no status shown to the paralegal.",
   "fix": "Catch only the error split_records raises for a bad block, and surface it as a visible record-level status, or let it raise.",
   "acceptance_test": "A unit test makes split_records raise and asserts a visible status, not body = block. Owner: backend."},
  {"severity": "nit",
   "title": "A redundant assertion in the per-visit table test",
   "evidence": "tests/unit/test_billing.py:376: assert p[\"checks\"] == [] or [c[\"code\"] for c in p[\"checks\"]] == [].",
   "why_it_matters": "The second clause adds nothing, and the disjunction reads as weaker than it is.",
   "fix": "Write assert p[\"checks\"] == [].",
   "acceptance_test": "The test still passes on HEAD and fails when a check is added."}
 ],
 "whats_right": [
  "Blocker 1 and the api.md placement are closed: both card files and the billing hook are in HEAD, and the DELETE section is intact at HEAD line 707.",
  "Per-visit rates with a $ or without one are excluded once and never totaled, in prose and in tables; mutants M01, M03, M04 and M06-M08 each fail a test.",
  "The verifier runs on the route and checks against the record block (mutants M16-M19 and M22 each fail a test); money is integer cents with no float and no LLM call."
 ],
 "questions_for_chris": [
  "CLAUDE.md section 6 and D-024 call for Sonnet on engineering reviewers. This review ran as claude-haiku-5-5, as the brief asked. Confirm the dispatch model for rounds 3 and later on T-083."
 ]}
```
