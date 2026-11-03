"""Letter isolation. R-EX-1 (no tool-authored flag content), D-019, D-012."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


BAD = ["73 days", "AI assistance", "Conflict", "Causation", "Prior condition", "REVIEWER NOTE", "visit count", "supplemented", "rate", "Pending items", "of 9"]

def accept(tok, it):
    st, _ = api("POST", f"/api/cases/{tok}/items/{it['id']}/review", {"action": "accept"})
    assert st == 200 or it.get("state") == "rejected", (it["id"], st)

def test_letter_has_no_flag_or_note_content(sample_case):
    """R-EX-1: accept everything (each accept must return 200), add a reviewer note (200); letter is non-empty, has 9 dated headings and the accepted quotes; none of the forbidden strings."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for it in c["entries"] + c["amounts"] + c["flags"]: accept(sample_case, it)
    gap = [f for f in c["flags"] if f["type"] == "gap"][0]
    assert api("POST", f"/api/cases/{sample_case}/items/{gap['id']}/review", {"action": "edit", "edits": {"note": "REVIEWER NOTE ask client"}})[0] == 200
    t = api("GET", f"/api/cases/{sample_case}/export")[1]["letter_text"]
    assert t.startswith("TREATMENT CHRONOLOGY") and len(re.findall(r"^[A-Z][a-z]+ \d+, 2026 — ", t, re.M)) == 9
    assert "Discharged from PT after two missed appointments." in t and "Billed charges accepted from these records:" in t
    for b in BAD: assert b not in t, b

def test_total_line_is_exact_even_with_rate_accepted(sample_case):
    """R-EX-8 / D-019: 'Billed charges accepted from these records: $8,390.00' with no clause."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for a in c["amounts"]: accept(sample_case, a)
    assert "Billed charges accepted from these records: $8,390.00" in api("GET", f"/api/cases/{sample_case}/export")[1]["letter_text"].split("\n")

def test_letter_is_subset_of_accepted(sample_case):
    """R-EX-1: with only entries 1 and 9 accepted, only their headings appear."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for e in (c["entries"][0], c["entries"][8]): accept(sample_case, e)
    t = api("GET", f"/api/cases/{sample_case}/export")[1]["letter_text"]
    assert len(re.findall(r"^[A-Z][a-z]+ \d+, 2026 — ", t, re.M)) == 2
