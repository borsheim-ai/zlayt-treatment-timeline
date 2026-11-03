# GATE M3+M4: installer-reviewer (fresh-eyes install of README.md at f6d5c19)

Verdict: **fail**, on one false README statement (blocker). The install and the walk themselves work.

What a first-time reader gets. I cloned the repo at f6d5c19 into an empty temp dir and followed README.md literally under `env -i` (HOME and PATH only, no key, no `.env`), on spare port 7893. `./run.sh` built `.venv`, installed requirements and served in demo mode. The server was healthy within 45 s of the clone starting. The sample case was on screen about 3 s after that. A scripted walk of all five README steps ended in two downloaded files (`sample-case-letter.txt`, `sample-case-notes.txt`) in 20.5 s of browser time. A second `./run.sh` on the same clone was healthy in 1 s with a clean `git status`.

README claims checked and found true:
- All 57 relative README links resolve in the clone (0 dead).
- The "How the AI is checked" files exist and show what the section says. `judges.py` holds J1-J4, with `GENERATOR_MODEL` and `JUDGE_MODEL` overrides and an `unavailable` verdict that is never positive. `grounding.py` does the verbatim check. `review.py` carries accept, edit and dismiss, with before and after stored in `review_events`. The judge prompts and the `/how-it-works` page match.
- Every label in the 3-minute walk matches the screen: "Open the sample case", "We found 9 records", "Draft the timeline", "19 timeline items and 4 bill amounts are ready for you to check.", "You checked every item on the timeline.", "You checked every bill amount.", "$8,390.00", "Your letter is ready. Every item has an answer.", and the Download buttons.
- The "try the checks yourself" claims hold. Leaving out a line drops it from the letter (8 lines). "No, don't count it" changes the total to $2,150.00.
- Port-in-use exits 3 with a one-line message. Python 3.9 gets a one-line refusal.

The blocker: the "Tests and evals" section says the `make evals` failure is expected, "the last lines name three `blocker:` items". On a clean clone at f6d5c19 the last lines name four. The fourth is not live-model-only: `blocker: spec_matches_golden is false`. The cause is real drift. `spec/REQUIREMENTS.md:260` still reads "Central ER discharge summary, January 9, 2026: $6,240.00". The app's letter and `evals/golden/sample.export.expected.txt:42` print "date of service [__________] (record dated January 9, 2026): $6,240.00" (D-073 fallback). The README tells the reader to treat the failure as by design, so it hides a real mismatch.

Major: the first README command cannot work as written (`OWNER` placeholder, repo not found). The README does disclose this and gives a zip alternative, so I could reach the sample case and the letter without it.

Not exercised: `docker build` and `docker run` (README itself says they were never run), `make test`, `deploy/`, live mode.

