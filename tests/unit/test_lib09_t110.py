"""T-110 on the lib09 Spanish packet (fixture backend, no network): where the 4/7 comes from, a record with no AI output never vanishes
(could-not-verify tray with its reason), and POSSIBLE_OVERLAP warns next to the charge total instead of guessing (D-019)."""
import json
import pathlib
import tempfile

import pytest

from app.backend import ingest as IN, overlap as OV, pipeline as PL, present, review as RV, totals as T, trace
from app.db import db as DB
from app.llm import provider as P
from evals import run as R
from tests.unit._fakes import FakeCall

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
NAME = "case_lib09_spanish_interpreter_espalda"
TEXT = (LIB / f"{NAME}.txt").read_text()
EXPECTED = json.loads((LIB / f"{NAME}.expected.json").read_text())


@pytest.fixture(scope="module")
def lib09():
    return PL.run_case(TEXT, "fixture")


def _stored(wrap=None):
    """Run the fixture backend into a kept database; `wrap(call)` may replace the model call (to force a miss on one record)."""
    tmp = tempfile.TemporaryDirectory()
    with PL._Backend("fixture"):
        conn, cid, call = PL._scratch_call(tmp.name, IN.normalize_text(TEXT))
        PL.run_pipeline(conn, cid, TEXT, call=wrap(call) if wrap else call)
    return tmp, conn, cid


def _miss_on(*item_ids):
    def wrap(call):
        def c(step, system, user, schema, *, item_id=None):
            if item_id in item_ids:
                raise P.FixtureMiss("forced")
            return call(step, system, user, schema, item_id=item_id)
        return c
    return wrap


# ---------------------------------------------------------------- AC1: the 4/7
def test_every_lib09_record_has_an_entry_nothing_vanishes(lib09):
    """The '4/7' is the eval matcher, not a load failure: all seven records are entries (six dated, one date-to-confirm), no errors, nothing in the tray."""
    got = {n for e in lib09["entries"] + lib09["undated_entries"] for r in e["record_ids"] for n in [int(r[1:])]}
    assert got == set(range(1, 8)) and lib09["errors"] == [] and lib09["tray"] == [] and lib09["status"] == "done"
    assert len(lib09["entries"]) == 6 and [e["record_ids"] for e in lib09["undated_entries"]] == [["r4"]]


def test_spanish_records_are_held_for_review_not_verified(lib09):
    """D-050: records 2, 4 and 7 are Spanish, so their entries are needs_review with AI_TRANSLATION; the English ones are verified. The hold is not why the matcher misses."""
    by = {e["record_ids"][0]: e for e in lib09["entries"] + lib09["undated_entries"]}
    for r in ("r2", "r4", "r7"):
        assert by[r]["state"] == "needs_review" and "AI_TRANSLATION" in by[r]["reasons"]
    for r in ("r1", "r3", "r5", "r6"):
        assert by[r]["state"] == "verified" or by[r]["reasons"] == ["CHARGE_TEXT_IN_ENTRY"]      # T-139: an entry that states an amount is held for review, for that reason alone
        assert "AI_TRANSLATION" not in by[r]["reasons"]


def test_the_three_matcher_misses_are_sentences_the_recorded_extract_left_out(lib09):
    """E1 (mechanism sentence), E2 (chief complaint sentence) and E6 (pain 5/10) are present as entries, but the recorded generator answer quoted other
    sentences of the record. Pinned so a change in the cause (a re-recorded extract, a prompt change) is noticed."""
    s = R.score_entries(EXPECTED, lib09)
    assert {m["entry"] for m in s["misses"]} == {"E1", "E2", "E6"} and s["entry_count"] == 7
    by = {e["record_ids"][0]: e for e in lib09["entries"]}
    assert "struck by a car" not in by["r1"]["excerpt"] and "Motivo de consulta" not in by["r2"]["excerpt"] and "5/10" not in by["r6"]["excerpt"]
    rec = {r["id"]: r for r in lib09["records"]}
    assert "struck by a car" in rec["r1"]["excerpt"] and "Pain 5/10" in rec["r6"]["excerpt"]      # the words are in the record, so a paralegal can edit the quote


