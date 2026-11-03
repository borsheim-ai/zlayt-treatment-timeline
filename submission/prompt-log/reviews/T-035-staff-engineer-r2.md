# T-035 round 2 review - staff-engineer-reviewer (commit 250e7b6)

Verdict: changes. Both round-1 blockers are fixed. One major (the eval report, AC6) remains open, and there is one minor.

Blocker 1, generator tests: `tests/unit/test_generator.py` has 17 tests. I checked them by mutation in a scratch copy of `app/`, `tests/`, `evals/`, `docs/` and `spec/`. The baseline of `test_generator`, `test_judges`, `test_schemas` and `test_grounding` is `1 failed, 114 passed`. The one failure is `test_j2_every_amount`, which is the T-037 pipeline stub.

| Mutation | Result |
|---|---|
| `generator.verify` grounding rejection set to `failures = []` | 3 failed (2 new generator tests plus the stub) |
| J1 recompose in `judge_entries` replaced with `pass` | 4 failed (3 generator tests plus the stub) |
| Judge failure returns `supported` | 7 failed |
| Unparseable judge output returns `supported` | 5 failed |
| J2 `disagree` mapped to `supported` | 2 failed |
| J2 runs on the first amount only | 2 failed |
| `SCHEMA_INVALID` not flagged | 2 failed |
| Rejected entries sent to J1 | 2 failed |
| A free-text `reason` re-added to Judge1 | 2 failed |

Every mutation is caught. The persona red flag "tests pass when the verifier is stubbed out" no longer holds.

Blocker 2, D-028: `schemas.py` Judge1-4 now carry only `verdict` and `reason_code`. `reason_code` is a closed `Literal` per judge. The JSON schema given to the provider has `properties == {verdict, reason_code}`, `additionalProperties: false`, and `required: [verdict, reason_code]`. A free-text `reason_code` raises `ValidationError`. An old-style `reason` key is ignored and never stored. All four judge prompts list the closed codes. The Why? text comes from the `why.judge_detail` templates in code. `ladder.judge` stores `reason_code` only.

Remaining problems:

- AC6 is still open. The four judge prompts were rewritten in r2, so any earlier report would be stale. The eval runner from T-038 exists, but a run waits for T-037.
- `test_j2_every_amount` still fails. AC4 was correctly unchecked, and `judge_amounts` is covered pipeline-free.
- A minor: the local schema is looser than the one handed to the provider (`reason_code` is required there but defaults to `NONE` locally).

Exercised:

- `python3 tools/board.py show T-035`
- Read in full: `schemas.py`, `generator.py`, `judges.py`, `test_generator.py`. Read the judge prompts via `grep reason`.
- `.venv/bin/python -m pytest` on the four files above, and on the whole of `tests/unit` (`45 failed, 646 passed, 6 errors`, all stubs of other cards).
- Nine scratch mutations (table above), each restored from the repo copy.
- Probes of `Judge1.model_json_schema()`, of a missing `reason_code`, and of a free-text `reason_code`.
- Grepped `except` and `float(` in `generator.py` and `judges.py`. There is no bare except and no float. Every `except` names its exception type.

```json
{"card": "T-035", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2, commit 250e7b6: app/backend/{generator,judges,schemas,why}.py, tests/unit/test_generator.py, judge prompts; scratch-copy mutation run",
 "exercised": ["board show T-035", "pytest test_generator/test_judges/test_schemas/test_grounding: 1 failed (test_j2_every_amount, T-037 stub) 114 passed", "pytest tests/unit: 45 failed 646 passed 6 errors (other cards' stubs)", "read schemas.py, generator.py, judges.py, test_generator.py, judge prompts (grep reason)", "9 mutations in a scratch copy (grounding rejection off, J1 recompose off, judge fail->supported, invalid->supported, j2 disagree->supported, j2 first amount only, schema-invalid unflagged, rejected sent to J1, free-text reason re-added): every one fails at least one test", "Judge1.model_json_schema(): properties {verdict, reason_code}, additionalProperties false; free-text reason_code -> ValidationError; missing reason_code -> NONE", "grep except/float in generator.py, judges.py: clean"],
 "verdict": "changes",
 "scores": {"determinism_and_code_vs_llm_split": 4, "failure_visibility": 5, "test_strength": 4, "spec_conformance": 4, "prompt_separation_and_injection_structure": 4},
 "findings": [
  {"severity": "major", "title": "Judge prompts changed in r2 with no eval report; AC6 open",
   "evidence": "card AC6 done:false; `ls evals/reports` lists no report; app/llm/prompts/judge_{faithfulness,amount_class,conflict,flag}_v1.md changelog lines say 'D-028 reason_code, no prose; label inside delimiters'; board note: 'AC6 open until T-038 eval runner'.",
   "why_it_matters": "Checklist 18 / CONTRACT 8.3: prompt and schema changes ship with a re-run eval report. The judge output contract changed (reason_code), and nothing yet shows the live judges still catch the 40 seeded hallucinations with the new output shape, or that the model emits valid reason_code values.",
   "fix": "After T-037 lands, run `LLM_BACKEND=claude-cli python -m evals.run`, attach evals/reports/<ts>.md and link it in the handoff; its prompt hashes must equal the files at HEAD.",
   "acceptance_test": "`python -m evals.run --check-fresh` exits 0 and the report lists the sha256 of all judge prompts; hallucination_catch_rate >= 0.95."},
  {"severity": "minor", "title": "Local judge validation is looser than the schema sent to the provider: a missing reason_code is silently defaulted to NONE",
   "evidence": "app/backend/schemas.py: `reason_code: _J1_CODES = \"NONE\"` with json_schema_extra required [verdict, reason_code]. Repro: `Judge1.model_validate({'verdict':'unsupported'})` -> verdict='unsupported' reason_code='NONE' (no error).",
   "why_it_matters": "Checklist 7: a validation failure should be a visible state, not a default value. The verdict still decides the state, so no unsafe outcome. But a model that stops emitting reason_code is not noticed, and the Why? detail silently disappears.",
   "fix": "Make reason_code required (no default) in Judge1-4, so a missing code becomes 'unsure', or add a test that pins the lenient behaviour as intended.",
   "acceptance_test": "test_schemas: Judge1.model_validate({'verdict':'unsupported'}) raises ValidationError, or an explicit test documents the default."}
 ],
 "whats_right": ["test_generator.py kills every mutation I tried (grounding rejection, J1 recompose, fail-open judge, J2 coverage), with no pipeline dependency.", "D-028 is enforced in the schema handed to the provider, the closed-list Literals, the prompts and the code-template Why? text, with a test that re-adding a free-text field fails.", "The source label now sits inside the nonce block, with a test asserting the nearest delimiter before the label is an opener."],
 "questions_for_chris": []}
```
