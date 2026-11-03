# Determinism diagnosis (T-075, R-CO-7)

**Status: cause of the 0.0 unconfirmed; the changes below are mitigations.** The 0.0 did not reproduce: the code before the changes was already 1.0 in 12 of 12 live runs (sets A and B), so the 1.0 after the changes is not evidence that they fixed it. They remove the flaky spots found by reading the per-item diffs (a judge that answered at random, a judge with no rule, order-dependent ids, retries without a pause). Whether any of them caused the 0.0 is unknown.

Trigger: `evals/reports/20261102T025219Z.md` (claude-cli, sample, 3 runs) gave `determinism_3run` 0.0; runs 2 and 3 differed from run 1 in entries, amounts and flags.

## 1. What was measured

Live runs of `evals/golden/sample.txt` through `pipeline.run_case` (`LLM_BACKEND=claude-cli ENABLE_LIVE=1`; generator claude-sonnet-5-5, judge claude-haiku-5-5), per item: state, record ids, excerpt, reason codes, judge verdict and reason code. Same code and prompts as the failing report except the three commits listed under "Cause of the 0.0".

| Set | Runs | Code/prompts | Signature (`evals.run.signature`) |
|---|---|---|---|
| A. before the changes | 9 parallel runs (3 compared in detail, then 9) | judge_flag_v1, judge_conflict_v1 | identical in all 9 |
| B. full eval, before the changes | `--runs 3` | same | determinism_3run 1.0 (report kept in the session scratch dir) |
| C. after the changes | 6 parallel runs | judge_flag_v2, judge_conflict_v2 | identical in all 6 |
| D. full eval, after the changes | `--runs 3` | same | `evals/reports/20261102T032823Z.md`: determinism_3run 1.0 |

So the 0.0 does **not** reproduce on demand: 12 live runs before the changes agreed on every state. If the 0.0 was real it is intermittent.

## 2. Per-item diffs found before the changes (9 runs)

Fields compared: state, record ids, excerpt (entries: the quote; flags: the evidence span), reason codes, judge verdict/reason code, summary text.

| Item | state | record ids | excerpt | Differs between runs | Cause class |
|---|---|---|---|---|---|
| e1, e3, e4, e6, e8 (entries) | verified in 9/9 | same | same in 9/9 | summary wording only ("41M" vs "41-year-old male"; ";" vs "and"; verbatim quote vs paraphrase) | extract variance in the summary. Allowed by R-CO-7 ("Summary wording may differ but must be supported"); J1 said `supported` 9/9 |
| a1..a4 (amounts) | same 9/9 | same | same | nothing | none |
| flag causation/accident_date_provenance (r7) | needs_review 9/9 | same | same | J4 reason_code `NOT_SUPPORTED_BY_QUOTE` vs `WRONG_CATEGORY` | judge flip in the reason code (verdict `disagree` 9/9) |
| flag causation/new_onset (r7) | needs_review 9/9 | same | same | J4 reason_code `NOT_SUPPORTED_BY_QUOTE` vs `WRONG_TYPE` | judge flip in the reason code |
| flag causation/patient_report (r9) | needs_review 9/9 | same | same | J4 reason_code `WRONG_TYPE` vs `NOT_SUPPORTED_BY_QUOTE` | judge flip in the reason code |
| flag pre_existing/degenerative_language (r8) | needs_review 9/9 | same | same | none | J4 disagreed 9/9 (see below) |
| flag conflict/treatment_plan_vs_actual (r4, r6) | needs_review 9/9 | same | same | J3 verdict `unsure` (2/9) vs `benign` (7/9); reason `JUDGE_UNSURE` vs `JUDGE_DISAGREES` | judge flip on a borderline case (verdict changed, state did not) |
| conflicts call | n/a | n/a | n/a | one run needed a retry of the conflicts call (call failed on attempt 1) | transient backend failure, recovered |
| ids (`e{n}`, `f_r{n}_{k}`, `f_cx1`) | | | | identical in 9/9 | none observed; ordering risk below |

No diff in record split, parsed dates, entry-id set, gap flag, amounts, classes or totals. No entry excerpt differed (the model picked the same whole sentences each time).

## 3. Findings behind the numbers

