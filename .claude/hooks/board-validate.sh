#!/bin/sh
# board-validate hook — logic in board_validate.py (§4.3)
exec python3 "$(dirname "$0")/board_validate.py"
