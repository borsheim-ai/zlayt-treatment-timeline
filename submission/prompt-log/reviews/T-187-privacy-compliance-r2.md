# T-187 privacy/compliance review, round 2: submission/prompt-log (commit ed0508e)

Verdict: **changes**. There are 0 blockers, 3 majors and 1 nit.

The folder has no secrets and no real records, and the round-1 fixes worked for the plain forms: tailnet hostnames, tailnet IPs and the work email no longer appear anywhere in the folder, including reviews/ and board-activity.jsonl. Three problems remain:

- **Major: work email.** The work email is still published in 4 files, written as a regex with a backslash before each dot. It survives because the worker's grep only matches the plain form. README.md:8 says the address was redacted.
- **Major: content behind home paths.** The bare `/Users/arsis` username is acceptable to publish, but the paths lead to more than a username. The orchestrator transcript lists Chris's job-application and prep files, including a third party's name, and quotes source and UX documents from an <outside project> project outside this repo. The README describes all of this as "paths left as they are". Chris has to decide whether that can go public.
- **Major: publishing guidance.** The warning to publish from a fresh export appears only in the card handoff, not in NEEDS_CHRIS. It also understates the problem. HEAD still has the tailnet hostname, IPs or work email in 13 tracked files outside the prompt log, including tools/board_server.py:28 and tools/export_prompt_log.py:22, and 29 commits are authored with the work-email address. A squash of HEAD would therefore leak too.

Device names (<device> and the phone names in a three-row `tailscale status` table at orchestrator.md:900-902) are acceptable to leave. Without hostnames or IPs they cannot be used to reach anything, and the README discloses that they were left. The same goes for the `<redacted-private>` prefix that appears in grep commands. It names only a /16 inside Tailscale's shared CGNAT range.

Secrets: `check_secrets: ok (3493 file(s) scanned)`, and my own sweep found 0 scanner-pattern hits across all 1,106 archive files. The `.env` key value is a 10-character documentation placeholder, not a live key. The value was not printed and is written here as <redacted>.

Real records: every MRN and DOB is labeled SYNTHETIC, 123-45-6789 is a test string, and the phone numbers are public business contacts from fetched pages or 555 numbers.

Note: the brief named `reviews/T-187-privacy-compliance.md`. That file is the round-1 review, and reviews are append-only, so this round follows the `-r2` convention.

