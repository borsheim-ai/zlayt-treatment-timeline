# T-085 round 4: legal-nurse-reviewer (Spanish-language records, D-050 never auto-verified)

Verdict: **pass**. No blockers, no majors, four minors, one nit.

Tested tree: `git archive HEAD` at b10bff4 extracted to a new empty scratchpad directory (`r4arch`). I confirmed it is identical to `git archive b10bff4` (`diff -rq` on `app/` and `tests/` printed nothing). The shared tree was not touched. Python was the project `.venv`, run with `-I` and an explicit `sys.path` to the archive. Later commits (HEAD is now ae76835) are out of scope.

## The D-050 question: can translated text reach the letter without a human accept?

No path found. My own end-to-end probe drove the real FastAPI app with a fake model: six records (English with stray words; Spanish with an ambiguous date and a $650.00 charge; Portuguese; Italian-or-Spanish; Spanish concussion; English). I checked every path you named:

| Path | Result |
|---|---|
| Pipeline run | e3 (Portuguese, `uncertain`), e4, e5, e2 (Spanish), amount a1, both gap flags: all `needs_review` with `AI_TRANSLATION` (`LANGUAGE_UNCERTAIN` too on e3). English e1, e6: `verified`. |
| Rerun | Identical states. |
| Rejudge (judges down, then up) | English e1, e6 go `verified`. Spanish and uncertain e2, e3, e4, e5 and a1 stay `needs_review` after the judge says `supported`. |
| Date confirm (`03/04/2026`, offered readings, chose one) | e2 loses `DATE_AMBIGUOUS` and keeps `AI_TRANSLATION`. Gap flag recomputed with `AI_TRANSLATION`. Nothing verified. |
| Batch accept | `[e4, e5]` and `[e3]` return 422 `not_verified`. `[e1, e6]` returns 200. A batch including e2 returns 422 `CODE_CHECK_FAILED` (D-051). |
| Export before any human accept | The letter holds only the two accepted English entries. No concussion, herniation, strain or $650 text. |
| Human accept | Single accept of e3, e4, e5 returns 200; they appear in the letter as `AI translation: ...` above the original quote; state stays `needs_review`. Accept of the amount returns 200, state `needs_review`. |
| Edit over a Spanish quote | Edited e5: still `needs_review`, `AI_TRANSLATION`. |
| Reclassify, manual entry | Reclassify refused without charge wording; manual entry refused because the record already has an entry (both paths also have unit coverage). |
| Narrative | `narrative.py:78` excludes entries carrying a translation label, so translated text does not enter the firm-voice paragraph. |

Fixtures for the 47 r3 pairs (`pairs.py`): 27 route `es`, 20 route `uncertain`, **0 verified**. 198 tests in the three Spanish/D-050/routing files pass; full `tests/unit` 1903 passed, 2 failed. Both failures call `git archive HEAD` or need a repo and cannot run in an exported tree (`CalledProcessError ... git archive HEAD`), so they are environmental, not product failures.

## Routing re-probes

