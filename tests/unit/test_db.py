"""Persistence, deletion, purge. ADR-006, R-PR-* privacy (delete_case = purge function), R-RV-5; db worker owns app/db."""
import pytest
from app.db import db as DB

H24 = 24 * 3600

@pytest.fixture
def conn(tmp_path):
    return DB.connect(str(tmp_path / "t.sqlite"))

def seed(conn, now=1000.0):
    cid = DB.create_case(conn, "SYNTHETIC raw text", now=now)
    DB.add_item(conn, cid, "entry", {"summary": "x"}, now=now)
    DB.add_llm_call(conn, cid, prompt="PROMPT with record text", response="RESPONSE", now=now)
    return cid

def test_delete_case_empties_every_table_including_prompts(conn):
    """ADR-006 / privacy: delete_case removes the case from EVERY table (cases, records, items, llm_calls prompts, events)."""
    cid = seed(conn)
    other = seed(conn)
    assert sum(DB.table_counts(conn, cid).values()) > 0
    DB.delete_case(conn, cid)
    assert sum(DB.table_counts(conn, cid).values()) == 0
    assert sum(DB.table_counts(conn, other).values()) > 0      # other cases untouched

def test_llm_calls_table_is_among_the_deleted(conn):
    """ADR-006: stored prompts live in llm_calls and are covered by delete_case."""
    cid = seed(conn)
    assert DB.table_counts(conn, cid).get("llm_calls", 0) >= 1
    DB.delete_case(conn, cid)
    assert DB.table_counts(conn, cid).get("llm_calls", 0) == 0

def test_purge_after_24h_with_injectable_now(conn):
    """ADR-006: cases older than 24 h are purged lazily; `now` is injectable (no sleeping)."""
    cid = seed(conn, now=1000.0)
    assert DB.purge_expired(conn, now=1000.0 + H24 - 1) == 0
    assert sum(DB.table_counts(conn, cid).values()) > 0
    assert DB.purge_expired(conn, now=1000.0 + H24 + 1) == 1
    assert sum(DB.table_counts(conn, cid).values()) == 0

def test_purge_uses_the_same_deletion_path(conn):
    """ADR-006: purge and DELETE are one function - a purged case leaves no row in any table (prompts included)."""
    cid = seed(conn)
    DB.purge_expired(conn, now=1000.0 + H24 + 1)
    assert all(v == 0 for v in DB.table_counts(conn, cid).values())

@pytest.mark.parametrize("status", ["pending", "accepted", "edited", "dismissed"])
def test_review_status_round_trip(conn, status):
    """R-RV-5 / ADR-005: review_status persists and reads back; new items start pending."""
    cid = seed(conn)
    iid = DB.add_item(conn, cid, "entry", {"summary": "y"})
    assert DB.get_item(conn, iid)["review_status"] == "pending"
    DB.set_review_status(conn, iid, status, edited={"summary": "z"} if status == "edited" else None)  # T-031 r2: edit needs a payload
    assert DB.get_item(conn, iid)["review_status"] == status

def test_invalid_review_status_rejected(conn):
    """ADR-005: only pending|accepted|edited|dismissed are valid; nothing else is stored."""
    cid = seed(conn); iid = DB.add_item(conn, cid, "entry", {})
    with pytest.raises(ValueError):
        DB.set_review_status(conn, iid, "auto_accepted")


# --- added by db worker for T-031 round 2 (staff-engineer findings); qa may fold into its own layout ---
import pathlib, re

def _entry(conn, cid, **p):
    return DB.add_item(conn, cid, "entry", {"summary": "orig", **p})

def test_review_status_round_trip_new_connection(tmp_path):
    """R-RV-8: status and the edit persist on a second connection; the original stays in its own column."""
    path = str(tmp_path / "p.sqlite")
    c1 = DB.connect(path); cid = DB.create_case(c1, "t", now=1); iid = _entry(c1, cid)
    DB.apply_review(c1, iid, "edit", edited={"summary": "new"}, now=2); c1.close()
    got = DB.get_item(DB.connect(path), iid)
    assert got["review_status"] == "edited" and got["edited"] == {"summary": "new"} and got["summary"] == "orig"

