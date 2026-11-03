---
name: prompt-log-privacy-rules
description: How evals/finalize_prompt_log.py matches private terms (gapped view, derived terms, outside-name switch precedence), D-072 one-final-build policy, test and checker locations
metadata:
  type: project
---

Rules live in `evals/finalize_prompt_log.py`; terms come from git-ignored `deploy/.private_patterns` (never print values; counts only, `<redacted>` in notes).

- Matching: normalized view (strip backslash/quotes/`+`/whitespace, casefold) PLUS a gapped alt per term of 7+ alnum chars: 0-12 punctuation chars between any two chars, 1-12 where the value has its own separator (`.`,`@`,`-`,`/`). Separator-required keeps the work-email local part (= Chris's public first.last) from redacting the prose "First Last".
- Derived terms in `load_terms()/_derive()`: device name minus `-<digits>` suffix; each `/` piece (8+) of a personal value; any term/email/device/third line equal (normalized) to an `#@outside` value is dropped so `REDACT_OUTSIDE_PROJECT_NAME` is the only switch. Values sorted longest-first so full host wins over its stem.
- Outside name: `OUTSIDE_PATH_RX` swallows whole path tails (`name-x/sub/file`) on the backslash-stripped view, then `OUTSIDE_RX` on the normalized view; HOME rules run first so `/Users/<u>/<name>/..` becomes `<home-path>`.
- D-072: do NOT rebuild/review per round; the final build + one independent privacy sweep happens at submission time inside T-188; the final privacy reviewer's own transcript is omitted from the published set (README lists the one omitted file).
- Tests: `tests/unit/test_finalize_prompt_log.py` (synthetic patterns via `SNAPSHOT_PATTERNS`, plus a real-pattern run of the reviewer checker `artifacts/review-evidence/T-187-r4-focus.py HEAD`, must print n=0 on every label; skipped without the local file).
- Pitfall: every review/QA session adds a transcript that carries private stems (tool output echoing card notes), so an early build can never stay clean. Never `print` a pattern value in a tool call; mask shapes (`a`/`9`) when you need to inspect.
