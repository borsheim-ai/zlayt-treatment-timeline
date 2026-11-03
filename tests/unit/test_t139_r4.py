"""T-139 round 4 (structural fix-up after the round cap; claims-adjuster r3, orchestrator §7.4):
(1) ONE money detector (app/backend/money.py) used by the charge-text hold, the export gate and evals/letter_check.py: no divergence;
(2) the export gate runs it on the FINAL letter text: any money outside the total line and the accepted-charge lines blocks the export and names the line,
    including a paralegal's own summary edit;
(3) labelled figures with cents or thousands separators ('Patient responsibility 1,200.00') and the other wordings the adjuster found are money;
(4) the held-out hint states the true cause (tests/unit/test_t139_r3.py::test_each_held_entry_says_the_true_reason)."""
import pytest

from app.backend import charge_text as CT
from app.backend import export as X
from app.backend import money
from evals import letter_check as LC
from tests.unit.test_t139_charge_text import _case, _entry, _lib_client, _post
from tests.unit.test_t139_r3 import CLINICAL

# The adjuster's seven accepted summary edits on the sample (edit_attack_r3.py): the r3 letter eval caught 1 of 7.
SEVEN_EDITS = [
    ("e4", "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits at 40 a visit."),
    ("e3", "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks; patient responsibility 6 per visit."),
    ("e5", "Pain 4/10, improving; patient reports missing 3 days of work; lost wages 3."),
    ("e8", "C5-C6 disc protrusion with mild right foraminal narrowing; findings may represent degenerative change, correlate clinically; MRI billed at two thousand one hundred fifty."),
    ("e9", "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision; injection quoted at fifteen hundred."),
    ("e7", "New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered; reimbursement 7 owed to patient."),
    ("e6", "Discharged from PT after two missed appointments; pain 3/10; paid in full 3."),
]
# Record wordings the r3 production check missed (attack_sweep_r3.txt): labelled figures, a figure before bill, 'Dollars:', a small dollar sign.
RECORD_WORDINGS = [
    "Patient responsibility 1,200.00.", "Patient responsibility: 1,200.00.", "Paid in full 2,150.00.", "Reimbursement 2,150.00.", "Lost wages 1,800.00.", "Wage loss 1,800.",
    "Usual and customary 185.00.", "Mileage reimbursement 87.00.", "Patient is worried about the 3,915 ER bill.", "The ambulance bill came to 1,380.", "Dollars: 185.00.",
    "PT at 185 a visit.", "PT at 185 each visit.", "Charge per visit ﹩185.",
    # the eval was narrower than production on these (r3 minor 3)
    "Total charge\n49100.", "Charge per\nvisit 185.", "Charge:\n1,200.00", "Allowed 4,413.50.", "LOP balance 1,550.", "Balance 1,550.", "Write-off 1,250.00.", "PT 185/session.",
]
NOT_MONEY = CLINICAL + [
    "Lost wages 3 weeks.", "Berg balance 45.", "Charge nurse 120 bpm on the unit.", "Take ibuprofen 3 a day.", "Plan of care: 2 a week for 6 weeks.", "Paid one visit.",
    "She was billed for twelve visits.", "Heart rate 110 bpm; balance and gait steady.", "Pain 6 per visit noted by therapist as 6/10.",
]


def _letter(line):
    return f"TREATMENT CHRONOLOGY\n\nJune 1, 2026 — Marrowgate General ED\nDx: cervical strain.\nSource [Ex. __ / Bates __]: \"{line}\"\n"


# ---------------------------------------------------------------- 1. one detector
def test_the_three_callers_use_the_one_detector(monkeypatch):
    text = "Plan of care: 12 visits at 40 a visit. Billed at fifteen hundred."
    assert money.has_money(text) and CT.check(text, text) and LC.unmarked_money(text) + LC.other_currency(text)
    assert X.letter_money_blockers(_letter(text))
    monkeypatch.setattr(money, "hits", lambda t: [])                       # blind the one module: every caller goes blind with it
    assert CT.check(text, text) == {} and not CT.has_currency(text)
    assert LC.dollar_figures(text) == [] and LC.other_currency(text) == [] and LC.unmarked_money(text) == []
    assert X.letter_money_blockers(_letter(text)) == []
    assert LC.violations(_letter(text)) == []


