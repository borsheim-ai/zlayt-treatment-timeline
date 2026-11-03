"""T-139 round 5 (the last fix; claims-adjuster r4, D-063):
(1) the export gate also scans the BILLED CHARGES section: a charge line carries only its own amount; any other money in its quoted sentence is trimmed from the shown clause
    by code (still a verbatim part of the record) or else blocks the export naming the line; the trace gate says the same (gate.ready == export allowed);
(2) number words directly after a money label (copay, deductible, patient responsibility, paid in full, wages, spent, ...) are money, in the hold, the gate and the eval."""
import pytest

from app.backend import charge_text as CT
from app.backend import export as X
from app.backend import money
from evals import letter_check as LC
from tests.unit.test_t139_charge_text import _case, _charge, _entry
from tests.unit.test_t139_r3 import CLINICAL
from tests.unit.test_t139_r4 import NOT_MONEY

# The adjuster's six number-word summaries (new_edits.json e1, e2, e3, e5, e7, e8) and the digit ones.
SIX_WORD_SUMMARIES = [
    "Transported to Central ER; ambulance copay of twenty.",
    "CT head negative; deductible of five hundred.",
    "Referred to physical therapy 2x/week for 6 weeks; patient spent fifteen hundred out of pocket.",
    "Pain 4/10, improving; patient reports missing 3 days of work; lost eighteen hundred in wages.",
    "MRI ordered; patient responsibility twelve hundred.",
    "Findings may represent degenerative change, correlate clinically; paid in full twenty-one fifty.",
]
DIGIT_WORDINGS = ["Insurer reimbursed 1,412.50.", "Copayment 40.00 collected.", "Coinsurance 430.00.", "MRI cost the patient 2,150.", "Policy limits 30,000.", "Med-pay 5,000.00 exhausted.",
                  "Net due 737.50.", "Patient spent 1,500 on the MRI.", "Lost 1,800.00 in wages."]
WORD_WORDINGS = SIX_WORD_SUMMARIES + ["Copay of twenty.", "Deductible of five hundred.", "Insurer reimbursed fifteen hundred.", "Refund of fifteen hundred.", "Lost eighteen hundred in wages.",
                                      "Wages of eighteen hundred lost.", "Out of pocket fifteen hundred.", "Patient responsibility twelve hundred.", "Paid in full twenty-one fifty.",
                                      "Patient spent fifteen hundred on the MRI.", "Coinsurance four hundred thirty.", "Copayment forty."]
STILL_CLINICAL = CLINICAL + NOT_MONEY + ["Lost wages three weeks.", "Patient spent two days in the unit.", "Paid one visit.", "Deductible not met.", "Copay collected at the desk.",
                                          "Wages: see employer letter.", "Out of pocket for two weeks with the brace.", "She spent twelve hours in the ED.", "Paid in full.", "Patient responsibility explained to her."]


# ---------------------------------------------------------------- 2. number words after a money label
@pytest.mark.parametrize("text", WORD_WORDINGS + DIGIT_WORDINGS)
def test_a_figure_or_number_words_after_a_money_label_are_money(text):
    assert money.has_money(text), text
    assert CT.check(text, text), text


@pytest.mark.parametrize("text", STILL_CLINICAL)
def test_clinical_words_and_labels_without_a_figure_are_not_money(text):
    assert not money.has_money(text), (text, money.strings(text))


def test_the_six_word_summaries_are_refused_at_edit_time_and_blocked_by_the_gate_and_flagged_by_the_eval():
    for s in SIX_WORD_SUMMARIES:
        assert CT.check(s, "Dx: cervical strain."), s
        with pytest.raises(X.ExportBlocked) as ei:
            X.build_export(_case([_entry(s, "Dx: cervical strain.")]))
        assert ei.value.items and ei.value.items[0]["reason_code"] == "MONEY_IN_LETTER" and ei.value.items[0]["item_id"] == "e1", s
        letter = X.build_export(_case([_entry(s, "Dx: cervical strain.")]), check_letter=False)["letter_text"]
        assert LC.violations(letter), s


