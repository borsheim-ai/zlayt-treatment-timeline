# T-085 round 2: legal-nurse-reviewer (Spanish-language records)

Verdict: **fail**. Two blockers, three majors, two minors.

Tested tree: `git archive HEAD` (9c1af01, which contains 1b1c711) extracted to the scratchpad. Reviewers cannot use `git worktree`, so the shared tree was not touched.

## Round-1 items

| Item | Result |
|---|---|
| `python -m app.pipeline` crash | Fixed. The sample and lib09 run to completion with rc 0. A French file is refused with `refused: unsupported_language (French)` and rc 1. The full unit suite passes: 1569 passed, 4 skipped. |
| Short Spanish lines detected and labeled | Partly fixed. 20 of 22 fresh lines resolve to es or uncertain. But 14 of 40 further unaccented, cognate-heavy lines resolve to `unknown` (English), and mixed English/Spanish lines can resolve to `en`. See blocker 1. |
| FR/PT/IT/DE short lines refused or uncertain | Partly fixed. 31 of 40 fresh lines are refused or uncertain. 9 run as English, and an Italian line is labeled Spanish. See blocker 2. |
| "No se descarta fractura" cannot pass as "Fracture ruled out" | Fixed. 9 fresh variants all behave correctly. These include "no descartada", "no descartable", "sin descartar", "pendiente descartar", "aún no se ha descartado", and "cabría descartar". The inverse direction is also correct: "Se descarta" with "cannot be excluded" is flagged. |
| Cue words added | Mostly. All 13 round-1 words work. New hedge and self-report words still miss. See major 2. |
| 54-pair token-check eval | Sound as a deterministic regression, but not as independent measurement. See minor 1. |

## What I exercised

On the clean archive:
- `pytest tests/unit`.
- CLI runs on the golden sample, lib09 (Spanish) and a French file.
- `generator.extract_one` with a fake model on four lines, to see the path, the label and the state.
- About 20 fresh Spanish detection lines.
- 40 further Spanish lines.
- 40 fresh FR/PT/IT/DE lines, plus 17 earlier ones.
- 58 `check_summary` probes: not-ruled-out variants, diacritics stripped, abbreviations, hedges, negations, numbers, laterality, dates, mixed text.

## Blocker 1: Spanish text is still routed to the English path, unlabeled, with hedge, side and severity checks skipped

Two routes lead there.

**(a) `unknown`.**
- 14 of 40 fresh Spanish lines resolve to `unknown`, which is treated as English.
- The lines are short, unaccented and cognate-heavy: "Escoliosis leve.", "Artrosis facetaria L4-L5.", "Contractura trapecio.", "Vertigo postural.", "Cirugia programada.", "Ibuprofeno 400 mg.", "Hernia L5-S1.", "TAC normal.", "Neumonia basal.", "Reduccion cerrada.", "Velocidad aproximada 35 mph.".
- Hedges outside the cue list make this dangerous. `extract_one` with a fake model, on "Dudoso edema oseo." and summary "Bone edema.", gives `['extract']` (the English step), state `verified`, reasons `[]`, label `None`.
- "Escoliosis leve." with the summary "Moderate scoliosis." gives no flag from the English checks.

**(b) Mixed text with English leading or tied.**
- `detect('MRI lumbar: protrusión L4-L5, posible compresión radicular.')` gives `en` (en 0.125, es 0.125).
- `grounding.check_summary('Lumbar MRI: protrusion at L4-L5 with nerve root compression.', that line)` returns `[]`.
- `spanish_text.check_summary` on the same pair returns `['SUMMARY_DROPS_QUALIFIER']`.
- "Pt refiere neck pain 7/10 desde el accidente." is also `en`, and "Neck pain 7/10 since the accident." returns `[]`.
- `lang_mixed` is set in `annotate` but nothing reads it: `grep` finds only `language.py` and a test.

Why this is a blocker:
- It is the round-1 blocker 2, narrowed but not closed.
- That blocker's acceptance test required "100% of at least 20 short ES one-liners routed es or flagged".
- Here, 14 of 40 fresh lines and 2 of 22 mixed or abbreviated lines fail it.
- The result is an unlabeled English summary of non-English text, with the hedge, side and negation checks skipped. That is a persona section 5 dealbreaker.

