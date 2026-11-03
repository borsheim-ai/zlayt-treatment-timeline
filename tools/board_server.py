#!/usr/bin/env python3
"""Board web UI server (stdlib only). Read-only except the inbox form and the STOP button.

Run: python3 tools/board_server.py [--port 7777]
Serves tools/board_ui.html and a JSON API over board/, memory/, reviews/, personas/ and .claude/agents/.
Tailnet-only exposure via `tailscale serve` (never Funnel). No auth by design.
"""
from __future__ import annotations
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board as B  # noqa: E402

ROOT = B.ROOT
UI = Path(__file__).resolve().parent / "board_ui.html"
READABLE = ["memory", "reviews", "personas", "research", "submission", "docs/RUNBOOK.md", "docs/LLM_VS_CODE.md",
            "spec", "board/milestones.md", "board/ALERT.md", "evals/reports", "artifacts/CAPTIONS.md"]
ALLOWED_HOSTS = {h.strip().lower() for h in os.environ.get(
    "BOARD_ALLOWED_HOSTS", "localhost,127.0.0.1,<redacted-private>").split(",") if h.strip()}
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
URLS = {"board": os.environ.get("BOARD_URL", "http://localhost:7777"), "app": os.environ.get("APP_URL", "http://localhost:7860")}


def _runbook_urls():
    try:
        txt = (ROOT / "docs" / "RUNBOOK.md").read_text()
        out = dict(URLS)
        m = re.search(r"Board \(tailnet\)[^\n]*?(https?://\S+)", txt)
        if m:
            out["board_tailnet"] = m.group(1).rstrip(")|`")
        m = re.search(r"App \(tailnet\)[^\n]*?(https?://\S+)", txt)
        if m:
            out["app_tailnet"] = m.group(1).rstrip(")|`")
        return out
    except FileNotFoundError:
        return URLS


def cards_payload():
    out = []
    for meta, body in B.all_cards():
        la = B.last_activity(meta, body)
        d = dict(meta)
        d["last_activity"] = la.strftime("%Y-%m-%dT%H:%M:%SZ") if la else None
        d["stalled"] = bool(meta.get("status") == "in_progress" and la and
                            (dt.datetime.now(dt.timezone.utc) - la).total_seconds() > B.STALL_MINUTES * 60)
        d["body"] = body
        out.append(d)
    return out


