---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].
