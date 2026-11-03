"""T-086 round 2 (security review): OCR_DERIVED survives every later step. An item read from a scanned page stays needs_review with reason
OCR_DERIVED after an edit, a manual entry, a not-a-duplicate split, a reclassify and a re-judge; a human edit never makes it verified.
SYNTHETIC text only."""
import pytest

from app.backend import confidence, pipeline as PL, rejudge, review as RV
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script

SUPPORTED = {"j1": {"verdict": "supported", "reason_code": "NONE"}}


def _case(tmp_path, source="ocr"):
    raw = G.raw("sample")
    conn = DB.connect(str(tmp_path / f"{source}.sqlite"))
    page = {"page": 1, "start": 0, "end": len(raw), **({"source": source} if source else {})}
    cid = DB.create_case(conn, raw, now=1.0, config_json={"source_pdf": True, "pages": [page]})
    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)
    return conn, cid, out


def _live_entry(out):
    return next(e for e in out["entries"] if e["state"] != "rejected")


def _stored(conn, cid, item_id):
    for k in ("entry", "amount", "flag"):
        for r in DB.list_items(conn, cid, k):
            if r["id"] == item_id:
                return r


def test_compose_state_takes_ocr_derived_as_context():
    assert confidence.compose_state({"judge": "supported"}, {"ocr_derived": True}) == ("needs_review", ["OCR_DERIVED"])
    assert confidence.compose_state({"judge": "supported"}, {"ocr_derived": False}) == ("verified", [])


def test_editing_an_ocr_item_keeps_needs_review_and_the_ocr_reason(tmp_path):
    conn, cid, out = _case(tmp_path)
    e = _live_entry(out)
    assert e["state"] == "needs_review" and "OCR_DERIVED" in e["reasons"]
    r = RV.apply_review(conn, cid, e["id"], dict(action="edit", edits={"summary": e["summary"].rstrip(".") + " (checked)."}), call=FakeCall(SUPPORTED))
    assert r["item"]["state"] == "needs_review" and "OCR_DERIVED" in r["item"]["reasons"]
    row = _stored(conn, cid, e["id"])
    assert row["state"] == "needs_review" and "OCR_DERIVED" in row["state_reasons"]
    assert row["ladder"]["state"] == "needs_review"


def test_a_second_edit_and_an_accept_still_leave_the_ocr_reason(tmp_path):
    conn, cid, out = _case(tmp_path)
    e = _live_entry(out)
    for suffix in (" (one).", " (two).", " (three)."):
        RV.apply_review(conn, cid, e["id"], dict(action="edit", edits={"summary": e["summary"].rstrip(".") + suffix}), call=FakeCall(SUPPORTED))
    RV.apply_review(conn, cid, e["id"], dict(action="accept"))
    row = _stored(conn, cid, e["id"])
    assert row["state"] == "needs_review" and "OCR_DERIVED" in row["state_reasons"]


def test_an_edit_with_no_judge_available_also_keeps_the_ocr_reason(tmp_path):
    conn, cid, out = _case(tmp_path)
    e = _live_entry(out)
    RV.apply_review(conn, cid, e["id"], dict(action="edit", edits={"summary": e["summary"].rstrip(".") + " (checked)."}), call=None)
    row = _stored(conn, cid, e["id"])
    assert row["state"] == "needs_review" and "OCR_DERIVED" in row["state_reasons"]


def test_a_text_layer_case_still_verifies_after_an_edit(tmp_path):
    conn, cid, out = _case(tmp_path, source=None)
    e = next(e for e in out["entries"] if e["state"] == "verified")
    r = RV.apply_review(conn, cid, e["id"], dict(action="edit", edits={"summary": e["summary"].rstrip(".") + " (checked)."}), call=FakeCall(SUPPORTED))
    assert r["item"]["state"] == "verified" and "OCR_DERIVED" not in r["item"]["reasons"]


def test_manual_entry_on_an_ocr_record_is_needs_review_with_the_ocr_reason(tmp_path):
    from app.backend import store
    conn, cid, out = _case(tmp_path)
    e = _live_entry(out)
    DB.update_item(conn, e["id"], now=2.0, case=cid, state="rejected")          # the AI's entry failed; the paralegal writes her own
    rec_id = e["record_ids"][0]
    rec = next(r for r in store.load_records(conn, cid) if r["id"] == rec_id)
    quote = e["excerpt"]
    r = RV.manual_entry(conn, cid, rec_id, {"summary": quote, "excerpt": quote}, call=FakeCall(SUPPORTED))
    assert r["item"]["state"] == "needs_review" and "OCR_DERIVED" in r["item"]["reasons"], rec["excerpt"]


def test_enforce_ocr_repairs_any_item_that_lost_the_reason(tmp_path):
    conn, cid, out = _case(tmp_path)
    e = _live_entry(out)
    DB.update_item(conn, e["id"], now=2.0, case=cid, state="verified", state_reasons_json=[])
    assert RV.enforce_ocr(conn, cid, 3.0) >= 1
    row = _stored(conn, cid, e["id"])
    assert row["state"] == "needs_review" and row["state_reasons"] == ["OCR_DERIVED"]
    assert RV.enforce_ocr(conn, cid, 4.0) == 0                                  # idempotent


def test_enforce_ocr_never_touches_rejected_items_or_text_cases(tmp_path):
    conn, cid, out = _case(tmp_path)
    rejected = [e for e in out["entries"] if e["state"] == "rejected"]
    RV.enforce_ocr(conn, cid, 2.0)
    for e in rejected:
        assert _stored(conn, cid, e["id"])["state"] == "rejected"
    conn2, cid2, _ = _case(tmp_path, source=None)
    assert RV.enforce_ocr(conn2, cid2, 2.0) == 0


def test_rejudge_keeps_the_ocr_reason():
    row = {"state_reasons": ["OCR_DERIVED"]}
    state, reasons = rejudge.recompose(row, "supported")
    assert state == "needs_review" and reasons == ["OCR_DERIVED"]