# ---------------------------------------------------------------- 1. the BILLED CHARGES section
REC = "Dx: cervical strain. {sentence}"


def _charged(sentence, raw="$2,150", cents=215000, exc=None, status="accepted"):
    rec = REC.format(sentence=sentence)
    records = [dict(n=1, source="Marrowgate General ED", date_iso="2026-02-14", excerpt=rec)]
    amt = _charge("a1", cents, raw, exc or sentence, status=status)
    return _case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")], [amt], records=records)


def _quote_line(out):
    lines = out["letter_text"].split("\n")
    return lines[lines.index(X.CHARGES_TITLE) + 3]


def test_a_clean_charge_line_is_untouched():
    out = X.build_export(_charged("Charge: $2,150."))
    assert 'Charge: $2,150."' in _quote_line(out) and "Billed charges accepted from these records: $2,150.00" in out["letter_text"]


@pytest.mark.parametrize("sentence,shown", [
    ("Charge: $2,150 (ins paid $1,412.50).", "Charge: $2,150"),
    ("Charge: $2,150; paid in full 2,150.00.", "Charge: $2,150"),
    ("Charge: $2,150, patient responsibility 1,200.00.", "Charge: $2,150"),
    ("Lost wages 1,800.00 claimed; charge: $2,150.", "charge: $2,150"),
    ("Allowed 1,412.50, write-off 737.50; charge $2,150.", "charge $2,150"),
    ("Charge: $2,150 (insurer reimbursed fifteen hundred).", "Charge: $2,150"),
    ("Charge: $2,150 less $737.50 contractual adjustment.", "Charge: $2,150"),
    ("Charge $2,150 paid in full 2,150.00 by the carrier.", "Charge $2,150"),
])
def test_other_money_in_a_charge_sentence_is_trimmed_by_code_and_stays_verbatim(sentence, shown):
    case = _charged(sentence)
    out = X.build_export(case)
    q = _quote_line(out)
    assert shown in q and not [m for m in money.strings(q) if "2,150" not in m], q
    inner = q.split('"', 1)[1].rsplit('"', 1)[0]
    assert inner in case["records"][0]["excerpt"]                         # still a verbatim part of the record
    assert X.money_blockers_for_case(case) == [] and LC.violations(out["letter_text"], [215000]) == []


@pytest.mark.parametrize("sentence", [
    "Insurer paid $1,412.50 of the $2,150 charge.",
    "Balance 737.50 after a charge of $2,150.",
    "Patient responsibility twelve hundred on a $2,150 charge.",
])
def test_when_no_clean_clause_exists_the_export_is_blocked_and_the_charge_line_is_named(sentence):
    case = _charged(sentence)
    with pytest.raises(X.ExportBlocked) as ei:
        X.build_export(case)
    b = ei.value.items[0]
    assert b["reason_code"] == "MONEY_IN_LETTER" and b["item_id"] == "a1" and b["kind"] == "amount" and "Billed charges" in b["why"] and f"Line {b['line']} " in b["why"]
    assert b["next_action"]["target"]["item_id"] == "a1" and X.money_blockers_for_case(case) == ei.value.items
    letter = X.build_export(case, check_letter=False)["letter_text"]
    assert LC.violations(letter, [215000])                                 # the eval agrees with the gate on the section rule


def test_dismissing_the_blocking_charge_clears_the_gate():
    case = _charged("Balance 737.50 after a charge of $2,150.")
    assert X.money_blockers_for_case(case)
    case["amounts"][0]["review_status"] = "dismissed"
    assert X.money_blockers_for_case(case) == [] and X.build_export(case)["letter_text"]


def test_a_charge_header_line_carries_only_its_own_amount():
    case = _charged("Charge: $2,150.")
    case["records"][0]["source"] = "Marrowgate General ED balance 1,200.00"
    with pytest.raises(X.ExportBlocked) as ei:
        X.build_export(case)
    assert [b["kind"] for b in ei.value.items if b["item_id"] == "a1"] == ["amount"]


