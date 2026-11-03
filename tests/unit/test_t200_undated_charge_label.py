"""T-200 (GATE-M2 r2 paralegal major): a counted ledger charge whose line states no date of service must not print the statement date as if it were a service date.
lib11's three ledger lines (statement date 06/15/2026, no date of service) were printed 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00', next to a
chronology that puts the clinic's visit on March 27. The letter now says 'itemized ledger, date of service [__________] (record dated June 15, 2026)'. A charge that states
its own date (the ED charge, a dated ledger line, an encounter note) keeps its date line. Code only."""
import re

import pytest

from app.backend import export, store
from tests.unit.test_t171_count_charge import LEDGER, SRC, by_text, client, count, lib11, run_case  # noqa: F401  (fixtures)

BARE = re.compile(r"itemized ledger, [A-Z][a-z]+ \d{1,2}, \d{4}: \$")
STATEMENT = "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): "


def _letter(c, tok, style=None):
    for it in c.get(f"/api/cases/{tok}").json()["entries"]:
        c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
    return c.get(f"/api/cases/{tok}/export", params={"style": style} if style else {}).json()["letter_text"]


@pytest.mark.parametrize("style", [None, "oneline"])
def test_lib11_counted_ledger_lines_are_labelled_with_the_statement_date(lib11, style):
    c, tok = lib11
    am = by_text(c, tok)
    ed = next(a for a in am.values() if a["kind"] == "charge")
    assert c.post(f"/api/cases/{tok}/items/{ed['id']}/review", json={"action": "accept"}).status_code == 200
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        assert count(c, tok, am[fig]["id"], confirm="separate_charge").status_code == 200
    lines = _letter(c, tok, style).split("\n")
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        assert STATEMENT + fig in lines, (fig, [l for l in lines if fig in l])
    assert not any(BARE.search(l) for l in lines), [l for l in lines if BARE.search(l)]          # no bare statement date in the charge section
    assert "Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00" in lines          # D-073: an ED provider name is not a document type, so no record date
    assert "Billed charges accepted from these records: $6,000.00" in lines
    assert "March 27, 2026" in "\n".join(lines)                                                  # the visit date the old line contradicted is still in the chronology


def test_a_counted_line_keeps_its_citation_and_quote(lib11):
    c, tok = lib11
    a = by_text(c, tok)["$250.00"]
    assert count(c, tok, a["id"], confirm="separate_charge").status_code == 200
    lines = _letter(c, tok).split("\n")
    i = lines.index(STATEMENT + "$250.00")
    assert lines[i + 1].startswith("Source [Ex. __ / Bates __]: ") and "New patient exam charge $250.00" in lines[i + 1]


def test_charge_service_dates_never_carries_a_date_d073_fallback():
    rec = {"source": SRC, "date_iso": "2026-06-15"}
    pos = LEDGER.index("$250.00")
    assert store.charge_service_dates({"excerpt": LEDGER, "value_cents": 25000}, rec, pos) == (None, None)
    dated = "Itemized ledger, statement date 06/15/2026. DOS 03/27/2026 New patient exam charge $250.00."
    assert store.charge_service_dates({"excerpt": dated, "value_cents": 25000}, rec, dated.index("$250.00")) == (None, None)          # D-073: a sentence is not read
    table = "Itemized ledger.\nDOS\tService\tCharge\n03/27/2026\tNew patient exam\t$250.00\n01/02/2026\toffice visit\tno charge\n"
    assert store.charge_service_dates({"excerpt": table, "value_cents": 25000}, rec, table.index("$250.00")) == (None, None)          # D-073 fallback: even its own row's DOS cell is not read
    note_rec = {"source": "Fennimoor Spine Clinic, progress note", "date_iso": "2026-03-27"}
    note = "Exam charge $250.00."
    assert store.charge_service_dates({"excerpt": note, "value_cents": 25000}, note_rec, note.index("$250.00")) == (None, None)      # D-073 fallback: not even a dated encounter note lends its date


def test_charge_service_dates_when_the_line_cannot_be_read():
    from app.backend import amounts as AM
    counted = {"excerpt": "x", "ladder": {"counted": {"not_counted_reason": AM.NO_DATE_WHY}}}
    assert store.charge_service_dates(counted, {"source": "s", "date_iso": "2026-06-15"}, None) == (None, None)
    assert store.charge_service_dates({"excerpt": "x"}, {"source": "Capital PT, visit 9", "date_iso": "2026-06-15"}, None) == (None, None)          # T-207 r2 F3: an unlocated figure prints the blank, even in an encounter record
    assert store.charge_service_dates({"excerpt": "x"}, {"source": "s", "date_iso": "2026-06-15"}, None) == (None, None)          # D-071 amendment 2: a record of unknown type never lends its date


def _case(**charge):
    return {"records": [{"n": 1, "source": "Fennimoor Spine Clinic, itemized ledger", "date_iso": "2026-06-15", "excerpt": "New patient exam charge $250.00."}],
            "entries": [], "flags": [], "pending_count": 0, "events": [],
            "amounts": [dict(id="a1", record_no=1, cents=25000, cls="charge", raw="$250.00", excerpt="New patient exam charge $250.00.", review_status="accepted", **charge)]}


def test_export_label_rules_on_a_hand_built_case():
    def line(**ch):
        return next(l for l in export.build_export(_case(**ch), None)["letter_text"].split("\n") if l.endswith("$250.00"))
    assert line(dos_iso=None, dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $250.00"
    blank = "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $250.00"
    assert line(dos_iso="2026-03-27", dos_end_iso=None) == blank          # D-073 fallback: a hand-built case's date is not printed either
    assert line(dos_iso="2026-06-09", dos_end_iso="2026-06-12") == blank
    assert line() == blank
    c = _case(dos_iso=None, dos_end_iso=None)
    c["records"][0]["date_iso"] = None
    assert next(l for l in export.build_export(c, None)["letter_text"].split("\n") if l.endswith("$250.00")) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________]: $250.00"
