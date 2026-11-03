# Review T-014 round 3 (staff-engineer-reviewer): ADRs, LLM_VS_CODE.md, API contract

Verdict: **changes** (0 blockers, 5 majors, 4 minors, 1 nit). Of the 10 staff r2 findings, 7 are fully resolved, 3 are partly resolved (each leaves one of the new majors below). Of the privacy r2 findings, the blocker (N1) and the demo-storage major (N2) are resolved; N3 is mostly resolved with two gaps that I carry as M2 and M5. Full table: `artifacts/review-evidence/T-014-r3-resolution.md`.

What I re-ran (details in the JSON): the 14 api.md JSON blocks parse; 19 of 19 `raw[start:end]` offsets equal their quotes on `evals/golden/sample.txt`; the ADR-011 rules, applied literally with the real lexicon v2, classify all 14 golden dollar amounts as the golden file expects (including case_09 `$275` charge, which failed in round 2); the privacy amount demo adapted to the new rules shows the injected `$50,000` changes nothing in the letter, including the total line; lexicon self-check recall is 11 of 11 and it tags case_07 record 3 and hits P1. Nothing is silently defaulted: judge failure on an edit saves as `needs_review` `JUDGE_UNAVAILABLE`, `FixtureMiss` is never retried, money is integer cents.

What is left is drift between the architect's text and artifacts that moved in parallel (lexicon v2, D-021, D-022, the golden file, REQUIREMENTS at 2e92535). Each fix is small, but each one would make a backend worker build the wrong thing, so they stay majors.

## Majors
- **M1 D-022 is not in the design.** `SUMMARY_DROPS_QUALIFIER` and per-sentence `source_kind` appear in no ADR, no LLM_VS_CODE row, no reason code (`grep -c SUMMARY_DROPS_QUALIFIER` on api.md, DECISIONS.md, LLM_VS_CODE.md = 0, 0, 0). The writer's REQUIREMENTS section 8 row 5 lists it as an open T-014 item.
- **M2 ADR-013's closed category list does not match lexicon v2.** The lexicon uses `prior_surgery`, `alternative_cause`, `objective_negative`, `litigation_referral`, `recovery_context`, `accident_date_provenance` (none in ADR-013; 0 mentions in the three architect docs) and not `no_objective_findings`, `normal_exam`, `attorney_referral`. Case_07 P1, the floor flag the injection design relies on, has category `prior_surgery`, so it has no template and no state rule.
- **M3 The `confirm_date` example puts a phone note into gap math.** api.md:206-210 recomputes `f_gap_r7_r8` (40 days) after confirming record 8 of case_01. Record 8 is a phone note; D-003, ADR-010 and golden case_01 (`gap_excluded_records: [8]`) exclude it. The example claims its numbers "come from golden case_01".
- **M4 `mg.` abbreviation.** ADR-016 says `mg.` is not an abbreviation and api.md:90-91 splits "Rx cyclobenzaprine 10 mg." from "Follow up with PCP in 1 week."; D-021 (binding) says the splitter keeps `mg.` intact, and R-TL-2 at HEAD lists it.
- **M5 Cut line undoes the injection control.** README-arch.md:82 lists "the per-record flag pass folded into one pass" as a cut. D-021 and ADR-008.3 make the per-record pass the structural control against one record suppressing another's flags.

## Minors and nit
m1 the api.md export example is a second copy of the golden file and already differs from it at HEAD; m2 `422 date_invalid` (R-RV-2) vs `invalid_edit` (api.md); m3 "golden variant E" is cited as evidence but does not exist and no card owns it; m4 normalisation says "trimmed" in api.md and ADR-006 but "nothing else is changed" in ADR-002, and the source of the demo's recorded hash set (evals/golden must ship in the image) is not stated; nit: docs still cite D-001..D-015.

## Buildability in about 7 hours
Plausible with the ordered cut line, once M5 is fixed. Cuts taken in round 3 (limiter, ledger, arbitrary-text ingest, LLM classifier) remove the least valuable code. Remaining weight: 17 backend modules, 7 prompts, about 40 calls per case, fixtures to record for every golden case the demo accepts (about 400 calls through the CLI backend at concurrency 3, and any prompt edit invalidates them). Build order in README-arch.md puts pure-code modules first, which is right.

