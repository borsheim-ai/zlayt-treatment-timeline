# Review T-014 (staff-engineer-reviewer): ADRs, LLM_VS_CODE.md, API contract draft

Verdict: **fail** (2 blockers, 6 majors). This is a strong, mostly coherent design. §5.2 is fully covered, the claude-cli backend matches the verified flags, and the code-owns-facts stance is right. But the design as written lets a false gap come out marked `verified`, and its default export does not carry the verbatim excerpt that ship-bar item 1 and R-EX-2 require.

## Checks run
1. §5.2 coverage: all 11 contract rows present in LLM_VS_CODE.md (18 rows), all 7 rules present, provider abstraction signature and three backends present. Deviations recorded in ADR-003 (clinical facts dropped, J4 added, injection row, Why row). One unrecorded deviation: judge #2 only on LLM-classified amounts (F3). One deviation not in the §5.2 text and not argued: LLM may "point at" a date when a record has none (row 3), against "ambiguous -> flag, never guess".
2. JSON examples: `artifacts/review-evidence/T-014-json-check.py`, output `.out`. 12 blocks, 11 parse, 1 fails (block 7, line 155, `{…}` placeholders). Offsets in the examples are wrong against the sample text (computed: record 2 excerpt is 136 chars not 137; `ER charges:` starts at 137 not 138; `Charge per visit $185.` starts at 71 not 56; record 1 is 132 chars not 143). Illustrative, but the handoff says "cross-checked".
3. Walkthrough of 9 records: `artifacts/review-evidence/T-014-walkthrough.md`. Gaps recomputed: `[0, 7, 7, 28, 14, 73, 11, 14]`; with r5 missing from entries the r4->r6 gap is 42 days; with r6 missing r5->r7 is 87.
4. claude-cli design vs `memory/ENVIRONMENT.md`: matches (see "whats_right"); `claude --help` confirms `--json-schema`, `--tools`, `--strict-mcp-config`, `--no-session-persistence`.
5. ~7-hour buildability and 6. R-ID service: findings F6-F8 below.

## Blockers
- F1: default export has no verbatim excerpt; the cut line removes the only path that has one.
- F2: gap engine runs over LLM-produced entries, so a rejected or failed record yields a false gap that is `verified`.

## Majors
F3 judge #2 skipped on code-classified amounts; F4 accident-date conflict has one quote and an unspecified finder; F5 summary numbers and dates are not code-checked; F6 `GET /api/cases` contradicts non-goal 2 and exposes other visitors' text; F7 R-RV-3 has no API surface and date edits leave gap flags stale; F8 flag text and the R-FL-4 self-report label have no owner.