def test_failed_extract_record_is_a_tray_item_with_its_reason():
    """A record the extract step made no output for used to vanish (only the run error named it). It is now a rejected entry in the could-not-verify tray."""
    tmp, conn, cid = _stored(_miss_on("e6"))
    with tmp:
        view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
        tray = [t for t in view["tray"] if t["record_ids"] == ["r6"]]
        assert len(tray) == 1 and tray[0]["state"] == "rejected" and tray[0]["reasons"] == ["FIXTURE_MISS"] and tray[0]["why"]
        assert tray[0]["attempt"] == {"summary": None, "excerpt": None}
        shown = {r for e in view["entries"] + view["undated_entries"] + view["tray"] for r in e["record_ids"]}
        assert shown == {f"r{n}" for n in range(1, 8)}                 # every record is on screen somewhere
        assert not any("r6" in e["record_ids"] for e in view["entries"])   # and the placeholder is not on the timeline
        tr = trace.case_trace(conn, cid)
        ex = next(s for s in tr["steps"] if s["id"] == "extract")
        assert ex["status"] == "fail" and ex["counts"]["records_without_entry"] == 1 and ex["counts"]["in_tray"] == 1
        assert next(s for s in tr["steps"] if s["id"] == "grounding")["status"] != "fail"     # a failed call is not a grounding failure


def test_tray_placeholder_never_reaches_the_letter_and_manual_entry_still_works():
    tmp, conn, cid = _stored(_miss_on("e6"))
    with tmp:
        from app.backend import export as X, store
        assert "May 12, 2026" not in X.build_export(store.export_case(conn, cid))["letter_text"]
        r = RV.manual_entry(conn, cid, "r6", {"summary": "MRI reviewed.", "excerpt": "MRI reviewed."}, call=FakeCall({"j1": {"verdict": "supported", "reason_code": "NONE"}}))
        assert r["item"]["id"] == "e6_m" and r["item"]["review_status"] == "pending"
        ex = next(s for s in trace.case_trace(conn, cid)["steps"] if s["id"] == "extract")
        assert ex["counts"]["records_without_entry"] == 0


def test_rerun_after_a_miss_replaces_the_placeholder():
    """The placeholder is pending, so a later successful run removes it instead of leaving a stale tray row."""
    tmp, conn, cid = _stored(_miss_on("e6"))
    with tmp:
        with PL._Backend("fixture"):
            PL.run_pipeline(conn, cid, TEXT, call=PL.AU.make_call(conn, cid))
        view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
        assert view["tray"] == [] and any(e["record_ids"] == ["r6"] for e in view["entries"])


# ---------------------------------------------------------------- AC1: POSSIBLE_OVERLAP
def test_lib09_warns_about_the_consult_and_the_statement_line_and_leaves_the_total_alone():
    tmp, conn, cid = _stored()
    with tmp:
        tv = present.totals_view(conn, cid)
        w = tv["possible_overlaps"]
        assert [(x["code"], x["service"], x["statement_text"], x["covered_text"]) for x in w] == [("POSSIBLE_OVERLAP", "consult", "$1,300.00", "$650.00")]
        assert w[0]["range"] == {"from": None, "to": "2026-05-20", "stated": False} and w[0]["date_known"] is True and "does not merge" in w[0]["message"]
        before = {k: tv[k] for k in ("accepted", "pending", "detected_not_a_total")}
        assert OV.view(conn, cid) == w                                  # the warning is computed on read and changes nothing stored
        assert {k: present.totals_view(conn, cid)[k] for k in before} == before


def test_warning_names_no_pair_for_the_rate_figures_or_the_balance(lib09):
    """The $400 session rate appears in the note and in the statement, and the statement balance names no service: neither pairs with anything."""
    tmp, conn, cid = _stored()
    with tmp:
        ids = {(x["statement_amount_id"], x["covered_amount_id"]) for x in OV.view(conn, cid)}
        text = {a["id"]: a["text"] for a in DB.list_items(conn, cid, "amount")}
        assert {(text[s], text[c]) for s, c in ids} == {("$1,300.00", "$650.00")}


