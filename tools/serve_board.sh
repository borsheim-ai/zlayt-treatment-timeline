#!/bin/sh
# Start (or restart) the board server in a detached tmux session so it survives tool calls and terminal closes.
cd "$(dirname "$0")/.." || exit 1
[ -x .git/hooks/pre-commit ] || ./tools/install_git_hooks.sh  # native secret scan for commits made outside Claude Code
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:board 2>/dev/null
tmux new-window -d -t zlayt -n board "python3 tools/board_server.py --port 7777 >> board/.server.log 2>&1"
sleep 1
curl -fsS http://localhost:7777/healthz && echo " board up on :7777"
