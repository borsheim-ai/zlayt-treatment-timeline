"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok, allow_failed=False):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (allow_failed and s["status"] == "failed"), s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
    assert c.post("/api/cases", content=b"{not json", headers={"content-type": "application/json"}).status_code == 400
    assert c.post("/api/cases/nope/accept_all", json={}).status_code in (404, 405)


def test_demo_gate_refuses_unrecorded_text_and_stores_nothing(env):
    db, c = env
    from app.db import db as DB
    r = c.post("/api/cases", json={"text": "SYNTHETIC totally new text\n\n=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: \"Hello.\""})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"
    assert DB.connect(db).execute("SELECT count(*) FROM cases").fetchone()[0] == 0
    assert c.post("/api/cases", json={"text": "   "}).status_code == 400
    assert c.post("/api/cases", json={"text": "x" * 70000}).status_code == 413
    # a recorded golden text (CRLF, padded) passes the gate
    assert c.post("/api/cases", json={"text": "\n" + G.raw("case_01_date_formats").replace("\n", "\r\n") + "\n"}).status_code == 201


def test_whole_case_after_run_matches_contract(env):
    _, c = env
    tok = run_case(c)
    g = c.get(f"/api/cases/{tok}").json()
    assert len(g["entries"]) == 9 and [e["date"] for e in g["entries"]] == sorted(e["date"] for e in g["entries"])
    e = g["entries"][0]
    assert {"id", "record_ids", "date", "provider", "summary", "excerpt", "excerpt_start", "state", "reasons", "why", "review_status", "ladder"} <= set(e)
    assert g["totals"]["pending"]["cents"] == 839000 and g["review"]["counts"]["pending"] == len(g["review"]["queue"])
    assert g["review"]["queue"] and g["tray"] == [] and g["backend"] == "fixture"
    gap = [f for f in g["flags"] if f["type"] == "gap"][0]
    assert gap["computed"]["days"] == 73 and gap["computed"]["from"] == "2026-03-06" and gap["evidence"][0]["record_id"]
    rec = g["records"][0]
    assert rec["sentences"] and all(g_text(rec, s) == s["text"] for s in rec["sentences"])


def g_text(rec, s):
    return rec["text"][s["start"] - rec["char_start"]:s["end"] - rec["char_start"]]


def test_why_returns_ladder_backend_and_calls(env):
    _, c = env
    tok = run_case(c)
    g = c.get(f"/api/cases/{tok}").json()
    w = c.get(f"/api/cases/{tok}/items/{g['entries'][0]['id']}").json()
    assert w["item"]["ladder"]["backend"] == "fixture" and w["calls"] and w["source"][0]["highlight_start"] is not None
    assert "user_text" not in w["calls"][0]
    assert c.get(f"/api/cases/{tok}/items/zzz").status_code == 404


def test_review_http_matrix_and_decisions_survive_restart(env, tmp_path):
    db, c = env
    tok = run_case(c)
    g = c.get(f"/api/cases/{tok}").json()
    e5 = [e for e in g["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
    ok = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "accept"})
    assert ok.status_code == 200 and ok.json()["item"]["review_status"] == "accepted" and ok.json()["review"]["counts"]["accepted"] == 1
    bad = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"date": "2026-01-01"}})
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_edit"
    nc = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}})
    assert nc.status_code == 422 and nc.json()["error"]["code"] == "invalid_edit"          # D-034: a figure not in the quote is never saved
    assert c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "bulk"}).status_code == 422
    c2 = TestClient(create_app(db, static_dir=str(tmp_path)))           # restart: the decision is still there
    assert [e for e in c2.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == e5][0]["review_status"] == "accepted"


def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode(env):
    _, c = env
    tok = run_case(c)
    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
    r = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10 and improving; patient reports missing 3 days of work, per the paralegal."}})
    j = r.json()
    assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
    assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]


def test_charge_cannot_be_edited_and_rerun_needs_confirm(env):
    _, c = env
    tok = run_case(c)
    a = c.get(f"/api/cases/{tok}").json()["amounts"][0]["id"]
    assert c.post(f"/api/cases/{tok}/items/{a}/review", json={"action": "edit", "edits": {"value": 1}}).status_code == 422
    assert c.post(f"/api/cases/{tok}/items/{a}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/run", json={})
    assert r.status_code == 409 and r.json()["error"]["code"] == "needs_confirm"


