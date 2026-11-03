"""T-110 r2 on lib09 (fixture backend, no network): Spanish cues let a paralegal reclassify an unclear figure to a charge through the T-084 guard, a rate
never becomes one, possible overlaps reach the internal notes (never the letter), and a hand-entered record leaves the tray."""
import pytest

from app.backend import amounts as A, export as X, present, reclassify as RC, review as RV, store
from app.db import db as DB
from tests.unit._fakes import FakeCall
from tests.unit.test_lib09_t110 import _stored, _miss_on, TEXT

J2 = lambda v, code="NONE": {"j2": {"verdict": v, "reason_code": code}}     # noqa: E731


def _by_text(conn, cid):
    out = {}
    for a in DB.list_items(conn, cid, "amount"):
        out.setdefault(a["text"], []).append(a)
    return out


# ---------------------------------------------------------------- the shared cues
@pytest.mark.parametrize("text", ["Costo por sesión de terapia: $400.00", "4 sesiones a $400.00 por sesion", "$90 por visita", "$50 cada sesión", "$50 cada uno", "$50 por hora"])
def test_spanish_rate_cues_are_rate_cues_and_the_classifier_calls_the_figure_a_rate(text):
    assert A.has_rate_cue(text)
    amt = A.find_amounts(text)[0]
    assert A.classify(text, amt) == "rate"


@pytest.mark.parametrize("text", ["Cargo por factura 4471: $400", "Honorarios: $650", "Consulta: $650.00"])
def test_spanish_charge_words_are_not_rate_cues(text):
    assert not A.has_rate_cue(text)


def test_charge_cue_es_and_balance_cue():
    assert A.charge_cue_es("Cargos: $1,300.00") == "Cargos" and A.charge_cue_es("Honorarios del médico $650") == "Honorarios"
    assert A.charge_cue_es("Estado de cuenta: consultas $1,300.00;") == "Estado de cuenta: consultas"
    assert A.charge_cue_es("Sin cargo: $0") is None and A.charge_cue_es("Saldo de cargos: $2,900") is None and A.charge_cue_es("Consulta: $650") is None
    assert A.BALANCE_CUE.search("Saldo: $2,900.00") and not A.BALANCE_CUE.search("Cargos: $1,300")


# ---------------------------------------------------------------- lib09 through the T-084 guard
def test_lib09_consultas_line_can_be_reclassified_to_a_charge_and_counts_in_the_total():
    tmp, conn, cid = _stored()
    with tmp:
        a5 = _by_text(conn, cid)["$1,300.00"][0]
        assert a5["kind"] == "unclear"
        call = FakeCall(J2("agree"))
        r = RC.reclassify(conn, cid, a5["id"], {"to": "charge"}, call=call, now=5.0)
        assert r["amount"]["kind"] == "charge" and r["reclassified"]["wording"].lower() == "estado de cuenta: consultas" and r["reclassified"]["judge_verdict"] == "agree"
        assert len(call.log) == 1 and r["item"]["review_status"] == "pending"
        for aid in (a5["id"],):
            RV.apply_review(conn, cid, aid, {"action": "accept"})
        t = present.totals_view(conn, cid)
        assert t["accepted"]["cents"] == 130000 and t["accepted"]["count"] == 1               # D-019 counts it once accepted


def test_lib09_consultas_reclassification_still_needs_the_judge():
    tmp, conn, cid = _stored()
    with tmp:
        a5 = _by_text(conn, cid)["$1,300.00"][0]
        with pytest.raises(RV.ReviewError) as e:
            RC.reclassify(conn, cid, a5["id"], {"to": "charge"}, call=FakeCall(J2("disagree", "SHOULD_BE_ESTIMATE")))
        assert e.value.detail["reason"] == "JUDGE_DISAGREES" and DB.get_item(conn, a5["id"], cid)["kind"] == "unclear"


