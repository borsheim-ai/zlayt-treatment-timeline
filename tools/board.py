#!/usr/bin/env python3
"""Board CLI — the single system of record for the Zlayt PM project.

Stdlib only. Cards are markdown files with a frontmatter block whose values are
JSON (JSON is valid YAML flow syntax, so the files stay human-readable and
YAML-compatible). Every write is atomic (temp file + os.replace); claims use
O_CREAT|O_EXCL lock files so concurrent agents cannot double-claim.

See docs/CONTRACT.md §4.4 and Appendix D.1 for the schema.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(os.environ.get("BOARD_ROOT") or Path(__file__).resolve().parent.parent)
BOARD = ROOT / "board"
CARDS = BOARD / "cards"
LOCKS = BOARD / ".locks"
INBOX = BOARD / "inbox"
ACTIVITY = BOARD / "activity.jsonl"
MILESTONES = BOARD / "milestones.md"
SHADOW = BOARD / ".state.json"
MEMORY = ROOT / "memory"
LESSONS = MEMORY / "LESSONS.md"
REVIEWS = ROOT / "reviews"

STATUSES = ["backlog", "ready", "in_progress", "in_review", "changes_requested",
            "done", "blocked", "needs_chris", "cancelled"]
MILESTONE_IDS = ["M0", "M1", "M2", "M3", "M4", "M5"]
MILESTONE_STATUSES = ["planned", "active", "gate_running", "gate_failed", "done"]
ROLES = ["orchestrator", "architect", "backend", "db", "frontend", "qa", "release",
         "writer", "researcher"]
PRIORITIES = ["P0", "P1", "P2"]
VERDICTS = ["pass", "changes", "fail"]
STALL_MINUTES = 45

# Legal transitions. `in_progress` is normally entered through `claim`.
TRANSITIONS = {
    "backlog": {"ready", "cancelled", "needs_chris", "blocked"},
    "ready": {"in_progress", "backlog", "blocked", "cancelled", "needs_chris"},
    "in_progress": {"in_review", "blocked", "ready", "needs_chris", "cancelled"},
    "in_review": {"done", "changes_requested", "in_progress", "blocked"},
    "changes_requested": {"in_progress", "needs_chris", "cancelled", "blocked"},
    "blocked": {"ready", "in_progress", "cancelled", "needs_chris"},
    "needs_chris": {"ready", "in_progress", "cancelled", "done"},
    "done": {"in_progress"},  # reopen on regression (note required)
    "cancelled": {"backlog"},
}

FIELD_ORDER = ["id", "title", "milestone", "role", "status", "priority", "depends_on",
               "created_by", "created_at", "updated_at", "claimed_by", "claimed_at",
               "rounds", "commits", "reviews", "ac"]
LIST_FIELDS = {"depends_on", "commits", "reviews", "ac"}
BLOCK_LIST_FIELDS = {"reviews", "ac"}  # one JSON object per line


class BoardError(Exception):
    pass


# ----------------------------------------------------------------- utilities
def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    s = s.strip().rstrip("Z")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue
    return None


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, (line.rstrip("\n") + "\n").encode("utf-8"))
    finally:
        os.close(fd)


class FileLock:
    """Exclusive lock via O_CREAT|O_EXCL with stale-lock recovery."""

    def __init__(self, name: str, timeout: float = 15.0, stale: float = 120.0):
        self.path = LOCKS / f"{name}.lock"
        self.timeout, self.stale = timeout, stale

    def __enter__(self):
        LOCKS.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + self.timeout
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale:
                        self.path.unlink(missing_ok=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.time() > deadline:
                    raise BoardError(f"could not acquire lock {self.path.name}")
                time.sleep(0.05)

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)


def log_event(event: str, agent: str, card: str | None = None, text: str = "", **extra) -> None:
    rec = {"ts": now(), "event": event, "agent": agent, "card": card, "text": text}
    rec.update(extra)
    append_line(ACTIVITY, json.dumps(rec, ensure_ascii=False))


# --------------------------------------------------------------- card format
def _dump_value(v) -> str:
    return json.dumps(v, ensure_ascii=False)


def serialize(meta: dict, body: str) -> str:
    lines = ["---"]
    keys = FIELD_ORDER + [k for k in meta if k not in FIELD_ORDER]
    for k in keys:
        if k not in meta:
            continue
        v = meta[k]
        if k in BLOCK_LIST_FIELDS:
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {_dump_value(item)}")
        else:
            lines.append(f"{k}: {_dump_value(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n" + body.lstrip("\n")


def parse(text: str, where: str = "card") -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise BoardError(f"{where}: missing frontmatter start '---'")
    end = text.find("\n---\n", 4)
    if end < 0:
        if text.rstrip().endswith("\n---"):
            end = text.rstrip().rfind("\n---")
        else:
            raise BoardError(f"{where}: missing frontmatter end '---'")
    head = text[4:end]
    body = text[end + 5:]
    meta: dict = {}
    current_list: str | None = None
    for ln, raw in enumerate(head.split("\n"), start=2):
        if not raw.strip():
            continue
        if raw.startswith("  - ") or raw.startswith("- "):
            if current_list is None:
                raise BoardError(f"{where}:{ln}: list item outside a list field")
            item = raw.split("- ", 1)[1].strip()
            meta[current_list].append(_load_value(item, f"{where}:{ln}"))
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", raw)
        if not m:
            raise BoardError(f"{where}:{ln}: cannot parse line: {raw!r}")
        key, val = m.group(1), m.group(2).strip()
        val = re.sub(r"\s+#.*$", "", val) if not val.startswith(("\"", "{", "[")) else val
        if val == "":
            meta[key] = []
            current_list = key
        else:
            meta[key] = _load_value(val, f"{where}:{ln}")
            current_list = None
    return meta, body


def _load_value(val: str, where: str):
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        pass
    if val in ("null", "~"):
        return None
    if val in ("true", "false"):
        return val == "true"
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if val.startswith("[") and val.endswith("]"):  # bare YAML flow list: [T-1, T-2]
        inner = val[1:-1].strip()
        return [x.strip().strip("'\"") for x in inner.split(",")] if inner else []
    if val.startswith("{"):
        raise BoardError(f"{where}: object values must be JSON: {val[:80]}")
    return val.strip("'\"")


def card_path(cid: str) -> Path:
    return CARDS / f"{cid}.md"


def load(cid: str, check_shadow: bool = True) -> tuple[dict, str]:
    p = card_path(cid)
    if not p.exists():
        raise BoardError(f"no such card {cid}")
    meta, body = parse(p.read_text(encoding="utf-8"), str(p.relative_to(ROOT)))
    if check_shadow:
        prev = _read_shadow().get(cid)
        if prev and prev != meta.get("status"):
            raise BoardError(f"{cid}: status changed {prev} -> {meta.get('status')} outside board.py; "
                             f"restore it to '{prev}' and use `board.py move`")
    return meta, body


def save(meta: dict, body: str) -> None:
    meta["updated_at"] = now()
    errs = check_meta(meta)
    if errs:
        raise BoardError("refusing to write invalid card: " + "; ".join(errs))
    atomic_write(card_path(meta["id"]), serialize(meta, body))
    with FileLock("shadow"):
        shadow = _read_shadow()
        shadow[meta["id"]] = meta["status"]
        atomic_write(SHADOW, json.dumps(shadow, indent=0, sort_keys=True))


def _read_shadow() -> dict:
    try:
        return json.loads(SHADOW.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def all_cards() -> list[tuple[dict, str]]:
    out = []
    for p in sorted(CARDS.glob("T-*.md"), key=lambda p: int(p.stem.split("-")[1])):
        try:
            out.append(parse(p.read_text(encoding="utf-8"), p.name))
        except BoardError as e:
            out.append(({"id": p.stem, "title": f"INVALID: {e}", "status": "blocked",
                         "milestone": "?", "role": "?", "priority": "P0", "ac": [],
                         "reviews": [], "depends_on": []}, ""))
    return out


def check_meta(meta: dict) -> list[str]:
    errs = []
    required = ["id", "title", "milestone", "role", "status", "priority", "ac"]
    for k in required:
        if k not in meta or meta[k] in (None, ""):
            errs.append(f"missing field {k}")
    if errs:
        return errs
    if not re.fullmatch(r"T-\d{3,}", str(meta["id"])):
        errs.append(f"bad id {meta['id']}")
    if meta["status"] not in STATUSES:
        errs.append(f"bad status {meta['status']}")
    if meta["milestone"] not in MILESTONE_IDS:
        errs.append(f"bad milestone {meta['milestone']}")
    if meta["role"] not in ROLES:
        errs.append(f"bad role {meta['role']}")
    if meta["priority"] not in PRIORITIES:
        errs.append(f"bad priority {meta['priority']}")
    for f in LIST_FIELDS:
        if f in meta and not isinstance(meta[f], list):
            errs.append(f"{f} must be a list")
    if not isinstance(meta.get("ac"), list) or not meta["ac"]:
        errs.append("ac must be a non-empty list")
    else:
        for i, a in enumerate(meta["ac"], 1):
            if not isinstance(a, dict) or not {"n", "text", "done"} <= set(a):
                errs.append(f"ac item {i} must have n, text, done")
            elif a.get("done") and not a.get("evidence"):
                errs.append(f"ac {a['n']} is done without evidence")
    for r in meta.get("reviews") or []:
        if not isinstance(r, dict) or r.get("verdict") not in VERDICTS or not r.get("persona"):
            errs.append(f"bad review entry {str(r)[:80]}")
    if meta["status"] == "done":
        if not all(a.get("done") for a in meta["ac"] if isinstance(a, dict)):
            errs.append("status done but not all AC checked")
        if not _reviews_pass(meta) and meta.get("created_by") == "orchestrator" and "NEEDS_CHRIS" in str(meta.get("title")):
            pass  # answered by Chris (human approval), see card notes
        elif not _reviews_pass(meta):
            errs.append("status done without a passing review set")
    return errs


def _reviews_pass(meta: dict) -> bool:
    revs = [r for r in meta.get("reviews") or [] if isinstance(r, dict)]
    debt_idx = max((i for i, r in enumerate(revs) if r.get("persona") == "orchestrator-§7.4" and r.get("debt")), default=None)
    if debt_idx is not None and all(r.get("verdict") == "pass" for r in revs[debt_idx + 1:]):
        return True  # accepted with documented debt (§7.4) and no later non-pass review
    latest: dict[str, str] = {}
    for r in meta.get("reviews") or []:
        if isinstance(r, dict) and r.get("persona"):
            latest[r["persona"]] = r.get("verdict")
    return bool(latest) and "pass" in latest.values() and all(v == "pass" for v in latest.values())


def append_note(body: str, agent: str, text: str) -> str:
    line = f"- {now()} {agent}: {text.strip()}"
    if "## Notes" not in body:
        body = body.rstrip() + "\n\n## Notes (append-only, newest last)\n"
    parts = body.split("## Handoff", 1)
    notes = parts[0].rstrip() + "\n" + line + "\n"
    return notes + ("\n## Handoff" + parts[1] if len(parts) == 2 else "")


def last_activity(meta: dict, body: str) -> dt.datetime | None:
    stamps = re.findall(r"^- (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z?)", body, re.M)
    cands = [parse_ts(s) for s in stamps] + [parse_ts(meta.get("claimed_at")), parse_ts(meta.get("updated_at"))]
    cands = [c for c in cands if c]
    return max(cands) if cands else None


HANDLED_MINUTES = {"assigned": 180, "review dispatched": 90}


def handled(body: str, marker: str) -> bool:
    """True if the card carries a recent `assigned:` / `review dispatched:` note (work is queued, not idle)."""
    limit = HANDLED_MINUTES[marker]
    tnow = dt.datetime.now(dt.timezone.utc)
    # a marker only counts if it is newer than the card's latest (re)submission / return
    resets = [parse_ts(m.group(1)) for m in re.finditer(r"^- (\S+) \S+: (moved \S+ -> (in_review|changes_requested|ready)|review \S+ \(.*?\): (changes|fail))", body, re.M)]
    floor = max([r for r in resets if r], default=None)
    for m in re.finditer(r"^- (\S+) orchestrator: " + re.escape(marker) + r":", body, re.M):  # only the orchestrator's markers count
        t = parse_ts(m.group(1))
        if t and (tnow - t).total_seconds() < limit * 60 and (floor is None or t >= floor):
            return True
    return False


# ---------------------------------------------------------------- milestones
DEFAULT_MILESTONES = [
    {"id": "M0", "title": "Operating system (harness, board, hooks, agents)", "status": "active", "budget_h": 1.5},
    {"id": "M1", "title": "Research, personas, requirements, architecture", "status": "planned", "budget_h": 2.5},
    {"id": "M2", "title": "Core pipeline + evals green", "status": "planned", "budget_h": 3.5},
    {"id": "M3", "title": "Review UI, export, E2E", "status": "planned", "budget_h": 3.5},
    {"id": "M4", "title": "Hardening, deployment, demo assets", "status": "planned", "budget_h": 2.0},
    {"id": "M5", "title": "Submission package", "status": "planned", "budget_h": 2.0},
]


def load_milestones() -> list[dict]:
    if not MILESTONES.exists():
        return [dict(m) for m in DEFAULT_MILESTONES]
    meta, _ = parse(MILESTONES.read_text(encoding="utf-8"), "milestones.md")
    return meta.get("milestones") or [dict(m) for m in DEFAULT_MILESTONES]


def save_milestones(ms: list[dict]) -> None:
    lines = ["---", "milestones:"] + [f"  - {json.dumps(m, ensure_ascii=False)}" for m in ms] + ["---"]
    body = ["# Milestones", "", "Generated by `tools/board.py` — edit through `board.py milestone` / `board.py gate`.", "",
            "| Milestone | Title | Status | Gate | Started | Finished | Budget (h) | Note |",
            "|---|---|---|---|---|---|---|---|"]
    for m in ms:
        body.append(f"| {m['id']} | {m['title']} | {m['status']} | {m.get('gate_result') or '-'}"
                    f"{(' ([record](../' + m['gate_record'] + '))') if m.get('gate_record') else ''} | "
                    f"{m.get('started_at') or '-'} | {m.get('done_at') or '-'} | {m.get('budget_h', '-')} | {m.get('note') or ''} |")
    body += ["", "Definitions: see docs/CONTRACT.md §4 (M0) and §5 (M1–M5)."]
    atomic_write(MILESTONES, "\n".join(lines) + "\n" + "\n".join(body) + "\n")


# ------------------------------------------------------------------- status
def git_tags() -> set[str]:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "tag"], capture_output=True, text=True, timeout=10).stdout
        return set(out.split())
    except Exception:
        return set()


def inbox_unread() -> list[Path]:
    if not INBOX.exists():
        return []
    return sorted(p for p in INBOX.glob("*.md") if p.is_file())


SUBMISSION_REQUIRED = ["submission/product-note.md", "submission/part2-process.md",
                       "submission/SUBMISSION_CHECKLIST.md", "submission/email-draft.md",
                       "submission/NEEDS_CHRIS.md", "submission/prompt-log/TOOLS.md",
                       "artifacts/CAPTIONS.md"]


def done_checks(cards, ms) -> dict:
    tags = git_tags()
    checks = {}
    checks["milestones_done"] = all(m["status"] == "done" and m.get("gate_result") == "pass" for m in ms)
    checks["tags"] = all(f"m{i}" in tags for i in range(6))
    try:
        ev = json.loads((ROOT / "evals/reports/latest.json").read_text())
        checks["evals_ship_bar"] = bool(ev.get("ship_bar_met"))
    except Exception:
        checks["evals_ship_bar"] = False
    try:
        it = json.loads((ROOT / "artifacts/install_test_last.json").read_text())
        checks["install_under_5min"] = bool(it.get("ok")) and float(it.get("seconds", 1e9)) < 300
    except Exception:
        checks["install_under_5min"] = False
    checks["submission_files"] = all((ROOT / f).exists() for f in SUBMISSION_REQUIRED)
    checks["demo_video_or_reason"] = (ROOT / "artifacts/demo.webm").exists() or (ROOT / "artifacts/DEMO_VIDEO_NOT_RECORDED.md").exists()
    try:
        checks["state_complete"] = "COMPLETE" in (MEMORY / "STATE.md").read_text()
    except FileNotFoundError:
        checks["state_complete"] = False
    checks["no_alert"] = not (BOARD / "ALERT.md").exists()
    open_cards = [m["id"] for m, _ in cards if m["status"] not in ("done", "cancelled", "needs_chris")]
    checks["all_cards_closed"] = not open_cards
    return checks


def compute_status() -> dict:
    cards = all_cards()
    ms = load_milestones()
    by_status = {s: 0 for s in STATUSES}
    by_ms: dict[str, dict] = {m["id"]: {"total": 0, "done": 0} for m in ms}
    stalled, ready_unclaimed, invalid, review_pending = [], [], [], []
    tnow = dt.datetime.now(dt.timezone.utc)
    done_ids = {m["id"] for m, _ in cards if m["status"] == "done"}
    active_now = {m["id"] for m in ms if m["status"] in ("active", "gate_running", "gate_failed")}
    for meta, body in cards:
        st = meta.get("status", "blocked")
        by_status[st] = by_status.get(st, 0) + 1
        if str(meta.get("title", "")).startswith("INVALID"):
            invalid.append(meta["id"])
        mm = by_ms.setdefault(meta.get("milestone", "?"), {"total": 0, "done": 0})
        if st not in ("cancelled", "needs_chris"):
            mm["total"] += 1
            mm["done"] += st == "done"
        if st == "in_progress":
            la = last_activity(meta, body)
            if la and (tnow - la).total_seconds() > STALL_MINUTES * 60:
                stalled.append({"id": meta["id"], "owner": meta.get("claimed_by"), "minutes": int((tnow - la).total_seconds() // 60)})
        if st == "ready" and meta.get("milestone") in active_now and all(d in done_ids for d in meta.get("depends_on") or []) and not handled(body, "assigned"):
            ready_unclaimed.append({"id": meta["id"], "role": meta["role"], "priority": meta["priority"], "title": meta["title"]})
        if st == "in_review" and not handled(body, "review dispatched"):
            review_pending.append(meta)
    active = [m for m in ms if m["status"] in ("active", "gate_running", "gate_failed")]
    active_ids = [m["id"] for m in active]
    active_no_cards = any(by_ms.get(a, {}).get("total", 0) == 0 for a in active_ids)
    gate_failed = any(m["status"] == "gate_failed" for m in ms)
    unread = inbox_unread()
    checks = done_checks(cards, ms)
    actionable = []
    for p in unread[:3]:
        actionable.append(f"Inbox note from Chris: {p.name} — run `board.py inbox` and act on it")
    for m in ms:
        if m["status"] == "gate_failed":
            actionable.append(f"Gate {m['id']} failed — triage findings into cards and re-run the gate")
    for c in review_pending[:5]:
        actionable.append(f"{c['id']} in_review, no review dispatched — dispatch Tier-1 reviewers: {c['title']}")
    changes_pending = [m for m, b in cards if m["status"] == "changes_requested" and not handled(b, "assigned")]
    for c in changes_pending[:5]:
        if int(c.get("rounds") or 0) >= 3:
            actionable.append(f"{c['id']} hit the 3-round cap — decide per §7.4 (accept w/ debt, re-scope, split, reassign, needs_chris)")
        else:
            actionable.append(f"{c['id']} changes_requested — send back to {c['role']}: {c['title']}")
    for r in sorted(ready_unclaimed, key=lambda r: r["priority"])[:5]:
        actionable.append(f"{r['id']} ready for {r['role']} ({r['priority']}): {r['title']}")
    if active_no_cards:
        actionable.append(f"Active milestone {active_ids} has no cards — plan them")
    for s in stalled[:3]:
        actionable.append(f"{s['id']} stalled {s['minutes']} min (owner {s['owner']}) — message or reassign")
    total = sum(v["total"] for v in by_ms.values())
    done_n = sum(v["done"] for v in by_ms.values())
    return {
        "generated_at": now(),
        "by_status": by_status,
        "by_milestone": by_ms,
        "milestones": ms,
        "active_milestones": active_ids,
        "stalled": stalled,
        "ready_unclaimed": len(ready_unclaimed),
        "ready_cards": ready_unclaimed,
        "in_review": len(review_pending),
        "in_review_total": by_status.get("in_review", 0),
        "changes_requested": len(changes_pending),
        "changes_requested_total": by_status.get("changes_requested", 0),
        "in_progress": by_status.get("in_progress", 0),
        "needs_chris": by_status.get("needs_chris", 0),
        "gate_failed": gate_failed,
        "inbox_unread": len(unread),
        "active_milestone_has_no_cards": active_no_cards,
        "invalid_cards": invalid,
        "progress_pct": round(100 * done_n / total, 1) if total else 0.0,
        "done_checks": checks,
        "done_definition_met": all(checks.values()),
        "actionable": actionable,
        "board_hash": board_hash(),
    }


def board_hash() -> str:
    h = hashlib.sha256()
    for p in sorted(CARDS.glob("T-*.md")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    if MILESTONES.exists():
        h.update(MILESTONES.read_bytes())
    for p in sorted(REVIEWS.glob("*.md")) if REVIEWS.exists() else []:
        h.update(p.name.encode())
        h.update(str(p.stat().st_size).encode())
    return h.hexdigest()[:16]


# ----------------------------------------------------------------- commands
def cmd_init(a):
    for d in (CARDS, LOCKS, INBOX, INBOX / "archive", REVIEWS, MEMORY):
        d.mkdir(parents=True, exist_ok=True)
    if not MILESTONES.exists():
        save_milestones([dict(m, started_at=now() if m["status"] == "active" else None) for m in DEFAULT_MILESTONES])
    ACTIVITY.touch()
    if not LESSONS.exists():
        atomic_write(LESSONS, "# LESSONS (append-only via `board.py lesson`)\n\nWhat worked, what didn't, and what harness change it caused.\n\n")
    log_event("init", a.agent or "orchestrator", None, "board initialized")
    print("board initialized")


def next_id() -> str:
    nums = [int(p.stem.split("-")[1]) for p in CARDS.glob("T-*.md")]
    return f"T-{(max(nums) + 1 if nums else 1):03d}"


def cmd_new(a):
    body = ""
    if a.body_file:
        body = Path(a.body_file).read_text(encoding="utf-8")
    elif a.body:
        body = a.body
    if "## Description" not in body:
        body = "## Description\n" + (body.strip() or "(see title and acceptance criteria)") + "\n"
    if "## Notes" not in body:
        body = body.rstrip() + "\n\n## Notes (append-only, newest last)\n"
    if "## Handoff" not in body:
        body = body.rstrip() + "\n\n## Handoff (filled when moving to in_review)\n"
    for d in a.depends or []:
        if not card_path(d).exists():
            raise BoardError(f"dependency {d} does not exist")
    if not a.ac:
        raise BoardError("at least one --ac is required (testable acceptance criterion)")
    with FileLock("new"):
        cid = next_id()
        meta = {
            "id": cid, "title": a.title, "milestone": a.milestone, "role": a.role,
            "status": a.status, "priority": a.priority, "depends_on": a.depends or [],
            "created_by": a.by, "created_at": now(), "updated_at": now(),
            "claimed_by": None, "claimed_at": None, "rounds": 0, "commits": [], "reviews": [],
            "ac": [{"n": i, "text": t, "done": False, "evidence": None} for i, t in enumerate(a.ac, 1)],
        }
        save(meta, body)
    log_event("new", a.by, cid, a.title, milestone=a.milestone, role=a.role)
    print(cid)


def cmd_claim(a):
    LOCKS.mkdir(parents=True, exist_ok=True)
    lock = LOCKS / f"claim-{a.id}.lock"
    if load(a.id)[0]["status"] in ("changes_requested", "blocked"):
        lock.unlink(missing_ok=True)  # previous round's claim; card is not being worked
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, a.agent.encode())
        os.close(fd)
    except FileExistsError:
        holder = lock.read_text() if lock.exists() else "?"
        raise BoardError(f"{a.id} already claimed (lock held by {holder})")
    try:
        with FileLock(a.id):
            meta, body = load(a.id)
            if meta["status"] not in ("ready", "changes_requested", "blocked"):
                raise BoardError(f"{a.id} is {meta['status']}; only ready/changes_requested/blocked cards can be claimed")
            if meta.get("claimed_by") and meta["status"] == "ready":
                raise BoardError(f"{a.id} already claimed by {meta['claimed_by']}")
            undone = [d for d in meta.get("depends_on") or [] if load(d)[0]["status"] != "done"]
            if undone and not a.force:
                raise BoardError(f"{a.id} depends on unfinished {undone} (use --force to override, with a note)")
            meta.update(status="in_progress", claimed_by=a.agent, claimed_at=now())
            body = append_note(body, a.agent, "claimed")
            save(meta, body)
    except BaseException:
        lock.unlink(missing_ok=True)
        raise
    log_event("claim", a.agent, a.id, meta["title"])
    print(f"{a.id} claimed by {a.agent}")


def _release_claim_lock(cid: str):
    (LOCKS / f"claim-{cid}.lock").unlink(missing_ok=True)


def cmd_move(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        cur, new = meta["status"], a.status
        if new not in STATUSES:
            raise BoardError(f"unknown status {new}")
        if new == cur:
            raise BoardError(f"{a.id} already {cur}")
        debt_close = cur in ("changes_requested", "in_review") and new == "done" and getattr(a, "accept_debt", None)
        if new not in TRANSITIONS.get(cur, set()) and not debt_close:
            raise BoardError(f"illegal transition {cur} -> {new}; allowed: {sorted(TRANSITIONS.get(cur, set()))}")
        if new == "in_progress" and cur in ("ready", "changes_requested", "blocked") and not meta.get("claimed_by"):
            raise BoardError("use `board.py claim` to start work")
        if new == "done":
            undone = [x["n"] for x in meta["ac"] if not x.get("done")]
            if undone:
                raise BoardError(f"cannot move to done: AC {undone} not checked")
            if getattr(a, "accept_debt", None):
                latest = {}
                for r in meta.get("reviews") or []:
                    if isinstance(r, dict):
                        latest[r.get("persona")] = r.get("verdict")
                if a.agent != "orchestrator" or int(meta.get("rounds") or 0) < 2 or "fail" in latest.values():
                    raise BoardError("--accept-debt (§7.4, D-024) needs: orchestrator, rounds >= 2, no persona's latest verdict = fail")
                append_line(MEMORY / "SCOPE_CUTS.md", f"| debt | {meta['id']} accepted with documented debt after {meta['rounds']} rounds (§7.4) | {a.accept_debt} | see card | {meta['milestone']} |")
                body = append_note(body, a.agent, f"accepted with documented debt (§7.4): {a.accept_debt}")
                meta.setdefault("reviews", []).append({"persona": "orchestrator-§7.4", "model": "claude-opus-5-5", "verdict": "pass",
                                                        "file": "memory/SCOPE_CUTS.md", "at": now(), "debt": a.accept_debt})
            elif cur == "needs_chris":
                if not a.note:
                    raise BoardError("closing a needs_chris card requires --note quoting Chris's answer")
            elif not _reviews_pass(meta):
                raise BoardError("cannot move to done: needs >=1 passing review and every persona's latest verdict = pass")
            if a.agent == meta.get("claimed_by") and a.agent != "orchestrator":
                raise BoardError("no self-approval: the worker that did the card cannot mark it done")
        if new == "in_review":
            undone = [x["n"] for x in meta["ac"] if not x.get("done")]
            if undone and not a.note:
                raise BoardError(f"AC {undone} unchecked; check them with evidence or give --note explaining")
            if "## Handoff" in body and not body.split("## Handoff", 1)[1].split("\n", 1)[-1].strip():
                raise BoardError("fill the Handoff section (what changed · how verified · what's left · surprises) before in_review (use `board.py handoff`)")
        if new in ("cancelled", "needs_chris", "blocked") and not a.note:
            raise BoardError(f"moving to {new} requires --note with the reason")
        if cur == "done" and not a.note:
            raise BoardError("reopening a done card requires --note")
        if new == "ready":
            meta.update(claimed_by=None, claimed_at=None)
            _release_claim_lock(a.id)
        if new in ("done", "cancelled"):
            _release_claim_lock(a.id)
        meta["status"] = new
        body = append_note(body, a.agent, f"moved {cur} -> {new}" + (f": {a.note}" if a.note else ""))
        save(meta, body)
    log_event("move", a.agent, a.id, f"{cur} -> {new}" + (f": {a.note}" if a.note else ""), status=new)
    print(f"{a.id}: {cur} -> {new}")


def cmd_note(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        body = append_note(body, a.agent, a.text)
        save(meta, body)
    log_event("note", a.agent, a.id, a.text)
    print(f"noted on {a.id}")


def cmd_handoff(a):
    text = Path(a.file).read_text(encoding="utf-8") if a.file else a.text
    if not text or not text.strip():
        raise BoardError("handoff text required")
    with FileLock(a.id):
        meta, body = load(a.id)
        head = body.split("## Handoff", 1)[0].rstrip()
        body = head + "\n\n## Handoff\n" + text.strip() + "\n"
        save(meta, body)
    log_event("handoff", a.agent, a.id, text.strip().splitlines()[0][:200])
    print(f"handoff written on {a.id}")


def cmd_ac(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        if a.add:
            n = max([x["n"] for x in meta["ac"]] or [0]) + 1
            meta["ac"].append({"n": n, "text": a.add, "done": False, "evidence": None})
            msg = f"AC {n} added: {a.add}"
        elif a.edit:
            item = next((x for x in meta["ac"] if x["n"] == a.edit), None)
            if not item or not a.text:
                raise BoardError("--edit N requires an existing AC and --text")
            item.update(text=a.text, done=False, evidence=None)
            msg = f"AC {a.edit} edited: {a.text}"
        elif a.check:
            item = next((x for x in meta["ac"] if x["n"] == a.check), None)
            if not item:
                raise BoardError(f"no AC {a.check}")
            if not a.evidence or len(a.evidence.strip()) < 10:
                raise BoardError("--evidence is required to check an AC (>= 10 chars: a test name, command output or file path)")
            item.update(done=True, evidence=a.evidence)
            msg = f"AC {a.check} checked: {a.evidence}"
        elif a.uncheck:
            item = next((x for x in meta["ac"] if x["n"] == a.uncheck), None)
            if not item:
                raise BoardError(f"no AC {a.uncheck}")
            item.update(done=False, evidence=None)
            msg = f"AC {a.uncheck} unchecked" + (f": {a.text}" if a.text else "")
        else:
            raise BoardError("one of --check/--uncheck/--add/--edit required")
        body = append_note(body, a.agent, msg)
        save(meta, body)
    log_event("ac", a.agent, a.id, msg)
    print(msg)


def cmd_review(a):
    if a.verdict not in VERDICTS:
        raise BoardError(f"verdict must be one of {VERDICTS}")
    rp = ROOT / a.file
    if not rp.exists():
        raise BoardError(f"review file {a.file} does not exist")
    errs = validate_review_file(rp)
    if errs:
        raise BoardError("review file invalid: " + "; ".join(errs))
    d = review_json(rp) or {}
    if d.get("verdict") != a.verdict:
        raise BoardError(f"--verdict {a.verdict} does not match the review file's verdict {d.get('verdict')!r}")
    if a.id not in str(d.get("card", "")).replace(" ", "").split("/") and not str(d.get("card", "")).startswith(a.id):
        raise BoardError(f"review file is for card {d.get('card')!r}, not {a.id}")
    fp = str(d.get("persona", ""))
    if fp and fp.replace("-reviewer", "") != a.persona.replace("-reviewer", ""):
        raise BoardError(f"--persona {a.persona} does not match the review file's persona {fp!r}")
    with FileLock(a.id):
        meta, body = load(a.id)
        meta.setdefault("reviews", []).append({"persona": a.persona, "model": a.model, "verdict": a.verdict,
                                                "file": a.file, "at": now()})
        msg = f"review {a.persona} ({a.model}): {a.verdict} — {a.file}"
        if a.verdict in ("changes", "fail") and meta["status"] == "in_review":
            meta["status"] = "changes_requested"
            meta["rounds"] = int(meta.get("rounds") or 0) + 1
            findings = _summarize_findings(rp)
            body = append_note(body, a.agent, msg + f"; round {meta['rounds']}; findings:\n" + findings)
        else:
            body = append_note(body, a.agent, msg)
        save(meta, body)
    log_event("review", a.agent, a.id, msg, persona=a.persona, verdict=a.verdict, file=a.file)
    print(msg + (f" -> {a.id} now {meta['status']} (round {meta['rounds']})" if a.verdict != "pass" else ""))


def review_json(path: Path) -> dict | None:
    txt = path.read_text(encoding="utf-8")
    for block in re.findall(r"```json\s*\n(.*?)\n```", txt, re.S):
        try:
            d = json.loads(block)
            if isinstance(d, dict) and "verdict" in d:
                return d
        except json.JSONDecodeError:
            continue
    return None


def _summarize_findings(path: Path) -> str:
    d = review_json(path)
    if not d:
        return f"    (see {path.relative_to(ROOT)})"
    out = []
    for f in d.get("findings") or []:
        if isinstance(f, dict) and f.get("severity") in ("blocker", "major", "minor"):
            out.append(f"    - [{f.get('severity')}] {f.get('title')} — fix: {f.get('fix', '')}"[:400])
    return "\n".join(out) or f"    (no blocker/major/minor findings; see {path.relative_to(ROOT)})"


def cmd_assign(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        body = append_note(body, "orchestrator", f"assigned: {a.to}")
        save(meta, body)
    log_event("assign", "orchestrator", a.id, f"assigned to {a.to}")
    print(f"{a.id} assigned to {a.to}")


def cmd_dispatch(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        if meta["status"] != "in_review":
            raise BoardError(f"{a.id} is {meta['status']}, not in_review")
        body = append_note(body, "orchestrator", f"review dispatched: {a.personas}")
        save(meta, body)
    log_event("dispatch", "orchestrator", a.id, f"review dispatched: {a.personas}")
    print(f"{a.id}: review dispatched to {a.personas}")


def cmd_commit(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        meta.setdefault("commits", []).append(a.sha)
        save(meta, body)
    log_event("commit", a.agent, a.id, a.sha)
    print(f"{a.id}: commit {a.sha} recorded")


def cmd_update(a):
    with FileLock(a.id):
        meta, body = load(a.id)
        changes = []
        for f in ("title", "priority", "role", "milestone"):
            v = getattr(a, f)
            if v:
                meta[f] = v
                changes.append(f"{f}={v}")
        if a.depends is not None:
            meta["depends_on"] = a.depends
            changes.append(f"depends_on={a.depends}")
        if a.append_body:
            text = Path(a.append_body).read_text(encoding="utf-8")
            head, sep, rest = body.partition("## Notes")
            body = head.rstrip() + "\n\n" + text.strip() + "\n\n" + sep + rest
            changes.append(f"body appended from {a.append_body}")
        if not changes:
            raise BoardError("nothing to update")
        body = append_note(body, a.agent, "updated " + ", ".join(changes))
        save(meta, body)
    log_event("update", a.agent, a.id, ", ".join(changes))
    print(f"{a.id} updated: {', '.join(changes)}")


def cmd_next(a):
    cards = all_cards()
    done_ids = {m["id"] for m, _ in cards if m["status"] == "done"}
    ms_active = {m["id"] for m in load_milestones() if m["status"] in ("active", "gate_running", "gate_failed")}
    cands = []
    for meta, _ in cards:
        if meta["role"] != a.role:
            continue
        if meta["status"] == "changes_requested":
            cands.append((0, meta))
        elif meta["status"] == "ready" and all(d in done_ids for d in meta.get("depends_on") or []):
            cands.append((1 if meta["milestone"] in ms_active else 2, meta))
    if not cands:
        if a.json:
            print("null")
        else:
            print(f"no claimable card for role {a.role}")
        return 3
    cands.sort(key=lambda t: (t[0], t[1]["priority"], t[1]["created_at"]))
    m = cands[0][1]
    if a.json:
        print(json.dumps({"id": m["id"], "title": m["title"], "status": m["status"], "priority": m["priority"]}))
    else:
        print(f"{m['id']}\t{m['priority']}\t{m['status']}\t{m['title']}")
    return 0


def cmd_status(a):
    s = compute_status()
    if a.json:
        print(json.dumps(s, indent=1))
        return
    ms_line = " ".join(f"{m['id']}:{m['status']}" for m in s["milestones"])
    bs = s["by_status"]
    print(f"[board] {s['progress_pct']}% done | {ms_line}")
    print(f"[board] ready={bs['ready']} in_progress={bs['in_progress']} in_review={bs['in_review']} "
          f"changes={bs['changes_requested']} blocked={bs['blocked']} needs_chris={bs['needs_chris']} "
          f"done={bs['done']} | inbox_unread={s['inbox_unread']} stalled={len(s['stalled'])}")
    if a.brief:
        for x in s["actionable"][:5]:
            print(f"[board] → {x}")
        return
    for mid, v in s["by_milestone"].items():
        print(f"  {mid}: {v['done']}/{v['total']}")
    if s["stalled"]:
        print("  stalled:", ", ".join(f"{x['id']}({x['minutes']}m,{x['owner']})" for x in s["stalled"]))
    print("  done checks:", ", ".join(f"{k}={'Y' if v else 'n'}" for k, v in s["done_checks"].items()))
    for x in s["actionable"]:
        print(f"  → {x}")


# Reviews written before this rule existed keep their recorded verdicts (lesson: T-113 r2 'changes' with no major).
_VERDICT_RULE_SINCE = 1793623945


def validate_review_file(p: Path) -> list[str]:
    errs = []
    if p.name.startswith("GATE-") or p.name.startswith("CONTRACT-"):
        if len(p.read_text(encoding="utf-8").strip()) < 50:
            errs.append("gate summary is empty")
        return errs
    d = review_json(p)
    if d is None:
        return ["review must contain a ```json block (Appendix D.2) with a verdict"]
    for k in ("card", "persona", "verdict", "findings", "exercised"):
        if k not in d:
            errs.append(f"review JSON missing '{k}'")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be one of {VERDICTS}")
    if not isinstance(d.get("findings"), list):
        return ["review JSON 'findings' must be a list (use [] for none)"]
    sev = [f.get("severity") for f in d.get("findings", []) if isinstance(f, dict)]
    for f in d.get("findings", []):
        if not isinstance(f, dict) or f.get("severity") not in ("blocker", "major", "minor", "nit"):
            errs.append(f"finding has bad severity: {str(f)[:80]}")
        elif not f.get("evidence"):
            errs.append(f"finding without evidence: {f.get('title')}")
    if "blocker" in sev and d.get("verdict") != "fail":
        errs.append("a blocker finding requires verdict 'fail' (§7.4)")
    elif "major" in sev and "blocker" not in sev and d.get("verdict") != "changes":
        errs.append("a major finding (no blockers) requires verdict 'changes' (§7.4)")
    elif not {"blocker", "major"} & set(sev) and d.get("verdict") != "pass" and p.stat().st_mtime > _VERDICT_RULE_SINCE:
        errs.append("no blocker or major finding requires verdict 'pass' (§7.4)")
    if not d.get("exercised"):
        errs.append("'exercised' is empty — a review that didn't exercise the artifact is invalid")
    return errs


def cmd_validate(a):
    targets = [Path(a.path)] if a.path else sorted(CARDS.glob("T-*.md"))
    errors = []
    shadow = _read_shadow()
    for t in targets:
        p = t if t.is_absolute() else (Path.cwd() / t)
        if not p.exists() and not t.is_absolute() and (ROOT / t).exists():
            p = ROOT / t
        p = Path(os.path.realpath(p))
        if not p.exists():
            errors.append(f"{t}: no such file")
            continue
        try:
            rel = p.relative_to(Path(os.path.realpath(ROOT)))
        except ValueError:
            errors.append(f"{t}: not inside the project")
            continue
        if not rel.parts or rel.parts[0] not in ("board", "reviews"):
            errors.append(f"{t}: not a board or review file")
            continue
        parts = rel.parts
        if parts[0] == "reviews" and p.suffix == ".md":
            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
        elif parts[:2] == ("board", "cards") and p.suffix == ".md":
            try:
                meta, body = parse(p.read_text(encoding="utf-8"), str(rel))
                errors += [f"{rel}: {e}" for e in check_meta(meta)]
                if meta.get("id") != p.stem:
                    errors.append(f"{rel}: id {meta.get('id')} does not match filename")
                prev = shadow.get(p.stem)
                if prev and prev != meta.get("status"):
                    errors.append(f"{rel}: status changed {prev} -> {meta.get('status')} outside board.py; use `board.py move`")
            except BoardError as e:
                errors.append(str(e))
        elif rel == Path("board/milestones.md"):
            try:
                load_milestones()
            except BoardError as e:
                errors.append(str(e))
    if errors:
        for e in errors:
            print(f"INVALID: {e}", file=sys.stderr)
        return 2
    print(f"ok ({len(targets)} file(s))")
    return 0


def cmd_milestone(a):
    ms = load_milestones()
    m = next((x for x in ms if x["id"] == a.id), None)
    if not m:
        raise BoardError(f"no milestone {a.id}")
    if a.status not in MILESTONE_STATUSES:
        raise BoardError(f"status must be one of {MILESTONE_STATUSES}")
    if a.status == "done" and m.get("gate_result") != "pass":
        raise BoardError(f"{a.id} cannot be done without a passing gate (`board.py gate {a.id} --result pass`)")
    prev = m["status"]
    m["status"] = a.status
    if a.status == "active" and not m.get("started_at"):
        m["started_at"] = now()
    if a.status == "done":
        m["done_at"] = now()
    if a.note:
        m["note"] = a.note
    save_milestones(ms)
    log_event("milestone", a.agent, None, f"{a.id}: {prev} -> {a.status}" + (f" ({a.note})" if a.note else ""))
    print(f"{a.id}: {prev} -> {a.status}")


def cmd_gate(a):
    ms = load_milestones()
    m = next((x for x in ms if x["id"] == a.id), None)
    if not m:
        raise BoardError(f"no milestone {a.id}")
    if not (ROOT / a.record).exists():
        raise BoardError(f"gate record {a.record} does not exist")
    if len((ROOT / a.record).read_text(encoding="utf-8").strip()) < 300:
        raise BoardError(f"gate record {a.record} is a stub (<300 chars); write the synthesis first")
    if a.result == "pass":
        open_cards = [c["id"] for c, _ in all_cards() if c["milestone"] == a.id and c["status"] not in ("done", "cancelled", "needs_chris")]
        if open_cards:
            raise BoardError(f"gate {a.id} cannot pass with open cards: {open_cards}")
    m["gate_result"] = a.result
    m["gate_record"] = a.record
    m["gate_at"] = now()
    m["status"] = "gate_failed" if a.result == "fail" else m["status"]
    save_milestones(ms)
    log_event("gate", a.agent, None, f"{a.id} gate {a.result} — {a.record}", milestone=a.id, result=a.result)
    print(f"gate {a.id}: {a.result}")


def cmd_lesson(a):
    if not LESSONS.exists():
        atomic_write(LESSONS, "# LESSONS (append-only via `board.py lesson`)\n\n")
    append_line(LESSONS, f"- {now()} **{a.agent}**: {a.text.strip()}")
    log_event("lesson", a.agent, a.card, a.text)
    print("lesson recorded")


def cmd_inbox(a):
    notes = inbox_unread()
    if not notes:
        print("inbox empty")
        return
    for p in notes:
        print(f"=== {p.name} ===")
        print(p.read_text(encoding="utf-8").strip())
        print()
    if a.ack:
        (INBOX / "archive").mkdir(parents=True, exist_ok=True)
        for p in notes:
            os.replace(p, INBOX / "archive" / p.name)
        log_event("inbox_ack", a.agent or "orchestrator", None, f"acknowledged {len(notes)} note(s)")
        print(f"acknowledged {len(notes)} note(s)")


def cmd_log(a):
    log_event(a.event, a.agent, a.card, a.text)
    print("logged")


def cmd_show(a):
    print(card_path(a.id).read_text(encoding="utf-8"))


def cmd_list(a):
    for meta, _ in all_cards():
        if a.status and meta["status"] != a.status:
            continue
        if a.milestone and meta["milestone"] != a.milestone:
            continue
        if a.role and meta["role"] != a.role:
            continue
        acd = sum(1 for x in meta["ac"] if x.get("done"))
        print(f"{meta['id']}\t{meta['milestone']}\t{meta['role']:<11}\t{meta['status']:<17}\t{meta['priority']}\tAC {acd}/{len(meta['ac'])}\t{meta['title']}")


# --------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="board.py", description="Zlayt PM project board CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--agent", default="orchestrator"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("new")
    s.add_argument("--title", required=True); s.add_argument("--milestone", required=True, choices=MILESTONE_IDS)
    s.add_argument("--role", required=True, choices=ROLES); s.add_argument("--priority", default="P1", choices=PRIORITIES)
    s.add_argument("--depends", nargs="*"); s.add_argument("--ac", action="append")
    s.add_argument("--by", default="orchestrator"); s.add_argument("--body-file"); s.add_argument("--body")
    s.add_argument("--status", default="ready", choices=["backlog", "ready", "needs_chris", "blocked"])
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("claim"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("move"); s.add_argument("id"); s.add_argument("status")
    s.add_argument("--agent", required=True); s.add_argument("--note")
    s.add_argument("--accept-debt", help="§7.4: accept after 3 rounds with the debt described here (logged to SCOPE_CUTS)")
    s.set_defaults(fn=cmd_move)

    s = sub.add_parser("note"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--text", required=True); s.set_defaults(fn=cmd_note)

    s = sub.add_parser("handoff"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--text"); s.add_argument("--file"); s.set_defaults(fn=cmd_handoff)

    s = sub.add_parser("ac"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--check", type=int); s.add_argument("--uncheck", type=int); s.add_argument("--evidence")
    s.add_argument("--add"); s.add_argument("--edit", type=int); s.add_argument("--text"); s.set_defaults(fn=cmd_ac)

    s = sub.add_parser("review"); s.add_argument("id"); s.add_argument("--persona", required=True)
    s.add_argument("--model", required=True); s.add_argument("--verdict", required=True, choices=VERDICTS)
    s.add_argument("--file", required=True); s.add_argument("--agent", default="orchestrator"); s.set_defaults(fn=cmd_review)

    s = sub.add_parser("assign"); s.add_argument("id"); s.add_argument("--to", required=True); s.set_defaults(fn=cmd_assign)

    s = sub.add_parser("dispatch"); s.add_argument("id"); s.add_argument("--personas", required=True); s.set_defaults(fn=cmd_dispatch)

    s = sub.add_parser("commit"); s.add_argument("id"); s.add_argument("--sha", required=True)
    s.add_argument("--agent", required=True); s.set_defaults(fn=cmd_commit)

    s = sub.add_parser("update"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--title"); s.add_argument("--priority", choices=PRIORITIES); s.add_argument("--role", choices=ROLES)
    s.add_argument("--milestone", choices=MILESTONE_IDS); s.add_argument("--depends", nargs="*")
    s.add_argument("--append-body"); s.set_defaults(fn=cmd_update)

    s = sub.add_parser("next"); s.add_argument("--role", required=True, choices=ROLES)
    s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_next)

    s = sub.add_parser("status"); s.add_argument("--json", action="store_true"); s.add_argument("--brief", action="store_true")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("milestone"); s.add_argument("action", choices=["set"]); s.add_argument("id", choices=MILESTONE_IDS)
    s.add_argument("--status", required=True); s.add_argument("--note"); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_milestone)

    s = sub.add_parser("gate"); s.add_argument("id", choices=MILESTONE_IDS); s.add_argument("--record", required=True)
    s.add_argument("--result", required=True, choices=["pass", "fail"]); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_gate)

    s = sub.add_parser("lesson"); s.add_argument("--agent", required=True); s.add_argument("--text", required=True)
    s.add_argument("--card"); s.set_defaults(fn=cmd_lesson)

    s = sub.add_parser("inbox"); s.add_argument("--ack", action="store_true"); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_inbox)

    s = sub.add_parser("log"); s.add_argument("--event", required=True); s.add_argument("--agent", required=True)
    s.add_argument("--card"); s.add_argument("--text", default=""); s.set_defaults(fn=cmd_log)

    s = sub.add_parser("show"); s.add_argument("id"); s.set_defaults(fn=cmd_show)

    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--milestone"); s.add_argument("--role")
    s.set_defaults(fn=cmd_list)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rc = args.fn(args)
        return rc or 0
    except BoardError as e:
        print(f"board.py: error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