Fix:
1. Make `extract_v1` and `extract_es_v1` return a `source_language` field. If the model says it is not English and the detector said `unknown` or `en`, upgrade the record to `uncertain` and route it through the translation path with LANGUAGE_UNCERTAIN. The model knows the language even when a word list does not.
2. For mixed records (`mixed` is true, or any Spanish cue or diacritic is present), run the union of the English and Spanish token checks. Never run English-only.
3. Treat `unknown` as English only when the text has no alphabetic word of 4 or more letters outside a small English whitelist.

Acceptance test:
- Add a held-out set of 40 or more unaccented cognate Spanish lines and 12 or more mixed lines.
- Assert that every one resolves to es or uncertain, or that `extract_one` raises LANGUAGE_UNCERTAIN.
- Assert that a translated summary carries "AI translation".

## Blocker 2: Short FR/PT/IT/DE lines still run as English, and one Italian line is labeled Spanish

- 9 of 40 fresh lines resolve to `unknown` or `en`, so they run as English:
  - Portuguese: "Receita: ibuprofeno 400 mg.", "Cirurgia agendada."
  - Italian: "Nessuna frattura.", "Possibile frattura dello scafoide.", "Ricetta: ibuprofene 400 mg.", "Intervento programmato."
  - German: "Kontrolle in vier Wochen." (`en`), "Rezept: Ibuprofen 400 mg.", "Operation geplant."
- `extract_one` on "Possibile frattura dello scafoide." and "Kontrolle in vier Wochen." gives step `extract`, state `verified`, no label.
- The hedge "Possibile" is therefore handled by the English path and the unflagged English summary "Scaphoid fracture." would pass.
- "Nessuna frattura alla radiografia." resolves to `es`. The Italian record would be summarized as Spanish, and the label would name the wrong source language.
- The AC says unsupported languages are refused or marked uncertain, never run as English. The author's lists (FRENCH, PORTUGUESE, ITALIAN, GERMAN in `test_spanish_failsafe.py`) all pass; fresh lines do not.

Fix:
- The same `source_language` self-report as blocker 1: if it names a language other than English or Spanish, mark the record `other` (refused) or `uncertain`.
- Add Italian and German function words and morphology (-zione, -isch, nessun*, possibile, kontrolle, rezept).
- When es beats an unsupported language by only a thin margin, mark the record `uncertain`.

Acceptance test: 40 held-out FR/PT/IT/DE lines where 0 resolve to `en`, `unknown` or `es`.

## Major 1: In mixed records, the Spanish checks ignore English self-report cues in the quote

- `ST.check_summary('Right shoulder pain 7/10.', 'Patient reports dolor 7/10 en hombro derecho.')` returns `[]`.
- The English checker flags it with `['SUMMARY_TOKEN_NOT_IN_EXCERPT', 'SUMMARY_DROPS_QUALIFIER']`.
- A patient report is recast as a finding on a record detected `es` with `mixed=True`.
- Fix: for a mixed quote, accept the union of the English and Spanish cue sets on the quote side (and require them in the summary).
- Acceptance test: that pair returns `SUMMARY_DROPS_QUALIFIER`.

## Major 2: Cue lists still miss hedge, self-report and approximation words

All of these return `[]`, so the dropped qualifier is not flagged:

| Quote | Summary |
|---|---|
| "Hallazgo incierto en menisco." | "Meniscal finding." |
| "Dudoso trazo de fractura." | "Fracture line." |
| "Lesion presuntamente traumatica." | "Traumatic injury." |
| "A decir del paciente, cayo de la escalera." | "Fell from the stairs." |
| "Calificó el dolor como 7/10." | "Pain 7/10." |
| "Velocidad aproximada 35 mph." | "Speed 35 mph." |

- `aproximada` and `aproximado` are missing from `_APPROX_CUES`. Only `aproximadamente` and `aprox` are listed.
- Also missing: incierto, dudoso, presunta, presuntamente, calificó, "a decir del".
- Unrecognized hedge words also drive lines to `unknown` (blocker 1).
- Fix: extend the lists, and have the researcher (lexicon owner) review them with a Spanish-speaking clinical source.
- Acceptance test: the six pairs return a drop reason.

## Major 3: The "uncertain" safety net is not exercised by any held-out data

- The fail-safe design is right: uncertain records take the translation path, are never `verified`, and carry LANGUAGE_UNCERTAIN.
- But the tests only exercise lines the author wrote into the lists, so the 22% foreign and 35% Spanish miss rates above are invisible.
- The suite has no held-out data and no coverage number.
- Fix: an opt-in evaluation of language routing on a fixed file of at least 100 labeled short lines (es, fr, pt, it, de, mixed) with a printed confusion matrix, plus a release gate for 100% of es lines resolving to es or uncertain and 0 of the others to en or es.
- Acceptance test: `python -m evals.run` (or a test) prints the routing confusion matrix.

