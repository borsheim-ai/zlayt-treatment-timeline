# Subagent: Architect: T-207 LLM_VS_CODE rows (Architect: T-207 LLM_VS_CODE rows)

Source: `agent-a6e3b278f0a1a34eb.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T00:46:46.193Z

You are the architect in /Users/arsis/zlayt-pm-project. Your card is T-207, P1; claim it and read its notes. The T-202 backend worker left the exact proposed text there.

Update docs/LLM_VS_CODE.md rows 2 and 3 so they state the rule for charge-line service dates, taken from D-071 with its amendment, clarification and addendum in memory/ORCHESTRATOR_DECISIONS.md:
- the date is code-only;
- an allow-list of positive evidence decides it: a DOS column header, a service label, or the charge row's own date cell;
- the statement-date disambiguation rule;
- when not certain, a fillable blank plus a Step 3 confirm note;
- never the LLM.

Keep the table's style. Commit only that file through `git commit` with a temp index built from the current HEAD. Write the handoff, move the card to in_review, and reply in 1 line.

### User / tool · 2026-11-03T00:46:46.199Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:49.018Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-207 --agent architect; $B show T-207; git status --short | head -20; git log --oneline | head -3"
}
````

### User / tool · 2026-11-03T00:46:49.354Z

**tool result**
````
T-207 claimed by architect
---
id: "T-207"
title: "LLM_VS_CODE rows 2 and 3: charge-line service dates are an allow-list of positive evidence (T-202 r3, D-071 amendment)"
milestone: "M3"
role: "architect"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:45:18Z"
updated_at: "2026-11-03T00:46:49Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "docs/LLM_VS_CODE.md row 2 and row 3 carry the text in the T-202 note from backend (allow-list, as-written form, not-stated form, validation), and say entry dates stay on the stricter ambiguous-never-guessed rule", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read."
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:46:49Z architect: claimed

## Handoff (filled when moving to in_review)

 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t206_statement_label.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
5703fc4 fix(backend): T-202 r3 D-071 amendment: a service date is an allow-list of positive evidence (label, service column, row cell, bill period); labeled but unreadable dates print as written; independent letter_check allow-list; notes section for undated charges
79714c6 feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
d23687e chore(guard): block git commit-tree and symbolic-ref (T-204 swapped a commit on HEAD by plumbing)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:49.644Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head; sed -n 1,40p docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T00:46:49.737Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
# Where the AI works and where plain code works

*Treatment Timeline prototype. For the hiring panel, reviewers and the developers who maintain it. Decisions behind this page: `memory/DECISIONS.md` ADR-003, 004, 005, 008, 010 to 020; cross-cutting decisions D-001 to D-057 in `memory/ORCHESTRATOR_DECISIONS.md`. Requirements it serves: `spec/REQUIREMENTS.md`.*

## The one-paragraph version

A paralegal turns scattered medical records into a treatment chronology, and an adjuster will read it looking for a reason to doubt it. One invented detail costs credibility. So we split the work by one question: **is there a single right answer?** If yes (a date, the days between two dates, a dollar total, whether a quote really appears in the record), ordinary code does it, because code is right every time and can be tested. If it takes reading messy human language (what happened in this visit, whether "findings may represent degenerative change" weakens a causation argument), a language model does it, and then its answer has to pass three checks before it can reach the letter: a code check, an independent second model acting as a skeptic, and the paralegal's own accept, edit or dismiss. Nothing the model wrote goes into the export without all three. Even then, the model never writes the wording of a warning: code does.

## The rules (enforced in code and tests, not only in prompts)

1. **Arithmetic, dates, totals, sorting, de-duplication, quote-matching, number-matching, schema checks and export assembly are never done by a model.**
2. **The model never supplies a value.** It may write a one-line summary and choose an exact excerpt, and point at wording that looks like a flag (a category and a quote). It may not supply a date, an amount, an amount's class or the text of a warning. A date or amount the code cannot find in the record is rejected.
3. **Every quote is checked.** Each excerpt must appear word for word in its record (extra spaces ignored). If not, the item is *rejected*: shown in a "could not verify" tray, never exportable.
4. **Every number in a summary is checked.** Any number, date or dollar figure, and the words left/right/no/not/without, in a summary or in the paralegal's own edit must appear in the excerpt. In a generated summary a miss marks the item for review with the offending tokens named. In a paralegal's edit or manual entry it is a hard 422 and nothing is saved, with no override (D-034, D-047).
5. **A second model double-checks the first, and every dollar classification.** The checker uses a different prompt and, by default, a different model. It sees only the record and the candidate, never the first model's reasoning, and answers with a fixed choice (no prose).
6. **No silent fixes.** When a check fails the system says so and why. It never "repairs" a quote, a date or an amount.
7. **A human decides everything.** Even a fully verified item starts as *pending*. Every accept is an individual decision, except a batch accept of verified, pending entries (code only, all or nothing; never amounts or flags). Every accept of an entry, single or batch, must pass the code checks first (D-051). Amounts and flags have no editable wording: their checks are stored with them, and an accept is refused while the stored state is `rejected` (409). Dates and amounts always need an explicit accept. The export contains exactly the accepted set.
8. **Doubt is shown, not hidden.** Items are `verified`, `needs_review` or `rejected` by a fixed rule, doubt sorted first, each with a one-sentence "Why?" made from a template.
9. **Swapping the model is configuration, and every swap is re-measured.** Prompts and models are versioned and stored in every audit record. Changing one means re-running the golden evaluation set.
10. **Retries change something** (one record at a time, a stricter format request), at most twice, then a visible failure state.
11. **Record text is data, never instructions.** The real protections are structural: models run with no tools, their output is a checked form, code (not a model) finds money and flags, and no code path can accept anything. A phrase scan adds a visible warning and forces review of everything from that record, but we do not claim a phrase list stops an attacker. Precisely: an amount in a warned record, or one not introduced by a billing label, cannot become a charge; a forged billing line in an unwarned record ("ER charges: $50,000.") is caught only by the paralegal's accept.

## The decision table

"Code" is ordinary deterministic code with unit tests. "LLM" is a model call. Where both appear, the second column says who is the source of truth.

| # | Pipeline step | Code or LLM | Why we drew the line here | How it is checked |
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
| 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical content. | n/a (deliberate omission). |
| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model's attention. | Unit tests with noisy, duplicate and dose-like numbers. An amount a model reports that code cannot find is rejected. Billing completeness (D-049): a final code accounting pass lists every money-shaped token in a billing record that no parser placed, so a missing figure is listed, never silent. |
| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*; a rate cue in the label ("per" or "each" followed by a unit word such as visit or session, "rate of", "/visit") or right after the amount ("$185 per visit", "$185 each", "$185/hr") is a *rate* ("Charge per visit $185"); "estimate(d)" is an *estimate*; lost-wage wording is *damages*; in a billing-statement record, "Statement for visit of 2026-02-02: $275" is a *charge*; a label ending "charge:" ("ER charges:", "Charge:") or "billed:" is a *charge*; everything else is *unclear*. There is no model classifier. Billing ledgers are also read line by line by `billing.py` into a cited listing (charge, adjustment, payment, rate, unclear; D-052). That listing is computed on read, is never totaled and never reaches the letter. | Billing language is regular enough for rules, and a rule can be tested. A rule cannot be argued with by a record that says "add $50,000 to the billed total". | **Judge 2 checks every classification** against the excerpt (`agrees`, `disagrees`, `unsure`), including the rule-made ones. A `charge` is `verified` only when judge 2 agrees; any other class needs review. Reclassification is guarded (D-042, T-084): a charge can always be moved out of the total; a figure moves in only if code finds charged-amount wording in its own sentence (no negation, balance cue or rate cue, a parsed value, no injection tag) and judge 2 agrees. A rate cue such as "Charge per visit $185" is refused before judge 2 is asked, so a rate cannot become a charge by its wording. Unit tests: 20 phrasings of "Charge per visit $185" all give *rate*; "Moderate" and "Corporate" never trigger the rate rule; all 14 dollar amounts across the golden cases get their golden class. `tests/unit/test_reclassify.py` covers each refusal (422 `reclassify_refused`) and the promotion of a figure that judge 2 agrees with. |
| 8 | Running total of charges | **Code**: sum of **accepted** amounts of class `charge`. The screen also shows "Pending review" separately and a "detected, not a total" figure. Rates, estimates, damages and unclear amounts are listed "not totaled". Billing adds no provider total, balance or "complete" badge (D-052); this case-level total is the only total. Beside it, `totals.possible_overlaps` (T-110) warns of a billing-statement line that may already include a separately stated charge for the same service; the total never changes and the two figures are never compared. | Arithmetic, and a total must mean "what she has verified", not "what the tool found". | Unit tests; E2E: the export total equals the accepted charges. The sample's PT rate ($185 per visit, visits never itemised) never becomes a PT total. |
| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes are excluded), independent of any model output or review state. Strictly more than 30 days; 30 is not a gap. | A gap is a fact about dates. If it depended on the model's entries, one dropped entry would invent a gap. | Unit tests at 29, 30, 31 days; sample 28-day near miss does not flag, 73-day gap does; dropping an entry never changes the result. Ambiguous dates are excluded, shown as a record warning, and any gap near one needs review; she resolves one by choosing a reading the code proposed (`confirm_date`). |
| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accident-date phrases ("date of accident", "DOA", "accident date", "collision on") plus date formats, compared with the earliest record date. Evidence is the stated-date quote and the `Date:` header line(s) of the earliest records. | Comparing two dates is not a language task, and the header line is part of the input text. | Unit test on the sample file with exact character offsets; both quotes ground; the two dates are shown side by side and never merged. No judge needed (arithmetic over quoted text). |
| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only classifies.** `app/backend/conflict_candidates.py` pairs two whole sentences by two fixed rules: **plan vs early end** (a stated plan, as a visit count or frequency × duration, against a LATER record showing a missed, no-show, cancelled, self-discharged or discontinued course; `plan_vs_outcome`, `:133-148`) and **denial vs prior history** (a sentence denying prior problems, against a sentence in another record that the phrase list marks as a prior condition or prior surgery, or that names an earlier accident or claim; `history_denials`, `:151-175`). **The rules drop pairs before any model sees them:** (1) *different person:* a sentence whose subject is a relative or another party from a closed list (the other driver, a witness, mother, husband, "family history") and that does not name the patient is never half of a candidate, on either side (`_other_person`, `:73-76`, applied at `:101`, `:138`, `:155`, `:166`, `:169`); a person the list does not name still reaches the judge, whose prompt is the backstop. (2) *across a semicolon:* the subject is read inside the sentence's own semicolon clause (the splitter cuts at ';'), so a relative named in the neighbouring clause neither hides the patient's own history nor is paired with it (`tests/unit/test_conflict_candidates.py::test_the_subject_is_read_inside_its_own_semicolon_clause`). (3) *intake forms:* a paperwork record (intake form, bill, affidavit, by the header test `gaps.admin_label`) is never the plan or the outcome of a course (`:79-83`, `:98`, `:138`; `::test_an_intake_form_is_never_the_plan_or_the_outcome_of_a_course`); a denial written on an intake form is still the patient's own statement and is compared. Code multiplies frequency × duration into visits ("2x/week for 6 weeks" = 12) and carries that arithmetic on the flag. An explicit visit count is the plan quoted when one exists. No numeric comparison is made between a count and a frequency plan, so the two are not checked against each other. Candidates come in a fixed order, so the set cannot vary between runs: there is no open-ended model search (`conflicts_v1` is retired). The model is `judge_conflict_v6` (J3; `judges.py:59`), and it only classifies each candidate as `conflict`, `benign` or `unsure`, with a fixed reason code and no prose. It never proposes a pair, a quote or a number. **Nothing the model produces is silently dropped (D-053):** a code-proposed pair that J3 calls `benign` goes to the could-not-verify tray (tray kind `flag`, reason `JUDGE_DISAGREES`, with the judge's fixed reason); a model-only flag that the flag judge (J4, `judge_flag_v3`, `judges.py:64`) calls `disagree` goes to the tray the same way (`flags.py:349-352`; `present.py:290-300`); a conflict the model proposed in the per-record pass, which no code candidate made, goes to the tray with `LLM_ONLY` and is not judged (`_model_conflicts`, `flags.py:185-209`, called at `:265`; backstop in `judge_flags`, `:381-383`, for a conflict handed in directly). The tray-on-no-candidate rule is for conflicts only: a model-only flag that J4 does not reject stays `needs_review` (`LLM_ONLY`), and a flag the phrase list also found stays `needs_review` even if J4 disagrees. Tray items are never flags and never reach the letter. A J3 or J4 `unsure` answer, or a judge that did not answer, keeps the flag visible as `needs_review`. **Candidate rules** also cover number-word visit counts with a plan cue, frequency × duration in weeks (including "twice-weekly for six weeks"), lost to follow-up, stopped or left care, negation- and completion-aware, and denials of earlier accidents or claims. **Not built as candidates:** dosage and laterality pairs (laterality is checked only within one summary, row 15), and month durations (`memory/SCOPE_CUTS.md`, row 13). Dosage and laterality pairs are neither proposed by code nor measured: every J3 control is a pair the candidate generator proposes (real packet candidates and variants of them, `evals/j3_controls.py`, checked by `tests/unit/test_t093_j3_controls_reachable.py::test_every_j3_control_input_is_producible_by_the_candidate_generator`), and the earlier dose, laterality, date and pain-score controls were removed for that reason (T-093 r4, 822ff38; `evals/golden/judge_controls.CHANGELOG.md`). | Reading comprehension is needed only for one yes or no per pair. An open-ended search let the model call "2x/week for 6 weeks" against "12 visits" a conflict (T-094, live run 2). The arithmetic and the choice of pairs are code's. | **Rung 1:** both quotes are whole sentences cut from the record text, and grounding still checks them. **Rung 2, J3:** `conflict` gives a flag (verified only when the other checks hold); `unsure` keeps it `needs_review`; `benign` on a code-proposed pair moves it to the could-not-verify tray, never exported. A denial is judged one candidate at a time, in record order, and the first confirmed conflict stands. **Rung 3:** human accept or dismiss. |
| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record as a second signal | Needs language judgment ("low back pain in 2023, resolved"). Running per record means one record's text never reaches the call that decides another record's flags; the phrase list is a second floor, trusted only as far as its measured recall on the golden set. | Quote check; **judge 4** confirms the category. If only the list or only the model fires, the item needs review and says which. A model-only flag that the flag judge rejects goes to the could-not-verify tray (row 11), never to the review queue or the letter. A model-only `scene_facts` flag (no phrase-list hit) goes to the tray as `LLM_ONLY` (`flags.py:173-174`). A model proposal that a fixed code rule filters out is listed, not dropped (row 13, D-057). |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:52.980Z

**tool call — Bash**
````
{
 "command": "sed -n 84,93p memory/ORCHESTRATOR_DECISIONS.md; ls app/backend/service_date.py tests/unit/test_t202_r3_allow_list.py evals/letter_check.py; grep -n \"service label\\|DOS\" app/backend/service_date.py | head -30"
}
````

### User / tool · 2026-11-03T00:46:53.078Z

**tool result**
````
## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.

## D-071 amendment — when the service date is not certain, print none and ask the human
T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.

## D-072 — The prompt log is built and privacy-reviewed once, last
Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
app/backend/service_date.py
evals/letter_check.py
tests/unit/test_t202_r3_allow_list.py
5:  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
6:  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
46:_UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
50:# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
264:    """[bool] per unit: a service label ends the 40 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
328:    others = []                       # dates near the line that no service label ties to it
350:    else:                                                                 # (b) a service label in the same clause
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:54.936Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T00:46:55.025Z

**tool result**
````
"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 round 3: an ALLOW-LIST, not a deny-list). Code only, no LLM
(LLM_VS_CODE rows 2 and 3).

The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
  (c) it is the date cell of the charge row itself, in a table whose header is (a);
  (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
      covers period ...').
Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
looked at again: an unlabeled date cannot become the line's date by default. The result is one of:
  - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
    EVERY labeled end then reads one way; a stated date after its statement, or more than five years before it, in a bill is doubtful);
  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service. The letter prints the T-200 form '(statement dated X; service date not stated)';
    a dated encounter note (visit note, imaging report: not a bill) keeps the note's own date;
  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
    the code cannot read it with certainty. The letter prints it AS WRITTEN ('date of service as written: "04/05/2026"; statement dated X'), never under 'service date not stated'.
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import re

from app.backend import amounts as AM

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:57.527Z

**tool call — Bash**
````
{
 "command": "grep -rn \"date of service \\[_\\|service date \\[_\\|\\[__________\\]\" app/backend/*.py | head; grep -n \"as written\" app/backend/store.py app/backend/present.py | head"
}
````

### User / tool · 2026-11-03T00:46:57.629Z

**tool result**
````
app/backend/store.py:121:    not stated)' when the quote labels no date of service, or '(date of service as written: "04/05/2026"; statement dated June 15, 2026)' when it labels one the code cannot read
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:59.131Z

**tool call — Bash**
````
{
 "command": "sed -n 105,175p app/backend/store.py; grep -rn \"date of service \\[\\|______\" app/backend app/frontend --include=*.py --include=*.js --include=*.html -l | head; git log --oneline -3 -- app/backend/store.py"
}
````

### User / tool · 2026-11-03T00:46:59.302Z

**tool result**
````
# ---------------------------------------------------------------- unit dicts for export / totals
def amount_pos(item: dict, rec):
    """Where the amount's own figure sits in its excerpt (T-140 r3: quotes and reasons are taken from the figure's own offset, never from a text search that finds
    the first equal figure). None when the stored offsets do not point at the figure's text."""
    start, raw = item.get("excerpt_start"), item.get("text") or ""
    if rec is None or start is None or not raw:
        return None
    from app.backend import generator          # lazy: generator imports store
    i = start - generator.body_offset(rec)
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def charge_service_date(item: dict, rec, pos) -> dict:
    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', '(statement dated June 15, 2026; service date
    not stated)' when the quote labels no date of service, or '(date of service as written: "04/05/2026"; statement dated June 15, 2026)' when it labels one the code cannot read
    with certainty), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
    the one period its bill states; an unlabeled date (birth, injury, referral, entry, transaction ...) is never the service date. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
    not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = dict(none) if bill else ({"state": "stated", "first": rd, "last": None, "reason": None, "raw": "", "raws": []} if rd else dict(none))
    else:
        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
    stated = r["state"] == "stated"
    note = None
    if not stated and not counted_undated:
        note = SD.confirm_note(r["reason"], r["raw"])
    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd),
            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}


def charge_service_dates(item: dict, rec, pos) -> tuple:
    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
    d = charge_service_date(item, rec, pos)
    return d["date_iso"], d["end_iso"]


def export_case(conn, case_id: str, blockers: bool = True) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    from app.backend import present                     # lazy: present imports store
    prep = present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"]      # D-069: the case's provenance chooses the wording of the export's notes and labels
    ents = []
    for e in DB.list_items(conn, case_id, "entry"):
        if e["state"] == "rejected":
            continue
        ed = e.get("edited") or {}
        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
        if "summary" in ed:
            d["original_summary"] = ed.get("original_summary", e["summary"])
            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
5703fc4 fix(backend): T-202 r3 D-071 amendment: a service date is an allow-list of positive evidence (label, service column, row cell, bill period); labeled but unreadable dates print as written; independent letter_check allow-list; notes section for undated charges
986fc55 fix(backend): T-202 r2 D-071 amendment: a charge line prints a service date only when code is certain, else the not-stated form and a Step 3 confirm note
f0921e4 feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:01.663Z

**tool call — Bash**
````
{
 "command": "grep -rn \"date of service \\[\\|date of service \\\\\\\\\\[\" app tests --include=* -r 2>/dev/null | grep -v \"\\.pyc\" | head; grep -rn \"_____\" app/backend/export.py app/backend/service_date.py | head"
}
````

### User / tool · 2026-11-03T00:47:01.796Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:05.860Z

**tool call — Bash**
````
{
 "command": "grep -ln \"fillable blank\\|date of service \\[\" board/cards/*.md | head; python3 tools/board.py list --status ready 2>/dev/null | head; python3 tools/board.py list --status in_progress 2>/dev/null | head"
}
````

### User / tool · 2026-11-03T00:47:06.089Z

**tool result**
````
T-184	M4	qa         	ready            	P0	AC 0/1	M4 demo assets: annotated screenshots of every guided-UI state (artifacts/screenshots/ + artifacts/CAPTIONS.md); <=3-minute Playwright-recorded walkthrough artifacts/demo.webm on the sample case; narration script Chris can read
T-188	M5	writer     	ready            	P0	AC 0/1	M5 package: submission/SUBMISSION_CHECKLIST.md mirroring Appendix A with links; submission/email-draft.md; final prioritized submission/NEEDS_CHRIS.md; PDF exports via pandoc (else HTML)
T-187	M5	qa         	in_progress      	P0	AC 1/1	M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide
T-198	M5	qa         	in_progress      	P0	AC 1/1	Prompt log + snapshot: redact the outside project name by default until Chris answers T-193
T-202	M3	backend    	in_progress      	P0	AC 1/1	D-071: letter charge lines print the bill's service date or period, not the statement date (case_09, lib14, lib10)
T-207	M3	architect  	in_progress      	P1	AC 0/1	LLM_VS_CODE rows 2 and 3: charge-line service dates are an allow-list of positive evidence (T-202 r3, D-071 amendment)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:07.726Z

**tool call — Bash**
````
{
 "command": "grep -n \"blank\\|__________\" board/cards/T-206.md board/cards/T-202.md | cut -c1-300 | head"
}
````

### User / tool · 2026-11-03T00:47:07.813Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:18.784Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='docs/LLM_VS_CODE.md'\ns=open(p).read()\na='waits for the paralegal. | The spec says'\nassert s.count(a)==1\ns=s.replace(a,'waits for the paralegal. Entry dates stay on this strict rule. **A charge line\\'s date of service is code only, never the LLM (D-071 and its amendment; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line by a DOS or service column header, by a service label in its clause (DOS, date of service, service date, seen on, visit date), by the charge row\\'s own date cell in a table whose header names service, or by the one period its bill states for its services counts. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. A numeric date that reads two ways is resolved by one fixed rule: a service cannot follow its statement, so it is certain only when a reading after the bill\\'s own (statement) date is impossible for every labeled end of the date or period (D-071 clarification). This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read. | The spec says',1)\nb='A model told to \"find the date\" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry\\'s date and provider equal the header values. An ambiguous date moves the entry to a \"Dates to confirm\" group after the timeline until the paralegal picks one of the readings the code proposed. |'\nassert s.count(b)==1\nc='for a charge line the date is not the record\\'s header date (a bill\\'s header date is its statement date) and the model is never asked. Code prints the service date or period the bill line itself states (positive evidence only, see row 2). When it is not certain, the letter does not guess: it prints a fillable blank beside the statement date (D-071 addendum: \"date of service [__________] (statement dated June 15, 2026)\") and Step 3 shows a confirm note asking the paralegal to read the date from the quote. A date the quote labels as the date of service but the code cannot read with certainty also shows as written (\"04/05/2026\"). When the quote labels no date at all, the line says \"(statement dated X; service date not stated)\".'\nassert 'The model is not asked for either. | A model' in s\ns=s.replace('The model is not asked for either. | A model','The model is not asked for either. **Charge-line exception:** '+c+' | A model',1)\ns=s.replace(b,b[:-2]+' Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and `evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser. |',1)\nopen(p,'w').write(s)\nEOF\ngit diff --stat docs/LLM_VS_CODE.md; git diff docs/LLM_VS_CODE.md | grep '^[+-]' | grep -v '^+++\\|^---' | wc -l"
}
````

