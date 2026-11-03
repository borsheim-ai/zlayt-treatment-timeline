# T-005 review — product-manager-reviewer

**Verdict: fail** (1 blocker, 3 majors, 3 minors).

CLAUDE.md is a tight, complete-in-shape map (81 lines, every §4.7 section present), and the board's tailnet URL works from Chris's phone path.
The card fails because a Chris action that the team itself recorded ("restart the session once") never reached
`submission/NEEDS_CHRIS.md`, and no item there has the `needs_chris` card that non-negotiable 1 requires. Majors: the restart
protocol would not actually resume an autonomous run today; the map points fresh agents at five paths that don't exist (unmarked) and leaves out
the one tool that makes reviewers spawnable in this host; and the decision/assumption logs record *what* but not *why / what if wrong*,
which is exactly what Zlayt says it grades ("decisions made under ambiguity, explained plainly").

Exercised: `wc -l CLAUDE.md` (81); existence check of 23 paths named in CLAUDE.md; CLI cheat sheet checked against `tools/board.py` argparse;
`curl` of all 4 RUNBOOK URLs + tailnet root; `tailscale serve status`; read `tools/serve_board.sh`, the STOP endpoint in
`tools/board_server.py:243-247` and the UI panel in `tools/board_ui.html:87-88` (STOP not clicked — side effect); `.claude/settings.json`
permissions; `board.py status --brief`, `list`, `list --status needs_chris`, `inbox`; read every memory file, RUNBOOK, NEEDS_CHRIS, and
CONTRACT §1, §4.5–4.8, §9, §10, §11, Appendix A.

