"""T-136 r3 (staff review r2 major 2): when the e2e conftest's private server cannot start, the run stops loudly with the server's own log. It must never fall back to whatever answers on :7860."""
import subprocess
import sys

import pytest

from tests.e2e import conftest as C


def _no_env(monkeypatch):
    monkeypatch.delenv("E2E_BASE_URL", raising=False)
    monkeypatch.delenv("ZLAYT_DB", raising=False)
    monkeypatch.setattr(C, "BASE", "http://localhost:7860")


def test_a_server_that_exits_at_start_stops_the_run_with_its_log_and_leaves_base_alone(monkeypatch):
    _no_env(monkeypatch)
    real = subprocess.Popen
    monkeypatch.setattr(subprocess, "Popen", lambda cmd, **kw: real([sys.executable, "-c", "print('boom: cannot import app.main'); raise SystemExit(3)"], **kw))
    with pytest.raises(pytest.exit.Exception) as e:
        C.pytest_configure(config=None)
    msg = str(e.value)
    assert "private test server" in msg and "exited with code 3" in msg and "boom: cannot import app.main" in msg, msg
    assert "nothing was sent to :7860" in msg.lower()
    assert C.BASE == "http://localhost:7860" and not C._PRIVATE.get("proc"), "no private server is registered and BASE was not pointed anywhere"


def test_a_server_that_never_answers_stops_the_run_too(monkeypatch):
    _no_env(monkeypatch)
    real = subprocess.Popen
    monkeypatch.setattr(subprocess, "Popen", lambda cmd, **kw: real([sys.executable, "-c", "import time; time.sleep(60)"], **kw))
    import time as _t
    monkeypatch.setattr(_t, "sleep", lambda s: None)                                  # do not wait out the 40 seconds
    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(OSError("refused")))
    with pytest.raises(pytest.exit.Exception) as e:
        C.pytest_configure(config=None)
    assert "did not answer /api/health" in str(e.value)