```json
{"card": "GATE-M3M4", "persona": "installer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "repo clone at f6d5c19 (README.md front door, D-074/T-212); app run via ./run.sh on http://127.0.0.1:7893 under env -i; sample case, 5-step walk, letter and notes download",
 "exercised": [
  "git clone of the repo into an empty temp dir, checkout f6d5c19 (3 s)",
  "env -i HOME PATH PORT=7893 ./run.sh: .venv created, pip install, demo mode, healthy within 45 s of clone start; GET /api/health",
  "Playwright walk of README steps 1-5 on a fresh clone: Open the sample case, Draft the timeline, answer 19 items, 4 amounts, Step 4, Download letter (.txt) and Download notes (.txt); console and HTTP errors: none",
  "Variant walk: No, leave it out on one line and No, don't count it on one charge; letter and total changed as the README says",
  "Scripted check of all 57 relative README links against the clone: 0 dead",
  "Read and grepped judges.py, grounding.py, review.py, rejudge.py, confidence.py, generator.py, pipeline.py, the prompt files listed in the README, and the /how-it-works page",
  "Second ./run.sh on the same clone (1 s, clean git status); port-in-use run (exit 3); system Python 3.9.6 run (exit 1); make config",
  "make evals on the clone: exit 2 in 14 s, four blocker lines",
  "python -I -m evals.run --check-spec and a diff read of REQUIREMENTS.md vs sample.export.expected.txt",
  "git clone https://github.com/OWNER/zlayt.git: Repository not found",
  "Not exercised: docker build/run, make test, deploy/, live mode"],
 "verdict": "fail",
 "scores": {"time_to_first_success": 5, "clean_clone_works_no_key": 5, "readme_accuracy": 2, "link_integrity": 5, "walk_labels_match_screen": 5, "tests_and_evals_instructions": 2},
 "findings": [
  {"severity": "blocker",
   "title": "README says make evals fails with three expected blockers; it names four, and the fourth is a real spec/golden mismatch",
   "evidence": "README.md 'Tests and evals': 'the last lines name three `blocker:` items'. Clean clone, env -i, `make evals` -> exit 2, 14 s. artifacts/review-evidence/GATE-M3M4-installer-make-evals.txt lists: blocker: 4_no_invented_facts; blocker: backend=fixture: determinism_3run ...; blocker: judge_controls (J3/J4 seeded wrong items): not measured; blocker: spec_matches_golden is false. The report (data/evals/20261103T133712Z.md:41) says 'spec_matches_golden: False'. spec/REQUIREMENTS.md:260 reads 'Central ER discharge summary, January 9, 2026: $6,240.00' while evals/golden/sample.export.expected.txt:42 and the app letter read 'Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00'.",
   "why_it_matters": "A README statement is false, and it tells the reader to treat the failure as by design. The fourth blocker is not live-run-only: the written spec's sample letter no longer equals what the product prints after D-073. A reviewer who runs make evals will see a number the README told them not to expect, on the one claim that explains the failure.",
   "fix": "Make the claim true. Preferred: update the spec section 6 letter and notes blocks (and record it against D-073 / SCOPE_CUTS 28) so `python -m evals.run --check-spec` passes, then the README's 'three' is correct. Minimum: change the README to the real count and say what the spec_matches_golden line means.",
   "acceptance_test": "On a fresh clone, `make evals` prints exactly the blocker lines the README names, and `.venv/bin/python -m evals.run --check-spec` reports spec_matches_golden true (or the README names the fourth and says why)."},
  {"severity": "major",
   "title": "First README command is a placeholder that fails: git clone https://github.com/OWNER/zlayt.git",
   "evidence": "README.md 'Run it': `git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt`. Run: `GIT_TERMINAL_PROMPT=0 git clone https://github.com/OWNER/zlayt.git zlayt` -> 'remote: Repository not found. fatal: repository ... not found'. The paragraph above it says the URL 'does not exist yet' and is 'in the submission email' once 'Chris publishes the public snapshot'.",
   "why_it_matters": "D-074 makes the README the front door with a two-command setup that works from a fresh clone. As committed, command one fails. The explanatory paragraph is also written for the team, not for Zlayt: it names Chris and an unpublished snapshot.",
   "fix": "Before sending, replace OWNER with the real URL and delete the 'does not exist yet' paragraph. Keep the zip route as one line. If the URL is still unknown at send time, lead with the unzip route.",
   "acceptance_test": "The first fenced command in README.md runs unmodified from an empty directory with no GitHub login and ends in a cloned `zlayt` folder."},
  {"severity": "minor",
   "title": "README walk does not mention the 'date of service [__________]' blank that every charge line in the letter now carries",
   "evidence": "Downloaded letter (artifacts/review-evidence/GATE-M3M4-installer-letter.txt, BILLED CHARGES): 'Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00'. README Step 4 mentions only 'an exhibit/Bates blank to fill in'.",
   "why_it_matters": "A reader who sees an unexplained blank in the letter may take it for a bug. The README names one blank and the letter has two kinds.",
   "fix": "Add one clause to Step 4: charge lines also carry a date-of-service blank, because the tool does not take a service date from the records (D-073).",
   "acceptance_test": "README Step 4 mentions both the Bates blank and the date-of-service blank, and both appear in the downloaded letter."}
 ],
 "whats_right": [
  "Clean clone to a running demo with no key and no .env in under a minute, and a second run starts in 1 s with a clean git status.",
  "Every walk label and expected message in the README matches the screen, and the 'How the AI is checked' links all resolve to files that show the judge, the code check and the human step.",
  "Port-in-use and old-Python failures are one clear line with a fix (exit 3 and exit 1)."],
 "questions_for_chris": ["What is the final public repo URL, or will Zlayt get the zipped folder? That decides whether the placeholder paragraph can go."]}
```
