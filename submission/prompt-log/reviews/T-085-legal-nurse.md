# T-085 review: legal-nurse-reviewer (Spanish-language records)

Verdict: **fail**. Three blockers, three majors.

Tested tree: `git archive HEAD` extracted to the scratchpad, HEAD at e2b4e3f, a descendant of 865b186. The board-guard hook denies `git worktree` for reviewers, so I used a read-only archive of the same commit instead. The shared tree's uncommitted edits were never touched.

The core design holds up. Excerpts stay verbatim Spanish, the English line carries "AI translation", and the code checks catch most wrong numbers, sides, months and negations. The weak points are routing and vocabulary:
- Short Spanish lines are routed to the English path with no label.
- Short French lines are routed to the Spanish path.
- The `python -m app.pipeline` CLI crashes on every input.
- The Spanish cue lists miss common clinical words.
- One hedge inversion is credited by design.
- Nothing measures the Spanish judge.

## Evidence

Clean-tree unit run (`pytest tests/unit`):
- `test_spanish_records.py`: 66 passed.
- Full unit suite: 7 failed, 1310 passed.
- `test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s` fails because of T-085.
- The other six failures belong to other cards: `sbs-flags`, trace tests, `judge_conflict_v3`.
- The handoff said only 2 T-089 failures, so it did not run clean.

Adversarial probes, 8 or more as requested:
- About 90 probes of `spanish_text.check_summary` against Spanish quotes and wrong English summaries.
- Results for negation, laterality, number, date, approximation and report-vs-finding probes are in the findings below.
- The live judge (`judge_faithfulness_es_v1`, claude-cli) on 14 cases: 13 of 13 unfaithful or faithful cases graded correctly, including "sin" to "with", left/right flip, hedge dropped, order shown as done, and "No se descarta" shown as "ruled out".
- The fixture backend cannot judge new text. It returns `unavailable`, and the item stays `needs_review`.

Replay of lib09 on the fixture backend:
- Records 2, 4 and 7 are `es`, `verified` or `needs_review`, with the label "AI translation".
- Record 2: "Niega pérdida del conocimiento" becomes "Denies loss of consciousness", and "Refiere dolor 6/10" becomes "Patient reports pain 6/10". Both are correct.