def test_confirm_date_case_01(env):
    _, c = env
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    rec = [r for r in g["records"] if r["date_status"] == "ambiguous"][0]
    gaps_before = sorted(f["id"] for f in g["flags"] if f["type"] == "gap")
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
    r = c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]})
    assert r.status_code == 200 and r.json()["record"]["date_status"] == "confirmed"
    g2 = c.get(f"/api/cases/{t}").json()
    assert g2["dates_to_confirm"] == [] and not [e for e in g2["undated_entries"] if rec["id"] in e["record_ids"]]
    if not rec["encounter"]:
        assert sorted(f["id"] for f in g2["flags"] if f["type"] == "gap") == gaps_before
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 422
    assert any(e["action"] == "confirm_date" for e in c.get(f"/api/cases/{t}/audit").json()["events"])


def test_export_equals_golden_when_everything_accepted(env):
    _, c = env
    tok = run_case(c)
    g = c.get(f"/api/cases/{tok}").json()
    held = []
    for it in g["entries"] + [a for a in g["amounts"] if a["kind"] == "charge"] + g["flags"]:
        r = c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
        if r.status_code == 422 and r.json()["error"]["detail"].get("reason_code") == "CHARGE_TEXT_IN_ENTRY":     # T-139: an entry whose quote cannot be narrowed is held out until re-quoted
            held.append(it["id"])
            continue
        assert r.status_code == 200
    assert held == []                                   # T-139 narrowing: the sample's e2/e4 lose their trailing charge sentence, so nothing is held out
    ex = c.get(f"/api/cases/{tok}/export").json()
    assert "$6,240" not in ex["letter_text"].split("BILLED CHARGES")[0] and "$185" not in ex["letter_text"]
    lines = ex["letter_text"].split("\n")
    assert lines[0] == "TREATMENT CHRONOLOGY" and "Billed charges accepted from these records: $8,390.00" in lines
    assert ex["internal_notes_text"]    # golden byte-equality runs on the curated fixture set (D-029, qa T-051)
    assert ex["totals"]["charges_cents"] == 839000 and ex["provenance"]["backend"] == "fixture" and "counts" in ex


def test_delete_removes_everything(env):
    db, c = env
    from app.db import db as DB
    tok = run_case(c)
    assert c.delete(f"/api/cases/{tok}").status_code == 204 and c.get(f"/api/cases/{tok}").status_code == 404
    conn = DB.connect(db)
    assert all(conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0] == 0 for t in ("cases", "records", "entries", "amounts", "flags", "llm_calls", "review_events"))


def test_only_review_module_sets_review_status():
    """T-040 AC5: apply_review/set_review_status are called only from review.py (and the pipeline's own rerun reset); no bulk route."""
    for p in (ROOT / "app" / "backend").glob("*.py"):
        if p.name in ("review.py", "pipeline.py", "case_extras.py"):   # case_extras: batch accept of verified entries (D-031)
            continue
        src = p.read_text()
        assert "DB.apply_review(" not in src and "set_review_status(" not in src, p.name
    tree = ast.parse((ROOT / "app" / "backend" / "api.py").read_text())
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and "accept_all" in n.value]


def test_no_text_in_logs(env, caplog, capsys):
    _, c = env
    caplog.set_level("DEBUG")
    run_case(c)
    out = capsys.readouterr()
    assert "Jordan Rivera" not in caplog.text + out.out + out.err


def test_two_cases_coexist_with_short_display_ids(env):
    """T-050: the same short ids (e1, r1, f_gap_r6_r7) exist in two cases; review on one does not touch the other; delete is per case."""
    _, c = env
    a, b = run_case(c), run_case(c)
    ga, gb = c.get(f"/api/cases/{a}").json(), c.get(f"/api/cases/{b}").json()
    assert [e["id"] for e in ga["entries"]] == [e["id"] for e in gb["entries"]] and ga["entries"][0]["id"].startswith("e") and "." not in ga["entries"][0]["id"]
    eid = ga["entries"][0]["id"]
    assert c.post(f"/api/cases/{a}/items/{eid}/review", json={"action": "accept"}).status_code == 200
    assert c.get(f"/api/cases/{b}").json()["entries"][0]["review_status"] == "pending"
    assert c.delete(f"/api/cases/{a}").status_code == 204 and len(c.get(f"/api/cases/{b}").json()["entries"]) == 9


class _Boom:
    STAGES = ()
    @staticmethod
    def ingest_case(*a, **k): raise RuntimeError("SECRET RECORD TEXT in a traceback")


