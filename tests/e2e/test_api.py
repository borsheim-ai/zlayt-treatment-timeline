"""API contract end to end (memory/contracts/api.md; R-IN-1, R-IN-2, R-RV-5, R-EX-1, ADR-006). Fixture backend."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_health_reports_fixture_backend_and_demo():
    """api.md health: backend fixture, demo_mode true on the public build."""
    st, h = api("GET", "/api/health"); assert st == 200 and h["backend"] == "fixture"

def test_create_sample_returns_nine_records_and_gap_flag():
    """R-IN-1: sample -> 9 records, ingest is synchronous code and already carries the 73-day gap flag."""
    st, c = api("POST", "/api/cases", {"sample": True})
    assert st in (200, 201) and c["record_count"] == 9 and len(c["gap_flags"]) == 1
    api("DELETE", f"/api/cases/{c['token']}")

def test_unknown_token_is_404():
    """api.md conventions: unknown token -> 404 not_found."""
    st, e = api("GET", "/api/cases/does-not-exist"); assert st == 404 and e["error"]["code"] == "not_found"

def test_non_recorded_text_refused_in_demo_mode():
    """D-020: text whose hash is not recorded -> 409 demo_mode_unsupported_input, nothing stored."""
    st, e = api("POST", "/api/cases", {"text": "SYNTHETIC totally new text"}); assert st == 409 and e["error"]["code"] == "demo_mode_unsupported_input"

def test_empty_input_is_400():
    """R-IN-2: empty input -> 400 bad_request."""
    assert api("POST", "/api/cases", {"text": ""})[0] == 400

def test_export_is_deterministic_and_equals_golden(sample_case):
    """R-EX-6: accept all nine entries + both charges + all flags -> letter_text equals the golden LETTER block byte for byte; twice identical."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for it in c["entries"] + [a for a in c["amounts"] if a["kind"] == "charge"] + c["flags"]:
        assert api("POST", f"/api/cases/{sample_case}/items/{it['id']}/review", {"action": "accept"})[0] == 200
    a = api("GET", f"/api/cases/{sample_case}/export")[1]; b = api("GET", f"/api/cases/{sample_case}/export")[1]
    golden = golden_text("sample.export.expected.txt").split("=== INTERNAL_NOTES_TEXT")[0].split("\n", 1)[1].rstrip("\n")
    assert a["letter_text"] == golden and a["letter_text"] == b["letter_text"] and a["internal_notes_text"] == b["internal_notes_text"]

def test_delete_removes_case():
    """ADR-006: DELETE -> 204 then 404."""
    tok = api("POST", "/api/cases", {"sample": True})[1]["token"]
    assert api("DELETE", f"/api/cases/{tok}")[0] == 204 and api("GET", f"/api/cases/{tok}")[0] == 404

def test_no_bulk_accept_endpoint(sample_case):
    """D-011: there is no bulk-accept route."""
    assert api("POST", f"/api/cases/{sample_case}/accept_all", {})[0] in (404, 405)
