"""T-050: many cases share one sqlite file; ids are short per case and never collide; delete_case touches only its own rows."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record


def seeded(conn, case, text):
    cid = DB.create_case(conn, text, now=1.0)
    PL.ingest_case(conn, cid, text, 1.0)
    return cid


def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a = seeded(conn, "sample", G.raw("sample"))
    b = seeded(conn, "case_01", G.raw("case_01_date_formats"))
    c = seeded(conn, "sample again", G.raw("sample"))
    ids = lambda cid: sorted(r["id"] for r in DB.list_items(conn, cid, "flag"))   # noqa: E731
    assert ids(a) == ids(c) and ids(a)                                              # same short ids in two cases
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (a,)).fetchone()[0] == 9
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (b,)).fetchone()[0] >= 8


def test_full_pipeline_twice_in_one_file(tmp_path):
    sums = golden_summaries()
    script = {"extract": lambda u: dict(summary=sums[which_record(u)[0]][0], excerpt=sums[which_record(u)[0]][1]),
              "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"}, "j3": {"verdict": "conflict", "reason_code": "NONE"},
              "j4": {"verdict": "agree", "reason_code": "NONE"}, "conflicts": {"flags": []}, "flags": {"flags": []}}
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    outs = []
    for _ in range(2):
        cid = DB.create_case(conn, G.raw("sample"), now=1.0)
        outs.append((cid, PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script), now=lambda: 1.0)))
    (a, oa), (b, ob) = outs
    assert [e["id"] for e in oa["entries"]] == [e["id"] for e in ob["entries"]] and len(oa["entries"]) == 9
    eid = oa["entries"][0]["id"]
    with pytest.raises(ValueError):                      # a bare id is ambiguous once two cases hold it
        DB.get_item(conn, eid)
    assert DB.get_item(conn, eid, a)["case_id"] == a and DB.get_item(conn, eid, b)["case_id"] == b
    DB.apply_review(conn, eid, "accept", now=2.0, case=a)
    assert DB.get_item(conn, eid, a)["review_status"] == "accepted" and DB.get_item(conn, eid, b)["review_status"] == "pending"


def test_delete_case_removes_only_that_case(tmp_path):
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a = seeded(conn, "a", G.raw("sample"))
    b = seeded(conn, "b", G.raw("sample"))
    for cid in (a, b):                                   # give both cases an audit row and an event so every table has content
        DB.add_llm_call(conn, cid, "prompt text", "{}", now=1.0)
        DB.apply_review(conn, DB.list_items(conn, cid, "flag")[0]["id"], "accept", now=2.0, case=cid)
    before = DB.table_counts(conn, b)
    DB.delete_case(conn, a)
    assert DB.get_case(conn, a) is None
    for t in DB._CASE_TABLES:                            # every per-case table, prompts included
        col = "id" if t == "cases" else "case_id"
        assert conn.execute(f"SELECT count(*) FROM {t} WHERE {col}=?", (a,)).fetchone()[0] == 0, t
    assert DB.table_counts(conn, b) == before and before["records"] == 9 and before["llm_calls"] == 1


def test_case_scoped_lookup_and_ambiguous_bare_id(tmp_path):
    """AC1 (named in test_db/test_pipeline too): case= scopes get_item/apply_review; a bare id held by two cases raises."""
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a, b = seeded(conn, "a", G.raw("sample")), seeded(conn, "b", G.raw("sample"))
    fid = DB.list_items(conn, a, "flag")[0]["id"]
    with pytest.raises(ValueError):
        DB.get_item(conn, fid)
    DB.apply_review(conn, fid, "dismiss", now=3.0, case=b)
    assert DB.get_item(conn, fid, b)["review_status"] == "dismissed" and DB.get_item(conn, fid, a)["review_status"] == "pending"
    with pytest.raises(KeyError):
        DB.get_item(conn, fid, "nonexistent-case")


def test_old_schema_file_is_deleted_and_rebuilt(tmp_path, caplog):
    """T-050 r2 / T-040 security r2: a file from schema version 1 is deleted (no *.old copy keeps its text) and a fresh v2 file is created; one log line."""
    import glob, sqlite3
    path = str(tmp_path / "old.sqlite")
    old = sqlite3.connect(path)
    old.executescript("CREATE TABLE cases (id TEXT PRIMARY KEY, raw_text TEXT); CREATE TABLE records (id TEXT PRIMARY KEY, case_id TEXT);"
                      "INSERT INTO cases VALUES ('x', 'SYNTHETIC old pasted text');")
    old.commit(); old.close()
    caplog.set_level("WARNING", logger="zlayt.db")
    conn = DB.connect(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION and conn.execute("SELECT count(*) FROM cases").fetchone()[0] == 0
    assert glob.glob(str(tmp_path / "old.sqlite*")) == [path] or sorted(glob.glob(str(tmp_path / "*"))) == [path]       # nothing else left behind
    assert b"SYNTHETIC old pasted text" not in open(path, "rb").read()
    assert len([r for r in caplog.records if r.name == "zlayt.db"]) == 1 and "SYNTHETIC" not in caplog.text
    DB.connect(path).close()                              # reopening a current file deletes nothing
    assert DB.connect(path).execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION
