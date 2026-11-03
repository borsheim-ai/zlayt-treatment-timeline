# M0 smoke check 4 — agent definition load tests (haiku, inline fallback)

Native load attempt: `Agent(subagent_type="paralegal-reviewer")` → "Agent type 'paralegal-reviewer' not found. Available agents: claude, claude-code-guide, Explore, general-purpose, Plan, statusline-setup". Same for `qa`.

Fallback: general-purpose subagent, model haiku, first step `python3 tools/agent_prompt.py <name>`. Replies, verbatim:

**paralegal-reviewer**
1. Agent name: paralegal-reviewer (persona: senior PI paralegal, Texas). Note: the definition loaded inline in fallback mode, so its write-guard hook is not attached.
2. Write paths: only `reviews/` and `artifacts/review-evidence/`.
3. Verdict rule: any blocker gives `fail`, otherwise any major gives `changes`, otherwise `pass`.
4. Model id: the definition says to record `claude-opus-5-5`, but I am running as `claude-haiku-5-5`, so the two disagree and you should decide which to record.
5. Body is marked PROVISIONAL, pending the M1 dossier at personas/paralegal.md.

**qa**
1. qa worker (Zlayt PM team): builds golden set, eval runner, tests, screenshots and demo video, and owns the ship-bar numbers. The definition loaded via inline fallback from `.claude/agents/qa.md`.
2. Owned paths: `tests/**`, `evals/**`, `artifacts/**` (except review-evidence), `tools/install_test.sh`.
3. Next card: `python3 tools/board.py next --role qa`
4. Never: mark my own card `done`, edit cards by hand, `git add -A` or `.`, touch real patient or client data, or print `.env` or secrets.
5. Report to the orchestrator: 15 lines maximum, with details in files.

Follow-up from reply 4: compile_agents.py now tells reviewers to record the model they actually run as.
