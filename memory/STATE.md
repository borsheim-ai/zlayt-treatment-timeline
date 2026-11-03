# STATE (orchestrator only)
Updated: 2026-11-03

## Milestones
M0 to M5 done (tags m0 to m5). Board 100% done; 8 cards wait in the needs_chris lane by design.

## What Chris hands Zlayt (D-074)
Published 2026-11-03 as the PRIVATE repo https://github.com/borsheim-ai/zlayt-treatment-timeline (2 commits: snapshot 3218c1a + link update cde4f11). Updates: rebuild the snapshot, rsync into the published clone, commit as Chris, push (no force). The running demo plus the **public snapshot** repo, built with `bash deploy/make_public_snapshot.sh` (needs the local, gitignored `deploy/.private_patterns`). Never this working repo or its history: it still holds private values in docs/CONTRACT.md, docs/RUNBOOK.md and submission/NEEDS_CHRIS.md (privacy gate, `reviews/FINAL-privacy-recheck.md`). README.md is the front door.

## Final state of the product
- Guided 4-step UI (D-068): Your cases -> Add records -> Check the timeline -> Check the bills -> Get your letter. Meets the "grandma" bar on desktop and phone (UX r3, GATE-M3M4 UX pass).
- Validation ladder shown and explained in the app (D-074, T-211): every item shows code check, second AI check (judge) and your decision; "How each answer is checked" page on every screen.
- Letter: every charge line prints "date of service [__________] (record dated X)" (D-073; SCOPE_CUTS 28). Total line "Billed charges accepted from these records".
- Suite at 43ce6eb: unit 5945 / e2e 614 passed, 0 failed; letter_check 0; spec check true (artifacts/gate-M3M4-suite-final.txt).
- Hiring panel: 4-5 on every row; "lean hire, need more evidence" (the One story T-189 and the stretch reason T-191 are Chris's).

## Needs Chris (submission/NEEDS_CHRIS.md)
T-189 One story of a miss · T-191 stretch-items reason · T-190 [CHRIS] placeholders and links · T-192 area-6 stance · T-193 prompt-log personal content (default redacted) · T-019 API key · T-022 public link · T-023 eval budget · Docker run (T-182 debt).

## Next 3 actions (if Chris re-opens work)
1. Fill T-189 and T-191 in submission/part2-process.md and product-note.md; re-render PDFs (submission/build_pdfs.sh).
2. Rebuild the snapshot after any edit (`bash deploy/make_public_snapshot.sh`), then publish only it.
3. Post-MVP backlog = SCOPE_CUTS rows 22-29 (date recognition, library recall, held M3 polish).