def test_total_still_sums_stated_charges_only_when_both_are_accepted():
    """Even with both figures accepted as charges the code adds what is stated (D-019) and warns: it never subtracts, merges or guesses."""
    amts = [dict(id="a2", cents=65000, cls="charge", review_status="accepted"), dict(id="a5", cents=130000, cls="charge", review_status="accepted"),
            dict(id="a1", cents=294000, cls="charge", review_status="accepted"), dict(id="a4", cents=215000, cls="charge", review_status="accepted")]
    assert T.totals(amts)["accepted_cents"] == 704000
    rows = [row("a2", "r2", 65000, "Consulta:", record_date="2026-04-14"), row("a5", "r7", 130000, "Estado de cuenta: consultas", statement=True, record_date="2026-05-20")]
    w = OV.possible_overlaps(rows)
    assert len(w) == 1 and w[0]["both_charges"] and w[0]["both_in_total"] is False       # pending here; accepted below
    for r in rows:
        r["review_status"] = "accepted"
    assert OV.possible_overlaps(rows)[0]["both_in_total"] is True


# ---------------------------------------------------------------- the pure rule
def row(id, rec, cents, label, kind="charge", statement=False, record_date="2026-04-14", after="", review_status="pending", excerpt=""):
    return {"id": id, "record_id": rec, "kind": kind, "value_cents": cents, "text": f"${cents // 100}.00", "review_status": review_status, "state": "needs_review",
            "label": label, "after": after, "statement": statement, "record_date": record_date, "record_excerpt": excerpt}


def test_english_statement_line_and_pt_note():
    w = OV.possible_overlaps([row("a1", "r1", 45000, "Physical therapy charge", record_date="2026-02-10"),
                              row("a2", "r2", 90000, "Statement: physical therapy", statement=True, record_date="2026-03-01")])
    assert [(x["statement_amount_id"], x["covered_amount_id"], x["service"]) for x in w] == [("a2", "a1", "physical_therapy")]


def test_different_service_never_pairs():
    assert OV.possible_overlaps([row("a1", "r1", 215000, "MRI charge"), row("a2", "r2", 130000, "Statement: consultations", statement=True, record_date="2026-05-20")]) == []


def test_charge_dated_after_the_statement_is_not_covered():
    assert OV.possible_overlaps([row("a1", "r1", 65000, "Consulta:", record_date="2026-06-01"),
                                 row("a2", "r2", 130000, "Estado de cuenta: consultas", statement=True, record_date="2026-05-20")]) == []


def test_stated_date_range_decides():
    ex = "Statement of account for services 2026-04-01 to 2026-04-30: consultations $1,300.00"
    s = row("a2", "r2", 130000, "Statement of account for services 2026-04-01 to 2026-04-30: consultations", statement=True, record_date="2026-05-20", excerpt=ex)
    inside = OV.possible_overlaps([row("a1", "r1", 65000, "Consult:", record_date="2026-04-14"), s])
    assert len(inside) == 1 and inside[0]["range"] == {"from": "2026-04-01", "to": "2026-04-30", "stated": True} and "stated date range" in inside[0]["message"]
    assert OV.possible_overlaps([row("a1", "r1", 65000, "Consult:", record_date="2026-03-14"), s]) == []        # before the range
    assert OV.possible_overlaps([row("a1", "r1", 65000, "Consult:", record_date="2026-05-10"), s]) == []        # after it, though before the statement was issued


def test_unconfirmed_charge_date_is_listed_not_ruled_out():
    w = OV.possible_overlaps([row("a1", "r1", 65000, "Consulta:", record_date=None),
                              row("a2", "r2", 130000, "Estado de cuenta: consultas", statement=True, record_date="2026-05-20")])
    assert len(w) == 1 and w[0]["date_known"] is False and "not confirmed" in w[0]["message"]


@pytest.mark.parametrize("change", [dict(kind="rate"), dict(review_status="dismissed"), dict(value_cents=None), dict(after=" por sesión"), dict(after=" per session")])
def test_a_rate_a_dismissed_or_unreadable_figure_is_never_a_party(change):
    other = {**row("a1", "r1", 65000, "Consulta:"), **change}
    assert OV.possible_overlaps([other, row("a2", "r2", 130000, "Estado de cuenta: consultas", statement=True, record_date="2026-05-20")]) == []


def test_statement_summary_lines_and_same_record_figures_never_pair():
    st = row("a2", "r2", 130000, "Saldo consultas", statement=True, record_date="2026-05-20")
    assert OV.possible_overlaps([row("a1", "r1", 65000, "Consulta:"), st]) == []
    same = row("a3", "r2", 65000, "Consulta:")
    assert OV.possible_overlaps([same, row("a2", "r2", 130000, "consultas", statement=True)]) == []


def test_no_arithmetic_in_the_module():
    src = pathlib.Path(OV.__file__).read_text()
    assert "float(" not in src and "sum(" not in src
