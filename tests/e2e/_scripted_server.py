"""Serve this tree's real app (API + app/frontend) on a spare port with a scripted call factory, so a pasted SYNTHETIC ledger runs without a model: demo mode refuses unrecorded text, and
amounts, the count rules and `count_confirm` are code, not LLM. Used by tests/e2e/test_count_duplicate.py (T-172 r2) to put a REAL likely_duplicate countable line in front of the page.
Usage: python tests/e2e/_scripted_server.py DB_PATH PORT"""
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.update(LLM_BACKEND="claude-cli", ENABLE_LIVE="1", ZLAYT_MODE="local", HOST="127.0.0.1")
os.environ.pop("ANTHROPIC_API_KEY", None)
import uvicorn  # noqa: E402

from app.backend.api import create_app  # noqa: E402

SCRIPT = {"extract": dict(summary="Cervical strain.", excerpt="Dx: cervical strain."), "extract_es": dict(summary="Cervical strain.", excerpt="Dx: cervical strain."),
          "j1": dict(verdict="supported", reason_code="NONE"), "j2": dict(verdict="agree", reason_code="NONE"), "j3": dict(verdict="benign", reason_code="NONE"),
          "j4": dict(verdict="agree", reason_code="NONE"), "conflicts": {"flags": []}, "flags": {"flags": []}}


def factory(conn, cid):
    def call(step, system, user, schema, *, item_id=None, validate=None):
        return SCRIPT[step], None
    return call


if __name__ == "__main__":
    uvicorn.run(create_app(sys.argv[1], call_factory=factory), host="127.0.0.1", port=int(sys.argv[2]), access_log=False, log_level="warning")
