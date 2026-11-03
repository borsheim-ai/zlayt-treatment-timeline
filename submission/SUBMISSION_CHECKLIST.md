# Submission checklist

Mirrors Appendix A of the Zlayt brief (`docs/CONTRACT.md`, Appendix A; standalone copy in `spec/SPEC.md`). Per D-074 (`memory/ORCHESTRATOR_DECISIONS.md`) Chris hands Zlayt the running demo and the repo; `README.md` is the place to start, and this packet is linked from it. All paths are relative to the repo root.

Status: **final** = in the repo and checked; **pending** = not final yet, with the card that owns it. Nothing marked pending is hidden from the reader.

## 1. Submitting: the five items

| # | Appendix A item | Status | Where it lives |
|---|---|---|---|
| 1 | Part 1: prototype link or repo with run instructions | **pending**: public demo link needs Chris's answer (T-022); the run path from a fresh clone is final and the README front door is written (T-212) | Run: [`README.md`](../README.md) (two commands, 3-minute walk). Code: [`app/`](../app/). Timed clean-clone install: [`deploy/TIMING.md`](../deploy/TIMING.md). Hosting options: [`deploy/HUGGINGFACE.md`](../deploy/HUGGINGFACE.md), [`deploy/REPLIT.md`](../deploy/REPLIT.md). Repo: https://github.com/borsheim-ai/zlayt-treatment-timeline (private until Chris grants Zlayt read access). It is built from a snapshot, never this working repo: [`deploy/SNAPSHOT.md`](../deploy/SNAPSHOT.md) (T-194, T-195) |
| 2 | Part 1: demo video (3 min or less) or annotated screenshots | **final** (T-184): a 174 s recording on the sample case and 72 annotated screenshots, with captions burned into the video, and the snapshot allow-list keeps the video and the screenshots (T-217). Voice-over is optional for Chris | Video: [`artifacts/demo.webm`](../artifacts/demo.webm). Screenshots: [`artifacts/screenshots/final/`](../artifacts/screenshots/final/). Captions: [`artifacts/CAPTIONS.md`](../artifacts/CAPTIONS.md). Narration script: [`artifacts/NARRATION.md`](../artifacts/NARRATION.md) |
| 3 | Part 1: one-page product note | **final** wording; the ladder display (T-211) and the D-073 date-of-service blank are stated as built. Ship-bar row 5 test counts are filled at 43ce6eb (`artifacts/gate-M3M4-suite-final.txt`). Two `[CHRIS: ...]` placeholders (name, link) and one reason (T-191) are Chris's | [`submission/product-note.md`](product-note.md), PDF [`submission/product-note.pdf`](product-note.pdf) |
| 4 | Part 1: prompt and conversation log | **final** (T-187, commit d8126e2: 773 transcripts); the final privacy sweep passed (`reviews/GATE-M4-summary.md`). What may be shown is Chris's call (T-193) | [`submission/prompt-log/`](prompt-log/): start with [`README.md`](prompt-log/README.md) (reading guide) and [`TOOLS.md`](prompt-log/TOOLS.md) (which AI tools). Transcripts: [`transcripts/`](prompt-log/transcripts/). Board log: [`board-activity.jsonl`](prompt-log/board-activity.jsonl). Reviews: [`reviews/`](prompt-log/reviews/). Decisions and lessons: [`decisions-and-lessons/`](prompt-log/decisions-and-lessons/). The brief: [`CONTRACT.md`](prompt-log/CONTRACT.md). What was redacted: [`REDACTIONS.md`](prompt-log/REDACTIONS.md) |
| 5 | Part 2: written document (4 pages or fewer) with a visual, covering all eight areas | **final** wording; Chris's "one story" is a marked block he writes (T-189); optional examples marked `[CHRIS: optional ...]` (T-190) | [`submission/part2-process.md`](part2-process.md), PDF [`submission/part2-process.pdf`](part2-process.pdf). Visual: [`submission/validation-ladder.svg`](validation-ladder.svg) (also in the PDF) plus the ship-bar table in area 4 |

Also in the packet: this checklist, [`submission/email-draft.md`](email-draft.md), [`submission/NEEDS_CHRIS.md`](NEEDS_CHRIS.md), [`submission/build_pdfs.sh`](build_pdfs.sh) (re-renders both PDFs after Chris fills his placeholders).

## 2. Part 1 must-haves, and where each lives

