---
name: demo-live-gate
description: Status of the demo live-call gate in provider.py (T-053 r1 blocker fixed in 02f9939, verified r2 at e83eb54); residual env-var paths to recheck on any card touching LLM_BACKEND, ENABLE_LIVE, RECORD_FIXTURES or runs
metadata:
  type: project
---

T-053 r1 (c61e84f): `provider.complete_with_meta` sent `claude-cli` and `anthropic-api` straight to the SDK with no ENABLE_LIVE or demo check. Fixed in 02f9939 by `provider.backend_name()` (provider.py:23-30): returns 'fixture' unless ENABLE_LIVE=1 or `_record_ok` (set only by record_context).

T-053 r2 (pinned e83eb54, archive artifacts/review-evidence/T-053-r2/head_e83eb54): with LLM_BACKEND=anthropic-api, dummy key, ENABLE_LIVE unset, the provider call, API sample run and RECORD_FIXTURES=1 API run all showed 0 SDK constructor/create calls and 0 socket attempts. Closed for the server path.

Residuals (all minor in r2):
- ENABLE_LIVE=1 with no key: health says backend anthropic-api, demo_mode true; runs fail BACKEND_UNAVAILABLE (fail closed, label wrong).
- RECORD_FIXTURES=1 without ENABLE_LIVE: dev path `pipeline.run_case` makes live calls (132 stub events). Server path does not reach it (judge_summary only from app/llm/record.py).

**Why:** D-008 says live needs an explicit ENABLE_LIVE opt-in; spec DECISIONS.md:163 says demo uses fixtures. The gate lives in provider.py, not only in the API layer, so check provider first.

**How to apply:** on any card touching runs, library loading, pasted text, LLM_BACKEND, ENABLE_LIVE or RECORD_FIXTURES, re-run the stub probe (counting `anthropic.Anthropic` ctor and `messages.create`, socket connect blocked) on the pinned commit. Note the installed SDK (anthropic 2.3.0) lacks the `temperature` kwarg the backend passes, so use a stub, not a real key.

Related: [[round2-review-workflow]], [[config-gate-patterns]]