def test_failed_create_stores_nothing_and_returns_clean_json(tmp_path, monkeypatch):
    """T-040 security r1: an unexpected failure during create leaves no case row and a standard JSON 500 without trace or text."""
    from app.db import db as DB
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    db = str(tmp_path / "boom.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path), pipeline=_Boom), raise_server_exceptions=False)
    r = c.post("/api/cases", json={"sample": True})
    assert r.status_code == 500 and r.json()["error"]["code"] == "internal" and "SECRET" not in r.text and "Traceback" not in r.text
    assert DB.connect(db).execute("SELECT count(*) FROM cases").fetchone()[0] == 0


def test_csp_and_nosniff_on_api_and_static(env, tmp_path):
    (tmp_path / "index.html").write_text("<p>hi</p>")
    _, c = env
    for path in ("/api/health", "/"):
        h = c.get(path).headers
        assert "script-src 'self'" in h["content-security-policy"] and "unsafe-inline" not in h["content-security-policy"].split("script-src-attr")[0]
        assert "frame-ancestors 'none'" in h["content-security-policy"] and h["x-content-type-options"] == "nosniff"


def test_oversize_body_is_413_before_parsing(env):
    _, c = env
    r = c.post("/api/cases", content=b'{"text":"' + b"x" * (600 * 1024) + b'"}', headers={"content-type": "application/json"})
    assert r.status_code == 413 and r.json()["error"]["code"] == "input_too_large"


def test_live_anthropic_needs_provider_cap_confirmation(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ENABLE_LIVE", "1"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.delenv("PROVIDER_CAP_CONFIRMED", raising=False)
    with pytest.raises(RuntimeError):
        create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path))
    monkeypatch.setenv("PROVIDER_CAP_CONFIRMED", "1")
    create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path))


def test_expired_case_is_gone_without_any_create(env):
    import time as _t
    from app.db import db as DB
    db, c = env
    conn = DB.connect(db)
    old = DB.create_case(conn, "SYNTHETIC", now=_t.time() - 25 * 3600)
    assert c.get(f"/api/cases/{old}").status_code == 404


def test_audit_is_metadata_only_unless_local_mode(env, monkeypatch):
    """T-040 AC (T-051 privacy): public/demo audit has no prompt, response, record or edit text; ZLAYT_MODE=local adds them."""
    _, c = env
    tok = run_case(c)
    e = c.get(f"/api/cases/{tok}").json()["entries"][0]
    c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"})
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    a = c.get(f"/api/cases/{tok}/audit").json()
    assert a["calls"] and {"model", "backend", "prompt_sha256", "verdict", "latency_ms"} <= set(a["calls"][0])
    assert not [k for call in a["calls"] for k in ("system_text", "user_text", "response_raw", "error") if k in call]
    assert "Jordan Rivera" not in c.get(f"/api/cases/{tok}/audit").text and all("before" not in ev and "after" not in ev for ev in a["events"])
    monkeypatch.setenv("ZLAYT_MODE", "local")
    full = c.get(f"/api/cases/{tok}/audit").json()
    assert full["calls"][0]["user_text"] and full["calls"][0]["system_text"] and "before" in full["events"][0]


def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
    """T-053 AC1: public/demo stays token-only (404); local mode lists cases and the library and loads a library case in one call."""
    _, c = env
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.get("/api/cases").status_code == 404 and c.get("/api/library").status_code == 404
    assert c.post("/api/cases", json={"library": "case_01_date_formats"}).status_code == 404
    monkeypatch.setenv("ZLAYT_MODE", "local")
    lib = c.get("/api/library").json()["cases"]
    assert lib and "path" not in lib[0] and {"id", "name", "description"} <= set(lib[0])
    r = c.post("/api/cases", json={"library": lib[0]["id"]})
    assert r.status_code == 201 and r.json()["token"] != tok
    listed = c.get("/api/cases").json()["cases"]
    assert [x["token"] for x in listed][:2] == [r.json()["token"], tok] and {"name", "status", "record_count", "counts", "created_at"} <= set(listed[0])
    assert "text" not in listed[0] and c.post("/api/cases", json={"library": "nope"}).status_code == 404


def test_cases_do_not_leak_decisions_between_each_other(env, monkeypatch):
    """T-053 AC3 (API half): decisions on one case never show on the other."""
    _, c = env
    monkeypatch.setenv("ZLAYT_MODE", "local")
    a, b = run_case(c), run_case(c, G.raw("case_01_date_formats"))
    ea = c.get(f"/api/cases/{a}").json()["entries"][0]["id"]
    assert c.post(f"/api/cases/{a}/items/{ea}/review", json={"action": "accept"}).status_code == 200
    la = {x["token"]: x["counts"] for x in c.get("/api/cases").json()["cases"]}
    assert la[a]["accepted"] == 1 and la[b]["accepted"] == 0


def test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set(env, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False


@pytest.mark.parametrize("host,ok", [("127.0.0.1", True), ("::1", True), ("localhost", True), ("0.0.0.0", False), ("192.168.1.20", False)])
def test_local_mode_refuses_non_loopback_host(tmp_path, monkeypatch, host, ok):
    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", host)
    if ok:
        create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path))
    else:
        with pytest.raises(RuntimeError):
            create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path))
    monkeypatch.delenv("ZLAYT_MODE")
    monkeypatch.setenv("HOST", "0.0.0.0")
    create_app(str(tmp_path / "h2.sqlite"), static_dir=str(tmp_path))          # public demo may bind anywhere