```json
{
  "card": "T-014",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit 94c7b08: memory/DECISIONS.md, docs/LLM_VS_CODE.md, memory/contracts/api.md, app/README-arch.md; read against docs/CONTRACT.md 5.2/8.2/10/D.4, spec/REQUIREMENTS.md, spec/SAMPLE_CASE_TRUTHS.md, memory/ENVIRONMENT.md; design review only, no app running; sample case = Appendix A records 1-9",
  "exercised": [
    "python3 tools/board.py show T-014 (AC read; notes/handoff claims ignored)",
    "git show --stat 94c7b08",
    "read all four changed files in full, CONTRACT 5.2 table/rules/provider text, 8.2, D.4, Appendix A/C, REQUIREMENTS.md in full, SCOPE_CUTS.md, ASSUMPTIONS.md, ENVIRONMENT.md",
    "python3 artifacts/review-evidence/T-014-json-check.py > T-014-json-check.out (12 blocks, 1 fail)",
    "python3 snippets: offsets and lengths of examples vs sample text; day gaps with a record removed (42 and 87)",
    "artifacts/review-evidence/T-014-walkthrough.md (10 truths traced step by step)",
    "claude --help | grep for --json-schema/--tools/--strict-mcp-config/--no-session-persistence/--max-turns (last absent; no tools means one turn)"
  ],
  "verdict": "fail",
  "scores": {
    "5.2 table completeness and fidelity": 4,
    "LLM/code boundary soundness": 3,
    "determinism and no silent fallback": 3,
    "provider abstraction / claude-cli safety": 4,
    "data model and audit (D.4)": 4,
    "API contract serves REQUIREMENTS": 2,
    "buildable in ~7h": 3,
    "example quality (JSON, offsets)": 3
  },
  "findings": [
    {
      "severity": "blocker",
      "title": "F1 Default export carries no verbatim excerpt, violating ship bar 1 and R-EX-2; the cut line removes the only compliant mode",
      "evidence": "memory/contracts/api.md:190 \"`cite=short` (default) gives `[Rec. 2, Central ER discharge summary, 01/09/2026]`; `quote` appends the verbatim excerpt.\"; api.md:203 \"every sentence in `letter_text` comes from an accepted entry's summary ... a citation, or a fixed heading\"; app/README-arch.md:61 cut line lists \"the quote-style citation option\"; CONTRACT 8.2 item 1 \"100% of exported statements and amounts carry a verbatim excerpt that exists in the input\"; spec/REQUIREMENTS.md R-EX-2 \"Every exported statement carries a citation ... and the verbatim excerpt\" (UT: \"for every exported line, the excerpt is a substring of the input\").",
      "why_it_matters": "The letter text is an LLM paraphrase plus a record citation. With the default (and with the quote option cut) the grounding_rate metric has nothing to measure on the exported text, and an adjuster sees a summary with no quoted source. The 100% grounding bar is the product's central claim. Charge lines in the example (`Central ER (01/09/2026): $6,240.00`) also carry no excerpt in either mode.",
      "fix": "Make quote-mode the only mode (drop the `cite` parameter): every exported entry, charge and flag line is followed by its verbatim excerpt and short citation. Remove the quote option from the cut line. If the architect wants a short mode, record an ADR changing ship bar 1 and R-EX-2 with Chris's sign-off.",
      "acceptance_test": "Export unit test over the sample accepted set: for every exported entry, amount and flag line, the attached excerpt is a whitespace-normalised substring of the input record; grounding_rate over exported items = 1.0; grep of the cut line shows no citation option."
    },
    {
      "severity": "blocker",
      "title": "F2 Gap engine runs over LLM-produced entries, so a rejected/failed record produces a false gap that is marked verified",
      "evidence": "docs/LLM_VS_CODE.md:36 \"calendar-day difference between consecutive dated entries across all providers\"; app/README-arch.md stage order puts `gaps` after `extract`/`verify`; api.md:126 f1 \"Calculated from two verified dates.\" state verified; api.md:241 ENDPOINT_NOT_VERIFIED covers only \"a gap or conflict depends on an entry that is not verified\". Repro with sample dates: python3 on Appendix A dates gives gaps [0,7,7,28,14,73,11,14]; dropping r5 (rejected to the tray) gives r4->r6 = 42 days (false flag, endpoints verified); dropping r6 turns the true 73 into 87.",
      "why_it_matters": "Dates are code-parsed record facts; a gap must not depend on whether the model produced a good entry. A single grounding failure invents a >30-day gap that the state composer calls `verified`, and it could be accepted into the internal notes. That is an invented fact and the exact failure the adjuster persona hunts.",
      "fix": "Compute gaps from the code-parsed `records.date_iso` where `date_status='parsed'`, independent of entries. Say so in LLM_VS_CODE row 9, the README-arch stage list and the api example. Records with ambiguous/missing dates are listed in the flag as \"excluded from gap math\" and force `needs_review` on every gap whose neighbours include them. Rejected-entry records still count for date arithmetic but make an adjoining gap `needs_review` with a reason.",
      "acceptance_test": "Unit test: sample records with the r5 entry forced to `rejected` still produce exactly one gap flag (r6->r7, 73 days) and no r4->r6 flag; test with r6 rejected still reports 73 days; ambiguous-date record excluded and listed."
    },
    {
      "severity": "major",
      "title": "F3 Judge #2 does not validate code-classified amounts; deviation from 5.2 and R-CH-2 is not argued in any ADR",
      "evidence": "CONTRACT 5.2 amounts row: \"Judge #2 validates each classification with the excerpt\"; spec/REQUIREMENTS.md R-CH-2 \"judge #2 checks every classification against its excerpt\"; app/README-arch.md:43 \"classify by rules, LLM only for undecided, J2 on those\"; LLM_VS_CODE.md:34 row 7; api.md a1 \"generator and judge null when code classified\"; ADR-003 deviation list names only clinical facts, J4, injection, Why.",
      "why_it_matters": "A written constraint is silently narrowed. The $185 -> `rate` call (the sample's key trap) is made by a keyword rule with no second check; a rule precedence bug (\"Charge per visit\" contains both \"charge\" and \"per visit\") would produce a verified `charge` and a PT total.",
      "fix": "Either run J2 on every classification (about 3 cheap calls on the sample) or add an ADR deviation: code-classified kinds are covered by unit tests plus a golden precedence test, and amend R-CH-2 with the writer. Specify rule precedence (rate words beat charge words) in row 7.",
      "acceptance_test": "Unit test: \"Charge per visit $185.\" -> kind `rate` for 20 phrasing variants; ADR-003 lists the deviation or R-CH-2 is amended; eval records J2 verdicts for all 3 sample amounts."
    },
    {
      "severity": "major",
      "title": "F4 Accident-date conflict: one quote in the example, no specified detector, second side is a header date outside the record body",
      "evidence": "api.md f2 evidence has a single entry `{\"record_id\": \"r7\", ..., \"start\": 0, \"end\": 0}` while explanation says \"records 1 and 2\"; f2 `origin: code+llm` with why \"second check confirmed they conflict\" but LLM_VS_CODE.md row 10 assigns structural conflicts to code only with no judge; README-arch module list has no stated-accident-date finder; CONTRACT 5.2 requires conflicts \"each citing two excerpts\"; SAMPLE_CASE_TRUTHS: \"2026-01-09 per EMS and ER records vs ... record 7\"; handoff: \"records 1-2 never state an accident date\".",
      "why_it_matters": "The conflict (a) in R-FL-2 cannot be produced as designed: the 01-09 side is a header date, not a verbatim substring of any record body, so the grounding verifier can neither pass nor reject it, and nothing says how code recognises \"Date of accident per intake form\" in the first place. Inconsistent origin/judge claims will confuse the backend worker.",
      "fix": "Specify in row 10 and ADR-003: (1) an `accident_date_phrases` list in the lexicon with the regex that extracts stated accident dates; (2) conflict evidence = the stated-date excerpt plus the earliest-treatment record's header line (record `raw_text` includes the header and grounding runs against `raw_text`); (3) origin `code`, no judge; fix the f2 example (two evidence items, real offsets, origin code).",
      "acceptance_test": "Golden unit test on sample.txt yields a conflict flag with two grounded evidence items (r7 body phrase and r1/r2 header), `origin: code`; the two dates are never merged."
    },
    {
      "severity": "major",
      "title": "F5 Summaries are checked for excerpt/provider/date but numbers and dates inside the summary are not code-checked",
      "evidence": "LLM_VS_CODE.md:32 row 4 rung 1: \"the excerpt is word-for-word in the record; the provider string appears in the record; the date equals the code parse\"; api.md ladder code_checks = {excerpt_verbatim, provider_in_record, date_matches_parse}; CONTRACT 5.2 extraction row also requires \"every amount must appear in the text\"; the sample summaries contain \"6/10\", \"40%\", \"1 week\".",
      "why_it_matters": "The most likely hallucination (a changed pain score, percentage, day count or dollar figure in the paraphrase) is caught only by a Haiku judge. LLM_VS_CODE rule 1 says numbers are never a model's job. GROUNDING_AMOUNT_NOT_IN_TEXT can currently never fire because the generator schema has no amounts field.",
      "fix": "Add a rung-1 check: every numeral, date and dollar token in the summary must occur in the record text (after normalisation); failure -> `rejected` with a new reason code `GROUNDING_NUMBER_NOT_IN_TEXT`. Add it to D.4 `code_checks` as `summary_numbers_in_text`. Also have R-RV-3 reuse the same function.",
      "acceptance_test": "Unit test: summary \"Pain 9/10\" against record \"Pain 4/10\" -> rejected; seeded set includes 5 number-swap hallucinations that the code check alone catches."
    },
    {
      "severity": "major",
      "title": "F6 GET /api/cases (case list) contradicts non-goal 2 and exposes other visitors' pasted text on the public Space",
      "evidence": "api.md:18 \"| GET | `/api/cases` | list cases (resume) |\" and the list example; spec/REQUIREMENTS.md section 5 item 2 \"One case at a time, no case list, no search across cases\"; SCOPE_CUTS.md row 2 \"Multi-case / matter management\"; DECISIONS.md:157 \"per-session rate limit\" with no session mechanism defined anywhere.",
      "why_it_matters": "On the shared HF Space (one SQLite, 24 h retention) any visitor can list and read every other visitor's pasted case and audit including full prompts. That is a design defect independent of the synthetic-data banner, and it contradicts a logged scope cut. \"Per session\" limits have no session id to key on.",
      "fix": "Remove `GET /api/cases` (and the `Resume` use) or scope it to an unguessable per-browser token set by cookie at first POST; define the session as that cookie and key rate limits on it. Use unguessable case ids (random 128-bit, not `case_8f3a`).",
      "acceptance_test": "Integration test: two clients with different cookies; client B cannot GET client A's case or list it (404); rate limit counts per cookie; no list endpoint in the api index."
    },
    {
      "severity": "major",
      "title": "F7 R-RV-3 has no API surface, and a date edit leaves stored gap flags stale",
      "evidence": "spec/REQUIREMENTS.md R-RV-3 \"An edit that adds a date or number not present in the excerpt shows a warning before acceptance. (Design decision for architect to confirm ...)\"; api.md review response is `{item, totals, review}` with no `warnings` and DECISIONS.md has no ADR answering it; api.md:172 \"Editing a date re-validates it as a real ISO date and re-sorts.\"; ADR-002 \"Totals are not stored ... a dismissal or edit can never leave a stale total\" but flags (including `computed_json` days) are stored; run endpoint clears all derived rows on rerun.",
      "why_it_matters": "A must-have requirement the architect was asked to confirm is unanswered; the API cannot serve it. And ADR-002 protects totals from staleness but not gaps: after the paralegal fixes an ambiguous date, the gap flag (computed at run time, excluded the record) still says what it said, and the only remedy is a rerun that wipes derived items.",
      "fix": "Add `warnings: []` to the review response (fires when the edited text contains a numeral/date token absent from the excerpt; non-blocking, uses the F5 function) and record the confirm in an ADR. Compute gap flags at read time from record dates (like totals) or recompute them inside the review handler after any date edit; state the choice in ADR-002.",
      "acceptance_test": "Unit: edit summary adding \"$9,000\" returns a warning; E2E/API: set the date of an ambiguous record, GET case shows a recomputed gap list without rerun."
    },
    {
      "severity": "major",
      "title": "F8 LLM-written flag text and the R-FL-4 patient-self-report label have no owner or validation",
      "evidence": "api.md f1/f2 `title` and `explanation` fields and the flags edit keys `title`, `explanation`; LLM_VS_CODE row 13 \"J4 confirms the category\" only; no flags prompt output schema anywhere; spec/REQUIREMENTS.md R-FL-4 \"Record 9 is labeled as patient self-report, not a physician opinion\"; SAMPLE_CASE_TRUTHS: \"(patient self-report, not a physician's causation opinion)\".",
      "why_it_matters": "For gap/conflict flags the text is code-templated, but for prior and causation flags the `explanation` is unconstrained model prose that goes into `internal_notes_text`. Nothing checks it for causation claims (the sample's forbidden outputs). The self-report label has no field or rule, so R-FL-4 cannot pass by design.",
      "fix": "Specify the flags LLM output schema: `{type, record_id, excerpt, phrase_category}` with `phrase_category` from a closed list (including `patient_report`, `speculative_language`, `missed_care`, `new_onset`, `prior_condition`); `title` and `explanation` are code templates keyed by category; no free LLM prose reaches a flag. Put the schema in ADR-003/api.md.",
      "acceptance_test": "Schema unit test rejects extra prose fields; the record-9 flag carries category `patient_report` and its template text says \"Patient states\"; grep shows no LLM string rendered in flag `explanation`."
    },
    {
      "severity": "minor",
      "title": "F9 Retry semantics inconsistent and owner unspecified; no run-level deadline",
      "evidence": "api.md:231 `SCHEMA_INVALID` \"after 2 retries\" (3 attempts) vs api.md:242 `LLM_FAILED_AFTER_RETRIES` \"failed twice\" (2 attempts); ADR-004 \"LLMError (... invalid JSON after the provider's own validation ...)\" does not say whether the provider also retries; ADR-003 point 7 does not name the module; 120 s timeout x 3 attempts x 9 records at concurrency 3.",
      "why_it_matters": "Hidden retries are forbidden by the lens; an off-by-one here makes R-CO-9's unit test ambiguous, and a provider-level retry would produce llm_calls rows the audit never sees. Worst-case wall clock is about 18 minutes with no run deadline.",
      "fix": "State: total attempts = 1 + 2 retries; the retry loop lives only in `audited.py`, one `llm_calls` row per attempt; providers never retry; add a run-level deadline (e.g. 8 min) that ends the run as `failed` with items finalised.",
      "acceptance_test": "Unit with a failing fake backend: exactly 3 llm_calls rows with attempt 1,2,3 and prompts differing on retry; items end `LLM_FAILED_AFTER_RETRIES`; fixture file for the retry prompt is keyed separately."
    },
    {
      "severity": "minor",
      "title": "F10 Offsets are defined against raw text but matched on whitespace-normalised text; examples have wrong numbers; block 7 is not valid JSON",
      "evidence": "ADR-002 \"Excerpt offsets ... computed by code by locating the verbatim excerpt inside the record\" vs R-TL-2 normalised match; T-014-json-check.out: `block 7 line 155: FAIL`; computed lengths: record 2 excerpt 136 (example says excerpt_end 137), `ER charges: $6,240.` at 137 (example 138), `Charge per visit $185.` at 71 (example 56), record 1 is 132 chars (example char_count 143); f2 evidence offsets `0, 0`.",
      "why_it_matters": "A multi-line paste that normalises whitespace will produce a verified entry whose raw offsets cannot be found; R-ST-1 highlights would silently fail (R-ST-2 has no reason code). Frontend coding against wrong numbers wastes time.",
      "fix": "Define offsets on the raw text via a normalised-to-raw index map built in grounding.py; add reason code `HIGHLIGHT_NOT_FOUND` -> needs_review (R-ST-2); correct the example numbers and replace `{…}` with valid JSON.",
      "acceptance_test": "Unit: excerpt spanning a newline in the record returns correct raw start/end; the json-check script reports 12/12 blocks parse; example offsets equal `record_text[start:end] == excerpt`."
    },
    {
      "severity": "minor",
      "title": "F11 GET /api/cases/{id} returns entries sorted needs_review-first, but R-TL-1 requires the timeline be chronological",
      "evidence": "api.md GET case: \"Items are returned pre-sorted: `needs_review` first, then `verified`, each by date\"; entries carry `record_id` but no `seq`; R-TL-1 \"Same-date records (1, 2) keep source order\".",
      "why_it_matters": "The product's main view is the chronology; two sort orders in one array invite a frontend bug and r1/r2 ordering needs a join to records.",
      "fix": "Return `entries` in chronological order (date, then record seq) with `seq` on each entry; the review order is `review.queue` only.",
      "acceptance_test": "API test: entries array is sorted by (date, seq) regardless of state; r1 precedes r2."
    },
    {
      "severity": "minor",
      "title": "F12 Over-engineering to cut for a ~7 hour build",
      "evidence": "ADR-006 rate limit + spend cap + 24 h purge + BYO key; api `?full=1`, `format=jsonl`, `cite=short|quote`, `reset`, flag `title`/`explanation` edit, `GET /api/cases`, `DELETE`; LLM_VS_CODE row 3 (LLM chooses among date candidates); row 1 LLM split fallback (already on cut line); row 14 phrase scan; ADR-003 estimate \"about 35 calls\" with 4 judges; SCOPE_CUTS #13 already cuts the split fallback while LLM_VS_CODE row 1 still documents it.",
      "why_it_matters": "Docs describe behavior the code will not have, which violates \"the table must match the code\" (CONTRACT 5.2), and every extra surface needs a test and a gate review. Dev loop on claude-cli at 30+ calls per run will also be slow and eats Chris's subscription limit during eval iteration.",
      "fix": "Cut from the contract now: row-3 LLM date pointing (ambiguous -> flag, per 5.2), BYO key, `?full`, flag title/explanation edit, case list, the split fallback from row 1 text (state 'one record, flagged'). Keep fixtures as the default for eval iteration; run the live backend only for recording and the 3-run determinism check.",
      "acceptance_test": "LLM_VS_CODE.md contains no row or sentence describing a behavior listed in SCOPE_CUTS.md; api.md endpoint index equals the set of routes in app/backend/main.py at the M2 gate."
    },
    {
      "severity": "minor",
      "title": "F13 Injection scan is presented as a security control; REQUIREMENTS wording says no entry changes state",
      "evidence": "LLM_VS_CODE.md row 14 \"Prompt injection is a security control, so it cannot depend on the model noticing\" (a short phrase lexicon); ADR-008 forces INJECTION_SUSPECTED -> `needs_review` on the record's entries; spec/REQUIREMENTS.md R-RV-6 \"no flag or entry changes state\".",
      "why_it_matters": "A phrase list is trivially bypassed; the real controls are no tools, schema validation and the human rung (ADR-008 items 1-3, 6). Overclaiming invites the privacy reviewer to break it. The R-RV-6 wording and ADR-008 behavior disagree.",
      "fix": "Reword row 14 to \"advisory warning; the control is the absence of tools and the schema/human rungs\" and ask the writer to align R-RV-6 (\"no unreviewed state change; an advisory needs_review is allowed\").",
      "acceptance_test": "Row 14 text no longer says 'security control'; R-RV-6 and ADR-008 agree; golden injection case asserts review_status of all items remains `pending` and tool-less backend flags unchanged."
    },
    {
      "severity": "minor",
      "title": "F14 Demo-mode audit loses the real backend; fixture key fragility not mitigated; cwd/fence handling unspecified",
      "evidence": "ADR-004 fixtures keyed by sha256(model+system+user+schema), `backend: fixture` on every demo item (api examples); CONTRACT D.4/5.2 \"audit record stores which backend produced each item\"; ADR-004 claude-cli flags do not say how the cwd outside the project is chosen or whether a markdown-fenced reply is stripped.",
      "why_it_matters": "A reviewer opening Why? in the public demo sees `fixture`, not that sonnet-5-5 via claude-cli produced it. Stripping ```json fences is a repair; if allowed it must be explicit, else the CLI backend fails on common output.",
      "fix": "Store `recorded_from: {backend, model, recorded_at}` inside each fixture file and surface it in the ladder; state that the CLI backend runs in `tempfile.mkdtemp()` and accepts exactly one fenced or bare JSON object, rejecting anything else.",
      "acceptance_test": "Ladder JSON for a replayed item shows `backend: fixture` and `recorded_from.backend: claude-cli`; unit test for fenced/bare/prose-wrapped replies."
    }
  ],
  "whats_right": [
    "claude-cli backend spec matches every verified flag (tools off, hooks disabled, strict MCP, no session persistence, cwd outside project, 3-way semaphore, 120 s timeout, Pydantic re-validation) and the audited.py chokepoint means no call skips the audit.",
    "State/review separation (ADR-005): compose_state is a pure function with a closed reason-code list, rejected items go to a visible tray and return 409 on accept, and no endpoint bulk-accepts; totals are computed at read time so they cannot go stale.",
    "Fixture backend keyed by prompt hash runs the real pipeline in demo mode and raises FixtureMiss instead of inventing; ADR-009 splits letter text from internal notes so adjuster-useful flags cannot leak into the demand letter."
  ],
  "questions_for_chris": [
    "Is a short, citation-only export (no excerpt in the letter text) acceptable to you, or must every exported line carry the verbatim quote as ship bar 1 reads? If short mode is wanted, the ship bar needs an ADR.",
    "How much of your claude.ai subscription limit are you willing to spend on live-backend eval iteration (about 25-35 calls per sample run, more for 20 seeded hallucinations x 3 runs)?"
  ]
}
```
