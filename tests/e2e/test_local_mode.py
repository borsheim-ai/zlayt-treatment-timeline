"""Local mode (ZLAYT_MODE=local on a loopback host): case list + library; two cases reviewed side by side do not leak decisions (T-053 AC3, D-031). Starts its own app instance on a free port (fixture backend, curated set)."""
import json, os, socket, subprocess, sys, time, urllib.request
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@pytest.fixture(scope="module")
def local(tmp_path_factory):
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=str(tmp_path_factory.mktemp("loc") / "l.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None)
    p = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            time.sleep(0.5)
    else:
        p.kill(); pytest.skip("local-mode instance did not start")
    yield base
    p.terminate()

def call(base, method, path, body=None):
    req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read(); return e.code, (json.loads(raw) if raw else None)

def ready(base, tok):
    assert call(base, "POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(180):
        if call(base, "GET", f"/api/cases/{tok}/status")[1]["status"] in ("ready", "failed"): break
        time.sleep(1)
    return call(base, "GET", f"/api/cases/{tok}")[1]

def test_case_list_and_library_exist_in_local_mode_only(local):
    """D-031 / D-008: /api/cases (GET) and /api/library exist in local mode with >= 2 library cases."""
    assert call(local, "GET", "/api/cases")[0] == 200
    st, lib = call(local, "GET", "/api/library"); assert st == 200 and len(lib["cases"]) >= 2

def test_two_library_cases_do_not_leak_decisions(local):
    """T-053 AC3: create two library cases, review them in alternation; an accept/dismiss in one never shows in the other, and each export holds only its own accepted entries."""
    ids = [c["id"] for c in call(local, "GET", "/api/library")[1]["cases"]][:2]
    toks = []
    for i in ids:
        st, c = call(local, "POST", "/api/cases", {"library": i}); assert st == 201; toks.append(c["token"])
    cases = [ready(local, t) for t in toks]
    a, b = cases
    ea = [e for e in a["entries"] if e["state"] != "rejected"][0]; eb = [e for e in b["entries"] if e["state"] != "rejected"][0]
    assert call(local, "POST", f"/api/cases/{toks[0]}/items/{ea['id']}/review", {"action": "accept"})[0] == 200
    assert call(local, "POST", f"/api/cases/{toks[1]}/items/{eb['id']}/review", {"action": "dismiss"})[0] == 200
    a2 = call(local, "GET", f"/api/cases/{toks[0]}")[1]; b2 = call(local, "GET", f"/api/cases/{toks[1]}")[1]
    st_a = {e["id"]: e["review_status"] for e in a2["entries"]}; st_b = {e["id"]: e["review_status"] for e in b2["entries"]}
    assert st_a[ea["id"]] == "accepted" and st_b[eb["id"]] == "dismissed"
    assert sum(v != "pending" for v in st_a.values()) == 1 and sum(v != "pending" for v in st_b.values()) == 1
    la = call(local, "GET", f"/api/cases/{toks[0]}/export")[1]["letter_text"]
    st_b2, body_b = call(local, "GET", f"/api/cases/{toks[1]}/export")      # D-045: case B has nothing accepted (one dismissal), so its export is refused, not an empty letter
    assert st_b2 == 422 and ea["summary"] not in json.dumps(body_b)
    assert ea["summary"] in la and eb["summary"] not in la
    for t in toks: call(local, "DELETE", f"/api/cases/{t}")
