# NEEDS CHRIS

Only things the team cannot do or decide without you. Nothing here blocks the run: each row says what we assumed meanwhile. Sorted by priority (P0 first). Open `needs_chris` cards on the board at the time of writing: T-019, T-022, T-023, T-189, T-190, T-191, T-192, T-193. T-195 is also here as a record: it was P0 and is now done (row 2).

**Where to answer.** Two places, named in each row:
- **Inbox:** the board page, Inbox tab, type one line, Send (`docs/RUNBOOK.md`, "Steer"). It lands in `board/inbox/` and the orchestrator acts on it.
- **File:** edit the named file in the repo, then re-render the PDFs with `bash submission/build_pdfs.sh` and put a one-line "done" in the Inbox.

You hand Zlayt the running demo and the repo (D-074), so the two links you owe are the demo link and the repo link.

| # | Pri | Card | What | Exact action and where | Assumed meanwhile |
|---|---|---|---|---|---|
| 1 | P0 | T-189 | **The one story: a feature or launch you owned that missed the mark.** Yours alone; the team will not write it. | **File:** replace the `[CHRIS: write this yourself ...]` block at the end of `submission/part2-process.md` ("The one story: a miss") with about 200 words: (1) what you shipped and expected, (2) what you missed and the number or signal that showed it, (3) one concrete process change (an artifact or a rule), (4) how it shows up in this project. Hooks from this build are listed in the block. | The marked block stays; the rest of Part 2 is complete. |
| 2 | P0 | T-195 | **Done. Publishing: only the public snapshot is pushed, never this working repo.** The working repo's history has the tailnet host and IPs in older commits and 29 commits authored with the work email. | **Done:** the snapshot is pushed to https://github.com/borsheim-ai/zlayt-treatment-timeline as a private repo, one commit on `main` (checked on GitHub). This working repo, its history and its branches were not pushed. | The repo is private, so Zlayt cannot open it yet; see row 6. Scan and its limits: `deploy/SNAPSHOT.md`. |
| 3 | P1 | T-190 | Byline and links | **File:** in `submission/product-note.md` line 3 and `submission/part2-process.md` line 3, replace `[CHRIS: full name]`; in the product note replace `[CHRIS: public link, ...]` with the demo link (see #4). In `submission/email-draft.md` fill every `[CHRIS: ...]` (contact, subject, demo link, repo link, your name). | Placeholders stay visible, so nothing goes out with a made-up name or link. |
| 4 | P1 | T-022 | Public demo link: cached demo only, or live model? | **Inbox:** `demo-only` or `live, cap $N/day`. Then paste the URL where #3 says. | Demo-only: the cached sample run through the real pipeline code; live needs an env opt-in (D-008). |
| 5 | P1 | T-193 | Prompt log: may it show job-application file names, the <outside project> project quotes and the third-party name? | **Inbox:** `show` or `redact`. The final prompt-log build (T-187) follows your answer. | Redacted. |
| 6 | P1 | none | **Give Zlayt read access to the private repo.** | **GitHub:** repo `borsheim-ai/zlayt-treatment-timeline`, Settings, then Collaborators. Add the GitHub username Zlayt gives you with read access. Or make the repo public when you are ready. | Until this is done, the repo link in the email asks Zlayt for a login. |
| 7 | P1 | T-019 | Real Anthropic API key, only if you answered "live" in #4 | **File and host secret:** `ANTHROPIC_API_KEY=...` in the local, gitignored `.env`, and as the Space secret `ANTHROPIC_API_KEY` on Hugging Face. Never in chat, a card or git. | Dev runs on the `claude-cli` backend (your claude.ai login); the public build runs the cached demo. |
| 8 | P2 | T-190 | Optional one-line real examples in Part 2 (each marked `[CHRIS: optional ...]`) | **File:** `submission/part2-process.md`. Area 1: watching real work without exposing client data. Area 5: how you measured the ~80% adoption on the OutSystems AI Agent Builder. Area 8: a late feature you supervised and what you cut. One or two sentences each, or delete the marker. | Part 2 reads complete without them. |
| 9 | P2 | T-190 | Product note, ship-bar row 5: the 4/5 "I could verify every claim quickly" is a persona, twice (old screen, guided screen); no real paralegal has used it | **File:** `submission/product-note.md` row 5 and the "Reviewability passed on paper" bullet; also `submission/part2-process.md` area 4. Have a paralegal run the sample case once and give you the score; replace the persona wording with it. | The documents say plainly that both scores are a persona's. |
| 10 | P2 | T-191 | Product note, Cut paragraph: why you reinstated cuts (D-031, D-042) and shipped three stretch items when the brief says at most one | **File:** `submission/product-note.md`, replace `[CHRIS: your reason, one line.]`. | The note records the decisions and their cost and leaves the reason marked. |
| 11 | P2 | T-192 | Part 2, area 6: the decision rights you give engineering | **File or Inbox:** confirm or change the "Engineering" paragraph (engineering decides how and has a "not safe to ship" veto; only a founder overrides it in writing; evidence first, then the safer answer for anything the carrier sees). | The paragraph stands as your stated stance. |
| 12 | P2 | T-023 | Live-model eval budget on your claude.ai plan (about 25 to 35 calls per sample run) | **Inbox:** `ok` or a cap, e.g. `max 300 calls`. | Live runs only for ship-bar measurements; fixtures otherwise. |
| 13 | last | none | **Send the email.** Nobody sends it for you. | After #1 to #6: open `submission/email-draft.md`, check every link opens without a login, send as a reply on the original thread. | Draft only. |

Optional, not blocking: the demo video ships in the repo as `artifacts/demo.webm` (174 s, sample case), the narration is burned in as on-screen captions, and the snapshot keeps the video and the screenshots (T-217). Nothing to host or paste for it. If you want your own voice, read `artifacts/NARRATION.md` over the video and replace the file; otherwise leave it.

## Answered
- Git author email (T-024): Chris gave the gmail address (00:47Z). Set repo-locally; earlier commits keep the previous author because history rewrites are blocked.

## Decided by the team — FYI, no action needed
Product calls we made under ambiguity. Override any of them through the Inbox if you disagree.
- Citation format in the export: `Provider, date of service` + `[Ex. __ / Bates __]` placeholder (A-106). Real Zinda practice is a discovery question in Part 2, area 1.
- Flags (gaps, priors, causation) never go in the letter text; they go in a separate "internal — do not send" block (D-001).
- AI-assistance statement: UI banner + internal notes, not the letter (D-009).
- Flagged record language may appear in the letter only as part of an accepted whole-sentence excerpt, listed in internal notes (D-012).
- Ambiguous dates are never inferred; the paralegal confirms them (D-010).
- Tailnet ports: board on :7777, app on :7860; your existing 443/8443 mappings untouched (ADR-000e).

## Letter total wording changed (D-062, 2026-11-02) — FYI, override if you disagree
- The carrier letter's total line now reads `Billed charges accepted from these records: $X` (was `... stated in these records`). Three adversarial rounds showed a classifier can be outworded by a crafted ledger, so the line now says exactly what it is: the sum of the charges the paralegal accepted one at a time, each listed with its source line. Assumption: firms prefer an honest, defensible total over one that implies the records state it.

## Docker verification (T-182) — 2 minutes, optional
- This Mac has the Docker client but no running daemon, so the image was verified with the same recipe outside Docker (fresh venv, README path 17 s). If you have Docker Desktop: start it, then run `make docker docker-run` in the repo and open http://localhost:7860. Note the result on T-182 via the board Inbox. Assumption until then: the Dockerfile is correct (the HF Space build will also exercise it).