```json
{"card": "T-085", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 865b186 (T-085) as present in HEAD e2b4e3f via git archive in the scratchpad; app/backend/{language,spanish,spanish_text,generator,review,pipeline}.py, app/llm/prompts/{extract_es_v1,judge_faithfulness_es_v1}.md; D-034, D-042; sample case evals/library/case_lib09_spanish_interpreter_espalda.txt (fixture) and ad hoc Spanish sentences",
 "exercised": [
  "python3 tools/board.py show T-085; read D-034 and D-042 in memory/ORCHESTRATOR_DECISIONS.md; read personas/legal-nurse.md",
  "git worktree refused by board-guard hook for reviewers; used git archive HEAD (e2b4e3f) extracted to scratchpad, read-only, shared tree untouched",
  "pytest tests/unit/test_spanish_records.py in the clean tree: 66 passed",
  "pytest tests/unit in the clean tree: 7 failed, 1310 passed; test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s fails with UnboundLocalError at pipeline.py:501",
  "python -m app.pipeline <spanish file> and <german file> with LLM_BACKEND=fixture: both crash with UnboundLocalError: cannot access local variable 'raw'",
  "probe.py: 50 adversarial ES quote / EN summary pairs through spanish_text.check_summary (negation niega/sin/nunca/tampoco/ausencia/negativo, laterality incl. der./izq., dose, decimal comma, hedge posible/probable/sugiere/compatible con/sospecha, self-report, approx, currency, numeric/written dates)",
  "probe2.py: 40 further pairs for vocabulary gaps (aqueja, alega, senala, expresa, quizas, tal vez, impresiona, eventual, jamas, carece, libre de, ni, nada), 'No se descarta' inversions, unit/frequency, numeric-date month reading",
  "probe3/4/5.py: language.detect and case_check on 12 short Spanish, French, Portuguese and German clinical lines; check_summary on the misrouted line",
  "judge_live.py: judge_faithfulness_es_v1 live via claude-cli (ENABLE_LIVE=1) on 14 ES/EN cases: 13 graded correctly, the one faithful 'sin embargo' passed",
  "replay.py: lib09 on fixture backend via pipeline.run_case: records 2/4/7 are es, quotes verbatim, label 'AI translation', judge supported, warnings SPANISH_RECORDS",
  "read language.py, spanish_text.py, spanish.py, both Spanish prompts, the 865b186 diff of generator/review/pipeline, and tests/unit/test_spanish_records.py"
 ],
 "verdict": "fail",
 "scores": {"excerpt_verbatim_original": 4, "translation_label_and_judge": 3, "d034_token_checks": 3, "negation_laterality_hedge_preservation": 3, "unsupported_language_failure": 2, "ladder_measured": 2},
 "findings": [
  {"severity": "blocker",
   "title": "python -m app.pipeline crashes on every input (English too); the CLI unsupported-language refusal can never run",
   "evidence": "app/backend/pipeline.py:500-505 (commit 865b186): the try/language.case_check(... IN.ingest(raw) ...) block runs before `a = ap.parse_args(...)` and `raw = open(...)`. Repro: `LLM_BACKEND=fixture python -m app.pipeline es1.txt` and the same for a German file both end in `UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value` at pipeline.py line 501. `pytest tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s` fails with that traceback; the handoff reported only 2 T-089 failures.",
   "why_it_matters": "AC 1 says unsupported languages still fail clearly. On the CLI they fail with a traceback, and every supported record fails too. The CLI is the documented offline entry point, and this regression is in a path the card touched.",
   "fix": "Move the case_check block after `raw = open(a.file, encoding='utf-8').read()` and after IN.check_limits(raw). Add a CLI test with an unsupported-language file expecting rc 1 and 'refused: unsupported_language (French)' on stderr, and a Spanish file expecting rc 0.",
   "acceptance_test": "test_t037_backend CLI test passes; new tests: `python -m app.pipeline french.txt` returns 1 with the refused line; `python -m app.pipeline spanish.txt` returns 0 on the fixture backend."},
  {"severity": "blocker",
   "title": "Short or abbreviation-heavy Spanish lines are 'unknown', run as English, carry no translation label, and lose hedge and side without a flag",
   "evidence": "language.py: unknown text is treated as English (`'en' if d['lang']=='unknown'`). `detect('RM cervical: protrusión discal C5-C6, posible estenosis foraminal derecha.')` gives lang unknown, so annotate sets lang='en', the English prompt and grounding.check_summary run, and entry.translation is null. Probe: grounding.check_summary('Cervical MRI: disc protrusion at C5-C6 with foraminal stenosis.', that line) returns [] while spanish_text.check_summary returns ['SUMMARY_DROPS_QUALIFIER']. 'Cervicalgia postraumática, espasmo paravertebral, ROM reducido aprox. 40%.' is also unknown, so English path. Also 'Dor cervical 7/10. Nega perda de consciência. Fisioterapia.' (Portuguese) is unknown, so English path.",
   "why_it_matters": "A Spanish quote gets an unlabeled English summary. The code checks that would catch 'posible' dropped (hedge converted to conclusion) and 'derecha' dropped never run, and the judge sees only the English-path prompt. This breaks the AC (English summaries of Spanish carry the label) and is a persona section 5 dealbreaker: a hedge converted into a conclusion with no flag. Real MRI impressions and one-line Dx notes are short. The handoff's claim that a wrong guess only means the pre-D-042 behaviour is wrong, because pre-D-042 there was no Spanish input path.",
   "fix": "Add diacritics, clinical Spanish terms (posible, derecha, izquierda, protrusión, pérdida, niega, sin, cervicalgia) and Spanish clinical abbreviations to the detector. For an 'unknown' record, also run a cheap Spanish-evidence test (any ñ, accented vowel, ¿¡, or Spanish clinical cue word); if present, route as Spanish (labelled) or send to needs_review with a LANGUAGE_UNCERTAIN warning. Never silently produce an unlabeled English summary of non-English text.",
   "acceptance_test": "Unit tests: the three lines above resolve to es (or flagged uncertain); each has entry.translation set when the generator output differs in language; the hedge-dropping summary returns SUMMARY_DROPS_QUALIFIER. Held-out set of at least 20 short ES one-liners with 100% routed es or flagged."},
  {"severity": "blocker",
   "title": "Short French or Portuguese lines are not refused: French is detected as Spanish and translated under a Spanish label, Portuguese falls to English",
   "evidence": "probe4.py: `Douleur cervicale 7/10, pas de perte de conscience.` gives lang es, case_check accepted. `La paciente se plaint de douleur à l'épaule droite depuis trois jours.` gives lang es, accepted. `Dor cervical 7/10. Nega perda de consciência. Fisioterapia.` gives lang en, accepted. The tests only cover full-sentence French, German, Portuguese, Italian, Chinese and Cyrillic notes.",
   "why_it_matters": "AC 1 requires non-supported languages to fail clearly. Here the French quote would be summarized with source_language_name 'Spanish', and the Spanish translation judge may pass a faithful translation of French. The label then misstates the source language, and the Spanish token tables are meaningless for French ('pas' and 'sans' are not negation cues).",
   "fix": "Add French and Portuguese function words and diacritics (à, ç, ã, õ, 'pas de', 'sans', 'nega', 'perda') with enough weight on short lines. When the best supported score is only marginally above an unsupported language, refuse that record (UNSUPPORTED_LANGUAGE) instead of accepting it. Test with at least 5 short lines per unsupported language.",
   "acceptance_test": "The three lines above are refused or skipped with UNSUPPORTED_LANGUAGE and a named language; 15 short fr/pt/it/de lines all refused; all 4 short ES lines in this review still accepted as es."},
  {"severity": "major",
   "title": "A hedge inversion is credited by design: 'No se descarta fractura' passes as 'Fracture ruled out'",
   "evidence": "spanish_text.check_summary('Fracture ruled out.', 'No se descarta fractura.') returns []. _EN_HEDGE_EXTRA and _EN_NEG_EXTRA (spanish_text.py:~60-64) both contain `ruled? out`, so 'ruled out' satisfies the hedge requirement and the negation requirement at once. 'Fracture excluded.' and 'No evidence of fracture.' are flagged, which shows the check is inconsistent. The live judge did catch this case.",
   "why_it_matters": "'No se descarta' means 'cannot be excluded', the standard radiology hedge. 'Ruled out' says the opposite, so a hedge becomes a conclusion in the exculpatory direction. That is a persona section 5 dealbreaker whenever the judge misses it or is unavailable.",
   "fix": "Remove `ruled? out` and `rule out` from the satisfiers when the quote contains 'no se descarta' or 'a descartar'. Make 'descarta' direction-aware: a quote with 'no se descarta' needs a hedge word (cannot be excluded, possible, may) and must not contain ruled out, excluded or no. A quote with 'se descarta' needs a negation or 'ruled out'.",
   "acceptance_test": "check_summary('Fracture ruled out.', 'No se descarta fractura.') returns SUMMARY_DROPS_QUALIFIER; ('Fracture cannot be excluded.', same) returns []; ('Fracture ruled out.', 'Se descarta fractura.') returns []."},
  {"severity": "major",
   "title": "Spanish cue lists miss common clinical self-report, hedge and negation words, so the qualifier check silently passes dropped qualifiers",
   "evidence": "check_summary returns [] for these Spanish-to-English summaries that drop the cue: 'Aqueja dolor cervical 7/10.' -> 'Neck pain 7/10.'; 'Alega dolor lumbar desde el accidente.' -> 'Low back pain since the accident.'; 'Señala dolor en rodilla izquierda.' -> 'Left knee pain.'; 'Expresa mareo...' -> 'Dizziness on standing.'; 'Quizás exista lesión meniscal.' -> 'Meniscal injury.'; 'Tal vez haya fractura.' -> 'Fracture.'; 'Impresiona como hernia discal.' -> 'Disc herniation.'; 'Eventual compromiso radicular.' -> 'Radicular compromise.'; 'Jamás había tenido dolor de rodilla.' -> 'Had knee pain before.'; 'Carece de antecedentes de lesión cervical.' -> 'History of cervical injury.'; 'Libre de dolor al alta.' -> 'Pain at discharge.'; 'Ni fractura ni luxación.' -> 'Fracture and dislocation.'; 'Nada que reportar en radiografía.' -> 'Findings on x-ray.' _SELF_CUES, _HEDGE_CUES and _NEG_CUES in spanish_text.py:34-45 lack these words. The correctly flagged cases were refiere, niega, sin, nunca, tampoco, ausencia, posible, probable, podría, sugiere, sospecha and compatible con.",
   "why_it_matters": "'Aqueja' and 'alega' are the usual Spanish words for patient-reported symptoms, and 'impresiona como' is a radiology hedge. Dropping them recasts a complaint as a finding and a hedge as a conclusion, and the D-034 code layer lets it through. Only the judge stands between the draft and a verified state. The handoff discloses that the Spanish lexicon for pre-existing and causation flags is missing, but not that the qualifier cue lists are this thin.",
   "fix": "Extend the cue lists: self-report (aqueja, alega, señala, expresa, indica, verbaliza, relata, cuenta, según refiere, motivo de consulta); hedge (quizá, quizás, tal vez, impresiona, eventual, sugestivo, a correlacionar, no concluyente, vs); negation (jamás, carece, libre de, ni, nada, sin evidencia). Have the researcher (lexicon owner) review the list with a Spanish-speaking clinician source.",
   "acceptance_test": "Each of the 13 pairs above returns the matching drop reason; a held-out list of at least 30 further pairs passes at 100% with no new false negatives."},
  {"severity": "major",
   "title": "No adversarial or gold evaluation exists for the Spanish judge and token checks; the recorded fixtures contain only faithful outputs",
   "evidence": "Handoff: 'no eval run'. tests/unit/test_spanish_records.py feeds scripted judge answers (FakeCall) and the lib09 fixtures are 6 recordings of faithful extract and judge calls (records 2, 4, 7). No evals/ file holds an unfaithful ES/EN pair, so no measured recall exists for 'sin' to 'with', side flip, dropped hedge, order shown as done. My live run of the judge on 14 cases (13 correct) is one-off and cannot be reproduced on the fixture backend. Reason codes were also wrong: a left/right flip was graded 'partially/OTHER_UNSUPPORTED'.",
   "why_it_matters": "Per D-042 and the ladder rule the judge must be an independent, measured check. Without a seeded-unfaithful set, a prompt change or model swap can regress Spanish faithfulness unnoticed. A judge verdict 'partially' for a wrong side suggests the verdict strength is also unmeasured.",
   "fix": "Add evals/adversarial/spanish_translation.jsonl with at least 40 ES/EN pairs (sin, niega, laterality, hedges, no se descarta, numbers, dates, decimal commas, order vs done, self-report vs finding, plus faithful controls). Record fixtures for judge_faithfulness_es_v1 on them and report recall and false-positive rate in the library report. A wrong side or hedge must not be graded 'supported'; assert the verdict, not just the state.",
   "acceptance_test": "`python -m evals.run` (or its adversarial runner) reports 100% of the unfaithful ES pairs as not supported on the recorded fixtures and 0 faithful controls graded unsupported."},
  {"severity": "minor",
   "title": "False positives on very common Spanish words: 'Sin embargo', 'Sin duda', 'No solo' are treated as negation",
   "evidence": "check_summary('However, pain persists.', 'Sin embargo, el dolor persiste.') returns SUMMARY_DROPS_QUALIFIER; same for 'Sin duda hay espasmo.' and 'No solo dolor cervical sino lumbar.' (these three are the code checks' fail-toward-flagging behaviour; the last one is a real 'no solo' so arguably correct).",
   "why_it_matters": "Routes faithful entries to needs_review and trains the paralegal to ignore SUMMARY_DROPS_QUALIFIER. This is a quality point, not a safety one.",
   "fix": "Skip negation cues followed by embargo or duda, and 'sin' directly before 'embargo'. Keep 'no solo'.",
   "acceptance_test": "'Sin embargo, el dolor persiste.' with 'However, pain persists.' returns []."},
  {"severity": "minor",
   "title": "A numeric Spanish date is silently read day-first in the summary, although the pipeline withholds the same record's date as ambiguous",
   "evidence": "spanish_text._date_months reads numeric dates day-first. check_summary('Follow-up visit June 3, 2026.', 'Fecha: 03/06/2026. ...') returns []; 'March 6, 2026' is flagged. In lib09 record 4 (03/05/2026) date_iso is None with DATE_EXCLUDED_FROM_GAPS, yet 'Admission May 3, 2026.' passes the check. extract_es_v1 tells the model to copy numeric dates as written.",
   "why_it_matters": "The tool resolves a date convention in the summary that it refuses to resolve in the timeline. A Spanish record from a US clinic can be month-first.",
   "fix": "For a numeric date, require the summary to keep the digits as written; accept a month name only when the case date convention is confirmed (T-088) or the day exceeds 12.",
   "acceptance_test": "'Admission May 3, 2026.' vs 'Fecha de ingreso: 03/05/2026.' returns SUMMARY_TOKEN_NOT_IN_EXCERPT; '03/05/2026' as written passes."},
  {"severity": "minor",
   "title": "Dose unit and frequency changes are not checked (shared with the English path, not new in T-085)",
   "evidence": "spanish_text.check_summary('Cyclobenzaprine 10 g', 'Ciclobenzaprina 10 mg.') returns []; ('Ibuprofen 400 mg three times daily.', 'Ibuprofeno 400 mg una vez al día.') returns []; ('Physical therapy for three weeks.', 'Fisioterapia por dos semanas.') returns []. grounding.check_summary shows the same for English. The live judge caught the frequency case.",
   "why_it_matters": "Persona checklist item 12 (medications as written). D-034 covers digits only; unit and frequency words ride on the judge alone.",
   "fix": "Add a unit and frequency token check (mg, mcg, g, ml, once, twice, three times, daily, every N hours) in grounding and in spanish_text. This is a shared-code change, so a separate card is acceptable.",
   "acceptance_test": "The three pairs above return SUMMARY_TOKEN_NOT_IN_EXCERPT."}
 ],
 "whats_right": [
  "Quotes are always the verbatim original Spanish (lib09 replay: excerpt in text, translated quote rejected) and the English line carries the 'AI translation' label, or 'Translation (edited by reviewer)' after an edit, in the entry and in the letter.",
  "The code checks catch number, month, side, negation and decimal-comma errors on Spanish quotes in about 40 of 50 first-round probes, and the numeric-token hard 422 holds across the language gap.",
  "The live judge graded 13 of 14 ES/EN probes correctly, including 'sin' turned into 'with', a side flip, a dropped hedge and an order shown as done, and passed the faithful 'sin embargo' sentence."
 ],
 "questions_for_chris": [
  "Should an uncertain-language record be sent to needs_review with a warning, or refused outright? I assumed flagged for review, because refusing a real Spanish MRI line would be worse than a visible warning."
 ]}
```
