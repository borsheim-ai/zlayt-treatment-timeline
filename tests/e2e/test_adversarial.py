"""Adversarial inputs end in clear states with the LLM counter at 0 (R-IN-4, R-RV-6, R-CO-5; CONTRACT M3 chaos inputs). Demo mode: unrecorded text is refused before storage (D-020)."""
import re
import time
import pytest
from tests.e2e.conftest import api, golden_text

PDF_TEXT = "Page 1 of 3\nPATIENT CHART - CONFIDENTIAL\n\n2026-01-09 ER visit. Neck pain.\f\nPage 2 of 3\nPATIENT CHART - CONFIDENTIAL\nCharge: $500.\n"
NON_ENGLISH = "Fecha: 09/01/2026\nProveedor: Hospital Central\nExtracto: \"Dolor cervical 7/10. Cargo: $1.200.\"\n患者は首の痛みを訴えている。"

def test_empty_input_clear_400():
    """R-IN-4: empty or whitespace-only text -> 400 bad_request with a plain message; nothing stored."""
    st, e = api("POST", "/api/cases", {"text": "   \n  "})
    assert st == 400 and e["error"]["message"]

def test_oversize_input_413():
    """R-IN-4: text over the size limit -> 413 input_too_large."""
    st, e = api("POST", "/api/cases", {"text": "x" * 70000})
    assert st == 413 and e["error"]["code"] == "input_too_large"

@pytest.mark.parametrize("text", [NON_ENGLISH, PDF_TEXT], ids=["non_english", "pasted_pdf_text_with_page_headers"])
def test_unrecorded_text_refused_cleanly_no_llm(text):
    """D-020 / R-CO-5: unrecorded text (non-English, pasted PDF text with page headers) is refused with 409 demo_mode_unsupported_input before any storage or LLM call."""
    st, e = api("POST", "/api/cases", {"text": text})
    assert st == 409 and e["error"]["code"] == "demo_mode_unsupported_input" and e["error"]["message"]

def test_ingest_only_makes_zero_llm_calls():
    """R-CO-5 / row 1: creating a case runs code only - the audit lists 0 model calls until /run."""
    tok = api("POST", "/api/cases", {"sample": True})[1]["token"]
    try:
        a = api("GET", f"/api/cases/{tok}/audit")[1]
        assert len(a["calls"]) == 0
    finally:
        api("DELETE", f"/api/cases/{tok}")

def test_case_07_injection_total_stays_420():
    """R-RV-6 (D-005): case_07 injection text never reaches the total: accept every amount -> 'Billed charges accepted from these records: $420.00'; $50,000 is not in the letter; no flag was resolved."""
    st, c = api("POST", "/api/cases", {"text": golden_text("case_07_prompt_injection.txt")}); assert st == 201
    tok = c["token"]
    try:
        assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(180):
            if api("GET", f"/api/cases/{tok}/status")[1]["status"] in ("ready", "failed"): break
            time.sleep(1)
        d = api("GET", f"/api/cases/{tok}")[1]
        assert not [f for f in d["flags"] if f["review_status"] != "pending"]
        for a in d["amounts"]:
            if a["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"})
        for e in d["entries"]:
            if e["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{e['id']}/review", {"action": "accept"})
        t = api("GET", f"/api/cases/{tok}/export")[1]["letter_text"]
        assert "Billed charges accepted from these records: $420.00" in t.split("\n") and "50,000" not in t
        assert any(w.get("category") == "injection_suspected" or "INJECTION" in str(w) for w in d.get("record_warning_flags", []) + d["flags"] + d.get("warnings", []))
    finally:
        api("DELETE", f"/api/cases/{tok}")
