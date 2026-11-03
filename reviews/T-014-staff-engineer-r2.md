# Review T-014 round 2 (staff-engineer-reviewer): ADRs, LLM_VS_CODE.md, API contract draft

Verdict: **changes** (0 blockers, 4 majors, 5 minors, 1 nit). Both round-1 blockers are resolved in the text, and I re-checked them against the sample file rather than the handoff. Gaps now come from record headers (ADR-010), the export carries an excerpt on every line (ADR-009), and the 14 JSON blocks in `api.md` parse. 19 of 19 `raw[start:end]` offsets equal the quoted strings on `evals/golden/sample.txt`. Thirteen of the fourteen round-1 findings are resolved and F12 is partial. What is left is spec drift between the architect's text and REQUIREMENTS rev 3 (export format, qualifier rule, abbreviation list), one hole in the amount rules that the golden set exposes, and an unspecified judge-failure path on edit.

## Exercised
- `python3 artifacts/review-evidence/T-014-json-check.py`: 14 blocks, 0 fail.
- `python3 -I artifacts/review-evidence/T-014-r2-offset-check.py`: 1879 chars, 19 of 19 offset checks pass.
- `python3 evals/golden/check_golden.py`: golden OK (10 cases).
- `python3 -I artifacts/review-evidence/T-014-r2-amount-sim.py`: ADR-011 rules applied literally to every golden case; one mismatch (case_09 `$275`).
- Walked the sample case, case_07 and case_09 through ingest, gaps, amounts, accident-date rule, judges and export. Checked D-001..D-018 and REQUIREMENTS rev 3 (R-IN, R-TL, R-FL, R-CH, R-RV, R-EX, R-CO) against `api.md`.
- Full resolution table: `artifacts/review-evidence/T-014-r2-staff-resolution.md`.
- Not exercised: no app code exists yet, so no mutation spot-check and no CLI run.

## Majors
- R2-1: the export format is specified three ways (ADR-009 and `api.md`, the golden file, REQUIREMENTS sec 6). `api.md:266` has dot leaders, a `Source: <label>, <date> [Ex...]` line, and a total-line reason ("visit count", "rate") inside the letter. R-EX-6 and R-EX-8 forbid all three. The byte-equality promise at `api.md:279` cannot hold.
- R2-2: ADR-011 cannot classify case_09's `$275` ("Statement for visit of 2026-02-02: $275.") as a charge. Charges are accept/dismiss only, so a real bill is permanently left out of the total.
- R2-3: the edit re-check calls judge 1 inside the review request. The design does not say what happens when the judge fails or when demo mode has no fixture for the edited text. `api.md` also contradicts itself on 422 versus 409.
- R2-4: ADR-016 over-applies D-012 and drifts from R-TL-8. It forces inclusion of every lexicon sentence, so sample entries 3 and 5 would be `needs_review`. REQUIREMENTS says only hedges force inclusion. `mg.` in its abbreviation list also contradicts the `api.md` sentence example.

## What I would not change
Gaps over record dates, the code-owned amounts, the closed reason codes, retries only in `audited.py`, and the fixture/recorded_from design.

