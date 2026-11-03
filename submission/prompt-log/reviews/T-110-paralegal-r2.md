# T-110 round 2: paralegal-reviewer (commit d24ff07)

Verdict: changes. No blockers. One major, three minors.

Setup: `git archive d24ff07` extracted into the scratchpad. Server A on port 7962 (`ZLAYT_MODE=local`, fixture backend, curated set, scratch DB). Server B on port 7963 (same, plus `ENABLE_LIVE=1`, `LLM_BACKEND=claude-cli`, scratch DB) for a real judge on my own probe text. Both stopped by PID (`kill 95133 96552`; curl then returned 000 on 7962 and 7963). Probe scripts: `artifacts/review-evidence/T-110-paralegal-r2-run1.py` to `run5.py`; probe text `T-110-paralegal-r2-probe.txt`; export text `T-110-paralegal-r2-live.tok.export.txt`.

## Your four checks

1. **"consultas $1,300" reclassifies and counts: confirmed, with one caveat.** lib09 a5 started `unclear`. `POST /reclassify {to: charge}` first returned 422 `JUDGE_UNAVAILABLE` (code check passed, wording "Estado de cuenta"; the fixture set has no recorded judge answer for class `charge` on this record). I then wrote a stand-in judge answer (`agree`) into my scratch copy's fixture dir under the missed key. The retry returned 200, kind `charge`, `judge_verdict: agree`, state `pending`. After accept, the total went from $5,090.00 to `Billed charges stated in these records: $6,390.00`. So the shipped demo cannot do this step; only a live or newly recorded judge can (finding 4).
2. **"$400 por sesión" stays a rate and is refused: confirmed.** a3 and a6 are kind `rate`. Reclassify returned 422 `NO_CHARGE_WORDING`, check `code`, for both. The saldo line a7 ($2,900) returned the same refusal.
3. **POSSIBLE OVERLAPS in the internal notes: confirmed.** The section reads "record 7 ... lists $1,300.00 on a statement line, and record 2 ... separately states $650.00, both for consult ... The total does not currently add both figures." `"overlap" in letter_text` is False. The total line has no parenthetical.
4. **Tray placeholder drops after a manual entry: confirmed.** With the record-6 extract fixture removed, `tray` was `[('e6','rejected')]`. After `POST /records/r6/entry` returned 201, `tray` was `[]` and `entries` held `e6_m`. After I accepted `e6_m`, `excluded` was `{'pending': 19, 'dismissed': 0, 'rejected': 0}`. The letter carried "Pain 5/10" and not the placeholder text.

## Call 1: "estado de cuenta" as a charge cue is too broad

It is a document title, not charge wording. The English guard's list (charged, billed, invoiced, amount due, balance due) names a charge; "statement" is not on it. Here any figure on a statement line passes the code check unless the sentence has `saldo`, a negation, or a rate cue.

I tried it. Probe text: six one-line Spanish statements, each beginning "Estado de cuenta:". Code check result on all six: passed (none returned `NO_CHARGE_WORDING`). The real judge (claude-haiku-5-5, server B) then answered:
- "pago recibido $300.00" (payment): refused, JUDGE_DISAGREES.
- "ajuste del seguro $500.00" (insurance adjustment): refused, JUDGE_DISAGREES.
- "el seguro pagó $4,000.00" (insurer paid): refused, JUDGE_DISAGREES.
- "copago de la paciente $50.00" (patient copay): **agreed, became a charge**.
- "pendiente de pago $2,900.00" (outstanding balance): **agreed, became a charge**.
- "sesiones de fisioterapia $1,600.00" (a real charge): agreed, correct.

I accepted the three that went through. The letter then read `Billed charges stated in these records: $4,550.00` and listed "$50.00" and "$2,900.00" with their quotes. Nothing warned that the $2,900 is a balance. So a balance and a payment-side figure can be promoted by one cue word the code treats as sufficient, with the judge as the only real barrier, and the judge missed two of five. The paralegal still has to click reclassify and accept, so I do not rate it a blocker. But the cue fails the persona's rule that the total holds explicit charges only.

