"""T-143 (GATE-M2 legal-nurse major 2, round 2): record.uncovered[] lists EVERY sentence of a record that no entry excerpt covers, except lines positively
identified as administrative by anchored whole-line patterns; verbatim text and offsets; a form answer carries its question. Code only; never in the letter
or the notes."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import present, uncovered as U
from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _view(block, rid="r1", start=0, **extra):
    return {"id": rid, "text": block, "char_start": start, "char_end": start + len(block), "duplicate_of": None, **extra}


def _block(body, date="2026-03-01", source="Clinic"):
    return f'=== Record 1 ===\nDate: {date}\nSource: {source}\nExcerpt: "{body}"\n'


def _uncovered(body, quotes, **kw):
    rv = _view(_block(body))
    U.attach([rv], [{"state": "needs_review", "record_ids": ["r1"], "excerpt": q} for q in quotes] + kw.get("extra", []), present.quote_body)
    return rv["uncovered"]


# ---- the three reviewer examples (pure code, the quote is what the entry kept) ----
def test_lib09_r6_pain_score_is_listed():
    body = "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."
    out = _uncovered(body, ["MRI reviewed. Recommend physical therapy and subacromial injection."])
    assert [u["text"] for u in out] == ["Interpreter: patient's daughter.", "Pain 5/10."]
    assert "number" in out[1]["kinds"]


def test_lib09_r2_chief_complaint_and_onset_is_listed():
    body = ("Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. "
            "Niega pérdida del conocimiento.")
    out = _uncovered(body, ["Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento."])
    assert [u["text"] for u in out] == ["Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo."]


def test_case_06_r3_baseline_history_is_listed():
    body = "History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10."
    out = _uncovered(body, ["Cervical ROM reduced. Pain 5/10."])
    assert [u["text"] for u in out] == ["History: occasional stiffness in the mornings at baseline."]


def test_offsets_are_case_text_offsets_and_text_is_verbatim():
    body = "Interpreter: patient's daughter. MRI reviewed. Pain 5/10."
    block = _block(body)
    raw = "PREAMBLE LINE\n\n" + block
    rv = _view(block, start=len("PREAMBLE LINE\n\n"))
    U.attach([rv], [{"state": "needs_review", "record_ids": ["r1"], "excerpt": "MRI reviewed."}], present.quote_body)
    assert [u["text"] for u in rv["uncovered"]] == ["Interpreter: patient's daughter.", "Pain 5/10."]
    for u in rv["uncovered"]:
        assert raw[u["start"]:u["end"]] == u["text"]
    assert set(u) == {"text", "start", "end", "kinds"}


# ---- negatives ----
def test_fully_quoted_record_has_nothing_uncovered():
    body = "Neck pain 5/10. No numbness."
    assert _uncovered(body, [body]) == []


def test_non_clinical_looking_sentences_are_listed_when_not_administrative():
    """Round 2: interpreter / history-source lines are listed (a nurse reads who gave the history); only positively administrative lines are skipped."""
    body = "Interpreter: patient's daughter. Hx obtained via patient's son, who interpreted. Pain 5/10."
    assert [u["text"] for u in _uncovered(body, ["Pain 5/10."])] == ["Interpreter: patient's daughter.", "Hx obtained via patient's son, who interpreted."]


@pytest.mark.parametrize("line", [
    "ED charge: $2,940.",                                          # money
    "MRI charge: $2,150.",
    "Physical therapy, 4 sessions at $400.00 per session.",        # rate with a clinical word
    "Firma de la paciente: illegible.",                            # signature lines
    "Electronically signed by J. Smith, MD",
    "Electronically signed by Dr. Ortiz.",
    "Signed: Dr X",
    "Dictated by Dr. Ortiz.",
    "J. Smith, MD",                                                # a bare ', MD' signature line (mutant S)
    "Dr. Lucan Ostrowe, DC",
    "Date of service: 03/01/2026.",                                # header fields
    "Fax: 555-0100.", "Phone: (555) 010-0100, front desk.",
    "Page 2 of 5.", "Faxed 03/04/2026 10:15 AM.",                  # stamps
    "Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3.",      # billing form lines
    "Item 28 TOTAL CHARGE 33000.", "Item 29 AMOUNT PAID 0 00.", "Item 31 signature date 110926.",
    "Adjustment (courtesy discount) -$274.00.", "Balance due $2,166.00.", "Balance due.", "Total charges 1500.",
    "No payments posted.", "Letter of protection requested.", "Letter of protection to Fennimoor Law Group.",   # legal / cost boilerplate, no dollar sign
    "Treatment is provided under a letter of protection.",
    "Cost of the visit was covered.", "Paid for the visit out of pocket.", "Patient owes the clinic for care.",
    "Date written 9/2l/26.", "CPT 97110, 96.00, 4 units.", "Charge per visit $185.", "Invoice for the run of 09/14/2026.", "Signed 3/27/2G.", "Sworn 02/01/2027.", "Itemized ledger, statement date 06/15/2026.",
    "Costo por sesión: pendiente.", "Saldo pendiente.", "---",
])
def test_positively_administrative_lines_are_skipped(line):
    assert U.is_administrative(line), line
    assert _uncovered(f"Neck pain 5/10. {line}", ["Neck pain 5/10."]) == []


@pytest.mark.parametrize("line", [
    "[X] adjustment [X] e-stim [X] hot pack.",                      # lib14: the treatment line (bare word 'adjustment')
    "Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack.",
    "Spinal adjustment performed, pain 4/10.",
    "Chiropractic adjustment to cervical spine.",
    "Adjusted C4-C6. [X] e-stim.",
    "Patient signed consent for cervical injection.",               # bare word 'signed'
    "Balance impaired on tandem gait.",
    "Pain 7 circled on a 0-10 scale.", "Pain 4 circled.",
    "Spinal adjustment performed, charge $120.00, pain 4/10.",      # clinical wins over a currency amount
    # round 3: an administrative-looking shape with a clinical kind, or with a tail that is not administrative, is listed
    "Adjustment to C5-6 performed.", "Adjustment of C4-5 and C5-6.",                 # '-6' is not a negative amount
    "Date of onset: 01/16/2026.", "Date of prior surgery: 2019.", "Date of surgery: 05/02/2026.", "Date of MRI: 05/29/2026.",
    "Source of history: patient's son.", "Name of interpreter: Maria L.", "Account of accident: rear-ended at a red light.",
    "Date of accident per intake form: 2026-01-19.", "Date of injury: 3/l8/26.",
    "Letter of protection issued; patient states neck pain began after collision.", "Under letter of protection, patient reports neck pain 5.",
    "Letter of protection issued; patient states he fell at work.",    # patient statement, no body-part word
    "Dictated by Dr. Ortiz, cervical strain with radiating pain to arm.", "Signed: patient reports neck pain improving.",
    "Dictated by Dr. Ortiz, cervical spine clinic.", "Fax: 555-0100, cervical spine clinic.", "Letter of protection to Fennimoor Spine Clinic.",
    "Cost of cervical collar was covered.", "Paid for chiropractic care out of pocket.",            # body part / procedure word: clinical kind wins
    "Splinted.", "Re-examination.", "Ortiz.", "Annual visit.",                                  # a lone capitalized word is not a signature
    "Rx cyclobenzaprine 10 mg, copay $10.", "Patient reports lost wages of $3,000 due to neck pain.",
    "Patient states she cannot afford $500 deductible and has stopped therapy.", "MRI cervical spine performed 05/29/2026, $1,850.",
    "MRI cervical spine (CPT 72141) ordered.", "Prior surgery 2019, patient denies complications.",
    "Cost of the injection caused worry about missing work.",       # cost word, not boilerplate shape
    "Payment plan discussed; patient reports neck pain.",
    "Date written 9/2l/26 and neck pain noted.",
])
def test_clinical_sentences_with_administrative_words_are_listed(line):
    assert not U.is_administrative(line), line
    listed = " ".join(u["text"] for u in _uncovered(line, []))
    assert listed == line or line in listed


@pytest.mark.parametrize("line", [
    "Patient states she was struck by a car while walking in a parking lot.",         # lib09 r1: patient-stated mechanism
    "Passenger vehicle struck from behind.", "Patient referred by attorney.",
    "Patient states symptoms began after the January collision.",
    "Hx of hypertension and diabetes.", "Prior similar episode last year.",
    "Gait antalgic.", "Sensation intact.", "Neuro intact.", "BP 120/80, HR 72.",     # exam / vitals
    "Meds: lisinopril, metformin.", "Off work for two weeks.",                       # medication / work status
    "Paciente refiere que los síntomas comenzaron después del choque.",
    "Interpreter: patient's daughter.", "Hx obtained via patient's son, who interpreted.",
    "Seen on 2026-03-01.", "Paperwork completed.",
])
def test_exam_medication_history_mechanism_and_interpreter_lines_are_listed(line):
    out = _uncovered(f"Pain 5/10. {line}", ["Pain 5/10."])
    assert [u["text"] for u in out] == [line]
    assert isinstance(out[0]["kinds"], list)                                         # kinds is a hint and may be empty


def test_round3_date_of_onset_label_and_answer_are_both_listed():
    """'Date of onset:' with its answer (one line, or the label alone then the answer) and 'Source of history:' are never removed as header fields."""
    body = "Date of onset: 01/16/2026. Source of history: patient's son. Date of onset: 01/16/2026"
    assert [u["text"] for u in _uncovered(body, [])] == ["Date of onset: 01/16/2026.", "Source of history: patient's son.", "Date of onset: 01/16/2026"]
    assert [u["text"] for u in _uncovered("Date of onset:\n01/16/2026. Source of history:\npatient's son.", [])]
    for line in ("Date of onset:", "Source of history:", "Date of onset: 01/16/2026"):
        assert not U.is_administrative(line), line


def test_round3_skip_needs_both_a_whole_line_pattern_and_no_clinical_kind():
    assert U.is_administrative("Fax: 555-0100.") and U.clinical_kinds("Fax: 555-0100.") == []
    assert not U.is_administrative("Fax: 555-0100, cervical spine clinic.")                 # pattern fails (tail) and a body part is present
    assert not U.is_administrative("Letter of protection requested; see attached.")          # open tail: no whole-line pattern
    assert not U.is_administrative("Signed: Dr X, patient has pain")                         # not a name-shaped tail
    assert U.is_administrative("Letter of protection requested.") and U.is_administrative("Electronically signed by J. Smith, MD")


def test_lib09_r1_struck_by_a_car_is_listed_with_the_entry_quote_as_in_the_library():
    body = ("Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. "
            "X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.")
    quote = "Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."
    assert [u["text"] for u in _uncovered(body, [quote])] == ["Hx obtained via patient's son, who interpreted.",
                                                              "Patient states she was struck by a car while walking in a parking lot."]


def test_lib14_lines():
    body = ("Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack. Date written 9/2l/26.")
    out = [u["text"] for u in _uncovered(body, [])]
    assert out[0] == "Pain 7 circled on a 0-10 scale."
    assert any("[X] adjustment [X] e-stim [X] hot pack." in t for t in out)
    cms = ("OCR of scanned CMS-1500. Item 14 injury date 091426 qualifier 431. Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. "
           "Item 28 TOTAL CHARGE 33000. Item 29 AMOUNT PAID 0 00. Item 31 signature date 110926.")
    assert [u["text"] for u in _uncovered(cms, [])] == ["OCR of scanned CMS-1500.", "Item 14 injury date 091426 qualifier 431."]
    inv = ("Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. Total charges $1,567.05. No payments posted. "
           "Letter of protection requested.")
    assert _uncovered(inv, []) == []


def test_form_answer_carries_its_question():
    body = "Motivo de la visita: dolor de espalda. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."
    out = _uncovered(body, ["Motivo de la visita: dolor de espalda."])
    assert [u["text"] for u in out] == ["Accidentes anteriores? Si [ ] No [X]."]
    assert body[out[0]["start"] - 0:out[0]["end"]] is not None
    # an answer whose question an entry quotes still carries the question; a non-question predecessor does not attach
    out2 = _uncovered("Prior accidents? No. Neck pain.", ["Prior accidents?"])
    assert [u["text"] for u in out2] == ["Prior accidents? No.", "Neck pain."]
    out3 = _uncovered("Seen today. No loss of consciousness.", ["Seen today."])
    assert [u["text"] for u in out3] == ["No loss of consciousness."]


@pytest.mark.parametrize("line,kind", [
    ("Pain 5/10.", "number"), ("Rx ibuprofen 800 mg.", "number"), ("Return in 4 weeks.", "number"), ("Strength 4/5.", "number"),
    ("Left knee swollen.", "body_part"), ("Rodilla izquierda hinchada.", "body_part"),
    ("Dx: concussion.", "term"), ("MRI ordered.", "term"), ("Resonancia solicitada.", "term"),
    ("No loss of consciousness.", "negation"), ("Patient denies numbness.", "negation"), ("Niega mareo.", "negation"), ("Si [ ] No [X].", "negation"),
])
def test_kinds_are_hints(line, kind):
    assert kind in U.clinical_kinds(line)


def test_rejected_entry_covers_nothing_and_other_records_do_not_cover():
    body = "Interpreter: patient's daughter. Pain 5/10."
    rv = _view(_block(body))
    ents = [{"state": "rejected", "record_ids": ["r1"], "excerpt": "Pain 5/10."}, {"state": "needs_review", "record_ids": ["r2"], "excerpt": "Pain 5/10."}]
    U.attach([rv], ents, present.quote_body)
    assert [u["text"] for u in rv["uncovered"]] == ["Interpreter: patient's daughter.", "Pain 5/10."]


def test_duplicate_record_and_unquotable_layout_get_empty_list():
    dup = _view(_block("Pain 5/10."), duplicate_of="r0")
    bad = _view(_block("Neck pain 5/10."))
    U.attach([dup], [], present.quote_body)
    U.attach([bad], [], lambda block: (0, "", present.NO_UNITS_LAYOUT))
    assert dup["uncovered"] == [] and bad["uncovered"] == []


def test_whitespace_differences_in_the_quote_still_cover():
    body = "Neck pain 5/10.  Pain with rotation."
    assert _uncovered(body, ["Neck pain 5/10. Pain with rotation."]) == []


def test_no_second_source_and_never_in_letter_or_notes_code():
    for name in ("export.py", "trace.py", "review.py", "store.py"):
        assert "uncovered" not in (ROOT / "app" / "backend" / name).read_text(), name
    src = (ROOT / "app/backend/uncovered.py").read_text()
    assert "app.llm" not in src.replace("app/llm/lexicon.yaml", "")


# ---- end to end on the recorded fixtures (the reviewer's cases) ----
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    return TestClient(create_app(str(tmp_path / "u.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _run(c, body):
    tok = c.post("/api/cases", json=body).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(160):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    return tok, c.get(f"/api/cases/{tok}").json()


def _texts(case, rid):
    return [u["text"] for r in case["records"] if r["id"] == rid for u in r["uncovered"]]


def test_api_lib09_and_case_06(client):
    tok, case = _run(client, {"library": "case_lib09_spanish_interpreter_espalda"})
    assert "Pain 5/10." in _texts(case, "r6")
    assert any(t.startswith("Motivo de consulta: dolor de espalda y hombro derecho") for t in _texts(case, "r2"))
    assert _texts(case, "r7") == []                                  # billing statement: no rate or charge resurfaces
    tok6, case6 = _run(client, {"text": G.raw("case_06_subtle_pre_existing")})
    assert _texts(case6, "r3") == ["History: occasional stiffness in the mornings at baseline."]


def test_api_every_item_is_a_verbatim_uncovered_slice_and_not_in_the_letter(client):
    tok, case = _run(client, {"sample": True})
    letter = client.get(f"/api/cases/{tok}/export").text
    n = 0
    for r in case["records"]:
        assert isinstance(r["uncovered"], list)
        for u in r["uncovered"]:
            n += 1
            assert r["char_start"] <= u["start"] < u["end"] <= r["char_end"]
            assert r["text"][u["start"] - r["char_start"]:u["end"] - r["char_start"]] == u["text"]
            assert isinstance(u["kinds"], list)
    # only listed sentences are outside every entry quote; a listed sentence is not in any entry excerpt
    quotes = [e["excerpt"] for e in case["entries"] + case["undated_entries"]]
    assert all(not any(u["text"] in q for q in quotes) for r in case["records"] for u in r["uncovered"])
    assert "uncovered" not in letter.lower()


def test_api_no_uncovered_sentence_is_in_the_letter_or_the_notes_after_accepting_everything(client):
    """Letter isolation by sentence, not by the word 'uncovered': accept every item of lib09 and export; no listed sentence's text appears in either document."""
    tok, case = _run(client, {"library": "case_lib09_spanish_interpreter_espalda"})
    listed = [u["text"] for r in case["records"] for u in r["uncovered"]]
    assert "Pain 5/10." in listed and any(t.startswith("Motivo de consulta") for t in listed)
    assert any(t.startswith("Patient states she was struck by a car") for t in listed)
    for it in case["entries"] + case["amounts"] + case["flags"]:
        client.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
    ex = client.get(f"/api/cases/{tok}/export").json()
    flag_text = " ".join(" ".join(str(v) for v in f.values() if isinstance(v, str)) for f in case["flags"])
    docs = {"letter": " ".join(ex["letter_text"].split()), "notes": " ".join(ex["internal_notes_text"].split())}
    assert docs["letter"] and docs["notes"]
    for t in listed:
        t = " ".join(t.split())
        assert t not in docs["letter"], t
        if t not in " ".join(flag_text.split()):                        # a flag (e.g. patient_report) may quote its own evidence sentence in the notes
            assert t not in docs["notes"], t


def test_uncovered_has_no_new_word_list_beyond_the_hint_kinds():
    """The administrative test is anchored patterns only: no bare-word alternation list may decide a skip (round-2 rule)."""
    src = (ROOT / "app/backend/uncovered.py").read_text()
    fn = src[src.index("def is_administrative"):src.index("# ---------------------------------------------------------------- clinical content")]
    assert "_BILLING" not in src and "_SIGNATURE" not in src and "_HEADER_FIELD" not in src
    assert "fullmatch" in fn
