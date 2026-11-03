"""D-031 LLM split fallback (T-057): code validates the model's boundaries; LLM_SPLIT on every LLM-split record; failure keeps one record."""
import pytest
from app.backend import ingest as IN, split_llm, pipeline as PL
from app.backend import flag_templates as FT

TEXT = ("March 3, 2026\nDr. Rowan Pell, orthopedics. Right wrist swelling after a fall. X-ray shows a distal radius fracture.\n\n"
        "March 17, 2026\nDr. Rowan Pell, orthopedics. Splint removed. Pain 2/10.\n")
T = IN.normalize_text(TEXT)
SECOND = T.index("March 17")


def test_code_split_finds_one_unsplit_block_without_a_splitter():
    r = IN.ingest(TEXT)
    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and not any(w["code"] == "LLM_SPLIT" for w in r["warnings"])


def test_no_model_for_unsplit_paste_emits_split_rejected_no_model():
    w = {x["code"]: x for x in IN.ingest(TEXT)["warnings"]}
    assert "SPLIT_AMBIGUOUS" in w
    assert "SPLIT_REJECTED" in w and "No model" in w["SPLIT_REJECTED"]["message"]


def test_confident_code_split_without_model_has_no_split_rejected():
    codes = [x["code"] for x in IN.ingest("Date: 2026-03-03\nSource: Clinic\nExcerpt: Neck pain.")["warnings"]]
    assert "SPLIT_REJECTED" not in codes


def test_valid_llm_split_makes_two_records_each_flagged():
    r = IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
    assert [x["char_start"] for x in r["records"]] == [0, SECOND] and r["split_method"] == "llm"
    assert r["records"][0]["date_raw"] == "March 3, 2026" and r["records"][1]["date_iso"] == "2026-03-17"
    assert [w["category"] for w in r["record_warnings"]] == ["llm_split", "llm_split"]
    assert all(w["reasons"] == ["LLM_SPLIT"] and w["title"] for w in r["record_warnings"])
    assert any(w["code"] == "LLM_SPLIT" for w in r["warnings"])
    for x in r["records"]:                      # every record text is a verbatim slice of the input
        assert T[x["char_start"]:x["char_end"]] == x["text"]


@pytest.mark.parametrize("bad", [
    [(0, SECOND + 3), (SECOND + 3, None)],            # not on a line start
    [(0, SECOND), (SECOND, 5)],                        # does not reach the end
    [(1, SECOND), (SECOND, 10 ** 6)],                  # does not start at 0 / overruns
    [(0, SECOND), (SECOND + 1, len(T))],               # gap
    [(0, len(T))],                                     # one span: nothing to split
    [(0, SECOND), (SECOND - 5, len(T))],               # overlap
])
def test_invalid_boundaries_keep_one_record(bad):
    bad = [(a, len(T) if b is None else b) for a, b in bad]
    r = IN.ingest(TEXT, splitter=lambda t: bad)
    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and not any(w["category"] == "llm_split" for w in r["record_warnings"])
    with pytest.raises(ValueError):
        IN.validate_split(T, bad)


def test_splitter_failure_keeps_one_record_with_a_reason():
    def boom(t):
        raise IN.SplitFailed("LLM_FAILED_AFTER_RETRIES")
    r = IN.ingest(TEXT, splitter=boom)
    assert len(r["records"]) == 1 and r["split_failure"] == "LLM_FAILED_AFTER_RETRIES" and r["split_method"] == "ambiguous"
    assert any(w["code"] == "SPLIT_AMBIGUOUS" for w in r["warnings"]) and any(w["code"] == "SPLIT_REJECTED" for w in r["warnings"])


def test_unexpected_splitter_errors_propagate():
    def boom(t):
        raise RuntimeError("down")
    with pytest.raises(RuntimeError):
        IN.ingest(TEXT, splitter=boom)


def test_splitter_not_called_when_code_split_is_confident():
    from tests.unit import _golden as G
    called = []
    r = IN.ingest(G.raw("sample"), splitter=lambda t: called.append(1))
    assert not called and r["split_method"] == "code" and len(r["records"]) == 9


def test_numbered_labels_every_line_with_its_offset():
    n = IN.numbered(T)
    assert f"@{SECOND}| March 17, 2026" in n and n.startswith("@0| March 3, 2026")


