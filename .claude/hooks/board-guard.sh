#!/bin/sh
# board-guard PreToolUse hook — logic in board_guard.py. Fails closed: if Python crashes without a decision, deny.
dir=$(dirname "$0")
PY=python3; [ -x /opt/homebrew/bin/python3 ] && PY=/opt/homebrew/bin/python3
out=$("$PY" "$dir/board_guard.py"); rc=$?
if [ $rc -ne 0 ] && [ -z "$out" ]; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"board-guard crashed (rc='"$rc"'); denying to fail closed"}}'
  exit 0
fi
[ -n "$out" ] && printf '%s\n' "$out"
exit $rc