1. **J4 (flag judge) was wrong, and wrong at random.** Its prompt defined `causation` as wording that "weakens or questions" causation. Four of the seven judged flags on the sample (new_onset, patient_report, accident_date_provenance, degenerative_language) are valid flags that do not weaken causation, so Haiku answered `disagree` every time and picked a different reason code at random. States happened to agree in the 9 runs only because the answer was stably "disagree"; any case where Haiku leaned the other way flips `verified`/`needs_review` for four flags at once.
2. **J3 (conflict judge) had no decision rule** for the sample's one LLM conflict ("Plan of care: 12 visits." vs "Discharged from PT after two missed appointments."). It split `unsure`/`benign` 2:7. A draw of `conflict` would flip the state to `verified`.
3. **Order-dependent identifiers.** Model flags were appended in the order the model returned them, so `f_r{n}_{k}` ids and the lexicon/model pairing followed model order; the conflict pass returned model order and duplicates (`f_cx{i}` ids are the judge nonce and fixture key). Not seen in the 9 runs, but any record with two model-only flags or two conflicts would change ids and could change the flag set.
4. **Retries without a pause.** `make_call` passed no `sleep`, so a failed claude-cli call was retried immediately, twice, into the same rate limit or load.

## 4. Cause of the 0.0 in 20261102T025219Z (inference, not observed)

That report was written at 20:52 local, while other agents were running claude-cli and editing the lexicon/credibility code (commits f6fa2dd at 20:55, b05a8f3, 8634bfe followed). Entries, amounts and flags differed together. All three item kinds depend on a Haiku judge (J1, J2, J4/J3) and on the Sonnet generator, so the single mechanism that moves all three is a judge or generator call that failed on all three attempts (`LLM_FAILED_AFTER_RETRIES` / `JUDGE_UNAVAILABLE` turns `verified` into `needs_review` or removes an entry), immediately retried with no pause. Every live run in this diagnosis logged one or two failed first attempts (`llm call failed ... attempt=1`), so a run where the same call failed three times in a row under load is expected to occur occasionally. The per-run data of that report was not kept, so this cannot be confirmed; the eval runner writes only the aggregate.

## 5. Changes made (mitigations of the flaky spots found; nothing is cached; every run calls the model)

| Flaky spot | Change | Where |
|---|---|---|
| J4 judges the wrong question | `judge_flag_v2`: a flag is a pointer, not a causation claim; ordered decision rules (negation, type, one rule per category, then wrong category), `unsure` only for an unreadable quote | `app/llm/prompts/judge_flag_v2.md`, `judges.py`, `flags.py`, `audited.py` |
| J3 has no rule | `judge_conflict_v2`: takes the flag category as input; plan versus outcome that differ is a `conflict` whatever the reason; same `unsure` rule | `app/llm/prompts/judge_conflict_v2.md`, `judges.run_j3_meta(category=)`, `flags.judge_flags` |
| model order decides ids and pairing | model flags sorted by position, type, category, text before pairing and numbering; conflicts deduplicated (category + unordered quote pair) and sorted | `flags.merge`, `flags.run_conflict_pass` |
| retries into the same failure | live backends sleep `RETRY_DELAYS_S` between attempts (the fixture backend never sleeps); attempt count unchanged (R-CO-9) | `audited.make_call` |

Not changed, on purpose: IDs stay record-number based (a record's number is set by the code splitter and is stable; content-hash ids would invalidate every judge nonce and fixture for no observed gain). Entry excerpt snapping was not added: R-TL-2 specifies that a non-whole-sentence excerpt goes to `needs_review`, and no excerpt varied in 18 live runs. R-CO-7's definition is untouched, and a transient total outage of a call still shows as a difference.

## 6. Result after the changes

Set C (6 runs): every flag's state identical, J4 `agree/NONE` 6/6 on all seven judged flags, J3 `conflict/PLAN_VS_ACTUAL` 6/6, entries/amounts unchanged. The four flags J4 used to reject (new_onset, patient_report, accident_date_provenance, degenerative_language) and the plan-vs-actual conflict are now `verified`; before they were `needs_review` through a wrong judge. Set D: `evals/reports/20261102T032823Z.md` determinism_3run 1.0, unsupported_count_3run 0, hallucination_catch_rate 1.000 (40/40), ship_bar_met True.

What this result does and does not show: D agrees with B (both 1.0), so it cannot tell changed code from unchanged code. It shows the changes did not break determinism and that the judge verdicts are now stable and correct on the seeded cases (set C). The only evidence that bears on the original 0.0 would be a recurrence with per-run data kept; that recorder is T-093 (qa), and the live case_02 variance is T-094.
