# T-016 review: compile persona dossiers into reviewer agent bodies (staff-engineer, mechanical pass)

Verdict: **pass**. Both acceptance criteria are supported by command output. One minor finding: the sync test does not pin the content that AC2 claims.

Results of the brief's commands:
- `python3 tools/compile_agents.py --check` -> `agent definitions in sync`, exit 0.
- `grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l` -> `13`.
- `grep -c "Skepticism rules (§7.3), verbatim" .claude/agents/*-reviewer.md` -> `:1` in all 13 files.
- `grep -c "First step, every review" .claude/agents/*-reviewer.md` -> `:1` in all 13 files.
- `.venv/bin/python -m pytest tools/tests/test_agents.py -q` -> `3 passed in 0.12s`, exit 0.

Supplementary checks: `COMPILED` present in 13/13; `verdict`/`findings`/`whats_right` D.2 keys present in 13/13; the three §7.3 rule bullets present in 13/13.

The shell mutation check (drop the §7.3 header from the generator in a scratch copy, regenerate, rerun the guards) was denied by the permission guard and was not run. Finding 1 is reasoned from code, not reproduced.

```json
{"card": "T-016", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "T-016 AC1-AC2; tools/compile_agents.py; tools/tests/test_agents.py; .claude/agents/*-reviewer.md (13 files). No app URL (not applicable). No sample case (not applicable).",
 "exercised": [
  "python3 tools/board.py show T-016 -> AC1 and AC2 text, status in_review",
  "python3 tools/compile_agents.py --check -> 'agent definitions in sync', exit 0",
  "grep -L PROVISIONAL .claude/agents/*-reviewer.md | wc -l -> 13",
  "grep -c COMPILED .claude/agents/*-reviewer.md -> 1 in each of 13 files",
  "grep -c 'Skepticism rules (§7.3), verbatim' .claude/agents/*-reviewer.md -> 1 in each of 13 files",
  "grep -c 'First step, every review' .claude/agents/*-reviewer.md -> 1 in each of 13 files",
  "grep -c for the three §7.3 rule bullets and for verdict/findings/whats_right -> 3 per file in 13/13 files",
  ".venv/bin/python -m pytest tools/tests/test_agents.py -q -> '3 passed in 0.12s', exit 0",
  "read tools/tests/test_agents.py (3 tests); grep of tools/compile_agents.py lines 11-13 (ROOT/AGENTS/PERSONAS) and 232-233 (--check)",
  "read .claude/agents/staff-engineer-reviewer.md frontmatter and lines 21-22 (first-step read)",
  "read harness and design review memory files for recurring patterns",
  "mutation check in a scratch copy: denied by the shell permission guard; not executed"
 ],
 "verdict": "pass",
 "scores": {"AC1_compile_and_sync": 5, "AC1_no_provisional_13of13": 5, "AC2_skepticism_rules_present": 5, "AC2_d2_format_present": 5, "test_guards_content_not_just_sync": 3, "pytest_green": 5},
 "findings": [
  {"severity": "minor",
   "title": "Sync test pins that files equal generator output, not that the §7.3 rules and D.2 format are present",
   "evidence": "tools/compile_agents.py:232-233 ('--check' is 'drift detection: agent files must equal generator output'). tools/tests/test_agents.py has 3 tests: test_agents_in_sync (runs --check only), test_no_provisional_reviewers (no PROVISIONAL string), test_agent_prompt_errors_cleanly. No test asserts the 'Skepticism rules (§7.3), verbatim' header, the three rule bullets, the D.2 keys, or that exactly 13 *-reviewer.md files exist. Reasoned from code, not reproduced: if reviewer() in compile_agents.py drops the header and the files are then regenerated, --check and all three tests still pass.",
   "why_it_matters": "AC2 is a content claim about the reviewer bodies. Right now it is only backed by hand-run greps. A future edit to the generator plus a normal recompile would silently remove §7.3 rules or the D.2 format and every automated guard would stay green. Same class of gap as the harness-review pattern 'agent files drifted from dossiers once between commits; no test'.",
   "fix": "Add a test that, for each of the 13 *-reviewer.md files, asserts the §7.3 header, the three SKEPTICISM bullets from tools/compile_agents.py, and the D.2 keys verdict/findings/whats_right are present; and that exactly 13 reviewer files exist.",
   "acceptance_test": "Mutate reviewer() to drop the §7.3 header, regenerate in a scratch copy, run pytest tools/tests/test_agents.py -q: the new test must fail. Unmutated tree: 4 passed."}
 ],
 "whats_right": [
  "--check drift mode (tools/compile_agents.py:232) gives a deterministic sync check; it returns 'agent definitions in sync' with exit 0.",
  "All 13 reviewer bodies carry the §7.3 header, all three verbatim rule bullets, the D.2 keys, and the first-step live-dossier read.",
  "tools/tests/test_agents.py runs offline (subprocess and file reads only) and passes 3/3."
 ],
 "questions_for_chris": [
  "This run is claude-haiku-5-5 (dispatched as a haiku mechanical pass per the card notes). The staff-engineer frontmatter says model: sonnet and the persona expects claude-sonnet-5-5. Is a haiku mechanical pass acceptable for the M1 gate, or does the gate need a sonnet-run staff-engineer review?"
 ]}
```
