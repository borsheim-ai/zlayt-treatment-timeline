"""T-139 r3 (staff review major 2): when code shortens the model's quote (charge_text.narrow_excerpt) or strips a summary clause that states an amount (generation
time or the quote-picker edit), the item trace serves a code step that says what was removed (verbatim), why, and the before and after text. The letter never shows it."""
import pytest

from app.backend import charge_text as CT
from tests.unit.test_t139_charge_text import LIB01, _accept_all, _lib_client, _post
from tests.unit.test_t139_charge_text import env  # noqa: F401  (fixture: lib01 with narrowing off, so e2 is held out and the quote picker applies)


def _steps(c, tok, item):
    tr = c.get(f"/api/cases/{tok}/items/{item}/trace")
    assert tr.status_code == 200
    return {s["id"]: s for s in tr.json()["steps"]}, [s["id"] for s in tr.json()["steps"]]


@pytest.fixture
def narrowed(tmp_path, monkeypatch):
    return _lib_client(tmp_path, monkeypatch, LIB01)


def test_narrowed_quote_step_names_the_removed_sentence_why_and_before_after(narrowed):
    c, tok = narrowed
    st, order = _steps(c, tok, "e2")
    s = st["excerpt_narrowed"]
    assert s["kind"] == "code" and s["status"] == "pass" and s["rule"] == "T-139" and s["blocks_export"] is False
    ev = s["evidence"]
    assert ev["removed"] == ["ED charge: $3,915."]                                          # verbatim
    assert ev["quote_before"].endswith("in 1 week. ED charge: $3,915.") and ev["quote_after"].endswith("in 1 week.") and "$" not in ev["quote_after"]
    assert ev["summary_before"].endswith("ED charge $3,915.") and "$" not in ev["summary_after"]
    assert "ED charge: $3,915." in s["why"] and "never in the letter" in s["why"] and "Billed charges" in s["why"]
    assert order.index("excerpt_narrowed") == order.index("extracted") + 1                  # right after the AI step it changed


def test_summary_clause_step_names_the_removed_clause_and_before_after(narrowed):
    c, tok = narrowed
    st, order = _steps(c, tok, "e2")
    s = st["charge_clause_removed"]
    assert s["kind"] == "code" and s["status"] == "pass" and s["rule"] == "T-139"
    ev = s["evidence"]
    assert ev["removed"] == ["ED charge $3,915"] and "$" not in ev["summary_after"] and ev["summary_before"].endswith("ED charge $3,915.")
    assert "ED charge $3,915" in s["why"] and "never in the letter" in s["why"]
    assert order.index("charge_clause_removed") > order.index("excerpt_narrowed")


def test_e4_names_its_charge_sentence_and_clause(narrowed):
    c, tok = narrowed
    st, _ = _steps(c, tok, "e4")
    assert st["excerpt_narrowed"]["evidence"]["removed"] == ["Charge per visit $140."]
    assert st["charge_clause_removed"]["evidence"]["removed"] == ["Charge per visit $140"]


def test_item_payload_carries_the_same_record(narrowed):
    c, tok = narrowed
    nar = c.get(f"/api/cases/{tok}/items/e2").json()["item"]["ladder"]["excerpt_narrowed"]
    assert nar["dropped"] == ["ED charge: $3,915."] and nar["original_excerpt"].endswith("$3,915.") and nar["summary_removed"] == ["ED charge $3,915"]
    assert nar["summary_before_charge_trim"].endswith("ED charge $3,915.")            # the text the amount clause was removed from


def test_an_untouched_entry_has_neither_step(narrowed):
    c, tok = narrowed
    st, _ = _steps(c, tok, "e1")
    assert "excerpt_narrowed" not in st and "charge_clause_removed" not in st


def test_the_trace_text_never_reaches_the_letter_or_the_notes(narrowed):
    c, tok = narrowed
    assert _accept_all(c, tok) == {}
    j = c.get(f"/api/cases/{tok}/export").json()
    letter = j["letter_text"]
    assert "Code removed" not in letter and "code removed" not in j["internal_notes_text"].lower()
    assert "ED charge" not in letter.split("BILLED CHARGES")[0] and "$3,915" not in letter.split("BILLED CHARGES")[0]


def test_the_step_comes_from_the_ladder_record_alone(narrowed):
    """Hiding the ladder record removes the step, so the assertions above pin the step to what generation stored."""
    from app.backend import trace as TR
    assert TR._narrow_steps({}, {"excerpt": "x", "summary": "y"}) == []
    got = TR._narrow_steps({"excerpt_narrowed": {"dropped": ["Fee $5."], "original_excerpt": "A b. Fee $5.", "original_summary": "A b; fee $5."}}, {"excerpt": "A b.", "summary": "A b."})
    assert [x["id"] for x in got] == ["excerpt_narrowed"] and got[0]["evidence"]["removed"] == ["Fee $5."]


# ---- the quote-picker edit: code strips the trailing amount clause from the AI summary; the trace shows it
def test_edit_time_clause_removal_is_in_the_trace(env):  # noqa: F811
    c, tok = env
    quote = "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week."
    r = _post(c, tok, "e2", {"action": "edit", "edits": {"excerpt": quote}})
    assert r.status_code == 200, r.json()
    st, order = _steps(c, tok, "e2")
    s = st["charge_clause_removed"]
    assert s["kind"] == "code" and s["rule"] == "T-139" and s["status"] == "pass"
    ev = s["evidence"]
    assert ev["removed"] and all("$3,915" in x for x in ev["removed"])
    assert "$3,915" in ev["summary_before"] and "$" not in ev["summary_after"]
    assert ev["quote_before"].endswith("$3,915.") and ev["quote_after"] == quote
    assert "excerpt_narrowed" not in st                                                # narrowing was off: only the edit-time trim happened
    assert order.index("charge_clause_removed") == order.index("extracted") + 1


def test_a_later_hand_edit_of_the_summary_drops_the_stale_edit_trim_step(env):  # noqa: F811
    c, tok = env
    quote = "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week."
    assert _post(c, tok, "e2", {"action": "edit", "edits": {"excerpt": quote}}).status_code == 200
    assert _post(c, tok, "e2", {"action": "edit", "edits": {"summary": "Cervical strain; X-ray negative for fracture; ibuprofen 600 mg."}}).status_code == 200
    st, _ = _steps(c, tok, "e2")
    assert "charge_clause_removed" not in st


def test_reset_removes_the_edit_time_step(env):  # noqa: F811
    c, tok = env
    quote = "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week."
    assert _post(c, tok, "e2", {"action": "edit", "edits": {"excerpt": quote}}).status_code == 200
    assert _post(c, tok, "e2", {"action": "reset"}).status_code == 200
    st, _ = _steps(c, tok, "e2")
    assert "charge_clause_removed" not in st
