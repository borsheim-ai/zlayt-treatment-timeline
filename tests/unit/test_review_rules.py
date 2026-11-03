"""Review/edit rules (backend/review.py). R-RV-2 (D-010, D-012), R-RV-3, R-CH-5, R-CH-7, ADR-005 edit re-check order; fake judge only."""
import pytest
from app.backend import pipeline as PL, review as RV, export as X
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record

def seeded(tmp_path, case="sample"):
    """Seeds a case through the pipeline with a case-aware fake (extract returns the first sentence unit of the cited record)."""
    from tests.unit._fakes import sample_script, which_record as wr
    if case == "sample":
        call = FakeCall(sample_script())
    else:
        def extract(u):
            n = wr(u, case)[0]; ex = G.record(case, n)["excerpt"]
            return dict(summary=ex.split(". ")[0].rstrip(".") + ".", excerpt=ex.split(". ")[0].rstrip(".") + ".")
        call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / f"rv-{case}.sqlite")); cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), call=call, now=lambda: 1.0)
    return conn, cid, out

def ent(out, n):
    """Entry id citing record n (api.md: entries carry record_ids like 'r5')."""
    return [e for e in out["entries"] + out.get("undated_entries", []) if f"r{n}" in e["record_ids"]][0]["id"]
def amt(out, raw): return [a for a in out["amounts"] if a["raw"] == raw][0]["id"]
def judge(v): return FakeCall({"j1": {"verdict": v, "reason_code": "NONE"}})

@pytest.mark.parametrize("edits", [{"date": "2026-01-01"}, {"provider": "Someone Else"}, {"record": "r2"}, {"summary": "ok", "date": "2026-01-01"}])
def test_entry_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: editing an entry's date, provider or record -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

@pytest.mark.parametrize("edits", [{"evidence": "x"}, {"type": "causation"}, {"title": "New title"}])
def test_flag_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: flag evidence, type and title are not editable (only a note)."""
    conn, cid, out = seeded(tmp_path)
    fid = [f for f in out["flags"] if f["type"] == "gap"][0]["id"]
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, fid, dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

@pytest.mark.parametrize("edits", [{"value": 1}, {"cls": "charge"}, {"amount": "$1"}, {"note": "x"}])
def test_charge_cannot_be_edited(tmp_path, edits):
    """R-CH-7 (D-010): a charge/rate has accept or dismiss only; no value or class edit, so a rate cannot become a charge."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, amt(out, "$185"), dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

def test_excerpt_not_contiguous_whole_sentences_is_422(tmp_path):
    """R-RV-2 (D-012): non-contiguous or mid-sentence excerpt edit -> 422."""
    conn, cid, out = seeded(tmp_path)
    for bad in ["Alert and oriented. 41M restrained driver, rear-ended at approx. 35 mph.", "rear-ended at approx. 35 mph"]:
        with pytest.raises(RV.ReviewError) as e:
            RV.apply_review(conn, cid, ent(out, 1), dict(action="edit", edits=dict(excerpt=bad)), call=judge("supported"))
        assert e.value.code == "invalid_edit"

def test_excerpt_dropping_hedge_is_422(tmp_path):
    """R-RV-2 / R-TL-8: re-selecting entry 8's excerpt without the hedge sentences -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, ent(out, 8), dict(action="edit", edits=dict(excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")), call=judge("supported"))
    assert e.value.code == "invalid_edit"

def test_confirm_date_on_parsed_record_is_422_invalid_edit(tmp_path):
    """R-RV-2: confirm_date on a parsed date -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.confirm_date(conn, cid, out["records"][0]["id"], "2026-01-09")
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

def test_confirm_date_non_candidate_is_422_date_invalid(tmp_path):
    """R-IN-5: case_01 record 8 confirm with a date that is not one of the two code readings -> 422 date_invalid; a candidate -> 200."""
    conn, cid, out = seeded(tmp_path, "case_01_date_formats")
    rid = [r for r in out["records"] if r["seq"] == 8][0]["id"]
    with pytest.raises(RV.ReviewError) as e:
        RV.confirm_date(conn, cid, rid, "2026-06-06")
    assert (e.value.status, e.value.code) == (422, "date_invalid")
    assert RV.confirm_date(conn, cid, rid, "2026-05-04")["record"]["date_status"] == "confirmed"

@pytest.mark.parametrize("confirm", [False, True])
def test_added_dollar_is_a_hard_422_even_with_confirm_and_saves_nothing(tmp_path, confirm):
    """D-034 (R-RV-3): summary edited to add '$9,000' -> 422 invalid_edit, no override via confirm_warnings; the item is unchanged."""
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    before = DB.get_item(conn, eid)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Visit 8: pain 4/10, improving; billed $9,000."), confirm_warnings=confirm), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["tokens"]
    assert DB.get_item(conn, eid) == before

