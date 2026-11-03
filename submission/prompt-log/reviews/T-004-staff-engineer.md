# T-004 staff-engineer-reviewer review

**Verdict: changes (0 blockers, 1 major, 3 minors, 2 nits).** All 21 files exist with valid YAML frontmatter that matches Appendix D.5:
name equals filename, one-line description (2,667 chars total across the roster, far inside the 15k-token budget), `model`, `effort: high`,
`memory: project`; the 13 reviewers carry `tools` and the PreToolUse `Edit|Write` hook, workers carry neither; researcher is opus, the other
workers sonnet; the §7.3 skepticism block is byte-identical to docs/CONTRACT.md in all 13 reviewers; `compile_agents.py` regenerates 19 of
21 files byte-for-byte (the other two differ only because personas/ dossiers now exist). The weakness is verification: the load test only
exercised the inline fallback, in which the write guard is not attached, and native loading has never been shown to work.
Evidence: `artifacts/review-evidence/T-004-agent-check.txt`.

```json
{
 "card": "T-004",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff e37efb3..fbe5690 -- tools/compile_agents.py tools/agent_prompt.py .claude/agents/ (21 files); contract §4.6, §6, D.5, §7.3",
 "exercised": [
  "python3 tools/agent_prompt.py staff-engineer-reviewer (this review was run from its output, in fallback mode)",
  "yaml.safe_load of all 21 frontmatters and per-file assertions: name==filename, description single line, model, effort, memory, tools/hooks on reviewers only, hook matcher and command, worker model per §6.1 (21/21 OK)",
  "string-compared the §7.3 skepticism block extracted from docs/CONTRACT.md against each reviewer body (13/13 verbatim)",
  "imported tools/compile_agents.py and diffed worker()/reviewer() output against the committed files (19 identical; product-manager and ux-designer differ because dossiers now exist)",
  "agent_prompt.py error paths: no args, unknown name, `--brief-file` without value, path traversal in name",
  "piped PreToolUse JSON into .claude/hooks/reviewer-write-guard.sh: Write to tools/board.py denied, Write under reviews/ allowed, ../ traversal denied, Bash redirection not inspected",
  "read artifacts/m0-smoke/agent-load-tests.md (the AC3 evidence) and checked this session's Agent tool listing for native agent types (none of the 21 are listed)",
  "read memory/DECISIONS.md ADR-000c (Python Playwright instead of the D.5 playwright mcpServers block)"
 ],
 "scores": {
  "d5_conformance": 4,
  "verifiability_of_load": 2,
  "error_handling_tooling": 3,
  "determinism_of_generator": 5
 },
 "findings": [
  {
   "severity": "major",
   "title": "Native loading of the agent definitions, and attachment of the write guard, was never exercised; AC2/AC3 evidence is fallback-only",
   "evidence": "artifacts/m0-smoke/agent-load-tests.md line 3: \"Agent(subagent_type=\\\"paralegal-reviewer\\\") -> 'Agent type 'paralegal-reviewer' not found. Available agents: claude, claude-code-guide, Explore, general-purpose, Plan, statusline-setup'\". The same list is what this session offers. The haiku replies came from `agent_prompt.py` text in a general-purpose subagent, and reply 1 itself says 'its write-guard hook is not attached'. So the frontmatter keys that make these real agents (hooks, memory, effort, tools as a comma string) have not been parsed by Claude Code, and the hook declared in frontmatter has never fired for a reviewer.",
   "why_it_matters": "§4.6/D.5 define these files as native subagent/teammate types (the orchestrator spawns workers 'by name'). If one key is wrong, the whole roster fails to load at the first real spawn, after M0 has been declared done, and every reviewer runs without the write guard in the meantime (as this review does). AC2 ('carry the write guard') is proven for the text of the file, not for behaviour. Labelled: unverified, not known-broken.",
   "fix": "After the session restart already queued in NEEDS_CHRIS: spawn `Agent(subagent_type='staff-engineer-reviewer')` and `qa`, have each report name/model/tools, and have the reviewer attempt a Write to tools/x.txt and expect the hook denial; save the transcript under artifacts/m0-smoke/. Until then, the M0 gate record should say native load is unverified.",
   "acceptance_test": "artifacts/m0-smoke/ contains a native-load transcript for one worker and one reviewer plus a denied out-of-bounds Write, each citing the agent type resolved by name."
  },
  {
   "severity": "minor",
   "title": "The write guard does not cover Bash, but every reviewer holds Bash and each body says 'a hook enforces this'",
   "evidence": "frontmatter of all 13 reviewers: `tools: Read, Grep, Glob, Bash, Write` and `matcher: \"Edit|Write\"`; body line 2: 'you may write only under reviews/ and artifacts/review-evidence/ (a hook enforces this)'. Piping {\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"echo x > tools/board.py\"}} into .claude/hooks/reviewer-write-guard.sh -> rc 0, no deny (T-004-agent-check.txt). In fallback mode there is no hook at all (tools/agent_prompt.py appends only an honor-system note).",
   "why_it_matters": "Non-negotiable 7 says reviewers never fix. A reviewer can `sed -i` a source file unhindered, and the body overstates what is enforced. This label: the matcher and tools line match D.5 exactly, so it is a gap in the template, not a deviation from it.",
   "fix": "Either add a Bash matcher to the reviewer hook that denies redirections/sed -i/tee/mv/cp/git-write outside the two allowed dirs, or reword the body to 'Edit/Write are hook-guarded; Bash writes are on your honor' and record the residual risk in DECISIONS.md.",
   "acceptance_test": "Piped Bash JSON that writes outside reviews/ returns a deny, or the body no longer claims full enforcement."
  },
  {
   "severity": "minor",
   "title": "agent_prompt.py: tracebacks instead of usage, silent frontmatter fallback, and a name that can traverse out of .claude/agents",
   "evidence": "tools/agent_prompt.py:9-10. `agent_prompt.py` -> IndexError; `agent_prompt.py nonexistent` -> FileNotFoundError traceback with no list of valid names; `agent_prompt.py qa --brief-file` -> IndexError; `agent_prompt.py ../../docs/CONTRACT` printed the whole contract (name is joined into a path unchecked). When the frontmatter regex (:11) does not match, `head, body = '', txt` silently prints the whole file with 'model: ?' (:13).",
   "why_it_matters": "This script is the only working load path today (fallback), and it is how every reviewer and worker gets its instructions; a failed load should say why and list valid names, and a malformed file should not be accepted silently.",
   "fix": "argparse with a choices list from the directory; exit 2 with a message on missing name/brief; reject names with / or ..; treat a missing frontmatter match as an error.",
   "acceptance_test": "Each of the four bad invocations above exits 2 with a one-line message and no traceback."
  },
  {
   "severity": "minor",
   "title": "Nothing detects agent files that are out of sync with the generator or the dossiers",
   "evidence": "Importing tools/compile_agents.py and comparing: product-manager-reviewer.md and ux-designer-reviewer.md differ from reviewer() output because personas/product-manager.md and personas/ux-designer.md now exist while the committed files still say <!-- PROVISIONAL -->. No test or board check compares them (tools/tests has none for agents).",
   "why_it_matters": "§4.6 says reviewer bodies are compiled from dossiers; hand-edited or stale definitions drift silently, and the Personas page labels them PROVISIONAL while a dossier exists.",
   "fix": "Add tools/tests/test_agents.py that asserts the 21 files equal compile output and (with an env/flag) that every dossier present is compiled; run compile_agents.py when dossiers land.",
   "acceptance_test": "pytest fails when a dossier exists and its agent file is still PROVISIONAL, or when any file differs from the generator."
  },
  {
   "severity": "nit",
   "title": "compile_agents.py CLI edge cases",
   "evidence": "tools/compile_agents.py main(): `--only` with no names gives an empty set, which is falsy, so all 21 files are rewritten; `--only typo` prints 'wrote 0 agent definition(s)' with rc 0; every run overwrites files unconditionally.",
   "why_it_matters": "A mistyped partial rebuild silently rewrites the roster or silently does nothing.",
   "fix": "Error on empty/unknown --only names; print which files changed.",
   "acceptance_test": "`compile_agents.py --only typo` exits 2."
  },
  {
   "severity": "nit",
   "title": "ADR-000c deviation from D.5 is not reflected in the template note",
   "evidence": "D.5 shows an mcpServers playwright block for Playwright reviewers and says qa/frontend get Playwright; the generated files carry no mcpServers and instead tell the agent to use Python Playwright from .venv (compile_agents.py HANDS_ON). memory/DECISIONS.md ADR-000c records the decision.",
   "why_it_matters": "Deviation is documented and reasonable; a reader of CONTRACT D.5 alone would flag it. Labelled: preference/consistency, not a violation.",
   "fix": "Add a one-line pointer to ADR-000c in the generator docstring.",
   "acceptance_test": "compile_agents.py docstring cites ADR-000c."
  }
 ],
 "whats_right": [
  "21/21 frontmatters parse and match D.5 (name, one-line description, model, effort, memory; hooks and tools only on reviewers).",
  "The §7.3 skepticism rules are byte-identical to the contract in all 13 reviewers, and the finding schema and verdict rule are embedded.",
  "Generator is deterministic: 19 of 21 committed files reproduce exactly from compile_agents.py."
 ],
 "questions_for_chris": [],
 "verdict": "changes"
}
```