## What I would not change
Gaps from code-parsed record dates; code-only amount classification with a judge on every class; the total line fixed by D-019; the edit re-check order with an explicit judge-unavailable state.

```json
{
  "card": "T-014",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "Round 3. git diff e442626..388d5b2 (memory/DECISIONS.md ADR-002..017, docs/LLM_VS_CODE.md, memory/contracts/api.md, app/README-arch.md), read at HEAD 8106024 (those four files unchanged since 388d5b2; spec/REQUIREMENTS.md and evals/golden updated at 2e92535/f8c1948 and compared); against memory/ORCHESTRATOR_DECISIONS.md D-001..D-023 and app/llm/lexicon.yaml v2 (2fee2df); design review only, no app code or server exists; sample case = evals/golden/sample.txt (1879 chars) plus all golden cases for the amount simulation",
  "exercised": [
    "python3 tools/board.py show T-014 (AC and round-3 handoff read; claims not trusted)",
    "read reviews/T-014-staff-engineer-r2.md and reviews/T-014-privacy-compliance-r2.md in full",
    "read memory/DECISIONS.md lines 1-307, docs/LLM_VS_CODE.md, memory/contracts/api.md (453 lines), app/README-arch.md, memory/ORCHESTRATOR_DECISIONS.md D-001..D-023, REQUIREMENTS R-TL-2/R-TL-8/R-EX-8/R-RV-2 and section 8 at HEAD",
    "python3 -I artifacts/review-evidence/T-014-json-check.py: total 14 blocks, 0 fail",
    "python3 -I artifacts/review-evidence/T-014-r2-offset-check.py: chars 1879, 19 19 (all offsets equal quoted strings)",
    ".venv/bin/python -I artifacts/review-evidence/T-014-r3-amount-sim.py > T-014-r3-amount-sim.out: ADR-011 rules 1-8 with the real lexicon over all golden cases, 14 of 14 dollar amounts match the golden class (case_09 $275 charge via rule 6, case_07 $50,000 unclear via rule 1, sample $185 rate); the 15th row is the value-less damages item",
    ".venv/bin/python -I artifacts/review-evidence/T-014-r3-amount-demo.py > T-014-r3-amount-demo.out: injected $50,000 with A2 pending, dismissed or accepted leaves the letter money block byte-equal to the control; forged untagged 'ER charges: $50,000.' stays out of the letter while pending and enters it once accepted",
    ".venv/bin/python -I research/lexicon_selfcheck.py: MUST recall 11/11, case_07 P1 HIT, injection hit case_07 r3, accident_date_phrases hit sample r7, RESULT: PASS",
    "python3 evals/golden/check_golden.py: golden OK: 10 cases (9 synthetic), 57 must_nots",
    "scratchpad script comparing the api.md export example with evals/golden/sample.export.expected.txt via git show 388d5b2 and HEAD: at 388d5b2 letter differs only on the total line; at HEAD letter entry 1 and three notes lines differ",
    ".venv/bin/python lexicon category dump vs ADR-013 list: 6 lexicon categories not in ADR-013",
    "grep for SUMMARY_DROPS_QUALIFIER, variant E, mg., fold/one pass, date_invalid, D-001..D-015 across the architect files",
    "git log 388d5b2..HEAD and git show HEAD:spec/REQUIREMENTS.md section 8 (writer's open list rows 2 and 5)",
    "wrote artifacts/review-evidence/T-014-r3-resolution.md",
    "Not exercised: no app code exists, so no mutation spot-check, no CLI run, no pytest"
  ],
  "verdict": "changes",
  "scores": {
    "5.2 table completeness and fidelity": 4,
    "LLM/code boundary soundness": 5,
    "determinism and no silent fallback": 5,
    "provider abstraction / claude-cli safety": 5,
    "data model and audit (D.4)": 5,
    "API contract serves REQUIREMENTS": 3,
    "buildable in ~7h": 4,
    "example quality (JSON, offsets)": 3,
    "consistency with binding decisions D-001..D-023": 3
  },
  "findings": [
    {
      "severity": "major",
      "title": "M1 D-022 (SUMMARY_DROPS_QUALIFIER, per-sentence source_kind) is not reflected anywhere in the design",
      "evidence": "memory/ORCHESTRATOR_DECISIONS.md D-022 (committed a399a4c, before the architect's 388d5b2): 'if an entry's excerpt contains a qualifier ... and the summary omits it, code marks the entry needs_review (reason SUMMARY_DROPS_QUALIFIER) ... Self-report is tagged per sentence/quote ... field name source_kind: patient_report'. Command: grep -c 'SUMMARY_DROPS_QUALIFIER' memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md -> 0, 0, 0. ADR-012 (DECISIONS.md:238-243) checks only tokens added to a summary, not qualifiers dropped; api.md reason-code appendix (:432-453) has no such code; entries in api.md:94-113 have no source_kind. spec/REQUIREMENTS.md section 8 row 5 (HEAD) lists 'No SUMMARY_DROPS_QUALIFIER' as an open T-014 r3 item.",
      "why_it_matters": "ADR-003 and LLM_VS_CODE row 4/15 are binding for M2. A backend built from them has no rung-1 check for an omitted hedge or negation, so a summary 'Findings suggest degenerative change' for an excerpt 'may represent ... correlate clinically' reaches `verified` if the judge agrees. That is the omission failure the decision exists to stop.",
      "fix": "Add to ADR-012 a second function (qualifiers in the excerpt, found with the lexicon hedge set, self_report entries, negation words, laterality and 'approx.', must each appear in the summary, else SUMMARY_DROPS_QUALIFIER); add the code to the api.md appendix and ADR-005's needs_review list, a clause to LLM_VS_CODE rows 4 and 15, a per-quote source_kind to the entry schema, and ADR-017 item for R-TL-10.",
      "acceptance_test": "Unit: summary 'Findings suggest degenerative change' over the sample record 8 excerpt -> needs_review with SUMMARY_DROPS_QUALIFIER; summary 'Discharged from physical therapy' over 'Discharged from PT after two missed appointments' still passes; grep -c SUMMARY_DROPS_QUALIFIER on the three architect files >= 1 each."
    },
    {
      "severity": "major",
      "title": "M2 ADR-013's closed category list does not match lexicon v2; the P1 floor flag has no category or template",
      "evidence": "Command: .venv/bin/python dump of app/llm/lexicon.yaml entries by (flag_type, category) vs the ADR-013 list. Lexicon categories NOT in ADR-013: accident_date_provenance, alternative_cause, litigation_referral, objective_negative, recovery_context, prior_surgery. ADR-013 categories used by no lexicon entry: no_objective_findings, normal_exam, attorney_referral. grep for the six names across DECISIONS.md, api.md, LLM_VS_CODE.md -> 0 hits. memory/DECISIONS.md:253 'a unit test asserts every category has one [template]' and :257 'one-sided hits are needs_review (LEXICON_ONLY ...)'. app/llm/lexicon.yaml header: 'Lexicon-only categories (no LLM counterpart ...): prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context, accident_date_provenance'. research/lexicon_selfcheck.py: 'case_07_prompt_injection P1 pre_existing must: HIT' via prior_surgery_terms[high] (category prior_surgery).",
      "why_it_matters": "The lexicon floor is the control that keeps case_07's must-flag P1 (prior ACL repair) alive when the model or an injected record fails to raise it (ADR-008.3, privacy N3). Its category is not in the closed list, so the template unit test cannot pass and the flag cannot be rendered or typed; a worker will either invent templates or drop the hit. Six lexicon categories (alternative_cause, recovery_context, accident_date_provenance ...) are in the same position.",
      "fix": "Make ADR-013's list the union with the lexicon's category names (or rename the lexicon's), give each a template and a flag_type, and say which categories are lexicon-only (origin lexicon, LEXICON_ONLY, needs_review). State that recovery_context entries with strength low never raise a flag.",
      "acceptance_test": "Unit: every `category` value in app/llm/lexicon.yaml entries is a key in flag_templates.py and in the api.md category list (set equality check); case_07 with a fixture whose flag pass omits P1 yields a pre_existing flag, origin lexicon, needs_review LEXICON_ONLY, rendered from a template."
    },
    {
      "severity": "major",
      "title": "M3 The confirm_date example adds a phone note to gap math, contradicting D-003, ADR-010 and golden case_01",
      "evidence": "memory/contracts/api.md:204-212: confirm_date on record r8 with {\"date\": \"2026-05-04\"} returns gap_flags [{\"id\": \"f_gap_r7_r8\", ... \"from\": \"2026-03-25\", \"to\": \"2026-05-04\", \"days\": 40}] and says 'The numbers above come from golden case_01'. evals/golden/case_01_date_formats.expected.json (git show 388d5b2): 'gap_excluded_records': [8], notes 'Record 8 is a phone note (non-encounter) and is excluded from gap math in any case.', gap_table has six pairs, all <= 14 days, none involving record 8. app/llm/lexicon.yaml non_encounter hit: case_01 r8 'Dr. Orla Pennywhistle, phone note'. D-003: 'Billing statements and phone notes are excluded'. DECISIONS.md:214 ADR-010: any gap flag 'whose span could contain one of its candidate dates' is needs_review, with no carve-out for non-encounter records.",
      "why_it_matters": "A backend worker (and the frontend, which codes against these examples) will treat a confirmed phone-note date as a gap endpoint and show a 40-day gap the golden file says must not exist. It also invents a fact in an example that claims golden provenance.",
      "fix": "Change the example to a case where an encounter record's date is ambiguous (or show gap_flags: [] and removed_flag_ids for case_01 r8), delete the 'come from golden case_01' sentence, and add to ADR-010: a record with encounter=false never causes ENDPOINT_NOT_VERIFIED and never recomputes gaps on confirm.",
      "acceptance_test": "API/unit test: confirm_date on case_01 record 8 returns 200 with gap_flags == [] and no f_gap_* flag involving r8; a gap table over case_01 equals the golden gap_table before and after confirmation."
    },
    {
      "severity": "major",
      "title": "M4 ADR-016 and the api.md sentence units say `mg.` is not an abbreviation; binding D-021 and R-TL-2 say it is",
      "evidence": "memory/ORCHESTRATOR_DECISIONS.md D-021: 'Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact.' spec/REQUIREMENTS.md:49 R-TL-2 at HEAD: abbreviation list '(`approx.`, `Dr.`, `Mr.`, `Mrs.`, `Ms.`, `vs.`, `etc.`, `e.g.`, `i.e.`, `mg.`)' (the list had no `mg.` at 388d5b2; the writer added it at 2e92535). memory/DECISIONS.md:282 ADR-016: 'notably `mg.` is not an abbreviation, because \"Rx cyclobenzaprine 10 mg. Follow up...\" is two units'. memory/contracts/api.md:90-91: sentences[3] 'Rx cyclobenzaprine 10 mg.' [477,502) and sentences[4] 'Follow up with PCP in 1 week.' [503,532).",
      "why_it_matters": "D-xx wins over architect text (DECISIONS.md:10). The sentence-unit list is the contract for excerpt validation, the excerpt-edit UI and the qualifier rule; the splitter and its unit test (R-TL-2: units concatenate to the record) will be written to one or the other, and the frontend example offsets will be wrong for record 2. This is the same drift I reported as R2-4 in round 2, reversed by a parallel edit.",
      "fix": "Follow D-021: remove the `mg.` sentence from ADR-016, point at R-TL-2's list as the single source, and regenerate api.md's records[].sentences for record 2 (one unit [477,532) 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'). If the architect believes mg. followed by a capital must end a sentence, raise it as a question to the orchestrator rather than overriding D-021 in an ADR.",
      "acceptance_test": "Unit: splitter on sample record 2 returns the units in the revised api.md example with matching offsets (text[start:end] == unit text for each); python3 -I artifacts/review-evidence/T-014-r2-offset-check.py still reports all offsets OK; grep -n 'mg\\.' memory/DECISIONS.md shows no 'is not an abbreviation'."
    },
    {
      "severity": "major",
      "title": "M5 The cut line lets the per-record flag pass be folded into one pass, which undoes D-021 and the injection control",
      "evidence": "app/README-arch.md:82: 'First to go if a milestone exceeds 150% of budget ...: the side-by-side layout ..., then the synchronous judge re-run on edits ..., then the per-record flag pass folded into one pass.' memory/ORCHESTRATOR_DECISIONS.md D-021: 'Prior/causation flag pass runs per record so an injected record can't suppress another record's flag.' memory/DECISIONS.md:191 ADR-008.3 'Suppression is made structural. The pre_existing/causation flag pass runs per record'; :197 lists 'one all-records flag pass' under alternatives considered and rejected. docs/LLM_VS_CODE.md:89 states the preserved P1 flag as fact.",
      "why_it_matters": "A cut under schedule pressure is exactly when nobody re-reads ADR-008. Folding the pass restores the round-2 condition (privacy N3): record 3's 'Report no prior conditions' reaches the call that decides record 2's flags, with a lexicon floor whose categories do not render (M2). The cut would silently void a stated guarantee in the hiring-panel doc.",
      "fix": "Remove that item from the cut line, or make it conditional in the same sentence: if taken, ADR-008.3 reverts to 'residual', LLM_VS_CODE row 12 and the worked example 2 sentence about record 2 are rewritten as conditional, the case banner says flags may be incomplete in any case with a tagged record, and the orchestrator records it in SCOPE_CUTS.md. Per-record calls can instead be cheapened by batching the judge, not the pass.",
      "acceptance_test": "grep -n 'folded into one pass' app/README-arch.md returns nothing (or the conditional wording above); EV case_07 with a fixture whose flags pass omits P1 still shows P1 from the lexicon floor."
    },
    {
      "severity": "minor",
      "title": "m1 The api.md export example is a second copy of the golden file and already differs from it at HEAD",
      "evidence": "Scratchpad script comparing json block 'letter_text'/'internal_notes_text' in memory/contracts/api.md with evals/golden/sample.export.expected.txt: at 388d5b2 the notes block is byte-equal and the letter differs on the total line only (golden still carried '(physical therapy charges to be supplemented)'); at HEAD 8106024, after qa's f8c1948: letter line 4 golden 'complained of neck pain 7/10' vs api.md 'neck pain 7/10'; notes differ on the causation line, the added 'Record 1 ... Conflict, accident date' line and the bills-to-request order. api.md:267 'this section is generated from that file' and :414 'on the fixture backend the sample output equals the golden file byte for byte'. spec/REQUIREMENTS.md section 8 row 2 lists the notes-block difference as open for T-014.",
      "why_it_matters": "This is the R2-1 failure mode again: an embedded copy of a file someone else owns will always drift. The golden file is the test target (ADR-009), so the api.md copy can only mislead.",
      "fix": "Replace the two full strings in the api.md example with the first and last lines plus '(full text: evals/golden/sample.export.expected.txt)', or regenerate from the golden file at the time of the M2 gate and add a pytest that fails when they differ.",
      "acceptance_test": "A unit test loads the api.md export block and compares letter_text/internal_notes_text to the golden file (or the block contains no full text and the test does not exist); passes at HEAD."
    },
    {
      "severity": "minor",
      "title": "m2 confirm_date error code: R-RV-2 says 422 date_invalid, api.md and ADR-005 say 422 invalid_edit",
      "evidence": "spec/REQUIREMENTS.md:93 R-RV-2: 'confirm_date ...: a date that is not one of the code-proposed readings -> 422 `date_invalid`'; memory/contracts/api.md:212 '`422 invalid_edit` when the record's date is not ambiguous, or the date is not one of its candidates'; DECISIONS.md:152 same. ADR-017 (:295-306) does not list it. Section 8 'Checked and aligned' claims api.md uses `422 date_invalid` for a non-candidate date; it does not (grep -c date_invalid memory/contracts/api.md = 0).",
      "why_it_matters": "Two status/code pairs for one input; the E2E written from R-RV-2 fails against an API built from api.md.",
      "fix": "Pick one (cheapest: adopt date_invalid in api.md for the non-candidate case, invalid_edit for 'not ambiguous') and add it to ADR-017 and the api.md error-code list at :9.",
      "acceptance_test": "API test: confirm_date with a non-candidate date returns the code named in both api.md and R-RV-2."
    },
    {
      "severity": "minor",
      "title": "m3 'Golden variant E' is cited as the evidence for the scoped injection claim, but it does not exist and nothing owns it",
      "evidence": "memory/DECISIONS.md:190 'golden variant E documents that it stays `pending` and is never in `totals.accepted` without an accept event'; docs/LLM_VS_CODE.md:44 row 16 '(golden variant E)'. Command: ls evals/golden | grep -i 'variant\\|case_10' -> no output; grep -n 'variant E' memory/DECISIONS.md docs/LLM_VS_CODE.md memory/SCOPE_CUTS.md -> only the two citing lines; ADR-017 lists no qa item. Hands-on: artifacts/review-evidence/T-014-r3-amount-demo.py runs F and G show the behaviour (pending -> not in letter; accepted -> letter total $50,420.00).",
      "why_it_matters": "A guarantee in the hiring-panel doc rests on a test that is not scheduled. The privacy r2 acceptance test asked for it explicitly.",
      "fix": "Add the variant to ADR-017 as a qa item (a case_07 variant with 'ER charges: $50,000.' untagged) with the expected output stated, or reword the two sentences to 'documented, not yet in the golden set'.",
      "acceptance_test": "evals/golden contains the variant with an expected.json asserting the amount is a pending charge and absent from totals.accepted; or the two citing lines no longer cite it."
    },
    {
      "severity": "minor",
      "title": "m4 Text normalisation is stated two ways, and the source of the demo's recorded hash set is not stated",
      "evidence": "memory/DECISIONS.md:99 ADR-002 'CRLF and CR become LF; nothing else is changed, and the normalised text is what is hashed and stored' vs api.md:49 and DECISIONS.md:164 'CRLF to LF, trimmed' and D-020 'normalized hash (CRLF->LF, trimmed)'. DECISIONS.md:164 'the hash is in the recorded set (the sample and the golden cases)' with no statement of where the set comes from; tests/fixtures are keyed by prompt hash (ADR-004 :136), not text hash; the Docker image ships fixtures but nothing says it ships evals/golden/*.txt.",
      "why_it_matters": "Trimming leading whitespace shifts every absolute offset the API promises; two normalisations give two hashes for the same paste. If the golden texts are not in the image, the gate rejects the sample.",
      "fix": "Say one thing: stored raw_text = CRLF/CR -> LF, trailing whitespace trimmed only (offsets unaffected), hashed after the same step. State that the recorded set = sha256 of the normalised evals/golden/*.txt computed at start-up and that evals/golden/*.txt ships in the image.",
      "acceptance_test": "Unit: sample.txt with CRLF and a trailing newline creates a case whose raw_text[start:end] equals the quotes in api.md; a one-word change returns 409 demo_mode_unsupported_input with no rows written; the container test finds the golden texts."
    },
    {
      "severity": "nit",
      "title": "n1 Decision citations are stale",
      "evidence": "docs/LLM_VS_CODE.md:3 'cross-cutting decisions D-001 to D-015'; memory/contracts/api.md:3 '(D-001..D-015)'; memory/DECISIONS.md:10 'cited as D-001..D-015'. The text cites D-016, D-017, D-018, D-019, D-020, D-021 elsewhere.",
      "why_it_matters": "The hiring panel reads these headers to find what binds the design.",
      "fix": "Change to D-001..D-023.",
      "acceptance_test": "grep -n 'D-001..D-015\\|D-001 to D-015' on the three files returns nothing."
    }
  ],
  "whats_right": [
    "Amount classification is code-only with rule precedence (rate beats charge) and a judge on every class; my literal simulation over all golden cases gets 14 of 14 dollar amounts right, and the injected $50,000 never touches the letter.",
    "Edit path is honest about judge failure: structure 422, token check 409, judge objection 409, judge down or no fixture saves as needs_review JUDGE_UNAVAILABLE, FixtureMiss never retried.",
    "Gaps still read only code-parsed record dates, and the api.md gap and accident-date evidence offsets are all exact (19 of 19)."
  ],
  "questions_for_chris": []
}
```