def test_the_gate_reads_the_letter_text_alone_for_a_charges_section():
    letter = ("TREATMENT CHRONOLOGY\n\nJune 1, 2026 — Marrowgate General ED\nDx: cervical strain.\nSource [Ex. __ / Bates __]: \"Dx: cervical strain.\"\n\n"
              "BILLED CHARGES\n\nMarrowgate General ED, February 14, 2026: $2,150.00\nSource [Ex. __ / Bates __]: \"Charge: $2,150 (ins paid $1,412.50).\"\n\n"
              "Billed charges accepted from these records: $2,150.00")
    b = X.letter_money_blockers(letter)
    assert len(b) == 1 and b[0]["expressions"] == ["$1,412.50"] and b[0]["reason_code"] == "MONEY_IN_LETTER"
    assert X.letter_money_blockers(letter.replace(" (ins paid $1,412.50)", "")) == []


def test_no_second_detector_for_the_charges_section():
    import inspect
    src = inspect.getsource(X.letter_money_blockers) + inspect.getsource(X._amount_quote)
    assert "re.compile" not in src and "dollar_strings" not in inspect.getsource(X._amount_quote)


# ---------------------------------------------------------------- gate.ready == export allowed (trace gate)
OLD, NEW = "Charge: $2,150.", "Balance 737.50 after a charge of $2,150."


def _poison(monkeypatch, new):
    """Store the sample's MRI record (and the charge item's excerpt) with a different sentence, as if the record had said it."""
    from app.backend import store
    orig = store.export_case

    def patched(conn, cid, **kw):
        case = orig(conn, cid, **kw)
        for r in case["records"]:
            r["excerpt"] = r["excerpt"].replace(OLD, new)
        for a in case["amounts"]:
            a["excerpt"] = (a.get("excerpt") or "").replace(OLD, new)
        return case
    monkeypatch.setattr(store, "export_case", patched)


def test_gate_ready_equals_export_allowed_for_a_charge_line_with_other_money(tmp_path, monkeypatch):
    from tests.unit.test_t139_charge_text import _lib_client, _post
    from tests.unit.test_t139_r4 import _gate
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    view = c.get(f"/api/cases/{tok}").json()
    for kind in ("entries", "amounts", "flags"):
        for it in view[kind]:
            _post(c, tok, it["id"], {"action": "accept"})
    assert _gate(c, tok)["ready"] is True and c.get(f"/api/cases/{tok}/export").status_code == 200
    with monkeypatch.context() as m:
        _poison(m, NEW)
        gate, ex = _gate(c, tok), c.get(f"/api/cases/{tok}/export")
        assert ex.status_code == 422 and gate["ready"] is False
        got = [b for b in gate["blockers"] if b["reason_code"] == "MONEY_IN_LETTER"]
        assert got and got[0]["kind"] == "amount" and "737.50" in " ".join(got[0]["expressions"]) and gate["counts"]["money_in_letter"] == len(got)
        assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in gate["blockers"]]
    with monkeypatch.context() as m:
        _poison(m, "Charge: $2,150 (ins paid $1,412.50).")                  # a clause code can trim: gate ready again, export allowed, the line shows the charge only
        gate, ex = _gate(c, tok), c.get(f"/api/cases/{tok}/export")
        assert ex.status_code == 200 and gate["ready"] is True and "1,412.50" not in ex.json()["letter_text"]


def test_a_ledger_row_is_cut_after_the_charge_figure():
    row = "06/10/2026  Manual therapy  $150.00  $0.00  $730.00"
    case = _charged(row, raw="$150.00", cents=15000)
    q = _quote_line(X.build_export(case))
    assert q.endswith('Manual therapy  $150.00"') and "730.00" not in q and row.startswith(q.split('"')[1])