Requirements with pass conditions: [`spec/REQUIREMENTS.md`](../spec/REQUIREMENTS.md) section 1. Sample records: [`evals/golden/sample.txt`](../evals/golden/sample.txt); truths: [`spec/SAMPLE_CASE_TRUTHS.md`](../spec/SAMPLE_CASE_TRUTHS.md).

| Must have | Status | Code | Check |
|---|---|---|---|
| Input: paste or upload text | final | [`app/backend/ingest.py`](../app/backend/ingest.py), [`app/frontend/guided/`](../app/frontend/guided/) | [`tests/unit/`](../tests/unit/), [`tests/e2e/guided/`](../tests/e2e/guided/) |
| Timeline: date, provider, one-line summary, exact source excerpt | final | [`app/backend/generator.py`](../app/backend/generator.py), [`app/backend/grounding.py`](../app/backend/grounding.py), [`app/backend/dates.py`](../app/backend/dates.py) | Grounding 1.000 in [`evals/reports/20261102T164038Z.md`](../evals/reports/20261102T164038Z.md) |
| Review flags: gaps over 30 days, conflicts, prior conditions, causation language | final | [`app/backend/gaps.py`](../app/backend/gaps.py), [`app/backend/conflicts.py`](../app/backend/conflicts.py), [`app/backend/flags.py`](../app/backend/flags.py), phrase list [`app/llm/lexicon.yaml`](../app/llm/lexicon.yaml) | Same report: 28-day interval not flagged, 73-day gap flagged |
| Billed charges: every amount with source, running total, unclear stays unclear | final | [`app/backend/money.py`](../app/backend/money.py), [`app/backend/amounts.py`](../app/backend/amounts.py), [`app/backend/totals.py`](../app/backend/totals.py) | Sample total $8,390.00; the $185 rate is never totaled (golden `must_not`) |
| Review step: accept, edit or dismiss each entry and flag | final | [`app/backend/review.py`](../app/backend/review.py), [`app/frontend/guided/review.js`](../app/frontend/guided/review.js) | [`tests/e2e/guided/`](../tests/e2e/guided/) |
| Export: copy-ready treatment text, only what she accepted | final | [`app/backend/export.py`](../app/backend/export.py) | Byte-exact template [`evals/golden/sample.export.expected.txt`](../evals/golden/sample.export.expected.txt) (the spec copy matches it: T-215, done); [`evals/letter_check.py`](../evals/letter_check.py) |
| Stretch (at most one): side-by-side source viewer | final, but see the note in the product note: three stretch items shipped, not one | [`app/frontend/sidebyside.js`](../app/frontend/sidebyside.js), [`app/backend/pdf_text.py`](../app/backend/pdf_text.py), [`app/backend/confidence.py`](../app/backend/confidence.py) | Reason is Chris's to write (T-191) |
| Guided four-step screen; the second AI check and the human decision shown on each item, and a "How each answer is checked" page | guided screen **final** (T-181); the ladder display is built (T-211, committed; gate fixes T-216 done) | [`app/frontend/guided/`](../app/frontend/guided/) | T-181 reviews: [`submission/prompt-log/reviews/T-181-ux-designer-r3.md`](prompt-log/reviews/T-181-ux-designer-r3.md), [`submission/prompt-log/reviews/T-181-paralegal-r2.md`](prompt-log/reviews/T-181-paralegal-r2.md) |

## 3. Part 1 constraints

| Constraint | Status | Where |
|---|---|---|
| Uses an LLM for at least one step; the line between model and code is explained | final | [`docs/LLM_VS_CODE.md`](../docs/LLM_VS_CODE.md) (graded table); prompts: [`app/llm/prompts/`](../app/llm/prompts/); the second check: [`app/backend/judges.py`](../app/backend/judges.py); the human step: [`app/backend/review.py`](../app/backend/review.py) |
| Nothing in the output that is not in the records | final | [`app/backend/grounding.py`](../app/backend/grounding.py); eval gates in [`evals/run.py`](../evals/run.py); 40 of 40 seeded wrong summaries caught by the code check and judge together (code alone 31, the judge the other 9) |
| Runs from a link or a repo in under 5 minutes | final for the repo path (17 s measured); link **pending** (T-022) | [`README.md`](../README.md), [`deploy/TIMING.md`](../deploy/TIMING.md) |
| Time-boxed, with cuts stated | final | [`memory/SCOPE_CUTS.md`](../memory/SCOPE_CUTS.md) (every cut, with reason and cost); summary in the product note |

## 4. Ground rules