def test_make_splitter_sends_numbered_nonce_wrapped_text_and_returns_spans():
    seen = {}
    def call(step, system, user, schema, *, item_id=None):
        seen.update(step=step, user=user, schema=schema, item_id=item_id)
        return {"records": [{"start": 0, "end": SECOND}, {"start": SECOND, "end": len(T)}]}, "c1"
    spans = split_llm.make_splitter(call)(T)
    assert spans == ([(0, SECOND), (SECOND, len(T))], "c1") and seen["step"] == "split"
    assert f"@{SECOND}|" in seen["user"] and "<record-" in seen["user"] and f"TOTAL: {len(T)}" in seen["user"]


def test_template_renders_for_llm_split():
    title, expl = FT.render("record_warning", "llm_split")
    assert "AI" in title and "AI" in expl


# ---- recorded fixture replay (python -m app.llm.record evals/golden/unsplit_paste.txt, LLM_FIXTURE_DIR=tests/fixtures/llm/split)
import json, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
EXP = json.loads((ROOT / "evals" / "golden" / "unsplit_paste.split.json").read_text())


@pytest.fixture
def replay(monkeypatch, tmp_path):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(ROOT / "tests" / "fixtures" / "llm" / "split"))
    from app.db import db as DB
    from app.llm import audited as AU
    raw = (ROOT / "evals" / "golden" / EXP["input_file"]).read_text()
    conn = DB.connect(str(tmp_path / "s.sqlite"))
    cid = DB.create_case(conn, raw, now=1.0)
    return conn, cid, raw, AU.make_call(conn, cid)


def test_golden_unsplit_paste_code_split_is_one_block():
    raw = (ROOT / "evals" / "golden" / EXP["input_file"]).read_text()
    r = IN.ingest(raw)
    assert len(r["records"]) == EXP["code_split"]["record_count"] and r["split_method"] == EXP["code_split"]["split_method"]


def test_golden_unsplit_paste_replays_recorded_split_through_audited(replay):
    from app.db import db as DB
    conn, cid, raw, call = replay
    ing = PL.run_ingest(raw, call=call)
    assert ing["split_method"] == EXP["llm_split"]["split_method"]
    got = [(r["n"], r["date_iso"], r["source"], r["text"].startswith(e["starts_with"])) for r, e in zip(ing["records"], EXP["records"])]
    assert got == [(e["record_no"], e["date"], e["source"], True) for e in EXP["records"]] and len(ing["records"]) == len(EXP["records"])
    warns = [f for f in ing["flags"] if f["type"] == "record_warning" and f["category"] == EXP["llm_split"]["record_warning_category"]]
    assert sorted(f["record_nos"][0] for f in warns) == [1, 2, 3] and all(f["reasons"] == ["LLM_SPLIT"] and f["state"] == "needs_review" for f in warns)
    assert any(w["code"] == "LLM_SPLIT" for w in ing["warnings"])
    rows = [c for c in DB.list_llm_calls(conn, cid) if c["step"] == "split"]          # the ladder record: one audited row, parsed
    assert len(rows) == 1 and rows[0]["parsed_ok"] == 1 and rows[0]["role"] == "generator"


def test_run_pipeline_replaces_the_single_stored_record(replay):
    """The case is created with the one unsplit record (code only); the run replaces it with the three LLM-split records."""
    from app.db import db as DB
    conn, cid, raw, call = replay
    PL.ingest_case(conn, cid, raw, 1.0)
    assert DB.table_counts(conn, cid)["records"] == 1
    PL.run_pipeline(conn, cid, raw, call=call, now=2.0)         # the other steps have no fixtures: they fail visibly, the split does not
    assert DB.table_counts(conn, cid)["records"] == 3


# ---- T-057 r1: each AC1 clause pinned on its own (line starts are valid in these, only the named defect is present)
T3 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
L2, L3 = T3.index("May 11"), T3.index("May 25")


@pytest.mark.parametrize("spans,code", [
    ([(0, L2), (L2, L3)], "SPLIT_NOT_COVERING"),                 # all starts on line starts, but the last record's text is dropped
    ([(0, L2), (L3, len(T3))], "SPLIT_NOT_CONTIGUOUS"),          # all starts on line starts, but the middle text is dropped
    ([(0, L3), (L2, len(T3))], "SPLIT_NOT_CONTIGUOUS"),          # overlap on line starts
])
def test_coverage_and_contiguity_are_checked_independently_of_line_starts(spans, code):
    with pytest.raises(ValueError, match=code):
        IN.validate_split(T3, spans)
    assert len(IN.ingest(T3, splitter=lambda t: spans)["records"]) == 1


