"""GET /api/cases/{token}/export through the router with a fake case loader (T-041 AC4, row 19). No DB, no LLM."""
import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.backend import export_routes as R
from tests.unit.test_export import build_case


def _client(case):
    R.set_case_loader(lambda t: case if t == "tok" else None)
    app = FastAPI()
    app.include_router(R.router)
    return TestClient(app)


def test_export_endpoint():
    c = build_case()
    for e in c["entries"]:
        if e["record_no"] == 5:
            e["review_status"] = "dismissed"
        if e["record_no"] == 6:
            e["review_status"] = "pending"
    for a in c["amounts"]:
        if a["id"] == "A1":
            a["review_status"] = "pending"
    cl = _client(c)
    r = cl.get("/api/cases/tok/export")
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j["letter_text"], str) and isinstance(j["internal_notes_text"], str)
    assert j["letter_text"] != j["internal_notes_text"] and "INTERNAL REVIEW NOTES" not in j["letter_text"]
    assert "AI assistance" not in j["letter_text"] and "AI assistance" in j["internal_notes_text"]
    for gone in ("February 20, 2026", "March 6, 2026", "$6,240.00"):
        assert gone not in j["letter_text"]
    assert "Billed charges accepted from these records: $2,150.00" in j["letter_text"].split("\n")
    assert {e["id"] for e in j["items"]["entries"]} == {f"e{n}" for n in (1, 2, 3, 4, 7, 8, 9)}
    assert "A1" not in {a["id"] for a in j["items"]["amounts"]}
    assert cl.get("/api/cases/nope/export").status_code == 404
    assert cl.get("/api/cases/nope/export").json()["error"]["code"] == "not_found"
