# T-187 privacy/compliance review: submission/prompt-log (commit 3b5fe43)

Verdict: **changes**. There are no blockers. I found no credentials and no real personal or medical data. The folder does publish the private tailnet's hostname, IP addresses and device names (major), and the "only edit is secret redaction" claim is looser than the code (minor).

What I checked:
- `tools/check_secrets.py`: `check_secrets: ok (3473 file(s) scanned)`. It scans git-tracked files, and all 1090 prompt-log files are tracked, so this covers the folder.
- My own sweep, scripts in `artifacts/review-evidence/T-187-sweep*.py`. No key value was printed.
  - Leftover `sk-ant-` fragments are all placeholders (`sk-ant-xxx`, `sk-ant-DUMMY`, `sk-ant-...`).
  - 5 `sk-` hits are `sk-not...` or `sk-proj` test strings.
  - `ghp_` appears only as fake scanner-test prefixes.
  - `ANTHROPIC_API_KEY` is `<redacted>` or a placeholder everywhere.
  - No private-key bodies, no `tskey-`, no OAuth tokens, no `.env` contents.
  - The 20+ character `token` values are the app's own case-capability tokens from local test runs, not credentials. One example token appears 123 times in the API contract.
- Personal and medical data:
  - The only SSN-shaped string is `123-45-6789`.
  - Every DOB and MRN I found is labeled SYNTHETIC (`Delphine Okonkwo-Vale (SYNTHETIC)`, `MRN: SYN-ED-40417`), or is "Jane Doe" in a test.
  - Phone numbers are business numbers scraped from web-search results, or 555 numbers.
  - Chris's name and `cborsheim@gmail.com` appear as git author and in his board inbox notes, which is appropriate for a candidate's own log. The inbox notes hold no other personal data.
- Transcript fidelity: I read `evals/finalize_prompt_log.py` and `tools/export_prompt_log.py`.
  - No real cap marker exists in the transcripts; the string appears only inside quoted source code.
  - The 291 redactions in `REDACTIONS.md` match the scripts.
- Size: 141.9 MB on disk, largest file 5.2 MB, 622 transcript files. The local git pack is 95.65 MiB (`git count-objects -vH`). This is acceptable in plain git. There is no `.gitattributes` and no remote.

Not exercised: I did not read all 622 transcripts line by line. The sweeps are pattern-based. A secret that the exporter and the scanner both missed, such as one not starting with `sk-ant-`, would not be seen.