def test_too_many_records_falls_back_to_one_record_not_input_too_large():
    lines = "".join(f"May {1 + i % 28}, 2026\nNote {i}.\n" for i in range(45))
    t = IN.normalize_text(lines)
    starts = [0] + [t.index(f"Note {i}.") - len(f"May {1 + i % 28}, 2026\n") for i in range(1, 45)]
    spans = list(zip(starts, starts[1:] + [len(t)]))
    r = IN.ingest(t, splitter=lambda x: spans)
    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and r["split_failure"] == "SPLIT_TOO_MANY"


def test_llm_split_flag_span_is_absolute_and_carries_the_call_id():
    r = IN.ingest(TEXT, splitter=lambda t: ([(0, SECOND), (SECOND, len(t))], "c42"))
    for w in r["record_warnings"]:
        ev, rec = w["evidence"][0], next(x for x in r["records"] if x["n"] == w["record_no"])
        assert T[ev["start"]:ev["end"]] == ev["text"] and rec["char_start"] <= ev["start"] and ev["end"] <= rec["char_end"]
        assert w["call_id"] == "c42"


def test_banner_is_in_no_record_prompt_and_code_agree():
    from tests.unit import _golden as G
    raw = (ROOT / "evals" / "golden" / "unsplit_paste.txt").read_text()
    t = IN.normalize_text(raw)
    i = t.index("May 11, 2026")
    r = IN.ingest(raw, splitter=lambda x: [(0, i), (i, len(x))])
    assert r["records"][0]["char_start"] == t.index("May 4, 2026") and "SYNTHETIC" not in r["records"][0]["text"]
    from app.llm import promptlib
    assert "leaves a leading banner line out" in promptlib.load("split_v1").text


def _extract(u):
    import re
    body = re.search(r"RECORD TEXT:\n<record-\w+>\n(.*?)\n</record-", u, re.S).group(1)
    s = body.split(". ")[0].rstrip(".") + "."
    return dict(summary=s, excerpt=s)


def _stub_call(spans_by_run):
    """Fake audited call: extract returns the record's first sentence; the split step returns the next scripted boundary list."""
    from tests.unit._fakes import FakeCall, sample_script
    runs = iter(spans_by_run)
    extract = _extract
    return FakeCall(sample_script(extract=extract, split=lambda u: {"records": [{"start": a, "end": b} for a, b in next(runs)]}))