```json
{"card": "T-187", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/prompt-log/ at ed0508e (git archive into scratchpad, 1,106 files, 139 MB); evals/finalize_prompt_log.py, tools/export_prompt_log.py; submission/NEEDS_CHRIS.md at ed0508e; history commit 3b5fe43; card handoff. Round 2.",
 "exercised": [
  "python3 tools/board.py show T-187 (AC, notes, handoff)",
  "git archive ed0508e submission/prompt-log | tar -x into scratchpad; git status --short submission/prompt-log (clean, so the working tree matches ed0508e)",
  "python3 tools/check_secrets.py: 'check_secrets: ok (3493 file(s) scanned)'",
  "artifacts/review-evidence/T-187-r2-sweep.py: check_secrets PATTERNS over the archive (0 hits), .env value comparison (value never printed), sk-ant, key=, base64 runs, <redacted-private>, tail+hex, 100.64/10, RFC1918, emails, .local, device names, /Users paths, phone/SSN/real-record wording",
  "artifacts/review-evidence/T-187-r2-entropy.py: high-entropy mixed-case tokens (64 distinct, all hashes, CSP/SRI digests, cache keys, synthetic case ids) and 47 distinct key/token=value pairs (case ids from token_urlsafe(16) at app/db/db.py:115, plan keys, code)",
  "artifacts/review-evidence/T-187-r2-envcheck.py: the .env ANTHROPIC_API_KEY value is a 10-character documentation placeholder, not a live key; its 22 occurrences are documentation and scanner-test strings",
  "artifacts/review-evidence/T-187-r2-escaped.py: backslash-escaped and split forms of the work email, the tailnet suffix, the tail+hex label and 100.64/10",
  "Recount of README edit classes: <redacted> 525 in 65 files, <redacted-private> 508 in 114 files, [image] 705 in 103 files, escaped fences 49 in 6 files",
  "Read README.md, REDACTIONS.md, transcript header line, orchestrator transcript lines 25685-25812 and 895-905 (masked)",
  "git grep for private-network strings at ed0508e outside the prompt-log (13 tracked files); git log author emails (530 gmail, 29 work domain); git grep in 3b5fe43 (86 files with the tailnet hostname, 17 with the work email); git remote -v (none)",
  "git show ed0508e:submission/NEEDS_CHRIS.md searched for prompt-log, history, 3b5fe43, fresh, squash, public, repo"
 ],
 "verdict": "changes",
 "scores": {"secrets_absent": 5, "private_network_redaction": 3, "synthetic_only": 5, "honest_framing": 3, "history_and_publication_guidance": 2},
 "findings": [
  {"severity": "major",
   "title": "Work email still published in backslash-escaped regex form; README says it was redacted",
   "evidence": "artifacts/review-evidence/T-187-r2-escaped.py over the ed0508e archive: work-email local part plus domain, escaped, 6 hits in 4 files; escaped domain, 21 hits in the same 4 files. Locations: transcripts/session-6ddf8076-a993026d-privacy-t-187-prompt-log-review.md:746 and :1723; transcripts/session-6ddf8076-orchestrator.md:69955; transcripts/session-6ddf8076-a35c33f9-qa-t-187-regenerate-prompt-log.md:100 and :360; reviews/T-187-privacy-compliance.md:60. Each is the full address written as a regex, with a backslash before each dot, which a reader can turn back into the address at a glance. README.md:8 says: 'a work email address that is not part of this submission [is] replaced with <redacted-private>, as are bare mentions of ... that email's domain in prose'. The plain-form grep the worker used cannot match the escaped form.",
   "why_it_matters": "The prompt log is public and goes to a prospective employer. The README's redaction claim is false for this identifier, and Chris decided to redact it.",
   "fix": "In evals/finalize_prompt_log.py and tools/export_prompt_log.py, match the address and the domain with an optional run of backslashes before each dot, or strip backslashes from a copy of each line, find match spans and map them back. Count these replacements in REDACTIONS.md under the private-network class.",
   "acceptance_test": "python3 -I artifacts/review-evidence/T-187-r2-escaped.py <regenerated folder> reports 0 hits for 'escaped work-email domain' and 'work-email local part'."},
  {"severity": "major",
   "title": "Home paths are acceptable, but the content reached through them is not: job-search files and another company's project are published",
   "evidence": "transcripts/session-6ddf8076-orchestrator.md:25714 lists '<personal file> Manager_<outside project>.pdf'. Line 25738 lists <personal file>, which contains a call-prep PDF named after a third party. Lines 25752-25812 hold verbatim excerpts of <home-path>, and lines 25878 and 26090 hold app.py excerpts. Similar excerpts are in session-6ddf8076-afa8fb18-t-081-t-082-ux-review-sonnet.md:414 and session-6ddf8076-ae25cdb9-frontend-t-081-stepper-t-082-judge-panel.md:1433. Process listings with <personal file> and <home-path> appear in 10 transcripts. README.md:8 says only: 'Device names and the local /Users/<name> paths are left as they are.'",
   "why_it_matters": "On its own, a /Users/arsis path discloses only a local username, which I accept. These entries go further: they publish the names of Chris's job applications and prep files, a third party's name, and source and design documents from an <outside project> project to another prospective employer. Only Chris can say whether the <outside project> material is his to publish. The README leads a reader to think only path strings were left.",
   "fix": "Ask Chris (NEEDS_CHRIS). Unless he approves publication, have the exporter replace the tool results of commands and reads that touch paths under the home directory other than zlayt-pm-project, ~/.claude and the scratchpad with '[outside-repo content omitted]', and mask those paths as <home-path>. List the omission in README.md as a fifth edit class. If he approves, have the README say plainly that the log includes excerpts from his other local projects.",
   "acceptance_test": "grep -rIlE '<personal file>|<personal file>|<outside project>' submission/prompt-log returns nothing, or README.md names the inclusion and NEEDS_CHRIS records Chris's approval."},
  {"severity": "major",
   "title": "NEEDS_CHRIS does not tell Chris that publishing needs a fresh export, and HEAD itself still carries the tailnet host, work email and work-email author in 29 commits",
   "evidence": "Searching 'git show ed0508e:submission/NEEDS_CHRIS.md' for prompt-log, history, 3b5fe43, fresh, squash, public or repo finds only line 24 (author email changed; 'earlier commits keep the previous author') and line 33 (tailnet ports). There is no publishing warning. The warning appears only in the T-187 card handoff. git grep at ed0508e outside submission/prompt-log finds 13 tracked files with tailnet or work-email strings, including tools/board_server.py:28 (the full tailnet hostname in a default), tools/export_prompt_log.py:22 (the work email inside the redaction regex), memory/ENVIRONMENT.md, docs/RUNBOOK.md and reviews/T-005-product-manager*.md. 'git log --format=%ae' shows 29 commits authored with the work-email domain. In 3b5fe43, 86 prompt-log files hold the tailnet hostname and 17 hold the work email. README.md:14 tells readers to 'git clone https://github.com/<owner>/zlayt.git', so the repo is meant to be public.",
   "why_it_matters": "Chris publishes the submission, and he reads NEEDS_CHRIS, not card handoffs. 'A fresh export, not this history' is necessary but not enough. A squash of HEAD would still publish the hostname, the IPs and the work email from 13 files, and pushing the existing history would also publish the work-email author on 29 commits. The prompt-log redaction protects nothing if the repo beside it carries the same values.",
   "fix": "Add a NEEDS_CHRIS item, filed with a card for the orchestrator or release: (1) publish from a new single-commit repo, never this history; (2) before that, remove the tailnet hostname, IPs and work email from the tracked tree, for example by moving the board_server default host and the exporter's private patterns to env or an untracked file, and by running the same redaction over memory/, docs/RUNBOOK.md, board/ and reviews/; (3) commit as the gmail author. A one-command check should run git grep over the snapshot before pushing.",
   "acceptance_test": "NEEDS_CHRIS.md has the publishing item. On the publish snapshot, git grep -lE for the tail+hex label, a '.<redacted-private>' host, 100.64/10 addresses and the work email (plain or escaped) returns nothing, and git log --format=%ae shows only the gmail address."},
  {"severity": "nit",
   "title": "Bare-domain rule rewrote Chris's bio in the CONTRACT.md 'copy'",
   "evidence": "CONTRACT.md:601: 'Earlier PM roles at Mouseflow, <redacted-private>...'. The domain rule removed a former-employer name from the bio. README.md:20 calls the file a 'Copy of docs/CONTRACT.md'.",
   "why_it_matters": "This is a small integrity change to a document described as a copy. It is disclosed in general terms by README class 2, but not for this file.",
   "fix": "Exempt that line, since the employer name is Chris's own public career history, or add '(one employer name in the bio is redacted)' to the CONTRACT.md row.",
   "acceptance_test": "Either CONTRACT.md:601 matches docs/CONTRACT.md:601, or the README row notes the change."}
 ],
 "whats_right": [
  "No secret anywhere: check_secrets patterns find 0 hits across 1,106 files, no sk-ant value is longer than 14 characters (all placeholders), and the only .env value is a documentation placeholder.",
  "Plain-form tailnet hostnames, tail+hex labels, 100.64/10 addresses and the work email now have 0 hits, including in reviews/ and board-activity.jsonl, where round 1 found them.",
  "README edit classes and counts match a recount (525/65, 508/114, 705/103, 49/6). All patient data is labeled SYNTHETIC (for example, MRN SYN-ED-40417)."
 ],
 "questions_for_chris": [
  "May the public prompt log include excerpts from your <home-path> project and the file names in <personal file> and <personal file>, or should the exporter omit content from outside the repo?",
  "Will the repo itself be public on GitHub? If so, will you publish from a fresh single-commit snapshot with the tailnet and work-email strings removed from the tree, as gmail author?"
 ]}
```