def test_library_texts_are_admitted_only_in_local_mode(env, tmp_path, monkeypatch):
    import app.backend.api as A
    lib = tmp_path / "lib"; lib.mkdir()
    (lib / "lib_case.txt").write_text(G.raw("sample").replace("Jordan Rivera", "Library Person"))
    monkeypatch.setattr(A, "LIBRARY", lib)
    text = (lib / "lib_case.txt").read_text()
    _, c = env
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    assert c.post("/api/cases", json={"text": text}).status_code == 409           # public demo: not a recorded text
    assert c.post("/api/cases", json={"library": "lib_case"}).status_code == 404
    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", "127.0.0.1")
    assert c.post("/api/cases", json={"library": "lib_case"}).status_code == 201
    assert c.post("/api/cases", json={"text": text}).status_code == 201


def test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):
    """D-036: peer address, not the HOST env var, gates local mode (covers `uvicorn --host 0.0.0.0`)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.delenv("HOST", raising=False)
    app = create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path))
    for peer in ("127.0.0.1", "127.0.0.5", "::1", "::ffff:127.0.0.1"):
        assert TestClient(app, client=(peer, 5000)).get("/api/cases").status_code == 200, peer
    for peer in ("192.168.1.5", "10.0.0.2", "<redacted-private>", "0.0.0.0", "testclient"):
        r = TestClient(app, client=(peer, 5000)).get("/api/cases")
        assert r.status_code == 403 and r.json()["error"]["code"] == "forbidden", peer
        assert TestClient(app, client=(peer, 5000)).get("/api/health").status_code == 403
    monkeypatch.delenv("ZLAYT_MODE")                                    # public build: no peer restriction
    assert TestClient(app, client=("192.168.1.5", 5000)).get("/api/health").status_code == 200


def test_side_or_negation_edit_is_a_422_with_plain_reason_and_confirm_flag_changes_nothing_d047(env):
    _, c = env
    tok = run_case(c)
    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]
    before = c.get(f"/api/cases/{tok}").json()
    for flag in ({}, {"confirm_warnings": True}):
        r = c.post(f"/api/cases/{tok}/items/{e5['id']}/review", json={"action": "edit", "edits": {"summary": "Visit 8: left-sided pain 4/10, improving; no missed work."}, **flag})
        err = r.json()["error"]
        assert r.status_code == 422 and err["code"] == "invalid_edit" and err["detail"]["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT"
        assert {"left", "no"} <= set(err["detail"]["tokens"]) and "quote" in err["message"]
    assert c.get(f"/api/cases/{tok}").json()["entries"] == before["entries"]


def test_no_409_confirm_path_for_edits_or_manual_entry_remains_d047():
    """D-047: grep the backend. The only needs_confirm left is the re-run of a case that already has decisions (api.py); review.py has no confirm flag."""
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[2] / "app" / "backend"
    src = {p.name: p.read_text() for p in root.glob("*.py")}
    assert "confirm_warnings" not in "".join(src.values()) and "keep_my_wording" not in "".join(src.values())
    assert [n for n, t in src.items() if "needs_confirm" in t] == ["api.py"]


def test_t142_case_view_states_what_the_conflict_check_covers(env):
    """T-142 / T-141 r2: GET case carries `checks` computed from the case: a created case has only the code checks, a finished English case all four."""
    _, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    ch = c.get(f"/api/cases/{tok}").json()["checks"]
    assert ch["conflict_types"] == ["accident_date", "provider_name"] and {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "NOT_RUN", "denial_vs_history": "NOT_RUN"}
    tok = run_case(c)
    ch = c.get(f"/api/cases/{tok}").json()["checks"]
    assert ch["conflict_types"] == ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"] and ch["skipped"] == [] and ch["notes"] == []
    assert set(ch["labels"]) == set(ch["conflict_types"]) and all(ch["labels"].values())
    assert {"dosage", "laterality", "diagnosis"} <= {x["type"] for x in ch["not_checked"]} and all(x["label"] for x in ch["not_checked"])


def test_health_reports_local_mode_as_a_bool(env, monkeypatch):
    """T-197: health.local_mode mirrors ZLAYT_MODE=local, so the guided UI skips /api/cases and /api/library in public mode."""
    monkeypatch.setenv("ZLAYT_MODE", "local")
    assert env[1].get("/api/health").json()["local_mode"] is True
    monkeypatch.delenv("ZLAYT_MODE")
    assert env[1].get("/api/health").json()["local_mode"] is False
    monkeypatch.setenv("ZLAYT_MODE", "public")
    assert env[1].get("/api/health").json()["local_mode"] is False