```json
{
  "card": "T-014",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "git diff 94c7b08..e442626 (HEAD 3c5eb7c): memory/DECISIONS.md ADR-002..017, docs/LLM_VS_CODE.md (20 rows), memory/contracts/api.md (11 routes, 14 JSON blocks), app/README-arch.md; read against memory/ORCHESTRATOR_DECISIONS.md D-001..D-018, spec/REQUIREMENTS.md revision 3, docs/CONTRACT.md 5.2, evals/golden/*; design review only, no app running; sample case = evals/golden/sample.txt (9 records, 1879 chars), plus case_07 and case_09",
  "exercised": [
    "python3 tools/board.py show T-014 (AC read; handoff claims not trusted)",
    "git log/diff --stat 94c7b08..e442626",
    "read ADR-000..017 in full, LLM_VS_CODE.md, api.md, README-arch.md, ORCHESTRATOR_DECISIONS.md, REQUIREMENTS.md rev 3 sections 1-7, CONTRACT 5.2",
    "python3 artifacts/review-evidence/T-014-json-check.py > T-014-r2-json-check.out: 14 blocks, 0 fail",
    "python3 -I artifacts/review-evidence/T-014-r2-offset-check.py > T-014-r2-offset-check.out: 1879 chars, 19/19 raw[start:end]==quoted string; record 4 highlight [858,928) equals excerpt; gaps [0,7,7,28,14,73,11,14]",
    "python3 evals/golden/check_golden.py: golden OK: 10 cases (9 synthetic), 54 must_nots",
    "python3 -I artifacts/review-evidence/T-014-r2-amount-sim.py > T-014-r2-amount-sim.out: ADR-011 rules 1-7 over all golden cases; MISMATCH case_09 $275 (rule 7 unclear vs golden charge)",
    "grep for cut behaviours (BYOK, ?full, jsonl, cite=, batch, date pointing) in LLM_VS_CODE.md, api.md, README-arch.md: only in the cut list",
    "grep app/llm/lexicon.yaml for accident_date, non_encounter, injection, DOA categories: none present (version 1 format)",
    "grep -c '^| (GET|POST|DELETE)' api.md = 11 routes vs README-arch.md:15 '12 endpoints'",
    "walked sample, case_07, case_09 through the design; wrote artifacts/review-evidence/T-014-r2-staff-resolution.md"
  ],
  "verdict": "changes",
  "scores": {
    "5.2 table completeness and fidelity": 5,
    "LLM/code boundary soundness": 4,
    "determinism and no silent fallback": 4,
    "provider abstraction / claude-cli safety": 5,
    "data model and audit (D.4)": 5,
    "API contract serves REQUIREMENTS": 3,
    "buildable in ~7h": 3,
    "example quality (JSON, offsets)": 5
  },
  "findings": [
    {
      "severity": "major",
      "title": "R2-1 Export format is specified three incompatible ways; the api.md example cannot satisfy R-EX-6 or R-EX-8 and the byte-equality guarantee cannot hold",
      "evidence": "memory/contracts/api.md:266 letter_text example: 'Central ER discharge summary, January 9, 2026 ........ $6,240.00', 'Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]: \"...\"', and total '(excludes physical therapy — per-visit rate only, visit count not stated)'; DECISIONS.md:200 (ADR-009) specifies the same `Source: <label>, <date> [Ex...]` shape and '(excludes <service> — <reason>)'; api.md:279 'letter_text equals evals/golden/sample.export.expected.txt'. spec/REQUIREMENTS.md R-EX-6 (line 124) 'no dot leaders', 'Source [Ex. __ / Bates __]:' with the golden file containing no '..' run; R-EX-8 (line 126) letter total is 'Billed charges stated in these records: $X (physical therapy charges to be supplemented)' and UT 'letter_text contains neither \"visit count\" nor \"rate\"'; sec 6 (lines 213-260). evals/golden/sample.export.expected.txt still has dot leaders ('Central ER, January 9, 2026 ........ $6,240.00'), short headings ('January 9, 2026 — Austin EMS') and the '(excludes physical therapy — per-visit rate only, visit count not stated)' total, so it matches neither the api.md example (heading 'Central ER discharge summary') nor sec 6. R-EX-4 item 7 'Future treatment recommended' has no counterpart in ADR-009's notes list (DECISIONS.md:201) or in the api.md notes example (:267).",
      "why_it_matters": "A backend worker following api.md fails the R-EX-8 unit test (the letter contains 'visit count' and 'rate'); one following REQUIREMENTS fails the golden-equality test in api.md:279 and R-EX-6. The export is the product's deliverable and the byte-equality test is the main guard on it. Putting the reason for an excluded PT total in the carrier-facing letter also contradicts the purpose of D-001 (reasons live in the internal notes).",
      "fix": "Make REQUIREMENTS sec 6 the single template of record: ADR-009 and api.md point to it instead of restating it. Regenerate the api.md export example from that template (no dot leaders, 'Source [Ex. __ / Bates __]:', R-EX-8 parenthetical, notes sections in R-EX-4 order including 'future treatment recommended' and 'record N (provider, date)' citations). Add 'ADR-017 item 3 is stale: sec 6 already uses header labels' and ask qa to regenerate the golden export file from sec 6.",
      "acceptance_test": "One export unit test on the fixture backend: letter_text equals evals/golden/sample.export.expected.txt byte for byte; the golden file has no '..' run and every amount matches \\$[\\d,]+\\.\\d{2}; letter_text contains neither 'visit count' nor 'rate'; internal_notes_text contains a 'FUTURE TREATMENT RECOMMENDED' section for record 9; grep of api.md and DECISIONS.md finds no second statement of the Source-line format."
    },
    {
      "severity": "major",
      "title": "R2-2 ADR-011 classification rules leave a golden-required charge unclassified (case_09 $275), and 'contains per/each/rate' is not word-bounded",
      "evidence": "Simulation artifacts/review-evidence/T-014-r2-amount-sim.out line 32: 'MISMATCH (2, \"$275\", \"unclear\", \"r7:Statement for visit of 2026-02-02:\") (2, \"$275\", \"charge\")'. evals/golden/case_09_nonvisit_hides_gap.txt record 2 'Source: Hobbleton Family Clinic, billing statement / Excerpt: \"Statement for visit of 2026-02-02: $275.\"'; its expected.json lists A1 $275 class charge, in_total true, required true. DECISIONS.md:225 rule 6 'charge: the label ends with charge(s): / charge: ... or billed:' and :226 rule 7 'otherwise unclear'; DECISIONS.md:222 rule 3 'label contains per, each or rate' (substring, not word). Every other golden amount (13 of 14) classifies as expected.",
      "why_it_matters": "A billing statement is the most common real source of a charge. With charges accept/dismiss only (D-010, ADR-005) the paralegal has no way to turn this $275 into a totaled charge, so the total silently loses a stated bill and the case_09 total ($275) is unreachable. Substring matching would also read 'Post-operative charge: $4,000' (operative contains per) and 'Moderate ... charge' (rate) as rates; both fail safe but are wrong and unmeasured.",
      "fix": "Add to ADR-011 and LLM_VS_CODE row 7 a rule between 5 and 6: an amount in a record whose source label matches the non_encounter billing-statement entries, preceded by a label from a small closed list (statement, balance, amount due, total, billed), is a charge. Require word boundaries for per/each/rate (\\bper\\b, \\beach\\b, \\brate\\b). Keep J2 on it.",
      "acceptance_test": "Unit test over all golden .txt files: classify() equals the expected class for every golden amount (case_09 $275 -> charge); 20 phrasings of 'Charge per visit $185' -> rate; 'Post-operative charge: $4,000' -> charge; 'Moderate' / 'Corporate' labels never trigger rate."
    },
    {
      "severity": "major",
      "title": "R2-3 Edit re-check runs judge 1 inside the review request with no specified behaviour on judge failure or fixture miss; api.md contradicts itself on 422 vs 409 for excerpt edits",
      "evidence": "DECISIONS.md:152 'an edit runs the token check and re-runs J1 ... If any objects, the response is 409 needs_confirm'; api.md:242 same; nothing says what a LLMError, timeout, or FixtureMiss does (ADR-004 :136 'A miss raises FixtureMiss'; ADR-006 demo mode forces the fixture backend, and every edited text is a new prompt hash). api.md:240 'excerpt (must be a contiguous run of whole sentences ...)' with 'Any other action or key ... is 422 invalid_edit' versus :242 'an excerpt edit also re-runs the whole-sentence and qualifier rules. If either objects, nothing is saved and the response is 409'. REQUIREMENTS R-RV-2 (line 93) expects 422 for 'an excerpt edit that is not a contiguous run of whole sentence units' and 'drops a hedge-set unit'; sec 6 note 'hedge sentences cannot be removed'.",
      "why_it_matters": "This is the judge-error path the lens exists for. As written a worker can return success on judge failure (a silent fallback) or crash with a 500. In the public demo every edit hits a fixture miss, so the R-RV-2 E2E ('edit entry 3's summary -> edited label') cannot pass unless the miss path is defined. Two status codes for the same input will be implemented differently by backend and frontend.",
      "fix": "State in ADR-005 and api.md: (1) judge failure on an edit (LLMError, timeout, FixtureMiss) adds warning JUDGE_UNAVAILABLE to the 409 needs_confirm response; it never saves silently and never blocks 'keep my wording'. (2) In demo mode the edit path therefore always needs the confirmation, and E2E tests that path. (3) Non-contiguous, mid-sentence, other-record or hedge-dropping excerpt edits are 422 invalid_edit (structural, per R-RV-2); numbers/dates/dollars not in the quote and judge objections are 409 needs_confirm.",
      "acceptance_test": "API tests: edit with a fake backend raising LLMError returns 409 with JUDGE_UNAVAILABLE and nothing persisted; same edit with confirm_warnings true saves and logs keep_my_wording; fixture backend with no recorded edit behaves identically; excerpt edit dropping the MRI hedge returns 422 invalid_edit; summary edit adding '$9,000' returns 409 SUMMARY_TOKEN_NOT_IN_EXCERPT."
    },
    {
      "severity": "major",
      "title": "R2-4 ADR-016 forces inclusion of every flagged sentence and lists 'mg.' as an abbreviation; both disagree with D-012, R-TL-8 and the api.md example",
      "evidence": "DECISIONS.md:269 'A sentence containing a lexicon hit (pre_existing, causation_weakening, compliance) or a hedge is a qualifier unit: an entry whose record contains one must include it in the excerpt, or the entry is needs_review with EXCERPT_OMITS_QUALIFIER'. D-012 (ORCHESTRATOR_DECISIONS.md:20) only says such a sentence 'is kept whole' and 'a hedge can never be cut'. REQUIREMENTS R-TL-8 (line 55) limits forced inclusion to the hedge set and says 'Entry 3 with excerpt \"Persistent neck pain 6/10, daily headaches.\" stays verified (the 2023 low back sentence is pre_existing, not a hedge)'. api.md appendix :305 'the record has a hedge sentence the excerpt leaves out'. DECISIONS.md:268 'abbreviation-safe for approx., Dr., mg., decimals' but api.md:88 splits 'Rx cyclobenzaprine 10 mg.' / 'Follow up with PCP in 1 week.' into two units, and R-TL-2 (line 49) lists approx. Dr. Mr. Mrs. Ms. vs. etc. e.g. i.e. (no mg.). DECISIONS.md:269 'each is a contiguous ... span' vs a single excerpt_start/excerpt_end pair in api.md.",
      "why_it_matters": "Under ADR-016 sample entry 3 (golden letter excerpt omits 'Patient reports low back pain in 2023, resolved.') and entry 5 (omits the self-report sentence) become needs_review, so the sample no longer matches R-TL-8, the golden export, or the 'verify quickly' bar. The rule also pushes the generator to put adverse sentences into the carrier letter by default, against D-017. A splitter that honours 'mg.' merges two api.md example units and breaks the offsets the frontend will code against.",
      "fix": "Amend ADR-016 and the appendix: forced inclusion only for the R-TL-8 hedge set; any lexicon sentence is merely never cut (D-012). Take 'mg.' out of the abbreviation list and cite R-TL-2's list as the single source. State that an excerpt is one contiguous run of units (one start/end pair).",
      "acceptance_test": "Unit: splitter on sample record 2 returns the six units in api.md:88 with those offsets; entry 3 with excerpt 'Persistent neck pain 6/10, daily headaches.' is verified; entry 8 with the excerpt cut before the hedge is needs_review EXCERPT_OMITS_QUALIFIER; an excerpt cut mid-sentence from any lexicon sentence is EXCERPT_NOT_WHOLE_SENTENCE."
    },
    {
      "severity": "minor",
      "title": "R2-5 Demo gate and FixtureMiss semantics are unspecified; a CRLF paste or a retry on a miss defeats 'pasting the sample works'",
      "evidence": "DECISIONS.md:163 'Pasting the sample works (fixtures are keyed by prompt hash). Any other text returns 409 demo_mode_unsupported_input'; ADR-008.3 nonce = first 12 hex of sha256(case text + step + item id); ADR-004 :132 audited.py retries 'changed conditions'; ADR-004 :136 FixtureMiss.",
      "why_it_matters": "A browser paste with CRLF or a trailing newline changes the text hash, so the nonce and every prompt hash change; every call then misses. Without a pre-check the user sees nine failed items instead of the 409 message. A retry loop that re-runs a fixture miss three times changes the prompt each time and writes nine meaningless llm_calls rows.",
      "fix": "Normalise newlines at ingest (stored raw text is the normalised text) and gate /run on text_sha256 being in the recorded set, returning the 409 before any call. Declare FixtureMiss non-retryable: the item ends FIXTURE_MISS (visible) immediately.",
      "acceptance_test": "Unit: sample.txt with CRLF line endings still runs in demo mode; text differing by one word returns 409 at /run with zero llm_calls rows; a backend raising FixtureMiss produces exactly one llm_calls row per item, not three."
    },
    {
      "severity": "minor",
      "title": "R2-6 The spend ledger is called reset-proof but lives on ephemeral disk; clocks are not injectable by design",
      "evidence": "DECISIONS.md:164 'append-only file $DATA_DIR/spend_ledger.jsonl ... Case deletion, purge and restarts never touch it'; :166 'SQLite lives on the container's ephemeral disk'; README-arch.md:57 'The spend ledger is an append-only file outside the case store'; ADR-003.7 8-minute deadline, ADR-006 24 h purge and 'current UTC day' cap have no stated time source.",
      "why_it_matters": "A Space rebuild or restart resets the file, so the cap is only as good as the container lifetime; the doc claims more. Deadline, purge and day-rollover tests will be wall-clock dependent unless a clock is injected (checklist item 14).",
      "fix": "State that the ledger resets on rebuild and that the real cap is a spend limit set on the provider key (Chris action, NEEDS_CHRIS). Add one sentence: all time reads go through an injectable now() in app/config.py.",
      "acceptance_test": "Unit tests for the 8-minute deadline, 24 h purge and UTC-day rollover run with a fake clock and no sleep(); ADR-006 text names the provider-side limit."
    },
    {
      "severity": "minor",
      "title": "R2-7 Still over-scoped for roughly 7 hours: the live-mode machinery and synchronous judge on edit",
      "evidence": "ADR-006 :164 per-IP limit + global ceiling + append-only ledger + daily cap + 24 h lazy purge (all dormant in the public demo, which is demo-only by default); ADR-003 :124 about 30 calls per sample run, plus 20 seeded hallucinations x 3 runs and a 3-run determinism check on a live CLI at over a minute per run; ADR-016 sentence-level excerpt editing needs its own UI; 20-row table, 4 judges, 17 backend modules, 7 prompts, nonce delimiters.",
      "why_it_matters": "Round 1 asked for cuts and most were taken, but the live-mode limiter and ledger are code, tests and gate review time spent on a path the submitted link never runs. If M2+M3 slip, the cut line (README-arch.md:79) removes the layout first and the limiter second, which is the wrong order of value.",
      "fix": "Pre-declare in README-arch.md: the limiter (per-IP and global) is the first cut, with ENABLE_LIVE refusing to start unless a provider-side cap is confirmed; keep only the ledger append and the cap check. Keep fixtures as the default for every eval iteration, with the live backend for recording and the 3-run check only.",
      "acceptance_test": "README-arch.md cut line lists the limiter before the layout; SCOPE_CUTS.md has a matching row; evals run on the fixture backend by default."
    },
    {
      "severity": "minor",
      "title": "R2-8 D-018 is neither reflected nor deferred; the closed flag-category lists cannot express its causation flags",
      "evidence": "ORCHESTRATOR_DECISIONS.md:26 D-018 (scene facts, 'no objective findings', WNL/full ROM and attorney referral are causation flags; lexicon entries carry flag_type, hedge, self_report); DECISIONS.md:10 and the handoff cite 'D-001..D-015/D-017' only; ADR-013 (:243) causation categories are speculative_language, patient_report, missed_care, new_onset; app/llm/lexicon.yaml is still 'version: 1' with flag_types [pre_existing, causation_weakening, compliance] and none of accident_date_phrases, non_encounter, injection (grep returns no match).",
      "why_it_matters": "D-018 flags would have no category, no template and no J4 mapping, so a lexicon-only hit cannot be rendered. Three lexicon categories that ADR-010, 014 and 008 depend on do not exist yet, and nothing marks that as a dependency in a card.",
      "fix": "Add the D-018 categories (e.g. scene_facts, no_objective_findings, normal_exam, attorney_referral) to ADR-013 with a template each, and add an ADR-017 line: 'lexicon.yaml v2 (flag_type, hedge, self_report, accident_date_phrases, non_encounter, injection) is a researcher deliverable that blocks gaps, conflicts and the injection scan'.",
      "acceptance_test": "ADR-013 category list is a superset of the D-018 flag types; every category has a template in the template unit test; lexicon self-check loads accident_date_phrases, non_encounter and injection categories."
    },
    {
      "severity": "minor",
      "title": "R2-9 Residual contract drift: dead GROUNDING_DATE_MISMATCH path, placement of ambiguous-date entries, R-CH-2 LLM wording",
      "evidence": "LLM_VS_CODE.md:31 row 3 'The model is not asked for either' (date or provider) but the same row says 'A model-supplied date that differs from the parsed header date rejects the entry'; api.md:302 GROUNDING_DATE_MISMATCH; DECISIONS.md:146; REQUIREMENTS R-TL-3 seeded test needs a model-returned 2026-01-19 (restated for provider in ADR-016 but not for date). api.md:80 'entries are chronological by (date, seq)' with no rule for an entry whose date is ambiguous (R-IN-5 'excluded from ordering'). REQUIREMENTS R-CH-2 'the LLM only when code can't' vs ADR-011 'no LLM classifier'. R-TL-2 test 'units concatenated equal the record text' vs api.md:88 sentences that start after the 'Excerpt: \"' prefix.",
      "why_it_matters": "A reason code that can never fire is untestable and misleads the frontend; an unplaced entry is a frontend guess; unreconciled R-IDs keep the staff-engineer and requirements checkers pointing at different behaviour.",
      "fix": "Either add an optional date echo to the generator schema (cheap cross-check that makes the code reachable) or restate R-TL-3 like R-TL-9 and drop the code. Put ambiguous/missing-date entries in a separate `undated` array (or last, with date null) and say so. Add all three items to ADR-017 for the writer.",
      "acceptance_test": "Seeded test for the chosen option passes; case_01 record 8 is absent from `entries` order until confirm_date and appears in `dates_to_confirm`; ADR-017 lists R-CH-2 and R-TL-2 as changed."
    },
    {
      "severity": "nit",
      "title": "R2-10 Endpoint count says 12; the index has 11",
      "evidence": "app/README-arch.md:15 'routes from memory/contracts/api.md (12 endpoints)'; handoff 'api.md 12 endpoints'; grep -c '^| (GET|POST|DELETE)' memory/contracts/api.md = 11. Also confirm_date's 200 example (api.md:203) omits the 'entry date' its prose promises.",
      "why_it_matters": "The acceptance test I proposed in round 1 compares the api index to main.py routes; the wrong count invites a missing route.",
      "fix": "Correct to 11 (or add the 12th endpoint if one was dropped by mistake) and add the entry date to the confirm_date example.",
      "acceptance_test": "Index row count equals the route count in app/backend/main.py at the M2 gate."
    }
  ],
  "whats_right": [
    "Gap math reads only code-parsed record headers (ADR-010): dropping or rejecting r5 or r6 cannot change the 73-day flag, and the api.md gap evidence offsets are all exact.",
    "Retries live only in audited.py with 1 + 2 attempts, one llm_calls row each, an 8-minute deadline, and a closed reason-code list with fixed templates; no path demotes a failure silently.",
    "The injection design relies on structure (no tools, code-classified amounts, tag forces needs_review, lexicon floor) and calls the phrase scan advisory, which the case_07 walkthrough confirms ($50,000 unclear, only $420 totalable)."
  ],
  "questions_for_chris": [
    "Do you want the public build to run live at all? If not, the per-IP limiter and spend ledger (R2-6, R2-7) can be dropped from M4 and replaced by a provider-side spend limit on whatever key you create."
  ]
}
```
