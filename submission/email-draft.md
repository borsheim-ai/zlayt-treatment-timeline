**To:** [CHRIS: address of the Zlayt contact who sent the project; reply on that thread]
**Subject:** Re: [CHRIS: subject of the original email] — treatment timeline project

Hi [CHRIS: first name of the Zlayt contact],

My project is below. Everything uses synthetic records only.

**Demo:** [CHRIS: link to the running demo]
**Repo:** https://github.com/borsheim-ai/zlayt-treatment-timeline

Start with `README.md` in the repo. It has the two-command setup from a fresh clone (17 seconds when we timed it, no API key needed), a three-minute walk through the demo, and where the second AI check and the human review step live in the code.

The rest is in the repo under `submission/`:

- **Product note** (one page): `submission/product-note.md`, PDF `submission/product-note.pdf`
- **Part 2** (four pages, with the validation-ladder diagram): `submission/part2-process.md`, PDF `submission/part2-process.pdf`
- **Prompts and conversations:** `submission/prompt-log/`, starting with its `README.md`
- **Demo recording and screenshots:** `artifacts/demo.webm` (under 3 minutes, sample case) and 72 annotated screenshots in `artifacts/screenshots/final/`, with `artifacts/CAPTIONS.md`
- **Checklist of what is where:** `submission/SUBMISSION_CHECKLIST.md`

What I built: a paralegal pastes records and gets a timeline where every line sits next to the exact quote it came from. Code does the dates, gaps, dollar amounts and totals. The model writes the one-line summaries and the second check reads them against the quote. She accepts, edits or dismisses every item, and the letter text contains only what she accepted.

Three things you should know before you open it:

1. The ship bar is met on my golden set (flags 1.000, no invented facts over three live runs). On 15 separate test packets written after the golden set, recall is lower: entries 0.775, amounts 0.681, must-flags 0.81. The product note says so.
2. The "easy to verify" score of 4 out of 5 comes from an AI reviewer standing in for a paralegal, not from a real paralegal. I have not had a real one use it.
3. I built it with a team of Claude Code agents that I directed and reviewed through a task board. The prompt log shows how.

I know the brief asked for one stretch item and I shipped three; the note explains why.

[CHRIS: optional, one sentence on when you are available to walk through it.]

Thanks,
[CHRIS: full name]
