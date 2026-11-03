"""T-183 r2: resource bounds for the public demo build (security review: any client could fill the disk and burn CPU; no money is at stake because the
public build makes no model call). Two caps, public mode only (ZLAYT_MODE != local); local/dev stays unlimited:
  DEMO_MAX_CASES  stored cases, default 200  -> POST /api/cases and the PDF upload answer 429 `busy` when the table is full (expired cases are purged first)
  DEMO_MAX_RUNS   runs in flight, default 4  -> POST /api/cases/{token}/run answers 429 `busy`
Pure functions that return a plain sentence (or None); the route turns it into the standard error body. No stack text, no key, no count of other users' data.
The case cap is a soft bound: simultaneous creates can overshoot it by a few, never grow it without limit."""
import os

DEFAULT_MAX_CASES = 200
DEFAULT_MAX_RUNS = 4
FULL_MESSAGE = "This demo is full right now. Try again later."
BUSY_MESSAGE = "This demo is busy right now. Try again in a minute."


def _limit(name: str, default: int) -> int:
    try:
        n = int(os.environ.get(name, "").strip() or default)
    except ValueError:
        return default
    return n if n >= 1 else default           # a zero, negative or unreadable value falls back to the default (a typo must not switch the demo off or lock it shut)


def max_cases() -> int:
    return _limit("DEMO_MAX_CASES", DEFAULT_MAX_CASES)


def max_runs() -> int:
    return _limit("DEMO_MAX_RUNS", DEFAULT_MAX_RUNS)


def case_full(conn, local: bool):
    """The 429 sentence when the public demo already stores the maximum number of cases, else None. Call after expired cases are purged."""
    if local:
        return None
    return FULL_MESSAGE if conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0] >= max_cases() else None


def runs_busy(in_flight: int, local: bool):
    """The 429 sentence when the public demo already has the maximum number of runs in flight, else None."""
    if local:
        return None
    return BUSY_MESSAGE if in_flight >= max_runs() else None