## Minor 1: The 54-pair set is sound as a regression, but it cannot show recall

- `tests/unit/spanish_translation_pairs.jsonl` has 54 pairs: 16 faithful controls, 34 unfaithful pairs that the code flags, 4 judge-only.
- Most unfaithful pairs are my round-1 probes. The `code_flags` field records what the code did when the file was written, so the check that "the code flags what it flags" is partly circular.
- Held-out recall on my fresh probes is 51 of 58 (7 misses, listed in major 2 and major 1, plus 1 dose-related miss on a mixed line).
- The 4 judge-only pairs are honestly listed: dose unit, frequency, order read as done, duration in words.
- Good: it asserts 0 false positives on the controls.

## Minor 2: The live Spanish judge eval is opt-in, unrun, and weaker than it looks

- `test_live_translation_judge_recall_and_false_positive_rate` is skipped by default and costs about 55 model calls.
- It fails only when an unfaithful pair is graded `supported`, so a left/right flip graded `partially` (which I saw in round 1) passes.
- It always passes `lang="es"`, so the uncertain path is not measured.
- No recorded fixtures or rates exist.
- Fix: assert that every unfaithful pair is `unsupported` or `partially`, and record the rate; run it once with `SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1 LLM_BACKEND=claude-cli` and paste the result into the card.
- This is a minor because the code checks hold on everything in the author's set.