def test_no_second_detector_is_left_behind():
    import evals.letter_check as lc
    import app.backend.charge_text as ct
    for mod, names in ((lc, ("_DOLLAR", "_UNMARKED", "_SIGN_FIG", "_MONEY_WORD", "spoken_money", "statement_money")), (ct, ("_UNMARKED", "_STRONG", "_WEAK", "_STATEMENT", "_SPOKEN"))):
        for n in names:
            assert not hasattr(mod, n), (mod.__name__, n)


# ---------------------------------------------------------------- 3. the wordings are money (and clinical numbers are not)
@pytest.mark.parametrize("text", RECORD_WORDINGS)
def test_each_record_wording_is_held_by_the_hold_the_eval_and_the_gate(text):
    assert CT.check(text, "").get("summary") and CT.check("", text).get("excerpt"), text
    assert LC.violations(_letter(text)), text
    assert X.letter_money_blockers(_letter(text)), text


@pytest.mark.parametrize("text", [t for _, t in SEVEN_EDITS])
def test_each_of_the_adjusters_seven_edits_is_money_for_all_three(text):
    assert CT.check(text, "").get("summary"), text
    assert any("states money" in v or "treatment text" in v for v in LC.violations(_letter(text))), text
    assert X.letter_money_blockers(_letter(text)), text


@pytest.mark.parametrize("text", NOT_MONEY)
def test_clinical_numbers_are_not_money_for_any_of_the_three(text):
    assert CT.check(text, text) == {}, money.hits(text)
    assert LC.violations(_letter(text)) == [], text
    assert X.letter_money_blockers(_letter(text)) == [], text


# ---------------------------------------------------------------- 2. the export gate
def test_the_gate_names_the_line_and_the_entry():
    letter = X.build_export(_case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")]))["letter_text"]
    assert X.letter_money_blockers(letter) == []
    bad = letter.replace("Diagnosis of cervical strain.", "Diagnosis of cervical strain; MRI billed at two thousand one hundred fifty.")
    got = X.letter_money_blockers(bad, [dict(id="e1", summary="Diagnosis of cervical strain; MRI billed at two thousand one hundred fifty.", excerpt="Dx: cervical strain.")])
    assert len(got) == 1
    b = got[0]
    assert b["reason_code"] == "MONEY_IN_LETTER" and b["item_id"] == "e1" and b["kind"] == "entry" and b["next_action"]["code"] == "EDIT_SUMMARY"
    assert b["text"] == bad.split("\n")[b["line"] - 1] and f"Line {b['line']} of the letter" in b["why"] and "two thousand one hundred fifty" in b["why"]


def test_the_gate_leaves_the_total_line_and_the_accepted_charge_lines_alone():
    letter = X.build_export(_case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")],
                                  [dict(id="a1", record_no=1, cents=391500, cls="charge", raw="$3,915.00", excerpt="ED charge: $3,915.", review_status="accepted")]))["letter_text"]
    assert X.TOTAL_PREFIX + "$3,915.00" in letter and "ED charge: $3,915." in letter
    assert X.letter_money_blockers(letter) == []


def test_a_human_summary_edit_blocks_the_export_with_the_line_named():
    case = _case([_entry("Diagnosis of cervical strain; patient responsibility 1,200.00.", "Dx: cervical strain.")])
    with pytest.raises(X.ExportBlocked) as ei:
        X.build_export(case)
    b = ei.value.items[0]
    assert b["reason_code"] == "MONEY_IN_LETTER" and "Line 4" in b["why"] and "patient responsibility 1,200.00" in b["why"]
    out = X.build_export(case, check_letter=False)                         # the eval's way to still read the text it is auditing
    assert "patient responsibility 1,200.00" in out["letter_text"]


def test_split_letter_is_by_structure_not_by_the_words():
    letter = ('TREATMENT CHRONOLOGY\n\nJune 1, 2026 — Marrowgate General ED\nDx.\nSource [Ex. __ / Bates __]: "Header BILLED CHARGES then Charge per visit $140."\n\n'
              'BILLED CHARGES\n\nMarrowgate General ED, June 1, 2026: $140.00\nSource [Ex. __ / Bates __]: "Charge: $140."\n\n' + X.TOTAL_PREFIX + "$140.00")
    head, tail = X.split_letter(letter)
    assert tail[0] == "BILLED CHARGES" and "Header BILLED CHARGES" in "\n".join(head)
    assert X.letter_money_blockers(letter)[0]["line"] == 5                 # the quote's own $140 is still found
    assert LC.violations(letter, [14000])                                  # and the eval is not blinded by the words in the quote
    assert X.split_letter("TREATMENT CHRONOLOGY\n\nDx.")[1] == []