def test_lib09_rate_per_session_is_refused_and_never_asks_the_judge():
    tmp, conn, cid = _stored()
    with tmp:
        for a in _by_text(conn, cid)["$400.00"]:
            call = FakeCall(J2("agree"))
            with pytest.raises(RV.ReviewError) as e:
                RC.reclassify(conn, cid, a["id"], {"to": "charge"}, call=call)
            assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
            assert call.log == [] and DB.get_item(conn, a["id"], cid)["kind"] in ("rate", "unclear")


def test_lib09_saldo_is_never_a_charge():
    tmp, conn, cid = _stored()
    with tmp:
        saldo = _by_text(conn, cid)["$2,900.00"][0]
        with pytest.raises(RV.ReviewError) as e:
            RC.reclassify(conn, cid, saldo["id"], {"to": "charge"}, call=FakeCall(J2("agree")))
        assert e.value.detail["reason"] == "NO_CHARGE_WORDING"


def test_a_saldo_in_the_same_sentence_as_a_charge_word_is_refused():
    row = {"text": "$2,900.00"}
    assert RC.charge_wording("Cargos, saldo: $2,900.00.", row) is None
    assert RC.charge_wording("Saldo: $2,900.00.", row) is None
    assert RC.charge_wording("Honorarios: $2,900.00.", row) == "Honorarios"
    assert RC.charge_wording("Sin cargo: $2,900.00.", row) is None
    assert RC.charge_wording("Honorarios $90 por sesión: $90.00.", {"text": "$90.00"}) is None


# ---------------------------------------------------------------- export: overlap in the internal notes only
def test_overlap_is_in_the_internal_notes_and_not_in_the_letter():
    tmp, conn, cid = _stored()
    with tmp:
        a = _by_text(conn, cid)
        for t in ("$2,940", "$2,150"):
            RV.apply_review(conn, cid, a[t][0]["id"], {"action": "accept"})
        case = store.export_case(conn, cid)
        [o] = case["possible_overlaps"]
        assert (o["statement_record_no"], o["covered_record_no"], o["service"]) == (7, 2, "consult")
        ex = X.build_export(case)
        notes, letter = ex["internal_notes_text"], ex["letter_text"]
        assert "POSSIBLE OVERLAPS (check before relying on the charges total)" in notes and "Possible overlap: record 7" in notes
        assert "$1,300.00" in notes and "record 2" in notes and "$650.00" in notes and "consult" in notes
        assert "The total does not currently add both figures" in notes
        assert "overlap" not in letter.lower() and "Billed charges accepted from these records: $5,090.00" in letter       # D-019: the letter and its total are untouched


def test_overlap_line_says_when_both_figures_are_in_the_total():
    tmp, conn, cid = _stored()
    with tmp:
        RV.apply_review(conn, cid, _by_text(conn, cid)["$2,940"][0]["id"], {"action": "accept"})
        case = store.export_case(conn, cid)
        case["possible_overlaps"][0]["both_in_total"] = True
        notes = X.build_export(case)["internal_notes_text"]
        assert "Both figures are in the charges total, so this service may be counted twice" in notes
        case["possible_overlaps"] = []
        assert "POSSIBLE OVERLAPS" not in X.build_export(case)["internal_notes_text"]            # no overlap: the notes are as before


# ---------------------------------------------------------------- the tray placeholder leaves once the paralegal enters the record by hand
def test_placeholder_leaves_the_tray_when_a_manual_entry_exists():
    tmp, conn, cid = _stored(_miss_on("e6"))
    with tmp:
        rid = "r6"
        assert [t["id"] for t in present.case_view(conn, cid, backend="fixture", models={}, demo_mode=True)["tray"]] == ["e6"]
        rejected_before = present.review_view(conn, cid)["counts"]["rejected"]
        assert rejected_before == 1 and present.rejected_count(conn, cid) == 1
        quote = "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."
        RV.manual_entry(conn, cid, rid, {"summary": "MRI reviewed; physical therapy and injection recommended; pain 5/10.", "excerpt": quote}, call=FakeCall(J2("agree")))
        view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=True)
        assert view["tray"] == [] and present.review_view(conn, cid)["counts"]["rejected"] == 0 and present.rejected_count(conn, cid) == 0
        assert DB.get_item(conn, "e6", cid)["state"] == "rejected"                          # the placeholder row stays for audit
        assert any(e["id"] == "e6_m" for e in view["entries"])


