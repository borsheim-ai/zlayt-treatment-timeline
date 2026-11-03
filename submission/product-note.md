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
| 4 | No invented facts: 0 unsupported over 3 runs; code check and judge catch 95% of seeded wrong summaries | 0; 40/40 together (code alone 31); 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12 [E] |
| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; unit re-run at e0d721d (label change only): 5,951 passed, 0 failed (`prompt-log/reviews/T-218-product-manager.md`); letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`) |

**Ship call.** Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: a stage-0 shadow beside a paralegal's own chronology (Part 2, area 5); live matters wait until recall meets the bar on the library and Zinda's own test set.

**What testing found.**

- **Reviewability passed on paper, failed in use.** A persona scored the M3 screen 4/5; I found it *very* hard to use. It is now four fixed steps (D-068); a UX reviewer passed it on desktop and a 390 px phone.
- **The 1.000 flag numbers do not generalize.** Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81 (`submission/prompt-log/reviews/GATE-M3-product-manager.md`, `memory/SCOPE_CUTS.md` rows 13, 23). Misses: conflicts code never proposes ("Left" vs "Right shoulder pain").
- **Billing took four adversarial rounds.** An adjuster reviewer outworded every word-list rule: a letter said $16,147, true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records". Date reading failed the same way; after six rounds the pre-declared fallback applies: every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (D-073, `memory/SCOPE_CUTS.md` row 28).
- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log final (e0d721d); M4 passed its privacy sweep (`reviews/GATE-M4-summary.md`).

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