```json
{"card": "T-187", "persona": "privacy-compliance-reviewer", "model": "claude-sonnet-5-5",
 "scope": "submission/prompt-log/ at commit 3b5fe43 (HEAD f22f8fc, working tree clean for the folder): README.md, TOOLS.md, REDACTIONS.md, transcripts/ (622 files), reviews/ (460), board-activity.jsonl, CONTRACT.md, decisions-and-lessons/; 1090 files, 141.9 MB; no app URL (documentation package)",
 "exercised": [
  "read personas/privacy-compliance.md and .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md",
  "read submission/prompt-log/README.md, TOOLS.md, REDACTIONS.md in full",
  "python3 tools/check_secrets.py -> 'check_secrets: ok (3473 file(s) scanned)' (git ls-files scope; all 1090 prompt-log files tracked, git status clean)",
  "own pattern sweep over all 1090 files (artifacts/review-evidence/T-187-privacy-sweep.py, sweep2-8): sk-*, sk-ant-* fragments, ghp_/tskey-/OAUTH/AKIA, x-api-key, authorization/bearer, password/secret/token=value, PEM bodies, KEY=VALUE env lines, 40+ char high-entropy strings; values never printed",
  "grep for tailnet CGNAT IPs (100.64-127.x), *.<redacted-private>, device names, LAN IPs, /Users/<name>, .local hosts: 17 tailnet-IP hits in 12 files, 234 <redacted-private> hits in 86 files, 13 device-name hits in 10 files",
  "email census: cborsheim@gmail.com 658 hits/267 files; <redacted-private> 27 hits/17 files; noreply@anthropic.com attribution trailers; qa@example.invalid",
  "PHI sweep: SSN-shaped (only 123-45-6789 x19), phone-shaped (17, all public business numbers or 555), MRN/DOB patterns (all labeled SYNTHETIC or Jane Doe); read the 15 board inbox events from Chris in board-activity.jsonl",
  "read evals/finalize_prompt_log.py and tools/export_prompt_log.py; counted [image] placeholders (652 in 94 files), four-backtick fence escapes (12 in 2 files), real cap markers (0), '<redacted>' markers vs REDACTIONS.md",
  "compared reviews/ against submission/prompt-log/reviews/ (diff -rq): 460 vs 462 files, T-045-staff-engineer-r3.md and T-180-ux-designer.md missing from the copy; 4347 activity lines and 190 cards on disk vs 4,341 events and 188 cards stated in TOOLS.md",
  "size: du/ls on folder and transcripts, git count-objects -vH (pack 95.65 MiB), no remote configured",
  "read docs/CONTRACT.md lines 225 and 323 (board has no auth, tailnet only; prompt-log contents) and docs/RUNBOOK.md (private tailscale serve, not funnel)"],
 "verdict": "changes",
 "scores": {"secrets_and_credentials": 5, "personal_and_medical_data": 5, "infrastructure_identifiers": 2, "transcript_fidelity_claims": 3, "reading_guide_honesty": 4, "size_and_deliverability": 4},
 "findings": [
  {"severity": "major",
   "title": "Private tailnet hostname, tailnet IPs and device names are published unredacted",
   "evidence": "Tailnet hostname <redacted-private> appears 234 times in 86 files, for example board-activity.jsonl:31 and transcripts/session-6ddf8076-aac944f8-qa.md:4170. Tailnet IPs: <redacted-private> x12, <redacted-private>, <redacted-private> (transcripts/session-6ddf8076-orchestrator.md:900-902, a `tailscale status` listing that also shows the login handle cborsheim@) and <redacted-private>. Device names `<device>`, `<device>` and `<device>` (a phone model) appear in 10 files, for example transcripts/session-6ddf8076-a3e1b297-architect.md:460, copied from memory/ENVIRONMENT.md:13. The hostname also exposes the board port 7777 and app port 7860, and the existing 443/8443/10000 mappings. docs/CONTRACT.md:225 says the board has 'No auth (tailnet only)', so tailnet obscurity is part of its protection. README.md and REDACTIONS.md say the only edit is secret-pattern redaction, and that pattern set has no tailnet rule. check_secrets passing therefore says nothing about this.",
   "why_it_matters": "The folder goes to an external hiring panel. These are not credentials, but they identify the candidate's private network, home machine and phone model, and they point at an unauthenticated STOP/inbox control surface that is protected only by tailnet membership. Nobody on a panel needs these strings to judge the work. Commit 3b5fe43 already holds the blobs, and destructive git is hook-blocked, so a plain follow-up commit will not remove them from history.",
   "fix": "Add a redaction class to evals/finalize_prompt_log.py: replace `[A-Za-z0-9-]+\\.tail[0-9a-f]+\\.<redacted-private>` with `<tailnet-host>`, tailnet-range <redacted-private>/10 addresses with `<tailnet-ip>`, and the device names (`<device>`, `<device>*`) with `<device>`. Count them in REDACTIONS.md by pattern, never by value. Regenerate the folder. Before any push, make sure the published branch does not carry the 3b5fe43 blobs (squash the folder into one fresh commit, or Chris rewrites history). Decide whether the product note and README should show the tailnet URL at all; they do not today.",
   "acceptance_test": "From submission/prompt-log: `grep -rIEl 'tail[0-9a-f]{6}\\.<redacted-private>|chriss-s25|<device>|\\b<redacted-private>\\.[0-9]+\\.[0-9]+'` returns nothing. Run the same grep over `git log -p` of the branch that will be shared. REDACTIONS.md lists the new pattern classes with counts."},
  {"severity": "minor",
   "title": "'Only edit is secret redaction' and 'unedited' are looser than the code",
   "evidence": "README.md says 'The only edit anywhere in this folder is secret redaction' and the transcripts are 'not summarized or tidied'. tools/export_prompt_log.py also (a) replaces every image block with the literal '[image]' (652 occurrences in 94 files, so screenshots the agents and reviewers looked at are absent), (b) rewrites any ```` fence inside a tool result to '` ` ` `' (fence(), 12 occurrences in 2 files), (c) renders non-text result blocks as '[type]', and (d) masks sk-ant-* and ANTHROPIC_API_KEY=value at export time, before finalize runs, so REDACTIONS.md counts only the re-spelled markers. The 'No real credential was found' sentence therefore cannot be verified from this folder for those masked values. It rests on the exporter having hidden the values.",
   "why_it_matters": "Honesty about the log is part of what is graded. A panel member who finds '[image]' or an altered fence has caught the claim as wrong, which costs more trust than the edit does. The credential claim should say what it actually rests on.",
   "fix": "Add one sentence to README.md and REDACTIONS.md listing the format-only transformations (images omitted as '[image]', ```` fences escaped, non-text blocks shown as '[type]'). Reword the credential sentence to: no key-shaped value remains in the folder, and values masked at export time were not inspected.",
   "acceptance_test": "README.md and REDACTIONS.md each mention images, fence escaping and export-time masking; a reader can reconcile '[image]' in the transcripts with the README without opening the exporter."},
  {"severity": "minor",
   "title": "A second personal or employer email address (<redacted-private>) is published in 17 transcripts",
   "evidence": "27 hits in 17 files, all `git log` output from before the T-024 author fix, for example transcripts/session-6ddf8076-a60c188d-t-012-review-privacy-compliance.md:1398 and transcripts/session-6ddf8076-ad769436-pm-review-t-025-t-005-r3.md:1504 ('16 <redacted-private>'). cborsheim@gmail.com is the address Chris gave for authorship (board-activity.jsonl, 'Email for author: cborsheim@gmail.com') and its use in author headers is appropriate. The <redacted-private> address was never given for publication.",
   "why_it_matters": "If it is a current or past employer address, a job application would be sending an employer identity to a prospective employer unintentionally. If it is a throwaway, it is still a second identity in a public packet.",
   "fix": "Ask Chris. If he does not want it published, add `<redacted-private>` to the redaction patterns and mention it in REDACTIONS.md.",
   "acceptance_test": "`grep -rIl '<redacted-private>' submission/prompt-log` returns nothing, or Chris confirms in NEEDS_CHRIS.md that it may stay."},
  {"severity": "nit",
   "title": "Reviews copy and stated counts are a stale snapshot",
   "evidence": "README says reviews/ is a 'copy of reviews/, every review', but reviews/ has 462 files and the copy has 460: T-045-staff-engineer-r3.md (written 15:11) and T-180-ux-designer.md (written 15:05) are missing. TOOLS.md says '188 cards' and '4,341 events'; disk has 190 cards and 4,347 activity lines. README flags the transcripts as a snapshot but not the reviews, and the counts disagree with the copied files.",
   "why_it_matters": "A reader who counts will find the numbers off by a few. This is small, but it is checkable.",
   "fix": "Re-run evals/finalize_prompt_log.py last, after all reviews are filed, or say 'snapshot as of 3b5fe43' next to the reviews row and the counts.",
   "acceptance_test": "`diff -rq reviews submission/prompt-log/reviews` shows only files that differ by redaction, and the counts in TOOLS.md equal `wc -l board-activity.jsonl` and `ls board/cards | wc -l`."},
  {"severity": "nit",
   "title": "Local OS username and scratch paths appear 22,489 times",
   "evidence": "`/Users/arsis` appears 22,489 times, plus session scratch paths such as /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-... in transcripts/session-6ddf8076-acdc9f4a-m0-review-security.md:1299.",
   "why_it_matters": "It is minor, but it is the same machine fingerprint as the tailnet finding, and it identifies the account name.",
   "fix": "Optional: map `/Users/arsis` to `/Users/<user>` in the same redaction pass. Paths in tool calls would no longer replay exactly, so skip this if exact replay matters more.",
   "acceptance_test": "`grep -rIc '/Users/arsis' submission/prompt-log` is zero, or the README states the paths are left as is."},
  {"severity": "nit",
   "title": "Size is acceptable, but it needs a delivery note",
   "evidence": "141.9 MB on disk (README says about 137 MB, with about 40 MB compressed). The largest file is 5.2 MB (transcripts/session-6ddf8076-orchestrator.md). The local pack is 95.65 MiB. Nothing is near a 100 MB per-file git limit. A 40 MB zip is over most email attachment limits.",
   "why_it_matters": "Plain git is the right call. The reading guide points a reader to the 4-5 files that matter. The risk is a delivery path that cannot carry it.",
   "fix": "In the email draft or README, deliver the folder as a repo link, not an attachment, and say which 3 files to open first (TOOLS.md, INDEX.md, the orchestrator session).",
   "acceptance_test": "submission/email draft links the repository, not the zip."}],
 "whats_right": [
  "The secrets handling is sound in practice: check_secrets passes, and my independent sweep found no key, token, PEM body or .env contents anywhere. Hits are labelled fakes, `<redacted>` markers, or app case tokens.",
  "Every medical identifier in the 1090 files is synthetic or labelled SYNTHETIC, and the only SSN-shaped string is 123-45-6789. There is no real patient data.",
  "The README is candid about the process, including the aborted earlier session, the stale 'capped' boilerplate, and the fact that the log is a snapshot. There are no real truncation markers, so the 'nothing was capped' claim holds."],
 "questions_for_chris": [
  "Is <redacted-private> an employer or other address you want kept out of a Zlayt submission? It appears in 17 transcripts via old git author lines.",
  "Are you comfortable with the tailnet hostname and your phone's device name being public? If not, the finalize script needs a tailnet redaction class and the folder needs regenerating on a history that does not hold the old blobs. Do you want to rewrite history (no remote exists yet) or squash into a fresh commit?"]}
```