# ---------------------------------------------------------------- T-110 r3: payment / balance / adjustment / copay wording beats any charge cue
_PROBE = [   # artifacts/review-evidence/T-110-paralegal-r2-probe.txt (reviewer's six statement lines), plus English twins
    "Estado de cuenta: pago recibido $300.00.", "Estado de cuenta: ajuste del seguro $500.00.", "Estado de cuenta: copago de la paciente $50.00.",
    "Estado de cuenta: el seguro pagó $4,000.00.", "Estado de cuenta: pendiente de pago $2,900.00.",
    "Estado de cuenta: sesiones de fisioterapia $1,600.00; costo por sesión $400.00.",
    "Estado de cuenta: consultas, pago $1,300.00.", "Estado de cuenta: consultas $1,300.00, saldo $900.00.", "Cargos: abono $200.00.", "Cargos: copago $50.00.",
    "Billed: insurance adjustment $500.00.", "Charges: payment received $300.00.", "Billed charges, paid $300.00.", "Balance: $2,900.00, billed.",
]


@pytest.mark.parametrize("line", _PROBE)
def test_payment_balance_adjustment_wording_beats_every_charge_cue(line):
    for amt in A.find_amounts(line):
        assert RC.charge_wording(line, dict(amt, text=amt["raw"])) is None


def test_estado_de_cuenta_is_context_never_a_cue_on_its_own():
    assert A.charge_cue_es("Estado de cuenta: sesiones de fisioterapia $1,600.00") is None and A.charge_cue_es("Estado de cuenta: $500.00") is None
    assert A.charge_cue_es("Estado de cuenta: consultas $1,300.00;") == "Estado de cuenta: consultas" and A.charge_cue_es("Consulta: $650") is None
    for w in ("copago", "pago recibido", "pendiente de pago", "saldo", "ajuste", "seguro pagó", "payment", "paid", "adjustment", "balance"):
        assert A.BALANCE_CUE.search(f"{w} $5"), w


def test_consultas_line_still_passes_the_wording_check():
    line = "Estado de cuenta: consultas $1,300.00;"
    amt = A.find_amounts(line)[0]
    assert RC.charge_wording(line, dict(amt, text=amt["raw"])) == "Estado de cuenta: consultas"


def test_spanish_unclear_figure_note_does_not_ask_for_a_clean_copy():
    tmp, conn, cid = _stored()
    with tmp:
        a2 = _by_text(conn, cid)["$650.00"][0]
        RV.apply_review(conn, cid, a2["id"], {"action": "accept", "compared": True})      # D-066
        notes = X.build_export(store.export_case(conn, cid))["internal_notes_text"]
        assert "clean copy" not in notes.lower().split("amounts not totaled", 1)[1].split("\n\n")[0]
        assert "Not classified as a charge" in notes and "check the original quote" in notes


def test_lib09_consultas_reclassify_works_on_the_recorded_judge_answer_no_fake_call():
    """T-110 r3: the demo path. The real judge's answer for lib09 'Estado de cuenta: consultas $1,300.00' as class charge is recorded in
    tests/fixtures/llm (agree), so the fixture backend completes the reclassification with no FakeCall."""
    from app.llm import audited as AU
    from app.backend import pipeline as PL
    tmp, conn, cid = _stored()
    with tmp, PL._Backend("fixture"):
        a5 = _by_text(conn, cid)["$1,300.00"][0]
        r = RC.reclassify(conn, cid, a5["id"], {"to": "charge"}, call=AU.make_call(conn, cid))
        assert r["amount"]["kind"] == "charge" and r["reclassified"]["judge_verdict"] == "agree"
        RV.apply_review(conn, cid, a5["id"], {"action": "accept"})
        assert present.totals_view(conn, cid)["accepted"]["cents"] == 130000
