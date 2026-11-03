# T-085 round 3: legal-nurse-reviewer (Spanish-language records, D-048 fail-safe routing)

Verdict: **fail**. Two blockers, two majors, two minors.

Tested tree: `git archive HEAD` (e7a1987) extracted to a new empty scratchpad directory (`t085r3`). The shared tree was not touched. Python was the project `.venv`, run with `-I` and an explicit `sys.path` to the archive.

## The three counts (60 fresh lines I wrote after reading r2 and D-048)

The 60 lines: 14 unaccented Spanish, 10 English-leading mixed, 6 Italian, 6 Portuguese, 6 French, 6 German, 6 Spanish abbreviation lines, and 6 lab/imaging header lines (3 Spanish, 1 each Italian, German, Portuguese). All 60 are non-English.

| Gate | Result | Gate value |
|---|---|---|
| Non-English lines routed as English | **0 of 60** | 0, met |
| Italian, Portuguese, French or German routed as Spanish | **1 of 27** ("Suspeita de hernia discal L4-L5." is Portuguese, routed `es`) | 0, **not met** |
| Dropped hedge or negation on a mixed line that passes the checks | **4 of 41** unfaithful mixed pairs | 0, **not met** |

Supplementary set (36 more cognate-heavy PT/IT/FR lines): 2 more leak to Spanish ("Hernia discal L5-S1 com compressao radicular." and "Cervicalgia post-traumatica."). Combined: 3 of 63 fresh foreign lines routed Spanish.

Confusion matrix for the 60 (label to route): es 12 uncertain, 11 es; mixed 4 uncertain, 6 es; it 4 other, 3 uncertain; pt 5 other, 1 es, 1 uncertain; fr 4 other, 2 uncertain; de 3 other, 4 uncertain.

## Review load from `uncertain`

- My 33 Spanish and mixed lines: 16 uncertain (48%).
- The shipped held-out file, Spanish and mixed rows: 35 of 84 uncertain (42%). By length: under 40 chars 29 of 61 (48%); 40 to 150 chars 5 of 17 (29%); over 150 chars 1 of 6 (17%).
- Realistic notes route fine: in `evals/library/case_lib09` (Spanish interpreter case) all 3 Spanish records are `es`.
- The load is concentrated in short fragments, one-line diagnoses, drug lines and lab/imaging headers. Roughly one in two such lines gets LANGUAGE_UNCERTAIN: it is labeled, never verified and carries a per-record warning.
- It is acceptable under D-048 because the paralegal accepts, edits or dismisses every entry anyway. The cost is the loss of the `verified` badge and a warning list that grows with the number of fragments.
- The wrong-direction cost is separate (see major 2): English records that become `uncertain` or `es`.

## Blocker 1: a stray English word in the summary satisfies the hedge or negation check, so a dropped qualifier passes

Both mechanisms are in `app/backend/spanish_text.py`.
- `_EN_HEDGE_EXTRA` includes `impress\w+` (line 63). Any summary containing "impression" counts as carrying a hedge.
- The negation check accepts any English negation word anywhere in the summary. "negative" in "CT head negative" satisfies "sin pérdida de conocimiento". The check is not tied to the clause.

Mixed lines that pass `check_summary` and reach `verified` (pre-judge) or only `needs_review` via LANGUAGE_UNCERTAIN:

| Route | Quote | Summary | Result |
|---|---|---|---|
| es | `CT head negative; sin perdida de conocimiento.` | `CT head negative.` | `[]`, verified |
| es | `Dx: concussion sin perdida de conocimiento; CT head negative.` | `Dx: concussion; CT head negative.` | `[]`, verified |
| es | `RM lumbar: protrusion L4-L5. Impression: posible compresion radicular.` | `Lumbar MRI: L4-L5 protrusion. Impression: nerve root compression.` | `[]` |
| uncertain | `Impression: probable strain; sin fractura.` | `Impression: strain; no fracture.` | `[]`, needs_review only |