def agents_payload():
    reviews_by_persona: dict = {}
    for p in sorted((ROOT / "reviews").glob("*.md")):
        if p.name.startswith(("GATE-", "CONTRACT-")):
            continue
        try:
            d = B.review_json(p)
        except Exception:
            d = None
        if not d:
            continue
        persona = d.get("persona", "?")
        if not persona.endswith("-reviewer"):
            persona = persona + "-reviewer"
        r = reviews_by_persona.setdefault(persona, {"counts": {"pass": 0, "changes": 0, "fail": 0}, "findings": []})
        r["counts"][d.get("verdict", "pass")] = r["counts"].get(d.get("verdict", "pass"), 0) + 1
        for f in d.get("findings", []):
            if isinstance(f, dict):
                r["findings"].append({"card": d.get("card"), "severity": f.get("severity"), "title": f.get("title"),
                                      "file": str(p.relative_to(ROOT)), "mtime": p.stat().st_mtime})
    agents = []
    for p in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        try:
            meta = {}
            txt = p.read_text()
            head = txt.split("\n---", 1)[0]
            for line in head.splitlines():
                m = re.match(r"^(name|description|model|effort|tools):\s*(.*)$", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
            name = meta.get("name", p.stem)
            kind = "reviewer" if name.endswith("-reviewer") else "worker"
            slug = name.replace("-reviewer", "")
            dossier = ROOT / "personas" / f"{slug}.md"
            summary = ""
            if dossier.exists():
                dt_ = dossier.read_text()
                para = [x.strip() for x in dt_.split("\n\n") if x.strip() and not x.strip().startswith("#")]
                summary = para[0][:600] if para else ""
            r = reviews_by_persona.get(name, {"counts": {"pass": 0, "changes": 0, "fail": 0}, "findings": []})
            findings = sorted(r["findings"], key=lambda f: -f["mtime"])[:10]
            agents.append({"name": name, "kind": kind, "model": meta.get("model"), "description": meta.get("description"),
                           "status": "PROVISIONAL" if "<!-- PROVISIONAL -->" in txt else ("COMPILED" if kind == "reviewer" else "active"),
                           "dossier": str(dossier.relative_to(ROOT)) if dossier.exists() else None, "dossier_summary": summary,
                           "review_counts": r["counts"], "last_findings": findings})
        except Exception as e:  # never break the page on one bad file
            agents.append({"name": p.stem, "kind": "?", "error": str(e)})
    return agents


def activity_payload(limit=300, persona=None):
    try:
        lines = (ROOT / "board" / "activity.jsonl").read_text().splitlines()
    except FileNotFoundError:
        return []
    out = []
    for ln in reversed(lines):
        try:
            e = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if persona and persona not in (e.get("agent") or "") and persona != e.get("persona"):
            continue
        out.append(e)
        if len(out) >= limit:
            break
    return out


def health_payload():
    acts = activity_payload(2000)
    orch = next((e["ts"] for e in acts if e.get("agent") == "orchestrator"), None)
    seen = {}
    for e in acts:
        a = e.get("agent")
        if a and a not in seen:
            seen[a] = e["ts"]
    teams = []
    for cfg in glob.glob(os.path.expanduser("~/.claude/teams/*/config.json")):
        try:
            c = json.loads(Path(cfg).read_text())
            teams.append({"team": Path(cfg).parent.name, "members": [m.get("name") for m in c.get("members", [])]})
        except Exception:
            pass
    hb = None
    prog = ROOT / "memory" / "PROGRESS.md"
    if prog.exists():
        hb = dt.datetime.fromtimestamp(prog.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"last_orchestrator_event": orch, "progress_md_mtime": hb, "agents_seen": seen, "teams": teams,
            "urls": _runbook_urls(), "stop_requested": (ROOT / "board" / "STOP").exists(),
            "alert": (ROOT / "board" / "ALERT.md").read_text() if (ROOT / "board" / "ALERT.md").exists() else None}


def milestones_payload():
    s = B.compute_status()
    out = []
    for m in s["milestones"]:
        d = dict(m)
        d.update(s["by_milestone"].get(m["id"], {"total": 0, "done": 0}))
        if m.get("gate_record") and (ROOT / m["gate_record"]).exists():
            d["gate_summary"] = (ROOT / m["gate_record"]).read_text()[:20000]
        out.append(d)
    cuts = (ROOT / "memory" / "SCOPE_CUTS.md").read_text() if (ROOT / "memory" / "SCOPE_CUTS.md").exists() else ""
    return {"milestones": out, "scope_cuts": cuts, "done_checks": s["done_checks"], "progress_pct": s["progress_pct"]}


def safe_read(rel: str):
    rel = rel.lstrip("/")
    p = (ROOT / rel).resolve()
    try:
        r = p.relative_to(ROOT)
    except ValueError:
        return None
    if not any(str(r) == a or str(r).startswith(a.rstrip("/") + "/") for a in READABLE):
        return None
    if not p.is_file() or p.stat().st_size > 2_000_000:
        return None
    return p.read_text(errors="replace")


class H(BaseHTTPRequestHandler):
    server_version = "ZlaytBoard/1.0"

    def log_message(self, fmt, *args):  # request log (no bodies)
        try:
            with open(ROOT / "board" / ".server.log", "a") as f:
                f.write("%s %s\n" % (self.log_date_time_string(), fmt % args))
        except OSError:
            pass

    def _send(self, code, payload, ctype="application/json"):
        data = payload if isinstance(payload, (bytes, bytearray)) else (
            json.dumps(payload, ensure_ascii=False, default=str).encode() if ctype == "application/json" else str(payload).encode())
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if "json" in ctype or "text" in ctype else ""))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _host_ok(self) -> bool:
        """DNS-rebinding guard: only our own host names may address this server."""
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]").lower()
        return host in ALLOWED_HOSTS

    def do_HEAD(self):
        self.send_response(405)
        self.end_headers()

    def do_GET(self):
        if not self._host_ok():
            return self._send(421, {"error": "unknown host"})
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path in ("/", "/index.html"):
                return self._send(200, UI.read_bytes(), "text/html")
            if u.path == "/api/status":
                return self._send(200, B.compute_status())
            if u.path == "/api/cards":
                return self._send(200, cards_payload())
            if u.path == "/api/agents":
                return self._send(200, agents_payload())
            if u.path == "/api/activity":
                lim = int(q["limit"]) if q.get("limit", "").isdigit() else 300
                return self._send(200, activity_payload(min(lim, 2000), q.get("persona")))
            if u.path == "/api/milestones":
                return self._send(200, milestones_payload())
            if u.path == "/api/health":
                return self._send(200, health_payload())
            if u.path == "/api/file":
                txt = safe_read(q.get("path", ""))
                return self._send(200, {"path": q.get("path"), "text": txt}) if txt is not None else self._send(404, {"error": "not readable"})
            if u.path == "/api/inbox":
                notes = [{"name": p.name, "text": p.read_text()} for p in B.inbox_unread()]
                arch = sorted((ROOT / "board" / "inbox" / "archive").glob("*.md"), reverse=True)[:20]
                return self._send(200, {"unread": notes, "archived": [{"name": p.name, "text": p.read_text()} for p in arch]})
            if u.path == "/healthz":
                return self._send(200, {"ok": True})
            return self._send(404, {"error": "not found"})
        except Exception as e:
            sys.stderr.write(f"GET {self.path} failed: {type(e).__name__}: {e}\n")
            return self._send(500, {"error": "internal error"})

    def _csrf_ok(self) -> str | None:
        """Cross-site POSTs are refused: JSON content type + custom header (forces a CORS preflight we never answer)
        + Origin, when present, must match Host. The orchestrator treats inbox notes as Chris's instructions."""
        if (self.headers.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
            return "Content-Type must be application/json"
        if self.headers.get("X-Board-Client") != "1":
            return "missing X-Board-Client header"
        origin, host = self.headers.get("Origin"), self.headers.get("Host") or ""
        if origin and urlparse(origin).netloc.lower() != host.lower():
            return "cross-origin request refused"
        return None

    def do_POST(self):
        try:
            return self._post()
        except Exception as e:  # never drop the connection on bad input
            return self._send(400, {"error": f"bad request: {type(e).__name__}"})

    def _post(self):
        u = urlparse(self.path)
        if not self._host_ok():
            return self._send(421, {"error": "unknown host"})
        bad = self._csrf_ok()
        if bad:
            return self._send(403, {"error": bad})
        n = int(self.headers.get("Content-Length") or 0)
        if n < 0 or n > 20000:
            return self._send(413, {"error": "too large"})
        raw = self.rfile.read(n).decode("utf-8", "strict")
        body = json.loads(raw)
        if not isinstance(body, dict):
            return self._send(400, {"error": "body must be a JSON object"})
        if u.path == "/api/inbox":
            text = body.get("text")
            if not isinstance(text, str):
                return self._send(400, {"error": "text must be a string"})
            text = text.strip()
            if not text:
                return self._send(400, {"error": "empty note"})
            ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            p = ROOT / "board" / "inbox" / f"{ts}.md"
            B.atomic_write(p, f"# Note from Chris — {B.now()}\n\n{text}\n")
            B.log_event("inbox", "chris", None, text[:200])
            return self._send(200, {"ok": True, "file": str(p.relative_to(ROOT))})
        if u.path == "/api/stop":
            if body.get("confirm") != "STOP":
                return self._send(400, {"error": "confirm must be 'STOP'"})
            (ROOT / "board" / "STOP").write_text(f"STOP requested from board UI at {B.now()}\n")
            B.log_event("stop", "chris", None, "STOP requested from board UI")
            return self._send(200, {"ok": True})
        return self._send(404, {"error": "not found"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("BOARD_PORT", 7777)))
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), H)
    print(f"board server on http://{a.host}:{a.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