def test_ladder_roundtrip(tmp_path):
    """AC2: D.4 ladder + backend, call ids and a recorded llm_calls row survive a new connection."""
    path = str(tmp_path / "l.sqlite")
    c1 = DB.connect(path); cid = DB.create_case(c1, "t", now=1)
    call = DB.add_llm_call(c1, cid, prompt="u", response="r", now=2, system="s", role="judge", step="judge_entries",
                           backend="fixture", model="m", prompt_version="judge_faithfulness_v1", verdict="supported",
                           latency_ms=5, cost_usd=0.0, attempt=1)
    ladder = {"item_id": "e1", "backend": "fixture", "generator": {"model": "g", "prompt_version": "extract_v1", "call_id": "c0"},
              "code_checks": {"excerpt_verbatim": True}, "judge": {"verdict": "supported", "call_id": call},
              "state": "verified", "human": {"action": None, "edited_text": None, "at": None}}
    iid = _entry(c1, cid, ladder_json=ladder); c1.close()
    c2 = DB.connect(path)
    assert DB.get_item(c2, iid)["ladder"] == ladder
    row = DB.get_llm_call(c2, call)
    assert (row["backend"], row["model"], row["prompt_version"], row["verdict"], row["latency_ms"]) == ("fixture", "m", "judge_faithfulness_v1", "supported", 5)
    assert len(row["prompt_sha256"]) == 64 and row["user_text"] == "u" and row["response_raw"] == "r"

def test_apply_review_logs_before_after_and_keeps_original(conn):
    cid = seed(conn); iid = _entry(conn, cid)
    DB.apply_review(conn, iid, "edit", edited={"summary": "new"}, now=5)
    DB.apply_review(conn, iid, "accept", now=6)
    ev = DB.list_events(conn, cid, iid)
    assert [e["action"] for e in ev] == ["edit", "accept"]
    assert ev[0]["before"] == {"review_status": "pending", "edited": None}
    assert ev[0]["after"] == {"review_status": "edited", "edited": {"summary": "new"}}
    assert ev[1]["before"]["review_status"] == "edited" and ev[1]["after"]["review_status"] == "accepted"
    assert DB.get_item(conn, iid)["summary"] == "orig"

def test_edit_without_payload_raises(conn):
    cid = seed(conn); iid = _entry(conn, cid)
    for call in (lambda: DB.apply_review(conn, iid, "edit"), lambda: DB.set_review_status(conn, iid, "edited")):
        with pytest.raises(ValueError):
            call()
    assert DB.get_item(conn, iid)["review_status"] == "pending" and DB.list_events(conn, cid) == []

def test_update_item_cannot_write_edits_status_or_ids(conn):
    cid = seed(conn); iid = _entry(conn, cid)
    for bad in ({"edited_json": {"summary": "X"}}, {"edited": {"summary": "X"}}, {"id": "e999"}, {"review_status": "accepted"}, {"case_id": "z"}):
        with pytest.raises(ValueError):
            DB.update_item(conn, iid, **bad)
    DB.update_item(conn, iid, state="verified", ladder={"backend": "fixture"}, now=3)       # allowed fields still work
    assert DB.get_item(conn, iid)["ladder"] == {"backend": "fixture"} and DB.list_events(conn, cid) == []

def test_secure_delete_is_on(conn):
    assert conn.execute("PRAGMA secure_delete").fetchone()[0] == 1

import ast

_WRITE_RE = re.compile(r"\b(UPDATE|INSERT|REPLACE)\b.*\b(review_status|edited_json)\b", re.I | re.S)

def _writer_sites(source: str):
    """(function, sql) for every string literal / f-string in `source` that is an UPDATE/INSERT touching review_status or edited_json."""
    out = []
    tree = ast.parse(source)
    docstrings = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.Module, ast.ClassDef))
                  and n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    def walk(node, fn):
        if id(node) in docstrings:
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fn = node.name
        if isinstance(node, ast.JoinedStr):
            sql = "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in node.values)
            if _WRITE_RE.search(sql): out.append((fn, sql))
            return
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and _WRITE_RE.search(node.value):
            out.append((fn, node.value))
        for ch in ast.iter_child_nodes(node):
            walk(ch, fn)
    walk(tree, None)
    return out

def test_review_status_only_via_apply_review():
    """AC5: every SQL statement under app/ that writes review_status or edited_json (any position in SET, named or
    positional params, f-strings) sits inside apply_review. AST scan, not a line grep."""
    sites = []
    for f in pathlib.Path("app").rglob("*.py"):
        sites += [(str(f), fn) for fn, _ in _writer_sites(f.read_text())]
    assert sites and all(f == "app/db/db.py" and fn == "apply_review" for f, fn in sites), sites

