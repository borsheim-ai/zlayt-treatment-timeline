# Subagent: Writer: Part 2 ethics fixes (Writer: Part 2 ethics fixes)

Source: `agent-a61bb1c0c28b17835.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T21:34:59.718Z

You are the writer in /Users/arsis/zlayt-pm-project on T-219, round 2. Claim it with --force. Read reviews/T-219-litigation-lead.md and its evidence: artifacts/review-evidence/T-219-op705.html and T-219-r105.html. Keep Chris's casual-professional voice and the 4-page limit.

**Blockers:**
1. **Paralegal sessions and closed matters.** The responsible attorney approves which closed matter is used before any session. Prefer synthetic or redacted copies. Say plainly that Texas Rule 1.05 confidentiality covers former clients too, so "I won't copy anything" isn't the only protection. Name the actual controls: attorney approval, Zinda's environment only, nothing leaves, and access is logged.
2. **Go/no-go message.** Under Texas Opinion 705, the lawyer must always verify the accuracy of AI output. Don't say that reading the internal notes is the verification. Say the paralegal checks each line against its quote and the attorney reviews before signing, and the tool makes that check fast but never replaces it.
3. **Library recall in the go/no-go.** It must state the below-bar recall (entries 0.775, amounts 0.681; evals/reports/library-latest.md) and what that means. The pilot runs as a stage-0 shadow first, and live use waits until recall on Zinda's own test set meets the bar. This must match what the product note says.

**Majors:**
- **Kill line.** Zero unsupported facts may reach a carrier. One is a stop.
- **Confidentiality for live matters and the test set.** Add the AI vendor's terms (no training on data, retention, BAA if needed) and client consent or engagement-letter disclosure where required. The responsible attorney, not the founders, decides on using real client data.

Keep the tone notes the reviewer liked. Re-check against the product note for consistency. A PM review may arrive with more items; fold them in if I send them. Re-render the PDF at 4 pages or fewer. Commit submission/ only, staging with a temp index and committing with `git commit`. Move the card to in_review and reply in 2 lines.

### User / tool · 2026-11-03T21:34:59.724Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:02.071Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-219 --agent writer --force; python3 tools/board.py show T-219 | head -80; ls submission/; cat .claude/agent-memory/writer/submission_pipeline.md",
 "description": "Claim card and show details"
}
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:02.246Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-219-litigation-lead.md"
}
````

### User / tool · 2026-11-03T21:35:02.271Z

**tool result**
````
T-219 claimed by writer
---
id: "T-219"
title: "Part 2 voice + people pass: casual-professional first person (Chris's voice), every people question answered with the actual words (lawyer, paralegal, developer, founder), stale lines fixed, <=4 pages"
milestone: "M5"
role: "writer"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T21:22:26Z"
updated_at: "2026-11-03T21:35:02Z"
claimed_by: "writer"
claimed_at: "2026-11-03T21:35:02Z"
rounds: 1
commits: ["7544137"]
reviews:
  - {"persona": "litigation-lead-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-219-litigation-lead.md", "at": "2026-11-03T21:34:51Z"}
ac:
  - {"n": 1, "text": "all 8 areas still covered; area 1 has 3 questions for the litigation lead and 3 for a paralegal; at least one real message/script each to a litigation lead or attorney, a paralegal, a developer, and founders; no stale status lines; [CHRIS] placeholders only for his own past facts; PDF <=4 pages; every number traces to a committed file", "done": true, "evidence": "submission/part2-process.md at 7544137: 8 areas in brief order; area 1 three questions each for lead and paralegal; messages: kickoff to lead (1), go/no-go to signing attorney (5), paralegal message + find-the-error + agenda (7), T-202 card + D-073 blocker message (8), founder one-line decision with default (6) and Friday page (7); trade table D-073/D-059/D-067/D-068/D-075; stale M4-pending and NEEDS_CHRIS #10 fixed; 6 [CHRIS] markers, Chris-past only (+ stance, name); build_pdfs.sh -> 4 pages; counts re-run with count_at.sh at 7471739; all cited paths in git ls-files"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T21:22:43Z writer: claimed
- 2026-11-03T21:25:52Z writer: Facts re-checked at 7471739 (count_at.sh: 565 reviews, 27 reports, 75 decisions, 56 lessons, 65 debt, 13 personas, 62 reqs; ship bar 20261102T164038Z; suite 43ce6eb 5945/614; library 34/42 from library-latest). Voice taken from Chris's 13 chat turns in session-6ddf8076-orchestrator.md. Stale: line 114 M4 pending (M4/M5 passed d84ed8b), NEEDS_CHRIS #10 should be #11 (T-192). Drafting rewrite.
- 2026-11-03T21:30:46Z writer: AC 1 checked: submission/part2-process.md at 7544137: 8 areas in brief order; area 1 three questions each for lead and paralegal; messages: kickoff to lead (1), go/no-go to signing attorney (5), paralegal message + find-the-error + agenda (7), T-202 card + D-073 blocker message (8), founder one-line decision with default (6) and Friday page (7); trade table D-073/D-059/D-067/D-068/D-075; stale M4-pending and NEEDS_CHRIS #10 fixed; 6 [CHRIS] markers, Chris-past only (+ stance, name); build_pdfs.sh -> 4 pages; counts re-run with count_at.sh at 7471739; all cited paths in git ls-files
- 2026-11-03T21:30:46Z writer: moved in_progress -> in_review
- 2026-11-03T21:31:00Z orchestrator: review dispatched: product-manager-reviewer, litigation-lead-reviewer
- 2026-11-03T21:34:51Z orchestrator: review litigation-lead-reviewer (claude-opus-5-5): fail — reviews/T-219-litigation-lead.md; round 1; findings:
    - [blocker] Paralegal sessions expose former-client files to an outside PM without attorney approval; 'I won't copy anything' is offered as the safeguard, and the tool has already run on a closed matter — fix: Default to de-identified or synthetic records for observation and for the find-the-error exercise. A real closed matter is used only after the responsible attorney picks and approves it,
    - [blocker] Go/no-go equates 'you read the internal notes' with 'the verification Texas Opinion 705 expects' — fix: Describe the actual supervision and stop labeling it as compliance. For example: 'Before any letter it helped with goes out, you read the internal notes and check the letter lines against their quotes, all of them at first and then a sample we agree on, the way you would check a 
    - [blocker] Go/no-go and ship-bar table report only favorable numbers; omit the below-bar library recall that the product note says blocks live use — fix: Add one bullet to :101-104, e.g. 'On unfamiliar packets it found 78% of treatment entries and 68% of charges, so she still reads every bill and the notes list bills to request.' Make the stand-in numbers either meet the bar or state that wit
    - [major] Kill threshold tolerates one unsupported fact reaching a carrier — fix: Kill if: 'one unsupported fact reaches a carrier'. Also state the response: stop the pilot, notify the signing attorney the same day, and the attorney decides whether and how to correct it with the carrier.
    - [major] Confidentiality controls for live matters and the real-work test set are incomplete; client-data decisions sit with founders, not the responsible attorney — fix: Add to :73 'model vendor terms reviewed (no training on our data, retention limits), de-identified where practical, client consent where the attorney decides it's required'. Add one line to the go/no-go: 'Live records go to 
    - [minor] No tie to Rule 4.01 or Stowers deadlines (checklist 20) — fix: One clause in area 2 or 5, e.g. 'A demand is a statement to the carrier, and on a Stowers deadline there's no second draft, so a blank beats a wrong date.' Add Stowers-deadline matters to the stage-1 watch list.
- 2026-11-03T21:34:51Z orchestrator: assigned: writer
- 2026-11-03T21:35:02Z writer: claimed

## Handoff
What changed: Part 2 rewritten first person in Chris's voice (taken from his 13 chat turns): trade-off table up front (D-073, D-059, D-067, D-068, D-075); quoted messages for lead kickoff, attorney go/no-go (Part 1 numbers stand in for shadow ones, Op. 705 supervision), paralegal ask, find-the-error, agenda, founder decision line and Friday page (marked made-up pilot numbers), T-202 card and the D-073 'dates aren't shipping' message; one 'Proof in the repo' line per area. Also fixed stale lines in SUBMISSION_CHECKLIST (privacy sweep done, 773 transcripts) and NEEDS_CHRIS row 8 (area 7 optional dropped). print.css: compact blockquote + h2 (product note unaffected, still 1 page). How verified: bash submission/build_pdfs.sh -> part2 4 pages, product note 1; count_at.sh 7471739; ship-bar numbers from evals/reports/20261102T164038Z.md; suite from artifacts/gate-M3M4-suite-final.txt; library 34/42 from library-latest.md; every cited path in git ls-files. Left: Chris's [CHRIS] items (name, 3 optional lines, area-6 stance, the miss story); public snapshot needs a rebuild to pick this up. Surprised: page fit hinged on default blockquote/h2 margins, not words (3,373 words fit once styled).

NEEDS_CHRIS.md
SUBMISSION_CHECKLIST.md
build_pdfs.sh
email-draft.md
evidence
part2-process.md
part2-process.pdf
print.css
product-note.md
product-note.pdf
prompt-log
validation-ladder.svg
---
name: submission-pipeline
description: How the product note and Part 2 doc were built and page-fitted, where each number comes from, and pitfalls
metadata:
  type: project
---

Submission docs live in `submission/`: `product-note.md` (1 page), `part2-process.md` (4 pages), `validation-ladder.svg` (hand-written; `mmdc` is not installed), `print.css` (shared print style).

**Page-fit check (no LaTeX here):** `pandoc X.md -s -o /private/tmp/.../x.html --css submission/print.css --embed-resources --resource-path=submission`, then Chrome headless `--print-to-pdf --no-pdf-header-footer`, count `/Type /Page` in the PDF. Product note fits one page only at 8.7pt (~1000 words); Part 2 fits 4 pages at 9.4pt (~2700 words). T-188 does the real PDFs; reuse print.css.

**Round 2 (after PM review fail):** render with a scratch copy of print.css plus `body{font-size:Npt}` (script pattern: pandoc --css <copy> then Chrome). Product note needed ~1050 words at 8.7pt; table column widths (dash counts) and orphan last lines matter more than words. Cite only paths `git ls-files` knows: reviews are tracked at `submission/prompt-log/reviews/`, not `reviews/`. Run a backtick-path existence check before handoff. Unit count: `git archive HEAD` into scratch, symlink `.venv`, pytest (about 6 min), save under `artifacts/unit-count-<sha>.txt`; a count is valid only for its commit. Library recall: committed `evals/reports/library-latest.md` (a74b727) gives entries 0.775, amounts 0.681, flags 0.81; the PM reviewer's d0b04bc run (untracked evidence) gave amounts 0.580 — flag the mismatch, don't pick silently. Never present T-181/T-179 as built until committed.

**Pitfalls:** pandoc needs a blank line before bullet/numbered lists after a bold lead-in; table column widths follow the dash counts in the separator row; a nested `**` inside a blockquote broke the miss-story block. The git-guard refuses `git add && git commit` in one command: stage, then commit with a pathspec in a second call.

**Number sources (re-check before final, they move):** live ship bar `evals/reports/20261102T164038Z.md`; unit 5698 / e2e 412 `evals/reports/m3-sensors.md`; library 34/42 = 0.81 from `reviews/GATE-M3-product-manager.md` (committed `library-latest.md` was stale); billing rounds `reviews/T-140-claims-adjuster*.md`; verify_quickly 4 `reviews/GATE-M3-paralegal.md` (old screen, persona, not a real paralegal).

**Honesty rules held:** no Chris-past facts beyond Appendix B; thresholds in Part 2 (30% time, 60% adoption) are labeled "my starting numbers"; fixes still in flight (T-177, T-179, T-181 guided UI) worded as in progress, so refresh them when those cards close.

**T-188 (final package) additions:** `bash submission/build_pdfs.sh` renders both PDFs (pandoc + Chrome headless, print.css plus a per-doc body size; reports page counts with pdfinfo). Product note fit one page only after tuning table dash widths (13:27) and cutting ~150 words; a blank line before a list is required or it collapses into a paragraph. Part 2's re-runnable counts moved into `submission/evidence/count_at.sh <sha>` (saved 5 footer lines); unit count evidence is `submission/evidence/unit-count-<sha>.txt` (git archive + linked .venv, ~7 min, 6815 passed at 9655f1d). The `validation-ladder.svg` carries status wording too (it was stale), so grep the svg when cards close. D-074: Chris hands Zlayt the demo + repo, README first (release owns README); email draft is a reply with `[CHRIS: ...]` links. Commit recipe: temp `GIT_INDEX_FILE`, `read-tree HEAD`, `git add` explicit paths, then `git commit -- <paths>` in a second call; afterwards `git reset -q -- submission` (no HEAD arg) to resync the shared index. `board.py claim` refuses when a dependency (T-187) is unfinished; used `--force` with a note because the brief said so.

**Repo link (private repo, 836a293):** `borsheim-ai/zlayt-treatment-timeline` is private, one commit on `main` (checked with `gh api`). The email's `**Repo:**` line and checklist row 1 carry the URL; NEEDS_CHRIS #6 is Zlayt's read access. Product note and Part 2 had no repo placeholder, so their PDFs were not re-rendered. Pitfall: the shared index can hold staged submission prose that is not in HEAD or the worktree (seen at a3b7309 for product-note, part2, checklist); a temp-index commit from HEAD leaves it staged, so check `git diff --cached HEAD -- submission/` before assuming the worktree is what gets published.

**T-218 (final suite counts, D-075):** when test counts are filled, grep `pending` across `submission/*.md` (product-note ship-bar row 5, Part 2 "Before release", checklist rows 3 and gate-suite row); all four went stale at once. The snapshot allow-list (`deploy/`, T-217) keeps `artifacts/demo.webm` and `artifacts/screenshots/final/` but NOT `artifacts/demo.vtt`, so do not link the .vtt from submission docs. Commit recipe reminder: git-guard rejects stage and commit in one Bash call; split them.

**T-219 (voice + people pass, 7544137):** Chris's voice source = his ~13 user turns in `submission/prompt-log/transcripts/session-6ddf8076-orchestrator.md` (split on `### User ·`, skip task-notifications): blunt, short, imperative ("Figure it out", "Looks good, get that shipped"). Part 2 now: trade table up front, quoted messages per person, one `*Proof in the repo:*` line per area, count note moved into the opener. Page fit: unstyled blockquotes (40px margins) and default h2 cost a full page; print.css now has compact `blockquote` and `h2` rules (product note has neither, unaffected). `blockquote{break-inside:avoid}` pushes Part 2 to 5 pages, don't add it. SVG `{width=%}` barely changes page fit. Illustrative future numbers (Friday page) must be labeled made-up; the attorney go/no-go uses Part 1 numbers labeled as stand-ins. T-140 adjuster: 3 fails + 1 changes, so say "three rounds running", billing "four adversarial rounds". NEEDS_CHRIS area-6 stance is row #11 (T-192), not #10. git-guard rejects `$(...)` in command position: write lists to a scratch file and loop in python.
````

### User / tool · 2026-11-03T21:35:02.279Z

**tool result**
````
1	# T-219 — litigation-lead review (Part 2 rewrite, commit 7544137)
2	
3	Reviewer: litigation-lead-reviewer (Bob Kessler, fictional plaintiff PI partner who signs the demands), fresh context, model claude-opus-5-5.
4	
5	**Verdict: fail.** The voice is right, the questions to me are good ones, and the go/no-go shows real understanding of what a wrong line costs with an adjuster. Three things would still stop me trusting this PM with my matters.
6	
7	1. The paralegal sessions have a paralegal pick a former client's file and show it to an outside PM, and the PM brings a chronology "from a closed matter" that his tool produced. All of this happens before anyone at the firm approves it, and "I won't copy or record anything" is offered as the confidentiality safeguard. Texas Rule 1.05(b)(1) applies to former clients too and has no "nothing was copied" exception.
8	2. The go/no-go says my reading the internal notes "is the verification Texas Opinion 705 expects." That is narrower than what 705 says.
9	3. The go/no-go asks for live matters but reports only the good numbers. It leaves out library recall (entries 0.775, amounts 0.681), which is the same figure the product note gives as the reason not to go live.
10	
11	**What I exercised (commands run and their output):**
12	- `git log --oneline -5` → HEAD `7544137 docs(writer): T-219 Part 2 in Chris's voice ...`; `git diff --stat 7544137 HEAD -- submission/part2-process.md` → empty (the file under review matches HEAD).
13	- `git show 7544137:submission/part2-process.md | cat -n`: read all 190 lines as the lawyer receiving these messages.
14	- `python3 tools/board.py show T-219`: AC, handoff, writer notes.
15	- `submission/product-note.md` (to check consistency with the ship call); `evals/reports/library-latest.md` (library recall per packet, plus 7 amount-type must_not hits at a74b727, pre-billing redesign); `evals/library/*.expected.json` (what each must_not hit was: all `amount_value`, none diagnosis or causation).
16	- Primary sources fetched with curl into `artifacts/review-evidence/T-219-op705.html` and `T-219-r105.html`: Texas Op. 705 ("a lawyer should always verify the accuracy of any responses received from a generative AI tool"; "Cf. Rule 5.03"; Op. 680 precautions including reviewing "terms of service"; "may need to secure client consent") and Texas Rule 1.05(b)(1) ("Reveal confidential information of a client or a former client to ... anyone else, other than the client, the clients representatives, or the members, associates, or employees of the lawyers law firm"), (c)(1)–(2).
17	- `personas/litigation-lead.md` (checklist items 13, 14, 15, 20) and my memory file `feedback_texas_law_checks.md`.
18	
19	**Out of my lens:** page count and PDF layout, PM-craft structure, and the engineering sections (area 8), except where they make a claim to a lawyer.
20	
21	```json
22	{"card": "T-219", "persona": "litigation-lead-reviewer", "model": "claude-opus-5-5",
23	 "scope": "submission/part2-process.md at commit 7544137 (identical to HEAD); cross-checked against submission/product-note.md and evals/reports/library-latest.md; no app run (document review)",
24	 "exercised": [
25	   "git log --oneline -5 -> 7544137 at HEAD; git diff --stat 7544137 HEAD -- submission/part2-process.md -> no diff",
26	   "git show 7544137:submission/part2-process.md | cat -n (full read, 190 lines)",
27	   "python3 tools/board.py show T-219 (AC, handoff)",
28	   "read submission/product-note.md lines 1-45 (ship call: shadow, not live matters, until library recall meets bar)",
29	   "read evals/reports/library-latest.md and evals/library/*.expected.json (7 must_not hits, all amount_value)",
30	   "curl Texas Op. 705 -> artifacts/review-evidence/T-219-op705.html; curl Texas Rule 1.05 -> artifacts/review-evidence/T-219-r105.html; extracted verify / Cf. 5.03 / terms of service / client consent / 1.05(b)(1),(c) text",
31	   "grep of part2 at 7544137 for closed matter, client data, Opinion 705, 0.775, 0.681, 4.01, Stowers"
32	 ],
33	 "verdict": "fail",
34	 "scores": {"kickoff_and_questions_for_lead": 4, "go_no_go_supervision_and_ethics": 2, "paralegal_engagement": 4, "client_data_protection": 1, "tone": 5, "trust_with_my_matters": 2},
35	 "findings": [
36	  {"severity": "blocker",
37	   "title": "Paralegal sessions expose former-client files to an outside PM without attorney approval; 'I won't copy anything' is offered as the safeguard, and the tool has already run on a closed matter",
38	   "evidence": "part2-process.md:37 heading '**Watching real work without client data.**' followed by 'She works on her own machine on a closed matter. I watch, copy nothing, record nothing. If the firm wants more distance, she redoes a closed matter from a redacted copy'; :145 to a paralegal: 'Pick a closed matter and build it the way you normally do while I watch. I won't copy or record anything.'; :149 'This one's from a closed matter. I planted five mistakes in it, mixed in with whatever the tool got wrong on its own.'; :151 'that no client data leaves your machine'. Compare :73, where the test set requires 'the attorney approves them', and :131, which asks whether the tool may run on closed matters at all. Texas R. 1.05(b)(1): a lawyer shall not knowingly 'Reveal confidential information of a client or a former client to ... anyone else, other than the client, the clients representatives, or the members, associates, or employees of the lawyers law firm' (artifacts/review-evidence/T-219-r105.html).",
39	   "why_it_matters": "A closed file is still a former client's confidential information. Showing it on screen to someone outside the firm is a disclosure whether or not anything is copied. The paralegal message lets my nonlawyer staff decide that disclosure, and the find-the-error printout means a former client's records went through the tool, and onto paper the PM carries, before the founder question at :131 was even asked. A partner who reads this asks who approved it. The doc's own heading ('without client data') contradicts its content. This misstates the confidentiality duty and the supervision duty, which makes it a blocker under this brief.",
40	   "fix": "Default to de-identified or synthetic records for observation and for the find-the-error exercise. A real closed matter is used only after the responsible attorney picks and approves it, the observer is under a written confidentiality agreement with the firm, and client consent is obtained where the attorney decides 1.05(c) requires it. Have the paralegal message say 'the matter [attorney] cleared for this' instead of 'Pick a closed matter'. Have :149 say the chronology came from a de-identified or synthetic packet, or from the attorney-approved shadow set after :131 is answered. Retitle :37 to something true, e.g. 'Watching real work, with the attorney's sign-off'.",
41	   "acceptance_test": "grep of part2 shows no instruction to a paralegal to choose a client matter. Every use of a real closed matter names attorney approval and the confidentiality agreement. No tool output from a real matter appears before the step that approves running the tool on real matters. The heading at :37 does not say 'without client data' while the text describes viewing a client file."},
42	  {"severity": "blocker",
43	   "title": "Go/no-go equates 'you read the internal notes' with 'the verification Texas Opinion 705 expects'",
44	   "evidence": "part2-process.md:106 'You read those notes before any letter it helped with goes out, as you'd check a new paralegal's work; that's the verification Texas Opinion 705 expects.' Op. 705 (artifacts/review-evidence/T-219-op705.html): 'a lawyer should always verify the accuracy of any responses received from a generative AI tool ... lawyers are responsible for the work product they submit regardless of who (or what) does the original research and drafting.'",
45	   "why_it_matters": "This is the message that tells me what I am agreeing to supervise, and it shrinks my duty to reading the warnings list. Op. 705 expects me to verify the accuracy of AI output in work product I send. My paralegals' per-line accepts are part of that under my supervision (the opinion's 'Cf. Rule 5.03' analogy), but reading the notes is not verifying the letter lines I sign. A PM who tells a signing attorney that the opinion is satisfied by less than it says loses the attorney, and it is a misstatement of the ethics duty.",
46	   "fix": "Describe the actual supervision and stop labeling it as compliance. For example: 'Before any letter it helped with goes out, you read the internal notes and check the letter lines against their quotes, all of them at first and then a sample we agree on, the way you would check a new paralegal's work. Op. 705 says you must verify AI output, not rely on it blindly. This is how we make that practical; you decide whether it's enough.'",
47	   "acceptance_test": "Line :106 no longer says reading the notes is 'the verification Op. 705 expects'. It names the attorney checking letter lines against source quotes, and it frames Op. 705 as 'verify, don't rely blindly', matching the fetched text."},
48	  {"severity": "blocker",
49	   "title": "Go/no-go and ship-bar table report only favorable numbers; omit the below-bar library recall that the product note says blocks live use",
50	   "evidence": "part2-process.md:101-103 lists grounding 242/242, 40/40 caught, 0 diagnosis/cause statements and 'The weak spot: on 15 unfamiliar packets it raised 34 of 42 warnings'. It does not mention entry recall 0.775 or amount recall 0.681 on the same 15 packets. :82 ship-bar row 'Recall | 95% of golden entries and amounts | 0.982 and 1.000' gives golden only, while the Flags row (:83) does show the library 0.81. submission/product-note.md:21: 'Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow ... not live matters, until library recall meets the bar.' evals/reports/library-latest.md: amounts 2/3, 3/7, 2/5, 5/9, 4/8, 3/5, 4/7 on seven packets.",
51	   "why_it_matters": "A go/no-go to the signing attorney has to give me the number that would make me say no. On unfamiliar records the tool found about two-thirds of the charges. That is an under-demand risk on every matter where a paralegal trusts it. The message names one weak spot and leaves out the bigger one, and it asks for live matters on numbers that the PM's own product note says do not support live matters. If I found that out after saying yes, I would not take another go/no-go from this PM at face value. It is the same reason an adjuster discounts a chronology that hides the gap.",
52	   "fix": "Add one bullet to :101-104, e.g. 'On unfamiliar packets it found 78% of treatment entries and 68% of charges, so she still reads every bill and the notes list bills to request.' Make the stand-in numbers either meet the bar or state that with Part 1's numbers the answer would be no-go. Add the library recall to the :82 row the same way :83 does for flags.",
53	   "acceptance_test": "The go/no-go message contains every ship-bar metric that misses its bar (entries, amounts, flags on library). Row :82 shows golden and library recall. The message's ask is consistent with product-note.md:21."},
54	  {"severity": "major",
55	   "title": "Kill threshold tolerates one unsupported fact reaching a carrier",
56	   "evidence": "part2-process.md:114 Output quality, Kill if: 'two unsupported facts reach a carrier'; compare :106 'One unsupported fact in a draft you review, and we pause.'",
57	   "why_it_matters": "A statement in a demand that no record supports is the bad day this whole project exists to prevent: a Rule 4.01 exposure if it is knowing, and a credibility hit that the adjuster remembers on the next file. The table reads as if the first one that reaches a carrier is tolerated. Pausing at one in a draft and killing at two at the carrier leaves the one-at-the-carrier case undefined.",
58	   "fix": "Kill if: 'one unsupported fact reaches a carrier'. Also state the response: stop the pilot, notify the signing attorney the same day, and the attorney decides whether and how to correct it with the carrier.",
59	   "acceptance_test": "Row :114 kill threshold is one fact reaching a carrier, and the doc names the same-day attorney notification."},
60	  {"severity": "major",
61	   "title": "Confidentiality controls for live matters and the real-work test set are incomplete; client-data decisions sit with founders, not the responsible attorney",
62	   "evidence": ":73 test set controls are 'the attorney approves them; they never leave Zinda's environment; access is logged', with nothing about the model vendor's terms (no training, retention), de-identification where practical, or client consent. :106 'What you're agreeing to supervise' has no word on where live client records go or on vendor terms. :125 'A founder decides: ... any real client data in any environment'. Op. 705 precautions (T-219-op705.html): 'reviewing and potentially renegotiating the \"terms of service\"', 'may need to secure client consent'.",
63	   "why_it_matters": "Stage 1 sends live client medical records to an LLM. The signing attorney is the one who has to decide that this is a permitted use of confidential information (Op. 705 / ABA 512: vendor terms, data security, consent). The go/no-go never asks him to. The decision table also routes 'real client data' to the founders. Persona checklist 14 lists these controls as the condition for an acceptable real-work test set.",
64	   "fix": "Add to :73 'model vendor terms reviewed (no training on our data, retention limits), de-identified where practical, client consent where the attorney decides it's required'. Add one line to the go/no-go: 'Live records go to [vendor] under terms you've reviewed: no training, [N]-day retention. Your call whether our engagement letters cover this.' In :125, make real client data a joint decision of the responsible attorney and a founder.",
65	   "acceptance_test": "Test-set paragraph names vendor terms, de-identification, and consent. The go/no-go names where live data goes and asks the attorney to approve it. The :125 table gives the attorney the client-data decision."},
66	  {"severity": "minor",
67	   "title": "No tie to Rule 4.01 or Stowers deadlines (checklist 20)",
68	   "evidence": "grep of part2 at 7544137 for '4.01' and 'Stowers': no matches. The carrier/adjuster framing is present (:15, :127, :171).",
69	   "why_it_matters": "The no-invention rule matters to me because these are statements to a third person (Rule 4.01) and because a time-limited demand has to be right before its deadline. Blank service dates (D-073) add paralegal time exactly when a Stowers clock is running. A PM who names that understands my calendar.",
70	   "fix": "One clause in area 2 or 5, e.g. 'A demand is a statement to the carrier, and on a Stowers deadline there's no second draft, so a blank beats a wrong date.' Add Stowers-deadline matters to the stage-1 watch list.",
71	   "acceptance_test": "Part 2 mentions statements to the carrier/Rule 4.01 and Stowers or time-limited demands at least once, accurately."},
72	  {"severity": "nit",
73	   "title": "'she' in the go/no-go is ambiguous with two paralegals",
74	   "evidence": ":103 'so she still reads the records'; :104 'for her to fill'; stage 1 is 'two paralegals' (:99, :106).",
75	   "why_it_matters": "In a message asking me to approve two people, 'she' reads as one unnamed paralegal.",
76	   "fix": "Use 'they' or 'each paralegal'.",
77	   "acceptance_test": "The go/no-go uses no unexplained 'she'."}
78	 ],
79	 "whats_right": [
80	  "The three questions for the lead (:31-33) are ones I'd answer, especially 'what did it cost? Days, or dollars off the offer?' and 'What will you never let software write in a letter?'",
81	  "Blank service dates over wrong ones, and 'warnings stay in internal notes, never with the carrier': this PM understands a wrong date costs every other line.",
82	  "Tone is right for a partner: short, direct, a clear ask with a deadline ('Yes, no, or \"yes, but\" by Thursday?'), and honest about the persona-only 4/5 (:87)."
83	 ],
84	 "questions_for_chris": [
85	  "Is Zlayt's PM treated as part of Zinda Law Group (an affiliate or retained vendor under the firm's confidentiality agreement)? If so, say it once in area 1. It changes how a lawyer reads the observation sessions, though attorney approval is still needed."
86	 ]}
87	```
88	
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:03.882Z

**tool call — Bash**
````
{
 "command": "cat -n submission/part2-process.md; echo ----; sed -n 1,45p submission/product-note.md; echo ---; cat evals/reports/library-latest.md | head -40",
 "description": "Read Part 2, product note, library report"
}
````

### User / tool · 2026-11-03T21:35:03.977Z

**tool result**
````
     1	# Part 2: from Zinda's request to a shipped, measured feature
     2	
     3	Chris [CHRIS: full name] · Zlayt AI PM project
     4	
     5	I built Part 1 with a team of AI agents working a card board I ran. Workers built; reviewer agents playing a paralegal, an adjuster, a staff engineer and others tried to break it. So most of this is how I actually worked, not theory. Receipts are in the repo: 565 review files, 27 eval reports, 75 logged decisions, 56 lessons (at 7471739; tests at 43ce6eb; `submission/evidence/count_at.sh` re-runs the counts).
     6	
     7	![The validation ladder: how anything an AI writes gets into the letter](validation-ladder.svg){width=70%}
     8	
     9	In the app, every item shows its code check, the second AI's verdict and reason, and the paralegal's decision.
    10	
    11	**What I'd trade off.** Real calls from this build. I'd make each again.
    12	
    13	| Trade | What it cost | Why |
    14	|----------|---------------|-------------------------------|
    15	| Blank service dates over wrong ones (D-073) | She types every service date from the bill | Six review rounds kept finding layouts that printed a wrong date. A wrong date gives the adjuster a reason to doubt every line. A blank can't be wrong. |
    16	| Bills accepted one charge at a time (D-059) | More clicks. No "accept all" for charges | An adjuster reviewer beat our ledger rules three rounds running. A sum of lines a person accepted one by one is the only total I can defend. |
    17	| Drafted treatment paragraph cut (D-067) | She writes the narrative herself | No eval, and its sentences carried no quotes. It comes back when both exist. |
    18	| Full redesign after I found the UI "VERY hard to use" (D-068) | Everything else stopped. One item at a time is slower for an expert than a table | A persona scored it 4/5. I used it and couldn't tell where to start or when I was done. Now: four fixed steps, one question at a time. |
    19	| Ship freeze to finish (D-075) | Polish findings went to the debt list | Serial review rounds were eating the clock. Fix only what makes the demo wrong, crash, leak or mislead. |
    20	
    21	## 1. Discovery
    22	
    23	**Who first.** The litigation lead who asked, then two or three paralegals, then the attorney who signs the demand. The lead tells me what a mistake costs; the paralegals tell me where the time goes.
    24	
    25	> Subject: Treatment chronologies, 30 minutes this week?
    26	>
    27	> [Name], thanks for the ask. Before I build anything I want to see where the time goes and what a mistake costs you. Could I get 30 minutes with you, 20 each with two paralegals who build chronologies, and one closed matter with its chronology, demand letter and the adjuster's reply? Nothing leaves your machines; I note steps, not content. A week later you get one page: what I saw, what I'd build first, how we'll know it works. Chris
    28	
    29	| First three questions for the litigation lead | First three for a paralegal |
    30	|----------------------|----------------------|
    31	| "Take the last demand letter that went out. Where did the chronology hold it up?" | "Walk me through the last chronology you built, from the first record you opened." |
    32	| "Last time an adjuster pushed back on a date or a fact, what did it cost? Days, or dollars off the offer?" | "Which entries do you always re-check against the source? Which one burned you?" |
    33	| "What will you never let software write in a letter? What would you check before you signed one it helped with?" | "When two records disagree or there's a long gap, where do you write that down, and who sees it?" |
    34	
    35	**Request versus need.** The request is "faster." The need is faster without a new way to be wrong. I ask for artifacts, not opinions, and compare what people say with what they did. Every time she opens the source to check a line, I mark it. That's the step the tool has to make cheap, not remove.
    36	
    37	**Watching real work without client data.** She works on her own machine on a closed matter. I watch, copy nothing, record nothing. If the firm wants more distance, she redoes a closed matter from a redacted copy, or we use synthetic records like Part 1. Here I had no access to Zinda's people, so I wrote nine assumptions, each with "what changes if wrong," and had 13 persona dossiers researched. A stand-in, not the real thing. [CHRIS: optional, one line on a time you watched real work without exposing customer data.]
    38	
    39	*Proof in the repo:* `memory/ASSUMPTIONS.md`, `personas/`
    40	
    41	## 2. Prioritization
    42	
    43	Chronology goes before demand drafting, deposition summaries and discovery responses:
    44	
    45	- **It's upstream.** A letter drafted on an unchecked chronology repeats its errors.
    46	- **It's checkable.** Every output line traces to a source line, so quality is measurable before anyone relies on it: a 73-day gap must flag, a 28-day one must not. Drafted prose is much harder to ground.
    47	- **Mistakes cost most here.** The lead's worry is credibility with adjusters.
    48	- **Every matter with treatment needs one.** Volume is high (to confirm: what share reach a demand).
    49	
    50	What would change my mind:
    51	
    52	- A timed baseline shows a hand-built chronology takes under an hour. Then I look elsewhere.
    53	- The lead says adjuster pushback comes from the bills, not the chronology. Billing goes first. (Billing alone took four adversarial rounds in Part 1.)
    54	- Most records arrive as scans. Then intake is the bottleneck and OCR comes first.
    55	- In the pilot, checking the tool's chronology takes as long as writing one. I stop and tell the founders.
    56	
    57	*Proof in the repo:* `submission/prompt-log/reviews/T-140-claims-adjuster-r4.md`
    58	
    59	## 3. Spec
    60	
    61	The user and assumptions (each with "if wrong"); 62 numbered requirements, each with a pass condition and the check that proves it; non-goals; a byte-exact letter template; the ship bar; and a table of what is code and what is AI. The API contract comes before any code. Every call made in review goes in the decision log, so spec and build can't drift quietly. Three acceptance criteria for the AI:
    62	
    63	| # | Acceptance criterion | Checked by |
    64	|--|-------------------|-------------|
    65	| AI-1 | Every timeline entry and every amount in the letter carries a quote that appears word for word in the input. Anything that fails goes to a "could not verify" list and is never exported. | Grounding 1.000, 242 checked |
    66	| AI-2 | Any number, side, negation or hedge in a summary must be in its quote, or the item is marked needs review with the reason. On her own edits it's a hard stop. | Unit tests. 40 planted wrong summaries, 40 caught |
    67	| AI-3 **must never** | State a diagnosis, severity or cause the record's own words don't state. Never turn "may represent degenerative change" into "degenerative" or "traumatic." Never merge two accident dates. Never total PT from "$185 per visit." | Golden "must not" rules: 0 hits. Any hit blocks the release |
    68	
    69	*Proof in the repo:* `spec/REQUIREMENTS.md`, `docs/LLM_VS_CODE.md`, `memory/contracts/api.md`
    70	
    71	## 4. Quality bar
    72	
    73	**The test set, from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes); the attorney approves them; they never leave Zinda's environment; access is logged. The senior paralegal's finished chronology is the answer key. A second paralegal marks it independently, and the attorney settles disagreements. Answers are written before any run. I tune on half and look at the other half once per release. Part 1 shows why: golden cases written next to the rules score 1.000 on flags; 15 separate library packets get 34 of 42 must-flags (0.81).
    74	
    75	**Who grades.** The paralegal marks every item right, wrong or missing; the attorney grades a sample on "would I sign this?" The AI judges get graded too, on planted wrong items: 40 of 40, 20 of 20, 12 of 12, zero false agrees.
    76	
    77	**What score means ship** (live run, 3 repeats). Ship means a supervised pilot, not unsupervised use.
    78	
    79	| Ship bar | Bar | Part 1 |
    80	|-----|------------------|------------|
    81	| Grounding | 100% of letter statements and amounts quote the input | 1.000 |
    82	| Recall | 95% of golden entries and amounts | 0.982 and 1.000 |
    83	| Flags | precision and recall 0.9 per type; 28-day interval no flag, 73-day gap flags | 1.000 golden; 0.81 recall on library packets |
    84	| No invented facts | 0 unsupported statements over 3 runs; judge catches 95% of planted wrong summaries | 0; 40 of 40 |
    85	| Reviewable | a paralegal rates "I could verify every claim quickly" 4/5 or better | 4/5, but from a persona, not a real paralegal |
    86	
    87	The last row is the honest gap. The persona gave the old screen 4/5 too, and I found it very hard to use. The ship call needs a real paralegal on the final screen.
    88	
    89	**Catching regressions.** Any change to a prompt, model, phrase list or schema reruns the eval before review. Each report records commit and prompt hashes, and a check fails if they no longer match. Every escaped bug becomes a test case.
    90	
    91	*Proof in the repo:* `evals/reports/20261102T164038Z.md`, `evals/reports/library-latest.md`, `evals/golden/`
    92	
    93	## 5. Ship and learn
    94	
    95	**Rollout.** Stage 0, shadow: she builds her chronology as usual on 5 closed matters while the tool builds its own, and we compare. Stage 1: two paralegals on live matters, attorney reviewing the internal notes. Stage 2: the whole team. A stage opens only when the one before hits its numbers. Before stage 1 the signing attorney gets this (Part 1's numbers stand in for the shadow's):
    96	
    97	> Subject: Go or no-go: two paralegals on live matters from Monday
    98	>
    99	> [Name], the shadow run is done. I'm asking for a go on stage 1.
   100	>
   101	> - Every line and amount in the letter section quotes the record word for word: 242 of 242.
   102	> - Planted wrong summaries caught by the second check: 40 of 40. Statements of a diagnosis, severity or cause the record doesn't make: 0.
   103	> - The weak spot: on 15 unfamiliar packets it raised 34 of 42 warnings she should see. It misses some, so she still reads the records.
   104	> - Service dates print as blanks for her to fill. On purpose.
   105	>
   106	> What you're agreeing to supervise: two paralegals accept, edit or dismiss every line, one at a time. Nothing goes in a letter they didn't accept. Warnings stay in internal notes, never with the carrier. You read those notes before any letter it helped with goes out, as you'd check a new paralegal's work; that's the verification Texas Opinion 705 expects. One unsupported fact in a draft you review, and we pause. Yes, no, or "yes, but" by Thursday? Chris
   107	
   108	**Feedback.** A 20-minute weekly check-in per paralegal, plus the audit log: every accept, edit and dismiss, with before and after, so I see where it was wrong without asking.
   109	
   110	| Measure | Definition | Expand if | Kill if |
   111	|----|----------|-------|-------|
   112	| Adoption | Share of demand letters whose chronology started in the tool | 60% after 20 matters | under 25% after 6 weeks of fixes |
   113	| Time saved | Median minutes, first paste to copied letter section, against her last three by hand | down 30% | down under 10% after 6 weeks |
   114	| Output quality | Errors that escaped, per 100 letter lines (found by the attorney or an adjuster); share of needs-review items accepted unchanged | 0 escaped | two unsupported facts reach a carrier |
   115	| Retention | Paralegals using it on 2+ matters in week 8, of those active in week 4 | 80% | under 50% |
   116	
   117	My starting numbers; the lead and I agree them in week 1. Then the cheapest fix that moves the weakest number. At OutSystems the AI Agent Builder reached about 80% adoption. [CHRIS: optional, one line on how you measured that adoption.]
   118	
   119	*Proof in the repo:* `app/backend/store.py` (audit log), `spec/REQUIREMENTS.md` section 7
   120	
   121	## 6. Operating rhythm and fast decisions
   122	
   123	| I decide alone, same day | I decide with the litigation lead | A founder decides |
   124	|-------|---------|---------|
   125	| Wording, queue order, which eval cases to add, bug triage, a scope cut inside a feature | Anything that changes what leaves the firm in a letter, and what counts as an error | Spend and vendors, any real client data in any environment, public exposure, expand or kill |
   126	
   127	**Engineering** decides how: stack, which model runs where inside the budget, test design, build or buy. Engineering has a "not safe to ship" veto I can't overrule; only a founder can, in writing. I decide what and when. We draw the AI-versus-code line together and write it down. Disagreements get settled by evidence first: write the test that shows who's right. Still open? The safer answer holds for anything the carrier sees. In this build a staff-engineer reviewer held one card through five review rounds before passing it, and was right to. [CHRIS: confirm or change this stance (NEEDS_CHRIS #11).]
   128	
   129	**Speed.** Every founder question is one line, with my default:
   130	
   131	> Need a yes or no by Thursday: can the shadow stage run on 5 closed Zinda matters inside the firm's environment? If I don't hear back, we shadow on synthetic records and stage 1 slips a week.
   132	
   133	I'd expect an answer in one business day, three for a vendor or spend call. No answer, and a reversible default goes ahead and gets logged. This build ran that way.
   134	
   135	**First 30 days.** Week 1: shadow three paralegals and the attorney; start the assumptions list, decision log and board. Week 2: timed baselines; pick and mark up the 20 matters. Week 3: spec and API contract signed off; first slice on the test set. Week 4: ship-bar run, shadow stage, go or no-go for stage 1.
   136	
   137	*Proof in the repo:* `memory/ORCHESTRATOR_DECISIONS.md`, `submission/NEEDS_CHRIS.md`
   138	
   139	## 7. Communicating with the team
   140	
   141	**Honest feedback from busy people.** I don't ask whether they like it. I put output in front of them and ask them to find the error. I sit with paralegals without the lead in the room; people say less in front of whoever assigns their work. And I trust what they do over what they say.
   142	
   143	> Subject: 20 minutes on one chronology?
   144	>
   145	> Hi [name], I'm building the tool that drafts treatment chronologies, and I need to hear where it's wrong, not whether it's nice. 20 minutes at your desk this week? Pick a closed matter and build it the way you normally do while I watch. I won't copy or record anything. Then you mark up one the tool made. If this week is bad, just say "not this week." Chris
   146	
   147	**The find-the-error ask**, handed over with a printed chronology:
   148	
   149	> This one's from a closed matter. I planted five mistakes in it, mixed in with whatever the tool got wrong on its own. Circle every line you wouldn't put in a letter. Ten minutes. Don't be nice.
   150	
   151	**Agenda, 30 minutes, one paralegal.** 0-3: why I'm here, and that no client data leaves your machine. 3-13: you walk me through a closed matter. 13-23: you mark the tool's chronology, lines you'd trust and lines you wouldn't, and why. 23-28: what would make you stop using it. 28-30: what I'll change, and when you'll hear back.
   152	
   153	**Unhappy, silent, or conflicting.** Unhappy: reproduce it on her own example, in the room; say what changes and by when; close the loop in writing that week. Silent: read the audit log, then ask about one specific item, never "any feedback?" Conflicting: whoever signs the letter decides what goes in it; whoever does the work decides how it flows. I tell both what I decided and why. In this build a paralegal reviewer blocked the first spec because accepted warnings would have reached the carrier. Now accepting a warning means "I've seen it," and warnings live in internal notes.
   154	
   155	**Founders, without more meetings.** One page every Friday and a decision log they can read any time. No standing meeting. An example, with made-up pilot numbers:
   156	
   157	> **Friday, pilot week 3.** Shipped: bill review on phones; 3 new eval cases from bugs. Adoption: 7 of 11 letters started in the tool. Time: median 52 min to 31. Quality: 0 escaped errors; 81% of needs-review items accepted unchanged. Retention: 2 of 2 paralegals still in. Need from you: OK to add a third paralegal Monday? Default yes. Risk: one hospital sends scans, and recall drops there.
   158	
   159	*Proof in the repo:* `memory/STATE.md`, `memory/ORCHESTRATOR_DECISIONS.md` (D-001)
   160	
   161	## 8. Supervising developers
   162	
   163	**Before they start:** spec, API contract, golden set, AI-versus-code table, non-goals, and a card per task whose acceptance criteria name the exact check. Can't say how it gets tested? Don't start. A real card, trimmed:
   164	
   165	> **T-202 (P0, backend). Letter charge lines show the date of service, not the bill's statement date.** Done when: on case_09, lib14 and lib10 the letter shows the service date or period; `evals/letter_check.py` checks every dated charge line's date against its own quote, across all 25 cases; unit and end-to-end tests pass from a clean archive of the commit. Goldens change only with a diff in the handoff.
   166	
   167	**Each week:** the board (cards by state, rounds per card), this eval report against the last, escaped bugs, review findings by severity, decisions waiting on me. Evidence, not claims: a worker's "12/12 pass" came from uncommitted files, and the committed code showed no charges panel. Now everything is verified from a clean copy of the commit.
   168	
   169	**When a review finds a blocker.** After the sixth round on T-202, this went to the backend developer:
   170	
   171	> Dates aren't shipping. Six rounds in, review still finds layouts that print a wrong date: a visit note lending its date to another visit's charge, a UB-04 period overriding a line's own date. In a demand letter a wrong date is worse than a blank. The adjuster uses it to doubt every other line, and she can't tell which to re-check. So we take the fallback: every charge line prints "date of service [__________] (record dated X)" and she fills it from the bill. Pull date extraction from the letter, keep the tests that pinned the bad patterns, log it as scope cut 28. We can't prove the rule, so it doesn't go out.
   172	
   173	What I'd change: the fallback was declared after round four. Next time it's in the card on day one.
   174	
   175	**Before release:** full unit and end-to-end suites on a clean copy of the commit (5,945 and 614 passed, 0 failed), the letter check at 0, the live eval, a timed clean-clone install, and adversarial reviewers. **Sign-off:** a reviewer in a fresh context who didn't write the work, then me. Workers never close their own cards. All six milestone gates passed, not all the first time: M3 failed round one on two blockers, and the combined M3 and M4 panel failed three of six reviewers before one fix round.
   176	
   177	**Late work, or a bug in front of users.** Late: cut scope, not checks. After three review rounds I accept the card with written debt or cut it. A bug in front of users: stop, reproduce, write the failing test, fix, record the lesson. Example: the demo labeled answers our team prepared as AI output. An over-claim; it took five review rounds to fix. [CHRIS: optional, one line on a late feature you supervised and what you cut.]
   178	
   179	**AI used:** to build, draft and red-team. **Not used:** to approve its own work, set the ship bar, draw the AI-versus-code line, talk to users, or send anything.
   180	
   181	*Proof in the repo:* `board/cards/T-202.md`, `artifacts/gate-M3M4-suite-final.txt`, `memory/LESSONS.md`
   182	
   183	## The one story: a miss
   184	
   185	> [CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
   186	>
   187	> 1. What you shipped and what you expected.
   188	> 2. What you missed, and the number or signal that showed it.
   189	> 3. One concrete change to your process: an artifact or a rule, not "communicate more."
   190	> 4. How it shows up here (hooks: the "must never" criterion; golden 1.000 vs library 0.81; the persona score).
----
# Treatment Timeline: product note

Chris [CHRIS: full name] · Zlayt PM project, Part 1 · demo: [CHRIS: public link] · synthetic data only · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`) · run: `README.md`

**Problem and user.** A Zinda litigation lead says paralegals spend hours turning records into a chronology before each demand letter, and mistakes cost credibility. The user is the paralegal; she reviews rather than trusts, so every line must be checkable. The attorney signs (A-101).

**What I built.** Paste or upload records (text or PDF). Each entry shows the AI's summary beside the verbatim quote; she accepts, edits or dismisses it. Code finds the dollar amounts; she accepts each charge. The export is two blocks that never mix (D-001): the **letter section** (accepted items only: quote, provider, date, `[Ex. __ / Bates __]`) and **internal notes, do not send** (gaps, conflicts, prior conditions, causation language, untotaled amounts). Every AI step: model drafts, code checks, second model checks, she decides. Guided four-step screen. A disputed summary needs a ticked "I compared it with the quote" (D-066). Each item shows its code check, second-check verdict and her decision (T-211).

**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts, real patient data, EHR integrations, medical or legal judgment. Cut after trying: the "patient said it" label (D-040), per-provider billing totals (D-052) and the drafted treatment paragraph (built without an eval, then cut, D-067), extracting service dates (D-073). **Stretch:** at most one; I shipped three (source viewer, PDF text layer, calibrated confidence), (D-031, D-042: reinstated cuts needing no integration or login). [CHRIS: your reason, one line.] The cost: billing took four rounds.

**Good enough to ship.** Live, 3 runs; generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md` (15 packets, a74b727, pre-billing redesign). [E] ran at 312efe6; prompts, grounding, judges unchanged since.

| # | Criterion (bar) | Result |
|-|-------------|---------------------------|
| 1 | Grounding: every exported statement and amount has a quote in the input (100%) | 1.000, 242 checked [E] |
| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (93/120; 47/69). Misses: ledgers, letters, cloned notes, Spanish, EOBs |
| 3 | Flags: precision, recall 0.9 per type; 28-day gap not flagged, 73-day flagged | golden: 1.000/1.000, four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |
| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12 [E] |
| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; unit re-run at HEAD (cd7fd27 changed only the label): 5,951 passed, 0 failed (`reviews/T-218-product-manager.md`); letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`) |

**Ship call.** Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow beside a paralegal's own chronology (Part 2, area 5), not live matters, until library recall meets the bar.

**What testing found.**

- **Reviewability passed on paper, failed in use.** A persona scored the M3 screen 4/5; I found it *very* hard to use. It is now four fixed steps (D-068); a UX reviewer passed it on desktop and a 390 px phone.
- **The 1.000 flag numbers do not generalize.** Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81 (`submission/prompt-log/reviews/GATE-M3-product-manager.md`, `memory/SCOPE_CUTS.md` rows 13, 23). Misses: conflicts code never proposes ("Left" vs "Right shoulder pain").
- **Billing took four adversarial rounds.** An adjuster reviewer outworded every word-list rule: a letter said $16,147, true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records". Date reading failed the same way; after six rounds the pre-declared fallback applies: every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (D-073, `memory/SCOPE_CUTS.md` row 28).
- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).

**How the AI can mislead her, and what the design does.**

| Failure | Design |
|-----------|----------------------|
| Changes a number, side or negation; drops a hedge | Code needs each in the quote: hard refusal on her edits, needs-review on AI text; failures go to a "could not verify" list |
| Says more than the quote | Code removes unsupported clauses; the second check (scored on seeded errors) reads the rest; a disputed one needs a ticked box (D-066) |
| Invents an amount, or obeys an order in a record | Only code finds money; she accepts each charge; models have no tools |
| Rules on cause or diagnosis | Flag wording is a code template; the model returns a category and quote only (D-007) |

**LLM and code.** Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts, totals, quote and number checks, flag wording, export. The model reads: summary and quote, flag category, one yes/no per conflict pair code proposes, where to cut an unsplit paste, and the second check. Table: `docs/LLM_VS_CODE.md`.

**Three metrics after launch.**

1. **Minutes from first paste to copied letter section, against her last three by hand.** Source: timestamps.
2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Source: attorney edit log. Target 0.
3. **Needs-review items accepted unchanged, and median seconds per item.** Source: audit log.
---
# Library report (reported, not gated)

Source commit: a74b727b1ed94befbd09c0a3da0e8556e66f787c (tree: clean). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done_with_errors | 5/6 | 2/2 | True | 1/1 | 0 | - | 0 | LLM_FAILED_AFTER_RETRIES r3 FIXTURE_MISS |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | 2/2 | 0 | M4 | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 3/7 | False | 2/2 | 0 | M3 | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 6/9 | 5/9 | False | 1/1 | 0 | M1 | 0 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 5/5 | True | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 3/5 | False | 0/0 | 0 | M2 | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 4/7 | False | 1/3 | 0 | M4 | 0 | - |

## Known honest failures (generated from the run above)

| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:42.843Z

**tool call — Bash**
````
{
 "command": "cat board/milestones.md | head -30; git log --oneline -5; git status --short submission/ | head; cat submission/build_pdfs.sh | head -40; grep -n \"privacy sweep\\|pending\" submission/*.md",
 "description": "Check milestones, git state, build script"
}
````

### User / tool · 2026-11-03T21:35:42.983Z

**tool result**
````
---
milestones:
  - {"id": "M0", "title": "Operating system (harness, board, hooks, agents)", "status": "done", "budget_h": 1.5, "started_at": "2026-11-02T00:07:00Z", "gate_result": "pass", "gate_record": "reviews/GATE-M0-summary.md", "gate_at": "2026-11-02T01:11:14Z", "done_at": "2026-11-02T01:11:14Z"}
  - {"id": "M1", "title": "Research, personas, requirements, architecture", "status": "done", "budget_h": 2.5, "started_at": "2026-11-02T00:17:08Z", "gate_result": "pass", "gate_record": "reviews/GATE-M1-summary.md", "gate_at": "2026-11-02T01:38:56Z", "done_at": "2026-11-02T01:38:56Z"}
  - {"id": "M2", "title": "Core pipeline + evals green", "status": "done", "budget_h": 3.5, "started_at": "2026-11-02T01:38:56Z", "note": "re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b)", "gate_result": "pass", "gate_record": "reviews/GATE-M2-summary.md", "gate_at": "2026-11-02T19:30:29Z", "done_at": "2026-11-02T19:30:29Z"}
  - {"id": "M3", "title": "Review UI, export, E2E", "status": "done", "budget_h": 3.5, "started_at": "2026-11-02T19:30:37Z", "note": "round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045", "gate_result": "pass", "gate_record": "reviews/GATE-M3-summary.md", "gate_at": "2026-11-03T15:18:34Z", "done_at": "2026-11-03T16:14:34Z"}
  - {"id": "M4", "title": "Hardening, deployment, demo assets", "status": "done", "budget_h": 2.0, "started_at": "2026-11-03T04:32:00Z", "gate_result": "pass", "gate_record": "reviews/GATE-M4-summary.md", "gate_at": "2026-11-03T18:58:05Z", "done_at": "2026-11-03T18:58:07Z"}
  - {"id": "M5", "title": "Submission package", "status": "done", "budget_h": 2.0, "started_at": "2026-11-03T04:32:00Z", "gate_result": "pass", "gate_record": "reviews/GATE-M5-summary.md", "gate_at": "2026-11-03T18:58:05Z", "done_at": "2026-11-03T18:58:07Z"}
---
# Milestones

Generated by `tools/board.py` — edit through `board.py milestone` / `board.py gate`.

| Milestone | Title | Status | Gate | Started | Finished | Budget (h) | Note |
|---|---|---|---|---|---|---|---|
| M0 | Operating system (harness, board, hooks, agents) | done | pass ([record](../reviews/GATE-M0-summary.md)) | 2026-11-02T00:07:00Z | 2026-11-02T01:11:14Z | 1.5 |  |
| M1 | Research, personas, requirements, architecture | done | pass ([record](../reviews/GATE-M1-summary.md)) | 2026-11-02T00:17:08Z | 2026-11-02T01:38:56Z | 2.5 |  |
| M2 | Core pipeline + evals green | done | pass ([record](../reviews/GATE-M2-summary.md)) | 2026-11-02T01:38:56Z | 2026-11-02T19:30:29Z | 3.5 | re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b) |
| M3 | Review UI, export, E2E | done | pass ([record](../reviews/GATE-M3-summary.md)) | 2026-11-02T19:30:37Z | 2026-11-03T16:14:34Z | 3.5 | round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045 |
| M4 | Hardening, deployment, demo assets | done | pass ([record](../reviews/GATE-M4-summary.md)) | 2026-11-03T04:32:00Z | 2026-11-03T18:58:07Z | 2.0 |  |
| M5 | Submission package | done | pass ([record](../reviews/GATE-M5-summary.md)) | 2026-11-03T04:32:00Z | 2026-11-03T18:58:07Z | 2.0 |  |

Definitions: see docs/CONTRACT.md §4 (M0) and §5 (M1–M5).
7544137 docs(writer): T-219 Part 2 in Chris's voice: real messages to lead, attorney, paralegal, developer, founders; trade-off table (D-073, D-059, D-067, D-068, D-075); proof lines per area; stale lines fixed; 4 pages
7471739 docs(memory): STATE records the private GitHub publish and how to update it
836a293 docs(writer): repo link to the private Zlayt repo; NEEDS_CHRIS marks snapshot push done and adds Zlayt read access
a3b7309 docs(readme): point Get the code step at the private GitHub repo
d84ed8b gate(M4,M5): pass — final privacy sweep + recheck, hiring panel verify; final STATE.md
 M submission/product-note.pdf
#!/usr/bin/env bash
# Render product-note.pdf and part2-process.pdf from the markdown with print.css.
# Needs pandoc and Google Chrome (headless). Run from anywhere: bash submission/build_pdfs.sh
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
for doc in product-note part2-process; do
  # print.css is the shared style; each document sets its own body size so it fits its page budget
  # (product note: one page; Part 2: four pages).
  size=8.6; [ "$doc" = part2-process ] && size=9.4
  cp print.css "$TMP/print-$doc.css"; echo "body{font-size:${size}pt}" >> "$TMP/print-$doc.css"; css="$TMP/print-$doc.css"
  pandoc "$doc.md" -s -o "$TMP/$doc.html" --css "$css" --embed-resources --resource-path=. --metadata title=" "
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/$doc.pdf" "file://$TMP/$doc.html" >/dev/null 2>&1
  echo "$doc.pdf: $(pdfinfo "$doc.pdf" | awk '/^Pages/{print $2}') page(s)"
done
submission/SUBMISSION_CHECKLIST.md:5:Status: **final** = in the repo and checked; **pending** = not final yet, with the card that owns it. Nothing marked pending is hidden from the reader.
submission/SUBMISSION_CHECKLIST.md:11:| 1 | Part 1: prototype link or repo with run instructions | **pending**: public demo link needs Chris's answer (T-022); the run path from a fresh clone is final and the README front door is written (T-212) | Run: [`README.md`](../README.md) (two commands, 3-minute walk). Code: [`app/`](../app/). Timed clean-clone install: [`deploy/TIMING.md`](../deploy/TIMING.md). Hosting options: [`deploy/HUGGINGFACE.md`](../deploy/HUGGINGFACE.md), [`deploy/REPLIT.md`](../deploy/REPLIT.md). Repo: https://github.com/borsheim-ai/zlayt-treatment-timeline (private until Chris grants Zlayt read access). It is built from a snapshot, never this working repo: [`deploy/SNAPSHOT.md`](../deploy/SNAPSHOT.md) (T-194, T-195) |
submission/SUBMISSION_CHECKLIST.md:14:| 4 | Part 1: prompt and conversation log | **final** (T-187, commit d8126e2: 773 transcripts); the final privacy sweep passed (`reviews/GATE-M4-summary.md`). What may be shown is Chris's call (T-193) | [`submission/prompt-log/`](prompt-log/): start with [`README.md`](prompt-log/README.md) (reading guide) and [`TOOLS.md`](prompt-log/TOOLS.md) (which AI tools). Transcripts: [`transcripts/`](prompt-log/transcripts/). Board log: [`board-activity.jsonl`](prompt-log/board-activity.jsonl). Reviews: [`reviews/`](prompt-log/reviews/). Decisions and lessons: [`decisions-and-lessons/`](prompt-log/decisions-and-lessons/). The brief: [`CONTRACT.md`](prompt-log/CONTRACT.md). What was redacted: [`REDACTIONS.md`](prompt-log/REDACTIONS.md) |
submission/SUBMISSION_CHECKLIST.md:40:| Runs from a link or a repo in under 5 minutes | final for the repo path (17 s measured); link **pending** (T-022) | [`README.md`](../README.md), [`deploy/TIMING.md`](../deploy/TIMING.md) |
submission/SUBMISSION_CHECKLIST.md:48:| Keep the prompts | final (T-187, d8126e2); privacy sweep passed | [`submission/prompt-log/`](prompt-log/) |
submission/SUBMISSION_CHECKLIST.md:81:| Card | Owner | What is pending |
submission/SUBMISSION_CHECKLIST.md:83:| T-187 | qa | Done. Final prompt-log build (d8126e2); the final privacy sweep passed and M4 closed (`reviews/GATE-M4-summary.md`) |
submission/product-note.md:28:- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:47.122Z

**tool call — Bash**
````
{
 "command": "git ls-files reviews/GATE-M4-summary.md reviews/GATE-M3-summary.md evals/reports/library-latest.md | cat; git diff --stat HEAD -- submission/; git diff --cached --stat HEAD -- submission/",
 "description": "Check tracked paths and staged state"
}
````

### User / tool · 2026-11-03T21:35:47.261Z

**tool result**
````
evals/reports/library-latest.md
reviews/GATE-M3-summary.md
reviews/GATE-M4-summary.md
 submission/product-note.pdf | Bin 113798 -> 113798 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:48.194Z

Now the Part 2 edits, area 1 first.

### Assistant · claude-opus-5-5 · 2026-11-03T21:35:54.290Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\n\nrep(\"\"\"and one closed matter with its chronology, demand letter and the adjuster's reply? Nothing leaves your machines; I note steps, not content.\"\"\",\n\"\"\"and, if the responsible attorney approves one, a redacted closed matter with its chronology, demand letter and the adjuster's reply? It stays on your systems; I note steps, not content.\"\"\")\n\nrep(\"\"\"**Watching real work without client data.** She works on her own machine on a closed matter. I watch, copy nothing, record nothing. If the firm wants more distance, she redoes a closed matter from a redacted copy, or we use synthetic records like Part 1. Here I had\"\"\",\n\"\"\"**Watching real work, with the attorney's sign-off.** A closed file is still client confidential: Texas Rule 1.05 covers former clients too, so \"I won't copy anything\" isn't the protection. The default is synthetic records, like Part 1, or a redacted copy. A real closed matter only if the responsible attorney picks and approves it first, under the firm's confidentiality agreement; it stays in Zinda's environment, nothing leaves, access is logged. Here I had\"\"\")\n\nrep(\"\"\"- **Mistakes cost most here.** The lead's worry is credibility with adjusters.\"\"\",\n\"\"\"- **Mistakes cost most here.** The lead's worry is credibility with adjusters. A demand is a statement to the carrier, and on a Stowers deadline there's no second draft.\"\"\")\n\nrep(\"\"\"the attorney approves them; they never leave Zinda's environment; access is logged.\"\"\",\n\"\"\"the responsible attorney approves them, not the founders. They never leave Zinda's environment; access is logged; de-identified where practical. The model vendor's terms are reviewed first: no training on our data, a retention limit, a BAA if needed. Client consent or an engagement-letter disclosure where the attorney decides it's required.\"\"\")\n\nrep(\"\"\"| Recall | 95% of golden entries and amounts | 0.982 and 1.000 |\"\"\",\n\"\"\"| Recall | 95% of entries and amounts | golden 0.982, 1.000; **library 0.775, 0.681** |\"\"\")\n\nopen(p,'w').write(s)\nEOF",
 "description": "Apply area 1-4 edits to Part 2"
}
````

### User / tool · 2026-11-03T21:35:54.399Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:07.171Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\n\nold_start=s.index(\"**Rollout.** Stage 0\")\nold_end=s.index(\"**Feedback.**\")\nnew='''**Rollout.** Stage 0, shadow: on 5 closed matters the attorney approves, each paralegal builds her chronology as usual while the tool builds its own, and we compare. Nothing it makes goes in a letter. Stage 1: two paralegals on live matters (none on a Stowers deadline at first), only once recall on Zinda's own test set meets the bar. Stage 2: the whole team. The go/no-go I'd send the signing attorney today, on Part 1's numbers:\n\n> Subject: Go on a shadow run, no-go on live matters yet\n>\n> [Name], where it stands and what I'm asking.\n>\n> - Every line and amount in the letter section quotes the record word for word: 242 of 242. Planted wrong summaries caught: 40 of 40. Statements of a diagnosis or cause the record doesn't make: 0.\n> - Below the bar: on 15 unfamiliar packets it found 78% of treatment entries and 68% of charges (bar: 95%), and 34 of 42 warnings. Trusted, that's missed visits and an under-stated demand. So the paralegals still read every record and every bill.\n> - Service dates print as blanks to fill. On purpose.\n>\n> So: go on a shadow on 5 closed matters you pick, inside our environment. Live matters wait until recall on our own test set meets the bar; then I ask again. Once live, the paralegals check each line against its quote before accepting it, and you check the letter lines against their quotes before you sign, all of them at first, then a sample we agree on. Texas Opinion 705 says the lawyer always verifies AI output. The tool makes that check fast; it never replaces it. Records go to [vendor] under terms you've reviewed: no training on our data, [N]-day retention. Whether our engagement letters cover that, or clients must consent, is your call. One unsupported fact in a draft and we pause. One that reaches a carrier and we stop; you hear that day, and you decide the correction. Yes, no, or \"yes, but\" by Thursday? Chris\n\n'''\ns=s[:old_start]+new+s[old_end:]\n\nrep(\"\"\"| 0 escaped | two unsupported facts reach a carrier |\"\"\",\n\"\"\"| 0 escaped | **one** unsupported fact reaches a carrier: stop, attorney told that day |\"\"\")\n\nrep(\"\"\"| Spend and vendors, any real client data in any environment, public exposure, expand or kill |\"\"\",\n\"\"\"| Spend and vendors, public exposure, expand or kill. Using real client data: the responsible attorney, never a founder |\"\"\")\n\nrep(\"\"\"> Need a yes or no by Thursday: can the shadow stage run on 5 closed Zinda matters inside the firm's environment? If I don't hear back, we shadow on synthetic records and stage 1 slips a week.\"\"\",\n\"\"\"> Need a yes or no by Thursday: OK to sign [vendor]'s no-training, short-retention terms? The attorney needs them before approving the shadow matters. If I don't hear back, we shadow on synthetic records and lose a week.\"\"\")\n\nrep(\"\"\"20 minutes at your desk this week? Pick a closed matter and build it the way you normally do while I watch. I won't copy or record anything. Then you mark up one the tool made.\"\"\",\n\"\"\"20 minutes at your desk this week? Build a chronology the way you normally do while I watch, from the redacted closed matter [attorney] cleared for this. It stays on Zinda's system. Then you mark up one the tool made.\"\"\")\n\nrep(\"\"\"> This one's from a closed matter. I planted five mistakes\"\"\",\n\"\"\"> This one's from a synthetic packet built like ours. I planted five mistakes\"\"\")\n\nrep(\"\"\"0-3: why I'm here, and that no client data leaves your machine. 3-13: you walk me through a closed matter.\"\"\",\n\"\"\"0-3: why I'm here, and which records we use (synthetic, or the matter [attorney] cleared). 3-13: you walk me through it.\"\"\")\nopen(p,'w').write(s)\nEOF\ngrep -n \"she\\b\\|her \" submission/part2-process.md | sed -n 1,40p | cut -c1-160",
 "description": "Rewrite rollout, go/no-go, kill line, area 6-7 confidentiality"
}
````

### User / tool · 2026-11-03T21:36:07.290Z

**tool result**
````
35:**Request versus need.** The request is "faster." The need is faster without a new way to be wrong. I ask for artifacts, not opinions, and compare what peopl
66:| AI-2 | Any number, side, negation or hedge in a summary must be in its quote, or the item is marked needs review with the reason. On her own edits it's a h
73:**The test set, from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes); the responsible attorney a
95:**Rollout.** Stage 0, shadow: on 5 closed matters the attorney approves, each paralegal builds her chronology as usual while the tool builds its own, and we 
105:> So: go on a shadow on 5 closed matters you pick, inside our environment. Live matters wait until recall on our own test set meets the bar; then I ask agai
112:| Time saved | Median minutes, first paste to copied letter section, against her last three by hand | down 30% | down under 10% after 6 weeks |
126:**Engineering** decides how: stack, which model runs where inside the budget, test design, build or buy. Engineering has a "not safe to ship" veto I can't o
140:**Honest feedback from busy people.** I don't ask whether they like it. I put output in front of them and ask them to find the error. I sit with paralegals 
144:> Hi [name], I'm building the tool that drafts treatment chronologies, and I need to hear where it's wrong, not whether it's nice. 20 minutes at your desk t
152:**Unhappy, silent, or conflicting.** Unhappy: reproduce it on her own example, in the room; say what changes and by when; close the loop in writing that wee
170:> Dates aren't shipping. Six rounds in, review still finds layouts that print a wrong date: a visit note lending its date to another visit's charge, a UB-04
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:14.503Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"Unhappy: reproduce it on her own example, in the room;\",\"Unhappy: reproduce it with her, in the room;\")\nrep(\"The last row is the honest gap. The persona gave\",\"Two honest gaps. Library recall is below the bar, so live use waits (area 5). And the last row: the persona gave\")\nopen(p,'w').write(s)\np='submission/product-note.md'\ns=open(p).read()\nrep(\"not live matters, until library recall meets the bar.\",\"not live matters until recall meets the bar on the library and on Zinda's own test set.\")\nrep(\"Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).\",\"Prompt log: final, e0d721d; M4 passed after the final privacy sweep (`reviews/GATE-M4-summary.md`).\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh",
 "description": "Final wording tweaks and render PDFs"
}
````

### User / tool · 2026-11-03T21:36:16.610Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:19.043Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/submission && pdftotext -f 5 -l 5 part2-process.pdf - | wc -w; pdftotext -f 5 -l 5 part2-process.pdf - | head -30; wc -w part2-process.md; git show HEAD:submission/part2-process.md | wc -w",
 "description": "Measure page 5 overflow"
}
````

### User / tool · 2026-11-03T21:36:19.178Z

**tool result**
````
      80
The one story: a miss
[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
1. What you shipped and what you expected.
2. What you missed, and the number or signal that showed it.
3. One concrete change to your process: an artifact or a rule, not “communicate more.”
4. How it shows up here (hooks: the “must never” criterion; golden 1.000 vs library 0.81; the persona score).

    3568 part2-process.md
    3371
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:31.741Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"In the app, every item shows its code check, the second AI's verdict and reason, and the paralegal's decision.\\n\\n\",\"\")\nrep(\"All six milestone gates passed, not all the first time: M3 failed round one on two blockers, and the combined M3 and M4 panel failed three of six reviewers before one fix round.\",\"All six milestone gates passed; M3 and the combined M3 and M4 panel each failed once first.\")\nrep(\"> - Every line and amount in the letter section quotes the record word for word: 242 of 242. Planted wrong summaries caught: 40 of 40. Statements of a diagnosis or cause the record doesn't make: 0.\",\n\"> - Every letter line and amount quotes the record word for word: 242 of 242. Planted wrong summaries caught: 40 of 40. Diagnoses or causes the record doesn't state: 0.\")\nrep(\"Trusted, that's missed visits and an under-stated demand. So the paralegals still read every record and every bill.\",\"Trusted, that means missed visits and an under-stated demand, so the paralegals still read every record and bill.\")\nrep(\"Shipped: bill review on phones; 3 new eval cases from bugs. \",\"Shipped: 3 new eval cases from bugs. \")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -8",
 "description": "Trim Part 2 and re-render"
}
````

### User / tool · 2026-11-03T21:36:33.576Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
cut it. A bug in front of users: stop, reproduce, write the failing test, fix, record the lesson. Example: the demo labeled answers our
team prepared as AI output. An over-claim; it took five review rounds to fix. [CHRIS: optional, one line on a late feature you
supervised and what you cut.]
AI used: to build, draft and red-team. Not used: to approve its own work, set the ship bar, draw the AI-versus-code line, talk to users,
or send anything.
Proof in the repo: board/cards/T-202.md, artifacts/gate-M3M4-suite-final.txt, memory/LESSONS.md
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:44.465Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"> - Service dates print as blanks to fill. On purpose.\\n\",\"\")\nrep(\" And I trust what they do over what they say.\",\"\")\nrep(\"Example: the demo labeled answers our team prepared as AI output. An over-claim; it took five review rounds to fix.\",\"Example: the demo labeled answers we prepared as AI output; five rounds to fix.\")\nrep(\"Week 1: shadow three paralegals and the attorney; start the assumptions list, decision log and board.\",\"Week 1: shadow three paralegals and the attorney; start assumptions, decision log and board.\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 5 part2-process.pdf - | tail -12",
 "description": "Further trims and re-render"
}
````

### User / tool · 2026-11-03T21:36:46.289Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
or send anything.
Proof in the repo: board/cards/T-202.md, artifacts/gate-M3M4-suite-final.txt, memory/LESSONS.md

The one story: a miss
[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
1. What you shipped and what you expected.

2. What you missed, and the number or signal that showed it.
3. One concrete change to your process: an artifact or a rule, not “communicate more.”
4. How it shows up here (hooks: the “must never” criterion; golden 1.000 vs library 0.81; the persona score).
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:36:53.883Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"Part 1 shows why: golden cases written next to the rules score 1.000 on flags; 15 separate library packets get 34 of 42 must-flags (0.81).\",\"Part 1 shows why: golden cases written next to the rules score 1.000 on flags; 15 unfamiliar packets, 0.81.\")\nrep(\"non-goals; a byte-exact letter template; the ship bar;\",\"non-goals; the letter template; the ship bar;\")\nrep(\"Stage 2: the whole team. The go/no-go I'd send\",\"Stage 2: the whole team. What I'd send\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -5",
 "description": "Trim and re-render again"
}
````

### User / tool · 2026-11-03T21:36:55.908Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
The one story: a miss
[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
1. What you shipped and what you expected.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:06.471Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\" (Billing alone took four adversarial rounds in Part 1.)\",\"\")\nrep(\"Shipped: 3 new eval cases from bugs. \",\"\")\nrep(\"Evidence, not claims: a worker's \\\"12/12 pass\\\" came from uncommitted files, and the committed code showed no charges panel. Now everything is verified from a clean copy of the commit.\",\"Evidence, not claims: a worker's \\\"12/12 pass\\\" came from uncommitted files, so now everything is verified from a clean copy of the commit.\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -5",
 "description": "Trim and re-render"
}
````

### User / tool · 2026-11-03T21:37:08.489Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
The one story: a miss
[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
1. What you shipped and what you expected.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:11.347Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/submission && for i in 1 2 3 4; do echo \"== p$i\"; pdftotext -layout -f $i -l $i part2-process.pdf - | grep -v '^\\s*$' | tail -3; done",
 "description": "Inspect page breaks"
}
````

### User / tool · 2026-11-03T21:37:11.509Z

**tool result**
````
== p1
Days, or dollars off the offer?”                                                                         burned you?”
“What will you never let software write in a letter? What would you check                                “When two records disagree or there’s a long gap, where do you write that
before you signed one it helped with?”                                                                   down, and who sees it?”
== p2
No invented facts      0 unsupported statements over 3 runs; judge catches 95% of planted wrong 0; 40 of 40
                       summaries
Reviewable             a paralegal rates “I could verify every claim quickly” 4/5 or better              4/5, but from a persona, not a real paralegal
== p3
baselines; pick and mark up the 20 matters. Week 3: spec and API contract signed off; first slice on the test set. Week 4: ship-bar run,
shadow stage, go or no-go for stage 1.
Proof in the repo: memory/ORCHESTRATOR_DECISIONS.md, submission/NEEDS_CHRIS.md
== p4
The one story: a miss
  [CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
   1. What you shipped and what you expected.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:16.766Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/submission && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && pdftoppm -r 40 -png part2-process.pdf $S/p2 && ls $S | grep p2",
 "description": "Render pages to PNG thumbnails"
}
````

### User / tool · 2026-11-03T21:37:17.347Z

**tool result**
````
app2
app2.log
app2.pid
app2.sqlite3
cli_rep2.err
exp2.py
p2-1.png
p2-2.png
p2-3.png
p2-4.png
p2-5.png
p2-all.png
p2.db
p2.py
p2.txt
p2b-1.png
p2b-4.png
pp2
snap2
t060p2
t060p2-wrap
t072r3-p2_be_patientstatement
tmp2.index
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:20.975Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && python3 -c \"\nfrom PIL import Image\nims=[Image.open(f'p2-{i}.png') for i in range(1,6)]\nw=sum(i.width for i in ims); h=max(i.height for i in ims)\no=Image.new('RGB',(w,h),'white'); x=0\nfor i in ims: o.paste(i,(x,0)); x+=i.width\no.save('p2-all.png')\"",
 "description": "Stitch page thumbnails"
}
````

### User / tool · 2026-11-03T21:37:21.134Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:23.744Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/p2-all.png"
}
````

### User / tool · 2026-11-03T21:37:23.753Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:35.505Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\na=\"**Each week:** the board (cards by state, rounds per card), this eval report\"\nassert s.count(a)==1\ns=s.replace(a,\"**Each week:** the board, this eval report\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -4",
 "description": "One more trim and re-render"
}
````

### User / tool · 2026-11-03T21:37:37.506Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark. About 200 words.]
1. What you shipped and what you expected.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:43.869Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\na=\" Goldens change only with a diff in the handoff.\"\nassert s.count(a)==1\ns=s.replace(a,\"\")\na=\"Late: cut scope, not checks. After three review rounds I accept the card with written debt or cut it.\"\nassert s.count(a)==1\ns=s.replace(a,\"Late: cut scope, not checks; after three review rounds, accept with written debt or cut.\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -4",
 "description": "Trim area 8 and re-render"
}
````

### User / tool · 2026-11-03T21:37:45.785Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
1. What you shipped and what you expected.
2. What you missed, and the number or signal that showed it.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:37:51.523Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"> [Name], where it stands and what I'm asking.\\n>\\n> - Every letter line\",\"> - [Name], every letter line\")\nrep(\"> So: go on a shadow on 5 closed matters\",\"> So: go on a shadow run on 5 closed matters\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -4",
 "description": "Merge go/no-go opener and re-render"
}
````

### User / tool · 2026-11-03T21:37:53.620Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 5 page(s)
2. What you missed, and the number or signal that showed it.
3. One concrete change to your process: an artifact or a rule, not “communicate more.”
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:01.221Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"> - [Name], every letter line\",\"> [Name], where it stands:\\n>\\n> - Every letter line\")\nrep(\"Volume is high (to confirm: what share reach a demand).\",\"(To confirm: what share reach a demand.)\")\nopen(p,'w').write(s)\np='submission/build_pdfs.sh'\ns=open(p).read()\nrep(\"size=9.4\",\"size=9.3\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh; cd submission && pdftotext -f 4 -l 4 part2-process.pdf - | tail -3",
 "description": "Revert opener, set 9.3pt, re-render"
}
````

### User / tool · 2026-11-03T21:38:03.236Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 4 page(s)
4. How it shows up here (hooks: the “must never” criterion; golden 1.000 vs library 0.81; the persona score).
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:08.708Z

**tool call — Bash**
````
{
 "command": "grep -n \"closed matter\\|client data\\|705\\|1\\.05\\|0\\.775\\|78%\\|Stowers\\|carrier\\|vendor\" submission/part2-process.md | cut -c1-220; sed -n 93,106p submission/part2-process.md; grep -o '`[^`]*`' submission/part2-process.md submission/product-note.md | sed 's/.*:`//;s/`$//' | sort -u > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/paths.txt",
 "description": "Consistency grep and collect cited paths"
}
````

### User / tool · 2026-11-03T21:38:08.824Z

**tool result**
````
25:> [Name], thanks for the ask. Before I build anything I want to see where the time goes and what a mistake costs you. Could I get 30 minutes with you, 20 each with two paralegals who build chronologies, and, if the re
35:**Watching real work, with the attorney's sign-off.** A closed file is still client confidential: Texas Rule 1.05 covers former clients too, so "I won't copy anything" isn't the protection. The default is synthetic re
45:- **Mistakes cost most here.** The lead's worry is credibility with adjusters. A demand is a statement to the carrier, and on a Stowers deadline there's no second draft.
71:**The test set, from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes); the responsible attorney approves them, not the founders. They never leave Zinda's env
80:| Recall | 95% of entries and amounts | golden 0.982, 1.000; **library 0.775, 0.681** |
93:**Rollout.** Stage 0, shadow: on 5 closed matters the attorney approves, each paralegal builds her chronology as usual while the tool builds its own, and we compare. Nothing it makes goes in a letter. Stage 1: two par
100:> - Below the bar: on 15 unfamiliar packets it found 78% of treatment entries and 68% of charges (bar: 95%), and 34 of 42 warnings. Trusted, that means missed visits and an under-stated demand, so the paralegals stil
102:> So: go on a shadow run on 5 closed matters you pick, inside our environment. Live matters wait until recall on our own test set meets the bar; then I ask again. Once live, the paralegals check each line against its
110:| Output quality | Errors that escaped, per 100 letter lines (found by the attorney or an adjuster); share of needs-review items accepted unchanged | 0 escaped | **one** unsupported fact reaches a carrier: stop, atto
121:| Wording, queue order, which eval cases to add, bug triage, a scope cut inside a feature | Anything that changes what leaves the firm in a letter, and what counts as an error | Spend and vendors, public exposure, ex
123:**Engineering** decides how: stack, which model runs where inside the budget, test design, build or buy. Engineering has a "not safe to ship" veto I can't overrule; only a founder can, in writing. I decide what and w
127:> Need a yes or no by Thursday: OK to sign [vendor]'s no-training, short-retention terms? The attorney needs them before approving the shadow matters. If I don't hear back, we shadow on synthetic records and lose a w
129:I'd expect an answer in one business day, three for a vendor or spend call. No answer, and a reversible default goes ahead and gets logged. This build ran that way.
141:> Hi [name], I'm building the tool that drafts treatment chronologies, and I need to hear where it's wrong, not whether it's nice. 20 minutes at your desk this week? Build a chronology the way you normally do while I
149:**Unhappy, silent, or conflicting.** Unhappy: reproduce it with her, in the room; say what changes and by when; close the loop in writing that week. Silent: read the audit log, then ask about one specific item, never
**Rollout.** Stage 0, shadow: on 5 closed matters the attorney approves, each paralegal builds her chronology as usual while the tool builds its own, and we compare. Nothing it makes goes in a letter. Stage 1: two paralegals on live matters (none on a Stowers deadline at first), only once recall on Zinda's own test set meets the bar. Stage 2: the whole team. What I'd send the signing attorney today, on Part 1's numbers:

> Subject: Go on a shadow run, no-go on live matters yet
>
> [Name], where it stands:
>
> - Every letter line and amount quotes the record word for word: 242 of 242. Planted wrong summaries caught: 40 of 40. Diagnoses or causes the record doesn't state: 0.
> - Below the bar: on 15 unfamiliar packets it found 78% of treatment entries and 68% of charges (bar: 95%), and 34 of 42 warnings. Trusted, that means missed visits and an under-stated demand, so the paralegals still read every record and bill.
>
> So: go on a shadow run on 5 closed matters you pick, inside our environment. Live matters wait until recall on our own test set meets the bar; then I ask again. Once live, the paralegals check each line against its quote before accepting it, and you check the letter lines against their quotes before you sign, all of them at first, then a sample we agree on. Texas Opinion 705 says the lawyer always verifies AI output. The tool makes that check fast; it never replaces it. Records go to [vendor] under terms you've reviewed: no training on our data, [N]-day retention. Whether our engagement letters cover that, or clients must consent, is your call. One unsupported fact in a draft and we pause. One that reaches a carrier and we stop; you hear that day, and you decide the correction. Yes, no, or "yes, but" by Thursday? Chris

**Feedback.** A 20-minute weekly check-in per paralegal, plus the audit log: every accept, edit and dismiss, with before and after, so I see where it was wrong without asking.

| Measure | Definition | Expand if | Kill if |
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:20.020Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/part2-process.md'\ns=open(p).read()\na=\"> So: go on a shadow run on 5 closed matters you pick, inside our environment. Live matters wait until recall on our own test set meets the bar; then I ask again. Once live,\"\nb=\" Records go to [vendor] under terms you've reviewed: no training on our data, [N]-day retention. Whether our engagement letters cover that, or clients must consent, is your call.\"\nassert s.count(a)==1 and s.count(b)==1\ns=s.replace(b,\"\")\ns=s.replace(a,\"> So: go on a shadow run on 5 closed matters you pick, inside our environment. Their records go to [vendor] under terms you've reviewed: no training on our data, [N]-day retention. Whether our engagement letters cover that, or clients must consent, is your call. Live matters wait until recall on our own test set meets the bar; then I ask again. Once live,\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\npython3 - \"$S/paths.txt\" <<'EOF'\nimport sys,subprocess,os\nfor l in open(sys.argv[1]):\n    p=l.strip()\n    if '/' in p and ' ' not in p:\n        q=p if not p.startswith('prompt-log') else 'submission/'+p\n        r=subprocess.run(['git','ls-files','--error-unmatch',q.rstrip('/')],capture_output=True)\n        ok = r.returncode==0 or os.path.isdir(q)\n        if not ok: print('MISSING',p)\nEOF",
 "description": "Reorder vendor sentence, render, check cited paths"
}
````

### User / tool · 2026-11-03T21:38:22.517Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 4 page(s)
MISSING reviews/T-218-product-manager.md
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:24.944Z

**tool call — Bash**
````
{
 "command": "ls reviews/T-218-product-manager.md submission/prompt-log/reviews/T-218* 2>&1; git ls-files | grep T-218 | head",
 "description": "Locate T-218 review file"
}
````

### User / tool · 2026-11-03T21:38:25.051Z

**tool result**
````
reviews/T-218-product-manager.md
submission/prompt-log/reviews/T-218-product-manager.md
board/cards/T-218.md
submission/prompt-log/reviews/T-218-product-manager.md
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:27.787Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's#(`reviews/T-218-product-manager.md`)#(`prompt-log/reviews/T-218-product-manager.md`)#' submission/product-note.md && grep -c \"prompt-log/reviews/T-218\" submission/product-note.md && bash submission/build_pdfs.sh && git diff --stat HEAD -- submission/",
 "description": "Fix product note citation and rebuild"
}
````

### User / tool · 2026-11-03T21:38:29.679Z

**tool result**
````
1
product-note.pdf: 2 page(s)
part2-process.pdf: 4 page(s)
 submission/build_pdfs.sh     |   2 +-
 submission/part2-process.md  |  62 ++++++++++++++++++++-----------------------
 submission/part2-process.pdf | Bin 263917 -> 266218 bytes
 submission/product-note.md   |   6 ++---
 submission/product-note.pdf  | Bin 113798 -> 114985 bytes
 5 files changed, 33 insertions(+), 37 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:33.849Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/product-note.md'\ns=open(p).read()\na=\"Prompt log: final, e0d721d; M4 passed after the final privacy sweep (`reviews/GATE-M4-summary.md`).\"\nassert s.count(a)==1\ns=s.replace(a,\"Prompt log final (e0d721d); M4 passed its privacy sweep (`reviews/GATE-M4-summary.md`).\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh",
 "description": "Shorten product note line, rebuild"
}
````

### User / tool · 2026-11-03T21:38:35.813Z

**tool result**
````
product-note.pdf: 2 page(s)
part2-process.pdf: 4 page(s)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:37.533Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/submission && pdftotext -f 2 -l 2 product-note.pdf - ; git diff HEAD -- product-note.md",
 "description": "See product note overflow and diff"
}
````

### User / tool · 2026-11-03T21:38:37.674Z

**tool result**
````
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit log.

diff --git a/submission/product-note.md b/submission/product-note.md
index 194ac6d..ba40c4d 100644
--- a/submission/product-note.md
+++ b/submission/product-note.md
@@ -16,16 +16,16 @@ Chris [CHRIS: full name] · Zlayt PM project, Part 1 · demo: [CHRIS: public lin
 | 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (93/120; 47/69). Misses: ledgers, letters, cloned notes, Spanish, EOBs |
 | 3 | Flags: precision, recall 0.9 per type; 28-day gap not flagged, 73-day flagged | golden: 1.000/1.000, four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |
 | 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12 [E] |
-| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; unit re-run at HEAD (cd7fd27 changed only the label): 5,951 passed, 0 failed (`reviews/T-218-product-manager.md`); letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`) |
+| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; unit re-run at HEAD (cd7fd27 changed only the label): 5,951 passed, 0 failed (`prompt-log/reviews/T-218-product-manager.md`); letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`) |
 
-**Ship call.** Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow beside a paralegal's own chronology (Part 2, area 5), not live matters, until library recall meets the bar.
+**Ship call.** Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow beside a paralegal's own chronology (Part 2, area 5), not live matters until recall meets the bar on the library and on Zinda's own test set.
 
 **What testing found.**
 
 - **Reviewability passed on paper, failed in use.** A persona scored the M3 screen 4/5; I found it *very* hard to use. It is now four fixed steps (D-068); a UX reviewer passed it on desktop and a 390 px phone.
 - **The 1.000 flag numbers do not generalize.** Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81 (`submission/prompt-log/reviews/GATE-M3-product-manager.md`, `memory/SCOPE_CUTS.md` rows 13, 23). Misses: conflicts code never proposes ("Left" vs "Right shoulder pain").
 - **Billing took four adversarial rounds.** An adjuster reviewer outworded every word-list rule: a letter said $16,147, true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records". Date reading failed the same way; after six rounds the pre-declared fallback applies: every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (D-073, `memory/SCOPE_CUTS.md` row 28).
-- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).
+- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log final (e0d721d); M4 passed its privacy sweep (`reviews/GATE-M4-summary.md`).
 
 **How the AI can mislead her, and what the design does.**
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:42.469Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"So: stage-0 shadow beside a paralegal's own chronology (Part 2, area 5), not live matters until recall meets the bar on the library and on Zinda's own test set.\",\n\"So: a stage-0 shadow beside a paralegal's own chronology (Part 2, area 5); live matters wait until recall meets the bar here and on Zinda's own test set.\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh",
 "description": "Shorten ship call, rebuild"
}
````

### User / tool · 2026-11-03T21:38:44.415Z

**tool result**
````
product-note.pdf: 2 page(s)
part2-process.pdf: 4 page(s)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:49.506Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1, a[:60]\n    s=s.replace(a,b)\nrep(\"live matters wait until recall meets the bar here and on Zinda's own test set.\",\"live matters wait until recall meets the bar on the library and Zinda's own test set.\")\nrep(\"unit re-run at HEAD (cd7fd27 changed only the label): 5,951\",\"unit re-run at cd7fd27 (label change only): 5,951\")\nopen(p,'w').write(s)\nEOF\nbash submission/build_pdfs.sh",
 "description": "Tighten product note, rebuild"
}
````

### User / tool · 2026-11-03T21:38:51.302Z

**tool result**
````
product-note.pdf: 1 page(s)
part2-process.pdf: 4 page(s)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:54.071Z

**tool call — Bash**
````
{
 "command": "grep -n \"cd7fd27\\|5,951\\|5951\" submission/prompt-log/reviews/T-218-product-manager.md | head -5",
 "description": "Verify re-run commit in T-218 review"
}
````

### User / tool · 2026-11-03T21:38:54.154Z

**tool result**
````
17:- **Check I ran beyond your list:** a fresh `git archive HEAD` unit run (ANTHROPIC_API_KEY unset) gave **5951 passed, 6 skipped, 0 failed** in 466 s. The skip count differs from the file's 12 and the total is the same, 5957, so it is an environment difference. `python -m evals.letter_check` at HEAD returns value 0 over 25 cases. I did not re-run e2e at HEAD (about 14 min), so I make no claim about it.
25: "scope": "HEAD e0d721d (T-218 fixes in c2dd104 and a932fc9; D-075 code change cd7fd27 after them); submission/{product-note,part2-process}.md + PDFs, SUBMISSION_CHECKLIST.md, NEEDS_CHRIS.md, email-draft.md, artifacts/{demo.webm,demo.vtt,gate-M3M4-suite-final.txt}; no app URL used; sample case via the video",
28:  "git rev-parse --short HEAD gives e0d721d; git log for the video, PDFs, notes and service_date.py; git show --stat c2dd104 and cd7fd27",
33:  "git archive HEAD into artifacts/review-evidence/T-218-pm/tree; pytest tests/unit there: 5951 passed, 6 skipped, 0 failed (artifacts/review-evidence/T-218-pm/unit-head.txt)",
41:   "evidence": "product-note.md:25 and part2-process.md:116: 'a fillable \"date of service [__________]\" with the record or statement date in parentheses, and no service date is extracted'. HEAD docs/LLM_VS_CODE.md:31 and memory/SCOPE_CUTS.md:113 say '(record dated X)', and the video frames t156 and t162 show '(record dated ...)'. cd7fd27 (D-075) made the label always 'record'",
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:38:57.086Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's#unit re-run at cd7fd27 (label change only): 5,951#unit re-run at e0d721d (label change only): 5,951#' submission/product-note.md && grep -c \"e0d721d (label\" submission/product-note.md && bash submission/build_pdfs.sh",
 "description": "Correct re-run commit, rebuild"
}
````

### User / tool · 2026-11-03T21:38:59.086Z

**tool result**
````
1
product-note.pdf: 1 page(s)
part2-process.pdf: 4 page(s)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:01.433Z

**tool call — Bash**
````
{
 "command": "grep -o \"\\[CHRIS\" submission/part2-process.md | wc -l; sed -n 23,36p submission/part2-process.md; sed -n 136,148p submission/part2-process.md",
 "description": "Recheck placeholders and edited areas"
}
````

### User / tool · 2026-11-03T21:39:01.535Z

**tool result**
````
       6
> Subject: Treatment chronologies, 30 minutes this week?
>
> [Name], thanks for the ask. Before I build anything I want to see where the time goes and what a mistake costs you. Could I get 30 minutes with you, 20 each with two paralegals who build chronologies, and, if the responsible attorney approves one, a redacted closed matter with its chronology, demand letter and the adjuster's reply? It stays on your systems; I note steps, not content. A week later you get one page: what I saw, what I'd build first, how we'll know it works. Chris

| First three questions for the litigation lead | First three for a paralegal |
|----------------------|----------------------|
| "Take the last demand letter that went out. Where did the chronology hold it up?" | "Walk me through the last chronology you built, from the first record you opened." |
| "Last time an adjuster pushed back on a date or a fact, what did it cost? Days, or dollars off the offer?" | "Which entries do you always re-check against the source? Which one burned you?" |
| "What will you never let software write in a letter? What would you check before you signed one it helped with?" | "When two records disagree or there's a long gap, where do you write that down, and who sees it?" |

**Request versus need.** The request is "faster." The need is faster without a new way to be wrong. I ask for artifacts, not opinions, and compare what people say with what they did. Every time she opens the source to check a line, I mark it. That's the step the tool has to make cheap, not remove.

**Watching real work, with the attorney's sign-off.** A closed file is still client confidential: Texas Rule 1.05 covers former clients too, so "I won't copy anything" isn't the protection. The default is synthetic records, like Part 1, or a redacted copy. A real closed matter only if the responsible attorney picks and approves it first, under the firm's confidentiality agreement; it stays in Zinda's environment, nothing leaves, access is logged. Here I had no access to Zinda's people, so I wrote nine assumptions, each with "what changes if wrong," and had 13 persona dossiers researched. A stand-in, not the real thing. [CHRIS: optional, one line on a time you watched real work without exposing customer data.]


**Honest feedback from busy people.** I don't ask whether they like it. I put output in front of them and ask them to find the error. I sit with paralegals without the lead in the room; people say less in front of whoever assigns their work.

> Subject: 20 minutes on one chronology?
>
> Hi [name], I'm building the tool that drafts treatment chronologies, and I need to hear where it's wrong, not whether it's nice. 20 minutes at your desk this week? Build a chronology the way you normally do while I watch, from the redacted closed matter [attorney] cleared for this. It stays on Zinda's system. Then you mark up one the tool made. If this week is bad, just say "not this week." Chris

**The find-the-error ask**, handed over with a printed chronology:

> This one's from a synthetic packet built like ours. I planted five mistakes in it, mixed in with whatever the tool got wrong on its own. Circle every line you wouldn't put in a letter. Ten minutes. Don't be nice.

**Agenda, 30 minutes, one paralegal.** 0-3: why I'm here, and which records we use (synthetic, or the matter [attorney] cleared). 3-13: you walk me through it. 13-23: you mark the tool's chronology, lines you'd trust and lines you wouldn't, and why. 23-28: what would make you stop using it. 28-30: what I'll change, and when you'll hear back.
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:06.195Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t219r2.index && git read-tree HEAD && git add submission/part2-process.md submission/part2-process.pdf submission/product-note.md submission/product-note.pdf submission/build_pdfs.sh && git diff --cached --stat HEAD",
 "description": "Stage submission files in temp index"
}
````

### User / tool · 2026-11-03T21:39:06.428Z

**tool result**
````
 submission/build_pdfs.sh     |   2 +-
 submission/part2-process.md  |  62 ++++++++++++++++++++-----------------------
 submission/part2-process.pdf | Bin 263917 -> 266218 bytes
 submission/product-note.md   |   6 ++---
 submission/product-note.pdf  | Bin 113798 -> 114064 bytes
 5 files changed, 33 insertions(+), 37 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:11.979Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t219r2.index git commit -q -m \"docs(writer): T-219 r2 Part 2 confidentiality and supervision fixes\n\nClosed matters only with responsible-attorney approval (Rule 1.05 covers\nformer clients); synthetic/redacted by default. Go/no-go states library\nrecall (0.775/0.681), asks for shadow only, frames Op. 705 as the lawyer\nverifying, adds vendor terms and consent. Kill line: one fact at a carrier.\nProduct note ship call aligned; stale M4 line and T-218 path fixed.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log --oneline -1",
 "description": "Commit with temp index"
}
````

### User / tool · 2026-11-03T21:39:13.224Z

**tool result**
````
check_secrets: ok (5 file(s) scanned staged)
67128ae docs(writer): T-219 r2 Part 2 confidentiality and supervision fixes
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:21.193Z

**tool call — Bash**
````
{
 "command": "git reset -q -- submission; git status --short submission/; B=\"python3 tools/board.py\"; $B commit T-219 --sha 67128ae --agent writer; $B ac T-219 --check 1 --agent writer --evidence \"67128ae: all 8 areas, questions and messages kept; blockers fixed (attorney-approved closed matters, Rule 1.05 former clients, synthetic/redacted default; go/no-go lists library 0.775/0.681 and asks shadow only, live waits for Zinda test-set recall; Op. 705 = lawyer verifies, tool makes it fast); majors fixed (kill at one fact at a carrier + same-day attorney notice; vendor terms, BAA, consent; attorney not founders decides client data); minor Stowers added; product note ship call aligned; build_pdfs.sh -> part2 4 pages (9.3pt), product note 1\"; $B handoff T-219 --agent writer --text \"What changed: area 1 retitled 'with the attorney's sign-off' (Rule 1.05 covers former clients; synthetic/redacted default; real closed matter only if responsible attorney approves, Zinda env only, nothing leaves, logged); kickoff, paralegal ask, find-the-error (now synthetic), agenda match. Go/no-go now 'go on shadow, no-go on live yet': states 78%/68% entries/charges and 34/42 warnings, live waits for recall on Zinda's test set; paralegals check each line vs quote, attorney checks letter lines before signing, Op. 705 = lawyer verifies, tool makes it fast, never replaces it; vendor terms + consent are the attorney's call; one fact at a carrier = stop, attorney told that day. Kill row: one fact. Test set: vendor terms, BAA, de-identify, consent; area 6 client data = responsible attorney. Stowers in area 2 and stage 1. Recall row shows library. Product note ship call aligned; stale 'M4 pending' and untracked T-218 path fixed. How verified: bash submission/build_pdfs.sh -> 4 + 1 pages; cited paths in git ls-files; 6 [CHRIS] markers unchanged. Left: PM review items if any. Surprised: fit needed 9.3pt (was 9.4) after ~25 lines of trims.\"; $B move T-219 in_review --agent writer",
 "description": "Resync index, record commit, AC, handoff, move"
}
````

### User / tool · 2026-11-03T21:39:21.577Z

**tool result**
````
T-219: commit 67128ae recorded
AC 1 checked: 67128ae: all 8 areas, questions and messages kept; blockers fixed (attorney-approved closed matters, Rule 1.05 former clients, synthetic/redacted default; go/no-go lists library 0.775/0.681 and asks shadow only, live waits for Zinda test-set recall; Op. 705 = lawyer verifies, tool makes it fast); majors fixed (kill at one fact at a carrier + same-day attorney notice; vendor terms, BAA, consent; attorney not founders decides client data); minor Stowers added; product note ship call aligned; build_pdfs.sh -> part2 4 pages (9.3pt), product note 1
handoff written on T-219
T-219: in_progress -> in_review
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:22.537Z

Updating my memory with the round-2 findings.

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:26.823Z

**tool call — Bash**
````
{
 "command": "cat >> .claude/agent-memory/writer/submission_pipeline.md <<'EOF'\n\n**T-219 r2 (litigation-lead fail, 67128ae):** lawyer-persona blockers to pre-empt in any people-facing doc: (1) never have a paralegal \"pick a closed matter\" or show one to an outside PM; Texas Rule 1.05 covers former clients, so default synthetic/redacted, real matter only with responsible-attorney approval, Zinda env only, logged; (2) never say reading notes \"is the verification Op. 705 expects\": the lawyer verifies AI output, the tool makes the check fast; (3) any go/no-go must show every below-bar number (library 0.775/0.681/0.81) and match the product note's ship call (shadow first, live waits for recall on Zinda's own test set); (4) kill line is ONE unsupported fact at a carrier; (5) client-data use is the responsible attorney's call, not founders; name vendor terms/BAA/consent. Page fit: Part 2 now 9.3pt in build_pdfs.sh. Product-note cites must be `prompt-log/reviews/...` (top-level `reviews/T-218-*` is untracked).\nEOF",
 "description": "Append round-2 lessons to writer memory"
}
````

### User / tool · 2026-11-03T21:39:26.913Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T21:39:28.749Z

I fixed all three blockers, both majors and the Stowers minor, and lined the product note's ship call up with Part 2 (shadow first, live only once recall meets the bar on Zinda's own test set). Committed 67128ae, which touches `submission/` only; the card is in review. Part 2 renders at 4 pages, but only after I cut the font from 9.4 to 9.3pt, and the product note is 1 page.
