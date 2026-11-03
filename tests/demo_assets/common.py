"""T-184 demo assets: shared setup. Archives a commit with `git archive` (never the dirty working tree), starts the app from that copy on its own port, stops it afterwards.
Not a pytest module (no test_ prefix). Usage: see shots.py and video.py."""
import contextlib
import json
import os
import pathlib
import socket
import subprocess
import tarfile
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = str(ROOT / ".venv" / "bin" / "python")


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def archive(rev="HEAD"):
    """Returns (dir, full_sha). The archive of `rev` in a fresh temp dir."""
    sha = subprocess.check_output(["git", "rev-parse", rev], cwd=ROOT, text=True).strip()
    d = pathlib.Path(tempfile.mkdtemp(prefix="demo-src-")) / "src"; d.mkdir()
    tar = subprocess.Popen(["git", "archive", sha], cwd=ROOT, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=tar.stdout, mode="r|") as t:
        t.extractall(d)
    tar.wait()
    return d, sha


@contextlib.contextmanager
def server(src, local=False):
    """Demo mode exactly as ./run.sh sets it (fixture backend, curated prepared answers). local=True adds ZLAYT_MODE=local (case list + the test-case library). Yields (base_url, db_path)."""
    port = free_port(); tmp = tempfile.mkdtemp(prefix="demo-db-"); db = os.path.join(tmp, "demo.sqlite3")
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ENABLE_LIVE")}
    env.update(LLM_BACKEND="fixture", FIXTURE_SET="curated", HOST="127.0.0.1", PORT=str(port), ZLAYT_DB=db)
    if local:
        env["ZLAYT_MODE"] = "local"
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([PY, "-m", "app.main"], cwd=src, env=env, stdout=log, stderr=subprocess.STDOUT)
    print(f"server pid {proc.pid} port {port} local={local}", flush=True)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
            except Exception:
                time.sleep(.3)
        else:
            raise RuntimeError("server did not start: " + open(os.path.join(tmp, "server.log")).read()[-800:])
        yield base, db
    finally:
        proc.terminate()
        try:
            proc.wait(10)
        except Exception:
            proc.kill()
        print(f"server pid {proc.pid} stopped", flush=True)


def api(base, method, path, body=None):
    req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw


def make_case(base, title=None, lib=None, run=True):
    body = {"sample": True} if lib is None else {"library": lib}
    if title:
        body["title"] = title
    st, c = api(base, "POST", "/api/cases", body); assert st in (200, 201), (st, c)
    tok = c["token"]
    if run:
        assert api(base, "POST", f"/api/cases/{tok}/run", {"confirm_rerun": False})[0] == 202
        for _ in range(300):
            s = api(base, "GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready", s
    return tok