def test_seeded_herniation_judge_unsupported_saves_as_needs_review_with_warning(tmp_path):
    """D-047/D-045b: 'herniation' passes the code check but judge #1 says unsupported -> no 409; saved as needs_review, warning JUDGE_UNSUPPORTED."""
    conn, cid, out = seeded(tmp_path)
    r = RV.apply_review(conn, cid, ent(out, 8), dict(action="edit", edits=dict(summary="Cervical MRI: C5-C6 disc herniation with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.")), call=judge("unsupported"))
    assert r["item"]["review_status"] == "edited" and r["item"]["state"] == "needs_review"
    assert "JUDGE_UNSUPPORTED" in [w["code"] for w in r["warnings"]]

def test_no_confirm_path_remains_confirm_warnings_is_ignored_and_no_event_is_logged(tmp_path):
    """D-047: the 409 'keep my wording' path is gone. A judge objection saves without a confirm; `confirm_warnings` changes nothing and no keep_my_wording event or override field is ever written."""
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    edits = dict(summary="Visit 8: pain 4/10, improving; the patient is recovering well.")
    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=edits, confirm_warnings=True), call=judge("unsupported"))
    assert r["item"]["review_status"] == "edited" and "kept_my_wording" not in r["item"]["edited"] and "override_reasons" not in r["item"]["edited"]
    assert not [x for x in DB.list_events(conn, cid) if x["action"] == "keep_my_wording"]
    from app.backend import store
    assert store.export_case(conn, cid)["events"] == []


_EXC5 = "Pain 4/10, improving."


@pytest.mark.parametrize("confirm", [False, True])
@pytest.mark.parametrize("summary,reason,key", [
    ("Visit 8: pain 4/10, improving; no radiating symptoms.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
    ("Visit 8: pain 4/10, improving; not in distress.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
    ("Visit 8: pain 4/10 improving without medication.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
    ("Visit 8: left-sided pain 4/10, improving.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
    ("Visit 8: right shoulder pain 4/10, improving.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "tokens"),
])
def test_side_negation_token_not_in_quote_is_a_hard_422_and_saves_nothing_d047(tmp_path, summary, reason, key, confirm):
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    before, events = DB.get_item(conn, eid), DB.list_events(conn, cid)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary=summary), confirm_warnings=confirm), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == reason and e.value.detail[key]
    assert e.value.message and "quote" in e.value.message
    assert DB.get_item(conn, eid) == before and DB.list_events(conn, cid) == events


def test_dropping_a_qualifier_of_the_quote_is_a_hard_422_d047(tmp_path):
    conn, cid, out = seeded(tmp_path); eid = ent(out, 8)
    before = DB.get_item(conn, eid)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Cervical MRI: C5-C6 disc herniation with foraminal narrowing."), confirm_warnings=True), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_DROPS_QUALIFIER" and "hedge" in e.value.detail["qualifiers"]
    assert "leaves out" in e.value.message
    assert DB.get_item(conn, eid) == before


def test_judge_is_not_called_when_a_code_check_fails_d047(tmp_path):
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    calls = []
    def spy(*a, **k):
        calls.append(1); return judge("supported")(*a, **k)
    with pytest.raises(RV.ReviewError):
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Visit 8: no pain, 4/10, improving.")), call=spy)
    assert calls == []

def test_judge_unavailable_saves_with_reason(tmp_path):
    """R-RV-3: code check passes, judge fails -> saved, state needs_review, reason JUDGE_UNAVAILABLE."""
    conn, cid, out = seeded(tmp_path)
    r = RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=dict(summary="Visit 8: pain 4/10 and improving.")), call=FakeCall({"j1": AU.LLMFailed("down")}))
    assert r["item"]["review_status"] == "edited" and r["item"]["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in r["item"]["reasons"]

def test_accept_unclear_amount_goes_to_notes_not_letter():
    """R-CH-5: accepting '$1,2OO' (case_03) puts 'request clean copy of bill' in the notes; it is not in the letter or total."""
    ex = G.expected("case_03_rate_and_ocr"); raw = {r["n"]: r for r in G.records("case_03_rate_and_ocr")}
    recs = [dict(n=r["record_no"], source=r["source"], date_iso=r["date"], excerpt=raw[r["record_no"]]["excerpt"]) for r in ex["records"]]
    amts = [dict(id="a2", record_no=2, cents=None, cls="unclear", raw="$1,2OO", excerpt="Statement for initial exam and x-ray: $1,2OO.", review_status="accepted"),
            dict(id="a3", record_no=3, cents=9500, cls="charge", raw="$95.00", excerpt="Charge: $95.00.", review_status="accepted")]
    out = X.build_export(dict(records=recs, entries=[], amounts=amts, flags=[], pending_count=0, events=[]))
    assert "request clean copy of bill" in out["internal_notes_text"].lower() and "1,2OO" not in out["letter_text"]
    assert "Billed charges accepted from these records: $95.00" in out["letter_text"].split("\n")

def test_accept_rate_keeps_total_8390(tmp_path):
    """R-CH-3/R-CH-7: accepting the $185 rate leaves the accepted total at what the charges give; rate listed only in notes."""
    conn, cid, out = seeded(tmp_path)
    for raw in ("$6,240", "$2,150", "$185"):
        RV.apply_review(conn, cid, amt(out, raw), dict(action="accept"), call=judge("supported"))
    r = RV.apply_review(conn, cid, amt(out, "$185"), dict(action="accept"), call=judge("supported"))
    assert r["totals"]["accepted"]["cents"] == 839000

def test_no_bulk_accept_exists():
    """D-011 / ADR-005: there is no bulk accept function in the review module."""
    assert not [n for n in dir(RV) if "bulk" in n.lower() or "accept_all" in n.lower()]


def test_helpers_work_on_api_shaped_output():
    """Helper smoke (no pipeline): ent()/amt() index api.md-shaped dicts by record_ids."""
    out = dict(entries=[dict(id="e5", record_ids=["r5"])], amounts=[dict(id="a3", raw="$185")])
    assert ent(out, 5) == "e5" and amt(out, "$185") == "a3"

@pytest.mark.parametrize("exc", [AU.LLMFailed("down"), P.FixtureMissing("h"), P.LLMError("TIMEOUT")])
def test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
    """T-039 debt / ADR-005, narrowed by T-073: an EXPECTED judge failure (LLMFailed, provider LLMError / FixtureMissing) on an edit saves the edit as needs_review with JUDGE_UNAVAILABLE and never as verified/supported. Any other exception is a bug and propagates (tests/unit/test_judge_guard.py)."""
    conn, cid, out = seeded(tmp_path)
    r = RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=dict(summary="Visit 8: pain 4/10 and improving.")), call=FakeCall({"j1": exc}))
    it = r["item"]
    assert it["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in it["reasons"] and it["state"] != "verified"
    assert it["ladder"]["judge"]["verdict"] not in ("supported", "agree")


# D-047 r2: qualifier words the quote does not carry (attribution, hedge, approximation) and the full side/negation class are hard 422s.
ADDED_QUALIFIER = [
    "Visit 8: patient reports pain 4/10, improving.", "Visit 8: patient states pain 4/10, improving.", "Visit 8: pain 4/10, improving per patient.",
    "Visit 8: pain 4/10, possibly improving.", "Visit 8: pain 4/10, likely improving.", "Visit 8: pain 4/10, improving; suggests recovery.",
    "Visit 8: pain 4/10, may be improving.", "Visit 8: pain approximately 4/10, improving.", "Visit 8: pain about 4/10, improving.", "Visit 8: pain ~4/10, improving.",
]
WIDE_VOCAB = ["Visit 8: patient denies radiating symptoms, pain 4/10, improving.", "Visit 8: pain 4/10, never worse.", "Visit 8: none reported, pain 4/10, improving.",
              "Visit 8: bilateral pain 4/10, improving.", "Visit 8: negative for distress, pain 4/10, improving.", "Visit 8: absent distress, pain 4/10, improving.",
              "Visit 8: neither worse nor better, pain 4/10, improving.", "Visit 8: pain 4/10, improving; didn't worsen."]


@pytest.mark.parametrize("confirm", [False, True])
@pytest.mark.parametrize("summary", ADDED_QUALIFIER + WIDE_VOCAB)
def test_added_qualifier_or_wide_negation_side_word_is_a_hard_422_and_saves_nothing_d047(tmp_path, summary, confirm):
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    before, events, calls = DB.get_item(conn, eid), DB.list_events(conn, cid), []
    def spy(*a, **k):
        calls.append(1); return judge("supported")(*a, **k)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary=summary), confirm_warnings=confirm), call=spy)
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and e.value.detail["tokens"]
    assert "does not say" in e.value.message and "reports" not in RV._QUALIFIER_WORDS["self_report"]
    assert DB.get_item(conn, eid) == before and DB.list_events(conn, cid) == events and calls == []