def test_rerun_with_different_boundaries_replaces_the_stored_records(tmp_path):
    """T-057 r1 blocker: same record count, different spans -> the records table follows the latest accepted split."""
    from app.db import db as DB
    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
    a2, a3 = T4.index("May 11"), T4.index("May 25")
    b2 = T4.index("Dr. A, ortho. Pain")                                         # a different, still line-start-valid, boundary
    A = [(0, a2), (a2, a3), (a3, len(T4))]
    B = [(0, b2), (b2, a3), (a3, len(T4))]
    call = _stub_call([A, B])
    conn = DB.connect(str(tmp_path / "s.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
    starts = lambda: [r[0] for r in conn.execute("SELECT char_start FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    assert starts() == [a for a, _ in A]
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
    assert starts() == [a for a, _ in B] and starts() != [a for a, _ in A]
    for e in DB.list_items(conn, cid, "entry"):
        rec = next(r for r in conn.execute("SELECT char_start, char_end FROM records WHERE case_id=? AND id=?", (cid, e["record_ids"][0])))
        assert e["excerpt"] in T4[rec[0]:rec[1]]


@pytest.mark.parametrize("second", ["call_fails", "invalid_spans"])
def test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent(tmp_path, second):
    """T-057 r2 blocker (probe_rerun_fail2): run 1 model-split into 3 records; run 2's split fails / is rejected -> one record. Stored
    records must equal run 2's records and every entry excerpt must be a substring of its own stored record."""
    from app.db import db as DB
    from app.llm import audited as AU
    from tests.unit._fakes import FakeCall, sample_script
    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
    a2, a3 = T4.index("May 11"), T4.index("May 25")
    A = [(0, a2), (a2, a3), (a3, len(T4))]
    runs = iter([A, second])

    def split(u):
        v = next(runs)
        if v == "call_fails":
            raise AU.LLMFailed("down")
        if v == "invalid_spans":
            return {"records": [{"start": 0, "end": 10}, {"start": 10, "end": 20}]}      # does not cover the text
        return {"records": [{"start": a, "end": b} for a, b in v]}
    call = FakeCall(sample_script(extract=_extract, split=split))
    conn = DB.connect(str(tmp_path / "c.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
    assert DB.table_counts(conn, cid)["records"] == 3
    out = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
    stored = [tuple(r) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    assert stored == [(r["id"], r["char_start"], r["char_end"]) for r in out["records"]] and len(stored) == 1
    spans = {r[0]: (r[1], r[2]) for r in stored}
    entries = DB.list_items(conn, cid, "entry")
    assert entries
    for e in entries:
        a, b = spans[e["record_ids"][0]]
        assert e["excerpt"] in T4[a:b], e["id"]


def test_value_error_outside_validate_split_is_not_reported_as_a_rejected_split(monkeypatch):
    def boom(text, spans):
        raise ValueError("programming error")
    monkeypatch.setattr(IN, "_llm_records", boom)
    with pytest.raises(ValueError, match="programming error"):
        IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])


def test_split_call_failure_reaches_the_run_errors_and_is_audited_with_prompt_version(tmp_path):
    from app.db import db as DB
    from app.llm import audited as AU
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "f.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    out = PL.run_pipeline(conn, cid, TEXT, call=FakeCall(sample_script(extract=_extract, split=AU.LLMFailed("down"))), now=lambda: 1.0)
    assert {"code": "LLM_FAILED_AFTER_RETRIES", "stage": "split"} == {k: v for k, v in next(e for e in out["errors"] if e["stage"] == "split").items() if k in ("code", "stage")}
    assert DB.table_counts(conn, cid)["records"] == 1


def test_split_audit_row_has_prompt_version_and_flag_resolves_to_call(replay):
    from app.db import db as DB
    conn, cid, raw, call = replay
    ing = PL.run_ingest(raw, call=call)
    row = next(c for c in DB.list_llm_calls(conn, cid) if c["step"] == "split")
    assert row["prompt_version"] == "split_v1"
    flags = [f for f in ing["flags"] if f.get("category") == "llm_split"]
    assert flags and all(f["ladder"]["generator"]["call_id"] == row["id"] and f["ladder"]["generator"]["prompt_version"] == "split_v1" for f in flags)


@pytest.mark.parametrize("second", ["call_fails", "different_bounds"])
def test_rerun_after_decisions_reuses_stored_records_and_never_resplits(tmp_path, second):
    """T-057 r3 blocker / D-039: every entry of run 1 is accepted; run 2's split would fail or move the boundaries. The records are
    frozen: no split call is made, every entry's record_ids resolve and its excerpt lies inside that stored record."""
    from app.db import db as DB
    from app.llm import audited as AU
    from tests.unit._fakes import FakeCall, sample_script
    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
    a2, a3 = T4.index("May 11"), T4.index("May 25")
    b2 = T4.index("Dr. A, ortho. Pain")
    A = [(0, a2), (a2, a3), (a3, len(T4))]
    runs, calls = iter([A, second]), []

    def split(u):
        v = next(runs)
        calls.append(v)
        if v == "call_fails":
            raise AU.LLMFailed("down")
        spans = A if v == A else [(0, b2), (b2, a3), (a3, len(T4))]
        return {"records": [{"start": a, "end": b} for a, b in spans]}
    call = FakeCall(sample_script(extract=_extract, split=split))
    conn = DB.connect(str(tmp_path / "d.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
    stored = lambda: [tuple(r) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    run1 = stored()
    assert len(run1) == 3
    entries = DB.list_items(conn, cid, "entry")
    for e in entries:
        DB.apply_review(conn, e["id"], "accept", now=1.5, case=cid)
    out = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
    assert len(calls) == 1, "a re-run with decided items must not call the split step"
    assert stored() == run1
    assert [(r["id"], r["char_start"], r["char_end"]) for r in out["records"]] == run1
    spans = {r[0]: (r[1], r[2]) for r in stored()}
    after = DB.list_items(conn, cid, "entry")
    assert {e["id"] for e in after} >= {e["id"] for e in entries}
    for e in after:
        assert e["record_ids"] and all(rid in spans for rid in e["record_ids"]), e["id"]
        a, b = spans[e["record_ids"][0]]
        assert e["excerpt"] in T4[a:b], e["id"]
        if e["id"] in {x["id"] for x in entries}:
            assert e["review_status"] == "accepted"


def test_resplit_stays_allowed_while_every_entry_is_pending(tmp_path):
    from app.db import db as DB
    from tests.unit._fakes import FakeCall, sample_script
    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
    a2, a3 = T4.index("May 11"), T4.index("May 25")
    runs, n = iter([[(0, a2), (a2, len(T4))], [(0, a2), (a2, a3), (a3, len(T4))]]), []
    call = FakeCall(sample_script(extract=_extract, split=lambda u: n.append(1) or {"records": [{"start": a, "end": b} for a, b in next(runs)]}))
    conn = DB.connect(str(tmp_path / "p.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
    assert len(n) == 2 and DB.table_counts(conn, cid)["records"] == 3


# ---- T-066 r2: run path with a missing fixture, and a multi-record paste with an unsplit tail
def test_run_pipeline_fixture_miss_emits_split_rejected_no_model(monkeypatch, tmp_path):
    """F1: the run path (a splitter is always wired) with no recorded split answer reports SPLIT_REJECTED / NO_MODEL; the FIXTURE_MISS detail stays in errors."""
    from app.db import db as DB
    from app.llm import audited as AU
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path / "empty"))
    conn = DB.connect(str(tmp_path / "m.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    out = PL.run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid), now=lambda: 1.0)
    rej = [w for w in out["warnings"] if w["code"] == "SPLIT_REJECTED"]
    assert len(rej) == 1 and "No model" in rej[0]["message"] and "FIXTURE_MISS" not in rej[0]["message"]
    assert out["split_failure"] == "NO_MODEL" and out["split_method"] == "ambiguous"
    errs = [e for e in out["errors"] if e["stage"] == "split"]
    assert len(errs) == 1 and errs[0]["code"] == "LLM_FAILED_AFTER_RETRIES" and errs[0]["cause"] == "FIXTURE_MISS"


TAIL = ("Date: 2026-03-03\nSource: Clinic A\nExcerpt: Neck pain.\n---\nDate: 2026-03-10\nSource: Clinic A\nExcerpt: Follow up.\n---\n"
        "Free text with no label at all.\n")


def test_multi_record_paste_with_unsplit_tail_gets_a_reason():
    """F2: the model is only asked about a single block, so a leftover tail gets SPLIT_REJECTED / NOT_ATTEMPTED, with or without a splitter."""
    for splitter in (None, lambda t: pytest.fail("the splitter must not be called for a multi-record paste")):
        r = IN.ingest(TAIL, splitter=splitter)
        assert len(r["records"]) == 3 and r["split_method"] == "ambiguous" and r["split_failure"] == "NOT_ATTEMPTED"
        w = {x["code"]: x for x in r["warnings"]}
        assert "SPLIT_AMBIGUOUS" in w and "NOT_ATTEMPTED" in w["SPLIT_REJECTED"]["message"]


def test_fully_labelled_multi_record_paste_has_no_split_rejected():
    r = IN.ingest("Date: 2026-03-03\nSource: Clinic A\nExcerpt: Neck pain.\n---\nDate: 2026-03-10\nSource: Clinic A\nExcerpt: Follow up.\n")
    assert r["split_method"] == "code" and r["split_failure"] is None and "SPLIT_REJECTED" not in [w["code"] for w in r["warnings"]]


# ---- T-057 r4 minor 1: each D-039 freeze trigger on its own (a single decided item of one kind freezes the stored records)
@pytest.mark.parametrize("kind,action", [("entry", "accept"), ("entry", "edit"), ("entry", "dismiss"), ("amount", "accept"), ("flag", "accept")])
def test_each_decision_kind_freezes_the_stored_records_on_its_own(tmp_path, kind, action):
    """Only one item is decided, and only its kind/action differs per case; the other items stay pending. The re-run must make no split
    call and keep the stored records, so a trigger limited to accepted entries (or to entries) fails here."""
    from app.db import db as DB
    from tests.unit._fakes import FakeCall, sample_script
    T5 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling. Charge $1,200.00 for the visit.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\n"
                           "June 25, 2026\nDr. A, ortho. Splint removed.\n")
    a2, a3 = T5.index("May 11"), T5.index("June 25")
    A, B = [(0, a2), (a2, a3), (a3, len(T5))], [(0, T5.index("Dr. A, ortho. Pain")), (T5.index("Dr. A, ortho. Pain"), a3), (a3, len(T5))]
    runs, calls = iter([A, B]), []
    call = FakeCall(sample_script(extract=_extract, split=lambda u: calls.append(1) or {"records": [{"start": a, "end": b} for a, b in next(runs)]}))
    conn = DB.connect(str(tmp_path / "k.sqlite")); cid = DB.create_case(conn, T5, now=1.0)
    PL.run_pipeline(conn, cid, T5, call=call, now=lambda: 1.0)
    stored = lambda: [tuple(r) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    run1, items = stored(), DB.list_items(conn, cid, kind)
    assert len(run1) == 3 and items, kind
    assert not any(i["review_status"] != "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k))
    DB.apply_review(conn, items[0]["id"], action, edited={"summary": "Edited."} if action == "edit" else None, now=1.5, case=cid)
    PL.run_pipeline(conn, cid, T5, call=call, now=lambda: 2.0)
    assert len(calls) == 1, f"{kind} {action} must freeze the records (no second split call)"
    assert stored() == run1


# ---- T-066 r3: one incomplete record, the single-record gate, and the reason surviving a re-run after a decision
def test_single_incomplete_labelled_record_never_claims_several_records():
    paste = "Date: 2026-03-03\nSource: Clinic A\n"          # date and source present, excerpt missing: not an unsplit block, not several records
    for splitter in (None, lambda t: pytest.fail("a labelled single record is not an unsplit block")):
        r = IN.ingest(paste, splitter=splitter)
        assert len(r["records"]) == 1
        assert not any("several records" in w["message"] for w in r["warnings"])
        assert r["split_failure"] != "NOT_ATTEMPTED"


def test_splitter_is_only_called_for_a_single_block_never_for_several_records():
    """r2 major 2: an unlabelled first block followed by two labelled records is several records; the model is never asked."""
    paste = "Some free text first.\n---\nDate: 2026-03-03\nSource: Clinic A\nExcerpt: Neck pain.\n---\nDate: 2026-03-10\nSource: Clinic A\nExcerpt: Follow up.\n"
    calls = []
    r = IN.ingest(paste, splitter=lambda t: calls.append(t) or [(0, len(t))])
    assert len(r["records"]) == 3 and calls == [] and r["split_failure"] == "NOT_ATTEMPTED"
    one = []                                                    # and the single unsplit block does reach the splitter
    IN.ingest("Neck pain after the crash. Seen at Clinic A.", splitter=lambda t: one.append(t) or None)
    assert len(one) == 1


def test_rerun_after_a_decision_keeps_the_split_rejected_reason(monkeypatch, tmp_path):
    """T-063 r3 minor (D-039): the first run could not split (no recorded answer); once an item is decided the records are frozen and the
    re-run makes no split call, yet the SPLIT_REJECTED warning is still shown and no new split error is recorded."""
    from app.db import db as DB
    from app.llm import audited as AU
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path / "empty"))
    conn = DB.connect(str(tmp_path / "k.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    first = PL.run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid), now=lambda: 1.0)
    assert first["split_failure"] == "NO_MODEL"
    item = next(i for k in ("flag", "amount") for i in DB.list_items(conn, cid, k))
    DB.apply_review(conn, item["id"], "accept", now=1.5, case=cid)
    n_split = len(DB.list_llm_calls(conn, cid, "split"))
    out = PL.run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid), now=lambda: 2.0)
    rej = [w for w in out["warnings"] if w["code"] == "SPLIT_REJECTED"]
    assert out["split_failure"] == "NO_MODEL" and len(rej) == 1 and "No model" in rej[0]["message"]
    assert len(DB.list_llm_calls(conn, cid, "split")) == n_split
    assert not [e for e in out["errors"] if e["stage"] == "split"]


def test_rerun_after_a_decision_replays_a_failed_split_reason_without_a_new_error(tmp_path):
    """The stored reason of a failed model call is shown again, but the frozen re-run made no call, so it records no new split error."""
    from app.db import db as DB
    from app.llm import audited as AU
    from tests.unit._fakes import FakeCall, sample_script

    def down(u):
        raise AU.LLMFailed("down")
    call = FakeCall(sample_script(extract=_extract, split=down))
    conn = DB.connect(str(tmp_path / "f.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    first = PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 1.0)
    assert [e["stage"] for e in first["errors"] if e["stage"] == "split"] == ["split"] and first["split_failure"]
    item = next(i for k in ("flag", "amount", "entry") for i in DB.list_items(conn, cid, k))
    DB.apply_review(conn, item["id"], "accept", now=1.5, case=cid)
    out = PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 2.0)
    assert out["split_failure"] == first["split_failure"] and any(w["code"] == "SPLIT_REJECTED" for w in out["warnings"])
    assert not [e for e in out["errors"] if e["stage"] == "split"]
