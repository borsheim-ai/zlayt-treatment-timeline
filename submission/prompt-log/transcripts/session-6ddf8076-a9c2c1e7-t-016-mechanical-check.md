# Subagent: T-016 mechanical check (T-016 mechanical check)

Source: `agent-a9c2c1e7b4590c4d8.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:57:15.276Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6) — mechanical check of T-016 "Compile persona dossiers into reviewer agent bodies" (M1). AC: `python3 tools/board.py show T-016`. Run exactly and quote outputs as evidence: `python3 tools/compile_agents.py --check`; `grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l` (expect 13); `grep -c "Skepticism rules (§7.3), verbatim" .claude/agents/*-reviewer.md`; `grep -c "First step, every review" .claude/agents/*-reviewer.md`; `.venv/bin/python -m pytest tools/tests/test_agents.py -q`. Each AC passes only if its command output supports it. Write reviews/T-016-staff-engineer.md (D.2 JSON, model = the model you actually run as). Do not fix anything. Reply ≤ 8 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:18.048Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-016",
 "description": "Show board card T-016 (AC source)"
}
````

### User / tool · 2026-11-02T00:57:18.181Z

**tool result**
````
---
id: "T-016"
title: "Compile persona dossiers into reviewer agent bodies (replace PROVISIONAL)"
milestone: "M1"
role: "orchestrator"
status: "in_review"
priority: "P0"
depends_on: ["T-010", "T-011"]
created_by: "orchestrator"
created_at: "2026-11-02T00:17:08Z"
updated_at: "2026-11-02T00:57:18Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T00:31:54Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "python3 tools/compile_agents.py compiles all 13 reviewer files; grep -L PROVISIONAL shows 13/13 reviewers COMPILED", "done": true, "evidence": "python3 tools/compile_agents.py --check -> 'agent definitions in sync'; grep -L PROVISIONAL .claude/agents/*-reviewer.md -> 13/13; tools/tests/test_agents.py"}
  - {"n": 2, "text": "each compiled reviewer body keeps the §7.3 skepticism rules and D.2 output format", "done": true, "evidence": "each reviewer body carries 'Skepticism rules (§7.3), verbatim' + D.2 output section (tools/compile_agents.py reviewer()); first-step live-dossier read added"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T00:31:54Z orchestrator: claimed
- 2026-11-02T00:31:54Z orchestrator: Compiled all 13 dossiers into reviewer bodies early (13/13 non-PROVISIONAL) so in-flight reviews use researched personas; will recompile after T-010/T-011 reviews if dossiers change.
- 2026-11-02T00:54:18Z orchestrator: AC 1 checked: python3 tools/compile_agents.py --check -> 'agent definitions in sync'; grep -L PROVISIONAL .claude/agents/*-reviewer.md -> 13/13; tools/tests/test_agents.py
- 2026-11-02T00:54:18Z orchestrator: AC 2 checked: each reviewer body carries 'Skepticism rules (§7.3), verbatim' + D.2 output section (tools/compile_agents.py reviewer()); first-step live-dossier read added
- 2026-11-02T00:54:18Z orchestrator: moved in_progress -> in_review
- 2026-11-02T00:57:18Z orchestrator: review dispatched: staff-engineer (haiku mechanical)

## Handoff
What changed: tools/compile_agents.py compiles personas/<slug>.md into all 13 reviewer bodies; --check drift mode + tools/tests/test_agents.py; reviewers re-read the live dossier first (host may cache definitions).
How verified: compile --check in sync; test_agents passes; litigation-lead r3 confirmed 0 dossier lines missing.
What's left: recompile after any dossier change (drift test fails otherwise).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:18.400Z

**tool call — Bash**
````
{
 "command": "python3 tools/compile_agents.py --check; echo \"EXIT=$?\"",
 "description": "Run compile_agents check and capture exit code"
}
````

### User / tool · 2026-11-02T00:57:18.505Z

**tool result**
````
agent definitions in sync
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:18.992Z

**tool call — Bash**
````
{
 "command": "grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l; echo \"---files---\"; grep -L PROVISIONAL .claude/agents/*-reviewer.md; echo \"---all reviewer files---\"; ls .claude/agents/*-reviewer.md",
 "description": "Count reviewer agent files without PROVISIONAL marker"
}
````

### User / tool · 2026-11-02T00:57:19.087Z

**tool result**
````
      13
---files---
.claude/agents/hiring-panel-reviewer.md
.claude/agents/accessibility-reviewer.md
.claude/agents/claims-adjuster-reviewer.md
.claude/agents/chaos-tester-reviewer.md
.claude/agents/installer-reviewer.md
.claude/agents/litigation-lead-reviewer.md
.claude/agents/legal-nurse-reviewer.md
.claude/agents/paralegal-reviewer.md
.claude/agents/privacy-compliance-reviewer.md
.claude/agents/security-reviewer.md
.claude/agents/product-manager-reviewer.md
.claude/agents/ux-designer-reviewer.md
.claude/agents/staff-engineer-reviewer.md
---all reviewer files---
.claude/agents/accessibility-reviewer.md
.claude/agents/chaos-tester-reviewer.md
.claude/agents/claims-adjuster-reviewer.md
.claude/agents/hiring-panel-reviewer.md
.claude/agents/installer-reviewer.md
.claude/agents/legal-nurse-reviewer.md
.claude/agents/litigation-lead-reviewer.md
.claude/agents/paralegal-reviewer.md
.claude/agents/privacy-compliance-reviewer.md
.claude/agents/product-manager-reviewer.md
.claude/agents/security-reviewer.md
.claude/agents/staff-engineer-reviewer.md
.claude/agents/ux-designer-reviewer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:19.502Z

**tool call — Bash**
````
{
 "command": "grep -c \"Skepticism rules (§7.3), verbatim\" .claude/agents/*-reviewer.md; echo \"---\"; grep -c \"First step, every review\" .claude/agents/*-reviewer.md",
 "description": "Count skepticism-rules and first-step markers per reviewer file"
}
````

### User / tool · 2026-11-02T00:57:19.601Z

**tool result**
````
.claude/agents/accessibility-reviewer.md:1
.claude/agents/claims-adjuster-reviewer.md:1
.claude/agents/chaos-tester-reviewer.md:1
.claude/agents/hiring-panel-reviewer.md:1
.claude/agents/installer-reviewer.md:1
.claude/agents/litigation-lead-reviewer.md:1
.claude/agents/legal-nurse-reviewer.md:1
.claude/agents/paralegal-reviewer.md:1
.claude/agents/privacy-compliance-reviewer.md:1
.claude/agents/security-reviewer.md:1
.claude/agents/product-manager-reviewer.md:1
.claude/agents/staff-engineer-reviewer.md:1
.claude/agents/ux-designer-reviewer.md:1
---
.claude/agents/chaos-tester-reviewer.md:1
.claude/agents/accessibility-reviewer.md:1
.claude/agents/claims-adjuster-reviewer.md:1
.claude/agents/hiring-panel-reviewer.md:1
.claude/agents/legal-nurse-reviewer.md:1
.claude/agents/litigation-lead-reviewer.md:1
.claude/agents/paralegal-reviewer.md:1
.claude/agents/product-manager-reviewer.md:1
.claude/agents/installer-reviewer.md:1
.claude/agents/staff-engineer-reviewer.md:1
.claude/agents/privacy-compliance-reviewer.md:1
.claude/agents/ux-designer-reviewer.md:1
.claude/agents/security-reviewer.md:1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:19.910Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tools/tests/test_agents.py -q; echo \"EXIT=$?\"",
 "description": "Run agent compile tests with project venv"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:20.178Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:20.399Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md"
}
````

### User / tool · 2026-11-02T00:57:20.457Z

**tool result**
````
...                                                                      [100%]
3 passed in 0.12s
EXIT=0
````

### User / tool · 2026-11-02T00:57:20.475Z

**tool result**
````
1	---
2	name: harness-review-patterns
3	description: Recurring defects in the board CLI / board server / hook guards seen in M0 reviews (rounds 1-2), plus reviewer-environment gotchas
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns (M0 round 2, HEAD f413e84):
9	- Hook guards are token/regex denylists: `board_guard.py` treats ANY token ending in `board.py` as an invocation (false-positives on `test_board.py`, `git diff -- tools/board.py x`); evaded by `bash -c`, `sh -c`, `eval`, globs, `python -c`. Always probe wrappers.
10	- Hook entry scripts `exec python3`; on system Python 3.9 the `X | None` annotations crash at import (outside try) -> rc 1 -> fail-open. Check `.claude/hooks/*.py` for `from __future__ import annotations` and import-time errors.
11	- Fixes tend to cover the implemented attack and skip the sibling (CSRF fixed via Origin==Host but no Host allowlist -> DNS rebinding passes). Test the round-1 acceptance line literally.
12	- Tests mirror the implementation (no Host test, no agent-sync test, no wrong-card/persona test). Agent files drifted from dossiers once between commits; no test.
13	- Free-text note markers (`assigned:`) used as machine state can be forged by any `note`.
14	
15	**Why:** these recurred across T-001/T-002/T-004 round 1 and 2.
16	**How to apply:** when re-reviewing harness code, re-run each round-1 acceptance test verbatim, then try the wrapper/sibling variant.
17	
18	Reviewer-environment gotchas:
19	- As a native `*-reviewer`, board-guard denies all non-read-only `board.py` subcommands even with a temp BOARD_ROOT; write-path repros cannot be run by reviewers (do not route around with python wrappers; ask the orchestrator). Read-only (`validate/show/list/status/next/inbox`) work with BOARD_ROOT set.
20	- Bash redirects are checked against the initial cwd and unexpanded `$VAR` paths: use literal absolute scratchpad paths, or put the work in a script file in the scratchpad. `... | tee path` followed by another command on the next line was also falsely denied.
21	- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.
22	
````

### User / tool · 2026-11-02T00:57:20.475Z

**tool result**
````
1	---
2	name: design-review-patterns
3	description: Recurring design-level defects found reviewing the Zlayt treatment-timeline architecture (T-014 rounds 1-2); check these first on later cards
4	metadata:
5	  type: project
6	---
7	
8	Round 1 (2026-11-01, fail): defects, all resolved in round 2 but re-check them in M2 code reviews.
9	- Flag/gap logic keyed on LLM entries instead of code-parsed record dates (r5 dropped -> false 42-day gap). In M2 test that gaps use `records.date_iso`.
10	- Export default omitted verbatim excerpt (cite=short) vs ship bar 1 / R-EX-2.
11	- Judge #2 skipped on code-classified amounts; summary numerals not code-checked; retry count wording inconsistent.
12	- Illustrative JSON in api.md had wrong offsets and a `{...}` block. Re-run `artifacts/review-evidence/T-014-json-check.py` and `T-014-r2-offset-check.py` after any api.md edit.
13	
14	Round 2 (changes, 4 majors) - new pattern: the architect's docs drift from REQUIREMENTS revision N because writer and architect edit in parallel.
15	- Export format restated in ADR-009, api.md and the golden file differ from REQUIREMENTS sec 6 (dot leaders, Source line, total-line parenthetical). Check byte-equality test target first.
16	- ADR-011 amount rules: simulate them on all `evals/golden/*.txt` (`T-014-r2-amount-sim.py`); case_09 `$275` billing-statement amount fell to `unclear`. Charges are accept/dismiss only, so a missed rule is unrecoverable for the user.
17	- Anything that calls a judge at request time (edit re-check) needs a stated judge-failure / FixtureMiss path; demo mode makes every edit a fixture miss.
18	- ADR-016 over-applied D-012 (forced inclusion of lexicon sentences; `mg.` abbreviation) vs R-TL-8 hedge-only.
19	- D-018 landed after the architect started; always check the newest D-xx against ADR category lists.
20	
21	**Why:** these made T-014 fail round 1 (2026-11-01) and require changes in round 2.
22	**How to apply:** on M2 backend review, run the golden amount simulation against the real `amounts.py`, check export equals golden file, and grep for a defined judge-unavailable path.
23	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:28.742Z

**tool call — Bash**
````
{
 "command": "echo \"COMPILED per file:\"; grep -c \"COMPILED\" .claude/agents/*-reviewer.md; echo \"D.2 keys per file (verdict+findings+whats_right):\"; for f in .claude/agents/*-reviewer.md; do printf \"%s \" \"$(basename $f)\"; grep -c -e '\"verdict\"' -e '\"findings\"' -e '\"whats_right\"' \"$f\"; done; echo \"--- test file ---\"; cat tools/tests/test_agents.py",
 "description": "Check COMPILED marker, D.2 keys, and read agent test file"
}
````

### User / tool · 2026-11-02T00:57:29.037Z

**tool result**
````
COMPILED per file:
.claude/agents/claims-adjuster-reviewer.md:1
.claude/agents/accessibility-reviewer.md:1
.claude/agents/chaos-tester-reviewer.md:1
.claude/agents/hiring-panel-reviewer.md:1
.claude/agents/litigation-lead-reviewer.md:1
.claude/agents/installer-reviewer.md:1
.claude/agents/legal-nurse-reviewer.md:1
.claude/agents/security-reviewer.md:1
.claude/agents/paralegal-reviewer.md:1
.claude/agents/privacy-compliance-reviewer.md:1
.claude/agents/product-manager-reviewer.md:1
.claude/agents/staff-engineer-reviewer.md:1
.claude/agents/ux-designer-reviewer.md:1
D.2 keys per file (verdict+findings+whats_right):
accessibility-reviewer.md 3
chaos-tester-reviewer.md 3
claims-adjuster-reviewer.md 3
hiring-panel-reviewer.md 3
installer-reviewer.md 3
legal-nurse-reviewer.md 3
litigation-lead-reviewer.md 3
paralegal-reviewer.md 3
privacy-compliance-reviewer.md 3
product-manager-reviewer.md 3
security-reviewer.md 3
staff-engineer-reviewer.md 3
ux-designer-reviewer.md 3
--- test file ---
"""Agent definitions stay in sync with the generator and dossiers (T-004 r2)."""
import subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]


def test_agents_in_sync():
    r = subprocess.run([sys.executable, str(REPO / "tools/compile_agents.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_no_provisional_reviewers():
    assert not [p.name for p in (REPO / ".claude/agents").glob("*-reviewer.md") if "PROVISIONAL" in p.read_text()]


def test_agent_prompt_errors_cleanly():
    for args in (["../../docs/CONTRACT"], ["qa", "--brief-file"], ["qa", "--brief-file", "/nonexistent"]):
        r = subprocess.run([sys.executable, str(REPO / "tools/agent_prompt.py"), *args], capture_output=True, text=True)
        assert r.returncode == 2 and "Traceback" not in r.stderr
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:33.507Z

**tool call — Bash**
````
{
 "command": "echo \"verbatim rule bullet count per file:\"; grep -c -e \"Grade against the criteria and thresholds, not against effort\" -e \"Say what you exercised (list it)\" -e \"Every finding needs evidence\" .claude/agents/*-reviewer.md; echo \"--- first step section (staff-engineer) ---\"; grep -n -A4 \"First step, every review\" .claude/agents/staff-engineer-reviewer.md; echo \"--- model/identity header ---\"; head -5 .claude/agents/staff-engineer-reviewer.md",
 "description": "Check verbatim rule bullets and first-step text in agents"
}
````

### User / tool · 2026-11-02T00:57:33.595Z

**tool result**
````
verbatim rule bullet count per file:
.claude/agents/accessibility-reviewer.md:3
.claude/agents/chaos-tester-reviewer.md:3
.claude/agents/hiring-panel-reviewer.md:3
.claude/agents/claims-adjuster-reviewer.md:3
.claude/agents/installer-reviewer.md:3
.claude/agents/legal-nurse-reviewer.md:3
.claude/agents/litigation-lead-reviewer.md:3
.claude/agents/privacy-compliance-reviewer.md:3
.claude/agents/paralegal-reviewer.md:3
.claude/agents/ux-designer-reviewer.md:3
.claude/agents/security-reviewer.md:3
.claude/agents/product-manager-reviewer.md:3
.claude/agents/staff-engineer-reviewer.md:3
--- first step section (staff-engineer) ---
21:**First step, every review:** read `personas/staff-engineer.md` in full. It is the live version of your dossier and supersedes the
22-compiled copy below (agent definitions may be cached by the host when loaded; the dossier file is always current).
23-
24-# Persona dossier (compiled from personas/staff-engineer.md)
25-
--- model/identity header ---
---
name: staff-engineer-reviewer
description: Staff engineer reviewer. Reads the diff for correctness, determinism, error handling, test quality and the LLM/code boundary as implemented.
model: sonnet
effort: high
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:57:56.509Z

**tool call — Bash**
````
{
 "command": "grep -n -e \"Skepticism\" -e \"def reviewer\" -e \"--check\" -e \"argv\" -e \"REPO\" -e \"write_text\" tools/compile_agents.py; echo \"---\"; du -sh --exclude=.venv --exclude=node_modules /Users/arsis/zlayt-pm-project 2>/dev/null | tail -1; ls /Users/arsis/zlayt-pm-project/reviews 2>&1 | head -5",
 "description": "Inspect generator skepticism emit and repo size"
}
````

### User / tool · 2026-11-02T00:57:56.608Z

**tool result**
````
20:$B ac T-### --check N --agent <role> --evidence "tests/x.py::test_y passes"
151:claim via `next` → read card + memory → work only in owned paths → run tests → `note` at each step → `ac --check` with evidence →
166:def reviewer(slug, d):
209:Skepticism rules (§7.3), verbatim:
231:def main(argv):
232:    if "--check" in argv:  # drift detection: agent files must equal generator output
240:    only = set(argv[argv.index("--only") + 1:]) if "--only" in argv else None
246:        (AGENTS / f"{name}.md").write_text(worker(name, d), encoding="utf-8"); n += 1
250:        (AGENTS / f"{slug}-reviewer.md").write_text(reviewer(slug, d), encoding="utf-8"); n += 1
255:    main(sys.argv[1:])
---
T-001-staff-engineer-r2.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer.md
T-003-security-r2.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:05.727Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"^(AGENTS|REPO|ROOT|PERSONAS|[A-Z_]+) *=\" tools/compile_agents.py; echo \"---\"; which rsync || echo \"no rsync\"",
 "description": "Confirm generator path constants before any mutation copy"
}
````

### User / tool · 2026-11-02T00:58:05.818Z

**tool result**
````
11:ROOT = Path(__file__).resolve().parent.parent
12:AGENTS = ROOT / ".claude" / "agents"
13:PERSONAS = ROOT / "personas"
15:CHEAT = """```
16:B="python3 tools/board.py"
27:SKEPTICISM = """- Grade against the criteria and thresholds, not against effort. "Mostly good" is not a verdict.
35:FINDING_SCHEMA = """Write `reviews/<card>-<persona>.md`: a short markdown summary, then exactly one fenced ```json block:
50:HANDS_ON = """## Exercising the app
56:DATA_RULES = """- Synthetic data only (Appendix A sample records or records labeled SYNTHETIC). Never fetch, generate, or imply real patient, client, or case data.
60:LLM_RULE = """Deterministic tasks are code, never LLM (dates, date arithmetic, gaps, substring verification, currency extraction, totals,
65:WORKERS = {
92:REVIEWERS = {
121:MODEL_IDS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
---
/usr/bin/rsync
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:09.723Z

**tool call — Bash**
````
{
 "command": "M=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut; rm -rf \"$M\" && mkdir -p \"$M\" && rsync -a --exclude .venv --exclude reviews --exclude artifacts /Users/arsis/zlayt-pm-project/ \"$M/\" && cd \"$M\" && sed -i '' 's/Skepticism rules (§7.3), verbatim:/Rules:/' tools/compile_agents.py && echo \"mutated generator line:\" && grep -n \"Rules:\" tools/compile_agents.py && python3 tools/compile_agents.py && echo \"regenerated (copy only)\" && python3 tools/compile_agents.py --check; echo \"check_rc=$?\"; echo \"header count after mutation:\"; grep -c \"Skepticism rules (§7.3), verbatim\" .claude/agents/*-reviewer.md | awk -F: '{s+=$2} END {print s\" total matches across 13 files\"}'; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tools/tests/test_agents.py -q; echo \"pytest_rc=$?\"",
 "description": "Mutation check in scratch copy: drop skepticism header, regenerate, rerun guards"
}
````

### User / tool · 2026-11-02T00:58:09.798Z

**tool result (error)**
````
Permission to use Bash with command M=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut; rm -rf "$M" && mkdir -p "$M" && rsync -a --exclude .venv --exclude reviews --exclude artifacts /Users/arsis/zlayt-pm-project/ "$M/" && cd "$M" && sed -i '' 's/Skepticism rules (§7.3), verbatim:/Rules:/' tools/compile_agents.py && echo "mutated generator line:" && grep -n "Rules:" tools/compile_agents.py && python3 tools/compile_agents.py && echo "regenerated (copy only)" && python3 tools/compile_agents.py --check; echo "check_rc=$?"; echo "header count after mutation:"; grep -c "Skepticism rules (§7.3), verbatim" .claude/agents/*-reviewer.md has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:31.719Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-016-staff-engineer.md",
 "content": "# T-016 review: compile persona dossiers into reviewer agent bodies (staff-engineer, mechanical pass)\n\nVerdict: **pass**. Both acceptance criteria are supported by command output. One minor finding: the sync test does not pin the content that AC2 claims.\n\nResults of the brief's commands:\n- `python3 tools/compile_agents.py --check` -> `agent definitions in sync`, exit 0.\n- `grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l` -> `13`.\n- `grep -c \"Skepticism rules (§7.3), verbatim\" .claude/agents/*-reviewer.md` -> `:1` in all 13 files.\n- `grep -c \"First step, every review\" .claude/agents/*-reviewer.md` -> `:1` in all 13 files.\n- `.venv/bin/python -m pytest tools/tests/test_agents.py -q` -> `3 passed in 0.12s`, exit 0.\n\nSupplementary checks: `COMPILED` present in 13/13; `verdict`/`findings`/`whats_right` D.2 keys present in 13/13; the three §7.3 rule bullets present in 13/13.\n\nThe shell mutation check (drop the §7.3 header from the generator in a scratch copy, regenerate, rerun the guards) was denied by the permission guard and was not run. Finding 1 is reasoned from code, not reproduced.\n\n```json\n{\"card\": \"T-016\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"T-016 AC1-AC2; tools/compile_agents.py; tools/tests/test_agents.py; .claude/agents/*-reviewer.md (13 files). No app URL (not applicable). No sample case (not applicable).\",\n \"exercised\": [\n  \"python3 tools/board.py show T-016 -> AC1 and AC2 text, status in_review\",\n  \"python3 tools/compile_agents.py --check -> 'agent definitions in sync', exit 0\",\n  \"grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l -> 13\",\n  \"grep -c COMPILED .claude/agents/*-reviewer.md -> 1 in each of 13 files\",\n  \"grep -c 'Skepticism rules (§7.3), verbatim' .claude/agents/*-reviewer.md -> 1 in each of 13 files\",\n  \"grep -c 'First step, every review' .claude/agents/*-reviewer.md -> 1 in each of 13 files\",\n  \"grep -c for the three §7.3 rule bullets and for verdict/findings/whats_right -> 3 per file in 13/13 files\",\n  \".venv/bin/python -m pytest tools/tests/test_agents.py -q -> '3 passed in 0.12s', exit 0\",\n  \"read tools/tests/test_agents.py (3 tests); grep of tools/compile_agents.py lines 11-13 (ROOT/AGENTS/PERSONAS) and 232-233 (--check)\",\n  \"read .claude/agents/staff-engineer-reviewer.md frontmatter and lines 21-22 (first-step read)\",\n  \"read harness and design review memory files for recurring patterns\",\n  \"mutation check in a scratch copy: denied by the shell permission guard; not executed\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"AC1_compile_and_sync\": 5, \"AC1_no_provisional_13of13\": 5, \"AC2_skepticism_rules_present\": 5, \"AC2_d2_format_present\": 5, \"test_guards_content_not_just_sync\": 3, \"pytest_green\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Sync test pins that files equal generator output, not that the §7.3 rules and D.2 format are present\",\n   \"evidence\": \"tools/compile_agents.py:232-233 ('--check' is 'drift detection: agent files must equal generator output'). tools/tests/test_agents.py has 3 tests: test_agents_in_sync (runs --check only), test_no_provisional_reviewers (no PROVISIONAL string), test_agent_prompt_errors_cleanly. No test asserts the 'Skepticism rules (§7.3), verbatim' header, the three rule bullets, the D.2 keys, or that exactly 13 *-reviewer.md files exist. Reasoned from code, not reproduced: if reviewer() in compile_agents.py drops the header and the files are then regenerated, --check and all three tests still pass.\",\n   \"why_it_matters\": \"AC2 is a content claim about the reviewer bodies. Right now it is only backed by hand-run greps. A future edit to the generator plus a normal recompile would silently remove §7.3 rules or the D.2 format and every automated guard would stay green. Same class of gap as the harness-review pattern 'agent files drifted from dossiers once between commits; no test'.\",\n   \"fix\": \"Add a test that, for each of the 13 *-reviewer.md files, asserts the §7.3 header, the three SKEPTICISM bullets from tools/compile_agents.py, and the D.2 keys verdict/findings/whats_right are present; and that exactly 13 reviewer files exist.\",\n   \"acceptance_test\": \"Mutate reviewer() to drop the §7.3 header, regenerate in a scratch copy, run pytest tools/tests/test_agents.py -q: the new test must fail. Unmutated tree: 4 passed.\"}\n ],\n \"whats_right\": [\n  \"--check drift mode (tools/compile_agents.py:232) gives a deterministic sync check; it returns 'agent definitions in sync' with exit 0.\",\n  \"All 13 reviewer bodies carry the §7.3 header, all three verbatim rule bullets, the D.2 keys, and the first-step live-dossier read.\",\n  \"tools/tests/test_agents.py runs offline (subprocess and file reads only) and passes 3/3.\"\n ],\n \"questions_for_chris\": [\n  \"This run is claude-haiku-5-5 (dispatched as a haiku mechanical pass per the card notes). The staff-engineer frontmatter says model: sonnet and the persona expects claude-sonnet-5-5. Is a haiku mechanical pass acceptable for the M1 gate, or does the gate need a sonnet-run staff-engineer review?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T00:58:31.876Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-016-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:33.084Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate; echo \"EXIT=$?\"",
 "description": "Run read-only board validator on the review file set"
}
````

### User / tool · 2026-11-02T00:58:33.219Z

**tool result**
````
ok (26 file(s))
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:37.549Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.",
 "new_string": "- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.\n- A chained shell mutation check in a scratch copy (`rm -rf` + `rsync` + `sed -i` + regenerate) was denied by the permission guard on T-016 (2026-11-01). Do not split the chain to get around it; reason from code and label the finding \"not reproduced\".\n- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor)."
}
````

### User / tool · 2026-11-02T00:58:37.646Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T00:58:39.907Z

T-016 review written to `/Users/arsis/zlayt-pm-project/reviews/T-016-staff-engineer.md`. Verdict: **pass** (0 blockers, 0 majors, 1 minor).
- AC1: `--check` printed `agent definitions in sync` (exit 0); `grep -L PROVISIONAL` gave 13; `COMPILED` is in 13/13.
- AC2: "Skepticism rules (§7.3), verbatim" matches 1 in each of 13 files; "First step, every review" matches 1 in each of 13; the D.2 keys and the three §7.3 bullets are present in 13/13.
- pytest `tools/tests/test_agents.py`: 3 passed, exit 0.
- Minor: the sync test only checks that files equal generator output, so a generator change plus recompile would pass with the rules removed. The mutation check in a scratch copy was denied by the permission guard, so this is reasoned from code and labelled not reproduced.
- `board.py validate`: `ok (26 file(s))`.
- Model recorded as `claude-haiku-5-5`. Question for Chris: is a haiku mechanical pass acceptable for the M1 gate, given the persona expects sonnet?