def _edit_and_export(tmp_path, monkeypatch):
    """The sample; every summary edit of the adjuster stored as if the edit-time check had a hole (patched out), everything accepted; then the real code exports."""
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    with monkeypatch.context() as m:
        m.setattr(CT, "check", lambda summary, excerpt: {})
        for iid, summary in SEVEN_EDITS:
            r = _post(c, tok, iid, {"action": "edit", "edits": {"summary": summary}})
            assert r.status_code == 200, (iid, r.json())
        view = c.get(f"/api/cases/{tok}").json()
        for kind in ("entries", "amounts", "flags"):
            for it in view[kind]:
                if it["review_status"] != "accepted":                            # an edit is not in the letter until she accepts it (T-134)
                    _post(c, tok, it["id"], {"action": "accept"})
    return c, tok


def test_the_seven_edits_are_refused_at_edit_time_and_store_nothing(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    before = {e["id"]: e["summary"] for e in c.get(f"/api/cases/{tok}").json()["entries"]}
    for iid, summary in SEVEN_EDITS:
        r = _post(c, tok, iid, {"action": "edit", "edits": {"summary": summary}})
        assert r.status_code == 422 and "CHARGE_TEXT_IN_ENTRY" in str(r.json()), (iid, r.json())
    assert {e["id"]: e["summary"] for e in c.get(f"/api/cases/{tok}").json()["entries"]} == before


def test_the_seven_edits_stored_past_the_edit_check_block_the_export_on_every_line(tmp_path, monkeypatch):
    c, tok = _edit_and_export(tmp_path, monkeypatch)
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 422, r.text[:300]
    err = r.json()["error"]
    assert err["code"] == "export_blocked" and "Line " in err["message"] and "The export is blocked." in err["message"]
    got = [b for b in err["detail"]["blockers"] if b["reason_code"] == "MONEY_IN_LETTER"]
    assert len(got) == len(SEVEN_EDITS), [b["why"] for b in got]
    assert {b["item_id"] for b in got} == {iid for iid, _ in SEVEN_EDITS}
    for b in got:
        assert b["item_id"] and b["next_action"]["target"]["item_id"] == b["item_id"] and b["text"][:60] in b["why"]


def test_after_the_paralegal_fixes_the_lines_the_export_goes_through(tmp_path, monkeypatch):
    c, tok = _edit_and_export(tmp_path, monkeypatch)
    for iid, _ in SEVEN_EDITS:
        assert _post(c, tok, iid, {"action": "dismiss"}).status_code == 200
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 200 and X.letter_money_blockers(r.json()["letter_text"]) == []


# ---------------------------------------------------------------- the trace export gate agrees with GET /export (D-044/D-045: gate.ready == export allowed)
def _gate(c, tok):
    return next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "export_gate")


def test_gate_ready_equals_export_allowed_when_a_stored_summary_carries_money(tmp_path, monkeypatch):
    c, tok = _edit_and_export(tmp_path, monkeypatch)                        # the seven money summaries are stored and accepted
    gate, ex = _gate(c, tok), c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and gate["ready"] is False
    got = [b for b in gate["blockers"] if b["reason_code"] == "MONEY_IN_LETTER"]
    assert len(got) == len(SEVEN_EDITS) and {b["item_id"] for b in got} == {i for i, _ in SEVEN_EDITS}
    assert all(b["line"] and b["text"] and b["next_action"]["target"]["item_id"] == b["item_id"] for b in got)
    assert gate["reason_code"] == "MONEY_IN_LETTER" and gate["counts"]["money_in_letter"] == len(SEVEN_EDITS) and gate["next_action"]
    assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in gate["blockers"]]
    assert c.get(f"/api/cases/{tok}/trace").json()["verdict"]["code"] == "needs_attention"
    for iid, _ in SEVEN_EDITS:                                              # fixing every line clears the gate and the export together
        assert _post(c, tok, iid, {"action": "dismiss"}).status_code == 200
    gate, ex = _gate(c, tok), c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200 and gate["ready"] is True and not [b for b in gate["blockers"] if b["reason_code"] == "MONEY_IN_LETTER"]


def test_gate_ready_equals_export_allowed_on_a_clean_case(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    view = c.get(f"/api/cases/{tok}").json()
    for kind in ("entries", "amounts", "flags"):
        for it in view[kind]:
            _post(c, tok, it["id"], {"action": "accept"})
    gate, ex = _gate(c, tok), c.get(f"/api/cases/{tok}/export")
    assert (ex.status_code == 200) == gate["ready"] and gate["counts"]["money_in_letter"] == 0
