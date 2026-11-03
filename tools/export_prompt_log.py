#!/usr/bin/env python3
"""Export Claude Code transcripts for this project to readable markdown (the prompt log Zlayt asks for).

One markdown file per session and per subagent, unedited except: secret-shaped strings and private network details
(tailnet hostnames, 100.64/10 addresses, a work email) are redacted, images become [image], and four-backtick fences
are escaped so the markdown stays valid. Usage:
  python3 tools/export_prompt_log.py [--out submission/prompt-log/transcripts] [--max-result 4000]
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJ = Path.home() / ".claude" / "projects" / ("-" + str(ROOT).strip("/").replace("/", "-").replace("_", "-"))
SECRET = re.compile(r"sk-ant-[A-Za-z0-9_\-]{4,}|(ANTHROPIC_API_KEY\s*=\s*)\S+")


# Private network details are redacted too (T-187 privacy review): tailnet hostnames and names, Tailscale CGNAT addresses
# (<redacted-private>/10), and a work email that is not part of the submission.
PRIVATE = re.compile(r"\b[A-Za-z0-9-]+\.tail[0-9a-f]+\.<redacted-private>\b|\btail[0-9a-f]{6,}\b"
                     r"|\b<redacted-private>\.\d{1,3}\.\d{1,3}\b|\b<redacted-private>\b", re.I)


def redact(s: str) -> str:
    s = SECRET.sub(lambda m: (m.group(1) or "") + "<redacted>", s)
    return PRIVATE.sub("<redacted-private>", s)


def fence(s: str) -> str:
    return "````\n" + s.replace("````", "` ` ` `") + "\n````"


def render_content(content, max_result: int) -> list[str]:
    out = []
    if isinstance(content, str):
        return [content]
    for c in content or []:
        t = c.get("type")
        if t == "text":
            out.append(c.get("text", ""))
        elif t == "thinking" and c.get("thinking"):
            out.append("<details><summary>thinking</summary>\n\n" + c["thinking"] + "\n\n</details>")
        elif t == "tool_use":
            inp = json.dumps(c.get("input"), ensure_ascii=False, indent=1)
            out.append(f"**tool call — {c.get('name')}**\n" + fence(inp))
        elif t == "tool_result":
            r = c.get("content")
            if isinstance(r, list):
                r = "\n".join(x.get("text", f"[{x.get('type')}]") for x in r if isinstance(x, dict))
            r = str(r or "")
            if len(r) > max_result:
                r = r[:max_result] + f"\n[... {len(r) - max_result} more characters capped by export_prompt_log.py --max-result {max_result}]"
            out.append("**tool result" + (" (error)" if c.get("is_error") else "") + "**\n" + fence(r))
        elif t == "image":
            out.append("[image]")
    return out


def export(jsonl: Path, title: str, dest: Path, max_result: int) -> int:
    lines = [f"# {title}", "", f"Source: `{jsonl.name}` (Claude Code transcript). Unedited except secret redaction.", ""]
    n = 0
    for raw in jsonl.read_text(errors="replace").splitlines():
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if d.get("type") not in ("user", "assistant"):
            continue
        msg = d.get("message") or {}
        parts = render_content(msg.get("content"), max_result)
        if not parts:
            continue
        who = "Assistant" if d["type"] == "assistant" else ("User" if d.get("origin", {}).get("kind") == "human" else "User / tool")
        model = msg.get("model")
        lines.append(f"### {who}{(' · ' + model) if model else ''} · {d.get('timestamp', '')}")
        lines.append("")
        lines.extend(parts)
        lines.append("")
        n += 1
    dest.write_text(redact("\n".join(lines)), encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="submission/prompt-log/transcripts")
    ap.add_argument("--max-result", type=int, default=4000)
    a = ap.parse_args()
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    index = ["# Transcript index", "", "| File | Agent | Model | Messages |", "|---|---|---|---|"]
    for sess in sorted(PROJ.glob("*.jsonl"), key=lambda p: p.stat().st_mtime):
        name = f"session-{sess.stem[:8]}-orchestrator.md"
        n = export(sess, f"Main session {sess.stem} (orchestrator / Chris)", out / name, a.max_result)
        index.append(f"| [{name}]({name}) | orchestrator (main session) | claude-opus-5-5 | {n} |")
        sub = PROJ / sess.stem / "subagents"
        for j in sorted(sub.glob("agent-*.jsonl"), key=lambda p: p.stat().st_mtime) if sub.exists() else []:
            meta = {}
            m = j.with_suffix(".meta.json")
            if m.exists():
                try:
                    meta = json.loads(m.read_text())
                except json.JSONDecodeError:
                    pass
            label = meta.get("name") or meta.get("description") or j.stem
            slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:50]
            fname = f"session-{sess.stem[:8]}-{j.stem[6:14]}-{slug}.md"
            n = export(j, f"Subagent: {label} ({meta.get('description', '')})", out / fname, a.max_result)
            index.append(f"| [{fname}]({fname}) | {label} — {meta.get('description', '')} | {meta.get('model', '?')} | {n} |")
    (out / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"exported {len(index) - 4} transcript(s) to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