```json
{"card": "T-085", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD 9c1af01 (contains 1b1c711, T-085 r2) via git archive in the scratchpad; app/backend/{language,spanish_text,spanish,generator,pipeline}.py, tests/unit/{test_spanish_failsafe.py,spanish_translation_pairs.jsonl}; sample case evals/golden/sample.txt and lib09 Spanish case; ad hoc short Spanish, mixed, French, Portuguese, Italian, German lines",
 "exercised": [
  "git archive HEAD (9c1af01) extracted to scratchpad t085r2; git worktree not used",
  "pytest tests/unit in the clean tree with LLM_BACKEND=fixture: 1569 passed, 4 skipped",
  "pytest test_spanish_failsafe.py test_spanish_records.py test_t037_backend.py: 180 passed, 1 skipped",
  "LLM_BACKEND=fixture python -m app.pipeline on evals/golden/sample.txt and evals/library/case_lib09_spanish_interpreter_espalda.txt: both complete, rc 0, no traceback",
  "LLM_BACKEND=fixture python -m app.pipeline on a one-record French file: 'refused: unsupported_language (French)', rc 1",
  "r2_detect.py: language.detect on 22 fresh Spanish lines (mixed, abbreviated, diacritics stripped, hedged) and 17 FR/PT/IT/DE lines, with case_check",
  "r2_es2.py: 40 further unaccented Spanish clinical lines, 14 resolve to unknown",
  "r2_for2.py: 40 fresh FR/PT/IT/DE short lines, 13 other, 18 uncertain, 9 run as en/unknown (7) or one Italian as es plus German 'Kontrolle' as en",
  "r2_mixed.py: grounding.check_summary vs spanish_text.check_summary on mixed pairs; showed English path returns [] where Spanish path flags",
  "r2_check.py: 58 check_summary probes (not-ruled-out variants, diacritics stripped, abbreviations, hedges, negations, numbers, laterality, dates, mixed): 7 misses, 0 false positives",
  "generator.extract_one with FakeCall on 4 lines: RM cervical line -> extract_es, label 'AI translation'; 'Dudoso edema oseo.', 'Kontrolle in vier Wochen.', 'Possibile frattura dello scafoide.' -> English 'extract' step, verified, no label",
  "Read spanish_translation_pairs.jsonl (54 pairs: 16 control, 34 code-flagged unfaithful, 4 judge-only) and the pair/live-eval tests; live eval not run (opt-in, ~55 calls)",
  "Read language.py and spanish_text.py in full"
 ],
 "verdict": "fail",
 "scores": {"cli_crash_fixed": 5, "short_spanish_routing_and_label": 3, "unsupported_language_refusal": 3, "no_se_descarta_hedge_inversion": 5, "cue_words": 3, "eval_pair_set": 3, "live_judge_eval": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Spanish text still runs on the English path, unlabeled, with hedge/side/severity checks skipped (unknown and mixed-English-leading)",
   "evidence": "r2_es2.py: 14 of 40 fresh unaccented Spanish lines resolve to 'unknown' (treated as English): 'Escoliosis leve.', 'Artrosis facetaria L4-L5.', 'Contractura trapecio.', 'Vertigo postural.', 'Cirugia programada.', 'Ibuprofeno 400 mg.', 'Hernia L5-S1.', 'TAC normal.', 'Neumonia basal.', 'Reduccion cerrada.', 'Velocidad aproximada 35 mph.'. generator.extract_one with FakeCall on 'Dudoso edema oseo.' -> steps ['extract'], state verified, reasons [], translation label None. Mixed: language.detect('MRI lumbar: protrusión L4-L5, posible compresión radicular.') -> en (en 0.125, es 0.125); grounding.check_summary('Lumbar MRI: protrusion at L4-L5 with nerve root compression.', that line) -> []; spanish_text.check_summary on the same pair -> ['SUMMARY_DROPS_QUALIFIER']. 'Pt refiere neck pain 7/10 desde el accidente.' -> en, 'Neck pain 7/10 since the accident.' -> []. grep lang_mixed: set in language.annotate, read nowhere outside tests.",
   "why_it_matters": "This is round-1 blocker 2 narrowed, not closed. An unlabeled English summary of Spanish text is produced and the checks that catch a dropped 'posible', a flipped side, or a patient report recast as a finding do not run. 'Escoliosis leve.' summarised as 'Moderate scoliosis.' returns [] on the English path. Persona section 5: a hedge converted into a conclusion. My round-1 acceptance test (at least 20 held-out short ES lines, 100% routed es or flagged) is not met.",
   "fix": "Have the extract prompts return a source_language field; if the model says non-English and the detector said unknown or en, upgrade the record to uncertain (translation path, LANGUAGE_UNCERTAIN, never verified). For mixed records, run the union of the English and Spanish token checks. Treat 'unknown' as English only when there is no alphabetic word of 4+ letters outside a small English whitelist.",
   "acceptance_test": "A held-out file of 40+ unaccented cognate Spanish lines and 12+ mixed lines: every one resolves to es or uncertain, or extract_one yields LANGUAGE_UNCERTAIN; each translated summary carries 'AI translation'; ST-style pair 'Lumbar MRI ... nerve root compression.' vs the mixed MRI line returns SUMMARY_DROPS_QUALIFIER on the routed path."},
  {"severity": "blocker",
   "title": "Short French/Portuguese/Italian/German lines still run as English (9 of 40 fresh lines); one Italian line is labeled Spanish",
   "evidence": "r2_for2.py: unknown/en for 'Receita: ibuprofeno 400 mg.', 'Cirurgia agendada.', 'Nessuna frattura.', 'Possibile frattura dello scafoide.', 'Ricetta: ibuprofene 400 mg.', 'Intervento programmato.', 'Kontrolle in vier Wochen.' (en), 'Rezept: Ibuprofen 400 mg.', 'Operation geplant.'. extract_one on 'Possibile frattura dello scafoide.' and 'Kontrolle in vier Wochen.' -> ['extract'], verified, no label. r2_detect.py: 'Nessuna frattura alla radiografia.' -> es (accepted, would be labeled as Spanish).",
   "why_it_matters": "The AC says unsupported languages are refused or marked uncertain and never run as English. The author's own lists pass, but fresh lines do not, so the guarantee is not real. An Italian hedge ('Possibile') is silently handled by the English path, and an Italian note labeled as a Spanish translation misstates the source language.",
   "fix": "Same source_language self-report as the first blocker: a named language other than English or Spanish sets the record to other or uncertain. Add Italian and German function words and morphology; mark es uncertain when its margin over an unsupported language is thin.",
   "acceptance_test": "40 held-out FR/PT/IT/DE short lines (including the 9 above): 0 resolve to en, unknown or es; each is refused by name or marked LANGUAGE_UNCERTAIN."},
  {"severity": "major",
   "title": "In mixed records the Spanish checks ignore English self-report cues in the quote",
   "evidence": "spanish_text.check_summary('Right shoulder pain 7/10.', 'Patient reports dolor 7/10 en hombro derecho.') -> []; grounding.check_summary on the same pair -> ['SUMMARY_TOKEN_NOT_IN_EXCERPT', 'SUMMARY_DROPS_QUALIFIER']. language.detect gives es with mixed=True.",
   "why_it_matters": "A patient report is recast as a finding in a record the tool itself marks as mixed. Persona section 5 (patient report recast as provider finding).",
   "fix": "For a quote with mixed=True, accept the union of English and Spanish cue sets on the quote side.",
   "acceptance_test": "The pair above returns SUMMARY_DROPS_QUALIFIER."},
  {"severity": "major",
   "title": "Spanish cue lists still miss hedge, self-report and approximation words",
   "evidence": "check_summary returns [] for: 'Hallazgo incierto en menisco.' -> 'Meniscal finding.'; 'Dudoso trazo de fractura.' -> 'Fracture line.'; 'Lesion presuntamente traumatica.' -> 'Traumatic injury.'; 'A decir del paciente, cayo de la escalera.' -> 'Fell from the stairs.'; 'Calificó el dolor como 7/10.' -> 'Pain 7/10.'; 'Velocidad aproximada 35 mph.' -> 'Speed 35 mph.'. _APPROX_CUES in spanish_text.py lists aproximadamente and aprox, not aproximada/aproximado.",
   "why_it_matters": "Persona checklist items 5, 6 and 14: hedges, self-report attribution and approximations are preserved. Unlisted hedge words also push lines to unknown (English path).",
   "fix": "Add incierto/a, dudoso/a, presunto/a, presuntamente, indeterminado/a, calificó, 'a decir del', aproximado/a to the cue lists; have the researcher review the lists.",
   "acceptance_test": "Each of the six pairs returns a drop reason; a further held-out list of 30 pairs passes with no misses."},
  {"severity": "major",
   "title": "Language routing has no held-out measurement, so the fail-safe's real miss rate is invisible",
   "evidence": "The fail-safe tests (test_short_spanish_clinical_lines_are_spanish_never_english, FRENCH/PORTUGUESE/ITALIAN/GERMAN lists) use only the author's own lines. On 40 fresh Spanish lines 35% resolve to unknown; on 40 fresh FR/PT/IT/DE lines 22% run as English or Spanish; the suite reports neither.",
   "why_it_matters": "The 'never English' guarantee cannot be trusted without a held-out, labeled set and a coverage number; the first two blockers passed 1569 tests.",
   "fix": "Add a labeled routing file of at least 100 short lines (es, fr, pt, it, de, mixed) with a printed confusion matrix and a gate: 100% of es lines resolve to es or uncertain, 0% of non-es lines resolve to en or es.",
   "acceptance_test": "A test or evals runner prints the routing confusion matrix and fails on any es line routed to en or any foreign line routed to en or es."},
  {"severity": "minor",
   "title": "The 54-pair set is a sound deterministic regression but cannot show recall: most unfaithful pairs are round-1 probes and code_flags records observed behaviour",
   "evidence": "tests/unit/spanish_translation_pairs.jsonl: 54 pairs = 16 control, 34 unfaithful with code_flags true, 4 judge_only (ST-050 dose unit, ST-051 frequency, ST-052 order read as done, ST-053 duration). On my 58 fresh probes the code layer missed 7. Strengths: 0 false positives on controls; judge-only pairs are listed honestly.",
   "why_it_matters": "The recall number is circular; fresh probes miss 12%.",
   "fix": "Keep the set as a regression but add a held-out file authored by someone who has not seen the cue lists and report recall separately.",
   "acceptance_test": "Report shows recall on a held-out pair file, separate from the regression set."},
  {"severity": "minor",
   "title": "Live Spanish judge eval is opt-in, unrun, and passes a wrong-side 'partially'",
   "evidence": "test_live_translation_judge_recall_and_false_positive_rate is skipped unless SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1; it fails only when an unfaithful pair comes back 'supported', and always passes lang='es'. No rate or fixtures recorded. Round 1: a left/right flip was graded 'partially'.",
   "why_it_matters": "The judge is the last rung for everything the code layer misses (dose, frequency, order vs done), and its measured rate is not on record.",
   "fix": "Run it once, record the rates on the card, record fixtures, and also assert on the verdict reason for side and negation pairs.",
   "acceptance_test": "A run report with recall and false-positive rate on 54 pairs is attached to T-085."}
 ],
 "whats_right": [
  "The CLI crash is fixed: sample and lib09 run, a French file is refused by name with rc 1, and the full unit suite passes (1569 passed).",
  "'No se descarta' is direction-aware: all 9 fresh variants, in both directions, behave correctly, and 'ruled out' no longer satisfies the hedge.",
  "The uncertain design is right: translation path, never verified, LANGUAGE_UNCERTAIN, no English token checks. It just has to be reached more often."
 ],
 "questions_for_chris": []}
```