The same mechanism on pure Spanish lines that route `es`:
- `RM de rodilla derecha. Impresion: posible desgarro del menisco medial.` with summary `Right knee MRI impression: medial meniscus tear.` returns `[]`.
- `Diagnóstico: esguince cervical y conmoción cerebral sin pérdida de conocimiento. TAC craneal negativo.` with summary `Diagnosis: cervical sprain and concussion. CT head negative.` returns `[]`.
- `Paciente con conmocion cerebral, sin perdida de conocimiento, TAC de cabeza negativo y dolor cervical 7/10.` with summary `Patient with concussion, CT head negative, neck pain 7/10.` returns `[]`.

The English path catches the English equivalent: `grounding.check_summary('Dx: concussion; CT head negative.', 'Dx: concussion without loss of consciousness; CT head negative.')` returns `['SUMMARY_DROPS_QUALIFIER']`. The Spanish module does not.

Why this is a blocker (persona section 5):
- "Without loss of consciousness" is dropped from a concussion diagnosis.
- A hedge ("posible") is converted into a conclusion.
- "Impresión" is the standard heading on imaging reports, and a translation of it will normally be "impression", so this is the likely case and not a contrived one.
- It misses the D-048 intent: the union is supposed to catch a dropped "posible" whichever language leads.

Fix:
1. Remove `impress\w+` from the summary-side hedge test. Keep it on the quote side only, as the Spanish cue "impresiona".
2. Bind the negation and hedge checks to the clause: for each quote negation or hedge cue, require an English negation or hedge word in the summary within the same sentence or clause. Where a quote has a negation and the summary has negation words only in a different clause, flag it.
3. Add a specific rule: Spanish "sin pérdida de conocimiento/conciencia", "niega pérdida de conocimiento" and "no loss of consciousness" require "without loss of consciousness" or "no loss of consciousness" in the summary. Mirror the English LOC rule.
4. Add these 7 pairs as regression tests.

Acceptance test: the 7 pairs above return `SUMMARY_DROPS_QUALIFIER`, and the 6 faithful controls in my set still return `[]`.

## Blocker 2: Portuguese and Italian lines still route to Spanish, and the result is labeled Spanish and verified

- `language.record_lang({'excerpt': 'Suspeita de hernia discal L4-L5.'})` returns `es`.
- `generator.extract_one` with a fake model (summary `Disc herniation at L4-L5.`) gives steps `['extract_es']`, state `verified`, reasons `[]`, `source_language_name` "Spanish", label "AI translation".
- The Portuguese hedge "Suspeita" (suspicion) is not in the Spanish cue list, so the unhedged summary passes. A hedge becomes a conclusion, and the label names the wrong source language.
- Also routed `es` in the supplementary set: "Hernia discal L5-S1 com compressao radicular." (Portuguese, `com` and `compressao` present) and "Cervicalgia post-traumatica." (Italian). The second is nearly identical to Spanish, which is the case the margin rule is meant to send to `uncertain`.
- The language.py docstring says "Italian, Portuguese, French and German never route to Spanish". My gate is 0 and the observed rate is 3 of 63. The 206-row file reports 0 of 86 foreign rows to `es`, so the file overstates safety.

Fix:
- When Spanish evidence is made only of words shared across the Romance lists (`hernia`, `discal`, `cervicalgia`), require at least one Spanish-only function word or stem before routing `es`; otherwise `uncertain`.
- Treat any Portuguese-only function word (`com`, `suspeita`, `compressao`, `sem`, `nao`) as non-Spanish evidence that blocks `es` unless Spanish clearly dominates.
- Cheaper and stronger: the model `source_language` self-report from r2 (not adopted). A model that says "Portuguese" would upgrade the record to `other` or `uncertain`.

Acceptance test: the 3 lines above plus the 60-line set return `other` or `uncertain`, with 0 routed `es`.

## Major 1: Spanish cue lists still miss common hedge, negation, self-report and approximation words

The author added the six r2 words. Fresh words fail. 20 fresh Spanish pairs: 13 return `[]` (the code check passes). Seven of those route `es` and reach `verified` pre-judge:

