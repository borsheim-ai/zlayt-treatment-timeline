"""T-108: the quote picker's sentence units (record_view 'sentences') are cut from the quotable body of a record only: no
`Excerpt:` label, no quote marks around a quoted block, no Date:/Source:/=== header lines. Each unit is a verbatim slice of the case text
at whole-sentence boundaries and passes the same check the save routes run (review.edit / review.manual_entry -> check_excerpt),
ALONE: the picker submits exactly raw[unit.start:unit.end] (app/frontend/excerpt.js), so a sentence that a hedge sentence qualifies is offered as one
combined unit with its hedge (T-108 r2). A record whose Excerpt label cannot be separated from its text offers no units and says why."""
import pathlib

import pytest
from fastapi.testclient import TestClient

from app.backend import grounding, language, present, spanish, store
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G

CASES = G.case_names()
LIBRARY = sorted(p.stem for p in (pathlib.Path(__file__).resolve().parents[2] / "evals" / "library").glob("*.txt"))


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "q.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _case(env, monkeypatch, body):
    db, c = env
    tok = c.post("/api/cases", json=body).json()["token"]
    return db, c, tok


def _check_all_units(db, c, tok, label):
    """Every offered unit, built the way the picker builds it (the text from unit.start to unit.end, nothing added), passes the save-route check."""
    case = c.get(f"/api/cases/{tok}").json()
    conn = DB.connect(db)
    raw = DB.get_case(conn, tok)["raw_text"]
    recs = {r["id"]: r for r in store.load_records(conn, tok, raw)}
    n = 0
    for rv in case["records"]:
        rec = recs[rv["id"]]
        for u in rv["sentences"]:
            n += 1
            quote = raw[u["start"]:u["end"]]
            assert quote == u["text"], "a unit is a verbatim slice of the case text"
            assert rv["char_start"] <= u["start"] < u["end"] <= rv["char_end"]
            assert not u["text"].startswith(("Excerpt", "Date:", "Source:", "===")), u["text"]
            assert not any(q in u["text"] for q in ('"', "\u201c", "\u201d")), u["text"]
            problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], quote)
            assert problems == [], (label, rv["id"], quote, problems)
            assert grounding.locate(rec["excerpt"], quote) is not None
    conn.close()
    return n, case


@pytest.mark.parametrize("name", CASES)
def test_every_offered_unit_saves_alone_golden(env, monkeypatch, name):
    db, c = env
    tok = c.post("/api/cases", json={"text": G.raw(name)}).json()["token"]
    assert _check_all_units(db, c, tok, name)[0]


