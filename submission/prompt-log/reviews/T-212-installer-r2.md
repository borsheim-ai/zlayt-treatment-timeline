# T-212 installer review, round 2 (installer-reviewer)

Verdict: **pass**. Scope: HEAD be257c9 (fix commit for the round-1 major, the OWNER clone step). The round-1 major is closed: `git show HEAD:README.md | grep -n OWNER` returns nothing (exit 1). A fresh clone of HEAD, run under `env -i` with a fresh HOME and a spare port, reached the sample case in 19.1 s and a drafted timeline in 20.5 s. No browser errors, no API key, no traceback. The server was stopped by PID and the spare port was confirmed free.

One minor remains: the first README step is prose, with no command in it (README.md:13). It is not a blocker, and the verdict rule gives `pass`.

Method: the README was followed literally. The one exception is the clone itself. The README now gives no command for it, so I used `git clone /Users/arsis/zlayt-pm-project` as the stand-in for "the repository link you were given". Full log: `artifacts/review-evidence/T-212-installer-log.txt`. Host notes: port 7860 is held by PID 37136 and 7871 by PID 90987 (not mine, not touched), so the walk ran on spare port 7893.

## Timing (T0 = before `git clone`, epoch 1793718132)

| Milestone | Elapsed |
|---|---|
| clone finished (HEAD be257c9) | +3 s |
| server healthy (`/api/health` 200), cold HOME, cold pip | +17 s |
| "We found 9 records" (sample case visible) | +19.1 s |
| "19 timeline items and 4 bill amounts are ready" | +20.5 s |

Re-run in the same clone with the same env: healthy in 1 s. The README's "17 s" timing claim matches the cold run.

## Exercised

1. `git show HEAD:README.md | grep -n -i -E "clone|zip|OWNER|example|<"` and the full HEAD README read. Result: no OWNER; the first step is prose at line 13.
2. `git show be257c9 -- README.md` and `git diff --stat a932fc9 be257c9`: README.md only, 1 insertion and 2 deletions.
3. `git show HEAD:run.sh` read. Its Python guard, default PORT 7860 and `serve` path were checked against the run below.
4. Host check (`artifacts/review-evidence/T-212-host-check.sh`): `env -i` PATH resolves `python3` to 3.12.2; listeners on 7860 and 7871 belong to other PIDs; 7893 is free.
5. Fresh `git clone` into a `mktemp -d`, `cd zlayt`, then `env -i HOME=<fresh> PATH=<clean> PORT=7893 ./run.sh` backgrounded (PID 84130). The server log, verbatim: `"mode": "demo"`, `"anthropic_api_key": "not set"`, `"warnings": []`, `Serving on http://127.0.0.1:7893`. Env names the server received: HOME, PATH, PORT (values not printed).
6. `curl /api/health`: `"demo_mode":true`, `"answers":"prepared"`, `"live_enabled":false`, `"synthetic_only":true`.
7. Playwright walk (`artifacts/review-evidence/T-212-walk.py`, dev venv, `-I`): first screen shows "Your cases" and "Open the sample case"; sample case shows "We found 9 records", the "Prepared by our team" badge and the synthetic banner; "Draft the timeline" gives "19 timeline items and 4 bill amounts are ready"; browser errors: none.
8. Screenshots viewed: `artifacts/review-evidence/T-212-r2-01-your-cases.png`, `artifacts/review-evidence/T-212-r2-02-sample-case-step1.png`, `artifacts/review-evidence/T-212-r2-03-draft-ready.png`.
9. Stopped PID 84130 (SIGTERM). Port 7893 has no listener. Listeners on 7860 and 7871 are unchanged.
10. Re-run in the same clone with the same env: healthy in 1 s (PID 84406), then stopped; no listener left.
11. Literal `./run.sh` on 7860 under `env -i` (no PORT): exit 3 with `error: port 7860 on 127.0.0.1 is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).` This matches the README troubleshooting text.
12. `env -i ... PATH=/usr/bin:/bin:... PYTHON=/usr/bin/python3 ./run.sh` (system Python 3.9.6): exit 1 with `Python 3.12+ is required (found: Python 3.9.6). Install it, or set PYTHON=/path/to/python3.12.` This matches README.md:23.
13. `docs/CONTRACT.md:451` and `memory/ORCHESTRATOR_DECISIONS.md:73` (D-065) read for the demo label wording.

