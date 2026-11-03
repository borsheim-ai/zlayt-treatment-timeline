---
name: backend-llm-review-patterns
description: T-035 r1 and T-033 r2 recurring findings - untested wiring, judge reason prose, label-window bleed in amount classification, scratch-copy controls
metadata:
  type: project
---

T-035 r1 (a2fc95a): pure-module tests (grounding, judges) pass while the stage module (generator.py) that wires them has none; mutate the call site in a scratch copy (cp -R app tests evals into scratchpad; avoid rm -rf, it is denied) to prove it.
**Why:** card ACs cite "scratch run" evidence and tests that depend on pipeline stubs (T-037), so nothing in the repo proves the wiring.
**How to apply:** on every backend LLM card, mutate the caller, not the helper; check ACs marked done whose named test fails.
Also check: judge schemas with a free `reason: str` vs LLM_VS_CODE row 5 / ADR-008.5 (enum only); labels (Source:) placed outside nonce delimiters.
Live check recipe: LLM_BACKEND=claude-cli, ingest.ingest(raw)["records"], DB.connect+create_case, audited.make_call -> generator.extract_one; 2 calls works and keeps "may represent" on record 8.

T-033 r2 (amounts.py): a fix that narrows the trigger words (per/each/rate -> per+unit noun) closes the reviewer's repro strings but leaves the six-word label window unbounded, so a rate phrase from the previous figure still leaks across a comma and reclassifies the next charge. Probe the same sentence with '.' and ',' in place of each other, and probe a figure after another figure's rate phrase, not only the reported strings.
**Why:** the r1 finding was a symptom (a charge reads as rate); the cause was the window, so word-list fixes recur.
**How to apply:** for any extraction/classification fix, re-run the original repro plus neighbouring-figure variants; check the window boundary, not only the trigger regex. Do not split on comma alone (it breaks 'Charge per visit, $185.').
Also: a scratch copy must include memory/ (tests read memory/contracts/*.md) or the full-suite control is invalid; cp -R of the tree minus .venv worked, an rsync-based copy was denied by the sandbox. Run mutations on test_<module>.py first, then the full suite only with a valid control.
T-035 r2: backend fixed both blockers well (9/9 scratch mutations killed); remaining = eval report/AC6 waiting on T-038/T-037.
T-038 (eval runner): gate code had `except Exception` fallbacks, ship_bar ignored runs>=3, --check-spec left stale ship_bar_met, tests assert only "ship_bar_met False" (mutate each bar term to check). Scratch copy needs memory/ dir too (tests read memory/contracts/api.md); run only test_eval_* files.