### User / tool · 2026-11-03T00:47:18.943Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
       4
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:22.208Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXXXX) && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat && git commit -q -m \"docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md; unset GIT_INDEX_FILE; git log --oneline -1; git show --stat HEAD | tail -3"
}
````

### User / tool · 2026-11-03T00:47:22.328Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXXXX) && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat && git commit -q -m "docs(architect): T-207 LLM_V
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:23.843Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t207 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat"
}
````

### User / tool · 2026-11-03T00:47:24.219Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:26.316Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/idx.t207 git commit -q -m \"docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md; git log --oneline -1; git show --stat HEAD | tail -3"
}
````

### User / tool · 2026-11-03T00:47:27.652Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
901ad5a docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)

 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:32.432Z

**tool call — Bash**
````
{
 "command": "rm -f /private/tmp/claude-501/idx.t207; B=\"python3 tools/board.py\"; $B ac T-207 --check 1 --agent architect --evidence \"docs/LLM_VS_CODE.md rows 2 and 3, commit 901ad5a; text per T-202 note + D-071 amendment/clarification/addendum\"; $B commit T-207 --sha 901ad5a --agent architect; $B handoff T-207 --agent architect --text \"What changed: LLM_VS_CODE row 2 (code-only allow-list: DOS/service column header, service label, the row's own date cell, the bill's one stated period; statement-date disambiguation 'a service cannot follow its statement'; unreadable years/dates not read; entry dates stay strict) and row 3 (charge-line exception: fillable blank + Step 3 confirm note when not certain, as-written form, 'service date not stated' form; validation cell names test_t202_r3_allow_list and letter_check.charge_date_violations). Verified: git diff shows only those 2 rows; commit 901ad5a via temp index, secrets check ok. Left: nothing in docs. Surprised me: the D-071 addendum's fillable blank ('date of service [__________] (statement dated X)') is not in the code at 5703fc4 (store.charge_service_date/service_date.printed_text print the 'as written' and 'service date not stated' forms; no card covers the blank), so the doc states the decided rule ahead of the code; backend needs a card.\"; $B move T-207 in_review --agent architect"
}
````

### User / tool · 2026-11-03T00:47:32.752Z

**tool result**
````
AC 1 checked: docs/LLM_VS_CODE.md rows 2 and 3, commit 901ad5a; text per T-202 note + D-071 amendment/clarification/addendum
T-207: commit 901ad5a recorded
handoff written on T-207
T-207: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:47:34.323Z

T-207 is in review (commit 901ad5a, only `docs/LLM_VS_CODE.md`, rows 2 and 3 updated), but the fillable blank the rows describe isn't in the code yet. Code at 5703fc4 prints the "as written" and "service date not stated" forms, and no board card covers the D-071 addendum's "date of service [__________]" blank, so backend needs a card for it.