| Quote | Summary |
|---|---|
| `Esguince cervical a valorar.` | `Cervical sprain.` |
| `Exento de fractura en radiografia.` | `Fracture on x-ray.` |
| `La paciente cuenta que se cayo de la escalera.` | `Fell from the stairs.` |
| `Sostiene que el dolor empezo tras el choque.` | `Pain began after the collision.` |
| `Al interrogatorio, dolor 7/10 en cuello.` | `Neck pain 7/10.` |
| `Casi 40% de limitacion de rango.` | `40% range limitation.` |
| `Rango de movimiento ca. 40% reducido.` | `Range of motion reduced 40%.` |

Six more return `[]` but are held only by LANGUAGE_UNCERTAIN: "pareciera", "habria", "supuesto", "cabe sospechar", "indemne de", "en torno a". "Exento de fractura" summarised as "Fracture on x-ray" is a negation turned into a finding.

Why major, not blocker: it is the same class as r2 major 2 and the cue lists are a known incomplete layer with the translation judge behind them. I did not run the judge (live eval is opt-in). If a 2-round-old finding keeps recurring with new words, the lists need a clinical source and not an authoring pass.

Fix: add exento/a de, a valorar, cuenta que, sostiene, interrogatorio, casi, ca., en torno a, pareciera, habría, supuesto, indemne, cabe sospechar; have the researcher (lexicon owner) review the Spanish lists against a Spanish clinical source.

Acceptance test: the 13 pairs above return a drop reason.

## Major 2: Plain English records are routed `uncertain` or `es` by one stray foreign-list word

Evidence (detect on plain English text I wrote):

| Text | Route | Reason |
|---|---|---|
| `Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. ...` (lib09 record 1, 38 words, en score 0.53) | uncertain | "could be Spanish or French": the word `son` |
| `Patient tolerated the operation well and was discharged home.` | uncertain | `operation` is in the German list |
| `Pain plus numbness in the right hand. Follow up in four weeks.` | uncertain | `plus` |
| `MRI: small hernia at L5-S1, mild vertebral body edema, no radicular signs.` | **es** | |
| `Patient was walking solo when struck by a vehicle. Complains of left hip pain.` | **es** | `solo` |
| `Radiology: eventual follow-up recommended. Findings: no acute fracture.` | **es** | `eventual` |

- 92 words in the foreign lists are ordinary English dictionary words (checked against `/usr/share/dict/words`), including `son`, `operation`, `plus`, `solo`, `eventual`, `hernia`, `basal`, `vertebral`, `radicular`, `discal`, `visita`, `mas`, `par`.
- Once `foreign_only > 0`, `detect` has no path that returns `en`, however much English there is. A 38-word English ER note with `en` 0.53 vs `fr` 0.05 comes out `uncertain`.
- Consequences: an English quote gets the Spanish prompt, the "AI translation" label and a LANGUAGE_UNCERTAIN warning, or is labeled as a Spanish translation, and the English-only checks (the stronger set) do not run.
- Scale: on the 27 repo case files (182 records) 177 stay `en`. The one false `uncertain` is the record above. So realistic rate is low, but the held-out file has only 38 English rows (18%) with none of these words, so it cannot show this.

Fix: return `en` when English evidence clearly dominates (for example `en` score at least 3 times the best foreign score and at least 8 English function words), whatever stray words appear. Add the collision words to `_ENGLISH_OK`. Add 30 or more English rows containing them to the held-out file.

Acceptance test: the 6 lines above route `en`, and the held-out file has at least 60 English rows with 0 routed `es` and at most 5% `uncertain`.

## Minor 1: The held-out file is a good instrument, but its claims run ahead of what it shows

