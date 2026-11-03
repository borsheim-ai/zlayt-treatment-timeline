"""Board server: CSRF refusal, input validation, XSS-safe rendering (T-002 round 2)."""
import json, os, shutil, socket, subprocess, sys, time, urllib.request
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def server(tmp_path_factory):
    root = tmp_path_factory.mktemp("b")
    (root / "tools").mkdir()
    for f in ("board.py", "board_server.py", "board_ui.html"):
        shutil.copy(REPO / "tools" / f, root / "tools" / f)
    (root / "reviews").mkdir(); (root / ".claude" / "agents").mkdir(parents=True)
    env = dict(os.environ, BOARD_ROOT=str(root))
    subprocess.run([sys.executable, str(root / "tools/board.py"), "init"], env=env, check=True, capture_output=True)
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    p = subprocess.Popen([sys.executable, str(root / "tools/board_server.py"), "--port", str(port)], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz"); break
        except Exception:
            time.sleep(0.1)
    yield f"http://127.0.0.1:{port}", root
    p.terminate()


def post(url, body, headers):
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


GOOD = {"Content-Type": "application/json", "X-Board-Client": "1"}


@pytest.mark.parametrize("headers,body", [
    ({"Content-Type": "application/json"}, '{"text":"x"}'),
    ({"Content-Type": "text/plain", "X-Board-Client": "1"}, '{"text":"x"}'),
    ({**GOOD, "Origin": "http://evil.example"}, '{"text":"x"}'),
    (GOOD, '{"text":5}'), (GOOD, "not json"), (GOOD, "[1]"),
])
def test_inbox_refuses(server, headers, body):
    url, root = server
    assert post(url + "/api/inbox", body, headers) in (400, 403)
    assert not list((root / "board" / "inbox").glob("*.md"))


def test_stop_refuses_cross_site(server):
    url, root = server
    assert post(url + "/api/stop", '{"confirm":"STOP"}', {**GOOD, "Origin": "http://evil.example"}) == 403
    assert not (root / "board" / "STOP").exists()


def test_inbox_accepts_same_origin(server):
    url, root = server
    host = url.split("//")[1]
    assert post(url + "/api/inbox", '{"text":"hello"}', {**GOOD, "Origin": url}) == 200
    assert len(list((root / "board" / "inbox").glob("*.md"))) == 1


def test_ui_has_no_inline_handlers_and_sanitizes():
    html = (REPO / "tools" / "board_ui.html").read_text()
    assert "onclick=\"open" not in html and "DOMPurify.sanitize" in html and "&#39;" in html


def test_dns_rebinding_refused(server):
    url, root = server
    before = len(list((root / "board" / "inbox").glob("*.md")))
    assert post(url + "/api/inbox", '{"text":"x"}', {**GOOD, "Host": "evil.example:7811", "Origin": "http://evil.example:7811"}) == 421
    assert post(url + "/api/inbox", '{"text":"x"}', {**GOOD, "Host": "evil.example"}) == 421
    assert len(list((root / "board" / "inbox").glob("*.md"))) == before
    req = urllib.request.Request(url + "/api/status", headers={"Host": "evil.example"})
    try:
        urllib.request.urlopen(req); code = 200
    except urllib.error.HTTPError as e:
        code = e.code
    assert code == 421


def test_csp_and_sri():
    html = (REPO / "tools" / "board_ui.html").read_text()
    assert html.count('integrity="sha384-') == 2  # marked, dompurify (pinned)