@pytest.mark.parametrize("rogue", [
    'conn.execute("UPDATE entries SET review_status=? WHERE id=?", (a, b))',
    'conn.execute("UPDATE entries SET edited_json=?, review_status=:s WHERE id=:i", (a, b))',
    'conn.execute(f"UPDATE {t} SET state=?, edited_json=? WHERE id=?", (a, b, c))',
    'conn.execute("INSERT INTO entries (id, review_status) VALUES (?, ?)", (a, b))',
])
def test_writer_guard_catches_rogue_forms(rogue):
    """The guard itself must not weaken: each rogue writer outside apply_review is detected."""
    src = "def apply_review(): pass\ndef sneaky(conn):\n    " + rogue + "\n"
    assert [fn for fn, _ in _writer_sites(src)] == ["sneaky"]

def test_add_item_rejects_edits_and_status(conn):
    cid = seed(conn)
    before = DB.table_counts(conn, cid)["entries"]
    for bad in ({"edited_json": {"summary": "X"}}, {"review_status": "accepted"}):
        with pytest.raises(ValueError):
            DB.add_item(conn, cid, "entry", bad)
    assert DB.table_counts(conn, cid)["entries"] == before
    assert DB.get_item(conn, _entry(conn, cid))["edited"] is None


def test_log_only_actions_not_duplicate_and_manual_entry(conn):
    """T-062: logged with before/after, status unchanged."""
    cid = seed(conn); iid = _entry(conn, cid)
    DB.apply_review(conn, iid, "not_duplicate", now=7)
    DB.apply_review(conn, iid, "manual_entry", now=8)
    ev = DB.list_events(conn, cid, iid)
    assert [e["action"] for e in ev] == ["not_duplicate", "manual_entry"]
    assert all(e["before"] == e["after"] == {"review_status": "pending", "edited": None} for e in ev)
    assert DB.get_item(conn, iid)["review_status"] == "pending"

def test_old_v2_file_is_rebuilt_and_accepts_new_actions(tmp_path):
    """T-062: a file written by schema v2 (review_events CHECK without not_duplicate/manual_entry) is deleted and rebuilt on connect."""
    import sqlite3
    path = str(tmp_path / "v2.sqlite")
    ddl = open("app/db/schema.sql", encoding="utf-8").read().replace(",'not_duplicate','manual_entry'", "")
    assert "manual_entry" not in ddl
    old = sqlite3.connect(path); old.executescript(ddl)
    old.execute("INSERT INTO cases (id, raw_text, created_at) VALUES ('c1', 'SYNTHETIC old', 1)")
    old.execute("PRAGMA user_version=2"); old.commit()
    with pytest.raises(sqlite3.IntegrityError):                       # proves the fixture really is the old schema
        old.execute("INSERT INTO review_events (id, case_id, item_id, action) VALUES ('v','c1','e1','manual_entry')")
    old.close()
    c = DB.connect(path)
    assert DB.get_case(c, "c1") is None                              # old file deleted, not migrated or kept
    cid = DB.create_case(c, "t", now=1); iid = _entry(c, cid)
    for a in ("not_duplicate", "manual_entry"):
        DB.apply_review(c, iid, a, now=2)
    assert c.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION == 4


def _v3_file(tmp_path, rows):
    """A real schema-v3 file: today's DDL with the two new actions taken out of the review_events CHECK, user_version 3."""
    import sqlite3
    path = str(tmp_path / "v3.sqlite")
    ddl = open("app/db/schema.sql", encoding="utf-8").read().replace(",'reclassify','rejudge'", "")
    assert "reclassify" not in ddl
    old = sqlite3.connect(path); old.executescript(ddl)
    old.execute("INSERT INTO cases (id, raw_text, created_at) VALUES ('c1', 'SYNTHETIC old', 1)")
    for i, (action, after) in enumerate(rows):
        old.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                    (f"v{i}", "c1", "a1" if i % 2 else "e1", action, '{"k": %d}' % i, after, float(i)))
    old.execute("PRAGMA user_version=3"); old.commit()
    with pytest.raises(sqlite3.IntegrityError):                       # proves the fixture really is the old schema
        old.execute("INSERT INTO review_events (id, case_id, item_id, action) VALUES ('x','c1','e1','rejudge')")
    old.close()
    return path