def test_every_offered_unit_saves_alone_sample(env):
    db, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    n, case = _check_all_units(db, c, tok, "sample")
    assert n
    raw = DB.get_case(DB.connect(db), tok)["raw_text"]
    by_rec = {e["record_ids"][0]: e for e in case["entries"] + case["undated_entries"] if len(e["record_ids"]) == 1}
    for rv in case["records"]:                 # the real routes a picked quote goes to, for every unit of every record
        for u in rv["sentences"]:
            q = raw[u["start"]:u["end"]]
            e = by_rec.get(rv["id"])
            if e:                              # "Change the quote": POST .../items/{id}/review {action: edit, edits: {excerpt}}
                r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "edit", "edits": {"excerpt": q}})
                reasons = (r.json().get("error", {}).get("detail") or {}).get("reasons", []) if r.status_code != 200 else []
                assert not set(reasons) & {"EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "GROUNDING_EXCERPT_NOT_VERBATIM"}, (rv["id"], q, r.text)
                assert r.status_code != 422 or r.json()["error"]["code"] != "invalid_edit", (rv["id"], q, r.text)
            else:                              # record without an entry (tray): manual entry; the first unit saves, later ones meet "already has an entry"
                r = c.post(f"/api/cases/{tok}/records/{rv['id']}/entry", json={"summary": q, "excerpt": q})
                assert r.status_code == 201 or "already has an entry" in r.text, (rv["id"], q, r.text)


@pytest.mark.parametrize("lib", LIBRARY)
def test_every_offered_unit_saves_alone_library(tmp_path, monkeypatch, lib):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "l.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    r = c.post("/api/cases", json={"library": lib})
    assert r.status_code == 201, r.text
    _check_all_units(db, c, r.json()["token"], lib)


def test_hedge_qualified_sentence_is_one_combined_unit(env):
    """Sample record 8: 'C5-C6 disc protrusion with mild right foraminal narrowing.' is qualified by the hedge sentence after it, so it is
    offered together with it; the unit alone saves (201), while the bare sentence is still refused by the route (the rule is unchanged)."""
    db, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    r8 = next(r for r in c.get(f"/api/cases/{tok}").json()["records"] if r["id"] == "r8")
    texts = [s["text"] for s in r8["sentences"]]
    first = next(t for t in texts if t.startswith("C5-C6 disc protrusion with mild right foraminal narrowing."))
    assert first != "C5-C6 disc protrusion with mild right foraminal narrowing." and len(first) > len("C5-C6 disc protrusion with mild right foraminal narrowing.")
    raw = DB.get_case(DB.connect(db), tok)["raw_text"]
    bare = "C5-C6 disc protrusion with mild right foraminal narrowing."
    assert c.post(f"/api/cases/{tok}/records/r8/entry", json={"summary": bare, "excerpt": bare}).status_code == 422
    assert c.post(f"/api/cases/{tok}/records/r8/entry", json={"summary": first, "excerpt": first}).status_code == 201
    assert bare not in texts


def test_golden_hedge_qualified_sentences_are_combined(env):
    """case_08: 'Signal change in the supraspinatus tendon.' is qualified by the hedge sentence after it; it is never offered bare."""
    db, c = env
    name = next(n for n in CASES if n.startswith("case_08"))
    tok = c.post("/api/cases", json={"text": G.raw(name)}).json()["token"]
    texts = [s["text"] for r in c.get(f"/api/cases/{tok}").json()["records"] for s in r["sentences"]]
    assert "Signal change in the supraspinatus tendon." not in texts
    assert any(t.startswith("Signal change in the supraspinatus tendon.") and len(t) > len("Signal change in the supraspinatus tendon.") for t in texts)


def test_sample_units_have_no_wrapper(env):
    db, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    r1 = c.get(f"/api/cases/{tok}").json()["records"][0]
    texts = [s["text"] for s in r1["sentences"]]
    assert texts[0] == "41M restrained driver, rear-ended at approx. 35 mph."
    assert texts[-1] == "Transported to Central ER."          # no closing quote mark
    assert "sentences_reason" not in r1
    assert not any("Excerpt" in t or '"' in t or t.startswith(("Date:", "Source:")) for t in texts)


def _units_of(block, rec=None):
    base, body, why = present.quote_body(block)
    if why:
        return why, []
    units = present.quote_units(body, {"excerpt": body, **(rec or {})})
    return None, [(base + a, base + b) for a, b in units]


def test_quote_body_cases():
    blk = '=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: "One. Two."'
    off, body, why = present.quote_body(blk)
    assert why is None and body == "One. Two." and blk[off:off + len(body)] == body
    assert present.quote_body("Date: 2026-01-01\nSource: X\nExcerpt: Plain text here.")[1] == "Plain text here."
    off, body, why = present.quote_body("Just a paragraph with no labels. Second one.")
    assert why is None and body == "Just a paragraph with no labels. Second one." and off == 0


@pytest.mark.parametrize("txt", ['Excerpt: "Pain persists after two weeks. Taking meds daily."',
                                 'Source: Synthetic Clinic\nExcerpt: "Pain persists after two weeks. Taking meds daily."',
                                 'Date: 2026-01-05\nExcerpt: "Pain persists after two weeks. Taking meds daily."'])
def test_label_only_or_header_missing_records_offer_no_units(txt):
    """T-108 r2 F2: a record with an Excerpt label but no full Date/Source layout keeps the label in the text the save route checks against;
    no unit is offered (never the whole block), and the reason is plain words."""
    recs = ingest_records(txt)
    for rec in recs:
        why, units = _units_of(rec["text"])
        if "Excerpt:" in rec["excerpt"] or "Source:" in rec["excerpt"]:
            assert units == [] and why == present.NO_UNITS_LAYOUT
        else:                                       # date+excerpt: the body is separable, units carry no label or quote mark
            assert why is None and units
            for a, b in units:
                t = rec["text"][a:b]
                assert not t.startswith(("Excerpt", "Source:")) and '"' not in t


def ingest_records(txt):
    from app.backend import ingest
    return ingest.split_records(txt)


def test_record_view_reports_reason_for_label_only_record():
    r = {"id": "r1", "seq": 1, "source_label": "", "date_raw": "", "date_iso": None, "date_status": "missing", "date_candidates": [],
         "duplicate_of": None, "injection_tag": 0, "encounter": 0, "char_start": 0, "char_end": 56}
    raw = 'Excerpt: "Pain persists after two weeks. Taking meds daily."'
    r["char_end"] = len(raw)
    v = present.record_view(r, raw)
    assert v["sentences"] == [] and v["sentences_reason"] == present.NO_UNITS_LAYOUT


def test_units_sit_at_true_offsets_when_source_repeats_the_body():
    """T-108 r2 F3: the Source line repeats the excerpt text; offsets still point into the Excerpt, not the Source line."""
    blk = 'Date: 2026-01-05\nSource: Pain persists. Taking meds daily.\nExcerpt: "Pain persists. Taking meds daily."'
    why, units = _units_of(blk)
    assert why is None and len(units) == 2
    ex = blk.index('Excerpt:')
    for a, b in units:
        assert a > ex and blk[a:b] in ("Pain persists.", "Taking meds daily.")