- r3 60-line set: non-English routed English 0 of 60; Italian, Portuguese, French or German routed Spanish 0 of 27 in that set; every row in an acceptable route.
- Brief's Portuguese line `Suspeita de hernia discal L4-L5.`: routes `uncertain`. `Hernia discal L5-S1 com compressao radicular.`: `uncertain`. In a 20-line fresh Portuguese/Italian set, one line routes `es`: `Cervicalgia post-traumatica.` (Italian or Portuguese; see minor 3).
- English stray words: 41 fresh English lines, 8 not English (r3's code on the same 41 lines: 26 not English). The `son`, `operation`, `plus`, `eventual`, `vertebral`, `radicular` lines now stay English. The other 8 are `uncertain` (see minor 2).

## Findings in short

- Minor 1: conflict flags that cite a Spanish record are still `verified` (the known gap; T-094 `flags.py` change not in b10bff4).
- Minor 2: 8 of 41 fresh short English lines still route `uncertain` and would be labelled "AI translation".
- Minor 3: an Italian line routes `es` and is labelled "Spanish"; `language.py` docstring overclaims.
- Minor 4: the Spanish code checks still miss dropped qualifiers, so a human accept of a translated entry with a dropped "sin pérdida de conocimiento" succeeds. D-050 makes the human the gate, as designed; this is the residual risk of that choice.
- Nit: a missing space in `language.py` glues two stop words.

```json
{"card": "T-085", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive b10bff4 (HEAD at review start, D-050 fix); app/backend/{confidence,language,flags,generator,pipeline,review,rejudge,reclassify,spanish_text,export,narrative,case_extras}.py; own FastAPI TestClient end-to-end probe with a fake model on a 6-record mixed case; r3 probe scripts re-run; 41 fresh English lines and 20 fresh Portuguese/Italian lines",
 "exercised": [
  "git archive HEAD (b10bff4) into a new scratchpad dir; diff -rq against git archive b10bff4: identical",
  "pytest tests/unit/test_d050_never_verified.py test_language_routing_heldout.py test_spanish_records.py: 198 passed; full tests/unit: 1903 passed, 2 failed (both need git archive HEAD / a repo, environmental)",
  "r3 scripts re-run: lines60.py (0/60 non-English routed English; 0 IT/PT/FR/DE routed es), pairs.py and pairs2.py (47 es/uncertain pairs, 0 verified), extra.py, extra2.py",
  "own API probe (r4probe/test_r4.py): run, rerun, rejudge with judges down then up, confirm_date on 03/04/2026, batch accept (translated, English, mixed), single accept of translated entries and amount, export before and after accept, edit, reclassify, manual entry, conflict flag citing a Spanish quote",
  "41 fresh English lines (en40.py): 8 route uncertain; same lines on the r3 archive: 26 not English",
  "20 fresh Portuguese/Italian lines (pt.py) including the brief's Portuguese line",
  "read git show b10bff4 for confidence.py, flags.py, generator.py, language.py, pipeline.py, reclassify.py, rejudge.py, review.py, spanish_text.py, why.py; read export.py, narrative.py:78, case_extras.py batch route"
 ],
 "verdict": "pass",
 "scores": {"d050_never_auto_verified": 5, "human_accept_still_works": 5, "english_stays_english": 4, "portuguese_routes_uncertain": 5, "spanish_code_check_recall": 2, "label_accuracy": 3},
 "findings": [
  {"severity": "minor",
   "title": "Conflict flags citing a Spanish record are still verified (known gap, T-094 one-line flags.py change not present at b10bff4)",
   "evidence": "app/backend/flags.py run_conflict_pass builds f['_stage'] = {grounding_failures, injection, agreement, judge} with no 'translated' key (flags.py:258-259), unlike _flag at flags.py:56. Probe: conflict between English 'Left shoulder pain 7/10.' and Spanish 'Refiere dolor 6/10 que empeora al levantar el brazo.' with J3 'conflict' gives f_cx1 state=verified, reasons=[], why='Quote found word for word, every number in the summary is in the quote, and the second check agreed.' Single accept of f_cx1 returns 200 and the item appears in internal_notes_text under FLAGS ACCEPTED quoting the Spanish. It does not reach letter_text (R-EX-1) and batch refuses it (not_an_entry).",
   "why_it_matters": "D-050 says every item from a Spanish or uncertain record is needs_review with the translation label. A conflict is judged by the English J3 on a Spanish quote and shows 'verified' with no translation caution. The paralegal and the internal notes see a conflict claim built on text the tool did not verify in that language.",
   "fix": "In flags.run_conflict_pass add 'translated': any(language.translated_record(r) for r in (ra, rb) if r) to f['_stage'] and pass it through _compose (the _compose ctx already reads st.get('translated')).",
   "acceptance_test": "A conflict whose evidence cites a record routed es or uncertain returns state needs_review with AI_TRANSLATION; a conflict between two English records stays verified."},
  {"severity": "minor",
   "title": "Short English lines with look-alike words still route uncertain: 8 of 41 fresh English lines",
   "evidence": "language.record_lang on: 'Patient walks solo with a cane; gait steady.' (uncertain, could be Spanish or French); 'Hernia repair in 2018, no complications.'; 'Basal metabolic panel within normal limits.'; 'Alta Vista Chiropractic: adjustment, cervical and thoracic, tolerated well.'; 'Discal protrusion at C5-C6, may represent degenerative change; correlate clinically.'; 'Lumbar hernia ruled out by ultrasound.'; 'Bill: office visit $150, plus x-ray $75; total $225.' (could be French or another language); 'Insurance information: Medicare Part B; copay $40.' (reason lists insurance, information, medicare). Same 41 lines on the r3 archive: 26 non-English.",
   "why_it_matters": "Fail-safe, not unsafe: those entries are needs_review with LANGUAGE_UNCERTAIN. The cost is that an English summary of an English record is prefixed 'AI translation:' in the letter after accept and runs the Spanish extraction prompt. The 'Discal protrusion ... may represent degenerative change; correlate clinically' line is a core hedge case for imaging text. This is a quality preference, not a spec violation.",
   "fix": "Add common English clinical and billing words (insurance, information, medicare, basal, metabolic, panel, repair, ruled, ultrasound, gait, steady, office, visit) to _ENGLISH_OK, and count 'hedged imaging' English phrases (may represent, correlate clinically, ruled out) toward english_only so the collision rule applies.",
   "acceptance_test": "The 8 lines above route en; the 60-line non-English set still routes 0 to en."},
  {"severity": "minor",
   "title": "An Italian-or-Portuguese line still routes es and is labelled Spanish; the language.py docstring overclaims",
   "evidence": "record_lang({'excerpt': 'Cervicalgia post-traumatica.'}) = 'es' at b10bff4. In the API probe, entry e4 carries translation.source_language_name = 'Spanish', label 'AI translation', review_label 'AI translation — check against the original'. The language.py docstring still says Italian, Portuguese, French and German never route to Spanish. The test file calls this line 'the reviewer's Italian line that cannot be told from Spanish' and asserts only that it is translated.",
   "why_it_matters": "Under D-050 the item cannot auto-verify and carries the check-against-original label, so the risk is bounded. The label still names the wrong language, and the code comment is false.",
   "fix": "For lines whose Spanish evidence is only Romance-shared words (cervicalgia, post-traumatica), return uncertain so the name reads 'an unidentified language'. Correct the docstring to say the guarantee is the D-050 label, not language identity.",
   "acceptance_test": "'Cervicalgia post-traumatica.' routes uncertain; docstring no longer claims zero Romance leakage."},
  {"severity": "minor",
   "title": "Residual: Spanish code checks still miss dropped qualifiers, so accepting a translated entry with a dropped 'sin pérdida de conocimiento' is allowed",
   "evidence": "Probe entry e5: quote 'Diagnóstico: conmoción cerebral sin pérdida de conocimiento. TAC craneal negativo.', summary 'Concussion. CT head negative.' State needs_review (AI_TRANSLATION), single accept returns 200 (no CODE_CHECK_FAILED), letter then shows 'AI translation: Concussion. CT head negative.' above the Spanish quote. pairs.py: 15 of 40 unfaithful mixed/cue pairs still return [] from spanish_text.check_summary (r3: 4 of 41 mixed). Contrast e2, where the English-vocabulary D-047 rule fires and blocks accept (EXCERPT_OMITS_QUALIFIER, 422).",
   "why_it_matters": "Persona section 5 treats a dropped 'without loss of consciousness' as a blocker. The brief says D-050 mitigates this because only a paralegal accept can put the text in the letter, the entry is labelled, and the original quote sits under it. I accept that for this round and rate it minor; the weakness is that D-051 'code checks bind accept' is blind for Spanish, so the paralegal's reading is the only check on translated qualifiers.",
   "fix": "Not required for this card. If revisited: add Spanish 'sin pérdida de conocimiento/conciencia' and 'niega pérdida de conocimiento' to a LOC rule requiring 'without loss of consciousness' or 'no loss of consciousness' in the summary, and show the quote's negation and hedge words next to the translation in the review row.",
   "acceptance_test": "The e5 pair returns SUMMARY_DROPS_QUALIFIER on a Spanish route and single accept returns 422."},
  {"severity": "nit",
   "title": "Missing space in language.py glues two stop words",
   "evidence": "language.py _STOP['en'] string ends '... symmetric advised\"' and the next literal starts '\"evaluation evaluated ...'. Probe: 'advised' in L._STOP['en'] = False, 'evaluation' = False, 'advisedevaluation' = True.",
   "why_it_matters": "Two ordinary English words stop counting toward English evidence.",
   "fix": "Add a trailing space after 'advised'.",
   "acceptance_test": "'advised' and 'evaluation' are members of _STOP['en']."}
 ],
 "whats_right": [
  "D-050 is enforced once in confidence.compose_state and every path I drove (run, rerun, rejudge, date confirm, batch, amount accept, edit) respected it; 0 of 47 Spanish or uncertain pairs and 0 translated items in my API case reached verified.",
  "A single human accept still works and the letter labels the entry 'AI translation:' with the original quote; batch accept refuses translated items with not_verified, and the narrative excludes translated entries.",
  "Routing improved: the brief's Portuguese line is uncertain, English stray-word lines dropped from 26 to 8 of 41 non-English, and r3's 0-of-60 English-leak gate still holds."
 ],
 "questions_for_chris": []}
```
