"""SQLite persistence (ADR-002, ADR-006). Owner: db.

- Times are epoch seconds passed in by the caller (`now=`); nothing here reads the clock, so tests inject a fake one.
- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
- delete_case() is the one deletion path; purge_expired() calls it. Never log record text or prompts.
"""
import hashlib
import json
import logging
import os
import re
import secrets
import sqlite3
import time

RETENTION_SECONDS = 24 * 3600
REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
           "confirm_date": None, "keep_my_wording": None,
           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")


def init(path: str = ":memory:"):
    return connect(path)


SCHEMA_VERSION = 4          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062); 4 = += reclassify, rejudge (T-095; v3 -> v4 is an in-place migration)
AUDIT_ONLY_ACTIONS = ("reclassify", "rejudge")          # logged by log_event(); never change review_status, so apply_review() refuses them
log = logging.getLogger("zlayt.db")


def connect(path: str):
    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
    pasted text past the 24 h purge (T-040 security r2)."""
    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
        probe = sqlite3.connect(path)
        try:
            version = probe.execute("PRAGMA user_version").fetchone()[0]
            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
        finally:
            probe.close()
        if has_tables and version != SCHEMA_VERSION and version != 3:
            for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
                if os.path.exists(path + ext):
                    os.remove(path + ext)
            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA secure_delete=ON")
    conn.execute("PRAGMA foreign_keys=ON")
    with open(_SCHEMA, encoding="utf-8") as f:
        schema = f.read()
    if path != ":memory:" and conn.execute("PRAGMA user_version").fetchone()[0] == 3 and \
            conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='review_events'").fetchone():
        _migrate_v3_to_v4(conn, schema)
    conn.executescript(schema)
    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
    return conn


def _migrate_v3_to_v4(conn, schema: str) -> None:
    """v3 -> v4 in place, keeping every row (T-095). SQLite cannot alter a CHECK, so review_events is rebuilt inside one transaction:
    the new table comes from schema.sql itself (no second copy of the DDL), rows are copied as they are except that the old stand-in
    `edit` rows whose payload says event == 'reclassify' get their real action. The user_version bump is part of the same transaction."""
    ddl = re.search(r"CREATE TABLE IF NOT EXISTS review_events \(.*?\n\);", schema, re.S).group(0).replace("IF NOT EXISTS ", "")
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("DROP INDEX IF EXISTS ix_events_case")
        conn.execute("ALTER TABLE review_events RENAME TO review_events_v3")
        conn.execute(ddl)
        rows = conn.execute("SELECT id, case_id, item_id, action, before_json, after_json, at FROM review_events_v3 ORDER BY rowid").fetchall()
        for r in rows:
            action = r["action"]
            if action == "edit":
                try:
                    after = json.loads(r["after_json"]) if r["after_json"] else None
                except ValueError:
                    after = None
                if isinstance(after, dict) and after.get("event") == "reclassify":
                    action = "reclassify"
            conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                         (r["id"], r["case_id"], r["item_id"], action, r["before_json"], r["after_json"], r["at"]))
        conn.execute("DROP TABLE review_events_v3")
        conn.execute("PRAGMA user_version=4")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _tok(prefix: str) -> str:
    return prefix + secrets.token_hex(6)


def _enc(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v


def _cols(conn, table):
    return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
    row = {"id": cid, "name": name, "source": source, "raw_text": raw_text, "text_sha256": sha256(raw_text),
           "created_at": now, **fields}
    _insert(conn, "cases", row)
    return cid


def update_case(conn, case_id: str, **fields) -> None:
    ok = _cols(conn, "cases") - {"id", "created_at", "raw_text"}
    bad = set(fields) - ok
    if bad:
        raise ValueError(f"unknown case fields {sorted(bad)}")
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE cases SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [case_id])


def get_case(conn, case_id: str):
    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    return _decode(r) if r else None


def _insert(conn, table, row):
    bad = set(row) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
                 [_enc(v) for v in row.values()])


def add_record(conn, case_id: str, **fields) -> str:
    rid = fields.pop("id", None) or _tok("r")
    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
    return rid


def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
    if kind not in _ITEM_TABLES:
        raise ValueError(f"unknown item kind {kind!r}")
    table, prefix = _ITEM_TABLES[kind]
    p = dict(payload)
    if {"review_status", "edited_json", "edited"} & set(p):
        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
    iid = p.pop("id", None) or _tok(prefix)
    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
    return iid


def _find(conn, item_id, case=None):
    """Item ids are unique per case (T-050). Pass `case` (the case id) whenever more than one case can share the file."""
    kind = _PREFIX_KIND.get(item_id[:1])
    if kind is None:
        raise KeyError(item_id)
    table = _ITEM_TABLE_OF[kind]
    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
    if case is not None:
        q, a = q + " AND case_id=?", a + [case]
    rows = conn.execute(q, a).fetchall()
    if not rows:
        raise KeyError(item_id)
    if len(rows) > 1:
        raise ValueError(f"item id {item_id!r} exists in several cases; pass case=")
    return table, rows[0]


def _decode(row) -> dict:
    out = {}
    for k in row.keys():
        v = row[k]
        if k.endswith("_json"):
            out[k[:-5]] = json.loads(v) if v else None
        else:
            out[k] = v
    return out


def get_item(conn, item_id: str, case: str = None) -> dict:
    return _decode(_find(conn, item_id, case)[1])


def list_items(conn, case_id: str, kind: str) -> list:
    table = _ITEM_TABLES[kind][0]
    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]


def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
    if locked & set(fields):
        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
    table, found = _find(conn, item_id, case)
    bad = set(fields) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    fields["updated_at"] = now
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])


def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
    if action not in ACTIONS:
        raise ValueError(f"invalid review action {action!r}")
    table, row = _find(conn, item_id, case)
    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
    status = ACTIONS[action] or row["review_status"]
    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
    if action == "edit" and not new_edited:
        raise ValueError("edit requires a non-empty edited payload")
    after = {"review_status": status, "edited": new_edited}
    conn.execute("BEGIN")
    try:
        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return get_item(conn, item_id, row["case_id"])


def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
    if action not in AUDIT_ONLY_ACTIONS:
        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
    eid = _tok("v")
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
    return eid


def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
    if status not in REVIEW_STATUSES:
        raise ValueError(f"invalid review_status {status!r}")
    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
    apply_review(conn, item_id, action, edited=edited, now=now, case=case)


def list_events(conn, case_id: str, item_id: str = None) -> list:
    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
    if item_id:
        q, a = q + " AND item_id=?", a + [item_id]
    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]


def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
    cid = fields.pop("id", None) or _tok("c")
    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
    _insert(conn, "llm_calls", row)
    return cid


def get_llm_call(conn, call_id: str):
    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
    return _decode(r) if r else None


def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
    if item_id:
        q, a = q + " AND item_id=?", a + [item_id]
    return [_decode(r) for r in conn.execute(q + " ORDER BY created_at, rowid", a)]


def delete_case(conn, case_id: str) -> None:
    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
    conn.execute("BEGIN")
    try:
        for t in _CASE_TABLES:
            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
    for cid in ids:
        delete_case(conn, cid)
    return len(ids)


def table_counts(conn, case_id: str) -> dict:
    return {t: conn.execute(f"SELECT COUNT(*) FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,)).fetchone()[0]
            for t in _CASE_TABLES}