I read all 206 rows. The labels are sound: no Spanish row is really Portuguese and no English row is really foreign. Problems:
- The docstring says "186 one-liners"; the file has 206 rows.
- 30 rows are in-sample (28 `reviewer_probe`, 2 `tuned_after_miss`).
- "authored" and "authored_batch2" were written, and the lists extended, in one commit (e7a1987). The git history cannot show the order, so the held-out claim rests on the docstring. My 60 lines are the actual out-of-sample measure: 1 of 27 foreign leak against the file's 0 of 86.
- Some Spanish labels are inherently shared with English or Portuguese ("Ibuprofeno 400 mg.", "Hernia L5-S1.", "TAC normal."). The file has no ambiguity class, so it counts `uncertain` as correct for them but gives no way to say a line has no right answer.
- `safe >= 0.95` as the aggregate floor would allow 10 unsafe lines. The separate zero-leak tests make this harmless today; keep them.
- The file measures routing only. Mixed-line qualifier loss is covered by 12 author-written pairs (the `test_mixed_and_new_cue_quotes...` tests), which is why blocker 1 passed 1814 tests.

Fix: correct the docstring, mark in-sample rows, add an English-collision block, and add 40 or more mixed-line qualifier pairs authored by someone who has not read `spanish_text.py`. This is a "should" item.

## Minor 2 (I would have done it differently, not a spec violation): offer a model self-report to cut the review load

Roughly 48% of short Spanish fragments land `uncertain`. The r2 suggestion of a `source_language` field in the extract output (accepting `es` only when the model and the detector agree, and escalating to `uncertain` or `other` when they disagree) would turn most of these into `es` with no loss of safety, and would also close blocker 2. D-048 chose pure fail-safe routing; I flag the alternative once.

## What I exercised

On the clean archive of e7a1987:
- `pytest tests/unit` with `LLM_BACKEND=fixture`: 1814 passed, 4 skipped.
- `python -m tests.unit.test_language_routing_heldout`: safe 98.1%, exact 67.5%, n=206.
- Read `language.py`, `spanish_text.py`, the routing and verify code in `generator.py`, and `test_language_routing_heldout.py` in full; read all 206 held-out rows.
- 60-line fresh set (`lines60.py`) through `language.record_lang` and `detect`.
- 36 supplementary PT/IT/FR lines.
- 42 mixed and 20 Spanish-cue unfaithful pairs plus 6 faithful controls, each through `generator.extract_one` with `FakeCall` (route, check reasons, state); 13 extra probes on the LOC and Impression mechanisms, comparing `grounding.check_summary` with `spanish_text.check_summary`.
- 10 plain English collision lines through `detect`; a dictionary scan of the foreign word lists.
- `language.annotate` equivalent over the 27 `evals/library` and `evals/golden` case files; `python -m app.pipeline` on `case_lib09_spanish_interpreter_espalda.txt` (rc 0, no traceback; record 1 had LLM_FAILED_AFTER_RETRIES under the fixture backend, expected).
- Not run: the live translation-judge eval (opt-in, about 55 calls). The judge is the third rung and I make no claim about it.