def test_v3_to_v4_migrates_in_place_keeping_rows_and_converts_reclassify_edits(tmp_path):
    """T-095: the case and every event survive; only `edit` rows whose payload says event == reclassify change action."""
    rows = [("accept", '{"review_status": "accepted"}'),
            ("edit", '{"edited": {"summary": "x"}}'),                          # a real edit: stays
            ("edit", '{"event": "reclassify", "kind": "unclear"}'),            # the T-084 stand-in: becomes reclassify
            ("edit", None),                                                    # no payload: stays
            ("edit", "not json"),                                              # unreadable payload: stays
            ("dismiss", '{"event": "reclassify"}'),                            # only `edit` rows are converted
            ("edit", '{"event": "reclassify", "kind": "charge"}')]
    path = _v3_file(tmp_path, rows)
    c = DB.connect(path)
    assert c.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION == 4
    assert DB.get_case(c, "c1")["raw_text"] == "SYNTHETIC old"             # migrated, not deleted
    import json
    ev = c.execute("SELECT * FROM review_events ORDER BY rowid").fetchall()        # raw: row v4 holds a payload that is not JSON
    assert [e["id"] for e in ev] == [f"v{i}" for i in range(7)] and [e["at"] for e in ev] == [float(i) for i in range(7)]
    assert [e["action"] for e in ev] == ["accept", "edit", "reclassify", "edit", "edit", "dismiss", "reclassify"]
    assert [json.loads(e["before_json"]) for e in ev] == [{"k": i} for i in range(7)]       # before/after payloads copied untouched
    assert c.execute("SELECT after_json FROM review_events WHERE id='v4'").fetchone()[0] == "not json"
    assert c.execute("SELECT 1 FROM sqlite_master WHERE name='review_events_v3'").fetchone() is None
    assert c.execute("SELECT 1 FROM sqlite_master WHERE type='index' AND name='ix_events_case' AND tbl_name='review_events'").fetchone()
    DB.log_event(c, "c1", "a1", "reclassify", {"a": 1}, {"b": 2}, now=9)  # the new CHECK accepts the new actions
    DB.log_event(c, "c1", "a1", "rejudge", now=10)
    assert [r[0] for r in c.execute("SELECT action FROM review_events ORDER BY rowid")][-2:] == ["reclassify", "rejudge"]
    c.close()
    c2 = DB.connect(path)                                                  # a second open is a no-op
    assert c2.execute("SELECT count(*) FROM review_events").fetchone()[0] == 9 and c2.execute("PRAGMA user_version").fetchone()[0] == 4


def test_v3_migration_rolls_back_if_it_fails(tmp_path, monkeypatch):
    """The rebuild is one transaction: an error mid-copy leaves the v3 file as it was (table, rows, version)."""
    import sqlite3
    path = _v3_file(tmp_path, [("edit", '{"event": "reclassify"}')])
    real = DB.json.loads
    monkeypatch.setattr(DB.json, "loads", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    with pytest.raises(RuntimeError):
        DB.connect(path)
    monkeypatch.setattr(DB.json, "loads", real)
    raw = sqlite3.connect(path)
    assert raw.execute("PRAGMA user_version").fetchone()[0] == 3
    assert raw.execute("SELECT action FROM review_events").fetchall() == [("edit",)]
    assert raw.execute("SELECT 1 FROM sqlite_master WHERE name='review_events_v3'").fetchone() is None


def test_log_event_only_writes_audit_actions_and_apply_review_refuses_them(conn):
    cid = seed(conn); iid = _entry(conn, cid)
    with pytest.raises(ValueError):
        DB.log_event(conn, cid, iid, "accept")
    for a in ("reclassify", "rejudge"):
        with pytest.raises(ValueError):
            DB.apply_review(conn, iid, a)
    DB.log_event(conn, cid, iid, "rejudge", {"x": 1}, {"y": 2}, now=3)
    ev = DB.list_events(conn, cid, iid)
    assert [(e["action"], e["before"], e["after"], e["at"]) for e in ev] == [("rejudge", {"x": 1}, {"y": 2}, 3)]
    assert DB.get_item(conn, iid)["review_status"] == "pending"
