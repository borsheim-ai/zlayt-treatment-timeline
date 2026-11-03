# T-110 round 3: paralegal-reviewer (commit e8e6955)

Verdict: pass. No blockers, no majors. Two minors on the same new guard, both on the reclassify path only.

Setup: `git archive e8e6955` extracted into the scratchpad (`.../scratchpad/r3`). Server on port 7972 (`ZLAYT_MODE=local`, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, scratch DB), stopped by PID (`kill $(cat server.pid)`; curl then returned 000). Probe scripts: `artifacts/review-evidence/T-110-paralegal-r3-run1.py`, `run2.py`, `T-110-paralegal-r3-mutate.py`; export text `T-110-paralegal-r3-export.txt`. Related unit tests in the archive copy: `425 passed, 1993 deselected`.

## Your three checks

1. **Every line of my r2 probe returns None from `charge_wording`: confirmed.** All six probe lines (pago recibido, ajuste del seguro, copago, el seguro pagó, pendiente de pago, and the sesiones/costo por sesión line) printed `None`. The `$400.00` on the last line is `None` too.
2. **"consultas $1,300" reclassifies on the recorded judge fixture; total $6,390: confirmed.** lib09 a5 on the fixture backend: `RECLASS a5 $1,300.00 -> 200 kind charge judge agree wording Estado de cuenta: consultas`, with no FakeCall and no stand-in fixture from me. After accepting a1, a4, a5: `accepted-total after {'cents': 639000, 'count': 3}` and the letter line `Billed charges stated in these records: $6,390.00`. a2, a3, a6, a7 all returned 422 `NO_CHARGE_WORDING` (check `code`). The recorded fixture `tests/fixtures/llm/4f6294...json` is stamped `claude-haiku-5-5` via `claude-cli`.
3. **The notes no longer say "Request clean copy of bill": confirmed.** With a2 ($650) and a7 ($2,900) accepted, `"clean copy" in notes` is False. The notes read: `"Consulta: $650.00." Not classified as a charge ($650.00); check the original quote.` and the same for `"Saldo: $2,900.00."`. The POSSIBLE OVERLAP note for $1,300 vs $650 is still in the internal notes only.

## Side effect: "sesiones de fisioterapia $1,600" on a statement is now refused

I ran it: `None | $1,600.00 | Estado de cuenta: sesiones de fisioterapia $1,600.00.` Also refused: radiografías $480, resonancia magnética $2,150, sala de emergencias $6,240 on an "Estado de cuenta:" line.

**As a default for this release: acceptable.** The figure stays `unclear`, is never totaled, and the note now points her to the original quote. Nothing is invented or lost, and the payment, copay, balance and adjustment lines from round 2 can no longer reach the total. That beats the round 2 behavior, where the judge was the only barrier and it missed two of five.

**But it is a dead end for a real charge.** The only Spanish statement line that can be promoted is one that says the literal word `consultas` (`_SERVICE_LINE_ES = re.compile(r"\bconsultas\b")`, amounts.py). That is one noun fitted to the lib09 fixture. A paralegal with a Spanish statement listing therapy, imaging or ER charges has no way to get them into the total except to retype them elsewhere. That is a minor, not a blocker, because the safe side holds.

**Narrowest fix (mutation-tested in a scratch copy, not in the repo).** Keep the payment/balance precedence exactly as it is. Replace the single noun with a short list of billed-service nouns: `consultas|sesiones|fisioterapia|terapia|radiograf\w+|resonancias?|tomograf\w+|urgencias|ambulancia`. With that change, all five payment-side probe lines still return `None`, `Estado de cuenta: sesiones de fisioterapia $1,600.00.` returns `'Estado de cuenta: sesiones'`, radiografías and resonancia pass, and "sala de emergencias" still fails (not in the list). `test_estado_de_cuenta_is_context_never_a_cue_on_its_own` asserts `None` for the sesiones line and must be updated with it.

## Second side effect, found while probing

The widened `BALANCE_CUE` also lists bare `seguro|insurance|insurer`, and `reclassify.py:78` applies it to English sentences. At d24ff07 these returned a wording; at e8e6955 they return None:
- `ER billed charges $6,240, submitted to insurance.` (was `billed`)
- `MRI charge: $2,150, billed to the patient's insurer.` (was `charge`)
- `Cargos: radiografías $480.00 (seguro médico).` (was `Cargos`)

A charge sentence that names the payer is normal. The bare words add nothing to the probe: each payment-side probe line is already caught by `pag*`, `ajuste`, `adjust*` or `paid`. In the same scratch copy, removing `seguro|insurance|insurer` from `BALANCE_CUE` left all five probe lines `None` and restored the three lines above. This only matters when the classifier left an English figure unclear and she reclassifies it; the classifier does not read `BALANCE_CUE` (only `reclassify.py:78` does).

Carry-over, unchanged by this commit: the overlap warning still has no frontend consumer (`grep -rl possible_overlaps app/frontend` in the archive returns nothing). It reaches her only in the export notes. That was my round 2 minor 3; it stays open.

