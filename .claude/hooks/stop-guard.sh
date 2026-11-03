#!/bin/sh
# stop-guard hook — logic in stop_guard.py (§4.3)
exec python3 "$(dirname "$0")/stop_guard.py"