```json
{"card": "T-085", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD e7a1987 via git archive in the scratchpad (t085r3); app/backend/{language,spanish_text,generator}.py, tests/unit/{test_language_routing_heldout.py,language_routing_heldout.jsonl}; D-048; 60 fresh lines (Spanish unaccented, English-leading mixed, IT/PT/FR/DE, abbreviations, lab/imaging headers) plus supplementary probes; evals/library case_lib09 Spanish case",
 "exercised": [
  "git archive HEAD (e7a1987) extracted to scratchpad t085r3; git worktree not used",
  "pytest tests/unit with LLM_BACKEND=fixture: 1814 passed, 4 skipped",
  "python -m tests.unit.test_language_routing_heldout: safe routing 98.1%, exact 67.5%, n=206 (en 34/4 uncertain, es 37 es/33 uncertain, mixed 12/2, it/pt/fr/de all other or uncertain)",
  "lines60.py: 60 fresh lines through language.record_lang/detect: 0 non-English routed en; 1 of 27 IT/PT/FR/DE routed es ('Suspeita de hernia discal L4-L5.' pt)",
  "36 supplementary PT/IT/FR cognate-heavy lines: 2 routed es ('Hernia discal L5-S1 com compressao radicular.', 'Cervicalgia post-traumatica.')",
  "pairs.py and pairs2.py: 42 mixed-line unfaithful pairs (41 counted as hedge/negation/self-report/approx/laterality drops) plus 6 faithful controls through generator.extract_one with FakeCall; 4 hedge/negation drops pass the checks (2 verified with es route plus 1 es-routed Impression and 1 uncertain)",
  "extra.py and extra2.py: 'CT head negative' / 'Impression' satisfier probes; spanish_text.check_summary vs grounding.check_summary on concussion-without-LOC pairs, pure Spanish and mixed",
  "20 fresh Spanish cue-gap pairs: 13 return [] (7 route es and reach verified pre-judge)",
  "10 plain English collision lines through detect: 3 routed es, 5 uncertain; dictionary scan of foreign word lists found 92 ordinary English words",
  "annotate-equivalent over 27 evals/library and evals/golden case files: 177 en, 3 es, 1 uncertain (English lib09 record 1, 'son'), plus 2 en records of the Spanish case",
  "python -m app.pipeline on case_lib09_spanish_interpreter_espalda.txt: rc 0, no traceback",
  "Read all 206 rows of language_routing_heldout.jsonl and audited labels; read language.py, spanish_text.py, generator.py routing/verify, and the held-out test file",
  "Not run: live translation judge eval (opt-in, about 55 model calls)"
 ],
 "verdict": "fail",
 "scores": {"non_english_never_english": 5, "foreign_never_spanish": 3, "mixed_line_union_checks": 3, "spanish_cue_lists": 3, "english_false_routing": 3, "heldout_set_quality": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A stray English word in the summary satisfies the hedge or negation check, so a dropped 'posible' or 'sin perdida de conocimiento' passes (4 of 41 mixed pairs; same on pure Spanish)",
   "evidence": "spanish_text.py:63 _EN_HEDGE_EXTRA contains impress\\w+; negation is satisfied by any English negation word anywhere in the summary. check_summary returns [] for: 'CT head negative; sin perdida de conocimiento.' -> 'CT head negative.' (es, verified); 'Dx: concussion sin perdida de conocimiento; CT head negative.' -> 'Dx: concussion; CT head negative.' (es, verified); 'RM lumbar: protrusion L4-L5. Impression: posible compresion radicular.' -> '... Impression: nerve root compression.' (es); 'Impression: probable strain; sin fractura.' -> 'Impression: strain; no fracture.' (uncertain, needs_review only). Pure Spanish: 'RM de rodilla derecha. Impresion: posible desgarro del menisco medial.' -> 'Right knee MRI impression: medial meniscus tear.' [], and 'Diagnóstico: esguince cervical y conmoción cerebral sin pérdida de conocimiento. TAC craneal negativo.' -> 'Diagnosis: cervical sprain and concussion. CT head negative.' []. English path: grounding.check_summary('Dx: concussion; CT head negative.', 'Dx: concussion without loss of consciousness; CT head negative.') -> ['SUMMARY_DROPS_QUALIFIER'].",
   "why_it_matters": "Persona section 5: 'without loss of consciousness' dropped from a concussion diagnosis, and a hedge converted into a conclusion. 'Impresión' is the standard imaging-report heading, so 'impression' in a translated summary is the expected output. D-048's stated intent (union of checks catches a dropped 'posible' whichever language leads) is not met. Gate: 0 dropped hedges or negations on mixed lines that pass; measured 4 of 41.",
   "fix": "Remove impress\\w+ from the summary-side hedge test (keep it quote-side). Bind negation and hedge checks to the clause or sentence: a quote negation or hedge must be matched by an English negation or hedge word in the same sentence of the summary. Add a Spanish LOC rule mirroring the English one ('sin/niega pérdida de conocimiento/conciencia' requires 'without/no loss of consciousness'). Add the 7 pairs as regression tests.",
   "acceptance_test": "The 7 pairs return SUMMARY_DROPS_QUALIFIER; the 6 faithful controls ('CT head negative; without loss of consciousness.' etc.) still return []; a held-out file of 40+ mixed-line qualifier pairs written by someone who has not read spanish_text.py shows 0 misses."},
  {"severity": "blocker",
   "title": "Portuguese and Italian lines still route to Spanish; the result is labeled Spanish and verified, with the Portuguese hedge dropped (3 of 63 fresh foreign lines; 1 of 27 in the 60-line set)",
   "evidence": "language.record_lang({'excerpt': 'Suspeita de hernia discal L4-L5.'}) -> es. generator.extract_one with FakeCall (summary 'Disc herniation at L4-L5.') -> steps ['extract_es'], state verified, reasons [], source_language_name 'Spanish', label 'AI translation'. Also es: 'Hernia discal L5-S1 com compressao radicular.' (pt), 'Cervicalgia post-traumatica.' (it). language.py docstring: 'Italian, Portuguese, French and German never route to Spanish'. The 206-row file reports 0 of 86 foreign rows to es.",
   "why_it_matters": "Gate: 0 IT/PT/FR/DE routed Spanish; measured 1 of 27 (3 of 63 with supplementary). A Portuguese 'suspeita' (suspicion) is not in the Spanish cue list, so the unhedged summary passes and the record carries verified status and the wrong source-language label. Persona section 5: hedge converted into a conclusion.",
   "fix": "Do not route es on evidence made only of Romance words shared across languages (hernia, discal, cervicalgia): require a Spanish-only function word or stem. Treat Portuguese-only function words (com, sem, nao, suspeita, compressao) as blocking evidence unless Spanish clearly dominates. Optionally add the model source_language self-report from r2.",
   "acceptance_test": "'Suspeita de hernia discal L4-L5.', 'Hernia discal L5-S1 com compressao radicular.', 'Cervicalgia post-traumatica.' and the 60-line set route other or uncertain, 0 to es; a 40+ held-out PT/IT line set written without reading the lists shows 0 routed es."},
  {"severity": "major",
   "title": "Spanish cue lists still miss common hedge, negation, self-report and approximation words (13 of 20 fresh pairs return [])",
   "evidence": "check_summary returns [] for: 'Esguince cervical a valorar.'->'Cervical sprain.'; 'Exento de fractura en radiografia.'->'Fracture on x-ray.'; 'La paciente cuenta que se cayo de la escalera.'->'Fell from the stairs.'; 'Sostiene que el dolor empezo tras el choque.'->'Pain began after the collision.'; 'Al interrogatorio, dolor 7/10 en cuello.'->'Neck pain 7/10.'; 'Casi 40% de limitacion de rango.'->'40% range limitation.'; 'Rango de movimiento ca. 40% reducido.'->'Range of motion reduced 40%.' (all route es, state verified pre-judge). Six more (pareciera, habria, supuesto, cabe sospechar, indemne de, en torno a) route uncertain and pass the code check.",
   "why_it_matters": "Persona checklist items 5, 6, 14: hedges, self-report attribution and approximations are preserved. 'Exento de fractura' read as 'Fracture' is a negation turned into a finding. Same class as r2 major 2; the six r2 words were added but fresh words fail at 65%.",
   "fix": "Add exento/a de, a valorar, cuenta que, sostiene, interrogatorio, casi, ca., en torno a, pareciera, habría, supuesto/a, indemne, cabe sospechar. Have the researcher (lexicon owner) review the Spanish lists against a Spanish clinical source rather than extending them one probe at a time.",
   "acceptance_test": "The 13 pairs return a drop reason; a further 30 fresh pairs written by someone who has not seen the lists show at most 2 misses."},
  {"severity": "major",
   "title": "Plain English records are routed uncertain or es by one stray foreign-list word, getting the Spanish prompt, the 'AI translation' label and no English-only checks",
   "evidence": "detect on lib09 record 1 (English ER note, 38 words, scores en 0.5263 fr 0.0526): lang uncertain, reason 'could be Spanish or French'; the only foreign word is 'son' (\"patient's son\"). 'Patient tolerated the operation well and was discharged home.' -> uncertain (operation in the German list). 'Pain plus numbness in the right hand. Follow up in four weeks.' -> uncertain. 'MRI: small hernia at L5-S1, mild vertebral body edema, no radicular signs.' -> es. 'Patient was walking solo when struck by a vehicle. Complains of left hip pain.' -> es. 'Radiology: eventual follow-up recommended. Findings: no acute fracture.' -> es. A scan of the foreign word lists against /usr/share/dict/words finds 92 ordinary English words. On the 27 repo case files, 177 of 182 English-bearing records stay en; the held-out file has 38 English rows, none with these words.",
   "why_it_matters": "A mislabeled 'AI translation' on an English quote misstates the source, and an English record loses the English-only checks (the stronger set). The review load from the fail-safe is paid by English records too. Realistic rate is low on the repo corpus but the held-out file cannot see it.",
   "fix": "In detect, return en when English evidence clearly dominates (for example en score at least 3 times the best foreign score and at least 8 English function words), whatever stray words appear. Add the collision words to _ENGLISH_OK. Add 30+ English rows containing them to the held-out file.",
   "acceptance_test": "The 6 lines above route en; the held-out file has 60+ English rows with 0 routed es and at most 5% uncertain."},
  {"severity": "minor",
   "title": "The held-out file's claims run ahead of what it shows: stale count, in-sample rows, unverifiable authoring order, no ambiguity class, only qualifier pairs written by the author",
   "evidence": "tests/unit/test_language_routing_heldout.py docstring: '186 one-liners'; wc -l language_routing_heldout.jsonl = 206. 28 reviewer_probe rows and 2 tuned_after_miss rows (15%). Word lists, file and tests land in one commit (e7a1987), so 'authored before the first run' cannot be verified from git. My 60 fresh lines: 1 of 27 foreign to es, against the file's 0 of 86. Rows 'Ibuprofeno 400 mg.', 'Hernia L5-S1.', 'TAC normal.' are shared across languages. Aggregate floor safe >= 0.95 would allow about 10 unsafe lines. Mixed-line qualifier loss is covered by 12 author-written pairs, which is why blocker 1 passed 1814 tests. Label audit of all 206 rows: no mislabeled row found.",
   "why_it_matters": "A routing gate is only worth its held-out discipline. The file is a good instrument and the labels are sound, but the 'zero leak' headline should not be read as out-of-sample.",
   "fix": "Fix the docstring count, add an in_sample flag and report out-of-sample rates separately, add an 'ambiguous' label, add English-collision rows and 40+ mixed-line qualifier pairs authored independently. Keep the separate zero-leak tests.",
   "acceptance_test": "The report prints in-sample and out-of-sample rates separately and the docstring count equals the line count."},
  {"severity": "minor",
   "title": "I would have done it differently (not a spec violation): add a model source_language self-report to reduce the uncertain load and close the foreign-to-Spanish leak",
   "evidence": "Held-out file Spanish and mixed rows: 35 of 84 uncertain (42%), 48% under 40 characters. My 33 Spanish and mixed lines: 16 uncertain (48%). Realistic notes route fine (lib09: 3 of 3 Spanish records es).",
   "why_it_matters": "Each uncertain record loses the verified badge and adds a warning; the load is concentrated in short fragments, one-line diagnoses and lab/imaging headers. It is acceptable under D-048 but avoidable.",
   "fix": "Add a source_language field to the extract output; accept es when model and detector agree, escalate to uncertain or other when they disagree. Chris's call, not a defect.",
   "acceptance_test": "On the 60-line set uncertain share for Spanish lines drops below 25% with 0 foreign lines to es or en."}
 ],
 "whats_right": [
  "No non-English line in my 60 reached the English path (0 of 60); r2 had 14 of 40 Spanish and 9 of 40 foreign lines running as English.",
  "On mixed lines the union now works for the r2 probes and most fresh ones: 37 of 41 unfaithful mixed pairs were flagged with 0 false positives on 6 faithful controls (hedge 'posible', 'patient states', 'per patient', laterality, approx, 'no se descarta').",
  "The 206-row held-out file, its confusion matrix and the separate zero-leak tests are the right instrument; labels audited sound, and the 27-file English corpus stays 177 of 182 en."
 ],
 "questions_for_chris": []}
```