```json
{"card": "T-110", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit e8e6955 via git archive; own server :7972 (fixture backend, curated set, ZLAYT_MODE=local, scratch DB); library case_lib09_spanish_interpreter_espalda; r2 probe lines plus extra statement lines; mutation test in a scratch copy",
 "exercised": [
  "read personas/paralegal.md, reviews/T-110-paralegal-r2.md, git show e8e6955 (amounts.py, export.py, tests/unit/test_lib09_t110_r2.py, the recorded judge fixture)",
  "charge_wording on all six r2 probe lines via a -I script against the archive copy: all None",
  "charge_wording on extra lines: consultas passes, sesiones/radiografias/resonancia/sala de emergencias on an Estado de cuenta line all None",
  "lib09 on :7972: a5 reclassify 200 judge agree wording 'Estado de cuenta: consultas'; a2 a3 a6 a7 422 NO_CHARGE_WORDING; accept a1 a4 a5 -> 639000 cents; letter 'Billed charges stated in these records: $6,390.00'",
  "accepted a2 and a7, GET export: internal notes carry 'Not classified as a charge ($650.00); check the original quote.', no 'clean copy'",
  "diffed charge_wording on seven English/Spanish lines between d24ff07 and e8e6955: three payer-naming charge sentences now None",
  "mutation test in a scratch copy: removed seguro|insurance|insurer from BALANCE_CUE and widened _SERVICE_LINE_ES; probe lines still None, sesiones/radiografias/resonancia pass, payer lines restored",
  "pytest tests/unit -k 'amount or reclass or charge or lib09 or export or totals' in the archive copy: 425 passed",
  "grepped archive app/frontend for possible_overlaps: no match",
  "stopped the server by PID; curl returned 000"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "totals_integrity": 5, "nothing_vanishes": 5},
 "findings": [
  {"severity": "minor",
   "title": "Only the literal word 'consultas' can promote a Spanish statement line; other real service charges are a dead end",
   "evidence": "amounts.py: _SERVICE_LINE_ES = re.compile(r'\\bconsultas\\b'). Probe in the archive copy: 'Estado de cuenta: sesiones de fisioterapia $1,600.00.' -> None; 'Estado de cuenta: radiografías $480.00.' -> None; 'Estado de cuenta: resonancia magnética $2,150.00.' -> None. After a mutation widening the noun list: sesiones, radiografías and resonancia return a wording; the five payment-side probe lines still return None.",
   "why_it_matters": "The refusal is the safe default (unclear, not totaled, note says check the original quote), but a paralegal with a Spanish statement of therapy or imaging charges cannot get them into the stated-charges total at all. The allow-list is one noun fitted to one fixture.",
   "fix": "Replace _SERVICE_LINE_ES with a short list of billed-service nouns (consultas, sesiones, fisioterapia, terapia, radiograf*, resonancia, tomograf*, urgencias, ambulancia). Keep the BALANCE_CUE and rate-cue precedence as is, so the judge stays a second gate and not the only one. Update test_estado_de_cuenta_is_context_never_a_cue_on_its_own, which currently pins the sesiones line to None.",
   "acceptance_test": "Unit: charge_wording returns None for the five payment-side probe lines (pago recibido, ajuste del seguro, copago, el seguro pagó, pendiente de pago) and a wording for 'Estado de cuenta: sesiones de fisioterapia $1,600.00.' and 'Estado de cuenta: radiografías $480.00.'"},
  {"severity": "minor",
   "title": "Bare 'seguro / insurance / insurer' in BALANCE_CUE now refuses ordinary charge sentences that name the payer",
   "evidence": "amounts.py BALANCE_CUE ends '...descuentos?|deducibles?|seguro|insurance|insurer|contractual|write-?offs?'; reclassify.py:78 applies it to English too. charge_wording at d24ff07 vs e8e6955: 'ER billed charges $6,240, submitted to insurance.' 'billed' -> None; \"MRI charge: $2,150, billed to the patient's insurer.\" 'charge' -> None; 'Cargos: radiografías $480.00 (seguro médico).' 'Cargos' -> None. Mutation (seguro|insurance|insurer removed): all three restored, all five payment-side probe lines still None.",
   "why_it_matters": "A charge sentence naming the payer is common in bills and notes. The refusal is the safe side, but it is a regression against round 2 and the words add no protection: pag*, ajuste, adjust*, paid and copago already catch every payment-side line in my probe.",
   "fix": "Remove seguro, insurance and insurer from BALANCE_CUE. Keep the specific payment and adjustment words.",
   "acceptance_test": "Unit: charge_wording returns a wording for 'ER billed charges $6,240, submitted to insurance.' and 'MRI charge: $2,150, billed to the patient's insurer.' and still returns None for 'Estado de cuenta: ajuste del seguro $500.00.' and 'Estado de cuenta: el seguro pagó $4,000.00.'"}
 ],
 "whats_right": [
  "Payment, balance, adjustment and copay wording now beats every charge cue in English and Spanish, so the judge is no longer the only barrier and the total stayed at explicit charges.",
  "The lib09 consultas step now works end to end on the fixture backend with a recorded real-judge answer: reclassify 200, accept, total $6,390.00, no parenthetical.",
  "The Spanish unclear note says 'Not classified as a charge; check the original quote' instead of sending her to request a clean copy, and the overlap note stays in the internal block only."],
 "questions_for_chris": []}
```
