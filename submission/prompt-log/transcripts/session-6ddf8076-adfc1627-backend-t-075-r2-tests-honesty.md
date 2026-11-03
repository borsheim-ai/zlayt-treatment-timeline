# Subagent: Backend: T-075 r2 tests + honesty (Backend: T-075 r2 tests + honesty)

Source: `agent-adfc1627366e7b07c.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:43:36.188Z

You own board card T-075, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-075-staff-engineer.md. The eval signature and per-run artifacts majors went to qa as T-093, and the live case_02 flap is T-094. Yours:
1. Rewrite `test_model_flag_order_does_not_change_the_flag_list` (tests/unit/test_t075_determinism.py) so it fails when the model-flag sort is removed: use 3 or more model-only flags in shuffled orders. Prove it with a scratch-copy mutation.
2. Add a test that fails if judges.py uses a judge prompt version other than the one the audit record says. Reverting J4 to v1 must turn it red.
3. Correct the card's claim. The pre-fix baseline was already 1.0 in 12 of 12 runs, so present the fixes as removing the flaky spots found, not as the cause of 1.0. Update evals/reports/determinism-diagnosis.md wording too (backend may edit that file for this card).

Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-075 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T03:43:36.193Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:38.334Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-075 | head -60; cat reviews/T-075-staff-engineer.md | head -80; cat tests/unit/test_t075_determinism.py; cat evals/reports/determinism-diagnosis.md"
}
````

### User / tool · 2026-11-02T03:43:38.483Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:40.250Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-075-staff-engineer.md | head -120; echo ======; cat tests/unit/test_t075_determinism.py; echo =====; cat evals/reports/determinism-diagnosis.md"
}
````

### User / tool · 2026-11-02T03:43:40.339Z

**tool result**
````
# T-075 review: staff-engineer-reviewer (commit 3104213, HEAD at review time)

Verdict: **changes**. No blocker, four majors, three minors.

The R-CO-7 definition in `evals/run.py` was **not weakened by this commit**: `evals/run.py` is not in `git show --stat 3104213`, and `git log -L383,404:evals/run.py` shows the function last changed in c8c7ba6 (T-038 r1). The commit does not cache anything. Every `run_case` builds a fresh `tempfile.TemporaryDirectory` database, `claude-cli` runs with `--no-session-persistence` and a timeout, and the fixture backend is only used when `ENABLE_LIVE` is unset.

My own live re-run (`LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --runs 3 --out <scratch>`) gave determinism 1.0, unsupported 0 and hallucination catch 40/40, as claimed. It also gave `ship_bar_met False` (golden_must_not_hits 1, entry_recall 0.965), which is finding 4.

What stays open:
- **Per-run artifacts are not kept.** The 0.0 is still undiagnosable if it recurs (finding 1).
- **The determinism metric is narrower than the R-CO-7 text.** Mutations to flag record ids, record split and totals all go undetected (finding 2).
- **Two of the new tests do not kill the mutants they claim to cover** (findings 3 and 6).
- **The fix is not evidenced by the report.** The pre-fix baseline was also 1.0 in 12 of 12 runs, so the green report cannot discriminate fixed from unfixed (finding 7).

```json
{
  "card": "T-075",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit 3104213 (app/backend/flags.py, judges.py, app/llm/audited.py, judge_flag_v2.md, judge_conflict_v2.md, tests/unit/test_t075_determinism.py, evals/reports/determinism-diagnosis.md, evals/reports/20261102T032823Z.md); evals/run.py signature/live_metrics; sample case (live claude-cli); no app URL",
  "exercised": [
    "python3 tools/board.py show T-075; git log/show --stat 3104213; git log -L383,404:evals/run.py (signature unchanged since c8c7ba6)",
    "read R-CO-7 and R-CO-3 in spec/REQUIREMENTS.md, evals/reports/determinism-diagnosis.md, evals/reports/20261102T032823Z.md, full code diff of app/ and tests/ in 3104213",
    ".venv/bin/python -m pytest tests/unit -q -> 1031 passed",
    "scratch script /private/tmp/claude-501/scratch-t075/sigtest.py: 17 mutations of one fixture run_case output, each run through evals.run.signature; MISSED: flag evidence record_id, flag record_nos/record_ids, totals (detected_pending_cents), record split (drop record, alter record text), flag reasons, entry id rename; DETECTED: flag state, flag excerpt, dropped flag, amount cents/kind/state, entry state/date/record_ids. totals has no key 'detected_not_a_total' (keys: accepted_cents, detected_pending_cents, detected_label, unclear_items, amounts_found, status, letter_line, ui_line)",
    "mutation spot-checks on git archive 3104213 in /private/tmp/claude-501/scratch-t075/repo (tests/unit/test_t075_determinism.py only): remove model-flag sort -> 4 passed (survives); remove conflict dedupe -> 1 failed; remove conflict sort -> 1 failed; make_call sleep always None -> 1 failed; always on -> 1 failed; J3 category line removed -> 1 failed; judges.run_j4_meta back to judge_flag_v1 -> 4 passed (survives). Control: with record 8 and two model-only flags (missed_care 'C5-C6 disc protrusion...', patient_report 'Charge: $2,150.') in swapped order, outputs are equal with the sort and differ without it",
    "live probe of v2 judges (claude-cli, 2 reps each, scratch probe.py): J4 on 8 seeded cases (negated, wrong category, wrong type, not-in-quote, 2 true flags) and J3 on 4 seeded pairs: 24/24 verdicts correct and stable across reps",
    "live eval re-run: LLM_BACKEND=claude-cli ENABLE_LIVE=1 .venv/bin/python -m evals.run --runs 3 --out /private/tmp/claude-501/scratch-t075/out -> report 20261102T034136Z.md: determinism_3run 1.0, unsupported_count_3run 0, hallucination 40/40, ship_bar_met False (blocker 4_no_invented_facts: golden_must_not_hits 1 on case_02, unsupported_summaries 1; entry_recall 0.965). ANTHROPIC_API_KEY not set or exported",
    "grep of changed lines for except/float(/sleep( (none added); read app/llm/provider.py, audited.py (RETRY_DELAYS_S 0.5/1.5, 3 attempts), claude_cli.py flags; grep for logging config in evals/run.py (none)"
  ],
  "verdict": "changes",
  "scores": {
    "r_co_7_definition_preserved": 4,
    "determinism_metric_sensitivity": 2,
    "diagnosability_of_future_failure": 1,
    "no_cross_run_caching": 5,
    "judge_prompt_discrimination": 4,
    "test_strength": 3,
    "evidence_honesty": 4
  },
  "findings": [
    {
      "severity": "major",
      "title": "Per-run determinism data is still discarded, so a recurrence of 0.0 is as undiagnosable as the first",
      "evidence": "evals/run.py:399-403: `sigs = [signature(o) for o in outs]` is a local; only {value, runs, status, r_ids} is returned. `python3 -c` on evals/reports/latest.json shows determinism_3run = {'r_ids': ['R-CO-7'], 'runs': 3, 'status': 'measured', 'value': 1.0} with no signatures. `git show --stat 3104213` does not touch evals/run.py. evals/run.py has no logging config, so 'llm call failed ... attempt=1' only goes to stderr. determinism-diagnosis.md section 4 says 'The per-run data of that report was not kept ... the eval runner writes only the aggregate' and the handoff says 'if it recurs, the eval should persist per-run signatures (qa)', so the known gap was deferred. The diagnosis section 1 set B report 'kept in the session scratch dir' is also not in the repo.",
      "why_it_matters": "The original 0.0 had a cause that is only inferred ('likely calls failing all retries under load'). The one change that would make the next 0.0 diagnosable was left undone. The card is the M2 gate blocker, and a recurrence at the gate leaves the team where it started.",
      "fix": "In live_metrics keep the per-run signatures (or the full per-run outputs minus text bodies) and write them next to the report (for example evals/reports/<ts>.runs.json). When determinism < 1.0, list the differing items (key, run, field) in the .md report. Configure logging in the CLI so failed-attempt warnings and the final call error codes per run land in that file.",
      "acceptance_test": "Unit test: live_metrics with Perfect(mutate=drop_in_run_2) returns/writes per-run signatures and the report names the dropped flag's (type, category, excerpt) and run number. Live: python -m evals.run --runs 3 leaves a runs file with 3 signatures."
    },
    {
      "severity": "major",
      "title": "The determinism signature is narrower than R-CO-7's text: flag record ids, record split and totals are not compared, and the totals term reads a key that does not exist",
      "evidence": "evals/run.py:383-390. R-CO-7: 'Flags are compared by (type, set of cited record IDs, evidence excerpt)'; code outputs identical include 'record split ... totals'. The signature's flag term is (type, category, excerpts, state) with no record ids. Its last term is `(out.get('totals') or {}).get('detected_not_a_total')`, but run_case totals has no such key, so the term is always None. Mutation results from sigtest.py: changing flag evidence record_id -> MISSED; flag record_ids -> MISSED; totals.detected_pending_cents -> MISSED; dropping a record -> MISSED; altering record 1 text -> MISSED; entry-id rename -> MISSED. (Amount cents/kind/state, flag state/excerpt/drop, entry date/state/record_ids are DETECTED.) Not introduced by 3104213; unchanged since c8c7ba6.",
      "why_it_matters": "The card AC is 'determinism_3run 1.0 without weakening R-CO-7's definition'. The definition was not changed by this commit, but the metric that gates M2 cannot see a flag that cites different records with the same quote, or a changed total. The 1.0 is weaker evidence than the report implies.",
      "fix": "Add the flag record_ids (sorted) to the flag term, the full `totals` dict (sorted keys) instead of the dead key, and the record list (n, excerpt hash) and entry id set to the signature. Keep the summary text out. Do not drop `category`.",
      "acceptance_test": "Parametrised unit test over signature(): each of the mutations above (flag record_ids, totals.detected_pending_cents, record excerpt, record count, entry ids) changes the signature; an entry summary rewrite does not."
    },
    {
      "severity": "major",
      "title": "test_model_flag_order_does_not_change_the_flag_list passes with the sort removed",
      "evidence": "tests/unit/test_t075_determinism.py:27-38. Mutation in the git-archive scratch copy: replace `uniq.sort(key=...)` in app/backend/flags.py:125 with a no-op -> `pytest tests/unit/test_t075_determinism.py -q` -> '4 passed'. Cause: of inputs a, b, c only c (missed_care) is model-only; a and b pair with lexicon flags (origin 'both'), so order is invisible. Control showing the sort matters: two model-only flags (missed_care on 'C5-C6 disc protrusion with mild right foraminal narrowing.', patient_report on 'Charge: $2,150.') in swapped order give equal output with the sort and [..., 'missed_care', 'patient_report'] vs [..., 'patient_report', 'missed_care'] without it.",
      "why_it_matters": "The docstring says 'Two model-only flags returned in either order give the same flags'. That is false for the test's inputs. The model-flag sort is the fix for 'order-dependent f_r{n}_{k} ids', and nothing proves it. The conflict-pass sort and dedupe are covered (their mutants fail), so the asymmetry is easy to miss.",
      "fix": "Add the two-model-only-flags case above (swapped orders, include a duplicate), and a second case where two model flags overlap the same lexicon flag so the pairing is order-sensitive. Fix the docstring.",
      "acceptance_test": "Removing `uniq.sort` in flags.merge makes the new test fail."
    },
    {
      "severity": "major",
      "title": "A fresh live run does not meet the ship bar: golden_must_not_hits 1 on case_02 and entry_recall 0.965 (non-sample, not caused by this diff as far as I can tell)",
      "evidence": "evals/reports run in scratch: /private/tmp/claude-501/scratch-t075/out/20261102T034136Z.md: 'ship_bar_met: False', 'Blockers: 4_no_invented_facts', 'golden_must_not_hits | 1 | 0', 'must_not detail: {case_02_gap_boundaries: {... unsupported_summaries: 1}}', 'entry_recall 0.965'. The committed report 20261102T032823Z.md has the same metrics at 0 hits and 0.982. Same command, same HEAD. J1 prompt (judge_faithfulness_v1), extract_v1 and the fixtures for them are untouched by 3104213, so this is generator or J1 variance on case_02.",
      "why_it_matters": "T-075 is the M2 gate blocker. The handoff cites one green report as proof of a stable gate. Two live runs of the same eval gave different ship_bar_met. R-CO-3 treats any must_not hit as a blocker, and R-CO-7 is only gated on the sample, so the case_02 variance is outside the AC, but the gate still needs it triaged.",
      "fix": "Open a card (qa/backend) for the case_02 unsupported summary: find which entry, its J1 verdict and whether the product marked it rejected; decide if the bar counts a caught-and-rejected summary. Until then, do not describe the gate as stable on one report.",
      "acceptance_test": "Three consecutive full live evals (`--runs 3`) each report ship_bar_met True, or the bar definition for caught-and-rejected summaries is changed by decision record."
    },
    {
      "severity": "minor",
      "title": "Reverting J4 to judge_flag_v1 in judges.py passes every T-075 test, and the audit record would still say v2",
      "evidence": "Mutation: app/backend/judges.py run_j4_meta `\"judge_flag_v2\", schemas.Judge4` -> `\"judge_flag_v1\"` -> '4 passed'. flags.py:judge_flags hard-codes `pv = \"judge_flag_v2\"` separately from the prompt that judges.py loads, and test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2 asserts only the ladder's pv string, PROMPT_OF_STEP, and the J3 category text.",
      "why_it_matters": "Two places name the same prompt. Drift gives an audit trail that lies about which prompt judged an item (checklist item 9).",
      "fix": "Have run_j4_meta/run_j3_meta return or expose the prompt version they used and have flags.py read it. Add a test that the J4 call's system text equals promptlib.load('judge_flag_v2').text.",
      "acceptance_test": "The v1 revert above fails a test."
    },
    {
      "severity": "minor",
      "title": "No committed negative control for the v2 flag and conflict judges; hallucination 40/40 does not measure them",
      "evidence": "evals/run.py:551: hallucination_catch_rate is computed with `pipeline.judge_summary` -> judges.run_j1 (judge_faithfulness_v1, unchanged by 3104213). `grep -rln 'run_j4\\|judge_flag' evals tests/unit` finds only report files and no seeded wrong-flag cases. My own live probe of 8 J4 and 4 J3 seeded cases (2 reps) gave 24/24 correct, so I have no evidence of a regression, but the repo has none either.",
      "why_it_matters": "v1 over-rejected, which is safe. v2 now says 'agree' for four flag categories that were 'disagree' on every run, so the failure that matters (agree on a wrong flag) has no test or eval. The brief's check 'the v2 prompts do not lower hallucination catch' is satisfied only trivially.",
      "fix": "Add a small seeded set (wrong category, negated, wrong type, quote not containing the named wording; plain pairs for J3) with an expected verdict, and report catch rate and false-agree count in the eval report for J3/J4.",
      "acceptance_test": "evals.run reports flag_judge_catch_rate on a live backend; a prompt that returns 'agree' for everything makes it fail."
    },
    {
      "severity": "minor",
      "title": "Handoff/AC wording presents the fix as the cause of the 1.0, but the baseline was already 1.0 in 12 of 12 runs",
      "evidence": "determinism-diagnosis.md sections 1 and 4: 'the 0.0 does not reproduce on demand: 12 live runs before the fix agreed on every state' and 'a judge or generator call that failed on all three attempts ... inference, not observed'. Card AC 2 is checked 'done' on one green report. The retry pause (RETRY_DELAYS_S = (0.5, 1.5), app/llm/audited.py:17) is tested only as `callable(seen[1])`.",
      "why_it_matters": "Honest in the diagnosis, but the board shows AC 2/2 done. A reader of the card will assume the 0.0 is fixed. Nothing shows a 0.5 s and 1.5 s pause survives the load that is thought to have caused it. I label this a wording and evidence issue, not a defect in the code.",
      "fix": "Mark the card note 'cause unconfirmed, fix is mitigation' and carry it into the M2 gate summary. Optionally test the delay values against RETRY_DELAYS_S.",
      "acceptance_test": "Card note and gate summary state the cause is unconfirmed; a test asserts the sleeps are called with (0.5, 1.5) on a live backend and never on fixture."
    }
  ],
  "whats_right": [
    "Conflict-pass ordering and dedupe, J3 category line and the live/fixture retry pause each have a test whose removal fails it, and no new bare except, float or sleep was added.",
    "The v2 judge prompts discriminate: 24/24 seeded live verdicts correct and stable across two repetitions, and the diagnosis candidly says the 0.0 cause is an inference.",
    "No cross-run state: fresh scratch database per run_case, --no-session-persistence, timeout on every claude-cli call; the signature definition itself was left untouched."
  ],
  "questions_for_chris": [
    "Should the ship bar count a summary that J1 judged unsupported and the pipeline rejected (case_02) as a golden_must_not hit, given nothing unsupported reaches the export?"
  ]
}
```
======
"""T-075 (R-CO-7): the order, wording or duplication of what a model returns must not change the flag set, the flag ids or the judge prompts.
Fake model only; the live 3-run check is evals/run.py."""
from app.backend import flags as F, judges as J
from app.llm import audited as AU, promptlib, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall

EX = G.expected("sample")
HEDGE = "Findings may represent degenerative change; correlate clinically."
PLAN, OUT = "Plan of care: 12 visits.", "Discharged from PT after two missed appointments."


def rec(n):
    r = G.record("sample", n)
    return dict(n=n, source=r["source"], excerpt=r["excerpt"], date_iso=EX["records"][n - 1]["date"])


def _ident(fl):
    return [(f["type"], f["category"], f["excerpt"], f["origin"], f["state"], tuple(f["reasons"])) for f in fl]


def test_model_flag_order_does_not_change_the_flag_list():
    """Two model-only flags returned in either order give the same flags in the same order (ids f_r{n}_{k} follow this order)."""
    a = dict(type="causation", category="speculative_language", excerpt=HEDGE)
    b = dict(type="pre_existing", category="degenerative_language", excerpt="Findings may represent degenerative change")
    c = dict(type="causation", category="missed_care", excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")
    r8 = rec(8)
    one = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [a, b, c]}}))
    two = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [c, b, a, dict(a)]}}))
    assert _ident(one) == _ident(two)


def test_conflict_order_and_duplicates_do_not_change_the_conflict_list():
    recs = [rec(n) for n in range(1, 10)]
    f1 = dict(type="conflict", category="treatment_plan_vs_actual", excerpt=PLAN, excerpt_b=OUT)
    f2 = dict(type="conflict", category="treatment_plan_vs_actual", excerpt=OUT, excerpt_b=PLAN)     # same pair, swapped
    f3 = dict(type="conflict", category="other_fact_mismatch", excerpt="Pain 4/10, improving.", excerpt_b="Pain 3/10.")
    one = F.run_conflict_pass(recs, call=FakeCall({"conflicts": {"flags": [f1, f3]}}))
    two = F.run_conflict_pass(recs, call=FakeCall({"conflicts": {"flags": [f3, f2, f1, dict(f1)]}}))
    assert [(f["category"], f["record_nos"]) for f in one] == [(f["category"], f["record_nos"]) for f in two]
    assert len(two) == 2


def test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2():
    c = FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}, "j4": {"verdict": "agree", "reason_code": "NONE"}})
    fl = F.run_conflict_pass([rec(n) for n in range(1, 10)], call=FakeCall({"conflicts": {"flags": [
        dict(type="conflict", category="treatment_plan_vs_actual", excerpt=PLAN, excerpt_b=OUT)]}}))
    F.judge_flags(fl, call=c)
    assert "FLAG CATEGORY: treatment_plan_vs_actual" in c.prompts("j3")[0]
    assert fl[0]["ladder"]["judge"]["prompt_version"] == "judge_conflict_v2"
    assert AU.PROMPT_OF_STEP["j3"] == "judge_conflict_v2" and AU.PROMPT_OF_STEP["j4"] == "judge_flag_v2"
    assert "decision rules" in promptlib.load("judge_conflict_v2").text.lower() and "unsure" in promptlib.load("judge_flag_v2").text


def test_live_backend_retries_pause_but_fixture_does_not(monkeypatch):
    """T-075: a live backend that just failed is retried after a pause, not at once; the fixture backend never sleeps."""
    seen = []
    monkeypatch.setattr(AU, "audited_call", lambda *a, **k: seen.append(k.get("sleep")) or ({}, "c1"))
    call = AU.make_call(None, "case")
    monkeypatch.setattr(P, "backend_name", lambda: "fixture")
    call("j4", "s", "u", {})
    monkeypatch.setattr(P, "backend_name", lambda: "claude-cli")
    call("j4", "s", "u", {})
    assert seen[0] is None and callable(seen[1])
=====
# Determinism diagnosis (T-075, R-CO-7)

Trigger: `evals/reports/20261102T025219Z.md` (claude-cli, sample, 3 runs) gave `determinism_3run` 0.0; runs 2 and 3 differed from run 1 in entries, amounts and flags.

## 1. What was measured

Live runs of `evals/golden/sample.txt` through `pipeline.run_case` (`LLM_BACKEND=claude-cli ENABLE_LIVE=1`; generator claude-sonnet-5-5, judge claude-haiku-5-5), per item: state, record ids, excerpt, reason codes, judge verdict and reason code. Same code and prompts as the failing report except the three commits listed under "Cause of the 0.0".

| Set | Runs | Code/prompts | Signature (`evals.run.signature`) |
|---|---|---|---|
| A. before the fix | 9 parallel runs (3 compared in detail, then 9) | judge_flag_v1, judge_conflict_v1 | identical in all 9 |
| B. full eval, before the fix | `--runs 3` | same | determinism_3run 1.0 (report kept in the session scratch dir) |
| C. after the fix | 6 parallel runs | judge_flag_v2, judge_conflict_v2 | identical in all 6 |
| D. full eval, after the fix | `--runs 3` | same | `evals/reports/20261102T032823Z.md`: determinism_3run 1.0 |

So the 0.0 does **not** reproduce on demand: 12 live runs before the fix agreed on every state. It is intermittent.

## 2. Per-item diffs found before the fix (9 runs)

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

## 5. Fixes (nothing is cached; every run calls the model)

| Cause | Fix | Where |
|---|---|---|
| J4 judges the wrong question | `judge_flag_v2`: a flag is a pointer, not a causation claim; ordered decision rules (negation, type, one rule per category, then wrong category), `unsure` only for an unreadable quote | `app/llm/prompts/judge_flag_v2.md`, `judges.py`, `flags.py`, `audited.py` |
| J3 has no rule | `judge_conflict_v2`: takes the flag category as input; plan versus outcome that differ is a `conflict` whatever the reason; same `unsure` rule | `app/llm/prompts/judge_conflict_v2.md`, `judges.run_j3_meta(category=)`, `flags.judge_flags` |
| model order decides ids and pairing | model flags sorted by position, type, category, text before pairing and numbering; conflicts deduplicated (category + unordered quote pair) and sorted | `flags.merge`, `flags.run_conflict_pass` |
| retries into the same failure | live backends sleep `RETRY_DELAYS_S` between attempts (the fixture backend never sleeps); attempt count unchanged (R-CO-9) | `audited.make_call` |

Not changed, on purpose: IDs stay record-number based (a record's number is set by the code splitter and is stable; content-hash ids would invalidate every judge nonce and fixture for no observed gain). Entry excerpt snapping was not added: R-TL-2 specifies that a non-whole-sentence excerpt goes to `needs_review`, and no excerpt varied in 18 live runs. R-CO-7's definition is untouched, and a transient total outage of a call still shows as a difference.

## 6. Result after the fix

Set C (6 runs): every flag's state identical, J4 `agree/NONE` 6/6 on all seven judged flags, J3 `conflict/PLAN_VS_ACTUAL` 6/6, entries/amounts unchanged. The four flags J4 used to reject (new_onset, patient_report, accident_date_provenance, degenerative_language) and the plan-vs-actual conflict are now `verified`; before they were `needs_review` through a wrong judge. Set D: `evals/reports/20261102T032823Z.md` determinism_3run 1.0, unsupported_count_3run 0, hallucination_catch_rate 1.000 (40/40), ship_bar_met True.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:42.001Z

**tool call — Bash**
````
{
 "command": "sed -n 95,150p app/backend/flags.py; grep -n \"judge_flag\\|judge_conflict\\|def run_j[34]\" app/backend/judges.py app/backend/flags.py app/llm/audited.py; grep -n \"prompt_version\\|pv\" app/backend/flags.py"
}
````

### User / tool · 2026-11-02T03:43:42.092Z

**tool result**
````
        if key in seen:
            seen[key]["lexicon_ids"].append(h["id"])
            continue
        f = _flag(record, h["flag_type"], h["category"], text[a:b], "lexicon", (a, b), False, "lexicon_only")
        f["lexicon_ids"] = [h["id"]]
        f["_span"] = (a, b)
        seen[key] = f
        out.append(f)
    return out


# ------------------------------------------------------------------ merge
def _overlap(a, b) -> bool:
    return bool(a and b and a[0] < b[1] and b[0] < a[1])


def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
    body, out, used = record["excerpt"], [], set()
    uniq, seen = [], set()
    for lf in llm_flags:
        if lf.get("category") in _CONTEXT_ONLY:
            continue
        k = (lf["type"], grounding.normalize(lf["excerpt"]))
        if k not in seen:
            seen.add(k)
            uniq.append(lf)
    # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
    # then type, category and text (code decides what code can decide).
    uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
    llm_spans = [grounding.locate(body, lf["excerpt"]) for lf in uniq]
    for lx in lex_flags:
        lx = dict(lx)
        lx["_stage"] = dict(lx["_stage"], injection=tagged)
        match = next((i for i, lf in enumerate(uniq) if i not in used and lf["type"] == lx["type"] and _overlap(llm_spans[i], lx.get("_span"))), None)
        if match is not None:
            used.add(match)
            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
            lx["ladder"] = dict(lx["ladder"], judge=None)
            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
            # only the fallback quote for phrase-list-only flags
            lx["excerpt"] = uniq[match]["excerpt"]
            sp = llm_spans[match]
            base = _base(record)
            lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
                               "start": base + sp[0] if sp else None, "end": base + sp[1] if sp else None}]
            lx["_span"] = sp or lx.get("_span")
            _render(lx, record)
        else:
            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
            lx["_stage"]["llm_failed"], lx["_stage"]["fixture_miss"] = llm_failed, fixture_miss
            if llm_failed or fixture_miss:
                lx["_stage"]["agreement"] = None
        out.append(_compose(lx))
    for i, lf in enumerate(uniq):
app/llm/audited.py:100:PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v2",
app/llm/audited.py:101:                  "j4": "judge_flag_v2", "conflicts": "conflicts_v1", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
app/backend/flags.py:279:def judge_flags(flags: list, *, call, case_text: str = "") -> list:
app/backend/flags.py:292:                step, pv = "j3", "judge_conflict_v2"
app/backend/flags.py:295:                step, pv = "j4", "judge_flag_v2"
app/backend/flags.py:300:            v, cid, reason, step, pv = "unavailable", None, "NONE", "j3" if f["type"] == "conflict" else "j4", "judge_conflict_v2" if f["type"] == "conflict" else "judge_flag_v2"
app/backend/judges.py:57:def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
app/backend/judges.py:58:    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v2 (T-075)."""
app/backend/judges.py:59:    return _run("j3", "judge_conflict_v2", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
app/backend/judges.py:63:def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
app/backend/judges.py:64:    return _run("j4", "judge_flag_v2", schemas.Judge4, [excerpt],
app/backend/judges.py:76:def run_j3(excerpt_a, excerpt_b, *, call, nonce=None, item_id=None, category=None):
app/backend/judges.py:80:def run_j4(excerpt, flag_type, category, *, call, nonce=None, item_id=None):
292:                step, pv = "j3", "judge_conflict_v2"
295:                step, pv = "j4", "judge_flag_v2"
300:            v, cid, reason, step, pv = "unavailable", None, "NONE", "j3" if f["type"] == "conflict" else "j4", "judge_conflict_v2" if f["type"] == "conflict" else "judge_flag_v2"
301:        f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:43.648Z

**tool call — Bash**
````
{
 "command": "sed -n 25,75p app/backend/judges.py; sed -n 275,305p app/backend/flags.py; sed -n 1,60p tests/unit/_fakes.py"
}
````

### User / tool · 2026-11-02T03:43:43.732Z

**tool result**
````
    """Returns (verdict, call_id, reason_code). verdict in the model's enum, or 'unavailable' / 'unsure'."""
    n = nonce or promptlib.nonce(step, *quotes, *[x if isinstance(x, str) else x[1] for x in lines])
    p = promptlib.load(prompt)
    blocks = "\n".join(f"{label}:\n{injection.wrap(q, n)}" for label, q in quotes_labelled(quotes, step))
    extra = "\n".join(f"{x[0]}:\n{injection.wrap(x[1], n)}" if isinstance(x, tuple) else x for x in lines)   # (name, text) = record-derived, wrapped
    user = blocks + "\n" + extra + "\nReturn the JSON object."
    try:
        out, call_id = call(step, p.text, user, model_cls.model_json_schema(), item_id=item_id)
    except AU.LLMFailed:
        return "unavailable", None, "NONE"
    try:
        m = model_cls.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        return "unavailable", call_id, "NONE"   # invalid judge output (bad enum, missing reason_code) = judge did not answer
    return m.verdict, call_id, m.reason_code


def quotes_labelled(quotes: list, step: str):
    names = {"j3": ["QUOTE A", "QUOTE B"]}.get(step, ["RECORD TEXT"] * len(quotes))
    return zip(names, quotes)


def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None):
    return _run("j1", "judge_faithfulness_v1", schemas.Judge1, [excerpt],
                [("SOURCE LABEL", label), f"CANDIDATE SUMMARY: {summary}"], call, nonce, item_id)


def run_j2_meta(excerpt: str, raw_amount: str, code_class: str, *, call, nonce=None, item_id=None):
    return _run("j2", "judge_amount_class_v1", schemas.Judge2, [excerpt],
                [f"AMOUNT: {raw_amount}", f"CLASS: {code_class}"], call, nonce, item_id)


def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v2 (T-075)."""
    return _run("j3", "judge_conflict_v2", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
                call, nonce, item_id)


def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
    return _run("j4", "judge_flag_v2", schemas.Judge4, [excerpt],
                [f"FLAG TYPE: {flag_type}", f"FLAG CATEGORY: {category}"], call, nonce, item_id)


def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]


def run_j2(excerpt, raw_amount, code_class, *, call, nonce=None, item_id=None):
    return run_j2_meta(excerpt, raw_amount, code_class, call=call, nonce=nonce, item_id=item_id)[0]


    return out


# ------------------------------------------------------------------ rung 2 for flags (J3 / J4)
def judge_flags(flags: list, *, call, case_text: str = "") -> list:
    """J4 on every model-involved pre_existing/causation flag; J3 on every model conflict. Lexicon-only flags have no judge.
    A disagreement, unsure answer or failed judge call leaves the flag needs_review (JUDGE_DISAGREES / JUDGE_UNSURE / JUDGE_UNAVAILABLE)."""
    for i, f in enumerate(flags):
        if f["type"] == "record_warning" or f["state"] == "rejected":
            continue
        item = f.get("id") or f"f{i}"
        nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
        try:
            if f["type"] == "conflict":
                if not f.get("excerpt_b"):
                    continue
                v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
                step, pv = "j3", "judge_conflict_v2"
            elif f["origin"] in ("llm", "both"):
                v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
                step, pv = "j4", "judge_flag_v2"
            else:
                continue
        except P.FixtureMiss:
            f["_stage"]["fixture_miss"] = True
            v, cid, reason, step, pv = "unavailable", None, "NONE", "j3" if f["type"] == "conflict" else "j4", "judge_conflict_v2" if f["type"] == "conflict" else "judge_flag_v2"
        f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
        f["_stage"]["judge"] = judges.to_ladder(step, v)
        _compose(f)
    return flags
"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]


def sample_script(**over):
    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
          "conflicts": {"flags": []}, "flags": {"flags": []}}
    sc.update(over)
    return sc

def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
    from app.backend import pipeline as PL
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:46.892Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nfrom tests.unit.test_t075_determinism import *\nr8=rec(8); print(r8[\"excerpt\"])\nfor r in [rec(n) for n in range(1,10)]:\n    print(r[\"n\"], len(r[\"excerpt\"]))\nprint([ (f['type'],f['category'],f['excerpt'],f['origin']) for f in F.run_flag_pass(r8, call=FakeCall({\"flags\":{\"flags\":[]}}))])\nE"
}
````

### User / tool · 2026-11-02T03:43:47.252Z

**tool result**
````
C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.
1 132
2 156
3 139
4 93
5 61
6 60
7 133
8 140
9 105
[('pre_existing', 'degenerative_language', 'Findings may represent degenerative change; correlate clinically.', 'lexicon'), ('causation', 'speculative_language', 'Findings may represent degenerative change; correlate clinically.', 'lexicon')]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:43:56.124Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport re\np=\"tests/unit/test_t075_determinism.py\"\ns=open(p).read()\na=s.index(\"def test_model_flag_order\")\nb=s.index(\"def test_conflict_order\")\nnew='''def test_model_flag_order_does_not_change_the_flag_list():\n    \"\"\"Three model-only flags (no lexicon flag shares their type and span) returned in every order, with a duplicate, give the same flags in\n    the same order (ids f_r{n}_{k} follow this order). Removing the model-flag sort in flags.merge makes this fail.\"\"\"\n    m1 = dict(type=\"causation\", category=\"missed_care\", excerpt=\"C5-C6 disc protrusion with mild right foraminal narrowing.\")\n    m2 = dict(type=\"causation\", category=\"new_onset\", excerpt=\"mild right foraminal narrowing\")\n    m3 = dict(type=\"causation\", category=\"patient_report\", excerpt=\"Charge: $2,150.\")\n    r8 = rec(8)\n    base = F.run_flag_pass(r8, call=FakeCall({\"flags\": {\"flags\": [m1, m2, m3]}}))\n    model_only = [f for f in base if f[\"origin\"] != \"lexicon\"]\n    assert len(model_only) == 3                      # the setup really has three model-only flags\n    for order in itertools.permutations([m1, m2, m3]):\n        got = F.run_flag_pass(r8, call=FakeCall({\"flags\": {\"flags\": [*order, dict(order[0])]}}))\n        assert _ident(got) == _ident(base), [x[\"category\"] for x in order]\n        assert [f[\"id\"] for f in got] == [f[\"id\"] for f in base]\n\n\n'''\ns=s[:a]+new+s[b:]\ns=s.replace(\"from app.backend import flags\",\"import itertools\\nfrom app.backend import flags\",1)\ns+='''\n\ndef test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names():\n    \"\"\"The prompt text a judge call carries must be the prompt the ladder's audit record says (J3 and J4). Reverting either judge in\n    judges.py to v1 while flags.py still records v2 makes this fail.\"\"\"\n    c = FakeCall({\"j3\": {\"verdict\": \"conflict\", \"reason_code\": \"PLAN_VS_ACTUAL\"}, \"j4\": {\"verdict\": \"agree\", \"reason_code\": \"NONE\"},\n                  \"conflicts\": {\"flags\": [dict(type=\"conflict\", category=\"treatment_plan_vs_actual\", excerpt=PLAN, excerpt_b=OUT)]},\n                  \"flags\": {\"flags\": [dict(type=\"causation\", category=\"missed_care\", excerpt=\"C5-C6 disc protrusion with mild right foraminal narrowing.\")]}})\n    fl = F.run_conflict_pass([rec(n) for n in range(1, 10)], call=c) + F.run_flag_pass(rec(8), call=c)\n    F.judge_flags(fl, call=c)\n    seen = {}\n    for f in fl:\n        j = f[\"ladder\"][\"judge\"]\n        if j and j[\"verdict\"] != \"unavailable\":\n            seen[f[\"type\"] == \"conflict\" and \"j3\" or \"j4\"] = j[\"prompt_version\"]\n    assert set(seen) == {\"j3\", \"j4\"}\n    for step, pv in seen.items():\n        sent = [l[\"system\"] for l in c.log if l[\"step\"] == step]\n        assert sent and all(s == promptlib.load(pv).text for s in sent), (step, pv)\n'''\nopen(p,\"w\").write(s)\nE\nsed -n 1,6p tests/unit/test_t075_determinism.py; .venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:43:56.774Z

**tool result**
````
"""T-075 (R-CO-7): the order, wording or duplication of what a model returns must not change the flag set, the flag ids or the judge prompts.
Fake model only; the live 3-run check is evals/run.py."""
import itertools
from app.backend import flags as F, judges as J
from app.llm import audited as AU, promptlib, provider as P
from tests.unit import _golden as G
        r8 = rec(8)
        base = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [m1, m2, m3]}}))
        model_only = [f for f in base if f["origin"] != "lexicon"]
        assert len(model_only) == 3                      # the setup really has three model-only flags
        for order in itertools.permutations([m1, m2, m3]):
            got = F.run_flag_pass(r8, call=FakeCall({"flags": {"flags": [*order, dict(order[0])]}}))
            assert _ident(got) == _ident(base), [x["category"] for x in order]
>           assert [f["id"] for f in got] == [f["id"] for f in base]
                    ^^^^^^^
E           KeyError: 'id'

tests/unit/test_t075_determinism.py:36: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_t075_determinism.py::test_model_flag_order_does_not_change_the_flag_list
1 failed, 4 passed in 0.25s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:01.891Z

**tool call — Bash**
````
{
 "command": "sed -i '/assert \\[f\\[\"id\"\\] for f in got\\]/d' tests/unit/test_t075_determinism.py && .venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -3\n# mutations on scratch copy\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut\nrm -rf $S; mkdir -p $S; cp -R app tests evals spec $S/ 2>/dev/null; ls $S; ls -d *.toml *.ini conftest.py 2>/dev/null\ncd $S\n# mutation 1: remove sort\npython3 - <<'E'\np=\"app/backend/flags.py\"; s=open(p).read()\ni=s.index(\"    uniq.sort(key=lambda lf\"); j=s.index(\"\\n\",i)\nopen(p,\"w\").write(s[:i]+\"    pass\"+s[j:])\nE\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T03:44:02.901Z

**tool result**
````
sed: 2: "tests/unit/test_t075_de ...": undefined label 'ests/unit/test_t075_determinism.py'
app
evals
spec
tests
tests/unit/test_t075_determinism.py:36: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_t075_determinism.py::test_model_flag_order_does_not_change_the_flag_list
1 failed, 4 passed in 0.26s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:03.900Z

BSD sed needs a different form; use python.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:09.254Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"tests/unit/test_t075_determinism.py\"\nL=[l for l in open(p).read().split(\"\\n\") if 'assert [f[\"id\"] for f in got]' not in l]\nopen(p,\"w\").write(\"\\n\".join(L))\nE\n.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -3\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut\nrm -rf $S; mkdir -p $S; cp -R app tests evals spec $S/\ncd $S\npython3 - <<'E'\np=\"app/backend/flags.py\"; s=open(p).read()\ni=s.index(\"    uniq.sort(key=lambda lf\"); j=s.index(\"\\n\",i)\nopen(p,\"w\").write(s[:i]+\"    pass\"+s[j:])\nE\necho \"--- mutation 1: no model-flag sort\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -3\ncp /Users/arsis/zlayt-pm-project/app/backend/flags.py app/backend/flags.py\nsed -i '' 's/\"judge_flag_v2\", schemas.Judge4/\"judge_flag_v1\", schemas.Judge4/' app/backend/judges.py\necho \"--- mutation 2: J4 v1\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -3\ncp /Users/arsis/zlayt-pm-project/app/backend/judges.py app/backend/judges.py\nsed -i '' 's/\"judge_conflict_v2\", schemas.Judge3/\"judge_conflict_v1\", schemas.Judge3/' app/backend/judges.py\necho \"--- mutation 3: J3 v1\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T03:44:11.852Z

**tool result**
````
.....                                                                    [100%]
5 passed in 0.23s
--- mutation 1: no model-flag sort
=========================== short test summary info ============================
FAILED tests/unit/test_t075_determinism.py::test_model_flag_order_does_not_change_the_flag_list
1 failed, 4 passed in 0.27s
--- mutation 2: J4 v1
=========================== short test summary info ============================
FAILED tests/unit/test_t075_determinism.py::test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names
1 failed, 4 passed in 0.26s
--- mutation 3: J3 v1
=========================== short test summary info ============================
FAILED tests/unit/test_t075_determinism.py::test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names
1 failed, 4 passed in 0.26s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:17.811Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"evals/reports/determinism-diagnosis.md\"; s=open(p).read()\ndef rep(a,b):\n    global s\n    assert a in s, a\n    s=s.replace(a,b,1)\nrep(\"# Determinism diagnosis (T-075, R-CO-7)\\n\",\"\"\"# Determinism diagnosis (T-075, R-CO-7)\n\n**Status: cause of the 0.0 unconfirmed; the changes below are mitigations.** The 0.0 did not reproduce: the code before the changes was already 1.0 in 12 of 12 live runs (sets A and B), so the 1.0 after the changes is not evidence that they fixed it. They remove the flaky spots found by reading the per-item diffs (a judge that answered at random, a judge with no rule, order-dependent ids, retries without a pause). Whether any of them caused the 0.0 is unknown.\n\"\"\")\nrep(\"## 5. Fixes (nothing is cached; every run calls the model)\",\"## 5. Changes made (mitigations of the flaky spots found; nothing is cached; every run calls the model)\")\nrep(\"## 6. Result after the fix\",\"## 6. Result after the changes\")\ns=s.rstrip(\"\\n\")+\"\"\"\n\nWhat this result does and does not show: D agrees with B (both 1.0), so it cannot tell changed code from unchanged code. It shows the changes did not break determinism and that the judge verdicts are now stable and correct on the seeded cases (set C). The only evidence that bears on the original 0.0 would be a recurrence with per-run data kept; that recorder is T-093 (qa), and the live case_02 variance is T-094.\n\"\"\"\nopen(p,\"w\").write(s)\nE\ngrep -n \"fix\\|Fix\" evals/reports/determinism-diagnosis.md | head -20"
}
````

### User / tool · 2026-11-02T03:44:17.920Z

**tool result**
````
3:**Status: cause of the 0.0 unconfirmed; the changes below are mitigations.** The 0.0 did not reproduce: the code before the changes was already 1.0 in 12 of 12 live runs (sets A and B), so the 1.0 after the changes is not evidence that they fixed it. They remove the flaky spots found by reading the per-item diffs (a judge that answered at random, a judge with no rule, order-dependent ids, retries without a pause). Whether any of them caused the 0.0 is unknown.
13:| A. before the fix | 9 parallel runs (3 compared in detail, then 9) | judge_flag_v1, judge_conflict_v1 | identical in all 9 |
14:| B. full eval, before the fix | `--runs 3` | same | determinism_3run 1.0 (report kept in the session scratch dir) |
15:| C. after the fix | 6 parallel runs | judge_flag_v2, judge_conflict_v2 | identical in all 6 |
16:| D. full eval, after the fix | `--runs 3` | same | `evals/reports/20261102T032823Z.md`: determinism_3run 1.0 |
18:So the 0.0 does **not** reproduce on demand: 12 live runs before the fix agreed on every state. It is intermittent.
20:## 2. Per-item diffs found before the fix (9 runs)
42:3. **Order-dependent identifiers.** Model flags were appended in the order the model returned them, so `f_r{n}_{k}` ids and the lexicon/model pairing followed model order; the conflict pass returned model order and duplicates (`f_cx{i}` ids are the judge nonce and fixture key). Not seen in the 9 runs, but any record with two model-only flags or two conflicts would change ids and could change the flag set.
51:| Cause | Fix | Where |
56:| retries into the same failure | live backends sleep `RETRY_DELAYS_S` between attempts (the fixture backend never sleeps); attempt count unchanged (R-CO-9) | `audited.make_call` |
58:Not changed, on purpose: IDs stay record-number based (a record's number is set by the code splitter and is stable; content-hash ids would invalidate every judge nonce and fixture for no observed gain). Entry excerpt snapping was not added: R-TL-2 specifies that a non-whole-sentence excerpt goes to `needs_review`, and no excerpt varied in 18 live runs. R-CO-7's definition is untouched, and a transient total outage of a call still shows as a difference.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:21.078Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"evals/reports/determinism-diagnosis.md\"; s=open(p).read()\nfor a,b in [(\"A. before the fix\",\"A. before the changes\"),(\"B. full eval, before the fix\",\"B. full eval, before the changes\"),(\"C. after the fix\",\"C. after the changes\"),(\"D. full eval, after the fix\",\"D. full eval, after the changes\"),\n (\"12 live runs before the fix agreed on every state. It is intermittent.\",\"12 live runs before the changes agreed on every state. If the 0.0 was real it is intermittent.\"),\n (\"found before the fix (9 runs)\",\"found before the changes (9 runs)\"),(\"| Cause | Fix | Where |\",\"| Flaky spot | Change | Where |\")]:\n    assert a in s; s=s.replace(a,b,1)\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3; git status --short | head"
}
````

### User / tool · 2026-11-02T03:44:46.117Z

**tool result**
````
........................................................................ [ 96%]
...................................                                      [100%]
1043 passed in 23.90s
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:52.481Z

**tool call — Bash**
````
{
 "command": "git add tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md && git commit -q -m \"test(backend): T-075 r2 strengthen sort and judge-prompt tests, reword diagnosis as mitigations\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md && SHA=$(git rev-parse --short HEAD) && echo $SHA\nB=\"python3 tools/board.py\"\n$B commit T-075 --sha $SHA --agent backend\n$B ac T-075 --check 2 --agent backend --evidence \"Corrected: pre-change baseline was already determinism 1.0 in 12/12 runs, so the changes are mitigations of flaky spots found, cause of the original 0.0 unconfirmed. Live 20261102T032823Z.md 1.0 / unsupported 0; per-run recorder is T-093, case_02 flap T-094\" \n$B note T-075 --agent backend --text \"r2: cause of the 0.0 UNCONFIRMED; changes are mitigations, not shown to be the fix (baseline 1.0 in 12/12). Tests: model-flag sort test now 3 model-only flags x all permutations + dup (fails with sort removed); new test that judge system prompt == promptlib.load(audit prompt_version) (fails with J3 or J4 reverted to v1); both proved by scratch-copy mutation. Diagnosis doc reworded.\"\n$B handoff T-075 --agent backend --text \"What changed: tests/unit/test_t075_determinism.py (sort test rewritten with 3 model-only flags, all orderings + dup; new audit-vs-sent judge prompt test), diagnosis doc reworded as mitigations, cause unconfirmed. How verified: scratch-copy mutations: no model-flag sort -> sort test red; J4 or J3 reverted to v1 -> prompt test red; pytest tests/unit 1043 passed. What's left: eval signature narrowness and per-run artifacts = T-093 (qa); case_02 live flap = T-094. Surprise: flag dicts have no id at run_flag_pass stage; list order is the observable.\"\n$B move T-075 in_review --agent backend"
}
````

### User / tool · 2026-11-02T03:44:52.566Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git add tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md && git commit -q -m "test(backend): T-075 r2 strengthen sort and judge-prompt tests, reword diagnosis as mitigations

````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:53.994Z

**tool call — Bash**
````
{
 "command": "git add tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md"
}
````

### User / tool · 2026-11-02T03:44:54.092Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:54.519Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"test(backend): T-075 r2 strengthen sort and judge-prompt tests, reword diagnosis as mitigations\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T03:44:54.822Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
b5b9b34
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:44:58.640Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; SHA=b5b9b34\n$B commit T-075 --sha $SHA --agent backend\n$B ac T-075 --check 2 --agent backend --evidence \"Corrected: pre-change baseline was already determinism 1.0 in 12/12 runs, so the changes are mitigations of flaky spots found; cause of the original 0.0 unconfirmed. Live 20261102T032823Z.md 1.0 / unsupported 0; per-run recorder is T-093, case_02 flap T-094\"\n$B note T-075 --agent backend --text \"r2: cause of the 0.0 UNCONFIRMED; changes are mitigations, not shown to be the fix (baseline 1.0 in 12/12). Sort test now uses 3 model-only flags x all permutations + dup (red with sort removed); new test: judge system prompt == promptlib.load(audit prompt_version) (red with J3 or J4 reverted to v1); both proved by scratch-copy mutation. Diagnosis doc reworded.\"\n$B handoff T-075 --agent backend --text \"What changed: tests/unit/test_t075_determinism.py (sort test rewritten; new audit-vs-sent judge prompt test), diagnosis doc reworded as mitigations, cause unconfirmed. How verified: scratch-copy mutations: no model-flag sort -> sort test red; J4 or J3 reverted to v1 -> prompt test red; pytest tests/unit 1043 passed. What's left: eval signature narrowness and per-run artifacts = T-093 (qa); case_02 live flap = T-094. Surprise: flags have no id at run_flag_pass stage, so list order is the observable.\"\n$B move T-075 in_review --agent backend"
}
````

### User / tool · 2026-11-02T03:44:58.985Z

**tool result**
````
T-075: commit b5b9b34 recorded
AC 2 checked: Corrected: pre-change baseline was already determinism 1.0 in 12/12 runs, so the changes are mitigations of flaky spots found; cause of the original 0.0 unconfirmed. Live 20261102T032823Z.md 1.0 / unsupported 0; per-run recorder is T-093, case_02 flap T-094
noted on T-075
handoff written on T-075
T-075: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:45:00.553Z

T-075 round 2 is in review (commit b5b9b34): the sort test now fails with the sort removed, the new judge-prompt test fails with J3 or J4 reverted to v1, and the card and diagnosis now call the changes mitigations with the cause unconfirmed. I proved both tests red on a scratch-copy mutation, and `.venv/bin/python -m pytest -q tests/unit` gives 1043 passed.