```json
{"card": "T-005", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "CLAUDE.md, memory/*.md, memory/contracts/api.md, docs/RUNBOOK.md, memory/ENVIRONMENT.md, submission/NEEDS_CHRIS.md (working tree 2026-11-02); board http://localhost:7777 and https://<redacted-private>:7777; no sample case (M0)",
 "exercised": [
  "wc -l CLAUDE.md -> 81 (AC1 under 120: met)",
  "existence check of 23 paths named in CLAUDE.md: 5 missing (spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md, tools/export_prompt_log.py, app/README-arch.md, tools/install_test.sh)",
  "CLI cheat sheet vs tools/board.py build_parser(): all listed verbs/flags valid; `new` absent from sheet",
  "curl http://localhost:7777 -> 200; https://<redacted-private>:7777 -> 200; localhost:7860 and tailnet :7860 -> 000 (app not built; RUNBOOK says live once M3)",
  "tailscale serve status: :7777 -> 127.0.0.1:7777 present; 443 -> 4173 and 8443/10000 -> 8787 present (root returns 502, nothing on 4173)",
  "read tools/serve_board.sh, board_server.py /api/stop, board_ui.html STOP panel (in Inbox tab, typed-confirm) — did not trigger STOP",
  ".claude/settings.json: no permissions.defaultMode",
  "board.py status --brief (needs_chris=0), list, list --status needs_chris (empty), inbox (empty)",
  "read memory/STATE, PROGRESS, DECISIONS, ASSUMPTIONS, SCOPE_CUTS, LESSONS, GLOSSARY, ENVIRONMENT, contracts/api.md; docs/RUNBOOK.md; submission/NEEDS_CHRIS.md",
  "read docs/CONTRACT.md §1, §4.1, §4.5-4.8, §9, §10, §11, Appendix A 'What we evaluate'"
 ],
 "verdict": "fail",
 "scores": {"map_completeness_for_fresh_agent": 3, "runbook_operable_by_chris": 3, "restart_readiness": 2, "needs_chris_quality": 2, "decisions_under_ambiguity_legibility": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A Chris action the team recorded is missing from NEEDS_CHRIS, and no NEEDS_CHRIS item has a needs_chris card",
   "evidence": "memory/LESSONS.md:8 'NEEDS_CHRIS: restart the session once to load native definitions.' — submission/NEEDS_CHRIS.md has exactly one row (API key, line 7), no restart item. `board.py status --brief` -> needs_chris=0; `board.py list --status needs_chris` -> empty. CONTRACT §1.1: 'write it to submission/NEEDS_CHRIS.md, create a card in the needs_chris lane, state your assumption'. CONTRACT §4.8.4 names this exact item: 'note it in NEEDS_CHRIS: \"restart the session once\"'.",
   "why_it_matters": "NEEDS_CHRIS is Chris's only to-do list and the board column is what he watches on his phone. Until he restarts, native agent definitions don't load and the reviewer write-guard hook is not attached (LESSONS.md:8) — a supervision gap the harness is supposed to close. A recorded fact was lost between files, and the contract's two-part rule (file + card) is half-met.",
   "fix": "Add row 2 to NEEDS_CHRIS.md: P0/P1, 'Restart the Claude session once so .claude/agents/* load natively', exact action (see restart finding for the correct command), where the answer goes (inbox note 'restarted'), assumption meanwhile (general-purpose subagents via tools/agent_prompt.py; write-guard is instruction-only). Create a needs_chris card for each NEEDS_CHRIS row (`board.py new --status needs_chris ...`) and cross-reference the card id in the table.",
   "acceptance_test": "`board.py list --status needs_chris` lists one card per NEEDS_CHRIS row; `grep -n -i restart submission/NEEDS_CHRIS.md` hits; every row has non-empty Exact action and Assumption cells."},
  {"severity": "major",
   "title": "Restart protocol would not resume the autonomous run as written",
   "evidence": "docs/RUNBOOK.md:24-26: `./tools/serve_board.sh` and `claude --continue` with no `cd /Users/arsis/zlayt-pm-project` (both are cwd-relative; --continue picks the latest conversation in cwd). No `--dangerously-skip-permissions` flag, and .claude/settings.json has no permissions.defaultMode -> a CLI resume runs in default permission mode and will stop on prompts nobody answers (CONTRACT §0 assumes the session runs with that flag). memory/STATE.md is 3 lines (only 'Active milestone: M0'); CONTRACT §4.5 requires in-flight work, next three actions, open risks, URLs, and 'STATE.md + board.py status must be enough to resume'. The resume prompt says 're-spawn the worker teammates' but nothing a resumed agent reads (CLAUDE.md, STATE.md, RUNBOOK) mentions the tools/agent_prompt.py fallback needed when definitions don't load (LESSONS.md:8, DECISIONS.md:10). 'Recreate the heartbeat' gives no schedule/text; the §9 heartbeat spec is only in CONTRACT.",
   "why_it_matters": "Chris has no technical help during the run; RUNBOOK's restart section is the one thing he must execute correctly from memory. As written, a reboot leaves him with a session that either stalls on permission prompts or resumes with no recorded in-flight state.",
   "fix": "RUNBOOK restart: prefix `cd /Users/arsis/zlayt-pm-project`; give the exact CLI line including `--dangerously-skip-permissions` (or state that the Desktop 'reopen session' path is the supported one and how its permission mode is set); add 'if Agent type not found: use tools/agent_prompt.py fallback' and the heartbeat text, or point to a STATE.md section that holds them. Rewrite STATE.md to the §4.5 shape now (milestone, in-flight cards, next 3 actions, open risks incl. un-restarted session, URLs).",
   "acceptance_test": "A fresh agent given only CLAUDE.md + STATE.md + `board.py status` can name the in-review cards, the next 3 actions, the agent-spawn fallback and the heartbeat command without opening CONTRACT.md; RUNBOOK restart commands run verbatim from a new terminal in $HOME."},
  {"severity": "major",
   "title": "CLAUDE.md map names 5 non-existent paths as if present and omits tools a fresh agent needs",
   "evidence": "CLAUDE.md:7 lists `spec/REQUIREMENTS.md` alongside SPEC.md as current spec — missing. CLAUDE.md:41 `docs/LLM_VS_CODE.md`, :49 `tools/export_prompt_log.py`, :54 `app/README-arch.md`, :58 `tools/install_test.sh` — all missing, none marked 'created in Mx'. CLAUDE.md:49 tools row omits tools/agent_prompt.py (the only working way to spawn personas in this host), tools/serve_board.sh, tools/screenshot_board.py. Cheat sheet CLAUDE.md:24-30 omits `board.py new` (card creation, incl. `--status needs_chris`) — the verb non-negotiable 1 depends on.",
   "why_it_matters": "§4.7 makes CLAUDE.md the map a fresh/compacted agent relies on. An agent told the spec includes REQUIREMENTS.md will either search for it or invent its absence; an orchestrator after compaction can't create a needs_chris card or spawn a reviewer from the map alone.",
   "fix": "Mark future paths '(created in M1)' etc.; add agent_prompt.py, serve_board.sh to the tools row; add `$B new --title .. --milestone Mx --role r [--status needs_chris] --ac ..` to the cheat sheet. Stays under 120 lines.",
   "acceptance_test": "Script: every backticked path in CLAUDE.md either exists or carries a '(created in Mx)' marker; `grep -c 'board.py new\\|\\$B new' CLAUDE.md` >= 1; `grep agent_prompt CLAUDE.md` hits; `wc -l` < 120."},
  {"severity": "major",
   "title": "ASSUMPTIONS/DECISIONS formats record conclusions, not reasoning under ambiguity",
   "evidence": "memory/ASSUMPTIONS.md:10-12 are bare assertions, e.g. A-102 'A \"treatment gap\" is measured between consecutive dates of service across all providers, not per provider.' — no basis, confidence, impact-if-wrong, or how/who validates. memory/DECISIONS.md:3 declares 'Status · Context · Decision · Consequences · Alternatives considered' but ADR-000 (:5-10) bundles four decisions as bullets with none of Context/Consequences/Alternatives. The plainest decision under ambiguity so far — moving board/app off the contract's 443/8443 to 7777/7860 because Chris's tailnet already used them (RUNBOOK.md:11-12, LESSONS.md:7) — is not in DECISIONS at all.",
   "why_it_matters": "Appendix A grades 'Self-direction and clarity: decisions made under ambiguity, explained plainly' and §1.12 says 'Zlayt grades these explicitly'. A hiring panel reading A-102 can't tell whether it was researched, guessed, or how the product behaves if it's wrong (gap logic is in the eval golden set). Seeding a weak format now means every later entry inherits it.",
   "fix": "ASSUMPTIONS columns/fields: ID · assumption · why we believe it (source or 'unverified guess') · confidence · if wrong, what changes in the product · how we'd validate (who to ask). Split ADR-000 into ADR-000a..d in the declared format; add an ADR for the port deviation from §10. (Architect owns DECISIONS — orchestrator should card it.)",
   "acceptance_test": "Every ASSUMPTIONS entry has non-empty basis, confidence, impact-if-wrong and validation fields; every ADR has all five declared headings; `grep -n 7777 memory/DECISIONS.md` hits."},
  {"severity": "minor",
   "title": "STOP is one-tap from the phone but resume is not documented for the phone",
   "evidence": "docs/RUNBOOK.md:21 'To resume, delete board/STOP and continue the session.' tools/board_server.py exposes only POST /api/stop (line 243); there is no un-stop endpoint or UI control.",
   "why_it_matters": "RUNBOOK is written for Chris on his phone (RUNBOOK.md:6). After an accidental STOP he needs a Mac terminal to undo it, which the doc doesn't say; the Remote Control path ('tell the orchestrator: remove board/STOP and continue') would work but isn't listed.",
   "fix": "Add the phone resume path (type into the Remote Control session) and the Mac path with full path `rm /Users/arsis/zlayt-pm-project/board/STOP`.",
   "acceptance_test": "RUNBOOK Stop section lists a resume step that works with only the phone."},
  {"severity": "minor",
   "title": "Handoff claims 'RUNBOOK URLs curl-verified'; half of them can't be",
   "evidence": "curl localhost:7860 and tailnet :7860 -> 000. RUNBOOK.md:9 App (local) row says '`make run`' with no 'from M3' marker; Makefile does not exist.",
   "why_it_matters": "Chris will tap/try every row; an unmarked dead row reads as broken. Also the handoff over-claims verification.",
   "fix": "Mark both app rows 'not live until M3; `make run` added by release in M4' and state in the handoff that only board URLs were verified.",
   "acceptance_test": "Every RUNBOOK URL row either curls 200 or carries an explicit 'live from Mx' note."},
  {"severity": "minor",
   "title": "SCOPE_CUTS and STATE seeds give no worked example of the expected entry",
   "evidence": "memory/SCOPE_CUTS.md:3-4 header only; memory/STATE.md:1-3.",
   "why_it_matters": "Workers propose cuts via card notes and the orchestrator transcribes; an example row (e.g. the deferred native-agent-definition load, or contract port change) anchors the quality bar for the hiring panel.",
   "fix": "Add one real row (anything already cut in M0) to SCOPE_CUTS.",
   "acceptance_test": "SCOPE_CUTS has >= 1 row with all five columns filled."}
 ],
 "whats_right": [
  "CLAUDE.md is 81 lines and has every §4.7 section (mission, 12 rules, CLI, map, ownership, report, review protocol, data, LLM/code) — keep it this tight.",
  "Board tailnet URL returns 200 and RUNBOOK.md:11-12 explains the port deviation in plain words Chris will understand.",
  "NEEDS_CHRIS table columns (exact action · where the answer goes · assumption meanwhile) are exactly the right shape; SCOPE_CUTS columns (cut · why · cost to add) likewise."
 ],
 "questions_for_chris": [
  "memory/ENVIRONMENT.md:13 records your tailnet IP, MagicDNS name and phone device name, and RUNBOOK has the <redacted-private> hostname; if this repo is shared with Zlayt, do you want those redacted? (privacy is outside my lens; flagging only)",
  "Your pre-existing tailnet mapping 443 -> 127.0.0.1:4173 currently returns 502 (nothing listening). Was that service running before this session? LESSONS.md:7 says the team overwrote and then restored the mapping."
 ]}
```