| Rule | Status | Where |
|---|---|---|
| Tell them which AI tools were used | final | [`submission/prompt-log/TOOLS.md`](prompt-log/TOOLS.md); product note header |
| Keep the prompts | final (T-187, d8126e2); privacy sweep passed | [`submission/prompt-log/`](prompt-log/) |
| Synthetic data only | final | The app shows a "synthetic data only" banner. Data: [`evals/golden/`](../evals/golden/), [`evals/library/`](../evals/library/); privacy review: [`submission/prompt-log/reviews/`](prompt-log/reviews/) (`GATE-M2-privacy-compliance.md`) |
| State assumptions about how PI firms work | final | [`memory/ASSUMPTIONS.md`](../memory/ASSUMPTIONS.md) (A-101 to A-109, each with "what changes if wrong" and "how to check"); cited in both documents |

## 5. Part 1 note: required contents

| Brief asks for | Section in [`product-note.md`](product-note.md) |
|---|---|
| Problem and user | Problem and user |
| What was built | What I built |
| What was cut and why | Cut |
| "Good enough to ship": 3 to 5 testable criteria, how tested, what was found | Good enough to ship (five criteria, live run); What testing found |
| Where the AI can fail or mislead, and how the design handles it | How the AI can mislead her |
| Model versus ordinary code | LLM and code (full table: [`docs/LLM_VS_CODE.md`](../docs/LLM_VS_CODE.md)) |
| Three post-launch metrics, and what each tells you | Three metrics after launch |

## 6. Part 2: the eight areas and the story

| Area | Section in [`part2-process.md`](part2-process.md) | Evidence in the repo |
|---|---|---|
| 1. Discovery (first three questions each for the lead and a paralegal) | 1 | [`personas/`](../personas/), [`memory/ASSUMPTIONS.md`](../memory/ASSUMPTIONS.md) |
| 2. Prioritization | 2 | [`spec/REQUIREMENTS.md`](../spec/REQUIREMENTS.md) |
| 3. Spec (three acceptance criteria incl. one "must never") | 3 | [`spec/REQUIREMENTS.md`](../spec/REQUIREMENTS.md), [`memory/contracts/api.md`](../memory/contracts/api.md) |
| 4. Quality bar | 4 | [`evals/`](../evals/), [`evals/reports/`](../evals/reports/) |
| 5. Ship and learn (adoption, time saved, quality, retention) | 5 | Metric definitions in the note and the audit log in [`app/backend/store.py`](../app/backend/store.py) |
| 6. Operating rhythm and fast decisions | 6 | [`memory/ORCHESTRATOR_DECISIONS.md`](../memory/ORCHESTRATOR_DECISIONS.md), [`submission/NEEDS_CHRIS.md`](NEEDS_CHRIS.md) |
| 7. Communicating with the team (sample message and agenda) | 7 | Paralegal message, find-the-error ask, agenda and a Friday founder page are in the section; lawyer messages in 1 and 5, developer card and blocker message in 8 |
| 8. Supervising developers | 8 | [`board/`](../board/), [`submission/prompt-log/reviews/`](prompt-log/reviews/), [`memory/LESSONS.md`](../memory/LESSONS.md) |
| One story: a miss | last section; **Chris writes it** (T-189) | Marked `[CHRIS: ...]` block with a suggested shape |
| Visual of the process | final | [`submission/validation-ladder.svg`](validation-ladder.svg) |

## 7. Pending, in one list

| Card | Owner | What is pending |
|---|---|---|
| T-187 | qa | Done. Final prompt-log build (d8126e2); the final privacy sweep passed and M4 closed (`reviews/GATE-M4-summary.md`) |
| T-194 | release | Snapshot pushed as one commit to the private repo (T-195). Pending: Zlayt read access (Chris, `NEEDS_CHRIS.md` #6) |
| T-215, T-216, T-217 | backend, frontend, qa | Done. The M3+M4 gate passed in round 2 (`reviews/GATE-M3-summary.md`); the suite is 0 failed (`artifacts/gate-M3M4-suite-final.txt`) |
| Gate suite | qa | Done: unit and e2e re-run at 43ce6eb; the counts in ship-bar row 5 are filled (`artifacts/gate-M3M4-suite-final.txt`; `artifacts/gate-M3M4-suite-f6d5c19.txt` is the earlier red run) |
| Chris | | `NEEDS_CHRIS.md`: T-189 (the story), T-190 (name, link), T-022 (demo link), T-193, T-191, T-192, T-019, T-023 |