## Call 2: $400 figures classed `rate` by code

Correct. "Costo por sesión de terapia física: $400.00" and "4 sesiones a $400.00 por sesión" are unit prices, both are refused for reclassify without a judge call, and neither reaches the total. One nit, not a finding: for the second line the record states 4 sessions, but the reason text only says "This figure is a rate, not a charge" and does not mention the stated count. A paralegal can do 4 x $400 herself; the tool leaves it out, which is the safe side.

```json
{"card": "T-110", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit d24ff07 via git archive; own servers :7962 (fixture, curated, ZLAYT_MODE=local) and :7963 (ENABLE_LIVE=1, claude-cli, real judge) with scratch DBs; library case_lib09_spanish_interpreter_espalda plus a six-record Spanish statement probe",
 "exercised": [
  "read personas/paralegal.md, reviews/T-110-paralegal.md, git show d24ff07 (amounts.py, reclassify.py, export.py), tests/unit/test_lib09_t110_r2.py",
  "loaded lib09 on :7962: 7 amounts, a3 and a6 kind rate, a2 a5 a7 kind unclear, a1 a4 charge verified",
  "POST reclassify to charge on a5 (422 JUDGE_UNAVAILABLE with wording 'Estado de cuenta', then 200 after a stand-in judge answer in my scratch fixture dir), a2 a3 a6 a7 (all 422 NO_CHARGE_WORDING, check code)",
  "accepted a1 a4 a5: accepted total 509000 -> 639000 cents, letter line 'Billed charges stated in these records: $6,390.00'",
  "export internal_notes_text: POSSIBLE OVERLAPS section present with records 7 and 2 and $1,300.00 / $650.00; letter_text has no 'overlap'",
  "removed the record-6 extract fixture in the scratch copy: tray [e6 rejected] -> [] after POST /records/r6/entry (201); excluded.rejected 0; letter has the manual quote, not the placeholder",
  "live probe on :7963 (claude-cli judge): six 'Estado de cuenta:' lines, reclassify each; accepted $50, $2,900, $1,600; letter total $4,550.00",
  "grepped the scratch copy's app/frontend for possible_overlaps: no match (only store.py, present.py, export.py, overlap.py)",
  "stopped both servers by PID and confirmed curl 000 on both ports"],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "totals_integrity": 3, "nothing_vanishes": 5},
 "findings": [
  {"severity": "major",
   "title": "'estado de cuenta' as a charge cue lets payment, copay and balance lines reach the total",
   "evidence": "amounts.py CHARGE_CUE_ES = r'\\b(?:cargos?|honorarios|estado\\s+de\\s+cuenta)\\b'; only saldo and sin cargo/gratis/no facturado are excluded (_NO_CHARGE_ES, BALANCE_CUE). Live probe on :7963 (artifacts/review-evidence/T-110-paralegal-r2-run3.py output): 'Estado de cuenta: copago de la paciente $50.00.' -> RECLASS a3 200 judge agree wording 'Estado de cuenta'; 'Estado de cuenta: pendiente de pago $2,900.00.' -> RECLASS a5 200 judge agree. After accept (run4.py): 'TOTAL LINE (probe) [Billed charges stated in these records: $4,550.00]', letter lines '$50.00' and '$2,900.00' with their quotes. Payment, adjustment and insurer-paid lines were refused only by the judge (JUDGE_DISAGREES).",
   "why_it_matters": "A statement of account lists payments, adjustments, copays and balances as well as charges. The code check is meant to be a hard first gate; here it passes every line on a statement, so the judge is the only barrier and it let a copay and an outstanding balance through. A balance in the total double counts the charges it restates (the same reason saldo is excluded). The adjuster will quote the $4,550 against the bills.",
   "fix": "Drop 'estado de cuenta' from CHARGE_CUE_ES (it names the document, like 'statement', which the English guard does not accept). For lib09 a5 use 'consultas' plus a statement context only if a separate rule is justified. Whatever stays, add refusals for pago, pagó, pagado, abono, copago, ajuste, crédito, descuento, deducible, pendiente, adeudo and balance-style 'monto adeudado' alongside saldo.",
   "acceptance_test": "Unit: charge_wording refuses each of the six probe sentences in artifacts/review-evidence/T-110-paralegal-r2-probe.txt except 'sesiones de fisioterapia $1,600.00' (which needs a charge word it does not have, so it is refused too). lib09 a5 behaviour is decided by Chris/the orchestrator; whichever way, a test pins it. Live eval: no probe line whose judge answer is agree reaches the letter total without a cue the code accepts."},
  {"severity": "minor",
   "title": "The demo cannot perform the lib09 consultas reclassification: no recorded judge answer",
   "evidence": "On :7962 (curated fixtures) POST /items/a5/reclassify {to: charge} returned 422 detail {reason: JUDGE_UNAVAILABLE, check: judge, error_class: LLMFailedFixtureMiss}. It only worked after I wrote a stand-in fixture for the missed key in my scratch copy. The unit test uses FakeCall(J2('agree')) (tests/unit/test_lib09_t110_r2.py:44).",
   "why_it_matters": "The demo is what Chris shows. Step 1 of this review works only with a judge answer no one has recorded, and the real judge's answer on a5 itself has not been seen (the earlier recorded answer for class unclear was SHOULD_BE_CHARGE).",
   "fix": "Record the real j2 answer for lib09 a5 with class charge into the curated set, and say in the handoff what it was. If the real judge disagrees, say so and keep the unit test honest.",
   "acceptance_test": "Fixture-backend e2e: lib09 a5 reclassify returns 200 on the curated set, total reads $6,390.00 after accept, with no FakeCall."},
  {"severity": "minor",
   "title": "The overlap warning still reaches the paralegal only at export, not on the review screen",
   "evidence": "grep of the scratch copy's app/frontend for 'possible_overlaps' returns nothing; the only consumers are store.py, present.py, export.py, overlap.py. The notes section works (run2.py output).",
   "why_it_matters": "She decides whether to accept both lines while reviewing. The warning that those two may overlap appears only after she exports, and it is written for the export. The first-round fix asked for both.",
   "fix": "Open the frontend card the worker mentioned: show each overlap beside the charges total with both excerpts and a dismiss action.",
   "acceptance_test": "E2E on lib09 after a5 is promoted: the charges panel shows the $1,300.00 vs $650.00 warning."},
  {"severity": "minor",
   "title": "Consulta $650.00 stays unreachable, and the notes still send her to 'Request clean copy of bill'",
   "evidence": "lib09 a2 reclassify -> 422 NO_CHARGE_WORDING (code). With a2 accepted, internal notes: 'Record 2 (...): \"Consulta: $650.00.\" Amount unclear ($650.00). Request clean copy of bill.'",
   "why_it_matters": "The same unchanged problem as round 1: she can read the figure and the quote; the note sends her to ask for a bill instead. 'Consulta' is a charge in a note whose sentence says 'Consulta: $650.00'. The tool may be right to refuse, but the note should say 'not classified; check the original', not 'request a clean copy'.",
   "fix": "Change the NOT TOTALED wording for a Spanish unclear figure to 'Not classified as a charge; check the original quote'.",
   "acceptance_test": "Unit: the export note for a Spanish unclear amount does not contain 'clean copy'."}
 ],
 "whats_right": [
  "The rate cue is shared and decisive: both $400 lines are rates, are refused without a judge call, and never reach the total.",
  "The saldo and negation refusals hold, and an unclear figure is never totaled until she reclassifies and accepts.",
  "The overlap note is internal-only, names both records and both amounts, and leaves the letter's total line untouched (D-019)."],
 "questions_for_chris": []}
```