Not exercised, and why: `docker build` and `docker run` (no Docker daemon on this host; the README says so, and the item is tracked in NEEDS_CHRIS). `make test` and `make evals` (the README change in be257c9 does not touch them; verify-staff ran the eval claim at 43ce6eb). The zip path (no zip is in the repo, so the README's "unzip the download" step was not run). Public link (none is published yet). The walk's later steps 2-4 (timeline answers, bills, letter).

Model note: the brief says the expected review model is claude-sonnet-5-5, but this run is claude-haiku-5-5. The `model` field below records what ran.

## Findings

Minor, README.md:13 at be257c9, verbatim: "Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder." The only code block after it is `./run.sh`. The clone command, with a concrete example, is gone. This breaks checklist item 3 (no placeholder without an example value), and a reader with a link who does not know `git clone <url>` has nothing to copy. It is not a §5 red flag and not a spec-constraint violation, so it is minor. The zip path is clear. The gate criterion (a fresh clone reaches the sample case) holds: I ran it.

Nit, docs/CONTRACT.md:451 says demo mode is labelled "cached demo". The UI label is "Demo: sample answers prepared by our team" (screenshot 01; `/api/health` `"answers":"prepared"`), which is what memory/ORCHESTRATOR_DECISIONS.md:73 (D-065) sets. A first-time reader can tell it is demo mode and that nothing is live, so checklist item 6 holds in substance. The literal string differs from CONTRACT §10. No installer action is needed. Noted so the contract wording is revisited at the next contract change.

## Scores (1 to 5)

- golden_path_fresh_clone: 5 (clone to sample case in 19.1 s, zero browser errors)
- time_to_first_success: 5 (20.5 s to a drafted timeline, cold HOME)
- demo_mode_without_key: 5 (env has no key; server reports `anthropic_api_key: not set`, `mode: demo`)
- prereq_and_port_errors: 5 (port-in-use one-liner exit 3; Python 3.9 guard exit 1, both match the README)
- rerun_second_time: 5 (1 s)
- readme_claims_checked_true: 5 (17 s timing, port message, Python message and walk labels all match)
- first_step_copy_pasteable: 3 (prose, no command; minor finding above)

```json
{"card": "T-212", "persona": "installer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD be257c9 (fix commit for round-1 OWNER major); clone of /Users/arsis/zlayt-pm-project into a mktemp dir; app at http://127.0.0.1:7893 (spare port; 7860 and 7871 owned by other PIDs, untouched); sample case: 'Open the sample case' -> 'We found 9 records' (9 synthetic records), then 'Draft the timeline' -> 19 timeline items, 4 bill amounts",
 "exercised": [
  "git show HEAD:README.md | grep -n -i -E 'clone|zip|OWNER|example|<' (no OWNER; exit 1); full README.md at HEAD read",
  "git show be257c9 -- README.md (1 insertion, 2 deletions); git diff --stat a932fc9 be257c9 (README.md only)",
  "git show HEAD:run.sh read (Python 3.12 guard, PORT default 7860, serve path)",
  "artifacts/review-evidence/T-212-host-check.sh: env -i python3 = 3.12.2; listeners 7860 (PID 37136), 7871 (PID 90987) untouched; 7893 free",
  "artifacts/review-evidence/T-212-installer-run.sh: git clone (T0 epoch 1793718132, clone +3 s, clone HEAD be257c9); env -i HOME=<fresh> PATH=<clean> PORT=7893 ./run.sh (PID 84130) healthy +17 s; server log 'mode: demo', 'anthropic_api_key: not set', 'Serving on http://127.0.0.1:7893'; server env names HOME, PATH, PORT only",
  "curl http://127.0.0.1:7893/api/health: demo_mode true, answers prepared, live_enabled false, synthetic_only true",
  "artifacts/review-evidence/T-212-walk.py (Playwright, dev venv, -I): first screen 'Your cases' and 'Open the sample case' present; 'We found 9 records' at +19.1 s; 'Prepared by our team' and synthetic banner present; '19 timeline items and 4 bill amounts' at +20.5 s; browser errors none",
  "screenshots viewed: artifacts/review-evidence/T-212-r2-01-your-cases.png, T-212-r2-02-sample-case-step1.png, T-212-r2-03-draft-ready.png",
  "stopped PID 84130 (SIGTERM); port 7893 no listener; re-run in same clone healthy in 1 s (PID 84406), stopped, no listener",
  "literal ./run.sh on 7860 under env -i: exit 3, 'error: port 7860 on 127.0.0.1 is already in use. Pick another with PORT=7870'",
  "env -i PATH=/usr/bin:/bin:... PYTHON=/usr/bin/python3 ./run.sh: exit 1, 'Python 3.12+ is required (found: Python 3.9.6)'",
  "docs/CONTRACT.md:451 and memory/ORCHESTRATOR_DECISIONS.md:73 (D-065) read for demo label wording",
  "NOT exercised: docker build/run (no daemon, per README and NEEDS_CHRIS); make test; make evals (no README change in be257c9 touches them); zip path (no zip in repo); public link (none published); walk steps 2-4 beyond draft"
 ],
 "verdict": "pass",
 "scores": {"golden_path_fresh_clone": 5, "time_to_first_success": 5, "demo_mode_without_key": 5, "prereq_and_port_errors": 5, "rerun_second_time": 5, "readme_claims_checked_true": 5, "first_step_copy_pasteable": 3},
 "findings": [
  {"severity": "minor",
   "title": "First README step is prose with no command; the clone syntax is left to the reader",
   "evidence": "README.md:13 at be257c9, verbatim: 'Get the code: clone the repository link you were given (or unzip the download), then `cd` into its folder.' The only code block after it (README.md:15-17) is `./run.sh`. Clone run by reviewer as stand-in: git clone /Users/arsis/zlayt-pm-project zlayt (artifacts/review-evidence/T-212-installer-log.txt lines 5-6).",
   "why_it_matters": "Checklist item 3 (no placeholder without an example value). The round-1 wrong URL was removed, but no concrete clone line replaced it, so a reader with a repository link has no copyable command. The zip path is clear. Gate AC (fresh clone reaches the sample case) is met: the run reached it in 19.1 s.",
   "fix": "Until the snapshot is published, add one example line to the first code block: `git clone <repository-link> zlayt && cd zlayt`, and keep the unzip path as its own line. After publish (T-195) replace <repository-link> with the real URL, as one exact command.",
   "acceptance_test": "From an empty directory, the first README code block, with <repository-link> replaced by the given link, runs without edits to reach 'Serving on http://127.0.0.1:7860' and then 'Open the sample case' shows 'We found 9 records'."},
  {"severity": "nit",
   "title": "Demo label wording differs from CONTRACT §10 literal 'cached demo'",
   "evidence": "docs/CONTRACT.md:451: 'labels it \"cached demo\"'. Screenshot artifacts/review-evidence/T-212-r2-01-your-cases.png shows 'Demo: sample answers prepared by our team'. /api/health: '\"answers\":\"prepared\"'. memory/ORCHESTRATOR_DECISIONS.md:73 (D-065) sets the badge text.",
   "why_it_matters": "Demo mode is visibly labelled and nothing is live, so checklist item 6 holds in substance. The literal string differs from the contract; D-065 amends it, so this is recorded, not a defect.",
   "fix": "No installer action. Reconcile CONTRACT §10 wording the next time the contract is amended.",
   "acceptance_test": "grep the demo badge text in the UI and README; both read 'Demo: sample answers prepared by our team' and match D-065."}
 ],
 "whats_right": [
  "README.md at be257c9 has no OWNER placeholder (grep exit 1); the fix is 1 insertion and 2 deletions in README.md only.",
  "Fresh clone under env -i with a fresh HOME, no API key: healthy in 17 s, sample case in 19.1 s, drafted timeline in 20.5 s, no browser errors.",
  "The README's port-in-use message (exit 3) and Python 3.9 message (exit 1) match the actual output word for word."
 ],
 "questions_for_chris": [
  "When the snapshot is published (T-195), what GitHub account and repo name should the first README step use, so it can be a single exact clone command?"
 ]}
```