@pytest.mark.parametrize("summary", ["Visit 8: pain 4/10, improving.", "Visit 8: patient reports pain 4/10, improving."])
def test_a_qualifier_the_quote_does_carry_is_not_refused_d047(tmp_path, summary):
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    exc = "Patient reports pain 4/10, improving." if "reports" in summary else _EXC5
    from app.backend import grounding as GR
    assert GR.new_tokens(summary, exc, "Capital PT, visit 8") == [] and GR.added_qualifier_tokens(summary, exc) == []


def test_two_refused_words_read_as_and_not_a_list():
    assert RV._quoted_words(["left", "no"]) == "“left” and “no”" and RV._quoted_words(["left"]) == "“left”"
    assert RV._quoted_words(["a", "b", "c"]) == "“a”, “b” and “c”"


def test_one_vocabulary_serves_the_edit_route_the_generator_check_and_the_gate_d047():
    """grounding.new_tokens is the single source: code_check_failures (gate/accept) and the route both call it, and a summary the route refuses fails the gate check too."""
    from app.backend import grounding as GR
    for s in ADDED_QUALIFIER + WIDE_VOCAB:
        assert GR.new_tokens(s, _EXC5), s
        assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in RV.code_check_failures({"id": "r5", "excerpt": _EXC5, "source": "", "date_iso": ""}, {"summary": s, "excerpt": _EXC5}), s
    assert not hasattr(RV, "_SIDE_NEG")
