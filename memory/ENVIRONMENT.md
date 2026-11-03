# ENVIRONMENT (orchestrator-owned)

Checked 2026-11-01 by orchestrator at bootstrap (§13.1).

| Tool | Version / status | Notes |
|---|---|---|
| OS | macOS (Darwin 25.6.0, arm64) | Chris's MacBook Pro |
| python3 | 3.12.2 | project venv at `.venv/` (gitignored). Use `.venv/bin/python`. |
| git | 2.50.1 | |
| node / npx | v21.7.1 / 10.5.0 | |
| jq | 1.7.1 | hooks use jq |
| claude CLI | 2.1.309 | logged in via claude.ai; dev LLM backend (`LLM_BACKEND=claude-cli`) |
| tailscale | installed; node `<device>` <redacted-private> | Chris's phone `<device>` on tailnet |
| tmux | /opt/homebrew/bin/tmux | |
| pandoc | /opt/homebrew/bin/pandoc | PDF/HTML exports in M5 |
| docker | /opt/homebrew/bin/docker | M4 container test |
| mmdc | not installed | Mermaid render fallback: hand-written SVG |
| Playwright | python package in .venv; chromium-headless-shell 1248 | |
| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
| Host | Claude Desktop app, Code tab | `.claude/launch.json` has URL-only entries, autoVerify false |

## Headless CLI (verified, not guessed)
Working invocation (from a cwd OUTSIDE the project):
`claude -p --model claude-haiku-5-5 --settings '{"disableAllHooks":true}' --tools "" --strict-mcp-config --output-format json --no-session-persistence --system-prompt "<sys>" "<user>"`
- Returns a JSON envelope with `result`, `total_cost_usd`, `modelUsage`. ~5 s round trip for haiku.
- `--json-schema <schema>` exists in 2.1.309 (structured output) — backend may use it, but must still validate with code.
- Model IDs confirmed live: `claude-haiku-5-5` (canonicalModel echoed). `claude-sonnet-5-5` to be confirmed by backend on first call.

## .env
`.env` exists with an `ANTHROPIC_API_KEY` entry that is 10 chars long — a placeholder, not a usable key. Treated as "no key". See NEEDS_CHRIS.

## Ports / URLs
See `docs/RUNBOOK.md` (filled after the board server starts).
- Board: http://localhost:7777
- App: http://localhost:7860
